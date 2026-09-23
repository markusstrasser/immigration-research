#!/usr/bin/env python3
"""Channel table for RESULT.md: central, range, per group member and per other resident.

Reads the derived outputs of hours_tax.py and elder_care.py (run those first). Channels that
ADD to the fiscal account are summed; channels inside P or beside the account are listed with
their values but never summed with the additive ones.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/care_household_services_2026_09_23/summary.py
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
D = HERE / "derived"
CPS_UNION = 40_896_574
OTHERS = 340_110_988 - CPS_UNION


def one(df: pd.DataFrame, **where) -> pd.Series:
    sel = df
    for col, val in where.items():
        sel = sel[sel[col] == val]
    if len(sel) != 1:
        raise SystemExit(f"[BLOCKED] expected one row for {where}, got {len(sel)}")
    return sel.iloc[0]


def main() -> None:
    hs = pd.read_csv(D / "hours_tax_specs.csv")
    tri = pd.read_csv(D / "ces_output_triangle.csv")
    net = pd.read_csv(D / "elder_care_net.csv")
    side = pd.read_csv(D / "partA_side_view_union_frame.csv")
    base = dict(shock="metro_weighted", scaling="cps_scaled")
    tax = "tax_bn_account_current"

    # --- induced taxes, household-service channel only
    central = one(hs, arm="CT", coefficient="t10_female_x_L", population="native_nonunion", **base)
    service = hs[(hs.shock == "metro_weighted") & (hs.scaling == "cps_scaled") & (
        ((hs.arm == "CT") & hs.coefficient.isin(["t10_female_x_L", "t10_female_x_L_cityfe"])
         & (hs.population == "native_nonunion"))
        | ((hs.arm == "EV") & (hs.coefficient != "ev_mothers_price_all_female_wage")))]
    all_channels = one(hs, arm="CT", coefficient="t7_iv_additional", attribution="all_channels",
                       population="native_nonunion", **base)
    # --- CES output gain to other factors (account central: sigma 2, capital adjusting)
    t_c = one(tri, hours_spec="central_ct_service_channel", sigma=2.0, capital_adjustment=1.0)
    t_k = one(tri, hours_spec="central_ct_service_channel", sigma=2.0, capital_adjustment=0.0)
    # --- elder care, net Medicaid; central = AAF pooled, midpoint of the two HCBS prices
    e = net[net.netting == "need_all_ages"]
    pooled = e[e.nf_spec == "aaf_pooled_precision_weighted"]
    e_central = pooled.bn_point.mean()
    # --- consumer surplus, inside P
    cs = one(side, price_arm="jpe_2008_2pct", shock="union_national")
    cs_m = one(side, price_arm="jpe_2008_2pct", shock="union_metro_w_other_population")
    cs_wp = one(side, price_arm="wp_2005_1.3pct", shock="union_national")

    rows = [
        dict(channel="taxes on native women's extra hours (household-service channel)",
             ruling="adds to fiscal account", central_bn=central[tax],
             low_bn=service[tax].min(), high_bn=service[tax].max(),
             ci_note=f"95% of central {central['tax_lo95_bn_account_current']:.2f} to "
                     f"{central['tax_hi95_bn_account_current']:.2f}; tau .366: "
                     f"{central['tax_bn_account_net_future_ss']:.2f}", in_sum=True),
        dict(channel="output gain to other factors from those hours, and its taxes (CES)",
             ruling="adds (second order)", central_bn=t_c.gross_income_gain_bn + t_c.receipts_gain_bn,
             low_bn=t_k.gross_income_gain_bn + t_k.receipts_gain_bn,
             high_bn=t_c.gross_income_gain_bn + t_c.receipts_gain_bn,
             ci_note=f"income {t_c.gross_income_gain_bn:.4f}, receipts {t_c.receipts_gain_bn:.3f}; "
                     f"capital fixed receipts {t_k.receipts_gain_bn:.2f}", in_sum=True),
        dict(channel="elder care: Medicaid nursing-facility saving net of Medicaid home care",
             ruling="adds to fiscal account", central_bn=e_central,
             low_bn=e.bn_point.min(), high_bn=e.bn_point.max(),
             ci_note=f"90% of central {pooled.bn_p5.min():.2f} to {pooled.bn_p95.max():.2f}; "
                     f"P(net<0) {pooled.prob_negative.min():.2f}-{pooled.prob_negative.max():.2f}",
             in_sum=True),
        dict(channel="native women's private gain from the extra hours", ruling="~0 (envelope)",
             central_bn=0.0, low_bn=0.0, high_bn=0.0, ci_note="beyond the service consumer surplus",
             in_sum=False),
        dict(channel="non-service part of the Cortés–Tessada hours effect (taxes)",
             ruling="not added (wage response: account's 0.33 grid, or confounded)",
             central_bn=all_channels[tax] - central[tax], low_bn=float("nan"), high_bn=float("nan"),
             ci_note=f"all-channel taxes {all_channels[tax]:.2f}", in_sum=False),
        dict(channel="consumer surplus on immigrant-intensive services, net of native low-skill wage gain",
             ruling="inside P (side view)", central_bn=cs.net_narrow_bn, low_bn=cs_wp.net_narrow_bn,
             high_bn=cs_m.net_narrow_bn,
             ci_note=f"gross {cs.consumer_loss_narrow_bn:.2f} (broad {cs.consumer_loss_broad_bn:.2f}); "
                     f"metro {cs_m.consumer_loss_narrow_bn:.2f}", in_sum=False),
    ]
    out = pd.DataFrame(rows)
    add = out[out.in_sum]
    total = dict(channel="TOTAL of additive channels", ruling="adds", central_bn=add.central_bn.sum(),
                 low_bn=add.low_bn.sum(), high_bn=add.high_bn.sum(), ci_note="", in_sum=False)
    out = pd.concat([out, pd.DataFrame([total])], ignore_index=True)
    out["per_group_member_usd"] = out.central_bn * 1e9 / CPS_UNION
    out["per_other_resident_usd"] = out.central_bn * 1e9 / OTHERS
    out.to_csv(D / "summary.csv", index=False)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 80)
    print(out.to_string(index=False))


if __name__ == "__main__":
    main()
