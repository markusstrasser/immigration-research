"""Unknown CPS/MEPS correlation sensitivity, conditional on held marginal SEs.

This is NOT a bound on omitted uncertainty in estimated calibration controls,
model transport, coverage error or a full survey-design confidence interval.
"""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def main():
    out = HERE/'derived/donor_dependence'
    out.mkdir(exist_ok=True)
    inputs = []
    for name in ['estimates', 'generation_contrasts']:
        source = HERE/f'derived/{name}.csv'
        d = pd.read_csv(source)
        values = d[['estimate', 'se_cps', 'se_meps']]
        if not np.isfinite(values).all().all() or (d[['se_cps', 'se_meps']] < 0).any().any():
            raise ValueError('Invalid supplied estimates or marginal standard errors')
        d['se_max_correlation'] = d.se_cps + d.se_meps
        d['se_min_correlation'] = (d.se_cps - d.se_meps).abs()
        d['normal95_maxcorr_low'] = d.estimate - 1.96*d.se_max_correlation
        d['normal95_maxcorr_high'] = d.estimate + 1.96*d.se_max_correlation
        d.to_csv(out/f'{name}.csv', index=False)
        inputs.append(dict(path=str(source), sha256=hashlib.sha256(source.read_bytes()).hexdigest(), rows=len(d)))
        if name == 'estimates':
            show = d[d.scenario.eq('all_age_shared') & d.target.eq('mexican_observed_total')
                     & (d.metric.eq('absolute_total') | (d.metric.eq('gap_total') & d.matching.eq('age_band')
                     & d.reference.isin(['third_plus_nh_white', 'all_native'])))]
            keys = ['metric', 'reference']
        else:
            show = d[d.scenario.isin(['all_age_shared', 'personal_sources']) & d.earlier.eq('mexico_born')
                     & d.later.eq('mexican_third_plus_selfid')]
            keys = ['scenario', 'later', 'earlier']
        print(show[keys+['estimate', 'se_max_correlation', 'normal95_maxcorr_low', 'normal95_maxcorr_high']].to_string(index=False))
    metadata = dict(inputs=inputs, script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                    construction='sqrt(Vc+Vm+2*rho*SEc*SEm), with rho=+1 for maximal variance',
                    scope='Conditional on supplied marginal SEs and first-order approximation; no additional calibration-control, coverage, transport or parameter uncertainty included',
                    trigger='HC-256 documents MEPS2024 calibration to March2025 CPS estimates; cross-source covariance is not established to be zero')
    (out/'audit.json').write_text(json.dumps(metadata, indent=2)+'\n')


if __name__ == '__main__':
    main()
