"""Own-key dollar gaps must preserve per-person normalization and typed closure."""
import copy

import pytest

from v9_exports import records


def fixture():
    result = {}
    for group, population, cost, changes in [
        ("indian_origin", 20., 40., {"13": -2., "14": 0., "15": 1., "18": 1., "20": 5., "21": 0.}),
        ("A1_third_plus_nh_white", 100., 100., {"13": -10., "14": 0., "15": 2., "18": 2., "20": 26., "21": 0.}),
    ]:
        parts = [dict(item=item, kind="college_operating" if item == "15" else "own_source",
                      delta_bn=delta, source_line="own", before_bn=0., after_bn=delta)
                 for item, delta in changes.items()]
        parts.append(dict(item="15", kind="college_capital", delta_bn=0., source_line="college",
                          before_bn=1., after_bn=1.))
        row = dict(population=population, cost=cost, v9_items=changes,
                   v9_before_cost_bn=cost-sum(changes.values()), v9_service_parts=parts)
        result["accrual", group, "low"] = (row, {}, None)
    return result


def test_gap_uses_indian_count_and_closes_by_item():
    gap = records(fixture())["indian_minus_white_gap"][0]
    assert gap["white_scale"] == .2
    assert gap["before_bn"] == 19.
    assert gap["after_bn"] == 20.
    assert gap["change_bn"] == 1.
    assert gap["change_by_item_bn"]["13"] == 0.
    assert "unmeasured" in gap["indian_item11"]


def test_changed_typed_college_part_is_rejected():
    data = fixture()
    data["accrual", "indian_origin", "low"][0]["v9_service_parts"][-1]["delta_bn"] = .01
    with pytest.raises(SystemExit, match="typed item15 parts do not close"):
        records(data)


def test_missing_college_capital_is_not_treated_as_zero():
    data = fixture()
    data["accrual", "indian_origin", "low"][0]["v9_service_parts"].pop()
    with pytest.raises(SystemExit, match="operating/capital must be priced jointly"):
        records(data)


def test_gap_change_invariant_to_white_reference_count():
    data = fixture()
    doubled = copy.deepcopy(data)
    white = doubled["accrual", "A1_third_plus_nh_white", "low"][0]
    for key in ("population", "cost", "v9_before_cost_bn"):
        white[key] *= 2
    white["v9_items"] = {key: value * 2 for key, value in white["v9_items"].items()}
    for part in white["v9_service_parts"]:
        for key in ("delta_bn", "before_bn", "after_bn"):
            part[key] *= 2
    assert records(doubled)["indian_minus_white_gap"][0]["change_bn"] == records(data)["indian_minus_white_gap"][0]["change_bn"]
