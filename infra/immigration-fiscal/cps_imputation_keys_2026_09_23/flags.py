"""Steps 1-2: allocation flags behind each account key, and the shares imputed.

Shares are weighted with the full ASEC weight; SEs use the 160 successive-difference
replicates. Output: derived/imputation_flags.csv, derived/imputed_shares.csv.
Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/cps_imputation_keys_2026_09_23/flags.py
"""
from __future__ import annotations

import numpy as np
import pandas as pd

import common as c

# Flag semantics quoted from the ASEC 2025 data dictionary (cps_asec_doc/ddl25.txt, cpsmar25.pdf ch. 6).
SEMANTICS = {
    "I_ANNVAL-type (ERN_VAL, WS_VAL, SE_VAL, FRM_VAL, DIV_VAL, RNT_VAL, PAW_VAL, WC_VAL, ...)":
        '"Levels 1-3 indicate imputations use of income range responses and 4-8 indicate imputations '
        'without range responses. Within each group, lower numbers indicate more match variables (and better '
        'matches)." 7 = "Level 104 statistical match (age, sex)"; 8 = "Level 105 statistical match (all donors '
        'can match to all recipients)"; 9 = "FL_665 ≠ 1 (full record impute)".',
    "Composite value flags (I_INTVAL, I_UCVAL, I_SSVAL, I_SSIVAL, I_VETVAL)":
        '"Imputation for non-response was conducted on the component variables." 11-14 = value imputed is '
        '<25%, 25-50%, 50-75%, 75-100% of the composite; 15 = "Value is 100% imputed in composite variable".',
    "Composite recipiency flags (I_INTYN, I_UCYN, I_SSYN, I_SSIYN, I_DSTYNCOMP)":
        '10 = "Some of the components are imputed"; 11 = "All of the components imputed".',
    "FL_665": '"Supplement Interview Status": 0 = "Complete nonresponse to supplement", 1 = "Supplement '
              'interview", 2 = "Some supplement response but not enough for interview", 3 = "Supplement '
              'interview but not enough income data".',
    "I_MCARE, I_MCAID, I_MOOP": '0 = "Reported", 1 = "Hotdeck imputation", 2 = "Logical imputation", 3 = "Whole '
                                'unit imputation".',
    "Household flags (I_HFOODS, I_HFDVAL, I_HPUBLI, I_HLOREN, I_HFLUNC, I_HENGAS, I_HENGVA)":
        '0 = "No allocation", 1 = "Allocated" (I_HFDVAL, I_HENGVA also 2 = "Allocated with range response").',
    "WICYNA": '"Allocation flag for WICYN": 0 = "Not allocated or NIU", 1 = "Allocated".',
    "PXNATVTY, PXMNTVTY, PXFNTVTY, PXHSPNON, PRCITFLG":
        '00 = "Not allocated"; 10-13 edited to a value; 20-23 longitudinal value; 40-43 allocated value.',
}


def ratio_reps(num, den):
    return num / den


