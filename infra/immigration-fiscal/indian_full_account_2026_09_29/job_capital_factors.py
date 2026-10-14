"""Indian-frame personal job-capital factors, using the source lane's construction read-only.

The same CPS 2025 INDUSTRY codes pass through job_capital.cell_of (including LJCW
government overrides). Thin cells use the source's N_MIN/SECTOR rule; wages >= TOP
are spread as national top wages. Mining and residential tax cells carry zero.
Factor = sum(industry wage share * national industry tax) / line national / plain
wage share. Group replicate weights propagate factor uncertainty; national weights
stay fixed, consistently with rekey_indian's other replicate keys.

  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/job_capital_factors.py
This command checks the committed white_nh personal factors at 1e-9; it writes nothing.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "job_capital_taxes_2026_10_14"
spec = importlib.util.spec_from_file_location("job_capital_source", SOURCE / "job_capital.py")
J = importlib.util.module_from_spec(spec)
spec.loader.exec_module(J)


class Factors:
    def __init__(self, frame, national_weights, *, foreign_source_removed=False):
        source_item = json.loads((SOURCE / "derived/item.json").read_text())
        if any(not g["passed"] for g in source_item["gates"]):
            raise SystemExit("[BLOCKED] source job-capital item has failed gates")
        self.item = source_item["arms"]["foreign_source_removed"] if foreign_source_removed else source_item
        self.provenance = {str(p.relative_to(HERE.parent)): hashlib.sha256(p.read_bytes()).hexdigest()
                           for p in (SOURCE / "job_capital.py", J.CROSSWALK,
                                     SOURCE / "derived/national_by_industry.csv", SOURCE / "derived/item.json")}
        nat = pd.read_csv(SOURCE / "derived/national_by_industry.csv").set_index("cell")
        cells = list(nat.index) + ["NOIND"]
        xw = pd.read_csv(J.CROSSWALK, dtype={"census_code": str})
        if not xw.census_code.is_unique or not set(xw.bea_industry) <= set(cells) | {"GOV"}:
            raise SystemExit("[BLOCKED] job-capital industry crosswalk invalid")
        cell = J.cell_of(frame, xw)
        self.wage = frame.WSAL_VAL.clip(lower=0).to_numpy(float)
        civ = J.masks(frame)["civilian"]
        if not set(cell[self.wage > 0]) <= set(cells):
            raise SystemExit("[BLOCKED] Indian-frame wage-bearing industry codes do not map")
        # Non-wage unmapped records have no effect on wages, but cannot index a tax cell.
        idx = np.array([cells.index(c) if c in cells else cells.index("NOIND") for c in cell])
        w = np.asarray(national_weights) * civ
        national = np.bincount(idx, weights=self.wage * w, minlength=len(cells))
        self.national_wages = float(national.sum())
        counts = np.bincount(idx[civ & (self.wage > 0)], minlength=len(cells))
        sectors = np.array([J.SECTOR[c] for c in cells])
        private = np.flatnonzero(~np.isin(sectors, ["government", "households", "none"]))
        pools = []
        for i in range(len(cells)):
            sector = np.flatnonzero(sectors == sectors[i])
            pools.append(np.array([i]) if counts[i] >= J.N_MIN or sectors[i] == "none"
                         else sector if counts[sector].sum() >= J.N_MIN else private)
        high = self.wage >= J.TOP
        nat_high = np.bincount(idx, weights=np.where(high, self.wage * w, 0), minlength=len(cells))
        self.rate = {}
        self.columns = {"corporate": "corporate_ex_foreign_bn" if foreign_source_removed else "corporate_bn",
                        "business_property": "c_and_i_property_bn",
                        "other_production_taxes": "other_production_taxes_bn"}
        for category, column in self.columns.items():
            vector = np.append(nat[column].to_numpy(float), 0.0)
            vector[np.isin(sectors, ["mining", "none"])] = 0.0
            if abs(float(vector.sum()) - self.item["lines"][category]["base_bn"]) > 1e-9:
                raise SystemExit(f"[BLOCKED] {category}: national industry vector does not reproduce item base")
            rate = np.zeros(len(cells))
            for i, pool in enumerate(pools):
                den = national[pool].sum()
                if vector[i] and den <= 0:
                    raise SystemExit(f"[BLOCKED] {category}: taxed cell has no national wages")
                if den > 0:
                    rate[pool] += vector[i] / den
            person_rate = rate[idx]
            if nat_high.sum() > 0:
                person_rate[high] = float(nat_high @ rate / nat_high.sum())
            self.rate[category] = person_rate
        self.civilian = civ

    def measure(self, group_weights):
        wages = np.asarray(group_weights) * self.civilian * self.wage
        plain = float(wages.sum() / self.national_wages)
        if plain <= 0:
            raise SystemExit("[BLOCKED] job-capital factor undefined: group has no wages")
        return {category: float(wages @ rate / self.item["lines"][category]["national_bn"] / plain)
                for category, rate in self.rate.items()}


def positive_control(*, foreign_source_removed=False):
    frame = J.load_frame()
    masks = J.masks(frame)
    weights = J.row4_weights(frame, masks, json.loads(J.checked(J.ROW4, J.ROW4_SHA).read_text()))[:, 0]
    calculator = Factors(frame, weights, foreign_source_removed=foreign_source_removed)
    measured = calculator.measure(weights * masks["white"])
    expected = calculator.item["factor"]["white_nh"]
    rows = [{"line": category, "measured": value, "committed": expected[category]["personal"],
             "absolute_difference": abs(value - expected[category]["personal"])}
            for category, value in measured.items()]
    if any(row["absolute_difference"] >= 1e-9 for row in rows) or any(not g["passed"] for g in J.GATES):
        raise SystemExit(f"[BLOCKED] job-capital positive control failed: {rows}")
    print("PASS job-capital white_nh personal positive control (1e-9):", rows)
    return rows


def run_positive_control(*, foreign_source_removed=False):
    """Keep the source's 161-column frame out of the already-loaded fiscal process."""
    command = [sys.executable, str(Path(__file__).resolve()), "--json"]
    if foreign_source_removed:
        command.append("--foreign-source-removed")
    result = subprocess.run(command,
                            text=True, capture_output=True)
    print(result.stdout, end="", flush=True)
    if result.returncode:
        print(result.stderr, file=sys.stderr, end="")
        raise SystemExit("[BLOCKED] isolated job-capital positive control failed")
    return json.loads(result.stdout.splitlines()[-1])


