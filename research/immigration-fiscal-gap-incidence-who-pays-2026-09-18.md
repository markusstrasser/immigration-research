claude-opus-5[1m]

**Verdict:** The complete resident account's Mexican-origin balance of −$263.22bn is overwhelmingly a **state-and-local** deficit, not a federal one: −$235.10bn of it (89%) is charged by states, counties, school districts and municipalities, and only −$28.12bn (11%) by Washington. Spread over the 117.20m native-headed households the annual figure is **$2,246 per household** under average financing and **$2,014** under marginal financing, where only the federal tenth is borrowed and only its interest falls due. It is **regressive as a share of income** — 7.39% of the bottom native decile's resources against 2.57% of the top decile's — because state-local revenue is mostly property, sales and user charges. In California it is **$8,498 per native household**, in Texas **$5,177**. The property-tax pass-through arm the brief asks about moves nothing: total unchanged, renters ±$149, owners ∓$73. What moves the answer is item F. And the control settles the interpretive question: the financing share vector is **identical for every group**, so the same matrix applied to the third-plus non-Hispanic white reference's own −$390.75bn gives **$3,334 per native household, 48% more**. Nothing in the distribution is about Mexican-origin residents. Only the scalar is.

[SOURCE: `infra/immigration-fiscal/gap_incidence_2026_09_18/` — `incidence.py`, `RESULT.md`, `derived/`, `derived_F_percapita/`]
[DATA: CPS ASEC 2025 public-use file, income year 2024, 142,125 person records, 58,147 SPM units; MEPS HC-256 2024; 2022 Census of Governments Table 1; OMB Historical Tables FY2027 edition; BLS CEX 2024 Table 1101; US Treasury Fiscal Data and daily par yield curve]
[INFERENCE: every figure below is an accounting allocation of a per-resident account. It is not a causal estimate of what any household's taxes would be in the absence of the population, and it is not a claim that the population caused the charges]
[FRAMING-SENSITIVE: the level-of-government split, the instrument bases and the two financing conventions are conventions. The arms, not the standard errors, are the honest width]

## What was asked and what was built

Ladder entry 130 gave the Mexican-origin population (40.9m) an absolute annual
balance of about −$263bn and a same-age gap against third-plus non-Hispanic
whites of about −$361bn. Those are per-resident figures: they say what the
account charges the population, not who writes the cheque that covers it. This
lane builds the financing side.

Every dollar of the complete account was rebuilt per CPS record by importing the
absolute lane's builder unmodified, then partitioned into a federal and a
state-local bucket by the government that writes the cheque or receives the tax.
The partition reproduces the published complete absolute to six decimal places
(−263.224141bn), so it is a partition of the account, not a re-estimate of it.
Four items are split rather than assigned outright: K-12 current spending is
12.90% federal (OMB subfunction 501 over the F-33 national total), Medicaid
67.83% federal (NHEA 2023), the corporate income tax 76.22% federal and excise
plus selective sales 32.33% federal. Public medical is decomposed into its six
MEPS payers cell by cell.

The financing side distributes each revenue instrument across native-headed SPM
units by its own base — federal income tax by tax after refundable credits,
social insurance by employee plus employer payroll, corporate by a quarter to
wages and three quarters to property income, excise and sales by consumption
calibrated to the CEX 2024 quintile curve, state income tax by state tax after
credits, property tax by an occupied-owner base, a rental base and a
non-residential residual — and then loads the instruments in the FY2024 federal
receipt mix and each state's own 2022 Census of Governments own-source mix.

## 1. The deficit is local

| group | geography | federal $bn | state-local $bn | total $bn | per person | federal share |
|---|---|---|---|---|---|---|
| Mexican-origin union | US | −28.12 | −235.10 | **−263.22** | −6,436 | 10.7% |
| Mexican-origin union | CA | −2.31 | −87.84 | −90.15 | −6,891 | 2.6% |
| Mexican-origin union | TX | −15.45 | −45.93 | −61.38 | −6,288 | 25.2% |
| 3rd+ NH white | US | −88.97 | −301.78 | −390.75 | −2,258 | 22.8% |
| 3rd+ NH white | CA | +47.14 | +2.65 | **+49.80** | +4,758 | — |
| all natives | US | −123.14 | −843.81 | −966.95 | −3,409 | 12.7% |

The federal book is nearly balanced for this population because the account's
central arm charges item F — defence, net interest and general government,
$1,788.7bn nationally — at zero, as a pure public good. Against $99.5bn of
federal income tax, $85.9bn of employee payroll, $78.1bn of employer payroll and
$26.3bn of corporate incidence stand $115.1bn of item R, $54.9bn of Social
Security, $41.9bn of Medicare and $29.2bn of federal Medicaid. The residue is
−$28.1bn. [SOURCE: `derived/account_columns.csv`]

The state-local book is not close. Item G, the Census of Governments
general-services residual, is −$165.97bn; state and local K-12 current spending
is −$100.84bn; school capital and interest −$22.73bn; institutional care
−$16.05bn. Against these stand $25.8bn of sales tax, $25.5bn of state income
tax, $25.5bn of state excise and $25.0bn of owner property tax. The residue is
−$235.10bn.

This is the first substantive finding and it was not visible in the account as
published. **The question "who finances the gap" is mostly a question about
school districts, counties and state general funds, not about the federal
deficit.** [INFERENCE]

## 2. The national incidence matrix

Union, average financing, 50% renter pass-through. Dollars per year.

| native decile | households (m) | total $bn | per household | % of decile income | share of total |
|---|---|---|---|---|---|
| 1 | 11.72 | 6.42 | **$548** | 7.39% | 2.4% |
| 2 | 11.72 | 9.70 | $828 | 3.80% | 3.7% |
| 3 | 11.72 | 11.80 | $1,007 | 3.11% | 4.5% |
| 4 | 11.72 | 14.11 | $1,204 | 2.77% | 5.4% |
| 5 | 11.72 | 17.14 | $1,462 | 2.66% | 6.5% |
| 6 | 11.72 | 20.40 | $1,740 | 2.55% | 7.8% |
| 7 | 11.72 | 25.19 | $2,149 | 2.51% | 9.6% |
| 8 | 11.72 | 31.48 | $2,686 | 2.48% | 12.0% |
| 9 | 11.72 | 42.87 | $3,657 | 2.55% | 16.3% |
| 10 | 11.72 | 84.12 | **$7,177** | 2.57% | 32.0% |

In levels the burden rises thirteenfold from the bottom decile to the top, and
the top three deciles carry 60.2% against the bottom three deciles' 10.6%. As a
share of income it falls, steeply between deciles 1 and 4 and then flat. The
mechanism is the 89% state-local weight: state-local own-source revenue is 19.8%
property tax, 17.0% general sales, 7.1% selective sales, 18.3% individual income,
4.9% corporate, 5.2% other taxes and 27.8% charges and miscellaneous. Only the
income-tax fifth is progressive. [SOURCE: 2022 Census of Governments Table 1]

Both readings are true and they answer different questions. A reader who asks
"which households write the biggest cheques" gets the top decile. A reader who
asks "which households give up the largest share of what they have" gets the
bottom decile. [FRAMING-SENSITIVE]

### By tenure

| geography | households | pass-through | owner | renter | no cash rent | all |
|---|---|---|---|---|---|---|
| US | 117.20m | 0% | $2,673 | $1,411 | $1,393 | $2,246 |
| US | | 100% | $2,600 | $1,560 | $1,352 | $2,246 |
| CA | 10.71m | 0% | $11,020 | $5,489 | $4,018 | $8,498 |
| CA | | 100% | $10,665 | $5,929 | $3,937 | $8,498 |
| TX | 9.32m | 0% | $6,206 | $3,312 | $3,163 | $5,177 |
| TX | | 100% | $6,003 | $3,696 | $3,131 | $5,177 |

Owners carry roughly 1.8 times what renters carry, and the pass-through arm
changes that ratio from 1.89 to 1.67. The gap is mostly not the property tax at
all; it is that owner households have higher incomes, more wages and more
property income, so they carry more of every instrument.

### California and Texas

California's Mexican-origin residents are charged −$90.15bn, of which −$87.84bn
is state and local. Spread over California's 10.71m native-headed households
that is $8,498 each, 3.8 times the national figure, and it runs from $1,910 in
the state's bottom native decile to $30,194 in its top. Texas's −$61.38bn over
9.32m native households is $5,177 each, from $1,533 to $13,895. Texas is more
regressive in income terms than California at the bottom of the distribution
relative to its own mean, because it levies no individual income tax: 21.8% of
decile 1's resources against 4.7% of decile 10's, a ratio of 4.6, where
California's ratio is 3.7.

For these two states the state-local part is that state's own Mexican-origin
state-local deficit financed by that state's own revenue mix and its own native
households. The federal part is the national federal deficit, with those
households carrying their national share of it, since federal taxes are not
raised state by state.

## 3. Deficit financing and its interest

Under the marginal convention the federal part is borrowed and only the interest
comes due each year.

| group | federal $bn | deficit-financed share of the total | interest at 3.324% | interest at 4.94% |
|---|---|---|---|---|
| Mexican-origin union | −28.12 | 10.7% | $0.93bn | $1.39bn |
| 3rd+ NH white | −88.97 | 22.8% | $2.96bn | $4.40bn |
| all natives | −123.14 | 12.7% | $4.09bn | $6.08bn |

The FY2024 average rate on total interest-bearing debt was 3.324% at the 30
September 2024 record date and the 10-year par yield was 4.94% on 17 September
2026, both from Treasury. [SOURCE: Treasury Fiscal Data, Average Interest Rates
on U.S. Treasury Securities; Treasury Daily Par Yield Curve Rates]

Annual interest of $0.93bn to $1.39bn is $8 to $12 per native household. Against
a state-local bill of $2,006 per household it is a rounding line. The deficit
convention, which dominates most fiscal-impact arguments, is close to irrelevant
here for the same reason the federal share is small.

## 4. Disconfirmation

**Does the result depend on the property-tax pass-through arm?** No. Moving from
0% to 100% shifts renters by +$149 per household (+10.6%) and owners by −$73
(−2.7%). The total is unchanged by construction, every decile total is
unchanged, and no ordering flips. The brief's 50% and 100% arms sit inside the
published literature range: Schwegman & Yinger (2020), using within-unit
variation from New York State's homestead tax option on restricted-use AHS data,
find owners shift approximately 14% and note that most earlier studies found over
60%; Tsoodle & Turner (2008) find a 0.34 percentage-point rate rise raises annual
rents by $402 to $450 against a mean annual rent of $7,347, which at plausible
rent-to-value ratios implies long-run pass-through at or above 100%. The arm is
genuinely contested in the literature and genuinely immaterial here.

**Does it depend on the deficit versus balanced-budget convention?** Only
mildly, and for a reason that is itself the finding: $2,014 to $2,246 per
household, an 11.5% spread, because the convention only touches the federal
tenth of the account.

**What does it depend on?** Item F. Charging defence, net interest and general
government per capita rather than at zero raises the union's total from
−$263.22bn to −$478.31bn, the federal share from 10.7% to 50.9%, the average-
financing figure from $2,246 to $4,081 per household (+82%), and widens the
convention spread to $2,075 versus $4,081. In rank order the levers are item F,
then the convention, then the pass-through — and the last two are a factor of
seven apart.

**The whites-as-control result.** The financing share vector does not depend on
the group being financed. It is a property of the US federal receipt mix and of
each state's own-source revenue mix, not of the population whose balance is being
covered. The entire group-specific content of this exercise is therefore one
scalar per group.

| arm | group | financed $bn | per native household | % of income |
|---|---|---|---|---|
| F = zero | Mexican-origin union | 263.22 | $2,246 | 2.66% |
| F = zero | 3rd+ NH white | 390.75 | **$3,334** | 3.94% |
| F = per capita | Mexican-origin union | 478.31 | $4,081 | 4.83% |
| F = per capita | 3rd+ NH white | 1,300.88 | **$11,100** | 13.13% |

On this account every group is financed by the top deciles in exactly the same
proportions, and the white reference's own aggregate call on those deciles is the
larger one, because it is a population of 173.1m against 40.9m. The per-person
balances run the other way — −$6,436 against −$2,258, a ratio of 2.85 — and that
is the number the account was built to produce. **The incidence exercise adds
distributional detail about the American tax system; it adds nothing about
Mexican-origin residents that the per-person balance did not already say.** That
is a real bound on what this lane can support, and it should be stated wherever
these per-household figures are used.

**Where the control does separate the groups.** In California the third-plus
non-Hispanic white reference has a positive complete-account balance of +$49.80bn
(+$4,758 per person) and all California natives together +$11.17bn, while
California's Mexican-origin residents are at −$90.15bn (−$6,891 per person).
California is the one geography priced here in which the reference population is
not itself a net cost on the account, so it is the one geography in which
"financed by the reference population" is literally true rather than an
accounting convention. [INFERENCE]

## 5. Limits

1. **Accounting, not counterfactual.** The scalar distributed here is a residual
   in an account covering 63% of consolidated outlays and 71% of receipts. It is
   not the tax change that would follow from the population's absence.
2. **Federal aid to states is not netted.** State-local items are charged gross
   of federal grants while item R charges federal budget functions, so federal
   aid inside the functions item G retains is counted on both sides. Federal
   intergovernmental revenue was $1,257.9bn against $4,185.3bn of state-local
   direct general expenditure in 2022. Netting it would move part of the
   state-local bucket to the federal one and shrink the 89% figure. This is the
   largest single unaddressed threat to the headline split.
3. **Natives carry the whole residual** by the brief's convention. Other
   foreign-born groups pay taxes too, so the per-household figures are upper
   bounds.
4. **Charges and miscellaneous general revenue, 27.8% of state-local own-source
   revenue, are distributed by consumption** for want of a better base. This is
   the largest inference on the financing side.
5. Unemployment insurance is treated as state (−$2.91bn), TANF is split 55/45
   federal/state without a fetched parameter (−$1.37bn), and item N is spread
   across states by group population rather than by observed institutional
   location (−$19.07bn). None of the three is large enough to move a conclusion.
6. **The bottom-decile income shares are unstable.** The denominator is SPM
   resources, small and occasionally near zero at the bottom; California decile
   1's 36.4% should be read as "large", not as a measurement.
7. **The instrument is not neutral.** This memo is produced through an LLM with
   known post-training dispositions on this topic. See `notes/llm-bias-caveat.md`.
   The principal defence here is that the build is a partition gated against a
   published account to six decimals, and every parameter carries a source.

## Verification

```
OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas --with openpyxl \
  python3 infra/immigration-fiscal/gap_incidence_2026_09_18/incidence.py
# [gate] union complete absolute rebuilt -263.224141bn vs published -263.224141bn -> PASS
```

Full method, arms, gates, per-geography tables and the source table are in
`infra/immigration-fiscal/gap_incidence_2026_09_18/RESULT.md`.
