"""Operator's 2026-10-15 price ruling, shared by all world-ledger readings.

Only recipient values change on the US side. Mexico's fiscal pesos use GDP
PPP, household purchasing power uses consumption PPP. Historic price rules
are explicit comparisons selected by operator_mexico_money/operator_us_general.
"""
import hashlib
import json
from functools import lru_cache
from pathlib import Path

import numpy as np

from mexico_prices import BUDGET_CLASSES, budget_from_gdp, price_budget, require

HERE = Path(__file__).resolve().parent
VCOLS = ('V_low_bn', 'V_central_bn', 'V_high_bn')
SERVICE_CLASSES = {'medicaid', 'medicare', 'health_services', 'services',
                   'education', 'public_good', 'justice', 'housing_voucher'}
WTP_CLASSES = {'medicaid', 'housing_voucher', 'snap'}
CATEGORY_BY_CLASS = dict(medicaid='9080000', medicare='9080000', health_services='9080000',
                         education='9120000', public_good='1400000', justice='1400000',
                         services='1300000', housing_voucher='9060000')
EXEMPTIONS = {'WTP', 'Mexican prices', 'alternative category prices'}


@lru_cache(maxsize=1)
def price_levels():
    path = HERE / 'inputs/icp_us_pli_2021.json'
    pin = json.loads((HERE / 'inputs/pins.json').read_text())['files'][path.name]
    data = path.read_bytes()
    require('us_icp_price_source_hash', hashlib.sha256(data).hexdigest() == pin['sha256'])
    source = json.loads(data)
    require('us_icp_source_2021', str(source['source']['id']) == '90')
    out = {}
    for row in source['source']['data']:
        keys = {v['concept']: v['id'] for v in row['variable']}
        require('us_icp_world_price_level_dimension', keys['Country'] == 'USA'
                and keys['Time'] == 'YR2021' and keys['Classification'] == 'PX.WL')
        require('us_icp_category_unique', keys['Series'] not in out)
        value = row['value']
        require('us_icp_positive_price', value is not None and np.isfinite(value) and value > 0)
        out[keys['Series']] = float(value)
    require('us_icp_complete_categories', set(CATEGORY_BY_CLASS.values())
            | {'1000000', '9110000', '1107300'} <= set(out))
    return out


def category(line, cls):
    """Use consumption-service prices, including service capital's own function.

    Utilities and residual enterprises lack exact ICP headings: their coarse
    mappings are explicit assumptions in every emitted line receipt.
    """
    require('us_service_class_known', cls in CATEGORY_BY_CLASS, cls=cls, line=line)
    if 'recreation_culture' in line or line.startswith(('capital_rec_', 'capital_return_rec_')):
        return '9110000', 'actual recreation and culture'
    if 'ent_' in line:
        component = line.split('ent_', 1)[1]
        if component.startswith(('transit_', 'airports_', 'ports_', 'tolls_')):
            return '1107300', '[ASSUMPTION] enterprise transport at ICP transport-services mix'
        if component.startswith(('power_', 'water_', 'sewer_')):
            return '9060000', '[ASSUMPTION] utilities at ICP combined housing/water/energy mix'
        if component.startswith('other_'):
            return '1400000', '[ASSUMPTION] residual enterprise at collective-government service mix'
    return CATEGORY_BY_CLASS[cls], 'valuation class service category'


def price_us_services(vgen, enabled=True):
    """Return priced V and its row receipts; all source/fiscal columns stay exact.

    Apply after average-cost/response-only selection. Explicit WTP and price
    arms already value the service and are exempt from a second price discount.
    Zero education value stays zero; a cost-valued education companion is priced.
    """
    v = vgen.copy()
    if not enabled:
        return v
    levels = price_levels()
    require('us_service_not_already_general_priced', 'us_price_factor' not in v
            or v.us_price_factor.eq(1.0).all())
    source_columns = [c for c in v if c not in VCOLS and not c.startswith('us_price_')]
    exemptions = v.get('us_service_price_exemption')
    if exemptions is not None:
        require('us_price_exemption_known', set(exemptions.dropna()) <= EXEMPTIONS)
    receipt = []
    for cls, line, exemption in zip(v.cls, v.line,
                                    exemptions if exemptions is not None else [None] * len(v)):
        if cls not in SERVICE_CLASSES:
            receipt.append(('', 1.0, 'not a cost-valued recipient service'))
            continue
        if cls in WTP_CLASSES or isinstance(exemption, str):
            receipt.append(('', 1.0, 'WTP' if cls in WTP_CLASSES else exemption))
            continue
        series, reason = category(str(line), cls)
        factor = levels['1000000'] / levels[series]
        require('us_service_factor_positive', np.isfinite(factor) and factor > 0)
        receipt.append((series, factor, reason))
    v['us_price_category'] = [x[0] for x in receipt]
    v['us_price_factor'] = [x[1] for x in receipt]
    v['us_price_reason'] = [x[2] for x in receipt]
    v[list(VCOLS)] = v[list(VCOLS)].mul(v.us_price_factor, axis=0)
    require('us_price_cannot_change_fiscal_cost', v[source_columns].equals(vgen[source_columns]))
    require('us_service_values_finite', np.isfinite(v[list(VCOLS)]).all().all())
    return v


def money_price_inputs(I, rates, enabled=True):
    """Original source pesos survive category comparisons; no fiscal uplift."""
    if not enabled:
        return I
    out = dict(I)
    gdp = rates['PA.NUS.PPP']
    budget = I['mxb']
    if 'fiscal_cost_pesos_bn' not in budget:
        budget = budget_from_gdp(budget, gdp)
    budget = price_budget(budget, dict.fromkeys(BUDGET_CLASSES, gdp))
    budget['bn'] = budget.recipient_value_bn
    budget['price_rule'] = 'GDP money'
    for side in ('recipient_value', 'fiscal_cost'):
        require('mexico_budget_all_categories_gdp_money',
                budget.loc[budget.cls.isin(BUDGET_CLASSES), f'{side}_ppp_divisor'].eq(gdp).all())
    out.update(mxb=budget, mexico_tax_ppp_divisor=gdp, mexico_tax_mix='GDP-money',
               remittance_price_basis='consumption', mexico_fiscal_money_rule=True)
    return out


def prepare_us_service_values(vgen, convention='average_cost', enabled=True):
    """Select the reading's public-good quantity before its price adjustment."""
    require('us_public_value_convention', convention in ('average_cost', 'response_only'))
    v = vgen.copy()
    if convention == 'response_only':
        mask = v.cls.eq('public_good')
        for col in VCOLS:
            v.loc[mask, col] = v.loc[mask, 'G_bn']
    return price_us_services(v, enabled)
