"""Phase-A diagnostics respect the system temp root and protect lane outputs."""
import sys
from pathlib import Path
import tempfile

import pytest

import p8_phase_a as phase


def test_phase_a_accepts_system_temporary_directory(tmp_path, monkeypatch):
    destination = tmp_path / "measurements"
    calls = []
    monkeypatch.setattr(sys, "argv", ["p8_phase_a.py", "--out-dir", str(destination)])
    monkeypatch.setattr(phase, "measure", lambda output, baseline: calls.append((output, baseline)))
    phase.main()
    assert destination.is_dir()
    assert calls == [(destination.resolve(), False)]


def test_phase_a_rejects_lane_derived_even_inside_temp_root(tmp_path, monkeypatch):
    lane = tmp_path / "lane"
    destination = lane / "derived" / "measurements"
    monkeypatch.setattr(phase, "HERE", lane)
    monkeypatch.setattr(sys, "argv", ["p8_phase_a.py", "--out-dir", str(destination)])
    with pytest.raises(SystemExit, match="BLOCKED.*system temporary directory"):
        phase.main()
    assert not destination.exists()


def test_phase_a_preserves_standard_temp_alias_outputs(monkeypatch):
    with tempfile.TemporaryDirectory(prefix="phase-a-alias-", dir="/tmp") as directory:
        destination = Path(directory) / "measurements"
        calls = []
        monkeypatch.setattr(sys, "argv", ["p8_phase_a.py", "--out-dir", str(destination)])
        monkeypatch.setattr(phase, "measure", lambda output, baseline: calls.append(output))
        phase.main()
        assert calls == [destination.resolve()]
