"""Attack on items 2 and 4 of main_case_candidate_2026_09_28. Read-only: imports the account's own row-4 code and the
production model, writes nothing. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/candidate_attack_2026_09_28/probe_production_pay.py

Item 2. The candidate recomputes the row-4 factors itself (ACS person file). Here the account's own weights come from
the account's own code, cps_imputation_keys_2026_09_23/combine_onbooks_lane.py acs_cells() and weight_arms() (IPUMS
extract 3, checked there against the PUMS), and are compared record by record and replicate by replicate with the
candidate's rule. P and F are then recomputed on the account's weights at every one of model.json's 3,888 cells and
compared with the candidate's stored row-4 grid.

Item 4. The public-pay charge decomposed: its codes, its payroll matching record by record, and P + F split by sector.
"""
import sys
sys.dont_write_bytecode = True
from pathlib import Path
import itertools
import json

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
F = ROOT / "infra/immigration-fiscal"
LANE = F / "cps_imputation_keys_2026_09_23"
CAND = F / "main_case_candidate_2026_09_28"
sys.path.insert(0, str(LANE))
sys.path.insert(0, str(F / "matched_benefits_2026_09_19"))
import common as c  # noqa: E402
import combine_onbooks_lane as acct  # noqa: E402  the account's own row-4 code (its main() is not run)
from model import equilibrium, fiscal_and_private  # noqa: E402

GDP_BN, TAX, CUT = 29298.0, [0.384, 0.426], {"hs_or_less": 39, "below_ba": 42}
stored = json.loads((CAND / "derived/production_row4.json").read_text())
model = json.loads((F / "assumption_explorer_2026_09_21/derived/model.json").read_text())

cols = sorted(set(["PRPERTYP", "A_AGE", "A_SEX", "PRCITSHP", "PENATVTY", "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "PEHSPNON",
                   "A_HGA", "GESTFIPS", "WSAL_VAL", "SEMP_VAL", "FRSE_VAL", "PEARNVAL", "LJCW", "ERN_VAL", "ERN_SRCE"]))
d = pd.read_parquet(LANE / "_cache/asec25_lane.parquet", columns=cols + c.REPS)
civ, target = c.masks(d)
W = d[c.REPS].to_numpy(float)

print("[2a] the account's own row-4 weights (combine_onbooks_lane.acs_cells + weight_arms) against the candidate's rule")
cells = acct.acs_cells()
arms, info = acct.weight_arms(d, W, cells)
W4_acct = arms["row4"]
acs = pd.read_parquet(F / "dataset_integrity_2026_09_23/_cache/acs_person_2024.parquet", columns=["ST", "RELSHIPP", "POBP", "CIT", "PWGTP"])
acs = acs[acs.RELSHIPP.ne(37) & acs.POBP.eq(303) & acs.CIT.isin([4, 5]) & ~acs.ST.isin([6, 48])]
W4_cand = W.copy()
for status in (4, 5):
    mask = (d.PENATVTY.eq(303) & d.PRCITSHP.eq(status) & ~d.GESTFIPS.isin([6, 48])).to_numpy()
    W4_cand[mask] *= float(acs.loc[acs.CIT.eq(status), "PWGTP"].sum()) / W[mask].sum(axis=0)
diff = np.abs(W4_acct - W4_cand)
rel = diff / np.where(W4_acct > 0, W4_acct, 1)
changed = np.any(W4_acct != W, axis=1)
print(f"  account targets: naturalized {cells['natz']:,.1f}, noncitizen {cells['noncit']:,.1f} (IPUMS extract 3)")
print(f"  candidate targets: naturalized {acs.PWGTP[acs.CIT.eq(4)].sum():,.1f}, noncitizen {acs.PWGTP[acs.CIT.eq(5)].sum():,.1f} (PUMS)")
print(f"  account factors (point) {info['factor_natz']:.6f} / {info['factor_noncit']:.6f}; candidate stored "
      f"{stored['row4_factors']['naturalized']['factor']:.6f} / {stored['row4_factors']['noncitizen']['factor']:.6f}")
print(f"  records the account reweights: {changed.sum()}; 161 columns; max |W4 diff| {diff.max():.3e} persons, max relative {rel.max():.3e}")
print(f"  union population: published {W[target, 0].sum():,.0f}; account row4 {W4_acct[target, 0].sum():,.0f}; "
      f"candidate row4 {W4_cand[target, 0].sum():,.0f}")
print(f"  civilian national population: published {W[civ, 0].sum():,.0f}; row4 {W4_acct[civ, 0].sum():,.0f} "
      f"(no national re-raking in either)")

