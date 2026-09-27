"""Read-only distinction between current saving, borrowing and imputed return."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parents[3]
FISCAL = ROOT / "infra/immigration-fiscal"
source = ROOT / "sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx"
table = pd.read_excel(source, "T30200-A", header=None)
year_col = table.columns[table.iloc[7].eq(2024)].item()
table[0] = pd.to_numeric(table[0], errors="coerce")
selected = table[table[0].isin([37, 42, 45, 46, 47, 48, 49])]
v = {int(r[0]): float(r[year_col]) / 1000 for _, r in selected.iterrows()}
assert len(v) == 7, "Federal capital-account rows missing"
reconstructed = v[37] + v[48] + v[42] - v[46] - v[45] - v[47]
assert abs(reconstructed - v[49]) <= 0.003, "Net-lending identity fails"
spec_file = FISCAL / "main_case_long_run_2026_09_27/derived/per_spec.csv"
spec = pd.read_csv(spec_file)
assert len(spec) == 128 and spec.method.nunique() == 2
assert (spec.cost_bn - spec.engine_cost_bn - spec.capital_total_bn).abs().max() < 1e-9
ends = {}
for label, idx in [("low", 48), ("high", 11)]:
    rows = spec[spec.spec.eq(idx)]
    assert len(rows) == 2
    cols = ["cost_bn", "engine_cost_bn", "capital_total_bn", "capital_federal_bn",
            "capital_state_local_bn", "group_housing_subsidies_bn"]
    ends[label] = rows[cols].mean().to_dict()
result = {
    "units": "billions of 2024 dollars; national figures are not group corrections",
    "federal_national": {"current_saving_bn": v[37], "net_lending_bn": v[49],
                         "reconstructed_net_lending_bn": reconstructed,
                         "borrowing_minus_current_deficit_bn": v[37] - v[49]},
    "main_case_fixed_end_specifications": ends,
    "source_sha256": {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                      for p in [source, spec_file]},
}
print(json.dumps(result, indent=2, sort_keys=True))
