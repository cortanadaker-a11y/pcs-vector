"""Serialize PCS form payloads into Stripe Checkout metadata for post-redirect restore."""

from __future__ import annotations

import base64
import json
import logging
import zlib
from typing import Any

logger = logging.getLogger(__name__)

FORM_METADATA_VERSION = "2"
FORM_CHUNK_SIZE = 450  # Stripe metadata values max 500 chars
MIN_BACKUP_CHUNK_SIZE = 500
MAX_METADATA_KEYS = 45  # leave room for product, fd_v, fd_n, fd_min/fm_*

# Short keys keep the compressed payload small enough for Stripe metadata limits.
FULL_TO_COMPACT: dict[str, str] = {
    "first_name": "fn",
    "last_name": "ln",
    "rank_pay_grade": "rg",
    "rank_title": "rt",
    "current_installation_preset": "cip",
    "current_installation_other": "cio",
    "gaining_installation": "gi",
    "gaining_installation_other": "gio",
    "move_window": "mw",
    "move_flexibility": "mf",
    "spouse_career_field": "scf",
    "spouse_career_other": "sco",
    "num_children": "nc",
    "child_age_ranges": "car",
    "has_pets": "hp",
    "pet_types": "pt",
    "pet_details": "pd",
    "housing_preference": "hpr",
    "budget_mode": "bm",
    "budget_preset": "bp",
    "max_monthly_budget": "mmb",
    "housing_must_haves_selected": "hmh",
    "housing_must_haves_other": "hmo",
    "primary_priority": "pp",
    "secondary_priority": "sp",
    "other_priorities": "op",
    "num_vehicles": "nv",
    "dity_interest": "di",
    "concern_flags": "cf",
    "specific_concerns": "sc",
    "form_submitted": "fs",
}
COMPACT_TO_FULL = {short: full for full, short in FULL_TO_COMPACT.items()}


def normalize_stripe_metadata(metadata: Any) -> dict[str, str]:
    """Safely convert Stripe metadata objects into a plain string dict."""
    if metadata is None:
        return {}

    normalized: dict[str, str] = {}
    try:
        if isinstance(metadata, dict):
            items = metadata.items()
        elif hasattr(metadata, "keys"):
            items = ((key, metadata[key]) for key in metadata.keys())
        else:
            return {}

        for key, value in items:
            if value is None:
                continue
            normalized[str(key)] = str(value)
    except (KeyError, TypeError, AttributeError) as exc:
        logger.warning("Could not read Stripe metadata: %s", exc)
        return normalized

    return normalized


def compact_form_data(form_data: dict[str, Any]) -> dict[str, Any]:
    """Use short keys and omit empty values to reduce payload size."""
    compact: dict[str, Any] = {}
    for full_key, short_key in FULL_TO_COMPACT.items():
        value = form_data.get(full_key)
        if value is None:
            continue
        if value == "" or value == [] or value is False:
            continue
        if full_key == "num_children" and value == 0:
            continue
        compact[short_key] = value
    compact["fs"] = True
    return compact


def _is_full_form_payload(payload: dict[str, Any]) -> bool:
    return any(key in payload for key in FULL_TO_COMPACT)


def expand_form_data(compact: dict[str, Any]) -> dict[str, Any]:
    """Expand compact keys back into the full form schema."""
    if _is_full_form_payload(compact):
        return compact

    expanded: dict[str, Any] = {}
    for short_key, value in compact.items():
        full_key = COMPACT_TO_FULL.get(short_key, short_key)
        expanded[full_key] = value
    if "form_submitted" not in expanded and compact.get("fs"):
        expanded["form_submitted"] = True
    return expanded


