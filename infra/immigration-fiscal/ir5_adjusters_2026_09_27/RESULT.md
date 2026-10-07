claude-opus-5-5

**2026-10-07:** the ledger's item T moved these figures by $0–3k per admission; the current values are under
[Revisions](#revisions). The premise still holds.

**Verdict:** Under the central assumptions the operator's premise holds: a Mexican parent of a US citizen who
adjusts inside the US costs less per admission than one who arrives new. The margin comes entirely from adjusters
who would have stayed without the green card, and it vanishes where an unauthorized senior would draw little public
care. All figures are central-case remaining-lifetime net costs in 2024 dollars.

- **Per admission.** At the evidence-based mix of adjusters (arm C), an adjuster costs $237k / $235k / $240k at
  ages 55 / 60 / 65 at 3%. A new arrival on the same basis costs $274k / $275k / $288k. With the tail lane's
  treatment of the premium tax credit the adjuster costs $230k / $231k / $241k, against the tail lane's
  $270k / $275k / $286k. Undiscounted, $463k / $412k / $370k against $527k / $476k / $437k
  [DATA: `derived/arms_by_age.csv`].
- **FY2024 flow.** The Mexican IR-5 flow at its observed split (19% issued abroad, 81% adjusting) is −$14.3bn at
  3%, against −$16.1bn if every parent were a new arrival. With the tail lane's credit treatment, −$13.9bn against
  its −$15.9bn [DATA: `derived/flow_fy2024.csv`].
- **Adjusters who would otherwise have left** cost more than a new arrival: $290k / $296k / $318k at 3% (arm B).
  Years already lived here bring Medicare, Social Security on earlier covered work and, for residents since before
  1996, Medicaid and SSI sooner [DATA: `derived/arms_by_age.csv`, `derived/adjuster_items.csv`].
- **Where the premise fails.**
  - Too few would have stayed: fewer than 15–23% of adjusters (value-weighted) staying without the green card
    reverses it. Published emigration rates imply 50–59% [DATA: `derived/breakeven.csv`].
  - Too little public care for an unauthorized senior: below about $2.0k / $2.1k / $3.0k a year at 55 / 60 / 65.
    With the federal floor alone ($1.9k a year at central prices) the adjuster is $1k / $2k / $13k dearer and the
    FY2024 flow $0.2bn dearer. Under the 2026 state rules for new enrollees ($2.7k) the adjuster is $5k / $4k
    cheaper at 55 / 60 and $4k dearer at 65. In the tail lane's low case it is $7k / $9k / $25k dearer [DATA:
    `derived/breakeven_floor.csv`, `derived/arms_by_age.csv`, `derived/flow_fy2024.csv`].
- **The premium tax credit.** The ledger, and so the tail lane, charges the credit per capita at every age, $324 a
  person-year. Keyed instead to Marketplace coverage and age, it moves a new arrival's value by −$2k to +$4k, so
  the tail lane's figures stand [DATA: `derived/ptc_inputs.csv`, `derived/arms_by_age.csv`].

# IR-5 parents who adjust inside the US: cost per admission

Lane opened 2026-09-27 from `BRIEF.md` (commit cf4bc30). Sections 1–5 answer the brief's questions 1–5, in order.

## 1. Who adjusts: Mexican IR-5 parents in the New Immigrant Survey 2003

Script `nis_adjusters.py` → `derived/nis_ir5_channels.csv`, `derived/nis_ir5_spells.csv`,
`derived/nis_ir5_adjuster_types.csv`, `derived/nis_provenance.json`. Source: NIS-2003 Round 1 (ICPSR
38031 v3), the probability sample of adults admitted as LPRs May–November 2003, read from the zip already
in `sources/`. Parents of US citizens are `VISACATMO = 3` (995 adults; 270 born in Mexico, 93 of them
adjusters). The administrative preload flags adjusters (`CISADJUST`) and their status at adjustment
(`NISTEMPVISA`). Section K records every move of 60 days or more, with the country and whether the
respondent had a visa. Section B records US work before the green card. All shares are weighted with
`NISWGTSAMP1`. Standard errors use the Kish effective n and ignore clustering.

| Mexican IR-5 parents, NIS-2003 | New arrivals | Adjusters |
|---|---:|---:|
| Share of the Mexican IR-5 flow | 67.0% | 33.0% ±2.9 |
| n (unweighted) | 177 | 93 |
| Mean age at the green card | 63.1 | 60.0 |
| Aged 55+ / 65+ | 81% / 47% | 63% / 36% |
| Years in the current US residence before the green card, median | 0 | 6.3 |
| Resident 5+ years before the green card | 14% | 53% ±6 |
| Resident under 2 years | 84% | 28% ±5 |
| Resident since before 22 Aug 1996 (continuous) | 13% | 47% |
| Ever entered without a visa or document | 25% | 35% |
| Worked in the US before the green card | 10% | 41% |
| Status at adjustment (admin): visitor for pleasure / entered without inspection / unknown or missing | — | 21% / 9% / 70% |

