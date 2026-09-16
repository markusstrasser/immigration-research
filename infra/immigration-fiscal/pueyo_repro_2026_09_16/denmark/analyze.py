"""Denmark origin-crime repro: rates, ratios, age-sex standardization, verification."""
import os, json
import pandas as pd, numpy as np
D = os.path.dirname(os.path.abspath(__file__))
R = lambda f: pd.read_csv(os.path.join(D, 'raw', f))
s4 = R('strafna4_offence_origin_2008_2024.csv')
s3 = R('strafna3_sex_age_origin_2008_2024.csv')
s9 = R('strafna9_sex_age_ancestry_2008_2024.csv')
pop = R('folk1c_pop_origin_sex_age_2008_2024.csv')
f1e = R('folk1e_2024q1_age15_79.csv')
pop['YEAR'] = pop.TID.astype(str).str[:4].astype(int)
out = []
def P(*a):
    s = ' '.join(str(x) for x in a); print(s); out.append(s)

# ---------- VERIFICATION ----------
P("="*70); P("VERIFICATION")
a_s9 = s9[(s9.ALDER == 'Age, total') & (s9.HERKOMST == 'Total') & (s9.TID == 2024)].INDHOLD.sum()
a_s4_dec = s4[(s4['OVERTRÆD'] == 'Criminal decisions total') & (s4.IELAND == 'Total') & (s4.TID == 2024)].INDHOLD.iloc[0]
P(f"(a) STRAFNA9 2024 persons guilty, M+K, age TOT, HERKOMST TOT = {a_s9:,}")
P(f"    STRAFNA4 2024 'Criminal decisions total', IELAND Total     = {a_s4_dec:,}")
P(f"    diff = {a_s4_dec - a_s9:+,} ({(a_s4_dec/a_s9-1)*100:+.3f}%)  -> {'PASS' if abs(a_s4_dec/a_s9-1)<0.005 else 'FAIL'}")
p_2024 = pop[(pop.YEAR == 2024) & (pop.KØN == 'Total') & (pop.IELAND == 'Total')].INDHOLD.sum()
p_f1e = f1e.INDHOLD.sum()
P(f"(b) FOLK1C 2024Q1 ages 15-79 IELAND=Total, KØN=Total = {p_2024:,}")
P(f"    FOLK1E 2024Q1 ages 15-79 HERKOMST=Total          = {p_f1e:,}")
P(f"    diff = {p_2024-p_f1e:+,} ({(p_2024/p_f1e-1)*100:+.4f}%)  -> {'PASS' if abs(p_2024/p_f1e-1)<0.005 else 'FAIL'}")
# extra: FOLK1C country rows sum vs Total row
csum = pop[(pop.YEAR == 2024) & (pop.KØN == 'Total') & (pop.IELAND != 'Total')].INDHOLD.sum()
P(f"(b2) FOLK1C sum over 241 country rows = {csum:,} vs Total row {p_2024:,} ({(csum/p_2024-1)*100:+.4f}%)")

# ---------- COUNTRY UNIVERSE ----------
CRIME_COUNTRIES = sorted(set(s4.IELAND) - {'Total', 'Other countries, total',
                          'Other countries, western', 'Other countries, non-western'})
popname = {c: c for c in CRIME_COUNTRIES}
pnames = set(pop.IELAND)
missing = [c for c in CRIME_COUNTRIES if c not in pnames]
P(f"\nSTRAFNA4 origins: {len(CRIME_COUNTRIES)}; not matched in FOLK1C: {missing}")

OFF = {'criminal_code_total': 'Criminal code, total', 'sexual_total': 'Sexual offenses, total',
       'violence_total': 'Crimes of violence, total', 'rape': 'Rape, etc ', 'robbery': 'Robbery ',
       'attempted_homicide': 'Attempted homicide ', 'assault_public_servant':
       'Assault against public servant while in discharge of his duties',
       'grievous_assault': 'Grievous assault ', 'blackmail': 'Blackmail and usury ',
       'forgery': 'Forgery ', 'fraud': 'Fraud ', 'shoplifting': 'Shoplifting, etc.',
       'groping': 'Offences against decency, by  pawing ', 'theft_other_objects': 'Theft of other objects ',
       'household_burglary': 'Household burglary ', 'all_decisions': 'Criminal decisions total'}
BURG = ['Burglary (banks, shops, etc.)', 'Household burglary ', 'Burglary (uninhabited buildings)']
THEFT = ['Other theft ', 'Theft of other objects ', 'Theft from cars, boats, etc.', 'Theft of vehicle',
         'Theft of mopeds ', 'Theft of bicycles ']
for k, v in OFF.items():
    assert v in set(s4['OVERTRÆD']), k

def rates(offlabels, yr0, yr1, label):
    c = s4[s4['OVERTRÆD'].isin(offlabels) & s4.TID.between(yr0, yr1)]
    c = c.groupby('IELAND').INDHOLD.sum().rename('persons')
    p = pop[(pop.KØN == 'Total') & pop.YEAR.between(yr0, yr1)].groupby('IELAND').INDHOLD.sum().rename('population')
    d = pd.concat([c, p], axis=1).dropna()
    d = d.loc[[i for i in d.index if i in CRIME_COUNTRIES]]
    d['rate_per_100k'] = d.persons / d.population * 1e5
    d['ratio'] = d.rate_per_100k / d.loc['Denmark', 'rate_per_100k']
    d['offence'] = label; d['year_range'] = f"{yr0}-{yr1}"
    return d.reset_index().rename(columns={'IELAND': 'origin'})

