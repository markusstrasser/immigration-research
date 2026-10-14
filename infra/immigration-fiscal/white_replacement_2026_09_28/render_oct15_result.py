"""Append the dated one-engine comparator fixes; keep all earlier evidence."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
BLACK = HERE.parent / 'black_comparator_rough_2026_09_28'
MARKER = '<!-- oct15 second round-2 comparator fixes -->'
STAMP = '2026-10-15'


def render():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv')
    c = pd.read_csv(HERE / 'derived/symmetric_comparisons_oct15.csv')
    pop = pd.read_csv(BLACK / 'derived/symmetric_population_oct15.csv')
    job = pd.read_csv(HERE / 'derived/domestic_source_changes_oct15.csv')
    changes = pd.read_csv(HERE / 'derived/round2_changes_oct15.csv')
    lines = [MARKER, '', f'## Round-2 comparator fixes — {STAMP}', '',
        'This section supersedes the earlier mixed-engine comparison readings. Every gap uses '
        'the complete lineage and comparator on the rough engine at the personal ends. The exact case '
        'lineage is reported separately in the bridge, itemized by evaluated line, public-capital return, '
        'production and post-engine amount. [CALCULATION: symmetric_comparisons_oct15.csv; '
        'lineage_engine_bridge_oct15.csv]', '',
        'The two mortality conventions are lineage whole-population with comparators own-group '
        '(mixed conventions), and every group on its own mortality. The own-lineage sensitivity '
        'transports source coefficients onto live pension amounts and bounds the unresolved '
        'added-profile split; it is not an independent status-specific mortality remeasurement. '
        'Cash is unchanged. [CALCULATION: mortality_conventions.py; symmetric_audit_oct15.json]', '',
        '| Mortality / profile; accrual, $bn low / high | Rough lineage | White | White gap | Without item 11 | Case minus rough bridge |',
        '|---|---:|---:|---:|---:|---:|']
    readings = [('mixed mortality conventions', 'none'), ('own-group mortality', 'low'), ('own-group mortality', 'high')]
    def pair(frame, column):
        x = frame.set_index('end')
        return f"{x.loc['low', column]:.3f} / {x.loc['high', column]:.3f}"
    for convention, bound in readings:
        sel = d[(d.arm == 'combined_rules_only') & (d.basis == 'accrual')
                & (d.mortality_convention == convention) & (d.mortality_bound == bound)]
        comp = c[(c.arm == 'combined_rules_only') & (c.basis == 'accrual')
                 & (c.mortality_convention == convention) & (c.mortality_bound == bound)]
        lines.append(f"| {convention}, {bound} | {pair(sel[sel.group == 'mexican_origin_rough'], 'cost_bn')} | "
                     f"{pair(sel[sel.group == 'A1_third_plus_nh_white'], 'cost_bn')} | "
                     f"{pair(comp, 'white_gap_rough_lineage_bn')} | {pair(comp, 'white_gap_without_item11_bn')} | "
                     f"{pair(comp, 'case_minus_rough_bridge_bn')} |")
    lines += ['', 'Item 11 is measured for the lineage only; white and Black mixed-unit removal remains '
        'unmeasured. Every gap row carries this label and the exact lineage-only amount. Removing item 11 '
        'shows its arithmetic size; it does not measure the comparator counterpart. Item 10 also remains '
        'lineage-only. Comparator coverage remains absent under the recorded own-price source limitation. '
        '[DATA: symmetric_audit_oct15.json; CALCULATION: comparison_contract.py]', '',
        '| Black minus rough lineage; accrual, $bn low / high | Own count | Equal lineage count | Equal count without item 11 |',
        '|---|---:|---:|---:|']
    for convention, bound in readings:
        sub = pop[(pop.arm == 'combined_rules_only') & (pop.basis == 'accrual')
                  & (pop.mortality_convention == convention) & (pop.mortality_bound == bound)]
        own = sub[sub.population_basis == 'own_count']
        equal = sub[sub.population_basis == 'scaled_to_lineage']
        lines.append(f"| {convention}, {bound} | {pair(own, 'black_minus_rough_lineage_bn')} | "
                     f"{pair(equal, 'black_minus_rough_lineage_bn')} | {pair(equal, 'black_minus_lineage_without_item11_bn')} |")
    lines += ['', 'Equal-count Black costs hold each end’s per-person cost fixed at the lineage count '
        'from population_v8.with_coverage; own-count results are beside them. This linear accounting '
        'standardization does not solve a new CES removal. [CALCULATION: symmetric_population_oct15.csv]', '',
        '| Item 9, own job-capital domestic-source change ($bn) | Low | High |', '|---|---:|---:|']
    x = job[job.basis == 'accrual'].groupby(['group', 'end']).cost_change_bn.sum()
    for group in ('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages', 'nh_black_rough'):
        lines.append(f'| {group} | {x.loc[group, "low"]:.3f} | {x.loc[group, "high"]:.3f} |')
    lines += ['', '| Status and pension fixes; accrual, $bn low / high | Before cost | Bracket only change | Payroll only change | Joint change | Exact scenario selection change | After cost |',
        '|---|---:|---:|---:|---:|---:|---:|']
    for group in ('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages',
                  'A4_third_plus_nh_white_stationary', 'nh_black_rough'):
        sub = changes[(changes.group == group) & (changes.basis == 'accrual')]
        values = [pair(sub, column) for column in ('before_cost_bn', 'bracket_rerake_change_bn',
            'payroll_denominator_change_bn', 'joint_bracket_payroll_change_bn',
            'scenario_pension_selection_change_bn', 'after_cost_bn')]
        lines.append('| ' + group + ' | ' + ' | '.join(values) + ' |')
    lines += ['', 'The bracket and payroll cells hold the other fix off; the joint cell applies both. '
        'The final scenario selection step includes the exact civilian record mask, population scaling and '
        'A3/A4 age weights; it is not an isolated age effect. Pension numerator conservation and status-input '
        'hash checks are enforced before selection. [CALCULATION: round2_changes_oct15.csv; '
        'mortality_comparators.py; status_keys_oct14.py]', '',
        'Reproduce with `sh infra/immigration-fiscal/white_replacement_2026_09_28/run_oct15.sh`. '
        'These are modeled annual removal costs. [CALCULATION: run_oct15.sh]', '']
    addition = '\n'.join(lines)
    for lane in (HERE, BLACK):
        path = lane / 'RESULT.md'
        old = path.read_text().split(MARKER)[0].rstrip()
        path.write_text(old + '\n\n' + addition.rstrip() + '\n')


if __name__ == '__main__':
    render()
