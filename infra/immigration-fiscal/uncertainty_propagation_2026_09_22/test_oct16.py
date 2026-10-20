"""Live v9 numerical/source contracts, separate from archived v8 route tests."""
import importlib.util
import hashlib
import json
from pathlib import Path
import subprocess
import sys

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
OUT = HERE/"derived/oct16"


@pytest.mark.parametrize("change,passes", [
    ({}, True),
    ({"adopted": "2026-10-16"}, False),
    ({"adopted": None}, False),
    ({"status": "candidate: main case v9"}, False),
    ({"v9": {"stub13": True}}, False),
    ({"v9": {}}, False),
])
def test_adopted_payload_preflight_is_cheap_and_rejects_stale_stamps(change, passes):
    payload = {"meta": {"adopted": "2026-10-20", "status": "adopted: main case v9", "v9": {"stub13": False}, **change}}
    script = "const q=require(process.argv[1]);q.validateAdoption({key:'oct16',lane:'main_case_2026_10_16'},JSON.parse(process.argv[2]));"
    run = subprocess.run(["node", "-e", script, str(HERE/"oct16_specs.cjs"), json.dumps(payload)],
                         capture_output=True, text=True, timeout=5)
    assert (run.returncode == 0) == passes
    if not passes:
        assert "[BLOCKED] oct16 sampling source: adopted non-STUB payload required" in run.stderr


def test_fixed_key_replicates_keep_calibrated_total_exact_and_block_real_drift():
    spec = importlib.util.spec_from_file_location("oct16_fixed_key_test", HERE/"propagate.py")
    prop = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prop)
    hf = np.ones(161) * .99
    hf[1:] += np.linspace(-1e-13, 1e-13, 160)
    np.testing.assert_array_equal(prop.fixed_key_replicates(1000., hf, .2), np.full(161, 198.))
    hf[1] += 1e-5
    with pytest.raises(ValueError, match="not calibrated"):
        prop.fixed_key_replicates(1000., hf, .2)


@pytest.mark.parametrize("basis", ["set", "cash"])
def test_relative_profile_invocation_reaches_own_key_guard(basis):
    root = HERE.parents[2]
    script = str((HERE/"oct16_sampling.py").relative_to(root))
    run = subprocess.run([sys.executable, "-m", "cProfile", script,
                          "--stage", basis, "--require-own"], cwd=root,
                         capture_output=True, text=True, timeout=10)
    assert run.returncode != 0
    assert "require_own: source10/11 deliver endpoint stacks only" in run.stderr


@pytest.mark.parametrize("kind,passes", [("full", True), ("no_personal", False), ("missing_source", False), ("nonfinite", False)])
def test_cash_oracle_requires_all_personal_rows_and_finite_comparisons(kind, passes):
    source = [dict(spec=i, cost_bn=300.+i, capital_bn=30.+i) for i in range(32)]
    rows = [dict(allocation="personal", live=q["cost_bn"], capital_live=q["capital_bn"]) for q in source]
    rows += [dict(allocation="shared") for _ in range(32)]
    if kind == "no_personal":
        rows = rows[32:]
    elif kind == "missing_source":
        source.pop()
    elif kind == "nonfinite":
        rows[0]["live"] = None
        source[0]["cost_bn"] = None
    script = "const q=require(process.argv[1]);const a=JSON.parse(process.argv[2]);const d=q.cashOracleDifferences(a.rows,a.source,'live','personal');if(d.length!==64||d.some(x=>x!==0))process.exit(3);"
    run = subprocess.run(["node", "-e", script, str(HERE/"oct16_specs.cjs"), json.dumps(dict(rows=rows, source=source))],
                         capture_output=True, text=True, timeout=5)
    assert (run.returncode == 0) == passes
    if not passes:
        assert "[BLOCKED] oct16 sampling source: cash oracle requires" in run.stderr


def test_item21_readonly_boundary_handles_both_rate_builds_and_blocks_changes(tmp_path):
    spec = importlib.util.spec_from_file_location("oct16_health_boundary_test", HERE/"health21_sampling.py")
    health = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(health)
    source = tmp_path/"producer.py"
    source.write_text("if True:\n    source_constant = 7\n\nif __name__ == '__main__':\n    forbidden_writer()\n\ndef main():\n    prices = source_constant\n    cov = coverage_build(prices)\n    cov_v9 = coverage_build(prices, capital_rate=.02)\n    write_output()\n")
    tree = health.readonly_producer_tree(source)
    namespace = {}
    exec(compile(tree, str(source), "exec"), namespace)
    assert namespace["main"]()["prices"] == 7
    source.write_text("def main():\n    cov = coverage_build(7)\n    unexpected = coverage_build(7)\n")
    with pytest.raises(ValueError, match="read-only boundary changed"):
        health.readonly_producer_tree(source)


