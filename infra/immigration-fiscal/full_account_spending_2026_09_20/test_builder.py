import importlib.util
from pathlib import Path
import json
import numpy as np
import pandas as pd
import pytest

P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('spending_builder',P/'builder.py')
b=importlib.util.module_from_spec(spec); spec.loader.exec_module(b)


def test_fixed_attribution_redistributes_and_never_erases_spending():
    average=b.allocate(100,.2,.95)
    fixed=b.allocate(100,.2,.95,fixed=True)
    assert average['target_bn']==19 and fixed['target_bn']==0
    assert fixed['other_household_bn']-average['other_household_bn']==19
    assert sum(average.values())==sum(fixed.values())==100


def test_residual_is_unallocated_not_institutional():
    r=b.allocate(100,.2,.95,represented_cap=30)
    assert r['unallocated_bn']==70 and r['outside_household_bn']==0
    assert r['target_bn']==6 and sum(r.values())==100


def test_foreign_pool_stays_external():
    assert b.allocate(100,.2,.95,external=True)==dict(target_bn=0.,other_household_bn=0.,outside_household_bn=0.,external_bn=100,unallocated_bn=0.)


def test_primary_pin_drift_fails(tmp_path):
    p=tmp_path/'raw.dat'; p.write_bytes(b'original')
    pins={'sources':[{'name':p.name,'sha256':b.sha(p)}]}
    b.verify_primary_pins([p],pins)
    p.write_bytes(b'changed')
    with pytest.raises(ValueError,match='changed'): b.verify_primary_pins([p],pins)


def test_unchanged_school_export_cannot_hide_changed_upstream(tmp_path):
    source=tmp_path/'school_generator.py'; source.write_text('original')
    school=tmp_path/'updated_account_components.csv'; school.write_text('unchanged')
    manifest=tmp_path/'manifest.json'
    manifest.write_text(json.dumps({'inputs':[{'path':str(source),'sha256':b.sha(source)}]}))
    assert source in b.verified_school_dependencies(school)
    source.write_text('changed')
    with pytest.raises(ValueError,match='Stale school upstream'):
        b.verified_school_dependencies(school)


def test_spm_sharing_conserves_every_unit_with_mixed_origin():
    actual=b.equal_unit_share([100,0,30],[1,1,2])
    np.testing.assert_array_equal(actual,[50,50,30])
    assert actual.sum()==130


def test_origin_rule_excludes_broad_foreignborn_selfid():
    d=pd.DataFrame(dict(PRPERTYP=[2,2,2,3],A_AGE=[40]*4,PRCITSHP=[4,1,1,4],
        PENATVTY=[310,57,57,303],PEFNTVTY=[310,303,57,303],PEMNTVTY=[310,57,57,303],PRDTHSP=[1]*4))
    civ,t=b.canonical_target(d)
    np.testing.assert_array_equal(t,[False,True,True,False])


def test_release_complete_partition_and_no_grants_or_capital():
    audit=P/'derived/audit.json'
    if not audit.exists(): pytest.skip('Build release first')
    receipt=json.loads(audit.read_text())
    for name,h in receipt['outputs'].items(): assert b.sha(P/'derived'/f'{name}.csv')==h
    c=pd.read_csv(P/'derived/categories.csv')
    assert abs(c.national_bn.sum()-10061.458)<1e-8
    assert not c.source_cells.str.contains('T31700-A:57|T31700-A:105|T31700-A:134').any()
    r=pd.read_csv(P/'derived/allocations.csv')
    np.testing.assert_allclose(r.target_bn+r.other_bn+r.external_bn+r.unallocated_bn,r.national_bn,atol=1e-8)
    assert np.allclose(r.loc[r.scenario_id.str.startswith('complete'),'unallocated_bn'],0,atol=1e-9)
    fixed=r.loc[r.scenario_id.str.endswith('_F_fixed')&r.category.isin(['defense','general_public_services','domestic_interest'])]
    assert fixed.target_bn.eq(0).all()
