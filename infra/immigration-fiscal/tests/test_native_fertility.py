"""Regression checks for the September 17 age/exposure construction failures."""
import ast
import importlib.util
from pathlib import Path
import re

import numpy as np
import pandas as pd


LANE = Path(__file__).resolve().parents[1] / "native_fertility_2026_09_16"


def load_build():
    spec = importlib.util.spec_from_file_location("fertility_build", LANE / "build_panel.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_female_age_bins_and_missingness():
    frame = pd.DataFrame({f"B01001_{i:03d}E": [float(i - 29)] for i in range(30, 41)})
    numerator, denominator = load_build().women_age_windows(frame)
    assert numerator.iloc[0] == 25  # Census female 20, 21, 22–24, 25–29, 30–34.
    assert np.isclose(denominator.iloc[0], 57.2)  # Female 15–49 plus one fifth of 50–54.
    frame["B01001_036E"] = np.nan
    numerator, denominator = load_build().women_age_windows(frame)
    assert pd.isna(numerator.iloc[0]) and pd.isna(denominator.iloc[0])


def test_origin_labels_survive_code_reassignment():
    tree = ast.parse((LANE / "analyze.py").read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "origin_leaves")
    scope = {"re": re}
    exec(compile(ast.Module(body=[function], type_ignores=[]), "origin_leaves", "exec"), scope)
    old = {"B05006_001E": {"label": "Estimate!!Total:"},
           "B05006_080E": {"label": "Estimate!!Total:!!Asia:!!Western Asia:!!Israel"}}
    new = {"B05006_001E": {"label": "Estimate!!Total:"},
           "B05006_080E": {"label": "Estimate!!Total:!!Asia:!!Western Asia:!!Armenia"},
           "B05006_084E": {"label": "Estimate!!Total:!!Asia:!!Western Asia:!!Israel"}}
    before, after = scope["origin_leaves"](old), scope["origin_leaves"](new)
    common = before.keys() & after.keys()
    assert len(common) == 1
    label = next(iter(common))
    assert before[label] == "B05006_080E" and after[label] == "B05006_084E"


def test_growth_allocation_conserves_totals_and_preserves_missing():
    # Isolate the production statements from this legacy top-level analysis script.
    tree = ast.parse((LANE / "analyze.py").read_text())
    positions = {target.id: i for i, node in enumerate(tree.body) if isinstance(node, ast.Assign)
                 for target in node.targets if isinstance(target, ast.Name)}
    statements = tree.body[positions["shares"]:positions["bartik"] + 1]
    scope = {"np": np, "leaves": ["a", "b"],
             "S10": pd.DataFrame({"a": [20., 80., np.nan, 0.], "b": [40., 60., np.nan, 0.]}),
             "S23": pd.DataFrame({"a": [22., 88., np.nan, 0.], "b": [32., 48., np.nan, 0.]})}
    exec(compile(ast.Module(body=statements, type_ignores=[]), "allocation", "exec"), scope)
    prediction = scope["bartik"]
    assert np.allclose(prediction.iloc[:2], [-6., -4.])
    assert pd.isna(prediction.iloc[2])
    assert prediction.iloc[3] == 0  # Observed zero is distinct from unavailable exposure.
    assert np.isclose(prediction.sum(), -10)  # Total origin change is allocated once.
