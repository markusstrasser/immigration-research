"""Publish separate-vintage policy companions without constructing a false total.

Native-First: uses the upstream source companion and this lane's calibrated
eligible-record subset. Fiscal years and calendar cash readings never sum.
"""
import hashlib
import json
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent
sys.path.insert(0,str(FISCAL/'scripts'))
from memory_budget import require_within_budget


def customs_current_vintage(upstream):
    """Select the source lane's September-30 BEA sensitivity, by named ends."""
    rows=[r for r in upstream['rows'] if r['part']=='customs_historical_current_bea'
          and r['which']=='set']
    if len(rows)!=2 or {r['end'] for r in rows}!={'low','high'}:
        raise ValueError('[BLOCKED] current-BEA customs companion missing unique named ends')
    if abs(rows[0]['delta_net_cost_bn']-rows[1]['delta_net_cost_bn'])>1e-9:
        raise ValueError('[BLOCKED] current-BEA customs companion ends differ')
    return rows[0]['delta_net_cost_bn']


def main():
    source=FISCAL/'consumption_tax_bases_r5_2026_10_15/derived/companion_summary.json'
    upstream=json.loads(source.read_text())
    individual=json.loads((HERE/'derived/oct16/tax_summary.json').read_text())
    rows=upstream['rows']
    expensing={end:sum(r['delta_net_cost_bn'] for r in rows if r['part']=='business_expensing_conditional'
                       and r['which']=='set' and r['end']==end) for end in ('low','high')}
    customs=customs_current_vintage(upstream)
    if set(expensing)!=set(('low','high')) or any(v<=0 for v in expensing.values()):
        raise ValueError('[BLOCKED] FY2028 expensing source absent')
    result=dict(case='oct16',status='partial; complete present-law total unmeasured',
      replacement_lead='The legacy individual-tax and eligibility subset approximately balanced on the old v5 frame. It was never a complete current-law estimate.',
      calibrated_located_subset=individual['net_benefit_cuts_minus_tax_cuts_bn'],
      calibrated_scope='located calibrated records, original latent descendants and completion; constructed coverage has no identified eligible applicant/tax-unit cells',
      legacy_subset=upstream['legacy_companion_net_taken_bn'],
      account_law='income-year2024 tax and benefit rules, pensions at what current law can pay (2026 Trustees)',
      fy2028_expensing=dict(delta_cost_bn=expensing,source_population='source companion v8 item6 keys',
        year='FY2028',price_year=2024,conditional=True),
      cy2025_customs=dict(delta_cost_bn=customs,year='CY2025',price_year=2024,
        source_part='customs_historical_current_bea',
        bea_vintage=upstream['customs_bridge']['current_bea']['vintage'],
        scope='historical customs sensitivity, not a certified FY2028 tariff-policy projection'),
      combined_total=None,no_sum_rule='FY2028 expensing and CY2025 customs are different-year objects; never sum',
      source_sha256={str(source.relative_to(FISCAL)):hashlib.sha256(source.read_bytes()).hexdigest()})
    require_within_budget('oct16 policy scope export')
    (HERE/'derived/oct16/policy_scope.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    main()
