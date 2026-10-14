#!/usr/bin/env python3
"""Child credits that cross the group's boundary in mixed tax units: what the personal allocation misses.

Main case v7 takes the group's total at the personal allocation, which charges a tax or credit to the record the survey
puts it on. The Census tax model puts all of a return's amounts on one record: the tax unit's head, or a dependent
filer. A joint return's spouse carries zeros (gate `one_record_per_return`). A removal of the group ends the credits a
non-member head claims for member children, and the personal allocation charges them to no one. It also leaves in
place the non-member children a member head claims, and the personal allocation charges their credits to the group.
This script prices both on CPS ASEC 2025 tax units (income year 2024) and states the filing-status effects beside them.

Rules. The script first reproduces the Census tax model's credits on every actual return from the 2024 schedule
(derived/validation.csv; the gates stop the run below the stated fit):
  child tax credit and credit for other dependents, nonrefundable part (CTC_CRD): $2,000 per dependent under 17 and
    $500 per other dependent, less $50 per $1,000 (or part) of AGI over $400,000 joint / $200,000 otherwise, limited
    to the tax before it, T0 = FEDTAX_BC + CTC_CRD (Schedule 8812 (2024) lines 4-14);
  refundable part (ACTC_CRD): the unused credit, at most $1,700 per child under 17 and 15% of wages plus
    self-employment income over $2,500 (Rev. Proc. 2023-34 section 3.05; Schedule 8812 lines 16a-20);
  EITC (EIT_CRED): section 32's percentages with Rev. Proc. 2023-34 section 3.06's amounts. Qualifying children are
    dependents under 19 or students under 24, earned income is net of half the self-employment tax, investment
    income is limited to $11,600, and the childless credit applies at ages 25-64;
  child and dependent care credit (inside T0): the household's child care spending (HCHCARE_VAL), at most $3,000 /
    $6,000 for one / two or more dependents under 13, at 35% less one point per $2,000 (or part) of AGI over $15,000,
    floor 20%. This is Form 2441 (2024) line 8, except that the Census model takes the lower rate at exact multiples.
    The credit is limited to the lower earner's earnings when both spouses work.
A return's dependents are the persons whose DEP_STAT names its head. Head-of-household status is an unmarried head
with a dependent: the Census model's rule, gated.

Counterfactuals per return. Each counterfactual credit is the Census credit plus the rule's change, floored at 0.
The tax before credits moves only by the rate schedule's change:
  A  non-member head: the return without its member dependents, filing status and incomes held;
  B  member head: the return without its non-member dependents, held likewise. Whether the child's credit continues
     after the member claimant leaves is a reading: R1 all of it, R2 only where the claimant's non-member spouse
     remains, R3 where that spouse or a non-member parent of the child lives in the household;
  C  non-member head of household whose dependents are all members: single status after the removal; Cr, the
     reverse, a member head of household whose dependents are all non-members, read as B;
  D  joint returns of a member and a non-member: the non-member spouse's own return, at that spouse's share of the
     return's income (rate-schedule model, no Census anchor beyond that share), single or head of household with the
     non-member dependents.
Generations: A and C follow the member dependents removed (split equally), B and Cr the member head, D the member
spouse.

Frame and keys follow the case. The group is the receipts builder's union of civilians. Weights are audit row 4's
(world_ledger_2026_09_27/population_basis.py reweight; replicates raked column by column to the same ACS totals).
The status rule is the adopted stack's state-aware flag with its on-books shares (cps_imputation_keys_2026_09_23
combine_onbooks_lane): an imputed unauthorized head's EITC counts at 0 and the rest of the return at the on-books
share. Account dollars: refundable parts go on the non-PTC part of the refundable_tax_credits line (NON_PTC x hf per
CPS dollar of the national key); tax parts go on the federal_income_tax line through v4 item 3's IRS-raked key, at
the ratio of each return's cell (tax_key_heldout_2026_09_28/keys.py), over the key's mass on row 4's weights. Sign:
positive raises the group's net cost.

Writes derived/terms.csv, derived/validation.csv, derived/example.json and derived/summary.json. From the repository
root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/mixed_unit_credits_2026_10_14/credits.py
"""
from __future__ import annotations

import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
ROOT = FISCAL.parents[1]
OUT = LANE / "derived"
CPS_ZIP = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
MTS = FISCAL / "dataset_integrity_2026_09_23/derived/spending_mts_credits.json"
STORED_STACK = FISCAL / "backtest_admin_totals_2026_09_28/derived/prediction_audit.json"
REPS = [f"pwwgt{i}" for i in range(161)]
PERSON = ["PH_SEQ", "PPPOS", "A_LINENO", "TAX_ID", "DEP_STAT", "FILESTAT", "PEPAR1", "PEPAR2", "A_AGE", "PRPERTYP",
          "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "A_ENRLW", "MARSUPWT", "AGI", "TAX_INC",
          "FEDTAX_BC", "FEDTAX_AC", "CTC_CRD", "ACTC_CRD", "EIT_CRED", "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "INT_VAL",
          "DIV_VAL", "RNT_VAL", "CAP_VAL", "UC_VAL", "PNSN_VAL", "ANN_VAL", "SS_VAL", "STATETAX_B", "STATETAX_A", "SPM_ID"]
TAX_FIELDS = ["AGI", "TAX_INC", "FEDTAX_BC", "FEDTAX_AC", "CTC_CRD", "ACTC_CRD", "EIT_CRED"]
GENS = ("G1", "G2", "G3+")

# Tax year 2024. Rev. Proc. 2023-34 (sha256 544ba41c7ba64f77da521e0d174a7b7394dc72b5c7c73d10adb19952d5aaae57):
# section 3.01 tables 1-3, 3.05, 3.06, 3.15. Schedule 8812 (2024) (8b5143ca...f977) and Form 2441 (2024)
# (aaaf70ba...f4df7) for the child and care credits; test_credits.py checks these numbers against the cached texts.
BRACKETS = {"joint": [23200, 94300, 201050, 383900, 487450, 731200],
            "hoh": [16550, 63100, 100500, 191950, 243700, 609350],
            "single": [11600, 47150, 100525, 191950, 243725, 609350]}
RATES = [.10, .12, .22, .24, .32, .35, .37]
STD = {"joint": 29200.0, "hoh": 21900.0, "single": 14600.0}
AGED = {"joint": 1550.0, "hoh": 1950.0, "single": 1950.0}        # per person 65 or older
# children: (credit %, phase-out %) from section 32(b)(1); (earned income amount, maximum credit, threshold other,
# threshold joint) from Rev. Proc. 2023-34 section 3.06(1)
EITC = {0: (.0765, .0765, 8260, 632, 10330, 17250), 1: (.34, .1598, 12390, 4213, 22720, 29640),
        2: (.40, .2106, 17400, 6960, 22720, 29640), 3: (.45, .2106, 17400, 7830, 22720, 29640)}
EITC_COMPLETED = {0: (18591, 25511), 1: (49084, 56004), 2: (55768, 62688), 3: (59899, 66819)}   # other, joint
EITC_INVESTMENT = 11600.0
CTC_CHILD, CTC_OTHER, CTC_STEP = 2000.0, 500.0, 50.0
CTC_THRESHOLD = {"joint": 400000.0, "other": 200000.0}
ACTC_MAX, ACTC_RATE, ACTC_FLOOR = 1700.0, 0.15, 2500.0
CDCC_CAP = (3000.0, 6000.0)
SS_BASE = {"joint": (32000.0, 44000.0, 6000.0), "other": (25000.0, 34000.0, 4500.0)}   # 26 U.S.C. 86(c), (a)(2)
OASDI_MAX = 168600.0

GATES: list[dict] = []


def gate(name, ok, value=None, **detail):
    """Stop the run on a failed check; record a passed one with its measured value (or its detail) for item.json."""
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {value if value is not None else detail}")
    GATES.append(dict(name=name, passed=True, value=value if value is not None else (detail or True)))
    print(f"  ✓ {name}", flush=True)


