#!/usr/bin/env python3
"""Ancestry shares for the people-conserving lineage count (the fractional sensitivity), on the account's CPS frame.

Each person counts by their share of Mexican-immigrant ancestry: the bookkeeping of lineage_cost_2026_09_19's
`per_capita` rule (TFR/2, each child shared between two parents), the only attribution that counts every person once
across all lineages. A Mexico-born person counts 1; a US-born person counts half of each parent's share, so one half per
Mexico-born parent and one quarter per Mexico-born grandparent. A parent born abroad outside Mexico, or a US-born
parent who does not report Mexican origin, contributes nothing [ASSUMPTION]. The added (hidden) persons take their
measured mix from population.json (a quarter per Mexico-born grandparent over the hidden third generation's cells).

What the CPS shows:
  G1    born in Mexico: 1.
  G2    both parents' birthplaces (PEMNTVTY, PEFNTVTY) for everyone. When the other parent is US-born, that parent's
        Mexican origin and own parents' birthplaces are seen only if they are a co-resident biological parent (PEPAR1/2,
        type 1, matched by sex); otherwise their share is unknown, between 0 and 1, and the person's between 1/2 and 1.
  G3plus grandparents' birthplaces only through co-resident biological parents' records (both parents: all four;
        one: two). Adults living apart from their parents show nothing, so their share is bounded by 0 and 1.
An unknown ancestor contributes between nothing and its full weight; every share is written as low and high bounds.
The G2 central gives each unknown other parent the mean share measured on co-resident US-born other parents
[ASSUMPTION: adults' parents resemble children's parents; intermarriage changed across cohorts]. The G3plus central is
the population lane's convention, the identified third-generation children's quarter-per-grandparent mix (0.6156,
recomputed from arm3_grandparent_counts.csv), applied to every identified third-plus member; this frame's own
measurement on co-resident children is written beside.

Costs are not split here. The account splits keys, corrections and production by generation only
(generation_account_2026_09_24), so lineage_case.cjs prices each generation's share at that generation's average cost
per member; the G2 class indicators written here (under-18 share, BA+ among adults 25+) show the direction of that
approximation.

Inputs : ../generation_account_2026_09_24/frame.py and its cached CPS ASEC 2025 frame (read-only: the script stops if
         the cache is missing rather than let frame.load() write it)
         ../generation_account_2026_09_24/derived/generation_results_sept29.csv (populations)
         ../mexican_origin_population_total_2026_09_19/derived/arm3_grandparent_counts.csv
         derived/population.json (the added persons' measured mix)
Outputs: derived/fractional_shares.json, derived/fractional_classes.csv, derived/gates_fractional.json
Run from the repository root, after population.py:
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_lineage_2026_10_05/fractional.py
"""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
GEN_LANE = FISCAL / "generation_account_2026_09_24"
GEN = GEN_LANE / "derived/generation_results_sept29.csv"
GRANDPARENTS = FISCAL / "mexican_origin_population_total_2026_09_19/derived/arm3_grandparent_counts.csv"
POP = OUT / "population.json"

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str = "") -> None:
    GATES.append({"gate": name, "passed": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}{' - ' + detail if detail else ''}", flush=True)


def main() -> None:
    sys.path.insert(0, str(GEN_LANE))
    import frame as F  # noqa: E402  read-only: the account's frame, masks and parent links
    if not (F.CACHE / "asec25_generation.parquet").exists():
        raise SystemExit("[BLOCKED] the generation account's cached frame is missing; frame.load() would write it there")
    print("[frame]", flush=True)
    d = F.load()
    civilian, union, gens = F.masks(d)
    n = len(d)
    w = d.pwwgt0.to_numpy(float)
    pops = {r["generation"]: float(r["population"]) for r in csv.DictReader(GEN.open()) if r["convention"] == "a"}
    for g in ("G2", "G3plus"):
        got = float(w[gens[g]].sum())
        gate(f"{g}: the frame's weights give generation_results_sept29.csv's population (1 person)",
             abs(got - pops[g]) < 1.0, f"{got:,.2f} vs {pops[g]:,.2f}")

    pen, pem, pef = (d[c].to_numpy() for c in ("PENATVTY", "PEMNTVTY", "PEFNTVTY"))
    mex_origin = d.PRDTHSP.to_numpy() == 1
    sex, age, hga = d.A_SEX.to_numpy(), d.A_AGE.to_numpy(), d.A_HGA.to_numpy()
    us = lambda x: np.isin(x, F.US_AREAS)  # noqa: E731
    mx = lambda x: x == F.MEXICO  # noqa: E731
    rows_ = F.parent_rows(d)
    typ = d[["PEPAR1TYP", "PEPAR2TYP"]].to_numpy()
    bio = np.where((rows_ >= 0) & (typ == 1), rows_, -1)  # co-resident biological parents

    def parent_of_sex(want: np.ndarray) -> np.ndarray:
        """Row of the co-resident biological parent of sex `want` (1 father, 2 mother), -1 if none."""
        out = np.full(n, -1)
        for slot in (0, 1):
            p = bio[:, slot]
            hit = (p >= 0) & (out < 0)
            hit &= sex[np.where(p >= 0, p, 0)] == want
            out[hit] = p[hit]
        return out

    father, mother = parent_of_sex(np.full(n, 1)), parent_of_sex(np.full(n, 2))

    def own_bounds(j: np.ndarray, mex: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """Share bounds of persons j from their own parents' birthplaces: a Mexico-born parent 1/2, a parent born
        abroad elsewhere 0, a US-born parent between 0 and 1/2 if j reports Mexican origin, else 0."""
        lo = 0.5 * (mx(pem[j]).astype(float) + mx(pef[j]).astype(float))
        unknown = 0.5 * (us(pem[j]).astype(float) + us(pef[j]).astype(float))
        return lo, lo + np.where(mex, unknown, 0.0)

    lo = np.full(n, np.nan)
    hi = np.full(n, np.nan)
    cls = np.full(n, "", dtype=object)

    # G2: one half per Mexico-born parent plus half the other parent's own share.
    g2 = gens["G2"]
    k = mx(pem).astype(int) + mx(pef).astype(int)
    two = g2 & (k == 2)
    lo[two] = hi[two] = 1.0
    cls[two] = "G2: two Mexico-born parents"
    one = g2 & (k == 1)
    other_bp = np.where(mx(pem), pef, pem)
    other_row = np.where(mx(pem), father, mother)
    abroad = one & ~us(other_bp)
    lo[abroad] = hi[abroad] = 0.5
    cls[abroad] = "G2: other parent born abroad outside Mexico"
    usb = one & us(other_bp)
    seen = usb & (other_row >= 0)
    p = other_row[seen]
    p_lo, p_hi = own_bounds(p, mex_origin[p])
    not_mex = ~mex_origin[p]
    lo[seen], hi[seen] = 0.5 + 0.5 * p_lo, 0.5 + 0.5 * p_hi
    seen_idx = np.flatnonzero(seen)
    cls[seen_idx[not_mex]] = "G2: US-born other parent at home, not of Mexican origin"
    cls[seen_idx[~not_mex]] = "G2: US-born other parent at home, of Mexican origin"
    unseen = usb & (other_row < 0)
    lo[unseen], hi[unseen] = 0.5, 1.0
    cls[unseen] = "G2: US-born other parent not at home (unknown)"
    gate("G2: every member is in exactly one class (two Mexico-born parents, other abroad, US-born seen, US-born unseen)",
         not np.isnan(lo[g2]).any() and np.array_equal(g2, two | abroad | seen | unseen))
    # Central for the unknown class: the measured mean share of co-resident US-born other parents.
    s_other_seen = float(np.average(0.5 * (p_lo + p_hi), weights=w[seen]))
    central = np.where(unseen, 0.5 + 0.5 * s_other_seen, 0.5 * (lo + hi))

    # G3plus: half of each parent's share; a co-resident parent's share from their own parents' birthplaces, an
    # absent parent's between 0 and 1. The strict quarter-per-Mexico-born-grandparent rule is the low bound.
    g3 = gens["G3plus"]
    half_lo = np.zeros(n)
    half_hi = np.zeros(n)
    for prow in (father, mother):
        at = g3 & (prow >= 0)
        q = prow[at]
        q_lo, q_hi = own_bounds(q, mex_origin[q])
        half_lo[at] += 0.5 * q_lo
        half_hi[at] += 0.5 * q_hi
        away = g3 & (prow < 0)
        half_hi[away] += 0.5
    lo[g3], hi[g3] = half_lo[g3], half_hi[g3]
    both = g3 & (father >= 0) & (mother >= 0)
    n_parents = (father >= 0).astype(int) + (mother >= 0).astype(int)
    mxgp = np.zeros(n, int)
    for prow in (father, mother):
        at = prow >= 0
        mxgp[at] += mx(pem[prow[at]]).astype(int) + mx(pef[prow[at]]).astype(int)
    for m in range(5):
        cls[both & (mxgp == m)] = f"G3plus: both parents at home, {m} Mexico-born grandparent(s) of 4"
    cls[g3 & (n_parents == 1)] = "G3plus: one parent at home"
    cls[g3 & (n_parents == 0)] = "G3plus: no parent at home (unknown)"
    gate("G3plus: with both parents at home the low bound is a quarter per Mexico-born grandparent (exact)",
         np.array_equal(lo[both], mxgp[both] / 4.0))

    gp = list(csv.DictReader(GRANDPARENTS.open()))
    conv = sum(float(r["fractional_weight"]) * float(r["self_id_mexican"]) for r in gp) / sum(float(r["self_id_mexican"]) for r in gp)
    popj = json.loads(POP.read_text())
    gate("the convention's 0.6156 is population.json's identified third-generation mix (1e-12)",
         abs(conv - popj["fractional_ancestry"]["identified_third_generation"]) < 1e-12, f"{conv:.6f}")
    # Positive control of the linkage: the population lane's definition (cps_counts.py arm 3: any linked parent, any
    # age, linked parents' own birthplaces, two parents linked) on this frame reproduces arm3_grandparent_counts.csv.
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    linked = (rows_ >= 0).sum(axis=1)
    pb = np.where(rows_ >= 0, pen[np.where(rows_ >= 0, rows_, 0)], -1)
    gp_seen = np.zeros(n)
    for slot in (0, 1):
        r_ = rows_[:, slot]
        at = r_ >= 0
        gp_seen[at] += mx(pem[r_[at]]).astype(float) + mx(pef[r_[at]]).astype(float)
    any_mx = ((pb == F.MEXICO) & (rows_ >= 0)).any(axis=1)
    all_us = np.where(rows_ >= 0, np.isin(pb, F.US_AREAS), True).all(axis=1) & (linked > 0)
    third_pop = native & ~mx(pen) & (linked == 2) & ~any_mx & all_us & (gp_seen > 0)
    worst = 0.0
    for r in gp:
        m = third_pop & (gp_seen == int(r["mexican_grandparents_of_4"]))
        worst = max(worst, abs(w[m].sum() - float(r["children"])), abs(w[m & mex_origin].sum() - float(r["self_id_mexican"])))
    mix_pop = float(np.average(gp_seen[third_pop & mex_origin] / 4.0, weights=w[third_pop & mex_origin]))
    gate("positive control: the population lane's linkage on this frame reproduces arm3_grandparent_counts.csv's cells "
         "(0.1 person, the file's rounding) and its identified mix (1e-6)", worst <= 0.1 and abs(mix_pop - conv) < 1e-6,
         f"max |diff| {worst:.2f} persons; mix {mix_pop:.6f}")
    central = np.where(g3, conv, central)

    def wmean(x: np.ndarray, m: np.ndarray) -> float:
        return float(np.average(x[m], weights=w[m]))

    shares = {
        "G1": {"low": 1.0, "central": 1.0, "high": 1.0, "population": pops["G1"]},
        "G2": {"low": wmean(lo, g2), "central": wmean(central, g2), "high": wmean(hi, g2), "population": pops["G2"],
               "unknown_other_parent_central": 0.5 + 0.5 * s_other_seen,
               "co_resident_us_born_other_parent_share": s_other_seen},
        "G3plus": {"low": wmean(lo, g3), "central": conv, "high": wmean(hi, g3), "population": pops["G3plus"],
                   "central_rule": "the identified third-generation children's quarter-per-grandparent mix (population lane "
                                   "convention), applied to every identified third-plus member",
                   "seen_low": wmean(lo, both), "seen_high": wmean(hi, both),
                   "seen_rule": "members with both biological parents at home (grandparents seen): low counts only "
                                "Mexico-born grandparents (the strict quarter rule), high gives every US-born grandparent "
                                "of a Mexican-origin parent full Mexican-immigrant ancestry",
                   "seen_share_of_g3plus": float(w[both].sum() / w[g3].sum()),
                   "seen_with_no_mexico_born_grandparent": float(w[both & (mxgp == 0)].sum() / w[both].sum()),
                   "share_with_no_parent_at_home": float(w[g3 & (n_parents == 0)].sum() / w[g3].sum())},
        "added": {"low": popj["fractional_ancestry"]["hidden_third_generation"],
                  "central": popj["fractional_ancestry"]["hidden_third_generation"],
                  "high": popj["fractional_ancestry"]["hidden_third_generation"],
                  "rule": "the hidden third generation's quarter-per-grandparent mix (population.json); later losses take it too"},
    }
    gate("G2 shares lie between 1/2 and 1 and G3plus shares between 0 and 1, low <= central <= high",
         0.5 <= shares["G2"]["low"] <= shares["G2"]["central"] <= shares["G2"]["high"] <= 1.0
         and 0.0 <= shares["G3plus"]["low"] <= shares["G3plus"]["central"] <= shares["G3plus"]["high"] <= 1.0)

    class_rows = []
    for c in dict.fromkeys(cls[g2 | g3]):
        m = (cls == c) & (g2 | g3)
        adults = m & (age >= 25)
        class_rows.append({
            "class": c, "persons": f"{w[m].sum():.1f}", "share_of_generation": f"{w[m].sum() / w[g2 if c.startswith('G2') else g3].sum():.6f}",
            "share_low": f"{wmean(lo, m):.6f}", "share_high": f"{wmean(hi, m):.6f}", "share_central": f"{wmean(central, m):.6f}",
            "under_18": f"{w[m & (age < 18)].sum() / w[m].sum():.6f}",
            "ba_plus_adults_25plus": f"{w[adults & (hga >= 43)].sum() / w[adults].sum():.6f}" if w[adults].sum() > 0 else "",
            "records": int(m.sum()),
        })
    tot = sum(float(r["persons"]) for r in class_rows)
    gate("the classes cover G2 and G3plus exactly (1 person)", abs(tot - pops["G2"] - pops["G3plus"]) < 1.0, f"{tot:,.1f}")

    if not all(g["passed"] for g in GATES):
        raise SystemExit(f"[BLOCKED] {sum(not g['passed'] for g in GATES)} gate(s) failed; nothing written")
    result = {"meta": {"source": "main_case_lineage_2026_10_05/fractional.py",
                       "rule": "share of Mexican-immigrant ancestry: Mexico-born 1; each US-born person half of each parent's "
                               "share (lineage_cost_2026_09_19 per_capita, TFR/2); a parent born abroad elsewhere or a "
                               "US-born parent not of Mexican origin 0; unknown ancestors bounded by 0 and their full weight",
                       "weights": "pwwgt0 (US-born keep CPS weights under audit row 4)",
                       "costs": "not split here: lineage_case.cjs prices each generation's share at its average cost"},
              "shares": shares}
    (OUT / "fractional_shares.json").write_text(json.dumps(result, indent=1) + "\n")
    with (OUT / "fractional_classes.csv").open("w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(class_rows[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(class_rows)
    (OUT / "gates_fractional.json").write_text(json.dumps({"gates": GATES}, indent=1) + "\n")
    for g, s in shares.items():
        print(f"  {g}: low {s['low']:.4f} central {s['central']:.4f} high {s['high']:.4f}")
    for r in class_rows:
        print(f"  {r['class']:<66} {float(r['persons']) / 1e6:6.3f}M  {r['share_low']}-{r['share_high']} "
              f"(central {r['share_central']})  under-18 {r['under_18']}  BA+ {r['ba_plus_adults_25plus']}")


if __name__ == "__main__":
    main()
