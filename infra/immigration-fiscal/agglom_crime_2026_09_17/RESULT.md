# Crime → de-agglomeration channel: audit of Cremieux "America's Bad Cities Are Costing You" + scaling to Mexican-origin

**Verdict:** **Do not book it.** The $888 and $392 are Cremieux's own arithmetic on two self-estimated parameters, and his package's own direct outcome measure (metro earnings per job) is zero with the wrong sign. The transfer to the Mexican-origin case fails on the flight leg: per immigrant arrival, natives fall only 0.134 (Saiz & Wachter IV) and total population rises, against a net city-emptying in the Great Migration. Book $0 with a named sensitivity of $0 to −$1,700 per US-born Mexican-origin adult-year (0–21% of the −$8,286 gap). Full reasoning in section G.

Model self-report: claude-opus-5[1m] (Opus 5, 1M context), researcher subagent, lane `infra/immigration-fiscal/agglom_crime_2026_09_17/`.

## Scope
1. Open Cremieux replication package (7 Sep 2026 post), identify underlying papers + coefficients; separate published coefficients from Cremieux's own arithmetic in the $888/yr density-loss and $392/yr crime-wave numbers.
2. Scale to Mexican-origin case [INFERENCE, range]: violent-crime-ratio scaling vs preference-driven native flight (Saiz & Wachter 2011).
3. Disconfirming evidence: immigrants raise density/agglomeration (Saiz 2007; Albert & Monras 2022; Peri TFP); Latino paradox (Sampson; MacDonald-Hipp-Gill 2013).
4. Verdict on ledger inclusion vs the −$8,286 gap.

## Findings

Sections A–G below. Package downloaded and read; Saiz & Wachter 2011 and MacDonald–Hipp–Gill 2013 fetched and quoted from the PDFs.

---
## A. The replication package: what it is [VERIFIED 2026-09-17]

