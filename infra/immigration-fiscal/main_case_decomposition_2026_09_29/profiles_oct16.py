"""Own national age-profile bridge for source21's restricted donor key.

Raw national donor totals are normalized separately. No Mexican-origin
translation or Mexican calibration is applied to the average-resident key.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent


def main(*, probe=False):
    case=json.loads((FISCAL/'main_case_2026_10_16/derived/summary.json').read_text())
    if case['v9']['status']!='adopted' and not probe:
        raise ValueError('[BLOCKED] source21 production profiles require the adopted oct16 case')
    source=FISCAL/'spending_keys_r5_2026_10_15/derived/item21.json'
    cells=FISCAL/'spending_keys_r5_2026_10_15/derived/item21_key_cells.csv'
    frame=FISCAL/'generation_account_2026_09_24/_cache/asec25_generation.parquet'
    m=json.loads(source.read_text())
    tab=pd.read_csv(cells).set_index(['key','band','nativity'])['mean']
    d=pd.read_parquet(frame,columns=['A_AGE','PENATVTY','PRPERTYP','pwwgt0','PUB','PRIV'])
    civ=(d.PRPERTYP.eq(2)|d.A_AGE.lt(15)).to_numpy()
    exposed=~(d.PUB.eq(0)&d.PRIV.eq(0)).to_numpy()
    bands=np.digitize(d.A_AGE.to_numpy(),[18,35,50,65])
    labels=['0-17','18-34','35-49','50-64','65+']
    born=np.where(d.PENATVTY.eq(57),'us_born','foreign_born')
    keys=pd.MultiIndex.from_arrays([[labels[b] for b in bands],born])
    edges=np.array(list(range(25))+list(range(25,81,5))+[85])
    bins=np.searchsorted(edges,d.A_AGE.to_numpy(),side='right')-1
    w=d.pwwgt0.to_numpy(float)
    out={'edges':edges.tolist(),'national_population_by_age':np.bincount(bins[civ],weights=w[civ],minlength=len(edges)).tolist(),
         'national_keys':{},'source_hashes':{},'rule':__doc__}
    for kind in ('old','new'):
        donor=tab.loc[kind].reindex(keys).to_numpy(float)*exposed
        if not np.isfinite(donor).all():
            raise ValueError('[BLOCKED] item21 national age donor cell missing')
        amounts=np.bincount(bins[civ],weights=(donor*w)[civ],minlength=len(edges))
        if abs(amounts.sum()/m['donor_totals'][kind]-1)>1e-12:
            raise ValueError('[BLOCKED] item21 national raw donor total differs from source')
        out['national_keys'][kind]=amounts.tolist()
    for file in (source,cells,frame):
        out['source_hashes'][str(file.relative_to(FISCAL))]=hashlib.sha256(file.read_bytes()).hexdigest()
    sys.path.insert(0,str(FISCAL/'scripts'))
    from memory_budget import require_within_budget
    require_within_budget('item21 own national age profiles')
    if not probe:
        (HERE/'derived/health_national_profiles_oct16.json').write_text(json.dumps(out,indent=1)+'\n')
    print(('CANDIDATE PROBE: no output written; ' if probe else 'PASS ')+
          'source21 national donor totals and own age profiles; no Mexican-origin ratio transferred')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--probe-only',action='store_true')
    main(probe=parser.parse_args().probe_only)
