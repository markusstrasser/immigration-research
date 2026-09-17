"""Unweighted IIMMLA education sensitivity with one fixed pooled age/sex standard."""
from pathlib import Path
import argparse
import hashlib
import json

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ALLOWED = HERE / 'derived' / 'joint_standard'
REPO = HERE.parents[2]
SOURCE = REPO / 'infra/immigration-fiscal/iimmla_2026_09_17/raw/ICPSR_22627/DS0001/22627-0001-Data.tsv'
RULES = REPO / 'infra/immigration-fiscal/iimmla_sensitivity_2026_09_17/analyze.py'
EXPECTED_SHA = '1d5fc8fbb1b2e52c7b5dc6c0e1c4b24d151066a7c19d35d3e4d5cc86ca360424'
AGE_LABELS = ['25–29', '30–34', '35–40']
SEX_LABELS = {1: 'Men', 0: 'Women'}
KEYS = [(a, s) for a in AGE_LABELS for s in ['Men', 'Women']]


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def raw_event(gate, respondent):
    out = pd.Series(np.nan, index=gate.index, dtype=float)
    out.loc[gate.eq(2) & respondent.eq(-9)] = 0.
    out.loc[gate.eq(1) & respondent.eq(2)] = 0.
    out.loc[gate.eq(1) & respondent.isin([1, 3])] = 1.
    return out


def strict_masks(d):
    foreign = lambda s: s.between(1, 70) & s.ne(62)
    own_us, parent_us = d.qs7.isin([1, 2]), d.qs10.eq(1)
    own_conflict = own_us & foreign(d.qs8)
    parent_conflict = parent_us & (d.qs11.isin([1, 2, 3]) | foreign(d.qs12am) | foreign(d.qs12bf))
    base = own_us & parent_us & ~own_conflict & ~parent_conflict
    birth = d[[f'q152b_{i}' for i in range(1, 5)]].copy()
    country = d[[f'q152c_{i}' for i in range(1, 5)]].copy()
    birth.columns = country.columns = range(4)
    country_foreign = country.ge(1) & country.le(70) & country.ne(62)
    conflict = (birth.eq(1) & country.eq(62)).any(axis=1) | (birth.eq(0) & country_foreign).any(axis=1)
    complete = birth.isin([0, 1]).all(axis=1) & birth.eq(1).any(axis=1) & d.q152b_5.eq(0) & d.q152b_6.eq(0)
    g3 = d.ethnos10.eq(1) & base & d.q152a.eq(1) & complete & ~conflict
    g4 = d.ethnos10.eq(1) & base & d.q152a.eq(2) & ~birth.eq(1).any(axis=1) & ~country_foreign.any(axis=1)
    if (g3 & g4).any():
        raise ValueError('Strict generation groups overlap')
    return {'G3': g3, 'G4plus': g4}


