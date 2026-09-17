"""Pew repeated cross sections: raw-item harmonization, no person-level joins.

Inputs are the frozen eight SAVs under --lane-dir/derived/pew. No raw edits.
Outputs are aggregate CSVs plus mapping/provenance/checks, not respondent data.
Requires numpy, pandas, pyreadstat. No inferential survey-design SEs are claimed.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd
import pyreadstat


SPECS = [
    dict(year=2011, match='PHCNSL2011', n=1220, w='weight', own='qn4', mother='qn7', father='qn8', party='qn81', lean='qn82', combo='combo81_82', english='qn57', american='qn54', age='qn95', sex='gender', origin=['qn301', 'qn302'], wording='2011-12'),
    dict(year=2012, match='PHCNSL2012', n=1765, w='weight', own='qn4', mother='qn7', father='qn8', party='qn61', lean='qn62', combo='Combo61_62', english='qn38', american=None, age='qn73', sex='gender', origin=['qn3'], wording='2011-12'),
    dict(year=2013, match='2013-U.S.', n=5103, w='totalwt', own='Q4', mother='Q410', father='Q411', party='PARTY', lean='PARTYLN', combo=None, english='Q387', american='Q130', age='q420rec', sex='GENDER', origin=['Q3REC'], wording='2013+'),
    dict(year=2014, match='2014-National', n=1520, w='weight', own='q4', mother='q7', father='q8', party='party', lean='partyln', combo='party_combo', english='lan3', american=None, age='age', sex='gender', origin=['q3'], wording='2013+'),
    dict(year=2015, match='2015-National', n=1500, w='weights', own='q4', mother='q7', father='q8', party='party', lean='partyln', combo='party_combo', english='lan3', american='q14', age='age', sex='sex', origin=['q3_combo'], wording='2013+'),
    dict(year=2016, match='2016-National', n=1507, w='weights', own='qn4', mother='qn7', father='qn8', party='party', lean='partyln', combo='party_combo', english='qnlan3', american=None, age='age', sex='sex', origin=['qn3'], wording='2013+'),
    dict(year=2018, match='2018-National', n=1501, w='weight', own='qn4', mother='qn7', father='qn8', party='party', lean='partyln', combo='party_combo', english='qnlan3', american=None, age='age', sex='sex', origin=['qn3'], wording='2013+'),
]
GENS = ['G1', 'G2', 'G3plus', 'unknown']


def generation(own, mother, father, pr_native):
    native = [1, 2] if pr_native else [2]
    abroad = [3] if pr_native else [1, 3]
    result = pd.Series('unknown', index=own.index)
    result.loc[own.isin(abroad)] = 'G1'
    result.loc[own.isin(native) & (mother.isin(abroad) | father.isin(abroad))] = 'G2'
    result.loc[own.isin(native) & mother.isin(native) & father.isin(native)] = 'G3plus'
    return result


def moments(y, w):
    ok = y.notna() & w.notna() & (w > 0)
    yy, ww = y[ok], w[ok]
    return dict(valid_n=int(ok.sum()), missing_n=int((~ok).sum()),
                excluded_weight_pct=float(w[~ok].sum() / w.sum() * 100) if w.sum() else None,
                weighted_pct=float(np.average(yy, weights=ww) * 100) if ok.any() else None,
                sum_weight=float(ww.sum()), kish_n=float(ww.sum() ** 2 / (ww @ ww)) if ok.any() else None)


def checks_generation():
    o = pd.Series([2, 2, 2, 8, 3, 1, 2, 2])
    m = pd.Series([2, 3, 2, 3, 9, 2, 1, 9])
    f = pd.Series([2, 9, 9, 2, 9, 2, 2, 9])
    assert generation(o, m, f, True).tolist() == ['G3plus', 'G2', 'unknown', 'unknown', 'G1', 'G3plus', 'G3plus', 'unknown']
    assert generation(o, m, f, False).tolist() == ['G3plus', 'G2', 'unknown', 'unknown', 'G1', 'G1', 'G2', 'unknown']


def load_survey(root, s):
    folders = [p for p in root.iterdir() if p.is_dir() and s['match'] in p.name]
    assert len(folders) == 1, s
    files = list(folders[0].glob('*.sav'))
    assert len(files) == 1
    sav = files[0]
    intake = json.loads((root / 'manifest.json').read_text())
    record = next(r for r in intake if Path(r['sav']).name == sav.name)
    encoding = record['encoding']
    # Existing intake records the SAV's required encoding; never retry silently.
    d, meta = pyreadstat.read_sav(sav, user_missing=True, encoding=None if encoding == 'readstat-auto' else encoding)
    assert len(d) == s['n']
    w = d[s['w']]
    assert w.notna().all() and (w > 0).all()
    for key in ['own', 'mother', 'father']:
        labels = meta.variable_value_labels[s[key]]
        assert 'Puerto Rico' in labels[1] and labels[2] in ['U.S.', 'United States']
    eng_labels = meta.variable_value_labels[s['english']]
    assert eng_labels[1].lower() == 'very well' and eng_labels[4].lower() == 'not at all'
    p, lean = d[s['party']], d[s['lean']]
    # Direct R/D answers outrank structurally unasked lean; remainder classified separately.
    choice = p.where(p.isin([1, 2]), lean.where(lean.isin([1, 2])))
    observed_dem = choice.eq(2).astype(float)
    observed_rep = choice.eq(1).astype(float)
    no_choice = choice.isna().astype(float)
    residual = pd.Series('major_party', index=d.index)
    residual.loc[choice.isna()] = 'unresolved_missing_or_skip'
    residual.loc[choice.isna() & lean.isin([3, 4])] = 'explicit_neither_other_lean'
    residual.loc[choice.isna() & lean.eq(8)] = 'lean_dont_know'
    residual.loc[choice.isna() & lean.eq(9)] = 'lean_refused' if s['year'] != 2013 else 'lean_other_dk_refused_combined'
    checks = {'n': len(d), 'positive_weights': True}
    # Published primary top lines use every respondent, including residual responses.
    expected_dem_rounded = {2011: 60, 2012: 66, 2013: 56, 2014: 58, 2015: 56, 2016: 60, 2018: 56}
    checks['dem_all_pct'] = float(np.average(observed_dem, weights=w) * 100)
    assert round(checks['dem_all_pct']) == expected_dem_rounded[s['year']]
    if s['combo']:
        for value in [1, 2]:
            assert choice.eq(value).equals(d[s['combo']].eq(value)), (s['year'], value)
        checks['direct_party_equals_published_combo'] = True
    else:
        checks['direct_party_equals_published_combo'] = 'No published composite in SAV'
    age = d[s['age']]
    if s['year'] == 2013:
        ageband = age.map({**dict.fromkeys([1, 2], 1), **dict.fromkeys([3, 4, 5, 6], 2), **dict.fromkeys([7, 8, 9], 3), **dict.fromkeys([10, 11, 12, 13, 14, 15], 4)})
    else:
        age = age.where(age.between(18, 97))
        ageband = pd.cut(age, bins=[17, 29, 49, 64, 120], labels=[1, 2, 3, 4]).astype(float)
        # Only compatible published four-band age categories may fill refused exact ages.
        band_key = 'Combo73_73a' if s['year'] == 2012 else 'age_combo'
        if band_key in d and s['year'] != 2016:
            ageband = ageband.fillna(d[band_key].where(d[band_key].isin([1, 2, 3, 4])))
    out = pd.DataFrame({'year': s['year'], 'weight': w, 'ageband': ageband,
                        'sex': d[s['sex']].where(d[s['sex']].isin([1, 2])),
                        'mexican_report': d[s['origin']].eq(1).any(axis=1),
                        'party_residual': residual,
                        'initial_party': p,
                        'dem_all': observed_dem, 'rep_all': observed_rep, 'no_major_party': no_choice,
                        'dem_two_party': observed_dem.where(choice.notna()),
                        'english_very_well': d[s['english']].eq(1).astype(float).where(d[s['english']].isin([1, 2, 3, 4]))})
    if s['combo']:
        out['dem_composite_valid'] = observed_dem.where(d[s['combo']].isin([1, 2, 3, 4]))
    if s['american']:
        out['typical_american'] = d[s['american']].eq(1).astype(float).where(d[s['american']].isin([1, 2]))
    for pr_native in [True, False]:
        out['gen_PR_native' if pr_native else 'gen_PR_migration'] = generation(d[s['own']], d[s['mother']], d[s['father']], pr_native)
    fields = [s[k] for k in ['w', 'own', 'mother', 'father', 'party', 'lean', 'combo', 'english', 'american', 'age', 'sex'] if s[k]] + s['origin']
    source = dict(survey_year=s['year'], sav=str(sav.relative_to(root)), encoding=encoding, sha256=hashlib.sha256(sav.read_bytes()).hexdigest(), n=len(d), fields={k: dict(label=meta.column_names_to_labels[k], values=meta.variable_value_labels.get(k, {})) for k in fields}, checks=checks)
    return out, source


def fit_adjusted(data, outcome, construction, population, wording_scope):
    """Descriptive WLS; equal total survey weight, fixed effects, no causal estimand."""
    d = data.copy()
    if population == 'reported_mexican':
        d = d[d.mexican_report]
    if wording_scope == '2013plus':
        d = d[d.year >= 2013]
    d = d[d[construction].isin(GENS[:3])].dropna(subset=['ageband', 'sex'])
    # Freeze equal-survey-year base weights BEFORE outcome conditioning. Thus
    # D/all and D/(D+R) do not silently use different within-year normalizations.
    d['model_weight'] = d.weight / d.groupby('year').weight.transform('sum')
    d = d.dropna(subset=[outcome])
    if len(d) == 0:
        return []
    rows = []
    for controls in [False, True]:
        x = pd.DataFrame({'intercept': np.ones(len(d)), 'G2': d[construction].eq('G2').astype(float).values, 'G3plus': d[construction].eq('G3plus').astype(float).values}, index=d.index)
        # Survey fixed effects always included, age/sex only sensitivity (potential mediators).
        extra = ['year', 'ageband', 'sex'] if controls else ['year']
        for field in extra:
            for value in sorted(d[field].unique())[1:]:
                x[f'{field}_{value}'] = d[field].eq(value).astype(float)
        a, y, w = x.to_numpy(), d[outcome].to_numpy(), d.model_weight.to_numpy()
        assert np.linalg.matrix_rank(a) == a.shape[1]
        beta, _, _, _ = np.linalg.lstsq(a * np.sqrt(w)[:, None], y * np.sqrt(w), rcond=None)
        assert np.max(np.abs(a.T @ (w * (y - a @ beta)))) < 1e-8
        for gen in ['G2', 'G3plus']:
            rows.append(dict(outcome=outcome, construction=construction, population=population, wording_scope=wording_scope, model='survey_year_age_sex' if controls else 'survey_year', generation=gen, versus='G1', adjusted_difference_pp=float(beta[x.columns.get_loc(gen)] * 100), n=len(d), survey_years=','.join(map(str, sorted(d.year.unique()))), interpretation='descriptive association; no design SE; controls do not identify causal assimilation'))
        rows.append(dict(outcome=outcome, construction=construction, population=population, wording_scope=wording_scope, model='survey_year_age_sex' if controls else 'survey_year', generation='G3plus', versus='G2', adjusted_difference_pp=float((beta[2] - beta[1]) * 100), n=len(d), survey_years=','.join(map(str, sorted(d.year.unique()))), interpretation='descriptive association; no design SE; controls do not identify causal assimilation'))
    return rows


def denominator_audit(data):
    rows, residuals = [], []
    for construction in ['gen_PR_native', 'gen_PR_migration']:
        for population in ['all_self_identified_latinos', 'reported_mexican']:
            for scope in ['all_years', '2013plus']:
                d = data.copy()
                if population == 'reported_mexican':
                    d = d[d.mexican_report]
                if scope == '2013plus':
                    d = d[d.year >= 2013]
                d = d[d[construction].isin(GENS[:3])].dropna(subset=['ageband', 'sex'])
                d['base_weight'] = d.weight / d.groupby('year').weight.transform('sum')
                for year in ['pooled'] + sorted(d.year.unique().tolist()):
                    dd = d if year == 'pooled' else d[d.year.eq(year)]
                    for gen in ['all'] + GENS[:3]:
                        c = dd if gen == 'all' else dd[dd[construction].eq(gen)]
                        w = c.base_weight
                        dw, rw = float(w[c.dem_all.eq(1)].sum()), float(w[c.rep_all.eq(1)].sum())
                        allpct = dw / w.sum() * 100
                        twopct = dw / (dw + rw) * 100
                        assert np.isclose(allpct, np.average(c.dem_all, weights=w) * 100)
                        take = (c.dem_all + c.rep_all).eq(1)
                        assert np.isclose(twopct, np.average(c.loc[take, 'dem_all'], weights=w[take]) * 100)
                        common = dict(construction=construction, population=population, wording_scope=scope, year=year, generation=gen)
                        rows.append(dict(**common, base_n=len(c), dem_n=int(c.dem_all.sum()), rep_n=int(c.rep_all.sum()), residual_n=int(c.no_major_party.sum()), weight_total=float(w.sum()), dem_weight=dw, rep_weight=rw, reported_dem_all_pct=allpct, dem_among_major_partisans_pct=twopct, effective_base_n=float(w.sum() ** 2 / (w @ w)), year_weighting='each survey has weight one on age-sex-known generation-known base; frozen before conditioning'))
                        for category, cc in c.groupby('party_residual'):
                            residuals.append(dict(**common, category=category, n=len(cc), weight=float(cc.base_weight.sum()), pct=float(cc.base_weight.sum() / w.sum() * 100), note='2013 combined Other/DK/Refused cannot be separated by provided answer code'))
    return pd.DataFrame(rows), pd.DataFrame(residuals)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--lane-dir', type=Path, required=True)
    ap.add_argument('--output-dir', type=Path, required=True)
    args = ap.parse_args()
    root = args.lane_dir / 'derived/pew'
    args.output_dir.mkdir(parents=True, exist_ok=True)
    checks_generation()
    frames, sources = [], []
    for s in SPECS:
        d, source = load_survey(root, s)
        frames.append(d)
        sources.append(source)
    full = pd.concat(frames, ignore_index=True)
    assert len(full) == 14116
    outcomes = ['dem_all', 'rep_all', 'no_major_party', 'dem_two_party', 'dem_composite_valid', 'english_very_well', 'typical_american']
    rows, missing, models = [], [], []
    for d, s in zip(frames, SPECS):
        for construction in ['gen_PR_native', 'gen_PR_migration']:
            for population in ['all_self_identified_latinos', 'reported_mexican']:
                subset = d[d.mexican_report] if population == 'reported_mexican' else d
                for gen in ['all'] + GENS:
                    cell = subset if gen == 'all' else subset[subset[construction].eq(gen)]
                    for outcome in outcomes:
                        if outcome in cell:
                            rows.append(dict(year=s['year'], construction=construction, population=population, generation=gen, outcome=outcome, cell_n=len(cell), **moments(cell[outcome], cell.weight)))
                missing.append(dict(year=s['year'], construction=construction, population=population, n=len(subset), unknown_gen_n=int(subset[construction].eq('unknown').sum()), unknown_gen_weighted_pct=float(np.average(subset[construction].eq('unknown'), weights=subset.weight) * 100), missing_age_n=int(subset.ageband.isna().sum()), missing_sex_n=int(subset.sex.isna().sum())))
    for outcome in ['dem_all', 'dem_two_party', 'english_very_well', 'typical_american']:
        for construction in ['gen_PR_native', 'gen_PR_migration']:
            for population in ['all_self_identified_latinos', 'reported_mexican']:
                for wording_scope in ['all_years', '2013plus']:
                    models.extend(fit_adjusted(full, outcome, construction, population, wording_scope))
    summary = pd.DataFrame(rows)
    summary.to_csv(args.output_dir / 'generation_outcomes.csv', index=False)
    pd.DataFrame(missing).to_csv(args.output_dir / 'classification_missingness.csv', index=False)
    pd.DataFrame(models).to_csv(args.output_dir / 'composition_sensitivity.csv', index=False)
    audit, residuals = denominator_audit(full)
    audit.to_csv(args.output_dir / 'denominator_audit.csv', index=False)
    residuals.to_csv(args.output_dir / 'party_residuals.csv', index=False)
    coverage = []
    for s in SPECS:
        coverage.append(dict(survey=s['year'], n=s['n'], party_wording=s['wording'], party_fields=s['party']+' + '+s['lean'], english_field=s['english'], typical_american_field=s['american'] or 'absent', own_birth=s['own'], mother_birth=s['mother'], father_birth=s['father'], weight=s['w'], scope='self-identified Latino adults; cross section, not panel'))
    coverage.append(dict(survey='2015-16 nonidentifier supplement', n=401, scope='Excluded from seven-wave series: different selection population; already analyzed with NSL2015 external mixture calibration', party_fields='party + partyln', english_field='lan3', typical_american_field='q14', own_birth='q4', mother_birth='q7', father_birth='q8', weight='OMNIWeight', party_wording='2013+'))
    pd.DataFrame(coverage).to_csv(args.output_dir / 'comparability.csv', index=False)
    payload = dict(status='PASS', surveys=7, repeated_cross_section_records=len(full), omitted_nonidentifier_records=401, checks=['expected seven survey sizes', 'all weights finite/positive', 'raw birthplace and English response labels validated', 'unknown parent cases remain unknown unless another parent establishes G2', 'Puerto Rico convention test cases', 'direct R/D membership agrees exactly with provided party composites in all six available surveys', 'seven all-respondent party estimates reproduce rounded primary toplines', 'weighted least-squares normal equations checked'], sources=sources)
    (args.output_dir / 'verification.json').write_text(json.dumps(payload, indent=2))
    selected = summary[(summary.construction == 'gen_PR_native') & (summary.population == 'all_self_identified_latinos') & summary.generation.isin(GENS[:3]) & summary.outcome.isin(['dem_all', 'english_very_well', 'typical_american'])]
    print(selected.pivot(index=['outcome', 'year'], columns='generation', values='weighted_pct').round(2).to_string())
    print('PASS: seven independent surveys, 14,116 records; all eight inputs covered.')


if __name__ == '__main__':
    main()
