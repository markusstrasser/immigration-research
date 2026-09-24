"""Split the spending that does not follow enrollment into its functions, by specification.

For each estimator (pupil-weighted), function f with share w_f of current spending and response b_f
(elasticity, or marginal-over-average cost for fe_level) contributes w_f * (1 - b_f) to the
non-response of current spending. fe_level is exactly additive over the current parts; the log
estimators are additive only to first order, and the gap is reported.

Classes (the brief: fixed categories are scale economies; a fall in instructional spending per pupil
is dilution):
  dilution            instruction
  dilution, broad     pupil support, instructional staff support (guidance, health, curriculum, libraries)
  scale economies     general, school and business administration; operation and maintenance;
                      transportation (route density); food service and other programs; nonspecified

Capital outlay and interest are outside current spending and outside the account's consumption line;
they are reported beside the table and never added.

The shift-share instrument is not decomposed: its first-stage F is below 10 in every specification
(estimate_iv.py -> derived/iv_first_stage.csv), and the brief uses an instrument only when strong.

Writes derived/nonresponse_decomposition.csv and derived/nonresponse_summary.csv.

    uv run --no-project --with pandas python3 infra/immigration-fiscal/school_dilution_2026_09_24/decompose.py
"""
import json
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
PARTS = {"instruction": "dilution", "pupil_support": "dilution_broad", "instr_staff": "dilution_broad",
         "gen_admin": "scale", "school_admin": "scale", "business": "scale", "om": "scale", "transport": "scale",
         "other_elsec": "scale", "support_other": "scale"}
BESIDE = ["capital_outlay", "interest"]
SPECS = {  # spec name in function_elasticities.csv (pupil-weighted), term, horizon label
    "fd_fy2000_2019": ("dlnN", "1 year"),
    "dl3_fy2000_2019": ("cumulative_3yr", "3 years"),
    "ld_stacked_fy2000_2019": ("dlnN", "4-5 years"),
    "ld19_2000_2019": ("dlnN", "19 years"),
    "fe_log_fy2000_2019": ("lnN", "within-district, all horizons"),
    "fe_level_fy2000_2019": ("x", "within-district, all horizons (additive)"),
}


def main():
    e = pd.read_csv(OUT / "function_elasticities.csv")
    shares = json.loads((OUT / "function_sample.json").read_text())["fy2000_2019"]["shares_of_current"]
    rows, summary = [], []
    for spec, (term, horizon) in SPECS.items():
        sel = e[e.spec.eq(spec) & e.weight.eq("pupils") & e.term.eq(term)].set_index("function")
        if spec.startswith("fe_level"):
            resp, lo, hi = sel.response_ratio, sel.response_ci_low, sel.response_ci_high
        else:
            resp, lo, hi = sel.beta, sel.ci_low, sel.ci_high
        total_nonresp = 1 - resp["current"]
        contrib = {f: shares[f] * (1 - resp[f]) for f in PARTS}
        for f, cls in PARTS.items():
            rows.append({"spec": spec, "horizon": horizon, "function": f, "class": cls, "share_of_current": shares[f],
                         "response": resp[f], "response_ci_low": lo[f], "response_ci_high": hi[f],
                         "contribution": contrib[f], "share_of_nonresponse": contrib[f] / total_nonresp})
        for f in BESIDE:
            rows.append({"spec": spec, "horizon": horizon, "function": f, "class": "beside_current",
                         "share_of_current": shares[f], "response": resp[f], "response_ci_low": lo[f],
                         "response_ci_high": hi[f], "contribution": float("nan"), "share_of_nonresponse": float("nan")})
        sum_parts = sum(contrib.values())
        dil = contrib["instruction"]
        broad = dil + contrib["pupil_support"] + contrib["instr_staff"]
        summary.append({"spec": spec, "horizon": horizon, "current_response": resp["current"],
                        "current_response_ci_low": lo["current"], "current_response_ci_high": hi["current"],
                        "nonresponse_total": total_nonresp, "nonresponse_sum_of_parts": sum_parts,
                        "additivity_gap": total_nonresp - sum_parts,
                        "instruction_response": resp["instruction"],
                        "instruction_ci_low": lo["instruction"], "instruction_ci_high": hi["instruction"],
                        "dilution_share_of_parts": dil / sum_parts, "dilution_broad_share_of_parts": broad / sum_parts,
                        "scale_share_of_parts": 1 - broad / sum_parts})
    d, s = pd.DataFrame(rows), pd.DataFrame(summary)
    d.to_csv(OUT / "nonresponse_decomposition.csv", index=False, lineterminator="\n", float_format="%.6f")
    s.to_csv(OUT / "nonresponse_summary.csv", index=False, lineterminator="\n", float_format="%.6f")
    print(s.to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
