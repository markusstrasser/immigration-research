from pathlib import Path
import argparse, hashlib, json, subprocess, sys
import numpy as np
import pandas as pd
import pyreadstat

ap = argparse.ArgumentParser()
ap.add_argument('--raw-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'raw')
ap.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'derived/pew')
args = ap.parse_args()
root = args.output_dir
if not (root / 'manifest.json').exists():
    subprocess.run([sys.executable, str(Path(__file__).with_name('probe.py')), '--raw-dir', str(args.raw_dir), '--output-dir', str(root)], check=True)
manifest = json.loads((root / 'manifest.json').read_text())
assert len(manifest) == 8
records, dictionary, frames = [], {}, []
for rec in manifest:
    archive = args.raw_dir / Path(rec['archive']).name
    assert hashlib.sha256(archive.read_bytes()).hexdigest() == rec['sha256'], f'Archive mismatch: {archive}'
    kwargs = {'encoding': rec['encoding']} if rec['encoding'] != 'readstat-auto' else {}
    d, m = pyreadstat.read_sav(rec['sav'], user_missing=True, **kwargs)
    dictionary[archive.name] = {'n': len(d), 'focus': rec['focus'], 'encoding': rec['encoding'], 'weight_stats': {}}
    for w in ['weight', 'weights', 'OMNIWeight', 'totalwt', 'form06wt', 'form12ncowt']:
        if w in d:
            dictionary[archive.name]['weight_stats'][w] = {'sum': float(d[w].sum()), 'min': float(d[w].min()), 'max': float(d[w].max()), 'nonmissing': int(d[w].notna().sum())}
    if '2015-National' not in archive.name and 'Self-Identified' not in archive.name:
        continue
    identified = '2015-National' in archive.name
    d['survey'] = 'NSL2015' if identified else 'nonHispanic2015_16'
    d['identified'] = int(identified)
    d['w'] = d['weights' if identified else 'OMNIWeight']
    assert (d.w > 0).all() and d.w.notna().all()
    d['pooled_w'] = d.w / d.w.sum() * (0.89 if identified else 0.11)
    d['pooled_counts_w'] = d.w / d.w.sum() * ((37.8 if identified else 4.9) / 42.7)
    rawgen = d.immgen.copy()
    d['immgen'] = np.where(d.q4 == 2, 8.0, 9.0)
    d.loc[d.q4.isin([1,3]), 'immgen'] = 1
    us = d.q4 == 2
    d.loc[us & (d.q7.isin([1,3]) | d.q8.isin([1,3])), 'immgen'] = 2
    usparents = us & (d.q7 == 2) & (d.q8 == 2)
    gps = d[['q8aa','q8ab','q8ba','q8bb']]
    d.loc[usparents & gps.isin([1,3]).any(axis=1), 'immgen'] = 3
    d.loc[usparents & (gps == 2).all(axis=1), 'immgen'] = 4
    dictionary[archive.name]['generation_audit'] = {'raw_counts':rawgen.value_counts(dropna=False).to_dict(), 'rebuilt_counts':d.immgen.value_counts(dropna=False).to_dict(), 'n_disagree':int((rawgen != d.immgen).sum()), 'rule':'Puerto Rico counts as migrant origin for Pew comparability; q4/q7/q8 and four q8 grandparent fields; unknown preserved'}
    assert (d.immgen == 1).sum() == d.q4.isin([1,3]).sum()
    assert (d.immgen.isin([1,2,3,4])).sum() > 0, 'Generation is wholly unknown despite available nativity fields'
    p1, p2 = ('q10a', 'q10b') if identified else ('ha2a', 'ha2b')
    d['parent_h_count'] = d[p1].map({1:1, 2:0}) + d[p2].map({1:1, 2:0})
    d['grandparent_h_count'] = d.q11a.map({1:1, 2:2, 3:0, 4:0}) + d.q11b.map({1:1, 2:2, 3:0, 4:0})
    for name, var, yes, valid in [('typical_american', 'q14', [1], [1,2]), ('democrat_id', 'party', [2], [1,2,3,4,5]), ('democrat_or_lean', 'party_combo', [2], [1,2,3]), ('ancestry_essential', 'q16c' if identified else 'q16cx', [1], [1,2,3,4])]:
        d[name] = d[var].isin(yes).astype(float).where(d[var].isin(valid))
        dictionary[archive.name].setdefault('analysis_variables', {})[var] = {'label':m.column_names_to_labels[var], 'values':m.variable_value_labels.get(var), 'user_missing':m.missing_ranges.get(var)}
    frames.append(d)
    for key in ['immgen','q14','q22','ha_combo','parent_h_count','grandparent_h_count','q16c','q16cx']:
        if key in d:
            for value in sorted(d[key].dropna().unique()):
                records.append({'survey':d.survey.iloc[0], 'variable':key, 'value':float(value), 'n':int((d[key] == value).sum()), 'weighted_pct_all':float(100*d.loc[d[key] == value,'w'].sum()/d.w.sum())})
