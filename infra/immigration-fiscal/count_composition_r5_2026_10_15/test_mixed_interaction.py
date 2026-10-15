import importlib.util
from pathlib import Path

import numpy as np


SPEC = importlib.util.spec_from_file_location("count_mixed", Path(__file__).with_name("mixed_interaction.py"))
M = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(M)


def test_signed_generation_allocation_and_no_false_bound():
    pieces = [{"end": end, "generation": gen, "line": "mixed_unit_removal",
               "economic_class": "unclassified_post_engine"}
              for end in ("low", "high") for gen in M.GENERATION_NAMES]
    data = {"weights": np.ones((3, 2)), "added_weights": np.zeros((3, 2)),
            "generation": np.arange(3),
            "base_piece_prices": np.tile(np.diag([-2., 3., 4.]), (2, 1))}
    result = M.mixed_allocation(data, {"denominator_pieces": pieces}, [1., .5, 1.])
    assert result["by_end"]["low"]["declared_per_member_delta_bn"] == -1.5
    assert result["by_end"]["low"]["whole_net_component_allocation_sensitivity_delta_bn"] == [-3., 0.]
    assert result["nonlinear_membership_interaction_measured"] is False
    assert result["sensitivity_is_rigorous_bound"] is False


def test_item10_uses_person_identity_not_household_or_position():
    data = {"person_ph_seq": np.array([10, 10, 20]), "person_pppos": np.array([2, 1, 1])}
    correction = {"meta": {"union_completion": {"observed_records": [
        {"PH_SEQ": 10, "PPPOS": 1, "observed_nonreporter": False},
        {"PH_SEQ": 20, "PPPOS": 1, "observed_nonreporter": True}]}}}
    flags = M.item10_flags(data, correction)
    assert flags["reporter"].tolist() == [False, True, False]
    assert flags["nonreporter"].tolist() == [False, False, True]
