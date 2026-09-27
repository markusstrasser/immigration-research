# The adopted account by generation

**Verdict (2026-09-26, schools at full average cost):** Since the main case charges the group's
pupils at their full average cost ($258.5–292.0bn a year; [decision](../decisions/2026-09-26-main-case-schools-full-cost.md),
ladder 230), all three Mexican-origin generations remain net costs to other US residents. That holds
at every one of its 64 specifications and under both ways of counting children.
- **Counted with their parents** (NAS): the Mexico-born cost others $136–155bn a year ($11.6–13.3k per
  adult), the second generation $66–68bn ($7.4–7.6k per adult) and the third-plus $55–71bn ($6.7–8.6k
  per adult).
- **Counted in their own generation:** $57–78bn, $105–117bn and $76–118bn.

Schools at full cost add $62.1bn (low end) and $48.5bn (high end) over September 24. Where the
children are counted decides who carries that cost: under the own-generation count the second and
third-plus generations carry 76–91% of it, and under the NAS count the Mexico-born carry 43–44%.
[CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md),
`run_generations.cjs` → `derived/generation_results.csv`, `generation_summary.json`
`change_from_sept24`; commit 2441ac8] [FRAMING-SENSITIVE]

| $bn a year, low / high end | (a) own generation | (b) minors with parents |
|---|---|---|
| G1, born in Mexico | 77.6 / 56.9 | 135.6 / 155.4 |
| G2, US-born, a parent born in Mexico | 105.0 / 117.5 | 67.9 / 66.1 |
| G3+, US-born of US-born parents | 75.8 / 117.6 | 55.0 / 70.5 |
| All three (the main case) | 258.5 / 292.0 | 258.5 / 292.0 |

The two columns are the main case's two ends.
- The low end is the shared allocation with school share 0.715 (specification 48).
- The high end is the personal allocation with share 0.865 (specification 11).

At a school response of 1 the school-share bound flips, so these are not September 24's
specifications 56 and 7. Priced at September 24's specifications first, the move from September 24
splits into:
- schools at 1: +$62.1bn / +$48.5bn;
- general government: +$0.5bn;
- row 8: −$0.1bn;
- the consumption key: −$4.1bn;
- the ends moving to 48 and 11: −$0.8bn / +$0.8bn.

The first-year budget response charges CBO's year-to-year school response ($200.9–245.7bn). It stays within
$1bn of the September 24 split for every generation:
- (a): $63.9/53.0bn, $82.1/95.5bn and $55.0/97.2bn;
- (b): $110.6/134.9bn, $50.6/53.2bn and $39.7/57.6bn.

[CALCULATION: [propagation report](../infra/immigration-fiscal/sept26_propagation_2026_09_26/RESULT_generation.md);
`run_generations.cjs --case sept26`] Sections 1–4 below are the September 24 record.

**September 24 verdict (record; superseded 2026-09-26):** Split by generation, the adopted main case ($200.9–246.3bn a year) leaves all three
Mexican-origin generations as net costs to other US residents. That holds at every one of the main
case's 64 specifications and under both ways of counting children. Counted with their parents, as
the National Academies count them, the Mexico-born cost others $110–135bn a year ($9.4–11.5k per
adult), the US-born second generation $50–53bn ($5.6–5.9k per adult) and the third-plus $40–59bn
($4.9–7.2k per adult). Counted in their own generation, the order changes: $54–64bn, $82–95bn and
$55–98bn. This is one year of the people alive in 2024. It cannot say what today's children will pay
as adults. [CALCULATION: [generation lane](../infra/immigration-fiscal/generation_account_2026_09_24/RESULT.md),
`run_generations.cjs` → `derived/generation_results.csv`; ladder 224] [FRAMING-SENSITIVE]

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

## Revisions

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
