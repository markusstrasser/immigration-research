# Immigration — New Falsifiable Claim Candidates (2026-06-24)

**Purpose:** Propose NEW, specific, falsifiable claims for the ledger, prioritizing the
under-covered areas: **crime**, **second-generation fiscal/mobility**, and sharp quantitative
claims that current evidence could **kill or confirm** (disconfirmation is mandatory — Constitution P4).

**Status:** Candidate list. None are graded yet; each is paired with the dataset/paper that would
settle it (cross-ref `immigration-dataset-roadmap.md`) and tagged with the evidence level needed.

**Coordinate map** (from `immigration-fiscal-welfare-ledger-map.md`): each claim notes its
generator cluster (A–U) and ledger coordinate where applicable.

**Evidence-level legend:** `[L1 admin-data]` (settled by an official administrative dataset) ·
`[L2 micro-study]` (needs a peer-reviewed micro design) · `[L3 ecological]` (county/state panel,
confound-prone) · `[L4 derived]` (algebraic transform of held data). "Kills" = the claim's most
likely outcome falsifies a current corpus belief.

---

## A. CRIME (the structural gap — repo name promises it, stack omits it)

### C1. Undocumented felony arrest rate in Texas is below 50% of the native-born rate (per-100k), and the gap survives a race-stratified native denominator
**Coordinate:** new `crime` domain; cluster A (NPV/incidence bridge via SCAAP). **Evidence needed:** `[L1 admin-data]`.
The current memo states the >2x aggregate violent-arrest gap but flags that it is NOT race-stratified (Light et al. did not stratify the native denominator). This claim is *sharper and more killable*: it asserts the per-capita undocumented felony arrest rate stays below the **non-Black native-born** rate. Most likely outcome: gap **narrows** from ~50% to ~30% (consistent with the incarceration data in the crime memo) — i.e. it would **partially falsify** the headline "2x lower" framing while confirming direction.
**Tests with:** TX-DPS-LIGHT-2020 (openICPSR 124923) joined to ACS race-by-nativity (held IPUMS panel). [SOURCE: openicpsr.org/.../124923, DOI 10.3886/E124923V1]

### C2. Incarceration rate by citizenship, computed directly from BJS Survey of Prison Inmates 2016, confirms non-citizen prisoners are under-represented relative to their share of the resident population
**Coordinate:** `crime`. **Evidence needed:** `[L1 admin-data]`, Butcher–Piehl method on micro-data.
Replaces the corpus's reliance on Cato/Nowrasteh *secondary* race-stratified tables with an **independent primary computation** from the BJS public-use file. This is a disconfirmation target for the corpus's own belief: if non-citizen prisoners are NOT under-represented in SPI-2016, the incarceration-gap finding has a serious problem.
**Tests with:** BJS-SPI-2016 (ICPSR 37692, DS1 public) + ACS institutionalized-GQ-by-nativity. [SOURCE: icpsr.umich.edu/.../37692]

### C3. Federal-offender composition: non-citizens are over-represented among federal convictions, but this is driven almost entirely by immigration offenses (8 U.S.C.) — net of immigration offenses, non-citizens are NOT over-represented
**Coordinate:** `crime`; isolates the immigration-offense confound. **Evidence needed:** `[L1 admin-data]`.
A classic restrictionist talking point ("non-citizens are X% of federal prisoners") is testable and likely **OVERBROAD**: the share collapses once immigration-specific offenses (illegal entry/reentry, document fraud) are removed. Killable in either direction.
**Tests with:** USSC-OFFENDERS individual datafiles (citizenship × offense of conviction, FY2002→). [SOURCE: ussc.gov/research/datafiles]

