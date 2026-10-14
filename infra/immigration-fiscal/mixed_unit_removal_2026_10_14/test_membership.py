"""Behavioral controls: lineage links, step exclusion and aggregate transport."""
import numpy as np
import pandas as pd
import membership
import json
from types import SimpleNamespace
import pytest


def test_biological_child_leaves_step_and_adoptive_child_stay():
    d=pd.DataFrame(dict(PH_SEQ=[1]*5,A_LINENO=[1,2,3,4,5],PEPAR1=[-1,-1,1,1,1],
                        PEPAR2=[-1]*5,PEPAR1TYP=[-1,-1,1,2,3],PEPAR2TYP=[-1]*5,
                        PRCITSHP=[1]*5,A_AGE=[40,40,8,8,8]))
    member=np.array([True,False,False,False,False])
    bio,step,_=membership.biological_children(d,member,np.ones(5,bool))
    np.testing.assert_array_equal(bio,[False,False,True,False,False])
    np.testing.assert_array_equal(step,[False,False,False,True,False])


def test_second_parent_biological_even_when_first_parent_is_nonmember():
    d=pd.DataFrame(dict(PH_SEQ=[1]*3,A_LINENO=[1,2,3],PEPAR1=[-1,-1,2],PEPAR2=[-1,-1,1],
                        PEPAR1TYP=[-1,-1,1],PEPAR2TYP=[-1,-1,1],PRCITSHP=[1]*3,A_AGE=[40,40,8]))
    bio,_,_=membership.biological_children(d,np.array([True,False,False]),np.ones(3,bool))
    assert bio[2]


def test_added_transport_only_G3_and_all_replicates():
    case={'lineage':{'members':{'g3plus':2.},'counts':{'identified_g3plus':4.}}}
    v=np.arange(483).reshape(3,161).astype(float)
    got=membership.transport_added(case,v)
    np.testing.assert_array_equal(got[:2],np.zeros((2,161)))
    np.testing.assert_array_equal(got[2],.5*v[2])


def test_latent_pool_requires_actual_native_parent_and_child_two_US_parent_fields():
    d=pd.DataFrame(dict(PH_SEQ=[1]*4,A_LINENO=[1,2,3,4],PEPAR1=[-1,-1,1,2],PEPAR2=[-1]*4,
                        PEPAR1TYP=[-1,-1,1,1],PEPAR2TYP=[-1]*4,PRCITSHP=[4,1,1,1],
                        A_AGE=[40,40,8,8],PEFNTVTY=[313,57,57,57],PEMNTVTY=[313,57,57,57],PRDTHSP=[1,1,0,0]))
    member=np.array([True,True,False,False])
    np.testing.assert_array_equal(membership.latent_mask(d,member,np.ones(4,bool)),[False,False,False,True])


def test_input_pin_register_rejects_drift_without_refreshing_it(tmp_path,monkeypatch):
    real=membership.LANE/'inputs/membership_pension_pins.json'
    paths=[p['path'] for p in json.loads(real.read_text())['files']]
    lane=tmp_path/'fiscal'/'mixed_unit_removal_2026_10_14'
    (lane/'inputs').mkdir(parents=True)
    for rel in paths:
        p=lane.parent/rel
        p.parent.mkdir(parents=True,exist_ok=True)
        p.write_bytes(b'original immutable input')
    c=SimpleNamespace(__file__=str(lane.parent/'mixed_unit_credits_2026_10_14/credits.py'),
                      CPS_ZIP=lane.parent/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip')
    monkeypatch.setattr(membership,'LANE',lane)
    membership.verify_pins(c)
    before=(lane/'inputs/membership_pension_pins.json').read_bytes()
    c.CPS_ZIP.write_bytes(b'drifted authoritative input')
    with pytest.raises(SystemExit,match='immutable input drift'):
        membership.verify_pins(c)
    assert (lane/'inputs/membership_pension_pins.json').read_bytes()==before
