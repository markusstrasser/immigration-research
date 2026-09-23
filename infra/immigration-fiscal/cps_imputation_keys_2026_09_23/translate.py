"""Step 5 (Python half): key-share changes -> line and component changes, with replicate SEs.

For each method, every receipt line (cbo_collective) and spending line key that uses a
perturbed CPS key moves by national_bn x (new share - published share); spending lines also
carry the household pool fraction, as in the spending builder. Components follow the main
case's formula: welfare = direct receipts - transfers - sum(response x services) + P + F, with
transfers and income-security services at response 1, economic affairs at 0 (delayed) in the
CBO-lag profiles, subsidies and capital-incidence receipts at 0.
Writes derived/line_deltas.json (read by main_case_translate.js), derived/line_deltas.csv and
derived/component_deltas.csv, then runs the Node translation.
"""
from __future__ import annotations

import json
import subprocess
import sys

import numpy as np
import pandas as pd

import common as c

MODEL = c.FISCAL / "assumption_explorer_2026_09_21/derived/model.json"


def ipw_methods():
    z = np.load(c.CACHE / "ipw_key_shares.npz")
    base, methods = {}, {}
    for name in z.files:
        parts = name.split("|")
        if parts[0] == "base":
            base[(parts[1], parts[2])] = z[name]
    main = {(p.split("|")[2], p.split("|")[3]): z[p] for p in z.files if p.startswith("a_brief_cells|material_5pct|")}
    lf = {(p.split("|")[2], p.split("|")[3]): z[p] for p in z.files if p.startswith("a_plus_labor_force|material_5pct|")}
    methods["a_ipw_brief_cells"] = main
    methods["a_ipw_plus_labor_force"] = lf
    for rule in ["material_1pct", "any_flag"]:
        m = dict(main)
        m.update({(p.split("|")[2], p.split("|")[3]): z[p] for p in z.files if p.startswith(f"a_brief_cells|{rule}|")})
        methods[f"a_ipw_brief_cells_derived_{rule}"] = m
    return base, methods


def hotdeck_methods():
    path = c.CACHE / "hotdeck_key_shares.npz"
    if not path.exists():
        return {}
    z = np.load(path)
    methods = {}
    for spec, variant, label in [("main", "matched", "b_hotdeck_union_matched"),
                                 ("main", "pooled", "b_control_pooled_donors"),
                                 ("main", "match_effect", "b_matched_over_pooled"),
                                 ("all_items", "matched", "b_hotdeck_union_matched_all_items"),
                                 ("all_items", "match_effect", "b_matched_over_pooled_all_items")]:
        prefix = f"{spec}|{variant}|"
        methods[label] = {(n.split("|")[2], n.split("|")[3]): z[n] for n in z.files if n.startswith(prefix)}
    return methods


def hotdeck_seeds():
    """Per-seed key shares: {(label, seed): method}; match effect per seed = base x matched / pooled."""
    path = c.CACHE / "hotdeck_key_shares.npz"
    if not path.exists():
        return {}
    z = np.load(path)
    per = {}
    for name in z.files:
        head, a, k = name.rsplit("|", 2) if name.count("|") == 3 else (None, None, None)
        if head is None or "@" not in head:
            continue
        spec, rest = head.split("|")
        variant, seed = rest.split("@")
        per.setdefault((spec, variant, int(seed)), {})[(a, k)] = z[name]
    out = {}
    for (spec, variant, seed), shares in per.items():
        if variant != "matched":
            continue
        pooled = per[(spec, "pooled", seed)]
        suffix = "" if spec == "main" else f"_{spec}"
        out[(f"b_hotdeck_union_matched{suffix}", seed)] = shares
        out[(f"b_matched_over_pooled{suffix}", seed)] = {key: z[f"base|{key[0]}|{key[1]}"] * shares[key] / pooled[key]
                                                         for key in shares}
    return out


def line_deltas(model, base, method, hf):
    rows = []
    for line in model["receipts"]["lines"]:
        for a in ["personal", "shared"]:
            cell = line["cells"]["cbo_collective"][a]
            k = (a, cell["key"])
            if k in method:
                d = line["national_bn"] * (method[k] - base[k])
                rows.append(dict(side="receipts", line=line["id"], key=cell["key"], allocation=a,
                                 preferred=True, direct=bool(cell["direct"]), response_class=cell["response_class"],
                                 target_bn=cell["target_bn"], reps=d))
    for line in model["spending"]["lines"]:
        for key, cells in line["keys"].items():
            for a in ["personal", "shared"]:
                k = (a, key)
                if k in method:
                    d = line["national_bn"] * hf * (method[k] - base[k])
                    rows.append(dict(side="spending", line=line["id"], key=key, allocation=a,
                                     preferred=key == line["preferred_key"], direct=False,
                                     response_class=line["response_class"], target_bn=cells[a]["target_bn"], reps=d))
    return rows


