"""Inputs for pricing the v4 case's state-price and road items for any group (rekey_sept29.py).

The v4 case (main_case_2026_09_29) prices three S&L spending lines and two receipt lines where the Mexican-origin union
lives (state_priced_services_2026_09_29) and keys road costs, gasoline taxes and licences by the union's share of
driver miles (roads_mileage_key_2026_09_29). To apply the same rules to another group, the re-key needs the per-state
relatives behind the state indexes and driver miles per person by race, ethnicity and age:

  derived/v4_state_relatives.csv  per state: the FY2024 direct per-resident spending relative of each function in the
      case's central package (state_per_capita.csv), the per-prisoner corrections relative and the imprisonment rate
      (prison_cost_by_state.csv; state_price.populations), and the S&L general sales tax per dollar of PCE and the
      motor-vehicle licence tax per resident relative to the US (Census FY2024 T09 and T24, BEA SAPCE PCE, the
      lane's state_price.read_finance / pce / populations, imported read-only).
  derived/v4_nhts_vmt.csv  NHTS 2017 annual driver VMT per person aged 5+ by group (NH white, NH Black, Hispanic, the
      rest, all) and five-year age band (80+), the congestion lane's definitions (trip weights WTTRDFIN x VMT_MILE on
      driver trips, DRVR_FLG 1; persons WTPERFIN).

Gates (exit 1, nothing written): the union's indexes recomputed from the state lane's group_share reproduce its
corrections.csv (every central function, corrections per inmate at group x imprisonment weights) and its two receipt
indexes (sales at group weights, licences at adult weights) to 1e-8; the Hispanic / non-Hispanic driver VMT per person
aged 5+ reproduces the congestion lane's 2017 national r_all (0.8930224334) to 1e-9.
Run from the repository root (about 1 min):
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/white_replacement_2026_09_28/v4_inputs.py
"""
from __future__ import annotations

import csv
import importlib.util
import sys
import zipfile
from pathlib import Path

sys.dont_write_bytecode = True   # read-only imports from other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

LANE = Path(__file__).resolve().parent
FISCAL = LANE.parent
DER = LANE / "derived"
SP = FISCAL / "state_priced_services_2026_09_29"
NHTS = FISCAL / "congestion_2026_09_23/_cache/nhts2017_csv.zip"
R_ALL_2017 = float(pd.read_csv(FISCAL / "congestion_2026_09_23/derived/nhts_ratios.csv").query(
    "survey == 2017 and cut == 'national'").r_all_driver_vmt_per_person_H_vs_N.iloc[0])
CENTRAL = {"public_order_safety": ["police", "judicial", "fire", "corrections_per_inmate", "protective_inspection"],
           "health_services": ["health"], "recreation_culture": ["parks_libraries"]}
PER_RESIDENT = ["police", "judicial", "fire", "protective_inspection", "health", "parks_libraries"]
BANDS = list(range(5, 80, 5)) + [80]
FAILS: list[str] = []


def gate(label, ok, detail=""):
    print(f"  {'PASS' if ok else 'FAIL'} {label}{' — ' + detail if detail else ''}", flush=True)
    if not ok:
        FAILS.append(label)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def state_relatives():
    sp = load("state_price", SP / "state_price.py")
    pc = pd.read_csv(SP / "derived/state_per_capita.csv")
    rel = pc[(pc.year == 2024) & (pc.basis == "direct")].pivot(index="fips", columns="function", values="relative")
    out = rel[PER_RESIDENT].copy()
    pris = pd.read_csv(SP / "derived/prison_cost_by_state.csv").set_index("fips")
    pop = sp.populations(2024)
    out["corrections_per_inmate"] = pris.relative.reindex(out.index)
    out["imprisonment_rate"] = (pris.prisoners / pop.reindex(pris.index)).reindex(out.index)
    fin = sp.read_finance(2024).reindex(sorted(sp.STATES))
    bases = {"pce": sp.pce(2024), "population": pop}
    for name, line in (("sales", "general_sales_tax"), ("licences", "personal_motor_vehicle")):
        spec = sp.RECEIPTS[line]
        tax = sum(fin.get(c, 0) for c in spec["codes"]) * 1e3
        base = bases[spec["base"]]
        out[f"{name}_relative"] = (tax / base / (tax.sum() / base.sum())).reindex(out.index)
    out.insert(0, "state", [sp.STATES[f] for f in out.index])
    return out


def index_of(rel, w_pop, w_adults):
    """A group's state indexes from its population and adult shares by state (Series on fips)."""
    ix = {f: float((rel[f] * w_pop.reindex(rel.index).fillna(0)).sum() / w_pop.sum()) for f in PER_RESIDENT}
    has = rel.corrections_per_inmate.notna()
    wr = w_pop.reindex(rel.index).fillna(0)[has] * rel.imprisonment_rate[has]
    ix["corrections_per_inmate"] = float((rel.corrections_per_inmate[has] * wr).sum() / wr.sum())
    ix["sales"] = float((rel.sales_relative * w_pop.reindex(rel.index).fillna(0)).sum() / w_pop.sum())
    ix["licences"] = float((rel.licences_relative * w_adults.reindex(rel.index).fillna(0)).sum() / w_adults.sum())
    return ix


