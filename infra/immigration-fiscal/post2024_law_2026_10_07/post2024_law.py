#!/usr/bin/env python3
"""Current law today beside the 2024 account: the lineage's cut from laws enacted or taking effect after income-year 2024.

The account is income-year 2024 under 2024 law. This script prices, for main case v5's 42.75M lineage, the transfer
changes that current law makes by the first fiscal year in which every piece is in full effect (FY2028), with FY2027
beside it:

(a) P.L. 119-21 (4 July 2025) eligibility limits, CBO's scores (pub 61570, Titles I and VII, relative to the January
    2025 baseline): SNAP §10108, Medicaid/CHIP §71109, the emergency-Medicaid FMAP §71110, Medicare §71201, the
    premium tax credit for eligible aliens only §71301 and below 100% FPL §71302; and the child tax credit's
    taxpayer-SSN rule §70104(b), which CBO/JCT do not score alone, measured here on the CPS tax model.
(b) Expiry of the enhanced premium tax credit after 2025 (not restored as of the run date), priced at CBO's cost of
    permanent extension (pub 61734, relative to the post-P.L. 119-21 baseline).
(c) The 2026 public-charge rule, read from public_charge_share_2026_10_07/derived/summary.json.

Shares come from CPS ASEC 2025 through the distribution lane's loader with the lineage weights of
world_ledger_2026_09_27/population_basis.py (pattern: public_charge_share.py): numerator on the lineage weights over a
row-4 denominator. Legal status uses the account's residual imputation (status_impute_2026_09_16 impute(), Borjas
rules, all origins). The CPS cannot tell LPRs from other lawfully present noncitizens, so each eligibility row carries
a broad share (every noncitizen recipient outside the kept classes) and a narrow one (those who arrived 2016 or
later, where refugees, parolees and asylum applicants sit); the narrow share is central [ASSUMPTION]. Cuban- and
Haitian-born (Cuban/Haitian entrants) and Marshall Islands- and Micronesia-born (COFA) are kept eligible by statute
and leave the affected denominators.

PTC shares are dollar-weighted by a premium tax credit computed on each CPS tax unit (TAX_ID): KFF's 2024 national
average benchmark ($477 a month at 40) on the CMS default age curve, tax-unit AGI against the 2023 poverty
guidelines, the ARPA/IRA applicable percentages (enhanced) and Rev. Proc. 2025-25's 2026 table (original, no credit
above 400% FPL). Units under 100% FPL are priced at 100%.

The 3.04M added descendants of the lineage are US-born citizens: no eligibility rule here touches them, and they enter
only through the G3+ records' lineage weights, which carry no noncitizen [CALCULATION: gated below].

Dollars: CBO's fiscal-year nominal figures deflated to calendar 2024 by CBO's CPI-U path (LTBO 2026, sheet 16, 2026
projections). Writes derived/rows.csv, derived/shares.csv, derived/summary.json. From the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/post2024_law_2026_10_07/post2024_law.py
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import openpyxl

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parents[1]
OUT = LANE / "derived"
STAGE = ROOT / "sources/immigration-fiscal/data/external/stage3/cbo"
CBO_LAW = STAGE / "pl119_21_estimate/61570-pl119-21-2025Recon-CLB.xlsx"
CBO_LAW_SHA = "b6f7a7ae822633a70d4abaec1e26e4b4ac428e7ed09fc3aee9dbd5d83c7bc552"
CBO_EXT = STAGE / "ptc_extension_61734/61734-data.xlsx"
CBO_EXT_SHA = "2e92669f00f2bf7bca55d9f57a1098967e7609154e7e085ea90d8cca03db5e54"
LTBO = STAGE / "ltbo_2026/62044-2026-LTBO.xlsx"
LTBO_SHA = "5e1dd450cebd869dd3066d3d965351f3778808ce17f261f7a0571e6c21d93e4b"
CURVE = FISCAL / "ir5_adjusters_2026_09_27/_cache/ptc/cms_state_age_curves_2017.txt"
PUBLIC_CHARGE = FISCAL / "public_charge_share_2026_10_07/derived/summary.json"
DECOMP = FISCAL / "main_case_decomposition_2026_09_29/derived/summary_oct05.json"
MTS = FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json"

sys.path.insert(0, str(FISCAL / "world_ledger_2026_09_27"))
from population_basis import reweight  # noqa: E402

sys.dont_write_bytecode = True  # read-only import from the status lane
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

STATUS_COLS = ["PH_SEQ", "PPPOS", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
               "PEINUSYR", "SS_VAL", "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER",
               "A_CLSWKR", "PEIOOCC"]
EXTRA_P = ["PH_SEQ", "PPPOS", "TAX_ID", "AGI", "CTC_CRD", "ACTC_CRD", "DEP_STAT", "MRKS", "MCAID", "PCHIP", "MCARE",
           "PEINUSYR"]
KEPT_BIRTHPLACES = {327: "Cuba", 332: "Haiti", 511: "Marshall Islands", 512: "Micronesia"}  # CPS Appendix H
RECENT = 25            # PEINUSYR 25 = 2016-2017 ... 28 = 2022-2025
NON_EXPANSION_2024 = {1, 12, 13, 20, 28, 45, 47, 48, 55, 56}  # AL FL GA KS MS SC TN TX WI WY (GESTFIPS)
ON_BOOKS = (0.44, 0.60, 0.75)  # cps_imputation_keys_2026_09_23/combine_status.py ON_BOOKS (low, central, high)
# [ASSUMPTION] share of the residual's unauthorized filers who truly lack a work-authorized SSN (low, central, high):
# the residual also holds DACA recipients, parolees and asylum applicants with work permits, who keep the credit.
NO_WORK_SSN = (0.80, 0.90, 1.00)
ODC = 500.0            # credit for other dependents, kept by dependents without a qualifying-child SSN
BENCHMARK_40 = 477.0   # KFF State Health Facts, US average benchmark premium at 40, 2024, $ a month
FPL_2023 = (14_580.0, 5_140.0)  # HHS 2023 guidelines, 48 states (2024 coverage year)
ENHANCED = [(1.0, 0.0, 0.0), (1.5, 0.0, 0.0), (2.0, 0.0, 2.0), (2.5, 2.0, 4.0), (3.0, 4.0, 6.0), (4.0, 6.0, 8.5)]
ORIGINAL = [(1.33, 2.10, 2.10), (1.5, 3.14, 4.19), (2.0, 4.19, 6.60), (2.5, 6.60, 8.44), (3.0, 8.44, 9.96),
            (4.0, 9.96, 9.96)]  # Rev. Proc. 2025-25 section 3.01, 2026
FYS = ("2027", "2028")


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")
    print(f"  gate ok: {name}")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def sheet_rows(path: Path, sheet: str):
    wb = openpyxl.load_workbook(path, data_only=True, read_only=True)
    return [list(r) for r in wb[sheet].iter_rows(values_only=True)]


def cbo_row(rows, section, label, start_col=3):
    """FY2025-2034 values of the first `label` row after the row naming `section`."""
    for i, r in enumerate(rows):
        if any(str(c).strip() == str(section) for c in r if c is not None):
            for r2 in rows[i:i + 12]:
                lab = next((str(c) for c in r2[:3] if c is not None and not str(c).startswith("Sec")), "")
                if lab.startswith(label):
                    vals = r2[start_col:start_col + 10]
                    return dict(zip([str(y) for y in range(2025, 2035)], [float(v) for v in vals]))
    raise SystemExit(f"[BLOCKED] CBO row {section} {label!r} not found")


def law_scores():
    gate("cbo_61570_hash", sha(CBO_LAW) == CBO_LAW_SHA)
    t1, t7 = sheet_rows(CBO_LAW, "Title I"), sheet_rows(CBO_LAW, "Title VII")
    rev = [r for r in t7]
    s = {
        "snap_10108": {"outlays": cbo_row(t1, 10108, "Estimated Outlays")},
        "medicaid_71109": {"outlays": cbo_row(t7, 71109, "Estimated Outlays")},
        "emergency_fmap_71110": {"outlays": cbo_row(t7, 71110, "Estimated Outlays")},
        "medicare_71201": {"outlays": cbo_row(t7, 71201, "Estimated Outlays")},
        "ptc_eligible_aliens_71301": {"outlays": cbo_row(t7, 71301, "Estimated Outlays")},
        "ptc_below_100_71302": {"outlays": cbo_row(t7, 71302, "Estimated Outlays")},
    }
    # Revenue rows sit in the revenue half of the sheet: the second block naming each section.
    for k, sec in (("ptc_eligible_aliens_71301", 71301), ("ptc_below_100_71302", 71302)):
        hits = [i for i, r in enumerate(rev) if any(str(c).strip() == str(sec) for c in r if c is not None)]
        gate(f"cbo_{sec}_has_outlay_and_revenue_blocks", len(hits) == 2, hits=hits)
        s[k]["revenues"] = cbo_row(rev[hits[1]:], sec, "Estimated Revenues")
    gate("cbo_71301_fy2028_printed", s["ptc_eligible_aliens_71301"]["outlays"]["2028"] == -7923
         and s["ptc_eligible_aliens_71301"]["revenues"]["2028"] == 544)
    gate("cbo_10108_fy2028_printed", s["snap_10108"]["outlays"]["2028"] == -216)
    gate("cbo_71110_fy2028_printed", s["emergency_fmap_71110"]["outlays"]["2028"] == -3112)
    # Context only (not in the arm): programme-wide provisions that hit the lineage as citizens.
    ctx = {"medicaid_work_requirements_71119": cbo_row(t7, 71119, "Estimated Outlays"),
           "snap_work_requirements_10102": cbo_row(t1, 10102, "Estimated Outlays"),
           "snap_state_match_10105": cbo_row(t1, 10105, "Estimated Outlays"),
           "ptc_verification_71303": cbo_row(t7, 71303, "Estimated Outlays"),
           "ptc_special_enrollment_71304": cbo_row(t7, 71304, "Estimated Outlays"),
           "ptc_recapture_71305": cbo_row(t7, 71305, "Estimated Outlays")}
    gate("cbo_71119_fy2028_printed", ctx["medicaid_work_requirements_71119"]["2028"] == -18960)
    return s, ctx


def extension_cost():
    gate("cbo_61734_hash", sha(CBO_EXT) == CBO_EXT_SHA)
    rows = sheet_rows(CBO_EXT, "Table 1")
    for i, r in enumerate(rows):
        if r[0] and str(r[0]).startswith("Permanently Extend"):
            net = next(x for x in rows[i:i + 6] if x[1] == "Net Effect on Deficit")
            vals = [float(v) for v in net[5:15]]
            out = dict(zip([str(y) for y in range(2026, 2036)], vals))
            gate("cbo_61734_fy2028_printed", round(out["2028"]) == 30382 and round(out["2027"]) == 31919)
            return out
    raise SystemExit("[BLOCKED] CBO 61734 extension row not found")


def deflators():
    """CY2024 dollars per FY nominal dollar, from CBO's 2026 CPI-U projections (CY growth rates)."""
    gate("ltbo_hash", sha(LTBO) == LTBO_SHA)
    rows = sheet_rows(LTBO, "16. 2025&2026 Econ Proj")
    cpi = {str(int(r[0])): float(r[5]) / 100 for r in rows if isinstance(r[0], (int, float)) and r[5] is not None}
    gate("ltbo_cpi_2026_projection_2027", abs(cpi["2027"] - 0.02547) < 1e-4, cpi2027=cpi["2027"])
    # CY average index: 2024 = 1. A fiscal year t is centred on 1 April of calendar t: three quarters of a year
    # past the middle of calendar t-1.
    idx = {"2024": 1.0}
    for y in range(2025, 2029):
        idx[str(y)] = idx[str(y - 1)] * (1 + cpi[str(y)])
    return {fy: 1 / (idx[str(int(fy) - 1)] * (1 + cpi[fy]) ** 0.75) for fy in FYS}, cpi


