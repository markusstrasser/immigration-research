"""Parent-routing scientific contracts for the independent v8 measurement."""
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np
import pandas as pd
import pytest
import measure_minor_parents_v8 as M


def test_exact_b_halves_outside_parent_and_oldest_relative():
    d = pd.DataFrame(dict(PH_SEQ=[1]*6, A_LINENO=range(1, 7), PF_SEQ=[1]*6,
                          A_AGE=[40, 40, 39, 12, 13, 14], PEPAR1=[0,0,0,2,1,0],
                          PEPAR2=[0,0,0,3,0,0]))
    gens = {g: np.zeros(6, bool) for g in M.GENS}
    gens["G2"][1] = True
    gens["G3plus"][2] = True
    union = gens["G2"] | gens["G3plus"]
    added = np.array([False,False,False,True,True,True])
    _, _, omega, rules, _ = M.expanded_assignments(d, np.ones(6, bool), union, gens, added)
    assert np.array_equal(omega["b"][3], [0, .5, .5])
    assert rules[3] == "parents_two_generations"
    assert np.array_equal(omega["b"][4], [0, 0, 1])
    assert rules[4] == "parents_outside_union_own"
    assert np.array_equal(omega["b"][5], [0, 1, 0])
    assert rules[5] == "oldest_union_relative"


def test_sdr_requires_all_160_replicates():
    values = np.r_[2., np.full(160, 3.)]
    assert M.sdr(values) == 2
    with pytest.raises(ValueError, match="160 finite"):
        M.sdr(values[:-1])
    values[-1] = np.nan
    with pytest.raises(ValueError, match="160 finite"):
        M.sdr(values)


def test_weighted_equivalents_keep_half_shares_in_every_replicate():
    weights = np.arange(2*161, dtype=float).reshape(2,161)
    assert np.array_equal(M.weighted(np.ones(2,bool), weights, np.array([.5,1.])),
                          .5*weights[0]+weights[1])


@pytest.mark.parametrize("linked,cause,movement",[(True,"newly_included_parent",.5),
    (False,"newly_included_oldest_union_relative",1.)])
def test_new_member_can_change_existing_minor_assignment(linked,cause,movement):
    d = pd.DataFrame(dict(PH_SEQ=[1,1,1],PPPOS=[1,2,3],A_LINENO=[1,2,3],PF_SEQ=[1,1,1],
                          A_AGE=[40,70,14],PEPAR1=[0,0,1 if linked else 0],
                          PEPAR2=[0,0,2 if linked else 0],PEPAR1TYP=[0,0,1],PEPAR2TYP=[0,0,1]))
    gens = {g:np.zeros(3,bool) for g in M.GENS}
    gens["G1"][0] = True
    gens["G2"][2] = True
    union = gens["G1"] | gens["G2"]
    reporters = np.array([False,True,False])
    civilian = np.ones(3,bool)
    old,rules,parents = M.F.assignments(d,civilian,union,gens)
    completed,cgens,new,nrules,_ = M.expanded_assignments(d,civilian,union,gens,reporters)
    out = M.completed_assignment_trace(d,union,gens,old,rules,completed,cgens,new,nrules,
                                       parents,reporters,np.zeros(3,bool),np.ones((3,161)))
    rows = out["existing_union_assignment_changes"]
    assert len(rows)==1 and rows[0]["PPPOS"]==3 and rows[0]["cause"]==cause
    delta = out["completed_assignment_effects"]["existing_union_delta_people"]
    assert delta["G1"]["replicates"]==[-movement]*161
    assert delta["G3plus"]["replicates"]==[movement]*161
    assert out["reporter_assignment_b"][0]["omega"]==[0.,0.,1.]
    propagated,prules = M.propagated_assignment(union,old,rules,new,nrules)
    assert np.array_equal(propagated["b"][union],old["b"][union])
    assert np.array_equal(propagated["b"][~union],new["b"][~union])
    assert np.array_equal(prules[union],rules[union])
