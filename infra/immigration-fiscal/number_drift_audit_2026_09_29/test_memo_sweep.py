"""The memo sweep's positive controls (memo_sweep.CONTROLS) against the registry on disk.

    uv run --no-project --offline python3 -m pytest infra/immigration-fiscal/number_drift_audit_2026_09_29/ -q
"""
import sys
from pathlib import Path

import pytest

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import memo_sweep as M  # noqa: E402


def test_positive_controls_pass():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    assert M.controls(recs, values, M.other_values(recs, values, registry)) == []


def test_the_adopted_case_is_current_and_the_registry_case_is_earlier():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    assert set(registry) == set(M.ADOPTED)
    assert [round(x, 1) for x in values["case.main"]] == [371.4, 434.8]
    assert [round(x, 1) for x in registry["case.main"]] == [321.8, 387.4]
    assert [round(x, 1) for x in values["pairing.total"]] == [462.9, 535.5]
    assert [round(x, 1) for x in registry["pairing.total"]] == [413.7, 488.0]
    for rid in ("case.main", "pairing.total"):
        others = M.other_values(recs, values, registry)[rid]
        assert any(o["origin"] == "registry" and o["kind"] == "vintage" for o in others)


def test_an_exemption_holds_only_while_its_sentence_stands():
    path, (phrase, reason) = next(iter(M.EXEMPT.items()))
    assert M.exemption(path, f"# A memo\n\n{phrase}\n") == reason
    assert M.exemption("research/immigration-some-memo.md", phrase) is None
    with pytest.raises(SystemExit, match="no longer does"):
        M.exemption(path, "# A memo rewritten to current values\n")
