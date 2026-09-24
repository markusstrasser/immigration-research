claude-opus-5-5[1m]

# Worklog — affirmative action cost lane (2026-09-24)

Checkpoint file for this lane. `RESULT.md` is the deliverable; this file records sources
fetched, numbers verified (with page), and gaps, appended as the work proceeds.

## Scope

Annual career cost to non-Hispanic white natives of race/ethnicity preferences, 2024 and
pre-2023, per channel (admissions, employment, contracting, other), with Hispanic and
Mexican-origin shares. Brief: `BRIEF.md`.

## Findings (appended as verified)

### Round 1 (admissions, employment, contracting sources), 2026-09-24 09:10

Admissions
- AKR, "What the SFFA cases reveal" (Duke version 17 Mar 2023, `_cache/akr_sffa_duke.pdf`),
  Table 11 p. 62: removing racial preferences, fixed class size. Harvard classes 2014-19:
  white 2,704 -> 3,195; Black 1,163 -> 324; Hispanic 1,188 -> 581; Asian 2,013 -> 2,812.
  UNC out-of-state 2016-21: white 6,954 -> 8,878; Black 1,605 -> 208; Hispanic 1,821 -> 738;
  Asian 2,698 -> 3,260. UNC in-state: white 18,865 -> 19,889; Black 2,374 -> 1,532;
  Hispanic 1,470 -> 1,212; Asian 3,223 -> 3,370. The prose on p. 34 gives different UNC
  in-state and out-of-state counts (older table version); the table is internally consistent.
  Table 10 p. 61: share of URM admits still admitted without preferences: Harvard Black 30.0,
  Hispanic 46.1; UNC OOS 8.7 / 29.2; UNC in-state 57.8 / 75.8.
- Espenshade & Chung 2005, SSQ 86(2) Table 2 p. 299, 1997 cohort, elite privates, race-blind
  simulation: white 5,134 -> 5,256; Black 899 -> 326; Hispanic 792 -> 381; Asian 2,369 -> 3,141.
  p. 298: white acceptance rate 23.8 -> 24.3; "Nearly four out of every five places ... filled by
  Asians". p. 302 (secondary): Long 2004b URM share of accepted students 16.1 -> 15.5 at all
  four-year, 10.6 -> 7.8 at top-decile schools; Wightman 1997 law school 3,435 -> 687.
- Hinrichs 2012, REStat 94(3) Table 5 p. 717 (minus signs lost in pdftotext; text p. 717 gives
  signs): public US News top 50: Black -1.74, Hispanic -2.03, Native -0.47, white +2.93,
  Asian +1.43 pp (bases 5.79/7.38/0.51, Table 4). All top-two-tier (col 3): Black -1.00,
  Hispanic -1.08, white +1.83, Asian +0.55; public top-two-tier (col 4): -1.18/-1.22/+1.78/+0.92.
- Bleemer QJE 2022 (advance-access pagination): p. 4 URM wages -5% ages 24-34, driven by
  Hispanics; Fig. VIII p. 36 Berkeley RD for on-the-margin non-URM: admission +36.6 (3.6) pp,
  enrollment +12.7 (3.0), CFSTY VA -0.17 (0.78), log wages early 30s -0.10 (0.11); p. 37
  "Prop 209 provided minimal benefits to non-URM students".
- Chetty-Deming-Friedman w31492 (rev. Aug 2025): p. 3-4 Ivy-Plus vs flagship +$101k mean
  earnings at 33 on $143k counterfactual; p. 30 no significant effect on mean income rank;
  p. 37 mean proportional effect across quantiles 23%.
- Dale & Krueger w17159 p. 24-25: basic model +100 school-SAT = ~6% earnings; selection-adjusted
  ~0; positive for Black/Hispanic and low-parent-education students. p. 3 cites Hoekstra 2009:
  flagship attendance +20% earnings for white men, none for white women. Table 1 p. 29: C&B mean 2007
  earnings $183,411 (1976 cohort), $139,698 (1989 cohort).
- NCES Digest 2024 Table 306.10 (resident students): Hispanic share 3.6 (1976), 4.0 (1980),
  5.8 (1990), 9.9 (2000), 15.8 (2013), 20.3 (2019), 22.2 (2023); Black 9.6, 9.4, 9.3, 11.7,
  14.7, 13.2, 13.4.
- IPEDS fall 2023 EF/ADM/HD downloaded to `_cache/ipeds/` (EF2024A not yet released: 404).

