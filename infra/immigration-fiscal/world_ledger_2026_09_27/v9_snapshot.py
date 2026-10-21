"""Explicit selected-input snapshot; capture once, verify at both route boundaries."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FILE = HERE / "inputs/oct16_source_hashes.json"
sys.path.insert(0, str(HERE.parent / "scripts"))
from adoption_gate import require_adopted
from historical_paths import relocated_record


def digest(path):
    with relocated_record(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def donor_paths():
    """Actual joint-tenure builder, source tables and preserved pricing closure."""
    fiscal = HERE.parent
    coverage = fiscal / "coverage_bound_2026_10_14"
    paths = {HERE / "v9_transport.py", HERE / "coverage_transport.py", Path(__file__).resolve()}
    paths.update(fiscal / "scripts" / name for name in (
        "historical_paths.py", "historical_paths.cjs", "historical_record_paths.json",
        "adoption_gate.py", "adoption_gate.cjs"))
    count = fiscal / "count_composition_r5_2026_10_15"
    paths.update(count / name for name in ("measure.py", "tenure.py", "mixed_interaction.py",
                                          "derived/native_person_factors.parquet"))
    # coverage_oct16 imports coverage_oct15, coverage_item21_oct16, coverage_bound
    # and source_tables; retain their local imports as one source-code epoch.
    paths.update(coverage.glob("*.py"))
    paths.add(fiscal / "generation_account_2026_09_24/_cache/asec25_generation.parquet")
    pins = coverage / "inputs/pins.json"
    paths.add(pins)
    # source_tables.load verifies these exact source files before parsing them;
    # tenure_rates additionally parses pes_cross.pdf for its Table D marginal.
    paths.update(coverage / "inputs" / name for name in (
        "pes_cross.pdf", "pes_national.pdf", "da_hispanic.xlsx", "da_age.xlsx", "legacy.json",
        "controls/base_adjustments.csv", "controls/base_adjustments_sex.csv", "controls/compare_base.py"))
    for basis in ("set", "cash"):
        manifest = coverage / f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json"
        paths.update((manifest, coverage / f"derived/pricing_audit_oct15_final_routing_{basis}.json",
                      coverage / f"_cache/oct15_final_routing/{basis}/pricing.npz"))
        paths.update(ROOT / row["path"] for row in json.loads(manifest.read_text())["files"])
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise SystemExit("[BLOCKED] missing donor source " + ", ".join(sorted(missing)))
    return paths


def verify(required=()):
    record = json.loads(FILE.read_text())
    if record.get("case") != "oct16" or record.get("provenance") != "[WORKTREE INPUT]":
        raise SystemExit("[BLOCKED] wrong oct16 source snapshot")
    for path in required:
        relative = str(path.relative_to(ROOT))
        if relative not in record["sha256"]:
            raise SystemExit("[BLOCKED] undeclared selected input " + relative)
    for relative, expected in record["sha256"].items():
        path = relocated_record(ROOT / relative)
        if not path.is_file() or digest(path) != expected:
            raise SystemExit("[BLOCKED] changed selected input " + relative)
    return record


def capture():
    require_adopted("oct16")
    old = json.loads((HERE / "inputs/oct15_source_hashes.json").read_text())
    paths = {relocated_record(ROOT / p) for p in old["sha256"] if "world_ledger_2026_09_27/" not in p}
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("[BLOCKED] missing historical selected input " + ", ".join(sorted(missing)))
    paths.update(donor_paths())
    paths.add(HERE / "source_identity.cjs")
    fiscal = HERE.parent
    required = [fiscal / "winners_losers_2026_09_24/derived/oct16" / name
                for name in ("channels.csv", "fiscal_specs.csv", "group_frame.csv", "fiscal_lines_band_ends.csv")]
    required.append(fiscal / "distribution_weights_2026_09_23/derived/oct16/channel_by_percentile.csv")
    for path in required:
        if not path.is_file():
            raise SystemExit("[BLOCKED] upstream not ready: " + str(path.relative_to(ROOT)))
    for lane in ("main_case_2026_10_16", "count_composition_r5_2026_10_15", "spending_keys_r5_2026_10_15",
                 "consumption_tax_bases_r5_2026_10_15", "one_rate_2026_10_15"):
        directory = fiscal / lane
        paths.update(p for p in directory.rglob("*") if p.is_file() and "_cache" not in p.parts
                     and p.suffix in (".cjs", ".py", ".json", ".csv", ".parquet"))
    gen = fiscal / "generation_account_2026_09_24"
    paths.update(gen / p for p in ("v9_split.cjs", "run_generations_v9.cjs"))
    paths.update(gen / "derived" / f"generation_{kind}_oct16{cash}.{ext}"
                 for kind, ext in (("corrections", "json"), ("results", "csv"), ("summary", "json")) for cash in ("", "_cash"))
    for lane in ("winners_losers_2026_09_24", "distribution_weights_2026_09_23"):
        paths.update((fiscal / lane / "derived/oct16").glob("*"))
    # world_ledger.INGROUP_VICTIMS: the live in-group victimization rows.
    paths.add(fiscal / "within_group_harm_2026_10_21/derived/rows.csv")
    # world_ledger.SOCIAL_PAIRING: the others-side social channels from the v9 pairing.
    paths.add(fiscal / "sept24_propagation_2026_09_24/derived/oct16/real_costs_totals.json")
    paths.update((fiscal / "coverage_bound_2026_10_14/derived").glob("*oct16*"))
    paths.add(fiscal / "count_composition_r5_2026_10_15/derived/native_person_factors.parquet")
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.is_file()]
    if missing:
        raise SystemExit("[BLOCKED] missing selected input " + ", ".join(sorted(missing)))
    record = {"case": "oct16", "provenance": "[WORKTREE INPUT]", "authority": "explicit selected immutable SHA256 source bytes; parent-owned commits",
              "sha256": {str(p.relative_to(ROOT)): digest(p) for p in sorted(paths)}}
    FILE.write_text(json.dumps(record, indent=1, sort_keys=True) + "\n")
    verify()
    return record


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--capture", action="store_true")
    args = parser.parse_args()
    record = capture() if args.capture else verify()
    print(f"oct16 [WORKTREE INPUT]: {len(record['sha256'])} selected sources verified")
