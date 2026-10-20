"""Freeze the v9 export's explicit original-key scaffold for public goods.

The v9 native consumer declares an unchanged v8 scaffold and separate typed
corrections. Zero-response public-good donor keys use that original scaffold;
current observed calibration and current coverage masses enter separately.
"""
import argparse
import json
from pathlib import Path

import coverage_transport as CT

HERE = Path(__file__).resolve().parent
RECEIPT = HERE / "inputs/oct16_recipient_routing.json"


def capture():
    from v9_snapshot import require_adopted
    require_adopted("oct16")
    directory = HERE.parent / "within_group_distribution_2026_09_29/_cache/oct16"
    files = [directory / "lines.json", directory / "lines_cash.json",
        HERE.parent / "within_group_distribution_2026_09_29/households.py",
        HERE.parent / "coverage_bound_2026_10_14/derived/coverage_bound_oct15.json"]
    for path in files[:2]:
        data = json.loads(path.read_text())
        CT.require(data["meta"]["case"] == "main_case_2026_10_16" and data["meta"]["v9"]["scaffold_case"] == "main_case_2026_10_15", "v9 source scaffold identity")
    record = dict(case="oct16", source_scope="selected v9 native export's declared original public-good source keys; fiscal posts not substituted",
        source_hashes={str(p.relative_to(CT.ROOT)): CT.digest(p) for p in files},
        lines={b:str((directory / ("lines_cash.json" if b == "cash" else "lines.json")).relative_to(CT.ROOT)) for b in ("set", "cash")},
        frozen_source=str(files[-1].relative_to(CT.ROOT)))
    RECEIPT.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    return record


def paths(basis):
    record = json.loads(RECEIPT.read_text())
    CT.require(record.get("case") == "oct16", "wrong v9 native source receipt")
    for relative, want in record["source_hashes"].items():
        CT.require(CT.digest(CT.ROOT / relative) == want, "changed v9 native routing input " + relative)
    return CT.ROOT / record["lines"][basis], CT.ROOT / record["frozen_source"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true", required=True)
    parser.parse_args()
    print(json.dumps(capture(), indent=1))
