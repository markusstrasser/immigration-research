"""The quantity share of each state-price gap, for valuing the sept29 case's three state-price lines.

The lead's ruling on valuation rule 1 (2026-09-29): a state-price line is part of its parent line priced where the
group lives. Its gap splits into a wage level and a quantity (state_priced_services_2026_09_29, RESULT "Wage
demarcation"). The wage part buys the group the same service at a higher price, so the group values it at 0; the
quantity part is more service, valued at the parent's class. valuation.py multiplies each state-price line's value by
the line's quantity share from this file; the cost to other residents keeps the whole gap.

For a function f of the state-pricing lane's central package, with gap_f its correction before the response
(corrections.csv pre_response_bn): quantity_f = gap_f x (real_f - 1) / (index_f - 1), where index_f is the group's
price index and real_f its quantity index (spending deflated by S&L pay in the function, over the same for everyone),
so the wage share of the gap is 1 - (real_f - 1) / (index_f - 1). It comes from the lane's wage_demarcation.csv
(FY2024, direct expenditure), except for state prisons, which the central package prices per prisoner
(corrections_per_inmate) and the demarcation file prices per resident. For them this script applies the lane's
method to the per-prisoner index: the lane's weights (the group located as each state imprisons, wr), its costs per
prisoner, and, as the ruling directs where a function has no demarcation row, the lane's fallback wage, all state and
local government pay (QCEW 2023 NAICS 10, own codes 2+3). The base is the all-prisoner weighting, under which the price
index is 1. valuation.py values state prisons at justice's offender-processing class, 0, so their pay basis moves no
value. A quantity share can be negative: the group then gets less of the service than the national average, and its
value falls below the parent line's.

Inputs: the state-pricing lane at its commit PIN (derived/corrections.csv, wage_demarcation.csv,
prison_cost_by_state.csv, group_population_by_state.csv), and its state_price.py (populations(), qcew_wage_index(),
FUNCTIONS, CENTRAL), imported read-only after a gate that the working tree holds the pinned file.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/state_price_quantity.py
Output: derived/state_price_quantity.csv, one row per function and one per state-price line.
"""
import importlib.util
import io
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
LANE = "infra/immigration-fiscal/state_priced_services_2026_09_29"
PIN = "ea41242"          # the lane's commit (2026-09-29 00:53 JST), whose central package candidate v4 carries


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def git(*args):
    return subprocess.run(["git", "-C", str(REPO), *args], capture_output=True, check=True).stdout


def pinned_csv(name):
    return pd.read_csv(io.BytesIO(git("show", f"{PIN}:{LANE}/derived/{name}")))


