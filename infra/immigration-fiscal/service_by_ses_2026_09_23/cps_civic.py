"""Formal volunteering, charitable giving and veteran status by Mexican and Indian origin and
generation, CPS September Civic Engagement and Volunteering Supplement, 2021 and 2023 pooled.

Files: Census public-use CSVs `sep{21,23}pub.csv` and the 160 successive-difference replicate
weights for the supplement weight, `sep{21,23}nrrep.csv` (joined on QSTNUM and OCCURNUM),
www2.census.gov/programs-surveys/cps/datasets/20{21,23}/supp/. Documentation: cpssep23.pdf.

Measures (adults 18+ with a supplement interview, PRSUPINT = 1, weight PWNRWGT):
  volunteered       PRSUPVOL = 1, the published formal-volunteering measure (PES16 or the
                    PES16A prompt about school and youth activities);
  volunteered_pes16 PES16 = 1 among PES16 answers, the ladder-152 definition;
  gave_over_25      PES18 = 1 among answers: money or possessions worth more than $25 to a
                    non-political group such as a charity, school or religious organisation;
  veteran           PEAFEVER = 1 among answers: ever on active duty (civilians; the CPS does not
                    interview people now on active duty), the one military measure with parental
                    birthplace.
Groups: Mexico-born; second generation from either parent's birthplace (US-born); third-plus
Mexican = US-born, both parents US-born, Hispanic origin Mexican (PRDTHSP 1); the same for India
(no third-plus group is identifiable); US-born non-Hispanic whites are the reference.

SEs: 160 replicates, SE = sqrt(4/160 * sum_r (theta_r - theta)^2), every estimate refitted per
replicate. Adjusted gaps are weighted linear-probability coefficients on group dummies against
US-born non-Hispanic whites: "ses" controls age band, sex, education (5), family income bracket
(6) and survey year; "ses_geo" adds state and metro status. The veteran models use men born 1956
or later only. Family income and education are
treated as pre-determined for these outcomes, as the brief allows.
"""
import sys
import urllib.request
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
CPS, DERIVED = HERE / "_cache" / "cps", HERE / "derived"
YEARS = {2021: "sep21", 2023: "sep23"}
R = 161  # full weight + 160 replicates
US_AREAS = (57, 60, 66, 69, 73, 78, 96)
COLUMNS = ["QSTNUM", "OCCURNUM", "PRTAGE", "PESEX", "PEEDUCA", "HEFAMINC", "GESTFIPS", "GTMETSTA", "PTDTRACE",
           "PEHSPNON", "PRDTHSP", "PRDASIAN", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRCITSHP", "PRPERTYP",
           "PRSUPINT", "PRSUPVOL", "PES16", "PES16A", "PES18", "PEAFEVER", "PWNRWGT"]
# Attachment 13 of cpssep23.pdf: unweighted tallies to confirm the file is read correctly.
TALLIES_2023 = {("PES16", 1): 12478, ("PES16", 2): 32957, ("PES16A", 1): 2034, ("PES18", 1): 24185,
                ("PES18", 2): 20932, ("PRSUPVOL", 1): 14512, ("PRSUPVOL", 2): 33253, ("PRSUPINT", 1): 47765,
                ("PRSUPINT", 2): 33414}
# AmeriCorps open data "CEV Findings: National Rates of All Measures" (population 16+), as cached
# by indian_civic_cps_2026_09_18/_cache/americorps_cev_national.csv (data.americorps.gov/d/rhng-qtzw).
PUBLISHED = {"volunteered": {2021: 0.232, 2023: 0.283}, "gave_over_25": {2021: 0.481, 2023: 0.485}}
MEASURES = {"volunteered": ("PRSUPVOL", 1, (1, 2)), "volunteered_pes16": ("PES16", 1, (1, 2)),
            "gave_over_25": ("PES18", 1, (1, 2)), "veteran": ("PEAFEVER", 1, (1, 2))}
GROUPS = ["mexico_born", "mexico_born_citizen", "mexican_2nd_gen", "mexican_3rd_plus", "india_born",
          "india_born_citizen", "indian_2nd_gen", "usb_asian_indian_selfid", "usb_nh_white",
          "usb_nh_white_3rd_plus", "usb_all"]
# mutually exclusive dummies for the regressions; the reference is the remaining US-born NH whites
DUMMIES = ["mexico_born", "mexican_2nd_gen", "mexican_3rd_plus", "india_born", "indian_2nd_gen"]


def fetch(year, name):
    """Download a public-use file once and check it against the server's Content-Length."""
    target = CPS / name
    url = f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/supp/{name}"
    if not target.exists():
        CPS.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=1200) as response, open(target, "wb") as out:
            expected = int(response.headers["Content-Length"])
            while block := response.read(1 << 20):
                out.write(block)
        assert target.stat().st_size == expected, f"{name}: {target.stat().st_size} of {expected} bytes"
    return target


