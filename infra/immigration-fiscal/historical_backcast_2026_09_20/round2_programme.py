"""Transport verified programme branches and price the new case's known use keys."""
from __future__ import annotations

import hashlib
import json

import pandas as pd

import backcast as b
from p7_backcast import use_cell


def inputs():
    audit = json.loads((b.HERE / "derived/p7/audit.json").read_text())
    for path, expected in audit["inputs"].items():
        if hashlib.sha256((b.ROOT / path).read_bytes()).hexdigest() != expected:
            raise ValueError(f"[BLOCKED] frozen programme source changed: {path}")
    use = pd.read_csv(b.HERE / "derived/p7/historical_use.csv").set_index(["key", "group", "year"])
    if not use.index.is_unique:
        raise ValueError("[BLOCKED] duplicate historical-use cell")
    for key in ("school_age_5_17", "medicaid_covered"):
        for group in ("union", "g3plus"):
            for year in b.YEARS:
                use_cell(use, key, group, year)
    measured = pd.read_csv(b.FISCAL / "backcast_pandemic_measured_2026_09_28/derived/measured_shares.csv")
    eip = measured.set_index(["key", "status", "allocation", "income_year"])
    cells = [("eip1_advance", "borjas", "personal", 2020),
             ("eip2", "borjas", "personal", 2020),
             ("eip1_catchup", "borjas", "personal", 2020),
             ("eip3", "borjas", "personal", 2021)]
    cells += [("refundable_credits", "none", "personal", year) for year in (2020, 2021, 2024)]
    for cell in cells:
        if cell not in eip.index:
            if cell == ("eip1_catchup", "borjas", "personal", 2020):
                from pandemic_zero import require_zero
                require_zero()
                continue
            raise ValueError(f"[BLOCKED] missing pandemic-use cell {cell}")
    return pd.read_csv(b.HERE / "derived/p7/programme_lines.csv"), use


def branch_paths(table, end, population):
    out = {}
    for variant in ("programme", "programme_pandemic", "programme_measured"):
        rows = table[(table.end == end) & (table.population == population)
                     & (table.rule == "programme") & (table.variant == variant)]
        values = rows.groupby("year").cost_bn.sum().reindex(b.YEARS)
        if values.isna().any():
            raise ValueError(f"[BLOCKED] missing programme branch {end}/{population}/{variant}")
        out[variant] = values
    return out


def new_measured_parts(parts, metadata, use, end):
    """New known programme keys get their own historical use, not the old total's displacement."""
    result = {k: v.copy() for k, v in parts.items()}
    audit = []
    for part, info in metadata.items():
        if info.get("item") not in ("foreign_source_tax", "union_completion", "mixed_unit_removal", "coverage"):
            continue
        if info.get('use_key_exempt'):
            continue
        lid = info.get("parent") or info["line"]
        key = "school_age_5_17" if lid == "education_services" else "medicaid_covered" if lid == "medicaid_and_chip_other_medical" else None
        if key is None or info["side"] != "spending" or part not in result:
            continue
        group = "g3plus" if info.get("path") == "lineage" or info.get("population_path") == "g3plus" else "union"
        fraction = info.get('measured_fraction', 1.0)
        if key == "school_age_5_17" and info["line"] == "education_services":
            # Same K12 operating fraction as P7; college/other education use stays fixed.
            engine = json.loads((b.HERE / "derived/p7/programme_inputs.json").read_text())
            fraction = engine[end]["lineage"]["spec"]["share"]
        if key == "medicaid_covered" and 'measured_fraction' not in info:
            engine = json.loads((b.HERE / "derived/p7/programme_inputs.json").read_text())
            fraction = engine[end]["lineage"]["medicaid_coverage_fraction"]
        anchor = use_cell(use, key, group, 2024).relative_use
        for year in b.YEARS:
            value = use_cell(use, key, group, year)
            if value is not None:
                result[part][year] *= 1 + fraction * (value.relative_use / anchor - 1)
        audit.append(dict(part=part, key=key, group=group, measured_fraction=fraction,
                          delta_2015_2024_bn=(result[part] - parts[part]).loc[2015:2024].sum()))
    return result, audit
