"""Principal-source checks on completed members and the unobserved coverage block."""
import json
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent


def test_observed_adult_target_excludes_principal_missing_people():
    for suffix in ("", "_cash"):
        lines = json.loads((HERE / f"_cache/oct15/lines{suffix}.json").read_text())
        coverage = lines["meta"]["coverage"]
        principal = json.loads((HERE.parent / coverage["file"]).read_text())
        source = principal["sets"][coverage["which"]]["scenarios"][coverage["construction"]]
        lineage = lines["meta"]["lineage"]
        full, observed = lineage["complete_generation_g3plus"], lineage["generation_g3plus"]
        assert abs(full["adults"]-observed["adults"]-source["adults_by_generation"]["G3plus"]) < 1e-6
        assert abs(full["population"]-observed["population"]-source["implied_net_missing_people"]["G3plus"]) < 1e-6
        assert observed["coverage_excluded"]["sha256"] == coverage["sha256"]


def test_completed_people_enter_their_own_observed_households():
    lines = json.loads((HERE / "_cache/oct15/lines.json").read_text())
    records = lines["meta"]["union_completion"]["observed_records"]
    household = pd.read_parquet(HERE / "_cache/oct15/households.parquet")
    assert {r["PH_SEQ"] for r in records} <= set(household.PH_SEQ)
    assert sum(r["observed_nonreporter"] for r in records) == 27
    assert sum(not r["observed_nonreporter"] for r in records) == 204
    population = float((household.union_members * household.weight).sum())
    assert abs(population - lines["meta"]["population_v8"]["without_coverage"]) < 1


def test_coverage_has_no_observed_household_and_reconciles_by_generation():
    lines = json.loads((HERE / "_cache/oct15/lines.json").read_text())
    coverage = lines["meta"]["coverage"]
    block = pd.read_csv(HERE / "derived/oct15/people_survey_misses.csv")
    assert not block.observed_household.any()
    assert "PH_SEQ" not in block
    for end in ("low", "high"):
        rows = block[block.end == end]
        assert abs(rows.cost_bn.sum() - coverage["by_end"][end]["total_bn"]) < 1e-4
        for generation, amount in coverage["by_end"][end]["by_generation"].items():
            assert abs(rows[rows.generation == generation].cost_bn.sum() - amount) < 1e-4
    assert abs(block[block.end == "low"].net_missing_people.sum() - coverage["net_missing_people"]) < 1e-4


def test_household_cost_excludes_the_unobserved_coverage_block():
    lines = json.loads((HERE / "_cache/oct15/lines.json").read_text())
    control = pd.read_csv(HERE / "derived/oct15/control.csv").set_index(["end", "item"])
    for end in ("low", "high"):
        # The conservation control sums actual person weights within each household.
        # Average household weights serve ranks/quantiles; ages' lineage factors differ within households.
        amount = control.loc[(end, "households_sum"), "bn"]
        remainder = control.loc[end].query("assigned == False").bn.sum()
        assert abs(amount + remainder - lines["union"][end]["cost_bn"]) < 1e-5
        missing = control.loc[end].loc[[f"people_survey_misses_{g}" for g in ("G1", "G2", "G3plus")]]
        assert not missing.assigned.any()
        assert abs(missing.bn.sum()-lines["meta"]["coverage"]["by_end"][end]["total_bn"]) < 2e-6
