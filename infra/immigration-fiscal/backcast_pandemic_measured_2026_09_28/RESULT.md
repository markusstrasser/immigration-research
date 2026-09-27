claude-opus-5-5

**Verdict:** The back-cast overcharged 2020–2021 by $123–133bn on the September 20 anchor. That is about a
third of what the memo's 2019/2022-mean row removes.

- **Payments.** CPS ASEC shows the group received the 2020 payments at **0.87 times other residents per
  person** under the statute's SSN rule (1.02 without it), and the 2021 payments at 1.03. The back-cast
  charged both years at the 2024 credit ratio of **2.34** (low end; 2.16 high).
- **Ten-year totals, September 20 anchor.** Programme rule: **$1.698tn → $1.564tn** (low) and **$1.979tn →
  $1.856tn** (high). Income rule: $1.966tn → $1.833tn and $2.235tn → $2.112tn.
- **Pandemic years' share.** It falls from 35.2–38.5% of the programme-rule total to 30.9–33.2%.
- **Adopted September 27 case** (the debt-legacy programme version). The cut is $37–49bn, to $2.606–2.987tn.
  - It is smaller because the September 24 corrections had already shrunk its 2024 credit line by a third.
  - The result lands within $1–9bn of the debt-legacy lane's "pandemic credits per head" sensitivity.
- **SSN exclusion.** The statute confirms the EIP1 exclusion, and it was wider than the memo says: the
  advance payment excluded every mixed-status joint return.
- **Other programmes.** SNAP, SSI and Social Security stay within 10% of their 2024 ratios in 2019–2023,
  except one noisy SSI cell. Unemployment ran 13–14% under its 2024 ratio in 2020 (z −1.5).
- **Workers' compensation.** The 2024 workers'-compensation key sits above all five earlier years. Averaging
  it over the six years would lower the 2024 account by $1.5–2.0bn.

# Measured pandemic years in the historical back-cast

Lane opened 2026-09-28 from `BRIEF.md` (commit 68a5d0a). Nothing outside this directory was edited. Nothing
was committed, staged or stashed.

## 1. The SSN rule, from the statutes

Checked against the enrolled public-law text on govinfo. The quotes are in `reads/quotes.json`, and
`verify.py` finds all 31 in the cached sources. "Valid identification number" means a Social Security number
in every round, so a filer with only an ITIN gets no payment of their own.

| Payment (national, NIPA year) | Rule for filers | Rule for children | Source |
|---|---|---|---|
| EIP1 advance, paid in 2020 ($274.7bn) | none if the filer, **or on a joint return either spouse**, lacks an SSN (military exception) | counted only with an SSN | CARES Act §2201, IRC 6428(g)(1); kept for advance refunds by CAA 2021 §273, 6428(g)(2) |
| EIP1 as a 2020 credit (the Recovery Rebate Credit, claimed in 2021) | joint return with one SSN spouse: $1,200 instead of $2,400 | counted if a parent and the child have SSNs | CAA 2021 §273, 6428(g)(1), "as if included in section 2201" |
| EIP2, paid Dec 2020–Jan 2021 | as the amended EIP1: $600 per SSN spouse | as the amended EIP1 | CAA 2021 §272, 6428A(g) |
| EIP3, paid 2021 | $1,400 per SSN spouse | any dependent with an SSN, whatever the parents' status | ARPA §9601, 6428B(e)(2) |

