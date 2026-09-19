"""Supported MEPS healthcare donor sensitivities, with full-design covariance.

Native-First: reuse the canonical CPS/MEPS parsers and annual calibration ratios.
Detailed origin is a CPS target label, never an observed MEPS spending stratum.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
DEFAULT_ROOT = Path('/Users/alien/Projects/immigration-research')
EDUCATIONS = ['lt_hs', 'hs_only', 'some_college', 'ba_plus']
OUTCOMES = ['raw', 'calibrated']
MIN_N, MIN_ESS = 30, 20.0
ORIGIN_CODES = {
    'mexico_born': [303],
    'other_central_america': list(range(310, 317)),
    'caribbean': [321, 323, 324, 327, 328, 329, 330, 332, 333, 338, 339, 340, 341, 343],
    'south_america': [360, 361, 362, 363, 364, 365, 368, 369, 370, 372, 373, 374],
    'southeast_asia': [205, 206, 211, 223, 226, 233, 236, 242, 247],
}
AGE_BANDS = [(25, 34), (35, 44), (45, 54), (55, 64), (65, 74), (75, 120)]


def full_design_covariance(data: pd.DataFrame, influence: np.ndarray) -> np.ndarray:
    """WR stratified-PSU Taylor covariance retaining every positive-weight PSU.

    Each influence row corresponds to the SAME row of the complete MEPS frame.
    Set influences outside the analytical domain to zero; never subset the design.
    """
    influence = np.asarray(influence, dtype=float)
    if influence.ndim != 2 or len(influence) != len(data) or not np.isfinite(influence).all():
        raise ValueError('Expected finite full-frame influence matrix')
    positive = data.PERWT24F.gt(0)
    design = data.loc[positive, ['VARSTR', 'VARPSU']].drop_duplicates()
    if design.isna().any().any() or (design <= 0).any().any():
        raise ValueError('Missing or invalid MEPS design variables')
    if np.any(influence[~positive.to_numpy()] != 0):
        raise ValueError('Zero-weight records must have zero influence')
    linear = pd.DataFrame(influence)
    linear['stratum'] = data.VARSTR.to_numpy()
    linear['psu'] = data.VARPSU.to_numpy()
    psus = linear.groupby(['stratum', 'psu']).sum().reindex(
        pd.MultiIndex.from_frame(design)).fillna(0)
    covariance = np.zeros((influence.shape[1], influence.shape[1]))
    for _, block in psus.groupby(level=0):
        count = len(block)
        if count < 2:
            raise ValueError('Lonely PSU in FULL MEPS design; no variance fallback')
        values = block.to_numpy()
        centered = values - values.mean(axis=0)
        covariance += count / (count - 1) * centered.T @ centered
    return covariance


def domain_means_covariance(data: pd.DataFrame, keys: list[str], outcomes: pd.DataFrame,
                            valid=None) -> dict:
    """Joint domain means/covariance for multiple correlated medical outcomes.

    Return cells, means (cell x outcome), covariance, influence, outcomes, keys.
    Covariance/influence order is CELL-MAJOR: cell0/raw, cell0/calibrated,
    cell1/raw, cell1/calibrated, ... . `means.reshape(-1)` has this order.
    The donor frame MUST retain all positive-weight survey records, even when
    `valid` restricts an adult, birth, education, or insurance analytical domain.
    """
    if len(data) != len(outcomes) or not np.isfinite(outcomes.to_numpy()).all():
        raise ValueError('Outcomes must be finite and aligned to the full donor frame')
    use = data.PERWT24F.gt(0).to_numpy(copy=True)
    if valid is not None:
        use &= np.asarray(valid, dtype=bool)
    if data.loc[use, keys].isna().any().any():
        raise ValueError('Missing donor key in declared domain')
    sample = data.loc[use]
    cells = sample.groupby(keys, sort=True).agg(
        n=('PERWT24F', 'size'), population=('PERWT24F', 'sum'))
    if cells.empty:
        raise ValueError('No donor domains')
    weight_sq = sample.assign(weight_sq=sample.PERWT24F ** 2).groupby(keys).weight_sq.sum()
    cells['effective_n'] = cells.population ** 2 / weight_sq
    cells['psus'] = sample.groupby(keys).apply(
        lambda x: len(x[['VARSTR', 'VARPSU']].drop_duplicates()), include_groups=False)
    cells['strata'] = sample.groupby(keys).VARSTR.nunique()
    cells['supported'] = (cells.n >= MIN_N) & (cells.effective_n >= MIN_ESS) & (cells.psus >= 2)
    means = np.zeros((len(cells), len(outcomes.columns)))
    influence = np.zeros((len(data), means.size))
    y = outcomes.to_numpy(dtype=float)
    weight = data.PERWT24F.to_numpy(dtype=float)
    for j, (key, cell) in enumerate(cells.iterrows()):
        key = key if isinstance(key, tuple) else (key,)
        mask = use.copy()
        for name, value in zip(keys, key):
            mask &= data[name].eq(value).to_numpy()
        means[j] = weight[mask] @ y[mask] / cell.population
        influence[mask, j * y.shape[1]:(j + 1) * y.shape[1]] = (
            weight[mask, None] * (y[mask] - means[j]) / cell.population)
    covariance = full_design_covariance(data, influence)
    cells = cells.reset_index()
    for k, name in enumerate(outcomes.columns):
        cells[f'mean_{name}'] = means[:, k]
        cells[f'se_{name}'] = np.sqrt(np.maximum(np.diag(covariance)[k::y.shape[1]], 0))
        cells[f'rse_{name}'] = np.divide(cells[f'se_{name}'], np.abs(means[:, k]),
            out=np.full(len(cells), np.nan), where=means[:, k] != 0)
    return dict(cells=cells, means=means, covariance=covariance, influence=influence,
                outcomes=list(outcomes.columns), keys=keys)


def cps_education(values) -> np.ndarray:
    v = np.asarray(values)
    return np.select([(v >= 31) & (v <= 38), v == 39, (v >= 40) & (v <= 42),
                      (v >= 43) & (v <= 46)], EDUCATIONS, default='unknown')


def meps_education(degree, years) -> np.ndarray:
    """Conservative crosswalk; 'other degree' and missing attainment stay unknown.

    MEPS HIDEG is degree, not years: GED counts as HS even with <12 years;
    grade12/no diploma stays below HS. Some college uses EDUCYR, as HIDEG alone
    codes many attendees as high-school graduates. HIDEG7 is ambiguous and excluded.
    """
    degree, years = np.asarray(degree), np.asarray(years)
    known_years = (years >= 0) & (years <= 17)
    low_years = known_years & (years <= 12)
    return np.select([
        np.isin(degree, [4, 5, 6]), (degree == 1) & low_years,
        np.isin(degree, [2, 3]) & low_years,
        np.isin(degree, [1, 2, 3]) & known_years & (years > 12)],
        ['ba_plus', 'lt_hs', 'hs_only', 'some_college'], default='unknown')


def sha256(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def load_inputs(root: Path):
    fiscal = root / 'infra/immigration-fiscal'
    for lane in ['build', 'ledger_absolute_2026_09_17']:
        sys.path.insert(0, str(fiscal / lane))
    import meps_health_transport_2024 as donor
    import absolute_ledger as annual
    base = annual.ext.base
    if 'A_HGA' not in base.PERSON:
        base.PERSON.append('A_HGA')
    raw = root / 'sources/immigration-fiscal/data/external/stage3'
    cps_zip = raw / 'census/cps_asec_2025/asecpub25csv.zip'
    meps_zip = raw / 'ahrq/meps_2024/h256dat.zip'
    sas = meps_zip.with_name('h256su.txt')
    params_path = fiscal / 'ledger_absolute_2026_09_17/params/params.json'
    print('[read] CPS and replicate weights', flush=True)
    cps, _, _, checks = base.prepare(cps_zip)
    for field in ['HIDEG', 'EDUCYR']:
        if field not in donor.FIELDS:
            donor.FIELDS.append(field)
    print('[read] MEPS full person frame', flush=True)
    meps, anchors = donor.read_meps(meps_zip, sas)
    params = annual.Params(params_path, False)
    rmcd = params.nhea_over_meps('meps_coverage', [['ratio', 'medicaid']], 'medicaid',
                                preferred='nhea_to_meps_ratio_medicaid')
    rmcr = params.nhea_over_meps('meps_coverage', [['ratio', 'medicare']], 'medicare',
                                preferred='nhea_to_meps_ratio_medicare')
    if rmcd is None or rmcr is None or not np.isfinite([rmcd, rmcr]).all():
        raise ValueError('Verified Medicaid/Medicare calibration ratios missing')
    meps['education'] = meps_education(meps.HIDEG, meps.EDUCYR)
    cps = pd.concat([cps, pd.DataFrame({
        'education': cps_education(cps.A_HGA), 'age_band': donor.age_band(cps.A_AGE),
        'born': np.where(cps.PENATVTY.eq(57), 1, 2),
        'insurance': donor.cps_insurance_category(cps),
        'exposure': ~(cps.PUB.eq(0) & cps.PRIV.eq(0))}, index=cps.index)], axis=1)
    if cps.loc[~cps.exposure, 'A_AGE'].gt(0).any():
        raise ValueError('Unexpected noninfant without reference-year exposure')
    outcomes = pd.DataFrame({'raw': meps.public_paid,
        'calibrated': meps.public_paid + (rmcd - 1) * meps.TOTMCD24 + (rmcr - 1) * meps.TOTMCR24})
    sources = [cps_zip, meps_zip, sas, params_path, Path(__file__), Path(donor.__file__),
               Path(base.__file__), Path(annual.__file__),
               meps_zip.with_name('h256doc.pdf'), meps_zip.with_name('h256cb.pdf'),
               cps_zip.with_name('asec2025_ddl_pub_full.pdf')]
    return cps, meps, outcomes, donor, dict(
        inputs=[dict(path=str(p), sha256=sha256(p)) for p in sources],
        cps_checks=checks, meps_population_anchors=anchors,
        ratios=dict(medicaid=rmcd, medicare=rmcr), params_used=params.used)


def fit_models(meps, cps, outcomes, donor):
    valid = meps.PERWT24F.gt(0) & meps.AGE24X.ge(0) & meps.BORNUSA.isin([1, 2])
    adult = valid & meps.AGE24X.ge(25)
    specs = {
        'canonical': (['age_band', 'born'], valid),
        'adult_age_birth': (['age_band', 'born'], adult),
        'education': (['age_band', 'born', 'education'], adult & meps.education.ne('unknown')),
        'insurance': (['age_band', 'born', 'insurance'], valid),
    }
    models, offset, parts, index_rows = {}, 0, [], []
    for name, (keys, mask) in specs.items():
        fit = domain_means_covariance(meps, keys, outcomes, mask)
        fit['offset'] = offset
        fit['codes'] = pd.MultiIndex.from_frame(fit['cells'][keys]).get_indexer(
            pd.MultiIndex.from_frame(cps[keys]))
        models[name] = fit
        parts.append(fit['influence'])
        for cell, row in fit['cells'].iterrows():
            for k, outcome in enumerate(outcomes.columns):
                index_rows.append(dict(j=offset + cell * len(outcomes.columns) + k,
                    model=name, cell=cell, outcome=outcome,
                    **{key: row[key] for key in keys}))
        offset += fit['means'].size
    joint = full_design_covariance(meps, np.column_stack(parts))
    # Reproduce the current canonical donor mean AND covariance before extension.
    old_cells, old_codes, old_cov = donor.donor_model(meps, cps, False)
    canon = models['canonical']
    if not np.array_equal(old_codes, canon['codes']) or not np.allclose(
        old_cells.mean_public_paid, canon['means'][:, 0], rtol=1e-12, atol=1e-9):
        raise ValueError('Canonical means or CPS donor assignments drifted')
    if not np.allclose(old_cov, canon['covariance'][0::2, 0::2], rtol=1e-10, atol=1e-7):
        raise ValueError('Canonical full-design covariance drifted')
    return models, joint, pd.DataFrame(index_rows)


def assignments(models, cps):
    """Return direct model and explicit supported-cell backoff assignments.

    Rich estimates over unsupported cells are NOT treated as supported. Mixed
    predictions are named backoff scenarios and record the affected CPS mass.
    """
    adult = cps.A_AGE.ge(25).to_numpy()
    output = {}
    for name, fit in models.items():
        codes = fit['codes']
        supported = codes >= 0
        supported &= fit['cells'].supported.to_numpy()[np.maximum(codes, 0)]
        js = np.where(codes >= 0, fit['offset'] + 2 * codes, -1)
        output[name] = dict(j=js, supported=supported, used_rich=supported)
    for rich, base in [('education', 'adult_age_birth'), ('insurance', 'canonical')]:
        use_rich = output[rich]['supported']
        j = np.where(use_rich, output[rich]['j'], output[base]['j'])
        if (j[adult] < 0).any():
            raise ValueError(f'Explicit {rich} backoff is unsupported for adult CPS records')
        output[rich + '_backoff'] = dict(j=j, supported=np.ones(len(cps), bool), used_rich=use_rich)
    return output


def target_masks(cps):
    foreign = cps.PRCITSHP.isin([4, 5])
    native = cps.PRCITSHP.isin([1, 2, 3])
    origins = {name: (foreign & cps.PENATVTY.isin(codes)).to_numpy()
               for name, codes in ORIGIN_CODES.items()}
    origins['all_native'] = native.to_numpy()
    us = [57, 60, 66, 69, 73, 78]
    origins['third_plus_nh_white'] = (native & cps.PEFNTVTY.isin(us) & cps.PEMNTVTY.isin(us)
                                     & cps.PEHSPNON.eq(2) & cps.PRDTRACE.eq(1)).to_numpy()
    ages = {'25_64': cps.A_AGE.between(25, 64).to_numpy()}
    ages.update({str(i): cps.A_AGE.between(lo, hi).to_numpy()
                 for i, (lo, hi) in enumerate(AGE_BANDS)})
    civilian = cps.PRPERTYP.eq(2).to_numpy()
    for origin, om in origins.items():
        for education in EDUCATIONS + ['all']:
            em = np.ones(len(cps), bool) if education == 'all' else cps.education.eq(education).to_numpy()
            for band, am in ages.items():
                yield (origin, education, band), civilian & om & em & am


def exposures(j, mask, weights, exposure, size):
    if (j[mask] < 0).any():
        raise ValueError('Unassigned donor included in estimate')
    result = np.zeros((size, weights.shape[1]))
    np.add.at(result, j[mask], weights[mask] * exposure[mask, None])
    return result


def joint_summary(replicates, gradient, covariance):
    cps_variance = 4 / 160 * np.square(replicates[1:] - replicates[0]).sum()
    meps_variance = float(gradient @ covariance @ gradient)
    if meps_variance < -1e-5:
        raise ValueError('Negative medical variance')
    return dict(estimate=float(replicates[0]), se_cps=float(np.sqrt(cps_variance)),
                se_meps=float(np.sqrt(max(0, meps_variance))),
                se_joint=float(np.sqrt(cps_variance + max(0, meps_variance))))


def estimate_targets(cps, models, covariance, index):
    assignments_by_model = assignments(models, cps)
    theta = np.concatenate([m['means'].reshape(-1) for m in models.values()])
    weights = cps[[f'pwwgt{i}' for i in range(161)]].to_numpy(dtype=float)
    exposure = cps.exposure.to_numpy(dtype=float)
    rows, support_rows, gradients, replicates = [], [], [], []
    for (origin, education, band), target in target_masks(cps):
        target_pop = float(weights[target, 0].sum())
        if not target.any() or target_pop <= 0:
            support_rows.append(dict(origin=origin, education=education, band=band,
                model='all', records=0, population=0, unsupported_population=0,
                unsupported_fraction=np.nan, status='empty_target_domain'))
            continue
        for model, assignment in assignments_by_model.items():
            is_backoff = model.endswith('_backoff')
            source_supported = assignment['used_rich']
            unsupported_pop = float(weights[target & ~source_supported, 0].sum())
            support_rows.append(dict(origin=origin, education=education, band=band,
                model=model, records=int(target.sum()), population=target_pop,
                unsupported_population=unsupported_pop, unsupported_fraction=unsupported_pop / target_pop,
                status='explicit_backoff' if is_backoff else 'direct_matching'))
            mask = target.copy()
            scope = 'all'
            if model in ['education', 'insurance']:
                mask &= assignment['supported']
                scope = 'supported'
            elif (assignment['j'][mask] < 0).any():
                raise ValueError(f'Base model cannot match adult target: {model}')
            if not mask.any():
                continue
            pop = weights[mask].sum(axis=0)
            if (pop <= 0).any():
                support_rows[-1]['status'] += ';nonpositive_replicate_population'
                continue
            e = exposures(assignment['j'], mask, weights, exposure, len(theta))
            e_canonical = exposures(assignments_by_model['canonical']['j'], mask, weights,
                                   exposure, len(theta))
            e_adult = exposures(assignments_by_model['adult_age_birth']['j'], mask, weights,
                               exposure, len(theta))
            for k, outcome in enumerate(OUTCOMES):
                ek, ec, ea = (np.roll(x, k, axis=0) for x in (e, e_canonical, e_adult))
                reps = theta @ ek / pop
                gradient = ek[:, 0] / pop[0]
                summary = joint_summary(reps, gradient, covariance)
                canonical_delta = joint_summary(theta @ (ek - ec) / pop,
                                                 (ek[:, 0] - ec[:, 0]) / pop[0], covariance)
                adult_delta = joint_summary(theta @ (ek - ea) / pop,
                                             (ek[:, 0] - ea[:, 0]) / pop[0], covariance)
                row = dict(row=len(rows), origin=origin, education=education, band=band,
                    model=model, scope=scope, outcome=outcome, records=int(mask.sum()),
                    population=float(pop[0]), target_population=target_pop,
                    supported_target_fraction=(target_pop - unsupported_pop) / target_pop,
                    dollars_total=float(theta @ ek[:, 0]),
                    dollars_per_person=summary.pop('estimate'), **summary,
                    delta_vs_canonical=canonical_delta.pop('estimate'),
                    **{f'delta_canonical_{n}': v for n, v in canonical_delta.items()},
                    delta_vs_adult_age_birth=adult_delta.pop('estimate'),
                    **{f'delta_adult_{n}': v for n, v in adult_delta.items()})
                rows.append(row)
                gradients.append(gradient)
                replicates.append(reps)
    return pd.DataFrame(rows), pd.DataFrame(support_rows), np.asarray(gradients), np.asarray(replicates)


def native_contrasts(estimates, gradients, replicates, covariance):
    keys = ['education', 'band', 'model', 'scope', 'outcome']
    rows = []
    for reference in ['all_native', 'third_plus_nh_white']:
        lookup = {tuple(row[k] for k in keys): int(row['row'])
                  for row in estimates[estimates.origin.eq(reference)].to_dict('records')}
        for row in estimates.to_dict('records'):
            j = lookup.get(tuple(row[k] for k in keys))
            if j is None:
                continue
            i = int(row['row'])
            summary = joint_summary(replicates[i] - replicates[j], gradients[i] - gradients[j], covariance)
            rows.append(dict(origin=row['origin'], reference=reference,
                **{k: row[k] for k in keys}, cost_difference_per_person=summary.pop('estimate'),
                **summary, target_population=row['population'],
                reference_population=float(estimates.iloc[j].population)))
    return pd.DataFrame(rows)


def age_deltas(estimates, gradients, replicates, covariance):
    """Aligned healthcare COST differences for correlated age/lifetime sums."""
    keys = ['origin', 'education', 'band', 'outcome']
    rows, delta_gradients, delta_replicates = [], [], []
    for model, baseline in [('education_backoff', 'canonical'),
                            ('education_backoff', 'adult_age_birth'),
                            ('insurance_backoff', 'canonical')]:
        lookup = {tuple(r[k] for k in keys): r for r in estimates[
            estimates.model.eq(baseline) & estimates.scope.eq('all')].to_dict('records')}
        current = estimates[estimates.model.eq(model) & estimates.band.ne('25_64')]
        for row in current.to_dict('records'):
            reference = lookup[tuple(row[k] for k in keys)]
            if row['records'] != reference['records'] or not np.isclose(
                    row['population'], reference['population'], rtol=1e-12, atol=1e-6):
                raise ValueError('Age sensitivity comparison changed the CPS domain')
            i, j = int(row['row']), int(reference['row'])
            dg, dr = gradients[i] - gradients[j], replicates[i] - replicates[j]
            summary = joint_summary(dr, dg, covariance)
            rows.append(dict(row=len(rows), estimate_row=i, baseline_row=j,
                model=model, baseline=baseline, **{k: row[k] for k in keys},
                population=row['population'], records=row['records'],
                medical_cost_delta_per_person=summary.pop('estimate'), **summary))
            delta_gradients.append(dg)
            delta_replicates.append(dr)
    return pd.DataFrame(rows), np.asarray(delta_gradients), np.asarray(delta_replicates)


def generate(root: Path, out: Path):
    cps, meps, outcomes, donor, audit = load_inputs(root)
    print('[fit] four donor specifications; full-design joint covariance', flush=True)
    models, covariance, index = fit_models(meps, cps, outcomes, donor)
    print('[estimate] origin x education x adult age domains', flush=True)
    estimates, support, gradients, replicates = estimate_targets(cps, models, covariance, index)
    contrasts = native_contrasts(estimates, gradients, replicates, covariance)
    deltas, delta_gradients, delta_replicates = age_deltas(estimates, gradients, replicates, covariance)
    theta = np.concatenate([fit['means'].reshape(-1) for fit in models.values()])
    if not np.allclose(gradients @ theta, estimates.dollars_per_person, atol=1e-6, rtol=1e-10):
        raise ValueError('Exported exposure gradients do not reconstruct medical point estimates')
    out.mkdir(parents=True, exist_ok=True)
    tables = {'estimates.csv': estimates, 'native_contrasts.csv': contrasts, 'age_deltas.csv': deltas,
              'target_support.csv': support, 'covariance_index.csv': index,
              'donor_cells.csv': pd.concat([fit['cells'].assign(model=name)
                                           for name, fit in models.items()], ignore_index=True)}
    for name, table in tables.items():
        table.to_csv(out / name, index=False)
    np.savez_compressed(out / 'medical_uncertainty.npz', covariance=covariance,
                        donor_means=theta, point_gradients=gradients,
                        cps_per_person_replicates=replicates,
                        age_delta_gradients=delta_gradients, age_delta_cps_replicates=delta_replicates)
    adult = meps.PERWT24F.gt(0) & meps.AGE24X.ge(25) & meps.BORNUSA.isin([1, 2])
    education_missing = []
    for born in [1, 2]:
        mask = adult & meps.BORNUSA.eq(born)
        population = float(meps.loc[mask, 'PERWT24F'].sum())
        unknown = mask & meps.education.eq('unknown')
        education_missing.append(dict(born=born, population=population,
            unknown_population=float(meps.loc[unknown, 'PERWT24F'].sum()),
            unknown_fraction=float(meps.loc[unknown, 'PERWT24F'].sum() / population),
            unknown_records=int(unknown.sum()), records=int(mask.sum())))
    audit.update(schema='health-transport-sensitivity-v1', price_year=2024,
        donor_support_rule=dict(minimum_unweighted_n=MIN_N, minimum_kish_effective_n=MIN_ESS,
            minimum_psus=2, rule_origin='analyst screening convention; not an AHRQ reliability standard',
            high_rse='cell raw/calibrated RSE exported; no guarantee of precise cost means'),
        education_unknown_by_birth=education_missing, origins=ORIGIN_CODES,
        age_bands={str(i): list(band) for i, band in enumerate(AGE_BANDS)},
        primary_comparison='calibrated healthcare, education_backoff versus canonical; '
            'adult_age_birth control separates donor-age-universe effect',
        accounting='Positive cost; calibrated = raw public paid + (Medicaid ratio-1)*Medicaid '
            '+ (Medicare ratio-1)*Medicare; replace raw+M jointly, never add both sensitivity deltas',
        uncertainty='Independent CPS SDR and MEPS full-design Taylor components; all matching arms '
            'and outcomes share a joint MEPS covariance; calibration multipliers treated as fixed',
        uncertainty_array_contract='row order is estimates.row; point_gradients map each per-person '
            'estimate to covariance_index.j; CPS replicate0 full weight and 1..160 SDR. Combining '
            'age rows uses these correlated arrays, never independent age SE sums. '
            'age_delta_* rows map to age_deltas.row; positive values are extra medical cost, '
            'so fiscal balance delta has the opposite sign.',
        identification='CPS origin differences in transported donor means, not observed origin-specific '
            'medical expenditures or causal immigration effects',
        limitations=['MEPS education is minimally-cleaned first-entry attainment; CPS is current attainment',
            'HIDEG other-degree/missing not classified; four-category education donors are complete cases',
            'education backoff is a stated mixed model, not observations for unsupported target cells',
            'insurance conditional matching changes the estimand and may condition on program uptake',
            '65+ insurance categories pooled as in canonical transport',
            'Kish effective n ignores clustering; design SEs are reported separately',
            'historical 2012 NHEA/MEPS multipliers transported to 2024; uncertainty not estimated'],
        canonical_reproduction=True, rows=len(estimates), full_design_positive_weight_records=int(meps.PERWT24F.gt(0).sum()),
        full_design_psus=len(meps.loc[meps.PERWT24F.gt(0), ['VARSTR', 'VARPSU']].drop_duplicates()),
        outputs={name: sha256(out / name) for name in [*tables, 'medical_uncertainty.npz']})
    (out / 'audit.json').write_text(json.dumps(audit, indent=2, default=str, allow_nan=False) + '\n')
    print(f'[written] {len(estimates)} estimates, {len(contrasts)} contrasts: {out}', flush=True)
    return estimates


def load_outputs(out: Path):
    """Reject modified inputs/artifacts before consuming the sensitivity release."""
    out = Path(out)
    audit = json.loads((out / 'audit.json').read_text())
    if audit.get('schema') != 'health-transport-sensitivity-v1':
        raise ValueError('Unsupported healthcare sensitivity schema')
    for item in audit['inputs']:
        if sha256(item['path']) != item['sha256']:
            raise ValueError(f"Stale healthcare input: {item['path']}")
    for name, expected in audit['outputs'].items():
        if sha256(out / name) != expected:
            raise ValueError(f'Stale healthcare output: {name}')
    return pd.read_csv(out / 'estimates.csv'), np.load(out / 'medical_uncertainty.npz'), audit


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=DEFAULT_ROOT)
    parser.add_argument('--out', type=Path, default=HERE / 'derived')
    args = parser.parse_args()
    generate(args.root.resolve(), args.out.resolve())


if __name__ == '__main__':
    main()
