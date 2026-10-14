**Verdict:** Revise the low-end premise to mobile capital returns with replacement income, as already stated in the frozen payload. Do not describe this as pure rents vanishing with US demand while owners' income stays fixed. None of the requested papers identifies the pure-rent share φ of the 2024 taxable supernormal slice, or its removal elasticity. Both fixed-rent and vanishing-rent arms can clear $5bn; none is established as the empirical central. This lane is a sensitivity analysis, not an adopted change. [INFERENCE; CALCULATION: `rents.py` → `derived/arms.csv`]

## Frame and held-fixed account

2024 annual dollars, $bn unless specified; one change from frozen v7, personal specifications 16 / 11, both fill-in methods averaged. All spending, other receipts, capital return, mining at zero response, the remaining supernormal slice and production's P/F retention remain fixed. The lineage baseline is 339.552 / 423.649; cash set 264.426 / 348.523. The identified union has 39,712,493 members; the lineage 42,752,213. Union figures use the union **at v7's lineage responses**, 317.743 / 395.811, to isolate this change; they are not the different union-only case. [DATA: `derived/case_inputs.json`; frozen `lineage_addition.json`]

Residence-tax rows assume **e_tax = 0**, meaning none of this incremental tax loss is already booked when the removed group's own income-tax receipts disappear. Without that assumption extra residence loss is `(1 − e_tax)R`, where e_tax is an unidentified tax-overlap fraction. Do not add taxes already counted on removed owners again. This parameter differs from e_private, the removed group's share of after-tax owner claims. Main private figures below assume e_private=0 and are **upper bounds**, not measured welfare of other residents. [ASSUMPTION; GAP; code review resolution]

## Primary sources and φ

φ denotes **pure economic rents / Treasury's taxable supernormal slice**, not the supernormal share itself. Treasury TP-5 is dated May 2012; the corresponding journal article appeared in 2013. Its definition is income above a risk-free return (printed p9 footnote4). Its p7 allocation **assumes** pure rent rather than risk. The parsed supernormal/normal split is 63% / 37%; it does not estimate composition within the former. [SOURCE: https://home.treasury.gov/system/files/131/TP-5.pdf]