[DATA: derived/nis_ir5_channels.csv; spell = LPR date minus the start of the current US residence from
Section K]

Non-Mexican IR-5 adjusters are a different population: 67% were visitors for pleasure at adjustment, their
median residence before the green card is 2.8 years and 31% had lived here 5+ years [DATA: same file,
group "other"]. The Mexican adjusters of 2003 were mostly settled residents: a median of 6.3 years in the
country, 41% had worked here, a third had crossed without documents at some point (then eligible to adjust
under 245(i)).

Adjuster types, cut where eligibility changes (Mexican IR-5 adjusters with a measured spell, n = 81):

| Type | Residence before the green card | Share, all | Share, never EWI | Mean age | Worked in the US before |
|---|---|---:|---:|---:|---:|
| T0 recent entrant | under 2 years | 27.8% | 37.8% | 60.8 | 15% |
| T1 settling | 2–5 years | 19.2% | 23.9% | 56.6 | 41% |
| T2 long resident | 5–28 years | 39.8% | 31.9% | 61.9 | 43% (mean 9.7 years) |
| T3 since before Aug 1996 (for an FY2024 adjustment) | 28+ years | 13.3% | 6.4% | 60.9 | 100% (mean 25 years) |

[DATA: derived/nis_ir5_adjuster_types.csv. The "never EWI" column drops adjusters who ever crossed without
documents, because since April 2001 such a parent can adjust only under grandfathered 245(i) or parole
(`../ir5_fraud_and_cohorts_2026_09_27/RESULT.md` §2).]

**What carries to FY2019–FY2024 and what does not.** In 2003 a third of Mexican IR-5 parents adjusted; in
FY2019–FY2024 about 80% did (visas issued abroad 6.9k–11.8k a year against 34k–63k green cards;
`../ir5_fraud_and_cohorts_2026_09_27/RESULT.md` §2). No published table after FY2002 gives prior status or
time in the US for adjusters by class, for Mexico or for all countries (`reads/who_adjusts.md` Q1; the
INS Yearbook's Table 10 was last usable in FY1997). The evidence on the recent mix is indirect:

- *Age.* Adjusters are younger. In NIS-2003 Mexican adjusters were 60.0 against 63.1 for new arrivals.
  DHS's FY2024 expanded Table 9 (all immediate relatives, all countries) shows the same within 55+:
  30.5% of adjusters are 55–59 against 23.5% of new arrivals, and 31.6% are 65–74 against 37.3%
  [SOURCE: `reads/who_adjusts.md` Q5, DHS OHSS expanded Tables 8–11 FY2024, sheets "Table 9 New Arrivals"
  and "Table 9 Adjust"].
- *Undocumented adjusters.* Warren (2020) puts undocumented Mexicans who adjusted at 45,000 a year in
  2010–2018, all classes [SOURCE: `reads/who_adjusts.md` Q4, Exa extract of Warren 2020, JMHS]. Mexico's
  adjustments of all classes ran 70k–100k a year in FY2010–FY2019 [DATA:
  `../late_arrival_tail_2026_09_27/derived/ir5_flow.csv`], so over half of Mexican adjusters had been
  undocumented. A parent who overstayed a visa and adjusts is a settled resident (T1–T3).
- *Recent entrants.* Nothing in law stops a parent living in Mexico from entering on a tourist visa or
  border crossing card and adjusting (*Matter of Cavazos*; USCIS dropped the 90-day rule in 2021)
  [SOURCE: `reads/who_adjusts.md` Q3]. Port-of-entry parole of 513,763 Mexicans (October 2018–May 2025)
  opened a third route: a parole satisfies INA 245(a) [SOURCE: same, GAO-26-107765 extract and USCIS
  Policy Manual vol. 7 part B ch. 2]. No count of IR-5 adjusters by prior parole exists.
- *DHS's quarterly adjustment report.* The OHSS Legal Immigration and Adjustment of Status Report (fourth-quarter
  workbooks for FY2019 and FY2022–FY2025) splits adjustments from new arrivals by nationality (Table 1A) and by
  class (Table 1B), never both at once. None of its six tables records an adjuster's prior status or last
  nonimmigrant class [DATA: `ohss_lias.py` checks the six table titles; `derived/ohss_lias_provenance.json`].
  The two margins barely moved in FY2025 [INFERENCE: so nothing points to a change in the Mexican IR-5 split,
  which itself stops at FY2024].

  | Adjustment share | FY2019 | FY2022 | FY2023 | FY2024 | FY2025 |
  |---|---:|---:|---:|---:|---:|
  | Parents of US citizens, all nationalities | 52% | 40% | 52% | 53% | 52% |
  | Mexican nationals, all classes | 64% | 51% | 63% | 65% | 65% |

  [DATA: `derived/ohss_lias_adjust_shares.csv`]

