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


def test_bad_national_closure_fails_loudly():
    with pytest.raises(RuntimeError,match="BLOCKED.*bad"):
        p7.check_total("bad",np.array([1.]),np.array([1e9]),2.)


def test_generated_pin_is_independent_of_output_destination(tmp_path,monkeypatch):
    import hashlib
    import types
    monkeypatch.setattr(p7,"HERE",tmp_path/"lane")
    p7.HERE.mkdir()
    wl=types.SimpleNamespace(file_sha=lambda p:hashlib.sha256(Path(p).read_bytes()).hexdigest())
    first=tmp_path/"first.json"
    second=tmp_path/"elsewhere"/"second.json"
    second.parent.mkdir()
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


def test_within_run_source_drift_fails_before_a_manifest_exists(tmp_path,monkeypatch):
    import hashlib
    import types
    monkeypatch.setattr(p7,"HERE",tmp_path/"lane")
    p7.HERE.mkdir()
    p7.PINS.clear()
    path=tmp_path/"input.txt"
    path.write_text("before")
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
