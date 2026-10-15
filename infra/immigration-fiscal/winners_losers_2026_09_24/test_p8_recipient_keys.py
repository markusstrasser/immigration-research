"""Premise tests for P8 health recipients and geographic conservation."""
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest

import p8_recipient_keys as K


FISCAL = Path(__file__).resolve().parent.parent


def test_air_old_share_survives_arbitrary_state_mix():
    d = pd.DataFrame(dict(A_AGE=[0,25,65,85,5,45,70,90], st=[6]*4+[48]*4, other=True))
    w = np.array([3,11,7,5,9,2,13,4], float)
    key, audit = K.air_mortality_key(d, w, FISCAL)
    assert audit["expected_age65_share"] == pytest.approx(2223944.55672 / 2878300.00674)
    # More local exposure in Texas changes geography, never the old-dollar share.
    allocated = key * np.where(d.st.eq(6), 0.2, 0.8)
    old = d.A_AGE.ge(65).to_numpy()
    assert np.dot(w[old], allocated[old]) / np.dot(w, allocated) == pytest.approx(audit["expected_age65_share"], abs=1e-12)
    assert key[0] > 0


def test_crashes_include_children_old_and_pedestrians_and_unknowns():
    d = pd.DataFrame(dict(A_AGE=[3,28,42,70], st=6, other=True))
    w = np.array([2,5,7,3], float)
    victims = pd.DataFrame(dict(AGE=[3,28,42,70,998,999], PER_TYP=[2,1,7,5,5,99]))
    key, audit = K.crash_key_from_victims(d, w, victims)
    assert np.dot(w, key) == pytest.approx(6)
    assert key[0] > 0 and key[-1] > 0
    assert audit["pedestrian_victims"] == 2
    assert audit["roles_without_known_ages"] == [99]
    assert {r["role"] for r in audit["age_role_rows"]} == {1,2,5,7,99}


def test_lineage_thinning_uses_target_state_age_not_national_age_only():
    d = pd.DataFrame(dict(A_AGE=[3,3,8,8,3,3,8,8], st=[6,6,6,6,48,48,48,48],
                          target=[True,False]*4, other=[False,True]*4,
                          PRCITSHP=1, PEMNTVTY=57, PEFNTVTY=57, PRDTHSP=[1,0]*4))
    weights = np.array([30,100,10,100,10,100,50,100], float)
    lineage = dict(counts=dict(added=20,at_g3_rate=20,later_losses=0),
                   age_mix=dict(bands=["0-4","5+"],mixes=dict(g3_rate=[0.5,0.5],later=[0.5,0.5])))
    out, rows = K.lineage_payers_state_age(d,weights,lineage,SimpleNamespace(US_AREAS={57}))
    # National bands each lose 10, placed 75/25 and 1/6 vs 5/6 by case G3+ states.
    assert (weights-out)[1] == pytest.approx(7.5)
    assert (weights-out)[5] == pytest.approx(2.5)
    assert (weights-out)[3] == pytest.approx(10/6)
    assert (weights-out)[7] == pytest.approx(50/6)
    assert out[0::2].tolist() == weights[0::2].tolist()
    assert rows.removed.sum() == pytest.approx(20)


def test_rental_capitalization_reaches_landlords_including_renter_landlords():
    d = pd.DataFrame(dict(other=True, st=[6,6,48,48], H_TENURE=[1,2,1,2],
                          HRNTVAL=[0,100,0,-200], n_other_hh=1))
    w = np.array([2,3,5,7],float)
    raw_ca,raw_tx=np.zeros(1000),np.zeros(1000)
    raw_ca[0],raw_tx[0]=100,200
    I=dict(R_spm=dict(p_other=np.zeros(4)),acs_geo={("central","national_uniform"):dict(value_cell_state={6:raw_ca,48:raw_tx},rent_state={6:40,48:60})})
    B=SimpleNamespace(bins=lambda p,n:np.zeros(len(p),dtype=int))
    key,audit=K.property_key_with_rentals(d,I,B,w,FISCAL)
    assert key[1] > 0 and key[3] > 0
    assert audit["owner_value_key"] == pytest.approx(300)
    assert np.dot(w,key) == pytest.approx(300+audit["rental_value_key"])
    assert audit["state_rental_rows"][0]["rental_value_key"] / audit["rental_value_key"] == pytest.approx(0.4)


def test_landlord_redistribution_preserves_state_dollars_and_sign():
    d=pd.DataFrame(dict(st=[6,6,48,48],other=True,capital=[100,0,0,200]))
    w=np.array([2,3,5,7],float)
    landlords=np.array([0,10,0,-20],float)
    central,broad,_,audit=K.landlord_split_by_state(SimpleNamespace(FISCAL=FISCAL),d,w,landlords)
    for state in [6,48]:
        m=d.st.eq(state).to_numpy()
        for result in [central,broad]:
            assert np.dot(w[m],result[m]) == pytest.approx(np.dot(w[m],landlords[m]),abs=1e-12)
    assert len(audit["state_audit"]) == 2


def test_state_spending_prices_schools_not_group_headcount():
    d=pd.DataFrame(dict(st=[6,6,48,48],A_AGE=[10,40,10,40],target=True,A_ENRLW=0,A_HSCOL=0,MCAID=0))
    weights=np.ones(4)
    shares,audit=K.state_spending_shares(d,weights,[dict(id="education_k12",state_local_bn=100)],FISCAL,"low")
    assert shares[6] > shares[48]
    assert sum(shares.values()) == pytest.approx(1)
    assert sum(r["cost_bn"] for r in audit["programme_state_rows"]) == pytest.approx(100)


def test_missing_jurisdiction_fails_loud():
    d=pd.DataFrame(dict(st=[6],A_AGE=[40],target=True,A_ENRLW=0,A_HSCOL=0,MCAID=0))
    with pytest.raises(ValueError,match="jurisdiction"):
        K.state_spending_shares(d,np.ones(1),[dict(id="general_public_services")],FISCAL,"low")
