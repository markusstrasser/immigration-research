claude-opus-5-5

**Verdict:** The five PM2.5 and crash figures that the evidence map printed as approximations now come from the air
and crash lanes' own functions, run over their full grids on the 39,712,493 people the account prices (data audit
row 4). The crash figures also use the NHTS ratios per person aged 5+, as the pairing does. The values are:
- PM2.5 deaths among others: 4,825.
- The PM2.5 span: $30.78–119.71bn.
- PM2.5 against as many average residents: $45.53bn.
- The crash span: −$55.07bn to +$70.84bn.
- Crashes charged by fault: $40.63bn (22.96–69.84).

The map had scaled each figure by its row's central factor. That was off by at most $0.22bn, but two printed numbers
change: PM2.5 against average residents goes from $45bn to $46bn, and crashes by fault from $40bn to $41bn. Each end
moves by its own factor because the group's share enters the lanes nonlinearly. The PM2.5 ends move by 0.97706 and
0.97732 against the central's 0.97720. The crash ends move by 0.95474 and 0.95300 against 0.95592. All 22 gates pass:
- both lanes reproduce their published files on their own counts;
- both centrals reproduce `population_basis_2026_09_29/derived/reeval.csv`;
- both factors reproduce `restated_pairing.csv`.

# Air and crash spans on the priced count, 2026-09-29

Lane `social_spans_priced_count_2026_09_29`, written by the teammate drift-audit-lane for the team lead. It adopts
nothing and changes no other lane's outputs. The map's registry records now read its file; the team lead reviews and
commits.

## What was run

`population_basis_2026_09_29/reeval.py` restated each pairing row's central value on row 4. It runs the lane's own
function with every CPS count that function reads replaced by the row-4 value. This lane runs the same substitution
through each lane's full factorial grid. Every end is then the grid's own minimum or maximum on the priced count. Both
lanes are imported read-only: their `main()` never runs and nothing is written beside them. The frame counts and the
under-5 shares come from reeval.py's own `counts()` and `under5_shares()` functions.

| Item | Function | What moves to row 4 |
|---|---|---|
| PM2.5 from consumption | `air_pollution_2026_09_28/air_items.py` `pm_grid`, 3^7 = 2,187 cells | the union, 40,896,574 → 39,712,493, and the CPS civilian frame, 336,727,803 → 335,543,722. Row 4 alone, as in the pairing: the item is keyed to consumption, not to travel per person. |
| Road crashes, but-for and fault-based | `road_crash_externality_2026_09_28/crash_model.py` `evaluate_split` over its `main()`'s 3^9 = 19,683 cells, with the composition term on | the union and frame counts. The union's share of Hispanic residents goes 0.589488 → 0.582348. The self-exposure q goes 0.298794 → 0.289555, from the congestion lane's exposures at the row-4 scale. The NHTS ratios apply per person aged 5+: the population share P goes 0.121453 → 0.115272, from p(1 − u_g) / [p(1 − u_g) + (1 − p)(1 − u_o)] with u_g = 0.079695 and u_o = 0.051801. |

[DATA: population_basis_2026_09_29/derived/frame_counts.csv; main_case_decomposition_2026_09_29/derived/age_bins.csv]
[CALCULATION: priced_spans.py → derived/priced_spans.csv]

## The five values

| Map record | Figure | The lane, on 40.90M | The map's scaled approximation | This lane, on 39.71M | The map prints |
|---|---|---|---|---|---|
| `pm25.deaths_priced` | deaths among others, central | 4,938.05 | 4,825.46 (× 0.977200) | 4,825.46 | 4,800, unchanged |
| `pm25.span_priced` | cost to others, low and high | 31.50 – 122.48 | 30.78 – 119.69 | 30.78 – 119.71 | 31–120, unchanged |
| `pm25.normalized_priced` | against as many average residents, central | −46.51 | 45.45 (× 0.977200) | −45.53 (factor 0.978979) | **$45bn → $46bn** |
| `crash.span_priced` | but-for cost, low and high | −57.68 – +74.34 | −55.14 – +71.06 (× 0.955917) | −55.07 – +70.84 | −55 to +71, unchanged |
| `crash.fault_based_priced` | charged by fault: central (low–high) | 42.34 (23.80–73.25) | 40.47 (22.75–70.02) | 40.63 (22.96–69.84) | **$40bn → $41bn** (23–70) |

