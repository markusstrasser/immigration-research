"""Restate the September 27 fiscal-plus-social pairing with every row on the adopted account's own count.

The published pairing, $416.19-490.74bn, adds a fiscal case priced on audit row 4's union (39,712,493 people) to
social rows built on the published CPS union (40,896,574), and divides the sum by 40,896,574. Here each row takes
its factor from basis.csv (the row-4 value over the published one) and the sum is divided by 39,712,493. The record's
other per-member figures are then restated: the pairings, the comparators, the white replacement, the generation
table and the lines the decomposition lane left to other lanes' counts.

Inputs: sept27_propagation_2026_09_27/derived/real_costs_totals.csv (the pairing's ends, the fiscal rows and the
added social items), its companion real_costs_totals.json from the same run (the section 7 channels, which the
CSV prints only inside its sums: victims, property crime, unreimbursed care, housing, congestion by band end),
basis.csv, derived/frame_counts.csv, derived/reeval.csv, derived/white_count.csv,
main_case_decomposition_2026_09_29/derived/headcount.csv (the per-member factors by generation),
black_comparator_rough_2026_09_28/derived/rekey_summary.csv, crime_victim_cost_2026_09_23/derived/arms.csv and
disease_food_2026_09_28/derived/totals.csv.

Gates (exit 1, nothing written): the rows add up to the published pairing at both ends (2e-6bn); the published
per-member figures reproduce the CSV's; every factor is positive; each 5+ record starts from the pairing's value
for its row (1e-6bn, or half a unit of the 2 dp an items.csv value is printed at); each restated record figure's
published value,
computed here, rounds to the figure the record prints. Record lines are found by their text, not a stored line
number, in each document as committed at PIN (the commit before the living documents took the restated figures),
so a rerun after they did is identical; a text not found exactly once there is written as [DEGRADED] and reported,
not skipped.

Writes derived/restated_pairing.csv (section, item, end, published, factor, restated, move, unit, note):
  row           each row's signed contribution to its end of the pairing, $bn
  pairing       the two ends, $bn
  per_member    $k: the published pairing on 40.90M (the record), on 39.71M (denominator only), and the restated
                pairing on 39.71M
  row_5plus, pairing_5plus, per_member_5plus
                a second restatement, row 4 plus the 5+ basis for the two traffic rows (reeval.csv's _5plus
                records: the NHTS per-person ratios on persons aged 5+); every other row as in the first
  reader        per-member and comparator figures in the INDEX, the FAQ, the evidence map's groups.py, the ladder,
                the generation memo and the real-costs memo: file:line, published and restated values
Run from the repository root after basis.py and white_count.py:
  uv run --no-project --offline python3 infra/immigration-fiscal/population_basis_2026_09_29/restate.py
"""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parent.parent
TOTALS = FISCAL / "sept27_propagation_2026_09_27" / "derived" / "real_costs_totals"
OUT = HERE / "derived" / "restated_pairing.csv"
FIELDS = ["section", "item", "end", "published", "factor", "restated", "move", "unit", "note"]
FAILS: list[str] = []
DEGRADED: list[str] = []
INDEX = "research/immigration-INDEX.md"
LADDER = "research/immigration-confidence-ladder.md"
MAP = "infra/immigration-fiscal/overview_2026_09_28/groups.py"
GEN = "research/immigration-adopted-account-by-generation-2026-09-25.md"
# The documents the reader rows restate, as committed before they took the restated figures (2026-09-29).
PIN = "b170585"
# Superseded pairings the INDEX printed with a per-member figure on 40.90M until its 2026-09-29 rewrite, at their
# printed totals, $bn: the text that found the line, the pairing, and the printed per-member range. Their social rows
# are not restated here.
SUPERSEDED = [("$10.9–12.8k per member", "ladder 265, 2026-09-28 final: $447-522bn", 447.0, 522.0, "10.9-12.8"),
              ("$11.3–13.1k per member", "ladder 264, 2026-09-28 later: $463-537bn", 463.0, 537.0, "11.3-13.1"),
              ("$9.1–10.9k per", "2026-09-28 later, fear/security/schools: $371-446bn", 371.0, 446.0, "9.1-10.9"),
              ("$8.9–10.7k per member", "2026-09-28, September 27 case: $363-438bn", 363.0, 438.0, "8.9-10.7")]
