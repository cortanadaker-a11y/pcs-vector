"""Serialize PCS form payloads into Stripe Checkout metadata for post-redirect restore."""

from __future__ import annotations

import base64
import json
import logging
import zlib
from typing import Any

logger = logging.getLogger(__name__)

FORM_METADATA_VERSION = "1"
FORM_CHUNK_SIZE = 450  # Stripe metadata values max 500 chars


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


def pack_form_data_for_stripe(form_data: dict[str, Any]) -> dict[str, str]:
    """Compress form data into Stripe-safe metadata chunks."""
    metadata: dict[str, str] = {
        "product": "pcs_vector_report",
        "fd_v": FORM_METADATA_VERSION,
    }
    raw = json.dumps(form_data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    compressed = zlib.compress(raw, level=9)
    encoded = base64.urlsafe_b64encode(compressed).decode("ascii")
    chunks = [
        encoded[offset : offset + FORM_CHUNK_SIZE]
        for offset in range(0, len(encoded), FORM_CHUNK_SIZE)
    ]
    metadata["fd_n"] = str(len(chunks))
    for index, chunk in enumerate(chunks):
        metadata[f"fd_{index}"] = chunk
    return metadata


def unpack_form_data_from_stripe(metadata: Any) -> dict[str, Any] | None:
    """Restore form data previously stored on a Checkout session."""
    safe_metadata = normalize_stripe_metadata(metadata)
    if safe_metadata.get("product") != "pcs_vector_report":
        return None

    try:
        chunk_count = int(safe_metadata.get("fd_n", "0"))
        if chunk_count <= 0:
            return None

        encoded_parts: list[str] = []
        for index in range(chunk_count):
            chunk_key = f"fd_{index}"
            if chunk_key not in safe_metadata:
                logger.warning("Stripe metadata missing chunk %s", chunk_key)
                return None
            encoded_parts.append(safe_metadata[chunk_key])

        encoded = "".join(encoded_parts)
        compressed = base64.urlsafe_b64decode(encoded.encode("ascii"))
        raw = zlib.decompress(compressed)
        data = json.loads(raw.decode("utf-8"))
        if isinstance(data, dict):
            return data
    except (KeyError, ValueError, json.JSONDecodeError, OSError, zlib.error) as exc:
        logger.warning("Could not unpack form metadata: %s", exc)
        return None
    return None