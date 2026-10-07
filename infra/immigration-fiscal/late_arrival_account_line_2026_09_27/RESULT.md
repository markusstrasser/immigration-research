claude-opus-5-5

**Verdict:** About 399,000 Mexico-born residents arrived at 50 or older (central reading; 327,000–505,000
across the entry-year grouping). They are 13.7% of Mexico-born seniors; the ACS lane finds 13.6%.

In the main case adopted on 2026-09-29 ($371.4–434.8bn, with the pension accrual), they cost other US residents
**$4.4bn at the union's low end and $4.1bn at its high end** ($12.1k / 11.4k a head on the case's row-4 headcount,
362,200). The grouping bounds give $3.7–5.6bn. That is 4.5–4.7% of the Mexico-born line and 1.0–1.2% of the case.
The pension switch lowers their cost by $1.1 / 1.5bn. It replaces the Social Security and Part A benefits their 65+
draw this year with the accrual on the payroll taxes they pay this year. In the cash set (the switch off,
$294.7–361.8bn) they cost $5.5 / 5.6bn ($15.1k / 15.5k). Late arrivals plus the rest of the Mexico-born reproduce the
generation lane's G1 to 9e-11bn in both sets. Under the set the proposed Medicare re-key shrinks to −$0.21bn and the
net correction to −$0.18bn, since only Parts B and D are still priced by the key (section 6).
[CALCULATION: `run_cells.cjs --case sept29|sept29_cash` → `derived/late_arrival_line_sept29.csv`] The September 27
figures follow.

[2026-10-05: on main case v5 (`oct05`, $390.3–461.2bn), the late arrivals cost $4.38 / 4.13bn ($12,085 / 11,394 a
head), against $4.38 / 4.13bn on September 29 ($4.3806 / 4.1305): v5 moves them by −$0.003bn. The 3.04M people v5
adds are third-plus, with no arrival year, so the Mexico-born move only by the larger group's responses and their
share of audit row 8 (−$0.09bn in all). They are 4.5% / 4.7% of the Mexico-born line and 1.1% / 0.9% of the case. The
cash set: $5.47 / 5.60bn. The Medicaid check is unchanged. [CALCULATION: `run_cells.cjs --case oct05|oct05_cash` →
`derived/late_arrival_line_oct05.csv`; section 7]]

[2026-10-07: on main case v6 (`oct07`, $389.08–461.48bn, adopted 2026-10-07), the late arrivals cost $4.36 / 4.12bn
($12,047 / 11,360 a head), −$0.014 / 0.012bn from v5. The 2026 Trustees paths lower G1's accrual per tax dollar
(−$0.010 / 0.008bn), and the user-fee item and retiree health net out most of the rest. They are 4.5% / 4.7% of the
Mexico-born line and 1.12% / 0.89% of the case. The cash set: $5.46 / 5.60bn. Pell goes by education's shares
[ASSUMPTION: no college-enrollment key exists by person here]; by its own line's adult-cash key they would cost
$0.05 / 0.07bn more. The Medicaid check is unchanged but for the Part A accrual. [CALCULATION: `run_cells.cjs
--case oct07|oct07_cash` → `derived/late_arrival_line_oct07.csv`; section 8]]

In the adopted September 27 case ($321.8–387.4bn), they cost other US residents **$5.7–5.8bn a year
($14.2–14.5k a head)**. The grouping bounds give $4.9–7.4bn. That is 6–7% of the Mexico-born line and
1.5–1.8% of the case. The September 27 per-head figures in this verdict divide by the CPS count (399,300; 226,600 at
65+). On the account's row-4 count (362,200) they are $15.6–16.0k, and $21.4–23.7k at 65+ against
$22.9–25.7k for younger arrivals (section 6).

The 227,000 of them now 65+ cost $4.4–4.9bn ($19.6–21.6k a head). That is **less** per head than
Mexico-born seniors who arrived younger ($21.7–24.3k), because the account also charges them less Social
Security ($3.8–5.3k against $6.9–9.9k), which more than offsets their lower taxes (−$5.0–6.3k against
−$7.5k). At 50–64 they cost $1.1–1.5k a head more than younger arrivals ($5.2–7.1k against $4.0–5.6k).

The account keys Medicare and community Medicaid to insurance status, not coverage, so it charges late
arrivals Medicare that a quarter of them lack. Re-keyed by ACS coverage inside the Mexico-born 65+, their
Medicaid rises $0.03–0.04bn and their Medicare falls $0.34bn: a proposed net **−$0.31bn**. The Medicare part
is a floor, because both surveys edit Medicaid seniors into Medicare.