def sha(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def sdr(x: np.ndarray) -> float:
    """160-replicate successive-difference SE, as the account's generator."""
    x = np.asarray(x, float)
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def by_path(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ---------------------------------------------------------------------------------------------------------------------
# 2024 rules
# ---------------------------------------------------------------------------------------------------------------------
def schedule(taxable, status):
    """Regular tax on taxable income by filing status (Rev. Proc. 2023-34 section 3.01)."""
    taxable = np.asarray(taxable, float)
    tax = np.zeros(len(taxable))
    for s, bounds in BRACKETS.items():
        m = status == s
        prev = 0.0
        for rate, upper in zip(RATES, bounds + [np.inf]):
            tax[m] += rate * np.clip(taxable[m] - prev, 0, upper - prev)
            prev = upper
    return tax


def half_se_tax(se, wages):
    """Half the self-employment tax: 92.35% of net earnings, OASDI up to the wage base left after wages, $400 floor."""
    base = np.maximum(np.asarray(se, float), 0) * 0.9235
    oasdi = np.minimum(base, np.maximum(OASDI_MAX - np.maximum(wages, 0), 0))
    return np.where(base >= 400, (0.124 * oasdi + 0.029 * base) / 2, 0.0)


def child_credits(status, agi, t0, earned, k17, other):
    """Schedule 8812 (2024): the nonrefundable credit (line 14) and the additional child tax credit (line 27, without
    the three-child payroll-tax alternative, which the Census model does not apply)."""
    threshold = np.where(status == "joint", CTC_THRESHOLD["joint"], CTC_THRESHOLD["other"])
    reduction = CTC_STEP * np.ceil(np.maximum(agi - threshold, 0) / 1000)
    total = np.maximum(CTC_CHILD * k17 + CTC_OTHER * other - reduction, 0)
    nonref = np.minimum(total, np.maximum(t0, 0))
    actc = np.minimum(np.minimum(total - nonref, ACTC_MAX * k17), ACTC_RATE * np.maximum(earned - ACTC_FLOOR, 0))
    return nonref, np.maximum(actc, 0)


def eitc(kids, earned, agi, joint, investment, age_ok):
    """Section 32 with Rev. Proc. 2023-34 section 3.06: the phase-in on earned income, capped at the maximum, and the
    phase-out on the greater of AGI and earned income."""
    k = np.minimum(kids, 3)
    out = np.zeros(len(k))
    for n, (pin, pout, _amount, maximum, th_other, th_joint) in EITC.items():
        m = k == n
        th = np.where(joint, th_joint, th_other)
        income = np.maximum(agi, earned)
        credit = np.minimum(np.minimum(pin * np.maximum(earned, 0), maximum), maximum - pout * np.maximum(income - th, 0))
        credit = np.maximum(credit, 0)
        if n == 0:
            credit = np.where(age_ok, credit, 0)
        out[m] = credit[m]
    return np.where(investment > EITC_INVESTMENT, 0.0, out)


def care_credit(agi, k13, care, limit, tax):
    """Form 2441 (2024) lines 3-11 as the Census model applies them (rate one point lower at exact $2,000 steps)."""
    steps = np.where(agi > 15000, np.floor((agi - 15000) / 2000) + 1, 0)
    rate = np.maximum(0.35 - 0.01 * steps, 0.20)
    cap = np.where(k13 >= 2, CDCC_CAP[1], np.where(k13 == 1, CDCC_CAP[0], 0.0))
    spent = np.minimum(np.minimum(np.maximum(care, 0), cap), np.maximum(limit, 0))
    return np.minimum(rate * spent, np.maximum(tax, 0))


def taxable_ss(other_income, benefits, joint):
    """26 U.S.C. 86: the taxable part of Social Security benefits from provisional income."""
    b1 = np.where(joint, SS_BASE["joint"][0], SS_BASE["other"][0])
    b2 = np.where(joint, SS_BASE["joint"][1], SS_BASE["other"][1])
    cap = np.where(joint, SS_BASE["joint"][2], SS_BASE["other"][2])
    prov = other_income + 0.5 * benefits
    tier1 = np.minimum(0.5 * benefits, 0.5 * np.maximum(prov - b1, 0))
    tier2 = np.minimum(0.85 * benefits, 0.85 * np.maximum(prov - b2, 0) + np.minimum(0.5 * benefits, cap))
    return np.where(prov <= b2, tier1, tier2) * (benefits > 0)


# ---------------------------------------------------------------------------------------------------------------------
# Frame
# ---------------------------------------------------------------------------------------------------------------------
def load() -> pd.DataFrame:
    got = sha(CPS_ZIP)
    gate("cps_source_is_the_accounts", got == CPS_SHA, value=got)
    with zipfile.ZipFile(CPS_ZIP) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=PERSON)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS", "HCHCARE_VAL"])
        w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", *REPS])
    d = d.merge(w.rename(columns={"h_seq": "PH_SEQ"}), on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    del w
    gate("replicates_join_every_person", not bool(d[REPS].isna().any().any()))
    gate("full_weight_is_marsupwt", (x := float((d.MARSUPWT / 100 - d.pwwgt0).abs().max())) < .01, value=x)
    d = d.merge(hh, left_on="PH_SEQ", right_on="H_SEQ", how="left", validate="many_to_one")
    gate("every_person_has_a_household", not bool(d.H_SEQ.isna().any()))
    gate("refundable_credit_identity",
         (x := float((d.FEDTAX_AC - (d.FEDTAX_BC - d.ACTC_CRD - d.EIT_CRED)).abs().max())) == 0, value=x)
    return d.sort_values(["PH_SEQ", "PPPOS"]).reset_index(drop=True)


def groups(d):
    """The receipts builder's union of civilians and its generations (full_account_spending builder canonical_target)."""
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3])
    us = [57, 60, 66, 69, 73, 78]
    g1 = (d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)).to_numpy() & civ
    g2 = (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303))).to_numpy() & civ
    g3 = (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)).to_numpy() & civ
    gen = np.select([g1, g2, g3], [0, 1, 2], -1)
    return civ, gen >= 0, gen


def row4_weights(d, civ, union):
    """Audit row 4: population_basis.reweight for the full weight; the 160 replicates raked to the same ACS totals
    column by column, as production_row4.json describes them."""
    sys.path.insert(0, str(FISCAL / "world_ledger_2026_09_27"))
    import population_basis as pb
    frame = pd.DataFrame({"PH_SEQ": d.PH_SEQ.to_numpy(), "PENATVTY": d.PENATVTY.to_numpy(),
                          "PRCITSHP": d.PRCITSHP.to_numpy(), "PEFNTVTY": d.PEFNTVTY.to_numpy(),
                          "PEMNTVTY": d.PEMNTVTY.to_numpy(), "civ": civ, "target": union,
                          "pw": d.pwwgt0.to_numpy(float)})
    r4 = pb.reweight(frame, CPS_ZIP, gate, "row4")
    W = d[REPS].to_numpy(float)
    outside = ~d.GESTFIPS.isin(pb.KEEP).to_numpy()
    meta = pb.row4()["row4_factors"]
    ranges = {}
    for label, code in pb.STATUS.items():
        m = d.PENATVTY.eq(pb.MEXICO).to_numpy() & d.PRCITSHP.eq(code).to_numpy() & outside
        f = meta[label]["acs_population"] / W[m].sum(axis=0)
        W[m] *= f
        ranges[label] = (float(f[1:].min()), float(f[1:].max()))
        gate(f"row4_replicate_factors_are_production_row4s_{label}",
             np.allclose(ranges[label], meta[label]["replicate_factor_range"], rtol=0, atol=1e-12),
             got=ranges[label], want=meta[label]["replicate_factor_range"])
    gate("row4_full_column_is_population_basis_reweight", (x := float(np.abs(W[:, 0] - r4.pw.to_numpy()).max())) < 1e-6,
         value=x)
    gate("row4_union_is_39712493", abs((x := float(W[union, 0].sum())) - 39712493.33118789) < 1e-3, value=x)
    g3 = pb.g3plus(frame.assign(pw=W[:, 0]))
    counts = pb.lineage()
    identified = float(W[g3, 0].sum())
    gate("lineage_identified_g3plus_is_the_cases", abs(identified - counts["identified_g3plus"]) < 1e-3, value=identified)
    return W, 1.0 + counts["added"] / identified, counts


def status_flag(d):
    """The adopted stack's state-aware unauthorized flag and on-books shares (row4+status_state_aware, origin case)."""
    sys.path.insert(0, str(FISCAL / "cps_imputation_keys_2026_09_23"))
    import combine_onbooks_lane as L
    import combine_status as cs
    s_in, hh = cs.status_inputs()
    with contextlib.redirect_stderr(io.StringIO()) as note:
        flag = L.state_aware_flag(s_in, hh, d, L.STATUS_BLIND_2024)
    gate("impute_status_still_reports_its_medicaid_caveat", "[DEGRADED]" in note.getvalue())
    configs, labels = L.share_configs(d)
    shares = {case: configs[("origin", case)] for case in ("low", "central", "high")}
    return np.asarray(flag, bool), shares, {case: labels[("origin", case)] for case in shares}