def load():
    frames = []
    for year, stem in YEARS.items():
        for name in (f"{stem}pub.csv", f"{stem}nrrep.csv"):
            fetch(year, name)
        pub = pd.read_csv(CPS / f"{stem}pub.csv", usecols=COLUMNS)
        if year == 2023:
            bad = {k: (int((pub[k[0]] == k[1]).sum()), v) for k, v in TALLIES_2023.items()
                   if int((pub[k[0]] == k[1]).sum()) != v}
            assert not bad, f"2023 tallies differ from Attachment 13: {bad}"
            print("  ✓ 2023 unweighted tallies match Attachment 13 of cpssep23.pdf")
        reps = pd.read_csv(CPS / f"{stem}nrrep.csv")
        reps.columns = [c.upper() if c.startswith("pwnrwgt") else c for c in reps.columns]
        frame = pub.merge(reps, on=["QSTNUM", "OCCURNUM"], how="left", validate="one_to_one")
        frame = frame[frame.PRSUPINT == 1].copy()
        assert frame["PWNRWGT0"].notna().all(), "supplement respondents without replicate weights"
        assert np.allclose(frame["PWNRWGT0"], frame["PWNRWGT"]), "replicate 0 differs from PWNRWGT"
        frame["year"] = year
        frames.append(frame)
        print(f"  ✓ {year}: {len(frame):,} supplement respondents")
    return pd.concat(frames, ignore_index=True)


def classify(d):
    native = d.PRCITSHP.isin([1, 2, 3])
    father_us, mother_us = d.PEFNTVTY.isin(US_AREAS), d.PEMNTVTY.isin(US_AREAS)
    mex_parent = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    ind_parent = d.PEFNTVTY.eq(210) | d.PEMNTVTY.eq(210)
    nh_white = d.PEHSPNON.eq(2) & d.PTDTRACE.eq(1)
    g = {
        "mexico_born": d.PENATVTY.eq(303) & ~native,
        "mexico_born_citizen": d.PENATVTY.eq(303) & d.PRCITSHP.eq(4),
        "mexican_2nd_gen": native & mex_parent & ~ind_parent,
        "mexican_3rd_plus": native & father_us & mother_us & d.PEHSPNON.eq(1) & d.PRDTHSP.eq(1),
        "india_born": d.PENATVTY.eq(210) & ~native,
        "india_born_citizen": d.PENATVTY.eq(210) & d.PRCITSHP.eq(4),
        "indian_2nd_gen": native & ind_parent & ~mex_parent,
        "usb_asian_indian_selfid": native & d.PRDASIAN.eq(1),
        "usb_nh_white": native & nh_white,
        "usb_nh_white_3rd_plus": native & nh_white & father_us & mother_us,
        "usb_all": native,
    }
    for name, mask in g.items():
        d[name] = mask.to_numpy()
    d["reference"] = d.usb_nh_white & ~d[DUMMIES].any(axis=1)
    return d


def se(theta):
    return float(np.sqrt(4.0 / 160.0 * np.sum((theta[1:] - theta[0]) ** 2)))


def weights(d):
    return d[[f"PWNRWGT{r}" for r in range(R)]].to_numpy(float)


def rate(d, measure):
    var, yes, answered = MEASURES[measure]
    d = d[d[var].isin(answered)]
    w = weights(d)
    y = d[var].eq(yes).to_numpy(float)
    return (w * y[:, None]).sum(0) / w.sum(0), len(d)


def design(d, spec):
    age = pd.cut(d.PRTAGE, [17, 24, 34, 44, 54, 64, 74, 200], labels=False)
    educ = pd.cut(d.PEEDUCA, [0, 38, 39, 42, 43, 46], labels=False)  # <HS, HS, some college/AA, BA, graduate
    income = pd.cut(d.HEFAMINC, [0, 7, 11, 13, 14, 15, 16], labels=False)  # <25k,25-50,50-75,75-100,100-150,150k+
    parts = [pd.DataFrame({"const": 1.0}, index=d.index), d[DUMMIES].astype(float)]
    if spec != "raw":
        parts += [pd.get_dummies(age, prefix="age", drop_first=True, dtype=float),
                  pd.get_dummies(educ, prefix="educ", drop_first=True, dtype=float),
                  pd.get_dummies(income, prefix="inc", drop_first=True, dtype=float),
                  pd.DataFrame({"female": d.PESEX.eq(2).astype(float)}, index=d.index)]
    parts.append(pd.DataFrame({"y2023": d.year.eq(2023).astype(float)}, index=d.index))
    if spec == "ses_geo":
        parts += [pd.get_dummies(d.GESTFIPS, prefix="st", drop_first=True, dtype=float),
                  pd.get_dummies(d.GTMETSTA, prefix="metro", drop_first=True, dtype=float)]
    x = pd.concat(parts, axis=1)
    x = x.loc[:, x.std() > 0].assign(const=1.0) if spec != "raw" else x
    return x