[SOURCE: Pub. L. 116-136 §2201; Pub. L. 116-260 div. N §§272–273; Pub. L. 117-2 §9601. The section 24(h)(7)
definition comes from Pub. L. 115-97 §11022 and requires an SSN issued to a citizen or a work-authorized
person. EIP3's own definition drops the work-authorization condition.]

The memo's sentence is right about EIP1 as paid, but it understates the exclusion. The first round
excluded every mixed-status joint return, including the SSN spouse and the US-citizen children. It did not
stop at households filing without SSNs. CAA 2021 restored the SSN spouse's $1,200 and the children's $500
only as a 2020 credit, paid in 2021.

The CPS cannot apply any of this directly. Census: "CPS ASEC lacks information on SSN, dependents who are
not resident in the household or don't have a parent pointer in the survey, and filing status for married
separate filers, all of which are known by IRS" [SOURCE: Census SEHSD-WP2021-18, PDF p. 11].

- **ASEC 2021 (income 2020).** `EIP_CRD` is the modeled sum of EIP1 and EIP2 at full take-up.
- **ASEC 2022 (income 2021).** `EIP_CRD` is EIP3.

[SOURCE: ASEC 2021 and 2022 data dictionaries; SEHSD-WP2021-18.] As released, the variable ignores the SSN
rule, so it gives an upper bound on the group's EIP share [INFERENCE]. Section 2 applies each payment's rule
per tax unit, with the Borjas residual standing in for "no SSN".

## 2. The group's measured shares, income 2019–2024 (task 1)

`measure_shares.py` reads ASEC 2020–2025 (income 2019–2024). It imports the account's union and sharing rule
(`canonical_target`, `equal_unit_share` from `full_account_spending_2026_09_20/builder.py`). It uses pwwgt0 and
the 160 replicate weights. It measures the account's keys: EITC plus ACTC for refundable credits, SNAP split
equally over the SPM unit, SSI, Social Security and unemployment compensation.

- **Local data.** ASEC 2022–2025 were local, in the files other lanes pinned. The dataset register lists
  ASEC 2022 onward. ASEC 2020 and 2021 were not local, so `acquire.py` pulled them from census.gov into
  `_cache/` (162MB and 169MB, pinned).
- **Gate against the account.** The ASEC 2025 run reproduces all 24 of the account's incidence keys that
  this lane shares with it, to 9.7e-17 [CALCULATION: `gate_account`].
- **Gate against the validation lane.** That lane gives every SPM-unit member the head's weight. With that
  weighting, the union's SNAP, Social Security and SSI dollars for 2021–2024 are reproduced to 5.6e-16
  [CALCULATION: `gate_validation`].
  - The account weights each person by their own weight, and this lane measures the shares that way.
  - The account's weighting gives shares 0.0–0.45 points above the validation lane's. [CALCULATION: union ÷
    (union + other) in `validation_fiscal_years_2026_09_28/derived/annual_components.csv`, compared with
    `measured_shares.csv`.]
- **Payments rebuilt.** Census's `EIP_CRD` is rebuilt exactly for every recipient unit before any SSN rule
  is applied. The rebuild uses the unit's filers, children under 17 (all dependents for EIP3), AGI and the
  statutory phase-outs.
- **SSN proxy.** The Borjas residual (`status_impute_2026_09_16/impute_status.py`, imported) stands in for
  "no SSN".
  - It places 4.3m of the group without an SSN in ASEC 2021 (11.9m nationally), and 4.5m (12.9m) in ASEC 2022.
  - The residual's spouse clause makes a citizen's spouse legal, so it creates no mixed-status couples.
- **Mixed-status bound.** The `borjas_own` treatment drops the spouse clause, which puts 5.2m of the group
  without an SSN. That is the bound for the EIP1 mixed-status exclusion.

Group share of national dollars, % (low-end, shared allocation). Standard errors and the personal allocation
are in `derived/measured_shares.csv`.

| Programme | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 |
|---|---:|---:|---:|---:|---:|---:|
| Population (civilian household) | 11.67 | 11.89 | 11.78 | 11.83 | 11.94 | 12.15 |
| Refundable credits (EITC + ACTC) | 25.96 | 25.63 | 18.25 | 24.85 | 24.81 | 24.46 |
| EIP1 advance, Census model / SSN rule | | 12.08 / 10.50 | | | | |
| EIP2, Census model / SSN rule | | 13.00 / 11.27 | | | | |
| EIP3, Census model / SSN rule | | | 13.63 / 12.49 | | | |
| SNAP | 14.89 | 14.82 | 14.96 | 15.31 | 15.21 | 14.81 |
| SSI | 8.19 | 8.10 | 7.30 | 8.76 | 8.27 | 8.23 |
| Social Security | 4.48 | 4.35 | 4.06 | 4.49 | 4.15 | 4.38 |
| Unemployment compensation | 12.20 | 9.83 | 10.73 | 12.98 | 13.34 | 11.60 |

[DATA: CPS ASEC 2020–2025 public use; CALCULATION: `derived/measured_shares.csv`. Standard errors, in points:
population 0.10–0.13; credits 0.28–0.72; payments 0.10–0.14; SNAP 0.51–0.80; SSI 0.61–0.82; Social Security
0.13–0.15; unemployment 0.39–1.63.]

The pandemic payments went to the group at about its population share:

- **EIP1, Census model.** Before any SSN rule, EIP1 reached the group at 1.02 times other residents per
  person (0.98 at the high end).
- **EIP1, SSN rule.** The rule lowers that to **0.87** (0.83 high). Excluding mixed-status joint returns
  as well (`borjas_own`) gives 0.80.
- **2021 payments.** They reached the group at 1.03 (0.97 high). They are weighted by their CPS national
  amounts: EIP2 and the EIP1 catch-up on income-2020 units, EIP3 on income-2021 units. EIP3 counted every
  dependent with an SSN, and the group has more children [INFERENCE].
- **What the back-cast charged.** Both years at the 2024 credit ratio, **2.34** times other residents
  (2.16 high).

[CALCULATION: `derived/eip_relative_use.csv`, column `per_person_vs_other_residents`.]

The 2021 credit share (18.25%) is the fully refundable child tax credit, which ASEC 2022 carries in `ACTC_CRD`
[SOURCE: ASEC 2022 data dictionary]. It reached many families outside the group.

## 3. The back-cast with the pandemic years measured (task 2)

`backcast_measured.py` first rebuilds the programme back-cast. It uses `historical_backcast_2026_09_20`'s own
helpers and pinned workbooks for the national indexes and the population-share path. It edits nothing in
that lane. Before any change, it checks three reproductions:

- the published transfers, within 6e-5bn;
- the published ten-year windows, within 1e-4tn;
- the debt-legacy annual gaps, which add to that lane's windows within 1e-5tn.

The back-cast holds each line's relative use (group share over population share) at 2024. The replacement
swaps in the measured relative use on the same key and allocation. The population path and every 2024
anchor stay as they were. In 2020 and 2021 the refundable-credit line is split into two parts. The line is
$430.7bn and $856.6bn in those years [DATA: NIPA 3.12 line 25, data published September 26, 2025].

- **The payments.** BEA puts them at $274.7bn and $569.2bn [SOURCE: BEA, "Effects of Selected Federal
  Pandemic Response Programs on Personal Income", 2022Q4 third, annual line 31]. They take the group's
  measured relative use under the SSN rule.
- **The rest of the line.** It keeps the account's credit key, at that income year's measured relative use.

Ten-year totals, 2015–2024, $tn in 2024 dollars. "New" uses the Borjas SSN rule. The range runs from
excluding mixed-status couples (`borjas_own`) to the Census model with no SSN rule:

| Anchor | End | Rule | Old | New (range) | Pandemic years' share, old → new |
|---|---|---|---:|---:|---|
| Sept 20 main (CBO-informed) | low | programme | 1.698 | 1.564 (1.562–1.578) | 38.5% → 33.2% |
| | low | income | 1.966 | 1.833 (1.830–1.846) | 35.4% → 30.7% |
| | high | programme | 1.979 | 1.856 (1.853–1.870) | 35.2% → 30.9% |
| | high | income | 2.235 | 2.112 (2.110–2.126) | 33.0% → 29.1% |
| Sept 27 adopted, debt-legacy programme version (cash) | low | programme | 2.655 | 2.606 (2.603–2.619) | 30.0% → 28.7% |
| | low | income | 2.897 | 2.848 (2.845–2.862) | 28.9% → 27.6% |
| | high | programme | 3.024 | 2.987 (2.984–3.001) | 28.3% → 27.4% |
| | high | income | 3.253 | 3.216 (3.214–3.230) | 27.4% → 26.5% |

[CALCULATION: `derived/backcast_measured_windows.csv`, variant `refundable_pandemic`.]

- **Longer windows.** The fifteen- and twenty-year windows fall by the same amounts. For example, the
  September 20 low-end programme rule goes from $2.738tn to $2.605tn over 2005–2024.
- **Full proportional services.** Programme rule: $2.639–2.800tn → $2.506–2.677tn. Income rule:
  $2.907–3.056tn → $2.774–2.933tn.

The September 20 cut is $133bn at the low end and $123bn at the high end, all of it in 2020–2021.

- **Payments: −$119bn (low end).** The back-cast attributed $230.7bn; the measurement gives $112.1bn. Without
  the SSN rule the cut would be $105bn. The rule therefore accounts for about a tenth of the payment cut, and
  pricing per head accounts for the rest.
- **Rest of the line: −$15bn.** That is −$18bn in 2021, where the fully refundable child credit lowered the
  group's key, and +$3bn in 2020.
- **High end.** Payments −$110bn and the rest −$13bn.

[CALCULATION: `derived/credit_line_parts.csv`.]

The same comparison against the alternatives already in the record (ten years, programme rule, $tn):

| Treatment of 2020–2021 | Sept 20 low | Sept 20 high | Sept 27 low | Sept 27 high |
|---|---:|---:|---:|---:|
| 2024 ratio (published) | 1.698 | 1.979 | 2.655 | 3.024 |
| Measured (this lane) | 1.564 | 1.856 | 2.606 | 2.987 |
| Credit excess over the 2019–2023 trend per head (debt legacy) | | | 2.607 | 2.996 |
| Both years at the 2019/2022 mean | 1.318 | 1.616 | 2.330 | 2.722 |

[DATA: `historical_backcast_2026_09_20/derived/backcast_categories_windows.csv`, rule `programme_ex_pandemic`;
`debt_legacy_2026_09_23/derived/adopted_backcast_windows.csv`, receipts `own_series`, rules
`programme_pandemic_per_head` and `programme_ex_pandemic`.]

- **The 2019/2022-mean row.** It removes $0.36–0.38tn on the September 20 anchor and $0.30–0.32tn on
  September 27. The measurement removes a third of that on the first anchor and a seventh on the second. The
  payments were real transfers, and the group got roughly its population share of them.
- **The per-head sensitivity.** The debt-legacy lane's version puts the 2020–2022 credit excess over the
  2019–2023 trend per head. It lands within $1bn (low) and $9bn (high) of the measurement. That lane expected
  per head to run "slightly high" because of the first round's SSN rule. The measurement agrees for 2020, when
  the payments reached the group at 0.87 per person, but the 2021 payments reached it at 1.03.
- **Why the September 27 cut is smaller.** The cut is −$49bn (low) and −$37bn (high). The September 24
  corrections had already lowered that case's 2024 credit line to $36.3bn and $32.6bn, against $55.4bn and
  $52.1bn. Premium tax credits are no longer keyed as EITC, and the EITC takes Treasury's shares over the
  audit's SSN rule. The old attribution of the payments was smaller to begin with, while the measured
  payments do not depend on the 2024 credit key. [SOURCE: `decisions/2026-09-24-main-case-audit-and-outside-checks.md`;
  DATA: `main_case_long_run_2026_09_27/derived/corrections.json`, refundable line −$19.07bn shared / −$19.51bn
  personal; `debt_legacy_2026_09_23/derived/federal_split_2024_lines.csv`.]
- **Payment timing.** NIPA records credits in the year they are paid. The `refundable_payment_timing`
  variant keys the rest of the line by the tax year paid:
  - 2020 takes the 2019 key;
  - 2021 takes the 2020 key, with the advance child credit ($98.3bn) at the 2021 key;
  - 2022 takes the 2021 key.

  This takes a further $3–4bn out of the ten-year total on September 20 and $2–3bn on September 27.
- **Every measured line, 2019–2023.** The `all_measured` variant replaces every CPS-keyed benefit line in
  all five years. The totals barely move: $1.564tn and $1.851tn (programme), $1.832tn and $2.107tn (income).
  The two sides cancel:
  - The credit key's higher ratios in 2019, 2022 and 2023 add $10bn.
  - Unemployment (−$10bn low, −$13bn high) and workers' compensation with temporary disability (−$11bn and
    −$9bn) take out about as much, net of rises in SNAP, cash assistance and other lines.

  [CALCULATION: `derived/line_paths.csv`.]

## 4. Other lines against the 2024 ratio (task 3)

`derived/ratio_vs_2024.csv` gives each CPS key's relative use in 2019–2023 over its 2024 value, for both
allocations. The standard errors treat the two survey years as independent. That overstates them, because the
CPS sample overlaps in adjacent years.

The table lists cells more than 10% from 2024, as ratio shared / personal with z. The dollar figures are the
September 20 account's 2024 lines on each key, $bn low / high.

| Key (account lines) | Cells beyond 10% | Reading |
|---|---|---|
| Refundable credits, EITC + ACTC (55.4 / 52.1) | 2019: 1.10 / 1.13 (z 3.0 / 3.2); 2021: 0.77 / 0.77 (z −10.9 / −9.3) | 2021 is the child-credit expansion; 2019 is a real, higher share |
| Unemployment (4.2 / 4.1) | 2020: 0.87 / 0.86 (z −1.5 / −1.4); 2021 high 0.88; 2022: 1.15 / 1.14; 2023: 1.17 / 1.14 (z ≤ 1.1) | pandemic benefits reached the group less per head; within 1.5 SE |
| Workers' compensation, temporary disability, black lung (5.5 / 4.8) | every year: 0.42–0.68 / 0.47–0.84 (z to −4.8 / −3.3) | the 2024 value is the outlier |
| Veterans' pension, readjustment, life insurance (12.4 / 9.6) | 2019: 1.23 / 1.30; 2020 low 0.83; 2021: 0.75 / 0.81 (z −2.2 / −1.2); 2022 low 0.88 | noisy (relative SE 11–16%) |
| Cash assistance (11.0 / 10.4) | 2020 high 1.11; 2021: 1.20 / 1.15 (z 0.5–1.0) | noisy (relative SE 11–17%) |
| All cash, keying other federal benefits (4.2 / 3.9) | 2020: 1.15 / 1.18 (z 3.5 / 3.8) | unemployment was a large part of all cash in 2020 |
| WIC, keying other state welfare (5.1) | 2019: 1.17 (z 2.0) | |
| Energy (0.6) | 2021: 0.68 (z −2.9); 2023: 0.84 | |
| SSI (5.3) | 2022 high only: 1.11 (z 0.7) | otherwise within 10% |
| SNAP (14.3), Social Security (63.4 / 60.5) | none | SNAP +2% to +6%, Social Security −6% to +6.5% |

- **Workers'-compensation anchor.**
  - The key's relative use in 2019–2023 is 1.10, 0.76, 1.23, 0.76 and 1.15 (low end), against 1.80 in 2024.
    That flags the account's 2024 anchor rather than the back-cast.
  - With the six years averaged, the 2024 account's three lines would be $2.03bn lower at the low end and
    $1.54bn lower at the high end. The adopted case carries the same three lines ($5.41bn and $4.84bn).
  - [CALCULATION: `ratio_vs_2024.csv`, `account_2024_change_if_pooled_bn`; INFERENCE that 2024 is sampling
    noise, from its z against 2020 and 2022.]
  - No other key moves the 2024 account by more than $0.6bn on this test.
- **Other federal benefits, 2020.**
  - NIPA 3.12 line 26 tripled in 2020, from $61.5bn to $191.7bn.
  - Three lines of the BEA table account for $128.1bn of that $130.2bn rise: FEMA's lost-wages supplemental
    payments ($35.5bn), Paycheck Protection loans to nonprofits ($41.5bn) and the Provider Relief Fund to
    nonprofits ($51.1bn). [SOURCE: BEA table above, annual lines 32–34 and note 7.]
  - That money is not household cash. The account keys the line by all cash, and a measured all-cash share
    cannot fix that composition. It is left as is.

## 5. Limits

- **SSN proxy.** The CPS has no SSN field, so the Borjas residual stands in for "no SSN". Its Medicaid
  clause treats California's status-blind Medicaid enrollees as legal. The SSN-rule shares are therefore,
  if anything, high. The Census-model and `borjas_own` columns bound the treatment.
- **Weights.** ASEC 2020 and 2021 are used with the replicate weights released in their public-use CSV
  files. Census also posted replicate-weight files on 2020-census population controls
  (`CPS_ASEC_ASCII_REPWGT_2020_2020BASE`, `CPS_ASEC_ASCII_REPWGT_2021_2020BASE`), which this lane does not
  use. Relative use divides a share by the same file's population share, so it cancels a level shift but not
  a change in composition.
- **Vintages.** The payment amounts are BEA's March 2023 vintage. Line 25 is the September 2025 vintage the
  back-cast pins, so any later revision of the payments lands in the rest of the line.
- **The credit key's path.** The rest of the credit line moves with the relative use of the status-blind
  Census credit key from year to year. The adopted case corrects that key's 2024 level, not its path.
- **Scope.** Only the programme-by-programme rule is re-run.
  - The memo's headline, $2.8–3.7tn over 2015–2024 on the September 27 anchor, uses the whole-budget rules.
    They carry 2020–2021 through national spending per head and are untouched here.
  - Only CPS benefit keys are measured by year. The medical keys (Medicaid, Medicare, TRICARE, VA medical,
    other health), the age keys, the school mix and the resource keys stay at their 2024 relative use.

## Reproduce

From the repository root; outputs rerun byte-identical (`verify.py`):

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/acquire.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/measure_shares.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/backcast_measured.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/backcast_pandemic_measured_2026_09_28/verify.py
```

`derived/`:

- `measured_shares.csv`: every key × allocation × income year, with SSN treatments for the payments.
- `survey_audit.csv`: union and no-SSN counts.
- `eip_relative_use.csv`.
- `backcast_measured_annual.csv` and `backcast_measured_windows.csv`: all anchors, rules and variants.
- `line_paths.csv` and `credit_line_parts.csv`.
- `ratio_vs_2024.csv`.
