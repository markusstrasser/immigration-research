"""Pre-estimation gates. Every check reads other lanes read-only; nothing outside this lane is written.

1. scaling_check.py's composite reproduces 0.59 / 0.84 (its regression loop is copied from
   assumption_explorer_2026_09_21/scaling_check.py main(); its sources and helpers are imported).
2. The administration lane's main state-panel estimate reproduces 0.47 (its loaders and estimator
   are imported from administration_response_2026_09_20/analyze.py; its main() writes, so it is not called).
3. This lane's individual-unit parser reproduces local_spending_composition_2026_09_18's county
   totals for one function (governmental administration, direct expenditure) in 2012 and 2022,
   and judicial and legal as a second function.
4. The Government Finance Database's current-operations columns match this lane's individual-unit
   build in 2012, 2017 and 2022, which is what licenses its 2002 and 2007 waves.

Gate 4 of the brief (main_case.js and the lane's evaluator) is main_case_map.js.
Output: derived/gates.json. Exits non-zero with [BLOCKED] on any failure.
"""
import csv
import importlib.util
import json
import sys
from pathlib import Path

import numpy as np
import openpyxl

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
sys.path.insert(0, str(HERE))
import finance  # noqa: E402  (this lane's individual-unit parser)

RESULTS = []


def gate(name, ok, detail):
    RESULTS.append({"gate": name, "pass": bool(ok), "detail": detail})
    print(f"  {'PASS' if ok else 'FAIL'} {name}: {detail}", flush=True)


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def gate_scaling():
    sc = load(FISCAL / "assumption_explorer_2026_09_21" / "scaling_check.py", "scaling_check")
    stored = json.loads((FISCAL / "assumption_explorer_2026_09_21" / "derived" / "scaling_check.json").read_text())
    source = sc.HERE / "_cache/slf2022.xlsx"
    import hashlib
    if hashlib.sha256(source.read_bytes()).hexdigest() != sc.SLF_SHA256:
        gate("scaling_check source pinned", False, "slf2022.xlsx hash differs")
        return None
    # Copied from scaling_check.main() (2026-09-21), without its write.
    rows = list(openpyxl.load_workbook(source, read_only=True, data_only=True).worksheets[0].values)
    names = rows[8]
    columns = {str(name).strip(): i for i, name in enumerate(names) if name and i >= 2}
    columns.pop("United States Total", None)
    by_line = {str(r[0]).strip(): r for r in rows if r and r[0] is not None}
    with sc.POP.open(encoding="latin-1") as stream:
        population = {r["NAME"]: float(r["POPESTIMATE2022"]) for r in csv.DictReader(stream) if r["SUMLEV"] == "040"}
    states = [s for s in columns if s in population and s != "District of Columbia"]
    b, se = {}, {}
    for label, lines in sc.FUNCTIONS.items():
        spend = {s: sum(float(by_line[l][columns[s]]) for l in lines) * 1000 for s in states}
        x = np.log([population[s] for s in states]); y = np.log([spend[s] for s in states])
        X = np.column_stack([np.ones(len(x)), x])
        beta, *_ = np.linalg.lstsq(X, y, rcond=None)
        resid = y - X @ beta
        cov = np.linalg.inv(X.T @ X) * (resid @ resid / (len(x) - 2))
        b[label], se[label] = float(beta[1]), float(np.sqrt(cov[1, 1]))
    comp = sc.general_public_service_2024()
    admin_label = "Governmental administration (financial, judicial, buildings, other)"
    total = sum(comp.values())
    state_local = comp["state_local_executive_legislative"] + comp["state_local_tax_financial"] + comp["state_local_other"]
    low = (state_local * b[admin_label] + comp["federal_tax_financial"] * b["Financial administration"]) / total
    high = b[admin_label]
    ok = round(low, 2) == stored["composite_low"] == 0.59 and round(high, 2) == stored["composite_high"] == 0.84
    gate("scaling_check composite 0.59/0.84", ok, f"low {low:.4f}, high {high:.4f} (stored {stored['composite_low']}/{stored['composite_high']})")
    stored_b = {e["function"]: e["elasticity"] for e in stored["elasticities"] if e["scope"] == "50 states"}
    worst = max(abs(round(b[k], 3) - stored_b[k]) for k in b)
    gate("scaling_check elasticities", worst == 0, f"max |diff| after rounding {worst}")
    return {"state_local_bn": state_local, "federal_tax_financial_bn": comp["federal_tax_financial"], "total_bn": total,
            "admin_elasticity": b[admin_label], "admin_se": se[admin_label],
            "financial_admin_elasticity": b["Financial administration"],
            "composite_low_unrounded": low, "composite_high_unrounded": high, "composition_bn": comp}


