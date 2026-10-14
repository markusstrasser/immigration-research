#!/usr/bin/env python3
"""M4: conditional surviving-SPM-unit SNAP, and unpriced health eligibility diagnostics.

This is deliberately not an identified benefit-removal estimator. SPM units are
proxies for SNAP/MAGI units; annual incomes and deduction totals are proxies for
monthly legally countable amounts. Never adopt the returned M4 silently:
details['adoptable'] is False. Sources are pinned and constants parsed at runtime.

Standalone: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/benefits.py
"""
from __future__ import annotations

import argparse
import hashlib
import html as html_util
from html.parser import HTMLParser
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time
import xml.etree.ElementTree as ET
import zipfile

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
INPUTS = LANE / 'inputs'
PERSON_COLUMNS = ['SPM_NUMPER', 'SPM_SNAPSUB', 'SPM_TOTVAL',
                  'SPM_CHILDCAREXPNS', 'SPM_CHILDSUPPD', 'SPM_MEDXPNS',
                  'PTOTVAL', 'SSI_VAL', 'PAW_VAL', 'MCAID', 'PCHIP',
                  'PUB', 'PRIV', 'PRDISFLG']
HOUSEHOLD_COLUMNS = ['HFOODMO', 'HFOODNO', 'HFDVAL', 'HFOODSP']
GENS = ('G1', 'G2', 'G3+')


def require(ok, name):
    if not ok:
        raise ValueError(f'[BLOCKED] M4 {name}')


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def verify_sources():
    pins = json.loads((INPUTS / 'benefit_pins.json').read_text())
    for name, pin in pins['files'].items():
        path = INPUTS / name
        require(path.exists(), f'missing pinned input {name}')
        with path.open('rb') as f:
            digest = hashlib.file_digest(f, 'sha256').hexdigest()
        require(digest == pin['sha256'], f'stale input {name}')
    return pins


def amounts(text):
    return [float(x.replace(',', '')) for x in re.findall(r'\$([\d,]+(?:\.\d+)?)', text)]


def table(text, title, end):
    require(title in text and end in text.split(title, 1)[1], f'cannot parse table {title}')
    return text.split(title, 1)[1].split(end, 1)[0]


def numeric_rows(text, width):
    rows = []
    for line in text.splitlines():
        values = amounts(line)
        if values and re.match(r'^\s*\d+(?:\+)?\s+', line):
            require(len(values) == width, 'primary table column count changed')
            rows.append(values)
    return np.asarray(rows, float)


def xml_text(name):
    return ' '.join(ET.parse(INPUTS / name).getroot().itertext())


class PrimaryTable(HTMLParser):
    """Read cells from the first CMS table, dropping superscript footnote markers."""
    def __init__(self):
        super().__init__()
        self.rows, self.row, self.cell = [], None, None
        self.in_table = False
        self.done = False
        self.sup = False

    def handle_starttag(self, tag, attrs):
        if tag == 'table' and not self.done:
            self.in_table = True
        if not self.in_table:
            return
        if tag == 'tr':
            self.row = []
        elif tag in ('td', 'th'):
            self.cell = ''
        elif tag == 'sup':
            self.sup = True

    def handle_data(self, data):
        if self.in_table and self.cell is not None and not self.sup:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == 'sup':
            self.sup = False
        if not self.in_table:
            return
        if tag in ('td', 'th') and self.cell is not None:
            self.row.append(self.cell.strip())
            self.cell = None
        elif tag == 'tr' and self.row:
            self.rows.append(self.row)
        elif tag == 'table':
            self.in_table = False
            self.done = True


