# Bryan Caplan immigration claims audit — 2026-04-21

**2026-09-05 interpretation correction:** Average resident income, incumbent welfare, fiscal balance and subgroup outcomes are different estimands. A subgroup loss does not refute a positive average; a local cost does not prove net loss or that restriction is necessary. Descriptive county/PUMA screens do not identify causal native-wage or capacity effects. See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md).

## Scope

This memo audits Bryan Caplan's main immigration claims against:

1. his own primary texts
2. official recent U.S. sources
3. the repo's current surge, threshold, crime, and county-outcome work

This is a claim audit, not a general evaluation of Caplan as a thinker.

**Instrument caveat:** immigration is a politically charged topic and the LLM instrument has known bias risk here. This memo leans on primary texts, official sources, and repo-built data artifacts rather than training-data impressions. [SOURCE: `notes/llm-bias-caveat.md`]

## Primary texts audited

1. [Why Should We Restrict Immigration?](https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf) [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
2. [Why Should We Restrict Immigration?](https://www.econlib.org/archives/2012/01/why_should_we_r.html) [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]
3. [The Social and Political Realities of Immigration: A Reply to Hoste](https://www.econlib.org/archives/2010/04/the_social_and.html) [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
4. [Immigration and the Welfare State](https://www.econlib.org/archives/2011/06/immigration_and_2.html) [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html]
5. [Does Immigration Shrink the Welfare State?](https://www.econlib.org/does-immigration-shrink-the-welfare-state/) [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]
6. [Assimilation and Immigration Restriction](https://www.econlib.org/archives/2015/12/krikorian_again.html) [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]
7. [Let Anyone Take a Job Anywhere](https://www.econlib.org/archives/2013/11/let_anyone_take.html) [SOURCE: https://www.econlib.org/archives/2013/11/let_anyone_take.html]

## Bottom line

Caplan is strongest where the current repo already agrees with the classic open-borders literature:

1. the `migrant-welfare` and `global-output` case for much freer movement is real [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83] [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
2. the U.S. observed-criminal-justice-rate objection to first-generation and unauthorized immigrants is weaker than restrictionists usually claim [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
3. broad `employment-collapse` rhetoric is too strong [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]

Caplan is weakest where recent surge and threshold evidence make local incidence unsafe to wave away:

1. a taxpayer-policy conclusion needs federal/state/local distribution and a comparison with proposed alternatives; local costs alone do not refute it [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. worker-policy conclusions require measured losses and alternative remedies; descriptive wage screens alone do not establish restriction’s necessity [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
3. the claim that political externalities are manageable by default is not established under surge conditions and capacity thresholds [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-causal-surge-2021-2024.md]

The clean verdict is:

1. `strong on migrant-welfare / global-gains direction, not strongest magnitude`
2. `strong on observed U.S. justice-system-rate skepticism`
3. `partial on labor`
4. `weak on destination-local fiscal and political incidence`

## Executive table

| Claim | Verdict | Why |
|---|---|---|
| `There is a moral presumption in favor of free migration.` | `Coherent normative starting point, not an empirical result` | This is a normative premise, compatible with a libertarian moral frame; it does not answer native-local welfare by itself. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [FRAMING-SENSITIVE] |
| `The economic case for much freer migration is extremely strong.` | `Mostly survives in direction, not in strongest magnitude` | Large global gains survive; realistic `double world GDP` style readings do not. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md] |
| `Immigration restrictions are not necessary to protect American workers.` | `Not adjudicated by the county wage screen` | A descriptive local wage association and projected losses for an exposed group do not show restriction is necessary; compare feasible remedies and their costs. [SOURCE: county-outcome memo; CBO60165; INFERENCE] |
| `Immigration restrictions are not necessary to protect American taxpayers.` | `Not adjudicated by a cost-only comparison` | Federal gains can coexist with state/local costs in education, shelter, and related services. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] |
| `Immigrants commit much less crime than natives.` | `Mostly survives for observed U.S. first-generation / unauthorized justice-system rates` | The U.S. evidence is strong for lower observed arrest, conviction, and incarceration rates, though the aggregate descriptive comparison is not a demographic-standardized estimate and the international generalization is weaker. True offending is less directly identified. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md] |
| `Immigration restrictions are not necessary to protect American culture.` | `Partly survives, but culture is not the best-developed bottleneck in this evidence surface` | Apocalyptic culture-collapse arguments are weak; assimilation is real. But the repo's current U.S. stress evidence is better developed for housing, services, and politics than for a clean culture mechanism. [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] |
| `Political externalities are limited because immigrants vote less, accept the status quo, and may restrain redistribution.` | `Partly survives in a narrow median-voter sense, fails as a full political-incidence answer` | National voting mechanics are only one channel; local overload, legitimacy effects, and possible citizen political response remain live. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md] |
| `Cheaper and more humane alternatives exist for each complaint.` | `Partly survives as institutional design logic, not as practical closure` | Keyhole solutions mitigate some objections, but do not dissolve housing, school, shelter, and credibility problems. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] |

## Claim 1: `There is a moral presumption in favor of free migration`

This is the foundation of Caplan's case. In the Cato piece and Econlib summary, he argues that voluntary exchange between natives and foreigners looks morally permissible on its face, so restriction needs a real excuse. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]

What survives:

1. As a libertarian moral premise, this is internally coherent. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]
2. It correctly forces empirical objectors to specify what harm they are actually invoking. [INFERENCE]

What does not follow:

1. A moral presumption is not a fiscal estimate. [FRAMING-SENSITIVE]
2. A rights-based starting point does not settle `who bears transition costs` in public systems with local externalities. [FRAMING-SENSITIVE]

Verdict:

1. `survives as a normative premise`
2. `cannot be verified or falsified by the county or CBO evidence alone`

## Claim 2: `The economic case for much freer migration is extremely strong`

Caplan's strongest empirical lane is that migration creates very large gains because labor is far more productive in high-productivity places. He is in the Clemens / place-premium tradition here. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf] [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]

What survives:

1. The direction of the global-gains claim survives. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
2. The repo's own bounded calibration still finds large gains under substantial movement, just far below the strongest slogans. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
3. Many anti-immigration arguments ignore the scale of migrant place-premium gains. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]

What fails:

1. The strongest open-borders headline versions are not realistic central forecasts once realistic migration volume, housing, congestion, and political constraints are added. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]
2. Official projections can show higher aggregate GDP with lower GDP per person in the expanded population. This does not establish lower incumbent welfare or refute conditional global gains; the populations being compared differ. [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]

Verdict:

1. `direction/sign survives`
2. `not entitled to the strongest magnitude or destination-local gloss`

## Claim 3: `Immigration restrictions are not necessary to protect American workers`

Caplan repeatedly argues that most Americans gain, while the losers do not lose much, and that even worker losses could be handled more humanely than by exclusion. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.econlib.org/archives/2013/11/let_anyone_take.html]

What survives:

1. The repo's current county panel does **not** show a broad employment-collapse story. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
2. The evidence supports Caplan's objection to the crudest version of `immigration destroys jobs`. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]

What cuts against him:

1. In counties with very high recent immigration and low permit throughput, `2021–2024` weekly wage growth is about `1.5 pp` lower in the repo's county screen. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
2. CBO projects that through `2026`, wage growth for non-surge workers with `12 or fewer years of education` is slightly lower than in the no-surge counterfactual. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
3. In the repo's current worker-incidence evidence surface, the better-developed concern is not broad `job destruction`; it is slower wage progression in constrained places. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [INFERENCE]

Verdict:

1. `collapse rhetoric is unsupported by the current county panel`
2. `Worker losses and alternative remedies need quantification; the audit has not established that restriction is necessary`

## Claim 4: `Immigration restrictions are not necessary to protect American taxpayers`

This claim concerns whether restrictions are necessary relative to alternative policies, not whether every fiscal cost is zero. He argues the fiscal effects are small and that researchers disagree on sign but agree on modest magnitude. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html]

Splitting fiscal ledgers reveals distributional costs, but does not by itself refute modest aggregate fiscal effects or show that entry restrictions are necessary. Caplan’s alternatives need a comparative feasibility and welfare assessment. [INFERENCE]

What survives:

1. The `federal` ledger can indeed be positive. CBO projects about `$897B` lower covered federal deficits over `2024–2034`, including revenue, mandatory spending and net interest but excluding discretionary appropriations and state/local budgets. Its proportional-discretionary illustration adds about `$0.2T`; it is not a verified bound. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
2. Caplan's criticism is supported where restrictionists blur national and local fiscal ledgers. [INFERENCE]

What the cost evidence establishes (not proof of restriction’s necessity):

1. The specified `2023 state/local` surge account is negative in the official CBO accounting. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. The large cost buckets are `education`, `shelter and related services`, and `border security`, not just cash welfare. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
3. The repo's current position already treats local school, shelter, housing, and service load as first-order channels rather than rhetorical appendices. [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md] [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md]

Verdict:

1. `local costs are relevant; necessity of restriction remains unproved`
2. `requires comparing restriction with feasible transfers, fees and capacity policies on a common welfare basis`

## Claim 5: `Immigrants commit much less crime than natives`

Caplan has long treated the crime objection as empirically weak. On current U.S. observed justice-system-rate evidence, this is one of his strongest empirical claims. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]

