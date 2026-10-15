"""Item-12 economic transport from the coverage lane's exact central donors.

The published coverage JSON originally omitted donor IDs and weights. This
adapter exports the unchanged canonical factor callable against its own pinned
pricing cache, then verifies it against sets.<basis>.scenarios.central. It never
copies a coverage formula. Signed missing mass is retained, including overcount
cells. Fiscal prices are the canonical constructed-person prices.
"""
import argparse
import hashlib
import importlib.util
import json
import resource
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
COVERAGE = HERE.parent / "coverage_bound_2026_10_14"
GENS = ("G1", "G2", "G3+")


def require(ok, why):
    if not ok:
        raise SystemExit("[BLOCKED] coverage transport: " + why)


def digest(path):
    with Path(path).open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def paths(case="oct15", basis="cash"):
    require(basis in ("cash", "set"), "explicit cash/set basis required")
    return (HERE / f"derived/coverage_donors_{case}_{basis}.csv",
            HERE / f"derived/coverage_transport_{case}_{basis}.json")


def validate_closure(donors, central):
    """Principal-source closure, separately by generation and fiscal end."""
    for generation in GENS:
        d = donors[donors.generation.eq(generation)]
        g = generation.replace("G3+", "G3plus")
        want = central["implied_net_missing_people"][g]
        if g == "G3plus":
            want += central["implied_net_missing_people"].get("added", 0.)
        require(abs(d.coverage_weight.sum() - want) < 1e-6,
                f"{generation} missing people do not close")
        for end in ("low", "high"):
            got = float(d.coverage_weight @ d[f"fiscal_{end}_bn_per_person"])
            require(abs(got - central["ends"][end]["by_generation"][g]) < 1e-9,
                    f"{generation}/{end} fiscal amount does not close")


def export(case="oct15", basis="cash"):
    """Capture canonical central donor computation; no upstream outputs mutate."""
    start = time.perf_counter()
    sys.path.insert(0, str(COVERAGE))
    import coverage_bound as canonical
    from export_pricing import constructed_prices
    from source_tables import load

    published_path = COVERAGE / f"derived/coverage_bound_{case}.json"
    published = json.loads(published_path.read_text())
    require(published["key"] == case, "published case key differs")
    central = published["sets"][basis]["scenarios"]["central"]
    cache_path = COVERAGE / f"_cache/{case}/{basis}/pricing.npz"
    audit_path = COVERAGE / f"derived/pricing_audit_{case}_{basis}.json"
    audit = json.loads(audit_path.read_text())
    require(audit["case"] == case and audit["basis"] == basis, "cache case/basis differs")
    manifest_path = COVERAGE / f"inputs/pricing_dependencies_{case}_{basis}.json"
    canonical.validate_cache_receipt(audit, manifest_path, cache_path)
    names = ("weights", "added_weights", "generation", "age", "sex", "arrival", "hispanic",
             "person_ph_seq", "person_pppos", "net_id", "net_added", "excluded_use_prices",
             "constructed_piece_prices", "base_piece_prices")
    with np.load(cache_path) as cache:
        data = {name: cache[name] for name in names}
    constructed_prices(data, audit)
    rates, base = load()
    f, af = canonical.factors(data, rates, base)
    require(np.all(data["added_weights"][:, 0] * af == 0), "nonzero latent coverage needs an explicit donor arm")
    donors = pd.DataFrame(dict(PH_SEQ=data["person_ph_seq"], PPPOS=data["person_pppos"],
        age=data["age"], sex=data["sex"], generation=np.array(GENS)[data["generation"]],
        counted_weight=data["weights"][:, 0], coverage_weight=data["weights"][:, 0] * f,
        fiscal_low_bn_per_person=data["net_id"][0, :, 0],
        fiscal_high_bn_per_person=data["net_id"][1, :, 0]))
    require(not donors.duplicated(["PH_SEQ", "PPPOS"]).any(), "duplicate donor ID")
    validate_closure(donors, central)
    destination, receipt_path = paths(case, basis)
    destination.parent.mkdir(exist_ok=True)
    donors.to_csv(destination, index=False, float_format="%.17g", lineterminator="\n")
    sources = [published_path, cache_path, audit_path, manifest_path, COVERAGE / "coverage_bound.py",
               COVERAGE / "source_tables.py", COVERAGE / "export_pricing.py", Path(__file__)]
    receipt = dict(case=case, basis=basis, scenario="central", rule="option_A_canonical_coverage_donors",
        export_remedy="Published JSON lacks donor IDs; unchanged canonical factors callable exports its exact donors; principal central counts and fiscal amounts gate admission.",
        source_hashes={str(p.relative_to(ROOT)): digest(p) for p in sources},
        donor_csv_sha256=digest(destination), rows=len(donors),
        missing_people={g: float(donors.coverage_weight[donors.generation.eq(g)].sum()) for g in GENS},
        fiscal_bn={e: float(donors.coverage_weight @ donors[f"fiscal_{e}_bn_per_person"]) for e in ("low", "high")},
        economic_assumption="Each classified economic component follows the case's same-age/sex/completed-generation canonical donor distribution; signed coverage weights retained.",
        gates=dict(counts_close=True, fiscal_close=True))
    receipt_path.write_text(json.dumps(receipt, indent=1, sort_keys=True) + "\n")
    sys.path.insert(0, str(HERE.parent / "scripts"))
    from memory_budget import require_within_budget
    peak = require_within_budget("world coverage donor export")
    print(f"coverage donor export elapsed {time.perf_counter()-start:.3f}s; peak physical {peak/1e6:.1f} MB; "
          f"resource maxrss {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}", file=sys.stderr)
    return receipt


