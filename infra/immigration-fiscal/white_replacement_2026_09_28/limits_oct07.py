#!/usr/bin/env python3
"""Three limits of the v6 (oct07) figures, sized read-only through this lane's library (rekey_sept29.py at oct07).

The team lead's decisions of 2026-10-07 keep each out of the central; this script sizes them for the RESULT's v6
section ("Limits of the v6 figures") and the lead's revisit items.

1. The case's own W. The case prices 1,082,721 members of the lineage as third-plus non-Hispanic whites
   (meta.lineage.members.white) on lines that come from main_case_lineage_2026_10_05/white_lines.py and
   added_age_mix_2026_10_07/band_lines.py, which import this library at its sept29 default: the rough keys of
   September 27, with income taxes on the CPS-dollar rule. On the IPEDS keys, and beside them item 4's tuition term,
   their cost per person moves by the amounts written here, at three age structures: the G3-rate persons' measured mix
   (v6's placement of the white end, meta.lineage.age_mix), the identified G3+ members' ages (v5's) and whites' own
   ages. Times the count, the case's move. Round 2 (the team lead, 2026-10-07: measure only) adds the move to the
   comparators' central income-tax keys, the case's own (CASE_TAX_KEY, the shared allocation; the personal one beside).
2. Item 4's Pell share at IPEDS's Hispanic private/public undergraduate enrollment ratio (0.6768, ipeds_keys.json) in
   place of the fee lane's assumed 0.75, by the fee lane's rule (the private share is the public share times the
   ratio, weighted 0.32 against 0.68). The share's change times Pell's $31.264bn is the term's move at either end's
   benefit-tax rule; the case's other_federal_benefits response is 1.
3. Tuition residency θ for a race at 0.5 and 1.5 (the central is 1; the union keeps the fee lane's 0.5): every race's
   tuition share from ipeds_keys.json's arms, on the rough union, A1, A3 and the NH Black group.

Gates (exit 1, nothing written): the library's setup; the white count is the payload's; the G3-rate mix sums to 1, has
no band without identified G3+ and is v5's placement when the identified mix stands in for it (the structure is the
age_tilt rule's); the three income-tax nationals are the sept29 dumps' (W's lines come from them); W's move to the
case's income-tax keys is minus the three lines' move (1e-9); positive controls on the cash basis, W's CPS-rule
income-tax amounts a person at the identified G3+'s ages are white_lines.json's and at the G3-rate mix band_lines.json's
(1e-9 relative); the share formula reproduces the fee lane's central and its 0.5 and 1.0 arms with their personal
terms (1e-12, 1e-9); every case dump's other_federal_benefits response is 1; at the central θ each group's cost is
rekey_summary_oct07.csv's (5e-5) and the union's cost does not move with a race's θ (1e-12).
Output: derived/limits_oct07.csv. Run from the repository root after rekey_sept29.py --case oct07:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/limits_oct07.py
"""
from __future__ import annotations

import contextlib
import csv
import io
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
sys.path.insert(0, str(LANE))
import rekey_sept29 as W  # noqa: E402

