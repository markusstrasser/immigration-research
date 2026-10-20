"""Unknown scalar costs cannot pass silently through comparator coverage."""
import importlib.util
from pathlib import Path

import pytest


@pytest.fixture(scope='module')
def consumer():
    spec = importlib.util.spec_from_file_location('scalar_policy_consumer', Path(__file__).with_name('rekey_sept29.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_new_scalar_stops(consumer):
    e = {'lines': [{'side': 'scalar', 'id': 'production_gain_bn', 'effect_bn': 0},
                   {'side': 'scalar', 'id': 'new_credit', 'effect_bn': 10}]}
    with pytest.raises(SystemExit, match='undeclared or duplicate'):
        consumer.validate_scalars(e)


def test_duplicate_scalar_stops(consumer):
    line = {'side': 'scalar', 'id': 'production_gain_bn', 'effect_bn': 1}
    with pytest.raises(SystemExit, match='undeclared or duplicate'):
        consumer.validate_scalars({'lines': [line, line]})


def test_known_scalar_policies_cover_live_and_archived_dump(consumer):
    for dump in (consumer.DUMP27, consumer.DUMP['accrual'], consumer.DUMP['cash']):
        for end in consumer.ENDS:
            assert consumer.validate_scalars(dump[end])


def test_full_only_lineage_scalar_stops(consumer):
    import copy
    consumer.use_case('oct16')
    bad = copy.deepcopy(consumer.FULL['accrual']['low'])
    bad['lines'].append({'side': 'scalar', 'id': 'added_only_credit', 'effect_bn': 10})
    with pytest.raises(SystemExit, match='undeclared or duplicate'):
        consumer.lineage_part(bad, consumer.DUMP['accrual']['low'])
    original = consumer.FULL['accrual']['low']
    consumer.FULL['accrual']['low'] = bad
    try:
        with pytest.raises(SystemExit, match='undeclared or duplicate'):
            consumer.run29('eng', 'low')
    finally:
        consumer.FULL['accrual']['low'] = original