def module():
    spec = importlib.util.spec_from_file_location("oct16_uncertainty_test", HERE/"oct16_sampling.py")
    value = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(value)
    return value


def test_source_cache_missing_or_mutated_payload_rejects(tmp_path):
    m = module()
    cache, manifest = tmp_path/"sources.json", tmp_path/"manifest.json"
    content = b'{"case":"oct16"}\n'
    with pytest.raises(ValueError, match="source manifest missing"):
        m.load_sources(cache, manifest)
    manifest.write_text(json.dumps(dict(path=str(m.SOURCE_CACHE.relative_to(m.ROOT)),
                                       bytes=len(content), sha256=hashlib.sha256(content).hexdigest())))
    with pytest.raises(ValueError, match="source cache missing"):
        m.load_sources(cache, manifest)
    cache.write_bytes(content)
    assert m.load_sources(cache, manifest) == {"case": "oct16"}
    cache.write_bytes(content.replace(b"oct16", b"oct15"))
    with pytest.raises(ValueError, match="differs from tracked manifest"):
        m.load_sources(cache, manifest)


def test_js_source_cache_missing_or_mutated_payload_rejects(tmp_path):
    m = module()
    cache, manifest = tmp_path/"sources.json", tmp_path/"manifest.json"
    content = b'{"case":"oct16"}\n'
    manifest.write_text(json.dumps(dict(path=str(m.SOURCE_CACHE.relative_to(m.ROOT)),
                                       bytes=len(content), sha256=hashlib.sha256(content).hexdigest())))
    script = "const q=require(process.argv[1]);console.log(JSON.stringify(q.loadSources(process.argv[2],process.argv[3])));"
    command = ["node", "-e", script, str(HERE/"oct16_specs.cjs"), str(cache), str(manifest)]
    missing = subprocess.run(command, capture_output=True, text=True, timeout=5)
    assert missing.returncode != 0 and "source cache missing" in missing.stderr
    cache.write_bytes(content)
    valid = subprocess.run(command, capture_output=True, text=True, check=True, timeout=5)
    assert json.loads(valid.stdout) == {"case": "oct16"}
    cache.write_bytes(content.replace(b"oct16", b"oct15"))
    changed = subprocess.run(command, capture_output=True, text=True, timeout=5)
    assert changed.returncode != 0 and "differs from tracked manifest" in changed.stderr


def test_source_anchor_follows_authoritative_rows_and_rejects_ambiguity():
    m = module()
    piece = dict(end="low", generation="G1", source_side="spending", source_line="x", line="x")
    anchor = dict(anchor_end="low", source_terms={"G1": {"spending:x": dict(cost_bn=2., key="population")}})
    row = dict(source_terms={"G1": {"spending:x": dict(cost_bn=6., key="population")}})
    assert m.source_ratio(piece, row, [row, anchor])[0] == 3.
    with pytest.raises(ValueError, match="unique authoritative source anchor"):
        m.source_ratio(piece, row, [row])
    with pytest.raises(ValueError, match="unique authoritative source anchor"):
        m.source_ratio(piece, row, [anchor, anchor])


def test_exported_source_anchors_reject_disagreeing_method_ends():
    script = "const q=require(process.argv[1]);const s=JSON.parse(process.argv[2]);console.log(JSON.stringify(q.anchorSpecs(s,'set')));"
    for ends, passes in (([[3, 7], [3, 7]], True), ([[3, 7], [4, 7]], False)):
        run = subprocess.run(["node", "-e", script, str(HERE/"oct16_specs.cjs"),
                              json.dumps(dict(end_specifications=dict(set=ends)))],
                             capture_output=True, text=True, timeout=5)
        assert (run.returncode == 0) == passes
        if passes:
            assert json.loads(run.stdout) == [3, 7]
        else:
            assert "common authoritative method ends" in run.stderr


def test_retained_lookup_preserves_coincident_specs_and_rejects_id_drift():
    m = module()
    coordinates = dict(normalization="cash", uc="uninsured_use_low", justice="use", share=.7, school=1., gg=.6)
    rows = pd.DataFrame([dict(spec=i, normalization="cash", medicaid_key="uninsured_use_low", justice_key="use",
                              school_share=.7, school_response=1., general_government_response=.6,
                              net_cost_bn=100.+i) for i in range(32)])
    assert m.retained_scalar(rows, 4, coordinates).net_cost_bn == 104.
    rows.loc[4, "spec"] = 0
    with pytest.raises(ValueError, match="all32 unique specification IDs"):
        m.retained_scalar(rows, 4, coordinates)
    rows.loc[4, "spec"] = 4
    rows.loc[4, "school_response"] = .8
    with pytest.raises(ValueError, match="coordinates differ"):
        m.retained_scalar(rows, 4, coordinates)


