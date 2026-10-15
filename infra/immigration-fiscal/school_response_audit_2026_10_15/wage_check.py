"""One omitted-input-price check of the school proportionality evidence."""
import argparse
import hashlib
import io
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import t


def read_wages(data):
    # The official 2019 member contains Latin-1 district names (e.g. byte f1).
    frame = pd.read_csv(io.BytesIO(data), sep='\t', dtype={'LEAID': str}, encoding='latin-1')
    expected = ['LEAID', 'LEA_NAME', 'ST_NAME', 'LEA_CWIFTEST', 'LEA_CWIFTSE']
    if list(frame.columns) != expected or frame.LEAID.duplicated().any():
        raise ValueError('[BLOCKED] unexpected CWIFT schema or duplicate district')
    if not frame.LEA_CWIFTEST.gt(0).all():
        raise ValueError('[BLOCKED] nonpositive or missing CWIFT')
    return frame


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-root', type=Path, required=True)
    parser.add_argument('--out-dir', type=Path, required=True)
    args = parser.parse_args()
    raw = args.data_root / 'infra/immigration-fiscal/school_dilution_2026_09_24/_cache/f33/elsec19.txt'
    folder = args.data_root / 'sources/immigration-fiscal/data/external/stage3/nces/cwift_2019'
    archive = folder / 'EDGE_ACS_CWIFT2019.zip'
    member = 'EDGE_ACS_CWIFT2019/EDGE_ACS_CWIFT2019_LEA1920.txt'
    pins = {raw: '0d3fe071e52fa01d40b5dddaabfe0e07c997a593b740d9c35b3c240a137ddb09',
            archive: '6876d520b9f1c97917391addccdc8f7b4ce80e2b066b08ad0f08bc6650ef13db',
            folder / 'EDGE_ACS_CWIFT_FILEDOC.pdf': 'b7afaf98a7c63fbc0d22063e57783a8f9f65fa8b669fbdc565aeff86eb1681e2'}
    for path, expected in pins.items():
        if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
            raise ValueError(f'[BLOCKED] changed source: {path.name}')
    d = pd.read_csv(raw, dtype=str, index_col=False)
    d['NCESID'] = d.NCESID.str.strip()
    for name in ['V33', 'TCURELSC', 'TCURINST']:
        d[name] = pd.to_numeric(d[name], errors='coerce')
    d = d[d.NCESID.str.fullmatch(r'\d{7}', na=False) & d.SCHLEV.isin(['01', '02', '03'])
          & d.V33.ge(100) & d.TCURELSC.gt(0) & d.TCURINST.gt(0)].copy()
    d['state'] = d.NCESID.str[:2]
    d = d[d.state.ne('11')]
    assert not d.NCESID.duplicated().any(), 'Duplicate raw district IDs'
    with zipfile.ZipFile(archive) as z:
        wages = read_wages(z.read(member))
    assert not wages.LEAID.duplicated().any(), 'Duplicate CWIFT district IDs'
    matched = d.merge(wages, left_on='NCESID', right_on='LEAID', how='left', validate='one_to_one')
    missing = matched.LEA_CWIFTEST.isna()
    receipt = {'source_hashes': {str(p.relative_to(args.data_root)): hashlib.sha256(p.read_bytes()).hexdigest()
                                for p in [raw, archive, folder / 'EDGE_ACS_CWIFT_FILEDOC.pdf']},
               'member': member, 'raw_sample_districts': len(d), 'raw_sample_pupils': float(d.V33.sum()),
               'unmatched_districts': int(missing.sum()), 'unmatched_pupils': float(matched.loc[missing, 'V33'].sum()),
               'unmatched_ids': sorted(matched.loc[missing, 'NCESID'].tolist()),
               'note': 'FY2019 finances joined to 2019 wage index with 2019-20 LEA identifiers. No imputation; conditional index SE not propagated.'}
    matched = matched[~missing].copy()
    assert matched.LEA_CWIFTEST.gt(0).all(), 'Nonpositive wage index'
    assert matched.V33.sum() / d.V33.sum() > .98, 'Less than 98% pupil coverage'
    rows = []
    for name, frame in [('all_raw', d), ('cwift_matched', matched)]:
        for outcome in ['TCURELSC', 'TCURINST']:
            for weighted in [False, True]:
                for adjusted in ([False, True] if name == 'cwift_matched' else [False]):
                    predictors = pd.DataFrame({'log_pupils': np.log(frame.V33)}, index=frame.index)
                    if adjusted:
                        predictors['log_wages'] = np.log(frame.LEA_CWIFTEST)
                    states = pd.get_dummies(frame.state, prefix='state', drop_first=True, dtype=float)
                    x = sm.add_constant(pd.concat([predictors, states], axis=1))
                    weights = frame.V33 if weighted else np.ones(len(frame))
                    fit = sm.WLS(np.log(frame[outcome]), x, weights=weights).fit(
                        cov_type='cluster', cov_kwds={'groups': frame.state, 'use_correction': True}, use_t=True)
                    beta, se = float(fit.params['log_pupils']), float(fit.bse['log_pupils'])
                    critical = t.ppf(.975, frame.state.nunique()-1)
                    rows.append({'sample': name, 'outcome': outcome, 'weight': 'pupil' if weighted else 'equal',
                                 'wage_control': adjusted, 'districts': len(frame), 'states': frame.state.nunique(),
                                 'pupils': float(frame.V33.sum()), 'beta': beta, 'se': se,
                                 'ci_low': beta-critical*se, 'ci_high': beta+critical*se,
                                 'wage_coefficient': float(fit.params['log_wages']) if adjusted else None})
    assert all(np.isfinite(r['beta']) and np.isfinite(r['se']) for r in rows)
    args.out_dir.mkdir(parents=True, exist_ok=True)
    pd.DataFrame(rows).to_csv(args.out_dir / 'wage_estimates.csv', index=False, lineterminator='\n')
    (args.out_dir / 'wage_receipt.json').write_text(json.dumps(receipt, indent=2, sort_keys=True)+'\n')
    print(pd.DataFrame(rows).to_string(index=False))


if __name__ == '__main__':
    main()
