# The adopted account by generation

**Verdict (2026-09-29, the main case of that date):** On the main case of $371.4–434.8bn a year
([decision](../decisions/2026-09-29-main-case-v4.md), ladder 275), all three Mexican-origin generations remain net
costs to other US residents. That holds at every one of its 64 specifications, under both ways of counting children,
and when benefits are counted as paid.
- **Counted with their parents** (NAS): the Mexico-born cost others $169–197bn a year ($16.0–18.7k per adult of the
  27.7M adults among the 39.7M the account prices), the second generation $111–122bn ($12.4–13.7k per adult) and the
  third-plus $91–116bn ($11.2–14.1k per adult).
- **Counted in their own generation:** $87–97bn, $152–179bn and $123–168bn.
- **Counting benefits when paid** (the cash set, $294.7–361.8bn): with their parents $150–183bn, $78–86bn and
  $67–93bn; in their own generation $73–87bn, $118–143bn and $90–146bn.

v4's changes add $49.6bn (low end) and $47.5bn (high end) to the September 27 case. The pension switch moves most,
and it lands mostly on the US-born: the accrual follows the payroll taxes a generation pays this year, while the
benefits it replaces follow this year's beneficiaries. Counted in their own generation, it adds $33.9 / 36.0bn to the
second generation and $32.8 / 22.6bn to the third-plus, against $10.0 / 14.4bn to the Mexico-born. Long-run property
taxes lower every generation's cost, by $7.7–10.2bn under (a).
[CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md),
`run_generations_v4.cjs --case sept29` and `--case sept29_cash` → `derived/generation_results_sept29.csv`,
`generation_results_sept29_cash.csv`, `generation_summary_sept29.json` `change_from_sept27_by_item`; commit aa1f53b;
the September 27 files rerun byte-identical] [FRAMING-SENSITIVE]

| $bn a year, low / high end | (a) own generation | (b) minors with parents |
|---|---|---|
| G1, born in Mexico | 97.2 / 87.1 | 169.4 / 197.4 |
| G2, US-born, a parent born in Mexico | 151.6 / 179.3 | 110.6 / 121.8 |
| G3+, US-born of US-born parents | 122.6 / 168.4 | 91.4 / 115.6 |
| All three (the main case) | 371.4 / 434.8 | 371.4 / 434.8 |

The ends are specifications 48 (shared allocation, 2%, the low long-run readings) and 11 (personal, 3%, the high
readings). Per-person figures divide by the account's row-4 counts (ladder 274); only the Mexico-born's count differs
from the CPS's. Beside the account, never in the range, without the capital return (a) is $88.1 / 74.9bn,
$138.8 / 156.7bn and $110.1 / 146.1bn. The lane did not split the 7% arm on this case (the whole case at 7%:
$457.5–511.1bn). State pricing applies the union's price indexes to each generation's keys; indexes from each
generation's own state mix are not computed.

**The September 27 case** ($321.8–387.4bn a year;
[decision](../decisions/2026-09-27-main-case-capital-return-and-long-run-responses.md), ladder 239) left all
three Mexican-origin generations net costs to other US residents, at every one of its 64 specifications and
under both ways of counting children.
- **Counted with their parents** (NAS): the Mexico-born cost others $159–191bn a year ($15.0–18.1k per
  adult of the 39.7M the account prices, ladder 274), the second generation $87–95bn ($9.8–10.7k per adult)
  and the third-plus $75–102bn ($9.2–12.4k per adult).
- **Counted in their own generation:** $78–94bn, $128–153bn and $100–156bn.

The case's four additions are long-run road and park responses, rental assistance, the return on public
capital and the government enterprises. They add $63.3bn (low end) and $95.4bn (high end) over the schools
case. They follow residents and pupils, so under the own-generation count the second and third-plus
generations carry 75–78% of the move, and under the NAS count the Mexico-born carry 37%.
- **The capital return** is $33.8 / 55.7bn of the case. It is an imputed resource cost at 2% / 3%, never a
  debt flow. Under (a): G1 $8.7 / 11.5bn, G2 $12.5 / 22.0bn, G3+ $12.5 / 22.2bn.
