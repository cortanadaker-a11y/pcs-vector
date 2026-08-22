#!/usr/bin/env python3
"""Audit OCONUS posts vs OHA/COLA data and calculator packages."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.housing_allowances import (  # noqa: E402
    get_housing_package,
    get_oconus_record,
    is_oconus_installation,
)
from services.installation_data import INSTALLATION_DATA  # noqa: E402
from services.utility_costs import get_utility_costs_for_installation  # noqa: E402


def main() -> None:
    oconus_posts = sorted(
        k for k, v in INSTALLATION_DATA.items() if v.get("theater") == "OCONUS"
    )
    data = json.loads((ROOT / "data" / "oconus_allowances_2026.json").read_text())
    loc_keys = sorted((data.get("locations") or {}).keys())

    print(f"OCONUS in INSTALLATION_DATA: {len(oconus_posts)}")
    print(f"Records in oconus_allowances_2026.json: {len(loc_keys)}")
    print()

    missing_record = []
    weak_pkg = []
    for p in oconus_posts:
        rec = get_oconus_record(p)
        pkg = get_housing_package(
            p, "E-5", with_dependents=True, years_of_service=4, num_dependents=1
        )
        util = get_utility_costs_for_installation(
            p, is_oconus=True
        )
        print(p)
        print(
            f"  is_oconus={is_oconus_installation(p)} "
            f"record={bool(rec)} system={pkg.get('housing_system')} "
            f"housing={pkg.get('housing_monthly_usd')} "
            f"cola={pkg.get('cola_monthly_usd')} "
            f"total={pkg.get('total_monthly_usd')} found={pkg.get('found')} "
            f"util_found={util.get('found')}"
        )
        if rec:
            print(
                f"  rec.system={rec.get('housing_system')} "
                f"cola_index={rec.get('cola_index')} "
                f"locality={rec.get('locality')}"
            )
        if not rec:
            missing_record.append(p)
        if not pkg.get("found") or pkg.get("total_monthly_usd") is None:
            weak_pkg.append(p)
        elif pkg.get("housing_system") == "BAH" and is_oconus_installation(p):
            # Foreign OCONUS should usually be OHA or BAH_PLUS_COLA (HI/PR)
            if "Hawaii" not in p and "Puerto Rico" not in p and "HI" not in p and ", PR" not in p:
                weak_pkg.append(p + " (got BAH, expected OHA?)")

    print("\n=== Missing oconus_allowances record ===")
    for p in missing_record:
        print(" ", p)
    print("\n=== Weak / wrong calculator package ===")
    for p in weak_pkg:
        print(" ", p)

    only_in_file = sorted(set(loc_keys) - set(oconus_posts))
    only_in_data = sorted(set(oconus_posts) - set(loc_keys))
    print("\n=== In JSON but not INSTALLATION_DATA OCONUS ===")
    for p in only_in_file:
        print(" ", p)
    print("\n=== In INSTALLATION_DATA OCONUS but not JSON ===")
    for p in only_in_data:
        print(" ", p)


if __name__ == "__main__":
    main()
