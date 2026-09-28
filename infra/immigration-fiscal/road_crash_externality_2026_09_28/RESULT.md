**Verdict:** With its driving against without it, the Mexican-origin group's traffic adds about **$44bn a year** (2024 $) of crash losses borne by people outside the group. The full grid runs from $6bn to $145bn, and one input sets most of that range: how fast the crash rate per mile rises with traffic. Most of the $44bn comes from non-fatal multi-vehicle crashes ($35bn), with $8bn from pedestrians and cyclists and $2bn from single-vehicle crashes. That is $1,088 per group member and $150 per other resident. Against the average resident's driving, the normalized cost is about **zero (−$2.6bn; range −$39bn to +$15bn)**. The group drives 11% fewer miles per person than the average resident and is involved in about 6% more crashes per mile, and the two roughly cancel. Charging the group only for the crashes its drivers cause gives almost the same central, $46bn ($26–81bn), and a normalized cost of $0. This fault-based figure is an alternative to the $44bn, never an addition. [CALCULATION: `crash_model.py` → `derived/items.csv`, `derived/model.json`, `derived/grid.csv`]
claude-opus-5-5

# Road-crash externality of the Mexican-origin group's driving (2024 $)

Lane opened 2026-09-28 20:55 JST (from `date`). Frame: the account's stationary 2024 comparison
with and without the 40.896574m CPS 2025 Mexican-origin residents (union), effects on all other
residents. Crash losses only; congestion delay (priced in `congestion_2026_09_23`) and pollution
(parallel `air_pollution_2026_09_28` lane) are excluded.

## Verdict table

| Item | Measure | Low | Central | High | $ / member (central) | Evidence level |
|---|---|---:|---:|---:|---:|---|
| Crash losses of outsiders, but-for | (a) absolute | 5.7 | **44.5** | 145.1 | 1,088 | cost base measured (NHTSA); traffic response contested |
| Same | (b) normalized | −39.4 | **−2.6** | 15.2 | −65 | as (a), plus NHTS Hispanic VMT ratio |
| Fault-based alternative (never add to the row above) | (a) absolute | 26.3 | 45.8 | 80.9 | 1,119 | attribution convention [FRAMING-SENSITIVE] |
| Same | (b) normalized | −18.6 | 0.0 | 20.0 | 0 | as above |

$bn a year, 2024 prices at 2023 crash counts. Low and high are the minimum and maximum over
6,561 factor combinations (eight factors at three levels), not a confidence interval.
[CALCULATION: `derived/items.csv`, `derived/grid.csv`]

Central components of (a): non-fatal multi-vehicle $34.7bn, fatal multi-vehicle $0.1bn,
pedestrians and cyclists $7.7bn and single-vehicle $2.0bn.

One input at a time, with the others at central (total, $bn):

| Input | Low level → total | High level → total |
|---|---:|---:|
| x non-fatal (0.2 / 0.6 / 1.0) | 21.5 | 67.5 |
| x fatal (−0.3 / 0 / 1.0) | 38.2 | 65.5 |
| self-exposure q (×1.3 / metro 0.30 / uniform 0.108) | 39.1 | 56.0 |
| non-motorist β (0.4,0 / 0.8,0.4 / 1.2,1.0) | 38.9 | 51.8 |
| group VMT ratio (0.692 / 0.874 / 0.893) | 35.9 | 45.4 |
| culpability OR (0.98 / 1.13 / 1.47) | 42.0 | 50.2 |
| single-vehicle external share (2% / 4% / 8%) | 43.5 | 46.5 |
| liability κ, group insured share | 44.1 | 45.9 |

Named scenarios [CALCULATION: `derived/scenarios.json`]:

| Scenario | Total | Note |
|---|---:|---|
| Parry-style: crash rate per mile independent of traffic (x = 0, β low) | 4.3 | Parry (2004) puts the external cost at 2.2–6.6¢ a mile |
| 2020 at face value (injury x 0.59, fatal x −1.61) | 6.6 | extra fatal crashes at higher speeds (−$33.8bn) cancel the non-fatal gain |
| Pure pairwise (every x and β = 1) | 94.8 | Vickrey; Edlin & Karaca-Mandic estimate more than this in dense states |
| Uniform national mixing (q = s) | 56.1 | removes the group's metro concentration |
| Mexican-coded culpability (OR 1.47) | 50.2 | normalized +$4.4bn |

## What the numbers mean

A crash between a group driver and an outsider costs the outsider their own losses, whoever is
at fault. Without the group's car there, some of those crashes would not happen at all. The
rest would have happened with another outsider instead. The elasticity x measures the first
share: how much the crash rate per mile rises with traffic. The whole spread in (a) comes from
x, and the evidence on it disagrees:

