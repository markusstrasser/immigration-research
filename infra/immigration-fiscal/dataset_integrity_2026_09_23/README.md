**Verdict:** Combined on one frame, the audit's corrections leave the main case essentially where it
was: **$202.9–251.1bn at central values**, against the published $203.2–249.6bn. They widen its
range to **$192–262bn**. The defects are real and run in both directions, and they nearly cancel:
- **Spending keys, net −$28.1bn** (−32.5 to −22.0), mostly overcharges. Premium tax credits are keyed as
  if they were EITC (−14.2), Medicaid long-term care is keyed by a community-only survey (−11.1), the
  education key over-weights K–12 (−3.5), and smaller items.
- **Tax records that overstate the group's taxes: +$27.9bn at the band's low end and +$29.6bn at its
  high end** ($21.5–34.6bn across on-books shares and fill-in methods). The Census tax model assumes
  every unauthorized worker files and complies. The CPS fills in missing income too high for the
  group. The $385bn federal gap is keyed by CPS liability rather than high incomes. These are stacked
  with the Mexico-born recount and a state-aware status flag, never added separately.

No combination changes the sign. Two alternatives move the central case down:
- if the CPS fill-ins carry no group bias (row 13 at zero), $195.3–242.0bn;
- with operator decision 2 (the pooled-MEPS medical figure replacing row 5), $196.3–244.5bn.

