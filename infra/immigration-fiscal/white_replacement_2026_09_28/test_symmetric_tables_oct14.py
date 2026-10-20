"""Independent closure checks on delivered sensitivity tables and population bases."""
import json
import hashlib
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent


def expanded_lineage_vector(symmetric, basis, end, half=None, partial=False):
    """Authenticate the expanded stack independently before asking the producer to select its endpoint."""
    pins = json.loads((HERE / 'inputs/pins.json').read_text())['symmetric_inputs_oct16']
    if partial:
        path = symmetric.CC.LINEAGE_REPLICATES
        assert hashlib.sha256(path.read_bytes()).hexdigest() == symmetric.CC.LINEAGE_REPLICATES_PIN
        path = symmetric.LINEAGE_ROUND2
    else:
        filename = 'lineage_children_total_replicates.csv' if half is None else f'lineage_half_{half}_total_replicates.csv'
        path = symmetric.CC.MIXED_SOURCE / filename
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pins[str(path.relative_to(symmetric.ROOT))]
    return symmetric.lineage_vector(basis, end, half, partial)


def test_actual_comparator_publications_match_pinned_terms_and_paired_se():
    import comparison_contract as C
    import mortality_conventions as MC
    import symmetric_comparators_oct14 as S
    source = C.load_mixed_unit(case='oct16')
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    vectors = {}
    for row in d[d.group.isin(C.MIXED_GROUPS)].itertuples():
        spec = MC.DERIVED.get(row.arm)
        if spec is None:
            term = C.comparator_removal(source, row.group, row.basis, row.end, row.population)
        else:
            rule = row.item11_effective_rule if pd.notna(row.item11_effective_rule) else spec['rule']
            key = row.basis, row.end, spec['rule'], spec.get('half'), spec.get('partial_lineage', False)
            if key not in vectors:
                vectors[key] = (C.lineage_item11_replicates(source, row.basis, row.end) if spec['rule'] == 'current'
                                else expanded_lineage_vector(S, row.basis, row.end, key[3], key[4]))
            term = C.true_count_removal(source, row.group, row.basis, row.end, row.population,
                                        row.true_own_count, rule, lineage_replicates=vectors[key])
            assert term['paired_se_bn'] is None
            assert row.item11_comparator_se_bn == pytest.approx(term['comparator_se_bn'], abs=1e-9)
            assert pd.isna(row.lineage_item11_se_bn)
        assert row.comparator_item11_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.item11_comparator_se_bn == pytest.approx(term['comparator_se_bn'], abs=1e-9)
        assert 'v9' in row.item11_se_scope and 'unmeasured' in row.item11_se_scope
        assert pd.isna(row.item11_paired_se_bn) and term['paired_se_bn'] is None
        assert row.item11_spending_bn + row.item11_receipt_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.cost_bn - row.cost_one_sided_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.cost_bn - row.cost_without_item11_bn == pytest.approx(term['bn'], abs=1e-9)
        assert '[FRAMING-SENSITIVE]' in row.framing
    # Reweighted readings are explicit; unmeasured current-rule rows are never eligible as the central.
    for row in d[d.group.str.startswith(('A3_', 'A4_'))].itertuples():
        assert 'reweighted' in row.mixed_unit_asymmetry
        assert row.cost_bn - row.cost_one_sided_bn == pytest.approx(row.comparator_item11_bn, abs=1e-9)
    for group in ('A2_us_born_nh_white', 'all_residents_slice'):
        rows = d[d.group.eq(group)]
        assert not rows.empty
        assert (rows.comparator_item11_bn == 0).all()
        assert rows.mixed_unit_asymmetry.str.startswith('unmeasured').all()
        assert rows.comparison_reading.eq('current-rule reading').all()
        assert rows.central_eligible.eq(False).all()
        assert not rows.arm.isin(MC.DERIVED).any()
    own = pd.read_csv(HERE / 'derived/symmetric_white_population_oct16.csv')
    lineage = d[d.group.eq('mexican_origin_engine')].set_index(['arm', 'basis', 'end', 'mortality_convention', 'mortality_bound'])
    for row in own.itertuples():
        assert row.lineage_minus_comparator_bn == pytest.approx(row.lineage_cost_bn - row.comparator_cost_bn, abs=1e-9)
        assert row.lineage_minus_comparator_bn - row.one_sided_gap_bn == pytest.approx(-row.comparator_item11_bn, abs=1e-9)
        # The lineage stays at its live count under its arm's rule in both frames.
        key = row.arm, row.basis, row.end, row.mortality_convention, row.mortality_bound
        assert row.lineage_population == pytest.approx(lineage.loc[key, 'population'], abs=1e-6)
        if row.membership_rule == 'current':
            live=json.loads((HERE.parent/'main_case_2026_10_16/derived/corrections.json').read_text())['meta']['population_v9']['with_coverage']
            assert row.lineage_population == pytest.approx(live, abs=1e-6)
        assert (row.population_warning == row.population_warning) == (row.population_basis == 'own_count')


