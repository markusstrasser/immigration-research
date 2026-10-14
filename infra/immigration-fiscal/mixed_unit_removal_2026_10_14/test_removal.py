"""Accounting and removal fixtures; run with the lane's pytest command."""
import importlib.util
import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
import sys
import types

LANE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tested_removal',LANE/'removal.py')
M=importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)


def test_external_driver_main_module_does_not_replace_runtime_api(monkeypatch):
    monkeypatch.setitem(sys.modules,'__main__',types.SimpleNamespace(driver='cProfile'))
    api=M.runtime_api()
    assert api.federal_removal is M.federal_removal
    assert api.gate is M.gate
    assert callable(api.load_module)


def test_signed_replicate_unit_totals_are_conserved():
    old=np.array([100.,100.,20.,20.])
    income=np.array([0.,1000.,20.,10.])
    unit=np.array([0,0,1,1])
    w=np.array([-1.,3.,2.,4.])
    new,residual=M.weight_preserving_split(old,income,unit,w,np.array([True,True]))
    assert new[0]==0
    assert np.max(np.abs(residual))<1e-9
    assert old@w==pytest.approx(new@w,abs=1e-9)


def test_CBO_sufficient_totals_match_independent_group_sums():
    old=np.array([10.,20.,30.,40.,50.,60.])
    new=np.array([20.,10.,25.,45.,55.,55.])
    w=np.array([1.,2.,-.1,1.,3.,2.])
    gen=np.array([-1,0,1,2,0,-1])
    civ=np.ones(6,bool)
    union=gen>=0
    code=np.array([0,0,1,1,2,2])
    targets=np.array([.2,.3,.5])
    bg,bc,delta,fd=M.consumption_exposure(old,new,w,civ,union,gen,code,targets)
    assert bg==pytest.approx(old[union]@w[union]/(old@w),abs=1e-12)
    oracle=sum(targets[j]*(old[(code==j)&union]@w[(code==j)&union])/(old[code==j]@w[code==j]) for j in range(3))
    assert bc==pytest.approx(oracle,abs=1e-12)
    for g in range(3):
        m=gen==g
        assert delta[g]==pytest.approx((new[m]-old[m])@w[m]/(old@w),abs=1e-12)
        oracle=sum(targets[j]*((new[(code==j)&m]-old[(code==j)&m])@w[(code==j)&m])/(old[code==j]@w[code==j]) for j in range(3))
        assert fd[g]==pytest.approx(oracle,abs=1e-12)


def test_zero_own_income_retains_declared_equal_split():
    old=np.array([10.,10.])
    new,_=M.weight_preserving_split(old,np.zeros(2),np.array([0,0]),np.array([2.,3.]),np.array([True]))
    np.testing.assert_array_equal(old,new)


def test_credit_cancellation_when_replicate_benchmark_masses_differ():
    # Reproducing the already-booked credit under the new operator must produce
    # zero correction, even when sampled national IRS key masses vary.
    weights=np.linspace(1,2,161)
    context={'mass_r4':.8,'vkey':np.linspace(.7,.9,161)}
    control_credit=100*weights/context['mass_r4']
    reproduced_credit=100*weights/M.federal_denominator(context)
    np.testing.assert_array_equal(reproduced_credit-control_credit,np.zeros(161))


def test_direct_weighted_totals_equal_full_materialized_account():
    values=np.array([100.,-20.,30.,-40.])
    owner=np.array([[1.,0.,0.,.5],[0.,1.,0.,.5],[0.,0.,1.,0.]])
    weights=np.arange(12,dtype=float).reshape(4,3)-2
    expected=owner@(values[:,None]*weights)
    actual=M.weighted_generation_totals(values,owner,weights)
    np.testing.assert_array_equal(actual,expected)


def test_missing_terminal_civilian_stratum_keeps_mask_shape():
    # The final SPM unit has only civilians; its odd subgroup is empty. This
    # fixture failed when the declared mask was longer than max(unit)+1.
    old=np.array([10.,10.,20.,20.])
    new,residual=M.weight_preserving_split(old,np.array([0.,20.,0.,30.]),np.array([0,0,2,2]),
                                         np.ones(4),np.array([True,False,True,False]))
    assert len(residual)==4
    assert np.max(np.abs(residual))<1e-9
    assert new.sum()==pytest.approx(old.sum())


def test_original_joint_tax_bill_is_not_duplicated_in_disposable_income():
    d=pd.DataFrame({'FEDTAX_AC':[100.,0.],'STATETAX_A':[50.,0.],
                    'PTOTVAL':[800.,200.],'FICA':[60.,15.]})
    R=pd.DataFrame({'row':[0],'spouse':[1]})
    income,fit,sit=M.disposable_income(d,R,{'agi_parts':np.array([800.,200.])})
    np.testing.assert_allclose(fit,[80.,20.],rtol=0,atol=1e-12)
    np.testing.assert_allclose(sit,[40.,10.],rtol=0,atol=1e-12)
    assert income.sum()==pytest.approx(1000-75-100-50)


