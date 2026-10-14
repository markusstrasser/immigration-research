"""A failed medical gate must leave the previous published result intact."""
import pytest
import medicaid_check as M


def test_failed_gate_cannot_overwrite_live_result(monkeypatch, tmp_path):
    derived = tmp_path / "derived"
    derived.mkdir()
    result = derived / "medicaid_check_oct15.csv"
    result.write_bytes(b"verified previous result\n")
    monkeypatch.setattr(M.F, "HERE", tmp_path)
    monkeypatch.setattr(M, "FAILS", ["forced scientific gate failure"])
    with pytest.raises(SystemExit, match="1 gate.*failed"):
        M.publish_rows([dict(value="unverified")], result.name)
    assert result.read_bytes() == b"verified previous result\n"
