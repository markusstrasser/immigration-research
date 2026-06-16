# David D. Friedman immigration claims audit — 2026-04-11

## Scope

This memo audits David D. Friedman's main immigration claims against:

1. his own essays
2. official recent sources
3. recent academic review papers
4. the repo's local immigration warehouse and verified memos

This is a claim audit, not a general evaluation of Friedman as a thinker.

## Primary texts audited

1. [Libertarians and Open Borders: The Argument](http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf)
2. [Welfare and Immigration](http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html)
3. [The Conservative Mistake](http://www.daviddfriedman.com/Machinery_3d_Edition/The%20Conservative%20Mistake.htm)

## Bottom line

Friedman is stronger than most pundits because he states a real mechanism instead of just cheering for immigration.

What survives:

1. the `global` and `migrant` welfare case for freer movement is strong
2. the `voluntary transaction` argument is real
3. `welfare exclusion` and `delayed political rights` would reduce some objections

What does not survive cleanly:

1. excluding immigrants from cash welfare does **not** eliminate local school, housing, shelter, congestion, and backlash costs
2. the claim that fears of political or social deterioration lack strong reason is too broad
3. his argument tends to slide between `world welfare`, `libertarian rights`, and `current citizen welfare`

The clean verdict is:

1. `strong on global-liberty logic`
2. `partial on actual state-capacity economics`
3. `too optimistic on local and political spillovers`

## Executive table

| Claim | Verdict | Why |
|---|---|---|
| `Libertarians ought to support open borders, with possible limits on political rights and transfers.` | `Mostly survives on a libertarian/global-welfare frame` | Voluntary exchange and migrant place-premium gains are real, and welfare/voting restrictions would remove some objections. But that does not settle native-local welfare. [SOURCE: http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf] [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83] |
| `Immigration restrictions block voluntary transactions in a way private owners in a free society would not.` | `Broadly right` | This is one of Friedman's strongest points. Even with public property, entry restrictions do more than mimic private exclusion. [SOURCE: http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf] |
| `Welfare-state objections should be solved by excluding immigrants from welfare, voting, or public schools, not by excluding them from entry.` | `Partly survives, but incomplete` | That would reduce part of the transfer problem, but it leaves local public goods, emergency systems, housing markets, and nonbudgetary crowding. [SOURCE: http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html] [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: research/immigration-unified-scenarios-memo.md] |
| `Free migration disciplines redistribution by making transfer-heavy jurisdictions less viable.` | `Plausible in theory, mixed in practice` | Mobility can constrain subnational redistribution, but it can also induce re-centralization instead of shrinkage; evidence on welfare magnets exists but does not yield Friedman's broad confidence. [SOURCE: http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html] [SOURCE: https://www.nber.org/papers/w17515] [SOURCE: https://www.nber.org/papers/w26454] |
| `Critics of free immigration offer no strong reason to expect immigrants to make the country more socialist, crime-ridden, or otherwise worse.` | `Too broad` | Some alarmist versions fail, but the political-economy literature does find real backlash, redistribution effects, and institutional stress under some conditions. [SOURCE: http://www.daviddfriedman.com/Machinery_3d_Edition/The%20Conservative%20Mistake.htm] [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jel.20221643] [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md] |

## Claim 1: `Open borders are the default libertarian position`

This is Friedman's strongest claim.

What survives:

1. The core voluntary-exchange point is real. Migration restrictions stop willing workers, employers, landlords, and customers from transacting across borders. [SOURCE: http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf]
2. On a global welfare frame, labor mobility likely creates extremely large gains because moving workers from low-productivity to high-productivity places raises output sharply. Clemens treats this as one of the largest underused gains in economics. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]
3. The repo's own stance does not reject immigration on a national-output frame. It already treats migration as a possible national resilience asset under aging and labor-force slowdown. [SOURCE: research/immigration-unified-scenarios-memo.md]

What does not follow:

1. A strong `global gains` argument does not prove that current U.S. citizens in high-pressure localities are better off. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]
2. A libertarian rights claim does not answer a public-finance or local-capacity question. [FRAMING-SENSITIVE]

Verdict:

1. `Survives` on libertarian and world-welfare terms
2. `Does not settle` native-local welfare

## Claim 2: `Welfare and voting objections should be handled by limiting rights, not entry`

This is more serious than standard open-borders rhetoric because Friedman actually proposes an institutional answer.

What survives:

1. It is true that open borders do not logically require immediate voting rights or full transfer eligibility. [SOURCE: http://www.daviddfriedman.com/Ideas%20I/Libertarianism/Immigration%20Arguments.pdf]
2. Restricting access to some transfers would reduce one important class of fiscal objection. [SOURCE: http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html]
3. The repo's new `MEPS` module weakens a crude version of the medical-burden objection for working-age foreign-born adults. For ages `25-64`, foreign-born cells show lower observed annual spending than U.S.-born cells within comparable insurance buckets. [SOURCE: research/immigration-public-mvp-meps-module-2026-04-11.md]

What fails:

1. CBO 2025 shows that recent immigration surge costs at state/local level were concentrated in `education`, `shelter`, and `border security`, not just cash welfare. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]
2. The repo's local warehouse shows that some large recent low-skill origin groups are meaningfully school-heavy even after the household-weight correction: `Mexico` about `1.0114` school-age children per linked household, `Honduras` about `1.2855`, `El Salvador` about `1.0600`, and `Guatemala` about `0.9960`. [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`, query on `origin_puma_household_context_2023` run 2026-04-11]
3. The same warehouse shows high rent exposure for several large origin groups: `China` about `$1,869`, `Colombia` about `$1,861`, `Brazil` about `$1,806`, `Venezuela` about `$1,765`, and `Mexico` about `$1,593` in weighted `PUMA` rent. [SOURCE: same query family]
4. Recent IMF work finds immigration can lower local goods inflation while raising `housing and utilities` inflation. So even with welfare exclusion, housing-capacity pressure remains. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf]

