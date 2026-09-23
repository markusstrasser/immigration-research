"""Inputs for restating Borjas's (2001) efficiency gain for 2024, from the ACS 2024 extract and BEA.

- m: Mexico-born workers relative to all other workers (Borjas's m = M/N), and the same for
  Mexico-born arrivals of the last five years (YOEP >= 2019), the "new immigrants" his sorting
  evidence concerns.
- theta: the Mexico-born share located in the high-wage states, where the high-wage states are
  those with the highest mean log full-time annual wage of US-born workers with high school or
  less (25-54), taken in order until they hold lambda = 40% of those US-born workers; the same
  for lambda = 30% and 45% (Borjas's three columns). The gap between the two groups is reported
  next to the model's implied gap 0.3 ln((1 - lambda) / lambda).
- GDP 2024 from BEA NIPA Table 1.1.5 (vintage published 26 August 2026), read from the repo's
  source copy.

Writes derived/borjas_2024_inputs.json and derived/borjas_state_sorting.csv.
"""
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
BEA = REPO / "sources" / "immigration-fiscal" / "data" / "external" / "bea_nipa" / "Section1All_xls.xlsx"


def gdp_2024() -> float:
    ws = openpyxl.load_workbook(BEA, read_only=True)["T10105-A"]
    rows = list(ws.iter_rows(values_only=True))
    years = next(r for r in rows if r[0] == "Line")
    col = list(years).index("2024")
    line1 = next(r for r in rows if r[1] and str(r[1]).strip() == "Gross domestic product")
    return float(line1[col]) * 1e6


def main() -> None:
    p = pd.read_parquet(HERE / "_cache" / "acs" / "p2024.parquet")
    p = p[~p["gq"]]
    emp = p[p["employed"]]
    M = float(emp.loc[emp["group"] == "mex_fb", "pwgtp"].sum())
    N = float(emp.loc[emp["group"] != "mex_fb", "pwgtp"].sum())
    M_recent = float(emp.loc[(emp["group"] == "mex_fb") & (emp["yoep"] >= 2019), "pwgtp"].sum())
    M_union = float(emp.loc[emp["group"].isin(["mex_fb", "mex_nb"]), "pwgtp"].sum())
    ft = emp[(emp["wkhp"] >= 35) & (emp["wage_real"] > 0) & emp["lowed"] & emp["agep"].between(25, 54)]
    nat = ft[ft["group"].isin(["mex_nb", "oth_nb"])]
    idx = nat.groupby("st").apply(lambda d: np.average(np.log(d["wage_real"]), weights=d["pwgtp"]),
                                  include_groups=False).rename("native_lowed_log_wage")
    wn = emp[emp["lowed"] & emp["group"].isin(["mex_nb", "oth_nb"])].groupby("st")["pwgtp"].sum().rename("native_lowed_workers")
    wm = emp[emp["lowed"] & (emp["group"] == "mex_fb")].groupby("st")["pwgtp"].sum().rename("mexfb_lowed_workers")
    wr = emp[emp["lowed"] & (emp["group"] == "mex_fb") & (emp["yoep"] >= 2019)].groupby("st")["pwgtp"].sum().rename("mexfb_recent_lowed_workers")
    st = pd.concat([idx, wn, wm, wr], axis=1).fillna(0).sort_values("native_lowed_log_wage", ascending=False)
    st["cum_native_share"] = st["native_lowed_workers"].cumsum() / st["native_lowed_workers"].sum()
    st.to_csv(DERIVED / "borjas_state_sorting.csv")
    sorting = {}
    for lam in (0.30, 0.40, 0.45):
        hi = st["cum_native_share"].shift(fill_value=0.0) < lam  # states up to the one crossing lambda
        top, rest = st[hi], st[~hi]
        gap = (np.average(top["native_lowed_log_wage"], weights=top["native_lowed_workers"])
               - np.average(rest["native_lowed_log_wage"], weights=rest["native_lowed_workers"]))
        sorting[str(lam)] = {
            "lambda_realised": float(top["native_lowed_workers"].sum() / st["native_lowed_workers"].sum()),
            "theta_mexfb": float(top["mexfb_lowed_workers"].sum() / st["mexfb_lowed_workers"].sum()),
            "theta_mexfb_recent": float(top["mexfb_recent_lowed_workers"].sum() / st["mexfb_recent_lowed_workers"].sum()),
            "observed_log_wage_gap": float(gap), "model_gap": float(0.3 * np.log((1 - lam) / lam)),
            "high_wage_states": [int(s) for s in top.index]}
    inputs = {"gdp_2024": gdp_2024(), "native_workers": N, "mexfb_workers": M,
              "mexfb_recent_workers": M_recent, "union_workers": M_union,
              "scenarios": [{"name": "mexico_born_all", "m": M / N},
                            {"name": "mexico_born_arrived_2019_2024", "m": M_recent / N},
                            {"name": "mexican_origin_union_upper", "m": M_union / (N + M - M_union)}],
              "sorting": sorting}
    (DERIVED / "borjas_2024_inputs.json").write_text(json.dumps(inputs, indent=2))
    print(json.dumps({k: v for k, v in inputs.items() if k != "sorting"}, indent=1))
    print(json.dumps(sorting, indent=1))


if __name__ == "__main__":
    main()
