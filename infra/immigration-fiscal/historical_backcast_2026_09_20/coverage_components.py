"""Consume oct15 coverage's authoritative typed pieces before historical transport.

No scalar federal-share fallback: named source pieces remain separate, and the
per-head constants/net calibration remain an explicit unlocated residual.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = HERE.parent / "coverage_bound_2026_10_14"
sys.path.insert(0, str(SOURCE))
import coverage_bound as C
import dependency_manifest


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] coverage source-piece profile: " + message)


def typed_rows(source, lines):
    """Canonical source IDs handle native-child aliases without name inference."""
    rows = []
    for end in C.ENDS:
        principal = source['ends'][end]
        decomposition = principal['decomposition']
        require(abs(source['parts'][end]['added']['coverage_bn']) < 1e-12,
                'added-person coverage needs its own declared historical transport')
        for i, piece in enumerate(decomposition['line_parts']):
            gen, kind = piece['generation'], piece['economic_class']
            require(gen in C.GENS, f'unknown source generation {gen}')
            lid = piece.get('source_line', piece['line'])
            common = dict(piece=f'{end}_{i}', end=end, generation=gen, line=lid,
                          source_piece_line=piece['line'], category=piece.get('category', 'unclassified'),
                          economic_class=kind)
            if kind == 'production':
                require(abs(piece['coverage_bn'] + piece['P_bn'] + piece['F_bn']) < 1e-9,
                        'typed production cost/sign closure')
                for field, name in [('P_bn', 'private_wtp_bn'), ('F_bn', 'induced_receipts_bn')]:
                    rows.append(dict(common, piece=f'{end}_{i}_{field}', line=name, side='production',
                                     value_bn=-piece[field], unlocated=False,
                                     transport_assumption=decomposition['production']['scope']))
            elif kind == 'capital_return':
                matches = [r for r in lines['generations'][gen][end]['capital'] if r['id'] == lid]
                require(len(matches) == 1, f'{gen}/{end}/{lid} has no unique canonical capital component')
                require(matches[0]['level'] == piece['level'], 'typed capital level changed')
                rows.append(dict(common, side='capital', value_bn=piece['coverage_bn'], unlocated=False,
                                 component_level=piece['level'], component_part=matches[0]['part']))
            elif kind == 'fiscal_line':
                side = piece['source_side']
                require(side in ('spending', 'receipt'), f'unknown fiscal source side {side}')
                require(piece.get('category') != 'pension_accrual' or lid in ('social_security', 'medicare'),
                        f'{lid} accrual lacks its source-specific income rule')
                rows.append(dict(common, side=side, value_bn=piece['coverage_bn'], unlocated=False))
            elif kind in ('unclassified_post_engine', 'unclassified_residual'):
                rows.append(dict(common, side='unlocated', value_bn=piece['coverage_bn'], unlocated=True,
                                 rule='source-declared unclassified post-engine/residual; class/federal split unresolved; held per declared union/G3+ population path'))
            else:
                require(False, f'unknown source economic class {kind}')
        for gen in C.GENS:
            require(abs(sum(r['value_bn'] for r in rows if r['end'] == end and r['generation'] == gen)
                        - principal['by_generation'][gen]) < 1e-9, f'{end}/{gen} typed generation closure')
        total = sum(r['value_bn'] for r in rows if r['end'] == end)
        require(abs(total - principal['total_bn']) < 1e-9, f'{end} typed principal closure')
        require(abs(total - decomposition['total_cost_bn']) < 1e-9, f'{end} typed decomposition closure')
    require(all(np.isfinite(r['value_bn']) for r in rows), 'nonfinite typed source piece')
    return rows


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    principal_path = SOURCE / "derived/coverage_bound_oct15.json"
    require(principal_path.exists(), "the parent's oct15 coverage file has not been delivered")
    principal = json.loads(principal_path.read_text())
    require(principal["key"] == "oct15", "wrong source case")
    result = {"case": "oct15", "coverage_transport": "source_piece_profile", "sets": {}, "inputs": {}}
    recovery_path = HERE.parent / 'uncertainty_propagation_2026_09_22/coverage_pes.py'
    spec = importlib.util.spec_from_file_location('backcast_coverage_recipe', recovery_path)
    recovery_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(recovery_module)
    result['source_recipe_validation'] = {}
    for basis in ("set", "cash"):
        manifest = SOURCE / f"inputs/pricing_dependencies_oct15_{basis}.json"
        audit_path = SOURCE / f"derived/pricing_audit_oct15_{basis}.json"
        cache_path = SOURCE / f"_cache/oct15/{basis}/pricing.npz"
        lines_path = SOURCE / ("inputs/oct15_base/lines.json" if basis == "set" else "inputs/oct15_base/lines_cash.json")
        require(all(p.exists() for p in (manifest, audit_path, cache_path, lines_path)), f"{basis} typed source inputs absent")
        recovery = recovery_module.validate_source_recipe(HERE.parent, manifest, dependency_manifest)
        result['source_recipe_validation'][basis] = recovery
        audit = json.loads(audit_path.read_text())
        require(audit["case"] == "oct15" and audit["basis"] == basis, "wrong price audit epoch")
        extra_sources = []
        if recovery.get('parity_receipt'):
            replay = ROOT / recovery['parity_receipt']
            parity = json.loads(replay.read_text())
            replay_root = replay.parent
            fresh_audit_path = replay_root / f'derived/pricing_audit_oct15_{basis}.json'
            fresh_cache_path = replay_root / f'_cache/oct15/{basis}/pricing.npz'
            fresh_audit = json.loads(fresh_audit_path.read_text())
            C.validate_cache_receipt(fresh_audit, ROOT / recovery['snapshot_manifest'], fresh_cache_path)
            original_cache_hash = hashlib.sha256(cache_path.read_bytes()).hexdigest()
            require(original_cache_hash == audit['pricing_cache_sha256'] == parity['principal_cache_sha256']
                    == parity['replay_cache_sha256'], 'original/replayed pricing cache byte parity')
            require(audit['dependency_manifest_sha256'] == hashlib.sha256(manifest.read_bytes()).hexdigest(),
                    'original pricing audit manifest changed')
            require(fresh_audit['denominator_pieces'] == audit['denominator_pieces'],
                    'replayed source driver declarations changed')
            extra_sources = [fresh_audit_path, fresh_cache_path]
        else:
            C.validate_cache_receipt(audit, manifest, cache_path)
        lines = json.loads(lines_path.read_text())
        require(all(p['denominator_scope'] == 'actual_declared_driver' for p in audit['denominator_pieces']),
                'a source piece has an untraced driver')
        result['sets'][basis] = typed_rows(principal['sets'][basis], lines)
        for p in [manifest, audit_path, cache_path, lines_path, principal_path, *extra_sources]:
            with p.open("rb") as stream:
                result["inputs"][str(p.relative_to(ROOT))] = hashlib.file_digest(stream, "sha256").hexdigest()
        snapshot = ROOT / recovery['snapshot_manifest'] if recovery.get('snapshot_manifest') else manifest
        for entry in json.loads(snapshot.read_text())['files']:
            result['inputs'][entry['path']] = entry['sha256']
        if recovery.get('snapshot_manifest'):
            result['inputs'][recovery['snapshot_manifest']] = recovery['snapshot_manifest_sha256']
        if recovery.get('parity_receipt'):
            result['inputs'][recovery['parity_receipt']] = recovery['parity_receipt_sha256']
    result['inputs'][str(recovery_path.relative_to(ROOT))] = hashlib.sha256(recovery_path.read_bytes()).hexdigest()
    result['inputs'][str(Path(__file__).resolve().relative_to(ROOT))] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    footprint = require_within_budget('coverage component trace')
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "coverage_components_oct15.json").write_text(json.dumps(result, indent=1, allow_nan=False) + "\n")
    print(f"PASS coverage named-piece/explicit-unlocated closure 1e-9; peak {footprint / 1e9:.3f} GB")


if __name__ == "__main__":
    main()
