"""The case's income-tax keys person by person on the CPS ASEC 2025 frame: one definition for every lane that puts the
survey's income tax on the case's keys.

v4 item 3 (heldout.py, `irs_2023_raked_with_cbo_groups`) keys receipts|federal_income_tax by FEDTAX_BC (income tax
after nonrefundable and before refundable credits) in CBO income group x IRS AGI bin cells, raked to CBO's 2022 group
shares and IRS's TY2023 bin shares. The case keys state_local_income_tax and other_personal_tax by STATETAX_A floored at
0 (state_liability). heldout.py works with the union's share inside each cell; this module gives every person's:
`raked_vector` the federal share, `state_base` the state key's dollars, each on the record (personal) or split equally
over the SPM unit (shared).

`case_keys` builds both on the benchmark lane's frame (external_benchmarks_2026_09_24/frame.py and its cached parquet,
loaded under its own name), reporting its gates through the caller's gate(label, ok, detail): IRS's bin shares are
heldout's bins.csv (1e-12); at each allocation the union's raked share is heldout's translation and the federal vector
sums to 1 over civilians on pwwgt0 (1e-12); the union's unraked federal and state shares are model.json's
federal_liability and state_liability cells (1e-9). `person_keys` runs it with gates that stop the run, keyed by
PH_SEQ and PPPOS for frames in another row order. `national_lines` gives model.json's lines the keys share out.

Moved on 2026-10-07 from white_replacement_2026_09_28/rekey_sept29.py (round 2, cc793ccf), so that the white library
and the ledger's item T (ledger_absolute_2026_09_17) load one definition; test_keys.py checks it. Other lanes have a
module named keys.py (generation_account_2026_09_24, late_arrival_account_line_2026_09_27), so callers load this one
by path under its own name, never through sys.path.
"""
from __future__ import annotations

import importlib.util
import json
import re
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
BENCH = FISCAL / "external_benchmarks_2026_09_24"
CBO_SPEC = "individual_inc_tax=individual_inc_tax_gross|2022"    # the CBO margin heldout.py rakes to
# the frame's columns the keys, the benchmark lane's masks and its CBO income read
TAX_COLS = ["PH_SEQ", "TAX_ID", "SPM_ID", "MARSUPWT", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY",
            "PRDTHSP", "pwwgt0", "AGI", "FEDTAX_BC", "FEDTAX_AC", "STATETAX_A", "WSAL_VAL", "PTOTVAL", "SSI_VAL", "PAW_VAL",
            "CAP_VAL", "MCARE"]
ALLOCATIONS = ("personal", "shared")
LINES = ("federal_income_tax", "state_local_income_tax", "other_personal_tax")
_BF = None


def benchmark_frame():
    """The benchmark lane's frame module, loaded once under its own name (as cbo_arm.groups builds the CBO groups)."""
    global _BF
    if _BF is None:
        spec = importlib.util.spec_from_file_location("benchmark_frame", BENCH / "frame.py")
        _BF = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(_BF)
    return _BF


def load_frame(columns=TAX_COLS):
    """The benchmark lane's cached CPS ASEC 2025 person frame, in its own row order."""
    path = benchmark_frame().CACHE / "cps25_frame.parquet"
    if not path.exists():
        raise SystemExit(f"[BLOCKED] missing {path} (external_benchmarks_2026_09_24 frame.load() builds it)")
    return pd.read_parquet(path, columns=columns)


def irs_2023():
    """IRS SOI TY2023 Table 1.2, income tax after credits by its 19 AGI bins, from this lane's read of the table
    (reads/irs_table_1_2_ty2023.md): bin labels and shares."""
    txt = (HERE / "reads/irs_table_1_2_ty2023.md").read_text()
    rows = re.findall(r"^\| ([^|]+?) \| ([\d,]+) \| ([\d,]+) \| [\d.]+% \|$", txt, re.M)
    total = float(re.search(r"All returns, total \(row 9\) \| \| ([\d,]+) \|", txt).group(1).replace(",", ""))
    amounts = np.array([float(r[2].replace(",", "")) for r in rows])
    if len(rows) != 19 or abs(amounts.sum() - total) > 1e-7 * total:
        raise SystemExit("[BLOCKED] the IRS TY2023 read does not give 19 bins adding to its total")
    return [r[0] for r in rows], amounts / amounts.sum()


