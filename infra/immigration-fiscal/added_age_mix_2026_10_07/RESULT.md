claude-opus-5-5

**Verdict:** Priced at their measured ages, v5's 3.04M added people cost **$1.35bn more at the low end and $2.86bn
more at the high end** on the set: **$391.6–464.1bn** against v5's $390.3–461.2bn (SE 0.26 / 0.37 from the loss
rates; 5–95% +0.89–1.78 / +2.26–3.44). On the cash set the change is −$0.27 / +$1.92bn: $307.1–385.3bn against
$307.4–383.4bn. The end specifications stay 48 and 11. [CALCULATION: `derived/age_mix_bands.csv`, `derived/summary.json`]

- **The direction v5 guessed holds, but the reason it gave does not.** The 1.94M people lost at the third-generation
  rate are not younger than the identified third-plus. Their share under 20 is 45.4%, against 46.7%. The 1.09M later
  losses are younger: 61.5% are under 20. Adults whose parent is an identified third-plus member report Mexican
  origin more often than children do (loss 4.5–8.5% at 25+, against 12.5–13.2% under 20). Of the +1.35 / +2.86bn,
  +1.22 / +2.52bn comes from the later losses.
- **The brief's premise fails in the data.** It assumed the respondent's report at birth persists. Within the same
  birth cohorts, though, adults report less loss than the cohort's children did: born 1980–84, 24.0% as children
  against 17.7% as co-resident adults; born 1990–94, 21.5% against 15.6%. If the report at birth did persist, the
  1975–94 cohorts' high childhood rates would make the hidden older, and the change would be **−$4.12 / −6.44bn**.
  That run is kept as an alternative, not the central.
- **The other readings stay small.** The 2022–26 window alone gives +0.42 / +1.01bn and 1994–2026 gives
  +2.28 / +4.19bn. Holding adults from 35 at the 25–34 rate gives +0.39 / +1.12bn, and the G4+ share measured by age
  gives +1.05 / +2.47bn. Every cross-section reading is positive on the set. Each is smaller than C3's ±1 SE,
  ±$3.0–3.9bn (lineage lane §5).
- **Recommendation: carry the central into the next main case; it does not justify a case of its own.** It replaces
  an assumption named in v5's Revisit-if list with a measurement, and it changes the headline by 0.3–0.6%. The
  record's wording should change in two ways. The bias does run low, but by $1–3bn, not "by little" from younger
  third-generation attriters. And the cash set's low end does not move (−0.27, SE 0.42).

Per member of the 42.75M lineage: $9,161 / 10,856 on the set (v5 $9,129 / 10,789) and $7,184 / 9,013 in cash (v5
$7,190 / 8,968). An added person costs others $6,752 / 9,729 on the set, against v5's $6,309 / 8,790.

## 1. Identity loss by age (`measure_loss.py`)

