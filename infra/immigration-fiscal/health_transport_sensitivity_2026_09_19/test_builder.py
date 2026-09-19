import numpy as np
import pandas as pd
import pytest
import importlib.util
from pathlib import Path

spec = importlib.util.spec_from_file_location("health_builder", Path(__file__).with_name("builder.py"))
lane = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lane)
domain_means_covariance, full_design_covariance = lane.domain_means_covariance, lane.full_design_covariance
meps_education, cps_education, age_deltas = lane.meps_education, lane.cps_education, lane.age_deltas


def test_full_design_domain_includes_outside_psus_and_joint_outcomes():
    data = pd.DataFrame(dict(PERWT24F=[1., 1., 1., 1.], VARSTR=[1, 1, 2, 2],
                             VARPSU=[1, 2, 1, 2], domain=[0, 1, 0, 1]))
    outcome = pd.DataFrame(dict(raw=[1., 3., 7., 11.], calibrated=[2., 6., 14., 22.]))
    fit = domain_means_covariance(data, ['domain'], outcome, data.domain.eq(0))
    assert fit['means'][0].tolist() == [4., 8.]
    np.testing.assert_allclose(fit['covariance'], [[4.5, 9.], [9., 18.]])
    with pytest.raises(ValueError, match='Lonely PSU'):
        full_design_covariance(data.iloc[[0, 2]].reset_index(drop=True),
                               fit['influence'][[0, 2]])


def test_education_preserves_ged_nondiploma_and_other_degree_ambiguity():
    assert meps_education([2, 1, 3, 4, 7, -8], [10, 12, 14, 15, 16, 17]).tolist() == [
        'hs_only', 'lt_hs', 'some_college', 'ba_plus', 'unknown', 'unknown']
    assert cps_education([38, 39, 41, 42, 43, 46, 0]).tolist() == [
        'lt_hs', 'hs_only', 'some_college', 'some_college', 'ba_plus', 'ba_plus', 'unknown']


def test_age_deltas_preserve_common_donor_covariance_and_cps_domain():
    common = dict(origin='mexico_born', education='lt_hs', band='0', outcome='calibrated',
                  scope='all', records=100, population=1000.)
    estimates = pd.DataFrame([{**common, 'row': i, 'model': model}
        for i, model in enumerate(['canonical', 'adult_age_birth', 'education_backoff'])])
    gradients = np.array([[1., 0.], [1., 0.], [0., 1.]])
    replicates = np.repeat(np.array([[1.], [1.], [2.]]), 161, axis=1)
    covariance = np.array([[9., 8.], [8., 9.]])
    rows, dg, dr = age_deltas(estimates, gradients, replicates, covariance)
    np.testing.assert_allclose(rows.medical_cost_delta_per_person, 1.)
    np.testing.assert_allclose(rows.se_meps, np.sqrt(2.))
    np.testing.assert_allclose(rows.se_cps, 0.)
    np.testing.assert_allclose(dg, [[-1., 1.], [-1., 1.]])
    estimates.loc[2, 'population'] = 999.
    with pytest.raises(ValueError, match='changed the CPS domain'):
        age_deltas(estimates, gradients, replicates, covariance)
