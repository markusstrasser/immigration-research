"""Closing share c of Mexican-origin G3 non-identifiers, pooled IPUMS-CPS ASEC 1994-2026.

Port of carryover_identity_2026_09_27/cps_identity.py Design 1 (co-resident parent pointers) to the
IPUMS extract staged by extract.py. Adults 18+ living with a linked parent; the parent's own MBPL/FBPL
gives the grandparents' birthplaces. G3 lineage (G3anc) = native-born, both own parents US-born,
civilian, every linked parent US-born, and at least one Mexico-born grandparent observed, whatever
the adult reports. Identifiers report a Mexican HISPAN code; non-identifiers do not. Gaps are group
minus third-plus non-Hispanic whites (native, both parents US-born, white only, civilian) in the same
frame, the whites reweighted to the group's age x sex cells (the carry-over lane's age_cells and
reweight, imported read-only). c = 1 - gap(non-identifiers) / gap(identifiers).

Differences from the Census-file design, all forced by IPUMS:
- IPUMS parent pointers (MOMLOC/POPLOC/MOMLOC2/POPLOC2) are constructed by IPUMS from RELATE in every
  year (2016 revision; cps.ipums.org MOMRULE page) and include step and adoptive parents. The Census
  design uses PEPAR1/PEPAR2 with type 1 (biological). The `direct` variant keeps only rule-11 links
  (direct relationship, unique), the IPUMS analogue of an unambiguous pointer.
- Earnings are INCWAGE (wage and salary) for workers with INCWAGE > 0; the Census design used PEARNVAL.
- No replicate weights in the extract: SEs are a cluster bootstrap. Cluster = CPSID (the household
  across its two ASEC years), stratum = the cluster's first ASEC year; B draws with replacement of
  clusters within stratum, among the clusters holding analysis rows.
- 2014 ASEC: the 3/8 and 5/8 files each sum to the population (ASECWT comparability note), so 2014
  weights are halved; other years enter at ASECWT as the carry-over lane's weight/len(years).
- HISPAN 901/902 (pre-2003 "do not know"/"no response") have unknown identity; they are kept out of
  the G3 lineage and of the white reference.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/g3_identity_pooled_2026_10_05/analyze.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # imports from other lanes must not write their __pycache__

import csv
import hashlib
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
DATA = CACHE / "asec_pooled.csv.gz"
CPI = FISCAL / "ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv"  # BLS CUUR0000SA0 annual average
PUB = FISCAL / "carryover_identity_2026_09_27/derived"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


co = _load("carryover_cps", FISCAL / "generation_carryover_2026_09_27/analyze_cps.py")

B = 400
SEED = 20261005
MEX_HISPAN = [100, 102, 103, 104, 108, 109]
UNKNOWN_HISPAN = [901, 902]
MEXICO = 20000
US_MAX = 15000  # IPUMS BPL: 09900 United States, 10000-12090 US territories; 15000+ abroad
PARENT_LINKS = [("MOMLOC", "MOMRULE"), ("POPLOC", "POPRULE"), ("MOMLOC2", None), ("POPLOC2", None)]
# IPUMS EDUC -> completed years, aligned with the Census A_HGA crosswalk in cps_identity.py (HGA_YEARS).
EDUC_YEARS = {2: 0, 10: 2.5, 20: 5.5, 30: 7.5, 40: 9, 50: 10, 60: 11, 71: 12, 73: 12, 81: 13, 91: 14, 92: 14,
              111: 16, 123: 18, 124: 19, 125: 21}
COLS = ["YEAR", "SERIAL", "CPSID", "CPSIDP", "HFLAG", "PERNUM", "ASECWT", "AGE", "SEX", "RACE", "HISPAN",
        "BPL", "MBPL", "FBPL", "NATIVITY", "EMPSTAT", "EDUC", "INCWAGE"] + [c for pair in PARENT_LINKS for c in pair if c]

GROUPS = ["G2", "G2_id", "G3anc", "G3anc_id", "G3anc_nonmex", "G3anc_nonhisp"]
FRAMES = {"cores_one": "adults 18+ co-resident with >=1 linked parent",
          "cores_both": "adults 18+ co-resident with two linked parents",
          # One linked parent: no spouse-of-parent link, the main route by which IPUMS adds a step-parent.
          "cores_single": "adults 18+ co-resident with exactly one linked parent"}
MEASURES = {  # name: (value fn, validity fn, unit)
    "ba_plus": (lambda d: d.EDUC.ge(111).astype(float), lambda d: d.AGE.ge(25), "pct"),
    "ba_plus_22plus": (lambda d: d.EDUC.ge(111).astype(float), lambda d: d.AGE.ge(22), "pct"),
    "educ_years": (lambda d: d.EDUC.map(EDUC_YEARS).astype(float), lambda d: d.AGE.ge(25), "years"),
    "employed": (lambda d: d.EMPSTAT.isin([10, 12]).astype(float), lambda d: d.AGE.ge(18), "pct"),
    "earnings_worker_mean": (lambda d: d.wage24, lambda d: d.INCWAGE.gt(0) & d.INCWAGE.lt(99999998), "usd2024"),
}
PERIODS = {"1994_2006": (1994, 2006), "2007_2021": (2007, 2021), "2022_2026": (2022, 2026),
           "1994_2002": (1994, 2002), "2003_2026": (2003, 2026)}
RHO_BA, RHO_BA_SE, A_BA = 0.921, 0.039, 0.112  # carryover_identity RESULT §1, BA+ published ratio and G3 hidden share


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load() -> pd.DataFrame:
    d = pd.read_csv(DATA, usecols=COLS)
    if d.duplicated(["YEAR", "SERIAL", "PERNUM"]).any():
        raise ValueError("duplicate person key")
    bad = d.AGE.ge(25) & ~d.EDUC.isin(EDUC_YEARS)
    if bad.any():
        raise ValueError(f"unmapped EDUC codes at 25+: {sorted(d.EDUC[bad].unique())}")
    return d


def classify(d: pd.DataFrame, direct_only: bool) -> dict:
    """Groups and frames for every person; parents linked within (YEAR, SERIAL) by PERNUM."""
    n = len(d)
    key = (d.YEAR.to_numpy(np.int64) * 100_000 + d.SERIAL.to_numpy(np.int64)) * 100 + d.PERNUM.to_numpy(np.int64)
    order = np.argsort(key)
    skey = key[order]
    hh = key - d.PERNUM.to_numpy(np.int64)
    bpl, mbpl, fbpl = d.BPL.to_numpy(), d.MBPL.to_numpy(), d.FBPL.to_numpy()
    is_us = lambda b: b < US_MAX
    gp = np.full((n, 8), np.nan)
    nlink = np.zeros(n, int)
    consistent = np.ones(n, bool)
    for j, (loc, rule) in enumerate(PARENT_LINKS):
        line = d[loc].to_numpy(np.int64)
        has = line > 0
        if direct_only:
            has &= d[rule].eq(11).to_numpy() if rule else False
        pos = np.searchsorted(skey, hh + line)
        pos = np.minimum(pos, n - 1)
        found = has & (skey[pos] == hh + line)
        if np.any(has & ~found):
            raise ValueError(f"{loc}: pointer to a missing person")
        p = order[pos]
        if np.any(found & (p == np.arange(n))):
            raise ValueError(f"{loc}: self link")
        nlink += found
        pb = bpl[p]
        consistent &= ~found | is_us(pb)
        usable = found & is_us(pb)
        gp[usable, 2 * j] = mbpl[p[usable]]
        gp[usable, 2 * j + 1] = fbpl[p[usable]]
    if nlink.max() > 2:
        raise ValueError("more than two linked parents")
    native = d.NATIVITY.between(1, 4).to_numpy()
    civilian = ~d.EMPSTAT.eq(1).to_numpy()
    parents_us = (is_us(d.MBPL) & is_us(d.FBPL)).to_numpy()
    hisp_code = d.HISPAN.to_numpy()
    known = ~np.isin(hisp_code, UNKNOWN_HISPAN)
    mex = np.isin(hisp_code, MEX_HISPAN)
    hisp = known & (hisp_code > 0)
    mex_gp = (gp == MEXICO).any(axis=1)
    all_gp = (~np.isnan(gp)).sum(axis=1) == 4
    g2 = native & civilian & ((d.MBPL == MEXICO) | (d.FBPL == MEXICO)).to_numpy() & known
    g3 = native & parents_us & civilian & consistent & mex_gp & known
    white = native & parents_us & civilian & (hisp_code == 0) & (d.RACE == 100).to_numpy()
    ok = consistent | ~parents_us
    return {"G2": g2, "G2_id": g2 & mex, "G3anc": g3, "G3anc_id": g3 & mex, "G3anc_nonmex": g3 & ~mex,
            "G3anc_nonhisp": g3 & ~hisp, "white3plus": white,
            "one": (nlink >= 1) & ok, "single": (nlink == 1) & ok, "both": (nlink == 2) & ok & (all_gp | ~parents_us),
            "n_mex_gp": (gp == MEXICO).sum(axis=1)}


def build(d: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    cpi = pd.read_csv(CPI).set_index("year").cpi_u
    out, audit = {}, {}
    keep = np.zeros(len(d), bool)
    for variant, direct in (("all", False), ("direct", True)):
        g = classify(d, direct)
        for k, v in g.items():
            out[f"{variant}:{k}"] = v
        keep |= g["one"] & np.logical_or.reduce([g[k] for k in GROUPS + ["white3plus"]])
    keep &= d.AGE.ge(18).to_numpy()
    p = d.loc[keep].copy()
    for k, v in out.items():
        p[k] = v[keep]
    p["w"] = p.ASECWT * np.where(p.YEAR.eq(2014), 0.5, 1.0)
    p["wage24"] = p.INCWAGE * (cpi.loc[2024] / p.YEAR.sub(1).map(cpi)).to_numpy()
    if p.wage24[p.INCWAGE.between(1, 99999997)].isna().any():
        raise ValueError("CPI year missing")
    audit["rows_extract"] = len(d)
    audit["rows_analysis"] = len(p)
    return p.reset_index(drop=True), audit


def replicate_counts(p: pd.DataFrame) -> np.ndarray:
    """Cluster multiplicities [n, B+1]: column 0 is the full sample; clusters are CPSID households,
    stratified by their first ASEC year in the analysis rows."""
    cl = pd.factorize(p.CPSID.where(p.CPSID.gt(0), -(p.YEAR * 100_000 + p.SERIAL)))[0]
    first = pd.Series(p.YEAR.to_numpy()).groupby(cl).min().to_numpy()
    rng = np.random.Generator(np.random.PCG64(SEED))
    mult = np.ones((cl.max() + 1, B + 1), np.float32)
    for y in np.unique(first):
        ids = np.flatnonzero(first == y)
        for b in range(1, B + 1):
            mult[ids, b] = np.bincount(rng.integers(0, len(ids), len(ids)), minlength=len(ids))
    return mult[cl]


def reweight(cg, wg, cr, wr):
    """co.reweight, vectorised over replicate columns: reference rows scaled to the group's cell mix."""
    k = int(max(cg.max(), cr.max())) + 1
    sg = np.stack([wg[cg == c].sum(0) for c in range(k)])
    sr = np.stack([wr[cr == c].sum(0) for c in range(k)])
    f = np.divide(sg / sg.sum(0), sr, out=np.zeros_like(sr), where=sr > 0)
    return wr * f[cr]