- **Near 0.** Cross-section safety-performance functions put the elasticity of crashes on
  traffic near 1, and Parry's (2004) 2.2–6.6¢ a mile assumes little volume effect.
  [SOURCE: Parry 2004, RFF DP 03-07 abstract]
- **Near or above 1.** Edlin and Karaca-Mandic (2006) find that in California an extra driver
  raises others' insured costs by $1,725–3,239 a year, and a 1% rise in driving raises insurer
  costs 3.3–5.4%. They find the effect small in sparse states. [SOURCE: EKM JPE 2006 abstract;
  UC Berkeley working paper text as returned by Exa]
- **The 2020 natural experiment.** VMT fell 11.0% from 2019 to 2020. Injury crashes fell 16.9%,
  PDO crashes 24.6% and people injured 16.7%, elasticities of 1.59, 2.43 and 1.57. Deaths rose
  7.3%, an elasticity of −0.61. [SOURCE: NHTSA Traffic Safety Facts 2023, Tables 1–2;
  CALCULATION: `model.json` `covid_2019_2020`] The drop is about the size of the group's traffic
  share (10.8%) and fell on commuting, which is 39% of Hispanic driving against 29% for others
  (NHTS 2022). Behaviour also changed in 2020 (speeding, impairment, belt use), so the fatal
  elasticity overstates the pure speed effect.

The central uses x = 0.6 for non-fatal and 0 for fatal crashes. On the high side, 1.0 is the
pairwise model's value. On the low side, 0.2 and −0.3 stop short of the 2020 fatal figure.
[INFERENCE] The average vehicle's external crash cost at central inputs is 16.9¢ a mile
(3.1–37.3¢), and the group's is 12.7¢ a mile on about 350bn miles. [CALCULATION]

## Method

1. **Cost base.** Blincoe et al. (2023) give 2019 comprehensive costs of $1,365.4bn: economic
   costs of $339.8bn plus $1,025.6bn of quality-of-life loss valued at USDOT's $10.9m VSL. The
   figures cover reported and unreported crashes (Table 1-8). The lane removes crash congestion
   ($36.0bn), which the congestion lane prices and which includes crash-induced emissions, and
   EMS ($1.35bn). It keeps $1,328.1bn, and the positive control reproduces this to $1m. Economic
   parts are updated with CPI-U (255.657 → 313.689 [TRAINING-DATA]) and quality-of-life parts
   with USDOT's VSL ($10.9m → $13.7m, 2024 [SOURCE: transportation.gov VSL table]). Counts are
   updated to 2023: deaths ×40,901/36,355, injured ×2,442,581/2,740,141, PDO crashes
   ×4,403,453/4,806,253 [SOURCE: TSF 2023 Tables 1–2]. The result is **$1,602bn**:
   - multi-vehicle crashes, fatal $261.6bn and non-fatal $716.0bn;
   - single-vehicle crashes $440.1bn;
   - pedestrians and cyclists, fatal $114.4bn and non-fatal $70.3bn (Tables 12-2 and 12-8).

   Multi-vehicle shares come from three sources. For deaths, 56.3% of 2023 occupant deaths
   occurred in crashes with two or more vehicles in transport (FARS). For injuries and PDO,
   multi-vehicle crashes are 75.5% and 71.2% of crashes with no non-motorist (TSF 2023 Tables
   28–29). The shares are by crash, so the multi-vehicle share of costs is if anything
   understated. [CALCULATION: `model.json` `base_2024_bn`]
2. **Who bears the losses.** About 47% of crash costs fall outside the at-fault vehicle:
   - the other party's half of multi-vehicle costs (61% of the total);
   - pedestrians and cyclists (11.5%);
   - passengers, who are 18.8% of single-vehicle occupant deaths (FARS).

   Passengers of the group's own drivers are mostly group members: 83.8% of the known-origin
   passengers killed with a killed Hispanic driver were Hispanic (n = 518; 7.4% with a
   non-Hispanic driver). [CALCULATION: `derived/fars_group_2023.json`]
3. **Group share of traffic s.** The group is 12.1% of residents (CPS 2025). NHTS puts its
   driving per person at 0.874 of others' (2017, southwestern cut; 0.692 in the 2022 national
   file; 0.893 in the 2017 national file). That gives s = 10.8% (8.7–11.0%) of vehicle miles.
   The congestion lane derived the same national φ, 10.8%. [DATA: `congestion_2026_09_23/derived/nhts_ratios.csv`]
