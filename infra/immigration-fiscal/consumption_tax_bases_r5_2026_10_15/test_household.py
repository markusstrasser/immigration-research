"""Behavior checks: overlapping exemptions, fixed collection pools, source controls."""
from pathlib import Path
import numpy as np
import pandas as pd
import pytest
import household

HERE=Path(__file__).resolve().parent


def test_joint_is_union_of_exempt_purchases():
    c=np.array([100.,100.,100.])
    f=np.array([30.,30.,30.]);snap=np.array([10.,10.,10.])
    e=np.array([0.,0.5,1.])
    joint=household.taxable_basket(c,f,snap,e,'joint')
    np.testing.assert_allclose(joint,[90.,80.,70.])
    # Full food exemption means SNAP adds nothing; no double subtraction.
    assert joint[-1]==household.taxable_basket(c,f,snap,e,'grocery')[-1]
    assert joint[0]==household.taxable_basket(c,f,snap,e,'snap')[0]


def test_benefit_cannot_exempt_more_than_purchases():
    assert household.taxable_basket([20.],[10.],[100.],0.,'joint')[0]==10.
    assert household.taxable_basket([-5.],[10.],[100.],1.,'joint')[0]==0.
    with pytest.raises(ValueError,match='outside'):
        household.taxable_basket([100.],[20.],[0.],1.1,'grocery')


def test_ce_controls_match_published_food_deciles():
    d=pd.read_csv(HERE/'derived/household_ce_deciles.csv')
    np.testing.assert_allclose(d.food_share,d.calibrated_food_share,rtol=1e-12)
    assert d.food_share.between(0,1).all()


def test_collection_normalization_and_full_basket_identity():
    d=pd.read_csv(HERE/'derived/household_state_factors.csv')
    full=d[d.arm.eq('full')]
    np.testing.assert_allclose(full.factor_state,1.,atol=1e-12)
    np.testing.assert_allclose(full.factor_national,1.,atol=1e-12)
    np.testing.assert_allclose(d.group_share_state,d.group_key/d.state_key,rtol=1e-12)
    positive=d.group_raw_key.gt(0)
    np.testing.assert_allclose(d.loc[positive,'factor_state'],
        (d.loc[positive,'group_key']/d.loc[positive,'group_raw_key']) /
        (d.loc[positive,'state_key']/d.loc[positive,'state_raw_key']),rtol=1e-12)
    for _,g in d[d.group.eq('union')&d.state_fips.ne(0)].groupby(['snap_source','arm']):
        # Allocation of a fixed $1 state tax pool to members and others closes.
        np.testing.assert_allclose(g.group_key/g.state_key+(g.state_key-g.group_key)/g.state_key,1.)


def test_state_rule_changes_and_complete_coverage():
    r=pd.read_csv(HERE/'inputs/grocery_state_2024.csv').set_index('state_fips')
    assert len(r)==51
    assert r.loc[6,'exempt_fraction']==1.  # California
    assert r.loc[48,'exempt_fraction']==1. # Texas
    assert r.loc[1,'exempt_fraction']==.25 # Alabama held at 3% in 2024
    assert r.loc[20,'exempt_fraction']==pytest.approx(1-2/6.5)
    assert r.loc[40,'exempt_fraction']==pytest.approx(125/366) # Aug 29-Dec 31
