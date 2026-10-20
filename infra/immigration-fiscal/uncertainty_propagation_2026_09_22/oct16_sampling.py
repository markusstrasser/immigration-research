"""Oct16 conditional signed-driver sampling, with independent ACS and PES blocks.

The principal costs are the case's exact all-specification values. Sampling
changes are re-evaluated on the source's delivered person drivers, fixing their
national masses and source calibration coefficients. Interior source amounts
are repriced; a changed key shape is a disclosed transport, not an own-key run.
Native-First: reuse source kernels, calibration, tenure and donor builders.
"""
from __future__ import annotations

import argparse
import copy
import gc
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import time
from source_cache import CACHE as SOURCE_CACHE, MANIFEST as SOURCE_MANIFEST, load_sources

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
COVER = FISCAL / "coverage_bound_2026_10_14"
COUNT = FISCAL / "count_composition_r5_2026_10_15"
OUT = HERE / "derived/oct16"
sys.dont_write_bytecode = True
sys.path.insert(0, str(COVER))
sys.path.insert(0, str(COUNT))
sys.path.insert(0, str(FISCAL / "scripts"))
import coverage_oct16 as K
import native_measure as N
from tenure import fixed_count_tenure, split_factors, tenure_rates
from memory_budget import require_within_budget
from mixed_interaction import item10_flags
from health21_sampling import Builder as Health21


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] oct16 uncertainty: " + message)


def digest(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def support_hashes(data):
    require(data["weights"].ndim == 2 and data["weights"].shape[1] == 161
            and data["added_weights"].shape == data["weights"].shape, "source CPS161 weight shape")
    return {key: {"sha256": hashlib.sha256(np.ascontiguousarray(data[key]).tobytes()).hexdigest(),
                  "shape": list(data[key].shape), "dtype": str(data[key].dtype)}
            for key in ("weights", "added_weights", "age", "sex", "arrival", "hispanic", "generation", "person_ph_seq", "person_pppos")}


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + "\n")


def health_dependencies():
    lane = FISCAL/"spending_keys_r5_2026_10_15"
    return [HERE/"health21_sampling.py", HERE/"propagate.py", lane/"health_residual.py", lane/"health_coverage.py", lane/"health_ratios.py",
            lane/"derived/item21.json", lane/"derived/item21_snapshot.json",
            FISCAL/"build/meps_health_transport_2024.py",
            ROOT/"sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip",
            ROOT/"sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt"]


def sdr(x):
    x = np.asarray(x, float)
    return float(np.sqrt(4 / (len(x)-1) * np.square(x[1:]-x[0]).sum()))


def covariance(x, y):
    return float(4/(len(x)-1) * np.dot(x[1:]-x[0], y[1:]-y[0]))


def prepare():
    """Read the actual 80 joint ACS targets; keep their cross-cell covariance."""
    acs_all = N.load_acs_minors()
    acs = acs_all[~acs_all.MIL.isin([1, 2])].copy()
    del acs_all
    targets = {}
    for region in ("CA_TX", "outside_CA_TX"):
        rm = acs.STATE.isin([6, 48]).to_numpy()
        if region == "outside_CA_TX":
            rm = ~rm
        for lo, hi in N.AGES:
            mask = rm & acs.AGEP.between(lo, hi).to_numpy()
            targets[f"{region}|{lo}-{hi}"] = {
                kind: acs.loc[mask & kind_mask, N.AW].to_numpy(float).sum(axis=0).tolist()
                for kind, kind_mask in N.categories(acs, True).items()}
    paths = [N.ACS, N.ACS_REL, COUNT/"native_measure.py", COUNT/"derived/native_calibration_replicates.json"]
    receipt = {"targets": targets, "source_sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths},
               "rule": "80 official joint ACS SDR target columns; no CPS-plus-ACS difference SE appended"}
    require_within_budget("oct16 ACS target preparation")
    write(OUT/"acs_targets.json", receipt)


