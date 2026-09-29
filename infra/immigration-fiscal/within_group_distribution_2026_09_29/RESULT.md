**Verdict:** Spread over its 7,106 sampled households, the September 27 case ($321.8–387.4bn a year) leaves most of the union in households that cost other residents more than they pay. Under full allocation (A), **24.2% (SE 0.5 pt) of members at the low end and 20.3% (SE 0.4) at the high end** live in households that pay more than they cost. Counting only individually used services (B), the shares are **31.1% (0.5) and 29.6% (0.5)**. The share rises with the head's education, from 12.4% / 9.4% below high school to 46.2% / 41.1% with a BA or more. It also rises by generation: 18.2% / 14.1% with a Mexico-born head, 26.4% / 24.5% with a second-generation head and 32.4% / 27.3% with a third-plus head. The cost is concentrated. The costliest 10% of households, holding 19% of members, carry **60.9% / 52.6%** of the net cost, and the costliest 20% carry **90.8% / 79.6%**. The member at the median lives in a household costing **$8,716 / $10,139 per member** a year, with quartiles of $349–16,312 at the low end and $2,113–17,661 at the high end. Children's schooling is charged to their own household, and this drives the family pattern. Households with three or more children are 2.3% / 1.1% net-positive, against 42.8% / 38.8% for households with no children. The imputed legal-status split does not hold up when the imputation rule changes (see Disconfirmation). [CALCULATION: `households.py` → `derived/net_positive_shares.csv`, `concentration.csv`, `household_balance_quantiles.csv`] [FRAMING-SENSITIVE]
claude-opus-5-5

# Within-group distribution of the net balance (income-year 2024)

This lane changes no total. It spreads the adopted September 27 case (`main_case_long_run_2026_09_27`,
$321.8194–387.3701bn) over the households of the CPS ASEC 2025 frame that the case is keyed on. It asks what
share of the union's members live in households that pay more than they cost, and how concentrated the cost is.
"Low" and "high" are the case's two ends. The low end is specification 48: shared allocation, GDP
normalization, general government at 0.60 and a 2% capital return. The high end is specification 11: personal
allocation, cash normalization, general government at 0.85 and 3%. A household's balance is its union members'
share of the case: taxes and receipts minus the services and transfers charged to them. A positive balance is a
net cost to other residents; a net contributor has a balance below zero. Members outside the union in the same
household are outside the account, as in the case.

## Method

1. **Lines by generation** (`export_lines.cjs`). Each generation's corrected model comes from the generation
   account: `model_G*.json` plus its corrections payload, which already ends with the enterprise re-key. The
   script evaluates each model with the package's `evaluateFull()` at the two ends. For every line it writes the
   key, allocation, amount, response and cost to other residents, plus the production term and the 24
   capital-return components. Gates: the union reproduces $321.8194 / $387.3701bn. Each generation's rows add to
   `generation_results.csv` (1e-6bn), and the three generations add to the union (1e-9bn).
2. **Persons within each generation** (`households.py`). Each line's corrected amount is spread over the
   generation's persons in proportion to the line's own key at the end's allocation. The keys are the account's
   CPS, MEPS and school vectors, imported read-only from the generation lane's `keys.py`. Gate: 88 key rows
   reproduce `generation_keys.csv` by generation (worst 5.8e-16). Five cases need a rule of their own:
   - **Public order by use** splits into its per-head part and its custody, arrest and ICE part, in the
     proportions of the use key's components. The per-head part goes over all members. The rest goes over
     members aged 18–64, the key's own base: the incarcerated are outside the household frame, so within a
     generation "use" cannot follow individuals.
   - **Medicaid with uninsured use** splits in the proportions of the generation's uncorrected cells. The
     Medicaid part follows the MEPS Medicaid key; the uninsured part follows uninsured person-years.
   - **The capital return** follows each component's own key rule: its numerator lines' person amounts. The 11
     enterprise components follow the enterprise-surplus receipt, which is per head.
   - **The production term** (P + F, a benefit to others of $13.3bn / $8.8bn) follows positive earnings within
     the skill cells. This is the generation lane's Aumann–Shapley attribution carried down to the worker. The
     cell parts are solved from the three generations' terms, with a residual of 1.8e-15bn. The account's CES
     attributes −$19.3bn to the low-skill cell (high school or less) and +$5.9bn to the high-skill cell at the
     low end (−$12.7bn / +$3.9bn at the high end). BA+ households therefore carry a small production *cost*.
   - **The lane constants** are care work, shelter and audit rows 8–10: −$5.16bn / −$5.20bn. They have no
     person-level rule, so they are not assigned and are reported as the residual.
3. **Households.** A household is the CPS household (PH_SEQ); its balance is the sum over its union members.
   Members are weighted by their person weights. Households are counted at the mean weight of their union
   members. The head is the reference person when that person is in the union (5,673 households). Otherwise it
   is the oldest union adult (1,222). If every union member is a minor, the head is the reference person, whose
   generation and status are then "outside_union" (211 households, 286 records).
4. **Legal status** is the Borjas residual imputation from `status_impute_2026_09_16/impute_status.py`, run with
   and without its Medicaid clause, as in ladder 185 (`parent_status_2026_09_23`). Gate: it reproduces that
   lane's Mexico-born 25–64 counts, 3.917061m and 4.778136m. The status applies to Mexico-born heads only;
   other heads are US-born or outside the union.
5. **Standard errors** come from the 160 ASEC replicate weights (successive difference replication, 4/160).
   Each replicate reruns the within-generation spread, the household sums and every statistic, holding the
   engine's line totals fixed. They measure the sampling noise of the distribution, not the model uncertainty
   of the totals. Cells under 200 records carry `small_cell` in the CSVs; none of the cells reported below is
   that small.

**The two conventions.**
- **A, full allocation:** every line at its main-case key and response. General government, public order per
  head, parks, housing and community services, the enterprise surplus and the per-head transfers are per head.
  Roads follow the account's resources key. The capital return follows its components' lines.
- **B, individually used services only:** every receipt except the enterprise surplus, set against three
  groups of spending:
  - transfers keyed to the household's own benefit receipt: CPS benefit amounts and SPM-unit benefits,
    including the income-security line keyed to cash assistance and housing subsidies;
  - health: MEPS use cells, Medicaid with uninsured use and Medicare;
  - K-12 schools: the school part of education plus the school reprice;
  - justice by use (the non-per-head part).

  B leaves out:
  - general government, roads and parks;
  - public order per head;
  - housing and community services;
  - transfers keyed per head or by age: student aid on the per-head P key, employment and training, other
    state benefits and pension guaranty ($9.5bn);
  - college and other education;
  - the capital return, the enterprise surplus and the production term.

  B's total is $201.3bn at the low end and $218.7bn at the high end.

A sensitivity, **A with schools per head**, keeps A but spreads the same school dollars equally over the
union's members instead of charging them to the pupils' households.

## Positive control (A reproduces the case)

| $bn | Low end (spec 48) | High end (spec 11) |
|---|---|---|
| Taxes and receipts (except the enterprise surplus) | −400.16 | −378.31 |
| Transfers keyed to own receipt | +190.71 | +177.89 |
| Health | +189.42 | +191.42 |
| K-12 schools (incl. reprice) | +181.48 | +187.80 |
| Justice by use | +39.86 | +39.86 |
| Justice per head | +29.80 | +29.80 |
| General government | +28.24 | +40.02 |
| Roads and parks | +19.44 | +29.63 |
| Capital return | +33.80 | +55.69 |
| College and other education | +10.96 | +10.82 |
| Per-head and age-keyed transfers | +9.49 | +9.49 |
| Enterprise surplus (receipt) | +5.56 | +5.56 |
| Housing and community services | +1.70 | +1.70 |
| Production term | −13.32 | −8.79 |
| **Households, sum** | **326.98** | **392.57** |
| Not assigned: lane constants (G1 / G2 / G3+) | −5.16 (−2.64 / −1.14 / −1.38) | −5.20 (−2.65 / −1.15 / −1.40) |
| **Households + not assigned = the case** | **321.8194** (difference 0.0000) | **387.3701** (difference 0.0000) |