def mean(x, w):
    return (x[:, None] * w).sum(0) / w.sum(0)


def gaps(p, W, rows_mask, variant, label):
    rows, reps = [], {}
    age, sex = p.AGE.to_numpy(), p.SEX.to_numpy()
    for frame, desc in FRAMES.items():
        fr = rows_mask & p[f"{variant}:{frame.replace('cores_', '')}"].to_numpy()
        for m, (fv, fvalid, unit) in MEASURES.items():
            x = fv(p).to_numpy(float)
            ok = fr & fvalid(p).to_numpy()
            ref = ok & p[f"{variant}:white3plus"].to_numpy()
            cr = co.age_cells(age[ref], sex[ref], frame)
            scale = 100 if unit == "pct" else 1
            for g in GROUPS:
                use = ok & p[f"{variant}:{g}"].to_numpy()
                if use.sum() < 2:
                    continue
                cg = co.age_cells(age[use], sex[use], frame)
                wr = reweight(cg, W[use], cr, W[ref])
                sg, sw = mean(x[use], W[use]), mean(x[ref], wr)
                gap = (sg - sw) * scale
                reps[(frame, m, g)] = gap
                reps[(frame, m, g, "weight")] = W[use].sum(0)
                rows.append(dict(label=label, links=variant, frame=frame, measure=m, unit=unit, group=g,
                                 n=int(use.sum()), n_ref=int(ref.sum()), weighted=float(W[use, 0].sum()),
                                 mean_age=float(np.average(age[use], weights=W[use, 0])),
                                 value=float(sg[0] * scale), ref_value_age_matched=float(sw[0] * scale),
                                 gap=float(gap[0]), se=float(np.std(gap[1:], ddof=1))))
    return rows, reps


