"""Read-only reuse of the frozen job-key replay; legal-form and compliance arms.

Native-First: import the existing lane's replay and SUSB workbook; no new CPS reader.
All replay output is redirected into this lane's ignored cache. No upstream writes.
"""
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
import numpy as np
import openpyxl

from population_keys import completion_shares

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
REFINE = FISCAL / "job_capital_key_refine_2026_10_14"


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, allow_nan=False) + "\n")


def se(x):
    return float(np.sqrt(4 / 160 * np.square(x[1:] - x[0]).sum()))


def replay():
    mod = load_module("pass_job_core", REFINE / "core.py")
    # core.main's paths are globals; its source lane and all source pins stay fixed.
    mod.HERE = HERE / "_cache/key_replay"
    mod.CACHE = mod.HERE / "_cache"
    mod.DERIVED = mod.HERE / "derived"
    (mod.HERE / "inputs").mkdir(parents=True, exist_ok=True)
    mod.CACHE.mkdir(exist_ok=True)
    mod.DERIVED.mkdir(exist_ok=True)
    assert mod.main() == 0
    core = json.loads((mod.DERIVED / "core.json").read_text())
    assert all(g["passed"] for g in core["gates"])
    z = dict(np.load(mod.CACHE / "core.npz"))
    return z, core


def legal_profiles():
    path = REFINE / "_cache/k1_susb_2022.xlsx"
    pin = json.loads((REFINE / "inputs/k1_pins.json").read_text())["susb_2022.xlsx"]
    assert hashlib.sha256(path.read_bytes()).hexdigest() == pin["sha256"]
    wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
    rows = {(r[3], r[2].split(":")[0], r[5].split(":")[0]): r
            for r in wb["LFO"].values if r[0] == "00"}
    wb.close()
    bins = [["1"], ["2", "3"], ["4", "6"], ["7"], ["9"]]
    output, profiles = [], {}
    # SUSB 2 = C/other corporation, 3 = S, 4 = partnership, 5 = sole proprietor.
    for sec in sorted({r[0] for r in rows} - {"99"}):
        profiles[sec] = {}
        for form in ["2", "3", "4", "5"]:
            total_row = rows.get((sec, form, "1"))
            if total_row is None:
                profiles[sec][form] = None
                continue
            total_prop = total_row[10] / rows[sec, "1", "1"][10]
            profile = []
            for label, codes in zip(["total", "under10", "10-99", "100-499", "500plus"], bins):
                published = all((sec, form, b) in rows for b in codes)
                prop = (sum(rows[sec, form, b][10] for b in codes)
                        / sum(rows[sec, "1", b][10] for b in codes)) if published else total_prop
                assert 0 <= prop <= 1
                profile.append(prop)
                output.append(dict(sector=sec, form=form, size=label, probability=prop,
                                   rule="published" if published else "[DEGRADED] all-size form share; missing size cells"))
            profiles[sec][form] = np.array(profile)
    return profiles, output, pin


def aggregate_bins(array):
    return np.stack([array[:, 0], array[:, 1], array[:, 2:4].sum(axis=1),
                     array[:, 4], array[:, 5:7].sum(axis=1)], axis=1)


