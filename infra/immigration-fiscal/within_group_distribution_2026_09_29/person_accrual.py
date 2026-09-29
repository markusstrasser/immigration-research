"""Person-level pension accrual for the September 29 case's household split (the arm `--accrual person` of
households.py; the lead's request of 2026-09-30).

The flat rule spreads each generation's Social Security accrual by its members' OASDI receipts and its Part A accrual
by their HI receipts: one accrual per tax dollar inside a generation. This script gives every union member their own
accrual from the pension lane's person model (pension_accrual_2026_09_28 at PENSION_COMMIT, the commit the adopted
payload pins; its code is imported read-only and nothing is written in that lane), at the lane's central: payable
benefits, entry-age normal attribution, the Trustees' new-issue rates, general mortality, US careers from arrival for
the Mexico-born, the unauthorized credited at Note 151's long-run 10%.
  - Social Security: central_accrual, the member's on-books OASDI tax times Note 2025.7's money's-worth ratio at their
    career earnings level, birth year and family type (the benefit formula's progressivity) times the lane's model
    factor, net of the future income tax on the benefits: times 1 - (the generation's relative benefit-tax rate) x (the
    member's timing share). The generation's own rate is the one the generation account splits the case's accrual by
    (v4_split.cjs: per tax dollar x (1 - the own-rate future share)), so the members of a generation add up to its
    net accrual per tax dollar.
  - Part A: hi_accrual's central (no spouse credit) per person: P(qualify | generation) x PV(Part A from 65 | age,
    sex) / the generation's expected covered years from career start, for members with HI-covered earnings under 65,
    times the on-books share and, for the unauthorized, 10%. hi_accrual computes only totals, so these lines repeat
    its central; the gates below hold them to the lane's published rows.
  - Non-members (NON_MEMBERS): under the account's shared allocation (the low end) each SPM unit's receipts are split
    equally among its members, so a member's OASDI and HI receipts include part of the taxes of non-members in the
    same unit (6% of the first generation's shared OASDI key, 11% of the second's, 22% of the third-plus's). The
    person vectors keep that convention, so every person of the frame with on-books tax gets the model's accrual: a
    non-member at the union's benefit-tax rate and, for Part A, the union's pooled P(qualify) and coverage curve,
    careers from 21 (the rates the case applies to the group's accrual).
The model grid is model_grid's, for the two (rate, mortality) runs the central reads: the central run on every
family, career start, birth year and level, and Note 2025.7's own basis (trust-fund rates) on careers from 21, which
normalizes the factor. It is computed in parallel and cached in _cache/sept29/ under a key of the lane's code.

Gates (exit 1 before anything is written):
  - the pension lane's code in the working tree is PENSION_COMMIT's, and its stage cache exists (frame() would
    otherwise rebuild it inside that lane);
  - the person model reproduces the lane's published central on its own frame: OASDI accrual per tax dollar by
    generation and for the union (summary.json at PENSION_COMMIT, 1e-12 relative), the future benefit-tax shares, the
    union's at its rate and each generation's at its own (1e-12 relative), Part A's P(qualify) and expected covered
    years (1e-12 relative) and its accrual by generation (hi_arms.csv, written to 6 decimals: 1e-6 bn);
  - the payload's ratio_net and Part A accrual (export_lines.cjs's _cache/sept29/lines.json meta): the union's net
    accrual per tax dollar is ratio_net (1e-12 relative) and its Part A is part_a_accrual_bn (1e-6 bn).
Writes _cache/sept29/person_accrual.parquet (one row per person of the frame: PH_SEQ, A_LINENO, the tax bases and the
accruals) and derived/sept29/person_accrual_model.json (inputs, gates, and the members' dispersion the flat rule leaves
out). Run from the
repository root after export_lines.cjs --case sept29 (a few minutes on the first run; the grid is then cached):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/person_accrual.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import hashlib  # noqa: E402
import io  # noqa: E402
import json  # noqa: E402
import os  # noqa: E402
import subprocess  # noqa: E402
from concurrent.futures import ProcessPoolExecutor  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
PENSION_LANE = FISCAL / "pension_accrual_2026_09_28"
PENSION_COMMIT = "9ea1beb"   # main_case_candidate_v4_2026_09_29/package.cjs PENSION_COMMIT, the payload's pin
sys.path.insert(0, str(PENSION_LANE))
import pension_accrual as PA  # noqa: E402  read-only: the person model

L, S, ss = PA.L, PA.S, PA.ss
CACHE = HERE / "_cache/sept29"
OUT = HERE / "derived/sept29"
GENS = ["G1", "G2", "G3plus"]
G_C = (PA.CENTRAL["rate"], PA.CENTRAL["mortality"])   # the central's (discount rate, mortality) run
SCEN = PA.CENTRAL["scenario"]
METHOD = PA.CENTRAL["method"]
LEVELS = ["very_low", "low", "medium", "high"]         # model_grid's order of Note 2025.3's scaled sets
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def rel_diff(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


def pinned(rel: str) -> bytes:
    return subprocess.run(["git", "-C", str(ROOT), "show", f"{PENSION_COMMIT}:{rel}"], check=True,
                          capture_output=True).stdout


# ------------------------------------------------------------------ the model grid (model_grid, two runs)
_W: dict = {}


def _init():
    econ = L.Economy()
    _W.update(econ=econ, prelim=S.scaled_factors().preliminary.to_numpy(), pay=PA.payable_path(econ))


def _cells(task):
    """One family and career start: the central run's per-tax attribution and ratio on every birth year and level,
    and on careers from 21 the base run's ratio (model_grid's loop body, on the central's scenario)."""
    fam, entry = task
    econ, prelim = _W["econ"], _W["prelim"]
    pay = _W["pay"] if SCEN == "payable" else None
    runs = [G_C] + ([PA.BASE] if entry == PA.ENTRIES[0] else [])
    out = {}
    for g in runs:
        k = np.full((len(PA.BIRTHS), len(LEVELS), 121), np.nan)
        mwr = np.full((len(PA.BIRTHS), len(LEVELS)), np.nan)
        for bi, b in enumerate(PA.BIRTHS):
            for li, lev in enumerate(LEVELS):
                w = L.worker(b, L.LEVEL_ADJ[lev], entry, fam, econ, prelim, arm=g[0], population=g[1], payable=pay)
                mwr[bi, li] = w["mwr"]
                k[bi, li] = w["per_tax"][METHOD]
        out[g] = (k, mwr)
    return fam, entry, out


