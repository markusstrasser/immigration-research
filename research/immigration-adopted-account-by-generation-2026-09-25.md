# The adopted account by generation

**Verdict (2026-10-21, main case v9):** On the main case of $368.0–436.6bn a year
([decision](../decisions/2026-10-16-main-case-v9.md), ladder 311), all three generations remain net costs to other
US residents. That holds at both ends of the case, under both ways of counting children, and when benefits are
counted as paid; the v9 split runs only the case's two end specifications. The completed union, the native-minor
calibration and the constructed Census coverage correction enter the 44.90M-person lineage; nonreporting
descendants and the completed reporter/child block count in the third-plus.
- **Counted with their parents** (NAS): the Mexico-born cost others $174.6–198.0bn a year ($15.9–18.0k per adult),
  the second generation $92.5–113.0bn ($9.6–11.8k per adult) and the third-plus $100.9–125.6bn ($9.5–11.8k per adult).
  The lineage has 31.23M adults among its 44.90M members.
- **Counted in their own generation:** $61.2–81.3bn, $142.7–164.5bn and $164.1–190.8bn, respectively.
- **Counting benefits when paid** (the cash set, $284.4–352.9bn): with their parents $159.4–182.7bn,
  $54.7–75.3bn and $70.3–94.9bn; in their own generation $45.9–66.0bn, $105.0–126.7bn and $133.5–160.2bn.

The case reads every generation at the personal allocation at both ends. Domestic-source business-capital taxes
follow the generation's industry key. The non-members who stay in mixed units have their own returns and benefits
recomputed; their consumption and owner-property response remains assumed [FRAMING-SENSITIVE]. Coverage and mixed-unit
post-engine amounts retain their declared generation parts; covered people take zero on administrative-use justice
keys. Items 16 and 17 take their declared generation parts, item 21 follows item 13's health lines, and the other v9
items follow each line's existing generation amounts. The third-plus's cost per member under own-generation counting
is $8,912 / 10,360. The pension switch, set less cash, is $83.6bn overall at both ends.

[ASSUMPTION] The pension and education/user-fee parts retain their source routing. Under (b), nonreporting
descendants whose parents cannot be observed stay in third-plus; observed completion children follow their source
records. The alternative placement of unlocated descendants' minors is not separately priced on v9.
[CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md),
`run_generations_v9.cjs` → `derived/generation_results_oct16.csv`, `generation_results_oct16_cash.csv`,
`generation_summary_oct16.json`, a24d2468. The pension switch is the set's results less the cash set's.] [FRAMING-SENSITIVE]

| $bn a year, low / high end | (a) own generation | (b) minors with parents |
|---|---|---|
| G1, born in Mexico | 61.2 / 81.3 | 174.6 / 198.0 |
| G2, US-born, a parent born in Mexico | 142.7 / 164.5 | 92.5 / 113.0 |
| G3+, US-born of US-born parents, with the added people | 164.1 / 190.8 | 100.9 / 125.6 |
| All three (the main case) | 368.0 / 436.6 | 368.0 / 436.6 |

The ends are specifications 16 and 11, both personal, the case's low and high readings, with public capital at
the one Trustees rate at both (item 20). Controlled rounding makes every column add: G2's low end under (a) is shown as 142.7
instead of its nearest 142.8. Per-member figures divide by each generation's completed and covered population
(18.41M in third-plus under (a)). Constructed coverage counts are an assumption, not observed individual records.
State pricing applies the union's price indexes to each generation's keys; indexes from each generation's own
state mix are not computed. The prose generation totals also use controlled rounding to add to their case totals.

The record is one year of the people alive in 2024, and it cannot say what today's children will pay as adults.

## 1. The split

Net cost to other US residents, $bn a year, income year 2024, at the two ends of main case v9 (specifications 16
and 11, both personal). Members and adults are the completed and covered lineage's, including the constructed
coverage people. CPS allocations are measured; service responses and the production term are assumed.

| (b) Minors with their parents (NAS 2017) | Members (m) | Adults (m) | Low end | High end | $ per adult, low / high |
|---|---:|---:|---:|---:|---|
| G1, born in Mexico | 16.13 | 11.01 | 174.6 | 198.0 | 15,868 / 17,992 |
| G2, US-born, a parent born in Mexico | 13.33 | 9.61 | 92.5 | 113.0 | 9,618 / 11,752 |
| G3+, US-born of US-born parents | 15.44 | 10.61 | 100.9 | 125.6 | 9,509 / 11,830 |

