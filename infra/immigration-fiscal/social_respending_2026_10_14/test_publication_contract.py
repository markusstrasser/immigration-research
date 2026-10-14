"""Negative controls for independently entered stacks and interrupted publication."""
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest
import respending as R
import stack as S
import pin_inputs as P


def test_standalone_stack_rejects_stale_input_before_output(monkeypatch, tmp_path):
    (tmp_path / "inputs").mkdir()
    (tmp_path / "source").write_text("changed")
    (tmp_path / "inputs/pins.json").write_text(json.dumps([
        dict(path="source", sha256="not-the-source-hash")]))
    monkeypatch.setattr(R, "HERE", tmp_path)
    monkeypatch.setattr(P, "INPUTS", {"source":"fixture"})
    with pytest.raises(ValueError, match="changed pinned input source"):
        S.main()


def test_standalone_stack_requires_every_declared_pin(monkeypatch, tmp_path):
    (tmp_path / "inputs").mkdir()
    (tmp_path / "inputs/pins.json").write_text("[]")
    monkeypatch.setattr(R, "HERE", tmp_path)
    monkeypatch.setattr(P, "INPUTS", {"source":"new required source"})
    with pytest.raises(ValueError,match="pin coverage differs"):
        S.main()


def test_unique_row_gate_survives_python_optimization():
    env = dict(os.environ, PYTHONPATH=str(Path(S.__file__).parent))
    result = subprocess.run([sys.executable, "-O", "-c", "import stack; stack.one([],end='low')"],
                            env=env, capture_output=True, text=True)
    assert result.returncode != 0
    assert "[BLOCKED] unique producer row" in result.stderr


def test_interrupted_publication_never_validates_mixed_generation(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path)
    R.publish_bundle("test", {"a.csv":"old-a\n", "b.csv":"old-b\n"})
    original_replace = R.os.replace
    calls = 0
    def interrupted(source, target):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("injected publication interruption")
        return original_replace(source, target)
    monkeypatch.setattr(R.os, "replace", interrupted)
    with pytest.raises(OSError, match="injected publication"):
        R.publish_bundle("test", {"a.csv":"new-a\n", "b.csv":"new-b\n"})
    with pytest.raises(ValueError, match="mixed or stale test generation"):
        R.verify_bundle("test")
    monkeypatch.setattr(R.os, "replace", original_replace)
    R.publish_bundle("test", {"a.csv":"new-a\n", "b.csv":"new-b\n"})
    R.verify_bundle("test")
    assert (tmp_path / "a.csv").read_text() == "new-a\n"


def test_valid_individual_bundles_cannot_mix_upstream_generations(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "BUNDLE_DEPENDENCIES", {"respending":[], "stack":["respending_generation.json"]})
    R.publish_bundle("respending", {"items.csv":"old\n"})
    dependencies = R.dependency_snapshot(tmp_path, ["respending_generation.json"])
    R.publish_bundle("stack", {"stacks.csv":"old-stack\n"}, dependencies=dependencies)
    R.verify_bundle("stack")
    R.publish_bundle("respending", {"items.csv":"new\n"})
    R.verify_bundle("respending")
    with pytest.raises(ValueError, match="stale stack dependency generation"):
        R.verify_bundle("stack")


def test_case_input_change_rejects_read_and_inflight_publication(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path)
    monkeypatch.setattr(R, "BUNDLE_DEPENDENCIES", {"respending":["case_inputs.json"]})
    (tmp_path/"case_inputs.json").write_text("old")
    dependencies = R.dependency_snapshot(tmp_path, ["case_inputs.json"])
    R.publish_bundle("respending", {"items.csv":"old\n"}, dependencies=dependencies)
    (tmp_path/"case_inputs.json").write_text("new")
    with pytest.raises(ValueError, match="stale respending dependency generation"):
        R.verify_bundle("respending")
    with pytest.raises(ValueError, match="dependencies changed during computation"):
        R.publish_bundle("respending", {"items.csv":"old\n"}, dependencies=dependencies)


def test_legacy_or_incomplete_producer_receipt_is_rejected(monkeypatch, tmp_path):
    monkeypatch.setattr(R, "OUT", tmp_path)
    path = tmp_path/"stack_generation.json"
    for receipt in ({"files":{}}, {"files":{}, "dependencies":{}}):
        path.write_text(json.dumps(receipt))
        with pytest.raises(ValueError, match="receipt lacks"):
            R.verify_bundle("stack")


def test_named_stack_replaces_exact_frozen_sender_levels():
    old = json.loads((R.FISCAL/"sept24_propagation_2026_09_24/derived/oct14/real_costs_totals.json").read_text())["lineage_social_rows"]["rows"]
    for row in R.read_csv(R.OUT/"conditional_stacks.csv"):
        for item, delta, target in [("pm25_consumption","mortality_delta_bn","pm_gross_replacement_bn"),
                                    ("road_crash_externality","crash_delta_bn","crash_replacement_bn")]:
            embedded = next(x for x in old if x["item"]==item)
            end = row["end"]
            original = embedded[f"union_before_boundary_{end}_bn"]*(1+embedded[f"share_{end}"])
            assert original+float(row[delta]) == pytest.approx(float(row[target]), abs=1e-9)