On the September 27 case and the schools case, late arrivals plus the rest of the Mexico-born reproduce the
generation lane's G1 to 2e-10bn (`verify.py`; the schools check dates from 2026-09-27, when the generation lane held
that case).

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
`case: sept27`. [Done 2026-09-29: the summary has carried `case: sept27` since 8654a0ce. `verify.py` matches the
generation lane's G1 at both ends, both conventions and all three readings, max |diff| 1.9e-10bn. The schools case is
now the one it reports [PENDING], since the generation lane holds one case.]

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

## 6. v4 case (sept29), 2026-09-29

The operator adopted candidate v4 as the main case on 2026-09-29 at 15:12 JST (`main_case_2026_09_29`, case key
`sept29`). It costs $371.4146–434.8410bn with the pension accrual; the cash set beside it (the switch off) costs
$294.7011–361.8175bn. `run_cells.cjs` runs both as `--case sept29` and `--case sept29_cash`. Model self-report:
claude-opus-5-5.

The v4 part reads the adopted lane, landed at 40c4ba7: `generation_account_2026_09_24/v4_split.cjs` `V4_LANE` and
`verify.py` `V4_LANE` name `main_case_2026_09_29`. The first sept29 run (17:03–17:21) read candidate v4's payloads, which
differ from the adopted ones only in five meta stamps. The repointed run (20:16) gives the figures below. The machine
rebooted at about 20:51 JST during this lane's `rerun_lane.py` gates; the run resumed at 21:13, and every step and gate
ran again (gates below).

**Method.** The September 27 steps run unchanged and give each cell's September 27 payload. The v4 part then goes on
each cell's September 27 model by the generation lane's rules. They live in `v4_split.cjs`, shared with that lane,
and its RESULT section "v4 case (sept29)" gives each rule with the alternative beside it. Two things are this lane's
own:
- **Item 3** (the IRS-matched income-tax key) goes through `scaledSplit` in two levels, as this lane splits every
  ratio-type change. Each cell's own change in the raked cells times its own stack factor, first over G1 (the cells
  summed), G2 and G3+, then inside G1. The non-additive remainder is at most $0.24bn.
- **Inputs by cell.** `run_split.sh` step 7 runs the generation lane's `v4_inputs.py` and `tax_key_split.py` on this
  lane's frame (`V4_LANE_DIR`) for each reading. They give the row-4 production grid, tenant shares, row-4 headcounts
  and the tax-key change by cell.

Inside G1 each cell takes G1's pension ratios on its own OASDI and HI receipts, and G1's benefit tax by its own
Social Security key. Every rule is linear in a cell's inputs, so the seven G1 cells add to the generation lane's G1.
The property tax on rented homes (`tenant_occupied_property`, new in v4) joins "taxes, property". Public housing's
deficit line (`housing_enterprise_surplus`) joins the other enterprise receipts under "other receipts". The five new
spending lines are services. Per-person figures use the row-4 headcounts (`v4_inputs.json`), the case's basis. The
row-4 weights scale naturalized Mexico-born by 0.856 and noncitizens by 0.778, so the late arrivals count 362,200
here, against 399,300 in the September 27 tables.

Section 3's September 27 tables divide by the CPS weights. On the row-4 count, the September 27 case costs $15,634 /
16,008 a head for late arrivals, $21,441 / 23,665 for those now 65+ and $22,901 / 25,719 for younger arrivals now 65+.
At 65+ late arrivals therefore still cost less a head on September 27. The Mexico-born cost $8,496 / 7,096 a head.
[CALCULATION: `late_arrival_line_sept29.csv`, rows `sept27_total`]