def _pool14(x):
    """heldout.py's 14 raking columns from 19 bins: no AGI with $1-5k, the bins to $1M, $1M and up pooled."""
    p = np.concatenate([x[:14], x[14:].sum(axis=0, keepdims=True)])
    return np.concatenate([p[:2].sum(axis=0, keepdims=True), p[2:]])


def bin_edges(labels):
    """The 18 edges between IRS's 19 AGI bins (bin 0: no AGI or a loss) and the bins' lower bounds from $1."""
    lows = [int(re.match(r"\$([\d,]+) (?:under|or more)", lab).group(1).replace(",", "")) for lab in labels[1:]]
    return np.array(lows[1:], float), lows


def bin_dollars(d, dollars, alloc, edges):
    """Each person's key dollars by AGI bin (n x 19), the bin being the record's own AGI's: on the record, or each SPM
    unit's dollars in each bin split equally over its members."""
    agi = d.AGI.to_numpy(float)
    b = np.where(agi <= 0, 0, np.searchsorted(edges, agi, side="right") + 1)
    codes, _ = pd.factorize(d.SPM_ID.to_numpy())
    size = np.bincount(codes).astype(float)
    m = np.zeros((len(d), 19))
    for k in range(19):
        x = dollars * (b == k)
        m[:, k] = x if alloc == "personal" else (np.bincount(codes, weights=x) / size)[codes]
    return m


def raked_vector(d, w, civ, g, alloc, cbo, cols, edges):
    """Each person's share of national federal income tax under v4 item 3's key (irs_2023_raked_with_cbo_groups) on
    weights w: the key's dollars (FEDTAX_BC on the record, or split equally over the SPM unit) in CBO income group j x
    AGI bin k, the cells raked to CBO's group shares and IRS's bin shares, and a person's share
    sum_k R[j, k] x its dollars in (j, k) / the cell's dollars. Sums to 1 over civilians. Returns it and the number of
    raking iterations."""
    m14 = _pool14(bin_dollars(d, d.FEDTAX_BC.to_numpy(float), alloc, edges).T).T
    pos = [j for j in cbo if cbo[j] > 0]
    tb = np.stack([m14[civ & (g == j)].T @ w[civ & (g == j)] for j in pos])
    rows = np.array([cbo[j] for j in pos])
    r = rows[:, None] * tb / tb.sum(axis=1, keepdims=True)
    for it in range(20000):
        r *= cols[None, :] / r.sum(axis=0)[None, :]
        r *= (rows / r.sum(axis=1))[:, None]
        if max(np.abs(r.sum(axis=0) - cols).max(), np.abs(r.sum(axis=1) - rows).max()) < 1e-12:
            break
    else:
        raise SystemExit(f"[BLOCKED] the {alloc} raking did not converge")
    ratio = np.divide(r, tb, out=np.zeros_like(r), where=tb > 0)
    v = np.zeros(len(d))
    for i, j in enumerate(pos):
        mj = civ & (g == j)
        v[mj] = m14[mj] @ ratio[i]
    return v, it + 1


def cbo_shares():
    """CBO's 2022 shares of individual income tax by income group (the benchmark lane's CBO_SPEC rows)."""
    shares = pd.read_csv(BENCH / "derived/cbo_group_shares.csv").query("spec == @CBO_SPEC").set_index("group")
    return {j: float(shares.loc[j, "cbo_share"]) for j in benchmark_frame().GROUPS}


def cbo_groups(d):
    """Each person's CBO income group, as cbo_arm.groups(d) assigns it: household income before transfers and taxes,
    Medicare at model.json's national line per enrollee."""
    bf = benchmark_frame()
    medicare = next(x for x in bf.model()["spending"]["lines"] if x["id"] == "medicare")["national_bn"]
    per = medicare * 1e9 / d.pwwgt0.to_numpy(float)[d.MCARE.eq(1).to_numpy()].sum()
    g, _ = bf.cbo_groups(d, bf.cbo_income(d, per), d.pwwgt0.to_numpy(float))
    return g


