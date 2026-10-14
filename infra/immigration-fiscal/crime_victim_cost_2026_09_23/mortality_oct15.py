"""Native mortality prices for every live crime footing; historical files stay fixed."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import time

import numpy as np
import pandas as pd

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent
ROOT=FISCAL.parent.parent
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE))
import mortality_arms as source
sys.path.insert(0,str(FISCAL/'coverage_bound_2026_10_14'))
from dependency_manifest import guard,validate_manifest

OUT=HERE/'derived/oct15'
CHOICES=(('dot_uniform',0.0),('dot_life_years',0.0),('dot_life_years',0.03))
FOOTINGS=(*source.FOOTINGS,'custody_unmixed')
MANIFEST=HERE/'inputs/mortality_dependencies_oct15.json'
ROUTE='crime mortality oct15 fixed-v7 quantities'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def require(ok,message):
    if not ok:
        raise ValueError('[BLOCKED] live crime mortality: '+message)


def csv_bytes(frame):
    return frame.to_csv(index=False,lineterminator='\n',float_format='%.17g').encode()


def publish(files,receipt):
    """Prepare all bytes, rename files, publish checksum receipt last."""
    OUT.mkdir(parents=True,exist_ok=True)
    receipt['outputs_sha256']={name:hashlib.sha256(value).hexdigest() for name,value in files.items()}
    with tempfile.TemporaryDirectory(prefix='.mortality-',dir=OUT) as stage:
        temporary=Path(stage)
        for name,value in files.items():
            (temporary/name).write_bytes(value)
        (temporary/'mortality_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        for name in files:
            os.replace(temporary/name,OUT/name)
        os.replace(temporary/'mortality_receipt.json',OUT/'mortality_receipt.json')


def build(tracker):
    started=time.perf_counter()
    source.valuation.check_pins()
    primary=json.loads((HERE/'inputs/pins.json').read_text())['files']
    frames=[]
    totals=[]
    dot=source.valuation.dot_vsl()
    for footing in FOOTINGS:
        legacy=source.active_victim_detail(footing,'legacy')
        nonfatal=legacy[legacy.offence.ne('Murder')]
        for valuation,rate in CHOICES:
            detail=source.active_victim_detail(footing,valuation,rate)
            require(np.array_equal(detail[detail.offence.ne('Murder')].cost_full.to_numpy(),nonfatal.cost_full.to_numpy()),
                    'mortality price changed nonfatal costs')
            murder=detail[detail.offence.eq('Murder')]
            require(len(murder)>0 and np.isfinite(murder[['outside_victims','unit_full','cost_full']].to_numpy()).all(),
                    'missing/nonfinite homicide source')
            if valuation=='dot_uniform':
                require(np.allclose(murder.unit_full,dot,rtol=0,atol=1e-8),'every central death must have uniform DOT VSL')
            require(np.allclose(detail.cost_full,detail.outside_victims*detail.unit_full,rtol=0,atol=1e-6),
                    'victim row dollar closure')
            detail['valuation']=valuation
            frames.append(detail)
            totals.append(dict(footing=footing,valuation=valuation,real_discount_rate=rate,
                               victim_cost_bn=float(detail.cost_full.sum()/1e9),
                               mortality_bn=float(murder.cost_full.sum()/1e9),
                               homicide_deaths=float(murder.outside_victims.sum()),
                               legacy_victim_cost_bn=float(legacy.cost_full.sum()/1e9),
                               mortality_price_change_bn=float((detail.cost_full.sum()-legacy.cost_full.sum())/1e9)))
    details=pd.concat(frames,ignore_index=True)
    require(len(totals)==len(FOOTINGS)*len(CHOICES),'incomplete mortality registry')
    inputs={entry['path']:entry['sha256'] for entry in primary}
    for path in (HERE/'mortality_arms.py',HERE/'vsl_standard.py',Path(__file__),
                 HERE/'inputs/pins.json',HERE/'derived/shr_p_offender_given_victim.csv'):
        inputs[str(path.relative_to(ROOT))]=digest(path)
    manifest_hash=tracker.finish()
    inputs.update({entry['path']:entry['sha256'] for entry in tracker.entries.values()})
    inputs[str(MANIFEST.relative_to(ROOT))]=manifest_hash
    sys.path.insert(0,str(FISCAL/'scripts'))
    from memory_budget import require_within_budget
    footprint=require_within_budget('live crime mortality')
    receipt=dict(case='oct15',source_quantity_case='frozen v7 social frame',inputs_sha256=inputs,
                 valuation_choices=[dict(valuation=v,real_discount_rate=r) for v,r in CHOICES],
                 footings=list(FOOTINGS),dot_vsl_2024usd=dot,
                 life_year_scope='SHR 2024 victim ages conditional on known Hispanic first offender; common NVSS period table, age40 calibration; source assumptions fixed',
                 gates=dict(primary_pins=True,all_central_deaths_uniform=True,nonfatal_unchanged=True,
                            all_rows_close=True,all_basis_rate_footings=True,physical_footprint=True))
    publish({'mortality_detail.csv':csv_bytes(details),'mortality_arms.csv':csv_bytes(pd.DataFrame(totals)),
             'mortality_age_profile.csv':csv_bytes(source.victim_age_profile())},receipt)
    print(f'PASS live crime mortality: {len(totals)} footing/basis/rate cells; {time.perf_counter()-started:.3f}s; physical {footprint/1e9:.3f}GB')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--capture',action='store_true',help='explicit discovery; normal execution requires all pinned read paths')
    arguments=parser.parse_args()
    with guard(capture=arguments.capture,manifest=MANIFEST,route=ROUTE) as tracker:
        build(tracker)
