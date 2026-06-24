# Immigration reasoning evolution — 2026-04-21

**Purpose:** Record how the repo's immigration reasoning changed across this cycle, including where later falsification forced a real correction.  
**Status note:** This is a narrative reconstruction from dated memos, local review artifacts, and the current git history. It is not a formally versioned decision log. Treat chronology claims as `[INFERENCE]` unless a dated artifact or commit is named explicitly.  
**Instrument note:** Politically charged topic; keep the raw artifacts in view and do not treat this file as a neutral substitute for them. [SOURCE: notes/llm-bias-caveat.md]

## Artifact basis

1. [immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md](research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md)
2. [immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md](research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md)
3. [immigration-threshold-first-panel-2026-04-21.md](research/immigration-threshold-first-panel-2026-04-21.md)
4. [immigration-threshold-causal-levers-2026-04-21.md](research/immigration-threshold-causal-levers-2026-04-21.md)
5. [immigration-county-outcome-panel-2026-04-21.md](research/immigration-county-outcome-panel-2026-04-21.md)
6. [immigration-capacity-frontier-2026-04-21.md](research/immigration-capacity-frontier-2026-04-21.md)
7. [.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md](.model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md)
8. [immigration-capacity-falsification-2026-04-21.md](research/immigration-capacity-falsification-2026-04-21.md)
9. [.model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md](.model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md)
10. commit `2cdd801` (`[analysis] Measure capacity frontier — compare stock flow and load`) [SOURCE: git history]
11. commit `1097c77` (`[research] Audit Bryan Caplan claims — score open-borders arguments`) [SOURCE: git history]
12. [immigration-frontier-rethink-2026-04-22.md](research/immigration-frontier-rethink-2026-04-22.md)
13. [immigration-receiver-failure-atlas-2026-04-22.md](research/immigration-receiver-failure-atlas-2026-04-22.md)
14. [immigration-resident-weighted-exposure-2026-04-22.md](research/immigration-resident-weighted-exposure-2026-04-22.md)
15. [immigration-open-borders-break-even-bounds-2026-04-22.md](research/immigration-open-borders-break-even-bounds-2026-04-22.md)
16. [immigration-receiver-counterfactuals-2026-04-22.md](research/immigration-receiver-counterfactuals-2026-04-22.md)

## Starting point: stop answering the scalar question

The initial attractors were all too coarse:

1. `open borders create huge gains`
2. `immigration hurts locals`
3. `economists disagree`

The real improvement started when the repo stopped answering the scalar question and split the ledgers:

1. `global`
2. `national aggregate`
3. `destination per capita`
4. `native local` [SOURCE: research/immigration-smith-decker-friedman-comparative-quantitative-audit-2026-04-11.md]

That was the first durable move from rhetoric toward incidence. [INFERENCE]

## Phase 1: open-borders rhetoric gets bounded

Reading the actual open-borders papers moved the repo from:

1. `freer migration might double world GDP`

to:

1. `large global gains remain plausible`
2. `literal doubling is not a realistic central forecast`
3. `the optimistic result depends on rich-country capacity staying largely intact` [SOURCE: research/immigration-open-borders-double-world-gdp-and-apartheid-audit-2026-04-21.md]

This was the first place where destination capacity became a first-order part of the reasoning rather than an afterthought. [INFERENCE]

## Phase 2: surge regime breaks the old evidence hierarchy

The repo then stopped treating pre-2020 Card/Borjas-style marginal labor shocks as the whole game. The `2021–2024` surge pushed the evidence search toward:

1. shelter saturation
2. state/local budgets
3. housing absorption
4. backlash under concentrated arrivals [SOURCE: research/immigration-causal-surge-2021-2024.md]

That reframed the project from `average wage effect` toward `flow x capacity x composition x regime`. [INFERENCE]

## Phase 3: the threshold object changes from stock to capacity

The first threshold pass did not confirm the naive `% foreign-born crosses X` story. Instead it pointed toward:

1. `permit throughput` for wage-side pressure
2. `rent burden` for local sorting pressure
3. `shelter stock and assignment regime` for receiver-city crisis cases [SOURCE: research/immigration-threshold-first-panel-2026-04-21.md] [SOURCE: research/immigration-threshold-causal-levers-2026-04-21.md]

This is where the repo’s threshold reasoning stopped being about population composition alone and started being about constrained absorption. [INFERENCE]

## Phase 4: county outcomes narrow the labor story

The county outcome panel then made the labor-incidence story less rhetorical and more specific:

