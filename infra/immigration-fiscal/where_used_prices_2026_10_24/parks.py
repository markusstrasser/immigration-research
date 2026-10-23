"""National municipal parks/recreation current spending, plus TPL diagnostics.

Exact place joins only. A government's headquarters county is not its catchment.
No construction flow or acreage is silently substituted for a capital stock.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import resource
import sys
import time
import zipfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REPO = HERE.parents[2]
OUT = HERE / "derived"
CACHE = HERE / "_cache/parks"
COG = FISCAL / "receipt_side_long_run_2026_09_28/_cache/census_2022_individual_unit_file.zip"
COUNTY_ACS = FISCAL / "school_cost_where_enrolled_2026_09_24/_cache/acs5_2024_B03001_county.json"
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
FIN24 = FISCAL / "detention_reconciliation_2026_09_20/_cache/census_2024_units.zip"
POP = REPO / "sources/immigration-fiscal/data/external/census_popest_2024/NST-EST2024-ALLDATA.csv"
COG_SHA = "c8de889f6b3320d3be347e3880607346d6440eda82705b26db2fa410fe6e83a5"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
OTHER_PINS = {
    COUNTY_ACS: "47676895c6c7ed8d6638a80ace2eecbc6070b7e398474e9780808328c7574553",
    FIN24: "0967c4d30466593796acb26f2b30c1afb37b5b9a5de43766dc65e4ccc95bd89a",
    POP: "b8b50bd345d8a5f33d5c8a28c95aeaa0a50971356f000d9b48276a65fd9022a7",
}
ACQUIRE_SPEC = importlib.util.spec_from_file_location("where_used_acquire", HERE / "acquire.py")
ACQUIRE = importlib.util.module_from_spec(ACQUIRE_SPEC)
ACQUIRE_SPEC.loader.exec_module(ACQUIRE)
source = ACQUIRE.source
STATES = ["01", "02", "04", "05", "06", "08", "09", "10", "11", "12", "13", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56"]


def sha(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def dump(name, value):
    (OUT / name).write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n")


def acs(path):
    raw = json.loads(path.read_bytes())
    if not isinstance(raw, list) or "B03001_004E" not in raw[0]:
        raise ValueError("[BLOCKED] unexpected ACS B03001 schema")
    d = pd.DataFrame(raw[1:], columns=raw[0], dtype="string")
    d["pop"] = pd.to_numeric(d.B03001_001E, errors="raise").astype(float)
    d["mex"] = pd.to_numeric(d.B03001_004E, errors="raise").astype(float)
    if "state" in d:
        d = d[d.state.isin(STATES)]
    if not (d["pop"].ge(0) & d.mex.ge(0) & d.mex.le(d["pop"])).all():
        raise ValueError("[BLOCKED] invalid ACS population cells")
    return d


def case_state_weights():
    """Reconstruct the weighting actually used by the case's state-price lane.

    Its published-CPS frame is intentional here: this reproduces an existing
    price index, not a replacement estimate of the account's national count.
    """
    builder = FISCAL / "full_account_spending_2026_09_20/builder.py"
    spec = importlib.util.spec_from_file_location("where_used_spending_builder", builder)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    with zipfile.ZipFile(CPS) as zipped:
        fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP"]
        p = pd.read_csv(zipped.open("pppub25.csv"), usecols=fields, dtype="int64")
        w = pd.read_csv(zipped.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"],
                        dtype={"h_seq": "int64", "PPPOS": "int64", "pwwgt0": "float64"}).rename(columns={"h_seq": "PH_SEQ"})
        h = pd.read_csv(zipped.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"], dtype="int64").rename(columns={"H_SEQ": "PH_SEQ"})
    p = p.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one").merge(h, on="PH_SEQ", validate="many_to_one")
    _, target = module.canonical_target(p)
    weights = p.loc[target].groupby("GESTFIPS").pwwgt0.sum()
    if not np.isclose(weights.sum(), 40896574.15235156, atol=0.01, rtol=0):
        raise ValueError("[BLOCKED] existing state-price CPS frame not reproduced")
    weights /= weights.sum()
    weights.index = weights.index.map(lambda s: f"{s:02d}")
    if set(weights.index) != set(STATES):
        raise ValueError("[BLOCKED] missing case state weight")
    return weights


def case_price_index(weights):
    """Exact FY2024 parks+libraries direct-expenditure price index in the case."""
    with zipfile.ZipFile(FIN24) as zipped:
        rows = zipped.read("2024_Individual_Unit_Files/24statetypepu.txt").decode("latin-1").splitlines()
    amount = defaultdict(float)
    for line in rows:
        if line[2] == "1" and line[4:7] in {"E61", "F61", "E52", "F52"}:
            if line[33:35] != "24":
                raise ValueError("[BLOCKED] wrong finance year")
            amount[line[:2]] += float(line[8:20]) * 1000
    amount = pd.Series(amount).reindex(STATES)
    pop = pd.read_csv(source(POP), dtype={"STATE": str, "SUMLEV": str})
    pop = pop[pop.SUMLEV.eq("040") & pop.STATE.str.zfill(2).isin(STATES)].copy()
    if pop.empty:
        pop = pd.read_csv(source(POP), dtype={"STATE": str})
        pop = pop[pop.SUMLEV.eq(40) & pop.STATE.str.zfill(2).isin(STATES)].copy()
    pop["state"] = pop.STATE.str.zfill(2)
    pop = pop.set_index("state")
    n = (pop.POPESTIMATE2023 + pop.POPESTIMATE2024) / 2
    n = n.reindex(STATES)
    relative = (amount / n) / (amount.sum() / n.sum())
    index = float((weights * relative).sum())
    declared = pd.read_csv(FISCAL / "state_priced_services_2026_09_29/derived/indexes.csv")
    principal = declared[(declared.year == 2024) & declared.basis.eq("direct") & declared.weights.eq("group") & declared.function.eq("parks_libraries")]
    if len(principal) != 1 or not np.isclose(index, float(principal["index"].iloc[0]), atol=1e-9, rtol=0):
        raise ValueError(f"[BLOCKED] case parks state price index not reproduced: {index}")
    return relative, index


def municipal():
    if sha(COG) != COG_SHA or sha(CPS) != CPS_SHA:
        raise ValueError("[BLOCKED] changed pinned CoG/CPS primary input")
    for path, wanted in OTHER_PINS.items():
        actual = source(path)
        if actual != path:
            print(f"[SOURCE-MIRROR] verifying exact pinned bytes for {path.relative_to(REPO)}", flush=True)
        if sha(actual) != wanted:
            raise ValueError(f"[BLOCKED] changed primary input: {path.relative_to(REPO)}")
    manifest = json.loads((OUT / "acquisition.json").read_text())
    for row in manifest["files"]:
        if sha(REPO / row["path"]) != row["sha256"]:
            raise ValueError("[BLOCKED] acquired primary input changed")
    places = acs(CACHE / "acs5_2024_place.json")
    places["fips"] = places.state + places.place
    places = places[places["pop"].gt(0)]
    counties = acs(COUNTY_ACS)
    state = counties.groupby("state")[["pop", "mex"]].sum()
    us = acs(CACHE / "acs5_2024_us.json").iloc[0]
    if not np.isclose(state["pop"].sum(), us["pop"], atol=0.1, rtol=0) or not np.isclose(state.mex.sum(), us.mex, atol=0.1, rtol=0):
        raise ValueError("[BLOCKED] ACS county/state/national populations do not close")
    directory, by_type, state_codes = {}, defaultdict(float), defaultdict(lambda: defaultdict(float))
    with zipfile.ZipFile(COG) as zipped:
        names = zipped.namelist()
        pid = next(name for name in names if name.endswith("Fin_PID_2022.txt"))
        fin = next(name for name in names if "FinEstDAT" in name)
        with zipped.open(pid) as stream:
            for raw in stream:
                line = raw.decode("latin-1")
                if line[2] == "2" and line[:2] in STATES:
                    directory[line[:12]] = {"uid": line[:12], "state": line[:2], "fips": line[:2] + line[111:116],
                                             "name": line[12:76].strip(), "E61": 0.0}
        with zipped.open(fin) as stream:
            for raw in stream:
                line = raw.decode("latin-1")
                code = line[12:15]
                if code not in {"E61", "F61", "G61", "E52", "F52"} or line[:2] not in STATES:
                    continue
                if line[27:31] != "2022":
                    raise ValueError("[BLOCKED] unexpected CoG fiscal year")
                value = float(line[15:27]) / 1e6  # $thousands -> $bn
                state_codes[line[:2]][code] += value
                if code == "E61":
                    by_type[line[2]] += value
                    if line[2] == "2":
                        if line[:12] not in directory:
                            raise ValueError("[BLOCKED] municipal finance has no PID")
                        directory[line[:12]]["E61"] += value
    d = pd.DataFrame(directory.values()).merge(places[["fips", "pop", "mex"]], on="fips", how="left", validate="many_to_one")
    if d.fips.duplicated().any():
        raise ValueError("[BLOCKED] overlapping municipality place IDs")
    missing = d[d["pop"].isna()].copy()
    d = d[d["pop"].notna()].copy()
    d["group_amount_bn"] = d.E61 * d.mex / d["pop"]
    t = d.groupby("state").agg(ops_bn=("E61", "sum"), group_amount_bn=("group_amount_bn", "sum"),
                                covered_pop=("pop", "sum"), covered_mex=("mex", "sum"), units=("uid", "count"))
    t = state.rename(columns={"pop": "state_pop", "mex": "state_mex"}).join(t).fillna(0)
    t["baseline_group_bn"] = t.ops_bn * t.state_mex / t.state_pop
    t["all_pc"] = t.ops_bn * 1e9 / t.state_pop
    t["group_pc"] = t.group_amount_bn * 1e9 / t.state_mex
    weights = case_state_weights()
    relative, index = case_price_index(weights)
    t["case_weight"] = weights
    t["case_state_price_relative"] = relative
    t["total_function_bn"] = pd.Series({s: sum(v.get(code, 0) for code in ["E61", "F61", "E52", "F52"]) for s, v in state_codes.items()})
    t["municipal_budget_fraction"] = t.ops_bn / t.total_function_bn
    t["within_state_factor"] = np.divide(t.group_pc, t.all_pc, out=np.ones(len(t)), where=t.all_pc.gt(0))
    t["case_index_delta"] = t.case_weight * t.case_state_price_relative * t.municipal_budget_fraction * (t.within_state_factor - 1)
    # This changes only the matched municipal E61 budget fraction. Existing
    # federal, library, nonmunicipal and construction allocations stay priced.
    bridge_delta = float(t.case_index_delta.sum())
    matched_total = float(d.E61.sum())
    group = float(d.group_amount_bn.sum())
    national = sum(by_type.values())
    missing_base = float(sum(row.E61 * state.loc[row.state, "mex"] / state.loc[row.state, "pop"] for row in missing.itertuples()))
    covered_city_factor = (group / d.mex.sum()) / (matched_total / d["pop"].sum())
    state_factor = group / t.baseline_group_bn.sum()
    # Nonnegative allocation bounds need no assumption about the residual's
    # geography. They are raw FY2022 allocations, not statistical intervals.
    rest_total = national - matched_total
    rest_base = float(sum(state_codes[s].get("E61", 0) * state.loc[s, "mex"] / state.loc[s, "pop"] for s in STATES)) - float(t.baseline_group_bn.sum())
    result = {"scope": "matched municipal E61 current operations; provision by residence",
              "factor_vs_acs_state_prices": state_factor,
              "factor_within_covered_cities": covered_city_factor,
              "factor_vs_national_municipal_price": group / (matched_total * us.mex / us["pop"]),
              "case_state_index_reproduced": index,
              "case_matched_municipal_bridge_index_delta": bridge_delta,
              "case_matched_municipal_bridge_relative_to_whole_sl_index": 1 + bridge_delta / index,
              "case_raked_factor_on_matched_municipal_block": float((t.case_weight * t.group_pc).sum() / (t.case_weight * t.all_pc).sum()),
              "coverage": {"municipalities": len(d), "positive_operations": int(d.E61.gt(0).sum()),
                           "population": float(d["pop"].sum()), "mexican_origin": float(d.mex.sum()),
                           "population_share": float(d["pop"].sum() / us["pop"]), "mexican_origin_share": float(d.mex.sum() / us.mex),
                           "matched_ops_bn": matched_total, "national_ops_bn": national,
                           "matched_share_of_sl_E61": matched_total / national,
                           "matched_share_of_municipal_E61": matched_total / by_type["2"],
                           "unmatched_municipalities": len(missing), "unmatched_municipal_ops_bn": float(missing.E61.sum())},
              "national_E61_by_type_bn": dict(by_type),
              "raw_2022_allocations_bn": {"matched_measured": group, "matched_state_baseline": float(t.baseline_group_bn.sum()),
                                          "unmatched_baseline": missing_base,
                                          "unmatched_delta_bound": [-missing_base, float(missing.E61.sum()) - missing_base],
                                          "all_unpriced_E61_total": rest_total, "all_unpriced_E61_state_baseline": rest_base,
                                          "all_unpriced_E61_delta_bound": [-rest_base, rest_total - rest_base]},
              "capital_identified": False,
              "limits": ["Residence measures geographic provision, not visitors or Mexican-origin use inside a place.",
                         "Case delta proportionally transports FY2022 municipal shares to FY2024 NIPA using each state's FY2024 parks+libraries direct-spending price.",
                         "Current E61 cash spending is not NIPA consumption net of sales/depreciation; that bridge remains conditional.",
                         "Case state-price weights are reconstructed on their original published CPS frame; no 40.90M level is substituted for the case count.",
                         "The same within-state price correction on additions/coverage/count is a transport assumption.",
                         "Other governments and unmatched municipalities remain unpriced; national operating correction is not identified.",
                         "Construction flow, acreage, and PAD-US/ParkServe polygons do not identify replacement-cost capital."]}
    d.to_csv(OUT / "park_municipalities.csv", index=False, lineterminator="\n", float_format="%.12g")
    missing.to_csv(OUT / "park_unmatched.csv", index=False, lineterminator="\n", float_format="%.12g")
    t.to_csv(OUT / "park_states.csv", lineterminator="\n", float_format="%.12g")
    return result, places


def tpl(places):
    """A deliberately restricted, geography-explicit corroboration sample."""
    spending = pd.read_excel(CACHE / "Staffing_Spending_Volunteers_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx", sheet_name="FY 23 Total Spending", header=None, dtype=object)
    acreage = pd.read_excel(CACHE / "Acreage_Park_System_Highlights_WEB_DATA_TABLES_City_Park_Facts_2024.xlsx", sheet_name="Parkland Stats by City", header=None, dtype=object)
    s = spending[spending[1].astype(str).str.fullmatch(r"\d{7}")].copy()
    s = s.rename(columns={1: "fips", 2: "city", 6: "maintenance", 7: "programming", 8: "capital_outlay", 9: "public_total"})
    s = s[["fips", "city", "maintenance", "programming", "capital_outlay", "public_total"]]
    a = acreage[acreage[1].astype(str).str.fullmatch(r"\d{7}")].copy()
    a = a.rename(columns={1: "fips", 9: "acres", 11: "designed_share"})[["fips", "acres", "designed_share"]]
    d = s.merge(a, on="fips", validate="one_to_one").merge(places[["fips", "pop", "mex"]], on="fips", validate="one_to_one")
    for col in ["maintenance", "programming", "capital_outlay", "public_total", "acres", "designed_share"]:
        d[col] = pd.to_numeric(d[col], errors="raise")
    d["operations"] = d.maintenance + d.programming
    d["designed_acres"] = d.acres * d.designed_share
    factors = {col: float(((d.mex * d[col] / d["pop"]).sum() / d.mex.sum()) / (d[col].sum() / d["pop"].sum())) for col in ["operations", "capital_outlay", "acres", "designed_acres"]}
    d.to_csv(OUT / "park_tpl_cities.csv", index=False, lineterminator="\n", float_format="%.12g")
    return {"cities": len(d), "population": float(d["pop"].sum()), "mexican_origin": float(d.mex.sum()),
            "relative_to_covered_residents": factors,
            "scope": "exact 7-digit place FIPS only; PS-prefixed regional systems excluded; includes Des Moines",
            "limits": "Convenience cross-check, not the top100 universe or national estimate. Public-only dollars, mixed source vintages. Capital outlay and acreage are not asset values."}


def main():
    started = time.perf_counter()
    result, places = municipal()
    result["tpl_cross_check"] = tpl(places)
    dump("parks.json", result)
    dump("park_sources.json", {str(path.relative_to(REPO)): {"sha256": sha(source(path)), "bytes": source(path).stat().st_size} for path in [COG, CPS, COUNTY_ACS, FIN24, POP]})
    print("Parks coverage: " + json.dumps(result["coverage"], sort_keys=True))
    print(json.dumps({"state_factor": result["factor_vs_acs_state_prices"], "case_index_delta": result["case_matched_municipal_bridge_index_delta"],
                      "elapsed_seconds": time.perf_counter() - started, "max_rss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}, sort_keys=True))


if __name__ == "__main__":
    main()
