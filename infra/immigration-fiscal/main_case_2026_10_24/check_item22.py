"""Independent check of item 22, without items.cjs.

For every specification row of derived/per_spec.csv (set) and derived/per_spec_cash.csv (cash), recompute item 22
from that row's capital pieces at the case rate (capital_case_rate_<component>_bn) and the rate lane's
rate_model.json theta_pairing.bound {level_by_component, rate_by_level_by_end}, read here directly:

    item 22 = sum over components of piece x (rate[level[component]][end] / r_c - 1)

and compare it with the row's item_capital_rate_theta_bound_bn. Also checks that the pieces add to
capital_case_rate_total_bn, that every component column has a level, and that the row's printed rates are the
lane's. Writes derived/independent_check.json; exits 1 on any failure.

Run: uv run --no-project python3 check_item22.py [--dir DIR].
"""

import csv
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
args = sys.argv[1:]
OUT = Path(args[args.index("--dir") + 1]).resolve() if "--dir" in args else HERE / "derived"
RATE_FILE = HERE.parent / "public_capital_rate_2026_10_24/derived/rate_model.json"

raw = RATE_FILE.read_bytes()
model = json.loads(raw)
bound = model["theta_pairing"]["bound"]
rc = model["r_c"]
level_of = bound["level_by_component"]
rates = bound["rate_by_level_by_end"]
END = {"low": 0, "high": 1}
TOL = 1e-9

failures, report = [], {"rate_file": str(RATE_FILE.relative_to(ROOT)) if RATE_FILE.is_relative_to(ROOT) else str(RATE_FILE),
                        "rate_sha256": hashlib.sha256(raw).hexdigest(), "tolerance_bn": TOL, "files": {}}
for name in ["per_spec.csv", "per_spec_cash.csv"]:
    with open(OUT / name, newline="") as f:
        rows = list(csv.DictReader(f))
    comps = [c[len("capital_case_rate_"):-len("_bn")] for c in rows[0] if c.startswith("capital_case_rate_") and c != "capital_case_rate_total_bn"]
    missing = [c for c in comps if c not in level_of]
    if missing:
        failures.append(f"{name}: components without a level: {missing}")
    worst = worst_total = worst_rate = 0.0
    for row in rows:
        end = END[row["reading"]]
        pieces = {c: float(row[f"capital_case_rate_{c}_bn"]) for c in comps}
        want = sum(v * (rates[level_of[c]][end] / rc - 1) for c, v in pieces.items() if c in level_of)
        got = float(row["item_capital_rate_theta_bound_bn"])
        worst = max(worst, abs(got - want))
        worst_total = max(worst_total, abs(sum(pieces.values()) - float(row["capital_case_rate_total_bn"])))
        for level, pair in rates.items():
            worst_rate = max(worst_rate, abs(float(row[f"rate_{level}"]) - pair[end]))
    ok = worst <= TOL and worst_total <= TOL and worst_rate == 0.0 and len(rows) == 128
    report["files"][name] = {"rows": len(rows), "components": len(comps), "max_abs_error_item22_bn": worst,
                             "max_abs_error_piece_total_bn": worst_total, "max_abs_error_rate": worst_rate, "pass": ok}
    if not ok:
        failures.append(f"{name}: item 22 {worst:.3e}, pieces {worst_total:.3e}, rates {worst_rate:.3e}, rows {len(rows)}")

report["pass"] = not failures
report["failures"] = failures
(OUT / "independent_check.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({k: v for k, v in report.items() if k != "files"} | {"files": {k: v["max_abs_error_item22_bn"] for k, v in report["files"].items()}}))
if failures:
    sys.exit(1)
