"""Recover the full-frame driver of an actual household pricing piece.

This read-only adapter follows households.py's line_split/routed_split and capital
parents. It changes no engine amount: pension receipt coefficients and production
cell attribution remain those of the exported case. A recovered driver is not a
claim to have rerun the engine's national fiscal account.
"""
from __future__ import annotations

import csv
import json
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
    native = p.get("native_child_source")
    state_source = p.get("state_price_source")
    population = "nonreporter" if native is not None or (state_source and state_source["population"] == "native") else p.get("observed_population")
    if population is not None:
        require(population in ("reporter", "nonreporter"), "unknown observed completion population")
        mask = np.asarray(s[population], dtype=bool)
    elif p["id"] == "mixed_unit_removal":
        mask = np.asarray(s["gens"][p["g"]], dtype=bool)
    else:
        mask = np.asarray(s.get("original_gens", s["gens"])[p["g"]], dtype=bool)
    require(mask.shape == (n,), "generation mask shape")
    own_mask = mask[rows]
    x = np.asarray(p["x"], dtype=float)
    require(x.shape == rows.shape and np.isfinite(x).all() and np.all(x >= 0), "invalid priced vector " + p["id"])
    require(np.all(x[~own_mask] == 0), "piece leaks outside its generation " + p["id"])
    full_G = s["lines"]["generations"][p["g"]][end]
    G = full_G.get("before_native_children") or full_G
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
            candidates = canonical("spending", row["key"]) if s["lines"]["meta"].get("basis") == "cash" else pension("oasdi")
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

    completion = p.get("completion_source")
    declared_mass = None
    if state_source is not None:
        matches = [part for part in full_G.get("added_state_prices", []) if all(state_source.get(k) == part.get(k)
                    for k in ("source_cell", "edit", "charge_source", "rule", "indexes_source"))]
        require(len(matches) == 1, "no unique principal added-state declaration")
        part = matches[0]
        subgroup = state_source["population"]
        require(subgroup in ("identified", "latent", "native"), "unknown added-state population")
        side, lid, selected = state_source["source_cell"].split("|")
        parent = row_of(side, lid)
        require((parent["scenario"] if side == "receipt" else parent["key"]) == selected
                and parent["key"] == state_source["key"], "added-state selected source cell mismatch")
        require(state_source["category"] == p["cat"] and np.isfinite(state_source["category_share"]),
                "added-state source category declaration mismatch")
        expected_share = 1.0
        if subgroup != "native" and side == "spending" and lid == "public_order_safety":
            j = ("G1", "G2", "G3plus").index(p["g"])
            use = s["use_parts"]
            per_head = use["per_head"][j]*s["per_head_factor"][j]
            by_use = sum(use[k][j] for k in ("custody", "arrest_like_custody", "ice_interior"))
            require(p["cat"] in ("justice_per_head", "justice_use"), "unknown added-state justice category")
            expected_share = (per_head if p["cat"] == "justice_per_head" else by_use)/(per_head+by_use)
        elif subgroup != "native" and side == "spending" and lid == "education_services":
            require(p["cat"] in ("schools", "education_other"), "unknown added-state education category")
            school, other = canonical(side, "school_part")[0][0], canonical(side, "P_part")[0][0]
            full_weights = np.asarray(s["W"])[:, 0]*mask
            expected_share = float((school if p["cat"] == "schools" else other) @ full_weights)/float((school+other) @ full_weights)
        require(abs(state_source["category_share"]-expected_share) < 1e-12, "added-state source category share mismatch")
        require(abs(p["bn"]-part["cost_by_population"][subgroup]*expected_share) < 1e-12,
                "added-state population cost differs from principal")
        if subgroup in ("identified", "latent"):
            original_g3 = np.asarray(s.get("original_gens", s["gens"])["G3plus"], dtype=bool)
            require(original_g3.shape == (n,), "added-state original G3 mask shape")
            fraction = np.ones(n)
            fraction[original_g3] = 1/np.asarray(s["f_rec"])[original_g3]
            if subgroup == "latent":
                fraction = 1-fraction
            require(np.isfinite(fraction).all() and np.all((fraction >= 0) & (fraction <= 1)),
                    "added-state actual identified/latent population fraction")
            choices = [(candidate*fraction, source) for candidate, source in line_candidates(parent, routed=False)]
            matching = [(candidate, source) for candidate, source in choices if _same(candidate, np.asarray(p["full_driver"]))]
            require(matching and all(_same(matching[0][0], candidate) for candidate, _ in matching),
                    "added-state full driver differs from principal source category")
            expected = matching[0][0]
        else:
            expected = np.zeros(n)
            identities = s["identities"]
            require(len(identities) == n, "added-state native identity is not unique")
            for record in s["lines"]["meta"]["child_pricing"]["records"]:
                index = identities[(record["PH_SEQ"], record["PPPOS"])]
                require(mask[index], "added-state native source outside observed child records")
                values = [row for row in record["ends"][end]["rows"] if row["side"] == side and row["id"] == lid]
                require(len(values) == 1 and (values[0]["scenario"] if side == "receipt" else values[0]["key"]) == selected,
                        "added-state native principal source mismatch")
                expected[index] = values[0]["amount_bn"]
        require(_same(np.asarray(p["full_driver"]), expected), "added-state full driver differs from principal source")
        matched_source = ("; driver: " + " | ".join(dict.fromkeys(source for _, source in matching))) if subgroup != "native" else ""
        candidates = [(expected, "principal added-state " + subgroup + ":" + state_source["source_cell"] + matched_source)]
    elif native is not None:
        kind, parent = native["kind"], native["parent"]
        require(kind in ("rows", "capital", "production"), "unknown native-child component")
        identities = s.get("identities")
        if identities is None:
            identities = {(int(h), int(pos)): i for i, (h, pos) in enumerate(zip(s["d"].PH_SEQ, s["d"].PPPOS, strict=True))}
        require(len(identities) == n, "native-child record identity is not unique")
        expected = np.zeros(n)
        for record in s["lines"]["meta"]["child_pricing"]["records"]:
            identity = (record["PH_SEQ"], record["PPPOS"])
            require(identity in identities and mask[identities[identity]], "native-child source outside observed child records")
            block = record["ends"][end]
            if kind == "production":
                require(parent == "production", "unknown native production parent")
                value = block["production_bn"]
            else:
                values = [r for r in block[kind] if r["id"] == parent and (kind != "rows" or r["side"] == native["side"])]
                require(len(values) == 1, "no unique native-child declared component")
                if kind == "rows":
                    require(values[0]["key"] == native["key"], "native-child selected source key mismatch")
                value = values[0]["cost_bn"]
                if kind == "rows" and parent == "education_services":
                    categories = values[0].get("category_cost_bn")
                    require(isinstance(categories, dict) and set(categories) == {"schools", "education_other"},
                            "missing native-child principal education category amounts")
                    require(all(np.isfinite(v) for v in categories.values())
                            and abs(sum(categories.values()) - value) < 1e-12,
                            "native-child education category cost closure")
                    require(native.get("category") in categories and native["category"] == p["cat"],
                            "native-child education category declaration mismatch")
                    value = categories[native["category"]]
                if kind == "rows" and parent == "medicare" and s["lines"]["meta"].get("basis") != "cash":
                    value = block["part_a_accrual_cost_bn"] if p["cat"] == "pension_accrual" else value-block["part_a_accrual_cost_bn"]
            sign = 1 if p["bn"] > 0 else -1
            expected[identities[identity]] = abs(value) if sign*value > 0 else 0
        require(_same(np.asarray(p["full_driver"]), expected), "native-child driver differs from principal own-age prices")
        candidates = [(expected, "native-child principal observed own-age " + kind + ":" + parent)]
    elif p["id"] == "mixed_unit_removal":
        require(p.get("distribution_assumption") == "declared generation total per member; no observed household split",
                "undeclared mixed-unit distribution")
        candidates = [(np.ones(n), "mixed_unit_removal declared per-member generation allocation")]
    elif completion is not None:
        declared = s["lines"]["meta"]["union_completion"]["carriers"]
        require(p["id"] in declared, "undeclared completion carrier")
        require(completion == declared[p["id"]], "changed completion source declaration")
        kind = completion["kind"]
        if kind == "line":
            parent = completion["parent_line"]
            if parent in ("corporate_capital", "corporate_labor", "remaining_production_property", "other_production_taxes"):
                key = {"corporate_capital": "corporate", "corporate_labor": "corporate",
                       "remaining_production_property": "business_property"}.get(parent, parent)
                candidates = [(s["completion_jobs"][key], "completion own-job principal source receipts " + key)]
                declared_mass = s["completion_national_mass"][key]
                require(np.isfinite(declared_mass) and declared_mass > 0, "invalid own-job principal national driver mass")
            elif parent == "tenant_occupied_property":
                path = Path(__file__).resolve().parents[1] / "union_completion_2026_10_14/derived/added_band_prices.json"
                rates = json.loads(path.read_text())
                which = s["lines"]["meta"]["basis"]
                index = ("low", "high").index(end)
                profile = np.array([r["g3_fallback_line_bn_per_person"][parent][which][index] for r in rates["rates"]])
                require(profile.shape == (17,) and np.isfinite(profile).all(), "invalid principal tenant age-price profile")
                driver = np.abs(profile)[np.minimum(age // 5, 16)]
                candidates = [(driver, "completion declared tenant G3 age-price proxy; fixed full-frame proxy mass")]
            elif parent == "lane_constants":
                candidates = [(np.ones(n), "completion declared lane constants per head")]
            elif parent in ("social_security", "medicare") and p["cat"] == "pension_accrual" and s["lines"]["meta"]["basis"] == "set":
                part = "oasdi" if parent == "social_security" else "part_a"
                candidates = [(s["completion_pension"]["person"][part][allocation], "completion declared person-pension profile " + part)]
            else:
                candidates = line_candidates(row_of(completion["side"], parent))
        elif kind == "production":
            candidates = [(np.asarray(s["prod_parts"][end]["earn"]), "completion declared production earnings")]
        elif kind == "capital":
            parent_piece = dict(p, id=completion["parent_line"], cat="capital")
            parent_piece.pop("completion_source")
            parent_piece.pop("observed_population")
            # Recover the declared capital parent's extension using the baseline restriction.
            parent_piece["x"] = np.where(s["original_gens"][p["g"]][rows], p["full_driver"][rows], 0.0)
            parent, source, override = full_key(s, parent_piece, end)
            candidates = [(parent, "completion capital via " + source)]
            require(override is None, "completion capital national-mass override needs an explicit route")
        elif kind == "nonreporters":
            require(population == "nonreporter", "nonreporter carrier assigned to wrong population")
            driver = np.asarray(p["full_driver"])
            require(np.all(driver[~mask] == 0), "nonreporter price driver leaks outside its observed records")
            candidates = [(driver, "completion observed nonreporter band/economic-class net-price driver")]
        else:
            require(False, "unknown completion driver kind " + str(kind))
    elif p["cat"] == "production":
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
    national_mass = declared_mass
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
