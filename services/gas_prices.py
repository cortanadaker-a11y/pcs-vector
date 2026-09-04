"""Retail regular gasoline near a post, for the calculator comparison row.

CONUS / AK / HI / PR: EIA weekly regular gasoline (USD/gal, including taxes).
The post's zip (or state) maps to the tightest published EIA area — a state
series when EIA publishes one, otherwise the PADD region.

OCONUS (Germany, Italy, Korea, Japan): planning estimates in USD/gal.
"""

from __future__ import annotations

import json
import logging
import re
import time
from pathlib import Path
from typing import Any

logger = logging.getLogger("pcs_vector.gas")

_EIA_WEEKLY_URL = (
    "https://www.eia.gov/dnav/pet/pet_pri_gnd_a_epmr_pte_dpgal_w.htm"
)
_FALLBACK_PATH = Path(__file__).resolve().parent.parent / "data" / "gas_prices_fallback.json"
_CACHE_TTL_SEC = 6 * 3600
_FETCH_TIMEOUT_SEC = 12

# EIA publishes weekly state series only for these.
_EIA_STATE_AREA = {
    "CA": "California",
    "CO": "Colorado",
    "FL": "Florida",
    "MA": "Massachusetts",
    "MN": "Minnesota",
    "NY": "New York",
    "OH": "Ohio",
    "TX": "Texas",
    "WA": "Washington",
}

# Official PADD membership → EIA row name when no state series exists.
_PADD_AREA = {
    "CT": "New England (PADD 1A)",
    "ME": "New England (PADD 1A)",
    "MA": "Massachusetts",
    "NH": "New England (PADD 1A)",
    "RI": "New England (PADD 1A)",
    "VT": "New England (PADD 1A)",
    "DE": "Central Atlantic (PADD 1B)",
    "DC": "Central Atlantic (PADD 1B)",
    "MD": "Central Atlantic (PADD 1B)",
    "NJ": "Central Atlantic (PADD 1B)",
    "NY": "New York",
    "PA": "Central Atlantic (PADD 1B)",
    "FL": "Florida",
    "GA": "Lower Atlantic (PADD 1C)",
    "NC": "Lower Atlantic (PADD 1C)",
    "SC": "Lower Atlantic (PADD 1C)",
    "VA": "Lower Atlantic (PADD 1C)",
    "WV": "Lower Atlantic (PADD 1C)",
    "IL": "Midwest (PADD 2)",
    "IN": "Midwest (PADD 2)",
    "IA": "Midwest (PADD 2)",
    "KS": "Midwest (PADD 2)",
    "KY": "Midwest (PADD 2)",
    "MI": "Midwest (PADD 2)",
    "MN": "Minnesota",
    "MO": "Midwest (PADD 2)",
    "NE": "Midwest (PADD 2)",
    "ND": "Midwest (PADD 2)",
    "OH": "Ohio",
    "OK": "Midwest (PADD 2)",
    "SD": "Midwest (PADD 2)",
    "TN": "Midwest (PADD 2)",
    "WI": "Midwest (PADD 2)",
    "AL": "Gulf Coast (PADD 3)",
    "AR": "Gulf Coast (PADD 3)",
    "LA": "Gulf Coast (PADD 3)",
    "MS": "Gulf Coast (PADD 3)",
    "NM": "Gulf Coast (PADD 3)",
    "TX": "Texas",
    "CO": "Colorado",
    "ID": "Rocky Mountain (PADD 4)",
    "MT": "Rocky Mountain (PADD 4)",
    "UT": "Rocky Mountain (PADD 4)",
    "WY": "Rocky Mountain (PADD 4)",
    "AZ": "West Coast (PADD 5)",
    "CA": "California",
    "HI": "West Coast (PADD 5)",
    "NV": "West Coast (PADD 5)",
    "OR": "West Coast (PADD 5)",
    "WA": "Washington",
    # AK is PADD 5 but CA-inflated West Coast is a bad proxy.
    "AK": "West Coast less California",
    "PR": "U.S.",
}

# Housing-market city rows when EIA publishes one that actually matches the post.
_CITY_AREA = {
    "Joint Base Lewis-McChord, WA": "Seattle",
    "Fort Carson, CO": "Denver",
    "Fort Hamilton, NY": "New York City",
}

_USPS = set(_PADD_AREA)
_OCONUS_STATES = {"Germany", "Italy", "Japan", "ROK", "South Korea"}

_STUB = re.compile(r'class="DataStub1">(?:<B>)*([^<]+)', re.I)
_CURRENT = re.compile(r'class="Current2">([0-9]\.[0-9]{2,3})')
_WEEK_DATE = re.compile(r"\b(0?[1-9]|1[0-2])/(0?[1-9]|[12][0-9]|3[01])/(\d{2})\b")

_cache: dict[str, Any] = {"at": 0.0, "table": None}


def _canonical(installation: str) -> str | None:
    from services.installation_data import _canonical_installation_name

    return _canonical_installation_name(installation)


def _zip_and_state(installation: str) -> tuple[str, str, str]:
    """Return (canonical_name, zip, USPS-or-country state)."""
    from services.installation_data import INSTALLATIONS, get_installation_data
    from services.utility_costs import get_utility_costs_for_installation

    canonical = _canonical(installation) or (installation or "").strip()
    zip_code = ""
    state = ""
    prof = INSTALLATIONS.get(canonical)
    if prof is not None:
        zip_code = str(prof.zip_code or "").strip()
        state = str(prof.state or "").split("/")[0].strip()
    meta = get_installation_data(canonical)
    if meta and not state:
        state = str(meta.get("state") or "").split("/")[0].strip()
    if not zip_code:
        util = get_utility_costs_for_installation(canonical)
        for area in util.get("areas") or []:
            zips = area.get("zips") or []
            if zips:
                zip_code = str(zips[0]).strip()
                break
    return canonical, zip_code, state


