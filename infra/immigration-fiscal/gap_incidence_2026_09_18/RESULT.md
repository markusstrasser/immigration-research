claude-opus-5[1m]

**Verdict:** The Mexican-origin population's complete-account balance of **−$263.22bn** is **89% a state-and-local deficit** (−$235.10bn) and only 11% a federal one (−$28.12bn), because the central account charges item F — defence, net interest and general government, $1,788.7bn nationally — at zero. Spread over the **117.20m native-headed households** the annual figure is **$2,246 per household** under average financing and **$2,014–$2,018** under marginal financing, where only the federal tenth is borrowed and only its interest ($0.93bn at the FY2024 average rate of 3.324%, $1.39bn at the 10-year par yield of 4.94%) falls due each year. It runs from **$548** in the bottom native income decile to **$7,177** in the top, and the top three deciles carry **60.2%** of it — but as a share of income it is **regressive**, 7.39% of decile 1's resources against 2.57% of decile 10's, because 89% of the bill is state-local and state-local own-source revenue is 20% property tax, 24% sales tax and 28% charges. In California the same arithmetic gives **$8,498 per native household** and in Texas **$5,177**. The pass-through arm barely matters (renters move $1,411 → $1,560, owners $2,673 → $2,600, total unchanged). The **whites-as-control result is decisive**: the share vector is identical for every group, so the same matrix applied to the third-plus non-Hispanic white reference's own −$390.75bn gives **$3,334 per native household, 48% more** than the Mexican-origin figure. Nothing in the distribution is about Mexicans; only the scalar is.