def calibration(data, roster, acs_targets):
    ids = pd.MultiIndex.from_arrays([data["person_ph_seq"], data["person_pppos"]])
    person = roster.set_index(["PH_SEQ", "PPPOS"]).reindex(ids)
    require(not person.isna().any().any(), "missing kernel person calibration cell")
    cells = json.loads((COUNT/"derived/native_calibration_replicates.json").read_text())["cells"]
    native = person.PRCITSHP.isin([1, 2, 3]).to_numpy() & (data["age"] < 18)
    mex, other = person.PRDTHSP.eq(1).to_numpy(), person.PRDTHSP.gt(1).to_numpy()
    conditional = np.ones_like(data["weights"])
    acs_factor = np.ones((len(ids), 81))
    for key, cell in cells.items():
        region, ages = key.split("|")
        lo, hi = map(int, ages.split("-"))
        rm = person.GESTFIPS.isin([6, 48]).to_numpy()
        if region == "outside_CA_TX":
            rm = ~rm
        mask = native & rm & (data["age"] >= lo) & (data["age"] <= hi)
        for chosen, field in ((mex, "mexican_rake_factor"), (other, "hispanic_reassignment_factor")):
            conditional[mask & chosen] = np.asarray(cell[field])
        # The central policy preserves CPS Hispanic totals. ACS perturbs only
        # the Mexican target, balancing other Hispanic weights on the same cell.
        require(np.allclose(cell["native_factor"], 1., rtol=0, atol=1e-12), "unsupported ACS-lower-total policy")
        central_mex = float(cell["target_mexican"][0]) / float(cell["mexican_rake_factor"][0])
        central_h = float(cell["target_hispanic"][0])
        central_other = central_h-central_mex
        require(central_other > 0, "empty balancing origin stratum")
        target = np.asarray(acs_targets[key]["mexican"])
        acs_factor[mask & mex] = target/central_mex
        acs_factor[mask & other] = (central_h-target)/central_other
        require(np.all(target > 0) and np.all(target < central_h), "ACS replicate target outside CPS Hispanic control")
    central = pd.read_parquet(COUNT/"derived/native_person_factors.parquet").set_index(["PH_SEQ", "PPPOS"]).reindex(ids)
    require(np.allclose(conditional[:, 0], central.central_member_factor, rtol=0, atol=1e-12), "central source factors differ")
    require(np.allclose(acs_factor[:, 0], conditional[:, 0], rtol=0, atol=1e-12), "ACS central target differs")
    return person.H_TENURE.to_numpy(int), conditional, acs_factor


def tenure_mass(data, tenure, weights, rates, base, marginal):
    """Vectorized source formula; equality to source fixed_count_tenure is gated."""
    _, da, pes = split_factors(data, rates, base)
    odds = {t: 1/(1+marginal[t]["all"]["nce_pct"]/100)-1 for t in ("owner", "renter")}
    tilt = np.where(tenure == 1, odds["owner"], odds["renter"])
    result = weights*da[:, None]
    _, inverse = np.unique(np.column_stack((data["age"], data["sex"], data["generation"])), axis=0, return_inverse=True)
    for cell in np.unique(inverse):
        mask = inverse == cell
        source = weights[mask]*pes[mask, None]
        target, denominator = source.sum(axis=0), (source*tilt[mask, None]).sum(axis=0)
        require(np.all((np.abs(denominator) > 1e-15) | (np.abs(target) < 1e-12)), "zero tenure support")
        scale = np.divide(target, denominator, out=np.zeros_like(target), where=denominator != 0)
        require(np.all(scale >= 0), "tenure tilt reverses signed cell")
        result[mask] += source*tilt[mask, None]*scale
    return result


def source_ratio(piece, row, source_rows):
    end = piece["end"]
    anchors = [r for r in source_rows if r.get("anchor_end") == end]
    require(len(anchors) == 1, "unique authoritative source anchor required: "+end)
    anchor = anchors[0]
    generation, side, line = piece["generation"], piece["source_side"], piece["source_line"]
    # Prefer an exact carrier's own evaluated amount when the producer exposes
    # it; source_line otherwise identifies the principal parent declaration.
    exact = side+":"+piece["line"]
    key = exact if exact in row["source_terms"][generation] else side+":"+line
    now, old = row["source_terms"][generation].get(key), anchor["source_terms"][generation].get(key)
    if now is None or old is None:
        return 1., "unmatched source piece; conditional endpoint driver held"
    a, b = now["cost_bn"], old["cost_bn"]
    driver = piece.get("key", "")
    if line == "medicaid_and_chip_other_medical" and key == "spending:"+line:
        if "canonical spending:medicaid" in driver:
            a, b = now["medicaid_base_cost_bn"], old["medicaid_base_cost_bn"]
        elif "uninsured person-years" in driver:
            a -= now["medicaid_base_cost_bn"]
            b -= old["medicaid_base_cost_bn"]
        else:
            return a/b if b else 1., "unmatched Medicaid subdriver; conditional endpoint driver held"
        require(abs(b) > 1e-12 or abs(a) < 1e-9, "zero Medicaid subdriver support")
        return a/b if b else 1., "exact own-spec medical/uninsured component coefficient"
    # The source household builder fixes its school/P person vectors before
    # looping readings and splits each line by their generation key masses
    # (households.py818–830,897–900). Specification school share changes the
    # line's evaluated response, not those fixed source-vector shares. Carry
    # that delivered conditional shape and reprice the actual line amount;
    # inferring a new mixture from the budget-share coordinate would invent a
    # different source allocation (including Pell and capital routes).
    if abs(b) < 1e-12:
        require(abs(a) < 1e-9, "interior nonzero source has zero endpoint support: "+key)
        return 1., "zero source in both specifications"
    note = "delivered source shape, per-specification amount"
    if now["key"] != old["key"]:
        note = f"[APPROX] endpoint key {old['key']} transported to {now['key']}"
    return a/b, note


