"""Brief part A: the place premium of the group's US-born second generation, with the first generation's
direct 2024 check against Clemens-Montenegro-Pritchett (CMP) and bounds for the third-plus generation.
Case-independent.

Convention (brief correction 3). G2's counterfactual is a controlled rearing comparison: the same person,
raised in Mexico by parents with the same schooling who stayed. It is not a history in which nobody migrated
(that person and Mexico's wages would both be different). Earnings are annual, per person, zeros included,
so employment and hours differences are part of the premium; both are reported separately.

US side: CPS ASEC 2025 (income year 2024) through the distribution lane's loader, the account's group
definition; earnings = PEARNVAL floored at zero, employment = worked last year (WORKYN), hours = HRSWK.
Mexico side (mexico.py, ENIGH 2024 in PPP dollars), gross pay like the CPS: pay as received plus the 2024
statutory withholding on formal jobs; the withheld tax, the pay as received and the consumption taxes on gross
pay at the household decile's IVA and IEPS rate are reported beside it (mexico_withheld_tax_bn,
mexico_take_home_bn, mexico_consumption_tax_bn).
- ages 25+: final schooling drawn from ESRU-EMOVI 2017, P(own | parents' schooling, sex, birth cohort),
  priced at the sex x age band x schooling cell;
- ages 15-24: Mexicans of that sex and age band whose co-resident parents have the given schooling;
- under 15: no labor income in either place.
Parents' schooling: IPUMS-CPS ASEC 1994-2025, US-born children 0-17 with a Mexico-born parent in the household,
the more-schooled Mexico-born parent, by the child's birth cohort.
Selection: the first generation sits at the 56th percentile of Mexico's residual wages (CMP, Ro/Re = 2.53/2.46).
The children inherit none of it (delta 0) or all of it (delta 0.028).

Outputs (derived/): g2_premium.csv (G1 check, G2, G3+ bound), g2_premium_by_age.csv, parents_schooling.csv,
group_ages.csv, g2_meta.json. --basis row4 counts the group on the account's row-4 persons (population_basis.py)
and writes g2_premium_row4.csv, group_ages_row4.csv and g2_meta_row4.json; the other two files do not depend on the
basis (IPUMS parents; G2 by age, whose records row 4 leaves alone).
Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/g2_premium.py [--basis row4]
"""
import argparse
import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from population_basis import BASES, reweight, row4, suffixed

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]
DERIVED = HERE / "derived"
IPUMS = REPO / "sources/immigration-fiscal/data/external/cps/cps_2ndgen.csv.gz"
IPUMS_SHA = "a510e7a9695486945fc87618b98e2f8d51f7d0d7df35f01319a70564ea8065a2"
CATS = ["none", "primaria_incompleta", "primaria", "secundaria", "preparatoria", "profesional"]
AGE_BANDS = [15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 200]
# CMP (2019 REStat; SSRN 1211427) for Mexico: Ro 2.53 (observably identical), Re 2.46 (selection-adjusted,
# migrants from the 56th percentile of residual wages), Table 8 Re 2.79 / 2.08 at the 50th / 70th percentiles.
# [SOURCE: corpus doi_10_2139_ssrn_1211427, quoted in the task-1 answer placegain.md]
CMP_RO, CMP_RE = 2.53, 2.46
G1_SELECTION = {"p50": CMP_RO / 2.79 - 1, "p56": CMP_RO / CMP_RE - 1, "p70": CMP_RO / 2.08 - 1}
G2_INHERITED = {"none": 0.0, "all": CMP_RO / CMP_RE - 1}
DIPLOMA_REREAD = (0.0, 0.25, 0.5)       # share of Mexico-schooled "high-school diplomas" read as secundaria
# Mishra (IMF WP/06/86, p. 16): the 1970-2000 outflow raised wages of high-school dropouts 5%, graduates 15%,
# some college 13%, college graduates about 2%, the average worker 8%. If the group lived in Mexico, wages there
# would be lower by that much: E_MX* = E_MX / (1 + x). [SOURCE: reads/mishra_2007.md quote 12]
MISHRA_X = {0: 0.05, 1: 0.05, 2: 0.05, 3: 0.05, 4: 0.14, 5: 0.02}
MISHRA_AVG = 0.08
MIN_N = 30                               # smallest EMOVI cell used before pooling


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for block in iter(lambda: fh.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def band_of(age):
    a = np.asarray(age, float)
    i = np.clip(np.searchsorted(AGE_BANDS, a, side="right") - 1, 0, len(AGE_BANDS) - 2)
    lab = np.array([f"{lo}-{hi - 1}" if hi < 200 else f"{lo}+" for lo, hi in zip(AGE_BANDS[:-1], AGE_BANDS[1:])])
    return lab[i]


def parent_bin(birth_year):
    """Birth-cohort bins of the IPUMS parents' table; earlier cohorts take the first bin (flagged)."""
    edges = [1981, 1986, 1991, 1996, 2001, 2006, 2011]
    labels = ["1976-80", "1981-85", "1986-90", "1991-95", "1996-2000", "2001-05", "2006-10", "2011-25"]
    return np.array(labels)[np.searchsorted(edges, np.asarray(birth_year), side="right")]


def emovi_cohort(birth_year):
    b = np.asarray(birth_year)
    return np.select([b <= 1962, b <= 1972, b <= 1982], ["1953-62", "1963-72", "1973-82"], "1983-92")


# ------------------------------------------------------------------ US side: CPS ASEC 2025
def load_asec(basis="cps"):
    spec = importlib.util.spec_from_file_location("dist_base", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    d["pw_cps"] = d.pw
    if basis == "row4":
        d = reweight(d, B.PATHS["cps"], gate)
    extra = ["PH_SEQ", "PPPOS", "A_SEX", "WORKYN", "HRSWK", "PEINUSYR"]
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=extra)
    gate("asec_extra_columns_aligned", np.array_equal(p.PH_SEQ.to_numpy(), d.PH_SEQ.to_numpy())
         and np.array_equal(p.PPPOS.to_numpy(), d.PPPOS.to_numpy()), records=len(d))
    for c in extra[2:]:
        d[c] = p[c].to_numpy()
    tgt = d.target.to_numpy()
    usb = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    mexpar = d.PEFNTVTY.eq(303).to_numpy() | d.PEMNTVTY.eq(303).to_numpy()
    d["gen"] = np.select([tgt & ~usb & d.PENATVTY.eq(303).to_numpy(), tgt & usb & mexpar, tgt & usb & ~mexpar],
                         ["G1", "G2", "G3+"], "")
    d["sex"] = np.where(d.A_SEX.eq(1), "male", "female")
    d["earn"] = np.maximum(d.PEARNVAL.to_numpy(float), 0.0)
    d["works"] = d.WORKYN.eq(1)
    d["birth_year"] = 2025 - d.A_AGE
    hga = d.A_HGA.to_numpy()
    # CPS A_HGA to the six categories: 31 none; 32 grades 1-4; 33 grades 5-6 and 34 grades 7-8 primaria; 35-38
    # grades 9-12 without a diploma secundaria; 39 diploma to 42 associate preparatoria; 43+ profesional.
    d["own_cat"] = np.select([hga == 31, hga == 32, np.isin(hga, [33, 34]), np.isin(hga, [35, 36, 37, 38]),
                              np.isin(hga, [39, 40, 41, 42]), hga >= 43], [0, 1, 2, 3, 4, 5], -1)
    d["diploma"] = hga == 39
    # PEINUSYR (ASEC 2025): 1 before 1950, 2 1950-59, 3 1960-64, 4 1965-69, 5 1970-74, 6 1975-79, then two-year
    # bands from 7 = 1980-81 to 27 = 2020-21, and 28 = 2022-2024 (repo note ledger_asec2026_2026_09_16/RESULT.md).
    code = d.PEINUSYR.to_numpy()
    mid = np.select([code == 1, code == 2, code == 3, code == 4, code == 5, code == 6, code == 28],
                    [1945, 1955, 1962, 1967, 1972, 1977, 2023], 1980.5 + 2 * (code - 7))
    d["arrival_age"] = np.where(code > 0, d.A_AGE - (2025 - mid), np.nan)
    return d


# ------------------------------------------------------------------ parents' schooling: IPUMS-CPS
def ipums_cat(educ):
    e = np.asarray(educ)
    return np.select([e == 0, e <= 2, (e >= 10) & (e <= 14), (e >= 20) & (e <= 32), (e >= 40) & (e <= 72),
                      (e >= 73) & (e <= 92), (e >= 100) & (e < 999)], [-1, 0, 1, 2, 3, 4, 5], -1)


def parents_schooling():
    gate("ipums_extract_hash", sha256(IPUMS) == IPUMS_SHA)
    cols = ["YEAR", "SERIAL", "PERNUM", "HFLAG", "ASECWT", "AGE", "SEX", "BPL", "MBPL", "FBPL", "NATIVITY", "EDUC",
            "NCHILD", "YNGCH"]
    d = pd.read_csv(IPUMS, usecols=cols)
    d = d[d.HFLAG.isna() | d.HFLAG.eq(0)]                 # 2014: keep the traditional-questionnaire 3/8 only
    kids = d[d.NATIVITY.isin([2, 3, 4]) & (d.FBPL.eq(20000) | d.MBPL.eq(20000)) & d.AGE.le(17)]
    par = d[d.BPL.eq(20000) & d.AGE.between(18, 75) & d.NCHILD.ge(1)][["YEAR", "SERIAL", "AGE", "SEX", "EDUC",
                                                                         "YNGCH"]]
    m = kids.merge(par, on=["YEAR", "SERIAL"], suffixes=("", "_p"))
    gap = m.AGE_p - m.AGE
    ok = (gap.between(14, 60) & (m.YNGCH_p <= m.AGE)
          & ((m.SEX_p.eq(1) & m.FBPL.eq(20000)) | (m.SEX_p.eq(2) & m.MBPL.eq(20000))))
    m = m[ok].copy()
    m["pcat"] = ipums_cat(m.EDUC_p)
    m = m[m.pcat >= 0]
    matched_w = m.drop_duplicates(["YEAR", "SERIAL", "PERNUM"]).ASECWT.sum()
    match_rate = matched_w / kids.ASECWT.sum()
    m["bin"] = parent_bin(m.YEAR - m.AGE)
    rows = []
    for f in DIPLOMA_REREAD:
        # Each parent's category CDF; a diploma is re-read as secundaria with probability f, independently.
        cdf = np.zeros((len(m), 6))
        for c in range(6):
            base = (m.pcat.to_numpy() <= c).astype(float)
            dip = m.EDUC_p.eq(73).to_numpy()
            cdf[:, c] = np.where(dip & (c == 3), f, base)
        # The more-schooled parent: P(max <= c) = product over matched parents.
        kid = pd.MultiIndex.from_frame(m[["YEAR", "SERIAL", "PERNUM"]])
        logc = pd.DataFrame(np.log(np.clip(cdf, 1e-300, None)), index=kid).groupby(level=[0, 1, 2]).sum()
        kcdf = np.exp(logc.to_numpy())
        kcdf[kcdf < 1e-200] = 0.0
        pmf = np.diff(np.hstack([np.zeros((len(kcdf), 1)), kcdf]), axis=1)
        first = m.drop_duplicates(["YEAR", "SERIAL", "PERNUM"]).set_index(["YEAR", "SERIAL", "PERNUM"])
        first = first.loc[logc.index]
        k = pd.DataFrame(pmf * first.ASECWT.to_numpy()[:, None], columns=range(6))
        k["bin"] = first.bin.to_numpy()
        k["n"] = 1
        g = k.groupby("bin").sum()
        for b, r in g.iterrows():
            tot = r[list(range(6))].sum()
            for c in range(6):
                rows.append(dict(diploma_reread=f, bin=b, parent_cat=c, parent_cat_name=CATS[c], share=r[c] / tot,
                                 children_n=int(r["n"])))
    out = pd.DataFrame(rows)
    gate("parents_shares_sum_to_one", np.allclose(out.groupby(["diploma_reread", "bin"]).share.sum(), 1.0))
    return out, float(match_rate)


# ------------------------------------------------------------------ Mexico side
def transitions():
    t = pd.read_csv(DERIVED / "mexico_transition.csv")
    out = {}
    levels = [("sex", "cohort"), ("cohort",), ()]
    for sex in ("male", "female"):
        for coh in ("1953-62", "1963-72", "1973-82", "1983-92"):
            for pc in range(6):
                for lev in levels:
                    s = t[t.parent_cat.eq(pc)]
                    if "sex" in lev:
                        s = s[s.sex.eq(sex)]
                    if "cohort" in lev:
                        s = s[s.cohort.eq(coh)]
                    if s.n.sum() >= MIN_N:
                        v = s.groupby("own_cat").w.sum()
                        out[(sex, coh, pc)] = (v.reindex(range(6), fill_value=0) / v.sum()).to_numpy()
                        break
                else:
                    raise SystemExit(f"[BLOCKED] no EMOVI cell with n >= {MIN_N} for parents {pc}")
    return out


# gross pay, pay as received, income tax and employee contributions withheld, consumption taxes (IVA and IEPS)
MONEY = ("inc", "net", "tax", "ctax")


def mexico_cells(ppp):
    """Lookup tables for one PPP ('gdp' or 'consumption'), keyed (sex, band, schooling) for adults and (sex,
    band, parents' schooling) for the young ('y' prefix): gross pay (ENIGH pay as received, formal jobs grossed
    up by the 2024 statutory withholding), pay as received, withheld tax, consumption taxes, employment and weekly
    hours."""
    cols = dict(inc=f"gross_per_person_ppp_{ppp}", net=f"income_per_person_ppp_{ppp}",
                tax=f"withheld_per_person_ppp_{ppp}", ctax=f"ctax_per_person_ppp_{ppp}", emp="employment_rate",
                hrs="weekly_hours_employed")
    c = pd.read_csv(DERIVED / "mexico_earnings_cells.csv")
    y = pd.read_csv(DERIVED / "mexico_young_by_parent.csv")
    out = {k: {(r.sex, r.band, r.cat): getattr(r, col) for r in c.itertuples()} for k, col in cols.items()}
    out.update({f"y{k}": {(r.sex, r.band, r.parent_cat): getattr(r, col) for r in y.itertuples()}
                for k, col in cols.items()})
    return out


def cell_or_neighbour(table, sex, band, cat):
    """A missing ENIGH cell (rare: 'none' among the young) takes the nearest schooling category's value."""
    for k in [cat, cat + 1, cat - 1, cat + 2, cat - 2]:
        if (sex, band, k) in table and np.isfinite(table[(sex, band, k)]):
            return table[(sex, band, k)]
    raise SystemExit(f"[BLOCKED] no ENIGH cell near {sex} {band} {cat}")


def mexico_rearing(people, parents, trans, cells, f, mishra):
    """Expected Mexico gross pay, pay as received, withheld tax, consumption taxes, employment ('emp') and weekly
    hours times employment ('hw') for each person under the rearing counterfactual; a dict of arrays."""
    pp = parents[parents.diploma_reread.eq(f)].pivot(index="bin", columns="parent_cat", values="share")
    key = pd.DataFrame({"sex": people.sex, "age": people.A_AGE, "by": people.birth_year})
    res = {}
    for (sex, age, by), _ in key.groupby(["sex", "age", "by"]):
        acc = dict.fromkeys(MONEY + ("emp", "hw"), 0.0)
        if age >= 15:
            ppar = pp.loc[parent_bin(by).item()].to_numpy()
            if age <= 24:
                yb = "15-19" if age <= 19 else "20-24"
                mix = [(ppar[pc], "y", yb, pc, MISHRA_AVG) for pc in range(6)]
            else:
                band, coh = band_of(age).item(), emovi_cohort(by).item()
                mix = [(ppar[pc] * trans[(sex, coh, pc)][oc], "", band, oc, MISHRA_X[oc])
                       for pc in range(6) for oc in range(6)]
            for p, pre, b, k, xm in mix:
                if p == 0:
                    continue
                x = 1 / (1 + xm) if mishra else 1.0
                for m in MONEY:
                    acc[m] += p * cell_or_neighbour(cells[pre + m], sex, b, k) * x
                er = cell_or_neighbour(cells[pre + "emp"], sex, b, k)
                acc["emp"] += p * er
                acc["hw"] += p * er * cell_or_neighbour(cells[pre + "hrs"], sex, b, k)
        res[(sex, age, by)] = acc
    keys = list(zip(key.sex, key.age, key.by))
    return {m: np.array([res[k][m] for k in keys]) for m in MONEY + ("emp", "hw")}


def mexico_own_schooling(people, cells, reread_f, mishra):
    """The same, priced at the person's own (US-observed) schooling; a diploma is secundaria with prob f."""
    out = {m: np.zeros(len(people)) for m in MONEY + ("emp", "hw")}
    for i, (sex, age, cat, dip) in enumerate(zip(people.sex, people.A_AGE, people.own_cat, people.diploma)):
        if age < 15 or cat < 0:
            continue
        band = band_of(age).item()
        mix = [(cat, 1.0)] if not (dip and reread_f > 0) else [(4, 1 - reread_f), (3, reread_f)]
        for c, p in mix:
            x = 1 / (1 + MISHRA_X[c]) if mishra else 1.0
            er = cell_or_neighbour(cells["emp"], sex, band, c)
            for m in MONEY:
                out[m][i] += p * cell_or_neighbour(cells[m], sex, band, c) * x
            out["emp"][i] += p * er
            out["hw"][i] += p * er * cell_or_neighbour(cells["hrs"], sex, band, c)
    return out


@np.errstate(invalid="ignore", divide="ignore")
def summarize(gen, convention, people, e, delta, extra):
    """e: the dict of per-person Mexico arrays. mexico_earnings_bn is gross pay; the premium is gross to gross."""
    w = people.pw.to_numpy()
    e_us = people.earn.to_numpy()
    works = people.works.to_numpy()
    hrs = people.HRSWK.to_numpy(float)
    wk = works & (hrs > 0)
    adult = people.A_AGE.to_numpy() >= 15
    E_US, E_MX = (w * e_us).sum(), (w * e["inc"] * (1 + delta)).sum()
    emp_mx, hw_mx = e["emp"], e["hw"]
    return dict(generation=gen, convention=convention, **extra, selection_delta=round(delta, 6),
                persons_m=w.sum() / 1e6, persons_15plus_m=w[adult].sum() / 1e6,
                us_earnings_bn=E_US / 1e9, mexico_earnings_bn=E_MX / 1e9, gain_bn=(E_US - E_MX) / 1e9,
                gain_per_person=(E_US - E_MX) / w.sum(), ratio_us_to_mexico=E_US / E_MX if E_MX > 0 else np.nan,
                mexico_take_home_bn=(w * e["net"] * (1 + delta)).sum() / 1e9,
                mexico_withheld_tax_bn=(w * e["tax"] * (1 + delta)).sum() / 1e9,
                mexico_consumption_tax_bn=(w * e["ctax"] * (1 + delta)).sum() / 1e9,
                employment_us_15plus=(w * works)[adult].sum() / w[adult].sum(),
                employment_mx_15plus=(w * emp_mx)[adult].sum() / w[adult].sum(),
                weekly_hours_us_workers=(w * hrs)[wk].sum() / w[wk].sum(),
                weekly_hours_mx_workers=((w * hw_mx)[adult].sum() / (w * emp_mx)[adult].sum()
                                         if (w * emp_mx)[adult].sum() > 0 else np.nan))


def main(basis="cps"):
    DERIVED.mkdir(exist_ok=True)
    d = load_asec(basis)
    parents, match_rate = parents_schooling()
    if basis == "cps":
        parents.to_csv(DERIVED / "parents_schooling.csv", index=False, lineterminator="\n", float_format="%.6g")
    trans = transitions()
    rows, by_age = [], []
    for ppp in ("gdp", "consumption"):
        cells = mexico_cells(ppp)
        # ---- G1: the direct 2024 check on CMP, observably identical (own schooling), ages 25-64
        g1 = d[d.gen.eq("G1")]
        for scope, sub in [("all_ages", g1), ("25_64", g1[g1.A_AGE.between(25, 64)]),
                           ("25_64_arrived_20plus", g1[g1.A_AGE.between(25, 64) & (g1.arrival_age >= 20)])]:
            for f in DIPLOMA_REREAD:
                for mishra in (False, True):
                    e = mexico_own_schooling(sub, cells, f, mishra)
                    for sel, delta in G1_SELECTION.items():
                        rows.append(summarize("G1", f"own_schooling_{scope}", sub, e, delta,
                                              dict(ppp=ppp, diploma_reread=f, mishra=mishra, selection=sel)))
        # ---- G2: rearing (central) and own US schooling (the premium's lower bound)
        g2 = d[d.gen.eq("G2")]
        for f in DIPLOMA_REREAD:
            for mishra in (False, True):
                e = mexico_rearing(g2, parents, trans, cells, f, mishra)
                for sel, delta in G2_INHERITED.items():
                    rows.append(summarize("G2", "rearing", g2, e, delta,
                                          dict(ppp=ppp, diploma_reread=f, mishra=mishra, selection=sel)))
                if ppp == "gdp" and f == 0.25 and not mishra:
                    tmp = g2.assign(**{f"mx_{m}": v for m, v in e.items()},
                                    band=np.where(g2.A_AGE < 15, "0-14", band_of(g2.A_AGE)))
                    for b, s in tmp.groupby("band"):
                        by_age.append(summarize("G2", "rearing", s, {m: s[f"mx_{m}"].to_numpy() for m in e}, 0.0,
                                                dict(band=b)))
                    # G2's Mexico-to-US ratios by sex x age band, for the G3+ upper bound
                    ratio = {m: {} for m in MONEY}
                    for (sx, b), s in tmp[tmp.A_AGE >= 15].groupby(["sex", "band"]):
                        for m in MONEY:
                            ratio[m][(sx, b)] = (s.pw * s[f"mx_{m}"]).sum() / max((s.pw * s.earn).sum(), 1.0)
        for mishra in (False, True):
            e = mexico_own_schooling(g2, cells, 0.0, mishra)
            for sel, delta in G2_INHERITED.items():
                rows.append(summarize("G2", "own_us_schooling", g2, e, delta,
                                      dict(ppp=ppp, diploma_reread=0.0, mishra=mishra, selection=sel)))
        # ---- G3+: bounds only. Lower: no premium. Upper: G2's rearing ratio by sex x age band applied.
        g3 = d[d.gen.eq("G3+")]
        if ppp == "gdp":
            e3 = {m: np.array([ratio[m].get((sx, b), np.nan) if a >= 15 else 0.0
                               for sx, b, a in zip(g3.sex, band_of(g3.A_AGE), g3.A_AGE)]) * g3.earn.to_numpy()
                  for m in MONEY}
            e3["emp"] = e3["hw"] = np.zeros(len(g3))
            rows.append(summarize("G3+", "bound_upper_g2_ratio", g3, e3, 0.0,
                                  dict(ppp=ppp, diploma_reread=0.25, mishra=False, selection="none")))
    out = pd.DataFrame(rows)
    out.to_csv(suffixed(DERIVED / "g2_premium.csv", basis), index=False, lineterminator="\n", float_format="%.6g")
    if basis == "cps":
        pd.DataFrame(by_age).to_csv(DERIVED / "g2_premium_by_age.csv", index=False, lineterminator="\n",
                                    float_format="%.6g")
    ages = d[d.gen.ne("")].groupby(["gen", "A_AGE"]).pw.sum().rename("persons").reset_index()
    ages.rename(columns={"gen": "generation", "A_AGE": "age"}).to_csv(
        suffixed(DERIVED / "group_ages.csv", basis), index=False, lineterminator="\n", float_format="%.6g")
    meta = dict(ipums_children_matched_share=match_rate,
                persons_m={g: float(d.pw[d.gen.eq(g)].sum() / 1e6) for g in ("G1", "G2", "G3+")})
    if basis != "cps":
        meta["basis"] = basis
    json.dump(meta, open(suffixed(DERIVED / "g2_meta.json", basis), "w"), indent=1, sort_keys=True)
    if basis == "cps":
        gate("g1_members", abs(meta["persons_m"]["G1"] - 12.22) < 0.05, got=meta["persons_m"]["G1"])
    else:
        # Row 4 removes Mexico-born union members only, so G1 falls by the union's fall and G2, G3+ keep theirs.
        pop = row4()["populations"]
        fall = float((d.pw_cps - d.pw)[d.gen.eq("G1")].sum())
        gate("row4_g1_falls_by_the_unions_fall", abs(fall - (pop["published"] - pop["row4"])) < 1e-3
             and float((d.pw_cps - d.pw)[d.gen.isin(["G2", "G3+"])].abs().sum()) == 0.0, g1_fall=fall,
             union_fall=pop["published"] - pop["row4"])
    gate("g2_members", abs(meta["persons_m"]["G2"] - 14.33) < 0.05, got=meta["persons_m"]["G2"])
    print(json.dumps(meta, indent=1), file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", default="cps", choices=BASES)
    main(ap.parse_args().basis)
