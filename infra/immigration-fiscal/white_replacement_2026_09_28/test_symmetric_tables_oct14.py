"""Independent closure checks on delivered sensitivity tables and population bases."""
import json
from pathlib import Path

import pandas as pd
import pytest

HERE = Path(__file__).resolve().parent


def test_zero_production_removes_whole_lineage_gain():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct14.csv')
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
    dump = json.loads((HERE / 'derived/engine_lines_oct14_union.json').read_text())
    dump['low']['lines'].append({'side': 'scalar', 'id': 'new_national_credit', 'effect_bn': 99})
    with pytest.raises(SystemExit, match='undeclared or duplicate comparator scalar policy'):
        W.run29('eng', 'low', dump=dump)


def test_black_population_standardization_is_per_person():
    d = pd.read_csv(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct14.csv')
    principal = json.loads((HERE.parent / 'main_case_2026_10_14/derived/corrections.json').read_text())
    count = principal['meta']['lineage']['counts']['lineage_population']
    for _, pair in d.groupby(['arm', 'basis', 'end']):
        pair = pair.set_index('population_basis')
        own, scaled = pair.loc['own_count'], pair.loc['scaled_to_lineage']
        assert scaled.population == pytest.approx(count, abs=1e-6)
        assert scaled.cost_per_person == own.cost_per_person
        assert scaled.cost_bn / scaled.population == pytest.approx(own.cost_bn / own.population, abs=1e-15)


def test_group_mortality_does_not_change_cash_flows():
    d = pd.read_csv(HERE / 'derived/symmetric_results_oct14.csv').query("basis == 'cash'")
    assert d[d.arm.eq('mortality_group')].change_from_raw_bn.abs().max() < 1e-9


def test_report_render_preserves_history_and_is_byte_idempotent(tmp_path, monkeypatch):
    import shutil
    import render_symmetric_result as render
    white, black = tmp_path / 'white', tmp_path / 'black'
    for lane in (white, black):
        (lane / 'derived').mkdir(parents=True)
    for name in ('symmetric_results_oct14.csv', 'symmetric_comparisons_oct14.csv',
                 'symmetric_hispanic_arm_oct14.csv', 'symmetric_status_sampling_oct14.csv'):
        shutil.copyfile(HERE / 'derived' / name, white / 'derived' / name)
    shutil.copyfile(HERE.parent / 'black_comparator_rough_2026_09_28/derived/symmetric_population_oct14.csv',
                    black / 'derived/symmetric_population_oct14.csv')
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
        assert (lane / 'RESULT.md').read_text().endswith(old)
