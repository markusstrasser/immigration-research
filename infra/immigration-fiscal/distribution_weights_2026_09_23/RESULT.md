**Verdict:** [2026-10-07: on main case v6 (`oct07`, $389.08–461.48bn: v5 plus the 2026 Trustees on separate funds,
retiree health on accrual, the added people at their measured ages, and user fees with the education keys),
`--case oct07` writes `derived/oct07/` beside `derived/oct05/`, which did not move. The fiscal channel is $417.10bn
(October 5: $417.58bn): cash $289.38bn, the return on public capital $48.82bn and the pension accrual $78.90bn
($287.70bn, $49.50bn, $80.38bn). Displaced beneficiaries carry $8.81bn ($8.81bn) and the wage channel −$1.65bn
(−$1.66bn); the central total is $460.80bn ($461.28bn), or $602.6bn at η = 1.3 mean-normalized ($603.3bn). Under tax
shares the bottom fifth carries $41.95bn ($41.99bn), 7.39% of its resources (7.40%); under per-person cuts, $112.73bn
($112.84bn). See "v6 case (oct07)" below.] [2026-10-05: on main case v5 (`oct05`, $390.29–461.24bn, which adds 3.04M descendants who no longer
report Mexican origin), `--case oct05` writes `derived/oct05/` beside `derived/sept29/`, which did not move. The fiscal
channel is $417.58bn (September 29: $395.71bn): cash $287.70bn, the return on public capital $49.50bn and the pension
accrual $80.38bn ($275.04bn, $45.80bn, $74.87bn). Displaced beneficiaries carry $8.81bn ($8.13bn) and the wage channel
−$1.66bn (−$1.61bn); the central total is $461.28bn ($438.67bn), or $603.3bn at η = 1.3 mean-normalized ($580.4bn).
Under tax shares the bottom fifth carries $41.99bn ($40.66bn), 7.40% of its resources (7.17%); under per-person cuts,
$112.84bn ($107.80bn). See "v5 case (oct05)" below.] [2026-09-27: the script now defaults to the main case of that day (`--case sept27`). The budget's fiscal channel is $351.0bn: cash financing $306.3bn plus the capital return's resource cost $44.7bn. Rental assistance and LIHEAP ($5.1bn) now fall on eligible households without the slots, $3.8bn of it on the bottom fifth. The central total with the social items is $390.8bn; the channels outside the budget do not move. `--case sept26_schools` reproduces 39b854b. See "The September 27 case" below.] [2026-09-26, later: the script now defaults to the main case with schools at full cost (`--case sept26_schools`). The fiscal channel is $276.7bn and the central total with the social items $311.4bn; the channels outside the budget do not move. `--case sept26` gives the one-year scenario ($224.8bn, $259.5bn). `--case sept24` and `--case sept23` with `--out-dir DIR` reproduce the runs described below.] [2026-09-25: the script now defaults to the main case adopted September 24: fiscal channel $225.1bn (text below: $227.9bn), central total $259.8bn (below: $262.6bn); the channels outside the budget do not move. `distribute.py --case sept23 --out-dir DIR` reproduces the run this text describes, byte for byte (`test_distribute.py`). See `../sept24_propagation_2026_09_24/RESULT.md`.] Relative to income, every channel except tax-financed fiscal cost falls hardest on
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

## Percentile table (2026-09-25)

`derived/channel_by_percentile.csv` gives the central channels and both totals in 100
person-weighted percentiles of other residents, on both rankings. It is for display (the figures
page's percentile curve). The run stops unless the percentiles nest in the quintiles and sum to
`channel_by_quintile.csv`. Every other derived file reran byte for byte, and `test_distribute.py`
still rebuilds the September 23 files.

On the September 24 case (SPM ranking), under tax-share financing every percentile loses: $449 to
$1,408 a person through the 99th percentile, and $12,658 in the top 1%. The top 1%'s fiscal share
is −$16,646, offset by housing (+$2,835) and wages (+$1,260). Under equal per-person cuts, the
bottom 60 percentiles lose $1,147 a person on average, and percentiles 95–100 come out ahead on
average (+$3,227 in the top 1%). These are averages within each percentile; ladder 226 counts
persons. Inputs published in bins keep their microdata key's shape inside each bin.
[CALCULATION: `distribute.py` → `derived/channel_by_percentile.csv`]

## The September 27 case (2026-09-27)

`--case sept27` moves A at each band end by the case's change, +$63.33bn / +$95.42bn (long-run road and park
responses, rental assistance at 1, government enterprises and the return on public capital); P and F do not
move. Run `node case_ends.cjs` first: at the case's end specifications (48 low, 11 high in both fill-in methods,
averaged) it writes the capital return and the capped programs' amounts to `derived/case_ends_sept27.json`,
gated to the case's `summary.json` (1e-9). The run ends with "261 gates passed".

**Three financing columns.** A no longer goes to the budget whole (audit §1, `research/immigration-conceptual-audit-2026-09-27.md`):

| $bn a year (negative = cost) | Low-cost end | High-cost end | Middle, distributed |
|---|---:|---:|---:|
| Cash financing (A + F, less the capital return and the capped programs) | −286.69 | −325.82 | −306.26 |
| Resource cost: return on public capital (federal part) | −33.80 (−0.83) | −55.69 (−1.74) | −44.74 |
| Displaced beneficiaries: rental assistance and LIHEAP | −5.09 | −5.09 | −5.09 |
| A + F | −325.59 | −386.60 | −356.09 |

The capital return is a cost of the budgets that hold the capital, so it is financed by each convention like the
cash part (`fiscal_cash_*`, `fiscal_resource_*`; `fiscal_*` is their sum). [CALCULATION: `derived/inputs.json`
`financing_columns`]

