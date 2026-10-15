#!/usr/bin/env python3
"""Native-child composition: matched universes, SDR comparisons and origin transfers.

The central calibration reallocates survey weight between origin strata, keeping
actual origin, ancestry membership and household configurations. A diagnostic
identity-transfer arm changes origin probabilities separately; reassignment cannot
erase parental-birthplace G2 membership. ACS lacks parental-nativity fields, so
the unobserved G2/G3 split is held at the CPS conditional composition.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import resource
import sys
import time
import zipfile

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = FISCAL.parents[1]
US = (57, 60, 66, 69, 73, 78)
CPS = FISCAL / 'mexican_origin_population_total_2026_09_19/_cache/cps_asec2025_person_subset.parquet'
ACS = FISCAL / 'mexican_origin_population_total_2026_09_19/_cache/acs2024_ancestry_subset.parquet'
ACS_REL = FISCAL / 'dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet'
CPS_ZIP = FISCAL / 'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
CW = [f'pwwgt{i}' for i in range(161)]
AW = ['PWGTP'] + [f'PWGTP{i}' for i in range(1, 81)]
AGES = ((0, 4), (5, 9), (10, 14), (15, 17))
KINDS = ('mexican', 'other_hispanic', 'hispanic')


def require(ok, text):
    if not ok:
        raise RuntimeError(f'[BLOCKED] native composition: {text}')


def sdr(v):
    v = np.asarray(v, float)
    return float(np.sqrt(4 / (len(v) - 1) * np.square(v[1:] - v[0]).sum()))


def compare(c, a, n_c, n_a):
    cs, ass = sdr(c), sdr(a)
    se = np.hypot(cs, ass)
    return dict(cps=float(c[0]), cps_se=cs, acs=float(a[0]), acs_se=ass,
                difference=float(c[0] - a[0]), difference_se=float(se),
                z_independent_surveys=float((c[0] - a[0]) / se) if se else 0.,
                cps_records=int(n_c), acs_records=int(n_a))


def write_csv(path, rows):
    require(bool(rows), f'empty output {path.name}')
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def load_cps():
    columns = ['PH_SEQ', 'PPPOS', 'A_LINENO', 'A_AGE', 'A_SEX', 'PRCITSHP',
               'PENATVTY', 'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP', 'PEHSPNON',
               'PRPERTYP', 'PEPAR1', 'PEPAR2', 'PEPAR1TYP', 'PEPAR2TYP'] + CW
    d = pd.read_parquet(CPS, columns=columns)
    with zipfile.ZipFile(CPS_ZIP) as z:
        h = pd.read_csv(z.open('hhpub25.csv'), usecols=['H_SEQ', 'GESTFIPS'])
    d = d.merge(h, left_on='PH_SEQ', right_on='H_SEQ', validate='many_to_one', how='left')
    require(d.GESTFIPS.notna().all(), 'all CPS household states located')
    require(not d.duplicated(['PH_SEQ', 'A_LINENO']).any(), 'CPS person keys unique')
    require(d.PRDTHSP.notna().all(), 'CPS origin observed')
    return d


def load_acs_minors():
    """Filter before materializing 81 weights; RELSHIPP=37 excludes institutions.

    Noninstitutional GQ (RELSHIPP=38) stay. Active-duty MIL=1/2 are excluded
    centrally; the verifier's RELSHIPP-only count is written separately.
    """
    cols = ['SERIALNO', 'SPORDER', 'STATE', 'AGEP', 'CIT', 'HISP'] + AW
    # Only Hispanic strata enter any comparison or calibration. Predicate
    # filtering before reading 81 weights avoids materializing all native minors.
    filters = [('AGEP', '<', 18), ('CIT', '<=', 3), ('HISP', '>', 1)]
    d = pd.read_parquet(ACS, columns=cols, filters=filters)
    r = pd.read_parquet(ACS_REL, columns=['SERIALNO', 'SPORDER', 'RELSHIPP', 'MIL'],
                        filters=filters)
    d = d.merge(r, on=['SERIALNO', 'SPORDER'], how='left', validate='one_to_one')
    require(d.RELSHIPP.notna().all(), 'ACS replicate subset joined to universe source')
    return d[d.RELSHIPP.ne(37)].copy()


def categories(d, acs=False):
    if acs:
        m = d.HISP.eq(2).to_numpy()
        h = d.HISP.gt(1).to_numpy()
    else:
        m = d.PRDTHSP.eq(1).to_numpy()
        h = d.PRDTHSP.gt(0).to_numpy()
    return dict(mexican=m, other_hispanic=h & ~m, hispanic=h)


def comparison_tables(c, a):
    native = c.PRCITSHP.isin([1, 2, 3]).to_numpy() & c.A_AGE.lt(18).to_numpy()
    ck, ak = categories(c), categories(a, True)
    cw, aw = c[CW].to_numpy(float), a[AW].to_numpy(float)
    rows, states = [], []
    cell_vectors = {}
    for region in ('national', 'CA_TX', 'outside_CA_TX'):
        cr = np.ones(len(c), bool) if region == 'national' else c.GESTFIPS.isin([6, 48]).to_numpy()
        ar = np.ones(len(a), bool) if region == 'national' else a.STATE.isin([6, 48]).to_numpy()
        if region == 'outside_CA_TX':
            cr, ar = ~cr, ~ar
        for lo, hi in ((0, 17),) + AGES:
            age = f'{lo}-{hi}'
            cm = native & cr & c.A_AGE.between(lo, hi).to_numpy()
            am = ar & a.AGEP.between(lo, hi).to_numpy()
            cell_vectors[(region, age)] = {}
            for kind in KINDS:
                cc, aa = cm & ck[kind], am & ak[kind]
                cv, av = cw[cc].sum(axis=0), aw[aa].sum(axis=0)
                row = dict(region=region, age_band=age, kind=kind,
                           **compare(cv, av, cc.sum(), aa.sum()))
                rows.append(row)
                cell_vectors[(region, age)][kind] = (cv, av)
    # State estimates are descriptive only. Flag cells with >=30 raw records
    # and <=30% coefficient of variation in both surveys; no sparse-state rake.
    for state in sorted(set(c.GESTFIPS) | set(a.STATE)):
        for lo, hi in ((0, 17),) + AGES:
            cm = native & c.GESTFIPS.eq(state).to_numpy() & c.A_AGE.between(lo, hi).to_numpy()
            am = a.STATE.eq(state).to_numpy() & a.AGEP.between(lo, hi).to_numpy()
            for kind in KINDS:
                cc, aa = cm & ck[kind], am & ak[kind]
                row = dict(state=int(state), age_band=f'{lo}-{hi}', kind=kind,
                           **compare(cw[cc].sum(axis=0), aw[aa].sum(axis=0), cc.sum(), aa.sum()))
                row['sample_allows_comparison'] = bool(row['cps_records'] >= 30 and row['acs_records'] >= 30
                    and row['cps_se'] <= .3 * row['cps'] and row['acs_se'] <= .3 * row['acs'])
                states.append(row)
    return rows, states, cell_vectors


def calibration_cell(cps_mex, cps_other, acs_mex, acs_hispanic, preserve_total):
    """Return origin-transfer probabilities, and a common Hispanic weight factor.

    Inputs may be CPS replicate vectors; ACS targets stay at central values in
    that conditional uncertainty calculation. ACS sampling errors are separate.
    """
    cm, co = np.asarray(cps_mex, float), np.asarray(cps_other, float)
    h = cm + co
    require(bool(np.all(h > 0)), 'positive Hispanic denominator in all calibration replicates')
    target_h = h if preserve_total else np.full_like(h, acs_hispanic)
    require(bool(np.all(target_h >= acs_mex)), 'Mexican target cannot exceed Hispanic target')
    factor = target_h / h
    before_mex, before_other = factor * cm, factor * co
    retain = np.minimum(1., acs_mex / before_mex)
    need = np.maximum(0., acs_mex - before_mex)
    require(bool(np.all((need == 0) | (before_other > 0))), 'other-Hispanic origin-transfer donors exist')
    other_to_mex = np.divide(need, before_other, out=np.zeros_like(need), where=before_other > 0)
    require(bool(np.all(other_to_mex <= 1 + 1e-12)), 'origin transfer probabilities bounded')
    after_mex = factor * (cm * retain + co * other_to_mex)
    require(bool(np.allclose(after_mex, acs_mex, rtol=0, atol=1e-7)), 'every replicate Mexican target closes')
    return dict(native_factor=factor, mexican_retention_probability=retain,
                other_to_mexican_probability=other_to_mex, target_hispanic=target_h,
                target_mexican=np.full_like(h, acs_mex))


def person_factors(c, vectors, comparison_rows):
    national = next(r for r in comparison_rows if r['region'] == 'national'
                    and r['age_band'] == '0-17' and r['kind'] == 'hispanic')
    agree = abs(national['z_independent_surveys']) <= 1.96
    preserve = agree or national['acs'] >= national['cps']
    policy = ('preserve_CPS_Hispanic_total' if preserve else 'ACS_lower_Hispanic_total')
    # Central changes survey weights by origin stratum; identities stay fixed.
    fields = ['PH_SEQ', 'PPPOS', 'A_LINENO', 'GESTFIPS', 'A_AGE', 'A_SEX', 'PRDTHSP']
    out = c[fields].copy()
    out['h_seq'], out['a_lineno'] = c.PH_SEQ, c.A_LINENO
    out['native_factor'] = 1.
    out['mexican_classification_factor'] = 1.
    out['mexican_effective_factor'] = 1.
    out['native_member_factor'] = 1.
    out['other_to_mexican_probability'] = 0.
    out['new_member_probability'] = 0.
    out['mexican_rake_factor'] = 1.
    out['hispanic_reassignment_factor'] = 1.
    out['central_member_factor'] = 1.
    out['reassign_to_other_hispanic'] = 0.
    out['cell'] = ''
    native = c.PRCITSHP.isin([1, 2, 3]).to_numpy() & c.A_AGE.lt(18).to_numpy()
    hisp, mex = c.PRDTHSP.gt(0).to_numpy(), c.PRDTHSP.eq(1).to_numpy()
    g2 = native & (c.PEFNTVTY.eq(303) | c.PEMNTVTY.eq(303)).to_numpy()
    # A Mexican reporter with one US-area parent is item 10's ancestry-based
    # completion universe; keep its membership when reporting origin changes.
    completion = native & mex & (c.PEFNTVTY.isin(US) ^ c.PEMNTVTY.isin(US)).to_numpy() & ~g2
    ancestry_stays = g2 | completion
    summaries, replicate_cells = [], {}
    for region in ('CA_TX', 'outside_CA_TX'):
        rm = c.GESTFIPS.isin([6, 48]).to_numpy()
        if region == 'outside_CA_TX':
            rm = ~rm
        for lo, hi in AGES:
            age = f'{lo}-{hi}'
            cell = f'{region}|{age}'
            cv = vectors[(region, age)]
            cal = calibration_cell(cv['mexican'][0], cv['other_hispanic'][0],
                                   cv['mexican'][1][0], cv['hispanic'][1][0], preserve)
            cal['mexican_rake_factor'] = cv['mexican'][1][0] / cv['mexican'][0]
            cal['hispanic_reassignment_factor'] = (cal['target_hispanic'] - cv['mexican'][1][0]) / cv['other_hispanic'][0]
            closed_h = (cv['mexican'][0] * cal['mexican_rake_factor']
                        + cv['other_hispanic'][0] * cal['hispanic_reassignment_factor'])
            require(np.allclose(closed_h, cal['target_hispanic'], rtol=0, atol=1e-7),
                    'central aggregate origin-stratum weights preserve Hispanic target every replicate')
            replicate_cells[cell] = {k: v.tolist() for k, v in cal.items()}
            m = native & rm & c.A_AGE.between(lo, hi).to_numpy()
            f, keep, enter = (cal[k][0] for k in ('native_factor', 'mexican_retention_probability',
                                                'other_to_mexican_probability'))
            out.loc[m, 'cell'] = cell
            out.loc[m & hisp, 'native_factor'] = f
            out.loc[m & mex, 'mexican_classification_factor'] = keep
            # Diagnostic identity-transfer arm is separate from central weights.
            out.loc[m & mex, 'mexican_effective_factor'] = cv['mexican'][1][0] / cv['mexican'][0][0]
            out.loc[m & mex, 'mexican_rake_factor'] = cal['mexican_rake_factor'][0]
            out.loc[m & hisp & ~mex, 'hispanic_reassignment_factor'] = cal['hispanic_reassignment_factor'][0]
            out.loc[m & mex, 'central_member_factor'] = cal['mexican_rake_factor'][0]
            out.loc[m & hisp & ~mex, 'central_member_factor'] = cal['hispanic_reassignment_factor'][0]
            out.loc[m & hisp & ~mex, 'other_to_mexican_probability'] = enter
            eligible_reporter = (c.PEFNTVTY.isin(US) | c.PEMNTVTY.isin(US)).to_numpy() & ~g2
            out.loc[m & hisp & ~mex & eligible_reporter, 'new_member_probability'] = enter
            out.loc[m & mex, 'reassign_to_other_hispanic'] = 1 - keep
            out.loc[m & hisp, 'native_member_factor'] = f
            out.loc[m & mex & ~ancestry_stays, 'native_member_factor'] = f * keep
            w = c.pwwgt0.to_numpy(float)
            summaries.append(dict(cell=cell, policy=policy, native_factor=f,
                mexican_retention_probability=keep, other_to_mexican_probability=enter,
                cps_hispanic=float(cv['hispanic'][0][0]), acs_hispanic=float(cv['hispanic'][1][0]),
                mexican_rake_factor=float(cal['mexican_rake_factor'][0]),
                hispanic_reassignment_factor=float(cal['hispanic_reassignment_factor'][0]),
                target_hispanic=float(cal['target_hispanic'][0]), target_mexican=float(cv['mexican'][1][0]),
                reassigned_mexican_people=float(w[m & mex].sum() * f * (1 - keep)),
                reassigned_G2_members_stay=float(w[m & mex & g2].sum() * f * (1 - keep)),
                reassigned_completion_members_stay=float(w[m & mex & completion].sum() * f * (1 - keep)),
                reassigned_other_reporters_depart=float(w[m & mex & ~ancestry_stays].sum() * f * (1 - keep)),
                other_Hispanic_to_Mexican_people=float(w[m & hisp & ~mex].sum() * f * enter),
                new_reporter_members_before_latent_overlap=float(w[m & hisp & ~mex & eligible_reporter].sum() * f * enter),
                central_Mexican_weight_change_people=float(w[m & mex].sum() * (cal['mexican_rake_factor'][0] - 1)),
                central_G2_Mexican_weight_change_people=float(w[m & mex & g2].sum() * (cal['mexican_rake_factor'][0] - 1)),
                CPS_member_factor_change_people=float(np.sum(w[m] * (out.native_member_factor.to_numpy()[m] - 1)))))
    require(np.isfinite(out.select_dtypes('number').to_numpy()).all(), 'person factors finite')
    return out, summaries, dict(policy=policy, national_Hispanic_totals_agree_95pct=agree,
        national_Hispanic_comparison=national, cells=replicate_cells,
        uncertainty='CPS 160 SDR replicates recalibrate denominators; ACS targets fixed centrally. Independent ACS SDR SE reported separately; no CPS–ACS covariance claimed.',
        central='Aggregate origin-stratum survey-weight calibration. central_member_factor=mexican_rake_factor on existing native Mexican minors, hispanic_reassignment_factor on other-Hispanic native minors, and 1 otherwise; lineage membership and household configurations fixed. Balancing other-Hispanic weights apply to existing lineage members too; no extra lineage entrants.',
        identity_transfer_arm='native_member_factor preserves G2 and item10 reporting-completion membership under origin reassignment; mexican_effective_factor is an all-Mexican pure-rake arm, including upwards factors. native_factor applies only Hispanic native minors; new_member_probability identifies other-Hispanic reporter entrants, and consumers must remove overlap with any existing nonreporting-lineage members.')


def linked_tables(d):
    """Duncan–Trejo intact-family generation masks, both types and biological.

    Includes all PRDTHSP codes and sex×age cells, not merely non-Hispanic cases.
    Generation describes observed co-resident lineage; it is not fiscal ownership.
    """
    n = len(d)
    ids = pd.MultiIndex.from_frame(d[['PH_SEQ', 'A_LINENO']])
    require(ids.is_unique, 'linked-family person ids unique')
    parents = np.column_stack([ids.get_indexer(pd.MultiIndex.from_arrays([d.PH_SEQ, d[f'PEPAR{j}']]))
                               for j in (1, 2)])
    pos = np.maximum(parents, 0)
    birth = d.PENATVTY.to_numpy()[pos]
    pm, pf = d.PEMNTVTY.to_numpy()[pos], d.PEFNTVTY.to_numpy()[pos]
    parent_mex = d.PRDTHSP.eq(1).to_numpy()[pos]
    child = d.PRCITSHP.isin([1, 2, 3]).to_numpy() & d.A_AGE.lt(18).to_numpy() & d.PENATVTY.ne(303).to_numpy()
    W = d[CW].to_numpy(float)
    rows, vectors = [], {}
    for arm in ('all_parent_types', 'biological'):
        present = parents >= 0
        if arm == 'biological':
            present &= d[['PEPAR1TYP', 'PEPAR2TYP']].to_numpy() == 1
        intact = present.all(axis=1)
        gp = ((pm == 303) | (pf == 303)).any(axis=1)
        mexico = (birth == 303).any(axis=1)
        all_us = np.isin(birth, US).all(axis=1)
        base = child & intact
        gens = {'G2': base & mexico, 'G3': base & ~mexico & all_us & gp,
                'G4plus': base & ~mexico & all_us & ~gp & parent_mex.any(axis=1)}
        for generation, gm in gens.items():
            for lo, hi in ((0, 17),) + AGES:
                for sex in (0, 1, 2):
                    m = gm & d.A_AGE.between(lo, hi).to_numpy()
                    if sex:
                        m &= d.A_SEX.eq(sex).to_numpy()
                    for origin in ('all', 'Mexican', 'other_Hispanic', 'non_Hispanic', 'all_nonMexican'):
                        om = {'all': np.ones(n, bool), 'Mexican': d.PRDTHSP.eq(1).to_numpy(),
                              'other_Hispanic': d.PRDTHSP.gt(1).to_numpy(),
                              'non_Hispanic': d.PRDTHSP.eq(0).to_numpy(),
                              'all_nonMexican': d.PRDTHSP.ne(1).to_numpy()}[origin]
                        v = W[m & om].sum(axis=0)
                        rows.append(dict(parent_arm=arm, generation=generation, age_band=f'{lo}-{hi}',
                                         sex=sex, origin=origin, persons=float(v[0]), se=sdr(v),
                                         records=int(np.sum(m & om))))
                        if lo == 0 and hi == 17 and sex == 0:
                            vectors[f'{arm}|{generation}|{origin}'] = v.tolist()
                    for code in sorted(d.loc[m, 'PRDTHSP'].unique()):
                        selected = m & d.PRDTHSP.eq(code).to_numpy()
                        v = W[selected].sum(axis=0)
                        rows.append(dict(parent_arm=arm, generation=generation, age_band=f'{lo}-{hi}',
                                         sex=sex, origin=f'PRDTHSP_{int(code)}', persons=float(v[0]), se=sdr(v),
                                         records=int(selected.sum())))
    return rows, vectors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', type=Path, default=HERE / 'derived')
    parser.add_argument('--skip-linked', action='store_true')
    args = parser.parse_args()
    start = time.perf_counter()
    args.out.mkdir(parents=True, exist_ok=True)
    c, a_all = load_cps(), load_acs_minors()
    a = a_all[~a_all.MIL.isin([1, 2])].copy()
    rows, states, vectors = comparison_tables(c, a)
    comparable, _, _ = comparison_tables(c, a_all)
    household, _, _ = comparison_tables(c, a_all[a_all.RELSHIPP.lt(37)])
    factors, calibration, cal = person_factors(c, vectors, rows)
    write_csv(args.out / 'native_cells.csv', rows)
    write_csv(args.out / 'native_verifier_universe.csv', comparable)
    write_csv(args.out / 'native_household_cells.csv', household)
    write_csv(args.out / 'native_states.csv', states)
    write_csv(args.out / 'native_calibration.csv', calibration)
    factors.to_parquet(args.out / 'native_person_factors.parquet', index=False)
    (args.out / 'native_calibration_replicates.json').write_text(json.dumps(cal, indent=2) + '\n')
    if not args.skip_linked:
        linked, linked_rep = linked_tables(c)
        write_csv(args.out / 'linked_origin_age_sex.csv', linked)
        (args.out / 'linked_origin_replicates.json').write_text(json.dumps(linked_rep, indent=2) + '\n')
    audit = dict(inputs={str(p.relative_to(REPO)): dict(bytes=p.stat().st_size,
                 sha256=hashlib.file_digest(p.open('rb'), 'sha256').hexdigest())
                 for p in (CPS, ACS, ACS_REL, CPS_ZIP)},
        universe='native citizenship codes 1–3; ages 0–17; CPS household survey; ACS excludes RELSHIPP=37 and MIL=1/2, retains noninstitutional GQ. native_verifier_universe.csv retains MIL=1/2 for verifier comparison',
        comparison_assumption='2025 March CPS versus 2024 annual ACS; timing and classification differences unresolved; independent-survey SDR standard errors',
        calibration_policy=cal['policy'], national_hispanic_z=cal['national_Hispanic_comparison']['z_independent_surveys'],
        sparse_state_rule='descriptive: both raw n>=30 and both CV<=0.30; age×region calibrations only',
        rows=dict(cps=len(c), acs_native_Hispanic_minors=len(a), person_factors=len(factors)),
        gates=dict(unique_CPS_keys=True, all_ACS_universe_links=True, every_CPS_replicate_Mexican_target_closes=True,
                   ancestry_G2_preserved_under_reclassification=True),
        limits=['ACS cannot identify parental-birthplace G2 versus G3; conditional CPS mix held.',
                'Origin transfer probabilities are fractional calibration, not observed individual reclassification.',
                'Do not additionally multiply a coverage count by a separate generic native ratio: recount its base with the person factors first.',
                'Central uses central_member_factor with household kernels and keeps membership masks fixed. native_member_factor and new_member_probability are diagnostic identity-transfer arms only.'])
    (args.out / 'native_audit.json').write_text(json.dumps(audit, indent=2) + '\n')
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != 'darwin':
        peak *= 1024
    require(peak < 2_500_000_000, 'native process exceeded 2.5GB RSS; outputs are not validated')
    print(json.dumps(dict(policy=cal['policy'], national_hispanic_z=audit['national_hispanic_z'],
        elapsed_seconds=time.perf_counter()-start, peak_rss_bytes=peak)))


if __name__ == '__main__':
    main()
