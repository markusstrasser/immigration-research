#!/usr/bin/env python3
"""Independently verify every staged county outcome against locked source bytes."""
import argparse
import hashlib
import json
from pathlib import Path

import pandas as pd

YEARS = [2011, *range(2013, 2023)]
STATES = set('01 02 04 05 06 08 09 10 11 12 13 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 44 45 46 47 48 49 50 51 53 54 55 56'.split())
BEA = {'20': 'bea_population', '35': 'bea_workplace_earnings_dollars',
       '36': 'bea_social_insurance_contributions_dollars', '42': 'bea_residence_adjustment_dollars',
       '45': 'bea_residence_net_earnings_dollars', '47': 'bea_transfer_receipts_dollars', '50': 'bea_wages_dollars'}
IRS = {'A00100': ('irs_agi_dollars', 'N1'), 'A00200': ('irs_wages_dollars', 'N00200'),
       'A06500': ('irs_income_tax_A06500_dollars', 'N06500')}
OUTPUTS = {'derived/' + name + '.csv' for name in (
    'county_year_outcomes', 'join_coverage', 'national_sum_diagnostics',
    'bea_combined_geographies_excluded', 'unmatched_geographies', 'ambiguous_zero_cells')}
MISSING = {'', '(D)', '(L)', '(NA)', '(NM)', 'N/A', 'NA', '*', '**', '-', '--'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def county(fips):
    return (fips.str.fullmatch(r'\d{5}') & fips.str[:2].isin(STATES)
            & fips.str[2:].ne('000') & fips.str[2:].lt('900'))


def numeric(series, label):
    text = series.astype(str).str.strip()
    values = pd.to_numeric(text, errors='coerce')
    require(not (values.isna() & ~text.isin(MISSING)).any(), f'unknown source numeric token: {label}')
    return values


def keyed_records(records, key, label):
    require(isinstance(records, list) and len(records) > 0, f'empty {label}')
    require(all(key in r for r in records), f'missing path in {label}')
    result = {r[key]: r for r in records}
    require(len(result) == len(records), f'duplicate paths in {label}')
    return result


def check_hash(path, record, label):
    require('bytes' in record and 'sha256' in record, f'missing hash/size: {label}')
    require(path.is_file(), f'missing file: {label}')
    require(path.stat().st_size == record['bytes'], f'size mismatch: {label}')
    require(digest(path) == record['sha256'], f'hash mismatch: {label}')


def verify_integrity(out, source_lock):
    manifest = json.loads((out / 'manifest.json').read_text())
    lock = keyed_records(json.loads(source_lock.read_text())['inputs'], 'local_relative_path', 'source lock')
    expected_inputs = {'raw/bea_cainc4/CAINC4.csv'}
    for year in YEARS:
        expected_inputs.add(f'raw/irs_soi/county/{year % 100:02}incyallnoagi.csv')
        expected_inputs.add(f'codebooks/{year % 100:02}incydocguide' + ('.doc' if year <= 2016 else '.docx'))
    require(set(lock) == expected_inputs, 'source lock artifact set mismatch')
    inputs = keyed_records(manifest['inputs'], 'output_path', 'input manifest')
    by_relative = {}
    for name, entry in inputs.items():
        path = Path(name)
        require(path.is_absolute() and '..' not in path.parts, f'invalid input path: {name}')
        require(path.is_relative_to(out), f'input manifest path outside bundle: {name}')
        rel = path.relative_to(out).as_posix()
        require(rel not in by_relative, f'duplicate input: {rel}')
        by_relative[rel] = entry
    require(set(by_relative) == set(lock), 'input manifest artifact set mismatch')
    for rel, pinned in lock.items():
        entry = by_relative[rel]
        require(all(k in entry and entry[k] == pinned[k] for k in ('bytes', 'sha256', 'official_url')),
                f'input manifest differs from source lock: {rel}')
        check_hash(out / rel, pinned, rel)
    outputs = keyed_records(json.loads((out / 'output_hashes.json').read_text()), 'path', 'output hashes')
    actual = {p.relative_to(out).as_posix() for p in (out / 'derived').rglob('*') if p.is_file()}
    require(set(outputs) == OUTPUTS and actual == OUTPUTS, 'derived output artifact set mismatch')
    for rel, entry in outputs.items():
        check_hash(out / rel, entry, rel)
    return manifest, len(lock), len(outputs)


def reconstruct(out):
    """Build expected values from source records, without importing the generator."""
    bea = pd.read_csv(out / 'raw/bea_cainc4/CAINC4.csv', dtype=str, encoding='cp1252',
                      keep_default_na=False, skipinitialspace=True)
    bea['fips'] = bea.GeoFIPS.str.strip().str.strip('"')
    bea['LineCode'] = bea.LineCode.str.strip()
    bea = bea[bea.LineCode.isin(BEA)].copy()
    require(not bea.duplicated(['fips', 'LineCode']).any(), 'duplicate source BEA key')
    require(set(bea.LineCode) == set(BEA), 'source BEA measures incomplete')
    for code in BEA:
        expected_unit = 'number of persons' if code == '20' else 'thousands of dollars'
        require(bea.loc[bea.LineCode == code, 'Unit'].str.lower().eq(expected_unit).all(),
                f'BEA source unit mismatch: {code}')
    names = bea[['fips', 'GeoName']].drop_duplicates().set_index('fips')
    require(names.index.is_unique, 'conflicting source BEA names')
    expected = []
    for year in YEARS:
        wide = bea.pivot(index='fips', columns='LineCode', values=str(year))
        b = pd.DataFrame(index=wide.index)
        for code, col in BEA.items():
            b[col] = numeric(wide[code], f'BEA {year} {code}') * (1 if code == '20' else 1000)
        b = b.join(names).reset_index()
        b = b[county(b.fips)]
        r = pd.read_csv(out / f'raw/irs_soi/county/{year % 100:02}incyallnoagi.csv',
                        dtype=str, encoding='cp1252', keep_default_na=False)
        r.columns = r.columns.str.upper()
        require(numeric(r.AGI_STUB, f'IRS {year} AGI_STUB').eq(0).all(), 'IRS source is not no-AGI totals')
        r['fips'] = r.STATEFIPS.str.zfill(2) + r.COUNTYFIPS.str.zfill(3)
        require(not r.fips.duplicated().any(), f'duplicate source IRS FIPS: {year}')
        state_totals = r[r.fips.str[2:].eq('000')].fips.str[:2]
        require(set(state_totals) == STATES, f'IRS state total coverage mismatch: {year}')
        irs = r[['fips', 'COUNTYNAME']].copy()
        irs['irs_returns'] = numeric(r.N1, f'IRS {year} N1')
        for source, (col, count) in IRS.items():
            amount = numeric(r[source], f'IRS {year} {source}') * 1000
            returns = numeric(r[count], f'IRS {year} {count}')
            ambiguous = returns.eq(0) & amount.eq(0)
            irs[col] = amount.mask(ambiguous)
            irs[col + '_zero_ambiguous'] = ambiguous
        irs = irs[county(irs.fips)]
        joined = b.merge(irs, on='fips', how='outer', validate='one_to_one', indicator=True)
        joined['join_status'] = joined.pop('_merge').astype(str)
        joined['year'] = year
        expected.append(joined)
    return pd.concat(expected, ignore_index=True).set_index(['fips', 'year']).sort_index()


def verify(out, source_lock):
    out = out.absolute()
    manifest, n_inputs, n_outputs = verify_integrity(out, source_lock)
    actual = pd.read_csv(out / 'derived/county_year_outcomes.csv', dtype={'fips': str}, low_memory=False)
    require(not actual.duplicated(['fips', 'year']).any(), 'duplicate derived FIPS-year')
    require(set(actual.year) == set(YEARS), 'derived year coverage mismatch')
    require(county(actual.fips).all(), 'invalid or excluded derived county FIPS')
    actual = actual.set_index(['fips', 'year']).sort_index()
    expected = reconstruct(out)
    require(actual.index.equals(expected.index), 'derived county-year union differs from sources')
    require(set(actual.columns) == set(expected.columns), 'derived column set mismatch')
    checks, missingness_checks = 0, 0
    numeric_cols = [*BEA.values(), 'irs_returns', *[x[0] for x in IRS.values()]]
    for col in expected:
        a, e = actual[col], expected[col]
        require(a.isna().equals(e.isna()), f'missingness mismatch: {col}')
        missingness_checks += len(e)
        known = e.notna()
        if col in numeric_cols:
            delta = pd.to_numeric(a[known], errors='raise') - e[known]
            require(delta.abs().lt(.01).all(), f'direct source value mismatch: {col}')
        else:
            require(a[known].astype(str).eq(e[known].astype(str)).all(), f'direct source label/flag mismatch: {col}')
        checks += int(known.sum())
    metadata = manifest['analysis']
    require(metadata['years'] == YEARS and metadata['missing_years'] == [2012], 'manifest year coverage mismatch')
    require(metadata['panel_rows'] == len(actual), 'manifest panel row count mismatch')
    require(metadata['county_fips'] == actual.index.get_level_values('fips').nunique(), 'manifest county count mismatch')
    return {'status': 'PASS', 'source_lock_sha256': digest(source_lock), 'hash_checked_inputs': n_inputs,
            'hash_checked_outputs': n_outputs, 'direct_source_value_checks': checks,
            'source_missingness_checks': missingness_checks, 'county_year_rows': len(actual),
            'exact_source_county_year_union': True, 'all_exported_fields_checked': True,
            'no_duplicate_or_aggregate_fips': True, 'missing_2012_explicit': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--source-lock', type=Path, default=Path(__file__).with_name('SOURCES.json'))
    args = parser.parse_args()
    result = verify(args.out, args.source_lock)
    (args.out / 'verification.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
