"""Dollar implications of this lane's findings: the justice key inside the account and victims'
harm beside it.

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/dollar_effects.py

Victims' harm: the victim-cost lane's model (crime_victim_cost_2026_09_23/victim_cost.py) is run
unchanged through the NIBRS lane's read-only rerun helper, after its central ($28.92bn full,
$4.50bn tangible) is reproduced. Changed inputs:
  murder     P(offender Hispanic | victim group) from each SHR imputation method (shr_impute.py)
  mixed      NCVS table 13 counts a multiple-offender group as Hispanic only if every offender
             was perceived Hispanic; groups with some Hispanic offenders sit in "Other". The
             Select file puts them in Hispanic (ncvs_units.py). Share theta of those incidents
             moved from Other to Hispanic within each victim row: 0 (lane), 0.5, 1.
Justice key (cj_use_allocation_2026_09_23): the arrest-keyed dollars are linear in the Hispanic
arrest ratio RR (its sensitivity RR -> 1 is -$2.750bn at RR 1.1454); prisons from the jail arm.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import numpy as np
import pandas as pd

import nibrs_base as nb  # noqa: F401  (puts the NIBRS lane on sys.path)
import nibrs_impute as ni
import victim_cost_rerun as vcr  # the NIBRS lane's read-only helper around the victim lane

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
FISCAL = HERE.parent
CJ = FISCAL / "cj_use_allocation_2026_09_23"
GROUP_COL = {"hispanic": "p_H_given_vH", "nh_white": "p_H_given_vNHW", "nh_black": "p_H_given_vNHB",
             "nh_other": "p_H_given_vNHO"}
LOG: list[str] = []


def say(s: str = "") -> None:
    print(s, flush=True)
    LOG.append(s)


def gate(name: str, ok: bool, detail: str) -> None:
    say(f"[gate] {name}: {'PASS' if ok else 'FAIL'} - {detail}")
    if not ok:
        raise SystemExit(f"[BLOCKED] gate failed: {name}")


def victims(rows: list) -> None:
    vc = vcr.load_victim_lane()
    S = vcr.setup(vc)
    held = pd.read_csv(vcr.VL / "derived/arms.csv").set_index("arm")
    cen = vcr.run(vc, S)
    gate("victim lane central reproduced", abs(cen["full"] / 1e9 - held.loc["central", "full_bn"]) < 1e-3
         and abs(cen["tangible"] / 1e9 - held.loc["central", "tangible_bn"]) < 1e-3,
         f"full ${cen['full'] / 1e9:.4f}bn, tangible ${cen['tangible'] / 1e9:.4f}bn, murder ${cen['murder_full'] / 1e9:.4f}bn")
    base = dict(full=cen["full"] / 1e9, tangible=cen["tangible"] / 1e9, murder=cen["murder_full"] / 1e9)

    def add(item, method, r, ref, note=""):
        rows.append(dict(line="victims' harm (beside the account)", item=item, method=method,
                         full_bn=r["full"] / 1e9, tangible_bn=r["tangible"] / 1e9, murder_full_bn=r["murder_full"] / 1e9,
                         delta_full_bn=r["full"] / 1e9 - ref["full"], delta_tangible_bn=r["tangible"] / 1e9 - ref["tangible"],
                         note=note))

    # murder: SHR imputation methods, 2024 window (central) and 2022-2024 (the lane's window arm)
    spec = pd.read_csv(OUT / "shr_imputation_specs.csv")
    p0 = S["hom"]["p"]
    for window in ["2024", "2022_2024"]:
        sp = spec[spec.window.astype(str).eq(window)]
        lane_row = sp[sp.method.str.startswith("victim lane")].iloc[0]
        for g, c in GROUP_COL.items():
            gate(f"SHR lane row equals the victim lane's P ({window}, {g})",
                 abs(p0.loc[(window, g), "p_off_hispanic"] - lane_row[c]) < 5e-7,
                 f"{p0.loc[(window, g), 'p_off_hispanic']:.6f}")
        ref = None
        for x in sp.itertuples():
            p = p0.copy()
            for g, c in GROUP_COL.items():
                p.loc[(window, g), "p_off_hispanic"] = getattr(x, c)
            S2 = dict(S, hom=dict(S["hom"], p=p))
            r = vcr.run(vc, S2, hom_window=window)
            if ref is None:
                ref = dict(full=r["full"] / 1e9, tangible=r["tangible"] / 1e9, murder=r["murder_full"] / 1e9)
            add("murder: SHR imputation of unknown offenders", f"{window}: {x.method}", r, ref,
                "delta against the same window's lane row" + ("" if window == "2024" else " (window arm, not central)"))

    # non-fatal: mixed-offender groups (NCVS all-Hispanic rule vs the Select file's coding)
    fac = pd.read_csv(OUT / "ncvs_victimization_factor.csv").set_index("victim")
    I0 = S["nc"]["I"]
    mt = mixed_theta()
    mt.to_csv(OUT / "nibrs_mixed_group_hispanic_fraction.csv", index=False, float_format="%.6f", lineterminator="\n")
    say("\n-- NIBRS: mean Hispanic fraction of mixed Hispanic / non-Hispanic offender groups --")
    say(mt.to_string(index=False, float_format=lambda z: f"{z:.4f}"))
    theta_nibrs = float(mt.loc[mt.offence.eq("All five"), "mean_hispanic_fraction"].iloc[0])
    # the Select file's Hispanic excess over table 13, and the part matched by its Other deficit
    u = pd.read_csv(OUT / "ncvs_victimizations_per_incident.csv")
    u = u[u.year.astype(str).eq("2022-2024")].set_index(["victim", "offender"])
    excess, matched = {}, {}
    for v in ["White", "Black", "Hispanic", "Other"]:
        r_v = fac.loc[v, "lane_row_ratio"]
        excess[v] = fac.loc[v, "select_victimizations"] / r_v - fac.loc[v, "hispanic_offender_incidents"]
        deficit = u.loc[(v, "Other"), "published_incidents"] - u.loc[(v, "Other"), "select_victimizations"] / r_v
        matched[v] = max(0.0, min(excess[v], deficit))
    say(f"   Select Hispanic excess over table 13, incidents 2022-2024: {sum(excess.values()):,.0f}; "
        f"matched by the Other deficit in the same victim row: {sum(matched.values()):,.0f}")
    for theta, move, lab in [(0.0, excess, ""), (0.5, excess, ""), (theta_nibrs, excess, " (NIBRS TX+AZ mean Hispanic "
                             "fraction of mixed groups)"), (theta_nibrs, matched, " (NIBRS fraction; only the excess "
                             "matched by the Other deficit)"), (1.0, excess, "")]:
        I2 = I0.copy()
        for v in ["White", "Black", "Hispanic", "Other"]:
            I2.loc[v, "Hispanic"] += theta * move[v]
            I2.loc[v, "Other"] -= theta * move[v]
        gate(f"mixed-group move keeps known-offender incidents (theta {theta:.4f})",
             abs(I2.drop(columns="Unknown").to_numpy().sum() - I0.drop(columns="Unknown").to_numpy().sum()) < 1, "")
        r = vcr.run(vc, dict(S, nc=dict(S["nc"], I=I2)))
        add("non-fatal: mixed-offender groups with a Hispanic member",
            f"theta {theta:.4f} of each group attributed Hispanic{lab}", r, base,
            "theta 0 is the lane (NCVS table 13 all-Hispanic rule); 1 is the Select file's coding")
    say(pd.DataFrame([r for r in rows if r["line"].startswith("victims")])[
        ["item", "method", "full_bn", "tangible_bn", "murder_full_bn", "delta_full_bn", "delta_tangible_bn"]]
        .to_string(index=False, float_format=lambda z: f"{z:.3f}"))


@lru_cache(maxsize=1)
def nibrs_df() -> pd.DataFrame:
    stages, _ = nb.load()
    return ni.spec_rows(ni.load_rows(), stages, nb.lane_specs()["central"])[0]


def mixed_theta() -> pd.DataFrame:
    """Mean Hispanic fraction of offender groups that mix Hispanic and non-Hispanic members (known
    ethnicity, two or more offenders), NIBRS TX+AZ central agencies: the police-recorded analogue
    of theta for the NCVS mixed groups."""
    df = nibrs_df()
    h = df[ni.HC].sum(axis=1)
    k = h + df[["NHW", "NHB", "NHO", "NHU"]].sum(axis=1)
    mixed = (df.n_known >= 2) & (h > 1e-9) & (k - h > 1e-9)
    out = [dict(offence="All five", victimisations=int(mixed.sum()), mean_hispanic_fraction=float((h / k)[mixed].mean()))]
    for o, g in df[mixed].groupby("offence"):
        out.append(dict(offence=o, victimisations=len(g), mean_hispanic_fraction=float((h / k)[g.index].mean())))
    return pd.DataFrame(out)


def booking_factors() -> pd.DataFrame:
    """Offender-segment vs arrestee-segment Hispanic share in single-offender, single-arrestee
    victimisations (TX+AZ central agencies): the relative understatement of Hispanic arrestees."""
    df = nibrs_df()
    NHK = ["NHW", "NHB", "NHO", "NHU"]
    a_h = df[ni.ARR_H].sum(axis=1)
    a_nh = df[ni.ARR_NH].sum(axis=1)
    one = (df.n_known == 1) & ((a_h + a_nh) == 1) & (df[ni.ARR_U].sum(axis=1) == 0) & (df[ni.HC + NHK].sum(axis=1) > 0.999)
    d = df[one].assign(off_H=df.loc[one, ni.HC].sum(axis=1) > 0.5, arr_H=a_h[one] > 0)
    out = []
    for lab, m in [("all ages, all five offences", np.ones(len(d), bool)), ("offender 18+, all five", d.off_age.ge(18)),
                   ("all ages, murder", d.offence.eq("Murder")), ("all ages, robbery", d.offence.eq("Robbery")),
                   ("all ages, aggravated assault", d.offence.eq("Aggravated assault")),
                   ("Texas only", d.state.eq("TX")), ("Arizona only", d.state.eq("AZ"))]:
        z = d[m]
        so, sa = z.off_H.mean(), z.arr_H.mean()
        out.append(dict(universe=lab, single_pairs=len(z), offender_segment_H=so, arrestee_segment_H=sa, factor=so / sa))
    return pd.DataFrame(out)


def justice(rows: list) -> None:
    s = json.loads((CJ / "derived/summary.json").read_text())
    rr = s["arrests"]["rr_hisp"]
    d_rr1 = s["sensitivity_delta_bn"]["arrest_rr_hispanic_1"]
    slope = -d_rr1 / (rr - 1)                       # $bn per unit of RR (the key is linear in RR)
    gate("cj lane arrest ratio and RR->1 sensitivity", abs(rr - 1.1454) < 1e-4 and abs(d_rr1 + 2.750) < 1e-3,
         f"RR {rr:.4f}, RR->1 {d_rr1:+.3f}bn, arrest-keyed dollars {slope * rr:.2f}bn")
    bf = booking_factors()
    bf.to_csv(OUT / "booking_factors.csv", index=False, float_format="%.6f", lineterminator="\n")
    say("\n-- booking discordance factors (offender-segment / arrestee-segment Hispanic share) --")
    say(bf.to_string(index=False, float_format=lambda z: f"{z:.4f}"))
    for x in bf.itertuples():
        rows.append(dict(line="justice key (inside the account)", item="arrest key: booking under-records Hispanic arrestees",
                         method=f"RR x {x.factor:.4f} ({x.universe}, TX+AZ NIBRS)", delta_main_case_bn=slope * rr * (x.factor - 1),
                         note="[INFERENCE] national transfer of the TX+AZ booking discordance; 0 if national arrest "
                              "tables book ethnicity as the offender records do"))
    rows.append(dict(line="justice key (inside the account)", item="arrest key: White-subtraction (Arm 5)", method="none",
                     delta_main_case_bn=0.0, note="the arrest key is Hispanic / all adults; no NH-white construction"))
    rows.append(dict(line="justice key (inside the account)", item="arrest key: census undercount of Hispanics (PES)",
                     method="A_T x RR", delta_main_case_bn=0.0,
                     note="cancels: a larger true group raises A_T and lowers RR by the same factor"))
    j = pd.read_csv(OUT / "jail_bjs_arm.csv")
    k = pd.read_csv(OUT / "jail_acs_key_sensitivity.csv")
    say(f"\n[info] jail arm rows {len(j)}, ACS sensitivity rows {len(k)}")
    jr = j[j.overlap_rule.eq("none")]
    cen = jr[jr.method.eq("survey_or_mean_post2000")].iloc[0]
    gate("jail worker's BJS-arm central (survey OR mean) re-derived by hand: 0.2186 x 0.70734 key, +$1.54bn",
         abs(cen.bjs_check_key - 0.21860 * 0.142788 / 0.201866) < 2e-4 and abs(cen.delta_bn_vs_central_prisons - 1.54) < 0.01,
         f"key {cen.bjs_check_key:.4f}, {cen.delta_bn_vs_central_prisons:+.3f}bn")
    for x in jr.itertuples():
        rows.append(dict(line="justice key (inside the account)", item="prisons: BJS check arm with corrected jail share",
                         method=f"jail share {x.method} ({x.jail_H_share:.4f})", delta_main_case_bn=0.0,
                         delta_check_arm_bn=float(x.delta_bn_vs_central_prisons),
                         note="check arm only; the adopted prisons key is ACS custody, so the main case does not move"))
    for x in k.itertuples():
        rows.append(dict(line="justice key (inside the account)", item="prisons: ACS custody key / f (facility recording)",
                         method=f"{x.instrument}; jail {x.jail_method}; {x.universe}; f {x.record_ratio_f:.3f}",
                         delta_main_case_bn=float(x.delta_bn_vs_central_prisons),
                         note="one-sided sensitivity, not adopted; passes 1:1 into the main case if adopted"))


def main() -> None:
    OUT.mkdir(exist_ok=True)
    rows: list = []
    victims(rows)
    justice(rows)
    D = pd.DataFrame(rows)
    D.to_csv(OUT / "dollar_effects.csv", index=False, float_format="%.6f", lineterminator="\n")
    jk = D[D.line.str.startswith("justice")]
    say("\n-- justice key --")
    say(jk[["item", "method", "delta_main_case_bn"]].to_string(index=False, float_format=lambda z: f"{z:+.3f}"))
    (OUT / "dollar_effects_log.txt").write_text("\n".join(LOG) + "\n")


if __name__ == "__main__":
    main()
