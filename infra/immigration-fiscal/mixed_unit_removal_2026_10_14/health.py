#!/usr/bin/env python3
"""Conditional survivor Medicaid/CHIP and enhanced-2024 ACA arms.

All outputs are adjustments to removal cost: additional survivor spending is
negative. Annual CPS income and a reconstructed statutory household are used;
they do not identify monthly eligibility or future participation. Costs bridge
official FY2023 state/group FYE costs to 2024; never label them measured CY2024.
Standalone uses the same 161 row-4 weights as removal.py, below 2.5 GB RSS.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import resource
import sys
import time
import zipfile

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import openpyxl

LANE = Path(__file__).resolve().parent
INPUTS = LANE / 'inputs'
GENS = ('G1', 'G2', 'G3+')
EXTRA = ['PTOTVAL', 'SSI_VAL', 'PRDISFLG', 'MCAID', 'PCHIP', 'PUB', 'PRIV',
         'NOW_MCAID', 'NOW_PUB', 'NOW_MCARE', 'NOW_PRIV', 'NOW_DEPMRK',
         'NOW_MRK','NOW_MRKS','NOW_DEPMRKS','NOW_GRP',
         'SPM_NUMPER','SPM_TOTVAL',
         'A_SPOUSE', 'PEPAR1TYP', 'PEPAR2TYP']


def require(ok, message):
    if not ok:
        raise ValueError('[BLOCKED] health ' + message)


def module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    obj = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def sdr(x):
    x = np.asarray(x)
    require(x.shape[-1] == 161, 'all 160 SDR replicates required')
    return np.sqrt(4 / 160 * ((x[..., 1:] - x[..., :1]) ** 2).sum(axis=-1))


def verify():
    pins = json.loads((INPUTS / 'health_pins.json').read_text())
    for name, p in pins['files'].items():
        with (INPUTS / name).open('rb') as f:
            require(hashlib.file_digest(f, 'sha256').hexdigest() == p['sha256'], 'stale source ' + name)
    return pins


def state_codes():
    a = json.loads((INPUTS / 'benefit_states.json').read_text())
    return {r[a[0].index('NAME')]: int(r[a[0].index('state')]) for r in a[1:] if r[a[0].index('NAME')] != 'Puerto Rico'}


def primary_rows(text, heading, end, codes):
    require(heading in text, 'missing primary heading ' + heading)
    block = text.split(heading, 1)[1].split(end, 1)[0]
    block = re.sub(r'District of\s*\n\s*([^\n]*)\n\s*Columbia', r'District of Columbia  \1', block)
    out = {}
    for line in block.splitlines():
        line = re.sub(r'^December 2024\s+', '', line)
        line = re.sub(r'\s+Section 2: Trends\s*$', '', line)
        name = next((name for name in sorted(codes,key=len,reverse=True) if re.match(re.escape(name)+r'(?:\d)?\s+',line.strip())),None)
        if name:
            rest = re.sub('^'+re.escape(name)+r'\d?\s*','',line.strip())
            cells = re.split(r'\s{2,}', rest)
            if heading == 'EXHIBIT 35. Medicaid':
                cells = re.findall(r'\d+(?:–\d+)?%?(?:;\s*\d+)?|–',rest)
            require(name not in out, 'duplicate primary state ' + name)
            out[name] = cells
    require(set(out) == set(codes), 'primary table state coverage ' + heading)
    return out


def numeric(x):
    x = re.sub(r'[^\d.\-]', '', str(x))
    return float(x) if x else 0.


def normalize_policy_pdf():
    """Remove superscript footnotes geometrically, retaining policy digits.

    Pages108/109 contain rotated landscape tables; normalize their content
    before filtering. Font-size filtering avoids turning 95+footnote3 into953.
    This regenerates the pinned parsed text, tested byte-for-byte.
    """
    import io
    import pdfplumber
    import pypdf
    source=pypdf.PdfReader(INPUTS/'health_macstats2024.pdf')
    writer=pypdf.PdfWriter()
    for index in [108,109,111,112]:
        writer.add_page(source.pages[index])
        page=writer.pages[-1]
        if index<110:
            page.rotate(90)
            page.transfer_rotation_to_content()
    stream=io.BytesIO();writer.write(stream);stream.seek(0)
    with pdfplumber.open(stream) as doc:
        return '\n'.join(page.filter(lambda o:o.get('object_type')!='char' or
                         (o.get('upright',True) and o.get('size',10)>=7)).extract_text(layout=True,y_tolerance=2)
                         for page in doc.pages)


def rules():
    verify()
    b = module(LANE / 'benefits.py', 'health_benefits')
    base = b.rules()
    codes = state_codes()
    old = (INPUTS / 'health_macstats2024.txt').read_text()
    new = (INPUTS / 'health_macstats2026.txt').read_text()
    policy = (INPUTS / 'health_policy2024.txt').read_text()
    child = primary_rows(policy, 'EXHIBIT 35. Medicaid', 'EXHIBIT 36. Medicaid', codes)
    adult = primary_rows(policy, 'EXHIBIT 36. Medicaid', 'END POLICY', codes)
    spend23 = primary_rows(old, 'EXHIBIT 16. Medicaid', 'EXHIBIT 17.', codes)
    spend24 = primary_rows(new, 'EXHIBIT 16. Medicaid', 'EXHIBIT 17.', codes)
    enrol = primary_rows(old, 'EXHIBIT 11. Full', 'EXHIBIT 12.', codes)
    thresholds, bridges = {}, {}
    for name, fips in codes.items():
        ch, ad = child[name], adult[name]
        require(len(ch) == 9 and len(ad) == 2, 'policy row column count ' + name)
        highest = lambda x: max([numeric(v) for v in x.replace('%', '').split('–')])
        # Remove trailing superscript footnotes by using the first digit run for
        # singleton cells; ranges retain their two policy endpoints.
        def limit(x):
            x = x.replace('%', '')
            if not re.search(r'\d',x):
                return 0.
            if '–' in x:
                return max(float(v) for v in re.findall(r'\d+', x))
            m = re.match(r'^(\d{1,3})(?:\D|$)', x)
            if m:
                return float(m[1])
            m = re.match(r'^(\d{3})\d$', x)
            return float(m[1]) if m else 0.
        med = [max(limit(ch[i]), limit(ch[i + 1])) for i in (0, 2, 4)]
        chip = limit(ch[6])
        parent = limit(ad[0])
        ex = ad[1].split(' (')[0]
        additional = limit(ex) if re.match(r'^\d',ex) else 0.
        optional = re.search(r'age 19–20 only:\s*(\d+)',ad[1],re.I)
        # Georgia Pathways is a conditional work/activity demonstration, not
        # unrestricted ACA expansion; retain a separate eligibility upper arm.
        if name == 'Georgia':
            additional = 0.
        thresholds[fips] = dict(children=med, chip=chip, parent=parent, adult=additional,
                                optional_19_20=float(optional[1]) if optional else 0.,
                                raw_child=ch, raw_adult=ad)
        require(len(spend23[name]) == len(spend24[name]) == 9 and len(enrol[name]) == 9,
                'cost bridge table width ' + name)
        bridges[fips] = numeric(spend24[name][0]) / numeric(spend23[name][0]) * numeric(enrol[name][3]) / numeric(enrol[name][4])
    # Age-specific statewide exceptions are stated in the policy table notes.
    require('children up to age two' in old and 'infants (defined by the state as being under age two)' in old,
            'state infant exception notes changed')
    w = openpyxl.load_workbook(INPUTS / 'health_group2023.xlsx', data_only=True)
    sheet = w['Exhibit 22']
    require('FY 2023' in sheet.cell(1, 1).value and sheet.cell(3, 4).value == 'Child', 'group cost vintage/schema')
    costs = {}
    for row in sheet.values:
        name = re.sub(r'[\d,]+$', '', str(row[0]))
        if name in codes:
            # Full-benefit FYE Child / new adult / other adult. Different prices
            # distinguish child/CHIP proxy, expansion, and caretaker categories.
            costs[codes[name]] = np.array([numeric(row[4]), numeric(row[6]), numeric(row[8])])
    require(set(costs) == set(codes.values()), 'state/group spending coverage')
    # NC expanded in Dec2023; its FY2023 expansion cell is zero in exhibit22.
    # WI's additional adult route is not ACA expansion. Use the named state's
    # observed other-adult cost proxy explicitly, never zero-cost enrollment.
    cost_proxy_states = []
    for fips in codes.values():
        if thresholds[fips]['adult'] > 0 and costs[fips][1] == 0:
            costs[fips][1] = costs[fips][2]
            cost_proxy_states.append(fips)
    with zipfile.ZipFile(INPUTS / 'health_aca2024.zip') as z:
        aca = pd.read_csv(z.open('2024 OEP State-Level Public Use File.csv'))
    states = json.loads((INPUTS / 'health_state_abbreviations.json').read_text())
    premiums = {states[r.State_Abrvtn]: numeric(r.Avg_Prm) * 12 for r in aca.itertuples() if r.State_Abrvtn in states}
    require(set(premiums) == set(codes.values()), 'ACA premium state coverage')
    ptc = (INPUTS / 'benefit_ptc24.txt').read_text()
    require('For 2024, the 2023 federal poverty lines are used' in ptc, 'ACA poverty vintage')
    # IRS Table 2 is integer FPL percentage, including enhanced credits >400%.
    table = ptc.split('Table 2. Applicable Figure', 1)[1].split('Line 8a', 1)[0]
    figures = {int(i): float(v) for i, v in re.findall(r'\b(\d{3})\s+(0\.\d{4})', table)}
    figures[150], figures[400] = 0., .085
    require(all(i in figures for i in range(150, 401)), 'IRS enhanced applicable-figure table completeness')
    # IRS Table 1-1 through 1-3 lists poverty amounts for 2023, used by 2024 PTC.
    fpl23 = []
    for heading in ('Table 1-1.', 'Table 1-2.', 'Table 1-3.'):
        block = ptc.split(heading, 1)[1]
        vals = re.findall(r'\b([1-8])\s{10,}\$([\d,]+)', block, re.M)[:8]
        require(len(vals) == 8, 'IRS poverty table ' + heading)
        fpl23.append([numeric(v) for _, v in vals])
    # IRS order contiguous states, Alaska, Hawaii; arrange contiguous,HI,AK.
    fpl23 = np.asarray([fpl23[0], fpl23[2], fpl23[1]])
    unearned = re.search(r'than \$([\d,]+), you must enter',ptc)
    require(unearned is not None,'dependent unearned filing threshold')
    return dict(base=base, thresholds=thresholds, bridges=bridges, costs=costs,
                premiums=premiums, ptc_figures=figures, fpl23=fpl23,
                cost_proxy_states=cost_proxy_states,unearned_filing=numeric(unearned[1]))


def poverty(size, state, fpl):
    region = np.where(state == 2, 2, np.where(state == 15, 1, 0))
    return fpl[region, np.minimum(size, 8) - 1] + np.maximum(size - 8, 0) * (fpl[region, 1] - fpl[region, 0])


def households(d, removed, income, earned_filing=14600., unearned_filing=1300.):
    """435.603(f) household members, tax-family and nonfiler exceptions.

    A household is built separately for every person. Surviving dependents whose
    claimant departs move to a remaining resident parent; otherwise use nonfiler
    rules. We do not invent a tax claimant or infer a legal caretaker from SPM.
    """
    n = len(d)
    age = d.A_AGE.to_numpy(int)
    fs = d.FILESTAT.to_numpy(int)
    dep = d.DEP_STAT.to_numpy(int)
    alive = ~removed
    keys = {(int(h), int(p)): i for i, (h, p) in enumerate(zip(d.PH_SEQ, d.A_LINENO))}
    hh = d.PH_SEQ.to_numpy(int)
    refs = lambda arr: np.array([keys.get((hh[i], int(v)), -1) if v > 0 else -1 for i, v in enumerate(arr)])
    par = np.stack([refs(d.PEPAR1), refs(d.PEPAR2)], axis=1)
    spouse = refs(d.A_SPOUSE)
    claim = refs(dep)
    # Explicit claimant linked by DEP_STAT, not merely TAX_ID equality.
    children = [[] for _ in range(n)]
    for i, parents in enumerate(par):
        if age[i] < 19 and alive[i]:
            for p in set(parents) - {-1}:
                if alive[p]:
                    children[p].append(i)
    for i in np.flatnonzero(alive & (claim >= 0)):
        if not alive[claim[i]]:
            staying = [p for p in par[i] if p >= 0 and alive[p] and age[p] >= 19]
            claim[i] = staying[0] if staying else -1
    taxfam = {}
    for i in np.flatnonzero(alive):
        if fs[i] <= 5 and dep[i] == 0:
            family = {i}
            s = spouse[i]
            if fs[i] in (1, 2, 3) and s >= 0 and alive[s]:
                family.add(s)
            taxfam[i] = family
    for i in np.flatnonzero(alive & (claim >= 0)):
        h = claim[i]
        # Treat the surviving parent as a new filer only when the documented
        # dependent link needs reconstruction. This is a stated counterfactual.
        if h not in taxfam:
            taxfam[h] = {h}
        taxfam[h].add(i)
    for h, f in list(taxfam.items()):
        s = spouse[h]
        if s in f:
            taxfam[h] = f | taxfam.get(s, set())
            taxfam[s] = taxfam[h]
    required = ((d.WSAL_VAL + d.SEMP_VAL + d.FRSE_VAL).to_numpy() > earned_filing) | ((d.INT_VAL + d.DIV_VAL + d.RNT_VAL + d.CAP_VAL + d.UC_VAL + d.PNSN_VAL + d.ANN_VAL).to_numpy() > unearned_filing)
    size, magi = np.ones(n, int), np.zeros(n)
    parent = np.array([bool(x) for x in children])
    exceptions = np.zeros(n, bool)
    roster, tax_roster = [], []
    tax_size,tax_magi=np.ones(n,int),np.zeros(n)
    for i in range(n):
        if not alive[i]:
            roster.append(())
            tax_roster.append(())
            continue
        c = claim[i]
        parents = {p for p in par[i] if p >= 0 and alive[p]}
        # Under 19: non-parent claimant; two resident parents not jointly filing;
        # noncustodial claimant (absent here -> no tax-family lookup).
        dependent = dep[i] > 0
        exceptional = dependent and (c < 0 or (c not in parents and c != spouse[i]))
        if dependent and age[i] < 19 and len(parents) == 2:
            pa, pb = tuple(parents)
            exceptional |= not (spouse[pa] == pb and fs[pa] in (1, 2, 3))
        exceptions[i] = exceptional
        if dependent and not exceptional and c in taxfam:
            members = set(taxfam[c])
            # f(2) adopts the CLAIMANT'S Medicaid household, including f(4)'s
            # resident spouse even when the claimant filed a separate return.
            claimant_spouse = spouse[c]
            if claimant_spouse >= 0 and alive[claimant_spouse]:
                members.add(claimant_spouse)
        elif not dependent and i in taxfam:
            members = set(taxfam[i])
        else:
            members = {i} | set(children[i])
            s = spouse[i]
            if s >= 0 and alive[s]:
                members.add(s)
            if age[i] < 19:
                members |= parents
                for p in parents:
                    members |= set(children[p])
        members = {j for j in members if alive[j]}
        # 435.603(f)(4): co-resident married spouses belong to each other's
        # Medicaid household even with separate returns. Do not change taxfam:
        # ACA retains its joint-tax-family rule.
        s = spouse[i]
        if s >= 0 and alive[s]:
            members.add(s)
        require(i in members, 'household excludes applicant')
        size[i] = len(members)
        # 435.603(d)(2)(i) excludes a nonrequired person's income in their
        # natural/adoptive/step parent's household, at ANY age. Paragraph
        # (d)(2)(ii) also excludes nonrequired f(2)(i) non-parent tax dependents
        # in their taxpayer's household. A ward's own nonfiler household without
        # a parent/claimant still counts that ward's own income.
        def income_excluded(j):
            in_parent_household = any(p >= 0 and p in members for p in par[j])
            nonparent_claim = (dep[j] > 0 and claim[j] >= 0 and
                               claim[j] not in par[j] and claim[j] != spouse[j])
            in_nonparent_taxpayer_household = nonparent_claim and claim[j] in members
            return not required[j] and (in_parent_household or in_nonparent_taxpayer_household)
        count = [j for j in members if not income_excluded(j)]
        magi[i] = max(sum(income[j] for j in count), 0.)
        roster.append(tuple(sorted(members)))
        tf = taxfam.get(c if dependent and c>=0 else i,{i})
        tax_roster.append(tuple(sorted(tf)))
        tax_size[i]=len(tf)
        # 36B household income excludes nonrequired tax dependents of every age;
        # if their claimant departed with no replacement, they are no longer
        # claimed in this counterfactual and their own income is included.
        tax_magi[i]=max(sum(income[j] for j in tf if required[j] or claim[j]<0),0.)
    return dict(size=size, magi=magi, parent=parent, exception=exceptions, roster=roster,
                tax_roster=tax_roster,tax_size=tax_size,tax_magi=tax_magi)


def eligibility(d, family, rule, policy='july24'):
    age, state = d.A_AGE.to_numpy(int), d.GESTFIPS.to_numpy(int)
    vals = rule['thresholds']
    med = np.array([vals[s]['children'][0 if a < 1 else 1 if a < 6 else 2] for s, a in zip(state, age)])
    chip = np.array([vals[s]['chip'] if not(s in (10,12,19,55) and a < 1) else 0. for s,a in zip(state,age)])
    # Statewide age<2 provisions; county-only California exception stays outside.
    for name,note in rule['base']['statewide_infant_notes'].items():
        mask=(state==note['state']) & (age<note['age_limit'])
        if name=='California':chip[mask]=np.maximum(chip[mask],note['threshold'])
        else:med[mask]=np.maximum(med[mask],note['threshold'])
    par = np.array([vals[s]['parent'] for s in state])
    adult = np.array([vals[s]['adult'] for s in state])
    adult_base=adult.copy()
    optional=np.array([vals[s]['optional_19_20'] for s in state])
    adult=np.maximum(adult,np.where((age>=19)&(age<=20),optional,0))
    if policy == 'dec23':
        v = np.stack([rule['base']['medicaid'][int(s)] for s in state])
        med = v[np.arange(len(d)), np.where(age < 1, 0, np.where(age < 6, 1, 2))]
        chip = v[:, 3]
        par, adult = v[:, 6], v[:, 7]
    threshold = np.where(age < 19, np.maximum(med, chip), np.maximum(adult, np.where(family['parent'], par, 0)))
    fpl = poverty(family['size'], state, rule['base']['fpl'])
    ratio = family['magi'] / fpl
    e = (threshold > 0) & (ratio <= (threshold + rule['base']['magi_disregard']) / 100.)
    # Child category vs expansion vs caretaker (expansion only above parent limit).
    group = np.where(age < 19, 0, np.where((adult_base >= 133) & (ratio <= (adult_base+5)/100) & ((~family['parent']) | (ratio > (par + 5) / 100)), 1, 2))
    chip_only = (age < 19) & (chip > med) & (ratio > (med + 5) / 100) & e
    return e, group, ratio, chip_only


def rates(d, W, eligible, group, ratio, coverage, supported):
    """State x category x income cells; weighted CPS observed coverage.

    Wilson uncertainty uses Kish effective N, with rates recomputed under each
    SDR weight. Empty cells have explicit [0,1] bounds; no substituted cells.
    """
    state = d.GESTFIPS.to_numpy(int)
    band = np.digitize(ratio, [.5, 1., 1.38, 2., 4.])
    ids = state * 100 + group * 10 + band
    bounds, meta = {}, []
    for cell in np.unique(ids):
        donor = (ids == cell) & eligible & supported
        wc = W[donor]
        if not len(wc):
            bounds[int(cell)] = (np.zeros(161), np.ones(161))
            meta.append(dict(cell=int(cell), sample=0, lower=0., upper=1.))
            continue
        den = wc.sum(axis=0)
        num = wc[coverage[donor]].sum(axis=0)
        p = np.divide(num, den, out=np.zeros(161), where=den > 0)
        p = np.clip(p, 0, 1)
        neff = float(den[0] ** 2 / np.square(wc[:, 0]).sum())
        z2 = 1.96 ** 2
        center = (p + z2 / (2 * neff)) / (1 + z2 / neff)
        radius = 1.96 * np.sqrt(p * (1 - p) / neff + z2 / (4 * neff ** 2)) / (1 + z2 / neff)
        low, high = np.maximum(center - radius, 0), np.minimum(center + radius, 1)
        low[den <= 0], high[den <= 0] = 0., 1.
        bounds[int(cell)] = low, high
        meta.append(dict(cell=int(cell), sample=int(donor.sum()), effective_n=neff,
                         observed=float(p[0]), lower=float(low[0]), upper=float(high[0])))
    return ids, bounds, meta


def attribute(person_change, d, W, union, gen):
    """Survivor event assigned to removed members' original SPM weight shares.

    The event is a person-priced benefit, not a shared unit amount. No division
    by unweighted unit size occurs. Sum of generations conserves each replicate.
    """
    unit, labels = pd.factorize(d.SPM_ID, sort=False)
    out = np.zeros((3, 161))
    for r in range(161):
        wm = np.bincount(unit, weights=W[:, r] * union, minlength=len(labels))
        events = np.bincount(unit, weights=person_change[:, r] * W[:, r], minlength=len(labels)) / 1e9
        require(np.all(wm[events != 0] != 0), 'event with no removed-member replicate mass')
        for g in range(3):
            wg = np.bincount(unit, weights=W[:, r] * (gen == g), minlength=len(labels))
            out[g, r] = (events * np.divide(wg, wm, out=np.zeros_like(wg), where=wm != 0)).sum()
        require(abs(out[:, r].sum() - events.sum()) < 1e-9, 'generation/weighted event conservation')
    return out


def ptc_amount(income, fpl, annual_premium, eligible, figures):
    percent = np.floor(income / fpl * 100).astype(int)
    factor = np.array([0. if p <= 150 else .085 if p >= 400 else figures[p] for p in percent])
    # Enhanced 2024 schedule has NO 400% upper cliff.
    return np.where(eligible & (percent >= 100), np.maximum(annual_premium - income * factor, 0), 0)


def ptc_family_amount(income,fpl,premium_per_person,coverage_count,figures):
    """IRS8962 coverage family excludes EACH MEC-eligible person, not filer unit.

    A Medicaid-eligible filer can claim PTC for another non-MEC relative.
    Premium and credit belong to the eligible coverage family; contribution
    uses the whole tax family's required-filing MAGI.
    """
    return ptc_amount(income,fpl,premium_per_person*coverage_count,
                      (income>=fpl)&(coverage_count>0),figures)


def tax_family_takeup(d,family,supported):
    """Observed coverage of ANY relative; one original carrier per tax family."""
    market=d.NOW_MRK.eq(1).to_numpy()
    subs=d.NOW_MRKS.eq(1).to_numpy()
    any_market=np.array([any(market[j] for j in members) for members in family['tax_roster']])
    any_subs=np.array([any(subs[j] for j in members) for members in family['tax_roster']])
    taxcols=[v for v in ['AGI','FEDTAX_BC','FEDTAX_AC','CTC_CRD','ACTC_CRD','EIT_CRED'] if v in d]
    carriers=d[taxcols].ne(0).any(axis=1).to_numpy() if taxcols else np.zeros(len(d),bool)
    candidates={}
    for i in np.flatnonzero(supported):
        candidates.setdefault(family['tax_roster'][i],[]).append(i)
    donor=np.zeros(len(d),bool)
    for rows in candidates.values():
        carrier=next((i for i in rows if carriers[i]),rows[0])
        donor[carrier]=True
    require(int(donor.sum())==len(candidates),'ACA donor taxfamily counted twice')
    return any_market,any_subs,donor


def compute(d, W, union, gen, ctx=None):
    ctx = ctx or {}
    rule = rules()
    needed = ['A_SPOUSE', 'DEP_STAT', 'FILESTAT', 'PH_SEQ', 'A_LINENO', 'PEPAR1', 'PEPAR2',
              'A_AGE', 'GESTFIPS', 'SPM_ID', 'PRDISFLG', 'SSI_VAL', 'SS_VAL', 'NOW_MCAID', 'NOW_PUB', 'NOW_MCARE', 'NOW_PRIV','NOW_MRK','NOW_MRKS']
    require(set(needed) <= set(d), 'missing columns ' + str(sorted(set(needed) - set(d))))
    W = np.asarray(W, float)
    union, gen = np.asarray(union, bool), np.asarray(gen, int)
    require(W.shape == (len(d), 161) and np.isfinite(W).all() and (W[:, 0] > 0).all(), 'weight shape/value')
    require(np.array_equal(union, gen >= 0), 'generation membership mismatch')
    civ = np.asarray(ctx.get('civ', d.PRPERTYP.ne(3).to_numpy()), bool)
    c = module(LANE.parent / 'mixed_unit_credits_2026_10_14/credits.py', 'health_credits')
    departure=np.asarray(ctx.get('removal_mask',union),bool)
    require((union<=departure).all(),'departure must include identified union')
    income = c.person_income(d)['agi_parts'] + d.SS_VAL.to_numpy(float)
    before = households(d, np.zeros(len(d), bool), income,c.STD['single'],rule['unearned_filing'])
    after = households(d, departure, income,c.STD['single'],rule['unearned_filing'])
    age = d.A_AGE.to_numpy(int)
    unit = pd.factorize(d.SPM_ID, sort=False)[0]
    mixed = (np.bincount(unit, weights=union)[unit] > 0) & (np.bincount(unit, weights=~union)[unit] > 0)
    supported = civ & (age < 65) & d.PRDISFLG.ne(1).to_numpy() & d.SSI_VAL.le(0).to_numpy()
    survivor = supported & ~departure & mixed
    covered = d.NOW_MCAID.eq(1).to_numpy()
    public = d.NOW_PUB.eq(1).to_numpy() & ~d.NOW_MCARE.eq(1).to_numpy()
    terms, diagnostics, takeup, unobserved = {}, {}, {}, {}
    state = d.GESTFIPS.to_numpy(int)
    for policy in ('july24', 'dec23'):
        e0, group0, r0, chip0 = eligibility(d, before, rule, policy)
        e1, group1, r1, chip1 = eligibility(d, after, rule, policy)
        gain = survivor & ~e0 & e1
        loss = survivor & e0 & ~e1
        ids0, bd0, cells0 = rates(d, W, e0, group0, r0, covered, supported)
        ids1, bd1, cells1 = rates(d, W, e0, group0, r0, public | covered, supported)
        # For gains use destination state/category/FPL donor cell in the original
        # population. For losses use source cell. Medicaid low and public high
        # distinguish observed Medicaid from broader coverage coding uncertainty.
        target = state * 100 + group1 * 10 + np.digitize(r1, [.5, 1., 1.38, 2., 4.])
        unobserved[policy]=[dict(cell=int(cell),persons=float(W[gain & (target==cell),0].sum()),
                                sample=int(next((v['sample'] for v in cells0 if v['cell']==int(cell)),0)),
                                bounds=[0.,1.]) for cell in np.unique(target[gain]) if int(cell) not in bd0 or next(v['sample'] for v in cells0 if v['cell']==int(cell))==0]
        prices0 = np.array([rule['costs'][s][g] for s, g in zip(state, group0)])
        prices1 = np.array([rule['costs'][s][g] for s, g in zip(state, group1)])
        bridges = np.array([rule['bridges'][s] for s in state])
        low_change, high_change = np.zeros_like(W), np.zeros_like(W)
        for i in np.flatnonzero(gain | loss):
            if gain[i]:
                lo = bd0.get(int(target[i]), (np.zeros(161), np.ones(161)))[0]
                hi = bd1.get(int(target[i]), (np.zeros(161), np.ones(161)))[1]
                # Already-reported public enrollment yields no new enrollment.
                if covered[i]:
                    lo = hi = np.zeros(161)
                low_change[i] = -prices1[i] * max(1., bridges[i]) * hi
                high_change[i] = -prices1[i] * min(1., bridges[i]) * lo
            else:
                lo, hi = bd0[int(ids0[i])][0], bd1[int(ids1[i])][1]
                low_change[i] = prices0[i] * min(1., bridges[i]) * lo
                high_change[i] = prices0[i] * max(1., bridges[i]) * hi
        terms[f'Medicaid_{policy}_low'] = attribute(low_change, d, W, union, gen)
        terms[f'Medicaid_{policy}_high'] = attribute(high_change, d, W, union, gen)
        diagnostic = {}
        for label, mask in [('newly_eligible', gain), ('newly_ineligible', loss),
                            ('newly_eligible_child', gain & (age < 19)), ('newly_ineligible_child', loss & (age < 19)),
                            ('newly_eligible_expansion_adult', gain & (group1 == 1)),
                            ('newly_eligible_caretaker', gain & (group1 == 2)),
                            ('newly_eligible_already_covered', gain & covered),
                            ('newly_ineligible_reported_covered', loss & covered),
                            ('newly_eligible_chip_only', gain & chip1)]:
            v = W[mask].sum(axis=0)
            diagnostic[label] = dict(persons=float(v[0]), se_persons=float(sdr(v)))
        for direction, mask in [('gained',gain),('lost',loss)]:
            diagnostic[direction+'_by_state']={str(s):float(W[mask & (state==s),0].sum()) for s in np.unique(state[mask])}
            for end,change_array in [('low',low_change),('high',high_change)]:
                value=(change_array[mask]*W[mask]).sum(axis=0)/1e9
                diagnostic[direction+'_'+end+'_spending_delta']=dict(bn=float(value[0]),se_bn=float(sdr(value)))
                prices=prices1 if direction=='gained' else prices0
                # Enrollment transition inferred by this arm, not actual observed.
                upper_cost=(direction=='gained' and end=='low') or (direction=='lost' and end=='high')
                costfactor=np.maximum(1.,bridges[mask]) if upper_cost else np.minimum(1.,bridges[mask])
                enrollment=np.divide(np.abs(change_array[mask]),(prices[mask]*costfactor)[:,None],out=np.zeros_like(change_array[mask]),where=prices[mask,None]>0)
                v=(enrollment*W[mask]).sum(axis=0)
                diagnostic[direction+'_'+end+'_enrollment_arm']=dict(persons=float(v[0]),se_persons=float(sdr(v)))
        diagnostics[policy] = diagnostic
        takeup[policy] = dict(Medicaid=cells0, public=cells1)
        if policy == 'july24':
            central_e0, central_e1, central_r0, central_r1, central_g0, central_g1 = e0, e1, r0, r1, group0, group1
    # ACA uses TAX families, which differ from Medicaid's dependent exceptions.
    # Reconstruct with exceptions suppressed through a separate tax-family map
    # derived from actual claimant links. Here family MAGI/size are statutory
    # Medicaid tax-rule household for tax filers; exceptions/nonfilers excluded.
    tax_supported = supported & d.FILESTAT.le(5).to_numpy() & d.DEP_STAT.eq(0).to_numpy()
    aca_surv = survivor & tax_supported
    # ESI is not identified by NOW_PRIV alone. Low arm holds private-enrolled
    # survivors' coverage fixed; high arm permits new Marketplace enrollment.
    annual_prem = np.array([rule['premiums'][s] for s in state])
    fpl0 = poverty(before['tax_size'], state, rule['fpl23'])
    fpl1 = poverty(after['tax_size'], state, rule['fpl23'])
    # PTC coverage family excludes Medicaid/CHIP-eligible relatives: count its
    # survivor and original members separately, never multiply by whole SPM size.
    cov0 = np.array([sum(supported[j] and not central_e0[j] for j in fam) for fam in before['tax_roster']])
    cov1 = np.array([sum(supported[j] and not central_e1[j] for j in fam) for fam in after['tax_roster']])
    ep0,ep1=(before['tax_magi']>=fpl0)&(cov0>0),(after['tax_magi']>=fpl1)&(cov1>0)
    # A surviving filing unit's original premium excludes removed people, since
    # their PTC is already in the member account. Household required contribution
    # is apportioned by remaining coverage-family persons before removal.
    noncov0 = np.array([sum(supported[j] and not central_e0[j] and not departure[j] for j in fam) for fam in before['tax_roster']])
    q0 = ptc_family_amount(before['tax_magi'],fpl0,annual_prem,cov0,rule['ptc_figures']) * np.divide(noncov0,cov0,out=np.zeros(len(d),float),where=cov0>0)
    q1 = ptc_family_amount(after['tax_magi'],fpl1,annual_prem,cov1,rule['ptc_figures'])
    # One representative per original filing household among staying filers.
    representative = np.zeros(len(d), bool)
    seen = set()
    for i in np.flatnonzero(aca_surv):
        token = before['tax_roster'][i]
        if token not in seen:
            seen.add(token)
            representative[i] = True
    # Person-weight event anchor is mean survivor filer weight, never borrowed
    # from departed filer. Source row actual w, preserved across replicates.
    marketplace,subsidized,tax_donors=tax_family_takeup(d,before,tax_supported)
    aca_diagnostics = {}
    ids, bd, cells = rates(d, W, ep0, central_g0, before['tax_magi']/fpl0, subsidized, tax_donors)
    _,bd_upper,cells_upper=rates(d,W,ep0,central_g0,before['tax_magi']/fpl0,marketplace,tax_donors)
    for label,mask in [('observed_rate_donor_families',tax_donors & ep0),('observed_subsidized_donor_families',tax_donors & ep0 & subsidized),
                       ('observed_marketplace_donor_families',tax_donors & ep0 & marketplace)]:
        v=W[mask].sum(axis=0);aca_diagnostics[label]=dict(filing_units=float(v[0]),se_units=float(sdr(v)))
    change = q0-q1
    low, high = np.zeros_like(W),np.zeros_like(W)
    for i in np.flatnonzero(representative):
        lo,hi=bd[int(ids[i])][0],bd_upper[int(ids[i])][1]
        # Subsidized Marketplace and all Marketplace coverage provide observed
        # lower/high take-up cells. Form1095-A subsidy dollars remain unobserved.
        low[i] = min(change[i],0)*hi + max(change[i],0)*lo
        high[i] = min(change[i],0)*lo + max(change[i],0)*hi
    terms['ACA_low'], terms['ACA_high'] = attribute(low,d,W,union,gen),attribute(high,d,W,union,gen)
    for direction,mask in [('spending_increases',representative & (change<0)),('spending_decreases',representative & (change>0))]:
        for end,arr in [('low',low),('high',high)]:
            v=(arr[mask]*W[mask]).sum(axis=0)/1e9
            aca_diagnostics[direction+'_'+end]=dict(bn=float(v[0]),se_bn=float(sdr(v)))
    for label,mask in [('newly_income_eligible',representative & ~ep0 & ep1),('newly_income_ineligible',representative & ep0 & ~ep1),
                       ('crossing_100_fpl',representative & ((before['tax_magi']>=fpl0)!=(after['tax_magi']>=fpl1))),
                       ('crossing_400_fpl',representative & ((before['tax_magi']>4*fpl0)!=(after['tax_magi']>4*fpl1)))]:
        v=W[mask].sum(axis=0);aca_diagnostics[label]=dict(filing_units=float(v[0]),se_units=float(sdr(v)))
    summaries = {k:dict(bn=float(v[:,0].sum()),se_bn=float(sdr(v.sum(axis=0))),
                        by_generation_bn={g:float(v[i,0]) for i,g in enumerate(GENS)},
                        by_generation_se_bn={g:float(sdr(v[i])) for i,g in enumerate(GENS)}) for k,v in terms.items()}
    rough_comparison={}
    masks=[('statutory_MAGI_uniform138',central_r0<=1.38,central_r1<=1.38)]
    if {'SPM_NUMPER','SPM_TOTVAL','PTOTVAL'}<=set(d):
        size=np.bincount(unit)
        remaining=np.bincount(unit,weights=~departure).astype(int)
        first=np.unique(unit,return_index=True)[1]
        inc0=d.SPM_TOTVAL.to_numpy(float)[first]
        inc1=inc0-np.bincount(unit,weights=d.PTOTVAL.to_numpy(float)*departure)
        region_state=d.GESTFIPS.to_numpy(int)[first]
        f0=poverty(size,region_state,rule['base']['fpl'])
        f1=poverty(np.maximum(remaining,1),region_state,rule['base']['fpl'])
        masks.append(('SPM_income_uniform138',inc0[unit]<=1.38*f0[unit],inc1[unit]<=1.38*f1[unit]))
    for label,e0,e1 in masks:
        rough_comparison[label]={}
        for direction,mask in [('newly_eligible',survivor&~e0&e1),('newly_ineligible',survivor&e0&~e1),
                                ('newly_eligible_children',survivor&~e0&e1&(age<19))]:
            v=W[mask].sum(axis=0)
            rough_comparison[label][direction]=dict(persons=float(v[0]),se_persons=float(sdr(v)))
    details = dict(adoptable=False,recommended='arm',status='[DEGRADED] rule-based bounded health arm; 2023 state/group costs bridged to 2024',
                   summaries=summaries,Medicaid=diagnostics,takeup_cells=takeup,unobserved_destination_cells=unobserved,ACA=aca_diagnostics,
                   rough_probe_comparison=rough_comparison,
                   aca_takeup_cells=dict(subsidized=cells,marketplace=cells_upper),source_pins=verify(),state_cost_bridges={str(k):v for k,v in rule['bridges'].items()},cost_proxy_states=rule['cost_proxy_states'],
                   survivors_supported=float(W[survivor,0].sum()),survivors_nonmagi=float(W[~union & mixed & ~supported & civ,0].sum()),
                   statutory_household_exception_persons=float(W[survivor & before['exception'],0].sum()),
                   assumptions=['2024 July eligibility snapshot; Dec2023 beside as policy-vintage arm; Georgia Pathways activity conditions excluded',
                                '435.603(f) filer/dependent/nonfiler household; departing claimant transfers only to resident staying parent; annual personal MAGI held',
                                'SSI/public assistance excluded; full SS included; nonrequired income excluded in natural/adoptive/step-parent household at anyage and nonparent taxpayer household; own nonparent/nonfiler income counts; resident marriedspouse in Medicaid regardlessfiling; ACA jointtaxfamily separate; absent foreign income/tax-exempt interest unmeasured',
                                'MAGI under65 nondisabled only; pregnancy, lawful status, five-year bar, optional19/20 routes, 12-month child continuous eligibility not simulated',
                                'Observed state/category/FPL-cell NOW_MCAID low and NOW_PUB excluding Medicare high, Wilson bounds; empty cells explicit0–1',
                                'FY2023 full-benefit FYE CMS/T-MSIS costs from MACPAC exhibit22; bridges2024 state benefits-spending ratio divided by July enrollment ratio; cost endpoint includes unbridged level',
                                'CHIP-only children priced at state Medicaid-child cost proxy, not measured CHIP cost',
                                'ACA2024 enhanced schedule parsed IRS8962 using2023 FPL; no400% cliff; CMS2024 average plan premium per member is conditional SLCSP proxy',
                                'ACA any-family-member NOW_MRKS subsidized Marketplace low/NOW_MRK all Marketplace high Wilson cells; each donor taxfamily counted once at original carrier weight; survivor events use survivingfiler weight; actual Form1095-A/employer-affordability unobserved; nonfiler ACA units excluded',
                                'SPM only allocates person-priced changes across removed members; all161 weighted totals close; no added-lineage extrapolation'])
    return dict(terms=terms,details=details,Medicaid_low=terms['Medicaid_july24_low'],Medicaid_high=terms['Medicaid_july24_high'],
                ACA_low=terms['ACA_low'],ACA_high=terms['ACA_high'])


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,default=LANE/'derived/health_results.json')
    parser.add_argument('--arrays-out',type=Path,default=LANE/'derived/health_arrays.npz')
    parser.add_argument('--membership',choices=['union','latent'],default='union')
    args=parser.parse_args();start=time.perf_counter()
    c=module(LANE.parent/'mixed_unit_credits_2026_10_14/credits.py','health_standalone_credits')
    d=c.load();civ,union,gen=c.groups(d);W,_,_=c.row4_weights(d,civ,union)
    d=d.drop(columns=c.REPS[1:])
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        cols=pd.read_csv(z.open('pppub25.csv'),nrows=0).columns
        fields=[x for x in EXTRA if x in cols and x not in d]
        extra=pd.read_csv(z.open('pppub25.csv'),usecols=['PH_SEQ','PPPOS']+fields)
    d=d.merge(extra,on=['PH_SEQ','PPPOS'],validate='one_to_one')
    ctx=dict(civ=civ)
    if args.membership=='latent':
        membership=module(LANE/'membership.py','health_membership')
        ctx['removal_mask']=union|membership.latent_mask(d,union,civ)
    result=compute(d,W,union,gen,ctx)
    args.out.parent.mkdir(parents=True,exist_ok=True)
    args.out.write_text(json.dumps(result['details'],indent=2,sort_keys=True)+'\n')
    np.savez_compressed(args.arrays_out,**result['terms'],Medicaid_low=result['Medicaid_low'],Medicaid_high=result['Medicaid_high'])
    print(json.dumps(result['details']['summaries'],indent=2))
    print(json.dumps(dict(elapsed_seconds=time.perf_counter()-start,max_rss_gb=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/(1e9 if sys.platform=='darwin' else 1e6))))


if __name__=='__main__':
    main()
