"""Prospective adjusted associations and selection falsifications, not causal IV."""
import json
import argparse
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--data-dir', type=Path, default=ROOT / '_cache')
parser.add_argument('--out', type=Path, default=ROOT / 'derived')
args = parser.parse_args()
args.out.mkdir(parents=True, exist_ok=True)
manifest = json.loads((args.data_dir / 'probe.json').read_text())
lock = json.loads((ROOT / 'sources.json').read_text())
for field in ['data_sha256', 'dictionary_sha256', 'data_bytes']:
    if manifest[field] != lock[field]:
        raise ValueError('Source manifest mismatch: ' + field)
selected = args.data_dir / 'selected.parquet'
if hashlib.sha256(selected.read_bytes()).hexdigest() != manifest['selected_sha256']:
    raise ValueError('Selected data changed after extraction')
df = pd.read_parquet(selected)
if len(df) != 21409 or df.CHILDID.duplicated().any():
    raise ValueError('Unexpected extracted rows or duplicate child IDs')

def require(test, message):
    if not test:
        raise ValueError(message)

def numeric(name):
    return pd.to_numeric(df[name], errors='raise')

def positive(name):
    values = numeric(name)
    return values.where(values >= 0)

def valid_id(name):
    values = df[name].astype(str)
    return values.where(values.str.fullmatch(r'\d{4}') & ~values.str.startswith('999'))

def language_count(language, lep_name, count_name):
    any_other, lep, count = numeric(language), numeric(lep_name), numeric(count_name)
    # Skip rules: no non-English language OR no LEP -> zero; other negatives unknown.
    out = count.where((lep == 1) & (count >= 0))
    out = out.mask((any_other == 2) | (lep == 2), 0)
    require(not ((any_other == 2) & (lep == 1)).any(), 'Contradictory language gates')
    require(not (((any_other == 2) | (lep == 2)) & (count > 0)).any(), 'Positive count contradicts zero gate')
    return out

df['ell1'] = language_count('A1OTLAN', 'A1LEP', 'A1NUMLE')
# Round 4 used separate forms for kindergarten and non-kindergarten classes.
# Harmonize them instead of selecting children on progression after baseline.
k_form = numeric('A4CLASS').isin([1, 2, 3])
non_k_form = numeric('A4CLASS') == 4
df['ell4'] = language_count('A4OTLA', 'A4LEP', 'A4NUMLE').where(non_k_form)
df.loc[k_form, 'ell4'] = language_count('A4KOTLA', 'A4KLEP', 'A4KNUML')[k_form]
for wave in [1, 4]:
    df[f'school{wave}'] = valid_id(f'S{wave}_ID')
    df[f'size{wave}'] = positive(f'A{wave}TOTRA')
    df[f'white{wave}'] = positive(f'A{wave}WHITE')
    if wave == 4:
        df['size4'] = df['size4'].where(non_k_form)
        df['white4'] = df['white4'].where(non_k_form)
        df.loc[k_form, 'size4'] = positive('A4KTOTR')[k_form]
        df.loc[k_form, 'white4'] = positive('A4KWHIT')[k_form]
    df[f'ell{wave}'] = df[f'ell{wave}'].where(df[f'ell{wave}'] <= df[f'size{wave}'])
    df[f'ell10pp{wave}'] = df[f'ell{wave}'] / df[f'size{wave}'] * 10
    df[f'anyell{wave}'] = (df[f'ell{wave}'] > 0).astype(float).where(df[f'ell{wave}'].notna())
    df[f'nonwhite10pp{wave}'] = (1-df[f'white{wave}']/df[f'size{wave}'])*10
    df[f'allwhite{wave}'] = (df[f'white{wave}'] == df[f'size{wave}']).astype(float).where(df[f'white{wave}'].notna())
    bad_size = ~df[f'size{wave}'].between(5, 45) | (df[f'white{wave}'] > df[f'size{wave}'])
    df.loc[bad_size, [f'ell10pp{wave}', f'anyell{wave}', f'nonwhite10pp{wave}', f'allwhite{wave}']] = np.nan