def rules():
    verify_sources()
    out = {}
    for year in (24, 25):
        text = (INPUTS / f'benefit_snap{year}_max.txt').read_text()
        maxima = table(text, 'Table 1:', 'Deductions')
        maxrows = numeric_rows(maxima, 7)
        increment = amounts(next(x for x in maxima.splitlines() if '+$' in x))
        deduction = table(text, 'Standard Deductions', 'Table 3:')
        standard = numeric_rows(deduction, 5)
        shelter = amounts(table(text, 'Table 3:', 'Table 4:' if year == 25 else 'Table 5:'))
        inc = (INPUTS / f'benefit_snap{year}_income.txt').read_text()
        net = table(inc, 'Table 1:', 'Table 2:')
        gross = table(inc, 'Table 2:', 'Table 3:')
        nr, gr = numeric_rows(net, 3), numeric_rows(gross, 3)
        ni = amounts(next(x for x in net.splitlines() if 'Each Additional' in x))
        gi = amounts(next(x for x in gross.splitlines() if 'Each Additional' in x))
        mintxt = (INPUTS / f'benefit_snap{year}_min.txt').read_text()
        minimum = amounts(next(x for x in mintxt.splitlines() if re.match(r'^\s*1-2\s+', x)))
        require(maxrows.shape == (8, 7) and standard.shape == (6, 5)
                and nr.shape == (8, 3) and gr.shape == (8, 3)
                and len(increment) == 7 and len(shelter) == 5 and len(minimum) == 7,
                'USDA primary tables have unexpected shape')
        out[year] = dict(max=maxrows, increment=np.array(increment), standard=standard,
                         shelter=np.array(shelter), net=nr, gross=gr,
                         net_increment=np.array(ni), gross_increment=np.array(gi),
                         minimum=np.array(minimum))
    law = xml_text('benefit_snap_benefits.xml')
    deductions = xml_text('benefit_snap_deductions.xml')
    earned = re.search(r'gross monthly earned income by (\d+) percent', law)
    benefit = re.search(r'reduced by (\d+) percent of', law)
    medical = re.search(r'\$(\d+) per month', deductions)
    require(earned is not None and benefit is not None and medical is not None, 'CFR rule parse failed')
    out['earned_rate'] = float(earned[1]) / 100
    out['benefit_rate'] = float(benefit[1]) / 100
    out['medical_floor'] = float(medical[1])
    age60 = re.search(r'age (\d+)\+', (INPUTS / 'benefit_snap24_max.txt').read_text())
    require(age60 is not None, 'SNAP elderly age parse failed')
    out['snap_elderly_age'] = int(age60[1])
    magi = xml_text('benefit_magi_law.xml')
    disregard = re.search(r'equivalent to (\d+) percentage points', magi)
    require(disregard is not None, 'MAGI disregard parse failed')
    out['magi_disregard'] = float(disregard[1])
    age65 = re.search(r'Individuals who are age (\d+) or older', magi)
    require(age65 is not None, 'MAGI senior age parse failed')
    out['magi_senior_age'] = int(age65[1])
    # The FR PDF has three columns. Identify each complete monetary table from
    # its characteristic dotted leaders; sort tables by the parsed first value.
    text = (INPUTS / 'benefit_fpl24_fr.txt').read_text()
    fplrows = [(int(n), float(v.replace(',', ''))) for n, v in
               re.findall(r'([1-8])\s+\.{3,}\s+\$?([\d,]+)', text)]
    require(len(fplrows) == 24, '2024 Federal Register poverty table changed')
    groups = [fplrows[i:i + 8] for i in range(0, 24, 8)]
    require(all([x[0] for x in g] == list(range(1, 9)) for g in groups), 'FPL rows out of order')
    groups.sort(key=lambda g: g[0][1])
    out['fpl'] = np.array([[x[1] for x in g] for g in groups])  # contiguous, HI, AK
    parser = PrimaryTable()
    html = (INPUTS / 'benefit_medicaid.html').read_text()
    require('December 1, 2023' in html, 'CMS threshold vintage changed')
    parser.feed(html)
    require(len(parser.rows) == 52 and all(len(x) == 9 for x in parser.rows), 'CMS states table changed')
    states = json.loads((INPUTS / 'benefit_states.json').read_text())
    require(isinstance(states, list) and 'NAME' in states[0] and 'state' in states[0], 'Census geography schema invalid')
    name_col, code_col = states[0].index('NAME'), states[0].index('state')
    codes = {x[name_col]: int(x[code_col]) for x in states[1:] if x[name_col] != 'Puerto Rico'}
    percent = lambda x: float(re.search(r'(\d+)%', x)[1]) if '%' in x else 0.0
    med = {}
    for row in parser.rows[1:]:
        require(row[0] in codes, f'CMS state not mapped: {row[0]}')
        v = np.array([percent(x) for x in row[1:]], float)
        # CMS's 200% entry for NY/MN includes BHP, which is not Medicaid.
        if row[0] in ('New York', 'Minnesota'):
            footnote = re.search(r'Adults with incomes from above (\d+)% and up to (\d+)%', html)
            require(footnote is not None, 'CMS BHP note missing')
            v[7] = float(footnote[1])
        med[codes[row[0]]] = v
    out['medicaid'] = med
    plain = html_util.unescape(re.sub(r'<[^>]+>', ' ', html))
    notes = {}
    for state_name in ('California', 'Minnesota'):
        pattern = (r'Separate CHIP in California covers certain children up to age (\d+)\s+with incomes up to (\d+)%'
                   if state_name == 'California' else
                   r'Minnesota covers children up to age (\d+) with incomes up to (\d+)%')
        note = re.search(pattern, plain)
        require(note is not None, f'CMS statewide infant note missing: {state_name}')
        notes[state_name] = dict(state=codes[state_name], age_limit=int(note[1]), threshold=float(note[2]))
    out['statewide_infant_notes'] = notes
    return out