def contrasts(reps, variant, label):
    out = []
    for frame in FRAMES:
        for m in MEASURES:
            def add(name, v, note):
                v = np.asarray(v, float)
                bs = v[1:][np.isfinite(v[1:])]
                out.append(dict(label=label, links=variant, frame=frame, measure=m, contrast=name, value=float(v[0]),
                                se=float(np.std(bs, ddof=1)), p05=float(np.percentile(bs, 5)),
                                p95=float(np.percentile(bs, 95)), note=note))
            r = lambda g: reps.get((frame, m, g))
            if r("G3anc") is None or r("G3anc_id") is None:
                continue
            wa = reps[(frame, m, "G3anc", "weight")]
            for nid, tag in (("G3anc_nonmex", "not Mexican"), ("G3anc_nonhisp", "not Hispanic")):
                if r(nid) is None:
                    continue
                add(f"G3anc: share {tag}", reps[(frame, m, nid, "weight")] / wa, "weighted share of the G3 lineage")
                add(f"G3anc: advantage, {tag} minus identifiers", r(nid) - r("G3anc_id"), "gap difference")
                add(f"G3anc: closing share, {tag}", 1 - r(nid) / r("G3anc_id"),
                    "c = 1 - gap(non-identifiers)/gap(identifiers)")
            add("G3anc: lineage minus identifiers", r("G3anc") - r("G3anc_id"), "how much non-identifiers move the G3 gap")
            if r("G2") is not None:
                add("rho G2 -> G3 lineage", r("G3anc") / r("G2"), "same frame")
                add("rho G2 -> G3 identifiers", r("G3anc_id") / r("G2"), "same frame")
    return out


