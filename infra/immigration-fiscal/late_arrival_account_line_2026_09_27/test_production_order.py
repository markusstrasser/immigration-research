"""JSON key order cannot change the physical production-array coordinate."""
import json
import subprocess
import pytest
import production as P


def test_grid_coordinate_matches_engine_for_reordered_json():
    path = P.F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json"
    dims = json.loads(path.read_text())["production"]["dims"]
    order = P.production_order(dims)
    coords = {k: dims[k][(i + 1) % len(dims[k])] for i, k in enumerate(order)}
    engine = P.F.FISCAL / "assumption_explorer_2026_09_21/engine.js"
    expected = int(subprocess.check_output(["node", "-e",
        "const E=require(process.argv[1]);process.stdout.write(String(E.productionIndex({production:{dims:JSON.parse(process.argv[2])}},JSON.parse(process.argv[3]))))",
        str(engine), json.dumps(dims), json.dumps(coords)], text=True))
    variants = (dims, dict(sorted(dims.items())), dict(reversed(list(dims.items()))))
    assert all(P.grid_index(variant, coords) == expected for variant in variants)


def test_unknown_production_dimension_stops():
    dims = json.loads((P.F.FISCAL / "assumption_explorer_2026_09_21/derived/model.json").read_text())["production"]["dims"]
    with pytest.raises(SystemExit, match="Engine.PRODUCTION_DIMS"):
        P.production_order(dict(dims, unknown=[1]))
