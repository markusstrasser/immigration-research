"""The live age comparison must retain its rough level and the principal case amount."""
import ast
from pathlib import Path


def test_live_levels_preserve_principal_and_remove_only_age_calibration():
    source = Path(__file__).with_name("social_rows.py")
    tree = ast.parse(source.read_text())
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "comparison_fiscal_level"]
    assert len(functions) == 1
    namespace = {}
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), "exec"), namespace)
    level = namespace["comparison_fiscal_level"]
    # A $20bn case/rough bridge belongs beside the $75bn rough age row.
    assert level("oct15", "mexican_origin_rough_white_ages", 75., 100., 80.) == 75.
    assert level("oct15", "mexican_origin_engine", 100., 100., 80.) == 100.
    assert level("oct15", "indian_origin", -10., 100., 80.) == -10.
    assert level("oct14", "mexican_origin_rough_white_ages", 75., 100., 80.) == 95.