def grid_key() -> str:
    h = hashlib.sha256()
    for f in ("lifetime_model.py", "sources.py", "pension_accrual.py"):
        h.update((PENSION_LANE / f).read_bytes())
    h.update(json.dumps(dict(g=list(map(str, G_C)), base=list(map(str, PA.BASE)), scen=SCEN, method=METHOD,
                             entries=PA.ENTRIES, births=PA.BIRTHS, levels=LEVELS, fams=list(L.FAMILY_SEXES))).encode())
    return h.hexdigest()[:16]


def model_grid() -> dict:
    """model_grid's dictionary for the central's scenario with the two runs model_factor reads; NaN elsewhere, so a
    person outside the computed cells stops model_factor."""
    fams = list(L.FAMILY_SEXES)
    shape = (len(fams), len(PA.ENTRIES), len(PA.BIRTHS), len(LEVELS))
    cache = CACHE / f"pension_grid_{grid_key()}.npz"
    if cache.exists():
        z = np.load(cache)
        k_c, m_c, m_b = z["k_c"], z["m_c"], z["m_b"]
        print(f"  · grid from {cache.name}", flush=True)
    else:
        k_c, m_c, m_b = np.full(shape + (121,), np.nan), np.full(shape, np.nan), np.full(shape, np.nan)
        tasks = [(f, e) for f in fams for e in PA.ENTRIES]
        n = min(8, os.cpu_count() or 1)
        print(f"  · computing the grid: {len(tasks)} tasks on {n} processes", flush=True)
        with ProcessPoolExecutor(max_workers=n, initializer=_init) as ex:
            for fam, entry, out in ex.map(_cells, tasks):
                fi, ei = fams.index(fam), PA.ENTRIES.index(entry)
                k_c[fi, ei], m_c[fi, ei] = out[G_C]
                if PA.BASE in out:
                    m_b[fi, ei] = out[PA.BASE][1]
        CACHE.mkdir(parents=True, exist_ok=True)
        np.savez(cache, k_c=k_c, m_c=m_c, m_b=m_b)
    k = {METHOD: {G_C: k_c, PA.BASE: np.full_like(k_c, np.nan)}}
    return dict(k=k, mwr={G_C: m_c, PA.BASE: m_b}, fams=fams)


