"""Checks for mixed_unit_credits_2026_10_14: the 2024 rules against hand values and the cached IRS texts, the
hand-checked example return, and the conservation of credits and the sets in derived/summary.json.

  uv run --no-project python3 -m pytest infra/immigration-fiscal/mixed_unit_credits_2026_10_14/test_credits.py -q
"""
import importlib.util
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

LANE = Path(__file__).resolve().parent
DER = LANE / "derived"
CACHE = LANE / "_cache"
_spec = importlib.util.spec_from_file_location("mixed_unit_credits", LANE / "credits.py")
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
TEXTS = {"rp": CACHE / "irs_rp_2023_34/rp-23-34.txt", "s8812": CACHE / "irs_s8812_2024/f1040s8--2024.txt",
         "f2441": CACHE / "irs_f2441_2024/f2441--2024.txt"}


def arr(*x):
    return np.array(x, dtype=float)


def text(name):
    path = TEXTS[name]
    if not path.exists():
        pytest.skip(f"{path} is an ignored download (credits.py's comments name the source and its sha256)")
    return " ".join(path.read_text().split())


def money(x):
    return f"${x:,.0f}"


# ---------------------------------------------------------------------------------------------------------------------
# rules by hand
# ---------------------------------------------------------------------------------------------------------------------
def test_rate_schedule_hand_values():
    got = C.schedule(arr(10402, 3102, 100000), np.array(["single", "hoh", "joint"]))
    # 10% of 10,402; 10% of 3,102; 2,320 + 12% of 71,100 + 22% of 5,700
    assert np.allclose(got, [1040.2, 310.2, 2320 + 8532 + 1254])


def test_child_credits_hand_values():
    # the example return: head of household, one child under 17, tax before credits $310, wages $25,002
    nonref, actc = C.child_credits(np.array(["hoh"]), arr(25002), arr(310), arr(25002), arr(1), arr(0))
    assert (nonref[0], actc[0]) == (310, 1690)
    # $50 per $1,000 (or part) of AGI over $400,000 joint: $410,500 takes $550 of $2,000
    nonref, actc = C.child_credits(np.array(["joint"]), arr(410500), arr(1e6), arr(410500), arr(1), arr(0))
    assert (nonref[0], actc[0]) == (1450, 0)
    # refundable part: at most $1,700 per child under 17 and 15% of earnings over $2,500; a $500 dependent is not refundable
    nonref, actc = C.child_credits(np.array(["single", "single"]), arr(12000, 60000), arr(0, 0), arr(12000, 60000),
                                   arr(1, 2), arr(0, 1))
    assert np.allclose(nonref, 0) and np.allclose(actc, [0.15 * 9500, 3400])


def test_eitc_reproduces_the_rev_proc_maximum_and_completed_phaseouts():
    for n, (pin, pout, amount, maximum, th_other, th_joint) in C.EITC.items():
        assert round(pin * amount) == maximum
        for joint, th, done in [(False, th_other, C.EITC_COMPLETED[n][0]), (True, th_joint, C.EITC_COMPLETED[n][1])]:
            assert abs(th + maximum / pout - done) < 1
            e = C.eitc(arr(n, n), arr(amount, done + 1), arr(amount, done + 1), np.array([joint, joint]), arr(0, 0),
                       np.array([True, True]))
            assert abs(e[0] - maximum) < 1 and e[1] == 0


def test_eitc_hand_values_and_limits():
    one = dict(joint=np.array([False]), investment=arr(0), age_ok=np.array([True]))
    # the example: 34% of $25,002 capped at $4,213, less 15.98% of the $2,282 over $22,720
    assert abs(C.eitc(arr(1), arr(25002), arr(25002), **one)[0] - (4213 - 0.1598 * 2282)) < 1e-9
    # the phase-out runs on the greater of AGI and earned income
    assert abs(C.eitc(arr(1), arr(20000), arr(30000), **one)[0] - (4213 - 0.1598 * (30000 - 22720))) < 1e-9
    # investment income over $11,600 disqualifies; the childless credit needs age 25-64
    assert C.eitc(arr(1), arr(20000), arr(20000), np.array([False]), arr(11601), np.array([True]))[0] == 0
    assert C.eitc(arr(1), arr(20000), arr(20000), np.array([False]), arr(11600), np.array([True]))[0] > 0
    assert C.eitc(arr(0), arr(8000), arr(8000), np.array([False]), arr(0), np.array([False]))[0] == 0
    assert abs(C.eitc(arr(0), arr(8000), arr(8000), **one)[0] - 0.0765 * 8000) < 1e-9