def dedupe(p: pd.DataFrame) -> np.ndarray:
    """Keep each CPSIDP's first ASEC year among analysis rows."""
    return ~(p.CPSIDP.gt(0) & p.sort_values("YEAR").duplicated("CPSIDP").sort_index()).to_numpy()


def flux(p: pd.DataFrame) -> list[dict]:
    """Identity reporting across a person's two ASEC years (CPSIDP linked), G3 lineage and G2."""
    out = []
    for g in ("G3anc", "G2"):
        q = p[p[f"all:{g}"] & p.CPSIDP.gt(0)]
        two = q[q.duplicated("CPSIDP", keep=False)].sort_values(["CPSIDP", "YEAR"])
        mex = two.HISPAN.isin(MEX_HISPAN).groupby(two.CPSIDP)
        first, last = mex.first(), mex.last()
        n = len(first)
        out.append(dict(group=g, persons_seen_twice=n, mexican_both=int((first & last).sum()),
                        not_mexican_both=int((~first & ~last).sum()), switched=int((first != last).sum()),
                        share_switched=float((first != last).mean()) if n else float("nan"),
                        not_mexican_either_year_who_switch=float((first != last).sum() / max((~first | ~last).sum(), 1))))
    return out


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def gate(rows):
    """2022-25 Census-file cells (cps_identity.py, white3plus reference) beside this port's."""
    pub = pd.read_csv(PUB / "cps_identity_gaps_CPS_ASEC_2022_2025.csv")
    pub = pub[pub.reference.eq("white3plus")]
    got = pd.DataFrame(rows)
    got = got[got.label.eq("gate_2022_2025") & got.links.eq("all")]
    out = []
    for frame in FRAMES:
        for m in ["ba_plus", "educ_years", "employed", "earnings_worker_mean"]:
            for g in GROUPS:
                a = got[got.frame.eq(frame) & got.measure.eq(m) & got.group.eq(g)]
                b = pub[pub.frame.eq(frame) & pub.measure.eq(m) & pub.generation.eq(g)]
                if a.empty or b.empty:
                    continue
                a, b = a.iloc[0], b.iloc[0]
                out.append(dict(frame=frame, measure=m, group=g, n_census=int(b.n), n_ipums=int(a.n),
                                n_ratio=a.n / b.n, gap_census=b.gap, se_census=b.se, gap_ipums=a.gap, se_ipums=a.se,
                                value_census=b.value, value_ipums=a.value))
    return out