# ------------------------------------------------------------------ Part A per person (hi_accrual's central)
def part_a(p: pd.DataFrame, econ, u_long: float) -> tuple[np.ndarray, dict]:
    """hi_accrual's central row (rate, scenario and mortality of CENTRAL, spouse False, the unauthorized at u_long)
    for every person of the frame: a union member at their generation's P(qualify) and coverage curve, as the lane;
    anyone else at the union's pooled ones, careers from 21 (NON_MEMBERS)."""
    w, age, gen = p.w.to_numpy(), p.age.to_numpy(), p.gen.to_numpy()
    union, unauth = p.union.to_numpy(), p.unauth.to_numpy()
    covered = (p.tax_hi > 0).to_numpy()
    medicare = (p.MCARE == 1).to_numpy()
    lawful_old = (age >= 65) & ~unauth
    info, pq = {}, np.zeros(len(p))
    for g in GENS:
        m = (gen == g) & lawful_old
        info[f"p_qualify_{g}"] = float(np.average(medicare[m], weights=w[m]))
        pq[gen == g] = info[f"p_qualify_{g}"]
    info["p_qualify_union"] = float(np.average(medicare[union & lawful_old], weights=w[union & lawful_old]))
    pq[~union] = info["p_qualify_union"]

    def curve(m):
        wt = pd.Series(w[m]).groupby(age[m]).sum()
        num = pd.Series(covered[m] * w[m]).groupby(age[m]).sum()
        return (num / wt).reindex(range(0, 91)).fillna(0.0).to_numpy()

    cov = {g: curve(gen == g) for g in GENS}
    cov["union"] = curve(union)
    start = np.where(p.mexico_born & p.arrival_age.notna(), np.maximum(p.arrival_age.fillna(21), 21), 21).astype(int)
    start[~union] = 21
    n_years = np.array([cov[k][s:65].sum() for k, s in zip(np.where(union, gen, "union"), start)])
    info["expected_covered_years"] = {g: float(cov[g][21:65].sum()) for g in GENS + ["union"]}
    own = PA.part_a_pv(age, p.sex.to_numpy(), econ, PA.CENTRAL["rate"], SCEN, PA.CENTRAL["mortality"])
    base = np.where(covered & (age < 65) & (n_years > 0), pq * own / np.maximum(n_years, 1e-9), 0.0)
    return base * p.onbooks.to_numpy() * np.where(unauth, u_long, 1.0), info


def wpct(x, w, qs):
    o = np.argsort(x, kind="stable")
    c = np.cumsum(w[o]) / w.sum()
    return [float(x[o][min(int(np.searchsorted(c, q)), len(o) - 1)]) for q in qs]


