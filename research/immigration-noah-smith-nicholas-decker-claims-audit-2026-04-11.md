# Noah Smith and Nicholas Decker immigration claims audit — 2026-04-11

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
2. they usually fail when stretched into `average citizen better off overall`

### Nicholas Decker

Best summary:

1. useful as a critique of simplistic constant-returns reasoning
2. overreaches hard from `some increasing-returns channels are real` to `immigrants must make us richer`

Verdict:

1. the anti-anti-immigration economic rhetoric is much too strong
2. the conclusion does **not** follow from the premises

## Executive table

| Author | Claim | Verdict | Why |
|---|---|---|---|
| Noah Smith | `The U.S. needs large-scale immigration to support its economy.` | `Mostly survives, but scope-limited` | National population and output support this; it does not settle per-capita welfare or local burden. [SOURCE: https://www.cbo.gov/system/files/2022-07/57975-demographic-outlook.pdf] [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf] |
| Noah Smith | `Immigration doesn't reduce wages for native-born people, except maybe a little in special cases.` | `Broadly directionally right, rhetorically too absolute` | Literature usually finds small average native effects, but some competing groups can lose and the repo does not treat this as a full welfare verdict. [SOURCE: research/immigration-economist-effects-matrix.md] [SOURCE: research/immigration-evidence-base-audit.md] |
| Noah Smith | `Immigrants are mostly unrelated to the inflation issue.` | `Too broad` | Better for headline inflation than many partisans claim, but recent evidence shows local housing and utilities inflation can rise with immigration. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf] [SOURCE: research/immigration-unified-scenarios-memo.md] |
| Noah Smith | `Mass deportation would make little difference to costs.` | `Overstated` | Mass deportation is unlikely to produce a clean broad consumer-price windfall, but removing workers from labor-intensive and housing-constrained sectors is not cost-neutral. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf] [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf] [INFERENCE] |
| Nicholas Decker | `Immigrants must make us richer.` | `Fails as stated` | Some increasing-returns channels are real, but neither official nor repo evidence supports a universal overall-gain claim on the relevant citizen-welfare ledger. [SOURCE: https://nicholasdecker.substack.com/p/yes-immigrants-must-make-us-richer] [SOURCE: research/immigration-verified-findings-report-2026-04-10.md] |
| Nicholas Decker | `Constant-returns assumptions bake in anti-immigration results.` | `Partly right, partly overclaimed` | Model assumptions matter, especially public-goods and incidence assumptions, but recent official projections do not reduce to one simple constant-returns story. [SOURCE: research/immigration-nas-scope-and-bias-update-2026-04-10.md] [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf] |
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

This directly cuts against Decker's suggestion that coherent anti-immigration arguments reduce to voting or institutions. The local school-capacity channel is real in the repo's own warehouse. [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`, query on `origin_puma_household_context_2023` run 2026-04-11]

### 2. State averages hide real housing-incidence differences

The `PUMA` layer shows that state-average rent often misses where groups actually sort within a state.

Examples:

1. `Colombia`: weighted `PUMA` rent exceeds weighted state rent by about `$184.25`
2. `Brazil`: about `+$157.51`
3. `China`: about `+$150.15`
4. `Venezuela`: about `+$135.59`
5. `Mexico`: about `-$111.09`

This matters for Smith's inflation and housing rhetoric. A national or state-average story can easily miss the actual renter-incidence faced in destination neighborhoods. [SOURCE: research/immigration-local-burden-puma-layer.md] [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`, query on `origin_puma_context_2023` and `state_median_gross_rent_2023` run 2026-04-11]

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

1. CBO also says `real GDP per person` would be lower in 2034 under the immigration increase it modeled. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
2. The repo's verified position is that the strongest result is an `incidence split`, not a scalar positive verdict. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
3. National macro support does not erase local schooling, shelter, or housing-capacity costs. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

Verdict:

1. `Mostly survives` for aggregate output / demographic support
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

1. Even official pro-growth projections do **not** imply that more immigration must raise `GDP per person` or average citizen welfare in the near-to-medium run. CBO's 2024 outlook explicitly says real GDP would be higher but real GDP per person lower under the immigration increase it modeled. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
2. The repo's strongest verified result remains an `incidence split`, which directly contradicts Decker's must-be-positive rhetoric. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
3. Local burden, schooling, shelter, congestion, renter incidence, and political backlash are real economic channels, not merely political afterthoughts. [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

Verdict:

1. `Fails as stated`
2. The positive channels are real
3. The universal conclusion is not

### Claim 2: `Constant returns assumptions bake in anti-immigration results`

What survives:

1. The repo already treats assumption choice as one of the biggest reasons immigration fiscal estimates swing. [SOURCE: research/immigration-nas-scope-and-bias-update-2026-04-10.md]
2. Public-goods allocation, time horizon, descendant treatment, and indirect fiscal channels are all major drivers. [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md]

What fails:

1. Decker overcompresses the problem into one production-function dispute. [INFERENCE]
2. The actual swing factors in the repo are broader: federal vs local incidence, child attribution, public-goods assignment, housing incidence, and local capacity. [SOURCE: research/immigration-fiscal-deceptive-data-reading-pack.md]
3. CBO's 2024 projection does not read like a trivial "constant returns equals bad immigration" story; it finds higher aggregate GDP with lower GDP per person and lower average real wages in the near term. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]

Verdict:

1. `Partly right` that assumptions matter enormously
2. `Wrong` that this single modeling move explains the whole disagreement

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

1. `useful on one methodological criticism`
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