def _encode_payload(payload: dict[str, Any]) -> tuple[str, int]:
    raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode("utf-8")
    compressed = zlib.compress(raw, level=9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    chunks = [
        encoded[offset : offset + FORM_CHUNK_SIZE]
        for offset in range(0, len(encoded), FORM_CHUNK_SIZE)
    ]
    return encoded, len(chunks)


def pack_form_data_for_stripe(form_data: dict[str, Any]) -> dict[str, str]:
    """Compress form data into Stripe-safe metadata chunks plus a minimal backup."""
    compact = compact_form_data(form_data)
    _, chunk_count = _encode_payload(compact)
    if chunk_count > MAX_METADATA_KEYS:
        raise ValueError(
            f"Form payload requires {chunk_count} metadata chunks; Stripe allows {MAX_METADATA_KEYS}."
        )

    metadata: dict[str, str] = {
        "product": "pcs_vector_report",
        "fd_v": FORM_METADATA_VERSION,
        "fd_n": str(chunk_count),
    }

    encoded, _ = _encode_payload(compact)
    for index in range(chunk_count):
        start = index * FORM_CHUNK_SIZE
        metadata[f"fd_{index}"] = encoded[start : start + FORM_CHUNK_SIZE]

    minimal_json = json.dumps(compact, separators=(",", ":"), sort_keys=True, ensure_ascii=True)
    if len(minimal_json) <= MIN_BACKUP_CHUNK_SIZE:
        metadata["fd_min"] = minimal_json
    else:
        fm_chunks = [
            minimal_json[offset : offset + MIN_BACKUP_CHUNK_SIZE]
            for offset in range(0, len(minimal_json), MIN_BACKUP_CHUNK_SIZE)
        ]
        metadata["fm_n"] = str(len(fm_chunks))
        for index, chunk in enumerate(fm_chunks):
            metadata[f"fm_{index}"] = chunk

    return metadata


def _decode_chunk_payload(encoded: str) -> dict[str, Any] | None:
    compressed = base64.urlsafe_b64decode(encoded.encode("ascii"))
    raw = zlib.decompress(compressed)
    data = json.loads(raw.decode("utf-8"))
    if isinstance(data, dict):
        return data
    return None


def _collect_chunked_payload(safe_metadata: dict[str, str]) -> str | None:
    chunk_count = int(safe_metadata.get("fd_n", "0") or "0")
    if chunk_count <= 0:
        return None

    encoded_parts: list[str] = []
    for index in range(chunk_count):
        chunk_key = f"fd_{index}"
        chunk = safe_metadata.get(chunk_key)
        if not chunk:
            logger.warning("Stripe metadata missing chunk %s", chunk_key)
            return None
        encoded_parts.append(chunk)
    return "".join(encoded_parts)


def unpack_form_data_from_stripe(metadata: Any) -> dict[str, Any] | None:
    """Restore form data previously stored on a Checkout session."""
    safe_metadata = normalize_stripe_metadata(metadata)
    if safe_metadata.get("product") != "pcs_vector_report":
        return None

    # 1) Full chunked payload
    try:
        encoded = _collect_chunked_payload(safe_metadata)
        if encoded:
            compact = _decode_chunk_payload(encoded)
            if compact:
                expanded = expand_form_data(compact)
                if expanded.get("form_submitted"):
                    return expanded
    except (ValueError, json.JSONDecodeError, OSError, zlib.error, KeyError) as exc:
        logger.warning("Could not unpack chunked form metadata: %s", exc)

    # 2) Minimal inline or split backup
    minimal_raw = _read_min_backup(safe_metadata)
    if minimal_raw:
        try:
            compact = json.loads(minimal_raw)
            if isinstance(compact, dict):
                expanded = expand_form_data(compact)
                if expanded.get("form_submitted"):
                    logger.info("Restored form data from Stripe minimal backup.")
                    return expanded
        except (json.JSONDecodeError, TypeError, ValueError) as exc:
            logger.warning("Could not unpack minimal backup: %s", exc)

    return None


def _read_min_backup(safe_metadata: dict[str, str]) -> str:
    if safe_metadata.get("fd_min"):
        return safe_metadata["fd_min"]
    fm_count = int(safe_metadata.get("fm_n", "0") or "0")
    if fm_count <= 0:
        return ""
    parts = [safe_metadata.get(f"fm_{index}", "") for index in range(fm_count)]
    if any(not part for part in parts):
        return ""
    return "".join(parts)


def _values_equal(left: Any, right: Any) -> bool:
    if left == right:
        return True
    if isinstance(left, (int, float)) and isinstance(right, (int, float)):
        if float(left).is_integer() and float(right).is_integer():
            return int(left) == int(right)
    return False


def _compacts_equivalent(left: dict[str, Any], right: dict[str, Any]) -> bool:
    if set(left.keys()) != set(right.keys()):
        logger.warning("Compact metadata key mismatch: %s", set(left.keys()) ^ set(right.keys()))
        return False
    return all(_values_equal(left[key], right[key]) for key in left)


def verify_packed_metadata(metadata: dict[str, str], form_data: dict[str, Any]) -> bool:
    """Confirm packed metadata round-trips to submitted form data."""
    restored = unpack_form_data_from_stripe(metadata)
    if not restored or not restored.get("form_submitted"):
        logger.warning("Packed metadata did not restore a submitted form.")
        return False
    submitted = compact_form_data(form_data)
    restored_compact = compact_form_data(restored)
    return _compacts_equivalent(submitted, restored_compact)