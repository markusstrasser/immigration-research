claude-opus-5[1m]

**Verdict:** NOT REPRODUCED. The raw count specification gives ~1 US-born non-Hispanic white child into private school per 10 Hispanic children added to public schools, but it **reverses to −0.12/−0.14 once metro enrolment growth is controlled** — it was measuring population growth, not substitution. The share specification is insignificant at every level on the full 334-metro panel; the **foreign-born** share coefficient is *negative*; the predictive part of the Hispanic share is the **US-born second generation**, the opposite of Betts & Fairlie's non-English-speaking mechanism. The public-goods response is real but confined to local revenue: within state-year, **−$447 local revenue and −$369 property-tax revenue per pupil per 10 points of Hispanic share**, **state aid offsets ~60%**, spending and total revenue unchanged. California's 2,954 school tax measures go the *other* way — higher-Hispanic districts vote **more** for bonds.

Memo: `research/immigration-school-flight-and-public-goods-2026-09-18.md` (891 lines)
Literature verification with page-level quotes: `LIT.md`

## Headline numbers

**Design (a), metro panel, 334 metros x 4 waves (2005, 2008, 2010, 2023), primary window 2008–2023**

| specification | elementary | secondary | all 5–17 |
|---|---|---|---|
| Δ private share (white US-born) on Δ Hispanic share | +0.154 (0.095) | +0.078 (0.073) | +0.137 (0.083) |
| same, on Δ foreign-born share | −0.284 (0.195) | −0.145 (0.114) | −0.305 (0.152)** |
| same, on Δ Asian share (horse race) | −0.323 (0.237) | −0.124 (0.183) | −0.424 (0.231)* |
| Hispanic foreign-born vs US-born share | −0.129 (0.245) / **+0.208 (0.094)** | −0.095 (0.151) / +0.093 (0.073) | −0.146 (0.194) / **+0.196 (0.086)** |
| counts, raw ("natives per Hispanic added") | **+0.101 (0.028)** | **+0.103 (0.016)** | **+0.113 (0.021)** |
| counts, + total enrolment growth | **−0.127 (0.041)** | **−0.117 (0.031)** | **−0.135 (0.039)** |
| two-way FE (metro, year) | +0.107 (0.080) | +0.042 (0.058) | +0.114 (0.072) |
| reverse-timing placebo | +0.018 (0.058) | +0.065 (0.056) | — |
| drop 5 largest metros / drop California | — | +0.080 (0.076) / +0.065 (0.080) | — |

2SLS on the 2000-base shift-share instrument: coefficients −0.28 to +0.30, SEs 0.4–2.3, first-stage F from **0.38** (degenerate) to 33. No causal identification; ladder 136's warning is confirmed.

**Design (b), district panel, 38,084 district-years, 13,776 districts, waves 2000/2010/2019**

District FE + state-year FE, per unit Hispanic enrolment share, 2020 dollars per pupil:

| flow | coefficient | per 10 points |
|---|---|---|
| local revenue | −4,472 (687)*** | −$447 |
| local property-tax revenue | −3,693 (664)*** | −$369 |
| state revenue | +2,809 (704)*** | +$281 |
| total revenue | −1,063 (1,093) | −$106 ns |
| current spending | −1,109 (636)* | −$111 |
| instructional spending | −597 (309)* | −$60 |
| local tax effort (local rev/pupil ÷ county median income) | −0.072 (0.020)*** | −6.5% of mean |

Pre-trend placebo on spending −$30 (854), i.e. none. County elderly share is **positive** on spending, +$4,917 (1,768), with an insignificant interaction — Poterba's direction does not appear. Fractionalisation index gives **+$1,155 (475)** on local revenue, the opposite sign to the Hispanic share.

Panel validation against NCES Digest table 203.50 (Hispanic share of public enrolment): 16.3% vs 16.4% (2000), 22.8% vs 23.1% (2010), 27.0% vs 27.7% (2019). Pupil counts 46.5m / 46.9m / 46.9m.

**Design (b) supplement, California ballot measures, 2,954 matched measures, 794 districts, 1998–2024, 83% name-match rate**

Yes vote share on Hispanic enrolment share, year and threshold fixed effects: **+0.043 (0.019)**. Pass indicator +0.088 (0.058) ns. Fractionalisation +0.007 (0.037) ns.

**Design (c), size**

Point estimates across the 334 panel metros, 2008–2023, using F-33 FY2024 prices ($9,589 state revenue per pupil) and NCES 2021-22 tuition:

| level | Δ Hispanic share | natives moved | tuition, $m | state aid shifted, $m |
|---|---|---|---|---|
| all 5–17, panel metros | +5.9 pts | 156,139 | 1,997 | 1,497 |
| all 5–17, California | +3.8 pts | 6,705 | 86 | 64 |
| all 5–17, Texas | +3.6 pts | 6,684 | 85 | 64 |

The underlying coefficient is insignificant, so every interval spans zero (`derived/size_estimates.csv` carries the 95% bounds). For scale, national private enrolment *fell* by about 450,000 over roughly this period.

**Accounting (§4 of the memo)**

Average private tuition $12,790 (2021-22, NCES 205.50) against average public current spending $17,846 per pupil (F-33 FY2024). Short run, with staffing fixed, measured GDP rises by roughly the tuition; long run, when enrolment adjusts, it **falls** by roughly $4,000 per pupil-year, because NIPA values government education output at input cost [SOURCE: BEA NIPA Handbook ch. 9]. Tuition is a real resource cost to the family and a defensive expenditure to the extent outcomes do not improve; lost state aid is a transfer between districts; local property tax does not move; fixed cost per remaining pupil rises.

