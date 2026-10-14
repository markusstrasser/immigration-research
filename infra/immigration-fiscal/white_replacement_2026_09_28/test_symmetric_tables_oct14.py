"""Independent closure checks on delivered sensitivity tables and population bases."""
import json
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent


def test_actual_comparator_publications_match_pinned_terms_and_paired_se():
    import comparison_contract as C
    import mortality_conventions as MC
    source = C.load_mixed_unit()
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv')
    for row in d[d.group.isin(C.MIXED_GROUPS)].itertuples():
        spec = MC.DERIVED.get(row.arm)
        if spec is None:
            term = C.comparator_removal(source, row.group, row.basis, row.end, row.population)
        else:
            term = C.true_count_removal(source, row.group, row.basis, row.end, row.population, row.true_own_count, spec['rule'])
        assert row.comparator_item11_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.item11_paired_se_bn == pytest.approx(term['paired_se_bn'], abs=1e-9)
        assert row.item11_spending_bn + row.item11_receipt_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.cost_bn - row.cost_one_sided_bn == pytest.approx(term['bn'], abs=1e-9)
        assert row.cost_bn - row.cost_without_item11_bn == pytest.approx(term['bn'], abs=1e-9)
        assert '[FRAMING-SENSITIVE]' in row.framing
    # Round 3 (C3 fix 5): A3 and A4 carry A1's term reweighted, labelled; A2 stays unmeasured at zero.
    for row in d[d.group.str.startswith(('A3_', 'A4_'))].itertuples():
        assert row.mixed_unit_asymmetry.startswith('reweighted from A1')
        assert row.cost_bn - row.cost_one_sided_bn == pytest.approx(row.comparator_item11_bn, abs=1e-9)
    a2 = d[d.group.eq('A2_us_born_nh_white')]
    assert (a2.comparator_item11_bn == 0).all() and a2.mixed_unit_asymmetry.str.startswith('unmeasured').all()
    own = pd.read_csv(HERE / 'derived/symmetric_white_population_oct15.csv')
    lineage = d[d.group.eq('mexican_origin_engine')].set_index(['arm', 'basis', 'end', 'mortality_convention', 'mortality_bound'])
    for row in own.itertuples():
        assert row.lineage_minus_comparator_bn == pytest.approx(row.lineage_cost_bn - row.comparator_cost_bn, abs=1e-9)
        assert row.lineage_minus_comparator_bn - row.one_sided_gap_bn == pytest.approx(-row.comparator_item11_bn, abs=1e-9)
        # The lineage stays at its live count under its arm's rule in both frames.
        key = row.arm, row.basis, row.end, row.mortality_convention, row.mortality_bound
        assert row.lineage_population == pytest.approx(lineage.loc[key, 'population'], abs=1e-6)
        if row.membership_rule == 'current':
            assert row.lineage_population == pytest.approx(float(source['gaps'][0]['lineage_count']), abs=1e-6)
        assert (row.population_warning == row.population_warning) == (row.population_basis == 'own_count')


def test_published_base_budget_identity_and_member_balance_definition():
    for lane in (HERE, HERE.parent / 'black_comparator_rough_2026_09_28'):
        d = pd.read_csv(lane / 'derived/rekey_summary_oct15.csv')
        for row in d[d.group.str.startswith(('A1_', 'A3_', 'A4_', 'nh_black'))].itertuples():
            assert row.cost - row.cost_evaluator_bn == pytest.approx(row.comparator_item11_bn, abs=5e-5)
            assert row.cost == pytest.approx(row.net_budget + row.capital - row.production_gain, abs=2e-4)
            assert row.balance == pytest.approx(row.taxes_paid - row.spending_drawn, abs=1e-4)
            # Three independently printed four-decimal fields, plus the added
            # correction's second rounding: up to two displayed units.
            assert row.net_budget == pytest.approx(row.spending_saved - row.taxes_lost, abs=2e-4)


def test_tax_parts_exclude_post_evaluator_metadata_from_decomposition():
    import income_tax_parts as P
    d = pd.read_csv(HERE / 'derived/income_tax_parts_oct15.csv')
    total = d[[f'{part}_bn' for part in P.PARTS]].sum(axis=1)
    assert (total - (d.central_bn - d.cps_bn)).abs().max() < 1e-3
    a1 = d[d.figure.eq('gap: union less A1_third_plus_nh_white')]
    assert (a1.central_with_comparator_item11_bn - a1.central_bn + a1.comparator_item11_bn).abs().max() < 1e-4


def test_zero_production_removes_whole_lineage_gain():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv').query("mortality_bound == 'none'")
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
    dump = json.loads((HERE / 'derived/engine_lines_oct15_union.json').read_text())
    dump['low']['lines'].append({'side': 'scalar', 'id': 'new_national_credit', 'effect_bn': 99})
    with pytest.raises(SystemExit, match='undeclared or duplicate comparator scalar policy'):
        W.run29('eng', 'low', dump=dump)


def test_black_population_standardization_is_per_person():
    d = pd.read_csv(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct15.csv')
    principal = json.loads((HERE.parent / 'main_case_2026_10_15/derived/corrections.json').read_text())
    count = principal['meta']['population_v8']['with_coverage']
    results = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv')
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
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct15.csv').query("basis == 'cash' and mortality_bound == 'none'")
    assert d[d.arm.eq('mortality_group')].change_from_raw_bn.abs().max() < 1e-9


def test_report_render_preserves_history_and_is_byte_idempotent(tmp_path, monkeypatch):
    import shutil
    import render_oct15_result as render
    white, black = tmp_path / 'white', tmp_path / 'black'
    for lane in (white, black):
        (lane / 'derived').mkdir(parents=True)
    for name in ('symmetric_results_oct15.csv', 'symmetric_comparisons_oct15.csv', 'symmetric_white_population_oct15.csv',
                  'symmetric_hispanic_arm_oct15.csv', 'symmetric_status_sampling_oct15.csv', 'round2_changes_oct15.csv'):
        shutil.copyfile(HERE / 'derived' / name, white / 'derived' / name)
    shutil.copyfile(HERE / 'derived/domestic_source_changes_oct15.csv', white / 'derived/domestic_source_changes_oct15.csv')
    shutil.copyfile(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct15.csv',
                    black / 'derived/symmetric_population_oct15.csv')
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
