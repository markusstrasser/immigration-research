"""Phase 2: label hypotheses (Palestine / Ex-Yugoslavia), violent-crime adjustment approximation,
STRAFNA9 aggregate adjustment."""
import os, io, json, requests
import pandas as pd, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
R = lambda f: pd.read_csv(os.path.join(D, 'raw', f))
s4 = R('strafna4_offence_origin_2008_2024.csv'); s3 = R('strafna3_sex_age_origin_2008_2024.csv')
s9 = R('strafna9_sex_age_ancestry_2008_2024.csv'); pop = R('folk1c_pop_origin_sex_age_2008_2024.csv')
pop['YEAR'] = pop.TID.astype(str).str[:4].astype(int)
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

OFF = {'rape': ['Rape, etc '], 'assault_public_servant': ['Assault against public servant while in discharge of his duties'],
 'attempted_homicide': ['Attempted homicide '], 'blackmail': ['Blackmail and usury '],
 'burglary': ['Burglary (banks, shops, etc.)', 'Household burglary ', 'Burglary (uninhabited buildings)'],
 'forgery': ['Forgery '], 'fraud': ['Fraud '], 'grievous_assault': ['Grievous assault '],
 'groping': ['Offences against decency, by  pawing '], 'robbery': ['Robbery '],
 'shoplifting': ['Shoplifting, etc.'], 'theft': ['Other theft ', 'Theft of other objects ',
 'Theft from cars, boats, etc.', 'Theft of vehicle', 'Theft of mopeds ', 'Theft of bicycles ']}
EXYU = ['Yugoslavia', 'Yugoslavia, Federal Republic', 'Serbia and Montenegro', 'Bosnia and Herzegovina',
        'Croatia', 'Republic of North Macedonia']
CANDS = {'Lebanon': ['Lebanon'], 'Kuwait': ['Kuwait'], 'Leb+Kuw': ['Lebanon', 'Kuwait'],
         'Leb+Kuw+Jor': ['Lebanon', 'Kuwait', 'Jordan'], 'Ex-Yugoslavia': EXYU}
# Pallesen chart values read off the image
CHART = {'rape': {'Somalia': 20, 'Syria': 16, 'Palestine': 12, 'Afghanistan': 11, 'Iraq': 9},
 'assault_public_servant': {'Somalia': 11, 'Palestine': 9, 'Tunisia': 8, 'Uganda': 7, 'Ethiopia': 5},
 'attempted_homicide': {'Somalia': 27, 'Morocco': 20, 'Palestine': 20, 'Iraq': 13, 'Pakistan': 10},
 'blackmail': {'Palestine': 27, 'Somalia': 14, 'Ex-Yugoslavia': 13, 'Iraq': 12, 'Afghanistan': 9},
 'burglary': {'Palestine': 10, 'Somalia': 8, 'Tunisia': 8, 'Morocco': 7, 'Ex-Yugoslavia': 5},
 'forgery': {'Somalia': 13, 'Syria': 10, 'Uganda': 10, 'Palestine': 9, 'Tanzania': 9},
 'fraud': {'Somalia': 8, 'Palestine': 8, 'Nigeria': 6, 'Morocco': 5, 'Ex-Yugoslavia': 5},
 'grievous_assault': {'Somalia': 17, 'Palestine': 12, 'Tunisia': 12, 'Algeria': 8, 'Iraq': 7},
 'groping': {'Syria': 12, 'Myanmar': 11, 'Afghanistan': 10, 'Somalia': 9, 'Iraq': 6},
 'robbery': {'Somalia': 33, 'Tunisia': 21, 'Palestine': 16, 'Algeria': 13, 'Uganda': 12},
 'shoplifting': {'Tunisia': 9, 'Ex-Yugoslavia': 7, 'Somalia': 7, 'Uganda': 7, 'Algeria': 6},
 'theft': {'Palestine': 8, 'Tunisia': 7, 'Somalia': 7, 'Ex-Yugoslavia': 5, 'Morocco': 4}}

def ratio(offlabels, origins, y0=2008, y1=2024):
    c = s4[s4['OVERTRÆD'].isin(offlabels) & s4.TID.between(y0, y1)]
    p = pop[(pop.KØN == 'Total') & pop.YEAR.between(y0, y1)]
    num = c[c.IELAND.isin(origins)].INDHOLD.sum(); den = p[p.IELAND.isin(origins)].INDHOLD.sum()
    dn = c[c.IELAND == 'Denmark'].INDHOLD.sum() / p[p.IELAND == 'Denmark'].INDHOLD.sum()
    return (num / den) / dn, num

