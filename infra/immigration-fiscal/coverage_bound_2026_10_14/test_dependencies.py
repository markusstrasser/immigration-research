"""Regression for same-total source changes and unpinned transitive reads."""
import json
import hashlib
from pathlib import Path

import pytest

import dependency_manifest as D
import coverage_bound as C
import export_pricing as E


@pytest.mark.parametrize("missing", [False, True])
def test_frozen_generation_archive_fails_closed(tmp_path, monkeypatch, missing):
    (tmp_path / "inputs").mkdir()
    source = tmp_path / "inputs/generation_results_original.csv"
    source.write_bytes(b"original committed rows")
    pin = {"generation_results_original.csv": {"sha256": hashlib.sha256(source.read_bytes()).hexdigest()}}
    pins = tmp_path / "inputs/pins.json"
    pins.write_text(json.dumps(pin))
    monkeypatch.setattr(E, "LANE", tmp_path)
    monkeypatch.setattr(E, "PINS", pins)
    E.verify_local_pins()
    if missing:
        source.unlink()
    else:
        source.write_bytes(b"concurrent new rows")
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] .*frozen generation input"):
        E.verify_local_pins()


def fixture_manifest(tmp_path, monkeypatch):
    lane = tmp_path / "lane"
    (lane / "inputs").mkdir(parents=True)
    monkeypatch.setattr(D, "ROOT", tmp_path)
    monkeypatch.setattr(D, "LANE", lane)
    monkeypatch.setattr(D, "MANIFEST", lane / "inputs/deps.json")
    upstream = tmp_path / "keys.py"
    upstream.write_text("cost = 1\n")
    with D.guard(capture=True) as tracker:
        assert upstream.read_text() == "cost = 1\n"
        tracker.finish()
    return upstream


def test_same_size_upstream_change_blocks_before_execution(tmp_path, monkeypatch):
    upstream = fixture_manifest(tmp_path, monkeypatch)
    upstream.write_text("cost = 2\n")
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] pricing dependency: stale keys.py"):
        D.ReadGuard(capture=False)


def test_new_transitive_read_blocks(tmp_path, monkeypatch):
    fixture_manifest(tmp_path, monkeypatch)
    unknown = tmp_path / "new-table.csv"
    unknown.write_text("rate\n1\n")
    with D.guard(capture=False):
        with pytest.raises(SystemExit, match=r"\[BLOCKED\] pricing dependency: new unpinned read"):
            unknown.read_text()


def test_duplicate_manifest_blocks(tmp_path, monkeypatch):
    fixture_manifest(tmp_path, monkeypatch)
    payload = json.loads(D.MANIFEST.read_text())
    payload["files"].append(payload["files"][0])
    D.MANIFEST.write_text(json.dumps(payload))
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] pricing dependency: empty or duplicate"):
        D.validate_manifest()


def test_principal_manifest_contains_actual_key_module():
    payload = json.loads(D.MANIFEST.read_text())
    files = {x["path"] for x in payload["files"]}
    assert "infra/immigration-fiscal/generation_account_2026_09_24/keys.py" in files
    assert "infra/immigration-fiscal/cps_imputation_keys_2026_09_23/common.py" in files


@pytest.mark.parametrize("changed", ["manifest.json", "_cache/pricing.npz"])
def test_same_cost_cache_requires_matching_input_digest(tmp_path, monkeypatch, changed):
    monkeypatch.setattr(C, "LANE", tmp_path)
    manifest = tmp_path / "manifest.json"
    monkeypatch.setattr(C, "MANIFEST", manifest)
    (tmp_path / "_cache").mkdir()
    contents = {"export_pricing.py": b"adapter", "national_keys.py": b"keys",
                "manifest.json": b"inputs", "_cache/pricing.npz": b"prices that close to the same total"}
    for name, data in contents.items():
        (tmp_path / name).write_bytes(data)
    receipt = {"adapter_sha256": hashlib.sha256(contents["export_pricing.py"]).hexdigest(),
               "national_keys_sha256": hashlib.sha256(contents["national_keys.py"]).hexdigest(),
               "dependency_manifest_sha256": hashlib.sha256(contents["manifest.json"]).hexdigest(),
               "pricing_cache_sha256": hashlib.sha256(contents["_cache/pricing.npz"]).hexdigest()}
    C.validate_cache_receipt(receipt)
    (tmp_path / changed).write_bytes(b"changed profiles with unchanged case totals")
    with pytest.raises(SystemExit, match=r"\[BLOCKED\] stale"):
        C.validate_cache_receipt(receipt)
