"""Gate: the pooled files reproduce ladder 170's single-year rates (civic_service_by_ancestry_2026_09_21,
ACS 2024 via the Census tabulate API, US-born men 18-49 by first ancestry): Mexican (ANC1P 210)
5.7% and Asian Indian (615) 1.05% ever on active duty. Also shows each year separately and the
lane's wider Mexican ancestry set. Writes `derived/reconcile_ladder170.txt`.
"""
import sys
from pathlib import Path

import duckdb

HERE = Path(__file__).resolve().parent
PUBLISHED_170 = {"ANC1P = 210": 0.057, "ANC1P = 615": 0.0105}
ROWS = {"Mexican, ANC1P 210 (ladder 170's code)": "ANC1P = 210",
        "Mexican, the lane's 7 ancestry codes": "ANC1P IN (210, 211, 212, 213, 215, 218, 219)",
        "Asian Indian, ANC1P 615": "ANC1P = 615"}


def main():
    con = duckdb.connect()
    lines = ["US-born men 18-49, share ever on active duty (MIL 1-2), person weights"]
    failed = False
    for year in (2022, 2023, 2024):
        for label, predicate in ROWS.items():
            n, rate = con.execute(f"""
                SELECT COUNT(*), SUM(CASE WHEN MIL IN (1, 2) THEN PWGTP ELSE 0 END)::DOUBLE / SUM(PWGTP)
                FROM read_parquet('{HERE / '_cache' / f'acs{year}_persons.parquet'}')
                WHERE NATIVITY = 1 AND SEX = 1 AND AGEP BETWEEN 18 AND 49 AND {predicate}""").fetchone()
            note = ""
            if year == 2024 and predicate in PUBLISHED_170:
                target = PUBLISHED_170[predicate]
                ok = abs(rate - target) < 0.0006  # ladder 170 prints 5.7% and 1.05%
                failed |= not ok
                note = f"  ladder 170 {100 * target:.2f}%  {'PASS' if ok else 'FAIL'}"
            lines.append(f"  {year}  {label:40s} records {n:>7,}  {100 * rate:5.2f}%{note}")
    text = "\n".join(lines) + ("\nFAIL\n" if failed else "\nPASS\n")
    (HERE / "derived" / "reconcile_ladder170.txt").write_text(text)
    print(text)
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