**Capped programs.** Rental assistance ($4.53bn) and LIHEAP ($0.56bn) are capped and rationed. Without the
group, eligible households who now go without would take its slots, so the amount falls on them, not on the
budget, under both conventions (`displaced_beneficiaries`, split by program in `displaced_housing_subsidies` and
`displaced_energy_assistance`). Each eligible non-recipient household with other residents bears an equal share
(household weight), split equally over its other-resident members. TANF-type aid (`family_and_general_assistance`,
$12.3bn / $11.7bn in A) is a block grant that states can move to other uses, so it stays with the conventions.

| Program | Proxy on the CPS ASEC 2025 household file | Rule it stands for | Eligible non-recipient households | Per household |
|---|---|---|---:|---:|
| Rental assistance | renter households paying cash rent (H_TENURE 2), money income below 50% of their state's median household money income (all households; state medians $55,500–113,820), neither in public housing (HPUBLIC) nor paying lower rent because a government pays part (HLORENT) | "very low income", 50% of the area's median family income adjusted for family size (24 CFR 5.603; vouchers, 982.201(b)) | 10.27m (18.6m other residents) | $441 |
| LIHEAP | households with money income below 150% of the 2024 HHS poverty guideline for their size ($15,060 + $5,380 per extra person; Alaska and Hawaii their own, 89 FR 2961), no energy assistance (HENGAST) | the greater of 150% of poverty and 60% of the state median income (42 U.S.C. 8624(b)(2)(B)) | 17.95m (38.2m) | $31 |

The account's rental key flags recipients with the same two survey items. The texts are cached in
`_cache/capped/` (ignored); their hashes are in `inputs.json`, and a gate finds each pinned figure in them.

The displaced beneficiaries sit at the bottom: Q1 −$3.83bn (0.67% of its resources), Q2 −$1.12bn, Q3 −$0.14bn,
Q4 and Q5 about 0. Financed by tax shares the same $5.09bn would have cost Q1 $0.15bn; by per-person cuts, $1.02bn.
At η = 1.3 the channel weighs −$28.0bn mean-normalized (equal split −$12.5bn).

| SPM quintiles, $bn a year | Total | Q1 | Q2 | Q3 | Q4 | Q5 | % of resources, Q1 / Q5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fiscal, (a) tax shares (schools case) | −351.00 (−276.72) | −10.64 | −22.44 | −37.84 | −62.05 | −218.03 | −1.88 / −4.06 |
| Fiscal, (b) per person | −351.00 (−276.72) | −70.20 | −70.20 | −70.20 | −70.20 | −70.20 | −12.37 / −1.31 |
| Displaced beneficiaries (new) | −5.09 | −3.83 | −1.12 | −0.14 | −0.00 | 0.00 | −0.67 / 0.00 |
| Central total, (a) | −390.80 (−311.42) | −37.31 | −47.11 | −60.08 | −74.29 | −172.01 | −6.58 / −3.21 |
| Central total, (b) | −390.80 (−311.42) | −96.87 | −94.86 | −92.44 | −82.44 | −24.18 | −17.07 / −0.45 |

At η = 1.3 the central total is −$531.7bn (a) and −$1,041.7bn (b) mean-normalized, −$237.6bn and −$465.5bn as
equal-split equivalents (schools case −$445.4bn, −$847.5bn, −$199.0bn, −$378.7bn). The range variants of the
fiscal channel carry the displaced beneficiaries at the same band end. [CALCULATION: `distribute.py` →
`derived/channel_by_quintile.csv`, `derived/weighted_totals.csv`, `derived/ranges_weighted.csv`]

Limits of the proxies: the rental proxy uses the state median household income without HUD's area medians and
family-size adjustment, and the LIHEAP proxy omits the 60%-of-state-median alternative, which widens eligibility
in higher-income states. Both programs target the poorest eligible households (75% of new voucher admissions
must be extremely low income, 24 CFR 982.201(b)(2); LIHEAP may prioritize the highest energy burdens), so the
loss probably falls lower than an equal share per eligible household [INFERENCE].

## v4 case (sept29), 2026-09-29

`--case sept29` runs the adopted v4 main case (`main_case_2026_09_29/`, commit 40c4ba7; $371.41–434.84bn at
specifications 48 / 11) and writes `derived/sept29/`, with the default's thirteen file names. Run
`node case_ends.cjs --case sept29` first; it writes `derived/case_ends_sept29.json`. The default stays the
September 27 case, and its files did not move. Run and gated 17:17–17:25 JST (log file times; `date` 17:23 JST).
The run ends with "291 gates passed". Code: `case_ends.cjs`, `distribute.py`, `test_distribute.py`.

**Three rules the case needed.** Each is designed here, with its alternative.

1. *Production moves wages and F, never A.* v4 solves the production model again on the account's row-4 weights
   (payload item 2). That moves P + F by −1.64bn at the low end and −1.11bn at the high end, and leaves A alone.
   Every earlier case moved A by the whole change in the band, which was right only because P and F stayed fixed.
   Here A moves by the case's change less the engine's change in P + F, and this lane's production scenarios are
   solved again on row-4 weights (`row4_nest_rows`). Their P goes to the wage channel and their F to the fiscal
   channel. Gates:
   - A equals the engine's A at both ends (|diff| 4.9e-5 and 3.4e-5; the gate's tolerance is 1e-3).
   - The re-solved scenarios equal the case's grid at their cells (5.0e-10bn).
   - The same solve on the published weights reproduces the nest file (3.7e-12bn).

   Alternative: book the change in A, as before. A would then miss the engine's by 1.64bn and 1.11bn, and the wage
   channel would stay on the published weights: −$1.47bn central instead of −$1.61bn.
