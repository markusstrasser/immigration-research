# Gated-Dataset Acquisition Specs — 2026-06-25

**Purpose:** Submission-ready acquisition specs for three gated datasets the immigration-research
repo needs. Each spec is verified variable-by-variable against primary sources (IPUMS / ICPSR /
FBI). A wrong variable name wastes a gated extract request, so correctness is the deliverable.

**Verification status:** All variable names, codes, sample coverage, titles, and access paths below
were checked live against primary sources on 2026-06-25 (IPUMS-CPS variable pages fetched and the
embedded code JSON parsed directly; FBI/UCR NIBRS offender-segment documentation; openICPSR 120490
landing + AER article). Items I could not confirm at the primary source are tagged `[UNVERIFIED]`.

**Headline results (read these first):**
1. **IPUMS-CPS — GREEN.** `FBPL` (father's birthplace) and `MBPL` (mother's birthplace) exist, carry
   full country detail, and — importantly — are available in **every monthly CPS and the ASEC from
   1994 onward**, not just ASEC. `NATIVITY` directly codes 1st/2nd-generation from BPL+FBPL+MBPL. The
   2nd-generation-by-origin test (cluster-V V02) is fully buildable. Extract recipe below.
2. **NIBRS — RED for INT-04 as scoped.** NIBRS offender records contain **only age, sex, race, and
   ethnicity**. There is **no citizenship, nativity, country-of-birth, or immigration-status field**
   anywhere in the offender record. INT-04 ("crime-by-status detail from NIBRS") is **infeasible** as
   written. Redirect spelled out below (NIBRS supports offense detail + victim-offender relationship,
   not status; status-by-crime must come from a different source).
3. **openICPSR 120490 — GREEN, public access.** Abramitzky–Boustan–Jácome–Pérez replication package
   for the AER 2021 two-centuries immigrant-mobility paper. Lets us measure father→child rank-rank
   income/occupation mobility **by origin country**, the headline benefit-side finding the corpus
   under-weights.

---

## 1. IPUMS-CPS — 2nd-generation-by-origin cultural-transmission test (cluster-V V02)

### What it unblocks
The repo's IPUMS-**USA** supply-shock panel lacks **parental** birthplace, so it cannot identify
who is a 2nd-generation immigrant or what their parents' origin is. IPUMS-**CPS** carries father's
and mother's birthplace at full country detail. This is the dataset that makes the
cultural-transmission test runnable: take native-born respondents whose parents were foreign-born,
group by parental origin country, and measure whether origin-culture outcomes (female labor-force
participation, fertility, education, earnings) persist into the 2nd generation net of the usual
controls.

### The core variables — VERIFIED

