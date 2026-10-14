#!/usr/bin/env python3
"""Freeze/check this lane's primary sources and frozen upstream controls.
--initialize is one-time and refuses overwrite. Default checks only, offline.
"""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

HERE = Path(__file__).resolve().parent


def digest(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def leaves(obj):
    if isinstance(obj, dict):
        if "path" in obj and "sha256" in obj:
            yield obj
        else:
            for value in obj.values():
                yield from leaves(value)


def freeze():
    records = {}
    for name in ["spending_pins.json", "highways_pins.json", "incidents_pins.json"]:
        for row in leaves(json.loads((HERE / "inputs" / name).read_text())):
            records[row["path"]] = row.copy()
    inventory = json.loads((HERE / "derived/inventory.json").read_text())
    for path, sha in inventory["inputs_sha256"].items():
        records["../" + path] = {"path": "../" + path, "sha256": sha, "kind": "frozen v7 control"}
    activity = json.loads((HERE / "derived/activity_keys.json").read_text())
    for path, sha in activity["meta"]["input_sha256"].items():
        relative = "../job_capital_taxes_2026_10_14/" + path
        records[relative] = {"path": relative, "sha256": sha, "kind": "item6 upstream control"}
    original = HERE.parent / "job_capital_taxes_2026_10_14/_cache/bea_SUPPLY-USE.zip"
    copy = HERE / "_cache/bea_SUPPLY-USE.zip"
    if not copy.exists():
        shutil.copyfile(original, copy)
    source = activity["meta"]["output_source"]
    records[str(copy.relative_to(HERE))] = {"path": str(copy.relative_to(HERE)), "sha256": source["sha256"], "url": source["url"], "kind": "BEA parsed primary archive"}
    return {"case": "oct14", "sources": [records[p] for p in sorted(records)]}


def validate(manifest):
    for row in manifest["sources"]:
        path = HERE / row["path"]
        if not path.is_file() or digest(path) != row["sha256"]:
            raise RuntimeError(f'[BLOCKED] pinned source missing/stale: {row["path"]}')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--initialize", action="store_true")
    args = parser.parse_args()
    target = HERE / "inputs/pins.json"
    if args.initialize:
        if target.exists():
            raise RuntimeError("[BLOCKED] refusing to replace existing source pins")
        manifest = freeze()
        validate(manifest)
        target.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    else:
        manifest = json.loads(target.read_text())
        validate(manifest)
    print(f'PASS {len(manifest["sources"])} source/control hashes; pins unchanged')


if __name__ == "__main__":
    main()
