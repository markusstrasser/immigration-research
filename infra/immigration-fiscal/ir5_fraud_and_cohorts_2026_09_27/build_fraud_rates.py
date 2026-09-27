"""Copy the reader's fraud-rate rows into `derived/fraud_rates.csv` (source, year, population, rate, page, ...).

`reads/fraud_rates_raw.csv` is the researcher's record; every quote is checked against the
archived text in `sources/` by verify.py. Rows with no denominator are counts, not rates.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
COLS = ["source", "year", "population", "rate", "numerator", "denominator", "method", "page", "url", "quote"]

rows = list(csv.DictReader((HERE / "reads" / "fraud_rates_raw.csv").open()))
with (HERE / "derived" / "fraud_rates.csv").open("w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=COLS + ["kind"], lineterminator="\n")
    w.writeheader()
    for r in rows:
        kind = "rate" if r["denominator"] or r["rate"] else "count (no denominator)"
        w.writerow({**{c: r[c] for c in COLS}, "kind": kind})
print(f"✓ wrote fraud_rates.csv: {len(rows)} rows")
