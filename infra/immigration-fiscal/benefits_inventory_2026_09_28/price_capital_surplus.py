"""Capital owners' gain from the union's labour (the "immigration surplus").

Runs the account's own production model (matched_benefits_2026_09_19/model.py, imported by path, never
copied) at capital adjustment 0 (fixed), .5 and 1 (the engine's reference), on the lane's CPS ASEC 2025
earnings pools (skill_composition.csv, point estimates). The increment of fixed over fully adjusted
capital is the short-run capital-owner gain the adopted case leaves out; at full adjustment the net
capital gain is zero by construction (released capital earns its rental rate elsewhere).

Normalized rows repeat the run for as many average residents: the union's headcount share of the
civilian population supplying that share of every earnings pool (average skill mix, average earnings).

Also computes NAS (2017, ch. 4) / Borjas (1995) homogeneous-labour surplus, E = 0.5 * s * |e| * m^2 * Y,
with e = -(1 - s) as NAS sets it (s .65 -> e -.35) and m the union's share of efficiency units (earnings).

Outputs: derived/capital_surplus_grid.csv, derived/capital_surplus_summary.json.
"""
import csv
import importlib.util
import itertools
import json
import pathlib

import numpy as np

LANE = pathlib.Path(__file__).resolve().parent
FISCAL = LANE.parent
MB = FISCAL / "matched_benefits_2026_09_19"
spec = importlib.util.spec_from_file_location("mb_model", MB / "model.py")
mb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mb)

GDP_BN = 29298.0          # matched_benefits builder.py default --gdp-billions (2026 ERP)
TAX = [.384, .426]        # builder.py line 130: Colas-Sachs current marginal rates, HS-or-less / some college+
CAP_TAX = .246            # builder.py line 130: Clemens macro capital-tax rate
ADJ = (0., .5, 1.)

pop = {r["group"]: float(r["all_ages"]) for r in
       csv.DictReader(open(FISCAL / "crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv"))}
N_UNION, N_ALL = pop["union"], pop["cps_all_civilian"]
POP_SHARE = N_UNION / N_ALL

pools = {}
for r in csv.DictReader(open(MB / "derived/skill_composition.csv")):
    pools.setdefault((r["proxy"], r["split"]), {}).setdefault(r["group"], {})[int(r["skill"])] = float(r["estimate"])


def run(target, shares, s, sigma, adj, scale_bn):
    res = mb.equilibrium(shares, target, sigma=sigma, labor_share=s, adjustment=adj)
    fp = mb.fiscal_and_private(res, TAX, CAP_TAX, 1., 0.)
    f = float(fp["labor_tax_gain"]) + float(fp["capital_tax_gain"])
    p = float(fp["private_wtp"])
    return dict(gross_bn=float(res["gross_income_gain"]) * scale_bn, P_bn=p * scale_bn, F_bn=f * scale_bn,
                PF_bn=(p + f) * scale_bn, capital_gain_bn=float(res["capital_gain"]) * scale_bn,
                labor_gain_low_bn=float(res["labor_gain"][0]) * scale_bn,
                labor_gain_high_bn=float(res["labor_gain"][1]) * scale_bn)


rows = []
for (proxy, split), g in sorted(pools.items()):
    nat = np.array([g["target"][k] + g["outside_target"][k] for k in (0, 1)])
    shares = nat / nat.sum()
    tgt = np.array([g["target"][k] / nat[k] for k in (0, 1)])
    m_eff = float((tgt * nat).sum() / nat.sum())
    for norm, s, sigma in itertools.product(("cash", "gdp"), (.60, .65, .70), (1.5, 2., 2.5)):
        scale = GDP_BN if norm == "gdp" else nat.sum() / 1e9 / s
        for who, target in (("union", tgt), ("average_residents", np.full(2, POP_SHARE))):
            base = run(target, shares, s, sigma, 1., scale)
            for adj in ADJ:
                r = run(target, shares, s, sigma, adj, scale)
                rows.append(dict(proxy=proxy, split=split, normalization=norm, labor_share=s, sigma=sigma,
                                 who=who, capital_adjustment=adj, efficiency_share=m_eff if who == "union" else POP_SHARE,
                                 **r, increment_PF_over_full_bn=r["PF_bn"] - base["PF_bn"]))

cols = list(rows[0])
with open(LANE / "derived/capital_surplus_grid.csv", "w", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=cols, lineterminator="\n")
    w.writeheader()
    for r in rows:
        w.writerow({k: (f"{v:.6f}" if isinstance(v, float) else v) for k, v in r.items()})


def pick(**kw):
    out = [r for r in rows if all(r[k] == v for k, v in kw.items())]
    assert out, kw
    return out


src = dict(proxy="PEARNVAL", split="hs_or_less")
summary = {"population": {"union": N_UNION, "all": N_ALL, "pop_share": POP_SHARE}}
# Reproduction gate: the adopted full-adjustment P+F must equal the memo's $8.79 cash / $13.32bn GDP.
for norm, want in (("cash", 8.79), ("gdp", 13.32)):
    got = pick(**src, normalization=norm, labor_share=.65, sigma=2., who="union", capital_adjustment=1.)[0]
    if abs(got["gross_bn"] - want) > .01 or abs(got["capital_gain_bn"]) > 1e-9:
        raise SystemExit(f"[BLOCKED] production term does not reproduce: {norm} {got['gross_bn']:.3f} vs {want}")
    summary[f"reproduced_full_adjustment_{norm}"] = got
for who in ("union", "average_residents"):
    for adj in (0., .5):
        grid = pick(**src, who=who, capital_adjustment=adj)
        inc = [r["increment_PF_over_full_bn"] for r in grid]
        ref = {n: pick(**src, who=who, capital_adjustment=adj, normalization=n, labor_share=.65, sigma=2.)[0]
               for n in ("cash", "gdp")}
        summary[f"{who}_adj{adj}"] = dict(min_bn=min(inc), max_bn=max(inc),
                                         ref_cash=ref["cash"], ref_gdp=ref["gdp"])
# NAS/Borjas homogeneous-labour check on the union's efficiency-unit share.
m = pick(**src, who="union", capital_adjustment=0.)[0]["efficiency_share"]
nas = {}
for s in (.60, .65, .70):
    for norm in ("cash", "gdp"):
        g = pools[("PEARNVAL", "hs_or_less")]
        Y = GDP_BN if norm == "gdp" else sum(g["target"][k] + g["outside_target"][k] for k in (0, 1)) / 1e9 / s
        nas[f"s{s}_{norm}"] = dict(union=.5 * s * (1 - s) * m ** 2 * Y, average=.5 * s * (1 - s) * POP_SHARE ** 2 * Y,
                                   wage_bill_transfer=s * (1 - s) * m * Y * (1 - m))
summary["nas_homogeneous"] = dict(efficiency_share=m, pop_share=POP_SHARE, rows=nas,
                                  nas_check_16_5pct_17_5tn=.5 * .65 * .35 * .165 ** 2 * 17500)
json.dump(summary, open(LANE / "derived/capital_surplus_summary.json", "w"), indent=1)
print(json.dumps({k: v for k, v in summary.items() if not k.startswith("reproduced")}, indent=1))
