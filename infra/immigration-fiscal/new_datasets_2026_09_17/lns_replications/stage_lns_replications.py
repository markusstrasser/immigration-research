#!/usr/bin/env python3
"""Copy only hash-verified public replication artifacts; never join respondent rows.

uv run python3 stage_lns_replications.py --source-dir VERIFIED_DOWNLOADS \
    --destination RAW_DIRECTORY

Requires Python 3.11+ and only its standard library.
The adjacent source_manifest.json records the public acquisition URLs. This script
does no network access, authentication, parsing, reweighting, or respondent linkage.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import sys
import tempfile


def digest(path):
    with path.open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def safe_path(root, relative):
    rel = Path(relative)
    if rel.is_absolute() or '..' in rel.parts or not rel.parts:
        raise ValueError(f'Unsafe relative path: {relative}')
    target = root / rel
    if not target.resolve().is_relative_to(root):
        raise ValueError(f'Path escapes configured directory: {relative}')
    return target


def verify(path, expected_size, expected_hash):
    if not path.is_file():
        raise ValueError(f'Missing file: {path}')
    if path.stat().st_size != expected_size or digest(path) != expected_hash:
        raise ValueError(f'Size/hash mismatch: {path}')


def copy_verified(source, target, size, sha256):
    if target.exists():
        verify(target, size, sha256)
        return False
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(dir=target.parent, prefix='.lns-stage-', delete=False) as handle:
            temporary = Path(handle.name)
            with source.open('rb') as origin:
                shutil.copyfileobj(origin, handle)
        verify(temporary, size, sha256)
        try:
            os.link(temporary, target)  # Atomic, same filesystem, never overwrites.
        except FileExistsError:
            verify(target, size, sha256)
            return False
        return True
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--source-dir', type=Path, default=Path(__file__).resolve().parent)
    parser.add_argument('--destination', type=Path, required=True)
    parser.add_argument('--manifest', type=Path, default=Path(__file__).resolve().with_name('source_manifest.json'))
    parser.add_argument('--dry-run', action='store_true', help='Verify every source and destination collision without writing.')
    args = parser.parse_args()
    source_root = args.source_dir.resolve()
    destination = args.destination.resolve()
    manifest_path = args.manifest.resolve()
    manifest = json.loads(manifest_path.read_text())
    if manifest.get('schema_version') != 1 or not manifest.get('files'):
        raise ValueError('Unsupported or empty source manifest')
    jobs, seen = [], set()
    for item in manifest['files']:
        source = safe_path(source_root, item['source_relative_path'])
        target = safe_path(destination, item['destination_relative_path'])
        if target in seen:
            raise ValueError(f'Duplicate destination in manifest: {target}')
        seen.add(target)
        if item.get('repository_restriction') is True:
            raise ValueError(f'Restricted file rejected: {source}')
        jobs.append((source, target, item['bytes'], item['sha256']))
    manifest_target = destination / 'source_manifest.json'
    if manifest_target in seen:
        raise ValueError('Artifact destination conflicts with manifest snapshot')
    jobs.append((manifest_path, manifest_target, manifest_path.stat().st_size, digest(manifest_path)))
    # Complete all checks before creating any destination directory or copying.
    for source, target, size, sha256 in jobs:
        verify(source, size, sha256)
        if target.exists():
            verify(target, size, sha256)
    copied = 0
    if not args.dry_run:
        for job in jobs:
            copied += copy_verified(*job)
    print(json.dumps({'status':'verified' if args.dry_run else 'staged', 'artifact_files':len(jobs)-1,
                      'manifest_files':1, 'copied_files':copied, 'bytes':sum(j[2] for j in jobs),
                      'destination':str(destination), 'joins_performed':0}, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f'ERROR: {exc}', file=sys.stderr)
        raise SystemExit(1)
