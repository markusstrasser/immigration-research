"""Independent source-semantic checks and table arithmetic for family analysis."""
import argparse,json,math,re
from pathlib import Path
import pandas as pd
P=argparse.ArgumentParser();P.add_argument('--lane-dir',type=Path,default=Path(__file__).resolve().parents[1])
P.add_argument('--output-dir',type=Path,default=Path(__file__).resolve().parents[1]/'derived/nlsy_family');A=P.parse_args();O=A.output_dir
raw=pd.read_csv(O/'parent_linkage_raw.csv').set_index('R0000100');b=pd.read_csv(A.lane_dir/'derived/nlsy/full_selected_data.csv').set_index('R0000100')
out=pd.read_csv(O/'family_analysis_rows.csv').set_index('R0000100');s=pd.read_csv(O/'parent_nativity_sources.csv')
checks={};assert raw.index.equals(b.index) and raw.index.equals(out.index)
assert len(raw)==8984 and raw.index.is_unique
codebook=json.loads((O/'parent_linkage_codebook.json').read_text())
for slot in range(1,17):
    block=codebook[f'R{11009+slot:05}00']
    positive_codes={int(m[2]):int(m[1]) for line in block.splitlines() if (m:=re.fullmatch(r'\s*(\d+)\s+(\d+)\s*',line)) and int(m[1])>0 and int(m[2])>0}
    ids=raw[f'R{11009+slot:05}00'];assert ids[ids>0].value_counts().to_dict()==positive_codes
checks['HHI2_ID_codebook_marginals_checked']=16
# Independently verify each accepted source's identity with the original roster.
for x in s.itertuples(index=False):
    r=raw.loc[x.caseid];parent=x.parent
    member=('R0533600' if parent=='mother' else 'R0532300') if x.mapping=='corrected_youth_HHI2' else ('R0733200' if parent=='mother' else 'R0731900')
    nonmember=('R0535100' if parent=='mother' else 'R0535000') if x.mapping=='corrected_youth_HHI2' else ('R0734600' if parent=='mother' else 'R0734500')
    sex=2 if parent=='mother' else 1
    if x.source.startswith('responding'):
        assert r.R0734800==(3 if parent=='mother' else 4)
        assert r.R0735000>0 and r.R0735000==r[member]
        assert x.us_born==r.R0551500
    elif x.source.startswith('spouse'):
        assert r.R0735000>0 and r[member]>0
        if x.mapping=='corrected_youth_HHI2':
            slots=[j for j in range(1,17) if r[f'R{11009+j:05}00']==r.R0735000]
            assert len(slots)==1
            position=slots[0]
            candidates=[r[f'R{11556+position:05}00'],r[f'R{11137+position:05}00']]
            ids={v for v in candidates if v>0}
            assert len(ids)==1 and r[member] in ids
        else:
            slots=[j for j in range(1,10) if r[f'R{7036+j:05}00']==r.R0735000]
            assert len(slots)==1 and r[f'R{7295+slots[0]:05}00']==r[member]
        assert x.us_born==r.R0555000
    elif x.source.startswith('nonresponding'):
        if x.source.startswith('nonresponding_1'):identity,inhh,sexvar,value='R0733400','R0733500','R0733700','R0559500'
        else:identity,inhh,sexvar,value='R0733900','R0734000','R0734200','R0559600'
        assert r[inhh] in (0,1) and r[identity]>0 and r[sexvar]==sex
        assert r[identity]==r[member if r[inhh]==1 else nonmember]
        assert x.us_born==r[value]
    else:
        assert x.source=='supplemental_'+('Z0501800' if parent=='mother' else 'Z0502000')
        assert x.us_born==b.loc[x.caseid,x.source.removeprefix('supplemental_')]
checks['accepted_source_records_rechecked']=len(s)
for parent in ['mother','father']:
    z=s[s.parent.eq(parent)&s.mapping.eq('corrected_youth_HHI2')].groupby('caseid').us_born.agg(lambda x:set(x))
    expected=z.map(lambda v:next(iter(v)) if len(v)==1 else float('nan')).reindex(out.index)
    assert expected.equals(out[parent+'_us'])
    checks[parent+'_conflict_count']=int(z.map(len).eq(2).sum())
# Raw codebook marginals independently bound the input interpretation.
for field,expected in [('R0551500',{0:1182,1:6754}),('R0555000',{0:908,1:4299}),('R0559500',{0:257,1:2037}),('R0559600',{0:37,1:245})]:
    assert raw[field][raw[field].isin([0,1])].value_counts().to_dict()==expected
checks['codebook_marginals_checked']=4
old=pd.read_csv(A.lane_dir/'derived/nlsy/analysis_rows.csv').set_index('R0000100')
assert old.index.equals(out.index)
assert out['incarceration'].equals(old.incarc_reported)
assert out['arrest'].equals(old.arrest_reported)
# Supplemental estimator must reproduce previous classifications exactly,
# except the deliberately separated known-US-parent/unknown-grandparent group.
mapping={'G1_foreign_born_childhood_resident':'Foreign_born_childhood_resident',
'G2_USborn_at_least_one_foreign_biological_parent':'G2_known_biological_parent_foreign',
'G3_USborn_USparents_foreign_grandparent':'G3_known_US_parents_foreign_grandparent',
'G4plus_USborn_USparents_all_four_USgrandparents':'G4plus_known_US_parents_and_grandparents',
'USborn_USparents_grandparents_unresolved':'Generation_unresolved','Generation_unresolved':'Generation_unresolved'}
assert out.supplemental_exact.map(mapping).equals(old.strict_generation)
checks['old_supplemental_classification_reproduced']=True
n_tables=0;n_cells=0
for filename in ['linked_exact_outcomes.csv','linked_coarse_outcomes.csv','supplemental_exact_outcomes.csv','supplemental_coarse_outcomes.csv','roster_only_exact_outcomes.csv','roster_only_coarse_outcomes.csv','parent_roster_exact_outcomes.csv','parent_roster_coarse_outcomes.csv','linked_comparison_outcomes.csv']:
    t=pd.read_csv(O/filename);groupcols=['sex','comparison' if 'comparison' in filename else 'identity']
    groupcols += [next(c for c in t if c.endswith(('_exact','_coarse')))]
    assert t[t.outcome=='incarceration'].baseline_n.sum()==8984
    for rec in t.to_dict('records'):
        g=out
        for col in groupcols:g=g[g[col].eq(rec[col])]
        v=g[(g.weight>0)&g[rec['outcome']].notna()]
        denom=sum(float(w) for w in v.weight)
        rate=100*sum(float(r.weight)*float(r[rec['outcome']]) for _,r in v.iterrows())/denom if denom else float('nan')
        assert len(g)==rec['baseline_n'] and len(v)==rec['outcome_n'] and int(v[rec['outcome']].sum())==rec['events']
        assert (math.isnan(rate) and math.isnan(rec['weighted_percent'])) or math.isclose(rate,rec['weighted_percent'],rel_tol=1e-12,abs_tol=1e-12)
        n_cells+=1
    n_tables+=1
checks['independent_weighted_cells']=n_cells;checks['tables']=n_tables;checks['verdict']='PASS'
(O/'verification.json').write_text(json.dumps(checks,indent=2));print(json.dumps(checks,indent=2),flush=True)