**The set, central reading, (a)** ($bn a year at the union's ends; [CALCULATION: `derived/late_arrival_line_sept29.csv`]):

| Subgroup | Persons (row 4) | $bn low / high | $ per person low / high | Lower-edge reading $bn | Upper-edge reading $bn | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| Arrived at 50+, all ages | 362,200 | 4.38 / 4.13 | 12,093 / 11,403 | 3.69 / 3.68 | 5.59 / 5.23 | −1.28 / −1.67 |
| of them 65+ | 207,100 | 3.09 / 2.98 | 14,933 / 14,390 | 2.86 / 2.74 | 3.85 / 3.69 | −1.35 / −1.92 |
| of them 50–64 | 155,100 | 1.29 / 1.15 | 8,299 / 7,412 | 0.83 / 0.94 | 1.74 / 1.54 | +0.07 / +0.25 |
| Arrived at 55+ | 210,700 | 2.98 / 2.88 | 14,136 / 13,686 | 2.45 / 2.37 | 3.42 / 3.27 | −1.03 / −1.31 |
| of them 65+ | 153,300 | 2.50 / 2.34 | 16,272 / 15,258 | 2.15 / 1.99 | 2.81 / 2.62 | −1.01 / −1.36 |
| Arrived younger, now 50+ | 4,631,100 | 42.01 / 38.15 | 9,071 / 8,237 | | | −8.78 / −10.86 |
| Arrived younger, now 65+ | 1,344,800 | 17.00 / 15.75 | 12,640 / 11,712 | | | −13.80 / −18.84 |
| Arrived younger, now 50–64 | 3,286,300 | 25.01 / 22.40 | 7,611 / 6,815 | | | +5.02 / +7.98 |
| All Mexico-born | 11,036,700 | 97.23 / 87.11 | 8,810 / 7,893 | | | +3.46 / +8.80 |

- **Share.** $4.4 / 4.1bn is 4.5% / 4.7% of the Mexico-born line and 1.18% / 0.95% of the case.
- **Convention (b):** 418,400 members and $5.11 / 5.31bn; the 65+ part is $3.31 / 3.33bn ($15.1k / 15.2k).
- **The change from September 27** is the pension switch for the 65+. It moves $−1.09 / −1.48bn onto the late
  line (set less cash set). At 65+ it cuts Social Security from $4,118 / 5,783 a head to $1,934 / 1,008 and
  Medicare from $12,064 to $8,208 / 7,880. Late arrivals now 65+ pay payroll tax on a small base, and the accrual
  follows that base. Younger arrivals now 65+ fall further ($21.8k / 24.6k cash to $12.6k / 11.7k), because
  they draw larger benefits. Younger arrivals aged 50–64 rise, because they pay in.
- **At 65+ the late arrivals now cost more a head than earlier arrivals** ($14.9k / 14.4k against $12.6k /
  11.7k). The pension switch removes the Social Security gap that made them cheaper on the September 27 case.
  What remains are their lower taxes (−$7.6k / −6.1k against −$9.1k / −9.0k a head) and higher Medicaid.

**The cash set, central reading, (a):**

| Subgroup | Persons (row 4) | $bn low / high | $ per person low / high | Lower-edge reading $bn | Upper-edge reading $bn | Change from September 27, $bn |
|---|---|---|---|---|---|---|
| Arrived at 50+, all ages | 362,200 | 5.47 / 5.61 | 15,095 / 15,475 | 4.77 / 5.15 | 7.02 / 7.17 | −0.20 / −0.19 |
| of them 65+ | 207,100 | 4.32 / 4.81 | 20,849 / 23,188 | 3.98 / 4.41 | 5.43 / 6.05 | −0.12 / −0.10 |
| of them 50–64 | 155,100 | 1.15 / 0.80 | 7,408 / 5,172 | 0.79 / 0.74 | 1.59 / 1.12 | −0.08 / −0.09 |
| Arrived younger, now 65+ | 1,344,800 | 29.27 / 33.13 | 21,768 / 24,638 | | | −1.52 / −1.45 |
| All Mexico-born | 11,036,700 | 87.20 / 72.73 | 7,901 / 6,590 | | | −6.57 / −5.58 |

In both tables the two age parts add to "arrived at 50+": where rounding each cell breaks the sum, the part nearest its
rounding boundary moves by one unit of its last digit (persons 207,100 for 207,163; set, upper edge 3.85 for 3.844;
cash set 4.81 for 4.804, 3.98 for 3.986 and −0.08 for −0.073).

Without the pension switch v4 moves the late line by −$0.2bn, mostly the long-run property taxes (−$0.26bn, against
+$0.10–0.11bn more services). The 65+ still cost less a head than earlier arrivals ($20.8k / 23.2k against
$21.8k / 24.6k), as on September 27.

**Medicaid check** (`medicaid_check.py --set sept29` → `derived/medicaid_check_sept29.csv`). v4 leaves the Medicaid
line alone: every cell's Medicaid part equals September 27's. Under the set the pension switch books Part A at its
accrual on each cell's HI receipts and removes Part A's share (0.3751) of current spending from the key. Only Parts
B and D, (1 − 0.3751) × the cash set's charge, are still priced by the MEPS key, so only they are re-keyed; the
accrual is reported beside them (`account_medicare_part_a_accrual_bn`). For the late arrivals now 65+:
- the set: Medicaid +$0.038 / +0.031bn, Medicare −$0.215bn, net **−$0.177 / −0.184bn** (three decimals, so the parts
  add);
- the cash set: unchanged from September 27, net −$0.31bn.

**Gates**, all passing (`run_cells.cjs`: 33 per run in the set and 32 in the cash set, which has no per-specification
file, at each of the three readings; `verify.py --set sept29`: 78 checks; `medicaid_check.py --set sept29`: 11):
- the September 27 steps' gates, unchanged (the netted edits add to `corrections.json` in all 278 cells);
- the union's items reproduce v4's part of the payload: 135 cells to 7.1e-15bn;
- item 3's cell shifts add to the union's (4.4e-16bn); the row-4 production grids add to the payload's (1.1e-13bn);
- the cells' v4 tails add to the union's (1.1e-12bn), and each payload gives the model its chain built (exact);
- **oracle:** the union reproduces the adopted lane's band at 48 / 11 (`main_case_bands.csv`, rows `adopted` and
  `cash_set`), $371.4146–434.8410bn and $294.7011–361.8175bn (tolerance 1e-4, the band's four decimals), and for the
  set its per-specification cost (`per_spec.csv`, 1.7e-13bn). The uncorrected union reproduces the row
  `uncorrected_at_adopted_responses`, $313.2581–378.9158bn (1e-4). The adopted `package.cjs` `evaluateFull` (for the
  cash set, on `forPayload` of its payload) gives every model's cost, union and cells (difference 0);
- the nine cells add to the union in all 64 specifications, corrected and uncorrected (1.4e-12bn), and every
  programme part adds to the union's at both ends (1.5e-12bn);
- the cells' September 27 costs at the same ends add to the September 27 band (1e-4);
- `verify.py --set sept29`: in both sets, all three readings, both conventions and both ends, late + younger equals
  the generation lane's G1 (`generation_summary_sept29{,_cash}.json`) to 9e-11bn. The cells add to the published
  band (5.01e-5), and `late_arrival_line_sept29.csv` adds within 1e-5.

`rerun_lane.py` gates (times from `date`, JST). The thirteen September 27 commands are `counts.py`, `run_split.sh` at
each reading, `run_cells.cjs --case sept27` and `--case sept26_schools` at each reading, `build_line.py`,
`medicaid_check.py` and `verify.py`. The nine sept29 commands are `run_cells.cjs --case sept29` and `--case sept29_cash`
at each reading, then the three scripts with `--set sept29`.
- Before the reboot: at 17:12 the old commands reproduced all 22 derived and lane files; `run_cells.cjs` showed as
  CHANGED only because it was edited during the pass. After the repoint, gate 1 was IDENTICAL, 23/23 (20:18–20:23). A
  gate label in `run_cells.cjs` was then corrected (20:31), and gate 1 was running again when the machine rebooted.
- After the reboot, with `UV_OFFLINE=1`: the first attempt (21:16) stopped when uv could not reach PyPI to resolve
  `--with openpyxl --with xlrd` (a connect timeout, not a lane failure), and uv's cache resolves both packages. Every
  command ran directly, all passing (21:25–21:35). Gate 1: IDENTICAL, 23/23, exit 0 (21:35–21:39). Gate 4, the
  thirteen commands and the nine: pass 1 IDENTICAL, 23/23, exit 0 (21:39–21:43); pass 2 IDENTICAL, 23/23, exit 0
  (21:43–21:48). No script was reported NOT RUN. Of the tracked files, only `RESULT.md` and the five changed scripts
  differ from HEAD.

**Files.**
- Changed: `run_split.sh` (step 7), `run_cells.cjs` (`--case sept29|sept29_cash`; `tenant_occupied_property` under
  property taxes), and `build_line.py`, `verify.py` and `medicaid_check.py` (`--set sept29`).
- New outputs: `derived/late_arrival_line_sept29.csv` and `derived/medicaid_check_sept29.csv`, beside the default
  files, which keep their two cases. `late_arrival_line_sept29.csv` adds two rows beside each total, never added to
  it: `sept27_total` and `change_from_sept27`.
- New intermediates, ignored: `_cache/cells_sept29{,_cash}_<reading>.json`, and `_cache/split_<reading>/v4_inputs.json`
  and `tax_key_by_generation.json`.
- Rebuild, after `LATE_DEF=<r> bash run_split.sh` for each reading: `node run_cells.cjs --case sept29|sept29_cash
  --def <r>`, then `build_line.py --set sept29`, `medicaid_check.py --set sept29` and `verify.py --set sept29`.
  `verify.py` needs the generation lane's step 7 first.
- `run_cells.cjs` loads the generation lane's `v4_split.cjs`, and `run_split.sh` runs its `v4_inputs.py` and
  `tax_key_split.py`: that lane's v4 files go in the same commit or an earlier one.

Log (times from `date`, JST): 15:17 brief read; 17:03 first sept29 run gated; 17:07 line and check built; 17:14 late
lane wired end to end; 17:21 rebuilt with the Part A rule per HI tax dollar; 20:15 repointed to the adopted lane
(40c4ba7); 20:16 rebuilt; 20:18–20:23 gate 1; 20:31 gate label corrected; about 20:51 reboot; 21:13 resumed; 21:16
PyPI timeout; 21:25–21:35 every command directly; 21:35–21:48 gates 1 and 4 (two passes).

## 7. v5 case (oct05), 2026-10-05

The operator adopted main case v5 on 2026-10-05 at 22:54 JST (`main_case_2026_10_05`, case key `oct05`). It is the
September 29 case plus 3.04M descendants of Mexican immigrants who no longer report Mexican origin, counted whole:
$390.2940–461.2431bn, and $307.3764–383.4093bn in the cash set. `run_cells.cjs` runs both as `--case oct05` and
`--case oct05_cash`. Model self-report: claude-opus-5-5.

**Method.** The sept29 steps run unchanged and give each cell's September 29 payload. The v5 part then goes on each
cell by the generation lane's `v5_split.cjs` (its RESULT section "v5 case (oct05)"):
- **The added people go on the G3plus cell.** That cell takes the lineage's cell edits and the production grid's change.
  The added people are third-plus by construction and have no arrival year, so no G1 cell takes any of them.
- **Row 8 is split by share.** Every cell takes audit row 8's change at the larger group (−$0.0080bn) times its share of
  the September 29 union's `lane_constants` k cell.
- **The responses follow the group's size.** Every cell is evaluated at v5's responses, which move with the group's
  size.

The G1 cells therefore move only by the response move and their row-8 share. Per-person figures keep the row-4
headcounts; the third-plus row counts the added people (17.38M), its adults at the identified G3+'s adult share
[ASSUMPTION, as in the generation lane]. The change is now measured from the September 29 case.

**The set, central reading, (a)** ($bn a year at the union's ends, 48 / 11; [CALCULATION:
`derived/late_arrival_line_oct05.csv`]):

