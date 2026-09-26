"""Size the 2020 ACS no-schooling step in scale_spillovers_2026_09_23's years-of-schooling items
(ACS 2024 PUMS; SCHL 1-3 scored 0 years, grades 1-11 scored 1-11).

Items affected: workers' mean years by label (dYRS, dHSY and Iranzo-Peri's dIPHS move by the same
amount, since every re-scored report is below 12 years) and the Mexico-born adults' (25+) mean
years that the innovation arm sets against BCHTT's pre-2020 10.88. Corrections by sub-group:
  mexborn      -> flow rates of the fixed Mexico-born population
  group_other  -> US-born Hispanic rates (the label is Mexican-origin Hispanics born outside Mexico)
  other        -> US-born, other Latin American Hispanic and non-Hispanic foreign-born rates
Method B only (flow rates); method A is shown for the Mexico-born with phi from its 20-64 level ratio
and 2019 grades 1-8 mix. Area-level (CZ, CBSA) specs are not re-run: the national change in dYRS
scales the linear average-schooling specs, and the innovation arm is recomputed from its formula.
A positive control first reproduces the lane's national totals from the same PUMS file.
Output: derived/scale_spillovers_corrected.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/acs_schooling_break_2026_09_26/fix_scale_spillovers.py
"""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import breakfix as B  # noqa: E402
import break_anatomy as A  # noqa: E402

LANE = ROOT / "infra/immigration-fiscal/scale_spillovers_2026_09_23"
NATIONAL = LANE / "derived/pums_national.csv"
INNOV = LANE / "derived/innovation_bchtt.csv"
YEARS = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10,
         14: 11, 15: 11.5, 16: 12, 17: 12, 18: 12.5, 19: 13.5, 20: 14, 21: 16, 22: 18, 23: 19, 24: 20}
BCHTT_MEAN_YEARS = 10.88
BCHTT_SLOPE = {"patents": 0.235, "wages": 0.199}   # arms.py BCHTT *_x_years, Table 9 col 2


def load(year: int) -> pd.DataFrame:
    p = A.CACHE / f"acs_person_{year}.parquet"
    B.gate(A.sha256(p) == A.SHA[year], f"[BLOCKED] {p.name} hash")
    d = pd.read_parquet(p, columns=["AGEP", "SCHL", "POBP", "HISP", "NATIVITY", "ESR", "PWGTP"])
    grp = d.HISP.eq(2) | d.POBP.eq(303)
    d["label"] = np.where(grp & d.POBP.eq(303), "mexborn", np.where(grp, "group_other", "other"))
    d["sub"] = np.where(d.label == "mexborn", "mexico_born",
                np.where(d.label == "group_other", "usborn_hispanic",
                 np.where(d.NATIVITY.eq(1), "usborn",
                  np.where(d.HISP.ne(1), "other_latam_hispanic_fb", "non_hispanic_fb"))))
    d["yrs"] = d.SCHL.fillna(0).astype(int).map(YEARS).fillna(0.0)
    d["worker"] = d.ESR.isin([1, 2, 4, 5])
    d["adult25"] = d.AGEP >= 25
    return d


def added_years(g: pd.DataFrame, rates: dict) -> tuple[float, float, float]:
    """Weighted years added by returning the excess no-schooling reports (method B), phi, dest mean."""
    if (g.SCHL == 1).sum() == 0:
        return 0.0, 0.0, np.nan
    phi, dest = B.split_b(B.weights_by_code(g.SCHL.astype(int).to_numpy(), g.PWGTP.to_numpy(float)), rates, "schl")
    y = sum(YEARS[k] * v for k, v in dest.items())
    return phi * float(g.PWGTP[g.SCHL == 1].sum()) * y, phi, y


