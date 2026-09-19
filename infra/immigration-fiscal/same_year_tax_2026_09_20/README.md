# Matched-year tax and earnings checks

Uncalibrated checks of CPS ASEC 2024 income-2023 against IRS/SSA 2023, and common-definition ACS 2024 versus CPS ASEC 2025 income-2024 wages. No fiscal-ledger parameter is changed. Dollar amounts below are billions of the stated year's dollars. These comparisons test aggregate components and survey distributions; they do not identify Mexican-origin administrative taxes or an immigration policy effect.

## Findings

| Income-2023 metric, civilian CPS | CPS | Administrative comparator | Raw difference |
|---|---:|---:|---:|
| Gross wage dollars / SSA AWI underlying compensation | 11,105.609 | 11,103.241 | +0.021% |
| Wage recipients, millions / SSA AWI recipients | 163.093 | 173.671 | −6.091% |
| OASDI wage base, all-covered proxy | 9,779.053 | 9,290.622 | +5.257% |
| OASDI self-employment base proxy | 450.457 | 484.640 | −7.053% |
| HI wage base, all-covered proxy | 11,105.609 | 11,254.976 | −1.327% |
| HI self-employment base proxy | 577.880 | 788.217 | −26.685% |
| Modeled tax returns, millions | 157.202 | 160.602 | −2.117% |
| AGI | 14,315.849 | 15,286.017 | −6.347% |
| Federal income tax before refundable credits | 1,819.018 | 2,108.587 | −13.733% |

[CALCULATION: `derived/ssa_comparisons.csv`, `irs_national.csv`; source URLs below.] SSA state-table comparisons subtract Puerto Rico and other/unknown from the all-area total for the national comparison; the AWI comparator remains all-area. Neither matches all CPS scope features. CPS all-survey-person tax liability is $1,825.981bn, −13.403% versus IRS; civilian restriction explains only $6.963bn of that comparison. Three scopes are exported, including civilian private households.

The federal-tax shortfall is concentrated in the upper income tail. Among modeled returns with AGI at least $500,000, CPS produces $431.160bn versus IRS $920.936bn, a $489.776bn shortfall. Below $500,000, CPS exceeds IRS by $200.207bn. Return counts, AGI and liabilities are above IRS in the $100,000–$500,000 range. This is a distributional discrepancy; it does not establish whether reporting, imputation, disclosure treatment, filing-unit modeling, tax modeling, or scope explains it. Applying the national −13.733% difference proportionally to Mexican-origin taxes is unsupported. [CALCULATION/INFERENCE: `irs_bracket_summary.csv`; all 19 source AGI bands also exported.]

**An earlier IRS benchmark was misdated.** Publication 4801, revised June 2026, describes its p.9 confidence-interval table as 2023, but the wages $9,738.950972bn and after-credit tax $2,098.923017bn exactly reproduce the downloaded **2022** complete tables. The same publication's 2023 p.15 wages/AGI agree with the **2023** complete tables: wages $10,204.095705bn, AGI $15,286.017359bn. The 2023 tax anchor is $2,108.587001bn. This is an internal publication inconsistency, not evidence that the two intended estimands differ by filing scope. Use the pinned year-specific complete tables. The mechanism of the publication error is unconfirmed. [SOURCE: [2022 Table 1.2](https://www.irs.gov/pub/irs-soi/22in12ms.xls), [2022 Table 1.4](https://www.irs.gov/pub/irs-soi/22in14ar.xls), [2023 Table 1.2](https://www.irs.gov/pub/irs-soi/23in12ms.xls), [2023 Table 1.4](https://www.irs.gov/pub/irs-soi/23in14ar.xls), each all-returns-total row; [Publication 4801](https://www.irs.gov/pub/irs-pdf/p4801.pdf), printed pp.9,15.]

## Independent wage-distribution corroboration

