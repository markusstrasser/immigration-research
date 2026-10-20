"""Write the nine conclusions and premise matrix on live main case v9 only.

The oct07 CSVs supply the historical claims and qualitative questions, never live values.
C8 tests the map's still-oct07 sentence against explicitly labelled live comparator
readings at personal ends, preserving gaps in the local-white symmetric route.
Every input file and its numeric CSV cells is pinned in tables_oct16_pins.json, rederived
after adoption; drift stops before writing. No script repins itself. Historical scripts
and outputs are preserved. Run after engine_breaks_sept29.cjs --case oct16 and all of
the generation, white, pairing, debt and winners lanes' oct16 runs:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/tables_oct16.py
"""
from __future__ import annotations
import csv
import hashlib
import importlib.util
import json
import math
import sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
F = HERE.parent
D = HERE / 'derived'
CASE = F / 'main_case_2026_10_16/derived'
PINS = HERE / 'tables_oct16_pins.json'
def require_adopted_payload(payload):
    live = json.loads((F / 'live_case.json').read_text())
    if live.get('key') != 'oct16' or live.get('lane') != CASE.parent.name or not live.get('adopted'):
        blocked('the live-case declaration is not adopted oct16')
    meta = payload.get('meta', {})
    if meta.get('adopted') != live['adopted'] or not meta.get('status', '').startswith('adopted: main case v9'):
        blocked('the oct16 payload adoption differs from the live-case declaration')

INPUTS = [
    *[D / f'{name}_oct16.csv' for name in ('c1_arms', 'c1_min_cuts', 'c2_tally', 'c2_break_even', 'c3_correction_split', 'c6_generation_break_even', 'c6_inputs')],
    D / 'first_year_item6_oct16.json', D / 'first_year_calibration.json', D / 'c1_search_oct16.json',
    CASE / 'summary.json', CASE / 'main_case_bands.csv', CASE / 'corrections.json', CASE / 'corrections_cash.json',
    *[F / 'white_replacement_2026_09_28/derived' / name for name in (
        'headline_oct16.csv', 'rekey_summary_oct16.csv', 'ipeds_terms_oct16.csv',
        'symmetric_results_oct16.csv', 'symmetric_audit_oct16.json', 'lineage_engine_bridge_oct16.csv')],
    F / 'white_replacement_2026_09_28/mortality_conventions.py', F / 'white_replacement_2026_09_28/comparison_contract.py',
    *[F / 'lineage_mortality_2026_10_14/derived' / name for name in ('case_changes.csv', 'comparisons.csv', 'accrual_ratios.csv', 'reproduced_ratios.csv', 'added_profiles.csv')],
    F / 'sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.csv',
    F / 'sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json',
    F / 'debt_legacy_2026_09_23/derived/oct16/current_flow_source_parts_2024.csv',
    F / 'debt_legacy_2026_09_23/derived/oct16/current_flow_contract.json',
    F / 'winners_losers_2026_09_24/derived/oct16/p7_net_shares.csv',
    F / 'winners_losers_2026_09_24/derived/oct16/p7_inputs.json',
    D / 'generation_source_contract_oct16.json',
    D / 'conclusions_oct07.csv', D / 'common_mode_oct07.csv',
    F / 'white_replacement_2026_09_28/derived/headline_oct07.csv',
    F / 'overview_2026_09_28/groups.py', F / 'overview_2026_09_28/quantity_registry.csv', F / 'overview_2026_09_28/quantities.py',
    F / 'main_case_lineage_2026_10_05/derived/white_lines.json', F / 'main_case_lineage_2026_10_05/derived/v5_summary.json']

def blocked(message):
    raise SystemExit(f'[BLOCKED] {message}')

def rows(file):
    with file.open(newline='') as stream:
        return list(csv.DictReader(stream))

def num(row, field):
    try:
        value = float(row[field])
    except (KeyError, TypeError, ValueError):
        blocked(f'missing or non-numeric {field}: {row}')
    if not math.isfinite(value):
        blocked(f'non-finite {field}: {row}')
    return value

def check(label, got, want, tol):
    if not all((math.isfinite(value) for value in (got, want, tol))) or tol < 0:
        blocked(f'{label}: non-finite value or invalid tolerance')
    if abs(got - want) > tol:
        blocked(f'{label}: {got} != {want} (tolerance {tol})')

def snapshot():
    """Evidence pins: every input's bytes and every numeric CSV cell, with its row and column."""
    result = {}
    for file in [*INPUTS, F / 'live_case.json']:
        if not file.exists():
            blocked(f'{file.relative_to(F)} absent: run its live oct16 producer first')
        cells = []
        if file.suffix == '.csv':
            for index, row in enumerate(rows(file)):
                for key, text in row.items():
                    try:
                        value = float(text)
                    except (TypeError, ValueError):
                        continue
                    if math.isfinite(value):
                        cells.append([index, key, value])
        result[str(file.relative_to(F))] = {'sha256': hashlib.sha256(file.read_bytes()).hexdigest(), 'numeric_cells': cells}
    return result