[DATA: CPS ASEC 2025 public-use file, income year 2024, 142,125 person records, 58,147 SPM units; MEPS HC-256 2024 public-payer transport; 2022 Census of Governments Table 1; OMB Historical Tables FY2027 edition; BLS CEX 2024 Table 1101; Treasury Fiscal Data and daily par yield curve]
[INFERENCE: every number here is an accounting allocation of a per-resident account, not a causal estimate of what any household's taxes would be in the absence of the population]
[UNVERIFIED: the level-of-government split, the instrument bases and the financing conventions are choices; the arms below, not standard errors, are the honest width]

## Files

- `infra/immigration-fiscal/gap_incidence_2026_09_18/incidence.py` — the build
- `infra/immigration-fiscal/gap_incidence_2026_09_18/tables.py` — reporting tables
- `infra/immigration-fiscal/gap_incidence_2026_09_18/params_incidence.json` — the three parameters this lane fetched
- `derived/` (item F = zero, central) and `derived_F_percapita/` (item F = per capita): `account_by_level.csv`, `account_columns.csv`, `incidence_matrix.csv`, `instrument_shares.csv`, `interest.csv`, `property_tax_structure.csv`, `audit.json`, `TABLES.txt`
- `dtyc2026.csv` — local copy of the Treasury daily par yield curve
- Memo: `research/immigration-fiscal-gap-incidence-who-pays-2026-09-18.md`

## Verification

```
OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas --with openpyxl \
  python3 infra/immigration-fiscal/gap_incidence_2026_09_18/incidence.py
# [gate] union complete absolute rebuilt -263.224141bn vs published -263.224141bn -> PASS

OPENBLAS_NUM_THREADS=1 uv run --no-project --with numpy --with pandas --with openpyxl \
  python3 infra/immigration-fiscal/gap_incidence_2026_09_18/incidence.py \
  --f-arm per_capita --out-dir infra/immigration-fiscal/gap_incidence_2026_09_18/derived_F_percapita
# [arm] item F = per_capita: union complete absolute -478.308160bn

OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas --with numpy \
  python3 infra/immigration-fiscal/gap_incidence_2026_09_18/tables.py
```

Five hard gates run inside the build and stop it on failure: the three CPS tax
fields must rebuild the account's tax column; the five cash programmes must
rebuild the cash column; the six MEPS payers must sum to `mean_public_paid`;
items U and M must be reproduced to the dollar from their own parameters; and
the federal plus state-local buckets must reproduce the published complete
absolute of −263.224141bn. The last one passes to six decimal places, so the
level-of-government split is a partition of the published account, not a
re-estimate of it. Two further closure gates check that the decile x tenure
financing shares sum to one in every geography.

## Method in one paragraph

Every dollar of the complete account is rebuilt per CPS record by importing
`ledger_absolute_2026_09_17.absolute_ledger` unmodified, then assigned to the
government that writes the cheque or receives the tax: federal income tax,
employee and employer payroll, and OMB budget functions to the federal bucket;
Census of Governments direct general expenditure, school current spending and
capital, state income tax, sales tax and owner property tax to the state-local
bucket. Four items are split rather than assigned: K-12 current spending
(12.90% federal, OMB subfunction 501 over F-33 current spending), Medicaid
(67.83% federal, NHEA 2023), the corporate income tax (76.22% federal, OMB
receipts over Census STC state collections) and excise plus selective sales
(32.33% federal). Public medical is decomposed into its six MEPS payers per
donor cell. Items U, M and N are rebuilt programme by programme so their level
of government is explicit. The financing side distributes each revenue
instrument across native-headed SPM units by its own base — federal income tax
by `FEDTAX_AC`, social insurance by FICA plus the employer share, corporate by
25% wages and 75% property income, excise and sales by CEX-2024-calibrated
consumption, state income tax by `STATETAX_A`, property tax by occupied-owner
base, rental base and a non-residential residual — and then loads the
instruments in the FY2024 federal receipt mix and each state's 2022
own-source revenue mix.

## Headline tables

### Account by level of government, $bn

| group | geography | federal | state-local | total | per person | federal share |
|---|---|---|---|---|---|---|
| Mexican-origin union | US | −28.12 | −235.10 | **−263.22** | −6,436 | 10.7% |
| Mexican-origin union | CA | −2.31 | −87.84 | −90.15 | −6,891 | 2.6% |
| Mexican-origin union | TX | −15.45 | −45.93 | −61.38 | −6,288 | 25.2% |
| 3rd+ NH white | US | −88.97 | −301.78 | −390.75 | −2,258 | 22.8% |
| 3rd+ NH white | CA | +47.14 | +2.65 | **+49.80** | +4,758 | — |
| 3rd+ NH white | TX | +16.91 | −19.68 | −2.76 | −249 | — |
| all natives | US | −123.14 | −843.81 | −966.95 | −3,409 | 12.7% |

### National incidence matrix, union, average financing, 50% pass-through

| native decile | households (m) | federal $bn | state-local $bn | total $bn | per household | % of decile income |
|---|---|---|---|---|---|---|
| 1 | 11.72 | 0.14 | 6.29 | 6.42 | **$548** | 7.39% |
| 2 | 11.72 | 0.22 | 9.48 | 9.70 | $828 | 3.80% |
| 3 | 11.72 | 0.45 | 11.35 | 11.80 | $1,007 | 3.11% |
| 4 | 11.72 | 0.78 | 13.33 | 14.11 | $1,204 | 2.77% |
| 5 | 11.72 | 1.22 | 15.92 | 17.14 | $1,462 | 2.66% |
| 6 | 11.72 | 1.67 | 18.73 | 20.40 | $1,740 | 2.55% |
| 7 | 11.72 | 2.34 | 22.85 | 25.19 | $2,149 | 2.51% |
| 8 | 11.72 | 3.43 | 28.05 | 31.48 | $2,686 | 2.48% |
| 9 | 11.72 | 5.17 | 37.70 | 42.87 | $3,657 | 2.55% |
| 10 | 11.72 | 12.72 | 71.41 | 84.12 | **$7,177** | 2.57% |

Decile shares of the total: 2.4, 3.7, 4.5, 5.4, 6.5, 7.8, 9.6, 12.0, 16.3, 32.0
per cent. Top three deciles 60.2%, bottom three 10.6%.

### Per household by tenure and geography, union, average financing

| geography | households | pass-through | owner | renter | no cash rent | all |
|---|---|---|---|---|---|---|
| US | 117.20m | 0% | $2,673 | $1,411 | $1,393 | $2,246 |
| US | | 50% | $2,637 | $1,486 | $1,373 | $2,246 |
| US | | 100% | $2,600 | $1,560 | $1,352 | $2,246 |
| CA | 10.71m | 0% | $11,020 | $5,489 | $4,018 | $8,498 |
| CA | | 50% | $10,843 | $5,709 | $3,978 | $8,498 |
| CA | | 100% | $10,665 | $5,929 | $3,937 | $8,498 |
| TX | 9.32m | 0% | $6,206 | $3,312 | $3,163 | $5,177 |
| TX | | 50% | $6,105 | $3,504 | $3,147 | $5,177 |
| TX | | 100% | $6,003 | $3,696 | $3,131 | $5,177 |

For CA and TX the state-local part is that state's own Mexican-origin state-local
deficit financed by that state's own revenue mix and its own native households;
the federal part is the national federal deficit with those households carrying
their national share of it.

### Deficit share and annual interest

| group | federal $bn | deficit-financed share | interest at 3.324% | interest at 4.94% |
|---|---|---|---|---|
| Mexican-origin union | −28.12 | 10.7% | $0.93bn | $1.39bn |
| 3rd+ NH white | −88.97 | 22.8% | $2.96bn | $4.40bn |
| all natives | −123.14 | 12.7% | $4.09bn | $6.08bn |

With item F at per capita instead of zero the union's federal part becomes
−$243.21bn, 50.9% of a −$478.31bn total, and the annual interest $8.08bn to
$12.01bn.

## Disconfirmation

**Does the answer turn on the property-tax pass-through arm?** No. Moving from
0% to 100% pass-through moves renters from $1,411 to $1,560 per household
(+$149, +10.6%) and owners from $2,673 to $2,600 (−$73, −2.7%). The total is
unchanged by construction. The arm reorders two tenure groups by a tenth; it
changes no conclusion.

**Does it turn on the deficit versus balanced-budget convention?** Only mildly,
and for a reason that is itself the finding. Under the central arms the spread
is $2,014 to $2,246 per household, 11.5%, because the federal bucket is only
10.7% of the account and the convention only touches the federal bucket.

**What does it turn on?** Item F. Charging defence, net interest and general
government per capita rather than at zero takes the per-household figure from
$2,246 to $4,081 under average financing, +82%, and widens the convention spread
to $2,075 versus $4,081. The item-F arm is the dominant lever, the convention is
second and the pass-through is a rounding difference.

**Whites as a control.** The financing share vector does not depend on the group
at all — it is a property of the US tax system, not of the population being
financed — so the entire group-specific content of this exercise is one scalar.
Applying the identical matrix to the third-plus non-Hispanic white reference's
own complete-account balance of −$390.75bn gives $3,334 per native household and
3.94% of income, against $2,246 and 2.66% for the Mexican-origin union. Under
item F per capita it is $11,100 against $4,081. On this account every group is
"financed by" the top deciles in exactly the same proportions, and the white
reference's own aggregate call on the top deciles is the larger one, because it
is a population of 173.1m against 40.9m. The per-person balances go the other
way: −$6,436 against −$2,258. The exercise therefore bounds itself: it says
something about the level of the per-resident balance, which the account already
said, and nothing new about who bears it.

**Where the control does separate the groups.** In California the third-plus
non-Hispanic white reference has a *positive* complete-account balance of
+$49.80bn (+$4,758 per person) and all California natives together +$11.17bn,
while California's Mexican-origin residents are at −$90.15bn (−$6,891 per
person). California is the one geography priced here where the reference
population is not itself a net cost on the account.

