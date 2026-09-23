#!/usr/bin/env python3
"""Survey counts of imputed-unauthorized Medi-Cal enrollees against DHCS's published counts.

Inputs (all produced in this lane): derived/cps_coverage_by_age.csv, cps_ca_all_medicaid.csv,
acs_ca_counts_by_age.csv, acs_ca_all_medicaid.csv, dhcs_uis_monthly.csv, and the DHCS all-eligibles
table _cache/t1_eligibility_by_age_group_sex_201001_202609.csv.

Two ratios per survey measure:
  * capture of DHCS's status-blind expansion enrollment (UIS plus some lawfully present) by the
    survey's `no_medicaid_rule` unauthorized who report Medicaid; under the paper rules that count is
    zero by construction, because rule (c) calls every Medicaid reporter legal;
  * the same survey's capture of ALL California Medi-Cal certified eligibles, the reporting-rate
    yardstick. Their product with DHCS's expansion count is the number of expansion enrollees the
    survey would show if they reported coverage as completely as other enrollees [INFERENCE].
Survey reference periods: CPS MCAID any time in 2024 and NOW_MCAID February-April 2025; ACS HINS4 at
interview through 2024. DHCS windows are matched accordingly (monthly averages).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 PYTHONDONTWRITEBYTECODE=1 uv run --no-project python3 \
        infra/immigration-fiscal/california_medical_status_2026_09_23/benchmark.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
DER = HERE / "derived"
T1 = HERE / "_cache/t1_eligibility_by_age_group_sex_201001_202609.csv"
BANDS = ["0-18", "19-25", "26-49", "50+", "all"]
DHCS_GROUPS = {"Age 00-18": "0-18", "Age 19-44": "19-44", "Age 45-64": "45-64", "Age 65+": "65+"}


def dhcs_all_eligibles() -> pd.DataFrame:
    """Monthly certified eligibles by DHCS age group, summed over counties (suppressed cells omitted)."""
    t = pd.read_csv(T1, encoding="utf-8-sig", low_memory=False)
    t["v"] = pd.to_numeric(t["Total Eligibles"].astype(str).str.replace(",", ""), errors="coerce")
    sw = t[t.County.eq("STATEWIDE")].groupby("Month of Eligibility").v.sum().rename("all")
    cty = t[~t.County.isin(["STATEWIDE"]) & t["Age Group"].isin(DHCS_GROUPS)]
    by = cty.groupby(["Month of Eligibility", "Age Group"]).v.sum().unstack().rename(columns=DHCS_GROUPS)
    return by.join(sw)


def window(df: pd.DataFrame, a: str, b: str) -> pd.Series:
    return df.loc[(df.index >= a) & (df.index <= b)].mean()


def main():
    uis = pd.read_csv(DER / "dhcs_uis_monthly.csv").set_index("month")
    uis = uis.rename(columns={"all_ages": "all"})
    alle = dhcs_all_eligibles()
    windows = {"CY2024_average": ("2024-01", "2024-12"), "Dec2024": ("2024-12", "2024-12"),
               "Feb_Apr2025_average": ("2025-02", "2025-04")}
    cps = pd.read_csv(DER / "cps_coverage_by_age.csv")
    cps = cps[(cps.region == "California") & (cps.group == "all_foreign_born")].set_index("age")
    acs = pd.read_csv(DER / "acs_ca_counts_by_age.csv")
    acs = acs[(acs.rules == "no_medicaid_rule") & (acs.population == "all_persons")
              & (acs.group == "all_foreign_born")].set_index("age")
    cps_all = pd.read_csv(DER / "cps_ca_all_medicaid.csv").set_index("age")
    acs_all = pd.read_csv(DER / "acs_ca_all_medicaid.csv")
    acs_all = acs_all[acs_all.population == "all_persons"].set_index("age")

    measures = [  # label, survey count by band (millions, se), all-resident count by DHCS group, DHCS window
        ("CPS MCAID, any time in 2024", lambda b: (cps.loc[b, "MCAID_millions"], cps.loc[b, "MCAID_se"]),
         lambda g: cps_all.loc[g, "MCAID_millions"], "CY2024_average"),
        ("CPS MCAID, any time in 2024, vs Dec 2024", lambda b: (cps.loc[b, "MCAID_millions"], cps.loc[b, "MCAID_se"]),
         lambda g: cps_all.loc[g, "MCAID_millions"], "Dec2024"),
        ("CPS NOW_MCAID, Feb-Apr 2025", lambda b: (cps.loc[b, "NOW_MCAID_millions"], cps.loc[b, "NOW_MCAID_se"]),
         lambda g: cps_all.loc[g, "NOW_MCAID_millions"], "Feb_Apr2025_average"),
        ("ACS HINS4, at interview in 2024", lambda b: (acs.loc[b, "medicaid_now"] / 1e6, acs.loc[b, "medicaid_now_se"] / 1e6),
         lambda g: acs_all.loc[g, "medicaid_now_all_residents"] / 1e6, "CY2024_average"),
    ]
    rows = []
    for label, get, get_all, win in measures:
        a, b = windows[win]
        u = window(uis, a, b)
        e = window(alle, a, b)
        rate_all = get_all("all") / (e["all"] / 1e6)
        for band in BANDS:
            n, se = get(band)
            dh = u[band] / 1e6
            rows.append({"measure": label, "dhcs_window": win, "age": band,
                         "survey_no_medicaid_rule_with_medicaid_millions": round(n, 4), "se": round(se, 4),
                         "survey_paper_rules_with_medicaid_millions": 0.0,
                         "dhcs_expansion_enrollment_millions": round(dh, 4),
                         "capture_no_medicaid_rule": round(n / dh, 3), "capture_se": round(se / dh, 3),
                         "survey_capture_all_medi_cal": round(rate_all, 3),
                         "expected_visible_expansion_enrollees_millions": round(dh * rate_all, 4)})
    bench = pd.DataFrame(rows)
    bench.to_csv(DER / "benchmark_survey_vs_dhcs.csv", index=False)

    rows = []
    for label, _, get_all, win in measures:
        e = window(alle, *windows[win])
        for g in ["0-18", "19-44", "45-64", "65+", "all"]:
            rows.append({"measure": label, "dhcs_window": win, "age": g,
                         "survey_all_residents_with_medicaid_millions": round(get_all(g), 4),
                         "dhcs_certified_eligibles_millions": round(e[g] / 1e6, 4),
                         "survey_capture": round(get_all(g) / (e[g] / 1e6), 3)})
    cal = pd.DataFrame(rows)
    cal.to_csv(DER / "benchmark_all_medi_cal_reporting.csv", index=False)

    # How many Californians the Medicaid clause misclassifies: three readings of one quantity.
    #   lower      -- California's Medicaid reports in excess of unlisted states' age-specific rates
    #                 (cps_ca_excess_over_unlisted.csv, replicate SE);
    #   calibrated -- DHCS's 2024 expansion enrollment times the survey's reporting rate for all
    #                 Medi-Cal enrollees (SE from the survey's all-enrollee count); Mexico-born scaled
    #                 by their share of the moved [INFERENCE];
    #   upper      -- everyone the clause moves into the legal column.
    ex = pd.read_csv(DER / "cps_ca_excess_over_unlisted.csv").set_index(["group", "age"])
    dec = pd.read_csv(DER / "cps_moved_decomposition.csv").set_index(["region", "group"])
    acs_mv = pd.read_csv(DER / "acs_ca_counts_by_age.csv")
    acs_mv = acs_mv[(acs_mv.rules == "no_medicaid_rule") & (acs_mv.population == "all_persons")
                    & (acs_mv.age == "all")].set_index("group")
    dh = window(uis, *windows["CY2024_average"])["all"] / 1e6
    e24 = window(alle, *windows["CY2024_average"])["all"] / 1e6
    rows = []
    for survey, all_n, all_se, mv_fb, mv_fb_se, mv_mx, mv_mx_se in (
            ("CPS", cps_all.loc["all", "MCAID_millions"], cps_all.loc["all", "MCAID_se"],
             dec.loc[("California", "all_foreign_born"), "moved_millions"], dec.loc[("California", "all_foreign_born"), "se"],
             dec.loc[("California", "mexico_born"), "moved_millions"], dec.loc[("California", "mexico_born"), "se"]),
            ("ACS", acs_all.loc["all", "medicaid_now_all_residents"] / 1e6, acs_all.loc["all", "se"] / 1e6,
             acs_mv.loc["all_foreign_born", "moved_by_medicaid_clause"] / 1e6, acs_mv.loc["all_foreign_born", "moved_se"] / 1e6,
             acs_mv.loc["mexico_born", "moved_by_medicaid_clause"] / 1e6, acs_mv.loc["mexico_born", "moved_se"] / 1e6)):
        cal_fb = dh * all_n / e24
        cal_se = dh * all_se / e24
        share_mx = mv_mx / mv_fb
        if survey == "CPS":
            rows.append({"survey": survey, "group": "all_foreign_born", "reading": "lower_excess_over_unlisted_states",
                         "millions": ex.loc[("all_foreign_born", "0-64"), "excess_millions"],
                         "se": ex.loc[("all_foreign_born", "0-64"), "se"]})
            rows.append({"survey": survey, "group": "mexico_born", "reading": "lower_excess_over_unlisted_states",
                         "millions": ex.loc[("mexico_born", "0-64"), "excess_millions"],
                         "se": ex.loc[("mexico_born", "0-64"), "se"]})
        rows += [{"survey": survey, "group": "all_foreign_born", "reading": "calibrated_dhcs_times_reporting_rate",
                  "millions": round(cal_fb, 4), "se": round(cal_se, 4)},
                 {"survey": survey, "group": "mexico_born", "reading": "calibrated_dhcs_times_reporting_rate",
                  "millions": round(cal_fb * share_mx, 4), "se": round(cal_se * share_mx, 4)},
                 {"survey": survey, "group": "all_foreign_born", "reading": "upper_all_moved",
                  "millions": round(mv_fb, 4), "se": round(mv_fb_se, 4)},
                 {"survey": survey, "group": "mexico_born", "reading": "upper_all_moved",
                  "millions": round(mv_mx, 4), "se": round(mv_mx_se, 4)}]
    band = pd.DataFrame(rows)
    band.to_csv(DER / "ca_misclassification_band.csv", index=False)
    print(band.to_string(index=False))
    pd.set_option("display.width", 250)
    print(bench.to_string(index=False))
    print(cal.to_string(index=False))


if __name__ == "__main__":
    main()
