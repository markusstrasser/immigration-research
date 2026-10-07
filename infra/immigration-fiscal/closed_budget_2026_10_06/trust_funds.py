#!/usr/bin/env python3
"""How much of each published fiscal gap the account already closes: Social Security's and Part A's shortfall
after their trust funds are depleted.

The published gaps (Auerbach & Gale 2026, CBO's letter of 24 September 2026, Treasury's FY 2025 Financial Report)
pay scheduled Social Security and Medicare Part A benefits after the trust funds run out, from general revenue. The
account values the promises it charges at payable benefits (pension_accrual_2026_09_28), so for the account those two
funds are closed by the benefit cuts current law makes, and only the rest of a gap remains for a general fix. That
rest is the gap less the post-depletion shortfall, averaged over the gap's window as a share of GDP:

    component = mean over the window's years t of x_t,   x_t = the share of GDP current law would leave unpaid in t,

taking the interest rate equal to GDP growth over the window [ASSUMPTION; with interest one point above growth the
later, larger years weigh less; audit.json reports that variant].

Two readings of x_t, one per baseline a gap rests on:
  trustees  2026 OASDI Trustees Report Table IV.B3 (intermediate; OASDI non-interest income less cost, % of GDP;
            printed pp. 67-68) after the combined fund's depletion in 2034 Q3, plus Part A from the 2026 Medicare
            Trustees Report: cost as % of GDP (Table V.B2, p. 188) times the share of cost income does not cover
            (Table III.B7 cost and income rates, p. 65) after HI's depletion in 2033 Q2.
  cbo       CBO's February 2026 long-term data (pub 62044, sheet 1a): Social Security outlays less revenues, % of GDP,
            after the combined fund's exhaustion in 2034 (the year Auerbach & Gale give for their CBO-based
            projections, p. 9). Part A is left at zero: CBO projected HI's exhaustion in 2052 (CBO 2025e as Auerbach &
            Gale cite it, p. 9), so a CBO-based gap carries almost none of it; the Trustees' Part A shortfall over
            2052-2056 is reported as a diagnostic.
The depletion year counts its post-depletion fraction (2034 Q3: 0.375; 2033 Q2: 0.625; CBO's year 0.5)
[ASSUMPTION: depletion at mid-quarter]. Years between tabulated ones are interpolated linearly.

For Treasury's 75-year gap (2026-2100) the component is the Trustees' 75-year open-group unfunded obligations,
which are the present value of exactly this post-depletion shortfall: OASDI 1.5% and HI 0.2% of GDP (2026 reports).

Separate funds (main case v6, 2026-10-07). The two readings above pool OASI and DI, as the account's pension accrual
did through v5. Current law keeps the funds separate, and v6's accrual follows it (pension_tr2026_2026_10_06,
all_2026_inputs_separate_funds): OASI is depleted in the fourth quarter of 2032 and DI's reserves stay positive
through 2100 (2026 OASDI Trustees Report, Table II.A1 and sec. II.D). The unpaid share is then OASI's shortfall after
its depletion, which DI's surplus cannot cover; DI pays in full. So:
  trustees  OASI's balance in Table IV.B3 after 2032 Q4 (0.125 of 2032), plus Part A as above;
  cbo       CBO's Social Security outlays less revenues plus the Trustees' DI balance (OASI's own deficit), after 2032 Q4
            [APPROX: CBO's 2026 workbook has neither the funds' split nor OASI's exhaustion year, so the Trustees' DI
            path and OASI date stand in], Part A at zero as above;
  75-year   OASI's open-group unfunded obligation over the present value of GDP, $30,297bn / $1,978.4tn (Table IV.B8,
            row H, and the note on p. 82), plus HI's 0.2%; the pooled $29,303bn gives 1.48%, published as 1.5%.

Gates (exit with [BLOCKED] before writing): the staged PDFs match their ACQUIRED.md hashes; every parsed OASDI row
satisfies income - cost = balance to rounding; the parsed rows reproduce the reports' payable percentages (OASDI 83%
in 2034, HI 89% in 2033 and 93% in 2100); CBO's sheet has every year 2026-2056. Separate funds: every parsed OASI and
DI row satisfies income - cost = balance, and OASI plus DI is OASDI, to rounding; OASI's income covers the report's
78% of its cost in 2032 to within a point (the table's rounded GDP shares give 78.8%).

Writes derived/trust_funds.json (components by window and reading) and derived/trust_fund_years.csv, and the
separate-funds components to derived/trust_funds_separate.json and derived/trust_fund_years_separate.csv.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/closed_budget_2026_10_06/trust_funds.py
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
from pathlib import Path

import openpyxl

ROOT = Path(__file__).resolve().parents[3]
LANE = Path(__file__).resolve().parent
OUT = LANE / "derived"
STAGE = ROOT / "sources/immigration-fiscal/data/external/stage3"
SSA = STAGE / "ssa/trustees_2026"
CMS = STAGE / "cms/trustees_2026"
CBO = STAGE / "cbo/ltbo_2026"
FILES = {"tr2026.pdf": SSA, "mtr2026.pdf": CMS, "62044-2026-LTBO.xlsx": CBO}
WINDOWS = {"2027-2056": (2027, 2056), "2026-2056": (2026, 2056)}
DEPLETION = {"oasdi_trustees": (2034, 0.375), "hi_trustees": (2033, 0.625), "oasdi_cbo": (2034, 0.5)}
HI_CBO_EXHAUSTION = 2052
PV_75 = {"oasdi": 1.5, "hi": 0.2, "window": "2026-2100",
         "source": "2026 OASDI Trustees Report, Highlights ('the 75-year open-group unfunded obligation for OASDI is "
                   "$29.3 trillion, or 1.5 percent of GDP over the years 2026-2100'); 2026 Medicare Trustees Report, "
                   "Highlights ('the 75-year open-group unfunded obligation for HI is $4.2 trillion, or 0.2 percent of "
                   "GDP')"}
# Separate funds: OASI's depletion (2026 OASDI Trustees Report, Highlights: "the fourth quarter of 2032"; DI's reserves
# "remain positive throughout the 75-year projection period"), and Table IV.B8's open-group unfunded obligations
# ($bn, present value at 1 January 2026) over the present value of GDP for 2026-2100 (p. 82, note 1: $1,978.4tn).
DEPLETION_SEPARATE = {"oasi": (2032, 0.125)}
UNFUNDED_75 = {"oasi": 30297.0, "di": -994.0, "oasdi": 29303.0, "pv_gdp_bn": 1978400.0}
OASI_PAYABLE_2032 = 78        # percent of scheduled benefits upon OASI's depletion (Table II.A1)


def blocked(msg: str) -> None:
    print(f"[BLOCKED] {msg}", file=sys.stderr)
    sys.exit(2)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def num(s: str) -> float:
    return 0.0 if s == "d" else float(s)  # "d": between -0.005 and 0.005


def rows(lines: list[str], ncols: int) -> dict[int, list[float]]:
    pat = re.compile(r"^\s*(\d{4})[ .]+" + r"\s+".join([r"([-+]?\d*\.\d+|[-+]?\d+|d)%?"] * ncols) + r"\s*$")
    got = {}
    for l in lines:
        m = pat.match(l.replace("−", "-"))
        if m:
            got[int(m.group(1))] = [num(v) for v in m.groups()[1:]]
    return got


def interp(table: dict[int, float], years: range) -> dict[int, float]:
    ks = sorted(table)
    out = {}
    for t in years:
        if t in table:
            out[t] = table[t]
            continue
        lo = max(k for k in ks if k < t)
        hi = min(k for k in ks if k > t)
        out[t] = table[lo] + (table[hi] - table[lo]) * (t - lo) / (hi - lo)
    return out


def frac(t: int, key: str, table: dict = DEPLETION) -> float:
    year, f = table[key]
    return 0.0 if t < year else (f if t == year else 1.0)


def main() -> None:
    gates = []
    for name, d in FILES.items():
        m = re.search(rf"\|\s*{re.escape(name)}\s*\|[^|]*\|[^|]*\|\s*sha256:([0-9a-f]{{64}})", (d / "ACQUIRED.md").read_text())
        ok = bool(m) and sha(d / name) == m.group(1)
        gates.append({"gate": f"{name} matches ACQUIRED.md", "pass": ok})
    years = range(2026, 2061)

    # OASDI, Table IV.B3, intermediate: OASI (3), DI (3), OASDI (3) income, cost, balance.
    tr = (SSA / "tr2026.txt").read_text().splitlines()
    i = next(k for k, l in enumerate(tr) if "Table IV.B3.—Annual Income Rates, Cost Rates, and Balances" in l)
    seg = tr[i:i + 140]
    a = next(k for k, l in enumerate(seg) if l.strip().startswith("Intermediate:"))
    b = next(k for k, l in enumerate(seg) if l.strip().startswith("Low-cost:"))
    parsed = rows(seg[a + 1:b], 9)
    oasdi = {y: v[6:9] for y, v in parsed.items()}
    want = list(range(2026, 2036)) + [2040, 2045, 2050, 2055, 2060]
    gates.append({"gate": "OASDI rows parsed for 2026-2035 and every fifth year to 2060",
                  "pass": all(y in oasdi for y in want), "detail": sorted(oasdi)})
    bad = [y for y, (inc, cost, bal) in oasdi.items() if abs(inc - cost - bal) > 0.011]
    gates.append({"gate": "OASDI income - cost = balance to rounding", "pass": not bad, "detail": bad})
    gates.append({"gate": "OASDI payable at depletion (2034) is the report's 83%",
                  "pass": round(100 * oasdi[2034][0] / oasdi[2034][1]) == 83,
                  "detail": oasdi[2034][0] / oasdi[2034][1]})
    # Separate funds: the same rows' OASI and DI columns (their gates go to trust_funds_separate.json only).
    oasi, di = {y: v[0:3] for y, v in parsed.items()}, {y: v[3:6] for y, v in parsed.items()}
    sep_gates = [
        {"gate": "OASI and DI income - cost = balance to rounding",
         "pass": not [y for tab in (oasi, di) for y, (inc, cost, bal) in tab.items() if abs(inc - cost - bal) > 0.011]},
        {"gate": "OASI plus DI is OASDI (income, cost and balance) to rounding",
         "pass": all(abs(oasi[y][j] + di[y][j] - oasdi[y][j]) <= 0.011 for y in oasdi for j in range(3))},
        {"gate": f"OASI's income covers the report's {OASI_PAYABLE_2032}% of its cost in 2032 to within a point",
         "pass": abs(100 * oasi[2032][0] / oasi[2032][1] - OASI_PAYABLE_2032) < 1.0,
         "detail": oasi[2032][0] / oasi[2032][1]}]

    # HI, Medicare Table III.B7 (cost, income rates, % of taxable payroll) and Table V.B2 (Part A, % of GDP).
    mt = (CMS / "mtr2026.txt").read_text().splitlines()
    i = next(k for k, l in enumerate(mt) if "Table III.B7.—HI Cost and Income Rates" in l)
    seg = mt[i:i + 80]
    a = next(k for k, l in enumerate(seg) if l.strip().startswith("Intermediate estimates:"))
    rates = {y: v[:2] for y, v in rows(seg[a + 1:a + 40], 3).items()}
    i = next(k for k, l in enumerate(mt) if "Table V.B2.—HI and SMI Incurred Expenditures as a Percentage" in l)
    seg = mt[i:i + 80]
    a = next(k for k, l in enumerate(seg) if l.strip().startswith("Intermediate estimates:"))
    part_a = {y: v[0] for y, v in rows(seg[a + 1:a + 40], 4).items()}
    for name, tab in (("HI cost and income rates", rates), ("Part A cost as % of GDP", part_a)):
        gates.append({"gate": f"{name} parsed for 2026-2035, every fifth year to 2060 and 2100",
                      "pass": all(y in tab for y in want + [2100]), "detail": sorted(tab)})
    gates.append({"gate": "HI payable in 2033 is the report's 89%",
                  "pass": round(100 * rates[2033][1] / rates[2033][0]) == 89})
    gates.append({"gate": "HI payable in 2100 is the report's 93%",
                  "pass": round(100 * rates[2100][1] / rates[2100][0]) == 93})

    # CBO, sheet 1a: Social Security revenues and outlays, % of GDP.
    ws = openpyxl.load_workbook(CBO / "62044-2026-LTBO.xlsx", read_only=True, data_only=True)["1a. Key Proj, Supp Data"]
    cbo = {}
    for r in ws.iter_rows(values_only=True):
        if isinstance(r[0], (int, float)) and 2026 <= int(r[0]) <= 2056:
            cbo[int(r[0])] = (float(r[1]), float(r[2]))
    gates.append({"gate": "CBO sheet 1a has Social Security revenues and outlays for every year 2026-2056",
                  "pass": sorted(cbo) == list(range(2026, 2057))})

    bad = [g for g in gates + sep_gates if not g["pass"]]
    if bad:
        blocked("; ".join(f"{g['gate']} ({g.get('detail', '')})" for g in bad))

    bal = interp({y: v[2] for y, v in oasdi.items()}, years)
    cr = interp({y: v[0] for y, v in rates.items() if y <= 2060}, years)
    ir = interp({y: v[1] for y, v in rates.items() if y <= 2060}, years)
    ag = interp({y: v for y, v in part_a.items() if y <= 2060}, years)
    x = {}
    for t in range(2026, 2057):
        x[t] = {
            "oasdi_trustees": max(0.0, -bal[t]) * frac(t, "oasdi_trustees"),
            "hi_trustees": ag[t] * max(0.0, (cr[t] - ir[t]) / cr[t]) * frac(t, "hi_trustees"),
            "oasdi_cbo": max(0.0, cbo[t][1] - cbo[t][0]) * frac(t, "oasdi_cbo"),
        }

    def mean(key: str, lo: int, hi: int, rg: float = 0.0) -> float:
        w = {t: (1 / (1 + rg)) ** (t - lo) for t in range(lo, hi + 1)}
        return sum(x[t][key] * w[t] for t in w) / sum(w.values())

    comps = {}
    for wname, (lo, hi) in WINDOWS.items():
        for rg, tag in ((0.0, ""), (0.01, "_r_minus_g_1pt")):
            comps[wname + tag] = {
                "trustees": {"oasdi": mean("oasdi_trustees", lo, hi, rg), "hi": mean("hi_trustees", lo, hi, rg)},
                "cbo": {"oasdi": mean("oasdi_cbo", lo, hi, rg), "hi": 0.0},
            }
            for v in comps[wname + tag].values():
                v["total"] = v["oasdi"] + v["hi"]
    hi_after_2052 = {w: sum(x[t]["hi_trustees"] for t in range(HI_CBO_EXHAUSTION, hi + 1)) / (hi - lo + 1)
                     for w, (lo, hi) in WINDOWS.items()}

    OUT.mkdir(exist_ok=True)
    with open(OUT / "trust_fund_years.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "oasdi_trustees_pct_gdp", "hi_trustees_pct_gdp", "oasdi_cbo_pct_gdp"])
        for t in sorted(x):
            w.writerow([t] + [f"{x[t][k]:.6f}" for k in ("oasdi_trustees", "hi_trustees", "oasdi_cbo")])
    out = {
        "lane": "closed_budget_2026_10_06",
        "note": "Post-depletion shortfall of Social Security (OASDI) and Medicare Part A (HI) as a share of GDP, "
                "averaged over each fiscal-gap window: the part of a gap that pays scheduled benefits the account "
                "values at payable benefits.",
        "windows": comps,
        "pv_75_year": PV_75,
        "diagnostics": {"hi_trustees_from_2052_mean_pct_gdp": hi_after_2052,
                        "depletion": {k: {"year": v[0], "fraction_after": v[1]} for k, v in DEPLETION.items()}},
        "inputs": {str((d / n).relative_to(ROOT)): sha(d / n) for n, d in FILES.items()}
                  | {str((d / t).relative_to(ROOT)): sha(d / t) for d, t in ((SSA, "tr2026.txt"), (CMS, "mtr2026.txt"))},
        "gates": gates,
    }
    (OUT / "trust_funds.json").write_text(json.dumps(out, indent=1) + "\n")
    for wname in WINDOWS:
        c = comps[wname]
        print(f"{wname}: trustees {c['trustees']['oasdi']:.4f} + {c['trustees']['hi']:.4f} = {c['trustees']['total']:.4f}; "
              f"cbo {c['cbo']['total']:.4f} (% of GDP)")

    # Separate funds (main case v6): OASI's shortfall after its depletion; DI pays in full through 2100.
    oasi_bal = interp({y: v[2] for y, v in oasi.items()}, years)
    di_bal = interp({y: v[2] for y, v in di.items()}, years)
    xs = {}
    for t in range(2026, 2057):
        f = frac(t, "oasi", DEPLETION_SEPARATE)
        xs[t] = {"oasi_trustees": max(0.0, -oasi_bal[t]) * f, "hi_trustees": x[t]["hi_trustees"],
                 "oasi_cbo": max(0.0, cbo[t][1] - cbo[t][0] + di_bal[t]) * f}

    def mean_sep(key: str, lo: int, hi: int, rg: float = 0.0) -> float:
        w = {t: (1 / (1 + rg)) ** (t - lo) for t in range(lo, hi + 1)}
        return sum(xs[t][key] * w[t] for t in w) / sum(w.values())

    comps_sep = {}
    for wname, (lo, hi) in WINDOWS.items():
        for rg, tag in ((0.0, ""), (0.01, "_r_minus_g_1pt")):
            comps_sep[wname + tag] = {
                "trustees": {"oasdi": mean_sep("oasi_trustees", lo, hi, rg), "hi": mean_sep("hi_trustees", lo, hi, rg)},
                "cbo": {"oasdi": mean_sep("oasi_cbo", lo, hi, rg), "hi": 0.0},
            }
            for v in comps_sep[wname + tag].values():
                v["total"] = v["oasdi"] + v["hi"]
    pv_sep = {"oasdi": 100 * UNFUNDED_75["oasi"] / UNFUNDED_75["pv_gdp_bn"], "hi": PV_75["hi"], "window": PV_75["window"],
              "pooled_unrounded": 100 * UNFUNDED_75["oasdi"] / UNFUNDED_75["pv_gdp_bn"],
              "source": "2026 OASDI Trustees Report, Table IV.B8 row H (OASI $30,297bn, DI -$994bn, OASDI $29,303bn) "
                        "over the present value of GDP for 2026-2100 ($1,978.4 trillion, p. 82 note 1); HI as above"}
    with open(OUT / "trust_fund_years_separate.csv", "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["year", "oasi_trustees_pct_gdp", "hi_trustees_pct_gdp", "oasi_cbo_pct_gdp"])
        for t in sorted(xs):
            w.writerow([t] + [f"{xs[t][k]:.6f}" for k in ("oasi_trustees", "hi_trustees", "oasi_cbo")])
    out_sep = {
        "lane": "closed_budget_2026_10_06",
        "note": "Post-depletion shortfall under current law's separate funds, as a share of GDP averaged over each "
                "fiscal-gap window: OASI's after its depletion in 2032 Q4 (DI pays in full through 2100; key 'oasdi' "
                "holds the programme's whole shortfall, OASI's), and Medicare Part A's as in trust_funds.json. The part "
                "of a gap that pays scheduled benefits main case v6's accrual values at payable benefits.",
        "windows": comps_sep,
        "pv_75_year": pv_sep,
        "pooled": {"file": "trust_funds.json", "switch_pct_gdp": {
            w: {r: comps_sep[w][r]["total"] - comps[w][r]["total"] for r in ("trustees", "cbo")} for w in comps}},
        "diagnostics": {"depletion": {"oasi": {"year": 2032, "fraction_after": 0.125}, "hi": DEPLETION["hi_trustees"],
                                      "di": "reserves positive through 2100"},
                        "cbo_reading": "CBO's Social Security outlays less revenues plus the Trustees' DI balance, "
                                       "from the Trustees' OASI depletion [APPROX]"},
        "inputs": out["inputs"],
        "gates": gates + sep_gates,
    }
    (OUT / "trust_funds_separate.json").write_text(json.dumps(out_sep, indent=1) + "\n")
    for wname in WINDOWS:
        c = comps_sep[wname]
        print(f"{wname} separate funds: trustees {c['trustees']['oasdi']:.4f} + {c['trustees']['hi']:.4f} = "
              f"{c['trustees']['total']:.4f}; cbo {c['cbo']['total']:.4f} (% of GDP)")


if __name__ == "__main__":
    main()
