"""Append the live comparator tables after the marker; text before it is the RESULT's record and stays.

Round 4: the central gives the completed lineage precedence over comparator members and their children, prices each
comparator's own school districts, and retains own Census coverage and mortality. Prior overlap, half overlap,
district, row-8 and Black DA arms are beside. Every cost comparison prints its lineage cost and decomposition.
"""
from pathlib import Path
import json
import math
import pandas as pd
import comparison_contract as CC
import mortality_conventions as MC
from mortality_conventions import CENTRAL

HERE = Path(__file__).resolve().parent
BLACK = HERE.parent / 'black_comparator_rough_2026_09_28'
MARKER = '<!-- oct15 C40 measured comparator mixed-unit removal -->'
STAMP = '2026-10-15'
READINGS = [  # arm, mortality convention, profile bound, label
    ('combined_rules_members', MC.OWN, 'low', 'Central: children rule, own coverage, own mortality (lineage profile bound low)'),
    ('combined_rules_members', MC.OWN, 'high', 'Central, lineage profile bound high'),
    ('combined_rules_members_general', MC.GENERAL, 'none', 'Beside: the same at whole-population mortality'),
    ('combined_rules_coverage', MC.OWN, 'low', 'Beside: current rule (children stay), own coverage, own mortality (bound low)'),
    ('combined_rules_coverage', MC.OWN, 'high', 'Beside: current rule, bound high'),
    ('combined_rules_only', MC.OWN, 'low', 'Beside: current rule, comparators without coverage, own mortality (bound low)'),
    ('combined_rules_members', MC.MIXED, 'none', 'Labelled, not for claims: lineage at whole-population, comparators at own mortality'),
]


def pair(frame, column, sign=1.):
    if column not in frame:
        raise SystemExit(f'[BLOCKED] reporting field missing: {column}')
    x = frame.set_index('end')
    if set(x.index) != {'low', 'high'} or not x.index.is_unique:
        raise SystemExit('[BLOCKED] reporting endpoint pair is not unique')
    values = pd.to_numeric(x[column], errors='coerce')
    if values.isna().all():
        if column.endswith('_se_bn') or column == 'se':
            return 'not computed'
        raise SystemExit(f'[BLOCKED] reporting endpoint missing or nonfinite: {column}')
    if not values.map(math.isfinite).all():
        raise SystemExit(f'[BLOCKED] reporting endpoint missing or nonfinite: {column}')
    return f"{sign * values.loc['low']:.3f} / {sign * values.loc['high']:.3f}"


def select(frame, arm, convention, bound, basis, **more):
    sub = frame[(frame.arm == arm) & (frame.mortality_convention == convention) & (frame.mortality_bound == bound)
                & (frame.basis == basis)]
    for k, v in more.items():
        sub = sub[sub[k] == v]
    if len(sub) != 2:
        raise SystemExit(f'[BLOCKED] reading {arm}/{convention}/{bound}/{basis} {more} is not one row per end')
    return sub


DECOMPOSITION = [('comparison_lineage_cost_bn', 'comparison'), ('case_headline_cost_bn', 'headline'),
                 ('lineage_children_block_bn', 'children block'), ('lineage_children_item11_bn', 'children item 11'),
                 ('lineage_mortality_delta_bn', 'own mortality'), ('case_minus_rough_bridge_bn', 'case − rough bridge')]


def lineage_decomposition(frame):
    if 'lineage_mortality_delta_bn' not in frame and 'mortality_delta_bn' in frame:
        frame = frame.assign(lineage_mortality_delta_bn=frame.mortality_delta_bn)
    if any(column not in frame or pd.to_numeric(frame[column], errors='coerce').isna().any()
           for column, _ in DECOMPOSITION):
        raise SystemExit('[BLOCKED] comparison lineage decomposition is incomplete')
    parts = [f'{label}: {pair(frame, column)}' for column, label in DECOMPOSITION]
    for field, label in [('lineage_school_price_transfer_bn', 'assumed education calibration'),
                         ('lineage_policy_delta_bn', 'policy change')]:
        if field in frame and frame[field].fillna(0.).ne(0.).any():
            parts.append(f'{label}: {pair(frame, field)}')
    return '<br>'.join(parts)


