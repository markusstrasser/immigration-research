"""Bounded medical cross-survey diagnostics; no adopted model parameters change."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError('[BLOCKED] ' + message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


ACQUISITION = load_module(__name__ + '_acquisition', LANE / 'acquire.py')


def verify_mcbs_2022_pins(inputs):
    for filename, (_, expected) in ACQUISITION.FILES.items():
        require(inputs[str(LANE / '_cache' / filename)] == expected,
                f'2022 MCBS pin mismatch: {filename}')


def tail_mean(y, eligible, q=.995):
    """CMS analogue: highest unweighted 0.5%, replaced by their arithmetic mean."""
    z = y.copy()
    ix = np.flatnonzero(eligible)
    count = max(1, int(np.ceil((1 - q) * len(ix) - 1e-10)))
    selected = ix[np.argsort(y[ix], kind='stable')[-count:]]
    z[selected] = y[selected].mean()
    return z, len(selected)


@dataclass
class Stat:
    value: float
    vector: np.ndarray
    n: int = 0
    weight: float = 0


class Survey:
    def __init__(self, d, kind, design_module):
        self.d, self.kind, self.dm = d, kind, design_module
        self.w = d.weight.to_numpy(float)
        if kind == 'meps':
            self.design = design_module.Design(d.stratum.to_numpy(), d.psu.to_numpy(), self.w)
        else:
            self.W = d[['weight'] + [f'CSPUF{i:03}' for i in range(1, 101)]].to_numpy(float)
            require(np.isfinite(self.W).all() and (self.W[:, 0] > 0).all(), 'MCBS weights invalid')

    def mean(self, y, mask):
        y, mask = np.asarray(y, float), np.asarray(mask, bool)
        require(np.isfinite(y).all(), 'nonfinite medical outcome')
        require(self.w[mask].sum() > 0, 'empty or zero-weight domain')
        if self.kind == 'meps':
            e = self.dm.mean(self.design, y, self.w, mask)
            return Stat(e.value, e.T, int(mask.sum()), e.W)
        ww = self.W[mask]
        denom = ww.sum(axis=0)
        require((denom > 0).all(), 'empty BRR replicate')
        v = (ww * y[mask, None]).sum(axis=0) / denom
        return Stat(float(v[0]), v, int(mask.sum()), float(denom[0]))

    def ratio(self, a, b):
        require(b.value > 0, 'nonpositive denominator mean')
        value = a.value / b.value
        vec = ((a.vector - value * b.vector) / b.value if self.kind == 'meps'
               else a.vector / b.vector)
        return Stat(value, vec)

    def combine(self, parts):
        return Stat(sum(c * e.value for c, e in parts), sum(c * e.vector for c, e in parts))

    def se(self, e):
        variance = (self.design.var(e.vector) if self.kind == 'meps'
                    else np.sum((e.vector[1:] - e.value) ** 2) / 49)
        return float(np.sqrt(variance))


def meps_frame(pool, year=None):
    d = pool.copy() if year is None else pool[pool.year.eq(year)].copy()
    d['weight'] = d.PERWT
    d['stratum'] = d.STRA9624 if year is None else d.VARSTR
    d['psu'] = d.PSU9624 if year is None else d.VARPSU
    d['hispanic'] = d.HISPANX.eq(1)
    d['white'] = d.RACETHX.eq(2)
    d['mexican'] = d.HISPNCAT.eq(1)
    d['valid'] = d.PERWT.gt(0) & d.AGE.ge(0) & d.BORNUSA.isin([1, 2])
    d['eligible'] = d.valid & d.AGE.ge(65) & d.MCREV.eq(1)
    d['age_group'] = np.where(d.AGE.lt(75), 2, 3)
    d['medicare'] = d.TOTMCR
    d['public_common'] = d.medicare + d.medicaid
    return d.reset_index(drop=True)


def add_meps_details(d, mp):
    p = mp.paths_for(2023)
    layout = mp.parse_sas_layout(p['su.txt'])
    cols = ['DUPERSID', 'SEX', 'FAMINC23', 'MCRPHO31', 'MCRPHO42', 'MCRPHO23']
    with zipfile.ZipFile(p['dat.zip']) as z:
        names = [n for n in z.namelist() if n.lower().endswith('.dat')]
        require(len(names) == 1, 'MEPS archive does not have exactly one dat')
        raw = z.read(names[0]).decode('ascii').splitlines()
    data = {}
    for col in cols:
        start, width, char = layout[col]
        values = [s[start:start + width].strip() for s in raw]
        data[col] = values if char else np.asarray(values, float)
    x = pd.DataFrame(data)
    require(x.DUPERSID.is_unique, 'duplicate MEPS IDs in added variables')
    d = d.merge(x, on='DUPERSID', how='left', validate='one_to_one')
    require(d.SEX.notna().all() and d.SEX.isin([1, 2]).all(), 'missing/invalid joined sex')
    d['sex'] = d.SEX
    d['income_low'] = d.FAMINC23.lt(25000)
    ma = d[['MCRPHO31', 'MCRPHO42', 'MCRPHO23']]
    d['ma_proxy'] = ma.eq(1).any(axis=1)
    d['no_ma_proxy'] = ma.isin([2, 3]).all(axis=1) & ma.eq(2).any(axis=1)
    return d


def mcbs_frame(path, year):
    with zipfile.ZipFile(path) as z:
        require(z.testzip() is None, 'MCBS corrupt ZIP')
        names = [n for n in z.namelist() if n.lower().endswith('.csv')]
        require(len(names) == 1, 'MCBS archive expected one CSV')
        d = pd.read_csv(z.open(names[0]), low_memory=False).copy()
    require(d.PUF_ID.is_unique and d.SURVEYYR.eq(year).all(), 'MCBS ID/year mismatch')
    require(d.CSP_RACE.isin([1, 2, 3, 4]).all(), 'MCBS race coding changed')
    require(d.CSP_AGE.isin([1, 2, 3]).all(), 'MCBS age coding changed')
    if year == 2022:
        require(len(d) == 6621, '2022 MCBS row count differs from codebook')
        require(d.CSP_RACE.value_counts().to_dict() == {1: 4936, 2: 673, 3: 678, 4: 334},
                '2022 MCBS race counts differ from codebook')
        require(d.CSP_AGE.value_counts().to_dict() == {1: 1093, 2: 2378, 3: 3150},
                '2022 MCBS age counts differ from codebook')
    d['weight'] = d.CSPUFWGT
    d['hispanic'], d['white'] = d.CSP_RACE.eq(3), d.CSP_RACE.eq(1)
    d['eligible'] = d.CSP_AGE.isin([2, 3])
    d['age_group'], d['sex'] = d.CSP_AGE, d.CSP_SEX
    d['medicare'] = d.PAMTCARE + d.PAMTMADV
    d['medicaid'] = d.PAMTCAID
    d['public_common'] = d.medicare + d.medicaid
    d['income_low'] = d.CSP_INCOME.eq(1)
    d['ma_proxy'], d['no_ma_proxy'] = d.PAMTMADV.gt(0), d.PAMTMADV.eq(0)
    require((d[['medicare', 'medicaid']] >= 0).all().all(), 'negative public payer')
    return d


def run(root, out):
    fiscal = root / 'infra/immigration-fiscal'
    upstream = fiscal / 'medical_ethnicity_pooled_2026_09_23'
    dm = load_module('validation_design', upstream / 'design.py')
    mp = load_module('validation_pool', upstream / 'meps_pool.py')
    access = fiscal / 'fiscal_access_2026_09_20/_cache'
    paths = [upstream / '_cache/pooled.parquet', upstream / 'design.py', upstream / 'meps_pool.py',
             access / 'CSPUF2023_Data.zip', access / 'CSPUF2023_Codebook.txt',
             LANE / '_cache/CSPUF2022_Data.zip', LANE / '_cache/CSPUF2022_Codebook.txt',
             Path(__file__), LANE / 'acquire.py', LANE / 'Design.md']
    paths += list(mp.paths_for(2023).values())
    inputs = {str(p): digest(p) for p in paths}
    require(inputs[str(access / 'CSPUF2023_Data.zip')] ==
            '56937f1a623b77a85d5b401c1fdc00791098772c240073f70cbbbdff9db86d41', '2023 MCBS pin mismatch')
    verify_mcbs_2022_pins(inputs)
    pool = pd.read_parquet(paths[0])
    require(set(pool.year) == set(range(2016, 2025)), 'MEPS pool years changed')
    m23 = add_meps_details(meps_frame(pool, 2023), mp)
    sources = {'MEPS2023': Survey(m23, 'meps', dm),
               'MCBS2023': Survey(mcbs_frame(access / 'CSPUF2023_Data.zip', 2023), 'mcbs', dm),
               'MEPS2022': Survey(meps_frame(pool, 2022), 'meps', dm),
               'MCBS2022': Survey(mcbs_frame(LANE / '_cache/CSPUF2022_Data.zip', 2022), 'mcbs', dm)}
    rows, estimates, caps = [], {}, []

    def report(label, s, domain, mask, payer, y, standard=False):
        d = s.d
        stats = {}
        for g in ['hispanic', 'white']:
            gm = np.asarray(mask & d[g], bool)
            if standard:
                parts = [s.mean(y, gm & d.age_group.eq(age) & d.sex.eq(sex))
                         for age in [2, 3] for sex in [1, 2]]
                e = s.combine([(0.25, p) for p in parts])
                small = min(p.n for p in parts) < 20
            else:
                e, small = s.mean(y, gm), int(gm.sum()) < 20
            stats[g] = e
            rows.append(dict(survey=label, domain=domain, payer=payer, statistic=g,
                             value=e.value, se=s.se(e), n=int(gm.sum()),
                             weighted_n=float(s.w[gm].sum()), small_cell=small))
        ratio = s.ratio(stats['hispanic'], stats['white'])
        estimates[(label, domain, payer)] = ratio
        rows.append(dict(survey=label, domain=domain, payer=payer, statistic='ratio',
                         value=ratio.value, se=s.se(ratio), n=int((mask & (d.hispanic | d.white)).sum()),
                         weighted_n=float(s.w[np.asarray(mask & (d.hispanic | d.white))].sum()),
                         small_cell=any(r['small_cell'] for r in rows[-2:])))

    for label, s in sources.items():
        d = s.d
        for payer in ['medicare', 'medicaid', 'public_common']:
            report(label, s, 'raw_65plus_medicare_ever', d.eligible, payer, d[payer].to_numpy())
        if not label.endswith('2023'):
            continue
        for age in [2, 3]:
            for sex in [1, 2]:
                report(label, s, f'age{age}_sex{sex}', d.eligible & d.age_group.eq(age) & d.sex.eq(sex),
                       'public_common', d.public_common.to_numpy())
        report(label, s, 'uniform_age_sex', d.eligible, 'public_common', d.public_common.to_numpy(), True)
        for income in [True, False]:
            report(label, s, f'income_low_{income}_concepts_differ', d.eligible & d.income_low.eq(income),
                   'public_common', d.public_common.to_numpy())
        for ma in ['ma_proxy', 'no_ma_proxy']:
            report(label, s, ma, d.eligible & d[ma], 'public_common', d.public_common.to_numpy())
            for g in ['hispanic', 'white']:
                e = s.mean(d[ma].to_numpy(float), d.eligible & d[g])
                rows.append(dict(survey=label, domain='coverage_proxy_share', payer=ma,
                                 statistic=g, value=e.value, se=s.se(e), n=e.n,
                                 weighted_n=e.weight, small_cell=e.n < 20))
        for q in [.99, .995]:
            # Shared-rule sensitivity; caps estimated separately from each survey's eligible sample.
            public = np.zeros(len(d))
            for payer in ['medicare', 'medicaid']:
                y = d[payer].to_numpy(float)
                cap = dm.weighted_quantile(y[d.eligible], s.w[d.eligible], q)
                public += np.minimum(y, cap)
                caps.append(dict(survey=label, method='weighted_winsor', payer=payer, q=q, cap=cap))
            report(label, s, f'common_winsor_{q}', d.eligible, 'public_common', public)
        if label == 'MEPS2023':
            report(label, s, 'include_unknown_birthplace', d.weight.gt(0) & d.AGE.ge(65) & d.MCREV.eq(1),
                   'public_common', d.public_common.to_numpy())
            public = np.zeros(len(d))
            for payer in ['medicare', 'medicaid']:
                z, n = tail_mean(d[payer].to_numpy(float), np.asarray(d.valid & d.MCREV.eq(1)))
                public += z
                caps.append(dict(survey=label, method='CMS_tail_mean_analogue', payer=payer, q=.995, count=n))
            report(label, s, 'cms_tail_mean_analogue', d.eligible, 'public_common', public)

    result = pd.DataFrame(rows)
    baseline = result[result.domain.eq('raw_65plus_medicare_ever') & result.statistic.eq('ratio')]
    for lab, expected in [('MEPS2023', .845), ('MCBS2023', 1.265)]:
        got = baseline[baseline.survey.eq(lab) & baseline.payer.eq('public_common')].value.iloc[0]
        require(abs(got - expected) < .001, f'{lab} prior baseline does not reproduce')

    # Independent-survey differences. No significance screening determines which rows are retained.
    gaps = []
    for year in [2022, 2023]:
        for payer in ['medicare', 'medicaid', 'public_common']:
            a = estimates[(f'MCBS{year}', 'raw_65plus_medicare_ever', payer)]
            b = estimates[(f'MEPS{year}', 'raw_65plus_medicare_ever', payer)]
            se = np.hypot(sources[f'MCBS{year}'].se(a), sources[f'MEPS{year}'].se(b))
            gaps.append(dict(year=year, payer=payer, difference=a.value-b.value, se=se,
                             z=(a.value-b.value)/se))

    decomposition = []
    for label, s in sources.items():
        d = s.d
        white_total = s.mean(d.public_common, d.eligible & d.white)
        components = []
        for payer in ['medicare', 'medicaid']:
            h = s.mean(d[payer], d.eligible & d.hispanic)
            w = s.mean(d[payer], d.eligible & d.white)
            difference = s.combine([(1, h), (-1, w)])
            contribution = s.ratio(difference, white_total)
            components.append(contribution.value)
            decomposition.append(dict(survey=label, payer=payer,
                                      hispanic_minus_white_dollars=difference.value,
                                      dollar_difference_se=s.se(difference),
                                      excess_ratio_contribution=contribution.value,
                                      contribution_se=s.se(contribution)))
        target = estimates[(label, 'raw_65plus_medicare_ever', 'public_common')].value - 1
        require(abs(sum(components) - target) < 1e-12, 'payer decomposition does not close')

    # Retrospective holdout on one common HC-036 design retains train/test covariance.
    long = Survey(meps_frame(pool), 'meps', dm)
    d = long.d
    predictions = []
    for group, reference, eligible in [('hispanic', 'white', d.eligible),
                                      ('mexican', 'valid', d.valid & d.AGE.ge(65))]:
        for payer in ['medicare', 'medicaid', 'public_common']:
            y = d[payer].to_numpy(float) * d.defl_med.to_numpy(float)
            by_period = {}
            for period, pm in [('train_2016_2023', d.year.le(2023)), ('last_year_2023', d.year.eq(2023)),
                               ('test_2024', d.year.eq(2024))]:
                a = long.mean(y, eligible & pm & d[group])
                b = long.mean(y, eligible & pm & d[reference])
                by_period[period] = long.ratio(a, b)
            observed = by_period['test_2024']
            for period in ['train_2016_2023', 'last_year_2023']:
                predicted = by_period[period]
                err = long.combine([(1, predicted), (-1, observed)])
                predictions.append(dict(group=group, reference=reference, payer=payer,
                                        predictor=period, predicted=predicted.value, observed=observed.value,
                                        error=err.value, absolute_error=abs(err.value),
                                        error_se=long.se(err), error_z=err.value/long.se(err)))
    out.mkdir(parents=True, exist_ok=True)
    result.to_csv(out / 'diagnostics.csv', index=False, lineterminator='\n')
    pd.DataFrame(gaps).to_csv(out / 'cross_survey_gaps.csv', index=False, lineterminator='\n')
    pd.DataFrame(predictions).to_csv(out / 'retrospective_2024.csv', index=False, lineterminator='\n')
    pd.DataFrame(decomposition).to_csv(out / 'payer_decomposition.csv', index=False, lineterminator='\n')
    pd.DataFrame(caps).to_csv(out / 'tail_treatments.csv', index=False, lineterminator='\n')
    audit = {'inputs_sha256': inputs, 'surveys': {k: {'rows': len(v.d), 'weighted_n': float(v.w.sum())}
                                               for k, v in sources.items()},
             'guards': ['raw payer ratios reproduce prior 2023 results', 'MCBS2023 source SHA pinned',
                        'complete common four age-sex cells', 'no empty BRR replicate',
                        'MEPS PSU design preserves all sample PSUs and train-test overlap'],
             'limitations': ['tail cutoff uncertainty conditional', 'income concepts differ',
                             'MA payment-positive and enrollment are different proxies',
                             '2024 data previously examined; retrospective prediction only']}
    (out / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(baseline[['survey', 'payer', 'value', 'se']].to_string(index=False))
    print(pd.DataFrame(gaps).to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source-root', type=Path, default=Path('/Users/alien/Projects/immigration-research'))
    parser.add_argument('--out-dir', type=Path, default=LANE / 'derived')
    args = parser.parse_args()
    run(args.source_root, args.out_dir)
