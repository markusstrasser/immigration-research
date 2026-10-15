"""Render the measured tables; no timestamps or process telemetry enter derived outputs."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def render():
    data = json.loads((HERE / "derived/results.json").read_text())
    rates = json.loads((HERE / "derived/rates.json").read_text())
    rows = data["results"]
    find = lambda arm, which, end: next(r for r in rows if (r["arm"], r["which"], r["end"]) == (arm, which, end))
    low, high = find("A", "set", "low"), find("A", "set", "high")
    text = [f"**Verdict:** One flat real rate per specification gives **${low['cost_bn']:.3f}–{high['cost_bn']:.3f}bn** on corrected v8, "
            f"changes of **{low['delta_bn']:+.3f}/{high['delta_bn']:+.3f}bn** at its fixed low/high ends. "
            "The simultaneous 2%→3% move at specification 11 is reported below; no new endpoints are selected. [CALCULATION: derived/arms.csv]",
            "# One rate per specification on corrected v8",
            "This is a model sensitivity for the income-year 2024 removal account, from the perspective of all other US residents. "
            "It holds the population, allocation, service responses, tax rules, economic quantities, payable-benefit paths and all non-rate assumptions fixed. "
            "Dollar figures are annual billions in the account's price basis, net cost; positive changes increase cost. "
            "The denominator is 45,230,062.30075857 whole lineage members (`meta.population_v8.with_coverage`). "
            "These are calculated counterfactuals, not observed historical group costs. [FRAMING-SENSITIVE] [DATA: main_case_2026_10_15/derived/summary.json v8]",
            "## Arms, totals and per member",
            "| Arm | Set | End / spec | Cost $bn | Δ v8 $bn | Cost/member $ | Δ/member $ |",
            "|---|---|---|---:|---:|---:|---:|"]
    for r in rows:
        text.append(f"| {r['arm']} | {r['which']} | {r['end']} / {r['specification']} | {r['cost_bn']:.6f} | {r['delta_bn']:+.6f} | {r['per_member_usd']:.2f} | {r['delta_per_member_usd']:+.2f} |")
    text += ["## Changes by valuation component",
             "[CALCULATION: derived/arms.csv, derived/components.csv] Each row is against corrected v8 at the same specification. "
             "Externally valued public-pension and retiree-health normal costs are held at their imported values, so each changes by zero in A and B; their rates and sizes are inventoried below. "
             "OASDI includes the future benefit-tax deduction's changed timing. Current benefit-tax receipts stay fixed. "
             "The cash set replaces OASDI/Part A accrual with current benefit payments, so its rate movement is entirely public capital.",
             "| Arm | Set | End | OASDI Δ $bn | Part A Δ $bn | Other accrual Δ $bn | Capital Δ $bn | Total Δ $bn |",
             "|---|---|---|---:|---:|---:|---:|---:|"]
    for r in rows:
        text.append(f"| {r['arm']} | {r['which']} | {r['end']} | {r['oasdi_delta_bn']:+.9f} | {r['part_a_delta_bn']:+.9f} | 0 | {r['capital_delta_bn']:+.9f} | {r['delta_bn']:+.9f} |")
    capital_totals = [sum(b["capital"].values()) for b in data["baselines"] if b["which"] == "set"]
    text.append(f"The complete baseline capital return is ${capital_totals[0]:.9f}/{capital_totals[1]:.9f}bn at the two ends, "
                "including engine/native cells, reporter carriers and coverage. The case summary's engine-only capital subtotal excludes the latter two. [CALCULATION: derived/results.json baselines]")
    text += ["The detailed CSV splits OASDI and Part A into original union, original added descendants, item 10 reporters, item 10 native children, and item 12 coverage. "
             "Capital splits into engine/native cells, reporter carriers, and coverage. Each component also has its own change per member. "
             "These disjoint deltas close to each arm's total within 1e-9bn before display rounding.",
             "## The rate component with both legs moving at specification 11",
             "| Set | 2% both legs $bn | 3% both legs $bn | 3% minus 2% $bn | Δ/member $ | Sign |",
             "|---|---:|---:|---:|---:|---|"]
    for which in ("set", "cash"):
        a, b = find("both_lowrate", which, "high"), find("both_highrate", which, "high")
        delta = b["cost_bn"] - a["cost_bn"]
        text.append(f"| {which} | {a['cost_bn']:.6f} | {b['cost_bn']:.6f} | {delta:+.6f} | {b['per_member_usd']-a['per_member_usd']:+.2f} | {'increases' if delta>0 else 'decreases'} cost |")
    k = rates["trustees_capital"]
    text += ["## Rate definitions and transport",
             "A uses flat real 2% at specification 16 and 3% at specification 11 for the OASDI and Part A calculations; capital already uses those rates. "
             "The imported `Economy.discount(float)` keeps historical tax accumulation fixed and changes future valuation on COLA inflation. "
             "Its annual indexing means the 2024→2025 factor retains the historical 2024 new-issue rate; the flat-rate arm starts with the 2025 rate. "
             "This reproduces the existing `rate_case_2_3` construction rather than retroactively changing historical returns. "
             "The SSA Note 2025.7 calibration denominator stays fixed; changing it together with the numerator would cancel the rate sensitivity. "
             "[SOURCE: pension_accrual_2026_09_28/lifetime_model.py:118–143; pension_tr2026_2026_10_06/pension_tr2026.py:277–279]",
             f"B leaves accrual at the Trustees path and charges capital at **{100*k['flat_real_equivalent']:.9f}% real** at both ends. "
             f"This is 1 / {k['annuity_factor']:.12f}, the reciprocal PV of one real dollar every end-year from 2025 onward. "
             "Nominal discount factors and accumulated COLAs come from the same imported 2026 economy through 2200; "
             f"the remaining perpetuity is valued at the ultimate real rate **{100*k['ultimate_real_rate']:.9f}%**. "
             "It is a declared level-real-perpetuity equivalent, not a unique rate for every pension maturity or an observed market average. "
             "[CALCULATION: build.py perpetuity_equivalent; derived/rates.json trustees_capital]",
             "`evaluate.cjs` starts from the mean of the two methods' `evaluateFull` results at specifications 16/11 in both sets. "
             "The source before v8 is the frozen oct14 generation/line split, used only to isolate the pre-completion/pre-coverage population. "
             "The pension model is rerun at published and row-4 weights; the unchanged row-4 results must match their full-precision upstream control. "
             "The adopted normalized generation shares, G3/white transport convention, reporter own-record profile ratios and coverage profiles are retained. "
             "Small serialization residuals in the frozen generation split remain in the baseline; only new-minus-old recalculated accrual deltas move. "
             "This is conditional on the case's existing person-profile approximations. It does not newly estimate missing people's ages or careers. "
             "[SOURCE: evaluate.cjs; row4_class_2026_09_29/row4_oct07.py:93–114; main_case_2026_10_14/item_row4.cjs; main_case_2026_10_15/item_union.cjs]",
             "A common rate is an accounting convention. The arithmetic alone does not rule out separately justified financing and social-opportunity rates; "
             "the finding is that these two entries' existing financing descriptions can be made consistent with a material change. "
             "The falsifier is a failed unchanged control, an omitted own-PV consumer, or failure of the component sums. "
             "This lane proposes no adoption and changes no live-case file. LLM bias can affect framing and source selection; deterministic controls constrain the calculation, not the choice of estimand. [INFERENCE]",
             "## Rate inventory",
             (HERE / "inventory.md").read_text(),
             "## Reproduce and checks",
             "```sh\nOPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/one_rate_2026_10_15/build.py\n"
             "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/one_rate_2026_10_15/ -q\n"
             "uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/one_rate_2026_10_15 "
             "\"uv run --no-project python3 {lane}/build.py\" "
             "\"uv run --no-project python3 -m pytest {lane}/test_one_rate.py -q\"\n```",
             "Outputs use LF. `derived/source_hashes.json` records upstream inputs and imported Python source. "
             "No timing, current timestamp or memory counter enters derived files. Runtime and memory use Python `time.perf_counter` and `resource.getrusage`; "
             "the validation log below records wall-clock times from `date`. No git mutation is performed.",
             "## Execution log",
             (HERE / "run-log.md").read_text()]
    blocks = []
    for item in text:
        if item.startswith("|") and blocks and blocks[-1].startswith("|"):
            blocks[-1] += "\n" + item
        else:
            blocks.append(item)
    (HERE / "RESULT.md").write_text("\n\n".join(blocks) + "\n")


if __name__ == "__main__":
    render()
