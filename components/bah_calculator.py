"""Homepage housing allowance calculator (BAH CONUS + OHA/COLA OCONUS)."""

from __future__ import annotations

import streamlit as st

from components.form_options import PAY_GRADE_TO_RANK, RANK_PAY_GRADES
from components.html_utils import safe_html
from services.bah_rates import list_bah_installations
from services.housing_allowances import compare_housing_packages, get_housing_package
from services.installation_data import SUPPORTED_INSTALLATIONS

YOS_OPTIONS = [
    "Under 2 years",
    "2–3 years",
    "4–5 years",
    "6–7 years",
    "8–9 years",
    "10–11 years",
    "12–13 years",
    "14–15 years",
    "16–17 years",
    "18–19 years",
    "20+ years",
]

_NONE_CURRENT = "— Skip comparison (gaining post only) —"
_WITH = "With dependents"
_WITHOUT = "Without dependents"


def _money(n: int | None) -> str:
    if n is None:
        return "—"
    sign = "-" if n < 0 else ""
    return f"{sign}${abs(n):,}"


def _resolve_dependents(deps_value: str) -> bool:
    return deps_value.strip() == _WITH


def render_bah_calculator() -> None:
    """Interactive BAH / OHA + COLA calculator for the homepage."""
    installations = list_bah_installations()
    if list(installations) != list(SUPPORTED_INSTALLATIONS):
        installations = list(SUPPORTED_INSTALLATIONS)
    if not installations:
        return

    grades = [g for g in RANK_PAY_GRADES if g != "Other"]

    st.markdown(
        f"""
        <div class="pcs-bah-wrap">
            <div class="pcs-bah-header">
                <div class="pcs-bah-badge">2026 · {len(installations)} posts · same list as the plan form</div>
                <h3>Housing Allowance Calculator</h3>
                <p class="pcs-bah-sub">
                    CONUS: BAH. Foreign OCONUS: OHA (rent max + utilities) + COLA.
                    Hawaii / Puerto Rico: BAH + COLA. Compare posts to see the monthly change.
                </p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.container(border=True):
        st.markdown('<p class="pcs-bah-section-label">Your profile</p>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns([1.1, 1.1, 1.2])
        with c1:
            pay_grade = st.selectbox(
                "Pay grade",
                options=grades,
                index=grades.index("E-5") if "E-5" in grades else 0,
                format_func=lambda g: f"{g} — {PAY_GRADE_TO_RANK.get(g, g)}",
                key="bah_calc_grade",
            )
        with c2:
            yos = st.selectbox(
                "Years of service",
                options=YOS_OPTIONS,
                index=2,
                key="bah_calc_yos",
                help="COLA can vary with pay and YOS. BAH/OHA ceilings use grade + dependents + location.",
            )
        with c3:
            deps = st.radio(
                "Dependents",
                options=[_WITH, _WITHOUT],
                horizontal=True,
                key="bah_calc_deps",
            )

        st.markdown('<p class="pcs-bah-section-label">Duty stations</p>', unsafe_allow_html=True)
        d1, d2 = st.columns(2)
        with d1:
            gaining = st.selectbox(
                "New post (gaining)",
                options=installations,
                index=installations.index("Fort Bragg, NC")
                if "Fort Bragg, NC" in installations
                else 0,
                key="bah_calc_gaining",
            )
        with d2:
            current_raw = st.selectbox(
                "Current post (optional compare)",
                options=[_NONE_CURRENT] + installations,
                key="bah_calc_current",
            )
            current = None if current_raw == _NONE_CURRENT else current_raw

        with_dependents = _resolve_dependents(deps)
        result = compare_housing_packages(
            pay_grade=pay_grade,
            with_dependents=with_dependents,
            gaining_installation=gaining,
            current_installation=current,
        )
        pkg = result["gaining"]

        if not pkg.get("found") or pkg.get("total_monthly_usd") is None:
            st.warning(
                f"No 2026 housing package on file for {pay_grade} at {gaining}. "
                "Try another post or verify with finance / DTMO."
            )
            return

        rank_label = PAY_GRADE_TO_RANK.get(pay_grade, pay_grade)
        dep_label = "with dependents" if with_dependents else "without dependents"
        dep_chip = "WITH DEPS" if with_dependents else "NO DEPS"
        system = pkg.get("housing_system") or "BAH"
        housing = int(pkg["housing_monthly_usd"] or 0)
        cola = int(pkg.get("cola_monthly_usd") or 0)
        total = int(pkg["total_monthly_usd"])

        if system == "OHA":
            label = f"OHA planning max · {gaining}"
            system_chip = "OHA + COLA"
            annual_note = f"{_money(total * 12)} / year combined (housing package + COLA)"
        elif system == "BAH_PLUS_COLA":
            label = f"BAH + COLA · {gaining}"
            system_chip = "BAH + COLA"
            annual_note = f"{_money(total * 12)} / year combined (BAH + COLA)"
        else:
            label = f"Monthly BAH · {gaining}"
            system_chip = "BAH"
            annual_note = f"{_money(total * 12)} / year housing allowance"

        st.markdown(
            f"""
            <div class="pcs-bah-result">
                <div class="pcs-bah-result-top">
                    <div class="pcs-bah-result-label">{safe_html(label)}</div>
                    <span class="pcs-bah-chip pcs-bah-chip-{'with' if with_dependents else 'without'}">{safe_html(dep_chip)} · {safe_html(system_chip)}</span>
                </div>
                <div class="pcs-bah-result-amount">{_money(total)}<span>/mo total</span></div>
                <div class="pcs-bah-result-meta">
                    {safe_html(pay_grade)} ({safe_html(rank_label)}) · {safe_html(dep_label)} · {safe_html(yos)}
                </div>
                <div class="pcs-bah-result-annual">{safe_html(annual_note)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Breakdown cards
        if system == "OHA":
            rent = pkg.get("oha_rent_max_usd")
            util = pkg.get("oha_utility_usd")
            st.markdown(
                f"""
                <div class="pcs-bah-pair">
                    <div class="pcs-bah-pair-card pcs-bah-pair-active">
                        <div class="pcs-bah-pair-k">OHA rent ceiling</div>
                        <div class="pcs-bah-pair-v">{_money(int(rent) if rent else None)}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card pcs-bah-pair-active">
                        <div class="pcs-bah-pair-k">OHA utilities</div>
                        <div class="pcs-bah-pair-v">{_money(int(util) if util else None)}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card pcs-bah-pair-diff">
                        <div class="pcs-bah-pair-k">COLA (index {safe_html(str(pkg.get('cola_index') or '—'))})</div>
                        <div class="pcs-bah-pair-v">{_money(cola)}/mo</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(pkg.get("disclaimer") or "")
            if pkg.get("currency_note"):
                st.caption(pkg["currency_note"])
        elif system == "BAH_PLUS_COLA":
            st.markdown(
                f"""
                <div class="pcs-bah-pair">
                    <div class="pcs-bah-pair-card pcs-bah-pair-active">
                        <div class="pcs-bah-pair-k">BAH</div>
                        <div class="pcs-bah-pair-v">{_money(housing)}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card pcs-bah-pair-active">
                        <div class="pcs-bah-pair-k">COLA (index {safe_html(str(pkg.get('cola_index') or '—'))})</div>
                        <div class="pcs-bah-pair-v">{_money(cola)}/mo</div>
                    </div>
                    <div class="pcs-bah-pair-card pcs-bah-pair-diff">
                        <div class="pcs-bah-pair-k">Combined</div>
                        <div class="pcs-bah-pair-v">{_money(total)}/mo</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.caption(pkg.get("disclaimer") or "")
        else:
            alt_with = get_housing_package(gaining, pay_grade, with_dependents=True)
            alt_without = get_housing_package(gaining, pay_grade, with_dependents=False)
            aw = alt_with.get("housing_monthly_usd")
            awo = alt_without.get("housing_monthly_usd")
            if aw is not None and awo is not None:
                active_with = "pcs-bah-pair-active" if with_dependents else ""
                active_without = "pcs-bah-pair-active" if not with_dependents else ""
                st.markdown(
                    f"""
                    <div class="pcs-bah-pair">
                        <div class="pcs-bah-pair-card {active_with}">
                            <div class="pcs-bah-pair-k">With dependents</div>
                            <div class="pcs-bah-pair-v">{_money(int(aw))}/mo</div>
                        </div>
                        <div class="pcs-bah-pair-card {active_without}">
                            <div class="pcs-bah-pair-k">Without dependents</div>
                            <div class="pcs-bah-pair-v">{_money(int(awo))}/mo</div>
                        </div>
                        <div class="pcs-bah-pair-card pcs-bah-pair-diff">
                            <div class="pcs-bah-pair-k">Dependent difference</div>
                            <div class="pcs-bah-pair-v">{_money(int(aw) - int(awo))}/mo</div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        # Comparison to current post
        cur = result.get("current")
        delta = result.get("monthly_delta_usd")
        if current and cur and cur.get("found") and cur.get("total_monthly_usd") is not None and delta is not None:
            curr_tot = int(cur["total_monthly_usd"])
            annual = int(result.get("annual_delta_usd") or 0)
            cur_sys = cur.get("housing_system") or "BAH"
            if delta > 0:
                tone, headline = "up", f"+{_money(delta)}/mo more at your new post"
            elif delta < 0:
                tone, headline = "down", f"{_money(delta)}/mo less at your new post"
            else:
                tone, headline = "flat", "Same total package at both posts"

            cur_bits = []
            if cur_sys == "OHA":
                cur_bits.append(f"OHA ≈ {_money(cur.get('housing_monthly_usd'))}")
            else:
                cur_bits.append(f"BAH {_money(cur.get('housing_monthly_usd'))}")
            if int(cur.get("cola_monthly_usd") or 0):
                cur_bits.append(f"COLA {_money(int(cur['cola_monthly_usd']))}")
            new_bits = []
            if system == "OHA":
                new_bits.append(f"OHA ≈ {_money(housing)}")
            else:
                new_bits.append(f"BAH {_money(housing)}")
            if cola:
                new_bits.append(f"COLA {_money(cola)}")

            detail = (
                f"{current} ({', '.join(cur_bits)} → {_money(curr_tot)} total) → "
                f"{gaining} ({', '.join(new_bits)} → {_money(total)} total). "
                f"About {_money(annual)} per year."
            )
            st.markdown(
                f"""
                <div class="pcs-bah-delta pcs-bah-delta-{tone}">
                    <div class="pcs-bah-delta-title">{safe_html(headline)}</div>
                    <div class="pcs-bah-delta-detail">{safe_html(detail)}</div>
                    <div class="pcs-bah-delta-grid">
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">Current total</div>
                            <div class="pcs-bah-delta-v">{_money(curr_tot)}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(current)}</div>
                        </div>
                        <div class="pcs-bah-delta-arrow">→</div>
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">New total</div>
                            <div class="pcs-bah-delta-v">{_money(total)}/mo</div>
                            <div class="pcs-bah-delta-s">{safe_html(gaining)}</div>
                        </div>
                        <div class="pcs-bah-delta-cell">
                            <div class="pcs-bah-delta-k">Change</div>
                            <div class="pcs-bah-delta-v">{_money(int(delta))}</div>
                            <div class="pcs-bah-delta-s">{_money(annual)} / year</div>
                        </div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        st.caption(
            "CONUS = BAH. Foreign OCONUS = OHA (actual rent up to max + utilities) + COLA. "
            "HI/PR = BAH + COLA. Figures are 2026 planning packages — OHA/COLA change with "
            "exchange rates and DTMO updates. Always verify on your LES and DTMO calculators."
        )
