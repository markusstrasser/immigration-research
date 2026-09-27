#!/usr/bin/env python3
"""Frozen component-share prediction. Native-First: pandas official ZIPs + NumPy SDR."""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import zipfile
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPS = [f'pwwgt{i}' for i in range(161)]
GROUPS = ['mexico_born', 'mexican_second_gen', 'mexican_third_plus_selfid', 'other']
METRICS = ['wages_own', 'wages_shared', 'federal_before_shared', 'federal_after_shared',
           'payroll_shared', 'snap_shared', 'ss_shared', 'ssi_shared']
SOURCE_FIELDS = {'wages_shared': 'WSAL_VAL', 'federal_before_shared': 'FEDTAX_BC',
                 'federal_after_shared': 'FEDTAX_AC', 'payroll_shared': 'FICA',
                 'ss_shared': 'SS_VAL', 'ssi_shared': 'SSI_VAL'}
FIELDS = ['PH_SEQ', 'PPPOS', 'A_AGE', 'A_SEX', 'PRPERTYP', 'PRCITSHP', 'PENATVTY',
          'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP', 'MARSUPWT', 'SPM_ID', 'SPM_HEAD',
          'SPM_NUMPER', 'SPM_WEIGHT', 'SPM_SNAPSUB', 'SPM_FEDTAX', 'SPM_FICA',
          'ACTC_CRD', 'EIT_CRED', 'AGI', *SOURCE_FIELDS.values()]
SPLITS = [(2022, 2024, 'primary'), (2022, 2023, 'secondary'), (2021, 2024, 'policy_stress')]
ARMS = ['population', 'frozen_share', 'group_transport', 'composition_transport']
EDGES = np.array([5000, 10000, 15000, 20000, 25000, 30000, 40000, 50000, 75000,
                  100000, 200000, 500000, 1000000, 1500000, 2000000, 5000000, 10000000])


def sha(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def se(v):
    v = np.asarray(v)
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def sources(root):
    lane = root / 'infra/immigration-fiscal'
    lock = json.loads((lane / 'same_year_tax_2026_09_20/source_lock.json').read_text())
    older = json.loads((lane / 'latam_comparison_2026_09_17/_cache/acquisition.json').read_text())
    paths = {}
    for year in [2022, 2023]:
        p = lane / f'latam_comparison_2026_09_17/_cache/{year}/asecpub{year % 100}csv.zip'
        pin = next(x['sha256'] for x in older if x['url'].endswith(p.name))
        paths[year] = (p, pin)
    paths[2024] = (lane / 'same_year_tax_2026_09_20/_cache/asecpub24csv.zip', lock['asecpub24csv.zip']['sha256'])
    paths[2025] = (root / 'sources/immigration-fiscal/data/external/stage3/census/cps_asec_2025/asecpub25csv.zip',
                   '318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b')
    return paths, lock


def group_codes(d):
    native = d.PRCITSHP.isin([1, 2, 3])
    parents_us = d.PEFNTVTY.isin([57, 60, 66, 69, 73, 78]) & d.PEMNTVTY.isin([57, 60, 66, 69, 73, 78])
    masks = [d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303),
             native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)),
             native & parents_us & d.PRDTHSP.eq(1)]
    if np.sum(masks, axis=0).max() > 1:
        raise ValueError('Overlapping generation groups')
    return np.select(masks, [0, 1, 2], 3).astype(int)


