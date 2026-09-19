from pathlib import Path
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[2] / 'infra/immigration-fiscal'
lane = root / 'displacement_transfers_2026_09_18/derived'
out = pd.read_csv(lane / 'metro_panel.csv', dtype={'cbsa': str})
base = pd.read_csv(lane / 'base_shares_pre1990.csv', dtype={'cbsa': str})
natl = pd.read_csv(lane / 'national_stock.csv').set_index('year')
ee = pd.read_csv(root / 'employment_entry_2026_09_18/derived/metro_year_panel.csv', dtype={'cbsa': str, 'sex': str})
ee = ee[ee.sex == '1'].drop_duplicates(['cbsa', 'year'])
ee['mex_share_fix'] = 100 * ee.t_mex1864 / ee.t_pop1864
m = out[out.year == 2008][['cbsa', 'ssi_rate', 'pop']].merge(out[out.year == 2018][['cbsa', 'ssi_rate']], on='cbsa', suffixes=('_0', '_1'))
t = ee[ee.year == 2008][['cbsa', 'mex_share_fix']].merge(ee[ee.year == 2018][['cbsa', 'mex_share_fix']], on='cbsa', suffixes=('_0', '_1'))
m = m.merge(t, on='cbsa').merge(base[['cbsa', 'mex_base_share']], on='cbsa')
m = m[m['pop'] >= 100000].replace([np.inf, -np.inf], np.nan).dropna()
shift = natl.loc[2018, 'mex'] - natl.loc[2008, 'mex']
w = m['pop'].to_numpy()
x = (m.mex_share_fix_1 - m.mex_share_fix_0).to_numpy()
y = (m.ssi_rate_1 - m.ssi_rate_0).to_numpy()
raw_z = (100 * m.mex_base_share * shift / m['pop']).to_numpy()
for scale in [1, -1, 0.001]:
    z = raw_z * scale
    X = np.column_stack([np.ones(len(z)), z])
    bread = np.linalg.inv((X.T * w) @ X)
    beta = bread @ (X.T @ (w * x))
    residual = x - X @ beta
    influence = (X.T * (w * residual)).T @ bread
    covariance = influence.T @ influence * len(z) / (len(z) - 2)
    first_stage_f = beta[1] ** 2 / covariance[1, 1]
    zc = z - np.average(z, weights=w)
    iv = np.sum(w * zc * y) / np.sum(w * zc * x)
    print(dict(n=len(m), national_shift=float(shift), scale=scale, first_stage_F=float(first_stage_f), iv_ssi=float(iv)))