tidy = []
for lbl, off in list(OFF.items()) + [('burglary_all', BURG), ('theft_all', THEFT)]:
    offl = off if isinstance(off, list) else [off]
    for y0, y1 in [(2008, 2024), (2010, 2022)]:
        tidy.append(rates(offl, y0, y1, lbl))
tidy = pd.concat(tidy, ignore_index=True)
tidy[['year_range', 'origin', 'offence', 'persons', 'population', 'rate_per_100k', 'ratio']].rename(
    columns={'ratio': 'ratio_to_danish_origin'}).to_csv(os.path.join(D, 'dk_origin_rates.csv'), index=False)

P("\n" + "="*70); P("CHART 1: violent crime 2010-2022, rate relative to Danish origin (top 20)")
v = tidy[(tidy.offence == 'violence_total') & (tidy.year_range == '2010-2022')].sort_values('ratio', ascending=False)
P(v.head(22)[['origin', 'persons', 'population', 'rate_per_100k', 'ratio']].to_string(index=False,
  formatters={'rate_per_100k': '{:.1f}'.format, 'ratio': '{:.2f}'.format}))
P("\nDenmark reference rate/100k: %.1f" % v[v.origin == 'Denmark'].rate_per_100k.iloc[0])

P("\n" + "="*70); P("CHART 3 (Pallesen) 2008-2024 ratios, top 6 per offence")
for lbl in ['rape', 'assault_public_servant', 'attempted_homicide', 'blackmail', 'burglary_all',
            'forgery', 'fraud', 'grievous_assault', 'groping', 'robbery', 'shoplifting', 'theft_all']:
    t = tidy[(tidy.offence == lbl) & (tidy.year_range == '2008-2024')].sort_values('ratio', ascending=False)
    t = t[t.persons >= 10]
    P(f"-- {lbl}: " + ", ".join(f"{r.origin} {r.ratio:.0f}x(n={int(r.persons)})" for r in t.head(6).itertuples()))

# ---------- AGE-SEX STANDARDIZATION (STRAFNA3: total persons guilty) ----------
P("\n" + "="*70); P("AGE-SEX STANDARDIZATION (STRAFNA3 = all persons guilty, any offence)")
AGEMAP = {'15-19': '15-29', '20-24': '15-29', '25-29': '15-29', '30-34': '30-49', '35-39': '30-49',
          '40-44': '30-49', '45-49': '30-49', '50-54': '50-79', '55-59': '50-79', '60-64': '50-79',
          '65-69': '50-79', '70-74': '50-79', '75-79': '50-79'}
pp = pop[pop.KØN.isin(['Men', 'Women'])].copy()
pp['band'] = pp.ALDER.str.replace(' years', '', regex=False).map(AGEMAP)
pp['sex'] = pp.KØN.map({'Men': 'Men', 'Women': 'Women'})
Y0, Y1 = 2010, 2021
pg = pp[pp.YEAR.between(Y0, Y1)].groupby(['IELAND', 'sex', 'band']).INDHOLD.sum().rename('population')
cc = s3[(s3.ALDER != 'Age, total') & s3.TID.between(Y0, Y1)].copy()
cc['band'] = cc.ALDER.str.replace(' years', '', regex=False)
cg = cc.groupby(['IELAND', 'KOEN', 'band']).INDHOLD.sum().rename('persons')
cg.index = cg.index.set_names(['IELAND', 'sex', 'band'])
m = pd.concat([cg, pg], axis=1).dropna()
m = m[m.population > 0]
std_w = m.loc['Denmark', 'population']
std_w = std_w / std_w.sum()
m['rate'] = m.persons / m.population
rows = []
for c in CRIME_COUNTRIES:
    if c not in m.index.get_level_values(0):
        continue
    sub = m.loc[c]
    if len(sub) < 6 or sub.persons.sum() < 50:
        continue
    crude = sub.persons.sum() / sub.population.sum()
    stdz = float((sub.rate * std_w.reindex(sub.index)).sum())
    rows.append((c, sub.persons.sum(), crude * 1e5, stdz * 1e5))
st = pd.DataFrame(rows, columns=['origin', 'persons', 'crude_per100k', 'std_per100k'])
dk = st[st.origin == 'Denmark'].iloc[0]
st['crude_ratio'] = st.crude_per100k / dk.crude_per100k
st['std_ratio'] = st.std_per100k / dk.std_per100k
st['pct_of_gap_removed'] = np.where(st.crude_ratio > 1, (st.crude_ratio - st.std_ratio) / (st.crude_ratio - 1) * 100, np.nan)
st = st.sort_values('crude_ratio', ascending=False)
st.to_csv(os.path.join(D, 'dk_agesex_standardized_totalcrime.csv'), index=False)
P(f"Direct standardization to Danish-origin sex x 3-age-band structure, {Y0}-{Y1}, all offences")
P(st.head(25).to_string(index=False, formatters={'crude_per100k': '{:.0f}'.format, 'std_per100k': '{:.0f}'.format,
  'crude_ratio': '{:.2f}'.format, 'std_ratio': '{:.2f}'.format, 'pct_of_gap_removed': '{:.0f}'.format}))

# STRAFNA9 aggregate check: how much adjustment moves non-western aggregate
P("\nSTRAFNA9 non-western immigrants, same method (aggregate sanity):")
POPMAP = {'Persons of Danish origin': '5', 'Immigrants from western countries': None}
f1c_h = None
open(os.path.join(D, 'analysis_log.txt'), 'w').write('\n'.join(out) + '\n')
print("\nwrote dk_origin_rates.csv, dk_agesex_standardized_totalcrime.csv, analysis_log.txt")
