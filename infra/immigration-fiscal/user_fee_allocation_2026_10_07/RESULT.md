claude-opus-5-5

**Verdict:** The account's netting of user fees is a small bias, not a material one. Crediting fees in proportion
to use understates the group's cost by **$2.79bn** at both ends of main case v5: public-college tuition $1.84bn,
the insured part of public-hospital charges $0.95bn, and other sales (paid per use) taken as zero. That is 0.6–0.7%
of the $390.29–461.24bn band. The keys on the same lines are wrong by more, and in the other direction. The account
keys public higher education's net cost by the ledger's item P, non-school capital outlay per head by state, which
the builder names "postsecondary". P gives the group 0.139 of the line, against its measured 0.116 share of public
colleges' cost, an overcharge of $5.45bn. Priced together as an engine edit, these lines move the case by
**−$2.58bn / −$3.16bn**, to $387.71–458.08bn (cash set $304.80–380.25bn). The edit covers the fee terms, the
use keys on higher education and its capital, BEA's K-12 weight, Pell at the group's share, the hospitals' insured
net and transit by rides. **Recommend it for the next main case as one item, with all its parts.** The fee term
alone would raise the case $2.79bn, while the full correction of the same lines lowers it. [CALCULATION: case.cjs, 30 gates]

**Parent's review (2026-10-07 12:23 JST): the transit terms are not new, so the next case takes every part but
transit.** v3's item 8 tested the same object, the transit loss inside the enterprise surplus, at the same ACS ratio
(0.7465). Weighting each state's rider share by where the deficit falls gave 1.019 (SE 0.017) times the population
key, and v4 kept that reading beside because it changes nothing distinguishable
(`main_case_candidate_v3_2026_09_28/RESULT.md`, item 8; `decisions/2026-09-29-main-case-v4.md`, rejected 4). The
national ratio used here assumes the same subsidy per rider in every state, which the state finance data reject:
California carries 20.7% of the deficit and the group is 26.8% of its riders. Without the transit operating and
capital terms, the lane moves v5 by **−$0.296bn / −$0.726bn** at specifications 48 / 11, on the set and the cash set
alike (from `derived/case_oct05.json`). That nets the higher-education key fix, the tuition fee term, Pell at the
group's share, the hospital terms, the K-12 weight and the college and K-12 capital keys.

# User-fee netting in the service allocation (2026-10-07)

Question: the account charges each public-service line at its national net cost (NIPA gross output
less sales) and allocates that net cost by a use key. If the group's share of fees paid (s_R)
differs from its share of use (s_C), the group's true net subsidy differs by (s_C − s_R) × R per
line. This lane sizes Σ (s_C − s_R) × R × response.

## Result

Split exactly, the group's true net subsidy on a line less what the account charges it is

    s_U G − s_R R − s_K N = (s_U − s_R) R + (s_U − s_K) N,     G = N + R,

where s_U is the group's share of use, s_R its share of fees and s_K the key the account puts on the net N. The
first term is the fee term this lane was asked for. The second is the key error on the net. The brief's
(s_C − s_R) × R, with s_C the account's key, matches the fee term only when s_K = s_U. Here that fails. At the
account's keys the brief's form gives tuition +$4.26bn and hospitals −$1.97bn, together +$2.29bn. On higher
education s_K (0.139) is far above s_U (0.116), so most of that +$4.26bn is the key error with its sign reversed.
[CALCULATION: fee_lines.py]

Terms at the case's ends, $bn, on the account's union (39.71M); every term enters at response 1 (gated):

