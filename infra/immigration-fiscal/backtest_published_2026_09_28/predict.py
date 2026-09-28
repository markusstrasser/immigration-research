"""Phase 1 of the pre-registered back-test: predictions for three published figures.

The account is the adopted September 27 case (`main_case_long_run_2026_09_27`); its frame is CPS ASEC 2025
(income year 2024) and its keys are the executed allocations in `assumption_explorer_2026_09_21/derived/
model.json`. Every key vector is built by the account's own builders, imported read-only:
`generation_account_2026_09_24/frame.py` and `keys.py` (frame, masks, convention (b), MEPS, school and
owner-property keys), `cps_imputation_keys_2026_09_23/common.py` (CPS receipt and spending keys),
`combine_status.py` (the audit's status rules on those keys), `combine_onbooks_lane.py` (audit row 4
weights), `status_impute_2026_09_16/impute_status.py` and `california_medical_status_2026_09_23`'s
state-aware flag.

Checks (BRIEF.md; the firewalled methodology read is reads/aic_methodology.md):
  1. NAE/AIC, "Examining the Economic Contributions of Undocumented Immigrants by Country of Origin"
     (March 2021, ACS 2019): household income, federal and state-local taxes, spending power and payroll
     contributions of Mexican undocumented households. Predicted from the households whose reference
     person is Mexico-born and imputed unauthorized, taxed as the account taxes them (audit row 2's
     on-books shares, row 4's weights, the state-aware flag). A shared-method comparison (both sides impute
     status by a Borjas-style residual and use CBO's federal rates): only a disagreement is informative, on
     income per household, the state distribution and the payroll share. Ratios, state shares and one
     declared 2019->2024 income bridge; no levels are scored.
  2. NAS 2017 Table 8-1 (2013): receipts and outlays per capita of first-generation immigrants and their
     dependents relative to the all-group average (0.79 and 0.90; not blind), on the account's keys under
     the account's conventions and under the report's scenario-1 conventions, with a ladder between them.
  3. CMS HCRIS Worksheet S-10: hospital uncompensated care by state, predicted by the account's
     uninsured-use key (each state's uninsured person-years, the group's at r).

Gates (exit 1): every base receipt and spending key reproduces its model.json cell (relative 1e-9); the
Mexico-born shares under convention (b) reproduce generation_key_shares.json (1e-9); the group's share
of uninsured person-years reproduces the uncompensated-care lane's key share (1e-9); the state totals
add to the national ones; row 4's weights reach the ACS cells; the NIPA splits add to the account's lines.
Outputs: derived/predictions.csv (every frozen number), derived/nas_ratios.csv, derived/hcris_states.csv,
derived/nae_quantities.csv, derived/nae_states.csv, derived/inputs.json (input hashes and gates).
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backtest_published_2026_09_28/predict.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import hashlib  # noqa: E402
import html  # noqa: E402
import json  # noqa: E402
import re  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
sys.path.insert(0, str(FISCAL / "generation_account_2026_09_24"))
import frame as F  # noqa: E402  the account's frame, masks and convention (b)
import keys as K  # noqa: E402  owner_property, meps_keys, school_keys
C = F.C
sys.path.insert(0, str(FISCAL / "cps_imputation_keys_2026_09_23"))
import combine_onbooks_lane as CO  # noqa: E402  row 4 weights; imports the state-aware flag
CS = CO.cs  # combine_status: the audit's status rules on the account's key vectors
sys.path.insert(0, str(FISCAL / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
GEN_SHARES = FISCAL / "generation_account_2026_09_24/derived/generation_key_shares.json"
UC = FISCAL / "uncompensated_care_2026_09_23/derived/summary.json"
ONBOOKS = FISCAL / "onbooks_share_2026_09_23/derived/onbooks_split.csv"
BEA = HERE / "_cache/bea/NipaDataA.txt"
BEA_URL = "https://apps.bea.gov/national/Release/TXT/NipaDataA.txt"
AWI = FISCAL / "external_benchmarks_2026_09_24/_cache/arm3b/awi_plain.html"
ACS = FISCAL / "dataset_integrity_2026_09_23/_cache/acs_person_{}.parquet"
ACS_YEARS = [2021, 2022, 2023, 2024]
ALLOC = ["personal", "shared"]
ENDS = {"personal": "uninsured_use_high", "shared": "uninsured_use_low"}  # specifications 11 and 48
REL = 1e-9
SS_CAP_2024 = 168_600  # the 2024 OASDI taxable maximum, for NAE's statutory payroll rule on 2024 earnings
FAILS: list[str] = []

STATES = {1: "AL", 2: "AK", 4: "AZ", 5: "AR", 6: "CA", 8: "CO", 9: "CT", 10: "DE", 11: "DC", 12: "FL", 13: "GA",
          15: "HI", 16: "ID", 17: "IL", 18: "IN", 19: "IA", 20: "KS", 21: "KY", 22: "LA", 23: "ME", 24: "MD",
          25: "MA", 26: "MI", 27: "MN", 28: "MS", 29: "MO", 30: "MT", 31: "NE", 32: "NV", 33: "NH", 34: "NJ",
          35: "NM", 36: "NY", 37: "NC", 38: "ND", 39: "OH", 40: "OK", 41: "OR", 42: "PA", 44: "RI", 45: "SC",
          46: "SD", 47: "TN", 48: "TX", 49: "UT", 50: "VT", 51: "VA", 53: "WA", 54: "WV", 55: "WI", 56: "WY"}
# States that had not implemented the ACA Medicaid expansion by 1 July of the year (implementation dates:
# MO 1 Oct 2021, OK 1 Jul 2021, SD 1 Jul 2023, NC 1 Dec 2023). [TRAINING-DATA: KFF status tracker; Phase 2
# verifies the dates against KFF before scoring, and KFF's dates govern under the same 1 July rule.]
NOT_EXPANDED = {2021: {"AL", "FL", "GA", "KS", "MS", "MO", "NC", "SC", "SD", "TN", "TX", "WI", "WY"},
                2022: {"AL", "FL", "GA", "KS", "MS", "NC", "SC", "SD", "TN", "TX", "WI", "WY"},
                2023: {"AL", "FL", "GA", "KS", "MS", "NC", "SC", "TN", "TX", "WI", "WY"},
                2024: {"AL", "FL", "GA", "KS", "MS", "SC", "TN", "TX", "WI", "WY"}}

# NAS scenario 1 assigns public goods, interest and congestible services on a per capita basis
# (pp. 364, 389, 472): lines the account keys by something else move to per capita in construction B.
PER_CAPITA_B = ["economic_affairs_services", "agricultural_subsidies", "transport_subsidies", "other_subsidies"]
EXTERNAL = ["foreign_territory_social_benefits", "other_foreign_current_transfers", "foreign_interest"]
# NAS receipts are taxes and social contributions (annex pp. 473-477); these account lines are neither.
NOT_TAXES = ["government_asset_income", "enterprise_surplus", "business_current_transfers",
             "personal_current_transfers", "rest_world_current_transfers", "rest_world_tax_contributions",
             "source_rounding"]


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def sdr(values):
    """160-replicate successive-difference SE (column 0 is the full sample)."""
    values = np.asarray(values, float)
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def rel_ok(got, want):
    return abs(got - want) <= REL * max(abs(want), 1e-12)


# ------------------------------------------------------------------------------------------------------
# Key vectors and their gates
# ------------------------------------------------------------------------------------------------------
def base_vectors(d, civ, index):
    """Per-person key vectors by side and allocation, as keys.py records them."""
    rk = C.receipt_keys(d, index)
    owner, params = K.owner_property(d)
    sk = C.spending_vectors(d, index)
    medical, _, _, _ = K.meps_keys(d)
    edu = K.school_keys(d, civ, params)
    n = len(d)
    out = {}
    for a in ALLOC:
        r = dict(rk[a])
        r.update(modeled_owner_property=owner, resident_population=np.ones(n), none=np.zeros(n))
        s = dict(sk[a])
        s.update(medical)
        s.update(school_operating=edu[a]["school"], postsecondary=edu[a]["P"],
                 education_mix=edu[a]["school"] + edu[a]["P"], external=np.zeros(n))
        out[a] = {"receipt": r, "spending": s}
    return out, params, edu


def key_denominator(key, v, w, civ):
    return F.RESIDENT if key == "resident_population" else float(v[civ] @ w[civ])


def gate_keys(model, vec, w, civ, union):
    """Every executed cell whose key has a per-person vector reproduces its union target (1e-9)."""
    hf = float(w[civ].sum()) / F.RESIDENT
    checked, skipped = 0, set()
    for line in model["receipts"]["lines"]:
        for scenario, cell in line["cells"].items():
            for a in ALLOC:
                c = cell[a]
                key = c["key"]
                if key not in vec[a]["receipt"]:
                    skipped.add(("receipt", key))
                    continue
                v = vec[a]["receipt"][key]
                national = c["target_bn"] + c["other_bn"]
                den = key_denominator(key, v, w, civ)
                got = national * float(v[union] @ w[union]) / den if den else 0.0
                checked += 1
                if not abs(got - c["target_bn"]) <= REL * max(abs(c["target_bn"]), 1.0):
                    gate(f"receipt {line['id']}/{scenario}/{a}/{key}", False, f"{got:.9f} vs {c['target_bn']:.9f}")
    gate(f"{checked} receipt cells reproduce model.json (1e-9)", not FAILS)
    n_fail, checked = len(FAILS), 0
    for line in model["spending"]["lines"]:
        for key, cell in line["keys"].items():
            for a in ALLOC:
                if key not in vec[a]["spending"]:
                    skipped.add(("spending", key))
                    continue
                v = vec[a]["spending"][key]
                den = float(v[civ] @ w[civ])
                got = line["national_bn"] * hf * float(v[union] @ w[union]) / den if den else 0.0
                checked += 1
                want = cell[a]["target_bn"]
                if not abs(got - want) <= REL * max(abs(want), 1.0):
                    gate(f"spending {line['id']}/{key}/{a}", False, f"{got:.9f} vs {want:.9f}")
    gate(f"{checked} spending cells reproduce model.json (1e-9)", len(FAILS) == n_fail)
    # Keys without a per-person vector are union-level splits (justice use, uninsured use, the federal-gap
    # arm); none of them is used below except through generation_key_shares.json.
    print(f"  cells without a per-person vector: {sorted(skipped)}", flush=True)
    return hf


# ------------------------------------------------------------------------------------------------------
# Check 2: NAS 2017 Table 8-1
# ------------------------------------------------------------------------------------------------------
def nas_groups(d, civ):
    """NAS 2017 pp. 387-388 over every resident: independents (18+) in their own generation; dependents
    (under 18) with their co-resident parents' generation, half and half when the parents differ
    (footnote 13's expectation), else the oldest co-resident adult relative's, else their own.
    First = foreign-born (PRCITSHP 4, 5); second = US-born (PRCITSHP 1, 2) with a parent born outside
    the US and its territories; third-plus = everyone else, including the born abroad of US parents."""
    n = len(d)
    fb = d.PRCITSHP.isin([4, 5]).to_numpy()
    us_born = d.PRCITSHP.isin([1, 2]).to_numpy()
    foreign_parent = (~d.PEMNTVTY.isin(F.US_AREAS) | ~d.PEFNTVTY.isin(F.US_AREAS)).to_numpy()
    gen = np.where(fb, 0, np.where(us_born & foreign_parent, 1, 2))
    own = np.zeros((n, 3))
    own[np.arange(n), gen] = 1.0
    parents = F.parent_rows(d)
    age = d.A_AGE.to_numpy()
    family = pd.MultiIndex.from_frame(d[["PH_SEQ", "PF_SEQ"]]).factorize()[0]
    adult = age >= 18
    oldest = pd.DataFrame({"family": family[adult], "age": age[adult], "row": np.flatnonzero(adult)}).sort_values(
        ["family", "age", "row"], ascending=[True, False, True]).drop_duplicates("family").set_index("family").row
    b = own.copy()
    rule = np.full(n, "independent", dtype=object)
    for i in np.flatnonzero(age < 18):
        slots = [p for p in parents[i] if p >= 0]
        if slots:
            b[i] = 0.0
            for p in slots:
                b[i, gen[p]] += 1.0 / len(slots)
            rule[i] = "parents"
        elif family[i] in oldest.index and oldest[family[i]] != i:
            b[i] = 0.0
            b[i, gen[oldest[family[i]]]] = 1.0
            rule[i] = "oldest_relative"
        else:
            rule[i] = "own"
    b[~civ] = 0.0
    return b, gen, rule


def line_shares(vec, W, civ, groups, resident=False):
    """Group shares of a key over the civilian universe, per replicate: dict group -> (161,)."""
    den = np.full(W.shape[1], F.RESIDENT) if resident else vec[civ] @ W[civ]
    return {g: (vec * om) @ W / den for g, om in groups.items()}


def nas_check(d, civ, union, W, model, vec, edu, params, gshares):
    print("[check 2: NAS 2017 Table 8-1]", flush=True)
    b, gen, rule = nas_groups(d, civ)
    omega_b = F.assignments(d, civ, union, F.masks(d)[2])[0]["b"]
    groups = {"nas_first_generation": b[:, 0], "nas_second_generation": b[:, 1], "nas_third_plus": b[:, 2],
              "mexico_born_b": omega_b[:, 0], "all": civ.astype(float)}
    w = W[:, 0]
    pop = {g: om @ W for g, om in groups.items()}
    gate("the three NAS groups partition the civilian universe",
         np.allclose(b[civ].sum(axis=1), 1.0) and abs((pop["nas_first_generation"] + pop["nas_second_generation"]
                                                      + pop["nas_third_plus"] - pop["all"])[0]) < 1e-3)
    n_fail = len(FAILS)
    for a in ALLOC:
        for side, sd in (("receipt", "receipt"), ("spending", "spending")):
            for key, v in vec[a][sd].items():
                entry = gshares["shares"][side][a].get(key)
                if entry is None or not np.any(v[union]):
                    continue
                got = float((v * omega_b[:, 0]) @ w) / float(v[union] @ w[union])
                if not abs(got - entry["b"][0]) <= REL:
                    gate(f"G1(b) share {side}/{a}/{key}", False, f"{got:.12f} vs {entry['b'][0]:.12f}")
    gate("Mexico-born (b) shares reproduce generation_key_shares.json (1e-9)", len(FAILS) == n_fail)

    rlines = model["receipts"]["lines"]
    slines = model["spending"]["lines"]
    rate = pd.Series(params.per_pupil_current_spending)
    # Schools at one national per-pupil cost (NAS: "the per-child cost of education ... is the same for all
    # groups", p. 390 note 16): the account's enrollment vector at the civilian average cost.
    cost = d.GESTFIPS.map(rate).to_numpy(float)
    enrolled = np.divide(edu["personal"]["school"], cost, out=np.zeros(len(d)), where=cost > 0)
    flat = enrolled * float(edu["personal"]["school"][civ] @ w[civ]) / float(enrolled[civ] @ w[civ])
    school_flat = {"personal": flat + edu["personal"]["P"],
                   "shared": C.unit_equal(flat, C.spm_index(d)) + edu["shared"]["P"]}

    # Ladder from the account's conventions (A0) to the report's scenario 1 (B = A5).
    steps = [("A0_account", "the account's keys and conventions: every receipt line keyed to residents; "
                            "external spending lines charged to no resident"),
             ("A1_tax_receipts", "receipts limited to taxes and social contributions"),
             ("A2_services_per_capita", "economic affairs and subsidies per capita"),
             ("A3_external_per_capita", "interest to and transfers abroad per capita"),
             ("A4_corporate_nas_80", "corporate tax 80% on interest and dividends, 20% on wages (scenario nas_80)"),
             ("A5_schools_flat", "one national per-pupil cost (construction B)")]
    rows = []
    for a in ALLOC:
        cache = {}

        def shares_of(key, side, override=None):
            if override is not None:
                v = override
            else:
                v = vec[a][side][key]
            tag = (side, key, id(override))
            if tag not in cache:
                cache[tag] = line_shares(v, W, civ, groups, resident=(key == "resident_population"))
            return cache[tag]

        for k, (step, label) in enumerate(steps):
            scenario = "nas_80" if k >= 4 else "cbo_collective"
            rec = {g: np.zeros(W.shape[1]) for g in groups}
            rtot = 0.0
            for line in rlines:
                if k >= 1 and line["id"] in NOT_TAXES:
                    continue
                c = line["cells"][scenario][a]
                if c["key"] == "none":
                    continue
                national = c["target_bn"] + c["other_bn"]
                s = shares_of(c["key"], "receipt")
                for g in groups:
                    rec[g] += national * s[g]
                rtot += national
            out_ = {g: np.zeros(W.shape[1]) for g in groups}
            stot = 0.0
            for line in slines:
                key = line["preferred_key"]
                override = None
                if k >= 2 and line["id"] in PER_CAPITA_B:
                    key = "population"
                if k >= 3 and line["id"] in EXTERNAL:
                    key = "population"
                if key == "external":
                    continue
                if k >= 5 and key == "education_mix":
                    override = school_flat[a]
                s = shares_of(key, "spending", override)
                for g in groups:
                    out_[g] += line["national_bn"] * s[g]
                stot += line["national_bn"]
            for g in groups:
                per_r = rec[g] / pop[g]
                per_o = out_[g] / pop[g]
                all_r = rec["all"] / pop["all"]
                all_o = out_["all"] / pop["all"]
                ratio_r = per_r / all_r
                ratio_o = per_o / all_o
                rows.append(dict(step=step, label=label, allocation=a, group=g, population_m=pop[g][0] / 1e6,
                                 receipts_bn=rec[g][0], outlays_bn=out_[g][0], receipts_ratio=ratio_r[0],
                                 receipts_ratio_se=sdr(ratio_r), outlays_ratio=ratio_o[0],
                                 outlays_ratio_se=sdr(ratio_o), fiscal_ratio=(rec[g] / out_[g])[0],
                                 receipts_pool_bn=rtot, outlays_pool_bn=stot))
    out = pd.DataFrame(rows)

    # The adopted overrides (justice use, uninsured use at each end) move only the union's cells; for the
    # Mexico-born (b) their effect is the union cell's G1(b) share less the base key's.
    lines = {l["id"]: l for l in slines}
    override = []
    for a in ALLOC:
        for line_id, key, base in [("public_order_safety", "use", "population"),
                                   ("medicaid_and_chip_other_medical", ENDS[a], "medicaid")]:
            cell = lines[line_id]["keys"][key][a]["target_bn"]
            base_cell = lines[line_id]["keys"][base][a]["target_bn"]
            g1 = gshares["shares"]["spending"][a][key]["b"][0]
            g1_base = gshares["shares"]["spending"][a][base]["b"][0]
            override.append(dict(allocation=a, line=line_id, key=key, g1b_bn=cell * g1, g1b_base_bn=base_cell * g1_base,
                                 change_bn=cell * g1 - base_cell * g1_base))
    override = pd.DataFrame(override)
    # Dependents' rule shares in the first-generation group, for the definitional note.
    minors = civ & (d.A_AGE.to_numpy() < 18)
    first_minor_rule = {r: float((b[:, 0] * (minors & (rule == r))) @ W[:, 0]) / 1e6
                        for r in ("parents", "oldest_relative", "own")}
    return out, override, first_minor_rule, gen


# ------------------------------------------------------------------------------------------------------
# Check 3: HCRIS S-10 uncompensated care by state
# ------------------------------------------------------------------------------------------------------
def acs_uninsured(year):
    a = pd.read_parquet(Path(str(ACS).format(year)),
                        columns=["ST", "PWGTP", "HICOV", "HISP", "POBP", "RELSHIPP", "MIL", "AGEP"])
    # Household population less active-duty adults, the CPS civilian universe's nearest ACS counterpart.
    keep = ~a.RELSHIPP.isin([37, 38]) & ~(a.MIL.eq(1) & a.AGEP.ge(17))
    a = a[keep]
    unins = a.HICOV.eq(2)
    group = a.POBP.eq(303) | a.HISP.eq(2)
    by = pd.DataFrame({"ST": a.ST, "u": a.PWGTP * unins, "ug": a.PWGTP * (unins & group),
                       "pop": a.PWGTP}).groupby("ST").sum()
    return by


def hcris_check(d, civ, union, W, uc, W4):
    print("[check 3: HCRIS S-10 by state]", flush=True)
    py = d.NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * d.NOCOV_CYR.eq(2).to_numpy(float)
    full_year = d.NOCOV_CYR.eq(3).to_numpy(float)
    st = d.GESTFIPS.to_numpy()
    w = W[:, 0]
    s_union = float(py[union] @ w[union]) / float(py[civ] @ w[civ])
    gate("the group's share of uninsured person-years reproduces the uncompensated-care key (1e-9)",
         rel_ok(s_union, uc["target_share"]), f"{s_union:.12f} vs {uc['target_share']:.12f}")
    fips = sorted(STATES)
    gate("every civilian record is in one of the 51 states", set(np.unique(st[civ])) == set(fips))
    tot = {}
    for name, v, m in [("py_group", py, civ & union), ("py_other", py, civ & ~union), ("full_year", full_year, civ),
                       ("pop", np.ones(len(d)), civ)]:
        tot[name] = np.vstack([(v * (m & (st == f))) @ W for f in fips])  # 51 x 161
    py_all = tot["py_group"] + tot["py_other"]
    gate("state person-years add to the national total",
         abs(py_all[:, 0].sum() - float(py[civ] @ w[civ])) < 1e-6 * float(py[civ] @ w[civ]))

    def shares(x):
        return x / x.sum(axis=0)

    r07 = 0.7 * tot["py_group"] + tot["py_other"]
    pred = {"account_r1": shares(py_all), "account_r07": shares(r07), "baseline_uninsured_count": shares(tot["full_year"]),
            "baseline_population": shares(tot["pop"])}
    g = tot["py_group"] / py_all
    rows = []
    for j, f in enumerate(fips):
        row = dict(fips=f, state=STATES[f], py_group=tot["py_group"][j, 0], py_other=tot["py_other"][j, 0],
                   full_year_uninsured=tot["full_year"][j, 0], population=tot["pop"][j, 0],
                   group_share_of_uninsured=g[j, 0], group_share_se=sdr(g[j]))
        for k, v in pred.items():
            row[k] = v[j, 0]
            row[k + "_se"] = sdr(v[j])
        for y, ne in NOT_EXPANDED.items():
            row[f"not_expanded_{y}"] = int(STATES[f] in ne)
        rows.append(row)
    states = pd.DataFrame(rows)
    # Variant: audit row 4's weights, under which the adopted tax block recomputes the uninsured-use share.
    w4 = W4[:, 0]
    py4 = np.array([(py * (civ & (st == f))) @ w4 for f in fips])
    pyg4 = np.array([(py * (civ & union & (st == f))) @ w4 for f in fips])
    states["account_r1_row4"] = py4 / py4.sum()
    states["group_share_of_uninsured_row4"] = pyg4 / py4
    # Year-matched ACS counts (uninsured at interview): the account's key on ACS counts, and the ACS group
    # share among the uninsured (Mexico-born or Mexican origin), as the Phase 2 variant for year Y.
    for y in ACS_YEARS:
        by = acs_uninsured(y).reindex(fips)
        if by.isna().any().any():
            raise SystemExit(f"[BLOCKED] ACS {y} misses a state")
        states[f"acs{y}_uninsured_share"] = (by.u / by.u.sum()).to_numpy()
        states[f"acs{y}_account_r07"] = ((0.7 * by.ug + (by.u - by.ug)) / (0.7 * by.ug + (by.u - by.ug)).sum()).to_numpy()
        states[f"acs{y}_group_share_of_uninsured"] = (by.ug / by.u).to_numpy()
    # The slope the 0.7 key implies for the r = 1 key's log errors, weighted by the predicted share (primary)
    # and unweighted: the alternative hypothesis, frozen here.
    x = states.group_share_of_uninsured.to_numpy()
    e07 = np.log(states.account_r07 / states.account_r1).to_numpy()
    wt = states.account_r1.to_numpy()
    implied = {}
    for label, ww in (("weighted", wt), ("unweighted", np.ones(len(x)))):
        X = np.column_stack([np.ones(len(x)), x])
        beta = np.linalg.lstsq(X * np.sqrt(ww)[:, None], e07 * np.sqrt(ww), rcond=None)[0]
        xb = np.average(x, weights=ww)
        implied[label] = dict(slope_r07=float(beta[1]), sxx=float(np.sum(ww / ww.sum() * (x - xb) ** 2)),
                              sxx_unnormalized=float(np.sum(ww * (x - xb) ** 2)))
    # Prior standard error of the slope for a residual SD sigma per state (weighted: an average-weight
    # state's SD, Var(e_j) = sigma^2 / (n w_j)).
    n = len(x)
    power = []
    for sigma in (0.2, 0.3, 0.4):
        se_w = sigma / np.sqrt(n * implied["weighted"]["sxx"])
        se_u = sigma / np.sqrt(implied["unweighted"]["sxx_unnormalized"])
        power.append(dict(sigma=sigma, se_weighted=float(se_w), se_unweighted=float(se_u),
                          detectable_weighted=bool(abs(implied["weighted"]["slope_r07"]) >= 2.8 * se_w),
                          detectable_unweighted=bool(abs(implied["unweighted"]["slope_r07"]) >= 2.8 * se_u)))
    national = {y: uc["aha_national_bn"] * uc["uplift_2024"] ** ((y - 2020) / 4) for y in (2021, 2022, 2023, 2024)}
    return states, implied, power, national, s_union


# ------------------------------------------------------------------------------------------------------
# Check 1: NAE/AIC 2021, undocumented Mexican households
# ------------------------------------------------------------------------------------------------------
def bea_2024():
    if not BEA.exists():
        raise SystemExit(f"[BLOCKED] missing {BEA}; fetch {BEA_URL} into _cache/bea/")
    series = {"B075RC": "federal_corporate", "B102RC": "state_local_corporate", "W025RC": "all_corporate",
              "B234RC": "federal_excise", "LA000239": "state_local_excise", "B235RC": "customs",
              "LA000237": "federal_other_production", "LA000357": "state_local_other_production"}
    out = {}
    for line in BEA.read_text().splitlines():
        code, _, rest = line.partition(",")
        if code in series and rest.startswith("2024,"):
            out[series[code]] = float(rest.split(",", 1)[1].strip('"').replace(",", "")) / 1e3
    if set(out) != set(series.values()):
        raise SystemExit(f"[BLOCKED] BEA series missing: {set(series.values()) - set(out)}")
    return out


def awi():
    text = html.unescape(re.sub(r"<[^>]+>", " ", AWI.read_text(encoding="utf-8", errors="replace")))
    out = {}
    for y in (2019, 2024):
        m = re.search(rf"\b{y}\s+([0-9,]+\.[0-9]{{2}})", text)
        if not m:
            raise SystemExit(f"[BLOCKED] SSA average wage index {y} not found in {AWI}")
        out[y] = float(m.group(1).replace(",", ""))
    return out


def onbooks_shares():
    split = pd.read_csv(ONBOOKS).set_index("kind")
    return {case: (float(split.loc[f"evidence_{case}", "s_mex"]), float(split.loc[f"evidence_{case}", "s_oth"]))
            for case in ("low", "central", "high")}


def tax_types(model, bea):
    """Account receipt lines mapped to NAE's categories, with NIPA 2024 level splits.
    Each entry: (line, key, fraction of the line's national amount)."""
    rl = {l["id"]: l for l in model["receipts"]["lines"]}
    fed_corp = bea["federal_corporate"] / bea["all_corporate"]
    fed_exc = bea["federal_excise"] / (bea["federal_excise"] + bea["state_local_excise"])
    fed_oth = bea["federal_other_production"] / (bea["federal_other_production"] + bea["state_local_other_production"])
    se_oasdi = .124 / .153
    return {
        "federal_income_tax": [("federal_income_tax", 1.0)],
        "social_security": [("employee_oasdi", 1.0), ("employer_oasdi", 1.0), ("self_employment_oasdi_hi", se_oasdi)],
        "medicare": [("employee_hi", 1.0), ("employer_hi", 1.0), ("self_employment_oasdi_hi", 1 - se_oasdi)],
        "federal_corporate": [("corporate_capital", fed_corp), ("corporate_labor", fed_corp)],
        "federal_excise": [("excise_selective_sales", fed_exc)],
        "customs": [("customs_duties", 1.0)],
        "other_social_contributions": [("other_domestic_social_contributions", 1.0)],
        "state_local_income": [("state_local_income_tax", 1.0), ("other_personal_tax", 1.0)],
        "state_local_sales_excise": [("general_sales_tax", 1.0), ("excise_selective_sales", 1 - fed_exc)],
        "state_local_property": [("modeled_owner_property", 1.0), ("personal_property_tax", 1.0),
                                 ("remaining_production_property", 1.0)],
        "state_local_other": [("personal_motor_vehicle", 1.0), ("other_production_taxes", 1 - fed_oth),
                              ("corporate_capital", 1 - fed_corp), ("corporate_labor", 1 - fed_corp)],
    }, dict(federal_corporate_fraction=fed_corp, federal_excise_fraction=fed_exc,
            federal_other_production_fraction=fed_oth,
            check_corporate=abs(rl["corporate_capital"]["national_bn"] + rl["corporate_labor"]["national_bn"]
                                - bea["all_corporate"]) < 1e-3,
            check_excise=abs(rl["excise_selective_sales"]["national_bn"] - bea["federal_excise"]
                             - bea["state_local_excise"]) < 1e-3,
            check_other=abs(rl["other_production_taxes"]["national_bn"] - bea["federal_other_production"]
                            - bea["state_local_other_production"]) < 1e-3,
            check_customs=abs(rl["customs_duties"]["national_bn"] - bea["customs"]) < 1e-3)


READINGS = {
    # CBO's federal taxes (individual income, payroll, corporate, excise; S8), NAE's likely rate base.
    "federal_A_cbo_scope": ["federal_income_tax", "social_security", "medicare", "federal_corporate", "federal_excise"],
    # The column's literal label: federal individual income tax only.
    "federal_B_income_tax": ["federal_income_tax"],
    "state_local": ["state_local_income", "state_local_sales_excise", "state_local_property", "state_local_other"],
}


def nae_check(d, civ, W, model, vec_status_fn, types, weights, heads_by):
    """Quantities for the households headed by each flagged reference person, per weight set and case.
    heads_by values: (reference persons, status mask for the rule, on-books shares, case, the Mexico-born
    persons imputed unauthorized, NAE's person count)."""
    rl = {l["id"]: l for l in model["receipts"]["lines"]}
    hh = d.PH_SEQ.to_numpy()
    income = d.PTOTVAL.to_numpy(float)
    # NAE's payroll rule (reads Q3): 12.4% to the taxable maximum and 2.9% on each earner's wages, or on
    # self-employment income for the self-employed, statutory and before any discount.
    earn = d.WSAL_VAL.clip(lower=0).to_numpy(float) + (d.SEMP_VAL + d.FRSE_VAL).clip(lower=0).to_numpy(float)
    statutory = 0.124 * np.minimum(earn, SS_CAP_2024) + 0.029 * earn
    rows, state_rows = [], []
    st = d.GESTFIPS.to_numpy()
    for wname, Wx in weights.items():
        for sname, (heads, unauth, s_arr, case, persons) in heads_by.items():
            members = np.isin(hh, hh[heads]) & civ
            rk = vec_status_fn(unauth, s_arr)
            households = heads.astype(float) @ Wx
            hi = (income * members) @ Wx
            count = persons.astype(float) @ Wx
            base = dict(weights=wname, status=sname, onbooks_case=case)
            rows.append(dict(base, quantity="households_m", value=households[0] / 1e6, se=sdr(households / 1e6)))
            rows.append(dict(base, quantity="persons_m", value=float(members @ Wx[:, 0]) / 1e6,
                             se=sdr(members.astype(float) @ Wx / 1e6)))
            rows.append(dict(base, quantity="mexico_born_unauthorized_m", value=count[0] / 1e6, se=sdr(count / 1e6)))
            rows.append(dict(base, quantity="household_income_bn", value=hi[0] / 1e9, se=sdr(hi / 1e9)))
            for qname, ratio in (("income_per_household", hi / households),
                                 ("income_per_unauthorized_person", hi / count),
                                 ("earnings_share_of_income", ((earn * members) @ Wx) / hi),
                                 ("statutory_payroll_over_income", ((statutory * members) @ Wx) / hi),
                                 ("statutory_payroll_halved_over_income", ((statutory * members) @ Wx) / hi / 2),
                                 # Descriptive: the unauthorized Mexico-born earners' payroll only (reads, unanswered 8).
                                 ("statutory_payroll_unauthorized_only_over_income",
                                  ((statutory * (members & persons)) @ Wx) / hi)):
                rows.append(dict(base, quantity=qname, value=ratio[0], se=sdr(ratio)))
            amounts = {}
            for a in ALLOC:
                keys_a = rk[a]
                for tname, parts in types.items():
                    total = np.zeros(Wx.shape[1])
                    for line_id, frac in parts:
                        cell = rl[line_id]["cells"]["cbo_collective"][a]
                        v = keys_a[cell["key"]]
                        national = (cell["target_bn"] + cell["other_bn"]) * frac
                        total = total + national * ((v * members) @ Wx) / (v[civ] @ Wx[civ])
                    amounts[(a, tname)] = total
                    rows.append(dict(base, quantity=f"{tname}_bn", allocation=a, value=total[0], se=sdr(total)))
                for rname, parts in READINGS.items():
                    total = sum(amounts[(a, t)] for t in parts)
                    rows.append(dict(base, quantity=f"{rname}_bn", allocation=a, value=total[0], se=sdr(total)))
                    ratio = total * 1e9 / hi
                    rows.append(dict(base, quantity=f"{rname}_over_income", allocation=a, value=ratio[0], se=sdr(ratio)))
                sl = sum(amounts[(a, t)] for t in READINGS["state_local"])
                for reading in ("federal_A_cbo_scope", "federal_B_income_tax"):
                    fed = sum(amounts[(a, t)] for t in READINGS[reading])
                    sp = hi / 1e9 - fed - sl
                    rows.append(dict(base, quantity=f"spending_power_{reading[8]}_bn", allocation=a, value=sp[0], se=sdr(sp)))
                    ratio = sp * 1e9 / hi
                    rows.append(dict(base, quantity=f"spending_power_{reading[8]}_over_income", allocation=a,
                                     value=ratio[0], se=sdr(ratio)))
                for t in ("social_security", "medicare"):
                    ratio = amounts[(a, t)] * 1e9 / hi
                    rows.append(dict(base, quantity=f"{t}_over_income", allocation=a, value=ratio[0], se=sdr(ratio)))
                ratio = (amounts[(a, "social_security")] + amounts[(a, "medicare")]) * 1e9 / hi
                rows.append(dict(base, quantity="payroll_over_income", allocation=a, value=ratio[0], se=sdr(ratio)))
            # State shares of household income (the household's state).
            for f in sorted(STATES):
                m = members & (st == f)
                share = ((income * m) @ Wx) / hi
                state_rows.append(dict(weights=wname, status=sname, onbooks_case=case, fips=f, state=STATES[f],
                                       income_share=share[0], income_share_se=sdr(share)))
    return pd.DataFrame(rows), pd.DataFrame(state_rows)


def tolerances(p, implied):
    """The declared scoring rules with their numeric bounds (PREDICTIONS.md states them in words)."""
    def val(check, item, construction, allocation=None):
        q = p[(p.check == check) & (p.item == item) & (p.construction == construction)]
        if allocation is not None:
            q = q[q.allocation == allocation]
        return q.value.to_numpy(float)

    out = {"check1": {}, "check2": {}, "check3": {}}
    out["check1"]["label"] = ("shared-method comparison, not an independent test: NAE and the account both impute status "
                              "by a Borjas-style residual and use CBO's federal rates, so agreement cannot validate "
                              "the account; only a disagreement is informative. Outcomes are 'finding' or 'no finding'.")
    per_household = val(1, "income_per_household_2019", "account_bridged_central")[0]
    per_person = val(1, "income_per_unauthorized_person_2019", "account_bridged_central")[0]
    out["check1"]["income_per_household"] = dict(
        rule="NAE's household income over its household count if the report states one, else over its count of "
             "Mexican immigrants lacking legal status (the account's value on the same denominator); finding if "
             "outside [0.80, 1.25] x the account's 2024 value times the central bridge; otherwise no finding",
        per_household=dict(low=0.8 * per_household, high=1.25 * per_household),
        per_unauthorized_person=dict(low=0.8 * per_person, high=1.25 * per_person))
    s = val(1, "statutory_payroll_over_income", "account")[0]
    out["check1"]["payroll_share"] = dict(
        rule="NAE's (Social Security + Medicare) over household income, United States row; no finding if inside "
             "[0.85, 1.15] x S (statutory rates on all members' earnings, NAE's standard rule) or inside "
             "[0.85, 1.15] x S/2 (the same, halved by the filing discount); finding otherwise",
        S=s, band_statutory=[0.85 * s, 1.15 * s], band_halved=[0.85 * s / 2, 1.15 * s / 2])
    out["check1"]["state_shares"] = dict(
        rule="D = total variation distance over NAE's listed states plus one 'rest' cell, NAE's shares of its "
             "United States row against the account's; no finding if D <= 0.08 and D < D(baseline); finding if "
             "D > 0.15 or D >= D(baseline); otherwise partial", agree_max=0.08, finding_min=0.15,
        baseline="baseline_mexico_born_population")
    # Tax ratios: the conventions differ in a known direction (NAE halves CBO and ITEP average rates), so a gap
    # in that direction is expected; a gap the other way beyond the band is a finding.
    conventions = {}
    for item, expected in (("federal_A_cbo_scope_over_income", "lower"), ("state_local_over_income", "lower"),
                           ("spending_power_A_over_income", "higher")):
        v = val(1, item, "account")
        conventions[item] = (dict(expected="NAE lower", finding_if_above=1.25 * v.max()) if expected == "lower"
                             else dict(expected="NAE higher", finding_if_below=v.min() - 0.03))
    conventions["federal_B_income_tax_over_income"] = dict(
        expected="NAE lower", finding_if_above=None,
        note="reported only: NAE's federal column is reading A or B (reads Q3), so the reading-A bound decides")
    out["check1"]["convention_ratios"] = conventions
    for group in ("nas_first_generation",):
        for m in ("receipts_ratio", "outlays_ratio"):
            v = val(2, f"{group}_{m}", "A5_schools_flat")
            out["check2"][f"{group}_{m}"] = dict(rule="hit if NAS is within 0.05 of both allocations (not blind)",
                                                 low=v.max() - 0.05, high=v.min() + 0.05, nas_2013={"receipts_ratio": 0.79,
                                                                                                    "outlays_ratio": 0.90}[m])
    out["check3"]["level"] = dict(
        rule="TVD between the S-10 state shares and account_r1; hit if TVD <= 0.15 and TVD <= 0.8 x TVD(population); "
             "miss if TVD > 0.25 or TVD >= TVD(population); otherwise partial", hit_max=0.15, miss_min=0.25,
        beat_population_factor=0.8)
    out["check3"]["slope"] = dict(
        rule="WLS of ln(S10 share / account_r1) on the group's share of the state's uninsured person-years, weights "
             "account_r1, HC1 errors, with the expansion indicator for year Y (primary) and without; 95% CI contains 0 "
             "and excludes the alternative: consistent with the adopted key; contains the alternative and excludes 0: "
             "favors r = 0.7; contains both: no power; excludes both: miss",
        null=0.0, alternative_weighted=implied["weighted"]["slope_r07"],
        alternative_unweighted=implied["unweighted"]["slope_r07"])
    out["check3"]["national"] = dict(rule="hit if S-10 national line 30 over account_N(Y) is inside [0.8, 1.25]",
                                     account_N={int(i.rsplit('_', 1)[1]): float(v) for i, v in
                                                p[p.item.str.startswith("national_uncompensated_care_")][["item", "value"]]
                                                .itertuples(index=False)}, low=0.8, high=1.25)
    out["check3"]["year_rule"] = ("latest cost-report year whose report count is at least 95% of the year before; "
                                  "the counts are read before any state total is formed")
    return out


# ------------------------------------------------------------------------------------------------------
def main():
    print("[frame and keys]", flush=True)
    d = F.load()
    civ, union, gens = F.masks(d)
    W = d[F.REPS].to_numpy(float)
    w = W[:, 0]
    index = C.spm_index(d)
    model = json.loads(MODEL.read_text())
    gshares = json.loads(GEN_SHARES.read_text())
    uc = json.loads(UC.read_text())
    vec, params, edu = base_vectors(d, civ, index)
    gate_keys(model, vec, w, civ, union)

    nas, override, first_minor_rule, _ = nas_check(d, civ, union, W, model, vec, edu, params, gshares)
    print("[audit row 4 weights]", flush=True)
    cells = CO.acs_cells()
    arms, info = CO.weight_arms(d, W, cells)
    W4 = arms["row4"]
    mex = d.PENATVTY.eq(303).to_numpy()
    catx = d.GESTFIPS.isin(CO.CA_TX).to_numpy()
    for gname, m in (("natz", mex & ~catx & d.PRCITSHP.eq(4).to_numpy()), ("noncit", mex & ~catx & d.PRCITSHP.eq(5).to_numpy())):
        gate(f"row 4 weights reach the ACS 2024 cell ({gname})", np.allclose(W4[m].sum(axis=0), cells[gname], rtol=1e-9))
    states, implied, power, national_uc, s_union = hcris_check(d, civ, union, W, uc, W4)

    print("[check 1: NAE 2021 undocumented Mexican households]", flush=True)
    bea = bea_2024()
    types, splits = tax_types(model, bea)
    gate("NIPA 2024 splits add to the account's corporate, excise, other-production and customs lines",
         splits["check_corporate"] and splits["check_excise"] and splits["check_other"] and splits["check_customs"])
    hh_fields = d[["H_SEQ", "HPUBLIC", "HLORENT"]].drop_duplicates("H_SEQ")
    paper = impute(d, hh_fields)["unauthorized"]
    aware_frame = d.assign(state=d.GESTFIPS)
    aware_frame.loc[CO.blind_mask(aware_frame, CO.STATUS_BLIND_2024), "MCAID"] = 2
    aware = impute(aware_frame, hh_fields)["unauthorized"]
    latin = d.PENATVTY.between(302, 399).to_numpy() & ~d.PENATVTY.eq(327).to_numpy()
    gate("paper rules reproduce the status lane's Mexico-born unauthorized in the union (4,567,144)",
         round(float(w[paper & mex & union].sum())) == 4567144, f"{w[paper & mex & union].sum():,.0f}")
    ref = d.PERRP.isin([40, 41]).to_numpy() & d.PRCITSHP.isin([4, 5]).to_numpy() & mex
    ob = onbooks_shares()
    heads_by = {}
    for sname, un in (("state_aware", aware), ("paper_rules", paper)):
        for case in ("low", "central", "high"):
            s_arr = np.where(mex, ob[case][0], ob[case][1])
            heads_by[(sname, case)] = (ref & un, un & latin, s_arr, case, un & mex & civ)

    def status_keys(unauth, s_arr):
        rk, _ = CS.status_vectors(d, unauth, s_arr, index)
        for a in ALLOC:
            rk[a]["modeled_owner_property"] = vec[a]["receipt"]["modeled_owner_property"]
        return rk

    nae_rows, nae_states = [], []
    for wname, Wx in (("row4", W4), ("published", W)):
        cases = [k for k in heads_by if wname == "row4" or k == ("state_aware", "central")]
        q, s = nae_check(d, civ, Wx, model, status_keys, types, {wname: Wx},
                         {f"{k[0]}|{k[1]}": heads_by[k] for k in cases})
        nae_rows.append(q)
        nae_states.append(s)
    # The account's raw keys (no status rule) for the same state-aware households: the rule's effect.
    heads, _, _, _, persons = heads_by[("state_aware", "central")]
    q, s = nae_check(d, civ, W4, model, lambda unauth, s_arr: {a: vec[a]["receipt"] for a in ALLOC}, types,
                     {"row4": W4}, {"state_aware|raw_keys": (heads, None, None, "raw", persons)})
    nae_rows.append(q)
    nae_states.append(s)
    nae = pd.concat(nae_rows, ignore_index=True)
    nae["status"] = nae.status.str.split("|").str[0]
    nae_state = pd.concat(nae_states, ignore_index=True)
    nae_state["status"] = nae_state.status.str.split("|").str[0]
    # Naive baselines: all Mexico-born persons' state distribution; national average rates on money income.
    mex_all = mex & d.PRCITSHP.isin([4, 5]).to_numpy() & civ
    base_state = pd.DataFrame([dict(fips=f, state=STATES[f],
                                    mexico_born_share=float(W4[mex_all & (d.GESTFIPS.to_numpy() == f), 0].sum())
                                    / float(W4[mex_all, 0].sum())) for f in sorted(STATES)])
    money = float(d.PTOTVAL.to_numpy(float)[civ] @ w[civ]) / 1e9
    rl = {l["id"]: l for l in model["receipts"]["lines"]}
    national_tax = {t: sum(rl[l]["national_bn"] * frac for l, frac in parts) for t, parts in types.items()}
    naive = {r: sum(national_tax[t] for t in parts) / money for r, parts in READINGS.items()}
    # The declared 2024 -> 2019 bridge for income per household or per person (no count enters it): SSA's
    # average wage index, ACS over CPS income, and the group's wage growth against the index (both INFERENCE).
    wage_idx = awi()
    bridge = dict(awi_2019=wage_idx[2019], awi_2024=wage_idx[2024], awi_ratio=wage_idx[2019] / wage_idx[2024],
                  acs_over_cps_income=(0.95, 0.90, 1.00), group_vs_awi_2019_over_2024=(1.0, 0.95, 1.05))
    for i, k in enumerate(("central", "low", "high")):
        bridge[k] = bridge["awi_ratio"] * bridge["acs_over_cps_income"][i] * bridge["group_vs_awi_2019_over_2024"][i]

    # ------------------------------------------------------------------ outputs
    OUT.mkdir(parents=True, exist_ok=True)
    nas.to_csv(OUT / "nas_ratios.csv", index=False, lineterminator="\n")
    states.to_csv(OUT / "hcris_states.csv", index=False, lineterminator="\n")
    nae.to_csv(OUT / "nae_quantities.csv", index=False, lineterminator="\n")
    nae_state = nae_state.merge(base_state, on=["fips", "state"], how="left")
    nae_state.to_csv(OUT / "nae_states.csv", index=False, lineterminator="\n")

    pred = []

    def add(check, item, construction, value, se=np.nan, allocation="", unit="", tag="CALCULATION", note=""):
        pred.append(dict(check=check, item=item, construction=construction, allocation=allocation, value=value,
                         se=se, unit=unit, tag=tag, note=note))

    # Check 1 (shared method; ratios, state shares and the bridge only; levels stay descriptive in
    # nae_quantities.csv): primary = row 4 weights, state-aware status, central on-books share.
    prim = nae.query("weights == 'row4' and status == 'state_aware' and onbooks_case == 'central'")
    scored = prim[prim.quantity.str.endswith("_over_income")
                  & ~prim.quantity.eq("statutory_payroll_unauthorized_only_over_income")]
    for _, r in scored.iterrows():
        add(1, r.quantity, "account", r.value, r.se, r.allocation if isinstance(r.allocation, str) else "", "ratio")
    tax_ratios = [f"{q}_over_income" for q in (*READINGS, "spending_power_A", "spending_power_B", "payroll")]
    for case in ("low", "high"):
        sub = nae.query("weights == 'row4' and status == 'state_aware' and onbooks_case == @case")
        for _, r in sub[sub.quantity.isin(tax_ratios)].iterrows():
            add(1, r.quantity, f"account_onbooks_{case}", r.value, r.se, r.allocation, "ratio")
    raw = nae.query("onbooks_case == 'raw'")
    for _, r in raw[raw.quantity.isin(tax_ratios)].iterrows():
        add(1, r.quantity, "account_raw_keys", r.value, r.se, r.allocation, "ratio",
            note="no status rule: every CPS wage on the books")
    for rname, v in naive.items():
        add(1, f"{rname}_over_income", "baseline_national_average_rate", v, unit="ratio",
            note="national line totals over CPS money income of the civilian universe")
        if rname != "state_local":
            add(1, f"spending_power_{rname[8]}_over_income", "baseline_national_average_rate",
                1 - v - naive["state_local"], unit="ratio")
    add(1, "payroll_over_income", "baseline_national_average_rate",
        (national_tax["social_security"] + national_tax["medicare"]) / money, unit="ratio")
    for k in ("central", "low", "high"):
        add(1, "bridge_2024_to_2019", k, bridge[k], unit="factor",
            note="SSA AWI 2019/2024 x ACS/CPS income x the group's wage growth against the AWI (INFERENCE on the last two)")
    # Income per household, and per Mexico-born person imputed unauthorized (NAE's count). Naive baselines:
    # the national mean money income per household and per person.
    national_heads = civ & d.PERRP.isin([40, 41]).to_numpy()
    for qname, den in (("income_per_household", national_heads), ("income_per_unauthorized_person", civ)):
        r = prim.query("quantity == @qname").iloc[0]
        add(1, qname, "account", r.value, r.se, unit="$ 2024")
        for k in ("central", "low", "high"):
            add(1, f"{qname}_2019", f"account_bridged_{k}", r.value * bridge[k], unit="$ 2019")
        add(1, f"{qname}_2019", "baseline_national_mean_bridged_central",
            money * 1e9 / float(w[den].sum()) * bridge["central"], unit="$ 2019",
            note="CPS money income of the civilian universe per household (per person for the per-person item)")
    ps = nae_state.query("weights == 'row4' and status == 'state_aware' and onbooks_case == 'central'")
    for _, r in ps.iterrows():
        add(1, f"income_share_{r.state}", "account", r.income_share, r.income_share_se, unit="share")
        add(1, f"income_share_{r.state}", "baseline_mexico_born_population", r.mexico_born_share, unit="share")

    # Check 2.
    for _, r in nas.iterrows():
        if r.group in ("nas_first_generation", "mexico_born_b"):
            for m in ("receipts_ratio", "outlays_ratio"):
                add(2, f"{r.group}_{m}", r.step, r[m], r[m + "_se"], r.allocation, "ratio")
    inc = d.PTOTVAL.to_numpy(float)
    b, _, _ = nas_groups(d, civ)
    for gname, om in (("nas_first_generation", b[:, 0]),
                      ("mexico_born_b", F.assignments(d, civ, union, gens)[0]["b"][:, 0])):
        ratio = ((inc * om) @ W / (om @ W)) / ((inc * civ) @ W / (civ.astype(float) @ W))
        add(2, f"{gname}_receipts_ratio", "baseline_income_proportional", ratio[0], sdr(ratio), unit="ratio")
        add(2, f"{gname}_outlays_ratio", "baseline_per_capita", 1.0, unit="ratio")
    for _, r in override.iterrows():
        add(2, f"mexico_born_b_override_{r.line}", f"adopted_key_{r.key}", r.change_bn, allocation=r.allocation,
            unit="$bn 2024", note="G1(b) share of the union cell less the base key's")

    # Check 3.
    for _, r in states.iterrows():
        for k in ("account_r1", "account_r07", "baseline_uninsured_count", "baseline_population"):
            add(3, f"share_{r.state}", k, r[k], r[k + "_se"], unit="share of national S-10 total")
        add(3, f"group_share_of_uninsured_{r.state}", "regressor", r.group_share_of_uninsured, r.group_share_se,
            unit="share")
    for label, v in implied.items():
        add(3, f"slope_implied_by_r07_{label}", "alternative_hypothesis", v["slope_r07"], unit="log points per unit share")
        add(3, f"slope_adopted_{label}", "null_hypothesis", 0.0, unit="log points per unit share")
    for p in power:
        add(3, "prior_slope_se_weighted", f"sigma_{p['sigma']}", p["se_weighted"], unit="log points per unit share")
        add(3, "prior_slope_se_unweighted", f"sigma_{p['sigma']}", p["se_unweighted"], unit="log points per unit share")
    for y, v in national_uc.items():
        add(3, f"national_uncompensated_care_{y}", "account_N", v, unit="$bn",
            note="AHA 2020 cost basis x the account's 1.20 uplift over 2020-2024, geometric by year")
    add(3, "group_share_of_uninsured_person_years", "account", s_union, unit="share")
    pred_df = pd.DataFrame(pred)
    pred_df.to_csv(OUT / "predictions.csv", index=False, lineterminator="\n")
    (OUT / "tolerances.json").write_text(json.dumps(tolerances(pred_df, implied), indent=1, default=float) + "\n")

    inputs = {
        "cps_zip_sha256": F.CPS_SHA,
        "files": {str(p.relative_to(ROOT)): sha(p) for p in
                  [MODEL, GEN_SHARES, UC, ONBOOKS, BEA, AWI, *[Path(str(ACS).format(y)) for y in ACS_YEARS]]},
        "bea_2024_bn": bea, "nipa_splits": {k: v for k, v in splits.items() if not k.startswith("check")},
        "onbooks_shares_mexico_other": ob, "row4": info, "bridge": bridge, "naive_rates": naive,
        "money_income_bn": money, "nas_first_generation_minors_m": first_minor_rule,
        "hcris_implied_slopes": implied, "hcris_prior_power": power,
        "gates_failed": FAILS,
    }
    (OUT / "inputs.json").write_text(json.dumps(inputs, indent=1, sort_keys=True, default=float) + "\n")
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print(f"  ✓ all gates passed; {len(pred)} predictions written")


if __name__ == "__main__":
    main()
