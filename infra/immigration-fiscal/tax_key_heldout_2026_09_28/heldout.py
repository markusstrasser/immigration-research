"""Score the September 27 main case's federal income-tax key on IRS data it was not fitted to.

The key is the account's `federal_liability` key: CPS ASEC 2025 federal income tax after nonrefundable and before
refundable credits (FEDTAX_BC, income year 2024; IRS's "income tax after credits") on the civilian universe. The adopted case gives it CBO's 2022 income gradient
(external_benchmarks_2026_09_24, "individual_inc_tax_gross", adopted September 24): each CBO income group's share
of the line is CBO's, and the union's share inside each group is the CPS's. The tax-records stack then scales the
union's amount by a factor per allocation and fill-in method.

The key's implied national distribution of tax over IRS's 19 AGI bins is each CBO group's CPS distribution over
bins, weighted by CBO's group shares. It is scored against IRS SOI Table 1.2, "Income tax after credits", for tax
year 2023, which no step of the key used (SOI has not published tax year 2024; see reads/). The score is the
validation memo's: total variation across the 19 bins, beside the frozen-IRS baseline (tax year 2022's shares).

The dollar translation holds the union's share inside each AGI bin and moves the bin distribution to IRS's:
share' = sum_b IRS_b x theta_b, as the CBO arm does with income groups. CPS AGI stops near $3.1M (top-coding), so
the bins from $1M up are pooled for it. A second translation keeps CBO's group shares as well: it rakes the key's
CBO-group x AGI-bin cells to both margins, holding the union's share inside each cell. ends.cjs puts each change
through the adopted case at every specification.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with xlrd python3 infra/immigration-fiscal/tax_key_heldout_2026_09_28/heldout.py

Writes derived/ (CSV, JSON) and reads/ (the IRS cells quoted); writes nothing if a gate fails.
"""
from __future__ import annotations

import ast
import csv
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
CACHE = HERE / "_cache"
OUT = HERE / "derived"
READS = HERE / "reads"
BENCH = FISCAL / "external_benchmarks_2026_09_24"
sys.path.insert(0, str(BENCH))
sys.dont_write_bytecode = True
import frame as f  # noqa: E402  (the benchmark lane's CPS frame, keys and CBO groups, read-only)
import cbo_arm  # noqa: E402

f.CACHE = CACHE  # the frame loader keeps its parquet cache in this lane, not in the benchmark lane
LOCK = FISCAL / "same_year_tax_2026_09_20/source_lock.json"
VALID = FISCAL / "validation_fiscal_years_2026_09_28"
CASE = FISCAL / "main_case_long_run_2026_09_27"
SECTION1 = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section1All_xls.xlsx"
SECTION1_SHA = "238ba851c9a4932d91a0dedb1b3f2e6c6d37574d154a54267da18b9cb0921a19"
SPEC = "individual_inc_tax=individual_inc_tax_gross|2022"
LINE = "federal_income_tax"
TOP_POOL = 14  # IRS bins 14..18 ($1M and up) are pooled for the translation
ALLOCS = ("personal", "shared")
GATES: list[tuple[str, bool, str]] = []


def gate(name: str, ok: bool, detail: str) -> None:
    GATES.append((name, bool(ok), detail))


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


# ---------------------------------------------------------------- IRS SOI Table 1.2
def irs_table(year: int) -> dict:
    name = f"{year % 100}in12ms.xls"
    p = CACHE / name
    acq = json.loads((CACHE / "acquisition.json").read_text())
    lock = json.loads(LOCK.read_text())
    digest = sha(p)
    t = pd.read_excel(p, header=None)
    title = str(t.iloc[0, 0])
    labels = [str(x).strip() for x in t.iloc[9:28, 0]]
    amounts = t.iloc[9:28, 10].to_numpy(float)
    total = float(t.iloc[8, 10])
    ok = (digest == acq["tables"][name]["sha256"] == lock[name]["sha256"] and f"Tax Year {year}" in title
          and title.startswith("Table 1.2.") and "Income tax after credits" in str(t.iloc[3, 9])
          and str(t.iloc[4, 10]).strip() == "Amount" and str(t.iloc[8, 0]).strip() == "All returns, total"
          and labels[0].startswith("No adjusted gross income") and labels[-1] == "$10,000,000 or more"
          and abs(amounts.sum() - total) <= 1e-7 * total)
    gate(f"irs_{year}_table_1_2_is_the_pinned_file", ok,
         f"{name} sha256 {digest[:12]} (= this lane's fetch and same_year_tax_2026_09_20's lock); 19 AGI rows add to "
         f"the total, {total:,.0f} thousand")
    return {"year": year, "file": name, "title": title, "header": str(t.iloc[3, 9]), "units": str(t.iloc[1, 0]),
            "labels": labels, "returns": t.iloc[9:28, 9].to_numpy(float), "amounts": amounts, "total": total,
            "shares": amounts / amounts.sum(), "sha256": digest}


