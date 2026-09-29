"""Age profiles of the keys the September 29 main case (v4, `main_case_2026_09_29`) charges and the September 27 case
did not: the three property-tax receipts its item 5 makes respond. `profiles.py` wrote every other key; this script
writes only the new ones, beside its output, and imports its helpers (`profiles.py` itself is not run).

  receipt|modeled_owner_property  the account's own key (`generation_account_2026_09_24/keys.py` `owner_property`: the
                                  state effective rate x the CPS home value of owner units, shared over the SPM unit), on
                                  the CPS frame under both weight sets, as `profiles.py` bins every other CPS key.
  receipt|renter_contract_rent    tenant-occupied property tax (item 5's split line), keyed by contract rent; and
  receipt|household_vehicles      personal property tax, re-keyed by item 5 to household vehicles. The CPS carries
                                  neither rent nor vehicles, so both come from the ACS 2024 person file, as the
                                  receipt-side lane (`receipt_side_long_run_2026_09_28/housing.py`) builds its shares:
                                  household amounts shared per member, the group proxy HISP=02 or POBP=303. The ACS gives
                                  per-person amounts in each age bin for the group and for all persons; a bin's union and
                                  national totals here are those per-person amounts times the CPS frame's union and
                                  national headcounts in the bin (indirect standardization on the frame's ages).

Gates (exit 1): the owner key's union and national totals under the published weights reproduce model.json's
modeled_owner_property cell (1e-6bn); the ACS person route reproduces the receipt-side lane's rent and vehicle shares
(`derived/housing.json`, its six printed decimals); the ACS files are the lane's pinned bytes; bins add to totals.
Outputs: derived/age_bins_sept29.csv (the columns of age_bins.csv), derived/acs_rates_sept29.csv. Run from the
repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/main_case_decomposition_2026_09_29/profiles_sept29.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import csv  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import zipfile  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import profiles as PR  # noqa: E402  (its helpers and the generation lane's modules; main() is not run)

F, K, L = PR.F, PR.K, PR.L
FISCAL = PR.FISCAL
ROOT = FISCAL.parents[1]
OUT = HERE / "derived"
ALLOC = PR.ALLOC
EDGES = PR.EDGES
gate = PR.gate
EXT = ROOT / "sources/immigration-fiscal/data/external/acs_pums_2024_1yr"
ACS = {  # the receipt-side lane's pins (housing.py LOCAL)
    "hus": (EXT / "csv_hus.zip", "8281008e53de98f0ef81e7a2ee5a8725991dda1ecfd2713ead73246425e515d0"),
    "pus": (EXT / "csv_pus.zip", "afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894"),
}
HOUSING = FISCAL / "receipt_side_long_run_2026_09_28/derived/housing.json"
MODEL = FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
STATES = {f"{s:02d}" for s in range(1, 57)} - {"03", "07", "14", "43", "52"}  # the 50 states and DC (housing.py STATES)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_zip_csvs(zpath: Path, members: list[str], usecols: list[str], dtype: dict) -> pd.DataFrame:
    with zipfile.ZipFile(zpath) as z:
        return pd.concat([pd.read_csv(z.open(m), usecols=usecols, dtype=dtype) for m in members], ignore_index=True)


def acs_rates():
    """Per-person contract rent and household vehicles by age bin, for the group proxy and for all persons: the
    receipt-side lane's person route (housing.py acs_person_amounts), with AGEP."""
    for name, (path, want) in ACS.items():
        gate(f"ACS {name} file is the receipt-side lane's pinned bytes", sha256(path) == want, path.name)
    hus = read_zip_csvs(ACS["hus"][0], ["psam_husa.csv", "psam_husb.csv"], ["SERIALNO", "NP", "TEN", "RNTP", "ADJHSG", "VEH"],
                        {"SERIALNO": str, "TEN": "Int64", "VEH": "Int64"})
    pus = read_zip_csvs(ACS["pus"][0], ["psam_pusa.csv", "psam_pusb.csv"], ["SERIALNO", "STATE", "PWGTP", "HISP", "POBP", "AGEP"],
                        {"SERIALNO": str, "STATE": str, "HISP": int, "POBP": int, "AGEP": int})
    pus = pus[pus.STATE.str.zfill(2).isin(STATES)]
    if hus.SERIALNO.duplicated().any():
        raise SystemExit("[BLOCKED] duplicate ACS housing SERIALNO")
    p = pus.merge(hus, on="SERIALNO", how="left", validate="many_to_one")
    adj = p["ADJHSG"] / 1e6
    np_ = p["NP"].where(p["NP"] > 0)
    rent = p["TEN"].eq(3) & p["RNTP"].notna()
    w = p["PWGTP"].astype(float)
    group = (p["HISP"].eq(2) | p["POBP"].eq(303)).to_numpy()
    amounts = {
        "renter_contract_rent": np.where(rent, 12 * p["RNTP"] * adj / np_, 0.0),
        "household_vehicles": np.where(p["VEH"].notna() & np_.notna(), p["VEH"].fillna(0) / np_, 0.0),
    }
    b = PR.bins_of(p["AGEP"].to_numpy())
    nb = len(EDGES)
    wv = w.to_numpy()
    pop = {"group": np.bincount(b, weights=np.where(group, wv, 0.0), minlength=nb), "all": np.bincount(b, weights=wv, minlength=nb)}
    rates, shares = {}, {}
    for key, x in amounts.items():
        x = np.asarray(x, float)
        if np.isnan(x).any():
            raise SystemExit(f"[BLOCKED] missing ACS amounts for {key} after the household merge")
        tot = {"group": np.bincount(b, weights=np.where(group, x * wv, 0.0), minlength=nb), "all": np.bincount(b, weights=x * wv, minlength=nb)}
        if (pop["group"] <= 0).any():
            gate(f"ACS {key}: every age bin holds group persons", False)
        rates[key] = {s: tot[s] / pop[s] for s in tot}
        shares[key] = float(tot["group"].sum() / tot["all"].sum())
    return rates, shares, pop


