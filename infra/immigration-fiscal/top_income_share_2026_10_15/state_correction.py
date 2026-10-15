"""California-only PIT distribution sensitivity; every other state's key stays fixed.

FTB's preliminary TY2023 resident liability distribution changes California's
within-state AGI-bin masses, never the state's national mass or NIPA's total.
CPS federal AGI proxies California AGI, and resident liability proxies all CA PIT.
These are explicit transport assumptions, not an identified nationwide correction.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import resource
import subprocess
import sys
import time
import urllib.request

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
SOURCE_URL = "https://publish.data.ca.gov/dataset/1555a2c4-740a-4b1c-adf1-1ab7721e90b3/resource/ee16e82e-c2cf-4900-b6c6-121ded321241/download/dof_spring_2025_odp.pdf"
SOURCE_SHA256 = "8d1aaffd9e4a1f7dc63c4dd9d11781a7f1a1b840d67aedfe0495f27bb104f9a9"
SOURCE_PATH = HERE / "_cache/state/ftb_dof_spring_2025.pdf"
# CPS has zero CA positive state liability under $10k in both samples. Pool the
# first three FTB rows to under $20k, rather than impute an unsupported share.
COARSE = ((0, 1, 2, 3), (4, 5, 6, 7), (8, 9), (10,), (11,), (12,), (13,))
LABELS = ("Under $20k (including losses)", "$20k–50k", "$50k–100k",
          "$100k–200k", "$200k–500k", "$500k–1M", "$1M+")


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def source_table(pdf):
    """Extract amounts from page 15, Exhibit A-10 p5; stop if its schema moves."""
    if sha256(pdf) != SOURCE_SHA256:
        raise ValueError("[BLOCKED] California source hash changed; inspect before updating pin")
    text = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], check=True,
                          capture_output=True, text=True).stdout
    pages = text.split("\f")
    page = pages[14]
    if not all(x in page for x in ("EXHIBIT A-10", "PAGE 5 OF 5", "2022-2023", "Resident Returns")):
        raise ValueError("[BLOCKED] expected FTB resident-return table missing on PDF page 15")
    section = page.split("Total Tax Liability", 1)[1].split("1/", 1)[0]
    lines = [x.strip() for x in section.splitlines() if x.strip()]
    values, extracted = [], []
    for line in lines:
        parts = re.split(r"\s{2,}", line)
        # Labels may contain padding around 'to', so locate the trailing six
        # numeric columns (2022 amount/average, 2023 amount/average, two changes).
        if len(parts) < 7:
            raise ValueError(f"[BLOCKED] unparsed FTB liability row: {line}")
        cols = parts[-6:]
        value = int(cols[2].replace(",", "").replace("$", ""))
        label = " ".join(parts[:-6])
        extracted.append({"ftb_label": label, "taxable_year": 2023, "liability_million": value,
                          "source_pdf_page": 15, "source_table": "Exhibit A-10, page 5 of 5"})
        values.append(value)
    if len(values) != 10 or values[-1] != 97083 or sum(values[:-1]) != values[-1]:
        raise ValueError("[BLOCKED] FTB liability rows fail published total or count")
    coarse = [sum(values[:3]), *values[3:-1]]
    return coarse, extracted


def nonincreasing(values, weights):
    """Weighted least-squares PAVA; weights are administrative liability masses."""
    blocks = []
    for i, (value, weight) in enumerate(zip(values, weights, strict=True)):
        if not 0 <= value <= 1 or weight <= 0:
            raise ValueError("[BLOCKED] invalid share or unsupported monotone bin")
        blocks.append([i, i + 1, value * weight, weight])
        while len(blocks) > 1 and blocks[-2][2] / blocks[-2][3] < blocks[-1][2] / blocks[-1][3]:
            b, a = blocks.pop(), blocks.pop()
            blocks.append([a[0], b[1], a[2] + b[2], a[3] + b[3]])
    out = [0.0] * len(values)
    for start, stop, vw, weight in blocks:
        out[start:stop] = [vw / weight] * (stop - start)
    return out


def state_arrays(rows, sample, state=6):
    matched = [r for r in rows if r["sample"] == sample and int(r["state"]) == state]
    selected = {int(r["bin14"]): r for r in matched}
    if len(matched) != len(selected):
        raise ValueError(f"[BLOCKED] duplicate CA bins for {sample}")
    if set(selected) != set(range(14)):
        raise ValueError(f"[BLOCKED] missing CA bins for {sample}")
    total, union = [], []
    for ids in COARSE:
        t = sum(float(selected[b]["total_state"]) for b in ids)
        u = sum(float(selected[b]["union_state"]) for b in ids)
        if t <= 0 or not 0 <= u <= t:
            raise ValueError(f"[BLOCKED] unsupported or invalid CA liability bin: {sample}, {ids}")
        total.append(t)
        union.append(u)
    return total, [u / t for u, t in zip(union, total, strict=True)]


def calculate(rows, admin_amounts, baseline_model_share):
    baseline_rows = [r for r in rows if r["sample"] == "baseline_2025_nominal"]
    national = sum(float(r["total_state"]) for r in baseline_rows)
    union = sum(float(r["union_state"]) for r in baseline_rows)
    if national <= 0 or abs(union / national - baseline_model_share) >= 1e-9:
        raise ValueError("[BLOCKED] baseline CPS national state share fails case-key parity")
    baseline = union / national
    ca_total, current = state_arrays(rows, "baseline_2025_nominal")
    _, pooled = state_arrays(rows, "pooled_real2023")
    ca_mass = sum(ca_total) / national
    ca_raw_share = sum(t * s for t, s in zip(ca_total, current, strict=True)) / sum(ca_total)
    other_contribution = baseline - ca_mass * ca_raw_share
    admin_total = sum(admin_amounts)
    admin_mass = [a / admin_total for a in admin_amounts]
    ca_admin_share = sum(m * s for m, s in zip(admin_mass, current, strict=True))
    current_admin = other_contribution + ca_mass * ca_admin_share
    variants = {"current_CA_admin": current.copy(), "carry_500k": current.copy(),
                "fixed_1_5pct": current.copy(), "pooled_top_only": current.copy(),
                "pooled_unconstrained": current.copy(), "pooled_monotone_central": current.copy()}
    variants["carry_500k"][-1] = current[-2]
    variants["fixed_1_5pct"][-1] = .015
    variants["pooled_top_only"][-1] = pooled[-1]
    variants["pooled_unconstrained"][-3:] = pooled[-3:]
    variants["pooled_monotone_central"][-3:] = nonincreasing(pooled[-3:], admin_mass[-3:])
    arms = {"current": {"share": baseline, "share_change": 0.0,
                         "share_change_vs_CA_admin": baseline - current_admin,
                         "CA_upper_bin_shares": current[-3:], "CA_admin_raked": False}}
    for name, shares in variants.items():
        value = other_contribution + ca_mass * sum(m * s for m, s in zip(admin_mass, shares, strict=True))
        arms[name] = {"share": value, "share_change": value - baseline,
                      "share_change_vs_CA_admin": value - current_admin,
                      "CA_upper_bin_shares": shares[-3:], "CA_admin_raked": True}
    return {"baseline_share": baseline, "baseline_model_share_rounded": baseline_model_share,
            "CA_national_mass": ca_mass, "CA_raw_share": ca_raw_share,
            "CA_admin_share_current": ca_admin_share, "CA_admin_bin_masses": admin_mass,
            "CA_current_bin_shares": current, "CA_pooled_bin_shares": pooled,
            "CA_bin_labels": LABELS, "CA_raw_bin_masses": [t / sum(ca_total) for t in ca_total],
            "other_states_union_contribution_held_fixed": other_contribution, "arms": arms}


def main():
    start = time.perf_counter()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    parser.add_argument("--fetch", action="store_true", help="acquire the pinned FTB PDF if missing")
    args = parser.parse_args()
    if not SOURCE_PATH.exists() and args.fetch:
        SOURCE_PATH.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(SOURCE_URL) as response:
            raw = response.read(10_000_001)
        if len(raw) > 10_000_000:
            raise ValueError("[BLOCKED] FTB source unexpectedly exceeds 10MB")
        SOURCE_PATH.write_bytes(raw)
    if not SOURCE_PATH.exists():
        raise SystemExit("[BLOCKED] missing FTB source; rerun with --fetch")
    amounts, extract = source_table(SOURCE_PATH)
    input_path = HERE / "derived/cps_state_bins.csv"
    with input_path.open(newline="") as f:
        rows = list(csv.DictReader(f))
    model = json.loads(MODEL.read_text())
    line = next(x for x in model["receipts"]["lines"] if x["id"] == "state_local_income_tax")
    result = calculate(rows, amounts, line["cells"]["cbo_collective"]["personal"]["share"])
    result.update({"line": "state_local_income_tax", "national_bn_held_fixed": line["national_bn"],
                   "source": {"url": SOURCE_URL, "sha256": SOURCE_SHA256, "pdf_page": 15,
                              "table": "Exhibit A-10 page 5 of 5", "taxable_year": 2023,
                              "object": "California resident-return total tax liability; preliminary statistical sample",
                              "amounts_unit": "$million", "amounts": amounts},
                   "coverage": "California only; CA national share remains raw CPS; other states unchanged",
                   "assumptions": ["CPS federal AGI bins proxy California AGI bins",
                                   "California resident-return liability distribution proxies all CA liability",
                                   "TY2023 preliminary administrative shape transported to income-year2024 case",
                                   "Published CPS weights identify baseline; case row4/status stack applied downstream",
                                   "Below $200k union shares remain baseline within common coarse bins",
                                   "Under $20k pooled because CPS CA positive liability is zero under $10k",
                                   "Other states and CA national tax-dollar mass stay at baseline CPS values"],
                   "interpretation": "Covered-state sensitivity, not a measured national correction; no federal-tax or SALT-deduction proxy",
                   "stack": "No stack/status/coverage/lineage multiplication here; parent case machinery applies it",
                   "inputs_sha256": {str(p.relative_to(FISCAL)): sha256(p) for p in [input_path, MODEL]}})
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "state_arms.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    with (args.out_dir / "state_ftb_extract.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(extract[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(extract)
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    peak_bytes = peak if sys.platform == "darwin" else peak * 1024
    if peak_bytes >= 2.5 * 1024**3:
        raise ValueError("[BLOCKED] state process exceeded 2.5GiB")
    print(f"PASS state baseline parity; CA mass={result['CA_national_mass']:.6%}; "
          f"central delta={result['arms']['pooled_monotone_central']['share_change']:.9f}; "
          f"seconds={time.perf_counter()-start:.3f}; peak_bytes={peak_bytes}")


if __name__ == "__main__":
    main()
