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


def test_v9_is_current_in_the_registry_and_earlier_cases_retained():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    earlier = M.earlier_values()
    assert M.ADOPTED == {} and registry == {}
    assert [round(x, 1) for x in values["case.main"]] == [368.0, 436.6]
    assert [round(x, 2) for x in values["case.per_member"]] == [8.20, 9.72]
    assert [round(x, 1) for x in values["case.cash_set"]] == [284.4, 352.9]
    # Every replaced case is retained, newest first, including v6, the evidence map's case until 2026-10-21.
    assert [label for _v, label in earlier["case.main"]] == ["the October 15 case (v8)",
                                                          "the October 14 case (v7)", "the October 7 case (v6)",
                                                          "the October 5 case (v5)", "the September 29 case (v4)"]
    assert _rounded(earlier["case.main"], 1) == [[365.8, 456.0], [339.6, 423.6], [389.1, 461.5], [390.3, 461.2], [371.4, 434.8]]
    assert _rounded(earlier["case.per_member"], 2) == [[8.09, 10.08], [7.94, 9.91], [9.10, 10.79], [9.13, 10.79], [9.35, 10.95]]
    assert _rounded(earlier["case.cash_set"], 1) == [[281.8, 371.9], [264.4, 348.5], [307.4, 385.4], [307.4, 383.4], [294.7, 361.8]]
    # v9 publishes the aggregate pairing, whose per-member value uses v9's own lineage count.
    assert [round(x, 1) for x in values["pairing.total"]] == [483.1, 557.3]
    assert [round(x, 2) for x in values["pairing.per_member_priced"]] == [10.76, 12.41]
    assert [round(x, 1) for x in values["pairing.fiscal_footing"]] == [368.0, 436.6]
    assert _rounded(earlier["pairing.total"], 1) == [[477.7, 573.4], [440.1, 537.5], [489.0, 570.7], [490.2, 570.7], [462.9, 535.5]]
    assert _rounded(earlier["pairing.per_member_priced"], 2) == [[10.56, 12.68], [10.29, 12.57], [11.44, 13.35], [11.47, 13.35], [11.66, 13.48]]
    assert _rounded(earlier["pairing.fiscal_footing"], 1) == [[365.8, 456.0], [334.8, 423.6], [384.3, 461.5], [385.4, 461.2], [366.7, 434.8]]
    others = M.other_values(recs, values, registry, earlier)
    # the September 27 case and pairing reach the sweep through `supersedes`, by record id
    for rid, ref, want in (("case.main", "case.sept27", [321.8, 387.4]),
                           ("pairing.total", "pairing.total_sept27", [413.7, 488.0])):
        hits = [o for o in others[rid] if o["origin"] == "referenced" and o["source"].startswith(ref + ":")]
        assert hits and all(o["kind"] == "vintage" for o in hits)
        assert [round(x, 1) for x in values[ref]] == want
    for rid in M.EARLIER:
        assert not any(o["origin"] == "registry" for o in others[rid])
        assert [o["kind"] for o in others[rid] if o["origin"] == "earlier"] == ["vintage"] * 5


def test_an_exemption_holds_only_while_its_sentence_stands():
    path, (phrase, reason) = next(iter(M.EXEMPT.items()))
    assert M.exemption(path, f"# A memo\n\n{phrase}\n") == reason
    assert M.exemption("research/immigration-some-memo.md", phrase) is None
    with pytest.raises(SystemExit, match="no longer does"):
        M.exemption(path, "# A memo rewritten to current values\n")


def test_an_allowance_passes_only_its_own_sentence_and_lapses_with_it():
    recs = M.Q.load_registry()
    values, registry = M.current_values(recs)
    others = M.other_values(recs, values, registry, M.earlier_values())
    key, reason = next((k, v) for k, v in M.ALLOW.items() if k[1] == "case.per_member")
    path, rid, quoted, phrase = key

    def classes(memo, text):
        return {r["class"] for r in M.sweep_text(memo, text, recs, values, others)
                if r["record"] == rid and r["quoted"] == quoted}
    own = f"The main case has a separate {quoted} {phrase}."
    other = f"The main case is {quoted} per member."
    [allowed] = classes(path, own)
    assert allowed.endswith("_allowed")
    assert [r["label"] for r in M.sweep_text(path, own, recs, values, others)
            if r["record"] == rid and r["quoted"] == quoted] == [f"allowed: {reason}"]
    # the same number in another sentence, or the same sentence in another memo, is still flagged
    assert classes(path, other) == {allowed.replace("_allowed", "_unlabelled")}
    assert classes("research/immigration-other.md", own) == {allowed.replace("_allowed", "_unlabelled")}
    # an allowance lapses once its memo loses the phrase or the number; a line break inside the phrase still holds
    # (the other entries' memos are not in these docs, so only this entry's verdict is read)
    def lapsed(docs):
        return [k for k in M.lapsed_allowances(docs) if k == key]
    assert lapsed([(path, own.replace(phrase, phrase.replace(" ", "\n", 1)))]) == []
    assert lapsed([(path, other)]) == [key]
    assert lapsed([(path, own.replace(quoted, "24.3%"))]) == [key]
    assert lapsed([]) == [key]
