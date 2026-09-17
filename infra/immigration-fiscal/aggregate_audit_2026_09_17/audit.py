"""Independent full-weight reconstruction; no policy or lifetime estimator."""
from pathlib import Path
import hashlib
import json
import sys

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
FISCAL = HERE.parent
sys.path.insert(0, str(FISCAL / "build"))
from analyze_cps_fiscal_2025 import prepare, CASH, NONCASH
from meps_health_transport_2024 import read_meps


def main():
    inputs = {
        "cps": FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
        "meps": ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip",
        "meps_dictionary": ROOT / "sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt",
        "extension": FISCAL / "gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv",
    }
    provenance = {}
    for name, path in inputs.items():
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        provenance[name] = {"path": str(path), "sha256": digest, "bytes": path.stat().st_size}
    d, _, _, validation = prepare(inputs["cps"])
    units = d.groupby("SPM_ID")
    sizes = units.SPM_ID.transform("size")
    if not np.array_equal(sizes.to_numpy(), d.SPM_NUMPER.to_numpy()):
        raise ValueError("SPM size does not match observed membership")
    component = {}
    for name, columns in [("tax", ["FICA", "FEDTAX_AC", "STATETAX_A"]),
                          ("cash", list(CASH.values())), ("social_security", ["SS_VAL"])]:
        total = units[columns].transform("sum").sum(axis=1)
        component[name] = total / sizes
        if not np.allclose(component[name].groupby(d.SPM_ID).sum(),
                           total.groupby(d.SPM_ID).first(), rtol=1e-10, atol=1e-6):
            raise ValueError(f"Allocation failed conservation: {name}")
    component["noncash"] = d[list(NONCASH.values())].sum(axis=1) / sizes
    meps, anchors = read_meps(inputs["meps"], inputs["meps_dictionary"])
    donor = meps[(meps.PERWT24F > 0) & (meps.AGE24X >= 0) & meps.BORNUSA.isin([1, 2])].copy()
    donor["band"] = np.digitize(donor.AGE24X, [18, 35, 50, 65])
    donor["weighted_cost"] = donor.PERWT24F * donor.public_paid
    cells = donor.groupby(["band", "BORNUSA"])[["weighted_cost", "PERWT24F"]].sum()
    means = cells.weighted_cost / cells.PERWT24F
    keys = zip(np.digitize(d.A_AGE, [18, 35, 50, 65]), np.where(d.PENATVTY == 57, 1, 2))
    component["health"] = np.array([means[key] for key in keys]) * ~((d.PUB == 0) & (d.PRIV == 0))
    d["balance"] = component["tax"] - component["cash"] - component["noncash"] - component["health"]
    d["nohealth"] = d.balance + component["health"]
    d["weight"] = d.MARSUPWT / 100
    d["band"] = np.digitize(d.A_AGE, [18, 25, 35, 45, 55, 65, 75])
    native = d.PRCITSHP.isin([1, 2, 3])
    us = [57, 60, 66, 69, 73, 78]
    parents_us = d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us)
    masks = {
        "white": native & parents_us & (d.PEHSPNON == 2) & (d.PRDTRACE == 1),
        "native": native,
        "G1": d.PRCITSHP.isin([4, 5]) & (d.PENATVTY == 303),
        "G2": native & ((d.PEFNTVTY == 303) | (d.PEMNTVTY == 303)),
        "G3": native & parents_us & (d.PRDTHSP == 1),
    }
    if sum(masks[g].astype(int) for g in ["G1", "G2", "G3"]).gt(1).any():
        raise ValueError("Target populations overlap")
    civilian = (d.PRPERTYP == 2) | (d.A_AGE < 15)
    profiles = {}
    for group, mask in masks.items():
        profiles[group] = {}
        for band, sub in d[mask & civilian].groupby("band"):
            if sub.weight.sum() <= 0:
                raise ValueError(f"Nonpositive denominator: {group}/{band}")
            values = {"population": float(sub.weight.sum()), "n": len(sub)}
            for key in ["balance", "nohealth"]:
                values[key] = float(np.average(sub[key], weights=sub.weight))
            for key, array in component.items():
                values[key] = float(np.average(np.asarray(array)[sub.index], weights=sub.weight))
            profiles[group][int(band)] = values
        if set(profiles[group]) != set(range(8)):
            raise ValueError(f"Missing age bands for {group}")
    rows = []
    for group in ["G1", "G2", "G3"]:
        sub = d[masks[group] & civilian]
        row = {"group": group, "population": float(sub.weight.sum()),
               "absolute_balance": float(sub.balance @ sub.weight)}
        for ref in ["white", "native"]:
            for metric in ["balance", "nohealth"]:
                reference = sub.band.map({b: p[metric] for b, p in profiles[ref].items()})
                row[f"gap_{ref}_{metric}"] = float((sub.weight * (sub[metric] - reference)).sum())
        rows.append(row)
    extension = pd.read_csv(inputs["extension"])
    extension = extension[extension.allocation.eq("equal_all_members") & extension.weighting.eq("person")]
    extension = extension.set_index(["group", "metric"], verify_integrity=True).estimate
    extra = []
    for group, label in [("G1", "mexico_born"), ("G2", "mexican_second_gen"), ("G3", "mexican_third_plus_selfid")]:
        population = float(d.loc[masks[group] & civilian & d.A_AGE.between(25, 64), "weight"].sum())
        for ref in ["third_plus_nh_white", "all_native"]:
            delta = {metric: float(sign * (extension[label, metric] - extension[ref, metric]) * population)
                     for metric, sign in [("employer_payroll", 1), ("sales_tax_share35", 1),
                                          ("property_tax_owner", 1), ("k12_charged_acs_native", -1)]}
            lunch = lambda g: extension[g, "extended_balance_net_of_school_lunch"] - extension[g, "extended_balance_base"]
            extra.append({"group": group, "reference": ref, "adult_population": population,
                          "increment": sum(delta.values()), **delta,
                          "lunch_gap_correction": float((lunch(label) - lunch(ref)) * population)})
    totals = {k: sum(r[k] for r in rows) for k in rows[0] if k != "group"}
    output = {"inputs": provenance, "raw_validation": validation, "meps_anchors": anchors,
              "groups": rows, "totals": totals, "profiles": profiles, "extension_from_csv": extra}
    destination = HERE / "derived"
    destination.mkdir(exist_ok=True)
    (destination / "audit.json").write_text(json.dumps(output, indent=2, allow_nan=False) + "\n")
    print(json.dumps({"totals": totals, "extension_from_csv": extra}, indent=2, allow_nan=False))


if __name__ == "__main__":
    main()
