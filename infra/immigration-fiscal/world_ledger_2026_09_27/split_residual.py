"""How the generation lane's split of each line departs from splitting the corrected line by the generations'
shares of it, per band end, generation and line (convention (a)). A diagnostic: no ledger number depends on it.

For a line at a band end, C_g is the lane's cost for generation g (the engine's effect negated: spending +,
receipts -), U_g the uncorrected model's cost at the same specification, and C, U their sums over generations:
- prorata_bn  = C x p_g, where p_g is the generation's share of the line's target in the uncorrected models, under
                the line's preferred key (spending) or the specification's receipt cell (receipts): the corrected
                line split by the generation lane's own per-line keys;
- spec_key_bn = C x U_g / U: the same split by the keys the engine applies at the specification;
- lane_bn     = C_g.
The steps add to the lane's cost: lane = prorata + key_step + corrections_step, where key_step = spec_key - prorata
and corrections_step = lane - spec_key = E_g - E x U_g / U, E_g being the change the generation's correction edits
make to the specification's cell (key or receipt scenario) times the line's response. The edits replay in the
payload's order, as engine.js applies them: a cell edit adds its `by`; a national-scale edit (from sept29) scales
the running cell by the new national total over the running one. A gate requires C_g - U_g = E_g to 1e-6 on every
line both models list. Correction-only lines (the payloads' `lines` and, from sept29, `receipt_lines`; absent from
the uncorrected models, or at zero from sept27) have no uncorrected split: their whole cost is correction_only_bn.
Lines the models do not list (capital-return components from sept27) have no preferred key: their split by the
specification's keys is unlisted_bn, and lane = unlisted + corrections_step. A gate requires the steps to add to
the lane's cost on every row.

Inputs: derived/generation_lines_<case>.csv and generation_lines_uncorrected_<case>.csv (generation_lines.cjs);
the generation lane's generation_corrections.json and model_{G1,G2,G3plus}.json at the case's generation pin.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/world_ledger_2026_09_27/split_residual.py [--case sept26_schools|sept27|sept29]
Output: derived/generation_split_residual_<case>.csv.
"""
import argparse
import json
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd

from valuation import PINS, lane_file

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
DERIVED = HERE / "derived"
GENS = ["G1", "G2", "G3plus"]
ALLOC = {"low": "shared", "high": "personal"}


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def git_json(pin, rel):
    return json.loads(subprocess.run(["git", "-C", str(REPO), "show", f"{pin}:{rel}"], capture_output=True,
                                     check=True).stdout)


def target_share(models, side, line, key, alloc):
    """Each generation's share of the line's target in the uncorrected models: the preferred key for spending, the
    specification's receipt cell for receipts; None when a model does not list the line."""
    t = []
    for g in GENS:
        m = models[g]
        lines = {x["id"]: x for x in (m["spending"] if side == "spending" else m["receipts"])["lines"]}
        if line not in lines:
            return None
        x = lines[line]
        cell = x["keys"][x["preferred_key"]] if side == "spending" else x["cells"][key.split(":")[0]]
        t.append(cell[alloc]["target_bn"])
    t = np.array(t, dtype=float)
    return t / t.sum() if t.sum() else None


