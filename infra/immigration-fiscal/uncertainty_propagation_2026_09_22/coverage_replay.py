"""Replay the producer into owned files and verify every frozen cache array."""
import argparse
import contextlib
import gc
import hashlib
import importlib
import json
import os
from pathlib import Path
import shutil
import sys
import time

import numpy as np

OWNER=Path(__file__).resolve().parent
FISCAL=OWNER.parent
PRODUCER=FISCAL/'coverage_bound_2026_10_14'
REPLAY=OWNER/'_cache/pes_replay'
sys.dont_write_bytecode=True
sys.path.insert(0,str(PRODUCER))
from coverage_pes import require,digest


def forbid_upstream_writes(event,args):
    if event=='open':
        path,mode,flags=args
        writing=('w' in (mode or '') or 'a' in (mode or '') or '+' in (mode or '')
                 or flags & (os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC))
        if writing and isinstance(path,(str,bytes)):
            require(Path(os.fsdecode(path)).resolve().is_relative_to(OWNER),
                    'owned replay attempted upstream write: '+os.fsdecode(path))
    elif event in ('os.mkdir','os.remove','os.rename','os.rmdir'):
        for path in args[:2] if event=='os.rename' else args[:1]:
            if isinstance(path,(str,bytes)):
                require(Path(os.fsdecode(path)).resolve().is_relative_to(OWNER),
                        'owned replay attempted upstream mutation: '+os.fsdecode(path))


def require_unchanged(root, start_hashes):
    require(all(digest(root/name)==value for name,value in start_hashes.items()),
            'source dependency changed during owned native replay; discard this receipt')


def main(basis):
    sys.path.insert(0,str(FISCAL/'debt_legacy_2026_09_23'))
    from v8_flow import require_adopted
    require_adopted(FISCAL)
    for kind in ('corrections','corrections_cash'):
        payload=json.loads((FISCAL/f'main_case_2026_10_15/derived/{kind}.json').read_text())
        require(payload['meta'].get('adopted')=='2026-10-15' and not payload['meta']['coverage'].get('stub'),
                'source replay requires adopted non-STUB payload')
    start=time.perf_counter()
    root=FISCAL.parent.parent
    original_manifest=PRODUCER/f'inputs/pricing_dependencies_oct15_{basis}.json'
    dependencies=json.loads(original_manifest.read_text())['files']
    start_hashes={row['path']:digest(root/row['path']) for row in dependencies}
    # The producer's own adapter is audited separately from its read manifest.
    start_hashes['infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py']=digest(PRODUCER/'export_pricing.py')
    exporter=importlib.import_module('export_pricing')
    deps=importlib.import_module('dependency_manifest')
    require(Path(exporter.__file__).resolve()==(PRODUCER/'export_pricing.py').resolve(),'wrong producer adapter')
    REPLAY.mkdir(parents=True,exist_ok=True)
    (REPLAY/'derived').mkdir(exist_ok=True)
    (REPLAY/'inputs/oct15_base').mkdir(parents=True,exist_ok=True)
    for file in ('national_keys.py',f'inputs/oct15_base/lines{"_cash" if basis=="cash" else ""}.json'):
        shutil.copyfile(PRODUCER/file,REPLAY/file)
    manifest=REPLAY/f'inputs/pricing_dependencies_oct15_{basis}.json'
    sys.addaudithook(forbid_upstream_writes)
    old_lane=exporter.LANE
    exporter.LANE=REPLAY
    try:
        with (REPLAY/f'build_{basis}.log').open('w') as log,contextlib.redirect_stdout(log):
            with deps.guard(capture=True,manifest=manifest,route=f'coverage oct15 personal flat pricing {basis}') as tracker:
                exporter.main(tracker,case='oct15',basis=basis)
    finally:
        exporter.LANE=old_lane
    gc.collect()  # release producer frame/closure cycles before two-cache parity
    deps.validate_manifest(manifest,f'coverage oct15 personal flat pricing {basis}')
    require_unchanged(root,start_hashes)
    original=PRODUCER/f'_cache/oct15/{basis}/pricing.npz'
    replay=REPLAY/f'_cache/oct15/{basis}/pricing.npz'
    checks={}
    with np.load(original) as old,np.load(replay) as new:
        require(set(old.files)==set(new.files),'replayed pricing cache array keys differ')
        for name in old.files:
            a,b=old[name],new[name]
            require(a.shape==b.shape and a.dtype==b.dtype,'replayed cache shape/type differs: '+name)
            require(np.array_equal(a,b,equal_nan=True),'replayed pricing cache array differs: '+name)
            checks[name]=dict(shape=list(a.shape),dtype=str(a.dtype),exact=True)
            del a,b
    receipt=dict(basis=basis,method='native producer replay with current code into owned outputs; every cached array exactly matches frozen principal',
                 source_code_sha256=start_hashes['infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py'],
                 source_adapter_sha256=start_hashes['infra/immigration-fiscal/coverage_bound_2026_10_14/export_pricing.py'],
                 source_start_end_sha256=start_hashes,
                 principal_cache_sha256=digest(original),replay_cache_sha256=digest(replay),
                 manifest=str(manifest.relative_to(FISCAL.parent.parent)),manifest_sha256=digest(manifest),
                 array_checks=checks,passed=True)
    sys.path.insert(0,str(FISCAL/'scripts'))
    from memory_budget import require_within_budget
    peak=require_within_budget('owned coverage replay and exact array parity')
    destination=REPLAY/f'parity_{basis}.json'
    require_unchanged(root,start_hashes)
    destination.write_text(json.dumps(receipt,indent=2)+'\n')
    gc.collect()
    print(f'PASS source replay {basis}: {len(checks)} exact arrays; {time.perf_counter()-start:.3f}s; physical {peak/1e9:.3f}GB',flush=True)


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--basis',choices=('set','cash'),required=True)
    main(parser.parse_args().basis)