def main():
    d = c.load_frame()
    civ, union = c.masks(d)
    other = civ & ~union
    W = d[c.REPS].to_numpy(float)
    ks, s, mat = c.key_status(d)
    s.update({"tax_unit_material_5pct": mat["tax_unit"], "spm_unit_material_5pct": mat["spm_unit"],
              "spm_resources": ks["shared"]["consumption"]})
    for thr, label in [(0.01, "1pct"), (None, "anyflag")]:
        _, _, m2 = c.key_status(d, thr)
        s[f"tax_unit_material_{label}"] = m2["tax_unit"]
        s[f"spm_unit_material_{label}"] = m2["spm_unit"]
    adult15 = d.A_AGE.ge(15).to_numpy()
    full = d.FL_665.ne(1).to_numpy()

    rows = []

    def add(item, measure, universe, flag, amount=None, note=""):
        for_rep = {}
        for gname, g in [("union", union), ("other", other)]:
            m = g & universe
            if amount is None:
                num, den = (flag[m, None] * W[m]).sum(0), W[m].sum(0)
            else:
                v = np.abs(amount)
                num, den = ((v * flag)[m, None] * W[m]).sum(0), (v[m, None] * W[m]).sum(0)
            rep = num / den
            for_rep[gname] = rep
            rows.append(dict(item=item, measure=measure, group=gname, estimate=rep[0], se=c.sdr(rep),
                             n_unweighted=int(m.sum()), n_flagged=int((m & flag.astype(bool)).sum()), note=note))
        diff = for_rep["union"] - for_rep["other"]
        rows.append(dict(item=item, measure=measure, group="union_minus_other", estimate=diff[0], se=c.sdr(diff),
                         n_unweighted=np.nan, n_flagged=np.nan, note=note))

    print("[flags] whole-supplement and item shares", flush=True)
    add("whole_supplement", "persons_15plus", civ & adult15, full & adult15, note="FL_665 != 1")
    add("whole_supplement", "persons_all_ages", civ, full, note="FL_665 != 1, children follow their household")
    for item in c.ITEMS:
        amount = c.item_amount(d, item)
        add(item, "persons_15plus", civ & adult15, s[item])
        add(item, "dollars", civ & adult15, s[item], amount)
        add(item, "dollars_whole_supplement_only", civ & adult15, s[item] & full, amount)
        add(item, "dollars_item_level_only", civ & adult15, s[item] & ~full, amount)
    # Earnings from the longest job by hot-deck level (I_ERNVAL), dollars.
    ern = d.ERN_VAL.to_numpy(float)
    level = d.I_ERNVAL.to_numpy()
    for label, codes in [("range_levels_1_3", [1, 2, 3]), ("no_range_levels_101_103", [4, 5, 6]),
                         ("age_sex_or_pooled_104_105", [7, 8]), ("whole_supplement_9", [9])]:
        add("earnings_longest_job", f"dollars_level_{label}", civ & adult15, np.isin(level, codes), ern,
            note="I_ERNVAL level; ERN_VAL includes wage and self-employment sources")
    for item, universe in [("medicare", civ), ("medicare_logical", civ), ("medicaid", civ),
                           ("medicaid_logical", civ), ("snap", civ), ("housing", civ), ("school_lunch", civ),
                           ("energy", civ), ("wic_person", civ), ("property_value", civ & d.H_TENURE.eq(1).to_numpy()),
                           ("moop", civ)]:
        add(item, "persons", universe, s[item])
    for item, col in [("snap", "SPM_SNAPSUB"), ("housing", "SPM_CAPHOUSESUB"), ("energy", "SPM_ENGVAL"),
                      ("school_lunch", "SPM_SCHLUNCH")]:
        add(item, "dollars", civ, s[item], d[col].to_numpy(float))
    add("wic_unit", "dollars", civ, c.unit_any(s["wic_person"], d.SPM_ID.to_numpy()), d.SPM_WICVAL.to_numpy(float))
    add("property_value", "dollars", civ & d.H_TENURE.eq(1).to_numpy(), s["property_value"], d.HPROP_VAL.to_numpy(float))
    for label in ["5pct", "1pct", "anyflag"]:
        add(f"tax_unit_material_{label}", "persons", civ, s[f"tax_unit_material_{label}"])
        add(f"tax_unit_material_{label}", "dollars_federal_liability", civ, s[f"tax_unit_material_{label}"],
            d.FEDTAX_BC.to_numpy(float))
        add(f"tax_unit_material_{label}", "dollars_refundable_credits", civ, s[f"tax_unit_material_{label}"],
            (d.EIT_CRED + d.ACTC_CRD).to_numpy(float))
        add(f"tax_unit_material_{label}", "dollars_state_liability", civ, s[f"tax_unit_material_{label}"],
            d.STATETAX_A.clip(lower=0).to_numpy(float))
    add("spm_resources", "persons", civ, s["spm_resources"])
    add("spm_resources", "dollars", civ, s["spm_resources"], d.SPM_RESOURCES.clip(lower=0).to_numpy(float))
    print("[flags] union-definition allocation", flush=True)
    for f in ["PXNATVTY", "PXMNTVTY", "PXFNTVTY", "PXHSPNON", "PRCITFLG"]:
        add(f"definition_{f}", "persons", civ, d[f].to_numpy() >= 10, note="codes 10+: edited or allocated")
    out = pd.DataFrame(rows)
    out.to_csv(c.OUT / "imputed_shares.csv", index=False)
    doc = [dict(item=i, flags=";".join(f), value_columns=";".join(v), account_keys=k)
           for i, (f, v, k) in c.ITEMS.items()]
    doc += [dict(item="whole_supplement", flags="FL_665", value_columns="all supplement items", account_keys="all"),
            dict(item="medicare", flags="I_MCARE (1,3 donor; 2 logical)", value_columns="MCARE", account_keys="medicare, medicare_income"),
            dict(item="medicaid", flags="I_MCAID (1,3 donor; 2 logical)", value_columns="MCAID", account_keys="medicaid_covered (alternative key only)"),
            dict(item="snap", flags="I_HFOODS;I_HFDVAL;I_HFOODM;I_HFOODN", value_columns="SPM_SNAPSUB", account_keys="snap"),
            dict(item="housing", flags="I_HPUBLI;I_HLOREN", value_columns="SPM_CAPHOUSESUB", account_keys="housing_support"),
            dict(item="school_lunch", flags="I_HFLUNC;I_HFLUNN", value_columns="SPM_SCHLUNCH", account_keys="none in the complete account; SPM resources"),
            dict(item="energy", flags="I_HENGAS;I_HENGVA", value_columns="SPM_ENGVAL", account_keys="energy"),
            dict(item="wic", flags="WICYNA", value_columns="SPM_WICVAL", account_keys="wic"),
            dict(item="eitc_inputs_and_tax", flags="members' earnings and income flags, FL_665 (tax unit TAX_ID)",
                 value_columns="FEDTAX_BC;STATETAX_A;EIT_CRED;ACTC_CRD (Census tax model)",
                 account_keys="federal_liability, state_liability, refundable_credits"),
            dict(item="spm_resources", flags="members' income flags, household noncash flags, WICYNA, I_MOOP, I_CHCAREVAL",
                 value_columns="SPM_RESOURCES", account_keys="consumption, resources"),
            dict(item="property_value", flags="I_PROPVAL", value_columns="HPROP_VAL", account_keys="modeled_owner_property (response 0)")]
    pd.DataFrame(doc).to_csv(c.OUT / "imputation_flags.csv", index=False)
    pd.DataFrame([dict(flag=k, dictionary_text=v) for k, v in SEMANTICS.items()]).to_csv(
        c.OUT / "flag_semantics.csv", index=False)
    show = out.query("group != 'union_minus_other'").pivot_table(index=["item", "measure"], columns="group",
                                                                  values="estimate")
    print(show.round(3).to_string(), flush=True)


if __name__ == "__main__":
    main()
