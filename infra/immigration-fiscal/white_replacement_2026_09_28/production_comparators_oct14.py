"""Same CES removal rule on each comparator's skill mix, conditional SDR sampling SE.

Inputs are the pinned ASEC archive, the live case's exported production cells and
matched_benefits_2026_09_19/model.py. No nativity exception and no new capital tax.
The added lineage's own production term remains the delivered case's overlay.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('comparator_ces', HERE.parent / 'matched_benefits_2026_09_19/model.py')
CES = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CES)


def sampling_se(values):
    values = np.asarray(values, float)
    if values.shape != (161,) or not np.isfinite(values).all():
        raise ValueError('[BLOCKED] production requires 161 finite SDR estimates')
    return float(np.sqrt(4 / 160 * np.square(values[1:] - values[0]).sum()))


def read_replicates(z, ids, fields, chunk_size=2048):
    index = pd.MultiIndex.from_frame(ids[['PH_SEQ', 'PPPOS']])
    if not index.is_unique:
        raise ValueError('[BLOCKED] duplicate production person IDs')
    weights = np.empty((len(ids), len(fields)), float)
    seen = np.zeros(len(ids), bool)
    for chunk in pd.read_csv(z.open('asec_csv_repwgt_2025.csv'),
                             usecols=['h_seq', 'PPPOS', *fields], chunksize=chunk_size):
        keys = pd.MultiIndex.from_frame(chunk[['h_seq', 'PPPOS']])
        pos = index.get_indexer(keys)
        if (pos < 0).any() or not keys.is_unique or seen[pos].any():
            raise ValueError('[BLOCKED] missing or duplicate production replicate IDs')
        weights[pos] = chunk[fields].to_numpy(float)
        seen[pos] = True
    # Published ASEC SDR replicates contain negative weights; retain them as
    # every canonical estimator does. Only the full-sample point is nonnegative.
    if ('pwwgt0' not in fields or not seen.all() or not np.isfinite(weights).all()
            or (weights[:, fields.index('pwwgt0')] < 0).any()):
        raise ValueError('[BLOCKED] incomplete or invalid production replicate join')
    return weights


class Production:
    def __init__(self, W):
        self.W, self.cache = W, {}
        self.states = json.loads((HERE / 'derived/production_state_oct14.json').read_text())
        row4 = json.loads((HERE.parent / 'main_case_candidate_2026_09_28/derived/production_row4.json').read_text())
        R = W.R
        with zipfile.ZipFile(R.ZIP) as z:
            d = pd.read_csv(z.open('pppub25.csv'), usecols=['PH_SEQ', 'PPPOS', 'A_HGA', 'PEARNVAL'])
            # Streaming avoids retaining two full weight frames plus a merged
            # copy while the fiscal library's point frame is already resident.
            weights = read_replicates(z, d, W.F.REPS)
        if len(d) != len(R.d) or not np.array_equal(d.PH_SEQ, R.d.PH_SEQ) or not np.array_equal(d.PEARNVAL, R.d.PEARNVAL):
            raise ValueError('[BLOCKED] production frame is not the rough frame in source order')
        if not np.allclose(weights[:, 0] * R.civ, W.PUBLISHED_W, rtol=0, atol=.01):
            raise ValueError('[BLOCKED] production point weights differ from rough frame')
        # Each replicate is raked to the same ACS cell total, as production_row4.py.
        for status, label in ((4, 'naturalized'), (5, 'noncitizen')):
            m = R.d.PENATVTY.eq(303).to_numpy() & R.d.PRCITSHP.eq(status).to_numpy() & ~np.isin(W.S.st, W.L.CA_TX)
            target = row4['row4_factors'][label]['acs_population']
            weights[m] *= target / weights[m].sum(axis=0)
        # The fiscal rough keys use rounded MARSUPWT/100. The principal production
        # calibration uses pwwgt0; do not substitute the rounded weight for it.
        self.point_weight_rounding_max = float(np.max(np.abs(weights[:, 0] * R.civ - R.w)))
        for status, label in ((4, 'naturalized'), (5, 'noncitizen')):
            m = R.d.PENATVTY.eq(303).to_numpy() & R.d.PRCITSHP.eq(status).to_numpy() & ~np.isin(W.S.st, W.L.CA_TX)
            W.gate(f'production {label}: all 161 weights close to principal ACS cell (1e-6 persons)',
                   np.max(np.abs(weights[m].sum(axis=0) - row4['row4_factors'][label]['acs_population'])) < 1e-6)
        self.weights = weights * R.civ[:, None]
        del weights
        self.earn = d.PEARNVAL.clip(lower=0).to_numpy(float)
        self.skill = [d.A_HGA.between(31, 39).to_numpy(), d.A_HGA.between(40, 46).to_numpy()]
        W.gate('production skill partition conserves national earnings in all 161 columns (1e-6bn)',
               np.max(np.abs(sum((self.earn * s) @ self.weights for s in self.skill) - self.earn @ self.weights)) / 1e9 < 1e-6)
        self.national = np.array([(self.earn * s) @ self.weights for s in self.skill])
        for end in W.ENDS:
            st = self.states[end]
            W.gate(f'{end}: production specification is the adopted dump specification', st['spec'] == W.DUMP['accrual'][end]['spec'])
            # The principal production grid removes the actual observed mask;
            # the rough fiscal scenario separately scales its rounded count.
            control = {'cps_w': R.w * R.MASK['mex'], 'ages': 'own'}
            v = self.evaluate(control, end, rerake=False)
            want = next(x['effect_bn'] for x in W.DUMP['accrual'][end]['lines'] if x['id'] == 'production_gain_bn')
            W.gate(f'{end}: union CES reproduces delivered production term (1e-8bn)', abs(v[0] - want) < 1e-8, f'{v[0]:.9f} / {want:.9f}')
        W.stop_if_failed()

    def evaluate(self, sc, end, rerake=True):
        cw, R = sc['cps_w'], self.W.R
        key = (end, rerake, hashlib.sha256(cw.tobytes()).hexdigest())
        if key in self.cache:
            return self.cache[key]
        target, outside = np.empty((2, 161)), np.empty((2, 161))
        # Replicates are independent columns. Work in small blocks instead of
        # retaining several n-person x 161-column scenario/complement copies.
        for start in range(0, 161, 16):
            cols = slice(start, min(start + 16, 161))
            wt = self.scenario_weights(sc, rerake, cols)
            target[:, cols] = np.array([(self.earn * s) @ wt for s in self.skill])
            remaining = self.weights[:, cols] - wt
            outside[:, cols] = np.array([(self.earn * s) @ remaining for s in self.skill])
        if np.max(np.abs(target + outside - self.national)) / 1e9 >= 1e-6:
            raise ValueError('[BLOCKED] group/complement skill earnings do not conserve national totals')
        st = self.states[end]
        if st['proxy'] != 'PEARNVAL' or st['split'] != 'hs_or_less':
            raise ValueError('[BLOCKED] undeclared production skill/proxy policy')
        shares, fractions = self.national / self.national.sum(axis=0), target / self.national
        r = CES.equilibrium(shares, fractions, st['sigma'], st['labor_share'], st['capital_adjustment'], st['labor_supply_elasticity'])
        part = CES.fiscal_and_private(r, [.384, .426], .246, st['capital_tax_retention'], st['excluded_capital_owner_share'])
        if np.max(np.abs(part['capital_tax_gain'])) > 1e-12:
            raise ValueError('[BLOCKED] production capital-tax term overlaps job-capital receipt lines')
        scale = np.full(161, 29298.) if st['normalization'] == 'gdp' else self.national.sum(axis=0) / st['labor_share'] / 1e9
        value = part['private_plus_receipts'] * scale
        self.cache[key] = value
        return value

    def scenario_weights(self, sc, rerake=True, columns=slice(None)):
        cw, R = sc['cps_w'], self.W.R
        ratios = np.divide(cw, R.w, out=np.zeros_like(cw), where=R.w > 0)
        wt = self.weights[:, columns] * ratios[:, None]
        if rerake:
            # Hold a slice's requested count and, where specified, its age mix fixed.
            if sc['ages'] == 'own':
                wt *= cw.sum() / wt.sum(axis=0)
            else:
                for b in R.BANDS:
                    m = R.cage == b
                    target = cw[m].sum()
                    if target:
                        wt[m] *= target / wt[m].sum(axis=0)
        return wt

    def gain(self, sc, end):
        return float(self.evaluate(sc, end)[0])
