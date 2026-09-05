# Noah Smith and Nicholas Decker immigration claims audit — 2026-04-11

**2026-09-05 interpretation correction:** Average resident income, incumbent welfare, fiscal balance and subgroup outcomes are different estimands. A subgroup loss does not refute a positive average; a local cost does not prove net loss or that restriction is necessary. Descriptive county/PUMA screens do not identify causal native-wage or capacity effects. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).

## Scope

This memo audits concrete immigration claims from:

1. Noah Smith / Noahpinion
2. Nicholas Decker / Homo Economicus

This is **not** a general rating of their blogs.
It is a claim-level audit against:

1. official sources
2. recent papers
3. the repo's verified immigration stack
4. the local public-use build state

## Objects audited

### Noah Smith

Primary pieces:

1. [A bunch of thoughts and evidence on immigration](https://www.noahpinion.blog/p/a-bunch-of-thoughts-and-evidence)
2. [Why immigration doesn't reduce wages](https://www.noahpinion.blog/p/why-immigration-doesnt-reduce-wages)
3. [Did immigration bring down inflation?](https://www.noahpinion.blog/p/did-immigration-bring-down-inflation)

### Nicholas Decker

Primary piece:

1. [Yes, Immigrants Must Make Us Richer](https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer)

## Bottom line

### Noah Smith

Best summary:

1. strongest on `national macro direction`
2. decent on `native-wage skepticism`
3. weakest on `local incidence` and `housing / inflation dismissal`

Verdict:

1. many of his economic claims survive in a **narrowed** form
2. the cited narrow evidence does not itself establish `average citizen better off overall`; failure to establish is not a negative average-welfare finding

### Nicholas Decker

Best summary:

1. raises a production-model question, but constant returns alone says nothing decisive about immigration gains
2. overreaches hard from `some increasing-returns channels are real` to `immigrants must make us richer`

Verdict:

1. the anti-anti-immigration economic rhetoric is much too strong
2. the conclusion does **not** follow from the premises

## Executive table

| Author | Claim | Verdict | Why |
|---|---|---|---|
| Noah Smith | `The U.S. needs large-scale immigration to support its economy.` | `Supports population/labor-force growth under the projection; necessity is not established` | A demographic projection does not prove that immigration is the only way to increase output or incumbent welfare; productivity, capital and the chosen policy objective matter. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf; INFERENCE] |
| Noah Smith | `Immigration doesn't reduce wages for native-born people, except maybe a little in special cases.` | `Broadly directionally right, rhetorically too absolute` | Literature usually finds small average native effects, but some competing groups can lose and the repo does not treat this as a full welfare verdict. [SOURCE: research/immigration-economist-effects-matrix.md] [SOURCE: research/immigration-evidence-base-audit.md] |
| Noah Smith | `Immigrants are mostly unrelated to the inflation issue.` | `Too broad` | Better for headline inflation than many partisans claim, but recent evidence shows local housing and utilities inflation can rise with immigration. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf] [SOURCE: research/immigration-unified-scenarios-memo.md] |
| Noah Smith | `Mass deportation would make little difference to costs.` | `Overstated` | Mass deportation is unlikely to produce a clean broad consumer-price windfall, but removing workers from labor-intensive and housing-constrained sectors is not cost-neutral. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf] [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf] [INFERENCE] |
| Nicholas Decker | `Immigrants must make us richer.` | `Fails as stated` | Some increasing-returns channels are real, but neither official nor repo evidence supports a universal overall-gain claim on the relevant citizen-welfare ledger. [SOURCE: https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer] [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] |
| Nicholas Decker | `Constant-returns assumptions bake in anti-immigration results.` | `Does not follow from constant returns` | Returns to scale concerns scaling all inputs; immigration can change one input and factor ratios. Public-goods allocation is a separate fiscal choice. See the explicit production-function calculation below. [RECALCULATION; INFERENCE] |
| Nicholas Decker | `The only coherent anti-immigration view is political voting / institutions, not economics.` | `False` | There are coherent economic objections on local schooling, shelter, congestion, renter incidence, and distributional conflict even without nativist politics. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md] |

## Repo data checks that matter