def components(rows, delayed):
    out = {}
    for a in ["personal", "shared"]:
        r = [x for x in rows if x["allocation"] == a and x["preferred"]]
        z = np.zeros(161)
        dr = sum((x["reps"] for x in r if x["side"] == "receipts" and x["direct"]), z)
        ind = sum((x["reps"] for x in r if x["side"] == "receipts" and not x["direct"]), z)
        tr = sum((x["reps"] for x in r if x["side"] == "spending" and x["response_class"] == "household_transfer"), z)
        inc = sum((x["reps"] for x in r if x["line"] == "income_security_services"), z)
        eco = sum((x["reps"] for x in r if x["line"] == "economic_affairs_services"), z)
        sub = sum((x["reps"] for x in r if x["side"] == "spending" and x["response_class"] == "subsidy"), z)
        welfare = dr - tr - inc - delayed * eco
        out[a] = dict(direct_receipts=dr, incidence_receipts=ind, transfers=tr, income_security_services=inc,
                      economic_affairs_services=eco, subsidies=sub, net_cost_change=-welfare)
    return out


def household_fraction(d):
    """Household pool fraction under all 161 weights (the spending builder's hf)."""
    civ, _ = c.masks(d)
    W = d[c.REPS].to_numpy(float)
    return W[civ].sum(axis=0) / c.RESIDENT


def translate(model, base, methods, hf):
    """Per method: the Node payload, line rows and component rows (both profiles)."""
    payload, line_rows, comp_rows = {}, [], []
    for name, method in methods.items():
        rows = line_deltas(model, base, method, hf)
        payload[name] = {"receipts": {}, "spending": {}}
        for x in rows:
            point = float(x["reps"][0])
            if x["side"] == "receipts":
                payload[name]["receipts"].setdefault(x["line"], {})[x["allocation"]] = point
            else:
                payload[name]["spending"].setdefault(x["line"], {}).setdefault(x["key"], {})[x["allocation"]] = point
            line_rows.append(dict(method=name, side=x["side"], line=x["line"], key=x["key"], allocation=x["allocation"],
                                  preferred=x["preferred"], direct=x["direct"], response_class=x["response_class"],
                                  published_target_bn=x["target_bn"], change_bn=point, change_se_bn=c.sdr(x["reps"])))
        for profile, delayed in [("cbo_lag", 0.0), ("proportional", 1.0)]:
            for a, comps in components(rows, delayed).items():
                for comp, reps in comps.items():
                    comp_rows.append(dict(method=name, profile=profile, allocation=a, component=comp,
                                          change_bn=float(reps[0]), se_bn=c.sdr(reps)))
    return payload, line_rows, comp_rows


def run_node(deltas_path, out_path):
    """Adopted main-case bands for every method in deltas_path (gated against the published bands)."""
    done = subprocess.run(["node", str(c.HERE / "main_case_translate.js"), str(deltas_path), str(out_path)],
                          text=True, capture_output=True)
    print(done.stdout + done.stderr, flush=True)
    if done.returncode:
        sys.exit(done.returncode)


def main(extra_methods=None):
    model = json.loads(MODEL.read_text())
    hf = household_fraction(c.load_frame())
    base, methods = ipw_methods()
    methods.update(hotdeck_methods())
    if extra_methods:
        methods.update(extra_methods)
    payload, line_rows, comp_rows = translate(model, base, methods, hf)
    # Hot-deck imputation variance: spread of the per-seed full-sample changes, combined with the
    # replicate SE by Rubin's rule, T = W + (1 + 1/M) B.
    per_seed = {}
    for (label, seed), method in hotdeck_seeds().items():
        for a, comps in components(line_deltas(model, base, method, hf), 0.0).items():
            for comp in ["direct_receipts", "transfers", "income_security_services", "net_cost_change"]:
                per_seed.setdefault((label, a, comp), []).append(float(comps[comp][0]))
    spread_rows = []
    for (label, a, comp), values in sorted(per_seed.items()):
        ref = next(r for r in comp_rows if r["method"] == label and r["profile"] == "cbo_lag"
                   and r["allocation"] == a and r["component"] == comp)
        m, b = len(values), float(np.var(values, ddof=1))
        spread_rows.append(dict(method=label, allocation=a, component=comp, seeds=m, change_bn=ref["change_bn"],
                                mean_of_seeds_bn=float(np.mean(values)), replicate_se_bn=ref["se_bn"],
                                between_seed_sd_bn=b ** 0.5,
                                total_se_bn=(ref["se_bn"] ** 2 + (1 + 1 / m) * b) ** 0.5))
    if spread_rows:
        spread = pd.DataFrame(spread_rows)
        spread.to_csv(c.OUT / "hotdeck_seed_spread.csv", index=False)
        print(spread.query("component == 'net_cost_change'").round(3).to_string(index=False), flush=True)
    (c.OUT / "line_deltas.json").write_text(json.dumps(payload, indent=1) + "\n")
    pd.DataFrame(line_rows).to_csv(c.OUT / "line_deltas.csv", index=False)
    comp = pd.DataFrame(comp_rows)
    comp.to_csv(c.OUT / "component_deltas.csv", index=False)
    show = comp.query("profile == 'cbo_lag'").pivot_table(index=["method", "component"], columns="allocation",
                                                           values=["change_bn", "se_bn"])
    print(show.round(2).to_string(), flush=True)
    run_node(c.OUT / "line_deltas.json", c.OUT / "main_case_translation.csv")


if __name__ == "__main__":
    main()
