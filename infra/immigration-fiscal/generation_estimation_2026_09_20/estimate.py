"""Age-standardized generic G4+ scenarios; no individual ancestry imputation."""
from pathlib import Path
import hashlib
import json
import sys
import zipfile

import numpy as np
import pandas as pd
import pyreadstat
from scipy.stats import t

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent/'generation_split_2026_09_20'))
sys.path.insert(0, str(HERE.parent/'norms_gen_2026_09_18'))
from analyze_cps import RAW, SHA, COLS, WEIGHTS, classify, population_masks, validate_weights
from norms_lib import Design

OUT = HERE/'derived'
GSS = HERE.parent/'attitudes_gen_2026_09_16/raw/GSS_stata/gss7224_r3a.dta'
GSS_SHA = 'a7622e03d9130e25968943b6f022f44dc0087baf0aa6b5cef150871152827344'
AGE_LABELS = ['18-24', '25-44', '45-64', '65+']
CASES = ['MAR_known_age', 'unknown_GP_lower', 'unknown_GP_upper',
         'unknown_age_outer_lower', 'unknown_age_outer_upper']


def age_bands(age):
    a = np.asarray(age, float)
    return np.select([(a >= 18)&(a < 25), (a >= 25)&(a < 45),
                      (a >= 45)&(a < 65), (a >= 65)&(a <= 120)],
                     list(range(4)), default=-1)


def ratio_influence(w, numerator, denominator):
    """Full-frame linearization, including zero outside the domain."""
    num, den = np.asarray(numerator, float), np.asarray(denominator, float)
    if np.any(num > den) or np.any(num < 0):
        raise ValueError('Numerator must be a subset of denominator')
    mass = w @ den
    if mass <= 0:
        raise ValueError('Empty donor denominator')
    p = float(w @ num / mass)
    return p, w * (num - p*den) / mass


def masks_for_case(domain, band, h, g3, g4, case):
    cell = domain & (band == h)
    unknown_age = domain & (band == -1)
    unknown_gp = ~(g3 | g4)
    if case == 'MAR_known_age':
        return cell & g4, cell & (g3 | g4)
    if case == 'unknown_GP_lower':
        return cell & g4, cell
    if case == 'unknown_GP_upper':
        return cell & (g4 | unknown_gp), cell
    if case == 'unknown_age_outer_lower':
        return cell & g4, cell | (unknown_age & (g3 | unknown_gp))
    if case == 'unknown_age_outer_upper':
        extra = unknown_age & (g4 | unknown_gp)
        return (cell & (g4 | unknown_gp)) | extra, cell | extra
    raise ValueError(case)


def domain_df(frame, mask):
    cells = frame.loc[mask, ['vstrat', 'vpsu']].drop_duplicates()
    result = len(cells) - cells.vstrat.nunique()
    if result < 1:
        raise ValueError('Insufficient domain PSU degrees of freedom')
    return int(result)


def cps_target():
    if hashlib.sha256(RAW.read_bytes()).hexdigest() != SHA:
        raise ValueError('CPS input hash changed')
    with zipfile.ZipFile(RAW) as z:
        with z.open('pppub25.csv') as f:
            d = pd.read_csv(f, usecols=COLS)
        with z.open('asec_csv_repwgt_2025.csv') as f:
            w = pd.read_csv(f, usecols=['h_seq', 'PPPOS']+WEIGHTS)
    n = len(d)
    d = d.merge(w.rename(columns={'h_seq': 'PH_SEQ'}), on=['PH_SEQ', 'PPPOS'],
                validate='one_to_one')
    if len(d) != n:
        raise ValueError('Weight join lost people')
    W = d[WEIGHTS].to_numpy(float)
    validate_weights(W)
    np.testing.assert_allclose(W[:, 0], d.MARSUPWT/100, atol=.011, rtol=0)
    base = population_masks(d)['G3plus']
    split = classify(d)
    ages = age_bands(d.A_AGE)
    adult = base & d.A_AGE.ge(18).to_numpy()
    if np.any(adult & (ages < 0)):
        raise ValueError('Unclassified target adult age')
    totals = np.array([W[adult & (ages == h)].sum(axis=0) for h in range(4)])
    children = base & d.A_AGE.lt(18).to_numpy()
    child_lo = W[children & split['G4plus_all_US_GP_observed']].sum(axis=0)
    child_hi = child_lo + W[children & split['G3plus_unresolved']].sum(axis=0)
    rows = []
    for h, label in enumerate(AGE_LABELS):
        use = adult & (ages == h)
        row = dict(ageband=label, n=int(use.sum()), people=totals[h, 0],
                   adult_share=totals[h, 0]/totals[:, 0].sum())
        for key, mask in split.items():
            row[key] = float(W[use & mask, 0].sum())
        rows.append(row)
    pd.DataFrame(rows).to_csv(OUT/'cps_age_target.csv', index=False)
    np.savez(OUT/'cps_target_replicates.npz', adult_by_age=totals,
             child_lower=child_lo, child_upper=child_hi)
    return totals, child_lo, child_hi, pd.DataFrame(rows)


