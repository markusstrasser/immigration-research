"""Adjacent check on ladder 182 (finding F1): the ancestry lane's household SSI and public-assistance
IV, re-run with a fixed-geography 2010 endpoint.

The lane's 2000-2010 panel matches 2013-delineation 2000 rows to 2009-delineation ACS 2010 rows
by code, which drops Los Angeles and mixes footprints. Here the 2010 endpoint for the outcome and
for the foreign-born share is the ACS 2008-2012 five-year county file summed onto the same 2013
CBSAs as the 2000 row (fetch_commute.py, build_commute.py). Rows: the lane's own sample and
definitions (PC), the same 334 metros with the fixed endpoint, all 341 metros (FG), and FG
without Los Angeles. Nothing in the ancestry lane is edited.

Writes derived/ssi_fixed_geography.csv.
"""
import pandas as pd

from common import DERIVED, menu, sample_fg, sample_pc, si, add_instruments


def main():
    cm = pd.read_csv(DERIVED / "commute_metro.csv", dtype={"cbsa": str})
    rows = []
    for outcome, col1f in (("ssi_rate", "ssi_rate_1f"), ("pa_rate", "pa_rate_1f")):
        lane = add_instruments(si.panel(outcome))
        menu(rows, lane, "dy", "dX", {"design": "PC lane panel (published 2010)", "outcome": outcome}, y0="y0")
        fg = sample_fg().merge(cm[["cbsa", "fb_share_1f", col1f]], on="cbsa", how="left")
        fg["dX"] = fg.fb_share_1f - fg.fb_share
        fg["dy"] = fg[col1f] - fg[outcome]
        fg["y0"] = fg[outcome]
        pc_ids = set(sample_pc().cbsa)
        for name, frame in (("PC metros, fixed 2008-12 endpoint", fg[fg.cbsa.isin(pc_ids)]),
                            ("FG all metros, fixed endpoint", fg),
                            ("FG without Los Angeles", fg[fg.cbsa != "31080"])):
            menu(rows, frame, "dy", "dX", {"design": name, "outcome": outcome}, y0="y0")
    est = pd.DataFrame(rows)
    est.to_csv(DERIVED / "ssi_fixed_geography.csv", index=False)
    show = est[est.estimator.isin(["first stage on Z2", "OLS", "IV with Z2", "IV with Z2_exmex", "IV with Z",
                                   "level placebo: Z2 on 2000 level", "level placebo: Z on 2000 level"])]
    with pd.option_context("display.width", 220, "display.max_rows", 200):
        print(show[["outcome", "design", "estimator", "n", "coef", "se", "F", "ar_lo", "ar_hi", "ar_kind"]]
              .round(4).to_string(index=False))


if __name__ == "__main__":
    main()
