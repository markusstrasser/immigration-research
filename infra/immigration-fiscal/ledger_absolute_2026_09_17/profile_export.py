"""Versioned point-estimate age schedules from the annual account itself.

No new estimator or uncertainty claim: household and personal base attribution
reuse all_age_ledger.matrices, and expanded items reuse build_charges.
"""
from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

KEY = ["allocation", "account", "group", "band"]
TARGETS = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]
UNION = "mexican_observed_total"
BASE = ["tax", "cash", "noncash", "employer", "sales", "owner_property", "school", "lunch"]
SIGNS = np.array([1, -1, -1, 1, 1, 1, -1, 1])


def _matrices(state):
    path = Path(__file__).resolve().parent.parent / "all_age_ledger_2026_09_17/analyze.py"
    spec = importlib.util.spec_from_file_location("annual_profile_base", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.matrices(state)


def validate_profiles(profiles, components):
    """Reject ambiguous keys, bad denominators, and inconsistent decompositions."""
    if profiles.empty or components.empty:
        raise ValueError("Empty age profile export")
    for table, key, numeric in [
            (profiles, KEY, ["population", "net_total", "net_per_person"]),
            (components, KEY + ["component"], ["population", "signed_total"])]:
        if table.duplicated(key).any() or table[key].isna().any().any():
            raise ValueError(f"Missing or duplicate profile key: {key}")
        if not np.isfinite(table[numeric].to_numpy()).all() or (table.population <= 0).any():
            raise ValueError("Nonfinite profile value or nonpositive population")
        bands = table.groupby(KEY[:-1]).band.agg(lambda x: set(x))
        if not bands.map(lambda x: x == set(range(8))).all():
            raise ValueError("Profiles must cover every age band 0 through 7")
    joined = components.groupby(KEY, as_index=False).agg(
        signed_total=("signed_total", "sum"), population=("population", "first"),
        population_values=("population", "nunique"))
    joined = profiles.merge(joined, on=KEY, how="outer", suffixes=("", "_component"),
                            validate="one_to_one", indicator=True)
    if not joined._merge.eq("both").all() or not joined.population_values.eq(1).all():
        raise ValueError("Profile/component coverage mismatch")
    if not np.allclose(joined.population, joined.population_component, rtol=1e-12, atol=1e-8):
        raise ValueError("Component population differs from profile denominator")
    if not np.allclose(joined.net_total, joined.signed_total, rtol=1e-12, atol=.02):
        raise ValueError("Age profile component sum differs from net total")
    if not np.allclose(joined.net_total / joined.population, joined.net_per_person,
                       rtol=1e-12, atol=1e-8):
        raise ValueError("Age profile per-person arithmetic failed")
    indexed = profiles.set_index(KEY).sort_index()
    for allocation in ["shared", "personal"]:
        for account in ["partial", "expanded"]:
            union = indexed.loc[(allocation, account, UNION)]
            parts = [indexed.loc[(allocation, account, g)] for g in TARGETS]
            for col in ["population", "net_total"]:
                if not np.allclose(union[col], sum(p[col] for p in parts), rtol=1e-12, atol=.02):
                    raise ValueError(f"Union is not the sum of targets: {allocation}/{account}/{col}")


def export_profiles(state, ctx, charges, centrals, stats, means, inst_by_group, out,
                    *, personal_builder):
    """Export both allocations; personal_builder receives a copied personal ctx.

    Call after inst_by_group exists. The callback returns build_charges' tuple,
    using fresh Params so personal audit lookups do not alter the shared audit.
    """
    if personal_builder is None:
        raise ValueError("Expanded personal profiles require personal charge reconstruction")
    shared, personal, _ = _matrices(state)
    d = state["d"]
    weight = np.asarray(ctx["weights"])[:, 0]
    bands = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    masks = {g: np.asarray(state["group"][g]) & ctx["civilian"]
             for g in inst_by_group if g != UNION}
    masks[UNION] = np.logical_or.reduce([masks[g] for g in TARGETS])
    personal_ctx = dict(ctx, allocation="personal", consumption_proxy=personal[:, 4])
    p_charges, p_dropped, p_centrals, _, _ = personal_builder(personal_ctx)
    if p_centrals != centrals:
        raise ValueError("Personal and shared profiles selected different annual item arms")
    rows, detail, anchors = [], [], {}
    for allocation, matrix, charge_set in [("shared", shared, charges),
                                            ("personal", personal, p_charges)]:
        expanded_items = {item: charge_set.data[charge_set.columns.index(f"{item}|{arm}")]
                          for item, arm in centrals.items() if arm is not None}
        for group, mask in masks.items():
            cell = stats[group]
            pop = cell["n"][:, 0]
            totals = np.array([matrix[mask & (bands == b)].T @ weight[mask & (bands == b)]
                               for b in range(8)])
            if allocation == "shared" and not np.allclose(totals, cell["y"][:, :8, 0],
                                                           rtol=1e-12, atol=.02):
                raise ValueError(f"Shared base age schedule drift: {group}")
            base = {name: totals[:, i] * SIGNS[i] for i, name in enumerate(BASE)}
            base["medical"] = -(cell["h"][:, :, 0] @ means)
            expanded = dict(base)
            for item, vector in expanded_items.items():
                expanded[item] = np.bincount(bands[mask], weights=vector[mask] * weight[mask],
                                              minlength=8)
                if allocation == "shared":
                    k = 8 + charges.columns.index(f"{item}|{centrals[item]}")
                    if not np.allclose(expanded[item], cell["y"][:, k, 0],
                                       rtol=1e-12, atol=.02):
                        raise ValueError(f"Shared item age schedule drift: {group}/{item}")
            expanded["N"] = -np.asarray(inst_by_group[group], dtype=float)
            for account, values in [("partial", base), ("expanded", expanded)]:
                net = np.sum(list(values.values()), axis=0)
                anchors[f"{allocation}|{account}|{group}"] = float(net.sum())
                for band in range(8):
                    key = dict(allocation=allocation, account=account, group=group,
                               band=band, population=float(pop[band]))
                    rows.append(dict(**key, net_total=float(net[band]),
                                     net_per_person=float(net[band] / pop[band])))
                    detail.extend(dict(**key, component=name, signed_total=float(value[band]))
                                  for name, value in values.items())
    profiles, components = pd.DataFrame(rows), pd.DataFrame(detail)
    validate_profiles(profiles, components)
    out = Path(out)
    files = {}
    for name, table in [("age_profiles.csv", profiles), ("age_profile_components.csv", components)]:
        path = out / name
        table.sort_values(KEY + (["component"] if "component" in table else [])).to_csv(path, index=False)
        files[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    return dict(files=files, price_year=2024, primary_allocation="personal",
                point_estimates_only=True, totals=anchors, personal_items_dropped=p_dropped,
                institution_N_denominator_note="N is an external ACS institutional-cost add divided "
                "by the CPS civilian household population in each age band. It is an allocated "
                "burden per household resident, not an institutional resident cost or transition rate.",
                allocation_note="Personal attribution uses direct tax, cash, employer payroll, "
                "school, K, D, and person-reported U recipients. Unit-level noncash and indirect "
                "receipts retain their documented household or incidence allocation. Medical stays "
                "personal in both arms. Person weights mean reallocations may change weighted totals.")
