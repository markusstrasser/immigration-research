"""Reproduce mortality controls, then price sex/nativity-specific Mexican tables.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/mortality.py
Nothing outside this lane is written. General Note 2025.7 denominator and the
2026 payable/net numerator use the comparators' imported actuarial route.
"""
from __future__ import annotations

import csv
import functools
import gc
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
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
WHITE = FISCAL / "white_replacement_2026_09_28"
BLACK = FISCAL / "black_comparator_rough_2026_09_28"
sys.path.insert(0, str(FISCAL / "scripts"))
import numpy as np
import pandas as pd
from memory_budget import require_within_budget


def load(name, path):
    pins = json.loads((HERE / "inputs/pins.json").read_text())
    original = str(path.relative_to(HERE.parents[2]))
    archive = pins["route_archives"][original]
    source = HERE.parents[2] / archive["file"]
    gate(f"frozen v7 module {original}", hashlib.sha256(source.read_bytes()).hexdigest() == archive["sha256"])
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    # Compile the exact archived bytes with original __file__/module metadata,
    # so unchanged relative imports resolve to the admitted upstream inputs.
    exec(compile(source.read_bytes(), str(path), "exec"), mod.__dict__)
    return mod


def gate(label, ok):
    if not ok:
        raise SystemExit(f"[BLOCKED] {label}")
    print(f"[gate] {label}", flush=True)


def write(name, rows):
    with (HERE / "derived" / name).open("w", newline="") as stream:
        wr = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)


def check_pins():
    pins = json.loads((HERE / "inputs/pins.json").read_text())
    root = HERE.parents[2]
    for file, expected in pins["local_sources"].items():
        actual_file = pins.get("route_archives", {}).get(file, {}).get("file", file)
        with (root / actual_file).open("rb") as stream:
            actual = hashlib.file_digest(stream, "sha256").hexdigest()
        gate(f"pin {file}", expected == actual)


def build_qx(reference, hazards, arm, nativity):
    """The brief specifies qx * HR (a probability approximation, not hazard integration).

    The inherited accrual model closes its life tables at 100; preserve that
    boundary. The NVSS reference includes foreign-born NH whites whereas the
    paper's reference is US-born NH whites: explicitly a transport limitation.
    """
    out = {}
    for sex, base in reference.items():
        rows = hazards[(hazards.sex == sex) & (hazards.nativity == nativity)]
        model_pair = (2, 4) if arm == "adjusted" else (1, 3)
        metric = "ci_low" if arm == "ci_low_hazard" else "ci_high" if arm == "ci_high_hazard" else "hr"
        young = float(rows[rows.model == model_pair[0]].iloc[0][metric])
        old = float(rows[rows.model == model_pair[1]].iloc[0][metric])
        if arm == "salmon_all_extra" and nativity == "foreign_born":
            old = float(hazards[(hazards.sex == sex) & (hazards.nativity == "us_born")
                                & (hazards.model == 3)].iloc[0].hr)
        first = 18 if arm == "extend_to_18" else 25
        hr = np.ones(121)
        hr[first:65] = young
        hr[65:100] = old
        q = np.clip(base * hr, 0, 1)
        if arm == "salmon_turra_pooled_proxy" and nativity == "foreign_born":
            rates = pd.read_csv(HERE / "inputs/salmon_turra_rates.csv")
            rates = rates[(rates.sex == sex) & rates.population.eq("all_hispanic")]
            gate(f"Turra {sex} six age bands", len(rates) == 6 and list(rates.age_low) == [65, 70, 75, 80, 85, 90])
            for _, r in rates.iterrows():
                q[int(r.age_low):int(r.age_high) + 1] *= float(r.combined_rate / r.us_rate)
        q[100:] = 1.0
        gate(f"{arm}/{nativity}/{sex} finite qx domain", bool(np.isfinite(q).all()) and bool(((q >= 0) & (q <= 1)).all()))
        out[sex] = q
    return out


@contextmanager
def synthetic_tables(P, tables):
    old = P.L.qx_table

    @functools.lru_cache(maxsize=None)
    def qx(population, sex):
        if population in tables:
            return tables[population][sex].copy()
        return old(population, sex)

    P.L.qx_table = qx
    P.L.survival.cache_clear()
    try:
        yield
    finally:
        P.L.qx_table = old
        old.cache_clear()
        P.L.survival.cache_clear()


