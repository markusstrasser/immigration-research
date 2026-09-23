"""National Household Travel Survey: daily driving by Hispanic origin, all purposes and commuting.

NHTS has no Mexican-origin flag, so Hispanic persons (R_HISP=01) stand in for the group [ASSUMPTION;
about 60% of US Hispanics are of Mexican origin]. The 2017 file adds a southwestern cut (households in
California, Texas, Arizona and New Mexico), where most Hispanics are of Mexican origin.

Quantities per survey and origin (annual; trip weights WTTRDFIN are annualised, person weights
WTPERFIN count persons aged 5+):
  driver VMT            sum of VMT_MILE over trips with DRVR_FLG=01
  commute driver VMT    the same for WHYTRP90=01 (to or from work)
  peak driver VMT       weekday trips (TDWKND=02) starting 6:00-9:59 or 15:00-18:59, the Urban
                        Mobility Report's peak periods
  vehicle-occupant hours  sum of TRVLCMIN/60 over trips in a privately owned vehicle
The ratios used downstream:
  rho = (all-purpose / commute driver VMT, Hispanic) / (the same, non-Hispanic): converts the
        group's ACS commuting share into an all-purpose traffic share
  r_all = Hispanic / non-Hispanic driver VMT per person aged 5+
  peak shares of driver VMT by origin
  occupancy ratio = (POV person-miles / driver VMT, Hispanic) / (the same, non-Hispanic)
  vehicle-occupant hours per person aged 5+ by urban-area size (URBANSIZE)

Outputs: derived/nhts_ratios.csv, derived/nhts_hours_by_urbansize.csv
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/nhts.py
"""
from __future__ import annotations

import pathlib
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
SOUTHWEST = {"CA", "TX", "AZ", "NM"}
URBANSIZE = {1: "50k-199k", 2: "200k-499k", 3: "500k-999k", 4: "1m+ with heavy rail",
             5: "1m+ without heavy rail", 6: "not in an urbanized area"}

SURVEYS = {
    2022: {"zip": "nhts2022_csv.zip", "trips": "tripv2pub.csv", "persons": "perv2pub.csv",
           # TRIPMODE 01/02: privately owned vehicle, driver or passenger
           "pov": lambda t: t["TRIPMODE"].isin([1, 2]), "state": None},
    2017: {"zip": "nhts2017_csv.zip", "trips": "trippub.csv", "persons": "perpub.csv",
           # TRPTRANS: car, SUV, van, pickup, motorcycle, RV, rental car
           "pov": lambda t: t["TRPTRANS"].isin([3, 4, 5, 6, 8, 9, 18]), "state": "HHSTATE"},
}


def read(year, member, cols):
    spec = SURVEYS[year]
    with zipfile.ZipFile(CACHE / spec["zip"]) as z, z.open(member) as fh:
        header = pd.read_csv(fh, nrows=0).columns
    use = [c for c in cols if c in header]
    with zipfile.ZipFile(CACHE / spec["zip"]) as z, z.open(member) as fh:
        return pd.concat(pd.read_csv(fh, usecols=use, chunksize=500_000,
                                     dtype={"HOUSEID": str, "PERSONID": str, "HHSTATE": str}))


