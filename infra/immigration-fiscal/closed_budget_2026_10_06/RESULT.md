claude-opus-5-5

**Verdict:** If the lineage pays its share of the permanent fix that stabilises federal debt, other residents pay **$354.6–425.6bn** a year on main case v5 instead of $390.3–461.2bn (−9.1% / −7.7%). The fix is Auerbach & Gale's 2026 current-law gap less the Social Security and Part A shortfall the account already treats as cut to payable benefits, split equally by household (AEI's own rule). Across the current-law gaps and six sharing rules the range is $343.1–449.5bn. Beside the headline, never in it. [FRAMING-SENSITIVE]

Written 2026-10-07 01:35 JST.

## The question

The adopted case is current law, and current law does not close the federal budget. So the headline counts the whole of the group's net cost as falling on other residents, including the part financed by borrowing that everyone's future taxes will repay. Orrenius, Viard & Zavodny (AEI, September 2025, p. 11) argue that each household that joins the population carries part of the tax rises or spending cuts that must eventually close the fiscal gap, so an account that ignores this overstates the burden on everyone else. This lane prices that argument.

With F the permanent yearly improvement in the primary balance that closes the gap with the group present, and s the group's share of it:

    cost to others on a closed budget = G − s·F

G is the case's net cost ($390.3–461.2bn; cash set $307.4–383.4bn).

## Results (2024 dollars, per year)

| Reading | Main case | Cash set |
|---|---|---|
| Headline: others carry the group's share of the deficit | 390.3–461.2 | 307.4–383.4 |
| **Central: Auerbach–Gale 2026 current law, general fund, per household** | **354.6–425.6** | **271.7–347.7** |
| Current law: two gaps × six rules × two readings | 343.1–449.5 | 260.2–371.9 |
| Current policy: three gaps × six rules | 278.3–451.1 | 195.4–373.4 |
| AEI as published (2013 infinite-horizon gap 4.23%, per person, scheduled benefits) | 232.4–303.3 | 149.5–225.5 |
| Every resident's whole 2024 account deficit shared per head (ladder 269's excess over average residents) | 280.5–297.4 | — |

The central fix is $370.1bn a year: 2.33% of GDP less 1.07 points of post-depletion OASDI shortfall on CBO's reading (HI is not exhausted inside CBO's window), times 2024 GDP. The group's household share is 9.64% (per person 12.74%), so it carries $35.7bn.

The last row is the limiting case: if the whole 2024 deficit in the account's own frame, not just the permanent fix, were shared per head, the group's cost to others would be its excess over average residents, which the case already prints. The closed budget lies between that and the headline because the permanent fix is far smaller than the account's 2024 deficit.

## Inputs: measured and assumed

Measured or published:
- G: the case's ends (`main_case_2026_10_05/derived/summary.json`).
- Published gaps (`sources.json`, each quoted from its staged PDF):
  - Auerbach & Gale 2026: 2.33% current law, 3.43% current policy, debt held at 99% of GDP in 2056.
  - CBO's letter of 24 September 2026: 1.9 points.
  - Treasury FY2025 Financial Report, 75 years: 4.7%, or 2.4% with discretionary spending growing with inflation and population.
  - AEI's 2013 figure (4.23%), reported as published only.
- Trust-fund shortfalls: parsed by `trust_funds.py` and gated against the reports' payable percentages (83% OASDI at 2034; HI 89% at 2033, 93% at 2100).
  - 2026 OASDI Trustees Table IV.B3.
  - 2026 Medicare Trustees Tables III.B7 × V.B2.
  - CBO 62044 sheet 1a.
- Household share: CPS ASEC 2025 household weights, each member scaled by audit row 4's reweight, on the decomposition's frame (`households.py`). Lineage households average 3.30 people against 2.49 overall.
- Federal tax mix: OMB Historical Table 2.1, FY2024. GDP: BEA NIPA T1.1.5, $29.30tn.

Assumed:
- The sharing rule. Six rules are run: per person, per household, federal benefits cut in proportion, all taxes, federal income and payroll taxes, income tax alone. The central uses AEI's own household rule.
- That the fix is permanent and falls on the 2024 population in 2024 proportions. A fix that phases in later falls more on future cohorts, among whom immigrant lines are over-represented (Auerbach & Oreopoulos 2000).
- Depletion-year fractions (OASDI 2034 Q3 → 0.375 of the year after depletion; HI 2033 Q2 → 0.625; CBO year → 0.5) and a simple mean over the window (r = g; r − g = 1 point is in `trust_funds.json` and moves the shortfall by about 0.05 points).
- The 75-year gaps net the Trustees' 75-year unfunded obligations (OASDI 1.5%, HI 0.2% of GDP).

## Why the general-fund version

Every published gap pays scheduled Social Security and Part A benefits after the trust funds run out. Since 2026-09-29 the account values the promises members earn at the benefits current law can pay (`pension_accrual_2026_09_28`). For the account, those funds are therefore already closed, and charging the group a share of the cost of paying scheduled benefits would count a benefit the account does not give. The "as published" rows are in `derived/closed_budget.csv` for comparison. They lower the cost further: $324.5–395.5bn at Auerbach–Gale current law (2.33% of GDP, $682.7bn) per household.