def load(year, path):
    # ASEC2022 dictionary: FEDTAX_AC also subtracts CDC_CRD and EIP_CRD.
    # Do not silently apply the post-pandemic identity to income2021.
    extra = ['CDC_CRD', 'EIP_CRD'] if year == 2022 else []
    with zipfile.ZipFile(path) as z:
        d = pd.read_csv(z.open(f'pppub{year % 100}.csv'), usecols=sorted(set(FIELDS + extra)))
        rw = pd.read_csv(z.open(f'asec_csv_repwgt_{year}.csv'), usecols=['h_seq', 'PPPOS', *REPS]).rename(columns={'h_seq': 'PH_SEQ'})
    d = d.merge(rw, on=['PH_SEQ', 'PPPOS'], how='left', validate='one_to_one')
    if d.isna().any().any():
        raise ValueError('Missing source fields or replicate weights')
    np.testing.assert_allclose(d.MARSUPWT / 100, d.pwwgt0, rtol=0, atol=.01)
    credit_audit = validate_credit_identity(d, year)
    d = d.sort_values(['SPM_ID', 'PPPOS']).reset_index(drop=True)
    units = d.groupby('SPM_ID', sort=True)
    heads = d.loc[d.SPM_HEAD.eq(1)].set_index('SPM_ID').sort_index()
    if not units.SPM_HEAD.sum().eq(1).all():
        raise ValueError('SPM head mismatch')
    if not units.size().eq(units.SPM_NUMPER.first()).all():
        raise ValueError('SPM size mismatch')
    if not units[['SPM_NUMPER', 'SPM_WEIGHT', 'SPM_SNAPSUB', 'SPM_FEDTAX', 'SPM_FICA']].nunique().eq(1).all().all():
        raise ValueError('Repeated SPM unit fields disagree')
    np.testing.assert_allclose(heads.SPM_WEIGHT / 100, heads.pwwgt0, rtol=0, atol=.01)
    np.testing.assert_array_equal(units.FEDTAX_AC.sum(), heads.SPM_FEDTAX)
    np.testing.assert_array_equal(units.FICA.sum(), heads.SPM_FICA)
    idx = pd.Categorical(d.SPM_ID, categories=heads.index).codes
    if not (idx >= 0).all():
        raise ValueError('SPM member has no unit-head index')
    if not d.A_SEX.isin([1, 2]).all():
        raise ValueError('Invalid sex code for fixed composition cells')
    pw = d[REPS].to_numpy(float)
    hw = heads[REPS].to_numpy(float)
    unit_weights = hw[idx]
    n = units.size().to_numpy(float)
    values = {'wages_own': d.WSAL_VAL.to_numpy(float)}
    source_totals = {k: units[v].sum().to_numpy(float) for k, v in SOURCE_FIELDS.items()}
    source_totals['snap_shared'] = heads.SPM_SNAPSUB.to_numpy(float)
    for metric, total in source_totals.items():
        values[metric] = (total / n)[idx]
        np.testing.assert_allclose(np.bincount(idx, weights=values[metric]), total, atol=.001)
        np.testing.assert_allclose(values[metric] @ unit_weights, total @ hw, rtol=1e-12, atol=.1)
    eligible = d.PRPERTYP.isin([1, 2]).to_numpy()
    groups = group_codes(d)
    age = np.searchsorted([25, 45, 65], d.A_AGE.to_numpy(), side='right')
    cells = groups * 8 + age * 2 + (d.A_SEX.to_numpy() - 1)
    exposure = np.zeros((2, 32, 161))
    outcome = np.zeros((len(METRICS), 32, 161))
    counts = []
    for c in range(32):
        take = eligible & (cells == c)
        counts.append(int(take.sum()))
        exposure[0, c] = pw[take].sum(axis=0)
        exposure[1, c] = unit_weights[take].sum(axis=0)
        for m, metric in enumerate(METRICS):
            w = pw if metric == 'wages_own' else unit_weights
            outcome[m, c] = values[metric][take] @ w[take]
    # Raw tax dollars already live on observed carriers; summing them once avoids
    # inventing filing-unit heads. Zero-tax records cannot affect this dollar distribution.
    agi = d.AGI.to_numpy()
    band = np.where(agi <= 0, 0, np.searchsorted(EDGES, agi, side='right') + 1)
    taxbins = np.stack([d.FEDTAX_BC.to_numpy()[band == b] @ pw[band == b] for b in range(19)])
    np.testing.assert_allclose(taxbins.sum(axis=0), d.FEDTAX_BC.to_numpy() @ pw, rtol=1e-12)
    audit = {'income_year': year - 1, 'person_rows': len(d), 'civilian_rows': int(eligible.sum()),
             'spm_units': len(heads), 'minimum_cell_n': min(counts), 'all_unit_guards': True,
             'national_own_wages_bn': float(outcome[0, :, 0].sum() / 1e9),
             'credit_identity': credit_audit}
    return exposure, outcome, np.array(counts), taxbins, audit


def validate_credit_identity(d, survey_year):
    expected = d.FEDTAX_BC - d.ACTC_CRD - d.EIT_CRED
    if survey_year == 2022:
        expected = expected - d.CDC_CRD - d.EIP_CRD
    residual = d.FEDTAX_AC - expected
    # Ten survey2022 records differ by one nominal dollar from the documented
    # identity. Preserve the released field, report the residual, reject >$1.
    # Later years retain the original exact identity guard.
    tolerance = 1 if survey_year == 2022 else 0
    np.testing.assert_allclose(d.FEDTAX_AC, expected, rtol=0, atol=tolerance)
    return {'nonzero_rows': int(residual.ne(0).sum()),
            'max_abs_nominal_dollars': int(abs(residual).max()),
            'raw_residual_dollars': float(residual.sum()),
            'released_fedtax_ac_retained': True}


