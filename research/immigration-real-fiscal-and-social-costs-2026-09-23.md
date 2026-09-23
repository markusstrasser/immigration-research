# Real fiscal and social costs of the Mexican-origin population to other residents

**Verdict:** The published account charges police, courts and prisons per head. Charging them
by use raises the Mexican-origin population's annual cost to other residents by only
**$1.7–5.9bn**, on top of the published **$165–197bn**. The reason is that Hispanic residents
are 20.2% of people in prisons and jails combined, close to their 20.7% share of working-age
residents. In state and federal prisons they are 23.4%. The account compares the group with the
average other resident, not with whites; Hispanic adults are imprisoned at 2.6 times the white
rate. The larger costs sit outside government budgets:

- **Crime victims.** Crimes by group members against other residents cost the victims about
  **$29bn a year** in full cost, including lives lost and pain. The range is $15–45bn, and the
  figure is $43bn if non-fatal offending follows arrest shares. Tangible losses are $4.5bn.
- **Uncompensated hospital care** adds **$1.6–9.2bn**.
- **Housing.** Other renters pay about **$34bn** more rent in the long run ($22–58bn), almost
  all of it to landlords who are other residents, so the net is a small gain (+$0.7–3.5bn).
- **Wages.** Wages move **$66–166bn** a year from less-educated to more-educated natives. Like
  the rent, this is a transfer among other residents, not a net cost.

Stacked on the published band, the use-keyed fiscal cost plus the social items come to about
**$197–244bn a year** at central values (full span $172–261bn), or $4.8–6.0k per group member.
If general government also grows with population (a proposal still open), the total is
**$225–285bn**. Two lanes are still running: road congestion, and an income-weighted version
that counts the transfers, which mostly run from poorer to richer residents (§4).
[CALCULATION: lanes and commits in "Sources"]

Date: 2026-09-23. Operator request: "equal charge --- should it be weighted with use of
courts, police, prisons? Do the remaining common sense stuff to get at the real fiscal and
social costs?"

## 1. Object and frame

Every number below uses the frame of the
[complete annual account](immigration-complete-annual-account-2026-09-20.md). It measures the
effect of the 40,896,574 CPS Mexican-origin residents, all generations and all schooling levels,
on **all other US residents** in 2024. The comparison is stationary, with and without the group,
in 2024 dollars a year. The main CBO-informed case ($165.1–197.4bn net cost) has four settings:

- school spending responds at 63–66%;
- economic-affairs and recreation budgets, highways included, are fixed;
- defense, general public services, existing interest and business subsidies are held at zero
  response by assumption;
- other services respond proportionally.

Its statistical standard error is about $12bn per case (ladder 184). This is not the generation
ledger. Per-person gaps against whites come from a different object and do not combine with
these totals ([FAQ, "Before combining numbers"](immigration-objections-faq-2026-09-21.md)).

## 2. Charging courts, police and prisons by use

Yes, use is the better key. It changes little because of what the account compares against.

| Part of public order and safety (BEA line 4, $519.2bn) | Per head | By use | Change $bn | Key |
|---|---:|---:|---:|---|
| Prisons ($121.3bn) | 12.0% | 14.2% | +2.63 | the group's share of institutional residents 18–64, ACS 2024 |
| Police excluding CBP and ICE custody ($210.7bn) | 12.0% | 13.1% | +2.21 | half arrests, half per head (patrol serves everyone) |
| Law courts ($80.2bn) | 12.0% | 13.3% | +1.01 | 60% criminal, keyed by arrests |
| ICE custody, interior part ($0.9bn) | 12.0% | 22.6% | +0.10 | Mexico's interior bed-day share |
| CBP ($23.9bn) and fire ($80.2bn) | 12.0% | 12.0% | 0 | not driven by residents' offending |
| **Total** | **$62.4bn** | **$68.4bn** | **+5.94** | band $171.1–203.3bn |

[CALCULATION: [justice-by-use lane](../infra/immigration-fiscal/cj_use_allocation_2026_09_23/RESULT.md),
`derived/central_split.csv`; 38 gates, rerun identical]

- **Why it is small.** Hispanic residents hold 20.2% of institutional places at 18–64 and are
  20.7% of household residents that age [DATA: `cj_use_allocation_2026_09_23/derived/acs_hisp_nativity_gq.csv`,
  sum of the Hispanic rows]. BJS counts give the same 20.2% for prisoners and jail inmates
  together. They are 23.4% of sentenced state and federal prisoners, whose ethnicity BJS adjusts
  with its prisoner surveys, and 14.4% of jail inmates, whose counts are unadjusted
  administrative reports. How much of that gap is coding is not established; if jails
  under-record Hispanic origin, the custody key is too low.
  [SOURCE: BJS, *Prisoners in 2023*, Tables 3 and 6; *Jail Inmates in 2023*, Table 5, via the lane]
  Hispanic adults are imprisoned at 606 per 100,000 against 460 for all adults (1.32 times),
  2.62 times the non-Hispanic white rate; non-Hispanic Black adults are at 5.27 times
  [DATA: *Prisoners in 2023* Table 6; `crime_victim_cost_2026_09_23/derived/offender_rate_crosscheck.csv`].
  Removing the group lowers custody costs by its share of custody. The comparison with whites
  belongs to the generation ledger, not to this account. [FRAMING-SENSITIVE]
