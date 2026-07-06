"""Temporary server-side storage for checkout form data.

After payment, users often land in a fresh Streamlit browser session. Stripe
Checkout metadata is a useful backup but is size-limited and can fail on large
payloads. This module is the PRIMARY restore path: full form JSON keyed by:
  - Stripe Checkout session_id
  - A pre-checkout draft_id (also stored in Stripe metadata as pcs_draft)

Implementation:
  - JSON files under data/checkout_forms/ and data/checkout_drafts/
  - In-process memory cache for fast repeat reads in the same worker
  - TTL-based expiry so stale drafts do not accumulate forever
  - PCS_VECTOR_DATA_DIR env override for deployments with ephemeral filesystems
"""

from __future__ import annotations

import json
import logging
import os
import re
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

DEFAULT_TTL_SECONDS = 72 * 3600  # 72 hours

_SESSION_ID_PATTERN = re.compile(r"^cs_(test|live)_[a-zA-Z0-9]+$")
_DRAFT_ID_PATTERN = re.compile(r"^[a-f0-9]{32}$")

# In-memory cache: storage_key -> (expires_at_unix, form_data)
_memory_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _data_root() -> Path:
    override = os.environ.get("PCS_VECTOR_DATA_DIR", "").strip()
    if override:
        root = Path(override)
    else:
        root = _project_root() / "data"
    root.mkdir(parents=True, exist_ok=True)
    return root


def get_store_dir() -> Path:
    """Directory for per-session JSON files (created on demand)."""
    store_dir = _data_root() / "checkout_forms"
    store_dir.mkdir(parents=True, exist_ok=True)
    return store_dir


def get_draft_dir() -> Path:
    """Directory for pre-checkout draft JSON files."""
    draft_dir = _data_root() / "checkout_drafts"
    draft_dir.mkdir(parents=True, exist_ok=True)
    return draft_dir


def _is_valid_session_id(session_id: str) -> bool:
    return bool(session_id and _SESSION_ID_PATTERN.match(session_id))


def _is_valid_draft_id(draft_id: str) -> bool:
    return bool(draft_id and _DRAFT_ID_PATTERN.match(draft_id))


def _session_file_path(session_id: str) -> Path | None:
    if not _is_valid_session_id(session_id):
        logger.warning(
            "Refusing checkout form store access for invalid session_id: %s",
            (session_id or "")[:24],
        )
        return None
    return get_store_dir() / f"{session_id}.json"


def _draft_file_path(draft_id: str) -> Path | None:
    if not _is_valid_draft_id(draft_id):
        logger.warning(
            "Refusing draft store access for invalid draft_id: %s",
            (draft_id or "")[:24],
        )
        return None
    return get_draft_dir() / f"{draft_id}.json"


def _read_payload(path: Path) -> dict[str, Any] | None:
    try:
        with path.open("r", encoding="utf-8") as handle:
            payload = json.load(handle)
        return payload if isinstance(payload, dict) else None
    except (OSError, json.JSONDecodeError) as exc:
        logger.warning("Could not read checkout form file %s: %s", path.name, exc)
        return None


def _write_payload(path: Path, payload: dict[str, Any]) -> bool:
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = path.with_suffix(".json.tmp")
        with temp_path.open("w", encoding="utf-8") as handle:
            json.dump(payload, handle, separators=(",", ":"), sort_keys=True)
        temp_path.replace(path)
        return True
    except OSError as exc:
        logger.warning("Could not write checkout form file %s: %s", path.name, exc)
        return False


def _payload_expired(payload: dict[str, Any], *, ttl_seconds: int) -> bool:
    saved_at = float(payload.get("saved_at", 0) or 0)
    stored_ttl = int(payload.get("ttl_seconds", ttl_seconds) or ttl_seconds)
    if saved_at <= 0:
        return True
    return time.time() > saved_at + stored_ttl


def _cache_put(cache_key: str, form_data: dict[str, Any], *, ttl_seconds: int) -> None:
    _memory_cache[cache_key] = (time.time() + ttl_seconds, form_data.copy())


def _cache_get(cache_key: str) -> dict[str, Any] | None:
    cached = _memory_cache.get(cache_key)
    if not cached:
        return None
    expires_at, form_data = cached
    if time.time() > expires_at:
        _memory_cache.pop(cache_key, None)
        return None
    return form_data.copy()


def _is_usable_form_data(form_data: Any) -> bool:
    if not isinstance(form_data, dict):
        return False
    if form_data.get("form_submitted"):
        return True
    # Accept payloads that clearly contain answers even if the flag was dropped.
    identity_keys = ("first_name", "fn", "email", "em", "gaining_installation", "gi")
    return any(form_data.get(key) for key in identity_keys)


