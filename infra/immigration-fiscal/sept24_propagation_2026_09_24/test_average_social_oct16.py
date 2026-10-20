"""Conservation, native input and cash-timing checks for the F09 comparator."""
import importlib.util
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


def load():
    spec = importlib.util.spec_from_file_location("average_social_test", HERE / "average_social_oct16.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_component_bridge_requires_every_source_and_closes_both_signs():
    m = load()
    absolute = [dict(item="harm", total_by_end_bn=dict(low=20., high=30.)),
                dict(item="benefit", total_by_end_bn=dict(low=-10., high=-5.))]
    average = dict(harm=dict(low=12., high=22.), benefit=dict(low=-12., high=-11.))
    result = m.component_bridge(absolute, average, dict(low=100., high=200.), dict(low=-10., high=20.))
    assert result["ends"]["low"] == dict(absolute_bn=110., equal_count_average_bn=-10., joint_social_excess_vs_average_bn=120.)
    assert result["ends"]["high"] == dict(absolute_bn=225., equal_count_average_bn=31., joint_social_excess_vs_average_bn=194.)
    del average["benefit"]
    with pytest.raises(ValueError, match="source component mismatch"):
        m.component_bridge(absolute, average, dict(low=100., high=200.), dict(low=-10., high=20.))


def test_cash_timing_mismatch_stops_before_native_sources(monkeypatch):
    m = load()
    states = {b: {e: dict(current_H_bn=10., government_consumption_removed_bn=2.,
                         government_consumption_national_bn=100., highway_response=.7, fiscal_cost_bn=20.)
                  for e in m.ENDS} for b in ("set", "cash")}
    states["set"]["low"]["current_H_bn"] = 11.
    monkeypatch.setattr(m, "average_components", lambda *a, **kw: pytest.fail("native sources must not run"))
    with pytest.raises(ValueError, match="social timing differs"):
        m.build_average_social([], states, absolute_fiscal_by_basis={}, population_people=10., national_people=100.)


def test_average_crime_is_national_incidence_and_own_random_receivers():
    m = load()
    source = m.Sources(m.FISCAL)
    first = m.crime_sources(source, .1)
    second = m.crime_sources(source, .2)
    # Same national source risks and active DOT prices, different removed and
    # retained populations. A linear scaling of Mexican social dollars fails.
    assert second["victims"]["low"] / first["victims"]["low"] == pytest.approx(.2 * .8 / (.1 * .9))
    assert second["victims"]["low"] == second["victims"]["high"]
    assert first["school_disruption"] == dict(low=0., high=0.)
    assert any("mortality_detail" in p for p in source.pins)


def test_average_housing_uses_own_share_in_both_native_geographies():
    m = load()
    result = m.housing_source(m.Sources(m.FISCAL), .13)
    # Random membership is uniform in every area, so the native local and
    # national paths coincide. Keeping the native Mexican TARGET breaks this.
    assert result["low"] == pytest.approx(result["high"], abs=1e-12)