## Gates (all pass; `derived/audit.json`)

- The decomposition's parts add to the case at both ends in both sets.
- Identity control: the per-person rule with F set to the case's own average-resident gap reproduces the printed excess over average residents, $280.5 / 297.4bn (ladder 269).
- The household share is computed on the decomposition's frame (NG 42,752,212.9, NC 335,543,722.2).
- Every share lies in (0, 1), every general-fund gap is positive, and cost falls as the fix rises.
- `test_closed_budget.py`: six tests (rows are G − s·F, general-fund gaps net the trust funds, monotone in F, household below per person, gates, summary matches the CSV).

## What this is not

- A forecast that the fix will happen, or of who will carry it. Current law first: the headline stands as the current-law statement, and this is an arm.
- A removal path. It is a sharing rule on the stationary 2024 account.
- A statement about state and local budgets. Most of the group's cost falls on them, and they balance each year, so other residents pay those costs now and no federal fix shares them. In the debt-legacy lane's v5 split (`debt_legacy_2026_09_23/derived/oct05/federal_split_2024.csv`, central convention), the federal part of the 2024 cash gap is $32.4 / 61.2bn (12.4% / 19.6%) against $228.3 / 251.1bn state and local. The pension accrual ($82.9 / 77.8bn) is federal and falls due later.

## Reproduce

From the repository root, in order:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/households.py
    uv run --no-project --with openpyxl python3 infra/immigration-fiscal/closed_budget_2026_10_06/trust_funds.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/closed_budget.py
    uv run --no-project python3 -m pytest infra/immigration-fiscal/closed_budget_2026_10_06/ -q

## v6 case (oct07), 2026-10-07

claude-opus-5-5 (teammate prop-b of the v6 consumer lanes). [2026-10-07: on main case v6 (`oct07`,
`../main_case_2026_10_07/`, adopted 2026-10-07) other residents pay **$357.1–429.5bn** a year on a closed budget,
against the case's $389.1–461.5bn (−8.2% / −6.9%); cash set $275.4–353.4bn against $307.4–385.4bn. The central is as
on v5: Auerbach & Gale's 2026 current-law gap, general fund on CBO's reading, split equally by household. It is now
netted of current law's separate OASI and DI funds, which v6's pension accrual uses. On v5 the central was
$354.6–425.6bn.] [CALCULATION: `closed_budget.py --case oct07` → `derived/oct07/summary.json`]

**What moved, oct05 → oct07, central ($bn, low / high):**

| Step | Cost to others |
|---|---:|
| v5 (oct05) | 354.6 / 425.6 |
| v6's items move the case (G) | −1.2 / +0.2 |
| the trust funds on separate funds (the switch) | +3.6 / +3.6 |
| the household share at the added people's measured ages | +0.1 / +0.1 |
| v6 (oct07) | 357.1 / 429.5 |

- **The switch to separate funds** (the brief's recommendation, current law first). Before v6 the general-fund fix
  netted the pooled OASDI fund's post-depletion shortfall from 2034 Q3. v6's pension accrual is on the 2026 Trustees'
  separate funds, where OASI is depleted in 2032 Q4 and DI pays in full through 2100 (TR2026 Table II.A1). So the fix
  now nets OASI's own shortfall from 2032 Q4 [DATA: `derived/trust_funds_separate.json`, `trust_funds.py`]:
  - over 2027–2056 on CBO's reading the netted component rises from 1.0667% to 1.1940% of GDP (Trustees' reading
    1.1282% → 1.2374%);
  - on CBO's reading the component is CBO's Social Security outlays less revenues plus the Trustees' DI balance (OASI's
    own deficit), from the Trustees' OASI date [APPROX: CBO's 2026 workbook has neither the funds' split nor an OASI
    date];
  - over 75 years, OASI's open-group unfunded obligation is $30,297bn over the present value of GDP, $1,978.4tn:
    1.531% of GDP (TR2026 Table IV.B8; pooled 1.481%).

  The central fix falls from $370.1bn to $332.9bn ((2.33 − 1.194)% × $29.30tn). At the household share of 9.605% the
  group's offset falls by $3.58bn, and the cost to others rises by the same at both ends (`summary.json`
  `pooled_funds_arm.switch_bn`). On the pooled funds v6's central would be $353.5–425.9bn and its current-law range
  $341.9–449.8bn.
- **The household share** [ASSUMPTION: the added people live in households of the identified G3+ records of their own
  ages]. v5 placed the 3.04M added people on the identified third-plus records in proportion, at that group's ages.
  v6 prices them at their measured age mix, so `households.py --case oct07` tilts each record's added weight by its
  five-year band's share of the added people over its share of the identified G3+, as the white lane's `age_tilt()`
  does. The share moves from 0.096365 to 0.096051 (householder rule 0.091301 → 0.090650), with 3.308 persons per
  lineage household against 3.297 (`derived/oct07/household_share.json`). The later losses are younger and live in
  larger households.