def main() -> None:
    d = load(2024)
    nat = pd.read_csv(NATIONAL)
    est = lambda lab, item: float(nat[(nat.label == lab) & (nat.item == item)].estimate.iloc[0])  # noqa: E731
    tot = {}
    for lab, g in d.groupby("label"):
        w = g.PWGTP.astype(float)
        tot[lab] = {"workers": float(w[g.worker].sum()), "workers_yrs": float((w * g.yrs)[g.worker].sum()),
                    "adults25": float(w[g.adult25].sum()), "adults25_yrs": float((w * g.yrs)[g.adult25].sum())}
        for k, v in tot[lab].items():
            B.gate(abs(v / est(lab, k) - 1) < 1e-9, f"[BLOCKED] control {lab} {k}: {v} vs {est(lab, k)}")
    print("positive control passed: national totals equal the lane's pums_national.csv", flush=True)

    rates = {s: B.flow_rates(s, "fixed") for s in d["sub"].unique()}
    add = {lab: {"workers_yrs": 0.0, "adults25_yrs": 0.0} for lab in tot}
    params = []
    for (lab, sub), g in d.groupby(["label", "sub"]):
        for univ, mask in (("workers_yrs", g.worker), ("adults25_yrs", g.adult25)):
            a, phi, y = added_years(g[mask], rates[sub])
            add[lab][univ] += a
            params.append({"label": lab, "sub": sub, "universe": univ, "phi": phi, "dest_mean_years": y,
                           "added_years_per_person": a / float(g.PWGTP[mask].sum())})

    scale = 40_896_574 / 39_429_519   # arms.py SCALE: group scaled to the CPS union, differenced out of others

    def dyrs(t):
        g0 = {k: t["mexborn"][k] + t["group_other"][k] for k in ("workers", "workers_yrs")}
        g = {k: scale * v for k, v in g0.items()}
        o = {k: t["other"][k] - (scale - 1) * g0[k] for k in g0}
        return o["workers_yrs"] / o["workers"] - (g["workers_yrs"] + o["workers_yrs"]) / (g["workers"] + o["workers"])

    corr = {lab: {k: v + (add[lab][k] if k in add[lab] else 0.0) for k, v in t.items()} for lab, t in tot.items()}
    rows = [{"item": "dYRS national (years)", "published": 0.255, "uncorrected": dyrs(tot), "method_B": dyrs(corr)}]
    for lab in tot:
        rows.append({"item": f"{lab} workers' mean years", "published": est(lab, "workers_yrs") / est(lab, "workers"),
                     "uncorrected": tot[lab]["workers_yrs"] / tot[lab]["workers"],
                     "method_B": corr[lab]["workers_yrs"] / corr[lab]["workers"]})
    y0 = tot["mexborn"]["adults25_yrs"] / tot["mexborn"]["adults25"]
    yb = corr["mexborn"]["adults25_yrs"] / corr["mexborn"]["adults25"]
    # method A for the Mexico-born adults: phi from the 20-64 level ratio, 2019 grades 1-8 mix of adults 25+
    S = pd.read_csv(A.DERIVED / "break_anatomy_shares.csv")
    s = S[(S.universe == "age20_64") & (S.group == "mexico_born") & (S.category == "none")].set_index("year").share_pct
    phi_a = 1 - s[2019] / s[2024]
    d19 = load(2019)
    m19 = d19[(d19.label == "mexborn") & d19.adult25]
    dest_a = B.split_a(B.weights_by_code(m19.SCHL.astype(int).to_numpy(), m19.PWGTP.to_numpy(float)), "schl")
    m24 = d[(d.label == "mexborn") & d.adult25]
    ya = y0 + phi_a * float(m24.PWGTP[m24.SCHL == 1].sum()) * B.mean_years(dest_a, "schl") / tot["mexborn"]["adults25"]
    rows.append({"item": "mexborn adults 25+ mean years (innovation arm)", "published": est("mexborn", "mean_years_adults25"),
                 "uncorrected": y0, "method_B": yb, "method_A": ya})
    inn = pd.read_csv(INNOV)
    for out in ("patents", "wages"):
        r = inn[(inn.outcome_ratio == out) & inn.spec.str.startswith("linear")].iloc[0]
        per_eff = r.gain_bn / r.effect_per_1000
        rows.append({"item": f"innovation {out} gain $bn (linear spec)", "published": r.gain_bn,
                     "uncorrected": per_eff * r.effect_per_1000,
                     "method_B": per_eff * (r.effect_per_1000 + BCHTT_SLOPE[out] * (yb - y0)),
                     "method_A": per_eff * (r.effect_per_1000 + BCHTT_SLOPE[out] * (ya - y0))})
    R = pd.DataFrame(rows)
    R.to_csv(HERE / "derived" / "scale_spillovers_corrected.csv", index=False, float_format="%.5f", lineterminator="\n")
    pd.DataFrame(params).to_csv(HERE / "derived" / "scale_spillovers_correction_params.csv", index=False,
                                float_format="%.5f", lineterminator="\n")
    pd.set_option("display.width", 200)
    print(R.to_string(index=False, float_format=lambda v: f"{v:.4f}"))
    print(pd.DataFrame(params).to_string(index=False, float_format=lambda v: f"{v:.4f}"))


if __name__ == "__main__":
    main()
