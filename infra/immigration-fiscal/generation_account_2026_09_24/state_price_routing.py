"""Generation geography on the state-pricing lane's national price relatives.

Native-First: existing pinned CSVs and producer parsing functions; no acquisition.
Writes generation_state_indexes.json; the consumer centers raw indexes on its
charge weights, preserving the frozen union amount. Replicate SEs describe these
geographic indexes conditional on the finance tables and row-4 reweight factors.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import frame as F
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SP = F.FISCAL / "state_priced_services_2026_09_29"


def load_module(path):
    spec = importlib.util.spec_from_file_location("generation_state_price_source", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main():
    start = time.perf_counter()
    source = load_module(SP / "state_price.py")
    paths = [F.CPS_ZIP, SP / "derived/state_per_capita.csv", SP / "derived/prison_cost_by_state.csv",
             SP / "derived/corrections.csv", SP / "derived/receipts_corrections.csv", SP / "derived/indexes.csv",
             SP / "derived/receipt_indexes.csv", source.SAPCE, source.POP, source.FIN[2024][0], SP / "state_price.py",
             F.FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json"]
    hashes = {str(p.relative_to(F.ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    pin = HERE / "inputs/state_pins.json"
    if "--pin" in sys.argv:
        pin.write_text(json.dumps(hashes, indent=1) + "\n")
    if not pin.exists() or json.loads(pin.read_text()) != hashes:
        raise SystemExit("[BLOCKED] missing or stale generation state-price pins")
    d = F.load()
    civ, union, gens = F.masks(d)
    omega, _, _ = F.assignments(d, civ, union, gens)
    W = d[F.REPS].to_numpy(float).copy()
    W0 = W.copy()
    row4 = json.loads(paths[-1].read_text())
    for label, status in [("naturalized", 4), ("noncitizen", 5)]:
        m = gens["G1"] & d.PRCITSHP.eq(status).to_numpy() & ~d.GESTFIPS.isin([6, 48]).to_numpy()
        W[m] *= row4["row4_factors"][label]["factor"]
    if abs(W[union, 0].sum() - row4["populations"]["row4"]) >= 1e-6:
        raise SystemExit("[BLOCKED] state indexes do not use the row-4 population")
    states = sorted(source.STATES)
    st = d.GESTFIPS.to_numpy()
    if set(st[union]) - set(states):
        raise SystemExit("[BLOCKED] missing union state price")
    adult = d.A_AGE.to_numpy() >= 18
    pc = pd.read_csv(SP / "derived/state_per_capita.csv")
    pc = pc[(pc.year == 2024) & (pc.basis == "direct")]
    relatives = {f: t.set_index("fips").relative.reindex(states).to_numpy() for f, t in pc.groupby("function")}
    prison = pd.read_csv(SP / "derived/prison_cost_by_state.csv").set_index("fips")
    pop = pc[pc.function.eq("police")].set_index("fips").population
    imprisonment = (prison.prisoners / pop).reindex(states).fillna(0).to_numpy()
    relatives["corrections_per_inmate"] = prison.relative.reindex(states).fillna(0).to_numpy()
    fin = source.read_finance(2024).reindex(states)
    for line in ["general_sales_tax", "personal_motor_vehicle"]:
        spec = source.RECEIPTS[line]
        tax = sum(fin.get(c, 0) for c in spec["codes"]) * 1e3
        base = source.pce(2024) if spec["base"] == "pce" else source.populations(2024)
        relatives[line] = ((tax / base) / (tax.sum() / base.sum())).reindex(states).to_numpy()
    wanted = set(pd.read_csv(SP / "derived/corrections.csv").query("candidate == True").function)
    wanted |= {"general_sales_tax", "personal_motor_vehicle"}
    if any(not np.isfinite(relatives[f]).all() for f in wanted):
        raise SystemExit("[BLOCKED] nonfinite state-price relative")

    def indexes(weight, om):
        order = np.argsort(st, kind="stable")
        starts = np.r_[0, np.flatnonzero(np.diff(st[order])) + 1]
        codes = st[order][starts]
        if codes.tolist() != states:
            raise SystemExit("[BLOCKED] state bucket coverage differs from the price table")
        sorted_weights = weight[order]

        def buckets(adults_only=False):
            grouped = []
            for j in range(om.shape[1]):
                factor = om[order, j] * (adult[order] if adults_only else 1)
                grouped.append(np.add.reduceat(sorted_weights * factor[:, None], starts, axis=0))
            return np.stack(grouped, axis=1)

        counts = buckets()
        adult_counts = buckets(True)
        result = {}
        for function in sorted(wanted):
            c = counts
            if function == "personal_motor_vehicle":
                c = adult_counts
            elif function == "corrections_per_inmate":
                c = counts * imprisonment[:, None, None]
            denom = c.sum(axis=0)
            if np.any(denom <= 0):
                raise SystemExit(f"[BLOCKED] zero generation state-price denominator {function}")
            result[function] = np.einsum("s,sgr->gr", relatives[function], c) / denom
        return result

    # Principal positive control: reproduce the producer's published-weight union indexes.
    legacy = indexes(W0, union[:, None].astype(float))
    checks = []
    for r in pd.read_csv(SP / "derived/corrections.csv").query("candidate == True").itertuples():
        gap = abs(legacy[r.function][0, 0] - r.index)
        checks.append({"function": r.function, "gap": float(gap), "pass": bool(gap < 2e-9)})
    for r in pd.read_csv(SP / "derived/receipts_corrections.csv").query("candidate == True").itertuples():
        gap = abs(legacy[r.line][0, 0] - r.index)
        checks.append({"function": r.line, "gap": float(gap), "pass": bool(gap < 2e-9)})
    if not all(r["pass"] for r in checks):
        raise SystemExit(f"[BLOCKED] state-price principal controls {checks}")
    result = {}
    for conv in ["a", "b"]:
        ix = indexes(W, omega[conv])
        result[conv] = {f: {g: {"index": float(v[j, 0]), "se": float(np.sqrt(4 / 160 * ((v[j, 1:] - v[j, 0]) ** 2).sum())),
                                     "replicates": v[j].tolist()} for j, g in enumerate(F.GENS)} for f, v in ix.items()}
        if np.max(np.abs(omega[conv][union].sum(axis=1) - 1)) > 1e-12:
            raise SystemExit("[BLOCKED] generation weights do not conserve the union")
    labour = {}
    for proxy in ["PEARNVAL", "WSAL_VAL"]:
        labour[proxy] = {}
        earnings = np.maximum(d[proxy].to_numpy(float), 0)
        for conv in ["a", "b"]:
            totals = F.totals(earnings, W, omega[conv])
            shares = totals / totals.sum(axis=0)
            labour[proxy][conv] = {g: shares[j].tolist() for j, g in enumerate(F.GENS)}
    out = {"source": "state_price_routing.py", "basis": "row4; raw generation geographic indexes; frozen national prices",
           "normalization": "consumer centers each function by its charge weights at the frozen union index",
           "added_people": "no measured generation-state distribution; existing case geography held fixed",
           "conventions": result, "positive_controls": checks, "labour_income_shares": labour}
    (HERE / "derived/generation_state_indexes.json").write_text(json.dumps(out, indent=1) + "\n")
    print(f"state indexes: {len(checks)} controls PASS; seconds={time.perf_counter()-start:.3f}; peak_bytes={resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}")


if __name__ == "__main__":
    main()