def sized(table_, increment, size, region):
    size = np.asarray(size, int)
    require(bool((size >= 1).all()), 'nonpositive assistance-unit size')
    return table_[np.minimum(size, 8) - 1, region] + np.maximum(size - 8, 0) * increment[region]


def snap_rule(rule, year, size, gross, earned, care, medical, support, elderly, state, shelter):
    """Annualized standard federal SNAP schedule; all financial arguments annual.

    Assumptions: unit is SPM, steady monthly income; all provided care/support are
    deductible; medical cost only when an elderly/disabled person is present;
    assets, citizenship, ABAWD, students, sanctions and state BBCE not identified.
    Alaska uses urban schedule only; callers exclude Alaska from priced scenarios.
    """
    r = rule[year]
    region = np.where(state == 2, 1, np.where(state == 15, 5, 0))
    dregion = np.where(state == 2, 1, np.where(state == 15, 3, 0))
    iregion = np.where(state == 2, 1, np.where(state == 15, 2, 0))
    gross = np.maximum(gross, 0) / 12
    earned = np.maximum(earned, 0) / 12
    deduction = r['standard'][np.minimum(size, 6) - 1, dregion]
    medical_ded = np.where(elderly, np.maximum(medical / 12 - rule['medical_floor'], 0), 0)
    net = np.maximum(gross - rule['earned_rate'] * earned - deduction
                     - np.maximum(care, 0) / 12 - medical_ded - np.maximum(support, 0) / 12, 0)
    if shelter == 'cap':
        # This varies the allowable deduction itself, not an observed rent.
        net = np.maximum(net - np.where(elderly, net, r['shelter'][dregion]), 0)
    else:
        require(shelter == 'zero', 'unknown shelter scenario')
    gross_limit = sized(r['gross'], r['gross_increment'], size, iregion)
    net_limit = sized(r['net'], r['net_increment'], size, iregion)
    eligible = ((gross <= gross_limit) | elderly) & (net <= net_limit)
    maximum = sized(r['max'], r['increment'], size, region)
    monthly = np.maximum(maximum - np.ceil(rule['benefit_rate'] * net), 0)
    monthly = np.where(size <= 2, np.maximum(monthly, r['minimum'][region]), monthly)
    return np.where(eligible, monthly, 0) * 12


def sdr(x):
    x = np.asarray(x)
    require(x.shape[-1] == 161, 'requires full weight plus all 160 replicate weights')
    return np.sqrt(4 / 160 * np.square(x[..., 1:] - x[..., :1]).sum(axis=-1))


def unit_values(d, fields):
    for f in fields:
        require(d.groupby('SPM_ID', sort=False)[f].nunique(dropna=False).eq(1).all(), f'nonconstant unit field {f}')