1. wage growth slows in high-immigration low-permit counties
2. broad employment collapse does not show up cleanly in the first coarse split
3. an IRS domestic-migration aggregate initially looked more affordability-sensitive than the first permit split, but later review showed that channel is not a native-incumbent-only measure and should not anchor native-sorting claims without relabeling [SOURCE: research/immigration-county-outcome-panel-2026-04-21.md] [SOURCE: sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv] [SOURCE: sources/immigration-causal/data/internal_migration/county_outflow_2022_23.csv]

At this stage the best internal summary became:

1. `the local problem is not generic job collapse`
2. `it is slower wage progression plus capacity strain plus sorting`

## Phase 5: capacity frontier sharpens the stress object

The frontier pass, committed in `2cdd801`, compared stock, flow, and load more directly and pushed the repo toward:

1. `stock share` for broad backlash
2. `flow-to-build-capacity` for wages, employment, and local sorting pressure [SOURCE: research/immigration-capacity-frontier-2026-04-21.md] [SOURCE: git history]

This was a real reasoning upgrade, but it also created a new temptation: to overread a strong descriptive stress object as a clean causal threshold. [INFERENCE]

## Phase 6: the first falsification draft over-narrowed for a real reason and a bad reason

The first falsification pass was directionally valuable because it tried to kill the new capacity story. But it made a real error:

1. it treated `2021–2022` overlap windows as placebo/pretrend evidence
2. it used a post-treatment permit denominator in the earlier-window section [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]

That led to an overly broad downgrade:

1. `high-load counties were already weaker`
2. `the strongest causal reading basically fails`

The critique was correct to reject that wording. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]

## Phase 7: critique-close forces the real correction

`/critique close` produced the key correction artifact:

1. the placebo semantics were wrong
2. the threshold sign-stability metric was misstated
3. zero-permit exclusion needed to be explicit
4. geographic robustness needed to be stronger than leave-one-state-out [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md]

That is the pivot where the reasoning evolution stops being just “more evidence” and becomes “error correction changed the conclusion.” [INFERENCE]

## Phase 8: corrected falsification narrows the story, but does not cleanly settle the labor split

After rebuilding the county panel with `2017–2024` QCEW, adding machine-readable window metadata, and rewriting the falsification script around a true `2017–2019` permit baseline, the corrected picture is:

