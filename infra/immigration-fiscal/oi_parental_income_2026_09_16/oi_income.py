"""OI Opportunity Atlas national_percentile_outcomes: incarceration by race x gender x parental income pctile.
Source: https://opportunityinsights.org/wp-content/uploads/2018/10/national_percentile_outcomes.csv
Outcome `jail_*`: share institutionalized (jail/prison) on 2010 Census Day, cohort born 1978-83 (ages 27-32).
"""
import pathlib, pandas as pd, numpy as np

D = pathlib.Path(__file__).parent
df = pd.read_csv(D / "_cache" / "national_percentile_outcomes.csv")
RACES = ["white", "black", "hisp", "asian", "natam"]
PCT = [10, 25, 50, 75, 90]
out_lines = []
def p(s=""):
    print(s); out_lines.append(str(s))

rows = []
for g in ["male", "female"]:
    for r in RACES:
        rate, n = df[f"jail_{r}_{g}"], df[f"jail_{r}_{g}_n"]
        m = rate.notna() & n.notna()          # suppressed cells: drop from BOTH numerator and denominator
        pooled = float((rate[m] * n[m]).sum() / n[m].sum()) if m.any() else float("nan")
        for q in PCT:
            rows.append(dict(gender=g, race=r, par_pctile=q, cov_n=float(n[m].sum()),
                             jail_rate=float(rate[df.par_pctile == q].iloc[0]),
                             cell_n=float(n[df.par_pctile == q].iloc[0]),
                             pooled_rate=pooled, total_n=float(n.sum())))
tab = pd.DataFrame(rows)
tab.to_csv(D / "oi_incarceration_by_race_income.csv", index=False)

def block(g):
    p(f"\n=== {g.upper()}: jail rate (share institutionalized, 2010) by parental income percentile ===")
    sub = tab[tab.gender == g]
    wide = sub.pivot(index="race", columns="par_pctile", values="jail_rate").reindex(RACES)
    wide["pooled"] = sub.groupby("race").pooled_rate.first().reindex(RACES)
    wide["N"] = sub.groupby("race").total_n.first().reindex(RACES)
    p(wide.to_string(float_format=lambda x: f"{x:,.4f}"))
    p(f"\n--- ratio to white ({g}) ---")
    rel = wide.drop(columns=["N"]).div(wide.drop(columns=["N"]).loc["white"])
    p(rel.to_string(float_format=lambda x: f"{x:.3f}"))
    return wide

wm = block("male")
wf = block("female")

# --- reweight Hispanic to the white parental-income distribution (males) ---
p("\n=== Decomposition: how much of the raw Hispanic-white male gap is parental income? ===")
for g in ["male", "female"]:
    hr, hn = df[f"jail_hisp_{g}"], df[f"jail_hisp_{g}_n"]
    wr, wn = df[f"jail_white_{g}"], df[f"jail_white_{g}_n"]
    m = hr.notna() & wr.notna() & hn.notna() & wn.notna()   # common support only
    hr, wr, hn, wn = hr[m], wr[m], hn[m], wn[m]
    h_raw = float((hr * hn).sum() / hn.sum())
    w_raw = float((wr * wn).sum() / wn.sum())
    h_cf = float((hr * wn).sum() / wn.sum())          # Hispanic rates, white income distribution
    raw_gap, adj_gap = h_raw - w_raw, h_cf - w_raw
    expl = (raw_gap - adj_gap) / raw_gap if raw_gap else float("nan")
    p(f"[{g}] common-support percentiles: {int(m.sum())}/100")
    p(f"[{g}] white={w_raw:.4f}  hisp_raw={h_raw:.4f} (ratio {h_raw/w_raw:.2f}x)  "
      f"hisp_reweighted_to_white_parinc={h_cf:.4f} (ratio {h_cf/w_raw:.2f}x)")
    p(f"[{g}] raw gap={raw_gap*100:.2f}pp  income-adjusted gap={adj_gap*100:.2f}pp  "
      f"share of gap explained by parental income = {expl*100:.1f}%")
    for r in ["black", "asian", "natam"]:
        rr, rn = df[f"jail_{r}_{g}"], df[f"jail_{r}_{g}_n"]
        m2 = rr.notna() & rn.notna() & df[f"jail_white_{g}"].notna()
        if m2.sum() < 10:
            p(f"[{g}] {r}: SUPPRESSED (only {int(m2.sum())} usable percentile cells) — skipped"); continue
        rr2, rn2 = rr[m2], rn[m2]; wn2 = df[f"jail_white_{g}_n"][m2]; wr2 = df[f"jail_white_{g}"][m2]
        w_ref = float((wr2*wn2).sum()/wn2.sum())
        r_raw = float((rr2 * rn2).sum() / rn2.sum()); r_cf = float((rr2 * wn2).sum() / wn2.sum())
        w_raw_l = w_ref
        e = ((r_raw - w_raw_l) - (r_cf - w_raw_l)) / (r_raw - w_raw_l)
        p(f"[{g}] {r}: raw {r_raw:.4f} ({r_raw/w_raw_l:.2f}x) -> reweighted {r_cf:.4f} "
          f"({r_cf/w_raw_l:.2f}x); {e*100:.1f}% of gap explained  [white ref {w_raw_l:.4f}, {int(m2.sum())} cells]")

p("\n=== Hispanic/white male ratio gradient (flat or shrinking?) ===")
mm = wm.drop(columns=["N", "pooled"])
for q in PCT:
    p(f"  p{q}: white={mm.loc['white', q]:.4f} hisp={mm.loc['hisp', q]:.4f} "
      f"ratio={mm.loc['hisp', q]/mm.loc['white', q]:.2f}x  "
      f"gap={(mm.loc['hisp', q]-mm.loc['white', q])*100:.2f}pp")

p("\n=== Comparison with ACS 2023/2024 US-born Mexican-origin vs white men 18-39 ===")
p("  ACS memo ratios: 1.72x (2023) and 1.94x (2024) institutionalised.")
p(f"  OI 2010 Census, cohort b.1978-83 (ages 27-32), Hispanic/white male pooled: "
  f"{wm.loc['hisp','pooled']/wm.loc['white','pooled']:.2f}x; at equal parental income: "
  f"see reweighted ratio above.")

(D / "oi_result.txt").write_text("\n".join(out_lines) + "\n")
