"""Read-only population, household and production-attribution diagnostics.

Prints JSON; never rebuilds or edits an audited lane. Counts describe the original
canonical CPS frame, before the later population correction. No policy savings.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess

import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
LANE = ROOT / "infra/immigration-fiscal"
SOURCE = LANE / "cps_imputation_keys_2026_09_23/_cache/asec25_lane.parquet"
PROD = LANE / "generation_account_2026_09_24/derived/production_by_generation.json"
BUILDER = LANE / "full_account_spending_2026_09_20/builder.py"
PINS = {
    SOURCE: "c5b881660ac06c80ff8cf424c2d4be0120a661a8e31357252ba1d98b92f447fb",
    PROD: "6a486fd4439a7721fceca5f3582851b5084b1c75861ba18adab6eb3a7f08e773",
    BUILDER: "a0c69ac4c5d935b7fad99c1f8909ef7b753c77a1596d4747ddad8dc7240541fd",
}


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def main():
    for path, expected in PINS.items():
        if not path.exists() or sha(path) != expected:
            raise RuntimeError(f"Audit snapshot absent or changed: {path}")
    spec = importlib.util.spec_from_file_location("audit_spending", BUILDER)
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)
    fields = ["pwwgt0", "PRPERTYP", "A_AGE", "PRCITSHP", "PENATVTY",
              "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "SPM_ID",
              "SPM_SNAPSUB", "SPM_CAPHOUSESUB", "SPM_WICVAL", "SPM_ENGVAL"]
    d = pd.read_parquet(SOURCE, columns=fields)
    if d.isna().any().any() or not (d.pwwgt0 >= 0).all():
        raise ValueError("Missing fields or invalid weights")
    civ, target = (pd.Series(x, index=d.index) for x in builder.canonical_target(d))
    w = d.pwwgt0
    count = lambda mask: float(w[mask].sum())
    nt = count(target)
    if abs(nt - 40896574.15235156) > .01:
        raise ValueError("Canonical target population drift")
    any_target = target.groupby(d.SPM_ID).transform("any")
    any_outside = (civ & ~target).groupby(d.SPM_ID).transform("any")
    mixed = any_target & any_outside
    demography = {
        "canonical_target_people": nt,
        "native_target_share": count(target & d.PRCITSHP.isin([1, 2, 3])) / nt,
        "citizen_target_share": count(target & d.PRCITSHP.isin([1, 2, 3, 4])) / nt,
        "noncitizen_target_share": count(target & d.PRCITSHP.eq(5)) / nt,
        "outside_civ_people_sharing_target_SPM_unit": count(civ & ~target & any_target),
        "outside_civ_children_under18_sharing_target_SPM_unit":
            count(civ & ~target & any_target & d.A_AGE.lt(18)),
        "target_people_in_mixed_SPM_unit": count(target & mixed),
    }
    unit_size = d.groupby("SPM_ID").SPM_ID.transform("size")
    benefits = {}
    for field in ["SPM_SNAPSUB", "SPM_CAPHOUSESUB", "SPM_WICVAL", "SPM_ENGVAL"]:
        if not d.groupby("SPM_ID")[field].nunique().eq(1).all():
            raise ValueError(f"Nonconstant resource-unit amount: {field}")
        per_person = d[field] / unit_size
        dollars = lambda mask: float((w[mask] * per_person[mask]).sum())
        benefits[field] = {
            "target_allocated_dollars": dollars(target),
            "target_allocated_dollars_in_mixed_units": dollars(target & mixed),
            "share_in_mixed_units": dollars(target & mixed) / dollars(target),
        }
    prod = json.loads(PROD.read_text())
    nonadditivity = {}
    for norm, ref in prod["reference"].items():
        total = lambda entry: entry["P"] + entry["F"]
        attributed = {g: total(v) for g, v in ref["attribution_a"].items()}
        standalone = {g: total(v) for g, v in ref["standalone_a"].items()}
        union = total(ref["union"])
        if abs(sum(attributed.values()) - union) > 1e-6:
            raise ValueError(f"Generation attribution does not close: {norm}")
        nonadditivity[norm] = {
            "unit": "billions 2024 dollars annually; P+F",
            "union": union, "attribution_a": attributed, "standalone_a": standalone,
            "standalone_sum": sum(standalone.values()),
            "standalone_sum_share_of_union": sum(standalone.values()) / union,
        }
    output = {
        "head": subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(),
        "inputs_sha256": {str(p.relative_to(ROOT)): sha(p) for p in PINS},
        "interpretation": "Original CPS weights, descriptive allocations; no causal savings, "
                          "unauthorized-status inference, survey intervals or policy effect.",
        "demography": demography, "unit_benefit_allocations": benefits,
        "production_nonadditivity": nonadditivity,
    }
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
