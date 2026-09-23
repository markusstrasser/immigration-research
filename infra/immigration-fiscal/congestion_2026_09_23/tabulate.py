"""ACS 2024 one-year PUMS: how the Mexican-origin group and everyone else get to work.

Reads only the needed columns of the zipped national person files in chunks.

Group person: Hispanic origin Mexican (HISP=02) or born in Mexico (POBP=303), the housing lane's
rule (../housing_transfer_2026_09_23/RESULT.md section 1). Workers are persons with a means of
transportation to work (JWTRNS). A car commuter (JWTRNS=01) with vehicle occupancy JWRIP=k counts
1/k of a vehicle, so the sum over carpool members is one vehicle; motorcycle and taxi or
ride-hailing commuters count one vehicle each. Vehicle-minutes are vehicles times one-way travel
time (JWMNP). Peak departures are 6:00-9:59 a.m. (JWDP codes 031-078), the Urban Mobility
Report's morning peak period; 7:00-8:59 a.m. (codes 043-066) is the narrow variant. Standard
errors use the 80 successive-difference replicate weights.

Outputs (derived/):
  pums_commute_national.csv  group x item: workers by means, vehicles, minutes, peak shares (with SE)
  pums_gate_b08301.csv       PUMS totals against published ACS 2024 tables B08301 and B08133
  pums_puma_commute.csv      PUMA x group cells, input to arms.py
  pums_commute_checks.json   person counts and the gate verdict
Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/congestion_2026_09_23/tabulate.py
"""
from __future__ import annotations

import io
import json
import pathlib
import zipfile

import numpy as np
import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[2]
PUMS = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
CACHE = HERE / "_cache"
DERIVED = HERE / "derived"
PREPS = [f"PWGTP{i}" for i in range(1, 81)]
CHUNK = 150_000
MEXICO = 303
MEANS = {1: "car_truck_van", 2: "bus", 3: "subway", 4: "commuter_rail", 5: "light_rail",
         6: "ferry", 7: "taxi_ridehail", 8: "motorcycle", 9: "bicycle", 10: "walked",
         11: "worked_from_home", 12: "other"}
PEAK = (31, 78)        # 6:00-9:59 a.m.
NARROW = (43, 66)      # 7:00-8:59 a.m.
GATE_TOLERANCE = 0.03  # "within a few percent"


def read_zip(usecols):
    with zipfile.ZipFile(PUMS / "csv_pus.zip") as z:
        for member in ("psam_pusa.csv", "psam_pusb.csv"):
            with z.open(member) as fh:
                yield from pd.read_csv(io.TextIOWrapper(fh), usecols=usecols, chunksize=CHUNK,
                                       dtype={"STATE": str, "PUMA": str})


def replicate_se(full, reps):
    return np.sqrt(4 / 80 * ((reps - full[..., None]) ** 2).sum(axis=-1))


def person_items(chunk):
    """Per-person quantities; every column is additive over persons."""
    means = chunk["JWTRNS"]
    rip = chunk["JWRIP"]
    minutes = chunk["JWMNP"].fillna(0).to_numpy(float)
    dep = chunk["JWDP"]
    car = means.eq(1).to_numpy()
    vehicle = np.where(car, 1 / rip.where(rip.ge(1), 1).to_numpy(float), 0.0)
    vehicle = vehicle + means.isin([7, 8]).to_numpy()
    peak = dep.between(*PEAK).to_numpy()
    narrow = dep.between(*NARROW).to_numpy()
    early = dep.lt(PEAK[0]).to_numpy()
    worker = means.notna().to_numpy()
    commuter = (worker & means.ne(11).to_numpy())
    transit = means.between(2, 6).to_numpy()
    income = chunk["PINCP"].fillna(0).to_numpy(float) * chunk["ADJINC"].to_numpy(float) / 1e6
    items = {
        "persons": np.ones(len(chunk)),
        "workers": worker.astype(float),
        "commuters": commuter.astype(float),
        "car_commuters": car.astype(float),
        "drove_alone": (car & rip.eq(1).to_numpy()).astype(float),
        "carpooled": (car & rip.ge(2).to_numpy()).astype(float),
        "transit_commuters": transit.astype(float),
        "vehicles": vehicle,
        "vehicle_minutes": vehicle * minutes,
        "car_person_minutes": car * minutes,
        "commuter_minutes": commuter * minutes,
        "transit_minutes": transit * minutes,
        "vehicles_peak": vehicle * peak,
        "vehicle_minutes_peak": vehicle * minutes * peak,
        "vehicles_narrow_peak": vehicle * narrow,
        "vehicles_before_6am": vehicle * early,
        "personal_income": income,
    }
    for code, name in MEANS.items():
        items[f"means_{name}"] = means.eq(code).to_numpy().astype(float)
    for k in range(2, 8):
        label = f"carpool_{k}" if k < 7 else "carpool_7plus"
        hit = rip.ge(7) if k == 7 else rip.eq(k)
        items[label] = (car & hit.to_numpy()).astype(float)
    items["carpool_5_6"] = items.pop("carpool_5") + items.pop("carpool_6")
    return pd.DataFrame(items)