| Subgroup | Persons (row 4) | $bn low / high | $ per person low / high | Lower-edge reading $bn | Upper-edge reading $bn | Change from September 29, $bn |
|---|---|---|---|---|---|---|
| Arrived at 50+, all ages | 362,200 | 4.38 / 4.13 | 12,085 / 11,394 | 3.69 / 3.68 | 5.58 / 5.23 | −0.003 / −0.003 |
| of them 65+ | 207,100 | 3.09 / 2.98 | 14,925 / 14,381 | 2.86 / 2.74 | 3.84 / 3.69 | −0.002 / −0.002 |
| of them 50–64 | 155,100 | 1.29 / 1.15 | 8,291 / 7,404 | 0.83 / 0.94 | 1.74 / 1.54 | −0.001 / −0.001 |
| Arrived at 55+ | 210,700 | 2.98 / 2.88 | 14,128 / 13,677 | 2.45 / 2.37 | 3.42 / 3.27 | −0.002 / −0.002 |
| Arrived younger, now 50+ | 4,631,100 | 41.97 / 38.10 | 9,062 / 8,227 | | | −0.04 / −0.05 |
| All Mexico-born | 11,036,700 | 97.15 / 87.02 | 8,802 / 7,885 | | | −0.09 / −0.09 |

The age parts add to "arrived at 50+" as in section 6 (persons 207,100 for 207,163; no dollar cell needed moving).