4. **Self-exposure q.** Weighted by the group's own traffic, the group's share of traffic in its
   urban areas is **0.299** (`phi_commute_route` in the congestion lane's `ua_exposure.csv`).
   About 30% of the other vehicles a group driver meets are group vehicles, against 10.8% under
   uniform mixing. Residential segregation within metros raises this further, so the low arm
   multiplies q by 1.3. The group's share of non-motorist victims is 26.8% (the Hispanic share
   of known-origin pedestrian deaths in FARS 2023) × 0.589 (the Mexican-origin share of
   Hispanics in CPS 2025) = 15.8%. [CALCULATION]
5. **Group risk per mile m (FARS 2023).** Origin is recorded only for people who die, from death
   certificates. FARS codes Mexican origin separately: 2,635 deaths, against 5,020 coded
   "Hispanic, not specified". Mexican coding is concentrated in Texas (36% of Mexican-coded
   deaths) and Arizona (12%); California is 6.9%. The measure is quasi-induced exposure among
   killed drivers in two-vehicle crashes with exactly one culpable driver. A driver is culpable
   with a behavioural driver-related factor or a moving violation charged. The culpable to
   non-culpable odds ratio against non-Hispanic drivers is:
   - 0.98 for all Hispanics, crude;
   - **1.13** for all Hispanics within states (Mantel–Haenszel);
   - 1.47 for Mexican-coded drivers within states (crude 1.30, CI 1.08–1.58);
   - 0.99 for other Hispanics within states.

   Involvement per mile relative to the average is m = (1 + OR)/2 = 1.063 at the central.
   Killed drivers' traits, Mexican-coded against non-Hispanic:

   | Killed drivers | Mexican-coded | All Hispanic | Non-Hispanic |
   |---|---:|---:|---:|
   | BAC ≥ .08 | 40.6% | 36.3% | 27.3% |
   | No licence (of known) | 22.3% | 17.6% | 4.9% |
   | Pickups | 18.4% | 14.5% | 13.5% |
   | Aged 16–34 | 56% | — | 33% |

   Within states the BAC gaps are smaller: TX 34% against 33%, AZ 36% against 29%, CA 37%
   against 28%. [CALCULATION: `fars_group.py`]
6. **Formulas** (docstring of `crash_model.py`):
   - Multi-vehicle: m·s·(1−q)·M·(x + κ[(1−f)·ins_o − f·ins_g]).
   - Non-motorist: β·m·s(1−q)/(1−s)·(1−h)·P.
   - Single-vehicle: m·s·S·e_sv.
   - Normalized: (a)·(1 − 1/R), with R = 0.888 × 1.063 = 0.944 at the central. R multiplies the
     group's VMT per person relative to the average resident by m.
   - Fault-based: outsider losses in crashes the group's drivers cause, times f = OR/(1 + OR),
     less the liability share κ·ins_g. Drivers are taken to be at fault in half of
     non-motorist crashes [ASSUMPTION], scaled by relative culpability.