Employment
- Miller 2017 AEJ Applied 9(3): p. 153 contractors employ ~1/4 of the workforce (OFCCP 2013);
  Black share +0.8 pp five years after first regulation, +0.8 pp more in five years after
  deregulation; fn 1 Hispanic results "qualitatively similar" (not reported). p. 157 ~1% of
  covered establishments reviewed per year; p. 158 43 debarments to 2001.
- Kurtulus 2016 JPAM 35(1) Table 4 p. 53, 1973-2003: Fed coefficient white male +0.090 (0.037),
  white female -0.122 (0.035), Hispanic male -0.058 (0.022), Hispanic female -0.018 (0.016),
  Black male +0.040, Black female +0.041 pp.
- Leonard 1990 JEP p. 50-51: 1974-80 Black male +0.62%/yr faster, white male -0.2%/yr at
  contractors; after 1980 effect reversed. Holzer-Neumark w7323 p. 35-37: Leonard's white male
  share at contractors -1.5 pp (2.6%) 1974-80; H-N micro data white male employment 10-15% lower
  at AA firms, mostly to white women and Black men.
- McCrary w12368 abstract: court-ordered quotas +14 pp Black share of new police hires.
- KRW w29053 p. 25: federal contractors show smaller Black-white contact gaps; Quillian 2017:
  whites +24% callbacks vs Latinos (CI 15-33), falling from 1.30 (1990) to 1.15 (2010).

Contracting (USAspending API, `_cache/usaspending/*.json`, pulled 2026-09-24)
- FY2024 contract obligations: all $740.66bn; self-certified SDB $77.29bn; 8(a) participants
  $36.70bn; minority-owned $78.79bn; Hispanic-owned $13.29bn; woman-owned $35.22bn.
- 8(a) set-aside + sole-source (codes 8A, 8AN): FY2024 $15.13bn (Hispanic-owned $1.36bn = 9.0%;
  Native American-owned $8.52bn); FY2023 $14.13bn; FY2022 $12.18bn.
- CRS IF12055 v3: FY2020 DBE awards and commitments ~$6.2bn. Marion 2007 WP p. 12: 1993-99 MBE
  7.0% and WBE 5.8% of federal-aid highway dollars; p. 1/4: 10 pp goal -> +4.3 pp DBE
  utilization (state trends), +5.4 pp (California IV). Marion 2009 REStat abstract p. 503:
  state-funded prices -5.6% after Prop 209 (full text paywalled; abstract only).
- DOT IFR 90 FR 47969 (3 Oct 2025): presumption removed; 41,000 firms to reevaluate.
- CRS R48190 (19 Sep 2024) p. 12-13: after Ultima (July 2023) SBA stopped presuming social
  disadvantage; entity-owned firms (ANC, tribes, NHO, CDC) need no narrative.

### Round 2 (calculation), 2026-09-24 09:40

- calc.py run twice; derived/calc_output.txt sha256 ee522e53...cc99 both runs (byte-identical) after the final note edit.
- 2024 central $3.96bn (0.18-18.70); pre-2023 $3.80bn (0.15-17.46); Hispanic $1.11bn; Mexican-origin $0.58bn;
  per NH-white-native worker $41 ($2-192).

## Gaps

- [GAP] Marion 2009 body text (DBE participation drop after Prop 209) unreachable.
- [GAP] National DBE dollars after FY2020 and the minority vs women split after 1999.
- [GAP] State and local MBE programs: no national total.
- [GAP] Graduate and professional school preferences (medicine, law) not priced.
- [GAP] Post-SFFA enrollment by race (IPEDS fall 2024) not yet published.

### Round 3 (Marion 2009 body retry), 2026-09-24 post-compaction

- calc.py rerun after compaction: all three derived files byte-identical to the hashes in
  RESULT.md (calc_output.txt ee522e53...cc99).
- Marion 2009 REStat body still unreachable: agent-browser on the DOI returns the citation only;
  Unpaywall reports no open copy; CiteSeerX (2006 WP, doi 10.1.1.365.2237) serves an HTML
  challenge to curl and times out on Exa crawl; only the WP abstract is reachable (same 5.6%).
- Secondary: NAS (Geshekter, 25 Sep 2008) quotes Marion: winning bids fell "by between 3.1 and
  5.6 percent relative to similar federal-aid contracts". UNVERIFIED. The 2.8% central is below
  that range; RESULT.md now gives the linear sensitivity (row 3c $0.53bn at 3.1%, $0.74bn at
  4.35%; 2024 central total $4.22bn at 4.35%). Parameters unchanged.
- [GAP] Marion 2009 Table with the 3.1-5.6% specifications: needs library access.