The lane therefore takes the NIS-2003 type shares as the central mix for Mexican IR-5 adjusters, with the
never-EWI shares (more recent entrants, fewer long residents) as the alternative. Section 5 reports the stay
probability and the public-care floor at which the conclusion flips. [INFERENCE: the 2003 mix is the only measured
one; the direction of drift since 2003 is not identified. The never-EWI T3 cell has 3 respondents.]

## 2. Eligibility at and after adjustment

`reads/eligibility_rules.md` quotes the primary text for each rule. Its 180 quotes are in
`reads/eligibility_quotes.json`, and `verify.py` finds every one verbatim in the files cached in `_cache/law/`.
The rules that move the valuation:

| Rule | New arrival | Adjuster | In the model |
|---|---|---|---|
| Medicare Part B and premium Part A at 65+ (42 U.S.C. 1395o(a)(2), 1395i-2(a)(3)) | after 5 years' continuous residence | residence "need not" be as an LPR (POMS GN 00303.800 A.4) and may begin with an illegal entry (HI 00805.005); "arrival as a visitor or tourist does not begin a period of residence" | wait max(0, 5 − r) years after the green card, r = 1 / 3 / 14 / 30 by type |
| Medicaid (state plan), SSI (8 U.S.C. 1613) | 5-year bar from admission | bar runs from adjustment; none for continuous residence since before 22 Aug 1996 (DOJ, 62 FR 61344 at 61414) | T3 outside the bar |
| SSI 40 quarters (8 U.S.C. 1612) | rarely met | US work before adjustment counts, undocumented work included | T3 |
| SNAP (7 CFR 273.4) | 5 years or 40 quarters | 5 years from adjustment or 40 quarters; the pre-1996 route does not help | T3 at adjustment; T2 as a variant |
| Social Security | little US covered work | all covered earnings count once a work-authorized SSN exists (POMS RS 00301.102) | T2 halfway to the Mexico-born mean, T3 at it |
| Premium tax credit, under 65 or in the Medicare wait (26 U.S.C. 36B) | no bar | no bar | keyed by coverage and age for both, in place of the ledger's per-capita share (section 3) |
| Sponsor deeming | until naturalization or 40 quarters | ends at adjustment with 40 quarters; rare in practice (GAO-09-375) | inside observed receipt, as in the tail lane |

[SOURCE: `reads/eligibility_rules.md` §0–§8, each row argued with quotes there]

Premiums: in 2024 Part B cost $174.70 a month, about a quarter of an aged enrollee's cost, with general revenue
paying about three times the premium. Premium Part A cost $505 a month ($278 with 30–39 quarters), the full
average cost of an aged Part A enrollee, so a buy-in at the average has no net public cost. Medicaid cannot pay
an adjuster's premiums during the five-year bar, because the Medicare Savings Programs are Medicaid, so the parent
or family pays them [SOURCE: `reads/eligibility_rules.md` §2: CMS 2024 fact sheet, 42 U.S.C. 1395i-2(d) and
1395r(a), 2025 Medicare Trustees Report, 42 CFR 435.406(a)(2)(ii)].

P.L. 119-21 (4 Jul 2025) keeps LPRs eligible for Medicare, Medicaid and SNAP. From 2026 it ends the credit below
100% of the poverty line for barred LPRs and pending adjusters, and from 2027 it ends it for pending adjusters
altogether. It pays emergency Medicaid at the regular match from 1 Oct 2026. The enhanced 2021–2025 credit lapsed [SOURCE: `reads/eligibility_rules.md` §5–§7,
§9 and its P.L. 119-21 table].

## 3. Method: three arms on the tail lane's machinery

`adjusters.py` imports `../late_arrival_tail_2026_09_27/per_admission.py` read-only. For each age from the
green card to 100 it builds the ledger's Mexico-born items (2024 dollars), scaled by ACS late-arrival earnings
and by receipt by years since arrival, and discounts them with Hispanic survival. Gate: the new-arrival
specification reproduces the tail lane's statutory profiles age by age (to 1e-6) and its NPVs within $0.06,
for every age, case and rate [CALCULATION: assertions in `adjusters.py`].

**The factual profile** (the parent as an LPR) uses the adjuster's clocks from section 2. Types carry the NIS
mean residence before the green card: r = 1, 3, 14 and 30 years for T0–T3 [DATA: mean spells 0.9 / 3.0 /
13.9 / 34.3, `derived/nis_ir5_adjuster_types.csv`; T3 capped at 30]. T2's Social Security is set halfway between
the late-arrival rate and the Mexico-born mean, and T3's at the mean [INFERENCE: assumed from the 43% and 100%
of them who worked here before the green card]. After an early Medicare start, take-up follows the new
arrival's first-eligible curve.