- **The enterprise receipt's re-key** to the corrected population share lowers G1's cost by $0.5 / 0.7bn
  and moves the others by under $0.1bn.

[CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md),
`run_generations.cjs` → `derived/generation_results.csv`, `generation_summary.json`
`change_from_sept26_schools`; commit 8654a0c; parent rerun byte-identical] [FRAMING-SENSITIVE]

| $bn a year, low / high end | (a) own generation | (b) minors with parents |
|---|---|---|
| G1, born in Mexico | 93.8 / 78.3 | 159.0 / 190.8 |
| G2, US-born, a parent born in Mexico | 127.6 / 153.0 | 87.3 / 95.0 |
| G3+, US-born of US-born parents | 100.5 / 156.1 | 75.5 / 101.6 |
| All three (the September 27 case) | 321.8 / 387.4 | 321.8 / 387.4 |

The ends are specifications 48 (shared allocation, 2%, the low long-run readings) and 11 (personal, 3%, the
high readings), as in the schools case. Beside the account, never in the range:
- without the capital return, (a) is $85.0 / 66.8bn, $115.1 / 131.0bn and $87.9 / 133.9bn;
- at 7% on every component, $115.6 / 93.6bn, $158.9 / 182.3bn and $131.8 / 185.8bn.

The first-year budget response is unchanged: it is still the schools case's, below.

**Earlier cases.** All three generations are net costs to other residents in every case, at every one of
its 64 specifications and under both ways of counting children. $bn a year, low / high end:

| | September 24, $200.9–246.3bn (sections 1–4) | Schools at full cost, September 26, $258.5–292.0bn | September 27, $321.8–387.4bn |
|---|---|---|---|
| (b) G1, born in Mexico | 110.2 / 134.8 | 135.6 / 155.4 | 159.0 / 190.8 |
| (b) G2 | 50.2 / 53.0 | 67.9 / 66.1 | 87.3 / 95.0 |
| (b) G3+ | 40.5 / 58.6 | 55.0 / 70.5 | 75.5 / 101.6 |
| (a) G1 | 63.8 / 53.6 | 77.6 / 56.9 | 93.8 / 78.3 |
| (a) G2 | 81.7 / 95.1 | 105.0 / 117.5 | 127.6 / 153.0 |
| (a) G3+ | 55.3 / 97.6 | 75.8 / 117.6 | 100.5 / 156.1 |
| Ends (specifications) | 56 and 7 | 48 and 11 | 48 and 11 |

Where the children are counted decides who carries each addition. Schools at full cost added $62.1bn (low
end) and $48.5bn (high end) over September 24: under the own-generation count the second and third-plus
generations carry 76–91% of it, and under the NAS count the Mexico-born carry 43–44%. At a school response
of 1 the school-share bound flips, so the ends moved from specifications 56 and 7 to 48 and 11. Priced at
September 24's specifications first, the move from September 24 splits into:
- schools at 1: +$62.1bn / +$48.5bn;
- general government: +$0.5bn;
- row 8: −$0.1bn;
- the consumption key: −$4.1bn;
- the ends moving to 48 and 11: −$0.8bn / +$0.8bn.

The first-year budget response charges CBO's year-to-year school response ($200.9–245.7bn). It stays within
$1bn of the September 24 split for every generation: (a) $63.9/53.0bn, $82.1/95.5bn and $55.0/97.2bn;
(b) $110.6/134.9bn, $50.6/53.2bn and $39.7/57.6bn. [CALCULATION: [generation
lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md), `run_generations.cjs` →
`derived/generation_results.csv`, `generation_summary.json` `change_from_sept24` (2441ac8); [propagation
report](../infra/immigration-fiscal/sept26_propagation_2026_09_26/RESULT_generation.md), `run_generations.cjs
--case sept26`; ladder 224] [FRAMING-SENSITIVE]

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
- v4 split, 2026-09-29: step 7 of `run_all.sh` (`v4_inputs.py`, `tax_key_split.py`, `run_generations_v4.cjs`)
  → `derived/generation_{results,summary,corrections}_sept29{,_cash}.*` (aa1f53b); 27 and 26 gates; the union
  reproduces the adopted band, $371.4146–434.8410bn and $294.7011–361.8175bn. [CALCULATION]

## Revisions

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
