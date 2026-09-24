#!/usr/bin/env python3
"""Question 3: who leaves California for Texas, by income, from IRS SOI migration files
(tax-year pairs 2011-12 to 2022-23; returns, individuals and AGI, AGI from the year-2 return).

Gate G3: in every year, (a) California's outflow row to Texas equals Texas's inflow row from
California; (b) the sum of California's destination-state rows equals its "Total Migration-US" row
less suppressed cells; (c) the sum over the other 50 inflow files of their California rows equals
the same total. (d) Every California row of the 2022-23 state outflow CSV equals the "State
Outflow" sheet of the published California workbook 2223ca.xlsx (returns, individuals, AGI).

Writes derived/irs_ca_tx.csv (per year), derived/irs_ca_austin.csv (California counties to the
Austin metro counties, 2018-19 to 2022-23) and derived/gate_irs.csv.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/movers_reasons_2026_09_24/irs_flows.py
"""
import sys

import pandas as pd

from lane_common import CACHE, write_csv

PAIRS = ["1112", "1213", "1314", "1415", "1516", "1617", "1718", "1819", "1920", "2021", "2122", "2223"]
AUSTIN = {453: "Travis", 491: "Williamson", 209: "Hays", 21: "Bastrop", 55: "Caldwell"}  # Austin-Round Rock MSA


def read(kind: str, p: str) -> pd.DataFrame:
    df = pd.read_csv(CACHE / "irs" / f"state{kind}flow{p}.csv", dtype=str, encoding="latin-1")
    df.columns = [c.lower() for c in df.columns]
    for c in ("y1_statefips", "y2_statefips", "n1", "n2", "agi"):
        df[c] = pd.to_numeric(df[c], errors="coerce")
    return df


def row(df: pd.DataFrame, name_col: str, **kw) -> pd.Series:
    sel = pd.Series(True, index=df.index)
    for k, v in kw.items():
        sel &= df[k] == v
    got = df[sel]
    if len(got) != 1:
        raise SystemExit(f"[FAILED] expected one row for {kw}, got {len(got)}")
    return got.iloc[0]