def allocation_check(d, civ, union, model, hf):
    """The review's claim that the personal total equals sharing among members only, on person-level keys, on the
    builders' weights (pwwgt0) and union. Rules: personal (the record's value); shared, the builders' rule (an SPM
    unit's unweighted sum split equally over its persons: full_account_spending_2026_09_20/builder.py:167-169, :241;
    full_account_receipts_2026_09_20/builder.py:120-122); members only, the same rule inside each unit's members,
    civilian non-members and others separately; and both again with a weight-preserving split (each person gets the
    weighted mean of the persons sharing with them). Shares are the group's key over the civilian key."""
    w = d.pwwgt0.to_numpy(float)
    unit = pd.factorize(d.SPM_ID)[0]
    klass = np.where(union, 0, np.where(civ, 1, 2))
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    keys = {"refundable_credits": ("spending", "refundable_tax_credits", (d.EIT_CRED + d.ACTC_CRD).to_numpy(float)),
            "social_security": ("spending", "social_security", d.SS_VAL.to_numpy(float)),
            "federal_liability": ("receipts", "federal_income_tax", d.FEDTAX_BC.to_numpy(float)),
            "wage_oasdi": ("receipts", "employee_oasdi", np.minimum(wage, 168600.0))}

    def split(v, groups, weighted):
        if weighted:
            return (pd.Series(v * w).groupby(groups).transform("sum")
                    / pd.Series(w).groupby(groups).transform("sum")).to_numpy()
        return pd.Series(v).groupby(groups).transform("mean").to_numpy()

    within = unit * 3 + klass
    rows = []
    for name, (side_, line_id, v) in keys.items():
        rules = {"personal": v, "shared": split(v, unit, False), "members_only": split(v, within, False),
                 "shared_weighted": split(v, unit, True), "members_only_weighted": split(v, within, True)}
        sh = {r: float(x[union] @ w[union] / (x[civ] @ w[civ])) for r, x in rules.items()}
        if side_ == "spending":
            line = next(x for x in model["spending"]["lines"] if x["id"] == line_id)
            stored, national = line["keys"][name], line["national_bn"] * hf
        else:
            line = next(x for x in model["receipts"]["lines"] if x["id"] == line_id)
            stored, national = line["cells"][model["receipts"]["reference"]], line["national_bn"]
        for a in ("personal", "shared"):
            gate(f"allocation_check_reproduces_model_jsons_{a}_share_{name}", abs(sh[a] - stored[a]["share"]) < 5e-9,
                 value=dict(got=sh[a], model_json=stored[a]["share"]))
        gate(f"weighted_members_only_sharing_is_the_personal_share_{name}",
             abs(sh["members_only_weighted"] - sh["personal"]) < 1e-12, value=sh["members_only_weighted"])
        rows.append(dict(key=name, side=side_, line=line_id, line_bn=national,
                         **{f"share_{r}": v_ for r, v_ in sh.items()},
                         **{f"{r}_minus_personal_bn": national * (sh[r] - sh["personal"]) for r in sh if r != "personal"}))
    g = pd.Series(w).groupby(unit)
    return pd.DataFrame(rows), float((g.max() > g.min() * (1 + 1e-12)).mean())


# ---------------------------------------------------------------------------------------------------------------------
# Returns
# ---------------------------------------------------------------------------------------------------------------------
def returns(d, union, gen, civ):
    """One row per return: the record carrying the Census tax fields (a head or a dependent filer), its spouse on a
    joint return, and counts of the dependents whose DEP_STAT names it, by membership."""
    carrier = d[TAX_FIELDS].ne(0).any(axis=1).to_numpy()
    dep = d.DEP_STAT.gt(0).to_numpy()
    joint_fs = d.FILESTAT.isin([1, 2, 3]).to_numpy()
    nondep = ~dep
    per_unit = pd.Series(carrier & nondep).groupby(d.TAX_ID.to_numpy()).sum()
    filers = pd.Series(nondep & d.FILESTAT.isin([1, 2, 3, 4, 5]).to_numpy()).groupby(d.TAX_ID.to_numpy()).sum()
    gate("one_record_per_return", int(per_unit.max()) == 1, max=int(per_unit.max()))
    jt = pd.Series(nondep & joint_fs).groupby(d.TAX_ID.to_numpy()).sum()
    gate("joint_units_hold_exactly_two_filers", set(jt[jt > 0].unique()) == {2}, value=sorted(map(int, jt[jt > 0].unique())))
    gate("filers_without_amounts_are_joint_spouses_only",
         bool(((nondep & d.FILESTAT.isin([1, 2, 3, 4, 5]).to_numpy() & ~carrier) <= joint_fs).all()))
    gate("every_unit_with_a_filer_has_one_carrier", bool((per_unit[filers > 0] == 1).all()))
    rows = np.flatnonzero(carrier)
    n = len(rows)
    key = pd.Series(np.arange(n), index=pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy()[rows],
                                                                   d.A_LINENO.to_numpy()[rows]]))
    # spouse: the other FILESTAT 1-3 non-dependent of a joint head's tax unit
    head_joint = joint_fs[rows] & nondep[rows]
    spouse_rows = np.flatnonzero(nondep & joint_fs & ~carrier)
    sp_by_unit = pd.Series(spouse_rows, index=d.TAX_ID.to_numpy()[spouse_rows])
    gate("one_spouse_per_joint_unit", not bool(sp_by_unit.index.duplicated().any()))
    spouse = np.full(n, -1)
    spouse[head_joint] = sp_by_unit.reindex(d.TAX_ID.to_numpy()[rows][head_joint]).fillna(-1).astype(int).to_numpy()
    gate("every_joint_head_has_a_spouse", bool((spouse[head_joint] >= 0).all()))
    # dependents, linked to the return of the person DEP_STAT names
    drows = np.flatnonzero(dep)
    ret = key.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy()[drows], d.DEP_STAT.to_numpy()[drows]]))
    linked = ret.notna().to_numpy()
    claimant_fs = d.set_index(["PH_SEQ", "A_LINENO"]).FILESTAT.reindex(
        pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy()[drows], d.DEP_STAT.to_numpy()[drows]])).to_numpy()
    gate("dependents_without_a_return_have_nonfiler_claimants", bool((claimant_fs[~linked] == 6).all()),
         other=np.unique(claimant_fs[~linked]).tolist())
    drows, ri = drows[linked], ret.to_numpy()[linked].astype(int)
    age = d.A_AGE.to_numpy()[drows]
    student = d.A_ENRLW.eq(1).to_numpy()[drows]
    mem = union[drows]
    kinds = {"k17": age < 17, "other": age >= 17, "keitc": (age < 19) | ((age < 24) & student), "k13": age < 13}
    counts = {}
    # A dependent filer claims no credit for anyone (the Census model gives its 3,300 returns none; IRC 152(b)(1)).
    by_depfiler = dep[rows][ri]
    for label, m in [("all", np.ones(len(drows), bool)), ("mem", mem), ("non", ~mem)]:
        counts[f"n_{label}"] = np.bincount(ri, weights=m.astype(float), minlength=n)
        for kind, km in kinds.items():
            counts[f"{kind}_{label}"] = np.bincount(ri, weights=(m & km & ~by_depfiler).astype(float), minlength=n)
        for g in range(3):
            counts[f"g{g}_{label}"] = np.bincount(ri, weights=(m & (gen[drows] == g)).astype(float), minlength=n)
    # a dependent who is the filer's (or spouse's) own child; for a non-member child of a member filer, the lineage's
    # identity-loss pattern
    h_line = d.A_LINENO.to_numpy()[rows][ri]
    s_line = np.where(spouse[ri] >= 0, d.A_LINENO.to_numpy()[np.maximum(spouse[ri], 0)], -9)
    par1, par2 = d.PEPAR1.to_numpy()[drows], d.PEPAR2.to_numpy()[drows]
    own_child = (par1 == h_line) | (par2 == h_line) | (par1 == s_line) | (par2 == s_line)
    # a non-member parent of the child in the household, who could claim the child once a member claimant leaves
    person = pd.Series(np.arange(len(d)), index=pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy(), d.A_LINENO.to_numpy()]))
    ph = d.PH_SEQ.to_numpy()[drows]

    def nonmember_parent(par):
        r = person.reindex(pd.MultiIndex.from_arrays([ph, par])).to_numpy()
        out = np.zeros(len(par), bool)
        out[~np.isnan(r)] = ~union[r[~np.isnan(r)].astype(int)]
        return out

    nm_parent = nonmember_parent(par1) | nonmember_parent(par2)
    counts["n_non_nm_parent"] = np.bincount(ri, weights=(~mem & nm_parent).astype(float), minlength=n)
    counts["n_non_own_only"] = np.bincount(ri, weights=(~mem & own_child & ~nm_parent).astype(float), minlength=n)
    R = pd.DataFrame({"row": rows, "spouse": spouse, **counts})
    fs = d.FILESTAT.to_numpy()[rows]
    R["status"] = np.select([np.isin(fs, [1, 2, 3]), fs == 4], ["joint", "hoh"], "single")
    R["depfiler"] = dep[rows]
    hoh_ok = (R.status.eq("hoh") == ((R.n_all > 0) & ~R.status.eq("joint") & ~R.depfiler)).to_numpy()
    gate("head_of_household_is_an_unmarried_head_with_a_dependent", bool(hoh_ok[~R.depfiler.to_numpy()].all()))
    R["mem_h"], R["gen_h"], R["civ_h"] = union[rows], gen[rows], civ[rows]
    sp = np.maximum(spouse, 0)
    R["mem_s"] = np.where(spouse >= 0, union[sp], False)
    R["gen_s"] = np.where(spouse >= 0, gen[sp], -1)
    R["civ_s"] = np.where(spouse >= 0, civ[sp], True)
    return R, drows, ri, gen[drows], mem


