"""Round 3 (C3 fix 3a): the lineage's own-mortality ratios under the comparators' left-out-share mix.

lineage_mortality_2026_10_14 prices the lineage's own mortality (Fenelon, Chinn and Anderson 2017 hazard ratios on the
NVSS 2024 NH-white tables) with the group factor on all of the ratio route's OASDI accrual. Round 3 moves only the
retirement part that the formula route models: the left-out share s(age), disability, children's and young survivors'
benefits, keeps the whole-population factor, as mortality_comparators.py now does for the white, Black and pooled
Hispanic rows. This script reprices that lane's central arm, the rows mortality_conventions.coefficients() reads (G1, G2
and G3+ on the row-4 frame, and the three added profiles), with the same mix on the live accrual module. Part A does not
change. The lane's frozen route, tables and frames are used as committed; nothing in that lane is written.

Controls before the mixed rows are admitted: without the mix, the live module reproduces the source's central and
general rows to 1e-9; under whole-population mortality the mix is the identity; Part A is identical with and without it.

Run from the repo root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/lineage_mortality_mix_oct15.py
Writes derived/lineage_mortality_mix_oct15.csv.
"""
from __future__ import annotations

import csv
import gc
import importlib.util
import json
import sys
import time
from pathlib import Path

sys.dont_write_bytecode = True
import pandas as pd

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
SOURCE = FISCAL / "lineage_mortality_2026_10_14"
OUT = LANE / "derived/lineage_mortality_mix_oct15.csv"
METRICS = ("oasdi_per_tax_dollar", "benefit_tax_timing", "oasdi_per_tax_dollar_net", "part_a_per_hi_tax_dollar",
           "cps_oasdi_tax_bn", "cps_hi_tax_bn")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod  # dataclasses resolve their module's namespace through sys.modules
    spec.loader.exec_module(mod)
    return mod


def gate(name, ok):
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}")
    print(f"[gate] {name}", flush=True)


class Mixed:
    """The live accrual module with the whole-population factor mixed on the left-out share."""

    def __init__(self, module, mix):
        self.module, self.mix = module, mix

    def oasdi_ratio(self, *args, **kwargs):
        return self.module.oasdi_ratio(*args, mix=self.mix, **kwargs)

    def part_a(self, *args, **kwargs):
        return self.module.part_a(*args, **kwargs)


def source_row(rows, **keys):
    sel = rows
    for k, v in keys.items():
        sel = sel[sel[k].eq(v)]
    gate(f"one source row {keys}", len(sel) == 1)
    return sel.iloc[0]


def same(row, ref, label, metrics=METRICS):
    gap = max(abs(row[k] - float(ref[k])) for k in metrics)
    gate(f"{label} reproduces the source (max gap {gap:.3g})", gap < 1e-9)


