"""Medical cell-mix diagnostic before LTSS; no audited model is written."""
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

root = Path(__file__).resolve().parents[3]
f = root / 'infra/immigration-fiscal'
m = f / 'medical_ethnicity_pooled_2026_09_23/derived'
d = pd.read_parquet(f / 'cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet', columns=[
    'A_AGE', 'PRPERTYP', 'PRCITSHP', 'PENATVTY', 'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP',
    'PUB', 'PRIV', 'GESTFIPS', 'pwwgt0'])
a = pd.read_parquet(f / 'dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet',
                    columns=['ST', 'RELSHIPP', 'POBP', 'CIT', 'PWGTP'])
a = a[a.RELSHIPP.ne(37) & a.POBP.eq(303) & a.CIT.isin([4, 5]) & ~a.ST.isin([6, 48])]
w = d.pwwgt0.to_numpy().copy()
nw = w.copy()
factors = {}
for citizenship in (4, 5):
    mask = d.PENATVTY.eq(303) & ~d.GESTFIPS.isin([6, 48]) & d.PRCITSHP.eq(citizenship)
    factor = a.loc[a.CIT.eq(citizenship), 'PWGTP'].sum() / w[mask].sum()
    nw[mask] *= factor
    factors[citizenship] = factor
civ = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
native = d.PRCITSHP.isin([1, 2, 3])
us = [57, 60, 66, 69, 73, 78]
target = civ & ((d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)) |
                 (native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303))) |
                 (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)))
exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0))
d['band'] = pd.cut(d.A_AGE, [-1, 17, 34, 49, 64, 200], labels=['0-17','18-34','35-49','50-64','65+'])
d['nativity'] = np.where(d.PENATVTY.eq(57), 'us_born', 'foreign_born')
cells = pd.read_csv(m / 'cps_cells.csv').set_index(['band', 'nativity'])
ratios = pd.read_csv(m / 'ratios.csv')
ratios = ratios[(ratios.spec == 'winsor_p995') & (ratios.scheme == 'transport') &
                (ratios.comparison == 'mexican_origin/all_donors')]
ratios = ratios.set_index(['measure', 'band', 'nativity'])
trans = pd.read_csv(m / 'translation_account.csv')
trans = trans[trans.spec == 'winsor_p995'].set_index('line')
mapping = {
    'medicaid_and_chip_other_medical': ('medicaid', 'medicaid'),
    'medicare': ('medicare', 'medicare'),
    'health_services': ('health_other', 'other_public'),
    'military_medical': ('tricare', 'tricare'),
    'veterans_other': ('va', 'va'),
}
results = []
for line, (key, measure) in mapping.items():
    values = np.zeros(len(d))
    old_cost = new_cost = old_rat_num = new_rat_num = 0.
    for (band, nativity), row in cells.iterrows():
        mask = d.band.eq(band) & d.nativity.eq(nativity) & exposure
        v = row[f'meps2024_{key}']
        values[mask] = v
        old = w[mask & target].sum() * v
        new = nw[mask & target].sum() * v
        ratio = ratios.loc[(measure, band, nativity), 'ratio']
        old_cost += old
        new_cost += new
        old_rat_num += old * ratio
        new_rat_num += new * ratio
    old_share = old_cost / (values[civ] * w[civ]).sum()
    new_share = new_cost / (values[civ] * nw[civ]).sum()
    old_factor = old_rat_num / old_cost
    new_factor = new_rat_num / new_cost
    assert abs(old_factor - trans.loc[line, 'key_weighted_ratio']) < 1e-9
    t = trans.loc[line, 'account_target_bn'] * new_share / old_share
    results.append(dict(line=line, old_factor=old_factor, recomputed_factor=new_factor,
                        aggregate_scaled_delta_bn=t * (old_factor - 1),
                        cell_recomputed_delta_bn=t * (new_factor - 1),
                        difference_bn=t * (new_factor - old_factor)))
source_paths = [
    f / 'cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet',
    f / 'dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet',
    m / 'cps_cells.csv', m / 'ratios.csv', m / 'translation_account.csv',
    f / 'main_case_2026_09_24/package.cjs',
    f / 'cps_imputation_keys_2026_09_23/combine_onbooks_lane.py',
    f / 'medical_ethnicity_pooled_2026_09_23/translate.py',
]
pins = {}
for source in source_paths:
    with source.open('rb') as handle:
        pins[str(source.relative_to(root))] = hashlib.file_digest(handle, 'sha256').hexdigest()
out = dict(scope='Raw medical composition interaction before LTSS carve-out; no model mutations.',
           sources_sha256=pins,
           row4_factors=factors, lines=results,
           total_difference_bn=sum(x['difference_bn'] for x in results))
dest = Path(__file__).resolve().parent / '_cache/medical_composition.json'
dest.parent.mkdir(exist_ok=True, parents=True)
dest.write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(out, indent=2))