[CALCULATION: `synthesis.py` → `derived/synthesis_net.csv`, reading the CPS imputation lane's stacks]

**Adopted 2026-09-24 (operator decision 1).** The package went into the engine with the outside checks.
Row 6 runs through the engine, CBO's income-tax gradient replaces row 3, and the pooled-MEPS figure
replaces row 5. The adopted main case is $200.9–246.3bn
([`main_case_2026_09_24`](../main_case_2026_09_24/RESULT.md), [decision](../../../decisions/2026-09-24-main-case-audit-and-outside-checks.md)). The figures below are the audit's own.

Date: 2026-09-23, band lanes folded in 2026-09-24. Operator: "Did we ever look at issues with the
datasets itself? Just formatting errors, bad columns, weird statistics that can't be real given real
world knowledge and taste? Bad political ways to categorize etc?" and "/analyze". Brief:
[BRIEF.md](BRIEF.md). Family reports, which carry the evidence and run commands: [cps.md](cps.md),
[acs.md](acs.md), [spending.md](spending.md), [crime.md](crime.md). Band lanes:
- [on-books share](../onbooks_share_2026_09_23/RESULT.md);
- [CPS imputation keys](../cps_imputation_keys_2026_09_23/RESULT.md);
- [Mexico-born count](../mexborn_count_2026_09_23/RESULT.md);
- [long-term care share](../ltss_share_2026_09_23/RESULT.md);
- [California status check](../california_medical_status_2026_09_23/RESULT.md).

## Effects on the main case

Effects are in $bn a year of cost to other residents. A negative effect means the published main
case is too high. Where two figures appear, they are the band's low end (shared allocation) and high
end (personal allocation).

| # | Defect | Grade | Effect | Status |
|---|---|---|---:|---|
| 1 | BEA refundable credits ($228.8bn, Table 3.12 line 25) are keyed by CPS EITC+ACTC, where the group holds 23.0%. Treasury paid $118.4bn of premium tax credits in 2024, and the group holds 10.9% of subsidized marketplace persons | A | **−14.2** | measured (`spending_mts_credits.py`) |
| 2 | The tax model treats every respondent as a resident, fully compliant filer. Re-keyed to the on-books lane's dollar share 0.52 (0.42–0.63) | B | +11.8 / +12.1 over row 3; alone +9.2 to +16.8 | measured share; tax block |
| 3 | The $385bn BEA–CPS federal income tax gap is keyed by CPS liability (group 5.7%), not high AGI (3.3%) | B | +9.5 / +9.6 | measured; the high-AGI share rests on 34 union records; tax block |
| 13 | CPS income fill-ins drift up for the group: its filled-in wages keep 9% of its own wage gap; re-imputed from group donors | B | +8.6 / +10.2 over rows 2 and 3; over row 2, +6.8 / +9.8 / +12.0 | measured drift, modelled correction; tax block |
| 4 | ASEC 2025 counts 1.185M too many Mexico-born outside CA+TX; ACS 2024's 11.07M is right | B | −2.2 / −2.5 stacked; alone +0.2 / +0.5 | measured count, account keys; tax block |
| — | Status imputation's Medicaid clause breaks in status-blind states (0.66M more union unauthorized) | B | +0.2 / +0.3 | measured; tax block |
| 5 | BEA Medicaid ($954bn) is keyed by a MEPS community-only key; the group draws 7.4% of long-term care dollars, not 12.25% | B | **−11.1** (−12.5 to −8.1) | measured from CMS T-MSIS/TAF |
| 6 | The education key puts 93% on K–12; BEA's split is 77–82% | B | **−3.5** (−4.8 to −2.2) | measured |
| 7 | The justice key uses FBI 2019 arrests (Hispanic RR 1.145); the repo holds 2023 and 2024 Table 43C (1.216, 1.205) | B | **+1.1** | measured |
| 8 | Unallocable state and local spending ($168.7bn) gets the administration elasticity 0.84 instead of the all-spending 0.96 | C | **+2.0** | measured |
| 9 | The MEPS donor filter drops 207 records carrying 3–4% of Medicare and Medicaid dollars; scaled to the non-LTSS remainder | C | −0.8 (−1.6 to 0) | bounded |
| 10 | Foster care and adoption spending is keyed by WIC | C | −1.5 (−2 to −1) | bounded |
| — | Hispanic-origin allocation, grants at the low end, top-code swaps, sentinels, weights, birthplace flags | D | each under ±1 | measured |
| 11 | Household rental assistance ($60bn) is held fixed as a business subsidy | choice | 0 now; +7.5 if it responded | classification, not in the net |
| 12 | Income-security consumption ($168bn, mostly social services and administration) is keyed by CPS public assistance (group 16.7%) | choice | 0 now; −7.5 with a population key, −20 with an all-cash key | key choice, not in the net |

**Net.**

| Band end | Tax block | Other rows | Net | Main case |
|---|---:|---:|---:|---:|
| Low (shared) | +27.9 (21.5 to 34.3) | −28.1 (−32.5 to −22.0) | **−0.3** (−11.0 to +12.3) | 202.9 (192.2 to 215.5) |
| High (personal) | +29.6 (24.8 to 34.6) | −28.1 (−32.5 to −22.0) | **+1.5** (−7.7 to +12.5) | 251.1 (241.9 to 262.1) |

The tax block's central is the mean of the two fill-in methods at the on-books lane's central share.
Its range runs from the high share with the plain hot deck to the low share with the hot deck net of
its control. The other rows' low and high are summed as independent bounds. Rows 11 and 12 are
classification choices, not data errors; with them the range is $172–270bn.

**The tax block at the central case**, stacked increments with the two fill-in methods averaged:

| Step | Low end | High end |
|---|---:|---:|
| Row 3 alone | +9.48 | +9.59 |
| Row 2 over row 3 (alone +12.71 / +13.13) | +11.81 | +12.08 |
| Row 13 over rows 2 and 3 | +8.60 | +10.21 |
| Row 4 over rows 2 and 13 | −2.24 | −2.51 |
| State-aware status flag | +0.20 | +0.26 |
| **Block** | **+27.86** | **+29.63** |

**Row 4 shrank from −7.1 to about −2.4.** The Mexico-born lane priced it by charging each removed
person the first generation's average net cost. That is the ledger's generation split scaled flat
onto the complete account, which this repo's routing rules forbid. On the account's own keys the
1.185M removed people are mostly working-age noncitizens, who pay about what they are charged:
$10.8–12.7bn of taxes against $10.5–12.2bn of spending. Only once row 2 has cut their on-books taxes
does removing them save money. [CALCULATION: `cps_imputation_keys_2026_09_23` step 5e,
`derived/status_combination_onbooks_lane_row4_lines.csv`]

**Combining.**
- Row 1 and the tax block share no dollars: the block's status and fill-in corrections use only the
  $110.46bn of the refundable line that is not premium credits.
- Rows 2, 3, 13 and 4 and the status flag are one stack. The CPS lane measured each on top of the
  others, with overlaps of about $1bn between rows 2 and 3 and $0.1–1.2bn between the fill-ins and
  rows 3 and 4.
- Row 5 and the pooled-MEPS medical lane re-key the same Medicaid dollars. Adopted together
  (decision 2) they give −17.7 (−21.1 to −8.7) in place of row 5, not in addition to it.
- Not computed, each well under $1bn:
  - row 4's effect on rows 1, 5 and 6;
  - row 3 under row 4's weights;
  - the production and fixed terms moving with row 4's wages (+0.2 to +0.4).

**Row 1 in detail.** BEA footnote 6: line 25 "includes the amounts by which federal refundable tax
credits reduce personal current tax liabilities … as well as the outlays". Calendar-2024 Treasury
outlays were:
- premium credits $118.35bn;
- EITC above liability $60.13bn (October is blank in the statement);
- child credit above liability $26.29bn.

[SOURCE: Monthly Treasury Statement Table 5, api.fiscaldata.treasury.gov; `derived/spending_mts_credits.json`]
That leaves $110.5bn of the line for EITC, the child credit and their liability offsets. Two things
push the group's true premium-credit share below the 10.9% person share: credit per enrollee rises
with age, and imputed unauthorized residents cannot receive the credit. So −$14.2bn is more likely
too small than too large [INFERENCE]. The spending audit's range was −$12.0bn to −$14.4bn for
$100–120bn of premium credits. The probe reproduces −12.02 / −13.22 / −14.43.

**Checks by the parent.**
- Every CPS, crime and spending script reran byte-identical (39 derived files).
- Band lanes were rerun by the parent before commit: CPS imputation 24/24, Mexico-born count
  13/13, long-term care 18/18, California status 22/22.
- The builders confirm the keying of line 25 and that receipts carry no status adjustment.
- The synthesis reads the CPS lane's stacks and stops with `[BLOCKED]` if any stack is missing.

## What would settle it

The analysis contract for this audit:
- **Leading explanation:** two-sided key mapping that nets to about zero. The main case stands, with
  an audit range of $192–262bn.
- **Top alternative:** the CPS fill-ins are unbiased for the group, and the net is about −$8bn
  ($195–242bn).

Three measurements would narrow it:
1. **Row 13.** Do the group's nonrespondents resemble its respondents in the same cell? Only linked
   administrative earnings can say. The public March weekly-earnings check (98 union records) cannot
   separate zero from the drift.
2. **Row 2: the on-books share of unauthorized earnings in 2024.** The on-books lane's 0.42–0.63
   moves the block by about ±$3bn.
3. **Row 3: the group's share of high-AGI liability.** It rests on 34 union records. IRS SOI tables
   by state and AGI, crossed with ACS composition, would test it.

**Decision impact.** The audit does not move the headline, its sign or the ranking of results. It
changes what the headline is made of: the group's taxes are lower than the account assumed, and its
keyed spending is lower too, by about the same amount.

## Categories and coding (the "political categories" question)

| Where | What | Effect | Status |
|---|---|---|---|
| NIBRS TX/AZ/CA arrestees | 95.5–98.6% of Hispanic arrestees are coded White by race. Constructions that subtract all Hispanics from White overstate Hispanic/NH-white arrest ratios by 1–5% | memos only; makes the group look worse | noted |
| BJS *Jail Inmates 2023* | Hispanic 14.4% of inmates against 18.4% of adults and 22.1% of adult arrests, flat 2013–23. BJS adjusts prisoners, not jails | weakens the justice lane's "three estimates agree"; the BJS arm would be +$2.45bn | note added to the justice lane |
| ACS 2021–2023 group quarters | 25–30% of Mexico-born inmates (by birthplace) coded generic "Other Hispanic" (2.5% in 2019, 5.4% in 2024): a processing regime, not self-identification | raw arm −$1.9bn; the central already reallocates | corrected in the central |
| Generation split, item N | institutional care counts raw HISP=02, without that reallocation | ledger −$21 to −$57 per person (~1%), $1.8bn | deferred to the next ledger rebuild |
| ACS 2020+ schooling | "no schooling completed" jumps 4.4 points for Latin American-born adults (−0.25 years); below-high-school share unchanged; natives unaffected | years-of-schooling comparisons across 2019/2020 | priced in ladder 197 |
| Census 1980 institutions | 26–29% of inmates' education allocated from household-like donors | crime-selection lane's 1980 education-held rows; direction unmeasured | noted |
| SHR | offender ethnicity missing for whole states (KY, OK 99%, MI 90%, LA 80%, CA 43%) | none after reweighting (0.1033 → 0.1024) | checked |
| CPS race | edited or allocated for 36% of G1 and 32% of G2 (the CPS has no "some other race" answer) | none on the account; anything on `PRDTRACE` for Hispanics is contaminated | noted |
| ACS 2020 race question | 5M native non-Hispanic whites moved from "white alone" to multiracial | <0.5% of per-person gaps | checked |
| CPS parents' birthplace | no "unknown" code, so every blank is hot-decked: 5.4% of G2/G3+ adults vs 2.55% of the white reference | union ≈ 0 | checked |
| 1990/2000 censuses | institution type not recorded; Rumbaut's "correctional" 2000 figures cover all institutions | FAQ 12, generation memo | corrected (7a44b69) |
| 2000 census birthplace | US birthplace allocated to 98% of allocated inmates | 3.45× → 2.7–3.0× | corrected (f88a52b, e6bcf01) |

## Memo claims corrected in this pass

- **Incarceration memo, 5-year origin table.** Central American and Dominican cells were read raw
  against whites while the Mexican cell was quoted coding-adjusted. With the same correction,
  Guatemalans read 0.99–1.26× whites, Dominicans 1.02–1.30× and Salvadorans 0.69–0.88×. So "at or
  below native whites" fails for the first two; the ordering below Mexicans holds (acs.md F5).
- **Generation memo §3.** The 18.8% "EITC use" for Mexico-born adults 25–64 is tax-model output.
  With the SSN rule applied to the imputed unauthorized it is 10.0% (cps.md 1b).
- **Justice lane RESULT.** "The Crime Data Explorer totals carry race only" missed the held 2023 and
  2024 Table 43C files (row 7), and "three estimates agree" leans on the under-recorded BJS jail
  count.
- **Bias-mechanisms memo line 25.** "4.55% incarcerated" is Rumbaut's label for institutional
  residence.

## Deferred, with reasons

- Ledger item N (+$1.8bn on the generation split): the ledger is fingerprinted, so the one-step
  reallocation waits for its next rebuild.
- ADJINC is omitted in four ACS scripts: 1.5–2% on dollar levels only; group ratios are unaffected.
- ACS earnings allocation (Mexico-born/white ratio 0.572 → 0.589): affects ACS cross-checks only.
- School allocation in the ACS: the generation split's K–12 charge is about $0.5bn low.
- Row 4's second-order effects on rows 1, 5 and 6, and the production and fixed terms under its
  weights: each well under $1bn, not computed.
- Not checked: census QHISPAN (no held extract carries it), ACS housing and commute item flags, the
  cause of the 2020 schooling break, whole-person imputation rates for correctional GQ.

## Proposal (the operator adopts)

1. **Adopt the audit as one package.** The main case becomes $202.9–251.1bn with an audit range of
   $192–262bn. The package corrects the account line by line: taxes and keyed spending both fall by
   about $28bn. The headline barely moves.
2. **Decision 2 separately.** The pooled-MEPS medical figure replaces row 5 and gives
   $196.3–244.5bn.
3. **Rows 11 and 12 stay classification choices,** reported beside the net.

The earlier proposal, to adopt the five measured rows now (about −$5bn) and hold rows 2, 4 and 5 as
a band, is superseded: the band lanes have measured rows 2, 4 and 5, and row 3 now sits inside the
tax block.

## Files

- Scripts: `cps_*.py`, `acs_*.py`, `spending_*.py`, `crime_*.py`, `synthesis.py`.
- Outputs: `derived/*.csv|json`.
- Ignored `_cache/`: slim ACS parquet extracts and the Treasury statement pages.

## Revisions

**2026-09-24 — band lanes folded in; the net moved from −$13.5bn to about zero.** The first synthesis
(2026-09-23) read −$29.2bn, −$13.5bn and +$3.0bn at low, central and high, a main case of about
$190–236bn. It summed each row separately and had three rows as bounds. Five band lanes then
measured or re-keyed them:
- Row 2 on the account's own keys: +9.2 / +12.9 / +16.8, in place of +5.0 / +10.6 / +17.0.
- Row 13 is new: CPS fill-in drift, +6.8 / +9.8 / +12.0 over row 2. These figures include the CPS
  lane's Medicare key fix: its translation had keyed Medicare spending by coverage.
- Row 4 moved from −7.1 to about −2.4. The old formula scaled the ledger's generation split flat
  onto the account.
- Row 5 moved from a −3.6 to −15 bound to −11.1 measured.
- A state-aware status flag was added.

Rows 2, 3, 13 and 4 are now read as one stack. The earlier text of this README is in git history
(commit 0021ad4 and before).

