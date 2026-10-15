"""Behavioral P7 controls: sharing, cohort mass and recipient boundaries."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location("p7_frames",HERE/"p7_frames.py")
p7 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p7)
spec_nest = importlib.util.spec_from_file_location("p7_nest",HERE/"p7_nest.py")
nest = importlib.util.module_from_spec(spec_nest)
spec_nest.loader.exec_module(nest)


def test_nest_scenario_extension_does_not_mutate_authoritative_globals():
    import types
    scope={"LANE_SCENARIOS":[("hs_or_less",2.,1.,np.inf)]}
    exec("def solve(): return LANE_SCENARIOS",scope)
    B=types.SimpleNamespace(row4_nest_rows=scope["solve"],LANE_SCENARIOS=scope["LANE_SCENARIOS"])
    solver=nest.scenario_solver(B,(8.7,17.9))
    assert [r[-1] for r in solver()]==[np.inf,8.7,17.9]
    assert len(B.row4_nest_rows())==1


def test_card_half_assignment_uses_different_group_and_payer_weights():
    d=pd.DataFrame(dict(PEARNVAL=[100.,200,300,400,100,200,300,400],
                        A_HGA=[39,40,42,43]*2,other=[True]*4+[False]*4,
                        target=[False]*4+[True]*4,native=[True]*8))
    # Add positive foreign branches so their share denominators are defined.
    d=pd.concat([d,d.assign(native=False)],ignore_index=True)
    rows=nest.card_bills(d,np.ones(16),np.full(16,2.),"fixture",p7.require)
    native,_,group,_=rows
    assert native["transfer_bn"]==pytest.approx(250/1e9)
    assert group["transfer_bn"]==pytest.approx(500/1e9)
    assert native["card_low_bn"]+native["card_high_bn"]==pytest.approx(1000/1e9)
    assert native["group_low_removal_share_card"]==pytest.approx(2/3)


def test_epsilon_change_keeps_nativity_and_skill_when_only_native_payers_thin():
    d=pd.DataFrame(dict(st=[6]*4,native=[True,False,True,False],A_HGA=[39,39,43,43],other=[True]*4))
    delta=np.array([10.,20,30,40])
    old=np.full(4,10.)
    new=np.array([5.,10,8,10])
    delivered=nest.transport_wage_delta(d,delta,old,new,p7.require)
    assert np.allclose(delivered*new,delta*old)
    assert np.array_equal(delivered[~d.native],delta[~d.native])


def test_unequal_sharing_can_cross_person_and_pooled_counts():
    d = pd.DataFrame(dict(SPM_ID=[1,1],other=[True,True]))
    wage = np.array([100.,0])
    tax = np.array([-40.,-40])
    w = np.ones(2)
    person = wage+tax
    pooled = p7.pooler(d,w)(person)
    unequal = p7.unequal_wages(d,wage,w,.2)+tax
    assert np.array_equal(person,[60,-40])
    assert np.array_equal(pooled,[10,10])
    assert np.array_equal(unequal,[-20,40])
    assert unequal.sum() == person.sum()
    # The individuals' signs are not bounded by their two endpoint signs.
    assert person[0]>0 and pooled[0]>0 and unequal[0]<0
    assert person[1]<0 and unequal[1]>0


def test_unequal_weights_conserve_each_unit_and_singletons():
    d=pd.DataFrame(dict(SPM_ID=[1,1,1,2,3],other=[True,True,True,True,False]))
    w=np.array([100.,200,50,80,20])
    x=np.array([100.,-30,0,60,999])
    for s in (.5,.8):
        y=p7.unequal_wages(d,x,w,s)
        assert np.dot(w[:3],y[:3]) == pytest.approx(np.dot(w[:3],x[:3]),abs=1e-9)
        assert y[3] == x[3] and y[4]==0


def test_aggregate_share_ahead_can_exceed_both_endpoint_counts():
    d=pd.DataFrame(dict(SPM_ID=[1,1,2,2],other=[True]*4))
    w=np.ones(4)
    x=np.array([100.,-1,8,-10])
    pooled=p7.pooler(d,w)(x)
    unequal=p7.unequal_wages(d,x,w,.8)
    assert (x>0).mean()==(pooled>0).mean()==.5
    assert (unequal>0).mean()==.75
    assert unequal.sum()==pytest.approx(x.sum(),abs=1e-12)


def test_reweighted_channel_preserves_gross_gains_and_losses():
    d=pd.DataFrame(dict(st=[6,6,48,48],other=[True]*4))
    x=np.array([100.,-100,10,-10])
    old=np.array([10.,10,20,20])
    new=np.array([8.,9,15,18])
    y=p7.transport(x,old,new,d)
    for state in (6,48):
        for sign in (1,-1):
            m=(d.st.to_numpy()==state)&(x*sign>0)
            assert np.dot(new[m],y[m])==pytest.approx(np.dot(old[m],x[m]),abs=1e-9)


def test_mixed_pool_preserves_boundary_transfers_and_member_dollars():
    d=pd.DataFrame(dict(SPM_ID=[1,1,2],other=[True,False,False]))
    w=np.array([100.,200,300])
    x=np.array([-10.,100,200])
    y=p7.pooler(d,w,np.ones(3,bool))(x)
    assert np.dot(w,y)==pytest.approx(np.dot(w,x),abs=1e-9)
    assert y[0]==y[1] and y[2]==x[2]


def test_mixed_presence_counts_nonmember_support_of_member_children():
    d = pd.DataFrame(dict(SPM_ID=[1]*4, other=[True,False,False,False],
                          target=[False,True,True,True]))
    weights = np.ones(4)
    resources = np.array([100.,10.,10.,10.])
    change, audit = p7.mixed_resource_change(d, weights, weights, resources, np.zeros(4))
    assert change.tolist() == [-67.5,0.,0.,0.]
    assert audit["forward_member_to_other_bn"] == pytest.approx(7.5/1e9)
    assert audit["reverse_other_to_member_bn"] == pytest.approx(75/1e9)
    assert audit["presence_boundary_change_bn"] == pytest.approx(-67.5/1e9)
    assert audit["removal_level_change_diagnostic_bn"] == pytest.approx(67.5/1e9)
    # Existing channel arrays are presence effects, so a cost of 20 lowers
    # the presence result by 20; it raises resources in the removal world.
    presence = np.array([-20.,0.,0.,0.])
    change, audit = p7.mixed_resource_change(d, weights, weights, resources, presence)
    assert change[0] == -87.5
    assert audit["other_after_level_bn"] == pytest.approx(120/1e9)


def test_mixed_presence_preserves_weighted_levels_and_nonmixed_units():
    d = pd.DataFrame(dict(SPM_ID=[1,1,1,2,2],other=[True,False,True,True,True],
                          target=[False,True,False,False,False]))
    other_weights = np.array([2.,0.,3.,4.,5.])
    member_weights = np.array([0.,7.,0.,0.,0.])
    resources = np.array([100.,10.,50.,30.,80.])
    presence = np.array([-20.,0.,10.,40.,-5.])
    change, audit = p7.mixed_resource_change(d,other_weights,member_weights,resources,presence)
    assert np.allclose(change[3:], (4*40+5*(-5))/9)
    assert np.dot(other_weights,change)/1e9 == pytest.approx(
        np.dot(other_weights,presence)/1e9 + audit["presence_boundary_change_bn"], abs=1e-15)


def test_bad_national_closure_fails_loudly():
    with pytest.raises(RuntimeError,match="BLOCKED.*bad"):
        p7.check_total("bad",np.array([1.]),np.array([1e9]),2.)


def test_equal_baselines_zero_presence_leave_no_mixed_transfer():
    d=pd.DataFrame(dict(SPM_ID=[1,1],other=[True,False],target=[False,True]))
    w=np.array([2.,3.])
    result,audit=p7.mixed_resource_change(d,w,w,np.array([30.,30.]),np.zeros(2))
    assert np.array_equal(result,np.zeros(2))
    assert audit["presence_boundary_change_bn"] == pytest.approx(0.,abs=1e-15)


def test_missing_manifest_does_not_enroll_current_input(tmp_path,monkeypatch):
    import types
    monkeypatch.setattr(p7,"HERE",tmp_path/"lane")
    path=tmp_path/"input"
    path.write_text("current bytes")
    wl=types.SimpleNamespace(ROOT=tmp_path,file_sha=lambda p:"arbitrary hash")
    with pytest.raises(RuntimeError,match="pin_manifest_exists"):
        p7.pin(path,wl)
    assert not (p7.HERE/"inputs/pins.json").exists()


def test_repeated_premise_gates_retain_every_evaluation(monkeypatch):
    monkeypatch.setattr(p7,"GATES",{})
    monkeypatch.setattr(p7,"GATE_COUNTS",{})
    monkeypatch.setattr(p7,"GATE_SCOPE","fixture")
    p7.require("premise",True)
    with pytest.raises(RuntimeError,match="premise"):
        p7.require("premise",False)
    assert p7.GATES["fixture/premise"]["passed"]
    assert not p7.GATES["fixture/premise/check_2"]["passed"]


def test_generated_pin_is_independent_of_output_destination(tmp_path,monkeypatch):
    import hashlib
    import types
    monkeypatch.setattr(p7,"HERE",tmp_path/"lane")
    p7.HERE.mkdir()
    wl=types.SimpleNamespace(file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest())
    first=tmp_path/"first.json"
    second=tmp_path/"elsewhere"/"second.json"
    second.parent.mkdir()
    (p7.HERE/"inputs").mkdir()
    import json
    (p7.HERE/"inputs/pins.json").write_text(json.dumps({"sha256":{"generated:fixture":hashlib.sha256(b'{"source":"same"}\n').hexdigest()}}))
    for path in (first,second):
        path.write_text('{"source":"same"}\n')
        p7.pin_generated(path,"generated:fixture",wl)
    assert p7.PINS["generated:fixture"] == wl.file_sha(first)


def test_cut_aggregation_keeps_national_total_and_sign_counts():
    d=pd.DataFrame(dict(other=[True,True,True,False],cut=["a","a","b","b"],resources_pc=[100.,200,300,0]))
    w=np.array([1.,2,3,99])
    x=np.array([10.,-5,20,999])
    rows=p7.cut_rows(d,w,x,{},["cut"])
    assert sum(r["total_bn"] for r in rows)==pytest.approx(60/1e9,abs=1e-15)
    assert rows[0]["winners_share"]==pytest.approx(1/3)
    assert rows[1]["winners_share"]==1


def test_responding_programmes_have_their_national_dollars(tmp_path):
    d=pd.DataFrame(dict(other=[True,True],SPM_ID=[1,2],SS_VAL=[100.,0],MCARE=[1,2],MCAID=[2,2],
                        A_AGE=[70,30],A_ENRLW=[2,2],A_HSCOL=[0,0]))
    for c in ["SSI_VAL","UC_VAL","SPM_SNAPSUB","SPM_CAPHOUSESUB","SPM_ENGVAL","ED_VAL","WC_VAL",
              "VET_VAL","DIS_VAL1","DIS_VAL2","PAW_VAL","ACTC_CRD","EIT_CRED"]:
        d[c]=0.
    w=np.array([1.,1.])
    key,table=p7.responding_programme_key(d,w,[dict(id="social_security",national_bn=10.,response=1.),
                                            dict(id="general_public_services",national_bn=6.,response=.5)])
    assert key.tolist()==[11.5e9,1.5e9]
    assert len(table)==2 and "ASSUMPTION" in table[1]["key"]


def test_within_run_source_drift_fails_with_a_manifest(tmp_path,monkeypatch):
    import hashlib
    import types
    monkeypatch.setattr(p7,"HERE",tmp_path/"lane")
    p7.HERE.mkdir()
    p7.PINS.clear()
    path=tmp_path/"input.txt"
    path.write_text("before")
    (p7.HERE/"inputs").mkdir()
    import json
    (p7.HERE/"inputs/pins.json").write_text(json.dumps({"sha256":{"input.txt":hashlib.sha256(b"before").hexdigest()}}))
    wl=types.SimpleNamespace(ROOT=tmp_path,file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest())
    p7.pin(path,wl)
    path.write_text("after")
    with pytest.raises(RuntimeError,match="within_run_pin"):
        p7.pin(path,wl)


def test_chunked_replicates_keep_shuffled_join_and_reject_unused_duplicate(tmp_path):
    import types
    import zipfile
    names=[f"pwwgt{i}" for i in range(1,161)]
    source=pd.DataFrame(np.arange(6*160).reshape(6,160),columns=names)
    source["h_seq"]=np.arange(6)+10
    source["PPPOS"]=1
    wanted=pd.DataFrame(dict(PH_SEQ=[15,10,13],PPPOS=[1,1,1]))
    path=tmp_path/"replicates.zip"
    def archive(frame):
        with zipfile.ZipFile(path,"w") as z:
            z.writestr("asec_csv_repwgt_2025.csv",frame.to_csv(index=False,lineterminator="\n"))
    archive(source)
    B=types.SimpleNamespace(PATHS={"cps":path})
    actual=p7.replicate_weights(wanted,B,chunk_size=2)
    expected=source.loc[[5,0,3],names].to_numpy(float).T
    assert np.array_equal(actual,expected)
    # The repeated identity is not requested by wanted; source uniqueness still
    # covers the full source window, not only the joined subset.
    archive(pd.concat([source,source.iloc[[2]]],ignore_index=True))
    with pytest.raises(RuntimeError,match="replicate_source_unique"):
        p7.replicate_weights(wanted,B,chunk_size=2)
