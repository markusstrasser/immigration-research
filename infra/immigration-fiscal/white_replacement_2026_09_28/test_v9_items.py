"""Own-key v9 contract and native count/mortality guards."""
from types import SimpleNamespace
import copy
import numpy as np
import pytest
import v9_items as V


def test_native_factors_join_person_ids_across_different_row_order():
    import pandas as pd
    roster=pd.DataFrame(dict(PH_SEQ=[2,1,1],PPPOS=[1,2,1]))
    factors=pd.DataFrame(dict(PH_SEQ=[1,1,2],PPPOS=[1,2,1],central_member_factor=[.9,.8,1.]))
    assert V.aligned_factors(roster,factors).tolist()==[1.,.8,.9]
    with pytest.raises(SystemExit,match='lacks comparator person ID'):
        V.aligned_factors(roster,factors.iloc[:2])
    with pytest.raises(SystemExit,match='not unique'):
        V.aligned_factors(roster,pd.concat([factors,factors.iloc[:1]]))


def test_basket_vectors_join_person_ids_and_block_missing_duplicate_age():
    import pandas as pd
    roster=pd.DataFrame(dict(PH_SEQ=[2,1,1],PPPOS=[1,2,1],A_AGE=[10,20,30]))
    basket=dict(ph_seq=np.array([1,2,1]),pppos=np.array([1,1,2]),age=np.array([30,10,20]))
    assert V.basket_indexer(roster,basket).tolist()==[1,2,0]
    with pytest.raises(SystemExit,match='matching comparator'):
        V.basket_indexer(roster,{k:v[:2] for k,v in basket.items()})
    with pytest.raises(SystemExit,match='not unique'):
        V.basket_indexer(roster,{k:np.append(v,v[0]) for k,v in basket.items()})
    with pytest.raises(SystemExit,match='matching comparator'):
        V.basket_indexer(roster,dict(basket,age=np.array([31,10,20])))


def test_adoption_guard_uses_live_declaration_and_rejects_stale_stamp():
    import json
    import check_dumps_oct14 as D
    meta=json.loads((V.FISCAL/'main_case_2026_10_16/derived/corrections.json').read_text())['meta']
    D.require_adopted(meta)
    with pytest.raises(SystemExit,match='adopted live'):
        D.require_adopted(dict(meta,adopted='2026-10-16'))
    with pytest.raises(SystemExit,match='adopted live'):
        D.require_adopted(dict(meta,status='candidate: main case v9'))


def test_active_mixed_unit_callers_name_their_case():
    import ast
    files=[p for lane in (V.HERE,V.FISCAL/'black_comparator_rough_2026_09_28')
           for p in lane.glob('*.py') if not p.name.startswith('test_')]
    missing=[]
    for path in files:
        for node in ast.walk(ast.parse(path.read_text())):
            if not isinstance(node,ast.Call):
                continue
            name=node.func.id if isinstance(node.func,ast.Name) else node.func.attr if isinstance(node.func,ast.Attribute) else ''
            if name=='load_mixed_unit' and not any(k.arg=='case' for k in node.keywords):
                missing.append(f'{path.name}:{node.lineno}')
    assert not missing, missing


def test_capital_rate_and_college_response_compose_without_double_count():
    W=SimpleNamespace(META={'one_rate':{'flat_real_equivalent':.020810698764}})
    components=[('college',10.),('college_user_fees',-2.),('roads',12.)]
    total,parts=V.capital(W,components,.03)
    response=V.source()[15]['central_response']
    assert total==pytest.approx((12.+8.*response)*.020810698764/.03,abs=1e-12)
    assert sum(p['delta_bn'] for p in parts)==pytest.approx(total-20.,abs=1e-12)
    assert parts[0]['kind']=='college_capital'
    assert parts[1]['kind']=='capital_rate_including_15x20'