- **Convention (b):** 418,400 members and $5.11 / 5.31bn; the 65+ part is $3.30 / 3.33bn.
- **The cash set**, central, (a): arrived at 50+ $5.47 / 5.60bn ($15,086 / 15,467), of them 65+ $4.32 / 4.80bn; the
  change from the September 29 cash set is the same −$0.003bn.
- **Share.** $4.38 / 4.13bn is 4.5% / 4.7% of the Mexico-born line and 1.12% / 0.89% of the case (1.18% / 0.95% on
  September 29: the case grew, the line did not).
- **Medicaid check** (`medicaid_check.py --set oct05` → `derived/medicaid_check_oct05.csv`). v5 touches neither the
  Medicaid nor the Medicare line of a G1 cell, so the file equals `medicaid_check_sept29.csv` but for its case labels:
  net −$0.177 / −0.184bn in the set, −$0.31bn in the cash set. A new gate holds every G1 cell's two parts at their
  sept29 values (1e-12). The Part A accrual gate now covers the eight cells without the added people. The added
  people's own Part A accrual sits in their cell edits, not in `meta.pension_accrual`.

**Gates**, all passing:
- `run_cells.cjs`: 37 per run in the set and 36 in the cash set, at each of the three readings. They add four to the
  sept29 runs: the v5 payload builds on the September 29 payload built here; the row-8 shares add to 1, and the nine
  v5 models add to the case's payload model (cells 1.4e-12bn, grid 1.1e-13bn), per convention; the specifications are
  the v5 package's. The oracle is the v5 lane's `main_case_bands.csv` (`adopted`, `cash_set`) at 48 / 11 to 1e-4, and
  `per_spec.csv` for the set (1.7e-13bn). The v5 package's `evaluateFull` gives every model's cost (difference 0), and
  the cells' September 29 costs add to the September 29 band (1e-4).