2. *Public housing is a capped program.* v4 splits public housing's enterprise deficit out of the enterprise
   surplus. The new receipt line, `housing_enterprise_surplus`, uses rental assistance's key at response 1 and costs
   $3.43bn for the group. Public housing is rationed like vouchers: a fixed stock of units with waiting lists. So
   without the group, eligible households who now go without would take those units [INFERENCE]. The amount
   therefore falls on rental assistance's eligible non-recipients, not on the budget:
   `displaced_housing_enterprise_surplus`, inside `displaced_beneficiaries`. `case_ends.cjs` gates that this capped
   cost equals the case's receipt effect: 3.4261bn at both ends, to 1e-9.

   Alternative: leave it in the budget under both conventions, as the enterprise surplus line was before. Q1 would
   then carry 3.0% of it under tax shares, instead of 72.7% as a displaced loss. Limit: rental assistance's proxy
   (very low income) is narrower than public housing's low-income eligibility.
3. *The pension accrual stays in the fiscal channel and is reported apart.* The case charges the accrual of the
   pension switch, the case less its cash set: $76.71bn and $73.02bn at the band ends. This lane distributes the
   whole fiscal channel over today's residents under both conventions, and never splits off the borrowed part (the
   winners lane does). So the accrual is distributed like the rest and reported alone, in `fiscal_accrual_*`, beside
   `fiscal_cash_*` and `fiscal_resource_*`: fiscal = cash + resource + accrual.

   Alternative: leave it out of today's distribution, as a claim that future taxpayers pay (the winners lane's
   rule). Dropping `fiscal_accrual_a` gives that reading directly.

Rental assistance falls to $4.14bn (September 27: $4.53bn). v4 item 1 moves public housing's $5.258bn operating
subsidy out of the national line, which drops from $60.261bn to $55.003bn. LIHEAP stays at $0.56bn.

**Four financing columns.** One decimal, so the parts add.

| $bn a year (negative = cost) | Low-cost end | High-cost end | Middle, distributed |
|---|---:|---:|---:|
| Cash financing: A + F, less the capital return, the accrual and the capped programs | −254.9 | −295.2 | −275.0 |
| Resource cost: return on public capital (federal part) | −34.4 (−0.8) | −57.2 (−1.8) | −45.8 |
| Pension accrual | −76.7 | −73.0 | −74.9 |
| Displaced beneficiaries: rental assistance, LIHEAP, public housing | −8.1 | −8.1 | −8.1 |
| A + F | −374.1 | −433.5 | −403.8 |

[CALCULATION: `derived/sept29/inputs.json` `financing_columns`]

| SPM quintiles, $bn a year | Total (Sept 27) | Q1 | Q2 | Q3 | Q4 | Q5 | % of resources, Q1 / Q5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fiscal, (a) tax shares | −395.71 (−351.00) | −12.00 | −25.31 | −42.66 | −69.95 | −245.79 | −2.11 / −4.58 |
| of which cash | −275.04 (−306.26) | −8.34 | −17.59 | −29.65 | −48.62 | −170.84 | −1.47 / −3.18 |
| of which return on public capital | −45.80 (−44.74) | −1.39 | −2.93 | −4.94 | −8.09 | −28.45 | −0.24 / −0.53 |
| of which pension accrual | −74.87 | −2.27 | −4.79 | −8.07 | −13.24 | −46.50 | −0.40 / −0.87 |
| Fiscal, (b) per person | −395.71 (−351.00) | −79.15 | −79.14 | −79.14 | −79.14 | −79.14 | −13.95 / −1.47 |
| Displaced beneficiaries | −8.13 (−5.09) | −6.03 | −1.86 | −0.24 | −0.00 | 0.00 | −1.06 / 0.00 |
| of which public housing | −3.43 | −2.49 | −0.83 | −0.11 | 0.00 | 0.00 | −0.44 / 0.00 |
| Central total, (a) | −438.67 (−390.80) | −40.66 | −50.22 | −64.48 | −82.05 | −201.26 | −7.17 / −3.75 |
| Central total, (b) | −438.67 (−390.80) | −107.80 | −104.05 | −100.97 | −91.24 | −34.61 | −19.00 / −0.64 |

Five quintile cells are rounded under control, one cent at most, so each row adds: fiscal (a) Q2, capital return Q4,
fiscal (b) Q1, central total (a) Q3 and central total (b) Q1. Financed by tax shares, the $8.13bn of displaced
beneficiaries would have cost Q1 $0.25bn; by per-person cuts, $1.63bn. At η = 1.3 the central total is −$580.4bn (a)
and −$1,155.3bn (b) mean-normalized, or −$259.3bn and −$516.3bn as equal-split equivalents. For September 27 those
were −$531.7bn, −$1,041.7bn, −$237.6bn and −$465.5bn. The displaced beneficiaries weigh −$44.2bn mean-normalized
(equal split −$19.8bn). Renters (−$33.86bn), landlords (+$37.37bn) and crime (−$32.34bn) do not depend on the case
and did not move; wages moved with the production rule. [CALCULATION: `distribute.py --case sept29` →
`derived/sept29/channel_by_quintile.csv`, `weighted_totals.csv`]

**Why this lane's fiscal channel differs from the winners lane's.** Both lanes take A at each band end from
`fiscal_totals` (one definition), and both move the capped programs out. They differ only in the induced receipts F
they add:
- This lane adds the F of its central production scenario, which is also the scenario its wage channel uses:
  below-BA split, σ = 2, capital adjusting, cash normalization.
- The winners lane adds the engine's F at the band's end specifications, averaged over the two ends: the
  high-school split, normalized to GDP at 48 and to cash at 11.

