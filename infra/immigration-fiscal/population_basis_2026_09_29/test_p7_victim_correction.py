import pytest

import p7_victim_correction as correction


def test_correction_preserves_low_and_corrects_high_with_declared_contract():
    rows = correction.correction_rows()
    legacy = rows[rows.vsl_standard.eq("legacy")].set_index("end")
    assert legacy.loc["low", "delta_row4_bn"] == pytest.approx(0, abs=1e-6)
    assert legacy.loc["high", "delta_row4_bn"] > 2
    assert set(rows.comparator) == {"with_without"}
    assert set(rows.measure) == {"absolute"}
    assert rows.overlap_set.notna().all()
