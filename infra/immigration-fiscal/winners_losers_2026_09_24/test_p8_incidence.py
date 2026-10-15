"""Scenario results must be independent of order and cached source aliases."""
from types import SimpleNamespace

import numpy as np
import pandas as pd

import p7_frames as p7
from p8_incidence import Incidence


def test_programme_receipts_keep_disability_sources_and_jurisdictions_separate():
    from p8_incidence import programme_keys
    d=pd.DataFrame(dict(other=True,pw=1.,SPM_ID=[1,2,3,4],DIS_SC1=[6,8,9,2],
                        DIS_SC2=0,DIS_VAL1=[100.,200.,300.,400.],DIS_VAL2=0))
    zeros=["PEN_SC1","PEN_SC2","PEN_VAL1","PEN_VAL2","SUR_SC1","SUR_SC2",
           "SUR_VAL1","SUR_VAL2","SS_VAL","SSI_VAL","UC_VAL","SPM_SNAPSUB",
           "SPM_CAPHOUSESUB","SPM_ENGVAL","MCARE","MCAID","A_AGE","A_ENRLW",
           "A_HSCOL","ED_VAL","WC_VAL","VET_VAL","PAW_VAL","ACTC_CRD",
           "EIT_CRED","VET_TYP4","VET_TYP5","MIL","CHAMPVA"]
    for name in zeros:
        d[name]=0
    import winners_losers as wl
    rows=[dict(id=name,national_bn=1.,response=1.,jurisdiction={"federal":fed,"state_local":1-fed},
               federal_share=fed,jurisdiction_basis="fixture") for name,fed in
          (("railroad_retirement",1),("black_lung",1),("temporary_disability",0))]
    federal,state,_=programme_keys(wl,d,np.ones(4),rows,{})
    np.testing.assert_array_equal(federal,[1e9,1e9,0.,0.])
    np.testing.assert_array_equal(state,[0.,0.,1e9,0.])


def test_evaluation_order_does_not_mutate_social_sources(monkeypatch):
    levels = ("low", "central", "high")
    d = pd.DataFrame(dict(other=[True,True],target=[False,False],st=[1,1],
                          pw=[1.,1.],SPM_ID=[1,2],SS_VAL=[0.,0.],MCARE=[0,0]))
    zero = lambda: np.zeros(2)
    all_levels = lambda v: {level: np.array(v,float) for level in levels}
    m = object.__new__(Incidence)
    m.d = m.dd = d
    m.weights = m.w = np.ones(2)
    m.mw = zero()
    m.other = np.ones(2,dtype=bool)
    m.resources = zero()
    m.fixes = frozenset()
    m.pool = lambda x: x.copy()
    m.notes, m.allocation_cache = {}, {}
    m.state_masks = {1: np.ones(2,dtype=bool)}
    m.wl = SimpleNamespace(CASE={"model":"fixture"},POSTAL={"AA":1},LEVELS=levels,
        alloc=lambda d,key,amount: np.full(2,amount*1e9/2),
        alloc_states=lambda d,key,amounts,**kw: np.full(2,sum(amounts.values())*1e9/2))
    fiscal = dict(federal_today=0.,future=0.,future_borrowing=0.,accrual=0.,
                  resource_federal=0.,state_local=0.)
    m.meta = dict(fiscal={level:fiscal.copy() for level in levels},
                  deficit={"share":0.},group_state_share={"AA":1.})
    m.trust = {level:dict(cash_benefits_bn=0.,payroll_bn=0.) for level in levels}
    m.fin = {"fixture":{"ends":{e:{"cost_bn":0.} for e in ("low","high")}}}
    m.channels = {name:all_levels([0.,0.]) for name in ("wages","displaced_beneficiaries")}
    for suffix in ("","_national_uniform"):
        m.channels["landlords"+suffix] = all_levels([2.,0.])
        m.channels["renters"+suffix] = all_levels([-1.,0.])
    cx = dict(kf=np.ones(2),ks=np.ones(2),property_key=np.ones(2),
              statew=all_levels([0.,0.]),credit=zero(),
              social={"housing_gain":all_levels([0.,0.])},
              social_values={"housing_gain":{e:1e-9 for e in levels}})
    m.context = lambda rule: cx
    monkeypatch.setattr(p7,"landlord_split",lambda wl,d,weights,land:
                        (land[::-1].copy(),None,None,None))
    def result(arm):
        return m.evaluate("a","stationary","central",arm=arm)[0]["person"].copy()
    first = result("recommended")
    stacked = result("stack")
    np.testing.assert_array_equal(stacked,[-2.,2.])
    np.testing.assert_array_equal(result("stack"),stacked)
    np.testing.assert_array_equal(result("recommended"),first)
    np.testing.assert_array_equal(cx["social"]["housing_gain"]["central"],[0.,0.])