def main():
    DERIVED.mkdir(exist_ok=True)
    cols = ["STATE", "PUMA", "PWGTP", "HISP", "POBP", "JWTRNS", "JWMNP", "JWDP", "JWRIP",
            "PINCP", "ADJINC"] + PREPS
    national = {}
    pumas = []
    names = None
    for chunk in read_zip(cols):
        grp = (chunk["HISP"].eq(2) | chunk["POBP"].eq(MEXICO)).to_numpy()
        items = person_items(chunk)
        names = names or list(items.columns)
        weights = chunk[["PWGTP"] + PREPS].to_numpy(float)
        for label, mask in (("group", grp), ("other", ~grp)):
            tot = items[mask].to_numpy().T @ weights[mask]          # item x 81
            national[label] = national.get(label, 0) + tot
            cell = items[mask].mul(chunk["PWGTP"].to_numpy(float)[mask], axis=0)
            cell["STATE"], cell["PUMA"] = chunk["STATE"].to_numpy()[mask], chunk["PUMA"].to_numpy()[mask]
            cell["group"] = label
            pumas.append(cell.groupby(["STATE", "PUMA", "group"]).sum())
    national["all"] = national["group"] + national["other"]
    rows = []
    for label, tot in national.items():
        se = replicate_se(tot[:, 0], tot[:, 1:])
        for i, item in enumerate(names):
            rows.append({"group": label, "item": item, "estimate": tot[i, 0], "se": se[i]})
        # Ratios with replicate SEs.
        idx = {n: i for i, n in enumerate(names)}
        ratios = {
            "mean_one_way_minutes_commuters": ("commuter_minutes", "commuters"),
            "mean_one_way_minutes_car": ("car_person_minutes", "car_commuters"),
            "vehicles_per_car_commuter": ("vehicles", "car_commuters"),
            "peak_share_of_vehicles": ("vehicles_peak", "vehicles"),
            "peak_share_of_vehicle_minutes": ("vehicle_minutes_peak", "vehicle_minutes"),
            "narrow_peak_share_of_vehicles": ("vehicles_narrow_peak", "vehicles"),
            "before_6am_share_of_vehicles": ("vehicles_before_6am", "vehicles"),
            "car_share_of_commuters": ("car_commuters", "commuters"),
            "wfh_share_of_workers": ("means_worked_from_home", "workers"),
            "commuters_per_person": ("commuters", "persons"),
            "vehicle_minutes_per_person": ("vehicle_minutes", "persons"),
        }
        for name, (num, den) in ratios.items():
            r = tot[idx[num]] / tot[idx[den]]
            rows.append({"group": label, "item": name, "estimate": r[0],
                         "se": float(replicate_se(np.array(r[0]), r[1:]))})
    table = pd.DataFrame(rows)
    # Group shares with replicate SEs.
    share_rows = []
    for i, item in enumerate(names):
        r = national["group"][i] / national["all"][i]
        share_rows.append({"group": "group_share", "item": item, "estimate": r[0],
                           "se": float(replicate_se(np.array(r[0]), r[1:]))})
    table = pd.concat([table, pd.DataFrame(share_rows)], ignore_index=True)
    table.to_csv(DERIVED / "pums_commute_national.csv", index=False)

    puma = pd.concat(pumas).groupby(level=[0, 1, 2]).sum().reset_index()
    puma.to_csv(DERIVED / "pums_puma_commute.csv", index=False)

    # Gate against the published national tables.
    pub = json.loads((CACHE / "acs2024_b08301_us.json").read_text())
    pub = dict(zip(pub[0], pub[1]))
    agg = json.loads((CACHE / "acs2024_b08133_us.json").read_text())
    agg = dict(zip(agg[0], agg[1]))
    est = table[table.group == "all"].set_index("item")["estimate"]
    gate = [
        ("workers 16+ (total)", "B08301_001E", est["workers"]),
        ("car, truck or van", "B08301_002E", est["means_car_truck_van"]),
        ("drove alone", "B08301_003E", est["drove_alone"]),
        ("carpooled", "B08301_004E", est["carpooled"]),
        ("2-person carpool", "B08301_005E", est["carpool_2"]),
        ("3-person carpool", "B08301_006E", est["carpool_3"]),
        ("4-person carpool", "B08301_007E", est["carpool_4"]),
        ("5-6-person carpool", "B08301_008E", est["carpool_5_6"]),
        ("7+-person carpool", "B08301_009E", est["carpool_7plus"]),
        ("public transportation", "B08301_010E", est[["means_bus", "means_subway", "means_commuter_rail",
                                                      "means_light_rail", "means_ferry"]].sum()),
        ("bus", "B08301_011E", est["means_bus"]),
        ("subway or elevated rail", "B08301_012E", est["means_subway"]),
        ("taxi or ride-hailing", "B08301_016E", est["means_taxi_ridehail"]),
        ("motorcycle", "B08301_017E", est["means_motorcycle"]),
        ("bicycle", "B08301_018E", est["means_bicycle"]),
        ("walked", "B08301_019E", est["means_walked"]),
        ("other means", "B08301_020E", est["means_other"]),
        ("worked from home", "B08301_021E", est["means_worked_from_home"]),
    ]
    rows = [{"item": n, "table_cell": c, "pums": p, "published": float(pub[c]),
             "moe90": float(pub[c.replace("E", "M")]), "difference": p / float(pub[c]) - 1}
            for n, c, p in gate]
    rows.append({"item": "aggregate one-way travel time, minutes", "table_cell": "B08133_001E",
                 "pums": est["commuter_minutes"], "published": float(agg["B08133_001E"]),
                 "moe90": float(agg["B08133_001M"]),
                 "difference": est["commuter_minutes"] / float(agg["B08133_001E"]) - 1})
    gate = pd.DataFrame(rows)
    gate.to_csv(DERIVED / "pums_gate_b08301.csv", index=False)
    major = gate[gate.item.isin(["workers 16+ (total)", "car, truck or van", "drove alone",
                                 "carpooled", "public transportation", "walked",
                                 "worked from home",
                                 "aggregate one-way travel time, minutes"])]
    checks = {
        "group_persons_acs": float(table[(table.group == "group") & (table.item == "persons")].estimate.iloc[0]),
        "all_persons_acs": float(est["persons"]),
        "gate_tolerance": GATE_TOLERANCE,
        "gate_max_abs_difference_major_rows": float(major["difference"].abs().max()),
        "gate_passed": bool(major["difference"].abs().max() <= GATE_TOLERANCE),
    }
    (DERIVED / "pums_commute_checks.json").write_text(json.dumps(checks, indent=2))
    pd.set_option("display.width", 200)
    print(gate.round(4).to_string(index=False))
    print(json.dumps(checks, indent=1))
    if not checks["gate_passed"]:
        raise SystemExit("[GATE FAILED] PUMS commuter totals differ from B08301 by more than 3%")


if __name__ == "__main__":
    main()
