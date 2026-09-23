# Lane brief: road congestion cost of the group's presence to other residents

Operator request (2026-09-23): "Do the remaining common sense stuff to get at the real fiscal
and social costs." Traffic is the largest common-sense channel not yet priced anywhere in the
repo.

## Frame (do not change)

The [complete annual account](../../../research/immigration-complete-annual-account-2026-09-20.md)
measures the annual 2024 effect of the 40.896574m CPS Mexican-origin residents (all generations
and schooling) on all **other** US residents in a stationary absent-target comparison. Its main
CBO-informed case ($165.1–197.4bn) holds **economic-affairs budgets fixed**, and those include
highways and transit. The group's traffic then runs on a network that would be the same size
without it, so other residents bear the extra delay as a non-budget cost of that assumption.
In the proportional-service benchmark, road and transit spending scale with population. There
the only extra delay is whatever added capacity fails to remove; Duranton and Turner's
"fundamental law" says traffic rises with lane-miles.

## Task

1. **The group's share of road travel.** Use ACS 2024 one-year PUMS persons
   (`sources/immigration-fiscal/data/external/acs_pums_2024_1yr/csv_pus.zip`, `PWGTP`). Define
   the group as the housing lane does: `HISP=02` or `POBP=303`; see
   `../housing_transfer_2026_09_23/RESULT.md` §1. Tabulate commuters by means (`JWTRNS`),
   one-way travel time (`JWMNP`), departure time (`JWDP`, peak versus off-peak) and car
   occupancy (`JWRIP`) for the group and for everyone else, nationally and by metro. Build the
   metro geography with the housing lane's PUMA→CBSA route
   (`../employment_entry_2026_09_18/_cache/xwalk_puma22.csv`; see its `arms.py`). Commuting is
   about a fifth to a quarter of vehicle-miles. If the NHTS 2022 public files can be downloaded
   (nhts.ornl.gov), use them for daily VMT per person by Hispanic origin across all trip
   purposes. Otherwise scale commuting to all travel with a stated, ranged assumption.
   **Gate:** ACS commuter totals by means within a few percent of published table B08301.
2. **Congestion cost to other residents if the group's traffic were absent.** Build two
   approaches and range both:
   - **A. Network delay.** Take metro delay hours and cost from the Texas A&M Transportation
     Institute *Urban Mobility Report* (latest edition with metro tables; mobility.tamu.edu).
     Apply a volume–delay relation (BPR-type, with the delay elasticity on congested links as a
     ranged input) and the group's metro traffic share. Integrate the removal of the group's
     inframarginal traffic, not the marginal. Value time with USDOT's 2016 guidance, revision 2
     (personal travel 50% of the median wage, business travel 100%), in 2024 dollars.
   - **B. Aggregate elasticity.** Take travel speed or commute time as a function of city
     population from Couture, Duranton and Turner (2018, *REStat*, "Speed") or Duranton and
     Turner (2011, *AER*). Apply the group's metro population share and value other residents'
     total travel time.
   Say which approach matches the main case's fixed network and which matches the proportional
   benchmark. **Positive control:** reproduce one published national total from the downloaded
   Urban Mobility Report file, such as total delay hours or congestion cost.
3. **Overlap.** Congestion adds to the main case only. Under proportional spending, add only the
   residual after capacity growth, and name the evidence for it. Fuel-tax receipts are already
   in the account's taxes; do not add them. Transit crowding and parking are optional and
   separate.
4. **Distribution.** Report delay hours and dollars per other-resident commuter, by the metros
   that carry most of the cost.

## Output

- `derived/` CSVs with the tabulations, metro exposure and every arm.
- `RESULT.md` opening with `**Verdict:**`. Give annual cost to other residents under A and B
  with ranges, the overlap ruling, and per-commuter figures. Then give method, sources, limits
  and a "Covered / skipped" list with reasons.

## Rules

- Run from the repository root: `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>`.
  Read the ZIPs in chunks, keeping only the needed columns.
- Tag claims `[SOURCE: …]`, `[DATA: …]`, `[CALCULATION: …]`, `[INFERENCE]` or `[UNVERIFIED]`.
  Read every number used in a calculation from the primary file or paper, never from a summary.
- If you need the Census API, the key is in `infra/immigration-fiscal/acquire/config.local.env`.
  Never print it, and pipe output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`.
- Edit nothing outside this directory. Do not commit. Return the RESULT.md path and at most
  10 lines.
