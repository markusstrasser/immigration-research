# Immigration open-borders break-even bounds

**Current assessment: 2026-09-05.** The arithmetic defines useful conditional scenarios. It does not estimate the probability or size of actual net losses, and the US housing comparator does not measure combined rich-country capacity. The earlier physical-frontier and “moderate loss” verdicts were stronger than these calculations warrant. [INFERENCE]

## Recomputed thresholds

Inputs retained from the original memo: $7,500 annual gain per additional migrant; $110T world GDP; 1.4B incumbent residents across rich destinations; 333M US residents; 2.5 people per housing unit; 1.4M US housing starts per year; 30-year construction horizon. These are scenario inputs recorded in April, not live measurements verified for September. The cited generator/data files are absent from this checkout.

| Additional migrants | Annual assumed gain | Share of $110T GDP | Annual break-even net loss per rich-destination incumbent |
|---|---:|---:|---:|
| 200M | $1.5T | 1.36% | $1,071 |
| 500M | $3.75T | 3.41% | $2,679 |

[CALCULATION: gain = migrants × $7,500; threshold = gain ÷ 1.4B]

If the entire $1.5T loss were instead borne by 333M US incumbents, the conditional amount is $4,505 each. This is a different incidence scenario; it must not be interchanged with the all-rich-destinations denominator. [CALCULATION]

## What “break even” means

The threshold compares the assumed gains with **additional net losses measured on a consistent basis**. It does not show that the threshold is reached, that all losses fall on incumbents, or that a particular rent increase measures those losses. [INFERENCE]

A higher rent can reduce a tenant's disposable income and increase the landlord's income. That distributional burden is real, but the gross payment is not automatically an equal reduction in world output or unweighted aggregate income. Construction uses real resources while creating a durable asset; its financing, depreciation, and services need consistent treatment. Welfare weights can also make a transfer matter for social welfare without changing aggregate output. [INFERENCE]

Annual gains and losses need matched timing. A one-time construction cost, a decade of transition strain, and a permanent annual productivity loss are different objects. To compare them, specify the path, discounting, horizon, and what the $7,500 gain already includes. Do not double-count a loss already netted out of that gain. [INFERENCE]

The former description of $1,071 as a reachable or merely moderate loss was a judgment without an estimated net-loss distribution. The current conclusion is conditional: a persistent net loss of that size would offset the assumed gain. Whether it occurs is unresolved. [INFERENCE]

## Housing arithmetic and its geographic scope

| Additional migrants | Units at 2.5 people/unit | Units/year over 30 years | Ratio to the assumed 1.4M US starts/year |
|---|---:|---:|---:|
| 200M | 80M | 2.67M | 1.90× |
| 500M | 200M | 6.67M | 4.76× |

[CALCULATION: migrants ÷ 2.5 ÷ 30; final column divides by 1.4M]

These are **comparators to US construction**, not estimates of total rich-world housing capacity. Applying global or multi-country arrivals entirely to the US numerator would change the scenario. Current starts also are not spare capacity: existing households already require construction. Conversely, starts can change, and existing units, household sharing, and destination choices affect demand. [INFERENCE]

Thus the table neither demonstrates an adequate transition nor proves a global physical ceiling. A capacity test requires a destination allocation, baseline housing demand, vacancies, construction response, and arrival schedule. Those quantities are not identified by this table. [INFERENCE]

## Current conclusion

The break-even calculation transparently states how large an additional net loss would have to be under the chosen gain assumption. The housing calculation states a unit requirement and a US scale comparison. Neither establishes an empirical upper bound on global migration gains. [INFERENCE]

## Revisions

### 2026-09-05 — separate arithmetic from empirical capacity and welfare claims

[Material inference repair decision](../decisions/2026-09-05-material-inference-repair.md): retain the correct threshold and unit calculations; withdraw claims that they establish reachable losses or a rich-world absorption ceiling; specify geography, timing, net accounting, and missing inputs. Earlier prose is retained verbatim below.

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Immigration open-borders break-even bounds — 2026-04-22

**Question:** If large migrant place-premium gains are real, how much destination-country capacity loss would be required to wipe them out under the repo's own conservative calibration?  
**Tier:** Deep | **Date:** 2026-04-22  
**Ground truth:** The repo already had a conservative open-borders baseline calibration. This pass translates it into break-even loss bounds and housing-absorption requirements instead of leaving it as a slogan argument. [SOURCE: sources/immigration-causal/scripts/open_borders_baseline.py] [SOURCE: sources/immigration-causal/scripts/analyze_open_borders_break_even.py]

## Bottom line

