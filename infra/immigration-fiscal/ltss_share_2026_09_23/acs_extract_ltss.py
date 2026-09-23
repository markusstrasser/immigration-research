"""Slim ACS 2024 1-year PUMS person extract for the LTSS-share lane.

Adds what the integrity audit's extract lacks: Medicaid coverage (HINS4), the disability items
(DDRS self-care, DOUT independent living, DREM, DPHY, DIS) and their allocation flags, and the 80
replicate weights (kept only for persons 65+, institutional residents and Medicaid-covered
people with a self-care or independent-living difficulty). Nothing is recoded.
Writes _cache/acs2024_ltss.parquet and _cache/acs2024_ltss_rep.parquet (ignored).
Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/ltss_share_2026_09_23/acs_extract_ltss.py
"""
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
ZIP = Path.home() / "research-data/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
MAIN = ["SERIALNO", "SPORDER", "STATE", "PUMA", "PWGTP", "AGEP", "SEX", "HISP", "POBP", "NATIVITY",
        "RELSHIPP", "HINS4", "DDRS", "DOUT", "DREM", "DPHY", "DIS", "FHINS4P", "FDDRSP", "FDOUTP"]
REP = [f"PWGTP{i}" for i in range(1, 81)]


def main():
    out = HERE / "_cache"
    out.mkdir(exist_ok=True)
    mains, reps = [], []
    with zipfile.ZipFile(ZIP) as z:
        for name in ("psam_pusa.csv", "psam_pusb.csv"):
            for chunk in pd.read_csv(z.open(name), usecols=MAIN + REP, dtype={"SERIALNO": str},
                                     chunksize=500_000, low_memory=False):
                keep = (chunk.AGEP.ge(65) | chunk.RELSHIPP.eq(37)
                        | (chunk.HINS4.eq(1) & (chunk.DDRS.eq(1) | chunk.DOUT.eq(1))))
                mains.append(chunk[MAIN])
                reps.append(chunk.loc[keep, ["SERIALNO", "SPORDER"] + REP])
                print(f"  ▸ {name}: {sum(len(m) for m in mains):,} rows", flush=True)
    d = pd.concat(mains, ignore_index=True)
    r = pd.concat(reps, ignore_index=True)
    if d.duplicated(["SERIALNO", "SPORDER"]).any():
        raise SystemExit("[BLOCKED] duplicate person keys")
    d.to_parquet(out / "acs2024_ltss.parquet", index=False)
    r.to_parquet(out / "acs2024_ltss_rep.parquet", index=False)
    print(f"  ✓ {len(d):,} persons; {len(r):,} with replicate weights")


if __name__ == "__main__":
    main()