def nhts_vmt():
    with zipfile.ZipFile(NHTS) as z:
        persons = pd.read_csv(z.open("perpub.csv"), usecols=["HOUSEID", "PERSONID", "WTPERFIN", "R_AGE", "R_HISP", "R_RACE"],
                              dtype={"HOUSEID": str, "PERSONID": str})
        parts = []
        for ch in pd.read_csv(z.open("trippub.csv"), usecols=["HOUSEID", "PERSONID", "WTTRDFIN", "VMT_MILE", "DRVR_FLG"],
                              dtype={"HOUSEID": str, "PERSONID": str}, chunksize=500_000):
            v = ch.VMT_MILE.where(ch.VMT_MILE.ge(0), 0).to_numpy(float) * ch.DRVR_FLG.eq(1).to_numpy()
            parts.append(pd.DataFrame({"HOUSEID": ch.HOUSEID, "PERSONID": ch.PERSONID,
                                       "vmt": ch.WTTRDFIN.to_numpy(float) * v}).groupby(["HOUSEID", "PERSONID"]).vmt.sum())
    vmt = pd.concat(parts).groupby(level=[0, 1]).sum()
    p = persons.set_index(["HOUSEID", "PERSONID"])
    if not vmt.index.isin(p.index).all():
        raise SystemExit("[BLOCKED] NHTS trips without a person record")
    p["vmt"] = vmt.reindex(p.index).fillna(0.0).to_numpy()
    p = p.reset_index()
    groups = {"nh_white": p.R_HISP.eq(2) & p.R_RACE.eq(1), "nh_black": p.R_HISP.eq(2) & p.R_RACE.eq(2),
              "hispanic": p.R_HISP.eq(1), "non_hispanic": p.R_HISP.eq(2),
              "rest": ~((p.R_HISP.eq(2) & p.R_RACE.isin([1, 2])) | p.R_HISP.eq(1)), "all": pd.Series(True, index=p.index)}
    per = {g: float(p.vmt[m].sum() / p.WTPERFIN[m].sum()) for g, m in groups.items()}
    gate("NHTS 2017: Hispanic / non-Hispanic driver VMT per person aged 5+ reproduces the congestion lane's r_all",
         abs(per["hispanic"] / per["non_hispanic"] - R_ALL_2017) < 1e-9, f"{per['hispanic'] / per['non_hispanic']:.10f} vs {R_ALL_2017:.10f}")
    aged = p[p.R_AGE.ge(5)].copy()
    aged["band"] = np.minimum(aged.R_AGE // 5 * 5, 80).astype(int)
    rows = []
    for g, m in groups.items():
        sub = aged[m.loc[aged.index]]
        by = sub.groupby("band").agg(persons=("WTPERFIN", "sum"), vmt=("vmt", "sum"), sample=("WTPERFIN", "size"))
        by = by.reindex(BANDS)
        if by.persons.isna().any():
            raise SystemExit(f"[BLOCKED] NHTS {g}: an age band has no persons")
        for b, r in by.iterrows():
            rows.append({"group": g, "band": b, "persons_5plus": r.persons, "driver_vmt_bn": r.vmt / 1e9,
                         "vmt_per_person": r.vmt / r.persons, "sample_persons": int(r["sample"])})
        rows.append({"group": g, "band": "all", "persons_5plus": float(p.WTPERFIN[m].sum()),
                     "driver_vmt_bn": float(p.vmt[m].sum() / 1e9), "vmt_per_person": per[g], "sample_persons": int(m.sum())})
    missing = int(p.R_AGE.lt(5).sum())
    print(f"  NHTS 2017 persons with no age of 5+ on record (in the all-ages rows only): {missing}")
    return pd.DataFrame(rows)


def main():
    print("[state relatives]", flush=True)
    rel = state_relatives()
    gp = pd.read_csv(SP / "derived/group_population_by_state.csv").set_index("fips")
    ix = index_of(rel, gp.group_share, gp.group_adult_share)
    corr = pd.read_csv(SP / "derived/corrections.csv").set_index("function")
    for fs in CENTRAL.values():
        for f in fs:
            want = float(corr.loc[f, "index"])
            gate(f"the union's {f} index reproduces corrections.csv", abs(ix[f] - want) < 1e-8, f"{ix[f]:.10f} vs {want:.10f}")
    rc = pd.read_csv(SP / "derived/receipts_corrections.csv").set_index("line")
    for name, line in (("sales", "general_sales_tax"), ("licences", "personal_motor_vehicle")):
        want = float(rc.loc[line, "index"])
        gate(f"the union's {line} index reproduces receipts_corrections.csv", abs(ix[name] - want) < 1e-8,
             f"{ix[name]:.10f} vs {want:.10f}")
    print("[NHTS 2017 driver miles]", flush=True)
    vmt = nhts_vmt()
    if FAILS:
        print(f"FAIL: {len(FAILS)} gate(s): {FAILS}")
        sys.exit(1)
    rel.index.name = "fips"
    rel.to_csv(DER / "v4_state_relatives.csv", lineterminator="\n", float_format="%.10g")
    with open(DER / "v4_nhts_vmt.csv", "w", newline="") as f:
        wr = csv.DictWriter(f, fieldnames=list(vmt.columns), lineterminator="\n")
        wr.writeheader()
        for r in vmt.to_dict("records"):
            wr.writerow({k: (f"{v:.10g}" if isinstance(v, float) else v) for k, v in r.items()})
    allrow = vmt[(vmt.band == "all")].set_index("group").vmt_per_person
    print("  driver VMT per person 5+ relative to all:", {g: round(v / allrow["all"], 4) for g, v in allrow.items()})
    print(f"  wrote derived/v4_state_relatives.csv ({len(rel)} states), derived/v4_nhts_vmt.csv ({len(vmt)} rows)")


if __name__ == "__main__":
    main()
