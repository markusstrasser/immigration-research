#!/usr/bin/env python3
"""Each group's 2024 line amounts on the sept29 case, for the debt legacy of the comparators.

The white replacement lane's sept29 re-key (`white_replacement_2026_09_28/rekey_sept29.py`, imported read-only; its
module-level build reads files and writes nothing) prices every line of the adopted case for any population on one
code path: the case's nationals, responses and capital; each group's rough CPS/MEPS keys on audit row 4's weights,
every slice scaled to the 39,712,493 people the account prices. This script runs its `setup()` (its own gates:
the dumps are the adopted bands, the row-4 frame, the positive controls) and `run29()` for four groups, on both
bases (cash: the cash set; accrual: the case's pension rule at each group's own accrual per tax dollar) and at both
end specifications (48 / 11), and writes every line's amount and response:

  mexican_origin_engine   the engine's own union amounts (the debt lane's anchor; parity input)
  mexican_origin_rough    the union on the rough keys every comparator uses (the like-for-like reference)
  A1_third_plus_nh_white  third-plus-generation non-Hispanic whites at their own ages
  all_residents_slice     an average-resident slice

Gate: each group's cost from the written amounts equals rekey_summary_sept29.csv's cost (5e-5, its 4 decimals).
Output: derived/group_lines_sept29.csv (tracked). Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run python3 infra/immigration-fiscal/legacy_comparators_2026_09_30/group_lines.py

--case oct05 writes derived/group_lines_oct05.csv from the library's oct05 run (the v5 case adopted 2026-10-05): both
union rows carry the 3,039,720 added people at the case lane's amounts on every line (the engine union's lines are the
case's own), A1 and the all-residents slice are on the lineage's 42,752,213, and the gate reads the white lane's
rekey_summary_oct05.csv. The capital return is in each group's cost_bn row, as for sept29.

--case oct07 writes derived/group_lines_oct07.csv from the library's oct07 run (main case v6, main_case_2026_10_07: v5
plus the items of its payload's meta.items): as oct05, with the items' union parts on both union rows (the engine union's
lines are the case's own; the rough union takes the union-only lines and the user-fee item's carrier receipt lines at
the engine's amounts, the library's rule 5), every group's accrual on the 2026 separate-funds path, and the gate on the
white lane's rekey_summary_oct07.csv.

On oct05 and oct07 the library keys Pell by each group's IPEDS share and public higher education by its measured use
(the lead's decision of 2026-10-07, a named defect fix; sept29 keeps the September 27 keys), so the rough union's and
A1's other_federal_benefits and education_services rows carry those terms. On oct07 the library adds item 4's tuition
term on education_services; its hospital term stays beside the central (the team lead, 2026-10-07), so no
health_services row carries it.

On oct05 and oct07 the library's central keys every group's income taxes on the case's own keys (round 2, the team
lead's instruction of 2026-10-07): federal income tax on v4 item 3's IRS-raked key, state and other personal taxes on
the state-liability key, the shared allocation. The rough union's and A1's federal_income_tax, state_local_income_tax
and other_personal_tax rows carry those keys; sept29 keeps the CPS-dollar rule.
"""
from __future__ import annotations

import csv
import importlib.util
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
WHITE = FISCAL / "white_replacement_2026_09_28"
GROUPS = ("mexican_origin_engine", "mexican_origin_rough", "A1_third_plus_nh_white", "all_residents_slice")
BASES = ("cash", "accrual")
ENDS = ("low", "high")
SIDE = {"receipts": "receipt", "spending": "spending"}     # the debt lane's side names


def load_rekey():
    spec = importlib.util.spec_from_file_location("rekey_sept29", WHITE / "rekey_sept29.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules["rekey_sept29"] = module
    spec.loader.exec_module(module)
    return module


def main(case: str = "sept29") -> None:
    K = load_rekey()
    K.use_case(case)
    K.setup()
    K.stop_if_failed()
    scen = K.scenarios()
    summary = pd.read_csv(WHITE / f"derived/rekey_summary_{case}.csv")
    rows, fails = [], []
    for basis in BASES:
        for end in ENDS:
            for g in GROUPS:
                r, lines, _, _, _ = K.run29(scen[g], end, basis)
                want = summary[(summary.basis == basis) & (summary.group == g) & (summary.end == end)].iloc[0]
                if abs(r["cost"] - want.cost) > 5e-5 or int(round(r["population"])) != int(want.population):
                    fails.append(f"{g} {basis} {end}: cost {r['cost']:.6f} vs {want.cost:.4f}")
                e = (K.FULL or K.DUMP)[basis][end]     # oct05: the case's dump (K.DUMP is its identified union)
                prod = next(x for x in e["lines"] if x["side"] == "scalar" and x["id"] == "production_gain_bn")
                for side, lid, national, amount, response in lines:
                    rows.append(dict(group=g, basis=basis, end=end, spec=e["spec"], side=SIDE[side], line=lid,
                                     national_bn=f"{national:.10f}", amount_bn=f"{amount:.10f}",
                                     response=f"{response:.10f}"))
                rows.append(dict(group=g, basis=basis, end=end, spec=e["spec"], side="scalar", line="cost_bn",
                                 national_bn="", amount_bn=f"{r['cost']:.10f}", response=""))
                rows.append(dict(group=g, basis=basis, end=end, spec=e["spec"], side="scalar", line="population",
                                 national_bn="", amount_bn=f"{r['population']:.4f}", response=""))
                rows.append(dict(group=g, basis=basis, end=end, spec=e["spec"], side="scalar",
                                 line="production_gain_bn", national_bn="",
                                 amount_bn=f"{(r['production_gain']):.10f}", response=""))
                print(f"  {basis:7s} {end:4s} {g:24s} cost {r['cost']:9.4f} (rekey_summary {want.cost:9.4f})"
                      f"  production {r['production_gain']:.4f} (dump {prod['effect_bn']:.4f})")
    if fails:
        raise SystemExit(f"[BLOCKED] group lines do not reproduce rekey_summary_{case}.csv: " + "; ".join(fails))
    out = HERE / "derived"
    out.mkdir(exist_ok=True)
    with open(out / f"group_lines_{case}.csv", "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    print(f"[written] derived/group_lines_{case}.csv: {len(rows)} rows")


if __name__ == "__main__":
    import argparse
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--case", default="sept29", choices=["sept29", "oct05", "oct07"],
                    help="sept29 (default), oct05 (v5) or oct07 (v6)")
    main(ap.parse_args().case)
