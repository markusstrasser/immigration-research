#!/usr/bin/env python3
"""Parse frozen NIPA subsidy programs; price explicit full-response sensitivities.

All source amounts are parsed. Program definitions and industry assignments are
assumptions. The unclassified residual is retained rather than assigned a false
program identity. The primary SUT is diagnostic only: its vintage is newer.
"""
from __future__ import annotations

import csv
import hashlib
import io
import json
import resource
import subprocess
import time
import zipfile
from pathlib import Path

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = HERE.parent
OUT = HERE / "derived"
CACHE = HERE / "_cache"
PINS = HERE / "inputs/k5_pins.json"


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def write_csv(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def table(book, sheet):
    rows = list(book[sheet].values)
    head = next(i for i, r in enumerate(rows) if r[0] == "Line")
    j = list(rows[head]).index("2024")
    title = " ".join(str(v) for r in rows[:head] for v in r if v is not None)
    assert "Millions of dollars" in title, "[BLOCKED] source units changed"
    out = {}
    for r in rows[head + 1:]:
        if r[0] is not None and str(r[0]).isdigit():
            label = str(r[1]).strip().split("\\")[0]
            assert isinstance(r[j], (float, int)), f"[BLOCKED] {sheet} {r[0]} not numeric"
            out[int(r[0])] = {"label": label, "series": str(r[2]), "national_bn": float(r[j]) / 1000}
    return out, rows


def main():
    start = time.perf_counter()
    pins = json.loads(PINS.read_text())
    files = {}
    for name, entry in pins.items():
        p = REPO / entry["path"]
        assert sha(p) == entry["sha256"], f"[BLOCKED] stale K5 source {name}"
        files[name] = p
    gates = []

    def gate(name, ok, value=None):
        gates.append({"name": name, "passed": bool(ok), "value": value})
        assert ok, f"[BLOCKED] {name}: {value}"

    book = openpyxl.load_workbook(files["nipa"], read_only=True, data_only=True)
    t13, raw13 = table(book, "T31300-A")
    t17, _ = table(book, "T31700-A")
    expected = {1: "Subsidies", 2: "Federal", 3: "Agricultural", 4: "Housing", 5: "Maritime", 6: "Air carriers", 7: "Other", 8: "State and local"}
    gate("NIPA 3.13 labels exact", all(t13[n]["label"] == label for n, label in expected.items()))
    amount = lambda n: t13[n]["national_bn"]
    gate("NIPA program components close to federal at 1e-6bn", abs(sum(amount(n) for n in range(3, 8)) - amount(2)) < 1e-6)
    gate("NIPA government components close at 1e-6bn", abs(amount(2) + amount(8) - amount(1)) < 1e-6)
    model = json.loads(files["model"].read_text())
    model_lines = {r["id"]: r["national_bn"] for r in model["spending"]["lines"]}
    programs = [
        (3, "agricultural_subsidies", "111CA", 0, "Fixed land and world-priced commodities; replacement workers under full adjustment."),
        (4, "housing_subsidies", "existing_housing_support", 1, "Already carried at response 1 by the case; excluded from K5."),
        (5, "transport_subsidies", "483", None, "Maritime program; full response is a sensitivity, route/security spending may remain."),
        (6, "transport_subsidies", "481", None, "Air-carrier program; full response is a sensitivity, fixed routes may remain."),
        (7, "other_subsidies", "unidentified", None, "Mixed rail, transit, crop insurance and other programs; needs split and enterprise offset."),
        (8, "other_subsidies", "482_proxy", None, "Primarily railroad payments in MP-5; current vintage and enterprise recipients not separately identified."),
    ]
    rows = []
    for n, line, key, response, reason in programs:
        rows.append({"source_table": "3.13", "source_line": n, "source_series": t13[n]["series"], "program": t13[n]["label"],
                     "national_bn": amount(n), "case_line": line, "candidate_key": key, "recommended_response": "WITHHOLD" if response is None else response,
                     "reason": reason})
    for line in sorted({r["case_line"] for r in rows}):
        a = sum(r["national_bn"] for r in rows if r["case_line"] == line)
        gate(f"{line} reproduces frozen national at 1e-6bn", abs(a - model_lines[line]) < 1e-6, a)
    nonhousing = amount(1) - amount(4)
    gate("nonhousing programs close at 1e-6bn", abs(sum(r["national_bn"] for r in rows if r["source_line"] != 4) - nonhousing) < 1e-6)
    footnote = next(str(r[0]) for r in raw13 if r[0] is not None and str(r[0]).startswith("1."))
    gate("Federal Other footnote identifies crop insurance and rail/transit", all(s in footnote for s in ["railroads", "mass transit", "FCIC"]))

    # Functional definitions differ from the program definitions. Preserve both;
    # never splice their agricultural or housing lines into a pseudo-program.
    functional = [{"source_table": "3.17", "source_line": n, **t17[n]} for n in range(78, 105)]
    gate("NIPA 3.17 total matches 3.13 at 1e-6bn", abs(t17[78]["national_bn"] - amount(1)) < 1e-6)
    leaves = [81, 83, 84, 85, 86, 87, 88, 79]
    rounding = amount(1) - sum(t17[n]["national_bn"] for n in leaves)
    functional.append({"source_table": "3.17", "source_line": "rounding", "label": "Published functional rounding remainder", "series": "CALCULATION", "national_bn": rounding})
    gate("functional leaf amounts plus explicit rounding close at 1e-6bn", abs(sum(t17[n]["national_bn"] for n in leaves) + rounding - amount(1)) < 1e-6)

    with zipfile.ZipFile(files["sut"]) as z:
        use = openpyxl.load_workbook(io.BytesIO(z.read("Use_Summary.xlsx")), read_only=True, data_only=True)
    use_rows = list(use["2024"].values)
    codes = list(use_rows[5])
    end = codes.index("T001")
    sut_rows = []
    for r in use_rows:
        if r[0] not in ["T00OSUB", "T00SUB"]:
            continue
        gate(f"SUT {r[0]} title", "subsidies" in str(r[1]).lower())
        vals = [float(v) / 1000 if isinstance(v, (float, int)) else 0.0 for v in r[2:end]]
        rounded_total = float(r[end]) / 1000
        # Industry cells are independently rounded to $mn. The residual remains
        # explicit, so exact closure is never obtained by weakening tolerance.
        residual = rounded_total - sum(vals)
        for code, a in zip(codes[2:end], vals):
            sut_rows.append({"source_row": r[0], "cell": str(code), "national_bn": a})
        sut_rows.append({"source_row": r[0], "cell": "ROUNDING", "national_bn": residual})
        gate(f"SUT {r[0]} cells plus rounding close at 1e-6bn", abs(sum(x["national_bn"] for x in sut_rows if x["source_row"] == r[0]) - rounded_total) < 1e-6)

    core = json.loads((OUT / "core.json").read_text())
    gate("frozen positive control and weight-conservation gates passed", all(g["passed"] for g in core["gates"]))
    npz = np.load(CACHE / "core.npz", allow_pickle=False)
    cells = list(npz["cells"])
    results = {}
    vectors = {}
    vector = lambda: np.zeros(len(cells))
    v = vector()
    v[cells.index("483")] = amount(5)
    v[cells.index("481")] = amount(6)
    vectors["named_transport_full_response"] = v
    v = vector()
    v[cells.index("482")] = amount(8)
    vectors["state_local_railroad_proxy_full_response"] = v
    national_wages = npz["size_wages_national"].sum(axis=1)[:, 0]
    v = (amount(7) + amount(8)) * national_wages / national_wages.sum()
    vectors["unclassified_residual_plain_wage_full_response"] = v
    vectors["all_nonfarm_nonhousing_plain_wage_full_response"] = vectors["named_transport_full_response"] + v
    # Functional-mix proxy: preserve 3.17's functional definitions as a distinct
    # sensitivity. Housing/community's excess over 3.13 housing is community
    # support by assumption, not an identified program. Crop support remains 0.
    functional_vector = vector()

    def wage_pool(group_cells, national_amount):
        idx = [cells.index(c) for c in group_cells]
        weights = national_wages[idx]
        v = vector()
        v[idx] = national_amount * weights / weights.sum()
        gate("functional wage-pool national closure at 1e-6bn", abs(v.sum() - national_amount) < 1e-6, national_amount)
        return v

    private = [c for c in cells if c not in ["RESIDENTIAL", "NOIND", "GOVF", "GOVSL", "HH814"]]
    for selected, amt in [(["481", "482", "483", "484", "485", "486", "487OS", "493"], t17[81]["national_bn"]),
                          (private, t17[83]["national_bn"]),
                          (["22"], t17[85]["national_bn"]),
                          (["23", "ORE", "624"], t17[87]["national_bn"] - amount(4)),
                          (["621", "622", "623", "624"], t17[88]["national_bn"])]:
        functional_vector += wage_pool(selected, amt)
    vectors["functional_mix_full_response_proxy"] = functional_vector
    gate("functional responding total closes at 1e-6bn", abs(functional_vector.sum() - (nonhousing - t17[84]["national_bn"] - rounding)) < 1e-6)
    engine_probe = """const fs=require('fs'); const E=require(process.argv[1]);
const m=JSON.parse(fs.readFileSync(process.argv[2])); const s=E.defaultState(m);
s.response_override.transport_subsidies=0; const a=E.evaluate(m,s);
s.response_override.transport_subsidies=1; const b=E.evaluate(m,s);
const t=b.spending.find(x=>x.id==='transport_subsidies').amount_bn;
console.log(JSON.stringify({welfare_move:b.welfare_bn-a.welfare_bn,target_bn:t}));"""
    epath = FISCAL / "assumption_explorer_2026_09_21/engine.js"
    sign = json.loads(subprocess.run(["node", "-e", engine_probe, str(epath), str(files["model"])], check=True, capture_output=True, text=True).stdout)
    gate("engine spending response0 to1 raises modeled cost by target amount at 1e-9bn", abs(sign["welfare_move"] + sign["target_bn"]) < 1e-9 and sign["target_bn"] > 0, sign)
    changes = {}
    plain_share = {g: npz[f"size_wages_{g}"].sum(axis=(0, 1)) / npz["size_wages_national"].sum(axis=(0, 1))
                   for g in ["union", "G1", "G2", "G3plus", "white"]}
    for name, v in vectors.items():
        gate(f"{name} finite nonnegative vector", bool(np.isfinite(v).all() and (v >= 0).all()))
        target = {g: npz[f"shares_{g}"].T @ v for g in ["union", "G1", "G2", "G3plus", "white"]}
        if name == "unclassified_residual_plain_wage_full_response":
            target = {g: plain_share[g] * (amount(7) + amount(8)) for g in target}
        if name == "all_nonfarm_nonhousing_plain_wage_full_response":
            target = {g: plain_share[g] * (amount(7) + amount(8)) + npz[f"shares_{g}"].T @ vectors["named_transport_full_response"] for g in target}
        gate(f"{name} generations close in all 161 replicates at 1e-9bn", float(np.max(np.abs(target["union"] - sum(target[g] for g in ["G1", "G2", "G3plus"])))) < 1e-9)
        union = target["union"]
        lineage = union + sum(core["lineage_rates"][g] * target[g] for g in core["lineage_rates"])
        changes[f"{name}__union"] = union
        changes[f"{name}__lineage"] = lineage
        for g in ["G1", "G2", "G3plus", "white"]:
            changes[f"{name}__{g}"] = target[g]
        changes[f"{name}__others_resource_cost_change_on_removal_union"] = -union
        changes[f"{name}__others_resource_cost_change_on_removal_lineage"] = -lineage
        se = lambda a: float(np.sqrt(4 / 160 * np.square(a[1:] - a[0]).sum()))
        results[name] = {"union_delta_bn": float(union[0]), "union_se_bn": se(union), "lineage_delta_bn": float(lineage[0]),
                         "lineage_conditional_se_bn": se(lineage), "national_bn": float(v.sum()), "response_low": 1, "response_high": 1,
                         "recommended": False, "status": "Gross-spending sensitivity; unresolved program composition/enterprise offsets. Same move at both ends, set and cash."}
    out_vectors = [{"arm": name, "cell": c, "national_bn": float(v[i]), "response_low": 1, "response_high": 1} for name, v in vectors.items() for i, c in enumerate(cells)]
    sut_total = sum(x["national_bn"] for x in sut_rows)
    summary = {"recommendation": "Keep agricultural subsidies at zero. Withhold the remaining K5 point revision until program identities and enterprise subsidy receipts are reconciled.",
               "scope": "Both personal endpoints; identified union and v7 lineage using frozen ancestry wage factors. National/lineage factors fixed for replicate SEs.",
               "national_bn": {"all_subsidies": amount(1), "housing_excluded": amount(4), "nonhousing": nonhousing,
                               "agricultural_fixed": amount(3), "unclassified_residual": amount(7) + amount(8)},
               "source_note": footnote, "functional_rounding_bn": rounding,
               "definition_conflicts_bn": {"agricultural_program_minus_function": amount(3) - t17[84]["national_bn"], "housing_function_minus_program": t17[87]["national_bn"] - amount(4)},
               "sut_newer_vintage_total_bn": sut_total, "sut_minus_frozen_nipa_bn": sut_total - amount(1),
               "plain_key_contract": "Plain-wage arms use each replicate's total corrected wages divided by total national wages directly; the diagnostic national vector is not an instruction to apply pooled cell shares. Read k5_changes.npz for exact changes.",
               "arms": results, "gates": gates,
               "offset": "Enterprise surplus already responds at 1 and includes subsidies from other government levels. Gross subsidy spending must be paired with its enterprise subsidy receipt to avoid counting an internal transfer as a net resource saving.",
               "excluded": "Housing assistance already in case; capital investment grants, tax expenditures classified as negative taxes, business current transfers and benefits classified as social transfers are outside NIPA current subsidies."}
    for n, rows_out in [("k5_programs.csv", rows), ("k5_functions.csv", functional), ("k5_sut_subsidies.csv", sut_rows), ("k5_vectors.csv", out_vectors)]:
        write_csv(OUT / n, rows_out)
    np.savez(CACHE / "k5_changes.npz", **changes)
    metric = {"elapsed_s": time.perf_counter() - start, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    gate("peak RSS below 2.5GB", metric["peak_rss_bytes"] < 2.5e9)
    (OUT / "k5_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    (CACHE / "k5_runtime.json").write_text(json.dumps(metric) + "\n")
    print(json.dumps({"arms": results, "runtime": metric, "gates": len(gates)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
