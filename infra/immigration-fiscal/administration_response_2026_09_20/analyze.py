"""Reproduce descriptive population-administration diagnostics; no causal calibration."""
from pathlib import Path
import hashlib
import json
import zipfile

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
OUT = HERE / 'derived'
YEARS = [2012, 2017, 2018, 2019, 2020, 2021, 2022, 2023]
CODES = ['E23', 'E29', 'E31']
HASHES = {}
EXPECTED_HASHES = json.loads((HERE/'inputs.sha256.json').read_text())


def record(path):
    key = str(path.relative_to(BASE))
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if EXPECTED_HASHES.get(key) != actual:
        raise ValueError(f'Unreviewed input vintage: {key}')
    HASHES[key] = actual


def unique_member(zf, ending):
    names = [n for n in zf.namelist() if Path(n).name.lower() == ending.lower()]
    if len(names) != 1:
        raise ValueError(f'Expected one {ending}: {names}')
    return names[0]


def read_finance():
    rows = []
    for year in YEARS:
        path = BASE / 'local_spending_composition_2026_09_18' / '_cache' / f'indunit_{year}.zip'
        record(path)
        with zipfile.ZipFile(path) as zf:
            mapping = {0: 0}
            if year == 2012:
                gid = unique_member(zf, 'Fin_GID_2012.txt')
                for line in zf.read(gid).decode('latin-1').splitlines():
                    if len(line) >= 118 and line[:2].isdigit() and line[113:115].isdigit():
                        old, new = int(line[:2]), int(line[113:115])
                        if old in mapping and mapping[old] != new:
                            raise ValueError('Inconsistent 2012 state crosswalk')
                        mapping[old] = new
            name = unique_member(zf, f'{str(year)[2:]}statetypepu.txt')
            for line in zf.read(name).decode('latin-1').splitlines():
                parts = line.split()
                if len(parts) < 2 or parts[1] not in CODES:
                    continue
                state_level, code = parts[:2]
                if len(state_level) != 3 or int(state_level[2]) not in [1, 2, 3]:
                    continue
                if len(parts) != 5:
                    raise ValueError(f'Unexpected selected record: {line}')
                state, level = int(state_level[:2]), int(state_level[2])
                if year == 2012:
                    state = mapping[state]
                amount, cv, yy = float(parts[2]), float(parts[3]), int(parts[4])
                if yy != year % 100 or amount < 0 or cv < 0:
                    raise ValueError(f'Invalid amount, CV or vintage: {line}')
                rows.append((year, state, level, code, amount, cv))
    data = pd.DataFrame(rows, columns=['year', 'state', 'level', 'code', 'amount_thousands', 'cv'])
    if data.duplicated(['year', 'state', 'level', 'code']).any():
        raise ValueError('Duplicate selected records')
    return data


def validate(data):
    path = BASE / 'macro_closure_2026_09_19' / '_cache' / 'finance_2022_us_combined.json'
    record(path)
    raw = json.loads(path.read_text())
    api = pd.DataFrame(raw[1:], columns=raw[0]).set_index('AGG_DESC')
    crosswalk = {'E23': 'LF0181', 'E29': 'LF0190', 'E31': 'LF0187'}
    checks = []
    for code, field in crosswalk.items():
        observed = data.query('year == 2022 and state == 0 and level == 1 and code == @code').amount_thousands.item()
        expected = float(api.loc[field, 'AMOUNT'])
        if observed != expected:
            raise ValueError(f'National API mismatch: {code} {observed} {expected}')
        checks.append({'check': '2022_national_API', 'code': code, 'amount_thousands': observed})
    for (year, level, code), group in data.groupby(['year', 'level', 'code']):
        national = group.loc[group.state.eq(0), 'amount_thousands'].item()
        states = group.loc[group.state.ne(0), 'amount_thousands'].sum()
        if abs(national - states) > 52:
            raise ValueError(f'National/state sum mismatch: {(year, level, code, national, states)}')
    levels = data.pivot(index=['year', 'state', 'code'], columns='level', values='amount_thousands').dropna()
    error = levels[1] - levels[2] - levels[3]
    if error.abs().max() > 2:
        raise ValueError('Combined/state/local operations do not conserve')
    checks.append({'check': 'level_conservation_max_thousands', 'amount_thousands': float(error.abs().max())})
    return checks


def panel(data):
    path = BASE / 'tiebout_sorting_2026_09_18' / '_cache' / 'state_covariates.csv'
    record(path)
    pop = pd.read_csv(path)[['state', 'year', 'B01003_001E']].rename(columns={'B01003_001E': 'population'})
    pop[['state', 'year']] = pop[['state', 'year']].astype(int)
    if pop.duplicated(['state', 'year']).any():
        raise ValueError('Duplicate population keys')
    d = data.loc[~data.state.isin([0, 11, 72])].pivot(index=['year', 'state', 'level'], columns='code', values='amount_thousands').reset_index()
    d = d.merge(pop, on=['state', 'year'], how='left', validate='many_to_one')
    missing_years = sorted(d.loc[d.population.isna(), 'year'].unique().tolist())
    if missing_years != [2020]:
        raise ValueError(f'Unexpected population gaps: {missing_years}')
    d = d.loc[d.year.ne(2020)].copy()
    if d.state.nunique() != 50 or d.population.le(0).any():
        raise ValueError('Unexpected population/state coverage')
    d['admin'] = d[CODES].sum(axis=1, min_count=3)
    d['central'] = d[['E23', 'E29']].sum(axis=1, min_count=2)
    d['log_population'] = np.log(d.population)
    initial = d.sort_values('year').drop_duplicates('state').set_index('state').population
    d['base_population'] = d.state.map(initial)
    return d


