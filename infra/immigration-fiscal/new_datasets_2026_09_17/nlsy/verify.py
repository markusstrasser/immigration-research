import argparse,json,pathlib,pandas as pd,numpy as np
p=argparse.ArgumentParser();p.add_argument('--output-dir',type=pathlib.Path,default=pathlib.Path(__file__).resolve().parents[1]/'derived/nlsy');o=p.parse_args().output_dir
j=json.loads((o/'join_and_coverage.json').read_text());assert j['full']['unique_ids']==j['supplied']['unique_ids']==8984
assert not any(j['supplied_overlap'].values());assert not any(j['profile_source_cache']['mismatches'].values());assert j['ability']['sex_disagreements']==0
d=pd.read_csv(o/'full_selected_data.csv').set_index('R0000100');a=pd.read_csv(o/'analysis_rows.csv').set_index('R0000100')
parent=pd.read_csv(o/'parent_supplement.csv').set_index('R0000100')
assert len(parent.columns)==10 and set(parent.columns).issubset(d.columns)
pd.testing.assert_frame_equal(parent.sort_index(),d[parent.columns].sort_index())
assert a.loc[d.E8043100.lt(0),'incarc_reported'].isna().all()
assert a.loc[d.Z0501800.lt(0)&d.Z0502000.lt(0),'strict_generation'].isin(['Generation_unresolved','Foreign_born_childhood_resident']).all()
required=['t1_self_identity.csv','t2_USborn_grandparent_history.csv','t3_strict_generation.csv','t4_parent_region_vs_identity.csv','t5_USborn_parent_region_GP.csv','t6_NHWhite_comparison.csv']
assert all((o/name).is_file() for name in required), 'Incomplete set of analysis tables'
for f in [o/name for name in required]:
    t=pd.read_csv(f);assert (t.events<=t.n_observed).all();assert (t.n_group==t.n_observed+t.missing).all();assert t.weighted_percent.dropna().between(0,100).all()
mask=a.sex.eq('Men')&a.mexican_self_id.eq('Mexican_Chicano_self_ID')&a.weight.gt(0);v=a[mask].dropna(subset=['incarc_reported'])
t=pd.read_csv(o/'t1_self_identity.csv');row=t[t.sex.eq('Men')&t.mexican_self_id.eq('Mexican_Chicano_self_ID')&t.outcome.eq('incarc_reported')].iloc[0]
assert row.n_observed==len(v);assert np.isclose(row.weighted_percent,100*np.average(v.incarc_reported,weights=v.weight))
tags=json.loads((o/'tagset_coverage.json').read_text());assert tags['overlap']==6795 and tags['standalone_not_exported']==9211
assert tags['key_variables']['E8043100']==dict(in_export=False,in_standalone=True)
assert tags['key_variables']['S7639500']==dict(in_export=False,in_standalone=False)
code=(o/'audited_selected_codebook.txt').read_text();assert 'not restricted to biological parents' in code;assert '2 implied decimal' in code
print('PASS: unique joins, overlap drift probes, skipped-parent and missing-outcome semantics, table denominators, direct weighted-rate recomputation, tagset membership, codebook guards')
