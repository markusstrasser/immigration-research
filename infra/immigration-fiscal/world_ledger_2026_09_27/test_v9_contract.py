"""V9 source closure, joint-count identity and worktree drift regressions."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from gz_io import read_artifact
import v9_snapshot as S
import coverage_transport as CT

HERE = Path(__file__).resolve().parent


def test_snapshot_detects_selected_source_tampering(tmp_path, monkeypatch):
    source = tmp_path / "selected.json"
    source.write_text("source\n")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps(dict(case="oct16", provenance="[WORKTREE INPUT]",
        sha256={source.name: hashlib.sha256(source.read_bytes()).hexdigest()})))
    monkeypatch.setattr(S, "ROOT", tmp_path)
    monkeypatch.setattr(S, "FILE", receipt)
    S.verify()
    (tmp_path / "unrelated.json").write_text("peer work\n")
    S.verify()
    source.write_text("changed\n")
    with pytest.raises(SystemExit, match="changed selected input"):
        S.verify()


def test_required_donor_source_must_be_explicitly_enrolled(tmp_path, monkeypatch):
    source = tmp_path / "coverage_oct16.py"
    source.write_text("source\n")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps(dict(case="oct16", provenance="[WORKTREE INPUT]", sha256={})))
    monkeypatch.setattr(S, "ROOT", tmp_path)
    monkeypatch.setattr(S, "FILE", receipt)
    with pytest.raises(SystemExit, match="undeclared selected input"):
        S.verify([source])


@pytest.mark.parametrize("when", ["before", "during"])
def test_donor_export_rejects_changed_builder_before_publication(tmp_path, monkeypatch, when):
    import sys
    from types import SimpleNamespace
    import v9_transport as T
    source_path = tmp_path / "coverage_oct16.py"
    source_path.write_text("reviewed source\n")
    receipt = tmp_path / "receipt.json"
    receipt.write_text(json.dumps(dict(case="oct16", provenance="[WORKTREE INPUT]",
        sha256={source_path.name: hashlib.sha256(source_path.read_bytes()).hexdigest()})))
    monkeypatch.setattr(S, "ROOT", tmp_path)
    monkeypatch.setattr(S, "FILE", receipt)
    monkeypatch.setattr(S, "donor_paths", lambda: {source_path})
    data = dict(weights=np.ones((1, 1)), added_weights=np.zeros((1, 1)), generation=np.array([0]),
                person_ph_seq=np.array([1]), person_pppos=np.array([1]), age=np.array([25]), sex=np.array([1]))
    def fixed(*args):
        source_path.write_text("changed donor algorithm\n")
        return np.zeros(1), None
    source = SimpleNamespace(load_kernel=lambda *a: (data, {}), load=lambda: (None, None),
        person_inputs=lambda d: (np.ones(1), np.ones(1)), fixed_count_tenure=fixed, GENS=("G1", "G2", "G3plus"),
        C=SimpleNamespace(factors=lambda *a: (np.zeros(1), np.zeros(1))))
    monkeypatch.setitem(sys.modules, "coverage_oct16", source)
    monkeypatch.setattr(T.V, "case_payload", lambda case: {"meta": {"coverage_tenure": {
        "coverage_counts_by_generation": dict(G1=0., G2=0., G3plus=0.)}}})
    if when == "before":
        source_path.write_text("changed donor algorithm\n")
    with pytest.raises(SystemExit, match="changed selected input"):
        T.export("cash")


def test_observed_recipient_calibration_holds_latent_descendants_fixed():
    from coverage_recipient_values import observed_calibration_mass
    identified, latent, factor = np.array([10., 20.]), np.array([5., 7.]), np.array([.8, 1.])
    correction = observed_calibration_mass(identified, factor)
    assert correction.tolist() == pytest.approx([-2., 0.])
    assert (identified + latent + correction).tolist() == pytest.approx((identified * factor + latent).tolist())


def test_rate_post_recovers_attributed_public_capital_without_changing_fiscal_delta():
    artifact = json.loads(read_artifact(HERE / "inputs/pension_cash_cells_oct16.json.gz"))
    for basis, block in artifact["results"].items():
        rate = block["payload"]["meta"]["one_rate"]["flat_real_equivalent"]
        lines = pd.DataFrame(block["lines"])
        for end, old_rate in (("low", .02), ("high", .03)):
            parts = block["payload"]["meta"]["coverage"]["by_end"][end]["decomposition"]["line_parts"]
            for part in parts:
                if part.get("id") != "one_rate" or part.get("component") != "capital_engine" or part["source_line"] not in ("gps_sl", "gps_fed"):
                    continue
                base = lines[lines.band_end.eq(end) & lines.generation.eq(part["generation"])
                             & lines.line.eq("capital_" + part["source_line"])].iloc[0]
                assert part["source_response"] == pytest.approx(base.response, abs=1e-12)
                assert part["coverage_bn"] == part["by_generation_bn"][part["generation"]]
                assert base.amount_bn + part["coverage_bn"] / part["source_response"] == pytest.approx(
                    base.amount_bn * rate / old_rate, abs=1e-9)


def test_count_atom_identities_preserve_capped_programs_across_pension_bases():
    artifact = json.loads(read_artifact(HERE / "inputs/pension_cash_cells_oct16.json.gz"))
    programs = {"housing_subsidies", "energy_assistance", "housing_enterprise_surplus"}
    selected = {}
    for basis, block in artifact["results"].items():
        rows = [(end, row) for end, part in block["payload"]["meta"]["coverage"]["by_end"].items()
                for row in part["decomposition"]["line_parts"] if row.get("source_line") in programs]
        values = {(end, row["generation"], row["line"]): row["coverage_bn"] for end, row in rows}
        assert len(values) == len(rows)
        selected[basis] = values
    assert selected["set"].keys() == selected["cash"].keys()
    assert selected["set"] == pytest.approx(selected["cash"], abs=1e-9)


def test_unrelated_zero_and_pension_rows_cannot_relabel_a_shared_source_atom():
    import subprocess
    code = """
