# Low-Skill Immigration: economist matrix, omitted channels, and data status

Date: 2026-04-10

## Core conclusion

The Clark Center poll is not a full-spectrum welfare ledger. It is a panel of economists answering a broad question about whether the average US citizen would be better off from more legal low-skilled immigration. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]

For this question, the strongest "agree" responses mostly do one of two things:

1. Lean on general-equilibrium intuition about gains from trade, complementarities, or cheaper services. [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/]
2. Lean on adjacent empirical channels such as safety-net use, child outcomes, or labor-market adjustment, rather than a full accounting of local schooling, congestion, housing, and descendant performance. [INFERENCE]

I did not identify a comprehensive low-skill-immigration local-cost ledger authored by the strongest Clark "agree" respondents in this pass. That is not proof of absence. It is a statement about what I could actually locate and tie to this exact policy question. [INFERENCE]

The best comprehensive benchmark I found remains the National Academies fiscal-impact framework. It already includes federal and state/local taxes and benefits, and it explicitly includes descendants. It does not look like a complete pricing of traffic congestion or a full housing-incidence welfare decomposition. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf]

## DuckDB clarification

Yes, the ACS work used DuckDB. But the distinction matters:

1. We used DuckDB as the query engine over flat files such as `/Volumes/SSK1TB/corpus/census_acs/csv_pus.csv`. [DATA: /Volumes/SSK1TB/corpus/census_acs/csv_pus.csv]
2. At the start of this pass, I did not find a preexisting immigration-focused `.duckdb` database file in this repo or in the immigration/census corpus paths I checked. [DATA: local filesystem search on 2026-04-10]
3. This pass adds a derived warehouse at [immigration_context.duckdb](sources/immigration-fiscal/data/derived/immigration_context.duckdb), built by [build_immigration_context_duckdb.sql](sources/immigration-fiscal/data/derived/build_immigration_context_duckdb.sql). [DATA]
4. The preexisting `.duckdb` files I did find on the SSD were FERC energy/regulatory datasets, not immigration datasets. [DATA: /Volumes/SSK1TB/corpus/ferc_eqr/ferc1_raw/ferc1_xbrl.duckdb; /Volumes/SSK1TB/corpus/ferc_regulatory/pudl_release/ferc1_xbrl.duckdb]

So the precise statement is:

- `DuckDB engine in use`: yes.
- `Preexisting immigration DuckDB already present`: no.
- `Derived immigration DuckDB now created in this repo`: yes.

### Local data footprint relevant to this question

1. `sources/immigration-fiscal/data/census`: about `950M`. [DATA: local `du -sh` on 2026-04-10]
2. `/Volumes/SSK1TB/corpus/census_acs`: about `1.1G`. [DATA: local `du -sh` from prior measurement in this project]
3. `/Volumes/SSK1TB/corpus/census_acs_tables`: about `1.3G`. [DATA: local `du -sh` from prior measurement in this project]
4. `/Volumes/SSK1TB/corpus/census_cps`: about `116M`. [DATA: local `du -sh` from prior measurement in this project]
5. `/Volumes/SSK1TB/corpus/dot_transport`: about `562M`. [DATA: local `du -sh` from prior measurement in this project]

That gives a public-data footprint of roughly `4.0G` touching this question, though some files are overlapping or complementary rather than additive. [INFERENCE]

### New derived warehouse

The warehouse created in this pass is intentionally narrow and state-level rather than pretending to be a county-grade causal panel.

Current components:

1. ACS 2023 low-skill working-age state summaries from `/Volumes/SSK1TB/corpus/census_acs/csv_pus.csv`. [DATA]
2. FHFA state purchase-only house price index data from `https://www.fhfa.gov/hpi/download/quarterly_datasets/hpi_po_state.txt`. [SOURCE]
3. Census 2023 school-finance district rows rolled up to state totals from `https://www2.census.gov/programs-surveys/school-finances/tables/2023/secondary-education-finance/elsec23t.txt`. [SOURCE]

Derived objects in the DuckDB:

1. `state_dim`
2. `fhfa_hpi_state`
3. `fhfa_state_2023q4`
4. `school_finance_district_2023`
5. `school_finance_state_2023`
6. `acs_low_skill_state_2023`
7. `state_context_2023`

