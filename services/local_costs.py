"""Per-installation 2026 typical 3BR rent and utility planning ranges.

Used when a post would otherwise inherit a generic High/Medium/Low stub
(the bug that made Aberdeen Proving Ground and Hunter AAF look identical).
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_PATH = Path(__file__).resolve().parent.parent / "data" / "local_costs_2026.json"


@lru_cache(maxsize=1)
def _load() -> dict[str, Any]:
    try:
        raw = json.loads(_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return raw.get("installations") or {}


def get_rent_3br(installation: str) -> tuple[int, int] | None:
    row = _load().get(installation) or {}
    band = row.get("rent_3br")
    if not (isinstance(band, list) and len(band) == 2):
        return None
    try:
        low, high = int(band[0]), int(band[1])
    except (TypeError, ValueError):
        return None
    if low <= 0 or high < low:
        return None
    return low, high


def get_utility_override(installation: str) -> dict[str, Any] | None:
    row = _load().get(installation) or {}
    util = row.get("utility")
    if not isinstance(util, dict):
        return None
    areas = util.get("areas")
    if not areas:
        return None
    return util


__all__ = ["get_rent_3br", "get_utility_override"]
