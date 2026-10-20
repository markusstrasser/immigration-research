"""Selected-case economic outputs and native routing must retain their identity."""
import hashlib
import json
import sys

import coverage_recipient_values as CR
import pytest
import v9_snapshot as SNAPSHOT
from population_basis import economic_path


def test_economic_outputs_keep_case_identity_and_historical_basis(tmp_path):
    source = tmp_path / "group_ages.csv"
    current = economic_path(source, "oct15", "oct15")
    future = economic_path(source, "oct15", "future")
    current.write_text("current case\n")
    future.write_text("future case\n")
    assert current.read_text() == "current case\n"
    assert future != current
    assert economic_path(source, "lineage", "oct05").name == "group_ages_lineage.csv"
    assert economic_path(source, "cps").name == "group_ages.csv"
    with pytest.raises(SystemExit, match="invalid economic case key"):
        economic_path(source, "oct15", "../oct15")


def test_native_routing_is_case_pinned_and_has_no_previous_case_fallback(tmp_path, monkeypatch):
    directory = tmp_path / "future_final_routing"
    directory.mkdir()
    files = {}
    for name in ("lines.json", "lines_cash.json", "adoption_receipt.md"):
        path = directory / name
        path.write_text("future native source\n")
        files[name] = {"bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
    (directory / "manifest.json").write_text(json.dumps({"vintage": "future_final_routing",
        "files": {name: files[name] for name in ("lines.json", "lines_cash.json")}, "adoption": files["adoption_receipt.md"]}))
    frozen = tmp_path / "future_coverage_source.json"
    frozen.write_text("{}\n")
    monkeypatch.setitem(CR.V.PINS, "future", {"coverage_routing_dir": str(directory), "coverage_source_receipt": str(frozen)})
    assert CR.routing_paths("future", "cash") == (directory / "lines_cash.json", frozen)
    (directory / "lines_cash.json").write_text("changed native source\n")
    with pytest.raises(SystemExit, match="stale selected routing source"):
        CR.routing_paths("future", "cash")
    monkeypatch.setitem(CR.V.PINS, "missing", {})
    with pytest.raises(SystemExit, match="selected missing native routing receipt absent"):
        CR.routing_paths("missing", "cash")


def test_snapshot_capture_cannot_silently_omit_missing_historical_input(tmp_path, monkeypatch):
    lane = tmp_path / "world"
    (lane / "inputs").mkdir(parents=True)
    (lane / "inputs/oct15_source_hashes.json").write_text(json.dumps({"sha256": {"missing_input.json": "recorded-hash"}}))
    monkeypatch.setattr(SNAPSHOT, "HERE", lane)
    monkeypatch.setattr(SNAPSHOT, "ROOT", tmp_path)
    monkeypatch.setattr(SNAPSHOT, "require_adopted", lambda key: None)
    with pytest.raises(SystemExit, match="missing historical selected input missing_input.json"):
        SNAPSHOT.capture()


@pytest.mark.parametrize("entrypoint", ["snapshot", "driver", "artifact", "routing"])
def test_fresh_world_route_and_capture_cannot_bypass_adoption(monkeypatch, entrypoint):
    def rejected(key):
        assert key == "oct16"
        raise SystemExit("[BLOCKED] adoption: stale live key")
    monkeypatch.setattr(SNAPSHOT, "require_adopted", rejected)
    with pytest.raises(SystemExit, match="stale live key"):
        if entrypoint == "snapshot":
            SNAPSHOT.capture()
        elif entrypoint == "driver":
            import run_oct15 as ROUTE
            monkeypatch.setattr(ROUTE.V, "require_pins", lambda *args: None)
            monkeypatch.setattr(sys, "argv", ["run_oct15.py", "--case", "oct16"])
            ROUTE.main()
        elif entrypoint == "artifact":
            import v9_artifact as ARTIFACT
            ARTIFACT.run(capture=True)
        else:
            import v9_routing as ROUTING
            ROUTING.capture()