def main():
    started = time.perf_counter()
    LM = load("lineage_mortality_source", SOURCE / "mortality.py")
    LM.check_pins()
    MC = load("lineage_mix_comparators", LANE / "mortality_comparators.py")
    live = load("lineage_mix_white", LANE / "accrual_white.py")
    R = LM.Route()
    gate("live and frozen accrual modules share the pension module", live.P is R.P)
    m14 = json.loads((FISCAL / "main_case_2026_10_14/derived/corrections.json").read_text())["meta"]["lineage"]["age_mix"]
    m15 = json.loads((FISCAL / "main_case_2026_10_15/derived/corrections.json").read_text())["meta"]["lineage"]["age_mix"]
    gate("v8's added age mix is the source's", m14 == m15)
    source = pd.read_csv(SOURCE / "derived/accrual_ratios.csv")
    controls = pd.read_csv(SOURCE / "derived/reproduced_ratios.csv")
    paths = R.M.verify_tables(SOURCE)
    profiles = R.profiles()
    rows = []
    with R.M.table_context(R.P, paths):
        R.econ, grid, taus, R.paths = R.TP.payable(R.P, R.prelim)
        R.denominator = dict(mwr={R.TP.BASE: grid["mwr"][R.TP.BASE]})
        gate("general grid key is the central run", (R.P.CENTRAL["rate"], "general") == R.TP.G and R.TP.BASE == R.P.BASE)
        method = R.P.CENTRAL["method"]
        mix = dict(g=R.TP.G, share=MC.left_out_share(),
                   grid=dict(fams=grid["fams"], k={method: {R.TP.G: grid["k"][method][R.TP.G]}},
                             mwr={R.TP.G: grid["mwr"][R.TP.G], R.TP.BASE: grid["mwr"][R.TP.BASE]}))
        mixed = Mixed(live, mix)
        for name in ("G1", "G2", "G3plus"):
            ref = source_row(source, group=name, basis="row4", arm="general")
            for label, module in (("none", live), ("left_out_share", mixed)):
                r = R.price(R.p4, name, "general", grid, taus, module=module)
                same(r, ref, f"general {name} row4, mix {label}")
                rows.append(dict(r, basis="row4", arm="general", age_mix="observed", mix=label))
        for name, key, frame in profiles:
            ref = source_row(controls, group=name, basis="added_profile", age_mix=key, mortality="general")
            for label, module in (("none", live), ("left_out_share", mixed)):
                r = R.price(frame, name, "general", grid, taus, rel=R.rel_g3 if name == "G3plus" else 1.0, module=module)
                same(r, ref, f"general added {name}/{key}, mix {label}")
                rows.append(dict(r, basis="added_profile", arm="general", age_mix=key, mix=label))
        del grid
        gc.collect()
        reference = {sex: R.P.L.qx_table("nh_white", sex).copy() for sex in ("male", "female")}
        hazards = pd.read_csv(SOURCE / "derived/hazard_ratios.csv")
        tables = {f"central_{nat}": LM.build_qx(reference, hazards, "central", nat) for nat in ("foreign_born", "us_born")}
        with LM.synthetic_tables(R.P, tables):
            for nat, groups in (("foreign_born", ("G1",)), ("us_born", ("G2", "G3plus"))):
                pop = f"central_{nat}"
                grid, taus = R.grid(pop)
                priced = [(name, "row4", "observed", R.p4, None) for name in groups]
                if nat == "us_born":
                    priced += [(name, "added_profile", key, frame, R.rel_g3 if name == "G3plus" else 1.0)
                               for name, key, frame in profiles]
                for name, basis, key, frame, rel in priced:
                    if basis == "row4":
                        ref = source_row(source, group=name, basis="row4", arm="central")
                    else:
                        ref = source_row(source, group=name, basis="added_profile", age_mix=key, arm="central")
                    plain = R.price(frame, name, pop, grid, taus, rel=rel, module=live)
                    same(plain, ref, f"central {name}/{basis}/{key} without the mix")
                    r = R.price(frame, name, pop, grid, taus, rel=rel, module=mixed)
                    gate(f"central {name}/{basis}/{key} Part A and payroll unchanged by the mix",
                         all(r[k] == plain[k] for k in ("part_a_per_hi_tax_dollar", "cps_oasdi_tax_bn", "cps_hi_tax_bn")))
                    rows.append(dict(plain, basis=basis, arm="central", age_mix=key, mix="none"))
                    rows.append(dict(r, basis=basis, arm="central", age_mix=key, mix="left_out_share"))
                del grid
                gc.collect()
    gate("ten source rows priced both ways", len(rows) == 2 * (3 + 3 + 3 + 3))
    with OUT.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    out = pd.DataFrame(rows)
    view = out[out.arm.eq("central")][["group", "basis", "age_mix", "mix", "oasdi_per_tax_dollar_net",
                                        "part_a_per_hi_tax_dollar"]]
    print(view.to_string(index=False), flush=True)
    print(json.dumps(dict(seconds=time.perf_counter() - started)), flush=True)


if __name__ == "__main__":
    main()
