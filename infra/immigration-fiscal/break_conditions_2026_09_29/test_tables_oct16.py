"""Live v9 evidence, response-only controls, and fail-loud drift behavior."""
import importlib.util
import json
import math
import os
import subprocess
from pathlib import Path
import pytest

def test_v9_generation_preflight_rejects_missing_dynamic_post_route():
    script = """
const {validateGenerationPayloads}=require(process.argv[1]);
const block={by_end:{low:{total_bn:0},high:{total_bn:0}}};
const gp=Object.fromEntries(['a','b'].map(c=>[c,Object.fromEntries(['G1','G2','G3plus'].map(g=>[g,{meta:{generation:g,case_key:'oct16',adopted:'2026-10-16',mixed_unit_removal:block,coverage:block}}]))]));
try {validateGenerationPayloads(gp,{adopted:'2026-10-16'},'oct16'); process.exit(2);}
catch(e) {console.error(e.message); process.exit(1);}
"""
    result = subprocess.run(['node', '-e', script, str(Path(__file__).resolve().parent / 'generation_preflight.cjs')], capture_output=True, text=True)
    assert result.returncode == 1
    assert '[BLOCKED] oct16 generation preflight: missing v9 per-spec post routing' in result.stderr


def test_adoption_uses_live_declaration_and_rejects_stale_payload(tmp_path, monkeypatch):
    (tmp_path / 'live_case.json').write_text(json.dumps({'key': 'oct16', 'lane': 'main_case_2026_10_16', 'adopted': '2026-10-20'}))
    monkeypatch.setattr(tables, 'F', tmp_path)
    payload = {'meta': {'adopted': '2026-10-20', 'status': 'adopted: main case v9'}}
    tables.require_adopted_payload(payload)
    payload['meta']['adopted'] = '2026-10-16'
    with pytest.raises(SystemExit, match='adoption differs'):
        tables.require_adopted_payload(payload)


def test_v9_generation_coverage_requires_old_plus_reprice_once():
    script = """
const {validateGenerationPayloads}=require(process.argv[1]);
const block=(lo,hi)=>({by_end:{low:{total_bn:lo},high:{total_bn:hi}}});
const specs=[{allocation:'personal',reading:'low'},{allocation:'personal',reading:'high'}];
const gp=Object.fromEntries(['a','b'].map(c=>[c,Object.fromEntries(['G1','G2','G3plus'].map(g=>[g,{meta:{generation:g,case_key:'oct16',adopted:'2026-10-16',mixed_unit_removal:block(1,2),coverage:block(1,2),v9_specs:specs,v9_posts_by_spec:[{coverage_repricing:1},{coverage_repricing:2}]}}]))]));
const full={adopted:'2026-10-16',mixed_unit_removal:block(3,6),coverage:block(6,12)};
validateGenerationPayloads(gp,full,'oct16');
gp.a.G1.meta.v9_posts_by_spec[0].coverage_repricing=2;
try {validateGenerationPayloads(gp,full,'oct16'); process.exit(2);}
catch(e) {console.error(e.message); process.exit(1);}
"""
    result = subprocess.run(['node', '-e', script, str(Path(__file__).resolve().parent / 'generation_preflight.cjs')], capture_output=True, text=True)
    assert result.returncode == 1
    assert '[BLOCKED] oct16 generation preflight: unclosed coverage' in result.stderr


