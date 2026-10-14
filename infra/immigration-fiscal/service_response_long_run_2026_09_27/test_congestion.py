import importlib.util
import json
from pathlib import Path

import numpy as np
import pytest

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('congestion_test', HERE/'congestion.py')
C = importlib.util.module_from_spec(spec)
spec.loader.exec_module(C)


def test_optimized_arm_matches_original_with_signed_relief():
    _, nhts, tau, vot, exposures, _ = C.setup()
    ex = exposures['2017 southwest']
    scope = ex.in_scope.to_numpy()
    for cut in (0., .07559, .2):
        args = (ex, scope, ex.phi_commute_route, .32, .104, cut, tau['central'], vot['central'], 2022, nhts['2017 southwest']['r_hours'])
        result = C.A.time_cost_arm(ex, .32*np.log1p(-ex.phi_commute_route)-.104*np.log1p(-cut), 0., tau['central'], ex.phi_commute_route, vot['central'], 2022, args[-1])
        assert C.arm(*args) == pytest.approx(C.A.summarise(result, ex, scope)['total_bn'], abs=1e-9)


def test_parent_boundary_baseline_and_replacement_closure():
    baseline = json.loads((HERE/'derived/congestion_pairing_baseline_oct15.json').read_text())
    replacement = {end: {'congestion_bn': baseline['source_published_before'][end+'_end']} for end in ('low','high')}
    C.GATES.clear()
    rows = C.pairing_values(baseline, replacement)
    assert all(g['passed'] for g in C.GATES)
    for row in rows.values():
        assert row['lineage_congestion_delta_bn'] == pytest.approx(0., abs=1e-9)
        assert row['replacement_lineage_congestion_bn'] == pytest.approx(row['baseline_lineage_congestion_bn'], abs=1e-9)
    baseline['row']['union_low_bn'] += 1.
    C.GATES.clear()
    with pytest.raises(SystemExit, match='no new outputs written'):
        C.pairing_values(baseline, replacement)
    assert any(not g['passed'] for g in C.GATES)
