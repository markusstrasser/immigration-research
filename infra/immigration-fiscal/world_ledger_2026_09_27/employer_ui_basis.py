"""Employer share of the live receipt account's heterogeneous domestic-social residual.

Pinned BEA primary workbook, 2024 tables 3.1/3.6. Includes UI and every other employer
contribution outside OASDI/HI. Household/self-employed contributions stay inside cash.
No group-specific employer observation is claimed: the group uses the national employer
fraction under the account's existing common positive-FICA-worker allocation key.
"""
import argparse
import functools
import hashlib
import json
import resource
import sys
import time
from decimal import Decimal
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
SOURCE = "bea_nipa_section3_2026_08_26.xlsx"


def gate(name, ok, **details):
    if not ok:
        raise SystemExit(f"[BLOCKED] {name}: {details}")


def source_path():
    manifest = HERE / "inputs/pins.json"
    gate("employer_other_manifest_exists", manifest.is_file())
    pins = json.loads(manifest.read_text())
    row = pins["files"].get(SOURCE)
    gate("employer_other_source_declared", row is not None)
    path = HERE / row["path"]
    gate("employer_other_source_exists", path.is_file(), path=str(path))
    gate("employer_other_source_hash", hashlib.sha256(path.read_bytes()).hexdigest() == row["sha256"])
    return path, row


def read_table(path, sheet):
    d = pd.read_excel(path, sheet_name=sheet, header=None)
    header = [i for i in range(len(d)) if str(d.iloc[i, 0]).strip() == "Line"]
    gate("employer_other_table_header_unique", len(header) == 1, sheet=sheet)
    head = header[0]
    columns = [j for j, v in enumerate(d.iloc[head]) if str(v) in ("2024", "2024.0")]
    gate("employer_other_2024_column_unique", len(columns) == 1, sheet=sheet)
    gate("employer_other_units_millions", "[Millions of dollars]" in d.iloc[:head, 0].astype(str).tolist())
    year_col = columns[0]
    out = {}
    for r in d.iloc[head + 1:].itertuples(index=False, name=None):
        raw_line = str(r[0]).strip()
        if raw_line.isdigit():
            line = int(raw_line)
            gate("employer_other_line_unique", line not in out, sheet=sheet, line=line)
            out[line] = {"label": str(r[1]).strip(), "bea_series": str(r[2]), "bn": float(r[year_col]) / 1000}
    return out


def compute_basis(t31, t36):
    """Exact account denominator; distinguish source rounding from measured workers."""
    def cell(table, line, expected):
        gate("employer_other_required_line", line in table, line=line)
        row = table[line]
        gate("employer_other_label", expected in row["label"], line=line, label=row["label"])
        gate("employer_other_cell_finite", np.isfinite(row["bn"]), line=line)
        return row["bn"]

    domestic = cell(t31, 8, "From persons")
    employers = cell(t36, 2, "Employer contributions")
    employer_oasdi_hi = cell(t36, 4, "hospital insurance")
    personal = cell(t36, 20, "Employee and self-employed contributions")
    personal_oasdi_hi = cell(t36, 22, "hospital insurance")
    supplementary = cell(t36, 27, "Supplementary medical insurance")
    ui = cell(t36, 7, "Unemployment insurance")
    dec = lambda x: Decimal(str(x))
    denominator = float(dec(domestic) - dec(personal_oasdi_hi) - dec(employer_oasdi_hi) - dec(supplementary))
    employer = float(dec(employers) - dec(employer_oasdi_hi))
    worker = float(dec(personal) - dec(personal_oasdi_hi) - dec(supplementary))
    # BEA tables publish millions. Keep their independently rounded two-million
    # discrepancy as an explicit source-rounding component, never as an employer.
    rounding = float(dec(denominator) - dec(employer) - dec(worker))
    gate("employer_other_denominator_positive", denominator > 0)
    gate("employer_other_nonnegative_components", employer >= 0 and worker >= 0 and ui >= 0)
    gate("employer_other_ui_subset", ui <= employer <= denominator)
    gate("employer_other_source_rounding_bounded", abs(rounding) <= 0.003 + 1e-10)
    gate("employer_other_national_closure", abs(employer + worker + rounding - denominator) < 1e-6)
    return dict(year=2024, national_domestic_residual_bn=denominator,
                national_employer_residual_bn=employer, national_worker_residual_bn=worker,
                national_source_rounding_bn=rounding, national_employer_ui_bn=ui,
                employer_fraction=employer / denominator, worker_fraction=worker / denominator,
                source_rounding_fraction=rounding / denominator, employer_ui_fraction=ui / denominator,
                group_allocation_assumption="Apply this national payer mix to the account's "
                    "other_domestic_social_contributions, whose positive_FICA_worker key is common to the mix. "
                    "The group's actual employer/worker mix is not measured.",
                unidentified_group_employer_fraction_bound=[0.0, 1.0],
                payer="employers for employer residual; worker/self-employed for worker residual; "
                      "unassigned source rounding, not an employer contribution",
                locators={"denominator": "T30100-A/8 - T30600-A/22 - T30600-A/4 - T30600-A/27",
                          "employer": "T30600-A/2 - T30600-A/4", "ui_subset": "T30600-A/7",
                          "worker": "T30600-A/20 - T30600-A/22 - T30600-A/27"},
                cells={"T30100-A/8": t31[8], **{f"T30600-A/{i}": t36[i] for i in (2, 4, 7, 20, 22, 27)}})


@functools.lru_cache(maxsize=1)
def load_basis():
    path, pin = source_path()
    out = compute_basis(read_table(path, "T30100-A"), read_table(path, "T30600-A"))
    out["source"] = pin
    return out


def allocate_group(residual_bn, basis=None):
    """Allocation of a frozen case's exact group receipt; caller supplies its live amount."""
    b = load_basis() if basis is None else basis
    gate("employer_other_group_residual_finite_nonnegative", np.isfinite(residual_bn) and residual_bn >= 0)
    employer = residual_bn * b["employer_fraction"]
    worker = residual_bn * b["worker_fraction"]
    rounding = residual_bn * b["source_rounding_fraction"]
    gate("employer_other_group_closure", abs(employer + worker + rounding - residual_bn) < 1e-6)
    return dict(employer_bn=employer, worker_bn=worker, source_rounding_bn=rounding,
                ui_subset_bn=residual_bn * b["employer_ui_fraction"],
                unidentified_employer_bound_bn=[0.0, residual_bn])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", type=Path, default=HERE / "derived/us_employer_other_basis.json")
    args = ap.parse_args()
    start = time.perf_counter()
    out = load_basis()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({"employer_fraction": out["employer_fraction"],
                      "seconds": time.perf_counter() - start,
                      "maxrss_bytes": resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}), file=sys.stderr)


if __name__ == "__main__":
    main()
