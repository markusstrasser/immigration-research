import numpy as np
import pandas as pd
import pytest

from events import build_events, relation
from benchmark import standardize
from measure import outcomes, cluster_interval


def family(whole_move=False):
    rows=[]
    for p in ['101','102','103']:
        for m in range(1,13):
            moving=(p!='101' or whole_move) and m>=4
            row={'SSUID':'test','PNUM':p,'MONTHCODE':m,'TAGE_EHC':50 if p=='101' else 25,
                 'ESEX':1,'EHISPAN':2,'ERESIDENCEID':'B' if moving else 'A','RIN_UNIV':1,
                 'ERH_BMONTH':4 if moving else 1,'ERH_EMONTH':12 if moving or (p=='101' and not whole_move) else 3,
                 'ARESIDENCEID':1,'ARH_BMONTH':1,'ARH_EMONTH':1,'EEHC_WHY':2,'RMESR':1,
                 'EPNSPOUS_EHC':np.nan,'EPNCOHAB_EHC':np.nan}
            for i in range(1,11):
                row[f'ET2_LNO{i}']=np.nan;row[f'TT2_AGE{i}']=np.nan
            same=[q for q in ['101','102','103'] if q!=p and ((q!='101' or whole_move) and m>=4)==moving]
            for i in range(1,4):
                row[f'RREL_PNUM{i}']=int(same[i-1]) if i<=len(same) else np.nan
                row[f'RREL{i}']=19 if i<=len(same) else np.nan
            rows.append(row)
    return pd.DataFrame(rows)


def test_simultaneous_departures_count_one_stayer_and_allow_later_move():
    d=family()
    # Move the focal person again after departure; do not condition away this response.
    ix=d.PNUM.eq('101')&d.MONTHCODE.ge(5)
    d.loc[ix,['ERESIDENCEID','ERH_BMONTH']]=['C',5]
    d.loc[d.PNUM.eq('101')&d.MONTHCODE.le(4),'ERH_EMONTH']=4
    e,p,a=build_events(d)
    assert len(e)==1 and len(p)==2 and e.iloc[0].n_departing==2
    assert e.iloc[0].later_focal_move and e.iloc[0].persistent


def test_whole_household_move_is_not_a_departure():
    e,p,a=build_events(family(whole_move=True))
    assert e.empty and p.empty


def test_baseline_age_does_not_exclude_post_event_birthday():
    d=family();d.loc[d.PNUM.eq('101'),'TAGE_EHC']=64
    d.loc[d.PNUM.eq('101')&d.MONTHCODE.ge(4),'TAGE_EHC']=65
    assert len(build_events(d)[0])==1


def test_zero_rules_keep_unpaid_hours_unknown_and_negative_earnings():
    d=pd.DataFrame({'RIN_UNIV':[1,1,1,1,2],'RMESR':[8,1,4,1,8],
        'TMWKHRS':[np.nan,np.nan,15,30,np.nan],'AMWKHRS':[0,0,9,9,0],
        'TPEARN_ALT':[np.nan,np.nan,-100,np.nan,np.nan],'APEARN_ALT':[0,0,9,9,0],
        'TPEARN':[np.nan,np.nan,-99,np.nan,np.nan],'APEARN':[0,0,9,9,0],
        'ENJ_UPDWKYN':[2,1,2,2,2],'MONTHCODE':[4]*5})
    for j in range(1,7):
        d[f'EJB{j}_BMONTH']=np.nan;d[f'EJB{j}_EMONTH']=np.nan
    x=outcomes(d)
    assert x.employment.iloc[:4].tolist()==[0,1,1,1]
    assert x.hours.iloc[0]==0 and np.isnan(x.hours.iloc[1])
    assert x.earnings.iloc[0]==0 and x.earnings.iloc[1]==0 and x.earnings.iloc[2]==-100
    assert np.isnan(x.earnings.iloc[3]) and np.isnan(x.earnings.iloc[4])


def test_cluster_resampling_keeps_identical_family_changes_together():
    one=cluster_interval(np.array([1.,-1.]),np.array(['a','b']))
    copies=cluster_interval(np.array([1.,1.,-1.,-1.]),np.array(['a','a','b','b']))
    assert one==copies


def test_missing_relation_column_cannot_corroborate_departure():
    with pytest.raises(AssertionError,match='relationship ID'):
        relation(pd.Series({'RREL_PNUM1':102}),'102')


def test_unsupported_benchmark_is_reported_instead_of_omitted():
    row={'SSUID':'a','PNUM':'101','t':4,'age':40,'sex':1,'children':False,'future_departure':False}
    row.update({f'employment_{m}':1 for m in ['m3','m2','m1','p0','p1','p2']})
    answer=standardize(pd.DataFrame([row]),pd.DataFrame([row]),'employment',False)
    assert len(answer)==2
    assert all(x['status']=='unsupported_no_control_strata' for x in answer)
