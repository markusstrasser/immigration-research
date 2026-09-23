"""Measure premium tax credits inside BEA Table 3.12 line 25 from Treasury's Monthly Treasury Statement.

Fetches MTS Table 5 (outlays) from the Fiscal Data API for October 2023 to January 2025, sums the
calendar-2024 monthly outlays of the three refundable-credit lines and applies the spending audit's
probe slope (derived/.. spending_credit_keys: -12.02 / -13.22 / -14.43 bn at 100 / 110 / 120 bn).
Run from the repository root:
    uv run --no-project python3 infra/immigration-fiscal/dataset_integrity_2026_09_23/spending_mts_credits.py
"""
import json
import pathlib
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache" / "mts"
OUT = HERE / "derived" / "spending_mts_credits.json"
API = ("https://api.fiscaldata.treasury.gov/services/api/fiscal_service/v1/accounting/mts/mts_table_5"
       "?filter=record_date:gte:2023-10-01,record_date:lte:2025-01-31&page%5Bsize%5D=10000"
       "&page%5Bnumber%5D={page}&fields=record_date,classification_desc,current_month_gross_outly_amt,"
       "current_fytd_gross_outly_amt,current_month_net_outly_amt,parent_id,classification_id")
LINES = {
    "ptc": "Refundable Premium Tax Credits and Cost Sharing Reductions",
    "eitc_refundable": "Payment Where Earned Income Credit Exceeds Liability for Tax",
    "actc": "Payment Where Child Tax Credit Exceeds Liability for Tax",
}
BEA_LINE25_2024 = 228.809  # $bn, T31200 line 25 (W811RC), CY2024
PROBE = [(100.0, -12.02), (110.0, -13.22), (120.0, -14.43)]  # spending_credit_keys.py stdout


def fetch():
    CACHE.mkdir(parents=True, exist_ok=True)
    rows = []
    for page in (1, 2, 3):
        path = CACHE / f"mts_table5_page{page}.json"
        if not path.exists():
            # curl uses the system trust store; Python's bundle rejects this machine's TLS chain
            subprocess.run(["curl", "-sS", "--fail", "--max-time", "60", API.format(page=page), "-o", str(path)],
                           check=True)
        data = json.loads(path.read_text())
        rows += data["data"]
        total = int(data["meta"]["total-count"])
        if len(rows) >= total:
            break
    assert len(rows) == total, (len(rows), total)
    return rows


def main():
    rows = fetch()
    out = {"source": "Treasury Monthly Treasury Statement Table 5 via api.fiscaldata.treasury.gov",
           "bea_line25_cy2024_bn": BEA_LINE25_2024, "lines": {}}
    for key, desc in LINES.items():
        months = {}
        for r in rows:
            if r["classification_desc"] != desc:
                continue
            m = r["record_date"][:7]
            v = r["current_month_net_outly_amt"]
            val = None if v in (None, "null", "") else float(v) / 1e9
            assert m not in months or months[m] == val, (desc, m)
            months[m] = val
        cy = {f"2024-{i:02d}": months.get(f"2024-{i:02d}") for i in range(1, 13)}
        out["lines"][key] = {
            "mts_line": desc,
            "cy2024_bn": round(sum(v for v in cy.values() if v is not None), 3),
            "months_null": [m for m, v in cy.items() if v is None],
        }
    ptc = out["lines"]["ptc"]["cy2024_bn"]
    assert not out["lines"]["ptc"]["months_null"], "PTC month missing"
    # probe is linear in the PTC amount; interpolate on its slope
    slope = (PROBE[-1][1] - PROBE[0][1]) / (PROBE[-1][0] - PROBE[0][0])
    effect = PROBE[0][1] + slope * (ptc - PROBE[0][0])
    out["ptc_effect_on_main_case_bn"] = round(effect, 2)
    out["non_ptc_remainder_bn"] = round(BEA_LINE25_2024 - ptc, 2)
    OUT.write_text(json.dumps(out, indent=1) + "\n")
    for k, v in out["lines"].items():
        print(f"{k:16s} CY2024 {v['cy2024_bn']:8.2f} bn  null months {v['months_null']}")
    print(f"PTC share of BEA line 25: {ptc / BEA_LINE25_2024:.3f}; non-PTC remainder {out['non_ptc_remainder_bn']} bn")
    print(f"re-key effect at MTS PTC: {out['ptc_effect_on_main_case_bn']} bn")


if __name__ == "__main__":
    main()
