"""Consistency of historical and live person-level accrual outputs (derived/sept29/ and derived/oct14/): the comparison file repeats
the flat, person and central arms' shares, every arm keeps the union's accrual and the central keeps the case's
totals, and the model record carries the payload's pension figures."""
import json
import ast
import importlib.util
from types import SimpleNamespace
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

D = Path(__file__).resolve().parent / "derived/sept29"
KEY = ["convention", "end", "breakdown", "cell"]


@pytest.fixture(params=["sept29", "oct14", "oct14/shared_allocation"])
def case_dir(request):
    return Path(__file__).resolve().parent / "derived" / request.param


def arms(case_dir):
    a = pd.read_csv(case_dir / "person_accrual_arms.csv")
    return a.set_index(["arm", *KEY])


def test_arms_repeat_the_flat_and_person_files(case_dir):
    a = arms(case_dir)
    for arm, name in (("flat", "net_positive_shares.csv"), ("person", "net_positive_shares_person_accrual.csv"),
                      ("person_payroll_onbooks", "net_positive_shares_person_onbooks.csv")):
        f = pd.read_csv(case_dir / name).query("convention in ['A', 'B']").set_index(KEY)
        sub = a.loc[arm].reindex(f.index)
        if arm == "flat":   # the flat file has no case-flag rows; the arms file adds them
            assert set(a.loc[arm].index) - set(f.index) == {k for k in a.loc[arm].index if k[2] == "head_status_case_flag"}
        assert np.allclose(sub.share_members_net_positive, f.share_members_net_positive, atol=1e-6)
        assert np.allclose(sub.se, f.se, atol=1e-6)
        assert (sub.records == f.records).all()


def test_flat_arm_is_its_own_baseline(case_dir):
    flat = arms(case_dir).loc["flat"]
    assert (flat.diff_vs_flat.abs() < 1e-12).all() and (flat.se_diff.abs() < 1e-12).all()


def test_every_arm_keeps_the_union_accrual(case_dir):
    # Each arm spreads each generation's accrual inside the generation, so the union's per member is the flat arm's.
    a = pd.read_csv(case_dir / "person_accrual_arms.csv").query("breakdown == 'all'")
    spread = a.groupby(["convention", "end"]).pension_accrual_per_member_usd.agg(lambda s: s.max() - s.min())
    assert a.arm.nunique() == 7 and (spread < 1e-6).all()


def test_central_keeps_the_case_totals(case_dir):
    # The central moves payroll taxes and accrual only inside generations: its control totals are the flat arm's.
    flat = pd.read_csv(case_dir / "control.csv").set_index(["end", "item"]).bn
    central = pd.read_csv(case_dir / "control_person_onbooks.csv").set_index(["end", "item"]).bn
    assert flat.index.equals(central.index) and np.allclose(flat, central, atol=1e-6, rtol=0)


def test_model_record_carries_the_payload():
    m = json.loads((D / "person_accrual_model.json").read_text())
    assert m["gates_passed"] and m["pension_commit"] == "9ea1beb"
    u = m["oasdi"]["union"]
    net = u["per_tax_dollar_gross"] * (1 - u["future_share_own_rate"])
    assert abs(net - m["payload"]["ratio_net"]) < 1e-12
    assert abs(m["part_a_bn"]["union"] - m["payload"]["part_a_accrual_bn"]) < 1e-6
    assert abs(sum(m["part_a_bn"][g] for g in ("G1", "G2", "G3plus")) - m["part_a_bn"]["union"]) < 1e-9


def test_late_frame_schema_covers_the_household_and_status_callers():
    """A newly used source column must not be silently dropped by the memory projection."""
    lane = Path(__file__).resolve().parent
    tree = ast.parse((lane / "households.py").read_text())
    schema = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
                  and any(isinstance(t, ast.Name) and t.id == "HOUSEHOLD_COLUMNS" for t in n.targets))
    main = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "main")
    projection = next(n.lineno for n in main.body if isinstance(n, ast.Assign)
                      and isinstance(n.value, ast.Call) and isinstance(n.value.func, ast.Name)
                      and n.value.func.id == "household_frame")
    status = ast.parse((lane.parent / "status_impute_2026_09_16/impute_status.py").read_text())
    imputer = next(n for n in status.body if isinstance(n, ast.FunctionDef) and n.name == "impute")
    required = set()
    nodes = [n for n in ast.walk(main) if getattr(n, "lineno", 0) > projection] + list(ast.walk(imputer))
    for n in nodes:
        if isinstance(n, ast.Attribute) and isinstance(n.value, ast.Name) and n.value.id == "d" and n.attr.isupper():
            required.add(n.attr)
        if isinstance(n, ast.Subscript) and isinstance(n.value, ast.Name) and n.value.id == "d":
            required.update(s.value for s in ast.walk(n.slice) if isinstance(s, ast.Constant)
                            and isinstance(s.value, str) and s.value.isupper())
    assert required <= set(schema), f"late frame omits caller fields: {sorted(required - set(schema))}"


def test_row4_blocks_match_the_real_canonical_builder():
    lane = Path(__file__).resolve().parent
    spec = importlib.util.spec_from_file_location("household_canonical_test", lane / "households.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    cells = module.L.acs_cells()
    module.pa.default_memory_pool().release_unused()
    d = module.load_frame()
    weights = d[module.F.REPS].to_numpy(float)
    arms, expected_info = module.L.weight_arms(d, weights, cells)
    expected = arms["row4"]
    del arms
    actual, info = module.row4_weights(d, weights, cells)
    assert np.array_equal(actual, expected)
    assert info == expected_info


def test_missing_frame_stops_before_calling_the_loader(tmp_path):
    tree = ast.parse((Path(__file__).resolve().parent / "households.py").read_text())
    guard = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "load_frame")
    called = []
    namespace = {"F": SimpleNamespace(CACHE=tmp_path, load=lambda: called.append(True))}
    exec(compile(ast.Module(body=[guard], type_ignores=[]), "load_frame_guard", "exec"), namespace)
    with pytest.raises(SystemExit, match="canonical frame cache missing"):
        namespace["load_frame"]()
    assert not called