**Frame.** The data are the IPUMS-CPS basic monthly files, January 1994 to August 2026, months-in-sample 1 and 5
(g3_identity_pooled_2026_10_05's extract 5, read in place). That lane's `classify()` is ported to DuckDB SQL so
that every age is kept.

- **G3anc.** Native, both own parents US-born, civilian, every linked parent US-born, HISPAN known, and a Mexico-born
  grandparent seen through a co-resident parent's MBPL/FBPL.
- **G4anc.** The same screen with no Mexico-born grandparent, and a linked parent who reports Mexican origin and whose
  own parents are US-born. This is a child of an identified third-plus member.
- **Loss.** HISPAN is not a Mexican code.
- **Weights and SEs.** WTFINL, person-records. SEs are linearised with CPSID households as clusters within the survey
  year. A household's MIS 1 and MIS 5 records fall a year apart, so the SEs are somewhat understated.

[DATA: `derived/loss_cells.csv`; CALCULATION: `derived/loss_tables.csv`]

**Gates.** The SQL's G3anc and identifier flags equal `classify()`'s person for person in 1994, 2010 and 2025: 1,244,
1,855 and 1,771 G3anc, 0 differences. The adult share not Mexican, 0.1539969999, equals the pooled lane's
`monthly_1994_2026_nodedup` value to 1e-9. No parent pointer is missing. Peak RSS was 0.65 GiB.

**Loss by age, 2007–2026 (the central window).**

| Age | G3anc loss (SE) | records | G4anc loss (SE) | records |
|---|---|---|---|---|
| 0–4 | 11.7% (0.4) | 10,059 | 12.8% (0.4) | 13,702 |
| 5–9 | 13.7% (0.5) | 9,153 | 12.7% (0.4) | 13,669 |
| 10–14 | 14.4% (0.5) | 7,446 | 13.2% (0.4) | 12,899 |
| 15–19 | 13.7% (0.6) | 5,360 | 12.5% (0.4) | 10,701 |
| 20–24 | 15.7% (0.9) | 2,214 | 11.5% (0.5) | 4,819 |
| 25–34 | 15.9% (1.2) | 1,368 | 8.5% (0.6) | 3,395 |
| 35–49 | 14.0% (1.3) | 856 | 7.5% (0.7) | 1,839 |
| 50+ | 11.2% (1.5) | 543 | 4.5% (0.8) | 805 |

Adults are seen only while they live with a parent.

**By period.** 2007–21 and 2022–26 agree: G3anc children 13.4% and 12.6%, adults 14.7% and 14.4%. In 1994–2006,
children ran at 20.7% and adults at 17.4%.

**Within cohort (all survey years), child-stage against adult-stage loss.**

| Born | G3anc child | G3anc adult | G4anc child | G4anc adult |
|---|---|---|---|---|
| 1975–79 | 29.1% (3.3) | 20.0% (1.4) | 21.2% (2.1) | 13.3% (0.8) |
| 1980–84 | 24.0% (1.5) | 17.7% (1.4) | 20.5% (0.9) | 12.5% (0.7) |
| 1985–89 | 24.7% (1.1) | 18.4% (1.3) | 20.0% (0.6) | 12.4% (0.7) |
| 1990–94 | 21.5% (0.8) | 15.6% (1.1) | 19.0% (0.5) | 10.4% (0.6) |
| 1995–99 | 17.1% (0.6) | 14.0% (1.1) | 17.1% (0.4) | 11.8% (0.7) |
| 2000–04 | 14.2% (0.5) | 13.2% (1.3) | 13.4% (0.4) | 10.6% (0.9) |

- **The pattern.** Every cohort reports less loss as adults than as children [CALCULATION]. A household respondent
  reports the child's origin; the adult reports their own.
- **The reading.** The gap fits a label that is not fixed at birth, or adults who leave home selectively.
  [INFERENCE] Either way, someone is hidden in the 2025 ASEC by their 2025 report, so the central uses the current
  cross-section.

## 2. The added people's age mix (`age_mix.py`)

Within a five-year band a, the identified third-plus is N(a) = T(a) × (1 − L(a)), so the hidden are
N(a) × L(a) / (1 − L(a)).

- **G3-rate part (1.94M).** L is G3anc's rate.
- **Later part (1.09M).** L is G4anc's rate, applied to the G4+ members of the band. The central gives G4+ the same
  share of the identified at every age, the population lane's convention [ASSUMPTION].
- **Counts.** Each part keeps arm b's count; only the ages move. v5 is this rule with a flat L.
- **Identified mix.** It is white_lines.json's g3plus structure (gate).

| Reading | Part | Under 20 | 20–64 | 65+ |
|---|---|---|---|---|
| v5 (identified) | both | 46.7% | 46.3% | 6.9% |
| **2007–26 cross-section (central)** | G3-rate | 45.4% | 49.0% | 5.6% |
| | later | **61.5%** | 35.5% | 3.0% |
| 2022–26 | G3-rate / later | 43.7% / 53.7% | 49.2% / 42.2% | 7.1% / 4.2% |
| 1994–2026 | G3-rate / later | 48.7% / 64.7% | 45.9% / 32.7% | 5.4% / 2.6% |
| adults 35+ at the 25–34 rate | G3-rate / later | 41.6% / 56.8% | 50.8% / 37.9% | 7.6% / 5.3% |
| G4+ share by age (co-resident) | later | 58.2% | 38.9% | 2.9% |
| cohort at birth (the brief's premise) | G3-rate / later | 30.1% / 33.7% | 58.7% / 55.9% | 11.2% / 10.4% |

[CALCULATION: `derived/age_mix.csv`, `derived/age_mix.json`]

- **Cohort reading.** Today's band takes the child-stage rate of the cohorts born in it. Bands from 50 (born before
  1976, never seen as children) hold the 45–49 rate.
- **Count (informational only).** If p3, a child rate, followed the central's age profile, the G3-rate count would
  be ×1.029. The cohort reading gives ×1.554. Neither is priced.

## 3. Pricing (`g3_age_keys.py`, `band_lines.py`, `price.cjs`, `summarize.py`)

v5 = the union at arm b's responses + later × G + (1 − C3) × g3 × G + C3 × g3 × W. Here G (an identified G3+ member)
and W (a third-plus white) are re-priced at each part's mix. W sits at the G3-rate mix, as v5 puts it at the
identified mix. Counts, C3 (0.5567) and responses are v5's.

**G3+ member: the engine's own keys by age (central route).**

- **Keys by band.** `g3_age_keys.py` rebuilds the account's per-person key vectors with keys.py's own functions,
  imported read-only. It sums the G3+ part of each by five-year band: T[side][allocation][key][band].
- **Gate.** Each of the 90 keys sums to generation_keys.csv's G3plus total (4.4e-16 relative). The justice parts and
  the federal-gap arm follow keys.py's rules.
- **Re-weighting.** Each cell of the corrected G3+ member moves by f = Σ_b (π′_b/π_b) T_b / Σ_b T_b, allocation by
  allocation. The cell's corrections follow its key's profile [ASSUMPTION].
- **Keys keys.py lacks.** housing_support takes the spending vector, and tenant property takes persons in cash-rent
  homes. The engine-only lines take pupils, college enrolment or persons. roads_vmt takes persons aged 5+
  [INFERENCE]. state_price_* takes the parent line's key.
- **The set's pension rule** rewrites three lines (gate: the set's and cash G3+ models differ only there).
  - Social Security takes the OASDI receipts' age profile.
  - Medicare keeps (1 − part_a_share) × the cash cell on its key; the rest goes on the HI receipts.
  - Federal income tax loses the tax on benefits, which takes the benefits key's profile.
