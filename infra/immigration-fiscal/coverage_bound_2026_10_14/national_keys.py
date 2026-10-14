"""Recover the full-frame driver of an actual household pricing piece.

This read-only adapter follows households.py's line_split/routed_split and capital
parents. It changes no engine amount: pension receipt coefficients and production
cell attribution remain those of the exported case. A recovered driver is not a
claim to have rerun the engine's national fiscal account.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np


def require(ok, message):
    if not ok:
        raise SystemExit("[BLOCKED] national piece driver: " + message)


def _same(x, y):
    """Pointwise relative tolerance, with exact agreement at structural zeroes."""
    return x.shape == y.shape and np.all(np.abs(x - y) <= 1e-12 * np.maximum(np.abs(x), np.abs(y)))


def full_key(snapshot, piece, end):
    """Return (full driver, source/method, national-mass override) or stop.

    Piece x is already masked to its generation on rows_u. Candidate drivers are
    confined to its declared line, route or capital parent; coincident values on
    one generation cannot authorize using an unrelated national key. Identical
    full extensions may have several legitimate source names.
    """
    s, p = snapshot, piece
    n = len(s["d"])
    rows = np.asarray(s["rows_u"])
    require(rows.ndim == 1 and np.issubdtype(rows.dtype, np.integer), "invalid union row indices")
    require(len(np.unique(rows)) == len(rows) and np.all((rows >= 0) & (rows < n)), "duplicate/out-of-frame union rows")
    require(p["g"] in s["gens"], "unknown generation " + str(p["g"]))
    mask = np.asarray(s["gens"][p["g"]], dtype=bool)
    require(mask.shape == (n,), "generation mask shape")
    own_mask = mask[rows]
    x = np.asarray(p["x"], dtype=float)
    require(x.shape == rows.shape and np.isfinite(x).all() and np.all(x >= 0), "invalid priced vector " + p["id"])
    require(np.all(x[~own_mask] == 0), "piece leaks outside its generation " + p["id"])
    G = s["lines"]["generations"][p["g"]][end]
    allocation = G["allocation"]
    vectors = s["vec"][allocation]
    age = np.asarray(s["age"])
    require(age.shape == (n,), "age shape")
    by_id = {}
    for row in G["rows"]:
        identity = (row["side"], row["id"])
        require(identity not in by_id, "duplicate generation line " + repr(identity))
        by_id[identity] = row

    def row_of(side, lid):
        require((side, lid) in by_id, "missing declared parent " + side + ":" + lid)
        return by_id[(side, lid)]

    def canonical(side, key):
        require((side, key) in vectors, "missing canonical key " + side + ":" + key)
        return [(np.asarray(vectors[(side, key)], dtype=float), "canonical " + side + ":" + key)]

    def pension(part):
        PA = s["PA"]
        if part == "oasdi":
            terms = [(lid, 1.0) for lid in PA["oasdi_lines"]] + [(PA["se_line"], PA["se_oasdi_share"])]
        else:
            terms = [(lid, 1.0) for lid in PA["hi_lines"]] + [(PA["se_line"], 1 - PA["se_oasdi_share"])]
        weights = np.asarray(s["W"])[:, 0]
        require(weights.shape == (n,) and np.isfinite(weights).all() and np.all(weights >= 0), "invalid pension spread weights")
        driver = np.zeros(n)
        coefficients = []
        for lid, fraction in terms:
            receipt = row_of("receipt", lid)
            vector = canonical("receipt", receipt["key"])[0][0]
            denominator = float(np.where(mask, vector, 0.0) @ weights)
            require(np.isfinite(denominator) and denominator > 0, "non-positive pension receipt mass " + lid)
            coefficient = fraction * receipt["amount_bn"] / denominator
            require(np.isfinite(coefficient) and coefficient >= 0, "invalid pension receipt coefficient " + lid)
            driver += coefficient * vector
            coefficients.append(f"{lid}:{coefficient:.17g}")
        return [(driver, "receipts_of " + part + "; fixed generation receipt coefficients " + ",".join(coefficients))]

    def line_candidates(row, routed=True, seen=()):
        identity = (row["side"], row["id"])
        require(identity not in seen, "cyclic split parent " + repr(identity))
        side, lid = identity
        chain = (*seen, identity)
        if side == "spending" and lid == "public_order_safety":
            candidates = [(np.ones(n), "public_order_safety per_head"),
                          (((age >= 18) & (age <= 64)).astype(float), "public_order_safety custody ages18-64")]
            if p["cat"] == "justice_per_head":
                candidates = candidates[:1]
            elif p["cat"] == "justice_use":
                candidates = candidates[1:]
        elif side == "spending" and row["key"].startswith("uninsured_use"):
            exposure = s["d"].NOCOV_CYR.eq(3).to_numpy(float) + 0.5 * s["d"].NOCOV_CYR.eq(2).to_numpy(float)
            candidates = canonical("spending", "medicaid") + [(exposure, "uninsured person-years NOCOV_CYR3 + 0.5*NOCOV_CYR2")]
        elif side == "spending" and lid.startswith("state_price_"):
            parent = lid.removeprefix("state_price_")
            candidates = line_candidates(row_of("spending", parent), routed=False, seen=chain)
        elif side == "spending" and lid in G.get("roads", {}):
            road = G["roads"][lid]
            candidates = [((age >= 5).astype(float), "road driver miles ages5+")]
            candidates += canonical("receipt", road["freight_key"])
            candidates += canonical("spending", road["old_key"])
        elif side == "spending" and lid == "social_security":
            candidates = pension("oasdi")
        elif side == "spending" and lid == "medicare":
            candidates = pension("hi") if p["cat"] == "pension_accrual" else canonical("spending", row["key"])
        elif side == "receipt" and lid == "federal_income_tax":
            candidates = canonical("receipt", row["key"]) + canonical("spending", "social_security")
        elif side == "spending" and lid == "education_services":
            candidates = canonical("spending", "school_part") + canonical("spending", "P_part")
        elif side == "spending" and lid == "school_reprice":
            candidates = canonical("spending", "school_part")
        elif side == "spending" and lid == "college_rekey":
            candidates = canonical("spending", "P_part")
        else:
            candidates = canonical(side, row["key"])
        if routed:
            for route in s["lines"]["meta"].get("routes", []):
                if (route["side"], route["line"]) == identity:
                    for vector, source in line_candidates(row_of("spending", route["basis"]), routed=False, seen=chain):
                        candidates.append((vector, "route " + route["part"] + " via " + route["basis"] + ": " + source))
        return candidates

    if p["cat"] == "production":
        pp = s["prod_parts"][end]
        candidates = [(np.asarray(pp["earn"]) * cell, "production earnings skill-cell " + str(i))
                      for i, cell in enumerate(pp["cells"])]
    elif p["cat"] == "capital":
        capital = [c for c in G["capital"] if c["id"] == p["id"]]
        require(len(capital) == 1, "no unique capital declaration " + p["id"])
        rule = capital[0]["rule"]
        if rule["kind"] == "receipt_amount_over_national":
            carrier = s["lines"]["meta"].get("carriers", {}).get(rule["line"])
            if carrier is not None:
                candidates = line_candidates(row_of("spending", carrier["parent_line"]))
            else:
                require(rule["line"] == "enterprise_surplus", "unknown capital receipt parent " + rule["line"])
                candidates = [(np.ones(n), "enterprise_surplus capital per_head")]
        elif rule["kind"] == "part_rekeyed":
            candidates = []
            for lid in (rule["parent_line"], rule["correction_line"]):
                candidates += line_candidates(row_of("spending", lid))
        else:
            require(rule["kind"] == "lines_amount_over_national", "unknown capital rule " + rule["kind"])
            candidates = []
            for lid in rule["numerator_lines"]:
                parents = [r for r in G["rows"] if r["id"] == lid]
                require(len(parents) == 1, "ambiguous capital numerator " + lid)
                candidates += line_candidates(parents[0])
        candidates = [(vector, "capital " + p["id"] + " parent: " + source) for vector, source in candidates]
    else:
        own = [r for r in G["rows"] if r["id"] == p["id"]]
        require(len(own) == 1, "no unique priced line " + p["id"])
        candidates = line_candidates(own[0])

    matches = []
    for vector, source in candidates:
        require(vector.shape == (n,) and np.isfinite(vector).all() and np.all(vector >= 0), "invalid full candidate " + source)
        masked = np.where(own_mask, vector[rows], 0.0)
        if _same(masked, x):
            matches.append((vector, source))
    require(bool(matches), "no exact declared extension " + p["g"] + " " + end + " " + p["id"] + " " + p["cat"])
    first = matches[0][0]
    require(all(_same(first, vector) for vector, _ in matches[1:]), "ambiguous full-frame extensions " + p["id"] + ": " + " | ".join(source for _, source in matches))
    require(_same(np.where(own_mask, first[rows], 0.0), x), "masked reconstruction mismatch " + p["id"])
    source = "exact_declared_driver_1e-12_relative; " + " | ".join(dict.fromkeys(source for _, source in matches))
    national_mass = None
    tenant = vectors.get(("receipt", "renter_contract_rent"))
    if tenant is not None and _same(first, np.asarray(tenant, dtype=float)):
        # households.tenant_key spreads the group's ACS state rent only over its
        # union tenants. v4_inputs.tenant divides that sum by all states' all_rent.
        # Its zeroes outside the union are not evidence of zero outside rent.
        path = Path(__file__).resolve().parents[1] / "receipt_side_long_run_2026_09_28/derived/states.csv"
        require(path.is_file(), "missing principal national tenant-rent table")
        with path.open(newline="") as stream:
            states = list(csv.DictReader(stream))
        require(len(states) == 51 and len({r["state"] for r in states}) == 51, "incomplete/duplicate national rent states")
        group_rent = np.asarray([float(r["group_rent"]) for r in states])
        all_rent = np.asarray([float(r["all_rent"]) for r in states])
        require(np.isfinite(group_rent).all() and np.isfinite(all_rent).all()
                and np.all(group_rent >= 0) and np.all(all_rent > 0)
                and np.all(group_rent <= all_rent), "invalid national rent values")
        got = float(first @ np.asarray(s["w_id"]))
        want = float(group_rent.sum())
        require(abs(got - want) <= 1e-12 * want, "tenant driver does not conserve the principal group rent")
        national_mass = float(all_rent.sum())
        source += "; principal national mass states.csv sum(all_rent), group mass sum(group_rent)"
    return first, source, national_mass