def test_care_credit_rates_caps_and_the_census_convention():
    # Form 2441 (2024) line 8, except that at an exact $2,000 step the Census model takes the lower rate (17,000: .33)
    c = C.care_credit(arr(15000, 15001, 17000, 43001, 30000), arr(1, 1, 1, 1, 2), arr(5000, 5000, 5000, 5000, 9000),
                      arr(1e5, 1e5, 1e5, 1e5, 4000), arr(1e5, 1e5, 1e5, 1e5, 1e5))
    assert np.allclose(c, [0.35 * 3000, 0.34 * 3000, 0.33 * 3000, 0.20 * 3000, 0.27 * 4000])
    assert C.care_credit(arr(20000), arr(1), arr(3000), arr(1e5), arr(100))[0] == 100      # limited to the tax


def test_taxable_social_security_and_half_se_tax():
    ss = C.taxable_ss(arr(20000, 50000), arr(20000, 30000), np.array([False, True]))
    assert np.allclose(ss, [2500, min(0.85 * 30000, 0.85 * 21000 + 6000)])
    half = C.half_se_tax(arr(10000, 10000, 300), arr(0, 168600, 0))
    assert np.allclose(half, [0.153 * 9235 / 2, 0.029 * 9235 / 2, 0])


# ---------------------------------------------------------------------------------------------------------------------
# constants against the cached IRS texts
# ---------------------------------------------------------------------------------------------------------------------
def eitc_row(t, label):
    m = re.search(re.escape(label) + r" \$([\d,]+) \$([\d,]+) \$([\d,]+) \$([\d,]+)", t)
    one, two, three, none = (float(x.replace(",", "")) for x in m.groups())
    return {1: one, 2: two, 3: three, 0: none}


def test_constants_match_rev_proc_2023_34():
    t = text("rp")
    for bounds in C.BRACKETS.values():
        assert all(f"{b:,}" in t for b in bounds)
    assert all(money(v) in t for v in list(C.STD.values()) + list(C.AGED.values()))
    rows = {k: eitc_row(t, label) for k, label in [
        ("amount", "Earned Income Amount"), ("maximum", "Maximum Amount of Credit"),
        ("th_joint", "Threshold Phaseout Amount"), ("done_joint", "Completed Phaseout Amount"),
        ("th_other", "Threshold Phaseout Amount (All"), ("done_other", "Completed Phaseout Amount (All")]}
    for n, (_pin, _pout, amount, maximum, th_other, th_joint) in C.EITC.items():
        assert (amount, maximum, th_other, th_joint) == (rows["amount"][n], rows["maximum"][n], rows["th_other"][n],
                                                         rows["th_joint"][n])
        assert C.EITC_COMPLETED[n] == (rows["done_other"][n], rows["done_joint"][n])
    assert "investment income exceeds $11,600" in t and C.EITC_INVESTMENT == 11600
    assert re.search(r"may be refundable is \$1,700", t) and C.ACTC_MAX == 1700


def test_constants_match_schedule_8812_and_form_2441():
    s = text("s8812")
    assert "Multiply line 4 by $2,000" in s and "Multiply line 6 by $500" in s
    assert "Married filing jointly—$400,000" in s and "All other filing statuses—$200,000" in s
    assert "next multiple of $1,000" in s and "Multiply line 10 by 5% (0.05)" in s
    assert "x $1,700" in s and "Subtract $2,500" in s and "by 15% (0.15)" in s
    assert (C.CTC_CHILD, C.CTC_OTHER, C.CTC_STEP, C.ACTC_FLOOR, C.ACTC_RATE) == (2000, 500, 50, 2500, 0.15)
    f = text("f2441")
    assert "more than $3,000 if you had one qualifying person or $6,000 if you had two" in f and C.CDCC_CAP == (3000, 6000)
    bands = re.findall(r"\$?([\d,]+)—([\d,]+|No limit) \.(\d\d)", f)
    assert sorted(int(r) for *_, r in bands) == list(range(20, 36))      # .35 down to .20, one band each
    for lo, _hi, rate in bands:
        agi = float(lo.replace(",", "")) + 1000      # inside the band, away from the Census model's step convention
        got = C.care_credit(arr(agi), arr(1), arr(3000), arr(1e5), arr(1e5))[0] / 3000
        assert abs(got - int(rate) / 100) < 1e-12, (lo, rate)