def pes_sigma(gradient, errors):
    terms = np.abs(gradient)*errors
    independent = float(np.linalg.norm(terms))
    maximum = float(terms.sum())
    minimum = float(max(0., 2*terms.max()-terms.sum()))
    return independent, minimum, maximum


def price_vectors(data, audit, row, source_rows):
    reading = row["coordinates"]["reading"]
    observed = np.zeros(len(data["weights"])); constructed = observed.copy()
    notes = set()
    for i, piece in enumerate(audit["denominator_pieces"]):
        if piece["end"] != reading:
            continue
        factor, note = source_ratio(piece, row, source_rows)
        observed += factor*data["base_piece_prices"][i]
        constructed += factor*data["constructed_piece_prices"][i]
        if note.startswith("[APPROX]") or note.startswith("unmatched"):
            notes.add(note+": "+piece["source_line"])
    added = observed.copy()
    for i, piece in enumerate(audit["other_pieces"]):
        if piece["end"] != reading:
            continue
        p = data["other_piece_prices"][i]
        if piece["population"] != "added":
            observed += p
            constructed += p
        if piece["population"] != "identified":
            added += p
    return observed, constructed, added, notes


def health_vector(data, audit, row, source_rows):
    value = np.zeros(len(data["weights"]))
    for i, piece in enumerate(audit["denominator_pieces"]):
        if piece["end"] == row["coordinates"]["reading"] and piece["source_side"] == "spending" and piece["source_line"] == "health_services":
            factor, _ = source_ratio(piece, row, source_rows)
            value += factor*data["base_piece_prices"][i]
    return value


def source_coverage(basis):
    """Use coverage's oct15 kernel, distinct from counts' final-routing kernel."""
    sources = load_sources()["sets"][basis]
    dependencies = health_dependencies()+[Path(__file__).resolve(), HERE/"source_cache.py", SOURCE_CACHE, SOURCE_MANIFEST, COVER/"coverage_oct16.py",
        FISCAL/"main_case_2026_10_16/coverage_snapshot.cjs", COVER/f"_cache/oct15/{basis}/pricing.npz",
        COVER/f"derived/pricing_audit_oct15_{basis}.json", COVER/f"inputs/pricing_dependencies_oct15_{basis}.json"]
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    snapshot = json.loads(subprocess.run(["node", str(FISCAL/"main_case_2026_10_16/coverage_snapshot.cjs")],
                                        capture_output=True, text=True, check=True).stdout)
    data, audit = K.load_kernel(basis, "oct15")
    K.transform(data, audit, snapshot, basis)
    health = Health21()
    rates, base = K.load()
    factor, _ = K.C.factors(data, rates, base)
    missing = data["weights"]*factor[:, None]
    rows = {}
    for row in sources["rows"]:
        _, constructed, _, notes = price_vectors(data, audit, row, sources["rows"])
        hp = health.vectors(health.central, data, audit, basis, row["coordinates"]["reading"], snapshot["rate"])
        vector = (constructed+hp[1])@missing
        if row["anchor_end"] is not None:
            expected = sources["meta"]["coverage"]["by_end"][row["coordinates"]["reading"]]["total_bn"]
            require(abs(vector[0]-expected) < 1e-9, "source oct15-vintage coverage monetary point closure")
        rows[str(row["spec"])] = {"replicates_bn": vector.tolist(), "transport": sorted(notes),
            "health21_coverage_bn": float(hp[1]@missing[:, 0])}
    peak = require_within_budget("oct16 original coverage source161")
    require(all(digest(ROOT/p) == expected for p, expected in hashes.items()), "source changed during own coverage evaluation")
    write(OUT/f"coverage_replicates_{basis}.json", {"basis": basis, "vintage": "oct15", "rows": rows, "support_sha256": support_hashes(data),
        "source_sha256": hashes,
        "rule": "Original coverage source kernel, transformed at each specification. Native16/17 use their distinct oct15_final_routing source kernel."})
    print(f"PASS {basis} own coverage-vintage vectors; physical {peak/1e9:.3f}GB")