**The premium tax credit is re-keyed**, for new arrivals and adjusters alike.
- *How the ledger charges it.* The ledger charges the credit's outlays per capita, at every age, inside its
  rest-of-budget item R. OMB records the refundable credit in subfunction 551 [SOURCE: OMB Public Budget
  Database, FY2025 Budget outlays, `_cache/ptc/BUDGET-2025-DB-2.xlsx`, account "Refundable Premium Tax Credit",
  subfunction 551 Health care services]. R carries function 550 net of federal Medicaid and CHIP [DATA:
  `../ledger_absolute_2026_09_17/derived/audit.json`, R detail `550_health_net`]. The share comes to $324 a
  person-year [CALCULATION: FY2024 net outlays of $110.2bn (Treasury MTS Table 5) over the ledger's 340.1m
  residents; `derived/ptc_inputs.csv`].
- *Why re-key it.* A parent of 55–64 outside Medicare and Medicaid is far more likely than average to hold
  Marketplace coverage, and the credit has no five-year bar.
- *The keyed amount.* `ptc.py` spreads the same $110.2bn over the 10.1m CPS persons with subsidized Marketplace
  coverage, weighted by the CMS default age curve: $15,893 per covered person at 55, $19,342 at 60 and $21,381
  at 64. Take-up is the CPS rate for Mexico-born naturalized citizens: 4.8% at 45–54, 6.7% at 55–59 and 6.2% at
  60–64 [DATA: `derived/ptc_inputs.csv`].
- *The swap.* Every profile trades the per-capita share for the keyed amount. An unauthorized parent draws no
  credit (26 U.S.C. 36B(e)).
- *Variants.* Noncitizens' take-up (low), the uninsured's take-up in the bar years (high), and the per-capita
  charge kept as in the tail lane. The line uses 2024 rates, so it overstates the credit after 2025
  [SOURCE: section 2].

**The counterfactual** is the same parent without the green card, unauthorized for life:
- No federal programs, Social Security or premium tax credit (8 U.S.C. 1611; 42 U.S.C. 402(y); 26 U.S.C. 36B(e)).
  Public care is at the tail lane's floor [DATA: `../lineage_cost_2026_09_19/derived/audit.json`
  `senior_pricing`]: $7,132 a year centrally (peak state coverage), $1,065 in the low case (federal floor) and
  $17,472 in the high case (full coverage everywhere).
- Income and payroll taxes on an on-books share of 60% (44–75%) of a wage 6% (0–14%) lower
  [SOURCE: Kossoudji & Cobb-Clark 2002, `_cache/lit/`; `../dataset_integrity_2026_09_23/derived/cps.md`].
- Presence items identical to the LPR profile: state and local services, the rest of the federal budget per
  capita, excise, sales and property taxes, and capital. They cancel in arm A.