print("\n[2b] P and F on the account's weights, all 3,888 cells, against the candidate's stored row-4 grid")
pearn = d.PEARNVAL.to_numpy(float)
earn = {"PEARNVAL": np.maximum(pearn, 0), "WSAL_VAL": np.maximum(d.WSAL_VAL.to_numpy(float), 0)}
hga = d.A_HGA
w0 = {"published": W[:, 0], "row4": W4_acct[:, 0]}
totals = {}
for proxy, split in itertools.product(earn, CUT):
    skill = [hga.between(31, CUT[split]).to_numpy(), hga.between(CUT[split] + 1, 46).to_numpy()]
    for name, w in w0.items():
        totals[(proxy, split, name)] = (np.array([(earn[proxy] * s * civ) @ w for s in skill]),
                                        np.array([(earn[proxy] * s * target) @ w for s in skill]))
dims = model["production"]["dims"]
order = ["proxy", "split", "normalization", "labor_share", "sigma", "capital_adjustment", "labor_supply_elasticity",
         "capital_tax_retention", "excluded_capital_owner_share"]
mine = {"published": {"P": [], "F": []}, "row4": {"P": [], "F": []}}
for cell in itertools.product(*[dims[k] for k in order]):
    proxy, split, norm, s, sigma, adj, el, ret, exc = cell
    for name in mine:
        nat, tgt = totals[(proxy, split, name)]
        r = equilibrium(nat / nat.sum(), tgt / nat, sigma, s, adj, el)
        part = fiscal_and_private(r, TAX, 0.246, ret, exc)
        scale = GDP_BN * 1e9 if norm == "gdp" else nat.sum() / s
        mine[name]["P"].append(float(part["private_wtp"] * scale / 1e9))
        mine[name]["F"].append(float(part["current_receipts_gain"] * scale / 1e9))
for name, ref in (("published", model["production"]), ("row4", stored["grid"]["row4"])):
    dP = max(abs(a - b) for a, b in zip(mine[name]["P"], ref["private_wtp_bn"]))
    dF = max(abs(a - b) for a, b in zip(mine[name]["F"], ref["induced_receipts_bn"]))
    print(f"  {name:9s} vs {'model.json' if name == 'published' else 'candidate row4 grid'}: max |dP| {dP:.2e}, max |dF| {dF:.2e} bn (3,888 cells)")
refc = model["production"]["reference"]
for norm in ("gdp", "cash"):
    idx = [i for i, cell in enumerate(itertools.product(*[dims[k] for k in order]))
           if dict(zip(order, cell)) == dict(refc, normalization=norm)][0]
    pf = {n: mine[n]["P"][idx] + mine[n]["F"][idx] for n in mine}
    print(f"  reference cell ({norm}, index {idx}): P+F {pf['published']:.6f} -> {pf['row4']:.6f}; cost change {pf['published'] - pf['row4']:+.6f}")

print("\n[4a] public-pay matching, record by record (incumbents: civilian, outside the group; published weight)")
inc = civ & ~target
ern, src, ljcw = d.ERN_VAL.to_numpy(float), d.ERN_SRCE.to_numpy(), d.LJCW.to_numpy()
public = np.isin(ljcw, [2, 3, 4]) & (src == 1) & inc
w = W[:, 0]
cut = CUT[refc["split"]]
skills = {"hs_or_less": hga.between(31, cut).to_numpy(), "more": hga.between(cut + 1, 46).to_numpy()}
base = {k: (earn["PEARNVAL"] * m * inc) @ w for k, m in skills.items()}
print(f"  public records {public.sum()}; outside both skill groups (A_HGA not 31-46): {(public & ~(skills['hs_or_less'] | skills['more'])).sum()}")
over = public & (np.maximum(ern, 0) > np.maximum(pearn, 0))
print(f"  public records whose longest-job pay exceeds their own base max(PEARNVAL,0): {over.sum()}, "
      f"excess ${((np.maximum(ern, 0) - np.maximum(pearn, 0)) * over) @ w / 1e9:.2f}bn of ${(np.maximum(ern, 0) * public) @ w / 1e9:.2f}bn")
nonpub_ws = inc & (ljcw == 1)
print(f"  wage records with LJCW 1 (private): {nonpub_ws.sum()}; LJCW 2/3/4 with ERN_SRCE != 1: {(np.isin(ljcw, [2, 3, 4]) & (src != 1) & inc).sum()}")
for k, m in skills.items():
    num = (np.maximum(ern, 0) * public * m) @ w
    print(f"  {k:10s}: public payroll ${num / 1e9:,.1f}bn / incumbent base ${base[k] / 1e9:,.1f}bn = {num / base[k]:.4f}")

print("\n[4b] P + F split by sector at the reference cell (row-4 weights); the charge is the public part")
for norm in ("gdp", "cash"):
    pp = stored["public_pay"]["row4"][norm]
    gain = np.array(pp["incumbent_labor_gain_bn"])
    pi = np.array(stored["public_pay"]["public_share_of_incumbent_earnings"])
    pub, priv = pi * gain, (1 - pi) * gain
    print(f"  {norm}: labor gain by skill {gain.round(2).tolist()} (sum {gain.sum():.4f}); public part {pub.round(2).tolist()} "
          f"(sum {pub.sum():.4f} = charge {pp['charge_bn']:.4f}); private part {priv.round(2).tolist()} (sum {priv.sum():.4f})")
