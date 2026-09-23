"""EITC receipt among Mexico-born adults 25-64: the tax model's rate (no SSN rule) against the rate
with EITC zeroed for the Borjas-residual unauthorized. The generation memo's 18.8% is the
first figure; own-receipt is taken as EIT_CRED > 0 on the person record, as in that memo's table.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
FISCAL = ROOT / "infra/immigration-fiscal"
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
COLS = ["PH_SEQ", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEINUSYR",
        "SS_VAL", "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER", "A_CLSWKR",
        "PEIOOCC", "MARSUPWT", "EIT_CRED"]

with zipfile.ZipFile(ZIP) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=COLS)
    hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT"])
un = impute(d, hh)["unauthorized"]
w = d.MARSUPWT / 100
m = d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303) & d.A_AGE.between(25, 64) & d.PRPERTYP.eq(2)
eitc = d.EIT_CRED.gt(0)
raw = w[m & eitc].sum() / w[m].sum()
cor = w[m & eitc & ~un].sum() / w[m].sum()
print(f"Mexico-born 25-64 EITC>0: tax model {100*raw:.1f}%; unauthorized zeroed {100*cor:.1f}%; "
      f"share of G1 EITC recipients imputed unauthorized {100*w[m & eitc & un].sum()/w[m & eitc].sum():.1f}%")
