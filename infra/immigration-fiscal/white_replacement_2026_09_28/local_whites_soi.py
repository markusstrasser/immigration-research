#!/usr/bin/env python3
"""An outside test of the local-whites gap (Part F on the case's income-tax keys) against IRS SOI's state data (the team
lead's request of 2026-10-07). The case's federal key rakes CPS FEDTAX_BC to IRS Table 1.2's national AGI bins and
CBO's income groups (tax_key_heldout_2026_09_28/keys.py), so every state's records take the national cells' factors.
SOI Historic Table 2 gives each state's income tax after credits (A06500, the key's concept) by AGI class for tax year
2023, the key's year. Here California's and Texas's records are raked to their own classes, as a check beside the
central, which stays on the national key (the case's rule). Read-only on this lane's library, the fragility script and
the staged SOI file; writes one file.

Rows (derived/local_whites_soi_<case>.csv, long: case, section, arm, slice, measure, basis, end, value, unit):
  shares  like for like, all residents of each state on the published weights (the raking's frame): SOI's share of the
          state's income tax by AGI class (its two lowest classes pooled to match the key's columns) against the key's
          raked share and the unraked SPM split of FEDTAX_BC; the third-plus whites' raked share, on the key and on arm
          iii; arm i's factor; each state's share of the 50 states' and DC's income tax (SOI's US row less other areas
          and Puerto Rico); the US share at AGI of $1M or more, SOI's state file against the key's (Table 1.2's).
  gaps    the local gap (Part F's regions and their sum) and A1's gap on the central and on each arm, both bases and
          ends, with each region's union and white costs, and each figure's change from the central:
            i    within: inside CA and TX each class's raked dollars are scaled so the state's class shares are SOI's;
                 each state keeps its total, and nothing outside CA and TX moves (the national bins drift);
            ii   within and totals: arm i, then CA's and TX's totals set to their SOI shares and the rest of the
                 country rescaled (the national bins drift further);
            iii  full raking: the key re-raked on three margins, CBO's groups and Table 1.2's pooled bins (the case's
                 two, held exactly) and region x class, with CA's and TX's class dollars at their SOI shares of the
                 national total and the rest of the country taking the remainder of each class.
          Each arm replaces the federal key vector; the union, A1 and Part F's pieces are rebuilt and repriced on it.

Gates (exit 1, nothing written): the setup's (income_tax_parts.py's five and the fragility script's three raking gates);
the SOI file's bytes and sha256; its classes 0-10 numeric and uncollapsed, each row's classes adding to its total, the
US row the sum of the states, DC, Puerto Rico and other areas, and the state file's US share at $1M or more within a
point of the key's; the benchmark frame's civilians are the rough frame's; the key's pooled columns add to it, it sums
to 1 on the published weights and its columns are Table 1.2's (1e-12); arm i keeps each state's and the national total,
arm ii the national total (1e-12); arm iii leaves the rest of the country a positive share of every class, converges,
holds Table 1.2's columns and CBO's groups (1e-12), and gives CA and TX SOI's class shares and totals (1e-10). Controls:
the rebuilt central is the library's state rows (5e-5) and the parts file's A1 gap (5e-5); on arm i the rest-of-US union
piece (no CA or TX records) does not move (1e-6) and California's does (> $0.1bn).
Run from the repository root after income_tax_parts.py --case <case> (--out-dir <dir> writes the file there instead):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -I infra/immigration-fiscal/white_replacement_2026_09_28/local_whites_soi.py --case oct07
"""
from __future__ import annotations

import argparse
import contextlib
import csv
import hashlib
import io
import os
import sys
from pathlib import Path

os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
sys.dont_write_bytecode = True   # read-only imports: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
sys.path.insert(0, str(LANE))
import local_whites_fragility as F  # noqa: E402

