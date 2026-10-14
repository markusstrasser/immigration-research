"""Read-only group mortality and row-4 accrual arms. Not a script: invoked by accrual_white/black --mortality.

The numerator uses NVSS 2024 group/sex qx and the case's 2026 path; Note 2025.7's denominator retains the 2025
general basis. No upstream source or outputs are changed. Inputs are pinned primary spreadsheets, never transcribed
rates. General controls reproduce existing comparator ratios before mortality arms are admitted. The Hispanic union
arm is a pooled-Hispanic proxy, held beside the general central; it does not identify lineage mortality by generation.
"""
from __future__ import annotations

import csv
import io
import hashlib
import importlib.util
import json
import resource
import sys
import time
import zipfile
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
sys.path.insert(0, str(FISCAL / 'scripts'))
from memory_budget import peak_bytes, require_within_budget
BLACK = FISCAL / "black_comparator_rough_2026_09_28"


def file_sha256(path):
    """Hash the same input bytes without retaining an input-sized buffer."""
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


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
                cps_hi_tax_bn=a["hi_tax_bn"], part_a_accrual_bn=a["accrual_bn"], p_qualify_65plus=a["p_qualify"],
                scenario_name="observed", end="", payroll_basis="legacy",
                population_basis="published CPS" if basis == "cps" else "row4 pension frame",
                oasdi_accrual_gross_bn=o["ratio"] * o["tax_bn"],
                oasdi_accrual_net_bn=o["ratio"] * (1 - rel * o["timing"]) * o["tax_bn"],
                multiplier_oasdi_tax_bn=o["tax_bn"], multiplier_hi_tax_bn=a["hi_tax_bn"])


def dependency_manifest(status=None):
    paths = dict(status.source_info["source_sha256"]) if status is not None else {}
    for path in (Path(__file__), LANE / "status_keys_oct14.py", LANE / "accrual_white.py",
                 BLACK / "accrual_black.py", LANE / "rekey_sept29.py",
                 FISCAL / "tax_key_heldout_2026_09_28/keys.py",
                 FISCAL / "external_benchmarks_2026_09_24/_cache/cps25_frame.parquet",
                 FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
                 FISCAL / "status_impute_2026_09_16/impute_status.py",
                 FISCAL / "california_medical_status_2026_09_23/cps_ca_status.py",
                 FISCAL / "tax_key_heldout_2026_09_28/reads/irs_table_1_2_ty2023.md",
                 FISCAL / "external_benchmarks_2026_09_24/derived/cbo_group_shares.csv",
                 FISCAL / "main_case_2026_10_15/derived/corrections.json"):
        paths[str(path.relative_to(FISCAL))] = file_sha256(path)
    for lane in (LANE, BLACK):
        for entry in json.loads((lane / "inputs/pins.json").read_text())["symmetric_sources"].values():
            path = FISCAL / entry["file"]
            paths[entry["file"]] = file_sha256(path)
    return dict(case="oct15", dependencies=paths)


def write_ratio_dependencies(lane, filename, status=None):
    ratio = lane / "derived" / filename
    manifest = dependency_manifest(status)
    manifest["output_sha256"] = file_sha256(ratio)
    ratio.with_suffix(".dependencies.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")


def verify_ratio_dependencies(lane, filename="accrual_ratios_mortality_oct15.csv"):
    path = (lane / "derived" / filename).with_suffix(".dependencies.json")
    gate("pension status dependency manifest exists", path.exists())
    manifest = json.loads(path.read_text())
    for name, expected in manifest["dependencies"].items():
        source = FISCAL / name
        gate(f"pension status dependency hash {name}", source.exists()
             and file_sha256(source) == expected)
    ratio = lane / "derived" / filename
    gate("pension output matches dependency manifest", ratio.exists()
         and file_sha256(ratio) == manifest["output_sha256"])
    return manifest