[CALCULATION: `households.py` → `derived/control.csv`] Every replicate's assigned total equals the full
sample's within 1e-11bn, because the line totals are held.

## Who is a net contributor

Share of the union's members who live in households that pay more than they cost (SE in brackets).

| Breakdown | Cell | Members (m) | Records | A low | A high | B low | B high | A, schools per head, low / high |
|---|---|---|---|---|---|---|---|---|
| All | — | 40.90 | 18,331 | **24.2% (0.5)** | **20.3% (0.4)** | **31.1% (0.5)** | **29.6% (0.5)** | 19.6% / 14.9% |
| Head's education | Below high school | 10.30 | 4,601 | 12.4% (1.0) | 9.4% (0.8) | 16.5% (1.1) | 15.9% (1.1) | 7.5% / 4.6% |
| | High school | 13.56 | 6,087 | 20.4% (1.0) | 16.3% (0.9) | 27.0% (1.2) | 25.6% (1.1) | 15.7% / 10.8% |
| | Some college | 9.92 | 4,433 | 25.8% (1.2) | 22.1% (1.1) | 34.2% (1.4) | 32.9% (1.4) | 20.5% / 16.8% |
| | BA or more | 7.12 | 3,210 | 46.2% (1.7) | 41.1% (1.5) | 55.6% (1.6) | 52.4% (1.7) | 43.4% / 35.1% |
| Head's generation | Mexico-born | 18.23 | 8,244 | 18.2% (0.7) | 14.1% (0.6) | 24.8% (0.8) | 23.4% (0.8) | 12.9% / 8.0% |
| | Second | 11.31 | 4,948 | 26.4% (1.1) | 24.5% (1.0) | 34.0% (1.1) | 34.4% (1.1) | 22.1% / 19.8% |
| | Third-plus | 10.79 | 4,853 | 32.4% (1.1) | 27.3% (1.0) | 39.4% (1.2) | 36.4% (1.2) | 28.6% / 22.2% |
| Own generation | Mexico-born | 12.22 | 5,631 | 22.7% (0.7) | 18.3% (0.7) | 30.1% (0.8) | 29.6% (0.9) | 14.5% / 10.2% |
| | Second | 14.33 | 6,349 | 21.2% (0.7) | 19.0% (0.7) | 27.5% (0.8) | 27.2% (0.8) | 17.5% / 14.3% |
| | Third-plus | 14.34 | 6,351 | 28.4% (0.7) | 23.3% (0.7) | 35.5% (0.8) | 32.1% (0.9) | 26.2% / 19.5% |
| Head's status, Borjas rules | Unauthorized | 6.42 | 2,794 | 20.1% (1.3) | 15.0% (1.3) | 28.1% (1.6) | 27.0% (1.7) | 11.7% / 7.4% |
| | Legal immigrant | 11.80 | 5,450 | 17.2% (0.9) | 13.6% (0.8) | 22.9% (1.0) | 21.5% (1.0) | 13.6% / 8.4% |
| | US-born | 22.09 | 9,801 | 29.4% (0.7) | 25.9% (0.6) | 36.7% (0.7) | 35.3% (0.8) | 25.3% / 21.0% |
| Head's status, no Medicaid rule | Unauthorized | 8.25 | 3,593 | 16.5% (1.1) | 12.3% (1.0) | 23.9% (1.2) | 22.9% (1.3) | 9.9% / 6.1% |
| | Legal immigrant | 9.98 | 4,651 | 19.6% (1.1) | 15.6% (0.9) | 25.4% (1.1) | 23.9% (1.1) | 15.4% / 9.6% |
| Head's age | Under 30 | 7.32 | 3,028 | 29.6% (1.5) | 23.8% (1.5) | 37.8% (1.8) | 36.2% (1.7) | 19.6% / 14.8% |
| | 30–44 | 15.85 | 7,164 | 23.7% (0.8) | 20.1% (0.8) | 30.2% (0.9) | 27.9% (0.9) | 21.8% / 16.1% |
| | 45–64 | 13.56 | 6,168 | 27.2% (1.1) | 23.0% (1.0) | 35.4% (1.2) | 34.4% (1.1) | 21.8% / 16.9% |
| | 65 and over | 4.16 | 1,971 | 6.5% (0.9) | 5.6% (0.9) | 8.6% (1.1) | 8.2% (1.0) | 4.7% / 4.2% |
| State | California | 13.08 | 5,132 | 24.4% (1.0) | 21.9% (1.0) | 31.5% (1.2) | 31.6% (1.1) | 21.0% / 17.7% |
| | Texas | 9.76 | 3,410 | 23.7% (1.3) | 19.3% (1.1) | 30.4% (1.4) | 28.8% (1.4) | 18.5% / 13.1% |
| | Other | 18.05 | 9,789 | 24.2% (0.9) | 19.6% (0.8) | 31.1% (0.9) | 28.5% (0.9) | 19.3% / 13.9% |
| Union children in household | None | 16.63 | 7,477 | 42.8% (1.0) | 38.8% (0.9) | 51.5% (0.9) | 52.5% (0.9) | 29.4% / 25.9% |
| | One or two | 16.84 | 7,483 | 15.4% (0.8) | 10.5% (0.7) | 22.5% (1.0) | 18.6% (1.0) | 16.5% / 9.4% |
| | Three or more | 7.43 | 3,371 | 2.3% (0.7) | 1.1% (0.6) | 4.9% (0.9) | 3.2% (0.9) | 5.0% / 2.7% |

The 211 households whose union members are all minors (0.58m members) are 13.9% / 0.0% net-positive under A.
Their union part is children only. The CSV also carries the share of households that are net-positive
(33.3% / 29.2% under A), the mean net cost per member and each cell's $bn with SEs.

**Mean net cost per member, A.** These are in `net_positive_shares.csv` and are pure reallocations of the
case, low / high:
- By the head's education: below high school $12,654 / $13,815; high school $9,705 / $11,119; some college
  $7,599 / $9,251; BA or more −$1,446 / +$1,093.
- By the head's generation: Mexico-born $9,371 / $10,760; second $7,365 / $8,386; third-plus $5,950 / $8,155.
- Heads aged 65 and over cost $19,692 / $20,630. Social Security, Medicare and MEPS health use make up
  $23.5k of that at the low end.

**Why the pattern.** Taxes per member rise steeply with the head's education: about $18.4k with a BA or more
against $5.7k below high school, at the low end. Transfers per member fall ($3.4k against $5.2k), while health
and the per-head services are flat. Children drive the family pattern (`category_means.csv`). At the low end, a
member of a household with three or more union children carries $9,701 of K-12 cost. A member of a childless
household carries $518. Tax per member is $4,813 against $13,429. Charging children's schooling to the
household therefore makes young families with children the least likely to be net-positive. Heads under 30 fall
from 29.6% to 19.6% when schools are spread per head: under A they are often childless.

