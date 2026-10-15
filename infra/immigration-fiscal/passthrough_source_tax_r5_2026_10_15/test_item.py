"""Economic identities and the item/engine integration contract."""
import json
import subprocess
from pathlib import Path

import numpy as np
import pytest

from owner_tax_sources import direct_equal_after_tax_loss, direct_replacement_loss, gilti_current_us_tax

HERE = Path(__file__).resolve().parent


def read(name):
    return json.loads((HERE / name).read_text())


@pytest.mark.parametrize("income", [-8, 0, 10, 100])
@pytest.mark.parametrize("rate", [.1, .22, .37])
def test_domestic_identical_replacement_cancels(income, rate):
    assert direct_replacement_loss(income, rate, 1, 1, 1) == 0
    assert direct_replacement_loss(income, rate, 0, 0, 1) == 0
    assert direct_replacement_loss(income, rate, 0, 1, 1) == pytest.approx(income * rate)


def test_equal_after_tax_not_same_pretax():
    # 100 at home pays20 and leaves80. At30% abroad,114.285714 income
    # leaves80. Full FTC leaves no residual US tax; lost US tax is20.
    assert direct_equal_after_tax_loss(100, .2, 0, .3) == pytest.approx(20)
    # At10% abroad, US tax of10 remains after credit, after-tax return80.
    assert direct_equal_after_tax_loss(100, .2, 0, .1) == pytest.approx(10)


def test_gilti_full_section78_grossup_and_eighty_percent_credit():
    x = gilti_current_us_tax(90, 90, 10)
    assert x["section78_gross_up"] == 10
    assert x["tentative_us_tax"] == pytest.approx(10.5)
    assert x["allowed_credit"] == 8
    assert x["current_us_residual"] == pytest.approx(2.5)
    assert gilti_current_us_tax(90, 0, 10)["current_us_residual"] == 0


def test_tiering_removed_before_capital_fraction():
    rows = read("inputs/income_sectors.json")["records"]
    for r in rows:
        if r["form"] == "partnership":
            assert r["direct_income_net_bn"] == pytest.approx(r["income_net_bn"] - r["known_upstream_ordinary_net_bn"])
    # Owner officer compensation/guaranteed payments already deducted: the
    # extractor keeps these separately rather than subtracting them again.
    assert sum(r["owner_compensation_deducted_bn"] or 0 for r in rows if r["form"] == "s_corporation") > 300


def test_gated_row4_source_and_pooled_generation_closure():
    keys = read("derived/job_keys.json")
    assert all(g["passed"] for g in keys["source_core_gates"])
    for forms in [*keys["shares"].values(), *keys["pooled_shares"].values()]:
        for v in forms.values():
            if v is None:
                continue
            assert np.allclose(sum(np.array(v[g]) for g in ["G1", "G2", "G3plus"]), v["union"], rtol=1e-12)
    assert any("[DEGRADED]" in r["rule"] for r in read("derived/legal_profiles.json"))


def test_completion_is_own_record_increment_not_population_scaling():
    keys = read("derived/job_keys.json")
    meta = keys["completion"]["metadata"]
    assert meta["completion_people"] == pytest.approx(517435.75719317, abs=1e-6)
    assert meta["selected_records"] == 231
    assert meta["wage_earners"] == 80
    assert meta["supported_wage_bn"] + sum(meta["excluded_wages_by_cell_bn"].values()) == pytest.approx(meta["corrected_wage_bn"])
    assert "no selected completion wage" in meta["top_wage_gate"]
    arm = read("derived/item.json")["arms"]["foreign_full_ftc_top_owner_labor"]["by_end"]["low"]
    assert sum(p["completion_cost_bn"] for p in arm["parts_by_line"]) == pytest.approx(-.04611042458502716)
    assert arm["omitted_population_people"] == read("derived/v8.json")["population"]["coverage"]


def test_case_parts_close_and_all_four_baselines():
    b = read("derived/v8.json")
    assert b["baseline"]["set"] == pytest.approx([365.791930255485, 455.981784588979], abs=1e-6)
    assert b["baseline"]["cash"] == pytest.approx([281.752563676073, 371.942418009567], abs=1e-6)
    c = read("derived/job_keys.json")["corporate"]
    assert sum(b["parts"].values()) == pytest.approx(c["lineage"]["before_bn"][0], abs=1e-9)


def test_item_sign_cancellation_and_no_silent_central():
    item = read("derived/item.json")
    assert item["central"] is None
    for name, arm in item["arms"].items():
        for value in arm["by_end"].values():
            assert sum(p["total_bn"] for p in value["parts_by_line"]) == pytest.approx(value["total_bn"], abs=1e-9)
            assert sum(value["by_generation_bn"].values()) == pytest.approx(value["total_bn"], abs=1e-9)
    assert item["arms"]["domestic_replacement"]["by_end"]["low"]["total_bn"] == 0
    assert item["arms"]["foreign_no_ftc_same_income"]["by_end"]["low"]["total_bn"] == 0
    assert item["arms"]["foreign_full_ftc_top_owner_labor"]["by_end"]["low"]["total_bn"] < 0
    script = "const I=require(process.argv[1]); try {I.build({},null,'set');process.exit(2);} catch(e) {if(!e.message.includes('no identified central'))throw e;}"
    subprocess.run(["node", "-e", script, str(HERE / "item.cjs")], check=True)


def test_signed_sector_allocations_are_not_ownership_probabilities():
    rows = read("inputs/income_sectors.json")
    national = rows["national"]["partnership"]["partner_allocations_bn"]
    expected = (national["individual_general"] + national["individual_limited"]) / national["all"]
    arm = read("derived/item.json")["arms"]["foreign_full_ftc_immediate_individual"]
    for p in arm["by_end"]["low"]["parts_by_line"]:
        if p["line"] == "owner_federal_partnership":
            assert p["owner_share"] == pytest.approx(expected)


def test_w09_is_receipt_only_same_cash_and_set():
    w = read("derived/w09.json")
    for end in ["low", "high"]:
        assert w["set"][end]["total_bn"] == pytest.approx(w["cash"][end]["total_bn"], abs=1e-12)
    for value in w["set"].values():
        assert value["total_bn"] == pytest.approx(value["union_and_v6_descendants_bn"] + value["completion_G3_profile_proxy_bn"] + value["coverage_generation_profile_proxy_bn"])
    assert w["set"]["high"]["total_bn"] == pytest.approx(.37 * w["set"]["low"]["total_bn"])


def test_real_v8_with_without_evaluations():
    for r in read("derived/evaluations.json"):
        assert r["with_bn"] - r["without_bn"] == pytest.approx(r["delta_cost_bn"], abs=1e-9)
