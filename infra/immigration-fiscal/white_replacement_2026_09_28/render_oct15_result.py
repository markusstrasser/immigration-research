"""Append the measured C40 comparison; retain earlier round-2 evidence."""
from pathlib import Path
import pandas as pd
import comparison_contract as CC

HERE = Path(__file__).resolve().parent
BLACK = HERE.parent / 'black_comparator_rough_2026_09_28'
MARKER = '<!-- oct15 C40 measured comparator mixed-unit removal -->'
STAMP = '2026-10-15'


def render():
    c = pd.read_csv(HERE / 'derived/symmetric_comparisons_oct15.csv')
    pop = pd.read_csv(BLACK / 'derived/symmetric_population_oct15.csv')
    source = CC.load_mixed_unit()
    lines = [MARKER, '', f'## Measured comparator mixed-unit removal (R2C40) — {STAMP}', '',
        'This section supersedes every earlier C40 reading with the comparator side at zero. '
        'Item 11 now enters A1 White and Black published costs after evaluation. The evaluator remains '
        'the unadjusted M5 calibration input. Other membership or age-standardized White definitions '
        '(A2/A3/A4) remain unmeasured; their own-age removal term is not silently reused. '
        '[CALCULATION: comparison_contract.py; symmetric_comparators_oct14.py]', '',
        '[FRAMING-SENSITIVE] Both sides rest on whole-person static removal. These are conditional '
        '2024 modeled amounts, with current-year survivor terms in both sets and no spousal-pension model. '
        'Only the item11 gap uncertainty is reported: it uses the signed lineage-minus-comparator '
        'replicate vectors in the pinned source gaps.csv, never component-SE quadrature. '
        '[DATA: ../mixed_unit_comparators_2026_10_15/derived/{white,black}_summary.json and gaps.csv]', '',
        '| Own-mask item11, $bn | Low / high | Own count |', '|---|---:|---:|',
        '| A1 White | -35.394141 / -17.804446 | 173,053,897.03 |',
        '| Black | -2.333671 / +0.646664 | 41,954,493.92 |', '',
        'A1 scales by the exact live lineage count / own count; Black central stays at its own count. '
        'Both groups also have separately labeled population standardizations. All contrasts below '
        'use the rough engine on both sides; the exact case-minus-rough bridge remains separate. '
        'Completion and coverage remain lineage-specific under the earlier source limitations. '
        '[CALCULATION: symmetric_comparisons_oct15.csv; symmetric_population_oct15.csv; '
        'symmetric_white_population_oct15.csv; lineage_engine_bridge_oct15.csv]', '',
        '| Basis / mortality / profile; lineage-minus-comparator, $bn low / high | A1 at lineage count | Black own count | Black at lineage count |',
        '|---|---:|---:|---:|']
    def pair(frame, column, sign=1.):
        x = frame.set_index('end')
        return f"{sign * x.loc['low', column]:.6f} / {sign * x.loc['high', column]:.6f}"
    readings = [('mixed mortality conventions', 'none'), ('own-group mortality', 'low'), ('own-group mortality', 'high')]
    for basis in ('accrual', 'cash'):
        for convention, bound in readings:
            sub = c[(c.arm == 'combined_rules_only') & (c.basis == basis)
                    & (c.mortality_convention == convention) & (c.mortality_bound == bound)]
            black = pop[(pop.arm == 'combined_rules_only') & (pop.basis == basis)
                        & (pop.mortality_convention == convention) & (pop.mortality_bound == bound)]
            own = black[black.population_basis == 'own_count']
            equal = black[black.population_basis == 'scaled_to_lineage']
            lines.append(f"| {basis}, {convention}, {bound}: measured both sides | {pair(sub, 'white_gap_rough_lineage_bn')} | {pair(own, 'black_minus_rough_lineage_bn', -1)} | {pair(equal, 'black_minus_rough_lineage_bn', -1)} |")
            lines.append(f"| One-sided gap (comparator item11 at zero) | {pair(sub, 'white_gap_one_sided_bn')} | {pair(own, 'black_minus_lineage_one_sided_bn', -1)} | {pair(equal, 'black_minus_lineage_one_sided_bn', -1)} |")
            lines.append(f"| Item11 paired gap SE (conditional, not full-cost SE) | {pair(sub, 'white_item11_paired_se_bn')} | {pair(own, 'item11_paired_se_bn')} | {pair(equal, 'item11_paired_se_bn')} |")
    lines += ['', 'The measured own-count and equal-count base-route gaps are also retained in the '
        'pinned source below. This base route uses whole-population mortality and its original status/production '
        'rules; it is distinct from the combined-rule sensitivities above. [DATA: source gaps.csv]', '',
        '| Base route / basis / count, $bn low / high | Measured both sides |', '|---|---:|']
    gaps = pd.DataFrame(source['gaps'])
    for group in ('white', 'black'):
        for method in ('set', 'cash'):
            for frame in ('own_count', 'lineage_count'):
                sub = gaps[(gaps.group == group) & (gaps.method == method) & (gaps.population_basis == frame)].copy()
                for col in ('both_sided_rough_gap_bn', 'one_sided_rough_gap_bn'):
                    sub[col] = pd.to_numeric(sub[col])
                lines.append(f"| {group}, {method}, {frame}: measured both sides | {pair(sub, 'both_sided_rough_gap_bn')} |")
                lines.append(f"| One-sided gap (comparator item11 at zero) | {pair(sub, 'one_sided_rough_gap_bn')} |")
    lines += ['', 'Reproduce with `sh infra/immigration-fiscal/white_replacement_2026_09_28/run_oct15.sh`. '
              'The SHA256 pins stop `[BLOCKED]` on a changed summary or paired-SE source. [CALCULATION: run_oct15.sh]', '']
    addition = '\n'.join(lines)
    for lane in (HERE, BLACK):
        path = lane / 'RESULT.md'
        old = path.read_text().split(MARKER)[0].rstrip()
        path.write_text(old + '\n\n' + addition.rstrip() + '\n')


if __name__ == '__main__':
    render()
