"""Oct15 current-flow mapping. A missing government share is never zero."""
import io
import json

import numpy as np
import pandas as pd

from committed_inputs import checked_bytes

DEBT = "infra/immigration-fiscal/debt_legacy_2026_09_23/derived/oct15"
MAPPING = {
    "federal_bn": ("cash", "federal_bn"),
    "state_local_bn": ("cash", "state_local_bn"),
    "resource_cost_bn": ("resource_cost", "responsive_bn"),
    "resource_cost_federal_bn": ("resource_cost", "federal_bn"),
    "displaced_bn": ("displaced_beneficiaries", "responsive_bn"),
    "displaced_federal_bn": ("displaced_beneficiaries", "federal_bn"),
    "accrual_bn": ("pension_accrual", "responsive_bn"),
}


def map_parts(frame, bands, basis):
    selected = frame[frame.basis.eq(basis) & frame.convention.eq("central")]
    allowed = {financing for financing, _ in MAPPING.values()} | {"unlocated", "private_production"}
    if not set(selected.financing) <= allowed:
        raise SystemExit(f"[BLOCKED] unknown financing category: {sorted(set(selected.financing)-allowed)}")
    if set(selected.end) != {"low", "high"}:
        raise SystemExit("[BLOCKED] current-flow split needs both case ends")
    rows = []
    for index, end in enumerate(("low", "high")):
        cells = selected[selected.end.eq(end)]
        if not np.isfinite(cells.responsive_bn).all():
            raise SystemExit("[BLOCKED] nonfinite current-flow amount")
        total = float(cells.responsive_bn.sum())
        error = abs(total - bands[index])
        if error > 1e-6:
            raise SystemExit(f"[BLOCKED] current-flow parts do not match case: {basis}/{end}: {error}bn")
        unlocated = cells.financing.eq("unlocated")
        missing = cells[["federal_bn", "state_local_bn"]].isna().any(axis=1)
        # Require the producer's declared missing fields: a renamed category or
        # new NaN cannot disappear through pandas' default skip-NaN reduction.
        if not missing.equals(unlocated):
            raise SystemExit("[BLOCKED] undeclared missing government shares")
        government = cells[~unlocated & ~cells.financing.eq("private_production")]
        if ((government.federal_bn + government.state_local_bn - government.responsive_bn).abs() > 1e-6).any():
            raise SystemExit("[BLOCKED] classified government shares do not close source parts")
        parts = {}
        for field, (financing, column) in MAPPING.items():
            values = cells.loc[cells.financing.eq(financing), column]
            if not np.isfinite(values).all():
                raise SystemExit(f"[BLOCKED] nonfinite classified split {field}")
            parts[field] = float(values.sum())
        unknown_abs = float(cells.loc[unlocated, "responsive_bn"].abs().sum())
        unknown_net = float(cells.loc[unlocated, "responsive_bn"].sum())
        rows.append(dict(basis=basis, end=end, net_cost_bn=total, case_error_bn=error,
                         unlocated_bn=unknown_net, unlocated_absolute_bn=unknown_abs,
                         status="[BLOCKED: no oct15 federal split]" if unknown_abs > 1e-6 else "identified",
                         **parts))
    return pd.DataFrame(rows)


def load(pins):
    contract = json.loads(checked_bytes(pins["debt"], f"{DEBT}/current_flow_contract.json"))
    frame = pd.read_csv(io.BytesIO(checked_bytes(pins["debt"], f"{DEBT}/current_flow_source_parts_2024.csv")))
    summary = json.loads(checked_bytes(pins["main_case"],
                         "infra/immigration-fiscal/main_case_2026_10_15/derived/summary.json"))
    parts = pd.concat([map_parts(frame, summary["v8"][key], basis)
                       for basis, key in (("set", "band_bn"), ("cash", "cash_set_bn"))], ignore_index=True)
    return parts, contract
