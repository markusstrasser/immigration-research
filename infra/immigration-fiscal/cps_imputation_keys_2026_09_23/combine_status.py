"""How this lane's correction combines with the dataset audit's tax-compliance re-key.

`dataset_integrity_2026_09_23/cps.md` row 1 (`cps_status_keys.py`) applies the status lane's rules to
the Latin-American-born people that `status_impute_2026_09_16` classes as unauthorized (PENATVTY
302-399 except Cuba): EITC zeroed; ACTC, federal and state liability, capped and uncapped wages,
self-employment payroll and the FICA-worker count scaled by an on-books share (0.44, 0.60, 0.75).
This lane corrects the imputed incomes those keys are built from. Both act on the same seven keys,
so they are combined on one frame: the status rules are applied to the account's own key vectors
(common.receipt_vectors, common.spending_vectors) of

  - the published file: the audit's correction alone, on the account's exact keys;
  - the reweighted file of step 4a (brief cells, material 5%);
  - the union-matched hot deck and its pooled control of step 4b (main specification, 5 seeds).

Status is held at its published assignment (main). A check recomputes it on each hot-deck frame,
where re-imputed Social Security, SSI, Medicare and Medicaid enter the status lane's legal-status
rules. Every combination goes through translate.py's gated main-case translation.
Outputs: derived/status_combination_keys.csv, derived/status_combination_components.csv,
derived/status_combination_by_key.csv, derived/status_combination_overlap.csv,
derived/status_combination_line_deltas.json, derived/status_combination_translation.csv.
Run from the repository root (after ipw.py and run_hotdeck.py):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
    infra/immigration-fiscal/cps_imputation_keys_2026_09_23/combine_status.py
"""
from __future__ import annotations

import json
import sys
import zipfile

import numpy as np
import pandas as pd

import common as c
import hotdeck
import ipw
import translate

sys.dont_write_bytecode = True  # read-only import from the status lane
sys.path.insert(0, str(c.FISCAL / "status_impute_2026_09_16"))
from impute_status import impute  # noqa: E402

AUDIT = c.FISCAL / "dataset_integrity_2026_09_23/derived/cps_status_keys.csv"
ON_BOOKS = (0.44, 0.60, 0.75)
SEEDS = [20260923 + i for i in range(5)]
SCALED = ["federal_liability", "state_liability", "wage", "wage_oasdi", "self_payroll", "positive_fica_worker"]
STATUS_KEYS = SCALED + ["refundable_credits"]
STATUS_COLS = ["PH_SEQ", "PPPOS", "A_LINENO", "A_SPOUSE", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
               "PEINUSYR", "SS_VAL", "SSI_VAL", "MCAID", "MCARE", "MIL", "CHAMPVA", "VET_YN", "PEAFEVER",
               "A_CLSWKR", "PEIOOCC"]
BENEFITS = ["SS_VAL", "SSI_VAL", "MCAID", "MCARE"]
# spending.md #1: the premium-tax-credit part of the refundable line is about $100-120bn of $228.8bn;
# the audit applies EITC+ACTC key changes to the rest only.
NON_PTC_FRACTION = (108.8 / 228.8, 128.8 / 228.8)


def status_inputs():
    with zipfile.ZipFile(c.CPS_ZIP) as z:
        s = pd.read_csv(z.open("pppub25.csv"), usecols=STATUS_COLS)
        hh = pd.read_csv(z.open("hhpub25.csv"), usecols=["H_SEQ", "HPUBLIC", "HLORENT"])
    return s, hh


