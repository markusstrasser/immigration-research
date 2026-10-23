"""Extract Putterman source inputs; incomplete index coverage is bounded, never zeroed.

Run: uv run --no-project --with xlrd python3 {lane}/extract_roots.py
Inputs: {lane}/_cache/social_{statehist,matrix}.xls (original author-linked files).
Output: {lane}/derived/roots_inputs.json, or --out-dir <scratch>.
The paper's statehist is 1-1500, NOT the workbook's precomputed 1-1950 index.
"""

import argparse
import hashlib
import json
from pathlib import Path

import xlrd


HERE = Path(__file__).resolve().parent
CACHE = HERE / "_cache"
SOURCE = {
    "social_statehist.xls": "https://drive.google.com/uc?export=download&id=1mS-KaK5sGgd3HYXSwBmMeBin_hT_8x0R",
    "social_matrix.xls": "https://drive.google.com/uc?export=download&id=1BC9tdKJ_uZi8F8BvzPdo9LXQKpRxsJZ6",
}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    files = {}
    for name, url in SOURCE.items():
        path = CACHE / name
        raw = path.read_bytes()
        if not raw.startswith(bytes.fromhex("d0cf11e0a1b11ae1")):
            raise SystemExit(f"[BLOCKED] Expected Excel OLE file: {name}")
        files[name] = {"url": url, "sha256": hashlib.sha256(raw).hexdigest()}

    state = xlrd.open_workbook(CACHE / "social_statehist.xls").sheet_by_index(0)
    assert state.cell_value(0, 11) == "1451-1500"
    assert state.cell_value(0, 40).strip() == "1-50"
    weights = [1.05 ** (-t) for t in range(30)]
    denominator = 50 * sum(weights)
    index = {}
    for i in range(2, state.nrows):
        code = state.cell_value(i, 0).lower()
        assert code not in index
        index[code] = sum(state.cell_value(i, 11 + t) * weights[t] for t in range(30)) / denominator
        assert 0 <= index[code] <= 1
    assert abs(index["mex"] - 0.533) < 0.0005, "Mexico anchor does not match paper p11"
    assert index["usa"] == 0, "United States anchor does not match paper p11"
    assert abs(index["chn"] - 0.906) < 0.0005, "China anchor does not match paper p11"

    matrix = xlrd.open_workbook(CACHE / "social_matrix.xls").sheet_by_index(0)
    result = {"sources": files, "construction": "Paper Eq 1, 30 half-centuries 1451-1500 back to 1-50, normalized 5 percent discount", "countries": {}}
    for target in ("mex", "usa"):
        rows = [i for i in range(1, matrix.nrows) if matrix.cell_value(i, 0).lower() == target]
        assert len(rows) == 1
        i = rows[0]
        terms = [(matrix.cell_value(0, j), matrix.cell_value(i, j)) for j in range(2, matrix.ncols - 1) if matrix.cell_value(i, j)]
        total = sum(w for _, w in terms)
        assert abs(total - 1) < 0.00005
        missing = [{"code": c, "weight": w} for c, w in terms if c not in index]
        subtotal = sum(w * index[c] for c, w in terms if c in index)
        unknown_mass = sum(x["weight"] for x in missing)
        result["countries"][target] = {
            "unadjusted_statehist1500": index[target],
            "matrix_row_mass": total,
            "partial_sum_not_estimate": subtotal,
            "missing": missing,
            "missing_mass": unknown_mass,
            "normalized_lower": subtotal / total,
            "normalized_upper": (subtotal + unknown_mass) / total,
            "bound_meaning": "Only missing source indices bounded 0-1; neither confidence interval nor immigrant causal effect",
        }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / "roots_inputs.json"
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result["countries"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