| $bn a year, central (one decimal, so the parts add) | Sept 27 | sept29 |
|---|---:|---:|
| Case, middle of the band | 354.6 | 403.1 |
| less the private production term at the ends, −P | −0.2 | −0.6 |
| less the capped programs (displaced beneficiaries) | −5.1 | −8.1 |
| = winners lane: taxpayers' fiscal channel, A + F at the band ends | 349.3 | 394.4 |
| plus the engine's F less this lane's (11.25 − 9.56; 10.26 − 8.98) | +1.7 | +1.3 |
| = this lane: fiscal channel, A + F of its central scenario | 351.0 | 395.7 |

Both levels include the return on public capital: $44.7bn for September 27 and $45.8bn for sept29. Both exclude
the capped programs, $5.09bn and $8.13bn, which sit beside them. For sept29, both include the pension accrual,
$74.9bn. The winners lane assigns the accrual to future taxpayers; this lane reports it apart.

The unrounded bridge is exact. The difference is 1.6966bn on September 27 and 1.2787bn on sept29, equal to the
engine's F less this lane's to 1e-4. It reproduces the winners file's September 27 figure,
`winners_losers_2026_09_24/derived/inputs.json` fiscal.central: cost 354.3989 less displaced 5.0944 = 349.3045. The sept29 figure is the
same construction on this run's A and the adopted lane's grid at the ends; the winners run will confirm it.