1. the descriptive load/capacity marker survives permutations, leave-one-division-out, and monotonicity [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
2. the two clean annual pre-COVID wage windows do not line up: `2017–2018` is positive while `2018–2019` is weak negative, so the annual wage channel is not cleanly identified from this panel [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
3. both clean annual pre-COVID employment windows are already negative, which keeps employment more suspicious than wages in the annual design [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
4. post-`2023–2024` wage and employment effects still survive annual controls, but the clean annual windows do not justify treating either channel as settled causal identification [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]
5. the IRS `97/000` layer is total domestic migration, not a native-incumbent-only series, so the corrected falsification pass quarantines that channel from the main claim set [SOURCE: research/immigration-capacity-falsification-2026-04-21.md] [SOURCE: sources/immigration-causal/data/internal_migration/county_inflow_2022_23.csv]

This is the current best correction:

1. `descriptive stress-marker claim`: survives strongly
2. `wage-side surge amplification`: still plausible, but not cleanly identified from the annual county panel
3. `employment-side surge amplification`: more suspicious because the clean presurge employment windows are already negative
4. `wage-versus-employment causal split from the annual panel`: not settled
5. `generic county threshold story across all outcomes`: too strong

## Phase 9: the threshold claim gets demoted, not killed

The corrected threshold search no longer supports a sweeping “real threshold family” line. It now supports:

1. wage-search performance that beats a null search
2. a **diffuse** cutoff surface rather than one stable breakpoint
3. poor transfer to margin
4. only moderate transfer to employment [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]

So the repo did **not** end at:

1. `thresholds are fake`

It ended at:

1. `threshold-search evidence exists for wages, but stable cutoff location does not`

## What the repo now actually believes

The current best position is:

1. `global-gains arguments survive only at bounded margins and with capacity caveats`
2. `destination-country incidence is mostly a capacity problem, not a stock-share problem`
3. `county flow/capacity is a strong stress marker`
4. `the annual county panel does not cleanly identify the wage channel, and employment remains more obviously confounded by presurge weakness`
5. `receiver-city synthetic controls remain the best next causal design`
6. `IRS domestic migration can still be useful descriptively, but not as a native-sorting claim without additional identification`

## Phase 10: the frontier itself gets demoted and rebuilt

The new rethink does not mainly add another result. It changes what counts as the frontier:

1. the annual county panel is demoted from would-be causal arbiter to `screening surface` [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
2. the main next causal object becomes `receiver-node saturation`, not another county threshold [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
3. the main next measurement repair becomes `resident-weighted incidence`, not median-county descriptive ratios [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]
4. the main next formalization move becomes `bounds and necessary-condition tests`, not increasingly fragile point-identification rhetoric [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]

This is a deeper shift than another robustness check. It says the previous unit of analysis likely reached diminishing returns. [INFERENCE]

## Phase 11: the new frontier gets executed

The rethink did not stay abstract for long. The first execution pass immediately did three things:

1. it built a receiver-node failure atlas and showed that `Denver` is the clearest multi-year physical saturation case, `NYC` the strongest all-around stress node, and `Boston` a high-cost regime case even below physical shelter saturation [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md]
2. it repaired the newcomer framing by switching from county medians toward resident-, renter-, and child-weighted exposure, which shrank the domestic-vs-abroad newcomer ratio sharply for the typical resident [SOURCE: research/immigration-resident-weighted-exposure-2026-04-22.md]
3. it translated the conservative open-borders baseline into break-even loss bounds and housing requirements, making the global-gains debate more explicitly falsifiable [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md]

That is the first time the repo has had all three ledgers moving together:

1. receiver-node overload
2. resident-weighted destination incidence
3. bounded global-gains math

This is closer to the real target than any one county panel by itself. [INFERENCE]

## Phase 12: the first receiver counterfactuals narrow again

The next obvious question was whether the receiver-node stories survive synthetic-control style counterfactuals against the national CoC panel. The answer is:

1. `Denver` survives as the clearest positive physical-overload divergence [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md]
2. `Chicago` comes back once the design checks absolute counts instead of only `PIT/HIC` ratios; it looks like an absolute-load divergence case rather than a pure shelter-saturation-ratio case [SOURCE: same]
3. `Boston` still does not survive as a physical-overload case in the public shelter panel, which pushes it harder into the regime-cost and service-load bucket [SOURCE: same]
4. `NYC` still looks substantively real but the synthetic fit is too concentrated on a tiny donor set to support strong causal rhetoric [SOURCE: same]
5. the ratio-placebo universe is too noisy for these synthetic controls to count as decisive inference [SOURCE: same]

So the repo learns two things at once:

1. the receiver frontier was still the right move
2. even that better object does not yet yield one clean final estimator

That is still progress because it kills a false simplification. [INFERENCE]

## Why this file exists

Without this trace, later work can easily flatten two different things into one:

1. `we changed our mind because new data arrived`
2. `we changed our mind because a critique found a real bug in our reasoning`

Both happened here. The second one matters more. [INFERENCE]

## Revisions

### 2026-04-22

The first draft of this file narrated the earlier falsification pass as if its “pretrend” downgrade were already sound. After the corrected county panel and first review artifacts landed, the file was rewritten to distinguish the bug-triggered correction from the evidence that still survives after that correction. A later review forced one more downgrade: the annual design needed a second clean pre-COVID window and an explicit `2017–2019` permit baseline. Once that extension landed, the annual wage windows no longer supported a clean causal reading either, while employment stayed negative in both clean presurge windows. [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-83e8f8/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-final-36f586/verified-disposition.md] [SOURCE: .model-review/2026-04-22-immigration-capacity-falsification-close-47cf93/verified-disposition.md] [SOURCE: research/immigration-capacity-falsification-2026-04-21.md]

Later the same day, the frontier was explicitly reframed again. Instead of trying to rescue the annual county panel with more threshold work, the repo wrote down a new next frontier: receiver-node saturation, resident-weighted local incidence, and bounded claim tests. [SOURCE: research/immigration-frontier-rethink-2026-04-22.md]

Later still, that frontier was partially executed rather than merely proposed: the receiver atlas, resident-weighted exposure repair, and open-borders break-even bounds all landed as repo-owned artifacts. [SOURCE: research/immigration-receiver-failure-atlas-2026-04-22.md] [SOURCE: research/immigration-resident-weighted-exposure-2026-04-22.md] [SOURCE: research/immigration-open-borders-break-even-bounds-2026-04-22.md]

One step after that, the repo finally ran the receiver synthetic controls it had been pointing toward and then reran them with a stronger donor-exclusion list and absolute-count outcomes. That sharpened the split again: `Denver` stayed the cleanest physical-overload survivor, `Chicago` reappeared on absolute load once denominator endogeneity was checked, `Boston` stayed a non-overload high-cost case, and `NYC` remained directionally real but match-fragile. The restraint also survived: ratio-placebo rankings were still too weak for decisive synthetic-control proof. [SOURCE: research/immigration-receiver-counterfactuals-2026-04-22.md]
