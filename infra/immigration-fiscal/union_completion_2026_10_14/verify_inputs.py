"""Verify all pins; --pin-new appends newly used files without changing any existing pin."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
EXTRA = [
    "mixed_unit_credits_2026_10_14/credits.py", "mixed_unit_credits_2026_10_14/derived/item.json",
    "job_capital_taxes_2026_10_14/job_capital.py",
    "job_capital_taxes_2026_10_14/inputs/census_industry_crosswalk.csv",
    "job_capital_taxes_2026_10_14/derived/item.json", "job_capital_taxes_2026_10_14/derived/national.json",
    "job_capital_taxes_2026_10_14/derived/national_by_industry.csv", "job_capital_taxes_2026_10_14/derived/case_keys.json",
    "full_account_receipts_2026_09_20/derived/allocation_keys.csv",
    "main_case_candidate_2026_09_28/derived/production_row4.json",
    "cps_imputation_keys_2026_09_23/derived/status_combination_keys.csv",
    "cps_imputation_keys_2026_09_23/combine_onbooks_lane.py",
    "receipt_side_long_run_2026_09_28/derived/counties.csv",
    "receipt_side_long_run_2026_09_28/derived/states.csv",
    "main_case_2026_10_07/derived/corrections.json", "main_case_2026_10_07/item_age_mix.cjs",
    "generation_account_2026_09_24/derived/stack_by_generation.json",
    "generation_account_2026_09_24/derived/generation_summary_oct14.json",
    "generation_account_2026_09_24/derived/generation_corrections_oct14.json",
    "generation_account_2026_09_24/derived/generation_keys.csv",
    "generation_account_2026_09_24/derived/generation_key_shares.json",
    "generation_account_2026_09_24/derived/v4_inputs.json",
    "main_case_2026_10_14/derived/lineage_addition.json",
    "main_case_2026_10_14/item_row4.cjs", "main_case_2026_10_14/item_child_credits.cjs",
    "main_case_2026_10_14/item_job_capital.cjs",
    "added_age_mix_2026_10_07/derived/band_lines.json",
    "gen_ledger_extension_2026_09_16/state_parameters.csv",
    "build/meps_health_transport_2024.py",
    "../../sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip",
    "../../sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt",
]


def sha(path):
    with path.open("rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pin-new", action="store_true")
    args = parser.parse_args()
    path = HERE / "inputs/pins.json"
    pins = json.loads(path.read_text())
    for name, digest in pins["sha256"].items():
        assert sha(FISCAL/name) == digest, f"[BLOCKED] changed pinned source: {name}"
    added = json.loads((HERE / "derived/added_band_prices.json").read_text())
    for name,digest in added["meta"]["hashes"].items():
        assert sha(FISCAL/name) == digest, f"[BLOCKED] added-price input changed: {name}"
    required = set(EXTRA) | set(added["meta"]["hashes"])
    missing = required-set(pins["sha256"])
    if args.pin_new:
        for name in sorted(missing):
            pins["sha256"][name] = sha(FISCAL/name)
        path.write_text(json.dumps(pins,indent=2)+"\n")
    else:
        assert not missing, f"[BLOCKED] unpinned inputs: {sorted(missing)}"
    print(f"PASS: {len(pins['sha256'])} immutable input hashes")


if __name__ == "__main__":
    main()
