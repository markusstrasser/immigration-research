"""Mexican-origin outcome gaps by generation, CPS ASEC 2022-2025 pooled.

Reuses the generation_split_2026_09_20 masks and grandparent classifier (imported, not copied)
and the September 5 ledger's partial tax-minus-transfer construction (SPM-unit totals shared
equally among adults). Gaps are group mean minus third-plus non-Hispanic white mean after the
whites are reweighted to the group's age x sex mix within the same frame. SEs use the published
160 SDR replicates, 4/160, pooled with a common replicate index across years.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


split = _load("gen_split_cps", FISCAL / "generation_split_2026_09_20/analyze_cps.py")

SOURCES = {
    2022: (FISCAL / "latam_comparison_2026_09_17/_cache/2022/asecpub22csv.zip", "22"),
    2023: (FISCAL / "latam_comparison_2026_09_17/_cache/2023/asecpub23csv.zip", "23"),
    2024: (FISCAL / "same_year_tax_2026_09_20/_cache/asecpub24csv.zip", "24"),
    2025: (split.RAW, "25"),
    2026: (FISCAL / "ledger_asec2026_2026_09_16/_cache/asecpub26csv.zip", "26"),
}
CPI = FISCAL / "ncvs_victim_offender_2026_09_18/derived/cpi_u_annual.csv"
REPS = [f"pwwgt{i}" for i in range(161)]
US = split.US
TAXES = ["FICA", "FEDTAX_AC", "STATETAX_A"]
CASH = ["SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL", "VET_VAL"]
NONCASH = ["SPM_SNAPSUB", "SPM_ENGVAL", "SPM_WICVAL", "SPM_SCHLUNCH", "SPM_BBSUBVAL"]
EXTRA = ["A_SEX", "A_HGA", "PEMLR", "PEARNVAL", "PEHSPNON", "PRDTRACE", "SPM_ID",
         "FEDTAX_BC", "ACTC_CRD", "EIT_CRED"] + TAXES + CASH + NONCASH


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def load_year(year: int) -> pd.DataFrame:
    path, yy = SOURCES[year]
    with zipfile.ZipFile(path) as z:
        header = pd.read_csv(z.open(f"pppub{yy}.csv"), nrows=0).columns
        # The broadband subsidy (ACP) ended in June 2024; ASEC 2026 drops the field. Only it may be absent.
        absent = [c for c in EXTRA if c not in header]
        if set(absent) - {"SPM_BBSUBVAL"}:
            raise ValueError(f"{year}: missing fields {absent}")
        d = pd.read_csv(z.open(f"pppub{yy}.csv"), usecols=list(dict.fromkeys(split.COLS + [c for c in EXTRA if c in header])))
        for c in absent:
            d[c] = 0
        w = pd.read_csv(z.open(f"asec_csv_repwgt_20{yy}.csv"), usecols=["h_seq", "PPPOS"] + REPS)
        h = pd.read_csv(z.open(f"hhpub{yy}.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
    w = w.rename(columns={"h_seq": "PH_SEQ"})
    n = len(d)
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one")
    if len(d) != n:
        raise ValueError(f"{year}: person-weight merge lost rows")
    d = d.merge(h, on="PH_SEQ", how="left", validate="many_to_one")
    if d.GESTFIPS.isna().any():
        raise ValueError(f"{year}: person without household state")
    np.testing.assert_allclose(d.MARSUPWT / 100, d.pwwgt0, rtol=0, atol=.011)
    split.validate_weights(d[REPS].to_numpy(float))
    if d[EXTRA].isna().any().any():
        raise ValueError(f"{year}: missing outcome field")
    d = d.copy()
    d["year"] = year
    return d


def grandparents(d: pd.DataFrame):
    """Grandparent birthplaces through linked co-resident biological parents (any person).

    Same linkage as split.classify (reported arm); returns (gp[n,4], n_bio_parents, consistent).
    """
    n = len(d)
    lookup = pd.Series(np.arange(n), index=pd.MultiIndex.from_frame(d[["PH_SEQ", "A_LINENO"]]))
    gp = np.full((n, 4), np.nan)
    nbio = np.zeros(n, int)
    consistent = np.ones(n, bool)
    for slot in (1, 2):
        line = d[f"PEPAR{slot}"].to_numpy()
        parent = lookup.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), line])).fillna(-1).to_numpy(int)
        linked = (line > 0) & (parent >= 0)
        bio = linked & d[f"PEPAR{slot}TYP"].eq(1).to_numpy()
        p = np.maximum(parent, 0)
        pb = d.PENATVTY.to_numpy()[p]
        consistent &= ~bio | np.isin(pb, US)
        usable = bio & np.isin(pb, US)
        nbio += bio
        for j, field in enumerate(["PEMNTVTY", "PEFNTVTY"]):
            gp[usable, 2 * (slot - 1) + j] = d[field].to_numpy()[p[usable]]
    return gp, nbio, consistent


def groups(d: pd.DataFrame):
    base = split.population_masks(d)
    cls = split.classify(d)
    gp, nbio, consistent = grandparents(d)
    # Gate: the generic linkage reproduces the imported classifier exactly.
    g3 = base["G3plus"] & consistent & (gp == 303).any(axis=1)
    g4 = base["G3plus"] & consistent & np.isin(gp, US).all(axis=1)
    if not (np.array_equal(g3, cls["G3_Mexico_GP_observed"]) and np.array_equal(g4, cls["G4plus_all_US_GP_observed"])):
        raise ValueError("Generic grandparent linkage does not reproduce generation_split classifier")
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    parents_us = (d.PEMNTVTY.isin(US) & d.PEFNTVTY.isin(US)).to_numpy()
    white = native & parents_us & d.PEHSPNON.eq(2).to_numpy() & d.PRDTRACE.eq(1).to_numpy() & civilian
    all4 = (~np.isnan(gp)).all(axis=1)
    g = {"G1": base["G1"], "G2": base["G2"], "G3plus_all": base["G3plus"],
         "G3_obs": cls["G3_Mexico_GP_observed"], "G4plus_obs": cls["G4plus_all_US_GP_observed"],
         "G3plus_unresolved": cls["G3plus_unresolved"], "white3plus": white}
    # Frames: co-resident with >=1 linked biological parent (US-born if the person is G3+),
    # and with both biological parents linked (all four grandparents observed).
    # The US-born-parent consistency and four-grandparent rules apply to people whose
    # reported parents are US-born (G3+, whites); a G2 person needs only the co-resident parents.
    ok = consistent | ~parents_us
    one = (nbio >= 1) & ok
    both = (nbio == 2) & ok & (all4 | ~parents_us)
    return g, one, both


def ledger(d: pd.DataFrame) -> np.ndarray:
    """Partial ledger per person: SPM-unit (payroll+federal after refundable+state) minus
    (SS, SSI, TANF/GA, UI, veterans) minus (SNAP, energy, WIC, school lunch, broadband),
    shared equally among the unit's adults 18+ (children only in child-only units)."""
    unit = pd.factorize(d.SPM_ID.astype(str) + "_" + d.year.astype(str))[0]
    tax = d[TAXES].sum(axis=1).to_numpy(float)
    cash = d[CASH].sum(axis=1).to_numpy(float)
    tot = np.bincount(unit, weights=tax - cash)
    noncash = d.groupby(unit)[NONCASH].first().sum(axis=1).to_numpy(float)
    if d.groupby(unit)[NONCASH].nunique().gt(1).any().any():
        raise ValueError("SPM noncash fields vary within unit")
    tot = tot - noncash
    adult = d.A_AGE.ge(18).to_numpy()
    nad = np.bincount(unit, weights=adult)
    elig = adult | (nad[unit] == 0)
    cnt = np.bincount(unit, weights=elig)
    out = np.where(elig, tot[unit] / cnt[unit], 0.0)
    if not np.allclose(np.bincount(unit, weights=out), tot):
        raise ValueError("Ledger allocation does not conserve unit totals")
    return out


