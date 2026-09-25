"""Reproduce the audit's distribution diagnostics without rewriting upstream outputs.

The gross-wage-dispersion variants are identification counterexamples, not fitted
economic scenarios or uncertainty bounds. Existing-nest variants use the lane's
own allocation convention for changed induced receipts.
"""
import hashlib
import itertools
import json
import subprocess
import sys
import types
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SNAPSHOT = 'beefbba'
REL = 'infra/immigration-fiscal/winners_losers_2026_09_24/winners_losers.py'
src = subprocess.check_output(['git', '-C', str(ROOT), 'show', f'{SNAPSHOT}:{REL}'])
# The probe imports frozen code but reads current economic inputs. Refuse changes
# to tracked fiscal inputs since the snapshot; figure/UI changes are independent.
for revs in ((SNAPSHOT,),):
    changed = subprocess.check_output(
        ['git', '-C', str(ROOT), 'diff', '--name-only', *revs,
         '--', 'infra/immigration-fiscal']).decode().splitlines()
    allowed = ('infra/immigration-fiscal/conceptual_audit_2026_09_25/',
               'infra/immigration-fiscal/figures_2026_09_22/')
    changed = [p for p in changed if not p.startswith(allowed)]
    if changed:
        raise SystemExit('[BLOCKED] economic inputs changed since audited snapshot: ' + ', '.join(changed))
W = types.ModuleType('audit_winners')
W.__file__ = str(ROOT / REL)
sys.modules[W.__name__] = W
exec(compile(src, W.__file__, 'exec'), W.__dict__)
B, _ = W.load_base()
d, _ = W.load_frame(B)
I = W.base_inputs(B, d)
fin = W.fiscal_inputs()
W.fiscal_one_definition(B, fin)
fedsplit, _ = W.federal_split(fin)
deficit = W.deficit_share_fy2024()
ch, totals, meta, ctx = W.build_frame(B, d, I, fin, fedsplit, deficit, {})
nets, ntot, _ = W.build_nets(ch, totals, [])
pool, poolinfo = W.spm_pooler(d)
pw, other = d.pw.to_numpy(), d.other.to_numpy()
Wother = pw[other].sum()
rows = []

def record(name, conv, arr):
    for unit, vals in [('person', arr), ('spm_pooled', pool(arr))]:
        rows.append(dict(scenario=name, financing=conv, unit=unit,
                         total_bn=float((pw * vals)[other].sum() / 1e9),
                         winners_pct=float(pw[other & (vals > 0)].sum() / Wother * 100),
                         mean_usd=float((pw * vals)[other].sum() / Wother)))

for conv in W.CONVENTIONS:
    base = nets[(f'net_social_{conv}', 'central')]
    record('published_central', conv, base)
    alt = (base - ch['wages']['central'] + ch['wages_eps3']['central']
           + ch[f'wages_eps3_receipts_{conv}']['central'])
    record('existing_epsilon3_wage_and_receipt_variant', conv, alt)
    nest = B.nest_rows()
    norm = (1 + meta['wages_P']['gdp_factor']) / 2
    tax_all, _ = B.tax_key(d, I['R_spm'], 'after', I['F_total'], I['S_total'])
    key = tax_all if conv == 'a' else np.ones(len(d))
    for split in ('hs_or_less', 'below_ba'):
        for sigma in (1.5, 2.0, 2.5):
            row = B.pick(nest, split, sigma, 1.0, np.inf)
            alt_wages = B.wage_delta(I['basis'][split], row, True) * norm
            delta_f = (row.induced_current_receipts_bn - I['account'].induced_current_receipts_bn) * norm
            receipts = B.per_person(d, key, delta_f)
            record(f'existing_nest_{split}_sigma_{sigma}', conv,
                   base - ch['wages']['central'] + alt_wages + receipts)
    wave = ch['wages']['central']
    uniform = np.where(other, (pw * wave)[other].sum() / Wother, 0)
    for frac in (0.0, 0.5, 1.5):
        alt = base + (frac - 1) * (wave - uniform)
        assert np.isclose((pw * alt)[other].sum(), (pw * base)[other].sum())
        record(f'aggregate_preserving_wage_dispersion_{frac}', conv, alt)
    record('all_federal_cost_allocated_today', conv,
           base + ch[f'fiscal_federal_today_{conv}']['central'] * deficit['share'] / (1-deficit['share']))

# Audit whether minimizing the dollar total also brackets the number of winners.
# Collapse onto the pooling units once so the exact finite grid is inexpensive.
codes, _ = pd.factorize(d.SPM_ID.to_numpy())
den = np.bincount(codes, weights=np.where(other, pw, 0))
valid = den > 0
def unit_values(arr):
    return np.bincount(codes, weights=np.where(other, pw * arr, 0))[valid] / den[valid]

grid_extrema = []
for conv in W.CONVENTIONS:
    groups = [([f'fiscal_{conv}', 'wages'], ('low', 'high')),
              (['renters', 'landlords'], W.LEVELS)]
    groups += [([k], W.LEVELS) for k in W.SOCIAL if k not in ('renters', 'landlords')]
    choices = [[(level, unit_values(sum(ch[k][level] for k in keys))) for level in levels]
               for keys, levels in groups]
    endpoints = {'min': None, 'max': None}
    for combo in itertools.product(*choices):
        arr = sum(vals for _, vals in combo)
        pct = float(den[valid][arr > 0].sum() / Wother * 100)
        rec = dict(financing=conv, winners_pct=pct,
                   total_bn=float((arr * den[valid]).sum() / 1e9),
                   recipe={'+'.join(keys): lev for (keys, _), (lev, _) in zip(groups, combo)})
        for direction in endpoints:
            best = endpoints[direction]
            if best is None or (pct < best['winners_pct'] if direction == 'min' else pct > best['winners_pct']):
                endpoints[direction] = rec
    grid_extrema.append(endpoints)

out = HERE / '_cache'
out.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(out / 'sensitivity.csv', index=False, lineterminator='\n')
published = pd.read_csv(ROOT / Path(REL).parent / 'derived/net_shares.csv')
for conv in W.CONVENTIONS:
    expected = published[(published.net == f'net_social_{conv}') &
                         (published['stack'] == 'central') &
                         (published.unit == 'spm_unit_pooled')].iloc[0]
    found = next(r for r in rows if r['scenario'] == 'published_central' and
                 r['financing'] == conv and r['unit'] == 'spm_pooled')
    assert np.isclose(found['winners_pct'], expected.winners_share * 100)
(out / 'metadata.json').write_text(json.dumps({'snapshot': SNAPSHOT,
    'snapshot_full': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', SNAPSHOT]).decode().strip(),
    'winners_source_sha256': hashlib.sha256(src).hexdigest(), 'pooling': poolinfo,
    'fiscal': meta['fiscal'], 'deficit': deficit,
    'pooled_winner_share_grid_extrema': grid_extrema,
    'gates_passed': sum(x['passed'] for x in W.GATES.values())}, indent=2) + '\n')
print(pd.DataFrame(rows).to_string(index=False))
print(json.dumps(poolinfo, indent=2))
