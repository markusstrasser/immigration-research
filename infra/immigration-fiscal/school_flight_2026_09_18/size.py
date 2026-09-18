"""Design (c): scale the estimated flight coefficient by the observed Hispanic-share change.

Multiplies the long-difference coefficient (change in the private share of US-born
non-Hispanic white children per unit change in the Hispanic share of enrolled children)
by the observed Hispanic-share change over the panel window, for the nation and for
California and Texas separately, and converts the implied head count into tuition spend
and into enrolment-linked state aid no longer flowing to the districts.

Prices: NCES Digest 2023 table 205.50 average private tuition, by school level
(derived/nces_national_context.csv). State revenue per pupil comes from the repo's own
F-33 load (derived/district_panel.csv), enrolment-weighted, 2020 dollars.

Every line is a mechanical projection of an estimated coefficient, NOT a measured
head count. The confidence interval is carried through so the width is visible.
"""
import pathlib
import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).parent
DERIVED = HERE / "derived"
CA, TX = 6, 48


def main():
    est = pd.read_csv(DERIVED / "estimates_flight.csv")
    panel = pd.read_csv(DERIVED / "metro_school_panel.csv", dtype={"cbsa": str})
    ctx = pd.read_csv(DERIVED / "nces_national_context.csv")
    ctxv = {(r.series, int(r.year)): r.value for r in ctx.itertuples()}

    years = sorted(panel.year.unique())
    # match estimate_flight.py's primary window: base year >= 2008, because ACS SCH=3
    # only began including home school in 2008
    base = [y for y in years if y >= 2008]
    y0, y1 = (base[0] if base else years[0]), years[-1]
    rows = []

    tuition = {"elem": ctxv[("private_avg_tuition_elem", 2021)],
               "sec": ctxv[("private_avg_tuition_secondary", 2021)],
               "all": ctxv[("private_avg_tuition", 2021)]}

    # Prices come from the repo's own local F-33 FY2024 district file rather than the
    # Urban panel, which stops at 2020: derived/f33_fy2024_per_pupil.csv.
    f33 = pd.read_csv(DERIVED / "f33_fy2024_per_pupil.csv").set_index("measure")
    state_aid_pp = float(f33.loc["state_revenue", "per_pupil_fy2024_dollars"])
    local_pp = float(f33.loc["local_revenue", "per_pupil_fy2024_dollars"])
    current_pp = float(f33.loc["current_spending", "per_pupil_fy2024_dollars"])
    aid_year = 2024
    print(f"F-33 FY2024 prices: state aid {state_aid_pp:,.0f}, local {local_pp:,.0f}, "
          f"current spending {current_pp:,.0f} per pupil")

    for lvl in ("elem", "sec", "all"):
        e = est[(est.spec == f"long {y0}-{y1}") & (est.level == lvl)
                & (est.treatment == "d hisp_share")]
        if e.empty:
            continue
        b, se = float(e.coef.iloc[0]), float(e.se.iloc[0])
        for scope, name, sel in (("US metros", "national (panel metros)", panel.index),
                                 ("CA metros", "California", panel.state_fips == CA),
                                 ("TX metros", "Texas", panel.state_fips == TX)):
            p = panel[sel] if not isinstance(sel, pd.Index) else panel
            a = p[p.year == y0]
            z = p[p.year == y1]
            if a.empty or z.empty:
                continue
            h0 = float((a[f"hisp_share_{lvl}"] * a[f"enr_{lvl}"]).sum() / a[f"enr_{lvl}"].sum())
            h1 = float((z[f"hisp_share_{lvl}"] * z[f"enr_{lvl}"]).sum() / z[f"enr_{lvl}"].sum())
            dh = h1 - h0
            wnh = float(z[f"wnh_enr_{lvl}"].sum())
            for tag, coef in (("point", b), ("lo95", b - 1.96 * se), ("hi95", b + 1.96 * se)):
                dshare = coef * dh
                n = dshare * wnh
                rows.append(dict(
                    level=lvl, scope=scope, region=name, bound=tag,
                    window=f"{y0}-{y1}", coef=coef, d_hisp_share=dh,
                    wnh_enrolled_end=wnh, implied_d_private_share=dshare,
                    implied_natives_moved=n,
                    tuition_per_pupil=tuition[lvl],
                    implied_tuition_spend_musd=n * tuition[lvl] / 1e6,
                    state_aid_per_pupil=state_aid_pp,
                    implied_state_aid_shifted_musd=n * state_aid_pp / 1e6,
                    aid_price_year=aid_year))
    out = pd.DataFrame(rows)
    out.to_csv(DERIVED / "size_estimates.csv", index=False)
    pt = out[out.bound == "point"]
    print(pt[["level", "region", "d_hisp_share", "implied_d_private_share",
              "implied_natives_moved", "implied_tuition_spend_musd",
              "implied_state_aid_shifted_musd"]].to_string(index=False))
    print(f"\nlocal revenue per pupil (2020$, {aid_year}): {local_pp:,.0f}; "
          f"state revenue per pupil: {state_aid_pp:,.0f}")
    print(f"wrote {DERIVED/'size_estimates.csv'}")


if __name__ == "__main__":
    main()