Common scope is civilian private-household residents; wage-earner means and quantiles require positive annual wage income. Both surveys' official replicate weights are used for totals, means, band shares, and within-survey target/complement ratios. Ratios retain the covariance between numerator and denominator.

| National 2024 wage measure | ACS | CPS |
|---|---:|---:|
| Mexican self-ID mean per earner | $48,216 | $51,520 |
| Other self-ID mean per earner | $69,683 | $75,042 |
| Ratio, Mexican self-ID / complement | .6919 | .6866 |
| Ratio 95% sampling interval | .6867–.6972 | .6649–.7082 |
| Mexican self-ID median per earner | $38,173 | $40,000 |
| Mexico-born mean per earner | $46,724 | $47,480 |
| Ratio, Mexico-born / complement | .6851 | .6458 |

The broad self-ID relative gap is corroborated, including Texas (.6501 ACS / .6491 CPS); California is .5512 / .5738. The birthplace-only national gap is smaller in ACS, so agreement is not universal. ACS self-ID wages total $891.587bn versus CPS $979.421bn (−8.968%); mean differences and recipient counts both matter. All ACS wages are −5.153% versus CPS. Neither survey is an administrative gold standard. [CALCULATION: `wage_distributions.csv`, `acs_cps_comparison.csv`.]