- **Production.** It follows the wage key.

**W.** W follows white_lines.py's own path: the white lane's rough re-key, reweighted to the mix. At the identified mix
it equals white_lines.json to 0 relative.

**Positive control.** At the identified mix every factor is exactly 1. The G3+ member and W equal the lineage lane's G1
and W1 cell for cell. The route gives v5's 390.293958 / 461.243125 and 307.376376 / 383.409252. It also gives the
change from v4 (+18.88 / +26.40) and the G3+ and white parts (16.715 / 22.959 and 2.462 / 3.759). The largest
difference is 1.1e-13 bn.

**Results** (ends 48 / 11; every reading keeps them).

| Set | Reading | Band ($bn) | Change | SE | G3-rate part | Later part |
|---|---|---|---|---|---|---|
| set | v5 | 390.29 / 461.24 | — | — | — | — |
| set | **2007–26 (central)** | **391.64 / 464.10** | **+1.35 / +2.86** | 0.26 / 0.37 | +0.12 / +0.33 | +1.22 / +2.52 |
| set | 2022–26 | 390.71 / 462.25 | +0.42 / +1.01 | 0.59 / 0.81 | −0.04 / +0.07 | +0.45 / +0.93 |
| set | 1994–2026 | 392.57 / 465.43 | +2.28 / +4.19 | 0.21 / 0.30 | +0.78 / +1.18 | +1.50 / +3.01 |
| set | adults 35+ at 25–34 | 390.68 / 462.36 | +0.39 / +1.12 | 0.24 / 0.33 | −0.57 / −0.68 | +0.95 / +1.80 |
| set | G4+ share by age | 391.35 / 463.71 | +1.05 / +2.47 | 0.27 / 0.38 | +0.12 / +0.33 | +0.93 / +2.14 |
| set | cohort at birth | 386.17 / 454.81 | −4.12 / −6.44 | 0.26 / 0.37 | −3.15 / −4.29 | −0.97 / −2.15 |
| cash | v5 | 307.38 / 383.41 | — | — | — | — |
| cash | **2007–26 (central)** | **307.11 / 385.32** | **−0.27 / +1.92** | 0.42 / 0.55 | −0.72 / −0.58 | +0.46 / +2.50 |
| cash | 2022–26 | 307.12 / 383.94 | −0.26 / +0.53 | 0.95 / 1.24 | −0.11 / −0.06 | −0.15 / +0.59 |
| cash | 1994–2026 | 308.21 / 387.14 | +0.84 / +3.73 | 0.34 / 0.45 | +0.14 / +0.60 | +0.70 / +3.13 |
| cash | adults 35+ at 25–34 | 307.45 / 384.55 | +0.08 / +1.14 | 0.39 / 0.50 | −0.65 / −0.97 | +0.72 / +2.11 |
| cash | G4+ share by age | 306.74 / 384.68 | −0.63 / +1.27 | 0.44 / 0.58 | −0.72 / −0.58 | +0.09 / +1.85 |
| cash | cohort at birth | 304.54 / 376.78 | −2.83 / −6.63 | 0.55 / 0.68 | −2.55 / −4.44 | −0.28 / −2.19 |

