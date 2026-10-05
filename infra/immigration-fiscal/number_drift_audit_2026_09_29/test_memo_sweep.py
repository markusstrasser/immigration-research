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
    assert M.controls(recs, values, M.other_values(recs, values, registry, M.earlier_values())) == []


def test_the_registry_carries_v5_and_the_september_27_and_29_values_are_earlier():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    earlier = M.earlier_values()
    # the evidence map moved to v5 on 2026-10-06, so no record needs the adopted-lane bridge
    assert M.ADOPTED == {} and registry == {}
    assert [round(x, 1) for x in values["case.main"]] == [390.3, 461.2]
    assert [round(x, 2) for x in values["case.per_member"]] == [9.13, 10.79]
    assert [round(x, 1) for x in earlier["case.main"][0]] == [371.4, 434.8]
    assert [round(x, 2) for x in earlier["case.per_member"][0]] == [9.35, 10.95]
    # the pairing is the propagation lane's v5 run; its September 29 run is the earlier vintage
    assert [round(x, 1) for x in values["pairing.total"]] == [490.2, 570.7]
    assert [round(x, 2) for x in values["pairing.per_member_priced"]] == [11.47, 13.35]
    assert [round(x, 1) for x in values["pairing.fiscal_footing"]] == [385.4, 461.2]
    assert [round(x, 1) for x in earlier["pairing.total"][0]] == [462.9, 535.5]
    assert [round(x, 2) for x in earlier["pairing.per_member_priced"][0]] == [11.66, 13.48]
    assert [round(x, 1) for x in earlier["pairing.fiscal_footing"][0]] == [366.7, 434.8]
    others = M.other_values(recs, values, registry, earlier)
    # the September 27 case and pairing reach the sweep through `supersedes`, by record id
    for rid, ref, want in (("case.main", "case.sept27", [321.8, 387.4]),
                           ("pairing.total", "pairing.total_sept27", [413.7, 488.0])):
        hits = [o for o in others[rid] if o["origin"] == "referenced" and o["source"].startswith(ref + ":")]
        assert hits and all(o["kind"] == "vintage" for o in hits)
        assert [round(x, 1) for x in values[ref]] == want
    for rid in ("case.main", "case.per_member", "pairing.total", "pairing.per_member_priced", "pairing.fiscal_footing"):
        assert any(o["origin"] == "earlier" and o["kind"] == "vintage" for o in others[rid])


def test_an_exemption_holds_only_while_its_sentence_stands():
    path, (phrase, reason) = next(iter(M.EXEMPT.items()))
    assert M.exemption(path, f"# A memo\n\n{phrase}\n") == reason
    assert M.exemption("research/immigration-some-memo.md", phrase) is None
    with pytest.raises(SystemExit, match="no longer does"):
        M.exemption(path, "# A memo rewritten to current values\n")