def wmedian(x, w):
    o = np.argsort(x)
    x, w = x[o], w[o]
    c = np.cumsum(w, axis=0)
    # one column per replicate
    idx = (c >= c[-1] / 2).argmax(axis=0)
    return x[idx]


def stat(kind, x, w):
    if kind == "mean":
        return (x[:, None] * w).sum(0) / w.sum(0)
    return wmedian(x, w)


def age_cells(age, sex, frame):
    if frame == "pop":
        b = np.digitize(age, [30, 35, 40, 45, 50, 55, 60])
    else:
        b = np.where(age <= 30, age - 18, 13 + np.digitize(age, [35, 40, 45, 55, 65]))
    return b * 2 + (sex - 1)


def reweight(cell_g, wg, cell_r, wr):
    """Reweight reference rows to the group's cell distribution, per replicate column."""
    k = int(max(cell_g.max(), cell_r.max())) + 1
    out = np.zeros_like(wr)
    for r in range(wg.shape[1]):
        sg = np.bincount(cell_g, weights=wg[:, r], minlength=k)
        sr = np.bincount(cell_r, weights=wr[:, r], minlength=k)
        f = np.divide(sg / sg.sum(), sr, out=np.zeros(k), where=sr > 0)
        out[:, r] = wr[:, r] * f[cell_r]
    uncovered = np.bincount(cell_g, weights=wg[:, 0], minlength=k)[
        np.bincount(cell_r, weights=wr[:, 0], minlength=k) == 0].sum() / wg[:, 0].sum()
    return out, float(uncovered)