def unauthorized(s, hh, d, frame=None):
    """The audit's rule, aligned to d's rows. With frame, benefit fields come from that frame."""
    if frame is not None:
        new = frame[["PH_SEQ", "PPPOS"] + BENEFITS]
        s = s.drop(columns=BENEFITS).merge(new, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    st = impute(s, hh)
    latin = s.PENATVTY.between(302, 399).to_numpy() & ~s.PENATVTY.eq(327).to_numpy()
    flag = pd.DataFrame({"PH_SEQ": s.PH_SEQ.to_numpy(), "PPPOS": s.PPPOS.to_numpy(),
                         "u": st["unauthorized"] & latin})
    out = d[["PH_SEQ", "PPPOS"]].merge(flag, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if out.u.isna().any():
        raise SystemExit("[BLOCKED] status flags do not align with the lane frame")
    return out.u.to_numpy(bool)


def status_vectors(frame, unauth, on_books, index):
    """The account's key vectors with the audit's rules applied (on_books None: unchanged)."""
    rv = c.receipt_vectors(frame)
    f = frame
    if on_books is not None:
        for k in SCALED:
            rv[k] = np.where(unauth, rv[k] * on_books, rv[k])
        f = frame.assign(EIT_CRED=np.where(unauth, 0.0, frame.EIT_CRED.to_numpy(float)),
                         ACTC_CRD=np.where(unauth, frame.ACTC_CRD.to_numpy(float) * on_books,
                                           frame.ACTC_CRD.to_numpy(float)))
    return c.receipt_keys(frame, index, rv), c.spending_vectors(f, index)


def key_shares(frame, unauth, on_books, W, civ, union, index):
    rk, sk = status_vectors(frame, unauth, on_books, index)
    out = {}
    for a in ["personal", "shared"]:
        for k, v in {**c.shares(rk[a], W, civ, union), **c.shares(sk[a], W, civ, union)}.items():
            out[(a, k)] = v
    return out


def ipw_shares(d, unauth, on_books, W, civ, union, index, stored):
    """Step 4a main specification with the status-scaled vectors for the seven audited keys."""
    cv = c.cell_vars(d)
    cv["union"] = union.astype(int)
    frames = [cv[cols] for cols in ipw.SPECS["a_brief_cells"]]
    status, _, _ = c.key_status(d, 0.05)
    rk, sk = status_vectors(d, unauth, on_books, index)
    out, cache = {}, {}
    for a in ["personal", "shared"]:
        vectors = {**rk[a], **sk[a]}
        for key in vectors:
            name = f"a_brief_cells|material_5pct|{a}|{key}"
            if name not in stored.files:
                continue
            if key not in STATUS_KEYS:
                out[(a, key)] = stored[name]
                continue
            imputed = status[a][key]
            sig = (a, hash(imputed.tobytes()))
            if sig not in cache:
                cache[sig] = ipw.ipw_weights(W, ~imputed, civ, frames)[0]
            Wa = cache[sig]
            v = vectors[key]
            out[(a, key)] = (v[union] @ Wa[union]) / (v[civ] @ Wa[civ])
    return out


def mean_shares(runs):
    return {k: np.mean([r[k] for r in runs], axis=0) for k in runs[0]}


def cost_by_key(lines):
    """Change in the main case's cost by key, $bn: minus direct receipts, plus transfers and
    income-security services (the lines that enter the band in the CBO-lag profiles)."""
    x = lines[lines.preferred].copy()
    counted = (x.side.eq("receipts") & x.direct) | (x.side.eq("spending") & (
        x.response_class.eq("household_transfer") | x.line.eq("income_security_services")))
    x = x[counted]
    x["cost_bn"] = np.where(x.side.eq("receipts"), -x.change_bn, x.change_bn)
    return x.groupby(["method", "allocation", "key"]).cost_bn.sum()


def main():
    d = c.load_frame()
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    index = c.spm_index(d)
    s_in, hh = status_inputs()
    unauth = unauthorized(s_in, hh, d)
    w0 = W[:, 0]
    print(f"[combine] status-lane unauthorized, Latin-American-born: {w0[unauth].sum() / 1e6:.3f}M, "
          f"in the union {w0[unauth & union].sum() / 1e6:.3f}M", flush=True)

    base = key_shares(d, unauth, None, W, civ, union, index)
    methods = {}
    for ob in ON_BOOKS:
        methods[f"status_{ob:.2f}"] = key_shares(d, unauth, ob, W, civ, union, index)

    # Gate 1: the audit's re-key reproduces on the account's exact keys (self-employment excepted:
    # the audit's own vector did not reproduce the account's key, cps.md row 1 limits).
    audit = pd.read_csv(AUDIT)
    rows = []
    for r in audit[audit.allocation.isin(["personal", "both"])].itertuples():
        key = "refundable_credits" if r.key == "eitc_actc_spending" else r.key
        ours = methods[f"status_{r.on_books:.2f}"][("personal", key)][0] / base[("personal", key)][0] - 1
        rows.append(dict(on_books=r.on_books, key=key, audit_rel=r.share_corrected / r.share_raw - 1, lane_rel=ours))
    check = pd.DataFrame(rows)
    check["difference"] = check.lane_rel - check.audit_rel
    print(check.round(4).to_string(index=False), flush=True)
    worst = check[check.key != "self_payroll"].difference.abs().max()
    if worst > 0.005:
        raise SystemExit(f"[BLOCKED] audit re-key not reproduced (max difference {worst:.4f})")

    # (a) reweighting, with and without the audit's rules. Gate 2: without them it equals step 4a.
    stored = np.load(c.CACHE / "ipw_key_shares.npz")
    plain = ipw_shares(d, unauth, None, W, civ, union, index, stored)
    gap = max(np.abs(plain[k] - stored[f"a_brief_cells|material_5pct|{k[0]}|{k[1]}"]).max() for k in plain)
    print(f"[combine] step 4a reproduced, max share difference {gap:.2e}", flush=True)
    if gap > 1e-12:
        raise SystemExit("[BLOCKED] step 4a shares not reproduced")
    methods["a_ipw_brief_cells"] = plain
    for ob in ON_BOOKS:
        methods[f"a_ipw_brief_cells+status_{ob:.2f}"] = ipw_shares(d, unauth, ob, W, civ, union, index, stored)

    # (b) hot deck, 5 seeds. Gate 3: without the rules the shares equal run_hotdeck.py's per seed.
    hd = np.load(c.CACHE / "hotdeck_key_shares.npz")
    runs, overlap = {}, []
    for seed in SEEDS:
        for variant, cells in [("matched", hotdeck.BASE), ("pooled", [])]:
            print(f"[combine] hot deck seed {seed} {variant}", flush=True)
            new, _ = hotdeck.run(d, seed=seed, verbose=False, base=cells)
            # Where the re-imputation changes the union's dollars: on the audit's unauthorized or not.
            for col in ["FEDTAX_BC", "STATETAX_A", "WSAL_VAL", "EIT_CRED"]:
                change = (new[col].to_numpy(float) - d[col].to_numpy(float)) * w0
                overlap.append(dict(seed=seed, variant=variant, column=col, union_change_bn=change[union].sum() / 1e9,
                                    on_unauthorized_bn=change[union & unauth].sum() / 1e9))
            plain_hd = key_shares(new, unauth, None, W, civ, union, index)
            gap = max(np.abs(plain_hd[k] - hd[f"main|{variant}@{seed}|{k[0]}|{k[1]}"]).max() for k in plain_hd)
            if gap > 1e-12:
                raise SystemExit(f"[BLOCKED] hot-deck shares not reproduced for seed {seed} {variant}: {gap:.2e}")
            runs.setdefault((variant, None, "fixed"), []).append(plain_hd)
            recomputed = unauthorized(s_in, hh, d, frame=new)
            moved = w0[(recomputed != unauth) & union].sum() / 1e6
            print(f"[combine]   recomputed status changes {moved:.3f}M union members; union unauthorized "
                  f"{w0[unauth & union].sum() / 1e6:.3f}M -> {w0[recomputed & union].sum() / 1e6:.3f}M", flush=True)
            for ob in ON_BOOKS:
                runs.setdefault((variant, ob, "fixed"), []).append(key_shares(new, unauth, ob, W, civ, union, index))
                runs.setdefault((variant, ob, "recomputed"), []).append(
                    key_shares(new, recomputed, ob, W, civ, union, index))
    overlap = pd.DataFrame(overlap).groupby(["variant", "column"])[["union_change_bn", "on_unauthorized_bn"]].mean()
    overlap["unauthorized_fraction"] = overlap.on_unauthorized_bn / overlap.union_change_bn
    overlap.reset_index().to_csv(c.OUT / "status_combination_overlap.csv", index=False)
    print(overlap.round(3).to_string(), flush=True)
    matched, pooled = mean_shares(runs[("matched", None, "fixed")]), mean_shares(runs[("pooled", None, "fixed")])
    methods["b_hotdeck_union_matched"] = matched
    methods["b_matched_over_pooled"] = {k: base[k] * matched[k] / pooled[k] for k in base}
    for ob in ON_BOOKS:
        st = methods[f"status_{ob:.2f}"]
        for mode in ["fixed", "recomputed"]:
            m = mean_shares(runs[("matched", ob, mode)])
            p = mean_shares(runs[("pooled", ob, mode)])
            tag = "" if mode == "fixed" else "_recomputed"
            methods[f"b_hotdeck_union_matched+status{tag}_{ob:.2f}"] = m
            methods[f"b_matched_over_pooled+status{tag}_{ob:.2f}"] = {k: st[k] * m[k] / p[k] for k in st}

    # Key table: relative change of the union's share against the published keys.
    key_rows = []
    for name, method in methods.items():
        for (a, k), v in method.items():
            if k in STATUS_KEYS + ["consumption", "social_security"]:
                key_rows.append(dict(method=name, allocation=a, key=k, rel_change=v[0] / base[(a, k)][0] - 1,
                                     rel_change_se=c.sdr(v / base[(a, k)] - 1)))
    pd.DataFrame(key_rows).to_csv(c.OUT / "status_combination_keys.csv", index=False)

    # Main case: the same gated translation as translate.py.
    model = json.loads(translate.MODEL.read_text())
    hf = translate.household_fraction(d)
    payload, line_rows, comp_rows = translate.translate(model, base, methods, hf)
    lines = pd.DataFrame(line_rows)
    comp = pd.DataFrame(comp_rows).query("profile == 'cbo_lag'")
    refundable = (lines[lines.preferred & lines.line.eq("refundable_tax_credits")]
                  .set_index(["method", "allocation"]).change_bn)
    net = comp[comp.component.eq("net_cost_change")].set_index(["method", "allocation"])
    for label, frac in zip(["non_ptc_low", "non_ptc_high"], NON_PTC_FRACTION):
        # Under spending.md #1 only the non-PTC part of the refundable line keeps the EITC+ACTC key.
        net[f"net_cost_change_{label}_bn"] = net.change_bn - refundable.reindex(net.index).fillna(0) * (1 - frac)
    net.reset_index().to_csv(c.OUT / "status_combination_components.csv", index=False)

    # Key by key: the audit alone, this lane alone, both on one frame, and the interaction.
    cost = cost_by_key(lines)
    by_key = []
    for ob in ON_BOOKS:
        audit_m = f"status_{ob:.2f}"
        for mine in ["a_ipw_brief_cells", "b_hotdeck_union_matched", "b_matched_over_pooled"]:
            both = f"{mine}+status_{ob:.2f}"
            for a in ["personal", "shared"]:
                keys = sorted(set(cost.loc[audit_m, a].index) | set(cost.loc[mine, a].index) | set(cost.loc[both, a].index))
                for k in keys:
                    get = lambda m: float(cost.get((m, a, k), 0.0))
                    by_key.append(dict(on_books=ob, lane_method=mine, allocation=a, key=k, audit_alone_bn=get(audit_m),
                                       lane_alone_bn=get(mine), combined_bn=get(both),
                                       interaction_bn=get(both) - get(audit_m) - get(mine)))
    by_key = pd.DataFrame(by_key)
    by_key.to_csv(c.OUT / "status_combination_by_key.csv", index=False)
    show = by_key.query("on_books == 0.44 and allocation == 'personal' and lane_method == 'b_hotdeck_union_matched'")
    print(show.round(2).to_string(index=False), flush=True)
    path = c.OUT / "status_combination_line_deltas.json"
    path.write_text(json.dumps(payload, indent=1) + "\n")
    print(net.reset_index()[["method", "allocation", "change_bn", "se_bn", "net_cost_change_non_ptc_low_bn",
                             "net_cost_change_non_ptc_high_bn"]].round(2).to_string(index=False), flush=True)
    translate.run_node(path, c.OUT / "status_combination_translation.csv")


if __name__ == "__main__":
    main()
