# The adopted account by generation

**Verdict (2026-10-07, main case v6):** On the main case of $389.1–461.5bn a year
([decision](../decisions/2026-10-07-main-case-v6.md), ladder 295), which counts the 3.04M descendants of Mexican
immigrants who no longer report Mexican origin as whole people at their measured ages, all three Mexican-origin
generations remain net costs to other US residents. That holds at every one of its 64 specifications, under both ways
of counting children, and when benefits are counted as paid. The added people are counted in the third-plus
generation.
- **Counted with their parents** (NAS): the Mexico-born cost others $169–197bn a year ($16.0–18.6k per adult of the
  29.3M adults among the lineage's 42.75M members), the second generation $109–121bn ($12.3–13.5k per adult) and the
  third-plus $111–144bn ($11.3–14.7k per adult).
- **Counted in their own generation:** $87–97bn, $150–178bn and $142–197bn.
- **Counting benefits when paid** (the cash set, $307.4–385.4bn): with their parents $150–183bn, $78–86bn and
  $80–117bn; in their own generation $73–87bn, $118–143bn and $102–169bn.

Of the case's four newest items under (a), printed at controlled rounding so the parts add
(retiree health's 0.584 shows as 0.59, the US-born's 0.815 as 0.82), the 2026 Trustees paths take $0.34 / 0.42bn from the
Mexico-born, $1.19 / 1.20bn from the second generation and $1.32 / 1.04bn from the third-plus. The added people's
measured age mix adds $1.35 / 2.86bn to the third-plus alone. Retiree health adds $0.59 / 0.77bn across the
generations. User fees take $0.30 / 0.73bn: the US-born generations' cost falls by $0.25 / 0.82bn and the
Mexico-born's moves by −$0.05 / +0.09bn. Each item is counted after the ones before it, so the case's interactions sit
with the later item. The third-plus's cost per member is $8,158 / 11,323. The pension
switch, the set less the cash set, is $9.7 / 14.0bn for the Mexico-born, $32.7 / 34.8bn for the second generation and
$39.3 / 27.3bn for the third-plus.

[ASSUMPTION] The pension item's union parts go to each generation by the pension lane's per-generation rows. The
user-fee item goes by each generation's share of its split-basis line: the education line for every part but the two
health parts. Pell follows it because it goes to students, though it sits on other federal benefits, and so do the
K-12 weight's two parts. Split by Pell's own line instead, the Mexico-born would move by +$0.07 / +1.01bn, the second
generation by −$0.47 / −0.87bn and the third-plus by +$0.40 / −0.14bn under (a). Under (b) the added people stay in
the third-plus, since their parents' generation is not observed; had their minors moved to the second generation as
the identified third-plus's do, about $5.2 / 9.3bn would move from the third-plus to the second, an indication rather
than a bound.
[CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md), section "v6 case
(oct07)": `run_generations_v6.cjs` → `derived/generation_results_oct07.csv`, `generation_results_oct07_cash.csv`,
`generation_summary_oct07.json` (`change_from_oct05_by_item`, `b_rule_indication`, `sensitivities`); commits
3f583fb4, 8e7b875f; the pension switch is the set's results less the cash set's] [FRAMING-SENSITIVE]

| $bn a year, low / high end | (a) own generation | (b) minors with parents |
|---|---|---|
| G1, born in Mexico | 96.9 / 86.7 | 168.9 / 196.8 |
| G2, US-born, a parent born in Mexico | 150.4 / 178.0 | 109.5 / 120.6 |
| G3+, US-born of US-born parents, with the added people | 141.8 / 196.8 | 110.7 / 144.1 |
| All three (the main case) | 389.1 / 461.5 | 389.1 / 461.5 |

The ends are specifications 48 (shared allocation, the lower capital return and the low long-run readings) and 11
(personal, the higher return and the high readings), and every cell is at its nearest rounding. Per-person figures
divide by the row-4 counts, the third-plus's with the added people (17.38M members under (a)). The added people's
adults are measured, 1.61M of the 3.04M [ASSUMPTION: the 15–19 band's adults at the identified third-plus's share,
APPROX]. State pricing applies the union's price indexes to each generation's keys; indexes from each generation's own
state mix are not computed.

Sections 1–4 below are the September 24 record. It is one year of the people alive in 2024, and it cannot
say what today's children will pay as adults.

## 1. The split

Net cost to other US residents, $bn a year, income year 2024, at the two ends of the adopted main
case. The low end is the shared allocation with GDP normalization, school share 0.865 at response
0.63, general government 0.59 and low uncompensated care; the high end is the personal allocation
with cash normalization, school share 0.715 at 0.66, general government 0.84 and high uncompensated
care. The own range is the generation's lowest and highest cost over all 64 specifications. CPS
allocations are measured; service responses and the production term are assumed.

| (b) Minors with their parents (NAS 2017) | Members (m) | Adults (m) | Low end | High end | Own range | $ per adult, low / high |
|---|---:|---:|---:|---:|---|---|
| G1, born in Mexico | 16.86 | 11.67 | 110.2 | 134.8 | 110.2–134.8 | 9,441 / 11,543 |
| G2, US-born, a parent born in Mexico | 12.21 | 8.91 | 50.2 | 53.0 | 44.0–59.3 | 5,629 / 5,941 |
| G3+, US-born of US-born parents | 11.83 | 8.18 | 40.5 | 58.6 | 40.5–58.6 | 4,945 / 7,160 |

