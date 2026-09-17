"""Describe authorized LNS derivatives without reconstructing IDs or merging people."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

SHAPES = {'27113': (8561,49), 'SZK4NF': (8634,30), '1KWH3E': (7688,22)}
GENERATIONS = {0:'Author first-generation noncitizen', 1:'Author first-generation citizen', 2:'Author second generation', 3:'Author third generation', 4:'Author fourth-plus generation'}
POLICIES = {1:'Immediate legalization', 2:'Guest worker leading to legalization', 3:'Temporary guest worker', 4:'Close/seal border', 5:'None of these'}

def clean(x):
    if isinstance(x, dict):
        return {str(k):clean(v) for k,v in x.items()}
    if isinstance(x, (list, tuple)):
        return [clean(v) for v in x]
    if isinstance(x, np.generic):
        return clean(x.item())
    if isinstance(x, float) and not np.isfinite(x):
        return None
    return x

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input-dir', type=Path, required=True)
    parser.add_argument('--output-dir', type=Path, required=True)
    args = parser.parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(Path(__file__).with_name('source_manifest.json').read_text())
    inputs = {f['study_key']:f for f in manifest['files'] if f['role']=='participant_data'}
    assert set(inputs)==set(SHAPES), 'Unexpected replication inventory'
    frames, coverage, idsets = {}, {}, {}
    for study, (rows, cols) in SHAPES.items():
        filename = inputs[study]['destination_relative_path']
        path = args.input_dir / filename
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == inputs[study]['sha256'], f'Unexpected input version: {path}'
        with pd.io.stata.StataReader(path, convert_categoricals=False) as reader:
            variable_labels = reader.variable_labels()
            value_labels = reader.value_labels()
            frame = reader.read()
        assert frame.shape == (rows, cols), (study, frame.shape)
        frames[study] = frame
        ids = [c for c in frame if c.lower() in ('caseid','respid')]
        idreport = {}
        for column in ids:
            values = frame[column]
            nonmissing = values.notna() & values.astype(str).str.strip().ne('')
            idreport[column] = {'nonmissing':int(nonmissing.sum()), 'unique':int(values[nonmissing].nunique()), 'duplicate_nonmissing_rows':int(values[nonmissing].duplicated().sum()), 'dtype':str(values.dtype)}
            idsets[(study, column)] = set(values[nonmissing].astype(str))
        coverage[study] = dict(file=filename, sha256=digest, shape=list(frame.shape), columns=list(frame.columns), variable_labels=variable_labels, value_labels=value_labels, missing=frame.isna().sum().to_dict(), all_missing_rows=int(frame.isna().all(axis=1).sum()), ids=idreport)
    # No identifier appears in either Branton or Perez; never join by row order.
    assert not coverage['27113']['ids'] and not coverage['1KWH3E']['ids']
    assert coverage['SZK4NF']['ids']['respid']['unique'] == 8634
    join_report = {'cross_package_id_overlap':'Not measurable: only SZK4NF exposes respondent ID.', 'joins_performed':0, 'fabricated_ids':False}
    w = frames['SZK4NF']
    coverage['SZK4NF']['partyid7_frequency'] = w.partyid7.value_counts(dropna=False).to_dict()
    coverage['SZK4NF']['weight_columns'] = [c for c in w if 'weight' in c.lower() or c.lower().startswith('wt_')]
    p = frames['1KWH3E']
    coverage['1KWH3E']['party_indicator_sum'] = p[['dems','reps','indys','noparty']].sum(axis=1).value_counts().to_dict()
    coverage['1KWH3E']['generation_indicator_sum'] = p[['second','third']].sum(axis=1).value_counts().to_dict()
    coverage['1KWH3E']['weight_summary'] = p.weight.describe().to_dict()
    origin_cols = ['cuban','puerto','dominic','salva']
    assert p[origin_cols].isin([0,1]).all().all()
    assert p[origin_cols].sum(axis=1).le(1).all()
    coverage['1KWH3E']['origin_counts'] = {c:int(p[c].sum()) for c in origin_cols}
    coverage['1KWH3E']['origin_counts']['Mexican_residual_documented_five_origin_sample'] = int(p[origin_cols].sum(axis=1).eq(0).sum())
    b = frames['27113']
    b['wt_nation_rev'] = b.wt_nation_rev.astype(float)
    nonblank = ~b.isna().all(axis=1)
    valid_weight = b.wt_nation_rev.notna() & np.isfinite(b.wt_nation_rev) & b.wt_nation_rev.gt(0)
    valid_generation = b.generation.isin(GENERATIONS)
    valid_policy = b.immpolinew.isin(POLICIES)
    assert valid_weight.equals(nonblank)
    assert valid_policy.equals(nonblank)
    assert int(nonblank.sum()) == 8212
    assert int((nonblank & ~valid_generation).sum()) == 43
    assert set(b.generation.dropna().unique()) == set(GENERATIONS)
    valid = valid_weight & valid_generation & valid_policy
    coverage['27113']['denominators'] = {'physical_rows':len(b), 'all_missing_rows':int((~nonblank).sum()), 'nonblank_positive_weight_and_policy':int(nonblank.sum()), 'generation_missing_among_nonblank':int((nonblank & ~valid_generation).sum()), 'table_rows':int(valid.sum()), 'nonblank_weight_sum':float(b.loc[nonblank,'wt_nation_rev'].sum()), 'table_weight_sum':float(b.loc[valid,'wt_nation_rev'].sum()), 'missing_generation_weight':float(b.loc[nonblank & ~valid_generation,'wt_nation_rev'].sum())}
    rows = []
    for code, label in GENERATIONS.items():
        x = b.loc[valid & b.generation.eq(code)]
        weights = x.wt_nation_rev.astype(float)
        denom = float(weights.sum())
        row = {'generation_code':code, 'generation_label':label, 'unweighted_n':len(x), 'sum_weight':denom, 'kish_weight_only_n':float(denom**2 / (weights**2).sum())}
        for policy, policy_label in POLICIES.items():
            match = x.immpolinew.eq(policy)
            row[f'policy_{policy}_weighted_pct'] = float(100*weights[match].sum()/denom)
            row[f'policy_{policy}_unweighted_pct'] = float(100*match.mean())
        assert abs(sum(row[f'policy_{i}_weighted_pct'] for i in POLICIES)-100)<1e-8
        rows.append(row)
    table = pd.DataFrame(rows)
    table.to_csv(args.output_dir/'generation_policy.csv',index=False)
    global_distribution = {str(i):float(100*b.loc[nonblank & b.immpolinew.eq(i),'wt_nation_rev'].sum()/b.loc[nonblank,'wt_nation_rev'].sum()) for i in POLICIES}
    result = dict(coverage=coverage, join_report=join_report, table=rows, policy_labels=POLICIES, global_policy_weighted_pct=global_distribution, interpretation='Descriptive within author-supplied 2006 derivative; no causal, contemporary population, exact-lineage or non-Hispanic-descendant inference.')
    (args.output_dir/'analysis.json').write_text(json.dumps(clean(result),indent=2,allow_nan=False))
    print(json.dumps(clean({'denominators':coverage['27113']['denominators'], 'table':rows, 'global':global_distribution, 'ids':coverage['SZK4NF']['ids'], 'join_report':join_report}),indent=2,allow_nan=False))

if __name__ == '__main__':
    main()
