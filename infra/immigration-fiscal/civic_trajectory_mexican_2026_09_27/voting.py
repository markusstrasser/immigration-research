"""Registration and turnout by Mexican-origin generation, CPS November Voting and Registration
Supplement 2020, 2022 and 2024 (citizens 18+).

Files: Census public-use fixed-width files novYYpub.dat (inside novYYpub.zip) and, for 2022 and
2024, the 160 successive-difference replicate weights novYYrep.dat (4 implied decimals, joined on
QSTNUM + OCCURNUM), www2.census.gov/programs-surveys/cps/datasets/<year>/supp/. Column positions
are read from the record layouts in the technical documentation cpsnovYY.pdf (cached as text in
_cache/); PES1/PES2 sit two bytes earlier in 2020 than in 2022/2024. No replicate file exists for
November 2020.

Universe: PRTAGE >= 18, citizens (PRCITSHP 1-4), PRPERTYP 2 (adult civilian), PWSSWGT > 0.
Measures, Census convention (item non-response kept in the denominator as not voting):
  voted       PES1 = 1;
  registered  PES1 = 1 or PES2 = 1;
  voted_responders  PES1 = 1 among PES1 in (1, 2): the Hur-Achen alternative convention.
Groups (mutually exclusive dummies; reference = US-born non-Hispanic white alone, none of these):
  mexico_born_naturalized  PENATVTY 303, PRCITSHP 4;
  mexican_2nd_gen          US-born (PRCITSHP 1-3), a Mexico-born parent;
  mexican_3rd_plus         US-born, both parents born in US areas, PEHSPNON 1 and PRDTHSP 1;
  india_born_naturalized, indian_2nd_gen (context, same instrument).
Adjusted gaps: weighted LPM coefficients on group dummies. "ses": age band (7), sex, education
(5), family income bracket (6); "ses_state": plus state and metro status.

SEs: 2022 and 2024 use the replicate weights, SE = sqrt(4/160 sum (theta_r - theta)^2), every
estimate refitted per replicate. 2020 has no replicates: its SE is the weighted-LS sandwich (HC1)
SE multiplied by the mean ratio replicate-SE / sandwich-SE of the same estimate in 2022 and 2024
(column se_method says which). Pooled rows average the three year-specific estimates with equal
weight (two presidential elections, one midterm); CPS rotation (4-8-4 months) makes November
samples two years apart disjoint, so the pooled SE is sqrt(sum var)/3.
"""
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CPS, DERIVED = HERE / "_cache" / "cps", HERE / "derived"
US_AREAS = (57, 60, 66, 69, 73, 78)
R = 161
# 1-based inclusive positions from cpsnovYY.pdf record layouts
BASE = {"HEFAMINC": (39, 40), "GESTFIPS": (93, 94), "GTMETSTA": (105, 105), "PRTAGE": (122, 123),
        "PESEX": (129, 130), "PEEDUCA": (137, 138), "PTDTRACE": (139, 140), "PRDTHSP": (141, 142),
        "PEHSPNON": (157, 158), "PRPERTYP": (161, 162), "PENATVTY": (163, 165), "PEMNTVTY": (166, 168),
        "PEFNTVTY": (169, 171), "PRCITSHP": (172, 173), "PWSSWGT": (613, 622), "QSTNUM": (815, 819),
        "OCCURNUM": (820, 821), "PRDASIAN": (934, 935)}
VOTE = {2020: {"PES1": (1001, 1002), "PES2": (1003, 1004)},
        2022: {"PES1": (1003, 1004), "PES2": (1005, 1006)},
        2024: {"PES1": (1003, 1004), "PES2": (1005, 1006)}}
# unweighted tallies printed in the technical documentation (Attachment: frequencies)
TALLIES = {2020: {("PES1", 1): 55170, ("PES1", 2): 14114, ("PES1", -2): 1149, ("PES1", -3): 1281,
                  ("PES1", -9): 10184, ("PES2", 1): 4823, ("PES2", 2): 8933},
           2022: {("PES1", 1): 39280, ("PES1", 2): 22393, ("PES1", -2): 1527, ("PES1", -3): 1286,
                  ("PES2", 1): 12171, ("PES2", 2): 9928},
           2024: {("PES1", 1): 48387, ("PES1", 2): 14708, ("PES1", -2): 1080, ("PES1", -3): 1017,
                  ("PES2", 1): 5844, ("PES2", 2): 8541}}