# The generation memo's tables (September 24 case): the row, its factor's key and the printed low / high dollars,
# which also find the line.
GEN_ROWS = [("(b) G1 per adult", "adults", 9441, 11543), ("(b) G2 per adult", None, 5629, 5941),
            ("(b) G3+ per adult", None, 4945, 7160), ("(a) G1 per member", ("generation a", "G1"), 5220, 4383),
            ("(a) G2 per member", ("generation a", "G2"), 5703, 6636),
            ("(a) G3+ per member", ("generation a", "G3plus"), 3859, 6808),
            ("(a) all three per member", ("all", "union"), 4912, 6023)]


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def read_csv(path):
    with path.open() as handle:
        return list(csv.DictReader(handle))


def locate(path, text):
    """path@PIN:line of the one line holding text at PIN, or a [DEGRADED] marker (recorded and printed)."""
    lines = subprocess.run(["git", "-C", str(ROOT), "show", f"{PIN}:{path}"], check=True, capture_output=True,
                           text=True).stdout.splitlines()
    hits = [i + 1 for i, t in enumerate(lines) if text in t]
    if len(hits) == 1:
        return f"{path}@{PIN}:{hits[0]}"
    DEGRADED.append(f"{path}@{PIN}: {text!r} found {len(hits)} times")
    return f"{path}@{PIN}:[DEGRADED: text found {len(hits)} times]"