def test_generation_replay_requires_exact_inputs_and_outputs(tmp_path):
    script = r"""
const {validateReproducedSource,validateGenerationPayloads}=require(process.argv[1]);
const hash=require('crypto').createHash('sha256').update('same').digest('hex');
const outputs=Object.fromEntries(['oct16','oct16_cash'].flatMap(key=>['results','summary','corrections'].map(kind=>
 [`generation_account_2026_09_24/derived/generation_${kind}_${key}.${kind==='results'?'csv':'json'}`,hash])));
const producer='generation_account_2026_09_24/run_generations_v9.cjs';
const inputs=Object.fromEntries([producer,'main_case_2026_10_16/package.cjs','main_case_2026_10_16/derived/corrections.json','main_case_2026_10_16/derived/corrections_cash.json'].map(p=>[p,hash]));
const c={case:'oct16',producer,inputs,outputs};
validateReproducedSource(c,'/root',()=>Buffer.from('same'));
let refused=0;
for(const mutate of [x=>delete x.outputs[Object.keys(x.outputs)[0]],x=>x.inputs[producer]='stale']){
 const copy=structuredClone(c);mutate(copy);
 try{validateReproducedSource(copy,'/root',()=>Buffer.from('same'));}catch(e){refused++;}
}
try{validateReproducedSource(c,'/root',()=>Buffer.from('mutated output'));}catch(e){refused++;}
const b={by_end:{low:{total_bn:0},high:{total_bn:0}}},specs=[{allocation:'personal',reading:'low'},{allocation:'personal',reading:'high'}];
const gp=Object.fromEntries(['a','b'].map(c=>[c,Object.fromEntries(['G1','G2','G3plus'].map(g=>[g,{meta:{generation:g,case_key:'oct16',case_lane:'main_case_2026_10_16',adopted:'2026-10-15',source_v8:'generation_corrections_oct15.json',mixed_unit_removal:b,coverage:b,v9_specs:specs,v9_posts_by_spec:[{coverage_repricing:0},{coverage_repricing:0}]}}]))]));
const full={adopted:'2026-10-20',mixed_unit_removal:b,coverage:b};
try{validateGenerationPayloads(gp,full,'oct16');}catch(e){refused++;}
validateGenerationPayloads(gp,full,'oct16',true);
gp.a.G1.meta.source_v8='invented.json';
try{validateGenerationPayloads(gp,full,'oct16',true);}catch(e){refused++;}
if(refused!==5)throw Error('negative controls '+refused);
console.log('PASS five provenance negatives');
"""
    result = subprocess.run(['node', '-e', script, str(Path(__file__).resolve().parent / 'generation_preflight.cjs')], capture_output=True, text=True)
    assert result.returncode == 0, result.stderr
    assert 'PASS five provenance negatives' in result.stdout


def test_v9_first_year_searches_every_mode_and_preserves_items_13_21():
    report = json.loads((tables.D / 'first_year_item6_oct16.json').read_text())
    case = json.loads((tables.CASE / 'summary.json').read_text())['v9']
    assert report['case'] == 'oct16'
    assert all(row['pass'] for row in report['checks'])
    for basis in ('set', 'cash'):
        principal = case['companions']['first_year']
        if basis == 'cash':
            principal = principal['cash']
        assert report['variants']['fixed_capital'][basis] == pytest.approx(principal['band_bn'], abs=1e-9, rel=0)
        assert report['ends']['fixed_capital'][basis] == principal['ends']
        for mode in ('fixed_capital', 'whole', 'corporate_only', 'off'):
            assert len(report['ends'][mode][basis]) == 2
            assert all(len(pair) == 2 and all(isinstance(i, int) and 0 <= i < 32 for i in pair)
                       for pair in report['ends'][mode][basis])
    assert report['post_components']
    assert all(row['item13_bn'] == pytest.approx(0, abs=1e-9) and isinstance(row['item21_bn'], (float, int))
               for row in report['post_components'])
    assert report['population_scope']['with_coverage'] == case['population']['with_coverage']
    # Independent closures (not the cost difference against itself) at every searched end.
    labels = [row['label'] for row in report['checks']]
    for needle in ('engine change rebuilt from receipt amounts and responses',
                   'non-engine change is post-engine, capital and companion terms',
                   'owner-property exclusion fixed across response modes',
                   'coverage line parts close to the coverage total'):
        assert sum(needle in label for label in labels) == len(report['post_components'])
    assert sum('calibrated multipliers' in label for label in labels) == 4 * len(report['post_components'])
    assert all(set(row['receipts']) == {'corporate_capital', 'corporate_labor', 'remaining_production_property',
                                        'other_production_taxes'} for row in report['components'])
    for row in report['post_components']:
        for name in ('line_parts', 'v9_line_parts'):
            part = row['post_engine'][name]
            assert part['rows'] > 0 and len(part['sha256']) == 64 and math.isfinite(part['sum_bn'])


def test_c1_search_states_its_size_cap_and_cross_checks():
    search = json.loads((tables.D / 'c1_search_oct16.json').read_text())
    cap = search['max_size_searched']
    assert cap == 5
    for direction in search['directions'].values():
        assert direction['max_size_searched'] == min(cap, direction['groups'])
        assert direction['complete'] == (direction['max_size_searched'] == direction['groups'])
    cuts = [r for r in tables.rows(tables.D / 'c1_min_cuts_oct16.csv') if r['minimal'] == 'yes']
    assert cuts and all(int(float(r['size'])) <= cap for r in cuts)
    checks = search['published_cross_checks']
    assert checks['item_arms_checked'] and checks['engine_arms_checked']
    assert not set(checks['item_arms_checked']) & set(checks['item_arms_without_current_row'])
HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('tables_oct16', HERE / 'tables_oct16.py')
tables = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tables)