def lpm(d, measure, spec):
    var, yes, answered = MEASURES[measure]
    d = d[d[var].isin(answered) & (d.reference | d[DUMMIES].any(axis=1))]
    assert d.HEFAMINC.between(1, 16).all() and d.PEEDUCA.between(31, 46).all(), "unexpected control codes"
    x = design(d, spec)
    X = x.to_numpy(float)
    assert np.linalg.matrix_rank(X) == X.shape[1], f"rank-deficient design for {measure} {spec}"
    y = d[var].eq(yes).to_numpy(float)
    w = weights(d)
    columns = [list(x.columns).index(g) for g in DUMMIES]
    coef = np.empty((R, len(DUMMIES)))
    for r in range(R):
        xw = X * w[:, r][:, None]
        coef[r] = np.linalg.solve(xw.T @ X, xw.T @ y)[columns]
    return coef, len(d), X.shape[1]


def main():
    DERIVED.mkdir(exist_ok=True)
    d = classify(load())
    adults = d[(d.PRTAGE >= 18) & (d.PWNRWGT > 0)]

    lines = ["National rates, population 16+, lane vs AmeriCorps published (same supplement):"]
    for measure, published in PUBLISHED.items():
        for year, value in published.items():
            theta, _ = rate(d[(d.year == year) & (d.PRTAGE >= 16)], measure)
            lines.append(f"  {measure:14s} {year}  lane {theta[0]:6.1%}  published {value:6.1%}  "
                         f"delta {100 * (theta[0] - value):+.1f} points")
    gate = "\n".join(lines)
    (DERIVED / "gate_cps_published.txt").write_text(gate + "\n")
    print(gate)

    rows = []
    arms = {"adults_18_plus": adults, "ba_plus": adults[adults.PEEDUCA >= 43],
            "family_income_100k_plus": adults[adults.HEFAMINC >= 15],
            "men_18_49": adults[(adults.PESEX == 1) & adults.PRTAGE.between(18, 49)],
            "men_18_plus_born_1956_on": adults[(adults.PESEX == 1) & (adults.year - adults.PRTAGE >= 1956)],
            "women_18_49": adults[(adults.PESEX == 2) & adults.PRTAGE.between(18, 49)]}
    for arm, frame in arms.items():
        white = {m: rate(frame[frame.usb_nh_white], m)[0] for m in MEASURES}
        for group in GROUPS:
            sub = frame[frame[group]]
            for measure in MEASURES:
                if arm.startswith(("men_", "women_")) and measure != "veteran":
                    continue
                theta, n = rate(sub, measure)
                rows.append({"arm": arm, "group": group, "measure": measure, "n": n, "rate": theta[0], "se": se(theta),
                             "diff_vs_nh_white_points": 100 * (theta[0] - white[measure][0]),
                             "diff_se_points": 100 * se(theta - white[measure])})
    rates = pd.DataFrame(rows)
    rates.to_csv(DERIVED / "cps_civic_rates.csv", index=False, float_format="%.6g", lineterminator="\n")

    gap_rows = []
    # veteran status: men born 1956 or later (post-draft cohorts), as in the ACS tables
    samples = {"veteran": adults[(adults.PESEX == 1) & (adults.year - adults.PRTAGE >= 1956)]}
    for measure in ("volunteered", "volunteered_pes16", "gave_over_25", "veteran"):
        for spec in ("raw", "ses", "ses_geo"):
            coef, n, k = lpm(samples.get(measure, adults), measure, spec)
            for j, group in enumerate(DUMMIES):
                gap_rows.append({"measure": measure, "spec": spec, "group": group, "n_model": n, "columns": k,
                                 "gap_points": 100 * coef[0, j], "se_points": 100 * se(coef[:, j])})
        print(f"  ✓ regressions: {measure}", flush=True)
    gaps = pd.DataFrame(gap_rows)
    gaps.to_csv(DERIVED / "cps_civic_gaps.csv", index=False, float_format="%.6g", lineterminator="\n")

    show = rates[rates.arm == "adults_18_plus"].pivot(index="group", columns="measure", values="rate")
    print("\n  adults 18+, pooled 2021+2023 rates\n", (100 * show).round(1).to_string())
    print("\n  gaps vs US-born NH whites (points)\n",
          gaps.pivot_table(index=["measure", "group"], columns="spec", values="gap_points").round(1).to_string())


if __name__ == "__main__":
    sys.exit(main())
