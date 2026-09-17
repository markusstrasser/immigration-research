"""Reconcile held partial fiscal accounts and compute conditional break-even values."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

p = argparse.ArgumentParser()
p.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[4])
p.add_argument('--output-dir', type=Path, default=Path(__file__).resolve().parents[1]/'derived/fiscal')
a = p.parse_args()
source = a.repo/'infra/immigration-fiscal/gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv'
d = pd.read_csv(source)
rows = []
for (allocation, group), sub in d.groupby(['allocation', 'group']):
    s = sub.set_index('metric')
    assert s.index.is_unique
    components = {'modeled_tax_total': 1, 'selected_cash_total': -1,
                  'selected_noncash_total': -1, 'employer_payroll': 1,
                  'sales_tax_share35': 1, 'property_tax_owner': 1, 'k12_charged_acs_native': -1}
    recomputed = sum(sign*s.loc[key, 'estimate'] for key, sign in components.items())
    balance = s.loc['extended_balance_base', 'estimate']
    assert np.isclose(recomputed, balance, rtol=0, atol=1e-8)
    base = d[(d.allocation == allocation)&(d.metric == 'extended_balance_base')].set_index('group')
    white_gap = balance-base.loc['third_plus_nh_white', 'estimate']
    assert np.isclose(white_gap, s.loc['extended_balance_base', 'difference_from_third_plus_nh_white'])
    rows.append({'allocation': allocation, 'group': group, 'partial_modeled_balance': balance,
                 'gap_to_white_reference': white_gap,
                 'gap_to_all_native_average': balance-base.loc['all_native', 'estimate'],
                 'omitted_net_dollars_for_zero_full_balance': -balance,
                 'omitted_relative_net_dollars_for_zero_white_gap': -white_gap})
a.output_dir.mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows).to_csv(a.output_dir/'conditional_thresholds.csv', index=False)
(a.output_dir/'audit.json').write_text(json.dumps({'status': 'PASS', 'source': str(source),
    'sha256': hashlib.sha256(source.read_bytes()).hexdigest(), 'reconciled_group_accounts': len(rows),
    'interpretation': 'Reconciliation of held aggregate outputs, not new microdata replication. Thresholds are conditional bookkeeping, not empirical bounds. All-native comparison includes the focal native-born group; no new standard errors inferred.'}, indent=2)+'\n')
print(pd.DataFrame(rows).query("group == 'mexican_second_gen'").to_string(index=False))