[CALCULATION: `derived/price_bands.csv`, `derived/age_mix_bands.csv`, `derived/summary.json`]

- **SEs.** They come from 2,000 draws of the band loss rates only. The engine-key route is linear in the mix (gate:
  unit bands reproduce every mix to $1e-6 a person). W's reweighting is linear to a near-constant $3–4 a person,
  which cancels to under $1m in the change.
- **Why the low and high ends differ.** At the low end (spec 48, shared allocation) a child carries part of the
  household's taxes. At the high end (spec 11, personal) a child carries none. A younger mix therefore raises the
  high end more.

**Per person** (set, low / high).

| Person | Identified mix | G3-rate mix | Later mix |
|---|---|---|---|
| G3+ member | $8,541 / 11,731 | $8,419 / 11,832 | $9,659 / 14,037 |
| W | $2,274 / 3,472 | $2,485 / 3,700 | — |

**External check.** On this route a G3+ minor costs about $13,043 / 19,926 on the set and $9,911 / 19,910 in cash.
These take bands 0–14 plus 3/5 of 15–19, so they are approximate. The lineage lane's convention (a) − (b) gives
$12,438 / 21,014 and $9,143 / 21,050 for G3 minors with a G2 parent. [CALCULATION; INFERENCE: different populations,
close agreement]

**Cross-check route (rough keys).** `band_lines.py` also applies the white lane's rough re-key factors to whole lines
of the G3+ member. That gives a central of +2.36 / +2.69 (set) and +1.49 / +1.70 (cash), and −6.40 / −6.59 for the
cohort reading. It is not the central because its income-tax and benefit keys are split within the tax or SPM unit.
It therefore gives one age profile to both allocations, while the engine's personal allocation gives children none
of a unit's taxes. The two routes agree in sign and size at the high end.

## 4. Gates