# Census P20 Table 1, citizens 18+, both sexes: reported voted % and registered %
PUBLISHED = {2020: (66.8, 72.7, "https://www2.census.gov/programs-surveys/cps/tables/p20/585/table01.xlsx"),
             2022: (52.2, 69.1, "https://www2.census.gov/programs-surveys/cps/tables/p20/586/vote01_2022.xlsx"),
             2024: (65.3, 73.6, "https://www2.census.gov/programs-surveys/cps/tables/p20/587/vote01_2024.xlsx")}
GROUPS = ["mexico_born_naturalized", "mexican_2nd_gen", "mexican_3rd_plus", "india_born_naturalized",
          "indian_2nd_gen", "usb_nh_white", "usb_nh_white_3rd_plus", "all_citizens"]
DUMMIES = ["mexico_born_naturalized", "mexican_2nd_gen", "mexican_3rd_plus", "india_born_naturalized",
           "indian_2nd_gen"]
MEASURES = ["voted", "registered", "voted_responders"]


def read_fixed(zpath, name, layout):
    specs = [(a - 1, b) for a, b in layout.values()]
    with zipfile.ZipFile(zpath) as z:
        return pd.read_fwf(z.open(name), colspecs=specs, names=list(layout), header=None, dtype=float)


def load(year):
    yy = str(year)[2:]
    d = read_fixed(CPS / f"nov{yy}pub.zip", f"nov{yy}pub.dat", {**BASE, **VOTE[year]})
    bad = {k: (int((d[k[0]] == k[1]).sum()), v) for k, v in TALLIES[year].items() if int((d[k[0]] == k[1]).sum()) != v}
    assert not bad, f"{year}: tallies differ from the technical documentation: {bad}"
    d["PWSSWGT"] /= 1e4
    d["year"] = year
    d = d[(d.PRTAGE >= 18) & d.PRCITSHP.between(1, 4) & (d.PRPERTYP == 2) & (d.PWSSWGT > 0)].copy()
    if year in (2022, 2024):
        layout = {"QSTNUM": (1, 5), "OCCURNUM": (6, 7)}
        layout.update({f"W{r}": (8 + 10 * r, 17 + 10 * r) for r in range(R)})
        rep = read_fixed(CPS / f"nov{yy}rep.zip", f"nov{yy}rep.dat", layout)
        n = len(d)
        d = d.merge(rep, on=["QSTNUM", "OCCURNUM"], how="left", validate="one_to_one")
        assert len(d) == n and d.W0.notna().all(), f"{year}: replicate join lost rows"
        for r in range(R):
            d[f"W{r}"] = d[f"W{r}"] / 1e4
        assert np.allclose(d.W0, d.PWSSWGT, atol=1e-3), f"{year}: replicate 0 differs from PWSSWGT"
    else:
        for r in range(R):
            d[f"W{r}"] = d.PWSSWGT
    print(f"  ✓ {year}: tallies match; {len(d):,} citizens 18+", flush=True)
    return d.copy()


def classify(d):
    native = d.PRCITSHP.isin([1, 2, 3])
    fus, mus = d.PEFNTVTY.isin(US_AREAS), d.PEMNTVTY.isin(US_AREAS)
    mexp = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    indp = d.PEFNTVTY.eq(210) | d.PEMNTVTY.eq(210)
    nhw = d.PEHSPNON.eq(2) & d.PTDTRACE.eq(1)
    g = {"mexico_born_naturalized": d.PENATVTY.eq(303) & d.PRCITSHP.eq(4),
         "mexican_2nd_gen": native & mexp & ~indp,
         "mexican_3rd_plus": native & fus & mus & d.PEHSPNON.eq(1) & d.PRDTHSP.eq(1),
         "india_born_naturalized": d.PENATVTY.eq(210) & d.PRCITSHP.eq(4),
         "indian_2nd_gen": native & indp & ~mexp,
         "usb_nh_white": native & nhw, "usb_nh_white_3rd_plus": native & nhw & fus & mus,
         "all_citizens": pd.Series(True, index=d.index)}
    for k, v in g.items():
        d[k] = v.to_numpy()
    d["reference"] = d.usb_nh_white & ~d[DUMMIES].any(axis=1)
    d["voted"] = d.PES1.eq(1).astype(float)
    d["registered"] = (d.PES1.eq(1) | d.PES2.eq(1)).astype(float)
    d["voted_responders"] = np.where(d.PES1.isin([1, 2]), d.PES1.eq(1), np.nan)
    return d