def main() -> None:
    out, gates = [], []
    for p in PAIRS:
        o, i = read("out", p), read("in", p)
        ca_o = o[o.y1_statefips == 6]
        tot_us = ca_o[(ca_o.y2_statefips == 97) & ca_o.y2_state_name.str.contains("Total Migration[- ]US$", regex=True)]
        same = ca_o[(ca_o.y2_statefips == 97) & ca_o.y2_state_name.str.contains("Same State")]
        nonmig = row(ca_o, "y2_state_name", y2_statefips=6)
        dest = ca_o[ca_o.y2_statefips.between(1, 56) & (ca_o.y2_statefips != 6)]
        ca_tx = row(ca_o, "y2_state_name", y2_statefips=48)
        tx_in = i[i.y2_statefips == 48]
        tx_from_ca = row(tx_in, "y1_state_name", y1_statefips=6)
        ca_in = i[i.y2_statefips == 6]
        tx_ca = row(ca_in, "y1_state_name", y1_statefips=48)
        ca_in_us = ca_in[(ca_in.y1_statefips == 97) & ca_in.y1_state_name.str.contains("Total Migration[- ]US$", regex=True)]
        tx_o = o[o.y1_statefips == 48]
        tx_nonmig = row(tx_o, "y2_state_name", y2_statefips=48)
        if len(tot_us) != 1 or len(ca_in_us) != 1:
            sys.exit(f"[FAILED] {p}: total rows not found")
        tot_us, ca_in_us = tot_us.iloc[0], ca_in_us.iloc[0]
        # gate: CA->TX equals TX<-CA; destination rows add to the US total (less suppressed cells)
        g_a = all(ca_tx[k] == tx_from_ca[k] for k in ("n1", "n2", "agi"))
        pos = dest[dest.n1 > 0]
        g_b_diff = float(tot_us.n1 - pos.n1.sum())
        others = i[(i.y1_statefips == 6) & i.y2_statefips.between(1, 56) & (i.y2_statefips != 6)]
        g_c_diff = float(tot_us.n1 - others[others.n1 > 0].n1.sum())
        suppressed = int((dest.n1 < 0).sum())
        gates.append({"pair": p, "ca_to_tx_equals_tx_from_ca": g_a, "ca_total_us_returns": int(tot_us.n1),
                      "sum_destination_rows": int(pos.n1.sum()), "diff_returns": g_b_diff,
                      "sum_other_inflow_files": int(others[others.n1 > 0].n1.sum()), "diff_inflow_side": g_c_diff,
                      "suppressed_cells": suppressed,
                      "pass": g_a and abs(g_b_diff) <= 10 * suppressed and abs(g_c_diff) <= 10 * suppressed})
        out.append({
            "pair": f"20{p[:2]}-20{p[2:]}", "agi_tax_year": 2000 + int(p[2:]) - 1,
            "ca_to_tx_returns": int(ca_tx.n1), "ca_to_tx_individuals": int(ca_tx.n2), "ca_to_tx_agi_bn": ca_tx.agi / 1e6,
            "tx_to_ca_returns": int(tx_ca.n1), "tx_to_ca_individuals": int(tx_ca.n2), "tx_to_ca_agi_bn": tx_ca.agi / 1e6,
            "ca_to_us_returns": int(tot_us.n1), "ca_to_us_individuals": int(tot_us.n2), "ca_to_us_agi_bn": tot_us.agi / 1e6,
            "us_to_ca_returns": int(ca_in_us.n1), "us_to_ca_individuals": int(ca_in_us.n2), "us_to_ca_agi_bn": ca_in_us.agi / 1e6,
            "ca_nonmigrant_returns": int(nonmig.n1), "ca_nonmigrant_agi_bn": nonmig.agi / 1e6,
            "tx_nonmigrant_returns": int(tx_nonmig.n1), "tx_nonmigrant_agi_bn": tx_nonmig.agi / 1e6,
            "ca_same_state_migrant_returns": int(same.iloc[0].n1) if len(same) else None,
        })
    d = pd.DataFrame(out)
    d["agi_per_return_ca_to_tx"] = (d.ca_to_tx_agi_bn * 1e9 / d.ca_to_tx_returns).round()
    d["agi_per_return_tx_to_ca"] = (d.tx_to_ca_agi_bn * 1e9 / d.tx_to_ca_returns).round()
    d["agi_per_return_ca_to_us"] = (d.ca_to_us_agi_bn * 1e9 / d.ca_to_us_returns).round()
    d["agi_per_return_us_to_ca"] = (d.us_to_ca_agi_bn * 1e9 / d.us_to_ca_returns).round()
    d["agi_per_return_ca_stayers"] = (d.ca_nonmigrant_agi_bn * 1e9 / d.ca_nonmigrant_returns).round()
    d["agi_per_return_tx_stayers"] = (d.tx_nonmigrant_agi_bn * 1e9 / d.tx_nonmigrant_returns).round()
    d["ratio_ca_to_tx_vs_ca_stayers"] = (d.agi_per_return_ca_to_tx / d.agi_per_return_ca_stayers).round(3)
    d["net_ca_to_tx_returns"] = d.ca_to_tx_returns - d.tx_to_ca_returns
    d["net_ca_to_tx_agi_bn"] = (d.ca_to_tx_agi_bn - d.tx_to_ca_agi_bn).round(3)
    d["net_ca_to_us_agi_bn"] = (d.ca_to_us_agi_bn - d.us_to_ca_agi_bn).round(3)
    for c in ("ca_to_tx_agi_bn", "tx_to_ca_agi_bn", "ca_to_us_agi_bn", "us_to_ca_agi_bn",
              "ca_nonmigrant_agi_bn", "tx_nonmigrant_agi_bn"):
        d[c] = d[c].round(3)
    # gate G3d: the 2022-23 CSV rows equal the published California workbook (2223ca.xlsx)
    wb = pd.read_excel(CACHE / "irs" / "2223ca.xlsx", sheet_name="State Outflow", header=None)
    wb = wb[pd.to_numeric(wb[0], errors="coerce") == 6]
    o = read("out", "2223")
    pub = {str(r[3]): (int(r[4]), int(r[5]), int(r[6])) for r in wb.itertuples(index=False)}
    csv_rows = {str(r.y2_state_name): (int(r.n1), int(r.n2), int(r.agi)) for r in o[o.y1_statefips == 6].itertuples()}
    identical = pub == csv_rows and all(k in pub for k in ("CA Total Migration-US", "CA Non-migrants", "Texas"))
    gates.append({"pair": "2223 vs 2223ca.xlsx", "ca_to_tx_equals_tx_from_ca": None,
                  "ca_total_us_returns": pub["CA Total Migration-US"][0], "sum_destination_rows": None,
                  "diff_returns": float(pub["CA Total Migration-US"][0] - csv_rows["CA Total Migration-US"][0]),
                  "sum_other_inflow_files": None, "diff_inflow_side": None, "suppressed_cells": None,
                  "pass": identical, "note": f"published workbook rows {len(pub)}, CSV rows {len(csv_rows)}, all identical: {identical}; "
                                        f"Texas {pub['Texas']}"})
    write_csv(d, "irs_ca_tx.csv")
    write_csv(pd.DataFrame(gates), "gate_irs.csv")

    # California counties to the Austin metro counties
    # County cells under 20 returns are suppressed, so the Austin sum is a floor; the state file's
    # California-to-Texas total is the full denominator.
    state_tx = dict(zip(d.pair, d.ca_to_tx_returns))
    au = []
    for p in ("1819", "1920", "2021", "2122", "2223"):
        f = CACHE / "irs" / f"countyoutflow{p}.csv"
        df = pd.read_csv(f, dtype=str, encoding="latin-1")
        df.columns = [c.lower() for c in df.columns]
        for c in ("y1_statefips", "y1_countyfips", "y2_statefips", "y2_countyfips", "n1", "n2", "agi"):
            df[c] = pd.to_numeric(df[c], errors="coerce")
        sel = (df.y1_statefips == 6) & (df.y2_statefips == 48) & df.y2_countyfips.isin(AUSTIN) & (df.n1 > 0)
        s = df[sel]
        tx_all = df[(df.y1_statefips == 6) & (df.y2_statefips == 48) & (df.y2_countyfips.between(1, 999)) & (df.n1 > 0)]
        au.append({"pair": f"20{p[:2]}-20{p[2:]}", "ca_counties_to_austin_returns": int(s.n1.sum()),
                   "individuals": int(s.n2.sum()), "agi_bn": round(s.agi.sum() / 1e6, 3),
                   "agi_per_return": round(s.agi.sum() * 1e3 / s.n1.sum()),
                   "ca_county_rows": int(len(s)),
                   "ca_to_all_tx_counties_returns_unsuppressed": int(tx_all.n1.sum()),
                   "austin_share_of_unsuppressed_county_rows": round(s.n1.sum() / tx_all.n1.sum(), 3),
                   "austin_share_of_state_file_ca_to_tx": round(s.n1.sum() / state_tx[f"20{p[:2]}-20{p[2:]}"], 3)})
    write_csv(pd.DataFrame(au), "irs_ca_austin.csv")
    ok = all(g["pass"] for g in gates)
    print(("PASS" if ok else "FAIL") + f" G3 IRS consistency, {len(gates)} tax-year pairs")
    print(d[["pair", "ca_to_tx_returns", "ca_to_tx_agi_bn", "agi_per_return_ca_to_tx", "agi_per_return_ca_stayers",
             "ratio_ca_to_tx_vs_ca_stayers", "net_ca_to_tx_agi_bn", "net_ca_to_us_agi_bn"]].to_string(index=False))
    print(pd.DataFrame(au).to_string(index=False))
    if not ok:
        print(pd.DataFrame(gates).to_string(index=False))
        sys.exit(1)


if __name__ == "__main__":
    main()