def comparison_table(lines, comparisons, black, readings):
    lines += ['| Reading, $bn low / high end | Set | Lineage − as many whites | Black − lineage, Black\'s count | '
              'Black − lineage, lineage\'s count | Lineage cost and decomposition, $bn low / high | Stated claim |',
              '|---|---|---:|---:|---:|---|---|']
    for arm, convention, bound, label in readings:
        for basis in ('accrual', 'cash'):
            sub = select(comparisons, arm, convention, bound, basis)
            own = select(black, arm, convention, bound, basis, population_basis='own_count')
            equal = select(black, arm, convention, bound, basis, population_basis='scaled_to_lineage')
            white_gap = '—' if arm.endswith('_half_black') else pair(sub, 'white_gap_rough_lineage_bn')
            own_gap = '—' if arm.endswith('_half_white') else pair(own, 'black_minus_rough_lineage_bn')
            equal_gap = '—' if arm.endswith('_half_white') else pair(equal, 'black_minus_rough_lineage_bn')
            claim = 'yes' if MC.stated(convention) else 'no (mixed pair)'
            lines.append(f'| {label} | {basis} | {white_gap} | {own_gap} | {equal_gap} | '
                         f'{lineage_decomposition(sub)} | {claim} |')


def black_coverage_table(lines, comparisons, black):
    lines += ['', '### Black coverage: demographic analysis beside the PES central', '',
              'The 2020 PES stays central for every group. The two demographic-analysis (DA) arms change Black\'s '
              'coverage only; the lineage retains its PES. The envelope prints the two DA arms\' minimum and maximum '
              'at each cost endpoint. [DATA: symmetric_population_oct15.csv; members_coverage_oct15.json]', '',
              '| Coverage and lineage profile bound | Set | Black true count | Black − lineage, Black\'s count, $bn low / high | '
              'Black − lineage, lineage\'s count, $bn low / high | Lineage cost and decomposition, $bn low / high |',
              '|---|---|---:|---:|---:|---|']
    arms = [('combined_rules_members', 'PES central'), ('combined_rules_members_da_middle', 'DA middle'),
            ('combined_rules_members_da_all_black', 'DA all Black')]
    for bound in ('low', 'high'):
        for basis in ('accrual', 'cash'):
            da = []
            for arm, label in arms:
                sub = select(comparisons, arm, MC.OWN, bound, basis)
                own = select(black, arm, MC.OWN, bound, basis, population_basis='own_count')
                equal = select(black, arm, MC.OWN, bound, basis, population_basis='scaled_to_lineage')
                lines.append(f'| {label}, bound {bound} | {basis} | {own.population.iloc[0]:,.0f} | '
                             f"{pair(own, 'black_minus_rough_lineage_bn')} | {pair(equal, 'black_minus_rough_lineage_bn')} | "
                             f'{lineage_decomposition(sub)} |')
                if arm != 'combined_rules_members':
                    da.append((own.set_index('end'), equal.set_index('end')))
            def envelope(index):
                return ' / '.join(f"{min(float(x[index].loc[e, 'black_minus_rough_lineage_bn']) for x in da):.3f}–"
                                  f"{max(float(x[index].loc[e, 'black_minus_rough_lineage_bn']) for x in da):.3f}"
                                  for e in ('low', 'high'))
            central = select(comparisons, 'combined_rules_members', MC.OWN, bound, basis)
            lines.append(f'| DA envelope, bound {bound} | {basis} | — | {envelope(0)} | {envelope(1)} | '
                         f'{lineage_decomposition(central)} |')


def change_table(lines, comparisons, black):
    lines += ['', '### Isolated and joint changes from the stated baseline', '',
              'Each entry is the central minus the named otherwise-identical baseline. SEs in the item-11 table '
              'describe level contrasts; a sampling SE for these changes is not computed. [CALCULATION: differences '
              'of symmetric_comparisons_oct15.csv and symmetric_population_oct15.csv]', '',
              '| Change and profile bound | Set | Change in lineage − as many whites, $bn low / high | '
              'Change in Black − lineage, Black\'s count, $bn low / high | '
              'Change in Black − lineage, lineage\'s count, $bn low / high | '
              'Central lineage cost and decomposition, $bn low / high |', '|---|---|---:|---:|---:|---|']
    for arm, label in [('combined_rules_members_round3', 'Lineage precedence'),
                       ('combined_rules_members_no_district', 'Own district prices'),
                       ('combined_rules_members_round3_no_district', 'Precedence + own district prices, joint'),
                       ('combined_rules_members_no_row8', 'Per-head row-8 correction'),
                       ('combined_rules_members_partial_lineage', 'Full lineage survivor solve')]:
        for bound in ('low', 'high'):
            for basis in ('accrual', 'cash'):
                central = select(comparisons, 'combined_rules_members', MC.OWN, bound, basis)
                base = select(comparisons, arm, MC.OWN, bound, basis).set_index('end')
                delta = central.copy()
                column = 'white_gap_rough_lineage_bn'
                delta[column] -= delta.end.map(base[column])
                cells = [pair(delta, column)]
                for count in ('own_count', 'scaled_to_lineage'):
                    current = select(black, 'combined_rules_members', MC.OWN, bound, basis, population_basis=count).copy()
                    previous = select(black, arm, MC.OWN, bound, basis, population_basis=count).set_index('end')
                    column = 'black_minus_rough_lineage_bn'
                    current[column] -= current.end.map(previous[column])
                    cells.append(pair(current, column))
                lines.append(f'| {label}, bound {bound} | {basis} | ' + ' | '.join(cells) +
                             f' | {lineage_decomposition(central)} |')