def edges_from_labels(labels: list[str]) -> np.ndarray:
    """Lower bounds of bins 2..18 from IRS's row labels: '$1 under $5,000', ..., '$10,000,000 or more'."""
    lows = []
    for lab in labels[1:]:
        m = re.match(r"\$([\d,]+) (?:under|or more)", lab)
        if not m:
            raise SystemExit(f"[BLOCKED] unreadable IRS bin label {lab!r}")
        lows.append(int(m.group(1).replace(",", "")))
    if lows[0] != 1:
        raise SystemExit("[BLOCKED] IRS bin 1 does not start at $1")
    return np.array(lows[1:], float)


def band_of(agi: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """IRS bin of each AGI: 0 for no AGI (zero or deficit), else 1 + the number of lower bounds at or below it."""
    return np.where(agi <= 0, 0, np.searchsorted(edges, agi, side="right") + 1)


def tv(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Total variation in percentage points, half the sum of absolute share differences (first axis = bins)."""
    return 50 * np.abs(np.asarray(x) - np.asarray(y)[:, None] if np.ndim(x) == 2 else np.asarray(x) - y).sum(axis=0)


def pool(x: np.ndarray, start: int = TOP_POOL) -> np.ndarray:
    """Bins below `start` and one bin for the rest ($1M and up by default)."""
    return np.concatenate([x[:start], x[start:].sum(axis=0, keepdims=True)])


def gdp(year: int) -> float:
    ws = openpyxl.load_workbook(SECTION1, read_only=True, data_only=True)["T10105-A"]
    rows = list(ws.iter_rows(values_only=True))
    head = next(r for r in rows if r and r[0] == "Line")
    line = next(r for r in rows if r and str(r[0]).strip() == "1")
    if "Gross domestic product" not in str(line[1]):
        raise SystemExit("[BLOCKED] T1.1.5 line 1 is not GDP")
    return float(line[[str(c) for c in head].index(str(year))])


def main() -> int:
    OUT.mkdir(exist_ok=True)
    READS.mkdir(exist_ok=True)
    irs = {y: irs_table(y) for y in (2022, 2023)}
    edges = edges_from_labels(irs[2023]["labels"])
    gate("irs_bins_are_the_same_both_years_and_the_memos", irs[2022]["labels"] == irs[2023]["labels"]
         and np.array_equal(edges, np.array(ast.literal_eval(re.search(r"EDGES = np\.array\((\[.*?\])\)",
                                                                      (VALID / "analysis.py").read_text(), re.S).group(1)), float)),
         f"19 bins, lower bounds {int(edges[0]):,} ... {int(edges[-1]):,}; identical to validation_fiscal_years_2026_09_28's EDGES")

    # The memo's frozen-IRS baseline and its CPS score, from the validation lane's own output.
    vd = pd.read_csv(VALID / "derived/irs_distribution.csv")
    memo = {arm: 0.5 * vd.loc[vd.arm == arm, "error_pp"].abs().sum() for arm in vd.arm.unique()}
    frozen = float(tv(irs[2022]["shares"], irs[2023]["shares"]))
    gate("frozen_irs_baseline_reproduces_the_memo", abs(frozen - memo["frozen_irs_2022"]) < 1e-9
         and round(frozen, 2) == 2.43 and round(memo["frozen_cps_2022"], 2) == 25.20,
         f"IRS 2022 shares against IRS 2023: {frozen:.4f}pp (validation lane {memo['frozen_irs_2022']:.4f}); its frozen "
         f"CPS 2022 arm {memo['frozen_cps_2022']:.4f}pp and same-year CPS 2023 {memo['same_year_cps_2023']:.4f}pp")

    # ------------------------------------------------------------ the CPS key and CBO's gradient
    d = f.load()
    civ, target = f.masks(d)
    W = f.weights(d)
    w = W[:, 0]
    vp = d.FEDTAX_BC.to_numpy(float)
    ids = d.SPM_ID.to_numpy()
    vec = {"personal": vp, "shared": f.unit_equal(vp, ids)}
    m = json.loads(f.MODEL.read_text())
    line = next(x for x in m["receipts"]["lines"] if x["id"] == LINE)
    national = line["national_bn"]
    ref = line["cells"][m["receipts"]["reference"]]
    key_share = {a: (vec[a][target] @ w[target]) / (vec[a][civ] @ w[civ]) for a in ALLOCS}
    gate("key_is_the_accounts_federal_liability", all(ref[a]["key"] == "federal_liability"
                                                      and abs(key_share[a] - ref[a]["target_bn"] / national) < 1e-9
                                                      for a in ALLOCS),
         "union share of FEDTAX_BC over the civilian universe: " + ", ".join(
             f"{a} {key_share[a]:.9f} (model.json {ref[a]['target_bn'] / national:.9f})" for a in ALLOCS))

    g, _ = cbo_arm.groups(d)
    groups = [j for j in f.GROUPS]
    comp = pd.read_csv(BENCH / "derived/cbo_components.csv").query("line == @LINE")
    shares = pd.read_csv(BENCH / "derived/cbo_group_shares.csv").query("spec == @SPEC").set_index("group")
    trans = pd.read_csv(BENCH / "derived/cbo_translation.csv").query("spec == @SPEC and line == @LINE")
    trans = trans.drop_duplicates(["allocation"]).set_index("allocation")
    deltas = json.loads((BENCH / "derived/cbo_deltas.json").read_text())
    cbo = {j: float(shares.loc[j, "cbo_share"]) for j in groups}
    agi = d.AGI.to_numpy(float)
    b = band_of(agi, edges)

    # Each person's key dollars by the AGI bin of the tax unit that owes them: the carrier's own bin (personal) or,
    # under the shared rule, every carrier's bin in the SPM unit, split equally over its members.
    codes, _ = pd.factorize(ids)
    size = np.bincount(codes).astype(float)
    M = {"personal": np.zeros((len(d), 19)), "shared": np.zeros((len(d), 19))}
    for k in range(19):
        x = vp * (b == k)
        M["personal"][:, k] = x
        M["shared"][:, k] = (np.bincount(codes, weights=x) / size)[codes]
    gate("bin_split_adds_to_the_key", all(np.allclose(M[a].sum(axis=1), vec[a], rtol=0, atol=1e-6) for a in ALLOCS),
         "per-person bin amounts add to the key vector under both allocations")

    def aggregates(a: str, bins: np.ndarray) -> dict:
        """Per CBO group: key dollars T (161), by bin Tb (19 x 161) and the union's Ub (19 x 161)."""
        Mb = np.zeros((len(d), 19))
        for k in range(19):
            x = vp * (bins == k)
            Mb[:, k] = x if a == "personal" else (np.bincount(codes, weights=x) / size)[codes]
        out = {}
        for j in groups:
            mj = civ & (g == j)
            mt = mj & target
            out[j] = {"T": vec[a][mj] @ W[mj], "Tb": Mb[mj].T @ W[mj], "Ub": Mb[mt].T @ W[mt]}
        return out

    def distributions(agg: dict) -> dict:
        tot = sum(agg[j]["T"] for j in groups)
        raw_p = sum(agg[j]["Tb"] for j in groups) / tot
        raw_u = sum(agg[j]["Ub"] for j in groups) / tot
        cal_p = sum(cbo[j] * agg[j]["Tb"] / agg[j]["T"] for j in groups if cbo[j] > 0)
        cal_u = sum(cbo[j] * agg[j]["Ub"] / agg[j]["T"] for j in groups if cbo[j] > 0)
        pi = {j: agg[j]["T"] / tot for j in groups}
        theta = {j: np.divide(agg[j]["Ub"].sum(axis=0), agg[j]["T"], out=np.zeros(161), where=agg[j]["T"] != 0)
                 for j in groups}
        return {"raw_p": raw_p, "raw_u": raw_u, "cal_p": cal_p, "cal_u": cal_u, "pi": pi, "theta": theta}

    A = {a: aggregates(a, b) for a in ALLOCS}
    D = {a: distributions(A[a]) for a in ALLOCS}
    rep_ok, rep_detail = True, []
    for a in ALLOCS:
        c = comp[comp.allocation == a].set_index("group")
        dpi = max(abs(D[a]["pi"][j][0] - c.loc[j, "key_share_pi"]) for j in groups)
        dth = max(abs(D[a]["theta"][j][0] - c.loc[j, "target_share_theta"]) for j in groups)
        s_new = D[a]["cal_u"][:, 0].sum()
        ds = abs(s_new - trans.loc[a, "reweighted_share"])
        dd = abs(national * (s_new - key_share[a]) - deltas[SPEC]["receipts"][LINE][a])
        rep_ok &= dpi < 1e-12 and dth < 1e-12 and ds < 1e-12 and dd < 1e-8 and abs(cbo["negative"]) < 1e-15
        rep_detail.append(f"{a}: pi {dpi:.1e}, theta {dth:.1e}, reweighted share {s_new:.9f} ({ds:.1e}), change "
                          f"{national * (s_new - key_share[a]):+.6f}bn ({dd:.1e})")
    gate("cbo_gradient_reproduces_the_adopted_delta", rep_ok and abs(sum(cbo.values()) - 1) < 1e-12,
         "group shares and the union's in-group shares reproduce cbo_components.csv, the reweighted share "
         "cbo_translation.csv and the change cbo_deltas.json feeds the case; " + "; ".join(rep_detail))
    for a in ALLOCS:
        for k in ("raw_p", "cal_p"):
            if not np.allclose(D[a][k].sum(axis=0), 1, atol=1e-12):
                raise SystemExit(f"[BLOCKED] {a} {k} does not add to 1")

    # ------------------------------------------------------------ scores
    I22, I23 = irs[2022]["shares"], irs[2023]["shares"]
    g24, g23 = gdp(2024), gdp(2023)
    growth = g24 / g23
    gate("gdp_growth_from_the_pinned_section_1", sha(SECTION1) == SECTION1_SHA and 1.03 < growth < 1.08,
         f"NIPA T1.1.5 line 1: {g23:,.0f} (2023) -> {g24:,.0f} (2024) $m, growth {growth - 1:.4%}")
    D_defl = distributions(aggregates("personal", band_of(agi / growth, edges)))
    arms = {
        "key_final_calibrated": D["personal"]["cal_p"],
        "key_before_cbo_gradient": D["personal"]["raw_p"],
        "key_final_calibrated_shared_rule": D["shared"]["cal_p"],
        "key_final_calibrated_agi_in_2023_dollars": D_defl["cal_p"],
    }
    score_rows = []
    for name, dist in arms.items():
        for target_year, T in (("2023", I23), ("2022", I22)):
            for bins_name, fn in (("19 bins", lambda x: x), ("15 bins, $1M and up pooled", pool)):
                s = tv(fn(dist), fn(T))
                score_rows.append([name, target_year, bins_name, s[0], f.sdr(s)])
    for bins_name, fn in (("19 bins", lambda x: x), ("15 bins, $1M and up pooled", pool)):
        score_rows.append(["frozen_irs_2022", "2023", bins_name, float(tv(fn(I22), fn(I23))), 0.0])
    score_rows.append(["memo_frozen_cps_2022 (validation lane)", "2023", "19 bins", memo["frozen_cps_2022"], None])
    score_rows.append(["memo_same_year_cps_2023 (validation lane)", "2023", "19 bins", memo["same_year_cps_2023"], None])
    S = {(r[0], r[1], r[2]): r[3] for r in score_rows}
    key19 = S[("key_final_calibrated", "2023", "19 bins")]
    cps_top = float(agi.max())
    empty = [k for k in range(19) if D["personal"]["cal_p"][k, 0] == 0]
    gate("cps_agi_top_coding_leaves_the_top_bins_empty", 2e6 < cps_top < 5e6 and {17, 18} <= set(empty)
         and all(k < 3 or k > 16 for k in empty),
         f"largest CPS AGI ${cps_top:,.0f}; key bins with no tax: {empty}; IRS 2023 puts "
         f"{100 * I23[[k for k in empty if k > 16]].sum():.2f}% of income tax after credits in the empty top bins and "
         f"{100 * I23[[k for k in empty if k < 3]].sum():.4f}% in the empty bottom ones")

    # ------------------------------------------------------------ translation: theta held inside each bin
    def translate(dist: dict, T: np.ndarray, start: int | None) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Change in the union's share when the key's bin distribution becomes T; `start` pools the bins from it up."""
        P, U = dist["cal_p"], dist["cal_u"]
        if start is not None:
            P, U, T = pool(P, start), pool(U, start), pool(T, start)
        theta = np.divide(U, P, out=np.zeros_like(U), where=P > 0)
        # Bins where the key has no tax take a neighbour's union share: the lowest taxed bin's below it and, above
        # the highest, the pooled share from $1M up (the key's top-coded carriers are the nearest to those bins).
        full = np.flatnonzero(P[:, 0] > 0)
        theta[:full[0]] = theta[full[0]]
        if start is None:
            theta[full[-1] + 1:] = pool(dist["cal_u"])[-1] / pool(dist["cal_p"])[-1]
        if full[-1] - full[0] + 1 != len(full):
            raise SystemExit("[BLOCKED] the key has an untaxed bin between taxed ones")
        new = (T[:, None] * theta).sum(axis=0)
        return new - U.sum(axis=0), theta, (T[:, None] - P) * theta

    variants = {}
    trans_rows = []
    for name, T, start in (("irs_2023_pooled_top", I23, TOP_POOL), ("irs_2023_19_bins", I23, None),
                           ("irs_2023_pooled_from_500k", I23, TOP_POOL - 1), ("irs_2022_pooled_top", I22, TOP_POOL)):
        variants[name] = {}
        for a in ALLOCS:
            ds, theta, contrib = translate(D[a], T, start)
            variants[name][a] = ds
            if name == "irs_2023_pooled_top":
                labels = irs[2023]["labels"][:TOP_POOL] + ["$1,000,000 or more (pooled)"]
                P, Tt = pool(D[a]["cal_p"][:, 0]), pool(T)
                for k, lab in enumerate(labels):
                    trans_rows.append([a, k, lab, 100 * P[k], 100 * Tt[k], 100 * (Tt[k] - P[k]), theta[k, 0],
                                       national * contrib[k, 0]])
    # Both margins at once: rake the final key's CBO-group x AGI-bin cells to CBO's group shares and IRS's bin
    # shares, holding the union's share inside each cell. Bin 0 (no AGI, where the key has no tax) joins bin 1 and
    # the bins from $1M up are pooled, so every IRS bin has key cells to take its mass.
    pos = [j for j in groups if cbo[j] > 0]

    def rake_cols(x: np.ndarray) -> np.ndarray:
        p = pool(x)
        return np.concatenate([p[:2].sum(axis=0, keepdims=True), p[2:]])

    def raked_change(a: str, T: np.ndarray) -> tuple[np.ndarray, int, dict]:
        X = np.stack([cbo[j] * rake_cols(A[a][j]["Tb"]) / A[a][j]["T"] for j in pos])  # groups x 14 bins x 161
        V = np.stack([cbo[j] * rake_cols(A[a][j]["Ub"]) / A[a][j]["T"] for j in pos])
        theta = np.divide(V, X, out=np.zeros_like(V), where=X > 0)
        rows = np.array([cbo[j] for j in pos])[:, None]
        cols = rake_cols(T)[:, None]
        R = X.copy()
        after_bin_step = None
        for it in range(20000):
            R *= (cols / R.sum(axis=0))[None]
            if after_bin_step is None:
                after_bin_step = {j: float(R[i].sum(axis=0)[0]) for i, j in enumerate(pos)}
            R *= (rows / R.sum(axis=1))[:, None]
            if max(np.abs(R.sum(axis=0) - cols).max(), np.abs(R.sum(axis=1) - rows).max()) < 1e-12:
                break
        else:
            raise SystemExit(f"[BLOCKED] raking did not converge ({a})")
        return (R * theta).sum(axis=(0, 1)) - V.sum(axis=(0, 1)), it + 1, after_bin_step

    variants["irs_2023_raked_with_cbo_groups"] = {}
    raking = {}
    for a in ALLOCS:
        ds, iters, drift = raked_change(a, I23)
        variants["irs_2023_raked_with_cbo_groups"][a] = ds
        raking[a] = {"iterations": iters, "cbo_group_shares": {j: cbo[j] for j in pos},
                     "group_shares_after_the_bin_step_alone": drift}
    # Diagnostic: the same bin reweighting applied to the key before CBO's gradient, beside CBO's own change
    # (both before the stack factor, national x share change, as cbo_deltas.json reports it).
    raw_check = {}
    for a in ALLOCS:
        ds_raw = translate({"cal_p": D[a]["raw_p"], "cal_u": D[a]["raw_u"]}, I23, TOP_POOL)[0]
        raw_check[a] = {"irs_2023_pooled_top_bn": national * float(ds_raw[0]), "se_bn": f.sdr(national * ds_raw),
                        "cbo_gradient_bn": deltas[SPEC]["receipts"][LINE][a]}
    s_final = {a: float(D[a]["cal_u"][:, 0].sum()) for a in ALLOCS}
    inputs = {"line": LINE, "national_bn": national, "reweighted_share": s_final,
              "share_change": {n: {a: float(v[a][0]) for a in ALLOCS} for n, v in variants.items()}}
    (OUT / "translation_inputs.json").write_text(json.dumps(inputs, indent=1, sort_keys=True) + "\n")
    done = subprocess.run(["node", str(HERE / "ends.cjs"), str(OUT / "translation_inputs.json"),
                           str(OUT / "main_case_translation.json")], capture_output=True, text=True, cwd=ROOT)
    if done.returncode:
        print(done.stdout + done.stderr)
        for p in (OUT / "translation_inputs.json", OUT / "main_case_translation.json"):
            p.unlink(missing_ok=True)
        raise SystemExit(f"[BLOCKED] ends.cjs exited {done.returncode}")
    mc = json.loads((OUT / "main_case_translation.json").read_text())
    summary_case = json.loads((CASE / "derived/summary.json").read_text())
    adopted = summary_case["main_case"]
    fac_ok = all(abs(x["allocations"][a]["final_union_tax_bn"] - x["allocations"][a]["stack_times_reweighted_bn"]) < 1e-6
                 for x in mc["methods"].values() for a in ALLOCS)
    end_ok = all(abs(x["evaluated_union_tax_at_ends_bn"][e]["amount_bn"]
                     - x["allocations"][mc["allocation_at_end"][e]]["final_union_tax_bn"]) < 1e-9
                 and x["evaluated_union_tax_at_ends_bn"][e]["response"] == 1 for x in mc["methods"].values()
                 for e in ("low", "high"))
    gate("case_union_tax_is_stack_factor_times_the_cbo_share", fac_ok and end_ok
         and abs(mc["band"]["low"] - adopted[0]) < 1e-6 and abs(mc["band"]["high"] - adopted[1]) < 1e-6,
         f"per method and allocation, the case's union federal income tax = stack factor x national x CBO-reweighted "
         f"share; the ends charge it at response 1; the band reproduces ${mc['band']['low']:.4f}-"
         f"{mc['band']['high']:.4f}bn")
    lin_ok = True
    for name in variants:
        v = mc["variants"][name]
        for e in ("low", "high"):
            lin_ok &= abs(v["change_at_case_ends_bn"][e] + v["union_tax_change_at_case_ends_bn"][e]) < 1e-9
    gate("engine_change_equals_minus_the_union_tax_change", lin_ok,
         "rerunning the case with the edit moves the cost at specs 48 / 11 by exactly minus the union's tax change")

    # Replicate SEs of the dollar change (point stack factor x national x replicate share change).
    se_rows = []
    for name, v in variants.items():
        for e, a in (("low", "shared"), ("high", "personal")):
            fac = np.mean([x["allocations"][a]["stack_factor"] for x in mc["methods"].values()])
            dollars = -fac * national * v[a]
            se_rows.append([name, e, a, mc["variants"][name]["change_at_case_ends_bn"][e], f.sdr(dollars),
                            mc["variants"][name]["band"]["low"], mc["variants"][name]["band"]["high"],
                            " ".join(mc["variants"][name]["end_specs"])])

    # ------------------------------------------------------------ outputs
    failed = [x for x in GATES if not x[1]]
    for name, ok, detail in GATES:
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: {detail}")
    if failed:
        for p in (OUT / "translation_inputs.json", OUT / "main_case_translation.json"):
            p.unlink(missing_ok=True)
        print(f"[BLOCKED] {len(failed)} gate(s) failed; nothing written")
        return 1

    def write(name: str, header: list[str], rows: list[list]) -> None:
        with (OUT / name).open("w", newline="") as h:
            wtr = csv.writer(h, lineterminator="\n")
            wtr.writerow(header)
            wtr.writerows(rows)

    # Sample records behind each bin's union share: carriers of the key (tax > 0) in the civilian universe.
    carrier = civ & (vp > 0)
    n_all = np.bincount(b[carrier], minlength=19)
    n_union = np.bincount(b[carrier & target], minlength=19)
    bin_rows = []
    for k in range(19):
        bin_rows.append([k, irs[2023]["labels"][k], 100 * I22[k], 100 * I23[k], 100 * D["personal"]["raw_p"][k, 0],
                         100 * D["personal"]["cal_p"][k, 0], 100 * D["shared"]["cal_p"][k, 0],
                         100 * D_defl["cal_p"][k, 0],
                         *(float(np.divide(D[a]["cal_u"][k, 0], D[a]["cal_p"][k, 0])) if D[a]["cal_p"][k, 0] else None
                           for a in ALLOCS), int(n_all[k]), int(n_union[k])])
    write("bins.csv", ["bin", "irs_label", "irs_2022_share_pct", "irs_2023_share_pct", "key_before_cbo_share_pct",
                       "key_final_share_pct", "key_final_shared_rule_share_pct", "key_final_agi_2023_dollars_share_pct",
                       "union_share_in_bin_personal", "union_share_in_bin_shared", "carrier_records",
                       "union_carrier_records"], bin_rows)
    write("scores.csv", ["arm", "irs_target_year", "bins", "total_variation_pp", "replicate_se_pp"], score_rows)
    write("translation_bins.csv", ["allocation", "bin", "label", "key_final_share_pct", "irs_2023_share_pct",
                                   "gap_pp", "union_share_in_bin", "union_tax_change_bn_before_stack_factor"], trans_rows)
    write("main_case_change.csv", ["target", "band_end", "allocation", "cost_change_bn", "replicate_se_bn",
                                   "band_low_bn", "band_high_bn", "end_specs_by_method"], se_rows)
    summary = {
        "lane": "tax_key_heldout_2026_09_28",
        "key": {"line": LINE, "national_bn": national, "cps": "CPS ASEC 2025 (income year 2024), FEDTAX_BC, civilian universe",
                "calibration": f"{SPEC} (external_benchmarks_2026_09_24, adopted 2026-09-24)",
                "share_before_cbo": key_share, "share_after_cbo": s_final,
                "final_union_tax_bn_by_method": {k: {a: x["allocations"][a]["final_union_tax_bn"] for a in ALLOCS}
                                                 for k, x in mc["methods"].items()},
                "stack_factor_by_method": {k: {a: x["allocations"][a]["stack_factor"] for a in ALLOCS}
                                           for k, x in mc["methods"].items()}},
        "held_out_year": {"used": 2023, "why": "SOI has not published tax year 2024 (reads/soi_availability.md); no "
                                               "step of the key used tax year 2023", "irs_total_income_tax_after_credits_thousands":
                          irs[2023]["total"]},
        "scores_pp": {f"{r[0]}|{r[1]}|{r[2]}": {"tv": r[3], "se": r[4]} for r in score_rows},
        "headline": {"key_final_vs_irs_2023_19_bins_pp": key19,
                     "frozen_irs_2022_vs_2023_pp": S[("frozen_irs_2022", "2023", "19 bins")],
                     "key_final_vs_irs_2023_pooled_top_pp": S[("key_final_calibrated", "2023", "15 bins, $1M and up pooled")],
                     "frozen_irs_pooled_top_pp": S[("frozen_irs_2022", "2023", "15 bins, $1M and up pooled")],
                     "key_before_cbo_vs_irs_2023_19_bins_pp": S[("key_before_cbo_gradient", "2023", "19 bins")]},
        "cps_largest_agi": cps_top, "empty_key_bins": empty,
        "gdp_growth_2023_2024": growth,
        "main_case": {"adopted_band_bn": adopted, "variants": mc["variants"]},
        "share_change": inputs["share_change"],
        "raking": raking,
        "bin_reweighting_of_the_key_before_cbo": raw_check,
        "gates_passed": len(GATES),
        "inputs": {rel(p): sha(p) for p in sorted([CACHE / "22in12ms.xls", CACHE / "23in12ms.xls", CACHE / "acquisition.json",
                                                    LOCK, f.CPS_ZIP, f.MODEL, SECTION1,
                                                    BENCH / "derived/cbo_components.csv", BENCH / "derived/cbo_group_shares.csv",
                                                    BENCH / "derived/cbo_translation.csv", BENCH / "derived/cbo_deltas.json",
                                                    BENCH / "frame.py", BENCH / "cbo_arm.py", VALID / "analysis.py",
                                                    VALID / "derived/irs_distribution.csv", CASE / "package.cjs",
                                                    CASE / "derived/summary.json", HERE / "ends.cjs"])},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=1, sort_keys=True) + "\n")
    (OUT / "gates.json").write_text(json.dumps([{"gate": n, "pass": ok, "detail": dt} for n, ok, dt in GATES], indent=1) + "\n")

    # reads/: the IRS cells this lane uses, quoted from the files.
    for y, t in irs.items():
        lines = [f"# IRS SOI Table 1.2, tax year {y}", "",
                 f"File: `_cache/{t['file']}` (https://www.irs.gov/pub/irs-soi/{t['file']}), sha256 `{t['sha256']}`.", "",
                 f"Title cell (A1): \"{' '.join(t['title'].split())}\"", "",
                 f"Units cell (A2): \"{' '.join(t['units'].split())}\"", "",
                 f"Column header (J4): \"{' '.join(t['header'].split())}\"; amount column K.", "",
                 "| Row label (column A) | Returns with income tax after credits (J) | Income tax after credits, $ thousands (K) | Share |",
                 "|---|---:|---:|---:|"]
        for lab, n, amt, s in zip(t["labels"], t["returns"], t["amounts"], t["shares"]):
            lines.append(f"| {lab} | {n:,.0f} | {amt:,.0f} | {100 * s:.4f}% |")
        lines.append(f"| All returns, total (row 9) | | {t['total']:,.0f} | 100% |")
        (READS / f"irs_table_1_2_ty{y}.md").write_text("\n".join(lines) + "\n")
    acq = json.loads((CACHE / "acquisition.json").read_text())
    av = ["# Has SOI published tax year 2024?", "",
          f"Checked {acq['fetched_utc']} (UTC) with a generic user agent; `_cache/acquisition.json` holds the responses.", "",
          "| File | HTTP status | Last-Modified |", "|---|---:|---|"]
    for name, p in sorted(acq["probes"].items()):
        av.append(f"| {p['url']} | {p['status']} | {p['last_modified']} |")
    linked = [y for y in acq["page"]["two_digit_tax_years_linked"] if y < 50]
    av += ["", f"The tables-by-AGI page ({acq['page']['url']}, HTTP {acq['page']['status']}) links files for tax "
           f"years {2000 + min(linked)}-{2000 + max(linked)} (two-digit prefixes {min(linked):02d}-{max(linked):02d}, "
           "plus 85 and 93-99 for 1985 and 1993-1999) and none for 2024.",
           "The preliminary Table 1 name exists for tax year 2022 and not for 2023 or 2024.", "",
           f"The Summer 2026 SOI Bulletin ({acq['bulletin']['url']}, sha256 `{acq['bulletin']['sha256']}`) carries no "
           "preliminary-data article. Its notice reads:", "", f"> {acq['bulletin']['notice']}", "",
           "Tax year 2023 is therefore the latest year SOI has published by AGI, and the held-out year here."]
    (READS / "soi_availability.md").write_text("\n".join(av) + "\n")

    print(f"\nkey vs IRS 2023, 19 bins: {key19:.2f}pp; frozen IRS 2022: {S[('frozen_irs_2022', '2023', '19 bins')]:.2f}pp; "
          f"key before CBO: {S[('key_before_cbo_gradient', '2023', '19 bins')]:.2f}pp")
    for r in se_rows:
        print(f"  {r[0]:22s} {r[1]:4s} ({r[2]}): cost {r[3]:+.3f}bn (SE {r[4]:.3f}); band {r[5]:.2f}-{r[6]:.2f} (ends {r[7]})")
    print(f"{len(GATES)} gates passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