def edit_cost(model, edits, side, line, key, alloc, response):
    """The generation's correction edits on the line, as a cost: the change they make to the specification's cell
    (its key for spending, its receipt scenario for receipts) in the uncorrected model, times the line's response,
    negated for receipts. The edits replay in the payload's order, as engine.js applies them: a cell edit adds its
    `by` to its own cell; a national-scale edit ({side, line, national_bn}) scales every cell of the line by the new
    national total over the running one."""
    x = {r["id"]: r for r in (model["spending"] if side == "spending" else model["receipts"])["lines"]}[line]
    cell = key if side == "spending" else key.split(":")[0]
    start = amount = (x["keys"] if side == "spending" else x["cells"])[cell][alloc]["target_bn"]
    national = x["national_bn"]
    for e in edits.get((side, line), []):
        if "national_bn" in e:
            amount *= e["national_bn"] / national
            national = e["national_bn"]
        elif (e.get("key") if side == "spending" else e.get("scenario")) == cell:
            amount += e["by"][alloc]
    return (amount - start) * response * (1 if side == "spending" else -1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--case", default="sept26_schools", choices=sorted(PINS))
    case = ap.parse_args().case
    pin = PINS[case]["generation"]
    gate("generation_pin", bool(pin), case=case)
    corr = git_json(pin, lane_file(case, "generation", "generation_corrections.json"))
    models = {g: git_json(pin, lane_file(case, "generation", f"model_{g}.json")) for g in GENS}
    edits = {g: {} for g in GENS}
    for g in GENS:
        for e in corr["payloads"]["a"][g]["edits"]:
            edits[g].setdefault((e["side"], e["line"]), []).append(e)
    only = {x["id"] for g in GENS for part in ("lines", "receipt_lines")
            for x in corr["payloads"]["a"][g].get(part, [])}
    keys = ["band_end", "generation", "side", "line"]
    c = pd.read_csv(DERIVED / f"generation_lines_{case}.csv", keep_default_na=False, na_values=[""])
    u = pd.read_csv(DERIVED / f"generation_lines_uncorrected_{case}.csv", keep_default_na=False, na_values=[""])
    tot = c[c.side == "total"].pivot_table(index=["band_end", "generation"], columns="line", values="effect_bn")
    c, u = (d[d.side != "total"].assign(cost=lambda x: -x.effect_bn).set_index(keys) for d in (c, u))
    # From sept27 the package lists the correction-only spending lines in the uncorrected models too, at zero.
    u_only = u.index.get_level_values("line").isin(only)
    gate("correction_only_lines_are_zero_in_the_uncorrected_models", bool((u[u_only].amount_bn.abs() < 1e-12).all()),
         nonzero=u[u_only & (u.amount_bn.abs() >= 1e-12)].index.tolist()[:5])
    u = u[~u_only]
    gate("uncorrected_lines_are_corrected_lines_less_correction_only_lines",
         set(u.index) == {k for k in c.index if k[3] not in only} and {k[3] for k in c.index} >= only,
         only_uncorrected=sorted(set(u.index) - set(c.index))[:5])
    rows, worst = [], 0.0
    for (end, side, line), grp in c.reset_index().groupby(["band_end", "side", "line"], sort=False):
        C = grp.set_index("generation").reindex(GENS)
        head = dict(case=case, band_end=end, spec=int(C.spec.iloc[0]), allocation=C.allocation.iloc[0], side=side,
                    line=line, key=C.key.iloc[0])
        if line in only:
            for g in GENS:
                rows.append(dict(head, generation=g, prorata_bn=np.nan, spec_key_bn=np.nan, lane_bn=C.cost[g],
                                 key_step_bn=np.nan, unlisted_bn=np.nan, corrections_step_bn=np.nan,
                                 correction_only_bn=C.cost[g]))
            continue
        U = u.loc[[(end, g, side, line) for g in GENS], "cost"].to_numpy()
        gate(f"one_key_per_line_{end}_{line}", C.key.nunique(dropna=False) == 1, keys=C.key.unique().tolist())
        p = target_share(models, side, line, head["key"], ALLOC[end]) if side != "capital" else None
        s = U / U.sum() if U.sum() else np.full(3, np.nan)
        total = C.cost.sum()
        for k, g in enumerate(GENS):
            if side != "capital":
                e = edit_cost(models[g], edits[g], side, line, head["key"], ALLOC[end], C.response[g])
                worst = max(worst, abs(C.cost[g] - U[k] - e))
            pr = total * p[k] if p is not None else np.nan
            sk = total * s[k]
            rows.append(dict(head, generation=g, prorata_bn=pr, spec_key_bn=sk, lane_bn=C.cost[g],
                             key_step_bn=sk - pr, unlisted_bn=sk if p is None else np.nan,
                             corrections_step_bn=C.cost[g] - sk, correction_only_bn=np.nan))
    gate("each_line_moves_by_its_correction_edit", worst < 1e-6, max_abs_diff=worst)
    out = pd.DataFrame(rows)
    steps = ["prorata_bn", "key_step_bn", "unlisted_bn", "corrections_step_bn", "correction_only_bn"]
    d = (out[steps].fillna(0).sum(axis=1) - out.lane_bn).abs().max()
    gate("the_steps_add_to_the_lane_cost_on_every_row", d < 1e-9, max_abs_diff=d)
    out["band_end"] = pd.Categorical(out.band_end, ["low", "high"])
    out = out.sort_values(["band_end", "generation", "side", "line"], kind="mergesort")
    # Gate: each generation's lines add to its direct response plus capital return.
    got = out.groupby(["band_end", "generation"], observed=True).lane_bn.sum()
    want = tot.direct_fiscal + tot.capital_return
    d = max(abs(got[k] - want[k]) for k in want.index)
    gate("lines_add_to_the_direct_response_and_capital_return", d < 1e-6, max_abs_diff=d)
    cols = ["case", "band_end", "spec", "allocation", "generation", "side", "line", "key", "prorata_bn", "spec_key_bn",
            "key_step_bn", "unlisted_bn", "corrections_step_bn", "correction_only_bn", "lane_bn"]
    out[cols].to_csv(DERIVED / f"generation_split_residual_{case}.csv", index=False, lineterminator="\n",
                     float_format="%.9f")
    print(f"  ✓ gates pass: every line moves by its correction edit (max |diff| {worst:.1e} bn); the steps add up")
    s = out.groupby(["band_end", "generation"], observed=True)[steps + ["lane_bn"]].sum(min_count=1)
    print(s.round(2).to_string())
    print(f"  wrote derived/generation_split_residual_{case}.csv: {len(out)} rows")


if __name__ == "__main__":
    main()
