"""A failed external case oracle must not leave publishable decomposition files."""
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
FISCAL = ROOT / "infra/immigration-fiscal"


def test_optional_response_cannot_be_hidden_in_completion():
    script = json.dumps(str(FISCAL / "main_case_decomposition_2026_09_29/v8_attribution.cjs"))
    program = f"""
const adapter = require({script});
const api = {{correctionsPayload: () => ({{meta: {{items: [{{id: 'item6_low_corporate_response', applied: true}}]}}}})}};
adapter.build(api, false, [], () => {{}});
"""
    result = subprocess.run(["node", "-e", program], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode != 0
    assert "needs a distinct step for nondefault item6_low_corporate_response" in result.stderr


def test_coverage_source_parts_keep_execution_separate_from_classification():
    script = json.dumps(str(FISCAL / "main_case_decomposition_2026_09_29/v8_attribution.cjs"))
    program = f"""
const {{coverageParts}} = require({script});
const row = {{total_bn: 4.2, decomposition: {{production: {{P_bn: 0.2, F_bn: 0.1}},
  capital_by_level_bn: {{federal: 0.5}}, unclassified_bn: 1, classified_fiscal_line_bn: 3,
  line_parts: [{{economic_class: 'fiscal_line', source_side: 'receipt', source_line: 'tax', coverage_bn: -2}},
    {{economic_class: 'fiscal_line', source_side: 'spending', source_line: 'benefit', coverage_bn: 5}}]}}}};
const p = coverageParts(row);
if (p.receipts_by_line.tax !== -2 || p.spending_by_line.benefit !== 5 || p.post_engine_bn !== 1)
  throw Error('Coverage execution amount replaced typed source classification');
row.decomposition.line_parts.pop();
try {{ coverageParts(row); throw Error('Dropped source part silently passed'); }}
catch (e) {{ if (!e.message.includes('fiscal source lines do not match')) throw e; }}
"""
    result = subprocess.run(["node", "-e", program], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 0, result.stderr


def test_failed_band_oracle_writes_no_outputs(tmp_path):
    package = json.dumps(str(FISCAL / "main_case_2026_10_15/package.cjs"))
    script = json.dumps(str(FISCAL / "main_case_decomposition_2026_09_29/decompose.cjs"))
    output = json.dumps(str(tmp_path))
    program = f"""
const p = require({package});
const original = p.csvRows;
p.csvRows = (rel) => original(rel).map(r =>
  rel.endsWith('main_case_bands.csv') && r.variant === 'adopted'
    ? {{...r, cost_low_bn: Number(r.cost_low_bn) + 1}} : r);
process.argv = ['node', 'decompose.cjs', '--case', 'oct15', '--v8-attribution', 'sequential', '--out-dir', {output}];
require({script});
"""
    result = subprocess.run(["node", "-e", program], cwd=ROOT, capture_output=True, text=True)
    assert result.returncode == 1, result.stderr
    assert "FAIL the case equals main_case_bands.csv" in result.stdout
    assert not list(tmp_path.iterdir()), "Failed oracle left decomposition artifacts"
