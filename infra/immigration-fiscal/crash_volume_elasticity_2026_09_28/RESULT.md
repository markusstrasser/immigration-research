**Verdict:** Graded and weighted toward the congested metros where the group drives, the evidence puts the cost-weighted non-fatal x at about **+0.07** (band −0.23 to +0.52) and the fatal x at about **−0.21** (band −1.55 to −0.16). The crash lane's non-fatal 0.6 lies above the non-fatal band and its fatal 0 lies just above the fatal band. Extra traffic raises minor crashes more than in proportion (PDO x ≈ +1.4). It leaves minor injuries about proportional (x ≈ 0) and lowers others' serious and fatal risk in congested traffic by slowing it (x ≈ −0.2, with congested-core experiments down to −1.65). About 90% of multi-vehicle non-fatal cost is injury rather than PDO, so the net comes out near zero. Re-running the crash lane as it stands, `evaluate_split` with California's non-fatal culpability, gives a but-for central of **$9.3bn**, against $42.5bn at the lane's old x. The full grid runs **−$63.7bn to +$63.2bn**, against $4.2–137.7bn. The upper tail falls by more than half, but the grid is only slightly narrower ($127bn wide against $133bn) and now straddles zero: in dense traffic the evidence disagrees on the sign. The adopted fault-based row ($42.3bn, $23.8–73.3bn) does not use x and is unchanged. The US is not structurally different on non-fatal crashes. It was different in 2020 on deaths: deaths rose 7% in dense and rural states alike while Europe's fell with traffic, and ITF/NHTSA attribute the US rise to impairment, speeding and belt non-use. [CALCULATION: `x_band.py` → `derived/x_band.json`, `derived/butfor_recomputed.json`] [FRAMING-SENSITIVE: exposure weighting and cost weighting]
claude-opus-5-5

# Crash rate vs traffic volume: x = ε − 1 by severity, and the crash lane's but-for re-run

Lane opened 2026-09-28 23:01 JST (from `date`). The volume elasticity x is the per-mile crash-rate
elasticity to traffic on a fixed network (ε is the crash-count elasticity, so x = ε − 1). Nothing in
`road_crash_externality_2026_09_28/` was edited; its `evaluate_split` (the lane as it stands) and
`evaluate` (the pre-revision function) are imported read-only through importlib. Nothing committed.
Revised after the lead's review (Block 3 below): NYC's serious-or-fatal estimate added, verdict moved
to `evaluate_split`.

## Verdict table

| Parameter | Lane today (low / central / high) | Evidence central | Band: bootstrap 10–90% of the central | Spread across settings (weighted IQR) |
|---|---|---:|---:|---:|
| x PDO (9.5% of multi-vehicle non-fatal cost) | — | +1.43 | — | +0.58 to +3.26 |
| x minor injury, MAIS 1–2 (47.7%) | — | 0.00 | — | −0.45 to +1.36 |
| x serious injury, MAIS 3–5 (42.8%) | — | −0.16 | — | −1.65 to +0.05 |
| **x non-fatal (cost-weighted)** | 0.2 / 0.6 / 1.0 | **+0.07** | **−0.23 to +0.52** | −0.86 to +0.98 |
| **x fatal** | −0.3 / 0 / 1.0 | **−0.21** | **−1.55 to −0.16** | −1.65 to +0.10 |

Rule, fixed before the numbers were seen (docstring of `x_band.py`):
- **Design weights.** Natural experiment 3, or 2 when x combines two specifications or is very
  imprecise. National 2019→2020 before-after 1. Panel 1. Handbook assumption 0.5. Cross-section 0.
- **Setting weights.** Dense congested settings carry the group's share of commute vehicle-minutes in
  urban areas with a travel-time index of at least 1.30, plus half the share at 1.20–1.30: 0.648.
  Mixed, national and sparse settings carry 0.352. [CALCULATION from `ua_exposure.csv`]
- **Central.** The weighted median per severity class, with the non-fatal classes combined by the
  lane's own Blincoe multi-vehicle cost shares. Serious-or-fatal estimates (London IV, German
  strikes, NYC) also enter the fatal class at half weight.