@dataclass(frozen=True)
class VerifiedRatioTable:
    lane: Path
    manifest: dict
    rows: pd.DataFrame


def read_verified_ratio_table(lane):
    """One fresh source verification and one exact ratio snapshot, scoped to a run."""
    manifest = verify_ratio_dependencies(lane)
    data = (lane / "derived/accrual_ratios_mortality_oct15.csv").read_bytes()
    gate("pension snapshot matches verified output", hashlib.sha256(data).hexdigest() == manifest["output_sha256"])
    return VerifiedRatioTable(lane, manifest, pd.read_csv(io.BytesIO(data), keep_default_na=False))


def select_verified_ratio(table, group, mortality, basis, scenario_name="observed", end="", payroll_basis="legacy"):
    """Pure exact selection from one already-verified option-set snapshot."""
    rows = table.rows
    selected = rows[(rows.group == group) & (rows.mortality == mortality) & (rows.basis == basis)
                    & (rows.scenario_name == scenario_name) & (rows.end == end)
                    & (rows.payroll_basis == payroll_basis) & (rows.scenario == "payable")]
    gate(f"exactly one pension ratio {group}/{scenario_name}/{mortality}/{payroll_basis}/{end}", len(selected) == 1)
    return selected.iloc[0].to_dict()


def require_ratio_snapshot_fresh(table):
    """Reject source changes and valid newer producer snapshots before publication."""
    current = verify_ratio_dependencies(table.lane)
    gate("pension option-set snapshot remains current", current == table.manifest)


def select_ratio(lane, group, mortality, basis, scenario_name="observed", end="", payroll_basis="legacy"):
    """Standalone selection always starts with a fresh dependency gate."""
    return select_verified_ratio(read_verified_ratio_table(lane), group, mortality, basis,
                                 scenario_name, end, payroll_basis)


def renormalized_row(row, m, status, sc, end):
    """Preserve the priced numerator; use the exact payroll dollars run29 multiplies."""
    lines = {x["id"]: x["national_bn"] for x in m.DUMP["cash"][end]["lines"] if x["side"] == "receipts"}
    se = status.receipt_amount(sc, "self_employment_oasdi_hi", lines["self_employment_oasdi_hi"])
    oasdi = sum(status.receipt_amount(sc, lid, lines[lid]) for lid in ("employee_oasdi", "employer_oasdi")) + m.SE_SHARE * se
    hi = sum(status.receipt_amount(sc, lid, lines[lid]) for lid in ("employee_hi", "employer_hi")) + (1-m.SE_SHARE) * se
    gate(f"{sc['name']} nonempty renormalized payroll", oasdi > 0 and hi > 0)
    result = dict(row, end=end, payroll_basis="renormalized_status", multiplier_oasdi_tax_bn=oasdi,
                  multiplier_hi_tax_bn=hi, oasdi_per_tax_dollar=row["oasdi_accrual_gross_bn"] / oasdi,
                  oasdi_per_tax_dollar_net=row["oasdi_accrual_net_bn"] / oasdi,
                  part_a_per_hi_tax_dollar=row["part_a_accrual_bn"] / hi)
    gate(f"{sc['name']}/{end} renormalized numerator closure", abs(result["oasdi_per_tax_dollar_net"] * oasdi
         - row["oasdi_accrual_net_bn"]) < 1e-9 and abs(result["part_a_per_hi_tax_dollar"] * hi-row["part_a_accrual_bn"]) < 1e-9)
    return result


def write_mortality_output(lane, rows, dependencies):
    """Admit the complete in-memory result before touching either previous output."""
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=list(rows[0]), lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    csv_text = buffer.getvalue()
    manifest = dict(dependencies, output_sha256=hashlib.sha256(csv_text.encode()).hexdigest())
    manifest_text = json.dumps(manifest, indent=2, sort_keys=True) + "\n"
    footprint = require_within_budget("comparator mortality")
    dest = lane / "derived/accrual_ratios_mortality_oct15.csv"
    dest.write_text(csv_text)
    dest.with_suffix(".dependencies.json").write_text(manifest_text)
    return footprint


