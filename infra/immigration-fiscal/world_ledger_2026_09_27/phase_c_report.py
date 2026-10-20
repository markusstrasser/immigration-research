"""Render executed matched-cash readings; preserve blocked beside calculations.

Native-First: figures come from executed CSVs and frozen v7 output.
"""
import argparse
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
import beside_arms as B
from debt_current import load as debt_parts
import valuation as V

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
PARTS = ("world_total_bn", "other_us_residents_bn", "group_total_bn", "mexico_residents_bn")
WEIGHTS = ("equal", "equal_lambda_1.16", "equal_lambda_1.5", "equal_lambda_hendren_a",
           "hendren_a", "hendren_b", "log_a", "log_b")
HOLDS = {
    "R1": "urban p56; state RPP; household consumption PPP; average-cost public goods",
    "R2": "urban p70; state RPP; output service prices; health/social 3a; response-only public goods; consumption-PPP private twin",
    "R3": "R1 with MMP 2.0 hourly same-person G1 parameter (not a causal low bound)",
}


def report(case):
    frame = pd.read_csv(D / f"readings_cash_{case}.csv")
    central = frame[frame.scope.eq("A_completed") & frame.public_pension_share.eq(1)]
    keys = ["reading", "end", "g3_bound", "weighting"]
    V.gate("report_full_cash_product", len(central) == 96 and not central.duplicated(keys).any())
    V.gate("report_reading_values_finite", np.isfinite(central[list(PARTS)]).all().all()
           and np.isfinite(frame[[p for p in PARTS if p != "world_total_bn"]]).all().all())
    source = HERE / "inputs/readings_v7_frozen.csv"
    receipt = json.loads(source.with_suffix(".json").read_text())
    V.gate("v7_comparison_source_pinned", hashlib.sha256(source.read_bytes()).hexdigest() == receipt["frozen_csv_sha256"])
    old = pd.read_csv(source)
    old = old[old.variant.eq("published")].rename(columns={"account_end": "end"})
    old["reading"] = old.reading.map({"reading1": "R1", "reading2": "R2", "reading3": "R3"})
    old = old[old.reading.notna() & old.weighting.isin(WEIGHTS)]
    delta = central.merge(old[keys + list(PARTS)], on=keys, suffixes=("", "_v7"), validate="one_to_one")
    V.gate("v7_bridge_complete", len(delta) == len(central))
    for part in PARTS:
        delta[f"change_{part}"] = delta[part] - delta[f"{part}_v7"]
    delta["comparison_basis"] = "frozen published v7 mixed pension basis versus current matched cash; not a single-case causal effect"
    delta["reason"] = delta.reading.map(HOLDS) + "; cash timing, v8 items9-12, completed donor economics, ownership/G3 statutory/capital/price fixes and pooled payer convention" + ("; v9 selected military/administration/college/basket/health/rate parts and joint16/17 source calibration" if case == "oct16" else "")
    delta.to_csv(D / f"readings_v7_bridge_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    if case == "oct15":
        debt, contract = debt_parts(V.PINS[case])
        debt.to_csv(D / f"debt_split_parts_{case}.csv", index=False, lineterminator="\n", float_format="%.12f")
    else:
        contract = dict(status=f"[BLOCKED: no {case} federal split]", financing_complete=False)
    status = dict(case=case, basis="matched_cash", status="PASS [DEGRADED: P032 funding proxy]",
                  readings_rows=len(frame), main_rows=len(central), scope_B_enters_total=False,
                  s_central=1, s_beside=[.5, 0], debt_status=contract["status"],
                  full_accrual_status="[BLOCKED] Mexico histories/public service-cost bridge missing",
                   shared_holds="Banxico principal; current P032 recipient payments; matched cash; Phase B social-channel scope; budgets GDP money; US general-price-level recipient services with declared WTP/explicit-price exemptions; actual-dollar fiscal costs; no debt recipe in totals",
                  pins=V.PINS[case], full_welfare_rerun_pass=True)
    (D / f"phase_c_status_{case}.json").write_text(json.dumps(status, indent=1, sort_keys=True) + "\n")
    lines = [f"# {case}: executed matched-cash readings", "",
             "All amounts are annual bn US dollar equivalents; positive is a gain with migration. Both ends are personal case specifications, with central economic assumptions fixed. G3+ zero means zero total-compensation premium; upper is the transported G2 sex-age bound.", "",
             "s=1 is [DEGRADED], an all-public P032 proxy. s=.5/0 change Mexico's public financing only; recipient payments stay fixed. B reports counted members' group position beside complete-lineage effects on others: no complete-world total or break-even. Excluded sender debits are disclosed in the CSV. Full accrual and debt recipes remain blocked beside without numbers.", ""]
    for name, hold in HOLDS.items():
        lines += [f"{name} holds: {hold}.", ""]
    lines += ["| Scope | Reading | s | End | G3+ | Weights | World | Group | Other US | Mexico |",
              "|---|---|---:|---|---|---|---:|---:|---:|---:|"]
    for row in frame.itertuples():
        world = f"{row.world_total_bn:.6f}" if np.isfinite(row.world_total_bn) else "partial scope"
        lines.append(f"| {row.scope} | {row.reading} | {row.public_pension_share:g} | {row.end} | {row.g3_bound} | {row.weighting} | {world} | {row.group_total_bn:.6f} | {row.other_us_residents_bn:.6f} | {row.mexico_residents_bn:.6f} |")
    lines += ["", "## Change from frozen published v7 readings", "",
               "This bridge changes pension basis and incorporates the adopted fixes. It is not a single-case effect. Each row holds its named reading, fiscal end, G3+ bound and weighting fixed. The CSV reason column names changed rules.", "",
              "| Reading | End | G3+ | Weights | v7 world | Cash world | Change |",
              "|---|---|---|---|---:|---:|---:|"]
    for row in delta.itertuples():
        lines.append(f"| {row.reading} | {row.end} | {row.g3_bound} | {row.weighting} | {row.world_total_bn_v7:.6f} | {row.world_total_bn:.6f} | {row.change_world_total_bn:+.6f} |")
    lines += ["", f"[CALCULATION: cash_readings.py; readings_cash_{case}.csv; readings_v7_bridge_{case}.csv]", ""]
    (D / f"readings_table_cash_{case}.md").write_text("\n".join(lines))
    print(json.dumps(status, sort_keys=True))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", default="oct16")
    report(parser.parse_args().case)


if __name__ == "__main__":
    main()