Verdict:

1. `Partly right` as an institutional design point
2. `Incomplete` as an economic answer

## Claim 3: `Free migration disciplines redistribution`

This is Friedman's most interesting positive mechanism.

What survives:

1. In theory, mobility can constrain redistribution because high-transfer jurisdictions become more attractive to net recipients and less attractive to net payers. [SOURCE: http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html]
2. There is real literature on welfare magnets and migrant selection. Razin and Wahba show the generosity/mobility interaction is not imaginary. [SOURCE: https://www.nber.org/papers/w17515]
3. Evidence from Denmark also supports the welfare-magnet idea in at least some institutional settings. [SOURCE: https://www.nber.org/papers/w26454]

What cuts against Friedman's confidence:

1. Mobility can discipline `subnational` redistribution without shrinking redistribution overall; authority can also shift upward to the national or supranational level. Friedman himself notes this possibility for Europe. [SOURCE: http://www.daviddfriedman.com/Libertarian/Welfare_and_Immigration.html]
2. The question here is not only welfare generosity but local capacity. Even if transfer generosity falls, school and housing pressure can still rise. [SOURCE: research/immigration-unified-scenarios-memo.md]
3. The repo's own current findings say the main modern result is an `incidence split`, not a simple anti-redistribution gain. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]

Verdict:

1. `Plausible mechanism`
2. `Not a sufficient modern answer`

## Claim 4: `Critics offer no strong reason to expect immigrants to make the country worse`

This is Friedman's weakest major claim.

What survives:

1. Crude essentialist versions of the claim are weak. It is not generally sound to infer that people leaving bad institutions want to recreate those same institutions. [SOURCE: http://www.daviddfriedman.com/Machinery_3d_Edition/The%20Conservative%20Mistake.htm]
2. The repo has not found strong evidence that immigrants are uniquely responsible for every macro ill people like to blame on them. [SOURCE: research/immigration-noah-smith-nicholas-decker-claims-audit-2026-04-11.md]

What fails:

1. The political-effects literature does find that immigration often triggers backlash, changes redistribution preferences, and can strengthen anti-immigrant politics. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jel.20221643]
2. The repo's full-spectrum memo also treats backlash and governance costs as real channels, even when they are hard to monetize. [SOURCE: research/full-spectrum-costs-unauthorized-immigration-research-memo.md]
3. So the right reply to alarmism is not `there is no strong reason`. It is `some fears are exaggerated, but the sign and magnitude depend on scale, destination, institutional design, and local capacity`. [INFERENCE]

Verdict:

1. `Too broad`

## First-principles quantitative pass

Friedman's argument becomes much clearer if the objective function is written explicitly.

### 1. Global ledger

For a migrant who moves from a low-productivity country to a high-productivity one:

`Delta W_global ~= migrant earnings gain + employer/consumer surplus in destination - congestion and public-cost spillovers - origin-country losses`

The first term is often very large. That is why the global or migrant-welfare case for freer migration is strong. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/jep.25.3.83]

### 2. Native-local ledger

For current residents of a destination locality:

`Delta W_native_local ~= market surplus + tax revenue - school/shelter/public-service cost - housing incidence - backlash/institutional cost`

The repo's current verified stack implies:

1. `market surplus` is often positive
2. `federal effects` can be positive
3. `state/local capacity costs` can also be real and concentrated
4. `housing incidence` is mixed, not zero
5. `backlash` is real in some settings

[SOURCE: research/immigration-unified-scenarios-memo.md] [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]

### 3. What welfare exclusion changes

Friedman's proposed fix removes only part of the negative side.

If non-citizens are excluded from cash welfare and voting:

1. some transfer costs fall
2. some political channels are delayed
3. but school-age child costs, emergency systems, roads, policing, shelters, translation, and housing-market pressure do **not** disappear

That is why his institutional fix weakens the objection but does not dissolve it. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-local-burden-puma-layer.md]

### 4. Why scale matters

The first-principles mistake in many open-borders arguments is assuming the marginal immigrant under current restrictions looks like the average immigrant under much looser restrictions.

Friedman is right that freer movement creates big gains.
He is not entitled to assume:

1. the destination mix stays benign at much larger scales
2. local housing supply expands fast enough
3. school and shelter systems remain below convex-capacity thresholds
4. backlash is small enough to ignore

This is exactly where the repo's local warehouse matters. It already shows large differences in school-age burden and rent exposure across origin groups and destination mixes. [SOURCE: `sources/immigration-fiscal/data/derived/immigration_context.duckdb`] [SOURCE: research/immigration-household-weighted-correction.md] [SOURCE: research/immigration-local-burden-puma-layer.md]

## Net verdict

If the question is `is Friedman right on the moral and global-welfare case for much freer migration?`

1. `Mostly yes`

If the question is `has Friedman solved the citizen-welfare and local-capacity problem by proposing welfare exclusion and delayed voting?`

1. `No`

If the question is `does his best argument survive after quantitative tightening?`

1. `Partially`
2. The strongest surviving version is `freer migration likely creates large global gains and can be made less fiscally dangerous by limiting transfers and political rights`.
3. The strongest failing version is `there is therefore no strong economic reason for restriction`.

The repo's current answer remains:

1. `incidence split, not scalar verdict`
