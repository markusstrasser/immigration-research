"""V8 financing cannot be inferred from resource dollars or carrier storage."""
from __future__ import annotations

import importlib.util
from pathlib import Path
from types import SimpleNamespace
import hashlib

import pandas as pd
import pytest

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('v8_current_flow',HERE/'v8_flow.py')
flow=importlib.util.module_from_spec(spec)
spec.loader.exec_module(flow)


def test_unadopted_case_is_blocked(tmp_path):
    import json
    (tmp_path/'live_case.json').write_text(json.dumps({'key':'oct15','adopted':'2026-10-15'}))
    source=tmp_path/'main_case_2026_10_15/derived'
    source.mkdir(parents=True)
    (source/'summary.json').write_text(json.dumps({'v8':{'status':'candidate'}}))
    with pytest.raises(ValueError,match='not adopted'):
        flow.require_adopted(tmp_path)


def test_composite_and_unidentified_source_payers_remain_unlocated():
    d=SimpleNamespace(LAST=2024,LONG_RUN_LINES=('roads',),ENTERPRISE_RECEIPT='enterprise')
    shares={'central':pd.DataFrame({'federal_tax':[1.0],'state_tax':[0.0],
                                   'general_public_services':[.4],'roads':[.2]},index=[2024])}
    corner={'capped':[]}
    for parent in ('unidentified','general_public_services','roads'):
        assert flow.source_row(d,corner,{'side':'spending','parent_line':parent},10.0,shares,'central') is None


def test_signed_receipt_storage_keeps_economic_government():
    d=SimpleNamespace(LAST=2024,LONG_RUN_LINES=(),ENTERPRISE_RECEIPT='enterprise')
    shares={'central':pd.DataFrame({'federal_tax':[1.0],'state_tax':[0.0]},index=[2024])}
    corner={'capped':[]}
    federal=flow.source_row(d,corner,{'side':'receipt','parent_line':'federal_tax'},-10.0,shares,'central')
    state=flow.source_row(d,corner,{'side':'receipt','parent_line':'state_tax'},-10.0,shares,'central')
    assert federal=={'federal_bn':-10.0,'state_local_bn':0.0,'financing':'cash'}
    assert state=={'federal_bn':0.0,'state_local_bn':-10.0,'financing':'cash'}


def test_composite_payer_uses_the_executed_source_split_when_available():
    d=SimpleNamespace(LAST=2024,LONG_RUN_LINES=(),ENTERPRISE_RECEIPT='enterprise')
    shares={'central':pd.DataFrame({'general_public_services':[.4]},index=[2024])}
    executed={('spending','general_public_services'):dict(responsive_bn=10.0,federal_bn=8.0,financing='cash')}
    row=flow.source_row(d,{'capped':[]},{'side':'spending','parent_line':'general_public_services'},
                        5.0,shares,'central',executed)
    assert row['federal_bn']==4.0 and row['state_local_bn']==1.0
    assert row['assumption'].startswith('source-line current payer ratio')


def test_rationed_program_remains_displacement():
    d=SimpleNamespace(LAST=2024,LONG_RUN_LINES=(),ENTERPRISE_RECEIPT='enterprise')
    shares={'central':pd.DataFrame({'housing':[1.0]},index=[2024])}
    result=flow.source_row(d,{'capped':['housing']},{'side':'spending','parent_line':'housing'},5.0,shares,'central')
    assert result['financing']=='displaced_beneficiaries'


def test_accrued_promises_stay_out_of_cash():
    common=dict(end='low',convention='central',side='spending',id='social_security',
                state_local_bn=0.0,financing='cash')
    set_row=dict(common,basis='set',responsive_bn=20.0,federal_bn=20.0,union_bn=18.0,lineage_bn=2.0)
    cash_row=dict(common,basis='cash',responsive_bn=8.0,federal_bn=8.0,union_bn=7.0,lineage_bn=1.0)
    result=flow.separate_timing([set_row,cash_row])
    costs={r['financing']:r['responsive_bn'] for r in result if r['basis']=='set'}
    assert costs=={'cash':8.0,'pension_accrual':12.0}
    accrual=next(r for r in result if r['financing']=='pension_accrual')
    assert accrual['union_bn']==11.0 and accrual['lineage_bn']==1.0


def test_mixed_composites_remain_unlocated_after_declared_components(tmp_path):
    components=['M1_federal','M2_state','M3_refunds','D_added_residual','M5_owner_property','M5_housing_key']
    rows=[dict(method='set',end=end,component=component,generation=g,r0=.1)
          for end in ('low','high') for component in components for g in ('G1','G2','G3+')]
    path=tmp_path/'replicates.csv'
    pd.DataFrame(rows).to_csv(path,index=False,lineterminator='\n')
    payload={'meta':{'mixed_unit_removal':{'source':{'files':{'replicates':
              {'path':'replicates.csv','sha256':hashlib.sha256(path.read_bytes()).hexdigest()}}},
              'D_scaling':{'scale':2},'by_end':{e:{'total_bn':3.0,'D_added_residual_bn':.6}
              for e in ('low','high')}}}}
    result=flow.mixed_source(SimpleNamespace(ROOT=tmp_path),payload,'set')['low']
    by={r['component']:r for r in result}
    assert by['D_added_residual']['federal_bn']==pytest.approx(.6)
    assert by['M5_housing_key']['financing']=='displaced_beneficiaries'
    residual=by['bounded_composites_unlocated']
    assert residual['responsive_bn']==pytest.approx(.9)
    assert residual['federal_bn'] is None and residual['state_local_bn'] is None
    path.write_text('corrupted')
    with pytest.raises(ValueError,match='component source hash changed'):
        flow.mixed_source(SimpleNamespace(ROOT=tmp_path),payload,'set')


def test_inserted_coverage_accrual_piece_does_not_shift_cash_matching():
    def row(basis,piece,line,value):
        return dict(basis=basis,piece=piece,end='low',convention='central',side='coverage',
                    id=line,generation='G1',source_line=line,source_side='receipt',
                    financing='cash',responsive_bn=value,federal_bn=value,state_local_bn=0.0,
                    union_bn=value,lineage_bn=0.0)
    rows=[row('set',0,'federal_income_tax',8.0),row('set',1,'federal_income_tax',2.0),
          row('set',2,'other_domestic_social_contributions',4.0),
          row('cash',0,'federal_income_tax',8.0),row('cash',1,'other_domestic_social_contributions',4.0)]
    result=flow.separate_timing(flow.coalesce_coverage(rows))
    accrued=[r for r in result if r['financing']=='pension_accrual']
    assert len(accrued)==1 and accrued[0]['responsive_bn']==2.0
    assert not any(r['financing']=='unlocated' for r in result)