I did not include BLS LAUS in the warehouse yet because the public flat files returned HTML traps to plain `curl`. That is an acquisition problem, not a modeling choice. [DATA] [INFERENCE]

## Is our analysis more refined than what an economist could do a year ago?

No, not in the strong causal-identification sense.

Top immigration economists, the National Academies, CBO-style fiscal modelers, and researchers using restricted Census or IRS/SSA-linked data already had stronger identification and, in some cases, better data than we do here. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf]

What is more refined here is the data-engineering workflow:

1. Fast joins across local public files.
2. Reproducible sensitivity analysis in one workspace.
3. Immediate comparison of survey claims against channel-specific papers.
4. Faster inspection of what is omitted from a given estimate.

So the honest statement is:

1. Our workflow is probably more flexible than a survey answer or op-ed. [INFERENCE]
2. It is not obviously more causally credible than the best academic/admin-data literature. [INFERENCE]

## Updated lever count

The old short list was an `8-ish` methodological frame. The working model is now better treated as `12` levers, because several local channels need to be separated instead of being hidden inside one fiscal bucket. [INFERENCE]

### The 12 levers

1. Wage substitution vs task complementarity.
2. Consumer price effects for labor-intensive services.
3. Federal tax and transfer incidence.
4. State/local education, health, and welfare incidence.
5. Descendant assumptions: child and grandchild mobility, taxpaying, and transfer use.
6. Public-goods attribution rules.
7. Time horizon and discount rate.
8. Legal status and program-eligibility assumptions.
9. Traffic and congestion externalities.
10. Housing-market incidence vs real deadweight loss.
11. Informal-economy effects, tax leakage, and labor-standards erosion.
12. Political-economy and social-friction spillovers.

