"""Policy boundaries and statutory-household counterfactual checks."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

S=importlib.util.spec_from_file_location('health_tested',Path(__file__).with_name('health.py'))
h=importlib.util.module_from_spec(S)
S.loader.exec_module(h)


@pytest.fixture(scope='module')
def rule():
    return h.rules()


def frame():
    # Two unmarried parents, their child, and a grandparent claiming the child.
    d=pd.DataFrame(dict(PH_SEQ=[1]*4,A_LINENO=[1,2,3,4],A_AGE=[35,34,8,60],
                        A_SPOUSE=[0,0,0,0],FILESTAT=[5,5,6,4],DEP_STAT=[0,0,4,0],
                        PEPAR1=[0,0,1,0],PEPAR2=[0,0,2,0],GESTFIPS=[48]*4,
                        WSAL_VAL=[40000,15000,0,0],SEMP_VAL=[0]*4,FRSE_VAL=[0]*4,
                        INT_VAL=[0]*4,DIV_VAL=[0]*4,RNT_VAL=[0]*4,CAP_VAL=[0]*4,
                        UC_VAL=[0]*4,PNSN_VAL=[0]*4,ANN_VAL=[0]*4))
    return d


def test_2024_primary_policy_changes_and_group_costs(rule):
    t=rule['thresholds']
    assert t[48]['adult']==0 and t[48]['parent']==12
    assert t[4]['chip']==225  # July24 Arizona increase from old200
    assert t[45]['parent']==95 and t[47]['parent']==100
    assert t[55]['adult']==95  # superscript3 must not produce953
    assert t[40]['parent']==33 # superscript6 must not produce336
    assert rule['costs'][6][0]==3697.1
    assert rule['costs'][37][1]==6338.13
    assert set(rule['cost_proxy_states'])=={37,55}


def test_primary_pdf_policy_parser_reproduces_pinned_text():
    assert h.normalize_policy_pdf()==(h.INPUTS/'health_policy2024.txt').read_text()


def test_medicaid_dependent_exception_keeps_parents_not_grandparent():
    d=frame();x=h.households(d,np.zeros(4,bool),np.array([40000,15000,0,6000]))
    assert x['exception'][2]
    assert x['roster'][2]==(0,1,2)
    assert x['size'][2]==3 and x['magi'][2]==55000
    # ACA tax family follows claimant despite Medicaid exception.
    assert x['tax_roster'][2]==(2,3)
    assert x['tax_size'][2]==2 and x['tax_magi'][2]==6000


def test_remove_claimant_parent_rebuilds_survivor_magi():
    d=frame();d.loc[2,'DEP_STAT']=1
    x=h.households(d,np.array([1,0,0,0],bool),np.array([40000,15000,0,6000]))
    assert x['roster'][2]==(1,2)
    assert x['size'][2]==2 and x['magi'][2]==15000
    assert x['tax_roster'][2]==(1,2)
    assert x['parent'][1] and not x['parent'][0]


def test_dependent_child_income_excluded_until_required_to_file():
    d=frame();d.loc[2,'DEP_STAT']=1;d.loc[2,'WSAL_VAL']=14000
    x=h.households(d,np.zeros(4,bool),np.array([40000,15000,14000,6000]))
    assert x['magi'][2]==55000
    d.loc[2,'WSAL_VAL']=15000
    y=h.households(d,np.zeros(4,bool),np.array([40000,15000,15000,6000]))
    assert y['magi'][2]==70000


@pytest.mark.parametrize('parent_type',[1,2,3])
def test_nonrequired_adult_child_excluded_in_parent_household_any_age(parent_type):
    d=frame();d.loc[2,'A_AGE']=20;d.loc[2,'DEP_STAT']=1
    d.loc[2,'WSAL_VAL']=5000;d.loc[2,'PEPAR2']=0
    d['PEPAR1TYP']=[0,0,parent_type,0]
    x=h.households(d,np.zeros(4,bool),np.array([40000,15000,5000,6000]))
    assert x['roster'][0]==(0,2) and x['magi'][0]==40000
    assert x['roster'][2]==(0,2) and x['magi'][2]==40000
    assert x['tax_magi'][0]==40000 and x['tax_magi'][2]==40000


def test_nonparent_ward_own_medicaid_income_counts_but_taxpayer_excludes_it():
    d=frame();d.loc[2,['PEPAR1','PEPAR2']]=0
    d.loc[2,'WSAL_VAL']=5000 # under19, nonrequired, claimed by grandparent
    x=h.households(d,np.zeros(4,bool),np.array([40000,15000,5000,6000]))
    assert x['exception'][2]
    assert x['roster'][2]==(2,) and x['magi'][2]==5000
    assert x['roster'][3]==(2,3) and x['magi'][3]==6000
    assert x['tax_roster'][2]==(2,3) and x['tax_magi'][2]==6000
    # Claimant departs; unclaimed survivor's own tax/MAGI income remains.
    after=h.households(d,np.array([0,0,0,1],bool),np.array([40000,15000,5000,6000]))
    assert after['roster'][2]==(2,) and after['magi'][2]==5000
    assert after['tax_roster'][2]==(2,) and after['tax_magi'][2]==5000


def test_resident_married_spouse_in_medicaid_even_separate_returns():
    d=frame();d.loc[0,'A_SPOUSE']=2;d.loc[1,'A_SPOUSE']=1
    d.loc[[0,1],'FILESTAT']=5;d.loc[2,'DEP_STAT']=1
    x=h.households(d,np.zeros(4,bool),np.array([40000,15000,0,6000]))
    assert x['roster'][0]==(0,1,2) and x['magi'][0]==55000
    assert x['roster'][1]==(0,1) and x['magi'][1]==55000
    assert x['tax_roster'][0]==(0,2) and x['tax_magi'][0]==40000
    assert x['tax_roster'][1]==(1,) and x['tax_magi'][1]==15000
    # A departing spouse is absent in both regimes.
    after=h.households(d,np.array([0,1,0,0],bool),np.array([40000,15000,0,6000]))
    assert after['roster'][0]==(0,2) and after['magi'][0]==40000


def test_parent_dependent_adopts_claimants_medicaid_spouse_not_aca_spouse():
    d=frame();d.loc[0,'A_SPOUSE']=2;d.loc[1,'A_SPOUSE']=1
    d.loc[[0,1],'FILESTAT']=5
    d.loc[2,'A_AGE']=20;d.loc[2,'DEP_STAT']=1;d.loc[2,'PEPAR2']=0
    d.loc[2,'WSAL_VAL']=5000
    x=h.households(d,np.zeros(4,bool),np.array([40000,15000,5000,6000]))
    assert x['roster'][2]==(0,1,2) and x['magi'][2]==55000
    assert x['tax_roster'][2]==(0,2) and x['tax_magi'][2]==40000


def test_pinned_primary_law_has_no_agecutoff_and_spouse_is_unconditional():
    import xml.etree.ElementTree as ET
    text=' '.join(ET.parse(h.INPUTS/'benefit_magi_law.xml').getroot().itertext())
    assert 'natural, adopted or step parent' in text
    assert 'whether or not the individual files a tax return' in text
    assert 'each spouse will be included in the household of the other spouse' in text
    assert 'regardless of whether they expect to file a joint tax return' in text
    ptc=(h.INPUTS/'benefit_ptc24.txt').read_text()
    assert 'dependents who are required to file an income tax return' in ptc


def test_nonexpansion_childless_not_138_and_expansion_boundary(rule):
    d=frame();fam=dict(size=np.ones(4,int),magi=np.array([15000]*4),parent=np.zeros(4,bool))
    e,g,r,chip=h.eligibility(d,fam,rule)
    assert not e[0] and not e[1] and e[2] # Texas adults fail, child qualifies
    d.loc[:,'GESTFIPS']=6
    fam['magi'][:]=h.poverty(np.ones(4,int),np.array([6]*4),rule['base']['fpl'])*1.38
    assert h.eligibility(d,fam,rule)[0].all()
    fam['magi'][:]+=1
    assert not h.eligibility(d,fam,rule)[0][0]


def test_enhanced_aca_uses_2023_fpl_and_no400_cliff(rule):
    assert rule['fpl23'][0,0]==14580
    income=np.array([14580*1.5,14580*2.,14580*3.,14580*4.,14580*4.01])
    q=h.ptc_amount(income,np.repeat(14580.,5),np.repeat(12000.,5),np.ones(5,bool),rule['ptc_figures'])
    assert q[0]==12000
    assert q[1]==12000-income[1]*.02
    assert q[2]==12000-income[2]*.06
    assert q[3]==12000-income[3]*.085
    assert q[4]>0 and q[4]<q[3]


def test_medicaid_eligible_filer_does_not_zero_other_relatives_ptc(rule):
    # Two-person tax family: filer eligible for Medicaid, other member eligible
    # for Marketplace. IRS coveragefamily excludes filer only; covcount1.
    q=h.ptc_family_amount(np.array([25000.]),np.array([19720.]),np.array([7000.]),np.array([1]),rule['ptc_figures'])
    assert q[0]==7000.
    # No eligible coverage-family members => no PTC at same family MAGI.
    zero=h.ptc_family_amount(np.array([25000.]),np.array([19720.]),np.array([7000.]),np.array([0]),rule['ptc_figures'])
    assert zero[0]==0.
    text=(h.INPUTS/'benefit_ptc24.txt').read_text()
    assert 'Coverage family. Your coverage family includes all' in text
    assert 'individuals in your tax family who are enrolled in a' in text


def test_any_relative_marketplace_takeup_and_unique_original_carrier():
    d=frame();d.loc[0,'A_SPOUSE']=2;d.loc[1,'A_SPOUSE']=1
    d.loc[[0,1],'FILESTAT']=2;d.loc[2,'DEP_STAT']=1
    d['AGI']=[55000,0,0,6000]
    d['NOW_MRK']=[2,2,1,2];d['NOW_MRKS']=[2,2,1,2]
    family=h.households(d,np.zeros(4,bool),np.array([40000,15000,0,6000]))
    market,subs,donor=h.tax_family_takeup(d,family,np.array([1,1,0,1],bool))
    assert market[0] and subs[0] # filer uninsured/Medicaid; relativeMarketplace
    assert market[1] and subs[1]
    assert donor.tolist()==[True,False,False,True] # jointspouse is not secondunit


def test_weighted_generation_conservation_unequal_signed_replicates():
    d=pd.DataFrame({'SPM_ID':[1,1,1]});W=np.ones((3,161));W[0]=2;W[1]=3;W[2]=7
    W[1,1]=-1
    change=np.zeros_like(W);change[2]=5000
    out=h.attribute(change,d,W,np.array([1,1,0],bool),np.array([0,2,-1]))
    assert np.allclose(out.sum(axis=0),(change*W).sum(axis=0)/1e9)
    assert out[0,0]==pytest.approx(35000/1e9*2/5)
    assert out[0,1]==pytest.approx(35000/1e9*2/1)


def test_empty_takeup_cells_are_explicit_full_range():
    d=pd.DataFrame({'GESTFIPS':[48,48]});W=np.ones((2,161))
    ids,bounds,meta=h.rates(d,W,np.array([False,False]),np.array([2,2]),np.array([1.,1.]),np.array([0,1],bool),np.ones(2,bool))
    assert meta[0]['sample']==0 and meta[0]['lower']==0 and meta[0]['upper']==1
    assert (bounds[int(ids[0])][0]==0).all() and (bounds[int(ids[0])][1]==1).all()
