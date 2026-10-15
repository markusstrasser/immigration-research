"""Case-contract tests: full-lineage repricing and explicit incomplete data."""
from pathlib import Path
import hashlib
import json
import math
import subprocess
import pytest

import veterans
import military_health

HERE = Path(__file__).resolve().parent


def test_fiscal_program_split_keeps_means_tested_pension():
    item = veterans.build_item()
    assert math.isclose(item['response'], 3.161729/(157.781014+3.161729), abs_tol=1e-15)
    assert item['compensation_response'] == 0
    assert item['pension_response'] == 1
    assert 0 < item['response'] < .03


def test_missing_va_outlay_table_fails_loud(tmp_path, monkeypatch):
    inputs = tmp_path / 'inputs'
    inputs.mkdir()
    records = json.loads((HERE / 'inputs/veterans_sources.json').read_text())
    for record in records:
        text = (HERE / 'inputs' / record['file']).read_text()
        if record['file'].startswith('va_'):
            text = text.replace('Distribution of Outlays (Net):', 'Different table')
        file = inputs / record['file']
        file.write_text(text)
        record['excerpt_sha256'] = hashlib.sha256(file.read_bytes()).hexdigest()
    (inputs / 'veterans_sources.json').write_text(json.dumps(records))
    monkeypatch.setattr(veterans, 'HERE', tmp_path)
    with pytest.raises(ValueError, match='outlay table'):
        veterans.build_item()


def test_unchanged_v8_and_full_lineage_parts_close():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    assert case['population'] == pytest.approx(45_230_062.30075857, abs=1e-6)
    for which, expected in [('set', [365.791930, 455.981785]), ('cash', [281.752564, 371.942418])]:
        assert list(case['baseline'][which].values()) == pytest.approx(expected, abs=1e-6)
        for number in ['13', '14', '15']:
            built = case['payloads'][which][number]['central']
            block = next(iter(built['meta'].values()))
            for end in ['low', 'high']:
                value = block['by_end'][end]
                assert sum(part['delta_bn'] for part in value['parts']) == pytest.approx(value['total_bn'], abs=1e-9)
                populations = {part['population'] for part in value['parts']}
                assert populations == {'engine', 'completion', 'coverage'}


def test_veterans_reprices_coverage_and_completion_without_cash_switch():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    rows = [r for r in case['rows'] if r['item'] == 13 and r['arm'] == 'central']
    assert len(rows) == 4
    assert max(r['change_bn'] for r in rows) - min(r['change_bn'] for r in rows) < 1e-9
    response = veterans.build_item()['response']
    built = case['payloads']['set']['13']['central']['meta']['veterans_compensation']['by_end']['low']
    before = sum(part['before_bn'] for part in built['parts'] if part['part'] == 'compensation')
    assert before == pytest.approx(10.34781988958276, abs=1e-6)
    assert built['by_part']['compensation'] == pytest.approx(before*(response-1), abs=1e-9)
    extension = [p for p in built['parts'] if p['part'] == 'extension']
    assert {p['source_line'] for p in extension} == {'veterans_other', 'veterans_readjustment', 'veterans_life_insurance', 'military_medical'}
    assert all(p['after_bn'] == 0 and p['response'] == 0 for p in extension)
    medical = [p for p in built['parts'] if p['part'] == 'va_medical']
    assert built['total_bn'] == pytest.approx(before*(response-1)-sum(p['before_bn'] for p in extension+medical), abs=1e-9)


def test_item13_generation_means_close_by_part_and_line():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    for which in ['set', 'cash']:
        block = case['payloads'][which]['13']['central']['meta']['veterans_compensation']
        for conv in ['a', 'b']:
            for end in ['low', 'high']:
                gen = block['by_generation'][conv][end]
                union = block['by_end'][end]
                assert sum(gen['by_generation_bn'].values()) == pytest.approx(union['total_bn'], abs=1e-9)
                for part in ['compensation', 'extension', 'va_medical']:
                    assert sum(gen['by_part'][part].values()) == pytest.approx(union['by_part'][part], abs=1e-9)
                for p in union['parts']:
                    rows = [q for q in gen['parts'] if q['part'] == p['part'] and q['line'] == p['line'] and q['population'] == p['population'] and (not p.get('generation') or q['generation'] == p['generation'])]
                    assert sum(q['delta_bn'] for q in rows) == pytest.approx(p['delta_bn'], abs=1e-9)


def test_declared_medical_approximation_enters_central_with_correct_scope():
    item = veterans.build_item()
    bridge = item['extension']['health_bridge']
    assert bridge['status'] == '[APPROXIMATION]'
    assert bridge['outlay_status'] == '[DATA]'
    assert bridge['central_national_bn'] == pytest.approx(70.484+10.372+8.886, abs=1e-12)
    assert bridge['federal_health_consumption'] == 179.7
    assert bridge['state_local_health_consumption'] == 126.839
    assert [p['line'] for p in item['extension']['lines'] if p.get('part') == 'va_medical'] == ['health_services']


