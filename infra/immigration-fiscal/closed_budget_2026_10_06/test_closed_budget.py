"""Consistency of the closed-budget arm's committed outputs: every row is G - s * F, the cost falls as the fix grows,
the household rule carries less than per head, the general-fund gaps net the trust-fund shortfall from the published
gaps, and the summary's central row is the one the docs quote. Each check runs on main case v5's outputs (derived/)
and main case v6's (derived/oct07/)."""
import csv
import json
from pathlib import Path

import pytest

LANE = Path(__file__).resolve().parent
D = LANE / "derived"
CASE_DIRS = pytest.mark.parametrize("d", [D, D / "oct07"], ids=["oct05", "oct07"])


def rows(d):
    with open(d / "closed_budget.csv", newline="") as f:
        return list(csv.DictReader(f))


@CASE_DIRS
def test_every_row_is_case_less_share_of_fix(d):
    for r in rows(d):
        offset = float(r["share"]) * float(r["fix_bn"])
        assert abs(offset - float(r["offset_bn"])) < 1e-6 * float(r["fix_bn"]) + 1e-4  # share is printed to 6 places
        assert abs(float(r["case_bn"]) - float(r["offset_bn"]) - float(r["cost_to_others_bn"])) < 1e-5


@CASE_DIRS
def test_general_fund_gap_is_published_gap_less_trust_funds(d):
    src = {g["id"]: g for g in json.load(open(LANE / "sources.json"))["fiscal_gaps"]}
    for r in rows(d):
        if r["basis"].startswith("general fund"):
            pub = src[r["fix"]]["pct_gdp"]
            assert abs(pub - float(r["trust_funds_pct_gdp"]) - float(r["pct_gdp"])) < 1e-3
            assert float(r["pct_gdp"]) > 0


@CASE_DIRS
def test_cost_falls_as_fix_rises(d):
    groups = {}
    for r in rows(d):
        groups.setdefault((r["rule"], r["set"], r["end"]), []).append((float(r["fix_bn"]), float(r["cost_to_others_bn"])))
    for pts in groups.values():
        pts.sort()
        assert all(b[1] <= a[1] + 1e-9 for a, b in zip(pts, pts[1:]))


@CASE_DIRS
def test_household_rule_carries_less_than_per_head(d):
    h = json.load(open(d / "household_share.json"))
    assert 0 < h["share"] < h["per_person_share"]
    assert h["persons_per_household_lineage"] > h["persons_per_household_all"]


@CASE_DIRS
def test_audit_gates_pass_and_identity_control_reproduces_printed_excess(d):
    gates = json.load(open(d / "audit.json"))["gates"]
    assert gates and all(g["pass"] for g in gates)
    assert any("reproduces the printed excess" in g["gate"] for g in gates)


@CASE_DIRS
def test_summary_central_matches_csv(d):
    s = json.load(open(d / "summary.json"))
    c = s["sets"]["main"]["central"]
    dfn = c["definition"]
    got = sorted(float(r["cost_to_others_bn"]) for r in rows(d)
                 if (r["fix"], r["basis"], r["rule"], r["set"]) == (dfn["fix"], dfn["basis"], dfn["rule"], "main"))
    assert [round(x, 3) for x in got] == [round(x, 3) for x in sorted(c["cost_bn"])]
