"""Coverage's conditional CPS construction on the account's shared 161 weights."""
import importlib
import json
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

from coverage_pes import digest, require, validate_source_recipe


def derive(fiscal, coverage, cps_zip, reps):
    root = fiscal.parent.parent
    lane = fiscal / 'coverage_bound_2026_10_14'
    sys.path.insert(0, str(lane))
    C = importlib.import_module('coverage_bound')
    tables = importlib.import_module('source_tables')
    deps = importlib.import_module('dependency_manifest')
    pricing = importlib.import_module('export_pricing')
    for module, name in ((C, 'coverage_bound.py'), (tables, 'source_tables.py'), (deps, 'dependency_manifest.py'),
                         (pricing, 'export_pricing.py')):
        require(Path(module.__file__).resolve() == (lane/name).resolve(), 'wrong coverage CPS producer module: '+name)
    frame_lane = fiscal / 'generation_account_2026_09_24'
    sys.path.insert(0, str(frame_lane))
    frame_source = importlib.import_module('frame')
    require(Path(frame_source.__file__).resolve() == (frame_lane/'frame.py').resolve()
            and frame_source.REPS == reps and frame_source.CPS_ZIP.resolve() == cps_zip.resolve(),
            'coverage and main CPS source/replicate axis differ')
    require(digest(cps_zip) == frame_source.CPS_SHA, 'official CPS source differs from authoritative pin')
    frame_path = fiscal / 'generation_account_2026_09_24/_cache/asec25_generation.parquet'
    frame = pd.read_parquet(frame_path, columns=['PH_SEQ', 'PPPOS', *reps])
    with zipfile.ZipFile(cps_zip) as z:
        official = pd.read_csv(z.open('asec_csv_repwgt_2025.csv'), usecols=['h_seq', 'PPPOS', *reps])
    official = official.rename(columns={'h_seq': 'PH_SEQ'})
    joined = frame[['PH_SEQ', 'PPPOS']].merge(official, on=['PH_SEQ', 'PPPOS'],
                                           how='left', validate='one_to_one')
    require(np.array_equal(frame[reps].to_numpy(), joined[reps].to_numpy()),
            'coverage canonical frame differs from main official CPS IDs/replicate columns')
    ids = pd.MultiIndex.from_frame(frame[['PH_SEQ', 'PPPOS']])
    del frame, joined, official
    source_path = fiscal / coverage['file']
    require(digest(source_path) == coverage['sha256'] and not coverage.get('stub'), 'coverage principal changed')
    principal = json.loads(source_path.read_text())
    rates, base = tables.load()
    receipt = {'replicate_ids': reps, 'frame_proof': 'canonical PH_SEQ/PPPOS weights equal official main CPS zip in every pwwgt0..160 column; native row4 calibration retained',
               'rule': 'conditional source CPS construction, producer calibrated prices/model held; shared vectors retain covariance with main CPS blocks; PES instrument remains separate',
               'vectors_bn': {}, 'se_bn': {}, 'inputs': {str(p.relative_to(root)): digest(p) for p in
                    (source_path, frame_path, cps_zip, Path(__file__), frame_lane/'frame.py')}, 'gates': {}}
    for name in ('coverage_bound.py', 'source_tables.py', 'dependency_manifest.py', 'export_pricing.py', 'inputs/pins.json',
                 'inputs/pes_cross.pdf', 'inputs/pes_national.pdf', 'inputs/controls/base_adjustments.csv',
                 'inputs/controls/base_adjustments_sex.csv'):
        receipt['inputs'][str((lane/name).relative_to(root))] = digest(lane/name)
    for basis in ('set', 'cash'):
        recovery = validate_source_recipe(fiscal, lane / f'inputs/pricing_dependencies_oct15_{basis}.json', deps)
        replay = Path(__file__).resolve().parent/'_cache/pes_replay'
        parity = json.loads((replay/f'parity_{basis}.json').read_text())
        own_manifest = root/parity['manifest']
        cache_path = replay/f'_cache/oct15/{basis}/pricing.npz'
        require(parity.get('passed') and parity['principal_cache_sha256'] == digest(lane/f'_cache/oct15/{basis}/pricing.npz')
                and parity['replay_cache_sha256'] == digest(cache_path)
                and parity['manifest_sha256'] == digest(own_manifest)
                and all(q['exact'] for q in parity['array_checks'].values()), 'owned coverage CPS cache parity changed')
        deps.validate_manifest(own_manifest,f'coverage oct15 personal flat pricing {basis}')
        own_audit = replay/f'derived/pricing_audit_oct15_{basis}.json'
        C.validate_cache_receipt(json.loads(own_audit.read_text()),own_manifest,cache_path)
        with np.load(cache_path) as cache:
            require(cache['weights'].shape[1] == 161, 'coverage replicate count/order')
            own_ids = pd.MultiIndex.from_arrays([cache['person_ph_seq'], cache['person_pppos']])
            require(not own_ids.has_duplicates and np.all(ids.get_indexer(own_ids) >= 0), 'coverage persons absent from main CPS frame')
            data = {k: cache[k] for k in ('age', 'sex', 'arrival', 'hispanic', 'generation', 'weights', 'net_id',
                                          'excluded_use_prices', 'constructed_piece_prices', 'base_piece_prices')}
        n = len(data['age'])
        data['added_weights'] = np.broadcast_to(np.asarray(0.), (n, 161))
        data['net_added'] = np.zeros((2, n, 161))
        # The producer's constructed-person rule (round 3, R3-12): missed people take zero on
        # administratively complete justice use. Its own function, so the rule has one definition.
        pricing.constructed_prices(data, json.loads(own_audit.read_text()))
        del data['constructed_piece_prices'], data['base_piece_prices'], data['excluded_use_prices']
        f, af = C.factors(data, rates, base)
        require(not np.any(af), 'unexpected added-descendant coverage factor')
        estimates, _, _ = C.evaluate(data, f, af)
        receipt['vectors_bn'][basis], receipt['se_bn'][basis] = {}, {}
        for i, end in enumerate(('low', 'high')):
            vector = np.asarray(estimates[i], float)
            se = float(np.sqrt(4 / 160 * np.sum((vector[1:] - vector[0]) ** 2)))
            expected = principal['sets'][basis]['ends'][end]
            require(vector.shape == (161,) and np.isfinite(vector).all(), 'invalid coverage CPS vector')
            require(abs(vector[0] - expected['coverage_bn']) < 1e-9 and
                    abs(se - expected['cps_replicate_se_bn']) < 1e-9, 'coverage point/SDR differs from source')
            receipt['vectors_bn'][basis][end] = vector.tolist()
            receipt['se_bn'][basis][end] = se
        receipt['inputs'][str(cache_path.relative_to(root))] = digest(cache_path)
        for path in (own_manifest, own_audit, replay/f'parity_{basis}.json'):
            receipt['inputs'][str(path.relative_to(root))] = digest(path)
        receipt['gates'][basis] = {'point_and_sdr_1e_9': True, 'shared_official_ids': True, 'recipe': recovery}
        del data
    return receipt


if __name__ == '__main__':
    owner = Path(__file__).resolve().parent
    fiscal = owner.parent
    meta = json.loads((fiscal/'main_case_2026_10_15/derived/corrections.json').read_text())['meta']
    require(meta.get('adopted') == '2026-10-15', 'coverage CPS requires adopted payload')
    receipt = derive(fiscal, meta['coverage'], fiscal/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip',
                     [f'pwwgt{i}' for i in range(161)])
    sys.path.insert(0, str(fiscal/'scripts'))
    from memory_budget import require_within_budget
    peak = require_within_budget('coverage CPS source proof')
    out = owner/'derived/oct15/coverage_cps_replicates.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(receipt, indent=2)+'\n')
    print(f'PASS coverage CPS source points/SDR/shared official IDs; physical {peak/1e9:.3f}GB')
