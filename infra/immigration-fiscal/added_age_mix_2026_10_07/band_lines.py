#!/usr/bin/env python3
"""Per-line age factors for the identified third-plus (G3+) and third-plus white (W) line amounts at any age mix, on
the white lane's rough re-key of the v4 case: the age route main_case_lineage_2026_10_05 white_lines.py uses for W,
extended to the G3+ members. price.cjs uses W from here; its central G3+ route is g3_age_keys.py's (the engine's own
keys by age, allocation by allocation), and the G3+ factors here are its cross-check route.

W at a mix: white_lines.py's own path (rekey_sept29.setup(), then run29 on scenario w3 reweighted to the mix), per
person and line, as the lineage lane's engine step reads white_lines.json. At the identified G3+'s mix it is
white_lines.json's g3plus_ages entry (gate).

G3+ at a mix: the engine's G3+ member (lineage_case.cjs G1: the corrected G3+ model per member) has no age dimension, so
its cells are multiplied line by line by f_line(mix) = rough G3+ amount at the mix / rough G3+ amount at the identified
mix. The rough G3+ is a scenario of the same library: CPS persons native, both parents US-born, Mexican origin (white_lines
.py's g3 mask), reweighted to the mix; MEPS persons US-born Hispanic (MEPS has neither parent birthplace nor Mexican
origin) [INFERENCE]; justice and LTSS by the library's age factors (crime-age and 65+ share, the white rules, whose
levels cancel in the ratio); accrual at the union's ratios; driving at Hispanic NHTS rates. A factor is a ratio of the
same group's keys at two age mixes, so only the age profile of each key enters, never its level.
  - lines the rough keys give 0 to a non-Mexican group (school_reprice, college_rekey, lane_constants, source_rounding):
    pupils, college enrolment, persons, persons (state_white.py ADJ_KEY);
  - the v4 difference lines (state_price_<line>: its parent line's factor; roads_vmt_sl/fed: the factor of k_road, the
    miles-and-consumption key the lines charge against the earnings key) [INFERENCE: a difference of two keys has no
    stable ratio];
  - lines held at zero (rest-of-world flows): 1;
  - the production term: the earnings (hi) key's factor.
At the identified mix every factor is exactly 1, so the lineage lane's G3+ member is reproduced bit for bit.

Mixes: age_mix.py's readings (each part), the identified mix, and the 17 unit bands (one band at 1), whose costs give
any mix's cost to first order (summarize.py's draws; the run's own non-linearity is gated there).
Gates (exit 1, nothing written): every positive control of the white lane's setup() passes; W at the identified mix is
white_lines.json's per line (1e-12 relative); every factor is finite and positive and exactly 1 at the identified mix;
the same amounts at both ends (no allocation arm in the rough keys).
Outputs: derived/band_lines.json, derived/gates_lines.json
Run from the repository root after age_mix.py:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/band_lines.py
"""
from __future__ import annotations

