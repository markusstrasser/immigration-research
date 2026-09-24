"""Arm 1 follow-up checks on the NIBRS records (Texas and Arizona 2022-2023, central agencies).

    uv run --no-project --with pandas --with numpy --with scikit-learn python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/nibrs_checks.py

1. Offender-segment vs arrestee-segment ethnicity in single-offender, single-arrestee incidents,
   by agency: where the two disagree, which record is wrong, and how much it moves arrestee-based
   ratios (the lane's arrestee comparison and, by extension, arrest-keyed shares).
2. A validation-adjusted allocation: offenders recorded without ethnicity get the Hispanic share
   that booked arrestees show in the same situation (agencies with sound arrestee coding only),
   relative to what the central imputes.
3. The recording-threshold pattern (Hispanic / NH-white falls as the agency threshold rises):
   imputation or agency composition? Ratios by threshold band with allocations a, k, b and c.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

import nibrs_base as nb
import nibrs_impute as ni

nr = nb.nr
HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
HC = nr.H_CLASSES
NHK = ["NHW", "NHB", "NHO", "NHU"]
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def agencies(stages: dict) -> pd.DataFrame:
    return pd.concat([d["agencies"].assign(state=st, year=yr) for (st, yr), d in stages.items()])


def discordance(df: pd.DataFrame, ag: pd.DataFrame) -> pd.DataFrame:
    a_h = df[ni.ARR_H].sum(axis=1)
    a_nh = df[ni.ARR_NH].sum(axis=1)
    one = (df.n_known == 1) & ((a_h + a_nh) == 1) & (df[ni.ARR_U].sum(axis=1) == 0) \
        & (df[HC + NHK].sum(axis=1) > 0.999)
    d = df[one].merge(ag[["state", "year", "agency_id", "pub_agency_name"]], on=["state", "year", "agency_id"], how="left")
    d["off_H"] = d[HC].sum(axis=1) > 0.5
    d["arr_H"] = (a_h[one] > 0).to_numpy()
    g = d.groupby(["state", "pub_agency_name"]).agg(
        single_pairs=("off_H", "size"), offender_H=("off_H", "sum"),
        off_H_arr_NH=("off_H", lambda s: int((s & ~d.loc[s.index, "arr_H"]).sum())),
        off_NH_arr_H=("off_H", lambda s: int((~s & d.loc[s.index, "arr_H"]).sum())))
    g["share_of_offender_H_booked_NH"] = g.off_H_arr_NH / g.offender_H.replace(0, np.nan)
    tot = g.sum(numeric_only=True)
    say(f"single-offender, single-arrestee incidents with both ethnicities recorded: {int(tot.single_pairs):,}; "
        f"offender Hispanic, arrestee non-Hispanic {int(tot.off_H_arr_NH):,}; offender non-Hispanic, arrestee "
        f"Hispanic {int(tot.off_NH_arr_H):,}")
    say(f"   offender-segment Hispanic share {tot.offender_H / tot.single_pairs:.4f}; arrestee-segment "
        f"{(tot.offender_H - tot.off_H_arr_NH + tot.off_NH_arr_H) / tot.single_pairs:.4f}")
    g = g.sort_values("off_H_arr_NH", ascending=False)
    say(g.head(12).to_string(float_format=lambda x: f"{x:.3f}"))
    return g.reset_index()


def arrestee_ratios(stages: dict, natpop: dict, drop_names: set[str]) -> pd.DataFrame:
    """The lane's arrestee ratios (adults and all ages), optionally without some agencies."""
    st2 = {}
    for k, d in stages.items():
        a = d["agencies"]
        d2 = dict(d)
        d2["agencies"] = a[~a.pub_agency_name.isin(drop_names)] if drop_names else a
        st2[k] = d2
    r = nr.arrestee_results(st2, nr.CENTRAL, natpop)
    return r[r.alloc.eq("a")]


def validation_adjusted(df: pd.DataFrame, P: pd.Series, base: pd.DataFrame, factor: float) -> pd.DataFrame:
    """Scale the Hispanic probability imputed to offenders recorded without ethnicity (UW, UB, UO,
    UU; not NOINFO) by `factor`, moving the difference to the non-Hispanic groups in proportion."""
    p = base.copy()
    for r in ["W", "B", "O"]:
        p[f"q_{r}"] = p[f"q_{r}"] * factor
    alloc = ni.allocate_rows(df, p)
    # UU keeps the central overall split for NOINFO; rescale only its UU part
    ov = base[["ov_H", "ov_NHW", "ov_NHB", "ov_NHO"]].to_numpy()
    uu = df["UU"].to_numpy()
    adj = ov.copy()
    adj[:, 0] = ov[:, 0] * factor
    rest = ov[:, 1:].sum(axis=1)
    scale = np.where(rest > 0, (1 - adj[:, 0]) / np.where(rest > 0, rest, 1), 1.0)
    adj[:, 1:] = ov[:, 1:] * scale[:, None]
    delta = uu[:, None] * (adj - ov)
    alloc[["H", "NHW", "NHB", "NHO"]] += delta
    return alloc