def test_pes_feasible_bounds_cover_signed_psd_correlations():
    m = module()
    gradient = np.array([-200., 100., -80.])
    errors = np.array([.0053, .007, .0087])
    independent, minimum, maximum = m.pes_sigma(gradient, errors)
    signed = gradient*errors
    assert maximum == pytest.approx(np.abs(signed).sum())
    assert minimum <= independent <= maximum
    # Perfect sign-aligned rank-one correlation is PSD and attains the upper.
    correlation = np.outer(np.sign(signed), np.sign(signed))
    assert np.linalg.eigvalsh(correlation).min() > -1e-12
    assert np.sqrt(signed@correlation@signed) == pytest.approx(maximum)


@pytest.mark.parametrize("basis", ["set", "cash"])
def test_live_shared_vectors_and_interval_owners(basis):
    m = module()
    data = json.loads((OUT/f"sampling_{basis}.json").read_text())
    summary = json.loads((OUT/"summary.json").read_text())
    source = m.load_sources()["sets"][basis]
    core_costs = pd.read_csv(OUT/f"core_{basis}/spec_costs.csv")
    assert len(core_costs) == 32 and set(core_costs.allocation) == {"personal"}
    np.testing.assert_allclose(core_costs.cost_oct16_bn, [r["cost_bn"] for r in source["rows"]], rtol=0, atol=1e-9)
    np.testing.assert_allclose(core_costs.capital_oct16_bn, [r["capital_bn"] for r in source["rows"]], rtol=0, atol=1e-9)
    coverage = json.loads((OUT/f"coverage_replicates_{basis}.json").read_text())
    assert coverage["vintage"] == "oct15"
    assert data["count_vintage"] == "oct15_final_routing"
    assert coverage["support_sha256"] == data["support_sha256"]
    assert coverage["support_sha256"]["weights"]["shape"][1] == 161
    for principal in (r for r in source["rows"] if r["anchor_end"] is not None):
        spec, reading = principal["spec"], principal["anchor_end"]
        assert coverage["rows"][str(spec)]["replicates_bn"][0] == pytest.approx(
            source["meta"]["coverage"]["by_end"][reading]["total_bn"], abs=1e-9)
    rows = data["rows"]
    assert len(rows) == 32 and {r["spec"] for r in rows} == set(range(32))
    assert "not an unconditional total uncertainty bound" in summary["status"]
    for row, principal in zip(rows, source["rows"]):
        assert row["net_cost_bn"] == principal["cost_bn"]
        cps = np.asarray(data["cps_deviations_bn"][str(row["spec"])])
        acs = np.asarray(data["acs_target_changes_bn"][str(row["spec"])])
        assert cps.shape == (161,) and acs.shape == (81,)
        assert cps[0] == acs[0] == 0
        assert m.sdr(cps) == pytest.approx(row["se_conditional_cps_bn"], abs=1e-10)
        assert m.sdr(acs) == pytest.approx(row["se_acs_targets_bn"], abs=1e-10)
        assert row["se_pes_feasible_min_bn"] <= row["se_pes_independent_bn"] <= row["se_pes_feasible_max_bn"]
        expected = np.sqrt(row["se_conditional_cps_bn"]**2+row["se_acs_targets_bn"]**2+row["se_pes_independent_bn"]**2)
        assert row["se_cps_acs_pes_independent_bn"] == pytest.approx(expected)
    final = pd.read_csv(OUT/f"case_uncertainty_{basis}.csv").to_dict("records")
    assembled = json.loads((OUT/f"assembled_vectors_{basis}.json").read_text())
    core = json.loads((OUT/f"core_{basis}/account_replicates.json").read_text())
    for row in final:
        raw = assembled[str(row["spec"])]
        assert m.sdr(raw["complete_cps_deviation_bn"]) == pytest.approx(row["se_cps_fiscal_keys_bn"], abs=1e-10)
        assert row["se_cps_retained_source_stacks_bn"] > 1
        variance = row["se_cps_retained_source_stacks_bn"]**2+row["se_cps_v9_delta_bn"]**2+2*row["retained_delta_covariance_bn2"]
        assert variance == pytest.approx(row["se_cps_fiscal_keys_bn"]**2, abs=1e-9)
        assert row["se_item21_pooled_ratio_bn"] > 0
        college = np.asarray(core["specifications"][str(row["spec"])]["item15_engine_replicates_bn"])
        assert college.shape == (161,) and abs(college[0]) > .1
        np.testing.assert_array_equal(college, np.full(161, college[0]))
    for label, field, take in (("independent_low", "ci95_low_bn", min), ("independent_high", "ci95_high_bn", max),
                               ("pes_correlated_low", "ci95_pes_correlated_low_bn", min),
                               ("pes_correlated_high", "ci95_pes_correlated_high_bn", max)):
        owner = summary["sets"][basis][label]
        assert owner["value_bn"] == pytest.approx(take(r[field] for r in final), abs=1e-10)
        assert owner["specifications"] == [r["spec"] for r in final if abs(r[field]-owner["value_bn"]) < 1e-10]