- **Band.** A resampling of estimates within each severity-by-setting bin (2,000 draws). It measures
  uncertainty in the central. Because medians jump between data points, its ends are coarse. The
  IQR column instead measures how much settings differ from each other. [CALCULATION]

## Evidence table

ε is the crash-count elasticity and x = ε − 1. "Dense" means a congested city core or peak, or the
densest state.

| Study | Setting (density) | Design (grade) | Severity | ε | x |
|---|---|---|---|---:|---:|
| Tang & van Ommeren 2022, J Econ Geog | Central London charge zone, IV on flow (dense) | natural experiment (A) | injury accidents / slight / serious+fatal | 0.64 / 0.81 / −0.65 | −0.36 / −0.19 / −1.65 |
| Green, Heywood & Navarro 2016, JPubE | Central London charge zone, DiD vs 20 cities (dense) | natural experiment, x combines two specs (A−) | injury accidents / serious+fatal / fatal | 2.36 / 1.58 / 2.36 | +1.36 / +0.58 / +1.36 |
| NYC Congestion Relief Zone (Itzkowitz … Morrison, AJE 2026, Table 1; MTA VMT −7.1%) | Manhattan CBD (dense) | natural experiment (A). Crash data January–June 2025 (6 months); the VMT change is MTA's first-year figure | non-injury / injury-or-fatal / serious-or-fatal | 1.58 / 0.55 / 0.84 | +0.58 / −0.45 / −0.16 (all CIs span 0) |
| Bauernschuster, Hener & Rainer 2017, AEJ:EP | 5 German cities, am peak, transit strikes (dense) | natural experiment, composition shifts (A) | crashes / slight / serious+fatal | 3.2–5.4 / 4.3–7.4 / ≈ −1.5 to −0.9 (imprecise) | +2.2–4.4 / +3.3–6.4 / −2.5 to −1.9 |
| same, denominator car-hours (+11–13%) | as above | as above | crashes | 1.1–1.3 | +0.1–0.3 |
| Edlin & Karaca-Mandic 2006, JPE | California; low-density states (dense; sparse) | state panel, IV (C) | insured losses (liability + collision) | 3.3–5.4; ≈1 | +2.3–4.4; ≈0 |
| Dickerson, Peirson & Vickerman 2000, Economica | London hourly counts × accidents (mixed flows) | within-road time series (B) | all | abstract only | ≈0 at low–moderate flow, "increases substantially at high flows" [GAP: number] |
| Bello 2021, Economic Inquiry | Ticino border, exchange-rate shock (moderate) | natural experiment (A) | injury accidents, late morning non-working days | "larger than 1" | >0 [GAP: number] |
| Fridstrøm, TØI 402/1998 (Norwegian county model) | Norway, monthly 1974–94 (sparse) | panel (C) | injury accidents (fixed network) / deaths (constant density) | 0.50 / 0.761 | −0.50 / −0.24 (fixed network lower) |
| US 2019→2020, TSF 2023 | US national (mixed) | national before-after (D) | PDO / injury crashes / injured / deaths | 2.43 / 1.59 / 1.57 / −0.61 | +1.43 / +0.59 / +0.57 / −1.61 |
| US states 2019→2020, FHWA VM-2 + FI-20 | most urban third; other two thirds (dense; mixed) | national before-after (D) | deaths | −0.55; −0.66 | −1.55; −1.66 |
| GB 2020, DfT RRCGB 2020 Table 1 | Great Britain (mixed) | national before-after (D) | slight / serious / fatal | 1.22 / 1.05 / 0.79 | +0.22 / +0.05 / −0.21 |
| ITF/IRTAD 2021, 11 countries with vkm | AU CA DK FI FR GB DE JP NL SI SE (mixed) | national before-after (D) | deaths | ≈1.0–1.2 | ≈0 to +0.2 [INFERENCE: "slightly decreased" risk] |
| CE Delft 2019 EU Handbook | EU urban; motorway and other (both) | assumption (E, weight 0.5) | casualties | 1.0; 0.75 | 0; −0.25 |
| HSM urban/suburban arterials, single-vehicle SPFs | US segments | cross-section, never central | single-vehicle | 0.47–0.81 | −0.53 to −0.19 |
| HSM rural divided segment SPF | US segments | cross-section, never central | all | 1.049 | +0.05 |