| Primary paper | What it measures and competing explanation | Implication for 2024 φ |
|---|---|---|
| Cronin, Lin, Power & Cooper, TP-5, pp7–11 | Tax-base change under expensing; risk-free benchmark; pure-rent composition imposed for incidence | φ=1 is their incidence assumption, not a measurement. Empirically uncalibrated [0,1] for this target. |
| Power & Frerick 2016, WP111, pp4–8 | Risk-free tax-base share, 40% in 1992–2002 and 25% in 2003–2013. Excess includes risk, entrepreneurial labor, decreasing returns, market power and luck. Causes not conclusively identified. | No pure-rent composition or 2024 bridge; [0,1] sensitivity support. [SOURCE: https://home.treasury.gov/system/files/131/wp-111.pdf] |
| Barkai 2020, J Finance, pp2422–2442 | Nonfinancial corporate value-added residual after labor, risk-adjusted capital cost and production taxes; omitted-capital scenarios matter | Supports possible rents under his user cost, but cannot divide by Treasury's taxable supernormal slice. [0,1] remains uncalibrated. |
| Karabarbounis & Neiman 2019, NBER Macro Annual, pp168–191 | Π assigns residual to profits, K to missing capital, R to rental-rate adjustments. K/R retain externally fixed positive profits. Alternative models, not mixture estimates. | No empirical φ=1/0/0 conversion. [0,1] remains uncalibrated. |
| De Loecker, Eeckhout & Unger 2020, QJE, pp565–606 | Listed-firm markups and a separate profit/sales measure after overhead/user cost; fixed and earlier startup costs complicate the residual | Neither markup nor profit/sales is φ; corporate-tax and later-year bridge missing. [0,1] remains uncalibrated. |
| Crouzet & Eberly 2023, J Finance, pp1874–1911 | Q+ separates installed intangibles and rents on physical/intangible capital; distinguishes pure markup rents from decreasing-return quasi-rents | Intangibles and rents overlap. Neither valuation residual nor rents/value-added is φ. [0,1] remains uncalibrated. |

The four published-paper PDFs, pages, DOI identities, parsed numerical anchors, incompatible denominators and disconfirmation are in [literature evidence](literature-evidence.md). No historical macro residual is averaged into a 2024 taxable share. [SOURCE: its primary receipts; INFERENCE: target transfer]

## Ownership and residence-tax calibration

Use Rosenthal/Mucciolo's 2024 update of Rosenthal/Austin and Rosenthal/Burke, ownership year 2022, Table5 (article p106, hearing PDF p71). This is **all US corporate equity including closely held corporations and FDI**, with mutual-fund look-through, rather than publicly traded shares alone. Ownership-value shares are assumed to describe these rent-flow shares in 2024. Foreign-stock/FDI allocation and unavailable private-fund look-through introduce uncertainty. [SOURCE: https://www.govinfo.gov/content/pkg/CHRG-118hhrg56532/pdf/CHRG-118hhrg56532.pdf; detailed dated comparison in `equity-evidence.md`]

| Holder | Printed $bn | Normalized share |
|---|---:|---:|
| US taxable | 12,810 | 26.7181% |
| Defined benefit | 3,264 | 6.8078% |
| Defined contribution | 3,335 | 6.9559% |
| IRAs | 5,104 | 10.6455% |
| Foreign | 20,050 | 41.8188% |
| Life-insurance separate accounts | 965 | 2.0127% |
| Nonprofits | 1,961 | 4.0901% |
| Government | 456 | 0.9511% |

Printed total 47,943, row sum 47,945, discrepancy 2: normalize the printed row sum; no invented balancing cell. Shares close at 1e-12. Source numbers are re-OCRed from the pinned PDF on every run; the rendered table was independently inspected. [CALCULATION: `rents.py`]

CBO's historical 2024 CapTax CSV gives federal average marginal dividend 19.44%, short-gain 31.25%, long-gain 20.14%, death-gain 0%. They are model estimates/projections, not measured average tax paid on rent. Its profit-use dividend share is 40%; the separate retained-earnings financing share is not multiplied into this rent payout. Dividend and nondividend gains shares exhaust one dollar once. Raw accrual realization shares yield a simple eventual-tax payout proxy, **not CBO's full investment EMTR**; no deferral discount is applied. [SOURCE: pinned https://github.com/US-CBO/captax/tree/b89974934148486b6ff0423707ebb8177621d4db; category/code trace in `equity-evidence.md`]

| Tax convention | Ownership-weighted rate per dollar of after-corporate rent | Interpretation |
|---|---:|---|
| dividend_only_cash | 2.0776% | Dividend-only flow; gains/withdrawals response set zero |
| taxable_payout_no_deferral | 3.9637% | Taxable dividend plus eventual gain, undiscounted |
| taxable_plus_insurance_no_deferral | 4.4101% | Above plus insurance at its CBO marginal withdrawal rate |
| all_retirement_at_top_bracket_no_deferral | 13.4415% | Stress: all DB/DC/IRA returns taxed at highest ordinary bracket, undiscounted |

The first through third rates form **conditional calibrations**, not empirical bounds. Insurance's 22.18% rate is for life insurance/nonqualified annuities; it is not an IRA withdrawal rate. Qualified retirement withdrawal taxation is not identified: Treasury's 2016 methodology assigns individual contribution-year marginal rates and withdrawal timing, without supplying an observed 2024 average. Traditional and qualified Roth treatment differ. The stress arm uses the parsed 37% top ordinary IRS bracket on all retirement earnings; it assumes full pass-through even for DB and ignores deferral. It is not a hard effective-tax ceiling (phase-outs, state taxes and NIIT can alter rates). No retirement tax on these earnings is automatically entered as a current-year cash receipt. [SOURCE: https://home.treasury.gov/system/files/131/Distribution-Retirement-Tax-Benefits-Methodology.pdf; https://www.irs.gov/pub/irs-prior/i1040gi--2024.pdf; ASSUMPTION]

## Arms and identities

Let J be the job-key supernormal source tax, D the demand-key supernormal source tax and t the corporate rate. After-corporate rent A = φ·S·(1−t)/t. The corporate rate is 21% federal statutory or 25% **assumed combined sensitivity**; this is a taxable-rent gross-up, not a measured effective rate on economic profits. Ownership-weighted residence loss R = τA. S is J for job-key rents and D for demand-key rents. [CALCULATION; ASSUMPTION]

- Vanishing low: `Δcost = φ(J−S) − (1−e_tax)R`. Job key reduces this to `−(1−e_tax)R`.
- Vanishing high: `Δcost = −φS − (1−e_tax)R`, because the central high has already retained that source-tax slice.
- Fixed low: `Δcost = +φJ`. Fixed high: zero change; no vanished income or owner loss.
- Private after-all-tax **all-domestic claim** loss on removal: A·s_domestic−R. The annual flow is not added again as a capitalized asset-value loss. For other residents exclude e_private separately; government, nonprofits and DB require their own incidence rules.

For rents stated to scale with the US market, demand is the more directly matching **conditional** key. These papers do not identify the elasticity or whether total consumption matches corporate domestic sales. Job key suits returns tied to capital at these jobs; it is not evidence of demand-driven pure rents. Customs is used as a consumption proxy because general sales taxes are state-priced and excises include fuel re-keying. Both fill-in methods are averaged; the added people use their own age-mix consumption cells. Union/lineage demand shares: 8.1880% / 8.9554%. Mining's source tax stays fixed, so demand uses the nonmining national base 651.508. [DATA: `case_inputs.cjs` → `derived/case_inputs.json`; ASSUMPTION: proportional market rents]

| φ=1, $bn | Union jobs | Union demand | Lineage jobs | Lineage demand |
|---|---:|---:|---:|---:|
| Supernormal source tax S | 26.216 | 33.608 | 28.404 | 36.757 |
| After-corporate rent, t=21% | 98.622 | 126.429 | 106.854 | 138.278 |
| Residence loss, payout proxy | 3.909 | 5.011 | 4.235 | 5.481 |
| All-domestic claim loss upper bound | 53.471 | 68.547 | 57.934 | 74.971 |
| Household account claim loss upper bound | 41.785 | 53.566 | 45.273 | 58.586 |

Household-account claims include taxable/DC/IRA/life accounts and exclude government/nonprofit/DB. Loss passing through to claimants is assumed. The removed group's ownership and tax overlap are unmeasured; other-resident private loss ranges from zero to the displayed bound. These owner amounts are **beside the fiscal account** and cannot be published as an identified social-total correction. [GAP; ASSUMPTION; DATA: `derived/arms.csv`]

| One change, φ=1, taxable payout proxy, t=21%, e_tax=0 | Low Δ | High Δ | Low / high resulting account |
|---|---:|---:|---:|
| Vanishing, union, jobs | -3.909 | -30.125 | 313.834 / 365.686 |
| Vanishing, union, demand | -12.403 | -38.619 | 305.340 / 357.192 |
| Vanishing, lineage, jobs | -4.235 | -32.640 | 335.317 / 391.010 |
| Vanishing, lineage, demand | -13.834 | -42.238 | 325.718 / 381.411 |
| Fixed, union | +26.216 | 0.000 | 343.959 / 395.811 |
| Fixed, lineage | +28.404 | 0.000 | 367.956 / 423.649 |

All changes scale linearly with φ. Tables use φ=1 to show scale, not an estimate. `arms.csv` also contains φ=0, 0.1, 0.25, 0.5; both corporate rates, all four residence conventions, both ends, union/lineage, and cash baselines. Cash columns apply the **same assumed tax flow**; only dividend-flow or fixed-source rows are direct current-flow illustrations. Eventual-gain/insurance/qualified-withdrawal rows are not identified income-year-2024 cash corrections. All other v7 numbers stay fixed. No arm is silently stacked with another lane. [DATA: `derived/arms.csv`]

## $5bn bar, uncertainty and recommendation

| Lineage φ needed to clear $5bn | Jobs, t=21% | Demand, t=21% | Jobs, t=25% | Demand, t=25% |
|---|---:|---:|---:|---:|
| Residence-only: taxable_payout_no_deferral | 1.181 | 0.912 | 1.480 | 1.144 |
| Full low: taxable_payout_no_deferral | 1.181 | 0.361 | 1.480 | 0.393 |
| Residence-only: taxable_plus_insurance_no_deferral | 1.061 | 0.820 | 1.331 | 1.028 |
| Full low: taxable_plus_insurance_no_deferral | 1.061 | 0.346 | 1.331 | 0.378 |
| Residence-only: all_retirement_at_top_bracket_no_deferral | 0.348 | 0.269 | 0.437 | 0.337 |
| Full low: all_retirement_at_top_bracket_no_deferral | 0.348 | 0.186 | 0.437 | 0.216 |

Values >1 cannot clear within φ∈[0,1] under that calibration. **Fixed rents clear at φ>0.176;** the existing φ=1 control is +28.404 / 0. Job-key residence-only losses stay below $5bn in the dividend/payout/insurance calibrations. Demand-key payout loss can clear at a large φ with t=21%; its source-key correction also matters. The top-bracket retirement stress clears sooner but is not measured and is not a current-year cash correction. Vanishing high clears for much smaller φ because it changes the source-tax premise as well. The bar verdict is conditional, not proof of the actual correction. [DATA: `thresholds.csv`]

Job-key union corporate SE comes from the existing lane's 160 CPS replicate weights; it propagates linearly conditional on φ, rates and ownership. For the φ=1 payout/t=21% job change its low/high SE is 0.144 / 1.110bn. The lineage's reported SE holds added-person taxes fixed and is only the union contribution. Exact v7 demand/owner joint replicates are not preserved here: no invented lineage/demand SE, no combining unrelated survey SEs as if independent. φ, ownership transfer, tax-rate and counterfactual uncertainty dominate and are not sampling SEs. [DATA: source `items.csv`; CALCULATION: `rents.py`]

**Recommendation:** Keep the low end explicitly conditional on replacement worldwide after-tax returns; the requested literature supports risk/intangible components being included in taxable supernormal returns but does not establish that all are replaceable. Correct the premise now, retain these arms beside the frozen case, and do not choose a numerical φ from incompatible historical residuals. If the parent instead means pure rents disappear with demand, adopt that counterfactual explicitly and recompute source taxes, retained-owner residence taxes and private claims together, with ownership exclusions. [INFERENCE; FRAMING-SENSITIVE]

Exact replacement decision wording:

> The low end assumes that the capital serving the group's jobs, including risk compensation and returns to reproducible or expensed intangibles, leaves the US tax base while its resident owners obtain replacement investments yielding the same worldwide after-tax income. Corporate source taxes therefore respond at one, while residence-based capital income and taxes remain unchanged. This is a full-adjustment assumption, not an estimate that pure rents scale with US demand. The pure-rent share and its removal response are unmeasured; fixed-rent and vanishing-rent readings are reported separately, with retained-owner taxes and owner losses under stated ownership rules.

This preserves the payload's actual rule; it does not imply Treasury measured replacement returns or a removal response. The high end's normal-return-only tax loss is also a restrictive premise: the excluded slice includes mobile risk/intangible returns as well as possible rents. [SOURCE: frozen `item_job_capital.cjs:272–283`; INFERENCE]

## Gates, reproduction and review

- 24 frozen-v7 controls: live set/cash central, corporate union/lineage, existing φ=1 fixed-rent arm, consumption conservation, population conservation and frozen upstream pins.
- 390 calculation gates: primary-source pins and extraction, national nonmining closure at 1e-6bn, corporate/source and private-tax partitions at 1e-9bn, ownership/payout conservation at 1e-12.
- Fourteen tests cover no-rent controls, source rekeying, tax/private partition, fixed high premise, invalid parameters, both-rate threshold coverage and owner scope.
- [Code review](review-evidence.md): conditional arithmetic passed; retained-owner fiscal scope finding addressed by explicit e_tax=0, overlap endpoint, e_private upper bounds and institutional-scope naming. No actual overlap amount is claimed.
- Raw `_cache/` downloads and scratch scripts remain ignored. `inputs/pins.json` freezes exact bytes and original URLs; `acquire.py --download` retrieves missing primary files and stops on drift. No Git writes, frozen edits or adoption.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/corporate_rents_2026_10_14/acquire.py --download
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/corporate_rents_2026_10_14/measured_run.py sh infra/immigration-fiscal/corporate_rents_2026_10_14/run_all.sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/corporate_rents_2026_10_14 "uv run --no-project python3 {lane}/measured_run.py sh {lane}/run_all.sh"
```

Tools: Node, Poppler, ImageMagick, Tesseract, the repo uv Python environment. Python `perf_counter` and `getrusage` measure runtime/RSS; volatile metrics stay in `_cache/run_metrics.json`. No ps, sysctl or `/usr/bin/time -l`. Source CSV writers use LF. Quantitative bias self-check: accounting and population held fixed; no empirical φ invented; incompatible denominators not averaged; owner scope and measured/modelled/assumed status labelled; sensitivity displayed symmetrically. LLM post-training can bias framing; primary-file extraction and the disconfirmation columns constrain, but do not remove, that instrument limitation.

## Work log (date output, JST)

- 2026-10-14 22:50:45+09:00 — primary-source parsing and exact v7 input trace underway.
- 2026-10-14 23:00:52+09:00 — 36 pins, 24 frozen controls, 390 calculation gates and 12 initial tests passed; measured run 4.314s and peak child RSS 228.62MiB, exit0.
- Code review resolved retained-owner scope; final tests expanded to 14. The initial pytest calls appended this lane's node IDs to the repo's ignored `.pytest_cache/v/cache/nodeids`; subsequent checks isolate their cache inside this lane. That incidental path is included in the changed-path manifest for the parent.
- Final reproduction receipt and changed-path list are recorded in `validation.md` and `changed-paths.txt`; neither is an adoption or commit claim.