What survives:

1. The repo's crime memo finds the weight of U.S. evidence supports lower observed first-generation and unauthorized arrest, conviction, or incarceration rates than native-born rates. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
2. The Texas administrative-data line remains one of the strongest direct sources. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]

Important caveats:

1. An unauthorized-versus-all-native comparison describes those populations; it is not a matched comparison. Excluding one racial group does not make the remaining covariate distributions equal or establish that the original descriptive gap was overstated. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]
2. This is strongest for observed current U.S. first-generation / unauthorized justice-system rates, not a universal all-country or true-offending rule. [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]

Verdict:

1. `mostly survives`
2. `Caplan is on strong ground here, with compositional caveats`

## Claim 6: `Immigration restrictions are not necessary to protect American culture`

Caplan often treats the cultural objection as weak: immigrants assimilate, their children learn English, and fears of permanent civilizational non-assimilation are overstated. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]

What survives:

1. The hardest-line permanent non-assimilation claim is too strong. [SOURCE: https://www.econlib.org/archives/2015/12/krikorian_again.html]
2. The repo's current evidence surface is better developed for `housing`, `services`, `shelter`, and `politics` than for `culture` as the first binding destination-country channel. That is not proof that culture is never first-binding. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [INFERENCE]

What remains open:

1. Trust, solidarity, and political-response channels are not zero merely because assimilation exists. [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md]
2. Caplan's welfare-state and trust optimism is partly a political-economy claim, not just a culture claim. [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html] [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]

Verdict:

1. `partly survives`
2. `culture collapse is not the clean modern objection`
3. `but culture/trust cannot simply be dismissed as solved`

## Claim 7: `Political externalities are limited`

Caplan's standard package here is:

1. immigrants vote less than natives [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
2. they accept the status quo by default [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
3. diversity may reduce support for redistribution [SOURCE: https://www.econlib.org/archives/2011/06/immigration_and_2.html] [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]

What survives:

1. In a narrow `median-voter today` sense, lower turnout and slower political incorporation do damp one channel of political effect. [SOURCE: https://www.econlib.org/archives/2010/04/the_social_and.html]
2. It is plausible that some immigration can weaken solidaristic support for redistribution. Caplan himself later acknowledges that the effect is moderate and mostly about slower growth rather than actual shrinkage of the welfare state. [SOURCE: https://www.econlib.org/does-immigration-shrink-the-welfare-state/]

What fails:

1. The relevant political channel is not only immigrant voting. It also includes possible citizen response, local overload, policy churn, and perceived unfairness. [SOURCE: research/immigration-full-spectrum-costs-unauthorized-memo.md]
2. The repo's threshold and county-outcome analyses report stronger political-response association signals in high-immigration constrained places, especially where permit capacity is weak and rent burden high. The mechanism is not yet cleanly separated into persuasion, turnout, sorting, Hispanic realignment, or busing-target endogeneity. [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md] [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
3. The surge memo already treats the `2021–2024` period as a different regime from the older low-intensity local-labor literature. [SOURCE: research/immigration-causal-surge-2021-2024.md]

Verdict:

1. `welfare-state-voting channel is partly supported`
2. `incomplete as a full political-incidence answer`

## Claim 8: `Cheaper and more humane alternatives exist for each complaint`

Caplan's keyhole-solution instinct is real and important. He argues that if immigrants burden workers, taxpayers, or politics, there are less coercive solutions than exclusion: entry fees, higher immigrant taxes, welfare exclusion, delayed voting, and related conditions. [SOURCE: https://www.econlib.org/archives/2012/01/why_should_we_r.html] [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]

What survives:

1. As a design principle, this is stronger than generic `just trust immigration` rhetoric. [INFERENCE]
2. Some objections really are more tractable through institutional design than through outright exclusion. [SOURCE: research/immigration-david-d-friedman-claims-audit-2026-04-11.md]

What fails:

1. The effectiveness, cost and feasibility of the proposed fixes for housing/school/shelter constraints must be evaluated. Their existence does not guarantee success, but observing a cost under current policy does not prove the alternatives fail. [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
2. They also rely on credibility and state capacity. A keyhole solution that is politically impossible or institutionally non-credible is not a full answer. Caplan himself acknowledges that open borders is `far out of sample` and that worst-case scenarios cannot be ruled out with confidence. [SOURCE: https://www.cato.org/sites/cato.org/files/serials/files/cato-journal/2012/1/cj32n1-2.pdf]

Verdict:

1. `good institutional imagination`
2. `not enough to close the empirical case`

## Hypothesized causal graph — edges are not estimated effects

The graph lists plausible mechanisms and competing channels. Drawing an edge does not verify it, estimate its magnitude or establish that it dominates omitted gains; county associations cannot validate every path. [INFERENCE]

### Baseline DAG

`migration liberalization`
-> `inflow volume and composition`
-> `migrant earnings gains`
-> `global output gains`

`migration liberalization`
-> `inflow volume and composition`
-> `destination labor supply`
-> `employer surplus / consumer surplus`
-> `national GDP gains`

`migration liberalization`
-> `inflow volume and composition`
-> `housing demand`
-> `rent burden / crowding`
-> `native sorting / political response`

`migration liberalization`
-> `inflow volume and composition`
-> `school / shelter / service load`
-> `state-local fiscal costs`
-> `political response / legitimacy costs`

`migration liberalization`
-> `inflow volume and composition`
-> `labor-market competition under local capacity constraints`
-> `slower wage growth for exposed groups`

`migration liberalization`
-> `inflow volume and composition`
-> `crime composition`
-> `public-safety concern`

### Main moderators

The following are candidate moderators in the repository’s descriptive screens, not a causally established ranking:

1. `permit throughput / housing-supply response` [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
2. `baseline rent burden / affordability` [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md]
3. `shelter inventory and legal regime` [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]
4. `pace and concentration of inflow` [SOURCE: research/immigration-causal-surge-2021-2024.md]
5. `skill/origin/family composition` [SOURCE: research/immigration-low-skill-origin-incidence-memo.md]

### Where Caplan is strongest

Caplan's model is strongest on the left side of the DAG:

1. `migrant earnings gains`
2. `global output gains`
3. `observed U.S. justice-system-rate skepticism`

These are real and durable parts of the case at that scope. [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md] [SOURCE: research/immigration-crime-rates-unauthorized-vs-native-born.md]

### Where Caplan is weakest

Caplan is weakest where omitted or downweighted right-side edges become first-order:

1. `housing demand -> rent burden -> native sorting / political response`
2. `school / shelter / service load -> state-local costs`
3. `capacity-constrained labor absorption -> slower wage growth`
4. `citizen political response and legitimacy effects`, which do not require immigrant voting to matter

These are questions for a policy comparison. The repository has not causally established every edge or shown that restriction dominates Caplan’s proposed alternatives. [INFERENCE]

## Net verdict

If the question is `Does Caplan's case that freer migration can create huge gains and that many standard restrictionist objections are overstated survive?`

1. `Yes, mostly.`

If the question is `Has Caplan shown that immigration restrictions are unnecessary for protecting the welfare of existing residents in the destination country?`

1. `Not established by this audit; neither has the necessity of restriction been established.`

The best current summary is:

1. `Caplan is strongest on migrant-welfare direction and large global-gains sign, not on the strongest open-borders magnitude or destination-capacity closure.`
2. `Caplan is strongest on observed U.S. justice-system-rate crime skepticism relative to his other empirical lanes.`
3. `Caplan is partially supported on labor, but only after dropping collapse rhetoric and admitting evidence consistent with a constrained-place wage-growth concern.`
4. `The audit identifies relevant costs and uncertainty, but has not compared restriction against Caplan’s proposed remedies or established a net welfare sign.`

So the final score is:

1. `substantial evidence on several gain channels, with policy-specific assumptions`
2. `local and political channels need estimation and comparison with feasible alternatives`

**GDP and welfare correction [INFERENCE]:** A lower population-wide GDP-per-person average after entry can coexist with gains for every incumbent, because new entrants change the population being averaged. Conversely aggregate growth does not guarantee every incumbent gains. Neither comparison alone determines total incumbent welfare. Rent payments transfer resources between tenants and owners; count real congestion/building costs separately and avoid counting a transfer as a whole-economy loss. A modeled large global gain is conditional, not a proved mathematical ceiling or a guaranteed feasible policy forecast.

## Revisions

| Date | Change |
|------|--------|
| 2026-06-16 | Replaced the "strongest current worker-incidence channel" shortcut with evidence-surface language: current memos better develop constrained-place wage progression than broad job destruction. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced first-binding culture and political-externality shortcuts with evidence-surface language: housing/service/political channels are better developed in current memos, not proven universally primary. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced remaining "Caplan is right" labels with claim-support language, including global-gains, ledger-blurring, labor-collapse, and DAG framing. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Replaced residual right/wrong and wins/loses verdict labels with strongest/weakest/support language while preserving the same claim ranking. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Bounded the Caplan global-gains verdict to direction/sign rather than strongest magnitude or destination-capacity closure. See `immigration-conclusion-audit-running-fixes.md`. |
| 2026-06-16 | Scoped shorthand "wins on crime" language to observed U.S. justice-system-rate skepticism, matching the crime memo's true-offending caveat. See `immigration-conclusion-audit-running-fixes.md`. |

- **2026-09-05 — Corrected welfare, comparator and model-scope reasoning.** See [material-inference repair](../decisions/2026-09-05-material-inference-repair.md). Earlier dated revision entries describe the historical state, including superseded conclusions.