def test_a3_a4_derived_publications_use_reconstructed_own_counts_and_factors():
    import comparison_contract as C
    import mortality_conventions as MC
    import symmetric_comparators_oct14 as S
    source = C.load_mixed_unit(case='oct16')
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    counts = json.loads((HERE / 'derived/members_coverage_oct16.json').read_text())['counts']
    for group in ('A3_third_plus_nh_white_at_union_ages', 'A4_third_plus_nh_white_stationary'):
        rows = d[d.group.eq(group) & d.arm.isin(MC.DERIVED)]
        assert {'combined_rules_members', 'combined_rules_coverage'} <= set(rows.arm)
        for arm in ('combined_rules_members', 'combined_rules_coverage'):
            principal = rows[rows.arm.eq(arm) & rows.mortality_convention.eq(MC.OWN)]
            assert len(principal) == 8  # two sets, two cost endpoints, two lineage profile bounds
        vectors = {}
        for row in rows.itertuples():
            spec = MC.DERIVED[row.arm]
            assert not spec.get('half')  # half-overlap departures are pair-specific A1/Black readings
            count = counts[f'{group}/{spec["rule"]}/central']
            assert row.true_own_count == pytest.approx(count['true_own_scale'], abs=1e-6)
            assert row.observed_own_count == pytest.approx(count['observed_own_scale'], abs=1e-6)
            factors = json.loads(row.item11_reweight_factors)
            assert set(factors) == {group}
            assert factors[group] == pytest.approx(count['item11_reweight'], abs=1e-12)
            assert set(factors[group]) == {'tax', 'spm', 'household'}
            assert all(np.isfinite(x) and x >= 0 for x in factors[group].values())
            key = row.basis, row.end
            vector_key = spec['rule'], *key, spec.get('partial_lineage', False)
            if vector_key not in vectors:
                vectors[vector_key] = (C.lineage_item11_replicates(source, *key) if spec['rule'] == 'current'
                                      else expanded_lineage_vector(S, *key, None, spec.get('partial_lineage', False)))
            vector = vectors[vector_key]
            term = C.true_count_removal(source, group, row.basis, row.end, row.population, row.true_own_count,
                                        row.item11_effective_rule, reweight=factors,
                                        observed_own=row.observed_own_count, lineage_replicates=vector)
            assert row.comparator_item11_bn == pytest.approx(term['bn'], abs=1e-9)
            assert row.item11_comparator_se_bn == pytest.approx(term['comparator_se_bn'], abs=1e-9)
            assert pd.isna(row.item11_paired_se_bn) and term['paired_se_bn'] is None
            assert row.item11_spending_bn == pytest.approx(term['spending_bn'], abs=1e-9)
            assert row.item11_receipt_bn == pytest.approx(term['receipt_bn'], abs=1e-9)
            assert pd.isna(row.lineage_item11_se_bn)
            own_term = C.true_count_removal(source, group, row.basis, row.end, row.true_own_count,
                                            row.true_own_count, row.item11_effective_rule, reweight=factors,
                                            observed_own=row.observed_own_count, lineage_replicates=vector)
            assert row.own_count_item11_bn == pytest.approx(own_term['bn'], abs=1e-9)
            assert row.own_count_item11_comparator_se_bn == pytest.approx(own_term['comparator_se_bn'], abs=1e-9)
            assert pd.isna(row.own_count_item11_paired_se_bn) and own_term['paired_se_bn'] is None
            assert row.own_count_item11_comparator_se_bn == pytest.approx(
                row.item11_comparator_se_bn * row.true_own_count / row.population, abs=1e-9)
        # Coverage changes the true denominator, without inventing a mixed-unit effect for missed people.
        for rule in ('current', 'children'):
            uncovered = counts[f'{group}/{rule}/none']
            covered = counts[f'{group}/{rule}/central']
            assert covered['observed_own_scale'] == uncovered['observed_own_scale']
            assert covered['item11_reweight'] == uncovered['item11_reweight']