def se_rep(theta):
    return float(np.sqrt(4.0 / 160.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def W(d):
    return d[[f"W{r}" for r in range(R)]].to_numpy(float)


def rate(d, measure):
    d = d[d[measure].notna()]
    w, y = W(d), d[measure].to_numpy(float)
    theta = (w * y[:, None]).sum(0) / w.sum(0)
    p, w0 = theta[0], w[:, 0]
    naive = float(np.sqrt(p * (1 - p) * (w0 ** 2).sum()) / w0.sum())  # Kish
    return theta, len(d), naive


def design(d, spec):
    parts = [pd.DataFrame({"const": 1.0}, index=d.index), d[DUMMIES].astype(float)]
    if spec != "raw":
        age = pd.cut(d.PRTAGE, [17, 24, 34, 44, 54, 64, 74, 200], labels=False)
        educ = pd.cut(d.PEEDUCA, [0, 38, 39, 42, 43, 46], labels=False)
        inc = pd.cut(d.HEFAMINC, [0, 7, 11, 13, 14, 15, 16], labels=False)
        parts += [pd.get_dummies(age, prefix="age", drop_first=True, dtype=float),
                  pd.get_dummies(educ, prefix="educ", drop_first=True, dtype=float),
                  pd.get_dummies(inc, prefix="inc", drop_first=True, dtype=float),
                  pd.DataFrame({"female": d.PESEX.eq(2).astype(float)}, index=d.index)]
    if spec == "ses_state":
        parts += [pd.get_dummies(d.GESTFIPS, prefix="st", drop_first=True, dtype=float),
                  pd.get_dummies(d.GTMETSTA, prefix="metro", drop_first=True, dtype=float)]
    x = pd.concat(parts, axis=1)
    return x.loc[:, (x.std() > 0) | (x.columns == "const")]


def lpm(d, measure, spec):
    d = d[d[measure].notna() & (d.reference | d[DUMMIES].any(axis=1))]
    assert d.HEFAMINC.between(1, 16).all() and d.PEEDUCA.between(31, 46).all(), "unexpected control codes"
    x = design(d, spec)
    X = x.to_numpy(float)
    assert np.linalg.matrix_rank(X) == X.shape[1], f"rank-deficient {measure} {spec}"
    y = d[measure].to_numpy(float)
    w = W(d)
    cols = [list(x.columns).index(g) for g in DUMMIES]
    same = np.allclose(w[:, 1], w[:, 0])
    coef = np.empty((1 if same else R, len(DUMMIES)))
    for r in range(coef.shape[0]):
        xw = X * w[:, r][:, None]
        coef[r] = np.linalg.solve(xw.T @ X, xw.T @ y)[cols]
    # HC1 sandwich on the full weight
    w0 = w[:, 0]
    xw = X * w0[:, None]
    bread = np.linalg.inv(xw.T @ X)
    e = y - X @ np.linalg.solve(xw.T @ X, xw.T @ y)
    meat = (X * (w0 * e)[:, None]).T @ (X * (w0 * e)[:, None])
    n, k = X.shape
    hc1 = np.sqrt(np.diag(bread @ meat @ bread) * n / (n - k))[cols]
    return coef, len(d), X.shape[1], hc1


def main():
    DERIVED.mkdir(exist_ok=True)
    data = {y: classify(load(y)) for y in (2020, 2022, 2024)}

    gate = ["CPS November turnout and registration, citizens 18+, lane vs Census P20 Table 1 "
            "(Census convention; tolerance 1 point on turnout)"]
    for y, (pv, pr, url) in PUBLISHED.items():
        tv, _, _ = rate(data[y], "voted")
        tr, _, _ = rate(data[y], "registered")
        ok = abs(100 * tv[0] - pv) <= 1.0
        gate.append(f"  {y}: voted {100 * tv[0]:.2f} vs {pv} ({100 * tv[0] - pv:+.2f}); registered "
                    f"{100 * tr[0]:.2f} vs {pr} ({100 * tr[0] - pr:+.2f}); weighted citizens "
                    f"{data[y].PWSSWGT.sum() / 1e3:,.0f}k  {'PASS' if ok else 'FAIL'}  [SOURCE: {url}]")
        assert ok, gate[-1]
    (DERIVED / "gate_turnout_published.txt").write_text("\n".join(gate) + "\n")
    print("\n".join(gate))

    rows = []
    # rates
    for y, d in data.items():
        for g in GROUPS:
            for m in MEASURES:
                theta, n, naive = rate(d[d[g]], m)
                rows.append(dict(kind="rate", year=y, group=g, measure=m, spec="raw", n=n, est=theta[0],
                                 se_rep=se_rep(theta) if y != 2020 else np.nan, se_naive=naive))
    # gaps
    for y, d in data.items():
        for m in MEASURES:
            for spec in ("raw", "ses", "ses_state"):
                coef, n, k, hc1 = lpm(d, m, spec)
                for j, g in enumerate(DUMMIES):
                    rows.append(dict(kind="gap", year=y, group=g, measure=m, spec=spec, n=n, est=coef[0, j],
                                     se_rep=se_rep(coef[:, j]) if y != 2020 else np.nan, se_naive=hc1[j]))
            print(f"  ✓ {y} {m} gaps", flush=True)
    t = pd.DataFrame(rows)
    # 2020 SE: sandwich/Kish SE x mean replicate/naive ratio of the same cell in 2022 and 2024
    key = ["kind", "group", "measure", "spec"]
    later = t[t.year != 2020].assign(ratio=lambda f: f.se_rep / f.se_naive).groupby(key).ratio.mean()
    t = t.join(later, on=key)
    t["se"] = np.where(t.year == 2020, t.se_naive * t.ratio, t.se_rep)
    t["se_method"] = np.where(t.year == 2020, "sandwich x mean 2022/2024 replicate ratio", "160 SDR replicates")
    pooled = t.groupby(key).agg(n=("n", "sum"), est=("est", "mean"),
                                se=("se", lambda s: float(np.sqrt((s ** 2).sum()) / 3))).reset_index()
    pooled["year"], pooled["se_method"] = "pooled_2020_2022_2024", "equal-weight mean of years, independent"
    pres = t[t.year.isin([2020, 2024])].groupby(key).agg(
        n=("n", "sum"), est=("est", "mean"), se=("se", lambda s: float(np.sqrt((s ** 2).sum()) / 2))).reset_index()
    pres["year"], pres["se_method"] = "presidential_2020_2024", "equal-weight mean of years, independent"
    t = pd.concat([t, pooled, pres], ignore_index=True)
    out = pd.DataFrame({"source": "CPS November Voting Supplement", "measure": t.measure + "_" + t.kind,
                        "generation": t.group, "year": t.year.astype(str), "n": t.n, "estimate": t.est,
                        "se": t.se, "se_method": t.se_method,
                        "adjustment": t.spec.map({"raw": "raw", "ses": "age, sex, education, family income",
                                                  "ses_state": "age, sex, education, family income, state, metro"})})
    out.to_csv(DERIVED / "voting.csv", index=False, float_format="%.6g", lineterminator="\n")
    show = out[(out.year == "pooled_2020_2022_2024")]
    print((show.pivot_table(index=["measure", "adjustment"], columns="generation", values="estimate") * 100).round(1).to_string())

    # item non-response by group, for the over-report discussion
    nr = []
    for y, d in data.items():
        for g in GROUPS:
            s = d[d[g]]
            nr.append(dict(year=y, group=g, n=len(s),
                           nonresponse=float(np.average(~s.PES1.isin([1, 2]), weights=s.PWSSWGT))))
    pd.DataFrame(nr).to_csv(DERIVED / "voting_nonresponse.csv", index=False, float_format="%.6g", lineterminator="\n")


if __name__ == "__main__":
    sys.exit(main())