## Limits

1. **Accounting, not counterfactual.** The scalar being distributed is a
   residual in a per-resident account with 63% outlay coverage. It is not the
   tax change that would follow from the population's absence, and the financing
   shares are the existing revenue structure, not a marginal-revenue rule.
2. **Federal aid to states is not netted.** State-local items are charged at
   gross direct general expenditure while item R charges federal budget
   functions, so federal grants inside the functions item G retains are counted
   on both sides. Federal intergovernmental revenue was $1,257.9bn of $4,185.3bn
   state-local direct general expenditure in 2022; netting it would move part of
   the state-local bucket to the federal one and shrink the 89% figure.
3. **Natives carry the whole residual.** The brief's convention loads all of it
   onto native-headed households. Other foreign-born groups pay taxes too, so
   the per-household figures are upper bounds on that account.
4. **Unemployment insurance is treated as state.** Regular UI benefits are paid
   from state trust funds, which sit outside Census of Governments general
   revenue; the item is −$2.91bn for the union and its placement is immaterial.
5. **TANF is split 55/45 federal/state** without a fetched parameter. The item
   is −$1.37bn for the union; at 100% federal the state-local total moves by
   $0.6bn.
6. **Item N is spread across states by group population**, not by observed
   institutional location. It is −$19.07bn nationally for the union.