def run(source, output):
    if not output.resolve().is_relative_to(ALLOWED):
        raise ValueError(f'Output must stay under {ALLOWED}')
    source_sha = sha(source)
    if source_sha != EXPECTED_SHA:
        raise ValueError(f'Unexpected source SHA256: {source_sha}')
    d = pd.read_csv(source, sep='\t', low_memory=False)
    d.columns = d.columns.str.lower()
    if len(d) != 4655 or not d.caseid.is_unique:
        raise ValueError('Unexpected row count or repeated CASEID')
    credential_counts = d.educred5.value_counts().sort_index().to_dict()
    expected_credentials = {0: 521, 1: 755, 2: 1371, 3: 401, 4: 1132, 5: 475}
    if credential_counts != expected_credentials or d.educred5.isna().any():
        raise ValueError('EDUCRED5 differs from primary codebook frequency table')
    if not d.gender.isin([0, 1]).all() or not d.age.between(20, 40).all():
        raise ValueError('Unknown age/sex; no implicit exclusions allowed')
    weight_fields = [c for c in d if 'weight' in c or 'wgt' in c or c == 'wt']
    if weight_fields:
        raise ValueError(f'Weight-like fields require review: {weight_fields}')
    masks = strict_masks(d)
    arrest, incarcerated = raw_event(d.q201, d.q202), raw_event(d.q203a, d.q203b)
    common = arrest.notna() & incarcerated.notna() & d.educred5.isin(range(6))
    if tuple(int(m.sum()) for m in masks.values()) != (196, 187):
        raise ValueError('Strict-history full-age anchors changed')
    if tuple(int((m & common).sum()) for m in masks.values()) != (192, 182):
        raise ValueError('Common-endpoint full-age anchors changed')
    for raw, supplied in [(arrest, d.evarre), (incarcerated, d.evpriso)]:
        if raw.loc[raw.notna()].ne(supplied.loc[raw.notna()]).any():
            raise ValueError('Known raw endpoint conflicts with supplied binary')
    eligible = (masks['G3'] | masks['G4plus']) & d.age.between(25, 40)
    d = d.copy()
    d['age_cell'] = pd.cut(d.age, [24, 29, 34, 40], labels=AGE_LABELS).astype(object)
    d['sex'] = d.gender.map(SEX_LABELS)
    d['ba'] = d.educred5.ge(4)
    pooled = d.loc[eligible].groupby(['age_cell', 'sex']).size().to_dict()
    if set(pooled) != set(KEYS) or min(pooled.values()) <= 0:
        raise ValueError('Fixed pooled age/sex standard has an empty cell')
    total = sum(pooled.values())
    standards = []
    for age, sex in KEYS:
        sex_total = sum(n for (a, s), n in pooled.items() if s == sex)
        standards.append(dict(age_cell=age, sex=sex, pooled_n=pooled[age, sex],
                              pooled_joint_share=pooled[age, sex]/total,
                              pooled_within_sex_age_share=pooled[age, sex]/sex_total))
    cells, estimates, selected_groups = [], [], {}
    for mode, mode_mask in [('education_endpoint', pd.Series(True, index=d.index)), ('common_raw_endpoints', common)]:
        for group, generation in masks.items():
            selected = generation & eligible & mode_mask
            selected_groups[mode, group] = selected
            for age, sex in KEYS:
                use = selected & d.age_cell.eq(age) & d.sex.eq(sex)
                n, events = int(use.sum()), int(d.loc[use, 'ba'].sum())
                if n == 0:
                    raise ValueError(f'Empty required cell: {mode}/{group}/{age}/{sex}; no dropping or renormalization')
                cells.append(dict(sample_mode=mode, group=group, age_cell=age, sex=sex,
                                  n=n, ba_events=events, ba_percent=100*events/n))
        for scope in ['All', 'Men', 'Women']:
            keys = [key for key in KEYS if scope == 'All' or key[1] == scope]
            denominator = sum(pooled[key] for key in keys)
            target_shares = {key: pooled[key]/denominator for key in keys}
            outcomes = {}
            for group in masks:
                subset = selected_groups[mode, group] & (d.sex.eq(scope) if scope != 'All' else True)
                rows = [r for r in cells if r['sample_mode'] == mode and r['group'] == group and (r['age_cell'], r['sex']) in keys]
                if len(rows) != len(keys):
                    raise ValueError('Incomplete required standardization cell grid')
                standard = sum(target_shares[r['age_cell'], r['sex']] * r['ba_percent'] for r in rows)
                # Independent respondent-weight calculation checks the cell-level sum.
                cell_n = {(r['age_cell'], r['sex']): r['n'] for r in rows}
                respondent_weights = np.array([target_shares[a, s]/cell_n[a, s] for a, s in zip(d.loc[subset, 'age_cell'], d.loc[subset, 'sex'])])
                check = 100*np.dot(d.loc[subset, 'ba'].to_numpy(float), respondent_weights)
                if not np.isclose(respondent_weights.sum(), 1) or not np.isclose(check, standard):
                    raise ValueError('Respondent-weight and cell-rate standardization disagree')
                outcomes[group] = dict(n=int(subset.sum()), events=int(d.loc[subset, 'ba'].sum()),
                                       crude=100*d.loc[subset, 'ba'].mean(), standardized=standard)
            for method in ['crude', 'standardized']:
                estimates.append(dict(sample_mode=mode, scope=scope, method=method,
                                      G3_n=outcomes['G3']['n'], G3_BA=outcomes['G3']['events'],
                                      G4plus_n=outcomes['G4plus']['n'], G4plus_BA=outcomes['G4plus']['events'],
                                      G3_percent=outcomes['G3'][method], G4plus_percent=outcomes['G4plus'][method],
                                      G4plus_minus_G3_pp=outcomes['G4plus'][method]-outcomes['G3'][method]))
    output.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(standards).to_csv(output/'standard.csv', index=False)
    pd.DataFrame(cells).to_csv(output/'cell_counts.csv', index=False)
    result = pd.DataFrame(estimates)
    result.to_csv(output/'contrasts.csv', index=False)
    audit = dict(source=str(source), source_sha256=source_sha, script_sha256=sha(Path(__file__)),
                 source_rows=len(d), rules_source=str(RULES), rules_sha256=sha(RULES),
                 codebook_sha256=sha(source.with_name('22627-0001-Codebook.pdf')),
                 educred5_valid_n=len(d), educred5_missing_n=0, educred5_counts=credential_counts,
                 standard='Pooled strict G3/G4plus Mexican-self-ID ages25–40 with valid education; fixed for both sample modes',
                 pooled_standard_n=total, standard_cells=standards, minimum_analysis_cell_n=min(r['n'] for r in cells),
                 strict_all_age_counts={g:int(m.sum()) for g,m in masks.items()},
                 common_all_age_counts={g:int((m & common).sum()) for g,m in masks.items()},
                 checks=dict(raw_source_hash=True, primary_credential_frequencies=True, nonempty_all_cells=True,
                             fixed_standard_both_sample_modes=True, respondent_weight_crosscheck=True),
                 interpretation='Unweighted local descriptive sensitivity; no national/design confidence intervals; distinct cross-sectional populations; Mexican self-ID is not symmetric verified Mexican ancestry.')
    (output/'audit.json').write_text(json.dumps(audit, indent=2, allow_nan=False)+'\n')
    primary = next(r for r in estimates if r['sample_mode'] == 'education_endpoint' and r['scope'] == 'All' and r['method'] == 'standardized')
    lines = [f'**Verdict:** At ages 25–40, the jointly age/sex standardized strict G4+ minus G3 BA contrast is {primary["G4plus_minus_G3_pp"]:+.3f} percentage points in this local sample. Sex-specific and sample-selection comparisons follow; no national or design-based inference is claimed.', '',
             'Strict Mexican-self-ID groups; IIMMLA 2004, five-county Los Angeles, ages 25–40. BA means EDUCRED5 >= 4. All 4,655 source EDUCRED5 values are valid and reproduce the primary codebook counts.', '',
             f'One fixed standard pools all {total} strict education-eligible G3/G4+ respondents ages 25–40 over 25–29/30–34/35–40 × men/women. Both sample modes use that same standard. Sex-specific estimates use its within-sex age shares. Every needed group/sample/cell is nonempty; minimum n = {audit["minimum_analysis_cell_n"]}.', '',
             '| Sample | Scope | Method | G3 n / BA | G4+ n / BA | G3 BA% | G4+ BA% | G4+−G3 pp |',
             '|---|---|---|---:|---:|---:|---:|---:|']
    for r in estimates:
        lines.append(f'| {r["sample_mode"]} | {r["scope"]} | {r["method"]} | {r["G3_n"]} / {r["G3_BA"]} | {r["G4plus_n"]} / {r["G4plus_BA"]} | {r["G3_percent"]:.3f} | {r["G4plus_percent"]:.3f} | {r["G4plus_minus_G3_pp"]:+.3f} |')
    lines += ['', 'Cell entries below are n / BA count. The fixed standard uses the pooled education-endpoint sample; common-sample analyses do not change these weights.', '',
              '| Age | Sex | Fixed pooled n / share | Education G3 | Education G4+ | Common G3 | Common G4+ |',
              '|---|---|---:|---:|---:|---:|---:|']
    lookup = {(r['sample_mode'], r['group'], r['age_cell'], r['sex']): r for r in cells}
    for age, sex in KEYS:
        entries = []
        for mode in ['education_endpoint', 'common_raw_endpoints']:
            for group in ['G3', 'G4plus']:
                r = lookup[mode, group, age, sex]
                entries.append(f'{r["n"]} / {r["ba_events"]}')
        lines.append(f'| {age} | {sex} | {pooled[age, sex]} / {100*pooled[age, sex]/total:.3f}% | ' + ' | '.join(entries) + ' |')
    lines += ['', 'Counts/BA numerators describe the observed selected sample; standardized percentages use fixed cell shares. Education-endpoint rows retain everyone with valid education; common rows additionally require interpretable raw respondent arrest and incarceration answers. Neither sample definition establishes representative national generations.', '',
              'Detailed six-cell counts and BA numerators are in `cell_counts.csv`; target counts/shares in `standard.csv`; provenance and exact credential counts in `audit.json`. Generic migration generation and Mexican self-ID remain separate constructs: G4+ cannot be symmetrically verified through Mexican-born great-grandparents in this release.', '',
              'Reproduce: `UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 infra/immigration-fiscal/iimmla_sensitivity_2026_09_17/joint_standard.py`', '',
              'Primary codebook: GENDER values 0 = female / 1 = male; EDUCRED5 values 4 = bachelor, 5 = advanced degree; Q152A/B/C raw-grandparent questions. Existing strict definitions are traced by the hashed rules file. Raw inputs are read-only.']
    (output/'REPORT.md').write_text('\n'.join(lines)+'\n')
    print(result.to_string(index=False))
    print(f'PASS: {len(cells)} nonempty cells, {len(estimates)} contrasts, fixed standard n={total}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output-dir', type=Path, default=ALLOWED)
    args = parser.parse_args()
    run(args.source, args.output_dir)
