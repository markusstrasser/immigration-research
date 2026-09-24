"""Disconfirmation checks on the preferred correction factor (family B, Mexican district shares).

Each row re-runs the family-B factor k with one assumption changed: the largest group districts
dropped (Los Angeles alone, the five largest), per-pupil spending over CCD fall-2023 membership
instead of F-33's fall-2022 enrollment, a narrower plausibility band, uncovered charter pupils priced
at 85% of their state's all-pupil mean, and districts matched only through their own Census geography.
Writes derived/robustness.csv; also each large district's share of the within-state lift
(derived/top_districts.csv) and F-33 district sums against the ASSF Table 8 prices the account uses
(derived/price_source_check.csv).

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/checks.py
"""
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import weighting as W  # noqa: E402

NAME = "mexican_district_share"
US_TABLE8 = 17619.389     # ASSF FY2024 Table 8, United States, current spending per pupil (_cache/elsec24_sumtables.xlsx)


def k_b(d, acct, assf, price="pp", uncovered_price_factor=None):
    t = W.state_table(d, price)
    if uncovered_price_factor is not None:
        # Uncovered pupils at factor x their state's all-pupil mean instead of the group-specific mean.
        p_all = t.P_all.copy()
        for name in ["all", NAME]:
            covered, total = t[f"Wmatched_{name}"], t[f"W_{name}"]
            unc = (total - covered).clip(lower=0)
            t[f"P_{name}"] = (covered * t[f"P_{name}"] + unc * uncovered_price_factor * p_all) / total
    row = [r for r in W.families(t, NAME, acct, assf) if r["family"] == "B"][0]
    row["k"] = row["R"] / row["R_embedded_same_concept"]
    return row


