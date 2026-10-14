"""Conditional PES derivative through the coverage producer, with no formula copy.

Native-First: call the producer's pinned source reader, factors and evaluate
functions on its authoritative pricing cache. This is an explicitly selected
common absolute NCE shock, not an official age/sex covariance estimate.
"""
from __future__ import annotations

import copy
import hashlib
import importlib
import json
import sys
import subprocess
from pathlib import Path

import numpy as np


def require(ok,message):
    if not ok:
        raise ValueError('[BLOCKED] source-derived PES gradient: '+message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def validate_receipt(fiscal, receipt):
    require(receipt.get('rule') == 'common_nce_source', 'wrong conditional rule')
    require(bool(receipt.get('inputs')), 'no pinned gradient inputs')
    root=fiscal.parent.parent
    for name, expected in receipt['inputs'].items():
        path=root/name
        require(path.is_file() and digest(path)==expected, 'gradient input changed: '+name)
    checks=receipt.get('finite_difference_checks', {})
    require(all(checks.get(basis, {}).get('passed') is True for basis in ('set','cash')),
            'set/cash finite-difference checks absent')


def job_code_provenance(root, entries, changed):
    """Only traced job producer code stamps may differ in a complete receipt."""
    household='infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py'
    completion='infra/immigration-fiscal/within_group_distribution_2026_09_29/completion_keys.py'
    job='infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct15/completion_jobs.json'
    codes=set(changed)&{household,completion}
    require(set(changed)<={household,completion,job},'untraced code/data dependency changed: '+str(changed))
    require(codes and job in changed,'incomplete producer code/receipt drift pair')
    current=json.loads((root/job).read_text())
    proof={}
    for relative,declared in current['source_sha256'].items():
        name='infra/immigration-fiscal/'+relative
        require(name in entries and digest(root/name)==declared,'job receipt does not name current source: '+relative)
        proof[name]={'original_sha256':entries[name]['sha256'],'current_sha256':declared}
        current['source_sha256'][relative]=entries[name]['sha256']
    restored=(json.dumps(current,indent=2)+'\n').encode()
    require(hashlib.sha256(restored).hexdigest()==entries[job]['sha256'],
            'job receipt changed beyond code stamps; identities/numeric metadata are not equal')
    require(all(name in proof for name in codes),'changed code is absent from job source stamps')
    return {'code_stamps':proof,'restored_receipt_sha256':entries[job]['sha256'],
            'current_receipt_sha256':digest(root/job),'receipt_data_exact':True}


def validate_source_recipe(fiscal, manifest, manifest_api):
    """Recover exact recipe provenance only after bounded native output proofs."""
    root=fiscal.parent.parent
    recipe=json.loads(manifest.read_text())
    owner=Path(__file__).resolve().parent
    out=owner/'_cache/pes_recipe'/manifest.stem
    household='infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py'
    job='infra/immigration-fiscal/within_group_distribution_2026_09_29/_cache/oct15/completion_jobs.json'
    entries={row['path']:row for row in recipe['files']}
    changed=[name for name,row in entries.items() if digest(root/name)!=row['sha256']]
    if not changed:
        manifest_api.validate_manifest(manifest,recipe['route'])
        return {'method':'current bytes match original frozen recipe','recovered':[]}
    provenance_proof=job_code_provenance(root,entries,changed)
    commit='b35ac8fb533b26c797abd2e03f3610b79bbadd73'
    run=subprocess.run(['git','-C',str(root),'show',commit+':'+household],
                       capture_output=True,env=dict(__import__('os').environ,GIT_OPTIONAL_LOCKS='0'))
    if set(changed)!={household,job} or run.returncode!=0 or hashlib.sha256(run.stdout).hexdigest()!=entries[household]['sha256']:
        basis='cash' if manifest.stem.endswith('_cash') else 'set'
        replay=owner/'_cache/pes_replay'
        parity=replay/f'parity_{basis}.json'
        require(parity.is_file(),'exact historical source unavailable; owned native producer replay required')
        verified=json.loads(parity.read_text())
        require(verified.get('passed') and verified['source_code_sha256']==digest(root/household),
                'owned replay receipt is stale or failed')
        require(verified['principal_cache_sha256']==digest(fiscal/f'coverage_bound_2026_10_14/_cache/oct15/{basis}/pricing.npz'),
                'principal pricing cache changed after exact native replay')
        with np.load(fiscal/f'coverage_bound_2026_10_14/_cache/oct15/{basis}/pricing.npz') as principal:
            principal_keys=set(principal.files)
        require(len(principal_keys)==16 and set(verified['array_checks'])==principal_keys
                and all(v.get('exact') for v in verified['array_checks'].values()),
                'owned native replay lacks every-array parity')
        require(verified['principal_cache_sha256']==verified['replay_cache_sha256'],
                'owned native replay changed compressed pricing cache bytes')
        own_manifest=root/verified['manifest']
        require(digest(own_manifest)==verified['manifest_sha256'],'owned replay manifest changed')
        manifest_api.validate_manifest(own_manifest,recipe['route'])
        own_audit=replay/f'derived/pricing_audit_oct15_{basis}.json'
        own_cache=replay/f'_cache/oct15/{basis}/pricing.npz'
        original_audit=fiscal/f'coverage_bound_2026_10_14/derived/pricing_audit_oct15_{basis}.json'
        old=json.loads(original_audit.read_text())
        new=json.loads(own_audit.read_text())
        require(new['adapter_sha256']==verified['source_adapter_sha256']==digest(fiscal/'coverage_bound_2026_10_14/export_pricing.py'),
                'fresh native replay adapter provenance changed')
        provenance={'national_keys_sha256','dependency_manifest_sha256','adapter_sha256'}
        require({k:v for k,v in old.items() if k not in provenance}==
                {k:v for k,v in new.items() if k not in provenance},
                'native replay changed economic/decomposition audit fields')
        require(digest(own_cache)==verified['replay_cache_sha256'],'owned cache changed after exact replay')
        return dict(method=verified['method'],source_manifest_sha256=digest(manifest),
                    snapshot_manifest=verified['manifest'],snapshot_manifest_sha256=verified['manifest_sha256'],
                    parity_receipt=str(parity.relative_to(root)),parity_receipt_sha256=digest(parity),
                    replay_audit=str(own_audit.relative_to(root)),replay_audit_sha256=digest(own_audit),
                    replay_cache=str(own_cache.relative_to(root)),replay_cache_sha256=digest(own_cache),
                    audit_semantic_parity=True,
                     job_code_provenance=provenance_proof,
                    source_code_sha256=verified['source_code_sha256'],recovered=[])
    require(run.returncode==0 and hashlib.sha256(run.stdout).hexdigest()==entries[household]['sha256'],
            'adoption snapshot does not contain exact pinned household source')
    old_code=run.stdout
    current=json.loads((root/job).read_text())
    key='within_group_distribution_2026_09_29/households.py'
    require(current['source_sha256'][key]==digest(root/household),'current job receipt does not name current household source')
    current['source_sha256'][key]=entries[household]['sha256']
    old_job=(json.dumps(current,indent=2)+'\n').encode()
    require(hashlib.sha256(old_job).hexdigest()==entries[job]['sha256'],
            'job receipt changed beyond household code hash; numeric/identity equality not proven')
    recovered=[]
    out.mkdir(parents=True,exist_ok=True)
    for name,value in ((household,old_code),(job,old_job)):
        target=out/Path(name).name
        require(len(value)==entries[name]['bytes'],'frozen recipe byte count differs')
        target.write_bytes(value)
        recovered.append(dict(original_path=name,snapshot_path=str(target.relative_to(root)),
                              original_sha256=entries[name]['sha256'],current_sha256=digest(root/name),
                              source_git_commit=commit if name==household else None))
        entries[name]['path']=str(target.relative_to(root))
    copied=out/'manifest.json'
    copied.write_text(json.dumps(recipe,indent=2)+'\n')
    manifest_api.validate_manifest(copied,recipe['route'])
    return dict(method='exact immutable producer recipe recovered; current migrated code is not enrolled',
                source_manifest_sha256=digest(manifest),snapshot_manifest=str(copied.relative_to(root)),
                snapshot_manifest_sha256=digest(copied),recovered=recovered)


def derive(fiscal,coverage):
    lane=fiscal/'coverage_bound_2026_10_14'
    source=fiscal/coverage['file']
    require(not coverage.get('stub') and digest(source)==coverage['sha256'],
            'coverage source is stale or STUB')
    principal=json.loads(source.read_text())
    require(principal['key']=='oct15','wrong source epoch')
    sys.path.insert(0,str(lane))
    C=importlib.import_module('coverage_bound')
    tables=importlib.import_module('source_tables')
    manifest_api=importlib.import_module('dependency_manifest')
    pricing=importlib.import_module('export_pricing')
    for module,name in ((C,'coverage_bound.py'),(tables,'source_tables.py'),
                        (manifest_api,'dependency_manifest.py'),(pricing,'export_pricing.py')):
        require(Path(module.__file__).resolve()==(lane/name).resolve(),
                'an imported source module belongs to another lane: '+name)
    rates,base=tables.load()  # verifies pinned primary PDF/control tables
    se=rates['hispanic']['all']['se_pct']/100
    require(abs(se-.0053)<1e-12,'published overall Hispanic PES SE is not 0.53 points')
    receipt={'rule':'common_nce_source','se_fraction':float(se),
             'source':'2020 PES Hispanic overall NCE SE, pinned Census Table C and national positive control',
             'covariance_rule':'[APPROX] one common absolute Hispanic NCE-fraction shock to all PES-priced age/sex cells; DA-priced children and 2024 controls fixed. Shape uncertainty is excluded. Consumer treats this scalar instrument as independent of CPS.',
             'derivative_bn_per_fraction':{},'finite_difference_checks':{},
             'inputs':{str(source.relative_to(fiscal.parent.parent)):digest(source)},
             'coverage_file_sha256':coverage['sha256'],
             'derivative_method':'producer factors/evaluate; centred differences at h=1e-4 and 1e-5, Richardson extrapolation, independent check at h=1e-6'}
    own_source=Path(__file__).resolve()
    receipt['inputs'][str(own_source.relative_to(fiscal.parent.parent))]=digest(own_source)
    for name in ('coverage_bound.py','source_tables.py','dependency_manifest.py','export_pricing.py','national_keys.py',
                 'inputs/pins.json','inputs/pes_cross.pdf','inputs/pes_national.pdf',
                 'inputs/controls/base_adjustments.csv','inputs/controls/base_adjustments_sex.csv'):
        p=lane/name
        receipt['inputs'][str(p.relative_to(fiscal.parent.parent))]=digest(p)
    for basis in ('set','cash'):
        manifest=lane/f'inputs/pricing_dependencies_oct15_{basis}.json'
        audit_path=lane/f'derived/pricing_audit_oct15_{basis}.json'
        cache_path=lane/f'_cache/oct15/{basis}/pricing.npz'
        require(json.loads(manifest.read_text())['route']==f'coverage oct15 personal flat pricing {basis}',
                'wrong frozen pricing manifest route')
        recovery=validate_source_recipe(fiscal,manifest,manifest_api)
        receipt.setdefault('frozen_recipe',{})[basis]=recovery
        for recovered in recovery['recovered']:
            receipt['inputs'][recovered['snapshot_path']]=recovered['original_sha256']
        if recovery.get('snapshot_manifest'):
            receipt['inputs'][recovery['snapshot_manifest']]=recovery['snapshot_manifest_sha256']
        if recovery.get('parity_receipt'):
            receipt['inputs'][recovery['parity_receipt']]=recovery['parity_receipt_sha256']
            for name in ('replay_audit','replay_cache'):
                receipt['inputs'][recovery[name]]=recovery[name+'_sha256']
        audit=json.loads(audit_path.read_text())
        require(audit['case']=='oct15' and audit['basis']==basis,'pricing audit set/epoch')
        require(digest(cache_path)==audit['pricing_cache_sha256'],'original audit pricing cache changed')
        if recovery.get('replay_audit'):
            root=fiscal.parent.parent
            C.validate_cache_receipt(json.loads((root/recovery['replay_audit']).read_text()),
                                     root/recovery['snapshot_manifest'],root/recovery['replay_cache'])
        else:
            C.validate_cache_receipt(audit,manifest,cache_path)
        with np.load(cache_path) as cache:
            data={k:cache[k] for k in ('age','sex','arrival','hispanic','generation','weights','net_id',
                                       'excluded_use_prices','constructed_piece_prices','base_piece_prices')}
        # Every central added-descendant factor is exactly zero and remains zero
        # under this Hispanic-only shock. These source branches therefore have
        # zero contribution, without loading their two large unused matrices.
        n=len(data['age'])
        data['added_weights']=np.broadcast_to(np.asarray(0.0),(n,161))
        data['net_added']=np.zeros((2,n,161))
        # The producer's constructed-person rule (round 3, R3-12), by its own function.
        pricing.constructed_prices(data,audit)
        del data['constructed_piece_prices'],data['base_piece_prices'],data['excluded_use_prices']
        def price(shift):
            perturbed=copy.deepcopy(rates)
            for row in perturbed['hispanic'].values():
                row['nce_pct']+=shift*100
            f,af=C.factors(data,perturbed,base)
            require(not np.any(af),'Hispanic shock unexpectedly changes added-descendant factors')
            estimates,_,_=C.evaluate(data,f,af)
            return np.asarray([v[0] for v in estimates],float)
        point=price(0.0)
        expected=np.asarray([principal['sets'][basis]['ends'][end]['coverage_bn'] for end in ('low','high')])
        require(np.allclose(point,expected,rtol=0,atol=1e-9),'producer point-price reconstruction')
        gradients={}
        for h in (1e-4,1e-5,1e-6):
            gradients[h]=(price(h)-price(-h))/(2*h)
        extrapolated=gradients[1e-5]+(gradients[1e-5]-gradients[1e-4])/99
        difference=np.abs(extrapolated-gradients[1e-6])
        tolerance=np.maximum(1e-6,np.abs(extrapolated)*1e-7)
        require(np.isfinite(extrapolated).all() and np.all(difference<=tolerance),
                'independent finite-difference check did not converge')
        receipt['derivative_bn_per_fraction'][basis]={end:float(extrapolated[i]) for i,end in enumerate(('low','high'))}
        receipt['finite_difference_checks'][basis]={'point_bn':point.tolist(),
            'max_difference_bn_per_fraction':float(difference.max()),
            'absolute_tolerance':1e-6,'relative_tolerance':1e-7,'passed':True}
        for p in (manifest,audit_path,cache_path):
            receipt['inputs'][str(p.relative_to(fiscal.parent.parent))]=digest(p)
        del data
    return receipt