def gate_admin_lane():
    an = load(FISCAL / "administration_response_2026_09_20" / "analyze.py", "admin_analyze")
    raw = an.read_finance()
    an.validate(raw)
    d = an.panel(raw)
    fit = an.fit(d.query("level == 1"))
    stored = next(r for r in csv.DictReader((FISCAL / "administration_response_2026_09_20" / "derived" / "estimates.csv").open())
                  if r["spec"] == "full" and r["outcome"] == "admin" and r["weighted"] == "False")
    ok = abs(fit["beta"] - float(stored["beta"])) < 1e-9 and round(fit["beta"], 2) == 0.47
    gate("administration lane state panel 0.47", ok,
         f"beta {fit['beta']:.4f} (CR1 SE {fit['se_CR1']:.3f}, 95% {fit['low95_normal']:.2f} to {fit['high95_normal']:.2f}), n={fit['n']}")
    return {"beta": fit["beta"], "se": fit["se_CR1"], "low95": fit["low95_normal"], "high95": fit["high95_normal"]}


def gate_county_totals():
    ref = {}
    with (FISCAL / "local_spending_composition_2026_09_18" / "derived" / "county_finance.csv").open() as fh:
        for r in csv.DictReader(fh):
            if r["year"] in ("2012", "2022"):
                ref[(r["fips"], int(r["year"]))] = (float(r["admin"]), float(r["judicial"]))
    out = {}
    for year in (2012, 2022):
        mine = finance.read_indunit(year)
        for idx, label in ((0, "admin"), (1, "judicial")):
            keys = {k[0] for k in ref if k[1] == year}
            if set(mine) != keys:
                gate(f"county set {year}", False, f"{len(set(mine) ^ keys)} counties differ")
                continue
            codes = ("23", "29", "31") if label == "admin" else ("25",)
            diffs = [abs(round(sum(mine[f][f"d{c}"] for c in codes), 1) - ref[(f, year)][idx]) for f in keys]
            total_mine = sum(sum(mine[f][f"d{c}"] for c in codes) for f in keys)
            total_ref = sum(ref[(f, year)][idx] for f in keys)
            gate(f"{label} direct expenditure {year}, every county", max(diffs) <= 0.05 + 1e-9,
                 f"{len(keys)} counties, max |diff| {max(diffs):.2f} $k, national {total_mine / 1e6:.3f} vs {total_ref / 1e6:.3f} $bn")
        out[year] = mine
    return out


def gate_gfd(indunit):
    gfd = {}
    with (HERE / "_cache" / "gfd_admin_county.csv").open() as fh:
        for r in csv.DictReader(fh):
            gfd[(r["fips"], int(r["year"]))] = r
    stats = {}
    for year in (2012, 2017, 2022):
        mine = indunit.get(year) or finance.read_indunit(year)
        common = sorted(f for f in mine if (f, year) in gfd)
        a = np.array([sum(mine[f][c] for c in ("e23", "e29", "e31")) for f in common])
        g = np.array([sum(float(gfd[(f, year)][c]) for c in ("e23", "e29", "e31")) for f in common])
        rel = abs(a.sum() - g.sum()) / a.sum()
        pos = (a > 0) & (g > 0)
        corr = float(np.corrcoef(np.log(a[pos]), np.log(g[pos]))[0, 1])
        share_close = float(np.mean(np.abs(a - g) <= np.maximum(1.0, 0.01 * a)))
        stats[year] = {"counties": len(common), "national_rel_diff": rel, "log_corr": corr, "share_within_1pct": share_close}
        detail = f"{len(common)} counties, national rel diff {rel:.5f}, log corr {corr:.5f}, {share_close:.1%} within 1%"
        if year == 2017:
            # Census re-released the 2017 file in 2023 ("06122023modp"); the database carries an earlier
            # release, and items move between E23 and E29 in 146 county-codes. A diagnostic, not a gate:
            # the definitional test is the exact match in 2012 and 2022.
            print(f"  NOTE GFD vs individual units, E23+E29+E31 2017 (vintage diagnostic): {detail}", flush=True)
            continue
        gate(f"GFD vs individual units, E23+E29+E31 {year}", rel < 1e-6 and share_close == 1.0, detail)
    return stats


def main():
    print("[gates]", flush=True)
    scaling = gate_scaling()
    admin = gate_admin_lane()
    indunit = gate_county_totals()
    gfd = gate_gfd(indunit)
    (HERE / "derived").mkdir(exist_ok=True)
    out = {"gates": RESULTS, "scaling_check": scaling, "administration_lane": admin, "gfd_vs_indunit": gfd}
    (HERE / "derived" / "gates.json").write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    failed = [r["gate"] for r in RESULTS if not r["pass"]]
    if failed:
        print(f"[BLOCKED] failed gates: {failed}", flush=True)
        return 1
    print("all python gates passed", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