def main():
    table = {(r["column"], r["item"]): r for r in read_csv(TOTALS.with_suffix(".csv"))}
    doc = json.loads(TOTALS.with_suffix(".json").read_text())
    basis = read_csv(HERE / "basis.csv")
    counts = {r["count"]: r for r in read_csv(HERE / "derived" / "frame_counts.csv")}
    n_record = doc["target_population_m"] * 1e6
    n_account = float(counts["union|all"]["row4"])

    def value(ref):
        kind, key = ref.split(":", 1)
        if kind == "csv":
            return float(table[tuple(key.split("|", 1))]["sept27"])
        node = doc
        for part in key.split("."):
            node = node[part]
        return float(node)

    rows, ends = [], {"low": [0.0, 0.0], "high": [0.0, 0.0]}
    for b in basis:
        v, f = int(b["sign"]) * value(b["value_ref"]), float(b["factor"])
        gate(f"factor positive: {b['row']} {b['end']}", f > 0)
        for end in (("low", "high") if b["end"] == "both" else (b["end"],)):
            ends[end][0] += v
            ends[end][1] += v * f
        rows.append(dict(section="row", item=b["row"], end=b["end"], published=v, factor=f, restated=v * f,
                         move=v * (f - 1), unit="bn", note=b["factor_method"]))
    published = {"low": value("csv:hispanic_mixed_group|total at central values (low)"),
                 "high": value("csv:custody|total at central values (high)")}
    for end in ("low", "high"):
        gate(f"rows add up to the published pairing, {end} end", abs(ends[end][0] - published[end]) < 2e-6,
             f"{ends[end][0]:.6f} vs {published[end]:.6f}")
    per = {"low": value("csv:hispanic_mixed_group|per group member (low)"), "high": value("csv:custody|per group member (high)")}
    # Since 2026-09-29 the CSV's per-member rows divide by the count the case prices (real_costs_totals.py); the record
    # printed the published pairing divided by n_record.
    n_csv = doc["per_member_population_m"]["sept27"] * 1e6
    gate("the CSV's per-member divisor is the account's row-4 count", abs(n_csv - n_account) < 1, f"{n_csv:,.1f}")
    for end in ("low", "high"):
        gate(f"published per member reproduces the CSV, {end} end", abs(published[end] / n_csv * 1e6 - per[end]) < 1e-6,
             f"${per[end]:.6f}k")
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)

    for end in ("low", "high"):
        p, r = published[end], ends[end][1]
        rows.append(dict(section="pairing", item="fiscal plus social, central values", end=end, published=p,
                         factor=r / p, restated=r, move=r - p, unit="bn",
                         note="low: Hispanic footing, decision 4's mixed-group victims; high: custody footing"))
    for end in ("low", "high"):
        p, r = published[end], ends[end][1]
        base = p / n_record * 1e6
        for item, v, note in (
                ("published pairing / 40.90M (the record)", base, f"divides by {n_record:,.1f}"),
                ("published pairing / 39.71M (denominator only)", p / n_account * 1e6, f"divides by {n_account:,.1f}"),
                ("restated pairing / 39.71M (every row on 39.71M)", r / n_account * 1e6,
                 "the answer: every row on the row-4 count and divided by it")):
            rows.append(dict(section="per_member", item=item, end=end, published=base, factor=v / base, restated=v,
                             move=v - base, unit="$k", note=note))

    # Second restatement: row 4 plus the 5+ basis for the traffic rows (reeval.csv's _5plus records).
    re5 = {r["row"]: r for r in read_csv(HERE / "derived" / "reeval.csv")}
    five = {("congestion", "low"): "congestion_low_end_5plus", ("congestion", "high"): "congestion_high_end_5plus",
            ("road_crash_externality", "both"): "road_crash_externality_5plus"}
    ends5 = {"low": 0.0, "high": 0.0}
    for b in basis:
        v, f5 = int(b["sign"]) * value(b["value_ref"]), float(b["factor"])
        name = five.get((b["row"], b["end"]))
        if name:
            r5 = re5[name]
            # social items reach real_costs_totals.csv at the 2 dp their lane's items.csv prints
            tol = 0.005 if b["value_ref"].startswith("csv:social_item") else 1e-6
            gate(f"the 5+ arm starts from the pairing's value: {name}", abs(float(r5["published_bn"]) - v) <= tol,
                 f"{float(r5['published_bn']):.6f} vs {v:.6f} (tolerance {tol})")
            f5 = float(r5["row4_bn"]) / float(r5["published_bn"])
            rows.append(dict(section="row_5plus", item=b["row"], end=b["end"], published=v, factor=f5, restated=v * f5,
                             move=v * (f5 - 1), unit="bn", note=f"row 4 alone x{float(b['factor']):.6f}; {r5['method']}"))
        for end in (("low", "high") if b["end"] == "both" else (b["end"],)):
            ends5[end] += v * f5
    for end in ("low", "high"):
        p, r, r5 = published[end], ends[end][1], ends5[end]
        rows.append(dict(section="pairing_5plus", item="fiscal plus social, central values, row 4 plus the 5+ basis",
                         end=end, published=p, factor=r5 / p, restated=r5, move=r5 - p, unit="bn",
                         note=f"row 4 alone {r:.6f}; the 5+ basis moves it {r5 - r:+.6f}"))
    for end in ("low", "high"):
        p, r, r5 = published[end], ends[end][1], ends5[end]
        base = p / n_record * 1e6
        rows.append(dict(section="per_member_5plus", item="restated pairing / 39.71M, row 4 plus the 5+ basis", end=end,
                         published=base, factor=(r5 / n_account * 1e6) / base, restated=r5 / n_account * 1e6,
                         move=r5 / n_account * 1e6 - base, unit="$k",
                         note=f"row 4 alone ${r / n_account * 1e6:.6f}k; divides by {n_account:,.1f}"))
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)

    def reader(where, item, published_v, restated_v, unit, note, factor=None, check=None):
        """check: (printed text, the published value rendered as the record renders it): a positive control."""
        if check is not None:
            gate(f"published value renders as the record prints it: {item}", check[0] == check[1],
                 f"{check[1]!r} vs printed {check[0]!r}")
        move = None if published_v is None or restated_v is None else restated_v - published_v
        rows.append(dict(section="reader", item=f"{where} {item}", end="both", published=published_v, factor=factor,
                         restated=restated_v, move=move, unit=unit, note=note))

    # Pairings (the INDEX, a living document).
    lo_r, hi_r = (ends[e][1] / n_account * 1e6 for e in ("low", "high"))
    lo_p, hi_p = (published[e] / n_record * 1e6 for e in ("low", "high"))
    reader(locate(INDEX, "$10.2–12.0k per member"), "latest pairing (ladder 266), $10.2-12.0k per member", lo_p, lo_r,
           "$k", f"restated ${lo_r:.1f}-{hi_r:.1f}k (every row on 39.71M); high end ${hi_p:.3f}k -> ${hi_r:.3f}k",
           check=("10.2-12.0", f"{lo_p:.1f}-{hi_p:.1f}"))
    # The INDEX printed these until its 2026-09-29 rewrite, which left superseded pairings to the ladder and git.
    for text, label, lo, hi, printed in SUPERSEDED:
        reader(f"{INDEX} (until 2026-09-29, {text!r})", f"superseded, {label}, ${printed}k per member", lo / n_record * 1e6,
               lo / n_account * 1e6, "$k",
               f"denominator only: ${lo / n_account * 1e6:.1f}-{hi / n_account * 1e6:.1f}k; social rows not restated",
               factor=n_record / n_account, check=(printed, f"{lo / n_record * 1e6:.1f}-{hi / n_record * 1e6:.1f}"))

    # The Black comparator: the case per member on 39.71M; the Black figure divides by its own count.
    rekey = {(r["group"], r["end"]): r for r in read_csv(FISCAL / "black_comparator_rough_2026_09_28" / "derived" / "rekey_summary.csv")}
    ratios = {}
    for end in ("low", "high"):
        black = float(rekey[("nh_black_rough", end)]["cost"]) / float(rekey[("nh_black_rough", end)]["population"])
        mex = float(rekey[("mexican_origin_engine", end)]["cost"])
        ratios[end] = (black / (mex / n_record), black / (mex / n_account))
    b_lo_p, b_hi_p = min(r[0] for r in ratios.values()), max(r[0] for r in ratios.values())
    b_lo_r, b_hi_r = min(r[1] for r in ratios.values()), max(r[1] for r in ratios.values())
    for where in (locate(INDEX, "1.5–1.7× the Mexican-origin"), locate(MAP, "1.5–1.7 times as much per member")):
        reader(where, "Black comparator, 1.5-1.7x the union per member (ladder 259)", b_lo_p, b_lo_r, "ratio",
               f"published {b_lo_p:.3f}-{b_hi_p:.3f}x; with the case per member on 39.71M {b_lo_r:.3f}-{b_hi_r:.3f}x, "
               f"printed {b_lo_r:.1f}-{b_hi_r:.1f}x (the Black figure divides by its own 41.95M count)",
               check=("1.5-1.7", f"{b_lo_p:.1f}-{b_hi_p:.1f}"))

    # The white replacement (ladder 263) with both sides on 39.71M: white_count.py.
    wc = {(r["figure"], r["end"]): r for r in read_csv(HERE / "derived" / "white_count.csv")}

    def span(figures, col):
        v = [float(wc[(f, e)][col]) for f in figures for e in ("low", "high")]
        return min(v), max(v)

    us = ("delta: A1, accrual (payable)", "delta: A3, cash, union ages")
    raw = ("delta: A1, cash, white ages",)
    local = ("delta: local whites, sum of CA, TX and rest",)
    for text, label, figs in (("$315–330bn", "the union against 40.9M third-plus whites, accrual or union ages", us),
                              ("$155–157bn", "the same on raw cash at white ages", raw),
                              ("$406–412bn", "against local whites state by state", local)):
        (a, b), (c, d_) = span(figs, "published_bn"), span(figs, "row4_bn")
        reader(locate(INDEX, text), f"{label}, {text}", a, c, "bn",
               f"${c:.0f}-{d_:.0f}bn with the union on row-4 weights and the whites at 39.71M (published ${a:.1f}-{b:.1f}, "
               f"restated ${c:.1f}-{d_:.1f}bn)", check=(text.strip("$bn").replace("–", "-"), f"{a:.0f}-{b:.0f}"))
    ca = [float(wc[("delta: local whites, California", e)][c]) for e in ("low", "high")
          for c in ("published_per_member", "row4_per_member")]
    reader(locate(INDEX, "California $14.1k per member"), "California per member against local whites (ladder 263)",
           ca[0] / 1e3, ca[1] / 1e3, "$k", f"${ca[0]:,.0f} -> ${ca[1]:,.0f} (high end ${ca[2]:,.0f} -> ${ca[3]:,.0f}): "
           "row 4 leaves California's people but moves the frame totals and the union's engine-share lines",
           check=("14.1", f"{ca[0] / 1e3:.1f}"))
    (a, b), (c, d_) = span(us, "published_bn"), span(us, "row4_bn")
    (e, f), (g, h) = span(local, "published_bn"), span(local, "row4_bn")
    (i, j), (k, m) = span(raw, "published_bn"), span(raw, "row4_bn")
    reader(locate(MAP, "about $320–410bn a year more"), "comparators claim, about $320-410bn against as many whites",
           a, c, "bn", f"about ${(c + d_) / 2:.0f}-{(g + h) / 2:.0f}bn (midpoints; published {(a + b) / 2:.0f}-{(e + f) / 2:.0f})")
    reader(locate(MAP, "$320bn (315–330) against US whites"), "comparators range", a, c, "bn",
           f"${(c + d_) / 2:.0f}bn ({c:.0f}-{d_:.0f}) against US whites, ${(g + h) / 2:.0f}bn ({g:.0f}-{h:.0f}) against "
           "local whites")
    reader(locate(MAP, "Against 40.9M whites"), "finding text, 40.9M whites, $320bn (315-330), $409bn (406-412)", a, c,
           "bn", f"against {n_account / 1e6:.1f}M whites: about ${(c + d_) / 2:.0f}bn ({c:.0f}-{d_:.0f}); local whites about "
           f"${(g + h) / 2:.0f}bn ({g:.0f}-{h:.0f})")
    reader(locate(MAP, "only $156bn"), "finding why, raw cash only $156bn", (i + j) / 2, (k + m) / 2, "bn",
           f"${(k + m) / 2:.0f}bn ({k:.1f}-{m:.1f})", check=("156", f"{(i + j) / 2:.0f}"))
    for text, name in (("($10,081 per member)", "sum of CA, TX and rest"), ("($14,133 per member", "California"),
                       ("($8,567)", "Texas"), ("($7,963)", "rest of US"), ("($18,816", "Los Angeles metro")):
        r = wc[(f"delta: local whites, {name}", "low")]
        pp, rp = float(r["published_per_member"]), float(r["row4_per_member"])
        reader(locate(LADDER, text), f"ladder 263 record, {name} per member against local whites", pp, rp, "$",
               f"${pp:,.0f} -> ${rp:,.0f} at the low end; a record: append a note", check=(text.strip("($)").split(" ")[0],
                                                                                           f"{pp:,.0f}"))

    # The decomposition's lines that depend on other lanes' counts (main_case_decomposition RESULT.md, "How many record
    # figures it touches"), each on its lane's own count.
    re_ = {r["row"]: r for r in read_csv(HERE / "derived" / "reeval.csv")}
    f_s = next(float(b["factor"]) for b in basis if b["row"] == "victims")
    victims = float(next(r for r in read_csv(FISCAL / "crime_victim_cost_2026_09_23" / "derived" / "arms.csv")
                         if r["arm"] == "central")["full_bn"])
    disease = float(next(r for r in read_csv(FISCAL / "disease_food_2026_09_28" / "derived" / "totals.csv")
                         if r["total"] == "disease_plus_food_safety" and r["measure"] == "absolute")["central_bn"])
    for where, label, pub_bn, r4_bn, printed, note in (
            (locate("research/immigration-real-fiscal-and-social-costs-2026-09-23.md", "$707 per group member"),
             "victims' harm, central, $707 per group member", victims, victims * f_s, "707",
             "the victim lane's central on s (linear), x0.985635"),
            (locate(LADDER, "$341 per member"), "scale net, $341 per member (ladder 201)",
             -float(re_["scale_net_earnings"]["published_bn"]), -float(re_["scale_net_earnings"]["row4_bn"]), "341",
             "the scale lane re-evaluated on the row-4 count (reeval.csv)"),
            (locate(LADDER, "$1,704 per member"), "PM2.5, $1,704 per member (ladder 260)",
             float(re_["pm25_consumption"]["published_bn"]), float(re_["pm25_consumption"]["row4_bn"]), "1,704",
             "the air lane re-evaluated on the row-4 count (reeval.csv)"),
            (locate(LADDER, "$7 per member"), "disease and food safety, $7 per member (ladder 261)", disease, disease,
             "7", "not headcount-based (CDC case counts, ACS kitchen shares; the US-born case share uses G2 and G3+, "
                  "which row 4 leaves): only the denominator moves")):
        pp, rp = pub_bn * 1e9 / n_record, r4_bn * 1e9 / n_account
        reader(where, label, pp, rp, "$", f"${pp:,.2f} -> ${rp:,.2f}; {note}", check=(printed, f"{pp:,.0f}"))
    reader(locate(LADDER, "−$1,446 / +$1,093"), "within-household per-member figures (ladder 268)", None, None, "$",
           "not restated: within_group_distribution_2026_09_29 spreads the row-4 totals over the published weights "
           "(households.py:116-118, RESULT.md:115 '40.90'); every amount of a Mexico-born member outside CA and TX "
           "runs low and the union mean per member 2.9% low; the shares and medians need the lane rerun on row-4 "
           "weights, with its key-total gates re-pinned")

    # The generation table (September 24 case): the decomposition's per-member factors (headcount.csv).
    hc = {(r["cut"], r["group"]): float(r["per_member_factor"]) for r in
          read_csv(FISCAL / "main_case_decomposition_2026_09_29" / "derived" / "headcount.csv")}
    adults = float(counts["mexico_born|18_plus"]["published"]) / float(counts["mexico_born|18_plus"]["row4"])
    for label, key, lo, hi in GEN_ROWS:
        f = adults if key == "adults" else hc[key] if key else 1.0
        reader(locate(GEN, f"{lo:,} / {hi:,}"), f"generation table, {label}", float(lo), lo * f, "$",
               f"${lo:,} / {hi:,} -> ${lo * f:,.0f} / {hi * f:,.0f} (x{f:.6f}"
               + ("; adults are Mexico-born adults, row 4 removes 1.108M of them)" if key == "adults" else ")"), factor=f)

    reader(locate(INDEX, "10–20% less per member"), "10-20% less per member in a typical budget year", None, None, "%",
           "unchanged: a ratio of per-member figures across years; its dollar totals are at today's size", factor=1.0)
    reader(locate("research/immigration-objections-faq-2026-09-21.md", "per member with its lower relative income"),
           "10% / 20% less per member in a typical budget year", None, None, "%", "unchanged, as the INDEX line", factor=1.0)
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)

    OUT.parent.mkdir(exist_ok=True)
    fmt = lambda v: "" if v is None else (f"{v:.6f}" if isinstance(v, float) else v)  # noqa: E731
    with OUT.open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=FIELDS, lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({k: fmt(r[k]) for k in FIELDS})
    for r in rows:
        if r["section"] == "reader":
            print(f"  reader  {r['item'][:96]:96s} {r['note'][:110]}")
        else:
            print(f"  {r['section']:10s} {r['item'][:48]:48s} {r['end']:5s} {fmt(r['published']):>12s} x{r['factor']:.6f} "
                  f"-> {fmt(r['restated']):>12s} ({r['move']:+.6f}) {r['unit']}")
    for d in DEGRADED:
        print(f"  [DEGRADED] {d}")
    print(f"  wrote {len(rows)} rows -> {OUT.relative_to(FISCAL)}")


if __name__ == "__main__":
    main()
