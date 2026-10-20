"""Identity and joint-count negative controls for the v9 group consumer."""
import numpy as np
import pandas as pd
import pytest

import p9_calibration
from p8_group_frame import coverage_components


def source_frame():
    return pd.DataFrame({"PH_SEQ": [10, 20, 30], "PPPOS": [1, 1, 2],
                         "central_member_factor": [.6, 1.3, 1.]})


def test_calibration_joins_identity_in_caller_order(monkeypatch):
    source = source_frame()
    monkeypatch.setattr(p9_calibration.pd, "read_parquet", lambda *a, **k: source)
    caller = source.loc[[2, 0], ["PH_SEQ", "PPPOS"]]
    np.testing.assert_array_equal(p9_calibration.observed_factors(caller), [1., .6])


@pytest.mark.parametrize("side", ["source", "caller"])
@pytest.mark.parametrize("defect", ["duplicate", "null"])
def test_calibration_rejects_ambiguous_identity(monkeypatch, side, defect):
    source = source_frame()
    caller = source[["PH_SEQ", "PPPOS"]].copy()
    frame = source if side == "source" else caller
    if defect == "duplicate":
        frame.loc[1, ["PH_SEQ", "PPPOS"]] = frame.loc[0, ["PH_SEQ", "PPPOS"]]
    else:
        frame.loc[0, "PH_SEQ"] = np.nan
    monkeypatch.setattr(p9_calibration.pd, "read_parquet", lambda *a, **k: source)
    with pytest.raises(ValueError, match=f"{defect} calibration person identity"):
        p9_calibration.observed_factors(caller)


@pytest.mark.parametrize("factor", [np.nan, np.inf, -0.1])
def test_calibration_rejects_invalid_factor(monkeypatch, factor):
    source = source_frame()
    source.loc[1, "central_member_factor"] = factor
    monkeypatch.setattr(p9_calibration.pd, "read_parquet", lambda *a, **k: source)
    with pytest.raises(ValueError, match="missing or invalid source calibration factor"):
        p9_calibration.observed_factors(source[["PH_SEQ", "PPPOS"]])


def test_calibration_rejects_missing_identity(monkeypatch):
    source = source_frame()
    caller = source[["PH_SEQ", "PPPOS"]].copy()
    caller.loc[1, "PPPOS"] = 9
    monkeypatch.setattr(p9_calibration.pd, "read_parquet", lambda *a, **k: source)
    with pytest.raises(ValueError, match="missing or invalid source calibration factor"):
        p9_calibration.observed_factors(caller)


def coverage_fixture(tmp_path):
    # item16 includes an observed-person change that must never be attributed
    # to missing people. item17 is conditional joint-minus16, not standalone17.
    rows = [dict(scenario=s, end=end, generation=g, change_bn=total,
                 coverage_change_bn=covered)
            for end in ("low", "high")
            for s, total, covered in (("item16", -5., -1.), ("joint", -2., 2.), ("item17", 100., 100.))
            for g in ("G1", "G2", "G3plus")]
    path = tmp_path / "parts.csv"
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator="\n")
    counts = {g: 10. for g in ("G1", "G2", "G3plus")}
    ends = {end: dict(total_bn=12., by_generation={g: 4. for g in counts}) for end in ("low", "high")}
    metadata = {"coverage": dict(counts_by_generation=counts, by_end=ends)}
    for name, scenario, per_group, delta in (("native_minor_calibration", "item16", -5., -1.),
                                            ("coverage_tenure", "joint", 3., 0.)):
        metadata[name] = dict(parts_file=str(path), parts_scenario=scenario,
            coverage_people_change_by_generation={g: delta for g in counts},
            by_end={end: dict(total_bn=3 * per_group, by_generation_bn={g: per_group for g in counts})
                    for end in ends})
    metadata["coverage_tenure"]["subtract_parts_scenario"] = "item16"
    return metadata


def gate(name, ok, **detail):
    if not ok:
        raise ValueError(name)


def test_coverage_dollars_and_people_apply_joint_parts_once(tmp_path):
    metadata = coverage_fixture(tmp_path)
    counts, costs, totals = coverage_components(metadata, "oct16", gate)
    assert counts == dict.fromkeys(("G1", "G2", "G3plus"), 9.)
    assert costs == {end: dict.fromkeys(counts, 6.) for end in ("low", "high")}
    assert totals == {"low": 18., "high": 18.}
    assert metadata["coverage"]["by_end"]["low"]["total_bn"] == 12.
    assert metadata["coverage"]["counts_by_generation"]["G1"] == 10.


def test_coverage_standalone17_cannot_replace_conditional_joint(tmp_path):
    metadata = coverage_fixture(tmp_path)
    metadata["coverage_tenure"]["parts_scenario"] = "item17"
    with pytest.raises(ValueError, match="coverage_tenure_source_closure_low"):
        coverage_components(metadata, "oct16", gate)


def test_coverage_generation_assignment_must_match_source(tmp_path):
    metadata = coverage_fixture(tmp_path)
    meta = metadata["native_minor_calibration"]["by_end"]["low"]["by_generation_bn"]
    meta["G1"] -= 1.
    meta["G2"] += 1.
    with pytest.raises(ValueError, match="source_generation_low_G1"):
        coverage_components(metadata, "oct16", gate)


def test_generation_cost_closure_does_not_hide_stale_population():
    from test_p8_group_frame import fixture_model
    from p8_group_frame import build_group_frame
    model = fixture_model()
    model.payload["meta"]["population_v8"]["with_coverage"] += 1.
    with pytest.raises(ValueError, match="generation_population_closure"):
        build_group_frame(model)
