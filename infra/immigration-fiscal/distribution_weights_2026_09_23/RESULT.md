**Verdict:** Relative to income, every channel except tax-financed fiscal cost falls hardest on
the bottom of the income distribution. Outside the budget the channels nearly cancel in dollars
but move money up the income scale. The bottom four fifths of other residents lose $80.7bn a year
and the top fifth gains $46.0bn, for a net of −$34.7bn. Weighted by income, those channels are
as bad as an equal per-person loss of $94–111bn at η = 1–2, 2.7–3.2 times their dollar sum.

The fiscal cost is $227.9bn. It is progressive if financed in proportion to taxes paid: the top
fifth bears 62% of it. It is regressive if financed by equal per-person service cuts: 8.0% of the
bottom fifth's resources against 0.85% of the top fifth's.

The central total is −$262.6bn. Under tax-share financing it takes 5.2% of the bottom fifth's
resources and 1.8% of the top fifth's. Under per-person cuts it takes 12.1% and 0.0%.

Brief's weighted formula (per person, 5th-percentile floor): at η = 1.3 the total is −$407bn
under tax-share financing and −$738bn under per-person cuts. Most of the move from −$263bn comes
from normalizing weights to mean income. On a normalization-free equal-split scale the totals are
−$182bn and −$330bn.

[CALCULATION: `distribute.py` → `derived/channel_by_quintile.csv`, `derived/regressivity.csv`,
`derived/weighted_totals.csv`] [FRAMING-SENSITIVE: the two financing conventions and every η are
value choices; all are shown]

Model self-report: `claude-opus-5-5[1m]`. Date: 2026-09-23. Brief: `BRIEF.md` (73077d1,
amended c43a401). Not committed.

## Headline tables

Other residents are the 295.83m CPS ASEC 2025 civilians outside the 40.90m Mexican-origin
target. They are ranked by SPM resources ÷ SPM equivalence scale. Each quintile holds 59.2m
persons (27.1m, 23.9m, 23.8m, 24.7m and 25.6m households). Signs are from other residents' point
of view. [DATA: CPS ASEC 2025 public-use file; CALCULATION: `derived/income_frame.csv`]

**Channel by income quintile, $bn a year (SPM quintiles)**

| Channel | Total | Q1 | Q2 | Q3 | Q4 | Q5 | Losses on Q1–Q2 | Gains to Q4–Q5 | % of resources, Q1 / Q5 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Fiscal cost, (a) tax shares | −227.9 | −6.9 | −14.6 | −24.6 | −40.3 | −141.6 | 9% | — | −1.22 / −2.64 |
| Fiscal cost, (b) per person | −227.9 | −45.6 | −45.6 | −45.6 | −45.6 | −45.6 | 40% | — | −8.03 / −0.85 |
| Wages, after tax | −1.5 | −4.8 | −11.1 | −11.8 | −4.2 | +30.4 | 23% | 85% | −0.84 / +0.57 |
| Renters' extra rent | −33.9 | −7.8 | −6.6 | −6.3 | −6.1 | −7.0 | 43% | — | −1.37 / −0.13 |
| Landlords' receipts | +37.4 | +0.6 | +1.3 | +2.6 | +4.2 | +28.7 | — | 88% | +0.11 / +0.53 |
| *Housing net (renters + landlords)* | +3.5 | −7.2 | −5.3 | −3.8 | −1.9 | +21.7 | 63% | 98% | −1.27 / +0.40 |
| Crime victims' harm | −32.3 | −10.4 | −6.5 | −5.5 | −5.0 | −4.9 | 52% | — | −1.83 / −0.09 |
| Unreimbursed hospital care | −4.4 | −0.5 | −0.7 | −1.0 | −1.1 | −1.2 | 27% | — | −0.08 / −0.02 |
| **Total, (a)** | **−262.6** | −29.8 | −38.1 | −46.7 | −52.5 | −95.6 | 24% | 84% | −5.24 / −1.78 |
| **Total, (b)** | **−262.6** | −68.4 | −69.1 | −67.7 | −57.8 | +0.4 | 44% | 98% | −12.06 / +0.01 |
| Consumer prices (side view, never added) | +23.8 | +2.2 | +2.7 | +3.8 | +5.5 | +9.7 | — | 64% | +0.39 / +0.18 |

"Losses on Q1–Q2" is the bottom two quintiles' share of the channel's gross losses, summed over
the persons who lose. "Gains to Q4–Q5" is the top two quintiles' share of gross gains. "% of
resources" divides each quintile's dollars by its SPM resources. The total is fiscal cost plus
wages, housing net, crime and unreimbursed care. [CALCULATION: `derived/channel_by_quintile.csv`,
`derived/regressivity.csv`]

Four channels need more than the table shows:

- **Housing** moves money from renters in every quintile to landlords at the top. Renters' extra
  rent is almost the same in dollars in every quintile. Per renter household it runs from $566 in
  the bottom ACS fifth to $1,770 in the top, but the bottom fifth has 13.8m renter households and
  the top 4.0m. Landlords' receipts go 77% to the top fifth and 65% to the top tenth.
  [CALCULATION: `derived/rent_per_renter_household_acs.csv`, `derived/channel_by_decile.csv`]
- **Wages** are a transfer inside the labor market. The top two deciles gain $30.4bn and deciles
  1–8 lose. The losers are the below-BA workers of the lower and middle quintiles.
  [CALCULATION: `derived/channel_by_decile.csv`]
- **Crime harm** per household is $384 in the bottom fifth and $191 in the top: 20 times the share
  of resources. [CALCULATION: `derived/channel_by_quintile.csv`]
- **Fiscal (a):** the top decile alone bears 48% of the fiscal cost. [CALCULATION:
  `derived/channel_by_decile.csv`]

**Per other-resident household, $ a year (SPM quintiles)**

| Channel | Q1 | Q2 | Q3 | Q4 | Q5 | All |
|---|---:|---:|---:|---:|---:|---:|
| Fiscal cost, (a) | −255 | −610 | −1,033 | −1,632 | −5,537 | −1,823 |
| Fiscal cost, (b) | −1,682 | −1,906 | −1,917 | −1,846 | −1,783 | −1,823 |
| Wages | −177 | −462 | −498 | −170 | +1,189 | −12 |
| Renters | −288 | −275 | −266 | −248 | −274 | −271 |
| Landlords | +22 | +55 | +107 | +171 | +1,122 | +299 |
| Housing net | −265 | −221 | −159 | −77 | +847 | +28 |
| Crime victims' harm | −384 | −271 | −232 | −204 | −191 | −259 |
| Unreimbursed care | −17 | −30 | −41 | −45 | −45 | −35 |
| **Total, (a)** | −1,098 | −1,594 | −1,963 | −2,127 | −3,737 | −2,100 |
| **Total, (b)** | −2,525 | −2,891 | −2,847 | −2,342 | +17 | −2,100 |
| Channels outside the budget | −843 | −985 | −929 | −496 | +1,800 | −278 |

Households are other-resident households, 125.0m; a household whose members fall in different
quintiles is split across them. [CALCULATION: `derived/channel_by_quintile.csv`
`usd_per_household`]

**Weighted net, $bn a year (SPM, per person, weights floored at the 5th percentile)**

| | Unweighted | η = 1 | η = 1.3 (Green Book) | η = 1.4 (A-4, 2023) | η = 2 |
|---|---:|---:|---:|---:|---:|
| Total (a), brief's formula Σ(y_i/ȳ)^−η Δ_i | −262.6 | −332.9 | −407.1 | −440.0 | −771.3 |
| Total (a), weights relative to the median | −262.6 | −254.0 | −286.5 | −301.3 | −449.2 |
| Total (a), equal-split equivalent | −262.6 | −192.6 | −181.9 | −178.8 | −164.2 |
| Total (b), brief's formula | −262.6 | −557.0 | −738.3 | −816.3 | −1,591.4 |
| Total (b), weights relative to the median | −262.6 | −425.1 | −519.5 | −559.1 | −926.8 |
| Total (b), equal-split equivalent | −262.6 | −322.4 | −329.9 | −331.8 | −338.8 |
| Channels outside the budget, brief's formula | −34.7 | −163.2 | −228.2 | −255.6 | −520.9 |
| Channels outside the budget, equal-split equivalent | −34.7 | −94.5 | −102.0 | −103.9 | −110.9 |

The three rows per total are one weighted sum on three scales. The brief's formula values a
dollar at its worth to a person at mean income ($121,546). Incomes are skewed (median $92,756),
so the average person's weight is above one: 1.73, 2.24, 2.46 and 4.70 at η = 1, 1.3, 1.4 and 2.
An equal per-person split of the same total would therefore be scaled up by the same factors.

The Green Book and A-4 normalize to the median, which multiplies the brief's figures by
(median/mean)^η = 0.76, 0.70, 0.68 and 0.58. The equal-split equivalent divides by the average
weight. It gives the total that, split equally per person, would be as bad, and it does not
depend on the normalization.

Under (a), the progressive financing makes the total less harmful than an equal split of the same
dollars: −$182bn against −$263bn at η = 1.3. Under (b), it is 26% worse. [CALCULATION:
`derived/weighted_totals.csv`, `derived/weights.csv`] [FRAMING-SENSITIVE]

## Weighted nets by channel

**Brief's formula, $bn a year (SPM, per person, p5 floor)**