Post text recovered in full by plain `curl` (no paywall). The replication link in the post body resolves to **OSF node `xzfdw`**, one file, `agglomeration_crime_replication.zip` (343 KB, sha256 `299ea600cd21c76d6509f6eb4482caf9b677eba3596c7a3a94aaf23d052d8260`, uploaded 2026-09-07, **current_version 4**, last modified 2026-09-08, 8 downloads at time of read). Unzipped to `_cache/pkg/` (not committed). Contents: 100+ numbered Python scripts, `output/*.txt` point estimates, `README.md`, `DATA_SOURCES.md`, `REFERENCES.md`, `CODE_REVIEW.md`. No raw data (~20 GB, fetch scripts included). [SOURCE: https://api.osf.io/v2/nodes/xzfdw/files/osfstorage/ ; https://osf.io/download/uh38j/]

The post itself says it is a **"timed post"** — written in under one hour or auto-deleted. The package is not: it is a large, separately-built research artifact with its own two-round code review.

## B. Where $888 and $392 come from [VERIFIED — arithmetic traced in `output/per_capita.txt`]

**$888 is not a published coefficient. It is Cremieux's own arithmetic over three inputs, two of which are his own estimates.**

The chain is: Black inflow → experienced-density loss → × a density elasticity of productivity `E` → × 2019 metro earnings → ÷ 305m Americans.

| Input | Value | Whose |
|---|---|---|
| Boustan instrument (predicted Black in-migration), white departures per Black arrival | IV **−2.628** (se 0.652), levels 1940–70, N=280, 70 metros; decade-diff IV −2.678 (0.760); by decade IV −1.64 / −3.06 / −3.18 | Boustan 2010 QJE design, **re-estimated** in `output/boustan_replication.txt`. The "2.7 white departures" in the brief matches −2.678. |
| Experienced-density change per Black inflow = 10% of 1940 city pop | OLS −14.9 (5.3), **IV −37.3 (12.0) log pts** 1969–2000; IV −40.2 (14.1) to 2019 | **Cremieux's own** (`output/accounting.txt` panel A) |
| Density elasticity of productivity `E` | **0.069 central**, 0.03–0.103 range | **Cremieux's own** county panel, script 27: "0.103 raw, 0.069 with college and race composition" (`scripts/35_per_capita.py:2-3`). **NOT Ahlfeldt–Pietrostefani 0.04**, which does not appear in `REFERENCES.md` at all. The literature anchors present are Ciccone & Hall 1996, Combes & Gobillon 2015, Combes et al. 2008, Rosenthal & Strange 2004. |
| Scale | 49 destination metros, 118m residents, $5.69tn 2019 earnings; divided by US 305m | Cremieux's own |

Result (`output/per_capita.txt`): E=0.030 → −$386/American; **E=0.069 → −$888/American** (−$2,297 per destination-metro resident, −$271 bn/yr); E=0.103 → −$1,325. So the headline is the **middle of a 2.3:1 band driven entirely by his own choice of `E`**, and the band is not shown in the post.

**$392** = the 1960s–90s crime wave, and it is a **sum of two arms** from `output/crime_per_capita.csv`:
- density loss, own OLS elasticity, E=0.069: **−$154.66/American**
- elasticity erosion, own panel dE/dln(hom) = **−0.0064 (SE 0.0043, t≈1.5)**: **−$236.79/American**
- sum −$391.4 ≈ the post's $392.

The erosion arm's own alternatives in the same file span **−$189 to −$4,810** per American (county-FE variant −$773; cross-metro slope −$2,294; Donovan NZ −$4,810). The chosen arm is the *smallest but one*, and its coefficient is **not significant at 5%** (−0.0064, SE 0.0043). Calling $392 a "lower bound" is defensible on arm-selection; calling it an estimate is not, at t≈1.5.

**Published coefficients actually used, with source:**
- **Cullen & Levitt 1999 REStat 81(2):159–169**: city-population elasticity to index crime **−0.10 per log point**; the package carries it as ≈−0.15 per log homicide at an assumed homicide-to-index ratio k=1.5 (`output/crime_channel.txt` final line; `output/per_capita.txt`). The "each reported crime → one resident leaves / 10% crime → 1% population" statement in the brief is Cullen–Levitt's own and matches −0.10.
- **Boustan 2010 QJE 125(1):417–443** — design and instrument, re-estimated above.
- **Derenoncourt 2022 AER 112(2):369–408** — cited in the post's footnote 6 and README part 10 only as a reason the migrants' *gain* side is overstated (second generation fared worse), not as an input to the loss.
- **Collins & Wanamaker 2014 AEJ:Applied 6(1):220–252** and **Boustan 2016** — anchor the migrant-gain side ("moving North roughly doubled a Black worker's earnings").
- **Donovan, de Graaff, de Groot & Schiff 2024, J. Housing Economics 64:101991** — the only published crime→agglomeration-erosion elasticity in the package (−0.13, New Zealand), used as an upper arm.
- **Shertzer & Walsh 2019 REStat 101(3):415–427** — in `REFERENCES.md`, used for racial sorting, not in the dollar chain.
- **Ahlfeldt & Pietrostefani 2019 — NOT in the package.** [VERIFIED NEGATIVE]

**Own arithmetic vs published, in one line:** the *design* (Boustan instrument, Cullen–Levitt elasticity) is published; the *magnitude* ($888, $392) is Cremieux's, resting on two self-estimated parameters (experienced-density IV of −37 log pts, E=0.069) and one insignificant one (erosion −0.0064).

## C. The disconfirmer inside his own package [VERIFIED]

The productivity loss is **imputed, never measured**. `output/accounting.txt` panel A, same regression, same sample: "Implied productivity effect of the experienced-density change at E = 0.05: −2.01 log pts per 10% inflow … **metro earnings per job actually +0.4 (2.9)**." The direct outcome is a precise-ish zero with the wrong sign. `output/crime_channel.txt` agrees: crime instrumented by the Migration gives **ln SMSA earnings/job growth 69–00 IV +0.175 (0.109)** and central-county **+0.156 (0.112)** — positive. Every dollar of the $888 comes from multiplying a density change by an assumed elasticity, against a measured earnings effect of zero.

Second internal tension: in the modern county panel (`output/violent_property.txt` panel A, 1981–2004, 423 counties), the elasticity of population and employment to the **violent**-crime rate is **positive** (+0.016 (0.004) and +0.024 (0.005)); only **homicide alone** is negative (population −0.057 (0.016), employment −0.092 (0.017)). The post's claim that "anti-agglomeration effects are particularly distinct for violent crime, as opposed to property crime" is carried by homicide and assault, not by the violent index.

[GAP] Not yet read: `CODE_REVIEW.md`, `output/african_flight.txt` (the placebo that the post leans on for "it's crime not race"), `output/unseen.txt`.

## D. The "it's crime, not race" placebo is weaker than the post says [VERIFIED]

The post asserts flatly that other visibly-distinct, discriminated-against, lower-crime groups "do not seem to lead people ... to leave." The package's own African-immigrant placebo (`output/african_flight.txt`, ACS tracts 2010–2019, county FE, clustered by county, per 10% inflow) is:

| Window | native-born Black inflow | African immigrant inflow | difference |
|---|---|---|---|
| 2010–2015 | −0.67 | +0.37 | +1.04 (0.39), p=0.007 |
| 2015–2019 | −1.43 | −1.20 | +0.23 (0.35), **p=0.506** |
| 2010–2019 | −0.07 | +1.25 | +1.31 (0.71), **p=0.066** |

One of three windows is significant. The README concedes it ("difference significant in 2010–2015, marginal over the decade, though modern flight is weak for all groups"); the post does not. `CODE_REVIEW.md` is a real two-pass audit (author + Grok 4.6) that found and fixed five sign- or magnitude-moving bugs, including a duplicate-CBSA problem that moved the headline density IV from −39.2 to −40.2 and a New-York-mapped-to-Staten-Island error. It is more careful than the post that summarises it.

## E. Scaling to the Mexican-origin case [INFERENCE — ranges, not estimates]

**The unit chain.** −40.2 log points of experienced density per Black inflow of 10% of 1940 central-city population, × E = 0.069, = −2.77% of destination-metro earnings per 10% inflow. At the mean 17% inflow that is −4.71%, matching the package's earnings-weighted −4.76%. Per migration-attributable Black person-year the loss is roughly **−$15,000 to −$23,000** [INFERENCE: my denominator, from −$271 bn/yr against a migration-attributable non-South Black stock of 12–18m; the package never computes a per-migrant loss, only per-American].

**The two legs that must transfer: crime intensity, and the flight response.**

*Crime leg.* The Great Migration chain runs on **homicide**: SMSA homicide rate IV +43.2 per 100k (1965–69) per 10% inflow; the modern county panel shows the population/employment elasticity is carried by homicide (−0.057, −0.092) and aggravated assault (−0.060, −0.100), while the **violent-crime index enters with the wrong sign** (+0.016, +0.024). The Black–white homicide offending ratio the literature rests on is about **7.6:1** (BJS Homicide Trends 1980–2008, offending 34.4 vs 4.5 per 100k) [UNVERIFIED-CITE: not re-fetched this session]; the violent-arrest ratio is ≈3.0–3.5:1. The repo's measured Mexican-origin ratios are institutionalisation **1.7–1.9×** white and violent arrests **2.6–3.3×** per adult (ladder 78, memo §12).

Scaling on *excess over 1*:
- like-for-like violent arrests: (2.6−1)/(3.5−1) to (3.3−1)/(3.0−1) = **0.64 to 1.15**
- on homicide, which is the leg the chain actually uses: (1.7−1)/(7.6−1) to (1.9−1)/(7.6−1) = **0.11 to 0.14**

*Flight leg — this is where the transfer breaks.* **Saiz & Wachter 2011, AEJ:Policy 3(2):169–188, doi:10.1257/pol.3.2.169, Table 3, IV (gravity-pull instrument), 36,847 tract-decades, 1980–90 and 1990–2000:** per immigrant arrival divided by initial tract population, **non-Hispanic white population −0.678 (0.045)**, **total native population −0.134 (0.043)**. Compare the Great Migration: whites **−2.628 (0.652)** per Black arrival (`output/boustan_replication.txt`, levels IV; decade-diff −2.678), and **ln total central-city population −1.263 (0.609)** per unit inflow — the cities *net-emptied*.

So per arrival the immigrant white-flight response is **0.26× the Great Migration's**, and the *net population* response is **+0.87 per arrival** (one arrival minus 0.134 native departures) against a net loss for the Great Migration. Saiz & Wachter say so explicitly: the native flight "can be entirely accounted for by a shrinking non-Hispanic white population", consistent with immigrant families bringing ≈0.45 native-born children each. **Density rises.**

**The two numbers the brief asks for:**

| Route | Assumption | Per US-born Mexican-origin adult-year | % of the −$8,286 gap |
|---|---|---|---|
| **A. Crime-scaled** | the whole Great Migration density loss is a dose-response to violent-crime intensity, so a group with a fraction of the crime excess produces that fraction of the loss | homicide-excess scaling: **−$1,700 to −$3,200**; violent-arrest scaling (not the leg the chain uses): −$10,000 to −$26,000 | 20–39%, or implausibly >100% |
| **B. Preference-driven flight (Saiz & Wachter's own reading)** | native departure from immigrant neighbourhoods is a taste for neighbourhood composition, not a response to crime; the arrival-to-density mapping is measured directly and is positive | **$0, or a density gain** | 0% |

**Why they differ.** Route A treats crime as the sole mediator and rescales a reduced form by an offending ratio; it never checks whether the mediator's downstream leg (net population) has the same sign for the new group. Route B uses the directly measured leg. Saiz & Wachter's three candidate explanations for slower housing-value growth in immigrant tracts are housing quality, reverse causality, and natives finding immigrant neighbourhoods less desirable — **crime is not among them**. If the flight is a composition preference, the crime ratio is not the right scalar at any value, and the density consequence is the measured +0.87, not a fraction of −1.26.

## F. Disconfirming evidence [VERIFIED except where flagged]

1. **Albert & Monras 2022, AER, doi:10.1257/aer.20211241** — "international migrants concentrate more in expensive cities — the more so, the lower the prices in their origin countries are — and consume less locally than comparable natives." Immigrants sort *into* dense, expensive, high-wage cities more strongly than natives. Direct sign flip on the location margin the whole channel depends on.
2. **Saiz 2007 JUE 61(2)** (already in repo §13): +1% of population from immigration → rents and values +≈1%. Arrivals raise the price of urban land. A de-agglomeration cost of the same arrivals would have to show up as land prices *falling*; the repo cannot book both this and §13's rent-increase cost without double-counting with opposite signs.
3. **Peri 2012 REStat** (repo §16): immigration raises state **TFP +1.37 (0.15)** with capital intensity unchanged (−0.08, 0.13). Measured aggregate productivity gain.
4. **MacDonald, Hipp & Gill 2013, J. Quantitative Criminology 29(2):191–215, doi:10.1007/s10940-012-9176-8**, 835 Los Angeles tracts, 1990 immigrant concentration as IV for 2000 concentration, outcome = change in crime rate per 1,000, 2000–2005. Table 3: predicted immigrant concentration on **violent crime −2.73 (.32)** and **−4.01 (.45)**; total crime −3.86 (1.06) and −6.76 (1.42). Appendix B, **foreign-born Latino concentration specifically: violent −3.70 (.468), total −6.24 (.135)**, all significant. In the same regressions **ln(persons per square mile) enters positively on violent crime, +1.10 (.26) to +1.35 (.29)** — density *raises* crime, the mirror image of the post's framing.
5. **Sampson's Latino paradox** (Sampson, Morenoff & Raudenbush 2005 AJPH; PHDCN Chicago): first-generation immigrants substantially less violent than third-plus generation, and living in a high-immigrant-concentration neighbourhood lowers violence independently. [UNVERIFIED-CITE: not re-fetched this session; the repo's own generational memo already carries the generational gradient.]

## G. Verdict: does any of this belong in the ledger?

**No, not as a booked line. Book $0 with a named one-sided sensitivity of $0 to −$1,700 per US-born Mexican-origin adult-year (0% to 21% of the −$8,286 gap), recorded the way §16 records the automation channel — mechanism named, magnitude explicitly not booked.**

Five reasons, in order of weight:

1. **The author's own direct measurement is zero.** `output/accounting.txt`: implied productivity effect −2.01 log points, "metro earnings per job actually **+0.4 (2.9)**." `output/crime_channel.txt`: crime instrumented by the Migration → ln earnings per job **+0.175 (0.109)**. Every dollar of the $888 is density × an assumed elasticity, standing against a measured outcome of zero with the wrong sign. The repo's own rule for the automation channel (§16: "the direct output measure is zero ... which is why it is tempting and why it should not be booked") applies verbatim.
2. **The magnitude is a free parameter.** E = 0.069 is Cremieux's own; the package's own band gives $386–$1,325 per American. The crime-wave $392 rests on an erosion coefficient of −0.0064 with SE 0.0043 (t ≈ 1.5), whose sibling arms in the same CSV span −$189 to −$4,810.
3. **The transfer leg has the wrong sign.** The channel is mediated by net population loss. Measured for immigrant arrivals (Saiz & Wachter IV), natives fall only 0.134 per arrival and total population rises. There is no credible route from a Mexican-origin arrival to a density *loss*.
4. **The one direct test on Hispanic immigrants goes the other way.** MacDonald–Hipp–Gill's IV puts foreign-born Latino concentration at −3.70 on violent crime per 1,000.
5. **Double-counting.** §12 already prices willingness-to-pay to avoid violence through victim intangibles (+$1,421 central, up to +$2,023). A de-agglomeration cost is largely the *same* willingness-to-pay expressed through location choice rather than victimisation. And §13 books immigrant arrival as *raising* rents; an agglomeration loss from the same arrival would require land prices to fall.

**[FRAMING-SENSITIVE]** Cremieux's own footnote concedes the density fall "reflects a revealed preference for lower density in response to crime rather than a pure deadweight loss per se." That concession is fatal to booking it in a fiscal ledger at all: a household that moves to a suburb it prefers at the margin has not lost the full modelled agglomeration rent.

**What is worth adopting from the package regardless of the verdict:** the Cullen & Levitt 1999 elasticity (−0.10 city population per log point of index crime) as a published anchor for any future crime→location work, and `CODE_REVIEW.md` as a model of what an audited replication package looks like.

## Remaining gaps

- [GAP] Black–white homicide offending ratio (7.6:1) taken from memory of BJS Homicide Trends 1980–2008; not re-fetched. If re-dispatched: pull `bjs.ojp.gov` NCJ 236018 Table/Figure for offender-race rates, and a Mexican-origin homicide offending ratio, which the repo does not appear to hold — §12 gives murder's *share* of the cost difference (65%), not the level ratio. That number would tighten Route A's 0.11–0.14 scalar, which is the only defensible one.
- [GAP] Sampson, Morenoff & Raudenbush 2005 AJPH coefficients not re-fetched.
- [GAP] `output/unseen.txt` (patents/invention channel) and `output/modern_agglomeration_crime.txt` not read; the README flags the latter as the least stable result, so it is unlikely to change the verdict.
- [GAP] Not attempted: rerunning any of the package's scripts (raw data ≈20 GB; `disk-preflight` rule applies and the verdict does not turn on re-execution).

## Revisions
2026-09-17 — stub replaced by sections A–G; `[UNVERIFIED]` header verdict superseded by section G.