def test_final_pin_capture_uses_repository_adoption_and_records_date_and_decision(tmp_path, monkeypatch):
    import sys
    import types
    pin_spec = importlib.util.spec_from_file_location('derive_oct16_pins', HERE / 'derive_oct16_pins.py')
    pins = importlib.util.module_from_spec(pin_spec)
    pin_spec.loader.exec_module(pins)
    case = tmp_path / 'case'
    case.mkdir()
    (case / 'corrections.json').write_text('{}')
    target = tmp_path / 'pins.json'
    source = types.SimpleNamespace(CASE=case, PINS=target, snapshot=lambda: {'source': 'checked'},
                                   require_adopted_payload=lambda payload: None)
    monkeypatch.setattr(pins, 'tables', source)
    monkeypatch.setattr(sys, 'argv', ['derive_oct16_pins.py'])
    def reject(key):
        raise SystemExit('[BLOCKED] adoption refused')
    monkeypatch.setattr(pins, 'require_adopted', reject)
    with pytest.raises(SystemExit, match='adoption refused'):
        pins.main()
    assert not target.exists()
    adoption = dict(key='oct16', adopted='2026-10-20', decision='decisions/2026-10-16-main-case-v9.md')
    monkeypatch.setattr(pins, 'require_adopted', lambda key: adoption)
    pins.main()
    record = json.loads(target.read_text())
    assert record['adoption'] == adoption
    assert set(record) == {'case', 'scope', 'adoption', 'inputs'}

def test_live_pairing_ignores_annotations_and_rejects_missing_live_numbers():
    records = [{'section': '6', 'column': 'historical', 'item': 'old', 'oct16': ''}, {'section': '7', 'column': 'pairing_on_priced_count', 'item': 'published pairing (low)', 'oct16': '440'}]
    assert tables.live_pairing_values(records) == {('pairing_on_priced_count', 'published pairing (low)'): 440.0}
    records[1]['oct16'] = ''
    with pytest.raises(SystemExit, match='\\[BLOCKED\\] missing or non-numeric oct16'):
        tables.live_pairing_values(records)

def test_evidence_drift_blocks_before_writing(tmp_path, monkeypatch):
    evidence = tmp_path / 'input.csv'
    evidence.write_text('value\n1\n')
    (tmp_path / 'live_case.json').write_text('{}\n')
    monkeypatch.setattr(tables, 'F', tmp_path)
    monkeypatch.setattr(tables, 'INPUTS', [evidence])
    pin = tmp_path / 'pins.json'
    pin.write_text(json.dumps({'inputs': tables.snapshot()}))
    monkeypatch.setattr(tables, 'PINS', pin)
    evidence.write_text('value\n2\n')
    with pytest.raises(SystemExit, match='\\[BLOCKED\\] final evidence drift'):
        tables.main()
    assert tables.snapshot()['input.csv']['numeric_cells'] == [[0, 'value', 2.0]]

def test_unknown_postengine_class_rule_blocks_before_case_loading():
    result = subprocess.run(['node', str(HERE / 'engine_breaks_sept29.cjs'), '--case', 'oct16', '--probe-only'], env={**os.environ, 'C2_POSTENGINE_CLASS_RULE': 'invented'}, capture_output=True, text=True)
    assert result.returncode != 0
    assert '[BLOCKED] unknown C2_POSTENGINE_CLASS_RULE invented' in result.stderr

def raw_comparator_fixture():
    return [{'case': 'oct16', 'arm': 'combined_rules_only', 'allocation': 'personal', 'mortality_convention': convention, 'mortality_bound': bound, 'basis': basis, 'group_mortality': 'whole-population' if convention == tables.MIXED_MORTALITY and group in ('mexican_origin_engine', tables.ROUGH_LINEAGE) else 'own-group', 'engine': 'case' if group == 'mexican_origin_engine' else 'rough', 'mixed_unit_removal_bn': 10 if group in ('mexican_origin_engine', tables.ROUGH_LINEAGE) else -5 if group == 'A1_third_plus_nh_white' else 0, 'comparator_item11_bn': -5 if group == 'A1_third_plus_nh_white' else 0, 'item11_paired_se_bn': 3 if group == 'A1_third_plus_nh_white' else '', 'mixed_unit_asymmetry': 'reweighted from A1: test' if group == 'A3_third_plus_nh_white_at_union_ages' else 'lineage measured; comparator measured', 'cost_without_item11_bn': 340 if group in ('mexican_origin_engine', tables.ROUGH_LINEAGE) else -20, 'group': group, 'end': end, 'cost_bn': 350 if group in ('mexican_origin_engine', tables.ROUGH_LINEAGE) else -25 if group == 'A1_third_plus_nh_white' else -20} for convention, bound in tables.MORTALITY_READINGS for basis in ('accrual', 'cash') for group in ('mexican_origin_engine', tables.ROUGH_LINEAGE, 'A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages') for end in ('low', 'high')]