- **The group's own excess depends on a coding correction.** The group is about 12.4% of
  residents aged 18–64 [CALCULATION: CPS/ACS scaling 1.0824 × ACS Mexican-origin household
  residents 18–64 ÷ all residents 18–64] and holds 14.2% of institutional places once ACS inmates
  coded only as "other Hispanic" are reassigned to named groups. Native "other Hispanic" adults
  show an institutional rate of 4.3%, against 1.2% for all natives, which points to institutional
  records without detailed origin rather than a real group [INFERENCE].
  Without the reassignment the prison share is 12.6% and the whole change is **+$1.67bn**.
- **Police rests on a 2019 arrest share.** It is the last year FBI tables report ethnicity.
  Hispanic adults made up 1.15 times their share of adult arrests. BJS's adult imprisonment
  ratio is also above 1: 1.42 in 2019 and 1.32 in 2023. NCVS victims' perceptions put Hispanic
  offending below the national rate, at 0.80. Carrying the arrest ratio down by the 2019–2023
  fall in imprisonment gives +$4.44bn. At the national arrest rate the central is +$3.19bn.
- **CBP is a boundary call.** Border spending follows crossings, not residents' offending. The
  lane keeps it per head. Holding it fixed, as the account holds defense, lowers the charge by
  $3.11bn (central +$2.84bn). Charging it by Mexico's share of encounters would raise it.
  Per head sits between the two.
- **Nativity.** The custody key raises the charge on US-born members, from $10.2bn to $12.7bn
  for prisons, and barely on the Mexico-born ($4.36bn to $4.51bn). At 18–64, 1.43% of US-born
  Mexican-origin adults and 0.79% of the Mexico-born live in institutions (after reassignment).
- **Full grid:** −$1.03bn to +$8.65bn across 216 key combinations. The Mexican-to-Hispanic
  ratio of 1.14 also moves between files: at its 2016 value (1.08) the central is +$4.70bn.
  [CALCULATION: justice lane `summary.json`, second pass 0a7299c]

## 3. What each priced channel adds

| Channel | What it is | $bn a year to other residents | Measured or modelled | Adds to the net? |
|---|---|---:|---|---|
| Courts, police, prisons by use | reallocation inside the fiscal account | +1.7 to +5.9 (grid −1.0 to +8.7) | measured shares, assumed keys | yes, if adopted (§6) |
| Uncompensated hospital care | government offsets keyed below use; unreimbursed care outside any budget | +1.6 to +9.2 (outside budgets 1.7–4.6) | measured uninsured share, published offsets, assumed use | yes, if adopted (§6) |
| Crime victims' harm | losses of other residents who are victims; excludes justice costs and offenders | 28.9 full (one at a time 23.5–34.0; envelope 15.4–45.3; arrest shares 43.1); 4.5 tangible (1.3–6.0) | measured incidents, modelled prices (lives valued at VSL) | yes, as a social (Z) item |
| Property crime | same frame, arrest-share proxy | 1.3–1.4 | proxy | yes, as Z; separate from the violent figure |
| Housing, net to other residents | rent the group pays to other residents' landlords, less the surplus triangle | −0.7 to −3.5, a gain (range −9.4 to +0.4) | modelled elasticities, measured rents | yes, as Z, long run only |
| Road congestion | delay on a road network held fixed in the main case | lane running | — | main case only |

Sources: [victim harm](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md),
[uncompensated care](../infra/immigration-fiscal/uncompensated_care_2026_09_23/RESULT.md),
[housing](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md).

- **Victims.** The central counts about 1,020 killings and 402,000 non-fatal violent
  victimisations of other residents a year, $707 per group member. Murder is 32% of the full
  cost. Victim-only unit prices (Miller et al. 2021) are used, as the
  [crime-harm rule](immigration-policy-causal-evidence-2026-09-20.md) requires. The older
  McCollister prices double count deaths, which is corrected in e8eab52. The offender input
  is the weakest link. NCVS victims perceive Hispanic non-fatal offending at 0.94 times the
  white rate, while arrests and imprisonment put it far higher. The $43.1bn arm uses arrest
  shares.
