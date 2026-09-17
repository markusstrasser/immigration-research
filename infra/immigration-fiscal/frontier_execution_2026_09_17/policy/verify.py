"""Independent Decimal/Fraction checks on the table-arithmetic output."""
import csv
import json
from decimal import Decimal
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent
rows = {r["spec"]: r for r in csv.DictReader((ROOT/"derived/published_table_arithmetic.csv").open())}
for r in rows.values():
    b, se = Decimal(r["estimate"]), Decimal(r["se"])
    for key, sign in [("normal95_low", -1), ("normal95_high", 1)]:
        assert abs(Decimal(r[key]) - (b + sign*Decimal("1.96")*se)) < Decimal("1e-12")
checks = json.loads((ROOT/"derived/checks.json").read_text())
for row in checks["ratio_checks"]:
    exact = Fraction(str(row["reduced"]))/Fraction(str(row["first_stage"]))
    assert abs(float(exact)-row["recomputed_ratio"]) < 1e-12
assert Decimal(rows["revenue_reduced_form_win"]["normal95_low"]) > 0
assert Decimal(rows["us_hires_iv_win"]["normal95_low"]) < 0
assert Decimal(rows["us_hires_iv_share"]["normal95_low"]) < 0
assert checks["status"].startswith("PARTIAL")
print("PASS: 12 interval calculations, four reduced-form/first-stage ratios, scope and sign guards")