Spreading the same school dollars per head instead does not raise the overall share; it lowers it, from 24.2%
to 19.6% at the low end. The per-head charge of about $4,400 a member moves many childless households, the main
net contributors, across zero. It lifts large families only from 2.3% to 5.0%. The per-pupil charge is the
account's own key, and it is the convention the National Academies (2017) use for school costs. Either way, a
cross-section of one year charges a household for its children now and records none of their later taxes.
[FRAMING-SENSITIVE]

## Concentration

Households are ranked by household net cost and counted at their weights. Figures are low end / high end,
SE in brackets.

| | A | B | A, schools per head |
|---|---|---|---|
| Share of the net cost carried by the costliest 10% of households | 60.9% (0.6) / 52.6% (0.5) | 86.9% / 79.5% | 52.8% / 45.6% |
| … by the costliest 20% | 90.8% (0.7) / 79.6% (0.6) | 126.5% / 116.6% | 79.6% / 69.4% |
| Members in the costliest 10% / 20% of households | 18.5% / 33.3% (low); 18.6% / 33.6% (high) | 17.7% / 31.8% | 17.2% / 31.4% (low) |
| Gross cost of net-cost households, $bn | 455.5 (2.3) / 502.2 (2.2) | 366.1 / 374.5 | 432.5 / 479.9 |
| Offset by net-contributor households, $bn | −128.6 (2.3) / −109.6 (2.2) | −164.8 / −155.8 | −105.6 / −87.3 |
| Share of households net-positive | 33.3% (0.6) / 29.2% (0.5) | 40.4% / 39.2% | — |

Under B the costliest 20% carry more than the whole net cost, because the net contributors offset $156–165bn.

**Net cost per member at the quantiles.** Members are weighted by person weight and valued at their
household's cost per member, $ a year (SE in brackets). Negative values are net contributions.

| | P10 | P25 | Median | P75 | P90 |
|---|---|---|---|---|---|
| A, low | −9,399 (326) | 349 (184) | **8,716 (191)** | 16,312 (226) | 23,596 (391) |
| A, high | −7,299 (451) | 2,113 (216) | **10,139 (244)** | 17,661 (274) | 25,115 (421) |
| B, low | −12,007 (357) | −2,341 (223) | 5,773 (186) | 13,236 (202) | 20,378 (343) |
| B, high | −11,518 (399) | −1,729 (205) | 6,114 (209) | 13,471 (232) | 20,645 (444) |
| A, schools per head, low / high | −6,569 / −3,878 | 2,125 / 4,190 | 8,376 / 9,867 | 13,781 / 14,574 | 21,064 / 22,254 |

Per household (household weights), the A median is $14,029 at the low end and $17,983 at the high end; the
interquartile range is −$5,518 to $42,792 and −$2,958 to $48,032
(`household_balance_quantiles.csv`).

## Disconfirmation and limits

- **Legal status is not a robust split.** Under Borjas's rules, unauthorized-headed households are *more*
  often net-positive than legal-immigrant-headed ones: 20.1% against 17.2% at the low end. They are also
  cheaper per member, $7,225 against $10,539. Without the Medicaid clause the order reverses: 16.5% against
  19.6%, and $8,848 against $9,803. There are two reasons:
  - The imputation assigns legal status from benefit receipt (Social Security, SSI, Medicare, military
    coverage and, under the paper's rules, Medicaid). Benefit-heavy households are therefore legal by
    construction. Transfers per member are $2,148 in unauthorized-headed households and $4,781 in
    legal-immigrant-headed ones.
  - The case's status-based corrections are large inside the Mexico-born generation. At the high end they
    remove $17.7bn of the generation's $29.3bn in refundable credits (the SSN rule) and $17.6bn of its
    $37.5bn in federal income tax. This lane spreads them over all Mexico-born persons by key, not onto the
    unauthorized, and the two errors run in opposite directions (`derived/line_scaling.csv`).

  Read the status rows as the imputation's grouping, not as a comparison of legal and unauthorized
  households. [UNVERIFIED direction]
- **The spread within a generation is first order.** Each generation's total is exact, but every correction
  is spread over the whole key inside it. The corrections move the Mexico-born generation's lines by $63bn /
  $83bn gross, the second by $32bn / $19bn and the third-plus by $22bn / $19bn (`line_scaling.csv`). The
  education and generation gradients are larger than any plausible reallocation of these within a
  generation. The status split is not.
- **Justice by use is only by generation.** Custody and arrests follow generation and age 18–64, not
  individual offending, which the survey does not record. Within a generation, B's "justice by use" is a
  charge per working-age adult. It adds about $1.1k per member to BA+ households at the low end, against
  $0.9k below high school.
- **The production term favours low-skill workers.** The account's CES makes the low-skill cell a benefit
  to others and the high-skill cell a small cost. Assigning it to workers adds about $310 per member to BA+
  households and subtracts about $570 per member below high school. B leaves the term out.
- **Mixed households and the shared allocation.**
  - 12.5% of members live in households whose reference person is outside the union. They are 35.0%
    net-positive under A at the low end, against 22.6% in the rest.
  - At the low end the shared allocation splits every key equally within the SPM unit. A union member in a
    mixed unit therefore carries part of a non-member's taxes and benefits, as the case does.
- **Survey noise.**
  - CPS benefit and income amounts are misreported and imputed. The account corrects the totals, but the
    distribution inside each key is the CPS's.
  - Per-household balances are noisy. That is why the results are shares and quantiles with replicate SEs,
    not individual households.
- **One year, not a lifetime.** A retired household is a net cost now on benefits it paid into earlier. A
  young family is a net cost for children who will pay taxes later. Neither is a lifetime balance.
- **Outside checks.** The education gradient runs the same way as published breakdowns by education, such as
  the National Academies' 2017 per-capita estimates. They are not comparable in level: they use a different
  object, reference group and year. [INFERENCE] Not searched in this lane:
  - a published share of immigrant households that are net contributors under a comparable full allocation.
    [GAP]

**Would change it.** Status-specific rules for the SSN and compliance corrections would change the status
rows. A person-level care-work and shelter rule would put the −$5.2bn residual on the right households; it is
about −$126 per member. A household definition based on the tax unit instead of the address would change the
mixed-household results.

## Files

- `export_lines.cjs`: the case by generation and line at the two ends, gated against the generation account.
  It writes `_cache/lines.json` (ignored).
- `households.py`: persons, households, conventions, replicate SEs and gates. It writes:
  - `derived/net_positive_shares.csv`: every breakdown, convention and end, with members, records, the share
    of members and of households net-positive, the mean net cost per member, the cell's $bn, SEs and
    `small_cell`;
  - `derived/concentration.csv`: top 10% and 20% shares, member shares, gross cost and offset, the share of
    households net-positive, with SEs;
  - `derived/household_balance_quantiles.csv`: P10–P90 per member and per household, with SEs;
  - `derived/category_means.csv`: the mean net cost per member by category and breakdown cell, with SEs;
  - `derived/control.csv`: the positive control;
  - `derived/line_scaling.csv`: corrected and uncorrected generation amounts per line;
  - `_cache/households.parquet` (ignored): one row per household with its categories.

**Covered (read-only).**
- `main_case_long_run_2026_09_27/package.cjs` and `derived/corrections.json`.
- `generation_account_2026_09_24`: `frame.py`, `keys.py`, `derived/model_G*.json`,
  `generation_corrections.json`, `generation_keys.csv`, `generation_key_shares.json` and
  `generation_results.csv`.
- `capital_return_services_2026_09_27/derived/engine_components.json`.
- `status_impute_2026_09_16/impute_status.py`; `parent_status_2026_09_23/parent_status.py` for the rules and
  counts.
- `cps_imputation_keys_2026_09_23/common.py`.

**Skipped.**
- Convention (b) of the generation account, minors with their parents. The household already holds its
  children, so it would not change a household's balance.
- Other specifications than the two ends.
- The generation lane's per-lane correction rules at person level. Its 504-line `correction_rules.py` works
  at generation level, and carrying each rule down to persons is the "Would change it" item above.
- `california_medical_status_2026_09_23`'s state-aware status variant (the imputation prints a `[DEGRADED]`
  note that points to it). Both rule sets are shown instead.