def test_precedence_zero_overlap_and_half_membership_conservation():
    data = json.loads((HERE / 'derived/members_coverage_oct16.json').read_text())
    precedence = data['counts']['precedence']
    assert data['controls']['alternative_white_black_overlap_people'] > 0.
    assert 'pair' in data['controls']['overlap_gate_scope']
    for group in ('A1_third_plus_nh_white', 'nh_black_rough'):
        row = precedence[group]
        assert row['survey_weight_overlap'] == 0.
        assert row['overlap'] > 0.
        assert row['round3'] - row['lineage_precedence'] == pytest.approx(row['overlap'], abs=1e-6)
        assert row['half_overlap'] == pytest.approx(row['lineage_precedence'] + .5 * row['overlap'], abs=1e-6)
        assert row['lineage_half_overlap'] == pytest.approx(row['lineage_observed'] - .5 * row['overlap'], abs=1e-6)
        assert row['half_overlap'] + row['lineage_half_overlap'] == pytest.approx(
            row['lineage_precedence'] + row['lineage_observed'], abs=1e-6)
        assert data['counts'][f'{group}/children/none']['observed_own_scale'] == pytest.approx(
            row['lineage_precedence'], abs=1e-6)


def test_partial_lineage_survivor_arm_reproduces_old_source_patch_and_isolates_its_cost():
    import comparison_contract as C
    import symmetric_comparators_oct14 as S
    source = C.load_mixed_unit(case='oct16')
    counts = json.loads(S.LINEAGE_ROUND2.read_text())['membership']
    ratio = counts['outside_existing_addition_definition'] / counts['latent_children_with_two_US_parents']
    columns = [f'r{i}' for i in range(161)]
    for basis, method in [('accrual', 'set'), ('cash', 'cash')]:
        for end in ('low', 'high'):
            table = source['lineage_replicates']
            cells = table[(table.method == method) & (table.end == end)]
            vectors = cells.groupby('component')[columns].sum()
            old_patch = (vectors.loc['M6_all_biological_federal_tax_arm'] - vectors.loc['M6_biological_children']
                         + ratio * vectors.loc[f'bounded_{end}_membership_benefit_interaction'])
            expected = (vectors.loc[f'bounded_{end}'] + old_patch).to_numpy(float)
            actual = expanded_lineage_vector(S, basis, end, None, True)
            np.testing.assert_allclose(actual, expected, atol=1e-9, rtol=0.)
    rows = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    key = ['basis', 'end', 'mortality_convention', 'mortality_bound', 'group']
    full = rows[rows.arm.eq('combined_rules_members')].set_index(key)
    partial = rows[rows.arm.eq('combined_rules_members_partial_lineage')].set_index(key)
    assert not partial.empty and set(partial.index) == set(full.index)
    for index, old in partial.iterrows():
        current = full.loc[index]
        assert current.population == old.population
        assert current.capital_resource_cost_bn == pytest.approx(old.capital_resource_cost_bn, abs=1e-9)
        assert current.production_gain_bn == pytest.approx(old.production_gain_bn, abs=1e-9)
        if index[-1].startswith('mexican_'):
            difference = current.mixed_unit_removal_bn - old.mixed_unit_removal_bn
            assert current.cost_bn - old.cost_bn == pytest.approx(difference, abs=1e-9)
            assert current.lineage_children_block_bn == pytest.approx(old.lineage_children_block_bn, abs=1e-9)
        else:
            assert current.cost_bn == pytest.approx(old.cost_bn, abs=1e-9)
            assert current.comparator_item11_bn == pytest.approx(old.comparator_item11_bn, abs=1e-9)