def person_income(d):
    """Per person: wages, self-employment income (raw and net of half its tax), investment income and AGI parts."""
    wages = d.WSAL_VAL.to_numpy(float)
    se = (d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    half = half_se_tax(se, wages)
    inv = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL.clip(lower=0) + d.CAP_VAL).to_numpy(float)
    agi_parts = (wages + se - half + (d.INT_VAL + d.DIV_VAL + d.RNT_VAL + d.CAP_VAL + d.UC_VAL + d.PNSN_VAL
                                       + d.ANN_VAL).to_numpy(float))
    return dict(wages=wages, se=se, earn_raw=wages + se, earn_eitc=wages + se - half, inv=inv, agi_parts=agi_parts,
                ss=d.SS_VAL.to_numpy(float), age=d.A_AGE.to_numpy(float),
                div_cap=np.maximum((d.DIV_VAL + d.CAP_VAL).to_numpy(float), 0))


# ---------------------------------------------------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------------------------------------------------
class Base:
    """The actual returns, anchored on the Census values."""

    def __init__(self, d, R, P, care):
        h, s = R.row.to_numpy(), R.spouse.to_numpy()
        has_s = s >= 0
        sp = np.maximum(s, 0)
        pick = lambda k: P[k][h] + np.where(has_s, P[k][sp], 0.0)  # noqa: E731
        self.status = R.status.to_numpy()
        self.joint = self.status == "joint"
        self.agi = d.AGI.to_numpy(float)[h]
        self.ti = d.TAX_INC.to_numpy(float)[h]
        self.fedbc = d.FEDTAX_BC.to_numpy(float)[h]
        self.ctc = d.CTC_CRD.to_numpy(float)[h]
        self.actc = d.ACTC_CRD.to_numpy(float)[h]
        self.eitc = d.EIT_CRED.to_numpy(float)[h]
        self.t0 = self.fedbc + self.ctc
        self.earn_raw, self.earn_eitc, self.inv = pick("earn_raw"), pick("earn_eitc"), pick("inv")
        eh, es = P["earn_raw"][h], np.where(has_s, P["earn_raw"][sp], 0.0)
        self.limit = np.where(self.joint & (eh > 0) & (es > 0), np.minimum(eh, es), eh + es)
        ah, as_ = P["age"][h], np.where(has_s, P["age"][sp], -1.0)
        self.age_ok = (((ah >= 25) & (ah <= 64)) | (self.joint & (as_ >= 25) & (as_ <= 64))) & ~R.depfiler.to_numpy()
        self.pref = (P["div_cap"][h] + np.where(has_s, P["div_cap"][sp], 0.0)) > 0
        self.aged = (ah >= 65).astype(float) + (self.joint & (as_ >= 65)).astype(float)
        self.care = np.maximum(care[h], 0.0)
        self.k = {f"{kind}": R[f"{kind}_all"].to_numpy() for kind in ("k17", "other", "keitc", "k13")}
        self.sched0 = schedule(self.ti, self.status)
        self.cdcc0 = care_credit(self.agi, self.k["k13"], self.care, self.limit, self.sched0)
        self.taxpre0 = self.t0 + self.cdcc0
        self.resid0 = self.taxpre0 - self.sched0          # the Census tax the rate schedule does not explain
        nonref, actc = child_credits(self.status, self.agi, self.t0, self.earn_raw, self.k["k17"], self.k["other"])
        e = eitc(self.k["keitc"], self.earn_eitc, self.agi, self.joint, self.inv, self.age_ok)
        self.rule = dict(nonref=nonref, actc=actc, eitc=e)
        self.resid = dict(nonref=self.ctc - nonref, actc=self.actc - actc, eitc=self.eitc - e)
        ded = self.agi - self.ti
        std0 = np.array([STD[x] for x in self.status]) + np.array([AGED[x] for x in self.status]) * self.aged
        self.itemized = np.where(ded > std0 + 1, ded, 0.0)   # 0: the standard deduction (or no taxable income)

    def actual(self):
        return dict(cdcc=self.cdcc0, t0=self.t0, nonref=self.ctc, actc=self.actc, eitc=self.eitc, fedbc=self.fedbc)

    def run(self, k, status=None, agi=None, ti=None, earn_raw=None, earn_eitc=None, inv=None, age_ok=None,
            limit=None, share=None, own_return=True):
        """A counterfactual: dependents k, and optionally a new filing status and income (with `share`, the part of
        the return's income a remaining spouse keeps). Credits carry the Census residual only on the same return
        (own_return); a remaining spouse's return is the rule's alone."""
        status = self.status if status is None else status
        agi = self.agi if agi is None else agi
        ti = self.ti if ti is None else ti
        earn_raw = self.earn_raw if earn_raw is None else earn_raw
        earn_eitc = self.earn_eitc if earn_eitc is None else earn_eitc
        inv = self.inv if inv is None else inv
        age_ok = self.age_ok if age_ok is None else age_ok
        limit = self.limit if limit is None else limit
        share = 1.0 if share is None else share
        sched = schedule(ti, status)
        cd = care_credit(agi, k["k13"], self.care, limit, sched)
        taxpre = np.maximum(sched + self.resid0 * share, 0)
        t0 = taxpre - cd
        nonref, actc = child_credits(status, agi, t0, earn_raw, k["k17"], k["other"])
        e = eitc(k["keitc"], earn_eitc, agi, status == "joint", inv, age_ok)
        keep = 1.0 if own_return else 0.0
        nonref = np.minimum(np.maximum(nonref + keep * self.resid["nonref"], 0), np.maximum(t0, 0))
        actc = np.maximum(actc + keep * self.resid["actc"], 0)
        e = np.maximum(e + keep * self.resid["eitc"], 0)
        return dict(cdcc=cd, t0=t0, nonref=nonref, actc=actc, eitc=e, fedbc=t0 - nonref)


def counts(R, label):
    return {kind: R[f"{kind}_{label}"].to_numpy() for kind in ("k17", "other", "keitc", "k13")}


def remaining_spouse(base, R, P, who):
    """The non-member spouse's own return: `who` is 'head' (the member spouse leaves) or 'spouse' (the member head
    leaves); the return's non-member dependents stay with them."""
    h, s = R.row.to_numpy(), R.spouse.to_numpy()
    sp = np.maximum(s, 0)
    own, other = (h, sp) if who == "head" else (sp, h)
    comp_o, comp_x = np.maximum(P["agi_parts"][own], 0), np.maximum(P["agi_parts"][other], 0)
    share = np.where(comp_o + comp_x > 0, comp_o / np.maximum(comp_o + comp_x, 1e-9), 0.5)
    ss_o, ss_x = P["ss"][own], P["ss"][other]
    joint_parts = P["agi_parts"][own] + P["agi_parts"][other]
    unexplained = base.agi - (joint_parts + taxable_ss(joint_parts, ss_o + ss_x, np.ones(len(h), bool)))
    agi = P["agi_parts"][own] + taxable_ss(P["agi_parts"][own], ss_o, np.zeros(len(h), bool)) + unexplained * share
    status = np.where(R.n_non.to_numpy() > 0, "hoh", "single")
    aged = (P["age"][own] >= 65).astype(float)
    std = np.where(status == "hoh", STD["hoh"], STD["single"]) + AGED["single"] * aged
    ti = np.maximum(agi - np.maximum(base.itemized * share, std), 0)
    age_ok = (P["age"][own] >= 25) & (P["age"][own] <= 64)
    return base.run(counts(R, "non"), status=status, agi=agi, ti=ti, earn_raw=P["earn_raw"][own],
                    earn_eitc=P["earn_eitc"][own], inv=P["inv"][own], age_ok=age_ok, limit=P["earn_raw"][own],
                    share=share, own_return=False), share, agi


