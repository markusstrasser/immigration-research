"""Beside-only origin coverage and fixed-G2-price screens; never case items.

Native-First: use linked-child PRDTHSP cells and the same coverage price cache.
Adults' origin is unobserved: any child-to-adult transport is named separately.
"""
import gc
import json
from pathlib import Path
import resource
import sys
import time

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
from measure import CASE, COVER, GENS, OUT, write_csv, write_json
from tenure import C, load, require


def origin_fraction(table, parent_arm, gen, band, sex):
    cell = table[(table.parent_arm == parent_arm) & (table.generation == gen)
                 & (table.age_band == band) & (table.sex == sex)]
    def value(name):
        selected = cell.loc[cell.origin == name, "persons"]
        require(len(selected) == 1, "missing/duplicate linked origin cell")
        return float(selected.iloc[0])
    denominator = value("all_nonMexican")
    numerator = value("other_Hispanic")
    return (numerator/denominator if denominator else 0.0), denominator


def age_band(age):
    return "0-4" if age < 5 else "5-9" if age < 10 else "10-14" if age < 15 else "15-17"


def main():
    start = time.perf_counter()
    table = pd.read_csv(OUT / "linked_origin_age_sex.csv")
    lookup = {(parent, gen, band, sex): origin_fraction(table, parent, gen, band, sex)
              for parent in ("all_parent_types", "biological") for gen in ("G3", "G4plus")
              for band in ("0-17", "0-4", "5-9", "10-14", "15-17") for sex in (1, 2)}
    lineage = json.loads((CASE / "corrections.json").read_text())["meta"]["lineage"]
    rates, base = load()
    results = {}
    for basis in ("set", "cash"):
        audit = json.loads((COVER / f"derived/pricing_audit_oct15_final_routing_{basis}.json").read_text())
        C.validate_cache_receipt(audit, COVER / f"inputs/pricing_dependencies_oct15_final_routing_{basis}.json",
                                 COVER / f"_cache/oct15_final_routing/{basis}/pricing.npz")
        with np.load(COVER / f"_cache/oct15_final_routing/{basis}/pricing.npz") as archive:
            data = {k: archive[k] for k in ("age", "sex", "generation", "arrival", "hispanic", "added_weights")}
            prices = archive["net_added"][:, :, 0].copy()-archive["excluded_use_prices"][:, :, 0]
        # Synthetic latent descendants inherit native arrival and Hispanic-report
        # coverage only in this explicit beside construction.
        hypothetical = {**data, "hispanic": np.ones(len(data["age"]), bool),
                         "generation": np.full(len(data["age"]), 2), "arrival": np.zeros(len(data["age"]), int)}
        factors, _ = C.factors(hypothetical, rates, base)
        weights = data["added_weights"][:, 0]
        original_g3 = data["generation"] == 2
        # The aggregate descendant stock is on original G3 proxy records;
        # completion's observed nonreporters are separate actual records.
        payload = json.loads((CASE / f"corrections{'_cash' if basis == 'cash' else ''}.json").read_text())
        ids = {(int(x["PH_SEQ"]), int(x["PPPOS"])) for x in payload["meta"]["union_completion"]["observed_records"]}
        with np.load(COVER / f"_cache/oct15_final_routing/{basis}/pricing.npz") as archive:
            is_completion = np.array([(int(h), int(p)) in ids for h, p in zip(archive["person_ph_seq"], archive["person_pppos"])])
        latent = original_g3 & ~is_completion
        by_arm = {}
        for parent in ("all_parent_types", "biological"):
            for construction in ("minor_only", "child_to_adult_transport"):
                shares = np.zeros(len(weights))
                unsupported_weight = 0.0
                for i in np.flatnonzero(latent):
                    age, sex = int(data["age"][i]), int(data["sex"][i])
                    if age >= 18 and construction == "minor_only":
                        continue
                    band = age_band(age) if age < 18 else "0-17"
                    g3, n3 = lookup[parent, "G3", band, sex]
                    g4, n4 = lookup[parent, "G4plus", band, sex]
                    if n3 == 0 or n4 == 0:
                        unsupported_weight += weights[i]
                    k = min(age//5, 16)
                    a = lineage["counts"]["at_g3_rate"]*lineage["age_mix"]["mixes"]["g3_rate"][k]
                    b = lineage["counts"]["later_losses"]*lineage["age_mix"]["mixes"]["later"][k]
                    shares[i] = (a*g3+b*g4)/(a+b)
                costs = prices @ (weights*factors*shares)
                by_arm[f"{parent}_{construction}"] = dict(
                    coverage_increment_bn=dict(zip(("low", "high"), map(float, costs))),
                    net_missing_people=float(weights @ (factors*shares)),
                    supported_latent_base_people=float(weights @ shares),
                    zero_denominator_proxy_people=unsupported_weight,
                    status="conditional beside only; not in items16/17",
                    adult_rule="none: adults withheld" if construction == "minor_only" else "UNVERIFIED transfer of same-sex linked-child pooled fractions to latent adults",
                    price_rule="existing blended latent profile; G3/G4 origin fractions blended by case age-specific descendant count parts")
        observed = is_completion & data["hispanic"]
        by_arm["observed_completion_nonreporter_hispanic"] = dict(
            coverage_increment_bn=dict(zip(("low", "high"), map(float, prices @ (weights*factors*observed)))),
            net_missing_people=float(weights @ (factors*observed)),
            status="beside: observed origin in item10 nonreporter records, own existing case prices")
        results[basis] = by_arm
        del data, hypothetical, prices
        gc.collect()
    # Reproduce the verifier's deliberately fixed-price, outside-CA/TX screen.
    cells = pd.read_csv(OUT / "native_household_cells.csv")
    screens = {}
    for basis in ("set", "cash"):
        prices = pd.read_csv(COVER / f"derived/age_prices_oct15_final_routing_{basis}.csv")
        screens[basis] = {}
        for end in ("low", "high"):
            p = prices[(prices.end == end) & (prices.generation == "G2")].set_index("age_band_march2025")
            value = 0.0
            for band in ("0-4", "5-9", "10-14", "15-17"):
                delta = cells[(cells.region == "outside_CA_TX") & (cells.age_band == band) & (cells.kind == "mexican")].difference
                require(len(delta) == 1, "fixed-price screen age cell")
                key = "15-19" if band == "15-17" else band
                value -= float(delta.iloc[0])*float(p.loc[key, "per_member_usd"])/1e9
            screens[basis][end] = value
    require(abs(screens["set"]["low"]+6.743981524) < 1e-8, "verifier fixed-price low control")
    require(abs(screens["set"]["high"]+7.268651923) < 1e-8, "verifier fixed-price high control")
    write_json(OUT / "origin_diagnostic.json", dict(sets=results, fixed_G2_price_screen_bn=screens,
        central_items_include_origin_diagnostic=False,
        text_correction="Non-Mexican reporters are not necessarily non-Hispanic; PRDTHSP distinguishes both. Linked native children falsify the categorical premise. Their origin fractions do not identify latent adults' origin.",
        limitations=["No latent adult origin data; no joint latent-stock re-estimation.",
                     "Child age-sex origin cells can be sparse; zero denominator cells explicitly expose unsupported proxy mass.",
                     "Minor-only coverage is a modeled transfer to latent minors, not directly observed omitted persons."]))
    print(json.dumps(dict(fixed_price_screen=screens, origin_coverage=results), indent=2))
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform != "darwin":
        peak *= 1024
    require(peak < 2_500_000_000, "diagnostic peak RSS exceeds 2.5GB")
    print(f"PASS {time.perf_counter()-start:.3f}s peakRSS {peak/1e6:.1f}MB")


if __name__ == "__main__":
    main()
