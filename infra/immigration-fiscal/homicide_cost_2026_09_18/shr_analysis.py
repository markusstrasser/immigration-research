"""Joint distribution of US homicide victim x offender ethnicity, age, relationship
and circumstance, from the FBI Supplementary Homicide Reports as compiled by the
Murder Accountability Project (SHR76_25a.csv, 1976-2025).

Universes
  A  single victim / single offender, cleared, criminal homicide  (the clean cell)
  B  every victim with a known offender (first offender's fields), cleared, criminal
Justifiable homicides (felon killed by police / by a private citizen) are excluded from
both and reported separately.  Writes derived/shr_*.csv.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
RAW = HERE / "_cache/SHR76_25a.csv"
OUT = HERE / "derived"
OUT.mkdir(exist_ok=True)

COLS = ["Year", "State", "Solved", "Situation", "VicAge", "VicSex", "VicRace", "VicEthnic",
        "OffAge", "OffSex", "OffRace", "OffEthnic", "Relationship", "Circumstance",
        "Homicide", "Weapon"]
JUSTIFIABLE = {"Felon killed by police", "Felon killed by private citizen"}
ETH_ORDER = ["hispanic", "nh_white", "nh_black", "nh_other", "unknown"]

INTIMATE = {"Wife", "Husband", "Girlfriend", "Boyfriend", "Common-law wife",
            "Common-law husband", "Ex-wife", "Ex-husband", "Homosexual relationship"}
FAMILY = {"Son", "Daughter", "Mother", "Father", "Brother", "Sister", "In-law",
          "Stepfather", "Stepmother", "Stepson", "Stepdaughter", "Other family"}
ACQUAINT = {"Acquaintance", "Friend", "Neighbor", "Employer", "Employee",
            "Other - known to victim"}
STRANGER = {"Stranger"}

CIRC = {
    "argument": {"Other arguments", "Argument over money or property",
                 "Brawl due to influence of alcohol", "Brawl due to influence of narcotics",
                 "Lovers triangle"},
    "felony": {"Robbery", "Burglary", "Larceny", "Motor vehicle theft", "Arson", "Rape",
               "Other sex offense", "Prostitution and commercialized vice", "Gambling",
               "All suspected felony type", "Narcotic drug laws"},
    "gang": {"Juvenile gang killings", "Gangland killings"},
    "other_known": {"Other", "Other - not specified", "Institutional killings",
                    "Sniper attack", "Child killed by babysitter", "Children playing with gun",
                    "Other negligent handling of gun", "Victim shot in hunting accident",
                    "Gun cleaning death - other than self", "All other manslaughter by negligence",
                    "Negligent handling of gun which resulted in death of another",
                    "Abortion", "Other - not specified "},
    "undetermined": {"Circumstances undetermined"},
}


def ethnicity(race: pd.Series, ethnic: pd.Series) -> pd.Series:
    out = pd.Series("unknown", index=race.index, dtype=object)
    nonh = ethnic.eq("Not of Hispanic origin")
    out[nonh & race.eq("White")] = "nh_white"
    out[nonh & race.eq("Black")] = "nh_black"
    out[nonh & race.isin(["Asian", "American Indian or Alaskan Native",
                          "Native Hawaiian or Pacific Islander"])] = "nh_other"
    out[ethnic.eq("Hispanic origin")] = "hispanic"
    return out


def relationship_class(s: pd.Series) -> pd.Series:
    out = pd.Series("unknown", index=s.index, dtype=object)
    out[s.isin(INTIMATE)] = "intimate"
    out[s.isin(FAMILY)] = "family"
    out[s.isin(ACQUAINT)] = "acquaintance"
    out[s.isin(STRANGER)] = "stranger"
    return out


def circumstance_class(s: pd.Series) -> pd.Series:
    out = pd.Series("other_known", index=s.index, dtype=object)
    for k, vals in CIRC.items():
        out[s.isin(vals)] = k
    return out


def age_band(a: pd.Series, width: int = 5, top: int = 85) -> pd.Series:
    a = pd.to_numeric(a, errors="coerce")
    band = np.where(a.isna() | (a >= 999), "unknown",
                    np.where(a >= top, f"{top}+",
                             (a // width * width).astype("Int64").astype(str) + "-" +
                             (a // width * width + width - 1).astype("Int64").astype(str)))
    return pd.Series(band, index=a.index)


def load() -> pd.DataFrame:
    df = pd.read_csv(RAW, usecols=COLS, low_memory=False)
    df = df[df.Homicide.eq("Murder and non-negligent manslaughter")].copy()
    df["justifiable"] = df.Circumstance.isin(JUSTIFIABLE)
    df["vic_eth"] = ethnicity(df.VicRace, df.VicEthnic)
    df["off_eth"] = ethnicity(df.OffRace, df.OffEthnic)
    df["rel"] = relationship_class(df.Relationship)
    df["circ"] = circumstance_class(df.Circumstance)
    df["vic_band"] = age_band(df.VicAge)
    df["off_band"] = age_band(df.OffAge)
    df["vic_age_n"] = pd.to_numeric(df.VicAge, errors="coerce").where(
        lambda s: s.between(0, 120))
    df["off_age_n"] = pd.to_numeric(df.OffAge, errors="coerce").where(
        lambda s: s.between(0, 120))
    return df


def matrix(d: pd.DataFrame, label: str) -> pd.DataFrame:
    t = pd.crosstab(d.vic_eth, d.off_eth).reindex(index=ETH_ORDER, columns=ETH_ORDER,
                                                  fill_value=0)
    t = t.reset_index().melt(id_vars="vic_eth", var_name="off_eth", value_name="n")
    t["universe"] = label
    return t


def main() -> None:
    df = load()
    rows_all = len(df)
    print(f"[load] criminal homicide victim records 1976-2025: {rows_all:,}")

    # ---- missingness by year, all criminal-homicide records -------------------
    m = df[df.Year.between(2010, 2025)]
    miss = m.groupby("Year").agg(
        records=("Year", "size"),
        vic_eth_unknown=("vic_eth", lambda s: (s == "unknown").mean()),
        vic_race_unknown=("VicRace", lambda s: (s == "Unknown").mean()),
        cleared=("Solved", lambda s: (s == "Yes").mean()),
    )
    sol = m[m.Solved.eq("Yes")]
    miss["off_eth_unknown_cleared"] = sol.groupby("Year").off_eth.apply(
        lambda s: (s == "unknown").mean())
    miss["off_race_unknown_cleared"] = sol.groupby("Year").OffRace.apply(
        lambda s: (s == "Unknown").mean())
    miss.round(4).to_csv(OUT / "shr_missingness_by_year.csv")
    print(miss.round(3).to_string())

    for w, (lo, hi) in {"2015_2023": (2015, 2023), "2019_2023": (2019, 2023)}.items():
        d = df[df.Year.between(lo, hi)]
        crim = d[~d.justifiable]
        just = d[d.justifiable]
        A = crim[crim.Situation.eq("Single victim/single offender") & crim.Solved.eq("Yes")]
        B = crim[crim.Solved.eq("Yes")]
        print(f"\n[{w}] criminal-homicide victims {len(crim):,}; justifiable {len(just):,}; "
              f"cleared {len(B):,}; single-single cleared {len(A):,}")

        pd.concat([matrix(A, "svso_cleared"), matrix(B, "all_cleared")]).to_csv(
            OUT / f"shr_vic_off_matrix_{w}.csv", index=False)

        # unsolved share by victim ethnicity
        u = crim.groupby("vic_eth").agg(victims=("Solved", "size"),
                                        cleared=("Solved", lambda s: (s == "Yes").sum()))
        u["unsolved_share"] = 1 - u.cleared / u.victims
        u.to_csv(OUT / f"shr_clearance_by_vic_eth_{w}.csv")
        print(u.round(3).to_string())

        # victim age x victim ethnicity (all criminal homicide victims, not only cleared)
        va = pd.crosstab(crim.vic_band, crim.vic_eth).reindex(columns=ETH_ORDER, fill_value=0)
        va.to_csv(OUT / f"shr_vic_age_by_eth_{w}.csv")
        # offender age x offender ethnicity (cleared only, by construction)
        oa = pd.crosstab(B.off_band, B.off_eth).reindex(columns=ETH_ORDER, fill_value=0)
        oa.to_csv(OUT / f"shr_off_age_by_eth_{w}.csv")

        # relationship by offender x victim ethnicity cell (universe A)
        rel = A.groupby(["off_eth", "vic_eth", "rel"]).size().rename("n").reset_index()
        rel.to_csv(OUT / f"shr_relationship_{w}.csv", index=False)
        circ = A.groupby(["off_eth", "circ"]).size().rename("n").reset_index()
        circ.to_csv(OUT / f"shr_circumstance_{w}.csv", index=False)

        # joint victim-age x offender-age x ethnicity pair, universe A (the cost input)
        joint = A.groupby(["off_eth", "vic_eth", "vic_band", "off_band", "rel"]).size()
        joint.rename("n").reset_index().to_csv(OUT / f"shr_joint_{w}.csv", index=False)

        # mean ages
        ages = A.groupby("off_eth").agg(off_age_mean=("off_age_n", "mean"),
                                        vic_age_mean=("vic_age_n", "mean"), n=("rel", "size"))
        print(ages.round(1).to_string())

        if w == "2019_2023":
            # victim single-year age by ethnicity and sex, universe = all criminal victims
            va1 = crim.groupby(["vic_eth", "VicSex", "vic_age_n"]).size().rename("n").reset_index()
            va1.to_csv(OUT / "shr_vic_age_single_year_2019_2023.csv", index=False)
            just.groupby(["vic_eth", "Circumstance"]).size().rename("n").reset_index().to_csv(
                OUT / "shr_justifiable_2019_2023.csv", index=False)

    # intra-group shares, universe A, both windows
    out = []
    for w, (lo, hi) in {"2015_2023": (2015, 2023), "2019_2023": (2019, 2023)}.items():
        d = df[df.Year.between(lo, hi) & ~df.justifiable]
        A = d[d.Situation.eq("Single victim/single offender") & d.Solved.eq("Yes")]
        known = A[A.off_eth.ne("unknown") & A.vic_eth.ne("unknown")]
        for g in ["hispanic", "nh_white", "nh_black"]:
            sub = known[known.off_eth.eq(g)]
            out.append(dict(window=w, off_eth=g, n=len(sub),
                            intra_share=(sub.vic_eth.eq(g)).mean(),
                            **{f"vic_{k}": (sub.vic_eth.eq(k)).mean()
                               for k in ["hispanic", "nh_white", "nh_black", "nh_other"]}))
    pd.DataFrame(out).round(4).to_csv(OUT / "shr_intra_group.csv", index=False)
    print("\n[intra-group, ethnicity-known cells]")
    print(pd.DataFrame(out).round(3).to_string(index=False))


if __name__ == "__main__":
    main()