Two patterns hold across settings:
- **x falls with severity almost everywhere.** PDO > minor > serious > fatal holds in the US 2020
  data, GB 2020, London (Tang & van Ommeren), the German strikes and Edlin & Karaca-Mandic's
  frequency-versus-severity split. More traffic brings more low-speed interactions and lower speeds.
  NYC is the partial exception. Its PDO estimate sits above its injury estimates, but its
  serious-or-fatal x (−0.16) sits above its injury-or-fatal x (−0.45), and every NYC CI spans zero.
- **Sign disagreement is concentrated in dense traffic.** In the same London zone, Green et al.
  find x = +1.4 and Tang & van Ommeren find −0.36 for injury accidents. The German strikes give +2 to
  +4 per car and +0.1 to +0.3 per car-hour. [CALCULATION: `derived/evidence.csv`]

## The crash lane's but-for, re-run

The lead rows use `evaluate_split`, the crash lane as it stands (with CCRS non-fatal culpability,
19,683 combinations). The `evaluate` rows are the pre-revision comparison the lead first asked for
(6,561 combinations). The other inputs are held at the lane's central except in the grid column.
$bn, 2024 prices. [CALCULATION: `derived/butfor_recomputed.json`]

| Case | Central | Other inputs at central | Full grid |
|---|---:|---:|---:|
| Lane today, `evaluate_split`, old x (0.2/0.6/1.0, −0.3/0/1.0) | 42.5 | 14.5 – 85.1 | 4.2 – 137.7 |
| **Evidence band (bootstrap), `evaluate_split`** | **9.3** | −34.7 – 34.8 | **−63.7 – 63.2** |
| Evidence spread across settings (IQR), `evaluate_split` | 9.3 | −71.3 – 65.3 | −117.3 – 107.9 |
| Fault-based row, adopted (`evaluate_split`; does not use x) | 42.3 | — | 23.8 – 73.3 |
| Pre-revision `evaluate`, old x | 44.5 | 15.2 – 88.5 | 5.7 – 145.1 |
| Pre-revision `evaluate`, evidence band (bootstrap) | 9.4 | −35.6 – 36.6 | −65.6 – 67.0 |
| Pre-revision `evaluate`, fault-based | 45.8 | — | 26.3 – 80.9 |

The table below crosses the new levels, `evaluate_split`, with the other inputs at central:

| x non-fatal \ x fatal | −1.55 | −0.21 | −0.16 |
|---|---:|---:|---:|
| −0.23 | −34.7 | −6.6 | −5.5 |
| +0.07 | −18.9 | **9.3** | 10.3 |
| +0.52 | 5.6 | 33.8 | 34.8 |

The normalized row at the new central is −$1.1bn under `evaluate_split`. It was −$0.84bn at this
lane's first central, is −$5.1bn at the crash lane's old x, and is −$0.6bn under `evaluate`.
The total moves linearly in x. Under `evaluate_split`, each 0.1 of x non-fatal is worth $5.4bn and
each 0.1 of x fatal $2.1bn; under `evaluate` the figures are $5.8bn and $2.1bn. [CALCULATION:
`x_band.json` `butfor_slope_per_0.1`]

This re-run leaves out a composition term that the lead is adding to the crash lane. When the
group's drivers are at fault more often (r > 1) and x < 1, removing them lowers others' risk:
- in multi-vehicle crashes, by s(1−q)M(r−1)(1−x)/2;
- for non-motorists, by F(r−1)(1−β)·nm_scale·NM.

That adds about +$1.8bn at the central, so the crash lane's revised figures will differ from the
ones above.

**Recommendation.** Keep the fault-based row as the account row; the evidence gives it more reason
than before. In the but-for row, replace the x levels with −0.23 / +0.07 / +0.52 and −1.55 / −0.21 /
−0.16. Present the row as "about $9bn; the sign is not established". The $42.5bn central rests on
x = 0.6, and the graded evidence does not support that value for injury-weighted costs. The case for
a high x rests on counts dominated by minor crashes and on insured losses. [INFERENCE]

