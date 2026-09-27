"""Per-resident FICA saving for a J-1 physician resident (RGH IM 2025-26 pay scale).

Inputs are quoted in reads/q1_rochester.md (pay) and reads/q2_q3_pay_gme_tax.md (rules).
J-1 physicians are "teachers or trainees" (IRC 7701(b)(5)(C)); exempt individual for 2 calendar
years (2-of-6 rule), so a July start is FICA-exempt July(Y1)-December(Y2) = 18 months, assuming
no prior F/J/Q exempt years. Residency pay runs July-June at one annual rate per PGY year.
Writes derived/fica_calc.txt and prints the same lines.
"""
from pathlib import Path

OASDI, HI = 0.062, 0.0145          # each side; resident pay is far below the OASDI wage base
RATE = OASDI + HI                   # 7.65% employer, 7.65% employee
FUTA_MAX = 0.006 * 7000             # $42 per employee after full state credit
pay = {"PGY1": 73000, "PGY2": 76000, "PGY3": 80000}

exempt_wages = pay["PGY1"] + pay["PGY2"] / 2          # Jul Y1-Jun Y2, then Jul-Dec Y2
total_wages = sum(pay.values())
side = exempt_wages * RATE
rows = [
    ("exempt wages over 3-yr residency", exempt_wages),
    ("share of residency wages exempt", exempt_wages / total_wages),
    ("employer FICA saved, whole residency", side),
    ("employee FICA saved, whole residency", side),
    ("combined, whole residency", 2 * side),
    ("employer FICA saved, per resident-year (3-yr avg)", side / 3),
    ("employer FICA saved in an exempt PGY-1 year", pay["PGY1"] * RATE),
    ("employer FUTA saved, max per exempt year", FUTA_MAX),
    ("employer saving as % of PGY-1 salary", RATE),
]
lines = [f"{k:52s} {v:>12,.2f}" if v > 1 else f"{k:52s} {v:>12.4f}" for k, v in rows]
out = Path(__file__).resolve().parent / "derived" / "fica_calc.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