def run(which):
    started = time.perf_counter()
    profile = []

    def checkpoint(stage):
        record = dict(stage=stage, seconds=time.perf_counter() - started,
                      peak_footprint_bytes=peak_bytes())
        profile.append(record)
        print("RESOURCE_PROFILE " + json.dumps(record, sort_keys=True), flush=True)
    W = load("mortality_white_accrual", LANE / "accrual_white.py")
    B = load("mortality_black_accrual", BLACK / "accrual_black.py")
    P = W.P
    gate("white and Black share the same pension module", B.P is P)
    TP = B.tr2026_path()
    meta = json.loads((FISCAL / "main_case_2026_10_15/derived/corrections.json").read_text())["meta"]
    TP.case_check(meta)
    lane = LANE if which == "white" else BLACK
    paths = verify_tables(lane)
    # Status build is the measured peak. Do it before retaining three actuarial
    # dataframes; their rows are independent of the comparator's setup order.
    import rekey_sept29 as comparison
    from status_keys_oct14 import build as status_build
    checkpoint("comparison imported")
    comparison.use_case("oct15")
    comparison.setup()
    comparison.stop_if_failed()
    checkpoint("comparison setup")
    status = status_build(comparison)
    checkpoint("status built")
    dependencies = dependency_manifest(status)
    checkpoint("dependencies hashed")
    p = P.frame()
    p4 = row4_frame(p, B.ZIP)
    symmetric = symmetric_frame(p4, P, B.ZIP, lane)
    checkpoint("actuarial frames built")
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

    # Map the consumer's record weights through actual person IDs, preserving
    # the actuarial frame order. A3/A4 must retain their scenario age tilts.
    with zipfile.ZipFile(B.ZIP) as z:
        ids = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "PPPOS", "A_LINENO"])
    gate("pension scenario raw IDs unique", not ids.duplicated(["PH_SEQ", "PPPOS"]).any())
    gate("pension scenario rough IDs align", np.array_equal(ids.PH_SEQ, comparison.R.d.PH_SEQ))
    lookup = p[["PH_SEQ", "A_LINENO"]].merge(ids.assign(rough_index=np.arange(len(ids))),
                 on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    gate("pension scenario IDs fully covered", lookup.rough_index.notna().all())
    order = lookup.rough_index.to_numpy(int)
    all_scenarios = comparison.scenarios()
    scenario_names = (("A1_third_plus_nh_white", "A2_us_born_nh_white",
                       "A3_third_plus_nh_white_at_union_ages", "A4_third_plus_nh_white_stationary")
                      if which == "white" else ("nh_black_rough",))
    scenario_weights = {}
    for name in scenario_names:
        sc = all_scenarios[name]
        weights = np.asarray(sc["cps_w"], float)[order]
        gate(f"{name} scenario pension weight closure", abs(float(weights.sum()) - sc["population"]) < 1e-6)
        scenario_weights[name] = (sc, weights)
    checkpoint("scenario weights built")

    def price(frame, name, grid, taus, econ, fiscal_paths, population):
        f = frame.copy()
        if name != "union":
            selection = frame.attrs.get("scenario_selection",
                        p.mexican_third_plus_selfid.to_numpy() if name == "G3plus" else mask)
            if frame.attrs.get("symmetric_eligibility"):
                selection = selection & frame.civilian.to_numpy(bool)
                gate(f"symmetric {name} civilian coverage", not bool((selection & ~frame.civilian.to_numpy(bool)).any()))
                if "scenario_selection" not in frame.attrs:
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

    def append_scenario_rows(grid, taus, econ, fiscal_paths, population):
        for scenario_name, (sc, weights) in scenario_weights.items():
            for basis in ("row4", "symmetric"):
                f = (p4 if basis == "row4" else symmetric).copy()
                f["w"] = weights
                f.attrs["scenario_selection"] = weights > 0
                row = price(f, group, grid, taus, econ, fiscal_paths, population)
                row.update(basis=basis, scenario_name=scenario_name,
                           age_mix=scenario_name, population_basis="exact comparator scenario cps_w")
                rows.append(row)
                for end in comparison.ENDS:
                    rows.append(renormalized_row(row, comparison, status, sc, end))

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
            out.append((key, f.w.to_numpy().copy()))
        return out

    def added_frame(weights):
        f = p.copy()
        f["w"] = weights
        return f

    rows, timings = [], {}
    with table_context(P, paths):
        t0 = time.perf_counter()
        econ, grid, taus, fiscal_paths = TP.payable(P, P.S.scaled_factors().preliminary.to_numpy())
        timings["general_grid_seconds"] = time.perf_counter() - t0
        checkpoint("general grid built")
        for name in ("union", group):
            row = price(p, name, grid, taus, econ, fiscal_paths, "general")
            central = pd.read_csv(lane / "derived/accrual_ratios_oct15.csv")
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
                sc = comparison.R.scenario("w3" if which == "white" else "blk", scaled=False)
                for end in comparison.ENDS:
                    rows.append(renormalized_row(row, comparison, status, sc, end))
        append_scenario_rows(grid, taus, econ, fiscal_paths, "general")
        if which == "white":
            observed_g3 = price(p, "G3plus", grid, taus, econ, fiscal_paths, "general")
            for k, col in (("oasdi_per_tax_dollar", "per_tax_dollar"), ("oasdi_per_tax_dollar_net", "net_per_tax_dollar"),
                           ("benefit_tax_timing", "timing"), ("part_a_per_hi_tax_dollar", "part_a_per_hi_tax_dollar")):
                gate(f"G3plus upstream {col}", abs(observed_g3[k] - float(upstream_g3[col])) < 5e-9 * max(1, abs(float(upstream_g3[col]))))
            rows.append(observed_g3)
            extra = [(name, key, frame) for name in ("G3plus", group) for key, frame in added_frames(name)]
            for name, key, weights in extra:
                row = price(added_frame(weights), name, grid, taus, econ, fiscal_paths, "general")
                row.update(basis="added_profile", age_mix=key)
                rows.append(row)
        checkpoint("general rows priced")
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
            checkpoint(f"{population} grid built")
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
                sc = comparison.R.scenario("w3" if which == "white" else "blk", scaled=False)
                for end in comparison.ENDS:
                    rows.append(renormalized_row(row, comparison, status, sc, end))
                append_scenario_rows(grid, taus, econ, fiscal_paths, population)
            if which == "white" and population == "hispanic":
                for name, key, weights in extra:
                    row = price(added_frame(weights), name, grid, taus, econ, fiscal_paths, population)
                    row.update(basis="added_profile", age_mix=key)
                    control = next(r for r in rows if r["group"] == name and r["basis"] == "added_profile"
                                   and r["age_mix"] == key and r["mortality"] == "general")
                    gate(f"added {name} {key} payroll conserved", abs(row["cps_oasdi_tax_bn"] - control["cps_oasdi_tax_bn"]) < 1e-9
                         and abs(row["cps_hi_tax_bn"] - control["cps_hi_tax_bn"]) < 1e-9)
                    rows.append(row)
            del grid
            checkpoint(f"{population} rows priced")
    checkpoint("all rows priced before admission")
    timings["peak_footprint_bytes"] = write_mortality_output(lane, rows, dependencies)
    timings["total_seconds"] = time.perf_counter() - started
    timings["resource_profile"] = profile
    print(pd.DataFrame(rows).to_string(index=False), flush=True)
    print(json.dumps(timings, sort_keys=True), flush=True)