- **The excess over average residents** (the limiting case) is pinned at $284.1 / 302.5bn, one decimal. It is the
  decomposition's oct07 parts beyond the shared one, age structure, taxes and service use (Shapley), 284.130103 /
  302.548443, which is v6's band less the shared part, 104.952450 / 158.931266
  (`../main_case_decomposition_2026_09_29/derived/summary_oct07.json`, `parts`). On v5 it was $280.5 / 297.4bn
  (ladder 269).

**Every sharing rule on oct07** (Auerbach & Gale 2026 current law, general fund, CBO reading, F = $332.9bn; $bn, low /
high):

| Rule | Share (low / high) | Main case | Cash set | v5 main case |
|---|---|---:|---:|---:|
| per_household (central) | 0.0961 | **357.1 / 429.5** | 275.4 / 353.4 | 354.6 / 425.6 |
| per_person | 0.1274 | 346.7 / 419.1 | 265.0 / 343.0 | 343.1 / 414.1 |
| federal_benefits | 0.1058 / 0.1015 | 353.9 / 427.7 | 279.4 / 358.3 | 351.2 / 423.7 |
| all_taxes | 0.0751 / 0.0707 | 364.1 / 438.0 | 282.6 / 362.1 | 362.5 / 434.9 |
| federal_taxes | 0.0697 / 0.0638 | 365.9 / 440.2 | 284.4 / 364.3 | 364.4 / 437.4 |
| income_tax | 0.0545 / 0.0491 | 371.0 / 445.1 | 289.5 / 369.3 | 370.1 / 442.9 |

| Reading | Main case | Cash set | v5 main case |
|---|---|---|---|
| Headline: others carry the group's share of the deficit | 389.1–461.5 | 307.4–385.4 | 390.3–461.2 |
| Current law: two gaps × six rules × two readings | 346.7–451.4 | 265.0–375.4 | 343.1–449.5 |
| Current policy: three gaps × six rules | 278.3–451.9 | 196.6–375.9 | 278.3–451.1 |
| AEI as published (per person, scheduled benefits) | 231.2–303.6 | 149.5–227.5 | 232.4–303.3 |
| Every resident's 2024 deficit shared per head (the excess over average residents) | 284.1–302.5 | — | 280.5–297.4 |

[CALCULATION: `derived/oct07/closed_budget.csv`, `derived/oct07/summary.json`]

The federal share of the group's 2024 cash gap is still small. In the debt-legacy lane's v6 split
(`../debt_legacy_2026_09_23/derived/oct07/federal_split_2024.csv`, central convention), it is $34.0 / 63.8bn (13.0% /
20.3%) against $227.3 / 251.2bn state and local. The pension accrual, $81.7 / 76.1bn, is federal.

**Gates** (`derived/oct07/audit.json`, 9, all pass; the run stops on any failure):
- the case's ends are the adoption's bands to 6 decimals, 389.082553 / 461.479709 and 307.399411 / 385.364123
  (1e-6);
- the decomposition's oct07 parts add to the case at both ends in both sets (1e-4, the CSV's rounding);
- per_person at the case's own gap reproduces the pinned excess, 284.1301 / 302.5484 against 284.1 / 302.5;
- the household share is on the decomposition's frame (NG 42,752,212.9, NC 335,543,722.2);
- the trust-fund gates of `trust_funds.py` all hold on the separate funds:
  - OASI's and DI's income less cost equals their balance;
  - OASI plus DI equals OASDI (±0.011);
  - OASI's 2032 payable share is within a point of 78% (Table IV.B3 gives 78.8%).

The v5 outputs are unchanged: `households.py`, `trust_funds.py` and `closed_budget.py` rewrite every tracked file
byte for byte. `test_closed_budget.py` runs its six checks on both `derived/` and `derived/oct07/`: 12 passed.

Reproduce, after the decomposition lane's oct07 run:

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/households.py --case oct07
    uv run --no-project --with openpyxl python3 infra/immigration-fiscal/closed_budget_2026_10_06/trust_funds.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/closed_budget_2026_10_06/closed_budget.py --case oct07

Log (append-only; times from `date`):
- 2026-10-07 15:09:35–15:09:39 JST: `households.py --case oct07`, `trust_funds.py` and `closed_budget.py --case oct07`
  run on the adopted case (218a2fb2) and the decomposition's oct07 files of 15:04. Their sha256 values were checked
  again at 15:11:35 (summary_oct07.json edcb7cb3…).
- 15:11:35: the band gate was added and both cases were rerun; 9 gates pass and v5's files are byte-identical.
- 15:11:35–15:11:43: `rerun_lane.py` over households (both cases), trust_funds, closed_budget (both cases) and
  `test_closed_budget.py`: IDENTICAL 20/20, exit 0. Not committed (the lead's brief).
- 15:14:28–15:14:37: after the excess comment was re-sourced to `summary_oct07.json` (prop-a's rerun IDENTICAL 51/51,
  15:03:57–15:04:25), `rerun_lane.py` over the same six commands: IDENTICAL 20/20, exit 0. The case-lane hash recorded
  in `derived/oct07/audit.json` (summary.json 54709259…) is the committed file's.
