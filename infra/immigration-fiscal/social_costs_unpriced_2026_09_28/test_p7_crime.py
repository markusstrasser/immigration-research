"""Material response, overlap, population and source-contract regressions."""
import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p7_crime_tested", HERE / "p7_crime.py")
p7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p7)


def test_households_have_no_population_subtraction():
    r = p7.response(dict(residential=10, commercial=0), 0.2, 0.6, 0.8)
    assert r["total_bn"] == pytest.approx(1.2)
    assert r["commercial_reverse_bn"] == 0


def test_business_security_has_separate_payment_credit():
    r = p7.response(dict(residential=10, commercial=20), 0.2, 0.6, 0.1)
    assert r["residential_forward_bn"] == pytest.approx(1.2)
    assert r["commercial_forward_bn"] == pytest.approx(2.16)
    assert r["commercial_reverse_bn"] == pytest.approx(1.6)
    assert r["total_bn"] == pytest.approx(1.76)


def test_zero_offending_retains_lost_business_contribution_only():
    r = p7.response(dict(residential=100, commercial=20), 0, 1, 0.1)
    assert r["total_bn"] == pytest.approx(-2)
    assert p7.response(dict(residential=100, commercial=20), 0, 1, 0)["total_bn"] == 0


def test_response_rejects_invalid_shares():
    with pytest.raises(ValueError, match="BLOCKED"):
        p7.response(dict(residential=1, commercial=1), 1.1, 1, 0)


def test_offending_sensitivity_cannot_change_payment_key():
    sc = p7.load("payment_independence_constants", HERE / "items.py")
    source = p7.load("payment_independence_sources", HERE / "security_inputs.py").load_security_inputs()
    a = p7.crime_responses(sc, source, factor=0.8)
    b = p7.crime_responses(sc, source, factor=1.2)
    current = json.loads((HERE / "derived/payment_keys.json").read_text())["low"]["union_share"]
    assert a["payment_share"] == b["payment_share"] == current


def test_lineage_business_reverse_uses_lineage_payment_share():
    payload = json.loads((HERE / "derived/p7_payload.json").read_text())
    for end in ("low", "high"):
        p = payload["response_parameters"][end]
        f = p["offending_share_union"] * (1+p["added_offending_share"])
        o = p["outside_share_before_boundary"] * (1-p["recipient_share"])
        pay = p["payment_share_lineage"]
        s = p["national_spending"]
        expected = s["residential"]*f*o + s["commercial"]*f*o*(1-pay) - s["commercial"]*pay*(1-f)
        assert payload["lineage_crime_rows"][end]["private_security"] == pytest.approx(expected, abs=1e-10)


def test_active_arm_and_security_overlap_are_reconciled():
    sc = p7.load("tested_social_constants", HERE / "items.py")
    source = p7.load("tested_security_sources", HERE / "security_inputs.py").load_security_inputs()
    legacy = p7.crime_responses(sc, source, "mixed", "legacy")
    dot = p7.crime_responses(sc, source, "mixed", "dot_uniform")
    joint = p7.crime_responses(sc, source, "mixed", "dot_uniform", subtract_security=True)
    assert dot["victims"] > legacy["victims"]
    assert dot["fear"] < legacy["fear"]
    assert legacy["security"] == pytest.approx(dot["security"])
    assert joint["fear"] == pytest.approx(0.5 * max(0, dot["wtp_minus_active_victims_bn"] - dot["security_forward_bn"]))
    assert joint["security"] == pytest.approx(dot["security"])
    # A negative payment credit must not increase the WTP overlap deduction.
    assert joint["security_forward_bn"] > joint["security"]


def test_missing_baseline_is_rejected_before_any_outputs(tmp_path, monkeypatch):
    (tmp_path / "pins.json").write_text(json.dumps({"files": [{"path": "does-not-exist", "sha256": "0" * 64}]}))
    monkeypatch.setattr(p7, "INPUTS", tmp_path)
    before = {p.name: p.read_bytes() for p in (HERE / "derived").glob("p7_*")}
    with pytest.raises(ValueError, match="missing or stale P7 baseline"):
        p7.main()
    assert before == {p.name: p.read_bytes() for p in (HERE / "derived").glob("p7_*")}


def test_renderer_rejects_missing_captured_receipt_before_outputs(tmp_path, monkeypatch):
    renderer = p7.load("tested_p7_renderer", HERE / "render_p7.py")
    monkeypatch.setattr(renderer, "HERE", tmp_path)
    with pytest.raises(SystemExit, match="BLOCKED.*captured validation receipt"):
        renderer.main()
    assert not (tmp_path / "RESULT.md").exists()


def test_noncrime_source_rows_and_benefit_sign_are_preserved():
    payload = json.loads((HERE / "derived/p7_payload.json").read_text())
    assert all(0 <= s < 1 for s in payload["recipient_shares"].values())
    gates = p7.rows(HERE / "derived/p7_gates.csv")
    assert all(r["result"] == "PASS" for r in gates)
    assert any("published full span positive control" in r["gate"] for r in gates)
    assert any("noncrime union span unchanged" in r["gate"] for r in gates)
