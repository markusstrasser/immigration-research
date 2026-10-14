"""Render P7 results and exact docs-worker wording from the checked numeric artifacts.

Native-First: plain Markdown and pandas CSV reads; no copied research-document numbers.
"""
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived/p7"
WINDOWS = ("10y_2015_2024", "15y_2010_2024", "20y_2005_2024")


def main():
    data = pd.read_csv(OUT / "windows.csv").set_index(["population", "rule", "scenario", "end"]).sort_index()

    def pair(pop, rule, scenario, column, digits=3):
        return " / ".join(f"{data.loc[(pop, rule, scenario, end), column]:,.{digits}f}" for end in ("low", "high"))

    def tn(rule, scenario):
        return "–".join(f"{data.loc[('lineage', rule, scenario, end), WINDOWS[0] + '_bn'] / 1000:.4f}"
                        for end in ("low", "high"))

    lines = [f"**Verdict:** The three controlled changes together put the 2015–2024 lineage back-cast at "
             f"${tn('ratio', 'stack')}tn (`ratio`), ${tn('income', 'stack')}tn (`income`) and "
             f"${tn('flat', 'stack')}tn (`flat`, with the historical capital-rate exception). "
             "These are beside results, not adopted changes to the fiscal case. The programme rule with measured "
             f"pandemic shares and available school-age/coverage keys gives ${tn('programme', 'programme_measured')}tn "
             f"or ${tn('programme_income', 'programme_measured')}tn with income scaling. "
             "[CALCULATION: `p7_backcast.py` → `derived/p7/windows.csv`]",
             "", "The current `derived/oct14/` files stay byte-identical. This is a model of historical costs in "
             "2024 dollars, summed without discounting, not observed historical group borrowing. Public-capital returns "
             "are imputed resource costs; pension accrual is valued future benefits. Personal allocation and "
             "specifications 16 / 11 are held throughout, rather than re-selecting historical band ends. "
             "[ASSUMPTION; DATA: `case_components_oct14.json`, `programme_inputs.json`]", "",
             "## Controlled changes", "", "Each entry is **low / high**, $bn accumulated in real 2024 dollars. "
             "Delta is against the same population, rule and window of the current case. The `union` means its "
             "39.71M identified members; `lineage` includes the 3.04M added descendants (42.75M in 2024). "
             "The added people's historical path is the identified G3+ count/share, with their 2024 ratio held fixed. "
             "The union follows the case-components split: the enlarged group's response change stays on the union. "
             "[DATA: `case_components_oct14.json` `lineage`; CALCULATION: `carried_parts`, `changes_annual.csv`]", ""]
    active = [("fixed_2pct", rule) for rule in ("flat", "ratio", "income")]
    active += [(scenario, rule) for scenario in ("yield_floor0", "yield_unfloored", "charged_base", "income_linked", "stack")
               for rule in ("flat", "ratio", "income")]
    for pop in ("lineage", "union"):
        lines += [f"### {pop}: totals", "", "| Scenario | Rule | 2015–2024 | 2010–2024 | 2005–2024 |",
                  "|---|---|---:|---:|---:|"]
        for scenario, rule in active:
            lines.append(f"| {scenario} | {rule} | " + " | ".join(pair(pop, rule, scenario, w + "_bn") for w in WINDOWS) + " |")
        lines += ["", f"### {pop}: one-change deltas and stack", "",
                  "| Scenario | Rule | 2015–2024 delta | 2010–2024 delta | 2005–2024 delta | 2024 annual delta |",
                  "|---|---|---:|---:|---:|---:|"]
        for scenario, rule in active:
            if scenario == "fixed_2pct":
                continue
            lines.append(f"| {scenario} | {rule} | " + " | ".join(pair(pop, rule, scenario, w + "_delta_bn") for w in WINDOWS)
                         + " | " + pair(pop, rule, scenario, "anchor_change_bn") + " |")
        lines.append("")
    lines += ["## Rate, base and income rules", "",
              "1. **Rate:** DFII10 is the daily inflation-indexed ten-year Treasury yield, in percent. Annual means "
              "exclude the file's blank non-trading days; 245–265 daily observations must exist per year. The low end "
              "uses the year's mean, floored at zero, divided by the old 2% on every capital component. The unfloored "
              "arm permits a negative cost of money. The high end retains 3%. The annual 2024 yield is "
              f"{pd.read_csv(OUT / 'real_yields.csv').set_index('year').loc[2024, 'mean']:.6f}%; its low-end cost moves "
              f"{pair('lineage', 'ratio', 'yield_floor0', 'anchor_change_bn')}bn. That movement is shown explicitly; "
              "it is not calibrated away. [SOURCE: https://fred.stlouisfed.org/series/DFII10; DATA: pinned "
              "`_cache/DFII10.csv`, `inputs/pins.json`; CALCULATION: `primary_rates` → `real_yields.csv`]", "",
              "2. **Charged base:** subtract NIPA 3.1 interest (line 27), subsidies (line 30) and NIPA 3.17 defence "
              "consumption (line 3) from total current expenditures. Recalibrate sigma at 2024, holding the base's "
              "charged group dollars fixed. The receipt base and the separately carried lines are held. Housing "
              "subsidies that the case does charge remain in the separate rental-assistance addition: excluding the "
              "whole subsidy line here avoids carrying the base with the excluded business subsidies. Flat has "
              "no national spending index, so this changes neither flat end. National totals close within 1e-9bn; "
              "the new spending index is exactly 1 at 2024. [DATA: pinned BEA Section3 workbook source cells; "
              "CALCULATION: `controlled_changes` → `charged_base.csv`]", "",
              "3. **Income:** apply the same measured ACS relative-income multiplier to the separately carried "
              "income-linked receipts, job-capital taxes keyed to wages, payroll-earned OASDI/Part A accrual, and "
              "induced production receipts. Property on homes, enterprises, user-fee carriers, other spending "
              "and private production value retain their existing path. A wages-based job-capital key is not an "
              "observation of historical capital-tax receipts. This preserves the unit-elasticity assumption. "
              "Every part's included/excluded classification is exported; ratio and flat do not use this "
              "multiplier. [ASSUMPTION; DATA: `income_classification.csv`; CALCULATION: `controlled_changes`]", "",
              "4. **Fail closed:** only `(T31200-A:20, 2005–2014)` is a permitted source/year blank. The pinned "
              "BEA note 4 says the post-2015 line includes reimbursements for healthcare received at private "
              "facilities; no such amounts are reported in the model's pre-2015 window. Every other absent or "
              "non-finite observation stops before cells are summed. Injection tests cover a missing 2019 "
              "observation, a missing year, a different source and infinity. This applies to both whole-budget "
              "and programme helpers; numerical controls are unchanged. [SOURCE: BEA T31200-A footnote 4; "
              "DATA: `STRUCTURAL_ZEROS`; CALCULATION: `test_p7_backcast.py`]", "",
              "**Disconfirmation of reviewer point estimates:** The live computation reproduces the ten-year "
              "low rate reduction to within about $0.2bn of the review's $211.8bn. The base correction is "
              f"{pair('lineage', 'ratio', 'charged_base', WINDOWS[0] + '_delta_bn')}bn, not $66bn. The income-linked "
              f"correction is {pair('lineage', 'income', 'income_linked', WINDOWS[0] + '_delta_bn')}bn, not "
              "−$65bn / +$39bn. The reviewer estimates were leads, not input data. [CALCULATION: `windows.csv`]", "",
              "**Review bar:** These are historical-rule corrections, not a new annual fiscal case. Rate has "
              "a 2024 change below $5bn at both ends; base and income recalibration preserve 2024; programme "
              "closes to the original case within 1e-6bn. None changes the annual headline by $5bn. The stated "
              "claim that every part of the current back-cast follows its programme series is falsified: its "
              "base follows whole-budget aggregates. The cumulative shifts exceed $5bn over many windows, "
              "which is a different denominator. [CALCULATION; INFERENCE]", "", "## Programme beside rule", ""]
    for pop in ("lineage", "union"):
        lines += [f"### {pop}", "", "| Variant | Rule | 2015–2024 total | 2010–2024 total | 2005–2024 total |",
                  "|---|---|---:|---:|---:|"]
        for variant in ("programme", "programme_pandemic", "programme_measured"):
            for rule in ("programme", "programme_income"):
                lines.append(f"| {variant} | {rule} | " + " | ".join(pair(pop, rule, variant, w + "_bn") for w in WINDOWS) + " |")
        lines.append("")
    lines += ["`programme` evaluates all charged v7 engine lines, at the personal specifications, on their "
              "national source series. OASDI accrual and the Part A accrual part of Medicare follow payroll "
              "contributions; Medicare's remaining part follows its benefit series. Synthetic lines follow "
              "their parents. The pension benefit-tax adjustment follows income-tax receipts. Capital follows "
              "its stock series at fixed 2% / 3%; private and induced production terms follow real GDP "
              "times their population-share path, as the case's existing production mapping does. "
              "`lane_constants` holds its 2024 value per person (no budget programme series). It includes "
              "the charged rental/energy-assistance and public-capital costs; a fiscal-gap-only debt output "
              "would omit those. The 2024 totals close to the full-precision engine at 1e-6bn. "
              "[DATA: `programme_inputs.json`; CALCULATION: `programme_lines.csv`]", "",
              "`programme_pandemic` replaces the refundable-credit line's 2020/2021 EIP part with the existing "
              "measured personal payment shares under the `borjas` SSN treatment and income-year/payment-year "
              "mapping. It applies measured relative use to the rest of that credit line. National EIP levels "
              "are parsed from annual line 31 of the pinned primary BEA PDF. The added non-identifying "
              "descendants' pandemic relative-use change is assumed to equal the identified union's, applied "
              "to their own G3+ population path; they are not observed by CPS identity. Other programme "
              "keys are held. [SOURCE: pinned BEA PDF URL in `inputs/pins.json`; DATA: "
              "`backcast_pandemic_measured_2026_09_28/derived/measured_shares.csv`; ASSUMPTION]", "",
              "`programme_measured` adds school-age (5–17 at survey) relative shares in 2005–2024 on the K-12 "
              "operating portion of education (the case's share coefficient) and school reprice, and Medicaid "
              "coverage relative shares in 2019–2024 on the medical line excluding its uncompensated-care key "
              "shift. The coverage fraction is held at the 2024 case fraction; the added people's fraction "
              "takes the same split. Medicaid is held at its 2024 relative key before 2019 because the local "
              "historical extract lacks coverage fields. Coverage counts are not programme spending; school "
              "age is a pupil-use proxy, not measured attendance. Capital and fee keys remain fixed at 2024. "
              "Both group paths are divided by the same extract's 2024 relative-use key; raw CPS headcounts "
              "are not scaled onto the case total. [DATA: `historical_use.csv`, `use_source_manifest.json`; "
              "ASSUMPTION]", "",
              "The coverage source has 160 replicate weights for 2019–2024. `programme_medicaid_se.csv` "
              "propagates each year's union/G3 covariance to a conditional annual price-change SE "
              "(2024 key and case prices fixed). The anchored 2024 change and SE are zero. Full-window SEs "
              "are not identified without cross-year survey covariance; school-age paths have no full-window "
              "replicates in the local extract. Rate and base use published series and have no survey sampling SE. "
              "No historical-tax/benefit causal estimate is claimed. [CALCULATION: `historical_use_replicates.csv`, "
              "`programme_medicaid_se.csv`; INFERENCE]", "",
              "`programme_pandemic_se.csv` prices the source lane's replicate SEs for the non-payment credit "
              "part, conditional on 2024 keys and prices. For the EIP part it gives lower/upper SE bounds "
              "across unknown round covariance (a single round has identical bounds). It does not add these "
              "parts' SEs or claim a whole-window SE. [DATA: source `measured_shares.csv` `relative_use_se`; "
              "CALCULATION: `programme_pandemic_se.csv`]", "",
              "## Gates, provenance and reproduction", "",
              "- Four live outputs reproduce byte for byte before any correction.",
              "- National charged/un-charged sums close at 1e-9bn; finite series and source/year gap checks fail closed.",
              "- Engine line effects plus production and capital close at 1e-9bn; programme/measurement 2024 anchors at 1e-6bn.",
              "- Historical-use grids: 52 central rows, 1,932 replicate rows; union plus other conserves national weights.",
              "- Rate high end and all inactive flat/income-index arms have exact zero shifts; the stack equals the three changes.",
              "- Primary downloads are immutable pins in `inputs/pins.json`; reused microdata hashes are in "
              "`use_source_manifest.json`, other dependencies in `audit.json`.", "",
              "Source-derived values and calculations constrain this LLM-produced output. The remaining political "
              "frame and historical relative-use assumptions are explicit, not made empirical by the arithmetic. "
              "[INFERENCE; repo instrument-bias caveat]", "", "```sh",
              "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/acquire_p7.py",
              "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/historical_use.py",
              "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/p7_backcast.py",
              "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/historical_backcast_2026_09_20/write_p7_result.py",
              "OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/historical_backcast_2026_09_20/ -q --import-mode=importlib",
              "```", "", "## Execution log", "",
              "- 2026-10-14 22:03 JST (`date`): the first programme union closure rejected the debt twin's split; "
              "traced its attribution difference and used the case's authoritative lineage parts instead.",
              "- 2026-10-14 22:10 JST (`date`): controls and 27 tests passed. Excel-sheet caching removed repeated "
              "parsing; P7 builds measured 4–8 seconds / about 0.20GB with `time.perf_counter` and "
              "`resource.getrusage`. Historical-use extraction measured 24.13 seconds / 1.90GB.",
              "- Final review/check receipts are in `validation.md`; no staging, merging or commits performed.", ""]
    (HERE / "RESULT.md").write_text("\n".join(lines))
    wording = ["**Verdict:** Replace the programme-series claim with wording that distinguishes the actual live "
               "base from the beside programme rule. The frozen central series has not been replaced.", "",
               "## Memo: current live rules", "",
               "These are model back-casts in 2024 dollars, not measured historical accounts. The `ratio` rule "
               "carries a whole-budget base with national current receipts and all current expenditures, with "
               "the group's 2024 ratios held fixed. Separately carried corrections follow their own national "
               "line series and population paths; public-capital returns follow net-stock series at fixed "
               "2% / 3%. The current `income` rule scales only the base receipts by measured ACS relative "
               "income; the carried corrections are unchanged. `flat` holds 2024 cost per member fixed, "
               "with added descendants on the identified G3+ count path. Across these live rules, 2015–2024 "
               "is $3.0–4.0tn. [DATA: `derived/oct14/backcast_windows.csv`; ASSUMPTION]", "",
               "## Memo: controlled corrections beside", "",
               f"Historical real ten-year yields floored at zero at the low end (high fixed 3%), a spending "
               f"base excluding defence, interest and subsidies, and income scaling on all separately carried "
               f"income-linked parts give ${tn('ratio', 'stack')}tn (`ratio`) and ${tn('income', 'stack')}tn "
               f"(`income`) over 2015–2024. The flat-with-historical-rate arm is ${tn('flat', 'stack')}tn. "
               "Each year's measured yield is used including 2024, so this sensitivity moves the 2024 low "
               "anchor as well; the change is shown separately and is below $5bn. These are beside sensitivities, "
               "not the adopted annual fiscal case. [CALCULATION: `derived/p7/windows.csv`; ASSUMPTION]", "",
               "## Memo: programme beside rule", "",
               f"The v7 `programme` rule carries every charged spending and receipt line with its national "
               f"programme or tax series, payroll-earned pension accrual with contribution series, capital "
               f"returns with stocks at fixed 2% / 3%, production with real GDP and population shares, and "
               f"constants per person. With measured "
               f"pandemic payment shares, historical school-age shares and available 2019–2024 coverage shares, "
               f"it gives ${tn('programme', 'programme_measured')}tn for 2015–2024, or "
               f"${tn('programme_income', 'programme_measured')}tn under `programme_income`. Medicaid before "
               "2019, fee and capital-use keys stay at 2024. Added non-identifying descendants follow measured "
               "G3+ population/use proxies. Both programmes reconcile to the 2024 v7 specifications at the "
               "personal allocation; their historical group shares remain modeled. [CALCULATION; ASSUMPTION]", "",
               "## FAQ 8: replacement passage", "",
               "The $3.0–4.0tn over 2015–2024 is a model back-cast across the current whole-budget `ratio`, "
               "base-receipt `income` and per-person `flat` rules. It is not a historical fiscal ledger: "
               "the base follows national whole-budget totals and separate corrections follow line series. "
               f"The three corrected rules beside give roughly ${min(data.loc[('lineage', rule, 'stack', 'low'), WINDOWS[0] + '_bn'] for rule in ('flat', 'ratio', 'income')) / 1000:.1f}–"
               f"{max(data.loc[('lineage', rule, 'stack', 'high'), WINDOWS[0] + '_bn'] for rule in ('flat', 'ratio', 'income')) / 1000:.1f}tn; "
               f"the programme-by-programme versions with measured pandemic shares and available yearly "
               f"use keys give ${tn('programme', 'programme_measured')}tn (or "
               f"${tn('programme_income', 'programme_measured')}tn with income scaling). Public-capital "
               "returns and accrued pension promises are inside these resource-cost totals, so they cannot "
               "be described as accumulated government borrowing. [CALCULATION; ASSUMPTION]", ""]
    (HERE / "docs-wording.md").write_text("\n".join(wording))
    print("Wrote RESULT.md and docs-wording.md from checked P7 outputs")


if __name__ == "__main__":
    main()
