# Receiver-node screen: correlated indicators without calibrated confirmation

**Current assessment — 2026-09-05.** The nine-node table screens selected areas for coincident administrative and household indicators. It does not establish Miami-Dade or NYC as causal “survivors” of a receiver-overload theory. The assigned probabilities 0.55, 0.30, and 0.15 are withdrawn: no likelihood, calibrated updating rule, or mutually exclusive hypothesis partition was supplied. [INFERENCE]

## Population and geography

ACS recent-entry and moved-from-abroad measures identify different populations and periods; neither identifies unauthorized status. The stated PUMA-to-node bridge allocates by **land-area overlap**, not population. This assumes population and outcomes are uniformly distributed within the source geography. It cannot be treated as a validated county estimate, and its error need not attenuate coefficients or rankings toward zero. Population weighting would improve the geographic allocation assumption but would not reveal legal status or eliminate all within-PUMA selection. [SOURCE: historical design/limits; INFERENCE]

EOIR base-city counts measure court venue workload, not the number or residence of local immigrants. Proceedings or filings are also not automatically unique people or a backlog stock: changes depend on new filings, transfers, completions, reporting, and court catchments. The broad/strict differences already reported for Harris (1.99× versus 0.81×) and DC (1.74× versus 0.17×) must remain measurement warnings, not be averaged into confirmation. [SOURCE: historical table; INFERENCE]

