---
date: 2026-09-25
concepts: [lineage-legal-status, noncitizen-voting, return-migration-selection, ancestry-instrument, off-books-competition, school-dilution, debt-legacy, winners-and-losers, service-response]
status: adopted
supersedes: []
relations:
  - applies: research/immigration-weekly-conceptual-audit-2026-09-25.md
  - refines: decisions/2026-09-25-school-dilution-priced-beside.md
evidence: research/immigration-weekly-conceptual-audit-2026-09-25.md
---

# 2026-09-25: Qualify the week's claims the conceptual audit caught, with a second review's amendments

## Context

The [weekly conceptual audit](../research/immigration-weekly-conceptual-audit-2026-09-25.md)
(`0ae82d8`) reviewed the September 19–25 findings and named nine problem families, most of them
places where one model's output is carried into another: a budget residual read as lost learning,
an all-household rate read as a native one, all-origin workers read as the group's, Mexico stayers
read as US stayers. The operator asked whether the audit was right, then asked for the fixes. A
second review checked each claim against the code and text it cites. Every confirmed claim holds.
One (the ancestry instrument) was already diagnosed in ladder 199 on September 23, two were
understated (lineage legal status, the voting bound) and two overstated (the winners count's
precision, and the transfer argument against the debt line).

## Alternatives considered

1. **Rewrite the affected memos.** Loses provenance and breaks the append-only rule for
   institutional knowledge.
2. **Leave the memos and let the audit stand alone.** Readers of the original memos, ladder and
   index keep quoting the withdrawn readings.
3. **Dated bracketed qualifications where each claim is stated, Revisions entries, and ladder and
   index notes; a model run where one answers the question instead of a label** (selected).

## Decision

- **Lineage legal status (ladder 159): "nearly irrelevant" withdrawn.** The model gave an
  unauthorized founder the pooled Mexico-born profile from 65, so legalizing could only remove the
  working-age difference. A statutory-eligibility arm now removes, from 65, the programs federal
  law closes to someone never legalized (cash transfers including Social Security, public medical,
  institutional care, noncash aid) and keeps taxes and services. Legalizing at year ten then
  **worsens** the century gap by $417,886 (−$854,686 → −$1,272,572), where the pooled rule showed a
  $24,578 improvement. The arm does not add back emergency Medicaid, state coverage such as
  California's or uncompensated care, so it is the favorable edge for the never-legalized founder.
- **Non-citizen voting note: its ceilings are detection counts, not upper bounds, and "too small
  by orders of magnitude to have decided any federal or California contest" is withdrawn.** It holds
  for statewide and presidential races. The closest House races sit within one order of magnitude
  of the note's own ceiling, some below it; the note's revision lists the certified margins. No
  contest is shown to have been decided by non-citizen ballots.
- **Return selection (ladders 174 and 178): the comparison is with Mexico non-migrants.** Its sign
  against emigrants who stay in the US is not established, so "only its direction" and the
  second-generation memo's mechanism sentence are withdrawn pending an ACS–ENADID comparison.
- **Ancestry instrument (ladders 182 and 183): ladder 199's diagnosis is carried to the lane
  result, the housing entry and the index.** Its pull is each metro's same-decade attraction for
  immigrants, so the SSI and housing coefficients are diagnostics, not causal effects. "No native
  take-up" is withdrawn because the 2000 endpoint has no native split.
- **Off-books competition (ladder 220): the $6.4bn edge and its $4.5bn of payroll tax are
  all-origin.** Mexico-born workers carry about half ($3.2bn, $2.3bn of it payroll tax); "already
  inside the account" holds for that part only.
- **School dilution (ladder 222): the $16.1bn is conditional** on an instructional dollar lost to
  enrollment growth costing as much learning as one removed by a spending cut. "The account cannot
  have both a low response and no dilution" holds for dollars per pupil only.
- **Debt legacy (ladder 207): kept beside the account.** Its proposed route, the interest row's
  response, answers the historical question inside the static comparison, which cannot remove past
  debt. The transfer argument does not shrink the figure: with crowding out the lost return on
  capital is at least the interest, and interest paid abroad leaves the country.
- **Movers (221), vending (223) and the new-immigrant survey (179): narrowed readings.** Reason
  shares among leavers cannot measure leaving rates; the 2019 law changed vending enforcement
  little; 57% of the 2003 cohort had adjusted status and were not at the start of a US career.
- **Winners and losers (226): the substitution elasticity alone spans 18.7–29.2% ahead**, and 6.97m
  other residents live in households with a group member whose resources the pooling leaves out.
  The published 14–30% stacks the dollar extremes; the enumerated maximum is 30.5%.
- **Service response (general government 0.59–0.84):** cross-state elasticities are used as
  finite-removal responses. The correction is sized separately and proposed, not adopted; changes
  to the headline stay with the operator. Sized on 2026-09-26 (ladder 227,
  `finite_response_2026_09_26`): $205.0–249.7bn, +$4.1bn / +$3.4bn, mostly because CBO's school
  coefficients are first-order elasticities too. Composed in one engine run with the consumption-key
  proposal (ladder 225), the two leave the case at $200.9–245.7bn, the published $201–246bn at its
  rounding (run K); adopting either alone moves it by about $4bn.

## Evidence

- Second review, 2026-09-25: each claim traced to code or text (`lineage.py` `founder_profile`,
  `second_instrument.py` `predicted_inflow`, `acs_cells.py`, school RESULT line 116, movers RESULT
  line 159, the voting note's derivation, `scaling_check.py` and `package.cjs`).
- `infra/immigration-fiscal/lineage_cost_2026_09_19/derived/sensitivities.csv`, three appended
  rows; the components reproduce the profile to 1.5e-11 dollars and every earlier output is
  unchanged.
- The audit's probes: `infra/immigration-fiscal/conceptual_audit_2026_09_25/README.md`.

## Revisit if

- Program-level eligibility for unauthorized seniors is priced, including emergency Medicaid,
  state coverage and uncompensated care.
- Returnees are compared with US stayers on harmonized schooling.
- Ladder 199's successor design (a pre-determined ancestry stock times 2000s national flows) or a
  native-specific 2000 outcome is built.
- Detection rates for voter-roll citizenship checks are measured.

## Supersedes

Nothing. Qualifies the entries named above; their original text is kept.