[Lead, 2026-09-28 23:50 JST, dissenting on the first sentence: the account's absolute column compares other residents
with and without the group. Near x = 0, the crashes others have with the group's drivers would largely happen anyway
without the group, as crashes among themselves; the fault-based row still charges for them, so it overstates that
comparison. The evidence therefore argues for the but-for as the account row, not for the fault-based row. The crash
lane now carries these x levels and the composition term: but-for $11.1bn (−$57.7bn to +$74.3bn). The switch is
proposed to the operator; it is his decision. [INFERENCE]]

## Is the US different?

The answer differs by severity.

- **Non-fatal: same direction.** In 2020 the US injury-crash x was +0.59 and the PDO x +1.43, against
  +0.22 for slight and +0.05 for serious casualties in Great Britain. The US response is somewhat
  larger, but both show crashes falling faster than traffic. Some of the drop may be fewer minor
  crashes reported to police, which affects both countries. [INFERENCE]
- **Fatal: the US was an outlier in 2020.** US deaths rose 7.3% as VMT fell 11.0% (x −1.61). Across
  the eleven ITF countries with vehicle-km data, traffic fell 12.2% and deaths per vehicle-km
  "slightly decreased" (x ≈ 0 to +0.2). In Great Britain x was −0.21. ITF names only the US,
  Switzerland and Ireland as having more deaths in 2020 than their 2017–19 average. Without the US,
  deaths in the 34 IRTAD countries fell 19.2%. [SOURCE: ITF 2021]
- **It is not road mix or density.** In the FHWA state data, deaths rose about 7% in each urbanisation
  third. In the most urban third the elasticity is −0.55, against −0.73 in the least urban.
  Massachusetts (VMT −16.6%, deaths +2.7%), New Jersey and California moved like rural states.
  [CALCULATION: `state_2020.py`]
- **Explanation.** ITF: "The main factors behind this increase include impaired driving, speeding and
  failure to wear a seat belt (NHTSA, 2021a)". It also notes that speeding and drink-driving data were
  too thin in other countries to compare. [SOURCE: ITF 2021, quoting NHTSA]
  - **Speed** is a volume channel. Emptier roads are faster everywhere, and the congested-core
    experiments find the same sign: serious and fatal x = −1.65 in London and −0.16 in NYC.
  - **Belt non-use and impairment** were a 2020 behavioural shock, larger in the US.
  - The US 2020 fatal x of −1.6 therefore overstates the pure volume effect. The fatal central (−0.21)
    sits with Europe and the fixed-network models. Its low end keeps the US and London values.
    [INFERENCE]
- **Transfer.** The dense natural experiments transfer in mechanism. US metros put more traffic on
  freeways, where decongestion raises speeds more than in a London or Manhattan grid. That argues for
  a US fatal x at or below the European value, not above it. [INFERENCE] Seat-belt and impairment
  rates were not retrieved for the comparison. [GAP]

## Disconfirmation

- **Steel-man for a high x.** Edlin & Karaca-Mandic find x = 2.3–4.4 on California insured losses.
  The German strikes give +2 to +4 for crashes and +3 to +6 for slight injuries per car. Green et al.
  find +1.4 in London. Dickerson et al. report a steep rise at high flows. Bello finds ε > 1, and the
  US 2020 injury x is +0.59.
  - If the group's peak driving in congested metros followed these, x non-fatal could be 1 or more.
    The but-for would then be at or above $64.1bn (`evaluate_split` at x 1.0 / 0).
  - The rule discounts this for three reasons. These estimates are counts dominated by minor crashes
    or insured losses; injuries are 90% of the cost. And two natural experiments in the same kind of
    congested core (London IV, NYC DiD) find x ≤ 0 for injuries.
  - If Edlin & Karaca-Mandic is moved into the minor-injury class, the central barely moves.
    [INFERENCE]
- **Fragility.** Dropping one study at a time moves the non-fatal central between −0.10 and +0.31.
  The low end comes from dropping the German strikes or all US 2020 rows, the high end from dropping
  NYC. The fatal central moves between −0.25 (drop Green et al.) and −0.16 (drop Tang & van Ommeren).
  In but-for terms (`evaluate_split`, other inputs at central) that is $0.0bn to $21.7bn. Before the
  NYC serious-or-fatal row was added, dropping Green et al. sent the fatal central to −1.55; that
  fragility is gone. [CALCULATION: `x_band.json` `leave_one_study_out`, `butfor_at_sensitivity_centrals`]
