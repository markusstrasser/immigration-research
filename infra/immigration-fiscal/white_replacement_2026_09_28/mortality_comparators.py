"""Read-only group mortality and row-4 accrual arms. Not a script: invoked by accrual_white/black --mortality.

The numerator uses NVSS 2024 group/sex qx and the case's 2026 path; Note 2025.7's denominator retains the 2025
general basis. No upstream source or outputs are changed. Inputs are pinned primary spreadsheets, never transcribed
rates. General controls reproduce existing comparator ratios before mortality arms are admitted. The Hispanic union
arm is a pooled-Hispanic proxy, held beside the general central; it does not identify lineage mortality by generation.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import resource
import sys
import time
import zipfile
from contextlib import contextmanager
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
BLACK = FISCAL / "black_comparator_rough_2026_09_28"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def gate(name, ok):
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}")
    print(f"[gate] {name}", flush=True)


def verify_tables(lane):
    pins = json.loads((lane / "inputs/pins.json").read_text())["mortality_sources"]
    paths = {}
    expected = {2: "males", 3: "females", 5: "Hispanic males", 6: "Hispanic females",
                14: "Black, non-Hispanic males", 15: "Black, non-Hispanic females",
                17: "White, non-Hispanic males", 18: "White, non-Hispanic females"}
    for name, pin in pins.items():
        path = lane / "inputs" / name
        gate(f"source hash {name}", path.exists() and hashlib.sha256(path.read_bytes()).hexdigest() == pin["sha256"])
        raw = pd.read_excel(path, header=None)
        header = " ".join(map(str, raw.iloc[:8].to_numpy().ravel()))
        number = int(name.split("Table")[1].split(".")[0])
        gate(f"source identity {name}", "2024" in header and f"Life table for {expected[number]}:" in header)
        paths[number] = path
    return paths


@contextmanager
def table_context(P, paths):
    """Add mortality keys to the existing lifetime API, restoring dictionary and both caches on exit."""
    mapping = {("general", "male"): paths[2], ("general", "female"): paths[3]}
    for pop, nums in (("nh_white", (17, 18)), ("nh_black", (14, 15)), ("hispanic", (5, 6))):
        if nums[0] in paths:
            mapping.update({(pop, "male"): paths[nums[0]], (pop, "female"): paths[nums[1]]})
    old = P.L.TABLES
    P.L.TABLES = {**old, **mapping}
    P.L.qx_table.cache_clear()
    P.L.survival.cache_clear()
    try:
        for key in mapping:
            q = P.L.qx_table(*key)
            gate(f"qx domain {key}", len(q) == 121 and bool(np.isfinite(q).all()) and bool(((q >= 0) & (q <= 1)).all()))
        yield
    finally:
        P.L.TABLES = old
        P.L.qx_table.cache_clear()
        P.L.survival.cache_clear()


def row4_frame(p, zip_path):
    """Apply the account's declared citizenship/state factors; comparator records retain their original weights."""
    r = json.loads((FISCAL / "main_case_candidate_2026_09_28/derived/production_row4.json").read_text())
    with zipfile.ZipFile(zip_path) as z:
        state = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).set_index("H_SEQ").GESTFIPS
    st = p.PH_SEQ.map(state)
    gate("every pension record has a state", bool(st.notna().all()))
    out = p.copy()
    for label, code in (("naturalized", 4), ("noncitizen", 5)):
        mask = p.PENATVTY.eq(303) & p.PRCITSHP.eq(code) & ~st.isin((6, 48))
        ref = r["row4_factors"][label]
        gate(f"row4 {label} record coverage", int(mask.sum()) == ref["records"])
        gate(f"row4 {label} weight coverage", abs(float(p.w[mask].sum()) - ref["cps_population"]) < 1e-3)
        out.loc[mask, "w"] *= ref["factor"]
    gate("row4 union population", abs(float(out.w[out.union].sum()) - r["populations"]["row4"]) < 1e-3)
    # The declared factors cover five Mexico-born military records too; the union is the civilian account.
    outside = ~p.union & p.civilian
    gate("row4 leaves civilian non-union weights unchanged", bool(np.array_equal(out.w[outside], p.w[outside])))
    return out


