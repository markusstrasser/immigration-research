claude-opus-5-5
**Verdict:** SSA's federal SSI by state and age, split on audit row 4 with the group's take-up equal to everyone
else's in each state and age, gives the group 10.33% / 10.21% of the SSI line (shared / personal). The case's
CPS-reported key gives 8.16% / 8.14%. Priced through the adopted package, the swap moves the case by **+$1.48 / +$1.49bn**
at specs 48 / 11. The case becomes $372.90 / $436.33bn, and the cash set $296.18 / $363.31bn; the sampling SE is
$0.53 / $0.55bn. This is an upper bound, not a better key, because equal take-up pays SSI to noncitizens that the 1996
rules mostly bar. Barring the imputed unauthorized cuts the move to +$0.93 / +$0.96bn, and barring every noncitizen
cuts it to +$0.69 / +$0.77bn. Raking the CPS's own reports to SSA's state and age totals reproduces the case
(−$0.01 / +$0.00bn), so the gap comes from the group's lower reported take-up within each state and age, not from the
CPS's geography. Beside the case, not adopted.

## The arm

The arm replaces the group's amount on the SSI line (`ssi` key) with national × household fraction × the
administrative share (65.134 × 0.99005 × share), the account's rule for a CPS key. The move is the same in the set and
the cash set: the SSI line has response 1 and fiscal weight 1 at both ends, and no capital component reads it
[DATA: derived/arm.csv, derived/arm.json].

| $bn | Group's share of the key, 48 / 11 | Group's SSI, 48 / 11 | Move, 48 / 11 (sampling SE) | Set, 48 / 11 | Cash set, 48 / 11 |
|---|---|---|---|---|---|
| Case: CPS-reported, row 4, fill-in step, CBO's shift | 8.16% / 8.14% (effective 8.03 / 7.90) | 5.1757 / 5.0940 | — | 371.4146 / 434.8410 | 294.7011 / 361.8175 |
| **Arm: SSA federal SSI by state × age, equal take-up** | **10.33% / 10.21%** | 6.6594 / 6.5837 | **+1.4837 / +1.4896** (0.53 / 0.55) | 372.8983 / 436.3306 | 296.1848 / 363.3071 |

The case's key sits under a fill-in step (union-matched hot deck) and CBO's income-group shift. Both correct CPS
reports, which an administrative key does not use, so the arm replaces the amount whole. Keeping them and adding
national × fraction × (administrative share − row-4 share), the back-test's sizing rule, moves the case +1.3967 /
+1.3341 [DATA: derived/arm.csv, `admin_state_age_additive`]. The SE is the replicate SE of the share's difference
from the row-4 share, and nearly all of it is the CPS sample under the case's key. The administrative share's own
SE is 0.10 pp, about $0.07bn [DATA: derived/shares.csv].