| Channel | Unweighted | η = 1 | η = 1.3 | η = 1.4 | η = 2 |
|---|---:|---:|---:|---:|---:|
| Fiscal cost, (a) | −227.9 | −169.6 | −178.9 | −184.4 | −250.4 |
| Fiscal cost, (b) | −227.9 | −393.8 | −510.0 | −560.7 | −1,070.5 |
| Wages | −1.5 | −46.2 | −62.7 | −69.0 | −121.7 |
| Renters | −33.9 | −62.2 | −82.6 | −91.6 | −183.5 |
| Landlords | +37.4 | +21.2 | +20.9 | +21.2 | +27.1 |
| Housing net | +3.5 | −41.0 | −61.7 | −70.4 | −156.5 |
| Crime victims' harm | −32.3 | −70.0 | −96.7 | −108.4 | −229.8 |
| Crime, A-4 treatment (intangible part unweighted) | −32.3 | −38.2 | −42.3 | −44.1 | −62.9 |
| Unreimbursed care | −4.4 | −6.0 | −7.2 | −7.7 | −13.0 |
| Consumer prices (side view) | +23.8 | +28.4 | +33.6 | +35.9 | +60.3 |

**Equal-split equivalent, $bn a year**

| Channel | Unweighted | η = 1 | η = 1.3 | η = 1.4 | η = 2 |
|---|---:|---:|---:|---:|---:|
| Fiscal cost, (a) | −227.9 | −98.2 | −79.9 | −75.0 | −53.3 |
| Fiscal cost, (b) | −227.9 | −227.9 | −227.9 | −227.9 | −227.9 |
| Wages | −1.5 | −26.7 | −28.0 | −28.0 | −25.9 |
| Renters | −33.9 | −36.0 | −36.9 | −37.2 | −39.1 |
| Landlords | +37.4 | +12.3 | +9.4 | +8.6 | +5.8 |
| Housing net | +3.5 | −23.7 | −27.6 | −28.6 | −33.3 |
| Crime victims' harm | −32.3 | −40.5 | −43.2 | −44.1 | −48.9 |
| Crime, A-4 treatment | −32.3 | −33.6 | −34.0 | −34.1 | −34.9 |
| Unreimbursed care | −4.4 | −3.5 | −3.2 | −3.2 | −2.8 |
| Consumer prices (side view) | +23.8 | +16.4 | +15.0 | +14.6 | +12.8 |

Housing and wages are near zero in dollars. On the equal-split scale each costs $24–33bn a year:
both take from below-median residents and give to the top.

A-4 (2023) says population-average values of mortality risk are already income-weighted and
should not be weighted again. Intangible harm (84% of victims' harm) is priced that way, so the
A-4 rows weight only the tangible 16%. That treatment lowers the weighted total by $54bn (a) and
$54bn (b) at η = 1.3 on the brief's scale, and by $9bn on the equal-split scale (rows
`TOTAL_a_A4_crime`, `TOTAL_b_A4_crime`). [SOURCE: OMB Circular A-4 (2023), §10, p. 67;
CALCULATION: `derived/weighted_totals.csv`]

## How much binning, the floor and the income measure move the answer

**Binning.** The brief's quintile-bin version Σ_q (ȳ_q/ȳ)^−η Δ_q uses unfloored bin means. It lands
within 3.5% of the per-person sum for the totals at η = 1–1.4. That match is partly luck: the
bottom bin's mean includes negative SPM resources, which offsets what averaging loses.

Applying the same p5 floor to the bins isolates resolution. Quintile bins then understate the
weighted cost as the brief expected:

- Totals: by 0.5–4.6% (a) and 6.0–9.3% (b) at η = 1–1.4, and by 12% and 17% at η = 2.
- Channels at η = 1.3: housing net by 17%, crime by 12%, renters by 11%. Landlords' gains are
  overstated by 10%.
- Deciles recover most of the gap.

| Total, $bn | η | Per person, p5 | Quintile bins (brief) | Quintile bins, floored | Decile bins, floored |
|---|---:|---:|---:|---:|---:|
| (a) | 1 | −332.9 | −344.6 | −331.1 | −336.1 |
| (a) | 1.3 | −407.1 | −419.4 | −393.0 | −406.4 |
| (a) | 1.4 | −440.0 | −452.5 | −419.9 | −437.5 |
| (a) | 2 | −771.3 | −781.0 | −676.6 | −747.8 |
| (b) | 1 | −557.0 | −554.8 | −523.6 | −548.0 |
| (b) | 1.3 | −738.3 | −737.5 | −676.8 | −722.3 |
| (b) | 1.4 | −816.3 | −815.4 | −740.6 | −796.6 |
| (b) | 2 | −1,591.4 | −1,567.4 | −1,327.2 | −1,519.8 |

