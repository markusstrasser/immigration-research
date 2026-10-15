"""Item13 service benefits and the declared VA medical outlay approximation.

The outlays are primary data; their FY-to-CY consumption bridge is approximate.
"""
from pathlib import Path
import hashlib
import json
import re
import openpyxl

HERE = Path(__file__).resolve().parent
BEA_SHA = '69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e'


def medical_outlay_cells(text):
    if 'Actual' not in text or 'Functional Distribution of Outlays (Net)' not in text:
        raise ValueError('[BLOCKED] missing VA actual net-outlay table')
    cells = {}
    for field, label in [
        ('medical_services', 'Medical Services (036-0160)'),
        ('medical_support_compliance', 'Medical Support and Compliance (036-0152)'),
        ('medical_facilities', 'Medical Facilities (036-0162)'),
        ('medical_community_care', 'Medical Community Care (036-0140)'),
        ('hospital_medical_function_703', 'Subtotal, Hospital and medical care for veterans'),
    ]:
        values = re.findall(r'^\s*'+re.escape(label)+r'\s+([\d,]+)', text, re.M)
        if not values or len(set(values)) != 1:
            raise ValueError('[BLOCKED] missing/conflicting VA medical outlay '+field)
        cells[field] = int(values[0].replace(',', '')) / 1000
    tef = re.findall(r'^\s*Cost of War Toxic Exposures Fund \(036-1126\)\s+([\d,]+)', text, re.M)
    if tef != ['19,457', '16,305']:
        raise ValueError('[BLOCKED] VA medical TEF scope absent or changed')
    cells['toxic_exposures_fund_all'], cells['toxic_exposures_fund_medical_function'] = [int(v.replace(',', ''))/1000 for v in tef]
    cells['medical_four_accounts'] = sum(cells[f] for f in ['medical_services', 'medical_support_compliance', 'medical_facilities', 'medical_community_care'])
    cells['four_accounts_less_community_care'] = cells['medical_four_accounts']-cells['medical_community_care']
    return cells


def validate_medical_bridge(medical, cells, federal_health):
    """Fail loudly on changed source/bridge scope rather than restoring response1."""
    if medical['status'] != '[APPROXIMATION]' or medical['outlay_status'] != '[DATA]':
        raise ValueError('[BLOCKED] VA medical bridge must distinguish data and approximation')
    masses = {'central': medical['central_national_bn'],
              **{name: arm['national_bn'] for name, arm in medical['arms'].items()}}
    expected = {'central': cells['four_accounts_less_community_care'],
                'va_medical_services_only': cells['medical_services'],
                'va_medical_four_accounts': cells['medical_four_accounts']}
    if set(masses) != set(expected) or any(
            not isinstance(value, (int, float)) or not 0 < value <= federal_health
            or abs(value-expected[name]) > 1e-12 for name, value in masses.items()):
        raise ValueError('[BLOCKED] VA medical approximation mass/source scope changed')


def build_extension():
    bea = HERE.parents[2] / 'sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx'
    with bea.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != BEA_SHA:
            raise ValueError('[BLOCKED] item13 extension BEA vintage changed')
    book = openpyxl.load_workbook(bea, read_only=True, data_only=True)
    def cell(sheet, line):
        rows = list(book[sheet].values)
        header = next(r for r in rows if r[0] == 'Line')
        year = next(i for i, value in enumerate(header) if str(value) == '2024')
        found = [r[year] for r in rows if str(r[0]) == str(line)]
        if len(found) != 1 or not isinstance(found[0], (int, float)):
            raise ValueError('[BLOCKED] missing primary military/health cell')
        return found[0] / 1000
    lines = []
    for name, key, line, component, anchor in [
        ('veterans_other', 'va_medical', 20, 'VA purchased care and other veterans benefits', 37.526),
        ('veterans_readjustment', 'veterans', 19, 'GI Bill/readjustment', 11.391),
        ('veterans_life_insurance', 'veterans', 14, 'veterans life insurance', .449),
        ('military_medical', 'tricare', 16, 'active-duty dependents purchased medical care', 7.157),
    ]:
        amount = cell('T31200-A', line)
        if amount != anchor:
            raise ValueError('[BLOCKED] military benefit national anchor changed')
        lines.append(dict(line=name, key=key, national_bn=amount, fraction=1,
                          response=0, component=component, source=f'BEA T31200-A:{line} CY2024'))
    national = {name: cell('T31700-A', line) for name, line in [
        ('health_consumption', 7), ('federal_health_consumption', 17), ('state_local_health_consumption', 26)]}
    book.close()
    if national != {'health_consumption': 306.539, 'federal_health_consumption': 179.7,
                    'state_local_health_consumption': 126.839}:
        raise ValueError('[BLOCKED] primary health consumption anchors changed')
    medical = json.loads((HERE / 'inputs/medical_bridge.json').read_text())
    if not medical['sources']:
        raise ValueError('[BLOCKED] missing primary medical source excerpts')
    for source in medical['sources']:
        file = HERE / 'inputs' / source['file']
        if hashlib.sha256(file.read_bytes()).hexdigest() != source['sha256']:
            raise ValueError('[BLOCKED] military health primary excerpt changed')
    cells = medical_outlay_cells((HERE / 'inputs/va_medical_fy2024_excerpt.txt').read_text())
    if any(abs(value-medical['fy2024_net_outlays_bn'][name]) > 1e-12 for name, value in cells.items()):
        raise ValueError('[BLOCKED] VA source actuals differ from declared bridge')
    validate_medical_bridge(medical, cells, national['federal_health_consumption'])
    lines.append(dict(line='health_services', key='health_other', fraction=None,
                      part='va_medical', response=0, component='VA direct hospital and medical care',
                      source='VA FY2026 Vol1 pp71-72,82 FY2024 actual outlays; declared FY-to-CY approximation'))
    return dict(lines=lines, health_bridge={**medical, **national},
                rule='Fixed defense: service-earned benefits response0; means-tested pension remains1.',
                included='Four complete benefit lines plus the declared three-account VA medical approximation.',
                source_bea_sha256=BEA_SHA,
                already_zero=['military pension normal cost in defense', 'military facilities and MERHCF normal cost in defense',
                              'military pension legacy interest in domestic_interest'],
                already_removed='Military retiree purchased care, other_federal_benefits/all_cash: existing retiree_health item removes 19.797540984bn nationally; no second removal.',
                unresolved=[
                    dict(line='other_state_benefits', key='population', status='[UNVERIFIED]', reason='T3.12 line42 includes veterans benefits, Alaska dividends and crime victims; military national subblock not bridged.'),
                    dict(line='health capital', key='health_other', status='[UNVERIFIED]', reason='VA hospital stock and military subblock of mixed health capital not measured.'),
                    dict(line='mixed administration/receipts', key='various', status='[UNVERIFIED]', reason='No additive service-contingent national subblocks or VA sales/fees bridged; no blanket removal.')])
