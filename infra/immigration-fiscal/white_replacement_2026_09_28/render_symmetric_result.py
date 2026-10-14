"""Render the P7 comparator evidence tables without replacing historical records."""
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent
BLACK = HERE.parent / 'black_comparator_rough_2026_09_28'
MARKER = '<!-- P7 symmetric comparator evidence -->'


def pair(d, group, arm, col):
    rows = d[(d.group == group) & (d.arm == arm) & (d.basis == 'accrual')].set_index('end')
    return f"{rows.loc['low', col]:.3f} / {rows.loc['high', col]:.3f}"


def render():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct14.csv')
    c = pd.read_csv(HERE / 'derived/symmetric_comparisons_oct14.csv').query("basis == 'accrual'")
    h = pd.read_csv(HERE / 'derived/symmetric_hispanic_arm_oct14.csv')
    pop = pd.read_csv(BLACK / 'derived/symmetric_population_oct14.csv')
    se = pd.read_csv(HERE / 'derived/symmetric_status_sampling_oct14.csv')
    verdict = '**Verdict:** Group-specific mortality materially lowers the Black comparator; exact full-case imputation symmetry remains unresolved. New tables correct production symmetry, status-only receipt rules, comparator pension eligibility/frame and scalar coverage, while preserving the frozen v7 and old rough outputs as controls.'
    lines = [verdict, MARKER, '', '## P7 comparator audit, 2026-10-14', '',
             'All dollar figures below are billions a year, personal allocation, v7 specifications 16 / 11. These are modeled annual removal/accounting costs, not observed lifetime contributions. Each row changes only its named policy from the current raw rough comparator. The identified union has 39.712M people; its lineage overlay brings it to 42.752M. White A1 uses that lineage count; Black keeps its own 41.954M count. [DATA: frozen case meta.lineage.counts; symmetric_results_oct14.csv/population]', '',
             '| One change from current rough central | Rough lineage change | A1 white change | Black change, own count |',
             '|---|---:|---:|---:|']
    for arm in ('production_own', 'production_zero', 'source_payroll_proxy', 'status_rules_fixed_union_benefits',
                'status_rules_coupled_accrual', 'mortality_group', 'accrual_row4', 'pension_symmetric_frame_status',
                'mortality_symmetric_frame_status', 'combined_rules_only', 'combined_zero_production'):
        lines.append(f"| {arm} | {pair(d, 'mexican_origin_rough', arm, 'change_from_raw_bn')} | {pair(d, 'A1_third_plus_nh_white', arm, 'change_from_raw_bn')} | {pair(d, 'nh_black_rough', arm, 'change_from_raw_bn')} |")
    lines += ['', '[CALCULATION: symmetric_comparators_oct14.py → derived/symmetric_results_oct14.csv. The $5bn review bar is evaluated in the CSV exceeds_5bn field, independently at each end; a comparator delta does not alter the frozen headline.]', '',
              'The own-production changes are below the bar; zero production for everyone moves the lineage over it at both ends. Mortality is over the bar for Black, below it for whites. Status-only receipt changes on the union exceed the bar; their fiscal effect depends on whether its already-earned pension liabilities are fixed or coupled to payer dollars. Source payroll proxy alone is a diagnostic, not an adopted correction. Row-4-only comparator ratios are below the bar. [CALCULATION: table and CSV]', '',
              '## Combined table and comparison denominators', '',
              '| Rule | Rough lineage cost | A1 white cost | Black cost, own count | White gap vs rough / case lineage, low | Black minus rough / case lineage, low |',
              '|---|---:|---:|---:|---:|---:|']
    for arm in ('legacy_raw', 'production_own', 'production_zero', 'combined_rules_only', 'combined_zero_production'):
        r = c[(c.arm == arm) & (c.end == 'low')].iloc[0]
        lines.append(f"| {arm} | {pair(d, 'mexican_origin_rough', arm, 'cost_bn')} | {pair(d, 'A1_third_plus_nh_white', arm, 'cost_bn')} | {pair(d, 'nh_black_rough', arm, 'cost_bn')} | {r.white_gap_rough_union_bn:.3f} / {r.white_gap_case_lineage_bn:.3f} | {r.black_minus_rough_union_bn:.3f} / {r.black_minus_case_lineage_bn:.3f} |")
    lines += ['', 'Both-end comparison columns are in symmetric_comparisons_oct14.csv. The old white gap 512.150 / 481.643 and Black-minus-lineage 106.980 / 103.326 use the rough lineage, not the frozen case. Holding the exact case numerator instead gives 535.937 / 507.498 and 83.194 / 77.472 before any comparator status correction. Those latter values alone reproduce the reviewer’s claimed “case-rule” gap, so they are not evidence of a newly executed all-group status rule. [CALCULATION: legacy_raw comparison rows]', '',
              '**Full row 13 remains unresolved.** The source averages matched hot-deck shares and a separate base × matched / pooled share ratio. That ratio is not additive over group partitions. No unique conserved all-group record vector is declared by the source. The new status arm applies the same origin-specific on-books flag/rules to every group’s records, using wage and a separate statutory self-payroll key. Income tax applies status after the existing personal IRS/CBO rake and renormalizes on row 4; it does not preserve the rake margins or reproduce the whole frozen aggregate imputation stack. All combined rows therefore carry full_row13_symmetric=false. A full matched replay was not substituted for the undeclared ratio extension. [DATA: combine_onbooks_lane.assemble; status_keys_oct14.build; ASSUMPTION: status after the carrier rake]', '',
              'Pension rows with basis=symmetric also apply the same all-origin source status and statutory payer definition to comparator eligibility and exclude military members. Pure mortality_group retains the old source frame to isolate the life-table change. The prior Black frame included military people and flagged unauthorized status only for Mexico-born people; those defects are independently corrected in the combined arm. General controls retain the original frames. The union’s frozen pension numerator remains fixed in the isolated status arm; the coupled arm uses exact engine cash/accrual payer-dollar rates including post-pension edits. Never multiply new payroll by the old R9 ratio calibrated to the raw payroll denominator. [DATA: mortality_comparators.symmetric_frame; status_keys_oct14.engine_accrual_rates]', '',
              '## Population standardization', '', '| Rule, accrual | Black own cost | At lineage count | Scaling increase | Per Black person |', '|---|---:|---:|---:|---:|']
    for arm in ('legacy_raw', 'combined_rules_only'):
        sub = pop[(pop.arm == arm) & (pop.basis == 'accrual')]
        own = sub[sub.population_basis == 'own_count'].set_index('end')
        scaled = sub[sub.population_basis == 'scaled_to_lineage'].set_index('end')
        p = lambda frame, col: f"{frame.loc['low', col]:.3f} / {frame.loc['high', col]:.3f}"
        lines.append(f"| {arm} | {p(own, 'cost_bn')} | {p(scaled, 'cost_bn')} | {p(scaled, 'scaling_delta_bn')} | ${own.loc['low','cost_per_person']:,.0f} / ${own.loc['high','cost_per_person']:,.0f} |")
    lines += ['', 'This is linear accounting standardization at fixed per-person amounts. It is not a new CES counterfactual for removing a larger group. All own/scaled populations and per-person values are printed in the Black lane’s symmetric_population_oct14.csv; every per-person equality passes at 1e-9. [CALCULATION: that file]', '',
              '## White measures for quoting', '', '| Arm, A1 whites | Allocated balance | Responsive budget cost | Resource cost incl. capital and production | Contribution to others |', '|---|---:|---:|---:|---:|']
    for arm in ('legacy_raw', 'combined_rules_only'):
        lines.append(f"| {arm} | {pair(d, 'A1_third_plus_nh_white', arm, 'allocated_balance_bn')} | {pair(d, 'A1_third_plus_nh_white', arm, 'responsive_budget_cost_bn')} | {pair(d, 'A1_third_plus_nh_white', arm, 'cost_bn')} | {pair(d, 'A1_third_plus_nh_white', arm, 'contribution_to_others_bn')} |")
    lines += ['', 'Allocated balance is all assigned receipts less assigned spending, before response assumptions. Responsive budget cost is spending saved less receipts lost. Resource cost adds the imputed return on public capital and subtracts the modeled production benefit. Contribution to others is its sign reversal, not the allocated balance. Neither capital return nor pension accrual is current borrowing. A2–A4, both bases and all arms are in symmetric_white_measures_oct14.csv. Exact full-row13 “case rules” is not an available measure. [CALCULATION: CSV fields; FRAMING-SENSITIVE: contribution as removal resource surplus]', '',
              '## Hispanic mortality arm beside the case', '',
              f"The identified-union 2026 payable/net Hispanic-proxy change is +{h.iloc[0].identified_delta_bn:.3f} at both ends. The added-profile extension is bounded at +{h.iloc[0].added_profile_delta_low_bn:.3f}–{h.iloc[0].added_profile_delta_high_bn:.3f}; the whole-lineage change is +{h.iloc[0].lineage_delta_low_bn:.3f}–{h.iloc[0].lineage_delta_high_bn:.3f}. The case would be {h.iloc[0].lineage_cost_low_bn:.3f}–{h.iloc[0].lineage_cost_high_bn:.3f} at the low end and {h.iloc[1].lineage_cost_low_bn:.3f}–{h.iloc[1].lineage_cost_high_bn:.3f} at the high. The narrow interval bounds missing added pension-dollar splits, not mortality uncertainty. [CALCULATION: symmetric_hispanic_arm_oct14.csv; ASSUMPTION: pooled Hispanic tables for actual lineage members, including those priced with white monetary rates]", '',
              'The quoted +19.6 is stale scheduled-benefit prose. The preserved executed 2025 payable/net arm is +14.897 / 14.270 (pension_accrual_2026_09_28/derived/case_beside.csv); neither is an executed 2026 whole-lineage number. New added-profile rows use the case’s measured band mixes and full-precision Hispanic/general factors. Their unknown dollar split is bounded, never typed or invented. [DATA: pension lane RESULT historical and final tables; mortality CSV added_profile rows]', '',
              '## Gates, sampling and remaining limits', '',
              '- Existing raw rough outputs reproduce before any change, at their 5e-5bn printed precision; frozen engine formula and lineage addition close at 1e-9bn.',
              '- The principal union production terms reproduce at 1e-8bn; all 161 skill-income columns conserve their national sums at 1e-6bn, ACS cells at 1e-6 persons. Production uses official pwwgt0; fiscal rough keys use rounded MARSUPWT/100. The count normalization is kept separate from the principal production control.',
              '- All 24 status line/rule national closures pass at 1e-6bn; record IDs, duplicates/missing joins and scenario-weight conservation fail closed.',
              '- NVSS 2024 sex-specific primary spreadsheets are pinned in inputs/pins.json, parsed directly, and checked for year/sex/complete ages. The general Note 2025.7 denominator stays general; group mortality changes the 2026 numerator. Medicare qualification stays observed; survival to 65 is already inside the pension PV.',
              '- Every scalar in both the full and identified dumps has a declared comparator policy. Unknown, duplicated or full-only lineage scalars stop; summary scalars are never added as a second cost.',
              '- Production SDR SEs are in symmetric_results_oct14.csv; status receipt-shift conditional SDR SEs are in symmetric_status_sampling_oct14.csv. These hold count, flags, carrier and requested age mix fixed; they do not estimate complete fiscal uncertainty, reimputation uncertainty or life-table uncertainty.', '',
              '[CALCULATION: executable gates and focused tests. SOURCE: NVSS primary URLs in each lane’s inputs/pins.json.]', '',
              '| Conditional status receipt shift, same both ends | Estimate | Paired SDR SE |', '|---|---:|---:|']
    for _, r in se[se.end.eq('low')].iterrows():
        lines.append(f'| {r.group}, {r.population / 1e6:.3f}M | {r.receipt_change_bn:+.3f} | {r.receipt_sampling_se_bn:.3f} |')
    lines += ['', 'Comparator mixed-unit credit crossings are deferred: no comparator event-level crossing was measured, and the union’s 5b term cannot be scaled by head count. The new combined table preserves the union term and carries no fabricated comparator term. An eligibility- and frame-consistent rerun of the crossing source is required; the reviewer’s guessed range is not source evidence. Full row13 is deferred because the principal declares no conserved comparator policy for its nonlinear ratio, not because of execution cost. [UNVERIFIED: comparator crossings; DATA: existing v7 R6 policy]', '',
              'Medical/justice and other rough proxies remain the inherited declared keys; this does not turn rough comparisons into observed causal group effects. The LLM research instrument can affect framing; numeric claims here rest on primary files, executable controls and an independent code review. [INFERENCE; DATA: existing lane rules; notes/llm-bias-caveat.md]', '',
              '## Reproduce', '', '```sh',
              'node infra/immigration-fiscal/white_replacement_2026_09_28/production_state_oct14.cjs',
              'OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/accrual_white.py --mortality',
              'OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/black_comparator_rough_2026_09_28/accrual_black.py --mortality',
              'OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/status_keys_oct14.py',
              'OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/symmetric_comparators_oct14.py',
              'uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/render_symmetric_result.py',
              '```', '', 'The first inspected build alone uses --pin; reruns verify the pins without rewriting them. Legacy run_oct14.sh remains the historical rough-output route. New live sensitivity commands are above; old output files are preserved, never refreshed from a new policy.', '',
              '## Execution log', '',
              '2026-10-14T12:21:58Z (from date): initial integrated build exited 0 in 21.435s, peak 2.243GB; expanded status/mortality controls and independent review follow. Final check receipts and exact changed-path manifest are in the assigned comparators-result.md. Times/memory use Python perf_counter/getrusage, not time -l.']
    report = '\n'.join(lines) + '\n'
    for lane in (HERE, BLACK):
        path = lane / 'RESULT.md'
        old = path.read_text()
        if MARKER in old:
            old = old.split('\n## Preserved earlier results\n', 1)[1].lstrip('\n')
        path.write_text(report + '\n## Preserved earlier results\n\n' + old)


if __name__ == '__main__':
    render()
