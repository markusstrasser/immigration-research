"""Material household weighting, source ownership and signed-calibration controls."""
import json
import numpy as np
import pytest

from oct16_statistics import summarize
from oct16_households import source_candidates, driver_parts, reconcile_native, latent_profiles


@pytest.mark.parametrize('live_key,status,blocked',[
    ('oct15','adopted','live key'),
    ('oct16','candidate','STATUS is not adopted'),
    ('oct16','adopted',None),
])
def test_repository_adoption_requires_matching_live_key_and_package(tmp_path,live_key,status,blocked):
    from oct16_households import require_adopted
    package=tmp_path/'case'
    package.mkdir()
    (package/'package.cjs').write_text('module.exports={V9:'+json.dumps({
        'CASE_KEY':'oct16','LANE':'case','STATUS':status,
        'ADOPTED':'2026-10-20','DECISION':'decision.md'})+'};\n')
    declaration=tmp_path/'live_case.json'
    declaration.write_text(json.dumps(dict(key=live_key,lane='case',adopted='2026-10-20',decision='decision.md')))
    if blocked:
        with pytest.raises(SystemExit,match=blocked):
            require_adopted('oct16',declaration)
    else:
        assert require_adopted('oct16',declaration)==dict(key='oct16',adopted='2026-10-20',decision='decision.md')


def test_final_publisher_rejects_unadopted_case_before_reading_inputs(monkeypatch):
    import oct16_households as household
    def blocked(key):
        assert key == 'oct16'
        raise ValueError('[BLOCKED] case is not adopted')
    monkeypatch.setattr(household,'require_adopted',blocked)
    with pytest.raises(ValueError,match='case is not adopted'):
        household.main()


def test_final_publisher_checks_adoption_before_loading_inputs(monkeypatch):
    import oct16_households as household
    calls = []
    monkeypatch.setattr(household,'require_adopted',lambda key: calls.append(key) or {'key':key,'adopted':'2026-10-20','decision':'decision.md'})
    def missing(path):
        assert calls == ['oct16']
        raise FileNotFoundError('adopted publisher reached inputs')
    monkeypatch.setattr(household,'read',missing)
    with pytest.raises(FileNotFoundError,match='adopted publisher reached inputs'):
        household.main()


def test_sign_uses_unweighted_balance_while_aggregate_uses_each_person_weight():
    result=summarize(np.array([-10.,8.,3.]),np.array([1.,10.,2.]),np.array([1,1,2]),{'all':np.array(['all']*3)})
    assert result['balance'].tolist()==[-2.,3.]
    assert result['weighted_dollars'].tolist()==[70.,6.]
    assert result['shares'][0]['share_members_net_positive']==11/13
    assert sum(result['weighted_dollars'])!=result['balance']@result['weight']


def test_net_concentration_can_exceed_one_and_gross_is_bounded():
    result=summarize(np.array([100.,-90.]),np.ones(2),np.arange(2),{'all':np.array(['all']*2)})
    stats={r['statistic']:r['value'] for r in result['concentration']}
    assert stats['top20_share_of_total']==4
    assert stats['top20_gross_positive_share']==.4


def test_count_atom_keeps_exact_carrier_owner_instead_of_all_parent_lines():
    atom=dict(generation='G3plus',source_side='receipt',source_line='tax',line='completion_tax',population='observed',category='taxes')
    originals=[dict(g='G3plus',source_side='receipt',source_line='tax',id=line,population=pop,cat='taxes')
               for line,pop in [('tax','engine'),('completion_tax','completion')]]
    assert [p['id'] for p in source_candidates(atom,originals)]==['completion_tax']


def test_native_calibration_signed_source_driver_is_on_changed_records_only():
    atom=dict(generation='G2',source_side='spending',source_line='school',line='school',population='observed',category='schools',cost_bn=-1.,source_piece='school')
    originals=[dict(g='G2',source_side='spending',source_line='school',id='school',population='engine',cat='schools',price=np.array([2.,3.,4.]))]
    parts=driver_parts(atom,originals,np.ones(3),np.array([.5,1.,2.]))
    assert len(parts)==1
    assert parts[0][2].tolist()==[-2.,0.,2.]
    assert parts[0][1]==1


def test_missing_spending_source_cannot_become_residual():
    atom=dict(generation='G2',source_side='spending',source_line='missing',line='missing',population='engine',cost_bn=1.)
    with pytest.raises(ValueError,match='no declared household source driver'):
        driver_parts(atom,[],np.ones(2),np.ones(2))