def state_base(d, alloc):
    """The state_liability key's dollars: STATETAX_A floored at 0, on the record or split equally over the SPM unit."""
    stl = d.STATETAX_A.clip(lower=0).to_numpy(float)
    return stl if alloc == "personal" else benchmark_frame().unit_equal(stl, d.SPM_ID.to_numpy())


def national_lines():
    """model.json's national lines the keys share out, $bn: federal, state and local, and other personal income tax."""
    model = {x["id"]: x for x in benchmark_frame().model()["receipts"]["lines"]}
    return {lid: float(model[lid]["national_bn"]) for lid in LINES}


def case_keys(d, civ, union, gate):
    """The case's keys on the benchmark frame d (TAX_COLS) at both allocations; civ and union are its masks
    (frame.masks). Gates go through gate(label, ok, detail). Returns fit_case_<allocation>, the federal shares (summing
    to 1 over civilians on pwwgt0), and sit_case_<allocation>, the state key's dollars."""
    bf = benchmark_frame()
    w0 = d.pwwgt0.to_numpy(float) * civ
    labels, irs = irs_2023()
    bins = pd.read_csv(HERE / "derived/bins.csv")
    gate("IRS TY2023 bin shares are heldout's bins.csv (1e-12)", list(bins.irs_label) == labels
         and float(np.abs(bins.irs_2023_share_pct.to_numpy() / 100 - irs).max()) < 1e-12)
    edges, _ = bin_edges(labels)
    cbo = cbo_shares()
    g = cbo_groups(d)
    held = json.loads((HERE / "derived/translation_inputs.json").read_text())
    model = {x["id"]: x for x in bf.model()["receipts"]["lines"]}
    cell = lambda lid, a: model[lid]["cells"]["cbo_collective"][a]["share"]  # noqa: E731
    out = {}
    for a in ALLOCATIONS:
        v, iters = raked_vector(d, w0, civ, g, a, cbo, _pool14(irs), edges)
        want = held["reweighted_share"][a] + held["share_change"]["irs_2023_raked_with_cbo_groups"][a]
        got = float(w0[union] @ v[union])
        gate(f"federal, {a}: the union's raked share is heldout's translation, the vector sums to 1 (1e-12; {iters} "
             "iterations)", abs(got - want) < 1e-12 and abs(float(w0 @ v) - 1) < 1e-12, f"{got:.15f} vs {want:.15f}")
        raw = d.FEDTAX_BC.to_numpy(float)
        raw = raw if a == "personal" else bf.unit_equal(raw, d.SPM_ID.to_numpy())
        st = state_base(d, a)
        f_u, s_u = float(w0[union] @ raw[union] / (w0 @ raw)), float(w0[union] @ st[union] / (w0 @ st))
        gate(f"federal and state, {a}: the union's unraked shares are model.json's federal_liability and state_liability "
             "cells (1e-9)", abs(f_u - cell("federal_income_tax", a)) < 1e-9 and abs(s_u - cell("state_local_income_tax", a)) < 1e-9
             and cell("other_personal_tax", a) == cell("state_local_income_tax", a), f"{f_u:.9f}, {s_u:.9f}")
        out[f"fit_case_{a}"], out[f"sit_case_{a}"] = v, st
    return out


def person_keys():
    """case_keys on the benchmark frame with gates that stop the run ([BLOCKED]), one row per CPS person keyed by
    PH_SEQ and PPPOS, beside the frame's civilian mask and pwwgt0."""
    fails = []

    def gate(label, ok, detail=""):
        print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
        if not ok:
            fails.append(label)

    d = load_frame(TAX_COLS + ["PPPOS"])
    civ, union = benchmark_frame().masks(d)
    keys = case_keys(d, civ, union, gate)
    if fails:
        raise SystemExit(f"[BLOCKED] the case's income-tax keys failed {len(fails)} gate(s): {fails}")
    out = pd.DataFrame({"PH_SEQ": d.PH_SEQ.to_numpy(), "PPPOS": d.PPPOS.to_numpy(), "civilian": civ,
                        "pwwgt0": d.pwwgt0.to_numpy(float), **keys})
    if out.duplicated(["PH_SEQ", "PPPOS"]).any():
        raise SystemExit("[BLOCKED] PH_SEQ and PPPOS do not identify the frame's persons")
    return out
