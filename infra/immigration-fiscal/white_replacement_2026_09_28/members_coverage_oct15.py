"""Round 3 comparator fixes 1 and 2 on the rough engine: Census coverage and members' biological children (oct15).

Fix 1, coverage. Every person in a comparator scenario takes the 2020 PES net coverage error of their own group, by
April-2020 age and sex, under the lineage's rule (`coverage_bound_2026_10_14`, `coverage_bound.factors`, reused
unchanged): zero for later births and 2020+ arrivals, the under-5 undercount absorbed by the blended base (the DA
residual) in the central, true count = census / (1 + NCE), relative to the CPS controls through q = base / census.
Groups: Hispanic (the lineage's own rates and q), non-Hispanic white alone, Black alone or in combination (Table C's
universe, the closest the report offers to non-Hispanic Black alone), and other non-Hispanic people (a rate derived
from the national total and the Hispanic rate). The estimates base takes race within non-Hispanic people from the
2010-based Vintage 2020 estimates, never from the 2020 census (`methods-statement-v2024.pdf`), so a race-specific
base / census ratio mixes the 2020 race-coding change into q (white 1.03-1.09, Black 1.03-1.10); every non-Hispanic
group takes the non-Hispanic q instead [ASSUMPTION: within non-Hispanic people of one age band and sex, the base
carries each race's census coverage in proportion]. The DA arm reads DA / base directly (Black alone: DA Table 1A,
all ages; non-Hispanic: Table 1C, ages 0-29). Missed people add no custody or arrests (administrative counts; the
lineage's constructed-person rule excludes its custody-driven justice use).

Fix 2, children. Members' biological minor children outside the group's definition (the source's own-parent rule,
`mixed_unit_removal_2026_10_14/membership.py:biological_children`) depart with them and count as members at their
own costs: CPS records keyed like the group's, MEPS external keys from the children's own race and five-year age
cells. The lineage's own children outside its definition and outside the added-descendant universe (the latent
subset) form a separate block at their own costs, so the comparison counts one rule for all three groups.

Terms are measured on the central comparator arm's settings (combined_rules_only: own-group mortality) and on the same
rules at whole-population mortality (combined_rules_general), and travel after the evaluator, as item 11 does;
symmetric_comparators_oct14.py builds its derived arms from them. Run from the repo root: uv run --no-project python3 <this>
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import time
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import openpyxl
import pandas as pd
from pypdf import PdfReader

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(HERE.parents[0] / 'scripts'))
import symmetric_comparators_oct14 as SYM  # noqa: E402
from memory_budget import require_within_budget  # noqa: E402

W = SYM.W
R = W.R
COV = W.FISCAL / 'coverage_bound_2026_10_14'
sys.path.insert(0, str(COV))
import coverage_bound as CB  # noqa: E402
import source_tables as ST  # noqa: E402

ROOT = HERE.parents[2]
INPUTS = HERE / 'inputs/coverage'
OUT = HERE / 'derived'
SOURCE_MEMBERSHIP = W.FISCAL / 'mixed_unit_removal_2026_10_14/membership.py'
MIXED = W.FISCAL / 'mixed_unit_comparators_2026_10_15/derived'
BANDS = [(0, 4), (5, 9), (10, 17), (18, 29), (30, 49), (50, 100)]
BLACK_CODES = {2, 6, 10, 11, 12, 16, 17, 18, 22, 23}     # PRDTRACE codes that include Black [SOURCE: ASEC 2025 dictionary]
RACE_GROUPS = ('hispanic', 'nh_white', 'black', 'nh_other')
GROUPS = {'A1_third_plus_nh_white': 'w3', 'nh_black_rough': 'blk'}
COVERAGE_ARMS = ('central', 'pes_only', 'da_middle', 'da_all_black')
MORTALITY = ('specific', 'general')     # combined_rules_only's group tables; combined_rules_general's whole population
FAILS: list[str] = []


def gate(label, ok, detail=''):
    print(f"  {'✓' if ok else '✗'} {label}{(' — ' + detail) if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def require(ok, why):
    if not ok:
        raise SystemExit('[BLOCKED] ' + why)


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_module(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# ------------------------------------------------------------------ inputs
def check_inputs():
    pins = json.loads((INPUTS / 'pins.json').read_text())
    for name, pin in pins.items():
        require(digest(INPUTS / name) == pin['sha256'], f'stale coverage input {name}')
    cov = json.loads((COV / 'inputs/pins.json').read_text())
    used = ['pes_cross.pdf', 'pes_national.pdf', 'da_hispanic.xlsx', 'controls/nc-est2024-alldata-r-file01.csv',
            'controls/dhc-p12h-us.json', 'controls/dhc-p12h-variables.json', 'controls/base_adjustments_sex.csv']
    for name in used:
        if name in cov:
            require(digest(COV / 'inputs' / name) == cov[name]['sha256'], f'stale coverage-lane input {name}')
    hashes = {str((INPUTS / n).relative_to(ROOT)): pins[n]['sha256'] for n in pins}
    hashes.update({str((COV / 'inputs' / n).relative_to(ROOT)): digest(COV / 'inputs' / n) for n in used})
    hashes[str(SOURCE_MEMBERSHIP.relative_to(ROOT))] = digest(SOURCE_MEMBERSHIP)
    hashes[str((COV / 'coverage_bound.py').relative_to(ROOT))] = digest(COV / 'coverage_bound.py')
    return hashes


def dhc_cells(path, variables, table):
    head, vals = json.loads(Path(path).read_text())
    row = dict(zip(head, vals))
    var = json.loads(Path(variables).read_text())['variables']
    cells = {}
    for name, value in row.items():
        if not (name.startswith(table + '_') and name.endswith('N')):
            continue
        parts = var[name]['label'].split('!!')
        if len(parts) != 4:
            continue
        sex = {'Male:': 1, 'Female:': 2}[parts[2]]
        label = parts[3]
        if label == 'Under 5 years':
            lo, hi = 0, 4
        elif label == '85 years and over':
            lo, hi = 85, 100
        else:
            nums = [int(x) for x in re.findall(r'\d+', label)]
            lo, hi = nums[0], nums[-1]
        cells[(lo, hi, sex)] = int(value)
    require(len(cells) == 46 and sum(cells.values()) == int(row[table + '_001N']), f'DHC {table} cells close')
    return cells


def band_sum(cells, band, sex):
    lo, hi = band
    require(all(not (s == sex and (l < lo <= h or l <= hi < h)) for (l, h, s) in cells), 'DHC cell straddles a band')
    return sum(v for (l, h, s), v in cells.items() if s == sex and l >= lo and h <= hi)


def national_total_rates():
    """PES national report Table 10: total household-population NCE by age and sex (2020 column)."""
    text = subprocess.run(['pdftotext', '-layout', str(COV / 'inputs/pes_national.pdf'), '-'], capture_output=True,
                          text=True, check=True).stdout.replace('–', '-')
    starts = {'0 to 4': '0 to 4 .', '5 to 9': '5 to 9 .', '10 to 17': '10 to 17 .',
              '18 to 29 males': '18-to-29 males', '18 to 29 females': '18-to-29 females',
              '30 to 49 males': '30-to-49 males', '30 to 49 females': '30-to-49 females',
              '50 and over males': '50-and-over males', '50 and over females': '50-and-over females'}
    out = {}
    for label, start in starts.items():
        hits = [re.findall(r'-?\d+\.\d+|\bN\b', line.replace('*', '')) for line in text.splitlines()
                if line.strip().startswith(start)]
        hits = [h for h in hits if len(h) == 8]
        require(len(hits) == 1, f'PES Table 10 row {label}: {len(hits)} matches')
        out[label] = {'nce_pct': float(hits[0][0]), 'se_pct': float(hits[0][1])}
    return out


def da_rows(path, sheet_first_age, n_ages, columns):
    """DA single-age rows by sex: {(age, sex): {series: persons}} for the named column triple offset."""
    rows = [[c for c in r if c is not None] for r in
            openpyxl.load_workbook(path, read_only=True, data_only=True).worksheets[0].iter_rows(values_only=True)]
    out = {}
    for sex, label in ((1, 'Male'), (2, 'Female')):
        marker = [i for i, r in enumerate(rows) if r and r[0] == label]
        require(len(marker) == 1, f'DA sex marker {label} in {path.name}')
        for i in range(n_ages):
            r = rows[marker[0] + 1 + i]
            age = 85 if r[0] == '85+' else int(r[0])
            require(age == sheet_first_age + i, f'DA age order {path.name}')
            out[(age, sex)] = {s: float(r[columns + k]) * 1000 for k, s in enumerate(('low', 'middle', 'high'))}
    return out


def coverage_tables():
    """Rates and base tables for the four groups, plus the inputs' audit rows."""
    rates_l, base_h = ST.load()        # the lineage's own Hispanic rates and base table, pins verified there
    reader = PdfReader(COV / 'inputs/pes_cross.pdf')
    rates = {'hispanic': rates_l['hispanic'], 'nh_white': rates_l['nonhispanic_white'],
             'black': ST.block(reader.pages[6], 'Black or African American')}
    total = national_total_rates()
    var = INPUTS / 'dhc-p12-variables.json'
    census = {'TOT': dhc_cells(INPUTS / 'dhc-p12-us.json', var, 'P12'),
              'H': dhc_cells(COV / 'inputs/controls/dhc-p12h-us.json', COV / 'inputs/controls/dhc-p12h-variables.json', 'P12H')}
    with (COV / 'inputs/controls/nc-est2024-alldata-r-file01.csv').open(newline='') as stream:
        rows = [r for r in csv.DictReader(stream) if r['YEAR'] == '2020' and r['MONTH'] == '4.2' and r['AGE'] != '999']
    require(len(rows) == 101, 'base single ages')
    base = {col: {(int(r['AGE']), s): int(r[f'{col}_{lab}']) for r in rows for s, lab in ((1, 'MALE'), (2, 'FEMALE'))}
            for col in ('TOT', 'H', 'NH', 'BA')}
    require(all(base['TOT'][k] == base['H'][k] + base['NH'][k] for k in base['TOT']), 'base TOT = H + NH')
    da_black = da_rows(INPUTS / 'da_black_alone.xlsx', 0, 86, 2)
    da_hnh = da_rows(COV / 'inputs/da_hispanic.xlsx', 0, 30, 5)    # columns 5-7: non-Hispanic low/middle/high
    nh_rates, tables, audit = {'all': {'nce_pct': float('nan'), 'se_pct': 0.0}}, {g: {} for g in ('nh', 'black')}, []
    for band in BANDS:
        for sex in (1, 2):
            label = CB.pes_label(band[0], sex)[0]
            b = {k: sum(base[k][(a, sex)] for a in range(band[0], band[1] + 1)) for k in base}
            c_tot, c_h = band_sum(census['TOT'], band, sex), band_sum(census['H'], band, sex)
            c_nh = c_tot - c_h
            n_t, n_h = total[label]['nce_pct'] / 100, rates['hispanic'][label]['nce_pct'] / 100
            true_nh = c_tot / (1 + n_t) - c_h / (1 + n_h)
            nce_nh = c_nh / true_nh - 1
            nh_rates[label] = {'nce_pct': 100 * nce_nh, 'se_pct': 0.0}
            q_nh = b['NH'] / c_nh
            hi_da = min(band[1], 85)
            nh_cell = {'base_over_census': q_nh, 'base': b['NH'], 'census': c_nh}
            bl_cell = {'base_over_census': q_nh, 'base': b['BA'], 'census': None}
            for series in ('low', 'middle', 'high'):
                da_b = sum(da_black[(a, sex)][series] for a in range(band[0], hi_da + 1))
                bl_cell['da_residual_factor_' + series] = da_b / b['BA'] - 1
                if band[1] <= 29:
                    da_n = sum(da_hnh[(a, sex)][series] for a in range(band[0], band[1] + 1))
                    nh_cell['da_residual_factor_' + series] = da_n / b['NH'] - 1
            tables['nh'][(*band, sex)], tables['black'][(*band, sex)] = nh_cell, bl_cell
            audit.append({'band': f'{band[0]}-{band[1]}', 'sex': sex, 'census_total': c_tot, 'census_hispanic': c_h,
                          'base_total': b['TOT'], 'base_hispanic': b['H'], 'base_nonhispanic': b['NH'],
                          'base_black_alone': b['BA'], 'q_nonhispanic': q_nh,
                          'q_hispanic': base_h[(*band, sex)]['base_over_census'],
                          'nce_total_pct': 100 * n_t, 'nce_hispanic_pct': 100 * n_h, 'nce_nonhispanic_derived_pct': 100 * nce_nh,
                          'nce_nh_white_pct': rates['nh_white'][label]['nce_pct'], 'nce_black_aoic_pct': rates['black'][label]['nce_pct'],
                          'da_black_over_base_middle': bl_cell['da_residual_factor_middle'],
                          'da_nonhispanic_over_base_middle': nh_cell.get('da_residual_factor_middle')})
    rates['nh_other'] = nh_rates
    base_tables = {'hispanic': base_h, 'nh_white': tables['nh'], 'black': tables['black'], 'nh_other': tables['nh']}
    return rates, base_tables, audit