def main() -> None:
    OUT.mkdir(exist_ok=True)
    stages, natpop = nb.load()
    rows = ni.load_rows()
    df, P = ni.spec_rows(rows, stages, nb.lane_specs()["central"])
    ag = agencies(stages)

    say("-- 1. Offender vs arrestee ethnicity, by agency --")
    g = discordance(df, ag)
    g.to_csv(OUT / "nibrs_offender_arrestee_discordance.csv", index=False, float_format="%.4f", lineterminator="\n")
    bad = set(g.loc[(g.offender_H >= 50) & (g.share_of_offender_H_booked_NH > 0.05), "pub_agency_name"])
    say(f"agencies booking > 5% of offender-recorded Hispanics as non-Hispanic (>= 50 pairs): {sorted(bad)}")
    rows_out = []
    for lab, drop in [("all central agencies (lane)", set()), ("without agencies with booking discordance > 5%", bad),
                      ("without Harris County Sheriff only", {"Harris"})]:
        r = arrestee_ratios(stages, natpop, drop)
        for x in r.itertuples():
            rows_out.append(dict(universe=lab, arrestees=x.arrestees, offence=x.offence, RR_H_NHW=x.RR_H_NHW,
                                 local_share_H=x.local_share_H, national_share_H=x.national_share_H))
    ar = pd.DataFrame(rows_out)
    ar.to_csv(OUT / "nibrs_arrestee_ratios_booking.csv", index=False, float_format="%.4f", lineterminator="\n")
    say(ar.pivot_table(index=["arrestees", "universe"], columns="offence", values="RR_H_NHW", sort=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n-- 2. Validation-adjusted allocation of offenders recorded without ethnicity --")
    val = pd.read_csv(OUT / "nibrs_arrestee_validation.csv")
    base = ni.chain_probs(df, [], 0.0)
    # recompute the validation pooled over offences, excluding agencies with booking discordance
    known_eth = df[HC + NHK].sum(axis=1)
    a_h = df[ni.ARR_H].sum(axis=1)
    a_k = a_h + df[ni.ARR_NH].sum(axis=1)
    m = (known_eth < 1e-9) & (df.NOINFO < 1e-9) & (a_k > 0)
    names = df[["state", "year", "agency_id"]].merge(ag[["state", "year", "agency_id", "pub_agency_name"]],
                                                     on=["state", "year", "agency_id"], how="left").pub_agency_name
    m_ok = m & ~names.isin(bad).to_numpy()
    unk = df[["UW", "UB", "UO", "UU"]].sum(axis=1)
    out = []
    for lab, mm in [("all agencies", m), ("without booking-discordant agencies", m_ok),
                    ("without booking-discordant agencies and Lake Havasu City", m_ok & ~names.eq("Lake Havasu City").to_numpy())]:
        obs = float((unk[mm] * a_h[mm] / a_k[mm]).sum() / unk[mm].sum())
        al = ni.allocate_rows(df[mm], base[mm])
        imp = float(al.H.sum() / al.sum(axis=1).sum())
        out.append(dict(sample=lab, victimisations=int(mm.sum()), arrestee_H=obs, central_imputed_H=imp, factor=obs / imp))
        say(f"   {lab}: n {int(mm.sum()):,}; arrestees Hispanic {obs:.3f}; central imputes {imp:.3f}; factor {obs / imp:.3f}")
    fac = pd.DataFrame(out)
    fac.to_csv(OUT / "nibrs_validation_factor.csv", index=False, float_format="%.4f", lineterminator="\n")
    res = [ni.ratios(df, ni.allocate_rows(df, base), P, "central", natpop)]
    for x in fac.itertuples():
        res.append(ni.ratios(df, validation_adjusted(df, P, base, x.factor), P,
                             f"validation-adjusted ({x.sample}, factor {x.factor:.2f})", natpop))
    R = pd.concat(res, ignore_index=True)
    cen = R[R.method.eq("central")].set_index("offence")
    R["dRR_H_NHW_vs_central"] = R.RR_H_NHW / R.offence.map(cen.RR_H_NHW) - 1
    R.to_csv(OUT / "nibrs_validation_adjusted.csv", index=False, float_format="%.6f", lineterminator="\n")
    say(R.pivot_table(index="method", columns="offence", values="RR_H_NHW", sort=False)[nr.OFFENCES]
        .to_string(float_format=lambda x: f"{x:.3f}"))

    say("\n-- 3. Recording threshold: bands of agencies, allocations a, k, b, c --")
    thr = []
    for lo, hi in [(0.5, 0.8), (0.8, 0.95), (0.95, 1.01), (0.5, 1.01)]:
        for alloc in ["a", "k", "b", "c"]:
            sp = {**nr.CENTRAL, "thresh": lo, "alloc": alloc}
            st2 = {}
            for k, d in stages.items():
                d2 = dict(d)
                d2["agencies"] = d["agencies"][d["agencies"].rec_rate.fillna(0).lt(hi)]
                st2[k] = d2
            r, _ = nr.results(st2, sp, natpop, f"{lo}-{hi}")
            for x in r.itertuples():
                thr.append(dict(band=f"[{lo:.2f}, {min(hi, 1):.2f}{']' if hi > 1 else ')'}", allocation=alloc, offence=x.offence,
                                RR_H_NHW=x.RR_H_NHW, RR_H_all=x.RR_H_all, rate_H=x.rate_H, rate_NHW=x.rate_NHW,
                                pop_H=x.pop_H, pop_NHW=x.pop_NHW, share_noinfo=x.share_noinfo,
                                share_eth_unknown=x.share_eth_unknown))
    T = pd.DataFrame(thr)
    T.to_csv(OUT / "nibrs_threshold_bands.csv", index=False, float_format="%.5f", lineterminator="\n")
    say(T[T.offence.isin(["Murder", "Robbery"])].pivot_table(index=["offence", "band"], columns="allocation",
                                                             values="RR_H_NHW", sort=False)
        .to_string(float_format=lambda x: f"{x:.3f}"))
    say(T[T.offence.isin(["Murder", "Robbery"]) & T.allocation.eq("a")][
        ["offence", "band", "RR_H_all", "rate_H", "rate_NHW", "pop_H", "pop_NHW", "share_noinfo", "share_eth_unknown"]]
        .to_string(index=False, float_format=lambda x: f"{x:.3f}" if abs(x) < 100 else f"{x:,.0f}"))
    (OUT / "nibrs_checks_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
