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
