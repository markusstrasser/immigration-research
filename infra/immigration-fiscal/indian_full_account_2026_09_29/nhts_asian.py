"""NHTS 2017 annual driver miles per person aged 5+ by five-year band for non-Hispanic Asian residents: the driving
rate the sept29 re-key's road-miles rule (white lane's rekey_sept29.py rule 4) needs for the Indian-origin group.

NHTS has no Asian Indian category, so NH Asian (R_HISP 2, R_RACE 3) stands in for the group [DEGRADED: a proxy]. The
code is white_replacement_2026_09_28/v4_inputs.py nhts_vmt() with that group added; the NH white rows must reproduce
the white lane's derived/v4_nhts_vmt.csv to 1e-8 relative (gate; summation order differs).
Output: derived/nhts_vmt_asian.csv (nh_asian and nh_white rows, as v4_nhts_vmt.csv lays them out).
Run from the repository root (about 1 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/nhts_asian.py
"""
from __future__ import annotations

import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
NHTS = FISCAL / "congestion_2026_09_23/_cache/nhts2017_csv.zip"
REF = FISCAL / "white_replacement_2026_09_28/derived/v4_nhts_vmt.csv"
BANDS = list(range(5, 80, 5)) + [80]


def main():
    with zipfile.ZipFile(NHTS) as z:
        persons = pd.read_csv(z.open("perpub.csv"), usecols=["HOUSEID", "PERSONID", "WTPERFIN", "R_AGE", "R_HISP", "R_RACE"],
                              dtype={"HOUSEID": str, "PERSONID": str})
        parts = []
        for ch in pd.read_csv(z.open("trippub.csv"), usecols=["HOUSEID", "PERSONID", "WTTRDFIN", "VMT_MILE", "DRVR_FLG"],
                              dtype={"HOUSEID": str, "PERSONID": str}, chunksize=500_000):
            v = ch.VMT_MILE.where(ch.VMT_MILE.ge(0), 0).to_numpy(float) * ch.DRVR_FLG.eq(1).to_numpy()
            parts.append(pd.DataFrame({"HOUSEID": ch.HOUSEID, "PERSONID": ch.PERSONID,
                                       "vmt": ch.WTTRDFIN.to_numpy(float) * v}).groupby(["HOUSEID", "PERSONID"]).vmt.sum())
    vmt = pd.concat(parts).groupby(level=[0, 1]).sum()
    p = persons.set_index(["HOUSEID", "PERSONID"])
    if not vmt.index.isin(p.index).all():
        raise SystemExit("[BLOCKED] NHTS trips without a person record")
    p["vmt"] = vmt.reindex(p.index).fillna(0.0).to_numpy()
    p = p.reset_index()
    groups = {"nh_asian": p.R_HISP.eq(2) & p.R_RACE.eq(3), "nh_white": p.R_HISP.eq(2) & p.R_RACE.eq(1)}
    aged = p[p.R_AGE.ge(5)].copy()
    aged["band"] = np.minimum(aged.R_AGE // 5 * 5, 80).astype(int)
    rows = []
    for g, m in groups.items():
        sub = aged[m.loc[aged.index]]
        by = sub.groupby("band").agg(persons=("WTPERFIN", "sum"), vmt=("vmt", "sum"), sample=("WTPERFIN", "size"))
        by = by.reindex(BANDS)
        if by.persons.isna().any():
            raise SystemExit(f"[BLOCKED] NHTS {g}: an age band has no persons")
        for b, r in by.iterrows():
            rows.append({"group": g, "band": b, "persons_5plus": r.persons, "driver_vmt_bn": r.vmt / 1e9,
                         "vmt_per_person": r.vmt / r.persons, "sample_persons": int(r["sample"])})
        rows.append({"group": g, "band": "all", "persons_5plus": float(p.WTPERFIN[m].sum()),
                     "driver_vmt_bn": float(p.vmt[m].sum() / 1e9),
                     "vmt_per_person": float(p.vmt[m].sum() / p.WTPERFIN[m].sum()), "sample_persons": int(m.sum())})
    out = pd.DataFrame(rows)
    ref = pd.read_csv(REF, dtype={"band": str})
    mine = out[out.group == "nh_white"].assign(band=lambda x: x.band.astype(str)).set_index("band")
    theirs = ref[ref.group == "nh_white"].set_index("band")
    t = theirs.vmt_per_person.reindex(mine.index)
    diff = float(((mine.vmt_per_person - t).abs() / t.abs().clip(lower=1.0)).max())
    if not diff < 1e-8:
        raise SystemExit(f"[BLOCKED] NH white rows do not reproduce v4_nhts_vmt.csv (max relative diff {diff})")
    print(f"[gate] NH white rows reproduce the white lane's v4_nhts_vmt.csv (max relative diff {diff:.2e})")
    (LANE / "derived").mkdir(exist_ok=True)
    out.to_csv(LANE / "derived/nhts_vmt_asian.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(out[out.band == "all"].to_string(index=False))


if __name__ == "__main__":
    main()
