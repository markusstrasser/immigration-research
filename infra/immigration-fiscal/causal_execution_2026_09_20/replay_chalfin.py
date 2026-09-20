"""Official Chalfin2015 data replay. Run with --data PATH --out DIR. Input SHA-256 and dimensions fail closed."""
import argparse
from pathlib import Path
import hashlib
import json
import math
import numpy as np
import pandas as pd
CRIMES = ['murder', 'rape', 'robbery', 'assault', 'burglary', 'larceny', 'motor']
OTHER = ['dfbnonmex', 'dushisp']

def design(d, covs, fe=True, year=False):
    parts = [np.ones((len(d), 1)), d[covs].to_numpy(dtype=float)]
    if fe:
        parts.append(d[FE].to_numpy(dtype=float))
    if year:
        parts.append(pd.get_dummies(d.year).to_numpy(dtype=float))
    return np.column_stack(parts)

def residual(a, c):
    return a - c @ np.linalg.lstsq(c, a, rcond=None)[0]

def clustered_score(v, g):
    return np.array([v[g == x].sum() for x in np.unique(g)])

def ar_set(y, x, z, g, cutoff=1.959963984540054):
    """Invert one-instrument cluster-robust AR Wald, asymptotic chi-square(1).
    Regress y-beta*x on controls + instrument; test instrument coefficient.
    Results are analytic roots; can be bounded, disjoint, all real, or empty.
    """
    zy, zx, zz = (z @ y, z @ x, z @ z)
    sy = clustered_score(z * (y - z * zy / zz), g)
    sx = clustered_score(z * (x - z * zx / zz), g)
    a = zx ** 2 - cutoff ** 2 * (sx @ sx)
    b = -2 * zy * zx + 2 * cutoff ** 2 * (sy @ sx)
    c = zy ** 2 - cutoff ** 2 * (sy @ sy)
    scale = max(abs(zx ** 2), abs(cutoff ** 2 * (sx @ sx)), 1.0)
    if abs(a) <= np.finfo(float).eps * 100 * scale:
        linear_scale = max(abs(2 * zy * zx), abs(2 * cutoff ** 2 * (sy @ sx)), 1.0)
        if abs(b) <= np.finfo(float).eps * 100 * linear_scale:
            return {'kind': 'all_real' if c <= 0 else 'empty', 'intervals': [[None, None]] if c <= 0 else []}
        root = float(-c / b)
        return {'kind': 'half_line', 'intervals': [[None, root]] if b > 0 else [[root, None]]}
    disc = b * b - 4 * a * c
    if disc < 0:
        result = {'kind': 'all_real' if a < 0 else 'empty', 'intervals': [[None, None]] if a < 0 else []}
    else:
        roots = sorted([(-b - math.sqrt(disc)) / (2 * a), (-b + math.sqrt(disc)) / (2 * a)])
        result = {'kind': 'bounded' if a > 0 else 'disjoint_unbounded', 'intervals': [roots] if a > 0 else [[None, roots[0]], [roots[1], None]]}
    return result

def iv(outcome, covs=None, drop=None):
    if covs is None:
        covs = COVS + OTHER
    names = [outcome, 'dmexfb_alt', 'dins', 'popweight', 'FMSA'] + covs + FE
    d = DF.dropna(subset=names)
    if drop is not None:
        d = d[d.FMSA != drop]
    w = np.sqrt(d.popweight.to_numpy())
    c = design(d, covs) * w[:, None]
    y, x, z = (residual(d[v].to_numpy() * w, c) for v in [outcome, 'dmexfb_alt', 'dins'])
    g = d.FMSA.to_numpy()
    b = z @ y / (z @ x)
    s = clustered_score(z * (y - b * x), g)
    se = np.sqrt(s @ s) / abs(z @ x)
    zg = clustered_score(z * z, g) / (z @ z)
    result = dict(outcome=outcome, n=len(d), clusters=len(np.unique(g)), controls_rank=int(np.linalg.matrix_rank(c)), beta=float(b), se_cr0=float(se), se_cluster_g=float(se * np.sqrt(len(zg) / (len(zg) - 1))), z=float(b / se), p_normal=float(math.erfc(abs(b / se) / math.sqrt(2))), ci95=[float(b - 1.959963984540054 * se), float(b + 1.959963984540054 * se)], ar95=ar_set(y, x, z, g), max_residual_instrument_energy=float(zg.max()), effective_instrument_energy_clusters=float(1 / (zg @ zg)))
    return result

