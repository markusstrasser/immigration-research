"""Source alignment, original benchmarks, and independent decomposition tests."""
import json
import os
from pathlib import Path

import numpy as np
import pytest
import statsmodels.api as sm

from employment import SOURCES, estimate, integer, load_api, parse_employment
from raw_finance import parse_population


@pytest.fixture(scope="module")
def originals():
    root = Path(os.environ.get("IMMIGRATION_AUDIT_DATA_ROOT", Path.cwd()))
    population, _ = parse_population(root / SOURCES["population"][0])
    states = root / SOURCES["states"][0]
    national = root / SOURCES["national"][0]
    records, checks = parse_employment(states, national, population)
    return records, checks, states, national, population


def test_duplicate_headers_must_agree(originals, tmp_path):
    _, _, states, _, _ = originals
    table = json.loads(states.read_text())
    repeated = [i for i, name in enumerate(table[0]) if name == "AGG_DESC"]
    assert len(repeated) == 2
    assert load_api(states)
    table[1][repeated[1]] = "EP_FAKE"
    bad = tmp_path / "disagree.json"
    bad.write_text(json.dumps(table))
    with pytest.raises(ValueError, match="duplicate API header disagrees"):
        load_api(bad)


def test_missing_suppressed_and_negative_values_fail():
    assert integer("0") == 0
    for value in [None, "-1", "N", "(X)", "", "1.0"]:
        with pytest.raises(ValueError):
            integer(value)


def test_nondata_api_response_is_rejected(tmp_path):
    for body in ["<html>Missing Key</html>", "{}", "[]", "[[], []]"]:
        response = tmp_path / "response.json"
        response.write_text(body)
        with pytest.raises(ValueError):
            load_api(response)


def test_original_national_benchmarks_and_state_totals(originals):
    records, checks, _, national, _ = originals
    us = {r["AGG_DESC"]: r for r in load_api(national) if r["GOVTYPE"] == "001"}
    assert us["EP0045"]["FT_EMP"] == "402414"
    assert us["EP0045"]["FT_PAY"] == "2419870841"
    assert us["EP0085"]["FT_EMP"] == "251189"
    assert us["EP0085"]["FT_PAY"] == "1499857156"
    assert len(records) == 102
    assert all(abs(c["residual"]) <= c["tolerance"] for c in checks)
    assert sum(r["ft_employees"] for r in records if r["basket"] == "finance") == 402414
    assert sum(r["ft_employees"] for r in records if r["basket"] == "finance_and_other_admin") == 653603


def test_changed_national_total_is_rejected(originals, tmp_path):
    _, _, states, national, population = originals
    table = json.loads(national.read_text())
    field = table[0].index("FT_EMP")
    function = table[0].index("AGG_DESC")
    gov = table[0].index("GOVTYPE")
    row = next(r for r in table[1:] if r[function] == "EP0045" and r[gov] == "001")
    row[field] = str(int(row[field]) + 1)
    wrong = tmp_path / "national.json"
    wrong.write_text(json.dumps(table))
    with pytest.raises(ValueError, match="states/DC minus US"):
        parse_employment(states, wrong, population)


def test_observed_fits_match_independent_wls_and_identity(originals):
    records = originals[0]
    fits, decompositions = estimate(records)
    assert len(fits) == 32
    assert len(decompositions) == 8
    assert max(abs(r["residual"]) for r in decompositions) < 1e-10
    for fit in fits:
        excluded = {"11"} if fit["sample"] == "all50" else {"02", "11", "15"}
        selected = [r for r in records if r["basket"] == fit["basket"] and r["state_fips"] not in excluded]
        pop = np.array([r["population_2022"] for r in selected])
        weight = pop if fit["weight"] == "population" else np.ones(len(pop))
        model = sm.WLS(np.log([r[fit["outcome"]] for r in selected]), sm.add_constant(np.log(pop)), weights=weight).fit(cov_type="HC3", use_t=True)
        assert fit["beta"] == pytest.approx(model.params[1], rel=1e-9)
        assert fit["hc3_se"] == pytest.approx(model.bse[1], rel=1e-8)
        assert fit["ci95_low"] == pytest.approx(model.conf_int()[1, 0], rel=1e-8)
        assert fit["ci95_high"] == pytest.approx(model.conf_int()[1, 1], rel=1e-8)
        assert (fit["evidence"] == "secondary_modeled_FTE") == (fit["outcome"] == "fte_modeled")