- `verify.py --set oct05`: 102 checks. In both sets, all readings, conventions and ends, late + younger equals the
  generation lane's G1 (`generation_summary_oct05*.json`) to 9e-11bn. The G3plus cell, with the added people, equals
  the generation lane's G3plus in cost, members and adults (1e-6).
- `medicaid_check.py --set oct05`: 15 gates.

`rerun_lane.py --online` over 31 commands: the thirteen September 27 commands, the nine sept29 commands, and the nine
oct05 commands. The oct05 commands are `run_cells.cjs --case oct05` and `--case oct05_cash` at each reading, then
`build_line.py`, `medicaid_check.py` and `verify.py` with `--set oct05`. Result: IDENTICAL, 25/25 files, exit 0
(23:20:27–23:24:25 JST), with no script NOT RUN. `--online` was needed because uv's offline cache cannot resolve
`run_split.sh`'s `--with openpyxl --with xlrd`.

**Files.**
- Changed: `run_cells.cjs` (`--case oct05|oct05_cash`, `v5Part()`), and `build_line.py`, `verify.py` and
  `medicaid_check.py` (`--set oct05`).
- New outputs: `derived/late_arrival_line_oct05.csv` (rows `sept29_total` and `change_from_sept29` beside each total)
  and `derived/medicaid_check_oct05.csv`. Ignored intermediates: `_cache/cells_oct05{,_cash}_<reading>.json`.
- `run_cells.cjs` loads the generation lane's `v5_split.cjs`, and `verify.py` reads its `generation_summary_oct05*.json`.
  That lane's v5 files (commit e5ca5efe) come first.

Log (times from `date` and file times, JST): by 23:18 the six oct05 runs, line, check and verify, and the edited
scripts compiled (their `.pyc` times); 23:20:27–23:24:25 `rerun_lane.py` IDENTICAL 25/25, exit 0; 23:28 this section.

## 8. v6 case (oct07), 2026-10-07

Main case v6 (`main_case_2026_10_07`, case key `oct07`) was adopted on 2026-10-07
(decisions/2026-10-07-main-case-v6.md). It is v5 plus four items (`meta.items`):
- the pension accrual on the 2026 Trustees paths (set only);
- retiree health on accrual;
- the added people at their measured age mix;
- user fees with the education keys.

It costs $389.0826–461.4797bn, and $307.3994–385.3641bn in the cash set. `run_cells.cjs` runs both as `--case oct07`
and `--case oct07_cash`. Model self-report: claude-opus-5-5.