The two levels should be quoted as one number, the winners lane's. It uses the case's own production term, so the
fiscal channel, the capped programs and the private production term add to the band's middle. This lane's F pairs
the fiscal channel with its wage scenario. That pairing matters inside this lane's totals but not for the channel's
level. Each convention allocates the total on a fixed key, so this lane's quintile shares apply unchanged to the
winners level. This lane's printed levels stay as run.
[CALCULATION: `derived/inputs.json` and `derived/sept29/inputs.json` (A, capped programs, production central_F),
`derived/case_ends_sept29.json` production ends (the engine's P and F at 48 / 11), and
`winners_losers_2026_09_24/derived/fiscal_specs.csv` for September 27's]

**Gates.**

| Gate | Result |
|---|---|
| 1. Existing outputs reproduce | `rerun_lane.py` with the four commands below: IDENTICAL, 33 of 33 files (19 tracked, 14 new); the tracked files equal HEAD |
| 2. sept29 outputs exist and the lane's gates pass | `derived/case_ends_sept29.json` and `derived/sept29/` (13 files); 291 gates; `pytest` 8 passed, including the sept29 rebuild |
| 3. Oracle | `case_ends_sept29.json` cost 371.4145998 / 434.8409586, against the oracle's 371.4146 / 434.8410. Less the accrual it gives 294.7010760 / 361.8174818, against 294.7011 / 361.8175. Tolerance 1e-4, the oracle's rounding; the lane itself gates the band to `summary.json` at 1e-9. A at 48 / 11 is −383.094429 / −442.524231, against the world ledger's cross-check of −383.0945 / −442.5242 (1e-4) |
| 4. Two passes after the sept29 run | both IDENTICAL, 33 of 33 |

```sh
node infra/immigration-fiscal/distribution_weights_2026_09_23/case_ends.cjs --case sept29
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py --case sept29
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/distribution_weights_2026_09_23 \
  "node {lane}/case_ends.cjs" "node {lane}/case_ends.cjs --case sept29" \
  "uv run --no-project python3 {lane}/distribute.py" "uv run --no-project python3 {lane}/distribute.py --case sept29" \
  --allow-unrun infra/immigration-fiscal/distribution_weights_2026_09_23/test_distribute.py
```

## v5 case (oct05), 2026-10-05

`--case oct05` runs the adopted v5 main case (`main_case_2026_10_05/`, adopted in 4bf02069; $390.29–461.24bn at
specifications 48 / 11) and writes `derived/oct05/`, with the default's thirteen file names. Run
`node case_ends.cjs --case oct05` first; it writes `derived/case_ends_oct05.json`. The default (September 27) and
`derived/sept29/` did not move. The run ends with "303 gates passed". Code: `case_ends.cjs`, `distribute.py`,
`test_distribute.py`.

v5 is v4 plus 3,039,720 people: descendants of Mexican immigrants who no longer report Mexican origin, counted whole
at G3+ members' and third-plus whites' amounts (`../main_case_lineage_2026_10_05/`). The case's consumer table asks
this lane to split the change into A and P + F as for the union, with the lineage's production delta belonging to
the added G3+ members.

**Four rules the case needed.**

1. *A moves by the change less the lineage's production delta.* v5's production grid is v4's plus the added G3+
   members' P and F; the added whites carry none. At the band's end cells that raises P + F by $0.2676bn (low) and
   $0.1760bn (high). A falls by the change in the band plus that delta, 18.8794 + 0.2676 = 19.1470 and
   26.4022 + 0.1760 = 26.5782, so A goes from −383.0944 / −442.5242 to −402.2414 / −469.1024. `case_ends.cjs` reads v4's grid at the same cell
   (`previous`); `distribute.py` gates that it is v4's own P and F at its ends, exactly. Gate: A equals the engine's
   A at both ends (|diff| 4.9e-5 and 3.4e-5; tolerance 1e-3).

   Alternative: book the whole change in A, as before September 29. A would miss the engine's by 0.27bn and 0.18bn.
2. *The lane's production scenarios take the lineage's delta.* They are solved on row-4 weights as for v4, gated
   against v4's grid (5.0e-10bn). Each scenario's wage changes in skill cell c are then scaled by λ_c and its capital
   columns by κ, so that its P and F equal v5's grid at its cell [ASSUMPTION: the added members' wage effects fall
   on other residents' skill cells as the union's do]. With capital adjusting there are no capital terms, and the
   unknowns are λ_0 and λ_1. With capital fixed there is one λ for both cells, plus κ. The σ_NI = 3 scenarios
   take their σ_NI-infinite sibling's factors.

   The factors are λ = 1.0336 in both cells for the below-BA split and 1.0222 / 1.0223 for high school or less. The
   capital-fixed scenario takes λ = 1.0467 and κ = 1.0464. Gates:
   - the parts reproduce each scenario (2.3e-13bn);
   - the scenarios start from v4's grid (4.7e-10bn) and reach v5's (2.9e-14bn);
   - every factor is within 10% of 1 (largest deviation 0.0467).

   The central scenario's P goes from −1.609 to −1.662 and its F from 8.979 to 9.282. The wage channel is −$1.66bn
   (v4: −$1.61bn).

   Alternative: leave the scenarios on v4's grid. Their P and F would then not be the case's at their cells, and
   the wage channel would stay at −$1.61bn.
3. *The pension accrual is the case less its cash set, read from the cash set.* v5's summary has no `item_pension`.
   `case_ends.cjs` therefore takes the accrual as −`cash_set.change_from_main_case_bn` at the case's end
   specifications, and gates that the cash set's band is the case's plus that change (1e-9). The definition is v4's:
   $82.92bn and $77.83bn at the band ends (v4: $76.71bn and $73.02bn).
4. *The added people stay among the payers.* They do not report Mexican origin, so the CPS frame holds them as
   natives among the 295.83M other residents. The lane cannot find them and leaves them there [ASSUMPTION: about
   3.04M of the frame's other residents, 1.03%, are the added people]. Under per-person financing (b) they carry
   1.03% of the fiscal channel, $4.29bn of $417.58bn [CALCULATION: 417.5785 × 3,039,719.6 / 295,831,228.8]. Under
   tax shares (a), their part depends on incomes the frame cannot attach to them.

The capped programs rise with the added people's use, to $8.81bn (v4: $8.13bn). Rental assistance is $4.49bn, LIHEAP
$0.61bn and public housing $3.72bn (v4: $4.14bn, $0.56bn, $3.43bn).

**Four financing columns.** One decimal, so the parts add; the low end's resource cost (−37.1478) is rounded under
control.

| $bn a year (negative = cost) | Low-cost end | High-cost end | Middle, distributed | sept29 middle |
|---|---:|---:|---:|---:|
| Cash financing: A + F, less the capital return, the accrual and the capped programs | −264.1 | −311.3 | −287.7 | −275.0 |
| Resource cost: return on public capital (federal part) | −37.2 (−0.9) | −61.9 (−1.9) | −49.5 | −45.8 |
| Pension accrual | −82.9 | −77.8 | −80.4 | −74.9 |
| Displaced beneficiaries: rental assistance, LIHEAP, public housing | −8.8 | −8.8 | −8.8 | −8.1 |
| A + F | −393.0 | −459.8 | −426.4 | −403.8 |

[CALCULATION: `derived/oct05/inputs.json` `financing_columns`; sept29's ends are in the v4 table above]

| SPM quintiles, $bn a year | Total (sept29) | Q1 | Q2 | Q3 | Q4 | Q5 | % of resources, Q1 / Q5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fiscal, (a) tax shares | −417.58 (−395.71) | −12.66 | −26.70 | −45.02 | −73.82 | −259.38 | −2.23 / −4.83 |
| of which cash | −287.70 (−275.04) | −8.72 | −18.40 | −31.01 | −50.86 | −178.71 | −1.54 / −3.33 |
| of which return on public capital | −49.50 (−45.80) | −1.50 | −3.16 | −5.34 | −8.75 | −30.75 | −0.26 / −0.57 |
| of which pension accrual | −80.38 (−74.87) | −2.44 | −5.14 | −8.67 | −14.21 | −49.92 | −0.43 / −0.93 |
| Fiscal, (b) per person | −417.58 (−395.71) | −83.52 | −83.51 | −83.52 | −83.52 | −83.51 | −14.72 / −1.56 |
| Displaced beneficiaries | −8.81 (−8.13) | −6.54 | −2.01 | −0.26 | −0.00 | 0.00 | −1.15 / 0.00 |
| of which public housing | −3.72 (−3.43) | −2.70 | −0.90 | −0.12 | 0.00 | 0.00 | −0.48 / 0.00 |
| Central total, (a) | −461.28 (−438.67) | −41.99 | −52.13 | −67.24 | −86.05 | −213.87 | −7.40 / −3.99 |
| Central total, (b) | −461.28 (−438.67) | −112.84 | −108.94 | −105.74 | −95.75 | −38.01 | −19.89 / −0.71 |

Four quintile cells are rounded under control, one cent at most, so each row adds and the three parts add to the
fiscal row: the capital return's Q2, the accrual's Q3 and Q5, and fiscal (b) Q5. The same procedure on
`derived/sept29/` reproduces the v4 table's five controlled cells. Financed by tax shares, the $8.81bn of displaced
beneficiaries would have cost Q1 $0.27bn; by per-person cuts, $1.76bn (v4: $0.25bn and $1.63bn).

At η = 1.3 the central total is −$603.3bn (a) and −$1,210.0bn (b) mean-normalized, or −$269.6bn and −$540.7bn as
equal-split equivalents. For v4 those were −$580.4bn, −$1,155.3bn, −$259.3bn and −$516.3bn. The displaced
beneficiaries weigh −$47.9bn mean-normalized (equal split −$21.4bn; v4 −$44.2bn and −$19.8bn).

The central total moves by −$22.61bn: fiscal −$21.87bn, displaced beneficiaries −$0.69bn and wages −$0.05bn. Renters
(−$33.86bn), landlords (+$37.37bn), crime (−$32.34bn), unreimbursed care and the published-band channels do not
depend on the case and did not move. [CALCULATION: `distribute.py --case oct05` → `derived/oct05/channel_by_quintile.csv`,
`weighted_totals.csv`; every channel's total compared with `derived/sept29/`]

**Bridge to the winners lane's level.** This is the v4 construction on this run's A and v5's grid at the band ends.

| $bn a year, central (one decimal, so the parts add) | sept29 | oct05 |
|---|---:|---:|
| Case, middle of the band | 403.1 | 425.8 |
| less the private production term at the ends, −P | −0.6 | −0.6 |
| less the capped programs (displaced beneficiaries) | −8.1 | −8.8 |
| = winners lane: taxpayers' fiscal channel, A + F at the band ends | 394.4 | 416.4 |
| plus the engine's F less this lane's (10.26 − 8.98; 10.49 − 9.28) | +1.3 | +1.2 |
| = this lane: fiscal channel, A + F of its central scenario | 395.7 | 417.6 |

The unrounded difference is 1.2069bn, the engine's F less this lane's to 7.6e-6, as on v4. The winners run on v5 will
confirm the oct05 level.

**Gates.**

| Gate | Result |
|---|---|
| 1. Existing outputs reproduce | `rerun_lane.py` with the seven commands below: IDENTICAL, 47 of 47 files, exit 0. The tracked files, the default's and `derived/sept29/`, equal HEAD |
| 2. The lane's gates on oct05 | 303 pass (sept29: 291). The twelve new ones: v5's base is the adopted sept29; the summary's band is `main_case_bands.csv`'s; the change is the summary's; the band is rebuilt from A; the case ends are the band; the previous grid is sept29's at both ends; A is the engine's; and the four `lineage_rows` gates |
| 3. Oracle | `case_ends_oct05.json` band 390.2939582 / 461.2431247 against the case's 390.2940 / 461.2431. Less the accrual it gives 307.3763762 / 383.4092521, against the cash set's 307.3764 / 383.4093 |
| 4. `pytest` | 10 passed: the sept23–sept26 rebuilds, `case_ends` for sept27, sept29 and oct05, the default, and the sept29 and oct05 directories |
| 5. JSON | `derived/oct05/inputs.json` parses in Node. The first run wrote infinite σ_NI as `Infinity`; it is now `"inf"`, as `nest_scenarios.csv` writes it |

```sh
node infra/immigration-fiscal/distribution_weights_2026_09_23/case_ends.cjs --case oct05
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py --case oct05
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/distribution_weights_2026_09_23 \
  "node {lane}/case_ends.cjs" "node {lane}/case_ends.cjs --case sept29" "node {lane}/case_ends.cjs --case oct05" \
  "uv run --no-project python3 {lane}/distribute.py" "uv run --no-project python3 {lane}/distribute.py --case sept29" \
  "uv run --no-project python3 {lane}/distribute.py --case oct05" \
  "uv run --no-project python3 -m pytest {lane}/test_distribute.py -q --import-mode=importlib -p no:cacheprovider"
```

Log, 2026-10-06 JST, times from `date`:
- 00:14:39–00:17:29: first rerun, IDENTICAL 47 of 47 but exit 3. Its pytest command named the directory, so
  `test_distribute.py` showed as NOT RUN.
- 00:18:35–00:18:54: `--case oct05` again after the σ_NI fix; 303 gates. Only `inputs.json` changed, at its seven
  σ_NI tokens.
- 00:19:13–00:21:13: `pytest`, 10 passed in 120 s.
- 00:21:22–00:24:11: the rerun above, IDENTICAL, exit 0.

## v6 case (oct07), 2026-10-07

`--case oct07` runs main case v6 (`main_case_2026_10_07/`, built in 218a2fb2 and adopted in 025203f4; $389.08–461.48bn
at specifications 48 / 11) and writes `derived/oct07/`, with the default's thirteen file names. Run
`node case_ends.cjs --case oct07` first; it writes `derived/case_ends_oct07.json`. The default (September 27),
`derived/sept29/` and `derived/oct05/` did not move. The run ends with "311 gates passed". Code: `case_ends.cjs`,
`distribute.py`, `test_distribute.py` (498a6a71).

v6 is v5 plus four items (the payload's `meta.items`): the pension accrual on the 2026 Trustees' separate funds (set
only), retiree health on accrual (the national totals of ten lines, both sets), the 3.04M added people at their
measured age mix (the lineage's edits and production grid replaced in place), and user fees with the education keys
(cell shifts on the union's cells of five lines and four capital offsets, both sets). The case lane's consumer table
called this lane a path swap in which the items move A only. That holds for three of the four; the age mix also
changes the grid.

**Five rules the case needed.**

1. *A moves by the change in the band less the grid's change.* The age mix re-values the added G3+ members' P and F,
   so v6's grid differs from v5's at the band ends' cells: P + F falls by $0.0378bn (low) and $0.0249bn (high). Since
   cost = −(P + F) − A, A rises by 1.2114 + 0.0378 = 1.2492 at the low end, where the band falls by 1.2114, and falls
   by 0.2366 − 0.0249 = 0.2117 at the high end, where the band rises by 0.2366. A goes from −402.2414 / −469.1024 to
   −400.9922 / −469.3141 (the engine's A; this lane's rebuild is within 4.9e-5 and 3.4e-5). `case_ends.cjs` reads v5's
   grid at the same cell (`previous`, `PREVIOUS_GRID`), and `distribute.py` gates that it is v5's own P and F at its
   ends, exactly (`Case.prev_grid`). Gate: A equals the engine's at both ends (tolerance 1e-3).

   Alternative: book the whole change in A, which is right for the three items that leave the grid alone. A would be
   −401.0300 / −469.3390 and miss the engine's by 0.038 and 0.025bn, so the engine-A gate would fail.
2. *The lane's production scenarios take v6's lineage delta.* They are solved on row-4 weights against September 29's
   grid, as for v5, and `lineage_rows` scales them to v6's grid [ASSUMPTION, v5's: the added members' wage effects
   fall on other residents' skill cells as the union's do]. v6's lineage delta in P and F is smaller than v5's, so the
   factors are closer to 1: λ is 1.0288 / 1.0289 below BA (v5 1.0336) and 1.0191 for high school or less (v5 1.0222 /
   1.0223). With capital fixed, λ is 1.0401 and κ 1.0398 (v5 1.0467, 1.0464). Gates:
   - the parts reproduce each scenario (2.3e-13bn);
   - the scenarios start from September 29's grid (4.7e-10bn) and reach v6's (3.6e-14bn);
   - every factor is within 10% of 1 (largest deviation 0.0401).

   The central scenario's P is −1.655 (v5 −1.662) and its F 9.239 (9.282). The wage channel is −$1.65bn (v5
   −$1.66bn).
3. *The pension accrual is the case less its cash set*, read from `cash_set.change_from_main_case_bn` as for v5:
   $81.68bn and $76.12bn at the band ends (v5: $82.92bn and $77.83bn). On v5 alone, item 1 lowers it by $2.85 / 2.67bn
   (it moves the set only) and the age mix raises it by $1.61 / 0.94bn (it moves the set more than the cash set).
   Retiree health and user fees move both sets alike.
4. *Retiree health and user fees reach this lane through A and the capital return only.* Their edits are on keyed
   spending lines, and the user fees' capital offsets are components of `meta.capital_return`. So the engine's lines,
   the case ends' capital return (gated equal to `summary.json`'s by level, 1e-9) and the financing columns carry them
   with nothing added here. The resource cost falls by $0.57 / 0.79bn. The user-fee offsets, which re-key the college
   and K-12 stocks by use, lower it by $0.63 / 1.00bn; the younger age mix raises it by $0.06 / 0.21bn; items 1 and 2
   move it by $0.0002bn or less [CALCULATION: `package.cjs` `caseOf(OCT05, …)` with the items added in registry
   order, the capital return at v6's end specifications; a one-off check, not a lane output].
5. *The added people stay among the payers* [ASSUMPTION, v5's rule 4]. The age mix changes what the case charges for
   them, but they still do not report Mexican origin, and the CPS frame holds them unfound among the 295.83M other
   residents. Under per-person financing (b) they carry $4.29bn of $417.10bn [CALCULATION: 417.1030 × 3,039,719.6 /
   295,831,228.8].

The capped programs barely move: $8.81bn (v5 $8.81bn), of which rental assistance $4.49bn, LIHEAP $0.60bn and public
housing $3.72bn.

**Four financing columns.** One decimal, so the parts add; no cell needs controlled rounding.

| $bn a year (negative = cost) | Low-cost end | High-cost end | Middle, distributed | oct05 middle |
|---|---:|---:|---:|---:|
| Cash financing: A + F, less the capital return, the accrual and the capped programs | −264.7 | −314.1 | −289.4 | −287.7 |
| Resource cost: return on public capital (federal part) | −36.6 (−0.9) | −61.1 (−1.9) | −48.8 | −49.5 |
| Pension accrual | −81.7 | −76.1 | −78.9 | −80.4 |
| Displaced beneficiaries: rental assistance, LIHEAP, public housing | −8.8 | −8.8 | −8.8 | −8.8 |
| A + F | −391.8 | −460.1 | −425.9 | −426.4 |

[CALCULATION: `derived/oct07/inputs.json` `financing_columns`; oct05's ends are in the v5 table above]

| SPM quintiles, $bn a year | Total (oct05) | Q1 | Q2 | Q3 | Q4 | Q5 | % of resources, Q1 / Q5 |
|---|---:|---:|---:|---:|---:|---:|---:|
| Fiscal, (a) tax shares | −417.10 (−417.58) | −12.64 | −26.67 | −44.96 | −73.74 | −259.09 | −2.23 / −4.83 |
| of which cash | −289.38 (−287.70) | −8.77 | −18.50 | −31.20 | −51.16 | −179.75 | −1.55 / −3.35 |
| of which return on public capital | −48.82 (−49.50) | −1.48 | −3.12 | −5.26 | −8.63 | −30.33 | −0.26 / −0.57 |
| of which pension accrual | −78.90 (−80.38) | −2.39 | −5.05 | −8.50 | −13.95 | −49.01 | −0.42 / −0.91 |
| Fiscal, (b) per person | −417.10 (−417.58) | −83.42 | −83.42 | −83.42 | −83.42 | −83.42 | −14.70 / −1.55 |
| Displaced beneficiaries | −8.81 (−8.81) | −6.54 | −2.01 | −0.26 | −0.00 | 0.00 | −1.15 / 0.00 |
| of which public housing | −3.72 (−3.72) | −2.70 | −0.90 | −0.12 | 0.00 | 0.00 | −0.48 / 0.00 |
| Central total, (a) | −460.80 (−461.28) | −41.95 | −52.05 | −67.14 | −85.95 | −213.71 | −7.39 / −3.98 |
| Central total, (b) | −460.80 (−461.28) | −112.73 | −108.79 | −105.60 | −95.63 | −38.05 | −19.87 / −0.71 |

Six quintile cells are rounded under control, one cent at most, so each row adds and the three parts add to the fiscal
row: fiscal (a)'s Q1 and Q5, the accrual's Q3, displaced beneficiaries' Q2, and the central totals' (a) Q5 and (b)
Q3. The procedure departs from ordinary rounding in as few cells as it can, ties going to the cells nearest their exact
values; on `derived/oct05/` it reproduces the v5 table and its four controlled cells. Financed by tax shares, the
$8.81bn of displaced beneficiaries would have cost Q1 $0.27bn; by per-person cuts, $1.76bn (v5: the same).

At η = 1.3 the central total is −$602.6bn (a) and −$1,208.6bn (b) mean-normalized, or −$269.3bn and −$540.1bn as
equal-split equivalents. For v5 those were −$603.3bn, −$1,210.0bn, −$269.6bn and −$540.7bn. The displaced
beneficiaries weigh −$47.9bn mean-normalized (equal split −$21.4bn), as on v5.

The central total moves by +$0.4834bn: fiscal +$0.4755bn (cash −$1.6808bn, the capital return +$0.6799bn, the accrual
+$1.4764bn), wages +$0.0074bn and displaced beneficiaries +$0.0005bn. Renters, landlords, crime, unreimbursed care and
the published-band channels do not depend on the case and did not move. [CALCULATION: `distribute.py --case oct07` →
`derived/oct07/channel_by_quintile.csv`, `weighted_totals.csv`; every channel's total compared with `derived/oct05/`]

**Bridge to the winners lane's level.** This is v5's construction on this run's A and v6's grid at the band ends.

| $bn a year, central (one decimal, so the parts add) | oct05 | oct07 |
|---|---:|---:|
| Case, middle of the band | 425.8 | 425.3 |
| less the private production term at the ends, −P | −0.6 | −0.6 |
| less the capped programs (displaced beneficiaries) | −8.8 | −8.8 |
| = winners lane: taxpayers' fiscal channel, A + F at the band ends | 416.4 | 415.9 |
| plus the engine's F less this lane's (10.49 − 9.28; 10.46 − 9.24) | +1.2 | +1.2 |
| = this lane: fiscal channel, A + F of its central scenario | 417.6 | 417.1 |

The unrounded difference is 1.2170bn, the engine's F less this lane's to 7.6e-6, as on v5. The winners run on v6 will
confirm the oct07 level.

**Gates.**

| Gate | Result |
|---|---|
| 1. Existing outputs reproduce | `rerun_lane.py` with the nine commands below: IDENTICAL, 61 of 61 files, exit 0. The tracked files, the default's, `derived/sept29/` and `derived/oct05/`, equal HEAD |
| 2. The lane's gates on oct07 | 311 pass (oct05: 303). The eight new ones: v6's base is the adopted oct05; the summary's band is `main_case_bands.csv`'s; the change is the summary's; the band is rebuilt from A; the case ends are the band; the previous grid is oct05's at both ends; and A is the engine's |
| 3. Oracle | `case_ends_oct07.json` band 389.0825529 / 461.4797093 against the case's 389.082553 / 461.479709. Less the accrual it gives 307.3994105 / 385.3641225, against the cash set's 307.399411 / 385.364123 |
| 4. `pytest` | 12 passed: the sept23–sept26 rebuilds, `case_ends` for sept27, sept29, oct05 and oct07, the default, and the sept29, oct05 and oct07 directories |
| 5. At HEAD | After the case lane's pinning commit (1548b396, no payload change), runs at 826a87dd to a scratch `--out-dir` reproduced `case_ends_oct07.json` and all thirteen `derived/oct07/` files byte for byte |

```sh
node infra/immigration-fiscal/distribution_weights_2026_09_23/case_ends.cjs --case oct07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/distribution_weights_2026_09_23/distribute.py --case oct07
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/distribution_weights_2026_09_23 \
  "node {lane}/case_ends.cjs" "node {lane}/case_ends.cjs --case sept29" "node {lane}/case_ends.cjs --case oct05" \
  "node {lane}/case_ends.cjs --case oct07" \
  "uv run --no-project python3 {lane}/distribute.py" "uv run --no-project python3 {lane}/distribute.py --case sept29" \
  "uv run --no-project python3 {lane}/distribute.py --case oct05" "uv run --no-project python3 {lane}/distribute.py --case oct07" \
  "uv run --no-project python3 -m pytest {lane}/test_distribute.py -q --import-mode=importlib -p no:cacheprovider"
```

Log, 2026-10-07 JST, times from `date`:
- 13:03: `--case oct07` coded; dev runs on the three-item candidate pass.
- 13:27 and 13:31: `case_ends_oct07.json` regenerated on the four-item case as the case lane rewrote its files (dev).
- 14:59:35–14:59:37: `case_ends.cjs --case oct07` in place on 218a2fb2's outputs: 14 gates.
- 14:59:41–15:00:16: `distribute.py --case oct07` in place: 311 gates.
- 15:00:32–15:04:54: the rerun above, IDENTICAL 61 of 61, exit 0.
- 15:05:15–15:07:49: `pytest`, 12 passed in 154 s.
- 15:14:43–15:15:59: the check at HEAD (gate 5).

## Revisions

2026-09-23: Connecticut planning regions (09110–09190) now map to 2013 CBSAs in the shared crosswalk; the housing lane's metro-local inputs moved (renters' extra rent −$33.86bn → −$33.86bn, landlords $37.36bn → $37.37bn, +$0.002bn each). The verdict's figures are unchanged at $0.1bn (bottom four fifths −$80.7bn, top fifth +$46.0bn, total −$262.6bn; at η = 1.3, −$407.1bn and −$738.3bn); the largest unweighted flow move is $0.003bn (renters, metro-local high). Four weighted-table cells change in their last printed digit: (b) η = 1 per person −557.0 → −557.1 (also in the headline η table), (a) η = 1.4 floored quintiles −419.9 → −420.0, (a) η = 2 quintile bins −781.0 → −781.1, and (b) η = 2 quintile bins −1,567.4 → −1,567.5. Owner-occupiers' top-fifth stock goes $815bn → $816bn, or $31,892 → $31,895 per household. Detail: [`CT_PLANNING_REGIONS.md`](../hedonic_composition_2026_09_19/CT_PLANNING_REGIONS.md).
