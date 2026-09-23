"""Spending audit: MEPS 2024 file-level checks behind the account's Medicare/Medicaid keys.

Which positive-weight persons does the donor filter (AGE24X>=0, BORNUSA in 1,2) drop, and what
share of public-payer dollars do they carry? Also MEPS national payer totals vs BEA 2024 lines.
"""
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/build"))
import meps_health_transport_2024 as m  # noqa: E402

META = ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024"
raw = META / "h256dat.zip"
sas = META / "h256su.txt"
m.FIELDS = list(dict.fromkeys(m.FIELDS + ["AGELAST", "DOBYY", "TOTMCR24", "TOTMCD24", "INSCOP24", "INSC1231", "ENDRFY24"]))
try:
    d, _ = m.read_meps(raw, sas)
except Exception as e:  # reader may reject extra fields; report and stop
    print("reader error", repr(e)); raise
pos = d.PERWT24F.gt(0)
keep = pos & d.AGE24X.ge(0) & d.BORNUSA.isin([1, 2])
print("positive-weight persons", int(pos.sum()), "kept", int(keep.sum()))
for c in ["AGE24X", "BORNUSA"]:
    print(c, "negative codes among positive weight:", d.loc[pos & ~d[c].ge(0), c].value_counts().to_dict())
for c in [x for x in ["INSC1231", "ENDRFY24", "INSCOP24"] if x in d]:
    print(c, "among dropped:", d.loc[pos & ~keep, c].value_counts().to_dict())
for payer in ["TOTMCR24", "TOTMCD24"]:
    tot = (d.loc[pos, payer] * d.loc[pos, "PERWT24F"]).sum()
    drop = (d.loc[pos & ~keep, payer] * d.loc[pos & ~keep, "PERWT24F"]).sum()
    print(f"{payer}: MEPS national ${tot/1e9:.1f}bn; dropped by filter ${drop/1e9:.1f}bn ({drop/tot:.1%}); "
          f"dropped weighted persons {d.loc[pos & ~keep, 'PERWT24F'].sum()/1e6:.2f}m, mean age last {d.loc[pos & ~keep, 'AGELAST'].mean() if 'AGELAST' in d else 'na'}")
print("BEA 2024: Medicare $1102.4bn, Medicaid+other medical $954.2bn [pinned workbook T31200-A lines 6, 33-34]")
