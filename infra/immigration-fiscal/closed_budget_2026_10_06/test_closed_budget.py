"""Consistency of the closed-budget arm's committed outputs: every row is G - s * F, the cost falls as the fix grows,
the household rule carries less than per head, the general-fund gaps net the trust-fund shortfall from the published
gaps, and the summary's central row is the one the docs quote."""
import csv
import json
from pathlib import Path

D = Path(__file__).resolve().parent / "derived"


def rows():
    with open(D / "closed_budget.csv", newline="") as f:
        return list(csv.DictReader(f))


def test_every_row_is_case_less_share_of_fix():
    for r in rows():
        offset = float(r["share"]) * float(r["fix_bn"])
        assert abs(offset - float(r["offset_bn"])) < 1e-6 * float(r["fix_bn"]) + 1e-4  # share is printed to 6 places
        assert abs(float(r["case_bn"]) - float(r["offset_bn"]) - float(r["cost_to_others_bn"])) < 1e-5


def test_general_fund_gap_is_published_gap_less_trust_funds():
    src = {g["id"]: g for g in json.load(open(D.parent / "sources.json"))["fiscal_gaps"]}
    for r in rows():
        if r["basis"].startswith("general fund"):
            pub = src[r["fix"]]["pct_gdp"]
            assert abs(pub - float(r["trust_funds_pct_gdp"]) - float(r["pct_gdp"])) < 1e-3
            assert float(r["pct_gdp"]) > 0


def test_cost_falls_as_fix_rises():
    groups = {}
    for r in rows():
        groups.setdefault((r["rule"], r["set"], r["end"]), []).append((float(r["fix_bn"]), float(r["cost_to_others_bn"])))
    for pts in groups.values():
        pts.sort()
        assert all(b[1] <= a[1] + 1e-9 for a, b in zip(pts, pts[1:]))


def test_household_rule_carries_less_than_per_head():
    h = json.load(open(D / "household_share.json"))
    assert 0 < h["share"] < h["per_person_share"]
    assert h["persons_per_household_lineage"] > h["persons_per_household_all"]


def test_audit_gates_pass_and_identity_control_reproduces_printed_excess():
    gates = json.load(open(D / "audit.json"))["gates"]
    assert gates and all(g["pass"] for g in gates)
    assert any("reproduces the printed excess" in g["gate"] for g in gates)


def test_summary_central_matches_csv():
    s = json.load(open(D / "summary.json"))
    c = s["sets"]["main"]["central"]
    d = c["definition"]
    got = sorted(float(r["cost_to_others_bn"]) for r in rows()
                 if (r["fix"], r["basis"], r["rule"], r["set"]) == (d["fix"], d["basis"], d["rule"], "main"))
    assert [round(x, 3) for x in got] == [round(x, 3) for x in sorted(c["cost_bn"])]
