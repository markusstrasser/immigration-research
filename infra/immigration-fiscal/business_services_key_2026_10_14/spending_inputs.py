#!/usr/bin/env python3
"""Parse the case-vintage BEA public-safety functional shares, keeping budgets fixed.
Default offline. Copies existing pinned primary input into this lane, never redownloads.
"""
from pathlib import Path
import hashlib
import json
import shutil
import time
import resource
import openpyxl

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
EXPECTED = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"


def main():
    start = time.perf_counter()
    source = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
    cache = HERE / "_cache/Section3All_xls.xlsx"
    cache.parent.mkdir(exist_ok=True)
    if not cache.exists():
        shutil.copyfile(source, cache)
    actual = hashlib.sha256(cache.read_bytes()).hexdigest()
    if actual != EXPECTED:
        raise RuntimeError("[BLOCKED] BEA case-vintage primary hash changed")
    wb = openpyxl.load_workbook(cache, read_only=True, data_only=True)
    rows = list(wb["T31600-A"].iter_rows(values_only=True))
    column = list(rows[7]).index("2024")
    lines = {str(r[0]): (str(r[1]).strip(), float(r[column])) for r in rows if r[0] and str(r[0]).isdigit()}
    expected = {"8": "Public order and safety", "9": "Police", "10": "Fire", "11": "Law courts", "12": "Prisons"}
    for line, label in expected.items():
        if lines[line][0] != label:
            raise RuntimeError(f"[BLOCKED] BEA label {line}")
    total = lines["8"][1]
    fractions = {label: lines[line][1] / total for line, label in expected.items() if line != "8"}
    if abs(sum(fractions.values()) - 1) > 1e-12:
        raise RuntimeError("[BLOCKED] BEA subfunctions do not close")
    cj = json.loads((HERE.parent / "cj_use_allocation_2026_09_23/derived/summary.json").read_text())
    # Border enforcement and custody are not commercial protection. Preserve the existing carve-out.
    excluded = cj["cbp"]["cbp_751_excl_invest_bn"] + cj["ice"]["custody_outlays_bn"]
    oracle = cj["sublines_bn"]
    for label, key in [("Police", "police"), ("Fire", "fire"), ("Law courts", "law_courts"), ("Prisons", "prisons")]:
        if abs(fractions[label] * cj["line4_bn"] - oracle[key]) > 1e-9:
            raise RuntimeError(f"[BLOCKED] existing CJ subline positive control {label}")
    out = {"source": "BEA NIPA Table 3.16, 2024 case vintage", "fractions": fractions,
           "subline_millions": {label: lines[line][1] for line, label in expected.items()},
           "excluded_border_and_custody_bn": excluded,
           "police_protective_fraction": 0.5,
           "police_protective_fraction_status": "ASSUMPTION: inherited police half-arrests half-population split; not empirically measured",
           "gates": {"primary_hash": True, "subfunction_closure_1e_12": True, "cj_positive_control_1e_9_bn": True}}
    (HERE / "inputs/spending_shares.json").write_text(json.dumps(out, indent=2, sort_keys=True) + "\n")
    pins = {"Section3All_xls.xlsx": {"path": str(cache.relative_to(HERE)), "sha256": actual,
             "url": "https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx"}}
    (HERE / "inputs/spending_pins.json").write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    print(f"PASS national share closure and existing lane control; seconds={time.perf_counter()-start:.3f}; maxrss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