def main():
    print("[pins]", flush=True)
    lane_rel = str(PENSION_LANE.relative_to(ROOT))
    code = [f"{lane_rel}/{f}" for f in ("pension_accrual.py", "lifetime_model.py", "sources.py", "benefit_tax.py")]
    dirty = subprocess.run(["git", "-C", str(ROOT), "diff", "--name-only", PENSION_COMMIT, "--", *code],
                           check=True, capture_output=True, text=True).stdout.split()
    gate(f"the pension lane's code is {PENSION_COMMIT}'s (the payload's pin)", not dirty, ", ".join(dirty) or "no diff")
    key = hashlib.sha256(b"".join(Path(f).read_bytes() for f in (ss.__file__, ss.ext.__file__, PA.ca.__file__)))
    stage = PA.CACHE / f"stage_{key.hexdigest()[:16]}.parquet"
    gate("the pension lane's stage cache exists (frame() reads it and writes nothing)", stage.exists(), stage.name)
    if FAILS:
        raise SystemExit(f"[BLOCKED] {FAILS}")
    lines = json.loads((CACHE / "lines.json").read_text())
    if lines["meta"]["case"] != "main_case_2026_09_29":
        raise SystemExit("[BLOCKED] _cache/sept29/lines.json is not the September 29 case's; run export_lines.cjs --case sept29")
    meta = lines["meta"]["pension_accrual"]
    summ = json.loads(pinned(f"{lane_rel}/derived/summary.json"))
    hi_rows = pd.read_csv(io.BytesIO(pinned(f"{lane_rel}/derived/hi_arms.csv")))
    bt_json = json.loads(pinned(f"{lane_rel}/derived/benefit_tax.json"))
    if summ["central"] != PA.CENTRAL:
        raise SystemExit(f"[BLOCKED] the lane's published central {summ['central']} is not its code's {PA.CENTRAL}")

    print("[frame]", flush=True)
    p = PA.frame()
    econ = L.Economy()
    prelim = S.scaled_factors().preliminary.to_numpy()
    u_long = S.quotes()["note151_eligible_share"]["value"]["end_of_projection"]
    rel = {g: bt_json["results"][bt_json["central_mapping"]]["groups"][g]["relative_rate"][0] for g in GENS + ["union"]}
    bt = PA.benefit_tax_inputs(pd.read_csv(PA.OUT / "case_lines.csv"))   # stops if benefit_tax.json is stale
    gate("relative benefit-tax rates: benefit_tax.json at the pin is the lane's working copy",
         all(bt["relative_rate"][bt["mapping"]][g] == rel[g] for g in rel), f"union {rel['union']:.6f}")

    print("[grid]", flush=True)
    grid = model_grid()
    share = PA.tob_share_path() * (1 + PA.hi_over_oasdi_tob())
    path = PA.BT_CENTRAL["bt_path"]
    tau = PA.tob_timing(econ, prelim, share * PA.obbba_factor() if path == "obbba" else share, runs=[(G_C, SCEN)])

    print("[Social Security]", flush=True)
    q = p[p.tax_oasdi > 0].reset_index(drop=True)     # every person with on-books OASDI tax (NON_MEMBERS)
    fam = ss.family_vector(q, "observed_family")
    acc, tob = PA.central_accrual(q, {SCEN: grid}, u_long, tau, fam)
    w, tax, gen, in_union = q.w.to_numpy(), q.tax_oasdi.to_numpy(), q.gen.to_numpy(), q.union.to_numpy()
    per = summ["oasdi_per_tax_dollar_central_by_generation"]
    own = summ["benefit_tax"]["future_share_by_generation_own_rate"]
    r_g = np.array([rel[g] if u else rel["union"] for g, u in zip(gen, in_union)])
    net = acc * (1 - r_g * tob)
    stats = {}
    for grp in ["union"] + GENS:
        m = in_union if grp == "union" else gen == grp
        got = float((w * acc)[m].sum() / (w * tax)[m].sum())
        gate(f"{grp}: OASDI accrual per tax dollar reproduces the lane's central (1e-12 relative)",
             rel_diff(got, per[grp]) < 1e-12, f"{got:.12f} vs {per[grp]:.12f}")
        timing = float((w * acc * tob)[m].sum() / (w * acc)[m].sum())
        fs = rel[grp] * timing
        want = summ["benefit_tax"]["future_share_group"] if grp == "union" else own[grp]
        gate(f"{grp}: future benefit-tax share at its own rate reproduces the lane's (1e-12 relative)",
             rel_diff(fs, want) < 1e-12, f"{fs:.12f} vs {want:.12f}")
        stats[grp] = dict(per_tax_dollar_gross=got, future_share_own_rate=fs, timing=timing,
                          per_tax_dollar_net=float((w * net)[m].sum() / (w * tax)[m].sum()))
    for g in GENS:
        want = per[g] * (1 - own[g])
        gate(f"{g}: members' net accrual per tax dollar is the generation account's net ratio (1e-12 relative)",
             rel_diff(stats[g]["per_tax_dollar_net"], want) < 1e-12, f"{stats[g]['per_tax_dollar_net']:.12f}")
    ratio_union = per["union"] * (1 - summ["benefit_tax"]["future_share_group"])
    gate("the union's net accrual per tax dollar is the payload's ratio_net (1e-12 relative)",
         rel_diff(ratio_union, meta["ratio_net"]) < 1e-12, f"{ratio_union:.15f} vs {meta['ratio_net']:.15f}")

    print("[Part A]", flush=True)
    part_a_all, info = part_a(p, econ, u_long)
    pinfo = summ["part_a"]
    for g in GENS:
        gate(f"{g}: Part A P(qualify) and expected covered years reproduce the lane's (1e-12 relative)",
             rel_diff(info[f"p_qualify_{g}"], pinfo[f"p_qualify_{g}"]) < 1e-12
             and rel_diff(info["expected_covered_years"][g], pinfo["expected_covered_years"][g]) < 1e-12,
             f"{info[f'p_qualify_{g}']:.6f}, {info['expected_covered_years'][g]:.4f} years")
    c = PA.CENTRAL
    central_hi = hi_rows[(hi_rows.rate == c["rate"]) & (hi_rows.scenario == SCEN) & (hi_rows.mortality == c["mortality"])
                         & (hi_rows.spouse == c["spouse"]) & (hi_rows.unauthorized == c["unauthorized"])].set_index("group")
    wp = p.w.to_numpy()
    part_a_bn = {}
    for grp in ["union"] + GENS:
        m = p.union.to_numpy() if grp == "union" else (p.gen == grp).to_numpy()
        part_a_bn[grp] = float((wp * part_a_all)[m].sum() / 1e9)
        gate(f"{grp}: Part A accrual reproduces hi_arms.csv's central (1e-6 bn, the file's rounding)",
             abs(part_a_bn[grp] - central_hi.loc[grp, "accrual_bn"]) < 1e-6,
             f"{part_a_bn[grp]:.9f} vs {central_hi.loc[grp, 'accrual_bn']:.6f}")
    gate("the union's Part A accrual is the payload's part_a_accrual_bn (1e-6 bn)",
         abs(part_a_bn["union"] - meta["part_a_accrual_bn"]) < 1e-6,
         f"{part_a_bn['union']:.9f} vs {meta['part_a_accrual_bn']:.9f}")
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed, nothing written: {FAILS}")
        sys.exit(1)

    # One row per person of the frame: the Social Security columns are zero without on-books OASDI tax.
    ssc = pd.DataFrame({"PH_SEQ": q.PH_SEQ.to_numpy(), "A_LINENO": q.A_LINENO.to_numpy(), "family": fam,
                        "oasdi_gross": acc, "tob": tob, "benefit_tax_rate": r_g, "oasdi_net": net})
    out = p[["PH_SEQ", "A_LINENO", "union", "gen", "w", "age", "sex", "mexico_born", "unauth", "onbooks", "tax_oasdi",
             "tax_hi"]].merge(ssc, on=["PH_SEQ", "A_LINENO"], how="left", validate="one_to_one")
    for col in ["oasdi_gross", "tob", "benefit_tax_rate", "oasdi_net"]:
        out[col] = out[col].fillna(0.0)
    out["family"] = out.family.fillna("")
    out["unauth"] = out.unauth.astype(bool)
    out["part_a"] = part_a_all
    out["hi_covered"] = (out.tax_hi > 0).to_numpy()

    # The dispersion the flat rule leaves out (the pension lane's frame and weights): members' net accrual per tax
    # dollar by career earnings level (the benefit formula's progressivity), family type, age and, in the first
    # generation, status, tax-weighted; Part A per HI tax dollar by age and by weighted quarter of HI tax.
    level = PA.career_levels(q, PA.CENTRAL["mapping"])
    band = np.select([level < 0.45, level < 1.0, level < 1.6], ["under_0.45", "0.45_1.0", "1.0_1.6"], "1.6_plus")
    age_band = np.select([q.age < 30, q.age < 45, q.age < 65], ["under_30", "30_44", "45_64"], "65_plus")
    status = np.where(q.unauth.to_numpy(), "unauthorized", np.where(gen == "G1", "G1_lawful", "us_born"))
    tw, lawful = w * tax, ~q.unauth.to_numpy()
    formula = {}
    for name, labels in (("career_level_x_awi", band), ("family", fam), ("age", age_band), ("status", status)):
        formula[name] = {}
        for cell in sorted(set(labels[in_union])):
            m = in_union & (labels == cell)
            row = dict(tax_share=float(tw[m].sum() / tw[in_union].sum()),
                       net_per_tax_dollar=float((w * net)[m].sum() / tw[m].sum()))
            if (m & lawful).any():
                row["net_per_tax_dollar_lawful"] = float((w * net)[m & lawful].sum() / tw[m & lawful].sum())
            formula[name][cell] = row
    h = (p.union & (p.tax_hi > 0) & (p.age < 65) & ~p.unauth).to_numpy()
    hw, ht, ha = wp[h], p.tax_hi.to_numpy()[h], part_a_all[h]
    cuts = wpct(ht, hw, [0.25, 0.5, 0.75])
    quarter = np.select([ht <= cuts[0], ht <= cuts[1], ht <= cuts[2]], ["q1", "q2", "q3"], "q4")
    hage = np.select([p.age.to_numpy()[h] < 30, p.age.to_numpy()[h] < 45], ["under_30", "30_44"], "45_64")
    formula["part_a_per_hi_tax_dollar_lawful"] = {
        name: {c: float((hw * ha)[labels == c].sum() / (hw * ht)[labels == c].sum()) for c in sorted(set(labels))}
        for name, labels in (("hi_tax_quarter", quarter), ("age", hage))}
    disp = {}
    for g in GENS:
        m = (out.gen == g).to_numpy() & (out.tax_oasdi > 0).to_numpy()
        r = (out.oasdi_net / out.tax_oasdi).to_numpy()[m]
        wm = out.w.to_numpy()[m]
        un = out.unauth.to_numpy()[m]
        cov = (out.gen == g).to_numpy() & out.hi_covered.to_numpy() & (out.age < 65).to_numpy()
        prt = (out.part_a / out.tax_hi.where(out.tax_hi > 0)).to_numpy()
        disp[g] = dict(
            oasdi_net_per_tax_dollar=dict(mean=float(np.average(r, weights=wm)),
                                          **dict(zip(["p10", "p50", "p90"], wpct(r, wm, [0.1, 0.5, 0.9]))),
                                          unauthorized=float(np.average(r[un], weights=wm[un])) if un.any() else None,
                                          others=float(np.average(r[~un], weights=wm[~un]))),
            part_a_per_hi_tax_dollar=dict(zip(["p10", "p50", "p90"], wpct(prt[cov], out.w.to_numpy()[cov], [0.1, 0.5, 0.9]))),
            part_a_per_covered_worker_usd=float(np.average(out.part_a.to_numpy()[cov], weights=out.w.to_numpy()[cov])),
            unauthorized_tax_share=float((wm * out.tax_oasdi.to_numpy()[m])[un].sum() / (wm * out.tax_oasdi.to_numpy()[m]).sum()))
    CACHE.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    out.to_parquet(CACHE / "person_accrual.parquet", index=False)
    hashes = {f: hashlib.sha256(pinned(f"{lane_rel}/derived/{f}")).hexdigest()
              for f in ("summary.json", "hi_arms.csv", "benefit_tax.json")}
    record = dict(
        pension_lane=lane_rel, pension_commit=PENSION_COMMIT, pension_files_sha256=hashes, stage_cache=stage.name,
        central=PA.CENTRAL, benefit_tax_path=path, unauthorized_credit=u_long, relative_benefit_tax_rate=rel,
        grid_cache=f"pension_grid_{grid_key()}.npz",
        persons=int(len(out)), union_members=int(out.union.sum()),
        members_with_oasdi_tax=int((q.union).sum()), non_members_with_oasdi_tax=int((~q.union).sum()),
        oasdi=stats, part_a_bn=part_a_bn, part_a_inputs=info, payload=dict(ratio_net=meta["ratio_net"],
                                                                            part_a_accrual_bn=meta["part_a_accrual_bn"]),
        dispersion=disp, formula_members=formula, gates_passed=True,
        note=("oasdi.*.per_tax_dollar_net nets each member at their generation's relative rate, as the generation "
              "account splits the accrual; the payload's ratio_net nets the union at the union's rate"))
    (OUT / "person_accrual_model.json").write_text(json.dumps(record, indent=1, sort_keys=True, default=float) + "\n")
    print(f"  ✓ wrote _cache/sept29/person_accrual.parquet ({len(out):,} persons, {int(out.union.sum()):,} members) "
          "and derived/sept29/person_accrual_model.json")


if __name__ == "__main__":
    main()
