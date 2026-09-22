# Indian-origin residents: the treasury, co-ethnic coordination, giving and the vote

## Audit correction — September 19, 2026

**The favorable working-age fiscal contrast and civic participation point estimates remain descriptive findings.** Compare fiscal figures with Mexico only on the same ledger, ages and allocation. CPS civic standard errors use weight/model approximations rather than the full survey design. Comparing opt-in IAAS vote estimates with separate GSS white-graduate groups is a benchmark sensitivity, not an identified education decomposition or an exact adjusted 6–14-point residual. The small second-generation adult cell does not project the still-young descendant population. The existing one-firm limit on adjudicated favoritism remains essential. [SOURCE: linked lane methods and fiscal/mechanisms audit evidence]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


Model self-report: claude-fable-5-1 (parent synthesis); lanes ran on claude-opus-5. September 18, 2026.
Lanes: `infra/immigration-fiscal/indian_ledger_2026_09_18/`, `indian_civic_cps_2026_09_18/`,
`indian_coordination_2026_09_18/`, `indian_politics_2026_09_18/`. Each `RESULT.md` carries the
full claim tables, sources fetched and skipped, and a dated parent-review block.

**Verdict:** On the repo's ledger Indian-origin residents are the most fiscally positive group
measured: India-born adults 25–64 run **+$24,163** per adult-year against **+$13,431** for the
white reference, a gap of **+$10,732 (se 1,351)**, and the second generation runs wider. The
clustering that invites the coordination question is large and administrative: 71.0% of FY2024
H-1B approvals, 88% spousal endogamy in the first generation. Favouritism is established at one
firm by one jury and not beyond it; the tests that separate favouritism from information point
both ways. Private giving is low at every income level in the only survey that compares it, and
at equal education India-born citizens vote 10 points less often than whites. The Democratic
lean is 28.8 points over US-born whites raw and 6–14 points against education-matched whites,
and it has been eroding since 2020 through the US-born.

Instrument caveat: LLM-conducted on a charged topic (`notes/llm-bias-caveat.md`). The
coordination lane's first verdict erred in the benign direction and the parent review corrected
it (§2); treat that as the expected sign of the instrument's error here.

## 1. The treasury

CPS ASEC 2025, adults 25–64, upstream `equal_all_members` allocation, person weights, after
employer payroll, sales, property, K-12 and MEPS public-paid health. [SOURCE:
`indian_ledger_2026_09_18/derived/india_ledger_result.txt`; parent re-run byte-identical; gate
reproduces the upstream white-reference figures to four decimals]

| Group | n | Net per adult-year | Gap vs white reference |
|---|---|---|---|
| India-born | 1,232 | +24,163 | +10,732 (se 1,351) |
| Second generation (India-born parent) | 209 | +34,003 | +20,572 (se 3,872) |
| White reference (third-plus generation) | 36,287 | +13,431 | — |
| Mexico-born | — | −10,794 (se 405) | — |

Arms that could have reversed the sign and did not: age-standardised +10,955; household
weighted +10,422; top 1 percent excluded +10,488; recent noncitizens (the temporary-visa proxy,
30% of India-born adults) excluded **+13,397**, because that slice is the lowest-net part of the
group at +17,956. Composition of the gap before extensions: modelled taxes +6,197, cash
transfers −1,972. Per-adult allocation widens the gap to +15,460 (se 1,695). [CALCULATION]

ACS 2023 profile [SOURCE: `derived/acs_profile_2023_result.txt`]: BA or higher 84.4%, graduate
degree 52.4%, median household income $165,193, computer and mathematical occupations 31.1%.
India-origin workers are 1.56% of the employed, 10.4% of computer/math, 8.4% of physicians and
10.7% of the self-employed in traveller accommodation; their overall self-employment rate is
below the foreign-born average (7.3% vs 13.2%). DHS Yearbook: 55.9% of FY2024 H-1B *admissions*
(a different object from the 71.0% of *approvals* in §2).

Limits. The period ledger is not a lifetime value; the group is young and positively selected
by the visa, so the figure describes this admission channel, not "Indians". CPS 2025 weights
the India-born to 4.28M against 2.94M in ACS 2023; the gaps are within-file, the CPS level
should not be quoted. [FRAMING-SENSITIVE: the absolute sign is a convention; the gap is not.]

## 2. Co-ethnic coordination

**Steel-man.** A group admitted through a computing visa will be concentrated in computing;
referral hiring reproduces incumbent composition for every group; co-ethnic trust substitutes
for costly contracts and raises trade with the origin country; niche entrepreneurship transmits
know-how. On this account clustering needs no preference, and co-ethnic matches should perform
as well as others.

**What is measured.** 71.0% of FY2024 H-1B approvals were India-born (283,397 of 399,395), and
the India-plus-China share is higher for continuing (89%) than initial (71%) approvals [SOURCE:
USCIS, Characteristics of H-1B Specialty Occupation Workers FY2024]. Gujarati-speaking Indians
are 84× more concentrated in motel management than other immigrant groups [SOURCE:
Kerr–Mandorff, HBS WP 16-042]; the ownership share in the academic source is one-third, not the
majority that trade-association figures claim. Spousal endogamy is 88.4% among the India-born
and 52.4% among the US-born of Indian ancestry (§1 ACS profile): the one direct measure of
in-group closure in our own data roughly halves in a generation.