There are 85 gates and all pass (`derived/gates_*.json`; summarize.py's in `summary.json`):

| Script | Gates |
|---|---|
| measure_loss.py | 5 |
| age_mix.py | 17 |
| g3_age_keys.py | 5 |
| band_lines.py | 7, among them the white lane's 57 setup controls |
| price.cjs | 37, among them the lineage lane's copied setup gates |
| summarize.py | 14 |

## 5. What is measured and what is assumed

- **Measured:**
  - loss rates by age and cohort for G3anc and G4anc, from 1994–2026 monthly CPS reports;
  - the identified G3+ age structure;
  - the engine's G3+ key holdings by age, every key and allocation;
  - W by age (the white lane).
- **Assumed:**
  - Co-resident adults' loss rates stand for all adults of their age. Adults living apart from parents cannot be
    linked to grandparents. G3anc's flat 18–49 rates argue against strong selection; G4anc's fall with age could be
    selection.
  - G4+ hold the same share of the identified at every age (central; the measured co-resident share is a
    sensitivity, +1.05 / +2.47).
  - Bands from 50 hold the 50+ rate. A cell's corrections follow its key's age profile. roads_vmt keys by persons aged
    5+.
- **[FRAMING-SENSITIVE]**
  - The central reads loss as a current report (who is hidden now), not a label fixed at birth. The within-cohort
    table supports this; the cohort reading is the alternative.
  - The counts stay arm b's, and identity loss past G3 is unchanged.
- **Not done:**
  - The count's own dependence on the age profile (×1.029 central, informational).
  - Arms a and c, and the fractional and replacement rows.
  - Propagation to consumers (the parent's call).
- **Instrument.** An LLM ran this analysis (`notes/llm-bias-caveat.md`). The numbers rest on the gates and the rerun,
  not on its judgment.

## 6. Reproduce

From the repository root (OPENBLAS_NUM_THREADS=1; peak RSS 1.35 GiB in g3_age_keys.py; about 30 s in total):

```sh
uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/measure_loss.py
uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/age_mix.py
uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/g3_age_keys.py
uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/band_lines.py
node infra/immigration-fiscal/added_age_mix_2026_10_07/price.cjs
uv run --no-project python3 infra/immigration-fiscal/added_age_mix_2026_10_07/summarize.py
```

`scripts/rerun_lane.py` on these six commands: IDENTICAL 22/22, exit 0.

**Inputs, read-only:**

- g3_identity_pooled_2026_10_05 `_cache/monthly_mis15.csv.gz` (sha256 ca414d91…, ignored; IPUMS-CPS extract 5) and
  its `analyze.py`;
- main_case_lineage_2026_10_05 `derived/` and `lineage_case.cjs` (lines 65–380 copied into price.cjs from d3b7e6e6);
- generation_account_2026_09_24 (keys.py, frame.py, `_cache/asec25_generation.parquet`, model and correction payloads);
- the white_replacement_2026_09_28 library;
- main_case_2026_09_29's package.

## Log
- 2026-10-07 10:44 JST — lane created; reading the lineage lane, identity-loss lanes, ladder 158/233.
- 2026-10-07 10:54 JST — measure_loss.py runs (5 gates pass: SQL port of classify() identical person for person in
  1994/2010/2025; adult share 0.1539969999 = the pooled lane's nodedup value). First reading: today's cross-section is
  near flat for G3anc (children 11.7–14.4%, adults 20–49 14–16%, 50+ 11%, 2007–26); G4anc falls with adult age
  (13% → 4.5%). Within each cohort the child-stage rate exceeds the same cohort's adult rate (1980–84: 24.0% vs
  17.7%), so loss is not fixed at birth. The brief's cohort premise is kept as an alternative, not the central.
- 2026-10-07 11:06 JST — pricing built. The rough re-key factors (band_lines.py) apply one shared-allocation age
  profile to both allocations, so the central route is the engine's own keys by age band (g3_age_keys.py, from
  keys.py's vectors; 90 keys gated to generation_keys.csv at 4e-16). The set's three pension lines take the profile of
  what the pension rule puts in them (OASDI and HI receipts, benefits for the tax on benefits). Positive control exact
  (5.7e-14 bn). Central (2007–26 cross-section): set +1.35 / +2.86bn, cash −0.27 / +1.92bn; cohort-at-birth reading
  −4.12 / −6.44bn.
- 2026-10-07 11:10 JST — draws moved from age_mix.json (5.7 MB) into summarize.py; the SQL output ordered (the
  first rerun found loss_tables.csv differing in its last digits); rerun IDENTICAL 22/22, exit 0. RESULT written.
