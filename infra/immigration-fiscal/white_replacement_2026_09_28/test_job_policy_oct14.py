"""An undeclared comparator must not silently receive the white R7 factor."""
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def consumer():
    path = Path(__file__).parent / "rekey_sept29.py"
    spec = importlib.util.spec_from_file_location("job_policy_consumer", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    module.use_case("oct16")
    return module


@pytest.mark.parametrize("group", ["ind", "ind1", "ind1se", "ind1wage", "ind1oth", "hhse", "hhwage"])
def test_undeclared_indian_policy_stops(consumer, group):
    for category in consumer.JOB_CAPITAL["lines"]:
        with pytest.raises(SystemExit, match="no R7 job-capital policy"):
            consumer.job_factor(group, category)


@pytest.mark.parametrize("group,source", [("w3", "white_nh"), ("wus", "white_nh"), ("wall", "white_nh"), ("blk", "black_nh")])
def test_authorized_comparator_uses_source_factor(consumer, group, source):
    for category in consumer.JOB_CAPITAL["lines"]:
        assert consumer.job_factor(group, category) == consumer.JOB_CAPITAL["factor"][source][category]["personal"]


def test_all_residents_uses_excluded_national_base(consumer):
    for category, line in consumer.JOB_CAPITAL["lines"].items():
        assert consumer.job_factor("avg", category) == line["base_bn"] / line["national_bn"]