| Term | Low end (spec 48) | High end (spec 11) | Route |
|---|---:|---:|---|
| Tuition fee term, (0.1159 − 0.0981) × $103.9bn | +1.84 | +1.84 | engine |
| Higher education keyed by use (0.1159), not item P (0.1392), on $234.0bn | −5.45 | −5.45 | engine |
| BEA's K-12 weight, 0.775 of the line, not the case's 0.795 | −0.57 | −0.73 | post-engine |
| College capital at use, not the line's blend | −0.90 | −1.51 | post-engine |
| K-12 capital at the K-12 key, not the line's blend | +0.27* | +0.51 | post-engine |
| **Education** | **−4.81** | **−5.34** | |
| Hospital fee term, insured payers | +0.95 | +0.95 | engine |
| Hospitals' insured net keyed by use, not the health key | −0.31* | −0.31* | engine |
| **Hospitals** | **+0.64** | **+0.64** | |
| **Pell at the group's share (0.169), not cash income (0.042–0.046)** | **+3.87** | **+3.97** | engine |
| Transit loss by rides (ratio 0.746), not population | −1.98 | −1.98 | engine |
| Transit capital by rides | −0.30 | −0.45 | post-engine |
| **Transit** | **−2.28** | **−2.43** | |
| **All terms** | **−2.58** | **−3.16** | |
| Fee terms alone (tuition and hospitals) | +2.79 | +2.79 | engine |
| Case: v5 → with all terms | 390.29 → 387.71* | 461.24 → 458.08* | |
| Cash set: v5 → with all terms | 307.38 → 304.80 | 383.41 → 380.25 | |
| Case with the fee terms alone | 393.08 | 464.03 | |

\* Controlled rounding so that printed parts add; exact values are in `derived/case_oct05.json`: K-12 capital
+0.2757, insured net −0.3037, the case's new ends 387.7166 and 458.0856. The ends stay at specifications 48 and 11.

Signs that hold across the arms:

- Positive fee term on tuition: 80 of 81 arms on NIPA's concept.
- Negative higher-education key term: every arm. The highest measured use share, 0.120, is below the account's 0.139.
- Positive Pell term: every arm.

The total's sign rests on the size of the higher-education key term against the Pell term. Taking several inputs
at their extreme ends together could reverse it.

| Input varied | Term | Central | Range |
|---|---|---:|---|
| Tuition on NIPA's concept (net tuition plus Pell): use cost (education and related; all less hospital, auxiliary and aid; all less hospital and aid), graduate cost weight 1–3, residency θ 0–1, Pell intensity (none, mid, NPSAS) | fee term | +1.84 | −0.15 to +3.37 |
| the same, gross tuition (all discounts added back) | fee term | | +1.76 to +4.69 |
| the same | higher-education key term | −5.45 | −7.54 to −4.42 |
| the same, NIPA's concept | fee + key | −3.61 | −7.69 to −1.05 |
| Hospitals: MEPS shares ±1 SE by payer, Medicare and private cost shares, payment-to-cost ratios, gross cost G, frame | fee term | +0.95 | −1.10 to +4.18 |
| the same | fee + key | +0.64 | −1.08 to +2.67 |
| Pell: within-unit intensity, public share 0.58–0.75, private-to-public share ratio 0.5–1 | Pell key | +3.87 / +3.97 | +2.59 to +5.09 |
| Education weights: the S&L mix; federal education consumption all non-K-12 or all K-12 | K-12 weight | −0.57 / −0.73 | −0.74 / −0.94 to −0.46 / −0.59 |
| Transit loss following bus commuters (ratio 1.031) or rail commuters (0.512) | transit, operating | −1.98 | +0.24 to −3.81 |
| The lineage's 3.04M added people at the union's per-member terms (×1.0765) | all terms | −2.58 / −3.16 | −2.77 / −3.40 |
| Other sales, not measured | fee term | 0 | ±1.75 for each 0.01 gap between use and fee shares |

## Construction

**Which lines carry fees.** NIPA T3.10.5 for 2024 puts S&L sales to other sectors at $683.760bn. That splits into
tuition and related educational charges $103.911bn (line 58), health and hospital charges $364.091bn (line 59) and
other sales $215.758bn (line 60). Note 5 says other sales include federal purchases of R&D from S&L general
government. Federal sales are $12.043bn, below the $20bn threshold. [SOURCE: BEA Section 3 workbook,
`sources/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx`, sha 69b5c7ae…]

