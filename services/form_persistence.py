"""Serialize PCS form payloads into Stripe Checkout metadata for post-redirect restore."""

from __future__ import annotations

import base64
import json
import zlib
from typing import Any

FORM_METADATA_VERSION = "1"
FORM_CHUNK_SIZE = 450  # Stripe metadata values max 500 chars


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


def unpack_form_data_from_stripe(metadata: dict[str, str] | None) -> dict[str, Any] | None:
    """Restore form data previously stored on a Checkout session."""
    if not metadata or metadata.get("product") != "pcs_vector_report":
        return None

    try:
        chunk_count = int(metadata.get("fd_n", "0"))
        if chunk_count <= 0:
            return None
        encoded = "".join(metadata.get(f"fd_{index}", "") for index in range(chunk_count))
        compressed = base64.urlsafe_b64decode(encoded.encode("ascii"))
        raw = zlib.decompress(compressed)
        data = json.loads(raw.decode("utf-8"))
        if isinstance(data, dict):
            return data
    except (ValueError, json.JSONDecodeError, OSError, zlib.error):
        return None
    return None