MEASURES = {  # name: (value fn, validity fn, stat kind, unit)
    "ba_plus": (lambda d: d.A_HGA.ge(43).astype(float), lambda d: d.A_AGE.ge(25), "mean", "pct"),
    "less_than_hs": (lambda d: d.A_HGA.le(38).astype(float), lambda d: d.A_AGE.ge(25), "mean", "pct"),
    "ba_plus_22plus": (lambda d: d.A_HGA.ge(43).astype(float), lambda d: d.A_AGE.ge(22), "mean", "pct"),
    "less_than_hs_20plus": (lambda d: d.A_HGA.le(38).astype(float), lambda d: d.A_AGE.ge(20), "mean", "pct"),
    "employed": (lambda d: d.PEMLR.isin([1, 2]).astype(float), lambda d: d.A_AGE.ge(18), "mean", "pct"),
    "earnings_worker_mean": (lambda d: d.earn24, lambda d: d.PEARNVAL.gt(0), "mean", "usd2024"),
    "earnings_worker_median": (lambda d: d.earn24, lambda d: d.PEARNVAL.gt(0), "median", "usd2024"),
    "ledger_partial_per_adult": (lambda d: d.ledger24, lambda d: d.A_AGE.ge(18), "mean", "usd2024"),
}
FRAMES = {
    # Observed G3/G4+ need a co-resident parent, so they appear only in the co-resident frames.
    "pop": ("all civilian household adults 25-64", ["G1", "G2", "G3plus_all", "G3plus_unresolved"]),
    "cores_one": ("adults 18+ co-resident with >=1 linked biological parent", ["G2", "G3_obs", "G3plus_all"]),
    "cores_both": ("adults 18+ co-resident with both biological parents linked", ["G2", "G3_obs", "G4plus_obs", "G3plus_all"]),
}


def build(years):
    cpi = pd.read_csv(CPI).set_index(pd.read_csv(CPI).columns[0]).iloc[:, 0]
    frames, audit = [], {}
    for y in years:
        d = load_year(y)
        g, one, both = groups(d)
        d = pd.concat([d, pd.DataFrame({**g, "one": one, "both": both}, index=d.index)], axis=1)
        d["ledger_raw"] = ledger(d)
        f = cpi.loc[2024] / cpi.loc[y - 1]
        d["earn24"] = d.PEARNVAL * f
        d["ledger24"] = d.ledger_raw * f
        audit[y] = dict(source=str(SOURCES[y][0]), sha256=sha(SOURCES[y][0]), rows=len(d), income_year=y - 1,
                        cpi_factor_to_2024=float(f),
                        fedtax_identity=bool((d.FEDTAX_AC == d.FEDTAX_BC - d.ACTC_CRD - d.EIT_CRED).all()))
        keep = d[list(g)].any(axis=1)
        frames.append(d.loc[keep, ["year", "GESTFIPS", "A_AGE", "A_SEX", "A_HGA", "PEMLR", "PEARNVAL", "earn24", "ledger24",
                                   "one", "both", *g, *REPS]].copy())
    return pd.concat(frames, ignore_index=True), audit


def gaps(p: pd.DataFrame, nyears: int, label: str):
    rows, reps = [], {}
    W = p[REPS].to_numpy(float) / nyears
    for frame, (desc, gens) in FRAMES.items():
        if frame == "pop":
            fr = p.A_AGE.between(25, 64).to_numpy()
        else:
            fr = p.A_AGE.ge(18).to_numpy() & p[frame.replace("cores_", "")].to_numpy()
        for m, (fv, fvalid, kind, unit) in MEASURES.items():
            if frame == "pop" and m in ("ba_plus_22plus", "less_than_hs_20plus"):
                continue
            x = fv(p).to_numpy(float)
            ok = fr & fvalid(p).to_numpy()
            ref = ok & p.white3plus.to_numpy()
            cr = age_cells(p.A_AGE.to_numpy()[ref], p.A_SEX.to_numpy()[ref], frame)
            for gname in gens:
                use = ok & p[gname].to_numpy()
                if use.sum() == 0:
                    continue
                cg = age_cells(p.A_AGE.to_numpy()[use], p.A_SEX.to_numpy()[use], frame)
                wr, unc = reweight(cg, W[use], cr, W[ref])
                sg = stat(kind, x[use], W[use])
                sw = stat(kind, x[ref], wr)
                raw_w = stat(kind, x[ref], W[ref])
                gap = sg - sw
                scale = 100 if unit == "pct" else 1
                key = (label, frame, m, gname)
                reps[key] = gap * scale
                se = lambda v: float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))
                rows.append(dict(source=label, frame=frame, frame_desc=desc, measure=m, unit=unit, generation=gname,
                                 n=int(use.sum()), n_ref=int(ref.sum()), weighted=float(W[use, 0].sum()),
                                 mean_age=float(np.average(p.A_AGE.to_numpy()[use], weights=W[use, 0])),
                                 value=float(sg[0] * scale), se_value=se(sg * scale),
                                 ref_value_age_matched=float(sw[0] * scale), ref_value_raw=float(raw_w[0] * scale),
                                 gap=float(gap[0] * scale), se=se(gap * scale), ref_cells_uncovered_share=unc))
    return rows, reps