def comparator_fixture():
    records = raw_comparator_fixture()
    for row in records:
        if row['group'] in ('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages'):
            row.update(item11_paired_se_bn=None, item11_comparator_se_bn=3.,
                       item11_se_scope='own-mask comparator SDR at v9 counts; calibrated v9 lineage paired replicate vector unmeasured')
    return records


def test_comparator_rejects_stale_paired_se_and_unlabelled_missingness():
    records = comparator_fixture()
    white = next(row for row in records if row['group'] == 'A1_third_plus_nh_white')
    white['item11_paired_se_bn'] = 0.
    with pytest.raises(SystemExit, match='numeric value is unsupported'):
        tables.comparator_values(records)
    white['item11_paired_se_bn'] = None
    white.pop('item11_se_scope')
    with pytest.raises(SystemExit, match='explicit source scope'):
        tables.comparator_values(records)
    white['item11_se_scope'] = 'calibrated v9 lineage paired replicate vector unmeasured'
    white['item11_comparator_se_bn'] = -1.
    with pytest.raises(SystemExit, match='must be nonnegative'):
        tables.comparator_values(records)


def test_comparator_pairing_requires_explicit_case_and_mortality_labels():
    records = comparator_fixture()
    values = tables.comparator_values(records)
    assert tables.comparator_gap(values, tables.MIXED_MORTALITY, 'none', 'accrual', 'A1_third_plus_nh_white') == [375, 375]
    records[0].pop('mortality_convention')
    with pytest.raises(SystemExit, match='explicit mortality convention/bound required'):
        tables.comparator_values(records)
    records = comparator_fixture()
    records[0]['case'] = 'oct14'
    with pytest.raises(SystemExit, match='comparator case must be oct16'):
        tables.comparator_values(records)
    records = comparator_fixture()
    next((r for r in records if r['group'] == tables.ROUGH_LINEAGE))['group_mortality'] = 'own-group'
    with pytest.raises(SystemExit, match="mortality pairing requires explicit label 'own-group mortality'"):
        tables.comparator_values(records)

def test_comparator_rejects_mixed_engines_and_undeclared_item11():
    records = comparator_fixture()
    next((r for r in records if r['group'] == tables.ROUGH_LINEAGE))['engine'] = 'case'
    with pytest.raises(SystemExit, match='different engine tags'):
        tables.comparator_values(records)
    records = comparator_fixture()
    next((r for r in records if r['group'] == tables.ROUGH_LINEAGE)).pop('mixed_unit_asymmetry')
    with pytest.raises(SystemExit, match='explicit mixed-unit asymmetry required'):
        tables.comparator_values(records)

def test_bridge_closes_at_every_mortality_bound_and_rejects_incomplete_parts():
    values = tables.comparator_values(comparator_fixture())
    parts = [{'case': 'oct16', 'arm': 'combined_rules_only', 'basis': basis, 'end': end, 'case_engine': 'case', 'rough_engine': 'rough', 'mortality_convention': mortality, 'mortality_bound': bound, 'side': 'spending', 'line': 'source', 'case_bn': 350, 'rough_bn': 350, 'case_minus_rough_bn': 0} for mortality, bound in tables.MORTALITY_READINGS for basis in ('accrual', 'cash') for end in ('low', 'high')]
    assert set(tables.bridge_values(parts, values)) == {(mortality, bound, basis, end) for mortality, bound in tables.MORTALITY_READINGS for basis in ('accrual', 'cash') for end in ('low', 'high')}
    with pytest.raises(SystemExit, match='missing itemized bridge'):
        tables.bridge_values(parts[:-1], values)
    values[tables.OWN_MORTALITY, 'low', 'accrual', 'mexican_origin_engine', 'low'] += 1
    with pytest.raises(SystemExit, match='itemized bridge closure'):
        tables.bridge_values(parts, values)

def test_comparator_missing_bound_or_duplicate_fails():
    records = comparator_fixture()
    with pytest.raises(SystemExit, match='missing comparator row'):
        tables.comparator_values(records[:-1])
    with pytest.raises(SystemExit, match='duplicate comparator row'):
        tables.comparator_values([*records, records[0]])

@pytest.mark.parametrize('got,want', [(float('nan'), 1), (1, float('inf'))])
def test_nonfinite_principal_or_calculation_cannot_pass_tolerance(got, want):
    with pytest.raises(SystemExit, match='non-finite value'):
        tables.check('principal', got, want, 1e-09)