def main():
    print("[frame]", flush=True)
    d = F.load()
    civ, union, _ = F.masks(d)
    W = d[F.REPS].to_numpy(float)
    print("[row 4 weights]", flush=True)
    arms, _ = L.weight_arms(d, W, L.acs_cells())
    weights = {"published": W[:, 0], "row4": arms["row4"][:, 0]}
    del arms, W
    n4 = float(weights["row4"][union].sum())
    gate("row-4 union count reproduces the CPS lane's 39.712M", abs(n4 / 1e6 - 39.712) < 0.001, f"{n4 / 1e6:.6f}M")
    b = PR.bins_of(d.A_AGE.to_numpy())
    nb = len(EDGES)

    print("[owner-occupied property key]", flush=True)
    owner, _ = K.owner_property(d)
    model = json.loads(MODEL.read_text())
    line = next(x for x in model["receipts"]["lines"] if x["id"] == "modeled_owner_property")
    ref = model["receipts"]["reference"]
    w = weights["published"]
    u_bn, n_bn = float(owner[union] @ w[union]) / 1e9, float(owner[civ] @ w[civ]) / 1e9
    for a in ALLOC:
        cell = line["cells"][ref][a]
        gate(f"owner key ({a}) reproduces model.json's cell {cell['target_bn']:.6f} of {line['national_bn']:.6f}bn",
             abs(u_bn - cell["target_bn"]) < 1e-6 and abs(n_bn - line["national_bn"]) < 1e-6, f"{u_bn:.9f} / {n_bn:.6f}")
    u4 = float(owner[union] @ weights["row4"][union]) / 1e9
    n4bn = float(owner[civ] @ weights["row4"][civ]) / 1e9
    print(f"  owner key on row 4: union {u4:.6f}bn of {n4bn:.6f}bn (published {u_bn:.6f} of {n_bn:.6f}); "
          f"share {u4 / n4bn:.9f} vs {u_bn / n_bn:.9f}", flush=True)

    print("[ACS rent and vehicles]", flush=True)
    rates, shares, acs_pop = acs_rates()
    H = json.loads(HOUSING.read_text())["keys"]
    for key, hk in [("renter_contract_rent", "rent_share"), ("household_vehicles", "vehicle_share")]:
        gate(f"ACS person route reproduces the receipt-side lane's {hk} {H[hk]}", round(shares[key], 6) == H[hk], f"{shares[key]:.9f}")

    print("[bins]", flush=True)
    rows = []
    for wname, wv in weights.items():
        wu, wc = np.where(union, wv, 0.0), np.where(civ, wv, 0.0)
        pu = np.bincount(b, weights=wu, minlength=nb)
        pc = np.bincount(b, weights=wc, minlength=nb)
        ub = np.bincount(b, weights=owner * wu, minlength=nb)
        cb = np.bincount(b, weights=owner * wc, minlength=nb)
        if abs(ub.sum() - float(owner[union] @ wv[union])) > 1e-6 * max(1.0, abs(ub.sum())):
            gate(f"{wname}/owner: bins add to the union total", False)
        vectors = {"receipt|modeled_owner_property": (ub, cb)}
        for key, r in rates.items():
            vectors[f"receipt|{key}"] = (pu * r["group"], pc * r["all"])
        for a in ALLOC:
            for name, (uu, cc) in vectors.items():
                for i in range(nb):
                    rows.append(dict(weights=wname, allocation=a, key=name, bin=EDGES[i], union=uu[i], national=cc[i]))
    OUT.mkdir(exist_ok=True)
    with (OUT / "age_bins_sept29.csv").open("w", newline="") as handle:
        out = csv.DictWriter(handle, fieldnames=["weights", "allocation", "key", "bin", "union", "national"], lineterminator="\n")
        out.writeheader()
        for r in rows:
            out.writerow({**r, "union": repr(float(r["union"])), "national": repr(float(r["national"]))})
    with (OUT / "acs_rates_sept29.csv").open("w", newline="") as handle:
        out = csv.writer(handle, lineterminator="\n")
        out.writerow(["bin", "acs_group_persons", "acs_all_persons", "rent_per_person_group", "rent_per_person_all",
                      "vehicles_per_person_group", "vehicles_per_person_all"])
        for i in range(nb):
            out.writerow([EDGES[i], repr(float(acs_pop["group"][i])), repr(float(acs_pop["all"][i])),
                          repr(float(rates["renter_contract_rent"]["group"][i])), repr(float(rates["renter_contract_rent"]["all"][i])),
                          repr(float(rates["household_vehicles"]["group"][i])), repr(float(rates["household_vehicles"]["all"][i]))])
    print(f"  wrote {len(rows)} bin rows; ACS shares rent {shares['renter_contract_rent']:.6f}, vehicles "
          f"{shares['household_vehicles']:.6f}", flush=True)
    if PR.FAILS:
        print(f"FAIL: {len(PR.FAILS)} gate(s): {PR.FAILS}")
        sys.exit(1)
    print("  all profile gates passed")


if __name__ == "__main__":
    main()