**The adjudicated case.** *Palmer v. Cognizant* (C.D. Cal. No. CV 17-6848-DMG), findings of 5
December 2025, cached at `indian_coordination_2026_09_18/sources/PalmerCognizant120525.pdf`:
non-South-Asian and non-Indian employees were 8.4× more likely to be terminated from the bench
(75.12 SD); about 99% of visa-holding employees were of Indian national origin and about 88% of
the US workforce South Asian; bench termination 30% for non-visa staff against 3% for visa
staff; Cognizant's own deck directs replacing staff higher on the "value chain" with visa
holders "with a lower grade and experience". The order decides the disparate-impact claim, so
it treats the visa policies as facially neutral. The same order records that the Phase I jury
found a pattern or practice of **intentional** discrimination by race and national origin,
"unexplainable on grounds other than race or national origin", and the court found **no
business necessity**. The findings do not identify the decision-makers or their ethnicity. So
the record shows the instrument (visa policy), a jury finding of discriminatory intent, and a
rejection of the cost defence; it neither shows nor rules out preference by co-ethnic managers.
No damages have been awarded and the merits are untested on appeal. [SOURCE for the findings;
INFERENCE for the last sentence but one]

**The contrary case.** *Koehler v. Infosys* (7th Cir. No. 25-2272, 13 July 2026) affirmed
summary judgment for Infosys on the same theory because the plaintiffs' expert inferred
ethnicity from surnames without expertise or a validated method. That is a ruling on
measurement, not a finding that Infosys did not discriminate. [SOURCE: slip opinion, cached]

**Favouritism or information.** Hegde–Tumlinson, on nearly all US venture deals 1991–2010:
co-ethnic investor–founder pairs (Indian pairs included) exit successfully more often, +2.5 to
+3.1 points, larger under IV: information. Åslund–Hensvik–Skans, Sweden: immigrant managers
hire immigrants at 43% against 6%, which the authors attribute to profit-maximising sorting.
Against these, Giuliano–Levine–Leonard find own-race hiring by US retail managers that they
cannot explain by networks or efficiency and read as taste. Nobody has run either design on
Indian managers in US tech. [SOURCE: papers as cited in the lane claim table; contested evidence]

**Cost to natives.** The identified cost attaches to the visa: Doran–Gelber–Isen's lottery
design has one additional H-1B crowding out about 1.5 other workers at the firm with no patent
gain; Bound–Braga–Golden–Khanna's calibration has native computer-science wages 2.8–3.8% and
employment 7.0–13.6% higher under 1994-level foreign hiring, with total output lower.

**Caste.** *CRD v. Cisco* is still open; the operative complaint pleads religion, ancestry,
national origin and race, not caste as a category; the individual defendants were dismissed in
2023. The 5% annual self-reported incidence comes from Carnegie's IAAS, an opt-in YouGov panel;
the higher Equality Labs figures come from a snowball sample. Banerjee et al. find no caste
penalty in Delhi software callbacks.

**Open.** DOL LCA wage levels at outsourcers against product firms, the direct test of the
wage-arbitrage reading, were not reached.

## 3. Giving, remittances and civic life

CPS Volunteering and Civic Life supplements 2019, 2021, 2023, adults 18+ [SOURCE:
`indian_civic_cps_2026_09_18/derived/summary.txt`; parent re-run of `verify.sh` 12/12
byte-identical]. The lane's volunteering level sits 2–3 points under the published national
rate in every year (group membership matches exactly), so read group differences, not levels.

| | India-born | US-born NH white | Indian 2nd gen |
|---|---|---|---|
| Donated to charity | 51.1 (1.6) | 57.8 (0.2) | 55.7 (4.0) |
| Donated, BA or higher only | 53.4 (1.7) | 73.3 (0.3) | 64.0 (4.3) |
| Volunteered for an organisation | 21.5 (1.3) | 29.8 (0.2) | 33.7 (3.8) |
| Volunteered, BA or higher only | 22.7 (1.4) | 42.6 (0.3) | 32.6 (4.2) |
| Political donation | 6.1 (0.8) | 10.5 (0.1) | 10.3 (2.5) |

Also: group membership 16.2 vs 32.0, contacted an official 4.6 vs 12.5, informal neighbourhood
action 31.0 vs 22.8. The raw rates look near native; at equal education the India-born give
and volunteer about 20 points less often, and the second generation closes roughly half of
that. The supplement has no donation amounts since the 2017 redesign.

Amounts exist only in the Indiaspora–Dalberg report (n=280 donor households, described by its
authors as not representative, funded by the bodies it concerns): below $100k Indian American
donors give 2.5% of income against a US average of 9.5%; at $100–200k, 2.9% against 6.4%
[SOURCE: `indian_politics_2026_09_18/raw/ipa_giving_2025.pdf`, Figure 4, parsed directly]. The
"4–5% of income" headline is donors only and the "$1bn gap" is a model output. Evidence level:
weak, single non-probability source, direction consistent with the CPS participation rates.

