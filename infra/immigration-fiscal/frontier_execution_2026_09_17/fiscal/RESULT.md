# Fiscal interpretation and conditional thresholds

**Verdict:** The held extended account's group differences reconcile. They remain differences in a partial modeled annual account, not estimates of total fiscal loss, lifetime burden or the effect of admitting another person. The numeric distinction is consequential: the Mexican-second-generation balance is positive inside this incomplete account while its comparison gap is negative. [DATA / INFERENCE]

`reconcile.py` independently adds the seven saved component means for all12 group/allocation cells and checks the recorded white-reference differences. It uses the held `gen_ledger_extension_2026_09_16/extended_ledger_by_generation.csv`, with a SHA-256 recorded in `derived/fiscal/audit.json`. This checks the aggregate account; it is not another raw-data replication.

| Allocation, adults25–64, 2024 income year | Mexican G2 partial balance | Difference from white G3+ reference | Difference from all-native average |
|---|---:|---:|---:|
| Equal shares across all resource-unit members | +$7,698 | −$8,286 | −$6,567 |
| Equal shares across adults18+ in resource unit | +$7,466 | −$10,633 | −$8,310 |

The all-native comparator removes the racial restriction but includes Mexican G2 itself; it is an overlapping descriptive benchmark. No new standard error is inferred from separately printed marginal errors. Neither comparator is the counterfactual outcome of an immigration policy. Changing family allocation alters both the unit interpretation and size of the difference. [DATA / METHOD]

For the first row, let omitted **net** fiscal components be `U`. The completed balance would be `7,698 + U`; it changes sign at `U = −7,698` per adult-year. Let the difference in omitted components between the two groups be `D`; the completed white-reference gap would be `−8,286 + D`, changing sign at `D = +8,286`. These are different thresholds. They are conditional identities, **not empirical bounds** or assertions that omitted terms lie near zero. Analogous thresholds for every cell are saved in `conditional_thresholds.csv`. [METHOD]

The old account omits substantial public health/institutional care, corporate taxes, public goods and indirect effects. It also models taxes from common income/wealth inputs and allocates average school costs. Its eight within-model sensitivity arms do not constitute eight independent confirmations of a full balance. A child's spending attributed to a parent's resource unit must not subsequently be counted again as an additional descendant cost. Marginal school cost need not always be lower than average cost: spare capacity and an expansion threshold imply different cases. No new dollar valuation of omitted terms is invented here. [SOURCE: [held account and assumptions](../../gen_ledger_extension_2026_09_16/RESULT.md); INFERENCE]

**Leading explanation:** the measured benchmark deficit largely reflects the tax side of the modeled account. **Alternative:** omitted differential costs/revenues and selection could materially change a completed comparison. **Discriminator:** a reconciled, population-and-year-matched health/public-service/tax linkage with explicit marginal policy incidence. **Decision impact:** preserve the descriptive gap; stop calling it a net cost or multiplying it into a lifetime policy verdict. **Next useful action:** fill a consequential omitted component with compatible evidence, rather than add more variants of the same income-based tax model.