const {sourceRecordId}=require(process.argv[1]);
function ids(rows){const occurrences=new Map();return rows.map(row=>({row,
 id:sourceRecordId([row.kind,row.line],occurrences).id})).filter(x=>x.row.amount!==0&&x.row.line==='housing_subsidies').map(x=>x.id);}
const shared=[{kind:'transfer',line:'housing_subsidies',amount:1},{kind:'transfer',line:'housing_subsidies',amount:2}];
const changed=[{kind:'pension',line:'social_security',amount:3},shared[0],
 {kind:'transfer',line:'energy_assistance',amount:0},shared[1]];
if(JSON.stringify(ids(shared))!==JSON.stringify(ids(changed)))process.exit(1);
if(new Set(ids(shared)).size!==shared.length)process.exit(2);
"""
    subprocess.run(["node", "-e", code, str(HERE / "source_identity.cjs")], check=True)


def test_live_cash_adapter_passes_unchanged_displaced_source_gates():
    import io
    import pension_cash as P
    import world_ledger as W
    artifact = json.loads(read_artifact(HERE / "inputs/pension_cash_cells_oct16.json.gz"))
    raw = artifact["results"]["set"]
    valued = {basis: P._value("oct16", block, basis=basis) for basis, block in artifact["results"].items()}
    glines, generations, union = valued["set"]
    pin = W.PINS["oct16"]
    channels = W.pinned_csv(pin["winners"], pin["dirs"]["winners"] + "/channels.csv").set_index("id")
    inputs = dict(case="oct16", pension_basis="full_accrual", glines=glines, vgen=generations, val=union,
        specs=pd.DataFrame(raw["specs"]).set_index("band_end"), ch=channels,
        gen=pd.read_csv(io.StringIO(raw["generation_results_csv"])),
        mxb=pd.DataFrame([dict(item="pensions paid", bn=1.)]))
    cash = P.adapt_cash(inputs, valuation_builder=lambda case, block, basis: valued[basis])
    assert cash["pension_meta"]["checks"]["displaced_sources_unchanged"] < 1e-9
    assert cash["specs"].cost_bn.tolist() == pytest.approx(artifact["results"]["cash"]["oracle_bn"], abs=1e-9)


def test_nested_component_json_never_enters_scalar_dataframe_constructor(monkeypatch):
    from types import SimpleNamespace
    import cash_readings as C
    components = [dict(line="social_security", component_side="spending", cls="cash", G_bn=2.),
                  dict(line="federal_income_tax", component_side="receipt", cls="tax", G_bn=-1.)]
    raw = pd.DataFrame([dict(end="low", line="coverage_fixture", net_cost_bn=1.,
                            recipient_components_json=json.dumps(components))])
    contract = pd.DataFrame(columns=["end", "line"])
    def scalar_frame(records):
        assert all("recipient_components_json" not in row for row in records)
        return pd.DataFrame(records)
    monkeypatch.setattr(C, "pd", SimpleNamespace(DataFrame=scalar_frame))
    out = C.recipient_cells(raw, contract)
    assert len(out) == 2
    assert out.net_cost_bn.sum() == 1.


@pytest.mark.parametrize("origin", ["coverage_fixture", "v9_counted_fixture"])
def test_declared_employer_mix_uses_actual_end_in_both_population_scopes(origin):
    import world_ledger as W
    frame = pd.DataFrame([dict(generation="G2", end=end, net_cost_bn=value, origin_line=origin,
        recipient_component_transport="signed_proportional_source_mix") for end, value in (("low", -2.), ("high", -3.))])
    inputs = dict(pension_basis="matched_cash", account_end="low")
    assert W.employer_compensation_at_end(inputs, frame, "G2") == 2.
    inputs["account_end"] = "high"
    assert W.employer_compensation_at_end(inputs, frame, "G2") == 3.
    with pytest.raises(SystemExit, match="employer_compensation_G2"):
        W.employer_compensation_at_end(inputs, frame.drop(columns="recipient_component_transport"), "G2")


def test_valid_employer_mix_cannot_waive_unrelated_direct_receipt_drift():
    import world_ledger as W
    frame = pd.DataFrame([dict(generation="G2", end=end, net_cost_bn=value,
        recipient_component_transport=marker) for end, value, marker in (
            ("low", -.1, "signed_proportional_source_mix"), ("high", -.2, "signed_proportional_source_mix"),
            ("low", -2., None), ("high", -3., None))])
    inputs = dict(pension_basis="matched_cash", account_end="high")
    with pytest.raises(SystemExit, match="employer_compensation_G2"):
        W.employer_compensation_at_end(inputs, frame, "G2")
    frame.loc[frame.recipient_component_transport.isna(), "net_cost_bn"] = -2.
    assert W.employer_compensation_at_end(inputs, frame, "G2") == pytest.approx(2.2)


@pytest.mark.parametrize("source_class", ["proportional_mix", "cash"])
def test_employer_transport_marker_requires_canonical_source_class(source_class):
    import cash_readings as C
    components = [dict(line="employer_oasdi", component_side="receipt", cls="tax", G_bn=-1.)]
    raw = pd.DataFrame([dict(end="low", line="coverage_fixture", net_cost_bn=-1., cls=source_class,
                            recipient_components_json=json.dumps(components))])
    out = C.recipient_cells(raw, pd.DataFrame(columns=["end", "line"]))
    assert ("recipient_component_transport" in out) == (source_class == "proportional_mix")


def test_v9_cells_close_to_both_principal_sets():
    summary = json.loads((HERE.parent / "main_case_2026_10_16/derived/summary.json").read_text())["v9"]
    for suffix, field in (("", "band_bn"), ("_cash", "cash_set_bn")):
        frame = pd.read_csv(HERE / f"derived/generation_lines_oct16{suffix}.csv")
        for i, end in enumerate(("low", "high")):
            values = frame[frame.band_end.eq(end)]
            costs = values[values.side.eq("total") & values.line.eq("cost")].effect_bn.sum()
            assert costs == pytest.approx(summary[field][i], abs=1e-9)
            fiscal = -values[values.side.ne("total")].effect_bn.sum()
            production = values[values.side.eq("total") & values.line.eq("production")].effect_bn.sum()
            assert fiscal + production == pytest.approx(costs, abs=1e-9)
            assert not values.line.str.contains("v9_passthrough_source_tax").any()


def test_joint_donor_counts_use_final_calibrated_generation_contract():
    payload = json.loads((HERE.parent / "main_case_2026_10_16/derived/corrections.json").read_text())
    donors, receipt = CT.load_donors("oct16", "cash")
    target = payload["meta"]["coverage_tenure"]["coverage_counts_by_generation"]
    for g, want in target.items():
        actual = donors.coverage_weight[donors.generation.eq(g.replace("G3plus", "G3+"))].sum()
        assert actual == pytest.approx(want, abs=1e-6)
    assert donors.coverage_weight.sum() == pytest.approx(payload["meta"]["population_v9"]["coverage"], abs=1e-6)
    assert receipt["scenario"] == "central_joint16_17"


def test_oct16_service_general_prices_preserve_all_source_fiscal_dollars():
    from service_prices import price_us_services, price_levels
    frame = pd.read_csv(HERE / "derived/valuation_by_generation_oct16.csv")
    priced = price_us_services(frame)
    for column in ("G_bn", "net_cost_bn", "amount_bn", "source_tax_credit_bn"):
        pd.testing.assert_series_equal(priced[column], frame[column])
    health = frame.line.eq("medicare")
    assert health.any()
    assert np.allclose(priced.loc[health, "V_central_bn"], frame.loc[health, "V_central_bn"]
                       * price_levels()["1000000"] / price_levels()["9080000"])


@pytest.mark.parametrize("column", ["amount_bn", "effect_bn", "response"])
def test_scalar_finite_gate_rejects_each_nonfinite_source_field(column):
    from types import SimpleNamespace
    import valuation as V
    values = dict(side="spending", line="health_services", amount_bn=1., effect_bn=-1., response=1.)
    values[column] = np.nan
    with pytest.raises(SystemExit, match="finite_line_health_services"):
        V.valuation_row(SimpleNamespace(**values), {}, {})


@pytest.mark.parametrize("line", ["veterans_pension_disability", "military_medical", "veterans_other"])
def test_zero_response_military_keeps_declared_effect_valuation(line):
    """Military fiscal-response changes do not change the lane's value basis."""
    from types import SimpleNamespace
    import valuation as V
    row = SimpleNamespace(side="spending", line=line, amount_bn=2., response=0., effect_bn=0.)
    _, cost, value, _ = V.value_line(row)
    assert cost == 0.
    assert value == [0., 0., 0.]
    row.line = "defense"
    _, cost, value, _ = V.value_line(row)
    assert cost == 0.
    assert value == [2., 2., 2.]


