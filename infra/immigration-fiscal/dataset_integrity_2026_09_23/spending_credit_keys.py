"""Spending audit: target shares of the components inside BEA Table 3.12 line 25 (refundable tax credits).

The spending lane keys the whole $228.8bn line by CPS EITC+ACTC. The line also carries ACA premium
tax credits (BEA 2014 briefing). This probe computes the target share of each component key in
CPS ASEC 2025 with the lane's own canonical target, so the key mismatch can be priced.
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
        "EIT_CRED", "ACTC_CRD", "CTC_CRD", "MRKS", "MRK", "I_MRKS", "FEDTAX_BC", "FEDTAX_AC", "MCAID", "I_MCAID", "TAX_ID"]
with zipfile.ZipFile(ARCH) as z:
    head = pd.read_csv(z.open("pppub25.csv"), nrows=0).columns
    use = [c for c in cols if c in head]
    d = pd.read_csv(z.open("pppub25.csv"), usecols=use)
    w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one")
civ, tgt = canonical_target(d)
wt = d.pwwgt0.to_numpy(float)
print("target pop m", wt[tgt].sum() / 1e6, "civ pop m", wt[civ].sum() / 1e6)


def share(v, label):
    v = np.asarray(v, float)
    nat = (v[civ] * wt[civ]).sum()
    t = (v[tgt] * wt[tgt]).sum()
    print(f"{label:38s} national {nat/1e9:10.2f}  target {t/1e9:8.2f}  share {t/nat:.4f}")
    return t / nat


for c in ["MRKS", "MRK", "MCAID"]:
    if c in d:
        print(c, "values", sorted(d[c].unique())[:8])
s_eitc = share(d.EIT_CRED, "EITC $")
s_actc = share(d.ACTC_CRD, "ACTC $")
s_both = share(d.EIT_CRED + d.ACTC_CRD, "EITC+ACTC $ (lane key)")
s_ctc = share(d.CTC_CRD, "CTC nonrefundable $")
s_mrks = share(d.MRKS.eq(1), "subsidized marketplace persons (MRKS=1)")
if "I_MRKS" in d:
    for g, m in [("target", tgt), ("other", civ & ~tgt)]:
        sel = m & d.MRKS.eq(1).to_numpy()
        print(g, "MRKS=1 allocated share", (wt[sel] * (d.I_MRKS.to_numpy()[sel] != 0)).sum() / wt[sel].sum())
# BEA line 25 composition bands, calendar 2024, $bn: EITC+refundable CTC carried at CPS-scale shares;
# premium tax credit 100-120 (CBO FY2024 outlays incl. related spending $103bn).
line = 228.809
for ptc in (100.0, 110.0, 120.0):
    rest = line - ptc
    blended = (rest * s_both + ptc * s_mrks) / line
    print(f"PTC {ptc:5.1f}: blended share {blended:.4f}  target $bn {line*0.9900527*blended:6.2f}  lane $bn {line*0.9900527*s_both:6.2f}  delta {line*0.9900527*(blended-s_both):+6.2f}")