def predict(train_e, train_y, test_e, arm):
    """All arrays are cell×replicate. Returns disjoint group shares."""
    te = train_e.reshape(4, 8, -1).sum(axis=1)
    ty = train_y.reshape(4, 8, -1).sum(axis=1)
    ve = test_e.reshape(4, 8, -1).sum(axis=1)
    if arm == 'population':
        totals = ve
    elif arm == 'frozen_share':
        totals = ty
    elif arm == 'group_transport':
        totals = ty / te * ve
    elif arm == 'composition_transport':
        if (train_e <= 0).any():
            raise ValueError('No training support; test outcomes must never fill a cell')
        totals = (train_y / train_e * test_e).reshape(4, 8, -1).sum(axis=1)
    else:
        raise ValueError(arm)
    if (totals.sum(axis=0) <= 0).any():
        raise ValueError('Nonpositive predicted component total')
    return totals / totals.sum(axis=0)


def score(years):
    rows, contrasts = [], []
    for train, test, split in SPLITS:
        et, yt, nt, _, _ = years[train]
        ev, yv, _, _, _ = years[test]
        for m, metric in enumerate(METRICS):
            w = int(metric != 'wages_own')
            actual_group = yv[m].reshape(4, 8, -1).sum(axis=1)
            actual = actual_group / actual_group.sum(axis=0)
            actual_union = actual[:3].sum(axis=0)
            err_by_arm, train_err_by_arm = {}, {}
            for arm in ARMS:
                if arm == 'composition_transport' and nt.min() < 20:
                    raise ValueError(f'Split {train}->{test} has unsupported training cell: {nt.min()}')
                # Test-only replication: old means fixed, later composition/outcomes replicated.
                pred = predict(et[w, :, :1], yt[m, :, :1], ev[w], arm)
                # Training-only replication: later composition/outcome fixed.
                pred_train = predict(et[w], yt[m], ev[w, :, :1], arm)
                error = 100 * (pred[:3].sum(axis=0) - actual_union)
                error_train = 100 * (pred_train[:3].sum(axis=0) - actual_union[0])
                err_by_arm[arm], train_err_by_arm[arm] = error, error_train
                rows.append({'split': split, 'train_income_year': train, 'test_income_year': test,
                             'metric': metric, 'arm': arm, 'actual_union_share_pct': 100 * actual_union[0],
                             'predicted_union_share_pct': 100 * pred[:3, 0].sum(),
                             'error_pp': error[0], 'absolute_error_pp': abs(error[0]),
                             'actual_union_share_se_pp': 100 * se(actual_union),
                             'error_test_only_se_pp': se(error), 'error_train_only_se_pp': se(error_train),
                             'error_se_cauchy_upper_pp': se(error) + se(error_train),
                             'group_total_variation_pp': 50 * np.abs(pred[:, 0] - actual[:, 0]).sum(),
                             'conditional_national_component_bn': actual_group[:, 0].sum() / 1e9,
                             'conditional_union_error_bn': error[0] / 100 * actual_group[:, 0].sum() / 1e9})
            for arm in ['group_transport', 'composition_transport']:
                gain = abs(err_by_arm['frozen_share']) - abs(err_by_arm[arm])
                gain_train = abs(train_err_by_arm['frozen_share']) - abs(train_err_by_arm[arm])
                contrasts.append({'split': split, 'metric': metric, 'arm': arm,
                                  'mae_gain_vs_frozen_pp': gain[0], 'paired_test_only_se_pp': se(gain),
                                  'paired_train_only_se_pp': se(gain_train),
                                  'paired_se_cauchy_upper_pp': se(gain) + se(gain_train)})
    return pd.DataFrame(rows), pd.DataFrame(contrasts)


