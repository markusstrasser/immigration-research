"""The CPS ASEC tax model assumes every respondent is a resident filer with full compliance
(Census, "Methods and Assumptions of the CPS ASEC Tax Model", Limitations). Two account keys inherit
that: receipts keyed by modeled liabilities and wages, and the refundable-credit spending line keyed
by EIT_CRED + ACTC_CRD. This script re-keys both with the status lane's corrections applied to the
Latin-American-born imputed-unauthorized (Borjas residual, `status_impute_2026_09_16/impute_status.py`):
EITC zeroed (SSN rule), ACTC, liabilities and wages scaled by an on-books share. It reports each key's
target share raw and corrected, and the implied change in the account's target dollars.
Writes derived/cps_status_keys.csv.
"""
from __future__ import annotations

import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
FISCAL = ROOT / "infra/immigration-fiscal"
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CATS = FISCAL / "full_account_receipts_2026_09_20/derived/category_allocations.csv"
US = [57, 60, 66, 69, 73, 78]
OASDI_CAP = 168_600
# Target dollars on the refundable-credit spending line keyed by EITC+ACTC (spending lane, share 0.2302).
REFUNDABLE_TARGET_BN = 52.14
PCOLS = ["PH_SEQ", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
         "PEMNTVTY", "PRDTHSP", "PEINUSYR", "SS_VAL", "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA",
         "VET_YN", "PEAFEVER", "A_CLSWKR", "PEIOOCC", "MARSUPWT", "FEDTAX_BC", "STATETAX_A",
         "WSAL_VAL", "SE_VAL", "FICA", "EIT_CRED", "ACTC_CRD"]
KEY_CATEGORIES = {
    "federal_liability": ["federal_income_tax"],
    "state_liability": ["state_local_income_tax", "other_personal_tax"],
    "wage_oasdi": ["employee_oasdi", "employer_oasdi"],
    "wage": ["employee_hi", "employer_hi"],
    "self_payroll": ["self_employment_oasdi_hi"],
    "positive_fica_worker": ["other_domestic_social_contributions"],
}


def main() -> None:
    with zipfile.ZipFile(ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PCOLS)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT"])
    st = impute(d, hh)
    w = (d.MARSUPWT / 100).to_numpy()
    latin = d.PENATVTY.between(302, 399).to_numpy() & ~d.PENATVTY.eq(327).to_numpy()
    unauth = st["unauthorized"] & latin
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    g1 = d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(303).to_numpy()
    g2 = native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy()
    g3 = native & d.PEFNTVTY.isin(US).to_numpy() & d.PEMNTVTY.isin(US).to_numpy() & d.PRDTHSP.eq(1).to_numpy()
    target = (g1 | g2 | g3) & civ
    print(f"imputed-unauthorized Latin-American-born: {w[unauth].sum()/1e6:.3f}M; "
          f"of which Mexico-born in target: {w[unauth & target].sum()/1e6:.3f}M")

    raw = {
        "federal_liability": d.FEDTAX_BC.clip(lower=0).to_numpy(float),
        "state_liability": d.STATETAX_A.clip(lower=0).to_numpy(float),
        "wage_oasdi": d.WSAL_VAL.clip(upper=OASDI_CAP).to_numpy(float),
        "wage": d.WSAL_VAL.to_numpy(float),
        "self_payroll": d.SE_VAL.clip(lower=0).to_numpy(float),
        "positive_fica_worker": d.FICA.gt(0).to_numpy(float),
    }
    rows = []
    cats = pd.read_csv(CATS)
    cats = cats[cats.scenario_id.eq("cbo_collective")]
    for on_books in (0.44, 0.60, 0.75):
        for key, v in raw.items():
            corr = np.where(unauth, v * on_books, v)
            s_raw = (w * v)[target].sum() / (w * v).sum()
            s_cor = (w * corr)[target].sum() / (w * corr).sum()
            for alloc in ("shared", "personal"):
                tb = cats[cats.allocation.eq(alloc) & cats.category.isin(KEY_CATEGORIES[key])].target_bn.sum()
                rows.append(dict(on_books=on_books, key=key, allocation=alloc, share_raw=s_raw,
                                 share_corrected=s_cor, target_bn=tb,
                                 delta_target_bn=tb * (s_cor / s_raw - 1)))
        # Refundable credits: EITC zeroed for the unauthorized holder, ACTC scaled by on-books share.
        v = (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)
        corr = np.where(unauth, d.ACTC_CRD.to_numpy(float) * on_books, v)
        s_raw = (w * v)[target].sum() / (w * v).sum()
        s_cor = (w * corr)[target].sum() / (w * corr).sum()
        rows.append(dict(on_books=on_books, key="eitc_actc_spending", allocation="both", share_raw=s_raw,
                         share_corrected=s_cor, target_bn=REFUNDABLE_TARGET_BN,
                         delta_target_bn=REFUNDABLE_TARGET_BN * (s_cor / s_raw - 1)))
    t = pd.DataFrame(rows)
    t.to_csv(HERE / "derived/cps_status_keys.csv", index=False)
    pd.set_option("display.width", 200)
    print(t.round(4).to_string())
    for ob in (0.44, 0.60, 0.75):
        s = t[t.on_books.eq(ob)]
        rec = s[s.key.ne("eitc_actc_spending")].groupby("allocation").delta_target_bn.sum()
        spend = s[s.key.eq("eitc_actc_spending")].delta_target_bn.iloc[0]
        # Welfare cost to others = spending - receipts; lower receipts raise it, lower spending cuts it.
        print(f"on-books {ob}: receipts change shared {rec['shared']:+.2f}bn personal {rec['personal']:+.2f}bn; "
              f"refundable spending change {spend:+.2f}bn; net cost change "
              f"{-rec['shared'] + spend:+.2f} / {-rec['personal'] + spend:+.2f}bn")


if __name__ == "__main__":
    main()
