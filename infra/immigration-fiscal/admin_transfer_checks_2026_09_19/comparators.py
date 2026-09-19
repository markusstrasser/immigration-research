"""Calendar-year comparators and deliberately noncausal uniform-raking arms."""
from datetime import datetime
import hashlib
import json
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

def pinned(path, expected):
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"Source vintage changed: {path}: {actual}")

def snap_months(rows):
    selected = []
    for row_number, row in enumerate(rows, 1):
        label = row[0]
        if not isinstance(label, str) or label.startswith("FY"):
            continue
        try:
            month = datetime.strptime(label, "%b %Y")
        except ValueError:
            continue
        if month.year == 2024:
            value = row[3]
            if not isinstance(value, (int, float)) or not np.isfinite(value) or value < 0:
                raise ValueError(f"Invalid monthly benefit at {row_number}")
            selected.append(dict(month=month.strftime("%Y-%m"), amount_dollars=value, source_row=row_number))
    if len(selected) != 12 or len({r["month"] for r in selected}) != 12:
        raise ValueError("Need exactly twelve unique calendar2024 months")
    return pd.DataFrame(selected).sort_values("month")

def bea_rows(rows):
    header = [r for r in rows if r[0] == "Line"]
    if len(header) != 1 or header[0].count("2024") != 1 or rows[1][0] != "[Millions of dollars]":
        raise ValueError("BEA year/unit declaration does not match")
    col = header[0].index("2024")
    result={}
    # Unused rows can contain literal missing-value markers. Never substitute
    # them for the explicitly requested program cells.
    for row in rows:
        if not str(row[0]).isdigit() or int(row[0]) not in {5,7,21,23,36}:
            continue
        if not isinstance(row[col],(int,float)) or not np.isfinite(row[col]):
            raise ValueError(f"Missing required BEA program cell: {row[0]}")
        result[int(row[0])]=dict(label=row[1].strip(),amount_bn=row[col]/1000)
    return result

def read_comparators(here, bea_path):
    source_path = here / "source_cells.json"
    sources = json.loads(source_path.read_text())
    snap_path = here / "_cache/snap-monthly.xlsx"
    pinned(snap_path, sources["snap"]["sha256"])
    book = openpyxl.load_workbook(snap_path, read_only=True, data_only=True)
    rows = list(book.active.values)
    book.close()
    if rows[2][3] != "Benefit Costs":
        raise ValueError("Not a benefit-cost column")
    months = snap_months(rows)
    snap = months.amount_dollars.sum()/1e9
    ss = sources["social_security"]
    domestic = (ss["all_areas"] - sum(ss["excluded"].values()))/1000
    ssi = sources["ssi_due"]
    if ssi["total"] != ssi["federal"] + ssi["federally_administered_state"]:
        raise ValueError("SSI federal/state sum fails")
    pinned(bea_path, sources["bea"]["sha256"])
    book = openpyxl.load_workbook(bea_path, read_only=True, data_only=True)
    bea = bea_rows(list(book["T31200-A"].values))
    book.close()
    definitions = [
        ("USDA_monthly_CY2024", "snap", snap, sources["snap"]["scope"]),
        ("SSA_50states_DC", "social_security", domestic, ss["scope"]),
        ("SSA_all_areas", "social_security", ss["all_areas"]/1000, "Includes overseas and territories; diagnostic only"),
        ("SSA_federally_administered_due", "ssi", ssi["total"]/1e6, ssi["scope"]),
        ("SSA_federal_cash", "ssi", sources["ssi_cash_federal"]["value"]/1000, sources["ssi_cash_federal"]["scope"]),
    ]
    for program, lines in sources["bea"]["rows"].items():
        definitions.append(("BEA_persons", program, sum(bea[n]["amount_bn"] for n in lines), sources["bea"]["scope"]))
    official = pd.DataFrame([dict(comparator=c, program=p, official_bn=v, scope=s) for c,p,v,s in definitions])
    arms = {
        "SNAP_OASDI_only": {"snap":snap,"social_security":domestic},
        "plus_SSI_administered_due": {"snap":snap,"social_security":domestic,"ssi":ssi["total"]/1e6},
        "plus_SSI_BEA_persons": {"snap":snap,"social_security":domestic,"ssi":bea[23]["amount_bn"]+bea[36]["amount_bn"]},
        "BEA_three_programs": {p:sum(bea[n]["amount_bn"] for n in sources["bea"]["rows"][p])
                               for p in ["snap","social_security","ssi"]},
    }
    return official, months, arms, [source_path, snap_path, bea_path]

def rake_shift(group_base, national_base, old_ratio, target):
    if national_base <= 0 or target < 0:
        raise ValueError("Invalid raking denominator or target")
    factor = target/national_base
    return factor, -group_base*(factor-old_ratio)

def compare(table, macro, official, arms):
    national = table[table.group.eq("national_civilian")]
    errors = national.merge(official, on="program", validate="many_to_many")
    for name in ["baseline", "after_U"]:
        errors[f"{name}_minus_official_bn"] = errors[f"{name}_bn"] - errors.official_bn
        errors[f"{name}_error_pct"] = 100*errors[f"{name}_minus_official_bn"]/errors.official_bn
    components, totals = [], []
    for allocation in ["shared","personal"]:
        nat = national[national.allocation.eq(allocation)].set_index("program")
        group_rows = table[table.allocation.eq(allocation) & table.group.eq("mexican_observed_total")].set_index("program")
        baseline_balance = macro.loc[macro.allocation.eq(allocation) & macro.group.eq("mexican_observed_total"),"signed_bn"].sum()
        for arm, targets in arms.items():
            changes = []
            for program, target in targets.items():
                row, group = nat.loc[program], group_rows.loc[program]
                factor, change = rake_shift(group.baseline_bn,row.baseline_bn,row.historical_ratio,target)
                components.append(dict(arm=arm,allocation=allocation,program=program,
                    official_target_bn=target,uniform_ratio=factor,target_group_baseline_bn=group.baseline_bn,
                    balance_change_bn=change,national_identity_residual_bn=factor*row.baseline_bn-target))
                changes.append(change)
            totals.append(dict(arm=arm,allocation=allocation,baseline_balance_bn=baseline_balance,
                balance_change_bn=sum(changes),sensitivity_balance_bn=baseline_balance+sum(changes),
                interpretation="Uniform raking sensitivity; administrative population/timing gaps unresolved; not ethnic correction or causal effect"))
    return errors,pd.DataFrame(components),pd.DataFrame(totals)
