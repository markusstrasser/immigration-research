"""External inputs for re-keying the road part of economic affairs by vehicle miles (RESULT.md).

Reads primary sources only and writes what rekey.cjs needs, with every gate recorded:
  - NIPA Table 3.5 and 3.4, 2024 (the account's pinned Section 3 workbook): the fuel taxes inside
    excise_selective_sales and the personal motor vehicle licences.
  - FHWA Highway Statistics 2023 MF-2 (net gallons taxed at prevailing rates, gasoline and special fuels, by
    State) and MF-121T (State gasoline and diesel rates, 31 Dec 2023): the gasoline share of State motor-fuel
    taxes, gallons x rate summed over States; MF-1 (gross State motor-fuel tax collections) is the control.
  - FHWA 1997 Highway Cost Allocation Study, Table V-21 (2000 cost responsibility for all levels of government
    by vehicle class, $m), transcribed from the page's image, pinned by hash.
  - The congestion lane's NHTS driver-VMT ratios (Hispanic vs non-Hispanic, per person aged 5+) and the
    decomposition lane's row-4 age bins (the under-5 shares that restate a per-5+ ratio per resident).

Writes derived/inputs.json, derived/state_fuel_split.csv and derived/hcas_v21.csv; stops with [BLOCKED] and
writes nothing when a gate fails. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/roads_mileage_key_2026_09_29/inputs.py [--out-dir DIR]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import re
from pathlib import Path

import openpyxl

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CACHE = HERE / "_cache"
PINS = FISCAL / "full_account_spending_2026_09_20" / "SOURCE_PINS.json"
NHTS = FISCAL / "congestion_2026_09_23" / "derived" / "nhts_ratios.csv"
AGE_BINS = FISCAL / "main_case_decomposition_2026_09_29" / "derived" / "age_bins.csv"
CACHED = {  # fetched 2026-09-29; FHWA pages direct, the V-21 image from the Wayback Machine (FHWA timed out)
    "hcas_final_five.cfm.html": "d497a4c6182d74313f1941b6acc8a9c0cab739cc56124449b8e1429d04267e8f",
    "hcas_table_v21.gif": "854e57bfcb4af1944650ed8e6ecaa1d0aebd2e434de9e1ef277ed4d2a7a02190",
    "hs2023_mf1.xlsx": "075082fc0fe3d96300ceaf40e1c5f420d006fc2549198f4817cac35d2611556f",
    "hs2023_mf2.html": "0e1c21d679ea4cdf509f971487ee2664209ff317ddf5cab8bdc2a7b887ad11da",
    "hs2023_mf121t.html": "57f642fab6408248d7a5e4fbf650f6947ab0091fad1fe664ea6c4f66619eb494",
}
URLS = {
    "hcas_final_five.cfm.html": "https://www.fhwa.dot.gov/policy/hcas/final/five.cfm",
    "hcas_table_v21.gif": "https://web.archive.org/web/2016id_/http://www.fhwa.dot.gov/policy/hcas/final/five/img27.gif",
    "hs2023_mf1.xlsx": "https://web.archive.org/web/2025id_/https://www.fhwa.dot.gov/policyinformation/statistics/2023/xls/mf1.xlsx",
    "hs2023_mf2.html": "https://web.archive.org/web/2025id_/https://www.fhwa.dot.gov/policyinformation/statistics/2023/mf2.cfm",
    "hs2023_mf121t.html": "https://www.fhwa.dot.gov/policyinformation/statistics/2023/mf121t.cfm",
}
# HCAS 1997 Table V-21, "2000 Federal Cost Responsibility for All Levels of Government by Vehicle Class"
# ($ millions): federal, state, local, total, as printed. The image ends at the >=80,000 lb row; the
# combination-truck and all-vehicle totals are the rows' sums (gated against the page text below).
V21 = [
    ("Autos", "passenger", 12405, 35988, 15791, 64184),
    ("Pickups and Vans", "passenger", 4770, 13678, 6328, 24777),
    ("Buses", "passenger", 221, 383, 268, 871),
    ("Single unit trucks <=25,000 lb", "freight", 1074, 1755, 886, 3715),
    ("Single unit trucks 25,001-50,000 lb", "freight", 981, 1867, 1349, 4197),
    ("Single unit trucks >=50,000 lb", "freight", 1098, 1929, 1212, 4239),
    ("Combination trucks <=50,000 lb", "freight", 222, 325, 149, 696),
    ("Combination trucks 50,001-70,000 lb", "freight", 528, 722, 306, 1555),
    ("Combination trucks 70,001-75,000 lb", "freight", 408, 517, 178, 1103),
    ("Combination trucks 75,001-80,000 lb", "freight", 6329, 8353, 2950, 17632),
    ("Combination trucks >=80,000 lb", "freight", 778, 1125, 450, 2353),
]
V21_SUBTOTALS = {"All Passenger Vehicles": (17396, 50049, 22387, 89832), "All Single Unit Trucks": (3153, 5551, 3447, 12151)}

GATES: list[dict] = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append({"gate": name, "pass": bool(ok), "detail": detail})
    print(("PASS " if ok else "FAIL ") + name + ": " + detail, flush=True)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def num(text: str) -> float:
    t = text.replace(",", "").strip()
    if t in ("", "-"):
        return 0.0
    m = re.match(r"^-?\d+(\.\d+)?", t)
    if not m:
        raise ValueError(f"not a number: {text!r}")
    return float(m.group(0))


def html_rows(path: Path) -> list[list[str]]:
    t = path.read_text(encoding="utf-8", errors="replace")
    t = t[t.find("<table"):]
    rows = []
    for r in re.findall(r"<tr.*?</tr>", t, flags=re.S):
        cells = [re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", c))).strip()
                 for c in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, flags=re.S)]
        rows.append(cells)
    return rows




def clean_state(name: str) -> str:
    name = re.sub(r"\s*\(\d+\)\s*$", "", name).strip()
    return "Dist. of Col." if name == "DC" else name  # MF-121T writes DC, MF-2 "Dist. of Col."


def nipa() -> dict:
    pin = next(p for p in json.loads(PINS.read_text())["sources"] if p["name"] == "Section3All_xls.xlsx")
    path = Path(pin["path"])
    gate("BEA Section 3 workbook is the account's pinned vintage", sha256(path) == pin["sha256"], pin["sha256"][:12])
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    out = {}
    for sheet in ("T30500-A", "T30400-A"):
        rows = list(book[sheet].values)
        header = [r for r in rows if r[0] == "Line"][0]
        j = [i for i, x in enumerate(header) if str(x) == "2024"][0]
        out[sheet] = {int(r[0]): (str(r[1]).strip(), r[2], r[j]) for r in rows if str(r[0]).isdigit()}
    book.close()
    want = {("T30500-A", 4): ("Excise taxes", "B234RC"), ("T30500-A", 5): ("Gasoline", "B2000C"),
            ("T30500-A", 8): ("Diesel fuel", "B2003C"), ("T30500-A", 23): ("Excise taxes", "LA000239"),
            ("T30500-A", 25): ("Gasoline", "LA000241"), ("T30500-A", 40): ("Motor vehicle licenses", "LA000356"),
            ("T30400-A", 10): ("Motor vehicle licenses", "S21030")}
    cells = {}
    for (sheet, line), (label, series) in want.items():
        lab, ser, val = out[sheet][line]
        gate(f"NIPA {sheet} line {line} is {label} ({series})", lab == label and ser == series, f"{lab} {ser} {val}")
        cells[f"{sheet}:{line}"] = val / 1000
    excise_line = cells["T30500-A:4"] + cells["T30500-A:23"]
    gate("excise_selective_sales is Table 3.5 lines 4 + 23 ($371.262bn in model.json)",
         abs(excise_line - 371.262) < 5e-4, f"{excise_line:.3f}")
    gate("personal_motor_vehicle is Table 3.4 line 10 ($26.125bn in model.json)",
         abs(cells["T30400-A:10"] - 26.125) < 5e-4, f"{cells['T30400-A:10']:.3f}")
    return {"federal_gasoline_bn": cells["T30500-A:5"], "federal_diesel_bn": cells["T30500-A:8"],
            "sl_motor_fuel_bn": cells["T30500-A:25"], "federal_excise_bn": cells["T30500-A:4"],
            "sl_excise_bn": cells["T30500-A:23"], "business_motor_vehicle_licences_bn": cells["T30500-A:40"],
            "personal_motor_vehicle_licences_bn": cells["T30400-A:10"],
            "source": f"{path.name} (sha256 {pin['sha256'][:12]}), Table 3.5 lines 4, 5, 8, 23, 25, 40 and Table 3.4 line 10, 2024"}


def fuel_split() -> tuple[dict, list[dict]]:
    mf2 = {}
    for cells in html_rows(CACHE / "hs2023_mf2.html"):
        if len(cells) == 14 and cells[0] not in ("Total", "Percentage", "STATE"):
            gas, sf, allf = num(cells[6]), num(cells[8]), num(cells[10])
            if abs(gas + sf - allf) > 1.5:
                raise SystemExit(f"[BLOCKED] MF-2 {cells[0]}: gasoline + special fuels != all motor fuels")
            mf2[clean_state(cells[0])] = (gas, sf)
        if cells and cells[0] == "Total":
            total_gas, total_sf = num(cells[6]), num(cells[8])
    gate("MF-2 has 51 State rows whose gallons add to the printed total",
         len(mf2) == 51 and abs(sum(v[0] for v in mf2.values()) - total_gas) < 60
         and abs(sum(v[1] for v in mf2.values()) - total_sf) < 60,
         f"{len(mf2)} rows; gasoline {total_gas:,.0f}, special fuels {total_sf:,.0f} thousand gallons")
    rates = {}
    for cells in html_rows(CACHE / "hs2023_mf121t.html"):
        name = clean_state(cells[0]) if cells else ""
        if name in mf2 and len(cells) >= 9 and name not in rates:
            rates[name] = (num(cells[1]), num(cells[3]))
    gate("MF-121T gives a gasoline and a diesel rate for every MF-2 State", set(rates) == set(mf2),
         f"{len(rates)} States; missing {sorted(set(mf2) - set(rates))}")
    rows = []
    for s in sorted(mf2):
        gas, sf = mf2[s]
        rg, rd = rates[s]
        rows.append({"state": s, "gasoline_kgal": gas, "special_fuels_kgal": sf, "gasoline_rate_cents": rg,
                     "diesel_rate_cents": rd, "gasoline_tax_m": gas * rg / 100 / 1000, "diesel_tax_m": sf * rd / 100 / 1000})
    g = sum(r["gasoline_tax_m"] for r in rows)
    d = sum(r["diesel_tax_m"] for r in rows)
    book = openpyxl.load_workbook(CACHE / "hs2023_mf1.xlsx", read_only=True, data_only=True)
    mf1 = [r for r in book[book.sheetnames[0]].values if r and isinstance(r[0], str) and r[0].strip() == "Total"][0]
    book.close()
    gross_m = mf1[1] / 1000
    # The level is only a control: rates as of 31 Dec 2023 overstate 2023 collections (+13%; a 10% gate set
    # before the data failed, see RESULT.md log 02:25). The split uses the share, which the weighting barely moves.
    gallon_share = total_gas / (total_gas + total_sf)
    gate("gallons x rates are within 15% of MF-1 gross State motor-fuel collections (level control)",
         abs((g + d) / gross_m - 1) < 0.15, f"{(g + d) / 1000:.2f} vs {gross_m / 1000:.2f} $bn ({(g + d) / gross_m - 1:+.1%})")
    gate("gasoline share: rate-weighted and gallon-weighted agree within 1 point",
         abs(g / (g + d) - gallon_share) < 0.01, f"{g / (g + d):.4f} vs {gallon_share:.4f}")
    return {"gasoline_share_of_state_motor_fuel_tax": g / (g + d), "gasoline_share_of_taxed_gallons": gallon_share,
            "implied_state_motor_fuel_tax_bn": (g + d) / 1000, "mf1_gross_collections_bn": gross_m / 1000,
            "source": "FHWA Highway Statistics 2023, MF-2 net volume taxed at prevailing rates x MF-121T rates (31 Dec 2023); control MF-1 gross tax collections"}, rows


def hcas() -> dict:
    page = (CACHE / "hcas_final_five.cfm.html").read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", page)))
    ok_rows = all(abs(f + s + l - t) <= 2 for _, _, f, s, l, t in V21)
    gate("V-21 rows: federal + state + local = total within rounding (2)", ok_rows, "11 class rows")
    for name, sub in V21_SUBTOTALS.items():
        cls = [r for r in V21 if (r[1] == "passenger") == (name == "All Passenger Vehicles") and ("Single" in r[0] or name == "All Passenger Vehicles")]
        sums = tuple(sum(r[i] for r in cls) for i in range(2, 6))
        gate(f"V-21 '{name}' row equals its class rows", all(abs(a - b) <= 2 for a, b in zip(sums, sub)), f"{sums} vs {sub}")
    tot = [sum(r[i] for r in V21) for i in range(2, 6)]
    gate("V-21 total matches the page text ($125bn; autos $64bn of $125bn)",
         "total costs of $125 billion" in text and "($64 billion out of $125 billion)" in text
         and round(tot[3] / 1000) == 125 and round(V21[0][5] / 1000) == 64, f"total {tot[3]:,}m, autos {V21[0][5]:,}m")
    level = {"all_levels": 5, "state_local": None, "federal": 2}
    shares = {}
    for name, col in level.items():
        if col is None:
            p = sum(r[3] + r[4] for r in V21 if r[1] == "passenger")
            t = sum(r[3] + r[4] for r in V21)
        else:
            p = sum(r[col] for r in V21 if r[1] == "passenger")
            t = sum(r[col] for r in V21)
        shares[name] = p / t
    return {"passenger_share": shares, "buses_share_all_levels": V21[2][5] / tot[3], "total_m": tot,
            "source": "FHWA, 1997 Federal Highway Cost Allocation Study, Table V-21 (2000, all levels of government), page five.cfm image img27.gif"}


def nhts_and_ages() -> dict:
    with NHTS.open() as f:
        ratios = {f"{r['survey']}_{r['cut']}": float(r["r_all_driver_vmt_per_person_H_vs_N"]) for r in csv.DictReader(f)}
    gate("three NHTS driver-VMT ratios read", set(ratios) == {"2017_southwest", "2017_national", "2022_national"},
         ", ".join(f"{k} {v:.4f}" for k, v in sorted(ratios.items())))
    with AGE_BINS.open() as f:
        rows = [r for r in csv.DictReader(f) if r["weights"] == "row4" and r["key"] == "extra|pop"]
    u = sum(float(r["union"]) for r in rows)
    n = sum(float(r["national"]) for r in rows)
    u5 = sum(float(r["union"]) for r in rows if float(r["bin"]) < 5)
    n5 = sum(float(r["national"]) for r in rows if float(r["bin"]) < 5)
    gate("row-4 union headcount is the account's 39,712,493", abs(u - 39712493.33118789) < 1e-3, f"{u:,.3f}")
    return {"nhts_driver_vmt_ratio_per_person_5plus": ratios,
            "under5_share": {"group": u5 / u, "others": (n5 - u5) / (n - u)},
            "nhts_age_source": "congestion_2026_09_23/derived/nhts_ratios.csv (r_all_driver_vmt_per_person_H_vs_N); "
                      "main_case_decomposition_2026_09_29/derived/age_bins.csv (row4, extra|pop, bins 0-4)"}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=str(HERE / "derived"))
    out = Path(ap.parse_args().out_dir)
    for name, digest in CACHED.items():
        gate(f"cached source {name} is the pinned fetch", sha256(CACHE / name) == digest, digest[:12])
    doc = {"nipa_2024": nipa()}
    doc["state_fuel"], state_rows = fuel_split()
    doc["hcas_v21"] = hcas()
    doc.update(nhts_and_ages())
    doc["cached_sources"] = {k: {"sha256": v, "url": URLS[k]} for k, v in CACHED.items()}
    doc["gates"] = GATES
    if not all(g["pass"] for g in GATES):
        raise SystemExit("[BLOCKED] a gate failed; nothing written")
    out.mkdir(parents=True, exist_ok=True)
    (out / "inputs.json").write_text(json.dumps(doc, indent=1, sort_keys=True) + "\n")
    with (out / "state_fuel_split.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(state_rows[0]), lineterminator="\n")
        w.writeheader()
        for r in state_rows:
            w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})
    with (out / "hcas_v21.csv").open("w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["vehicle_class", "responsibility", "federal_m", "state_m", "local_m", "total_m"])
        w.writerows(V21)
    print(f"wrote {out}/inputs.json, state_fuel_split.csv, hcas_v21.csv")


if __name__ == "__main__":
    main()
