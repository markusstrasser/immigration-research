"""v8 membership conservation and native stayer-flow routing premises."""
from pathlib import Path
from types import SimpleNamespace
import json

import numpy as np
import pandas as pd
import pytest

import p8_membership as M
import p8_stayers as S


def test_membership_retains_original_other_when_loader_already_excluded_completion(monkeypatch):
    d = pd.DataFrame(dict(target=[True,False,False], other=[False,False,True],
                          other_base=[False,True,True],
                          PEPAR1TYP=1, PEPAR2TYP=1))
    canonical = SimpleNamespace(masks=lambda d: None, parent_rows=lambda d: None)
    monkeypatch.setattr(M, 'source_masks', lambda *args:
                        (np.array([False,True,False]), np.zeros(3,bool), Path('/tmp/source.py')))
    result, meta = M.apply_membership(d, Path('/tmp/fiscal'), canonical)
    assert result.other_oct14.tolist() == [False,True,True]
    assert result.target.tolist() == [True,True,False]
    assert result.other.tolist() == [False,False,True]
    assert d.target.tolist() == [True,False,False]
    assert meta['coverage_payer_people'] == 0.


def test_completion_removes_actual_people_after_the_old_latent_thinning():
    d = pd.DataFrame(dict(A_AGE=[25,25,25], st=6, PRCITSHP=1,
                          PEMNTVTY=[57,57,57], PEFNTVTY=[57,57,100], PRDTHSP=[1,0,1],
                          target=[True,False,True], other=[False,True,False],
                          target_oct14=[True,False,False], other_oct14=[False,True,True],
                          completion_member=[False,False,True]))
    w = np.array([20.,100.,10.])
    lineage = dict(counts=dict(added=5.,at_g3_rate=5.,later_losses=0.),
                   age_mix=dict(bands=['all'],mixes=dict(g3_rate=[1.],later=[1.])))
    out, cells, audit = M.payer_weights(d,w,lineage,SimpleNamespace(US_AREAS=[57]))
    assert out.tolist() == [20.,95.,0.]
    assert audit['oct14_payer_people'] == 105.
    assert audit['oct15_payer_people'] == 95.
    assert audit['removed_completion_people'] == 10.
    assert audit['coverage_payer_people'] == 0.


def test_stayer_flows_follow_own_spm_then_explicit_same_state_bucket():
    # Departing carrier 0 has a stayer in its SPM. Carrier 2 has none, and
    # therefore uses an explicit same-state bucket; the other state never pays.
    v = np.array([2.,1.,-4.,5.,0.])
    stay = np.array([False,True,False,True,True])
    units = np.array([1,1,2,3,4])
    states = np.array([6,6,6,6,48])
    w = np.array([1.,2.,1.,6.,10.])
    out, audit = S._remap(v,stay,units,states,w)
    assert out.tolist() == [0.,2.,0.,2.,0.]
    assert out.sum() == v.sum()
    assert audit['reassigned_within_spm_bn'] == 2.
    assert audit['unlocated_stayer_buckets'][0]['status'] == '[DEGRADED]'
    assert audit['unlocated_stayer_buckets'][0]['signed_bn'] == -4.


def test_stayer_routing_blocks_a_state_without_surviving_mass():
    with pytest.raises(ValueError, match='no stayer'):
        S._remap(np.array([1.,0.]), np.array([False,True]),
                 np.array([1,2]), np.array([6,48]), np.ones(2))


def test_old_credit_is_merged_once_at_source_dollars_after_payer_weight_change():
    d = pd.DataFrame(dict(other=[False,True,True], SPM_ID=[1,1,2], st=6))
    source_weights = np.array([10.,20.,30.])
    payer_weights = np.array([0.,10.,15.])
    original = np.array([100.,50.,20.])
    routed, audit = M.replacement_credit(d,payer_weights,original,source_weights)
    assert routed.tolist() == pytest.approx([0.,200.,40.])
    assert np.dot(routed,payer_weights) == pytest.approx(np.dot(original,source_weights))
    assert audit['source_total_bn'] == pytest.approx(2600 / 1e9)


def test_raw_policy_tax_observer_uses_native_before_after_not_old5b_delta():
    col = SimpleNamespace(n=3, events={})
    receipts = {}
    # A nonzero complete item5b subtraction is deliberately different from the
    # direct before-after amount; neither forward-only restoration nor zero
    # subtraction can recover the individual resource events by assumption.
    producer = dict(M1=np.array([[1.3]]), M3=np.array([[.8]]),
                    item=dict(receipts=np.array([[.7]]), spending=np.array([[1.2]])))
    observer = dict(h=np.array([0,1]), own=np.array([1,2]),
                    af=np.array([4.,1.]), bf=np.array([1.,2.]),
                    cr_after=np.array([0.,2.]), cr_before=np.array([3.,1.]))
    S._capture_policy('federal','union',producer,observer,col,receipts)
    assert col.events['union_policy_federal'].tolist() == [-1.,2.,1.]
    assert col.events['union_policy_refunds'].tolist() == [3.,1.,-2.]
    assert receipts['union_federal']['signed_presence_bn'] == 2.
    assert receipts['union_refunds']['signed_presence_bn'] == 2.
    assert receipts['union_federal']['source_fiscal_delta_bn'] == 1.3
    assert receipts['union_federal']['source_old5b_subtraction_bn'] == .7