# ------------------------------------------------------------------ the frame's extra fields
def frame_extra():
    with zipfile.ZipFile(R.ZIP) as z:
        x = pd.read_csv(z.open('pppub25.csv'), usecols=['PH_SEQ', 'PPPOS', 'A_AGE', 'A_SEX', 'PEINUSYR', 'A_LINENO',
                                                       'PEPAR1', 'PEPAR2', 'PEPAR1TYP', 'PEPAR2TYP'])
    require(len(x) == len(R.d) and np.array_equal(x.PH_SEQ.to_numpy(), R.d.PH_SEQ.to_numpy())
            and np.array_equal(x.A_AGE.to_numpy(), R.d.A_AGE.to_numpy()), 'CPS extra fields align with the rough frame')
    for k in ('PRCITSHP', 'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP', 'PEHSPNON', 'PRDTRACE'):
        x[k] = R.d[k].to_numpy()
    return x


def race_group(x):
    hisp = x.PEHSPNON.eq(1).to_numpy()
    race = x.PRDTRACE.to_numpy()
    return np.where(hisp, 'hispanic', np.where(race == 1, 'nh_white', np.where(np.isin(race, list(BLACK_CODES)), 'black', 'nh_other')))


def meps_frame():
    lay = R.lay
    with zipfile.ZipFile(R.MEPS) as z:
        name = [n for n in z.namelist() if n.lower().endswith('.dat')][0]
        vals = [(float(t[lay['SEX'][0]:sum(lay['SEX'])]), float(t[lay['AGELAST'][0]:sum(lay['AGELAST'])]))
                for t in (ln.decode('ascii') for ln in z.open(name))]
    sex = np.array([v[0] for v in vals])
    require(len(sex) == len(R.md) and np.array_equal(np.array([v[1] for v in vals]), R.md.AGELAST.to_numpy()), 'MEPS rows align')
    racethx = R.md.RACETHX.to_numpy()
    group = np.where(racethx == 1, 'hispanic', np.where(racethx == 2, 'nh_white', np.where(racethx == 3, 'black', 'nh_other')))
    return sex, group


