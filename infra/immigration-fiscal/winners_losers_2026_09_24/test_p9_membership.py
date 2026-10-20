"""Calibration changes observed payers, preserving latent state/age placement."""
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import p8_membership as membership
import winners_losers as wl


def fixture(monkeypatch):
    monkeypatch.setattr(wl, 'CASE', dict(lane='fixture'))
    d = pd.DataFrame(dict(A_AGE=25, st=[6, 48, 6, 48, 6], PRCITSHP=1,
        PEMNTVTY=57, PEFNTVTY=[57, 57, 57, 57, 100], PRDTHSP=[1, 1, 0, 0, 1],
        target=[True, True, False, False, True], other=[False, False, True, True, False],
        target_oct14=[True, True, False, False, False], other_oct14=[False, False, True, True, True],
        completion_member=[False, False, False, False, True],
        pw_production=[10., 10., 100., 100., 10.]))
    weights = np.array([5., 15., 100., 100., 8.])
    lineage = dict(counts=dict(added=4., at_g3_rate=4., later_losses=0.),
        age_mix=dict(bands=['0-4', '5+'], reading='fixture', route='fixture',
                     mixes=dict(g3_rate=[0., 1.], later=[0., 1.], identified=[0., 1.])))
    namespace = SimpleNamespace(CASE=dict(case='oct16'), US_AREAS=[57], age_band_factors=wl.age_band_factors)
    return d, weights, lineage, namespace


def test_calibrated_payers_keep_raw_latent_donor_state_shape(monkeypatch):
    d, weights, lineage, namespace = fixture(monkeypatch)
    out, cells, audit = membership.payer_weights(d, weights, lineage, namespace)
    # Calibration changes observed donor weights to5/15, but the original latent
    #4people stay2/2 by state, matching the complete group proxy, not1/3.
    np.testing.assert_array_equal(out, [5., 15., 98., 98., 0.])
    assert cells.removed.tolist() == pytest.approx([2., 2.])
    assert audit['removed_completion_people'] == 8.
    assert audit['coverage_payer_people'] == 0.
    np.testing.assert_array_equal(weights, [5., 15., 100., 100., 8.])


def test_current_payer_route_requires_raw_donor_weights(monkeypatch):
    d, weights, lineage, namespace = fixture(monkeypatch)
    with pytest.raises(ValueError, match='raw latent donor weights missing'):
        membership.payer_weights(d.drop(columns='pw_production'), weights, lineage, namespace)


def test_wrong_latent_mass_is_rejected(monkeypatch):
    d, weights, lineage, namespace = fixture(monkeypatch)
    namespace.age_band_factors = lambda *args: (np.array([1.1, 1.1, 1., 1., 1.]), {})
    with pytest.raises(ValueError, match='removed lineage count'):
        membership.payer_weights(d, weights, lineage, namespace)