def item11_table(lines, whites, black, results):
    lines += ['', '### Item 11: own count and lineage count, with uncertainty', '',
              'SEs condition on the selected coverage factors, population counts and reweighting factors. Comparator '
              'SE is the correction alone; paired SE is the signed lineage-minus-comparator replicate contrast. '
              'An unavailable expanded-lineage vector prints “not computed”. [CALCULATION: comparison_contract.py; '
              'DATA: symmetric_white_population_oct15.csv; symmetric_population_oct15.csv]', '',
              '| Group, coverage, profile bound | Set | Count basis | Population | Item 11, $bn low / high | '
              'Comparator SE, $bn low / high | Lineage SE, $bn low / high | Paired SE, $bn low / high |',
              '|---|---|---|---:|---:|---:|---:|---:|']
    for group, frame, frames in [('A1 white', whites, ('own_count', 'lineage_count')),
                                 ('Black', black, ('own_count', 'scaled_to_lineage'))]:
        arms = [('combined_rules_members', 'PES central'),
                ('combined_rules_members_partial_lineage', 'old partial lineage survivor patch')]
        if group == 'Black':
            arms += [('combined_rules_members_da_middle', 'DA middle'), ('combined_rules_members_da_all_black', 'DA all Black')]
        for arm, label in arms:
            for bound in ('low', 'high'):
                for basis in ('accrual', 'cash'):
                    for count_basis in frames:
                        rows = select(frame, arm, MC.OWN, bound, basis, population_basis=count_basis)
                        lines.append(f'| {group}, {label}, bound {bound} | {basis} | {count_basis} | '
                                     f"{rows.population.iloc[0]:,.0f} | {pair(rows, 'comparator_item11_bn')} | "
                                     f"{pair(rows, 'item11_comparator_se_bn')} | {pair(rows, 'lineage_item11_se_bn')} | "
                                     f"{pair(rows, 'item11_paired_se_bn')} |")
    for arm, rule in [('combined_rules_members', 'children, PES central'),
                      ('combined_rules_coverage', 'current, PES central')]:
        for group, label in [('A3_third_plus_nh_white_at_union_ages', 'A3 reweighted'),
                             ('A4_third_plus_nh_white_stationary', 'A4 reweighted')]:
            for bound in ('low', 'high'):
                for basis in ('accrual', 'cash'):
                    rows = select(results, arm, MC.OWN, bound, basis, group=group)
                    for count_basis, population, prefix in [('own_count', 'true_own_count', 'own_count_'),
                                                             ('lineage_count', 'population', '')]:
                        amount = prefix + 'item11_bn' if prefix else 'comparator_item11_bn'
                        lines.append(f'| {label}, {rule}, bound {bound} | {basis} | {count_basis} | '
                                     f"{rows[population].iloc[0]:,.0f} | {pair(rows, amount)} | "
                                     f"{pair(rows, prefix + 'item11_comparator_se_bn')} | "
                                     f"{pair(rows, 'lineage_item11_se_bn')} | "
                                     f"{pair(rows, prefix + 'item11_paired_se_bn')} |")