def load_donors(case="oct15", basis="cash"):
    destination, receipt_path = paths(case, basis)
    require(destination.exists() and receipt_path.exists(), "donor export absent; run coverage_transport.py first")
    receipt = json.loads(receipt_path.read_text())
    require(receipt["case"] == case and receipt["basis"] == basis, "donor receipt case/basis differs")
    for relative, sha in receipt["source_hashes"].items():
        require(digest(ROOT / relative) == sha, "stale source " + relative)
    require(digest(destination) == receipt["donor_csv_sha256"], "donor file hash differs")
    return pd.read_csv(destination, float_precision="round_trip"), receipt


def transport_weights(frame, case="oct15", basis="cash"):
    """Add exact donor mass without changing any counted record or reference payer."""
    require("coverage_pw" not in frame, "coverage transport already applied")
    donors, receipt = load_donors(case, basis)
    ids = pd.MultiIndex.from_frame(frame[["PH_SEQ", "PPPOS"]])
    require(ids.is_unique, "frame IDs not unique")
    positions = ids.get_indexer(pd.MultiIndex.from_frame(donors[["PH_SEQ", "PPPOS"]]))
    require(np.all(positions >= 0), "a canonical donor is missing from completed frame")
    require(np.array_equal(frame.A_AGE.to_numpy()[positions], donors.age.to_numpy()), "donor ages differ")
    if "A_SEX" in frame:
        require(np.array_equal(frame.A_SEX.to_numpy()[positions], donors.sex.to_numpy()), "donor sexes differ")
    if "gen" in frame:
        require(np.array_equal(frame.gen.to_numpy()[positions], donors.generation.to_numpy()), "completed donor generations differ")
    delta = np.zeros(len(frame))
    delta[positions] = donors.coverage_weight.to_numpy()
    require(np.all(frame.target.to_numpy()[positions]), "donor is outside completed members")
    out = frame.copy()
    out["pw_counted"] = frame.pw.to_numpy()
    out["coverage_pw"] = delta
    out["pw"] = frame.pw.to_numpy() + delta
    require(np.all(out.pw >= 0), "negative completed donor weight")
    out.attrs["coverage_economic_counterfactual"] = receipt
    return out


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--case", default="oct15")
    parser.add_argument("--basis", choices=("cash", "set"), default="cash")
    args = parser.parse_args()
    print(json.dumps(export(args.case, args.basis), indent=1))
