#!/usr/bin/env python3
"""Summary table: both channels, three arms, against the repo's fiscal figures."""
import json
from pathlib import Path
import pandas as pd

D = Path(__file__).resolve().parent / "derived"
A = pd.read_csv(D / "partA_price_results.csv")
B = pd.read_csv(D / "partB_hours_results.csv")
W = pd.read_csv(D / "native_lowskill_wage_offset.csv")
aud = json.loads((D / "compute_audit.json").read_text())
MEX = aud["mexborn_dropout"]

# repo fiscal reference points (ladder 123, 130): annual $bn
FISCAL = {"gap_vs_third_plus_whites_main": 290.59, "gap_vs_all_natives_main": 215.00,
          "complete_gap_vs_whites": 354.28, "complete_absolute": 254.0}

def pick(df, **kw):
    m = df
    for k, v in kw.items():
        m = m[m[k] == v]
    return m.iloc[0]

rows = []
for label, price_arm, hours_arm, wage_arm in [
    ("central (published JPE 2008 + hours|H>0)", "published_jpe_2008", "hours_given_working_addl_controls", "full"),
    ("working-paper elasticity + unconditional hours", "working_paper_2005", "usual_hours_addl_controls", "full"),
    ("conservative (half elasticity, half hours)", "half_published", "half_hours_given_working", "half"),
]:
    a = pick(A, arm=price_arm, shock="lf_adjusted", scope="narrow_immigrant_intensive")
    ab = pick(A, arm=price_arm, shock="lf_adjusted", scope="broad_incl_other_nontraded")
    b = pick(B, population="topq_native_college_women", arm=hours_arm, shock="lf_adjusted")
    w = pick(W, arm=wage_arm, shock="lf_adjusted")
    cs = float(a.annual_loss_bn)
    cs_broad = float(ab.annual_loss_bn)
    off = float(w.annual_gain_bn)
    earn = -float(b.earnings_change_bn)
    tax = -float(b.tax_bn_high_earner_buildup)
    net_cs = cs - off
    total = net_cs + tax
    rows.append(dict(
        arm=label,
        A_consumer_surplus_bn=cs, A_consumer_surplus_broad_bn=cs_broad,
        A_native_lowskill_wage_offset_bn=off, A_net_bn=net_cs,
        B_private_earnings_bn=earn, B_tax_revenue_bn=tax,
        defensible_native_total_bn=total,
        fiscal_only_bn=tax,
        per_mex_lowskill_worker_total=total * 1e9 / MEX,
        per_mex_lowskill_worker_fiscal=tax * 1e9 / MEX,
        **{f"pct_of_{k}": 100.0 * total / v for k, v in FISCAL.items()},
        **{f"fiscal_pct_of_{k}": 100.0 * tax / v for k, v in FISCAL.items()},
    ))
S = pd.DataFrame(rows)
S.to_csv(D / "summary_table.csv", index=False)
pd.set_option("display.width", 250)
print(S.round(2).T.to_string())
