"""English-learner check: revealed marginal current spending per English learner within states.

District current spending per pupil (Census F-33) on the district's English-learner share (NCES CCD
LEA file 141, 2018-19, the last public district EL release held here) and child-poverty share (SAIPE),
with state fixed effects and log enrollment, weighted by enrollment; standard errors clustered by
state. Two years: FY2019 spending with 2018-19 EL counts and SAIPE 2018 (year-matched), and FY2024
spending with the same EL shares and SAIPE 2023 (lagged EL). The coefficient is dollars per pupil
for a district made entirely of English learners, i.e. revealed marginal spending per English
learner; it includes whatever formula money follows EL counts to the district.

The within-district EL premium the district weighting cannot see is bounded by
coefficient x (group EL rate - EL rate of the group's districts). The group's EL rate is not
measured administratively; it is scaled from ACS 2024 English ability (speaks English less than
"very well") of Mexican-origin versus all public K-12 pupils. Writes derived/el_regression.csv and
derived/el_within_district.json.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
      python3 infra/immigration-fiscal/school_cost_where_enrolled_2026_09_24/el_check.py
"""
import json
import sys

sys.dont_write_bytecode = True
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ccd  # noqa: E402
from weighting import F33, PP_BAND, build  # noqa: E402

ROOT = HERE.parents[2]
F33_19 = HERE / "_cache/elsec19t.txt"
SAIPE = {2018: HERE / "_cache/ussd18.txt",
         2023: ROOT / "sources/immigration-fiscal/data/external/stage4/saipe/ussd23.txt"}


def f33(path):
    """FY2024 is comma-delimited with SCHLEV; FY2019 is tab-delimited without it (level taken from FY2024)."""
    sep = "\t" if "\t" in Path(path).open().readline() else ","
    d = pd.read_csv(path, sep=sep, dtype={"NCESID": str, "SCHLEV": str, "CONUM": str})
    d = d[d.NCESID.notna() & d.NCESID.str.strip().ne("")].copy()
    d["LEAID"] = d.NCESID.str.strip().str.zfill(7)
    d["fips"] = d.LEAID.str[:2].astype(int)
    d["ENROLL"] = pd.to_numeric(d.ENROLL, errors="coerce")
    d["pp"] = pd.to_numeric(d.TCURSPND, errors="coerce") * 1000 / d.ENROLL.where(d.ENROLL > 0)
    if "SCHLEV" not in d:
        level = pd.read_csv(F33, dtype={"NCESID": str, "SCHLEV": str}, usecols=["NCESID", "SCHLEV"])
        d["SCHLEV"] = d.LEAID.map(level.set_index(level.NCESID.str.zfill(7)).SCHLEV)
    return d[["LEAID", "fips", "SCHLEV", "ENROLL", "pp"]]


def saipe(path):
    rows = []
    for line in path.read_text(encoding="latin-1").splitlines():
        if len(line) < 108 or line[:2] == "00":
            continue
        rows.append(dict(LEAID=line[0:2] + line[3:8], kids=float(line[91:99]), poor=float(line[100:108])))
    s = pd.DataFrame(rows)
    s["pov_share"] = s.poor / s.kids.where(s.kids > 0)
    return s[["LEAID", "pov_share", "kids"]]


def fe_wls(df, y, xs, w, cluster):
    """Weighted least squares with fixed effects by `cluster` (state), cluster-robust SEs by state."""
    df = df.dropna(subset=[y] + xs + [w]).copy()
    wt = df[w].to_numpy(float)

    def demean(col):
        v = df[col].to_numpy(float)
        g = df.groupby(cluster)
        m = g[col].transform(lambda s: np.average(s, weights=df.loc[s.index, w]))
        return v - m.to_numpy(float)
    Y = demean(y)
    X = np.column_stack([demean(x) for x in xs])
    sw = np.sqrt(wt)
    Xw, Yw = X * sw[:, None], Y * sw
    beta, *_ = np.linalg.lstsq(Xw, Yw, rcond=None)
    resid = Yw - Xw @ beta
    bread = np.linalg.inv(Xw.T @ Xw)
    meat = np.zeros((len(xs), len(xs)))
    for _, idx in df.groupby(cluster).indices.items():
        s = Xw[idx].T @ resid[idx]
        meat += np.outer(s, s)
    g = df[cluster].nunique()
    n, k = len(df), len(xs) + g
    vcov = bread @ meat @ bread * g / (g - 1) * (n - 1) / (n - k)
    return beta, np.sqrt(np.diag(vcov)), len(df), g


