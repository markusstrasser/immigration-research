claude-opus-5-5

**Verdict:** About 399,000 Mexico-born residents arrived at 50 or older (central reading; 327,000–505,000
across the entry-year grouping). They are 13.7% of Mexico-born seniors; the ACS lane finds 13.6%.

In the adopted September 27 case ($321.8–387.4bn), they cost other US residents **$5.7–5.8bn a year
($14.2–14.5k a head)**. The grouping bounds give $4.9–7.4bn. That is 6–7% of the Mexico-born line and
1.5–1.8% of the case.

The 227,000 of them now 65+ cost $4.4–4.9bn ($19.6–21.6k a head). That is **less** per head than
Mexico-born seniors who arrived younger ($21.7–24.3k), because the account also charges them less Social
Security ($3.8–5.3k against $6.9–9.9k), which more than offsets their lower taxes (−$5.0–6.3k against
−$7.5k). At 50–64 they cost $1.1–1.5k a head more than younger arrivals ($5.2–7.1k against $4.0–5.6k).

The account keys Medicare and community Medicaid to insurance status, not coverage, so it charges late
arrivals Medicare that a quarter of them lack. Re-keyed by ACS coverage inside the Mexico-born 65+, their
Medicaid rises $0.03–0.04bn and their Medicare falls $0.34bn: a proposed net **−$0.31bn**. The Medicare part
is a floor, because both surveys edit Medicaid seniors into Medicare.

On the schools case, late arrivals plus the rest of the Mexico-born reproduce the generation lane's G1 to
2e-10bn. The generation lane has not yet run the September 27 case.

This is an annual line. Never add it to the per-admission lifetime value (ladder 235). [CALCULATION:
`run_cells.cjs`, `build_line.py`, `medicaid_check.py`, `verify.py` → `derived/`] [FRAMING-SENSITIVE]

# Late-arrival (arrived at 50+) Mexico-born line in the main case

Lane started 2026-09-27. Sections appended as computed.

## 1. Subgroup size (CPS ASEC 2025, the account's frame)

Script `counts.py` → `derived/counts.csv`. The frame, the union and the generation masks are
`generation_account_2026_09_24/frame.py` at 0f22f0c, copied here; only the G1 mask changes: G1 is cut into
seven cells by approximate age at arrival (arrived before 50, at 50–54, at 55+) and current age.

**Age at arrival.** `PEINUSYR` is grouped year of entry: single decades or five-year spans before 1980,
two-year spans 1980–2021, and one span 2022–2025 [DATA: ASEC 2025 dictionary,
`indian_civic_cps_2026_09_18/_cache/asec_2025_PEINUSYR.json`]. Age at arrival = current age − years since
arrival, read three ways: *central*, arrival at the span's midpoint (the last span ends at the survey,
2025.2) and birth half a year before the age's anniversary; *lower*, earliest arrival and latest birth
(counted 50+ only if certain); *upper*, latest arrival and earliest birth (possibly 50+). Top-coded ages
(80 = 80–84, 85 = 85+) take 82/88 central and their interval ends in the bounds. [CALCULATION:
`frame.py` `arrival_age`]

| Reading | Arrived at 50+ | of them 65+ | Share of Mexico-born 65+ | Arrived at 55+ | of them 65+ | Records (50+) |
|---|---|---|---|---|---|---|
| central | 399,300 (SE 36,800) | 226,600 | 13.7% (SE 1.4 pp) | 227,300 | 165,400 | 209 |
| lower (certain) | 326,500 | 204,700 | 12.4% | 185,400 | 139,500 | 170 |
| upper (possible) | 505,100 | 278,200 | 16.9% | 272,900 | 187,200 | 256 |

Mexico-born in the account: 12,220,800 (5,631 records); 65+: 1,648,300; 50+: 5,384,600. Younger arrivals
at the same ages: 4,985,300 aged 50+ and 1,421,700 aged 65+ (central). SEs from the 160 replicate weights
(4/160 × Σ(θr − θ)²).

**Against the ACS lane.** The sister lane's ACS 2019–2023 pool gives 13.6% (SE 0.2 pp) of Mexico-born 65+
arrived at 50+, 179,700 persons [DATA: `late_arrival_tail_2026_09_27/derived/late_arrival_65plus.csv`].
The CPS central reading gives 13.7%, inside one SE; the grouping moves it between 12.4% and 16.9%. The CPS
level (226,600) is higher than the ACS's (179,700) because the CPS Mexico-born 65+ total is larger here
(1.65m against 1.32m) and the frame is 2025 against a 2019–2023 pool. The CPS cell is 122 records: every
dollar figure below carries that sampling error on top of the account's.