[DATA: derived/priced_spans.csv, columns `published` and `priced`; the lanes' items.csv and items_detail.csv]

Against the approximations, the new values move by −$0.0045bn and +$0.014bn (the PM2.5 ends) and +$0.083bn (the
normalized figure). They move by +$0.066bn and −$0.22bn (the crash ends) and by +$0.16bn, +$0.21bn and −$0.18bn (the
fault-based row). The deaths move by +0.0002. The approximations used each lane's printed values and the factor printed
to six places; this lane uses both unrounded. The map's central values are unchanged: `pm25.cost` and `crash.cost`
still read restated_pairing.csv. Every extreme sits at the same grid cell on both counts (column
`cell_on_published_count`).

## Why each end moves by its own factor

The gate asked that every span end move by the same factor logic as the central, or that this RESULT say why not. The
logic is the same: every figure is its lane's function on the row-4 counts. The factors differ because the group's
share enters each function nonlinearly. `derived/end_factors.csv` splits each end's factor into its parts, cell by
cell.

**PM2.5.** The cost to others is D θ s r (1 − σ) × morbidity × VSL. The self-share σ = Lι + (1 − L)sE is the part of
the group's pollution that the group breathes itself. On row 4 the population share s falls by × 0.974474 (0.121453 →
0.118353) in every cell. σ falls with s, so the share falling on others, 1 − σ, rises. The rise depends on the cell's
L and E:
- the low end's cell (L 0.45, E 1.20): × 1.002653, total factor 0.977059;
- the central: × 1.002798, total factor 0.977200;
- the high end's cell (L 0.25, E 1.05): × 1.002917, total factor 0.977317.

The deaths among others are the central cell's deaths, and the cost is deaths times constants. So they move by exactly
the cost's factor, and the old approximation was already right to within its rounding. The normalized figure is D θ s
[r(1 − σ) − (1 − s)]. Its comparison group's term, 1 − s, grows as s falls, so the bracket's magnitude rises by
× 1.004623 and the figure moves by 0.978979, not by 0.977200.

**Crashes.** Each multi-vehicle term scales with the traffic share s = P r / (P r + 1 − P) and with 1 − q. Here q is
the group's own share of the traffic where it drives. The non-motorist term scales with s(1 − q)/(1 − s) × (1 − h),
and the single-vehicle term with s alone. On the priced count s falls by about × 0.948 in every cell. 1 − q rises, by
an amount that depends on the cell's q setting:
- q at 1.3 × the metro exposure: × 1.019640;
- q at 1.0 × the metro exposure (the central): × 1.013176;
- uniform mixing, where q = s: × 1.006361.

Both ends of the but-for span sit at uniform mixing, so both fall further than the central: × 0.954743 and ×
0.952998, against 0.955917. The high end falls most because its non-motorist and single-vehicle parts are larger.
Those parts move by × 0.9506 and × 0.9485, against × 0.9545 for the multi-vehicle parts. The fault-based row uses
neither the volume elasticities nor the composition term. Its low end sits at q 1.3 × (× 0.964843), its central at
1.0 × (× 0.959697) and its high end at uniform mixing (× 0.953546). Its parts are mostly multi-vehicle and
non-motorist, the parts that the fall in q offsets. That is why the but-for central's factor, 0.955917, understated
it by $0.16bn.

## Gates

All 22 pass; `derived/gates.csv` lists each gate with its values.