| (a) Children in their own generation | Members (m) | Adults (m) | Low end | High end | $ per member, low / high |
|---|---:|---:|---:|---:|---|
| G1 | 11.48 | 11.01 | 61.2 | 81.3 | 5,329 / 7,083 |
| G2 | 15.01 | 9.61 | 142.7 | 164.5 | 9,512 / 10,959 |
| G3+ | 18.41 | 10.61 | 164.1 | 190.8 | 8,912 / 10,360 |
| All three | 44.90 | 31.23 | 368.0 | 436.6 | 8,196 / 9,722 |

[CALCULATION: `derived/generation_results_oct16.csv`, `population`, `adults`, `cost_bn`, `per_adult_usd`,
`per_member_usd`; the all-three row is the case, `main_case_2026_10_16/derived/summary.json` `v9.band_bn`,
`v9.per_member_usd.set`]

The generations add to the main case at both ends and under both conventions (the summary's closure gate).
Convention (b) follows the brief: minors go to the generation of their co-resident parents in the group (split
50/50 across two generations), else to the oldest adult relative in the group. NAS also moves some dependents aged
18–23, so (b) leaves slightly more college cost with the second generation than NAS would. [SOURCE: NASEM (2017),
pp. 377, 387–388, verified in the local copy; CALCULATION: lane `mixed_units.py` → `derived/minors_convention_b.csv`]

None of these figures is age-standardized. Under (a), per adult is not a per-parent figure, because 5.4m of the
second generation are minors.

## 2. What moves it

- **Where children count.** Moving minors to their parents' generation shifts $113–117bn onto the first
  generation. Under (b) a second-generation adult with their minor children costs others 61–65% of what a
  Mexico-born adult does.
- **The household allocation rule.** The case reads every generation at the personal allocation, so the swap
  between shared and personal rules that moved costs between the first and third-plus generations on the
  September 24 case is not part of the v9 split. The shared allocation is a whole-case companion and is not split
  by generation. The non-members who stay in mixed units are recomputed (the verdict above). [FRAMING-SENSITIVE]
- **The production term** has no unique split, since the CES block is not linear. The v9 split carries the case's
  declared production parts by generation; the alternative attributions measured on the September 24 case (first
  order, total labor income) are not rerun on v9.

[CALCULATION: `derived/generation_results_oct16.csv`, (b) minus (a) G1 `cost_bn`; (b) G2 over G1 `per_adult_usd`;
`generation_summary_oct16.json` `routing`]

## 3. Beside the September 19 generation ledger

The ledger in `ledger_absolute_2026_09_17` measures each generation against third-plus non-Hispanic
whites of the same age. With the income tax the survey misses on the main case's keys (item T, ladder
296), its gaps are −$8,849, −$8,499 and −$7,118 per person. This split measures what each generation
costs everyone else under the adopted account, with no reference group. The two are different objects,
and neither is scaled onto the other. [CALCULATION: lane `compare_ledger.py` →
`derived/ledger_comparison.csv`, ledger columns, the ledger read through its hash-checking loader]

- At the groups' own ages the reference whites are net contributors under the shared allocation
  (+$3.8k to +$5.6k per person), so there a gap exceeds the group's own balance (−$5,633, −$5,706 and
  −$3,688). Under the personal allocation the own balances are −$3,086, −$6,388 and −$6,600, and at the
  third-plus's ages the whites run −$1.3k, so its gap (−$5,261) is smaller than its balance.
- The account's personal allocation puts the Mexico-born lowest at both ends: $5,329 / 7,083 per member,
  against $9,512 / 10,959 for the second generation and $8,912 / 10,360 for the third-plus.
  [DATA: `derived/generation_results_oct16.csv`, convention (a), `per_member_usd`]
- The two are not compared balance for balance. The live case prices the completed and covered 44.90M-person
  lineage, and its runner writes no bridge to the ledger's populations.

The FAQ's combining rule still applies: the ledger's generation gaps must not be scaled onto the
$368.0–436.6bn. This split is computed directly on the account.

## 4. What it does not answer

"Their children pay it back" concerns future taxes of today's children. It needs a cohort account
with the corrections carried into it; this one-year split cannot test it. Today's third-plus adults
descend mostly from arrivals before about 1970, so the step from second to third-plus is not a
forecast for the grandchildren of recent arrivals ([FAQ](immigration-objections-faq-2026-09-21.md)
entry 5).

The generation boundary rests on reported parents' birthplaces. 54% of group members (75% of adults)
live without a linked parent; their items are allocated for 4.8%, and where a parent is present the
report agrees with the parent's own birthplace 96.4% of the time. A disagreement rate of about 3–5%
likely applies to the unchecked majority and falls on the G2/G3+ boundary. [CALCULATION: lane
`parents_check.py` → `derived/parent_birthplace_check.csv`]

**Would change it:** measured benefit receipt and justice use by parents' birthplace; a counterfactual
production model; a change to the main case itself, which moves every generation.

