# Lane brief: who among other residents gains and loses, and the income-weighted net

Operator request (2026-09-23): "if renters->owners ... it might stay within the native
population but is a regressive money transfer from poor to rich ... we should mention or model
these dynamics ... Also for other domains/areas?"

## Frame (do not change)

The [complete annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
measures the annual 2024 effect of the 40.896574m CPS Mexican-origin residents on all **other**
US residents, stationary and with and without the group, counting a dollar as a dollar
(fiscal weight 1). The [real-costs memo](../../../research/immigration-real-fiscal-and-social-costs-2026-09-23.md)
adds priced channels beside it. **Do not re-estimate any channel's total.** Take each total as
given, divide it among other residents by income, and then weight.

## Task

1. **Income frame.** On CPS ASEC 2025 (income year 2024), use the account's archive and
   canonical target (`../full_account_spending_2026_09_20/builder.py` `canonical_target`; the
   archive in `../gen_ledger_extension_2026_09_16/_cache/`, sha-gated). Rank **other
   residents**, person-weighted, into quintiles of equivalized household income. The central
   measure is SPM resources ÷ the SPM unit's equivalence scale, or household money income
   ÷ √size; report the other as a check. Persons in a household with target members keep
   their own place, but only non-target persons count. Report each quintile's mean
   equivalized income ȳ_q and the overall mean ȳ.
2. **Divide each channel among the quintiles**, in $bn a year, with signs from other residents'
   point of view:
   - **Wages.** Use `../wage_distribution_2026_09_23/` and its source grid
     `../production_nativity_nest_2026_09_22/derived/nest_scenarios.csv`. Apply each skill
     cell's wage change to each other-resident worker's earnings in that cell, with the
     branches' cell definitions for each split. Central: long run, ε = ∞, below-BA split,
     σ = 2. Report the min and max over splits and σ, and the ε = 3 case. The capital part
     is zero in the long-run primary case. The short run, fixed capital, is a labelled
     sensitivity with capital income by quintile.
   - **Rents.** Use `../housing_transfer_2026_09_23/`. Other renters' extra contract rent (long
     run central, and the range) is spread by each renter household's contract rent. Use
     ACS 2024 PUMS: `HINCP`/`NP` equivalized, `RNTP`, and the lane's metro exposure. Landlords'
     receipts are divided on two ranged keys: ACS `INTP` (interest, dividends and net rental
     income) by quintile, and SCF 2022 other-residential-real-estate holdings by income. The
     housing lane holds the SCF extract (`../housing_transfer_2026_09_23/_cache/scfp2022s.zip`). Carry the housing net gain (+$0.7–3.5bn) to
     landlords. Owner-occupiers' value gain is a stock: report it by quintile, but not in
     the annual flow.
   - **Crime victims' harm.** Split the $28.9bn central and the $15.4–45.3bn envelope from
     `../crime_victim_cost_2026_09_23/` by victims' household income, using the NCVS
     violent-victimization rates by household income from the published BJS tables for
     2022–2024. Record the table and cells. The ranking is victims' household income, which
     is not the CPS measure; state the mapping.
   - **The fiscal net cost ($165.1–197.4bn)**, as imposed incidence under two stated
     conventions: (a) financed in proportion to all taxes paid (federal, state and local) by
     quintile; (b) financed by per-person service cuts. For federal taxes cite CBO's latest
     distribution of household income tables; for state and local, ITEP *Who Pays?* (7th
     edition) or the CPS tax fields. The old
     [who-pays lane](../gap_incidence_2026_09_18/) has conventions you may reuse, but its
     totals are superseded; see `research/immigration-fiscal-gap-incidence-who-pays-2026-09-18.md`.
   - **Uncompensated care** (`../uncompensated_care_2026_09_23/`): the unreimbursed part is
     split by private insurance coverage, and the under-charged public part by (a) or (b)
     above.
   - **Consumer prices, a side view only.** The account's production model has one good, so
     the wage and capital changes are its complete incidence. The CEX quintile split of the
     consumer-price gain
     (`research/immigration-consumer-price-and-native-hours-2026-09-18.md`;
     `../consumer_price_benefit_2026_09_18/derived/partA_price_results.csv`) overlaps them. Show it as an alternative lens, never added.
3. **Weights.** For each channel and in total, compute the equity-weighted net
   Σ_q (ȳ_q/ȳ)^(−η) × Δ_q for η = 0, 1, 1.3 and 2; at η = 0 it equals the unweighted sum.
   Cite the primary guidance for the η values: UK HM Treasury *Green Book* on the elasticity
   of marginal utility, and US OMB Circular A-4 (2023 revision) with its later status.
   Read both documents; do not rely on this brief for the values.
4. **Report the regressivity plainly.** For each channel give the share of losses borne by
   the bottom two quintiles and the share of gains to the top two. Give per-household
   dollars by quintile.

## Positive controls

- CPS: other residents total 336.727803m − 40.896574m within CPS, and the canonical-target
  gate from `builder.py`.
- Every channel's quintile split sums back to its given total within rounding (gate).
- At η = 0 the weighted total equals the unweighted sum (gate).

## Output

- `derived/`: the channel × quintile matrix ($bn), per-household dollars, weights, and
  weighted totals by η.
- `RESULT.md` opening with `**Verdict:**`: which channels are regressive or progressive and by
  how much, and the weighted net at each η beside the unweighted one. Then method, sources,
  limits (imposed incidence, income mapping, victim-income proxy) and a "Covered / skipped"
  list with reasons.

## Rules

- Run from the repository root: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`.
  Read the ZIPs in chunks, keeping only the needed columns.
- Tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`, `[INFERENCE]`, `[UNVERIFIED]`
  and `[FRAMING-SENSITIVE]`. The choice of η is a value judgment; show every value.
- The Census API key is in `infra/immigration-fiscal/acquire/config.local.env`. Never print
  it; pipe output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
- Edit nothing outside this directory. Do not commit. Return the RESULT.md path and at most
  10 lines.