def test_live_source_hashes_and_acs_universe():
    m = module()
    for record in (m.load_sources(), json.loads((OUT/"acs_targets.json").read_text())):
        for relative, digest in record["source_sha256"].items():
            assert m.digest(m.ROOT/relative) == digest
    targets = json.loads((OUT/"acs_targets.json").read_text())["targets"]
    assert len(targets) == 8
    assert all(len(v["mexican"]) == 81 for v in targets.values())
    # Every ACS target uses the source's exact active-duty/institution exclusion.
    source = json.loads((m.COUNT/"derived/native_calibration_replicates.json").read_text())["cells"]
    for key, value in targets.items():
        assert value["mexican"][0] == source[key]["target_mexican"][0]


def test_zero_endpoint_support_cannot_create_an_interior_source():
    m = module()
    piece = dict(end="low", generation="G1", source_side="spending", source_line="x", line="x")
    rows = [dict(source_terms={"G1": {"spending:x": dict(cost_bn=0., key="population")}}) for _ in range(32)]
    rows[3]["anchor_end"] = "low"
    row = dict(source_terms={"G1": {"spending:x": dict(cost_bn=1., key="population")}})
    with pytest.raises(ValueError, match="zero endpoint support"):
        m.source_ratio(piece, row, rows)


def test_school_budget_share_does_not_invent_a_new_source_person_mixture():
    m = module()
    # Producer household line_split fixes these vector shares from generation
    # key masses. Equal evaluated dollars therefore mean equal coefficients,
    # even if a specification's school budget-share coordinate changes.
    anchor = dict(source_terms={"G1": {"spending:education_services": dict(cost_bn=20., key="education_mix")}},
                  coordinates=dict(share=.7))
    row = dict(source_terms=anchor["source_terms"], coordinates=dict(share=.9))
    rows = [dict(anchor_end="low", **anchor)]
    for driver in ("canonical spending:school_part", "canonical spending:P_part"):
        piece = dict(end="low", generation="G1", source_side="spending", source_line="education_services",
                     line="education_services", key=driver)
        assert m.source_ratio(piece, row, rows)[0] == 1.


def test_item21_uses_own_pooled_ofd_stl_covariance():
    m = module()
    record = json.loads((OUT/"item21_pooled_covariance.json").read_text())
    assert record["measure"] == "ofd_stl" and len(record["cells"]) == 10
    covariance = np.asarray(record["covariance"])
    np.testing.assert_allclose(np.diag(covariance), [r["se"]**2 for r in record["cells"]], rtol=1e-12, atol=1e-12)
    assert np.linalg.eigvalsh(covariance).min() > -1e-10
    assert np.count_nonzero(covariance-np.diag(np.diag(covariance))) > 0
    for path, expected in record["source_sha256"].items():
        assert m.digest(m.ROOT/path) == expected


def test_unselected_item19_cannot_enter_central_cps_estimator():
    m = module()
    for applied in (False,):
        meta = {"items": [{"id": "passthrough_source_tax", "applied": applied}],
                "passthrough_source_tax": {"by_end": "deliberately invalid unselected diagnostic"}}
        np.testing.assert_array_equal(m.passthrough_replicates(meta, "low"), np.zeros(161))
    np.testing.assert_array_equal(m.passthrough_replicates({"items": []}, "high"), np.zeros(161))
    with pytest.raises(ValueError, match="beside-only19"):
        m.passthrough_replicates({"items": [{"id": "passthrough_source_tax", "applied": True}]}, "low")


def test_allocation_items_can_own_real_edits_but_must_tile_the_payload():
    path = HERE/"propagate.py"
    spec = importlib.util.spec_from_file_location("oct16_payload_blocks_test", path)
    prop = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(prop)
    p = {"edits": [{}, {}, {}], "meta": {"lineage": {"edits": {"first": 0, "count": 1, "row8_edit_index": 0}},
         "items": [{"id": "basket", "kind": "allocation", "applied": True, "edits": {"first": 1, "count": 2}}]}}
    assert prop.payload_blocks(p)["items"][0]["id"] == "basket"
    p["meta"]["items"][0]["edits"]["first"] = 2
    with pytest.raises(ValueError, match="do not follow"):
        prop.payload_blocks(p)