def registry_fixture():
    # Member mother leaves; a nonmember father on a different current return
    # receives the staying child. His filing status and credits must change.
    d=pd.DataFrame({'PH_SEQ':[1,1,1],'A_LINENO':[1,2,3],
                    'PEPAR1':[0,0,1],'PEPAR2':[0,0,2],
                    'A_AGE':[40,40,10],'A_ENRLW':[0,0,0]})
    R=pd.DataFrame({'row':[0,1],'spouse':[-1,-1],'status':['hoh','single'],
                    'depfiler':[False,False], 'n_all':[1,0], 'n_mem':[0,0],
                    'n_non':[1,0], 'k17_all':[1,0], 'k13_all':[1,0], 'keitc_all':[1,0],
                    'other_all':[0,0], 'g0_mem':[0,0], 'g1_mem':[0,0], 'g2_mem':[0,0]})
    return d,R


def test_staying_child_is_transferred_to_actual_nonmember_parent():
    d,R=registry_fixture()
    out,own,k,owner,details=M.survivor_registry(d,R,np.array([True,False,False]),
        np.array([1,-1,-1]),np.ones(3,bool),np.array([2]),np.array([0]))
    assert own.tolist()==[-1,1]
    assert k['n'].tolist()==[0.,1.]
    assert out.status.tolist()==['single','hoh']
    assert owner[:,1].tolist()==[0.,1.,0.]
    assert details['transferred_dependents']==1
    assert details['nonmember_dependents_without_remaining_claimant']==0


def test_no_imaginary_claimant_when_both_parents_leave():
    d,R=registry_fixture()
    out,own,k,owner,details=M.survivor_registry(d,R,np.array([True,True,False]),
        np.array([1,2,-1]),np.ones(3,bool),np.array([2]),np.array([0]))
    assert own.tolist()==[-1,-1]
    assert k['n'].sum()==0
    assert details['nonmember_dependents_without_remaining_claimant']==1


def test_parent_nonfiler_gets_new_return_instead_of_assumed_credit():
    d,R=registry_fixture()
    R=R.iloc[:1].copy()
    out,own,k,owner,details=M.survivor_registry(d,R,np.array([True,False,False]),
        np.array([1,-1,-1]),np.ones(3,bool),np.array([2]),np.array([0]))
    assert own.tolist()==[-1,1]
    assert out.row.tolist()==[0,1]
    assert k['n'].tolist()==[0.,1.]
    assert details['new_nonfiler_claimants']==1


def test_completed_replicates_reproduce_SEs_and_stack():
    results=pd.read_csv(LANE/'derived/results.csv')
    reps=pd.read_csv(LANE/'derived/replicates.csv').set_index(['component','generation'])
    cols=[f'r{i}' for i in range(161)]
    for _,row in results.iterrows():
        v=(reps.loc[(row.component,row.generation),cols].to_numpy(float) if row.generation!='all'
           else reps.loc[row.component,cols].sum(axis=0).to_numpy(float))
        assert v[0]==pytest.approx(row.union_delta_low_bn,abs=1e-9)
        se=np.sqrt(4/160*np.square(v[1:]-v[0]).sum())
        assert se==pytest.approx(row.union_se_bn,abs=1e-9)
    for gen in ('G1','G2','G3+'):
        stack=reps.loc[('conditional_fixed_pool_stack',gen),cols].to_numpy(float)
        parts=sum(reps.loc[(k,gen),cols].to_numpy(float) for k in
                  ('M1','M2','M3','M4_conditional_SNAP','M5_fixed_pool'))
        np.testing.assert_allclose(stack,parts,rtol=0,atol=1e-9)


def test_unidentified_M6_and_health_are_not_admitted_as_zero_effects():
    x=json.loads((LANE/'derived/summary.json').read_text())
    assert x['adopted_new_edit_bn'] is None
    assert x['M6']['cost_delta_bn'] is None
    assert x['M6']['overlap_identified'] is False
    assert x['M6']['duplicate_count_added']==0
    assert x['stack']['Medicaid_CHIP_ACA_spending_identified'] is False
    assert x['stack']['M6_included'] is False


def test_positive_control_uses_original_outputs_byte_for_byte():
    original=LANE.parent/'mixed_unit_credits_2026_10_14/derived'
    for path in (LANE/'derived/positive_control').iterdir():
        assert path.read_bytes()==(original/path.name).read_bytes()


def test_case_split_has_no_added_people_in_union_receipt_target():
    x=json.loads((LANE/'derived/case_inputs.json').read_text())
    for line in x['lines'].values():
        assert line['union_target_bn']+line['lineage_target_bn']==pytest.approx(line['full_target_bn'],abs=1e-9)
    assert x['endpoints']=={'set':[16,11],'cash':[16,11]}