These are the local results that matter most for auditing Smith and Decker.

### 1. The warehouse does show real local school-burden heterogeneity

Among origin groups with at least `10,000` recent low-skill adults in the corrected household-normalized `PUMA` layer:

1. `Afghanistan`: `2.6291` school-age children per linked household; `86.67%` of linked households have school-age children
2. `Honduras`: `1.2855`; `70.87%`
3. `Myanmar`: `1.2650`; `66.14%`
4. `El Salvador`: `1.0600`; `58.63%`
5. `Mexico`: `1.0114`; `53.49%`
6. `Guatemala`: `0.9960`; `59.07%`

These historical linked-household/context summaries motivate a school-capacity question. They do not measure incremental spending, crowding, causal native losses or an all-in negative welfare effect. Their April extraction has not been re-certified after the September allocation/code audit. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`, query on `origin_puma_household_context_2023` run 2026-04-11]

### 2. State averages hide real housing-incidence differences

The `PUMA` layer shows that state-average rent often misses where groups actually sort within a state.

Examples:

1. `Colombia`: weighted `PUMA` rent exceeds weighted state rent by about `$184.25`
2. `Brazil`: about `+$157.51`
3. `China`: about `+$150.15`
4. `Venezuela`: about `+$135.59`
5. `Mexico`: about `-$111.09`

These weighted PUMA rent levels describe location exposure and sorting, not the causal rent change induced by an origin group or each household’s actual payment. A level comparison cannot rebut an inflation claim without a time/counterfactual bridge. [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`, query on `origin_puma_context_2023` and `state_median_gross_rent_2023` run 2026-04-11]

### 3. The new `MEPS` module weakens crude health-burden rhetoric, but does not rescue the broad economist verdict

The repo's first real public-use `MEPS` module found that for working-age adults `25-64`, foreign-born cells generally show lower observed annual medical spending than U.S.-born cells within comparable insurance buckets:

1. `any private`: about `$5,522` foreign-born vs `$8,084` U.S.-born
2. `public only`: about `$5,185` vs `$10,200`
3. `uninsured`: about `$782` vs `$1,451`

So the repo does **not** support a simple story that foreign-born working-age adults are mechanically a heavier observed annual medical-cost burden. But this is still one ledger, not a scalar welfare verdict. [SOURCE: research/immigration-public-mvp-meps-module-2026-04-11.md]

## Noah Smith

### Claim 1: `The U.S. needs large-scale immigration to support its economy`

Smith's framing:

1. the U.S. needs immigration to grow instead of shrink
2. small declining towns especially need immigrants
3. large immigration is economically necessary