def fit(d, outcome='admin', weight=False, trends=False, difference=False):
    d = d.dropna(subset=[outcome, 'log_population']).copy()
    if not difference:
        d = d.loc[d[outcome].gt(0)]
    y = d[outcome].to_numpy() if difference else np.log(d[outcome].to_numpy())
    terms = [np.ones((len(d), 1)), d[['log_population']].to_numpy()]
    if not difference:
        state = pd.get_dummies(d.state, drop_first=True, dtype=float).to_numpy()
        terms += [state, pd.get_dummies(d.year, drop_first=True, dtype=float).to_numpy()]
        if trends:
            terms.append(state * (d.year.to_numpy() - d.year.mean())[:, None])
    x = np.column_stack(terms)
    weights = d.base_population.to_numpy() if weight else np.ones(len(d))
    root = np.sqrt(weights / weights.mean())
    xw, yw = x * root[:, None], y * root
    b, _, rank, _ = np.linalg.lstsq(xw, yw, rcond=None)
    if rank != x.shape[1] or len(d) <= rank:
        raise ValueError('Rank-deficient or saturated specification')
    residual = yw - xw @ b
    inverse = np.linalg.pinv(xw)
    bread = inverse @ inverse.T
    scores = pd.DataFrame(xw * residual[:, None]).groupby(d.state.to_numpy()).sum().to_numpy()
    n, k, g = len(d), rank, len(scores)
    covariance = bread @ (scores.T @ scores) @ bread * (g / (g-1)) * ((n-1)/(n-k))
    se = float(np.sqrt(max(covariance[1, 1], 0)))
    return {'beta': float(b[1]), 'se_CR1': se, 'low95_normal': float(b[1]-1.96*se),
            'high95_normal': float(b[1]+1.96*se), 'n': n, 'states': g,
            'years': ','.join(map(str, sorted(d.year.unique()))), 'weighted': weight}


def estimates(d):
    results = []
    samples = {
        'full': d,
        'census_waves': d.loc[d.year.isin([2012, 2017, 2022])],
        'pre2020': d.loc[d.year.lt(2020)],
        'exclude2020_22': d.loc[~d.year.between(2020, 2022)],
    }
    for label, sample in samples.items():
        for weighted in [False, True]:
            results.append(dict(spec=label, level=1, outcome='admin', **fit(sample.query('level == 1'), weight=weighted)))
    results.append(dict(spec='state_trends', level=1, outcome='admin', **fit(d.query('level == 1'), trends=True)))
    for level in [1, 2, 3]:
        for outcome in ['admin', 'central', *CODES]:
            if level == 1 and outcome == 'admin':
                continue
            results.append(dict(spec='function_level', level=level, outcome=outcome, **fit(d.query('level == @level'), outcome=outcome)))
    for start, end in [(2012, 2017), (2017, 2022), (2012, 2022)]:
        x = d.query('level == 1 and year == @start').set_index('state')
        y = d.query('level == 1 and year == @end').set_index('state')
        pair = x[['admin', 'population', 'base_population']].join(y[['admin', 'population']], lsuffix='_start', rsuffix='_end').dropna()
        pair = pair.assign(admin=np.log(pair.admin_end/pair.admin_start), log_population=np.log(pair.population_end/pair.population_start), year=end).reset_index()
        for weighted in [False, True]:
            results.append(dict(spec=f'LD_{start}_{end}', level=1, outcome='admin', **fit(pair, weight=weighted, difference=True)))
    loo = []
    for state in sorted(d.state.unique()):
        loo.append(dict(dropped_state=int(state), **fit(d.query('level == 1 and state != @state'))))
    return pd.DataFrame(results), pd.DataFrame(loo)


def main():
    OUT.mkdir(exist_ok=True)
    raw = read_finance()
    checks = validate(raw)
    d = panel(raw)
    results, loo = estimates(d)
    raw.to_csv(OUT/'selected_finance.csv', index=False)
    d.to_csv(OUT/'panel.csv', index=False)
    results.to_csv(OUT/'estimates.csv', index=False)
    loo.to_csv(OUT/'leave_one_state_out.csv', index=False)
    coverage = d.groupby('level')[['admin', 'central', *CODES]].count().to_dict()
    audit = {'input_sha256': HASHES, 'checks': checks, 'coverage': coverage,
             'missing_population_year_excluded': 2020, 'CI': 'normal approximation, state clustered CR1; excludes survey measurement uncertainty',
             'interpretation': 'descriptive; no identified fixed share or federal response'}
    (OUT/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(results.query("level == 1 and outcome == 'admin'").to_string(index=False))
    print('Leave-one-state-out beta range:', loo.beta.min(), loo.beta.max())
    print('Coverage:', coverage)


if __name__ == '__main__':
    main()
