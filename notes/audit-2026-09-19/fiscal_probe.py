import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / 'infra/immigration-fiscal/pronatal_equivalence_2026_09_18'))
import lifetime_profiles as L

original = L.A.matrices
def personal_matrices(state):
    shared, personal, renter = original(state)
    return personal, shared, renter
L.A.matrices = personal_matrices
p = L.profiles().pivot(index='band', columns='group', values='balance_per_person')
result = {}
for rate in [0.0, 0.03]:
    ref = L.lifetime(p['third_plus_nh_white'], 0, rate)
    for group in p.columns:
        start = 25 if group == 'mexico_born' else 0
        val = L.lifetime(p[group], start, rate)
        result[f'{group}|{rate}'] = {'balance': val, 'vs_white_child': ref-val}
print('PERSON_SOURCE_LIFETIMES', json.dumps(result, indent=2))
rate = 879.879 / ((26330.142473 + 28307.312291) / 2)
debt = 263.224141 * ((1+rate)**10-1)/rate
print('COMPOUND_CHECK', rate, debt, debt-10*263.224141)
Path('/private/tmp/fiscal_audit_probe_20260919.json').write_text(json.dumps(result, indent=2))
