"""Price audit row 4 (Mexico-born count) at the chosen level, and carry it to the unauthorized count.

Formula (dataset_integrity_2026_09_23/cps.md, row 3): effect on the main case =
  -(CPS count - chosen level) / CPS count x (G1 share of the union net, ledger waterfall step 14)
  x main case. The per-person figure is unchanged; only the count moves.

Levels for February-April 2025, each an ACS-based figure in the CPS universe (households plus
noninstitutional group quarters):
  central  ACS 2024 as tabulated (11.07M);
  low      ACS 2024 moved to 15 March 2025 at its own 2023-24 pace (smallest correction);
  high     ACS 2024 times the CPS monthly change from its 2024 average to February-April 2025
           (largest correction; part of that CPS fall is first-contact nonresponse, see
           rotation_design.py).
A check row uses the change in MIS 5-8 only (households first reached before 2025), which is
less exposed to the first-contact effect.
Reference rows repeat the audit's two ACS figures and the ASEC 2026 count.

Inputs are parsed from the files that publish them. Writes derived/pricing.csv,
derived/unauthorized_implication.csv and derived/lpr_anchor.csv.
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
D = HERE / "derived"
UNAUTH = FISCAL / "unauthorized_population_size_2026_09_19/derived"


def main() -> None:
    bands = pd.read_csv(FISCAL / "main_case_2026_09_23/derived/main_case_bands.csv")
    main_row = bands[(bands.profile == "cbo_category_lag_non_school_full") & (bands.variant == "adopted")].iloc[0]
    mc_low, mc_high = float(main_row.cost_low_bn), float(main_row.cost_high_bn)
    wf = pd.read_csv(FISCAL / "ledger_absolute_2026_09_17/derived/waterfall.csv")
    step14 = wf[wf.step == 14].set_index("group").cumulative_bn
    g1_share = step14["mexico_born"] / step14["mexican_observed_total"]

    cps = float(pd.read_csv(D / "asec_gate.csv").set_index("asec").reproduced_m[2025])
    ann = pd.read_csv(D / "annual_series.csv").set_index("year")
    acs24, acs23 = ann.acs_mexborn_noninst_m[2024], ann.acs_mexborn_noninst_m[2023]
    mon = pd.read_csv(D / "monthly_series.csv")
    avg24 = mon[mon.year == 2024].mexborn_m.mean()
    feb_apr25 = mon[(mon.year == 2025) & mon.month.isin([2, 3, 4])].mexborn_m.mean()
    asec26 = float(pd.read_csv(D / "asec_gate.csv").set_index("asec").reproduced_m[2026])
    rot = pd.read_csv(D / "rotation_by_month.csv")
    rot = rot[rot.group == "mis5_8"]
    mis58_24 = rot[rot.year == 2024].mex_level_m.mean()
    mis58_25 = rot[(rot.year == 2025) & rot.month.isin([2, 3, 4])].mex_level_m.mean()

    levels = [
        ("low effect: ACS 2024 trended to 15 March 2025", acs24 + (8.5 / 12) * (acs24 - acs23)),
        ("central: ACS 2024, households + noninstitutional GQ", acs24),
        ("high effect: ACS 2024 x CPS monthly change 2024 -> Feb-Apr 2025", acs24 * feb_apr25 / avg24),
        ("check: ACS 2024 x CPS MIS 5-8 change 2024 -> Feb-Apr 2025 (households recruited before 2025)",
         acs24 * mis58_25 / mis58_24),
        ("reference: ACS 2024 households only (audit low)", ann.acs_mexborn_hh_m[2024]),
        ("reference: ACS 2024 incl. institutional GQ (audit high)", ann.acs_mexborn_all_m[2024]),
        ("reference: CPS ASEC 2026", asec26),
    ]
    rows = []
    for name, level in levels:
        excess = (cps - level) / cps
        rows.append(dict(scenario=name, level_m=level, cps_asec2025_m=cps, excess_share=excess,
                         g1_share_step14=g1_share, main_case_low_bn=mc_low, main_case_high_bn=mc_high,
                         effect_at_main_low_bn=-excess * g1_share * mc_low,
                         effect_at_main_high_bn=-excess * g1_share * mc_high,
                         g1_ledger_net_step14_bn=step14["mexico_born"],
                         g1_ledger_net_rescaled_bn=step14["mexico_born"] * level / cps))
    p = pd.DataFrame(rows).round(6)
    p.to_csv(D / "pricing.csv", index=False)

    s = json.loads((UNAUTH / "cps2025_summary.json").read_text())
    un_cps = s["borjas_residual_mexico_born"] / 1e6
    reg = pd.read_csv(UNAUTH / "acs2024_residual_by_region.csv").set_index("region_of_birth")
    noncit_ratio = ann.acs_mexborn_noncit_noninst_m[2024] / ann.cps_mexborn_noncit_m[2025]
    u = pd.DataFrame([
        dict(route="lane figure: Borjas residual on CPS ASEC 2025", mexico_born_unauthorized_m=un_cps),
        dict(route="same rules on ACS 2024 (lane's own run), no coverage", mexico_born_unauthorized_m=reg.loc["Mexico", "residual_unadjusted"] / 1e6),
        dict(route="same rules on ACS 2024 with OHSS coverage (lane's own run)", mexico_born_unauthorized_m=reg.loc["Mexico", "residual_ohss_coverage"] / 1e6),
        dict(route="CPS residual x ACS/CPS noncitizen ratio (excess spread like other CPS noncitizens)", mexico_born_unauthorized_m=un_cps * noncit_ratio),
        dict(route="CPS residual x central level / CPS count", mexico_born_unauthorized_m=un_cps * acs24 / cps),
    ])
    u["change_vs_lane_m"] = u.mexico_born_unauthorized_m - un_cps
    u["change_vs_lane_pct"] = 100 * u.change_vs_lane_m / un_cps
    u = u.round(6)
    u.to_csv(D / "unauthorized_implication.csv", index=False)

    b = pd.read_csv(D / "benchmarks_parsed.csv").set_index("item").value
    lpr24, lpr25 = b["Mexico-born LPRs, January 1 2024 (revised)"] / 1e6, b["Mexico-born LPRs, January 1 2025"] / 1e6
    lp = pd.DataFrame([
        dict(survey="ACS 2024 (noninstitutional)", noncitizens_m=ann.acs_mexborn_noncit_noninst_m[2024], ohss_lpr_m=lpr24),
        dict(survey="CPS ASEC 2025", noncitizens_m=ann.cps_mexborn_noncit_m[2025], ohss_lpr_m=lpr25),
    ])
    lp["non_lpr_noncitizens_m"] = lp.noncitizens_m - lp.ohss_lpr_m
    lp = lp.round(6)
    lp.to_csv(D / "lpr_anchor.csv", index=False)

    with pd.option_context("display.width", 250, "display.max_columns", 20):
        print(p.to_string(index=False))
        print(u.to_string(index=False))
        print(lp.to_string(index=False))


if __name__ == "__main__":
    main()