- Enforcement zero centrally, because the ledger keeps it in the per-capita federal budget. A variant charges $565 a
  year [CALCULATION: $6.207bn over 10.99m unauthorized residents, the ledger's parameters].

**Arms.**
- A: the parent would have stayed anyway. Cost = factual minus the counterfactual for life.
- B: the parent would have left. Cost = the factual in full.
- C: factual minus the counterfactual weighted by the chance the parent is still here.
  - T0 recent entrants leave at once; a quarter stay in the high case.
  - T1 leave at 3.6% a year (5.0% low, 1.2% high).
  - T2 and T3 leave at 1.5% a year (2.3% low, 0.7% high).
  - Evidence: after 0–4 / 5–9 / 10+ years of residence, CPS matching gives 5.0% / 3.6% / 2.0% a year.
    Mexican-born aged 35–64 emigrate at 2.1% (men) and 0% (women), and all foreign-born aged 65+ at 2.3%.
    Residual methods give about 1.0%, and MPI assumes 0.7% after 10 years [SOURCE: Van Hook & Zhang 2011,
    Table 1 and literature review; Van Hook 2024; `reads/emigration_quotes.json`].
  - The 1.5% for settled residents is [INFERENCE: between the residual and CPS-matching estimates, since CPS
    matching also counts circular trips].
  - These rates make the value-weighted chance of staying 0.76–0.85 for T2 and T3, 0.53–0.70 for T1 and 0.50–0.59
    for the average adjuster at 3% [CALCULATION: `derived/breakeven.csv`, `p_stay_central_implied`].

What is measured and what is assumed:

| Input | Status | Source |
|---|---|---|
| Type shares, residence spells, prior work | measured, 2003 | NIS-2003 (section 1) |
| Type mix of FY2019–FY2024 adjusters | assumed equal to 2003 | no later table exists |
| Age mix by channel | measured in 2003, shifted to the tail lane's FY2024 share aged 55+ | NIS-2003; tail lane |
| FY2024 split, 11,760 issued abroad of 63,050 | measured | State Dept Table VIII; DHS OHSS via the tail lane |
| Age profile, receipt by years since arrival | measured | ledger (CPS, MEPS 2024); ACS via the tail lane |
| Eligibility clocks | law | `reads/eligibility_rules.md` |
| Social Security of T2 and T3 | assumed | NIS work histories |
| Medicare take-up of adjusters | assumed equal to new arrivals' first-eligible curve | ACS via the tail lane |
| Premium tax credit | measured total, allocated by coverage and age | Treasury MTS, CPS ASEC 2025, CMS age curve |
| Public-care floor | modelled | lineage lane |
| Tax gain from legalization | measured under IRCA | Kossoudji & Cobb-Clark 2002; CPS comparison |
| Departure without the green card | measured for broader groups; the value for these parents is assumed | Van Hook & Zhang 2011; Van Hook 2024 |

## 4. Cost per admission at 55, 60 and 65

Remaining-lifetime net cost per admission, Mexican IR-5 parent, central case ($k, 2024 dollars):

| | 3%: 55 | 60 | 65 | 0%: 55 | 60 | 65 |
|---|---:|---:|---:|---:|---:|---:|
| New arrival, tail lane (credit per capita) | 270 | 275 | 286 | 525 | 478 | 437 |
| New arrival, credit keyed to coverage | 274 | 275 | 288 | 527 | 476 | 437 |
| Adjuster, arm A: would have stayed anyway | 185 | 182 | 186 | 364 | 322 | 288 |
| Adjuster, arm B: would have left | 290 | 296 | 318 | 554 | 507 | 476 |
| **Adjuster, arm C: evidence-based departures** | **237** | **235** | **240** | **463** | **412** | **370** |
| Adjuster, arm C, departure range | 222–245 | 220–242 | 225–247 | 434–478 | 385–425 | 346–381 |
| Adjuster, arm C, never-EWI type mix | 241 | 238 | 243 | 471 | 418 | 375 |
| Adjuster, arm C, credit per capita (like for like with the tail lane) | 230 | 231 | 241 | 456 | 409 | 371 |

[DATA: `derived/arms_by_age.csv`, variant central (rows 1 and 8 variant ptc_off), counterfactual central, case
central; profiles `new_arrival`, `adjuster_nis_all` and `adjuster_nis_no_ewi`. The first row is this lane's
`ptc_off` new arrival, which the gate ties to `../late_arrival_tail_2026_09_27/derived/per_admission.csv`.]

By type at 3%, arms A / B / C ($k):

| Type (share) | 55 | 60 | 65 | Value-weighted chance of staying |
|---|---|---|---|---:|
| T0 recent entrant (28%) | 169 / 274 / 274 | 161 / 275 / 275 | 156 / 288 / 288 | 0 |
| T1 settling (19%) | 169 / 274 / 219 | 161 / 275 / 208 | 157 / 289 / 197 | 0.53–0.70 |
| T2 long resident (40%) | 193 / 297 / 218 | 192 / 306 / 215 | 199 / 331 / 219 | 0.76–0.85 |
| T3 since before 1996 (13%) | 219 / 323 / 244 | 225 / 339 / 248 | 249 / 381 / 268 | 0.76–0.85 |
| New arrival, for comparison | 274 | 275 | 288 | |

[DATA: `derived/arms_by_age.csv`; `derived/breakeven.csv` for the last column]

- **T0 and T1.** At 55 and 60 they cost exactly what a new arrival costs if they would have left: their Medicaid,
  SSI and SNAP bars run from adjustment, and their shorter Medicare wait (4 or 2 years) ends before they turn 65
  anyway. At 65 they reach Medicare 1–3 years sooner.
- **T2 and T3.** They cost more than a new arrival if they would have left. Social Security on earlier covered
  work adds $31k (T2) and $63k (T3) at 60. At 65, immediate Medicare (with Medicaid for T3) adds $9k (T2) and $16k
  (T3) of medical cost. Being on Medicare also means they draw no credit, which saves $6k against a new arrival
  who draws it during the wait [DATA: `derived/adjuster_items.csv`].

What the green card changes for a T2 long resident adjusting at 60 (3%, $k, positive = revenue):

| Item group | New arrival | T2 as LPR (arm B) | T2 unauthorized for life | Arm A: the difference |
|---|---:|---:|---:|---:|
| Taxes on earnings (income, payroll, corporate) | +72.7 | +72.7 | +45.3 | +27.5 |
| Social Security and SSI | −88.3 | −119.5 | 0 | −119.5 |
| Public medical care | −192.2 | −192.2 | −102.0 | −90.2 |
| Premium tax credit, net of the per-capita share | −0.2 | −0.2 | +5.7 | −5.9 |
| SNAP and other noncash | −3.4 | −3.4 | 0 | −3.4 |
| Presence items (services, excise, sales and property taxes, capital, rest of budget) | −63.8 | −63.8 | −63.1 | −0.8 |
| Total | −275.3 | −306.4 | −114.1 | −192.3 |

[DATA: `derived/adjuster_items.csv`, age 60, rate 0.03. The credit row nets the keyed credit against the
per-capita share taken out of R. The −0.8 is the ledger's refundable-credit improper payments, which an
unauthorized parent cannot claim.]

The green card turns a parent who already costs $114k (public care at the floor and shared services, net of the
taxes paid on the books) into one who costs $306k. The $192k difference is the admission's cost if the parent was
staying anyway [CALCULATION: same table].

## 5. The FY2024 flow and where the premise fails

Mexico's FY2024 IR-5 flow: 63,050 green cards, 11,760 of them visas issued abroad (18.7%) [DATA:
`../late_arrival_tail_2026_09_27/derived/ir5_flow.csv`; `../ir5_fraud_and_cohorts_2026_09_27/reads/ir5_mexico_iv_issued.csv`].
The age mix gives each channel its NIS-2003 age distribution, with a common odds shift so that 38% of the flow is
55+ (the tail lane's FY2024 central; 48% upper). The script checks that valuing the whole flow as new arrivals
with the credit per capita reproduces the tail lane's −$15.9bn [CALCULATION: assertion in `mix_and_flow.py`].

| FY2024 Mexican IR-5 flow | Per admission, 3% ($k) | Flow, 3% ($bn) | Per admission, 0% ($k) | Flow, 0% ($bn) |
|---|---:|---:|---:|---:|
| All as new arrivals, tail lane (credit per capita) | 252 | −15.9 | 525 | −33.1 |
| All as new arrivals, credit keyed | 255 | −16.1 | 528 | −33.3 |
| Observed split, adjusters valued as new arrivals at their own ages | 255 | −16.1 | 529 | −33.3 |
| Observed split, arm A | 186 | −11.7 | 393 | −24.8 |
| Observed split, arm B | 267 | −16.8 | 549 | −34.6 |
| **Observed split, arm C** | **227** | **−14.3** | **477** | **−30.1** |
| Arm C, departure range | 215–232 | −13.5 to −14.7 | 453–490 | −28.5 to −30.9 |
| Arm C, never-EWI type mix | 230 | −14.5 | 484 | −30.5 |
| Arm C, upper age mix (48% aged 55+) | 230 | −14.5 | 467 | −29.5 |
| Arm C, credit per capita | 220 | −13.9 | 471 | −29.7 |

[DATA: `derived/flow_fy2024.csv`, case central, counterfactual central, type mix `nis_all` unless named]

At 3%, new arrivals average $263k and adjusters $218k per admission. Valued as new arrivals at their own ages, the
adjusters would average $254k, so their younger ages change almost nothing. Nearly all of the $1.8bn gap between
−$16.1bn and −$14.3bn comes from the adjusters' clocks and counterfactual [DATA: `derived/flow_fy2024.csv`,
columns `mean_new_arrival`, `mean_adjuster`, `mean_adjuster_as_new_arrival`, `flow_adjusters_as_new_bn`].

