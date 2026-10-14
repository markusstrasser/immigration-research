"""Independent unified-accounting, replicate and scenario-selection checks."""
import importlib.util
import json
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

LANE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tested_round2',LANE/'round2.py')
M=importlib.util.module_from_spec(spec);spec.loader.exec_module(M)


def test_diagnostic_SNAP_parts_cannot_be_selected_as_complete_arms():
    values={key:np.full((3,161),i) for i,key in enumerate(M.SNAP_FULL_ARMS)}
    values['SNAP_zero_observed_newly_eligible_low']=np.full((3,161),-999.)
    values['SNAP_cap_observed_newly_ineligible']=np.full((3,161),999.)
    selected=M.full_snap_arms(values)
    assert len(selected)==4
    assert min(v[0,0] for v in selected.values())==0
    assert max(v[0,0] for v in selected.values())==3
    with pytest.raises(ValueError,match='complete SNAP arms missing'):
        M.full_snap_arms({'SNAP_zero_observed_newly_eligible_low':np.zeros((3,161))})


def test_round2_SEs_match_160_replicates_and_case_offsets():
    summary=json.loads((LANE/'derived/round2_summary.json').read_text())
    frame=pd.read_csv(LANE/'derived/round2_replicates.csv').set_index(['method','end','component','generation']).sort_index()
    cols=[f'r{r}' for r in range(161)]
    case=json.loads((LANE/'derived/case_inputs.json').read_text())
    for row in summary['results']:
        values=frame.loc[(row['method'],row['end'],row['component']),cols].to_numpy(float)
        assert values.shape==(3,161)
        total=values.sum(axis=0)
        assert total[0]==pytest.approx(row['bn'],abs=1e-9)
        assert np.sqrt(4/160*np.square(total[1:]-total[0]).sum())==pytest.approx(row['se_bn'],abs=1e-9)
        if 'case_total_bn' in row:
            assert row['case_total_bn']==pytest.approx(case['bands'][row['method']][('low','high').index(row['end'])]+total[0],abs=1e-9)


def test_unified_stack_uses_full_SNAP_once_and_preserves_covariance():
    summary=json.loads((LANE/'derived/round2_summary.json').read_text())
    frame=pd.read_csv(LANE/'derived/round2_replicates.csv').set_index(['method','end','component','generation']).sort_index()
    cols=[f'r{r}' for r in range(161)]
    get=lambda method,end,name:frame.loc[(method,end,name),cols].to_numpy(float)
    components=('M1_federal','M2_state','M3_refunds','M6_biological_children','D_added_residual',
                'M5_consumption','M5_owner_property','M5_housing_key')
    for row in summary['results']:
        if row['component'] not in ('bounded_low','bounded_high'): continue
        h,a,s=row['arm'].split('|')
        assert s in M.SNAP_FULL_ARMS
        expected=sum(get(row['method'],row['end'],k) for k in components)
        expected+=get('diagnostic','low','health_latent_'+h)+get('diagnostic','low','health_latent_'+a)
        expected+=get('diagnostic','low','SNAP_latent_'+s)
        actual=get(row['method'],row['end'],row['component'])
        np.testing.assert_allclose(actual,expected,rtol=0,atol=1e-9)
        np.testing.assert_allclose(get(row['method'],row['end'],'M5_SNAP_key')+
                                   get(row['method'],row['end'],'M4_SNAP_baseline_interaction'),0,rtol=0,atol=1e-9)


def test_priced_population_and_projection_are_not_added_twice():
    summary=json.loads((LANE/'derived/round2_summary.json').read_text())
    members=summary['membership']
    case=json.loads((LANE/'derived/case_inputs.json').read_text())
    assert members['existing_addition_count_unchanged']==pytest.approx(case['lineage']['counts']['added'],abs=1e-6)
    total=sum(members[k] for k in ('roster_g3_priced_count','roster_white_priced_count',
                                  'remaining_added_g3_priced_count','remaining_added_white_priced_count'))
    assert total==pytest.approx(case['lineage']['counts']['added'],abs=1e-6)
    assert members['no_new_population_or_own_cost']
    assert summary['resource_keys']['artifact_admitted_bn']==0
    assert len(summary['resource_keys']['conservation'])==4
    assert all(v['columns']==161 and v['max_group_gap_bn']<1e-6 for v in summary['resource_keys']['conservation'].values())
