"""Render the price ruling directly from checked CSVs; append dated records."""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

PARTS = ('world_total_bn', 'group_total_bn', 'mexico_residents_bn', 'other_us_residents_bn')
KEYS = ['reading', 'account_end', 'g3_bound', 'weighting']
VARIANTS = ('published', 'brief_category', 'mexico_only', 'us_only', 'both')
WEIGHTS = {'equal', 'equal_lambda_1.16', 'equal_lambda_1.5', 'equal_lambda_hendren_a',
           'hendren_a', 'hendren_b', 'log_a', 'log_b'}


def tables(frame, parts=PARTS, equal_only=False):
    if equal_only:
        frame = frame[frame.weighting.eq('equal')]
    indexed = frame.set_index([*KEYS, 'variant'])
    lines = []
    for part in parts:
        lines.extend([f'### {part}\n',
                      '| reading | end | G3+ | weights | published | brief category rule | Mexico-only Δ | US-only Δ | joint Δ | ruled | $5bn bar (MX / US / joint) |',
                      '|---|---|---|---|---:|---:|---:|---:|---:|---:|---|'])
        for key in frame[KEYS].drop_duplicates().itertuples(index=False, name=None):
            rows = {variant: indexed.loc[(*key, variant)] for variant in VARIANTS}
            deltas = [float(rows[v][f'delta_{part}']) for v in ('mexico_only', 'us_only', 'both')]
            bar = ' / '.join('over' if abs(d) >= 5 else 'under' for d in deltas)
            reading, end, bound, weighting = key
            numbers = [float(rows['published'][part]), float(rows['brief_category'][part]),
                       *deltas, float(rows['both'][part])]
            lines.append(f'| {reading} | {end} | {bound} | {weighting} | '
                         + ' | '.join(f'{n:+.6f}' for n in numbers) + f' | {bar} |')
        lines.append('')
    return '\n'.join(lines)


def append_exact(path, heading, text):
    previous = path.read_text() if path.exists() else '**Verdict:** Operator price ruling implemented.\n'
    if heading in previous:
        if text not in previous:
            raise SystemExit(f'[BLOCKED] price-ruling record already exists with different bytes: {path}')
        return
    with path.open('a') as stream:
        stream.write('\n\n' + text + '\n')


def validate_coverage(frame, receipt):
    if set(frame.reading) != set(receipt['readings']) or len(frame) != receipt['rows']:
        raise SystemExit('[BLOCKED] missing whole reading or wrong declared row count')
    if frame.duplicated([*KEYS, 'variant']).any():
        raise SystemExit('[BLOCKED] duplicate price-ruling comparison cells')
    for name, group in frame.groupby('reading'):
        expected = len(VARIANTS) * 2 * 2 * len(WEIGHTS)
        if (len(group) != expected or set(group.variant) != set(VARIANTS)
                or set(group.account_end) != {'low', 'high'} or set(group.g3_bound) != {'zero', 'upper'}
                or set(group.weighting) != WEIGHTS):
            raise SystemExit(f'[BLOCKED] incomplete price-ruling coverage: {name}')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--timestamp', required=True)
    parser.add_argument('--append-result', type=Path)
    parser.add_argument('--append-log', type=Path)
    args = parser.parse_args()
    source = args.data / 'operator_price_changes_v7.csv'
    frame = pd.read_csv(source)
    receipt = json.loads((args.data / 'operator_price_receipt.json').read_text())
    validate_coverage(frame, receipt)
    columns = [*PARTS, *(f'delta_{p}' for p in PARTS)]
    if not np.isfinite(frame[columns]).all().all():
        raise SystemExit('[BLOCKED] nonfinite price-ruling values')
    factors = pd.read_csv(args.data / 'operator_us_service_factors_v7.csv').fillna('')
    mapping = factors[['line', 'cls', 'us_price_category', 'us_price_factor', 'us_price_reason']].drop_duplicates()
    heading = '## Operator price ruling — 2026-10-15 01:36 JST'
    intro = f'{heading}\n\nImplemented {args.timestamp}. This replaces fix 2\'s central rule; earlier price conclusions remain historical.\n\n'
    intro += 'Mexico\'s lost public receipts, saved budget and services forgone use GDP PPP for the entire budget, including cash and education. Household purchasing power and remittance recipients use consumption PPP; each reading keeps its stated private-pay counterfactual. Mexico\'s category-price arm is beside, labelled **Mexico\'s services at US prices**, together with the superseded brief\'s national/use service mixes.\n\n'
    intro += 'US cost-valued recipient services take US GDP price level / category price level, both World=100, ICP 2021 source 90. Actual US fiscal costs and receipt dollars stay fixed; the difference is recipient value lost (negative loss where the specified ratio exceeds one). Medicaid, housing vouchers, SNAP and explicit WTP arms are exempt. Reading 2 keeps its own health/social-services 3a; those already-priced lines are exempt from a second adjustment. Response-only quantities are selected before pricing.\n\n'
    intro += 'ICP 2021 price spreads are transported to 2024 [ASSUMPTION]. Utility and residual-enterprise category mappings are explicit coarse proxies; the line table names them. Education retains V=0 except in an explicitly cost-valued companion. Source JSON, URL, retrieval date and SHA256 are in `inputs/icp_us_pli_2021.json` and `inputs/pins.json`. [SOURCE: World Bank ICP 2021 source 90, PX.WL]\n\n'
    intro += 'These executed comparisons isolate prices on frozen v7 inputs, holding the published upstream compensation, pension, capital and G3+ definitions fixed. They are not an oct15 adoption or the joint round-2 result. Published R1 and every reading\'s centre matched the stored oracle within '
    intro += f'{receipt["published_max_abs_error_bn"]:.12g}bn; actual US fiscal-row error is {receipt["us_cost_max_abs_error_bn"]:.12g}bn. '
    intro += 'Both account ends, both G3+ bounds, all eight weightings and all four party totals appear in the CSV and full report. Every $5bn verdict is generated from abs(unrounded signed change) >= 5. [CALCULATION: operator_price_bridge.py; operator_price_changes_v7.csv]\n\n'
    intro += f'Full comparison: [{args.out.name}]({args.out}). Exact amounts: [{source.name}]({source}). '
    intro += f'Line receipts: [operator_us_service_factors_v7.csv]({args.data / "operator_us_service_factors_v7.csv"}).\n\n'
    full = intro + tables(frame)
    full += '\n### US line-to-category factors and exemptions\n\n'
    full += '| line | class | ICP heading | factor | rule / exemption |\n|---|---|---|---:|---|\n'
    for row in mapping.sort_values(['line', 'us_price_reason']).itertuples(index=False):
        full += f'| {row.line} | {row.cls} | {row.us_price_category or "exempt"} | {row.us_price_factor:.12f} | {row.us_price_reason} |\n'
    args.out.write_text(full)
    record = intro + tables(frame, parts=('world_total_bn',), equal_only=True)
    if args.append_result:
        append_exact(args.append_result, heading, record)
    if args.append_log:
        append_exact(args.append_log, heading, record)
    print(f'PRICE_DOCUMENT {len(frame)} comparison rows; {len(mapping)} distinct line/category/exemption entries')


if __name__ == '__main__':
    main()