### C4. Sanctuary-policy adoption did NOT raise crime rates in adopting cities vs. comparable controls
**Coordinate:** `crime`; `[L3 ecological]` / DiD. **Verify pass:** `supported` (confidence 1.0) — multiple peer-reviewed studies find no crime increase, some find robbery/property decreases. [SOURCE: sciencedirect S0167268121004480; Justice Quarterly 36(4); PMC7959582]
This is a CONFIRM-leaning claim worth pinning to the ledger because it directly rebuts a high-salience public belief. Falsification surface: a credible DiD on post-2017 sanctuary designations showing a crime increase.
**Tests with:** FBI-NIBRS-CDE county crime panel × sanctuary-jurisdiction list × foreign-born share (held county warehouse). [SOURCE: cde.ucr.cjis.gov]

### C5. Intensified interior immigration enforcement (Secure Communities / 287(g)) did NOT reduce local crime — and may have raised violent victimization via reduced reporting among Latinos
**Coordinate:** `crime` + enforcement-cost (cluster B/G). **Verify pass:** `contradicted` for the "enforcement reduces crime" claim (confidence 0.95) — NIJ 305488, J. Law Econ Org 38(2), NBER w32109 all find no meaningful crime reduction; PMC11309025 finds raised victimization risk. [SOURCE: ojp.gov/pdffiles1/nij/grants/305488.pdf]
**Disconfirmation value:** kills the deterrence rationale for enforcement-as-crime-policy. The killable inverse: a jurisdiction-level design showing Secure Communities lowered the index crime rate.
**Tests with:** Secure Communities activation dates × FBI county crime + NCVS victimization. [SOURCE: nber.org/w32109]

### C6. The ICE national-docket criminal-noncitizen counts, when converted to an annual rate over the resident unauthorized stock, imply a per-capita serious-crime rate BELOW the native-born rate
**Coordinate:** `crime`; `[L4 derived]` — explicitly a rate-base-fallacy demonstration. **Evidence needed:** held ICE-ERO letter + Pew/CMS unauthorized stock.
Turns the corpus's qualitative "stock-not-rate" caveat into a **quantified falsifiable claim**. If the implied rate actually exceeds native-born, the corpus's dismissal of the ICE numbers is wrong.
**Tests with:** ICE-ERO-STATS (held) + unauthorized-population denominators. [SOURCE: ice.gov/statistics]

### C7. Deportation of a resident (removal) does not lower the origin household's local crime exposure — net of incapacitation, removals show no measurable crime decrease in the sending county
**Coordinate:** `crime`. **Evidence needed:** `[L3 ecological]`/IV (IZA dp12413 instrument).
Tests the incapacitation premise behind mass-removal-as-public-safety. [SOURCE: docs.iza.org/dp12413.pdf]

---

## B. SECOND-GENERATION fiscal & mobility (corpus under-weights this; cluster C/D)