# ---------------------------------------------------------------------------------------------------------------------
# outputs
# ---------------------------------------------------------------------------------------------------------------------
def test_example_return_by_hand():
    e = json.loads((DER / "example.json").read_text())
    assert e["FILESTAT"] == 4 and not e["head_member"] and len(e["dependents"]) == 1
    kid = e["dependents"][0]
    assert kid["member"] and kid["age"] < 17
    # head of household: taxable income is AGI less $21,900; the Census model rounds the tax to dollars
    assert e["AGI"] == e["wages"] and e["TAX_INC"] == e["AGI"] - 21900 and e["TAX_INC"] <= 16550
    t0 = round(0.10 * e["TAX_INC"])
    assert e["FEDTAX_BC"] + e["CTC_CRD"] == t0 and e["CTC_CRD"] == min(2000, t0)
    assert e["ACTC_CRD"] == min(2000 - e["CTC_CRD"], 1700, 0.15 * (e["wages"] - 2500))
    assert abs(e["EIT_CRED"] - (min(0.34 * e["wages"], 4213) - 0.1598 * max(e["AGI"] - 22720, 0))) < 1
    # without the child: no credit (the childless credit is gone above $18,591), the tax back on the return
    assert e["AGI"] > 18591
    assert e["counterfactual_no_dependents"] == {"nonref": 0.0, "actc": 0.0, "eitc": 0.0, "fedtax_bc": float(t0)}
    assert e["A"] == {"nonref": e["CTC_CRD"], "actc": e["ACTC_CRD"], "eitc": e["EIT_CRED"]}
    # single status: AGI less $14,600 at 10%
    single = e["single_status"]
    assert single["taxable_income"] == e["AGI"] - 14600 and abs(single["fedtax_bc"] - 0.10 * single["taxable_income"]) < 1
    assert abs(e["C"] - (single["fedtax_bc"] - t0)) < 1e-9


def test_rules_reproduce_the_census_credits():
    v = pd.read_csv(DER / "validation.csv").set_index("field")
    assert v.loc["ctc_crd", "share_returns_within_1"] == 1.0
    assert v.loc["actc_crd", "share_positive_returns_within_1"] >= 0.999
    assert v.loc["eit_cred", "share_positive_returns_within_1"] >= 0.998
    assert v.loc["care_credit_vs_schedule_gap", "share_positive_returns_within_1"] >= 0.97


def test_conservation_and_the_sets_add_up():
    s = json.loads((DER / "summary.json").read_text())
    assert abs(s["frame"]["union_row4"] - 39712493.33118789) < 1e-3
    for c in s["conservation"].values():
        assert abs(c["attributed_members_bn"] + c["attributed_others_bn"] - c["cps_total_bn"]) < 1e-9
        assert c["forward_in_bn"] >= 0 and c["reverse_out_bn"] >= 0
        assert abs(c["personal_members_bn"] + c["forward_in_bn"] - c["reverse_out_bn"] - c["attributed_members_bn"]) < 1e-9
    acc = s["account"]
    tot = lambda r, k, g="total": acc[r][k]["bn"][g]  # noqa: E731
    for r in acc:
        for g in ("G1", "G2", "G3+", "total"):
            assert abs(tot(r, "forward_A", g) + tot(r, "reverse_B", g) - tot(r, "child_credit_net_A_plus_B", g)) < 1e-6
        assert abs(sum(tot(r, "child_credit_net_A_plus_B", g) for g in ("G1", "G2", "G3+")) - tot(r, "child_credit_net_A_plus_B")) < 1e-6
        assert abs(tot(r, "child_credit_net_A_plus_B") + tot(r, "status_C_forward") + tot(r, "status_Cr_reverse")
                   - tot(r, "child_credit_and_status_net")) < 1e-6
        assert abs(tot(r, "child_credit_and_status_net") + tot(r, "joint_split_D") - tot(r, "full_removal_recomputation")) < 1e-6
    assert acc["R1"]["forward_A"] == acc["R2"]["forward_A"] == acc["R3"]["forward_A"]
    cl = s["reverse_R1_by_why_the_child_stays_bn"]
    rev = {r: tot(r, "reverse_B") + tot(r, "status_Cr_reverse") for r in acc}
    assert abs(sum(cl.values()) - rev["R1"]) < 1e-6
    assert abs(cl["claimants_nonmember_spouse_remains_D2"] + cl["nonmember_parent_in_household"] - rev["R3"]) < 1e-6
    assert abs(cl["claimants_nonmember_spouse_remains_D2"] - rev["R2"]) < 1e-6
    assert abs(sum(s["forward_A_by_return_type_bn"].values()) - tot("R1", "forward_A")) < 1e-6
    assert abs(sum(s["forward_A_by_head_origin_bn"].values()) - tot("R1", "forward_A")) < 1e-6
    assert abs(sum(sum(v.values()) for v in s["joint_split_D_by_head_bn"].values()) - tot("R1", "joint_split_D")) < 1e-6


def test_terms_table_is_complete():
    t = pd.read_csv(DER / "terms.csv")
    assert not t.isna().any().any()
    assert not t.duplicated(["component", "generation", "reading"]).any()
    assert set(t.reading) == {"R1", "R2", "R3"} and set(t.generation) == {"G1", "G2", "G3+"}
    assert set(t.side) == {"receipts", "spending"}


