"""State pricing's price indexes on audit row 4's state mix.

v4's state-pricing item multiplies each parent line's (row-4) key by sum_f S&L_f x (index_f - 1), and the sales and
licence receipts by (S&L / national) x (index - 1). Each index_f is sum_s w_s x relative price_s, with w_s the group's
state shares at the ASEC published weights (state_price.py group_by_state: pwwgt0, TARGET_N 40,896,574). Row 4 moves
1.18M people, all outside California and Texas, so it moves w_s. This recomputes the lane's central indexes with its
own functions (imported read-only; main() is not run, nothing is written outside this lane) at the published shares
(gates: the lane's derived indexes) and at row 4's (Mexico-born naturalized / noncitizen outside CA+TX times
weight_arms' factors, from derived/row4_parta.json).
Writes derived/row4_state_index.json. Run from the repository root after row4_parta.py:
  OPENBLAS_NUM_THREADS=1 UV_OFFLINE=1 uv run --no-project python3 infra/immigration-fiscal/row4_class_2026_09_29/row4_state_index.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True

import csv  # noqa: E402
import json  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
LANE = FISCAL / "state_priced_services_2026_09_29"
sys.path.insert(0, str(LANE))
import state_price as SP  # noqa: E402

FAILS = []


def gate(label, ok, detail=""):
    print(f"GATE {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


FAC = json.loads((OUT / "row4_parta.json").read_text())["factors"]
COUNTS = {r["count"]: r for r in csv.DictReader(open(FISCAL / "population_basis_2026_09_29/derived/frame_counts.csv"))}
N_ROW4 = float(COUNTS["union|all"]["row4"])
by, rep, rep_adults = SP.group_by_state()
# The same persons as group_by_state, with row 4's factor.
canonical_target = SP.canonical_target_fn()
fields = ["PH_SEQ", "PPPOS", "A_AGE", "PTOTVAL", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP"]
with zipfile.ZipFile(SP.CPS) as z:
    d = pd.read_csv(z.open("pppub25.csv"), usecols=fields)
    w = pd.read_csv(z.open("asec_csv_repwgt_2025.csv"), usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
    h = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"]).rename(columns={"H_SEQ": "PH_SEQ"})
d = d.merge(w, on=["PH_SEQ", "PPPOS"], validate="one_to_one", how="left").merge(h, on="PH_SEQ", validate="many_to_one", how="left")
civ, target = canonical_target(d)
mb = d.PENATVTY.eq(303) & ~d.GESTFIPS.isin([6, 48])
f = np.where(mb & d.PRCITSHP.eq(4), FAC["natz"], np.where(mb & d.PRCITSHP.eq(5), FAC["noncit"], 1.0))
d = d.assign(target=target, adult=d.A_AGE.ge(18), w4=d.pwwgt0 * f)
g = d[d.target]
gate("published group total", abs(g.pwwgt0.sum() - SP.TARGET_N) < 0.01, f"{g.pwwgt0.sum():.4f}")
gate("row-4 group total", abs(g.w4.sum() - N_ROW4) < 1.0, f"{g.w4.sum():.4f}")
by4 = pd.DataFrame({"group": g.groupby("GESTFIPS").w4.sum(), "group_adults": g[g.adult].groupby("GESTFIPS").w4.sum(),
                    "group_income_bn": (g.w4 * g.PTOTVAL.clip(lower=0)).groupby(g.GESTFIPS).sum() / 1e9}).reindex(by.index).fillna(0)
gate("published by-state groups rebuilt", float((g.groupby("GESTFIPS").pwwgt0.sum().reindex(by.index).fillna(0) - by.group).abs().max()) < 1e-6)


def gp_of(b):
    return b.assign(group_share=b.group / b.group.sum(), group_adult_share=b.group_adults / b.group_adults.sum())


gp0, gp4 = gp_of(by), gp_of(by4)
w_rep = rep / rep.sum()
w_rep_adults = rep_adults / rep_adults.sum()
fin = SP.read_finance(2024)
pop = SP.populations(2024)
amt = SP.function_amounts(fin, "direct").reindex(sorted(SP.STATES))
rel = amt.div(pop, axis=0) / (amt.sum() / pop.sum())
ix0, ix4 = SP.indexes(gp0.group_share, rel), SP.indexes(gp4.group_share, rel)
pix0, _, _ = SP.prison_per_inmate(gp0, w_rep)
pix4, _, _ = SP.prison_per_inmate(gp4, w_rep)
sel = lambda t: float(t[(t.year == 2024) & (t.spec == "institutions") & (t.weights == "group_x_state_imprisonment")]["index"].iloc[0])  # noqa: E731
ix0["corrections_per_inmate"], ix4["corrections_per_inmate"] = sel(pix0), sel(pix4)
rix0 = SP.receipt_indexes(gp0, w_rep, w_rep_adults)
rix4 = SP.receipt_indexes(gp4, w_rep, w_rep_adults)

corr = [r for r in csv.DictReader(open(LANE / "derived/corrections.csv")) if r["candidate"] == "True"]
rcorr = {r["line"]: r for r in csv.DictReader(open(LANE / "derived/receipts_corrections.csv")) if r["candidate"] == "True"}
out = {"functions": {}, "lines": {}, "receipts": {}}
for r in corr:
    fn = r["function"]
    gate(f"published index {fn} reproduces corrections.csv", abs(ix0[fn] - float(r["index"])) < 1e-8, f"{ix0[fn]:.9f} vs {r['index']}")
    out["functions"][fn] = dict(line=r["line"], sl_amount_bn=float(r["sl_amount_bn"]), index_published=float(ix0[fn]), index_row4=float(ix4[fn]))
for line in sorted({r["line"] for r in corr}):
    fs = [v for v in out["functions"].values() if v["line"] == line]
    pre0 = sum(v["sl_amount_bn"] * (v["index_published"] - 1) for v in fs)
    pre4 = sum(v["sl_amount_bn"] * (v["index_row4"] - 1) for v in fs)
    out["lines"][line] = dict(sp_pre_published_bn=pre0, sp_pre_row4_bn=pre4, ratio=pre4 / pre0)
    print(f"{line}: sum S&L x (index - 1) published {pre0:.6f} row 4 {pre4:.6f} ratio {pre4 / pre0:.6f}", flush=True)
for line, r in rcorr.items():
    wname = r["weights"]
    pick = lambda t: float(t[(t.year == 2024) & (t.receipt == line) & (t.weights == wname)]["index"].iloc[0])  # noqa: E731
    i0, i4 = pick(rix0), pick(rix4)
    gate(f"published receipt index {line} reproduces receipts_corrections.csv", abs(i0 - float(r["index"])) < 1e-8, f"{i0:.9f}")
    k = float(r["sl_amount_bn"]) / float(r["national_bn"])
    out["receipts"][line] = dict(weights=wname, index_published=i0, index_row4=i4, factor_published=k * (i0 - 1), factor_row4=k * (i4 - 1))
    print(f"{line}: index published {i0:.6f} row 4 {i4:.6f}; factor {k * (i0 - 1):.6f} -> {k * (i4 - 1):.6f}", flush=True)
out["shares"] = {"CA": [float(gp0.group_share[6]), float(gp4.group_share[6])], "TX": [float(gp0.group_share[48]), float(gp4.group_share[48])]}
out["gates_failed"] = FAILS
if FAILS:
    print(f"[BLOCKED] {len(FAILS)} gate(s) failed; nothing written", flush=True)
    sys.exit(1)
(OUT / "row4_state_index.json").write_text(json.dumps(out, indent=1) + "\n")