Government enterprises sit outside consumption. The account holds their current surplus as the enterprise_surplus
receipt at a population key, so fares, tolls and utility bills are netted inside it. Public transit's loss is
$66.690bn (T3.8 line 14). The Census FY2022 composition of charges is in `derived/other_sales.csv`. [SOURCE: Census
2022 Table 1, `ledger_residual_agg_2026_09_16/_cache/22slsstab1.xlsx`, sha 4dd123c5…]

**What the account does with education.** education_services is all-government education consumption, $1,221.159bn
(T3.17 line 9). The case implements its key as the union's row-4 amount T0·f plus the school edit at s and the
college edit at 1 − s, which equals n·hf·f·[W·(s·k + 1 − s)·Ts/Ns + (1 − W)·Tp/Np]:

- s is the school fraction.
- W = 0.795 is row 6's mean of 0.77 and 0.82.
- f = 0.99220 is the line's row-4 factor.
- k = 1.0342 is the school price.
- hf = 0.990053.

fee_lines.py gates this: it reproduces the case's row-6 college edit to 1e-9 from W, hf, f and the components.

Tp/Np = 0.14170 is the ledger's item P. `ledger_absolute_2026_09_17/absolute_ledger.py:70` defines P as "non-school
state and local capital outlay", and lines 633–651 charge it per capita by state of residence.
`full_account_spending_2026_09_20/builder.py:250` builds the "postsecondary" key from P, and `builder.py:127` keys
education_benefits by that key. So 1 − W of the line, and the higher education within it, sits at
P_eff = hf·f·P = 0.13919, a state-weighted head count. [DATA: `school_enrollment_2026_09_20/derived/updated_account_components.csv`]

**The group's share of public college use and fees.** higher_ed.py works on IPEDS FY2023 finance (GASB F1A) for
1,888 finance units. Those units hold 98.25% of public FTE in the 50 states and DC; PSU, Pitt, Temple and Delaware
report under FASB and fall outside. It combines them with fall 2023 enrollment by race and the ACS 2024 share of
Hispanic public college students who are of Mexican origin, by state and level:

- Use: s_U is the group's share of education-and-related cost at FTE shares, with graduate FTE weighted 2.
- Fees: s_R is its share of net tuition plus Pell. Undergraduates are adjusted for residency at θ = 0.5 of the
  unit's out-of-state rate, and graduates are priced at the unit's graduate tuition ratio.
- Pell goes to the group at the unit's Mexican undergraduate share times the midpoint of 1 and the NPSAS:20
  Hispanic Pell intensity of 1.26.

The results are s_U = 0.11507 and s_R = 0.09744 (ρ 0.847). The FTE share is 0.135. Put on the union by
φ = 39.71M / 39.43M (the ACS group) = 1.00718, they become 0.11590 and 0.09814. [DATA: IPEDS files staged under
`sources/immigration-fiscal/data/external/stage3/nces/ipeds_2023/` (ACQUIRED.md); ACS 2024 PUMS csv_pus.zip,
sha afdc6d90…; SOURCE: NPSAS:20 First Look, NCES 2023-466, tables A-5 and A-6]

NIPA's concept is net tuition plus Pell. NIPA records Pell as a federal social benefit to persons (T3.12 line 26,
note 7: "aid to students"), and persons pay it on as tuition. IPEDS FY2023 net tuition plus Pell is $98.9bn,
against NIPA's 2024 $103.9bn. So the fee term pairs with the Pell key below. Crediting the group with
Pell-financed tuition while keying Pell by cash income would understate its cost. [INFERENCE]