def symmetric_frame(p, P, zip_path, lane=LANE):
    """Apply all-origin source eligibility by actual person IDs; this is a separate arm, never the union control."""
    sys.path.insert(0, str(FISCAL / "cps_imputation_keys_2026_09_23"))
    import combine_onbooks_lane as L
    for name, pin in json.loads((lane / "inputs/pins.json").read_text())["symmetric_sources"].items():
        path = FISCAL / pin["file"]
        gate(f"symmetric source hash {name}", path.exists() and L.c.sha(path) == pin["sha256"])
    gate("symmetric principal frame exists", (L.c.CACHE / "asec25_lane.parquet").exists())
    # Only point status/payer vectors are used here; do not materialize 160
    # unrelated replicate columns alongside the full actuarial frame.
    import pyarrow.parquet as pq
    source_path = L.c.CACHE / "asec25_lane.parquet"
    columns = [col for col in pq.read_schema(source_path).names if col not in L.c.REPS[1:]]
    d = pd.read_parquet(source_path, columns=columns)
    s, hh = L.cs.status_inputs()
    flag = L.state_aware_flag(s, hh, d, L.STATUS_BLIND_2024)
    shares, _ = L.share_configs(d)
    with zipfile.ZipFile(zip_path) as z:
        ids = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "A_LINENO"])
    gate("symmetric raw person IDs unique", not bool(ids.duplicated(["PH_SEQ", "A_LINENO"]).any())
         and not bool(ids.duplicated(["PH_SEQ", "PPPOS"]).any()))
    gate("symmetric source person IDs unique", not bool(d.duplicated(["PH_SEQ", "PPPOS"]).any()))
    vectors = L.c.receipt_vectors(d)
    net_se = P.ss.SECA_FACTOR * np.maximum(d.SEMP_VAL.to_numpy(float) + d.FRSE_VAL.to_numpy(float), 0)
    net_se = np.where(vectors["self_payroll"] > 0, net_se, 0.0)  # authoritative vector applies its filing threshold
    capped_se = np.minimum(net_se, np.maximum(P.ss.ext.OASDI_CAP_2024 - vectors["wage_oasdi"], 0))
    gate("symmetric statutory self-payroll reproduces principal vector", bool(np.max(np.abs(
         P.SE_OASDI * capped_se + P.SE_HI * net_se - vectors["self_payroll"])) < 1e-9))
    src = d[["PH_SEQ", "PPPOS", "A_AGE", "PRCITSHP", "PENATVTY"]].copy()
    src["source_civilian"] = L.c.masks(d)[0]
    src["source_wage"] = vectors["wage"]
    src["source_oasdi_wage"] = P.SE_OASDI * vectors["wage_oasdi"]
    src["source_se"] = net_se / P.ss.SECA_FACTOR
    src["source_oasdi_se"] = P.SE_OASDI * capped_se
    src["source_hi_se"] = P.SE_HI * net_se
    src["all_unauth"] = flag
    src["origin_onbooks"] = shares[("origin", "central")]
    del d, s, hh, flag, shares, vectors, net_se, capped_se
    bridge = p[["PH_SEQ", "A_LINENO"]].merge(ids, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    joined = bridge.merge(src, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one", indicator=True)
    gate("symmetric source person IDs fully covered", len(joined) == len(p) and bool(joined._merge.eq("both").all()))
    for left, right in (("age", "A_AGE"), ("PRCITSHP", "PRCITSHP"), ("PENATVTY", "PENATVTY")):
        gate(f"symmetric person identity {left}", bool(np.array_equal(p[left], joined[right])))
    gate("symmetric civilian masks agree principal source", bool(np.array_equal(p.civilian, joined.source_civilian)))
    disagreement = joined.all_unauth.to_numpy(bool) != p.unauth_state_aware.to_numpy(bool)
    print(f"[diagnostic] distinct source status producers disagree on {int(disagreement.sum())} records; "
          f"weighted persons {float(p.w[disagreement].sum()):.6f}", flush=True)
    f = p.copy()
    change = p.civilian & ~p.union   # the frozen identified-union principal remains on its admitted route
    for col, source_col in (("wage", "source_wage"), ("se", "source_se"), ("oasdi_wage", "source_oasdi_wage"),
                            ("oasdi_se", "source_oasdi_se"), ("hi_se", "source_hi_se")):
        f.loc[change, col] = joined.loc[change, source_col].to_numpy()
    f.loc[change, "unauth"] = joined.loc[change, "all_unauth"].to_numpy(bool)
    onbooks = np.where(joined.all_unauth, joined.origin_onbooks, 1.0)
    f.loc[change, "onbooks"] = onbooks[change]
    f.loc[change, "tax_oasdi"] = ((f.oasdi_wage + f.oasdi_se) * f.onbooks)[change]
    f.loc[change, "tax_hi"] = ((P.SE_HI * f.wage + f.hi_se) * f.onbooks)[change]
    gate("symmetric comparator status is the declared source", bool(np.array_equal(f.unauth[change], joined.all_unauth[change])))
    gate("symmetric union eligibility held fixed", bool(np.array_equal(f.unauth[p.union], p.unauth[p.union])))
    gate("symmetric union payroll held fixed", np.max(np.abs(f.tax_oasdi[p.union] - p.tax_oasdi[p.union])) < 1e-9
         and np.max(np.abs(f.tax_hi[p.union] - p.tax_hi[p.union])) < 1e-9)
    f.attrs["symmetric_eligibility"] = True
    return f


def output_row(name, basis, population, o, a, rel, n):
    return dict(group=name, entry_rule="lane" if name in ("union", "G3plus") else "immigrants_at_arrival",
                scenario="payable", basis=basis, mortality=population, age_mix="observed", population=n,
                oasdi_per_tax_dollar=o["ratio"], benefit_tax_timing=o["timing"], relative_benefit_tax_rate=rel,
                future_share=rel * o["timing"], oasdi_per_tax_dollar_net=o["ratio"] * (1 - rel * o["timing"]),
                part_a_per_hi_tax_dollar=a["accrual_bn"] / a["hi_tax_bn"], cps_oasdi_tax_bn=o["tax_bn"],
                cps_hi_tax_bn=a["hi_tax_bn"], part_a_accrual_bn=a["accrual_bn"], p_qualify_65plus=a["p_qualify"])


def run(which):
    started = time.perf_counter()
    W = load("mortality_white_accrual", LANE / "accrual_white.py")
    B = load("mortality_black_accrual", BLACK / "accrual_black.py")
    P = W.P
    gate("white and Black share the same pension module", B.P is P)
    TP = B.tr2026_path()
    meta = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())["meta"]
    TP.case_check(meta)
    lane = LANE if which == "white" else BLACK
    paths = verify_tables(lane)
    p = P.frame()
    p4 = row4_frame(p, B.ZIP)
    symmetric = symmetric_frame(p4, P, B.ZIP, lane)
    with zipfile.ZipFile(B.ZIP) as z:
        race = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "A_LINENO", "PEHSPNON", "PRDTRACE"])
    race = p[["PH_SEQ", "A_LINENO"]].merge(race, on=["PH_SEQ", "A_LINENO"], validate="one_to_one", how="left")
    gate("pension race coverage", bool(race.PEHSPNON.notna().all()))
    group = "third_plus_nh_white" if which == "white" else "nh_black"
    mask = p[P.WHITE].to_numpy() if which == "white" else (race.PEHSPNON.eq(2) & race.PRDTRACE.eq(2)).to_numpy()
    proxy = B.benefit_tax_proxy() if which == "black" else None
    rel = {"union": W.STORED["rel_union"], group: W.WHITE_REL_RATE if which == "white"
           else proxy[group]["relative_rate_calibrated"]}
    if which == "white":
        upstream_g3 = pd.read_csv(TP.TR_LANE / "derived/arms.csv")
        upstream_g3 = upstream_g3[upstream_g3.arm.eq(TP.ARM) & upstream_g3.group.eq("G3plus")].iloc[0]
        rel["G3plus"] = float(upstream_g3.future_share / upstream_g3.timing)
    mid = P.entry_midpoints()

    def price(frame, name, grid, taus, econ, fiscal_paths, population):
        f = frame.copy()
        if name != "union":
            selection = p.mexican_third_plus_selfid.to_numpy() if name == "G3plus" else mask
            if frame.attrs.get("symmetric_eligibility"):
                selection = selection & frame.civilian.to_numpy(bool)
                gate(f"symmetric {name} civilian coverage", not bool((selection & ~frame.civilian.to_numpy(bool)).any()))
                gate(f"symmetric {name} person weight closure", abs(float(frame.w[selection].sum())
                     - float(p4.w[selection].sum())) < 1e-6)
                newly = selection & f.unauth.to_numpy(bool) & ~p.unauth.to_numpy(bool)
                old_tax = float((p4.w * p.tax_oasdi)[selection].sum())
                print(f"[diagnostic] symmetric {name}: civilian population {float(frame.w[selection].sum()):.6f}; "
                      f"new unauthorized persons {float(frame.w[newly].sum()):.6f}; "
                      f"old OASDI-weight share {float((p4.w * p.tax_oasdi)[newly].sum()) / old_tax:.9f}", flush=True)
            f["union"] = selection
            f["gen"] = np.where(selection, "G3plus" if name == "G3plus" else "W3" if which == "white" else "B", "")
        if which == "black":
            arr = f.age - (2024.5 - f.PEINUSYR.map(mid))
            immigrant = (f.mexico_born if name == "union" else f.PRCITSHP.isin([4, 5])) & arr.notna()
            f["entry"] = np.where(immigrant, arr.fillna(21), 21.0)
            f["start"] = np.where(immigrant, np.maximum(arr.fillna(21), 21), 21).astype(int)
        module = W if which == "white" else B
        g = (P.CENTRAL["rate"], population)
        with TP.on_path(P, fiscal_paths):
            qq = f[f.union & f.tax_oasdi.gt(0)].reset_index(drop=True)
            o = module.oasdi_ratio(qq, {"payable": grid}, P.S.quotes()["note151_eligible_share"]["value"]["end_of_projection"],
                                   taus, scens=("payable",), g=g)["payable"]
            a = module.part_a(f[f.union].copy(), econ, P.S.quotes()["note151_eligible_share"]["value"]["end_of_projection"],
                              "payable", population=population)
        return output_row(name, "cps", population, o, a, rel[name], float(f.w[f.union].sum()))

    def added_frames(name):
        """Reweight each source profile to the case's measured added mix, holding its within-band people fixed."""
        am = meta["lineage"]["age_mix"]
        source = am["source"]["files"]["age_mix"]
        path = FISCAL / source["file"]
        gate("added age mix primary bytes", hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"])
        mixes = json.loads(path.read_text())["readings"][am["reading"]]
        band = np.minimum(p.age.to_numpy() // 5, len(am["bands"]) - 1).astype(int)
        selection = p.mexican_third_plus_selfid.to_numpy() if name == "G3plus" else mask
        n = float(p.w[selection].sum())
        counts = np.bincount(band[selection], weights=p.w[selection], minlength=len(am["bands"]))
        out = []
        for key in (("g3_rate", "later") if name == "G3plus" else ("g3_rate",)):
            target = np.asarray(mixes[key], float)
            gate(f"{name} {key} age mix matches case", np.array_equal(target, np.asarray(am["mixes"][key], float)))
            gate(f"{name} {key} every band covered", bool((counts > 0).all()) and abs(float(target.sum()) - 1) < 1e-12)
            f = p.copy()
            f.loc[selection, "w"] *= (target * n / counts)[band[selection]]
            gate(f"{name} {key} population conserved", abs(float(f.w[selection].sum()) - n) < 1e-6)
            realized = np.bincount(band[selection], weights=f.w[selection], minlength=len(target)) / n
            gate(f"{name} {key} age shares close", bool(np.max(np.abs(realized - target)) < 1e-12))
            out.append((key, f))
        return out

    rows, timings = [], {}
    with table_context(P, paths):
        t0 = time.perf_counter()
        econ, grid, taus, fiscal_paths = TP.payable(P, P.S.scaled_factors().preliminary.to_numpy())
        timings["general_grid_seconds"] = time.perf_counter() - t0
        for name in ("union", group):
            row = price(p, name, grid, taus, econ, fiscal_paths, "general")
            central = pd.read_csv(lane / "derived/accrual_ratios_oct14.csv")
            ref = central[(central.group == name) & central.scenario.eq("payable")]
            if "entry_rule" in ref:
                ref = ref[ref.entry_rule.eq(row["entry_rule"])]
            gate(f"general {name} exactly one control row", len(ref) == 1)
            for k in ("oasdi_per_tax_dollar", "benefit_tax_timing", "oasdi_per_tax_dollar_net", "part_a_per_hi_tax_dollar"):
                gate(f"general {name} {k} control", abs(row[k] - float(ref.iloc[0][k])) <= 5.01e-7)
            if name == "union":
                upstream = TP.union_row()
                for k, col in (("oasdi_per_tax_dollar", "per_tax_dollar"), ("benefit_tax_timing", "timing"),
                               ("part_a_accrual_bn", "part_a_bn"), ("cps_hi_tax_bn", "hi_tax_bn")):
                    gate(f"union upstream {col}", abs(row[k] - float(upstream[col])) < 5e-9 * max(1, abs(float(upstream[col]))))
            rows.append(row)
            row4 = price(p4, name, grid, taus, econ, fiscal_paths, "general")
            row4["basis"] = "row4"
            rows.append(row4)
            if name == group:
                row = price(symmetric, name, grid, taus, econ, fiscal_paths, "general")
                row["basis"] = "symmetric"
                rows.append(row)
        if which == "white":
            observed_g3 = price(p, "G3plus", grid, taus, econ, fiscal_paths, "general")
            for k, col in (("oasdi_per_tax_dollar", "per_tax_dollar"), ("oasdi_per_tax_dollar_net", "net_per_tax_dollar"),
                           ("benefit_tax_timing", "timing"), ("part_a_per_hi_tax_dollar", "part_a_per_hi_tax_dollar")):
                gate(f"G3plus upstream {col}", abs(observed_g3[k] - float(upstream_g3[col])) < 5e-9 * max(1, abs(float(upstream_g3[col]))))
            rows.append(observed_g3)
            extra = [(name, key, frame) for name in ("G3plus", group) for key, frame in added_frames(name)]
            for name, key, frame in extra:
                row = price(frame, name, grid, taus, econ, fiscal_paths, "general")
                row.update(basis="added_profile", age_mix=key)
                rows.append(row)
        # Retain only the denominator's money-worth array; release the unused general grid's large k arrays.
        denominator = dict(mwr={TP.BASE: grid["mwr"][TP.BASE]})
        del grid
        arms = [(group, "nh_white" if which == "white" else "nh_black")]
        if which == "white":
            arms.append(("union", "hispanic"))
        for name, population in arms:
            t0 = time.perf_counter()
            g = (P.CENTRAL["rate"], population)
            with TP.on_path(P, fiscal_paths):
                grid = TP.TR.hybrid(TP.TR.grid(econ, P.S.scaled_factors().preliminary.to_numpy(),
                                              fiscal_paths["separate_2026"], [g]), denominator)
                with TP.TR.patched(P, "payable_path", lambda _e: fiscal_paths["separate_2026"]):
                    taus = P.tob_timing(econ, P.S.scaled_factors().preliminary.to_numpy(), TP.TR.tob_share_tr2026(),
                                        runs=[(g, "payable")])
            timings[f"{population}_grid_seconds"] = time.perf_counter() - t0
            for basis, frame in (("cps", p), ("row4", p4)):
                row = price(frame, name, grid, taus, econ, fiscal_paths, population)
                row["basis"] = basis
                control = next(r for r in rows if r["group"] == name and r["basis"] == basis and r["mortality"] == "general")
                gate(f"{population} {basis} payroll conserved", abs(row["cps_oasdi_tax_bn"] - control["cps_oasdi_tax_bn"]) < 1e-9
                     and abs(row["cps_hi_tax_bn"] - control["cps_hi_tax_bn"]) < 1e-9)
                gate(f"{population} {basis} finite positive ratios", all(np.isfinite(row[k]) and row[k] > 0 for k in
                     ("oasdi_per_tax_dollar_net", "part_a_per_hi_tax_dollar")))
                rows.append(row)
            if name == group:
                row = price(symmetric, name, grid, taus, econ, fiscal_paths, population)
                row["basis"] = "symmetric"
                control = next(r for r in rows if r["group"] == name and r["basis"] == "symmetric" and r["mortality"] == "general")
                gate(f"symmetric {name} mortality payroll conserved", abs(row["cps_oasdi_tax_bn"] - control["cps_oasdi_tax_bn"]) < 1e-9
                     and abs(row["cps_hi_tax_bn"] - control["cps_hi_tax_bn"]) < 1e-9)
                rows.append(row)
            if which == "white" and population == "hispanic":
                for name, key, frame in extra:
                    row = price(frame, name, grid, taus, econ, fiscal_paths, population)
                    row.update(basis="added_profile", age_mix=key)
                    control = next(r for r in rows if r["group"] == name and r["basis"] == "added_profile"
                                   and r["age_mix"] == key and r["mortality"] == "general")
                    gate(f"added {name} {key} payroll conserved", abs(row["cps_oasdi_tax_bn"] - control["cps_oasdi_tax_bn"]) < 1e-9
                         and abs(row["cps_hi_tax_bn"] - control["cps_hi_tax_bn"]) < 1e-9)
                    rows.append(row)
            del grid
    dest = lane / "derived/accrual_ratios_mortality_oct14.csv"
    with dest.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    timings["total_seconds"] = time.perf_counter() - started
    timings["peak_memory_bytes"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    print(pd.DataFrame(rows).to_string(index=False), flush=True)
    print(json.dumps(timings, sort_keys=True), flush=True)
