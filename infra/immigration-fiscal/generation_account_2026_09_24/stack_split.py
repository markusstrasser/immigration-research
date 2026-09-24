"""Step 4, tax-records block: the CPS lane's adopted stack split exactly by generation.

The package's first block (`package.cjs` stackShifts) is the CPS lane's stack
`row4+status_state_aware|central|<method>` for the fill-in methods b_hotdeck_union_matched and
b_matched_over_pooled (`cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`). Every line moves by
national_bn (times the household fraction on spending) x (new union key share - published union
share), and a union key share is the union's key total over the national total. A generation's share
is its own key total over the same national total, so the generation shares add to the union's and
each line change splits exactly. This script recomputes the lane's shares with the lane's own
functions (imported read-only), once for the union and once with each generation in its place:

- A: the status rules at the on-books lane's central origin shares (paper flag, published weights);
- B: the state-aware status flag in place of the paper flag;
- C: audit row 4's weights (Mexico-born outside CA+TX scaled to the ACS), with every CPS-weighted
  input the lane recomputes under them (MEPS payer keys, unit-split adults, the school keys through
  their age proxy, the per-head part of the justice use key, the uncompensated-care shift);
- D: the two fill-in methods on top: the union-matched hot deck (5 seeds) and the same net of its
  pooled-donor control. The hot deck redraws only imputed records, so a generation's part of D is
  the change in its own imputed records plus its part of the national re-normalization: the brief's
  "generation make-up of the imputed records", weighted by how far each record's values moved. The
  ratio method (ref x m / p) splits as ref x (m_g - p_g) / p, which adds to the union's change.

The status rules change only the audit's unauthorized, who in the union are all Mexico-born, but the
line's national total is fixed, so the other generations' shares move through the denominator. The
uncompensated-care shift is g x (s - k) x n at the arm that sets each end of the lane's range; each
generation takes its own s and k at that same arm. Both conventions are computed: in (b) a minor
counts in the parents' generation, and a minor with parents in two generations counts half in each,
so each generation's payload is its whole members' plus half its half members' (the lane's shares are
linear in the member set).

Gates (exit 1): each convention's generation weights partition the lane frame's union; each hot-deck
run reproduces the lane's stored union shares; for the union the recomputed payloads equal the stored
ones (`_cache/onbooks_lane_line_deltas.json`, 1e-9 bn per cell); under each convention the three
generations add to the union in every cell (1e-9 bn).
Output: derived/stack_by_generation.json (payloads by generation for each stored stack and the four
components). About 15 minutes: ten hot-deck runs. `--no-hotdeck` stops after A, B and C.
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/stack_split.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import hashlib  # noqa: E402
import json  # noqa: E402

import numpy as np  # noqa: E402

import frame as F  # noqa: E402  (puts the CPS lane on sys.path)
import combine_onbooks_lane as L  # noqa: E402
import combine_status as cs  # noqa: E402
import hotdeck  # noqa: E402
import run_hotdeck  # noqa: E402
import translate  # noqa: E402

c = F.C
CFG = ("origin", "central")
V = "row4+status_state_aware"
METHODS = ["b_hotdeck_union_matched", "b_matched_over_pooled"]
STORED = {"A_rules_paper": "origin|central|audit_rules_alone",
          "rules_state_aware": "status_state_aware|central|audit_rules_alone",
          "rules_row4_state_aware": f"{V}|central|audit_rules_alone",
          **{m: f"{V}|central|{m}" for m in METHODS}}
CACHE_FILE = c.CACHE / "onbooks_lane_line_deltas.json"
COLS = ["pwwgt0", "pwwgt1"]  # the full-sample weight (column 0) and one replicate the lane's printing needs
FAILS = []


def gate(label, ok, detail=""):
    print(f"  {'✓' if ok else '✗'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def cells_of(payload):
    """{(side, line, key, allocation): value} for a Node payload (receipt key None)."""
    out = {}
    for line, by in payload.get("receipts", {}).items():
        for a, v in by.items():
            out[("receipts", line, None, a)] = v
    for line, keys in payload.get("spending", {}).items():
        for key, by in keys.items():
            for a, v in by.items():
                out[("spending", line, key, a)] = v
    return out


def combine(payloads, weights):
    """Sum of payloads times weights, cell by cell (missing cells count as 0)."""
    out = {"receipts": {}, "spending": {}}
    for p, f in zip(payloads, weights):
        for (side, line, key, a), v in cells_of(p).items():
            cell = out[side].setdefault(line, {}) if side == "receipts" else \
                out[side].setdefault(line, {}).setdefault(key, {})
            cell[a] = cell.get(a, 0.0) + f * v
    return out


def worst_gap(p, q):
    a, b = cells_of(p), cells_of(q)
    return max(abs(a.get(k, 0.0) - b.get(k, 0.0)) for k in set(a) | set(b))


def generation_weights(d):
    """Each convention's generation weights (n x 3; F.assignments) on the CPS lane's rows."""
    g = F.load()
    civ, union, gens = F.masks(g)
    omega, _, _ = F.assignments(g, civ, union, gens)
    cols = {f"{conv}{j}": omega[conv][:, j] for conv in omega for j in range(3)}
    keys = g[["PH_SEQ", "PPPOS"]].assign(**cols)
    m = d[["PH_SEQ", "PPPOS"]].merge(keys, on=["PH_SEQ", "PPPOS"], how="left", validate="one_to_one")
    if m[list(cols)].isna().any().any():
        raise SystemExit("[BLOCKED] generation weights do not align with the CPS lane's frame")
    return {conv: np.column_stack([m[f"{conv}{j}"].to_numpy(float) for j in range(3)]) for conv in omega}


def mask_set(union, omega):
    """Boolean masks whose payloads combine linearly into each convention's generations: convention
    (a) is 0/1; convention (b) gives a minor with parents in two generations half to each, so each
    generation is its whole members plus half its half members."""
    masks, recipe = {"union": union}, {}
    for conv, om in omega.items():
        if not np.all(np.isin(om, [0.0, 0.5, 1.0])):
            raise SystemExit(f"[BLOCKED] convention {conv} weights other than 0, 1/2 and 1")
        for j, g in enumerate(F.GENS):
            masks[f"{conv}1|{g}"] = om[:, j] == 1.0
            half = om[:, j] == 0.5
            recipe[(conv, g)] = [(f"{conv}1|{g}", 1.0)]
            if half.any():
                masks[f"{conv}h|{g}"] = half
                recipe[(conv, g)].append((f"{conv}h|{g}", 0.5))
    return masks, recipe


def main():
    no_hotdeck = "--no-hotdeck" in sys.argv[1:]
    raw = CACHE_FILE.read_bytes()
    stored = json.loads(raw)
    d = c.load_frame()
    civ, union = c.masks(d)
    omega = generation_weights(d)
    for conv, om in omega.items():
        gate(f"({conv}) generation weights partition the lane frame's union",
             np.allclose(om[union].sum(axis=1), 1) and not om[~union].any())
    masks, recipe = mask_set(union, omega)
    W = d[COLS].to_numpy(float)
    index = c.spm_index(d)
    s_in, hh = cs.status_inputs()
    unauth = cs.unauthorized(s_in, hh, d)
    aware = L.state_aware_flag(s_in, hh, d, L.STATUS_BLIND_2024)
    configs, _ = L.share_configs(d)
    share = configs[CFG]
    model = json.loads(translate.MODEL.read_text())
    mts = json.loads(L.MTS.read_text())
    f_new = mts["non_ptc_remainder_bn"] / next(x for x in model["spending"]["lines"] if x["id"] == L.REFUNDABLE)["national_bn"]
    hf = W[civ].sum(axis=0) / c.RESIDENT  # translate.household_fraction on these columns
    po_fraction = L.justice_per_head_fraction(model)
    cells = L.acs_cells()
    arms_w, _ = L.weight_arms(d, W, cells)
    W4 = arms_w["row4"]
    del arms_w
    weights = {"published": W, "row4": W4}

    vec_paper = L.frame_vectors(d, unauth, share, index, cs.STATUS_KEYS)
    vec_aware = L.frame_vectors(d, aware, share, index, cs.STATUS_KEYS)
    everything = L.frame_vectors(d, unauth, None, index)
    meps = L.meps_vectors(d)
    adults_unit = c.receipt_keys(d, index)["shared"]["adults"]
    ages = {k: c.spending_vectors(d, index)["personal"][k] for k in ["age5_24", "age18_24"]}
    published_ages = {k: (v[union] @ W[union]) / (v[civ] @ W[civ]) for k, v in ages.items()}
    lines_by_id = {x["id"]: x for x in model["spending"]["lines"]}
    school = {(a, k): lines_by_id[ln]["keys"][k][a]["share"] for ln, k in
              [("education_services", "education_mix"), ("education_services", "school_operating"),
               ("education_benefits", "postsecondary")] for a in L.ALLOC}
    uc = json.loads(L.UC.read_text())
    exposure = L.uninsured_exposure(d)

    sh = {}
    for name, M in masks.items():
        base = L.weigh(everything, W[civ], W[M], civ, M)  # = cs.key_shares(d, unauth, None, ...), gated below
        extra = {w: L.extra_shares(meps, adults_unit, ages, Wv[civ], Wv[M], civ, M, published_ages, school)
                 for w, Wv in weights.items()}
        plain4 = L.weigh(everything, W4[civ], W4[M], civ, M)
        sh[name] = dict(
            base=base, extra=extra, plain={"published": base, "row4": plain4},
            paper=L.weigh(vec_paper, W[civ], W[M], civ, M, cs.STATUS_KEYS, base),
            aware=L.weigh(vec_aware, W[civ], W[M], civ, M, cs.STATUS_KEYS, base),
            row4=L.weigh(vec_aware, W4[civ], W4[M], civ, M, cs.STATUS_KEYS, plain4))

    def uc_values(name, wname):
        """uncompensated_care's eight arm values g x (s - k) x n for one mask under one weight set;
        each account key share is the union's published key share times this mask's key share over
        the union's published key share (so the masks add to the union)."""
        M, Wv, s_u = masks[name], weights[wname], sh["union"]
        s = (exposure[M] @ Wv[M]) / (exposure[civ] @ Wv[civ])
        ratios = {p: sh[name]["extra"][wname][("personal", k)] / s_u["extra"]["published"][("personal", k)]
                  if k != "population" else
                  sh[name]["plain"][wname][("personal", "population")] / s_u["base"][("personal", "population")]
                  for p, k in L.UC_KEYS.items()}
        aha, uplift = uc["aha_national_bn"], uc["uplift_2024"]
        keys = {p: uc["account_key_shares"][p] * ratios[p] for p in L.UC_KEYS}
        values = []
        for spec in L.UC_OFFSETS.values():
            total_off = sum(spec["programs"].values())
            g = total_off / spec["total_uc"]
            for state_local_key in ("health_other", "per_head"):
                k = sum(v / total_off * keys[state_local_key if p == "state_local" else p] for p, v in spec["programs"].items())
                for n in (aha, aha * uplift):
                    values.append(g * (s - k) * n)
        return np.array(values)

    pub_u, new_u = uc_values("union", "published"), uc_values("union", "row4")
    ends = {"shared": (int(np.argmin(pub_u[:, 0])), int(np.argmin(new_u[:, 0]))),
            "personal": (int(np.argmax(pub_u[:, 0])), int(np.argmax(new_u[:, 0])))}
    adopted_uc = json.loads(L.MAIN_INPUTS.read_text())["uncompensated_inside_bn"]
    gate("uncompensated-care arms reproduce the adopted inside under-charge",
         max(abs(pub_u[ends["shared"][0], 0] - adopted_uc["equal_low"]),
             abs(pub_u[ends["personal"][0], 0] - adopted_uc["equal_high"])) < 1e-9,
         f"{pub_u[ends['shared'][0], 0]:.4f}-{pub_u[ends['personal'][0], 0]:.4f}bn")

    def uc_rows(name):
        pub, new = uc_values(name, "published"), uc_values(name, "row4")
        return [dict(side="spending", line=L.MEDICAID_LINE, key="medicaid", allocation=a, preferred=True,
                     direct=False, response_class="household_transfer", target_bn=0.0,
                     reps=new[ends[a][1]] - pub[ends[a][0]]) for a in ("shared", "personal")]

    def stack(name, shares, wname):
        """combine_onbooks_lane.main's stack(): line deltas against the published account."""
        s = sh[name]
        base_fixed = {**s["base"], **s["extra"]["published"]}
        rows = translate.line_deltas(model, base_fixed, {**shares, **s["extra"][wname]}, hf)
        rows = [dict(x, reps=x["reps"] * po_fraction)
                if x["side"] == "spending" and x["line"] == "public_order_safety" and x["key"] == "population" else x
                for x in rows]
        if wname != "published":
            rows = rows + uc_rows(name)
        rows = [dict(x, reps=x["reps"] * f_new) if x["line"] == L.REFUNDABLE else x for x in rows]
        return L.payload_from_rows(rows)

    payloads = {k: {} for k in STORED}
    for name in masks:
        s = sh[name]
        payloads["A_rules_paper"][name] = L.payload_for(model, s["base"], s["paper"], hf, f_new)
        payloads["rules_state_aware"][name] = stack(name, s["aware"], "published")
        payloads["rules_row4_state_aware"][name] = stack(name, s["row4"], "row4")

    if not no_hotdeck:
        hd = np.load(c.CACHE / "hotdeck_key_shares.npz")
        runs = {"matched": [], "pooled": []}
        seeds = run_hotdeck.SPECS["main"][1]
        for i, seed in enumerate(seeds):
            for variant, cells_ in [("matched", hotdeck.BASE), ("pooled", [])]:
                print(f"[hotdeck] [{2 * i + (variant == 'pooled') + 1}/{2 * len(seeds)}] seed {seed} {variant}", flush=True)
                new, _ = hotdeck.run(d, seed=seed, verbose=False, base=cells_, item_property=False)
                if not (new[["PH_SEQ", "PPPOS"]].to_numpy() == d[["PH_SEQ", "PPPOS"]].to_numpy()).all():
                    raise SystemExit("[BLOCKED] hot-deck frame rows do not align with the lane frame")
                plain = cs.key_shares(new, unauth, None, W, civ, union, index)
                gap = max(abs(plain[k][0] - hd[f"main|{variant}@{seed}|{k[0]}|{k[1]}"][0]) for k in plain)
                gate(f"hot deck seed {seed} {variant} reproduces the lane's stored union shares", gap < 1e-12, f"{gap:.1e}")
                all_new = L.frame_vectors(new, unauth, None, index)
                rules_new = L.frame_vectors(new, aware, share, index, cs.STATUS_KEYS)
                per = {}
                for name, M in masks.items():
                    p_v = L.weigh(all_new, W4[civ], W4[M], civ, M)
                    per[name] = L.weigh(rules_new, W4[civ], W4[M], civ, M, cs.STATUS_KEYS, p_v)
                runs[variant].append(per)
                del new, all_new, rules_new
        m = {name: cs.mean_shares([r[name] for r in runs["matched"]]) for name in masks}
        p = {name: cs.mean_shares([r[name] for r in runs["pooled"]]) for name in masks}
        ref_u, p_u = sh["union"]["row4"], p["union"]
        for name in masks:
            ref = sh[name]["row4"]
            ratio = {}
            for k in ref:
                if np.any(p_u[k] == 0):
                    if np.any(m[name][k] != p[name][k]):
                        raise SystemExit(f"[BLOCKED] pooled union share zero with a matched change for {k}")
                    ratio[k] = ref[k]
                else:
                    ratio[k] = ref[k] + ref_u[k] * (m[name][k] - p[name][k]) / p_u[k]
            payloads["b_hotdeck_union_matched"][name] = stack(name, m[name], "row4")
            payloads["b_matched_over_pooled"][name] = stack(name, ratio, "row4")

    # Each convention's generations from the mask payloads.
    by_conv = {}
    for key, per in payloads.items():
        if not per:
            continue
        gap = worst_gap(per["union"], stored[STORED[key]])
        gate(f"{STORED[key]}: the union reproduces the stored payload", gap < 1e-9, f"max |diff| {gap:.1e} bn")
        for conv in omega:
            gen = {g: combine([per[m] for m, _ in recipe[(conv, g)]], [f for _, f in recipe[(conv, g)]]) for g in F.GENS}
            gap = worst_gap(combine([gen[g] for g in F.GENS], [1.0] * 3), per["union"])
            gate(f"{STORED[key]} ({conv}): the three generations add to the union", gap < 1e-9, f"max |diff| {gap:.1e} bn")
            by_conv.setdefault(key, {"union": per["union"]})[conv] = gen

    # Components by generation: A, B = state-aware - paper, C = row 4 on top, D per method.
    comps = {}
    for conv in ["union", *omega]:
        for g in (["union"] if conv == "union" else F.GENS):
            P = {k: (v["union"] if conv == "union" else v[conv][g]) for k, v in by_conv.items()}
            parts = {"A_status_rules": P["A_rules_paper"],
                     "B_state_aware_flag": combine([P["rules_state_aware"], P["A_rules_paper"]], [1, -1]),
                     "C_row4_weights": combine([P["rules_row4_state_aware"], P["rules_state_aware"]], [1, -1])}
            for meth in METHODS:
                if meth in P:
                    parts[f"D_{meth}"] = combine([P[meth], P["rules_row4_state_aware"]], [1, -1])
            for comp, payload in parts.items():
                comps.setdefault(comp, {}).setdefault(conv, {})[g] = payload
    out = dict(meta=dict(source=str(CACHE_FILE.relative_to(F.FISCAL)), source_sha256=hashlib.sha256(raw).hexdigest(),
                         stacks=STORED, case="central, origin on-books shares", non_ptc_fraction=f_new,
                         household_fraction=float(hf[0]), justice_per_head_fraction=po_fraction,
                         uc_arms={a: dict(published=e[0], row4=e[1]) for a, e in ends.items()},
                         hotdeck_seeds=None if no_hotdeck else run_hotdeck.SPECS["main"][1],
                         layout="payloads[stack][union | a | b][generation]; components[name][union | a | b][generation]"),
               payloads=by_conv, components=comps)
    if no_hotdeck:
        print("[stack] --no-hotdeck: A, B and C only; nothing written")
    else:
        (F.OUT / "stack_by_generation.json").write_text(json.dumps(out, sort_keys=True) + "\n")
    for comp, per in comps.items():
        for conv in omega:
            line = "; ".join(f"{g} {sum(v for k, v in cells_of(per[conv][g]).items() if k[3] == 'personal'):+.3f}"
                             for g in F.GENS)
            union_sum = sum(v for k, v in cells_of(per["union"]["union"]).items() if k[3] == "personal")
            print(f"  {comp} ({conv}): sum of personal cell changes, $bn: union {union_sum:+.3f}; {line}", flush=True)
    if FAILS:
        print(f"✗ {len(FAILS)} gate(s) failed: {FAILS}")
        sys.exit(1)
    print("  ✓ all stack gates passed")


if __name__ == "__main__":
    main()