def summarise(year):
    spec = SURVEYS[year]
    state = [spec["state"]] if spec["state"] else []
    trips = read(year, spec["trips"], ["HOUSEID", "PERSONID", "WTTRDFIN", "VMT_MILE", "DRVR_FLG", "TRPMILES",
                                       "TRIPMODE", "TRPTRANS", "TRVLCMIN", "WHYTRP90", "STRTTIME",
                                       "TDWKND", "R_HISP", "URBANSIZE"] + state)
    persons = read(year, spec["persons"], ["HOUSEID", "PERSONID", "WTPERFIN", "R_HISP",
                                           "URBANSIZE"] + state)
    if "R_HISP" not in trips:  # the 2017 trip file carries only the household flag
        trips = trips.merge(persons[["HOUSEID", "PERSONID", "R_HISP"]], on=["HOUSEID", "PERSONID"],
                            how="left", validate="many_to_one")
        if trips["R_HISP"].isna().any():
            raise ValueError("trips without a person record")
    w = trips["WTTRDFIN"].to_numpy(float)
    vmt = trips["VMT_MILE"].where(trips["VMT_MILE"].ge(0), 0).to_numpy(float)
    driver = trips["DRVR_FLG"].eq(1).to_numpy()
    minutes = trips["TRVLCMIN"].where(trips["TRVLCMIN"].ge(0), 0).to_numpy(float)
    miles = trips["TRPMILES"].where(trips["TRPMILES"].ge(0), 0).to_numpy(float)
    pov = spec["pov"](trips).to_numpy()
    commute = trips["WHYTRP90"].eq(1).to_numpy()
    start = pd.to_numeric(trips["STRTTIME"], errors="coerce")
    peak = (trips["TDWKND"].eq(2) & (start.between(600, 959) | start.between(1500, 1859))).to_numpy()
    trips_items = pd.DataFrame({
        "driver_vmt": w * vmt * driver,
        "commute_driver_vmt": w * vmt * driver * commute,
        "peak_driver_vmt": w * vmt * driver * peak,
        "pov_hours": w * minutes / 60 * pov,
        "commute_pov_hours": w * minutes / 60 * pov * commute,
        "peak_pov_hours": w * minutes / 60 * pov * peak,
        "driver_trips": w * driver,
        "pov_person_miles": w * miles * pov,
    })
    cuts = {"hispanic": trips["R_HISP"].eq(1).to_numpy(), "non_hispanic": trips["R_HISP"].eq(2).to_numpy()}
    pcuts = {"hispanic": persons["R_HISP"].eq(1).to_numpy(), "non_hispanic": persons["R_HISP"].eq(2).to_numpy()}
    if spec["state"]:
        sw_t = trips[spec["state"]].isin(SOUTHWEST).to_numpy()
        sw_p = persons[spec["state"]].isin(SOUTHWEST).to_numpy()
        cuts.update({"hispanic_southwest": cuts["hispanic"] & sw_t,
                     "non_hispanic_southwest": cuts["non_hispanic"] & sw_t})
        pcuts.update({"hispanic_southwest": pcuts["hispanic"] & sw_p,
                      "non_hispanic_southwest": pcuts["non_hispanic"] & sw_p})
    rows = []
    for cut, mask in cuts.items():
        tot = trips_items[mask].sum()
        pop = persons.loc[pcuts[cut], "WTPERFIN"].sum()
        row = {"survey": year, "cut": cut, "persons_5plus": pop,
               "sample_persons": int(pcuts[cut].sum()), "sample_trips": int(mask.sum())}
        row.update({f"{k}_per_person": v / pop for k, v in tot.items()})
        row["commute_share_of_driver_vmt"] = tot["commute_driver_vmt"] / tot["driver_vmt"]
        row["peak_share_of_driver_vmt"] = tot["peak_driver_vmt"] / tot["driver_vmt"]
        row["all_over_commute_driver_vmt"] = tot["driver_vmt"] / tot["commute_driver_vmt"]
        row["pov_hours_total"] = tot["pov_hours"]
        # Occupants per vehicle-mile: POV person-miles over driver VMT.
        row["occupancy_pmt_per_driver_vmt"] = tot["pov_person_miles"] / tot["driver_vmt"]
        row["pov_hours_per_driver_vmt"] = tot["pov_hours"] / tot["driver_vmt"]
        rows.append(row)
    out = pd.DataFrame(rows)
    hours = []
    for size, label in URBANSIZE.items():
        for cut in ("hispanic", "non_hispanic"):
            m_t = cuts[cut] & trips["URBANSIZE"].eq(size).to_numpy()
            m_p = pcuts[cut] & persons["URBANSIZE"].eq(size).to_numpy()
            pop = persons.loc[m_p, "WTPERFIN"].sum()
            hours.append({"survey": year, "urbansize": size, "label": label, "cut": cut,
                          "persons_5plus": pop, "sample_persons": int(m_p.sum()),
                          "pov_hours_per_person": trips_items.loc[m_t, "pov_hours"].sum() / pop,
                          "driver_vmt_per_person": trips_items.loc[m_t, "driver_vmt"].sum() / pop})
    return out, pd.DataFrame(hours)


def ratios(out):
    rows = []
    for (year, suffix) in ((2022, ""), (2017, ""), (2017, "_southwest")):
        d = out[out.survey == year].set_index("cut")
        h, n = d.loc["hispanic" + suffix], d.loc["non_hispanic" + suffix]
        rows.append({
            "survey": year, "cut": "national" if not suffix else "southwest",
            "rho_all_over_commute_H_vs_N": h.all_over_commute_driver_vmt / n.all_over_commute_driver_vmt,
            "r_all_driver_vmt_per_person_H_vs_N": h.driver_vmt_per_person / n.driver_vmt_per_person,
            "r_commute_driver_vmt_per_person_H_vs_N": h.commute_driver_vmt_per_person / n.commute_driver_vmt_per_person,
            "r_pov_hours_per_person_H_vs_N": h.pov_hours_per_person / n.pov_hours_per_person,
            "peak_share_H": h.peak_share_of_driver_vmt, "peak_share_N": n.peak_share_of_driver_vmt,
            "commute_share_H": h.commute_share_of_driver_vmt, "commute_share_N": n.commute_share_of_driver_vmt,
            "occupancy_ratio_H_vs_N": h.occupancy_pmt_per_driver_vmt / n.occupancy_pmt_per_driver_vmt,
            "sample_persons_H": h.sample_persons, "sample_persons_N": n.sample_persons,
        })
    return pd.DataFrame(rows)


def main():
    DERIVED.mkdir(exist_ok=True)
    outs, hours = zip(*(summarise(y) for y in SURVEYS))
    out = pd.concat(outs, ignore_index=True)
    rat = ratios(out)
    out.to_csv(DERIVED / "nhts_by_origin.csv", index=False)
    rat.to_csv(DERIVED / "nhts_ratios.csv", index=False)
    pd.concat(hours, ignore_index=True).to_csv(DERIVED / "nhts_hours_by_urbansize.csv", index=False)
    pd.set_option("display.width", 220)
    pd.set_option("display.max_columns", 30)
    print(out.round(3).to_string(index=False))
    print(rat.round(4).to_string(index=False))
    print(pd.concat(hours).round(2).to_string(index=False))


if __name__ == "__main__":
    main()
