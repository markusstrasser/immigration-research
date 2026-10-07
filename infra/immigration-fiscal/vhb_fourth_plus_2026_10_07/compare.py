#!/usr/bin/env python3
"""Positive control against the lineage lane's bands, the VHB arms' bands beside v5, and the Hispanic-channel check.

1. Every v5_bands.csv row of arms floor, a, b and c written by this lane's lineage_case.cjs copy equals the
   main_case_lineage_2026_10_05 row to 1e-6 (each numeric column), and every row of that lane is present here.
2. derived/vhb_bands.csv: each arm's central band on the set and the cash set, the change from v5 (arm b) and from v4,
   and per member of the lineage.
3. derived/hispanic_channel.csv: the hidden fourth-plus each arm implies (added - the floor's added, i.e. the
   self-identified fourth-plus x (1/p4 - 1), CPS frame), the part that would still report Hispanic at VHB's fourth-plus
   retention ((82.8 - 51.0) / (100 - 51.0)) and at the CPS child-stage retention for children of G3+ parents
   (1 - not Hispanic / not Mexican, civic_trajectory_mexican_2026_09_27 identity_loss.csv, three couple types), against
   the CPS stock of third-plus "Other Hispanic" (benchmark.py), which caps the first.

Run from the repository root after lineage_case.cjs:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/vhb_fourth_plus_2026_10_07/compare.py
"""
from __future__ import annotations

import csv
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
LIN5 = FISCAL / "main_case_lineage_2026_10_05/derived"
IDLOSS = FISCAL / "civic_trajectory_mexican_2026_09_27/derived/identity_loss.csv"
CONTROL_ARMS = ("floor", "a", "b", "c")
TOL = 1e-6
GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'✓' if ok else '✗'} {name}{' - ' + detail if detail else ''}", flush=True)


def rows(path: Path) -> list[dict]:
    with path.open(newline="") as f:
        return list(csv.DictReader(f))


