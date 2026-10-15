"""Deterministic completion/coverage contract; no lane or git writes."""
import copy

import numpy as np
import pandas as pd
import pytest

import population_basis as P


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit("[BLOCKED] " + name)


def sample():
    d = pd.DataFrame(dict(
        PH_SEQ=[1, 2, 3, 4, 5, 6], PPPOS=[1] * 6,
        target=[True, True, True, False, False, False],
        civ=[True] * 6, other_base=[False, False, False, True, True, True],
        other=[False, False, False, False, False, True],
        pwwgt0=[10., 20., 25., 4., 6., 50.], pw=[10., 20., 30., 4., 6., 50.],
        pw_row4=[10., 20., 25., 4., 6., 50.],
        A_AGE=[40, 20, 30, 30, 5, 30], PRCITSHP=[4, 1, 1, 1, 1, 1],
        PENATVTY=[303, 57, 57, 57, 57, 57],
        PEFNTVTY=[303, 303, 57, 400, 57, 57], PEMNTVTY=[303, 57, 57, 57, 57, 57],
        PEARNVAL=[100., 200., 300., 400., 0., 500.]))
    records = [dict(PH_SEQ=4, PPPOS=1, age=30, people=4., generation="G3plus"),
               dict(PH_SEQ=5, PPPOS=1, age=5, people=6., generation="G3plus")]
    payload = dict(meta=dict(
        population_v8=dict(without_coverage=70., with_coverage=76., coverage=6.),
        union_completion=dict(observed_records=records, counts=dict(total=10.)),
        coverage=dict(counts_by_generation=dict(G1=1., G2=2., G3plus=3.))))
    return d, payload


def test_completion_at_own_records_and_coverage_only_in_denominator():
    d, payload = sample()
    before = d.copy(deep=True)
    out = P.completed_frame(d, payload, gate)
    pd.testing.assert_frame_equal(d, before)
    np.testing.assert_array_equal(out.pw, before.pw)
    np.testing.assert_array_equal(out.pw_row4, before.pw_row4)
    np.testing.assert_array_equal(out.other, [False, False, False, False, False, True])
    assert out.target.sum() == 5
    assert len(out) == len(before)
    assert (out.PEARNVAL * out.pw)[out.target].sum() == 15600.
    info = out.attrs["population_oct15"]
    assert info["located_persons"] == {"G1": 10., "G2": 20., "G3+": 40.}
    assert info["unlocated_coverage_persons"] == {"G1": 1., "G2": 2., "G3+": 3.}
    assert info["complete_denominator_persons"] == {"G1": 11., "G2": 22., "G3+": 43.}
    assert info["located_total"] == 70.
    assert info["complete_total"] == 76.
    assert not info["coverage_in_economic_record_weights"]


def test_current_loader_other_exclusion_and_old_complement_agree():
    d, payload = sample()
    out_current = P.completed_frame(d, payload, gate)
    d["other"] = d.other_base
    out_old = P.completed_frame(d, payload, gate)
    pd.testing.assert_frame_equal(out_current, out_old)


def test_frozen_rounding_changes_no_economic_record():
    d, payload = sample()
    payload["meta"]["population_v8"]["without_coverage"] += .00003
    payload["meta"]["population_v8"]["with_coverage"] += .00003
    out = P.completed_frame(d, payload, gate)
    np.testing.assert_array_equal(out.pw, d.pw)
    info = out.attrs["population_oct15"]
    assert info["source_rounding"]["people"] == pytest.approx(.00003)
    assert info["complete_denominator_persons"]["G1"] == pytest.approx(11.00003)


@pytest.mark.parametrize("defect,expected", [
    ("duplicate_source", "unique_person_ids"),
    ("missing_source", "all_records_located"),
    ("overlap_original", "outside_original_union"),
    ("bad_weight", "own_source_weights"),
    ("bad_age", "own_ages"),
    ("bad_generation", "own_generation"),
    ("negative_coverage", "coverage_counts_nonnegative_finite"),
    ("wrong_coverage", "coverage_counts_close"),
    ("wrong_located", "located_count_is_case_without_coverage"),
    ("wrong_complete", "full_denominators_close"),
    ("wrong_original_other", "original_other_is_frozen_complement"),
    ("duplicate_frame", "frame_has_unique_person_ids"),
])
def test_invalid_contracts_fail_loudly(defect, expected):
    d, payload = sample()
    meta = payload["meta"]
    records = meta["union_completion"]["observed_records"]
    if defect == "duplicate_source":
        records.append(copy.deepcopy(records[0]))
    elif defect == "missing_source":
        records[0]["PH_SEQ"] = 99
    elif defect == "overlap_original":
        records[0]["PH_SEQ"] = 1
    elif defect == "bad_weight":
        records[0]["people"] = 5.
    elif defect == "bad_age":
        records[0]["age"] = 31
    elif defect == "bad_generation":
        records[0]["generation"] = "G2"
    elif defect == "negative_coverage":
        meta["coverage"]["counts_by_generation"]["G1"] = -1.
    elif defect == "wrong_coverage":
        meta["population_v8"]["coverage"] = 8.
    elif defect == "wrong_located":
        meta["population_v8"]["without_coverage"] = 71.
    elif defect == "wrong_complete":
        meta["population_v8"]["with_coverage"] = 80.
    elif defect == "wrong_original_other":
        d.loc[0, "other_base"] = True
    elif defect == "duplicate_frame":
        d.loc[5, "PH_SEQ"] = 4
    with pytest.raises(SystemExit, match=expected):
        P.completed_frame(d, payload, gate)