def attribute(change, unit, W, union, gen, mixed):
    """Attribute each unit's weighted change to removed members' weight shares.

    Preserve weights of all people. A unit's event weight is its original mean
    person weight; its after-removal benefit is split among surviving people in
    inverse proportion to their aggregate weight, independently per replicate.
    """
    nu = len(change)
    wm = np.stack([np.bincount(unit, weights=W[:, r] * union, minlength=nu) for r in range(161)], axis=1)
    out = np.zeros((3, 161))
    for g in range(3):
        wg = np.stack([np.bincount(unit, weights=W[:, r] * (gen == g), minlength=nu) for r in range(161)], axis=1)
        require((wm[mixed] != 0).all(), 'zero removed-member replicate mass')
        share = np.divide(wg, wm, out=np.zeros_like(wg), where=wm != 0)
        out[g] = (change * share * mixed[:, None]).sum(axis=0)
    national = (change * mixed[:, None]).sum(axis=0)
    require(np.max(np.abs(out.sum(axis=0) - national)) < 1e-6,
            'generation closure exceeds 1e-6bn')
    return out


def compute(d, W, union, gen, civ, model, flag=None):
    """Return conditional M4 + sensitivity terms (3x161), JSON-safe diagnostics.

    Positive raises removal net cost. Benefits to surviving nonmembers that grow
    reduce removal savings and give a negative adjustment to v7's member costs.
    Medicaid/CHIP and ACA changes are unidentified: held numerically and disclosed,
    never asserted zero in reality. No added-lineage effects are extrapolated.
    """
    rule = rules()
    missing = sorted(set(PERSON_COLUMNS + ['GESTFIPS', 'SPM_ID', 'pwwgt0',
                                         'A_AGE', 'WSAL_VAL', 'SEMP_VAL', 'FRSE_VAL']) - set(d.columns))
    require(not missing, f'missing CPS columns {missing}')
    W = np.asarray(W, float)
    union, civ, gen = np.asarray(union, bool), np.asarray(civ, bool), np.asarray(gen, int)
    # Census SDR replicate weights contain signed values. Never clip them:
    # preserve the pinned survey replicates, while full sample weights are positive.
    require(W.shape == (len(d), 161) and np.isfinite(W).all() and (W[:, 0] > 0).all(), 'invalid replicate frame')
    require(np.array_equal(union, gen >= 0) and (civ[union]).all(), 'membership frame inconsistent')
    require(set(gen).issubset({-1, 0, 1, 2}), 'unrecognized generation')
    require(not d[PERSON_COLUMNS].isna().any().any(), 'missing benefit data')
    fields = ['SPM_SNAPSUB', 'SPM_TOTVAL', 'SPM_CHILDCAREXPNS', 'SPM_CHILDSUPPD', 'SPM_MEDXPNS', 'SPM_NUMPER', 'GESTFIPS']
    unit_values(d, fields)
    unit, labels = pd.factorize(d.SPM_ID, sort=False)
    nu = len(labels)
    first = np.unique(unit, return_index=True)[1]
    size = np.bincount(unit, minlength=nu)
    require(np.array_equal(size, d.SPM_NUMPER.to_numpy()[first]), 'SPM roster does not close to NUMPER')
    nm = np.bincount(unit, weights=union, minlength=nu).astype(int)
    remaining = size - nm
    mixed = (nm > 0) & (remaining > 0)
    all_civ = np.bincount(unit, weights=~civ, minlength=nu) == 0
    state = d.GESTFIPS.to_numpy(int)[first]
    priced = mixed & all_civ & (state != 2)
    B = d.SPM_SNAPSUB.to_numpy(float)[first]
    require((B >= 0).all(), 'negative reported SNAP')
    sumv = lambda v: np.bincount(unit, weights=v, minlength=nu)
    pt = d.PTOTVAL.to_numpy(float)
    # Preserve the SPM_TOTALVAL residual and remove each member's own total income.
    income0 = d.SPM_TOTVAL.to_numpy(float)[first]
    income1 = income0 - sumv(np.where(union, pt, 0))
    earn = (d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy(float)
    earn0, earn1 = sumv(earn), sumv(np.where(union, 0, earn))
    # CPS deductions are annual SPM-unit totals, with no payer/dependent allocation.
    # Pro-rate their remaining amounts by the fraction of persons who remain.
    fraction = remaining / size
    care0 = d.SPM_CHILDCAREXPNS.to_numpy(float)[first]
    med0 = d.SPM_MEDXPNS.to_numpy(float)[first]
    support0 = d.SPM_CHILDSUPPD.to_numpy(float)[first]
    special = (d.A_AGE.ge(rule['snap_elderly_age']) | d.SSI_VAL.gt(0) | d.PRDISFLG.eq(1)).to_numpy()
    old_special, new_special = sumv(special) > 0, sumv(special & ~union) > 0
    safe_n = np.maximum(remaining, 1)
    allw = np.stack([np.bincount(unit, weights=W[:, r], minlength=nu) for r in range(161)], axis=1)
    nonw = np.stack([np.bincount(unit, weights=W[:, r] * ~union, minlength=nu) for r in range(161)], axis=1)
    require((nonw[priced] != 0).all(), 'zero surviving-person replicate mass')
    unitw = allw / size[:, None]
    # Baseline exactly reproduces the source key, including unequal CPS weights.
    key = B[unit] / size[unit]
    original_national = key[civ] @ W[civ]
    original_member = key[union] @ W[union]
    original_other = key[civ & ~union] @ W[civ & ~union]
    require(np.max(np.abs((original_member + original_other - original_national) / 1e9)) < 1e-6,
            'baseline SNAP national closure')
    require((original_national > 0).all(), 'empty SNAP key')
    line = next(x for x in model['spending']['lines'] if x['id'] == 'snap')
    require(line.get('preferred_key', 'snap') == 'snap', 'SNAP line changed preferred key')
    # The account denominator is explicitly declared by its stored frame audit.
    stored = json.loads((FISCAL / 'backtest_admin_totals_2026_09_28/derived/prediction_audit.json').read_text())
    hf = stored['household_fraction']
    pubshare = float(key[union] @ d.pwwgt0.to_numpy()[union] / (key[civ] @ d.pwwgt0.to_numpy()[civ]))
    require(abs(pubshare - line['keys']['snap']['personal']['share']) < 5e-9, 'positive control SNAP model share')
    conversion = line['national_bn'] * hf / original_national
    terms, fit = {}, {}
    for shelter in ('zero', 'cap'):
        r0, r1, maximum = np.zeros(nu), np.zeros(nu), np.zeros(nu)
        for year, months in ((24, 9), (25, 3)):
            r0 += months / 12 * snap_rule(rule, year, size, income0, earn0, care0, med0, support0, old_special, state, shelter)
            r1 += months / 12 * snap_rule(rule, year, safe_n, income1, earn1, care0 * fraction,
                                        med0 * fraction, support0 * fraction, new_special, state, shelter)
            region = np.where(state == 2, 1, np.where(state == 15, 5, 0))
            maximum += months * sized(rule[year]['max'], rule[year]['increment'], safe_n, region)
        # Census anchored level + schedule difference. Exactly B without removal.
        require(np.max(np.abs((B + r0 - r0) - B)) < 1e-6, 'calibration identity')
        predicted = np.minimum(np.maximum(B + r1 - r0, 0), maximum)
        existing = np.where(B > 0, predicted, 0)
        for tag, after in [('existing_participation', existing), ('full_takeup_proxy', predicted)]:
            change = (B[:, None] / size[:, None] * nonw - after[:, None] * unitw) * conversion
            terms[f'SNAP_{shelter}_{tag}'] = attribute(change, unit, W, union, gen, priced)
        active = B > 0
        fit[shelter] = dict(reported_bn=float((B * unitw[:, 0])[active & all_civ].sum() / 1e9),
                            raw_schedule_bn=float((r0 * unitw[:, 0])[all_civ].sum() / 1e9),
                            reported_benefit_units_failing_proxy_income_test=int((active & (r0 == 0) & all_civ).sum()),
                            dollars_on_reported_units_failing_proxy_income_test_bn=float(
                                (B * unitw[:, 0])[active & (r0 == 0) & all_civ].sum() / 1e9),
                            residual_l1_bn=float((np.abs(B - r0) * unitw[:, 0])[all_civ].sum() / 1e9))
    # Program-value envelope, conditional on SPM assistance-unit membership and
    # original unit event weights. It does not impose annual income-test proxies.
    original_non = B[:, None] / size[:, None] * nonw
    terms['SNAP_envelope_low'] = attribute((original_non - maximum[:, None] * unitw) * conversion,
                                         unit, W, union, gen, priced)
    terms['SNAP_envelope_high'] = attribute(original_non * conversion, unit, W, union, gen, priced)
    require((terms['SNAP_envelope_low'].sum(axis=0) <= terms['SNAP_envelope_high'].sum(axis=0)).all(),
            'SNAP envelope inverted')
    med = medicaid_diagnostics(d, W, union, unit, size, remaining, mixed & all_civ,
                               state, income0, income1, rule)
    details = dict(adoptable=False, status='[DEGRADED] conditional SNAP; Medicaid/CHIP and ACA spending changes unidentified',
                   recommended='withhold M4; publish partial-stack and conditional scenarios beside it',
                   frame=dict(mixed_spm_units=int(mixed.sum()), priced_snap_units=int(priced.sum()),
                              signed_replicate_weights=int((W[:, 1:] < 0).sum()),
                              excluded_alaska_units=int((mixed & (state == 2)).sum()),
                              excluded_noncivilian_units=int((mixed & ~all_civ).sum()),
                              surviving_persons=float(W[(~union) & priced[unit], 0].sum()),
                              identified_only=True, lineage='No mixed-unit records for added people; no extrapolation'),
                   calibration=dict(original_national_snap_key_bn=float(original_national[0] / 1e9),
                                    published_snap_target_share=pubshare, household_fraction=hf,
                                    account_bn_per_cps_bn=float(conversion[0] * 1e9), baseline_fit=fit),
                   status_rule='Imputed unauthorized flag is not a legal eligibility record; legal program status remains unidentified',
                   Medicaid_CHIP=med, ACA=dict(status='unidentifiable; spending held',
                       missing=['Form 1095-A enrollment premiums and SLCSP', 'APTC paid',
                                'monthly marketplace coverage', 'employer coverage affordability',
                                'legal tax-family MAGI and immigration eligibility']),
                   assumptions=['SPM unit is proxy assistance unit', 'Annual incomes treated as steady monthly incomes',
                       'SPM total-income residual held on surviving unit', 'CPS deduction totals pro-rated by persons remaining',
                       'SNAP shelter deduction zero vs maximum; not observed rent or utility costs',
                       'Federal income tests only; assets, BBCE, ABAWD, students and status not identified',
                       'SNAP reported annual level residual held; existing participation vs full-takeup proxy',
                       'Original mean person weight is unit event weight; survivor weights unchanged',
                       'Health eligibility uses SPM income proxy; neither receipt nor expected spending changes are inferred'],
                   national_closure_max_bn=float(np.max(np.abs((original_member + original_other - original_national) / 1e9))),
                   summaries={k: dict(bn=float(v[:, 0].sum()), se_bn=float(sdr(v.sum(axis=0))),
                                      by_generation_bn={g: float(v[i, 0]) for i, g in enumerate(GENS)},
                                      by_generation_se_bn={g: float(sdr(v[i])) for i, g in enumerate(GENS)})
                              for k, v in terms.items()})
    return dict(M4=terms['SNAP_zero_existing_participation'], terms=terms, details=details)


def medicaid_diagnostics(d, W, union, unit, size, remaining, mixed, state, income0, income1, rule):
    """Income-test proxy transitions. Retain spending at its fixed MEPS key."""
    age = d.A_AGE.to_numpy()
    nonmember = ~union & mixed[unit]
    # MAGI does not apply to age/disability routes; two states' special CHIP
    # counties and age-19/20 optional routes require finer policy data.
    supported = nonmember & (age < rule['magi_senior_age']) & ~d.PRDISFLG.eq(1).to_numpy() & ~d.SSI_VAL.gt(0).to_numpy()
    require(set(state).issubset(rule['medicaid']), 'missing state Medicaid threshold')
    values = np.stack([rule['medicaid'][int(x)] for x in state])[unit]
    child_column = np.where(age < 1, 0, np.where(age < 6, 1, 2))
    med_child = values[np.arange(len(d)), child_column]
    chip = np.maximum(med_child, values[:, 3])
    for note in rule['statewide_infant_notes'].values():
        matches = (state[unit] == note['state']) & (age < note['age_limit'])
        chip[matches] = np.maximum(chip[matches], note['threshold'])
    # Broad parent proxy only: adult shares an SPM unit with a child; this is not
    # a legal caretaker determination and is explicitly disclosed.
    child0 = np.bincount(unit, weights=age < 19, minlength=len(size)) > 0
    child1 = np.bincount(unit, weights=(age < 19) & ~union, minlength=len(size)) > 0
    parent0 = np.where(child0[unit], values[:, 6], 0)
    parent1 = np.where(child1[unit], values[:, 6], 0)
    adult0, adult1 = np.maximum(parent0, values[:, 7]), np.maximum(parent1, values[:, 7])
    t0 = np.where(age < 19, chip, adult0)
    t1 = np.where(age < 19, chip, adult1)
    fregion = np.where(state == 2, 2, np.where(state == 15, 1, 0))
    fpl = rule['fpl']
    def poverty(n):
        return fpl[fregion, np.minimum(np.maximum(n, 1), 8) - 1] + np.maximum(n - 8, 0) * (fpl[fregion, 1] - fpl[fregion, 0])
    before = np.maximum(income0, 0)[unit] <= poverty(size)[unit] * (t0 + rule['magi_disregard']) / 100
    after = np.maximum(income1, 0)[unit] <= poverty(remaining)[unit] * (t1 + rule['magi_disregard']) / 100
    before &= t0 > 0
    after &= t1 > 0
    reported = d.MCAID.eq(1).to_numpy()
    out = dict(status='[DEGRADED] income eligibility proxy only; all Medicaid/CHIP spending held',
               threshold_vintage='CMS December 1, 2023 snapshot held across calendar 2024',
               missing=['legal MAGI household', 'monthly MAGI', 'qualified status and five-year eligibility',
                        'pregnancy', 'state 2024 within-year threshold changes', 'continuous eligibility/takeup',
                        'special CHIP counties and optional age-19/20/demonstration routes'],
               spending_rule='fixed MEPS age-by-birth expected payment key, unchanged by simulated eligibility',
               groups={})
    for label, mask in [('children', age < 19), ('adults', (age >= 19) & (age < rule['magi_senior_age']))]:
        group = supported & mask
        cases = dict(survivors=group, reported_covered=group & reported,
                     proxy_eligible_before=group & before, proxy_eligible_after=group & after,
                     newly_proxy_eligible=group & ~before & after, lost_proxy_eligibility=group & before & ~after,
                     reported_covered_but_proxy_ineligible_before=group & reported & ~before,
                     reported_covered_losing_proxy_eligibility=group & reported & before & ~after)
        out['groups'][label] = {k: dict(persons=float(W[m, 0].sum()),
                                      se_persons=float(sdr(W[m].sum(axis=0)))) for k, m in cases.items()}
    out['unsupported_survivors'] = float(W[nonmember & ~supported, 0].sum())
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, default=LANE / 'derived/benefit_results.json')
    parser.add_argument('--arrays-out',type=Path,help='Optional exact component replicates for bounded-memory parent integration')
    args = parser.parse_args()
    start = time.perf_counter()
    c = module(FISCAL / 'mixed_unit_credits_2026_10_14/credits.py', 'm4_credits')
    d = c.load()
    civ, union, gen = c.groups(d)
    W, _, _ = c.row4_weights(d, civ, union)
    d = d.drop(columns=c.REPS[1:])
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        extra = pd.read_csv(z.open('pppub25.csv'), usecols=['PH_SEQ', 'PPPOS'] + PERSON_COLUMNS)
        h = pd.read_csv(z.open('hhpub25.csv'), usecols=['H_SEQ'] + HOUSEHOLD_COLUMNS)
    d = d.merge(extra, on=['PH_SEQ', 'PPPOS'], validate='one_to_one').merge(h, on='H_SEQ', validate='many_to_one')
    result = compute(d, W, union, gen, civ, json.loads(c.MODEL.read_text()))
    args.out.parent.mkdir(exist_ok=True, parents=True)
    args.out.write_text(json.dumps(result['details'], indent=2, sort_keys=True) + '\n')
    if args.arrays_out is not None:
        args.arrays_out.parent.mkdir(parents=True,exist_ok=True)
        np.savez_compressed(args.arrays_out,**result['terms'])
    elapsed = time.perf_counter() - start
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    rss_gb = rss / (1e9 if sys.platform == 'darwin' else 1e6)
    print(json.dumps({'elapsed_seconds': elapsed, 'max_rss_gb': rss_gb}))
    print(json.dumps(result['details']['summaries'], indent=2))
    print(result['details']['status'])


if __name__ == '__main__':
    main()
