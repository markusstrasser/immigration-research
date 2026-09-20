#!/usr/bin/env python3
"""Exercise source verification with intact and independently corrupted bundles."""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def fixture(bundle, target):
    target.mkdir()
    shutil.copytree(bundle / 'derived', target / 'derived')
    for name in ['raw', 'codebooks']:
        (target / name).symlink_to(bundle / name, target_is_directory=True)
    manifest = json.loads((bundle / 'manifest.json').read_text())
    for item in manifest['inputs']:
        rel = Path(item['output_path']).relative_to(bundle)
        item['output_path'] = str(target / rel)
    (target / 'manifest.json').write_text(json.dumps(manifest))
    refresh_output_hashes(target)


def refresh_output_hashes(target):
    records = [{'path': p.relative_to(target).as_posix(), 'bytes': p.stat().st_size,
                'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}
               for p in sorted((target / 'derived').glob('*.csv'))]
    (target / 'output_hashes.json').write_text(json.dumps(records))


def mutate(target, name):
    path = target / 'derived/county_year_outcomes.csv'
    if name in {'missing_year', 'masked_population', 'earnings_x1000', 'altered_flag', 'altered_returns'}:
        d = pd.read_csv(path, dtype={'fips': str}, low_memory=False)
        if name == 'missing_year':
            d = d[d.year != 2011]
        elif name == 'masked_population':
            d.loc[d.year == 2011, 'bea_population'] = float('nan')
        elif name == 'earnings_x1000':
            d['bea_workplace_earnings_dollars'] *= 1000
        elif name == 'altered_flag':
            row = d.index[d.irs_wages_dollars.notna()][0]
            d.loc[row, 'irs_wages_dollars_zero_ambiguous'] = True
        elif name == 'altered_returns':
            d['irs_returns'] *= 1000
        d.to_csv(path, index=False)
        # Deliberately repair hashes: value/coverage checks must reject these cases.
        refresh_output_hashes(target)
    elif name in {'omitted_input_entry', 'omitted_input_hash'}:
        path = target / 'manifest.json'
        m = json.loads(path.read_text())
        if name == 'omitted_input_entry':
            m['inputs'].pop()
        else:
            m['inputs'][0].pop('sha256')
        path.write_text(json.dumps(m))
    elif name in {'omitted_output_entry', 'omitted_output_hash', 'empty_output_hashes'}:
        path = target / 'output_hashes.json'
        records = json.loads(path.read_text())
        if name == 'omitted_output_entry':
            records.pop()
        elif name == 'empty_output_hashes':
            records = []
        else:
            records[0].pop('sha256')
        path.write_text(json.dumps(records))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--bundle', type=Path, required=True)
    parser.add_argument('--source-lock', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    bundle = args.bundle.absolute()
    verifier = Path(__file__).with_name('verify_corpus.py')
    results = []
    cases = {'missing_year': 'derived year coverage mismatch',
             'masked_population': 'missingness mismatch: bea_population',
             'earnings_x1000': 'direct source value mismatch: bea_workplace_earnings_dollars',
             'altered_flag': 'direct source label/flag mismatch: irs_wages_dollars_zero_ambiguous',
             'altered_returns': 'direct source value mismatch: irs_returns',
             'omitted_input_entry': 'input manifest artifact set mismatch',
             'omitted_input_hash': 'input manifest differs from source lock',
             'omitted_output_entry': 'derived output artifact set mismatch',
             'omitted_output_hash': 'missing hash/size',
             'empty_output_hashes': 'empty output hashes'}
    with tempfile.TemporaryDirectory(prefix='county-verifier-regression-', dir='/private/tmp') as directory:
        work = Path(directory)
        # Even valid runs write their verification receipt only inside fixtures.
        for name, optimize in [('valid', False), ('valid_optimized', True), *[(n, True) for n in cases]]:
            target = work / name
            fixture(bundle, target)
            if name in cases:
                mutate(target, name)
            command = [sys.executable, *(['-O'] if optimize else []), str(verifier),
                       '--out', str(target), '--source-lock', str(args.source_lock.absolute())]
            result = subprocess.run(command, capture_output=True, text=True)
            if name in cases:
                require(result.returncode != 0 and cases[name] in result.stderr,
                        f'{name}: expected failure absent: {result.stdout}\n{result.stderr}')
                details = {'case': name, 'optimized': optimize, 'rejected_as_expected': True,
                           'expected_reason': cases[name]}
            else:
                require(result.returncode == 0, f'{name} failed: {result.stderr}')
                details = {'case': name, 'optimized': optimize, 'result': json.loads(result.stdout)}
            results.append(details)
            print(json.dumps(details), flush=True)
    report = {'status': 'PASS', 'valid_runs': 2, 'negative_cases': len(cases),
              'source_bytes_mutated': False, 'results': results}
    if args.report:
        args.report.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': 'PASS', 'valid_runs': 2, 'negative_cases': len(cases)}))


if __name__ == '__main__':
    main()