**Two numbers decide the sign.**
1. *The chance of staying without the green card.* Arm C lies between A and B. The stay probability p* at which
   an average adjuster costs the same as a new arrival of the same age is 0.15 / 0.18 / 0.23 at 55 / 60 / 65 at
   3% (0.14 / 0.17 / 0.21 undiscounted) [DATA: `derived/breakeven.csv`]. The departure rates imply 0.50 / 0.54 /
   0.59. For the long residents alone p* is 0.23–0.33 (T2) and 0.47–0.71 (T3). A T3 parent who would have gone
   home costs $323–381k. For T0 and T1, p* is 0–0.01, because their cost if they would have left equals the new
   arrival's.
2. *The public care an unauthorized senior draws.* Every value is linear in this floor. It enters arm A with the
   opposite sign from the new arrival's barred years, because the parent would draw it for life without the green
   card. The adjuster costs less than a new arrival while the floor exceeds $2,024 / $2,136 / $3,012 a year at
   55 / 60 / 65 at 3% ($1,662 / $1,768 / $2,607 undiscounted; $1,565 / $1,602 / $2,478 at 3% with the never-EWI
   mix). Each $1,000 a year of floor moves the gap by $7.1k / $8.1k / $11.4k [DATA: `derived/breakeven_floor.csv`,
   case central, arm C_central; the four floors fit a line with a largest residual of $0.12].

The lineage lane prices the floor, at central prices, at:
- $1,903 a year for the federal floor (emergency Medicaid and uncompensated care);
- $2,667 under the 2026 state rules for new enrollees;
- $7,132 at peak state coverage, the tail lane's central;
- $12,626 for full coverage everywhere.

[DATA: `derived/adjuster_provenance.json`]

New arrival minus adjuster (arm C) at 3%, $k (positive: the adjuster costs less), and p* at 3%:

