"""Counterfactual conservation and distinct-premise tests."""
import json
import csv
import pytest
from rents import HERE, counterfactual


@pytest.mark.parametrize("arm", ["vanishing", "fixed"])
@pytest.mark.parametrize("end", ["low", "high"])
def test_phi_zero_restores_every_component(arm, end):
    row = counterfactual(0, 30, 40, .25, .04, .6, arm, end)
    assert all(v == 0 for v in row.values())


def test_demand_rekey_cannot_be_residence_only():
    jobs = counterfactual(1, 30, 30, .25, .04, .6, "vanishing", "low")
    demand = counterfactual(1, 30, 40, .25, .04, .6, "vanishing", "low")
    assert jobs["source_change_bn"] == 0
    assert demand["source_change_bn"] == -10
    assert demand["delta_bn"] == pytest.approx(-14.8)


def test_private_and_residence_tax_partition_without_double_counting():
    row=counterfactual(.5,30,40,.25,.04,.6,"vanishing","high")
    assert row["residence_loss_bn"]+row["domestic_owner_loss_after_residence_tax_bn"] == pytest.approx(.6*60)
    assert row["delta_bn"]-row["domestic_owner_loss_after_residence_tax_bn"] == pytest.approx(-20-.6*60)


def test_fixed_rents_high_end_is_already_fixed():
    row=counterfactual(1,30,30,.25,.04,.6,"fixed","high")
    assert all(v == 0 for v in row.values())


@pytest.mark.parametrize("phi,t,r,s", [(-.1,.25,.04,.6),(1.1,.25,.04,.6),(.5,0,.04,.6),(.5,.25,.7,.6)])
def test_invalid_identification_assumptions_fail_loud(phi,t,r,s):
    with pytest.raises(ValueError):
        counterfactual(phi,30,40,t,r,s,"vanishing","low")


def test_generated_controls_and_conditional_se_presence():
    data=json.loads((HERE/"derived/summary.json").read_text())
    assert data["gates"] and all(x["passed"] for x in data["gates"])
    assert data["ownership"]["rounding_residual_bn"] == 2
    assert data["rates"]["dividend_share"] == pytest.approx(.4)


def test_both_corporate_rates_have_thresholds():
    rows=list(csv.DictReader((HERE/"derived/thresholds.csv").open()))
    vanishing=[r for r in rows if r["residence_rule"]!="fixed"]
    assert len(vanishing)==64
    assert {float(r["corporate_rate"]) for r in vanishing}=={.21,.25}


def test_other_resident_scope_is_flagged_in_each_output():
    rows=list(csv.DictReader((HERE/"derived/arms.csv").open()))
    assert rows and all(float(r["e_tax_assumed"])==0 for r in rows)
    assert all(float(r["household_account_claim_loss_upper_bn"])<=float(r["domestic_owner_loss_after_residence_tax_bn"])+1e-9 for r in rows)