[CALCULATION: `derived/weighted_totals.csv` columns `quintile_bins`, `quintile_bins_floored_p5`,
`decile_bins_floored_p5`]

**Floor.** The brief's formula is sensitive to the floor because the floor sets the bottom
weights. At η = 1.3, total (a) is −$594bn with a 2nd-percentile floor ($5,084), −$456bn at the
3rd ($12,783), −$407bn at the 5th ($22,151) and −$370bn at the 10th ($34,102). The equal-split
equivalents are −$165bn, −$176bn, −$182bn and −$188bn. Total (b) is −$328bn to −$335bn on that
scale at every floor.

The 1st-percentile floor is degenerate. On SPM resources it is −$61, so no weight exists. On money
income it is $4, and the weights explode: total (a) reaches −$27 trillion at η = 1 and −$518
trillion at η = 1.3. The p2 and p3 columns are the usable low-floor sensitivities. [CALCULATION: `derived/weighted_totals.csv`
`person_p1`…`person_p10`, `equal_split_p1`…`equal_split_p10`; `derived/income_frame.csv`]

**Income measure.** Ranking by household money income ÷ √size (the check) barely changes the
quintile shares:

- Total (a) by quintile: −26.6, −36.9, −47.1, −54.7, −97.4.
- Total (b) by quintile: −68.1, −69.0, −68.1, −58.5, +1.0.

Money income is lower at the bottom than SPM resources, which add transfers and tax credits. It
therefore raises the brief's-formula totals: at η = 1.3, (a) −$472bn and (b) −$953bn. The
equal-split equivalents are almost unchanged: (a) −$165bn, (b) −$332bn, outside-budget channels
−$104bn. [CALCULATION: `derived/*.csv` rows with `measure = money`]

## Ranges

The ranges stack the most costly and the least costly choice of each channel on the weighted
scale:

- Fiscal: adopted A band, −$216.5bn to −$258.4bn.
- Wages: the grid of splits and σ, with any change in induced receipts financed by the same
  convention.
- Housing: low, central and high × metro-local and national-uniform exposure × INTP, SCF and mid
  landlord keys.
- Crime: victim envelope of $15.4–45.3bn and its key variants.
- Unreimbursed care: $3.2–5.6bn.

| $bn a year (SPM, p5) | Unweighted | η = 1.3, brief's formula | η = 1.3, equal split | η = 1.4, brief's formula | η = 1.4, equal split |
|---|---:|---:|---:|---:|---:|
| (a) most costly | −302.4 | −525.2 | −234.7 | −571.3 | −232.2 |
| (a) least costly | −213.8 | −297.2 | −132.8 | −318.6 | −129.5 |
| (b) most costly | −302.4 | −882.1 | −394.2 | −976.9 | −397.1 |
| (b) least costly | −213.8 | −601.5 | −268.8 | −664.3 | −270.0 |

[CALCULATION: `derived/ranges_weighted.csv`, all η and both measures]

## Sensitivities

- **Wage grid**, after-tax P, $bn:
  - Central (below-BA, σ = 2): −1.47.
  - Other splits and σ: −1.97 (below-BA, σ = 1.5) to −0.12 (high school or less, σ = 2.5).
  - Account's split (high school or less, σ = 2): −0.16.
  - ε = 3: +3.41. By quintile: −6.6, −12.3, −10.2, −0.5, +32.9.
  - Before tax, the central is +8.09. By quintile: −7.7, −17.6, −18.2, −4.6, +56.1.
  - Weighted at η = 1.3 under (a), the grid runs −$81.2bn to −$44.3bn.

  [CALCULATION: `derived/wage_scenarios.csv`, `derived/ranges_weighted.csv`]
- **Short run, fixed capital** (labelled sensitivity, before tax). Wages −$351.6bn plus capital
  +$375.9bn, keyed by CPS interest, dividend and rent income, gives +$24.3bn. By quintile:
  −13.1, −38.1, −46.3, −26.7, +148.5. The top two fifths take 90% of the gross gains. [CALCULATION:
  `derived/channel_by_quintile.csv` `wages_short_run_pretax`]
- **Landlord keys.** The top fifth's share of landlords' receipts is 77.8% on the ACS INTP key and
  75.7% on the SCF key. On SCF 2022, the top 10% of families by equivalized income hold 62% of
  other residential real estate ($8.84tn) and the top 1% hold 24%. Spreading renters' extra rent
  at national-uniform exposure moves the bottom fifth from −7.8 to −8.4. [CALCULATION:
  `derived/inputs.json` `scf`; `derived/channel_by_quintile.csv`]