FAILS: list[str] = []
GROUPS = ["mexican_origin_rough", "A1_third_plus_nh_white", "A3_third_plus_nh_white_at_union_ages", "nh_black_rough"]


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def case_w(rows, meta):
    """1. The case's W per person on the IPEDS keys (and the tuition term beside) and on the case's income-tax keys
    (round 2, both allocations), at three age structures. Every move starts from the CPS-dollar rule W's lines keep."""
    R = W.R
    d = R.d
    am = meta["lineage"]["age_mix"]
    g3 = (d.PRCITSHP.isin([1, 2, 3]) & d.PEFNTVTY.isin(R.US) & d.PEMNTVTY.isin(R.US) & d.PRDTHSP.eq(1)).to_numpy()
    ident = R.structure(g3, R.w, R.cage)
    g3_rate = np.asarray(am["mixes"]["g3_rate"], float)
    gate("the frame's identified G3+ ages are the age-mix lane's identified mix, exactly",
         [float(x) for x in ident] == am["mixes"]["identified"])
    gate("the G3-rate mix sums to 1 and has no band without identified G3+ (1e-12)",
         abs(g3_rate.sum() - 1) < 1e-12 and not ((ident <= 0) & (g3_rate > 0)).any())
    tax = tuple(W.CASE_TAX_KEY)
    s29 = json.loads((DER / "engine_lines_sept29_cash.json").read_text())
    for lid in tax:
        a = next(x for x in s29["low"]["lines"] if x["side"] == "receipts" and x["id"] == lid)["national_bn"]
        gate(f"{lid}: the sept29 national is oct07's (W's lines come from sept29)", a == R.NATIONAL["receipts|" + lid],
             f"{a} vs {R.NATIONAL['receipts|' + lid]}")
    wl = json.loads((FISCAL / "main_case_lineage_2026_10_05/derived/white_lines.json").read_text())
    bl = json.loads((FISCAL / "added_age_mix_2026_10_07/derived/band_lines.json").read_text())
    band = next(k for k, v in bl["mixes"].items() if v["pi"] == am["mixes"]["g3_rate"])
    personal = {k: v + "_personal" for k, v in W.CASE_TAX_KEY.items()}
    R.PI["case_w_g3_rate"], R.PI["case_w_identified"] = g3_rate, ident
    n_white = meta["lineage"]["members"]["white"]
    for arm, sc in (("g3_rate_mix", R.scenario("w3", "case_w_g3_rate")),
                    ("identified_g3plus_ages", R.scenario("w3", "case_w_identified")),
                    ("white_own_ages", R.scenario("w3"))):
        pop = float(sc["population"])
        for basis in W.BASES:
            for end in W.ENDS:
                with W.patched(vars(W), IPEDS_ON=False, FEES_ON=False):
                    rough = W.run29(sc, end, basis, "cps")[0]["cost"]
                with W.patched(vars(W), FEES_ON=False):
                    keys = W.run29(sc, end, basis, "cps")[0]["cost"]
                r_cps, lines_cps = W.run29(sc, end, basis, "cps")[:2]
                full = r_cps["cost"]
                cps_pp = {x[1]: x[3] * 1e9 / pop for x in lines_cps if x[0] == "receipts" and x[1] in tax}
                if basis == "cash" and arm != "white_own_ages":
                    ref = ({x["id"]: x["per_person_usd"] for x in wl["g3plus_ages"]["cash"][end]["lines"]
                            if x["side"] == "receipts"} if arm == "identified_g3plus_ages" else
                           {lid: bl["mixes"][band]["white"]["cash"]["lines"]["receipts|" + lid] * 1e9 for lid in tax})
                    gate(f"positive control, cash {end}: W's CPS-rule income taxes a person at {arm} are "
                         f"{'white_lines.json' if arm == 'identified_g3plus_ages' else 'band_lines.json ' + band}'s "
                         f"(1e-9 rel.)", all(abs(cps_pp[x] - ref[x]) <= 1e-9 * abs(ref[x]) for x in tax),
                         ", ".join(f"{x} {cps_pp[x]:.4f}/{ref[x]:.4f}" for x in tax))
                case = {}
                for alloc, key in (("shared", W.CASE_TAX_KEY), ("personal", personal)):
                    with W.patched(vars(W), CASE_TAX_KEY=key):
                        r, lines = W.run29(sc, end, basis)[:2]
                    move = sum((a[3] - b[3]) * a[4] for a, b in zip(lines, lines_cps)
                               if a[0] == "receipts" and a[1] in tax)
                    gate(f"case W {arm} {basis} {end} ({alloc}): the move to the case's income-tax keys is minus the "
                         f"three lines' move (1e-9)", abs((r["cost"] - full) + move) < 1e-9
                         and [a[:3] for a in lines] == [b[:3] for b in lines_cps], f"{r['cost'] - full:+.6f}")
                    case[alloc] = r["cost"]
                for item, v in (("ipeds_keys", keys - rough), ("tuition_beside", full - keys),
                                ("income_tax_keys", case["shared"] - full),
                                ("income_tax_keys_personal", case["personal"] - full)):
                    pp = v * 1e9 / pop
                    rows.append(dict(item=f"case_w_{item}", arm=arm, basis=basis, end=end, per_person_usd=f"{pp:.4f}",
                                     count=f"{n_white:.4f}", bn=f"{pp * n_white / 1e9:.6f}"))
                print(f"  case W {arm:22s} {basis:7s} {end:4s} rough ${rough * 1e9 / pop:9.2f} a person; IPEDS keys "
                      f"${(keys - rough) * 1e9 / pop:+8.2f}; tuition beside ${(full - keys) * 1e9 / pop:+6.2f}; the "
                      f"case's income-tax keys ${(case['shared'] - full) * 1e9 / pop:+9.2f} (personal "
                      f"${(case['personal'] - full) * 1e9 / pop:+9.2f})")


