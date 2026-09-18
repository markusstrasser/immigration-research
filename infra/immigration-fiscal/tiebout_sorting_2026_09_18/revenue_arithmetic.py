"""California and Texas: the AGI that left net of what arrived, and what that is worth
in state and local revenue, set beside the state's Mexican-origin fiscal gap.

Inputs
  derived/soi_state_agi.csv     IRS SOI in/out AGI by state and AGI bracket
  ITEP "Who Pays?" 2024 effective state+local tax rate on the top 1% of taxpayers
    (California 12.1%, Texas 4.6%)  [SOURCE: data/itep/itep_table_5.tsv]
  ledger_stress_2026_09_17/derived/state_matched.csv   the state fiscal gaps

Convention: out-migrant AGI is the year-1 figure (income reported while still resident),
in-migrant AGI the year-2 figure (income reported after arriving), which is how SOI
frames each flow. A positive net number means AGI left.

[CAVEAT] The revenue figure is state-and-local only. The fiscal gap it is compared with
is a whole-of-government account covering federal, state and local budgets, so the two
are not the same unit. The comparison below is therefore an upper bound on how much of
the gap the migration channel could plausibly offset at the state level, not a share of
the published gap.

Output: derived/revenue_arithmetic.csv
"""
import os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(HERE, "derived")
STRESS = os.path.join(os.path.dirname(HERE), "ledger_stress_2026_09_17", "derived",
                      "state_matched.csv")
RATE = {"06": 0.121, "48": 0.046}      # ITEP top-1% effective state+local rate
NAME = {"06": "California", "48": "Texas"}


def main():
    soi = pd.read_csv(os.path.join(DERIVED, "soi_state_agi.csv"), dtype={"statefips": str})
    soi["statefips"] = soi["statefips"].str.zfill(2)
    rows = []
    for fips, rate in RATE.items():
        d = soi[soi.statefips == fips]
        for stub, label in [(0, "all filers"), (7, "AGI $200k+"), (6, "AGI $100-200k")]:
            g = d[d.agi_stub == stub].sort_values("year2")
            net_agi = (g.outflow_y1_agi_0 - g.inflow_y2_agi_0) / 1e6   # $bn
            net_ret = (g.outflow_n1_0 - g.inflow_n1_0)
            for y, a, n, o, i in zip(g.year2, net_agi, net_ret,
                                     g.outflow_y1_agi_0 / 1e6, g.inflow_y2_agi_0 / 1e6):
                rows.append(dict(state=NAME[fips], bracket=label, year=y,
                                 out_agi_bn=o, in_agi_bn=i, net_agi_out_bn=a,
                                 net_returns_out=n,
                                 revenue_at_top1_rate_bn=a * rate))
    r = pd.DataFrame(rows)
    r.to_csv(os.path.join(DERIVED, "revenue_arithmetic.csv"), index=False)
    pd.set_option("display.width", 200)
    for st in r.state.unique():
        print("\n=== %s ===" % st)
        print(r[r.state == st].pivot_table(index="year", columns="bracket",
                                           values="net_agi_out_bn")
              .round(2).to_string())
        s = r[(r.state == st)].groupby("bracket").agg(
            mean_net_agi_out_bn=("net_agi_out_bn", "mean"),
            last_net_agi_out_bn=("net_agi_out_bn", "last"),
            mean_revenue_bn=("revenue_at_top1_rate_bn", "mean"),
            cumulative_revenue_bn=("revenue_at_top1_rate_bn", "sum"),
            years=("year", "count"))
        print(s.round(3).to_string())

    gap = pd.read_csv(STRESS)
    g = gap[(gap.target == "mexican_observed_total") & (gap.metric == "gap_total")
            & (gap.scenario == "all_age_shared") & (gap.cells.isin(["CA_age", "TX_age"]))]
    print("\n=== state Mexican-origin gap totals, $bn/yr (whole-of-government) ===")
    print(g[["cells", "reference", "estimate"]].assign(
        bn=lambda x: (x.estimate / 1e9).round(1))[["cells", "reference", "bn"]]
        .to_string(index=False))


if __name__ == "__main__":
    main()
