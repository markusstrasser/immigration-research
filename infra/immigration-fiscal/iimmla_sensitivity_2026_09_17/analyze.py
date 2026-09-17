"""IIMMLA generation sensitivity; raw sources are read-only.

Source: ICPSR22627 DS0001. Definitions are tied to its codebook/questionnaire.
No sampling weights are supplied in the inspected release. All rates unweighted.
"""
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'iimmla_2026_09_17/raw/ICPSR_22627/DS0001/22627-0001-Data.tsv'


def binary_person_endpoint(gate, person):
    """Family gate: 1 yes/2 no; person: 1 respondent/2 other/3 both.

    Unknown/refused/contradictory paths stay missing; structural skip is allowed
    only after a definite no-family-event gate.
    """
    result = pd.Series(np.nan, index=gate.index, dtype=float)
    result.loc[gate.eq(2) & person.eq(-9)] = 0.0
    result.loc[gate.eq(1) & person.eq(2)] = 0.0
    result.loc[gate.eq(1) & person.isin([1, 3])] = 1.0
    return result


def analyze(source, output):
    output.mkdir(parents=True, exist_ok=True)
    d = pd.read_csv(source, sep='\t', low_memory=False)
    d.columns = d.columns.str.lower()
    required = ['ethnos10', 'generat4', 'qs7', 'qs8', 'qs10', 'qs11', 'qs12am', 'qs12bf', 'q152a', 'educred5', 'evarre', 'evpriso', 'q201', 'q202', 'q203a', 'q203b', 'gender', 'age']
    required += [f'q152b_{i}' for i in range(1, 7)] + [f'q152c_{i}' for i in range(1, 5)]
    assert set(required).issubset(d), sorted(set(required) - set(d))
    assert len(d) == 4655
    assert d.educred5.isin(range(6)).all()
    assert d.evarre.isin([0, 1]).all() and d.evpriso.isin([0, 1]).all()
    weights = [c for c in d if 'weight' in c or 'wgt' in c or c == 'wt']
    assert not weights, f'Weight-like field discovered; inspect before running: {weights}'
    mex = d.ethnos10.eq(1)
    own_us = d.qs7.isin([1, 2])
    parents_us = d.qs10.eq(1)
    # Foreign-country codes1..70, US62;71 refused/72 don't know, -9 structural.
    def foreign(s):
        return s.between(1, 70) & s.ne(62)
    parental_conflict = parents_us & (d.qs11.isin([1, 2, 3]) | foreign(d.qs12am) | foreign(d.qs12bf))
    own_conflict = own_us & foreign(d.qs8)
    base = own_us & parents_us & ~parental_conflict & ~own_conflict
    b = d[[f'q152b_{i}' for i in range(1, 5)]].copy()
    c = d[[f'q152c_{i}' for i in range(1, 5)]].copy()
    b.columns = c.columns = range(4)
    c_foreign = c.ge(1) & c.le(70) & c.ne(62)
    gp_conflict = (b.eq(1) & c.eq(62)).any(axis=1) | (b.eq(0) & c_foreign).any(axis=1)
    slots_complete = b.isin([0, 1]).all(axis=1) & b.eq(1).any(axis=1) & d.q152b_5.eq(0) & d.q152b_6.eq(0)
    generic_g3 = base & d.q152a.eq(1) & slots_complete & ~gp_conflict
    generic_g4 = base & d.q152a.eq(2) & ~b.eq(1).any(axis=1) & ~c_foreign.any(axis=1)
    mexico_gp = (b.eq(1) & c.eq(43)).any(axis=1)
    unknown_foreign_country = (b.eq(1) & ~c_foreign).any(axis=1)
    all_selected_countries_answered = (~b.eq(1) | c_foreign).all(axis=1)
    source_g3 = mex & d.generat4.eq(3)
    source_g4 = mex & d.generat4.eq(4)
    samples = {
        'source_G3_Mex_selfID': source_g3,
        'source_G4plus_Mex_selfID': source_g4,
        'positive_GP_answer_G3_before_conflict_exclusion_Mex_selfID': mex & base & d.q152a.eq(1) & slots_complete,
        'strict_generic_G3_Mex_selfID': mex & generic_g3,
        'strict_generic_G4plus_Mex_selfID': mex & generic_g4,
        'strict_MexGP_G3_Mex_selfID': mex & generic_g3 & mexico_gp,
        'strict_MexGP_G3_all_selected_countries_answered_Mex_selfID': mex & generic_g3 & mexico_gp & all_selected_countries_answered,
        'strict_MexGP_G3_any_sampled_identity': generic_g3 & mexico_gp,
        'source_G3_removed_by_strict_generic': source_g3 & ~generic_g3,
        'source_G4_removed_by_strict_generic': source_g4 & ~generic_g4,
        'strict_generic_G3_no_confirmed_MexGP_Mex_selfID': mex & generic_g3 & ~mexico_gp,
    }
    ep = pd.DataFrame(index=d.index)
    ep['BAplus'] = d.educred5.ge(4).astype(float)
    ep['no_HS'] = d.educred5.eq(0).astype(float)
    ep['arrest_supplied'] = d.evarre.astype(float)
    ep['incarceration_supplied'] = d.evpriso.astype(float)
    ep['arrest_raw'] = binary_person_endpoint(d.q201, d.q202)
    ep['incarceration_raw'] = binary_person_endpoint(d.q203a, d.q203b)
    common = ep[['BAplus', 'no_HS', 'arrest_raw', 'incarceration_raw']].notna().all(axis=1)
    rows = []
    for name, mask in samples.items():
        for sample_mode, selected in [('endpoint_available', mask), ('common_raw_endpoints', mask & common)]:
            for endpoint in ep:
                valid = selected & ep[endpoint].notna()
                n = int(valid.sum())
                events = int(ep.loc[valid, endpoint].sum())
                rows.append(dict(group=name, sample_mode=sample_mode, endpoint=endpoint, n_group=int(mask.sum()), n_selected=int(selected.sum()), n_valid=n, n_missing=int(selected.sum())-n, events=events, percent=100*events/n if n else None))
    rates = pd.DataFrame(rows)
    rates.to_csv(output/'rates.csv', index=False)
    contrasts = []
    pairs = [
        ('source', 'source_G3_Mex_selfID', 'source_G4plus_Mex_selfID'),
        ('strict_generic', 'strict_generic_G3_Mex_selfID', 'strict_generic_G4plus_Mex_selfID'),
        ('confirmed_MexGP_G3_vs_selfID_G4_ASYMMETRIC', 'strict_MexGP_G3_Mex_selfID', 'strict_generic_G4plus_Mex_selfID'),
    ]
    for label, third, fourth in pairs:
        for mode in rates.sample_mode.unique():
            for endpoint in ep:
                g3 = rates[(rates.group == third) & (rates.sample_mode == mode) & (rates.endpoint == endpoint)].iloc[0]
                g4 = rates[(rates.group == fourth) & (rates.sample_mode == mode) & (rates.endpoint == endpoint)].iloc[0]
                contrasts.append(dict(comparison=label, sample_mode=mode, endpoint=endpoint, G3_n=int(g3.n_valid), G4_n=int(g4.n_valid), G3_percent=g3.percent, G4_percent=g4.percent, G4_minus_G3_pp=g4.percent-g3.percent))
    pd.DataFrame(contrasts).to_csv(output/'contrasts.csv', index=False)
    class_label = pd.Series('unresolved_or_conflicting', index=d.index)
    class_label.loc[~own_us | ~parents_us] = 'not_confirmed_USborn_USparents'
    class_label.loc[generic_g3] = 'strict_generic_G3'
    class_label.loc[generic_g4] = 'strict_generic_G4plus'
    pd.crosstab(d.loc[mex, 'generat4'], class_label[mex]).to_csv(output/'source_to_strict_counts.csv')
    audit = {
        'source': str(source), 'source_bytes': source.stat().st_size,
        'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'source_rows': len(d), 'weights': 'unweighted; no source weight variable found',
        'definitions': {
            'base': 'QS7=1/2; QS10=1; no contradictory QS8/QS11/QS12 country report',
            'strict_G3': 'base + Q152A=1 + complete Q152B1..4 flags with at least one foreign + B5/B6=0 + no country/nativity conflict',
            'strict_G4plus': 'base + Q152A=2 + no positive foreign grandparent flag or foreign grandparent country',
            'MexGP': 'at least one matched Q152B_i=1 and Q152C_i=43; not inferred from ETHNOS10',
            'G4_origin_limit': 'No Mexican-born GP is possible under this rule; Mexican origin is self-identification only. No exact-country symmetric G3/G4 lineage comparison is identified.',
            'raw_arrest': 'Q201/Q202; lifetime respondent arrest; unknown/refused remains missing',
            'raw_incarceration': 'Q203A/Q203B; lifetime reform school/detention/jail/prison; not adult-only',
            'BAplus': 'EDUCRED5>=4 (documented supplied credential variable)',
            'no_HS': 'EDUCRED5=0',
        },
        'sample_counts': {k:int(v.sum()) for k,v in samples.items()},
        'source_G3_Q152A': d.loc[source_g3,'q152a'].value_counts().to_dict(),
        'source_G4_Q152A': d.loc[source_g4,'q152a'].value_counts().to_dict(),
        'source_G3_own_QS7': d.loc[source_g3,'qs7'].value_counts().to_dict(),
        'source_G4_own_QS7': d.loc[source_g4,'qs7'].value_counts().to_dict(),
        'Mex_selfID_source_G3plus_parent_conflicts': int(((source_g3|source_g4)&parental_conflict).sum()),
        'Mex_selfID_source_G3plus_gp_conflicts': int(((source_g3|source_g4)&gp_conflict).sum()),
        'strict_Mex_selfID_G3_any_unresolved_foreign_country': int((mex&generic_g3&unknown_foreign_country).sum()),
        'strict_MexGP_G3_any_unresolved_foreign_country': int((mex&generic_g3&mexico_gp&unknown_foreign_country).sum()),
        'strict_no_MexGP_known_other_foreign_countries': int((mex&generic_g3&~mexico_gp&all_selected_countries_answered).sum()),
        'strict_no_MexGP_with_unresolved_foreign_country': int((mex&generic_g3&~mexico_gp&unknown_foreign_country).sum()),
        'MexGP_G3_sampled_ethnicity_codes': d.loc[generic_g3&mexico_gp,'ethnos10'].value_counts().to_dict(),
        'endpoint_audit': {},
    }
    focal = source_g3 | source_g4
    for kind in ['arrest', 'incarceration']:
        raw, supplied = ep[f'{kind}_raw'], ep[f'{kind}_supplied']
        audit['endpoint_audit'][kind] = {
            'focal_raw_unknown': int((focal&raw.isna()).sum()),
            'focal_unknown_supplied_zero': int((focal&raw.isna()&supplied.eq(0)).sum()),
            'focal_unknown_supplied_one': int((focal&raw.isna()&supplied.eq(1)).sum()),
            'focal_known_disagreements': int((focal&raw.notna()&raw.ne(supplied)).sum()),
            'all_known_disagreements': int((raw.notna()&raw.ne(supplied)).sum()),
        }
    composition = []
    for name, mask in samples.items():
        for mode, selected in [('endpoint_available',mask),('common_raw_endpoints',mask&common)]:
            composition.append(dict(group=name,sample_mode=mode,n=int(selected.sum()),men=int((selected&d.gender.eq(1)).sum()),women=int((selected&d.gender.eq(0)).sum()),age_mean=float(d.loc[selected,'age'].mean()),age_min=int(d.loc[selected,'age'].min()),age_max=int(d.loc[selected,'age'].max())))
    pd.DataFrame(composition).to_csv(output/'composition.csv',index=False)
    subgroup_rows = []
    principal = ['source_G3_Mex_selfID','source_G4plus_Mex_selfID','strict_generic_G3_Mex_selfID','strict_generic_G4plus_Mex_selfID','strict_MexGP_G3_Mex_selfID']
    for name in principal:
        for age_rule in ['20to40','25to40']:
            age_mask = d.age.between(20 if age_rule == '20to40' else 25,40)
            for sex, sex_mask in [('All',pd.Series(True,index=d.index)),('Men',d.gender.eq(1)),('Women',d.gender.eq(0))]:
                selected = samples[name] & common & age_mask & sex_mask
                for endpoint in ['BAplus','no_HS','arrest_raw','incarceration_raw']:
                    n = int(selected.sum())
                    events = int(ep.loc[selected,endpoint].sum())
                    subgroup_rows.append(dict(group=name,age_rule=age_rule,sex=sex,endpoint=endpoint,n=n,events=events,percent=100*events/n if n else None))
    pd.DataFrame(subgroup_rows).to_csv(output/'subgroup_rates.csv',index=False)
    assert all(v['focal_known_disagreements'] == 0 for v in audit['endpoint_audit'].values())
    assert not (generic_g3 & generic_g4).any()
    assert not (samples['strict_MexGP_G3_Mex_selfID'] & ~samples['strict_generic_G3_Mex_selfID']).any()
    # Anchors independently recomputed in the preceding audit. Detect source drift.
    assert (int(source_g3.sum()), int(source_g4.sum())) == (212, 189)
    assert int(d.loc[source_g3, 'evarre'].sum()) == 64
    assert int(d.loc[source_g4, 'evarre'].sum()) == 38
    (output/'audit.json').write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))
    print(pd.DataFrame(contrasts).to_string(index=False))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--output-dir', type=Path, default=HERE/'derived')
    args = parser.parse_args()
    resolved = args.output_dir.resolve()
    if not (resolved.is_relative_to(HERE/'derived') or resolved.is_relative_to(Path('/private/tmp'))):
        raise ValueError('Outputs must remain in this lane derived directory or /private/tmp')
    analyze(args.source, args.output_dir)