def main():
    el = ccd.el_1819()
    el = el[el.DMS_FLAG.eq("Reported")]
    rows = []
    frames = {}
    for year, path, saipe_year in [(2019, F33_19, 2018), (2024, F33, 2023)]:
        d = f33(path).merge(el[["LEAID", "LEP_COUNT"]], on="LEAID", how="inner")
        d = d.merge(saipe(SAIPE[saipe_year]), on="LEAID", how="left")
        enroll_19 = f33(F33_19).set_index("LEAID").ENROLL
        d["el_share"] = d.LEP_COUNT / d.LEAID.map(enroll_19)
        keep = (d.SCHLEV.isin(["01", "02", "03"]) & d.pp.between(*PP_BAND) & d.ENROLL.ge(100)
                & d.el_share.between(0, 1) & d.fips.le(56))
        d = d[keep].copy()
        d["log_enroll"] = np.log(d.ENROLL)
        frames[year] = d
        for label, xs in [("el_only", ["el_share", "log_enroll"]), ("el_poverty", ["el_share", "pov_share", "log_enroll"])]:
            beta, se, n, g = fe_wls(d, "pp", xs, "ENROLL", "fips")
            mean_pp = np.average(d.pp, weights=d.ENROLL)
            for x, b, s in zip(xs, beta, se):
                rows.append(dict(spending_year=f"FY{year}", el_year="2018-19", saipe_year=saipe_year, model=label,
                                 term=x, coef=b, se=s, n_districts=n, states=g, weighted_mean_pp=mean_pp,
                                 coef_over_mean_pp=b / mean_pp))
    reg = pd.DataFrame(rows)
    out = HERE / "derived"
    reg.to_csv(out / "el_regression.csv", index=False, lineterminator="\n", float_format="%.6f")

    # Group EL exposure: EL share of the districts where the group enrolls (2018-19 EL over F-33 FY2019
    # enrollment; 2023-24 group weights), against the group's own EL rate scaled from ACS English ability.
    d, _ = build()
    d = d.merge(frames[2019][["LEAID", "el_share"]], on="LEAID", how="left")
    have = d.el_share.notna()
    el_all = np.average(d.el_share[have], weights=d.w_all[have])
    el_groups_districts = np.average(d.el_share[have], weights=d.w_mex_dist[have])
    acs = pd.read_csv(out / "acs_state_pupils.csv").set_index("state_fips").loc[0]
    scale = acs.mex_pupil_eng_lt_very_well_rate / acs.pupil_eng_lt_very_well_rate
    group_el_rate = min(1.0, el_all * scale)
    b = reg[(reg.model == "el_poverty") & (reg.term == "el_share")].set_index("spending_year")
    result = dict(
        el_share_all_pupils_weighted=el_all, el_share_of_groups_districts=el_groups_districts,
        acs_eng_lt_very_well_mexican=acs.mex_pupil_eng_lt_very_well_rate, acs_eng_lt_very_well_all=acs.pupil_eng_lt_very_well_rate,
        group_el_rate_scaled=group_el_rate, coverage_all=float(d.w_all[have].sum() / d.w_all.sum()),
        coverage_group=float(d.w_mex_dist[have].sum() / d.w_mex_dist.sum()),
        coef_fy2024=float(b.coef["FY2024"]), se_fy2024=float(b.se["FY2024"]),
        coef_fy2019=float(b.coef["FY2019"]), se_fy2019=float(b.se["FY2019"]),
        within_district_el_premium_per_group_pupil_fy2024=float(b.coef["FY2024"] * (group_el_rate - el_groups_districts)),
        note=("Upper-bound style: assumes the whole revealed EL coefficient is spent on EL pupils themselves; "
              "the district weighting already carries the between-district part."),
    )
    (out / "el_within_district.json").write_text(json.dumps(result, indent=1) + "\n")
    print(reg.to_string(index=False))
    print(json.dumps(result, indent=1))


if __name__ == "__main__":
    main()
