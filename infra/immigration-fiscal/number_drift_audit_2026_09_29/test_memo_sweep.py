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


def _rounded(cases, places):
    return [[round(x, places) for x in v] for v, _label in cases]


def test_v6_is_current_and_the_october_5_and_september_27_and_29_values_are_earlier():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    earlier = M.earlier_values()
    # main case v6 is current for the memos while the evidence map and its registry stay on v5
    assert set(registry) == set(M.ADOPTED)
    assert [round(x, 1) for x in values["case.main"]] == [389.1, 461.5]
    assert [round(x, 2) for x in values["case.per_member"]] == [9.10, 10.79]
    assert [round(x, 1) for x in values["case.cash_set"]] == [307.4, 385.4]
    assert [round(x, 1) for x in registry["case.main"]] == [390.3, 461.2]
    assert [round(x, 2) for x in registry["case.per_member"]] == [9.13, 10.79]
    # the earlier cases, newest first: the October 5 case (v5), then the September 29 case (v4)
    assert [label for _v, label in earlier["case.main"]] == ["the October 5 case (v5)", "the September 29 case (v4)"]
    assert _rounded(earlier["case.main"], 1) == [[390.3, 461.2], [371.4, 434.8]]
    assert _rounded(earlier["case.per_member"], 2) == [[9.13, 10.79], [9.35, 10.95]]
    assert _rounded(earlier["case.cash_set"], 1) == [[307.4, 383.4], [294.7, 361.8]]
    # the pairing is the propagation lane's v6 run; its v5 and September 29 runs are the earlier vintages
    assert [round(x, 1) for x in values["pairing.total"]] == [489.0, 570.7]
    assert [round(x, 2) for x in values["pairing.per_member_priced"]] == [11.44, 13.35]
    assert [round(x, 1) for x in values["pairing.fiscal_footing"]] == [384.3, 461.5]
    assert [round(x, 1) for x in registry["pairing.total"]] == [490.2, 570.7]
    assert _rounded(earlier["pairing.total"], 1) == [[490.2, 570.7], [462.9, 535.5]]
    assert _rounded(earlier["pairing.per_member_priced"], 2) == [[11.47, 13.35], [11.66, 13.48]]
    assert _rounded(earlier["pairing.fiscal_footing"], 1) == [[385.4, 461.2], [366.7, 434.8]]
    others = M.other_values(recs, values, registry, earlier)
    # the September 27 case and pairing reach the sweep through `supersedes`, by record id
    for rid, ref, want in (("case.main", "case.sept27", [321.8, 387.4]),
                           ("pairing.total", "pairing.total_sept27", [413.7, 488.0])):
        hits = [o for o in others[rid] if o["origin"] == "referenced" and o["source"].startswith(ref + ":")]
        assert hits and all(o["kind"] == "vintage" for o in hits)
        assert [round(x, 1) for x in values[ref]] == want
    for rid in M.ADOPTED:
        assert any(o["origin"] == "registry" and o["kind"] == "vintage" for o in others[rid])
        assert [o["kind"] for o in others[rid] if o["origin"] == "earlier"] == ["vintage", "vintage"]


def test_an_exemption_holds_only_while_its_sentence_stands():
    path, (phrase, reason) = next(iter(M.EXEMPT.items()))
    assert M.exemption(path, f"# A memo\n\n{phrase}\n") == reason
    assert M.exemption("research/immigration-some-memo.md", phrase) is None
    with pytest.raises(SystemExit, match="no longer does"):
        M.exemption(path, "# A memo rewritten to current values\n")