- **Handbook assumptions at weight 0.** The non-fatal central becomes +0.17 and the fatal −0.24, a
  but-for of $14.4bn. [CALCULATION]
- **Exposure weighting.** [FRAMING-SENSITIVE]
  - Dense evidence alone gives x +0.15 / −0.16 ($14.8bn).
  - Mixed and national evidence alone gives +0.13 / −0.24 ($11.9bn).
  - Equal weights give +0.17 / −0.24 ($14.4bn).
- **Multi-vehicle crashes against all crashes.** The lane's x applies to multi-vehicle crashes. Most
  estimates above cover all crashes, including single-vehicle crashes and pedestrians. The HSM
  cross-sections put single-vehicle AADT exponents at 0.47–0.81: single-vehicle risk per mile falls
  with volume. A multi-vehicle-only x is therefore likely above the all-crash x, and the +0.07 may be
  low. [GAP: CRSS/TSF 2019–2020 split by number of vehicles not pulled; NHTSA returned a TLS error]
- **Measurement.**
  - NYC's crash data cover January–June 2025 (6 months). MTA's VMT −7.1% is the first-year figure, so
    the two windows differ.
  - Green et al.'s x combines a monthly-count and an annual-rate specification.
  - The ITF fatal figure is inferred from "slightly decreased".
  - The GB figures use rounded published changes.
  - 2020 PDO counts may be inflated by lower police reporting.
- **Heterogeneity is real.** The weighted IQR (non-fatal −0.86 to +0.98) is wider than the lane's
  grid. The evidence identifies the shape (x falls with severity) better than the level.

## Files covered and skipped

Covered:

| Source | Used for |
|---|---|
| EKM final working paper (escholarship qt2h23t6rt, via Exa full text) | California elasticities, low-density states, frequency against severity |
| Bauernschuster et al. AEJ:EP full text (Exa library) | Table 4, car count and car-hours |
| CE Delft 2019 Handbook v1.1 full text | risk elasticities, Sommer et al., Lindberg |
| ITF/IRTAD Road Safety Annual Report 2021 PDF text | 11-country vkm, deaths, US reasons |
| Green, Heywood & Navarro Lancaster WP (`_cache/ghn_2014_wp.pdf`) | counts, rates, serious and fatal |
| Tang & van Ommeren TI DP 20-080 / SSRN abstract | x by severity |
| NYC: MTA anniversary release; Itzkowitz … Morrison AJE 2026 Table 1 (Exa highlights; the lead verified the serious-or-fatal row); MDPI Safety 2026 abstract | VMT −7.1%, IRRs |
| DfT RRCGB 2020 (gov.uk, Exa crawl) | Table 1 |
| FHWA Highway Statistics 2019/2020 VM-2, FI-20 (`_cache/*.html`) | state VMT and deaths |
| Fridstrøm TØI 402/1998 summary; Fridstrøm ITF 2011 DP (Exa highlights) | Norway elasticities |
| HSM ch. 12 via NCHRP 17-54 excerpt; SPF guide example | cross-section exponents |
| Retallack & Ostendorf 2019 abstract | review: linear dominates; U-shape with finer data |
| crash lane `crash_model.py` (imported), congestion lane `ua_exposure.csv` | re-run, exposure |

Skipped:

| Source | Reason |
|---|---|
| Dickerson et al. 2000 full text | Wiley paywall; research MCP `fetch_paper` failed for every DOI tried; Kent repository has no PDF |
| Li, Graham & Majumdar 2012 | not fetched (fetch_paper failed); the two London studies above cover the setting |
| Lindberg 2001 | read through CE Delft's citation only (−0.25) |
| Bello 2021 full text | abstract only; ε > 1 without a number |
| Wegman & Katrakazas 2021 | the ITF 2021 report is the same authors' analysis |
| ITF per-country figures (Figures 4, 17) | graphics, not text |
| NHTSA TSF 2019/2020 PDFs | curl TLS error (rc 35); multi- against single-vehicle split for 2020 not computed |
| Ferrante 2026 SSRN (NYC) | abstract not returned |
| US state injury crashes | not pulled for time |

