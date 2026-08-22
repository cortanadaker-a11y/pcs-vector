#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from services.bah_rates import list_bah_installations
from services.housing_allowances import get_housing_package, get_oconus_record
from services.installation_data import INSTALLATION_DATA
from services.utility_costs import _UTILITY_BY_INSTALL, get_utility_costs_for_installation


def main() -> None:
    bah_list = set(list_bah_installations())
    oconus = {k for k, v in INSTALLATION_DATA.items() if v.get("theater") == "OCONUS"}
    print("OCONUS not in bah dropdown:", sorted(oconus - bah_list))
    print("AK / other special:")
    for k, v in sorted(INSTALLATION_DATA.items()):
        if v.get("state") in ("AK", "HI", "PR", "Japan", "ROK", "Germany", "Italy") or "USAG" in k or "Camp " in k:
            rec = get_oconus_record(k)
            pkg = get_housing_package(k, "E-5", with_dependents=True, years_of_service=4, num_dependents=1)
            print(
                f"  {k} theater={v.get('theater')} "
                f"sys={pkg.get('housing_system')} cola={pkg.get('cola_monthly_usd')} "
                f"rec={bool(rec)} util={k in _UTILITY_BY_INSTALL}"
            )

    print("\nUtility table keys count:", len(_UTILITY_BY_INSTALL))
    missing_util = []
    for p in sorted(INSTALLATION_DATA.keys()):
        u = get_utility_costs_for_installation(p, is_oconus=INSTALLATION_DATA[p].get("theater") == "OCONUS")
        if not u.get("found"):
            missing_util.append(p)
    print("Installations using regional util fallback:", len(missing_util))
    for p in missing_util:
        if INSTALLATION_DATA[p].get("theater") == "OCONUS" or p.startswith("USAG") or "Camp " in p:
            print("  OCONUS/overseas fallback:", p)


if __name__ == "__main__":
    main()