def calculate(z, core, profiles):
    source = load_module("pass_job_source", FISCAL / "job_capital_taxes_2026_10_14/job_capital.py")
    k1 = load_module("pass_legal_source", REFINE / "k1_legal.py")
    cells = z["cells"].astype(str)
    sector = [k1.SECTOR_CODE.get(source.SECTOR[c]) for c in cells]
    national = aggregate_bins(z["size_wages_national"])
    groups = ["G1", "G2", "G3plus", "white", "union"]
    wages = {g: aggregate_bins(z[f"size_wages_{g}"]) for g in groups}
    wages["national"] = national
    item = json.loads((FISCAL / "job_capital_taxes_2026_10_14/derived/item.json").read_text())
    cw = item["case_wage_key"]["shares"] if "case_wage_key" in item else json.loads(
        (FISCAL / "job_capital_taxes_2026_10_14/derived/case_keys.json").read_text())["case_wage_key"]["shares"]
    # Same factor as the source's case_wage_key arm, applied separately by generation.
    compliance = {}
    for g in ["G1", "G2", "G3plus"]:
        plain = z[f"size_wages_{g}"][:, :, 0].sum() / z["size_wages_national"][:, :, 0].sum()
        compliance[g] = cw[g]["personal"] / plain
    compliance["white"] = 1.0
    # The union cannot take one compliance scalar: composition varies by sector/size.
    onbook = {g: wages[g] * compliance[g] for g in compliance}
    onbook["union"] = sum(onbook[g] for g in ["G1", "G2", "G3plus"])
    out, sufficient = {}, {}
    for sec in sorted(set(sector) - {None}):
        idx = np.array([i for i, s in enumerate(sector) if s == sec])
        out[sec], sufficient[sec] = {}, {}
        for form in ["3", "4", "5"]:
            prop = profiles[sec][form]
            if prop is None:
                out[sec][form] = None
                continue
            # Exclude crop/animal and rail where SUSB has no matching scope.
            supported = np.array([cells[i] not in ["111CA", "482"] for i in idx])
            used = idx[supported]
            den = (national[used] * prop[None, :, None]).sum(axis=(0, 1))
            shares = {}
            for g in groups:
                num = (wages[g][used] * prop[None, :, None]).sum(axis=(0, 1))
                shares[g] = np.divide(num, den, out=np.zeros(161), where=den > 0)
            shares["lineage"] = shares["union"] + sum(core["lineage_rates"][g] * shares[g]
                                                       for g in ["G3plus", "white"])
            out[sec][form] = {g: v.tolist() for g, v in shares.items()}
            sufficient[sec][form] = (den, shares)
    pooled = {"61+81": {}}
    for form in ["3", "4", "5"]:
        den = sum(sufficient[sec][form][0] for sec in ["61", "81"])
        pooled["61+81"][form] = {g: np.divide(sum(sufficient[sec][form][0] *
            sufficient[sec][form][1][g] for sec in ["61", "81"]), den,
            out=np.zeros(161), where=den > 0).tolist() for g in groups + ["lineage"]}
    # W09: exact K1 thin-cell algorithm; only corporate tax, mining still zero.
    pools = [np.fromstring(p, sep=",", dtype=int) for p in z["cell_pool"]]
    covered = np.array([s is not None and c not in ["111CA", "482"] for c, s in zip(cells, sector)])
    prop = np.array([profiles[s]["2"] if ok else np.ones(5) for s, ok in zip(sector, covered)])
    corporate = {}
    for g in groups:
        adjusted = np.zeros_like(z[f"shares_{g}"])
        for i, idx in enumerate(pools):
            den_all = national[idx].sum(axis=(0, 1))
            raw = np.divide(wages[g][idx].sum(axis=(0, 1)), den_all,
                            out=np.zeros(161), where=den_all > 0)
            numerator = (onbook[g][idx] * prop[idx, :, None]).sum(axis=(0, 1))
            denominator = (national[idx] * prop[idx, :, None]).sum(axis=(0, 1))
            legal = np.divide(numerator, denominator, out=np.zeros(161), where=denominator > 0)
            factor = np.divide(legal, raw, out=np.ones(161), where=raw > 0)
            adjusted[i] = z[f"shares_{g}"][i] * factor
        old = z["tax_corporate_ex_foreign"] @ z[f"shares_{g}"]
        new = z["tax_corporate_ex_foreign"] @ adjusted
        corporate[g] = dict(before_bn=old.tolist(), after_bn=new.tolist(), ratio=float(new[0] / old[0]))
    corporate["lineage"] = {}
    for field in ["before_bn", "after_bn"]:
        corporate["lineage"][field] = (np.array(corporate["union"][field]) + sum(
            core["lineage_rates"][g] * np.array(corporate[g][field]) for g in ["G3plus", "white"])).tolist()
    completion = completion_shares(z, core, profiles, source, k1.SECTOR_CODE)
    return dict(shares=out, pooled_shares=pooled, completion=completion, corporate=corporate, compliance=compliance,
                lineage_rates=core["lineage_rates"], source_core_gates=core["gates"],
                scope="sector x enterprise-size conditional legal-form payroll proxy, TY2022 form mix transported to income-year2024; agricultural production/rail scope not observed; no nonemployer identification")


def main():
    z, core = replay()
    profiles, rows, pin = legal_profiles()
    out = calculate(z, core, profiles)
    out["susb_source"] = pin
    dump(HERE / "derived/job_keys.json", out)
    dump(HERE / "derived/legal_profiles.json", rows)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