import contextlib
import io
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
WHITE = FISCAL / "white_replacement_2026_09_28"
WL = FISCAL / "main_case_lineage_2026_10_05/derived/white_lines.json"
BASES = ("accrual", "cash")
ENDS = ("low", "high")
ADJ_KEY = {"school_reprice": "k12", "college_rekey": "college", "lane_constants": "pc", "source_rounding": "pc"}
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def main() -> None:
    sys.path.insert(0, str(WHITE))
    print("[the white lane's library: setup (its positive controls; output kept to its failures)]", flush=True)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        import rekey_sept29 as W  # noqa: E402
        W.setup()
    log = buf.getvalue()
    failed = [ln for ln in log.splitlines() if "FAIL" in ln]
    gate("rekey_sept29.setup(): every positive control of the white lane passes", not failed and not W.FAILS,
         f"{log.count('PASS')} passes" + (f"; {failed[:3]}" if failed else ""))
    R = W.R
    d, md = R.d, R.md
    g3 = (d.PRCITSHP.isin([1, 2, 3]) & d.PEFNTVTY.isin(R.US) & d.PEMNTVTY.isin(R.US) & d.PRDTHSP.eq(1)).to_numpy()
    R.MASK["g3x"] = g3
    R.MMASK["g3x"] = (md.RACETHX.eq(1) & md.BORNUSA.ne(2)).to_numpy()   # US-born Hispanic (BORNUSA 2 = abroad)
    W.GROUP_OF["g3x"] = "union"
    W.RACE_RATES["g3x"] = "hispanic"
    if "hispanic" not in W.VRATE:   # the library builds three groups' rates; the NHTS file holds the Hispanic rows too
        W.VRATE["hispanic"] = (W.NHTS[(W.NHTS.group == "hispanic") & (W.NHTS.band != "all")]
                               .assign(band=lambda x: x.band.astype(int)).set_index("band").vmt_per_person)
    # Unit bands under 15 hold no adults and 0-4 no one aged 5+: the library's licence index and miles rate are then 0/0.
    # Their miles share is 0 (no drivers), so the index's value does not matter; set it to 1 and the share to 0.
    # Process-local wrappers, applied only where the library returns NaN; every other call is the library's.
    _miles, _index = W.miles_share, W.state_index

    def miles_share(sc, union_sc=None):
        s_, rho, u5 = _miles(sc, union_sc)
        return (0.0, 0.0, u5) if not np.isfinite(s_) else (s_, rho, u5)

    def state_index(cw):
        ix = _index(cw)
        if not np.isfinite(ix["licences"]):
            ix["licences"] = 1.0
        return ix
    W.miles_share, W.state_index = miles_share, state_index
    ident = R.structure(g3, R.w, R.cage)
    wl = json.loads(WL.read_text())
    gate("the identified mix recomputed here is white_lines.json's g3plus structure, exactly",
         [float(x) for x in ident] == wl["meta"]["age_structures"]["g3plus"])
    mixes = json.loads((OUT / "age_mix.json").read_text())
    pis = {"identified": np.asarray(ident, float)}
    for name, x in mixes["readings"].items():
        if name == "flat":
            continue
        for part in ("g3_rate", "later"):
            pis[f"{name}|{part}"] = np.asarray(x[part], float)
    nb = len(R.BANDS)
    for i in range(nb):
        pis[f"band|{i}"] = np.eye(nb)[i]

    def scen(g, name, pi):
        R.PI[name] = pi
        return R.scenario(g, name)

    base = {}
    for b in BASES:
        sc = scen("g3x", "identified", pis["identified"])
        rows = {}
        for end in ENDS:
            r, rr, _, terms, _ = W.run29(sc, end, b)
            rows[end] = ({f"{s}|{lid}": a for s, lid, nat, a, resp in rr}, terms)
        same = max(abs(rows["low"][0][k] - rows["high"][0][k]) for k in rows["low"][0])
        gate(f"g3x {b}: the rough G3+ amounts are the same at both ends", same == 0.0, f"{same:.1e}")
        base[b] = (rows["low"][0], rows["low"][1], sc)
    lines = list(base["accrual"][0])
    sp_parent = {lid: x["parent"] for lid, x in W.SP_LINES.items()}

    def factors(b, sc, amt, terms):
        a0, t0, s0 = base[b]
        f = {}
        for k in lines:
            side, lid = k.split("|", 1)
            if lid in R.ZERO:
                f[k] = 1.0
            elif lid in ADJ_KEY:
                f[k] = sc["share"][ADJ_KEY[lid]] / s0["share"][ADJ_KEY[lid]]
            elif lid in ("roads_vmt_sl", "roads_vmt_fed"):
                f[k] = terms["k_road"] / t0["k_road"]
            elif lid in sp_parent:
                p = f"spending|{sp_parent[lid]}"
                f[k] = amt[p] / a0[p]
            else:
                f[k] = amt[k] / a0[k] if a0[k] != 0 else float("nan")
        return f, sc["share"]["hi"] / s0["share"]["hi"]

    out = {}
    for name, pi in pis.items():
        out[name] = {"pi": pi.tolist(), "g3x": {}, "white": {}}
        for b in BASES:
            sc = scen("g3x", name, pi)
            r, rr, _, terms, _ = W.run29(sc, "low", b)
            amt = {f"{s}|{lid}": a for s, lid, nat, a, resp in rr}
            f, fprod = factors(b, sc, amt, terms)
            out[name]["g3x"][b] = {"factors": f, "production_factor": fprod, "k_road": terms["k_road"],
                                   "cost_rough_bn": r["cost"], "population": r["population"]}
            sw = scen("w3", name, pi)
            rw, rwr, _, _, _ = W.run29(sw, "low", b)
            pop = float(sw["population"])
            out[name]["white"][b] = {"lines": {f"{s}|{lid}": a / pop for s, lid, nat, a, resp in rwr},
                                     "cost_rough_bn_per_person": rw["cost"] / pop, "population": pop}
    bad = [(n, b, k) for n, x in out.items() for b in BASES for k, v in x["g3x"][b]["factors"].items()
           if not (np.isfinite(v) and (v > 0 or (n.startswith("band|") and v == 0)))]
    gate("every G3+ factor is finite and positive (zero only in a unit band: children pay no payroll tax)", not bad,
         f"{bad[:5]}")
    one = all(v == 1.0 for b in BASES for v in out["identified"]["g3x"][b]["factors"].values()) and all(
        out["identified"]["g3x"][b]["production_factor"] == 1.0 for b in BASES)
    gate("at the identified mix every G3+ factor is exactly 1", one)
    worst = 0.0
    for b in BASES:
        want = wl["g3plus_ages"][b]["low"]
        wmap = {f"{x['side']}|{x['id']}": x["amount_bn"] / want["population"] for x in want["lines"]}
        got = out["identified"]["white"][b]["lines"]
        worst = max(worst, max(abs(got[k] - wmap[k]) / max(abs(wmap[k]), 1e-12) for k in wmap), 0.0 if set(got) == set(wmap) else 1.0)
    gate("W at the identified mix is white_lines.json's g3plus_ages per person, every line (1e-12 relative)", worst < 1e-12, f"{worst:.1e}")
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    OUT.mkdir(exist_ok=True)
    meta = {"source": "added_age_mix_2026_10_07/band_lines.py", "bands": wl["meta"]["age_structures"]["band"],
            "rule": "G3+ cells x factor(line, mix); W per person and line at the mix (white_lines.py's path)",
            "g3x_meps": "US-born Hispanic (RACETHX 1, BORNUSA not 2)", "adj_key": ADJ_KEY}
    (OUT / "band_lines.json").write_text(json.dumps({"meta": meta, "mixes": out}) + "\n")
    (OUT / "gates_lines.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    for name in ["identified"] + [n for n in out if not n.startswith("band|") and n != "identified"]:
        x = out[name]
        print(f"  {name:<40} rough G3+ ${x['g3x']['accrual']['cost_rough_bn'] * 1e9 / x['g3x']['accrual']['population']:,.0f}"
              f" / cash ${x['g3x']['cash']['cost_rough_bn'] * 1e9 / x['g3x']['cash']['population']:,.0f};"
              f" W ${x['white']['accrual']['cost_rough_bn_per_person'] * 1e9:,.0f} / ${x['white']['cash']['cost_rough_bn_per_person'] * 1e9:,.0f}")


if __name__ == "__main__":
    main()