# ------------------------------------------------------------------ coverage factors
def factors(x, rows, rates, tables, arm):
    """Per-record coverage factor f (true / controlled - 1) for the records in `rows`, by own group."""
    f = np.zeros(len(x))
    groups = race_group(x)
    for g in RACE_GROUPS:
        m = rows & (groups == g)
        if not m.any():
            continue
        mode, da_max = 'central', 29
        if arm == 'pes_only':
            mode = 'pes_only'
        elif arm == 'da_middle':
            mode = 'da_middle'
        elif arm == 'da_all_black' and g == 'black':
            mode, da_max = 'da_middle', 100
        data = {'age': x.A_AGE.to_numpy()[m], 'sex': x.A_SEX.to_numpy()[m],
                'generation': np.where(x.PRCITSHP.isin([4, 5]).to_numpy()[m], 0, 1),
                'arrival': x.PEINUSYR.to_numpy()[m], 'hispanic': np.ones(int(m.sum()), bool)}
        values, _ = CB.factors(data, {'hispanic': rates[g], 'nonhispanic_white': rates['nh_white']}, tables[g],
                               mode=mode, da_max_age=da_max)
        f[m] = values
    require(np.isfinite(f).all(), 'finite coverage factors')
    return f


# ------------------------------------------------------------------ scenarios
def published_meps(g, sc):
    """The MEPS weights R.scenario gave the published scenario (keyed does not store them)."""
    mmask = R.MMASK[g]
    if abs(sc['population'] - float(R.w[R.MASK[g]].sum())) < 1e-6:      # unscaled (Black at own count)
        return R.mw * mmask
    mfrac = (sc['population'] / R.CPS_TOTAL) * float(R.mw.sum())
    return R.mw * mmask * (mfrac / float(R.mw[mmask].sum()))