Next queries if reopened:
- CRSS 2019/2020 (injury and PDO by number of vehicles) for a multi-vehicle 2020 x;
- Dickerson et al. Table (flow bands);
- Bello's elasticity table;
- NYC CRZ 12-month follow-up by severity;
- Sommer et al. 2002 design.

## Reproduce

```sh
# from the repository root; FHWA HTML and PDFs in _cache/ (ignored); fetch with fetch_sources.sh
OPENBLAS_NUM_THREADS=1 uv run --no-project --with lxml python3 infra/immigration-fiscal/crash_volume_elasticity_2026_09_28/state_2020.py
OPENBLAS_NUM_THREADS=1 uv run --no-project --offline python3 infra/immigration-fiscal/crash_volume_elasticity_2026_09_28/x_band.py
```

## Findings (appended as verified)



### Block 1 — 2026-09-28 23:07 JST: first primary texts read

- **Edlin & Karaca-Mandic (2005 final WP = JPE 2006), state panel 1987–1995, state and year FE, IV on
  registered vehicles and licensed drivers per lane-mile.** "In California, a 1% increase in driving
  raises insurer costs by roughly 3.3%, according to Specification (3), our linear model, and by 5.4%,
  according to Specification (10)." So ε(insured cost) = 3.3–5.4 and x = 2.3–4.4 in the densest state.
  Low-density states: "small economically insignificant and generally statistically insignificant"
  (South Dakota −$50 ± 57 to $127 ± 60 per driver). Decomposition: density "appear[s] to consistently
  increase accident frequency, but not severity. The severity of accidents may fall somewhat with
  increases in density in low density states, and rise in high density states." Insured costs are
  liability + collision (PDO and bodily injury), not deaths. [SOURCE: escholarship qt2h23t6rt, text
  in `_cache/exa/ekm.txt`] Grade: panel (within-state changes over 9 years; density growth is not
  exogenous, and CA's claims environment changed over 1987–95) [INFERENCE].
- **Bauernschuster, Hener & Rainer (2017, AEJ:EP), 71 transit strikes, five largest German cities,
  2002–2011, city-day am/pm peaks.** Morning peak: car hours +11 to 13%, "a 2.5 to 4.3 percent increase
  in the number of cars on roads and a 8.4 percent increase in travel times"; vehicle crashes +0.607 on
  a base of 4.280 (+14.2%, p = 0.07); slightly injured +0.790 on 3.940 (+20.1%); seriously or fatally
  injured −0.013 (s.e. 0.055) on 0.354 (no effect). Evening peak: all insignificant; seriously or
  fatally injured −0.093 (s.e. 0.055) on 0.648. [SOURCE: AEJ:EP text, Table 4, via
  `_cache/exa/bhr.txt`] Against the car count (+2.5–4.3%), crash ε ≈ 3.3–5.7 and slight-injury
  ε ≈ 4.7–8.0; against car hours (+11–13%), crash ε ≈ 1.1–1.3. [CALCULATION: 14.2/4.3, 14.2/2.5,
  20.1/4.3, 20.1/2.5, 14.2/13, 14.2/11] Strike days also move inexperienced drivers, cyclists and
  walkers onto the street, so ε against cars overstates a pure volume effect [INFERENCE]. Grade:
  natural experiment, dense peak traffic, one hour-band.
- **CE Delft (2019, v1.1) EU Handbook.** Recommends a risk elasticity (casualty risk per vkm vs vkm) of
  **0 for urban roads and −0.25 for motorways and other roads**; cites Sommer et al. (2002, Switzerland)
  −0.5 motorway, −0.25 urban, −0.62 other; Lindberg (2001) and Ricardo-AEA et al. (2014) −0.25; "All
  suggested risk elasticities are negative" (Hesjevoll & Elvik 2016). [SOURCE: handbook text,
  `_cache/exa/cedelft.txt`] These are assumptions for casualties (injury + fatal), not estimates of
  crash counts; Sommer is a cross-section/time-series model [GAP: Sommer design not read].