- **One footing for both crime lanes.** The justice central assumes Mexican-origin offending
  sits above the Hispanic average as custody does (ratio 1.14). The victim central assumes the
  two are equal. On the equal footing the pair is **+$1.7bn and $28.9bn**; on the custody
  footing it is **+$5.9bn and $32.3bn**.
  [CALCULATION: justice `summary.json` `scaling_raw`; victim `arms.csv` "ACS institutional ratio 1.118"]
- **Uncompensated care.** The group holds 25.7% (SE 0.6) of the nation's uninsured
  person-years against 12.0% of residents: 35.1% of the Mexico-born are uninsured and 14.3% of
  US-born members. That is $11.0–13.2bn of hospitals' uncompensated care. Governments offset
  65–80% of it (Urban Institute), and the account keys those offsets at 12–20%. The lower end
  assumes the group's uninsured use hospitals at 0.7 times the average.
- **Housing.** The long-run arm matches the account's primary case: structures are rebuilt and
  land is scarce. The short-run arm (fixed stock: renters pay $110–120bn) must not be paired with
  it. Monras (2020) finds rents *fall* with low-skilled Mexican inflows because construction
  gets cheaper. The repo's decade estimate (ladder 183) cannot reject that.

## 4. Transfers among other residents: not added, but who bears them

At fiscal weight 1 these cancel inside "other residents", and the production term already
contains their net. They answer who pays, not how much.
[CALCULATION: [wage split](../infra/immigration-fiscal/wage_distribution_2026_09_23/RESULT.md) (3afdb25);
[housing](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) §4, §8]