ACS uses rolling prior-12-month income, adjusted with `ADJINC`; CPS uses calendar 2024. Sampling intervals do not resolve reporting, timing, coverage or topcoding. Quantiles are weighted point estimates without sampling intervals. ACS lacks the parental birthplace fields needed to reproduce the canonical 40.896574m Mexican-origin union, so the narrower self-ID and Mexico-born groups are shown separately and as a union. No G3/G4 inference or causal assimilation result is claimed. [SOURCE: [ACS 2024 PUMS documentation](https://www.census.gov/programs-surveys/acs/microdata/documentation.html), held 2024 dictionary; CPS dictionaries.]

## Tax units and concept bridges

`TAX_ID` is the native Census tax-unit identifier. The dictionary places AGI/tax dollars on a tax-unit head or dependent filer. The implementation selects the unique nonzero tax/AGI carrier in each filing unit, plus each observed dependent filer; it never assumes the first spouse carries tax dollars or invents an identifier. It finds 61,674 core payload-bearing units, 3,511 dependent filers, and 560 additional zero-payload filing units in the 2024 sample. All tax/AGI totals are conserved. All 560 zero-payload units have zero wages and identical member weights, including replicates. One mixed civilian/Armed Forces unit creates a 2,693-return difference between alternative scoped head selections, with zero tax-dollar effect. That count bound is explicit in `audit.json`; the first-member convention is used only for these zero-income counts. These are modeled returns, not observed IRS filings. [SOURCE: 2024 dictionary pp.6C-31–32; CALCULATION.]

IRS returns include filers beyond the civilian household survey, and exclude nonfilers. Its taxable wages differ from CPS gross wages; the IRS 2023 total-wage value $10,204.096bn also differs from its W-2 wage amount $10,046.008bn. `return_wages` sums spouses' wages inside the native tax unit, excludes a dependent's own wage from that parent sum, then uses the carrier's survey weight. It is therefore distinct from person-weighted national wage income. Neither wage concept is silently substituted for the other. Federal before-refundable liability is compared to IRS income tax after nonrefundable credits; after-refundable CPS liability is exported without an invalid IRS comparison. FICA, cash collections, and income-tax liability are separate quantities.

The statutory OASDI proxy applies the 2023 $160,200 cap to wages, then remaining cap to `0.9235 * max(business+farm profit,0)` if at least $400. HI is uncapped. This is explicitly an all-covered proxy, not measured eligibility. Government exemptions, other coverage exceptions, pretax benefits, multiple employers, additional Medicare tax, and CPS/SSA annual-population differences remain unresolved. Longest-job government classification `WECLW=6` is verified in the held 2024 dictionary. It does not identify coverage of every annual job. [SOURCE: [SSA contribution base](https://www.ssa.gov/oact/COLA/cbb.html), [2023 Schedule SE](https://www.irs.gov/pub/irs-prior/f1040sse--2023.pdf), [SSA 2025 Supplement, Tables 4.B10/4.B12 and notes](https://www.ssa.gov/policy/docs/statcomps/supplement/2025/4b.html), [AWI underlying data](https://www.ssa.gov/oact/cola/awidevelop.html).]

SSA's tables are preliminary 1% CWHS estimates, with rounded worker counts and dollar amounts, mostly assigned by residence and with employer-location fallback. Wage and self-employment workers overlap. OASDI wage entries do not net multiple-employer refunds. Subtracting Puerto Rico and other/unknown does not remove institutional residents, military personnel, deaths/emigration before survey, or align compensation definitions. Worker-count and dollar differences therefore are diagnostics, not identified measurement errors.

**Supported annual-ledger correction from this lane: none identified.** Applying zero is a decision not to extrapolate an unmeasured ethnic adjustment, not proof that true bias is zero. The existing 2024 target's modeled employer OASDI on wages of people whose longest job was government is $8.207bn personal allocation / $9.183bn shared. Setting all those selected wages exempt gives an extreme component sensitivity of that size; it is not an estimated correction, nor a bound on all payroll error. Employee FICA cannot simply be reduced by the same number. These sensitivities are exported with `applied_correction=0`.

## Reproduce, provenance and validation

From the canonical repository, set `lane` to the absolute lane directory; raw and derived directories are ignored. Public downloads are fingerprint-locked. Existing CPS 2024 is probed at `sources/immigration-fiscal/data/census/cps_asec_2024_march.zip`; the live download and that archive have the identical SHA256 `cdb39cdac34bef99dd0940ab28e306f692404c2eea44d85dfd634214872a0a09`. A previously used local-cache probe missed this legacy filename. The new acquisition entrypoint reuses it. Source locking fails loudly if bytes drift.

```sh
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 "$lane/acquire.py" --raw "$lane/_cache" --source-root /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy --with xlrd python3 "$lane/builder.py" --source-root /Users/alien/Projects/immigration-research
OPENBLAS_NUM_THREADS=1 VECLIB_MAXIMUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy python3 "$lane/acs_check.py" --source-root /Users/alien/Projects/immigration-research
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas python3 "$lane/summarize.py"
UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --offline --no-project --with pandas --with numpy --with xlrd python3 -m unittest discover -s "$lane" -p 'test_*.py' -v
```

Nine tests cover tax-carrier/spouse/dependent construction, zero-income head and scope ambiguity, invalid carriers, cap/loss/self-employment arithmetic, income-band endpoints, weighted quantiles, SDR variance, source drift, and independent IRS year anchors. Full builds check person/household/replicate joins, exact credit identity, national/target/rest conservation, complete AGI partitions, official source units and totals, raw ACS row count, and all replicate partitions. The field reader uses the actual 2024 ACS `STATE` column. Early validation found and repaired a pandas-Series assertion incompatibility and the obsolete `ST` assumption; tax-unit guards exposed the documented zero-income ambiguity instead of dropping those filers.

`source_lock.json` records downloaded source URLs and hashes. `ssa_sources.json` contains manually transcribed primary values after direct HTTP requests returned 403; the primary SSA pages were read through the web tool. There is no inferred or secondary-source fallback. The two audit files fingerprint raw inputs, generators and outputs. Sampling SEs use 160 CPS or 80 ACS successive-difference replicates, factor `4/R`; no combined source/model confidence interval is claimed.

Restricted CPS–SSA/IRS linkage, imputation-error decomposition, detailed job-by-job coverage, and causal tax attribution are not implemented: the public files do not identify those administrative components. The national earnings and tax discrepancy is now located sufficiently to reject a uniform calibration. No external contact or restricted linkage occurred.
