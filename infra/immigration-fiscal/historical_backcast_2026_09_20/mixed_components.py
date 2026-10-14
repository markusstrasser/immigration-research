"""Exact r0 programme/generation parts for v8's bounded mixed-unit delta."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
SOURCE = FISCAL / 'mixed_unit_removal_2026_10_14'
GENS = ('G1', 'G2', 'G3+')
FIXED = {'M1_federal': ('receipt', 'federal_income_tax'),
         'M2_state': ('receipt', 'state_local_income_tax'),
         'M3_refunds': ('spending', 'refundable_tax_credits'),
         'M6_biological_children': ('receipt', 'federal_income_tax'),
         'D_added_residual': ('receipt', 'federal_income_tax'),
         'M5_owner_property': ('receipt', 'modeled_owner_property'),
         'M5_housing_key': ('spending', 'housing_subsidies'),
         'M5_consumption': ('receipt', 'consumption_receipts_composite')}
CONSUMPTION = {'general_sales_tax': 'T30500-A:20', 'excise_selective_sales': 'T30500-A:4;T30500-A:23',
               'customs_duties': 'T30500-A:15', 'personal_current_transfers': 'T30100-A:17'}


def require(ok, message):
    if not ok:
        raise ValueError('[BLOCKED] mixed source programme parts: ' + message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def rows_for(meta, frame, basis, end, case):
    principal = meta['by_end'][end]
    h, a, s = principal['envelope_arm'].split('|')
    definitions = [(k, basis, end, side, line) for k, (side, line) in FIXED.items()]
    definitions += [('health_latent_' + h, 'diagnostic', 'low', 'spending', 'medicaid_and_chip_other_medical'),
                    ('health_latent_' + a, 'diagnostic', 'low', 'spending', 'medicaid_and_chip_other_medical'),
                    ('SNAP_latent_' + s, 'diagnostic', 'low', 'spending', 'snap')]
    weights = {CONSUMPTION[k]: case['lines'][k]['union_target_bn'] for k in CONSUMPTION}
    total_weight = sum(weights.values())
    require(total_weight > 0, 'consumption reference weights absent')
    weights = {ref: v / total_weight for ref, v in weights.items()}
    amounts = {CONSUMPTION[k]: case['lines'][k]['national_bn'] for k in CONSUMPTION}
    rows = []
    for component, method, source_end, side, line in definitions:
        for gen in GENS:
            key = (method, source_end, component, gen)
            require(key in frame.index, f'missing r0 cell {key}')
            value = float(frame.loc[key, 'r0'])
            require(np.isfinite(value), f'nonfinite r0 {key}')
            if component == 'D_added_residual':
                require(gen == 'G3+' or abs(value) <= 1e-12, 'D_added appears outside G3+')
                value = principal['D_added_residual_bn'] if gen == 'G3+' else 0.0
            row = dict(end=end, generation=gen, component=component, side=side, line=line, value_bn=value,
                       path='lineage' if component == 'D_added_residual' else 'union', rule='line')
            if component == 'M5_consumption':
                row.update(rule='composite_receipts', income_linked=True, composite_cells=weights,
                           composite_national_bn=amounts,
                           transport_assumption='Source preserves only aggregate M5 consumption receipts. Historical index weights its four national receipt indices by2024 union amounts; exact line-by-generation split, including excise CBO allocation, is not observed in preserved output.')
            elif component == 'M3_refunds':
                row.update(rule='non_eip_credits', transport_assumption='Solved EITC/ACTC refund change follows refundable credits excluding separately measured EIP payments; no EIP counterfactual is inferred from this2024 component.')
            elif component.startswith('health_latent_Medicaid'):
                row.update(measured_fraction=1.0, use_key='medicaid_covered')
            elif component.startswith('health_latent_ACA'):
                row.update(use_key_exempt=True, transport_assumption='ACA premium credits use the other-medical national index; Medicaid coverage is not an ACA use observation.')
            rows.append(row)
    for gen in GENS:
        require(abs(sum(r['value_bn'] for r in rows if r['generation'] == gen)
                    - principal['by_generation_bn'][gen]) <= 1e-9, f'{basis}/{end}/{gen} r0 closure')
    require(abs(sum(r['value_bn'] for r in rows) - principal['total_bn']) <= 1e-9,
            f'{basis}/{end} principal closure')
    return rows


def main():
    frame_path = SOURCE / 'derived/round2_replicates.csv'
    case_path = SOURCE / 'derived/case_inputs.json'
    frame = pd.read_csv(frame_path, usecols=['method', 'end', 'component', 'generation', 'r0']).set_index(['method', 'end', 'component', 'generation'])
    require(frame.index.is_unique, 'duplicate r0 cell')
    case = json.loads(case_path.read_text())
    result = dict(case='oct15', sets={}, inputs={})
    for basis in ('set', 'cash'):
        payload_path = FISCAL / f'main_case_2026_10_15/derived/corrections{"_cash" if basis == "cash" else ""}.json'
        meta = json.loads(payload_path.read_text())['meta']['mixed_unit_removal']
        for entry in meta['source']['files'].values():
            source = ROOT / entry['path']
            require(digest(source) == entry['sha256'], 'adopted source pin changed: ' + entry['path'])
            result['inputs'][entry['path']] = entry['sha256']
        result['sets'][basis] = sum((rows_for(meta, frame, basis, end, case) for end in ('low', 'high')), [])
        result['inputs'][str(payload_path.relative_to(ROOT))] = digest(payload_path)
    for p in (Path(__file__).resolve(), case_path, SOURCE / 'round2.py', SOURCE / 'removal.py'):
        result['inputs'][str(p.relative_to(ROOT))] = digest(p)
    sys.path.insert(0, str(FISCAL / 'scripts'))
    from memory_budget import require_within_budget
    footprint = require_within_budget('mixed programme decomposition')
    (HERE / 'derived/mixed_components_oct15.json').write_text(json.dumps(result, indent=1, allow_nan=False) + '\n')
    print(f'PASS exact mixed r0 generation/total closure1e-9; physical_footprint={footprint}')


if __name__ == '__main__':
    main()