def build(g, sc0, members, kids, f, total, extra, msex, mgroup, hold=None, own_rule=False):
    """A scenario of members plus kids with coverage factors f, `total` persons, keyed like the group.

    sc0: the published scenario whose MEPS convention (scaled or own count) the new one keeps. hold: (custody,
    arrests) of the same membership uncovered at this total. Missed people add none: at an equal count the observed
    people are observed / true of the total; at the own count the held totals stand.
    """
    w = R.w
    mass = w * (members | kids) * (1 + f)
    observed = float((w * (members | kids)).sum())
    true = float(mass.sum())
    cw = mass * (total / true)
    mwt0 = published_meps(g, sc0)
    rho = float(mwt0.sum()) / float(sc0['cps_w'].sum())
    # members' MEPS: the published structure, each single-age/sex cell scaled by the members' mean CPS factor
    age = np.minimum(R.d.A_AGE.to_numpy(), 85)
    sex = extra.A_SEX.to_numpy()
    mage = np.minimum(np.maximum(R.md.AGELAST.to_numpy(), 0), 85).astype(int)
    fm = np.zeros(len(R.md))
    for a in range(86):
        for s in (1, 2):
            m = members & (age == a) & (sex == s) & (w > 0)
            if m.any():
                fm[(mage == a) & (msex == s)] = float((w[m] * f[m]).sum() / w[m].sum())
    mwt_m = mwt0 * (1 + fm)
    mwt_m = mwt_m * (rho * float(cw[members].sum()) / float(mwt_m.sum()))
    mwt = mwt_m
    if kids.any():
        kband = R.cage
        kgroup = race_group(extra)
        mband = R.band(np.maximum(R.md.AGELAST.to_numpy(), 0))
        mwt_k = np.zeros(len(R.md))
        for gk in RACE_GROUPS:
            for b in R.BANDS:
                k = kids & (kgroup == gk) & (kband == b)
                if not k.any() or cw[k].sum() <= 0:
                    continue
                cell = (mgroup == gk) & (mband == b)
                if not cell.any():
                    cell = mband == b
                    gate(f'MEPS cell {gk}/{b} empty: the age band any race stands in', True)
                mwt_k += R.mw * cell * (rho * float(cw[k].sum()) / float(R.mw[cell].sum()))
        mwt = mwt_m + mwt_k
    sc = R.keyed(g, cw, total, 'own', mwt)
    if hold is not None:
        # The Black lane's custody and arrest keys are fixed national shares; at the own count they stand.
        ratio = 1.0 if (own_rule or g == 'blk') else observed / true
        custody, arrests = hold
        sc['keys']['custody'], sc['keys']['arrests'] = custody * ratio, arrests * ratio
        ph = sc['share']['pc'] * R.pc_scale
        key = {'fire': ph, 'prisons': sc['keys']['custody'], 'law_courts': 0.6 * sc['keys']['arrests'] + 0.4 * ph,
               'police_cbp': ph, 'police_ice_border': ph, 'police_ice_interior': ph,
               'police_non_border': 0.5 * sc['keys']['arrests'] + 0.5 * ph}
        justice = float(sum(R.cj.loc[c, 'national_bn'] * v for c, v in key.items()) / R.cj.national_bn.sum())
        sc['keys']['justice'] = sc['external']['public_order_safety'] = justice
    for k in ('ages', 'scenario_name'):
        if k in sc0:
            sc[k] = sc0[k]
    return sc, observed, true


