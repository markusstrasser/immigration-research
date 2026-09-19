"""2023 Medicaid administrative scope check; no demographic recalibration.

Reuses the canonical MEPS fixed-width parser and age/birth transport structure.
CMS administrative eligibility categories are NEVER imputed from survey age.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
MONTHS = ['JA', 'FE', 'MA', 'AP', 'MY', 'JU', 'JL', 'AU', 'SE', 'OC', 'NO', 'DE']
NATIONAL_ROWS = [
    ('Total', 94.0, 877.2, 877.2e3 / 94.0),
    ('Children', 33.8, 136.5, 4042),
    ('Adults: Non-Expansion, Non-Disabled, Under Age 65', 16.5, 97.2, 5903),
    ('Adults: ACA Medicaid Expansion', 25.0, 199.6, 7993),
    ('Aged', 9.6, 188.4, 19674),
    ('People with Disabilities', 9.3, 255.6, 27579),
]


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def verify_sources(raw):
    pins = json.loads((HERE / 'source_pins.json').read_text())
    for item in pins['files']:
        path = raw / item['name']
        if not path.is_file() or sha(path) != item['sha256']:
            raise ValueError(f'Source absent or changed: {path}')
    return pins


def monthly_bounds(values):
    """Edited MEPS coverage: 1 yes, 2 no, -1 outside monthly universe.

    Other negative responses remain unknown, contributing only to the upper
    bound. They are never silently treated as an observed absence of coverage.
    """
    values = np.asarray(values)
    if values.ndim != 2 or values.shape[1] != 12:
        raise ValueError('Expected twelve monthly coverage observations')
    if not np.isin(values, [-15, -9, -8, -7, -1, 1, 2]).all():
        raise ValueError('Unexpected MEPS monthly coverage code')
    yes = (values == 1).sum(axis=1)
    unknown = np.isin(values, [-15, -9, -8, -7]).sum(axis=1)
    return yes / 12.0, (yes + unknown) / 12.0, (yes > 0).astype(float), unknown


def cps_coverage_bounds(codes):
    """CPS supplies none/some/all, not a month count; some spans 1..11."""
    codes = np.asarray(codes)
    if not np.isin(codes, [0, 1, 2, 3]).all():
        raise ValueError('Unexpected CPS annual coverage code')
    return ((codes == 3) + (codes == 2) / 12.0,
            (codes == 3) + 11 * (codes == 2) / 12.0)


def canonical_cps_domains(cps):
    """Use the canonical all-age civilian, reference exposure and origin rules."""
    civilian = cps.PRPERTYP.eq(2) | cps.A_AGE.lt(15)
    exposure = ~(cps.PUB.eq(0) & cps.PRIV.eq(0))
    if cps.loc[~exposure, 'A_AGE'].gt(0).any():
        raise ValueError('Post-reference-year exclusion contains noninfant')
    if cps.PENATVTY.le(0).any():
        raise ValueError('Unknown birthplace cannot select a donor')
    native = cps.PRCITSHP.isin([1, 2, 3])
    parents_us = cps.PEFNTVTY.isin([57, 60, 66, 69, 73, 78]) & cps.PEMNTVTY.isin([57, 60, 66, 69, 73, 78])
    mexico_born = cps.PRCITSHP.isin([4, 5]) & cps.PENATVTY.eq(303)
    second = native & (cps.PEFNTVTY.eq(303) | cps.PEMNTVTY.eq(303))
    third_plus = native & parents_us & cps.PRDTHSP.eq(1)
    return civilian.to_numpy(), exposure.to_numpy(), (mexico_born | second | third_plus).to_numpy()


def wr_variance(data, influence):
    """Full-design stratified PSU estimator, including zero domain influences."""
    positive = data.PERWT23F.gt(0)
    frame = data.loc[positive, ['VARSTR', 'VARPSU']].copy()
    frame['v'] = np.asarray(influence)[positive]
    if frame[['VARSTR', 'VARPSU']].isna().any().any():
        raise ValueError('Missing survey design')
    psu = frame.groupby(['VARSTR', 'VARPSU']).v.sum()
    variance = 0.0
    for _, block in psu.groupby(level=0):
        n = len(block)
        if n < 2:
            raise ValueError('Lonely PSU; no silent design fallback')
        variance += n / (n - 1) * ((block - block.mean()) ** 2).sum()
    return float(variance)


def load_meps(root):
    sys.path.insert(0, str(root / 'infra/immigration-fiscal/build'))
    from public_mvp_io import parse_meps_sas_fields
    folder = root / 'sources/immigration-fiscal/data/external/stage3/ahrq/meps'
    archive, layout_path = folder / 'h251dat.zip', folder / 'h251su.txt'
    layout = parse_meps_sas_fields(layout_path)
    coverage = [f'MCD{month}23X' for month in MONTHS]
    fields = ['AGE23X', 'BORNUSA', 'PERWT23F', 'VARSTR', 'VARPSU', 'TOTMCD23', *coverage]
    if not set(fields) <= layout.keys():
        raise ValueError('Required MEPS2023 variables absent')
    with zipfile.ZipFile(archive) as z:
        members = [name for name in z.namelist() if name.lower().endswith('.dat')]
        if len(members) != 1:
            raise ValueError('Ambiguous MEPS raw member')
        data = pd.DataFrame([{k: float(line[layout[k][0]:sum(layout[k])])
                              for k in fields} for line in z.open(members[0])])
    if data.TOTMCD23.lt(0).any() or data.PERWT23F.lt(0).any():
        raise ValueError('Invalid Medicaid expenditure or weight')
    low, high, ever, unknown = monthly_bounds(data[coverage])
    data['member_years_low'], data['member_years_high'] = low, high
    data['ever_covered'], data['unknown_months'] = ever, unknown
    data['age_band'] = np.digitize(data.AGE23X, [18, 35, 50, 65])
    return data, [archive, layout_path]


def national_meps(data, ratio):
    masks = {'all': np.ones(len(data), bool),
             'age_0_20': data.AGE23X.between(0, 20).to_numpy(),
             'age_21_64': data.AGE23X.between(21, 64).to_numpy(),
             'age_65_plus': data.AGE23X.ge(65).to_numpy(),
             'age_unknown_or_out_of_scope': data.AGE23X.lt(0).to_numpy()}
    rows = []
    for group, mask in masks.items():
        w = data.PERWT23F.to_numpy() * mask
        spend = float(w @ data.TOTMCD23)
        years_low, years_high = float(w @ data.member_years_low), float(w @ data.member_years_high)
        ever = float(w @ data.ever_covered)
        row = dict(domain=group, records=int((mask & data.PERWT23F.gt(0)).sum()),
                   population=float(w.sum()), raw_spending=spend, calibrated_spending=spend * ratio,
                   se_raw_spending=np.sqrt(wr_variance(data, w * data.TOTMCD23)),
                   member_years_low=years_low, member_years_high=years_high,
                   ever_enrolled=ever, unknown_weighted_months=float(w @ data.unknown_months),
                   raw_per_ever_enrollee=spend / ever,
                   raw_per_member_year_low=spend / years_high,
                   raw_per_member_year_high=spend / years_low,
                   calibrated_per_member_year_low=spend * ratio / years_high,
                   calibrated_per_member_year_high=spend * ratio / years_low,
                   denominator_correction_pct=(ever / years_low - 1) * 100)
        rate = spend / years_low
        influence = w * (data.TOTMCD23.to_numpy() - rate * data.member_years_low) / years_low
        row['se_raw_per_member_year'] = np.sqrt(wr_variance(data, influence))
        row['se_calibrated_per_member_year'] = row['se_raw_per_member_year'] * ratio
        rows.append(row)
    result = pd.DataFrame(rows)
    additive = ['population', 'raw_spending', 'calibrated_spending',
                'member_years_low', 'member_years_high', 'ever_enrolled']
    np.testing.assert_allclose(result.loc[1:, additive].sum().to_numpy(float),
                               result.loc[0, additive].to_numpy(float), rtol=1e-12, atol=.01)
    return result


def load_scorecard(path):
    payload = json.loads(path.read_text())
    rows = pd.DataFrame(payload['results'])
    if payload['count'] != len(rows) or not rows.measure_id.eq('EX.5').all():
        raise ValueError('Incomplete/wrong Scorecard data')
    if set(rows.data_period) != {'2022', '2023'}:
        raise ValueError('Scorecard year set changed; revisit year match')
    if rows.duplicated(['state_abbreviation', 'data_period', 'strat_tier1_value']).any():
        raise ValueError('Duplicate Scorecard state/year/eligibility observations')
    rows['per_member_year'] = pd.to_numeric(rows.measure_value.replace('null', np.nan), errors='raise')
    return rows


def cps_projection(root, meps, ratio):
    archive = root / 'sources/immigration-fiscal/data/census/cps_asec_2024_march.zip'
    fields = ['PH_SEQ', 'A_AGE', 'PENATVTY', 'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP',
              'MARSUPWT', 'MCAID_CYR', 'MCAID', 'CAID', 'PUB', 'PRIV', 'PRPERTYP', 'PRCITSHP']
    with zipfile.ZipFile(archive) as z:
        cps = pd.read_csv(z.open('pppub24.csv'), usecols=fields)
        household = pd.read_csv(z.open('hhpub24.csv'), usecols=['H_SEQ', 'GESTFIPS'])
    cps = cps.merge(household, left_on='PH_SEQ', right_on='H_SEQ', validate='many_to_one', how='left')
    if cps[fields + ['GESTFIPS']].isna().any().any():
        raise ValueError('Missing CPS value or household state')
    cps['age_band'] = np.digitize(cps.A_AGE, [18, 35, 50, 65])
    cps['BORNUSA'] = np.where(cps.PENATVTY.eq(57), 1, 2)
    donors = meps.loc[meps.PERWT23F.gt(0) & meps.BORNUSA.isin([1, 2]) & meps.AGE23X.ge(0)].copy()
    donors['wx'] = donors.PERWT23F * donors.TOTMCD23
    means = donors.groupby(['age_band', 'BORNUSA']).agg(population=('PERWT23F', 'sum'),
                                                        total=('wx', 'sum'), records=('wx', 'size'))
    means['medicaid_mean'] = means.total / means.population
    cps = cps.merge(means.medicaid_mean, on=['age_band', 'BORNUSA'], how='left', validate='many_to_one')
    if cps.medicaid_mean.isna().any():
        raise ValueError('Unsupported age/birth donor cell')
    civilian, exposure, mexican = canonical_cps_domains(cps)
    cps['medicaid_mean'] *= exposure
    low, high = cps_coverage_bounds(cps.MCAID_CYR)
    cps['member_low'], cps['member_high'] = low, high
    # CPS reported Medicaid only; combined coverage CYR also has CHIP/other.
    # These bounds apply to the combined concept, not exact Medicaid person-years.
    all_group = np.ones(len(cps), bool)
    groups = {'all': civilian, 'mexican_origin_canonical_union': civilian & mexican}
    rows = []
    for state, state_mask in [('US', all_group), ('CA', cps.GESTFIPS.eq(6)), ('TX', cps.GESTFIPS.eq(48))]:
        for group, group_mask in groups.items():
            weight = cps.MARSUPWT.to_numpy() / 100 * state_mask * group_mask
            raw = float(weight @ cps.medicaid_mean)
            lower, upper = float(weight @ cps.member_low), float(weight @ cps.member_high)
            rows.append(dict(state=state, group=group, population=float(weight.sum()),
                             raw_model_spending=raw, calibrated_model_spending=raw * ratio,
                             coverage_member_years_low=lower, coverage_member_years_high=upper,
                             reported_medicaid_ever=float(weight @ cps.CAID.eq(1)),
                             combined_coverage_ever=float(weight @ cps.MCAID.eq(1)),
                             implied_calibrated_cost_low=raw * ratio / upper,
                             implied_calibrated_cost_high=raw * ratio / lower))
    return pd.DataFrame(rows), means.reset_index(), archive


def scope_stresses(raw, calibrated_spending, out):
    """Observed LTSS amounts provide scale tests, not a matched subtraction.

    TAF encounter expenditures and CMS64 cash payments differ; all-LTSS also
    removes HCBS already represented in MEPS. Do not label residual a lower bound.
    """
    with zipfile.ZipFile(raw / 'ltss2023_tables.zip') as z:
        book = pd.ExcelFile(z.open('A2_LTSSExpDlvrySystm_2023.xlsx'))
        total = pd.read_excel(book, sheet_name='A.2.1 All-Total', header=1)
        inst = pd.read_excel(book, sheet_name='A.2.2 All-Inst', header=1)
        quality = pd.read_excel(book, sheet_name='DQ Measures', header=1)
    quality.loc[quality.State.isin(['California', 'Texas'])].to_csv(
        out / 'ltss_2023_ca_tx_quality.csv', index=False)
    selected = total.loc[total.State.isin(['National', 'California', 'Texas'])].copy()
    columns = ['LTSS (total)', 'Institutional (total)', 'HCBS (total)']
    for col in columns:
        selected[col] = pd.to_numeric(selected[col], errors='raise')
    if not np.allclose(selected[columns[0]], selected[columns[1]] + selected[columns[2]], atol=1, rtol=0):
        raise ValueError('LTSS expenditures fail component identity')
    selected.to_csv(out / 'ltss_2023_observed.csv', index=False)
    national = selected.loc[selected.State.eq('National')].iloc[0]
    inst_national = inst.loc[inst.State.eq('National')].iloc[0]
    dsh_names = [c for c in inst if 'DSH' in str(c) and 'total' in str(c)]
    if len(dsh_names) != 1:
        raise ValueError('Cannot identify institutional DSH total')
    dsh = float(inst_national[dsh_names[0]])
    rows = []
    for label, subtraction in [
            ('unadjusted_scope_gap', 0),
            ('subtract_published_institutional_LTSS_excluding_DSH', national['Institutional (total)'] - dsh),
            ('subtract_ALL_published_LTSS_excluding_DSH_including_overlapping_HCBS', national['LTSS (total)'] - dsh)]:
        remainder = 877.2e9 - subtraction
        rows.append(dict(stress=label, cms_reported_total=877.2e9,
                         subtraction=subtraction, dsh_already_excluded_from_scorecard=dsh,
                         remaining_admin_scale=remainder, calibrated_meps=calibrated_spending,
                         residual_scale=remainder - calibrated_spending,
                         status='ARITHMETIC_SCALE_TEST_NOT_MATCHED_CORRECTION_OR_HARD_BOUND'))
    pd.DataFrame(rows).to_csv(out / 'scope_stresses_2023.csv', index=False)
    payload = json.loads((raw / 'ex2_national2023.json').read_text())
    fiscal = pd.DataFrame(payload['results'])
    if payload['count'] != len(fiscal) or not fiscal.data_period.eq('2023').all():
        raise ValueError('Incomplete or wrong-year EX.2 dataset')
    fiscal = fiscal.loc[fiscal.value_type.str.contains('Dollars')].copy()
    fiscal['spending'] = pd.to_numeric(fiscal.measure_value, errors='raise')
    fiscal[['group_tier1_value', 'group_tier2_value', 'spending']].to_csv(
        out / 'cms_fy2023_service_spending.csv', index=False)
    medicaid = fiscal.loc[fiscal.group_tier2_value.eq('Medicaid')]
    children = medicaid.loc[~medicaid.group_tier1_value.eq('Total'), 'spending'].sum()
    reported_total = medicaid.loc[medicaid.group_tier1_value.eq('Total'), 'spending'].iloc[0]
    # Published category rows do not exhaust the separately reported total.
    # Preserve that discrepancy rather than forcing an invented residual category.
    pd.DataFrame([dict(fiscal_year=2023, published_medicaid_total=reported_total,
                       sum_displayed_medicaid_categories=children,
                       unallocated_difference=reported_total - children,
                       status='PUBLISHED_CATEGORY_SUBTOTAL_DIFFERS;NO_FORCED_ALLOCATION')]).to_csv(
        out / 'cms_fy2023_category_closure.csv', index=False)
    return rows


def build(root, raw, out):
    pins = verify_sources(raw)
    out.mkdir(parents=True, exist_ok=True)
    # A failed rebuild must never leave a stale successful receipt behind.
    (out / 'audit.json').unlink(missing_ok=True)
    params_path = root / 'infra/immigration-fiscal/ledger_absolute_2026_09_17/params/params.json'
    ratio = json.loads(params_path.read_text())['meps_coverage']['nhea_to_meps_ratio_medicaid']['value']
    scorecard = load_scorecard(raw / 'ex5.json')
    national = pd.DataFrame(NATIONAL_ROWS, columns=['eligibility', 'member_years_millions',
                                                  'spending_billions', 'per_member_year'])
    # The national administrative publication includes PR/Guam/USVI, unlike MEPS.
    national['scope'] = '50 states/DC plus PR/Guam/USVI; Title XIX; all residence settings'
    national.to_csv(out / 'cms_national_2023.csv', index=False)
    scorecard.to_csv(out / 'cms_state_eligibility_2022_2023.csv', index=False)
    data, inputs = load_meps(root)
    meps = national_meps(data, ratio)
    meps.to_csv(out / 'meps_national_2023.csv', index=False)
    projected, donor_cells, cps_path = cps_projection(root, data, ratio)
    projected.to_csv(out / 'cps_transport_2023.csv', index=False)
    donor_cells.to_csv(out / 'donor_cells_2023.csv', index=False)
    rate_rows = scorecard.loc[scorecard.data_period.eq('2023') & scorecard.state_abbreviation.isin(['CA', 'TX'])]
    rate_rows[['state_abbreviation', 'strat_tier1_value', 'per_member_year', 'notes']].to_csv(
        out / 'ca_tx_observed_rates_2023.csv', index=False)
    total = meps.iloc[0]
    comparisons = []
    for basis in ['raw', 'calibrated']:
        comparisons.append(dict(comparison='National MEPS vs CMS; UNMATCHED_SCOPE', basis=basis,
                                survey_spending=total[f'{basis}_spending'], admin_spending=877.2e9,
                                difference=total[f'{basis}_spending'] - 877.2e9,
                                percent_difference=(total[f'{basis}_spending'] / 877.2e9 - 1) * 100,
                                survey_member_years=total.member_years_low, admin_member_years=94e6,
                                survey_per_member_year=total[f'{basis}_per_member_year_high'],
                                admin_per_member_year=877.2e9 / 94e6))
    pd.DataFrame(comparisons).to_csv(out / 'national_scope_comparison.csv', index=False)
    state_check = projected.loc[projected.group.eq('all') & projected.state.isin(['CA', 'TX'])].merge(
        rate_rows.loc[rate_rows.strat_tier1_value.eq('Total'), ['state_abbreviation', 'per_member_year']],
        left_on='state', right_on='state_abbreviation', validate='one_to_one')
    state_check['rate_gap_low_pct'] = (state_check.implied_calibrated_cost_low / state_check.per_member_year - 1) * 100
    state_check['rate_gap_high_pct'] = (state_check.implied_calibrated_cost_high / state_check.per_member_year - 1) * 100
    state_check['status'] = 'COMBINED_COVERAGE_BOUNDS_AND_SPENDING_SCOPE_DIFFER;NOT_EXACT_MATCH'
    state_check.to_csv(out / 'state_comparison_2023.csv', index=False)
    scope = scope_stresses(raw, total.calibrated_spending, out)
    inputs += [cps_path, params_path, root / 'infra/immigration-fiscal/build/public_mvp_io.py',
               root / 'infra/immigration-fiscal/build/meps_health_transport_2024.py',
               root / 'infra/immigration-fiscal/all_age_ledger_2026_09_17/analyze.py',
               root / 'infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extend_ledger.py']
    audit = dict(year=2023, model='canonical age/birth structure reconstructed with 2023 inputs',
                 calibration_ratio=ratio, raw_meps_rows=len(data),
                 positive_weight_meps_rows=int(data.PERWT23F.gt(0).sum()),
                 donor_age_rule='AGE23X >= 0; negative end-year ages retained only in direct national total and explicit age residual',
                 donor_age_excluded=meps.loc[meps.domain.eq('age_unknown_or_out_of_scope'),
                     ['records', 'population', 'raw_spending', 'calibrated_spending']].iloc[0].to_dict(),
                 scope_status='DEGRADED_COMPARABILITY_NOT_EXACT_ELIGIBILITY_VALIDATION',
                 canonical_correction_applied=False, institutions_added=False,
                 inputs=[dict(path=str(p), sha256=sha(p)) for p in inputs],
                 sources=pins, builder_sha256=sha(Path(__file__)),
                 outputs=[dict(name=p.name, sha256=sha(p)) for p in sorted(out.glob('*.csv'))])
    (out / 'audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    print(meps.to_string(index=False))
    print(projected.to_string(index=False))
    print(pd.DataFrame(scope).to_string(index=False))
    return audit


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path, default=Path('/Users/alien/Projects/immigration-research'))
    parser.add_argument('--raw', type=Path, default=HERE / 'raw')
    parser.add_argument('--out', type=Path, default=HERE / 'derived')
    args = parser.parse_args()
    build(args.root, args.raw, args.out)
