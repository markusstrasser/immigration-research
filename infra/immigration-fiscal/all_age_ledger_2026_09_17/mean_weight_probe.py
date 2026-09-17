"""Test the external critique's mean-unit-weight attribution alternative.

Direct health and person-weighted populations are identical between assignment
arms, so health cancels from each paired contrast. No medical model rerun needed.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from analyze import COEFFICIENTS, COMPONENTS, FISCAL, HERE, REFERENCES, TARGETS, ext, matrices
from estimator import account, contrast, sufficient, sum_cells, summarize


def main():
    source = FISCAL / 'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    state = ext.build(argparse.Namespace(cps_zip=source))
    d, w, index = state['d'], state['person_weights'], state['index']
    shared, personal, _ = matrices(state)
    delta = personal - shared
    head = d.loc[d.SPM_HEAD.eq(1)].sort_values('SPM_ID')[ext.base.REPS].to_numpy()[index]
    counts = np.bincount(index, minlength=state['n_units'])
    if (counts <= 0).any():
        raise ValueError('Empty source unit')
    unit_mean = np.column_stack([np.bincount(index, weights=w[:, r], minlength=len(counts))/counts
                                 for r in range(161)])[index]
    # This alternative preserves the original person-weighted SHARED national
    # component totals, unlike a generic head-weight convention.
    mean_budget, original_budget = shared.T @ unit_mean, shared.T @ w
    national_residual = mean_budget - original_budget
    # Different floating-point summation paths over trillion-dollar totals can
    # differ by cents. Check tight relative precision as well as absolute cents.
    if not np.allclose(mean_budget, original_budget, rtol=1e-12, atol=.02):
        raise ValueError(f'Mean-unit shared-budget residual: {np.max(np.abs(national_residual)):.9f} dollars')
    civilian = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    groups = {g: state['group'][g] & civilian for g in TARGETS[:3] + REFERENCES[:2]}
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    zero_health = np.zeros((len(d), 1))
    rows, vectors, residuals = [], {}, {}
    for label, dollar_weights in [('head', head), ('unit_mean', unit_mean)]:
        residual = delta.T @ dollar_weights
        residuals[label] = dict(zip(COMPONENTS, np.max(np.abs(residual), axis=1).tolist()))
        if np.max(np.abs(residual)) > .02:
            raise ValueError(f'{label} reassignment changed a national component budget')
        stats = sufficient(delta, zero_health, dollar_weights, groups, bands,
                           population_weights=w, health_weights=w)
        stats[TARGETS[-1]] = sum_cells([stats[g] for g in TARGETS[:3]])
        for target in TARGETS:
            metrics = {'absolute_total': account(stats[target], COEFFICIENTS, [0]).sum(axis=0)}
            for reference in REFERENCES[:2]:
                metrics[f'{reference}|age_band'] = contrast(stats[target], stats[reference], COEFFICIENTS, [0])[0]
            for metric, vector in metrics.items():
                vectors[label, target, metric] = vector
                rows.append(dict(weighting=label, target=target, contrast=metric,
                                 **summarize(vector, [0], np.zeros((1, 1)))))
    old_path = HERE / 'derived/fixed_budget_attribution.csv'
    old = pd.read_csv(old_path)
    for row in rows:
        if row['weighting'] != 'head':
            continue
        anchor = old[old.target.eq(row['target']) & old.contrast.eq(row['contrast'])]
        if len(anchor) != 1 or max(abs(row[k]-anchor[k].iloc[0]) for k in ['estimate', 'se_joint']) > .02:
            raise ValueError('Independent paired head-dollar reconstruction failed its stored anchor')
    for target in TARGETS:
        for metric in ['absolute_total'] + [f'{r}|age_band' for r in REFERENCES[:2]]:
            vector = vectors['unit_mean', target, metric] - vectors['head', target, metric]
            rows.append(dict(weighting='unit_mean_minus_head', target=target, contrast=metric,
                             **summarize(vector, [0], np.zeros((1, 1)))))
    out = HERE / 'derived/mean_weight'
    out.mkdir(exist_ok=True)
    table = pd.DataFrame(rows)
    table.to_csv(out/'paired_changes.csv', index=False)
    np.savez_compressed(out/'replicates.npz', **{'|'.join(k): v for k, v in vectors.items()})
    inputs = [source, Path(__file__), HERE/'analyze.py', HERE/'estimator.py',
              Path(ext.__file__), Path(ext.base.__file__), ext.HERE/'state_parameters.csv', old_path]
    audit = dict(inputs=[dict(path=str(p), sha256=ext.base.sha(p)) for p in inputs],
                 mean_matches_original_shared_max_residual=float(np.max(np.abs(national_residual))),
                 shared_budget_rtol=1e-12, shared_budget_atol=.02,
                 shared_budget_max_relative_residual=float(np.max(np.abs(national_residual)/np.maximum(np.abs(original_budget), 1))),
                 attribution_component_max_residual=residuals, stored_head_anchors_passed=12,
                 population_and_direct_health_unchanged=True, rows=len(table))
    (out/'audit.json').write_text(json.dumps(audit, indent=2)+'\n')
    print(table[table.target.eq(TARGETS[-1])].to_string(index=False))
    print('PASS: 161-vector component budgets, original shared-budget equivalence, 12 head anchors')


if __name__ == '__main__':
    main()