def _load_fallback() -> dict[str, Any]:
    try:
        raw = json.loads(_FALLBACK_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        logger.warning("gas price fallback JSON missing or invalid")
        return {"as_of": "", "prices": {}, "oconus_estimates": {}}
    return {
        "as_of": str(raw.get("as_of") or ""),
        "prices": {str(k): float(v) for k, v in (raw.get("prices") or {}).items()},
        "oconus_estimates": {
            str(k): float(v) for k, v in (raw.get("oconus_estimates") or {}).items()
        },
        "source": "fallback",
    }


def _parse_eia_html(html: str) -> dict[str, Any]:
    prices: dict[str, float] = {}
    for stub in _STUB.finditer(html):
        name = stub.group(1).replace("\xa0", " ").strip().rstrip("<").strip()
        name = re.sub(r"<.*", "", name).strip()
        if not name:
            continue
        window = html[stub.end() : stub.end() + 1800]
        cur = _CURRENT.search(window)
        if not cur:
            continue
        prices[name] = float(cur.group(1))

    as_of = ""
    latest = None
    for m in _WEEK_DATE.finditer(html):
        month, day, yy = int(m.group(1)), int(m.group(2)), int(m.group(3))
        year = 2000 + yy if yy < 80 else 1900 + yy
        stamp = (year, month, day)
        if latest is None or stamp > latest:
            latest = stamp
            as_of = f"{year:04d}-{month:02d}-{day:02d}"
    return {"as_of": as_of, "prices": prices, "source": "eia_weekly"}


def _fetch_eia_table() -> dict[str, Any] | None:
    try:
        import requests
    except ImportError:
        return None
    try:
        resp = requests.get(
            _EIA_WEEKLY_URL,
            headers={"User-Agent": "PCS-Vector/1.0 (https://github.com/cortanadaker-a11y/pcs-vector)"},
            timeout=_FETCH_TIMEOUT_SEC,
        )
        if resp.status_code >= 400 or not resp.text:
            return None
        parsed = _parse_eia_html(resp.text)
        if len(parsed.get("prices") or {}) < 8:
            return None
        return parsed
    except Exception:
        logger.exception("EIA weekly gasoline fetch failed")
        return None


def _eia_table() -> dict[str, Any]:
    now = time.time()
    cached = _cache.get("table")
    if cached and (now - float(_cache.get("at") or 0)) < _CACHE_TTL_SEC:
        return cached
    live = _fetch_eia_table()
    table = live if live and live.get("prices") else _load_fallback()
    # Keep OCONUS estimates even on a live EIA fetch.
    fallback = _load_fallback()
    if "oconus_estimates" not in table:
        table["oconus_estimates"] = fallback.get("oconus_estimates") or {}
    _cache["table"] = table
    _cache["at"] = now
    return table


def _area_for(canonical: str, state: str) -> str | None:
    if canonical in _CITY_AREA:
        return _CITY_AREA[canonical]
    usps = (state or "").upper()
    if usps in _EIA_STATE_AREA:
        return _EIA_STATE_AREA[usps]
    if usps in _PADD_AREA:
        return _PADD_AREA[usps]
    return None


def _format_usd_gal(price: float) -> str:
    return f"${price:.2f}/gal"


def get_gas_price_for_installation(installation: str | None) -> dict[str, Any]:
    """Latest regular-gas figure for a post. Always returns a dict."""
    empty = {
        "found": False,
        "usd_gal": None,
        "label": "—",
        "area": "",
        "zip": "",
        "state": "",
        "source": "",
        "as_of": "",
    }
    if not (installation or "").strip():
        return empty

    canonical, zip_code, state = _zip_and_state(installation)
    table = _eia_table()
    prices: dict[str, float] = table.get("prices") or {}
    oconus: dict[str, float] = table.get("oconus_estimates") or {}

    usps = (state or "").upper()
    if usps in _OCONUS_STATES or state in _OCONUS_STATES:
        key = state if state in oconus else usps
        if key in oconus:
            price = float(oconus[key])
            return {
                "found": True,
                "usd_gal": price,
                "label": _format_usd_gal(price),
                "area": state,
                "zip": zip_code,
                "state": state,
                "source": "oconus_estimate",
                "as_of": "planning estimate",
            }
        return {**empty, "zip": zip_code, "state": state}

    area = _area_for(canonical, usps or state)
    if area and area in prices:
        price = float(prices[area])
        return {
            "found": True,
            "usd_gal": price,
            "label": _format_usd_gal(price),
            "area": area,
            "zip": zip_code,
            "state": usps or state,
            "source": table.get("source") or "eia_weekly",
            "as_of": table.get("as_of") or "",
        }
    if "U.S." in prices:
        price = float(prices["U.S."])
        return {
            "found": True,
            "usd_gal": price,
            "label": _format_usd_gal(price),
            "area": "U.S.",
            "zip": zip_code,
            "state": usps or state,
            "source": table.get("source") or "eia_weekly",
            "as_of": table.get("as_of") or "",
        }
    return {**empty, "zip": zip_code, "state": usps or state}


__all__ = ["get_gas_price_for_installation"]
