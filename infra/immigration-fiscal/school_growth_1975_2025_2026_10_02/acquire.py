"""Acquire parent-linked historical school microdata using the existing IPUMS client.

Run with submit, status, or download. Raw microdata stay in the ignored cache.
"""
import argparse
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "schooling_selection_position_2026_09_23"))
import ipums_api as api

api.CACHE = HERE / "_cache"
SAMPLES = ["us1980b", "us1990b", "us2000g", "us2010a", "us2024a"]
VARIABLES = ["AGE", "SEX", "BPL", "CITIZEN", "YRIMMIG", "EDUC", "EDUCD",
             "MOMLOC", "POPLOC", "SCHOOL", "SCHLTYPE", "GQ", "STATEFIP"]
SPEC = {"description": "Historical public-school children and parental education; 1975+ immigration",
        "dataFormat": "csv", "dataStructure": {"rectangular": {"on": "P"}},
        "samples": {s: {} for s in SAMPLES}, "variables": {v: {} for v in VARIABLES}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("action", choices=["submit", "status", "download"])
    args = parser.parse_args()
    api.CACHE.mkdir(exist_ok=True)
    receipt = HERE / "request.json"
    if args.action == "submit":
        if receipt.exists():
            raise SystemExit("[BLOCKED] request already recorded; use status or download")
        number = api.submit("usa", SPEC)
        receipt.write_text(json.dumps({"number": number, "spec": SPEC}, indent=2) + "\n")
        print("submitted", number)
    else:
        number = json.loads(receipt.read_text())["number"]
        if args.action == "status":
            print(number, api.status("usa", number).get("status"))
        else:
            print(api.download("usa", number, "school_parents"))


if __name__ == "__main__":
    main()