def source_tax_line_changes(before, after):
    """Measure item 9 on evaluated own-group lines, rejecting unrelated changes."""
    old = {(side, line): (national, amount, response) for side, line, national, amount, response in before}
    new = {(side, line): (national, amount, response) for side, line, national, amount, response in after}
    if len(old) != len(before) or len(new) != len(after) or old.keys() != new.keys():
        raise SystemExit("[BLOCKED] item-9 comparison has duplicate or unmatched job lines")
    rows = []
    for (side, line), (national, amount, response) in new.items():
        previous_national, previous_amount, previous_response = old[(side, line)]
        if abs(national - previous_national) > 1e-9 or abs(response - previous_response) > 1e-9:
            raise SystemExit("[BLOCKED] item-9 comparison changed a national total or response")
        difference = amount - previous_amount
        if line in ("corporate_capital", "corporate_labor"):
            if side != "receipts":
                raise SystemExit("[BLOCKED] item-9 corporate source line is not a receipt")
            rows.append({"line": line, "national_bn": national, "response": response,
                         "old_receipt_bn": previous_amount, "domestic_receipt_bn": amount,
                         "receipt_change_bn": difference, "net_cost_change_bn": -difference * response})
        elif abs(difference) > 1e-9:
            raise SystemExit(f"[BLOCKED] item-9 comparison changed unrelated line {line}")
    if len(rows) != 2:
        raise SystemExit("[BLOCKED] item-9 comparison needs both corporate source lines")
    return rows


if __name__ == "__main__":
    control = positive_control(foreign_source_removed="--foreign-source-removed" in sys.argv)
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    print(f"[memory] peak physical footprint {require_within_budget('Indian job-capital control') / 1e9:.3f} GB")
    if "--json" in sys.argv:
        print(json.dumps(control))