def carryover(rows, reps):
    out = []
    pairs = {"pop": [("G1", "G2"), ("G2", "G3plus_all")],
             "cores_one": [("G2", "G3_obs"), ("G2", "G3plus_all")],
             "cores_both": [("G2", "G3_obs"), ("G3_obs", "G4plus_obs"), ("G2", "G4plus_obs"), ("G2", "G3plus_all")]}
    labels = sorted({k[0] for k in reps})
    for label in labels:
        for frame, pp in pairs.items():
            for m in MEASURES:
                for a, b in pp:
                    ka, kb = (label, frame, m, a), (label, frame, m, b)
                    if ka not in reps or kb not in reps:
                        continue
                    ga, gb = reps[ka], reps[kb]
                    rho = gb / ga
                    se = float(np.sqrt(4 / 160 * np.square(rho[1:] - rho[0]).sum()))
                    dse = float(np.sqrt(4 / 160 * np.square((gb - ga)[1:] - (gb - ga)[0]).sum()))
                    # A ratio is unstable when its denominator gap is within 2 SE of zero.
                    sa = float(np.sqrt(4 / 160 * np.square(ga[1:] - ga[0]).sum()))
                    out.append(dict(source=label, frame=frame, measure=m, generation=f"{a}->{b}",
                                    n=next(r["n"] for r in rows if (r["source"], r["frame"], r["measure"], r["generation"]) == kb),
                                    gap_from=float(ga[0]), gap_to=float(gb[0]), rho=float(rho[0]), se=se,
                                    change_in_gap=float(gb[0] - ga[0]), se_change=dse,
                                    denominator_stable=bool(abs(ga[0]) > 2 * sa)))
    return out


def write(rows, path):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def gate_2025():
    d = load_year(2025)
    cls = split.classify(d)
    ref = pd.read_csv(split.HERE / "derived/cps_generation_split.csv").query("arm=='reported_linkage' and age=='all'")
    got = {}
    for k in ["G3_Mexico_GP_observed", "G4plus_all_US_GP_observed"]:
        v = d.pwwgt0.to_numpy()[cls[k]].sum()
        exp = ref.loc[ref.generation.eq(k), "people"].iloc[0]
        if abs(v - exp) > 1:
            raise ValueError(f"Gate failed: {k} {v} vs {exp}")
        got[k] = float(v)
    return got


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="2022,2023,2024,2025")
    ap.add_argument("--label", default="CPS_ASEC_2022_2025")
    ap.add_argument("--out", type=Path, default=HERE / "derived")
    a = ap.parse_args()
    a.out.mkdir(exist_ok=True)
    gate = gate_2025()
    print("gate 2025 reproduced:", gate, flush=True)
    years = [int(y) for y in a.years.split(",")]
    p, audit = build(years)
    rows, reps = gaps(p, len(years), a.label)
    co = carryover(rows, reps)
    write(rows, a.out / f"cps_gaps_{a.label}.csv")
    write(co, a.out / f"cps_carryover_{a.label}.csv")
    (a.out / f"cps_audit_{a.label}.json").write_text(json.dumps(dict(gate_2025=gate, years=audit,
        pooling="weights/len(years); common replicate index across years; overlapping households across adjacent ASECs are person-years, not unique persons"), indent=2) + "\n")
    np.save(a.out / f"_reps_{a.label}.npy", {"|".join(map(str, k)): v for k, v in reps.items()}, allow_pickle=True)
    pd.set_option("display.width", 250)
    t = pd.DataFrame(rows)
    print(t[["frame", "measure", "generation", "n", "mean_age", "value", "ref_value_age_matched", "gap", "se"]].round(2).to_string(index=False))
    print(pd.DataFrame(co)[["frame", "measure", "generation", "gap_from", "gap_to", "rho", "se", "denominator_stable"]].round(3).to_string(index=False))


if __name__ == "__main__":
    main()