W, R, S = F.W, F.R, F.S
DER = F.DER
# IRS SOI Historic Table 2, tax year 2023, all states (https://www.irs.gov/pub/irs-soi/23in55cmcsv.csv, fetched
# 2026-10-07; byte-identical to backtest_admin_totals_2026_09_28's copy of 2026-09-28) [SOURCE]
SOI = R.ROOT / "sources/immigration-fiscal/data/external/stage3/irs_soi/historic_table2/23in55cmcsv.csv"
SOI_BYTES = 757078
SOI_SHA = "d1f7c8901fcefb2c46f5dd14f22715b7c8513794ce7b9ea6a6a947f1c548668f"
FIPS = {"CA": 6, "TX": 48}
# SOI's AGI classes (AGI_STUB) and the key's 14 pooled columns, grouped to match
GROUP_STUBS = [(1, 2), (3,), (4,), (5,), (6,), (7,), (8,), (9,), (10,)]
GROUP_COLS = [(0, 1), (2, 3, 4), (5, 6, 7), (8,), (9,), (10,), (11,), (12,), (13,)]
GROUP_LABEL = ["under $10k (incl. no AGI)", "$10k-25k", "$25k-50k", "$50k-75k", "$75k-100k", "$100k-200k",
               "$200k-500k", "$500k-1M", "$1M or more"]
G = np.zeros((14, len(GROUP_COLS)))
for _g, _c in enumerate(GROUP_COLS):
    G[list(_c), _g] = 1.0
REGIONS = (*F.REGIONS, "sum of CA, TX and rest")
ARMS = {"central": "the national key (the case's rule)",
        "i": "within CA and TX, each state's total kept",
        "ii": "within CA and TX, and their totals at SOI's shares",
        "iii": "full raking with CA's and TX's SOI classes as margins"}
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def stop():
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)


def soi():
    """Each state's (and the 50 states' and DC's) income tax after credits, total and class shares."""
    if not SOI.is_file():
        raise SystemExit(f"[BLOCKED] missing source: {SOI}")
    raw = SOI.read_bytes()
    gate("SOI file: its bytes and sha256 are the pinned ones", len(raw) == SOI_BYTES
         and hashlib.sha256(raw).hexdigest() == SOI_SHA, f"{len(raw)} bytes")
    stop()
    t = pd.read_csv(io.BytesIO(raw), thousands=",", dtype={"STATE": str}, usecols=["STATE", "AGI_STUB", "A06500"])
    x = t.pivot(index="STATE", columns="AGI_STUB", values="A06500")
    gate("SOI: every row has AGI classes 0-10 with numeric income tax after credits (no collapsed class)",
         list(x.columns) == list(range(11)) and pd.api.types.is_numeric_dtype(x.stack()) and not x.isna().any().any())
    stop()
    gate("SOI: each row's ten classes add to its total (exact)",
         float((x[list(range(1, 11))].sum(axis=1) - x[0]).abs().max()) < 0.5)
    gate("SOI: the US row is the sum of the states, DC, Puerto Rico and other areas (exact)",
         all(abs(float(x.drop("US")[k].sum()) - float(x.loc["US", k])) < 0.5 for k in range(11)))
    us50 = x.loc["US"] - x.loc["OA"] - x.loc["PR"]
    out = {}
    for st, r in (("US50", us50), ("CA", x.loc["CA"]), ("TX", x.loc["TX"])):
        out[st] = {"total": float(r[0]), "groups": np.array([float(r[list(s)].sum()) for s in GROUP_STUBS]) / float(r[0])}
    return out


def price_all():
    """The local gap (each region and the sum), each region's union and white costs and A1's gap on the current key."""
    W.UNION_SC = R.scenario("mex")
    a1 = W.scenarios()["A1_third_plus_nh_white"]
    with contextlib.redirect_stdout(io.StringIO()):
        st = {b: W.state_rows(b)[0] for b in W.BASES}
    if W.FAILS:
        raise SystemExit(f"[BLOCKED] the library's state gates: {W.FAILS[:3]}")
    res = {}
    for b in W.BASES:
        for x in st[b]:
            if x["region"] in REGIONS:
                res[(b, x["end"], x["region"], "gap")] = float(x["delta_union_ages_bn"])
                res[(b, x["end"], x["region"], "union cost")] = float(x["cost_union_bn"])
                res[(b, x["end"], x["region"], "white cost at union ages")] = float(x["cost_white_union_ages_bn"])
        for end in W.ENDS:
            res[(b, end, "A1", "gap")] = W.run29(W.UNION_SC, end, b)[0]["cost"] - W.run29(a1, end, b)[0]["cost"]
    return res