df['ses'] = numeric('WKSESL').where(numeric('WKSESL') > -8)
df['female'] = numeric('GENDER').map({1: 0, 2: 1})
df['age1'] = positive('R1_KAGE') / 12
df['duration_k'] = (positive('R2_KAGE') - positive('R1_KAGE')) / 12
df['duration_g1'] = (positive('R4AGE') - positive('R2_KAGE')) / 12
native_white_english = (numeric('RACE') == 1) & (numeric('P2CHPLAC') == 1) & (numeric('WKLANGST') == 2)
timing_qa = {}
for duration, upper in [('duration_k', 1), ('duration_g1', 2)]:
    invalid = df[duration].notna() & ~df[duration].between(0, upper, inclusive='neither')
    timing_qa[duration] = {'invalid_all_children': int(invalid.sum()), 'invalid_target_children': int((invalid & native_white_english).sum()), 'allowed_years_exclusive': [0, upper]}
    df.loc[invalid, duration] = np.nan
scales = {}
for domain, suffix in [('reading', 'RSCL'), ('math', 'MSCL')]:
    for wave in [1, 2, 4]:
        score = positive(f'C{wave}R4{suffix}')
        reference_weight = numeric(f'C{wave}WEIGHT')
        ref = score.notna() & (reference_weight > 0)
        mean = np.average(score[ref], weights=reference_weight[ref])
        sd = np.sqrt(np.average((score[ref]-mean)**2, weights=reference_weight[ref]))
        scales[f'{domain}{wave}'] = {'mean': float(mean), 'sd': float(sd), 'reference': f'C{wave}WEIGHT-positive observed scores, all origins'}
        df[f'{domain}{wave}'] = (score-mean)/sd
        for power in [2, 3]:
            df[f'{domain}{wave}_{power}'] = df[f'{domain}{wave}']**power
controls = ['ses','female','age1']
baseline1 = ['reading1','reading1_2','reading1_3','math1','math1_2','math1_3']
baseline2 = ['reading2','reading2_2','reading2_3','math2','math2_2','math2_3']

def fit(sample, outcome, exposure, covariates, weight, school, fixed):
    columns = [outcome, exposure, weight, school]+covariates
    data = sample.dropna(subset=list(dict.fromkeys(columns))).copy()
    data = data[data[weight] > 0]
    if fixed:
        # Singleton schools supply no within-school identifying information.
        data = data[data.groupby(school)[school].transform('size') > 1]
    require(len(data) > 100 and data[school].nunique() > 20, 'Insufficient sample')
    w = data[weight].to_numpy(float)
    w = w/w.mean()
    matrix = data[[outcome, exposure]+covariates].astype(float).copy()
    if fixed:
        weighted = matrix.mul(w, axis=0)
        sums = weighted.groupby(data[school]).transform('sum')
        den = pd.Series(w, index=data.index).groupby(data[school]).transform('sum')
        matrix -= sums.div(den, axis=0)
    y = matrix.iloc[:,0].to_numpy()
    x = matrix.iloc[:,1:].to_numpy()
    if not fixed:
        x = np.column_stack([x, np.ones(len(data))])
    root = np.sqrt(w)
    xw, yw = x*root[:,None], y*root
    require(np.linalg.matrix_rank(xw) == xw.shape[1], 'Rank-deficient design')
    bread = np.linalg.inv(xw.T@xw)
    beta = np.linalg.lstsq(xw, yw, rcond=None)[0]
    residual = y-x@beta
    scores = x*(w*residual)[:,None]
    clusters = pd.DataFrame(scores).groupby(data[school].to_numpy()).sum().to_numpy()
    groups = len(clusters)
    rank = xw.shape[1] + (groups if fixed else 0)
    correction = groups/(groups-1)*(len(data)-1)/(len(data)-rank)
    covariance = bread@(clusters.T@clusters)@bread*correction
    se = float(np.sqrt(covariance[0,0]))
    # Identify how much exposure variation survives all modeled covariates.
    other = xw[:,1:]
    residual_t = xw[:,0]-other@np.linalg.lstsq(other,xw[:,0],rcond=None)[0]
    energy = pd.Series(residual_t**2).groupby(data[school].to_numpy()).sum()
    effective = float(energy.sum()**2/(energy**2).sum())
    return {'n':len(data),'schools':groups,'beta':float(beta[0]),'se_school_cr1':se,'ci95_normal':[float(beta[0]-1.96*se),float(beta[0]+1.96*se)],'effective_exposure_schools':effective,'outcome':outcome,'exposure':exposure,'controls':covariates,'school_fe':fixed,'weight':weight,'round4_class_forms':{str(k):int(v) for k,v in data.A4CLASS.value_counts().items()}}, data