- **ITF/IRTAD Road Safety Annual Report 2021.** Eleven countries with vkm data (Australia, Canada,
  Denmark, Finland, France, GB, Germany, Japan, Netherlands, Slovenia, Sweden): traffic −12.2% in 2020
  vs 2017–19; "the number of road fatalities per billion vehicle-kilometres travelled slightly
  decreased", i.e. fatal ε ≈ 1 or a little above, x_fatal ≈ 0 to slightly positive. Spread: Sweden −17%
  risk, Netherlands +12%; GB fatality rate +6% vs 2019. US: VMT −13.2% (ITF's figure; FHWA final
  −11.0%), deaths +7.2%, fatal crashes +5.1% vs 2017–19. Excluding the US, deaths in 34 IRTAD
  countries fell 19.2%; with it, 8.6%. [SOURCE: ITF 2021 PDF text, `_cache/exa/itf.txt`]
- [GAP] per-country 2020 vkm and death changes are in Figures 4 and 17 (graphics, not text); GB is
  taken from DfT below.

### Block 2 — 2026-09-28 23:17 JST: London, NYC, GB 2020, US states

- **Tang & van Ommeren (2022, J Econ Geography; TI DP 20-080), London Congestion Charge, IV on traffic
  flow.** "The charge attributed to a 9.4% reduction in traffic flow, which resulted in a less than
  proportional 6.0% and 7.6% decrease in accidents and slight injuries, and a 6.5% increase in serious
  injuries/fatalities. ... rate elasticities with respect to traffic flow are −0.36, −0.19 and −1.65"
  (these are x directly); "marginal external benefit of road safety from an additional kilometre driven
  is approximately £0.16". [SOURCE: SSRN 3736929 / TI DP abstract via Exa] STATS19 counts only injury
  accidents, so "accidents" here are injury accidents. Grade: natural experiment (IV), congested core.
- **Green, Heywood & Navarro (2016, JPubE; Lancaster WP 2014), same charge, DiD against 20 UK cities.**
  Count: "approximately 40 fewer accidents per month in the CCZ ... pre-policy monthly average ... 111
  ... roughly a 35 percent decline"; rate: "almost exactly 1 fewer accident per million miles ... pre-
  policy ... 4.51 ... the rate fell approximately 22 percent"; serious and fatal −25%, fatal −35%
  (43 and 4.3 a year). [SOURCE: `_cache/ghn_2014_wp.txt`] Implied miles 0.65/0.78 = 0.833, so injury-
  accident x ≈ +1.36, serious+fatal x ≈ +0.58, fatal x ≈ +1.36 [CALCULATION; combines a monthly-count
  and an annual-rate specification, so rough]. The two London studies disagree in sign; TvO measures
  flow at count points and instruments it, GHN compares London's zone with other cities' trends.
- **NYC Congestion Relief Zone, 2025.** MTA/Governor, first anniversary: "over 73,000 fewer vehicles
  are entering the zone, an 11 percent reduction ... total Vehicle Miles Traveled (VMT) down by 7.1
  percent". [SOURCE: mta.info press release, via Exa] Morrison et al. (Am J Epidemiol 2026), CRZ vs
  control zone: all crashes IRR 0.92 (0.87–0.97); non-injury 0.89 (0.81–0.98); injury or fatal 0.96
  (0.88–1.06); pedestrian 0.96 (0.83–1.12); cyclist 0.98 (0.81–1.18). [SOURCE: AJE 195(9):2487
  highlights via Exa] On VMT −7.1%: x(all) ≈ +0.13, x(PDO) ≈ +0.58, x(injury+fatal) ≈ −0.45, each
  with CIs spanning zero [CALCULATION in `x_band.py`]. A ZIP-level DiD (MDPI Safety 12(3):64, 2026)
  finds no significant change in crashes or injuries [SOURCE: abstract]. Grade: natural experiment,
  first 6–12 months.
- **Great Britain 2020 (DfT RRCGB 2020, Table 1, adjusted).** Traffic −21% (286bn vehicle miles);
  casualties −25%; fatalities −17% (1,460); KSI −22%; serious −22%; slight −25%. [SOURCE: gov.uk
  release via Exa crawl] x: slight +0.22, serious +0.05, fatal −0.21 [CALCULATION: ln(1+Δc)/ln(0.79) − 1
  on the rounded published changes].