## Reproduce

```sh
# from the repository root
node infra/immigration-fiscal/within_group_distribution_2026_09_29/export_lines.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --weights row4
# the case adopted on 2026-09-29 (row-4 weights only), written to derived/sept29/
node infra/immigration-fiscal/within_group_distribution_2026_09_29/export_lines.cjs --case sept29
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/within_group_distribution_2026_09_29/households.py --case sept29 --weights row4
```

Both scripts stop with exit 1 on a failed gate. Together they run in about ten seconds.

## Log

- 2026-09-29 00:21 JST — lane directory and stub created; reading generation_account_2026_09_24 and the main-case package.
- 2026-09-29 00:29 JST — export done
- 2026-09-29 00:31 JST — households.py runs: all gates pass (88 key rows reproduce generation_keys.csv, 5.8e-16; production cells close; each generation's pieces + residual = its cost; households + lane constants = 321.819357 / 387.370055). 7,106 households, 18,331 union person records; 1,433 households have a reference person outside the union.
- 2026-09-29 00:37 JST — rerun of both scripts (exit 0): the six derived CSVs and `_cache/lines.json` are byte-identical to the previous run (time from the `date` call made with the rerun).
- 2026-09-29 00:43 JST — since the 00:29 entry: households.py built and gated (keys, production cells, generation closure, households + lane constants = the case), spending categories set by key, the schools-per-head sensitivity and category means added, minor-only households headed by their reference person; RESULT.md written with the final numbers.
- 2026-09-29 04:43 JST — `--weights row4` arm added (audit row 4's weights on all 161 columns; key-total gate re-pinned to G2/G3+ `generation_keys.csv` and the union's row-4 `age_bins.csv`; union count, per-head part and per-head spread gates added; gates now run before anything is written). Validation exit codes: export 0, published 0 (`derived/` unchanged), row 4 0, `rerun_lane.py` 0 with 15/15 files identical (04:38–04:41 from `date`). Results in "On the account's count (audit row 4)" below.

## Lead verification (2026-09-29 00:53 JST)

- Reran both scripts in place with `scripts/rerun_lane.py`: rc 0, 9 of 9 files byte-identical.
- The positive control (households plus the lane constants reproduce $321.8194bn / $387.3701bn) runs inside `households.py`, which exits 1 on any failed gate.

## On the account's count (audit row 4), 2026-09-29

**Verdict:** Spread over the 39,712,493 members the case prices, instead of the published CPS union of 40,896,574, the household shares stand. No share of members in net-contributor households moves by more than its standard error under either convention. Under full allocation (A) the shares are **24.2% / 20.5%**, against 24.2% / 20.3%. Counting only individually used services (B) they are **31.0% / 29.8%**, against 31.1% / 29.6%. The education and generation gradients move by at most 0.5 points, and the legal-status split still flips with the imputation rule. The dollar figures rise, because the case's unchanged totals now fall on 2.9% fewer members. The mean per member rises by exactly that factor, 2.98%, and the Mexico-born members' own mean rises 10.7%. The median member's household costs **$9,097 / $10,405** per member, against $8,716 / $10,139; both moves exceed their SEs. The per-head school charge is $4,567 / $4,726, against $4,438 / $4,592. BA+ heads stay near zero (−$1,474 / +$1,098), and the costliest tenth of households carries 60.7% / 52.3% of the net cost (was 60.9% / 52.6%). The gates that add household charges up to the case's line totals close to float precision on both arms, because the spread rescales every line to its generation's total. The frame mismatch shows instead in the per-head lines: on the published weights the Mexico-born are charged 9.7% less per member than other members for the same line, and on row 4 the spread is 7.5e-11. [CALCULATION: `households.py --weights row4` → `derived/row4/net_positive_shares.csv`, `household_balance_quantiles.csv`, `concentration.csv`, `category_means.csv`] [FRAMING-SENSITIVE: the per-member denominator]

claude-opus-5-5

**Published → row 4.** Columns are the case's two ends under each convention. Shares are % of members; SEs are the published figure's replicate SE. An asterisk marks a change larger than that SE. The change is a reweighting to fixed ACS 2024 targets, so the mark compares its size with the figure's sampling noise; it is not a test of the change.

| | A, low | A, high | B, low | B, high |
|---|---|---|---|---|
| Union members (m) | 40.90 → 39.71 | 40.90 → 39.71 | 40.90 → 39.71 | 40.90 → 39.71 |
| **Members in net-contributor households** (SE 0.4–0.5) | **24.2 → 24.2** | **20.3 → 20.5** | **31.1 → 31.0** | **29.6 → 29.8** |
| Head below high school | 12.4 → 12.0 | 9.4 → 9.2 | 16.5 → 16.1 | 15.9 → 15.4 |
| Head high school | 20.4 → 20.3 | 16.3 → 16.7 | 27.0 → 26.7 | 25.6 → 26.0 |
| Head some college | 25.8 → 25.8 | 22.1 → 22.1 | 34.2 → 34.1 | 32.9 → 33.0 |
| Head BA or more | 46.2 → 46.3 | 41.1 → 41.4 | 55.6 → 55.9 | 52.4 → 52.6 |
| Head Mexico-born | 18.2 → 17.8 | 14.1 → 14.3 | 24.8 → 24.3 | 23.4 → 23.5 |
| Head second generation | 26.4 → 26.6 | 24.5 → 24.6 | 34.0 → 33.8 | 34.4 → 34.5 |
| Head third-plus | 32.4 → 32.4 | 27.3 → 27.3 | 39.4 → 39.4 | 36.4 → 36.4 |
| Head unauthorized, Borjas rules | 20.1 → 19.2 | 15.0 → 14.6 | 28.1 → 27.3 | 27.0 → 26.9 |
| Head legal immigrant, Borjas rules | 17.2 → 17.1 | 13.6 → 14.1 | 22.9 → 22.8 | 21.5 → 21.7 |
| Head unauthorized, no Medicaid rule | 16.5 → 15.6 | 12.3 → 11.9 | 23.9 → 23.1 | 22.9 → 22.8 |
| Head legal immigrant, no Medicaid rule | 19.6 → 19.6 | 15.6 → 16.2 | 25.4 → 25.3 | 23.9 → 24.0 |
| Households net-positive | 33.3 → 33.3 | 29.2 → 29.5 | 40.4 → 40.3 | 39.2 → 39.2 |
| **Net cost per member, $** | | | | |
| **Median member's household** | 8,716 → 9,097\* | 10,139 → 10,405\* | 5,773 → 6,003\* | 6,114 → 6,317 |
| Mean, all members | 7,995 → 8,234\* | 9,599 → 9,885\* | 4,923 → 5,077\* | 5,347 → 5,513\* |
| Mean, BA+ heads | −1,446 → −1,474 | +1,093 → +1,098 | −5,435 → −5,539 | −4,088 → −4,184 |
| Mean, Mexico-born members (own generation) | 7,889 → 8,736\* | 6,625 → 7,336\* | 5,473 → 6,091\* | 3,254 → 3,633\* |
| Mean, unauthorized-headed (Borjas rules) | 7,225 → 7,790\* | 8,652 → 9,403\* | 4,611 → 5,022 | 4,883 → 5,402\* |
| Mean, legal-immigrant-headed (Borjas rules) | 10,539 → 11,063\* | 11,907 → 12,459\* | 7,665 → 8,046\* | 7,884 → 8,228\* |
| **Concentration** | | | | |
| Costliest 10% of households, share of the net cost | 60.9 → 60.7 | 52.6 → 52.3 | 86.9 → 86.4 | 79.5 → 78.9 |
| Members in the costliest 10% | 18.5 → 18.7 | 18.6 → 18.7 | 17.7 → 17.8 | 17.7 → 17.8 |
| Offset by net-contributor households, $bn | −128.6 → −128.4 | −109.6 → −109.5 | −164.8 → −164.5 | −155.8 → −155.5 |
| **A with schools per head** | | | | |
| School charge per member (the ladder's "about $4,400"), $ | 4,438 → 4,567 | 4,592 → 4,726 | | |
| Members in net-contributor households | 19.6 → 19.7 | 14.9 → 15.2 | | |

[CALCULATION: `derived/` against `derived/row4/`, same file and row]

In the schools-per-head sensitivity, three high-end shares move by more than their SE: below-high-school heads 4.6% → 5.2%, Mexico-born heads 8.0% → 8.6% and Mexico-born members 10.2% → 11.1%. No share under A or B does.

**What moved and why.**
- **Dollars per member.** Row 4 removes 1,184,081 Mexico-born members outside California and Texas, and the case's line totals stay as they are. The same dollars therefore fall on fewer people. The union mean rises by the count factor, 1.029816. The Mexico-born members' own mean rises 10.73%, and the second and third-plus generations' own means do not move under A, since row 4 leaves their totals and counts. Medians rise 2.6–4.4%, and the 75th and 90th percentiles 2.0–3.4%.
- **Shares barely move.** For the Mexico-born as a group, row 4 scales every category by the same factor. Their mean taxes, transfers, health and per-head charges each rise exactly 10.73%; only the two splits below differ. A balance scaled by a positive factor keeps its sign. Person by person the factors differ: each line's charge per Mexico-born person rises by the inverse of its key's fall, 5–18%, since their key totals fall to 0.848–0.953 of the published ones (median 0.908, across 84 key vectors). The shares move only through those differences, through the reweighting (17.18m members in Mexico-born-headed households instead of 18.23m) and through mixed households, where the Mexico-born members now carry more.
- **BA+ heads.** Their balance is near zero, and it stays near zero when it is scaled.
- **Concentration.** The costliest tenth's share falls 0.3–0.6 points, within its SE.
- **Legal status.** The split still flips with the imputation rule. Under Borjas's rules, 19.2% of members in unauthorized-headed households live in net-contributor households at the low end, against 17.1% in legal-immigrant-headed ones. Without the Medicaid clause, the figures are 15.6% and 19.6%. Row 4 removes more of the imputed unauthorized than of the Mexico-born as a whole: the Mexico-born unauthorized aged 25–64 fall from 3.917m to 3.401m under Borjas's rules (−13.2%) and from 4.778m to 4.194m without the clause (−12.2%). All Mexico-born members fall 9.7%. The imputed unauthorized are all noncitizens, whom row 4 scales by 0.778 outside CA and TX, against 0.856 for naturalized citizens. The status rows remain the imputation's grouping, not a legal comparison.
- **B's total moves; A's does not.** B's total rises $0.30bn / $0.29bn, to $201.6bn / $218.9bn, because two within-line splits follow the count:
  - public order's per-head part moves $0.41bn to justice by use, a B item;
  - the first generation's education line moves $0.11bn / $0.13bn from K-12 schools (B) to college and other education (A only), because row 4 removes more of the first generation's school key than of its college key.

  A's total is unchanged. `control.csv` differs only in those four category rows.

**The gates on both arms.** The spread rescales each line to its generation's total under whatever weights it is given. The gates that add household charges up to the case are therefore identities, and they close to float precision on both arms, published / row 4:
- each generation's pieces against its cost: 8.5e-14 / 8.5e-14bn;
- households plus the residual against the case: 6.3e-13 / 2.3e-12bn;
- every replicate against the full sample: 9.8e-12 / 6.6e-12bn;
- the key totals against their references: 5.8e-16 / 5.8e-16 (relative).

On row 4 the key-total gate is re-pinned. G2 and G3+ reproduce `generation_keys.csv`, since row 4 leaves their weights, and the union reproduces `main_case_decomposition_2026_09_29/derived/age_bins.csv`, column row4. The row-4 union count equals `headcount.csv` exactly (39,712,493.331). The check that separates the two frames is new. The engine charges each per-head line the same amount per member in every generation on the row-4 count. On the published weights, the Mexico-born are charged 1/1.107 of what other members are charged for every per-head line with a nonzero charge (general government, parks and recreation, housing and community services, other state benefits, the enterprise surplus): a spread of 9.7%. On row 4 the widest spread is 7.5e-11, and the row-4 arm gates it at 1e-9. [CALCULATION: `households.py` gate lines]

**What the row-4 arm changes beyond the weights.**
- Public order's per-head part moves with each generation's share of the civilian frame: G1 −$0.820bn, G2 and G3+ +$0.036bn each. This reproduces the engine's own row-4 change to that part (`generation_account_2026_09_24/derived/stack_by_generation.json`, component `C_row4_weights`) within 5.3e-8bn, and it is gated.
- Two inputs are kept at their published values, and both are sized:
  - The production term's attribution. The generation terms fit the published labor shares to 1.8e-15bn. On row-4 labor shares they would leave 0.030bn / 0.020bn, so the generation lane attributed the term on the published weights, and the case keeps the term at its published value. Each generation-by-cell part is still spread over its workers at row-4 weights.
  - G1's split of Medicaid with uninsured use, which follows the generation's uncorrected cells. A first-order row-4 update would move $0.085bn / $0.124bn inside G1 from uninsured to Medicaid-covered persons, both within health.
- The status imputation's count gate stays on the published weights. The flag does not use them.

**Would change it.** If the CPS rather than the ACS counts the Mexico-born outside CA and TX correctly (ladder 209), the fiscal case itself belongs on 40.90M and its line totals move with it. Neither arm here would then stand as it is.

**Validation (2026-09-29, exit codes).** `export_lines.cjs` 0. `households.py --weights published` 0, and its six `derived/` files unchanged: `git status` shows only `derived/row4/` as new. `households.py --weights row4` 0. `scripts/rerun_lane.py` over the three commands 0: IDENTICAL, 15 of 15 files unchanged.

**Files.** `households.py --weights row4` writes the same six files to `derived/row4/` and its household table to `_cache/row4/households.parquet` (ignored). The published run's outputs are unchanged.

## v4 case (sept29), 2026-09-29

**Verdict:** Spread over the 39,712,493 members it prices (audit row 4), the v4 main case ($371.4146 / $434.8410bn) leaves **16.2% (SE 0.4) / 12.3% (0.4)** of the union's members in households that pay more than they cost under full allocation (A). The September 27 case on the same weights leaves 24.2% / 20.5%. Under B, which now counts the members' own pension accrual beside their taxes and individually used services, the shares are **23.8% (0.5) / 22.1% (0.5)**, against 31.0% / 29.8%. The costliest tenth of households carries **53.2% (0.5) / 47.5% (0.5)** of the net cost, against 60.7% / 52.3%, and the costliest fifth 79.4% / 72.1%. The pension switch drives the change. The case now charges each worker the benefits their payroll taxes earn: 97.4 cents per OASDI tax dollar (ratio_net 0.9737) plus the Part A accrual, $150.5bn / $143.9bn in all. It no longer charges retirees their current Social Security benefits or Medicare's Part A share. A working household's payroll taxes therefore mostly stop counting as a net contribution, and retiree households get cheaper. At the low end, members with a BA+ head fall from 46.3% to 36.2% net-positive, and members with a head aged 65 or over rise from 6.5% to 9.8%. The member at the median lives in a household costing **$9,755 / $11,160** per member, against $9,097 / $10,405. [CALCULATION: `export_lines.cjs --case sept29`, `households.py --case sept29 --weights row4` → `derived/sept29/net_positive_shares.csv`, `concentration.csv`, `household_balance_quantiles.csv`, `category_means.csv`] [FRAMING-SENSITIVE: the accrual convention, and its spread inside a generation]

claude-opus-5-5

The run was resumed after the 20:51 JST reboot. The code was written before it, and every step below was rerun after it (log at the end).

**What runs.**
- `export_lines.cjs --case sept29` evaluates the adopted payload (`main_case_2026_09_29/derived/corrections.json`, through the adopted package at its main profile) and the generation account's v4 split (`generation_corrections_sept29.json`) at specifications 48 and 11. It also evaluates the cash set, the pension switch off, at the same specifications. Its payload is candidate v4's `corrections_v4_cash.json`, from which the adopted lane builds its cash-set row. The pension lines are split into their parts from the difference. The script writes `_cache/sept29/lines.json`.
- `households.py --case sept29 --weights row4` spreads the lines over persons and households. It writes the six files to `derived/sept29/` and the household table to `_cache/sept29/households.parquet` (ignored).
- The case runs on the row-4 weights only: `--case sept29` without `--weights row4` stops with [BLOCKED]. The September 27 files in `derived/` and `derived/row4/` do not move.

**Positive control (A reproduces the case).** $bn, one decimal. Two parts carry controlled rounding so that the printed parts add to the printed totals: roads and parks at the low end (22.05, printed 22.1) and health at the high end (173.55, printed 173.5).

| $bn | Low end (spec 48) | High end (spec 11) | Sept 27 on row 4, low / high |
|---|---|---|---|
| Taxes and receipts (except the enterprise surplus) | −435.6 | −413.9 | −400.2 / −378.3 |
| Transfers keyed to own receipt | +136.5 | +127.2 | +190.7 / +177.9 |
| Health | +171.6 | +173.5 | +189.4 / +191.4 |
| Pension accrual (new; in B) | +150.5 | +143.9 | — |
| K-12 schools (incl. reprice) | +181.4 | +187.7 | +181.4 / +187.7 |
| Justice by use | +44.0 | +44.0 | +40.3 / +40.3 |
| Justice per head | +32.1 | +32.1 | +29.4 / +29.4 |
| General government | +28.2 | +40.0 | +28.2 / +40.0 |
| Roads and parks | +22.1 | +33.1 | +19.4 / +29.6 |
| Capital return | +34.4 | +57.2 | +33.8 / +55.7 |
| College and other education | +11.1 | +10.9 | +11.1 / +10.9 |
| Per-head and age-keyed transfers | +9.5 | +9.5 | +9.5 / +9.5 |
| Enterprise surplus (receipt) | +0.8 | +0.8 | +5.6 / +5.6 |
| Housing and community services | +1.7 | +1.7 | +1.7 / +1.7 |
| Production term | −11.7 | −7.7 | −13.3 / −8.8 |
| **Households, sum** | **376.6** | **440.0** | 327.0 / 392.6 |
| Not assigned: lane constants | −5.2 | −5.2 | −5.2 / −5.2 |
| **Households + not assigned = the case** | **371.4146** (difference 1.5e-12) | **434.8410** (4.5e-13) | 321.8194 / 387.3701 |

[CALCULATION: `derived/sept29/control.csv` against `derived/row4/control.csv`]

Against September 27 on the same weights:
- Taxes and receipts rise $35.5bn / $35.6bn. Most of the rise is item 5's property taxes, $27.2bn: the owner-occupied tax $19.0bn, the tax on tenant-occupied housing $6.8bn and personal property $1.3bn. Sales and excise taxes add $7.5bn.
- Transfers fall $54.2bn / $50.7bn. Social Security benefits leave the account ($56.3bn / $53.0bn), and workers' compensation and housing subsidies fall $1.3bn / $1.1bn. Public housing's deficit enters at $3.4bn.
- Health falls $17.9bn. Medicare's Part A share of benefits leaves ($19.7bn), and state pricing adds $1.8bn to health services.
- The pension accrual enters: OASDI $109.4bn / $102.8bn and Part A $41.1bn.
- State pricing of public order adds $6.4bn to justice. Roads by miles and state pricing of recreation add $2.6bn / $3.5bn to roads and parks, and the capital return rises $0.6bn / $1.5bn. The enterprise surplus falls $4.7bn, of which $3.4bn is public housing's deficit, now keyed as a transfer. The production term moves to the row-4 grid.

**September 27 → September 29, both on row 4.** The same persons and weights; only the case changes. Shares are % of members. The SEs of the sept29 shares in the headline row are in brackets; those of the other rows are in `net_positive_shares.csv`.

| | A, low | A, high | B, low | B, high |
|---|---|---|---|---|
| Union members (m) | 39.71 → 39.71 | 39.71 → 39.71 | 39.71 → 39.71 | 39.71 → 39.71 |
| Net cost assigned to households, $bn | 327.0 → 376.6 | 392.6 → 440.0 | 201.6 → 248.4 | 218.9 → 262.4 |
| **Members in net-contributor households** | **24.2 → 16.2 (0.4)** | **20.5 → 12.3 (0.4)** | **31.0 → 23.8 (0.5)** | **29.8 → 22.1 (0.5)** |
| Head below high school | 12.0 → 7.1 | 9.2 → 4.2 | 16.1 → 10.8 | 15.4 → 10.0 |
| Head high school | 20.3 → 12.0 | 16.7 → 8.4 | 26.7 → 17.8 | 26.0 → 16.8 |
| Head some college | 25.8 → 16.9 | 22.1 → 13.5 | 34.1 → 27.0 | 33.0 → 24.7 |
| Head BA or more | 46.3 → 36.2 | 41.4 → 29.7 | 55.9 → 49.1 | 52.6 → 45.6 |
| Head Mexico-born | 17.8 → 11.0 | 14.3 → 7.1 | 24.3 → 17.0 | 23.5 → 15.8 |
| Head second generation | 26.6 → 18.0 | 24.6 → 15.7 | 33.8 → 26.7 | 34.5 → 26.1 |
| Head third-plus | 32.4 → 22.9 | 27.3 → 17.9 | 39.4 → 32.2 | 36.4 → 29.0 |
| Head under 30 | 29.8 → 16.4 | 24.1 → 12.1 | 37.5 → 27.0 | 36.4 → 24.8 |
| Head 30–44 | 23.6 → 16.4 | 20.2 → 12.6 | 30.1 → 22.2 | 28.1 → 20.5 |
| Head 45–64 | 27.4 → 17.9 | 23.6 → 13.6 | 35.3 → 27.0 | 34.9 → 25.2 |
| Head 65 and over | 6.5 → 9.8 | 5.8 → 7.8 | 8.8 → 14.3 | 8.1 → 13.5 |
| No union children | 42.8 → 30.3 | 39.0 → 24.4 | 51.4 → 43.7 | 52.4 → 42.3 |
| One or two union children | 15.6 → 9.1 | 11.0 → 5.6 | 22.4 → 14.0 | 19.2 → 11.5 |
| Three or more | 2.4 → 1.2 | 1.1 → 1.0 | 5.0 → 2.0 | 3.3 → 1.3 |
| Head unauthorized, Borjas rules | 19.2 → 10.0 | 14.6 → 6.5 | 27.3 → 16.3 | 26.9 → 15.0 |
| Head legal immigrant, Borjas rules | 17.1 → 11.6 | 14.1 → 7.4 | 22.8 → 17.3 | 21.7 → 16.2 |
| Head unauthorized, no Medicaid rule | 15.6 → 8.3 | 11.9 → 5.5 | 23.1 → 13.3 | 22.8 → 12.3 |
| Head legal immigrant, no Medicaid rule | 19.6 → 13.2 | 16.2 → 8.3 | 25.3 → 19.9 | 24.0 → 18.5 |
| Households net-positive | 33.3 → 24.2 | 29.5 → 18.7 | 40.3 → 33.4 | 39.2 → 31.2 |
| **Net cost per member, $** | | | | |
| **Median member's household** | 9,097 → 9,755 | 10,405 → 11,160 | 6,003 → 6,597 | 6,317 → 6,952 |
| P10 | −9,859 → −3,790 | −7,708 → −1,628 | −12,467 → −6,661 | −12,048 → −5,881 |
| P90 | 24,321 → 22,207 | 25,877 → 23,627 | 21,041 → 18,525 | 21,320 → 18,629 |
| Mean, all members | 8,234 → 9,483 | 9,885 → 11,081 | 5,077 → 6,254 | 5,513 → 6,606 |
| Mean, BA+ heads | −1,474 → +1,481 | 1,098 → 3,809 | −5,539 → −2,376 | −4,184 → −1,193 |
| Mean, below-high-school heads | 13,244 → 13,067 | 14,478 → 14,333 | 10,474 → 10,077 | 10,512 → 10,065 |
| Mean, heads 65 and over | 20,146 → 10,114 | 21,116 → 11,312 | 17,077 → 6,960 | 16,945 → 7,010 |
| Mean, heads 30–44 | 8,162 → 11,064 | 10,251 → 12,916 | 4,850 → 7,689 | 5,692 → 8,263 |
| Mean, Mexico-born members (own generation) | 8,736 → 9,049 | 7,336 → 8,133 | 6,091 → 6,189 | 3,633 → 4,178 |
| Mean, unauthorized-headed (Borjas rules) | 7,790 → 9,966 | 9,403 → 11,524 | 5,022 → 7,009 | 5,402 → 7,277 |
| Mean, legal-immigrant-headed (Borjas rules) | 11,063 → 11,254 | 12,459 → 12,636 | 8,046 → 8,091 | 8,228 → 8,208 |
| **Concentration** | | | | |
| Costliest 10% of households, share of the net cost | 60.7 → 53.2 | 52.3 → 47.5 | 86.4 → 69.7 | 78.9 → 65.4 |
| Costliest 20% | 90.6 → 79.4 | 79.4 → 72.1 | 126.1 → 100.9 | 116.1 → 95.6 |
| Members in the costliest 10% | 18.7 → 19.6 | 18.7 → 19.6 | 17.8 → 19.0 | 17.8 → 18.9 |
| Gross cost of net-cost households, $bn | 455.4 → 454.0 | 502.1 → 505.9 | 366.1 → 350.7 | 374.4 → 358.1 |
| Offset by net-contributor households, $bn | −128.4 → −77.4 | −109.5 → −65.8 | −164.5 → −102.3 | −155.5 → −95.8 |
| **A with schools per head** | | | | |
| Members in net-contributor households | 19.7 → 11.2 | 15.2 → 8.3 | | |

[CALCULATION: `derived/row4/` against `derived/sept29/`, same file and row]

The per-member figures divide by the row-4 count: 39,712,493 members in all, of whom G1 11,036,701, G2 14,333,218 and G3+ 14,342,575 (`net_positive_shares.csv`, own generation).

**What moved and why.** Per member, A, low end, $ (`category_means.csv`):

| Head | Taxes | Transfers | Health | Pension accrual | Net cost (all categories) |
|---|---|---|---|---|---|
| All members | −10,076 → −10,970 | 4,802 → 3,438 | 4,770 → 4,320 | 0 → 3,791 | 8,234 → 9,483 |
| Aged 65 and over | −9,028 → −10,007 | 12,828 → 4,091 | 11,269 → 8,585 | 0 → 2,233 | 20,146 → 10,114 |
| Aged 30–44 | −9,993 → −10,843 | 3,772 → 3,561 | 3,719 → 3,618 | 0 → 3,920 | 8,162 → 11,064 |
| BA or more | −18,753 → −20,215 | 3,500 → 2,022 | 4,776 → 4,355 | 0 → 6,425 | −1,474 → +1,481 |
| Below high school | −5,970 → −6,637 | 5,453 → 3,859 | 5,184 → 4,561 | 0 → 2,403 | 13,244 → 13,067 |

- The accrual follows OASDI and HI receipts, so it lands where the payroll taxes are: $6,425 per member with a BA+ head, against $2,403 below high school.
- The benefits it replaces sat with retirees. Heads aged 65 and over lose $8,737 of transfers and $2,684 of health per member and gain $2,233 of accrual; their net cost halves.
- Net contributors are mostly working households whose taxes exceed their services. The accrual takes back 97 cents of each OASDI dollar they pay, so many of them cross zero: BA+ heads fall from 46.3% to 36.2%, and households without children from 42.8% to 30.3%.
- The cost becomes less concentrated. Retirees and large families were the costliest households; retirees' charge falls, and the accrual spreads cost over working households. The offset by net contributors shrinks from $128.4bn to $77.4bn at the low end.
- The status rows no longer flip with the imputation rule: unauthorized-headed households are less often net-positive under both. This is not evidence about status, because the accrual is spread without regard to it (rule 1, below).

**Rules designed for the case's new lines.** Each generation's line is carried down to its persons; the alternative is beside each.
1. **The pension switch** (social_security, medicare, federal_income_tax; new category `pension_accrual`, in B).
   - Rule: Social Security's line is now the OASDI accrual. Inside a generation it follows the persons' OASDI receipts: employee and employer OASDI on their keys, plus 80.3% (se_oasdi_share) of the self-employment tax. Medicare's line has two parts. Its remaining benefits (the cash set's Medicare less the Part A share, 37.5%) follow the Medicare key, and the Part A accrual follows HI receipts (employee and employer HI plus the rest of the self-employment tax). The federal income tax loses the tax on current benefits, on the Social Security benefit key.
   - Why: the generation account (`v4_split.cjs`) sets each generation's accrual at its own accrual per tax dollar times its OASDI receipts, and gives a cell inside a generation its generation's ratio on the cell's own receipts. The pension lane's ratios are G1 1.077, G2 0.973 and G3+ 1.011, gross of the benefit tax. This carries the same rule down to the person. B keeps the accrual because it is the members' own claim, earned by their own contributions, as the current benefits it replaces were in B on September 27.
   - Gates: the generations' accruals add to ratio_net times the union's OASDI receipts ($109.406993bn / $102.754953bn), the Part A accruals to $41.137128bn and the benefit tax to $2.091206bn / $1.816900bn (1e-9bn). The set and the cash set differ in these three lines only.
   - Alternative, and why it matters: each worker's own accrual from the pension lane's person-level model (`pension_accrual_2026_09_28/pension_accrual.py` central_accrual). That model has two features the flat ratio drops. Benefits are progressive in earnings (Note 2025.7's ratio at the worker's career level, birth year and family type), so the flat ratio charges high earners too much accrual and low earners too little. And the unauthorized accrue at 10% of the rate (Note 151's long-run eligible share), so inside G1 the flat ratio charges unauthorized workers an accrual they will mostly not receive, and legal immigrants too little. Under that model, the education gradient in the shares would be steeper, the overall share probably a little higher (most net contributors are high earners), and unauthorized-headed households cheaper than shown [INFERENCE; not computed: the pension lane keeps no person-level accruals, and computing them means running its model grid on this frame]. G1's total does not move either way.
2. **Roads keyed by miles** (roads_vmt_sl, roads_vmt_fed). Each generation's line splits into the pieces of candidate v4's formula, highway national × (FP s_vmt + (1 − FP) k_cons − k_old). The driver-mile piece goes over members aged 5 and over at equal miles, the generation account's rule (`v4_inputs.py`). The freight piece follows the excise line's consumption key, and the old-key piece, negative, economic affairs' resources key. Gate: the freight piece's implied key equals the generation's excise share before the gasoline shift (1e-9). Alternative: the generation account's roads_by_population, per head with no age cut.
3. **State pricing** (state_price_public_order_safety, _health_services, _recreation_culture). Each line follows its parent line's split; public order's is per head and by use. The generation account prices each generation's gap as the union's index on the generation's own parent amount. Alternative: each member's own state index on their parent amount. It would move the charge toward high-price states such as California [INFERENCE]; the account carries no index by person.
4. **Public housing's deficit** (receipt housing_enterprise_surplus, $3.4bn): the housing-assistance key, as a transfer (in B), since it funds the recipients' units. Alternative: per head, like the enterprise surplus it is split from (A only).
5. **The tax on tenant-occupied housing** (receipt tenant_occupied_property, key renter_contract_rent, −$6.8bn). It goes to union members in homes rented for cash, each weighted by their state's group rent per such member on the row-4 weights. This is the generation account's rule carried to the person, and it is gated to that rule's generation shares (`v4_inputs.json` tenant_share, 2.2e-16). Alternative: the account's tenant_national, the same persons with no state weights.
6. **The owner-occupied property tax** (modeled_owner_property, now at response 0.763, −$19.0bn) and **the personal property tax** (capital key, −$1.3bn) use keys the lane already builds (`keys.py` owner_property and the CPS capital key). On row 4 the owner key is pinned for G2 and G3+ only, because the decomposition lane's row-4 age bins do not carry it.
7. **Part-rekeyed capital** (the highway components). The return splits in the proportions of the key's two parts (the adopted package's keyOf): the parent's part on economic affairs' key and the road line's part on its three pieces. Gate: the two parts add to the component's key (1e-12).
8. **Production.** The cell parts are solved on the row-4 labor shares, because the case puts the grid on row 4 and the generation account attributes it there (`v4_inputs.py`). The September 27 runs keep the published attribution. Residual 8.9e-16bn.

**The count.** No sept29 figure reads the published 40.9M frame. Every step uses the row-4 weights: the union count reproduces `headcount.csv` (39,712,493.331), the per-member figures divide by it, and the tenant key and the production labor shares use it. The per-head lines charge each generation the same per member (widest spread 7.5e-11). The 40.9M frame stands beside it as the September 27 case's published arm (`derived/`). One step still reads the published weights and moves no figure: the status imputation's count gate, since the flag itself does not use weights.

**Gates, printed in this run.**
- `export_lines.cjs --case sept29`: exit 0, 53 gates. The union reproduces the adopted band at specifications 48 / 11, 371.414600 / 434.840959 (tolerance 1e-4, the oracle's rounding), and the cash set 294.7010760 / 361.8174818 (1e-4). Each generation's rows add to `generation_results_sept29.csv` and `generation_results_sept29_cash.csv` (1e-6bn), and the generations add to the union (1e-9bn). The pension, road and capital gates are under the rules above.
- `households.py --case sept29 --weights row4`: exit 0. The union count matches (1 person), 90 key rows match (worst 5.8e-16 relative), and public order's per-head part moves as the engine's does (5.3e-8bn). The per-head lines charge each generation the same per member (7.5e-11) and the production cells close (8.9e-16bn). Each generation's pieces plus its residual equal its cost (1.1e-13bn). Households plus the residual reproduce the case, 1.5e-12 / 4.5e-13bn against a tolerance of 1e-6bn, and every replicate matches the full sample (6.8e-12bn). There is one reference person per household, and the status counts match.
- Old cases unchanged and repeatable: `scripts/rerun_lane.py` over the five commands, twice after the sept29 run, exit 0 and IDENTICAL, 21 of 21 files both times. The tracked files in `derived/` and `derived/row4/` equal HEAD.
- The six sept29 files and `_cache/sept29/lines.json` are byte-identical to the ones written before the reboot.

**Inputs not yet committed.** The generation account's v4 files, written by that lane and uncommitted at this run (sha256 prefixes): `generation_corrections_sept29.json` 818adc171564, `generation_corrections_sept29_cash.json` 50c3500e2a54, `generation_results_sept29.csv` d3c15b7cf47c, `generation_results_sept29_cash.csv` 1e7465f06809, `generation_summary_sept29.json` e2939a26d0b5, `v4_inputs.json` 31a77369be8b. If any of them changes before it is committed, rerun the two sept29 commands.

**Limits and what would change it.**
- The accrual convention is the case's; the cash set would charge retirees their benefits and leave workers' payroll taxes as contributions. This lane does not spread the cash set, though `_cache/sept29/lines.json` carries its pension amounts by generation. [FRAMING-SENSITIVE]
- The person-level accrual (rule 1) would move the education gradient and the status rows.
- The September 27 limits carry over:
  - justice by use follows generation and age, not individual offending;
  - the status-based corrections, and now the accrual, are spread over all Mexico-born persons by key;
  - the lane constants (−$5.2bn) are not assigned;
  - G1's split of Medicaid with uninsured use follows the published cells;
  - one year is not a lifetime.

**Files.** New: `derived/sept29/` (the six files) and `_cache/sept29/` (ignored). Changed: `export_lines.cjs` (the `--case` switch, capRule from the payload's meta.capital_return with a gate that it equals the capital lane's rules on September 27, and the sept29 splits) and `households.py` (`--case sept29`, the rules above).

**Log (sept29; times from `date` calls).**
- 20:58 JST — resumed after the reboot. The code (export_lines.cjs, households.py) and `derived/sept29/` (20:48) were in the working tree, uncommitted.
- 20:58–21:05 — reran `export_lines.cjs` (exit 0; `_cache/lines.json` byte-identical to the pre-reboot copy), `export_lines.cjs --case sept29` (exit 0, 53 gates) and `households.py --case sept29 --weights row4` (exit 0, 13 s). All outputs are byte-identical to the pre-reboot ones.
- 21:07–21:09 — `rerun_lane.py` pass 1: exit 0, IDENTICAL 21/21.
- 21:10–21:11 — `rerun_lane.py` pass 2: exit 0, IDENTICAL 21/21. `households.py --case sept29` without `--weights row4`: [BLOCKED], exit 1.
- 21:54–21:55 — after the RESULT and a docstring line in `households.py` (its sept29 run command), `rerun_lane.py` pass 3: exit 0, IDENTICAL 21/21.
