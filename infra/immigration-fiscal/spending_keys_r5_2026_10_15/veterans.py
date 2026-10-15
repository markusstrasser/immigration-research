"""Item 13: fixed-defense response, with an explicit FY-to-CY composition bridge.

The program outlays are measured; their shares transported to BEA's CY line are
modeled. No normal-cost replacement is added under the parent's fixed-defense rule.
"""
from pathlib import Path
import hashlib
import json
import re
import openpyxl
from military_health import build_extension

HERE = Path(__file__).resolve().parent


def build_item():
    sources = json.loads((HERE / 'inputs/veterans_sources.json').read_text())
    for source in sources:
        file = HERE / 'inputs' / source['file']
        if hashlib.sha256(file.read_bytes()).hexdigest() != source['excerpt_sha256']:
            raise ValueError('[BLOCKED] item13 primary-source excerpt changed')
    text = (HERE / 'inputs/va_budget_2024_excerpt.txt').read_text()
    sections = text.split('Distribution of Outlays (Net):')
    if len(sections) != 2:
        raise ValueError('[BLOCKED] VA excerpt lacks exactly one outlay table')
    outlays = sections[1]
    fiscal = {}
    for label in ['Compensation', 'Pension', 'Burial']:
        match = re.search(r'^\s*' + label + r'\s+\$([\d,]+)', outlays, re.M)
        if match is None:
            raise ValueError(f'[BLOCKED] VA FY2024 outlay {label} absent')
        fiscal[label.lower()] = int(match[1].replace(',', '')) / 1e6
    if fiscal != {'compensation': 157.781014, 'pension': 3.161729, 'burial': .351874}:
        raise ValueError('[BLOCKED] VA FY2024 source cells changed')
    obligation = {}
    for label in ['Compensation', 'Pension']:
        match = re.search(r'Total ' + label + r' Obligations:\s+\$([\d,]+)', text)
        if match is None:
            raise ValueError('[BLOCKED] VA obligation arm source absent')
        obligation[label.lower()] = int(match[1].replace(',', '')) / 1e6
    # The literal 2024 compensation benefits-paid cell, not actuarial expense.
    treasury = (HERE / 'inputs/treasury_note13_excerpt.txt').read_text()
    row = next(line for line in treasury.splitlines() if line.strip().startswith('Less benefits paid'))
    paid = [float(x) for x in re.findall(r'\(([\d.]+)\)', row)]
    if paid != [186.7, 176.2, .3, .3, 187.0, 176.5]:
        raise ValueError('[BLOCKED] Treasury 2024 compensation paid cell changed')
    def response(c, p, other=0):
        return (p + other) / (c + p + other)
    central = response(fiscal['compensation'], fiscal['pension'])
    bea = HERE.parents[2] / 'sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx'
    with bea.open('rb') as stream:
        if hashlib.file_digest(stream, 'sha256').hexdigest() != '69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e':
            raise ValueError('[BLOCKED] veterans BEA source vintage changed')
    book = openpyxl.load_workbook(bea, read_only=True, data_only=True)
    rows = list(book['T31200-A'].values)
    header = next(row for row in rows if row[0] == 'Line')
    year = next(i for i, value in enumerate(header) if str(value) == '2024')
    cells = [row[year] for row in rows if str(row[0]) == '18']
    if len(cells) != 1:
        raise ValueError('[BLOCKED] veterans BEA line18 absent or duplicated')
    national = cells[0] / 1000
    book.close()
    if national != 180.525 or rows[1][0] != '[Millions of dollars]':
        raise ValueError('[BLOCKED] veterans BEA principal line changed')
    return {
        'id': 'veterans_compensation', 'number': 13,
        'kind': 'post_engine', 'line': 'veterans_pension_disability',
        'status': 'CONDITIONAL: accepted compensation FY mix; four service-benefit extensions; VA medical [DATA] outlays with declared [APPROXIMATION] consumption bridge',
        'response': central,
        'bea_national_bn': national,
        'bea_modeled_split_bn': {'compensation': national*(1-central), 'means_tested_pension': national*central,
                                'unidentified_other': None},
        'other_limit': 'No independent CY2024 other-program amount identified; the two-program central bridge is a scope assumption. Burial inclusion is an explicit alternative, not an observed BEA component.',
        'components_fy2024_bn': fiscal,
        'compensation_response': 0, 'pension_response': 1,
        'other_rule': 'Burial is outside the pension/disability benefit bridge; retained at response1 in the inclusion arm.',
        'arms': {
            'obligation_mix': response(obligation['compensation'], obligation['pension']),
            'treasury_compensation_mix': response(paid[1], fiscal['pension']),
            'burial_retained': response(fiscal['compensation'], fiscal['pension'], fiscal['burial']),
            'unchanged': 1,
            'compensation_only': central,
        },
        'sources': sources,
        'bridge': 'BEA CY2024 national line is preserved; split by measured VA FY2024 compensation:pension outlay shares. FY timing, accrual and territorial adjustments are not observed by component.',
        'method_source': 'https://apps.bea.gov/scb/pdf/national/nipa/Methpap/methpap5.pdf, p46: monthly outlays, timing adjustments, survivor programs and foreign/territorial exclusions',
        'group_key': 'The existing veterans benefit-dollar key is applied equally to both parts; distinct Mexican-origin pension/compensation shares are not measured.',
        'fixed': 'Defense positions replaced; compensation response0, pension1, no replacement normal cost. Both accounting sets keep this rule.',
        'limits': ['FY2024 shares are a declared composition proxy, not an observed CY2024 BEA decomposition.',
                   'VA outlays and Treasury benefits-paid differ in timing/accounting; Treasury mix is an arm, not silently equated.',
                   'Separate group receipt shares could change retained pension cost; current CPS veterans key is benefit dollars, not veteran population.'],
        'extension': build_extension(),
    }
