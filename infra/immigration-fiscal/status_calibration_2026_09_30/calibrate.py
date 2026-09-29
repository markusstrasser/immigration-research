"""The legal-status calibration arm, step 1: re-assign status among the group's Mexico-born noncitizens so their
unauthorized total reaches Pew's 4.3M, DHS's 4.8M and CMS's 5.1M, and rebuild the case's status stack on each.

Status in the adopted case is the Borjas residual on CPS ASEC 2025 (status_impute_2026_09_16), not raked to any
external total (its RESULT.md:195), with the state-aware Medicaid rule (california_medical_status_2026_09_23,
STATUS_BLIND_2024). The case applies audit row 2 to that flag on the account's row-4 weights (Mexico-born outside
CA+TX at their ACS 2024 level): the stack `row4+status_state_aware|central|<method>` of cps_imputation_keys_2026_09_23
step 5e. On that frame the Mexico-born unauthorized number 4.607M. That is the frame every count here uses: CPS ASEC
2025 persons in the group (civilian), row-4 weights, full-sample column.

Who moves (the residual method's own criteria; a tier that would overshoot moves a uniform fraction theta of its
members, every whole tier before it moves in full):
  raising (DHS, CMS): legal -> unauthorized, weakest legal signal first.
    T1  legal only through the Medicaid clause (unauthorized once the clause is dropped at every state-age, the status
        lane's no_medicaid_rule; the adopted flag already drops it where 2024 coverage ignored status).
    T2  then legal only through clause (i), a legal or citizen spouse, with the Medicaid clause dropped.
    T3  then everyone else legal (not reached: the script stops if a target needs it).
  lowering (Pew): unauthorized -> legal, earliest arrival first: rule (a) presumes pre-1980 arrivals legal; the next
    arrival band (1980-81, IRCA's continuous-residence window) is the next most likely legal, then 1982-83, and so on.
Alternative (proportional): every imputed-legal Mexico-born noncitizen of the group is unauthorized with one fraction
(raising), or every imputed-unauthorized one keeps the flag with one fraction (lowering). It preserves each status
group's composition: what the calibration moves when the residual's ranking carries no information at the margin.

A fractional flag theta counts a person unauthorized with weight theta: the six scaled keys and the ACTC at
1 - theta + theta x s, the EITC at 1 - theta (s the on-books share of the person's origin, central case). At theta of 0
or 1 this is combine_status.status_vectors bit for bit.

Gates, each stopping with [BLOCKED] before anything is written:
  1. the adopted flag reproduces the California lane's union counts on the published weights, and on the row-4
     weights the CPS lane's 4.607M; every unauthorized union member is Mexico-born;
  2. each arm's total equals its target within 1,000 people, and only Mexico-born noncitizens of the group move;
  3. each hot-deck frame without the rules reproduces run_hotdeck.py's stored shares (1e-12);
  4. with the adopted flag, the rebuilt stacks equal the case's stored stacks cell for cell (1e-9 $bn):
     row4+status_state_aware|central|{b_hotdeck_union_matched, b_matched_over_pooled, audit_rules_alone}.

Writes derived/arms.csv, derived/tiers.csv, derived/movers.csv and derived/stacks.json.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/status_calibration_2026_09_30/calibrate.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import json  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
CPS = FISCAL / "cps_imputation_keys_2026_09_23"
OUT = HERE / "derived"
sys.path.insert(0, str(CPS))

import combine_onbooks_lane as ob  # noqa: E402
import combine_status as cs  # noqa: E402
import common as c  # noqa: E402
import hotdeck  # noqa: E402
import run_hotdeck  # noqa: E402
import translate  # noqa: E402
from impute_status import impute  # noqa: E402  (combine_status put status_impute_2026_09_16 on the path)

ARM = "row4+status_state_aware"
CFG = ("origin", "central")
METHODS = ["b_hotdeck_union_matched", "b_matched_over_pooled"]
STACK_NAMES = METHODS + ["audit_rules_alone"]
STORED = CPS / "_cache" / "onbooks_lane_line_deltas.json"
MEXICO = 303
TOL = 1000.0
ADOPTED_M = 4.607  # cps_imputation_keys_2026_09_23/RESULT.md:757, "Under row 4's weights the union count is 4.607M"
# Mexico-born unauthorized, external totals (mexborn_count_2026_09_23/RESULT.md:243; unauthorized lane
# derived/published_estimates.csv): Pew mid-2023 4.3M; DHS OHSS 1 January 2022, 44% of 10.99M; CMS 2024 5.1M.
TARGETS = {"pew": 4.3e6, "dhs": 4.8e6, "cms": 5.1e6}
ARRIVAL = json.loads((FISCAL / "indian_civic_cps_2026_09_18/_cache/asec_2025_PEINUSYR.json").read_text())["values"]["item"]


def blocked(msg: str):
    raise SystemExit(f"[BLOCKED] {msg}")


def aligned(s: pd.DataFrame, flag: np.ndarray, d: pd.DataFrame) -> np.ndarray:
    """A status-frame flag on d's rows (combine_status.unauthorized's alignment)."""
    f = pd.DataFrame({"PH_SEQ": s.PH_SEQ.to_numpy(), "PPPOS": s.PPPOS.to_numpy(), "x": np.asarray(flag, bool)})
    out = d[["PH_SEQ", "PPPOS"]].merge(f, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if out.x.isna().any():
        blocked("a status flag does not align with the lane frame")
    return out.x.to_numpy(bool)


def vectors_theta(frame: pd.DataFrame, theta: np.ndarray, s: np.ndarray, index: np.ndarray) -> dict:
    """combine_onbooks_lane.frame_vectors on the status keys with a fractional flag theta."""
    rv = c.receipt_vectors(frame)
    keep = 1.0 - theta + theta * s
    for k in cs.SCALED:
        rv[k] = rv[k] * keep
    f = frame.assign(EIT_CRED=frame.EIT_CRED.to_numpy(float) * (1.0 - theta),
                     ACTC_CRD=frame.ACTC_CRD.to_numpy(float) * keep)
    rk, sk = c.receipt_keys(frame, index, rv), c.spending_vectors(f, index)
    out = {}
    for a in ob.ALLOC:
        merged = {**rk[a], **sk[a]}
        out[a] = {k: merged[k] for k in cs.STATUS_KEYS}
    return out


def fill(theta0: np.ndarray, tiers: list, w: np.ndarray, delta: float, up: bool) -> tuple[np.ndarray, list]:
    """Move delta persons (weights w) through the tiers in order: whole tiers, then a uniform fraction of the tier
    that would overshoot. up: legal -> unauthorized (theta rises from 0); else unauthorized -> legal (falls from 1)."""
    th, left, used = theta0.copy(), delta, []
    for name, mask in tiers:
        if left <= 0:
            break
        size = float(w[mask].sum())
        if size <= 0:
            continue
        frac = min(1.0, left / size)
        th[mask] = frac if up else 1.0 - frac
        used.append((name, size, frac))
        left -= frac * size
        if frac < 1.0:
            break
    if left > TOL:
        blocked(f"the tiers run out {left:,.0f} persons short of the target")
    return th, used


def payload_diff(a: dict, b: dict) -> float:
    """Largest absolute difference between two stack payloads, cell by cell (a cell missing on one side counts)."""
    def flat(x, pre=()):
        if isinstance(x, dict):
            for k, y in x.items():
                yield from flat(y, pre + (k,))
        else:
            yield pre, float(x)
    fa, fb = dict(flat(a)), dict(flat(b))
    return max(abs(fa.get(k, 0.0) - fb.get(k, 0.0)) for k in set(fa) | set(fb))


def main() -> None:
    d = c.load_frame()
    civ, union = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    Wc, Wu = W[civ], W[union]
    index = c.spm_index(d)
    s_in, hh = cs.status_inputs()
    paper = cs.unauthorized(s_in, hh, d)
    aware = ob.state_aware_flag(s_in, hh, d, ob.STATUS_BLIND_2024)
    configs, labels = ob.share_configs(d)
    s = configs[CFG]
    mex = d.PENATVTY.eq(MEXICO).to_numpy()
    noncit = d.PRCITSHP.eq(5).to_numpy()
    mexu = union & mex & noncit

    # Gate 1: the adopted flag.
    counts = pd.read_csv(ob.CA_COUNTS).query("region == 'US' and group == 'union'").set_index("rules").unauthorized_millions
    got = {"paper": W[paper & union, 0].sum() / 1e6, "aware": W[aware & union, 0].sum() / 1e6}
    want = {"paper": counts["borjas_paper_rules"], "aware": counts["state_aware_verified_states"]}
    print(f"[gate 1] union unauthorized, published weights: paper {got['paper']:.4f}M (California lane "
          f"{want['paper']:.4f}M), state-aware {got['aware']:.4f}M ({want['aware']:.4f}M)", flush=True)
    if max(abs(got[k] - want[k]) for k in got) > 5.1e-5:
        blocked("the flags do not reproduce the California lane's union counts")
    if (aware & union & ~mexu).any():
        blocked("an unauthorized union member who is not a Mexico-born noncitizen")

    cells = ob.acs_cells()
    arms_w, _ = ob.weight_arms(d, W, cells)
    W4 = arms_w["row4"]
    del arms_w
    w4 = W4[:, 0]
    n0 = float(w4[aware & union].sum())
    print(f"[gate 1] Mexico-born unauthorized on the case's frame (row-4 weights, state-aware flag): {n0:,.0f} "
          f"(CPS lane {ADOPTED_M}M)", flush=True)
    if abs(n0 / 1e6 - ADOPTED_M) > 0.0005:
        blocked("the adopted flag on the row-4 weights is not the CPS lane's 4.607M")

    # Tiers.
    nm = impute(s_in, hh, use_medicaid_rule=False)
    nm_unauth, nm_own = aligned(s_in, nm["unauthorized"], d), aligned(s_in, nm["own_legal"], d)
    if (mexu & aware & ~nm_unauth).any():
        blocked("an adopted unauthorized who is legal without the Medicaid clause")
    t1 = mexu & ~aware & nm_unauth
    t2 = mexu & ~aware & ~nm_unauth & ~nm_own
    t3 = mexu & ~aware & ~t1 & ~t2
    raise_tiers = [("T1_medicaid_clause_only", t1), ("T2_spouse_clause_only", t2), ("T3_own_signal", t3)]
    arrival = d.PEINUSYR.to_numpy()
    codes = sorted({int(x) for x in arrival[mexu & aware]}, key=lambda x: (x == 0, x))
    lower_tiers = [(f"arrived_{ARRIVAL[str(k)]}", mexu & aware & (arrival == k)) for k in codes]
    for name, m in raise_tiers + lower_tiers:
        print(f"[tier] {name}: {m.sum()} records, {w4[m].sum():,.0f} persons", flush=True)

    # Arms: the adopted flag, the rule and the proportional alternative at each target.
    base_theta = aware.astype(float)
    thetas, arm_rows, tier_use = {"adopted": base_theta}, [], []
    legal_pool, unauth_pool = mexu & ~aware, mexu & aware
    for target, n in TARGETS.items():
        up = n > n0
        delta = abs(n - n0)
        th, used = fill(base_theta, raise_tiers if up else lower_tiers, w4, delta, up)
        thetas[target] = th
        tier_use += [dict(arm=target, tier=t, tier_persons=size, fraction_moved=frac) for t, size, frac in used]
        pool = legal_pool if up else unauth_pool
        frac = delta / float(w4[pool].sum())
        thp = base_theta.copy()
        thp[pool] = frac if up else 1.0 - frac
        thetas[f"{target}_proportional"] = thp
        tier_use.append(dict(arm=f"{target}_proportional", tier="adopted_legal_noncitizens" if up else "adopted_unauthorized",
                             tier_persons=float(w4[pool].sum()), fraction_moved=frac))
    for name, th in thetas.items():
        total = float(w4[union] @ th[union])
        moved = np.abs(th - base_theta) > 0
        target = TARGETS.get(name.split("_")[0], n0) if name != "adopted" else n0
        arm_rows.append(dict(arm=name, rule="adopted" if name == "adopted" else ("proportional" if "proportional" in name else "tiers"),
                             target=target, total=total, miss=total - target, adopted=n0, moved_persons=float(w4 @ np.abs(th - base_theta)),
                             moved_records=int(moved.sum())))
        print(f"[gate 2] {name}: total {total:,.0f}, target {target:,.0f}, miss {total - target:+.3f}; "
              f"{int(moved.sum())} records move", flush=True)
        if abs(total - target) > TOL:
            blocked(f"{name} misses its target by {total - target:,.0f}")
        if (moved & ~mexu).any():
            blocked(f"{name} moves someone who is not a Mexico-born noncitizen of the group")
    if "--tiers-only" in sys.argv[1:]:
        print(pd.DataFrame(arm_rows).to_string(index=False))
        print(pd.DataFrame(tier_use).to_string(index=False))
        return

    # Who moves: the tiers' profiles beside the adopted statuses (row-4 weights).
    prof = []
    val = {"age": d.A_AGE.to_numpy(float), "wage": d.WSAL_VAL.clip(lower=0).to_numpy(float),
           "federal_liability": d.FEDTAX_BC.to_numpy(float), "eitc": d.EIT_CRED.to_numpy(float),
           "actc": d.ACTC_CRD.to_numpy(float), "earner": d.WSAL_VAL.gt(0).to_numpy(float),
           "medicaid": d.MCAID.eq(1).to_numpy(float), "california": d.GESTFIPS.eq(6).to_numpy(float),
           "under_19": d.A_AGE.lt(19).to_numpy(float)}
    for name, m in [("adopted_unauthorized", mexu & aware), ("adopted_legal_noncitizens", mexu & ~aware)] + raise_tiers + lower_tiers:
        n = float(w4[m].sum())
        row = dict(group=name, records=int(m.sum()), persons=n)
        row.update({f"mean_{k}": (float(w4[m] @ v[m]) / n if n else np.nan) for k, v in val.items()})
        prof.append(row)

    # The stacks. Rules alone on the published frame, then each hot-deck frame, all on the row-4 weights.
    weights = {"published": (Wc, Wu), "row4": (W4[civ], W4[union])}
    base = cs.key_shares(d, paper, None, W, civ, union, index)
    plain4 = ob.weigh(ob.frame_vectors(d, paper, None, index), *weights["row4"], civ, union)
    audit = {name: ob.weigh(vectors_theta(d, th, s, index), *weights["row4"], civ, union, cs.STATUS_KEYS, plain4)
             for name, th in thetas.items()}

    model = json.loads(translate.MODEL.read_text())
    mts = json.loads(ob.MTS.read_text())
    line = next(x for x in model["spending"]["lines"] if x["id"] == ob.REFUNDABLE)
    f_new = mts["non_ptc_remainder_bn"] / line["national_bn"]
    hf = translate.household_fraction(d)
    meps = ob.meps_vectors(d)
    rk_pub = c.receipt_keys(d, index)
    ages = {k: c.spending_vectors(d, index)["personal"][k] for k in ["age5_24", "age18_24"]}
    published_ages = {k: (v[union] @ Wu) / (v[civ] @ Wc) for k, v in ages.items()}
    lines_by_id = {x["id"]: x for x in model["spending"]["lines"]}
    school = {(a, k): lines_by_id[ln]["keys"][k][a]["share"] for ln, k in
              [("education_services", "education_mix"), ("education_services", "school_operating"),
               ("education_benefits", "postsecondary")] for a in ob.ALLOC}
    extra_w = {w: ob.extra_shares(meps, rk_pub["shared"]["adults"], ages, *weights[w], civ, union, published_ages, school)
               for w in weights}
    po_fraction = ob.justice_per_head_fraction(model)
    uc = json.loads(ob.UC.read_text())
    exposure = ob.uninsured_exposure(d)
    plain_w = {"published": base, "row4": plain4}

    def uc_ends(wname):
        Wc_v, Wu_v = weights[wname]
        share = (exposure[union] @ Wu_v) / (exposure[civ] @ Wc_v)
        ratios = {p: extra_w[wname][("personal", k)] / extra_w["published"][("personal", k)] if k != "population"
                  else plain_w[wname][("personal", "population")] / base[("personal", "population")]
                  for p, k in ob.UC_KEYS.items()}
        return share, ob.undercharged(uc, share, ratios)

    _, (uc_low, uc_high) = uc_ends("published")
    _, (lo, hi) = uc_ends("row4")
    uc_rows = [dict(side="spending", line=ob.MEDICAID_LINE, key="medicaid", allocation=a, preferred=True, direct=False,
                    response_class="household_transfer", target_bn=pub[0], reps=new - pub,
                    source="uncompensated-care shift (uninsured use)")
               for a, new, pub in [("shared", lo, uc_low), ("personal", hi, uc_high)]]
    base_fixed = {**base, **extra_w["published"]}

    def stack(shares: dict) -> dict:
        """combine_onbooks_lane.main's stack() for the row-4 variant, as a Node payload."""
        rows = translate.line_deltas(model, base_fixed, {**shares, **extra_w["row4"]}, hf)
        rows = [dict(x, source="account key (MEPS medicare or unit-split adults)")
                if ob.lane_of(x["side"], x["key"], x["allocation"]) != x["key"] else x for x in rows]
        rows = [dict(x, reps=x["reps"] * po_fraction, source="per-head part of the justice use key")
                if x["side"] == "spending" and x["line"] == "public_order_safety" and x["key"] == "population"
                else x for x in rows]
        rows = rows + uc_rows
        rows = [dict(x, reps=x["reps"] * f_new) if x["line"] == ob.REFUNDABLE else x for x in rows]
        return ob.payload_from_rows(rows)

    hd = np.load(c.CACHE / "hotdeck_key_shares.npz")
    runs = {"matched": [], "pooled": []}
    _, seeds = run_hotdeck.SPECS["main"]
    for seed in seeds:
        for variant, cells_ in [("matched", hotdeck.BASE), ("pooled", [])]:
            print(f"[hot deck] seed {seed} {variant}", flush=True)
            new, _ = hotdeck.run(d, seed=seed, verbose=False, base=cells_, item_property=False)
            if not (new[["PH_SEQ", "PPPOS"]].to_numpy() == d[["PH_SEQ", "PPPOS"]].to_numpy()).all():
                blocked("hot-deck frame rows do not align with the lane frame")
            plain = cs.key_shares(new, paper, None, W, civ, union, index)
            gap = max(np.abs(plain[k] - hd[f"main|{variant}@{seed}|{k[0]}|{k[1]}"]).max() for k in plain)
            if gap > 1e-12:
                blocked(f"gate 3: hot-deck shares not reproduced for seed {seed} {variant}: {gap:.2e}")
            p_v = ob.weigh(ob.frame_vectors(new, paper, None, index), *weights["row4"], civ, union)
            runs[variant].append({name: ob.weigh(vectors_theta(new, th, s, index), *weights["row4"], civ, union,
                                                 cs.STATUS_KEYS, p_v) for name, th in thetas.items()})
    print("[gate 3] every hot-deck frame reproduces run_hotdeck.py's stored shares (1e-12)", flush=True)

    stacks = {}
    for name in thetas:
        m = cs.mean_shares([r[name] for r in runs["matched"]])
        p = cs.mean_shares([r[name] for r in runs["pooled"]])
        ref = audit[name]
        stacks[name] = {"b_hotdeck_union_matched": stack(m),
                        "b_matched_over_pooled": stack({k: ref[k] * m[k] / p[k] for k in ref}),
                        "audit_rules_alone": stack(ref)}

    # Gate 4: the adopted flag rebuilds the case's stacks.
    stored = json.loads(STORED.read_text())
    worst = {k: payload_diff(stacks["adopted"][k], stored[f"{ARM}|central|{k}"]) for k in STACK_NAMES}
    print(f"[gate 4] adopted flag vs the case's stored stacks, largest cell difference: "
          + ", ".join(f"{k} {v:.1e}" for k, v in worst.items()), flush=True)
    if max(worst.values()) > 1e-9:
        blocked("the adopted flag does not rebuild the case's stacks")

    # Outputs.
    OUT.mkdir(exist_ok=True)
    pd.DataFrame(arm_rows).to_csv(OUT / "arms.csv", index=False, lineterminator="\n", float_format="%.6f")
    tiers = pd.DataFrame(prof).merge(pd.DataFrame(tier_use).rename(columns={"tier": "group"}), on="group", how="outer")
    tiers.to_csv(OUT / "tiers.csv", index=False, lineterminator="\n", float_format="%.6f")
    ids = d[["PH_SEQ", "PPPOS"]].merge(s_in[["PH_SEQ", "PPPOS", "A_LINENO"]], on=["PH_SEQ", "PPPOS"], how="left",
                                         validate="one_to_one")
    movers = []
    for name, th in thetas.items():
        m = np.flatnonzero(np.abs(th - base_theta) > 0)
        movers.append(pd.DataFrame({"arm": name, "PH_SEQ": ids.PH_SEQ.to_numpy()[m], "PPPOS": ids.PPPOS.to_numpy()[m],
                                    "A_LINENO": ids.A_LINENO.to_numpy()[m], "adopted": base_theta[m], "theta": th[m],
                                    "weight_row4": w4[m], "weight_published": W[m, 0]}))
    pd.concat(movers).to_csv(OUT / "movers.csv", index=False, lineterminator="\n", float_format="%.12g")
    meta = {"frame": "CPS ASEC 2025 persons in the group (civilian), row-4 weights (cps_imputation_keys_2026_09_23 "
                     "weight_arms 'row4'), full-sample column; status = the state-aware flag (STATUS_BLIND_2024)",
            "adopted_total": n0, "targets": TARGETS, "on_books_central": {"mexico_born": labels[CFG][0], "other_latin": labels[CFG][1]},
            "non_ptc_fraction": f_new, "stored_stacks": str(STORED.relative_to(FISCAL)), "gate_4_largest_difference_bn": worst}
    (OUT / "stacks.json").write_text(json.dumps({"meta": meta, "stacks": stacks}, indent=1, sort_keys=True) + "\n")
    print(pd.DataFrame(arm_rows).to_string(index=False), flush=True)
    print(tiers.round(3).to_string(index=False), flush=True)


if __name__ == "__main__":
    main()
