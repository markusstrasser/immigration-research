"""Arm 5: the White-subtraction counter-item, tested on NIBRS arrestees in the NIBRS lane's frame.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/arm5_white_subtraction.py

Older arrest-flow routes (`crime_cost_2026_09_16/crime_cost.py` route B, `nibrs_arrests_2026_09_16`)
build non-Hispanic white arrests from tables that report race and ethnicity separately:
    scaled_white = White (race panel) x ethnicity-panel total / race-panel total
    NH white     = scaled_white - Hispanic (ethnicity panel)
Every Hispanic arrestee is subtracted from White, although some are coded Black, other or
unknown race. NIBRS records race and ethnicity per arrestee, so the true NH-white count is known
and the construction can be run beside it on the same records.

Hispanic / NH-white overstatement = NHW_true / NHW_constructed - 1 (denominators cancel).
The NIBRS lane's offender ratios (2.30 murder) use disjoint classes and carry none of this.
"""
from __future__ import annotations

from pathlib import Path

import pandas as pd

import nibrs_base as nb

nr = nb.nr
HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
H = ["HW", "HB", "HO", "HU"]
NHK = ["NHW", "NHB", "NHO", "NHU"]
RACE_KNOWN = ["HW", "HB", "HO", "NHW", "NHB", "NHO", "UW", "UB", "UO"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def universe(stages: dict, states: tuple, rec_min: float) -> tuple[pd.DataFrame, pd.Series]:
    cells, pops = [], []
    for (st, yr), d in stages.items():
        if st not in states:
            continue
        ag = d["agencies"]
        keep = ag[ag.comp_source.ne("tribal_excluded") & ag.rec_rate.fillna(0).ge(rec_min)]
        a = d["acells"]
        cells.append(a[a.agency_id.isin(keep.agency_id) & a.offence.isin(nr.OFFENCES)])
        pops.append(keep[[f"c_{g}{s}" for g in ["hisp", "nhw"] for s in ["_12", "_18"]]].sum())
    return pd.concat(cells), pd.concat(pops, axis=1).sum(axis=1)


def construct(c: pd.DataFrame) -> dict:
    eh = c[H].sum()
    E = eh + c[NHK].sum()
    R = c[RACE_KNOWN].sum()
    rw = c[["HW", "NHW", "UW"]].sum()
    nhw = c["NHW"]
    route_b = rw * E / R - eh
    pure = c["HW"] + nhw - eh
    return dict(hispanic=eh, nhw_true=nhw, nhw_route_b=route_b, nhw_no_rescale=pure,
                hispanic_white_coded=c["HW"] / eh, hispanic_not_white=(eh - c["HW"]) / eh,
                over_route_b=nhw / route_b - 1, over_no_rescale=nhw / pure - 1)


def main() -> None:
    OUT.mkdir(exist_ok=True)
    stages, _ = nb.load()
    # positive control: the lane's arrestee ratio (central, all ages, allocation a) from the same stages
    lane = nr.arrestee_results({k: v for k, v in stages.items()}, nr.CENTRAL, nr.national_pops())
    lane = lane[lane.alloc.eq("a")].set_index(["arrestees", "offence"]).RR_H_NHW
    say(f"[gate] lane arrestee Hispanic / NH-white, central, all ages: murder {lane[('all ages', 'Murder')]:.3f}, "
        f"robbery {lane[('all ages', 'Robbery')]:.3f} (nibrs_checks.py: 2.279, 2.946)")
    assert abs(lane[("all ages", "Murder")] - 2.279) < 5e-4 and abs(lane[("all ages", "Robbery")] - 2.946) < 5e-4

    rows = []
    for lab, states, rec in [("central: TX+AZ, agencies recording >= 50%", ("TX", "AZ"), 0.5),
                             ("TX, all agencies", ("TX",), 0.0), ("AZ, all agencies", ("AZ",), 0.0),
                             ("CA, all agencies", ("CA",), 0.0)]:
        cells, pop = universe(stages, states, rec)
        for age, sel, sfx in [("all ages", None, "_12"), ("adults 18+", "18p", "_18")]:
            a = cells if sel is None else cells[cells.age18.eq(sel)]
            t = a.groupby(["offence", "cls"]).arrestees.sum().unstack("cls", fill_value=0)
            t = t.reindex(columns=H + NHK + ["UW", "UB", "UO", "UU"], fill_value=0).astype(float)
            t.loc["All five"] = t.sum()
            for off, c in t.iterrows():
                r = construct(c)
                raw_true = (r["hispanic"] / pop[f"c_hisp{sfx}"]) / (r["nhw_true"] / pop[f"c_nhw{sfx}"])
                rows.append(dict(universe=lab, arrestees=age, offence=off, **r,
                                 RR_H_NHW_known_true=raw_true,
                                 RR_H_NHW_known_route_b=raw_true * (1 + r["over_route_b"]),
                                 RR_H_NHW_lane_central=lane.get((age, off), float("nan"))
                                 if lab.startswith("central") else float("nan")))
    R = pd.DataFrame(rows)
    R["RR_H_NHW_lane_route_b"] = R.RR_H_NHW_lane_central * (1 + R.over_route_b)
    R.to_csv(OUT / "arm5_white_subtraction.csv", index=False, float_format="%.6f", lineterminator="\n")
    show = R[R.offence.isin(["Murder", "Robbery", "All five"])][
        ["universe", "arrestees", "offence", "hispanic", "hispanic_white_coded", "over_route_b", "over_no_rescale",
         "RR_H_NHW_lane_central", "RR_H_NHW_lane_route_b"]]
    say(show.to_string(index=False, float_format=lambda x: f"{x:.4f}" if abs(x) < 100 else f"{x:,.0f}"))
    say("\nThe NIBRS lane's offender ratios (central 2.30 murder, 4.22 robbery) use disjoint race-ethnicity classes:"
        " the construction is absent there, so Arm 5 changes them by 0.")
    (OUT / "arm5_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