def test_unclassified_shared_post_amount_has_no_invented_household_owner():
    atom=dict(generation='G2',source_side='post_engine',source_line='mixed_unit_removal',
        line='mixed_unit_removal',population='observed',category='other_shared',cost_bn=-.0123,
        economic_class='unclassified_post_engine',source_piece='mixed-calibration')
    originals=[dict(g='G2',source_side='post_engine',source_line='mixed_unit_removal',id='mixed_unit_removal',
        population='engine',cat='other_shared',price=np.zeros(2))]
    assert driver_parts(atom,originals,np.ones(2),np.array([.5,1.]))==[]
    with pytest.raises(ValueError,match='zero signed source driver'):
        driver_parts({**atom,'economic_class':'classified'},originals,np.ones(2),np.array([.5,1.]))


def test_pure_calibration_preserves_unit_prices_and_does_not_create_crossings():
    prices=np.array([100.,100.])
    old=np.ones(2)
    new=np.array([.5,1.])
    correction,natural,remainder=reconcile_native(prices,old,new,np.ones(2,bool),-50/1e9)
    assert np.array_equal(correction,np.zeros(2))
    assert natural == -50/1e9 and remainder == 0
    assert (prices+correction)@new == 150
    assert np.array_equal(prices+correction,np.array([100.,100.]))
    assert np.array_equal((prices-80)<0,(prices+correction-80)<0)


def test_source_repricing_changes_only_the_calibrated_records():
    prices=np.array([100.,100.])
    old=np.ones(2)
    new=np.array([.5,1.])
    correction,natural,remainder=reconcile_native(prices,old,new,np.ones(2,bool),-60/1e9)
    assert correction[1]==0
    assert np.allclose(correction,[-20.,0.])
    assert np.isclose((prices+correction)@new,140)


def test_declared_college_operating_proxy_uses_its_exact_capital_carrier():
    atom=dict(generation='G3plus',source_side='spending',source_line='education_services',
        line='oct16_college_operating:completion_college',population='observed',category='education',cost_bn=-1.,source_piece='college')
    originals=[dict(g='G3plus',source_side='capital',source_line='college',id='completion_college',
        population='completion',cat='capital',price=np.array([2.,3.]))]
    parts=driver_parts(atom,originals,np.ones(2),np.array([.5,1.]))
    assert len(parts)==1 and parts[0][0]=='education_other'
    assert np.array_equal(parts[0][2],[-2.,0.])


def test_health_native_completion_part_keeps_its_actual_child_owner():
    atom=dict(generation='G3plus',source_side='spending',source_line='health_services',
        line='native_child_spending_health_services',population='completion',profile='native_nonreporters')
    originals=[dict(g='G3plus',source_side='spending',source_line='health_services',id='native_child_spending_health_services',
        population='native',cat='health')]
    assert source_candidates(atom,originals)==originals


def test_college_operating_amount_follows_declared_capital_source_line():
    atom=dict(generation='G3plus',source_side='spending',source_line='education_services',
        line='education_services:college_only',population='completion',kind='college_operating',
        capital_source_line='union_completion_college_low',cost_bn=-1.,source_piece='college')
    originals=[dict(g='G3plus',source_side='capital',source_line='college',id='union_completion_college_low',
        population='completion',cat='capital',price=np.array([2.,3.]))]
    parts=driver_parts(atom,originals,np.ones(2),np.ones(2))
    assert len(parts)==1 and parts[0][0]=='education_other'
    assert np.array_equal(parts[0][2],[2.,3.])


def test_health_original_and_latent_parts_use_their_distinct_weight_fractions():
    original=dict(g='G3plus',source_side='spending',source_line='health_services',id='health_services',
        population='engine',cat='health',price=np.array([4.,8.]),original_fraction=np.array([.8,.6]),latent_fraction=np.array([.2,.4]))
    atom=dict(generation='G3plus',source_side='spending',source_line='health_services',line='health_services',cost_bn=1.,source_piece='health')
    observed=driver_parts({**atom,'population':'original_union'},[original],np.ones(2),np.ones(2))
    latent=driver_parts({**atom,'population':'added_lineage'},[original],np.ones(2),np.ones(2))
    assert np.allclose(observed[0][2],[3.2,4.8])
    assert np.allclose(latent[0][2],[.8,3.2])


def test_latent_component_age_profiles_close_and_remain_distinct():
    lineage={'counts':{'later_losses':10.,'at_g3_rate':20.},'c3':.6,
        'age_mix':{'mixes':{'later':[.9,.1],'g3_rate':[.1,.9]}}}
    profiles=latent_profiles(np.array([2,7]),lineage)
    assert np.allclose(sum(profiles.values()),1)
    assert profiles['lineage_later_g3'][0]>profiles['lineage_later_g3'][1]
    assert np.allclose(profiles['lineage_g3_rate_white']/profiles['lineage_g3_rate_g3'],1.5)
