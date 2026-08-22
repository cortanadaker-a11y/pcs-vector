#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.housing_allowances import _load_oconus, get_housing_package, get_oconus_record
from services.installation_data import INSTALLATION_DATA
from services.utility_costs import get_utility_costs_for_installation

_load_oconus.cache_clear()


def main() -> None:
    ak = [
        "Joint Base Elmendorf-Richardson, AK",
        "Fort Wainwright, AK",
        "Fort Greely, AK",
    ]
    for p in ak:
        assert INSTALLATION_DATA[p]["theater"] == "OCONUS", p
        rec = get_oconus_record(p)
        assert rec and rec["housing_system"] == "BAH_PLUS_COLA", p
        pkg = get_housing_package(
            p, "E-5", with_dependents=True, years_of_service=4, num_dependents=1
        )
        assert pkg["housing_system"] == "BAH_PLUS_COLA", (p, pkg)
        assert pkg.get("cola_monthly_usd", 0) > 0, (p, pkg)
        u = get_utility_costs_for_installation(p, is_oconus=True)
        assert u["found"], p
        a = u["areas"][0]
        assert "water_trash_usd_mo" in a and "internet_usd_mo" in a
        print(
            p,
            "BAH",
            pkg["housing_monthly_usd"],
            "COLA",
            pkg["cola_monthly_usd"],
            "total",
            pkg["total_monthly_usd"],
        )

    for p in [
        "Camp Casey, South Korea",
        "Camp Zama, Japan",
        "USAG Italy, Italy",
        "Fort Shafter, HI",
        "Fort Buchanan, PR",
    ]:
        u = get_utility_costs_for_installation(p, is_oconus=True)
        assert u["found"], p
        print("util ok", p)

    casey = get_housing_package(
        "Camp Casey, South Korea",
        "E-5",
        with_dependents=True,
        years_of_service=4,
        num_dependents=1,
    )
    print(
        "Casey COLA",
        casey.get("cola_monthly_usd"),
        "index",
        casey.get("cola_index"),
        "OHA",
        casey.get("housing_monthly_usd"),
    )
    print("ok")


if __name__ == "__main__":
    main()
