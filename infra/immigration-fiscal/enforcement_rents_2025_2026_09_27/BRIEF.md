# Lane brief: did 2025 interior enforcement lower rents?

Date 2026-09-27, 23:50 JST. Parent session immigration-research-1c. The operator pasted a DHS post and asked
"true?". The claim, verbatim:

> Texas accounted for about a quarter of ICE arrests in July and posted the country's sharpest rent drops,
> with San Antonio down 4.8%, Austin 4.3%, Dallas and Houston about 3%. Miami's average rent is down 2.6%.
> Phoenix is down 4.2%. Atlanta is down 3.2%. Nashville is down 5.3%. New Orleans is down 8%. Research shows
> that illegal-worker inflows push rents and home prices up. That inflow has been reversed in the states
> running the hardest interior enforcement.

It makes three claims: the rent figures, the premise that inflows raise rents, and the attribution of the
2025 declines to enforcement. Test each separately.

## What exists (read first)

- Ladder 180 and 183 (`research/immigration-confidence-ladder.md`):
  - within state, a one-point larger rise in the Mexican-origin share 2010–2023 goes with +0.030 (SE 0.007)
    log points more rent growth 2015–2026 across 168 metros;
  - the instrumented 2000–2010 estimate is a diagnostic null, +1.4% (SE 1.4) per point of foreign-born share;
  - Saiz supply elasticities.
- The winners lane (INDEX "Beside the fiscal headline"): the group's renters pay $22–58bn a year more.
- Zillow ZIP-level ZORI and ZHVI: `../hedonic_composition_2026_09_19/_cache/zillow/` (`src/zillow.py` fetched
  them). Check the last month present. Zillow's metro ZORI CSV is free to fetch if a newer month is needed.
- Census building permits: `../housing_supply_ca_tx_2026_09_22/` (state monthly in `_cache/`; metro files
  are free at census.gov/construction/bps).
- 2025 enforcement by locality: `../construction_housing_supply_2026_09_23/_cache/papers/brookings_beyond-arrests-how-ice-enforcement-depressed-local-employment-in-2025.txt`.
  Use its measure or its data source. The Deportation Data Project and TRAC publish ICE arrests by state or
  area of responsibility.

## Questions

1. **The numbers.** Which source matches DHS's figures (Apartment List, Realtor.com, Zillow or another)?
   - Are they year-over-year for July 2025?
   - Do they reproduce, and how do the same metros look on ZORI?
   - Was the Texas share of ICE arrests in July about a quarter?
2. **Timing.** Were these metros' rents already falling before the 2025 enforcement surge? Give their rent
   growth for 2023, 2024 and 2025.
3. **Supply.** Multifamily permits for 2021–2023, per 1,000 existing units, stand in for 2023–2025 completions.
   How much of the cross-metro rent change do they explain?
4. **Enforcement.** Across the largest metros (at least 100 with ZORI):
   - regress the change in rent growth (2025 against 2024) on enforcement intensity (ICE arrests per 1,000
     residents in 2025, at state or area-of-responsibility level, SEs clustered at that level);
   - control for the supply proxy and the 2024 rent growth;
   - run a placebo: the 2024 change against 2023 on the same 2025 enforcement measure.
   Report every coefficient with its SE and N.
5. **Counterexamples.** Take the high-supply metros in low-cooperation jurisdictions (for example Denver). Do
   their rents fall as much?
6. **Magnitude.** How far could enforcement move population in 2025, counting arrests, departures and the
   lost inflow? Size that move against the Texas metros' population. What rent change does it imply at
   ladder 180's association and at a Saiz-type elasticity of about 1? Compare that with the 3–8% declines.
   - Separate the border-driven fall in inflow, which is national, from interior enforcement, which varies by
     state.
7. **Verdict.** For each claim: true, false, or not identified, with the numbers.

## Rules

- Work only in `infra/immigration-fiscal/enforcement_rents_2025_2026_09_27/`. Do not edit other lanes,
  `research/`, `decisions/`, INDEX, FAQ, ladder or `CLAUDE.md`.
- The checkout is shared: no commits, and no `git add`, `stash`, `checkout` or `reset`.
- Raw downloads go in an ignored `_cache/`, with a `.gitignore` in the lane. Firecrawl is out of credits: use
  Exa or direct HTTP with a generic User-Agent, and no personal identifier in any request. Automated x.com
  fetching is blocked; the claim text above is all you need.
- Run Python as `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repository root. Write
  CSVs with `lineterminator="\n"`. Two runs must be byte-identical.
- Tag every number: [SOURCE], [DATA], [CALCULATION], [INFERENCE] or [TRAINING-DATA]. Steel-man the DHS claim
  before testing it.
- Stub `RESULT.md` with `**Verdict:** pending` first and append as you go.
- Final message: the RESULT path and at most ten lines.