def test_v9_count_standardization_does_not_reuse_old_lineage_paired_se():
    import comparison_contract as C
    source=C.load_mixed_unit(case='oct16')
    current=44_903_074.086245224
    term=C.comparator_removal(source,'A1_third_plus_nh_white','accrual','low',current)
    assert term['paired_se_bn'] is None
    assert term['comparator_se_bn']>0
    own=C.comparator_removal(source,'A1_third_plus_nh_white','accrual','low',term['own_count'])
    assert own['paired_se_bn'] is None
    assert term['bn']/current==pytest.approx(own['bn']/own['own_count'],abs=1e-15)
    historical=copy.copy(source)
    historical['comparison_case']='oct15'
    with pytest.raises(SystemExit,match='population differs'):
        C.comparator_removal(historical,'A1_third_plus_nh_white','accrual','low',current)


def test_v9_count_standardization_keeps_source_and_population_stops():
    import comparison_contract as C
    source=C.load_mixed_unit(case='oct16')
    for bad in (0.,-1.,float('nan')):
        with pytest.raises(SystemExit,match='positive finite count'):
            C.comparator_removal(source,'A1_third_plus_nh_white','accrual','low',bad)
    for frame in ('own_count','lineage_count'):
        tampered=copy.deepcopy(source)
        for row in tampered['gaps']:
            if (row['group'],row['method'],row['end'],row['population_basis'])==(C.registered('A1_third_plus_nh_white')[1],'set','low',frame):
                row['comparator_adjustment_bn']=str(float(row['comparator_adjustment_bn'])+1e-6)
        own=C.comparator_removal(source,'A1_third_plus_nh_white','accrual','low',1e6)['own_count']
        population=own if frame=='own_count' else 44_903_074.086245224
        with pytest.raises(SystemExit,match='own-count standardization mismatch'):
            C.comparator_removal(tampered,'A1_third_plus_nh_white','accrual','low',population)


def test_symmetric_selects_live_case_before_loading_survivor_contract(monkeypatch):
    import symmetric_comparators_oct14 as S
    monkeypatch.setattr(S.W, 'CASE', 'sept29')
    monkeypatch.setattr(S.W, 'use_case', lambda case: setattr(S.W, 'CASE', case))
    monkeypatch.setattr(S, 'check_pins', lambda pin: {})

    def inspect_source(*, case):
        assert case == 'oct16'
        raise RuntimeError('live source selected')

    monkeypatch.setattr(S.CC, 'load_mixed_unit', inspect_source)
    with pytest.raises(RuntimeError, match='live source selected'):
        S.main()


def test_all_comparator_own_parts_close_and_have_no_origin_calibration():
    import pandas as pd
    path=V.HERE/'derived/v9_item_changes_oct16.csv'
    if not path.exists():
        pytest.skip('final adopted oct16 output is not published')
    rows=pd.read_csv(path)
    for (_,_,_),group in rows.groupby(['group','basis','end']):
        own=group[group.item.astype(str).isin(['13','14','15','18','20','21'])]
        assert set(own.item.astype(str))=={'13','14','15','18','20','21'}
        assert group.iloc[0].own_after_bn-group.iloc[0].own_before_bn==pytest.approx(own.own_change_bn.sum(),abs=1e-9)
        assert not own[own.item.astype(str).isin(['16','17'])].shape[0]


def test_health_capital_post_is_classified_as_resource_at_live_rate():
    import json
    payload=json.loads((V.FISCAL/'main_case_2026_10_16/derived/corrections.json').read_text())['meta']
    dump=json.loads((V.HERE/'derived/engine_lines_oct16.json').read_text())
    for end in ('low','high'):
        classified=dump[end]['v9_classified']
        actual=sum(p['value_bn'] for p in classified['parts'] if p['origin']=='21')
        expected=sum(p['capital_stock_delta_bn'] for p in payload['health_residual_key']['by_end'][end]['parts']
                     if p.get('side')=='capital' and p['population']!='coverage')*payload['one_rate']['flat_real_equivalent']
        assert expected>0
        assert actual==pytest.approx(expected,abs=1e-9)
        assert classified['capital_bn']==pytest.approx(sum(p['value_bn'] for p in classified['parts']
                                                         if p['economic_class']=='capital_return'),abs=1e-9)