def test_policy_route_excludes_fixed_pools_and_legacy_restoration(tmp_path, monkeypatch):
    fiscal = tmp_path / 'fiscal'
    source_dir = fiscal / 'mixed_unit_removal_2026_10_14/derived'
    source_dir.mkdir(parents=True)
    cache = tmp_path / 'cache'
    cache.mkdir()
    fixed = dict(M1_federal=1.,M2_state=.2,M3_refunds=.3,M6_biological_children=.1,
                 M5_consumption=2.,M5_owner_property=3.,M5_housing_key=4.)
    policy = dict(M1_federal=.7,M2_state=.2,M3_refunds=.4,M6_biological_children=.15)
    chunks = dict(tax={**{k:v for k,v in fixed.items() if k in S.POLICY_TAX},
                       **{'policy_'+k:v for k,v in policy.items()}},
                  resources={k:fixed[k] for k in ('M5_owner_property','M5_housing_key')},
                  consumption={'M5_consumption':2.},
                  health=dict(Medicaid_low=.5,Medicaid_high=1.,ACA_low=.2,ACA_high=.4),
                  snap=dict(SNAP_zero_observed_high_takeup=.3,SNAP_cap_observed_low_takeup=.6))
    frame = dict(PH_SEQ=np.array([1,2]),PPPOS=np.array([1,1]),SPM_ID=np.array([1,2]),
                 state=np.array([6,6]),stayer=np.ones(2,bool),weight=np.ones(2))
    for part, values in chunks.items():
        path = cache / ('item11_'+part+'.npz')
        np.savez(path, **frame, **{k:np.array([v,0.]) for k,v in values.items()})
        Path(str(path)+'.json').write_text(json.dumps(dict(source_sha256={},
            policy_tax_bn=policy if part=='tax' else None,policy_before_after={})))
    summaries, ends = [], {}
    for end,h,a,s in [('low','Medicaid_low','ACA_low','SNAP_zero_observed_high_takeup'),
                       ('high','Medicaid_high','ACA_high','SNAP_cap_observed_low_takeup')]:
        summaries.append(dict(method='set',end=end,component='bounded_'+end,arm='|'.join((h,a,s))))
        benefit = chunks['health'][h]+chunks['health'][a]+chunks['snap'][s]
        ends[end] = dict(D_added_residual_bn=.05,total_bn=sum(fixed.values())+benefit+.05)
    (source_dir/'round2_summary.json').write_text(json.dumps(dict(results=summaries)))
    monkeypatch.setattr(S,'FISCAL',fiscal)
    monkeypatch.setattr(S,'_signature',lambda: {})
    monkeypatch.setattr(S,'source_paths',lambda: [])
    d = pd.DataFrame(dict(PH_SEQ=frame['PH_SEQ'],PPPOS=frame['PPPOS'],other=True))
    payload = dict(meta=dict(mixed_unit_removal=dict(by_end=ends)))
    without = S.load_stayers(d,np.ones(2),fiscal,cache,payload)
    with_legacy = S.load_stayers(d,np.ones(2),fiscal,cache,payload,legacy_credit=np.array([1e9,0.]))
    assert set(without['by_end']['low']) == set(S.POLICY_TAX) | {'Medicaid','ACA','SNAP'}
    assert set(without['by_end']['low']) == set(without['by_end']['high'])
    for end in ('low','high'):
        for component in without['by_end'][end]:
            assert np.array_equal(without['by_end'][end][component],with_legacy['by_end'][end][component])
        assert with_legacy['metadata']['by_end'][end]['attribution_bn'] - without['metadata']['by_end'][end]['attribution_bn'] == pytest.approx(1.)
    assert without['metadata']['by_end']['low']['direct_policy_bn'] == pytest.approx(2.45)
    assert without['metadata']['by_end']['high']['direct_policy_bn'] == pytest.approx(3.45)
    assert without['metadata']['by_end']['low']['source_fiscal_minus_policy_bn'] == pytest.approx(9.2)
    assert 'D_added_residual' not in without['by_end']['low']
    assert 'M5_consumption' in without['by_end_attribution']['low']
