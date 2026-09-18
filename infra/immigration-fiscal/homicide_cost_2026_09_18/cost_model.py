"""Treasury cost of one homicide in the repo's period-profile frame.

Three channels, all in 2024 dollars:
  victim     remaining lifetime fiscal balance from the age at death, partial account
             and with the complete-account per-person-year shift
  children   SSA child survivor benefits, the widowed-parent benefit, the lump sum,
             and a foster-care arm for children whose only resident parent is the victim
  offender   corrections at the ledger's per-prisoner-year cost, a life-sentence arm,
             and the offender's own foregone fiscal profile while imprisoned

The victim distribution each offender group produces comes from the SHR (universe A,
cleared single-victim/single-offender criminal homicides, 2019-2023) reweighted so the
victim ethnicity x age x sex marginal matches CDC WONDER X85-Y09 deaths for 2019-2023.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

PROFILES = FISCAL / "pronatal_equivalence_2026_09_18/derived/age_profiles_references.csv"
AUDIT = FISCAL / "gap_interest_2026_09_18/derived/audit.json"
BANDS = {0: (0, 18), 1: (18, 25), 2: (25, 35), 3: (35, 45), 4: (45, 55), 5: (55, 65),
         6: (65, 75), 7: (75, 83)}
TERMINAL = 83                      # the period profile's constructed lifetime
CORRECTIONS = 59_619.0             # crime_cost_2026_09_16, 2024 dollars per prisoner-year
TIME_SERVED_MURDER = 15.0          # BJS released prisoners, mean years, murder
SOCIAL_COST_MURDER = 13_087_784.0  # crime_cost_2026_09_16, McCollister restated to 2024$
VICTIM_TANGIBLE = 1_074_537.0

# SHR ethnicity -> available fiscal profile
PROFILE_FOR = {"hispanic": "mexican_observed_total", "nh_white": "third_plus_nh_white",
               "nh_black": "all_native", "nh_other": "all_native"}


def load_profiles() -> tuple[pd.DataFrame, dict]:
    p = pd.read_csv(PROFILES)
    wide = p.pivot(index="band", columns="group", values="balance_per_person")
    pop = p.pivot(index="band", columns="group", values="population")
    mex = ["mexico_born", "mexican_second_gen", "mexican_third_plus_selfid"]
    wide["mexican_observed_total"] = ((wide[mex] * pop[mex]).sum(axis=1) / pop[mex].sum(axis=1))
    pop["mexican_observed_total"] = pop[mex].sum(axis=1)
    shift = json.loads(AUDIT.read_text())["complete_minus_partial_per_person_year"]
    shift["all_native"] = shift["all_native"]
    return wide, shift


def by_age(wide: pd.DataFrame, group: str) -> np.ndarray:
    """Per-person-year balance at each single year of age 0..82."""
    out = np.zeros(TERMINAL)
    for b, (lo, hi) in BANDS.items():
        out[lo:hi] = wide.loc[b, group]
    return out


def remaining(prof: np.ndarray, age: float, rate: float, shift: float = 0.0) -> float:
    a = int(np.clip(round(age), 0, TERMINAL - 1))
    yrs = np.arange(a, TERMINAL)
    disc = (1.0 + rate) ** (-(yrs - a))
    return float(((prof[a:] + shift) * disc).sum())


# --------------------------------------------------------------------------- victims
def wonder_victims() -> pd.DataFrame:
    w = pd.read_csv(OUT / "wonder_deaths_age_hispanic_race_sex_2019_2023.csv")
    w = w[w.deaths.notna()]
    mid = {"< 1 year": 0.5, "1-4 years": 3, "5-9 years": 7, "10-14 years": 12,
           "15-19 years": 17, "20-24 years": 22, "25-29 years": 27, "30-34 years": 32,
           "35-39 years": 37, "40-44 years": 42, "45-49 years": 47, "50-54 years": 52,
           "55-59 years": 57, "60-64 years": 62, "65-69 years": 67, "70-74 years": 72,
           "75-79 years": 77, "80-84 years": 82, "85-89 years": 82, "90-94 years": 82,
           "95-99 years": 82, "100+ years": 82, "Not Stated": np.nan}
    w["age_mid"] = w.age5.map(mid)
    w = w[w.age_mid.notna()]
    eth = np.where(w.hispanic_origin.eq("Hispanic or Latino"), "hispanic",
                   np.where(w.race.eq("White"), "nh_white",
                            np.where(w.race.eq("Black or African American"), "nh_black",
                                     "nh_other")))
    w["vic_eth"] = np.where(w.hispanic_origin.eq("Not Stated"), "unknown", eth)
    w["sex"] = w.sex.str.lower()
    w["band5"] = w.age5
    return w


def victim_cost_table(wide, shift) -> pd.DataFrame:
    rows = []
    for eth, group in [("nh_white", "third_plus_nh_white"),
                       ("hispanic", "mexican_observed_total"),
                       ("hispanic_mexico_born", "mexico_born"),
                       ("hispanic_second_gen", "mexican_second_gen"),
                       ("hispanic_third_plus", "mexican_third_plus_selfid"),
                       ("all_native_reference", "all_native")]:
        prof = by_age(wide, group)
        sh = shift.get(group, shift["all_native"])
        for lo, hi in [(0, 18), (18, 25), (25, 35), (35, 45), (45, 55), (55, 65),
                       (65, 75), (75, 83)]:
            a = (lo + hi - 1) / 2
            rows.append(dict(
                victim_eth=eth, profile=group, band=f"{lo}-{hi-1}", age_mid=a,
                partial_r0=remaining(prof, a, 0.0),
                partial_r3=remaining(prof, a, 0.03),
                complete_r0=remaining(prof, a, 0.0, sh),
                complete_r3=remaining(prof, a, 0.03, sh),
                complete_shift_per_year=sh))
    return pd.DataFrame(rows)


# --------------------------------------------------------------------------- children
def child_params() -> dict:
    p = json.loads((OUT / "external_params.json").read_text())
    return {k: (v.get("value") if isinstance(v, dict) else v) for k, v in p.items()}


CPS_GROUP = {"hispanic": "mexican_observed_total", "nh_white": "third_plus_nh_white",
             "nh_black": "all_native", "nh_other": "all_native"}
CPS_BANDS = ["18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]


def cps_lookup() -> pd.DataFrame:
    c = pd.read_csv(OUT / "cps_parent_channel_by_age.csv")
    return c.set_index(["group", "sex", "band"])


def cps_band(age: float) -> str | None:
    if age < 18:
        return None
    for lab, (lo, hi) in zip(CPS_BANDS, [(18, 25), (25, 35), (35, 45), (45, 55),
                                         (55, 65), (65, 75), (75, 200)]):
        if lo <= age < hi:
            return lab
    return None


def child_cost(age, sex, eth, params, cps, foster_share=0.0, rate=0.0):
    band = cps_band(age)
    if band is None:
        return dict(child_years=0.0, ssa_child=0.0, ssa_spouse=0.0, lump=float(params["ssa_lump_sum_death_payment"]),
                    foster=0.0, total=float(params["ssa_lump_sum_death_payment"]))
    try:
        r = cps.loc[(CPS_GROUP[eth], sex, band)]
    except KeyError:
        return dict(child_years=0.0, ssa_child=0.0, ssa_spouse=0.0, lump=0.0, foster=0.0, total=0.0)
    child_years = float(r.mean_child_years)
    sole_years = float(r.mean_sole_child_years)
    yrs16 = float(r.mean_years_to_16_max)
    disc = 1.0 if rate == 0 else (1 - (1 + rate) ** -max(child_years, 1e-9)) / (rate * max(child_years, 1e-9))
    ssa_child = 12 * params["ssa_child_survivor_avg_monthly"] * child_years * disc
    spouse_years = max(yrs16 - 0.0, 0.0) * (1 - sole_years / max(child_years, 1e-9)) if child_years else 0.0
    ssa_spouse = 12 * params["ssa_widowed_mother_father_avg_monthly"] * spouse_years
    foster = foster_share * sole_years * params["foster_care_cost_per_child_year"]
    lump = float(params["ssa_lump_sum_death_payment"])
    return dict(child_years=child_years, sole_child_years=sole_years, ssa_child=ssa_child,
                ssa_spouse=ssa_spouse, lump=lump, foster=foster,
                total=ssa_child + ssa_spouse + lump + foster)


# --------------------------------------------------------------------------- offender
def offender_cost(age, eth, wide, shift, life_share, rate=0.0, complete=False):
    group = PROFILE_FOR.get(eth, "all_native")
    prof = by_age(wide, group)
    sh = shift.get(group, shift["all_native"]) if complete else 0.0
    life_years = max(TERMINAL - 1 - age, 0.0)
    years = life_share * life_years + (1 - life_share) * TIME_SERVED_MURDER
    a = int(np.clip(round(age), 0, TERMINAL - 1))
    end = int(min(TERMINAL, a + round(years)))
    t = np.arange(a, end)
    disc = (1.0 + rate) ** (-(t - a))
    corrections = float(CORRECTIONS * disc.sum())
    foregone = float(((prof[a:end] + sh) * disc).sum())
    return dict(years=years, corrections=corrections, foregone=foregone,
                total=corrections + foregone)


# --------------------------------------------------------------------------- main
def main() -> None:
    wide, shift = load_profiles()
    params = child_params()
    cps = cps_lookup()
    life_share = float(params["bjs_life_sentence_share_murder"])

    vt = victim_cost_table(wide, shift)
    vt.round(0).to_csv(OUT / "victim_remaining_balance.csv", index=False)
    print("[victim remaining lifetime balance, per person, 2024$]")
    print(vt[vt.victim_eth.isin(["nh_white", "hispanic"])].round(0).to_string(index=False))

    # ---- victim weights: SHR universe A reweighted to the WONDER victim marginal
    shr = pd.read_csv(OUT / "shr_joint_2019_2023.csv")
    vic_sex = pd.read_csv(OUT / "shr_vic_age_single_year_2019_2023.csv")
    wnd = wonder_victims()

    # WONDER marginal by victim ethnicity x 5-year band (drop 'unknown' ethnicity: 0.2%)
    wm = wnd[wnd.vic_eth.ne("unknown")].groupby(["vic_eth", "band5", "sex"]).deaths.sum()
    wm = wm / wm.sum()

    # SHR cleared single-single, ethnicity known on both sides
    A = shr[shr.off_eth.ne("unknown") & shr.vic_eth.ne("unknown")
            & shr.vic_band.ne("unknown")].copy()
    band_map = {"0-4": "1-4 years", "5-9": "5-9 years", "10-14": "10-14 years",
                "15-19": "15-19 years", "20-24": "20-24 years", "25-29": "25-29 years",
                "30-34": "30-34 years", "35-39": "35-39 years", "40-44": "40-44 years",
                "45-49": "45-49 years", "50-54": "50-54 years", "55-59": "55-59 years",
                "60-64": "60-64 years", "65-69": "65-69 years", "70-74": "70-74 years",
                "75-79": "75-79 years", "80-84": "80-84 years", "85+": "85-89 years"}
    A["band5"] = A.vic_band.map(band_map)
    A = A[A.band5.notna()]
    mids = {"< 1 year": 0.5, "1-4 years": 3, "5-9 years": 7, "10-14 years": 12,
            "15-19 years": 17, "20-24 years": 22, "25-29 years": 27, "30-34 years": 32,
            "35-39 years": 37, "40-44 years": 42, "45-49 years": 47, "50-54 years": 52,
            "55-59 years": 57, "60-64 years": 62, "65-69 years": 67, "70-74 years": 72,
            "75-79 years": 77, "80-84 years": 82, "85-89 years": 82}
    A["vic_age_mid"] = A.band5.map(mids)
    A["off_age_mid"] = A.off_band.map(band_map).map(mids)
    A = A[A.off_age_mid.notna()]

    # sex split of victims inside each (eth, band) from the SHR single-year file
    vs = vic_sex[vic_sex.VicSex.isin(["Male", "Female"]) & vic_sex.vic_eth.ne("unknown")].copy()
    vs["band5"] = pd.cut(vs.vic_age_n, bins=[-.1, .99, 4.99, 9.99, 14.99, 19.99, 24.99, 29.99,
                                             34.99, 39.99, 44.99, 49.99, 54.99, 59.99, 64.99,
                                             69.99, 74.99, 79.99, 200],
                         labels=["< 1 year", "1-4 years", "5-9 years", "10-14 years",
                                 "15-19 years", "20-24 years", "25-29 years", "30-34 years",
                                 "35-39 years", "40-44 years", "45-49 years", "50-54 years",
                                 "55-59 years", "60-64 years", "65-69 years", "70-74 years",
                                 "75-79 years", "80-84 years"])
    sexshare = (vs.groupby(["vic_eth", "band5", "VicSex"], observed=True).n.sum()
                  .rename("n").reset_index())
    tot = sexshare.groupby(["vic_eth", "band5"], observed=True).n.transform("sum")
    sexshare["share"] = sexshare.n / tot
    sexshare["sex"] = sexshare.VicSex.str.lower()
    sexshare["band5"] = sexshare.band5.astype(str)

    # SHR cell weights, then reweight so the (eth, band, sex) marginal matches WONDER
    A = A.merge(sexshare[["vic_eth", "band5", "sex", "share"]], on=["vic_eth", "band5"],
                how="left")
    A["n_sex"] = A.n * A.share.fillna(0.5)
    shr_marg = A.groupby(["vic_eth", "band5", "sex"]).n_sex.sum()
    shr_marg = shr_marg / shr_marg.sum()
    scale = (wm / shr_marg).replace([np.inf, -np.inf], np.nan)
    A = A.join(scale.rename("scale"), on=["vic_eth", "band5", "sex"])
    A["w"] = A.n_sex * A.scale.fillna(0.0)
    cov = pd.DataFrame({"shr_share": shr_marg, "wonder_share": wm, "scale": scale}).dropna()
    cov.round(5).to_csv(OUT / "shr_to_wonder_scaling.csv")
    print(f"\n[scaling] SHR universe-A cells {len(A):,}; weight retained "
          f"{A.w.sum()/A.n_sex.sum():.3f} of the raw cell weight")

    # ---- per-homicide expected treasury cost by offender ethnicity
    out = []
    for foster_share in [0.0, 0.25, 1.0]:
        for rate in [0.0, 0.03]:
            for complete in [False, True]:
                for life in [0.0, life_share, 1.0]:
                    for off_eth, g in A.groupby("off_eth"):
                        w = g.w.to_numpy()
                        if w.sum() <= 0:
                            continue
                        vic, ch, off = [], [], []
                        for _, r in g.iterrows():
                            prof = by_age(wide, PROFILE_FOR[r.vic_eth])
                            sh = shift.get(PROFILE_FOR[r.vic_eth], shift["all_native"]) if complete else 0.0
                            vic.append(remaining(prof, r.vic_age_mid, rate, sh))
                            ch.append(child_cost(r.vic_age_mid, r.sex if isinstance(r.sex, str) else "all",
                                                 r.vic_eth, params, cps, foster_share, rate)["total"])
                            off.append(offender_cost(r.off_age_mid, off_eth, wide, shift,
                                                     life, rate, complete)["total"])
                        vic, ch, off = np.array(vic), np.array(ch), np.array(off)
                        out.append(dict(
                            off_eth=off_eth, rate=rate, account="complete" if complete else "partial",
                            life_share=life, foster_share=foster_share,
                            n_cells=len(g), weight=float(w.sum()),
                            victim_balance=float(np.average(vic, weights=w)),
                            child_cost=float(np.average(ch, weights=w)),
                            offender_cost=float(np.average(off, weights=w)),
                            total=float(np.average(vic + ch + off, weights=w)),
                            mean_victim_age=float(np.average(g.vic_age_mid, weights=w)),
                            mean_offender_age=float(np.average(g.off_age_mid, weights=w))))
    res = pd.DataFrame(out)
    res.to_csv(OUT / "treasury_cost_per_homicide.csv", index=False)

    central = res[(res.rate == 0.0) & (res.account == "partial")
                  & (res.life_share == life_share) & (res.foster_share == 0.0)]
    print("\n[central arm: partial account, undiscounted, life share "
          f"{life_share:.3f}, no foster arm] treasury dollars per cleared homicide")
    print(central[["off_eth", "mean_offender_age", "mean_victim_age", "victim_balance",
                   "child_cost", "offender_cost", "total"]].round(0).to_string(index=False))

    comp = res[(res.rate == 0.0) & (res.account == "complete")
               & (res.life_share == life_share) & (res.foster_share == 0.0)]
    print("\n[complete account, undiscounted]")
    print(comp[["off_eth", "victim_balance", "child_cost", "offender_cost", "total"]]
          .round(0).to_string(index=False))

    # victim-side-only table by victim ethnicity and age band, both accounts
    rows = []
    for (eth, band), g in A.groupby(["vic_eth", "band5"]):
        prof = by_age(wide, PROFILE_FOR[eth])
        sh = shift.get(PROFILE_FOR[eth], shift["all_native"])
        a = mids[band]
        rows.append(dict(vic_eth=eth, band=band, age_mid=a, weight=float(g.w.sum()),
                         partial_r0=remaining(prof, a, 0.0), partial_r3=remaining(prof, a, 0.03),
                         complete_r0=remaining(prof, a, 0.0, sh),
                         complete_r3=remaining(prof, a, 0.03, sh)))
    pd.DataFrame(rows).round(0).to_csv(OUT / "victim_balance_by_cell.csv", index=False)
    print(f"\n[written] {OUT}/treasury_cost_per_homicide.csv and 3 more")


if __name__ == "__main__":
    main()