all_d = pd.concat(frames, ignore_index=True)
rows = []
def tab(d, source, group, weight):
    for outcome in ['identified','typical_american','democrat_id','democrat_or_lean','ancestry_essential']:
        z = d.loc[d[outcome].notna()]
        if not len(z):
            continue
        w = z[weight]
        rows.append({'source':source,'group':group,'outcome':outcome,'n_total':len(d),'n_valid':len(z),'n_missing':len(d)-len(z),'weighted_pct':float(100*np.average(z[outcome],weights=w)),'n_eff_kish':float(w.sum()**2/(w*w).sum()),'weighted_missing_pct':float(100*d.loc[d[outcome].isna(),weight].sum()/d[weight].sum())})
for source in ['NSL2015', 'nonHispanic2015_16', 'pooled_89_11', 'pooled_counts']:
    d = all_d if source.startswith('pooled') else all_d.loc[all_d.survey == source]
    weight = 'pooled_w' if source.startswith('pooled') else 'w'
    if source == 'pooled_counts':
        weight = 'pooled_counts_w'
    groups = {'all':np.ones(len(d),dtype=bool), 'gen3plus':d.immgen.isin([3,4])}
    for g in range(1,5):
        groups[f'gen{g}'] = d.immgen == g
    for p in range(3):
        groups[f'parents_hispanic_{p}'] = d.parent_h_count == p
    for g in range(5):
        groups[f'grandparents_hispanic_{g}'] = d.grandparent_h_count == g
    for group, mask in groups.items():
        if np.any(mask):
            tab(d.loc[mask],source,group,weight)
pd.DataFrame(rows).to_csv(root/'results.csv',index=False)
pd.DataFrame(records).to_csv(root/'distributions.csv',index=False)
(root/'survey_dictionary.json').write_text(json.dumps(dictionary,indent=2))
(root/'analysis_notes.json').write_text(json.dumps({'pooling':'append separate surveys; external fixed 89/11 calibration plus published-count sensitivity 37.8m/4.9m; not estimated prevalence','inference':'descriptive weighted proportions; Kish effective n is not a survey-design confidence interval','grandparent_map':{'1':1,'2':2,'3':0,'4':0},'missing':'8/9 excluded; structural NaN excluded; no codes silently treated as zero','archive_hashes_verified':len(manifest)},indent=2))
out = pd.DataFrame(rows)
with (root/'generated_tables.md').open('w') as f:
    f.write('# Reproduced descriptive tables\n\n')
    for source in ['NSL2015','nonHispanic2015_16','pooled_89_11','pooled_counts']:
        f.write(f'## {source}\n\n| Group | Outcome | n valid / total | Weighted percent | Kish effective n |\n|---|---|---:|---:|---:|\n')
        for r in rows:
            if r['source'] == source and r['group'] in ['all','gen1','gen2','gen3','gen4','grandparents_hispanic_1','grandparents_hispanic_4']:
                f.write(f"| {r['group']} | {r['outcome']} | {r['n_valid']} / {r['n_total']} | {r['weighted_pct']:.2f} | {r['n_eff_kish']:.1f} |\n")
        f.write('\n')
print(out.loc[out.group.isin(['all','gen3','gen4','grandparents_hispanic_1','grandparents_hispanic_4'])].to_string(index=False))
print(pd.DataFrame(records).query('variable == "q22" or variable == "ha_combo"').to_string(index=False))