## Data defects found and fixed

1. **California 2010 inflated 13x.** The Census PUMS endpoint returned records outside the requested `AGEP` range, so the recursive age split counted the same children once per single year of age. Fixed by re-fetching with a single-age split and an explicit age filter; `pull_kids.py` now filters too. `audit_kids.py` checks every state-year against its own cross-year median and now reports 0 of 257 outside ±25%.
2. **Multi-state metros split and dropped.** `build_metro.py` grouped on state as well as CBSA, fragmenting New York, Chicago, Washington, Philadelphia, Kansas City, Charlotte, Memphis and Portland, which then failed the balanced-panel filter. Each CBSA is now assigned the state of its largest allocated child population. The correction moved the elementary share coefficient from +0.218 (0.084) to +0.154 (0.095) and the sample from 291 to 334 metros — §5.7.
3. **ACS `SCH` = 3 changed meaning in 2008**, from "private school or college" to "private school or college **or home school**" (checked against the Census API variable dictionary). The primary window therefore starts in 2008; the 2005-based window is still reported, flagged `[SCH def change]`.
4. **Per-pupil denominators.** Urban's CCD enrolment year is the autumn *after* the F-33 finance year, so per-pupil figures use the F-33's own membership count and CCD counts are used only for race shares.

## Files

| File | What it does |
|---|---|
| `BRIEF.md` | the dispatch, saved verbatim |
| `pull_kids.py` | ACS 1-year PUMS cells, children 5–17, school type x race/ethnicity x nativity, by PUMA |
| `fetch_one_state_year.py` | single-age-split fetch for one state-year, with the age filter |
| `audit_kids.py` | cross-year consistency audit of every state-year cell file |
| `build_metro.py` | PUMA → county → fixed 2013 CBSA; metro x year school-type panel |
| `estimate_flight.py` | design (a): long differences, two-way FE, horse races, generation split, 2SLS, placebo, influence, counts with and without growth control |
| `pull_districts.py` | Urban Institute Education Data Portal: CCD finance, enrolment-by-race, directory |
| `pull_county_controls.py` | county elderly share and median household income (Poterba control) |
| `build_districts.py` | district-year panel, 2020 dollars, screens, wave-coverage filter |
| `estimate_districts.py` | design (b): district FE + state-year FE by alternating projections, Poterba interaction, long difference, pre-trend placebo |
| `ceda_bonds.py` | California school bond and parcel-tax measures vs district Hispanic share |
| `size.py` | design (c): scales the coefficient to head counts, tuition and state aid |
| `tables.py` | renders every estimate file into the memo's §3 |
| `assemble.sh` | rebuilds the memo from `_parts/` |

## Verification commands

```bash
cd /Users/alien/Projects/immigration-research/infra/immigration-fiscal/school_flight_2026_09_18
UV='uv run --no-project --with pandas>=2 --with numpy>=2 --with openpyxl --with xlrd'
set -a; . ../acquire/config.local.env; set +a   # CENSUS_API_KEY, never printed
PUMS_YEARS=2005,2008,2010,2023 $UV python3 pull_kids.py    # resumable, skips cached state-years
$UV python3 audit_kids.py                                   # must print 0 outside [0.80, 1.25]
$UV python3 build_metro.py
$UV python3 estimate_flight.py
DIST_YEARS=2000,2010,2019 $UV python3 pull_districts.py     # resumable
$UV python3 pull_county_controls.py
$UV python3 build_districts.py
OPENBLAS_NUM_THREADS=1 $UV python3 estimate_districts.py
$UV python3 ceda_bonds.py
$UV python3 size.py
$UV python3 tables.py && ./assemble.sh
```

## Covered / skipped

**Covered.** Design (a) in full, including every disconfirmation check the brief preregistered (Asian-share horse race, pre-trend placebo, influence of large metros and California) plus three not asked for (the generation split, the enrolment-growth control that reverses the count result, and the group-specific outcomes). Design (b) in full, with the revenue-source decomposition that identifies the equalisation channel, a Poterba interaction and a pre-trend placebo. The California bond analysis, which the brief marked conditional, was reachable and is included. Design (c) with 95% bounds. The §4 accounting with BEA's own wording and the repo's F-33 prices.

**Skipped or incomplete.**
- **Waves.** PUMS 2013, 2015 and 2018 were dropped for throughput (2013 reached 43 states, 2015 reached 10). District waves 2005 and 2015 were dropped the same way (2005 reached 76 of 153 files); 2020 was dropped deliberately because Urban's CCD enrolment year 2020 is the pandemic autumn. Urban's F-33 redistribution stops at 2020, so the district panel cannot be carried to the FY2024 file the repo holds locally.
- **Literature [GAP].** Alesina, Baqir & Easterly 1999 and Hopkins 2009 were **not** retrieved — the literature agent hit its turn limit twice and then a rate limit. The unverified claims are named explicitly in memo §1.3 and §1.4, and nothing in the memo rests on them. The Louisiana Scholarship Program and Altonji, Elder & Taber 2005 are unverified for the same reason, so §5.4's switcher-outcome conclusion rests on the DC Opportunity Scholarship Program alone.
- **Not attempted.** Charter enrolment, the largest competing exit route, is inside the public share throughout and is not separated (memo §5.1). Homeschooling is inside the private share from 2008 on and is not separated.

Not committed, per the brief.

*Parent note, 2026-09-18:* `derived/district_panel.csv` (18 MB) is regenerated by `build_districts.py` from the cached Urban Institute pulls and is gitignored; every other derived file is committed. All four estimation scripts re-run by the parent reproduce their outputs byte-identically.