def first_stage(covs, fe, year=False, excluded=None, dependent='dmexfb_alt'):
    d = DF.dropna(subset=[dependent, 'dins', 'popweight', 'FMSA'] + covs + FE)
    if excluded is not None:
        d = d[d.FMSA != excluded]
    w = np.sqrt(d.popweight.to_numpy())
    c = design(d, covs, fe, year) * w[:, None]
    x, z = (residual(d[v].to_numpy() * w, c) for v in [dependent, 'dins'])
    b = z @ x / (z @ z)
    s = clustered_score(z * (x - b * z), d.FMSA.to_numpy())
    n, g, k = (len(d), len(s), int(np.linalg.matrix_rank(c)) + 1)
    se0 = np.sqrt(s @ s) / (z @ z)
    se = se0 * np.sqrt(g / (g - 1) * (n - 1) / (n - k))
    return dict(dependent=dependent, n=n, clusters=g, rank=k, beta=float(b), se_cr0=float(se0), se_stata_small=float(se), F_stata_small=float((b / se) ** 2))

def main(argv=None):
    global ROOT, SOURCE, DF, COVS, FE
    parser = argparse.ArgumentParser(description='Replay the original Chalfin2015 command and documented sensitivities')
    parser.add_argument('--data', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    SOURCE = args.data.resolve()
    ROOT = args.out.resolve()
    actual_sha = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    if actual_sha != 'd41b4882f615cfe8063f16ee6dcd0e26f3cf43873f661529234518174d1b567d':
        raise ValueError('Unexpected input SHA-256: ' + actual_sha)
    DF = pd.read_stata(SOURCE).sort_values(['FMSA', 'year']).copy()
    if DF.shape != (276, 172) or DF.FMSA.nunique() != 92:
        raise ValueError('Unexpected official-data dimensions')
    ROOT.mkdir(parents=True, exist_ok=True)
    COVS = [x for x in DF.columns if x.startswith('deduc') or x.startswith('dage')]
    COVS += ['dblack', 'demployed', 'dusbirths']
    FE = [x for x in DF.columns if x.startswith('grp_')]
    for crime in CRIMES:
        DF['reconstructed_dlograte_' + crime] = DF.groupby('FMSA')['logpc_' + crime].diff()
    unit_checks = {}
    for crime in CRIMES:
        diff = DF.groupby('FMSA')[f'logpc_{crime}'].diff()
        unit_checks[f'{crime}_dlog_equals_diff'] = float((diff - DF[f'dlogpc_{crime}']).abs().max())
        count_diff = np.log(DF[crime].where(DF[crime] > 0)).groupby(DF.FMSA).diff()
        unit_checks[f'{crime}_dlog_equals_log_count_diff'] = float((count_diff - DF[f'dlogpc_{crime}']).abs().max())
        for denom in ['population', 'poptotal', 'popweight', 'popit']:
            ratio = (DF[crime] / DF[denom]).where(lambda x: x > 0)
            gap = (DF[f'logpc_{crime}'] - np.log(ratio)).replace([np.inf, -np.inf], np.nan).dropna()
            unit_checks[f'{crime}_log_minus_log_count_over_{denom}'] = dict(min=float(gap.min()) if len(gap) else None, max=float(gap.max()) if len(gap) else None, std=float(gap.std()) if len(gap) > 1 else None, valid_rows=len(gap))
    for mex in ['mexicanfb', 'mexicanfb_tot', 'mexfb', 'mexfba']:
        for denom in ['population', 'poptotal', 'popweight', 'popit']:
            for scale in [1, 100]:
                candidates = {'diff_share': (DF[mex] / DF[denom]).groupby(DF.FMSA).diff() * scale, 'count_change_over_lag_population': DF.groupby('FMSA')[mex].diff() / DF.groupby('FMSA')[denom].shift() * scale}
                for label, v in candidates.items():
                    err = (v - DF.dmexfb_alt).abs()
                    finite = err[np.isfinite(err)]
                    unit_checks[f'dmexfb_alt_vs_{label}_{mex}_{denom}_scale{scale}'] = float(finite.max()) if len(finite) else None
    unit_checks['dmexfb_alt_equals_100_change_mexfba'] = float((DF.groupby('FMSA').mexfba.diff() * 100 - DF.dmexfb_alt).abs().max())
    unit_checks['population_vs_poptotal_ratio'] = {k: float(v) for k, v in (DF.population / DF.poptotal).describe().items()}
    unit_checks['population_vs_poptotal_change_log_max_gap'] = float(np.log(DF.population / DF.poptotal).groupby(DF.FMSA).diff().abs().max())
    rate_sensitivity = [iv('reconstructed_dlograte_' + c) for c in CRIMES]
    baseline = [iv('dlogpc_' + c) for c in CRIMES]
    less_controlled = [iv('dlogpc_' + c, covs=[]) for c in CRIMES]
    loo = []
    for crime in CRIMES:
        for msa in DF.FMSA.unique():
            r = iv('dlogpc_' + crime, drop=msa)
            r.update(excluded_msa=int(msa), excluded_name=str(DF.loc[DF.FMSA == msa, 'FMSANAME'].iloc[0]))
            loo.append(r)
    stages = {'year_only': first_stage([], False, True), 'controls_no_FE': first_stage(COVS + OTHER, False), 'main': first_stage(COVS + OTHER, True), 'exclude_1600': first_stage(COVS + OTHER, True, excluded=1600), 'exclude_4480': first_stage(COVS + OTHER, True, excluded=4480)}
    falsification = {dep: first_stage(COVS, True, dependent=dep) for dep in ['dfbnonmex', 'dushisp', 'dmexfbk']}
    out = dict(source=str(SOURCE), sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(), covariates=COVS + OTHER, fixed_effects=FE, baseline=baseline, less_controlled_region_year_only=less_controlled, first_stages=stages, falsification=falsification, leave_one_msa_out=loo, unit_checks=unit_checks, notes=['No small-sample multiplier applied to CR0 IV; ivreghdfe embedded ivreg2 source lines1194-1205 confirms this no-small convention. G/(G-1) alternative is diagnostic only.', 'AR intervals use asymptotic clustered chi-square reference, not bootstrap; high-leverage clusters can undermine approximation.', 'Supplied dlogpc outcomes actually equal changes in log raw offense counts, not changes in contemporaneous per-capita rates.', 'dmexfb_alt equals 100 times within-MSA change in mexfba; adult-age scope not documented in supplied archive labels.', 'No causal victim cost claimed: numerator geography/reporting comparability has not been established.'], reconstructed_contemporaneous_log_rate_sensitivity=rate_sensitivity)
    (ROOT / 'chalfin_replay.json').write_text(json.dumps(out, indent=2, allow_nan=False) + '\n')
    pd.DataFrame([{k: v for k, v in r.items() if k not in ['ar95', 'ci95']} for r in baseline]).to_csv(ROOT / 'chalfin_baseline.csv', index=False)
    pd.DataFrame([{k: v for k, v in r.items() if k not in ['ar95', 'ci95']} for r in loo]).to_csv(ROOT / 'chalfin_leave_one_out.csv', index=False)
    print('Reproduced', len(baseline), 'offense models and', len(loo), 'leave-one-out estimates; outputs:', ROOT)
if __name__ == '__main__':
    main()
