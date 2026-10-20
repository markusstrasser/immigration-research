"""Adoption is the live declaration AND the package's adopted status."""
import json
from pathlib import Path
import subprocess

import pytest

GATE = Path(__file__).resolve().parents[1] / "infra/immigration-fiscal/scripts/adoption_gate.cjs"


@pytest.mark.parametrize("key,status,expected", [("oct15", "adopted", False),
                                                 ("oct16", "candidate", False),
                                                 ("oct16", "adopted", True)])
def test_live_key_and_package_status(tmp_path, key, status, expected):
    declaration = dict(key=key, lane="case", adopted="2026-10-20", decision="decision.md")
    (tmp_path / "live_case.json").write_text(json.dumps(declaration))
    (tmp_path / "case").mkdir()
    (tmp_path / "case/package.cjs").write_text("module.exports={V9:" + json.dumps(
        dict(STATUS=status, CASE_KEY="oct16", LANE="case", ADOPTED="2026-10-20", DECISION="decision.md")) + "};\n")
    result = subprocess.run(["node", str(GATE), "oct16", str(tmp_path / "live_case.json")],
                            capture_output=True, text=True)
    assert (result.returncode == 0) == expected, result.stderr
    if expected:
        assert json.loads(result.stdout) == dict(key="oct16", adopted="2026-10-20", decision="decision.md")
    else:
        assert "[BLOCKED]" in result.stderr


@pytest.mark.parametrize("case_key,lane", [("oct15", "case"), ("oct16", "wrong_lane")])
def test_wrong_package_identity_is_rejected(tmp_path, case_key, lane):
    declaration = dict(key="oct16", lane="case", adopted="2026-10-20", decision="decision.md")
    (tmp_path / "live_case.json").write_text(json.dumps(declaration))
    (tmp_path / "case").mkdir()
    (tmp_path / "case/package.cjs").write_text("module.exports={V9:" + json.dumps(
        dict(STATUS="adopted", CASE_KEY=case_key, LANE=lane, ADOPTED="2026-10-20", DECISION="decision.md")) + "};\n")
    result = subprocess.run(["node", str(GATE), "oct16", str(tmp_path / "live_case.json")],
                            capture_output=True, text=True)
    assert result.returncode != 0 and "case/lane identity" in result.stderr
