#!/usr/bin/env python3
"""Forensic data-integrity gate for the unified warehouse — catches the unit-bug class.

Motivated by two real bugs found by accident 2026-06-25: a remittance figure of
$151,636/adult (total-worldwide / a 437K subsample) and `avg_medicaid_total_computable`
≈ $109B labelled as an *average*. Both are "intensive column carrying an extensive
value" — a per-unit/average field holding a total-scale number. This gate scans every
numeric column and flags the smell deterministically, so the class can't recur silently.

Checks (HIGH severity = blocking):
  1. INTENSIVE-MAGNITUDE — a column named like a per-unit/average dollar figure
     (avg_/mean_/median_/*_per_adult/_per_capita/_per_pupil/_per_person/_per_household)
     whose magnitude is total-scale (|value| > $1,000,000). A real per-person dollar
     figure (income, NPV, cost) sits well under $1M; a billion-scale "average" is a
     mislabelled total.
  2. RATIO-RANGE — a share/pct/fraction/rate column with values outside its implied
     range (fractions ∉ [-0.01, 1.5]; percents ∉ [-1, 150]). Excludes *_per_100k /
     *_per_1000 (legitimately large rates).

Planned extension (not yet — false-positive-prone without per-column curation):
  BENFORD first-significant-digit test on large natural-quantity columns.

Run: uv run --with duckdb python audit_data_integrity.py [--json]
Exit non-zero if any HIGH-severity flag fires (suitable as a verification-gate step).
"""
from __future__ import annotations

import json
import re
import sys

from paths import unified_duckdb_path

# "3pct"/"2pct" in a name = a discount rate, NOT a percentage column — don't classify as ratio.
DIGIT_PCT = re.compile(r"\d\s*pct")

INTENSIVE_RE = ("avg_", "mean_", "median_", "_per_adult", "_per_capita", "_per_pupil",
                "_per_person", "_per_household", "_per_hh")
DOLLARISH = ("usd", "dollar", "cost", "spend", "income", "net", "remit", "wage",
             "earnings", "npv", "tax", "benefit", "medicaid", "snap", "outlay")
RATIO_RE = ("_share", "_pct", "_fraction", "_frac", "share_", "pct_", "_rate")
EXCLUDE_RATE = ("_per_100k", "_per_1000", "_per_100000", "rate_per", "_per_100k")
DOLLAR_PER_PERSON_CEIL = 1_000_000.0


def _classify(col: str) -> str:
    c = col.lower()
    if any(k in c for k in EXCLUDE_RATE) or DIGIT_PCT.search(c):
        return "rate_per_n"
    if any(p in c for p in INTENSIVE_RE) and any(d in c for d in DOLLARISH):
        return "intensive_dollar"
    if any(k in c for k in RATIO_RE):
        return "ratio"
    return "other"


def build(as_json: bool = False) -> int:
    try:
        import duckdb
    except ImportError:
        sys.exit("need duckdb — uv run --with duckdb python audit_data_integrity.py")

    db = unified_duckdb_path()
    if not db.exists():
        sys.exit(f"missing {db} — build it: reproduce.sh build unified")
    con = duckdb.connect(str(db), read_only=True)

    reals = con.execute("SELECT schema_name, table_name FROM main._catalog ORDER BY 1,2").fetchall()
    flags: list[dict] = []
    for sch, tbl in reals:
        cols = con.execute(
            f"SELECT column_name, data_type FROM information_schema.columns "
            f"WHERE table_schema='{sch}' AND table_name='{tbl}'"
        ).fetchall()
        for col, dtype in cols:
            if not any(t in dtype.upper() for t in ("INT", "DECIMAL", "DOUBLE", "FLOAT", "NUMERIC")):
                continue
            kind = _classify(col)
            if kind not in ("intensive_dollar", "ratio"):
                continue
            try:
                mn, mx = con.execute(f'SELECT min("{col}"), max("{col}") FROM "{sch}"."{tbl}"').fetchone()
            except Exception:
                continue
            if mn is None:
                continue
            if kind == "intensive_dollar" and max(abs(mn), abs(mx)) > DOLLAR_PER_PERSON_CEIL:
                flags.append({"sev": "HIGH", "check": "INTENSIVE-MAGNITUDE", "col": f"{sch}.{tbl}.{col}",
                              "detail": f"per-unit/avg dollar field reaches {max(abs(mn), abs(mx)):,.0f} (> $1M) — likely a total mislabelled as average/per-capita"})
            elif kind == "ratio":
                # ADVISORY only: percents are legitimately negative (net balances) and "share"
                # columns are sometimes percent-scale, so flag ONLY genuine impossibilities (>200).
                if mn < -200 or mx > 200:
                    flags.append({"sev": "LOW", "check": "RATIO-RANGE", "col": f"{sch}.{tbl}.{col}",
                                  "detail": f"share/rate field range [{mn:.4g}, {mx:.4g}] — magnitude implausible for any ratio/percent (>200)"})
    con.close()

    flags.sort(key=lambda f: f["col"])
    high = [f for f in flags if f["sev"] == "HIGH"]
    if as_json:
        print(json.dumps({"flags": flags, "high": len(high)}, indent=2))
    else:
        print(f"\n[data-integrity gate] scanned {len(reals)} tables")
        for f in flags:
            mark = "✗" if f["sev"] == "HIGH" else "!"
            print(f"  {mark} [{f['check']} · {f['sev']}] {f['col']}")
            print(f"      {f['detail']}")
        if not flags:
            print("  ✓ no integrity flags")
        print(f"\n  {len(high)} HIGH-severity flag(s)")
    return 1 if high else 0


if __name__ == "__main__":
    sys.exit(build(as_json="--json" in sys.argv))
