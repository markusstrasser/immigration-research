"""Independent Python reconstruction from a public CSV mirror; not official data validation.
Run: uv run --no-project --with pandas --with numpy --with statsmodels python3 replicate_bracero_danzer.py
"""
from pathlib import Path
import hashlib
import json
import math
import platform
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import t

BASE = Path(__file__).resolve().parent
RAW = BASE / 'raw'
OUT = BASE / 'derived'
OUT.mkdir(exist_ok=True)
d = pd.read_csv(RAW / 'bracero-mirror/data.csv')
c = pd.read_csv(RAW / 'bracero-mirror/cpi.csv')
d['time_m'] = (d.Year - 1960) * 12 + d.Month - 1
assert not d.duplicated(['State_FIPS', 'time_m']).any()
assert not c.duplicated(['State_FIPS', 'time_m']).any()
d = d.merge(c[['State_FIPS', 'time_m', 'cpi']], on=['State_FIPS', 'time_m'], how='left', validate='1:1')
d['Mexican'] = d.Mexican_final
full = (((d.Year == 1954) & (d.Month >= 7)) | (d.Year >= 1955)) & (d.Year <= 1972)
d.loc[full, 'Mexican'] = d.loc[full, 'Mexican'].fillna(0)
share55 = (d.loc[d.Year == 1955, 'Mexican'] / d.loc[d.Year == 1955, 'TotalHiredSeasonal_final']).replace([np.inf, -np.inf], np.nan)
share = d.loc[d.Year == 1955, ['State_FIPS']].assign(share=share55).groupby('State_FIPS')['share'].mean()
d['share55'] = d.State_FIPS.map(share)
d['treatment'] = (d.Year >= 1965) * d.share55
d['hourly'] = d.HourlyComposite_final / (d.cpi / 0.1966401)
d['daily'] = d.DailywoBoard_final / (d.cpi / 0.1966401)
d['domestic'] = d[['Local_final', 'Intrastate_final', 'Interstate_final']].sum(axis=1)
d.loc[(d.Year < 1954) | (d.Year > 1973) | ((d.Year == 1973) & (d.Month > 7)), 'domestic'] = np.nan
# A paper table treats unreported state counts as zero ONLY in months with a
# source report. Never turn a whole missing report into 46 observed zeroes.
report_month = d.groupby('time_m')['Local_final'].transform('count') > 0
d.loc[~report_month, 'domestic'] = np.nan
d['quarter'] = (d.Year - 1960) * 4 + ((d.Month - 1) // 3)

# Complete state-months only inside detected report months. CSV rows can be absent,
# not merely contain missing cells. Keep this separate from the wage panel.
report_times=d.loc[report_month&d.Year.ge(1954)&((d.Year<1973)|((d.Year==1973)&d.Month.le(7))), 'time_m'].unique()
eligible_states=share.dropna().index
grid=pd.MultiIndex.from_product([eligible_states, sorted(report_times)], names=['State_FIPS','time_m'])
source_panel=d.set_index(['State_FIPS','time_m'])
added=grid.difference(source_panel.index)
domestic_panel=source_panel.reindex(grid).reset_index()
domestic_panel['Year']=1960+domestic_panel.time_m//12
domestic_panel['Month']=domestic_panel.time_m%12+1
domestic_panel['share55']=domestic_panel.State_FIPS.map(share)
domestic_panel['treatment']=(domestic_panel.Year>=1965)*domestic_panel.share55
domestic_panel['domestic']=domestic_panel[['Local_final','Intrastate_final','Interstate_final']].sum(axis=1)
assert not domestic_panel.duplicated(['State_FIPS','time_m']).any()
assert domestic_panel.groupby('time_m').size().eq(len(eligible_states)).all()
(OUT/'domestic_panel_completion.json').write_text(json.dumps({'eligible_states':len(eligible_states),'detected_report_months':len(report_times),'added_absent_state_months':len(added),'completed_rows':len(domestic_panel),'added_months':sorted(set(int(t) for _,t in added)),'limit':'Report months inferred from any observed Local_final, not verified against official report calendar. Published employment sample remains unmatched.'},indent=2))

def regress(frame, outcome, timecol, label, published=None):
    s = frame.dropna(subset=[outcome, 'treatment', 'State_FIPS', timecol]).copy()
    x = pd.concat([pd.Series(1., index=s.index, name='constant'), s[['treatment']], pd.get_dummies(s.State_FIPS.astype(int).astype(str), prefix='state', drop_first=True, dtype=float), pd.get_dummies(s[timecol].astype(int).astype(str), prefix='time', drop_first=True, dtype=float)], axis=1)
    model = sm.OLS(s[outcome].astype(float), x).fit(cov_type='cluster', cov_kwds={'groups': s.State_FIPS, 'use_correction': True})
    b = float(model.params['treatment'])
    se = float(model.bse['treatment'])
    nested_se = se * math.sqrt((len(s)-model.df_model-1)/(len(s)-model.df_model-1+s.State_FIPS.nunique()-1))
    # Independent FWL solution with alternating projections; no dummy matrix.
    residual = s[[outcome, 'treatment']].astype(float).copy()
    for iteration in range(1000):
        old = residual.to_numpy().copy()
        residual -= residual.groupby(s.State_FIPS).transform('mean')
        residual -= residual.groupby(s[timecol]).transform('mean')
        if np.max(np.abs(residual.to_numpy() - old)) < 1e-10:
            break
    yr, xr = residual[outcome].to_numpy(), residual.treatment.to_numpy()
    fwl = float(xr @ yr / (xr @ xr))
    assert abs(fwl - b) < 1e-7 * max(1, abs(b)), (label, b, fwl)
    crit = float(t.ppf(.975, s.State_FIPS.nunique()-1))
    r = dict(label=label, n=len(s), states=s.State_FIPS.nunique(), beta=b, se_lsdv_cluster=se, se_nested_state_adjustment=nested_se, t95_low=b-crit*se, t95_high=b+crit*se, fwl_beta=fwl, fwl_iterations=iteration+1)
    if published is not None:
        r['published_beta'] = published
        r['absolute_difference'] = abs(b-published)
        tolerance = .000501 if label=='daily_all' else (.000051 if abs(published)<1 else .051)
        r['matches_printed_rounding'] = abs(b-published) <= tolerance
    return r

quarterly = d.loc[d.Month.isin([1,4,7,10])]
results = []
for start, end, suffix, anchors in [(1942,1975,'all',(-.0356,-.385)), (1960,1970,'1960_1970',(-.0401,-.0247))]:
    q = quarterly.loc[quarterly.Year.between(start,end)].copy()
    for outcome, anchor in zip(['hourly','daily'],anchors):
        results.append(regress(q,outcome,'quarter',f'{outcome}_{suffix}',anchor))
        q[f'log_{outcome}'] = np.log(q[outcome].where(q[outcome]>0))
        results.append(regress(q,f'log_{outcome}','quarter',f'log_{outcome}_{suffix}'))
results.append(regress(d,'Mexican','time_m','exposure_first_stage_post1965'))
results.append(regress(domestic_panel,'domestic','time_m','domestic_all',-12801.7))
results.append(regress(domestic_panel.loc[domestic_panel.Year.between(1960,1970)],'domestic','time_m','domestic_1960_1970',-1648.3))
pd.DataFrame(results).to_csv(OUT/'bracero_raw_mirror_results.csv', index=False)

# Published Danzer et al. 2024 supplement Table B-6, automation count column.
beta=np.array([-1.552,-1.745,-2.544,-3.173,-3.647,-2.483,-2.045,-2.222,-2.480,-.865,-.194])
se=np.array([.906,1.122,1.328,1.250,1.415,1.458,1.424,1.776,1.421,1.415,.789])
delta=.1
annual=pd.DataFrame({'event_year':range(11),'beta':beta,'se':se,'effect_for_10pp':np.expm1(delta*beta),'normal95_low':np.expm1(delta*(beta-1.96*se)),'normal95_high':np.expm1(delta*(beta+1.96*se))})
annual.to_csv(OUT/'danzer_annual_count_ratios.csv',index=False)
# Every PSD correlation matrix obeys sd(sum b)<=sum sd(b). This is conservative,
# conditional on reported asymptotic marginal SEs, and is NOT a count-stock CI.
avg=float(beta.mean())
upperse=float(se.mean())
danzer={'source':'Published 2024 supplement Table B-6 column 1', 'exposure_change':delta,'sum_beta':float(beta.sum()),'sum_se_upper_bound':float(se.sum()),'mean_beta':avg,'mean_se_upper_bound':upperse,'geometric_mean_ratio_10pp':math.exp(delta*avg),'covariance_agnostic_normal95_ratio':[math.exp(delta*(avg-1.96*upperse)),math.exp(delta*(avg+1.96*upperse))], 'actual_cumulative_count_effect':'NOT IDENTIFIED from printed coefficients: need untreated predicted count path, covariance and possibly cross-region aggregation weights', 'claim_guard':'Returning annual effects toward zero does not establish cumulative invention catch-up.'}
(OUT/'danzer_partial_bound.json').write_text(json.dumps(danzer,indent=2)+'\n')
manifest={'date':'2026-09-17','python':platform.python_version(),'numpy':np.__version__,'pandas':pd.__version__,'statsmodels':sm.__version__,'mirror_tree_sha':json.loads((RAW/'bracero-julia-tree.json').read_text())['sha'],'provenance':'DEGRADED: third-party public CSV mirror, original ICPSR byte identity not verified','inputs':[]}
for path in sorted(RAW.rglob('*')):
    if path.is_file():
        manifest['inputs'].append({'path':str(path.relative_to(BASE)),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
(BASE/'epoch2-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
print(pd.DataFrame(results).to_string(index=False))
print(json.dumps(danzer,indent=2))
print('PASS: all regressions independently matched by FWL; raw rows',len(d))
