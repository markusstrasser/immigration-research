"""Composition-policy invariants, including membership not identified by origin."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


SPEC = importlib.util.spec_from_file_location('native_measure', Path(__file__).with_name('native_measure.py'))
N = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(N)


def test_origin_loss_preserves_hispanic_total_and_all_replicate_mexican_targets():
    mex = np.array([100., 105., 95.])
    other = np.array([50., 40., 60.])
    x = N.calibration_cell(mex, other, 80., 140., True)
    np.testing.assert_allclose(x['native_factor'], 1.)
    np.testing.assert_allclose(mex*x['mexican_retention_probability'] +
                               other*x['other_to_mexican_probability'], 80.)
    np.testing.assert_allclose(x['target_hispanic'], mex+other)


def test_other_hispanic_to_mexican_transfer_reaches_upward_target_without_creating_people():
    x = N.calibration_cell(np.array([100., 95.]), np.array([50., 55.]), 120., 150., True)
    assert np.all(x['mexican_retention_probability'] == 1)
    np.testing.assert_allclose(x['other_to_mexican_probability'], [.4, 25/55])
    np.testing.assert_allclose(x['target_hispanic'], 150.)


def test_lower_hispanic_total_is_a_distinct_control_factor():
    x = N.calibration_cell(np.array([100., 120.]), np.array([50., 60.]), 80., 120., False)
    np.testing.assert_allclose(x['native_factor'], [.8, 2/3])
    np.testing.assert_allclose(x['target_hispanic'], 120.)


def test_impossible_hispanic_target_fails_loudly():
    with pytest.raises(RuntimeError, match='Mexican target cannot exceed Hispanic target'):
        N.calibration_cell(np.array([100.]), np.array([20.]), 130., 120., True)


def test_ancestry_membership_survives_mexican_origin_reassignment():
    # One G2, one both-US-parent reporter, one completion reporter, one
    # nonreporting G2: only the both-US reporter departs after origin transfer.
    c = pd.DataFrame(dict(PH_SEQ=[1,2,3,4], PPPOS=[1]*4, A_LINENO=[1]*4,
        GESTFIPS=[6]*4, A_AGE=[2]*4, A_SEX=[1]*4, PRDTHSP=[1,1,1,2],
        PRCITSHP=[1]*4, PEFNTVTY=[303,57,57,303], PEMNTVTY=[57,57,301,57],
        pwwgt0=[10.]*4))
    vectors = {}
    for region in ('CA_TX','outside_CA_TX'):
        for lo, hi in N.AGES:
            vectors[(region,f'{lo}-{hi}')] = {
                'mexican': (np.repeat(100.,161),np.repeat(80.,81)),
                'other_hispanic': (np.repeat(50.,161),np.repeat(70.,81)),
                'hispanic': (np.repeat(150.,161),np.repeat(150.,81))}
    rows = [dict(region='national',age_band='0-17',kind='hispanic',
                 z_independent_surveys=0.,acs=150.,cps=150.)]
    result, _, _ = N.person_factors(c,vectors,rows)
    np.testing.assert_allclose(result.native_member_factor, [1.,.8,1.,1.])
    np.testing.assert_allclose(result.mexican_effective_factor[:3], .8)
    # Central survey weights balance both origin strata, including G2 members.
    np.testing.assert_allclose(result.central_member_factor, [.8,.8,.8,1.4])
    np.testing.assert_allclose(result.hispanic_reassignment_factor, [1.,1.,1.,1.4])


def test_linked_nonmexican_hispanic_children_are_not_called_nonhispanic():
    # Two US-born biological parents, one Mexico-born grandparent; child
    # reports another Hispanic origin. This is a linked G3 non-Mexican child.
    d = pd.DataFrame(dict(PH_SEQ=[1]*3,A_LINENO=[1,2,3],PEPAR1=[0,0,1],PEPAR2=[0,0,2],
        PEPAR1TYP=[0,0,1],PEPAR2TYP=[0,0,1],PENATVTY=[57]*3,
        PEMNTVTY=[303,57,57],PEFNTVTY=[57]*3,PRDTHSP=[1,0,2],
        PRCITSHP=[1]*3,A_AGE=[40,40,10],A_SEX=[1,2,1]))
    d = pd.concat([d, pd.DataFrame(1., index=d.index, columns=N.CW)], axis=1)
    rows, _ = N.linked_tables(d)
    selected = {r['origin']:r for r in rows if r['parent_arm']=='biological'
                and r['generation']=='G3' and r['age_band']=='0-17' and r['sex']==0}
    assert selected['other_Hispanic']['persons'] == 1
    assert selected['all_nonMexican']['persons'] == 1
    assert selected['non_Hispanic']['persons'] == 0
