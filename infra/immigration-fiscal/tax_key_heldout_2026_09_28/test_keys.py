"""keys.py: the federal key sums to 1 over civilians and gives the union heldout's translated share at both
allocations (1e-12), every case_keys gate passes, and A1 (third-plus non-Hispanic whites on the white lane's oct15
frame) reproduces income_tax_keys_oct15.csv at both allocations. The shared-share regression pin is on the
historical frame; v8's count is read from its payload, not used to change these person-level keys.
The A1 test imports the white library (white_replacement_2026_09_28/rekey_sept29.py), about 80 s and 1.5 GB.

    uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/tax_key_heldout_2026_09_28/test_keys.py -q
"""
import importlib.util
import hashlib
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True   # the white library's imports read other lanes: write nothing beside them

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import pytest  # noqa: E402

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
_spec = importlib.util.spec_from_file_location("tax_key_heldout_keys", HERE / "keys.py")
TK = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(TK)
A1_FEDERAL_SHARED = 0.150132410617     # baseline lineage frame remains separate from item 10's carriers


@pytest.fixture(scope="module")
def built():
    gates = []
    d = TK.load_frame()
    civ, union = TK.benchmark_frame().masks(d)
    keys = TK.case_keys(d, civ, union, lambda label, ok, detail="": gates.append((label, bool(ok), detail)))
    sys.path.insert(0, str(FISCAL / "scripts"))
    from memory_budget import require_within_budget
    require_within_budget("heldout person-key tests")
    return d, civ, union, keys, gates


def test_every_gate_passes(built):
    gates = built[4]
    assert len(gates) == 5 and all(ok for _, ok, _ in gates), [g for g in gates if not g[1]]


@pytest.mark.parametrize("alloc", TK.ALLOCATIONS)
def test_federal_key_sums_to_one_and_gives_heldouts_union_share(built, alloc):
    d, civ, union, keys, _ = built
    w0 = d.pwwgt0.to_numpy(float) * civ
    v = keys[f"fit_case_{alloc}"]
    held = json.loads((HERE / "derived/translation_inputs.json").read_text())
    want = held["reweighted_share"][alloc] + held["share_change"]["irs_2023_raked_with_cbo_groups"][alloc]
    assert abs(float(w0 @ v) - 1) < 1e-12
    assert abs(float(w0[union] @ v[union]) - want) < 1e-12
    assert not (v[~civ] != 0).any()


@pytest.mark.parametrize("alloc", TK.ALLOCATIONS)
def test_a1_share_on_the_white_lanes_oct15_frame(built, alloc):
    d, _, _, keys, _ = built
    sys.path.insert(0, str(FISCAL / "white_replacement_2026_09_28"))
    import rekey_sept29 as W   # noqa: E402
    R = W.R
    assert np.array_equal(d.PH_SEQ.to_numpy(), R.d.PH_SEQ.to_numpy())
    assert np.array_equal(d.SPM_ID.to_numpy(), R.d.SPM_ID.to_numpy())
    w4, n4 = W.row4_weights()
    payload = json.loads((FISCAL / "main_case_2026_10_15/derived/corrections.json").read_text())
    assert payload["meta"]["adopted"] == "2026-10-15"
    assert payload["meta"]["allocation"]["group_total"] == "personal"
    leaf_meta = json.loads((FISCAL / "white_replacement_2026_09_28/derived/income_tax_keys_oct15_meta.json").read_text())
    assert leaf_meta["case"] == "oct15" and leaf_meta["allocation"] == "personal"
    assert leaf_meta["baseline_lineage_counts"] == payload["meta"]["lineage"]["counts"]
    baseline_population = payload["meta"]["lineage"]["counts"]["lineage_population"]
    comparison_population = payload["meta"]["population_v8"]["with_coverage"]
    assert leaf_meta["tax_key_control_baseline_population"] == baseline_population
    assert leaf_meta["comparison_population"] == comparison_population
    for relative in ("main_case_2026_10_15/derived/corrections.json", "tax_key_heldout_2026_09_28/keys.py"):
        assert hashlib.sha256((FISCAL / relative).read_bytes()).hexdigest() == leaf_meta["inputs_sha256"][relative]
    leaf_csv = "white_replacement_2026_09_28/derived/income_tax_keys_oct15.csv"
    assert hashlib.sha256((FISCAL / leaf_csv).read_bytes()).hexdigest() == leaf_meta["csv_sha256"][leaf_csv]
    w3 = R.MASK["w3"]
    assert abs(n4 + payload["meta"]["lineage"]["counts"]["added"] - baseline_population) < 1e-8
    baseline_cw = w4 * w3 * (baseline_population / float(w4[w3].sum()))
    cw = w4 * w3 * (comparison_population / float(w4[w3].sum()))
    v = keys[f"fit_case_{alloc}"]
    got = float(cw @ v / (w4 @ v))
    printed = pd.read_csv(FISCAL / "white_replacement_2026_09_28/derived/income_tax_keys_oct15.csv").set_index(
        ["group", "line"]).loc[("A1_third_plus_nh_white", "federal_income_tax"), f"share_{alloc}"]
    if alloc == "shared":
        baseline_got = float(baseline_cw @ v / (w4 @ v))
        assert abs(baseline_got - A1_FEDERAL_SHARED) < 1e-12
    assert f"{got:.9f}" == f"{float(printed):.9f}"
    from memory_budget import require_within_budget
    require_within_budget("heldout white-frame tests")
