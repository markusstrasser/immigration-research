"""Apply the pre-registered independent-price test (decisions/2026-10-24-land-independent-price-test.md).

Rule as revised before any price was seen (the decision's Revisions, points 3' and 4'). For each source s in
A_assessor, B_transactions, C_acquisitions: q_c = P_s,c / the lane's FHFA urban price for county c
(`derived/reference_top5.csv`). s passes if it prices Los Angeles plus at least two other counties, its charge-weighted
geometric mean q is in [0.80, 1.25], and Los Angeles's q is in [0.80, 1.25]. Land is identified if at least two sources
pass. Each covered source's repriced sum takes unpriced top-five counties at its own mean q. If identified, the central
is the median of the FHFA sum and the passing sources' sums, the range spans them. A source missing its prices.csv
counts as not passing. Also reports the revisit check: do the sources disagree with each other more than with FHFA?

    uv run --no-project python3 infra/immigration-fiscal/land_price_check_2026_10_24/test.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = ["A_assessor", "B_transactions", "C_acquisitions"]
Q_LO, Q_HI = 0.80, 1.25
LA = "06037"


def load_reference():
    ref = {r["county"]: r for r in csv.DictReader(open(HERE / "derived" / "reference_top5.csv"))}
    total = json.loads((HERE / "derived" / "reference_total.json").read_text())["total_bn"]
    return ref, total


def load_prices(src: str) -> dict[str, float] | None:
    p = HERE / src / "prices.csv"
    if not p.exists():
        return None
    out = {}
    for r in csv.DictReader(open(p)):
        c = r["county_fips"].strip().zfill(5)
        v = r["price_per_acre_2024"].strip()
        if v:
            out[c] = float(v)
    return out


def test_source(prices, ref, total):
    q = {c: prices[c] / float(ref[c]["fhfa_urban_p24_per_acre"]) for c in ref if c in prices}
    w = {c: float(ref[c]["charge_high_bn"]) for c in q}
    gmean = math.exp(sum(w[c] * math.log(q[c]) for c in q) / sum(w.values())) if q else None
    repriced, moved = [], []
    for i, end in enumerate(["low", "high"]):
        ch = {c: float(ref[c][f"charge_{end}_bn"]) for c in ref}
        s = total[i] - sum(ch.values()) + sum(ch[c] * q.get(c, gmean if gmean else 1.0) for c in ref)
        repriced.append(s)
        moved.append(s / total[i] - 1)
    others = sum(1 for c in q if c != LA)
    coverage = LA in q and others >= 2
    in_band = lambda v: v is not None and Q_LO <= v <= Q_HI
    passes = coverage and in_band(gmean) and in_band(q.get(LA))
    return dict(q=q, gmean_q=gmean, repriced_bn=repriced, moved=moved, coverage_ok=coverage, passes=passes)


def main() -> int:
    ref, total = load_reference()
    results, logq = {}, {}
    for s in SOURCES:
        prices = load_prices(s)
        if prices is None:
            results[s] = dict(missing=True, passes=False)
            continue
        results[s] = test_source(prices, ref, total)
        logq[s] = {c: math.log(v) for c, v in results[s]["q"].items()}
    n_pass = sum(r["passes"] for r in results.values())
    # Revisit check: mean |log q| (distance from FHFA) vs mean pairwise |log q_s - log q_t| on shared counties.
    to_fhfa = [abs(v) for d in logq.values() for v in d.values()]
    pair = [abs(logq[a][c] - logq[b][c]) for i, a in enumerate(logq) for b in list(logq)[i + 1:]
            for c in logq[a] if c in logq[b]]
    disagreement = dict(mean_abs_log_q_vs_fhfa=sum(to_fhfa) / len(to_fhfa) if to_fhfa else None,
                        mean_abs_log_q_between_sources=sum(pair) / len(pair) if pair else None, n_pairs=len(pair))
    d = disagreement
    disagreement["sources_disagree_more_than_with_fhfa"] = (
        None if d["mean_abs_log_q_between_sources"] is None
        else d["mean_abs_log_q_between_sources"] > d["mean_abs_log_q_vs_fhfa"])
    sums = [total] + [r["repriced_bn"] for r in results.values() if r.get("coverage_ok")]
    passing = [total] + [r["repriced_bn"] for r in results.values() if r.get("passes")]
    med = lambda xs: sorted(xs)[len(xs) // 2] if len(xs) % 2 else sum(sorted(xs)[len(xs) // 2 - 1:len(xs) // 2 + 1]) / 2
    estimate = dict(central_bn=[med([s[i] for s in passing]) for i in range(2)] if n_pass >= 2 else None,
                    range_bn=[[min(s[i] for s in sums), max(s[i] for s in sums)] for i in range(2)])
    out = dict(total_bn=total, q_band=[Q_LO, Q_HI], sources=results, n_pass=n_pass, identified=n_pass >= 2,
               estimate=estimate, disagreement=disagreement)
    (HERE / "derived" / "test_result.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for s, r in results.items():
        if r.get("missing"):
            print(f"  ✗ {s}: no prices.csv")
            continue
        qs = ", ".join(f"{c} {v:.2f}" for c, v in sorted(r["q"].items()))
        print(f"  {'✓' if r['passes'] else '✗'} {s}: q [{qs}] mean q {r['gmean_q']:.2f} sum {r['repriced_bn'][0]:.2f} / {r['repriced_bn'][1]:.2f}bn "
              f"moved {r['moved'][0]:+.1%} / {r['moved'][1]:+.1%} coverage {'ok' if r['coverage_ok'] else 'short'}")
    print(f"passed {n_pass}/3 → {'identified' if n_pass >= 2 else 'not identified'}; estimate {estimate}")
    print(f"disagreement {disagreement}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
