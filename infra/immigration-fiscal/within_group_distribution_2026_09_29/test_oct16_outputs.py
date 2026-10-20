"""Independently reconcile published oct16 allocations to principal case bands."""
import json
from pathlib import Path

import pandas as pd
import pytest

HERE=Path(__file__).resolve().parent


@pytest.fixture(params=[(a,b,s) for a in ('personal','shared') for b in ('set','cash')
                       for s in ('','_person_accrual','_person_onbooks')])
def output(request):
    allocation,basis,suffix=request.param
    sub=Path('oct16')/('shared_allocation' if allocation=='shared' else '')/('cash' if basis=='cash' else '')
    return allocation,basis,suffix,HERE/'derived'/sub,HERE/'_cache'/sub


def test_public_allocation_closes_against_principal_case_and_separate_missed_people(output):
    allocation,basis,suffix,directory,cache=output
    controls=json.loads((directory/('controls'+suffix+'.json')).read_text())
    bands=pd.read_csv(HERE.parent/'main_case_2026_10_16/derived/main_case_bands.csv')
    variant=('shared_allocation' if basis=='set' else 'shared_allocation_cash_set') if allocation=='shared' else ('adopted' if basis=='set' else 'cash_set')
    row=bands.query("profile=='long_run_non_school_full' and variant==@variant").iloc[0]
    for end in ('low','high'):
        whole=next(r for r in controls['gates'] if r['end']==end and 'generation' not in r)
        assert abs(whole['actual_bn']-row['cost_'+end+'_bn'])<1e-4
        assert all(abs(r['gap_bn'])<1e-9 for r in controls['gates'] if r['end']==end)
    missed=pd.read_csv(directory/('people_survey_misses'+suffix+'.csv'))
    assert not missed.observed_household.any()
    assert 'PH_SEQ' not in missed
    assert abs(missed.query("end=='low'").net_missing_people.sum()-(controls['population']['with_coverage']-controls['population']['without_coverage']))<1e-5


def test_member_share_and_dollar_conservation_use_actual_calibrated_person_aggregates(output):
    allocation,basis,suffix,directory,cache=output
    households=pd.read_parquet(cache/('households'+suffix+'.parquet'))
    shares=pd.read_csv(directory/('net_positive_shares'+suffix+'.csv')).query("breakdown=='all' and cell=='all'").set_index(['convention','end'])
    concentration=pd.read_csv(directory/('concentration'+suffix+'.csv')).set_index(['convention','end','statistic'])
    for convention in ('A','B'):
        for end in ('low','high'):
            negative=households[f'{convention}_{end}_household_cost_usd']<0
            observed=households.loc[negative,'calibrated_members'].sum()/households.calibrated_members.sum()
            assert abs(observed-shares.loc[(convention,end),'share_members_net_positive'])<1e-10
            actual=households[f'{convention}_{end}_weighted_cost_usd'].sum()/1e9
            expected=concentration.loc[(convention,end,'total_bn'),'value']
            assert abs(actual-expected)<1e-8