def test_tables_use_final_first_year_verdict():
    report = json.loads((tables.D / 'first_year_item6_oct16.json').read_text())
    conclusions = {r['id']: r for r in tables.rows(tables.D / 'conclusions_oct16.csv')}
    clause = 'First-year horizon breaks C1 alone' if report['first_year_breaks_alone'] else 'First-year horizon does not break C1 alone'
    assert clause in conclusions['C1']['break_condition']
    premise = next((r for r in tables.rows(tables.D / 'common_mode_oct16.csv') if r['premise_id'] == 'P02'))
    assert clause in premise['effect_if_swapped']

def test_generation_parts_add_to_final_case():
    case = json.loads((tables.CASE / 'summary.json').read_text())['v9']
    records = tables.rows(tables.D / 'c6_generation_break_even_oct16.csv')
    for basis, key in (('case_accrual', 'band_bn'), ('cash_set', 'cash_set_bn')):
        for convention in ('a', 'b'):
            selected = [r for r in records if r['case'] == basis and r['convention'] == convention]
            assert {r['generation'] for r in selected} == {'G1', 'G2', 'G3plus'}
            for i, field in enumerate(('cost_low_end_bn', 'cost_high_end_bn')):
                assert sum((float(r[field]) for r in selected)) == pytest.approx(case[key][i], abs=0.0002, rel=0)

def test_c8_reports_all_source_mortality_bounds():
    records = tables.rows(tables.D / 'c8_comparisons_oct16.csv')
    assert len(records) == 24
    assert {r['case'] for r in records} == {'oct16'}
    assert {(r['mortality_convention'], r['mortality_bound']) for r in records} == set(tables.MORTALITY_READINGS)
    for row in records:
        assert row['lineage_engine'] == row['comparator_engine'] == 'rough'
        assert float(row['lineage_minus_comparator_bn']) == pytest.approx(float(row['lineage_cost_bn']) - float(row['comparator_cost_bn']), abs=1e-09, rel=0)
        assert float(row['lineage_minus_comparator_without_item11_bn']) == pytest.approx(float(row['lineage_minus_comparator_bn']) - float(row['mixed_unit_removal_bn']), abs=1e-09, rel=0)
        assert row['mixed_unit_asymmetry']
        assert row['item11_paired_se_bn'] == ''
        assert float(row['item11_comparator_se_bn']) >= 0
        assert 'calibrated v9 lineage paired replicate vector unmeasured' in row['item11_se_scope']
    conclusions = {r['id']: r for r in tables.rows(tables.D / 'conclusions_oct16.csv')}
    assert 'matched local-white reading GAP' in conclusions['C8']['status_on_v9']
    assert all((label in conclusions['C8']['reading_on_v9'] for label in (tables.MIXED_MORTALITY, tables.OWN_MORTALITY)))


def test_current_flow_keeps_unlocated_and_incomplete_financing():
    directory = tables.F / 'debt_legacy_2026_09_23/derived/oct16'
    contract = json.loads((directory / 'current_flow_contract.json').read_text())
    records = tables.rows(directory / 'current_flow_source_parts_2024.csv')
    summary = json.loads((tables.CASE / 'summary.json').read_text())['v9']
    result = tables.current_flow_values(contract, records, summary)
    assert len(result) == 4
    assert all(r['complete_state_local_share_pct'] == r['legacy_interest_bn'] == '' for r in result)
    unlocated = next(r for r in records if r['financing'] == 'unlocated' and r['convention'] == 'central')
    unlocated['federal_bn'] = '0'
    with pytest.raises(SystemExit, match='must not silently acquire a payer'):
        tables.current_flow_values(contract, records, summary)
    contract['financing_complete'] = True
    with pytest.raises(SystemExit, match='declared incomplete'):
        tables.current_flow_values(contract, records, summary)


def test_winner_contract_rejects_duplicate_and_other_frame():
    records = tables.rows(tables.F / 'winners_losers_2026_09_24/derived/oct16/p7_net_shares.csv')
    values = tables.winner_values(records)
    assert len(values) == 3 and all(0 < value < 100 for value in values)
    selected = [r for r in records if r['arm'] == 'recommended' and r['frame'] == 'stationary'
                and r['level'] == 'central' and r['epsilon'] == 'infinite' and r['sharing'] == 'pooled']
    with pytest.raises(SystemExit, match='absent or duplicated'):
        tables.winner_values([*records, selected[0]])
    with pytest.raises(SystemExit, match='absent or duplicated'):
        tables.winner_values([{**r, 'frame': 'cohort'} for r in records])