**Method.** The sept29 steps run unchanged and give each cell's September 29 payload. The v6 part then goes on each
cell by the generation lane's `v6_split.cjs` (its RESULT section "v6 case (oct07)"), over the nine cells instead of the
three generations:
- **The lineage block** (the lineage item's values) goes on the G3plus cell. Every cell takes row 8's edit at its share
  of the September 29 union's `lane_constants` k cell.
- **Retiree health's ten national-scale edits** go on every cell as they are. Each cell carries the union's national
  totals, so its share of every line holds.
- **The pension item's union parts** follow the September 29 split's pension rule with the 2026 per-generation factors.
  Each G1 cell takes G1's factor (×0.98595 on the accrual per tax dollar, ×1.00109 on Part A) on its own OASDI receipts
  and Part A accrual. The lineage parts go on the G3plus cell.
- **User fees** go pro rata to each cell's share of the union amount of the part's split-basis line
  (`meta.user_fees.splits.split_basis`), and so do the carriers. The added people take none.

Two of the user-fee rules are assumptions:
- **Pell** (`union_key_pell`, +$3.87 / 3.97bn at the union) goes by `education_services`, the case's rule
  [ASSUMPTION]. A college-enrollment key would be better, but none exists by person or generation here. Pell's own
  line, `other_federal_benefits`, is keyed by adult cash assistance. The part stays on that line in the engine, so this
  lane's programme rows show it under other transfers; its split across cells follows education's shares.
- **The K-12 weight's two parts** sit on row 6's re-blend lines (`school_reprice`, `college_rekey`), which carry no cell
  amounts here, so they also go by `education_services` [ASSUMPTION]. In the household split and the decomposition this
  moves $0.10 / 0.04bn from schools to other education. Here both lines sit in the education programme.

Per-person figures keep the row-4 headcounts. The third-plus row counts the added people, its adults at their measured
age mix (1,609,482) [ASSUMPTION, as in the generation lane]. The change is measured from v5 (`oct05`).

**The set, central reading, (a)** ($bn a year at the union's ends, 48 / 11; [CALCULATION:
`derived/late_arrival_line_oct07.csv`]):

| Subgroup | Persons (row 4) | $bn low / high | $ per person low / high | Lower-edge reading $bn | Upper-edge reading $bn | Change from v5, $bn |
|---|---|---|---|---|---|---|
| Arrived at 50+, all ages | 362,200 | 4.36 / 4.12 | 12,047 / 11,360 | 3.68 / 3.67 | 5.57 / 5.21 | −0.014 / −0.012 |
| of them 65+ | 207,100 | 3.08 / 2.97 | 14,868 / 14,320 | 2.85 / 2.73 | 3.83 / 3.67 | −0.012 / −0.012 |
| of them 50–64 | 155,100 | 1.28 / 1.15 | 8,278 / 7,405 | 0.83 / 0.94 | 1.74 / 1.54 | −0.002 / 0.000 |
| Arrived at 55+ | 210,700 | 2.97 / 2.87 | 14,080 / 13,636 | 2.44 / 2.36 | 3.41 / 3.26 | −0.010 / −0.009 |
| Arrived younger, now 50+ | 4,631,100 | 41.81 / 37.89 | 9,028 / 8,182 | | | −0.16 / −0.21 |
| All Mexico-born | 11,036,700 | 96.89 / 86.66 | 8,779 / 7,852 | | | −0.26 / −0.36 |

The age parts add to "arrived at 50+" as in section 6: persons print 207,100 for 207,163, and the high end's change for
65+ prints −0.012 for −0.0127, by largest remainder.

- **Convention (b):** 418,400 members and $5.09 / 5.29bn; the 65+ part is $3.29 / 3.31bn. The change from v5 is
  −$0.015 / 0.014bn.
- **The cash set**, central, (a): arrived at 50+ cost $5.46 / 5.60bn ($15,076 / 15,455), of them 65+ $4.31 / 4.79bn.
  The change from the v5 cash set is −$0.004 / 0.004bn.
- **Share.** $4.36 / 4.12bn is 4.5% / 4.7% of the Mexico-born line and 1.12% / 0.89% of the case, as on v5.
- **What moves them.** v6 moves the late arrivals by −$0.014 / 0.012bn (printed by largest remainder so that it adds):
  - Social Security −$0.010 / 0.008bn: G1's accrual per tax dollar falls (×0.98595) on the 2026 paths. Medicare
    +$0.001 / 0.000bn: G1's Part A factor (×1.00109).
  - Education −$0.015 / 0.002bn and capital −$0.003 / 0.001bn: the user-fee item and its offsets.
  - Services +$0.011 / 0.012bn: the service lines that retiree health's normal costs and item 4's health parts move.
  - Other transfers +$0.002 / −0.013bn: Pell, kept on `other_federal_benefits`, less retiree health's cut of that line.

  The Mexico-born line moves −$0.26 / 0.36bn: Social Security −$0.36 / 0.44bn, education −$0.78 / 0.21bn, capital
  −$0.15 / 0.06bn, Medicare +$0.02bn, other transfers +$0.68 / −0.02bn and services +$0.33 / 0.35bn.
  [CALCULATION: `late_arrival_line_oct07.csv` less `late_arrival_line_oct05.csv`, by programme]