def test_item_follows_the_v7_contract():
    item = json.loads((DER / "item.json").read_text())
    s = json.loads((DER / "summary.json").read_text())
    model = json.loads((LANE.parent / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    net = item["net_bn"]["personal"]
    assert item["reading"] == "R3_with_status"
    assert abs(net - s["account"]["R3"]["child_credit_and_status_net"]["bn"]["total"]) < 1e-6
    assert set(item["by_generation"]) == {"G1", "G2", "G3plus"}
    assert abs(sum(v["personal"] for v in item["by_generation"].values()) - net) < 1e-12
    parts = item["parts"]
    assert len(parts) == 18 and {p["term"] for p in parts.values()} == {"A", "B", "C", "Cr"}
    assert abs(sum(p["cost_bn"] for p in parts.values()) - net) < 1e-12
    for p in parts.values():
        assert (p["side"], p["line"]) in {("receipt", "federal_income_tax"), ("spending", "refundable_tax_credits")}
        assert p["bn"] == (-p["cost_bn"] if p["side"] == "receipt" else p["cost_bn"])
        assert p["generation"] in {"G1", "G2", "G3plus"}
    for g, v in item["by_generation"].items():
        assert abs(sum(p["cost_bn"] for p in parts.values() if p["generation"] == g) - v["personal"]) < 1e-12
    # the receipt edit once per federal_liability rule (seven), the gap rule absent; the parts add to the two edits
    cells = next(x for x in model["receipts"]["lines"] if x["id"] == "federal_income_tax")["cells"]
    rules = [sc for sc in model["receipts"]["scenarios"] if cells[sc]["personal"]["key"] == "federal_liability"]
    receipt = [e for e in item["edits"] if e["side"] == "receipt"]
    spending = [e for e in item["edits"] if e["side"] == "spending"]
    assert sorted(e["scenario"] for e in receipt) == sorted(rules) and len(rules) == 7
    assert "federal_gap_high_agi" not in {e["scenario"] for e in receipt} and "federal_gap_high_agi" in item["edits_note"]
    assert len(spending) == 1 and (spending[0]["line"], spending[0]["key"]) == ("refundable_tax_credits", "refundable_credits")
    assert all(e["by"]["shared"] == 0 for e in item["edits"])
    r_sum = sum(p["bn"] for p in parts.values() if p["side"] == "receipt")
    s_sum = sum(p["bn"] for p in parts.values() if p["side"] == "spending")
    assert all(abs(e["by"]["personal"] - r_sum) < 1e-12 for e in receipt)
    assert abs(spending[0]["by"]["personal"] - s_sum) < 1e-12 and abs(s_sum - r_sum - net) < 1e-12
    # lineage: the G3+ term per identified G3+ member
    lin = item["lineage"]
    assert abs(lin["g3plus_per_member_usd"] - item["by_generation"]["G3plus"]["personal"] * 1e9 / lin["identified_g3plus"]) < 1e-9
    assert abs(lin["identified_g3plus"] - s["frame"]["lineage_counts"]["identified_g3plus"]) < 1e-9
    # arms
    assert set(item["arms"]) == {"R1_with_status", "R2_with_status", "R3_without_status"}
    for name, a in item["arms"].items():
        assert abs(sum(v["personal"] for v in a["by_generation"].values()) - a["net_bn"]["personal"]) < 1e-9
        assert abs(a["edits_personal"]["spending"] - a["edits_personal"]["receipt"] - a["net_bn"]["personal"]) < 1e-9
    assert abs(item["arms"]["R3_without_status"]["net_bn"]["personal"]
               - s["account"]["R3"]["child_credit_net_A_plus_B"]["bn"]["total"]) < 1e-6
    assert all(g["passed"] for g in item["gates"]) and len(item["gates"]) == s["gates"]


def test_members_only_sharing_is_personal_only_when_the_split_keeps_weights():
    a = pd.read_csv(DER / "allocation_check.csv")
    model = json.loads((LANE.parent / "assumption_explorer_2026_09_21/derived/model.json").read_text())
    for r in a.itertuples():
        if r.side == "spending":
            stored = next(x for x in model["spending"]["lines"] if x["id"] == r.line)["keys"][r.key]
        else:
            stored = next(x for x in model["receipts"]["lines"] if x["id"] == r.line)["cells"][model["receipts"]["reference"]]
        assert abs(r.share_personal - stored["personal"]["share"]) < 5e-9 and abs(r.share_shared - stored["shared"]["share"]) < 5e-9
        assert abs(r.share_members_only_weighted - r.share_personal) < 1e-12
        assert abs(r.members_only_weighted_minus_personal_bn) < 1e-9
        # the builders' unweighted split moves the group's share even among members only
        assert abs(r.members_only_minus_personal_bn) > 0.1
