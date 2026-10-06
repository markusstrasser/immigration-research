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