**How the key is built** [CALCULATION: ssi_key.py]:
- The state totals are federal SSI paid in calendar 2024: $59.655bn over the 50 states and DC. The source is SSA,
  Annual Statistical Supplement 2025, Table 7.B7 [SOURCE: https://www.ssa.gov/policy/docs/statcomps/supplement/2025/7b.xlsx].
  The line pays federal SSI only, so the key leaves out the federally administered state supplements.
- Each state's total is split over under 18, 18–64 and 65 or older by December 2024 federal payments. These are
  recipients × average payment from the SSI Annual Statistical Report 2024, Tables 10 and 11
  [SOURCE: https://www.ssa.gov/policy/docs/statcomps/ssi_asr/2024/ssi_asr24.xlsx], less the state's December
  supplementation (Supplement Table 7.B3). The supplementation is spread over ages at the national supplement's mix
  from ASR Table 5; California holds 95.4% of it.
- Both SSA files are the back-test lane's pinned browser downloads (`backtest_admin_totals_2026_09_28/_cache/`,
  hashes in its `derived/sources.json`). Nothing was fetched from SSA.
- Each civilian in a state × age cell carries the cell's dollars over its civilians on audit row 4's weights. The
  shared allocation splits each SPM unit's sum equally among its members, as the case's key does.

**Where the swap comes from.** The four steps add up to the arm [DATA: derived/arm.csv; CALCULATION: differences of
its rows]:

| Step ($bn) | 48 | 11 |
|---|---|---|
| Drop the fill-in step and CBO's shift (the case at its row-4 share) | +0.087 | +0.156 |
| SSA's state × {under 65, 65+} totals replace the CPS's, with the CPS's group shares within each cell (`hybrid_cps_within_cell`) | −0.101 | −0.153 |
| The group's citizens at their cell's citizen average (to `admin_citizens_only`) | +0.707 | +0.770 |
| Noncitizens at their cell's average (to the arm) | +0.791 | +0.717 |
| **Arm** | **+1.484** | **+1.490** |

The CPS gets the state and age spread about right: the second step is within noise (SE $0.34bn). The gap sits
within cells:
- In California, Texas and New Mexico, 23.5M of the group's 39.7M, the two keys nearly agree on the group's share of
  each state's SSI: California 27.9% (administrative) against 27.1% (CPS), Texas 30.3% against 31.9%, New Mexico
  31.7% against 32.1% [DATA: derived/by_state.csv].
- 84% of the gap, 1.75 of 2.07 pp at 11, lies in the other 48 areas. There the CPS holds few group recipients: 203
  group persons report SSI nationally and none in 19 states, where the administrative key puts 1.10% of the line,
  about $0.71bn, on the group [DATA: derived/by_state.csv, derived/cps_checks.csv; CALCULATION].
- The group's working-age members there are more often noncitizens, 28.6% against 22.5% in the three states
  [CALCULATION: derived/key_cells.csv, civilians × group share × group noncitizen share].

## The key's own bias

**Noncitizen eligibility.** Equal take-up pays each noncitizen the cell's average. Since August 22, 1996 a noncitizen
needs two things. The first is a qualified-alien status, such as lawful permanent residence, refugee, asylee or
parolee. The second is one of a short list of conditions:
- receiving SSI and lawfully residing in the U.S. on that date;
- lawful permanent residence with 40 qualifying quarters of work, and not within the first five years for entrants
  after that date;
- military service;
- lawful residence on that date plus blindness or disability;
- the first seven years as a refugee or asylee.

The unauthorized qualify under none [SOURCE: SSA, Spotlight on SSI benefits for noncitizens, read via the Wayback
copy; quotes in reads/sources_read.md]. In the CPS, noncitizens are 18.1% of the group but hold 7.4% of its reported
SSI dollars. The flagged unauthorized, 11.6% of the group, report none, by construction: the status rules read SSI
receipt as evidence of legal status [DATA: derived/cps_checks.csv]. Two bounds follow:
- barring the flag moves the case +0.9257 / +0.9646 (shares 9.46% / 9.40%);
- barring every noncitizen moves it +0.6932 / +0.7724 (9.10% / 9.10%).

Under take-up equal within citizenship, the key lies between the citizens-only bound and the arm. Where in between
depends on SSA's noncitizen recipient counts, which the next section leaves unread. [INFERENCE]

**State supplements.** The line pays federal SSI only, and the key uses federal SSI. A key built on federally
administered totals, which include California's $3.256bn supplement (of $3.414bn nationally), would move the case
+2.0205 / +2.0060. That is $0.54 / $0.52bn more than the arm, because the group is 33% of California's population
[DATA: derived/arm.csv, derived/by_state.csv; SOURCE: 7.B7]. The supplement's split by age inside a state is
modelled: the national age mix applied to each state's December supplement. The December federal cells it leaves
match 7.B3's federal payments within 0.14% in every state [DATA: derived/audit.json]. The supplement itself is
California's cost, not this line's.

**CPS under-reporting.** This bias touches the case's key, not the administrative one, which uses no reports.
- Overall, the CPS reports $58.64bn against SSA's $63.07bn federally administered, a ratio of 0.93. The ratio is
  1.02 under 65, because CPS income items start at age 15 and children's SSI sits on a parent's record, and 0.69 at
  65 and over [DATA: derived/cps_checks.csv].
- The same age pattern appears in 2012 linked data: 123.2% at 18–64 and 72.7% at 65 and over
  [SOURCE: Census SEHSD-WP2017-39, Table 1].
- The group is young, so the elderly shortfall tilts the CPS key toward it. Raking to SSA's totals takes that back
  (step 2 above).
- The group's reported SSI is imputed no more often than others': 36.3% of its dollars against 37.2%
  [DATA: derived/cps_checks.csv].
- No linked study splits SSI misreporting by Hispanic origin or nativity (reads/sources_read.md). For Social Security
  receipt at 65 and over, Hispanic respondents miss more often than white non-Hispanics (false negatives 14.3%
  against 6.4%; foreign-born 16.3%, noncitizens 20.7%). False positives offset most of this: net receipt is 0.760
  against 0.788 linked for Hispanics and 0.876 against 0.881 for white non-Hispanics [SOURCE: SEHSD-WP2017-39,
  Table 6 Panel A]. That is a net differential of about 3 points.
- If SSI behaves like Social Security, the CPS understates the group's SSI by about 3%, or +$0.15bn. That is about a
  fifth of the citizens-only step (+0.707 / +0.770). The rest of the within-cell gap would then be real: lower
  disability receipt or higher counted income among the group's citizens. The lane cannot separate these.
  [INFERENCE]

**Smaller points.**
- The age split applies December 2024's mix to calendar-year totals. CPS ages are at the March 2025 interview.
- SSA's totals include institutionalized recipients, and the key keeps the case's household fraction (0.990).
- A key without the age split overstates the group, +2.0833 / +2.1642, because SSI per head rises with age and the
  group is young [DATA: derived/arm.csv, derived/by_age.csv].

## Beside the case, not adopted

Nothing in the adopted case changes. Recommendation: keep the CPS key. On the evidence here, the SSI key's
correction lies between 0 and +$1.5bn. The legally informed bounds, +$0.69 to +$0.96bn, are 1.3–1.8 SEs from zero,
under the back-test's $2bn materiality.

The sharper test exists and was not run. ASR Tables 29–33 (noncitizen recipients by state, age and country of
origin) and Table 14 (foreign-born recipients by country) would replace the bar assumption with counts. They were
read by title only, so the back-test's planned blind test stays blind (its post-hoc note 6). The test would run in two
steps:
1. predict Mexico-born and noncitizen recipients from the CPS on row 4, and have the parent commit the prediction;
2. open the tables.

## Gates

- **Oracle:** the payload models give 371.4146 / 434.8410 (set) and 294.7011 / 361.8175 (cash set) at 48 / 11. They
  match `main_case_2026_09_29/derived/summary.json` to 1e-9, and a zero edit returns them exactly
  [DATA: derived/arm.json gates].
- **State totals equal SSA's published totals:**
  - The key's state totals equal 7.B7's federal SSI in all 51 areas (maximum gap 9.3e-10 $k; $59.655194bn in all).
  - The supplement variant's totals equal 7.B7's totals (1.9e-9 $k).
  - Table 10's categories and ages add to its totals, and its areas to "All areas".
  - 7.B7's parts add to its totals within $1k.
  - The December cells match Table 11's all-age averages within 0.06% and 7.B3's federal payments within 0.14%
    [DATA: derived/audit.json].
- **Case reproduced:**
  - row 4's union is 39,712,493 persons;
  - the household fraction is 0.9900527030;
  - the flag counts are 9.992831M and 4.607453M;
  - the case's SSI shares and SEs match the back-test's stored ones to 4.4e-12 and 4.5e-13;
  - every priced move equals its edit (1e-9) [DATA: derived/audit.json, derived/arm.json].
- **Reruns:** `rerun_lane` passed twice, IDENTICAL; the counts are in the log.

## Files and reproduction

- `ssi_key.py` builds the SSA cells and the keys. It writes `derived/ssa_cells.csv`, `key_cells.csv`, `shares.csv`,
  `by_age.csv`, `by_state.csv`, `cps_checks.csv` and `audit.json`.
- `price_arm.cjs` prices every key through `main_case_2026_09_29/package.cjs` and the cash payload, and writes
  `derived/arm.csv` and `arm.json`.
- `reads/sources_read.md` holds the quoted SSA rules and the Bee–Mitchell table cells.
- It imports the CPS lane's frame, masks and row-4 weights (`cps_imputation_keys_2026_09_23`) read-only.

```sh
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/ssi_key_bound_2026_09_30 \
  "uv run --no-project --with openpyxl python3 {lane}/ssi_key.py" "node {lane}/price_arm.cjs"
```

Nothing is committed, staged or stashed. Nothing outside this directory was written.

## Log

- started: lane created; inputs not yet inspected.
- 2026-09-30 02:34 JST: inputs located, nothing fetched. SSA files are the back-test lane's browser downloads
  (`backtest_admin_totals_2026_09_28/_cache/ssa_ssi_asr24.xlsx`, `ssa_supplement2025_7b.xlsx`, hashes in its
  `derived/sources.json`): 7.B7 (federal SSI and state supplementation, calendar 2024, by state), 7.B3
  (December supplementation by state), ASR Tables 10 and 11 (December recipients and average payment by state and
  age) and Table 5 (national payments by type and age). Tables 14 and 29–33 (foreign-born and noncitizen
  recipients) were read by title only, to keep the back-test's planned blind test blind (its post-hoc note 6).
- 2026-09-30 02:34 JST: oracle probe: the payload models give 371.4146 / 434.8410 (set) and 294.7011 / 361.8175 (cash) at specs
  48 / 11; the SSI line is keyed `ssi`, national 65.134, response 1, group amount 5.1757 (shared) / 5.0940
  (personal) $bn.
- 2026-09-30 02:41 JST: `ssi_key.py` runs (about 30 s), all gates pass: SSA tables hold the 51 areas and add up; the key's state
  totals equal 7.B7's federal SSI (max gap 9.3e-10 $k); row 4 gives the union 39,712,493 and the back-test's
  household fraction and flag counts; the case's SSI shares reproduce the back-test's stored ones (4.4e-12).
  Group share of the key, personal / shared: case 8.141% / 8.161%; administrative, equal take-up by state x age,
  10.210% / 10.327% (+2.07 / +2.17 pp, SE 0.85 / 0.83 pp).
- 2026-09-30 02:41 JST: `price_arm.cjs` runs, all gates pass (oracle to 1e-9 and printed decimals, zero edit exact, every move equals
  its edit). The arm moves the case +1.4837 / +1.4896 $bn at 48 / 11, set and cash alike.
- 2026-09-30 02:42 JST (the rerun logs' modification times, from `stat`): two `rerun_lane` passes over the 12 files
  then present: both IDENTICAL, exit 0.
- 2026-09-30 02:47 JST (`reads/sources_read.md`'s modification time, from `stat`): sources for the bias read: SSA's noncitizen rules (Wayback copy) and Bee and Mitchell (2017),
  Tables 1 and 6, re-read from the primary PDF. A researcher sub-agent's literature pass (stopped at 40 turns) found
  no SSI misreporting split by ethnicity or nativity; its notes stay outside the repo, and only what was re-read is
  cited (`reads/sources_read.md`).
- 2026-09-30 03:02 JST (`date` at each pass's end): after the reads and this RESULT were written, two more
  `rerun_lane` passes over all 13 files: both `[rerun] IDENTICAL: 13/13 files unchanged`, exit 0. Only this log
  line was written after them; no script reads or writes this file.