- **Pell by its own line** (`split_basis_edited_line_move`, beside each total). Split by `all_cash` as its edited line
  would split it, Pell would move the late arrivals by +$0.046 / 0.073bn in (a), and +$0.039 / 0.056bn in (b). It
  would move the Mexico-born line by +$0.07 / 1.01bn in (a) and −$0.62 / 0.51bn in (b), the generation lane's G1
  figures. The nine cells still add to the case (1e-9). The cash set's moves are the same, since item 4 enters both
  sets alike.
- **Medicaid check** (`medicaid_check.py --set oct07` → `derived/medicaid_check_oct07.csv`). The re-key is unchanged:
  net −$0.177 / −0.184bn in the set and −$0.31bn in the cash set. Only the cells' Part A accrual moves, since v6 books
  Part A at $40.783bn on the 2026 paths against $41.137bn. G1's Part A factor is above 1 (×1.00109), so the late
  arrivals' 65+ accrual rises from $0.1386bn to $0.1389bn at the low end. The gate against oct05 holds every G1 cell's
  Medicaid part, and its Medicare part less its change in Part A accrual (1e-12). The cash set has no accrual. Of the
  file's 532 rows, only the 12 Part A accrual rows differ from `medicaid_check_oct05.csv`.

**Gates**, all passing:
- `run_cells.cjs`: 53 per run in the set and 50 in the cash set, at each of the three readings. The v6 part's gates, per
  convention:
  - the v6 payload builds on the September 29 payload built here, and `v6_split.cjs` runs on the same engine and model;
  - the row-8 shares add to 1, the lineage goes on G3plus, and the nine v6 models add to the case's payload model
    (cells 1.4e-12bn, grid 1.1e-13bn);
  - each cell shift's shares add to 1 (1e-12), and before each of the ten national-scale edits every cell carries the
    union's national total (exact);
  - the carriers' shares add to 1 and their key values to the union's (1e-12 relative);
  - the September 29 pension rule reproduces each cell's pension references (1e-9);
  - beside the case, with the parts split by their edited lines, the nine models add to the case's payload model and
    the nine cells to the case's band at both ends (1e-9).

  The engine gates:
  - The oracle is the v6 lane's `main_case_bands.csv` (`adopted`, `cash_set`) at 48 / 11, to four decimals.
  - New with v6, the union also matches the band in `summary.json` at full precision (1e-6): $389.082553 / 461.479709bn,
    and $307.399411 / 385.364123bn in the cash set.
  - The nine cells add to the union in all 64 specifications, corrected and uncorrected (1.5e-12bn).
  - The v6 package's `evaluateFull` gives every model's cost (difference 0).
  - The cells' v5 costs add to the v5 band (1e-4).
- `verify.py --set oct07`: 103 checks. In both sets, all readings, conventions and ends, late + younger equals the
  generation lane's G1 (`generation_summary_oct07*.json`) to 8.8e-11bn. The G3plus cell, with the added people, equals
  the generation lane's G3plus in cost, members and adults (1e-6).
- `medicaid_check.py --set oct07`: 16 gates.

`rerun_lane.py --online` ran 40 commands: the 31 of v5, then `run_cells.cjs --case oct07` and `--case oct07_cash` at
each reading, then `build_line.py`, `medicaid_check.py` and `verify.py` with `--set oct07`. Result: IDENTICAL, 27/27
files, exit 0 (15:08:38–15:12:43 JST by `date`), with no script NOT RUN. `git diff --quiet` on `derived/` gave rc 0.

**Files.**
- Changed: `run_cells.cjs` (`--case oct07|oct07_cash`, `v6Part()`, the edited-line cells beside the case, the
  full-precision band gate), and `build_line.py` (`--set oct07`, `split_basis_edited_line_move`), `verify.py` and
  `medicaid_check.py` (`--set oct07`).
- New outputs:
  - `derived/late_arrival_line_oct07.csv`, with rows `oct05_total`, `change_from_oct05` and
    `split_basis_edited_line_move` beside each total;
  - `derived/medicaid_check_oct07.csv`;
  - ignored intermediates: `_cache/cells_oct07{,_cash}_<reading>.json`.
- `run_cells.cjs` loads the generation lane's `v6_split.cjs`, and `verify.py` reads its `generation_summary_oct07*.json`.
  That lane's v6 files come first (commit 3f583fb4).

Log (times from `date` and file times, JST):
- 15:04:02–15:04:15: the first final runs.
- 15:08:04–15:08:16: the finals rewritten with the full-precision band gate (all nine commands rc 0).
- 15:08:38–15:12:43: `rerun_lane.py` IDENTICAL 27/27, exit 0.
- This section was written after 15:29.

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
