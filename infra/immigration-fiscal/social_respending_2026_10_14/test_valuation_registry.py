"""A partially applied life-year arm must fail the joint valuation contract."""
import pytest
from valuation_registry import mortality_registry


def declarations(basis="dot_uniform", rate=0):
    return {channel:dict(valuation=basis,real_discount_rate=rate)
            for channel in ("crime","pm25","road_crash")}


def test_all_channels_share_basis_and_rate():
    assert mortality_registry("dot_uniform",0,declarations())["uniform_vsl_usd"] == 13_700_000
    assert mortality_registry("dot_life_years",.03,declarations("dot_life_years",.03))["valuation"] == "dot_life_years"


def test_partial_life_year_arm_or_missing_channel_fails():
    d = declarations("dot_life_years",.03)
    d["road_crash"]["valuation"] = "dot_uniform"
    with pytest.raises(ValueError,match="mixed mortality valuation"):
        mortality_registry("dot_life_years",.03,d)
    d = declarations()
    del d["crime"]
    with pytest.raises(ValueError,match="needs crime, PM and crash"):
        mortality_registry("dot_uniform",0,d)


def test_discount_rate_mismatch_fails():
    d = declarations("dot_life_years",0)
    d["crime"]["real_discount_rate"] = .03
    with pytest.raises(ValueError,match="mixed mortality valuation"):
        mortality_registry("dot_life_years",0,d)
