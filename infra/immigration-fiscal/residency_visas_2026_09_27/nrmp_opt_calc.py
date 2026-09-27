"""Displacement arithmetic from NRMP 2025 Table 4A/4B/5/2 and a rough OPT FICA range.

NRMP inputs are quoted in reads/q4_nrmp_crowdout.md; SEVIS counts in reads/q6_opt.md.
OPT wage, time-in-status and exempt share are ASSUMPTIONS, labelled below.
Writes derived/nrmp_opt_calc.txt and prints the same lines.
"""
from pathlib import Path

lines = []
active = {"MD Sr": 20368, "DO Sr": 8392, "MD Grad": 1751, "DO Grad": 630, "US IMG": 4587, "Non-US IMG": 11465}
placed_active = {"MD Sr": 19922, "DO Sr": 8259, "MD Grad": 934, "DO Grad": 343, "US IMG": 3370, "Non-US IMG": 6915}
unplaced = {k: active[k] - placed_active[k] for k in active}
for k, v in unplaced.items():
    lines.append(f"unplaced after SOAP 2025  {k:11s} {v:>6,}")
us = sum(v for k, v in unplaced.items() if k != "Non-US IMG")
lines.append(f"unplaced US-school or US-citizen applicants  {us:,}")
lines.append(f"PGY-1 positions minus all active US MD+DO seniors  {40041 - 20368 - 8392:,}  ({(40041-20368-8392)/40041:.1%} of 40,041)")
im = {2025: (10584, 1145, 3573), 2024: (9767, 1089, 3109)}
for y, (filled, usimg, nonus) in im.items():
    lines.append(f"IM categorical {y}: IMG share of filled {(usimg+nonus)/filled:.1%}; non-US IMG {nonus/filled:.1%}; US IMG {usimg/filled:.1%}")
lines.append(f"seniors ranking only IM, unmatched: MD {67/3772:.1%}, DO {41/1649:.1%}")
nonus_placed = placed_active["Non-US IMG"]
lines.append(f"non-US IMG PGY-1 placements still needed if every unplaced American replaced one  "
             f"{nonus_placed - us:,} of {nonus_placed:,}")

# OPT FICA forgone, 2024 (rough). SEVIS stock of records authorized in 2024: OPT 340,066; STEM OPT 165,524.
RATE = 0.153  # employer 7.65% + employee 7.65%
cases = {  # (OPT year-fraction worked in CY, STEM year-fraction, exempt share, mean wage) -- ASSUMPTIONS
    "low":     (0.40, 0.70, 0.80, 60000),
    "central": (0.50, 0.80, 0.85, 75000),
    "high":    (0.60, 0.90, 0.90, 90000),
}
for name, (fo, fs, ex, w) in cases.items():
    py = 340066 * fo + 165524 * fs
    total = py * ex * w * RATE
    lines.append(f"OPT FICA forgone {name:7s}: person-years {py:,.0f}; total ${total/1e9:.2f}bn; employer ${total/2e9:.2f}bn; employee ${total/2e9:.2f}bn")

out = Path(__file__).resolve().parent / "derived" / "nrmp_opt_calc.txt"
out.parent.mkdir(exist_ok=True)
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("\n".join(lines))
