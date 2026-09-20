"""Regression probes for confirmed verifier and placebo-donor defects."""
import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent


def require(value, message):
    if not value:
        raise ValueError(message)


base = json.loads((ROOT / 'derived/chalfin/chalfin_replay.json').read_text())
variants = {'valid': base}
variants['wrong_ar_kind'] = copy.deepcopy(base)
variants['wrong_wald'] = copy.deepcopy(base)
variants['duplicate_outcome'] = copy.deepcopy(base)
variants['wrong_ar_kind']['baseline'][0]['ar95']['kind'] = 'empty'
variants['wrong_wald']['baseline'][0]['ci95'] = [1000, 2000]
variants['duplicate_outcome']['baseline'][0] = variants['duplicate_outcome']['baseline'][1]
with tempfile.TemporaryDirectory() as scratch:
    for name, value in variants.items():
        fixture = Path(scratch) / f'{name}.json'
        fixture.write_text(json.dumps(value))
        result = subprocess.run([sys.executable, '-O', str(ROOT / 'verify_chalfin.py'), '--results', str(fixture)], capture_output=True, text=True)
        require((result.returncode == 0) == (name == 'valid'), f'Unexpected verifier result: {name}: {result.stderr}')

models = placebos = 0
for spec in ['source-year', 'published-pool', 'june-only']:
    work = ROOT / 'mariel/work'
    panel = pd.read_csv(work / f'scm-{spec}-panel.csv', dtype={'ID': str})
    for result_file in (work / f'results-{spec}').glob('Total_*.json'):
        result = json.loads(result_file.read_text())
        models += 1
        outcome = result_file.stem
        matrix = np.log(panel.pivot(index='fiscal_year', columns='ID', values=outcome).where(lambda x: x > 0))
        for target, fit in [('105013001', result['actual'])] + list(result['placebos'].items()):
            weights = fit['weights']
            require(target not in weights, 'Target included in its own donors')
            if target != '105013001':
                placebos += 1
                require('105013001' not in weights, 'Treated Dade contaminates placebo counterfactual')
            require(abs(sum(weights.values()) - 1) < 1e-5, 'Weights fail simplex')
            years = [int(y) for y in fit['gaps_by_year']]
            expected = matrix.loc[years, target].to_numpy() - matrix.loc[years, list(weights)].to_numpy() @ np.array(list(weights.values()))
            require(np.allclose(expected, list(fit['gaps_by_year'].values()), atol=2e-5, rtol=0), 'Saved SCM path inconsistent with data and weights')
        actual = result['actual']['standardized_mean_gap']
        ranks = [fit['standardized_mean_gap'] for fit in result['placebos'].values()]
        expected_p = (1 + sum(abs(z) >= abs(actual) for z in ranks)) / (len(ranks) + 1)
        require(np.isclose(expected_p, result['p_two_sided_standardized_mean']), 'Placebo rank mismatch')
require(models == 21 and placebos > 0, f'Incomplete validation: {models} models, {placebos} placebos')
print(f'PASS: valid baseline plus 3 corruption regressions under -O; {models} SCM paths/ranks and {placebos} uncontaminated placebo paths')