Remittances: India's inward flow was $118.7bn in FY2023-24, US share 27.7% [SOURCE: RBI
remittance survey, sixth round]; the implied $33bn from the US is [INFERENCE] because RBI
computes the share on two components, not the balance-of-payments total. "Indian Americans pay
5–6% of US taxes" traces to an advocacy self-report and is not cited here.

## 4. The vote

**Turnout** [SOURCE: CPS November supplements 2016–2024; gate: 2020 citizen turnout 66.77%
against 66.8% in P20-585]. Citizens 18+, pooled: India-born 65.1% (n=1,748), US-born NH white
64.7%, China-born 42.5%, Mexico-born 42.9%, Indian second generation 57.0% (n=833). Adjusted
for age, sex, education, income and metro, the India-born coefficient goes from 0.0 (±1.2) to
**−10.3 (±1.2)**; among BA holders 68.0 against 77.6. Parity is presidential-year only (+7.5 in
2020, +5.6 in 2024, −4.2 in 2018, −11.0 in 2022). Only 45.3% of India-born adults are citizens;
they naturalise late (7.6% at 5–9 years against 24.7% for other foreign-born, the green-card
backlog) and almost completely (96.7% at 30+ years).

**Direction** [SOURCE: Carnegie IAAS 2020, 2024, 2026; YouGov opt-in panel; 2026 N=1,000,
±3.6, fielded 25 Nov 2025 – 6 Jan 2026, with a revised frame adding mixed-race respondents;
page fetched independently by the parent]. Presidential preference among citizens: 68/22
(2020), 62/30 (2024), 57/25 (2026 re-ask). Party ID: Democrat 52 → 46, Republican 15 → 19,
independent 23 → 29. In 2024 Trump support was 39% among the US-born and 24% among the
naturalised, from 22% each in 2020; the movement is concentrated in US-born men under 40.
Trend direction is supported; magnitudes mix real change with the frame change.

**Rich but votes left, tested against composition** [CALCULATION: GSS 2021–24,
`indian_politics_2026_09_18/derived/matched_white_gss.csv`, re-run byte-identical]. US-born NH
white two-party Biden share: all 46.8%; BA or higher 61.6%; postgraduate 69.7% (n=553);
postgraduate, top income quintile, top-100 metro 64.7% (se 7.2, n=86). Indian American: 75.6%.
With 84% BA and 52% graduate degrees, the education-matched white benchmark lies between 62%
and 70%, so composition explains half to four-fifths of the 28.8-point gap and 6–14 points
remain. Among white graduates higher income goes with a more Democratic vote, so high income
is no anomaly within this class. Limits: probability GSS against opt-in IAAS, GSS income
top-coded below the Asian Indian median.

**What they vote for** [SOURCE: IAAS 2026]. Top issues: prices 21%, jobs 17%, health care 13%,
immigration 11%, taxes and spending 5%. Opposition to each enforcement item 61–74%, including
66% against the $100k H-1B fee. Non-Democrats' reasons for withholding support: extreme left
19%, illegal immigration 17%, economic policy 17%, crime 16%, identity politics 16%; "not good
for India" 6%. On India: Modi approval 47/34 in 2024; BJP 28%, Congress 20%, don't know 51%.
[FRAMING-SENSITIVE: whether these positions are good policy is not decided here.]

**Organised influence.** Six Indian-origin House members, all Democrats [SOURCE: House Clerk
roster]; individual contributions $46.6m Democratic against $16.3m Republican in 2020 [SOURCE:
Pal et al., surname classifier, F1 81.7%]; the four main advocacy organisations report about
$7.4m combined revenue (FY2023 990s); ethnic PACs raised $18k and $219k in the 2024 cycle.
Senate and governors not verified; FARA filings for the Indian government not reached.

## What would change this

- LCA wage data showing outsourcers pay at product-firm levels would remove the arbitrage
  reading of §2; a Giuliano-style manager design on US tech showing own-group hiring that
  underperforms would establish favouritism beyond one firm.
- A probability-sample vote measure by national origin (none exists; CES carries no Asian
  origin detail) could move the §4 residual in either direction.
- A lifetime account with return migration and ageing would shrink the §1 gap; it cannot
  plausibly reverse it given the recent-noncitizen arm.

## Revisions

- 2026-09-18 — created. Ladder 150–153.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).

## Revisions — September 21, 2026

Third-plus Indian (US-born, both parents US-born, Asian Indian race) is now on the same 2025 ledger: n=49 adults 25–64, age-standardised gap **+$11,806 (se 8,150)** vs 3rd+ NH whites, which does not reject parity. G2 age-standardised **+$23,692 (se 5,482)** is unchanged. The G3 cell is an identified-race remainder, not observed grandparents. [DATA: `infra/immigration-fiscal/indian_generation_2026_09_21/RESULT.md`]