P("="*72); P("LABEL TEST: which STRAFNA4 origin(s) reproduce Pallesen's 'Palestine' bar?")
P(f"{'offence':<24}{'chart':>7}" + "".join(f"{k:>14}" for k in CANDS))
err = {k: [] for k in CANDS}
for off, vals in CHART.items():
    if 'Palestine' not in vals: continue
    tgt = vals['Palestine']; row = f"{off:<24}{tgt:>7}"
    for k, o in CANDS.items():
        r, n = ratio(OFF[off], o); row += f"{r:>9.1f}(n{int(n)})"[:14].rjust(14)
        err[k].append(abs(r - tgt) / tgt)
    P(row)
P("mean |rel err| vs chart 'Palestine': " + ", ".join(f"{k}={np.mean(v)*100:.0f}%" for k, v in err.items()))

P("\n" + "="*72); P("FULL CHART-3 COMPARISON (2008-2024, n>=10, 'Palestine'->Lebanon, 'Ex-Yugoslavia'->6 ex-YU codes)")
rows = []
for off, vals in CHART.items():
    for name, cv in vals.items():
        origins = EXYU if name == 'Ex-Yugoslavia' else (['Lebanon'] if name == 'Palestine' else [name])
        r, n = ratio(OFF[off], origins)
        rows.append((off, name, cv, round(r, 1), int(n)))
cmp3 = pd.DataFrame(rows, columns=['offence', 'chart_label', 'chart_ratio', 'my_ratio', 'my_persons'])
cmp3['abs_diff'] = (cmp3.my_ratio - cmp3.chart_ratio).abs()
cmp3.to_csv(os.path.join(D, 'chart3_comparison.csv'), index=False)
P(cmp3.to_string(index=False))
P(f"\nmedian |chart - mine| = {cmp3.abs_diff.median():.1f}x ; within 1x: {(cmp3.abs_diff<=1).sum()}/{len(cmp3)}"
  f" ; within 2x: {(cmp3.abs_diff<=2).sum()}/{len(cmp3)}")

# ---- violent crime 2010-2021 raw + approximate age-sex adjustment ----
P("\n" + "="*72); P("CHART 2: age/sex-adjusted violent crime 2010-2021")
VIOL = ['Crimes of violence, total']
AGEMAP = {'15-19': '15-29', '20-24': '15-29', '25-29': '15-29', '30-34': '30-49', '35-39': '30-49',
 '40-44': '30-49', '45-49': '30-49', '50-54': '50-79', '55-59': '50-79', '60-64': '50-79',
 '65-69': '50-79', '70-74': '50-79', '75-79': '50-79'}
Y0, Y1 = 2010, 2021
pp = pop[pop.KØN.isin(['Men', 'Women'])].copy()
pp['band'] = pp.ALDER.str.replace(' years', '', regex=False).map(AGEMAP)
pg = pp[pp.YEAR.between(Y0, Y1)].groupby(['IELAND', 'KØN', 'band']).INDHOLD.sum().rename('population')
pg.index = pg.index.set_names(['IELAND', 'sex', 'band'])
cc = s3[(s3.ALDER != 'Age, total') & s3.TID.between(Y0, Y1)].copy()
cc['band'] = cc.ALDER.str.replace(' years', '', regex=False)
cc['sex'] = cc.KOEN.map({'Men': 'Men', 'Women': 'Women'})
cg = cc.groupby(['IELAND', 'sex', 'band']).INDHOLD.sum().rename('persons')
m = pd.concat([cg, pg], axis=1).dropna(); m = m[m.population > 0]; m['rate'] = m.persons / m.population
w = m.loc['Denmark', 'population']; w = w / w.sum()
def adjfac(c):
    if c not in m.index.get_level_values(0): return np.nan
    sub = m.loc[c]
    if len(sub) < 6: return np.nan
    crude = sub.persons.sum() / sub.population.sum()
    return float((sub.rate * w.reindex(sub.index)).sum()) / crude
dk_fac = adjfac('Denmark')
CH2 = {'Kuwait': 6.5, 'Tunisia': 6.4, 'Somalia': 6.2, 'Lebanon': 5.7, 'Jordan': 4.8, 'Uganda': 4.8,
       'Algeria': 4.0, 'Morocco': 3.8, 'Iraq': 3.3, 'Ethiopia': 3.0, 'Egypt': 3.0, 'Iran': 2.9,
       'Syria': 2.5, 'Turkey': 2.4, 'Afghanistan': 2.3, 'Pakistan': 1.9, 'Denmark': 1.0}
