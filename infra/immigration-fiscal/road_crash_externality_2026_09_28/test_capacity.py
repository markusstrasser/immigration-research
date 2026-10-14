import importlib.util
import json
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('capacity_test', HERE / 'capacity_response.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def central(crash, liability):
    levels = {**crash.FACTORS, **crash.x_levels_evidence(), 'r_nf': crash.ccrs_nonfatal_or()}
    p = {k: values[1] for k, values in levels.items()}
    p['liab'] = liability
    result = crash.evaluate_split(*[p[k] for k in crash.FACTORS], r_nf=p['r_nf'], composition=True)
    return p, result, C.density_parts(crash, p, result)


def test_mortality_identity_nonfatal_and_liability_hold():
    crash = C.load_crash()
    gross, _ = C.mortality_base(crash, 13.7e6)
    deltas = []
    for liability in crash.FACTORS['liab']:
        p, result, density = central(crash, liability)
        identity, identical_density = C.reprice_mortality(crash, p, result, density, gross, dict.fromkeys(gross, 1.0))
        assert identity == result and identical_density == density
        changed, changed_density = C.reprice_mortality(crash, p, result, density, gross, dict.fromkeys(gross, .7))
        assert changed['mv_nonfatal'] == result['mv_nonfatal']
        assert changed_density['nm_nonfatal'] == density['nm_nonfatal']
        assert sum(changed[k] for k in ('mv_fatal', 'mv_nonfatal', 'nonmotorist', 'single_vehicle')) == pytest.approx(changed['total'], abs=1e-9)
        deltas.append(changed['total'] - result['total'])
    # Financial liability affects the base but is never multiplied by VSLY.
    assert max(deltas)-min(deltas) < 1e-9


def test_signed_capacity_and_missing_age_source_contract():
    assert C.residual_share(.1, 0) == pytest.approx(.1)
    assert C.residual_share(.1, .1) == 0
    assert C.residual_share(.1, .2) < 0
    document = json.loads((HERE/'derived/fars_mortality_2023.json').read_text())
    assert set(document['profiles']) == {'mv_fatal', 'nm_fatal', 'sv_fatal'}
    assert 'passengers PER_TYP 2' in document['classes']
    for profile in document['profiles'].values():
        assert sum(profile['age_counts'].values()) == profile['known_age_records']
        assert profile['known_age_records'] + profile['missing_age_records'] == profile['all_records']
        for rate in ('0', '0.03'):
            r = profile['rates'][rate]
            assert r['missing_age_low_years'] <= r['remaining_years'] <= r['missing_age_high_years']


def test_output_basis_complete_without_uniform_fallback():
    rows = C.read_csv(HERE/'derived/capacity_items_oct15.csv')
    expected = {(v,r,e,a,p) for v,r in [('dot_uniform','0'),('dot_life_years','0'),('dot_life_years','0.03')]
                for e in ('low','high') for a in ('multivehicle_only','all_density') for p in ('union','lineage_gross','lineage')}
    assert {(r['valuation'],r['real_discount_rate'],r['end'],r['arm'],r['population']) for r in rows} == expected
    assert len(rows) == len(expected)
    for row in rows:
        assert float(row['central_bn'])-float(row['before_live_key_central_bn']) == pytest.approx(float(row['live_key_delta_bn']), abs=1e-9)
        if row['valuation'] == 'dot_life_years':
            assert abs(float(row['mortality_only_delta_bn'])) > 1e-6


def test_full_replacement_delta_uses_uniform_fixed_network_baseline():
    rows = C.read_csv(HERE/'derived/capacity_items_oct15.csv')
    uniform = {(r['end'], r['arm'], r['population']): r for r in rows if r['valuation']=='dot_uniform'}
    for row in rows:
        base = uniform[row['end'], row['arm'], row['population']]
        # Recover the original uniform gross receiver boundary from its published
        # replacement. All life-year arms must remove that same original row.
        old = float(base['central_bn'])-float(base['change_from_gross_live_bn'])
        assert old+float(row['change_from_gross_live_bn']) == pytest.approx(float(row['central_bn']), abs=1e-9)
