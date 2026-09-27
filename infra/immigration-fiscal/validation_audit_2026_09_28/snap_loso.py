"""Retrospective state cross-validation of a common SNAP reporting-odds correction.

Frozen before scoring: use every previously validity-screened state; no residual-
based exclusions; fit a dollar-weighted common odds ratio on all other valid states.
Compare raw and corrected held-state Hispanic benefit-dollar shares. Point errors
only. These sources, the screen and estimand were already inspected; this is NOT
prospective validation and does not evaluate the adopted direct-admin BV key.
"""
from pathlib import Path
import ast
import hashlib
import json
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
LANE = ROOT / 'infra/immigration-fiscal/admin_benefit_keys_2026_09_24'
DEST = Path(__file__).resolve().parent / 'derived/snap_loso'
DEST.parent.mkdir(parents=True, exist_ok=True)
files = {k: LANE / v for k, v in {
    'replicates': '_cache/cps_state_replicates.npz',
    'validity': 'derived/admin_validity.csv',
    'qc': 'derived/admin_snap_qc.csv',
    'cps': 'derived/cps_keys_state.csv',
    'code': 'compare.py',
}.items()}
files['diagnostic'] = Path(__file__).resolve()


def sha(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


method = {
    'label': 'Retrospective leave-one-state-out point-error diagnostic',
    'training': 'All other previously validity-screened states, admin-dollar weighted shares on both sides',
    'equation': 'rho=odds(sum(A*h)/sum(A))/odds(sum(A*a)/sum(A)); prediction=h/(rho*(1-h)+h)',
    'gates': 'At least 20 valid states; positive administrative/CPS dollar totals; at least 10 raw Hispanic CPS records per valid state; pooled training and held-state shares strictly inside (0,1)',
    'scoring': 'Admin-dollar-weighted MAE, RMSE, bias in percentage points; every residual; raw vs corrected; no CI or headline correction',
    'support_summary': 'At least 30 raw Hispanic CPS records shown as a previously inspected descriptive subgroup only; all valid states remain scored',
    'nonindependence': 'Sources, estimand and outcome-based administrative screen already inspected. This is a new common-rho transport test, not the adopted BV direct substitution.',
    'units': 'States means state/DC jurisdictions. Shares of SNAP benefit dollars. QC allocates across benefit participants; CPS across SPM unit members. QC weights use its reported FYWGT*FSBEN sums, not asserted annual budget totals.',
    'sha256': {str(p.relative_to(ROOT)): sha(p) for p in files.values()},
}
DEST.with_suffix('.method.json').write_text(json.dumps(method, indent=2)+'\n')
tree = ast.parse(files['code'].read_text())
names = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == 'NAMES' for t in n.targets))
r = np.load(files['replicates'])
states = r['states'].astype(str)
v = pd.read_csv(files['validity']).query('programme == "snap"').set_index('state')
if set(v.index) != set(states):
    raise ValueError('State ordering/universe mismatch')
qc = pd.read_csv(files['qc'])
qc = qc[(qc.measure == 'dollars') & qc.geography.isin(names)].copy()
qc['state'] = qc.geography.map(names)
qc = qc.set_index('state').reindex(states)
c = pd.read_csv(files['cps']).query('programme == "snap" and measure == "key" and allocation == "both"').set_index('geography').reindex(states)
d = pd.DataFrame({
    'state': states,
    'valid_admin': ~v.reindex(states).invalid.to_numpy(bool),
    'qc_units': qc.units.to_numpy(),
    'qc_weighted_benefit_dollars': qc.total.to_numpy(),
    'qc_hisp_share': qc.hisp_share_imputed.to_numpy(),
    'qc_unknown_share': qc.unknown_share.to_numpy(),
    'cps_records': c.records.to_numpy(),
    'cps_hisp_records': c.hisp_records.to_numpy(),
    'cps_weighted_benefit_dollars': r['snap|key|both|total'][:, 0],
    'cps_hisp_weighted_benefit_dollars': r['snap|key|both|hisp'][:, 0],
})
d['raw_share'] = d.cps_hisp_weighted_benefit_dollars / d.cps_weighted_benefit_dollars
if not np.allclose(d.raw_share, c.hisp_share, atol=1e-12):
    raise ValueError('Stored point-share reconstruction mismatch')
d = d[d.valid_admin].copy().reset_index(drop=True)
if len(d) < 20 or d.cps_hisp_records.min() < 10:
    raise ValueError('Insufficient state support')
if not np.isfinite(d[['qc_weighted_benefit_dollars', 'cps_weighted_benefit_dollars',
                      'raw_share', 'qc_hisp_share']].to_numpy()).all():
    raise ValueError('Nonfinite totals/shares')
if not ((d.qc_weighted_benefit_dollars > 0) & (d.cps_weighted_benefit_dollars > 0)
        & d.raw_share.between(0, 1, inclusive='neither') & d.qc_hisp_share.between(0, 1, inclusive='neither')).all():
    raise ValueError('Invalid totals/shares')
odds = lambda x: x / (1-x)
for i in d.index:
    train = d.drop(i)
    A = train.qc_weighted_benefit_dollars
    H = np.average(train.raw_share, weights=A)
    B = np.average(train.qc_hisp_share, weights=A)
    rho = odds(H) / odds(B)
    h = d.loc[i, 'raw_share']
    d.loc[i, 'training_states'] = len(train)
    d.loc[i, 'training_rho'] = rho
    d.loc[i, 'corrected_share'] = h / (rho*(1-h)+h)
d['raw_error_pp'] = 100*(d.raw_share-d.qc_hisp_share)
d['corrected_error_pp'] = 100*(d.corrected_share-d.qc_hisp_share)
d['absolute_error_change_pp'] = d.corrected_error_pp.abs()-d.raw_error_pp.abs()
d['share_of_scored_qc_dollars'] = d.qc_weighted_benefit_dollars/d.qc_weighted_benefit_dollars.sum()

def metrics(part):
    out = {'states': len(part), 'qc_dollar_weight': float(part.qc_weighted_benefit_dollars.sum())}
    for key in ['raw', 'corrected']:
        e = part[f'{key}_error_pp'].to_numpy()
        w = part.qc_weighted_benefit_dollars.to_numpy()
        out[key] = {'mae_pp': float(np.average(np.abs(e), weights=w)),
                    'rmse_pp': float(np.sqrt(np.average(e*e, weights=w))),
                    'bias_pp': float(np.average(e, weights=w))}
    out['states_improved'] = int((part.absolute_error_change_pp < 0).sum())
    out['states_worse'] = int((part.absolute_error_change_pp > 0).sum())
    return out

# Provenance is the input sha256s in method; a git HEAD here would change the output on every commit.
out = {'method': method, 'all_valid_states': metrics(d),
       'at_least_30_raw_hispanic_records': metrics(d[d.cps_hisp_records >= 30]),
       'training_rho_min_max': [float(d.training_rho.min()), float(d.training_rho.max())],
       'improvement_claim': 'Descriptive prediction errors only; no statistical significance or fiscal correction.'}
d.to_csv(DEST.with_suffix('.csv'), index=False, lineterminator='\n')
DEST.with_suffix('.json').write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: v for k, v in out.items() if k != 'method'}, indent=2))
print(d[['state','cps_hisp_records','qc_hisp_share','raw_share','corrected_share','raw_error_pp','corrected_error_pp','absolute_error_change_pp']].to_string(index=False))