- **Crime keys.** The bottom fifth's share of victims' harm is 32.2% on the central rank mapping,
  31.6% on dollar brackets and 28.1% with every violent crime keyed by all-violence rates. With
  victims' race mix applied it is 34.3%. On the equal footing ($28.9bn) the shape is the same
  (Q1 −9.3). [CALCULATION: `derived/channel_by_quintile.csv` `crime_*`]
- **Tax key check.** Keying (a) by the CPS tax fields gives the bottom fifth 2.0% and the top
  fifth 59.3% (CBO and ITEP: 3.0% and 62.1%). The weighted fiscal cost stays within 3% at
  η ≤ 1.4 (−178.3 vs −178.9 at 1.3). [CALCULATION: `fiscal_a_cps_tax_fields` rows]
- **Published September 20 fiscal band** in place of the adopted case (brief's $165.1–197.4bn),
  with crime on the equal footing and the under-charged uncompensated care financed by the same
  convention:
  - Totals are −$218.7bn under both conventions.
  - (a) by quintile: −27.4 … −69.9. (b) by quintile: −59.2 … +9.0.
  - At η = 1.3: −$365bn (a) and −$638bn (b) on the brief's scale; −$163bn and −$285bn equal
    split.

  [CALCULATION: `TOTAL_*_published_band` rows]
- **Owner-occupiers' value gain** is a stock, reported and never added. It is $1,931.6bn:
  $191bn, $225bn, $292bn, $408bn and $815bn by quintile, or $7,051 to $31,892 per household.
  [CALCULATION: `owner_value_stock_metro_local_central` rows]
- **Consumer prices** (side view). Of the $23.8bn gain, 41% goes to the top fifth. Relative to
  resources it is the one benefit larger at the bottom: 0.39% against 0.18%. The one-good
  production model already counts price effects through wages and capital, so it is never added.
  [CALCULATION: `consumer_prices_side_view` rows]

## Method

- **Income frame.** CPS ASEC 2025 (income year 2024) comes from the account's sha-gated archive,
  with the target from `full_account_spending_2026_09_20/builder.py` `canonical_target`.
  - Every other resident gets y_i: SPM resources ÷ SPM equivalence scale (central), or household
    money income ÷ √household size (check).
  - Each person has a person-weighted percentile. Ties are broken by record order, so no cell is
    empty.
  - Persons who live with target members keep their own place, and only non-target persons
    count.
  - Weights are (max(y_i, floor)/ȳ)^−η, with ȳ the unfloored person-weighted mean of other
    residents: $121,546 SPM and $84,567 money.
  - Quintiles and deciles are for display only.
- **Resolution.** Channels measured on the CPS are carried per person. ACS and SCF inputs go into
  1,000 percentile cells of that survey's own other-resident ranking (income ÷ √size). Each cell
  is spread over the CPS persons in the same cell. Binned inputs are spread within each bin by the
  microdata base named below.
- **Fiscal cost** is taken as given from the adopted main case (decision
  `decisions/2026-09-23-main-case-general-government-and-use-keys.md`), not the brief's published
  band. The operator adopted the case after the brief was written, and the published band is a
  variant above.
  - The channel is the direct fiscal response A plus the induced receipts F of the central wage
    scenario. A is each case's welfare minus its production term. The adopted A runs −$216.5bn to
    −$258.4bn (midpoint −$237.5bn), and F = +$9.56bn, so the channel is −$227.9bn.
  - Fiscal cost plus wages (−$229.4bn) lies inside the adopted $203.2–249.6bn band. It is
    $3.0bn more costly than the band's midpoint. The band's low end carries the GDP
    normalization's production term ($13.3bn), while the central here takes the below-BA split
    at cash normalization ($8.1bn, $0.7bn below the account's high-school-or-less split).
  - (a) Taxes are attributed to every civilian and the cost is spread over other residents in
    proportion. Federal: CBO's 2022 shares of federal taxes by group (quintiles 1–4, 81–90,
    91–95, 96–99, top 1%) × BEA 2024 federal receipts of $4,976.3bn. State and local: ITEP
    rates × CBO income shares by group × BEA 2024 state-local receipts of $2,553.5bn.
  - Groups are all-civilian percentiles of the same equivalized measure. The SPM ranking uses
    CBO's after-transfer-and-tax tables and the money ranking the before tables. Within a group,
    taxes are spread by per-capita household money income.
  - (b) An equal amount per other resident.
- **Wages.** The central is long run, ε = ∞, below-BA split, σ = 2, cash normalization, labor share
  0.65, zero labor-supply elasticity, nest option A by nativity, earnings proxy PEARNVAL.
  - Each skill cell's percentage wage change is applied to each other-resident worker's earnings
    in that cell, with the branches' cell definitions: A_HGA 31–42 vs 43–46 below-BA; 31–39 vs
    40–46 high school or less.
  - After tax uses the nest's labor tax rates 0.384 and 0.426, so the channel equals the nest's P
    and the tax part equals its F. Both are gated.
- **Housing.** Long run, form A, central ownership, from `housing_transfer_2026_09_23`.
  - Renters: other-resident renter households on ACS 2024 PUMS, each charged RNTP × 12 × ADJHSG ×
    f. Here f = 1 − (1 − s)^e is its PUMA's exposure: the metro-area group share s, averaged over
    the PUMA's areas by allocation factor.
  - Landlords get the renters' $33.9bn plus the housing net ($3.5bn), keyed half on ACS INTP of
    other residents and half on SCF 2022 other residential real estate (ORESRE). Each key is
    also reported alone.
  - Owner values: VALP × ADJHSG × f, by quintile as a stock.
- **Crime victims' harm.** The central is the custody footing ($32.3bn), which the real-costs
  memo §7 pairs with the adopted justice key. The equal footing ($28.9bn) is a variant.
  - The serious part (murder, rape and sexual assault, robbery, aggravated assault; 82.6% of the
    cost) is keyed by NCVS rates of violence excluding simple assault. Simple assault is keyed by
    the simple-assault rates, all for persons 12 and older by household income bracket.
  - Rates are pooled over 2022–2024 with the BJS population weights. CPS civilians 12+ are ranked
    by household money income and placed in the NCVS brackets by the brackets' pooled population
    shares (rank mapping). Dollar thresholds are a variant.
- **Unreimbursed care.** The outside-budget part (midpoint $4.4bn; $3.2–5.6bn) is spread equally
  over other residents with private coverage (PRIV = 1). The under-charged public part
  ($3.7–5.7bn) sits inside the adopted fiscal A, so it follows (a) or (b) with the fiscal cost.
- **Consumer prices.** The CEX quintile split of the central $23.8bn (JPE 2008 elasticities,
  labor-force-adjusted shock, narrow scope) is spread equally per person within money-income
  quintiles of other residents. CPS has no consumption base to spread it by.
- **Weighted nets.** For each channel and each floor (p1, p2, p3, p5, p10):
  - Per person: Σ_i w_i (y_i/ȳ)^−η Δ_i, with w_i the person weight.
  - Quintile and decile bins, with unfloored and floored bin means.
  - Median-normalized: × (median/ȳ)^η.
  - Equal-split equivalent: ÷ the mean weight.
  - η ∈ {0, 1, 1.3, 1.4, 2}. The brief lists 0, 1, 1.3 and 2; 1.4 is A-4's value.

## Sources

- **Guidance on η:**
  - HM Treasury, *The Green Book (2026)*, Chapter 7, "Distributional weighting",
    https://www.gov.uk/government/publications/the-green-book-appraisal-and-evaluation-in-central-government/the-green-book-2026
    (page last updated 5 February 2026). It sets the welfare weight of a group as (median
    equivalised income of the national population ÷ median equivalised income of the group)^1.3.
    "The '1.3' ... is an estimate of the elasticity of marginal utility of income, based on a
    review of international evidence." Practitioners "must present weighted estimates alongside
    unweighted estimates." [SOURCE: `_cache/sources/greenbook_2026.txt`]
  - OMB Circular A-4 (November 9, 2023), §10 "Distributional Effects", pp. 66–67. The weight is
    (ȳ_i / y_med)^−ε, and "OMB has determined that 1.4 is a reasonable estimate of the absolute
    value of the income elasticity of marginal utility". Income is "inclusive of government taxes
    and transfer programs" (fn. 124), which matches SPM resources. Fn. 125 allows the group mean
    in place of the median when incidence is proportional to income. Values of mortality risk
    reduction should not be income-weighted (p. 67, fn. 129). The 1.4 default recurs on p. 74.
    [SOURCE: `_cache/sources/a4_2023.txt`]
  - Later status: Executive Order 14192 (January 31, 2025; 90 FR 9065) §6(b) directs OMB to revoke
    the 2023 Circular and reinstate the 2003 version. OMB Memorandum M-25-15 (February 12, 2025)
    revokes it and reinstates Circular A-4 of September 17, 2003. The 2003 Circular asks for a
    separate description of distributional effects, quantitative where they are important, and
    gives no weights or elasticity. [SOURCE: `_cache/sources/eo14192_govinfo.txt`,
    `omb_m25_15.txt`, `a4_2003.txt`]
  - A web search on 2026-09-23 found no later revision. [UNVERIFIED beyond that search]
- **Taxes:**
  - CBO, *The Distribution of Household Income, 2022* (January 2026, publication 61911),
    additional data for researchers: tables 12 (shares of federal taxes) and 10 (shares of income
    before transfers and taxes), all households, 2022, both rankings.
  - ITEP, *Who Pays?* 7th edition (January 2024), Appendix A "Average Across All States":
    non-elderly, 2024 law at 2023 incomes. Rates are 11.4, 10.4, 10.5, 10.3, 9.5, 8.3 and 7.2%.
    The next-15% rate is used for CBO's 81–90 and 91–95 groups.
  - BEA NIPA Tables 3.2 and 3.3, 2024 (workbook pinned in `sources/`).

  [SOURCE: `_cache/sources/cbo_61911/…`, `itep_ITEP-Who-Pays-7th-edition.txt`; DATA: BEA workbook]
- **Victimization:** BJS, *Criminal Victimization, 2023* (NCJ 309335, revised June 9, 2025),
  Table 3 (2022 and 2023). BJS, *Criminal Victimization, 2024* (NCJ 310547, September 2025),
  Table 3 (2023 and 2024) and Appendix Table 19 (persons 12+ by household income).
  - Pooled violent rates per 1,000, by bracket (<$25k, $25–50k, $50–100k, $100–200k, $200k+):
    40.0, 24.4, 21.1, 17.2, 20.4.
  - Excluding simple assault: 20.4, 9.9, 7.7, 5.8, 6.7.

  [SOURCE: `_cache/sources/bjs_cv23.txt`, `bjs_cv24.txt`; CALCULATION: `derived/inputs.json` `ncvs`]
- **Microdata:**
  - CPS ASEC 2025 public use (`gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip`).
  - ACS 2024 1-year PUMS (`sources/immigration-fiscal/data/external/acs_pums_2024_1yr`).
  - SCF 2022 summary extract (`housing_transfer_2026_09_23/_cache/scf/rscfp2022.dta`).
  - PUMA→county and county→CBSA crosswalks from `employment_entry_2026_09_18` and
    `hedonic_composition_2026_09_19`.
- **Channel totals, read only:**
  - `full_account_2026_09_20/derived/{service_response_cases,headline_cases}.csv`
  - `main_case_2026_09_23/derived/{main_case_bands.csv,inputs.json}`
  - `production_nativity_nest_2026_09_22/derived/{nest_scenarios,branch_composition}.csv`
  - `housing_transfer_2026_09_23/derived/{arms_headline,cbsa_exposure}.csv`
  - `crime_victim_cost_2026_09_23/derived/{cost_by_offence_central,cost_by_victim_and_offence_central,arms}.csv`
  - `uncompensated_care_2026_09_23/derived/added_cost_arms.csv`
  - `consumer_price_benefit_2026_09_18/derived/partA_price_results.csv`

  Every cached document's hash is in `derived/sources_manifest.csv`.

## Gates

`derived/gates.json` lists 212 gates, all passed. [CALCULATION: `distribute.py`]

- **CPS:** the canonical target is 40,896,574.15. Civilians are 336,727,803 and other residents
  295,831,228.85, the brief's control. Household sizes match the records.
- **Account totals:**
  - The published band is reproduced ($165.12–197.38bn), and the adopted band equals published
    plus general government, justice and the inside part of uncompensated care
    ($203.207–249.640bn).
  - The account's production term matches the nest.
  - For seven wage scenarios the CPS earnings bases equal the nest's branch earnings, after-tax
    wage changes sum to the nest's P and tax changes to its F.
  - ACS rent and owner-value totals equal the housing lane's in all six arms.
  - The SCF family count is 131.306m.
  - BEA totals are in range.
- **Pins:** the CBO pins match tables 12 and 10, the ITEP pins match Appendix A, and the NCVS
  cells match both BJS reports' text. The crime central is 28.92/32.34, and uncompensated inside
  matches the main case.
- **Sums:** every channel's quintile split sums to its total (a hard stop), and 17 channels per
  measure sum to the totals given by their lanes. At η = 0 every weighted figure equals the
  unweighted sum (130 gates).

## Limits

- **Imposed incidence** [FRAMING-SENSITIVE]. The fiscal cost is 87% of the unweighted total, and
  its split is a convention. (a) assumes the cost is met by raising every tax in proportion; (b)
  assumes equal cuts in services per person. The actual mix of deficit, tax and service
  responses is not identified. Both use average tax shares, not the marginal incidence of a
  particular tax change.
- **Income mapping.** ACS and SCF households are ranked by money income ÷ √size within their own
  survey and placed at the CPS person with the same percentile on the SPM (or money) measure.
  People who rank differently on SPM resources and money income are misplaced. The error flattens
  the measured concentration of rents and landlord receipts. [INFERENCE]
  - CBO groups are households ranked by size-adjusted income with equal numbers of people.
    ITEP's are non-elderly families. The ITEP rates are applied to all ages and combined with
    CBO's income shares instead of ITEP's dollar shares. CBO's 2022 shares are applied to 2024
    totals.
- **Victim-income proxy.** NCVS reports victimization by unequivalized household income in five
  brackets, and its income item under-reports relative to the CPS. NCVS puts 12.6% of persons
  12+ under $25,000; the CPS puts 9.1% there. Hence the rank mapping as central.
  - The key ignores age, sex, race and place except in the race-mix variant.
  - Homicide (32% of the harm) has no NCVS income profile. It is keyed by serious violent
    victimization, a proxy. [INFERENCE]
  - The crime lane covers violent crime only.
- **Weights** [FRAMING-SENSITIVE]. η is a value judgment. The brief's mean-normalized totals
  depend on the floor and the normalization. The equal-split equivalents are stable across floors
  p3–p10 and both income measures, so they carry the comparison.
  - SPM resources are negative for 1.0% of other residents, because SPM subtracts medical, work
    and child-care expenses and taxes. The floor sets those at the 5th percentile. [CALCULATION:
    CPS ASEC 2025, person-weighted]
  - Normalization uses other residents' mean or median, not the national figure, which would
    include the target group.
- **Within-bin spreading.**
  - Taxes within CBO groups follow per-capita money income, which ignores within-group
    progressivity.
  - The consumer-price gain is equal per person within a quintile.
  - Unreimbursed care is equal per privately covered person. Premium increases fall largely on
    wages in practice. [INFERENCE]
  - The short-run capital gain is keyed by CPS interest, dividend and rent income. That misses
    retirement-account and business equity and top-coded amounts. [INFERENCE]
- **Stationary annual comparison.** The channel totals come with their own uncertainty, shown in
  the ranges. No dynamics.

## Covered / skipped

Covered:

- All six channels in the brief: wages, rents, crime victims' harm, fiscal (a) and (b),
  uncompensated care, and consumer prices as a side view.
- The owner value stock.
- η = 0, 1, 1.3, 2, plus 1.4.
- Per-person weights with p5 central and p1 and p10 sensitivities, plus p2 and p3 because p1 is
  degenerate.
- The brief's quintile-bin version, plus floored quintile and decile bins.
- Both income measures.
- The regressivity shares and per-household dollars.
- The primary documents on η, read.
- Extras:
  - median normalization;
  - equal-split equivalents;
  - A-4 treatment of intangible crime harm;
  - a CPS tax-field check key;
  - the published-band variant;
  - stacked ranges.

Skipped:

- **Replicate-weight standard errors.** Not computed. The key shares move less across the
  mapping variants than the channel totals move across their ranges. [INFERENCE] The archive
  holds 160 replicate weights if needed.
- **Property crime.** Outside the crime lane's scope.
- **Congestion.** Its lane (`congestion_2026_09_23`) was dispatched alongside this one, so there
  was no integrated total to take as given. A total can be added later as another per-person
  key.
- **Other nest dimensions.** Labor share, labor-supply elasticity, normalization, earnings proxy
  and nest option are held at the account's central. The brief asks only for splits, σ and ε.
- **Other housing arms.** The short-run arm and form B are not used. The brief names the long-run
  central and its range.
- **Group-median weights** (the Green Book's and A-4's group form). Per-person weights make the
  group statistic unnecessary; the median-normalized column carries their normalization.
- **A-4 *Explanation and Response to Public Input* (November 2023).** It documents the 1.4 value
  and was not read.

## Reproduce

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py
```

The first run reads the ACS PUMS ZIPs in chunks (about two minutes) and caches the needed columns
in `_cache/acs_extract.pkl`. Later runs take about 15 seconds and end with "212 gates passed". The
cached guidance and statistical documents in `_cache/sources/` are ignored; their hashes are in
`derived/sources_manifest.csv`.

## Revisions

2026-09-23: Connecticut planning regions (09110–09190) now map to 2013 CBSAs in the shared crosswalk; the housing lane's metro-local inputs moved (renters' extra rent −$33.86bn → −$33.86bn, landlords $37.36bn → $37.37bn, +$0.002bn each). The verdict's figures are unchanged at $0.1bn (bottom four fifths −$80.7bn, top fifth +$46.0bn, total −$262.6bn; at η = 1.3, −$407.1bn and −$738.3bn); the largest unweighted flow move is $0.003bn (renters, metro-local high). Four weighted-table cells change in their last printed digit: (b) η = 1 per person −557.0 → −557.1 (also in the headline η table), (a) η = 1.4 floored quintiles −419.9 → −420.0, (a) η = 2 quintile bins −781.0 → −781.1, and (b) η = 2 quintile bins −1,567.4 → −1,567.5. Owner-occupiers' top-fifth stock goes $815bn → $816bn, or $31,892 → $31,895 per household. Detail: [`CT_PLANNING_REGIONS.md`](../hedonic_composition_2026_09_19/CT_PLANNING_REGIONS.md).