The important change is that schooling and descendants are not "missing" from the NAS-style fiscal framework, but congestion and a clean housing welfare treatment mostly are. [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf; SOURCE: https://doi.org/10.1016/j.jue.2006.07.004]

## Recent papers and posts that change how to read the data

These do not all have the same epistemic weight. I am separating papers and official reports from Substack-style prompts.

### Higher-weight papers and official reports

1. Colas and Sachs, *The Indirect Fiscal Benefits of Low-Skilled Immigration*. Main point: the standard direct fiscal ledger misses indirect fiscal gains operating through resident wages, labor supply, and tax payments. Their empirical U.S. estimate is roughly `$750` per low-skilled immigrant per year in indirect fiscal benefit, with a larger range under alternative model choices. This does not erase all direct low-skill costs, but it is exactly the kind of omitted positive channel that makes a one-line "low-skill immigrants are a fiscal burden" statement too crude. [SOURCE: https://www.econstor.eu/bitstream/10419/282044/1/352.pdf]
2. CBO, *Effects of the Surge in Immigration on State and Local Budgets in 2023* (June 2025). Main point: for the 2021+ immigration surge, state/local budgets were net negative in 2023 even after including higher taxes and broader economic effects. CBO explicitly counts crowded classrooms and more crowded public transportation in its broader "potential effects" measure. This matters because it is one of the cleanest recent official acknowledgments that local crowding costs are real and do belong in the ledger. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. Vigdor, Bier, and Howard, *Immigrants, Housing Wealth, and Local Government Finances* (Cato, April 2025). Main point: fiscal studies that ignore the capitalization of immigration into property values miss a real local-revenue channel. I do not treat their headline magnitudes as settled, but the analytical move is important: if immigration raises housing values in constrained places, it can also raise property-tax collections and homeowner wealth. [SOURCE: https://www.cato.org/briefing-paper/immigrants-housing-wealth-local-government-finances]
4. Orrenius, Viard, and Zavodny, *The Fiscal Impact of Immigration: An Update* (AEI, September 2025). Main point: high-skill immigrants drive the average positive fiscal result, low-skill immigrants remain net negative on direct accounting, but recent work on indirect fiscal effects shrinks or partly offsets the low-skill burden. This is a useful synthesis because it explicitly recognizes the federal/state-local split and the newer indirect-effects literature. [SOURCE: https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf?x97961=]
5. Edelberg, Veuger, and Watson, Brookings update on immigration flows (January 2026). Main point: do not use the CPS to infer recent changes in the foreign-born population level because the CPS uses fixed population controls. This is one of the most important data-science warnings in the new commentary layer: some highly circulated immigration charts are methodologically invalid before any ideological debate even starts. [SOURCE: https://www.brookings.edu/articles/macroeconomic-implications-of-immigration-flows-in-2025-and-2026-january-2026-update/]

### Lower-weight but useful prompt sources

1. Daniel Di Martino, *No, More Immigration Won’t Fix the Federal Budget* (February 20, 2026). Useful not because it settles the issue, but because it sharpens the audit questions: individual versus household attribution, treatment of U.S.-born children, public-goods allocation, and the timing problem of counting prime-age tax years before old-age benefits come due. [SOURCE: https://substack.com/home/post/p-188402226] [FRAMING-SENSITIVE]
2. Aporia, *Externalities from low-skilled migration* (July 2, 2025). Low reliability as a scientific source, but useful as a prompt list for channels the mainstream fiscal literature often leaves thinly priced: automation delay, culture/trust claims, household-level welfare attribution, and second-order local externalities. Those claims need separate verification before use. [SOURCE: https://www.aporiamagazine.com/p/externalities-from-low-skilled-migration] [FRAMING-SENSITIVE]

## New ways to understand the data

The recent literature suggests at least six better cuts than the usual "net fiscal effect" one-number fight.

1. Split direct from indirect fiscal effects. The newest important positive channel is not just taxes paid by immigrants themselves; it is taxes paid by others because labor markets and capital returns adjust. [SOURCE: https://www.econstor.eu/bitstream/10419/282044/1/352.pdf]
2. Split federal from state/local. The federal ledger can be positive while the state/local ledger is negative. That is not a contradiction; it is an incidence mismatch. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf; SOURCE: https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf?x97961=]
3. Split renters from homeowners. Housing-price effects are partly a burden on renters and partly a gain to homeowners and local tax bases. Treating all housing-price increases as pure social loss is sloppy. [SOURCE: https://www.cato.org/briefing-paper/immigrants-housing-wealth-local-government-finances; SOURCE: https://doi.org/10.1016/j.jue.2006.07.004]
4. Split budgetary cost from nonbudgetary crowding cost. CBO’s 2025 report is useful because it explicitly includes crowding without requiring that the crowding already show up as higher spending. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
5. Stop using CPS for foreign-born population levels. Use ACS, Census estimates, administrative data, or explicit demographic models instead. [SOURCE: https://www.brookings.edu/articles/macroeconomic-implications-of-immigration-flows-in-2025-and-2026-january-2026-update/]
6. Treat legal status, age, and family structure as first-order variables rather than footnotes. Recent commentary from both AEI and critics of Cato is basically saying the same thing here: the average result is not informative unless composition is explicit. [SOURCE: https://www.aei.org/wp-content/uploads/2025/09/The-Fiscal-Impact-of-Immigration-An-Update.pdf?x97961=; SOURCE: https://substack.com/home/post/p-188402226] [FRAMING-SENSITIVE]

## Positive effects that belong in the calculation

These channels are real enough that a balanced model should include them rather than only loading the downside.

| Positive channel | Mechanism | Usually included in pro-immigration papers? | Usually included in local-cost critiques? | Source |
|---|---|---|---|---|
| Lower prices for labor-intensive services | More supply in cleaning, food, care, agriculture, hospitality, construction-related services | Often yes | Often underweighted | Survey comments explicitly mention cheaper services and gains from trade [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] |
| Native task specialization | Natives shift toward language/communication/managerial tasks while immigrants do manual/task-intensive work | Yes in the Peri-style literature | Often omitted | [SOURCE: David Card referenced on the Clark page at https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [INFERENCE] |
| Firm cost reduction and productivity | Lower input costs can expand output and employment | Often yes | Often omitted | [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] [INFERENCE] |
| Labor supply to shortage or undesirable jobs | Fills jobs natives are less willing to do at existing wages | Often yes | Sometimes acknowledged but not valued | [INFERENCE] |
| Payroll taxes with limited benefit take-up | Some groups contribute more than they draw, especially early on | Sometimes yes | Often contested | [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] |
| Housing supply labor | Immigrant labor can expand residential construction and partially offset housing demand pressure | Rarely modeled jointly with housing demand | Rarely modeled jointly with labor benefits | [INFERENCE] |
| Consumer-demand multiplier | More households increase demand for goods and services, raising local output | Sometimes implicit | Often omitted | [INFERENCE] |
| Upward mobility of descendants | Children of immigrants often outperform parental generation and can strengthen the future tax base | Sometimes yes | Often dismissed too quickly | [SOURCE: https://www.nber.org/papers/w26408] |

The practical problem is that no one paper prices all of these positives and all of the local negatives at once. [INFERENCE]

## Matrix A: strongest Clark Center "agree" economists

Question-fit rigor here means rigor for the exact question "does this account for the real costs to the average US citizen, including local non-federal costs?" It is not a judgment on the economist's overall quality. [INFERENCE]

| Economist | Survey vote / confidence | Direct basis I could tie to this question | Effects plausibly included | Main omissions vs a full-spectrum welfare model | Question-fit rigor | Assessment |
|---|---|---|---|---|---|---|
| Hilary Hoynes | `Agree / 10` | Strong public-finance and safety-net work; adjacent to immigration-fiscal incidence, not a full local-cost ledger in this pass [INFERENCE] | Transfer use, poverty, low-income household incidence | Traffic, housing incidence, local school crowding/capacity, full descendant accounting | Medium-adjacent | Useful for the welfare/tax-transfer slice, not enough for the whole question |
| Daron Acemoglu | `Agree / 8` | No direct comprehensive low-skill-immigration cost paper located in this pass [INFERENCE] | Likely GE productivity/complementarity logic | Local fiscal incidence, congestion, housing, descendants | Low-for-this-question | Strong economist, weak direct evidence for this exact claim |
| David Autor | `Agree / 8` | No direct comprehensive low-skill-immigration cost paper located in this pass; closest fit is labor-market/task-adjustment reasoning [INFERENCE] | Wage/task reallocation, complementarity logic | Local fiscal incidence, congestion, housing, descendants | Medium-adjacent | Strong on labor adjustment, not a complete welfare ledger |
| Janet Currie | `Agree / 8` | Strong work on children, health, and family public-program channels; not a full immigration local-cost ledger in this pass [INFERENCE] | Child/family transfer and health channels | Traffic, housing, full GE labor effects, full descendant fiscal ledger | Medium-adjacent | Strong on specific social-cost channels, incomplete overall |
| Oliver Hart | `Agree / 8` | Survey comment relies on "classical gains from trade" and mentions welfare payments to unemployed immigrants [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Broad efficiency gains, some transfer costs | Schools, congestion, housing, local capacity, descendants | Low-for-this-question | Honest about one countervailing channel, still far from comprehensive |
| Maurice Obstfeld | `Agree / 8` | No direct comprehensive low-skill-immigration cost paper located in this pass [INFERENCE] | Open-economy efficiency / factor-mobility logic [INFERENCE] | Local public finance, congestion, housing, descendants | Low-for-this-question | Mostly macro intuition, not local-cost pricing |
| Nancy Stokey | `Agree / 8` | No direct comprehensive low-skill-immigration cost paper located in this pass [INFERENCE] | GE/growth/trade intuition [INFERENCE] | Local fiscal incidence, congestion, housing, descendants | Low-for-this-question | Same issue: plausible theory, not this ledger |
| Christopher Udry | `Strongly Agree / 4` | Survey comment cites complementarities but also says the data is not decisive [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] | Complementarity | Nearly all local fiscal and capacity channels | Low-for-this-question | Most explicit example of strong directional view with limited accounting |

### Read of Matrix A

The strongest Clark "agree" bloc does not look like a bloc of economists who all ran comprehensive local-cost ledgers and got the same answer.

It looks more like:

1. a few economists with adjacent empirical credibility,
2. several economists applying broad economic logic,
3. a survey format that compresses all omitted-channel uncertainty into one yes/no answer.

That is not fraudulent, but it is thinner evidence than the slogan "economists agree" suggests. [INFERENCE]

## Matrix B: actual papers by effect channel

This table is the more honest evidentiary map for the policy question.

| Paper / source | What it really estimates | Positive effects covered | Negative effects covered | Important exclusions | Rigor for the channel | Use in the full model |
|---|---|---|---|---|---|---|
| National Academies, *The Economic and Fiscal Consequences of Immigration* (2017) | Long-run fiscal impact by education, age at arrival, and descendants | Federal taxes, some labor-market integration, descendant tax contributions | Federal and state/local benefits, education, descendant public costs | Traffic congestion, full housing welfare treatment, some local-capacity frictions | High | Best baseline ledger [SOURCE: https://d279m997dpfwgl.cloudfront.net/wp/2016/09/0922_immigrant-economics-full-report.pdf] |
| David Card labor-market work cited on the Clark page | Native wage/employment effects of immigration shocks | Complementarity, small average native wage effects | Distributional pressure on competing workers | Fiscal incidence, housing, congestion | High for labor-market channel | Use for lever 1, not as a full welfare answer [SOURCE: https://kentclarkcenter.org/surveys/low-skilled-immigrants/] |
| Peri-style task-specialization literature | Native task upgrading and productivity adjustment | Complementarity, productivity, service-price moderation | Some distributional adjustment costs | State/local fiscal channels, housing, congestion | High for labor/task channel | Use for positive offset, not for the full cost ledger [INFERENCE] |
| Dustmann-Frattini-style fiscal work | Net fiscal contribution by cohort and skill mix | Taxes paid, age structure, labor-force contribution | Benefit use and fiscal transfers | US local congestion and housing channels, exact US institutional details | High for fiscal channel in its institutional setting | Good comparator, not a direct US local-cost answer [INFERENCE] |
| Saiz (housing) | Effect of immigration inflows on local rents and house prices | None directly, except possible supply response inference | Housing-cost incidence on renters and buyers | Deadweight vs transfer decomposition, broader fiscal effects | High for housing-price response | Use for lever 10 only [SOURCE: https://doi.org/10.1016/j.jue.2006.07.004] |
| Abramitzky et al. (children of immigrants) | Intergenerational mobility and descendant outcomes | Child upward mobility and future tax-base potential | Some descendant underperformance heterogeneity by group is outside headline summaries | Parent-generation local congestion/housing/fiscal burden | High for descendant mobility | Use for lever 5, not as a full welfare answer [SOURCE: https://www.nber.org/papers/w26408] |
| Duncan and Trejo | Slower educational/economic convergence for some Hispanic-origin groups | Provides skepticism against overly optimistic descendant assumptions | Shows descendant underperformance risk for some groups | Full fiscal general equilibrium, local-capacity costs | High for subgroup convergence question | Use as a skeptical sensitivity check on lever 5 [SOURCE: https://www.nber.org/papers/w24394] |
| FRBSF / Monras housing note | Immigrants consume less housing than comparable natives and cluster in cities | Offsets naive demand-only housing arguments | None directly beyond housing-demand nuance | Broader welfare, congestion, fiscal channels | Medium | Good correction to simplistic housing stories [SOURCE: https://www.frbsf.org/research-and-insights/publications/economic-letter/2023/07/why-immigration-is-an-urban-phenomenon/] |
| Local ACS + VMT external-cost overlay in this project | Commute mode mix and a rough congestion add-on | Corrects overstatement that low-skill immigrants are mostly non-drivers | Adds a local traffic cost not in the main fiscal tables | Needs stronger local causal identification and city-specific calibration | Medium | Use as a cautious add-on, not a standalone verdict [DATA: /Volumes/SSK1TB/corpus/census_acs/csv_pus.csv; SOURCE: https://www.brookings.edu/wp-content/uploads/2017/06/jpube-vmt-paper.pdf] |

## What is and is not "bad science"

If a paper estimates one channel and is explicit about that, it is not bad science for being partial.

If a survey answer or paper is then used rhetorically as if it settled the complete welfare question, that is a framing problem and sometimes a standards problem.

The strongest criticism here is:

1. many "agree" economists are not presenting a complete local-cost accounting,
2. some omitted channels run negative,
3. some omitted positive channels also matter,
4. the right response is a broader ledger, not a one-sided dismissal.

That is a stronger and more defensible critique than just saying "bad science." [INFERENCE]

## Practical takeaway

For a serious low-skill immigration calculation, the clean stack is:

1. Start with the National Academies fiscal ledger.
2. Add a descendant-performance sensitivity band using both Abramitzky-style optimism and Duncan-Trejo-style skepticism.
3. Add local congestion explicitly.
4. Treat housing carefully as incidence plus any defensible deadweight component, not as pure loss by assumption.
5. Keep positive channels in view: task complementarity, consumer-price effects, shortage-job filling, and descendant mobility.

That is the first version of a model that is broad enough to criticize both cheap pro-immigration slogans and cheap anti-immigration slogans.