QWI does not identify immigrant or native workers; its stable-employment earnings outcome is monthly earnings, not native hourly wages. HIC/PIT and spending-per-resident inputs additionally inherit the program and geographic limitations of the [receiver atlas](immigration-receiver-failure-atlas-2026-04-22.md). [SOURCE: [Census QWI variables](https://api.census.gov/data/timeseries/qwi/se/variables.html); INFERENCE]

## What the score tests

The score counts whether a location exceeds the **nine selected nodes' medians** on correlated inputs, including exposure, housing, court and political outcomes. Changing the node set changes those thresholds and ranks. A high count is not a calibrated probability, a national rarity measure, a measure of loss magnitude, or independent multi-channel evidence. Using the same outcomes to define “synchronization” and then calling high-scoring places confirmation of synchronization does not independently test the proposed causal chain. [SOURCE: historical scoring definition; INFERENCE]

Concurrent housing scarcity, court policy, exposure, and measurement error can coexist; they are not exclusive hypotheses that can receive probabilities summing to one without a model. The screen can motivate matched comparisons with predetermined definitions, direct local intake data, and mapped residence outcomes. It cannot establish that immigration rather than shared trends produced the pattern. [INFERENCE]

The original joins, code, and raw node outputs were not recovered for replication. The recorded values and broad/strict sensitivity remain historical evidence to inspect, not freshly verified full-spectrum overload findings. [GAP]

## Revisions

- **2026-09-05:** Withdrew arbitrary posteriors and causal-survivor labels, retained mapping disconfirmation, and clarified correlated-score and outcome-universe limits. [Decision](../decisions/2026-09-05-material-inference-repair.md).

<!-- historical-snapshot:start superseded=2026-09-05 -->
<details>
<summary>Superseded historical analysis — retained verbatim for source and correction provenance</summary>

**Historical text, not the current assessment.** Its earlier verdicts, confidence labels, and source-version claims are superseded by the corrections above. It is retained to preserve quotations and the reasoning that was corrected.

# Immigration Receiver-Node Kill Test — 2026-04-23

## Bottom Line

[DATA] The end-to-end public-data pass was run across nine receiver nodes using 2024 ACS PUMS exposure, Census 2020 PUMA relationship geography, EOIR Case Data 2026-0301, QWI county labor data, and the existing receiver failure atlas.

[INFERENCE] The receiver-node theory survives the first kill test for `Miami-Dade County` and `New York City`: both show high recent-entry exposure, high renter/crowding stress, elevated court load versus 2017-2019, and above-median 2024 GOP shift. `Bexar County` is the second-tier survivor. `Harris County`, `Denver County`, `Boston / MA core`, `Chicago / Cook County`, `District of Columbia`, and `El Paso County` are mixed or channel-specific, not full-spectrum confirmations.

## Outputs

| Output | Path |
|---|---|
| Final kill table | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_node_kill_test_2024.csv` |
| ACS node exposure | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_acs_2024_node_exposure.csv` |
| EOIR broad venue panel | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_eoir_pressure_2017_2025.csv` |
| EOIR strict venue panel | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_eoir_pressure_strict_2017_2025.csv` |
| QWI labor summary | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_qwi_labor_2021_2024.csv` |
| PUMA bridge | `sources/immigration-causal/data/outcomes/analysis/receiver_node_kill_test/receiver_puma_bridge.csv` |
| Build script | `sources/immigration-causal/scripts/build_receiver_node_kill_test.py` |

## Design

[SOURCE: https://www2.census.gov/programs-surveys/acs/data/pums/2024/1-Year/] ACS 2024 PUMS supplies PUMA-level person and household exposure.

[SOURCE: https://www.census.gov/geographies/reference-files/time-series/geo/relationship-files.2020.html] Census 2020 PUMA relationship files supply the PUMA-to-county-subdivision bridge. The analysis uses `tab20_puma520_cousub20_natl.txt`.

[SOURCE: https://fileshare.eoir.justice.gov/EOIR%20Case%20Data.zip] EOIR Case Data 2026-0301 supplies court proceeding counts by base-city venue.

[SOURCE: https://api.census.gov/data/timeseries/qwi/se] Census LEHD QWI supplies county-quarter labor outcomes by education and industry.

[DATA] Receiver-node shelter/capacity/political context is taken from `sources/immigration-causal/data/outcomes/analysis/receiver_failure_atlas_2024.csv`.

[INFERENCE] The synchronized-pressure score is a screening index, not a causal estimate. It flags whether a receiver node is above the nine-node median on: recent-entry ACS exposure, moved-from-abroad ACS exposure, severe rent burden, crowding, sheltered/HIC ratio, overall homeless/HIC ratio, spending per resident, EOIR filings versus 2017-2019, and GOP shift.

## Main Table

| Node | Recent-entry share | Moved-from-abroad share | Severe rent-burden share | Crowded-person share | Shelter/HIC | EOIR filed 2024 | EOIR vs 2017-19 | Strict EOIR vs 2017-19 | GOP shift | Flags |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Miami-Dade County | 10.94% | 2.26% | 36.12% | 15.13% | 0.94 | 128,114 | 3.30x | 3.99x | 9.29 pp | 8 |
| New York City | 4.68% | 1.14% | 27.62% | 17.84% | 1.21 | 140,657 | 3.06x | 2.73x | 7.83 pp | 8 |
| Bexar County | 3.90% | 1.06% | 25.36% | 9.33% | 1.02 | 49,761 | 3.26x | 3.26x | 4.42 pp | 6 |
| Harris County | 6.61% | 1.82% | 27.79% | 11.89% | 0.72 | 80,388 | 1.99x | 0.81x | 3.74 pp | 5 |
| Denver County | 2.97% | 0.64% | 20.72% | 6.64% | 1.34 | 43,062 | 4.20x | 7.28x | 2.41 pp | 4 |
| Boston / MA core | 5.76% | 1.42% | 22.63% | 6.77% | 0.83 | 48,329 | 2.87x | 2.25x | 3.34 pp | 3 |
| Chicago / Cook County | 3.88% | 1.15% | 25.18% | 8.06% | 0.85 | 95,226 | 5.33x | 5.33x | 4.34 pp | 3 |
| District of Columbia | 3.79% | 1.25% | 24.28% | 11.18% | 0.90 | 29,646 | 1.74x | 0.17x | -0.32 pp | 3 |
| El Paso County | 2.46% | 0.85% | 25.34% | 9.69% | 0.57 | 25,579 | 1.74x | 1.66x | 10.26 pp | 3 |

## Interpretation

[INFERENCE] `Miami-Dade County` is the strongest all-channel survivor. It has the highest recent-entry share, highest severe rent-burden share, high crowding, high EOIR filings under both broad and strict court mapping, and high GOP shift. Shelter saturation is not above 1.0 on the sheltered/HIC metric, so the stress signal is more housing/court/political than shelter-bed overflow.

[INFERENCE] `New York City` is the cleanest full-spectrum overload case. It has high ACS exposure, high crowding, severe rent burden, shelter saturation, very high spending per resident in the prior atlas, high EOIR filings under strict and broad court definitions, and high GOP shift.

[INFERENCE] `Bexar County` is a plausible second-tier receiver-pressure case: shelter/HIC is above 1.0, EOIR filings are 3.26x baseline under strict mapping, and GOP shift is above the node median. The weaker point is that crowding and foreign-born share are lower than NYC/Miami/Harris.

[INFERENCE] `Harris County` is mixed. ACS exposure and housing stress are high, but the court signal is not robust to strict venue mapping: broad EOIR filings are 1.99x baseline, while strict Houston-only filings are 0.81x. Treat Harris as a housing/labor exposure case, not a proven court-pressure case.

[INFERENCE] `Denver County` is also mixed. Shelter pressure and EOIR filings are high, especially under strict mapping, but ACS recent-entry exposure and household stress are below the node median. This looks more like shelter/court concentration than broad ACS-measured newcomer exposure.

[INFERENCE] `Chicago / Cook County` has a very strong EOIR court-load signal but weaker ACS/housing/shelter synchronization. That makes it a court-pressure case, not yet a full receiver-overload case.

[INFERENCE] `District of Columbia` weakens under strict EOIR mapping. The broad court region count is mostly not a DC-residence signal, and the strict venue ratio is below baseline. Do not use DC as a clean immigration-court overload proof without a better residence/venue bridge.

## What This Changes

[INFERENCE] The more powerful theory is no longer "immigration raises or lowers average national welfare." The better testable theory is:

`flow x capacity x composition x regime -> local incidence -> political feedback`

[INFERENCE] Previous average-county models missed two things: first, receiver nodes are not interchangeable counties; second, channels can split. A wage null does not kill a shelter/court overload story, and a court spike does not prove broad fiscal harm.

## Causal Status

[INFERENCE] Leading hypothesis, `P = 0.55`: concentrated recent immigration exposure interacting with constrained local capacity is producing synchronized pressure in a subset of receiver nodes, especially Miami-Dade and NYC.

[INFERENCE] Top alternative, `P = 0.30`: national EOIR backlog/policy timing and local housing scarcity independently create similar-looking pressure without immigration-flow concentration being the main cause. This alternative is strongest for Chicago, Denver, DC, and Harris.

[INFERENCE] Residual, `P = 0.15`: measurement and mapping artifacts, especially PUMA area allocation and EOIR venue-to-residence mismatch.

[INFERENCE] Falsifier: the receiver-node theory should be downgraded if a population-weighted PUMA bridge, direct shelter inflow records, or residence-linked court data removes the Miami-Dade/NYC synchronization, or if matched high-exposure/low-capacity nodes do not show higher stress than comparable low-exposure nodes.

## Limits

[LIMIT] ACS PUMS does not identify undocumented status or legal channel.

[LIMIT] PUMA-to-receiver-node allocation uses county-subdivision area overlap, not population overlap.

[LIMIT] EOIR base city is court venue, not respondent residence. Strict venue mapping was added because broad mapping can overstate node attribution.

[LIMIT] QWI is labor-market outcome data by county and education; it does not identify immigrant workers.

[LIMIT] There are only nine receiver nodes in this screening table. The score is a triage device, not a publishable regression result.

</details>
<!-- historical-snapshot:end -->
