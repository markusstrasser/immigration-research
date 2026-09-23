"""Spending audit: how much of the target's CPS EITC+ACTC sits with noncitizen Mexico-born filers.

The Census tax model simulates EITC/ACTC without legal status. Filers without an SSN (ITIN) cannot
claim EITC; ACTC needs a child SSN. This probe prices the upper bound of that eligibility defect.
"""
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/full_account_spending_2026_09_20"))
sys.path.insert(0, str(ROOT / "infra/immigration-fiscal/build"))
from builder import canonical_target  # noqa: E402

ARCH = ROOT / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
cols = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP",
        "EIT_CRED", "ACTC_CRD", "PEINUSYR"]
with zipfile.ZipFile(ARCH) as z:
    head = pd.read_csv(z.open("pppub25.csv"), nrows=0).columns
    d = pd.read_csv(z.open("pppub25.csv"), usecols=[c for c in cols if c in head])
    w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one")
civ, tgt = canonical_target(d)
wt = d.pwwgt0.to_numpy(float)
cred = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
nat = (cred[civ] * wt[civ]).sum()
t = (cred[tgt] * wt[tgt]).sum()
nc_mx = (d.PRCITSHP.eq(5) & d.PENATVTY.eq(303)).to_numpy()
t_nc = (cred[tgt & nc_mx] * wt[tgt & nc_mx]).sum()
print(f"credit $ national {nat/1e9:.2f}bn target {t/1e9:.2f}bn; held by noncitizen Mexico-born records {t_nc/1e9:.2f}bn ({t_nc/t:.1%})")
# Also all noncitizens nationally (other groups have unauthorized too)
nc = d.PRCITSHP.eq(5).to_numpy()
o_nc = (cred[civ & ~tgt & nc] * wt[civ & ~tgt & nc]).sum()
print(f"other residents' credit $ held by noncitizens {o_nc/1e9:.2f}bn ({o_nc/(nat-t):.1%})")
# Ineligible fraction f of noncitizen-held credits (unauthorized share); ~0.4-0.6 for Mexico-born, ~0.3-0.5 other
for f_t, f_o in [(0.4, 0.3), (0.5, 0.4), (0.6, 0.5)]:
    new_t = t - f_t * t_nc
    new_nat = nat - f_t * t_nc - f_o * o_nc
    s0, s1 = t / nat, new_t / new_nat
    print(f"unauth share mx {f_t} other {f_o}: key share {s0:.4f} -> {s1:.4f}")
