"""Gates for the civic trajectory lane. Exit 1 on any failure.

1. The Sept-supplement volunteering rates for Mexican G1/G2/G3+ recomputed from
   service_by_ses_2026_09_23/derived/cps_civic_rates.csv equal that lane's RESULT.md section 4
   (10.9 / 15.1 / 19.7%).
2. CPS November turnout for all citizens 18+ within 1 point of Census P20 Table 1, each year.
3. Spouse linkage: share of married persons 25-54 with a found spouse record >= 99%.
4. Output schema: the four required CSVs carry source, measure, generation, n, estimate, se,
   adjustment.
5. civic_carryover.csv is reproduced exactly by rerunning carryover.py's assembly in memory.
"""
import io
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import carryover  # noqa: E402

PUBLISHED_TURNOUT = {"2020": 66.8, "2022": 52.2, "2024": 65.3}  # P20-585/586/587 Table 1
REQUIRED = ["source", "measure", "generation", "n", "estimate", "se", "adjustment"]
failures = []


def check(ok, msg):
    print(("PASS  " if ok else "FAIL  ") + msg)
    if not ok:
        failures.append(msg)


rates = pd.read_csv(HERE.parent / "service_by_ses_2026_09_23" / "derived" / "cps_civic_rates.csv")
vol = rates[(rates.arm == "adults_18_plus") & (rates.measure == "volunteered")].set_index("group").rate
for grp, want in (("mexico_born", 10.9), ("mexican_2nd_gen", 15.1), ("mexican_3rd_plus", 19.7)):
    got = round(100 * vol[grp], 1)
    check(got == want, f"Sept volunteering {grp}: {got} vs RESULT.md section 4 {want}")

v = pd.read_csv(HERE / "derived" / "voting.csv", dtype={"year": str})
for year, pub in PUBLISHED_TURNOUT.items():
    got = 100 * v[(v.measure == "voted_rate") & (v.generation == "all_citizens") & (v.year == year)].estimate.iloc[0]
    check(abs(got - pub) <= 1.0, f"turnout {year}: lane {got:.2f} vs published {pub} (|diff| <= 1)")

link = dict(line.split(": ") for line in (HERE / "derived" / "gate_spouse_linkage.txt").read_text().splitlines())
check(float(link["share"]) >= 0.99, f"spouse linkage share {float(link['share']):.4f} >= 0.99 "
      f"({link['spouse_found']} of {link['married_25_54']})")

for name in ("voting.csv", "intermarriage.csv", "child_identification.csv", "civic_carryover.csv"):
    cols = pd.read_csv(HERE / "derived" / name, nrows=1).columns
    missing = [c for c in REQUIRED if c not in cols]
    check(not missing, f"{name} schema {'complete' if not missing else 'missing ' + str(missing)}")

t = pd.DataFrame(carryover.cps_sept() + carryover.voting() + carryover.endogamy() + carryover.norms())
t = pd.concat([carryover.add_rho(t), pd.DataFrame(carryover.military_context())], ignore_index=True)
cols = ["source", "measure", "generation", "n", "estimate", "se", "adjustment", "units", "rate", "white_rate",
        "rho_from_previous", "rho_se", "rho_g1_to_g3plus"]
buf = io.StringIO()
t[cols].to_csv(buf, index=False, float_format="%.6g", lineterminator="\n")
check(buf.getvalue() == (HERE / "derived" / "civic_carryover.csv").read_text(),
      "civic_carryover.csv reproduces from the source CSVs")

print(f"\n{len(failures)} failure(s)")
sys.exit(1 if failures else 0)
