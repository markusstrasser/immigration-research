"""Observed Census2024 source refresh, holding incidence assumptions constant."""
import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
NEEDED = [4, 7, 12, 24, 103, 107, 123, 129, 132, 159, 109, 115, 131, 161, *range(48, 57)]


def parse_api(raw):
    """Predicate fields can repeat; collapse only exactly identical columns."""
    frame = pd.DataFrame(raw[1:], columns=raw[0])
    for name in frame.columns[frame.columns.duplicated()].unique():
        repeated = frame.loc[:, frame.columns == name]
        if not all(repeated.iloc[:, 0].equals(repeated.iloc[:, i])
                   for i in range(1, repeated.shape[1])):
            raise ValueError(f"Conflicting duplicate Census field: {name}")
    return frame.loc[:, ~frame.columns.duplicated()].copy()


def us_state_population(frame):
    """Match the 50-state/DC finance universe; Puerto Rico is a separate area."""
    selected = frame[frame.SUMLEV.eq(40) & frame.STATE.ne(72)]
    return selected.set_index("STATE").POPESTIMATE2024


def read_finance(cache, year):
    manifest = json.loads((HERE / "census_sources.json").read_text())
    expected = {r["file"]: r["sha256"] for r in manifest["files"]}
    tables = {}
    for geo in ["us", "state"]:
        name = f"finance_{year}_{geo}_combined.json"
        data = (Path(cache) / name).read_bytes()
        if hashlib.sha256(data).hexdigest() != expected[name]:
            raise ValueError(f"Census source vintage changed: {name}")
        raw = json.loads(data)
        frame = parse_api(raw)
        if not frame.GOVTYPE.eq("001").all() or not frame.YEAR.eq(str(year)).all():
            raise ValueError("Census government/year selection differs")
        if frame.duplicated([geo, "AGG_DESC"]).any():
            raise ValueError("Duplicate Census source key")
        tables[geo] = frame
    states = sorted(tables["state"].state.unique())
    if len(states) != 51:
        raise ValueError("Census release must cover 50 states plus DC")
    records, control_checks = {}, []
    for line in NEEDED:
        code = f"LF{line:04}"
        us = tables["us"].loc[tables["us"].AGG_DESC.eq(code)]
        rows = tables["state"].loc[tables["state"].AGG_DESC.eq(code)].copy()
        if len(us) != 1 or us.AMOUNT_F.notna().any() or rows.AMOUNT_F.notna().any():
            raise ValueError(f"Missing or flagged Census control: {code}")
        rows["dollars"] = pd.to_numeric(rows.AMOUNT, errors="raise") * 1000
        national = float(us.AMOUNT.iloc[0]) * 1000
        if (rows.dollars < 0).any() or abs(rows.dollars.sum() - national) > 51_000:
            raise ValueError(f"Census state sum cannot reconcile to US {code}")
        # API omits zero/not-applicable state cells. Nonnegative reported cells
        # exhaust the independent national control within dollar rounding.
        missing = sorted(set(states) - set(rows.state))
        series = rows.set_index("state").dollars.reindex(states, fill_value=0)
        series.index = series.index.astype(int)
        records[line] = series
        control_checks.append(dict(year=year, line=code, label=us.AGG_DESC_LABEL.iloc[0],
                                   national_dollars=national, sum_reported_states_dollars=float(rows.dollars.sum()),
                                   missing_state_cells=missing, omitted_cell_rule="zero at published precision conditional on national-control conservation"))
    values = pd.DataFrame(records)
    values["G_gross"] = values[103] - values[[107, 123, 129, 132, 159]].sum(axis=1)
    values["fees"] = values[list(range(48, 57))].sum(axis=1)
    values["G_net"] = values.G_gross - values.fees
    values["P"] = values[109] + values[131] + values[161] - values[115]
    if (values[["G_net", "P"]] < 0).any().any():
        raise ValueError("Negative observed service/capital component")
    return values, control_checks


def vintage_effects(d, weight, groups, values, ctx, charges, params, root, cache, allocation):
    fiscal = root / "infra/immigration-fiscal"
    parameter_file = json.loads((fiscal / "ledger_absolute_2026_09_17/params/params.json").read_text())
    source = next(r for r in parameter_file["staged_files"] if r["path"].endswith("NST-EST2024-ALLDATA.csv"))
    path = Path(source["path"])
    if hashlib.sha256(path.read_bytes()).hexdigest() != source["sha256"]:
        raise ValueError("State population source changed")
    population = pd.read_csv(path)
    # The population release includes Puerto Rico at SUMLEV40; the finance
    # survey's US control and the CPS universe cover 50 states plus DC.
    population = us_state_population(population)
    current, checks = read_finance(cache, 2024)
    if set(current.index) != set(population.index):
        raise ValueError("Census finance/population geography mismatch")
    # C and X previously include only state receipts; this refresh includes
    # the same tax types at both state and local levels, explicitly.
    fed_c = params.pick("omb", ["receipts", "corporat"], "money", preferred="receipts_corporation_income")
    fed_x = params.pick("omb", ["receipts", "excise"], "money", preferred="receipts_excise")
    if fed_c is None or fed_x is None:
        raise ValueError("Verified federal receipt anchors required")
    new_c = fed_c + next(r["national_dollars"] for r in checks if r["line"] == "LF0024")
    new_x = fed_x + next(r["national_dollars"] for r in checks if r["line"] == "LF0012")
    old_c = charges.meta["C|wage25_capital75"]["national_dollars"]
    old_x = charges.meta["X|per_capita"]["national_dollars"]
    updated = dict(G=-d.GESTFIPS.map(current.G_net / population).to_numpy(),
                   P=-d.GESTFIPS.map(current.P / population).to_numpy(),
                   C=values["C"] * new_c / old_c, X=values["X"] * new_x / old_x)
    if not np.isfinite(np.column_stack(list(updated.values()))).all():
        raise ValueError("Nonfinite updated charges")
    rows = []
    g_keys = [key for key in charges.meta if key.startswith("G|") and "fees_by_state_per_capita" in charges.meta[key]]
    if len(g_keys) != 1:
        raise ValueError("Expected one canonical service fee mapping")
    old_g = charges.meta[g_keys[0]]
    old_fees = d.GESTFIPS.map(old_g["fees_by_state_per_capita"]).to_numpy() * old_g["deflator"]
    new_fees = d.GESTFIPS.map(current.fees / population).to_numpy()
    for group, mask in groups.items():
        for component in updated:
            before = float(values[component][mask] @ weight[mask]) / 1e9
            after = float(updated[component][mask] @ weight[mask]) / 1e9
            rows.append(dict(allocation=allocation, group=group, component=component,
                             original_signed_bn=before, updated_signed_bn=after, balance_change_bn=after - before,
                             receipt_change_bn=after - before if component in {"C", "X"} else 0,
                             spending_change_bn=before - after if component in {"G", "P"} else 0,
                             scope="Census2024 G/P plus local C/X; unchanged incidence;2024 state population; other account components unchanged"))
        before_fee = float(old_fees[mask] @ weight[mask]) / 1e9
        after_fee = float(new_fees[mask] @ weight[mask]) / 1e9
        rows.append(dict(allocation=allocation, group=group, component="G_fee_grossup",
                         original_signed_bn=0, updated_signed_bn=0, balance_change_bn=0,
                         receipt_change_bn=after_fee - before_fee, spending_change_bn=after_fee - before_fee,
                         scope="Symmetric grossup of observed2024 fees; no net fiscal effect"))
    return rows, checks, str(path)