def children_targets(groups, kids, scs, extra, msex, mgroup):
    """The children-rule groups' own-count line targets for the mixed-unit survivor solve, built as the adapter's
    prepare() builds the current groups' (default evaluator settings; the per-person cost of the lineage-count
    scenario; lines from the natural unscaled MEPS universe), with the lineage's children block on the lineage side."""
    civ = R.civ.astype(bool)
    none = np.zeros(len(R.d), bool)
    block, block_base = scs['lineage_block', 'none'][0], scs['lineage_block_base', 'none'][0]
    out = {}
    for group, name in (('white_children', 'A1_third_plus_nh_white'), ('black_children', 'nh_black_rough')):
        g = GROUPS[name]
        members = R.MASK[g] & civ & (R.w > 0)
        own = float(R.w[members | kids[name]].sum())
        natural, _, _ = build(g, R.scenario(g, scaled=False), members, kids[name], np.zeros(len(R.d)), own, extra, msex, mgroup)
        published = scs[name, 'children', 'none'][0]
        entries = {}
        for method, basis in (('set', 'accrual'), ('cash', 'cash')):
            entries[method] = {}
            for end in W.ENDS:
                amount, rows, *_ = W.run29(natural, end, basis)
                pub = W.run29(published, end, basis)[0]
                blk = W.run29(block, end, basis)[0]
                blk = {'cost': blk['cost'] - W.run29(block_base, end, basis)[0]['cost'],
                       'population': scs['lineage_block', 'none'][2]}
                entries[method][end] = {
                    'population': own, 'members': float(R.w[members].sum()), 'children': float(R.w[kids[name]].sum()),
                    'cost_bn': pub['cost'] * own / pub['population'],
                    'natural_unscaled_universe_cost_bn': amount['cost'],
                    'published_comparator_cost_bn': pub['cost'], 'published_comparator_population': pub['population'],
                    'rough_lineage_cost_bn': W.run29(W.UNION_SC, end, basis)[0]['cost'] + blk['cost'],
                    'case_lineage_cost_bn': W.run29('eng', end, basis)[0]['cost'] + blk['cost'],
                    'lineage_population': W.R.TARGET + W.LINEAGE['counts']['added'] + blk['population'],
                    'lineage_children_block': {'cost_bn': blk['cost'], 'population': blk['population']},
                    'specification': W.DUMP[basis][end]['spec'],
                    'lines': {lid: {'side': side, 'national_bn': national, 'union_target_bn': target, 'response': response}
                              for side, lid, national, target, response in rows}}
        out[group] = entries
    return out


