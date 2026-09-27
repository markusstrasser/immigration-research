import importlib.util
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

spec = importlib.util.spec_from_file_location('medical_validation', Path(__file__).with_name('analysis.py'))
a = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = a
spec.loader.exec_module(a)


def test_tail_mean_is_not_winsorization_and_preserves_unweighted_sum():
    y = np.arange(1000, dtype=float)
    y[-1] = 10000
    out, count = a.tail_mean(y, np.ones(1000, bool), .99)
    assert count == 10
    assert out.sum() == pytest.approx(y.sum())
    assert np.max(out) > np.quantile(y, .99)
    assert np.array_equal(out[:980], y[:980])


def test_tail_mean_does_not_touch_people_outside_eligible_population():
    y = np.arange(1000, dtype=float)
    eligible = np.arange(1000) < 500
    out, _ = a.tail_mean(y, eligible)
    assert np.array_equal(out[500:], y[500:])


def brr_survey():
    d = pd.DataFrame({'weight': [1., 2., 3., 4.]})
    return a.Survey(pd.concat([d, pd.DataFrame({f'CSPUF{i:03}': [1+i/1000, 2., 3., 4.]
                                               for i in range(1, 101)})], axis=1), 'mcbs', None)


def test_brr_ratio_computed_inside_replicates_and_identity_variance_zero():
    s = brr_survey()
    first = s.mean(np.array([1, 2, 4, 9]), np.ones(4, bool))
    second = s.mean(np.array([3, 4, 5, 6]), np.ones(4, bool))
    r = s.ratio(first, second)
    np.testing.assert_allclose(r.vector, first.vector / second.vector)
    assert s.se(s.combine([(1, first), (-1, first)])) == 0
    assert s.se(s.ratio(first, first)) == 0


def test_empty_domains_and_zero_denominators_fail_loud():
    s = brr_survey()
    with pytest.raises(ValueError, match='BLOCKED'):
        s.mean(np.ones(4), np.zeros(4, bool))
    with pytest.raises(ValueError, match='BLOCKED'):
        s.ratio(a.Stat(1, np.ones(101)), a.Stat(0, np.zeros(101)))


@pytest.mark.parametrize('filename', list(a.ACQUISITION.FILES))
def test_analysis_uses_authoritative_acquisition_pin_after_drift(monkeypatch, filename):
    inputs = {str(a.LANE / '_cache' / name): expected
              for name, (_, expected) in a.ACQUISITION.FILES.items()}
    a.verify_mcbs_2022_pins(inputs)
    url, expected = a.ACQUISITION.FILES[filename]
    changed = 'changed-' + expected
    monkeypatch.setitem(a.ACQUISITION.FILES, filename, (url, changed))
    with pytest.raises(ValueError, match='2022 MCBS pin mismatch'):
        a.verify_mcbs_2022_pins(inputs)
    inputs[str(a.LANE / '_cache' / filename)] = changed
    a.verify_mcbs_2022_pins(inputs)
