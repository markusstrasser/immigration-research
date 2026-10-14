#!/usr/bin/env python3
"""Price SUT 2024 subsidy cells with exact frozen pooled keys, not tax subtraction.

National SUT totals are a newer vintage than the frozen NIPA spending account.
All results are response sensitivities, not additional national expenditure.
"""
from __future__ import annotations

import csv
import io
import json
import resource
import subprocess
import sys
import time
import zipfile
from pathlib import Path

import numpy as np
import openpyxl

sys.dont_write_bytecode = True
from core import CACHE, DERIVED, FISCAL, HERE, digest

REPO = FISCAL.parents[1]
PINS = HERE / "inputs/k5_cells_pins.json"
GROUPS = ("union", "G1", "G2", "G3plus", "white")


def se(v):
    return float(np.sqrt(4 / 160 * np.square(v[1:] - v[0]).sum()))


def parse_sut(path):
    with zipfile.ZipFile(path) as z:
        book = openpyxl.load_workbook(io.BytesIO(z.read("Use_Summary.xlsx")), read_only=True, data_only=True)
    rows = list(book["2024"].values)
    if rows[1][0] != "(Millions of dollars)" or rows[3][0] != "2024":
        raise RuntimeError("[BLOCKED] SUT year or units changed")
    codes = list(rows[5])
    stop = codes.index("T001")
    parsed = []
    totals = {}
    for row_code, label in (("T00SUB", "Less: Subsidies on products"), ("T00OSUB", "Less: Other subsidies on production")):
        r = next(r for r in rows if r[0] == row_code)
        if r[1] != label:
            raise RuntimeError(f"[BLOCKED] SUT label changed: {row_code}")
        vals = [float(v) / 1000 if isinstance(v, (float, int)) else 0.0 for v in r[2:stop]]
        totals[row_code] = float(r[stop]) / 1000
        parsed.extend({"source_row": row_code, "cell": str(c), "national_bn": v} for c, v in zip(codes[2:stop], vals))
        parsed.append({"source_row": row_code, "cell": "ROUNDING", "national_bn": totals[row_code] - sum(vals)})
    book.close()
    return parsed, totals


def mapped_vector(rows, cells, agriculture_response=1, include_624=True, include_ore=True):
    """SUT private cells only; housing and government enterprises remain separate."""
    v = np.zeros(len(cells))
    for row in rows:
        cell = row["cell"]
        if cell == "525":
            cell = "523"  # Frozen job-capital concordance; both subsidy rows are zero.
        if cell not in cells or (cell == "624" and not include_624) or (cell == "ORE" and not include_ore):
            continue
        v[cells.index(cell)] += row["national_bn"] * (agriculture_response if cell == "111CA" else 1)
    return v