def age_curve():
    curve = {}
    for line in CURVE.read_text().splitlines():
        m = re.match(r"\s*(\d+)(?:-(\d+))?(\s+and Older)?\s+(\d\.\d{3})\s", line)
        if m:
            lo = int(m.group(1))
            hi = int(m.group(2)) if m.group(2) else (120 if m.group(3) else lo)
            for a in range(lo, hi + 1):
                curve[a] = float(m.group(4))
    gate("cms_age_curve", curve[21] == 1.0 and curve[40] == 1.278 and curve[64] == 3.0)
    return curve


def applicable(ratio, table, cap_400):
    """Applicable percentage of income (fraction) by FPL ratio; NaN above 400% where the original law gives none."""
    r = np.maximum(ratio, 1.0)
    out = np.full(r.shape, np.nan)
    lo = 1.0
    for hi, a, b in table:
        m = (r >= lo) & (r < hi) if hi < 4.0 else (r >= lo) & (r <= hi)
        out[m] = (a + (b - a) * (r[m] - lo) / (hi - lo)) / 100 if hi > lo else a / 100
        lo = hi
    above = r > 4.0
    out[above] = np.nan if cap_400 else table[-1][2] / 100
    if not cap_400:
        out[r < 1.5] = 0.0
    return out


def build_frame(extra_p=(), extra_h=()):
    """CPS ASEC 2025 civilians on the lineage weights, with the residual status flag; tax_side.py reuses it."""
    spec = importlib.util.spec_from_file_location("dist_base", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    extra_p = [c for c in extra_p if c not in EXTRA_P and c not in d.columns]
    with zipfile.ZipFile(B.PATHS["cps"]) as z:
        p = pd.read_csv(z.open("pppub25.csv"), usecols=EXTRA_P + extra_p)
        s = pd.read_csv(z.open("pppub25.csv"), usecols=STATUS_COLS)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT", "HFDVAL", "GESTFIPS"]
                         + list(extra_h))
    d = d.merge(p, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    d = d.merge(hh.rename(columns={"H_SEQ": "PH_SEQ"})[["PH_SEQ", "HFDVAL", "GESTFIPS"] + list(extra_h)],
                on="PH_SEQ", validate="many_to_one", how="left")
    st = impute(s, hh)
    flag = pd.DataFrame({"PH_SEQ": s.PH_SEQ, "PPPOS": s.PPPOS, "unauth": st["unauthorized"]})
    d = d.merge(flag, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left")
    gate("status_aligned", not d.unauth.isna().any())
    return reweight(d, B.PATHS["cps"], gate, "lineage")


def main() -> None:
    d = build_frame()

    frame = json.loads(DECOMP.read_text())["frame"]["row4"]
    civ, tgt = d.civ.to_numpy(), d.target.to_numpy()
    lw, r4 = d.pw.to_numpy(float), d.pw_row4.to_numpy(float)
    gate("lineage_is_the_decompositions_NG", abs(lw[tgt].sum() - frame["NG"]) < 1e-2)
    gate("row4_civilians_are_the_decompositions_NC", abs(r4[civ].sum() - frame["NC"]) < 1.0)
    noncit = d.PRCITSHP.eq(5).to_numpy() & civ
    unauth = d.unauth.to_numpy(bool) & civ
    # The added descendants ride on G3+ records' weights (lw > r4 within the target): all citizens.
    lifted = tgt & (lw > r4 * (1 + 1e-9))
    gate("added_descendants_are_citizens", lifted.any() and not (lifted & noncit).any(),
         lifted_noncitizen=int((lifted & noncit).sum()))
    added_m = float((lw - r4)[tgt].sum()) / 1e6
    kept = d.PENATVTY.isin(list(KEPT_BIRTHPLACES)).to_numpy()
    recent = d.PEINUSYR.ge(RECENT).to_numpy()
    expansion = ~d.GESTFIPS.isin(list(NON_EXPANSION_2024)).to_numpy()

    # Tax units.
    unit = d.TAX_ID.to_numpy()
    dep = d.DEP_STAT.gt(0).to_numpy()
    g = d.groupby("TAX_ID")
    n_unit = g.TAX_ID.transform("size").to_numpy(float)
    agi = d.AGI.where(~d.DEP_STAT.gt(0), 0).groupby(d.TAX_ID).transform("sum").to_numpy(float)
    fpl = FPL_2023[0] + FPL_2023[1] * (n_unit - 1)
    ratio = np.maximum(agi, 0) / fpl

    # (a7) Child tax credit: units where no filer has a work-authorized SSN (every non-dependent is imputed
    # unauthorized) lose the credit for qualifying children; dependents who are noncitizens or 17+ keep the ODC.
    filer_ok = pd.Series(~dep & ~d.unauth.to_numpy(bool)).groupby(unit).transform("any").to_numpy()
    has_filer = pd.Series(~dep).groupby(unit).transform("any").to_numpy()
    no_ssn_unit = has_filer & ~filer_ok
    ctc_unit = (d.CTC_CRD + d.ACTC_CRD).groupby(d.TAX_ID).transform("sum").to_numpy(float)
    nonref_unit = d.CTC_CRD.groupby(d.TAX_ID).transform("sum").to_numpy(float)
    odc_dep = dep & (d.PRCITSHP.eq(5).to_numpy() | d.A_AGE.ge(17).to_numpy())
    n_odc = pd.Series(odc_dep).groupby(unit).transform("sum").to_numpy(float)
    lost_unit = np.where(no_ssn_unit, ctc_unit - np.minimum(nonref_unit, ODC * n_odc), 0.0)
    refund_unit = d.ACTC_CRD.groupby(d.TAX_ID).transform("sum").to_numpy(float)
    lost_pc = lost_unit / n_unit
    lost_ref_pc = np.where(no_ssn_unit, refund_unit, 0.0) / n_unit
    gate("ctc_loss_nonnegative", (lost_unit >= -1e-9).all())
    ctc = {"national_row4_bn": float((lost_pc * r4)[civ].sum()) / 1e9,
           "lineage_bn": float((lost_pc * lw)[tgt].sum()) / 1e9,
           "lineage_refundable_bn": float((lost_ref_pc * lw)[tgt].sum()) / 1e9,
           "lineage_units_people_m": float(lw[tgt & no_ssn_unit & (ctc_unit > 0)].sum()) / 1e6}

    # Premium tax credit on each unit's subsidized-Marketplace members.
    curve = age_curve()
    mrks = d.MRKS.eq(1).to_numpy() & civ
    prem = np.where(mrks, d.A_AGE.clip(0, 100).map(curve).to_numpy(float) * BENCHMARK_40 / curve[40] * 12, 0.0)
    prem_unit = pd.Series(prem).groupby(unit).transform("sum").to_numpy()
    enh = np.maximum(prem_unit - applicable(ratio, ENHANCED, False) * np.maximum(agi, 0), 0.0)
    pct_o = applicable(ratio, ORIGINAL, True)
    orig = np.where(np.isnan(pct_o), 0.0, np.maximum(prem_unit - np.nan_to_num(pct_o) * np.maximum(agi, 0), 0.0))
    share_in_unit = np.where(prem_unit > 0, prem / np.where(prem_unit > 0, prem_unit, 1), 0.0)
    enh_p, orig_p = enh * share_in_unit, orig * share_in_unit
    gate("ptc_original_le_enhanced", (orig_p <= enh_p + 1e-6).all())
    nat_enh, nat_orig = float((enh_p * r4)[civ].sum()), float((orig_p * r4)[civ].sum())
    lin_enh, lin_orig = float((enh_p * lw)[tgt].sum()), float((orig_p * lw)[tgt].sum())
    mts = json.loads(MTS.read_text())
    lin_person_share = float(lw[tgt & mrks].sum() / r4[civ & mrks].sum())
    ptc = {"modelled_national_enhanced_bn": nat_enh / 1e9, "modelled_national_original_bn": nat_orig / 1e9,
           "modelled_enhanced_fraction_national": 1 - nat_orig / nat_enh,
           "modelled_enhanced_fraction_lineage": 1 - lin_orig / lin_enh,
           "lineage_share_of_enhancement_dollars": (lin_enh - lin_orig) / (nat_enh - nat_orig),
           "lineage_share_of_enhanced_credit_dollars": lin_enh / nat_enh,
           "lineage_share_of_mrks_persons": lin_person_share,
           "account_ptc_bn": mts["lines"]["ptc"]["cy2024_bn"],
           "account_lineage_ptc_person_key_bn": mts["lines"]["ptc"]["cy2024_bn"] * lin_person_share}

    # Shares of each eligibility class: (numerator lineage weights, denominator row 4), unit weights per person.
    def share(mask, wt=None):
        u = np.ones(len(d)) if wt is None else wt
        den = float((u * r4)[mask].sum())
        num = float((u * lw)[mask & tgt].sum())
        return (num / den if den > 0 else float("nan")), int(mask.sum()), den
    snap_p = (d.HFDVAL > 0).to_numpy() & civ
    mcaid_p = (d.MCAID.eq(1) | d.PCHIP.eq(1)).to_numpy() & civ
    mcare_p = d.MCARE.eq(1).to_numpy() & civ
    lp = noncit & ~kept & ~unauth          # lawfully present noncitizens by the residual rules
    classes = {
        "snap_10108": {"broad": snap_p & lp, "narrow": snap_p & lp & recent},
        "medicaid_71109": {"broad": mcaid_p & lp, "narrow": mcaid_p & lp & recent},
        "medicare_71201": {"broad": mcare_p & lp, "narrow": mcare_p & lp & recent},
        # Marketplace is no residual rule: a noncitizen with subsidized coverage whom the rules leave unauthorized is
        # most plausibly a parolee, TPS holder or applicant, so §71301's classes do not condition on the flag.
        "ptc_eligible_aliens_71301": {"broad": mrks & noncit & ~kept, "narrow": mrks & noncit & ~kept & recent},
        "ptc_below_100_71302": {"broad": mrks & noncit & ~kept & (ratio < 1.0),
                                "narrow": mrks & noncit & ~kept & (ratio < 1.0) & recent},
        "emergency_fmap_71110": {
            "broad": (unauth | (noncit & ~kept & d.PEINUSYR.ge(27).to_numpy())) & expansion & (ratio <= 1.38)
            & d.A_AGE.between(19, 64).to_numpy(),
            "narrow": unauth & expansion & (ratio <= 1.38) & d.A_AGE.between(19, 64).to_numpy()},
    }
    weights = {"ptc_eligible_aliens_71301": orig_p, "ptc_below_100_71302": orig_p}
    share_rows, shares = [], {}
    for k, cls in classes.items():
        for which, mask in cls.items():
            sh, n, den = share(mask, weights.get(k))
            gate(f"{k}_{which}_share_in_unit_interval", 0 <= sh < 1 and n > 0, share=sh, n=n)
            shares.setdefault(k, {})[which] = sh
            share_rows.append({"row": k, "class": which, "records": n, "population_or_dollars_row4": round(den),
                               "lineage_share": round(sh, 6),
                               "unit": "original-law PTC $" if k in weights else "persons"})

    law, ctx = law_scores()
    ext = extension_cost()
    defl, cpi = deflators()
    pc = json.loads(PUBLIC_CHARGE.read_text())["rates"]

    rows = []
    for fy in FYS:
        f = defl[fy]
        def add(item, national_bn, share_c, share_lo, share_hi, consolidated=True, note=""):
            lo, hi = sorted((share_lo, share_hi))
            rows.append({"fy": fy, "item": item, "national_fy_nominal_bn": round(national_bn, 4),
                         "lineage_share": round(share_c, 6),
                         "lineage_2024usd_bn": round(national_bn * share_c * f, 4),
                         "lineage_low_bn": round(national_bn * lo * f, 4),
                         "lineage_high_bn": round(national_bn * hi * f, 4),
                         "consolidated_government": consolidated, "note": note})
        for k in ("snap_10108", "medicaid_71109", "medicare_71201"):
            nat = -law[k]["outlays"][fy] / 1e3
            add(k, nat, shares[k]["narrow"], shares[k]["narrow"], shares[k]["broad"])
        for k in ("ptc_eligible_aliens_71301", "ptc_below_100_71302"):
            nat = (-law[k]["outlays"][fy] + law[k]["revenues"][fy]) / 1e3
            add(k, nat, shares[k]["narrow"], shares[k]["narrow"], shares[k]["broad"],
                note="outlay and revenue parts of the credit; CBO baseline at original-law credits")
        nat = -law["emergency_fmap_71110"]["outlays"][fy] / 1e3
        add("emergency_fmap_71110", nat, shares["emergency_fmap_71110"]["narrow"],
            shares["emergency_fmap_71110"]["narrow"], shares["emergency_fmap_71110"]["broad"], consolidated=False,
            note="federal-to-state shift; zero for consolidated government unless states cut coverage")
        # (a7) the CTC rule, measured in 2024 dollars at 2024 credit amounts; on-books share as the account's tax block.
        rows.append({"fy": fy, "item": "ctc_taxpayer_ssn_70104b", "national_fy_nominal_bn": "",
                     "lineage_share": round(ctc["lineage_bn"] / ctc["national_row4_bn"], 6),
                     "lineage_2024usd_bn": round(ctc["lineage_bn"] * ON_BOOKS[1] * NO_WORK_SSN[1], 4),
                     "lineage_low_bn": round(ctc["lineage_bn"] * ON_BOOKS[0] * NO_WORK_SSN[0], 4),
                     "lineage_high_bn": round(ctc["lineage_bn"] * ON_BOOKS[2] * NO_WORK_SSN[2], 4),
                     "consolidated_government": True,
                     "note": "CPS tax-model credits of units whose filers are all imputed unauthorized x on-books "
                             "0.44/0.60/0.75 x no work-authorized SSN 0.80/0.90/1.00"})
        # (b) enhanced PTC expiry: CBO's extension cost x the lineage's share of enhancement dollars (central) or of
        # enhanced credit dollars (high: if the dynamic loss tracks whole credits of those who drop coverage).
        add("ptc_enhanced_expiry", ext[fy] / 1e3, ptc["lineage_share_of_enhancement_dollars"],
            ptc["lineage_share_of_enhancement_dollars"], ptc["lineage_share_of_enhanced_credit_dollars"],
            note="CBO 61734 permanent-extension cost, post-P.L. 119-21 baseline")
        # (c) the public-charge rule: DHS dollars (no deflation applied; DHS's RIA prices one steady-state year).
        rows.append({"fy": fy, "item": "public_charge_2026_rule", "national_fy_nominal_bn":
                     round(pc["10.3%"]["combined_matched_only_bn"], 4),
                     "lineage_share": round(pc["10.3%"]["lineage_weights"]["dollar_weighted_share"], 6),
                     "lineage_2024usd_bn": round(pc["10.3%"]["lineage_weights"]["combined_bn"], 4),
                     "lineage_low_bn": round(pc["3.3%"]["lineage_weights"]["combined_bn"], 4),
                     "lineage_high_bn": round(pc["17.3%"]["lineage_weights"]["combined_bn"], 4),
                     "consolidated_government": True, "note": "public_charge_share_2026_10_07, DHS 3.3/10.3/17.3%"})

    # Overlaps. (1) (b) is priced on the post-(a) baseline, (a)'s PTC rows on original-law credits: the enhancement
    # on (a)'s people falls between them and is added back, at the (a) classes' own modelled enhanced/original ratio.
    # (2) Public charge x (a): people who lose SNAP or Medicaid eligibility under (a) cannot also disenroll; bounded by
    # DHS's rate times (a)'s lineage SNAP + Medicaid dollars.
    for fy in FYS:
        R = {r["item"]: r for r in rows if r["fy"] == fy}
        bridge = {}
        for k in ("ptc_eligible_aliens_71301", "ptc_below_100_71302"):
            m = classes[k]["narrow"]
            e, o = float((enh_p * lw)[m & tgt].sum()), float((orig_p * lw)[m & tgt].sum())
            bridge[k] = R[k]["lineage_2024usd_bn"] * (e / o - 1) if o > 0 else 0.0
        rows.append({"fy": fy, "item": "overlap_bridge_enhancement_on_a_ptc_classes", "national_fy_nominal_bn": "",
                     "lineage_share": "", "lineage_2024usd_bn": round(sum(bridge.values()), 4),
                     "lineage_low_bn": round(sum(bridge.values()), 4), "lineage_high_bn": round(sum(bridge.values()), 4),
                     "consolidated_government": True, "note": "adds the enhancement on (a)'s PTC classes"})
        a_pc = R["snap_10108"]["lineage_2024usd_bn"] + R["medicaid_71109"]["lineage_2024usd_bn"]
        rows.append({"fy": fy, "item": "overlap_public_charge_x_a", "national_fy_nominal_bn": "",
                     "lineage_share": "", "lineage_2024usd_bn": round(-0.103 * a_pc, 4),
                     "lineage_low_bn": round(-0.173 * a_pc, 4), "lineage_high_bn": round(-0.033 * a_pc, 4),
                     "consolidated_government": True, "note": "DHS rate x (a)'s lineage SNAP + Medicaid cut"})

    summary = {"lane": "post2024_law_2026_10_07", "deflator_cy2024_per_fy_dollar": defl, "cpi_u_growth": cpi,
               "lineage_m": float(lw[tgt].sum()) / 1e6, "added_descendants_m": added_m,
               "ctc_rule_measured": ctc, "ptc_model": ptc, "shares": shares, "totals": {}}
    for fy in FYS:
        R = [r for r in rows if r["fy"] == fy]
        tot = {k: sum(float(r[k]) for r in R) for k in ("lineage_2024usd_bn", "lineage_low_bn", "lineage_high_bn")}
        cons = {k: sum(float(r[k]) for r in R if r["consolidated_government"])
                for k in ("lineage_2024usd_bn", "lineage_low_bn", "lineage_high_bn")}
        summary["totals"][fy] = {"with_emergency_fmap_shift": tot, "consolidated_government": cons}
    ctx_rows = []
    lin_share_ctx = {"medicaid_work_requirements_71119": share(mcaid_p & expansion & d.A_AGE.between(19, 64).to_numpy()
                                                               & ~noncit)[0],
                     "snap_work_requirements_10102": share(snap_p & d.A_AGE.between(18, 64).to_numpy())[0],
                     "snap_state_match_10105": share(snap_p)[0],
                     "ptc_verification_71303": lin_person_share, "ptc_special_enrollment_71304": lin_person_share,
                     "ptc_recapture_71305": lin_person_share}
    for k, v in ctx.items():
        ctx_rows.append({"item": k, "cbo_fy2028_outlays_bn": -v["2028"] / 1e3,
                         "lineage_person_share": round(lin_share_ctx[k], 6),
                         "scale_2024usd_bn": round(-v["2028"] / 1e3 * lin_share_ctx[k] * defl["2028"], 3)})
    summary["context_not_in_arm"] = ctx_rows

    OUT.mkdir(exist_ok=True)
    for name, data in (("rows.csv", rows), ("shares.csv", share_rows), ("context_not_in_arm.csv", ctx_rows)):
        with open(OUT / name, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(data[0]), lineterminator="\n")
            w.writeheader()
            w.writerows(data)
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    for r in rows:
        print(f"  FY{r['fy']} {r['item']:44s} ${float(r['lineage_2024usd_bn']):7.3f}bn "
              f"({float(r['lineage_low_bn']):.3f}-{float(r['lineage_high_bn']):.3f}) share {r['lineage_share']}")
    for fy, t in summary["totals"].items():
        print(f"  ▸ FY{fy}: with the FMAP shift ${t['with_emergency_fmap_shift']['lineage_2024usd_bn']:.2f}bn; consolidated "
              f"${t['consolidated_government']['lineage_2024usd_bn']:.2f}bn "
              f"({t['consolidated_government']['lineage_low_bn']:.2f}-{t['consolidated_government']['lineage_high_bn']:.2f})")
    print(json.dumps({"ctc": ctc, "ptc": ptc}, indent=1))


if __name__ == "__main__":
    main()