# ---------------------------------------------------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------------------------------------------------
def main() -> None:
    sys.dont_write_bytecode = True  # the other lanes' modules are imported read-only
    print("[load] CPS ASEC 2025 persons, households and replicate weights", flush=True)
    d = load()
    civ, union, gen = groups(d)
    W, lineage_factor, lineage_counts = row4_weights(d, civ, union)
    d = d.drop(columns=REPS[1:])                    # pwwgt0 stays: the published weight
    flag, onbooks, onbooks_labels = status_flag(d)
    stored = json.loads(STORED_STACK.read_text())["asec2025_adopted"]
    for name, got in [("civilian_m", W[civ, 0].sum() / 1e6), ("flagged_m", W[civ & flag, 0].sum() / 1e6),
                      ("flagged_union_m", W[union & flag, 0].sum() / 1e6), ("union_m", W[union, 0].sum() / 1e6)]:
        gate(f"row4_status_frame_reproduces_the_adopted_stacks_{name}", abs(float(got) - stored[name]) < 1e-9,
             got=float(got), want=stored[name])
    hf = float(d.pwwgt0.to_numpy()[civ].sum() / 340_110_988.0)
    gate("household_fraction_is_the_accounts", abs(hf - json.loads(STORED_STACK.read_text())["household_fraction"]) < 1e-12,
         value=hf)

    alloc, unequal_units = allocation_check(d, civ, union, json.loads(MODEL.read_text()), hf)
    R, drows, ri, dgen, dmem = returns(d, union, gen, civ)
    P = person_income(d)
    base = Base(d, R, P, d.HCHCARE_VAL.to_numpy(float))
    h = R.row.to_numpy()
    wr = W[h]                                       # each return carries its head's row-4 weights (161)
    n = len(R)
    print(f"[returns] {n} returns, {len(drows)} linked dependents", flush=True)

    # --- 1. the rules reproduce the Census credits on the actual returns -------------------------------------------
    w0 = wr[:, 0]
    depf = R.depfiler.to_numpy()
    gate("dependent_filers_carry_no_credits", (x := float(np.abs(base.ctc + base.actc + base.eitc)[depf].max())) == 0,
         value=dict(largest_credit=x, returns=int(depf.sum())))
    val = []
    gap = np.maximum(base.sched0 - base.t0, 0)
    fits = {"ctc_crd": (base.rule["nonref"], base.ctc), "actc_crd": (base.rule["actc"], base.actc),
            "eit_cred": (base.rule["eitc"], base.eitc)}
    for name, (model, census) in fits.items():
        err = np.abs(model - census)
        pos = census > 0
        val.append(dict(field=name, returns=n, census_bn=float(census @ w0 / 1e9), rule_bn=float(model @ w0 / 1e9),
                        share_returns_within_1=float((err <= 1).mean()),
                        share_positive_returns_within_1=float((err[pos] <= 1).mean()),
                        share_census_dollars_on_returns_within_1=float((census * (err <= 1)) @ w0 / (census @ w0))))
    plain = ~base.pref & (base.agi < 400000)       # returns the ordinary rate schedule taxes in full
    err = np.abs(base.cdcc0 - gap)
    m = plain & (gap > 1)
    val.append(dict(field="care_credit_vs_schedule_gap", returns=int(plain.sum()), census_bn=float(gap[plain] @ w0[plain] / 1e9),
                    rule_bn=float(base.cdcc0[plain] @ w0[plain] / 1e9), share_returns_within_1=float((err[plain] <= 1).mean()),
                    share_positive_returns_within_1=float((err[m] <= 1).mean()),
                    share_census_dollars_on_returns_within_1=float((gap[plain] * (err[plain] <= 1)) @ w0[plain]
                                                                   / (gap[plain] @ w0[plain]))))
    for row in val:
        print(f"  {row['field']:30s} census ${row['census_bn']:.3f}bn rule ${row['rule_bn']:.3f}bn within $1: "
              f"{row['share_positive_returns_within_1']:.4f} of positive returns, "
              f"{row['share_census_dollars_on_returns_within_1']:.4f} of dollars")
    vt = {r["field"]: r for r in val}
    fit = {k: (vt[k]["share_returns_within_1"] if k == "ctc_crd" else vt[k]["share_positive_returns_within_1"]) for k in vt}
    gate("rule_reproduces_ctc_crd_on_every_return", fit["ctc_crd"] == 1.0, value=fit["ctc_crd"])
    gate("rule_reproduces_actc_crd_999_of_positive_returns", fit["actc_crd"] >= 0.999, value=fit["actc_crd"])
    gate("rule_reproduces_eit_cred_998_of_positive_returns", fit["eit_cred"] >= 0.998, value=fit["eit_cred"])
    gate("rule_reproduces_the_care_credit_97_of_positive_gaps", fit["care_credit_vs_schedule_gap"] >= 0.97,
         value=fit["care_credit_vs_schedule_gap"])
    actual = base.actual()
    gate("the_actual_scenario_returns_the_census_values",
         all(np.allclose(base.run(base.k)[f], actual[f], atol=1e-6) for f in ("t0", "nonref", "actc", "eitc", "fedbc")))

    # --- 2. counterfactuals -------------------------------------------------------------------------------------------
    s_m = base.run(counts(R, "non"))            # member dependents removed
    s_n = base.run(counts(R, "mem"))            # non-member dependents removed
    nm_h, m_h = ~R.mem_h.to_numpy(), R.mem_h.to_numpy()
    has_s = R.spouse.to_numpy() >= 0
    m_s = R.mem_s.to_numpy()
    civ_ok = R.civ_h.to_numpy() & R.civ_s.to_numpy()
    n_mem, n_non = R.n_mem.to_numpy(), R.n_non.to_numpy()
    # C: single status for a non-member head of household left with no dependent
    c_mask = nm_h & (base.status == "hoh") & (n_non == 0) & (n_mem > 0)
    std_single = STD["single"] + AGED["single"] * base.aged
    ti_c = np.maximum(base.agi - np.where(base.itemized > 0, base.itemized, std_single), 0)
    s_c = base.run(counts(R, "non"), status=np.where(c_mask, "single", base.status), ti=np.where(c_mask, ti_c, base.ti))
    # Cr: the reverse, a member head of household whose dependents are all non-members files single without them
    cr_mask = m_h & (base.status == "hoh") & (n_mem == 0) & (n_non > 0)
    s_cr = base.run(counts(R, "mem"), status=np.where(cr_mask, "single", base.status),
                    ti=np.where(cr_mask, ti_c, base.ti))
    # D: the non-member spouse alone
    d1 = nm_h & has_s & m_s
    d2 = m_h & has_s & ~m_s
    s_r1, share1, agi1 = remaining_spouse(base, R, P, "head")
    s_r2, share2, agi2 = remaining_spouse(base, R, P, "spouse")

    def flows(s):
        return np.stack([s["fedbc"], s["nonref"], s["cdcc"], s["actc"], s["eitc"]])  # 5 x n

    F0, Fm, Fn, Fc, Fcr, Fr1, Fr2 = map(flows, (actual, s_m, s_n, s_c, s_cr, s_r1, s_r2))
    # Net-cost parts per return, CPS dollars: receipts (federal income tax before refundable credits; the group's
    # receipts fall = cost up) and spending (refundable credits charged to the group = cost up).
    comp = {}
    a = nm_h & (n_mem > 0) & civ_ok
    comp["A_nonref"] = np.where(a, F0[1] - Fm[1], 0)
    comp["A_care"] = np.where(a, F0[2] - Fm[2], 0)
    comp["A_actc"] = np.where(a, F0[3] - Fm[3], 0)
    comp["A_eitc"] = np.where(a, F0[4] - Fm[4], 0)
    b = m_h & (n_non > 0) & civ_ok
    comp["B_nonref"] = -np.where(b, F0[1] - Fn[1], 0)
    comp["B_care"] = -np.where(b, F0[2] - Fn[2], 0)
    comp["B_actc"] = -np.where(b, F0[3] - Fn[3], 0)
    comp["B_eitc"] = -np.where(b, F0[4] - Fn[4], 0)
    gate("A_and_B_move_tax_only_through_the_credits", bool(
        np.allclose(np.where(a, Fm[0] - F0[0], 0), comp["A_nonref"] + comp["A_care"], atol=1e-6)
        and np.allclose(np.where(b, Fn[0] - F0[0], 0), -(comp["B_nonref"] + comp["B_care"]), atol=1e-6)))
    cm = c_mask & civ_ok
    comp["C_status"] = np.where(cm, Fc[0] - Fm[0], 0)
    gate("C_changes_no_credit", bool(np.allclose(np.where(cm, Fc[3:] - Fm[3:], 0), 0)))
    crm = cr_mask & civ_ok
    comp["Cr_status"] = -np.where(crm, Fcr[0] - Fn[0], 0)
    gate("Cr_changes_no_credit", bool(np.allclose(np.where(crm, Fcr[3:] - Fn[3:], 0), 0)))
    dm1, dm2 = d1 & civ_ok, d2 & civ_ok
    comp["D_receipts"] = (np.where(dm1, Fr1[0] - Fm[0], 0)
                          + np.where(dm2, Fr2[0] + (Fn[0] - F0[0]), 0))
    comp["D_spending"] = (np.where(dm1, (Fm[3] + Fm[4]) - (Fr1[3] + Fr1[4]), 0)
                          + np.where(dm2, -(Fr2[3] + Fr2[4]) + (F0[3] - Fn[3]) + (F0[4] - Fn[4]), 0))
    side = {"A_nonref": "receipts", "A_care": "receipts", "A_actc": "spending", "A_eitc": "spending",
            "B_nonref": "receipts", "B_care": "receipts", "B_actc": "spending", "B_eitc": "spending",
            "C_status": "receipts", "Cr_status": "receipts", "D_receipts": "receipts", "D_spending": "spending"}
    # Status rule: an imputed unauthorized head's EITC counts at 0, everything else at its on-books share.
    fh = flag[h]
    f_other = np.where(fh, onbooks["central"][h], 1.0)
    f_eitc = np.where(fh, 0.0, 1.0)
    rule = {k: (f_eitc if k.endswith("_eitc") else f_other) for k in comp}
    # D's spending mixes ACTC and EITC; split it so each gets its own factor.
    d_actc = (np.where(dm1, Fm[3] - Fr1[3], 0) + np.where(dm2, -Fr2[3] + (F0[3] - Fn[3]), 0))
    d_eitc = comp["D_spending"] - d_actc
    comp_ruled = {k: v * rule[k] for k, v in comp.items() if k != "D_spending"}
    comp_ruled["D_spending"] = d_actc * f_other + d_eitc * f_eitc

    # --- 3. generations ------------------------------------------------------------------------------------------------
    frac_mem = np.stack([R[f"g{g}_mem"].to_numpy() for g in range(3)]) / np.maximum(n_mem, 1)   # 3 x n
    gen_h, gen_s = R.gen_h.to_numpy(), R.gen_s.to_numpy()
    owner = {}
    for k in comp:
        if k.startswith(("A_", "C_")):
            owner[k] = frac_mem
        elif k.startswith(("B_", "Cr_")):
            owner[k] = np.stack([(gen_h == g).astype(float) for g in range(3)])
        else:  # D: the member spouse (head on D2 returns)
            owner[k] = np.stack([np.where(dm1, gen_s == g, 0) + np.where(dm2, gen_h == g, 0) for g in range(3)]
                                ).astype(float)
    for k in comp:
        live = np.abs(comp_ruled[k]) > 0
        gate(f"{k}_has_a_generation_wherever_it_is_nonzero", bool(np.allclose(owner[k][:, live].sum(axis=0), 1)))

    # --- 4. account dollars ---------------------------------------------------------------------------------------------
    model = json.loads(MODEL.read_text())
    mts = json.loads(MTS.read_text())
    eitc_case = np.where(flag, 0.0, d.EIT_CRED.to_numpy(float))
    actc_case = np.where(flag, d.ACTC_CRD.to_numpy(float) * onbooks["central"], d.ACTC_CRD.to_numpy(float))
    n_key = (eitc_case + actc_case)[civ] @ W[civ]                      # national refundable key, 161
    ref_line = next(x for x in model["spending"]["lines"] if x["id"] == "refundable_tax_credits")
    share_pub = float((d.EIT_CRED + d.ACTC_CRD).to_numpy()[union] @ d.pwwgt0.to_numpy()[union]
                      / ((d.EIT_CRED + d.ACTC_CRD).to_numpy()[civ] @ d.pwwgt0.to_numpy()[civ]))
    gate("published_refundable_key_share_is_model_jsons", abs(share_pub - ref_line["keys"]["refundable_credits"][
        "personal"]["share"]) < 1e-9, got=share_pub)
    per_ref = mts["non_ptc_remainder_bn"] * hf / n_key                 # account $bn per CPS dollar, 161
    km = by_path(FISCAL / "tax_key_heldout_2026_09_28/keys.py", "case_tax_keys")
    with contextlib.redirect_stdout(io.StringIO()):
        pk = km.person_keys()
    bench = km.load_frame(km.TAX_COLS + ["PPPOS"])
    gate("tax_key_frame_is_this_frame", len(bench) == len(d) and bool(
        (bench.sort_values(["PH_SEQ", "PPPOS"]).FEDTAX_BC.to_numpy() == d.FEDTAX_BC.to_numpy()).all()))
    groups_b = km.cbo_groups(bench)
    labels, _ = km.irs_2023()
    edges, _ = km.bin_edges(labels)
    agi_b = bench.AGI.to_numpy(float)
    b19 = np.where(agi_b <= 0, 0, np.searchsorted(edges, agi_b, side="right") + 1)
    b14 = np.where(b19 <= 1, 0, np.minimum(b19, 14) - 1)
    pkm = pk.set_index(["PH_SEQ", "PPPOS"]).reindex(pd.MultiIndex.from_arrays([bench.PH_SEQ, bench.PPPOS]))
    v = pkm.fit_case_personal.to_numpy()
    fb = bench.FEDTAX_BC.to_numpy(float)
    pos = (fb > 0) & pkm.civilian.to_numpy()
    cells = pd.DataFrame({"g": groups_b[pos], "b": b14[pos], "ratio": v[pos] / fb[pos]})
    spread = cells.groupby(["g", "b"]).ratio.agg(lambda x: float(x.max() / x.min() - 1))
    gate("irs_key_ratio_is_constant_within_each_cell", float(spread.max()) < 1e-9, max=float(spread.max()))
    table = cells.groupby(["g", "b"]).ratio.first()
    cell_of = pd.DataFrame({"PH_SEQ": bench.PH_SEQ, "PPPOS": bench.PPPOS, "g": groups_b, "b": b14}
                           ).set_index(["PH_SEQ", "PPPOS"])
    hc = cell_of.reindex(pd.MultiIndex.from_arrays([d.PH_SEQ.to_numpy()[h], d.PPPOS.to_numpy()[h]]))
    ratio = table.reindex(pd.MultiIndex.from_arrays([hc.g, hc.b])).to_numpy()
    live_receipts = np.zeros(n, bool)
    for k in comp_ruled:
        if side[k] == "receipts":
            live_receipts |= np.abs(comp_ruled[k]) > 0
    gate("every_return_with_a_tax_change_has_an_irs_key_cell", bool(np.isfinite(ratio[live_receipts]).all()),
         missing=int((~np.isfinite(ratio[live_receipts])).sum()))
    ratio = np.nan_to_num(ratio)
    fit_line = next(x for x in model["receipts"]["lines"] if x["id"] == "federal_income_tax")["national_bn"]
    # The key sums to 1 over civilians on pwwgt0; on row 4's weights its mass differs slightly, and a share is mass / it.
    vd = pk.set_index(["PH_SEQ", "PPPOS"]).reindex(pd.MultiIndex.from_arrays([d.PH_SEQ, d.PPPOS]))
    gate("tax_key_civilians_are_this_frames", bool((vd.civilian.to_numpy() == civ).all()))
    vkey = vd.fit_case_personal.to_numpy(float)
    gate("tax_key_sums_to_1_over_civilians_on_pwwgt0", abs((x := float(vkey[civ] @ d.pwwgt0.to_numpy()[civ])) - 1) < 1e-9,
         value=x)
    mass_r4 = float(vkey[civ] @ W[civ, 0])
    per_fit = fit_line * ratio / mass_r4                                # account $bn per CPS dollar at weight 1

    # --- 5. totals ------------------------------------------------------------------------------------------------------
    # Readings of the reverse terms (B and Cr), the part of a non-member child's credit that continues once the member
    # claimant leaves: R1 all of it; R2 only where the claimant's non-member spouse remains; R3 where that spouse or a
    # non-member parent of the child lives in the household (dependents counted equally within a return).
    reverse = [k for k in comp if k.startswith(("B_", "Cr_"))]
    keep_by = {"R1": np.ones(n), "R2": dm2.astype(float),
               "R3": np.where(dm2, 1.0, R.n_non_nm_parent.to_numpy() / np.maximum(n_non, 1))}
    READINGS = tuple(keep_by)

    def keep_of(reading, k):
        return keep_by[reading] if k in reverse else np.ones(n)

    def account(x, k):
        """Account $bn of CPS-dollar flow x on component k's line, 161 columns."""
        return (x * per_fit) @ wr if side[k] == "receipts" else (x @ wr) * per_ref

    rows = []
    for k in comp_ruled:
        for g in range(3):
            for reading in READINGS:
                xg = comp_ruled[k] * owner[k][g] * keep_of(reading, k)
                cps, acct = xg @ wr, account(xg, k)
                rows.append(dict(component=k, side=side[k], generation=GENS[g], reading=reading,
                                 cps_bn=cps[0] / 1e9, cps_se_bn=sdr(cps) / 1e9, account_bn=acct[0],
                                 account_se_bn=sdr(acct), returns=int((np.abs(xg) > 0).sum()),
                                 returns_m=float(wr[np.abs(xg) > 0, 0].sum() / 1e6)))
    terms = pd.DataFrame(rows)

    # --- 6. conservation and frame gates -------------------------------------------------------------------------------
    cred = {"ctc_crd": (base.ctc, "A_nonref", "B_nonref"), "actc_crd": (base.actc, "A_actc", "B_actc"),
            "eit_cred": (base.eitc, "A_eitc", "B_eitc")}
    conservation = {}
    for name, (census, ka, kb) in cred.items():
        tot = census @ w0
        on_members = np.where(m_h, census, 0) @ w0
        moved_in = np.where(a, comp[ka], 0) @ w0
        moved_out = -np.where(b, comp[kb], 0) @ w0
        members, others = on_members + moved_in - moved_out, (tot - on_members) - moved_in + moved_out
        gate(f"{name}_attributed_to_members_and_others_adds_to_the_cps_total",
             abs(members + others - tot) < 1e-6 * max(tot, 1) and 0 <= moved_in <= tot - on_members + 1e-6
             and 0 <= moved_out <= on_members + 1e-6,
             value=dict(cps_total_bn=tot / 1e9, members_bn=members / 1e9, others_bn=others / 1e9))
        conservation[name] = dict(cps_total_bn=tot / 1e9, personal_members_bn=on_members / 1e9,
                                  forward_in_bn=moved_in / 1e9, reverse_out_bn=moved_out / 1e9,
                                  attributed_members_bn=members / 1e9, attributed_others_bn=others / 1e9)
    gate("every_member_dependent_is_civilian", bool(civ[drows][dmem].all()))

    # --- 7. hand-checked example: a non-member head of household, one member child under 17 ----------------------------
    pool = np.flatnonzero(c_mask & civ_ok & ~fh & (R.n_all.to_numpy() == 1) & (R.k17_mem.to_numpy() == 1)
                          & (R.k13_all.to_numpy() == 0) & (base.inv == 0) & (P["se"][h] == 0)
                          & (base.itemized == 0) & (base.eitc > 0) & (base.actc > 0) & (base.ctc > 0)
                          & (base.aged == 0) & (d.SS_VAL.to_numpy()[h] == 0))
    gate("an_example_return_exists", len(pool) > 0, value=int(len(pool)))
    i = int(pool[0])
    example = dict(PH_SEQ=int(d.PH_SEQ.iloc[h[i]]), head_line=int(d.A_LINENO.iloc[h[i]]),
                   FILESTAT=int(d.FILESTAT.iloc[h[i]]), head_age=int(d.A_AGE.iloc[h[i]]),
                   head_member=bool(m_h[i]), wages=float(P["wages"][h[i]]), AGI=float(base.agi[i]),
                   TAX_INC=float(base.ti[i]), FEDTAX_BC=float(base.fedbc[i]), CTC_CRD=float(base.ctc[i]),
                   ACTC_CRD=float(base.actc[i]), EIT_CRED=float(base.eitc[i]),
                   dependents=[dict(line=int(d.A_LINENO.iloc[r]), age=int(d.A_AGE.iloc[r]), member=bool(union[r]),
                                    generation=GENS[gen[r]] if gen[r] >= 0 else None)
                               for r in drows[ri == i]],
                   counterfactual_no_dependents=dict(nonref=float(Fm[1, i]), actc=float(Fm[3, i]), eitc=float(Fm[4, i]),
                                                     fedtax_bc=float(Fm[0, i])),
                   single_status=dict(taxable_income=float(ti_c[i]), fedtax_bc=float(Fc[0, i])),
                   A=dict(nonref=float(comp["A_nonref"][i]), actc=float(comp["A_actc"][i]),
                          eitc=float(comp["A_eitc"][i])),
                   C=float(comp["C_status"][i]), weight=float(w0[i]))

    # --- 8. outputs -----------------------------------------------------------------------------------------------------
    OUT.mkdir(parents=True, exist_ok=True)
    terms = terms.round(9)
    terms.to_csv(OUT / "terms.csv", index=False, lineterminator="\n")
    with open(OUT / "validation.csv", "w", newline="") as fh_:
        wcsv = csv.DictWriter(fh_, fieldnames=list(val[0]), lineterminator="\n")
        wcsv.writeheader()
        wcsv.writerows([{k: (round(v, 9) if isinstance(v, float) else v) for k, v in r.items()} for r in val])
    (OUT / "example.json").write_text(json.dumps(example, indent=1) + "\n")

    def agg(reading, keys, field="account_bn"):
        t = terms[(terms.reading == reading) & terms.component.isin(keys)]
        return {g: float(t[t.generation == g][field].sum()) for g in GENS} | {"total": float(t[field].sum())}

    def agg_se(reading, keys):
        """SE of a sum of components, from the replicates (recomputed, not added in quadrature)."""
        out = {GENS[g]: sum(account(comp_ruled[k] * owner[k][g] * keep_of(reading, k), k) for k in keys)
               for g in range(3)}
        out["total"] = sum(out[x] for x in GENS)
        return {kk: sdr(vv) for kk, vv in out.items()}

    def full(keys, weight):
        return float(sum(account(comp_ruled[k] * weight, k)[0] for k in keys))

    A = [k for k in comp if k.startswith("A_")]
    B = [k for k in comp if k.startswith("B_")]
    sets = {"forward_A": A, "reverse_B": B, "child_credit_net_A_plus_B": A + B,
            "status_C_forward": ["C_status"], "status_Cr_reverse": ["Cr_status"],
            "child_credit_and_status_net": A + B + ["C_status", "Cr_status"],
            "joint_split_D": ["D_receipts", "D_spending"], "full_removal_recomputation": list(comp)}
    joint = base.joint
    nn = np.maximum(n_non, 1)
    nm_par, own_only = R.n_non_nm_parent.to_numpy(), R.n_non_own_only.to_numpy()
    reverse_classes = {   # R1's reverse terms (B and Cr) by why the child would stay, dependents counted equally
        "claimants_nonmember_spouse_remains_D2": dm2.astype(float),
        "nonmember_parent_in_household": np.where(dm2, 0, nm_par / nn),
        "own_child_of_member_filer_only": np.where(dm2, 0, own_only / nn),
        "other_relative_or_unrelated": np.where(dm2, 0, (n_non - nm_par - own_only) / nn)}
    mex_h = d.PRDTHSP.to_numpy()[h] == 1
    st_cred = (d.STATETAX_B - d.STATETAX_A).to_numpy(float)[h]
    forward_types = {"joint_with_member_spouse_D1": dm1.astype(float),
                     "joint_both_nonmembers": (joint & ~dm1).astype(float), "unmarried_head": (~joint).astype(float)}
    summary = dict(
        lane="mixed_unit_credits_2026_10_14", income_year=2024, sign="positive raises the group's net cost",
        frame=dict(union_row4=float(W[union, 0].sum()), returns=n, dependent_filer_returns=int(depf.sum()),
                   linked_dependents=int(len(drows)),
                   lineage_g3plus_factor=lineage_factor, lineage_counts=lineage_counts),
        conversion=dict(refundable_bn_per_cps_bn=float(per_ref[0] * 1e9), non_ptc_bn=mts["non_ptc_remainder_bn"],
                        household_fraction=hf, national_refundable_key_bn=float(n_key[0] / 1e9),
                        federal_income_tax_line_bn=fit_line, irs_key_mass_on_row4=mass_r4,
                        federal_account_per_cps_dollar={
                            name: float((x * per_fit) @ w0 / (x @ w0) * 1e9)
                            for name, x in [("A", comp_ruled["A_nonref"] + comp_ruled["A_care"]),
                                            ("B", comp_ruled["B_nonref"] + comp_ruled["B_care"]),
                                            ("C", comp_ruled["C_status"]), ("Cr", comp_ruled["Cr_status"]),
                                            ("D", comp_ruled["D_receipts"])]},
                        federal_national_average_per_cps_dollar=float(fit_line * 1e9 / (d.FEDTAX_BC.to_numpy(float)[civ]
                                                                                         @ W[civ, 0]))),
        onbooks_central=dict(mexico_born=onbooks_labels["central"][0], other_latin_american=onbooks_labels["central"][1]),
        conservation=conservation, gates=len(GATES),
        account={reading: {name: dict(bn=agg(reading, keys), se_bn=agg_se(reading, keys),
                                      cps_bn=agg(reading, keys, "cps_bn"))
                           for name, keys in sets.items()} for reading in READINGS},
        reverse_R1_by_why_the_child_stays_bn={c: full(reverse, wt) for c, wt in reverse_classes.items()},
        forward_A_by_return_type_bn={t: full(A, wt) for t, wt in forward_types.items()},
        forward_A_by_head_origin_bn={   # a non-member head of Mexican origin may be in the lineage the case adds
            "nonmember_head_reports_mexican_origin": full(A, mex_h.astype(float)),
            "nonmember_head_does_not": full(A, (~mex_h).astype(float))},
        joint_split_D_by_head_bn={
            "D1_nonmember_head_member_spouse_leaves": {k: full([k], dm1.astype(float)) for k in ("D_receipts", "D_spending")},
            "D2_member_head_leaves_nonmember_spouse_files_alone": {k: full([k], dm2.astype(float))
                                                                   for k in ("D_receipts", "D_spending")}},
        crossing_persons_m=dict(
            member_dependents_of_nonmember_returns=float(W[drows, 0][dmem & (nm_h & civ_ok)[ri]].sum() / 1e6),
            nonmember_dependents_of_member_returns=float(W[drows, 0][~dmem & (m_h & civ_ok)[ri]].sum() / 1e6),
            mixed_joint_returns_nonmember_head=float(w0[dm1].sum() / 1e6),
            mixed_joint_returns_member_head=float(w0[dm2].sum() / 1e6),
            hoh_nonmember_heads_losing_status=float(w0[cm].sum() / 1e6),
            hoh_member_heads_with_only_nonmember_dependents=float(w0[crm].sum() / 1e6)),
        # Not priced: state credits (all of them, child-related or not) on the crossing returns, apportioned by the
        # crossing dependents' share of the return's dependents, CPS dollars on row 4's weights.
        state_credits_on_crossing_returns_bound_cps_bn=dict(
            forward=float((st_cred * n_mem / np.maximum(R.n_all.to_numpy(), 1) * w0)[a].sum() / 1e9),
            **{f"reverse_{r}": float((st_cred * n_non / np.maximum(R.n_all.to_numpy(), 1) * keep_by[r] * w0)[b].sum() / 1e9)
               for r in READINGS}),
        allocation_check=dict(spm_units_with_unequal_person_weights=unequal_units,
                              rows=alloc.round(12).to_dict(orient="records")),
        excluded_noncivilian=dict(returns=int((~civ_ok & ((nm_h & (n_mem > 0)) | (m_h & (n_non > 0)) | d1 | d2)).sum())),
    )

    # --- 9. the item for main case v7 (the lead's contract): R3 with head-of-household status, identified union ------
    rec = "R3"
    status_keys = ["C_status", "Cr_status"]
    terms_of = {"A": A, "B": B, "C": ["C_status"], "Cr": ["Cr_status"]}
    G_OUT = {"G1": "G1", "G2": "G2", "G3+": "G3plus"}
    SIDE_OUT = {"receipts": "receipt", "spending": "spending"}
    LINE_OF = {"receipts": "federal_income_tax", "spending": "refundable_tax_credits"}

    def bn(keys, reading, g=None, on=None):
        """Net-cost $bn of the components `keys` (only those on side `on`, if given) at a reading, on the full weights,
        for one generation (index into GENS) or all."""
        out = 0.0
        for k in keys:
            if on is None or side[k] == on:
                out += float(account(comp_ruled[k] * keep_of(reading, k) * (1.0 if g is None else owner[k][g]), k)[0])
        return out

    # A part's bn is its change to the group's target on its line, so the parts add to the two edits; cost_bn is its
    # effect on the group's net cost (a receipt part's cost_bn is minus its bn).
    parts = {}
    for term, keys in terms_of.items():
        for sd in ("receipts", "spending"):
            if any(side[k] == sd for k in keys):
                for i, g in enumerate(GENS):
                    cost = bn(keys, rec, i, sd)
                    parts[f"{term}_{SIDE_OUT[sd]}_{G_OUT[g]}"] = dict(
                        bn=-cost if sd == "receipts" else cost, cost_bn=cost, line=LINE_OF[sd], side=SIDE_OUT[sd],
                        generation=G_OUT[g], term=term)
    receipt_edit = sum(v["bn"] for v in parts.values() if v["side"] == "receipt")
    spending_edit = sum(v["bn"] for v in parts.values() if v["side"] == "spending")
    net = sum(v["cost_bn"] for v in parts.values())
    by_gen = {G_OUT[g]: {"personal": sum(v["cost_bn"] for v in parts.values() if v["generation"] == G_OUT[g])}
              for g in GENS}
    fit_cells = next(x for x in model["receipts"]["lines"] if x["id"] == "federal_income_tax")["cells"]
    ref_sc = model["receipts"]["reference"]
    on_key = [sc for sc in model["receipts"]["scenarios"] if fit_cells[sc]["personal"]["key"] == "federal_liability"]
    absent = sorted(set(model["receipts"]["scenarios"]) - set(on_key))
    edits = [dict(side="receipt", line="federal_income_tax", scenario=sc, by=dict(personal=receipt_edit, shared=0.0))
             for sc in on_key]
    edits.append(dict(side="spending", line="refundable_tax_credits", key=ref_line["preferred_key"],
                      by=dict(personal=spending_edit, shared=0.0)))
    gate("refundable_tax_credits_preferred_key_is_refundable_credits", ref_line["preferred_key"] == "refundable_credits",
         value=ref_line["preferred_key"])
    gate("item_receipt_edit_covers_the_seven_federal_liability_rules", len(on_key) == 7 and absent == ["federal_gap_high_agi"]
         and ref_sc in on_key, value=dict(listed=on_key, absent=absent))
    # main_case_2026_09_24/package.cjs expand(): other rules take the reference edit times their target over the
    # reference's; on the seven federal_liability rules that ratio is exactly 1.
    gate("item_federal_liability_rules_share_the_reference_target",
         all(fit_cells[sc]["personal"]["target_bn"] == fit_cells[ref_sc]["personal"]["target_bn"] for sc in on_key),
         value=fit_cells[ref_sc]["personal"]["target_bn"])
    gate("item_is_the_summarys_r3_with_status",
         abs(net - summary["account"][rec]["child_credit_and_status_net"]["bn"]["total"]) < 1e-6, value=net)
    gate("item_parts_add_to_the_two_edits_and_the_net", abs(spending_edit - receipt_edit - net) < 1e-12
         and abs(receipt_edit + bn(A + B + status_keys, rec, None, "receipts")) < 1e-9
         and abs(spending_edit - bn(A + B + status_keys, rec, None, "spending")) < 1e-9,
         value=dict(receipt=receipt_edit, spending=spending_edit, net=net))
    gate("item_generations_add_to_the_net", abs(sum(v["personal"] for v in by_gen.values()) - net) < 1e-12,
         value={g: v["personal"] for g, v in by_gen.items()})

    def arm(reading, keys):
        return dict(net_bn={"personal": bn(keys, reading)},
                    by_generation={G_OUT[g]: {"personal": bn(keys, reading, i)} for i, g in enumerate(GENS)},
                    se_bn={"personal": agg_se(reading, keys)["total"]},
                    edits_personal=dict(receipt=-bn(keys, reading, None, "receipts"),
                                        spending=bn(keys, reading, None, "spending")))

    arms = {"R1_with_status": arm("R1", A + B + status_keys), "R2_with_status": arm("R2", A + B + status_keys),
            "R3_without_status": arm("R3", A + B)}
    for name, x in arms.items():
        gate(f"item_arm_{name}_is_the_summarys", abs(x["net_bn"]["personal"] - summary["account"][name[:2]][
            "child_credit_net_A_plus_B" if name.endswith("without_status") else "child_credit_and_status_net"][
            "bn"]["total"]) < 1e-6, value=x["net_bn"]["personal"])
    per_member = by_gen["G3plus"]["personal"] * 1e9 / lineage_counts["identified_g3plus"]
    summary["gates"] = len(GATES)
    item = dict(
        lane="mixed_unit_credits_2026_10_14", income_year=2024, reading="R3_with_status",
        sets="both: the set and the cash set take the same edits (current-year flows)",
        sign=("net_bn, by_generation and a part's cost_bn: positive raises the group's net cost; a part's bn and the "
              "edits: the change to the group's target on the line, so a receipt part's bn is minus its cost_bn"),
        scope=("the identified union on audit row 4's weights (39,712,493 people) at the personal allocation; the 3.04M "
               "added descendants are out of scope (see lineage); the shared cell is 0"),
        reading_rule=("a non-member child's credit continues after the member claimant leaves only where the claimant's "
                      "non-member spouse or a non-member parent of the child stays in the household (R3), and the "
                      "head-of-household status effects (C, Cr) are included"),
        net_bn={"personal": net},
        se_bn={"personal": summary["account"][rec]["child_credit_and_status_net"]["se_bn"]["total"]},
        by_generation=by_gen, parts=parts, edits=edits,
        edits_note=("the receipt edit is listed once for each of the seven federal_liability rules; federal_gap_high_agi "
                    "is absent: its key (observed_liability_plus_positive_gap_high_agi) is not computed here"),
        lineage=dict(g3plus_per_member_usd=per_member, g3plus_term_bn=by_gen["G3plus"]["personal"],
                     identified_g3plus=lineage_counts["identified_g3plus"],
                     rule=("the v7 lane applies it to the lineage's G3+-priced members (later losses plus (1 − C3) of "
                           "the G3-rate attriters); the white-priced part takes 0, not measured")),
        arms=arms,
        beside=dict(joint_split_D_bn=summary["account"][rec]["joint_split_D"]["bn"]["total"],
                    joint_split_D_se_bn=summary["account"][rec]["joint_split_D"]["se_bn"]["total"],
                    state_credits_on_crossing_returns_bound_cps_bn=summary[
                        "state_credits_on_crossing_returns_bound_cps_bn"]),
        gates=GATES)
    alloc.round(12).to_csv(OUT / "allocation_check.csv", index=False, lineterminator="\n")
    (OUT / "item.json").write_text(json.dumps(item, indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
                                   + "\n")
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    for reading in READINGS:
        for name in sets:
            x = summary["account"][reading][name]
            print(f"  {reading} {name:28s} ${x['bn']['total']:+.3f}bn (SE {x['se_bn']['total']:.3f}) "
                  + " ".join(f"{g} {x['bn'][g]:+.3f}" for g in GENS) + f"  [CPS ${x['cps_bn']['total']:+.3f}bn]")
    print("  reverse R1 by why the child stays:", {c: round(v, 3) for c, v in summary["reverse_R1_by_why_the_child_stays_bn"].items()})
    print("  forward A by return type:", {t: round(v, 3) for t, v in summary["forward_A_by_return_type_bn"].items()})
    print("  joint split D by head:", json.dumps(summary["joint_split_D_by_head_bn"]))
    print(f"✓ {len(GATES)} gates passed")


if __name__ == "__main__":
    main()