## Sources

- Lane: [`generation_account_2026_09_24`](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md)
  (brief, `run_all.sh`). Inputs: main case v9 (`main_case_2026_10_16`, `package.cjs`, `derived/corrections.json`),
  the account's CPS ASEC 2025 frame and keys, the September 19 ledger. [DATA]
- Live v9 split: `run_generations_v9.cjs` → `derived/generation_{results,summary,corrections}_oct16{,_cash}.*`
  (a24d2468); source, generation and post-engine closures match the live case. The lane's replay of 2026-10-20
  (`scripts/rerun_lane.py`, `run_all.sh`) is byte-identical. [CALCULATION]

## Revisions

- 2026-10-21 (main case v9, [decision](../decisions/2026-10-16-main-case-v9.md), a24d2468): the verdict, §1 and §2
  follow `oct16`. With their parents the generations cost $174.6–198.0bn, $92.5–113.0bn and $100.9–125.6bn (v8:
  $154.8–185.9bn, $99.2–126.0bn, $111.8–144.1bn), so the first generation's cost rises and the US-born generations'
  falls. The v9 split runs only the case's two ends, so
  the claim that every generation is a net cost at all 32 personal specifications is now stated at both ends. §§1–2,
  which had kept the September 24 record (finding: it read as the adopted split), now give the live split; the
  September 24 allocation swap, correction split and production attributions are not rerun on v9, so their
  numbers are dropped and the points kept. Concept affected: the adopted account's split by generation (ladder 224).

- 2026-10-15 (corrected main case v8, [decision](../decisions/2026-10-15-main-case-v8.md)): the living case figures and source pointers follow the completed reporting union and central Census coverage correction, with domestic-source corporate taxes and the mixed-unit stayers recomputed. Concept affected: the live annual account and its population.

- 2026-10-14 (main case v7, [decision](../decisions/2026-10-14-main-case-v7.md)): live case figures and their source paths now use `oct14`, at the personal allocation at both ends, with mixed-unit child credits, taxes on job capital and the two measured frame/key corrections. Phase 1 updates committed sources; pending comparator and distribution consumers await their committed reruns. Concept affected: the live account and its companions.

- 2026-10-08, later: §3 rewritten to the live case, because the operator's rule keeps living text on the live case
  and the live case has no ledger bridge. The body now carries item T on the ledger side: gaps −$7,584, −$7,521 and
  −$6,195 → −$8,849, −$8,499 and −$7,118; the reference whites at the groups' ages +$2.5–3.9k → +$3.8–5.6k; own
  balances −$5,929, −$5,881 and −$4,223 → −$5,633, −$5,706 and −$3,688, with the personal −$3,086, −$6,388 and −$6,600
  added, and with them the one case where the gap is smaller than the balance (the third-plus under the personal
  allocation, whose whites run −$1.3k). The September 24 account figures (own balances −$5,220, −$5,703 and −$3,859; the $1.7–3.0k excess at average
  cost; the $2.2–2.7k taken off by the responses) and the dated bracket are deleted, so the "close to this account's"
  claim goes with them. The orderings are checked on the live split instead ($8,158, $8,779 and $10,493 a member at the
  low end; $7,852, $12,419 and $11,323 at the high end), the combining rule names $389.1–461.5bn where it named
  $201–246bn, and the note that §§1–4 are the September 24 record now excepts §3. Concept affected: the comparison with the September 19 generation ledger (ladder 224).

- 2026-10-08, item T: added a dated bracket to §3 with the ledger's current figures, because the white-reference
  ledger's expanded account now charges the income tax the survey misses on the main case's keys (item T;
  [decision](../decisions/2026-10-07-ledger-item-t-income-tax-keys.md)): the generation gaps −$7,584, −$7,521 and
  −$6,195 → −$8,849, −$8,499 and −$7,118; the reference whites at the groups' ages +$2.5–3.9k → +$3.8–5.6k; the
  ledger's own balances −$5,929, −$5,881 and −$4,223 → −$5,633, −$5,706 and −$3,688. Both orderings hold. §3 stays
  the September 24 record: its account side is that case's, and the live case has no ledger bridge, so the
  comparison itself is not restated. Concept affected: the comparison with the September 19 generation ledger
  (ladder 224).

- 2026-10-08: living text states only the live case, at the operator's request; earlier-case figures removed,
  recoverable at 0e0c5e28.