def test_superseded_case_outputs_are_never_rewritten(tmp_path, monkeypatch):
    import os
    import valuation as V
    frame = pd.DataFrame({"a": [1.5]})
    derived = tmp_path / "derived"
    derived.mkdir()
    monkeypatch.setattr(V, "HERE", tmp_path)
    frozen = derived / "x_oct15.csv"
    frozen.write_text(frame.to_csv(index=False, lineterminator="\n"))
    os.utime(frozen, (0, 0))
    V.write_case_csv(frame, frozen, "oct15")                       # same bytes: left untouched
    assert frozen.stat().st_mtime == 0
    with pytest.raises(SystemExit, match="historical_output_unchanged"):
        V.write_case_csv(pd.DataFrame({"a": [2.5]}), frozen, "oct15")
    V.write_case_csv(frame, derived / "absent_oct15.csv", "oct15")   # history is never created
    assert not (derived / "absent_oct15.csv").exists()
    V.write_case_csv(frame, derived / "x_oct16.csv", V.LIVE_CASE)  # the live case writes
    assert (derived / "x_oct16.csv").read_text() == "a\n1.5\n"
    V.write_case_csv(frame, tmp_path / "x_oct15.csv", "oct15")     # outside derived/: a test's scratch output
    assert (tmp_path / "x_oct15.csv").is_file()


def test_gzip_artifacts_are_deterministic_and_pinned_on_content(tmp_path):
    from gz_io import gzip_bytes, write_csv_gz
    body = b'{"x": 1}\n'
    assert gzip_bytes(body) == gzip_bytes(body) and read_artifact_bytes(tmp_path, gzip_bytes(body)) == body
    frame = pd.DataFrame({"a": [1.0, 2.0]})
    write_csv_gz(frame, tmp_path / "one.csv.gz")
    write_csv_gz(frame, tmp_path / "two.csv.gz")
    assert (tmp_path / "one.csv.gz").read_bytes() == (tmp_path / "two.csv.gz").read_bytes()
    assert pd.read_csv(tmp_path / "one.csv.gz").equals(frame)
    record = json.loads((HERE / "inputs/pension_cash_pins.json").read_text())["artifacts"]["oct16_cash"]
    assert record["path"].endswith(".json.gz")
    assert hashlib.sha256(read_artifact(HERE / record["path"])).hexdigest() == record["sha256"]


def read_artifact_bytes(tmp_path, compressed):
    path = tmp_path / "artifact.json.gz"
    path.write_bytes(compressed)
    return read_artifact(path)