- **US states 2019→2020 (FHWA Highway Statistics VM-2 and FI-20).** Deaths rose about 7% in every
  urbanisation tercile: least urban (urban VMT share 0.29–0.52) VMT −8.9%, deaths +7.1%, ε −0.73;
  middle VMT −10.6%, deaths +7.5%, ε −0.64; most urban (0.72–0.95) VMT −11.8%, deaths +7.2%, ε −0.55.
  Massachusetts VMT −16.6%, deaths 334→343; New Jersey −15.2%, 559→584; California −12.0%,
  3,606→3,847; Maryland −15.5%, 521→567. All states: VMT −11.0%, deaths 36,113→38,735 (+7.3%),
  ε −0.60. [DATA: `_cache/vm2_2019.html` etc.; CALCULATION: `state_2020.py` → `derived/state_2020.csv`]
  The US 2020 fatal rise is not a rural or low-density artefact: dense states moved the same way.
- **Group exposure (congestion lane `ua_exposure.csv`).** 53.4% of the group's commute vehicle-minutes
  are in urban areas with a travel-time index ≥ 1.30 (others 38.9%), 22.6% at 1.20–1.30, 23.9% below
  1.20; very large areas 45.6%; Los Angeles alone 15.4% (TTI 1.64). Peak share of commute
  vehicle-minutes 0.631 (others 0.703). [CALCULATION]
- [GAP] Dickerson et al. (2000) and Bello (2021) give only directions in their abstracts (x ≈ 0 at
  low–moderate flow, rising at high flow; injury-accident ε > 1 in Ticino); numbers not read.

### Block 3 — 2026-09-28 23:45 JST: lead review

- **NYC serious-or-fatal row added.** The AJE study's Table 1 gives "Crashes involving serious injury or
  fatality … 0.94 (0.71-1.24)". The Exa highlight in Block 2 showed it truncated ("…94 (0.7…–1.24)");
  the lead verified it. On VMT −7.1%, x = −0.16 [CALCULATION]. It enters the serious class and, at
  half weight, the fatal class, as the London IV and German strike rows do. The rule would have
  included it; leaving it out was an extraction miss.
- **Correction to Block 2.** The AJE study's first author is Itzkowitz (Block 2 said "Morrison et al.").
  Its crash data cover January–June 2025, 6 months, not "6–12 months". MTA's VMT −7.1% is the
  first-year figure.
- **What moved.**
  - x non-fatal central +0.03 → +0.07; band −0.69/+0.47 → −0.23/+0.52.
  - x fatal central −0.24 → −0.21; band −1.65/0.00 → −1.55/−0.16.
  - Serious-class median −0.25 → −0.16.
  - Dense-only sensitivity −0.49/−1.55 → +0.15/−0.16.
  - Assumptions at weight 0: +0.26/−1.55 → +0.17/−0.24.
  - Leave-one-out ranges: non-fatal −0.66…+0.31 → −0.10…+0.31; fatal −1.55…−0.21 → −0.25…−0.16.
  - `evaluate_split` but-for $6.6bn → $9.3bn; grid −$103.5bn…+$64.0bn → −$63.7bn…+$63.2bn;
    normalized −$0.84bn → −$1.14bn.
  - `evaluate` $6.6bn → $9.4bn.
  [CALCULATION: rerun of `x_band.py`, rc 0]
- **Verdict now leads with `evaluate_split`.** That function is the crash lane as it stands, with the
  adopted fault-based row at $42.3bn ($23.8–73.3bn). The `evaluate` figures remain as the
  pre-revision comparison.

## Log

- 2026-09-28 23:07 JST — block 1 appended (EKM, BHR, CE Delft, ITF 2021).
- 2026-09-28 23:17 JST — block 2 appended (TvO, GHN, NYC CRZ, GB 2020, US states, exposure).
- 2026-09-28 23:23 JST — `x_band.py` run (rc 0): x non-fatal +0.03 (−0.69 to +0.47), x fatal −0.24 (−1.65 to 0.00); but-for $6.6bn (−108.9 to +67.4); verdict and final sections written.
- 2026-09-28 23:45 JST — lead review: NYC serious row added; verdict on evaluate_split. `x_band.py` rerun (--offline, rc 0).
