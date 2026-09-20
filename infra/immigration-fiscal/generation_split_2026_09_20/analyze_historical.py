"""Historical, descriptive generation splits; never a 2024 fiscal headcount."""
from pathlib import Path
import hashlib
import json
import numpy as np
import pandas as pd
import pyreadstat

ROOT = Path(__file__).resolve().parents[3]
BASE = ROOT / 'infra/immigration-fiscal/new_datasets_2026_09_17/derived'
OUT = Path(__file__).resolve().parent / 'derived/historical'
OUT.mkdir(parents=True, exist_ok=True)
ORDER = ['G1', 'G2', 'G3', 'G4plus', 'Unresolved']
SPECS = [
    ('NSL2015_identifiers', 'Pew-Research-Center_2015-National-Survey-of-Latinos-Dataset',
     'NSL2015_FOR RELEASE.sav', 'weights', 37.8, 1500),
    ('Omnibus2015_16_nonidentifiers', 'Pew-Research-Center_2016-Survey-of-Self-Identified-non-Hispanics-Dataset',
     'NSL2015 Omnibus_FOR RELEASE.sav', 'OMNIWeight', 4.9, 401),
]
SOURCE = 'https://www.pewresearch.org/race-and-ethnicity/2017/12/20/methodology-hispanic-identity/'


def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def classify(d):
    native = d.q4.eq(2)
    parents_native = native & d.q7.eq(2) & d.q8.eq(2)
    gps = d[['q8aa', 'q8ab', 'q8ba', 'q8bb']]
    masks = [d.q4.isin([1, 3]),
             native & (d.q7.isin([1, 3]) | d.q8.isin([1, 3])),
             parents_native & gps.isin([1, 3]).any(axis=1),
             parents_native & gps.eq(2).all(axis=1)]
    assert np.column_stack(masks).sum(axis=1).max() <= 1
    result = pd.Series(np.select(masks, ORDER[:4], default='Unresolved'), index=d.index)
    # Independent respondent-wise implementation, including unknown branches.
    def row_rule(r):
        own, mom, dad, *grandparents = r
        if own in (1, 3):
            return 'G1'
        if own != 2:
            return 'Unresolved'
        if mom in (1, 3) or dad in (1, 3):
            return 'G2'
        if mom != 2 or dad != 2:
            return 'Unresolved'
        if any(x in (1, 3) for x in grandparents):
            return 'G3'
        return 'G4plus' if all(x == 2 for x in grandparents) else 'Unresolved'
    check = d[['q4', 'q7', 'q8', 'q8aa', 'q8ab', 'q8ba', 'q8bb']].apply(row_rule, axis=1)
    assert result.equals(check)
    return result


def summarize(d, source, weight, universe):
    assert len(d) > 0 and d[weight].gt(0).all()
    denom = d[weight].sum()
    rows = []
    for g in ORDER:
        mask = d.generation.eq(g)
        rows.append(dict(source=source, universe=universe, generation=g,
                         n=int(mask.sum()), weight_mass=float(d.loc[mask, weight].sum()),
                         weighted_percent=100 * d.loc[mask, weight].sum() / denom,
                         denominator_n=len(d), denominator_weight=float(denom)))
    assert sum(x['n'] for x in rows) == len(d)
    assert abs(sum(x['weighted_percent'] for x in rows) - 100) < 1e-10
    return rows


audit = {'calibration_source': SOURCE,
         'calibration': {'identifying_million_benchmark': 37.8, 'nonidentifying_million_benchmark': 4.9,
                         'total_million_benchmark': 42.7,
                         'rule': 'Normalize full-survey weights, apply benchmark mixture, then subset q3_combo==1.'},
         'generation': 'Generic nativity; Puerto Rico treated as migrant origin. GP countries unavailable. G4plus is not exact G4.',
         'mexican_origin': 'q3_combo==1; code9 mixed heritage excluded because Mexican component unavailable.',
         'sources': [], 'checks': ['Positive finite weights', 'Full-survey normalization before origin subset',
                                  'Disjoint generation masks', 'Independent row classifier matches',
                                  'All generation rows including unknown exhaust numerator and sum to100%']}