- 2026-10-07 (main case v6, [decision](../decisions/2026-10-07-main-case-v6.md), ladder 295): the split now runs on
  the main case of $389.1–461.5bn (commits 3f583fb4, 8e7b875f), with the cash set beside it. The October 5 case stays
  below as the earlier case.
  - The 2026 Trustees paths lower every generation's cost, and the added people's measured ages raise the third-plus's
    alone. Counted in its own generation the third-plus costs $142–197bn (was $142–195bn); with its parents
    $111–144bn (was $110–142bn). All three remain net costs at every specification, also on the cash set.
  - User fees and the education keys go to each generation by the education line's shares, Pell and the K-12
    weight's two parts included [ASSUMPTION]; the added people's adults are at their measured age mix.
  - Concept affected: the adopted account's split by generation (ladder 224). Under (b) the third-plus now costs more
    than the second generation at the low end too, $110.7bn against $109.5bn, where on October 5 the second generation
    led by $0.1bn. Under (a) the order is unchanged: the second generation leads at the low end and the third-plus at
    the high end.

- 2026-10-05, later (main case v5, [decision](../decisions/2026-10-05-main-case-v5.md), ladder 281): the split now
  runs on the main case of $390.3–461.2bn (commits e5ca5efe, 86af8f7e), which counts the 3.04M descendants who no
  longer report Mexican origin as whole people, with the cash set beside it.
  - The added people go on the third-plus: counted in its own generation it costs $142–195bn (was $123–168bn), with
    its parents $110–142bn (was $91–116bn). The Mexico-born and the second generation move only by the larger group's
    responses, by about $0.1bn. All three remain net costs at every specification, also on the cash set.
  - Per-person figures divide by the lineage's 42.75M members and 29.4M adults; the third-plus's cost per member falls,
    because an added person costs less than an identified member.
  - Concept affected: the adopted account's split by generation (ladder 224). At the high end the third-plus again
    costs more than the second generation under both conventions: under (a) $195.0bn against $179.2bn, under (b)
    $142.2bn against $121.7bn. At the low end the second generation still leads, under (b) by $0.1bn ($110.56bn
    against $110.46bn).
- 2026-09-29, later (main case v4, [decision](../decisions/2026-09-29-main-case-v4.md), ladder 275): the split now
  runs on the main case of $371.4–434.8bn (commit aa1f53b), with the cash set beside it.
  - Every generation's cost rises, and all three remain net costs at every specification, also on the cash set.
  - Counted with their parents, the Mexico-born cost $169–197bn, the second generation $111–122bn and the
    third-plus $91–116bn; per person on the account's row-4 counts.
  - The pension switch lands mostly on the US-born generations under the own-generation count.
  - Concept affected: the adopted account's split by generation (ladder 224). At the high end the second generation
    now costs more than the third-plus under both conventions: under (a) $179.3bn against $168.4bn, where on
    September 27 the third-plus led by $3.1bn; under (b) $121.8bn against $115.6bn, where the third-plus led by
    $6.6bn. The low-end ordering is unchanged.
- 2026-09-27 (the return on public capital, long-run roads and parks, rental assistance and enterprises,
  [decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md)): the split now runs
  on the main case of $321.8–387.4bn (commit 8654a0c).
  - Every generation's cost rises, and all three remain net costs at every specification.
  - Counted with their parents, the Mexico-born cost $159–191bn, the second generation $87–95bn and the
    third-plus $75–102bn.
  - Concept affected: the adopted account's split by generation (ladder 224). The ordering under each
    convention is unchanged. Under (a) the third-plus now lead the second generation at the high end by
    $3.1bn ($156.1bn against $153.0bn), where the margin was $0.1bn.
  - Inherited, not repaired: the rental-assistance keying defect of the conceptual audit (§7, about $0.2bn
    on the whole case) passes into each generation.
- 2026-09-26 (schools at full average cost, [decision](../decisions/2026-09-26-main-case-schools-full-cost.md)):
  the split now runs on the main case of $258.5–292.0bn (commit 2441ac8).
  - Every generation's cost rises, and all three remain net costs at every specification.
  - Counted with their parents, the Mexico-born cost $136–155bn, the second generation $66–68bn
    and the third-plus $55–71bn.
  - The earlier-in-the-day case (finite-removal responses and the consumption key) is the first-year
    budget response, within $1bn of September 24 for every generation.
  - Concept affected: the adopted account's split by generation (ladder 224). The ordering under
    each convention is unchanged: under (b) the Mexico-born cost most, and under (a) the second
    generation costs most at the low end and the third-plus at the high end, though only by $0.1bn
    ($117.6bn against $117.5bn).
- 2026-09-29 (cleanup, [decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md)): the schools-case and
  September 24 verdicts became one table of earlier cases. The verdict's G1 per adult is on the 39.7M the account
  prices, $15.0–18.1k (was $13.6–16.3k on the CPS's 40.9M), and §1 gives the September 24 table on that count
  (ladder 274). Concept affected: the per-member and per-adult denominators; no dollar total changes.
