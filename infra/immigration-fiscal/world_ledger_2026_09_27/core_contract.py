"""Oct15 core incidence and stage-input contract, before full-world dependencies."""
import hashlib
import json
import sys
from pathlib import Path

import pandas as pd
import valuation as V


def main():
    V.require_pins("oct15", "generation", "main_case")
    record = json.loads((V.HERE / "inputs/oct15_source_hashes.json").read_text())
    V.gate("explicit_core_snapshot", record["case"] == "oct15" and record["provenance"] == "[WORKTREE INPUT]")
    for rel, expected in record["sha256"].items():
        V.gate(f"snapshot_{rel}", hashlib.sha256((V.REPO / rel).read_bytes()).hexdigest() == expected)
    payload = V.case_payload("oct15")
    V.ITEM_CLASS.update({f"capital_{c['id']}": V.LINE_CLASS[f"capital_{c['of_component']}"]
                        for c in payload["meta"]["capital_return"]["components"] if c.get("of_component")})
    classes, payers = V.receipt_contract("oct15")
    declared = V.completion_incidence(payload, classes, payers)
    for key in ("oct15", "oct15_cash"):
        lines = pd.read_csv(V.DERIVED / f"generation_lines_{key}.csv")
        receipts = set(lines.loc[lines.side.eq("receipt"), "line"])
        V.gate(f"all_receipts_declared_{key}", receipts <= set(classes) and receipts <= set(payers),
               unknown=sorted(receipts - (set(classes) & set(payers))))
        carriers = set(lines.loc[lines.line.isin(declared), "line"])
        V.gate(f"all_completion_carriers_declared_{key}", carriers == set(declared))
        V.gate(f"post_engine_rows_{key}", set(lines.loc[lines.side.eq("post_engine"), "line"]) == {"mixed_unit_removal", "coverage"})
    out = dict(case="oct15", provenance="[COMMITTED INPUT]", pins=V.PINS["oct15"], receipts={line: dict(incidence_class=classes[line], economic_payer=payers[line])
                for line in sorted(receipts)}, completion_carriers=declared)
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
    from memory_budget import require_within_budget
    print(f"core contract passes; footprint {require_within_budget('world core contract')} bytes")
    (V.DERIVED / "core_incidence_oct15.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
