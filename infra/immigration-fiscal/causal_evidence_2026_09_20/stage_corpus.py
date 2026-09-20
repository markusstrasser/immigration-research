#!/usr/bin/env python3
"""Stage a small, validated outcome panel. This does not estimate causal effects."""
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import urllib.request
import zipfile
from pathlib import Path

import pandas as pd

YEARS = [2011, *range(2013, 2023)]
STATES = {f'{x:02}' for x in [1,2,4,5,6,8,9,10,11,12,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,44,45,46,47,48,49,50,51,53,54,55,56]}
IRS = {'A00100': ('irs_agi_dollars', 'N1'), 'A00200': ('irs_wages_dollars', 'N00200'), 'A06500': ('irs_income_tax_A06500_dollars', 'N06500')}
BEA = {'20': 'bea_population', '35': 'bea_workplace_earnings_dollars', '36': 'bea_social_insurance_contributions_dollars', '42': 'bea_residence_adjustment_dollars', '45': 'bea_residence_net_earnings_dollars', '47': 'bea_transfer_receipts_dollars', '50': 'bea_wages_dollars'}
MISSING = {'', '(D)', '(L)', '(NA)', '(NM)', 'N/A', 'NA', '*', '**', '-', '--'}
LIMIT = 10_000_000_000


def require(test, message):
    if not test:
        raise ValueError(message)