def test_published_lineage_decomposition_and_complete_cost_identity():
    import mortality_conventions as MC
    results = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    for name in ('comparison_lineage_cost_bn', 'case_headline_cost_bn', 'lineage_children_block_bn',
                 'lineage_children_item11_bn', 'lineage_mortality_delta_bn', 'case_minus_rough_bridge_bn',
                 'lineage_policy_delta_bn'):
        assert name in results
    frames = [results, pd.read_csv(HERE / 'derived/symmetric_comparisons_oct16.csv'),
              pd.read_csv(HERE / 'derived/symmetric_white_population_oct16.csv'),
              pd.read_csv(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct16.csv')]
    for frame in frames:
        # Diagnostic policies are explicit deltas from the same live headline.
        rows = frame
        assert not rows.empty
        decomposition = (rows.case_headline_cost_bn - rows.case_minus_rough_bridge_bn
                         + rows.lineage_children_block_bn + rows.lineage_children_item11_bn
                         + rows.lineage_mortality_delta_bn + rows.lineage_policy_delta_bn)
        assert np.isfinite(decomposition).all()
        assert np.max(abs(decomposition - rows.comparison_lineage_cost_bn)) < 1e-9
        central = rows[rows.arm.eq('combined_rules_members') & rows.mortality_convention.eq(MC.OWN)]
        assert not central.empty and central.lineage_policy_delta_bn.abs().max() < 1e-9
        zero_production = rows[rows.arm.eq('production_zero')]
        assert not zero_production.empty and zero_production.lineage_policy_delta_bn.gt(0.).all()
    rows = results[results.arm.isin(MC.DERIVED)]
    assert np.max(abs(rows.cost_bn - (rows.responsive_budget_cost_bn + rows.capital_resource_cost_bn
                                     - rows.production_gain_bn))) < 1e-9
    assert np.max(abs(rows.contribution_to_others_bn + rows.cost_bn)) < 1e-9
    assert np.max(abs(rows.cost_per_person - rows.cost_bn * 1e9 / rows.population)) < 1e-6
    lineage = rows[rows.group.eq('mexican_origin_rough')]
    assert np.max(abs(lineage.cost_bn - lineage.comparison_lineage_cost_bn)) < 1e-9


def test_published_base_budget_identity_and_member_balance_definition():
    for lane in (HERE, HERE.parent / 'black_comparator_rough_2026_09_28'):
        d = pd.read_csv(lane / 'derived/rekey_summary_oct16.csv')
        for row in d[d.group.str.startswith(('A1_', 'A3_', 'A4_', 'nh_black'))].itertuples():
            assert row.cost - row.cost_evaluator_bn == pytest.approx(row.comparator_item11_bn, abs=5e-5)
            assert row.cost == pytest.approx(row.net_budget + row.capital - row.production_gain, abs=2e-4)
            assert row.balance == pytest.approx(row.taxes_paid - row.spending_drawn, abs=1e-4)
            # Three independently printed four-decimal fields, plus the added
            # correction's second rounding: up to two displayed units.
            assert row.net_budget == pytest.approx(row.spending_saved - row.taxes_lost, abs=2e-4)


def test_tax_parts_exclude_post_evaluator_metadata_from_decomposition():
    import income_tax_parts as P
    d = pd.read_csv(HERE / 'derived/income_tax_parts_oct16.csv')
    total = d[[f'{part}_bn' for part in P.PARTS]].sum(axis=1)
    assert (total - (d.central_bn - d.cps_bn)).abs().max() < 1e-3
    a1 = d[d.figure.eq('gap: union less A1_third_plus_nh_white')]
    assert (a1.central_with_comparator_item11_bn - a1.central_bn + a1.comparator_item11_bn).abs().max() < 1e-4


def test_zero_production_removes_whole_lineage_gain():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv').query("mortality_bound == 'none'")
    for group in ('mexican_origin_engine', 'mexican_origin_rough'):
        for end in ('low', 'high'):
            for basis in ('accrual', 'cash'):
                sub = d[(d.group == group) & (d.end == end) & (d.basis == basis)].set_index('arm')
                raw, zero = sub.loc['legacy_raw'], sub.loc['production_zero']
                assert zero.production_gain_bn == 0
                assert zero.cost_bn - raw.cost_bn == pytest.approx(raw.production_gain_bn, abs=1e-9)
                assert zero.population == raw.population


def test_scalar_change_is_fail_closed_in_actual_consumer():
    import rekey_sept29 as W
    dump = json.loads((HERE / 'derived/engine_lines_oct16_union.json').read_text())
    dump['low']['lines'].append({'side': 'scalar', 'id': 'new_national_credit', 'effect_bn': 99})
    with pytest.raises(SystemExit, match='undeclared or duplicate comparator scalar policy'):
        W.run29('eng', 'low', dump=dump)


def test_black_population_standardization_is_per_person():
    d = pd.read_csv(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct16.csv')
    principal = json.loads((HERE.parent / 'main_case_2026_10_16/derived/corrections.json').read_text())
    count = principal['meta']['population_v9']['with_coverage']
    results = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv')
    lineage = results[results.group.eq('mexican_origin_engine')].set_index(
        ['arm', 'basis', 'end', 'mortality_convention', 'mortality_bound']).population
    for key, pair in d.groupby(['arm', 'basis', 'end', 'mortality_convention', 'mortality_bound']):
        pair = pair.set_index('population_basis')
        own, scaled = pair.loc['own_count'], pair.loc['scaled_to_lineage']
        # the lineage's count under the arm's rule: the case's, plus its children block under the children rule
        assert scaled.population == pytest.approx(lineage.loc[key], abs=1e-6)
        if own.membership_rule == 'current':
            assert scaled.population == pytest.approx(count, abs=1e-6)
        assert scaled.cost_per_person == own.cost_per_person
        assert scaled.cost_bn / scaled.population == pytest.approx(own.cost_bn / own.population, abs=1e-15)


def test_group_mortality_does_not_change_cash_flows():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct16.csv').query("basis == 'cash' and mortality_bound == 'none'")
    assert d[d.arm.eq('mortality_group')].change_from_raw_bn.abs().max() < 1e-9


def test_report_render_preserves_history_and_is_byte_idempotent(tmp_path, monkeypatch):
    import shutil
    import render_oct15_result as render
    white, black = tmp_path / 'white', tmp_path / 'black'
    for lane in (white, black):
        (lane / 'derived').mkdir(parents=True)
    for name in ('symmetric_results_oct16.csv', 'symmetric_comparisons_oct16.csv', 'symmetric_white_population_oct16.csv',
                  'symmetric_hispanic_arm_oct16.csv', 'symmetric_status_sampling_oct16.csv', 'round2_changes_oct16.csv',
                  'members_coverage_oct16.json'):
        shutil.copyfile(HERE / 'derived' / name, white / 'derived' / name)
    shutil.copyfile(HERE / 'derived/domestic_source_changes_oct16.csv', white / 'derived/domestic_source_changes_oct16.csv')
    shutil.copyfile(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct16.csv',
                    black / 'derived/symmetric_population_oct16.csv')
    originals = {white: 'Original white evidence.\n', black: 'Original Black evidence.\n'}
    for lane, old in originals.items():
        (lane / 'RESULT.md').write_text(old)
    monkeypatch.setattr(render, 'HERE', white)
    monkeypatch.setattr(render, 'BLACK', black)
    render.render()
    first = {lane: (lane / 'RESULT.md').read_bytes() for lane in originals}
    render.render()
    for lane, old in originals.items():
        assert (lane / 'RESULT.md').read_bytes() == first[lane]
        assert (lane / 'RESULT.md').read_text().startswith(old)