| Variant | 55 | 60 | 65 | p*, 55–65 |
|---|---:|---:|---:|---:|
| Central | +37 | +40 | +47 | 0.15–0.23 |
| Floor: 2026 state rules for new enrollees | +5 | +4 | −4 | 0.38–0.64 |
| Floor: federal only | −1 | −2 | −13 | 0.49–0.82 |
| Floor: full state coverage everywhere | +76 | +85 | +110 | 0.08–0.10 |
| Tail lane's low case (federal floor at low prices, Medicare weight 0.75) | −7 | −9 | −25 | 0.74–1.22 |
| Tail lane's high case (full coverage at high prices, Medicare weight 0.55) | +110 | +124 | +168 | 0.02–0.07 |
| Receipt indexed on years since arrival (T2, T3) | +20 | +8 | +10 | 0.31–0.51 |
| Social Security of T2 at the Mexico-born mean | +27 | +28 | +31 | 0.24–0.35 |
| Social Security of T2 and T3 at the late-arrival rate | +52 | +61 | +74 | 0.00–0.03 |
| Earnings of T2 and T3 at the Mexico-born mean | +42 | +44 | +49 | 0.03–0.20 |
| SNAP from adjustment for T2 (40 quarters) | +36 | +40 | +47 | 0.16–0.23 |
| Medicare premiums credited to both | +34 | +36 | +50 | 0.17–0.22 |
| Credit per capita, as in the tail lane | +40 | +44 | +46 | 0.14–0.25 |
| Credit take-up of noncitizens | +37 | +40 | +45 | 0.15–0.25 |
| Credit take-up of the uninsured in the bar years | +38 | +43 | +61 | 0.13–0.16 |
| Smaller tax gain from legalization (wage premium 0, on-books 75%) | +27 | +33 | +43 | |
| Larger tax gain (wage premium 14%, on-books 44%) | +46 | +48 | +52 | |
| Enforcement $565 a year while unauthorized | +43 | +46 | +52 | |

[DATA: `derived/arms_by_age.csv`, `derived/breakeven.csv`; case central unless named; p* is not defined for the
counterfactual variants in `breakeven.csv`]

**When "$270–286k is an upper bound for adjusters" holds.** Compared at the same age and on the same
assumptions, it holds in every row above except three:
- the federal-only floor, at every age;
- the 2026 state rules, at 65;
- the tail lane's low case, at every age.

For the FY2024 flow it holds in every central-case and high-case variant except the federal-only floor, where the
adjusters cost $0.17bn more; under the 2026 rules the margin is $0.12bn. It fails in the tail lane's low case, by
$0.2–1.1bn in most variants [DATA: `derived/flow_fy2024.csv`].

**When it fails.**
1. *If most adjusting parents would have left without the green card.* The average value-weighted chance of
   staying must stay above 0.15–0.23, or above 0.23–0.33 among long residents alone. For a T3 parent who would
   have gone home, the new-arrival figure understates the cost by $49k / $64k / $93k at 3% [CALCULATION:
   $323k / $339k / $381k against $274k / $275k / $288k].
2. *If an unauthorized senior would draw less than about $2.0–3.0k a year in public care.* That covers the federal
   floor alone, in states that give unauthorized seniors no coverage, and new enrollees under the 2026 rules at
   65.
3. *In combination.* In the tail lane's low case, with receipt indexed on years since arrival, the adjuster costs
   $22k / $39k / $61k more than a new arrival on the same assumptions at 3%. That is $12k / $25k / $30k more than
   even the tail lane's central $270k / $275k / $286k [DATA: `derived/arms_by_age.csv`, case low, variant
   index_since_arrival].

Taken literally against the tail lane's central figures, arm C stays below $270k / $275k / $286k in every
central-case variant; the closest is the federal-only floor at 55, $2k below. Arm B exceeds them by up to $69k at
3%. It ties at 60 only where Medicare premiums are credited or T2 and T3 get the late-arrival Social Security
[DATA: same file].

**Not modelled.** Each item below either raises the adjuster's cost relative to the truth or bounds it with a
variant.
- *LPR emigration.* Neither this lane nor the tail lane lets an LPR leave; only the arm C counterfactual departs.
  This raises C.
- *Medicare take-up in the bar years.* Adjusters in the Medicaid bar pay their own premiums, with no Medicare
  Savings Program, and probably enroll less than the new arrivals' curve assumes. This raises B and C for T2.
- *Part D Extra Help from adjustment.* It sits inside the Medicare item.
- *The credit for pending applicants before the green card.* It falls outside the admission's window.
- *Post-2025 credit rules.* They are bounded by the credit variants.
- *Floors for existing enrollees under the 2026 rules.* The lineage lane prices new enrollees only.
- *The parole route as its own type.* No count exists (section 1).

## Run, gates and files

