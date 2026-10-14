"""Requested limiting cases and explicit response regression checks."""
import numpy as np
import pytest
from reallocation import record, two_block


def test_empty_response_is_rejected_instead_of_selecting_central():
    parts={"corporate":np.arange(161.)}
    default={r:{"corporate":v} for r,v in (("low",1.),("high",.37))}
    assert np.array_equal(record(parts,default)["low"],parts["corporate"])
    with pytest.raises(ValueError,match="explicit responses"):
        record(parts,default,{})
    zeros={r:{"corporate":0.} for r in default}
    assert not record(parts,default,zeros)["low"].any()


def test_reallocation_off_recovers_pooled_jobs_key():
    w=np.array([[10.],[20.],[30.]])
    wg=np.array([[1.],[4.],[5.]])
    # Nontrivial pooled tax exposure differs from actual wage shares.
    shares=np.array([[.12],[.12],[.08]])
    taxes=np.array([[3.],[9.],[11.]])
    got,_=two_block(w,wg,shares,taxes,np.array([1,0,0],bool),np.array([0,1,0],bool),np.array([0,0,1],bool),.08,0.)
    assert np.max(abs(got-(shares*taxes).sum(axis=0)))<1e-9


@pytest.mark.parametrize("demand",[.02,.08,.3])
def test_one_intensity_two_blocks_recover_plain_share(demand):
    w=np.array([[10.],[20.],[30.]])
    wg=np.array([[.2],[4.],[5.]])
    taxes=.5*w
    got,terms=two_block(w,wg,wg/w,taxes,np.array([1,0,0],bool),np.array([0,1,1],bool),np.zeros(3,bool),demand)
    assert np.max(abs(got-wg.sum(axis=0)/w.sum(axis=0)*taxes.sum(axis=0)))<1e-6
    assert np.max(abs(terms["n_release"]+terms["t_release_for_refill"]-.5*wg[1:].sum(axis=0)))<1e-9


def test_native_refill_can_be_negative():
    w=np.array([[10.],[20.]])
    wg=np.array([[1.],[.1]])
    taxes=np.array([[5.],[2.]])
    got,terms=two_block(w,wg,wg/w,taxes,np.array([1,0],bool),np.array([0,1],bool),np.zeros(2,bool),.2)
    assert terms["n_refill_wages"][0]<0
    assert got[0]<((wg/w)*taxes).sum()
