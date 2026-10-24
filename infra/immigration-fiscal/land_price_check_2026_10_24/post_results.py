"""Post-results reading (not the pre-registered test): source B with its two CPI-converted counties moved to 2024 by
house-price indexes instead. San Bernardino and Santa Clara have no Case-Shiller index of their own; the worker used
the CPI, which understates land appreciation from 2005-2010 to 2024. Here they take Case-Shiller Los Angeles and San
Francisco (the worker's own fallback indexes). Inputs come from `post_results_inputs.py`, run on the workers' scratch
caches: `derived/post_results_inputs.json`.

    uv run --no-project python3 infra/immigration-fiscal/land_price_check_2026_10_24/post_results.py
"""
import json
from pathlib import Path

import test as t

HERE = Path(__file__).resolve().parent
inp = json.loads((HERE / "derived" / "post_results_inputs.json").read_text())
ref, total = t.load_reference()
b = t.load_prices("B_transactions")
for c in ("06071", "06085"):
    if abs(b[c] - inp[c + "_B"]["cpi"]) > 0.5:
        raise ValueError(f"[BLOCKED] B's {c} price no longer matches the post-results input")
    b[c] = inp[c + "_B"]["case_shiller"]
res = {"B_transactions_house_index": t.test_source(b, ref, total)}
res["A_assessor_alternatives"] = {c: inp[c] for c in ("06037", "06073", "06071")}
res["note"] = ("B passes with house-price indexes; A and C still fail, so 1 of 3 passes and land stays not identified. "
               "A's acre-weighted mean is below its median; its lot<=1 acre San Diego variant (worker) is q 0.52.")
(HERE / "derived" / "post_results.json").write_text(json.dumps(res, indent=1, sort_keys=True) + "\n")
r = res["B_transactions_house_index"]
print(f"B with house-price indexes: mean q {r['gmean_q']:.3f}, LA q {r['q']['06037']:.2f}, passes {r['passes']}, "
      f"sum {r['repriced_bn'][0]:.2f} / {r['repriced_bn'][1]:.2f}bn")
