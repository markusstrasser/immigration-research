"""Observed reporter NAS(b) destinations on the lane's actual seven G1 cells.

Only new reporter rows are exported. Original P7 parent assignments stay frozen.
All three arrival readings use the same pinned raw CPS and completed union.
"""
from __future__ import annotations

import hashlib
import json
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import frame as F

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget


def sha(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def build():
    measurement = HERE.parent / "generation_account_2026_09_24/inputs/minor_parent_measurement_oct15.json"
    case = HERE.parent / "main_case_2026_10_15/derived/corrections.json"
    sources = [Path(__file__), HERE / "frame.py", Path(F.C.__file__), measurement, case, F.CPS_ZIP]
    hashes = {str(p): sha(p) for p in sources}
    if hashes[str(F.CPS_ZIP)] != F.CPS_SHA:
        raise ValueError("[BLOCKED] unreviewed raw CPS source")
    measured = json.loads(measurement.read_text())["reporter_assignment_b"]
    observed = json.loads(case.read_text())["meta"]["union_completion"]["observed_records"]
    fields = ["PH_SEQ", "PPPOS", "SPM_ID", "PRPERTYP", "A_AGE", "PRCITSHP", "PENATVTY",
              "PEMNTVTY", "PEFNTVTY", "PRDTHSP", "PEINUSYR", "A_LINENO", "PEPAR1", "PEPAR2", "PF_SEQ"]
    with zipfile.ZipFile(F.CPS_ZIP) as archive:
        data = pd.read_csv(archive.open("pppub25.csv"), usecols=fields)
    data = data.sort_values(["SPM_ID", "PPPOS"]).reset_index(drop=True)
    lookup = {(int(r.PH_SEQ), int(r.PPPOS)): i for i, r in enumerate(data.itertuples())}
    if len(lookup) != len(data):
        raise ValueError("[BLOCKED] duplicate source person identity")
    civilian, union, canonical = F.masks(data)
    expanded = union.copy()
    for record in observed:
        row = lookup[(record["PH_SEQ"], record["PPPOS"])]
        if union[row] or not civilian[row] or data.A_AGE.iloc[row] != record["age"]:
            raise ValueError("[BLOCKED] completion identity/universe differs")
        expanded[row] = True
    indices = [lookup[(r["PH_SEQ"], r["PPPOS"])] for r in measured]
    if len(indices) != len(set(indices)):
        raise ValueError("[BLOCKED] duplicate reporter identity")
    readings = {}
    for reading in ("central", "lower", "upper"):
        generations = {**F.g1_cells(data, np.logical_or.reduce([canonical[g] for g in F.G1_CELLS]), reading),
                       "G2": canonical["G2"], "G3plus": canonical["G3plus"] | (expanded & ~union)}
        omega, rules, _ = F.assignments(data, civilian, expanded, generations)
        records = []
        for source, index in zip(measured, indices, strict=True):
            fine = omega["b"][index]
            aggregate = [fine[:7].sum(), fine[7], fine[8]]
            if not np.allclose(aggregate, source["omega"], atol=1e-12, rtol=0) or rules[index] != source["rule"]:
                raise ValueError("[BLOCKED] fine reporter route disagrees with principal completed NAS(b)")
            records.append(dict(PH_SEQ=source["PH_SEQ"], PPPOS=source["PPPOS"],
                                people=source["people"], A_AGE=source["A_AGE"],
                                omega_b=dict(zip(F.GENS, fine.tolist(), strict=True)), rule=str(rules[index])))
        readings[reading] = records
    if any(sha(p) != hashes[str(p)] for p in sources):
        raise ValueError("[BLOCKED] fine-route source changed during measurement")
    require_within_budget("observed reporter fine arrival routes")
    return dict(version=1, rule="Exact completed NAS(b) for new reporter rows only; original P7 union mapping frozen",
                source_sha256=hashes, generations=F.GENS, readings=readings)


def main():
    result = build()
    output = HERE / "_cache/reporter_fine_oct15.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(f"PASS: {len(result['readings']['central'])} exact reporter routes, three arrival readings")


if __name__ == "__main__":
    main()
