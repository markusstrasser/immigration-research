#!/usr/bin/env python3
"""Native-headed household share by the CEX 2024 income-quintile cut points.

The CEX consumer-unit quintiles are defined on income before taxes with published
lower limits 29,932 / 57,452 / 94,511 / 155,925 (Table 1101, 2024).  This pass reads
the ACS 2024 1-year HOUSING file, keeps housing-unit records, and computes the
native-householder share of households in each of those income bands, so the CEX
per-consumer-unit expenditures can be scaled to native consumer units rather than to
all consumer units.  Nativity of the householder comes from the person file
(SPORDER==1 is not reliable; RELSHIPP==20 identifies the householder).
"""
from __future__ import annotations
import json, zipfile
from pathlib import Path
import numpy as np, pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"; OUT.mkdir(exist_ok=True)
DATA = Path("/Users/alien/research-data/immigration-fiscal/data/external/acs_pums_2024_1yr")
PZIP = DATA / "csv_pus.zip"
HZIP = DATA / "csv_hus.zip"
CUTS = [29932.0, 57452.0, 94511.0, 155925.0]
LABELS = ["q1_lowest", "q2_second", "q3_third", "q4_fourth", "q5_highest"]

# householder nativity + household income both live on the person/housing files.
# HINCP is on the housing file; we only have the person file staged, but the person
# record of the householder carries HINCP?  No - so use the person file's household
# income proxy: sum of PINCP within SERIALNO.  Documented as a proxy.
PCOLS = ["SERIALNO", "PWGTP", "RELSHIPP", "NATIVITY", "POBP", "PINCP", "ADJINC", "AGEP"]


def main() -> None:
    frames = []
    with zipfile.ZipFile(PZIP) as z:
        for name in sorted(n for n in z.namelist() if n.lower().endswith(".csv")):
            print(f"[read] {name}", flush=True)
            with z.open(name) as fh:
                for ch in pd.read_csv(fh, usecols=PCOLS, dtype={"SERIALNO": str},
                                      chunksize=500_000, low_memory=False):
                    frames.append(ch)
    df = pd.concat(frames, ignore_index=True)
    df = df[df.SERIALNO.str.slice(4, 6) == "HU"]
    adj = df.ADJINC / 1_000_000.0
    df["inc"] = df.PINCP.fillna(0) * adj
    hh_inc = df.groupby("SERIALNO", sort=False)["inc"].sum()
    head = df[df.RELSHIPP == 20].copy()
    head["hh_income"] = head.SERIALNO.map(hh_inc)
    head["band"] = np.digitize(head.hh_income.to_numpy(), CUTS)
    head["native"] = head.NATIVITY == 1
    head["mexborn"] = head.POBP == 303

    rows = []
    for b, lab in enumerate(LABELS):
        m = head.band == b
        tot = head.loc[m, "PWGTP"].sum()
        nat = head.loc[m & head.native, "PWGTP"].sum()
        mex = head.loc[m & head.mexborn, "PWGTP"].sum()
        rows.append(dict(quintile=lab, households=float(tot),
                         native_head_households=float(nat),
                         native_head_share=float(nat / tot),
                         mexborn_head_households=float(mex),
                         mexborn_head_share=float(mex / tot)))
    out = pd.DataFrame(rows)
    out.to_csv(OUT / "native_hh_by_quintile.csv", index=False)
    print(out.to_string(index=False), flush=True)
    (OUT / "acs_hh_audit.json").write_text(json.dumps(dict(
        cut_points=CUTS, source="ACS 2024 1-year PUMS person file, household income "
        "approximated as the sum of ADJINC-adjusted PINCP within SERIALNO (housing "
        "file HINCP not staged); housing units only; householder = RELSHIPP 20.",
        total_households=float(head.PWGTP.sum())), indent=2))


if __name__ == "__main__":
    main()
