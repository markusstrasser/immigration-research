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

### 2026-09-29 — remove the superseded analysis

[Cleanup decision](../decisions/2026-09-29-delete-superseded-and-cruft-docs.md): the verbatim pre-repair analysis that followed this section was removed; recover it with `git show 36c4477:research/immigration-open-borders-break-even-bounds-2026-04-22.md`.
