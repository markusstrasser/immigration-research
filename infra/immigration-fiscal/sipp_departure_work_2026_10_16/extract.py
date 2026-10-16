"""Extract pinned 2025 SIPP inputs; raw files are never modified."""
from pathlib import Path
import hashlib
import json
import zipfile

import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
RAW = ROOT / 'sources/immigration-fiscal/data/external/stage3/census/sipp_2025/pu2025_csv.zip'
SCHEMA = ROOT / '.scratch/clarity-next-20260905/admission/pu2025_schema.json'
EXPECTED = '570798a6f512c8f82af311ee01a1668d178063c9076c18a05bc3a5a0039b67ed'
SCHEMA_HASH = '6cdc23c537ba1431540e62994f0c05e05e62920e785384872bf5b7c23fe8c241'
CACHE = HERE / '_cache'
DERIVED = HERE / 'derived'


def sha(path):
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    assert sha(RAW) == EXPECTED, '[BLOCKED] source archive changed'
    assert sha(SCHEMA) == SCHEMA_HASH, '[BLOCKED] source schema changed'
    schema = json.loads(SCHEMA.read_text())
    names = {x['name'] for x in schema}
    base = '''SSUID PNUM SPANEL SWAVE MONTHCODE ERESIDENCEID ARESIDENCEID
        ERH_BMONTH ERH_EMONTH ARH_BMONTH ARH_EMONTH THHLDSTATUS RIN_UNIV
        TAGE_EHC ESEX EHISPAN EBORNUS RMESR AMESR TMWKHRS AMWKHRS
        TPEARN APEARN TPEARN_ALT APEARN_ALT WPFINWGT RHNUMPER RHNUMPERWT2 EEHC_WHY AEHC_WHY
        EMS_EHC AMS_EHC EPNSPOUS_EHC EPNCOHAB_EHC APNSPOUS_EHC APNCOHAB_EHC
        TMOVER ENJ_UPDWKYN ENJ_NOWRK11'''.split()
    base += [f'{prefix}{i}' for prefix in ['ET2_LNO', 'TT2_AGE', 'AT2_AGE', 'ET2_WORK']
             for i in range(1, 11)]
    # Include every published job-month/spell field needed to audit structural zeros.
    base += [x['name'] for x in schema if x['name'].startswith(('EJB', 'RJB', 'TJB'))
             and any(s in x['name'] for s in ('_JOBID', '_STARTWK', '_ENDWK', '_MWKHRS', '_MSUM', '_BMONTH', '_EMONTH'))]
    base += [x['name'] for x in schema if x['name'].startswith(('RREL', 'AREL'))]
    # Type-2 relationship names vary by release; take the authoritative schema subset.
    base += [x['name'] for x in schema if x['name'].startswith(('ET2_', 'AT2_'))
             and ('REL' in x['name'] or 'MONTH' in x['name'])]
    base = list(dict.fromkeys(base))
    assert set(base) <= names, f'[BLOCKED] missing schema fields {set(base)-names}'
    with zipfile.ZipFile(RAW) as z:
        assert z.namelist() == ['pu2025.csv']
        with z.open('pu2025.csv') as f:
            d = pd.read_csv(f, sep='|', usecols=base, dtype=str)
    for col in set(base) - {'SSUID', 'PNUM', 'ERESIDENCEID'}:
        d[col] = pd.to_numeric(d[col], errors='raise')
    assert not d.duplicated(['SSUID', 'PNUM', 'MONTHCODE']).any()
    assert d.groupby('SSUID').SPANEL.nunique().eq(1).all()
    d = d.sort_values(['SSUID', 'PNUM', 'MONTHCODE']).reset_index(drop=True)
    d.to_parquet(CACHE / 'persons.parquet', index=False)
    receipt = {'raw_sha256': EXPECTED, 'schema_sha256': SCHEMA_HASH,
               'script_sha256': sha(Path(__file__)), 'rows': len(d),
               'persons': len(d[['SSUID', 'PNUM']].drop_duplicates()),
               'columns': list(d.columns), 'parquet_sha256': sha(CACHE / 'persons.parquet')}
    (CACHE / 'extract_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    (DERIVED / 'input_receipt.json').write_text(json.dumps(receipt, indent=2)+'\n')
    (DERIVED / 'schema.json').write_text(json.dumps([x for x in schema if x['name'] in base], indent=2)+'\n')
    diagnostics = {c: d[c].value_counts(dropna=False).sort_index().to_dict()
                   for c in ['THHLDSTATUS', 'RIN_UNIV', 'ARESIDENCEID']}
    print(json.dumps({'rows': len(d), 'columns': len(d.columns), 'diagnostics': diagnostics}, default=str))


if __name__ == '__main__':
    main()
