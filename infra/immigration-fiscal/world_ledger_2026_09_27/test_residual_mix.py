"""Parent Phase C proportional residual convention and explicit coverage incidence."""
from types import SimpleNamespace
import json
import shutil

import pandas as pd
import pytest

import valuation as V


def donor(side, cls, cost, value, payer="government_budget"):
    return dict(component_side=side, cls=cls, economic_payer=payer, net_cost_bn=cost,
                V_low_bn=value, V_central_bn=value, V_high_bn=value,
                third_party_bn=0.0, source_tax_credit_bn=-cost if cls == "source_tax" else 0.0)


@pytest.mark.parametrize("amount", [-0.107, 0.434, 0.0])
def test_signed_proportional_mix_conserves_each_row_and_receipt_side(amount):
    donors = pd.DataFrame([donor("spending", "cash", 10.0, 10.0),
                           donor("spending", "education", 4.0, 0.0),
                           donor("receipt", "tax", -3.0, -3.0, "group_filers"),
                           donor("receipt", "source_tax", -1.0, 0.0, "outside_owners")])
    mix = V.proportional_component_mix(donors, amount)
    assert mix.net_cost_bn.sum() == pytest.approx(amount, abs=1e-12)
    assert mix.groupby("component_side").net_cost_bn.sum().to_dict() == pytest.approx(
        {"spending": amount * 1.4, "receipt": amount * -0.4})
    assert mix.V_central_bn.sum() == pytest.approx(amount * 0.7)
    assert mix.source_tax_credit_bn.sum() == pytest.approx(amount * 0.1)
    assert mix.assumption.str.startswith("[ASSUMPTION]").all()


def test_mix_blocks_unidentified_nonzero_net_and_nonfinite_donors():
    donors = pd.DataFrame([donor("spending", "cash", 1.0, 1.0), donor("receipt", "tax", -1.0, -1.0)])
    with pytest.raises(SystemExit, match="residual_mix_nonzero"):
        V.proportional_component_mix(donors, 0.2)
    donors.loc[0, "V_central_bn"] = float("nan")
    with pytest.raises(SystemExit, match="finite_residual_mix"):
        V.proportional_component_mix(donors, 0.2)


def test_coverage_receipt_uses_explicit_parent_class_payer_and_sign(monkeypatch, tmp_path):
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    monkeypatch.setattr(V, "receipt_contract", lambda case: (V.RECEIPT_CLASS, V.RECEIPT_PAYER))
    source = dict(generation="G1", line="federal_income_tax", source_line="federal_income_tax",
                  source_side="receipt", economic_class="fiscal_line", coverage_bn=-0.2,
                  source_response=1.0)
    residual = dict(generation="G1", line="lane_residual", economic_class="unclassified_residual", coverage_bn=0.1)
    payload = {"meta": {"coverage": {"by_end": {"low": {"decomposition": {"line_parts": [source, residual]}}}}}}
    counted = pd.DataFrame([dict(band_end="low", generation="G1", side=side, line=line,
                                 amount_bn=amount, response=1.0, effect_bn=effect)
                            for side, line, amount, effect in
                            [("spending", "social_security", 2.0, -2.0),
                             ("receipt", "federal_income_tax", 1.0, 1.0)]])
    coverage = pd.DataFrame([dict(band_end="low", generation="union", side="coverage",
                                  line=f"coverage_{i}_G1_{s['line']}", amount_bn=s["coverage_bn"],
                                  effect_bn=-s["coverage_bn"], response=1.0) for i, s in enumerate([source, residual])])
    V.prepare_coverage_values("oct15", counted, coverage, payload=payload, basis="cash")
    receipt = V.valuation_row(next(coverage.itertuples()), V.RECEIPT_CLASS, V.RECEIPT_PAYER)
    assert receipt["receipt_incidence_class"] == "tax"
    assert receipt["economic_payer"] == "group_filers"
    assert receipt["V_central_bn"] == -0.2
    assert receipt["net_cost_bn"] == -0.2
    for raw in coverage.itertuples(index=False):
        main = V.valuation_row(raw, V.RECEIPT_CLASS, V.RECEIPT_PAYER)
        padded = dict(raw._asdict(), generation="G2", amount_bn=0.0, effect_bn=0.0)
        other = V.valuation_row(SimpleNamespace(**padded), V.RECEIPT_CLASS, V.RECEIPT_PAYER)
        assert other["V_central_bn"] == other["net_cost_bn"] == 0.0
        assert main["V_central_bn"] != 0.0


def test_coverage_unknown_receipt_is_never_defaulted_to_tax(monkeypatch, tmp_path):
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    monkeypatch.setattr(V, "receipt_contract", lambda case: (V.RECEIPT_CLASS, V.RECEIPT_PAYER))
    source = dict(generation="G1", line="new_receipt", source_line="new_receipt", source_side="receipt",
                  economic_class="fiscal_line", coverage_bn=-0.2)
    payload = {"meta": {"coverage": {"by_end": {"low": {"decomposition": {"line_parts": [source]}}}}}}
    counted = pd.DataFrame([dict(band_end="low", generation="G1", side="spending", line="social_security",
                                amount_bn=1.0, effect_bn=-1.0, response=1.0)])
    coverage = pd.DataFrame([dict(band_end="low", side="coverage", line="coverage_0_G1_new_receipt",
                                 amount_bn=-0.2, effect_bn=0.2, response=1.0)])
    with pytest.raises(SystemExit, match="unclassified receipt"):
        V.prepare_coverage_values("oct15", counted, coverage, payload=payload, basis="cash")


def test_live_cash_each_residual_component_and_generation_closes(monkeypatch, tmp_path):
    import pension_cash as P
    shutil.copyfile(V.DERIVED / "state_price_quantity.csv", tmp_path / "state_price_quantity.csv")
    monkeypatch.setattr(V, "DERIVED", tmp_path)
    raw = json.loads((V.HERE / "inputs/pension_cash_cells_oct15.json").read_text())["results"]["cash"]
    _, generations, union = P._value("oct15", raw)
    mixed = union[union.cls.eq("proportional_mix")]
    assert len(mixed) == 10
    for row in mixed.itertuples():
        components = pd.DataFrame(json.loads(row.recipient_components_json))
        assert set(components.component_side) == {"receipt", "spending"}
        assert components.G_bn.sum() == pytest.approx(row.G_bn, abs=1e-10)
        for col in ("V_low_bn", "V_central_bn", "V_high_bn", "source_tax_credit_bn"):
            assert components[col].sum() == pytest.approx(getattr(row, col), abs=1e-10)
    for col in ("net_cost_bn", "V_low_bn", "V_central_bn", "V_high_bn", "source_tax_credit_bn"):
        u = union.groupby(["end", "line"])[col].sum().sort_index()
        g = generations.groupby(["end", "line"])[col].sum().sort_index()
        pd.testing.assert_index_equal(u.index, g.index)
        assert (u - g).abs().max() < 1e-9
    padded = generations[generations.cls.eq("proportional_mix") & generations.G_bn.eq(0)]
    for encoded in padded.recipient_components_json:
        assert all(component["G_bn"] == component["V_central_bn"] == 0.0
                   for component in json.loads(encoded))