def main():
    code = f"{LANE}/state_price.py"
    gate("state_price_py_is_the_pinned_file", git("rev-parse", f"{PIN}:{code}") == git("hash-object", code), pin=PIN)
    spec = importlib.util.spec_from_file_location("state_price", REPO / code)
    sp = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(sp)
    corr = pinned_csv("corrections.csv")
    corr = corr[corr.candidate].set_index("function")
    wd = pinned_csv("wage_demarcation.csv")
    wd = wd[(wd.year == 2024) & (wd.basis == "direct")].set_index("function")
    rows = []
    for parent, functions in sp.CENTRAL.items():
        gate(f"central_functions_are_the_candidate_rows_{parent}",
             sorted(functions) == sorted(corr.index[corr.line == parent]), functions=functions)
        for f in functions:
            c = corr.loc[f]
            if f in wd.index:
                d = wd.loc[f]
                gate(f"demarcation_index_is_the_correction_index_{f}", abs(d["index"] - c["index"]) < 1e-9,
                     demarcation=d["index"], correction=c["index"])
                rows.append(dict(line=f"state_price_{parent}", function=f, gap_bn=c.pre_response_bn,
                                 index=d["index"], wage_level_index=d.wage_level_index, real_index=d.real_index,
                                 source="wage_demarcation.csv (FY2024 direct)",
                                 qcew_fallback_states=d.qcew_fallback_states if isinstance(d.qcew_fallback_states, str)
                                 else ""))
                continue
            gate(f"only_state_prisons_lack_a_demarcation_row_{f}", f == "corrections_per_inmate", function=f)
            # The lane's per-prisoner weights and costs (state_price.prison_per_inmate, FY2024 institutions).
            pc = pinned_csv("prison_cost_by_state.csv").assign(fips=lambda x: x.fips.astype(int)).set_index("fips")
            gp = pinned_csv("group_population_by_state.csv").set_index("fips")
            pris, rel = pc.prisoners, pc.relative
            pop = sp.populations(2024).reindex(pris.index)
            w = gp.group_share.reindex(pris.index)
            w = w / w.sum()
            wr = w * (pris / pop)
            wr = wr / wr.sum()
            allp = pris / pris.sum()
            index = float((wr * rel).sum())
            gate("per_prisoner_index_reproduces_the_lane", abs(index - c["index"]) < 1e-9, index=index, lane=c["index"])
            # 1 to the ten significant digits the lane's CSV keeps.
            gate("all_prisoner_index_is_one", abs(float((allp * rel).sum()) - 1) < 1e-9,
                 index=float((allp * rel).sum()))
            # All S&L government pay: the parks_libraries column, whose only industry is NAICS 10.
            wage, _ = sp.qcew_wage_index()
            gate("parks_libraries_pay_is_naics_10", sp.FUNCTIONS["parks_libraries"]["naics"] == ["10"])
            wg = wage["parks_libraries"].reindex(pris.index)
            gate("all_sl_pay_complete", bool(wg.notna().all()))
            real = float((wr * rel / wg).sum()) / float((allp * rel / wg).sum())
            rows.append(dict(line=f"state_price_{parent}", function=f, gap_bn=c.pre_response_bn,
                             index=index, wage_level_index=float((wr * wg).sum()), real_index=real,
                             source="computed per prisoner: all S&L government pay (QCEW NAICS 10), the lane's "
                                    "fallback", qcew_fallback_states=""))
    out = pd.DataFrame(rows)
    out["quantity_share"] = (out.real_index - 1) / (out["index"] - 1)
    out["wage_share_of_gap"] = 1 - out.quantity_share
    out["quantity_bn"] = out.gap_bn * out.quantity_share
    # Gate: each demarcation row's wage share is the lane's: the same formula on its CSV's ten significant digits,
    # which a small gap (judicial: index - 1 = 0.011) amplifies to about 1e-7.
    lane = wd.wage_share_of_gap.reindex(out.function)
    d = (out.wage_share_of_gap.to_numpy() - lane.to_numpy())[out.function.isin(wd.index).to_numpy()]
    gate("wage_shares_are_the_lanes", bool(np.all(np.abs(d) < 1e-6)), max_abs_diff=float(np.abs(d).max()))
    lines = out.groupby("line", sort=False)[["gap_bn", "quantity_bn"]].sum().reset_index()
    lines["quantity_share"] = lines.quantity_bn / lines.gap_bn
    lines["function"], lines["source"] = "all", "sum of the line's functions"
    # Gate: each line's gap is its candidate rows' sum in corrections.csv.
    want = corr.groupby("line").pre_response_bn.sum()
    gap = {f"state_price_{k}": v for k, v in want.items()}
    worst = max(abs(r.gap_bn - gap[r.line]) for r in lines.itertuples())
    gate("line_gaps_are_the_central_package", worst < 1e-9, max_abs_diff=worst)
    cols = ["line", "function", "gap_bn", "index", "wage_level_index", "real_index", "wage_share_of_gap",
            "quantity_share", "quantity_bn", "source", "qcew_fallback_states"]
    res = pd.concat([out, lines], ignore_index=True)[cols]
    res.to_csv(DERIVED / "state_price_quantity.csv", index=False, lineterminator="\n", float_format="%.9f")
    print(res.drop(columns=["source", "qcew_fallback_states"]).round(4).to_string(index=False))
    print(f"  wrote derived/state_price_quantity.csv: {len(res)} rows (state-pricing lane at {PIN})")


if __name__ == "__main__":
    main()
