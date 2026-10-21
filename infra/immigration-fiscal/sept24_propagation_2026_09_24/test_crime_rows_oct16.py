"""The oct16 business-crime and commercial-security rows and the crime rows' v9 sender terms, read back from the
written pairing (decision 2026-10-21-business-crime-in-pairing)."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ENDS = ("low", "high")


def doc():
    return json.loads((HERE / "derived/oct16/real_costs_totals.json").read_text())


def rows(d):
    return {r["item"]: r for r in d["v9_social_environment"]["current_social_rows"]}


def test_business_row_is_the_lane_net_plus_the_v9_terms():
    d = doc()
    lane = json.loads((FISCAL / "business_crime_2026_10_21/derived/summary.json").read_text())["pairing"]
    r = rows(d)["business_crime"]
    for end in ENDS:
        v8 = r["v8_added_by_end_bn"][end]
        assert d["joint_social_stack"]["ends"][end]["extra_social_rows_bn"]["business_crime"] == lane["ends"][end]["net_bn"]
        assert abs(r["total_by_end_bn"][end] - lane["ends"][end]["net_bn"] - v8["added_people_bn"]
                   - v8["item11_consumption_bn"] - v8["completion_receivers_bn"]) < 1e-12
        assert r["contract"]["gross_beside_bn"][end] == lane["ends"][end]["gross_bn"]


def test_commercial_row_is_the_part_p7_leaves_out():
    d = doc()
    p7 = d["p7_crime"]
    for end in ENDS:
        q = p7["response_parameters"][end]
        out = q["outside_share_before_boundary"] * (1 - p7["recipient_shares"]["victims"])
        off = q["offending_share_union"] * (1 + q["added_offending_share"])
        level = q["national_spending"]["commercial"] * off * (1 - out) * (1 - q["payment_share_lineage"])
        got = d["joint_social_stack"]["ends"][end]["extra_social_rows_bn"]["commercial_security_member_victims"]
        assert abs(got - level) < 1e-12


def test_senders_exclude_coverage_and_rows_close():
    d = doc()
    env = d["v9_social_environment"]
    senders = env["v8_added_social"]["crime_senders"]
    people = env["v8_added_social"]["people"]
    assert senders["people_12_plus"] == people["located_change_12_plus"]
    assert abs(senders["people_12_plus"]) < people["completion"]          # the coverage people are not senders
    for end in ENDS:
        assert senders["share_12_plus"][end] == senders["people_12_plus"] / senders["union_12_plus_row4"]
        victims = rows(d)["victims"]["v8_added_by_end_bn"][end]
        assert abs(victims["added_people_bn"] - victims["union_part_bn"] * senders["share_12_plus"][end]) < 1e-12
        j = d["joint_social_stack"]["ends"][end]
        assert abs(sum(r["total_by_end_bn"][end] for r in rows(d).values()) - j["social_rows_bn"]) < 1e-9
        assert abs(j["fiscal_pairing_bn"] + j["social_rows_bn"] - j["with_round1_social_fixes_bn"]) < 1e-9