The higher-education dollars on the line are $234.0bn. That is S&L higher-education consumption, $229.963bn (T3.16
line 108, with no education benefits in it), plus a share of federal non-K-12 consumption. The K-12 weight 0.775 is
government-wide K-12, $946.196bn (T3.16 line 31), over the line. That is the audit's own 0.77
(`dataset_integrity_2026_09_23/spending.md` #5). Its 0.82 takes the $64.5bn of education benefits out of a
consumption line that already excludes them. [CALCULATION: fee_lines.py]

**The capital keys by part.** The case keys the return on college and on K-12 structures by the whole line's blend:
(education amount + college or school edit) over the line's total.

- College stock: the union's key is 0.1545 (shared) / 0.1588 (personal). The use key is κ·U + (1 − κ)·P_eff = 0.1168,
  with κ = 0.961, higher education's share of non-K-12 education investment (T3.15.5 less T3.16).
- K-12 stock: the union's key is 0.1588 / 0.1633, against its own K-12 key at the school price, 0.1639 / 0.1695.

Both terms are stock × rate × the consumer's response × the key change. The gates check that each component's key
splits into the union's part and the lineage's edits to 1e-12.

**Hospitals.** health.py reads MEPS 2024 (HC-256, the account's pinned file) for the group's share of hospital
facility payments by payer, with design-based standard errors:

| Payer | Group share | SE |
|---|---:|---:|
| Medicare | 0.033 | 0.012 |
| Medicaid | 0.202 | 0.062 |
| Private and other | 0.050 | 0.008 |

It puts these on the union's frame by 0.11676 / 0.12492, the union's population share over MEPS's. It combines them
with government hospitals' payer mix and payment-to-cost ratios:

- Medicaid 20.1% of services at 95.4% of cost [SOURCE: Milliman, Nov 2024, HCRIS 2021].
- Medicare at 86.8% and private payers at 144.8% of cost [SOURCE: AHA Chartbook 2018, Table 4.4, 2016].
- Medicare's 0.35 and private payers' 0.36 cost shares [ASSUMPTION].

On the insured payers the group's use share is 0.0722 and its fee share 0.0690. The fee term is +$0.95bn; with the
union's health key 0.0625, the residual is +$0.64bn. The uninsured term is out: the case already charges
uncompensated care by use (decision 2026-09-23). [CALCULATION: fee_lines.py, derived/health_terms.csv]

**Pell and transit.**

- Pell: grants were $31.264bn in FY2023 [SOURCE: CRS IF12780 Table 2]. The group's share is 0.169: 0.183 of public
  institutions' Pell, times φ, with public institutions at 0.68 of Pell and the group's private-sector share at
  0.75 of its public one [ASSUMPTION for both]. The case keys Pell inside other_federal_benefits by CPS cash income,
  at 0.042–0.046 for the union.
- Transit: the group is 8.65% of transit commuters against 11.59% of residents (ACS 2024, JWTRNS 02–06), a ratio of
  0.746 applied to the union's enterprise-surplus share, 0.11718. Commutes stand in for rides [ASSUMPTION].

**Engine edit.** case.cjs adds six synthetic spending lines, fee_tuition, fee_health, key_higher_ed, key_health,
key_pell and key_transit. Each has national 0, key k and an edit by allocation, at response 1 at both readings. It
evaluates them through `main_case_candidate_v4_2026_09_29/consumer.cjs` on `main_case_2026_10_05/derived/corrections.json`
and `corrections_cash.json`. The K-12 weight term (A + B·s at the education line's response) and the three capital
terms are post-engine, as the case's capital return is.

Gates, both sets:

- the consumer reproduces summary.json's bands at specifications 48 and 11, and those are the lowest and highest
  costs;
- fee_lines.py's union reads match the engine's on the payload's pre-lineage edits;
- every parent line responds at 1 at all 64 specifications;
- the lines at zero reproduce every specification exactly;
- each line, the fee lines together and all the lines change every specification by the sum of their amounts
  (1e-9).

Because of these gates, the first-order sum is exact here.

## Limits

- **IPEDS shares are institution-level.** Within an institution, only residency and Pell vary by group. IPEDS
  reports Hispanic students, not Mexican-origin ones; the ACS state ratio converts them. The ACS cannot see union
  members who do not report Mexican origin, so φ assumes they use and pay alike.
- **Survey years do not line up.** IPEDS FY2023 shares are applied to NIPA 2024 totals, and Pell is the AY2023–24
  award, $31.264bn. Calendar 2024 Pell may differ [UNVERIFIED].
- **The hospital term is the noisiest.** The Medicaid share's SE is 0.062. Government hospitals' Medicare and
  private cost shares are assumed. G, the gross cost, comes from Census hospital spending scaled to NIPA ($295.6bn),
  below NIPA's own charges ($364.1bn). Census books state Medicaid payments to local hospitals as intergovernmental
  revenue [INFERENCE]. Sizing G from the charges instead gives +$0.78bn.
- **Other sales are not measured** ($215.8bn, of which about $41bn is federal R&D purchases from public
  universities). Parking, parks, solid waste, school lunches and college dormitories and dining are paid per use.
- **The transit ratio follows commuters.** Since bus riders (ratio 1.03) and rail riders (0.51) differ, the split
  of the loss by mode decides the term, from +$0.24bn to −$3.81bn.
- **Only the union is priced.** The lineage's 3.04M added people carry no term; at the union's per-member terms the
  total is −$2.77 / −3.40bn.
- **State and other federal grants are left out of the fee pool.** These are $13.6bn at public institutions in FY2023
  (IPEDS F1E02–F1E04), and their benefit keys are left as they are. Counting them in both places moves the total by
  −$0.2bn to 0 [INFERENCE, at a Pell-like 0.17 group share of those grants: the fee term falls about $0.9bn, and the
  state-grant and SEOG keys rise $0.75–0.9bn].

## Beside the lane (found, not priced)

- **S&L education benefits ($64.479bn, T3.12 line 40) are keyed by the same item P.** That is the account's
  education_benefits at "postsecondary". The Census definition of "other education" covers tuition grants,
  fellowships, aid to private schools and special programs. Two NPSAS:20 figures suggest the group's share of state
  grants is above P: Hispanic undergraduates receive state grants at 1.34× the average per student (table A-3: 29.4%
  against 22.5%; table A-4: $3,600 against $3,500). Its share of institutional aid and aid to private schools is
  likely below. The composition is not measured; each 0.01 of key error on the line is $0.64bn.
- **The builder's "postsecondary" label is wrong** (builder.py:250); the key is item P. Fixing the label is a
  one-line change in another lane.
- **MEPS 2024 puts the group at 35.3% of full-year uninsured persons** (SE 3.9pp; 33.0% on the union's frame). The
  uncompensated-care lane keys by 25.7% of uninsured person-years. The two measures differ in concept, so this is a
  flag, not a finding.
- **Airports, water and sewer capital are keyed by population** in the enterprise option. The group's use of
  flights is likely below that share, and of water and sewer near it [INFERENCE]. Not measured.

## Reproduce

From the repository root (no network; external inputs pinned by sha256 in each script):

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/acs_college.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/acs_transit.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/higher_ed.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/health.py
    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/user_fee_allocation_2026_10_07/fee_lines.py
    node infra/immigration-fiscal/user_fee_allocation_2026_10_07/case.cjs

Rerun check:

    uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/user_fee_allocation_2026_10_07 \
      "uv run --no-project python3 {lane}/acs_college.py" "uv run --no-project python3 {lane}/acs_transit.py" \
      "uv run --no-project python3 {lane}/higher_ed.py" "uv run --no-project python3 {lane}/health.py" \
      "uv run --no-project python3 {lane}/fee_lines.py" "node {lane}/case.cjs"

Outputs, all in `derived/`:

| File | Content |
|---|---|
| acs_public_college_by_state.csv, acs_population.json | ACS shares |
| acs_transit.json | transit commuter shares |
| higher_ed_shares.csv, higher_ed.json | IPEDS shares, every arm |
| health_meps_shares.csv, health.json | MEPS shares |
| fee_lines.csv | the lines with R ≥ $20bn |
| higher_ed_terms.csv, health_terms.csv | terms by arm |
| other_sales.csv | the composition of NIPA's other sales |
| fee_lines.json | the amounts the engine edit takes |
| case_oct05.csv, case_oct05.json | per specification, and the ends with arms |

Peak memory: higher_ed.py 424 MB, every other script under 215 MB; the six run in about 40 s. higher_ed.py prints
pandas PerformanceWarnings, which are harmless.

## Log (times from `date`)

- 2026-10-07 11:02 JST — lane opened; stub written.
- 2026-10-07 11:18 JST — traced the lines. NIPA T3.10.5 (pinned Section3All, sha 69b5c7ae…) 2024: S&L sales to
  other sectors $683.760bn = tuition and related educational charges $103.911bn + health and hospital charges
  $364.091bn + other sales $215.758bn (footnote 5: includes federal R&D purchases from S&L general government);
  federal sales $12.043bn. T3.17 S&L health (net) $126.839bn = gross $491.383bn less sales $364.544bn.
  Government enterprises (T3.8) are outside consumption; the account holds their surplus as receipts.
- Education key: the v5 college part is row 6's blend w·Ts/Ns + (1−w)·Tp/Np at k = 1 (main_case_2026_09_24/package.cjs
  educationShifts; school_cost_where_enrolled_2026_09_24/lines.py row6). Tp/Np is the ledger's item P, which
  ledger_absolute_2026_09_17/absolute_ledger.py:70 and :633-651 define as "non-school state and local capital outlay",
  charged per capita by state of residence — not postsecondary use. full_account_spending_2026_09_20/builder.py:319
  names it 'postsecondary'. So public higher education's net cost is keyed by a state-weighted head count, and
  education_benefits (T3.12 l40, $64.5bn) by the same key. [DATA: updated_account_components.csv, P national $63.51bn,
  union $9.00bn, share 0.1417]
- 2026-10-07 11:36 JST — higher education measured (higher_ed.py on IPEDS FY2023 finance, fall 2023 race,
  ACS 2024 Mexican share of Hispanic public college students by state): the group's share of public colleges'
  education-and-related cost s_U = 0.1151, of tuition plus Pell s_R = 0.0974 (rho 0.847); its FTE share is 0.135
  and the account's P key 0.1417 (CPS frame). Health (health.py, MEPS 2024 HISPNCAT 1): after the case's
  uncompensated-care charge, the insured payer-mix residual is +0.71bn (range −0.80 to +2.54). Transit
  (acs_transit.py): the group is 8.65% of transit commuters against 11.59% of residents (ratio 0.746).
- 2026-10-07 12:04 JST — fee_lines.py and case.cjs built; first engine run, 30 gates pass. The case's implemented
  key on the college part is P_eff = hf·f·P = 0.13919, not the CPS-frame 0.1417: the row-6 re-blend carries the
  line's row-4 factor f = 0.99220 (gated by reproducing row 6's college edit). The capital return on K-12 and college
  structures is keyed by the whole line's blend, so both stocks get a by-part key term.
- 2026-10-07 12:04 JST — corrections to the entries above. The 11:18 entry's builder.py:319 is wrong:
  builder.py:250 builds the "postsecondary" key from item P, and builder.py:127 keys education_benefits by it. The
  11:36 health residual (+0.71bn) used the v5 health key, including the lineage, with raw MEPS shares. On the union's
  frame and key it is +0.64bn (range −1.08 to +2.67); health.py now measures only, and fee_lines.py prices.
- 2026-10-07 12:10 JST — the central K-12 weight moved from the S&L mix (0.777) to government-wide K-12 (T3.16
  line 31, 0.775), the audit's own 0.77; the S&L mix is now an arm. Totals moved from −2.49 / −3.05 to −2.58 / −3.16.
- 2026-10-07 12:13 JST — RESULT written.
- 2026-10-07 12:16 JST — `scripts/rerun_lane.py` over the six commands under Reproduce: IDENTICAL 21/21, exit 0.
- 2026-10-07 12:23 JST — parent review: transit terms overlap v3 item 8 (deficit-weighted riders key 1.019, beside in v4); the next case takes the other terms, −0.296 / −0.726bn on v5.