1. Under the repo's conservative `$7,500` annual gain assumption, a `+200M` rich-destination scenario yields about `$1.5T` annual gain, or about `1.36%` of world GDP. [SOURCE: sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv]
2. To erase that gain completely, destination-incumbent losses would need to reach about `$1,071` per existing rich-country resident per year, or about `$4,505` per U.S. resident per year if the entire burden were borne by the U.S. [SOURCE: same]
3. The physical absorption burden is enormous. `+200M` migrants imply about `80M` housing units at `2.5` people per unit, which is about `55%` of the current U.S. housing stock and would require about `1.9x` current U.S. annual housing starts for `30` straight years. [SOURCE: same]
4. So the strong global-gains case does **not** die automatically, but it survives only if destination-capacity erosion stays well below a very demanding physical absorption frontier. [INFERENCE]

The housing comparison is a `U.S. benchmark`, not a literal estimate of total rich-world housing capacity. It is used because the repo's concrete capacity baseline is U.S.-centric. [SOURCE: sources/immigration-causal/data/clemens/open_borders_break_even_bounds.json]

## New artifacts

1. [analyze_open_borders_break_even.py](sources/immigration-causal/scripts/analyze_open_borders_break_even.py)
2. [open_borders_break_even_bounds.csv](sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv)
3. [open_borders_break_even_bounds.json](sources/immigration-causal/data/clemens/open_borders_break_even_bounds.json)

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | The conservative `+200M` scenario still yields very large annual gains | `$1.5T`, about `1.36%` of world GDP | HIGH | [open_borders_break_even_bounds.csv](sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv) | VERIFIED |
| 2 | The gain can be wiped out by moderate-to-large incumbent losses, not by only catastrophic ones | About `$1,071` per existing rich-country resident per year is enough in the `+200M` scenario | HIGH | [open_borders_break_even_bounds.csv](sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv) | VERIFIED |
| 3 | The physical absorption burden becomes huge quickly | `80M` housing units for `+200M`; `200M` housing units for `+500M` | HIGH | [open_borders_break_even_bounds.csv](sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv) | VERIFIED |

## 1) The break-even inequality is now explicit

The repo's earlier high-level formulation was:

`global gains survive iff place-premium gains > destination-capacity losses + origin losses`

This pass gives that a quantitative bound. [SOURCE: research/immigration-frontier-rethink-2026-04-22.md] [SOURCE: sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv]

For `+200M` migrants at `$7,500` gain each:

1. annual gain = `$1.5T`
2. break-even loss = `1.36%` of world GDP
3. break-even loss = `5.47%` of current U.S. GDP
4. break-even loss per existing rich-country resident = about `$1,071`

[SOURCE: sources/immigration-causal/data/clemens/open_borders_break_even_bounds.csv]

That is big enough that the global-gains case is not trivially killed. It is also small enough that destination-country degradation cannot be waved away. [INFERENCE]

## 2) The housing requirement is the real stress test

The same `+200M` scenario implies:

1. about `80M` housing units
2. about `2.67M` housing units per year over `30` years
3. about `1.90x` current U.S. annual housing starts over that `30`-year horizon

[SOURCE: same]

Again, that is a U.S. benchmark comparator, not a literal claim about the full rich world. [SOURCE: sources/immigration-causal/data/clemens/open_borders_break_even_bounds.json]

That is the deeper point. The break-even welfare loss and the physical absorption constraint point in the same direction:

1. the gains are not fake
2. but they rely on a destination-capacity machine that has to scale much more than current rich-country housing systems do

## 3) The stronger slogans now look even less realistic

At `+500M` migrants with the same conservative gain:

1. annual gain = `$3.75T`
2. break-even loss per existing rich-country resident = about `$2,679`
3. housing units required = `200M`
4. annual housing need over `30` years = about `6.67M`, or about `4.76x` current U.S. starts

[SOURCE: same]

So the repo can now say something tighter:

1. bounded or moderate liberalization can still carry very large gains
2. the strongest open-borders magnitude claims rely on absorption scales that look physically and politically extreme

## What now survives

1. the global-gains case still survives in direction under conservative per-migrant gains [SOURCE: same]
2. the case does **not** survive as a carefree slogan about rich countries absorbing arbitrarily large flows without major system scaling [INFERENCE]
3. housing is the clearest physical bottleneck in the baseline math [SOURCE: same]

## Best current formulation

The strongest honest version is:

1. `global gains can remain large`
2. `the break-even threshold is not impossibly high`
3. `the physical absorption requirement is still severe`

That is a cleaner, more falsifiable position than either “double world GDP” optimism or reflexive dismissal. [INFERENCE]

</details>
<!-- historical-snapshot:end -->