def write(path: Path, recs: list[dict]) -> None:
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(recs[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(recs)


def main() -> None:
    print("[positive control: lineage lane bands]", flush=True)
    mine = {(r["set"], r["arm"], r["variant"]): r for r in rows(OUT / "v5_bands.csv")}
    theirs = {(r["set"], r["arm"], r["variant"]): r for r in rows(LIN5 / "v5_bands.csv")}
    missing = [k for k in theirs if k not in mine]
    gate("every lineage-lane band row is present here", not missing, f"{len(theirs)} rows; missing {missing[:3]}")
    num = ["low_bn", "high_bn", "change_low_bn", "change_high_bn", "population", "per_member_low_usd",
           "per_member_high_usd", "m_g3plus", "m_white"]
    worst, worst_key = 0.0, None
    for k, t in theirs.items():
        for c in num:
            d = abs(float(mine[k][c]) - float(t[c]))
            if d > worst:
                worst, worst_key = d, (k, c)
    gate(f"floor, a, b, c, v4: every numeric column equals the lineage lane's ({TOL:g})", worst <= TOL,
         f"max |diff| {worst:.2e} at {worst_key}")
    gate("the rule text of every control row is unchanged", all(mine[k]["rule"] == t["rule"] for k, t in theirs.items()))

    pop = json.loads((OUT / "population.json").read_text())["arms"]
    p4 = {r["arm"]: float(r["p4_effective"]) for r in rows(OUT / "arms_vhb.csv") if r["arm"].startswith("vhb_")}
    p4.update({"b": float(next(r for r in rows(OUT / "arms_vhb.csv") if r["arm"].startswith("b_one_step"))["p4_effective"])})
    arms = [a for a in pop if a != "floor"]
    out = []
    for arm in arms:
        rec = {"arm": arm, "p4_effective": f"{p4[arm]:.6f}" if arm in p4 else "",
               "added_account": f"{pop[arm]['added']:.1f}", "g3_rate_account": f"{pop[arm]['g3_rate']:.1f}",
               "later_account": f"{pop[arm]['later']:.1f}", "lineage_population": f"{pop[arm]['population']:.1f}"}
        for s in ("set", "cash"):
            r, b, v4 = mine[(s, arm, "central")], mine[(s, "b", "central")], mine[(s, "v4", "adopted v4")]
            lo, hi = float(r["low_bn"]), float(r["high_bn"])
            rec.update({f"{s}_low_bn": f"{lo:.6f}", f"{s}_high_bn": f"{hi:.6f}",
                        f"{s}_change_from_v5_low_bn": f"{lo - float(b['low_bn']):.6f}",
                        f"{s}_change_from_v5_high_bn": f"{hi - float(b['high_bn']):.6f}",
                        f"{s}_change_from_v4_low_bn": f"{lo - float(v4['low_bn']):.6f}",
                        f"{s}_change_from_v4_high_bn": f"{hi - float(v4['high_bn']):.6f}",
                        f"{s}_per_member_low_usd": f"{float(r['per_member_low_usd']):.2f}",
                        f"{s}_per_member_high_usd": f"{float(r['per_member_high_usd']):.2f}"})
        out.append(rec)
    write(OUT / "vhb_bands.csv", out)

    print("[Hispanic channel]", flush=True)
    vhb = {r["generation"]: r for r in rows(OUT / "vhb_table_2_1.csv")}
    m4, h4 = float(vhb["G4+"]["pct_id_mexican"]), float(vhb["G4+"]["pct_id_hispanic"])
    keep_vhb = (h4 - m4) / (100 - m4)
    il = [r for r in rows(IDLOSS) if r["generation"] == "mex_G3plus" and r["adjustment"].startswith("three couple types")]
    nm = next(float(r["estimate"]) for r in il if r["measure"] == "child-stage loss: not reported mexican")
    nh = next(float(r["estimate"]) for r in il if r["measure"] == "child-stage loss: not reported hispanic")
    keep_cps = 1 - nh / nm
    other = next(float(r["persons"]) for r in rows(OUT / "cps_third_plus_hispanic_detail.csv")
                 if r["ages"] == "all ages" and r["origin"] == "Other Hispanic")
    floor_cps = pop["floor"]["added_cps"]
    ch = []
    for arm in arms:
        hid = pop[arm]["added_cps"] - floor_cps
        ch.append({"arm": arm, "hidden_fourth_plus_cps": f"{hid:.1f}",
                   "still_hispanic_at_vhb_retention": f"{hid * keep_vhb:.1f}",
                   "still_hispanic_at_cps_retention": f"{hid * keep_cps:.1f}",
                   "cps_third_plus_other_hispanic": f"{other:.1f}",
                   "vhb_retention": f"{keep_vhb:.6f}", "cps_retention": f"{keep_cps:.6f}"})
        print(f"  {arm:<18} hidden G4+ {hid / 1e6:.3f}M; still Hispanic at VHB's {keep_vhb:.3f}: {hid * keep_vhb / 1e6:.3f}M, "
              f"at the CPS's {keep_cps:.3f}: {hid * keep_cps / 1e6:.3f}M; CPS third-plus Other Hispanic {other / 1e6:.3f}M")
    write(OUT / "hispanic_channel.csv", ch)
    (OUT / "gates_compare.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed")
    print("[bands, central]")
    for r in out:
        print(f"  {r['arm']:<18} added {float(r['added_account']) / 1e6:.4f}M  set {float(r['set_low_bn']):.2f}-"
              f"{float(r['set_high_bn']):.2f} ({float(r['set_change_from_v5_low_bn']):+.2f} / "
              f"{float(r['set_change_from_v5_high_bn']):+.2f} on v5)  cash {float(r['cash_low_bn']):.2f}-"
              f"{float(r['cash_high_bn']):.2f}  per member ${float(r['set_per_member_low_usd']):,.0f}-"
              f"{float(r['set_per_member_high_usd']):,.0f}")


if __name__ == "__main__":
    main()
