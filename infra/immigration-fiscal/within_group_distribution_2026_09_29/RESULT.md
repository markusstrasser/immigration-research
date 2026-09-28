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
```

Both scripts stop with exit 1 on a failed gate. Together they run in about ten seconds.

## Log

- 2026-09-29 00:21 JST — lane directory and stub created; reading generation_account_2026_09_24 and the main-case package.
- 2026-09-29 00:29 JST — export done
- 2026-09-29 00:31 JST — households.py runs: all gates pass (88 key rows reproduce generation_keys.csv, 5.8e-16; production cells close; each generation's pieces + residual = its cost; households + lane constants = 321.819357 / 387.370055). 7,106 households, 18,331 union person records; 1,433 households have a reference person outside the union.
- 2026-09-29 00:37 JST — rerun of both scripts (exit 0): the six derived CSVs and `_cache/lines.json` are byte-identical to the previous run (time from the `date` call made with the rerun).
- 2026-09-29 00:43 JST — since the 00:29 entry: households.py built and gated (keys, production cells, generation closure, households + lane constants = the case), spending categories set by key, the schools-per-head sensitivity and category means added, minor-only households headed by their reference person; RESULT.md written with the final numbers.

## Lead verification (2026-09-29 00:53 JST)

- Reran both scripts in place with `scripts/rerun_lane.py`: rc 0, 9 of 9 files byte-identical.
- The positive control (households plus the lane constants reproduce $321.8194bn / $387.3701bn) runs inside `households.py`, which exits 1 on any failed gate.