- **The frame.** The age bins sum to the row-4 union and frame. The under-5 shares equal the roads lane's `keys.csv`.
- **The air lane on its own counts.** Its union and frame are the published CPS counts. The absolute and
  normalized low, central and high values print exactly as `items.csv` prints them. The deaths among others print as
  `items_detail.csv` does, 4,938.05. The grid keeps its cells in order on row 4.
- **The air lane on row 4.** The central, 68.092103594, equals reeval.csv's `pm25_consumption` row4_bn. Its factor,
  0.977200394, prints as restated_pairing.csv's (section `row`). The printed published value 69.6808 times that factor
  gives the restated 68.092105.
- **The crash lane on its own counts.** Its union and frame are the published counts. The congestion exposures at the
  lane's scale give its q, 0.298793803, to 1e-12. The but-for and fault-based spans equal `model.json` `spans` exactly
  and print as `items.csv`.
- **The crash lane on row 4.** Row 4 alone gives reeval.csv's `road_crash_externality`, 10.876623930. Adding the 5+
  basis gives its `road_crash_externality_5plus`, 10.566366076. The factor, 0.955916779, prints as restated_pairing.csv's
  (section `row_5plus`), and 11.05 times it gives the restated 10.562880. The fault-based central is the same with the
  composition term off, which is crash_model.py's own check.
- **Ranges.** Every span holds its central on the priced count.

## A convention in restated_pairing.csv

`restated_pairing.csv` restates each row as the lane's printed central times the exact factor. For crashes that is
11.05 × 0.955917 = 10.562880. The lane's unrounded central gives 10.566366, which is $0.0035bn more. For PM2.5 the
difference is 1.4e-6. The pairing total and every printed figure are unaffected: $413.7–488.0bn either way. The
convention follows from restate.py's "published" column. This lane reproduces it and does not change it.

## Files

- `priced_spans.py`: the re-evaluation and its gates.
- `derived/priced_spans.csv`: 13 rows, one per (item, measure, statistic). Columns:
  - `lane_printed`: the lane's file as printed;
  - `published`: the lane's function on its own counts, unrounded;
  - `priced`: the same on row 4, plus the 5+ basis for crashes;
  - `factor`;
  - `cell`: the grid cell holding the value;
  - `cell_on_published_count`.
- `derived/end_factors.csv`: 44 rows, each end's factor split into its parts on the same cell.
- `derived/gates.csv`: the 22 gates with their values. A failed gate writes no file.

Consumers: the evidence map's records `pm25.deaths_priced`, `pm25.span_priced`, `pm25.normalized_priced`,
`crash.span_priced` and `crash.fault_based_priced` in `overview_2026_09_28/quantity_registry.csv`.

## Reproduce

From the repository root, after `population_basis_2026_09_29/frame_counts.py` and `reeval.py`:

```
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 \
    infra/immigration-fiscal/social_spans_priced_count_2026_09_29/priced_spans.py
```

It runs in about 10 seconds and needs no network. The congestion setup reads ignored inputs: the congestion lane's
`_cache/` and a crosswalk in `employment_entry_2026_09_18/_cache/`.

## Log

Times come from `date` calls.
- 2026-09-29 10:10:07 JST: started, after reading reeval.py, air_items.py, crash_model.py and restated_pairing.csv.
- 2026-09-29 10:20:44 JST: the script and outputs written; two runs were `cmp`-identical.
- 2026-09-29 10:21:40–10:23:51 JST: validation, with this lane and the map's rebinding in the working tree on HEAD
  0a4d9dc:
  - two lane runs, all 22 gates PASS and the three CSVs `cmp`-identical;
  - two map builds `cmp`-identical, 66 bindings, no approximate marks on the page;
  - two drift audits `cmp`-identical, 665 of 665 MATCH;
  - two registry checks `cmp`-identical, 79 records, 13 FIXED;
  - pytest 23 passed, and ruff passed;
  - no file written in the imported lanes.