def test_medical_bridge_rejects_missing_or_out_of_scope_mass():
    bridge = json.loads((HERE / 'inputs/medical_bridge.json').read_text())
    cells = military_health.medical_outlay_cells((HERE / 'inputs/va_medical_fy2024_excerpt.txt').read_text())
    for value in [None, 0, float('nan'), 138.543, 306.539]:
        altered = {**bridge, 'central_national_bn': value}
        with pytest.raises(ValueError, match='mass/source scope'):
            military_health.validate_medical_bridge(altered, cells, 179.7)


def test_va_medical_arms_scale_only_health_subblock_and_typed_coverage():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    masses = {'central': 89.742, 'va_medical_services_only': 70.484, 'va_medical_four_accounts': 121.130}
    for which in ['set', 'cash']:
        for arm, mass in masses.items():
            block = case['payloads'][which]['13'][arm]['meta']['veterans_compensation']
            for end in ['low', 'high']:
                value = block['by_end'][end]
                medical = [p for p in value['parts'] if p['part'] == 'va_medical']
                assert {p['population'] for p in medical} == {'engine', 'completion', 'coverage'}
                assert all(p['source_line'] == 'health_services' for p in medical)
                assert all(p['key'] == ('k' if p['population'] == 'completion' else 'health_other') for p in medical)
                assert all(p['amount_bn'] == 0 for p in medical if p['population'] == 'completion' and not p['line'].endswith('_health_other'))
                national = next(p['national_bn'] for p in medical if p['population'] == 'engine')
                assert national == pytest.approx(308.358754899, abs=1e-9)
                for p in medical:
                    assert p['national_component_bn'] == mass
                    assert p['fraction'] == pytest.approx(mass/national, abs=1e-12)
                    assert p['before_bn'] == pytest.approx(p['amount_bn']*p['fraction'], abs=1e-9)
                    assert p['after_bn'] == 0 and p['response'] == 0
                assert value['by_part']['compensation']+value['by_part']['extension'] == pytest.approx(-13.013447638, abs=1e-9)
                assert value['by_part']['va_medical'] == pytest.approx(-5.904991128*mass/89.742, abs=1e-9)
                for conv in ['a', 'b']:
                    coverage = [p for p in block['by_generation'][conv][end]['parts'] if p['part'] == 'va_medical' and p['population'] == 'coverage']
                    if conv == 'a':
                        coverage_a = coverage
                    else:
                        assert coverage == coverage_a


def test_medical_excerpt_requires_actual_outlay_cells():
    text = (HERE / 'inputs/va_medical_fy2024_excerpt.txt').read_text()
    with pytest.raises(ValueError, match='medical_services'):
        military_health.medical_outlay_cells(text.replace('Medical Services (036-0160)', 'Different appropriation'))
    with pytest.raises(ValueError, match='TEF scope'):
        military_health.medical_outlay_cells(text.replace('16,305', '20,268'))


def test_compensation_only_arm_and_unchanged_are_preserved():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    for which in ['set', 'cash']:
        blocks = case['payloads'][which]['13']
        old = blocks['compensation_only']['meta']['veterans_compensation']
        assert old['low'] == pytest.approx(-10.144536217, abs=1e-9)
        assert blocks['unchanged']['meta']['veterans_compensation']['low'] == 0


def test_college_tuition_and_pell_are_not_scaled():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    built = case['payloads']['set']['15']['central']['meta']['public_college_response']
    for value in built['by_end'].values():
        parts = value['parts']
        assert all(p['source_line'] != 'other_federal_benefits' for p in parts)
        assert {p['kind'] for p in parts} == {'college_operating', 'college_capital'}
        # Gross/net response applies only to the use-priced NIPA subblock; no
        # entire education or tuition-disparity line is multiplied.
        assert all(p['line'] == 'education_services:college_only' for p in parts if p['kind'] == 'college_operating')


def test_method_parts_keep_method_mean_and_require_method():
    case = json.loads((HERE / 'derived/case_changes.json').read_text())
    for block in case['payloads']['set']['13']['central']['meta'].values():
        for end in block['by_end'].values():
            values = [m['total_bn'] for m in end['by_method'].values()]
            assert max(values) - min(values) > .1
            assert sum(values)/len(values) == pytest.approx(end['total_bn'], abs=1e-12)
    code = "const I=require('./items.cjs');try{I.postEngineFor({meta:{x:{by_end:{low:{total_bn:2,by_method:{a:{total_bn:1}}}}}}},'low');process.exit(2)}catch(e){if(!e.message.includes('explicit source method'))throw e}"
    subprocess.run(['node', '-e', code], cwd=HERE, check=True)