def main():
    started = time.perf_counter()
    hashes = check_inputs()
    rates, tables, audit = coverage_tables()
    mem = load_module(SOURCE_MEMBERSHIP, 'members_coverage_source_membership')
    extra = frame_extra()
    msex, mgroup = meps_frame()
    W.use_case('oct15')
    W.setup()
    groups = W.scenarios()
    production = SYM.Production(W)
    status = SYM.status_build(W)
    ratio_tables = {lane: SYM.read_verified_ratio_table(lane) for lane in (SYM.HERE, SYM.BLACK)}
    coupled = SYM.status_params(status, coupled=True)['union']
    accruals = {}
    for mortality in MORTALITY:
        accruals[mortality] = SYM.mortality_params(mortality, 'symmetric', payroll_basis='renormalized_status',
                                                   ratio_tables=ratio_tables)
        accruals[mortality]['union'] = coupled
    civ = R.civ.astype(bool)
    result = {'case': 'oct15', 'arm': 'combined_rules_only', 'source_hashes': hashes, 'base_audit': audit,
              'rates': {g: {k: v for k, v in rates[g].items() if k != 'all'} for g in rates},
              'controls': {}, 'counts': {}, 'missed_by_band': {}, 'runs': []}

    def run(sc):
        out = {}
        for mortality in MORTALITY:
            with W.patched(vars(W), ACC=accruals[mortality]):
                for basis in W.BASES:
                    for end in W.ENDS:
                        out[mortality, basis, end] = W.run29(sc, end, basis, production='own', production_model=production,
                                                             status_keys=status, status_rule='rules_only')[0]
        return out

    # positive control 1: the factor machinery reproduces the lineage's net missing people on its own records
    union = R.MASK['mex'] & civ
    hisp_flag = R.d.PRDTHSP.to_numpy() > 0
    data = {'age': extra.A_AGE.to_numpy()[union], 'sex': extra.A_SEX.to_numpy()[union],
            'generation': np.where(extra.PRCITSHP.isin([4, 5]).to_numpy()[union], 0, 1),
            'arrival': extra.PEINUSYR.to_numpy()[union], 'hispanic': hisp_flag[union]}
    fu, _ = CB.factors(data, {'hispanic': rates['hispanic'], 'nonhispanic_white': rates['nh_white']}, tables['hispanic'])
    missed_union = float((R.w[union] * fu).sum())
    # v8's union completion adds observed reporting records outside the rough mask (coverage_bound oct15 prices them)
    position = pd.Series(np.arange(len(extra)), index=pd.MultiIndex.from_frame(extra[['PH_SEQ', 'PPPOS']]))
    completion = [r for r in W.META['union_completion']['observed_records'] if r['central_reporter']]
    rows_c = position.reindex(pd.MultiIndex.from_tuples([(r['PH_SEQ'], r['PPPOS']) for r in completion])).to_numpy()
    require(np.isfinite(rows_c.astype(float)).all() and not union[rows_c.astype(int)].any(), 'completion records located outside the mask')
    rows_c = rows_c.astype(int)
    data_c = {'age': extra.A_AGE.to_numpy()[rows_c], 'sex': extra.A_SEX.to_numpy()[rows_c],
              'generation': np.where(extra.PRCITSHP.isin([4, 5]).to_numpy()[rows_c], 0, 1),
              'arrival': extra.PEINUSYR.to_numpy()[rows_c], 'hispanic': hisp_flag[rows_c]}
    fc, _ = CB.factors(data_c, {'hispanic': rates['hispanic'], 'nonhispanic_white': rates['nh_white']}, tables['hispanic'])
    missed_union += float((np.array([r['people'] for r in completion]) * fc).sum())
    cov = json.loads((COV / 'derived/coverage_bound_oct15.json').read_text())
    ref = sum(cov['sets']['set']['implied_net_missing_people'][k] for k in ('G1', 'G2', 'G3plus', 'added'))
    gate('lineage net missing people reproduced on the rough frame (100 persons)', abs(missed_union - ref) < 100,
         f'{missed_union:,.3f} vs coverage lane {ref:,.3f}')
    result['controls']['lineage_missing_people'] = {'rough_frame': missed_union, 'coverage_lane': ref}

    # children: members' biological minor children outside the group; the lineage's beyond its latent subset
    kids = {}
    for name, g in GROUPS.items():
        bio, step, _ = mem.biological_children(extra, R.MASK[g] & civ, civ)
        kids[name] = bio
    bio_l, _, _ = mem.biological_children(extra, union, civ)
    latent = mem.latent_mask(extra, union, civ)
    kids['lineage'] = bio_l & ~latent
    counts_mixed = {n: json.loads((MIXED / f'{grp}_summary.json').read_text())['counts']
                    for n, grp in (('A1_third_plus_nh_white', 'white'), ('nh_black_rough', 'black'))}
    for name in GROUPS:
        got = float(R.w[kids[name]].sum())
        want = counts_mixed[name]['biological_children_outside_group_stay']['weighted_persons']
        gate(f'{name}: children count is the mixed-unit lane\'s (1 person)', abs(got - want) < 1.0, f'{got:,.1f} vs {want:,.1f}')
    src = json.loads((W.FISCAL / 'mixed_unit_removal_2026_10_14/derived/membership.json').read_text())
    for label, got, want in (('biological', float(R.w[bio_l].sum()), src['extra_children']),
                             ('latent', float(R.w[latent].sum()), src['latent_children_with_two_US_parents'])):
        gate(f'lineage {label} children reproduce the source membership (100 persons)', abs(got - want) < 100,
             f'{got:,.1f} vs {want:,.1f}')
    result['counts']['lineage_source'] = {'extra_children': src['extra_children'],
                                          'latent_children_with_two_US_parents': src['latent_children_with_two_US_parents']}
    result['counts']['children'] = {n: float(R.w[k].sum()) for n, k in kids.items()}

    # The lineage's children block: natives under 18, keyed with the white rules. A children-only scenario has no
    # adults, and per-adult indices (v4_inputs licences) divide by zero, so the block is priced as the increment it
    # adds to A1 at its own count: its own lines at its own records, MEPS from its own race and age cells.
    scs = {}
    sc_w3 = groups['A1_third_plus_nh_white']
    a1 = R.MASK['w3'] & civ & (R.w > 0) & ~kids['lineage']    # 9k lineage children are also A1 members
    a1_own = float(R.w[a1].sum())
    zero = np.zeros(len(R.d))
    none = np.zeros(len(R.d), bool)
    scs['lineage_block_base', 'none'] = build('w3', sc_w3, a1, none, zero, a1_own, extra, msex, mgroup)
    for arm in ('none',) + COVERAGE_ARMS:
        f = zero if arm == 'none' else factors(extra, kids['lineage'], rates, tables, arm)
        total = a1_own + float((R.w * kids['lineage'] * (1 + f)).sum())
        hold = None if arm == 'none' else (scs['lineage_block', 'none'][0]['keys']['custody'],
                                           scs['lineage_block', 'none'][0]['keys']['arrests'])
        sc, obs, true = build('w3', sc_w3, a1, kids['lineage'], f, total, extra, msex, mgroup, hold=hold, own_rule=True)
        sc['scenario_name'] = 'lineage_children_block'
        scs['lineage_block', arm] = (sc, obs - a1_own, true - a1_own)

    # A1 and Black: published (positive control), coverage only, children only, children with coverage
    L = groups['A1_third_plus_nh_white']['population']
    for name, g in GROUPS.items():
        sc0 = groups[name]
        members = R.MASK[g] & civ & (R.w > 0)
        for rule in ('current', 'children'):
            k = kids[name] if rule == 'children' else np.zeros(len(R.d), bool)
            for arm in ('none',) + COVERAGE_ARMS:
                rows = members | k
                f = np.zeros(len(R.d)) if arm == 'none' else factors(extra, rows, rates, tables, arm)
                if g == 'w3':
                    lineage_add = 0.0 if rule == 'current' else scs['lineage_block', arm][2]
                    total = L + lineage_add
                else:
                    total = float((R.w * rows * (1 + f)).sum())
                hold = None
                if arm != 'none':
                    u = scs[name, rule, 'none'][0]
                    hold = (u['keys']['custody'], u['keys']['arrests'])
                    if g == 'w3' and abs(total - u['population']) > 1e-6:
                        # the uncovered scenario at this total: custody/arrests scale with the total linearly
                        hold = tuple(v * total / u['population'] for v in hold)
                sc, obs, true = build(g, sc0, members, k, f, total, extra, msex, mgroup, hold=hold, own_rule=(g == 'blk'))
                scs[name, rule, arm] = (sc, obs, true)
                result['counts'][f'{name}/{rule}/{arm}'] = {'observed_own_scale': obs, 'true_own_scale': true,
                                                            'published_total': total}
                if arm != 'none':
                    groups_r = race_group(extra)
                    by = []
                    for band in BANDS:
                        for s in (1, 2):
                            age20 = extra.A_AGE.to_numpy() - 5   # coarse: March-2025 age less 5, for the summary only
                            m = rows & (age20 >= band[0]) & (age20 <= band[1]) & (extra.A_SEX.to_numpy() == s)
                            by.append({'band_2020_coarse': f'{band[0]}-{band[1]}', 'sex': s,
                                       'missed_people': float((R.w[m] * f[m]).sum()),
                                       'controlled_people': float(R.w[m].sum())})
                    result['missed_by_band'][f'{name}/{rule}/{arm}'] = by
                    result['missed_by_band'][f'{name}/{rule}/{arm}/by_group'] = {
                        gk: float((R.w * f * (rows & (groups_r == gk))).sum()) for gk in RACE_GROUPS}
    # positive control 2: the rebuilt published scenarios reproduce the published cost exactly
    costs = {}
    for key, (sc, obs, true) in scs.items():
        costs[key] = run(sc)
    for name in GROUPS:
        pub = run(groups[name])
        for be, r in pub.items():
            gate(f'{name}/{be[0]}/{be[1]}/{be[2]}: rebuilt published scenario reproduces its cost (1e-9bn)',
                 abs(costs[name, 'current', 'none'][be]['cost'] - r['cost']) < 1e-9,
                 f"{costs[name, 'current', 'none'][be]['cost']:.9f} vs {r['cost']:.9f}")
    fields = ('cost', 'taxes_lost', 'spending_saved', 'capital', 'production_gain', 'balance', 'net_budget')
    for key, by in costs.items():
        if key[0] == 'lineage_block_base':
            continue
        for (mortality, basis, end), r in by.items():
            row = {'scenario': key[0], 'rule': key[1] if len(key) == 3 else 'children', 'coverage': key[-1],
                   'mortality': mortality, 'basis': basis, 'end': end}
            if key[0] == 'lineage_block':
                b = costs['lineage_block_base', 'none'][mortality, basis, end]
                row.update({f + '_bn': r[f] - b[f] for f in fields}, population=scs[key][2],
                           pricing='increment over A1 at its own count')
            else:
                row.update({f + '_bn': r[f] for f in fields}, population=r['population'], pricing='scenario')
            result['runs'].append(row)
    targets = children_targets(groups, kids, scs, extra, msex, mgroup)
    if FAILS:
        raise SystemExit('[BLOCKED] ' + '; '.join(FAILS))
    (OUT / 'children_targets_oct15.json').write_text(json.dumps(targets, indent=1) + '\n')
    peak = require_within_budget('members and coverage terms')
    (OUT / 'members_coverage_oct15.json').write_text(json.dumps(result, indent=1) + '\n')
    with (OUT / 'members_coverage_runs_oct15.csv').open('w', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=list(result['runs'][0]), lineterminator='\n')
        writer.writeheader()
        writer.writerows(result['runs'])
    print(f"[PASS] members and coverage terms; elapsed_seconds={time.perf_counter() - started:.1f} peak_footprint_gb={peak / 1e9:.3f}")


if __name__ == '__main__':
    main()