| Who | Long-run change a year |
|---|---|
| Less-educated native workers | wages 2.2–7.0% lower, −$66 to −$166bn (ε = ∞, the account's default); −$26 to −$107bn at ε = 3 |
| More-educated native workers | wages 1.0–3.0% higher, +$71 to +$163bn |
| Less-educated workers born abroad outside the group | −$14 to −$30bn (−$24 to −$50bn at ε = 3) |
| Natives as a whole, after tax | −$14.6 to −$0.3bn (+$26 to +$59bn at ε = 3) |
| Renter households outside the group (38.99m) | +$22 to +$58bn rent, central $34bn, about $860 a household |
| Owner-occupiers outside the group (80.64m) | +$1.2 to +$3.3tn home value, a stock |

The wage figures are the account's calibrated CES, not a measured wage effect. Measured wage
effects on less-educated natives are disputed in both directions
([canon audit](immigration-canon-citation-audit-2026-09-17.md)). The dollar size depends on
where the skill line falls and on the substitution elasticity σ.

**The transfers run from poorer to richer residents.** Less-educated workers and renters pay.
More-educated workers, landlords and, as a stock, homeowners gain. The same direction likely
holds where the account nets gains without showing who gets them. Cheaper low-wage services go
mostly to higher-income households: the top income quintile receives 43% of the consumer gain,
the bottom 9% [SOURCE: [prices memo](immigration-consumer-price-and-native-hours-2026-09-18.md),
`partA_price_results.csv`]. Violent victimisation is highest in low-income households
[UNVERIFIED here; the distribution lane reads the NCVS tables]. The fiscal gap may run the
other way, because federal taxes are progressive. Counting a dollar as a dollar, as the account
does, hides all of this. The standard fix is to weight each dollar by the recipient's income
relative to the mean, raised to −η. A distribution lane is dividing each channel's total by
income quintile of other residents and reporting the net at η = 0, 1, 1.3 and 2. Choosing η is
a value judgment, so every value is shown. [INFERENCE; FRAMING-SENSITIVE]

## 5. Checked and not found, or already inside the account

- **Native out-migration** from California is real, but the $2.1bn of state-local revenue it
  costs is 1.1% of that state's gap. It tracks top tax rates, not the Mexican-origin share
  (ladder 139).
- **Displaced natives drawing transfers:** no take-up on the margins measurable for 2000–2010.
  The instrument is weak on exogeneity, so this is a null, not a reversal (ladder 140).
- **Flight from public schools** does not reproduce. Local revenue falls where Hispanic
  enrollment rises, and state aid mostly offsets it (ladder 141).
- **Neighbourhood upkeep and petty disorder:** no group effect at equal income (ladder 142).
- **Extra school costs** in the districts where the group lives are already priced: the
  district differential is $0.50–0.56bn
  ([school lane](../infra/immigration-fiscal/school_enrollment_2026_09_20/README.md)).

## 6. What the operator is asked to decide

These change the analysis protocol, so they are proposals.

1. **Key public order and safety by use** in the headline: prisons by custody, police half by
   arrests, courts by the criminal share. Choose CBP per head (lane central) or fixed. My view:
   per head, because both alternatives rest on counterfactual border flows the account does not
   model.
2. **Key uncompensated hospital care** to uninsured use, and carry the unreimbursed part as a
   cost outside the budget.
3. **General government at 0.59–0.84 response** instead of zero. This has been open since
   September 21 and adds $28.5–40.6bn: cross-state spending on administration scales with
   population at 0.84 ([explorer README](../infra/immigration-fiscal/assumption_explorer_2026_09_21/README.md)).
4. **Report victims' harm and the housing net as social (Z) items beside the fiscal headline**,
   never folded into a figure labelled fiscal.

## 7. Putting the pieces together

The rules: transfers (§4) are not added. The ledger and this account are not mixed. Each item
below is built in this account's frame and does not overlap the others: victims' harm excludes
justice costs, housing excludes the production term, uncompensated care is net of offsets
already charged. [CALCULATION: sums of the rows above]

The two crime lanes enter on one footing at a time (§3).

| $bn a year | Mexican-origin rates = Hispanic | Custody ratio carried over |
|---|---:|---:|
| Published fiscal net cost, main case | 165.1–197.4 | 165.1–197.4 |
| + courts, police, prisons by use | +1.7 | +5.9 |
| + uncompensated hospital care, equal use | +4.3 to +9.2 | +4.3 to +9.2 |
| = fiscal, keyed by use | 171–208 | 175–213 |
| + crime victims' harm, full cost | +28.9 | +32.3 |
| − housing net gain | −3.5 to −0.7 | −3.5 to −0.7 |
| **= total at central values** | **197–237** | **204–244** |
| Per group member | $4.8–5.8k | $5.0–6.0k |

Stacking every low choice, then every high one (justice grid, uncompensated care at 0.7× use,
the victim envelope, the housing range), spans **$172–261bn**, or $4.2–6.4k per member.
Setting general government at 0.59–0.84 response adds $28.5–40.6bn, giving **$225–285bn**
at central values. The published figure is $4.0–4.8k per member.

The sign does not depend on any item here. As before, it turns only if public services do not
grow with the population.

## 8. Still unpriced

- **Road congestion.** In the main case highway and transit budgets are fixed, so the group's
  traffic shows up as delay rather than spending. A lane is running
  (`infra/immigration-fiscal/congestion_2026_09_23/`).
- **Innovation and automation.** Low-skill labour supply may slow mechanisation; nothing is
  priced for this group.
- **Institutions, politics and trust.** No dollar measure is defensible from held data.
- **Amenity and culture.** Housing prices show no amenity discount (ladder 155). At matched
  age, education and sex, creative labour per head is 0.72–0.74 of whites' (ladder 156).
- **Remittances** are not a cost in this frame. They are the group's own income, and the
  consumption taxes they displace are already in the account's receipts.

## Limits

- The victim figure prices lives at the value of a statistical life and includes pain and
  suffering, so it is a welfare measure, not a budget cost. Its $4.5bn tangible part is the
  closest analogue to budget dollars. [FRAMING-SENSITIVE]
- The police key (half by arrests), the court criminal share (50–75%), CBP, and the offset
  shares for uncompensated care are assumptions with stated ranges.
- Input years differ: BEA 2024, ICE FY2024, arrests 2019, BJS 2023, NCVS 2022–2024,
  ACS 2024, CPS March 2025, AHA 2020.
- Built with an LLM on a politically charged topic ([bias caveat](../notes/llm-bias-caveat.md)).
  Each lane exports its inputs and disconfirming arms so every key can be rechecked.

## Sources

| Lane | Commit | Result |
|---|---|---|
| [Justice by use](../infra/immigration-fiscal/cj_use_allocation_2026_09_23/RESULT.md) | c124ac7, 0a7299c | +$5.94bn central; +$1.67bn raw coding; +$2.84bn with CBP fixed |
| [Crime victims' harm](../infra/immigration-fiscal/crime_victim_cost_2026_09_23/RESULT.md) | d5cf290, 95ed28d | $28.9bn full / $4.5bn tangible; $43.1bn on arrest shares |
| Double-count correction in older crime prices | e8eab52 | McCollister risk-of-homicide premium removed |
| [Housing transfer](../infra/immigration-fiscal/housing_transfer_2026_09_23/RESULT.md) | 073a79d | renters +$34bn; net +$0.7–3.5bn |
| [Uncompensated care](../infra/immigration-fiscal/uncompensated_care_2026_09_23/RESULT.md) | 06a42b7 | +$1.6–9.2bn |
| [Wage split](../infra/immigration-fiscal/wage_distribution_2026_09_23/RESULT.md) | 3afdb25 | −$66 to −$166bn / +$71 to +$163bn |
| [Congestion](../infra/immigration-fiscal/congestion_2026_09_23/BRIEF.md) | 77d25cf (brief) | running |
