**Verdict:** The complete ACS 2024 person PUMS produces the requested education × origin × age institutional stock counts with all 80 sampling replicates. Both external count gates reproduce exactly; 68 gates and 8 unit tests pass. Cost outputs remain explicit uncalibrated scenarios. Sparse institutional cells materially limit subgroup precision.

[DATA] Run on 2026-09-19 from the unmodified source ZIP; 3,422,888 records, 340,110,990 weighted US residents of all ages. The independent stored US-native, Mexican-self-identified male age-18–39 institutional count reproduces 107,917. Source SHA-256: `afdc6d90c6e2f0bab365ed32d95ba4c4d8ac651162f46ac7861295b2dc469894`. Detailed hashes and gate results are in `derived/audit.json`.

### Observed institutional stocks, ages 25+, all education

| Origin/reference | Weighted institutional residents | Raw institutional records |
|---|---:|---:|
| Mexico foreign-born | 80,327 | 1,733 |
| Other Central America foreign-born | 28,518 | 578 |
| Caribbean foreign-born | 37,162 | 806 |
| South America foreign-born | 15,238 | 276 |
| Identifiable Southeast Asia foreign-born | 14,988 | 371 |
| All US natives | 3,133,307 | 70,886 |
| Native non-Hispanic white proxy | 1,783,221 | 41,680 |

[DATA SOURCE] Sum `derived/counts.csv` over bands with `education=all,quantity=institutional_population`. These are stock counts, not rates or fiscal costs. Native rows overlap. Definitions, source links and consumer requirements are in [README.md](README.md).

There are 210 origin × education × age cells, including overlapping all-education rows. Of these, 85 institutional-population cells and 100 institutional-male cells have fewer than 30 observations. Three institutional-population cells have no observed records. Flags retain all raw values. No smoothing, pooling or zero-risk inference is applied.

The export consists of four `[35,6,81]` weighted arrays plus four `[35,6]` unweighted arrays, axis tables, the long count table, and a separate hypothetical-price table. Education partitions hold for every weight and quantity. Self contrasts have exactly zero estimated difference and variance; institutions/households/male-institution subsets are consistent. The full run completed in 28.91 seconds on this machine.

Limits: ACS public person records do not distinguish prison from nursing and other institutions at the level required for these prices. Attained schooling is not admission schooling; native NH white is not third-plus NH white; the oldest band is cross-sectional. Price scenarios 0/50k/100k/150k are not calibrated government costs, identified marginal costs, or credible bounds. They may overlap medical expenditure already elsewhere in a fiscal account; any additional-cost interpretation belongs to the consuming scenario. No entry-window extension, life-cycle institutional transition or demographic causal effect is estimated.

Validation command: `UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 -m unittest -v test_institutional_counts.py`; reproduction command: `UV_CACHE_DIR=/private/tmp/immigration-uv-cache uv run --no-project python3 institutional_counts.py`. An initial pandas 3 read-only-mask error was fixed by non-mutating mask composition and is covered by the accumulation test; the successful full run is the one reported here.