[SOURCE: https://www.noahpinion.blog/p/a-bunch-of-thoughts-and-evidence]

What survives:

1. CBO projects that immigration is carrying an increasing share of U.S. population growth, and without immigration the population would begin shrinking in the 2030s. [SOURCE: https://www.cbo.gov/system/files/2025-03/61187-LTBO-Executive-Summary.pdf]
2. CBO also projects that higher immigration raises aggregate real GDP and expands the labor force. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
3. The repo already treats migration as a potential `national resilience asset` under aging and labor-force slowdown conditions. [SOURCE: research/immigration-unified-scenarios-memo.md]

What does not survive cleanly:

1. CBO also projects lower `real GDP per person` in the expanded population in2034. This does not imply lower incumbent income or welfare, and it does not alone refute an aggregate-output claim. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
2. The repo's verified position is that the strongest result is an `incidence split`, not a scalar positive verdict. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
3. National macro support does not erase local schooling, shelter, or housing-capacity costs. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

Verdict:

1. `Supports a conditional demographic/output channel, not a theorem that large-scale immigration is economically necessary`
2. `Does not prove` that the average citizen is better off overall

### Claim 2: `Immigration doesn't reduce wages for native-born people`

Smith's framing:

1. native wages are usually unchanged
2. immigrants mostly raise both labor supply and labor demand
3. anti-immigration wage fear is mostly unsupported

[SOURCE: https://www.noahpinion.blog/p/why-immigration-doesnt-reduce-wages]

What survives:

1. The repo's economist audit says many pro-immigration papers are not wrong on the wage / complementarity channel. [SOURCE: research/immigration-economist-effects-matrix.md]
2. The evidence-base audit concluded that no clear core paper behind the pro camp was factually wrong on its stated labor-market object. [SOURCE: research/immigration-evidence-base-audit.md]
3. The broad literature often finds small average native wage effects near zero, especially compared with public rhetoric. [SOURCE: research/immigration-evidence-base-audit.md]

What cuts against Smith's stronger rhetoric:

1. The repo explicitly treats `Borjas vs Peri` as unresolved on the size of native low-skill displacement, not as fully settled in one direction. [SOURCE: research/immigration-verification-handoff.md]
2. The repo also treats these labor-market papers as `partial channels`, not full welfare ledgers. [SOURCE: research/immigration-economist-effects-matrix.md]
3. Even if the average native wage effect is small, local public-finance and housing incidence can still be negative. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]

Verdict:

1. `Broadly right` that native-wage doom narratives are overstated
2. `Too confident` if read as "wage concern is solved" or "therefore immigration is good overall"

### Claim 3: `Immigrants are mostly unrelated to the inflation issue`

Smith's framing:

1. immigration probably did not drive the disinflation of 2023
2. immigration should not get credit for everything good in the economy
3. immigration is mostly unrelated to inflation

[SOURCE: https://www.noahpinion.blog/p/did-immigration-bring-down-inflation]

What survives:

1. The strongest recent partisan claim that immigration was the main reason inflation fell is not well supported. [SOURCE: https://www.noahpinion.blog/p/did-immigration-bring-down-inflation]
2. The repo already agreed that immigrants are not a clean all-purpose explanation for inflation dynamics. [SOURCE: research/immigration-unified-scenarios-memo.md]

What does not survive:

1. The IMF 2025 working paper finds that higher immigration lowers local `goods inflation` but raises `housing and utilities inflation`. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf]
2. The repo's current housing view is explicitly that renters and high-cost service users can lose in constrained markets. [SOURCE: research/immigration-unified-scenarios-memo.md]
3. Smith's `mostly unrelated` line is therefore too broad if read at the local or renter-incidence level. [INFERENCE]

Verdict:

1. `Right` against the crude claim that immigration alone explains national disinflation
2. `Wrong / too broad` if used to deny local housing-cost pressure

### Claim 4: `Mass deportation would accomplish nothing`

This claim appears in Smith's roundup as a linked prior post, not as a detailed claim re-argued there. [SOURCE: https://www.noahpinion.blog/p/a-bunch-of-thoughts-and-evidence]

What survives:

1. The repo does not support a story where removing immigrants automatically makes the average citizen broadly better off. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
2. Large immigration reductions can reduce labor-force growth and GDP growth. [SOURCE: https://www.brookings.edu/articles/macroeconomic-implications-of-immigration-flows-in-2025-and-2026-january-2026-update/]

What cuts against `nothing`:

1. Removing workers from labor-intensive sectors is not a zero-effect event. [INFERENCE]
2. The repo's own local-burden stack shows immigration changes real school and housing exposure patterns, so saying deportation would do literally nothing is too strong. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-local-burden-puma-layer.md]

Verdict:

1. `Likely directionally right` against magical price-drop promises
2. `Overstated` because "nothing" is not the same as "not the clean fix advocates promise"

## Nicholas Decker

### Claim 1: `Immigrants must make us richer`

Decker's framing:

1. constant returns to scale are obvious nonsense
2. specialization, ideas, and fixed costs imply increasing returns
3. therefore immigrants must make us richer

[SOURCE: https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer]

What survives:

1. It is reasonable to argue that some immigration gains operate through specialization, ideas, and scale. [SOURCE: https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer]
2. The repo already treats indirect positive channels as real and often undercounted. [SOURCE: research/immigration-economist-effects-matrix.md]

What fails:

1. CBO’s projected increase in aggregate GDP and decrease in GDP per person concern an expanded population. Neither identifies the change in pre-existing citizens’ average welfare; even gains for every incumbent can coexist with a lower new population average. This is a scope limit, not a CBO refutation of incumbent gains. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
2. The repo's strongest verified result remains an `incidence split`, which requires specifying the welfare objective but does not alone contradict a positive average-incumbent claim. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
3. Local burden, schooling, shelter, congestion, renter incidence, and political backlash are real economic channels, not merely political afterthoughts. [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

Verdict:

1. `Fails as stated`
2. The positive channels are real
3. The universal conclusion is not

### Claim 2: `Constant returns assumptions bake in anti-immigration results`

What survives:

1. The repo already treats assumption choice as one of the biggest reasons immigration fiscal estimates swing. [SOURCE: research/immigration-nas-scope-and-bias-update-2026-04-10.md]
2. Fiscal allocations, horizons and indirect tax channels can change estimates, but these choices are distinct from returns to scale in a production function. [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md]

What fails:

1. Decker overcompresses the problem into one production-function dispute. [INFERENCE]
2. The actual swing factors in the repo are broader: federal vs local incidence, child attribution, public-goods assignment, housing incidence, and local capacity. [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md]
3. CBO's 2024 projection does not read like a trivial "constant returns equals bad immigration" story; it finds higher aggregate GDP with lower GDP per person and lower average real wages in the near term. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]

Verdict:

1. `The constant-returns argument is invalid as a theorem; fiscal assumptions require a separate analysis`
2. `A corrected production model still does not settle the full welfare question`

### Claim 3: `The only coherent anti-immigration view is that immigrants vote for bad things`

This is the weakest sentence in Decker's piece.

Why it fails:

1. Coherent economic objections exist even if you set aside identity politics.
2. CBO 2025 directly finds net state/local costs from the recent surge, with education, shelter, and border-security pressures carrying much of the burden. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. The repo's verified findings support real local burden heterogeneity through school-age child intensity and rent exposure. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
4. The repo's full-spectrum memo identifies local congestion, language-access overhead, court friction, and informal-labor distortion as real cost channels, even without any appeal to voting behavior. [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md]

Verdict:

1. `False`

## Net comparison

### Noah Smith

Best classification:

1. `usually valid partials`
2. `often overgeneralized by conclusion`

### Nicholas Decker

Best classification:

1. `not a valid constant-returns theorem; useful channels require separate evidence`
2. `then leaps past the evidence`

## Final verdict

If the question is `who is closer to the truth?`

1. `Noah Smith` is closer on average.
2. But even Noah's better claims are usually `too broad for the full welfare question`.
3. `Nicholas Decker` is more philosophically aggressive than empirically disciplined on this topic.

If the question is `what survives after verification?`

1. immigration has real macro and labor-market upside channels
2. those channels do **not** settle the local-capacity or average-citizen ledger
3. strong anti-immigration fiscal numbers are also assumption-sensitive and often overstated
4. the cleanest current repo stance remains: `incidence split, not scalar verdict`

## Next useful extension

If this memo is continued, the next names to audit should be:

1. Daniel Di Martino
2. David Bier
3. Steven Camarota
4. one Clark-center economist with a strong `agree` vote

That would produce a tighter `commentator stack` across pro, skeptical, and restrictionist sides.

**GDP and welfare correction [INFERENCE]:** A lower population-wide GDP-per-person average after entry can coexist with gains for every incumbent, because new entrants change the population being averaged. Conversely aggregate growth does not guarantee every incumbent gains. Neither comparison alone determines total incumbent welfare. Rent payments transfer resources between tenants and owners; count real congestion/building costs separately and avoid counting a transfer as a whole-economy loss. A modeled large global gain is conditional, not a proved mathematical ceiling or a guaranteed feasible policy forecast.


## Revisions

- **2026-09-05 — Corrected welfare, comparator and model-scope reasoning.** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Earlier dated revision entries describe the historical state, including superseded conclusions.

**Constant-returns correction [RECALCULATION]:** `F(K,L)=sqrt(KL)` has constant returns when both inputs scale. At `K=L=100`, output is100. Holding capital100 and increasing labor to121 raises output to110 but lowers output per worker from1 to110/121≈0.909. Constant returns does not mean output per worker is invariant when only labor changes; public-goods allocation is a separate fiscal question. This corrects the earlier partial endorsement of Decker’s production-function argument.