def _load_from_path(
    path: Path,
    cache_key: str,
    *,
    ttl_seconds: int,
    delete_on_expiry,
) -> dict[str, Any] | None:
    if not path.exists():
        return None

    payload = _read_payload(path)
    if not payload:
        return None

    if _payload_expired(payload, ttl_seconds=ttl_seconds):
        delete_on_expiry()
        return None

    form_data = payload.get("form_data")
    if not _is_usable_form_data(form_data):
        return None

    normalized = dict(form_data)
    if not normalized.get("form_submitted"):
        normalized["form_submitted"] = True

    _cache_put(cache_key, normalized, ttl_seconds=ttl_seconds)
    return normalized.copy()


def _save_form_payload(
    path: Path,
    cache_key: str,
    payload: dict[str, Any],
    form_data: dict[str, Any],
    *,
    ttl_seconds: int,
) -> bool:
    if not _write_payload(path, payload):
        return False
    _cache_put(cache_key, form_data, ttl_seconds=ttl_seconds)
    return True


def save_checkout_form(
    session_id: str,
    form_data: dict[str, Any],
    *,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> bool:
    """Persist submitted form answers keyed by Checkout session_id."""
    if not _is_usable_form_data(form_data):
        logger.warning("Refusing to save checkout form without usable answers.")
        return False

    path = _session_file_path(session_id)
    if path is None:
        return False

    normalized = dict(form_data)
    normalized["form_submitted"] = True

    payload = {
        "session_id": session_id,
        "saved_at": time.time(),
        "ttl_seconds": ttl_seconds,
        "form_data": normalized,
    }
    if not _save_form_payload(path, session_id, payload, normalized, ttl_seconds=ttl_seconds):
        return False

    logger.info("Saved checkout form backup for session %s", session_id)
    return True


def save_checkout_draft(
    draft_id: str,
    form_data: dict[str, Any],
    *,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> bool:
    """Persist form answers before Stripe session creation (pcs_draft metadata key)."""
    if not _is_usable_form_data(form_data):
        logger.warning("Refusing to save checkout draft without usable answers.")
        return False

    path = _draft_file_path(draft_id)
    if path is None:
        return False

    normalized = dict(form_data)
    normalized["form_submitted"] = True

    payload = {
        "draft_id": draft_id,
        "saved_at": time.time(),
        "ttl_seconds": ttl_seconds,
        "form_data": normalized,
    }
    if not _save_form_payload(path, f"draft:{draft_id}", payload, normalized, ttl_seconds=ttl_seconds):
        return False

    logger.info("Saved checkout draft %s", draft_id)
    return True


def load_checkout_form(
    session_id: str,
    *,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> dict[str, Any] | None:
    """Load form answers for a Checkout session_id, or None if missing/expired."""
    cached = _cache_get(session_id)
    if cached and _is_usable_form_data(cached):
        return cached

    path = _session_file_path(session_id)
    if path is None:
        return None

    return _load_from_path(
        path,
        session_id,
        ttl_seconds=ttl_seconds,
        delete_on_expiry=lambda: delete_checkout_form(session_id),
    )


def load_checkout_draft(
    draft_id: str,
    *,
    ttl_seconds: int = DEFAULT_TTL_SECONDS,
) -> dict[str, Any] | None:
    """Load form answers by pre-checkout draft id from Stripe metadata."""
    cache_key = f"draft:{draft_id}"
    cached = _cache_get(cache_key)
    if cached and _is_usable_form_data(cached):
        return cached

    path = _draft_file_path(draft_id)
    if path is None:
        return None

    return _load_from_path(
        path,
        cache_key,
        ttl_seconds=ttl_seconds,
        delete_on_expiry=lambda: delete_checkout_draft(draft_id),
    )


def delete_checkout_form(session_id: str) -> None:
    """Remove a stored checkout form (best-effort)."""
    _memory_cache.pop(session_id, None)
    path = _session_file_path(session_id)
    if path is None:
        return
    try:
        path.unlink(missing_ok=True)
    except OSError as exc:
        logger.warning("Could not delete checkout form file %s: %s", path.name, exc)


def delete_checkout_draft(draft_id: str) -> None:
    """Remove a stored checkout draft (best-effort)."""
    _memory_cache.pop(f"draft:{draft_id}", None)
    path = _draft_file_path(draft_id)
    if path is None:
        return
    try:
        path.unlink(missing_ok=True)
    except OSError as exc:
        logger.warning("Could not delete checkout draft file %s: %s", path.name, exc)


def cleanup_expired(*, ttl_seconds: int = DEFAULT_TTL_SECONDS) -> int:
    """Delete expired JSON backups. Returns number of files removed."""
    removed = 0
    for directory, delete_fn, cache_prefix in (
        (get_store_dir(), delete_checkout_form, ""),
        (get_draft_dir(), delete_checkout_draft, "draft:"),
    ):
        for path in directory.glob("*.json"):
            payload = _read_payload(path)
            if not payload or _payload_expired(payload, ttl_seconds=ttl_seconds):
                try:
                    path.unlink(missing_ok=True)
                    removed += 1
                except OSError:
                    pass
                key = payload.get("session_id") or payload.get("draft_id") if payload else path.stem
                if isinstance(key, str):
                    cache_key = f"{cache_prefix}{key}" if cache_prefix else key
                    _memory_cache.pop(cache_key, None)
    return removed