def main():
    d, _ = W.build()
    acct = pd.read_csv(W.OUT / "account_pupils_by_state.csv").set_index("fips")
    assf = pd.read_csv(W.STATE_PARAMS).set_index("fips").per_pupil_current_spending.reindex(acct.index)
    base = k_b(d, acct, assf)
    rows = [dict(check="baseline", **base)]
    top = d[d.valid].sort_values("w_mex_dist", ascending=False).LEAID
    for label, drop in [("drop Los Angeles Unified", ["0622710"]), ("drop five largest group districts", list(top.head(5)))]:
        dd = d.copy()
        dd.loc[dd.LEAID.isin(drop), "valid"] = False     # their pupils take the state's group mean
        rows.append(dict(check=label, **k_b(dd, acct, assf)))
    dd = d.copy()
    lea = W.read_f33()[0].set_index("LEAID")
    dd["pp_ccd"] = dd.LEAID.map(lea.TCURSPND) / dd.tot_all.where(dd.tot_all > 0)
    dd["valid"] = dd.valid & dd.pp_ccd.between(*W.PP_BAND)
    rows.append(dict(check="spending over CCD fall-2023 membership", **k_b(dd, acct, assf, price="pp_ccd")))
    dd = d.copy()
    dd["valid"] = dd.valid & dd.pp.between(5_000, 50_000)
    rows.append(dict(check="per-pupil band 5,000-50,000", **k_b(dd, acct, assf)))
    rows.append(dict(check="uncovered pupils at 0.85 x state all-pupil mean", **k_b(d, acct, assf, uncovered_price_factor=0.85)))
    rows.append(dict(check="uncovered pupils at 1.00 x state all-pupil mean", **k_b(d, acct, assf, uncovered_price_factor=1.0)))
    dd = d.copy()
    own = dd.share_source.eq("district")
    dd["w_mex_dist"] = np.where(own, dd.w_mex_dist, dd.w_mex_state)
    rows.append(dict(check="state share where no own district geography", **k_b(dd, acct, assf)))
    out = pd.DataFrame(rows)
    out["k_minus_baseline"] = out.k - base["k"]
    out.to_csv(W.OUT / "robustness.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(out[["check", "R", "k", "k_state_mix_only", "k_within_state_only", "k_minus_baseline"]].to_string(index=False))
    district_contributions(d, assf, base)
    price_sources(assf)


def district_contributions(d, assf, base):
    """Each district's share of the within-state lift: k_within - 1 = sum over districts of
    (W_s / Wmatched_s) w_d ASSF_s (pp_d / P_all_s - 1) / sum_s W_s ASSF_s. Writes derived/top_districts.csv."""
    t = W.state_table(d, "pp")
    v = d[d.valid & d.pp.notna()].copy()
    col = W.WEIGHTS[NAME]
    ws = t[f"W_{NAME}"]
    denom = (ws * assf.reindex(t.index)).sum()
    v["state_all_pupil_pp"] = v.fips.map(t.P_all)
    v["pp_over_state_mean"] = v.pp / v.state_all_pupil_pp
    v["lift"] = (v.fips.map(ws / t[f"Wmatched_{NAME}"]) * v[col] * v.fips.map(assf)
                 * (v.pp_over_state_mean - 1) / denom)
    total = v.lift.sum()
    if abs(total - (base["k_within_state_only"] - 1)) > 1e-9:
        raise SystemExit(f"[BLOCKED] district contributions {total} != k_within - 1 {base['k_within_state_only'] - 1}")
    v["group_pupils"] = v[col]
    v["share_of_lift"] = v.lift / total
    top = v.sort_values("group_pupils", ascending=False).head(25)
    keep = ["LEAID", "NAME", "fips", "group_pupils", "pp", "state_all_pupil_pp", "pp_over_state_mean", "lift", "share_of_lift"]
    top[keep].to_csv(W.OUT / "top_districts.csv", index=False, lineterminator="\n", float_format="%.6f")
    pos, neg = v.lift[v.lift > 0].sum(), v.lift[v.lift < 0].sum()
    print(f"\nwithin-state lift {total:.5f}: districts above their state mean +{pos:.5f}, below {neg:.5f}; "
          f"top 25 group districts {top.lift.sum():.5f}")
    print(top[keep].round(4).to_string(index=False))


def price_sources(assf):
    """F-33 district sums (TCURSPND / ENROLL) against the account's ASSF Table 8 prices, by state.
    Writes derived/price_source_check.csv."""
    f = pd.read_csv(W.F33, dtype={"NCESID": str, "FIPST": str},
                    usecols=["NCESID", "FIPST", "TCURSPND", "ENROLL", "TCURINST", "TCURSSVC", "TCURONON"])
    f["fips"] = f.FIPST.astype(int)
    # TCURSPND is instruction + support services + other non-instructional current spending, row by row.
    f["parts_equal"] = (f.TCURSPND - f.TCURINST - f.TCURSSVC - f.TCURONON).abs() <= 1
    g = f.groupby("fips")[["TCURSPND", "ENROLL"]].sum()
    g["tcurspnd_equals_components_share"] = f.groupby("fips").parts_equal.mean()
    g["f33_sum_per_pupil"] = g.TCURSPND * 1000 / g.ENROLL
    g["assf_table8_per_pupil"] = assf.reindex(g.index)
    g.loc[0, ["TCURSPND", "ENROLL"]] = g[["TCURSPND", "ENROLL"]].sum()
    g.loc[0, "f33_sum_per_pupil"] = g.loc[0, "TCURSPND"] * 1000 / g.loc[0, "ENROLL"]
    g.loc[0, "assf_table8_per_pupil"] = US_TABLE8
    g.loc[0, "tcurspnd_equals_components_share"] = f.parts_equal.mean()
    g["ratio"] = g.f33_sum_per_pupil / g.assf_table8_per_pupil
    # Share of current spending paid from COVID-19 federal assistance (F-33 item AE1), as weighting.py
    # removes it for the ex-relief prices.
    f33, covid_share = W.read_f33()
    g["covid_relief_share"] = covid_share.reindex(g.index)
    g.loc[0, "covid_relief_share"] = f33.AE1.sum() / f33.TCURSPND.sum()
    g = g.reset_index()
    g.to_csv(W.OUT / "price_source_check.csv", index=False, lineterminator="\n", float_format="%.6f")
    print("\n" + g[g.fips.isin([0, 4, 6, 17, 36, 48])].round(4).to_string(index=False))


if __name__ == "__main__":
    main()