def pell_hispanic(rows):
    """2. Item 4's Pell share at IPEDS's Hispanic private/public ratio, by the fee lane's rule."""
    ik = json.loads((DER / "ipeds_keys.json").read_text())
    fee = json.loads((FISCAL / "user_fee_allocation_2026_10_07/derived/fee_lines.json").read_text())
    c, pell = ik["constants"], fee["pell"]
    share, s_personal = pell["share"], pell["s_cash_union"]["personal"]

    def at(ratio):
        return share * (c["pell_public"] + (1 - c["pell_public"]) * ratio) / (
            c["pell_public"] + (1 - c["pell_public"]) * c["pell_private_relative_union"])

    gate("the union's Pell share is the fee lane's and ipeds_keys.json's (1e-15)",
         abs(share - ik["union"]["pell"]) < 1e-15 and abs(at(c["pell_private_relative_union"]) - share) < 1e-15)
    arm = {a["private"]: a for a in pell["arms"] if a["public"] == "central" and a["intensity"] == "mid"}
    for name, ratio in (("low", 0.5), ("high", 1.0)):
        got = at(ratio)
        term = (got - s_personal) * c["pell_bn"]
        gate(f"positive control: the rule at private/public {ratio} gives the fee lane's '{name}' arm's share (1e-12) "
             f"and personal term (1e-9)",
             abs(got - arm[name]["share"]) < 1e-12 and abs(term - arm[name]["term_personal_bn"]) < 1e-9,
             f"{got:.12f} vs {arm[name]['share']:.12f}")
    for basis in W.BASES:
        for end in W.ENDS:
            r = next(x for x in W.FULL[basis][end]["lines"] if x["id"] == "other_federal_benefits")["response"]
            gate(f"the case's other_federal_benefits response is 1 ({basis}, {end})", r == 1, f"{r}")
    ratio = ik["private_public_enrollment"]["hispanic"]["ratio"]
    got = at(ratio)
    move = (got - share) * c["pell_bn"]
    rows.append(dict(item="pell_hispanic_ratio", arm=f"{ratio:.6f} for 0.75", basis="both", end="both",
                     per_person_usd="", count="", bn=f"{move:.6f}"))
    print(f"  item 4's Pell share {share:.6f} at 0.75; {got:.6f} at IPEDS's Hispanic {ratio:.4f}: the term moves "
          f"{move:+.4f}bn")


def theta_arms(rows, scen):
    """3. A race's tuition residency θ at 0.5 and 1.5."""
    summary = pd.read_csv(DER / "rekey_summary_oct07.csv")
    saved = {r: W.IK["races"][r]["tuition"] for r in W.IK["races"]}
    cost = {}
    try:
        for arm in ("central", "0.5", "1.5"):
            for r in W.IK["races"]:
                W.IK["races"][r]["tuition"] = saved[r] if arm == "central" else W.IK["races"][r]["tuition_arms"][arm]
            for basis in W.BASES:
                for end in W.ENDS:
                    for g in GROUPS:
                        cost[(arm, basis, end, g)] = W.run29(scen[g], end, basis)[0]["cost"]
    finally:
        for r, v in saved.items():
            W.IK["races"][r]["tuition"] = v
    for basis in W.BASES:
        for end in W.ENDS:
            for g in GROUPS:
                want = summary[(summary.basis == basis) & (summary.group == g) & (summary.end == end)].cost.iloc[0]
                gate(f"θ central: {g} ({basis}, {end}) is rekey_summary_oct07.csv's (5e-5)",
                     abs(cost[("central", basis, end, g)] - want) < 5e-5)
            u = [cost[(a, basis, end, "mexican_origin_rough")] for a in ("central", "0.5", "1.5")]
            gate(f"the union's cost does not move with a race's θ ({basis}, {end}; 1e-12)", max(u) - min(u) < 1e-12)
            for arm in ("central", "0.5", "1.5"):
                union = cost[(arm, basis, end, "mexican_origin_rough")]
                for g in GROUPS[1:]:
                    c = cost[(arm, basis, end, g)]
                    value = c if g == "nh_black_rough" else union - c
                    rows.append(dict(item="theta_" + ("nh_black_cost" if g == "nh_black_rough" else g.split("_")[0] + "_gap"),
                                     arm=arm, basis=basis, end=end, per_person_usd="", count="", bn=f"{value:.6f}"))
                if basis == "accrual":
                    print(f"  θ {arm:7s} {end:4s} A1 gap {union - cost[(arm, basis, end, GROUPS[1])]:9.4f}  A3 gap "
                          f"{union - cost[(arm, basis, end, GROUPS[2])]:9.4f}  NH Black {cost[(arm, basis, end, GROUPS[3])]:9.4f}")


def main():
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        W.use_case("oct07")
        W.setup()
        scen = W.scenarios()
    fails = [ln for ln in buf.getvalue().splitlines() if "FAIL" in ln]
    if fails or W.FAILS:
        print(buf.getvalue())
        raise SystemExit(f"[BLOCKED] the library's oct07 setup failed: {fails[:3]}")
    print(f"the library's oct07 setup: {buf.getvalue().count('PASS')} gates passed")
    meta = json.loads((FISCAL / "main_case_2026_10_07/derived/corrections.json").read_text())["meta"]
    gate("the case's white members are the library's payload's (exact)",
         meta["lineage"]["members"]["white"] == W.LINEAGE["members"]["white"], f"{meta['lineage']['members']['white']:,.3f}")
    rows: list[dict] = []
    case_w(rows, meta)
    pell_hispanic(rows)
    theta_arms(rows, scen)
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    with open(DER / "limits_oct07.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    print(f"[written] derived/limits_oct07.csv: {len(rows)} rows")


if __name__ == "__main__":
    main()
