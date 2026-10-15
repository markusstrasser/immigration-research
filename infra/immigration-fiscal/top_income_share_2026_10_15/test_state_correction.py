"""Accounting and source-schema guards for the covered-state sensitivity."""
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
SPEC = importlib.util.spec_from_file_location("state_correction", HERE / "state_correction.py")
S = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(S)


def fixture_rows():
    rows = []
    for sample in ("baseline_2025_nominal", "pooled_real2023"):
        for state in (6, 36):
            for b in range(14):
                share = .1 if state == 6 else .02
                if sample == "pooled_real2023" and state == 6 and b == 13:
                    share = .2
                rows.append(dict(sample=sample, state=state, bin14=b,
                                 total_state=100, union_state=100 * share))
    return rows


def test_admin_shape_separated_from_top_share_and_other_states_fixed():
    result = S.calculate(fixture_rows(), [1] * 7, .06)
    assert result["baseline_share"] == pytest.approx(.06)
    assert result["CA_national_mass"] == .5
    assert result["other_states_union_contribution_held_fixed"] == pytest.approx(.01)
    assert result["arms"]["current"]["share_change"] == 0
    assert result["arms"]["current_CA_admin"]["share_change"] == pytest.approx(0)
    # An increase of .1 in one of seven equally sized CA administrative bins
    # affects only one half of the national mass: .1 / 7 / 2.
    assert result["arms"]["pooled_top_only"]["share_change"] == pytest.approx(.1 / 14)
    assert result["arms"]["carry_500k"]["share_change"] == pytest.approx(0)


def test_monotone_fit_pools_upturn_and_preserves_weighted_share():
    fitted = S.nonincreasing([.07, .03, .06], [2, 1, 3])
    assert fitted == pytest.approx([.07, .0525, .0525])
    assert sum(v * w for v, w in zip(fitted, [2, 1, 3])) == pytest.approx(.35)


def test_missing_support_and_wrong_baseline_fail_loud():
    rows = fixture_rows()
    with pytest.raises(ValueError, match="parity"):
        S.calculate(rows, [1] * 7, .05)
    with pytest.raises(ValueError, match="missing CA bins"):
        S.state_arrays(rows[:-15], "pooled_real2023")
    with pytest.raises(ValueError, match="duplicate CA bins"):
        S.state_arrays(rows + [rows[0]], "baseline_2025_nominal")
    with pytest.raises(ValueError, match="unsupported"):
        S.state_arrays([{**r, "total_state": 0, "union_state": 0} for r in rows], "pooled_real2023")


def test_pinned_administrative_source_and_rounded_total():
    if not S.SOURCE_PATH.exists():
        pytest.skip("pinned FTB source not acquired")
    amounts, extract = S.source_table(S.SOURCE_PATH)
    assert amounts == [40, 1126, 6272, 15956, 26145, 14950, 32594]
    assert sum(amounts) == 97083
    assert len(extract) == 10
    assert extract[-1]["liability_million"] == 97083