frames, rows, ancestry = [], [], []
for name, folder, filename, wt, benchmark, expected_n in SPECS:
    p = BASE / 'pew' / folder / filename
    meta_path = p.parent / 'metadata.json'
    d, metadata = pyreadstat.read_sav(p, user_missing=True)
    labels = metadata.variable_value_labels
    assert len(d) == expected_n
    assert labels['q3_combo'][1] == 'Mexican' and 'Mixed heritage' in labels['q3_combo'][9]
    assert labels['q4'][2] == 'U.S.'
    assert d[wt].gt(0).all() and np.isfinite(d[wt]).all()
    d['source'], d['generation'], d['source_weight'] = name, classify(d), d[wt]
    d['pooled_weight'] = d[wt] / d[wt].sum() * (benchmark / 42.7)
    assert abs(d.pooled_weight.sum() - benchmark / 42.7) < 1e-12
    for kind, mask in [('Mexican', d.q3_combo.eq(1)), ('Mixed_unspecified', d.q3_combo.eq(9)),
                       ('Other_or_unknown', ~d.q3_combo.isin([1, 9]))]:
        ancestry.append(dict(source=name, reported_origin=kind, n=int(mask.sum()),
                             percent_source_weight=100*d.loc[mask, wt].sum()/d[wt].sum(),
                             pooled_probability_mass=d.loc[mask, 'pooled_weight'].sum()))
    z = d[d.q3_combo.eq(1)].copy()
    rows.extend(summarize(z, name, 'source_weight', 'Mexican reported origin; historical adults'))
    frames.append(d)
    audit['sources'].append(dict(source=name, raw_path=str(p), raw_sha256=digest(p), metadata_path=str(meta_path),
                                  metadata_sha256=digest(meta_path), full_n=len(d), weight=wt,
                                  full_weight_sum=float(d[wt].sum()), coefficient=benchmark/42.7,
                                  all_generation_n=d.generation.value_counts().to_dict(), mexican_n=len(z)))
combined = pd.concat(frames, ignore_index=True)
assert abs(combined.pooled_weight.sum() - 1) < 1e-12
mex = combined[combined.q3_combo.eq(1)].copy()
rows.extend(summarize(mex, 'Pooled_historical_37.8_4.9', 'pooled_weight', 'Mexican reported origin; calibrated historical adults'))
pd.DataFrame(rows).to_csv(OUT/'pew_generation_distribution.csv', index=False)
pd.DataFrame(ancestry).to_csv(OUT/'pew_origin_coverage.csv', index=False)

nlsy_path = BASE / 'nlsy_family/family_analysis_rows.csv'
nlsy = pd.read_csv(nlsy_path)
labels = {'G1_foreign_born_childhood_resident': 'G1',
          'G2_USborn_at_least_one_foreign_biological_parent': 'G2',
          'G3_USborn_USparents_foreign_grandparent': 'G3',
          'G4plus_USborn_USparents_all_four_USgrandparents': 'G4plus',
          'USborn_USparents_grandparents_unresolved': 'Unresolved', 'Generation_unresolved': 'Unresolved'}
n = nlsy[nlsy.identity.eq('Mexican_Chicano_self_ID') & nlsy.weight.gt(0)].copy()
assert n.linked_exact.isin(labels).all()
n['generation'] = n.linked_exact.map(labels)
nrows = summarize(n, 'NLSY97_positive_R21_weight', 'weight', 'Mexican/Chicano self-ID; 1980-84 birth cohort residentUS1997')
pd.DataFrame(nrows).to_csv(OUT/'nlsy_generation_distribution.csv', index=False)
audit['nlsy'] = dict(derived_path=str(nlsy_path), derived_sha256=digest(nlsy_path), n=len(n),
                    weight='U6365400/100; round21 weight from existing audited family-analysis rows',
                    limitation='Survey-retained cohort distribution, not all-age2024; birth wording includes territories inconsistently.')
audit['script_sha256'] = digest(Path(__file__))
(OUT/'audit.json').write_text(json.dumps(audit, indent=2))
print(pd.DataFrame(rows)[['source', 'generation', 'n', 'weighted_percent']].to_string(index=False))
print(pd.DataFrame(nrows)[['source', 'generation', 'n', 'weighted_percent']].to_string(index=False))