def precedence_table(lines, counts):
    precedence = counts.get('precedence')
    if not precedence:
        raise SystemExit('[BLOCKED] reporting needs the lineage-precedence membership counts')
    lines += ['', '### Observed own members under the three overlap rules', '',
              'Survey-weighted counts; coverage is applied separately. Half overlap divides both person weight and '
              'cost equally; the two half-overlap lineage counts are pair-specific. Each alternative comparator '
              'has zero survey-weight overlap with the lineage under the central rule. A1 and Black are pairwise '
              'comparison alternatives, not a simultaneous partition. '
              '[DATA: members_coverage_oct15.json, counts.precedence]', '',
              '| Comparator | Round 3, child in both | Lineage precedence (central) | Half overlap | Overlap | '
              'Lineage under round 3 / precedence | Lineage under half overlap |', '|---|---:|---:|---:|---:|---:|---:|']
    for group, label in [('A1_third_plus_nh_white', 'A1 white'), ('nh_black_rough', 'Black')]:
        row = precedence[group]
        lines.append(f"| {label} | {row['round3']:,.0f} | {row['lineage_precedence']:,.0f} | {row['half_overlap']:,.0f} | "
                     f"{row['overlap']:,.0f} | {row['lineage_observed']:,.0f} | {row['lineage_half_overlap']:,.0f} |")


def reweighted_table(lines, comparisons, results):
    lines += ['', '### A3 and A4 on the children and coverage rules, beside', '',
              'A3/A4 remain reweighted readings, conditional on survivor terms being uniform per departing member '
              'within each mixed tax unit, SPM unit or household. Their factors use the reconstructed observed '
              'membership weights; missed coverage people add no item 11. A2 and the all-residents slice remain '
              'current-rule readings: A2\'s own mixed-unit mask was not solved, and a population slice is not a '
              'membership definition. The contract refuses both as centrals. [CALCULATION: comparison_contract.py]', '',
              '| Reweighted comparator and rule, profile bound | Set | Lineage − as many comparator members, $bn low / high | '
              'Comparator item 11, $bn low / high | Comparator SE, $bn low / high | Paired SE, $bn low / high | '
              'Lineage cost and decomposition, $bn low / high |', '|---|---|---:|---:|---:|---:|---|']
    for arm, rule in [('combined_rules_members', 'children, own coverage'), ('combined_rules_coverage', 'current, own coverage')]:
        for group, label in [('A3_third_plus_nh_white_at_union_ages', 'A3, lineage ages'),
                             ('A4_third_plus_nh_white_stationary', 'A4, stationary ages')]:
            CC.require_central_reading(group)
            for bound in ('low', 'high'):
                for basis in ('accrual', 'cash'):
                    sub = select(comparisons, arm, MC.OWN, bound, basis)
                    rows = select(results, arm, MC.OWN, bound, basis, group=group).copy()
                    lineage = sub.set_index('end')
                    rows['reweighted_gap_bn'] = rows.end.map(lineage.comparison_lineage_cost_bn) - rows.cost_bn
                    lines.append(f'| {label}; {rule}; bound {bound} | {basis} | '
                                 f"{pair(rows, 'reweighted_gap_bn')} | {pair(rows, 'comparator_item11_bn')} | "
                                 f"{pair(rows, 'item11_comparator_se_bn')} | {pair(rows, 'item11_paired_se_bn')} | "
                                 f'{lineage_decomposition(sub)} |')


