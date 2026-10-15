#!/usr/bin/env python3
"""Item 14: measured BEA blocks, row-4 caseloads, explicit incomplete bridge.

Default emits a DEGRADED partial conditional item: only the source-defined federal
retirement block is rekeyed. Its consumption mass uses proportional C/GI, which is
an assumption. --require-complete blocks because a program-complete measured
consumption bridge is unavailable. No budget-total or agency-expense fallback.
Run: uv run --no-project python3 <lane>/income_security.py
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import time
import zipfile

sys.dont_write_bytecode = True

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
BEA = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
BEA_SHA = "69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
MEDICAID = HERE / "_cache/admin/financial-management-report-fy2024.zip"


def sha(path):
    h = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def require(ok, message):
    if not ok:
        raise ValueError(f"[BLOCKED] {message}")


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def bea_measurements(path=BEA):
    require(sha(path) == BEA_SHA, "BEA case vintage changed")
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables = {}
    for name in ["T31505-A", "T31600-A", "T31700-A", "T31200-A"]:
        rows = list(book[name].values)
        require(rows[1][0] == "[Millions of dollars]", f"{name} units")
        headers = [row for row in rows if row[0] == "Line"]
        require(len(headers) == 1, f"{name} header")
        column = [i for i, value in enumerate(headers[0]) if str(value) == "2024"]
        require(len(column) == 1, f"{name} year")
        tables[name] = {int(row[0]): {"label": row[1].strip(), "million": row[column[0]]}
                        for row in rows if str(row[0]).isdigit()}
    book.close()
    c, g, x, b = (tables[name] for name in ["T31700-A", "T31505-A", "T31600-A", "T31200-A"])
    require(c[10]["million"] == 167818 and c[20]["million"] == 30536
            and c[31]["million"] == 137281, "consumption anchors")
    federal = {label: g[line]["million"] / 1000 for label, line in
               [("disability", 73), ("retirement", 74), ("welfare_and_social_services", 75),
                ("unemployment", 76), ("other", 77)]}
    state_local = {label: g[line]["million"] / 1000 for label, line in
                   [("disability", 116), ("welfare_and_social_services", 117)]}
    require(abs(sum(federal.values()) - g[72]["million"] / 1000) < 1e-12, "federal C+GI closes")
    require(abs(sum(state_local.values()) - g[115]["million"] / 1000) < 1e-12, "S&L C+GI closes")
    require("Retirement" in g[74]["label"], "retirement label")
    # S&L income security has only disability and welfare. The subtraction is
    # recorded as a candidate accounting bridge, not proof of program workloads.
    sl_disability = (x[113]["million"] - b[28]["million"]) / 1000
    sl_welfare = c[31]["million"] / 1000 - sl_disability
    return {
        "consumption_bn": {"total": 167.818, "federal": 30.536, "state_local": 137.281,
                           "published_level_rounding": .001},
        "gross_investment_bn": {"total": c[114]["million"] / 1000,
                                "federal": c[124]["million"] / 1000,
                                "state_local": c[133]["million"] / 1000},
        "consumption_plus_gross_investment_bn": {"federal": federal, "state_local": state_local},
        "state_local_consumption_accounting_bridge_bn": {
            "disability": sl_disability, "welfare_and_social_services": sl_welfare,
            "status": "ACCOUNTING_BRIDGE_NOT_PROGRAM_WORKLOAD",
            "formula": "T3.16:113 minus T3.12:28; remainder of T3.17:31",
        },
        "retirement_scope": "T3.15.5 footnote 1: administering OASI and railroad retirement; employee pensions excluded",
        "source": {"path": str(path.relative_to(ROOT)), "sha256": BEA_SHA,
                   "url": "https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx",
                   "vintage": "published 2025-09-26; CY2024; file created 2026-08-25"},
    }


def caseload_keys():
    require(sha(CPS) == CPS_SHA, "CPS primary hash changed")
    spending = module("item14_spending", FISCAL / "full_account_spending_2026_09_20/builder.py")
    population = module("item14_population", FISCAL / "world_ledger_2026_09_27/population_basis.py")
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
              "PEMNTVTY", "PRDTHSP", "SPM_ID", "SS_VAL", "SSI_VAL", "PAW_VAL", "UC_VAL",
              "WC_VAL", "SPM_SNAPSUB", "MCAID"]
    with zipfile.ZipFile(CPS) as archive:
        d = pd.read_csv(archive.open("pppub25.csv"), usecols=fields)
        w = pd.read_csv(archive.open("asec_csv_repwgt_2025.csv"),
                        usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
    d = d.merge(w, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    require(not d.isna().any().any(), "missing CPS field or weight")
    civ, target = spending.canonical_target(d)
    d["civ"], d["target"], d["pw"] = civ, target, d.pwwgt0

    def gate(label, ok, **detail):
        require(ok, f"{label}: {detail}")

    d = population.reweight(d, CPS, gate, "row4")
    weights = d.pw.to_numpy(float)
    vectors = {key: d[field].gt(0).to_numpy(float) for key, field in
               [("social_security", "SS_VAL"), ("ssi", "SSI_VAL"),
                ("cash_assistance_caseload", "PAW_VAL"), ("unemployment", "UC_VAL"),
                ("workers_comp", "WC_VAL"), ("snap", "SPM_SNAPSUB")]}
    vectors.update(population=np.ones(len(d)), medicaid_covered=d.MCAID.eq(1).to_numpy(float),
                   cash_assistance=d.PAW_VAL.to_numpy(float))
    rows = {}
    for allocation in ["personal", "shared"]:
        out = {}
        for key, vector in vectors.items():
            # SNAP is SPM-unit exposure and Medicaid own coverage; keep their
            # established account scope. Shared cash programs spread own receipt.
            if allocation == "shared" and key not in ["population", "snap", "medicaid_covered"]:
                vector = spending.equal_unit_share(vector, d.SPM_ID)
            national = float(weights[civ] @ vector[civ])
            own = float(weights[target] @ vector[target])
            require(national > 0 and 0 <= own <= national, f"empty/invalid {key}")
            out[key] = {"national": national, "target": own, "share": own / national,
                        "national_positive_records": int(np.count_nonzero(civ & (vector > 0))),
                        "target_positive_records": int(np.count_nonzero(target & (vector > 0))),
                        "unit": "dollars" if key == "cash_assistance" else "positive_key_persons"}
        base = out["cash_assistance"]["share"]
        for value in out.values():
            value["ratio_to_current_cash_assistance"] = value["share"] / base
        rows[allocation] = out
    rows["scope"] = {"population_basis": "row4", "persons": float(weights[target].sum()),
                     "row4_source": {"path": population.ROW4_REL, "commit": population.ROW4_PIN,
                                     "factors": population.row4()["row4_factors"]},
                     "cps_sha256": CPS_SHA, "positive_key_persons_are":
                     "CPS reported recipient/exposure proxies; not administrative ethnic caseload counts",
                     "child_welfare_key": None,
                     "oasdi_caveat": "SS_VAL combines OASI and DI; no separately measured OASI/RR caseload",
                     "snap_caveat": "SPM-unit exposure, not SNAP administrative assistance-unit count"}
    return rows


def agency_evidence():
    source = json.loads((HERE / "inputs/admin_sources.json").read_text())
    if MEDICAID.exists():
        require(sha(MEDICAID) == source["medicaid"]["sha256"], "CMS-64 cache changed")
        with zipfile.ZipFile(MEDICAID) as archive:
            book = openpyxl.load_workbook(archive.open("FY 2024 FMR NET EXPENDITURES.xlsx"),
                                          read_only=True, data_only=True)
            rows = [row for row in book["ADM - National Totals"].values if row[0] == "Total Net Expenditures"]
            require(len(rows) == 1, "CMS ADM national total missing or duplicated")
            values = [int(value) for value in rows[0][1:4]]
            require(values == source["medicaid"]["national_row_dollars"], "CMS ADM transcription changed")
            require(values[0] == sum(values[1:]), "CMS federal/state financing does not close")
            book.close()
    else:
        raise ValueError("[BLOCKED] CMS primary cache missing; do not replace with a page summary")
    return source


def conditional_keys(bea, keys):
    mass = bea["consumption_bn"]
    fed = bea["consumption_plus_gross_investment_bn"]["federal"]
    retirement_max = fed["retirement"]
    retirement_proxy = retirement_max * mass["federal"] / sum(fed.values())
    fractions = {"partial_retirement_proportional_investment": retirement_proxy / mass["total"],
                 "retirement_all_investment": 0.0,
                 "retirement_no_investment": retirement_max / mass["total"]}
    arms = {}
    for name, fraction in fractions.items():
        arms[name] = {"status": "CONDITIONAL_PARTIAL_BRIDGE", "retirement_consumption_bn": fraction * mass["total"],
                      "by_allocation": {}}
        for allocation in ["personal", "shared"]:
            current = keys[allocation]["cash_assistance"]["share"]
            retirement = keys[allocation]["social_security"]["share"]
            share = (1 - fraction) * current + fraction * retirement
            arms[name]["by_allocation"][allocation] = {"effective_share": share, "share_ratio": share / current}
    # Whole-line alternatives locate sensitivity; neither is an adopted correction.
    for key in ["population", "social_security", "ssi", "snap", "medicaid_covered", "unemployment", "workers_comp"]:
        arms[f"whole_line_{key}"] = {"status": "SCENARIO_NOT_MEASURED_PROGRAM_MIX",
                                    "by_allocation": {allocation: {
                                        "effective_share": keys[allocation][key]["share"],
                                        "share_ratio": keys[allocation][key]["ratio_to_current_cash_assistance"]}
                                        for allocation in ["personal", "shared"]}}
    welfare = bea["state_local_consumption_accounting_bridge_bn"]["welfare_and_social_services"]
    for key in ["population", "ssi", "snap", "medicaid_covered"]:
        fraction = welfare / mass["total"]
        arms[f"state_welfare_residual_{key}"] = {
            "status": "SCENARIO_NOT_MEASURED_PROGRAM_MIX",
            "welfare_consumption_bn": welfare, "by_allocation": {}}
        for allocation in ["personal", "shared"]:
            current = keys[allocation]["cash_assistance"]["share"]
            share = (1 - fraction) * current + fraction * keys[allocation][key]["share"]
            arms[f"state_welfare_residual_{key}"]["by_allocation"][allocation] = {
                "effective_share": share, "share_ratio": share / current}
    for arm in arms.values():
        arm["effective_key_ratio"] = {allocation: values["share_ratio"]
                                      for allocation, values in arm["by_allocation"].items()}
    return arms


def build_item(*, require_complete=False):
    if require_complete:
        raise ValueError("[BLOCKED] item14 has no measured program-complete consumption bridge; child welfare key absent")
    bea = bea_measurements()
    keys = caseload_keys()
    arms = conditional_keys(bea, keys)
    return {"item": 14, "id": "income_security_administration", "target_line": "income_security_services",
            "status": "[DEGRADED] PARTIAL_CONDITIONAL_BRIDGE", "complete_measured_key": None,
            "default_arm": "partial_retirement_proportional_investment",
            "central": arms["partial_retirement_proportional_investment"],
            "effective_key_ratio": arms["partial_retirement_proportional_investment"]["effective_key_ratio"],
            "components": [
                {"id": "federal_retirement", "level": "federal", "key": "social_security_caseload",
                 "consumption_bn": arms["partial_retirement_proportional_investment"]["retirement_consumption_bn"],
                 "status": "MODELED_PROPORTIONAL_CONSUMPTION_INVESTMENT_BRIDGE",
                 "scope": bea["retirement_scope"]},
                {"id": "federal_other_unresolved", "level": "federal", "key": "cash_assistance",
                 "consumption_bn": bea["consumption_bn"]["federal"] - arms["partial_retirement_proportional_investment"]["retirement_consumption_bn"],
                 "status": "CURRENT_KEY_PRESERVED_UNRESOLVED_PROGRAM_MIX"},
                {"id": "state_local_unresolved", "level": "state_local", "key": "cash_assistance",
                 "consumption_bn": bea["consumption_bn"]["state_local"],
                 "status": "CURRENT_KEY_PRESERVED_UNRESOLVED_PROGRAM_MIX"},
                {"id": "published_rounding", "key": "cash_assistance", "consumption_bn": .001,
                 "status": "PUBLISHED_ROUNDING"}],
            "arms": arms, "bea": bea, "caseload_keys": keys, "agency_evidence": agency_evidence(),
            "unresolved": ["Consumption vs gross investment within federal subfunctions",
                           "Federal retirement OASI/RR caseload vs combined OASDI proxy",
                           "Federal disability/welfare/other agency-to-NIPA program bridge",
                           "State/local welfare SNAP/Medicaid/TANF/child-welfare consumption masses",
                           "State/local disability workload and matching key", "Child-welfare key absent"],
            "interactions": {"items_9_10": "Rekey source lines and added lineage/completion carriers consistently",
                             "item_11": "Adopted source has no income-security administration component; held fixed in retirement-only partial arm. A future SNAP/Medicaid workload bridge needs its own benefit-removal interaction; never multiply the scalar total.",
                             "item_12": "Coverage prices these services; reprice its income-security part under the same arm",
                             "items_13_15": "No common spending lines; item15 only education"},
            "adapter_contract": "Apply effective share ratio only to this spending line; central remains a conditional partial model. Do not relabel complete_measured_key null as zero correction or measured success."}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", type=Path, default=HERE / "inputs/admin_item.json")
    parser.add_argument("--require-complete", action="store_true")
    args = parser.parse_args()
    start = time.perf_counter()
    item = build_item(require_complete=args.require_complete)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(item, indent=2, sort_keys=True, allow_nan=False) + "\n")
    print(f"{item['status']}; seconds={time.perf_counter()-start:.3f}; "
          f"maxrss_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