| Mnemonic | Full name | Verified detail | Source |
|---|---|---|---|
| **`FBPL`** | Father's birthplace | "indicates whether the person's father was born in the United States and, if not, his foreign country of birth." Uses the BPL country-code scheme: ~40 categories in 1994, **100+ from 1995 forward**. Unknown/Other → 96000. | [SOURCE: https://cps.ipums.org/cps-action/variables/FBPL] |
| **`MBPL`** | Mother's birthplace | "indicates whether the person's mother was born in the United States and, if not, her foreign country of birth." Same BPL coding as FBPL; ~40 cats 1994, 100+ from 1995; Unknown/Other → 96000. | [SOURCE: https://cps.ipums.org/cps-action/variables/MBPL] |
| **`NATIVITY`** | Foreign birthplace or parentage | Constructed from `BPL` + `FBPL` + `MBPL`. Codes (parsed from the page's code table): **0** = Unknown; **1** = Both parents native-born; **2** = Father foreign, mother native; **3** = Mother foreign, father native; **4** = Both parents foreign; **5** = Foreign born. "Completely comparable across years" and with IPUMS-USA. | [SOURCE: https://cps.ipums.org/cps-action/variables/NATIVITY] |
| **`BPL`** | Birthplace (respondent's own) | Respondent's own country/state of birth — the 1st-gen identifier and foreign-born key. Same coding family as FBPL/MBPL. | [SOURCE: https://cps.ipums.org/cps-action/variables/BPL] |
| **`CITIZEN`** | Citizenship status | Codes (parsed): **1** = Born in U.S.; **2** = Born in U.S. outlying/territory; **3** = Born abroad of American parents; **4** = Naturalized citizen; **5** = Not a citizen; **9** = NIU. No flags; comparable across years. | [SOURCE: https://cps.ipums.org/cps-action/variables/CITIZEN] |
| **`YRIMMIG`** | Year of immigration | When a foreign-born person "came to the U.S. to stay." **Interval-coded, not single-year**: 0000 = NIU; 0001 = 1949 or earlier; 0002 = 1950–1959; then 5-year, then 2-year and 2–4-year bands. Bands shifted across survey years → cross-year comparisons of arrival cohort are lossy after 1991. | [SOURCE: https://cps.ipums.org/cps-action/variables/YRIMMIG] |

**Note on "detailed versions":** there is **no separate `FBPLD`/`MBPLD`**. `FBPL`/`MBPL` already carry
the country-detailed birthplace codes (the 100+-category scheme is the detail). This differs from
`BPL` in IPUMS-USA where a `BPLD` exists; in IPUMS-CPS the parental-birthplace variables are
single-level country detail. Do **not** request `FBPLD`/`MBPLD` — they are not CPS variables.
[SOURCE: https://cps.ipums.org/cps-action/variables/FBPL]

### Parental-birthplace sample coverage — VERIFIED (and better than assumed)
The prompt assumed parental birthplace might be ASEC-only. **It is not.** `FBPL`, `MBPL`, `NATIVITY`,
and `CITIZEN` are available in **all monthly CPS samples AND the ASEC from 1994 through 2024** (and
into 2025–2026 with gaps — October 2025 not collected due to the federal shutdown).
[SOURCE: https://cps.ipums.org/cps-action/variables/FBPL] [SOURCE: https://cps.ipums.org/cps-action/variables/NATIVITY]

Implication for the extract: parental birthplace + the *basic-monthly* labor outcomes (`EMPSTAT`,
`LABFORCE`) need only a monthly sample. But **income, detailed work, and the welfare/program outcomes
are ASEC-only** — so for the full V02 outcome battery, draw the **ASEC** samples (1994→2024, ~30
years) where parental birthplace and the rich economic block coexist.

### Weight — VERIFIED
- **`ASECWT`** — the ASEC person weight. Confirmed present on cps.ipums.org (with an `ASECWT_parent`
  companion). **Use `ASECWT` for any ASEC-based estimate.** [SOURCE: https://cps.ipums.org/cps-action/variables/ASECWT]
- `WTFINL` — the **basic-monthly** final person weight; use it only if you build the test on a basic
  monthly sample instead of ASEC. Do **not** mix: ASEC estimates take `ASECWT`, monthly estimates
  take `WTFINL`. [SOURCE: https://cps.ipums.org/cps-action/variables/WTFINL]
- Replicate weights (`REPWTP`) are available if you want design-based SEs. `[UNVERIFIED]` — not
  re-checked this pass; confirm on the extract screen if needed.

### Outcome variables for the V02 battery — IPUMS-CPS mnemonics
These are the standard IPUMS-CPS names for the outcomes V02 needs. **Each should be confirmed on its
own variable page at extract time** (I verified the identity/birthplace/weight block exhaustively;
the outcome mnemonics below are the canonical IPUMS-CPS names but were not each re-fetched this pass —
treat as `[VERIFY-AT-EXTRACT]`; they auto-validate when added to the cart):

| Need | Mnemonic | Sample |
|---|---|---|
| Employment status | `EMPSTAT` | monthly + ASEC |
| In labor force (for **female LFP**) | `LABFORCE` | monthly + ASEC |
| Total personal income | `INCTOT` | ASEC |
| Wage/salary income | `INCWAGE` | ASEC |
| Educational attainment | `EDUC` (+ `EDUCD` detail) | monthly + ASEC |
| Hours/weeks worked | `UHRSWORKLY`, `WKSWORK1` | ASEC |
| Sex (for female-LFP split) | `SEX` | all |
| Age | `AGE` | all |
| **Fertility** | **`FREVER`** (children ever born) and **`YNGCH`** / **`NCHILD`** (own children in household) | `FREVER` = June Fertility Supplement only; `YNGCH`/`NCHILD` = all |

**Fertility caveat (important for V02 design):** CPS does **not** carry a clean completed-fertility
measure in the ASEC. `FREVER` (children ever born) is collected only in the periodic **June Fertility
& Marital History Supplement**, not the ASEC. `YNGCH`/`NCHILD` (own children in household) are
available everywhere but measure *coresident* children, not completed fertility, and undercount for
older women whose children have left home. If fertility is a load-bearing outcome for the
cultural-transmission test, either (a) restrict to June-supplement years for `FREVER`, or (b) use
`NCHILD`/`YNGCH` for women in prime childbearing ages with the coresidence caveat stated.
`[VERIFY-AT-EXTRACT]` — confirm `FREVER` June-supplement coverage on its variable page.

### Extract recipe (cps.ipums.org)
1. Register / log in at **https://cps.ipums.org** (free; IPUMS account). [SOURCE: https://cps.ipums.org]
2. **Select samples:** ASEC 1994 → 2024 (all years). (Add basic-monthly samples only if you also want
   a monthly-only LFP series.)
3. **Add variables (cart):**
   - Identity/origin: `BPL`, `FBPL`, `MBPL`, `NATIVITY`, `CITIZEN`, `YRIMMIG`
   - Demographics: `AGE`, `SEX`, `RACE`, `HISPAN`, `MARST`
   - Education: `EDUC`, `EDUCD`
   - Labor/income: `EMPSTAT`, `LABFORCE`, `INCTOT`, `INCWAGE`, `UHRSWORKLY`, `WKSWORK1`
   - Fertility: `NCHILD`, `YNGCH` (+ `FREVER` if you add June-supplement samples)
   - Weights: `ASECWT` (auto-included with ASEC); add `REPWTP` if you want design SEs
   - (`YEAR`, `SERIAL`, `PERNUM`, `CPSIDP` are attached automatically as record IDs)
4. **Filters / case selection:** none needed at extract; do the 2nd-gen selection in analysis
   (`NATIVITY` ∈ {2,3,4} = native-born with ≥1 foreign-born parent; subset by `FBPL`/`MBPL` origin).
   Optionally restrict at extract to `AGE >= 25` to focus on completed-education adults.
5. **Format:** request **fixed-width (.dat) + DDI codebook**, or CSV. The repo already parses IPUMS
   fixed-width (the IPUMS-USA panel) → DDI/.dat keeps tooling consistent. Approx size: an ASEC
   1994–2024 person extract with ~25 variables is on the order of **a few GB uncompressed** (each ASEC
   year ≈ 100–200k households / 200k+ persons; 30 years × ~25 cols). Gzipped download is far smaller.
   `[UNVERIFIED]` exact byte size — IPUMS reports it on the extract screen before you submit; check there.
6. **Access path:** IPUMS-CPS is **free, registration-gated** (not a paid DUA). Extracts process
   server-side; download when ready (minutes to ~1 hr by size). [SOURCE: https://cps.ipums.org]

### Honest limits
- CPS is a **cross-section** (rotating panel at most 16 months); it does **not** link respondents to
  their actual parents — `FBPL`/`MBPL` are *self-reported parental birthplace*, available only while
  the question is asked and only as country-of-birth, not as a parental record. You get
  origin-of-parents, not a parent–child linked panel (that's what dataset #3 is for).
- `YRIMMIG` interval-banding limits arrival-cohort precision (above).
- Parental birthplace was added to the CPS in **1994**; there is no pre-1994 CPS 2nd-gen-by-origin
  series here. [SOURCE: https://cps.ipums.org/cps-action/variables/FBPL]

---

## 2. NIBRS — crime-by-status detail (INT-04) — **INFEASIBLE AS SCOPED**

### The critical determination (verified, stated plainly)
**NIBRS offender records do NOT contain citizenship, nativity, country of birth, or immigration
status.** The NIBRS **Offender Segment** is, in the words of the published reference, "the sparsest
of the available segments, and provides only four new variables that are about the offender's
demographics": **age, sex, race, and ethnicity** — nothing else.
[SOURCE: https://ucrbook.com/offender-segment-1.html]

The FBI's own data-element numbering confirms it: the offender attributes are **Data Element 37 (Age
of Offender), 38 (Sex of Offender), 39 (Race of Offender), 39A (Ethnicity of Offender)**. There is no
offender citizenship/nativity element. [SOURCE: https://www.fbi.gov/file-repository/ucr/a-guide-to-understanding-nibrs.pdf]

The closest thing in all of NIBRS is **Data Element 51, "Resident Status of Arrestee"**, which lives
in the **Arrestee Segment** (not the Offender Segment). And even DE 51 is **residency** (resident /
nonresident of the reporting jurisdiction), **not citizenship or immigration status** — it tells you
whether the arrestee lived locally, not whether they are foreign-born or undocumented.
[SOURCE: https://ucrbook.com/offender-segment-1.html] [SOURCE: https://www.fbi.gov/file-repository/ucr/a-guide-to-understanding-nibrs.pdf]

**Conclusion: INT-04 as scoped ("crime-by-status detail from NIBRS") cannot be built.** There is no
status field to join crime to. Do not request a NIBRS extract expecting a citizenship/nativity column
— it does not exist, and "ethnicity" (Hispanic/Latino vs not) is **not** nativity and must not be
substituted for it.

### What NIBRS CAN support (the valid redirect)
NIBRS is incident-level and rich on everything *except* status. Keep it for what it does well:
- **Offense detail:** ~50+ offense types coded per incident (the Offense Segment), far finer than the
  old summary UCR hierarchy. [SOURCE: https://www.fbi.gov/file-repository/ucr/a-guide-to-understanding-nibrs.pdf]
- **Victim–offender relationship:** the Victim Segment records the relationship of each victim to each
  offender — a genuine NIBRS strength unavailable in summary UCR. [SOURCE: https://ucrbook.com/offender-segment-1.html]
- **Incident circumstances:** location type, weapon, time, clearance, multiple offenses/victims/
  offenders per incident.
- **Ecological designs:** county/agency-level offense and arrest counts (joinable to county
  foreign-born share by FIPS) — the Ousey–Kubrin / Wadsworth immigration↔crime correlation design.
  This is the repo's existing `FBI-NIBRS-CDE` roadmap line, which already correctly flags "no nativity
  at incident level — ecological only." That line stands; **INT-04's individual-status ambition does
  not.**

Access for the ecological/offense use: FBI Crime Data Explorer bulk download (https://cde.ucr.cjis.gov)
or the ICPSR/NACJD NIBRS series (annual public-use studies). [SOURCE: https://www.icpsr.umich.edu/web/NACJD/studies/38690]

### Where crime-by-status (the real INT-04 goal) MUST come from instead
Status-by-crime requires a source that actually records immigration status. The repo's own roadmap
already lists the right substitutes — redirect INT-04 to these:
- **Texas DPS arrest records** (Light, He & Robey, PNAS 2020) — the *only* US source recording
  immigration status of all arrestees; openICPSR 124923. The correct home for "crime by legal status."
  [SOURCE: https://www.openicpsr.org/openicpsr/project/124923/version/V1/view]
- **US Sentencing Commission Individual Offender datafiles** — carry offender **citizenship** for
  federal offenders. [SOURCE: https://www.ussc.gov/research/datafiles/commission-datafiles]
- **BJS Survey of Prison Inmates 2016** — citizenship/nativity of state+federal prisoners
  (incarceration rate by nativity, Butcher–Piehl method). [SOURCE: https://www.icpsr.umich.edu/web/NACJD/studies/37692]

**Recommendation:** mark INT-04 "NIBRS" line **closed-infeasible**; fold its question into the
Texas-DPS / USSC / SPI crime cluster, which already exists in `immigration-dataset-roadmap.md`.
(Per the repo's "propose first" boundary, this protocol change is a proposal for human sign-off.)

---

## 3. openICPSR study 120490 — Abramitzky–Boustan immigrant intergenerational mobility

### Identity — VERIFIED
- **Title:** *Data and Code for: Intergenerational Mobility of Immigrants in the US over Two Centuries*
  [SOURCE: https://www.openicpsr.org/openicpsr/project/120490/version/V1/view]
- **Authors:** Ran Abramitzky (Stanford, NBER), Leah Platt Boustan (Princeton, NBER), Elisa Jácome
  (Princeton/Northwestern), Santiago Pérez (UC Davis, NBER).
  [SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.20191586]
- **Supports article:** *American Economic Review* 2021, **111(2): 580–608**,
  DOI **10.1257/aer.20191586**. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.20191586]
- **openICPSR project:** 120490, version V1; DOI **10.3886/E120490V1**.
  [SOURCE: https://www.openicpsr.org/openicpsr/project/120490/version/V1/view]

### What it contains — VERIFIED (structure) / partial (file-by-file)
The openICPSR landing exposes a build pipeline (folder path observed:
`…/V1/build/code/6_assemble_linked/_Main`), confirming it is a **full replication package: staged
build code that assembles the linked father–son data + analysis code that reproduces the paper's
figures/tables**, organized in numbered build steps. [SOURCE: https://www.openicpsr.org/openicpsr/project/120490/version/V1/view]

The underlying data are **linked father–son pairs spanning ~1880–2015**, combining (a) historically
linked complete-count US Census records (genealogy-assisted linking) for the historical cohorts and
(b) modern cohorts (CPS / tax-based ranks à la Opportunity Insights) for the contemporary period.
[SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.20191586]
`[UNVERIFIED — file manifest]`: the exact list of included data files vs. files the user must obtain
elsewhere is on the openICPSR file tree, which **bot-blocks automated fetch (HTTP 403)** — the page
resolves in a browser (the search index reads its folder contents) but WebFetch/Firecrawl are blocked.
**The operator should open the URL in a browser to read the precise file manifest and any "data not
included / obtain from X" notes.** AER packages of this vintage commonly ship derived/crosswalk files
openly while pointing to restricted raw sources (e.g., full-count Census, tax data) for the most
sensitive inputs — confirm on the page. `[UNVERIFIED]`

### Access / DUA terms — VERIFIED as public
- openICPSR project 120490 is **public-access** (the AER data-availability policy requires the
  replication package be openly posted). It requires a **free openICPSR/ICPSR login to download**;
  download invokes openICPSR's standard **Terms of Use** (cite the data, no re-identification, research
  use) — the lightweight click-through TOU, **not** a heavy restricted-data DUA for the package itself.
  [SOURCE: https://www.openicpsr.org/openicpsr/project/120490/version/V1/view]
- **Caveat:** any *restricted raw inputs* the package points to (if it does — see manifest caveat
  above) would carry their own separate agreements. The package's own posted files are public.
  `[UNVERIFIED]` whether 120490 references any restricted input — confirm in-browser.

### What it lets us measure
- **Father→son rank-rank intergenerational mobility by origin country**: for sons raised at a given
  point in the father's income/occupation distribution, where they end up in their own generation's
  distribution — computed **separately by parental sending country** and across historical vs. modern
  cohorts. [SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.20191586]
- The headline result it reproduces: **children of immigrants from nearly every sending country show
  higher upward mobility than children of the US-born**, similar historically and today. This is the
  **benefit-side** finding the corpus's evidence-base audit flags as under-weighted; it directly
  counters the "low-skill immigrant parent ⇒ permanent fiscal drag" frame in the welfare-ledger map.
  [SOURCE: https://www.aeaweb.org/articles?id=10.1257/aer.20191586]
- **Fit with dataset #1:** CPS gives *contemporary cross-sectional* 2nd-gen-by-origin outcomes;
  120490 gives the *linked, two-century, father–son mobility* version with a published, citable
  benchmark. Complementary — CPS for the cultural-transmission battery (LFP/fertility/educ), 120490
  for the income-mobility-by-origin headline.

### Acquisition note
openICPSR direct download → scriptable into `infra/immigration-fiscal/acquire/` like the other
openICPSR pulls in the roadmap (124923 Texas DPS, etc.), **but** the file tree must first be read in
a browser to script the right paths (403 on automated fetch). Approx size `[UNVERIFIED]` — shown on
the openICPSR download page.

---

## Provenance & limits summary

| Claim class | Status |
|---|---|
| IPUMS-CPS `FBPL`/`MBPL`/`NATIVITY`/`CITIZEN`/`YRIMMIG` names + codes + 1994→ coverage | **VERIFIED** (pages fetched, code JSON parsed) |
| IPUMS-CPS `ASECWT` weight identity | **VERIFIED** |
| IPUMS-CPS outcome mnemonics (`EMPSTAT`,`INCTOT`,`EDUC`,`FREVER`…) | canonical but `[VERIFY-AT-EXTRACT]` (not each re-fetched; auto-validated in cart) |
| IPUMS-CPS exact extract byte size | `[UNVERIFIED]` (shown pre-submit) |
| NIBRS offender record has NO citizenship/nativity | **VERIFIED** (FBI guide + ucrbook reference) |
| NIBRS DE 51 = residency-not-citizenship, in Arrestee segment | **VERIFIED** |
| openICPSR 120490 title/authors/AER cite/DOIs | **VERIFIED** |
| openICPSR 120490 public-access + free-login TOU | **VERIFIED** |
| openICPSR 120490 exact file manifest + any restricted inputs | `[UNVERIFIED]` (page 403s automated fetch; open in browser) |

**Instrument note:** this is a data-spec memo, not a substantive immigration claim, so the LLM-bias
caveat is low-stakes here — but the *redirect* recommendations (closing INT-04, folding it into the
crime cluster) are methodology calls; treat them as proposals for human sign-off per the repo's
"propose first" boundary on protocol changes.
