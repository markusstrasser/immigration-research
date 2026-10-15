"""Fresh Mexican payroll/profile inputs for tests of archived v7 US contracts.

The archived derived directory remains read-only. One session build supplies the
new statutory profiles while keeping the tests' frozen v7 US receipt oracles.
This diagnostic fixture is not an adopted world reading or pension estimate.
"""
import shutil
import sys
from pathlib import Path

import pytest

import g2_premium as G
import mexico as M
import valuation as V
import world_ledger as W

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))
from memory_budget import require_within_budget


@pytest.fixture(scope="session")
def v7_inputs(tmp_path_factory):
    """Rebuild current salary/profile schema once, exclusively in pytest scratch."""
    target = tmp_path_factory.mktemp("world_v7_diagnostic") / "derived"
    shutil.copytree(Path(__file__).resolve().parent / "derived", target)
    with pytest.MonkeyPatch.context() as patch:
        for module in (M, G, W, V):
            patch.setattr(module, "DERIVED", target)
        M.main()
        G.main("lineage")
        inp = W.load("oct14", "lineage")
        require_within_budget("v7 diagnostic test fixture")
    inp.update(pension_basis="legacy_mixed_diagnostic", historical_probe=True,
               mexico_capital_source=False, mexico_isn=False, mexico_input_dir=target)
    return inp