def sampling_summary(point, gss_var, cps_reps, df):
    cps_var = 4/160 * np.square(cps_reps[1:]-cps_reps[0]).sum()
    se_gss, se_cps = np.sqrt(max(0., gss_var)), np.sqrt(cps_var)
    se_zero_cov = np.hypot(se_gss, se_cps)
    se_cov_upper = se_gss + se_cps
    critical = t.ppf(.975, min(df, 160))
    return dict(estimate=point, se_GSS=se_gss, se_CPS=se_cps,
                se_zero_cov=se_zero_cov, se_cov_upper=se_cov_upper,
                df_t=min(df, 160),
                ci95_cov_upper_lo=point-critical*se_cov_upper,
                ci95_cov_upper_hi=point+critical*se_cov_upper)


def main():
    OUT.mkdir(exist_ok=True)
    target, child_lo, child_hi, anchors = cps_target()
    digest = hashlib.sha256(GSS.read_bytes()).hexdigest()
    if digest != GSS_SHA:
        raise ValueError('GSS input hash changed')
    cols = ['year', 'id', 'age', 'born', 'parborn', 'hispanic', 'granborn',
            'vstrat', 'vpsu', 'wtssnrps', 'wtssps']
    data, metadata = pyreadstat.read_dta(GSS, usecols=cols, encoding='latin1')
    assert metadata.variable_value_labels['hispanic'][2] == 'mexican, mexican american, chicano/a'
    assert metadata.variable_value_labels['born'][1] == 'yes'
    assert metadata.variable_value_labels['parborn'][0] == 'both born in the u.s.'
    assert metadata.variable_value_labels['granborn'][0] == 'none'
    data = data.apply(pd.to_numeric, errors='coerce')
    if data.duplicated(['year', 'id']).any():
        raise ValueError('Repeated GSS respondent ID within survey year')
    results, cell_rows, missing_rows, audits = [], [], [], []
    for start, excluded_year in [(2016, 0), (2021, 0), (2016, 2021)]:
        keep_year = data.year.between(start, 2024) & data.year.ne(excluded_year)
        d = data[keep_year].reset_index(drop=True).copy()
        domain = (d.hispanic.eq(2)&d.born.eq(1)&d.parborn.eq(0)).to_numpy()
        band = age_bands(d.age)
        g3, g4 = d.granborn.isin([1, 2, 3, 4]).to_numpy(), d.granborn.eq(0).to_numpy()
        unknown_gp = ~(g3 | g4)
        for weight in ['wtssnrps', 'wtssps']:
            for pool in ['survey_mass', 'equal_year']:
                w = d[weight].to_numpy().copy()
                if not np.isfinite(w).all() or np.any(w <= 0):
                    raise ValueError('Missing or nonpositive GSS weight')
                if pool == 'equal_year':
                    # Normalize the full survey before selecting the Mexican domain.
                    w /= d.groupby('year')[weight].transform('sum').to_numpy()
                d['w'] = w
                design = Design(d)
                tag = dict(start=start, end=2024, excluded_year=excluded_year,
                           weight=weight, pooling=pool)
                missing_rows.append(dict(**tag, domain_n=int(domain.sum()),
                    missing_age_n=int((domain & (band < 0)).sum()),
                    missing_age_share=float(w[domain & (band < 0)].sum()/w[domain].sum()),
                    unknown_GP_share=float(w[domain & unknown_gp].sum()/w[domain].sum())))
                audits.append(dict(**tag, full_n=len(d), domain_n=int(domain.sum()),
                    strata=design.n_strata, psus=design.n_psu,
                    fullframe_df=design.n_psu-design.n_strata,
                    known_age_domain_df=domain_df(d, domain & (band >= 0)),
                    all_age_domain_df=domain_df(d, domain)))
                for case in CASES:
                    p, influences = [], []
                    active = np.zeros(len(d), bool)
                    for h, label in enumerate(AGE_LABELS):
                        num, den = masks_for_case(domain, band, h, g3, g4, case)
                        ph, ih = ratio_influence(w, num, den)
                        p.append(ph); influences.append(ih); active |= den
                        support = d.loc[den, ['vstrat', 'vpsu']].drop_duplicates()
                        cell_rows.append(dict(**tag, case=case, ageband=label,
                            denominator_n=int(den.sum()), numerator_n=int(num.sum()),
                            kish_n=float(w[den].sum()**2/np.square(w[den]).sum()),
                            domain_psus=len(support), fraction_G4plus=ph))
                    p = np.asarray(p)
                    influence = np.column_stack(influences)
                    cov = design.cov(influence)
                    df = domain_df(d, active)
                    point_count = float(p @ target[:, 0])
                    count_reps = p @ target
                    point_share = point_count/target[:, 0].sum()
                    share_reps = count_reps/target.sum(axis=0)
                    count_var = target[:, 0] @ cov @ target[:, 0]
                    age_share = target[:, 0]/target[:, 0].sum()
                    share_var = age_share @ cov @ age_share
                    for metric, point, var, reps in [
                        ('adult_G4plus_people', point_count, count_var, count_reps),
                        ('adult_G4plus_share', point_share, share_var, share_reps)]:
                        results.append(dict(**tag, case=case, metric=metric,
                            **sampling_summary(point, var, reps, df)))
                    # Compatibility is checked and reported; no clipping to observations.
                    below = p*target[:, 0] < anchors.G4plus_all_US_GP_observed.to_numpy()
                    above = p*target[:, 0] > (target[:, 0]-anchors.G3_Mexico_GP_observed.to_numpy())
                    if below.any() or above.any():
                        audits.append(dict(**tag, case=case, anchor_conflict_agebands=
                            [AGE_LABELS[h] for h in np.flatnonzero(below | above)]))
                    if case in ['unknown_age_outer_lower', 'unknown_age_outer_upper']:
                        child = child_lo if case.endswith('lower') else child_hi
                        results.append(dict(**tag, case=case, metric='all_age_G4plus_people',
                            **sampling_summary(point_count+child[0], count_var,
                                               count_reps+child, df)))
    res = pd.DataFrame(results)
    res.to_csv(OUT/'standardized_scenarios.csv', index=False)
    pd.DataFrame(cell_rows).to_csv(OUT/'donor_cells.csv', index=False)
    pd.DataFrame(missing_rows).to_csv(OUT/'missingness.csv', index=False)
    manifest = dict(GSS_source=str(GSS), GSS_sha256=digest,
        CPS_source=str(RAW), CPS_sha256=SHA,
        adult_target_people=float(target[:, 0].sum()),
        child_observed_G4plus=float(child_lo[0]), child_possible_G4plus=float(child_hi[0]),
        design_engine='norms_gen_2026_09_18/norms_lib.py:Design',
        design_engine_sha256=hashlib.sha256((HERE.parent/'norms_gen_2026_09_18/norms_lib.py').read_bytes()).hexdigest(),
        variance='Full-frame WR GSS linearization; CPS4/160 SDR; source SE sum for unknown covariance.',
        df='Korn-Graubard domain occupied PSU minus strata, capped at160 for CPS contribution.',
        limitations=['Conditional source-period/frame transport within age',
                     'Generic immigrant generations; GP countries absent',
                     'Central scenario assumes unknown GP and missing age are ignorable within age',
                     'Outer missing-age endpoints are conservative and not sharp',
                     'Sampling intervals exclude transport and identity/coverage errors'],
        design_audits=audits)
    (OUT/'audit.json').write_text(json.dumps(manifest, indent=2)+'\n')
    focus = res[(res.weight=='wtssnrps') & (res.pooling=='survey_mass')]
    print(focus[['start','excluded_year','case','metric','estimate','ci95_cov_upper_lo','ci95_cov_upper_hi']].to_string(index=False))


if __name__ == '__main__':
    main()
