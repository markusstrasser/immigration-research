"""Verify the source-declared zero EIP1 catch-up under its actual tax-unit rule."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import time

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PRODUCER = HERE.parent / 'backcast_pandemic_measured_2026_09_28/measure_shares.py'
OUT = HERE / 'derived/oct15/pandemic_zero_audit.json'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def require_zero():
    audit = json.loads(OUT.read_text())
    if audit['survey_year'] != 2021 or audit['income_year'] != 2020 or audit['payment_year'] != 2021:
        raise ValueError('[BLOCKED] EIP1 catch-up calendar mapping changed')
    for path, expected in audit['inputs'].items():
        if digest(ROOT / path) != expected:
            raise ValueError('[BLOCKED] stale EIP1 zero source: ' + path)
    if audit['national_bn'] != 0 or audit['nonzero_records'] != 0 or audit['max_payment_usd'] != 0:
        raise ValueError('[BLOCKED] EIP1 catch-up is no longer structurally zero')
    return 0.0


def main():
    started = time.perf_counter()
    spec = importlib.util.spec_from_file_location('backcast_zero_source', PRODUCER)
    source = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(source)
    frame, households = source.load(2021)  # Survey2021 reports calendar income2020.
    masks = source.no_ssn_masks(frame, households)
    catchup = source.eip_parts(frame, masks['borjas'], 2021)['eip1_catchup']
    nonzero = int(np.count_nonzero(catchup))
    national = float(np.dot(catchup, frame.pwwgt0.to_numpy()) / 1e9)
    if nonzero or national != 0:
        raise ValueError('[BLOCKED] source-declared Borjas EIP1 catch-up has positive payment')
    inputs = [PRODUCER, Path(source.impute.__code__.co_filename), source.SOURCES[2021][0], Path(__file__)]
    audit = dict(survey_year=2021, income_year=2020, payment_year=2021, status='borjas',
                 rule='EIP1 amended credit less advance; producer SSN spouse rule; zero verified on every tax unit',
                 national_bn=national, nonzero_records=nonzero, max_payment_usd=float(np.max(catchup)),
                 inputs={str(p.relative_to(ROOT)): digest(p) for p in inputs})
    sys.path.insert(0, str(HERE.parent / 'scripts'))
    from memory_budget import require_within_budget
    footprint = require_within_budget('EIP structural-zero verification')
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(audit, indent=2, sort_keys=True) + '\n')
    print(f'PASS EIP1 catch-up national amount0, {nonzero} nonzero records; seconds={time.perf_counter()-started:.3f}; physical_footprint={footprint}')


if __name__ == '__main__':
    main()