## 2. Method: the generation split with the G1 mask cut

The generation lane's split is copied (`generation_account_2026_09_24` at 0f22f0c, clean in git) and run
with the mask changed. Nine cells replace three generations: seven G1 cells (arrived <50 / 50–54 / 55+ ×
current age), G2 and G3plus unchanged.

- **Unchanged and exact.** Keys, models, production attribution, the tax-records stack (all ten hot-deck
  runs), the external re-keys and the consumption key split per person. The cells add to the generation
  lane's G1 person for person.
- **Two-level splits.** The generation lane has two non-additive splits: ratio-type changes at each
  generation's own stack factor, and the consumption key's own-factor part. Both run first over
  G1/G2/G3plus exactly as there, then inside G1 by the same rule on G1's amount. `run_cells.cjs`
  `twoLevel`.
- **Rules that gave an amount "to G1".** They need a split inside G1 [INFERENCE, FLAGGED]:
  - Mexico-born LTSS users: by each Mexico-born CPS person's ACS proxy rate at their arrival class and
    five-year age band (`acs_rates.py`, ACS 2019–2023 from the sister lane's cache). Institutional
    residents stand in for nursing facilities, community Medicaid enrollees for ICF/IID and HCBS, and all
    residents for mental-health facilities. The disability items are not in the cached pull.
  - Shelter's use-based charge: by Mexico-born entrants of 2022–2025 (`PEINUSYR` 28).
  - Care workers' hours: by the Mexico-born CPS workers in those occupations.
  - Justice custody and ICE interior: by counts aged 18–64, the rule the lane already uses for the
    US-born.
  - The benefits sensitivity "all to G1": by the key's own shares.
- **Case `sept27`.** The package exports the schools package's shift lists unchanged. Each cell's corrected
  model gets `rekeyEdits` (package rule, "For consumers" 2). Cost is `evaluateFull`, with the capital
  return keyed by the cell's own evaluation. Programme parts come from that one evaluation.

Gates, all passing (`_cache/run_cells_*.log`, `_cache/run_split_*.log`):
- lanes rebuild `packageShifts`; every split adds to its union shift (2e-12bn);
- netted cell edits add to `corrections.json` in all 270 (schools) or 278 (sept27) cells;
- the corrected union reproduces the case: sept27 $321.8194–387.3701bn, schools $258.4885–291.9548bn;
- the uncorrected union reproduces its band ($332.7493–398.3079bn / $265.5903–298.6797bn);
- the nine cells add to the union in all 64 specifications (1.9e-12bn);
- programme parts add to the package's `cost()` (1.1e-13bn).

`verify.py` rebuilds the Mexico-born total as late arrivals plus their complement. On the schools case it
matches the generation lane's G1 at both ends, both conventions and all three readings: max |diff|
1.9e-10bn. The generation lane has not yet run `--case sept27` (`sept27_propagation_2026_09_27/RESULT_generation.md`
is pending). For sept27, the G1 identity therefore holds by construction, and the cells are checked against
the case's published band. **[PENDING]** Re-run `verify.py` once the generation lane's summary carries
`case: sept27`.

## 3. The late-arrival line in the main case

Net cost to other US residents, $bn a year (2024), at the union's two band ends. The low end is shared
allocation with GDP normalization; the high end is personal allocation with cash normalization. Convention
(a): each person in their own cell. A positive figure is a cost. [CALCULATION: `run_cells.cjs` →
`build_line.py` → `derived/late_arrival_line.csv`]

**September 27 case (adopted, $321.8–387.4bn):**

| Subgroup (central reading) | Persons | $bn low / high | $ per person low / high | Lower-edge reading $bn | Upper-edge reading $bn |
|---|---|---|---|---|---|
| Arrived at 50+, all ages | 399,300 | 5.66 / 5.80 | 14,184 / 14,523 | 4.91 / 5.27 | 7.27 / 7.41 |
| of them 65+ | 226,600 | 4.44 / 4.90 | 19,599 / 21,632 | 4.09 / 4.50 | 5.61 / 6.21 |
| of them 50–64 | 172,700 | 1.22 / 0.90 | 7,076 / 5,192 | 0.82 / 0.77 | 1.66 / 1.20 |
| Arrived at 55+ | 227,300 | 4.01 / 4.19 | 17,645 / 18,440 | 3.38 / 3.54 | 4.49 / 4.68 |
| of them 65+ | 165,400 | 3.51 / 3.70 | 21,222 / 22,362 | 3.03 / 3.19 | 3.95 / 4.19 |
| Arrived younger, now 50+ | 4,985,300 | 50.79 / 49.01 | 10,188 / 9,830 | | |
| Arrived younger, now 65+ | 1,421,700 | 30.80 / 34.59 | 21,662 / 24,327 | | |
| Arrived younger, now 50–64 | 3,563,600 | 19.99 / 14.42 | 5,610 / 4,046 | | |
| All Mexico-born | 12,220,800 | 93.77 / 78.31 | 7,673 / 6,408 | | |

- **Share of the case.** Late arrivals are 3.3% of the Mexico-born and cost $5.7–5.8bn: 6.0–7.4% of the
  Mexico-born line and 1.5–1.8% of the case.
- **Grouping bounds.** The bounds move persons, not per-person costs: $14.4–16.1k a head at either edge.
- **Convention (b)** (minors with their parents): 458,200 members and $6.4–7.0bn. The 65+ part is
  $4.7–5.3bn ($19.5–22.0k).

**Schools case (September 26 main case, $258.5–292.0bn), checked against the generation lane:**
- arrived at 50+: $5.12 / 5.07bn ($12,825 / 12,687);
- of them 65+: $4.11 / 4.46bn ($18,154 / 19,702);
- younger arrivals now 65+: $28.87 / 31.84bn ($20,303 / 22,395).

The September 27 case adds $0.5–0.7bn to the late line: capital return, long-run roads and parks, and
rental assistance.

**By programme, $ per person a year, sept27, (a), central, low / high:**

| Programme | Arrived 50+, now 65+ | Arrived younger, now 65+ | Arrived 50+, now 50–64 | Arrived younger, now 50–64 |
|---|---|---|---|---|
| Taxes, income | −1,156 / −374 | −1,685 / −1,731 | −2,492 / −1,973 | −2,488 / −2,570 |
| Taxes, payroll | −3,196 / −2,635 | −3,505 / −3,478 | −3,029 / −3,183 | −3,660 / −4,139 |
| Taxes, consumption | −1,783 / −1,783 | −2,096 / −2,096 | −1,783 / −1,783 | −1,865 / −1,865 |
| Taxes, property and other | −195 / −201 | −242 / −249 | −195 / −207 | −211 / −222 |
| **Taxes, total** | **−6,330 / −4,993** | **−7,528 / −7,554** | **−7,499 / −7,146** | **−8,225 / −8,796** |
| Medicaid (incl. LTSS) | 3,660 / 3,735 | 3,336 / 3,372 | 2,626 / 2,683 | 2,673 / 2,710 |
| Medicare | 11,028 / 11,028 | 11,411 / 11,411 | 2,067 / 2,067 | 2,122 / 2,122 |
| Social Security | 3,764 / 5,286 | 6,887 / 9,908 | 1,422 / 461 | 915 / 806 |
| SSI | 126 / 54 | 161 / 83 | 244 / 0 | 69 / 101 |
| SNAP | 535 / 535 | 332 / 332 | 179 / 179 | 165 / 165 |
| Refundable credits | 262 / 24 | 164 / 73 | 1,090 / 1,285 | 758 / 880 |
| Other transfers | 845 / 792 | 1,458 / 1,376 | 519 / 367 | 665 / 606 |
| Education (share of services) | 2,549 / 1,067 | 2,147 / 1,140 | 2,724 / 1,007 | 2,969 / 1,097 |
| Other services | 2,396 / 3,031 | 2,865 / 3,325 | 3,353 / 3,564 | 3,656 / 3,949 |
| Subsidies incl. rental assistance | 275 / 275 | 130 / 130 | 55 / 55 | 58 / 58 |
| Return on public capital | 617 / 881 | 620 / 942 | 649 / 904 | 679 / 938 |
| Production term | −128 / −85 | −320 / −211 | −354 / −233 | −894 / −590 |
| **Net cost** | **19,599 / 21,632** | **21,662 / 24,327** | **7,076 / 5,192** | **5,610 / 4,046** |

In $bn for the late arrivals now 65+ (low / high):
- taxes −1.44 / −1.13;
- Medicaid 0.83 / 0.85;
- Medicare 2.50;
- Social Security 0.85 / 1.20;
- SSI 0.03 / 0.01;
- services 1.12 / 0.93;
- capital 0.14 / 0.20.
Every row for every subgroup is in `derived/late_arrival_line.csv`.

**Reading.** At 65+ the late arrivals cost others about $2.1–2.7k a head *less* than Mexico-born seniors
who arrived younger:
- Their taxes are lower by $1.2–2.6k.
- Their Social Security, which the account keys on reported receipt, is lower by $3.1–4.6k. They have
  not paid in, and it shows on both sides of the ledger.
- Medicare is charged almost equally ($11.0k against $11.4k), although a quarter of them report none
  (section 4).

At 50–64 they cost $1.1–1.5k a head more than younger arrivals, mostly through lower payroll and income
taxes. Per head over all ages, the late group costs more than younger arrivals now 50+ ($14.2–14.5k
against $9.8–10.2k). That is age mix: 57% of late arrivals are 65+, against 29% of younger arrivals aged
50+.

**Caveats.**
- SSI and Social Security are CPS-reported. The ACS lane finds more SSI among late arrivals (10.2%
  against 8.7%); the CPS cell shows less.
- Education under the shared allocation ($2.5k a head at 65+) is the SPM unit's equal split: late arrivals
  live with school-age grandchildren. Under the personal allocation it falls to $1.1k [INFERENCE: the
  education line's part not keyed to the person's own pupils; not traced further here].
- The CPS cell is 122 records at 65+ and 209 at 50+. The count's replicate SE is 9–12%. The dollar
  figures carry at least that sampling error, which the engine does not propagate (the account runs on
  the full-sample weight).

## 4. Medicaid pricing check (proposed correction, not applied)

Script `medicaid_check.py` → `derived/medicaid_check.csv`. Case sept27; the schools case gives the same
figures, because neither the Medicaid nor the Medicare line changes between the two cases.

**How the account prices them.** Each insured person, with any public or private coverage, takes:
- the MEPS mean Medicaid and Medicare payment of their age band × US-birth cell;
- times the pooled Mexican-origin ratio of that cell (0.88 at 65+; ladder 206).

Medicaid's long-term-care users are then charged by the LTSS lane's users' shares. Inside the Mexico-born,
those shares follow ACS proxy rates by arrival class (section 2). The key does not read a person's own
Medicaid or Medicare coverage. The brief's "per covered person from a pooled figure" is therefore "per
insured person from a pooled cell mean".

**Coverage** (Mexico-born 65+):

| Measure | Arrived 50+ | Arrived younger |
|---|---|---|
| Medicaid, ACS 2019–2023 | 40.1% | 32.0% |
| Medicaid, CPS 2025 | 13.3% | 14.9% |
| Medicare, ACS | 74.9% | 89.7% |
| Medicare, CPS | 68.8% | 86.8% |
| Neither, CPS | 31.2% | 13.2% |
| Institutionalized, ACS | 1.09% | 1.01% |

- **ACS against CPS.** The CPS Medicaid rate is a third of the ACS's and has the wrong sign on a
  122-record cell. The check uses the ACS rates, applied to each CPS person by arrival class and
  five-year age band. That gives expected coverage of Medicaid 37.5% against 31.5% and Medicare 72.8%
  against 89.2%.
- **Coverage edit.** Both surveys edit every 65+ Medicaid reporter to Medicare coverage: zero
  Medicaid-only records at 65+ in either file. A Medicaid enrollee without Medicare, for whom Medicaid is
  the only public payer, is therefore invisible. The edit also overstates the late arrivals' Medicare,
  so the Medicare figure below is a floor.

**What the account charges the late arrivals now 65+** ($bn, low / high):
- **Medicaid: 0.83 / 0.85** ($3,660 / 3,735 a head).
  - The LTSS users' charge is 0.57 ($2,534 a head, against $2,224 for younger arrivals).
  - The rest is 0.26 / 0.27, or $3,002 / 3,202 per expected covered person (younger: $3,527 / 3,642).
- **Medicare: 2.50**, which is $15,154 per expected covered person. The younger arrivals' figure is
  $12,797: the key charges the uncovered.

**Proposed correction A: re-key by coverage.** Community Medicaid and Medicare are each keyed by expected
coverage inside the Mexico-born 65+. The group's totals are held, so the change is zero-sum against
younger arrivals. For the late arrivals now 65+:
- Medicaid: +$0.03–0.04bn;
- Medicare: −$0.34bn;
- net: **−$0.31bn a year (−$1,350 to −1,380 a head)**.

The account over-charges late arrivals through Medicare more than it under-charges them through Medicaid.
The Medicare part is a floor, given the survey edit.

**Level beside it (B, not late-specific).** MCBS 2023 gives $6,648 of Medicaid payments per Hispanic 65+
community beneficiary with any Medicaid payment ($2,379 mean ÷ 35.8% with Medicaid). The account's
community Medicaid is 0.45–0.48 of that per expected covered late arrival, and 0.53–0.55 for younger
arrivals. [DATA: `mcbs_elderly_medical_2026_09_22/derived/ratios.csv`; ladder 173]

At MCBS's level, the late arrivals' community Medicaid would be $0.56bn in 2023 dollars, +$0.29–0.31bn.
Younger arrivals would rise by +$1.35–1.40bn. The comparison mixes sources: MCBS is claims-linked and
community-only, while the account's lines are NIPA totals keyed by MEPS. This is ladder 206's open
MCBS-against-MEPS item for all Mexican-origin seniors, not a late-arrival error, so it is not proposed
here.

**LTSS band.** Across the LTSS lane's variants (`ltss_share_2026_09_23/derived/shares.csv`), the late
arrivals' users' charge runs from $0.55bn (NF priced by ACS Medicaid users) to $0.60bn (union CPS-scaled).
The central charge is $0.57bn. The "no IHSS" diagnostic gives $0.40bn.

The within-Mexico-born split rests on ACS proxies without the disability items. Late arrivals' higher
community Medicaid rate (39% against 31%) raises their HCBS share. Their institutional rate is close to
younger arrivals' (1.09% against 1.01%). [INFERENCE, FLAGGED]

## 5. Frame

This is an annual account: 2024's taxes against 2024's benefits and services. "Did not pay in" shows up
in two ways:
- lower taxes this year (−$5.0–6.3k a head at 65+, against −$7.5k for younger arrivals);
- smaller contributory benefits: Social Security $3.8–5.3k against $6.9–9.9k, and Medicare in
  principle, though the account's key misses that (section 4).

Means-tested programmes (Medicaid, SNAP, SSI, rental assistance) are drawn as reported or keyed.

The per-admission lifetime value of a sponsored parent is ladder 235 (the sister lane: $437–525k
undiscounted, $270–286k at 3%). It is a separate object: it counts one admission's remaining life. This
line is one year's cost of everyone who arrived at 50+ and is here now. **Never add the two.**
[FRAMING-SENSITIVE]

## Files

**Covered**, from `generation_account_2026_09_24` at 0f22f0c:
- `frame.py` (mask cut; arrival age), `keys.py`, `build_models.py`, `production.py`, `stack_split.py`,
  `external_split.py`, `correction_rules.py` and `consumption_split.py`: generalized to the nine cells,
  with the G1 rules above.
- `run_generations.cjs` lines 62–445, as `run_cells.cjs`.

**New:**
- `counts.py`, `acs_rates.py`, `build_line.py`, `medicaid_check.py`, `verify.py`, `run_split.sh`;
- `derived/counts.csv`, `derived/late_arrival_line.csv`, `derived/medicaid_check.csv`.
- Intermediates (models, splits, cell JSONs, logs) live in the ignored `_cache/split_<reading>/` and
  `_cache/cells_<case>_<reading>.json`. Rebuild with
  `LATE_DEF=<r> bash run_split.sh`, then `node run_cells.cjs --case <c> --def <r>`, `build_line.py`,
  `medicaid_check.py` and `verify.py`.

**Skipped**, with reasons:
- `compare_ledger.py`, `parents_check.py`, `mixed_units.py`, `test_masks.py`: generation-lane diagnostics,
  not needed for a G1 cut.
- `run_generations.cjs` lines 446–856: lane contributions, sensitivities, the ledger bridge and the chain
  from September 24. None is asked for, and the sensitivities would multiply run time with no bearing on
  the late line.
- Replicate-weight SEs on dollars: the engine runs on the full-sample weight only.