From the repository root:

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/ohss_lias.py      # fetches the OHSS workbooks if missing
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/nis_adjusters.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/ptc.py            # fetches the MTS file if missing
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/adjusters.py      # about 3 minutes
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/mix_and_flow.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/ir5_adjusters_2026_09_27/verify.py        # reruns all five
```

`verify.py` checks four things:
- the 249 quotes in `reads/*_quotes.json` against their cached sources;
- a rerun of the five scripts, each with exit 0, which fires their gates;
- every file in `derived/` rewritten by that rerun and byte-identical to the file before it;
- the headline numbers of sections 4 and 5.

The scripts' own gates are:
- the six OHSS table titles in every workbook, and each extracted row's total against its two parts;
- the NIS row counts (8,573 adults, 995 IR-5 parents);
- the new-arrival profiles and NPVs against the tail lane;
- the FY2024 credit total against its fiscal-year-to-date figure, and the CY2024 total against
  `dataset_integrity_2026_09_23`;
- the NIS age mix against the tail lane's (within 0.002);
- the tail lane's FY2024 flow (within $0.01bn);
- the floor fit being linear (within $1).

Files:
- `reads/eligibility_rules.md`, `reads/eligibility_quotes.json`: question 3, from primary text.
- `reads/who_adjusts.md`, `reads/who_adjusts_quotes.json`: question 1, published evidence.
- `reads/emigration_quotes.json`: the departure rates of arm C.
- `derived/nis_ir5_*.csv`, `derived/nis_provenance.json`: question 1 from NIS-2003.
- `derived/ohss_lias_adjust_shares.csv`, `derived/ohss_lias_provenance.json`: question 1, the OHSS
  adjustment-report margins through FY2025.
- `derived/ptc_inputs.csv`, `derived/ptc_provenance.json`: the premium tax credit.
- `derived/adjuster_values.csv`: factual (arm B), counterfactual and arm A NPVs for every profile, variant, case,
  age and rate, plus the counterfactual with departures.
- `derived/adjuster_items.csv`: the item decomposition.
- `derived/adjuster_provenance.json`: input hashes and parameters.
- `derived/arms_by_age.csv`: arms A, B and C by type and for the adjuster averages.
- `derived/flow_fy2024.csv`: the FY2024 flow.
- `derived/breakeven.csv`: the stay probability p* and the value-weighted chance of staying implied by arm C.
- `derived/breakeven_floor.csv`: the break-even floor.
- `_cache/` (ignored): the laws, agency pages and papers read, the NIS extracts, the CMS age curve, the MTS
  credit file, the OMB budget database and the OHSS adjustment-report workbooks.

Judgment calls, each tested by a variant or a range above:
1. The 2003 NIS type mix stands in for FY2024.
2. The departure rates of arm C.
3. The tail lane's barred-year floor serves as the unauthorized parent's lifetime floor.
4. Social Security of T2 and T3.
5. The Medicare clock runs from the NIS start of residence, even after a visitor entry (T0).
6. Receipt is indexed from the green card.
7. The premium tax credit is keyed at FY2024 rates in place of the per-capita share.
8. Medicare premiums are not credited (the tail lane's convention).
9. Presence items cancel, and enforcement is zero.

## Revisions

**2026-10-07, the ledger's item T.** The white-reference ledger's expanded account now carries item T, the income
tax the CPS misses, put on the main case's income-tax keys (`ledger_absolute_2026_09_17`, 9d690482). Each parent's
own tax rises, so every arm except A costs less, and new arrivals gain more than adjusters. The figures above are the
record before T. Central case, ages 55 / 60 / 65, at 3% unless noted [DATA: `derived/arms_by_age.csv`,
`derived/flow_fy2024.csv`, `derived/breakeven.csv`, `derived/breakeven_floor.csv`; `verify.py` pins these]:
- Arm C adjuster: $237k / $235k / $240k → $236k / $234k / $240k. New arrival: $274k / $275k / $288k →
  $271k / $273k / $286k.
- With the tail lane's credit treatment: adjuster $230k / $231k / $241k → $228k / $231k / $240k, against
  $270k / $275k / $286k → $267k / $273k / $285k.
- Undiscounted: $463k / $412k / $370k → $462k / $411k / $370k, against $527k / $476k / $437k → $524k / $474k / $435k.
- The adjuster's margin narrows by $1–2k a head.
- FY2024 flow: −$14.3bn → −$14.2bn, against −$16.1bn → −$16.0bn if every parent arrived new. The gap between them
  goes from $1.8bn to $1.7bn. With the tail lane's credit treatment the flow goes from −$13.9bn to −$13.8bn, against
  −$15.9bn → −$15.7bn.
- Per-admission averages: new arrivals $263k → $261k, adjusters $218k → $217k, adjusters valued as new arrivals
  $254k → $251k.
- Arm B: $290k / $296k / $318k → $287k / $294k / $316k. T3 since before 1996: $323k / $339k / $381k →
  $320k / $337k / $379k. Its arm A does not move, and its arm C moves by less than $0.5k.
- Reversal thresholds:
  - Stay probability: 15–23% → 16–23%, against the 50–59% → 50–58% that published departure rates imply.
  - Break-even floor: $2,024 / $2,136 / $3,012 → $2,270 / $2,318 / $3,109 a year. The slopes, $7.1k / $8.1k /
    $11.4k per $1,000 of floor, do not change.
- Under the federal floor alone the adjuster is $3k / $3k / $14k dearer (was $1k / $2k / $13k), and the flow is
  still $0.2bn dearer.
- Under the 2026 state rules the adjuster is $3k / $3k cheaper at 55 / 60 (was $5k / $4k) and $5k dearer at 65
  (was $4k).
- In the tail lane's low case it is $9k / $10k / $26k dearer (was $7k / $9k / $25k).
- The premium tax credit variants do not move.