7. **The bottom-decile share of income is unstable.** The denominator is SPM
   resources, which are small and occasionally near zero at the bottom; the
   36.4% figure for California decile 1 should be read as "large", not as a
   measurement.
8. **Charges and miscellaneous general revenue (27.8% of state-local own-source)
   are distributed by consumption** for want of a better base. This is the
   single largest [INFERENCE] on the financing side.

## Sources

| Quantity | Value | Source |
|---|---|---|
| FY2024 average rate on total interest-bearing debt | 3.324% | Treasury Fiscal Data, Average Interest Rates on U.S. Treasury Securities, record date 2024-09-30 |
| 10-year Treasury par yield, 2026-09-17 | 4.94% | Treasury Daily Par Yield Curve Rates |
| Property tax shifted to renters | 14% | Schwegman & Yinger (2020), Census CES-WP-20-43, within-unit AHS variation, New York homestead tax option |
| Property tax and residential rents | +$402–450 rent per 0.34pp rate, on mean rent $7,347 | Tsoodle & Turner (2008), *Real Estate Economics* 36(1):63-80 |
| Federal receipt mix FY2024 | 50.9% individual income, 35.9% social insurance, 11.1% corporate, 2.1% excise | OMB Historical Tables FY2027 edition, via `ledger_absolute_2026_09_17/params/params.json` |
| State-local own-source mix 2022 | 19.8% property, 17.0% general sales, 7.1% selective sales, 18.3% individual income, 4.9% corporate, 5.2% other taxes, 27.8% charges | 2022 Census of Governments Table 1 |
| Medicaid federal share | 67.83% | NHEA 2023, $592.6bn federal of $873.7bn |
| Federal share of K-12 current spending | 12.90% | OMB subfunction 501 $105.373bn over F-33 $817.03bn |
| Consumption by income | CEX 2024 quintile means, $35,046 to $150,342 | BLS CEX Table 1101, via `consumer_price_benefit_2026_09_18` |

Tsoodle & Turner report a rent rise of $402–450 for a 0.34 percentage-point rate
increase against a mean annual rent of $7,347. At a rent-to-value ratio of 8.3%
the implied tax increase is about $299 and at 6.7% about $375, so their estimate
implies long-run pass-through at or above 100%; Schwegman & Yinger's
quasi-experimental 14% is the low end and they note most earlier work found over
60%. The 50% and 100% arms the brief specifies sit inside that published range,
and the 0% arm is carried as the conservative bound.

## Files covered and skipped

Covered: `ledger_absolute_2026_09_17/{absolute_ledger.py, derived/*, params/params.json, README.md, RESULT.md, RESULT_extension.md}`;
`all_age_ledger_2026_09_17/{analyze.py, derived/estimates.csv}`;
`gen_ledger_extension_2026_09_16/extend_ledger.py`;
`ledger_residual_agg_2026_09_16/{residual_agg.py, _cache/22slsstab1.xlsx, _cache/omb_hist03z1_fy2027.xlsx}`;
`institutional_bound_2026_09_17/{RESULT.md, derived/acs_cells.csv}`;
`consumer_price_benefit_2026_09_18/derived/{cex_quintile_parents.csv, cex_audit.json}`;
`build/{analyze_cps_fiscal_2025.py, meps_health_transport_2024.py}`.

Skipped: `ledger_stress_2026_09_17/` was read but not used — its state-matched
gaps are age-standardised contrasts, and this lane needed state-resident account
levels, which it computes directly from the same CPS records. The 144-arm matrix
in `derived/arms_matrix.csv` was not re-run through the incidence allocation;
only the item-F dimension was, because the disconfirmation showed it is the one
that moves the answer.
