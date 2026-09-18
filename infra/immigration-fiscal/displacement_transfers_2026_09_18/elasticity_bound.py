"""Transfer published wage elasticities onto the Mexican-origin wage bill, as a RANGE.

This is an arithmetic transfer, not an estimate. It answers: if the published elasticities
are right, how large is the annual wage loss to earlier Mexico-born workers and to the
Mexican second generation, and what does that cost the Treasury in forgone tax?

Two corrections to the brief's specification, both from the source papers:

1. The brief asks to apply the Ottaviano-Peri earlier-immigrant elasticity to BOTH the
   Mexico-born stock AND the second generation's wage bill. Ottaviano-Peri's structure does
   not permit that. Their large negative number is the effect on FOREIGN-BORN workers, who
   are imperfect substitutes for natives; the second generation is US-born and takes their
   NATIVE elasticity, which is +1.8% on average and -1.1% for high-school dropouts (NBER
   w12497 Table 7, sigma=6.6). Applying -19.8% to a native-born group would contradict the
   paper being cited. The second generation is therefore carried with the native elasticity.

2. The brief's -6.7% could not be verified (see the memo). Both -19.8% (verified, NBER
   working paper) and -6.7% (the brief's figure, unverified) are carried through, and the
   spread between them is reported as part of the range rather than resolved.

Elasticity scope also differs between the two sources and is kept separate:
  Ottaviano-Peri: the cumulative effect of FOURTEEN YEARS of immigration (1990-2004, an
                  inflow of 11.0% of initial employment overall, 20% for HS dropouts)
  Borjas 2003:    -3 to -4% per 10% increase in the skill group's supply, partial
                  equilibrium with capital fixed
"""
import json, pathlib
import pandas as pd

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"

# ---- inputs, all measured elsewhere in this lane ------------------------------
W = pd.read_csv(DERIVED / "wage_bills.csv")
NAT = pd.read_csv(DERIVED / "national_stock.csv").set_index("year")


def bill(group, band="all_ages"):
    r = W[(W.group == group) & (W.band == band)].iloc[0]
    return float(r.wage_bill), float(r.persons), float(r.avg_tax_rate_on_wages)


MXB, MXB_N, MXB_TAX = bill("mexico_born")
SG, SG_N, SG_TAX = bill("mexican_second_gen")

# Ottaviano-Peri NBER w12497, Table 7 (long run) and Table 8 (as of 2004), sigma = 6.6
OP = {"foreign-born average, long run": -0.198,
      "foreign-born average, as of 2004": -0.209,
      "foreign-born HS dropouts, long run": -0.163,
      "BRIEF'S FIGURE [UNVERIFIED]": -0.067}
OP_NATIVE = {"US-born average, long run": +0.018,
             "US-born HS dropouts, long run": -0.011}
# Borjas 2003 (NBER w9755): -3 to -4% per 10% supply increase in the skill cell
BORJAS = (-0.30, -0.40)   # per unit proportional supply increase

# Marginal tax-and-transfer rate applied to a wage change. The all-age ledger stores no
# marginal rate, so three are carried and every one is labelled.
RATES = {
    "measured average rate on wages, Mexico-born (FICA+federal+state, employee side)": MXB_TAX,
    "measured average rate on wages, Mexican second generation": SG_TAX,
    "employee side + employer payroll (7.65pp added)": None,   # filled per group below
    "assumed high case incl. benefit phase-outs": 0.35,
}

rows = []


def add(scenario, group, wage_bill, elast, rate_label, rate, note):
    loss = wage_bill * elast
    rows.append({"scenario": scenario, "group": group,
                 "wage_bill_2024_usd": wage_bill, "elasticity": elast,
                 "wage_change_usd": loss, "tax_rate_label": rate_label,
                 "tax_rate": rate, "fiscal_change_usd": loss * rate, "note": note})


# ---- Bound 1: an Ottaviano-Peri-scale inflow (14 years, 11% of employment) ----
for lab, e in OP.items():
    for rl, r in (("Mexico-born average rate", MXB_TAX),
                  ("employee + employer payroll", MXB_TAX + 0.0765),
                  ("high case 0.35", 0.35)):
        add("OP: 1990-2004-scale inflow", "mexico_born", MXB, e, rl, r,
            f"OP elasticity: {lab}")
for lab, e in OP_NATIVE.items():
    for rl, r in (("second-gen average rate", SG_TAX),
                  ("employee + employer payroll", SG_TAX + 0.0765),
                  ("high case 0.35", 0.35)):
        add("OP: 1990-2004-scale inflow", "mexican_second_gen", SG, e, rl, r,
            f"OP NATIVE elasticity (second gen is US-born): {lab}")

# ---- Bound 2: Borjas, applied to the actual 2021-2024 inflow ------------------
# The supply shock is the foreign-born stock increase over the US labour force. BLS CPS
# civilian labour force averaged 168.1 million in 2024; the stock increase is measured in
# this lane's own national series.
LF_2024 = 168.1e6
dfb = NAT.loc[2024, "fb"] - NAT.loc[2021, "fb"]
supply_shock = dfb / LF_2024
for i, e in enumerate(BORJAS):
    for grp, wb, tx in (("mexico_born", MXB, MXB_TAX),
                        ("mexican_second_gen", SG, SG_TAX)):
        for rl, r in ((f"{grp} average rate", tx),
                      ("employee + employer payroll", tx + 0.0765),
                      ("high case 0.35", 0.35)):
            add("Borjas: actual 2021-2024 inflow", grp, wb, e * supply_shock, rl, r,
                f"Borjas {-e*100:.0f}% per 10% supply; shock = {100*supply_shock:.2f}% of the "
                f"2024 labour force ({dfb/1e6:.2f}M / {LF_2024/1e6:.1f}M)")

out = pd.DataFrame(rows)
out.to_csv(DERIVED / "elasticity_bound.csv", index=False)

pd.set_option("display.width", 220)
print(f"Mexico-born wage bill 2024:            ${MXB/1e9:,.1f}bn  ({MXB_N/1e6:.2f}M people, "
      f"avg tax rate on wages {MXB_TAX:.3f})")
print(f"Mexican second-generation wage bill:   ${SG/1e9:,.1f}bn  ({SG_N/1e6:.2f}M people, "
      f"avg tax rate on wages {SG_TAX:.3f})")
print(f"2021-2024 foreign-born stock increase: {dfb/1e6:.2f}M = {100*supply_shock:.2f}% "
      f"of the 2024 civilian labour force\n")
for sc in out.scenario.unique():
    g = out[out.scenario == sc]
    print("=" * 100); print(sc)
    for grp in g.group.unique():
        h = g[g.group == grp]
        lo, hi = h.wage_change_usd.min(), h.wage_change_usd.max()
        flo, fhi = h.fiscal_change_usd.min(), h.fiscal_change_usd.max()
        print(f"  {grp:<22} wage change ${lo/1e9:+,.1f}bn to ${hi/1e9:+,.1f}bn   "
              f"fiscal ${flo/1e9:+,.1f}bn to ${fhi/1e9:+,.1f}bn")
print("\nwrote derived/elasticity_bound.csv", out.shape)