def sha(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def read_csv(path):
    require(path.is_file() and path.stat().st_size > 100, f'missing/empty CSV: {path}')
    require(not path.open('rb').read(500).lstrip().lower().startswith((b'<html', b'<!doctype')), f'HTML masquerades as data: {path}')
    # BEA's downloaded county names contain Windows-1252 (e.g. Dona Ana n-tilde).
    # IRS selected payloads use the same legacy text encoding; ASCII is a subset.
    return pd.read_csv(path, dtype=str, keep_default_na=False, skipinitialspace=True, encoding='cp1252')


def county_mask(fips):
    # BEA 900-series Virginia combined areas are not individual county FIPS.
    return fips.str.fullmatch(r'\d{5}') & fips.str[:2].isin(STATES) & (fips.str[2:] != '000') & (fips.str[2:] < '900')


def number(series, label, audit, allow_negative=False):
    text = series.str.strip()
    values = pd.to_numeric(text, errors='coerce')
    bad = text[values.isna() & ~text.isin(MISSING)]
    require(bad.empty, f'unknown numeric tokens in {label}: {bad.unique()[:8]}')
    if not allow_negative:
        require(not (values < 0).any(), f'negative value in nonnegative measure {label}')
    audit[label] = {'rows': len(text), 'missing_tokens': text[values.isna()].value_counts().to_dict(), 'negative_values_retained': int((values < 0).sum())}
    return values


def copy_checked(source, target, official, records, source_kind='corpus'):
    target.parent.mkdir(parents=True, exist_ok=True)
    source_hash = sha(source)
    if target.exists():
        require(sha(target) == source_hash, f'refusing to overwrite different bytes: {target}')
    else:
        shutil.copyfile(source, target)
    require(sha(target) == source_hash, f'copy mismatch: {target}')
    records.append({'source_path': str(source.resolve()), 'output_path': str(target), 'bytes': target.stat().st_size, 'sha256': source_hash, 'official_url': official, 'source_kind': source_kind})


def codebook(year, corpus, out, seed, fetch, records):
    stem = f'{year%100:02}incydocguide'
    ext = '.doc' if year <= 2016 else '.docx'
    name = stem + ext
    url = f'https://www.irs.gov/pub/irs-soi/{name}'
    target = out / 'codebooks' / name
    target.parent.mkdir(parents=True, exist_ok=True)
    if (seed / name).exists():
        copy_checked(seed / name, target, url, records, 'official_codebook_seed')
    elif year != 2011:
        archive = corpus / 'irs_soi' / 'county' / f'county{year}.zip'
        require(zipfile.is_zipfile(archive), f'Invalid codebook archive: {archive}')
        with zipfile.ZipFile(archive) as z:
            require(name in z.namelist(), f'Codebook absent in {archive}')
            require(z.getinfo(name).file_size < 2_000_000, 'unexpected codebook size')
            data = z.read(name)
        if target.exists():
            require(target.read_bytes() == data, f'different existing codebook {target}')
        else:
            target.write_bytes(data)
        records.append({'source_path': f'{archive}!{name}', 'output_path': str(target), 'bytes': len(data), 'sha256': sha(target), 'archive_sha256': sha(archive), 'official_url': url, 'source_kind': 'corpus_archive_member'})
    else:
        require(fetch, f'2011 codebook missing; supply --codebooks-root or --fetch-codebooks: {url}')
        with urllib.request.urlopen(url, timeout=45) as response:
            data = response.read(2_000_001)
        require(len(data) <= 2_000_000, 'codebook exceeds retrieval cap')
        target.write_bytes(data)
        records.append({'source_path': url, 'output_path': str(target), 'bytes': len(data), 'sha256': sha(target), 'official_url': url, 'source_kind': 'official_download'})
    text = subprocess.run(['textutil', '-convert', 'txt', '-stdout', str(target)], check=True, capture_output=True, text=True).stdout
    require('thousands of dollars' in text.lower(), f'unverified units in {name}')
    label = re.search(r'A06500\s+(Income tax(?: after credits)? amount)', text, re.I)
    require(label, f'unverified tax field in {name}')
    require('A00100' in text and 'A00200' in text, f'missing income definitions in {name}')
    (target.with_suffix('.txt')).write_text(text)
    return {'year': year, 'file': name, 'official_url': url, 'money_units': 'thousands of nominal dollars', 'A06500': label.group(1), 'verified_from_actual_codebook': True}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--corpus-root', required=True, type=Path)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--codebooks-root', type=Path, default=Path(__file__).parent / 'codebooks')
    parser.add_argument('--fetch-codebooks', action='store_true')
    parser.add_argument('--max-bytes', type=int, default=LIMIT)
    args = parser.parse_args()
    require(0 < args.max_bytes <= LIMIT, 'max-bytes must be <=10GB')
    corpus, out = args.corpus_root.resolve(), args.out.resolve()
    require(not out.is_relative_to(corpus) and out != corpus, 'output must not be inside read-only corpus')
    selected = [corpus/'bea_cainc4/CAINC4.csv', *[corpus/f'irs_soi/county/{y%100:02}incyallnoagi.csv' for y in YEARS]]
    require(all(p.is_file() for p in selected), 'required corpus file missing')
    require(sum(p.stat().st_size for p in selected) + 30_000_000 <= args.max_bytes, 'selected raw plus reserved derived bytes exceed cap')
    require(not out.exists() or sum(p.stat().st_size for p in out.rglob('*') if p.is_file()) <= args.max_bytes, 'existing output already exceeds cap')
    out.mkdir(parents=True, exist_ok=True)
    records, audits = [], {}
    # Validate every CSV and codebook before copying corpus payloads.
    bea = read_csv(selected[0])
    require({'GeoFIPS','LineCode','Unit',*[str(y) for y in YEARS]} <= set(bea), 'BEA schema mismatch')
    irs_sources = {}
    for y,p in zip(YEARS,selected[1:]):
        df = read_csv(p)
        df.columns = df.columns.str.upper()
        require({'STATEFIPS','COUNTYFIPS','COUNTYNAME','AGI_STUB','N1',*IRS,*[x[1] for x in IRS.values()]} <= set(df), f'IRS {y} schema mismatch')
        require((pd.to_numeric(df.AGI_STUB) == 0).all(), f'non-total AGI classes in {y}')
        irs_sources[y] = df
    book_checks = [codebook(y, corpus, out, args.codebooks_root, args.fetch_codebooks, records) for y in YEARS]
    bea['fips'] = bea.GeoFIPS.str.strip().str.strip('"')
    bea['LineCode'] = bea.LineCode.str.strip()
    bea = bea[bea.LineCode.isin(BEA)].copy()
    require(not bea.duplicated(['fips','LineCode']).any(), 'duplicate BEA geography/line')
    for line in BEA:
        unit = 'Number of persons' if line == '20' else 'Thousands of dollars'
        require((bea.loc[bea.LineCode==line,'Unit'].str.lower() == unit.lower()).all(), f'BEA units mismatch line {line}')
    long = bea.melt(id_vars=['fips','GeoName','LineCode'], value_vars=[str(y) for y in YEARS], var_name='year', value_name='value')
    long['year'] = long.year.astype(int)
    long['measure'] = long.LineCode.map(BEA)
    parts = []
    for line, name in BEA.items():
        d = long[long.LineCode == line].copy()
        d['value'] = number(d.value, name, audits, allow_negative=line in {'35','42','45'}) * (1 if line == '20' else 1000)
        parts.append(d)
    long = pd.concat(parts, ignore_index=True)
    bw = long.pivot(index=['fips','year'], columns='measure', values='value').reset_index()
    names = bea[['fips','GeoName']].drop_duplicates()
    bw = bw.merge(names, on='fips', validate='many_to_one')
    bea_counties = bw[county_mask(bw.fips)].copy()
    bea_national = bw[bw.fips == '00000'].copy()
    excluded_bea = bw[bw.fips.str[:2].isin(STATES) & (bw.fips.str[2:] >= '900')]
    frames, states, suppressed = [], [], []
    for year, df in irs_sources.items():
        df['fips'] = df.STATEFIPS.str.zfill(2) + df.COUNTYFIPS.str.zfill(3)
        require(not df.duplicated('fips').any(), f'duplicate IRS county {year}')
        result = df[['fips','COUNTYNAME']].copy()
        result['year'] = year
        result['irs_returns'] = number(df.N1, f'IRS{year}_N1', audits)
        for column,(name,count) in IRS.items():
            raw = number(df[column], f'IRS{year}_{column}', audits, allow_negative=column == 'A00100') * 1000
            n = number(df[count], f'IRS{year}_{count}', audits)
            # IRS can exclude small/dominant cells; zero is not known true zero.
            ambiguous = (n == 0) & (raw == 0)
            result[name] = raw.mask(ambiguous)
            result[name+'_zero_ambiguous'] = ambiguous
            for fips in result.loc[ambiguous,'fips']:
                suppressed.append({'fips': fips, 'year': year, 'measure':name,'reason':'reported zero amount and zero returns; true zero versus disclosure exclusion unresolved'})
        states.append(result[result.fips.str[:2].isin(STATES) & (result.fips.str[2:] == '000')])
        frames.append(result[county_mask(result.fips)])
    ic = pd.concat(frames, ignore_index=True)
    ist = pd.concat(states, ignore_index=True)
    require(not ic.duplicated(['fips','year']).any(), 'IRS county-year not unique')
    panel = bea_counties.merge(ic, on=['fips','year'], how='outer', validate='one_to_one', indicator=True)
    panel = panel.rename(columns={'_merge':'join_status'}).sort_values(['year','fips'])
    require(len(panel) > 30000, 'unexpectedly small panel')
    require(set(panel.year) == set(YEARS) and 2012 not in set(panel.year), 'year coverage changed')
    diagnostics, coverage = [], []
    for y,g in panel.groupby('year'):
        counts = g.join_status.value_counts().to_dict()
        complete = g[['bea_population','bea_wages_dollars','bea_transfer_receipts_dollars',*[v[0] for v in IRS.values()]]].notna().all(axis=1)
        coverage.append({'year': y, 'matched': counts.get('both',0), 'matched_with_population':int(((g.join_status=='both') & g.bea_population.notna()).sum()), 'matched_complete_main_outcomes':int(((g.join_status=='both') & complete).sum()), 'bea_only':counts.get('left_only',0),'irs_only':counts.get('right_only',0)})
        for var in BEA.values():
            published = bea_national.loc[bea_national.year == y,var].iloc[0]
            total = g[var].sum(min_count=1)
            matched = g.loc[g.join_status=='both',var].sum(min_count=1)
            diagnostics.append({'year':y,'measure':var,'county_sum':total,'matched_county_sum':matched,'reference_sum':published,'reference':'BEA national published','county_reference_ratio':total/published if published else None})
        for var in [* [v[0] for v in IRS.values()], 'irs_returns']:
            total = g[var].sum(min_count=1)
            ref = ist.loc[ist.year==y,var].sum(min_count=1)
            diagnostics.append({'year':y,'measure':var,'county_sum':total,'matched_county_sum':g.loc[g.join_status=='both',var].sum(min_count=1),'reference_sum':ref,'reference':'IRS 50-state plus DC totals in same county file; not all federal receipts','county_reference_ratio':total/ref if ref else None})
    # All schema, units, numeric tokens, uniqueness and join checks have now run.
    for p in selected:
        rel = p.relative_to(corpus)
        url = 'https://apps.bea.gov/regional/zip/CAINC4.zip' if 'bea_cainc4' in str(rel) else f'https://www.irs.gov/pub/irs-soi/{p.name}'
        copy_checked(p, out/'raw'/rel, url, records)
    derived = out/'derived'
    derived.mkdir(exist_ok=True)
    panel.to_csv(derived/'county_year_outcomes.csv', index=False)
    pd.DataFrame(coverage).to_csv(derived/'join_coverage.csv', index=False)
    pd.DataFrame(diagnostics).to_csv(derived/'national_sum_diagnostics.csv', index=False)
    excluded_bea.to_csv(derived/'bea_combined_geographies_excluded.csv', index=False)
    pd.DataFrame(suppressed).to_csv(derived/'ambiguous_zero_cells.csv', index=False)
    panel.loc[panel.join_status!='both',['fips','year','GeoName','COUNTYNAME','join_status']].to_csv(derived/'unmatched_geographies.csv',index=False)
    metadata = {'status':'DESCRIPTIVE_OUTCOMES_ONLY','years':YEARS,'missing_years':[2012],'source_bytes':sum(p.stat().st_size for p in selected),'cap_bytes':args.max_bytes,'panel_rows':len(panel),'county_fips':panel.fips.nunique(),'coverage':coverage,'codebook_checks':book_checks,'numeric_audit':audits,'nominal_dollars':True,'limitations':['No policy treatment, ethnicity, nativity, or legal status columns; not causal.','BEA 900-series combined Virginia geographies excluded; unmatched IRS county/cities retained. No guessed crosswalk.','County boundaries differ over time; exact FIPS join does not harmonize historical geography.','IRS income tax after credits excludes refunds and is not net federal revenue.','IRS ZIP-derived geography and filing-year windows differ from BEA economic residence/year concepts.','2012 absent, never interpolated.','Zero amount plus zero returns is marked ambiguous and left missing; disclosure removal can affect positive cells too.']}
    (out/'manifest.json').write_text(json.dumps({'inputs':records,'analysis':metadata},indent=2))
    outputs = [{'path':str(p.relative_to(out)),'bytes':p.stat().st_size,'sha256':sha(p)} for p in derived.glob('*.csv')]
    (out/'output_hashes.json').write_text(json.dumps(outputs,indent=2))
    size = sum(p.stat().st_size for p in out.rglob('*') if p.is_file())
    require(size <= args.max_bytes, f'output exceeded cap: {size}')
    print(json.dumps({'status':'PASS','source_bytes':metadata['source_bytes'],'output_bytes':size,'panel_rows':len(panel),'coverage':coverage},indent=2))


if __name__ == '__main__':
    main()