rows = []
for c, cv in CH2.items():
    raw, n = ratio(VIOL, [c], Y0, Y1)
    f = adjfac(c) / dk_fac
    rows.append((c, round(raw, 2), round(raw * f, 2), cv, int(n), round(f, 3)))
cmp2 = pd.DataFrame(rows, columns=['origin', 'raw_ratio_2010_2021', 'approx_adj_ratio', 'chart_adj_ratio',
                                   'persons', 'agesex_factor_rel_DK'])
cmp2['implied_chart_gap_removed_pct'] = ((cmp2.raw_ratio_2010_2021 - cmp2.chart_adj_ratio) /
                                         (cmp2.raw_ratio_2010_2021 - 1) * 100).round(0)
cmp2['my_gap_removed_pct'] = ((cmp2.raw_ratio_2010_2021 - cmp2.approx_adj_ratio) /
                              (cmp2.raw_ratio_2010_2021 - 1) * 100).round(0)
cmp2.to_csv(os.path.join(D, 'chart2_comparison.csv'), index=False)
P(cmp2.to_string(index=False))

# ---- STRAFNA9 aggregate adjustment (needs FOLK1E by sex x age x ancestry) ----
P("\n" + "="*72); P("STRAFNA9 aggregate (ancestry groups), age-sex standardized to Danish-origin structure")
S = requests.Session(); S.headers.update({'User-Agent': 'research-agent/1.0'})
body = {"table": "FOLK1E", "format": "CSV", "lang": "en", "variables": [
    {"code": "OMRÅDE", "values": ["000"]}, {"code": "KØN", "values": ["1", "2"]},
    {"code": "ALDER", "values": [str(a) for a in range(15, 80)]},
    {"code": "HERKOMST", "values": ["1", "24", "25", "34", "35"]},
    {"code": "Tid", "values": [f"{y}K1" for y in range(Y0, Y1 + 1)]}]}
r = S.post('https://api.statbank.dk/v1/data', json=body, timeout=600); r.raise_for_status()
f1e = pd.read_csv(io.StringIO(r.text), sep=';'); f1e.to_csv(os.path.join(D, 'raw', 'folk1e_sex_age_ancestry_2010_2021.csv'), index=False)
json.dump(body, open(os.path.join(D, 'bodies', 'folk1e_ancestry_body.json'), 'w'), ensure_ascii=False, indent=1)
f1e['band'] = pd.cut(f1e.ALDER.str.extract(r'(\d+)')[0].astype(int), [14, 29, 49, 79],
                     labels=['15-29', '30-49', '50-79']).astype(str)
pg9 = f1e.groupby(['HERKOMST', 'KØN', 'band']).INDHOLD.sum().rename('population')
pg9.index = pg9.index.set_names(['H', 'sex', 'band'])
c9 = s9[(s9.ALDER != 'Age, total') & s9.TID.between(Y0, Y1)].copy()
c9['band'] = c9.ALDER.str.replace(' years', '', regex=False)
cg9 = c9.groupby(['HERKOMST', 'KOEN', 'band']).INDHOLD.sum().rename('persons')
cg9.index = cg9.index.set_names(['H', 'sex', 'band'])
m9 = pd.concat([cg9, pg9], axis=1).dropna(); m9['rate'] = m9.persons / m9.population
w9 = m9.loc['Persons of Danish origin', 'population']; w9 = w9 / w9.sum()
base = m9.loc['Persons of Danish origin']; base_c = base.persons.sum() / base.population.sum()
base_s = float((base.rate * w9.reindex(base.index)).sum())
for h in ['Immigrants from western countries', 'Immigrants from non-western countries',
          'Descendants from western countries', 'Descendants from non-western countries']:
    sub = m9.loc[h]; cr = sub.persons.sum() / sub.population.sum()
    st = float((sub.rate * w9.reindex(sub.index)).sum())
    P(f"  {h:<42} crude {cr/base_c:5.2f}x  age-sex std {st/base_s:5.2f}x  "
      f"gap removed {((cr/base_c - st/base_s)/(cr/base_c - 1)*100):5.0f}%")
open(os.path.join(D, 'analysis_log.txt'), 'a').write('\n'.join(out) + '\n')
print("\nwrote chart2_comparison.csv, chart3_comparison.csv")
