#!/usr/bin/env python3
"""Business/freight gross-output keys, reusing item 6's CPS wage-cell rules.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/activity_keys.py
Output: derived/activity_keys.json. No upstream files are written.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

sys.dont_write_bytecode = True

HERE = Path(__file__).resolve().parent
UP = HERE.parent / "job_capital_taxes_2026_10_14"
PINS = {
    "job_capital.py": "c720e31f3d9803d4413443f0dbd65da8d45cab633029cb3e20b7e990a084c1b7",
    "national.py": "34860d512b4c2fe146c1e6983f40dcab68479716c1b720a304bf9a996b3b5576",
    "derived/wages_by_industry.csv": "3bccaa790e713c2206ccba4a091b42a41b293b58eda41ee4aede4ee806202009",
    "derived/national.json": "d3bf71be1bdd3c66e265db3721acdbdb06902548b74d2470d5d06df0395fd0a0",
    "derived/national_by_industry.csv": "95ff41e65fd36dcb87a12ebd502a6c0c54365cb5596da083d7c75ed3107087f8",
    "derived/case_keys.json": "d9048296ac9f3485b737f788225167b33450d3b5735bcbe085fafe7fd0b74063",
    "inputs/census_industry_crosswalk.csv": "25bcaf038773cbb337227c19de547895d6b370892d14222e407962f326432a92",
}


def module(name):
    spec = importlib.util.spec_from_file_location(f"bizserv_{name}", UP / f"{name}.py")
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


def require(name, ok, detail=""):
    jc.gate(name, ok, detail)
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}: {detail}")


def assert_upstream():
    require("all upstream CPS and national reader gates pass", all(g["passed"] for g in jc.GATES + national.GATES))


jc = module("job_capital")
national = module("national")


def build():
    for path, digest in PINS.items():
        jc.checked(UP / path, digest)
    nj = json.loads((UP / "derived/national.json").read_text())
    case = json.loads((UP / "derived/case_keys.json").read_text())
    require("national and case-key gates pass", all(g["passed"] for g in nj["gates"] + case["gates"]))
    nat = pd.read_csv(UP / "derived/national_by_industry.csv").set_index("cell")
    cells = list(nat.index) + ["NOIND"]
    cw = case["case_wage_key"]["shares"]

    d = jc.load_frame()
    masks = jc.masks(d)
    crosswalk = pd.read_csv(UP / "inputs/census_industry_crosswalk.csv")
    require("crosswalk unique and cells covered", crosswalk.census_code.is_unique
            and set(crosswalk.bea_industry) <= set(cells) | {"GOV"})
    cell = jc.cell_of(d, crosswalk)
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    require("all wage codes map to national cells", not np.any((cell == "UNMAPPED") & (wage > 0)))
    ci = np.array([cells.index(c) for c in cell])
    units = pd.factorize(d.SPM_ID, sort=True)[0]
    nu = np.bincount(units).astype(float)
    nc = len(cells)

    def wages(weights, group, values=wage):
        return jc.cell_wages(values, ci, nc, masks[group], weights, units, nu, "personal")

    wp = d[jc.REPS].to_numpy(float)
    pub_g, pub_n = wages(wp, "union"), wages(wp, "civilian")
    keys = pd.read_csv(jc.checked(jc.KEYS, jc.KEYS_SHA)).query("allocation_key == 'wage' and allocation == 'personal'").iloc[0]
    share = pub_g.sum(axis=0) / pub_n.sum(axis=0)
    require("published union and national wages reproduce builder (1e-9 relative)",
            abs(pub_g[:, 0].sum() / keys.target_key_total - 1) < 1e-9
            and abs(pub_n[:, 0].sum() / keys.national_key_total - 1) < 1e-9)
    require("published wage share and SE reproduce builder (1e-9)",
            abs(share[0] - keys.target_key_share) < 1e-9 and abs(jc.se(share) - keys.target_share_sampling_se) < 1e-9)
    del pub_g, pub_n, wp
    row4 = json.loads(jc.checked(jc.ROW4, jc.ROW4_SHA).read_text())
    w = jc.row4_weights(d, masks, row4)
    assert_upstream()
    v6 = json.loads(jc.checked(jc.V6, jc.V6_SHA).read_text())
    require("identified G3plus and union counts reproduce case (1e-3 persons)",
            abs(w[masks["G3plus"], 0].sum() - v6["meta"]["lineage"]["counts"]["identified_g3plus"]) < 1e-3
            and abs(row4["populations"]["row4"] - v6["meta"]["lineage"]["counts"]["account_union"]) < 1e-3)

    groups = {"G1": "G1", "G2": "G2", "G3plus": "G3plus", "white_nh": "white"}
    raw = {"national": wages(w, "civilian")}
    hi = np.where(wage >= jc.TOP, wage, 0.0)
    lo = np.where(wage >= jc.TOP, 0.0, wage)
    spread = wages(w, "civilian", hi)
    spread /= spread.sum(axis=0)
    for label, g in groups.items():
        raw[label] = wages(w, g, lo) + spread * wages(w, g, hi).sum(axis=0)
        direct = wages(w, g)
        require(f"{label} top-wage redistribution conserves all weight columns (1e-12)",
                np.max(np.abs(raw[label].sum(axis=0) / direct.sum(axis=0) - 1)) < 1e-12)
    raw["union"] = sum(raw[g] for g in jc.GENS)
    require("generations reproduce union wages every cell (1e-12 relative)",
            np.max(np.abs(raw["union"].sum(axis=0) / wages(w, "union").sum(axis=0) - 1)) < 1e-12)
    fill = pd.read_csv(jc.checked(jc.FILLIN, jc.FILLIN_SHA)).query("key == 'wage'").set_index(["method", "allocation"])
    rc = float(np.mean([fill.loc[(meth, "personal"), "rel_change"] for meth in jc.METHODS]))
    stack = json.loads(jc.checked(jc.STACK, jc.STACK_SHA).read_text())
    comps = [stack["components"][f"D_{meth}"] for meth in jc.METHODS]

    def part(c, g):
        return (c["a"][g] if g in jc.GENS else c["union"]["union"])["receipts"]["corporate_labor"]["personal"]

    require("each fillin method conserves generation change (1e-9 bn)",
            all(abs(sum(part(c, g) for g in jc.GENS) - part(c, "union")) < 1e-9 for c in comps))
    delta = float(np.mean([part(c, "union") for c in comps]))
    splits = {g: float(np.mean([part(c, g) for c in comps])) / delta for g in jc.GENS}
    factors = {g: 1 + rc * splits[g] * raw["union"][:, 0].sum() / raw[g][:, 0].sum() for g in jc.GENS}
    corrected = {g: raw[g] * factors.get(g, 1) for g in groups}
    corrected["union"] = sum(corrected[g] for g in jc.GENS)
    require("corrected generation wages reproduce union fillin (1e-12)",
            abs(corrected["union"][:, 0].sum() / raw["union"][:, 0].sum() - 1 - rc) < 1e-12)
    nrec = np.bincount(ci[masks["civilian"] & (wage > 0)], minlength=nc)
    sectors = np.array([jc.SECTOR[c] for c in cells])
    private = np.flatnonzero(~np.isin(sectors, ["government", "households", "none"]))
    pools = []
    for i in range(nc):
        sector = np.flatnonzero(sectors == sectors[i])
        pools.append(np.array([i]) if nrec[i] >= jc.N_MIN or sectors[i] == "none"
                     else sector if nrec[sector].sum() >= jc.N_MIN else private)
    shares = {}
    for g, matrix in corrected.items():
        shares[g] = np.zeros_like(raw["national"])
        for i, idx in enumerate(pools):
            den = raw["national"][idx].sum(axis=0)
            shares[g][i] = np.divide(matrix[idx].sum(axis=0), den, out=np.zeros_like(den), where=den > 0)
    plain = {g: corrected[g].sum(axis=0) / raw["national"].sum(axis=0) for g in corrected}
    old = pd.read_csv(UP / "derived/wages_by_industry.csv").query("allocation == 'personal'").set_index("cell")
    require("positive control reproduces each item6 wage share and SE (1e-9)",
            all(abs(shares["union"][cells.index(c), 0] - r.union_share) < 1e-9
                and abs(jc.se(shares["union"][cells.index(c)]) - r.union_share_se) < 1e-9 for c, r in old.iterrows()))
    require("positive control reproduces each item6 wage bill exactly at CSV precision (six decimals)",
            all(round(corrected["union"][cells.index(c), 0] / 1e9, 6) == r.union_wages_bn
                and round(raw["national"][cells.index(c), 0] / 1e9, 6) == r.national_wages_bn for c, r in old.iterrows()))

    path = national.pinned("bea_SUPPLY-USE.zip")
    industries, use_row = national.read_use(path)
    output = use_row("T018")
    source_sum = sum(output[c] for c in industries)
    source_total = output["T001"]
    require("BEA output source rounding within half-million per industry", abs(source_sum - source_total) <= 0.5 * len(industries))
    output_scale = source_total / source_sum
    bea_output = {c: output[c] / 1000 * output_scale for c in industries}
    output_total = sum(bea_output.values())
    require("normalized BEA output industries close to T018 total (1e-6 bn)", abs(output_total - source_total / 1000) < 1e-6)
    business = {c: x for c, x in bea_output.items() if c != "HS" and not c.startswith("G")}
    vec = national.to_cells(business, cells)
    require("private gross output maps and closes (1e-6 bn)", abs(vec.sum() - sum(business.values())) < 1e-6)
    require("positive-output cells have wages in every replicate", all((raw["national"][i] > 0).all() for i in np.flatnonzero(vec > 0)))
    goods = np.isin(sectors, ["agriculture", "mining", "durable", "nondurable"])
    freight = vec * goods
    nonmining = sectors != "mining"
    vectors = {"business_output_full": (vec, vec.sum()), "business_output_mining_fixed": (vec * nonmining, vec.sum()),
               "freight_output_full": (freight, freight.sum()), "freight_output_mining_fixed": (freight * nonmining, freight.sum())}
    results = {}
    for key, (vector, base) in vectors.items():
        values = {g: shares[g].T @ vector / base for g in corrected}
        require(f"{key} generations close to union in every replicate (1e-12)",
                np.max(np.abs(sum(values[g] for g in jc.GENS) - values["union"])) < 1e-12)
        full = freight if key.startswith("freight") else vec
        results[key] = {"national_output_bn": float(base), "responding_output_bn": float(vector.sum()),
                        "mining_output_fraction": float(full[~nonmining].sum() / base), "groups": values}
    results["plain_wage"] = {"national_output_bn": None, "responding_output_bn": None, "groups": plain}
    national_population = w[masks["civilian"]].sum(axis=0)
    population = {g: w[masks[groups.get(g, g)]].sum(axis=0) / national_population for g in corrected}
    results["population"] = {"national_output_bn": None, "responding_output_bn": None, "groups": population}
    for key, item in results.items():
        item["groups"] = {g: {"share": float(v[0]), "se": jc.se(v), "replicates": v.tolist(),
                              "factor": float(v[0] / (cw[g]["personal"] if g in cw else plain[g][0])),
                              "factor_over_lane_plain": float(v[0] / plain[g][0])} for g, v in item["groups"].items()}
    key_order = list(results)
    union_vectors = np.array([results[k]["groups"]["union"]["replicates"] for k in key_order])
    differences = union_vectors[:, 1:] - union_vectors[:, :1]
    covariance = 4 / 160 * differences @ differences.T
    assert_upstream()
    return {"meta": {"year": 2024, "allocation": "personal", "population": row4["populations"]["row4"],
                     "rule": "item6-style corrected and smoothed industry wage share weighted by BEA T018 private gross output",
                     "output_source": national.PINS["bea_SUPPLY-USE.zip"], "input_sha256": PINS,
                     "gross_output_is": "activity proxy including intermediate production, not value added or measured service use",
                     "excluded_output": "HS housing; all government industries; no private-household/noindustry output",
                     "freight_goods": "agriculture incl forestry/fishing, mining, durable and nondurable manufacturing; construction excluded",
                     "mining_fixed": "zero mining numerator with full national denominator; hybrid = this partial share + mining_output_fraction * baseline household/consumption key",
                     "factor_rule": "union/generations divide case wage shares; white_nh divides its corrected lane plain wage share",
                     "replicate_rule": "index 0 main estimate; indexes 1-160 CPS SDR; covariance = 4/160 sum replicate deviations outer product",
                     "uncertainty": "CPS replicate SE conditional on national output, top pooling and main fillin factors; fillin/model uncertainty not included",
                     "fillin": {"methods": jc.METHODS, "mean_rel_change": rc, "generation_factors": factors},
                     "case_wage_shares": {g: cw[g]["personal"] for g in cw},
                     "lane_plain_shares": {g: float(v[0]) for g, v in plain.items()},
                     "national_all_industry_output_bn": output_total,
                     "output_rounding": {"source_cell_sum_mn": source_sum, "source_total_mn": source_total,
                                         "common_normalization_factor": output_scale}},
            "keys": results, "union_covariance": {"key_order": key_order, "matrix": covariance.tolist()},
            "by_industry": [{"cell": c, "sector": jc.SECTOR[c], "private_output_bn": float(vec[i]),
                             "freight_output_bn": float(freight[i]), "wage_earners": int(nrec[i]),
                             "pooled_cells": [cells[j] for j in pools[i]], "union_wage_share": float(shares["union"][i, 0])}
                            for i, c in enumerate(cells)], "gates": jc.GATES + national.GATES}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    start = time.perf_counter()
    result = build()
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # macOS reports bytes; Linux reports KiB.
    peak_bytes = peak if sys.platform == "darwin" else peak * 1024
    require("process peak memory below 2.5GB", peak_bytes < 2_500_000_000)
    result["gates"] = jc.GATES + national.GATES
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "activity_keys.json").write_text(json.dumps(result, indent=1, allow_nan=False) + "\n")
    print(f"[timing] seconds={time.perf_counter() - start:.3f} peak_MB={peak_bytes / 1e6:.1f}")
    for k, v in result["keys"].items():
        print(f"{k}: union {v['groups']['union']['share']:.9f}, SE {v['groups']['union']['se']:.9f}")


if __name__ == "__main__":
    main()
