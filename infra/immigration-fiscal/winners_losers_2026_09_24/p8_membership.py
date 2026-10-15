"""Observed v8 membership, preserving the v7 payer frame and its latent thinning."""
from __future__ import annotations

import ast
import importlib.util
from pathlib import Path
import zipfile

import numpy as np
import pandas as pd


def require(ok, message):
    if not bool(ok):
        raise ValueError('[BLOCKED] v8 membership: ' + message)


def source_masks(d, fiscal, canonical):
    """Execute the two authoritative, side-effect-free producer mask functions."""
    source = Path(fiscal) / 'union_completion_2026_10_14/completion.py'
    tree = ast.parse(source.read_text())
    fns = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in {'masks', 'siblings'}]
    require(len(fns) == 2, 'completion mask API changed')
    ns = {'np': np, 'gate': lambda name, ok, **kw: require(ok, name)}
    exec(compile(ast.Module(body=fns, type_ignores=[]), str(source), 'exec'), ns)
    civ, union, _, _, reporters, _, _ = ns['masks'](d, canonical)
    arms, mex, _ = ns['siblings'](d, canonical, civ, union)
    return reporters, arms['biological'] & ~mex, source


def apply_membership(d, fiscal, canonical):
    """Return a copy with observed completion members; coverage has no CPS rows."""
    d = d.copy()
    canonical_path = Path(fiscal) / 'generation_account_2026_09_24/frame.py'
    if not all(hasattr(canonical, name) for name in ('masks', 'parent_rows')):
        spec = importlib.util.spec_from_file_location('p8_membership_canonical', canonical_path)
        canonical = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(canonical)
    archive = Path(fiscal) / 'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    fields = ['PH_SEQ', 'PPPOS', 'PEPAR1TYP', 'PEPAR2TYP']
    missing = [k for k in fields[2:] if k not in d]
    if missing:
        with zipfile.ZipFile(archive) as z:
            extra = pd.read_csv(z.open('pppub25.csv'), usecols=fields[:2] + missing)
        d = d.merge(extra, on=fields[:2], how='left', validate='one_to_one', sort=False)
        require(d[missing].notna().all().all(), 'parent fields join incomplete')
    reporters, children, source = source_masks(d, fiscal, canonical)
    require(not (reporters & children).any(), 'reporters and children overlap')
    added = reporters | children
    require(not (added & d.target.to_numpy(bool)).any(), 'completion already a member')
    original_other = d.other_base.to_numpy(bool) if 'other_base' in d else d.other.to_numpy(bool)
    require(np.all(original_other[added]), 'completion outside original payer frame')
    d['target_oct14'] = d.target.to_numpy(bool)
    d['other_oct14'] = original_other
    d['completion_reporter'] = reporters
    d['completion_child'] = children
    d['completion_member'] = added
    d['target'] = d.target_oct14 | added
    d['other'] = d.other_oct14 & ~added
    require(not (d.target & d.other).any(), 'person sits in group and payer pool')
    return d, dict(source_paths=[str(source), str(archive), str(canonical_path)],
                   reporter_records=int(reporters.sum()), child_records=int(children.sum()),
                   coverage_payer_people=0.0)


def payer_weights(d, weights, lineage, wl, *, geographic=True):
    """First reproduce oct14's latent payer thinning, then remove actual additions.

    The one-US-parent reporter and child masks are outside v7's two-US-parent
    latent-loss universe. Therefore they retain their full original weights.
    Coverage is survey-absent and must never be subtracted from the payer pool.
    """
    from p8_recipient_keys import lineage_payers_state_age
    import p7_frames
    original = d.copy()
    original['target'], original['other'] = d.target_oct14, d.other_oct14
    fn = lineage_payers_state_age if geographic else p7_frames.lineage_payers
    out, cells = fn(original, np.asarray(weights, float), lineage, wl)
    old_other = original.other.to_numpy(bool)
    completion = d.completion_member.to_numpy(bool)
    original_total = float(out[old_other].sum())
    require(np.all(out[completion] == np.asarray(weights)[completion]),
            'completion overlaps existing latent payer thinning')
    removed = float(np.asarray(weights)[completion].sum())
    out[completion] = 0.0
    got = float(out[d.other.to_numpy(bool)].sum())
    tolerance = 1e-6 * max(original_total, 1.)
    require(abs(got - (original_total - removed)) <= tolerance,
            'oct15 payer pool differs from oct14 minus observed completion')
    require(not np.any((out > 0) & d.target.to_numpy(bool) & ~d.target_oct14.to_numpy(bool)),
            'new member retains payer weight')
    return out, cells, dict(oct14_payer_people=original_total, removed_completion_people=removed,
                           oct15_payer_people=got, coverage_payer_people=0.,
                           payer_gap_people=got - (original_total - removed))


def replacement_credit(d, payer_weights, legacy_credit, source_weights):
    """Move the old5b term for the beside fiscal-attribution incidence arm.

    This forward-only restoration preserves the previous attribution convention;
    it is not raw own-resource policy incidence. The direct policy route observes
    native tax/refund before-after flows and never calls for any old5b restoration.
    Newly completed claimant carriers use the explicit same-SPM/state rule.
    """
    from p8_stayers import _remap
    weights = np.asarray(payer_weights, float)
    original = np.asarray(legacy_credit, float) * np.asarray(source_weights, float) / 1e9
    routed, audit = _remap(original, d.other.to_numpy(bool), d.SPM_ID.to_numpy(),
                           d.st.to_numpy(), weights)
    array = np.divide(routed * 1e9, weights, out=np.zeros(len(d)), where=weights > 0)
    require(abs(float(array @ weights / 1e9) - float(original.sum())) < 1e-8,
            'old5b replacement lost source dollars')
    return array, dict(source_total_bn=float(original.sum()),
                       recipient_total_bn=float(array @ weights / 1e9), **audit)
