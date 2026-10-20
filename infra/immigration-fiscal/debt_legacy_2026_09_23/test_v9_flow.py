"""Economic-source routing regressions for the v9 current-flow bridge."""
from pathlib import Path
import importlib.util
import sys
import pytest
import pandas as pd
import hashlib
import json

HERE = Path(__file__).resolve().parent
sys.path.insert(0,str(HERE))
try:
    spec = importlib.util.spec_from_file_location("v9_flow_tests",HERE/"v9_flow.py")
    flow = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(flow)
    classify = flow.classify
finally:
    sys.path.pop(0)


def test_va_delta_is_federal_even_inside_mixed_health_line():
    base = [dict(side="spending",id="health_services",responsive_bn=10.,federal_bn=6.,financing="cash")]
    row = classify(base,-3.,"health_services","spending","veterans_compensation",force=(1.,"cash"))
    assert row["federal_bn"] == -3.
    assert row["state_local_bn"] == 0.


def test_native_cache_rejects_missing_or_changed_bytes(tmp_path, monkeypatch):
    monkeypatch.setattr(flow, "HERE", tmp_path)
    out = tmp_path / "derived/oct16"
    out.mkdir(parents=True)
    with pytest.raises(ValueError, match="manifest missing"):
        flow.load_native_frame(out)
    cache = tmp_path / "_cache/oct16/native_frame.json"
    cache.parent.mkdir(parents=True)
    data = b'{"case":"oct16"}\n'
    cache.write_bytes(data)
    receipt = {"artifact": {"path": "_cache/oct16/native_frame.json", "bytes": len(data),
                           "sha256": hashlib.sha256(data).hexdigest()}, "source_pins": {}}
    (out / "native_frame_manifest.json").write_text(json.dumps(receipt))
    assert flow.load_native_frame(out)["case"] == "oct16"
    cache.write_bytes(data.replace(b"oct16", b"oct15"))
    with pytest.raises(ValueError, match="hash/size mismatch"):
        flow.load_native_frame(out)
    cache.write_bytes(data)
    monkeypatch.setattr(flow, "FISCAL", tmp_path)
    source = tmp_path / "upstream.json"
    source.write_bytes(b"original")
    receipt["source_pins"] = {"upstream.json": hashlib.sha256(source.read_bytes()).hexdigest()}
    (out / "native_frame_manifest.json").write_text(json.dumps(receipt))
    source.write_bytes(b"changed!")
    with pytest.raises(ValueError, match="stale native frame source"):
        flow.load_native_frame(out)
    cache.unlink()
    with pytest.raises(ValueError, match="cache missing"):
        flow.load_native_frame(out)


def test_military_history_requires_complete_component_export(tmp_path, monkeypatch):
    spec = importlib.util.spec_from_file_location("military_history_test", HERE / "military_history_oct16.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "FISCAL", tmp_path)
    source = tmp_path / "historical_backcast_2026_09_20/derived"
    source.mkdir(parents=True)
    (source / "case_components_oct16.json").write_text("{}\n")
    with pytest.raises(ValueError, match="military source history prerequisite missing:.*case_parts_annual"):
        module.main()


def test_military_history_uses_named_ends_and_gates_principal():
    spec = importlib.util.spec_from_file_location("military_history_ends_test", HERE / "military_history_oct16.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    located={'mil':{'line':'military_medical'}}
    ends={e:{'additions_bn':{'mil':v}} for e,v in (('low',-1.),('high',-2.))}
    meta={'concepts':{'net_cost_cbo_informed':{'ends':ends}}}
    annual=pd.DataFrame([dict(concept=f'net_cost_cbo_informed_oct16_{e}',rule=r,part='mil',year=2024,
                              value_bn=ends[e]['additions_bn']['mil'])
                         for e in ends for r in ('flat','ratio','income')])
    selected=module.select_history(meta,annual,located)
    assert len(selected)==6 and set(selected.end)=={'low','high'}
    with pytest.raises(ValueError,match='both named case ends'):
        module.select_history(meta,annual.iloc[:-1],located)
    annual.loc[0,'value_bn']+=.01
    with pytest.raises(ValueError,match='anchor changed'):
        module.select_history(meta,annual,located)


def test_coverage_health_removes_the_federal_subblock_before_rekeying():
    # National fullhealth100/federal80 includes VA20. Residual80/federal60.
    fraction=flow.residual_health_payer(.8,100.,20.)
    assert abs(80.*fraction-100.*.8+20.)<1e-12
    # Retaining the old mixed ratio would wrongly remove only16 federal.
    assert 80.*.8-100.*.8 == -16.


def test_capital_rate_never_becomes_borrowing():
    row = classify([],5.,"college","capital","one_rate",level="state_local")
    assert row["financing"] == "resource_cost"
    assert row["state_local_bn"] == 5.
    unknown = classify([],5.,"unknown","capital","one_rate")
    assert unknown["financing"] == "resource_cost" and unknown["federal_bn"] is None


def test_health_stock_change_uses_the_selected_rate():
    flow.require_capital_rate(dict(capital_stock_delta_bn=10.,delta_bn=.208),.0208)
    with pytest.raises(ValueError,match="selected Trustees rate"):
        flow.require_capital_rate(dict(capital_stock_delta_bn=10.,delta_bn=.3),.0208)


def test_production_net_is_unlocated_without_separate_P_and_F():
    row = classify([],3.,"production","production","native_minor_calibration")
    assert row["financing"] == "unlocated"
    assert row["federal_bn"] is None and row["state_local_bn"] is None


def test_source_receipt_uses_economic_side_and_preserves_displacement():
    base = [dict(side="receipt",id="housing_enterprise_surplus",responsive_bn=2.,federal_bn=.5,
                 financing="displaced_beneficiaries")]
    row = classify(base,-1.,"housing_enterprise_surplus","receipt","coverage_tenure")
    assert row["financing"] == "displaced_beneficiaries"
    assert row["federal_bn"] == -.25 and row["state_local_bn"] == -.75