**Premiums and liability.** In the but-for comparison the group's liability insurance repays
outsiders about 5.7% of their losses in mixed crashes (κ 0.15 × fault share 0.53 × insured
share 0.72). Outsiders' insurers pay the group about 6.0% of the group's losses in the crashes
outsiders cause. Net, premiums internalise about nothing (the κ term moves the total by
$0.4–1.4bn). Uninsured and unlicensed driving matters in the fault-based variant, where the group
repays 10.8% of the losses it causes. [CALCULATION] The IRC puts uninsured drivers at 15.4%
nationally in 2023 [SOURCE: IRC 2025 summary]. The group's insured share of 0.72 (0.60–0.80) is
an [ASSUMPTION] anchored on the unlicensed rate above; IRC state rates were not retrieved [GAP].
Lueders, Hainmueller and Lawrence (2017) find that California's AB60 licences, more than 600,000
of them in 2015, changed neither crashes nor fatal crashes but cut hit-and-runs. Licensing
therefore moves compensation, not crash frequency. The model accordingly leaves licensing out of
m. [SOURCE: PNAS abstract and introduction; the effect's size was not read, GAP]

## Disconfirmation

- **The volume response could be zero or negative.** Under Parry's assumption the total is $4.3bn.
  With the 2020 death response taken at face value it is $6.6bn: removing the group's traffic
  would then speed traffic enough to raise outsiders' deaths by about as much as it cuts
  non-fatal losses. Both scenarios are inside the grid. The fault-based variant does not depend
  on this input and stays at $46bn.
- **Per-mile risk may not be elevated.** The crude pooled Hispanic odds ratio is 0.98. NHTSA's own
  per-mile rates show Hispanic occupants dying at 0.96 of the white rate per passenger-vehicle
  mile in 2017 (0.69 against 0.72 per 100m person-miles). Pedestrians' rates are similar
  (16.06 against 15.17). [SOURCE: NHTSA DOT HS 813 188, Tables 2–3 and 6, via
  `_cache/disparities.txt`] These rates describe victims, not the risk imposed on others. They
  still argue against a large per-mile multiplier, so the central uses only 1.063.
- **Is the higher culpability real?** The Mexican-coded odds ratio of 1.47 may be a
  death-certificate artefact. Texas records 1,799 Hispanic and only 457 non-Hispanic killed
  drivers, so its non-Hispanic cell looks under-coded. For that reason the central uses the
  all-Hispanic within-state 1.13. [GAP] Surviving drivers' origin is absent from FARS, so no
  non-fatal crash evidence on the group's involvement was used. California's crash records
  (CCRS/SWITRS party race and at-fault flags) would test this directly.
- **Is the normalized sign robust?** No. It is negative whenever the group's VMT ratio times m is
  below 1: at the central, and with the 2022 NHTS ratio of 0.692. It turns positive (up to
  +$15bn) with the Mexican-coded odds ratio and the 2017 national VMT ratio. [FRAMING-SENSITIVE]
- **Steel-man for a higher figure.** Edlin and Karaca-Mandic's national Pigouvian revenue,
  $220bn a year in their dollars and insured costs only, times the group's 10.8% share gives
  about $24bn, or roughly $48bn in 2024 prices (CPI ×2.0 [TRAINING-DATA]). That is above the
  central's insured part before any quality-of-life loss. The group is also concentrated in the
  dense metros where their externality is largest, which the national x does not capture.
  [INFERENCE]

## Double counting

- **Congestion lane.** Blincoe's crash-congestion category ($40.2bn in 2024 terms) is removed.
  The UMR delay that lane prices includes incident delay. The crash-induced emissions inside that
  category leave with it, so nothing overlaps the air-pollution lane.
- **Fiscal account.**
  - EMS ($1.5bn nationally) is removed: police, fire and EMS sit in the account's public-safety
    lines.
  - The group's own public medical costs, lost taxes and uncompensated care are in the account.
    The model counts only outsiders' losses, so they are excluded by construction.
  - Outsiders' public medical costs and lost taxes from crashes with the group are not in the
    account and are included. They are about $1bn of the central (government pays 8.7% of
    economic costs, and economic costs are about a quarter of comprehensive ones [INFERENCE]).
  - Police investigation and court time are in the account's justice and general-government
    lines. Blincoe's legal costs are private (insurer-paid) and stay in.
- **Crime-victim lane.** It explicitly omits impaired-driving crashes
  (`crime_victim_cost_2026_09_23/RESULT.md`, Limits 7), so the two do not overlap.
- **Within this lane.** The fault-based rows are an alternative to the but-for rows; never add
  both. The `component_*` rows are parts of the but-for total.

## What can be added beside the account

[2026-09-28, later: the operator added the **fault-based** absolute row (`road_crash_externality_fault_based`, $45.8bn, $26.3–80.9bn) to the social rows of the fiscal-plus-social total, from the September 27 case on. It does not depend on the traffic-volume elasticity, and it charges crashes the way the account charges crime, by who causes them. The but-for row below and both normalized rows sit beside, never added ([decision](../../../decisions/2026-09-28-social-items-pollution-crashes.md)). The culpability odds ratio is being tested against California's crash records (`ccrs_nonfatal_involvement_2026_09_28`).]

The but-for absolute, **$44.5bn ($5.7–145.1bn)**, can sit beside the fiscal account with the
other social items, as congestion does. It is a real-resource loss borne by other residents,
about 98% private (injury and life-quality losses, property) and about $1bn taxpayer-borne. It
is not keyed to any budget line, so it does not move with the main case's service responses.
Two caveats go with it. The figure depends on the traffic-volume response, the weakest link,
and a reader who takes Parry's view would put it near $4bn. The normalized figure is about zero,
so the group's roads are about as dangerous to others per resident as an average group's.
[FRAMING-SENSITIVE] Do not scale it onto the generation ledger.

**Noise** is not priced. Older FHWA cost-allocation estimates put car noise near 0.1¢ a mile
[TRAINING-DATA, not verified]. On 350bn miles that is well under $1bn, small against crashes.
[INFERENCE]

## Files covered and skipped

Covered:

| File or source | Used for |
|---|---|
| `_cache/blincoe_2023_dot_hs_813403.pdf` (read as `_cache/blincoe.txt`) | Tables 1-1, 1-8, 3-4, 3-6, 12-1, 12-2, 12-7, 12-8, 15-4, 15-5; VSL text |
| `_cache/tsf2023.pdf` (NHTSA DOT HS 813 738) | Tables 1, 2, 28, 29 |
| `_cache/FARS2023NationalCSV.zip` | person, vehicle, accident, MIPER, driverrf, violatn, via `fars_group.py` |
| `_cache/irc_um_uim_2017_2023.pdf` | IRC research summary (national uninsured and underinsured rates) |
| `_cache/nhtsa_disparities_813188.pdf` | per-mile fatality rates by race and ethnicity |
| Exa pages: EKM (JPE abstract, escholarship working-paper text); Parry 2004 abstract; Lueders et al. PNAS abstract and introduction; USDOT VSL table; Braver 2003 and Raifman & Choma 2022 abstracts | parameters and cross-checks |
| `congestion_2026_09_23/derived/ua_exposure.csv`, `nhts_ratios.csv`, `RESULT.md` | q, NHTS ratios, overlap |
| `crime_victim_cost_2026_09_23/derived/target_population_cps2025.csv` | N and the Mexican share of Hispanics |

Skipped:

| Source | Reason |
|---|---|
| Parry, Walls & Harrington 2007 full text | paywalled; the Parry 2004 abstract stands in |
| EKM PDF | escholarship returned CloudFront 403; figures come from the abstract and working-paper excerpt |
| IRC state table | full report paywalled |
| Lueders effect size | full text not fetched; only the direction is used |
| FARS 2022 | download truncated (curl exit 56); 2023 used |
| California CCRS/SWITRS and Texas CRIS party-level race | would measure non-fatal at-fault involvement and insurance by origin; not pulled for time [GAP] |
| Anderson & Auffhammer 2014 (vehicle-weight externality) | not read; the pickup share gap (18.4% against 13.5%) is left unpriced [GAP] |

Next queries if re-dispatched:

- data.ca.gov CCRS parties (RaceDesc, IsAtFault) for quasi-induced exposure on injury crashes;
- Dickerson, Peirson & Vickerman (2000, EJ) and Green, Heywood & Navarro (2016, JUE) on the
  volume elasticity;
- the 2020 volume response by state density.

## Reproduce

```sh
# from the repository root; FARS 2023 CSV zip and PDFs are in _cache/ (ignored)
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/road_crash_externality_2026_09_28/fars_group.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/road_crash_externality_2026_09_28/crash_model.py
```

## Log (times from `date`)

- 2026-09-28 20:55 JST — stub written; reading the congestion lane's method and parameters next.
- 2026-09-28 21:24 JST — sources in `_cache/`:
  - Blincoe et al. 2023 (DOT HS 813 403), all 2019 $:
    - comprehensive $1,365.4bn, economic $339.8bn;
    - congestion $36.0bn, EMS $1.35bn;
    - pedestrians $112.5bn, bicyclists $32.2bn;
    - VSL $10.9m;
    - Table 15-5 payers: government $29.5bn, insurers $182.5bn, other $48.6bn, self $79.2bn.
  - IRC 2025 summary: 15.4% of drivers uninsured in 2023, 18.0% underinsured.
  - NHTSA 813 188 (disparities).
  - FARS 2023 national CSV.
- Between 21:24 and 21:37 JST (no `date` call; two entries were first stamped 21:40 and 21:55 by
  estimate, corrected here):
  - `fars_group.py` → `derived/fars_group_2023.json`. Killed drivers, Mexican-coded against
    non-Hispanic: BAC ≥ .08 40.6% vs 27.3%, no licence 22.3% vs 4.9%, pickups 18.4% vs 13.5%.
    Culpability odds ratio 1.30 crude and 1.47 within states; all Hispanic 1.13 within states.
  - TSF 2023: the 2019→2020 volume experiment. Named sources: USDOT VSL, Parry 2004, EKM 2006,
    Lueders 2017.
- 2026-09-28 21:37 JST — `crash_model.py`:
  - the positive control passes: kept 2019 base $1,328,059m against $1,328,060m;
  - central (a) $44.5bn, (b) −$2.6bn, fault-based $45.8bn;
  - scenarios written to `derived/scenarios.json`.
- 2026-09-28 22:43 JST (lead): the operator added the fault-based row to the social rows of the fiscal-plus-social total (decision 2026-09-28-social-items-pollution-crashes); lane outputs unchanged.