sample = df[native_white_english].copy()
results = []
for label, wave, endpoint, baseline, weight, school, duration in [
    ('kindergarten',1,2,baseline1,'BYCOMW0','school1','duration_k'),
    ('spring_2000_followup',4,4,baseline2+baseline1,'Y2COMW0','school4','duration_g1')]:
    for domain in ['reading','math']:
        for exposure in [f'anyell{wave}',f'ell10pp{wave}',f'nonwhite10pp{wave}',f'allwhite{wave}']:
            # Hold the sample fixed across raw, baseline and within-school fits.
            common = sample.dropna(subset=[f'{domain}{endpoint}', exposure, weight, school]+controls+baseline+[duration])
            common = common[common[weight] > 0]
            common = common[common.groupby(school)[school].transform('size') > 1]
            for spec, covariates, fixed in [('unadjusted',[],False),('baseline',controls+baseline+[duration],False),('school_fe',controls+baseline+[duration],True)]:
                result,_ = fit(common, f'{domain}{endpoint}', exposure, covariates, weight, school, fixed)
                result.update(period=label,specification=spec)
                results.append(result)
        # Future first-grade exposure predicting already-realized kindergarten learning.
        if wave == 4:
            for exposure in ['anyell4','ell10pp4','nonwhite10pp4','allwhite4']:
                prior_exposure = exposure[:-1] + '1'
                result,_ = fit(sample, f'{domain}2', exposure, controls+baseline1+['duration_k',prior_exposure], weight, school, True)
                result.update(period='pre_first_grade_placebo',specification='school_fe_baseline')
                results.append(result)

# Preserve the all-white contrast and actual target exposure, without calling nonwhite immigrant.
descriptive = []
for wave, weight in [(1,'BYCOMW0'),(4,'Y2COMW0')]:
    valid = sample.dropna(subset=[f'anyell{wave}',f'ell10pp{wave}',f'allwhite{wave}',weight])
    valid = valid[valid[weight]>0]
    descriptive.append({'wave':wave,'n':len(valid),'weighted_any_ell':float(np.average(valid[f'anyell{wave}'],weights=valid[weight])),'weighted_ell_share':float(np.average(valid[f'ell10pp{wave}']/10,weights=valid[weight])),'weighted_all_white':float(np.average(valid[f'allwhite{wave}'],weights=valid[weight]))})
require(len(results) == 56, 'Missing or extra model specifications')
output = {'status':'adjusted_associations_not_causal_effects','source_sha256':manifest['data_sha256'],'selected_sha256':manifest['selected_sha256'],'native_white_english_n':int(native_white_english.sum()),'timing_qa':timing_qa,'scales':scales,'descriptive':descriptive,'models':results}
(args.out/'results.json').write_text(json.dumps(output,indent=2,allow_nan=False))
pd.DataFrame(results).to_csv(args.out / 'models.csv', index=False)
print(json.dumps({'target_n':int(native_white_english.sum()),'descriptive':descriptive,'selected':[r for r in results if r['exposure'].startswith('anyell') and r['specification'] != 'unadjusted']},indent=2))
