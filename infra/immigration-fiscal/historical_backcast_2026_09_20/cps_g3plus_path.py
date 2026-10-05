#!/usr/bin/env python3
"""The identified third-plus generation by year, the path the v5 lineage is carried back on; writes
`inputs/cps_g3plus_path.csv`.

The main case adopted on 2026-10-05 (main_case_2026_10_05) adds 3.04M descendants of Mexican immigrants who no
longer report Mexican origin. Their count by year (the third-plus generation by year times the attrition rate) is not
measured. Until it is, the back-cast carries the lineage at the identified third-plus generation's own path, holding
the added people's 2024 ratio to it (the case lane's Consumers row). This script measures that path: the CPS ASEC
weighted count of self-identified Mexican-origin people born in the United States or an outlying area to two parents
born there (IPUMS BPL, MBPL and FBPL under 15000; HISPAN 100, 102-104, 108 or 109, the codes of
g3_identity_pooled_2026_10_05/analyze.py), the population lane's third-plus (bounds_coverage_fiscal.py g3).

Year t is income year t, ASEC survey year t + 1: the account's 2024 is ASEC 2025. The 2014 ASEC holds two subsamples
(HFLAG 0 and 1), each weighted to the whole population; both are kept, at half weight. Only ASEC records count
(ASECFLAG 1).

Input : ../g3_identity_pooled_2026_10_05/_cache/asec_pooled.csv.gz, IPUMS-CPS extract 4 (ignored; that lane's
        extract.py rebuilds it), SHA256 pinned
Output: inputs/cps_g3plus_path.csv: year, asec_year, g3plus_persons, g3plus_sample_n, union_persons, all_persons
        (union: Mexico-born, US-born with a Mexico-born parent, or third-plus as above)
Gate  : ASEC 2025's third-plus is within 0.5% of the population lane's 14,383,006.5 on the Census public-use file
        (main_case_lineage_2026_10_05/derived/population.json meta.self_id_third_plus_cps); every year 2006-2025 has
        records. Nothing is written on failure.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/cps_g3plus_path.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
EXTRACT = FISCAL / "g3_identity_pooled_2026_10_05/_cache/asec_pooled.csv.gz"
EXTRACT_SHA256 = "59e1c80d8738f8f3938b235db66f1656bce480b3cee276fcb1ed6ba748822e7e"
POPULATION = FISCAL / "main_case_lineage_2026_10_05/derived/population.json"
OUT = HERE / "inputs/cps_g3plus_path.csv"
MEX_HISPAN = [100, 102, 103, 104, 108, 109]
MEXICO, US_MAX = 20000, 15000
YEARS = range(2005, 2025)
COLS = ["YEAR", "ASECFLAG", "HFLAG", "ASECWT", "BPL", "MBPL", "FBPL", "HISPAN"]


def main() -> None:
    digest = hashlib.sha256(EXTRACT.read_bytes()).hexdigest()
    if digest != EXTRACT_SHA256:
        raise SystemExit(f"[BLOCKED] {EXTRACT.name} is not IPUMS-CPS extract 4 as pinned: {digest}")
    sums = []
    for chunk in pd.read_csv(EXTRACT, usecols=COLS, chunksize=1_000_000, dtype={"HFLAG": "float64"}):
        d = chunk[(chunk.ASECFLAG == 1) & chunk.YEAR.between(YEARS[0] + 1, YEARS[-1] + 1)]
        w = d.ASECWT * d.YEAR.eq(2014).map({True: 0.5, False: 1.0})
        native = d.BPL < US_MAX
        g3 = native & (d.MBPL < US_MAX) & (d.FBPL < US_MAX) & d.HISPAN.isin(MEX_HISPAN)
        union = (d.BPL == MEXICO) | (native & ((d.MBPL == MEXICO) | (d.FBPL == MEXICO))) | g3
        sums.append(pd.DataFrame(dict(asec_year=d.YEAR, g3plus_persons=w * g3, g3plus_sample_n=g3.astype(int),
                                      union_persons=w * union, all_persons=w)).groupby("asec_year").sum())
    table = pd.concat(sums).groupby(level=0).sum()
    missing = [t + 1 for t in YEARS if t + 1 not in table.index]
    if missing:
        raise SystemExit(f"[BLOCKED] the extract has no ASEC records for {missing}")
    want = json.loads(POPULATION.read_text())["meta"]["self_id_third_plus_cps"]
    got = table.loc[YEARS[-1] + 1, "g3plus_persons"]
    if abs(got / want - 1) > 0.005:
        raise SystemExit(f"[BLOCKED] ASEC 2025's third-plus {got:,.1f} is not the population lane's {want:,.1f} (0.5%)")
    out = table.reset_index()
    out.insert(0, "year", out.asec_year - 1)
    out["g3plus_sample_n"] = out.g3plus_sample_n.astype(int)
    OUT.parent.mkdir(exist_ok=True)
    out.round(2).to_csv(OUT, index=False, lineterminator="\n")
    print(f"ASEC 2025 third-plus {got:,.1f} (population lane {want:,.1f}, {100 * (got / want - 1):+.2f}%)")
    print(out.assign(**{c: out[c] / 1e6 for c in ("g3plus_persons", "union_persons", "all_persons")}).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