def render():
    c = pd.read_csv(HERE / 'derived/symmetric_comparisons_oct15.csv')
    pop = pd.read_csv(BLACK / 'derived/symmetric_population_oct15.csv')
    whites = pd.read_csv(HERE / 'derived/symmetric_white_population_oct15.csv')
    results = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv')
    source = CC.load_mixed_unit()
    central = c[c.central.astype(bool)]
    if set(central.arm) != {CENTRAL['arm']} or set(central.mortality_convention) != {CENTRAL['mortality_convention']}:
        raise SystemExit('[BLOCKED] the central comparison rows are not the declared central reading')
    CC.require_stated(CENTRAL['mortality_convention'])
    lines = [MARKER, '',
        f'## Comparators after round 4 (R4C4) — {STAMP}', '',
        'This section is regenerated by `render_oct15_result.py`; it replaces the R2C40 tables that stood here earlier '
        'on 2026-10-15 (git keeps them). Each comparator carries its own 2020 '
        'Census coverage by age and sex, members\' biological minor children outside a group\'s definition depart with '
        'them and count as members. The central gives the completed lineage and its added-child universe precedence: '
        'a person belongs to one group. Comparators\' K-12 lines carry their own race-specific school-district prices '
        'on the case\'s F-33 × CCD vintage; the lineage retains the case\'s school price. Group survival factors move '
        'only the retirement share of the accrual, '
        'and A3/A4 take A1\'s item 11 reweighted. [CALCULATION: symmetric_comparators_oct14.py; members_coverage_oct15.py; '
        'school_key_oct15.py; district_prices_oct15.py; lineage_mortality_mix_oct15.py; comparison_contract.py]', '',
        '[FRAMING-SENSITIVE] Whole-person static removal on the rough engine on both sides; conditional 2024 modeled '
        'amounts. "As many whites" scales A1\'s per-person cost to the lineage\'s true count (its own coverage and the '
        'children rule included); Black is shown at its own true count and at the lineage\'s. A stated claim uses a '
        'reading with one mortality convention on both sides; the mixed pair is labelled and refused by the guard '
        '(`comparison_contract.require_stated`). Uncertainty below concerns item 11 only; it is not a paired SE for '
        'the whole modeled fiscal cost. [DATA: symmetric_comparisons_oct15.csv; symmetric_population_oct15.csv]', '']
    comparison_table(lines, c, pop, READINGS)
    lines += ['', 'The bridge column is the case engine\'s lineage cost less the rough engine\'s on the same reading: '
              'row-13 lines and the exact keys the rough engine does not carry. The comparison itself is rough on both '
              'sides. The cost cell explicitly prints the comparison lineage beside the case headline, its children '
              'block and item 11, its mortality change, and the case-minus-rough bridge. Those components are read '
              'from each row; the headline is not substituted for the comparison lineage. '
              'Diagnostic arms\' intentional changes to the case appear as a separate policy delta when nonzero. '
              'Both engines already carry the measured school repricing; the remaining education_services '
              'case-minus-rough residual is an incidence difference, not an identified district-price correction. '
              'The central preserves it in the bridge. R4_LINEAGE_SCHOOL_BRIDGE=1 separately enables an assumed '
              'whole-education calibration; any school-transfer amount under that switch is already included '
              'in the headline-minus-bridge decomposition. '
              '[CALCULATION: lineage_engine_bridge_oct15.csv closes the bridge line by line to 1e-9bn]', '',
              '### Isolated changes and overlap rules, beside', '',
              'The no-district and round-3 arms isolate each change with other round-4 corrections held fixed. The '
              'round-3/no-district arm is their joint baseline; half-overlap arms are pair-specific endpoint '
              'interpolations that halve the shared children\'s person weight and cost. The partial-lineage arm '
              'retains the old federal-and-benefit patch beside the full expanded-lineage survivor solve; all '
              'other rules stay fixed. [CALCULATION: symmetric_comparators_oct14.py]', '']
    diagnostics = []
    for arm, label in [('combined_rules_members_round3', 'Round-3 overlap, own district prices'),
                       ('combined_rules_members_no_district', 'Lineage precedence, district prices off'),
                       ('combined_rules_members_round3_no_district', 'Round-3 overlap, district prices off (joint baseline)'),
                       ('combined_rules_members_no_row8', 'Per-head row-8 correction off'),
                       ('combined_rules_members_partial_lineage', 'Old partial lineage survivor patch'),
                       ('combined_rules_members_half_white', '50/50 overlap: lineage and A1'),
                       ('combined_rules_members_half_black', '50/50 overlap: lineage and Black')]:
        diagnostics.extend((arm, MC.OWN, bound, f'{label}, profile bound {bound}') for bound in ('low', 'high'))
    comparison_table(lines, c, pop, diagnostics)
    change_table(lines, c, pop)
    members = json.loads((HERE / 'derived/members_coverage_oct15.json').read_text())
    precedence_table(lines, members['counts'])
    controls = members['controls']
    lines += ['', f"A1 and Black alternatives themselves share {controls['alternative_white_black_overlap_people']:,.2f} "
              'observed, survey-weighted people under the children rule. The zero-overlap gate applies to each '
              'lineage/comparator pair. [DATA: members_coverage_oct15.json, controls.alternative_white_black_overlap_people '
              'and controls.overlap_gate_scope]', '']
    black_coverage_table(lines, c, pop)
    item11_table(lines, whites, pop, results)
    reweighted_table(lines, c, results)
    lines += ['',
              '### A1 white at its own count', '',
              'A1 at its own count is a different population from the lineage: not an as-many comparison. It is shown '
              'for scale only. [DATA: symmetric_white_population_oct15.csv, population_warning]', '',
              '| Reading | Set | A1 own count | Lineage − A1 at its own count, $bn low / high | '
              'Lineage cost and decomposition, $bn low / high |', '|---|---|---:|---:|---|']
    for arm, convention, bound, label in READINGS[:1] + READINGS[3:4]:
        for basis in ('accrual', 'cash'):
            sub = select(whites, arm, convention, bound, basis, population_basis='own_count')
            lines.append(f"| {label} | {basis} | {sub.population.iloc[0]:,.0f} | {pair(sub, 'lineage_minus_comparator_bn')} | "
                         f'{lineage_decomposition(sub)} |')
    lines += ['', '### Base route (not the comparison central)', '',
              'The mixed-unit lane\'s own gaps on the base route: whole-population mortality, the original status and '
              'production rules, the current membership rule, no comparator coverage. Kept as that lane\'s record; '
              'the tables above supersede it for every comparison claim. [DATA: ../mixed_unit_comparators_2026_10_15/derived/gaps.csv]', '',
              '| Base route: group, set, count | Lineage − comparator, measured both sides, $bn low / high | '
              'Comparator item 11 at zero | Lineage cost and decomposition, $bn low / high |', '|---|---:|---:|---|']
    gaps = pd.DataFrame(source['gaps'])
    targets = json.loads((CC.MIXED_SOURCE / 'comparator_targets.json').read_text())
    for group in ('white', 'black'):
        for method in ('set', 'cash'):
            for frame in ('own_count', 'lineage_count'):
                sub = gaps[(gaps.group == group) & (gaps.method == method) & (gaps.population_basis == frame)].copy()
                for col in ('both_sided_rough_gap_bn', 'one_sided_rough_gap_bn'):
                    sub[col] = pd.to_numeric(sub[col])
                for name, _ in DECOMPOSITION:
                    sub[name] = 0.
                for i, row in sub.iterrows():
                    target = targets[group][method][row.end]
                    sub.loc[i, 'comparison_lineage_cost_bn'] = target['rough_lineage_cost_bn']
                    sub.loc[i, 'case_headline_cost_bn'] = target['case_lineage_cost_bn']
                    sub.loc[i, 'case_minus_rough_bridge_bn'] = target['case_lineage_cost_bn'] - target['rough_lineage_cost_bn']
                lines.append(f"| {group}, {method}, {frame} | {pair(sub, 'both_sided_rough_gap_bn')} | "
                             f"{pair(sub, 'one_sided_rough_gap_bn')} | {lineage_decomposition(sub)} |")
    lines += ['', '### Remaining measured and unmeasured asymmetries', '',
              '- The lineage school price retains the measured school-level premium of 0.56797% (about $0.8bn on '
              'the $143bn school base); comparator school-level mixes are unmeasured. Each group now carries its '
              'own measured district differential. [DATA: district_prices_oct15.json; '
              '../school_cost_where_enrolled_2026_09_24/derived/within_district.json]',
              '- The education-benefits bridge is −$2.036694bn at both ends. The case\'s state-priced per-head '
              'component P and the comparator\'s low-income college key differ; higher education also carries the '
              'comparators\' IPEDS re-key. Component P is non-school state-local capital, so no existing October '
              'college-enrollment key can simply be ported to remove this difference. '
              '[CALCULATION: lineage_engine_bridge_oct15.csv; ../full_account_spending_2026_09_20/builder.py; '
              '../generation_account_2026_09_24/keys.py; rekey_sept29.py]',
              '- The CPS cannot identify adult comparator descendants living apart from member parents. Added '
              'comparator descendants are biological minors; the lineage\'s whole-person descent frame includes '
              'adult descendants. This remaining difference is unmeasured. [ASSUMPTION; measurement limit]', '']
    lines += ['', 'Reproduce with `sh infra/immigration-fiscal/white_replacement_2026_09_28/run_oct15.sh`. '
              'The SHA256 pins stop `[BLOCKED]` on a changed summary or paired-SE source. [CALCULATION: run_oct15.sh]', '']
    addition = '\n'.join(lines)
    for lane in (HERE, BLACK):
        path = lane / 'RESULT.md'
        old = path.read_text().split(MARKER)[0]
        separator = '' if old.endswith('\n\n') else ('\n' if old.endswith('\n') else '\n\n')
        path.write_text(old + separator + addition.rstrip() + '\n')


if __name__ == '__main__':
    render()
