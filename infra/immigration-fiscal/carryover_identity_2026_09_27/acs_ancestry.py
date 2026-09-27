"""US-born adults with Mexican ancestry who do not report Mexican origin: ACS 2024 1-year PUMS.

The ancestry write-in reveals some attriters directly: people who write a Mexican ancestry but
answer the Hispanic-origin question "not Hispanic" or another Hispanic origin. ACS has no parents'
birthplace, so generation is unknown (the group mixes G2 and G3+). Schooling, earnings and income
are measured for the same people, which is what the choice between the two attriter conventions
needs. Groups are US-born adults 25-64; the reference is US-born non-Hispanic white alone without a
Mexican ancestry entry, reweighted to each group's age (5-year) x sex mix. SEs use the 80
successive-difference replicate weights (4/80).

Mexican ancestry codes and HISP coding follow mexican_origin_population_total_2026_09_19/
acs_ancestry.py (2024 PUMS data dictionary). Income fields are scaled by ADJINC / 1e6.
Input: sources/.../acs_pums_2024_1yr/csv_pus.zip (read-only); cache: _cache/acs2024_native_2564.parquet.
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv
import hashlib
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ZIP = REPO / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
MEX_ANC = (210, 211, 212, 213, 215, 218, 219)
REPS = [f"PWGTP{i}" for i in range(1, 81)]
COLS = ["SERIALNO", "SPORDER", "ADJINC", "PWGTP", "AGEP", "SEX", "NATIVITY", "HISP", "ANC1P", "ANC2P",
        "RAC1P", "SCHL", "ESR", "WAGP", "PERNP", "PINCP"] + REPS
# SCHL -> completed years, aligned with the CPS crosswalk (12th grade without diploma = 12,
# some college = 13, associate = 14, BA = 16, MA = 18, professional = 19, doctorate = 21).
SCHL_YEARS = {1: 0, 2: 0, 3: 0, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5, 9: 6, 10: 7, 11: 8, 12: 9, 13: 10, 14: 11,
              15: 12, 16: 12, 17: 12, 18: 13, 19: 13, 20: 14, 21: 16, 22: 18, 23: 19, 24: 21}


def extract() -> pd.DataFrame:
    out = CACHE / "acs2024_native_2564.parquet"
    if out.exists():
        return pd.read_parquet(out)
    CACHE.mkdir(exist_ok=True)
    frames = []
    with zipfile.ZipFile(ZIP) as z:
        for name in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(name) as fh:
                for chunk in pd.read_csv(fh, usecols=COLS, dtype={"SERIALNO": "string"}, chunksize=300_000,
                                         low_memory=False):
                    c = chunk[chunk.NATIVITY.eq(1) & chunk.AGEP.between(25, 64)]
                    anc = c.ANC1P.isin(MEX_ANC) | c.ANC2P.isin(MEX_ANC)
                    c = c[anc | c.HISP.eq(2) | (c.HISP.eq(1) & c.RAC1P.eq(1))]
                    frames.append(c)
                    print(f"  {name}: kept {sum(len(f) for f in frames):,}", flush=True)
    d = pd.concat(frames, ignore_index=True).sort_values(["SERIALNO", "SPORDER"], kind="mergesort")
    d = d.reset_index(drop=True)
    d.to_parquet(out, index=False, compression="zstd")
    return d


def reweight(cg, wg, cr, wr):
    k = int(max(cg.max(), cr.max())) + 1
    out = np.zeros_like(wr)
    for r in range(wg.shape[1]):
        sg = np.bincount(cg, weights=wg[:, r], minlength=k)
        sr = np.bincount(cr, weights=wr[:, r], minlength=k)
        f = np.divide(sg / sg.sum(), sr, out=np.zeros(k), where=sr > 0)
        out[:, r] = wr[:, r] * f[cr]
    return out


def sdr(v):
    return float(np.sqrt(4 / 80 * np.square(v[1:] - v[0]).sum()))


def main():
    DERIVED.mkdir(exist_ok=True)
    d = extract()
    if len(d.ADJINC.unique()) != 1:
        raise ValueError("ADJINC varies within the 1-year file")
    adj = float(d.ADJINC.iloc[0]) / 1e6
    W = d[["PWGTP"] + REPS].to_numpy(float)
    anc = (d.ANC1P.isin(MEX_ANC) | d.ANC2P.isin(MEX_ANC)).to_numpy()
    hisp = d.HISP.to_numpy()
    grp = {
        "mex_id_all": hisp == 2,
        "anc_id": anc & (hisp == 2),
        "anc_nonmex": anc & (hisp != 2),
        "anc_nonhisp": anc & (hisp == 1),
        "anc_otherhisp": anc & (hisp >= 3),
        "white_ref": (hisp == 1) & d.RAC1P.eq(1).to_numpy() & ~anc,
    }
    cell = np.digitize(d.AGEP.to_numpy(), [30, 35, 40, 45, 50, 55, 60]) * 2 + (d.SEX.to_numpy() - 1)
    measures = {
        "ba_plus": (d.SCHL.ge(21).astype(float) * 100, np.ones(len(d), bool), "pct"),
        "less_than_hs": (d.SCHL.le(15).astype(float) * 100, np.ones(len(d), bool), "pct"),
        "educ_years": (d.SCHL.map(SCHL_YEARS).astype(float), np.ones(len(d), bool), "years"),
        "employed": (d.ESR.isin([1, 2, 4, 5]).astype(float) * 100, np.ones(len(d), bool), "pct"),
        "earnings_worker_mean": (d.PERNP.fillna(0) * adj, d.PERNP.fillna(0).gt(0).to_numpy(), "usd2024"),
        "wage_worker_mean": (d.WAGP.fillna(0) * adj, d.WAGP.fillna(0).gt(0).to_numpy(), "usd2024"),
        "income_person_mean": (d.PINCP.fillna(0) * adj, np.ones(len(d), bool), "usd2024"),
    }
    rows, reps = [], {}
    for m, (x, valid, unit) in measures.items():
        x = x.to_numpy(float)
        ref = grp["white_ref"] & valid
        for g in [k for k in grp if k != "white_ref"]:
            use = grp[g] & valid
            wr = reweight(cell[use], W[use], cell[ref], W[ref])
            vg = (x[use, None] * W[use]).sum(0) / W[use].sum(0)
            vr = (x[ref, None] * wr).sum(0) / wr.sum(0)
            reps[(m, g)] = vg - vr
            reps[(m, g, "w")] = W[use].sum(0)
            rows.append(dict(measure=m, unit=unit, group=g, n=int(use.sum()), weighted=float(W[use, 0].sum()),
                             mean_age=float(np.average(d.AGEP.to_numpy()[use], weights=W[use, 0])),
                             value=float(vg[0]), ref_value_age_sex_matched=float(vr[0]), gap=float(vg[0] - vr[0]),
                             se=sdr(vg - vr)))
    con = []
    for m in measures:
        for nid in ("anc_nonmex", "anc_nonhisp", "anc_otherhisp"):
            for base in ("anc_id", "mex_id_all"):
                adv = reps[(m, nid)] - reps[(m, base)]
                close = 1 - reps[(m, nid)] / reps[(m, base)]
                con.append(dict(measure=m, contrast=f"advantage, {nid} minus {base}", value=float(adv[0]), se=sdr(adv)))
                con.append(dict(measure=m, contrast=f"closing share, {nid} vs {base}", value=float(close[0]),
                                se=sdr(close)))
        sh = reps[(m, "anc_nonmex", "w")] / (reps[(m, "anc_nonmex", "w")] + reps[(m, "anc_id", "w")])
        con.append(dict(measure=m, contrast="share not Mexican among Mexican-ancestry US-born", value=float(sh[0]),
                        se=sdr(sh)))
    for name, rr in (("acs_ancestry_gaps.csv", rows), ("acs_ancestry_contrasts.csv", con)):
        with open(DERIVED / name, "w", newline="") as f:
            w = csv.DictWriter(f, fieldnames=list(rr[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(rr)
    h = hashlib.sha256()
    with ZIP.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    (DERIVED / "acs_ancestry_audit.txt").write_text(
        f"source {ZIP.relative_to(REPO)} sha256 {h.hexdigest()}\nADJINC {adj:.6f}\nrecords kept {len(d)}\n")
    pd.set_option("display.width", 250)
    print(pd.DataFrame(rows).round(3).to_string(index=False))
    print(pd.DataFrame(con).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
