import json
from pathlib import Path
import subprocess

import pytest

HERE = Path(__file__).resolve().parent


def test_sibling_registry_selection_and_fail_closed():
    script = r'''
const I=require(process.argv[1]);
let blocked=false;try{I.build17({B:{}},null,"set");}catch(e){blocked=/selectedItems/.test(e.message);}
if(!blocked)throw Error("missing selection did not fail");
const a=I.build16({},null,"set").meta.native_minor_calibration;
const b=I.build17({selectedItems:["coverage_tenure"]},null,"set").meta.coverage_tenure;
const joint=I.build17({selectedItems:["native_minor_calibration","coverage_tenure"]},null,"set").meta.coverage_tenure;
console.log(JSON.stringify({a,b,joint}));
'''
    result = subprocess.run(["node", "-e", script, str(HERE / "items.cjs")],
                            check=True, capture_output=True, text=True)
    actual = json.loads(result.stdout)
    source = json.loads((HERE / "derived/items.json").read_text())["sets"]["set"]
    for end in ("low", "high"):
        assert actual["a"]["by_end"][end]["total_bn"] == source["item16"]["by_end"][end]["total_bn"]
        assert actual["a"]["by_end"][end]["total_bn"]+actual["joint"]["by_end"][end]["total_bn"] == pytest.approx(source["joint"]["by_end"][end]["total_bn"], abs=1e-12)
        assert actual["b"]["by_end"][end]["total_bn"] == source["item17"]["by_end"][end]["total_bn"]


def test_coverage_count_interactions_and_generation_parts():
    source = json.loads((HERE / "derived/items.json").read_text())
    for scenarios in source["sets"].values():
        assert scenarios["unchanged"]["population_change"] == 0
        assert abs(scenarios["item17"]["population_change"]) < 1e-6
        assert scenarios["joint"]["population_change"] == pytest.approx(scenarios["item16"]["population_change"], abs=1e-6)
        for item in scenarios.values():
            for value in item["by_end"].values():
                assert sum(value["by_generation_bn"].values()) == pytest.approx(value["total_bn"], abs=1e-9)