def rake3(civ, w0, m14, cols, rows_, pos, gj, reg, tgt):
    """IPF on (CBO group, pooled column, region) cells to the groups' shares, the columns' shares and region x class."""
    tb = np.zeros((len(pos), 14, 3))
    for a, j in enumerate(pos):
        for s in range(3):
            mm = civ & (gj == j) & (reg == s)
            tb[a, :, s] = m14[mm].T @ w0[mm]
    r = tb / tb.sum()
    err, it = np.inf, 0
    for it in range(50000):
        r *= (rows_ / r.sum(axis=(1, 2)))[:, None, None]
        r *= (cols / r.sum(axis=(0, 2)))[None, :, None]
        rc = np.einsum("jcs,cg->sg", r, G)
        r *= np.einsum("sg,cg->cs", np.divide(tgt, rc, out=np.ones_like(tgt), where=rc > 0), G)[None, :, :]
        err = max(np.abs(r.sum(axis=(1, 2)) - rows_).max(), np.abs(r.sum(axis=(0, 2)) - cols).max(),
                  np.abs(np.einsum("jcs,cg->sg", r, G) - tgt).max())
        if err < 1e-13:
            break
    gate("arm iii: the three-margin raking converges (1e-12)", err < 1e-12, f"max margin error {err:.1e} after {it + 1} iterations")
    ratio = np.divide(r, tb, out=np.zeros_like(r), where=tb > 0)
    vcol = np.zeros_like(m14)
    for a, j in enumerate(pos):
        for s in range(3):
            mm = civ & (gj == j) & (reg == s)
            vcol[mm] = m14[mm] * ratio[a, :, s][None, :]
    return vcol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", choices=W.TAX_CASES, required=True)
    ap.add_argument("--out-dir", type=Path, default=LANE / "derived", help="where the file goes (default derived/)")
    args = ap.parse_args()
    case = args.case
    bf, d = F.setup(case)
    rows, _ = F.capture()
    rk = F.raking(bf, d)
    if F.FAILS:
        raise SystemExit(f"[BLOCKED] the fragility script's gates: {F.FAILS}")
    sd = soi()
    TK = W.TK
    civ, _ = bf.masks(d)
    civ = np.asarray(civ)
    gate("the benchmark frame's civilians are the rough frame's", np.array_equal(civ, np.asarray(R.civ)))
    w0 = d.pwwgt0.to_numpy(float) * civ          # the published weights, on which the case builds its key
    _, irs = TK.irs_2023()
    cbo = TK.cbo_shares()
    gj = TK.cbo_groups(d)
    cols = TK._pool14(irs)
    pos = [j for j in cbo if cbo[j] > 0]
    rows_ = np.array([cbo[j] for j in pos])
    v0 = R.K["fit_case"].copy()
    vcol, m14 = rk["vcol"], rk["m14"]
    st = np.asarray(S.st)
    reg = np.where(st == FIPS["CA"], 0, np.where(st == FIPS["TX"], 1, 2))
    gate("the key's pooled raked columns add to it (1e-12 relative)", np.allclose(vcol.sum(axis=1), v0, rtol=1e-12, atol=0))
    tot0 = float(w0 @ v0)
    gate("the key sums to 1 over civilians on the published weights (1e-12)", abs(tot0 - 1) < 1e-12, f"{tot0:.15f}")
    nat = (w0 @ vcol) @ G
    gate("the key's pooled columns are IRS Table 1.2's (1e-12)", np.allclose(w0 @ vcol, cols, rtol=0, atol=1e-12))
    gate("SOI's state file and the key agree on the US share at AGI of $1M or more (within 0.01)",
         abs(sd["US50"]["groups"][-1] - nat[-1] / nat.sum()) < 0.01,
         f"{sd['US50']['groups'][-1]:.4f} vs {nat[-1] / nat.sum():.4f}")
    stop()
    out = []

    def add(section, arm, slc, measure, value, unit, basis="", end=""):
        txt = f"{value:.4f}" if unit == "bn" else f"{value:.6f}"
        out.append({"case": case, "section": section, "arm": arm, "slice": slc, "measure": measure, "basis": basis,
                    "end": end, "value": txt, "unit": unit})

    def cls(vc, m):
        x = (w0[m] @ vc[m]) @ G
        return x / x.sum(), float(x.sum())

    # ---------------------------------------------------------------- the arms' key vectors
    v1 = v0.copy()
    for s, fips in FIPS.items():
        m = civ & (st == fips)
        rak, rtot = cls(vcol, m)
        v1[m] = (vcol[m] * (G @ (sd[s]["groups"] / rak))[None, :]).sum(axis=1)
        gate(f"arm i keeps {s}'s total (1e-12 relative)", abs(float(w0[m] @ v1[m]) - rtot) <= 1e-12 * rtot)
    gate("arm i keeps the national total (1e-12)", abs(float(w0 @ v1) - tot0) <= 1e-12)
    v2 = v1.copy()
    inside = civ & np.isin(st, list(FIPS.values()))
    for s, fips in FIPS.items():
        m = civ & (st == fips)
        v2[m] *= (sd[s]["total"] / sd["US50"]["total"]) * tot0 / float(w0[m] @ v1[m])
    rest = civ & ~inside
    v2[rest] *= (tot0 - float(w0[inside] @ v2[inside])) / float(w0[rest] @ v1[rest])
    gate("arm ii keeps the national total (1e-12)", abs(float(w0 @ v2) - tot0) <= 1e-12)
    tgt = np.zeros((3, len(GROUP_COLS)))
    for i, s in enumerate(FIPS):
        tgt[i] = sd[s]["groups"] * sd[s]["total"] / sd["US50"]["total"]
    tgt[2] = cols @ G - tgt[0] - tgt[1]
    gate("arm iii leaves the rest of the country a positive share of every class", bool((tgt[2] > 0).all()))
    stop()
    vc3 = rake3(civ, w0, m14, cols, rows_, pos, gj, reg, tgt)
    v3 = vc3.sum(axis=1)
    gate("arm iii holds Table 1.2's pooled columns (1e-12)", np.allclose(w0 @ vc3, cols, rtol=0, atol=1e-12))
    gate("arm iii holds CBO's group shares (1e-12)",
         all(abs(float(w0[civ & (gj == j)] @ v3[civ & (gj == j)]) - cbo[j]) < 1e-12 for j in pos))
    for i, (s, fips) in enumerate(FIPS.items()):
        got, tot = cls(vc3, civ & (st == fips))
        gate(f"arm iii gives {s} SOI's class shares and total (1e-10)",
             np.allclose(got, sd[s]["groups"], rtol=0, atol=1e-10) and abs(tot - tgt[i].sum()) < 1e-10)
    stop()

    # ---------------------------------------------------------------- shares, like for like
    for s, fips in FIPS.items():
        m = civ & (st == fips)
        rak, rtot = cls(vcol, m)
        unr, utot = cls(m14, m)
        w3 = m & R.MASK["w3"]
        rak3, _ = cls(vcol, w3)
        arm3, _ = cls(vc3, w3)
        for g, lab in enumerate(GROUP_LABEL):
            slc = f"{s}: AGI {lab}"
            add("shares", "", slc, "SOI share of the state's income tax after credits", sd[s]["groups"][g], "share")
            add("shares", "central", slc, "the key's raked share, all residents", rak[g], "share")
            add("shares", "", slc, "unraked share (SPM split of FEDTAX_BC), all residents", unr[g], "share")
            add("shares", "central", slc, "raked share, third-plus non-Hispanic whites", rak3[g], "share")
            add("shares", "iii", slc, "raked share, third-plus non-Hispanic whites", arm3[g], "share")
            add("shares", "i", slc, "factor on the class's raked dollars", sd[s]["groups"][g] / rak[g], "ratio")
        slc = f"{s}: share of the 50 states' and DC's income tax"
        add("shares", "", slc, "SOI", sd[s]["total"] / sd["US50"]["total"], "share")
        add("shares", "central", slc, "the key, raked", rtot / tot0, "share")
        add("shares", "", slc, "unraked (SPM split of FEDTAX_BC)", utot / float(w0 @ m14.sum(axis=1)), "share")
    slc = "US: AGI $1M or more"
    add("shares", "", slc, "SOI state file, the 50 states and DC", sd["US50"]["groups"][-1], "share")
    add("shares", "central", slc, "the key (IRS Table 1.2)", nat[-1] / nat.sum(), "share")
    add("shares", "", slc, "unraked (SPM split of FEDTAX_BC)", float((w0 @ m14) @ G[:, -1]) / float(w0 @ m14.sum(axis=1)),
        "share")

    # ---------------------------------------------------------------- gaps on each arm
    kt0, u0 = R.KTOT["fit_case"], W.UNION_SC
    res = {}
    try:
        for arm, vec in (("central", v0), ("i", v1), ("ii", v2), ("iii", v3)):
            R.K["fit_case"] = vec
            R.KTOT["fit_case"] = float((R.w * vec).sum())
            res[arm] = price_all()
    finally:
        R.K["fit_case"], R.KTOT["fit_case"], W.UNION_SC = v0, kt0, u0
    c0 = res["central"]
    for (b, end, slc, kind), val in c0.items():
        if kind == "gap" and slc != "A1":
            gate(f"control: the rebuilt central is the library's state rows, {slc} {b} {end} (5e-5)",
                 abs(val - float(rows[(b, end, slc)]["delta_union_ages_bn"])) < 5e-5)
    parts = pd.read_csv(DER / f"income_tax_parts_{case}.csv")
    for b in W.BASES:
        for end in W.ENDS:
            want = float(parts[(parts.basis == b) & (parts.end == end)
                               & (parts.figure == "gap: union less A1_third_plus_nh_white")].central_bn.iloc[0])
            gate(f"control: the rebuilt central A1 gap is the parts file's, {b} {end} (5e-5)",
                 abs(c0[(b, end, "A1", "gap")] - want) < 5e-5, f"{c0[(b, end, 'A1', 'gap')]:.4f}")
    a = res["i"]
    gate("control: on arm i the rest-of-US union piece does not move (1e-6) and California's does (> $0.1bn)",
         all(abs(a[(b, e, "rest of US", "union cost")] - c0[(b, e, "rest of US", "union cost")]) < 1e-6
             for b in W.BASES for e in W.ENDS)
         and abs(a[("accrual", "low", "California", "union cost")] - c0[("accrual", "low", "California", "union cost")]) > 0.1)
    stop()
    for arm, r in res.items():
        for (b, end, slc, kind), val in r.items():
            name = "local gap (California, Texas, rest of US)" if slc == "sum of CA, TX and rest" else (
                "A1 gap (third-plus non-Hispanic whites at their own ages)" if slc == "A1" else slc)
            add("gaps", arm, name, kind, val, "bn", b, end)
            if arm != "central":
                add("gaps", arm, name, f"{kind}: change from the central", val - c0[(b, end, slc, kind)], "bn", b, end)

    path = args.out_dir / f"local_whites_soi_{case}.csv"
    with open(path, "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(out[0]), lineterminator="\n")
        wr.writeheader()
        wr.writerows(out)
    print(f"[written] {path} ({len(out)} rows)")
    show = pd.DataFrame(out)
    show["v"] = show.value.astype(float)
    with pd.option_context("display.width", 250, "display.max_rows", 200, "display.max_columns", 20):
        top = show[(show.section == "shares") & show.slice.str.contains(r"\$1M or more|share of the 50")]
        print(top[["arm", "slice", "measure", "value"]].to_string(index=False))
        g = show[(show.section == "gaps") & (show.basis == "accrual") & (show.measure == "gap")]
        print(g.pivot_table(index=["arm", "end"], columns="slice", values="v", sort=False).round(2).to_string())
    for arm, desc in ARMS.items():
        print(f"  arm {arm}: {desc}")


if __name__ == "__main__":
    main()