class Route:
    def __init__(self):
        self.M = load("lineage_mortality_comparators", WHITE / "mortality_comparators.py")
        self.W = load("lineage_accrual_white", WHITE / "accrual_white.py")
        self.B = load("lineage_accrual_black", BLACK / "accrual_black.py")
        self.P, self.TP = self.W.P, load("lineage_tr2026_path", WHITE / "tr2026_path.py")
        gate("same admitted pension module", self.B.P is self.P)
        self.meta = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())["meta"]
        self.TP.case_check(self.meta)
        cache_key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in
                                    (self.P.ss.__file__, self.P.ss.ext.__file__, self.P.ca.__file__)))
        gate("read-only pension frame cache already exists", (self.P.CACHE / f"stage_{cache_key.hexdigest()[:16]}.parquet").exists())
        self.p = self.P.frame()
        self.p4 = self.M.row4_frame(self.p, self.B.ZIP)
        self.u_long = self.P.S.quotes()["note151_eligible_share"]["value"]["end_of_projection"]
        self.prelim = self.P.S.scaled_factors().preliminary.to_numpy()
        self.rel_union = self.W.STORED["rel_union"]
        upstream = pd.read_csv(self.TP.TR_LANE / "derived/arms.csv")
        row = upstream[(upstream.arm == self.TP.ARM) & (upstream.group == "G3plus")].iloc[0]
        self.rel_g3 = float(row.future_share / row.timing)
        with zipfile.ZipFile(self.B.ZIP) as z:
            race = pd.read_csv(z.open("pppub25.csv"), usecols=["PH_SEQ", "A_LINENO", "PEHSPNON", "PRDTRACE"])
        race = self.p[["PH_SEQ", "A_LINENO"]].merge(race, on=["PH_SEQ", "A_LINENO"], validate="one_to_one", how="left")
        self.black_mask = (race.PEHSPNON.eq(2) & race.PRDTRACE.eq(2)).to_numpy()
        gate("race coverage", bool(race.PEHSPNON.notna().all()))

    def price(self, frame, name, population, grid, taus, *, rel=None, module=None):
        P, TP = self.P, self.TP
        module = module or self.W
        f = frame[frame.union].copy()
        if name != "union":
            f = frame.copy()
            if name in ("G1", "G2", "G3plus"):
                f = f[f.gen.eq(name) & f.union].copy()
            elif name == "third_plus_nh_white":
                f = f[f[P.WHITE]].copy()
                f["gen"] = "W3"
            elif name == "nh_black":
                f = f[self.black_mask].copy()
                f["gen"] = "B"
        if module is self.B:
            arr = f.age - (2024.5 - f.PEINUSYR.map(P.entry_midpoints()))
            imm = f.PRCITSHP.isin([4, 5]) & arr.notna()
            f["entry"] = np.where(imm, arr.fillna(21), 21.0)
            f["start"] = np.where(imm, np.maximum(arr.fillna(21), 21), 21).astype(int)
        g = (P.CENTRAL["rate"], population)
        with TP.on_path(P, self.paths):
            o = module.oasdi_ratio(f[f.tax_oasdi.gt(0)].reset_index(drop=True), {"payable": grid}, self.u_long,
                                   taus, scens=("payable",), g=g)["payable"]
            a = module.part_a(f, self.econ, self.u_long, "payable", population=population)
        rel = self.rel_union if rel is None else rel
        return self.M.output_row(name, "cps", population, o, a, rel, float(f.w.sum()))

    def profiles(self):
        am = self.meta["lineage"]["age_mix"]
        source = am["source"]["files"]["age_mix"]
        path = FISCAL / source["file"]
        gate("added age mix primary hash", hashlib.sha256(path.read_bytes()).hexdigest() == source["sha256"])
        mixes = json.loads(path.read_text())["readings"][am["reading"]]
        band = np.minimum(self.p.age.to_numpy() // 5, len(am["bands"]) - 1).astype(int)
        profiles = []
        for name, keys in (("G3plus", ("g3_rate", "later")), ("third_plus_nh_white", ("g3_rate",))):
            sel = self.p.mexican_third_plus_selfid.to_numpy() if name == "G3plus" else self.p[self.P.WHITE].to_numpy()
            n = float(self.p.w[sel].sum())
            counts = np.bincount(band[sel], weights=self.p.w[sel], minlength=len(am["bands"]))
            for key in keys:
                target = np.asarray(mixes[key], float)
                gate(f"{name}/{key} matches frozen case", np.array_equal(target, np.asarray(am["mixes"][key], float)))
                gate(f"{name}/{key} all bands supported", bool((counts > 0).all()) and abs(float(target.sum()) - 1) < 1e-12)
                f = self.p.copy()
                f.loc[sel, "w"] *= (target * n / counts)[band[sel]]
                gate(f"{name}/{key} population closure", abs(float(f.w[sel].sum()) - n) < 1e-6)
                gate(f"{name}/{key} age share closure", np.max(np.abs(np.bincount(band[sel], weights=f.w[sel],
                                                                                 minlength=len(target)) / n - target)) < 1e-12)
                profiles.append((name, key, f))
        return profiles

    def grid(self, population):
        g = (self.P.CENTRAL["rate"], population)
        start = time.perf_counter()
        with self.TP.on_path(self.P, self.paths):
            grid = self.TP.TR.hybrid(self.TP.TR.grid(self.econ, self.prelim, self.paths["separate_2026"], [g]),
                                      self.denominator)
            with self.TP.TR.patched(self.P, "payable_path", lambda _e: self.paths["separate_2026"]):
                taus = self.P.tob_timing(self.econ, self.prelim, self.TP.TR.tob_share_tr2026(), runs=[(g, "payable")])
        gate(f"{population} Note general denominator unchanged", np.array_equal(grid["mwr"][self.TP.BASE],
                                                                                self.denominator["mwr"][self.TP.BASE]))
        print(f"[timing] {population} grid+timing {time.perf_counter() - start:.3f}s", flush=True)
        return grid, taus


def case_inputs(meta):
    full, union = {}, {}
    for basis, suffix in (("accrual", ""), ("cash", "_cash")):
        full[basis] = json.loads((WHITE / f"derived/engine_lines_oct14{suffix}.json").read_text())
        union[basis] = json.loads((WHITE / f"derived/engine_lines_oct14_union{suffix}.json").read_text())
    share = meta["pension_accrual"]["se_oasdi_share"]
    part_a = meta["pension_accrual"]["part_a_share"]
    out = {}
    for end in ("low", "high"):
        amt = {f"{r['side']}|{r['id']}": r["amount_bn"] for r in union["cash"][end]["lines"] if r["side"] != "scalar"}
        se = amt["receipts|self_employment_oasdi_hi"]
        otax = amt["receipts|employee_oasdi"] + amt["receipts|employer_oasdi"] + share * se
        hitax = amt["receipts|employee_hi"] + amt["receipts|employer_hi"] + (1 - share) * se
        extra = {}
        for basis in full:
            fm = {f"{r['side']}|{r['id']}": r["amount_bn"] for r in full[basis][end]["lines"] if r["side"] != "scalar"}
            um = {f"{r['side']}|{r['id']}": r["amount_bn"] for r in union[basis][end]["lines"] if r["side"] != "scalar"}
            extra[basis] = {key: fm[key] - um.get(key, 0) for key in fm}
        added_ss = extra["accrual"]["spending|social_security"]
        added_pa = extra["accrual"]["spending|medicare"] - (1 - part_a) * extra["cash"]["spending|medicare"]
        gate(f"{end} added nonnegative accrued liabilities", min(added_ss, added_pa) >= 0)
        out[end] = dict(oasdi_tax_bn=otax, hi_tax_bn=hitax, added_ss_bn=added_ss, added_part_a_bn=added_pa,
                        base_accrual_bn=full["accrual"][end]["cost_bn"], base_cash_bn=full["cash"][end]["cost_bn"])
    return out


def profile_deltas(rows, control, amounts):
    factors = []
    for r in rows:
        ref = next(c for c in control if c["basis"] == "added_profile" and c["group"] == r["group"]
                   and c["age_mix"] == r["age_mix"])
        factors.append(dict(group=r["group"], age_mix=r["age_mix"],
                            ss_factor=r["oasdi_per_tax_dollar_net"] / ref["oasdi_per_tax_dollar_net"] - 1,
                            hi_factor=r["part_a_per_hi_tax_dollar"] / ref["part_a_per_hi_tax_dollar"] - 1))
    lo = amounts["added_ss_bn"] * min(f["ss_factor"] for f in factors) + amounts["added_part_a_bn"] * min(f["hi_factor"] for f in factors)
    hi = amounts["added_ss_bn"] * max(f["ss_factor"] for f in factors) + amounts["added_part_a_bn"] * max(f["hi_factor"] for f in factors)
    return lo, hi, factors


def main():
    started = time.perf_counter()
    check_pins()
    R = Route()
    paths = R.M.verify_tables(HERE)
    profiles = R.profiles()
    controls, all_rows, qrows = [], [], []
    audits = []
    amounts = case_inputs(R.meta)
    with R.M.table_context(R.P, paths):
        t0 = time.perf_counter()
        R.econ, grid, taus, R.paths = R.TP.payable(R.P, R.prelim)
        print(f"[timing] general grid+timing {time.perf_counter() - t0:.3f}s", flush=True)
        R.denominator = dict(mwr={R.TP.BASE: grid["mwr"][R.TP.BASE]})
        denom_hash = hashlib.sha256(R.denominator["mwr"][R.TP.BASE].tobytes()).hexdigest()
        # Reproduce the full-precision frozen general ratios before new mortality.
        for name, frame, basis, rel, module, lane in (
            ("union", R.p, "cps", R.rel_union, R.W, WHITE),
            ("union", R.p4, "row4", R.rel_union, R.W, WHITE),
            ("third_plus_nh_white", R.p, "cps", 1.0, R.W, WHITE),
            ("nh_black", R.p, "cps", R.B.benefit_tax_proxy()["nh_black"]["relative_rate_calibrated"], R.B, BLACK),
            ("G3plus", R.p, "cps", R.rel_g3, R.W, WHITE)):
            r = R.price(frame, name, "general", grid, taus, rel=rel, module=module)
            r["basis"] = basis
            frozen = pd.read_csv(lane / "derived/accrual_ratios_mortality_oct14.csv")
            ref = frozen[(frozen.group == name) & (frozen.basis == basis) & (frozen.mortality == "general")].iloc[0]
            metrics = ("oasdi_per_tax_dollar", "benefit_tax_timing", "oasdi_per_tax_dollar_net", "part_a_per_hi_tax_dollar", "cps_oasdi_tax_bn", "cps_hi_tax_bn")
            max_gap = max(abs(r[k] - float(ref[k])) for k in metrics)
            gate(f"general {name}/{basis} full-precision control", max_gap < 1e-9)
            audits.append(dict(control=f"general {name}/{basis}", max_abs_gap=max_gap, passed=True))
            controls.append(r)
        for name in ("G1", "G2", "G3plus"):
            r = R.price(R.p4, name, "general", grid, taus)
            r.update(basis="row4", arm="general")
            all_rows.append(r)
        for name, key, frame in profiles:
            r = R.price(frame, name, "general", grid, taus, rel=R.rel_g3 if name == "G3plus" else 1.0)
            r.update(basis="added_profile", age_mix=key)
            frozen = pd.read_csv(WHITE / "derived/accrual_ratios_mortality_oct14.csv")
            ref = frozen[(frozen.group == name) & (frozen.basis == "added_profile") & (frozen.age_mix == key)
                         & (frozen.mortality == "general")].iloc[0]
            gate(f"general added {name}/{key} control", max(abs(r[k] - float(ref[k])) for k in metrics) < 1e-9)
            controls.append(r)
        del grid
        gc.collect()
        hgrid, htaus = R.grid("hispanic")
        for frame, basis in ((R.p, "cps"), (R.p4, "row4")):
            r = R.price(frame, "union", "hispanic", hgrid, htaus)
            r["basis"] = basis
            frozen = pd.read_csv(WHITE / "derived/accrual_ratios_mortality_oct14.csv")
            ref = frozen[(frozen.group == "union") & (frozen.basis == basis) & (frozen.mortality == "hispanic")].iloc[0]
            gate(f"pooled Hispanic union/{basis} full-precision control", max(abs(r[k] - float(ref[k])) for k in metrics) < 1e-9)
            controls.append(r)
        hprofiles = []
        for name, key, frame in profiles:
            r = R.price(frame, name, "hispanic", hgrid, htaus, rel=R.rel_g3 if name == "G3plus" else 1.0)
            r.update(basis="added_profile", age_mix=key)
            hprofiles.append(r)
            controls.append(r)
        ref_arm = pd.read_csv(WHITE / "derived/symmetric_hispanic_arm_oct14.csv")
        gen = next(r for r in controls if r["group"] == "union" and r["basis"] == "row4" and r["mortality"] == "general")
        hisp = next(r for r in controls if r["group"] == "union" and r["basis"] == "row4" and r["mortality"] == "hispanic")
        pooled = []
        for end, amt in amounts.items():
            ss = (hisp["oasdi_per_tax_dollar_net"] - gen["oasdi_per_tax_dollar_net"]) * amt["oasdi_tax_bn"]
            hi = (hisp["part_a_per_hi_tax_dollar"] - gen["part_a_per_hi_tax_dollar"]) * amt["hi_tax_bn"]
            lo, high, _ = profile_deltas(hprofiles, controls, amt)
            ref = ref_arm[ref_arm.end.eq(end)].iloc[0]
            r = dict(end=end, identified_ss_delta_bn=ss, identified_part_a_delta_bn=hi,
                     identified_delta_bn=ss + hi, added_profile_delta_low_bn=lo, added_profile_delta_high_bn=high,
                     lineage_delta_low_bn=ss + hi + lo, lineage_delta_high_bn=ss + hi + high)
            gap = max(abs(r[k] - float(ref[k])) for k in r if k != "end")
            gate(f"{end} pooled Hispanic union + added bound reproduces BEFORE new tables", gap < 1e-9)
            audits.append(dict(control=f"pooled_hispanic {end}", max_abs_gap=gap, passed=True))
            pooled.append(r)
        del hgrid
        gc.collect()
        write("pooled_control.csv", pooled)
        reference = {sex: R.P.L.qx_table("nh_white", sex).copy() for sex in ("male", "female")}
        hazards = pd.read_csv(HERE / "derived/hazard_ratios.csv")
        arms = ("central", "salmon_all_extra", "salmon_turra_pooled_proxy", "adjusted", "ci_low_hazard", "ci_high_hazard", "extend_to_18")
        tables = {f"{arm}_{nat}": build_qx(reference, hazards, arm, nat)
                  for arm in arms for nat in ("foreign_born", "us_born")}
        for pop, sexes in tables.items():
            for sex, q in sexes.items():
                for age, val in enumerate(q):
                    qrows.append(dict(mortality=pop, sex=sex, age=age, qx=val))
        with synthetic_tables(R.P, tables):
            for arm in arms:
                # USB grid also prices every descendant profile. Each grid is released before the next one.
                for nat, groups in (("foreign_born", ("G1",)), ("us_born", ("G2", "G3plus"))):
                    pop = f"{arm}_{nat}"
                    if nat == "us_born" and arm in ("salmon_all_extra", "salmon_turra_pooled_proxy"):
                        same = all(np.array_equal(tables[pop][sex], tables["central_us_born"][sex])
                                   for sex in ("male", "female"))
                        gate(f"{pop} exact central descendant table reuse", same)
                        clones = [dict(r, mortality=pop, arm=arm) for r in all_rows if r["arm"] == "central"
                                  and (r["basis"] == "added_profile" or r["group"] in ("G2", "G3plus"))]
                        gate(f"{pop} complete reused descendant/profile rows", len(clones) == 5)
                        all_rows.extend(clones)
                        continue
                    grid, taus = R.grid(pop)
                    for name in groups:
                        r = R.price(R.p4, name, pop, grid, taus)
                        r.update(basis="row4", arm=arm)
                        all_rows.append(r)
                    if nat == "us_born":
                        for name, key, frame in profiles:
                            r = R.price(frame, name, pop, grid, taus, rel=R.rel_g3 if name == "G3plus" else 1.0)
                            r.update(basis="added_profile", age_mix=key, arm=arm)
                            all_rows.append(r)
                    del grid
                    gc.collect()
                    require_within_budget(f"mortality {pop}")
    write("reproduced_ratios.csv", controls)
    write("mortality_qx.csv", qrows)
    write("accrual_ratios.csv", all_rows)
    outputs, generation, profile_output = [], [], []
    base = {r["group"]: r for r in all_rows if r["arm"] == "general"}
    gate("general generations OASDI dollars close to union", abs(sum(r["cps_oasdi_tax_bn"] for r in base.values()) - gen["cps_oasdi_tax_bn"]) < 1e-9)
    gate("general generations HI dollars close to union", abs(sum(r["cps_hi_tax_bn"] for r in base.values()) - gen["cps_hi_tax_bn"]) < 1e-9)
    for metric, tax in (("oasdi_per_tax_dollar_net", "cps_oasdi_tax_bn"), ("part_a_per_hi_tax_dollar", "cps_hi_tax_bn")):
        gate(f"general generations {metric} reconstruct union", abs(sum(b[metric] * b[tax] for b in base.values()) / gen[tax] - gen[metric]) < 1e-9)
    for arm in arms:
        for end, amt in amounts.items():
            parts = []
            for name in ("G1", "G2", "G3plus"):
                ref = base[name]
                r = next(r for r in all_rows if r["arm"] == arm and r["group"] == name and r["basis"] == "row4")
                for tax in ("cps_oasdi_tax_bn", "cps_hi_tax_bn"):
                    gate(f"{arm}/{name} {tax} held fixed", abs(r[tax] - ref[tax]) < 1e-9)
                ss = (r["oasdi_per_tax_dollar_net"] - ref["oasdi_per_tax_dollar_net"]) * ref["cps_oasdi_tax_bn"] / gen["cps_oasdi_tax_bn"] * amt["oasdi_tax_bn"]
                hi = (r["part_a_per_hi_tax_dollar"] - ref["part_a_per_hi_tax_dollar"]) * ref["cps_hi_tax_bn"] / gen["cps_hi_tax_bn"] * amt["hi_tax_bn"]
                part = dict(arm=arm, basis="accrual", end=end, generation=name, population=ref["population"],
                            oasdi_delta_bn=ss, part_a_delta_bn=hi, delta_low_bn=ss + hi, delta_high_bn=ss + hi)
                generation.append(part)
                parts.append(part)
            pp = [r for r in all_rows if r["arm"] == arm and r["basis"] == "added_profile"]
            lo, hi, factors = profile_deltas(pp, controls, amt)
            for f in factors:
                profile_output.append(dict(arm=arm, end=end, **f,
                                           ss_delta_bn=amt["added_ss_bn"] * f["ss_factor"],
                                           part_a_delta_bn=amt["added_part_a_bn"] * f["hi_factor"]))
            generation.append(dict(arm=arm, basis="accrual", end=end, generation="added_descendants",
                                   population=R.meta["lineage"]["counts"]["lineage_population"] - float(R.p4.w[R.p4.union].sum()),
                                   oasdi_delta_bn="bounded", part_a_delta_bn="bounded", delta_low_bn=lo, delta_high_bn=hi))
            identified = sum(p["delta_low_bn"] for p in parts)
            total_lo, total_hi = identified + lo, identified + hi
            gate(f"{arm}/{end} generation parts close at 1e-9", abs(sum(p["delta_low_bn"] for p in generation if p["arm"] == arm and p["end"] == end) - total_lo) < 1e-9
                 and abs(sum(p["delta_high_bn"] for p in generation if p["arm"] == arm and p["end"] == end) - total_hi) < 1e-9)
            outputs.append(dict(arm=arm, basis="accrual", end=end, specification=16 if end == "low" else 11,
                                identified_union_delta_bn=identified, added_delta_low_bn=lo, added_delta_high_bn=hi,
                                lineage_delta_low_bn=total_lo, lineage_delta_high_bn=total_hi,
                                base_cost_bn=amt["base_accrual_bn"], cost_low_bn=amt["base_accrual_bn"] + total_lo,
                                cost_high_bn=amt["base_accrual_bn"] + total_hi,
                                cash_delta_bn=0.0, exceeds_5bn=max(abs(total_lo), abs(total_hi)) >= 5))
            outputs.append(dict(arm=arm, basis="cash", end=end, specification=16 if end == "low" else 11,
                                identified_union_delta_bn=0.0, added_delta_low_bn=0.0, added_delta_high_bn=0.0,
                                lineage_delta_low_bn=0.0, lineage_delta_high_bn=0.0,
                                base_cost_bn=amt["base_cash_bn"], cost_low_bn=amt["base_cash_bn"],
                                cost_high_bn=amt["base_cash_bn"], cash_delta_bn=0.0, exceeds_5bn=False))
    write("case_changes.csv", outputs)
    write("generation_changes.csv", generation)
    cash_generation = [dict(r, basis="cash", oasdi_delta_bn=0.0, part_a_delta_bn=0.0,
                            delta_low_bn=0.0, delta_high_bn=0.0) for r in generation]
    write("generation_changes_cash.csv", cash_generation)
    write("added_profiles.csv", profile_output)
    comparisons = []
    frozen_c = pd.read_csv(WHITE / "derived/symmetric_comparisons_oct14.csv")
    frozen_r = pd.read_csv(WHITE / "derived/symmetric_results_oct14.csv")
    for source_arm in ("mortality_group", "mortality_symmetric_frame_status", "combined_rules_only"):
        selected = frozen_c[frozen_c.arm.eq(source_arm)]
        if selected.empty:
            continue
        for _, c in selected.iterrows():
            delta = next(r for r in outputs if r["arm"] == "central" and r["basis"] == c.basis and r["end"] == c.end)
            rs = frozen_r[(frozen_r.arm == source_arm) & (frozen_r.basis == c.basis) & (frozen_r.end == c.end)]
            u = float(rs[rs.group == "mexican_origin_engine"].iloc[0].cost_bn)
            b = float(rs[rs.group == "nh_black_rough"].iloc[0].cost_bn)
            w = float(rs[rs.group == "A1_third_plus_nh_white"].iloc[0].cost_bn)
            gate(f"{source_arm}/{c.basis}/{c.end} frozen comparisons trace to cost rows", abs(u - w - c.white_gap_case_lineage_bn) < 1e-9
                 and abs(b - u - c.black_minus_case_lineage_bn) < 1e-9)
            comparisons.append(dict(source_arm=source_arm, basis=c.basis, end=c.end,
                                    change="only lineage mortality; all comparator costs held fixed", lineage_base_cost_bn=u,
                                    black_cost_bn=b, white_cost_bn=w,
                                    lineage_new_cost_low_bn=u + delta["lineage_delta_low_bn"],
                                    lineage_new_cost_high_bn=u + delta["lineage_delta_high_bn"],
                                    white_gap_old_bn=c.white_gap_case_lineage_bn,
                                    white_gap_new_low_bn=c.white_gap_case_lineage_bn + delta["lineage_delta_low_bn"],
                                    white_gap_new_high_bn=c.white_gap_case_lineage_bn + delta["lineage_delta_high_bn"],
                                    black_minus_lineage_old_bn=c.black_minus_case_lineage_bn,
                                    black_minus_lineage_new_low_bn=c.black_minus_case_lineage_bn - delta["lineage_delta_high_bn"],
                                    black_minus_lineage_new_high_bn=c.black_minus_case_lineage_bn - delta["lineage_delta_low_bn"]))
    write("comparisons.csv", comparisons)
    audit = dict(controls=audits, denominator_sha256=denom_hash, denominator_unchanged=True,
                 general_controls_before_new_tables=True, parts_close_absolute_1e_9=True,
                 cash_zero_reason="Only future accrued OASDI/Part A liabilities and future benefit-tax timing change. Current cash benefits, taxes, population and every other line stay fixed.",
                 attribution="Identified delta by row4 actuarial CPS OASDI and HI payroll shares, common union benefit-tax rate. Not a replacement of the case's complete generation account.",
                 added_bound="Componentwise min/max relative mortality factors across the comparators' three measured age/profile combinations, all assigned US-born Mexican mortality. Not an identified exact added-dollar split.")
    (HERE / "derived/audit.json").write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n")
    peak = require_within_budget("lineage mortality")
    timing = dict(elapsed_seconds=time.perf_counter() - started, peak_physical_bytes=peak,
                  ru_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
    (HERE / "_cache/timing.json").write_text(json.dumps(timing, indent=2) + "\n")
    print(json.dumps(timing), flush=True)
    print(pd.DataFrame(outputs).query("basis == 'accrual'").to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
