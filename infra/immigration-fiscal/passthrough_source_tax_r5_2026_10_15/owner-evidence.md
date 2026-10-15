# Owner tax evidence for item 19

**Verdict:** Published SOI supports reproducible, form-specific allocations of federal tax by owners' AGI. It does not identify the marginal tax on this capital, its foreign replacement route, a national state-source rate, or its normal-return fraction. These inputs provide conditional arms with explicit missing central values. Counting a net source-tax loss reduces the case's fiscal cost. [CALCULATION: `owner_tax_sources.py`; INFERENCE]

## Federal owner rates

The inputs reuse the register's `same_year_tax_2026_09_20` official TY2022/2023 Table 1.2 and Table 1.4 workbooks, copied into `_cache/owner/` and independently SHA-256 checked. Table 1.4 separates positive and negative Schedule C, partnership and S-corporation income by AGI. Table 1.2 supplies all-return tax after credits and total income tax for the same bins. Money is nominal dollars in thousands. [SOURCE: [SOI tables](https://www.irs.gov/statistics/soi-tax-stats-individual-statistical-tables-by-size-of-adjusted-gross-income); DATA: `inputs/owner_source_pins.json`]

For each positive-AGI bin b, a_b = tax_b/AGI_b. The positive-income arm for form f is sum_b positive_income_fb*a_b / sum_b positive_income_fb. The signed-net arm replaces positive income with positive income minus reported losses in both sums. The nonpositive-AGI bin has no usable AGI denominator; its income and losses are disclosed, excluded from both sums, and never assigned a fabricated zero rate. Separate positive and loss column sums must reproduce the source totals within rounding. [CALCULATION: `extract_year()` → `inputs/owner_agi_rates.json`]

| Form | 2023 positive / net, after credits | 2023 positive / net, total income tax | 2022 positive / net, after credits |
|---|---:|---:|---:|
| Schedule C | 11.2013% / 12.1064% | 11.3676% / 12.2906% | 11.6140% / 12.2894% |
| Partnership | 22.1634% / 22.7889% | 22.8913% / 23.5013% | 22.2466% / 22.7928% |
| S corporation | 21.8098% / 22.3095% | 22.5399% / 23.0617% | 21.8977% / 22.3504% |

[CALCULATION: `inputs/owner_agi_rates.json` `years[].by_form`]

These are income-weighted **all-return bin tax allocations**. They are not tax calculated on linked owners with and without business income. They mix within-bin owners and nonowners, allocate taxation of other income to this income, reflect existing deductions/credits, and do not isolate capital from owners' labor or differences by industry. Applying them to 2024 industry operating profits assumes transfer across year, income definition and industry. Schedule E individual distributions do not identify the tax status of all ultimate partnership owners; multiplying the complete Form 1065 base by an individual rate requires an additional ownership assumption. The JSON marks the central rate null and excludes self-employment tax/state taxes. [INFERENCE; GAP]

For a different, historical estimand, Cooper et al.'s Treasury WP104 reports 2011 federal tax changes from removing business income while other income stays fixed: partnership 15.9%, S corporation 24.9%, sole proprietor 13.6% (printed p4; sector comparisons in Figures 7–9). Their partnership tracing includes nonindividual owners and assumptions for unresolved ownership; preferred income and heterogeneous owner types help explain its lower rate. Those data predate TCJA and section 199A. `owner_historical_rates.json` preserves these as historical sensitivity inputs, without calling them 2024 rates or equating their all-income denominator with operating capital profit. [SOURCE: [Treasury WP104](https://home.treasury.gov/system/files/131/wp-104.pdf)]

## Replacement income: US loss is source tax less retained US tax

Let I be the capital-income amount, tau the allocated US rate, d the domestic replacement share, c the fraction of tentative US tax on foreign replacement extinguished by FTCs, and q foreign pre-tax replacement income divided by source income. Assuming domestic replacement has identical taxable income and US rate, the conditional US loss is **I*tau*(1-d)*(1-q*(1-c))**. Domestic replacement cancels exactly. d and c have endpoint arms 0/1; q must be supplied. q=1 is an unchanged-pre-tax-income convention, not generally an equal-worldwide-after-tax-income assumption. [CALCULATION: `direct_replacement_loss`; INFERENCE]

