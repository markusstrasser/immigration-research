"""The group's share of public transit commuters, ACS 2024 1-year PUMS (persons), for the transit key beside the lane.

The account nets every non-housing government enterprise into one receipt, the current surplus of government
enterprises, and keys it, and the return on enterprise capital, by population. Public transit runs the largest
loss (NIPA T3.8 line 14, -$66.690bn in 2024). Its fares are roughly proportional to rides, so the fee term is zero;
what the population key misses is the group's share of rides. Commuting by transit (JWTRNS 02-06: bus, subway or
elevated rail, commuter rail, light rail or streetcar, ferry) stands in for rides [ASSUMPTION: about half of transit
trips are commutes; the rest are taken at the same group share].

Group: HISP 02 or POBP 303, as acs_college.py. Writes derived/acs_transit.json. Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/acs_transit.py
"""
import hashlib
import json
import zipfile
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
PUMS = REPO / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip"
PUMS_SHA = "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"
TRANSIT = [2, 3, 4, 5, 6]
OUT = HERE / "derived"


def sha(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def main():
    if sha(PUMS) != PUMS_SHA:
        raise SystemExit(f"[BLOCKED] {PUMS} is not the pinned ACS 2024 person file")
    acc = {k: 0.0 for k in ["persons", "group", "workers", "group_workers", "transit", "group_transit"]}
    by_mode = []
    with zipfile.ZipFile(PUMS) as z:
        for name in ["psam_pusa.csv", "psam_pusb.csv"]:
            for d in pd.read_csv(z.open(name), usecols=["PWGTP", "HISP", "POBP", "JWTRNS"], chunksize=500_000):
                g = d.HISP.eq(2) | d.POBP.eq(303)
                w = d.PWGTP.astype(float)
                worker = d.JWTRNS.notna()
                transit = d.JWTRNS.isin(TRANSIT)
                acc["persons"] += w.sum(); acc["group"] += w[g].sum()
                acc["workers"] += w[worker].sum(); acc["group_workers"] += w[worker & g].sum()
                acc["transit"] += w[transit].sum(); acc["group_transit"] += w[transit & g].sum()
                by_mode.append(d[transit].assign(w=w[transit], gw=w[transit & g].reindex(d[transit].index).fillna(0))
                               .groupby("JWTRNS")[["w", "gw"]].sum())
    modes = pd.concat(by_mode).groupby(level=0).sum()
    out = {k: float(v) for k, v in acc.items()}
    out.update(population_share=acc["group"] / acc["persons"], worker_share=acc["group_workers"] / acc["workers"],
               transit_commuter_share=acc["group_transit"] / acc["transit"],
               by_mode={int(k): {"commuters": float(r.w), "group_share": float(r.gw / r.w)} for k, r in modes.iterrows()},
               source={"file": str(PUMS.relative_to(REPO)), "sha256": PUMS_SHA, "transit_codes": TRANSIT})
    (OUT / "acs_transit.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ["population_share", "worker_share", "transit_commuter_share", "by_mode"]},
                     indent=1))


if __name__ == "__main__":
    main()
