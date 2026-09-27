"""Mexican-origin non-identifiers in CPS ASEC: G2 adults, and an ancestry-defined G3 in one sample.

Two measurements the carry-over lane did not make:

1. Second generation, all adults 25-64. G2 is defined by a Mexico-born parent, so it already
   contains the adults who do not report Mexican origin. Split it into identifiers
   (PRDTHSP = 1) and non-identifiers, and measure the non-identifiers' advantage on schooling,
   earnings and the partial ledger for the same people.
2. Same-sample test. Among adults 18+ living with a linked biological parent, the parent's own
   record gives the grandparents' birthplaces. The third generation can then be defined by a
   Mexico-born grandparent whatever the person reports (G3anc), next to identifiers only
   (G3anc_id, which is the carry-over lane's G3_obs) and the second generation in the same frame.

Loaders, grandparent linkage, ledger, age x sex reweighting and statistics are imported read-only
from generation_carryover_2026_09_27/analyze_cps.py. The gap function below follows its gaps()
line for line, with extra groups and an optional second reference. Gate: every group the carry-over
lane published reproduces its gap and SE to 1e-9.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # imports from other lanes must not write their __pycache__

import argparse
import csv
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CARRY = FISCAL / "generation_carryover_2026_09_27"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


co = _load("carryover_cps", CARRY / "analyze_cps.py")
split = co.split
REPS = co.REPS

# A_HGA -> completed years, copied from mexican_origin_population_total_2026_09_19/
# bounds_coverage_fiscal.py (HGA_YEARS), the crosswalk behind the 1.049-year gap.
HGA_YEARS = {0: 0, 31: 0, 32: 2.5, 33: 5.5, 34: 7.5, 35: 9, 36: 10, 37: 11,
             38: 12, 39: 12, 40: 13, 41: 14, 42: 14, 43: 16, 44: 18, 45: 19, 46: 21}

MEASURES = dict(co.MEASURES)
MEASURES["educ_years"] = (lambda d: d.A_HGA.map(HGA_YEARS).astype(float), lambda d: d.A_AGE.ge(25), "mean", "years")

G2_GROUPS = ["G2", "G2_id", "G2_nonmex", "G2_nonhisp"]
G3_GROUPS = ["G3anc", "G3anc_id", "G3anc_nonmex", "G3anc_nonhisp"]
# G4 lineage as NLSY97 defines G4+: four US-born grandparents, and the person or a linked parent reports
# Mexican origin. It sees one step of loss (parent reports, adult child does not), never a parent's own.
G4_GROUPS = ["G4par", "G4par_id", "G4par_nonmex", "G4par_nonhisp"]
POP = G2_GROUPS + ["G3plus_all"]
FRAMES = {
    # frame: (description, groups, references)
    "pop": ("all civilian household adults 25-64", POP, ["white3plus"]),
    "pop_25_44": ("adults 25-44", POP, ["white3plus"]),
    "pop_45_64": ("adults 45-64", POP, ["white3plus"]),
    "pop_cohort": ("adults 25-64 born 1979-1985 (survey year minus age), the NLSY97 cohort +-1", POP, ["white3plus"]),
    "cores_one": ("adults 18+ co-resident with >=1 linked biological parent",
                  G2_GROUPS + G3_GROUPS + ["G3_obs", "G3plus_all"], ["white3plus", "white_clean"]),
    "cores_both": ("adults 18+ co-resident with both biological parents linked",
                   G2_GROUPS + G3_GROUPS + G4_GROUPS + ["G3_obs", "G4plus_obs", "G3plus_all"],
                   ["white3plus", "white_clean"]),
}
# Groups and frames the carry-over lane published: (my frame, my group) -> its generation label.
GATE = {("pop", "G2"): "G2", ("pop", "G3plus_all"): "G3plus_all",
        ("cores_one", "G2"): "G2", ("cores_one", "G3_obs"): "G3_obs", ("cores_one", "G3plus_all"): "G3plus_all",
        ("cores_both", "G2"): "G2", ("cores_both", "G3_obs"): "G3_obs", ("cores_both", "G4plus_obs"): "G4plus_obs",
        ("cores_both", "G3plus_all"): "G3plus_all"}
KEEP = ["year", "A_AGE", "A_SEX", "A_HGA", "PEMLR", "PEARNVAL", "earn24", "ledger24", "one", "both",
        "PRDTRACE", "PEHSPNON", "PRDTHSP", "n_mex_gp"]


def parent_mexican(d: pd.DataFrame, mex: np.ndarray) -> np.ndarray:
    """True when a linked co-resident biological parent reports Mexican origin (same linkage as
    co.grandparents: PEPAR1/PEPAR2 line numbers within the household, type 1 = biological)."""
    n = len(d)
    lookup = pd.Series(np.arange(n), index=pd.MultiIndex.from_frame(d[["PH_SEQ", "A_LINENO"]]))
    out = np.zeros(n, bool)
    for slot in (1, 2):
        line = d[f"PEPAR{slot}"].to_numpy()
        parent = lookup.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), line])).fillna(-1).to_numpy(int)
        bio = (line > 0) & (parent >= 0) & d[f"PEPAR{slot}TYP"].eq(1).to_numpy()
        out |= bio & mex[np.maximum(parent, 0)]
    return out


def groups(d: pd.DataFrame) -> dict:
    """The carry-over lane's groups plus identity splits of G2, an ancestry-defined G3 and a
    parent-identified G4."""
    g, one, both = co.groups(d)
    gp, _, consistent = co.grandparents(d)
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    parents_us = (d.PEMNTVTY.isin(co.US) & d.PEFNTVTY.isin(co.US)).to_numpy()
    hisp = d.PEHSPNON.eq(1).to_numpy()
    mex = hisp & d.PRDTHSP.eq(1).to_numpy()
    mex_gp = (gp == 303).any(axis=1)
    par_mex = parent_mexican(d, mex)
    g3anc = native & parents_us & civilian & consistent & mex_gp
    g4par = native & parents_us & civilian & consistent & np.isin(gp, co.US).all(axis=1) & (mex | par_mex)
    if not np.array_equal(g3anc & mex, g["G3_obs"]):
        raise ValueError("G3anc identifiers do not reproduce the carry-over lane's G3_obs")
    if not np.array_equal(g4par & mex, g["G4plus_obs"]):
        raise ValueError("G4par identifiers do not reproduce the carry-over lane's G4plus_obs")
    out = {**g, "one": one, "both": both,
           "G2_id": g["G2"] & mex, "G2_nonmex": g["G2"] & ~mex, "G2_nonhisp": g["G2"] & ~hisp,
           "G3anc": g3anc, "G3anc_id": g3anc & mex, "G3anc_nonmex": g3anc & ~mex, "G3anc_nonhisp": g3anc & ~hisp,
           "G4par": g4par, "G4par_id": g4par & mex, "G4par_nonmex": g4par & ~mex, "G4par_nonhisp": g4par & ~hisp,
           # Whites with an observed Mexico-born grandparent or a Mexican-identifying parent are attriters.
           "white_clean": g["white3plus"] & ~mex_gp & ~par_mex}
    return out


def build(years):
    cpi = pd.read_csv(co.CPI)
    cpi = cpi.set_index(cpi.columns[0]).iloc[:, 0]
    frames, audit = [], {}
    names = None
    for y in years:
        d = co.load_year(y)
        g = groups(d)
        names = [k for k in g if k not in ("one", "both")]
        d = pd.concat([d, pd.DataFrame(g, index=d.index)], axis=1)
        d["ledger_raw"] = co.ledger(d)
        f = cpi.loc[2024] / cpi.loc[y - 1]
        d["earn24"] = d.PEARNVAL * f
        d["ledger24"] = d.ledger_raw * f
        d["n_mex_gp"] = (co.grandparents(d)[0] == 303).sum(axis=1)  # observed Mexico-born grandparents
        audit[y] = dict(source=str(co.SOURCES[y][0]), sha256=co.sha(co.SOURCES[y][0]), rows=len(d), income_year=y - 1,
                        cpi_factor_to_2024=float(f))
        keep = d[names].any(axis=1) & d.A_AGE.ge(18)
        frames.append(d.loc[keep, KEEP + names + REPS].copy())
    return pd.concat(frames, ignore_index=True), audit, names


def frame_mask(p: pd.DataFrame, frame: str) -> np.ndarray:
    if frame == "pop":
        return p.A_AGE.between(25, 64).to_numpy()
    if frame == "pop_25_44":
        return p.A_AGE.between(25, 44).to_numpy()
    if frame == "pop_45_64":
        return p.A_AGE.between(45, 64).to_numpy()
    if frame == "pop_cohort":
        born = p.year - p.A_AGE
        return (p.A_AGE.between(25, 64) & born.between(1979, 1985)).to_numpy()
    return p.A_AGE.ge(18).to_numpy() & p[frame.replace("cores_", "")].to_numpy()


def sdr(v: np.ndarray) -> float:
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def gaps(p: pd.DataFrame, nyears: int, label: str):
    rows, reps = [], {}
    W = p[REPS].to_numpy(float) / nyears
    age, sex = p.A_AGE.to_numpy(), p.A_SEX.to_numpy()
    for frame, (desc, gens, refs) in FRAMES.items():
        fr = frame_mask(p, frame)
        cell_frame = "pop" if frame.startswith("pop") else frame
        for m, (fv, fvalid, kind, unit) in MEASURES.items():
            if frame.startswith("pop") and m in ("ba_plus_22plus", "less_than_hs_20plus"):
                continue
            x = fv(p).to_numpy(float)
            ok = fr & fvalid(p).to_numpy()
            for refname in refs:
                ref = ok & p[refname].to_numpy()
                cr = co.age_cells(age[ref], sex[ref], cell_frame)
                for gname in gens:
                    use = ok & p[gname].to_numpy()
                    if use.sum() == 0:
                        continue
                    cg = co.age_cells(age[use], sex[use], cell_frame)
                    wr, unc = co.reweight(cg, W[use], cr, W[ref])
                    sg = co.stat(kind, x[use], W[use])
                    sw = co.stat(kind, x[ref], wr)
                    scale = 100 if unit == "pct" else 1
                    gap = (sg - sw) * scale
                    reps[(label, frame, m, gname, refname)] = gap
                    reps[(label, frame, m, gname, "weight")] = W[use].sum(0)
                    rows.append(dict(source=label, frame=frame, frame_desc=desc, measure=m, unit=unit, generation=gname,
                                     reference=refname, n=int(use.sum()), n_ref=int(ref.sum()),
                                     weighted=float(W[use, 0].sum()),
                                     mean_age=float(np.average(age[use], weights=W[use, 0])),
                                     value=float(sg[0] * scale), se_value=sdr(sg * scale),
                                     ref_value_age_matched=float(sw[0] * scale), gap=float(gap[0]), se=sdr(gap),
                                     ref_cells_uncovered_share=unc))
    return rows, reps


def gate(rows, label):
    pub = pd.read_csv(CARRY / "derived" / f"cps_gaps_{label}.csv")
    got = pd.DataFrame(rows)
    checked = 0
    for (frame, grp), gen in GATE.items():
        a = got[got.frame.eq(frame) & got.generation.eq(grp) & got.reference.eq("white3plus")].set_index("measure")
        b = pub[pub.frame.eq(frame) & pub.generation.eq(gen)].set_index("measure")
        for m in b.index:
            if abs(a.gap[m] - b.gap[m]) > 1e-9 or abs(a.se[m] - b.se[m]) > 1e-9 or a.n[m] != b.n[m]:
                raise ValueError(f"[BLOCKED] gate: {frame} {grp} {m}: {a.gap[m]} vs {b.gap[m]}")
            checked += 1
    return checked


def contrasts(rows, reps, label):
    """Shares, non-identifier advantages and generation ratios, each with its SDR SE."""
    out = []

    def add(frame, measure, ref, name, v, note):
        v = np.asarray(v, float)
        out.append(dict(source=label, frame=frame, measure=measure, reference=ref, contrast=name,
                        value=float(v[0]), se=sdr(v), note=note))

    got = {(r["frame"], r["measure"], r["generation"], r["reference"]) for r in rows}
    for frame, (_, gens, refs) in FRAMES.items():
        for m in MEASURES:
            for ref in refs:
                def rep(g):
                    return reps.get((label, frame, m, g, ref))
                for base, parts in (("G2", ("G2_id", "G2_nonmex", "G2_nonhisp")),
                                    ("G3anc", ("G3anc_id", "G3anc_nonmex", "G3anc_nonhisp")),
                                    ("G4par", ("G4par_id", "G4par_nonmex", "G4par_nonhisp"))):
                    if (frame, m, base, ref) not in got:
                        continue
                    idg, nm, nh = parts
                    wa = reps[(label, frame, m, base, "weight")]
                    for nid, tag in ((nm, "not Mexican"), (nh, "not Hispanic")):
                        if (frame, m, nid, ref) not in got:
                            continue
                        wn = reps[(label, frame, m, nid, "weight")]
                        add(frame, m, ref, f"{base}: share {tag}", wn / wa, "weighted share of the lineage group")
                        add(frame, m, ref, f"{base}: advantage, {tag} minus identifiers", rep(nid) - rep(idg),
                            "gap(non-identifiers) - gap(identifiers); both age x sex matched to the reference")
                        add(frame, m, ref, f"{base}: closing share, {tag}", 1 - rep(nid) / rep(idg),
                            "share of the identifiers' gap that the non-identifiers close")
                    add(frame, m, ref, f"{base}: lineage minus identifiers", rep(base) - rep(idg),
                        "how much including non-identifiers moves the group's gap")
                pairs = [("G2", "G3plus_all", "rho G2 -> G3+ identifiers (published convention)"),
                         ("G2_id", "G3plus_all", "rho G2 identifiers -> G3+ identifiers")]
                if "G3anc" in gens:
                    pairs += [("G2", "G3anc", "rho G2 -> G3 ancestry (lineage on both sides)"),
                              ("G2", "G3anc_id", "rho G2 -> G3 identifiers (carry-over G3_obs convention)"),
                              ("G2_id", "G3anc_id", "rho G2 identifiers -> G3 identifiers")]
                if "G4par" in gens:
                    pairs += [("G3anc", "G4par", "rho G3 ancestry -> G4 parent-identified (lineage on both sides)"),
                              ("G3anc_id", "G4par_id", "rho G3 identifiers -> G4+ identifiers (carry-over convention)")]
                for a, b, name in pairs:
                    if (frame, m, a, ref) in got and (frame, m, b, ref) in got:
                        add(frame, m, ref, name, rep(b) / rep(a), "ratio of gaps; replicate SE")
                if "G3anc" in gens and (frame, m, "G3anc", ref) in got:
                    add(frame, m, ref, "attrition component: rho(lineage G3) - rho(identifier G3)",
                        rep("G3anc") / rep("G2") - rep("G3anc_id") / rep("G2"), "same sample, same G2 denominator")
    return out


def composition(p: pd.DataFrame, nyears: int, label: str):
    """Who the non-identifiers are: race, Hispanic origin and observed Mexico-born grandparents (full-sample weight)."""
    w0 = p["pwwgt0"].to_numpy(float) / nyears
    flags = {"white_only": p.PRDTRACE.eq(1), "black_only": p.PRDTRACE.eq(2), "other_race": ~p.PRDTRACE.isin([1, 2]),
             "hispanic_not_mexican": p.PEHSPNON.eq(1) & ~p.PRDTHSP.eq(1), "not_hispanic": p.PEHSPNON.eq(2),
             "one_mexico_born_grandparent": p.n_mex_gp.eq(1)}
    rows = []
    for frame, gens in (("pop", ["G2_id", "G2_nonmex"]), ("cores_one", ["G2_id", "G2_nonmex", "G3anc_id", "G3anc_nonmex"]),
                        ("cores_both", ["G3anc_id", "G3anc_nonmex", "G4par_id", "G4par_nonmex"])):
        fr = frame_mask(p, frame)
        for g in gens:
            use = fr & p[g].to_numpy()
            w = w0[use]
            row = dict(source=label, frame=frame, group=g, n=int(use.sum()), weighted=float(w.sum()),
                       mean_age=float(np.average(p.A_AGE.to_numpy()[use], weights=w)),
                       mean_mexico_born_grandparents=float(np.average(p.n_mex_gp.to_numpy()[use], weights=w)))
            row.update({k: float((w * v.to_numpy()[use]).sum() / w.sum()) for k, v in flags.items()})
            rows.append(row)
    return rows


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="2022,2023,2024,2025")
    ap.add_argument("--label", default="CPS_ASEC_2022_2025")
    a = ap.parse_args()
    DERIVED.mkdir(exist_ok=True)
    CACHE.mkdir(exist_ok=True)
    years = [int(y) for y in a.years.split(",")]
    p, audit, _ = build(years)
    rows, reps = gaps(p, len(years), a.label)
    checked = gate(rows, a.label)
    print(f"gate: {checked} published gap/SE/n cells reproduced to 1e-9", flush=True)
    con = contrasts(rows, reps, a.label)
    write(rows, DERIVED / f"cps_identity_gaps_{a.label}.csv")
    write(con, DERIVED / f"cps_identity_contrasts_{a.label}.csv")
    write(composition(p, len(years), a.label), DERIVED / f"cps_identity_composition_{a.label}.csv")
    np.savez_compressed(CACHE / f"reps_{a.label}.npz", **{"|".join(k): v for k, v in reps.items()})
    (DERIVED / f"cps_identity_audit_{a.label}.json").write_text(json.dumps(dict(
        gate_cells_reproduced=checked, years=audit,
        pooling="weights/len(years); common replicate index; adjacent ASECs share households, so n counts person-years"),
        indent=1, sort_keys=True) + "\n")
    pd.set_option("display.width", 250)
    c = pd.DataFrame(con)
    show = c[c.reference.eq("white3plus") & c.measure.isin(["ba_plus", "educ_years", "earnings_worker_mean",
                                                            "ledger_partial_per_adult", "ba_plus_22plus"])]
    print(show[["frame", "measure", "contrast", "value", "se"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
