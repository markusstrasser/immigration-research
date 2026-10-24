"""Apply the pre-registered independent-price test (decisions/2026-10-24-land-independent-price-test.md).

For each source s in A_assessor, B_transactions, C_acquisitions: q_c = P_s,c / the lane's FHFA urban price for county
c (`derived/reference_top5.csv`), q_c = 1 where s has no price. Repriced sum = total - sum(charge_c) +
sum(charge_c * q_c), at each end. s passes if the sum moves <= 25% at both ends and s prices Los Angeles plus at least
two other counties. Land is identified if at least two sources pass. A source missing its prices.csv counts as not
passing. Also reports the decision's revisit check: do the sources disagree with each other more than with FHFA?

    uv run --no-project python3 infra/immigration-fiscal/land_price_check_2026_10_24/test.py
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = ["A_assessor", "B_transactions", "C_acquisitions"]
THRESHOLD = 0.25
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
    repriced, moved = [], []
    for i, end in enumerate(["low", "high"]):
        ch = {c: float(ref[c][f"charge_{end}_bn"]) for c in ref}
        s = total[i] - sum(ch.values()) + sum(ch[c] * q.get(c, 1.0) for c in ref)
        repriced.append(s)
        moved.append(s / total[i] - 1)
    others = sum(1 for c in q if c != LA)
    coverage = LA in q and others >= 2
    passes = coverage and all(abs(m) <= THRESHOLD for m in moved)
    return dict(q=q, repriced_bn=repriced, moved=moved, coverage_ok=coverage, passes=passes)


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
    out = dict(total_bn=total, threshold=THRESHOLD, sources=results, n_pass=n_pass, identified=n_pass >= 2,
               disagreement=disagreement)
    (HERE / "derived" / "test_result.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    for s, r in results.items():
        if r.get("missing"):
            print(f"  ✗ {s}: no prices.csv")
            continue
        qs = ", ".join(f"{c} {v:.2f}" for c, v in sorted(r["q"].items()))
        print(f"  {'✓' if r['passes'] else '✗'} {s}: q [{qs}] sum {r['repriced_bn'][0]:.2f} / {r['repriced_bn'][1]:.2f}bn "
              f"moved {r['moved'][0]:+.1%} / {r['moved'][1]:+.1%} coverage {'ok' if r['coverage_ok'] else 'short'}")
    print(f"passed {n_pass}/3 → {'identified' if n_pass >= 2 else 'not identified'}; disagreement {disagreement}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
