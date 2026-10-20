"""Permanent gates: `backcast.py --case sept24`, `--case sept26` and `--case sept26_schools` rebuild the
files committed for those cases byte for byte, and the default run (the main case of 2026-09-27) rebuilds
the derived/ files, its case_components.cjs input included. The main case adopted on 2026-09-29 (`--case sept29`)
writes derived/sept29/ and derived/case_components_sept29.json beside them; its run rebuilds both. So does the main
case adopted on 2026-10-05 (`--case oct05`, derived/oct05/), whose third-plus path input (inputs/cps_g3plus_path.csv)
rebuilds from the pooled CPS extract when that ignored file is on disk, and main case v6 (`--case oct07`,
derived/oct07/ and derived/case_components_oct07.json).

The files of each earlier case are the ones committed at its commit below, the last commit whose derived/
held that run. debt_legacy.py reads each case's concept columns, so they must keep their values.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/historical_backcast_2026_09_20/ -q --import-mode=importlib
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SEPT24_COMMIT = "da2b107"
SEPT26_COMMIT = "f5b4aae"
SCHOOLS_COMMIT = "c0297e4"
DERIVED = "infra/immigration-fiscal/historical_backcast_2026_09_20/derived"
NAMES = ("backcast_annual.csv", "backcast_windows.csv")
PARTS = ("case_parts_windows.csv", "case_parts_annual.csv")
DEFAULT_NAMES = NAMES + PARTS


def rebuild(tmp_path: Path, *args: str) -> None:
    run = subprocess.run([sys.executable, str(HERE / "backcast.py"), *args, "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
    assert run.returncode == 0, run.stderr[-2000:]


@pytest.mark.parametrize("case, commit", [("sept24", SEPT24_COMMIT), ("sept26", SEPT26_COMMIT),
                                          ("sept26_schools", SCHOOLS_COMMIT)])
def test_old_case_rebuilds_committed_files(tmp_path, case, commit):
    rebuild(tmp_path, "--case", case)
    committed = {n: subprocess.run(["git", "show", f"{commit}:{DERIVED}/{n}"], cwd=ROOT, capture_output=True,
                                   check=True).stdout for n in NAMES}
    differ = [n for n in NAMES if (tmp_path / n).read_bytes() != committed[n]]
    assert not differ, differ
    assert not any((tmp_path / n).exists() for n in PARTS)


@pytest.mark.parametrize("case", ["sept27", "sept29", "oct05", "oct07", "oct14"])
def test_case_components_rebuild(tmp_path, case):
    run = subprocess.run(["node", str(HERE / "case_components.cjs"), "--case", case, "--out-dir", str(tmp_path)], cwd=ROOT,
                         capture_output=True, text=True)
    assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
    name = f"case_components_{case}.json"
    assert (tmp_path / name).read_bytes() == (HERE / "derived" / name).read_bytes()


def test_archived_sept27_rebuilds_derived(tmp_path):
    rebuild(tmp_path, "--case", "sept27")
    differ = [n for n in DEFAULT_NAMES if (tmp_path / n).read_bytes() != (HERE / "derived" / n).read_bytes()]
    assert not differ, differ


@pytest.mark.parametrize("case", ["sept29", "oct05", "oct07", "oct14"])
def test_case_rebuilds_its_directory(tmp_path, case):
    rebuild(tmp_path, "--case", case)
    assert sorted(p.name for p in tmp_path.iterdir()) == sorted(p.name for p in (HERE / "derived" / case).iterdir())
    differ = [n for n in DEFAULT_NAMES if (tmp_path / n).read_bytes() != (HERE / "derived" / case / n).read_bytes()]
    assert not differ, differ


def test_live_case_default_and_lineage_denominator():
    import importlib.util

    spec = importlib.util.spec_from_file_location("backcast_live", HERE / "backcast.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    assert module.DEFAULT_CASE == "oct16"
    assert "oct15" not in module.later_cases("oct16")
    import json
    import pandas as pd

    annual = pd.read_csv(HERE / "derived/oct16/backcast_annual.csv").set_index("year")
    summary = json.loads((HERE.parent / "main_case_2026_10_16/derived/summary.json").read_text())
    per_member = summary["v9"]["per_member_usd"]
    assert abs(annual.loc[2024, "lineage_millions"] - summary["v9"]["population"]["with_coverage"] / 1e6) < 5e-5
    for name, want in zip(module.PER_LINEAGE_MEMBER["oct16"], per_member["set"]):
        for rule in ("ratio", "income"):
            assert abs(annual.loc[2024, f"{name}__{rule}__per_lineage_member_usd"] - want) < 0.01


def test_v8_components_are_distinct_and_close_to_the_live_principal():
    import json

    data = json.loads((HERE / "derived/case_components_oct15.json").read_text())
    summary = json.loads((HERE.parent / "main_case_2026_10_15/derived/summary.json").read_text())["v8"]
    block = data["concepts"]["net_cost_cbo_informed"]
    for i, end in enumerate(("low", "high")):
        row = block["ends"][end]
        amount = row["base_bn"] + sum(row["additions_bn"].values()) + sum(row["capital_bn"].values()) \
            + sum(row["v5_capital_bn"].values()) + sum(sum(p.values()) for p in row["v6_capital_bn"].values())
        assert abs(amount - summary["band_bn"][i]) < 1e-9
    for item in ("foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage"):
        assert any(p["item"] == item for p in block["v6_parts"].values())
    capital = [p for p in block["v6_parts"].values() if p["item"] == "union_completion" and p["rule"] == "capital"]
    assert capital and all(p.get('path') == 'lineage' or p.get('population_path') == 'g3plus' for p in capital)
    constants = [p for p in block['v6_parts'].values() if p['line'] == 'lane_constants']
    assert constants and all(p['rule'] == 'per_person' for p in constants)


def test_retired_historical_rate_switch_fails_loudly(tmp_path):
    run = subprocess.run([sys.executable, str(HERE / "backcast.py"), "--case", "oct15", "--out-dir", str(tmp_path)],
                         cwd=ROOT, env={**os.environ, "OPENBLAS_NUM_THREADS": "1", "BACKCAST_RATE_ANCHOR": "historical_all_years"},
                         capture_output=True, text=True)
    assert run.returncode != 0
    assert "BACKCAST_RATE_ANCHOR retired" in run.stderr
    assert not list(tmp_path.iterdir())


def test_round2_pension_rules_and_fixed_resource_rate():
    import json
    import pandas as pd

    table = pd.read_csv(HERE / "derived/oct15/round2_income_parts.csv")
    hi = table[table.contributions == "hi"]
    assert len(hi) and hi[hi.year < 2019].after_delta_bn.abs().max() == 0
    assert hi[hi.year.between(2019, 2023)].after_delta_bn.abs().max() > .01
    oasdi = table[(table.contributions == "oasdi") & (table.year != 2024)]
    assert len(oasdi)
    assert (oasdi.after_delta_bn - oasdi.before_unit_delta_bn).abs().max() > .01
    assert table[table.year == 2024][["before_unit_delta_bn", "after_delta_bn"]].abs().to_numpy().max() < 1e-9
    paths = pd.read_csv(HERE / "derived/oct15/round2_income_paths.csv").set_index("year")
    assert paths.loc[:2018].covered_workers_per_member.eq(1.).all()
    assert paths.loc[2019:2023].covered_workers_per_member.ne(1.).any()
    assert paths.loc[2024].eq(1.).all()
    audit = json.loads((HERE / "derived/oct15/round2_pension_audit.json").read_text())
    assert 0 < audit["groups"]["union"]["pia_earnings_elasticity"] < 1
    changes = pd.read_csv(HERE / "derived/oct15/round2_annual.csv")
    for _, rows in changes.groupby(["concept", "rule", "year"]):
        rows = rows.set_index("scenario")
        live = rows.loc["live_fixed_resource_rates", "cost_bn"] if "live_fixed_resource_rates" in rows.index else None
        if live is None:
            continue
        financing = rows.loc["financing_cost_dfii10_floor0_beside", "cost_bn"]
        if "_high" in rows.iloc[0].concept:
            assert abs(live - financing) < 1e-9
    assert not changes.cost_bn.isna().any()


def test_preserved_CPS_worker_split_identity_and_available_years():
    import pandas as pd

    table = pd.read_csv(HERE / 'derived/oct15/worker_income.csv')
    assert table.survey_year.eq(table.year + 1).all()
    assert (table.relative_workers_per_member * table.relative_earnings_per_worker
            - table.relative_labour_income_per_member).abs().max() < 1e-10
    assert table.group_workers.le(table.group_population).all()
    assert table.national_workers.le(table.national_population).all()
    measured = table[table.definition.eq('positive_wage_or_SE_age_lt65')]
    assert set(measured.year) == set(range(2019, 2025))
    assert measured[measured.year == 2024].source.str.endswith('asecpub25csv.zip').all()
    wage_only = table[table.definition.eq('wage_only_age_lt65_IPUMS_all_ASEC')]
    assert set(wage_only.year) == set(range(2005, 2025))


def test_unknown_accrual_does_not_fall_back_to_unit_income():
    import importlib.util
    import pandas as pd

    spec = importlib.util.spec_from_file_location('pension_transport_gate', HERE / 'pension_transport.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with pytest.raises(ValueError, match='unknown pension contribution rule'):
        module.part_factor('new_health_promise', {'rule': 'accrual', 'contributions': 'unknown'},
                           {'covered_workers_per_member_union': pd.Series([1.])})


def test_missing_historical_use_cell_fails_except_declared_coverage_gap():
    import sys
    import pandas as pd
    sys.path.insert(0, str(HERE))
    from p7_backcast import use_cell
    use = pd.read_csv(HERE / 'derived/p7/historical_use.csv').set_index(['key', 'group', 'year'])
    for cell in [('school_age_5_17', 'union', 2010), ('medicaid_covered', 'g3plus', 2021)]:
        with pytest.raises(ValueError, match='missing historical-use cell'):
            use_cell(use.drop(index=cell), *cell)
    assert use_cell(use, 'medicaid_covered', 'union', 2010) is None


def test_joint_programme_branches_reconcile():
    import pandas as pd
    branches = pd.read_csv(HERE / 'derived/oct15/round2_programme_branches.csv')
    assert branches.reconciliation_residual_bn.abs().max() <= 1e-9
    reconciliation = pd.read_csv(HERE / 'derived/oct15/round2_charged_programme_reconciliation.csv')
    assert reconciliation.residual_bn.abs().max() <= 1e-9
    assert (reconciliation.programme_minus_charged_bn - reconciliation.programme_delta_bn
            + reconciliation.charged_base_delta_bn).abs().max() <= 1e-9
    assert set(branches.branch) == {'programme_spending', 'pandemic_measured', 'historical_school_medicaid',
                                    'new_known_use_keys', 'per_part_income', 'precision_anchor'}
    base = pd.read_csv(HERE / 'derived/oct15/round2_added_expenditure_base.csv')
    assert base.gross_added_expenditure_2024_bn.gt(0).all()
    assert (base.gross_added_expenditure_2024_bn - base.separately_carried_added_expenditure_2024_bn
            - base.residual_added_expenditure_2024_bn).abs().max() <= 1e-9
    income_parts = pd.read_csv(HERE / 'derived/oct15/round2_income_parts.csv')
    keys = ['concept', 'part', 'year']
    assert income_parts[keys].equals(income_parts.sort_values(keys)[keys].reset_index(drop=True))


def test_pandemic_zero_is_an_explicit_amount_gate(tmp_path, monkeypatch):
    import json
    import sys
    sys.path.insert(0, str(HERE))
    import pandemic_zero
    assert pandemic_zero.require_zero() == 0
    audit = json.loads(pandemic_zero.OUT.read_text())
    audit['national_bn'] = 0.1
    altered = tmp_path / 'zero.json'
    altered.write_text(json.dumps(audit))
    monkeypatch.setattr(pandemic_zero, 'OUT', altered)
    with pytest.raises(ValueError, match='no longer structurally zero'):
        pandemic_zero.require_zero()


def test_mixed_programme_parts_close_and_preserve_D_lineage():
    import json
    data = json.loads((HERE / 'derived/mixed_components_oct15.json').read_text())
    for basis in ('set', 'cash'):
        payload = HERE.parent / f'main_case_2026_10_15/derived/corrections{"_cash" if basis == "cash" else ""}.json'
        principal = json.loads(payload.read_text())['meta']['mixed_unit_removal']['by_end']
        for end in ('low', 'high'):
            rows = [r for r in data['sets'][basis] if r['end'] == end]
            assert {r['side'] for r in rows} == {'receipt', 'spending'}
            assert abs(sum(r['value_bn'] for r in rows) - principal[end]['total_bn']) <= 1e-9
            for gen in ('G1', 'G2', 'G3+'):
                assert abs(sum(r['value_bn'] for r in rows if r['generation'] == gen)
                           - principal[end]['by_generation_bn'][gen]) <= 1e-9
            own = [r for r in rows if r['path'] == 'lineage']
            assert own and {r['component'] for r in own} == {'D_added_residual'}
            assert abs(sum(r['value_bn'] for r in own) - principal[end]['D_added_residual_bn']) <= 1e-9


def test_pre2024_G3_coverage_count_uses_its_cost_path():
    import sys
    import pandas as pd
    sys.path.insert(0, str(HERE))
    from backcast import transported_lineage_count
    group = pd.Series({2015: 8., 2024: 10.})
    g3 = pd.Series({2015: 2., 2024: 5.})
    count = transported_lineage_count(group, g3, union=10., added=3., reporters=0.5, covered_g3=0.7)
    expected = (10. - 0.5 - 0.7) * 0.8 + (3. + 0.5 + 0.7) * 0.4
    assert abs(count[2015] - expected) < 1e-12
    assert count[2024] == 13.


def test_non_EIP_credit_gate_uses_requested_years_and_rejects_missing_current_cell(monkeypatch):
    import sys
    import pandas as pd
    sys.path.insert(0, str(HERE))
    import backcast as b
    from p7_backcast import pandemic_amounts
    nominal = pd.Series(229., index=range(1929, 2025))
    nominal.loc[:1975] = float('nan')
    for year, paid in pandemic_amounts().items():
        nominal[year] += paid
    monkeypatch.setattr(b, 'line', lambda *args: nominal * 1e3)
    data = {'concepts': {'x': {'v6_parts': {'typed': {'rule': 'non_eip_credits',
            'line': 'refundable_tax_credits', 'national_bn': 229.}}}}}
    categories = pd.DataFrame({'source_cells': ['T31200-A:25']}, index=['refundable_tax_credits'])
    real = pd.Series(1., index=b.YEARS)
    paths = b.v4_series(data, None, None, real, categories, {}, 'v6')
    assert paths['typed'].eq(1.).all()
    nominal[2010] = float('nan')
    with pytest.raises(ValueError, match='typed'):
        b.v4_series(data, None, None, real, categories, {}, 'v6')


def test_typed_coverage_aliases_and_signed_production_are_preserved():
    import importlib.util

    spec = importlib.util.spec_from_file_location('coverage_components_gate', HERE / 'coverage_components.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    source, lines = {'ends': {}, 'parts': {}}, {'generations': {'G1': {}}}
    for end in module.C.ENDS:
        pieces = [dict(generation='G1', line='native_child_spending_medicare', source_line='medicare',
                       source_side='spending', category='pension_accrual', economic_class='fiscal_line', coverage_bn=2.),
                  dict(generation='G1', line='native_child_capital_k12', source_line='k12', level='state_local',
                       category='capital', economic_class='capital_return', coverage_bn=3.),
                  dict(generation='G1', line='production', source_line='production', economic_class='production',
                       coverage_bn=-.5, P_bn=.2, F_bn=.3),
                  dict(generation='G1', line='named_unknown', economic_class='unclassified_residual', coverage_bn=.25)]
        source['ends'][end] = dict(total_bn=4.75, by_generation=dict(G1=4.75, G2=0., G3plus=0.),
                                   decomposition=dict(line_parts=pieces, total_cost_bn=4.75,
                                                      production=dict(scope='source generation ratio')))
        source['parts'][end] = dict(added=dict(coverage_bn=0.))
        lines['generations']['G1'][end] = dict(capital=[dict(id='k12', level='state_local', part='core')])
    rows = module.typed_rows(source, lines)
    assert any(r['line'] == 'medicare' and r['source_piece_line'] == 'native_child_spending_medicare' for r in rows)
    assert any(r['line'] == 'induced_receipts_bn' and r['value_bn'] == -.3 for r in rows)
    assert any(r['line'] == 'named_unknown' and r['unlocated'] for r in rows)
    source['ends']['low']['decomposition']['line_parts'][0]['source_line'] = 'unknown_health_promise'
    with pytest.raises(ValueError, match='source-specific income rule'):
        module.typed_rows(source, lines)


@pytest.mark.skipif(not (HERE.parent / "g3_identity_pooled_2026_10_05/_cache/asec_pooled.csv.gz").exists(),
                    reason="the pooled CPS ASEC extract (ignored) is not on disk")
def test_g3plus_path_rebuilds(tmp_path):
    path = HERE / "inputs/cps_g3plus_path.csv"
    kept = path.read_bytes()
    try:
        run = subprocess.run([sys.executable, str(HERE / "cps_g3plus_path.py")], cwd=ROOT,
                             env={**os.environ, "OPENBLAS_NUM_THREADS": "1"}, capture_output=True, text=True)
        assert run.returncode == 0, run.stdout[-2000:] + run.stderr[-2000:]
        assert path.read_bytes() == kept
    finally:
        path.write_bytes(kept)