def irs_diagnostic(root, lock, years):
    raw = root / 'infra/immigration-fiscal/same_year_tax_2026_09_20/_cache'
    data, hashes = {}, {}
    for year in [2022, 2023]:
        p = raw / f'{year % 100}in12ms.xls'
        hashes[str(p.relative_to(root))] = sha(p)
        if hashes[str(p.relative_to(root))] != lock[p.name]['sha256']:
            raise ValueError('IRS source drift')
        f = pd.read_excel(p, header=None)
        if not isinstance(f.iloc[0, 0], str) or f'Tax Year {year}' not in f.iloc[0, 0]:
            raise ValueError(f'IRS table does not declare Tax Year {year}')
        if not isinstance(f.iloc[3, 9], str) or 'Income tax after credits' not in f.iloc[3, 9]:
            raise ValueError('IRS table income-tax column header changed')
        bins = f.iloc[9:28, 10].to_numpy(float) * 1000
        np.testing.assert_allclose(bins.sum(), float(f.iloc[8, 10]) * 1000, rtol=1e-7)
        data[year] = bins / bins.sum()
    target = data[2023]
    cps_old = years[2022][3][:, 0]; cps_old = cps_old / cps_old.sum()
    cps_new = years[2023][3][:, 0]; cps_new = cps_new / cps_new.sum()
    rows = []
    for name, pred in [('frozen_irs_2022', data[2022]), ('frozen_cps_2022', cps_old), ('same_year_cps_2023', cps_new)]:
        for b in range(19):
            rows.append({'arm': name, 'agi_band': b, 'predicted_share_pct': 100 * pred[b],
                         'irs_2023_share_pct': 100 * target[b], 'error_pp': 100 * (pred[b] - target[b])})
    return pd.DataFrame(rows), hashes


def run(args):
    if importlib.util.find_spec('xlrd') is None:
        raise RuntimeError('[BLOCKED] IRS .xls reader absent. Run uv with --with xlrd before python3.')
    args.out.mkdir(parents=True, exist_ok=True)
    paths, lock = sources(args.source_root)
    years, hashes, audits, cells = {}, {}, [], []
    codebook = args.source_root / 'infra/immigration-fiscal/latam_comparison_2026_09_17/_cache/2022/asec2022_ddl_pub_full.pdf'
    hashes[str(codebook.relative_to(args.source_root))] = sha(codebook)
    if hashes[str(codebook.relative_to(args.source_root))] != '77622b19e77a24e8f5f6145fcb171ab856a2d438fda0ba1e04e7ce345b9f2428':
        raise ValueError('Pandemic credit-identity dictionary source drift')
    for year, (path, pin) in paths.items():
        observed = sha(path)
        if observed != pin:
            raise ValueError(f'Source hash mismatch {path.name}')
        hashes[str(path.relative_to(args.source_root))] = observed
        print(f'Loading survey{year} / income{year - 1}', flush=True)
        years[year - 1] = load(year, path)
        exposure, outcome, counts, _, audit = years[year - 1]
        audits.append(audit)
        for c in range(32):
            cells.append({'income_year': year - 1, 'group': GROUPS[c // 8], 'age_band': (c % 8) // 2,
                          'sex': c % 2 + 1, 'sample_n': counts[c], 'person_exposure': exposure[0, c, 0],
                          'spm_head_exposure': exposure[1, c, 0]})
    scores, contrasts = score(years)
    external, irshashes = irs_diagnostic(args.source_root, lock, years)
    hashes.update(irshashes)
    # Annual raw component accounts, independently reconstructed for every year.
    accounts = []
    for year, (exposure, outcome, _, _, _) in years.items():
        for m, metric in enumerate(METRICS):
            for g, group in enumerate(GROUPS):
                values = outcome[m, g * 8:(g + 1) * 8].sum(axis=0)
                accounts.append({'income_year': year, 'group': group, 'metric': metric,
                                 'amount_bn': values[0] / 1e9, 'se_bn': se(values) / 1e9})
    frames = {'scores': scores, 'paired_scores': contrasts, 'support': pd.DataFrame(cells),
              'annual_components': pd.DataFrame(accounts), 'irs_distribution': external}
    for name, frame in frames.items():
        frame.to_csv(args.out / f'{name}.csv', index=False, lineterminator='\n')
    result = {'design_sha256': sha(HERE / 'DESIGN.md'), 'script_sha256': sha(Path(__file__)),
              'source_hashes': hashes, 'survey_guards': audits,
              'output_hashes': {name: sha(args.out / f'{name}.csv') for name in frames},
              'national_scale_predicted': False, 'causal_effect_validated': False,
              'uncertainty': 'Separate SDR test and training errors; sum bounds first-order SE with unknown cross-year covariance.'}
    (args.out / 'audit.json').write_text(json.dumps(result, indent=2) + '\n')
    print(scores.groupby(['split', 'arm']).absolute_error_pp.mean().unstack().to_string())
    print(external.groupby('arm').error_pp.apply(lambda x: abs(x).sum() / 2).to_string())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--out', type=Path, default=HERE / 'derived')
    run(parser.parse_args())