### S1. US-born children of immigrants (second generation) are the HIGHEST net fiscal contributors of any generational group, exceeding third-generation-plus natives
**Coordinate:** Fiscal — dynasty (incl. 2nd gen); ledger sign ~0/+. **Verify pass:** `supported` (0.9) — NAS 2016 (NAP.edu/23550) finds 2nd-gen are top net contributors; Census CB16-203 on earnings. (NBER w26408 = Abramitzky-Boustan *mobility*, NOT the NAS net-contributor finding — don't conflate.) [SOURCE: nap.edu/23550; census.gov CB16-203]
**Disconfirmation value:** directly attacks the "low-skill parent ⇒ permanent fiscal drag" frame named in the ledger map. Killable: a same-universe lifetime micro-sim showing 2nd-gen net contribution below 3rd-gen+.
**Tests with:** NAS 2016 fiscal tables + ABJP-MOBILITY (openICPSR 120490) for the mobility mechanism. [SOURCE: nber.org/system/files/working_papers/w26408]

### S2. Children of immigrants from nearly EVERY origin country have higher upward mobility (rank-rank) than children of US-born parents at the same parental income percentile
**Coordinate:** second-gen mobility; cluster D. **Verify pass:** `supported` (1.0) — Abramitzky-Boustan-Jácome-Pérez AER 2021, millions of father-son pairs, holds historically and today. [SOURCE: elisajacome.github.io/Jacome/ImmigrantMobility_AER.pdf]
**Killable inverse:** an origin for which the second-gen rank-rank slope is *below* the US-born baseline at low parental income.
**Tests with:** ABJP-MOBILITY-120490 + OI Opportunity Atlas 2nd-gen tables. [SOURCE: aeaweb.org 10.1257/aer.20191586]

### S3. Quantify the convergence: by the second generation, the first-generation crime/incarceration ADVANTAGE has largely disappeared (2nd-gen incarceration ≈ same-race native-born, not ≈ first-gen low)
**Coordinate:** bridges crime (A) and second-gen (C). **Evidence needed:** `[L2 micro-study]`.
The crime memo (Claim 9) flags this generational-assimilation pattern but marks it scope-limited and un-quantified. This pins a number. **Disconfirmation-heavy:** its likely outcome FALSIFIES any clean "immigrants and their descendants are low-crime" narrative — the advantage is a first-generation, not a lineage, property.
**Tests with:** OI Opportunity Atlas 2nd-gen incarceration-by-origin tables. [SOURCE: opportunityinsights.org/data]

### S4. Per-capita welfare/benefit receipt RISES from first-generation non-citizens to naturalized citizens and the second generation (i.e. the low first-gen welfare use does not persist down the lineage)
**Coordinate:** Fiscal — federal cash-flow; cluster C/G. **Verify pass:** `supported` (1.0) — naturalized citizens consume more per-capita than non-citizens (older, more SS/Medicare-eligible); the household-vs-per-capita metric drives disagreement. [SOURCE: cato.org BP-137; nber.org/w27811]
**Disconfirmation value:** complicates the "immigrants use less welfare" claim by showing it is generation- and metric-dependent — a genuine ledger-coordinate-switching trap made explicit.
**Tests with:** SIPP/CPS per-capita benefit receipt by generation × citizenship (held SIPP MVP + ACS). [SOURCE: cato.org/sites/cato.org/files/2022-03/BP-137.pdf]

---

## C. SHARP QUANTITATIVE CLAIMS that current evidence could KILL or CONFIRM

### Q1. Refugees reach net-positive fiscal contribution within ~8 years of arrival and are net positive over 20 years
**Coordinate:** Fiscal — lifetime NPV, humanitarian channel; cluster T05/A. **Verify pass:** `supported` (1.0) — NBER w23498 (8-year break-even, 20-yr net positive); HHS 2024 study $124B positive over 15 yrs. [SOURCE: nber.org/system/files/working_papers/w23498; hhs.gov 2024-02-15 release]
**Killable:** the HHS number was politically contested at release; a same-universe re-estimate could move the break-even point. Refugees are a distinct selection regime from labor migrants (crime memo's international caveat) — worth a separate ledger line.
**Tests with:** HHS-ORR data + ASPE refugee fiscal-impact file. [SOURCE: aspe.hhs.gov refugee-fiscal-impact-study]

### Q2. Emergency Medicaid for unauthorized/ineligible non-citizens totaled ~$27B over FY2017–23 ($18B federal + $9B state) — a DIRECT admin cost-line replacing the corpus's inferential MEPS proxy
**Coordinate:** Fiscal — state-local + federal; cluster C/N. **Evidence needed:** `[L1 admin-data]`.
The corpus currently prices unauthorized health costs *inferentially* via the MEPS→SIPP bridge. This is a killable confirm: if the direct CMS-64 number is far below the inferred proxy, the corpus's health-cost line is overstated.
**Tests with:** CMS-EMERGENCY-MEDICAID (CBO Arrington letter 2024-10). [SOURCE: cbo.gov/system/files/2024-10/Arrington_Letter_EmergencyMedicaid_Immigration_final.pdf]

### Q3. The <HS-education immigrant cell's lifetime fiscal NPV flips sign (− to +) between the NAS "current-law" accounting and the dynamic capital-tax GE specification
**Coordinate:** Fiscal — lifetime NPV <HS cell; cluster A01/A02. **Evidence needed:** `[L4 derived]` re-run.
The ledger map asserts NAS −$109k flips to +$128k under Clemens GE. This pins it as a *falsifiable reproduction target*: re-derive both under one same-universe micro-sim. If the flip does NOT reproduce, a central ledger-map claim is wrong.
**Tests with:** NAS 2016 + held education-bucket stock + lifetime warehouse. [SOURCE: immigration-fiscal-welfare-ledger-map.md A01/A02]

### Q4. Immigrant entrepreneurship: foreign-born are net firm FOUNDERS at a per-capita rate above US-born, quantifiable from official Census ABS owner-nativity microdata (not secondary citation)
**Coordinate:** Labor demand / entrepreneurship; cluster T04/F04; ledger sign +. **Evidence needed:** `[L1 admin-data]`.
Replaces the corpus's secondary citation (Azoulay et al.) with a primary computation. Killable: if ABS owner-nativity shows foreign-born below US-born per-capita ownership in job-creating NAICS sectors.
**Tests with:** CENSUS-ABS-CBO API (USBORN/USCITIZEN × NAICS). [SOURCE: census.gov/data/developers/data-sets/abs.html]

### Q5. State/local net fiscal cost per added 2023-surge resident is approximately −$2.1k/yr (direct) — but this is a first-generation, single-year, state-local-only figure that does NOT survive a dynasty or federal-inclusive horizon
**Coordinate:** Fiscal — first-gen static state-local (−); cluster C/N/O. **Evidence needed:** `[L4 derived]`, already partly in matrix Claim 3.
This is the corpus's most-cited negative number; the claim asserts its *fragility* (coordinate-switching). Killable: show the −$2.1k persists under a dynasty/federal horizon (it should not, per S1).
**Tests with:** CBO 2025 state-local immigration file (held). [SOURCE: cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

### Q6. SCAAP criminal-alien inmate-days data shows the incarceration cost of criminal aliens is concentrated in a handful of states (CA/TX/AZ/NY), and per-capita criminal-alien inmate-days are NOT rising over FY2015–23
**Coordinate:** crime↔fiscal bridge; cluster C/R. **Evidence needed:** `[L1 admin-data]`.
The only national admin series tying incarceration burden to dollars. Disconfirmation target for any "rising criminal-alien burden" claim.
**Tests with:** DOJ-SCAAP award PDFs (inmate-days × jurisdiction × FY). [SOURCE: bja.ojp.gov/program/state-criminal-alien-assistance-program-scaap]

---

## Priority ordering (for ledger insertion + testing)

1. **C1, C2, S3** — crime claims with held-or-cheap data that most directly fill the structural gap and carry high disconfirmation value (each can falsify a current corpus framing).
2. **S1, S2** — second-gen fiscal/mobility, strongest evidence anchors (verify confidence 0.9–1.0), correct the cost-side skew.
3. **C4, C5** — already verify-anchored (sanctuary no-effect confirmed; enforcement-deterrence contradicted) — pin as standing rebuttals.
4. **Q2, Q5** — replace inferential corpus numbers with direct admin data / expose coordinate-switching fragility.
5. **Q1, Q3, Q4, C3, C6, C7, S4, Q6** — second wave, mostly new-data-acquisition-gated.

## Verification log (this pass)

| Claim | Tool | Verdict | Confidence |
|---|---|---|---|
| S1 (2nd-gen top net contributors) | verify_claim/Exa | supported | 0.9 |
| C4 (sanctuary no crime increase) | verify_claim/Exa | supported | 1.0 |
| S2 (2nd-gen mobility > native) | verify_claim/Exa | supported | 1.0 |
| C5 (enforcement reduces crime) | verify_claim/Exa | **contradicted** | 0.95 |
| S4 (per-capita welfare rises by generation) | verify_claim/Exa | supported | 1.0 |
| Q1 (refugee 8-yr break-even, 20-yr net+) | verify_claim/Exa | supported | 1.0 |

Note: Exa /answer is web-grounded, not adversarial cross-model; treat confidences as a triage signal, not a final grade. All six were sense-checks of the claim *direction*; the ledger entry must still be settled against the paired primary dataset.
