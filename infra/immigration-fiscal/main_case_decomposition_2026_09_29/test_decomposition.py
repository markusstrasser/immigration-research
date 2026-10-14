"""A failed external case oracle must not leave publishable decomposition files."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FISCAL = ROOT / "infra/immigration-fiscal"


def test_failed_band_oracle_writes_no_outputs(tmp_path):
    package = json.dumps(str(FISCAL / "main_case_2026_10_14/package.cjs"))
    script = json.dumps(str(FISCAL / "main_case_decomposition_2026_09_29/decompose.cjs"))
    output = json.dumps(str(tmp_path))
    program = f"""
const p = require({package});
const original = p.csvRows;
p.csvRows = (rel) => original(rel).map(r =>
  rel.endsWith('main_case_bands.csv') && r.variant === 'adopted'
    ? {{...r, cost_low_bn: Number(r.cost_low_bn) + 1}} : r);
process.argv = ['node', 'decompose.cjs', '--case', 'oct14', '--out-dir', {output}];
require({script});
"""
    result = subprocess.run(["node", "-e", program], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 1, result.stderr
    assert "FAIL the case equals main_case_bands.csv" in result.stdout
    assert not list(tmp_path.iterdir()), "Failed oracle left decomposition artifacts"