def csv_write(path, rows):
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def main():
    start = time.perf_counter()
    paths = {
        "sut": CACHE / "k4_bea_supply_use.zip", "core_arrays": CACHE / "core.npz",
        "core_record": DERIVED / "core.json", "model": FISCAL / "assumption_explorer_2026_09_21/derived/model.json",
        "spending_partition": FISCAL / "full_account_spending_2026_09_20/builder.py",
        "maincase_payload": FISCAL / "main_case_2026_10_14/derived/corrections.json",
        "maincase_package": FISCAL / "main_case_2026_10_14/package.cjs",
        "engine": FISCAL / "assumption_explorer_2026_09_21/engine.js",
        "nipa": REPO / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx",
    }
    pins = {k: {"path": str(p.relative_to(REPO)), "sha256": digest(p)} for k, p in paths.items()}
    pins["sut"]["url"] = "https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip"
    if PINS.exists() and json.loads(PINS.read_text()) != pins:
        raise RuntimeError("[BLOCKED] K5 cell source pin changed")
    if not PINS.exists():
        PINS.write_text(json.dumps(pins, indent=2) + "\n")
    core = json.loads(paths["core_record"].read_text())
    if not all(g["passed"] for g in core["gates"]):
        raise RuntimeError("[BLOCKED] core positive control failed")
    c = np.load(paths["core_arrays"], allow_pickle=False)
    cells = list(c["cells"])
    rows, totals = parse_sut(paths["sut"])
    gates = []

    def gate(name, ok, value=None):
        gates.append({"name": name, "passed": bool(ok), "value": value})
        if not ok:
            raise RuntimeError(f"[BLOCKED] {name}: {value}")

    for code, total in totals.items():
        gap = sum(r["national_bn"] for r in rows if r["source_row"] == code) - total
        gate(f"{code} national cells plus explicit rounding close at 1e-6bn", abs(gap) <= 1e-6, gap)
    trace_js = """const P=require(process.argv[1]); const out=[];
    for(const method of P.METHODS) for(const index of [16,11]) {
      const m=P.modelFor('central',method,P.withCentral({}));
      const r=P.evaluateFull(m,P.MAIN_SPECS[index],P.MAIN_PROFILE);
      const sp=JSON.parse(JSON.stringify(P.MAIN_SPECS[index]));
      sp.line_responses.transport_subsidies=1;
      const changed=P.evaluateFull(m,sp,P.MAIN_PROFILE);
      out.push({method,index,sign_probe_delta_cost_bn:changed.cost_bn-r.cost_bn,lines:r.evaluation.spending.filter(x=>x.id.includes('subsid')||['other_federal_benefits','other_state_welfare','family_and_general_assistance'].includes(x.id))});
    } console.log(JSON.stringify(out));"""
    trace = json.loads(subprocess.run(["node", "-e", trace_js, str(paths["maincase_package"])], check=True, capture_output=True, text=True).stdout)
    gate("live nonhousing subsidy lines all respond at zero at both personal ends", all(r["response"] == 0 for e in trace for r in e["lines"] if r["id"] in ("agricultural_subsidies", "transport_subsidies", "other_subsidies")))
    gate("live housing and possible nonprofit-benefit carriers respond at one", all(r["response"] == 1 for e in trace for r in e["lines"] if r["id"] in ("housing_subsidies", "other_federal_benefits", "other_state_welfare", "family_and_general_assistance")))
    gate("live spending response0 to1 raises net cost by line amount at 1e-9bn", all(abs(e["sign_probe_delta_cost_bn"] - next(r["amount_bn"] for r in e["lines"] if r["id"] == "transport_subsidies")) < 1e-9 for e in trace))
    records, vectors, rep_rows, arms = [], [], [], {}
    for agriculture in (1, 0):
        for social in (True, False):
            for ore in (True, False):
                name = f"ag{agriculture}_624{'included' if social else 'excluded'}_ore{'included' if ore else 'excluded'}"
                v = mapped_vector(rows, cells, agriculture, social, ore)
                parts = {g: c[f"shares_{g}"].T @ v for g in GROUPS}
                gate(f"{name} generations close in all 161 replicates at 1e-9bn", np.max(abs(parts["union"] - sum(parts[g] for g in ("G1", "G2", "G3plus")))) < 1e-9)
                parts["lineage"] = parts["union"] + sum(core["lineage_rates"][g] * parts[g] for g in core["lineage_rates"])
                arms[name] = {"responding_national_bn": float(v.sum()), "recommendation": "arm", "response_low": 1, "response_high": 1}
                for g, a in parts.items():
                    gate(f"{name} {g} finite 161 replicates", a.shape == (161,) and np.isfinite(a).all())
                    arms[name][g] = {"delta_net_cost_bn": float(a[0]), "conditional_se_bn": se(a)}
                    records.append({"arm": name, "population": g, **arms[name][g], "low_delta_net_cost_bn": float(a[0]), "high_delta_net_cost_bn": float(a[0])})
                    rep_rows.extend({"arm": name, "population": g, "replicate": i, "delta_net_cost_bn": float(x)} for i, x in enumerate(a))
                vectors.extend({"arm": name, "cell": str(cell), "responding_national_bn": float(v[i])} for i, cell in enumerate(cells))
    keyed_rows = []
    for row in rows:
        cell = row["cell"]
        included = cell in cells
        record = {**row, "mapping_status": "private job cell" if included else "excluded housing/enterprise/rounding; no silent wage key"}
        for g in ("union", "G3plus", "white"):
            record[f"{g}_pooled_share"] = float(c[f"shares_{g}"][cells.index(cell), 0]) if included else 0.0
            record[f"{g}_keyed_bn"] = record[f"{g}_pooled_share"] * row["national_bn"]
        record["lineage_keyed_bn"] = record["union_keyed_bn"] + sum(core["lineage_rates"][g] * record[f"{g}_keyed_bn"] for g in core["lineage_rates"])
        keyed_rows.append(record)
    model = json.loads(paths["model"].read_text())
    national = {r["id"]: r["national_bn"] for r in model["spending"]["lines"] if r["family"] == "subsidies"}
    summary = {
        "recommendation": "Keep as arms. SUT cells identify recipient industries, not response elasticities or the program/enterprise/nonprofit overlap. Agriculture stays at 0 under the reserve premise. Do not add another national spending line or subtract subsidies from corporate tax.",
        "scope": "Exact core pooled personal cell shares, all 161 CPS replicates, live lineage G3plus/white wage rates held fixed. Same cost move at both v7 personal ends, set and cash.",
        "sut_totals_bn": totals, "sut_sum_bn": sum(totals.values()), "frozen_nipa_subsidy_lines_bn": national,
        "sut_minus_frozen_nipa_bn": sum(totals.values()) - sum(national.values()),
        "overlap_status": "624 is not a separately named case line. Complete NIPA subsidies are already partitioned into four spending lines (nonhousing response0); social benefits separately include nonprofit payments and respond1. Industry 624 alone does not establish a duplicate: include/exclude624 arms bracket the claimed overlap, not an observed reconciliation. ORE included/excluded is a separate housing-program ambiguity.",
        "live_case_trace": trace, "lineage_rates": core["lineage_rates"], "arms": arms, "gates": gates,
        "excluded_cells": "HS housing, GFE/GSLE government enterprises, general government and explicit rounding have no private-job key. Their already priced housing/enterprise carriers are retained; new gross subsidy charges there would need matched offsets.",
        "source_urls": ["https://apps.bea.gov/industry/release/zip/SUPPLY-USE.zip", "https://www.bea.gov/help/faq/1408", "https://apps.bea.gov/scb/issues/2022/11-november/1122-nea-annual-update.htm"],
    }
    csv_write(DERIVED / "k5_cells_source.csv", keyed_rows)
    csv_write(DERIVED / "k5_cells_arms.csv", records)
    csv_write(DERIVED / "k5_cells_vectors.csv", vectors)
    csv_write(DERIVED / "k5_cells_replicates.csv", rep_rows)
    runtime = {"elapsed_s": time.perf_counter() - start, "peak_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    gate("RSS below 2.5GB", runtime["peak_rss_bytes"] < 2.5e9, runtime["peak_rss_bytes"])
    # Timing/RSS are reported, not written into reproducible scientific bytes.
    gates[-1].pop("value")
    (DERIVED / "k5_cells_summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({"arms": arms, "runtime": runtime, "gates": len(gates)}, indent=2))


if __name__ == "__main__":
    main()
