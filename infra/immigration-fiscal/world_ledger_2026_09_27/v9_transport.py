"""Economic donor weights from v9's exact joint calibration/tenure builder.

Fiscal component amounts stay in their own typed case export. No generation-
average fiscal price is presented as a reconstructed person price.
"""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

import coverage_transport as CT
import valuation as V

HERE = Path(__file__).resolve().parent


def export(basis):
    from v9_snapshot import donor_paths, verify
    required = donor_paths()
    verify(required)
    sys.path.insert(0, str(CT.COVERAGE))
    import coverage_oct16 as source
    data, audit = source.load_kernel(basis, "oct15_final_routing")
    rates, base = source.load()
    tenure, factor = source.person_inputs(data)
    weight = data["weights"][:, 0] * factor
    f, _ = source.fixed_count_tenure(data, tenure, weight, rates, base)
    missing = weight * f
    payload = V.case_payload("oct16")
    want = payload["meta"]["coverage_tenure"]["coverage_counts_by_generation"]
    observed = {}
    for i, g in enumerate(source.GENS):
        observed[g] = float(missing[data["generation"] == i].sum())
        CT.require(abs(observed[g] - want[g]) < 1e-6, "v9 joint source donor count " + g)
    _, added_factor = source.C.factors(data, rates, base)
    CT.require(np.all(data["added_weights"][:, 0] * added_factor == 0), "nonzero latent coverage needs its own donor arm")
    frame = pd.DataFrame(dict(PH_SEQ=data["person_ph_seq"], PPPOS=data["person_pppos"], age=data["age"],
        sex=data["sex"], generation=np.array(CT.GENS)[data["generation"]], counted_weight=weight,
        coverage_weight=missing))
    CT.require(not frame.duplicated(["PH_SEQ", "PPPOS"]).any(), "duplicate v9 source donor identity")
    verify(required)
    destination, receipt_path = CT.paths("oct16", basis)
    frame.to_csv(destination, index=False, lineterminator="\n", float_format="%.17g")
    sources = [Path(__file__), CT.COVERAGE / "coverage_oct16.py", CT.COVERAGE / "coverage_bound.py",
        CT.COVERAGE / "source_tables.py", source.FISCAL / "count_composition_r5_2026_10_15/measure.py",
        source.FISCAL / "count_composition_r5_2026_10_15/tenure.py",
        source.FISCAL / "count_composition_r5_2026_10_15/derived/native_person_factors.parquet",
        source.FISCAL / "main_case_2026_10_16/derived/corrections.json",
        CT.COVERAGE / f"derived/pricing_audit_oct15_final_routing_{basis}.json",
        CT.COVERAGE / f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json",
        CT.COVERAGE / f"_cache/oct15_final_routing/{basis}/pricing.npz"]
    sources = set(sources) | required
    receipt = dict(case="oct16", basis=basis, scenario="central_joint16_17", rule="source_fixed_count_tenure_on_calibrated_record_weights",
        source_hashes={str(p.relative_to(CT.ROOT)): CT.digest(p) for p in sorted(sources)},
        donor_csv_sha256=CT.digest(destination), rows=len(frame), missing_people={g.replace("G3plus", "G3+"): n for g, n in observed.items()},
        economic_assumption="Each economic component follows the source's joint16/17 donor distribution; signed weights retained. Fiscal typed line dollars are independently consumed from the exact case payload, not inferred from generation-average donor prices.",
        gates=dict(counts_close=True, fiscal_source="exact case typed parts, not donor scalar price"))
    receipt_path.write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    print("v9 joint donor physical_peak_bytes=" + str(require_within_budget("world v9 joint donors")))
    return receipt


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", choices=("oct16",), default="oct16")
    parser.add_argument("--basis", choices=("cash", "set"), default="cash")
    args = parser.parse_args()
    print(json.dumps(export(args.basis), indent=1))
