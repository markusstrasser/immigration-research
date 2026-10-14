"""Read the production model's labor share and verify its fixed-capital form."""
from __future__ import annotations

import hashlib
import importlib.util
import inspect
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "matched_benefits_2026_09_19/model.py"


def main():
    digest = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    pins = json.loads((HERE / "inputs/pins.json").read_text())["files"]
    if pins.get(str(SOURCE.relative_to(HERE.parent))) != digest:
        raise SystemExit("[BLOCKED] primary production model drift: reverify before changing its pin")
    spec = importlib.util.spec_from_file_location("production_model", SOURCE)
    model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(model)
    labor = inspect.signature(model.equilibrium).parameters["labor_share"].default
    # Equal removals in both skill groups give q = 1 - removal at any CES elasticity.
    removal = 0.1
    fixed = model.equilibrium([0.5, 0.5], [removal, removal], adjustment=0.)
    long_run = model.equilibrium([0.5, 0.5], [removal, removal], adjustment=1.)
    q = 1 - removal
    if not (0 < labor < 1
            and abs(float(fixed["capital_without_over_with"]) - 1) < 1e-12
            and abs(float(fixed["output_without_over_with"]) - q**labor) < 1e-12
            and abs(float(long_run["output_without_over_with"]) - q) < 1e-12):
        raise SystemExit("[BLOCKED] production model no longer has the fixed-capital q**labor_share form")
    result = {
        "source": str(SOURCE.relative_to(HERE.parent)),
        "sha256": digest,
        "labor_share": labor,
        "alpha": 1 - labor,
        "first_year_multiplier": labor,
        "rule": "[ASSUMPTION; APPROX] First-order fixed-capital output/profit response: 1 - alpha; business property response 0. Other production and both corporate lines scale their long-run responses.",
        "form_probe": {
            "labor_remaining": q,
            "fixed_capital": float(fixed["capital_without_over_with"]),
            "fixed_output": float(fixed["output_without_over_with"]),
            "long_run_output": float(long_run["output_without_over_with"]),
            "finite_loss_ratio": float((1 - fixed["output_without_over_with"]) / (1 - long_run["output_without_over_with"])),
        },
    }
    (HERE / "derived/first_year_calibration.json").write_text(json.dumps(result, indent=2) + "\n")
    print(f"[gates] fixed-capital form passes (1e-12); alpha={1-labor}, multiplier={labor}")


if __name__ == "__main__":
    main()