| (a) Children in their own generation | Members (m) | Adults (m) | Low end | High end | Own range | $ per member, low / high |
|---|---:|---:|---:|---:|---|---|
| G1 | 12.22 | 11.67 | 63.8 | 53.6 | 44.7–74.8 | 5,220 / 4,383 |
| G2 | 14.33 | 8.91 | 81.7 | 95.1 | 81.7–95.1 | 5,703 / 6,636 |
| G3+ | 14.34 | 8.18 | 55.3 | 97.6 | 55.3–97.6 | 3,859 / 6,808 |
| All three | 40.90 | 28.77 | 200.9 | 246.3 | 200.9–246.3 | 4,912 / 6,023 |

Members and adults are the published CPS counts. The account prices 39.71M people: audit row 4 scales
down 1.18M Mexico-born residents outside California and Texas, nearly all of them first generation. On
that count (ladder 274) G1 costs $10,431 / 12,754 per adult under (b) and $5,780 / 4,853 per member under
(a), and all three $5,058 / 6,203 per member; G2 and G3+ do not move. [CALCULATION:
`population_basis_2026_09_29/restate.py` → `derived/restated_pairing.csv`, reader rows for this table]

The generations add to the main case at every specification and under both conventions to within
$1.5e-12bn. Convention (b) follows the brief: minors go to the generation of their co-resident
parents in the group (split 50/50 across two generations), else to the oldest adult relative in the
group. NAS also moves some dependents aged 18–23, so (b) leaves slightly more college cost with the
second generation than NAS would. [SOURCE: NASEM (2017), pp. 377, 387–388, verified in the local
copy; CALCULATION: lane `mixed_units.py` → `derived/minors_convention_b.csv`]

None of these figures is age-standardized: second-generation adults average 34.7 years, the
third-plus 40.8 and the Mexico-born 48.2. Under (a), per adult is not a per-parent figure, because
5.4m of the second generation are minors and 4.3m of them count with a Mexico-born parent under (b).

## 2. What moves it

- **Where children count.** Moving minors to their parents' generation shifts $46–81bn onto the first
  generation. Under (b) a second-generation adult with their minor children costs others 51–60% of
  what a Mexico-born adult does.
- **The household allocation rule.** The shared rule splits every key equally within the SPM unit,
  so parents carry part of their children's costs even under (a), and units that include people
  outside the group pass costs and taxes across its boundary. 36% of third-plus members share a unit
  with someone outside the group (18% of the second generation, 10% of the first). Swapping the rule
  at either end moves $19–32bn between the first and third-plus generations under (a).
  [FRAMING-SENSITIVE]
- **The 270 corrections of September 24.** Under (a) they raise the first generation's cost by $6.0bn
  (low end) and $4.3bn (high end) and lower the second's by $4.2bn and $6.1bn and the third-plus's by
  $4.2bn and $1.6bn. Under (b) the first generation moves only +$0.4bn and −$0.7bn, because its
  children's shares of the premium-credit re-key and pooled medical offset the tax-records stack. The
  corrections are split with each source lane's own functions where possible; the seven alternative
  rules for the rest move no generation by more than $3.7bn and turn none negative.
- **The production term** ($8.8–13.3bn) has no unique split, since the CES block is not linear. Its
  first-order attribution gives the first generation two thirds; splitting by total labor income would
  raise the first generation's cost by $2.7–4.0bn and lower the others' by $1.2–2.2bn each.

[CALCULATION: lane `generation_summary.json` (`allocation_swap`, `lanes`, `sensitivities`),
`production.py` → `derived/production_by_generation.json`]

## 3. Beside the September 19 generation ledger

The ledger in `ledger_absolute_2026_09_17` measures each generation against third-plus non-Hispanic
whites of the same age: −$7,584, −$7,521 and −$6,195 per person. This split measures what each
generation costs everyone else under the adopted account, with no reference group. The two are
different objects, and neither is scaled onto the other. [CALCULATION: lane `compare_ledger.py` →
`derived/ledger_comparison.csv`, the ledger read through its hash-checking loader]

- At the groups' own ages the reference whites are net contributors (+$2.5k to +$3.9k per person
  under the shared allocation), so a gap exceeds the group's own balance.
- The groups' own balances in the ledger (−$5,929, −$5,881, −$4,223) are close to this account's
  (−$5,220, −$5,703, −$3,859) under the same allocation, but they get there through offsetting
  differences: the account charges $1.7–3.0k more per person at average cost, and the adopted
  marginal responses then take off $2.2–2.7k. The closeness validates neither.
- Both objects put the third-plus lowest under the shared allocation and the first generation lowest
  under the personal one.

The FAQ's combining rule still applies: the ledger's generation gaps must not be scaled onto the
$201–246bn. This split is computed directly on the account.

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

**Would change it:** measured benefit receipt and justice use by parents' birthplace (each flagged
rule moves a generation by $2bn or less); a counterfactual production model; a change to the main
case itself, which moves every generation.

## Sources

- Lane: [`generation_account_2026_09_24`](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md)
  (brief, `run_all.sh`, 19 derived files). Inputs: the adopted main case
  (`main_case_2026_09_24`, `package.cjs`, `derived/corrections.json`), the account's CPS ASEC 2025
  frame and keys, the September 19 ledger. [DATA]
- Parent rerun, 2026-09-25: `run_all.sh` passes every gate (masks, keys, models to 5.7e-14bn,
  production, correction splits, engine per generation) and rewrites all 19 derived files
  byte-identical; `main_case.cjs` still passes and its lane is unchanged. [CALCULATION]
- v6 split, 2026-10-07: step 9 of `run_all.sh` (`run_generations_v6.cjs`, with `v6_split.cjs`)
  → `derived/generation_{results,summary,corrections}_oct07{,_cash}.*` (3f583fb4, 8e7b875f); 47 and 41 gates; the
  union reproduces the adopted band, $389.0826–461.4797bn and $307.3994–385.3641bn. [CALCULATION]

## Revisions

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