`direct_equal_after_tax_loss` offers a separate proportional-tax arm: if the foreign tax rate f applies to the same base and is fully creditable up to tentative US tax, combined tax is max(tau,f), q=(1-tau)/(1-max(tau,f)), c=min(1,f/tau). It holds worldwide after-tax income equal. Deductions, credit limits, different tax bases, preferential income rates and carryovers can break this simple bridge. No distribution of d, c, q or f is measured here. [CALCULATION; ASSUMPTION]

The 2024 individual FTC is category-limited by foreign taxable income relative to total taxable income. Foreign taxes passed through by partnerships/S corporations use Schedule K-3 information. An individual CFC shareholder cannot automatically use the CFC's taxes as direct credits; section 962 introduces separate corporate-rate inclusion tax and potentially deemed-paid credits. [SOURCE: [Publication 514 (2024)](https://www.irs.gov/pub/irs-prior/p514--2024.pdf), printed pp9–10,18,21]

For a corporation or eligible section-962 elector, `gilti_current_us_tax(T,G,F)` separates the 2024 mechanics: T=sum positive pro-rata tested incomes after foreign tax; G=actual GILTI inclusion; F=pro-rata tested foreign taxes. Form 1118 Schedule D II gives inclusion fraction a=G/T; column 3 gives **full** assigned tax H=aF; column 4 gives the **80%** eligible credit. Section 78 gross-up is H, not 0.8H. [SOURCE: [Form 1118, Dec2022 revision](https://www.irs.gov/pub/irs-prior/f1118--2022.pdf), p4; [Dec2023 instructions](https://www.irs.gov/pub/irs-prior/i1118--2023.pdf), printed pp17–18; CALCULATION]

With an unrestricted 50% section-250 deduction, tentative US tax is .21*.5*(G+H); allowed FTC is min(.8H,tentative,applicable 904 limit). The helper allows a lower effective deduction share and additional FTC limit. The section-250 deduction is taxable-income-limited; it applies to domestic C corporations and eligible 962 electors, not automatically to S corporations. [SOURCE: [2024 Form8993 instructions](https://www.irs.gov/pub/irs-prior/i8993--2024.pdf), pp1,5; [.21 statutory calculation on Form1120](https://www.irs.gov/pub/irs-prior/f1120--2024.pdf), p1]

G cannot be set to all replacement profit without specifying tested losses, QBAI, interest and exclusions; it comes from Form8992. The helper does not infer a CFC route, QBAI, ownership, later distributions, shareholder residence taxes or state taxation. Retained current US CFC tax offsets the source loss and must not be counted again under item9. [SOURCE: [2024 Form8992 instructions](https://www.irs.gov/pub/irs-prior/i8992--2024.pdf); INFERENCE]

Examples per $100 pre-foreign-tax profit, no QBAI/losses/other expenses, complete inclusion: F=0,T=G=100 gives US10.5; F=10,T=G=90 gives gross-up10, tentative10.5, FTC8, US2.5; F=15,T=G=85 gives US0 after FTC limit. These are arithmetic demonstrations of a stipulated route, not estimated replacement tax rates. [CALCULATION: `gilti_current_us_tax`]

## State source taxes

National source-state liability and its replacement offset remain unidentified. A zero additional correction means withheld measurement, never measured absence of tax. California's fixed **2024** Form3804 instructions illustrate an elective PTE payment of 9.3% of qualified net income, paired with a credit against owners' personal income tax; this is not an extra 9.3% tax on top of the owner's complete tax or a national upper bound. [SOURCE: [2024 FTB3804 instructions](https://www.ftb.ca.gov/forms/2024/2024-3804-instructions.pdf), p1]

IRS Notice2020-75 allows qualifying state/local PTE income-tax payments as deductions in non-separately stated federal income. Thus adding a modeled state liability can require a federal-base adjustment and reconciliation with state owner credits and the account's existing receipts. Geographic job shares do not identify the owners' residence/source nexus or elective take-up. The JSON preserves the CA legal example and an explicit withheld-state arm; it does not supply an invented national state rate. [SOURCE: [Notice2020-75](https://www.irs.gov/pub/irs-drop/n-20-75.pdf); INFERENCE; GAP]

## Normal return versus owners' labor

Smith et al.'s QJE TableIV and discussion (printed pp46–47) average six owner-death/retirement impacts across top1%, million-dollar and top0.1% owners: 76.8%, rounded to a75% labor calibration. The million-dollar owner-death and retirement impacts are81.6% and82.5%. Death analysis uses S corporations/partnerships, owners≤64 with≥20% ownership, deaths2005–2010, substantial prior sales/employment, matched comparison firms; the million-dollar sample has765 treated firms. Sole proprietors and a representative 2024 all-income population are not the identified target. [SOURCE: [QJE author PDF](https://eml.berkeley.edu/~yagan/Capitalists.pdf), TableIV, sectionsIV.A–B]

The remaining25% contains physical capital, transferable intangibles and market-position returns. It cannot identify the normal/supernormal split within capital. Applying75% labor outside the historical top-owner sample is a calibration arm. Copying C-corporation .37 would add another unsupported transfer. An r*K normal-income arm is transparent if r, K, timing, debt/equity and taxable/economic depreciation conventions are specified; accounting assets alone do not measure the expensing-counterfactual share of taxable profits. This component supplies normal-share endpoints0/1 and leaves its central value null. [INFERENCE; GAP]

The Federal Reserve Board's annual H.15 series `RIFLGFCY10_N.A` directly reports nominal 10-year Treasury yields of **2.95% in 2022**, **3.96% in 2023**, and **4.21% in 2024**. `extract_normal_yield()` reads these observations from the pinned official table into `owner_normal_yield.json`; it does not average rounded monthly yields. [SOURCE: [Federal Reserve annual series](https://www.federalreserve.gov/datadownload/Preview.aspx?pi=400&preview=H15%2FH15%2FRIFLGFCY10_N.A&rel=H15)]

For the requested diagnostic, the proposed high-end rule on frozen TY2022 inputs is normal-income proxy = min(max(capital profit,0), .0295*max(book net equity,0)), separately by industry and S corporation/partnership form. Its tax follows that proxy through the same explicit owner-rate and replacement-income arms. Exclude Schedule C when no comparable equity stock is available. Using .0421 with the same frozen book inputs is a separate rate sensitivity. This is a **conditional tax-book proxy**, not an observed normal fraction: historical book equity can diverge substantially from market-value capital, year-end stocks differ from annual averages, and depreciation, expensing, risk, intangibles and negative equity require explicit conventions. [ASSUMPTION; INFERENCE]

## Reproduction and checks

Run `uv run --no-project --with xlrd python3 infra/immigration-fiscal/passthrough_source_tax_r5_2026_10_15/owner_tax_sources.py`. `--acquire` fills missing cache files and requires recorded SHA-256/size/URL matches for known pins. Existing sources use the local register entry; later official forms/papers total under10MB. PDF/OLE signatures reject HTML error pages. Cache≥10GB and disk<100MB stop acquisition. [CALCULATION: script guards]

Initial acquisition of nonexistent `i1118--2024.pdf` failed404. The official prior-year inventory establishes the operative Dec2023 instructions/Dec2022 form; both are now pinned and used, with no current-2025-law substitution. Regression checks cover full gross-up versus80% credit, domestic cancellation, all-foreign full-credit loss, zero-credit cancellation, positive-income source totals, headers, years, bin AGI parity, and byte-identical offline regeneration. Parent owns the integrated lane tests/rerun. [SOURCE: [IRS prior-year inventory](https://www.irs.gov/prior-year-forms-and-instructions?find=Instruction%201118); CALCULATION]

Measured acquisition+extraction:9.47s, peakRSS52,527,104 bytes on macOS; added CA2024/1120 sources+build2.53s,45,989,888 bytes. Timings use `perf_counter`/`getrusage`, not `/usr/bin/time -l`. [CALCULATION: command output2026-10-15]

H.15 acquisition+build completed 2026-10-15 02:28 UTC in 0.99s, peak RSS 46,153,728 bytes. [CALCULATION: command output]