def calculate(basis, require_own=False):
    start = time.perf_counter()
    sources = load_sources()
    dependencies = [Path(__file__).resolve(), HERE/"oct16_specs.cjs", HERE/"source_cache.py", SOURCE_CACHE, SOURCE_MANIFEST, OUT/"acs_targets.json",
        COVER/"coverage_oct16.py", COVER/"coverage_bound.py", COVER/"source_tables.py", COUNT/"tenure.py",
        COUNT/"measure.py", COUNT/"mixed_interaction.py", COUNT/"native_measure.py",
        COUNT/"derived/native_calibration_replicates.json", COUNT/"derived/native_person_factors.parquet",
        COVER/f"_cache/oct15_final_routing/{basis}/pricing.npz",
        COVER/f"derived/pricing_audit_oct15_final_routing_{basis}.json",
        COVER/f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json"]
    dependencies.extend(health_dependencies()+[OUT/"item21_pooled_covariance.json", OUT/f"coverage_replicates_{basis}.json"])
    source_sha256 = {str(p.relative_to(ROOT)): digest(p) for p in dependencies}
    block = sources["sets"][basis]
    require("health_residual_key" in block["items"] and "passthrough_source_tax" not in block["items"],
            "central selection must include21 and exclude unidentified19")
    if require_own:
        require(all(r["anchor_end"] is not None for r in block["rows"]),
                "require_own: source10/11 deliver endpoint stacks only; interior all-spec own-key U06 is unmeasured")
    targets = json.loads((OUT/"acs_targets.json").read_text())["targets"]
    coverage_record = json.loads((OUT/f"coverage_replicates_{basis}.json").read_text())
    require(all(digest(ROOT/p) == expected for p, expected in coverage_record["source_sha256"].items()),
            "source changed after own coverage-vintage evaluation")
    coverage_source = coverage_record["rows"]
    snapshot = json.loads(subprocess.run(["node", str(FISCAL/"main_case_2026_10_16/coverage_snapshot.cjs")],
                                        text=True, capture_output=True, check=True).stdout)
    data, audit = K.load_kernel(basis, "oct15_final_routing")
    require(support_hashes(data) == coverage_record["support_sha256"],
            "coverage/count person weights differ; shared health derivative support requires own transport")
    old_prices = {row["spec"]: price_vectors(data, audit, row, block["rows"])[:3] for row in block["rows"]}
    # Keep an exact copy only of source point totals, not a second price matrix.
    K.transform(data, audit, snapshot, basis)
    roster = N.load_cps()[["PH_SEQ", "PPPOS", "GESTFIPS", "PRCITSHP", "PRDTHSP"]]
    frame = pd.read_parquet(FISCAL/"generation_account_2026_09_24/_cache/asec25_generation.parquet",
                           columns=["PH_SEQ", "PPPOS", "H_TENURE"])
    roster = roster.merge(frame, on=["PH_SEQ", "PPPOS"], validate="one_to_one")
    tenure, factors, acs_factors = calibration(data, roster, targets)
    del roster, frame
    rates, base = K.load()
    marginal = tenure_rates()
    old_payload = json.loads((FISCAL/f"main_case_2026_10_15/derived/corrections{'_cash' if basis == 'cash' else ''}.json").read_text())
    flags = item10_flags(data, old_payload)
    W, AW = data["weights"], data["added_weights"]
    native_W = W*factors
    native_AW = AW.copy()
    native_AW[flags["nonreporter"]] *= factors[flags["nonreporter"]]
    missing = tenure_mass(data, tenure, native_W, rates, base, marginal)
    f0, _ = K.C.factors(data, rates, base)
    for r in (0, 1, 80, 160):
        proof, _ = fixed_count_tenure(data, tenure, native_W[:, r], rates, base, marginal)
        require(np.allclose(missing[:, r], native_W[:, r]*proof, rtol=0, atol=1e-7), "vectorized tenure/source mass differs")
    # Full ACS-target changes on central CPS, carrying all eight target cells jointly.
    acs_W = W[:, :1]*acs_factors
    acs_AW = np.broadcast_to(AW[:, :1], acs_W.shape).copy()
    acs_AW[flags["nonreporter"]] *= acs_factors[flags["nonreporter"]]
    acs_missing = tenure_mass(data, tenure, acs_W, rates, base, marginal)
    # Finite difference actual source common-NCE and conditional tenure kernel.
    # All axes use signed fractions, so the primary percent fields move by100h.
    gradients = []
    for axis in ("common_nce", "owner", "renter"):
        by_h = []
        for h in (1e-4, 1e-5):
            shifted = []
            for sign in (-1, 1):
                rr, mm = copy.deepcopy(rates), copy.deepcopy(marginal)
                if axis == "common_nce":
                    for z in rr["hispanic"].values():
                        z["nce_pct"] += sign*h*100
                else:
                    mm[axis]["all"]["nce_pct"] += sign*h*100
                shifted.append(tenure_mass(data, tenure, native_W[:, :1], rr, base, mm)[:, 0])
            by_h.append((shifted[1]-shifted[0])/(2*h))
        # Richardson extrapolation; record convergence per final price vector below.
        gradients.append((by_h[1]+(by_h[1]-by_h[0])/99, by_h[1]))
    errors = np.array([marginal["all"]["se_pct"], marginal["owner"]["all"]["se_pct"], marginal["renter"]["all"]["se_pct"]])/100
    require(np.allclose(errors, [.0053, .007, .0087], rtol=0, atol=1e-12), "Table D marginal SEs changed")
    health = Health21()
    pooled = json.loads((OUT/"item21_pooled_covariance.json").read_text())
    donor_covariance, donor_cells = health.donor_covariance()
    rate = snapshot["rate"]
    health_prices, ratio_gradients, donor_gradients = {}, {}, {}
    for reading in ("low", "high"):
        health_prices[reading] = health.vectors(health.central, data, audit, basis, reading, rate)
        ratio_gradients[reading] = health.gradients(data, audit, basis, reading, rate,
            native_W[:, 0], missing[:, 0], native_AW[:, 0], pooled["cells"])
        donor_gradients[reading] = health.gradients(data, audit, basis, reading, rate,
            native_W[:, 0], missing[:, 0], native_AW[:, 0], donor_cells, donor=True)
    rows, vectors, acs_vectors, transport, item_vectors = [], {}, {}, [], {}
    for row in block["rows"]:
        spec, reading = row["spec"], row["coordinates"]["reading"]
        observed, constructed, added_observed, notes = price_vectors(data, audit, row, block["rows"])
        hp = health_prices[reading]
        own21_parts = row["v9_post_engine"]["parts"]["health_residual_key"]
        require(all(p["population"] != "coverage" for p in own21_parts), "coverage21 counted in direct post twice")
        for part in own21_parts:
            if "capital_stock_delta_bn" in part:
                require(abs(part["delta_bn"]-part["capital_stock_delta_bn"]*rate) < 1e-9,
                        "native21 direct capital is not valued at live20 rate; consumer cannot repair source silently")
        require(abs(float(hp[0]@W[:, 0]+hp[2]@AW[:, 0])-sum(p["delta_bn"] for p in own21_parts)) < 1e-9,
                "item21 own direct health/state-price/capital monetary source oracle")
        observed += hp[0]
        constructed += hp[1]
        added_observed += hp[2]
        if require_own and notes:
            raise ValueError("[BLOCKED] require_own: "+"; ".join(sorted(notes)))
        conditional = observed @ native_W + added_observed @ native_AW + constructed @ missing
        acs = observed @ acs_W + added_observed @ acs_AW + constructed @ acs_missing
        without_native = observed @ W + added_observed @ AW + constructed @ (W*f0[:, None])
        native_delta = conditional-without_native
        item16 = (observed @ (native_W-W) + added_observed @ (native_AW-AW)
                  + constructed @ ((native_W-W)*f0[:, None]))
        item17 = constructed @ (missing-native_W*f0[:, None])
        old_observed, old_constructed, old_added = old_prices[spec]
        coverage_repricing = (constructed-old_constructed) @ (W*f0[:, None])
        completion_repricing = ((observed-old_observed) @ (W*flags["reporter"][:, None])
                                + (added_observed-old_added) @ (AW*flags["nonreporter"][:, None]))
        item21_engine = hp[0] @ (W*(~flags["reporter"])[:, None])
        # Original latent descendants retain the source's declared price-profile
        # placement; observed item10 nonreporters belong to its own source block.
        item21_engine += hp[2] @ (AW*(~flags["nonreporter"])[:, None])
        require(np.allclose(item16+item17, native_delta, rtol=0, atol=1e-9), "joint-minus16 replicate closure")
        if row["anchor_end"] is not None:
            for values, key in ((item16, "native_minor_calibration"), (item17, "coverage_tenure")):
                expected_delta = block["meta"][key]["by_end"][reading]["total_bn"]
                require(abs(values[0]-expected_delta) < 1e-9,
                        f"{key} monetary source closure {values[0]} vs {expected_delta}")
        require(np.isclose(conditional[0], acs[0], rtol=0, atol=1e-9), "CPS/ACS central monetary closure")
        gradient = np.array([constructed @ g[0] for g in gradients])
        check = np.array([constructed @ g[1] for g in gradients])
        require(np.all(np.abs(gradient-check) < np.maximum(1e-6, np.abs(gradient)*1e-6)), "PES finite differences fail")
        se_cps, se_acs = sdr(conditional), sdr(acs)
        pi, pl, pu = pes_sigma(gradient, errors)
        point = row["cost_bn"]
        independent = float(np.sqrt(se_cps**2+se_acs**2+pi**2))
        correlated = float(np.sqrt(se_cps**2+se_acs**2+pu**2))
        rows.append({"case": "oct16", "basis": basis, "spec": spec, "reading": reading,
            "net_cost_bn": point, "kernel_point_bn": float(conditional[0]),
            "fixed_principal_minus_kernel_bn": float(point-conditional[0]),
            "se_conditional_cps_bn": se_cps, "se_acs_targets_bn": se_acs,
            "se_native_joint_change_bn": sdr(native_delta),
            "se_item16_bn": sdr(item16), "se_item17_bn": sdr(item17),
            "item16_item17_covariance_bn2": covariance(item16, item17),
            "native_account_covariance_bn2": covariance(without_native, native_delta),
            "se_pes_independent_bn": pi, "se_pes_feasible_min_bn": pl, "se_pes_feasible_max_bn": pu,
            "se_cps_acs_pes_independent_bn": independent, "se_cps_acs_pes_correlated_bn": correlated,
            "ci95_low_bn": point-1.96*independent, "ci95_high_bn": point+1.96*independent,
            "ci95_pes_correlated_low_bn": point-1.96*correlated, "ci95_pes_correlated_high_bn": point+1.96*correlated,
            "gradient_common_nce_bn": float(gradient[0]), "gradient_owner_bn": float(gradient[1]), "gradient_renter_bn": float(gradient[2]),
            "se_item21_pooled_ratio_bn": float(np.sqrt(np.array(ratio_gradients[reading]) @ np.array(pooled["covariance"]) @ np.array(ratio_gradients[reading]))),
            "transported_key_shapes": len(notes)})
        vectors[str(spec)] = (conditional-conditional[0]).tolist()
        acs_vectors[str(spec)] = (acs-acs[0]).tolist()
        item_vectors[str(spec)] = {"item16_bn": item16.tolist(), "item17_conditional_on16_bn": item17.tolist(),
            "coverage_repricing_bn": coverage_repricing.tolist(), "completion_repricing_bn": completion_repricing.tolist(),
            "coverage_final_bn": coverage_source[str(spec)]["replicates_bn"],
            "item21_engine_repricing_bn": item21_engine.tolist()}
        if notes:
            transport.append({"spec": spec, "notes": sorted(notes)})
    peak = require_within_budget("oct16 shared CPS/ACS/PES signed-driver evaluation")
    require(all(digest(ROOT/name) == value for name, value in source_sha256.items()),
            "source changed during signed-driver evaluation")
    output = {"basis": basis, "rows": rows, "cps_deviations_bn": vectors, "acs_target_changes_bn": acs_vectors,
        "item_replicates": item_vectors,
        "item21_pooled_ratio_gradients": ratio_gradients, "item21_new_donor_gradients": donor_gradients,
        "joint_meps_payer_covariance": donor_covariance,
        "transport": transport, "pes_axes": ["common_nce", "owner", "renter"], "pes_marginal_se_fraction": errors.tolist(),
        "pes_covariance_search": {"searched": ["pinned Census PES report Table C/D", "count lane tenure_rates", "coverage source_tables"],
            "result": "No joint covariance matrix published in these inputs. Independent diagonal and PSD-feasible marginal-SE-only envelopes are conditional alternatives. Age/sex shape covariance is unidentified."},
        "scope": "conditional source-driver sampling only; no joint total SE. Fixed national masses, driver-price coefficients, original descendant count/rule and unlocated residual. Interior line amounts are own-spec; changed key shapes retain delivered endpoint shapes. MEPS donor, school translator and production-parameter errors are separate and excluded here.",
        "source_sha256": source_sha256, "support_sha256": support_hashes(data), "count_vintage": "oct15_final_routing",
        "elapsed_diagnostic_seconds": round(time.perf_counter()-start, 3)}
    # Timing is diagnostic stdout only, so replays preserve bytes.
    elapsed = output.pop("elapsed_diagnostic_seconds")
    write(OUT/f"sampling_{basis}.json", output)
    pd.DataFrame(rows).to_csv(OUT/f"kernel_diagnostics_{basis}.csv", index=False, lineterminator="\n")
    print(f"PASS {basis} 32 own-spec principal values and conditional CPS/ACS/PES blocks; {elapsed:.3f}s; physical {peak/1e9:.3f}GB", flush=True)


def passthrough_replicates(meta, reading):
    """The unidentified beside-only source19 must never enter this central run."""
    selected = {q["id"] for q in meta["items"] if q.get("applied")}
    require("passthrough_source_tax" not in selected, "beside-only19 selected in central uncertainty estimator")
    return np.zeros(161)


def retained_scalar(scalars, spec, coordinates):
    """Preserve raw specification identity when effective-rate points coincide."""
    require("spec" in scalars and len(scalars) == 32 and set(scalars.spec) == set(range(32)),
            "retained account needs all32 unique specification IDs")
    principal = scalars.loc[scalars.spec.eq(spec)]
    require(len(principal) == 1, "nonunique retained account specification")
    scalar = principal.iloc[0]
    require(scalar.normalization == coordinates["normalization"]
            and scalar.medicaid_key == coordinates["uc"]
            and scalar.justice_key == coordinates["justice"]
            and np.isclose(scalar.school_share, coordinates["share"], rtol=0, atol=1e-12)
            and np.isclose(scalar.school_response, coordinates["school"], rtol=0, atol=1e-12)
            and np.isclose(scalar.general_government_response, coordinates["gg"], rtol=0, atol=1e-12),
            "retained account specification coordinates differ")
    return scalar


def assemble():
    sources = load_sources()
    principal_summary = json.loads((FISCAL/"main_case_2026_10_16/derived/summary.json").read_text())
    result = {"case": "oct16", "sets": {},
              "status": "[CONDITIONAL APPROXIMATION] assembled account estimator; not an unconditional total uncertainty bound",
              "source_sha256": sources["source_sha256"], "claims": {}}
    result["lineage_companions"] = {k: v for k, v in principal_summary["v9"]["companions"].items() if k.startswith("lineage_")}
    result["lineage_rule"] = "Authoritative whole-case count/C3 alternatives beside conditional sampling; neither 95% intervals nor covariance envelopes and not added as independent generation SEs."
    all_rows = []
    for basis in ("set", "cash"):
        data = json.loads((OUT/f"sampling_{basis}.json").read_text())
        core = json.loads((OUT/f"core_{basis}/account_replicates.json").read_text())
        source_rows = sources["sets"][basis]["rows"]
        scalars = pd.read_csv(OUT/f"core_{basis}/case_uncertainty.csv").query("case == 'oct16'")
        require(len(scalars) == 32, "retained account does not cover all32 specifications")
        covariance_meps = np.asarray(data["joint_meps_payer_covariance"])
        old_covariance = np.asarray(core["meps_payer_covariance"])
        n_old = len(old_covariance)
        require(np.allclose(covariance_meps[:n_old, :n_old], old_covariance, rtol=1e-10, atol=1e-12),
                "new joint MEPS covariance does not preserve the retained payer block")
        rows, complete_vectors = [], {}
        for record in data["rows"]:
            row = dict(record)
            spec, reading = row["spec"], row["reading"]
            coordinates = source_rows[spec]["coordinates"]
            scalar = retained_scalar(scalars, spec, coordinates)
            require(abs(scalar.net_cost_bn-row["net_cost_bn"]) < 1e-9, "account/full source point differs")
            raw = core["specifications"][str(spec)]
            item = data["item_replicates"][str(spec)]
            def deviation(name):
                v = np.asarray(item[name])
                return v-v[0]
            retained = np.asarray(raw["cps_cost_deviation_bn"])
            delta = (np.asarray(raw["new_engine_cost_deviation_bn"])
                -np.asarray(raw["coverage_cost_deviation_bn"])+deviation("coverage_final_bn")
                +deviation("completion_repricing_bn")+deviation("item21_engine_repricing_bn")
                +deviation("item16_bn")+deviation("item17_conditional_on16_bn")
                +passthrough_replicates(sources["sets"][basis]["meta"], reading))
            complete = retained+delta
            require(complete.shape == (161,) and abs(complete[0]) < 1e-12, "shared CPS vector IDs/central deviation")
            meps_gradient = np.r_[-np.asarray(raw["meps_welfare_gradient"]), data["item21_new_donor_gradients"][reading]]
            require(covariance_meps.shape == (len(meps_gradient), len(meps_gradient)), "joint donor gradient shape")
            meps_variance = float(meps_gradient@covariance_meps@meps_gradient)
            require(meps_variance >= -1e-10, "negative joint MEPS monetary variance")
            se_meps = float(np.sqrt(max(0., meps_variance)))
            se_cps = sdr(complete)
            se_acs, se_ratio = row["se_acs_targets_bn"], row["se_item21_pooled_ratio_bn"]
            se_school, se_production = float(scalar.se_school_correction_bn), float(scalar.se_production_term_bn)
            nuisance = se_acs**2+se_ratio**2+se_meps**2+se_school**2+se_production**2
            independent = float(np.sqrt(se_cps**2+nuisance+row["se_pes_independent_bn"]**2))
            correlated = float(np.sqrt(se_cps**2+nuisance+row["se_pes_feasible_max_bn"]**2))
            # The school upper is a source-specific unknown-covariance bound.
            core_upper = float(scalar.se_all_positive_correlation_bn-scalar.se_cps_fiscal_keys_bn
                               -scalar.se_meps_donor_bn-scalar.se_production_term_bn-scalar.se_coverage_pes_bn)
            require(core_upper >= 0, "negative retained school covariance upper")
            positive = se_cps+se_acs+se_ratio+se_meps+core_upper+se_production+row["se_pes_feasible_max_bn"]
            point = row["net_cost_bn"]
            row.update(allocation="personal", se_cps_retained_source_stacks_bn=sdr(retained), se_cps_v9_delta_bn=sdr(delta),
                retained_delta_covariance_bn2=covariance(retained, delta),
                se_cps_fiscal_keys_bn=se_cps, se_meps_donor_bn=se_meps, se_school_correction_bn=se_school,
                se_production_term_bn=se_production, se_combined_independent_bn=independent,
                se_pes_correlated_bn=correlated, se_all_positive_correlation_bn=positive,
                ci95_low_bn=point-1.96*independent, ci95_high_bn=point+1.96*independent,
                ci95_pes_correlated_low_bn=point-1.96*correlated, ci95_pes_correlated_high_bn=point+1.96*correlated,
                ci95_envelope_low_bn=point-1.96*positive, ci95_envelope_high_bn=point+1.96*positive)
            rows.append(row)
            complete_vectors[str(spec)] = {"complete_cps_deviation_bn": complete.tolist(),
                "v9_delta_bn": delta.tolist(), "joint_meps_cost_gradient": meps_gradient.tolist()}
        def owner(field, which):
            v = which(r[field] for r in rows)
            return {"value_bn": v, "specifications": [r["spec"] for r in rows if abs(r[field]-v) < 1e-10]}
        scope = ("Measured account/benefit/job/K2/completion/mixed-unit CPS source stacks retained and joined before SDR; "
            "13/14/15/18/20 source repricing,16/17 native161,80 joint ACS target fiscal changes;19 excluded by central meta.items, "
            "21 own raw-driver fiscal blocks and pooled OFD/STL ratio covariance. MEPS2024 cross-payer covariance retained. "
            "Different surveys/production/school blocks combined as if independent; pooled ratios include2024 MEPS, so donor-ratio covariance is unidentified. "
            "The school correction also overlaps CPS inputs; its covariance with the joint account block is not identified here. "
            "Other payers' pooled ethnic-translation ratios remain fixed; their translator sampling is not fully measured by this item21 calculation. "
            "Item21 keeps its source white unit-band payer amounts and fee offsets fixed. "
            "PES axes have no published covariance; feasible-correlated alternative holds other block independences. "
            "Interior changed-key shapes and source10/11 endpoint stacks are disclosed conditional transports; not own-key U06. "
            "Fixed original descendant count/rules, national source masses, unlocated residuals and source policy parameters. "
            "No unconditional total bound, complete count-model uncertainty, or causal confidence interval.")
        result["sets"][basis] = {"point_low": owner("net_cost_bn", min), "point_high": owner("net_cost_bn", max),
            "independent_low": owner("ci95_low_bn", min), "independent_high": owner("ci95_high_bn", max),
            "pes_correlated_low": owner("ci95_pes_correlated_low_bn", min), "pes_correlated_high": owner("ci95_pes_correlated_high_bn", max),
            "positive_correlation_low": owner("ci95_envelope_low_bn", min), "positive_correlation_high": owner("ci95_envelope_high_bn", max),
            "specifications": len(rows), "scope": scope, "pes_covariance_search": data["pes_covariance_search"],
            "range_se_cps_bn": [min(r["se_cps_fiscal_keys_bn"] for r in rows), max(r["se_cps_fiscal_keys_bn"] for r in rows)],
            "range_se_acs_bn": [min(r["se_acs_targets_bn"] for r in rows), max(r["se_acs_targets_bn"] for r in rows)],
            "range_se_meps_bn": [min(r["se_meps_donor_bn"] for r in rows), max(r["se_meps_donor_bn"] for r in rows)]}
        result["sets"][basis]["specification_span_bn"] = max(r["net_cost_bn"] for r in rows)-min(r["net_cost_bn"] for r in rows)
        result["sets"][basis]["within_spec_conditional_95_width_bn"] = [min(3.92*r["se_combined_independent_bn"] for r in rows), max(3.92*r["se_combined_independent_bn"] for r in rows)]
        pd.DataFrame(rows).to_csv(OUT/f"case_uncertainty_{basis}.csv", index=False, lineterminator="\n")
        all_rows.extend(rows)
        write(OUT/f"assembled_vectors_{basis}.json", complete_vectors)
    result["claims"] = {"U1_U2": "Conditional intervals, PES covariance envelopes and lineage arms are different objects.",
        "U4": "Item21 own pooled OFD/STL ratio influences and full10-cell covariance enter monetary gradients. Other payer translators remain fixed, and same-source donor-ratio covariance is unidentified; U4 is only partly resolved.",
        "U6": "All32 point/independent/PES-feasible/global-correlation interval owners searched in both sets. Own-key U06 remains unresolved for disclosed transported source shapes.",
        "U7": "Common NCE plus owner/renter gradients evaluated through fixed-count tenure; full PES age/sex covariance unidentified.",
        "U8": "Cash has a separately repriced assembled conditional interval with all32 owner search; not a complete unconditional cash uncertainty bound."}
    pd.DataFrame(all_rows).to_csv(OUT/"case_uncertainty.csv", index=False, lineterminator="\n")
    write(OUT/"summary.json", result)
    print("PASS assembled oct16 conditional estimator and all32 interval-owner searches, both sets")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=("prepare", "coverage_set", "coverage_cash", "set", "cash", "assemble"))
    parser.add_argument("--require-own", action="store_true")
    args = parser.parse_args()
    if args.stage == "prepare":
        prepare()
    elif args.stage in ("coverage_set", "coverage_cash"):
        source_coverage(args.stage.removeprefix("coverage_"))
    elif args.stage in ("set", "cash"):
        calculate(args.stage, args.require_own)
    elif args.stage == "assemble":
        assemble()
    else:
        subprocess.run([sys.executable, str(HERE/"pooled21.py")], check=True)
        subprocess.run([sys.executable, str(HERE/"account_core.py")], check=True)
        for stage in ("prepare", "coverage_set", "set", "coverage_cash", "cash", "assemble"):
            subprocess.run([sys.executable, str(Path(__file__)), "--stage", stage]+(["--require-own"] if args.require_own else []), check=True)


if __name__ == "__main__":
    main()
