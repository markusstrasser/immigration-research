#!/usr/bin/env python3
"""Premium tax credit (PTC) per lawfully present Mexican-born parent, by age.

The late-arrival tail lane has no PTC line of its own. Its ledger charges the credit's outlays per
capita, at every age, inside the rest-of-budget item R: OMB records the refundable credit in
subfunction 551, and the ledger's R carries function 550 net of federal Medicaid and CHIP
(ledger_absolute_2026_09_17/absolute_ledger.py, "550_health_net"). A parent of 55-64 outside
Medicare and Medicaid is far more likely than average to hold Marketplace coverage, so this script
keys the same national dollars by coverage and age, and adjusters.py swaps that key for the
per-capita share. Eligibility is quoted in reads/eligibility_rules.md section 7: no five-year bar;
lawfully present LPRs below 100% FPL who cannot get Medicaid because of their status were treated as
at 100% FPL through tax year 2025.

Method (a key-by-coverage allocation of the Treasury total):
  PTC dollars: Monthly Treasury Statement Table 5 line "Refundable Premium Tax Credits and Cost
    Sharing Reductions", net outlays of FY2024 (October 2023 to September 2024), the year of the
    ledger's OMB functions; fetched from api.fiscaldata.treasury.gov into _cache/ptc/ if missing.
    Per capita inside R: that total over the ledger's US resident population.
  Keys: CPS ASEC 2025 persons with any subsidized Marketplace coverage last year (MRKS = 1), each
    weighted by the CMS federal default age curve (premium ratio by age; the credit rises with the
    premium). Dollars per person-with-coverage at age a = total x f(a) / sum(w f(a) [MRKS=1]).
  Take-up for a lawfully present Mexican-born parent: the CPS MRKS rate of Mexico-born people of the
    same age band. Naturalized citizens are the central proxy (lawfully present, same origin and age);
    noncitizens (who include the unauthorized, not eligible) are the low case; the high case is the
    MRKS rate of all US residents of that age with no employer coverage, no Medicaid and no Medicare,
    the position of a parent inside the Medicaid bar.
CPS under-reports Marketplace enrollment; allocating the Treasury total over CPS-reported coverage
keeps the product (take-up x dollars) consistent with Treasury outlays.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/ptc.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import subprocess
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
OUT = HERE / "derived"
MTS = HERE / "_cache/ptc/mts_table5_ptc_fy2024.json"
MTS_URL = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_5"
           "?filter=classification_desc:eq:Refundable%20Premium%20Tax%20Credits%20and%20Cost%20Sharing%20"
           "Reductions,record_date:gte:2023-10-01,record_date:lte:2024-12-31"
           "&fields=record_date,classification_desc,current_month_net_outly_amt,current_fytd_net_outly_amt"
           "&page%5Bsize%5D=100")
MTS_CY = ROOT / "infra/immigration-fiscal/dataset_integrity_2026_09_23/derived/spending_mts_credits.json"
LEDGER_AUDIT = ROOT / "infra/immigration-fiscal/ledger_absolute_2026_09_17/derived/audit.json"
ASEC = ROOT / "infra/immigration-fiscal/gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CURVE = HERE / "_cache/ptc/cms_state_age_curves_2017.txt"
CURVE_URL = ("https://www.cms.gov/cciio/programs-and-initiatives/health-insurance-market-reforms/"
             "downloads/statespecagecrv053117.pdf")
MEXICO = 303  # PENATVTY, CPS ASEC 2025 Appendix H
BANDS = ((45, 55), (55, 60), (60, 65), (65, 70))


def sha256(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def default_curve() -> dict[int, float]:
    """Default premium ratio by single age from the CMS table (first numeric column)."""
    curve = {}
    for line in CURVE.read_text().splitlines():
        m = re.match(r"\s*(\d+)(?:-(\d+))?(\s+and Older)?\s+(\d\.\d{3})\s", line)
        if not m:
            continue
        lo = int(m.group(1))
        hi = int(m.group(2)) if m.group(2) else (120 if m.group(3) else lo)
        for a in range(lo, hi + 1):
            curve[a] = float(m.group(4))
    assert curve[21] == 1.0 and curve[60] == 2.714 and curve[64] == 3.0 and curve[0] == 0.765, curve
    assert all(a in curve for a in range(0, 101)), sorted(set(range(101)) - set(curve))
    return curve


def fy2024_total_bn() -> float:
    """FY2024 net outlays of the credit line: the twelve months October 2023 to September 2024."""
    if not MTS.exists():
        MTS.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run(["curl", "-sS", "--fail", "--max-time", "60", "-A", "Mozilla/5.0", "-o", str(MTS), MTS_URL],
                       check=True)
    rows = json.loads(MTS.read_text())["data"]
    months = {r["record_date"][:7]: float(r["current_month_net_outly_amt"]) for r in rows}
    fy = [f"2023-{m}" for m in ("10", "11", "12")] + [f"2024-{m:02d}" for m in range(1, 10)]
    assert all(m in months for m in fy), sorted(set(fy) - set(months))
    total = sum(months[m] for m in fy)
    fytd = [float(r["current_fytd_net_outly_amt"]) for r in rows if r["record_date"] == "2024-09-30"]
    assert len(fytd) == 1 and abs(total - fytd[0]) < 1.0, (total, fytd)
    cy = sum(months[f"2024-{m:02d}"] for m in range(1, 13)) / 1e9
    assert abs(cy - json.loads(MTS_CY.read_text())["lines"]["ptc"]["cy2024_bn"]) < 0.001, cy
    return total / 1e9


def main() -> None:
    OUT.mkdir(exist_ok=True)
    total_bn = fy2024_total_bn()
    resident = float(json.loads(LEDGER_AUDIT.read_text())["us_resident_population"])
    curve = default_curve()
    cols = ["A_AGE", "PRCITSHP", "PENATVTY", "MRKS", "GRP", "MCAID", "MCARE", "MARSUPWT"]
    with zipfile.ZipFile(ASEC) as z:
        d = pd.read_csv(z.open("pppub25.csv"), usecols=cols)
    d["w"] = d.MARSUPWT.astype(float) / 100  # two implied decimals (CPS ASEC 2025 dictionary)
    assert 330e6 < d.w.sum() < 345e6, d.w.sum()
    d["f"] = d.A_AGE.clip(0, 100).map(curve)
    mr = d.MRKS == 1
    key = float((d.w * d.f)[mr].sum())
    per_factor = total_bn * 1e9 / key
    rows = [{"item": "mts_ptc_fy2024_bn", "age": "", "value": round(total_bn, 3),
             "note": "Treasury MTS Table 5, net outlays October 2023 to September 2024"},
            {"item": "ledger_us_resident_population", "age": "", "value": resident,
             "note": "ledger_absolute_2026_09_17 audit.json, the denominator of its per-capita items"},
            {"item": "ptc_per_capita_inside_ledger_R", "age": "", "value": round(total_bn * 1e9 / resident, 2),
             "note": "2024 dollars per person-year at every age, inside R (function 550 net of Medicaid, CHIP)"},
            {"item": "cps_subsidized_marketplace_persons_m", "age": "",
             "value": round(float(d.w[mr].sum()) / 1e6, 4), "note": "CPS ASEC 2025, MRKS = 1"},
            {"item": "ptc_per_unit_age_factor", "age": "", "value": round(per_factor, 2),
             "note": "total / sum(w f(age)) over MRKS = 1"}]
    for a in range(45, 70):
        rows.append({"item": "ptc_per_covered_person", "age": a, "value": round(per_factor * curve[a], 2),
                     "note": "2024 dollars"})
    mx = d[d.PENATVTY == MEXICO]
    nocov = (d.GRP != 1) & (d.MCAID != 1) & (d.MCARE != 1)
    for lo, hi in BANDS:
        band = f"{lo}-{hi - 1}"
        sel = {"mexico_naturalized": mx[(mx.PRCITSHP == 4) & mx.A_AGE.between(lo, hi - 1)],
               "mexico_noncitizen": mx[(mx.PRCITSHP == 5) & mx.A_AGE.between(lo, hi - 1)],
               "all_no_employer_medicaid_medicare": d[nocov & d.A_AGE.between(lo, hi - 1)]}
        for name, s in sel.items():
            rate = float(np.average(s.MRKS == 1, weights=s.w))
            ne = float(s.w.sum() ** 2 / (s.w ** 2).sum())
            rows.append({"item": f"mrks_rate_{name}", "age": band, "value": round(rate, 6),
                         "note": f"n={len(s)}; se={np.sqrt(rate * (1 - rate) / ne):.4f} (Kish, no design)"})
    with (OUT / "ptc_inputs.csv").open("w", newline="") as fh:
        wr = csv.DictWriter(fh, fieldnames=["item", "age", "value", "note"], lineterminator="\n")
        wr.writeheader()
        wr.writerows(rows)
    prov = {"mts": {str(MTS.relative_to(ROOT)): sha256(MTS), "url": MTS_URL},
            "mts_cy2024_crosscheck": {str(MTS_CY.relative_to(ROOT)): sha256(MTS_CY)},
            "ledger_audit": {str(LEDGER_AUDIT.relative_to(ROOT)): sha256(LEDGER_AUDIT)},
            "asec": {str(ASEC.relative_to(ROOT)): sha256(ASEC)},
            "age_curve": {"url": CURVE_URL, "file": str(CURVE.relative_to(HERE)),
                          "sha256_pdf": sha256(CURVE.with_suffix(".pdf"))}}
    (OUT / "ptc_provenance.json").write_text(json.dumps(prov, indent=1, sort_keys=True) + "\n")
    print(pd.DataFrame(rows).to_string())


if __name__ == "__main__":
    main()