def load_module(name, file):
    spec = importlib.util.spec_from_file_location(name, file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def band(row):
    return [num(row, 'cost_low_bn'), num(row, 'cost_high_bn')]

def pair_text(values, digits=1):
    return ' / '.join((f'{v:,.{digits}f}' for v in values))
MORTALITY = load_module('mortality_conventions_c8', F / 'white_replacement_2026_09_28/mortality_conventions.py')
COMPARISON = load_module('comparison_contract_c8', F / 'white_replacement_2026_09_28/comparison_contract.py')
MIXED_MORTALITY = MORTALITY.MIXED
OWN_MORTALITY = MORTALITY.OWN
MORTALITY_READINGS = ((MIXED_MORTALITY, 'none'), (OWN_MORTALITY, 'low'), (OWN_MORTALITY, 'high'))
ROUGH_LINEAGE = 'mexican_origin_rough'

def validate_item11_uncertainty(row):
    """V9 has own-mask SDR, but no calibrated lineage paired replicate vector."""
    if row.get('item11_paired_se_bn') not in (None, ''):
        blocked('C8 oct16 paired item11 SE is unmeasured; a numeric value is unsupported')
    scope = str(row.get('item11_se_scope', ''))
    if 'calibrated v9 lineage paired replicate vector unmeasured' not in scope:
        blocked('C8 unavailable paired item11 SE requires its explicit source scope')
    if num(row, 'item11_comparator_se_bn') < 0:
        blocked('C8 comparator-only item11 SDR must be nonnegative')

def comparator_values(records, arm='combined_rules_only', comparators=('A1_third_plus_nh_white', 'A3_third_plus_nh_white_at_union_ages')):
    """No implicit whole-population/own-group pairing; row provenance is mandatory."""
    selected, declared = ({}, {})
    for row in records:
        if row.get('arm') != arm:
            continue
        if row.get('case') != 'oct16':
            blocked('C8 comparator case must be oct16')
        reading = (row.get('mortality_convention'), row.get('mortality_bound'))
        if reading not in MORTALITY_READINGS:
            blocked(f'C8 explicit mortality convention/bound required: {reading}')
        if row.get('allocation') != 'personal':
            blocked('C8 comparator allocation must be personal')
        if row.get('group_mortality') not in ('whole-population', 'own-group'):
            blocked('C8 actual group mortality declaration required')
        key = (*reading, row['basis'], row['group'], row['end'])
        if key in selected:
            blocked(f'C8 duplicate comparator row: {key}')
        selected[key] = num(row, 'cost_bn')
        declared[key] = row
    for reading in MORTALITY_READINGS:
        for basis in ('accrual', 'cash'):
            for group in ('mexican_origin_engine', ROUGH_LINEAGE, *comparators):
                for end in ('low', 'high'):
                    if (*reading, basis, group, end) not in selected:
                        blocked(f'C8 missing comparator row: {(*reading, basis, group, end)}')
            for group in comparators:
                for end in ('low', 'high'):
                    try:
                        lineage = declared[*reading, basis, ROUGH_LINEAGE, end]
                        comparator = declared[*reading, basis, group, end]
                        COMPARISON.require_same_engine(lineage, comparator)
                        if lineage.get('engine') != 'rough' or comparator.get('engine') != 'rough':
                            blocked('C8 gap requires both sides on engine rough')
                        for row in (lineage, comparator):
                            removal = num(row, 'mixed_unit_removal_bn')
                            check('C8 item11 exclusion closes', num(row, 'cost_without_item11_bn'), num(row, 'cost_bn') - removal, 1e-09)
                            if not row.get('mixed_unit_asymmetry'):
                                blocked('C8 explicit mixed-unit asymmetry required')
                        if group == 'A1_third_plus_nh_white':
                            check('C8 measured comparator item11 declaration', num(comparator, 'mixed_unit_removal_bn'), num(comparator, 'comparator_item11_bn'), 1e-09)
                            validate_item11_uncertainty(comparator)
                        else:
                            if not (str(comparator.get('mixed_unit_asymmetry', '')).startswith('reweighted from A1') and abs(num(comparator, 'mixed_unit_removal_bn') - num(comparator, 'comparator_item11_bn')) <= 1e-09):
                                blocked("C8 age-standardized comparator item11 must be A1's declared reweighted term")
                            validate_item11_uncertainty(comparator)
                        MORTALITY.validate_pair(lineage, declared[*reading, basis, group, end], reading[0])
                    except ValueError as error:
                        raise SystemExit(str(error)) from error
    return selected

def comparator_gap(values, mortality, bound, basis, group):
    return [values[mortality, bound, basis, ROUGH_LINEAGE, end] - values[mortality, bound, basis, group, end] for end in ('low', 'high')]

def bridge_values(records, values):
    """Require the delivered itemization for every mortality reading."""
    parts = {}
    for row in records:
        if row.get('arm') != 'combined_rules_only':
            continue
        reading = (row.get('mortality_convention'), row.get('mortality_bound'))
        if (row.get('case'), row.get('case_engine'), row.get('rough_engine')) != ('oct16', 'case', 'rough') or reading not in MORTALITY_READINGS:
            blocked('C8 bridge provenance must declare case-to-rough oct16 and a source mortality reading')
        key = (*reading, row['basis'], row['end'])
        identity = (*key, row['side'], row['line'])
        if identity in parts:
            blocked('C8 duplicate bridge component')
        value = num(row, 'case_minus_rough_bn')
        check('C8 bridge component difference', value, num(row, 'case_bn') - num(row, 'rough_bn'), 1e-09)
        parts[identity] = value
    totals = {}
    for mortality, bound in MORTALITY_READINGS:
        for basis in ('accrual', 'cash'):
            for end in ('low', 'high'):
                key = (mortality, bound, basis, end)
                selected = [amount for identity, amount in parts.items() if identity[:4] == key]
                if not selected:
                    blocked(f'C8 missing itemized bridge {mortality}/{bound}/{basis}/{end}')
                total = sum(selected)
                check(f'C8 {mortality}/{bound}/{basis}/{end} itemized bridge closure', total, values[mortality, bound, basis, 'mexican_origin_engine', end] - values[mortality, bound, basis, ROUGH_LINEAGE, end], 1e-09)
                totals[key] = total
    return totals

def live_pairing_values(records):
    """Section 7 is the current pairing; dated revision rows have no live oct16 amount."""
    return {(row['column'], row['item']): num(row, 'oct16') for row in records if row['section'] == '7'}

def current_flow_values(contract, records, summary):
    """Validate the native source split without assigning its unlocated remainder."""
    if (contract.get('case') != 'oct16' or contract.get('financing_complete') is not False
            or contract.get('historical_stock_identified') is not False):
        blocked('C5 requires the declared incomplete oct16 current-flow contract')
    for name, sha in contract['source_pins'].items():
        if hashlib.sha256((F / name).read_bytes()).hexdigest() != sha:
            blocked(f'C5 current-flow source drift: {name}')
    result = []
    for basis, oracle in (('set', 'band_bn'), ('cash', 'cash_set_bn')):
        for i, end in enumerate(('low', 'high')):
            check(f'C5 {basis}/{end} source band', contract['bands_bn'][basis][i], summary[oracle][i], 1e-9)
            rr = [r for r in records if (r['basis'], r['end'], r['convention']) == (basis, end, 'central')]
            if not rr:
                blocked(f'C5 absent native source corner {basis}/{end}')
            check(f'C5 {basis}/{end} full source closure', sum(num(r, 'responsive_bn') for r in rr), summary[oracle][i], 1e-9)
            cash = [r for r in rr if r['financing'] == 'cash']
            unlocated = [r for r in rr if r['financing'] == 'unlocated']
            if any(r.get('federal_bn') or r.get('state_local_bn') for r in unlocated):
                blocked('C5 unlocated source must not silently acquire a payer')
            for r in cash:
                check('C5 identified cash payer closure', num(r, 'federal_bn') + num(r, 'state_local_bn'), num(r, 'responsive_bn'), 1e-9)
            federal = sum(num(r, 'federal_bn') for r in cash)
            check(f'C5 {basis}/{end} federal cash principal', federal, contract['federal_current_cash_bn'][f'{basis}|{end}|central'], 1e-9)
            for kind in {r['financing'] for r in rr}:
                check(f'C5 {basis}/{end}/{kind} principal', sum(num(r, 'responsive_bn') for r in rr if r['financing'] == kind), contract['financing_totals_bn'][f'{basis}|{end}|central|{kind}'], 1e-9)
            result.append({'case': 'oct16', 'basis': basis, 'end': end,
                           'identified_federal_cash_bn': federal,
                           'identified_state_local_cash_bn': sum(num(r, 'state_local_bn') for r in cash),
                           'unlocated_source_total_bn': sum(num(r, 'responsive_bn') for r in unlocated),
                           'complete_state_local_share_pct': '', 'legacy_interest_bn': '',
                           'scope': 'identified current cash only; full payer/timing and historical financing unmeasured; capital resource cost never borrowing'})
    return result


def winner_values(records):
    """Use the live stationary, recommended social stack with explicit pooling."""
    selected = [r for r in records if (r.get('case'), r.get('frame'), r.get('level'), r.get('arm'),
                r.get('epsilon'), r.get('population'), r.get('sharing')) ==
                ('oct16', 'stationary', 'central', 'recommended', 'infinite', 'lineage', 'pooled')]
    if len(selected) != 3 or {r['financing'] for r in selected} != {'a', 'b', 'c'}:
        blocked('C5 exact live stationary pooled winner rows absent or duplicated')
    for row in selected:
        share = num(row, 'winners_share')
        if not 0 <= share <= 1:
            blocked('C5 invalid winner prevalence')
        check('C5 winner/loser prevalence closure', share + num(row, 'losers_share'), 1., 1e-12)
        check('C5 stationary future financing', num(row, 'future_bn'), 0., 1e-9)
        check('C5 financing preserves central total', num(row, 'total_bn'), num(selected[0], 'total_bn'), 1e-9)
    return [100 * num(next(r for r in selected if r['financing'] == c), 'winners_share') for c in ('a', 'b', 'c')]

def write(file, data):
    with file.open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(data[0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(data)

def main():
    current = snapshot()
    if not PINS.exists():
        blocked('tables_oct16_pins.json absent: derive pins from the final adopted run before tables')
    pinned = json.loads(PINS.read_text())
    if pinned['inputs'] != current:
        changed = [name for name in current if current[name] != pinned['inputs'].get(name)]
        blocked(f'final evidence drift: {changed}')
    summary = json.loads((CASE / 'summary.json').read_text())['v9']
    payload = json.loads((CASE / 'corrections.json').read_text())
    require_adopted_payload(payload)
    if payload['meta']['allocation']['group_total'] != 'personal':
        blocked('the live payload is not adopted v9 at the personal allocation')
    ends = summary['end_specifications']['set'][0]
    if any((ends != row for basis in ('set', 'cash') for row in summary['end_specifications'][basis])):
        blocked('set and cash ends differ: the tally rule needs revision')
    end_labels = [f'low_end_{ends[0]}', f'high_end_{ends[1]}']
    arms = {r['arm']: r for r in rows(D / 'c1_arms_oct16.csv')}
    bands = {r['variant']: r for r in rows(CASE / 'main_case_bands.csv') if r['profile'] == 'long_run_non_school_full'}
    for variant, arm, key in [('adopted', 'adopted', 'band_bn'), ('cash_set', 'pension_cash', 'cash_set_bn')]:
        for i, value in enumerate(band(arms[arm])):
            check(f'{variant} published band', value, band(bands[variant])[i], 0.0001)
            check(f'{variant} summary', value, summary[key][i], 0.0001)
    midpoint = sum(band(arms['adopted'])) / 2
    horizon = json.loads((D / 'first_year_item6_oct16.json').read_text())
    for basis, arm in (('set', 'first_year_horizon'), ('cash', 'first_year_horizon_cash')):
        for i, value in enumerate(horizon['variants']['fixed_capital'][basis]):
            check(f'first-year {basis} engine report', band(arms[arm])[i], value, 0.0001)
    check('first-year lower threshold', horizon['thresholds']['low_bn'], 0.75 * sum(summary['band_bn']) / 2, 1e-09)
    horizon_breaks = sum(horizon['variants']['fixed_capital']['set']) / 2 < horizon['thresholds']['low_bn']
    if horizon_breaks != horizon['first_year_breaks_alone']:
        blocked('first-year C1 verdict disagrees with the unrounded engine report')
    horizon_clause = 'First-year horizon ' + ('breaks C1 alone' if horizon_breaks else 'does not break C1 alone')
    cuts = [r for r in rows(D / 'c1_min_cuts_oct16.csv') if r['minimal'] == 'yes']
    search = json.loads((D / 'c1_search_oct16.json').read_text())
    cap = search.get('max_size_searched')
    if not isinstance(cap, int) or cap < 1 or any(int(float(r['size'])) > cap for r in cuts):
        blocked('C1 search receipt lacks its size cap, or lists a cut above it')
    complete = {d: v.get('complete') for d, v in search['directions'].items()}
    cut_scope = (f'{len(cuts)} minimal cuts of at most {cap} arms'
                 + ('' if all(complete.values()) else f'; minimal cuts of more than {cap} arms are not enumerated on v9 [SCOPE]'))
    tally = {(r['model'], r['end']): r for r in rows(D / 'c2_tally_oct16.csv')}
    tally_of = lambda model: [num(tally[model, e], 'tally_bn') for e in end_labels]
    be = rows(D / 'c2_break_even_oct16.csv')
    split = {(r['reading'], r['end']): r for r in rows(D / 'c3_correction_split_oct16.csv')}
    for row in split.values():
        check('C3 side closure', num(row, 'net_move_bn'), num(row, 'tax_side_move_bn') + num(row, 'spending_side_move_bn') + num(row, 'interaction_bn'), 0.0002)
        check('C3 full case', num(row, 'all_edits_bn'), band(arms['adopted'])[end_labels.index(row['end'])], 0.0001)
    gen = rows(D / 'c6_generation_break_even_oct16.csv')
    for case, oracle in [('case_accrual', 'adopted'), ('cash_set', 'pension_cash')]:
        for conv in ('a', 'b'):
            rr = [r for r in gen if r['case'] == case and r['convention'] == conv]
            if {r['generation'] for r in rr} != {'G1', 'G2', 'G3plus'}:
                blocked(f'C6 incomplete generations for {case} {conv}')
            for i, key in enumerate(('cost_low_end_bn', 'cost_high_end_bn')):
                check(f'C6 {case} {conv} sum', sum((num(r, key) for r in rr)), band(arms[oracle])[i], 0.0002)
    white = F / 'white_replacement_2026_09_28/derived'
    comparator_records = rows(white / 'symmetric_results_oct16.csv')
    comparator = comparator_values(comparator_records)
    central = comparator_values(comparator_records, arm=MORTALITY.CENTRAL['arm'], comparators=('A1_third_plus_nh_white',))
    bridges = bridge_values(rows(white / 'lineage_engine_bridge_oct16.csv'), comparator)
    comparator_rows = {(r['mortality_convention'], r['mortality_bound'], r['basis'], r['group'], r['end']): r for r in comparator_records if r['arm'] == 'combined_rules_only'}
    for basis, key in (('accrual', 'band_bn'), ('cash', 'cash_set_bn')):
        for i, end in enumerate(('low', 'high')):
            check(f'C8 labelled mixed mortality headline {basis}/{end}', comparator[MIXED_MORTALITY, 'none', basis, 'mexican_origin_engine', end], summary[key][i], 1e-09)
    head = {(r['figure'], r['end']): r for r in rows(white / 'headline_oct16.csv')}
    white_summary = {(r['basis'], r['group'], r['end']): r for r in rows(white / 'rekey_summary_oct16.csv')}
    for basis, key in (('accrual', 'band_bn'), ('cash', 'cash_set_bn')):
        for i, end in enumerate(('low', 'high')):
            row = white_summary[basis, 'mexican_origin_engine', end]
            check(f'C8 {basis} engine union on final adopted case {end}', num(row, 'cost'), summary[key][i], 0.0001)
            check(f'C8 {basis} personal end {end}', num(row, 'spec'), ends[i], 0)
    A1 = 'age artefact removed: A1 third-plus whites, accrual (central)'
    LOCAL = 'local whites state by state, union ages, accrual (central)'
    RAW = 'raw cash at white ages: A1, cash set'

    def white_band(figure):
        return [num(head[figure, end], 'oct16_bn') for end in ('low', 'high')]
    sys.path.insert(0, str(F / 'overview_2026_09_28'))
    MAP = load_module('groups', F / 'overview_2026_09_28/groups.py')
    Q = load_module('quantities', F / 'overview_2026_09_28/quantities.py')
    site = Q.groups_sites(MAP.GROUPS).get('selection/f263/text', '')
    if not all((f'{{{{q:{rid}|mid_range}}}}' in site for rid in ('whites.gap_a1', 'whites.gap_local'))):
        blocked('C8 map sentence no longer quotes the two historical white comparisons')
    if '{{q:whites.gap_cash|mid_range}}' not in Q.groups_sites(MAP.GROUPS).get('selection/f263/why', ''):
        blocked('C8 map why line no longer quotes its historical raw-cash comparator')
    historical = {(r['figure'], r['end']): r for r in rows(white / 'headline_oct07.csv')}
    references = {}
    for rid, fig in (('whites.gap_a1', A1), ('whites.gap_local', LOCAL), ('whites.gap_cash', RAW)):
        expected = tuple((num(historical[fig, e], 'oct07_bn') for e in ('low', 'high')))
        if Q.record_value(rid) != expected:
            blocked(f'C8 {rid}: map changed from the explicit historical oct07 baseline')
        references[fig] = sum(expected) / 2
    claim = Q.fill(site)[0]
    historical_claim = next((r['claim_tested'] for r in rows(D / 'conclusions_oct07.csv') if r['id'] == 'C8'))
    if claim != historical_claim:
        blocked("C8 map's claim text changed from oct07: restate its frame before grading oct16")
    real = live_pairing_values(rows(F / 'sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.csv'))
    pairing = [real['pairing_on_priced_count', f'published pairing ({e})'] for e in ('low', 'high')]
    # Since v8 the pairing's fiscal row is the case at both ends (no Hispanic/custody footing rows on oct16):
    # take the published social rows and require pairing - social to be the live band.
    social = [real['pairing_on_priced_count', f'social rows after environmental replacements ({e})'] for e in ('low', 'high')]
    for i, e in enumerate(('low', 'high')):
        check(f'C4 pairing fiscal footing is the live case ({e})', pairing[i] - social[i], summary['band_bn'][i], 1e-09)
    real_doc = json.loads((F / 'sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json').read_text())
    inherited = real_doc.get('inherited_oct15', {}).get('social_items_in_the_social_rows', {})
    if real_doc.get('case') != 'oct16' or inherited.get('case') != 'oct15':
        blocked('C4 item spans: oct16 real-costs document must carry the inherited oct15 record-basis items')
    span_items = {it['item']: it for it in inherited.get('items', [])}

    def normalized_central(item):
        value = (span_items.get(item, {}).get('normalized_bn') or {}).get('central')
        if not isinstance(value, (int, float)) or not math.isfinite(value):
            blocked(f'C4 normalized central absent: {item}')
        return float(value)
    debt_dir = F / 'debt_legacy_2026_09_23/derived/oct16'
    current_flows = current_flow_values(json.loads((debt_dir / 'current_flow_contract.json').read_text()),
        rows(debt_dir / 'current_flow_source_parts_2024.csv'), summary)
    wins = winner_values(rows(F / 'winners_losers_2026_09_24/derived/oct16/p7_net_shares.csv'))
    conclusions = rows(D / 'conclusions_oct07.csv')
    for row in conclusions:
        row['status_on_v9'] = row.pop('status_on_v6')
        row['reading_on_v9'] = row.pop('reading_on_v6')
    C = {r['id']: r for r in conclusions}

    def update(cid, status, reading, condition, note, premise):
        C[cid].update(status_on_v9=status, reading_on_v9=reading, break_condition=condition, break_distance_note=note, deciding_premise=premise, source=f'[CALCULATION: live oct16 files pinned in {PINS.name}]', premises=C[cid]['premises'] + '; v9 personal allocation; domestic-source job-capital tax; completed membership; bounded mixed-unit removal and coverage, post-engine', rival_reading='[FRAMING-SENSITIVE] Alternative conventions and comparison populations answer different questions; live alternatives are reported in the break-condition and premise cells.')

    def arm_text(arm):
        return f"{arm}: ${pair_text(band(arms[arm]))}bn ({num(arms[arm], 'move_pct_of_midpoint'):+.1f}%)"
    cut_text = '; '.join((f"{r['set']} ({num(r, 'move_pct_of_midpoint'):+.1f}%)" for r in cuts if int(float(r['size'])) <= 2))
    update('C1', 'holds, restated', f"${pair_text(summary['band_bn'])}bn; midpoint ${midpoint:.1f}bn; ${pair_text(summary['per_member_usd']['set'], 0)} per member. Personal specifications {ends}.", f"Midpoint cuts: below ${0.75 * midpoint:.1f}bn or above ${1.25 * midpoint:.1f}bn. Minimal cuts of one or two: {cut_text}. {arm_text('first_year_horizon')}. {horizon_clause}; items6/9 business property at 0, corporate and production at 1-alpha; completion in full with first-year parent responses and source endpoint prices; item11 without its owner property; item12 at its source lines' first-year responses, public capital and property at zero [ASSUMPTION; APPROX]. [APPROX: additive item/lineage arms in combinations]", f'{cut_scope}. All arms and stacks remain in c1_arms_oct16.csv and c1_min_cuts_oct16.csv.', 'P02/P03/P04/P05/P20, and v9 receipt rules')
    t = tally_of('case_accrual')
    status2 = 'direct-receipt clause holds at both ends' if min(t) >= 0 else 'direct-receipt clause BREAKS at both ends' if max(t) < 0 else 'direct-receipt clause splits by end'
    be_text = '; '.join((f"{r['case']} {r['variant']} {r['allocation']}: {100 * num(r, 'break_even_most_adverse'):.2f}% / {100 * num(r, 'break_even_least_adverse'):.2f}%" for r in be))
    update('C2', status2,
           f"Direct receipts less household transfers: ${pair_text(t)}bn. Union at case responses ${pair_text(tally_of('union_at_case_responses'))}bn; cash ${pair_text(tally_of('cash_set'))}bn.",
           f"{be_text}. At scheduled benefits ${pair_text([num(tally['case_accrual', e], 'tally_at_scheduled_bn') for e in end_labels])}bn; lineage arm a ${pair_text(tally_of('lineage_arm_a'))}bn, arm c ${pair_text(tally_of('lineage_arm_c'))}bn.",
           "Direct receipts exclude job-capital indirect receipts; completion real-line carriers take their parent's class. Military post adjustments use their original source-line transfer class. [GAP] Mixed-unit, coverage and count-calibration net amounts have no complete receipt/transfer-class split in the payload, so the class tally excludes those net amounts; the service break-even includes them in full. A negative break-even means a cost even at zero service response.",
           'P05 and v9 receipt/credit/military rules')
    C['C2']['premises'] = 'P01/P03/P04/P05/P07/P08/P20; payable-benefit accrual on 2026 separate funds; personal allocation; keyed completion and credit parts held. Class-defined tally including completion parent classes; post-engine costs excluded from this clause because their class split is undeclared.'
    C['C2']['claim_tested'] = 'Historical September-27 claim: ' + C['C2']['claim_tested']
    split_pair = lambda key: [num(split['pension_rebuilt', e], key) for e in end_labels]
    cancellation = all((abs(net) < min(abs(tax), abs(spending)) / 2 for net, tax, spending in zip(split_pair('net_move_bn'), split_pair('taxes_move_by_line_type_bn'), split_pair('spending_move_by_line_type_bn'))))
    net_claim = all((8.25 <= abs(v) <= 13.75 for v in split_pair('net_move_bn')))
    side_claim = all((43.5 <= abs(v) < 57.5 for key in ('taxes_move_by_line_type_bn', 'spending_move_by_line_type_bn') for v in split_pair(key)))
    status3 = f"{('holds' if side_claim else 'BREAKS')} side magnitudes; {('holds' if net_claim else 'BREAKS')} net-about-11; {('holds' if cancellation else 'BREAKS')} cancellation"
    update('C3', status3, f"Taxes ${pair_text(split_pair('taxes_move_by_line_type_bn'), 2)}bn; spending ${pair_text(split_pair('spending_move_by_line_type_bn'), 2)}bn; net ${pair_text(split_pair('net_move_bn'), 2)}bn.", 'The historical claim tests side magnitudes $44–57bn at its printed whole-bn precision, net-about-$11bn at a quarter ($8.25–13.75bn), and cancellation as a net below half the smaller side. Rebuilt union pension switch; lineage and every meta.items edit are held in all four runs. Their changes are not counted as dataset corrections.', 'See both pension_rebuilt and increments_held rows. [GAP: holding lineage/items excludes their correction-dependent re-keying.]', 'P08')
    deviations = {}
    for item in ('pm25_consumption', 'road_crash_externality', 'scale_net_earnings'):
        if item not in span_items:
            blocked(f'C4 item span absent: {item}')
        it = span_items[item]
        deviations[item] = [float(it['low_bn']) - float(it['central_bn']), float(it['high_bn']) - float(it['central_bn'])]
    ranges_text = '; '.join((f'{item}: ${pair_text(values)}bn' for item, values in deviations.items()))
    update('C4', 'holds, restated' if all((75 <= v <= 125 for v in social)) else 'BREAKS about-$100bn add', f'Social rows ${pair_text(social)}bn; published pairing ${pair_text(pairing)}bn.', f"A quarter of the add is ${sum(social) / 8:.1f}bn; of the pairing ${sum(pairing) / 8:.1f}bn. Item deviations {ranges_text} (oct15 record-basis spans the oct16 real-costs file carries; v9 does not reprice them). [INFERENCE: additive published social tails; added people's rows held.]", "Since v8 the pairing's fiscal row is the case at both ends; pairing minus the published social rows equals the live band.", 'C1 plus social prices and elasticities')
    source_pair = lambda field: [r[field] for r in current_flows if r['basis'] == 'set']
    status5 = f"most UNMEASURED; {('holds' if all((12.5 <= value <= 100 * 1.25 / 6 for value in wins[:2])) else 'BREAKS')} about-one-in-six (quarter threshold)"
    update('C5', status5,
        f"[GAP] Complete state-local share and legacy interest unmeasured. Identified current cash: federal ${pair_text(source_pair('identified_federal_cash_bn'))}bn; state-local ${pair_text(source_pair('identified_state_local_cash_bn'))}bn. Unlocated set source costs ${pair_text(source_pair('unlocated_source_total_bn'))}bn. Stationary financing, recommended central social stack, pooled winners {pair_text(wins)}% (a / b / c).",
        'Most means above 50%, but the native debt contract does not identify the full payer/timing split or historical financing. No zero or complete share is substituted. The about-one-in-six quarter interval is12.5–20.8333% under rules a/b. Financing and pooling determine the winner shares.',
        'The winner shares are modeled incidence, not observed individual effects. Current cash source amounts are neither complete financing nor Treasury borrowing; capital resource costs remain separate.', 'P05/P06/P11 and v9 taxes')
    cost_min = min((num(r, k) for r in gen if r['case'] == 'case_accrual' for k in ('cost_low_end_bn', 'cost_high_end_bn')))
    bmax = max((100 * num(r, k) for r in gen if r['case'] == 'case_accrual' for k in r if k.startswith('break_even')))
    cash_min = min((num(r, k) for r in gen if r['case'] == 'cash_set' for k in ('cost_low_end_bn', 'cost_high_end_bn')))
    cash_bmax = max((100 * num(r, k) for r in gen if r['case'] == 'cash_set' for k in r if k.startswith('break_even')))
    update('C6', 'holds' if cost_min > 0 else 'BREAKS at a generation end', f'Each generation costs others at both ends under both conventions; minimum ${cost_min:.1f}bn. Largest service break-even {bmax:.1f}%.', f"A generation becomes a gain below its own service break-even. On cash, minimum generation cost ${cash_min:.1f}bn at the case's personal ends; largest service break-even {cash_bmax:.1f}% over both allocations and conventions. All values are in c6_generation_break_even_oct16.csv. The progress clause retains its historical cohort evidence.", "G3+ carries the added people and the case's lineage item parts.", 'C1 and lineage/generation allocation')
    central_a1 = {bound: comparator_gap(central, MORTALITY.CENTRAL['mortality_convention'], bound, 'accrual', 'A1_third_plus_nh_white') for bound in ('low', 'high')}
    moves = [100 * (sum(central_a1[bound]) / 2 / references[A1] - 1) for bound in ('low', 'high')]
    C['C8']['claim_tested'] = claim
    comparison_figures = [A1, LOCAL, RAW, 'age artefact removed: A3 white rates at union ages, accrual', 'age artefact removed: A3 white rates at union ages, cash', 'local whites state by state, union ages, cash']
    historical_midpoints = {fig: sum((num(historical[fig, e], 'oct07_bn') for e in ('low', 'high'))) / 2 for fig in comparison_figures}
    white_readings = 'Live legacy headline gaps are withheld: they mix the case lineage and rough comparator engines. Historical oct07 figures remain historical.'
    comparison_rows, matched_readings = ([], [])
    matched_figures = ((A1, 'accrual', 'A1_third_plus_nh_white'), (RAW, 'cash', 'A1_third_plus_nh_white'), (comparison_figures[3], 'accrual', 'A3_third_plus_nh_white_at_union_ages'), (comparison_figures[4], 'cash', 'A3_third_plus_nh_white_at_union_ages'))
    for mortality, bound in MORTALITY_READINGS:
        for figure, basis, group in matched_figures:
            values = comparator_gap(comparator, mortality, bound, basis, group)
            matched_readings.append(f'oct16 {mortality}, mortality bound {bound}, {figure}: ${pair_text(values)}bn')
            for i, end in enumerate(('low', 'high')):
                lineage_row = comparator_rows[mortality, bound, basis, ROUGH_LINEAGE, end]
                comparison_row = comparator_rows[mortality, bound, basis, group, end]
                case_value = comparator[mortality, bound, basis, 'mexican_origin_engine', end]
                comparison_rows.append({'case': 'oct16', 'mortality_convention': mortality, 'mortality_bound': bound, 'arm': 'combined_rules_only', 'allocation': 'personal', 'basis': basis, 'figure': figure, 'group': group, 'end': end, 'lineage_engine': 'rough', 'comparator_engine': 'rough', 'lineage_cost_bn': comparator[mortality, bound, basis, ROUGH_LINEAGE, end], 'comparator_cost_bn': comparator[mortality, bound, basis, group, end], 'lineage_minus_comparator_bn': values[i], 'lineage_minus_comparator_without_item11_bn': num(lineage_row, 'cost_without_item11_bn') - num(comparison_row, 'cost_without_item11_bn'), 'mixed_unit_removal_bn': num(lineage_row, 'mixed_unit_removal_bn') - num(comparison_row, 'mixed_unit_removal_bn'), 'comparator_item11_bn': num(comparison_row, 'mixed_unit_removal_bn'), 'item11_paired_se_bn': comparison_row.get('item11_paired_se_bn', ''), 'lineage_minus_comparator_one_sided_bn': values[i] + num(comparison_row, 'mixed_unit_removal_bn'), 'mixed_unit_asymmetry': comparison_row['mixed_unit_asymmetry'], 'framing': COMPARISON.MIXED_FRAME, 'case_lineage_cost_bn': case_value, 'case_minus_rough_lineage_bridge_bn': bridges[mortality, bound, basis, end], 'bridge_itemization': 'white_replacement_2026_09_28/derived/lineage_engine_bridge_oct16.csv'})
    update('C8', ('A1 holds against historical map claim' if max(map(abs, moves)) <= 25 else 'A1 BREAKS historical map claim') + '; matched local-white reading GAP', f"Live v9 A1 on round 3's central (members' children depart with them, every group at its own coverage and its own mortality) ${pair_text(central_a1['low'])}bn / ${pair_text(central_a1['high'])}bn at the lineage's low / high profile bounds; rough engine on both sides. Move on the map's historical oct07 A1 midpoint: {pair_text(moves)}% (bounds low / high). Current-rule readings: " + '; '.join(matched_readings), f'A quarter from the historical map midpoints ${references[A1]:.2f}bn (A1), ${references[LOCAL]:.2f}bn (local). {white_readings} The explicitly tagged A1/A3 matched readings use symmetric_results_oct16.csv; all bounds are preserved in c8_comparisons_oct16.csv. [GAP] No local-state own-production/own-mortality row is delivered; the live legacy source mixes engines and cannot clear that gap.', "The map remains oct07 by operator rule; the consumer is oct16. The live full lineage and A1/A3 use personal ends on the rough engine, own comparator production/status/eligibility/frame rules. The mixed mortality conventions retain whole-population lineage mortality and each comparator's own mortality. Own-group mortality replaces the lineage's mortality using both source bounds. Case-versus-rough lineage bridge and itemization are beside each gap. Item 11 is measured for the lineage, A1 whites and Black; A3 takes A1's term reweighted by its weight on members in mixed units; every row declares its scope and reports its exclusion. Completion remains lineage-only. The current-rule readings leave comparators without Census coverage; round 3's central gives each its own. The mixed mortality pair is labelled and never a stated claim. [FRAMING-SENSITIVE]", 'P05/P07/P14')
    C['C8']['discriminating_observation'] = '[GAP] The tagged rules-only comparisons do not identify causal replacement or transport lineage-only membership/mixed-unit estimates to comparators; local-state matched mortality/production remains uncomputed.'
    rivals = {'C1': f"[FRAMING-SENSITIVE] First-year budgets: {arm_text('first_year_horizon')}; first-year cash: {arm_text('first_year_horizon_cash')}; counted by ancestry share: ${pair_text([band(arms['ancestry_share_low'])[0], band(arms['ancestry_share_high'])[1]])}bn.", 'C2': f"[FRAMING-SENSITIVE] Counting benefits when paid gives direct receipts less household transfers of ${pair_text(tally_of('cash_set'))}bn; payroll receipts and future earned benefits belong to different annual budgets.", 'C3': "[ASSUMPTION] The tax side scales imputed-unauthorized wages to an assumed on-books share; correction cancellation does not validate either side's key. Spending checks and tax adjustments have different evidence.", 'C4': f"[FRAMING-SENSITIVE] Against as many average residents, normalized PM2.5 ${normalized_central('pm25_consumption'):.1f}bn and crashes ${normalized_central('road_crash_externality'):.1f}bn (oct15 record-basis items). Absolute and normalized costs have different counterfactuals.", 'C5': '[INFERENCE] Wage-channel totals assigned to survey people do not identify who gains. Household pooling and financing can change the winner share at the same aggregate cost.', 'C6': "[INFERENCE] Today's G3+ descends from earlier stock than today's G2; the cross-section does not identify parent-to-child progress. Linked cohorts could show a different trajectory.", 'C8': '[FRAMING-SENSITIVE] An all-residents slice answers a composition question. The white headline, own-age cash, union-age cash and local-white gaps are distinct comparisons.'}
    for cid, text in rivals.items():
        C[cid]['rival_reading'] = text
    for cid in ('C7', 'C9'):
        C[cid]['status_on_v9'] = 'unchanged historical evidence; not rerun'
        C[cid]['reading_on_v9'] = '[GAP] No v9 computation for this claim. Historical record: ' + C[cid]['reading_on_v9']
    premises = rows(D / 'common_mode_oct07.csv')
    for row in premises:
        row['best_supported_alternative'] = row['best_supported_alternative'].replace('v6', 'v9')
        row['effect_if_swapped'] = ''
        if row['premise_id'] == 'P02':
            row['best_supported_alternative'] += '; item 6 business property at 0, corporate and production at 1-alpha [ASSUMPTION; APPROX]'
            row['effect_if_swapped'] = arm_text('first_year_horizon') + f'; {horizon_clause}; C4 horizon not re-priced here [GAP].'
        elif row['premise_id'] == 'P05':
            row['effect_if_swapped'] = arm_text('pension_cash') + f"; C2 cash tally ${pair_text(tally_of('cash_set'))}bn; C5 complete cash payer share unmeasured."
        elif row['premise_id'] == 'P08':
            row['effect_if_swapped'] = f"C2 without dataset corrections ${pair_text(tally_of('v4_items_without_dataset_corrections'))}bn; C3 split in c3_correction_split_oct16.csv."
        elif row['premise_id'] == 'P03':
            row['effect_if_swapped'] = arm_text('school_within_district') + '; ' + arm_text('property_none')
        elif row['premise_id'] == 'P20':
            row['effect_if_swapped'] = '; '.join((arm_text(a) for a in ('lineage_arm_a', 'lineage_arm_c', 'ancestry_share_low', 'ancestry_share_high')))
        elif row['premise_id'] == 'P01':
            row['effect_if_swapped'] = '[GAP] Alternative survey frame not rerun on v9. Historical experiments remain in oct07/sept29 files.'
    for row in comparison_rows:
        source = comparator_rows[row['mortality_convention'], row['mortality_bound'], row['basis'], row['group'], row['end']]
        row.update(item11_comparator_se_bn=source['item11_comparator_se_bn'],
                   item11_se_scope=source['item11_se_scope'])
    write(D / 'conclusions_oct16.csv', conclusions)
    write(D / 'common_mode_oct16.csv', premises)
    write(D / 'c8_comparisons_oct16.csv', comparison_rows)
    write(D / 'c5_current_source_scope_oct16.csv', current_flows)
    print(f'[written] conclusions_oct16.csv (9), common_mode_oct16.csv ({len(premises)}), c8_comparisons_oct16.csv ({len(comparison_rows)}), c5_current_source_scope_oct16.csv ({len(current_flows)}); {len(current)} pinned files')
if __name__ == '__main__':
    main()
    sys.path.insert(0, str(F / 'scripts'))
    from memory_budget import require_within_budget
    print(f"[memory] break-condition tables peak physical footprint {require_within_budget('break-condition tables') / 1000000000.0:.3f} GB")