def main():
    DERIVED.mkdir(exist_ok=True)
    d = load()
    p, audit = build(d)
    del d
    W_all = p.w.to_numpy(np.float64)[:, None] * replicate_counts(p)
    keep_first = dedupe(p)
    yr = p.YEAR.to_numpy()
    runs = [("pooled_1994_2026_dedup", keep_first, ["all", "direct"]),
            ("pooled_1994_2026_nodedup", np.ones(len(p), bool), ["all", "direct"]),
            ("gate_2022_2025", (yr >= 2022) & (yr <= 2025), ["all"]),
            ("gate_2022_2026", yr >= 2022, ["all"])]
    runs += [(f"period_{k}_dedup", keep_first & (yr >= a) & (yr <= b), ["all"]) for k, (a, b) in PERIODS.items()]
    all_rows, all_con, closing = [], [], {}
    for label, mask, variants in runs:
        for v in variants:
            rows, reps = gaps(p, W_all, mask, v, label)
            all_rows += rows
            all_con += contrasts(reps, v, label)
            closing[(label, v)] = 1 - reps[("cores_one", "ba_plus", "G3anc_nonmex")] / reps[("cores_one", "ba_plus", "G3anc_id")]
            print(f"  ✓ {label} {v}", flush=True)
    # Period heterogeneity of c (BA+, cores_one): difference across the same bootstrap draws.
    tests = []
    for a, b in (("1994_2006", "2007_2021"), ("2007_2021", "2022_2026"), ("1994_2006", "2022_2026"),
                 ("1994_2002", "2003_2026")):
        diff = closing[(f"period_{a}_dedup", "all")] - closing[(f"period_{b}_dedup", "all")]
        se = float(np.std(diff[1:], ddof=1))
        tests.append(dict(period_a=a, period_b=b, c_a=float(closing[(f"period_{a}_dedup", "all")][0]),
                          c_b=float(closing[(f"period_{b}_dedup", "all")][0]), diff=float(diff[0]), se=se,
                          z=float(diff[0] / se), share_draws_below_zero=float((diff[1:] < 0).mean())))
    write(tests, DERIVED / "period_tests.csv")
    write(all_rows, DERIVED / "gaps.csv")
    write(all_con, DERIVED / "contrasts.csv")
    write(gate(all_rows), DERIVED / "gate_2022_2025.csv")
    write(flux(p), DERIVED / "identity_flux.csv")

    # Counts of G3 lineage and non-identifiers by period, frame cores_one.
    counts = []
    for label, (a, b) in {"1994_2026": (1994, 2026), **PERIODS}.items():
        for dd, m0 in (("dedup", keep_first), ("nodedup", np.ones(len(p), bool))):
            m = m0 & (yr >= a) & (yr <= b) & p["all:one"].to_numpy()
            for age_lo in (18, 25):
                ma = m & p.AGE.ge(age_lo).to_numpy()
                counts.append(dict(period=label, dedupe=dd, min_age=age_lo,
                                   **{g: int((ma & p[f"all:{g}"].to_numpy()).sum()) for g in
                                      ["G3anc", "G3anc_id", "G3anc_nonmex", "G3anc_nonhisp", "white3plus"]},
                                   direct_G3anc_nonmex=int((m0 & (yr >= a) & (yr <= b) & p["direct:one"].to_numpy()
                                                            & p.AGE.ge(age_lo).to_numpy()
                                                            & p["direct:G3anc_nonmex"].to_numpy()).sum())))
    write(counts, DERIVED / "counts.csv")

    # Corrected step, rho* = rho (1 - a c), BA+ (carryover_identity RESULT §1).
    con = pd.DataFrame(all_con)
    step = []
    for label in con.label.unique():
        for v in con[con.label.eq(label)].links.unique():
            s = con[con.label.eq(label) & con.links.eq(v) & con.frame.eq("cores_one") & con.measure.eq("ba_plus")
                    & con.contrast.eq("G3anc: closing share, not Mexican")]
            if s.empty:
                continue
            c, se = s.value.iloc[0], s.se.iloc[0]
            rho = RHO_BA * (1 - A_BA * c)
            se_rho = float(np.hypot((1 - A_BA * c) * RHO_BA_SE, RHO_BA * A_BA * se))
            step.append(dict(label=label, links=v, c=c, se_c=se, rho=RHO_BA, a=A_BA, rho_star=rho, se_rho_star=se_rho,
                             note="SE: delta method, rho and c independent"))
    write(step, DERIVED / "corrected_step.csv")

    dropped = int((~keep_first).sum())
    audit.update(source=str(DATA.relative_to(FISCAL.parents[1])), sha256=sha(DATA), bootstrap_reps=B, seed=SEED,
                 bootstrap="cluster = CPSID household (both ASEC years), stratum = first year; clusters with analysis rows",
                 dedupe_rows_dropped=dropped,
                 dedupe_g3anc_dropped=int((~keep_first & p["all:G3anc"].to_numpy()).sum()),
                 weights="ASECWT; 2014 halved (3/8 and 5/8 files each sum to the population)",
                 cpi=str(CPI.relative_to(FISCAL.parents[1])))
    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=1, sort_keys=True) + "\n")
    pd.set_option("display.width", 250)
    print(pd.DataFrame(step).round(3).to_string(index=False))
    print(pd.DataFrame(counts).to_string(index=False))


if __name__ == "__main__":
    main()
