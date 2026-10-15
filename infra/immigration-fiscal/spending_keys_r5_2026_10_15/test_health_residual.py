"""Independent numerical contracts for the restricted-payer counterfactual."""
import json
from pathlib import Path

import pandas as pd
import pytest

HERE=Path(__file__).resolve().parent


def load(name):
    return json.loads((HERE/'derived'/name).read_text())


def test_old_source_rebuilt_and_national_mass_conserved():
    a=load('item21.json')
    n=a['national_bn']
    assert n['va_held']+n['residual']==pytest.approx(n['health_services'],abs=1e-9)
    assert a['gates']['old_translation_max_gap_bn']<1e-9
    assert a['gates']['national_row4_max_normalization_gap']<1e-12
    assert a['donor_mass_bn']['TOTVA24']+a['donor_mass_bn']['TOTTRI24']>9*(a['donor_mass_bn']['TOTOFD24']+a['donor_mass_bn']['TOTSTL24'])


def test_old_key_changes_no_population_or_generation():
    a=load('item21.json')['arms']['old_key']['sets']
    for s in a.values():
        for conv in s['by_generation'].values():
            for e in conv.values():
                assert all(abs(p['delta_bn'])<1e-9 for p in e['parts'])
        for i in s['count_interactions'].values():
            assert all(abs(e['total_bn'])<1e-9 for e in i['by_end'].values())


def test_conventions_cash_population_and_capital_close():
    a=load('item21.json')
    for arm in a['arms'].values():
        assert arm['sets']['set']==arm['sets']['cash']
        for end in ['low','high']:
            source=arm['sets']['set']
            assert source['by_generation']['a'][end]['total_bn']==pytest.approx(source['by_generation']['b'][end]['total_bn'],abs=1e-9)
            rows=source['by_end'][end]['parts']
            assert {p['population'] for p in rows}=={'original_union','added_lineage','completion','coverage'}
            assert sum(p['delta_bn'] for p in rows)==pytest.approx(source['by_end'][end]['total_bn'],abs=1e-9)
            for p in rows:
                assert p['after_bn']-p['before_bn']==pytest.approx(p['delta_bn'],abs=1e-9)
                if p.get('source_side',p.get('side'))=='capital':
                    assert p['source_line']=='health_sl'
                    assert p['delta_bn']==pytest.approx(p['capital_stock_delta_bn']*a['rates'][end],abs=1e-9)


def test_white_profile_held_and_foreign_ratio_cells_not_overwritten():
    a=load('item21.json')
    rows=a['arms']['central']['sets']['set']['by_end']['low']['parts']
    assert all(p['delta_bn']==0 for p in rows if p.get('profile')=='lineage_g3_rate_white')
    ratios=pd.read_csv(HERE/'derived/item21_ratios.csv')
    assert len(ratios)==20
    assert set(ratios.nativity)=={'us_born','foreign_born'}
    # Aggregate 'both' cells must never overwrite the transport foreign-born cell.
    assert ratios.query("spec=='winsor_p995' and nativity=='foreign_born' and band=='0-17'").iloc[0].ratio==pytest.approx(.4719915927423518,abs=1e-12)


def test_reported_group_shares_include_coverage_and_fixed_fee_dollars():
    s=pd.read_csv(HERE/'derived/item21_shares.csv')
    old=s.query("arm=='old_key'")
    assert .065<old.old_share.sum()<.067
    assert list(old.old_share)==list(old.new_share)
    assert 'coverage' in set(old.population)


def test_common_rate_coverage_and_counts_are_explicit_and_old_key_zero():
    a=load('item21_v9_coverage.json')
    source=load('item21_coverage.json')
    rate=load('item21.json')['v9_capital_rate']
    assert a['capital_rate']==rate
    for name,arm in a['arms'].items():
        for end,sr in [('low',.02),('high',.03)]:
            rows=source['arms'][name]['sets']['set']['ends'][end]['decomposition']['line_parts']
            expected=sum(q['coverage_bn']*(rate/sr if q['economic_class']=='capital_return' else 1) for q in rows)
            assert arm['sets']['set']['ends'][end]['total_bn']==pytest.approx(expected,abs=1e-9)
        assert arm['sets']['cash']==arm['sets']['set']
    for s in a['arms']['old_key']['sets'].values():
        assert all(e['total_bn']==0 for e in s['ends'].values())
        assert all(e['total_bn']==0 for v in s['item_overrides'].values() for e in v['by_end'].values())


def test_csv_keeps_capital_only_metadata_and_lf(tmp_path):
    import health_residual as H
    path=tmp_path/'parts.csv'
    H.write_csv(path,[{'line':'health','change_bn':1.},
                      {'line':'health_sl','change_bn':2.,'capital_rate':.021,'source_capital_rate':.02}])
    assert b'\r' not in path.read_bytes()
    rows=pd.read_csv(path)
    assert rows.iloc[1].capital_rate==.021
    assert rows.iloc[1].source_capital_rate==.02
