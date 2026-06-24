# Immigration commentators — comparative quantitative audit of Noah Smith, Nicholas Decker, and David D. Friedman

**Question:** Can we evaluate the main immigration claims of `Noah Smith`, `Nicholas Decker`, and `David D. Friedman` with a more rigorous, more decisive, and more quantitative first-principles framework?  
**Tier:** Deep  
**Date:** 2026-04-11

## Ground truth

The repo already had three separate named audits:

1. [immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md](research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md)
2. [immigration-david-d-friedman-claims-audit-2026-04-11.md](research/immigration-david-d-friedman-claims-audit-2026-04-11.md)
3. [immigration-verified-findings-report-2026-04-10.md](research/immigration-verified-findings-report-2026-04-10.md)

Those memos already converged on one core result:

1. the strongest current repo finding is an `incidence split`, not a scalar verdict [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
2. national macro and federal-budget gains can coexist with local school, shelter, housing, and backlash costs [SOURCE: research/immigration-unified-scenarios-memo.md]

This memo tightens that result into a common quantitative frame and then scores all three commentators against it.

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | The `2021–2026` immigration surge above baseline adds `8.7M` people, lowers federal deficits by about `$897B` over `2024–2034`, and raises nominal GDP by about `$8.9T` over the same window. | official budget/econ projection | HIGH | https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf | VERIFIED |
| 2 | The same surge added about `4.4M` residents in `2023` and imposed about `-$9.2B` direct and `-$9.8B` potential state/local net cost in that year. | official state/local budget projection | HIGH | https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf | VERIFIED |
| 3 | On a rough aggregate basis, that `2023` local ledger is about `+$2.3k` taxes, `+$4.4k` spending, and `-$2.1k` direct net per added resident. | arithmetic from CBO aggregates | HIGH | CBO 2025 + local computation | DATA |
| 4 | Doubling immigration lowers local inflation by about `0.1–0.2pp`, but raises local housing and utilities inflation; effects are larger for working-age and low-education immigrants. | IMF paper | HIGH | https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf | VERIFIED |
| 5 | CBO projects that through `2026` the surge slightly reduces wage growth for non-surge workers with `12 or fewer years of education`, with slight reversal later. | official labor-market projection | HIGH | https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf | VERIFIED |
| 6 | CBO’s broader 2024 population revision implies higher immigration boosts real GDP growth by about `0.2pp/year` and leaves real GDP about `2%` larger by `2034`, but real GDP per person about `0.8%` smaller. | official macro projection | HIGH | https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf | VERIFIED |
| 7 | The repo warehouse shows large school/rent heterogeneity across origin groups, so local burdens are not a rhetorical artifact. | local DuckDB + warehouse memos | HIGH | `immigration_context.duckdb`, household/PUMA memos | VERIFIED |

## Common first-principles framework

The right starting point is not `is immigration good or bad?`

It is:

`which welfare function are we evaluating?`

There are at least three distinct ledgers.

### 1. Global ledger

`Delta W_global = migrant income gain + destination producer/consumer surplus + dynamic productivity gains - origin losses - local congestion/public-cost spillovers`

This is the strongest ledger for `Friedman`, and a hidden support beam for both `Smith` and `Decker`. [SOURCE: http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf] [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]

### 2. U.S. national ledger

`Delta W_US = Delta consumer surplus + Delta employer profits + Delta federal budget + Delta national productivity - Delta native wage competition - Delta discretionary public cost - Delta political/backlash cost`

This is where `Smith` mostly lives, even when he talks as if he is answering the average-citizen question. [SOURCE: research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md]

### 3. Native-local ledger

`Delta W_native_local = Delta local tax base - Delta school cost - Delta shelter/service cost - Delta housing incidence - Delta congestion - Delta backlash/institutional cost + local producer gains`

This is the ledger that breaks most sweeping pro-immigration rhetoric, because local costs are concentrated rather than averaged away. [SOURCE: research/immigration-unified-scenarios-memo.md] [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]

## Quantitative anchors

### Federal / macro anchor

From CBO 2024:

1. the surge exceeds prior-trend net immigration by `8.7M` over `2021–2026` [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]
2. federal deficits fall by about `$897B` over `2024–2034` [SOURCE: same]
3. federal revenues rise by about `$1.175T`; outlays rise by about `$278B` [SOURCE: same]
4. nominal GDP is higher by about `$8.9T` over `2024–2034` and by about `$1.3T` in `2034` [SOURCE: same]
5. through `2026`, wage growth of non-surge workers with `<=12` years of education is slightly lower than in the no-surge counterfactual [SOURCE: same]
6. inflation is almost unchanged on average, but the greatest upward pressure comes from housing [SOURCE: same]

Useful rough arithmetic:

1. `$897B / 8.7M ~= $103k` net federal deficit reduction per above-baseline surge person over the `2024–2034` window [DATA]

That is **not** a literal all-in lifetime immigrant NPV. It is a rough order-of-magnitude average of the federal effect of this specific surge scenario, including macro spillovers. [INFERENCE]

From CBO's broader 2024 outlook revision:

1. higher immigration raises real GDP growth by about `0.2pp/year` from `2024` to `2034` [SOURCE: https://www.cbo.gov/system/files/2024-02/59710-Outlook-2024.pdf]
2. real GDP is about `2%` larger in `2034` [SOURCE: same]
3. real GDP per person is about `0.8%` smaller in `2034` [SOURCE: same]
4. average real wages are slightly lower by `2034` than otherwise [SOURCE: same]

This is the cleanest official demonstration that `aggregate positive` and `per-person ambiguous/negative` can both be true at the same time. [INFERENCE]

### State/local anchor

From CBO 2025:

1. the surge added about `4.4M` residents in `2023` [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. direct state/local taxes: `$10.1B` [SOURCE: same]
3. direct state/local spending: `$19.3B` [SOURCE: same]
4. direct net cost: `-$9.2B` [SOURCE: same]
5. potential revenues: `$18.8B` [SOURCE: same]
6. potential spending: `$28.6B` [SOURCE: same]
7. potential net cost: `-$9.8B` [SOURCE: same]
8. largest direct cost buckets: `education`, `shelter and related services`, `border security` [SOURCE: same]
9. potential effects explicitly include nonbudgetary costs such as `crowded classrooms` and `crowded public transportation` [SOURCE: same]

Useful rough arithmetic:

1. `$10.1B / 4.4M ~= $2.30k` state/local taxes per added resident in `2023` [DATA]
2. `$19.3B / 4.4M ~= $4.39k` direct state/local spending per added resident [DATA]
3. `$9.2B / 4.4M ~= $2.09k` direct net cost per added resident [DATA]
4. `$9.8B / 4.4M ~= $2.23k` potential net cost per added resident [DATA]

Again, these are not permanent subgroup ledgers. They are rough per-added-resident orders of magnitude for the `2023` surge snapshot. [INFERENCE]

### Housing / inflation anchor

From IMF 2025:

1. doubling immigration lowers local inflation by about `0.1–0.2pp` [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf]
2. higher immigration lowers local `goods inflation` [SOURCE: same]
3. higher immigration raises local `housing and utilities inflation` [SOURCE: same]
4. effects are `2x–3x` larger for working-age and low-education immigrants [SOURCE: same]
5. effects on overall inflation dissipate after about a year, but housing effects can last several years [SOURCE: same]

### Local warehouse anchor

From the repo's own DuckDB warehouse:

School-heavy groups among large recent low-skill origin groups:

1. `Honduras`: about `1.2855` school-age children per linked household [DATABASE: DuckDB query on `origin_puma_household_context_2023`]
2. `El Salvador`: about `1.0600` [DATABASE: same]
3. `Mexico`: about `1.0114` [DATABASE: same]
4. `Guatemala`: about `0.9960` [DATABASE: same]

High-rent destination groups:

1. `China`: about `$1,868.99` weighted `PUMA` rent [DATABASE: same]
2. `Colombia`: about `$1,860.56` [DATABASE: same]
3. `Brazil`: about `$1,806.41` [DATABASE: same]
4. `Venezuela`: about `$1,765.18` [DATABASE: same]

[SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-local-burden-puma-layer.md]

## The decisive test

A commentator is only entitled to a broad `immigration helps us` conclusion if the following inequality is likely true on the ledger they are implicitly using:

`Delta gains = Delta macro/productivity + Delta consumer/employer surplus + Delta federal fiscal`

must be greater than

`Delta costs = Delta low-skill wage pressure + Delta state/local burden + Delta housing incidence + Delta backlash/institutional cost`

The three commentators differ mostly by which right-hand-side terms they shrink toward zero.

## Noah Smith

### Core hidden assumptions

Smith is strongest when he is making a `national macro` argument:

1. labor force growth matters
2. average native wage effects are small
3. immigration is not the main driver of recent inflation

His weak point is that he implicitly downweights:

1. local school and shelter costs
2. housing incidence on renters and service users
3. political backlash / legitimacy cost

### Decisive quantitative read

What the evidence lets him say:

1. the national macro sign is probably positive [SOURCE: CBO 2024]
2. average wage doom narratives are too strong [SOURCE: CBO 2024; research/immigration-economist-effects-matrix.md]
3. deportation is not a magical cost-of-living fix [SOURCE: IMF 2025; repo warehouse]

What the evidence does **not** let him say:

1. that the average citizen is clearly better off overall
2. that immigration is mostly unrelated to inflation in any operational sense that includes housing
3. that local burden is too small to matter

### Verdict

`Noah Smith` is `mostly right on the national ledger` and `not entitled to a full-welfare verdict`.

In a sharper formula:

1. `Delta macro + Delta federal > 0` is likely true
2. `Delta macro + Delta federal - Delta local - Delta housing - Delta backlash > 0` is not shown

Status:

1. `best of the three`
2. `still partial`

## Nicholas Decker

### Core hidden assumptions

Decker's strongest claim is that increasing returns, specialization, and dynamic gains are real.

That part is fine.

His failure is the word `must`.

To justify `immigrants must make us richer`, he needs the negative terms to be either:

1. zero,
2. second-order, or
3. guaranteed to be dominated by gains.

The available evidence does not support any of those.

### Decisive quantitative read

Against Decker:

1. there is an observed `-$9.2B` direct state/local cost in `2023` and `-$9.8B` potential cost for the surge [SOURCE: CBO 2025]
2. the repo warehouse shows meaningful school and housing heterogeneity rather than trivial local costs [SOURCE: DuckDB + repo memos]
3. CBO 2024 explicitly shows short-run wage-growth pressure for non-surge workers with `<=12` years of education [SOURCE: CBO 2024]
4. CBO's broader 2024 outlook says higher immigration can leave `real GDP` higher while `real GDP per person` is `0.8%` smaller in `2034` [SOURCE: CBO 2024 Outlook]
5. IMF 2025 shows housing inflation rises even when overall inflation falls [SOURCE: IMF 2025]

The strongest surviving version of Decker:

1. `some anti-immigration models undercount scale/productivity gains`

The failing version:

1. `therefore immigrants must make us richer`
2. `therefore the only coherent objections are political`

### Verdict

`Nicholas Decker` is `decisively wrong` if the target is current-citizen or native-local welfare.

He survives only as:

1. a reminder that static constant-returns models are incomplete

He fails as:

1. a full welfare claim
2. a claim about the space of coherent objections

Status:

1. `most overstated of the three`

## David D. Friedman

### Core hidden assumptions

Friedman is a different case.

He is not mainly saying `immigration is great because GDP`.

He is saying:

1. voluntary movement is a liberty default
2. global and migrant gains are very large
3. many objections should be handled by limiting transfers or political rights, not entry

This is intellectually stronger than Decker, because it actually changes institutions on the margin.

### Decisive quantitative read

What survives:

1. on a `global` or `migrant-welfare` ledger, freer migration probably generates very large gains [SOURCE: Friedman primary text; Clemens]
2. welfare exclusion and delayed voting rights do remove part of the transfer/political objection [SOURCE: Friedman primary texts]

What fails:

1. welfare exclusion does **not** remove schooling, shelter, roads, policing, emergency care, translation, housing pressure, or backlash
2. CBO 2025 local costs are not mostly cash welfare; they are heavily `education`, `shelter`, and `border security`
3. local housing pressure remains after transfer exclusion [SOURCE: IMF 2025]

The surviving version of Friedman:

1. `open entry with restricted transfers/political rights can reduce some of the strongest fiscal objections while preserving much of the global gain`

The failing version:

1. `therefore there is no strong economic reason for restriction`

### Verdict

`David D. Friedman` is `mostly right on liberty/global welfare`, `partly right on institutional design`, and `still wrong as a complete answer to native-local welfare`.

Status:

1. `stronger than Decker`
2. `more careful than Noah on frame`
3. `still incomplete on local-capacity economics`

## Comparative ranking

### By truth on the global ledger

1. `Friedman`
2. `Noah Smith`
3. `Decker`

### By truth on the current U.S. national ledger

1. `Noah Smith`
2. `Friedman`
3. `Decker`

### By truth on the native-local ledger

1. `Noah Smith`
2. `Friedman`
3. `Decker`

### By rhetorical overclaim

1. `Decker` worst
2. `Friedman` medium
3. `Noah Smith` least bad

## Net decision

If the question is:

`Which of the three is most defensible after quantitative tightening?`

The answer is:

1. `Noah Smith` on the national ledger
2. `David D. Friedman` on the global-liberty ledger
3. `Nicholas Decker` on neither broad ledger

If the question is:

`Does any one of them win the full argument?`

The answer is:

1. `No`

The decisive reason is simple:

1. the federal/macroeconomic gains are real
2. the local-capacity and housing costs are also real
3. none of the three fully prices both sides at once

So the repo's current best answer remains:

1. `incidence split, not scalar verdict`

## Disconfirmation

What cuts against this memo's tighter conclusion:

1. CBO's federal result is unusually favorable and could, in principle, dominate more local costs than current static comparisons suggest [SOURCE: CBO 2024]
2. local costs from the recent surge are not identical to all future low-skill immigration regimes [SOURCE: CBO 2025]
3. descendant gains and dynamic productivity gains may be undercounted in local current-year ledgers [SOURCE: NAS; research/immigration-unified-scenarios-memo.md]
4. some backlash effects may reflect perception error rather than actual local burden [SOURCE: Alesina/Stantcheva redistribution papers; Alesina/Tabellini review] [SCITE: S:1 C:0 M:12]

Those caveats weaken any `national net negative` story.
They do **not** rescue Decker's `must`, nor do they grant Noah or Friedman a full all-ledgers victory.

## Search log

Main axes used:

1. `official budget/economy`: CBO 2024 federal report; CBO 2025 state/local report
2. `relative price mechanism`: IMF 2025 immigration/local inflation paper
3. `political-economy counterweight`: Alesina/Tabellini review; redistribution literature surfaced through scite
4. `repo ground truth`: DuckDB warehouse, MEPS module, household/PUMA memos, prior named audits

Useful hits:

1. CBO 2024 gave the cleanest national/federal magnitude anchors
2. CBO 2025 gave the cleanest state/local and nonbudgetary crowding anchors
3. IMF 2025 gave the cleanest housing-versus-overall inflation split
4. the local DuckDB warehouse gave the best evidence that school and rent heterogeneity is operational, not decorative
