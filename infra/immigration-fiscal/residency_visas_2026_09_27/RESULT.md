claude-opus-5-5

# Residency visas: crowd-out, pay parity, FICA exemptions (Rochester claim)

**Verdict:** The Rochester post misreads a real roster. Rochester General's internal-medicine page lists 78 residents
(three classes plus chiefs), not 82 hired in one round; 2 trained at a US school and 73 abroad (excluding the
Caribbean), but the page shows no visa or citizenship, so "80 on H-1B or J-1" and "2 Americans" are unverified.
Pay is one scale, and Medicare GME pays the same per resident regardless of citizenship. The real tax break is J-1:
about $8,500 of employer FICA over a residency, $2,800 a year averaged. H-1B residents pay full FICA and cost the
employer more. The binding limit is positions: 40,041 PGY-1 slots against 28,760 US MD and DO seniors. US MD seniors
who rank only internal medicine go unmatched 1.8% of the time. The contestable margin is about 2,900 unplaced US
graduates and US-citizen IMGs a year. The one documented USMLE breach is Nepal: 832 examinees' scores were
invalidated in 2024. OPT's FICA exemption forgoes roughly $2–4bn a year.

Lane: `infra/immigration-fiscal/residency_visas_2026_09_27/` · brief: `BRIEF.md` (ab66513) · started 2026-09-28 JST.
Source quotes live in `reads/`, one file per source. Every number carries a tag
(`[SOURCE]`, `[CALCULATION]`, `[INFERENCE]`, `[UNVERIFIED]`). Scripts `fica_calc.py`, `nrmp_opt_calc.py` and
`roster.py` write `derived/`; `strip_html.py` turns the cached roster HTML into the text `roster.py` reads.

## Steel-man of the claim

The strongest version: some community internal-medicine programs fill almost every seat with graduates of foreign
schools, often from a few countries, while US graduates (including US citizens who studied in the Caribbean and DO
graduates) go unmatched. If visa-holding residents were cheaper, through a payroll-tax exemption or lower pay, a
hospital would have a cost motive to prefer them, and a concentrated faculty network could steer seats. A documented
test-security breach (Nepal 2024) would make foreign exam scores less trustworthy as a screen. The check below takes
each link in turn: the count, the pay, the tax, who is displaced, and the exam record.

## Checks (appended as each completes)


### Q1. The Rochester count (checked 2026-09-28; quotes in `reads/q1_rochester.md`)

The claim is an X post by @JobsNowPaper, 2026-09-26, with an image this lane could not see (x.com not fetched; text
via Instapundit). The hospital's own roster for the **Rochester General internal medicine residency** is the only
hospital source that fits it. It lists **78 names, not 82**: 5 chief residents, 24 PGY-3, 25 PGY-2 and 24 PGY-1
[CALCULATION: `roster.py` → `derived/roster_counts.txt`]. It is three classes plus chiefs, not one hiring round; the
program has **24 first-year positions** a year [SOURCE: program page, "24 R1 Positions"]. The page shows academic year
2025-26 (its chiefs are listed as Class of 2024-25 graduates).

The page gives medical school only, never visa or citizenship. **Exactly 2 residents graduated from US schools**, both
from Lake Erie College of Osteopathic Medicine (one PGY-2, one PGY-1) [CALCULATION: `roster.py` →
`derived/roster_by_school_country.csv`]. That matches the post's "only 2 are Americans",
so the post appears to have equated "US school" with "American" and "foreign school" with "H-1B or J-1" [INFERENCE].
That equation is wrong in two known ways:
- **3 residents trained at Caribbean schools** (Saba, Ross, American University of Antigua) [CALCULATION:
  `roster.py`]. Those schools mainly
  enrol US citizens, and NRMP counts them as "U.S. IMGs" when the graduate is a citizen. Their citizenship is not on the
  page [UNVERIFIED either way].
- A foreign-school graduate can be a US citizen or green-card holder. NRMP's "non-U.S. IMG" category means non-citizen,
  which includes permanent residents; it is not the same as visa holder [SOURCE: NRMP definitions, reads/q4].

What is verified: 73 of 78 listed residents (94%) trained at schools outside the US and Caribbean. By school country:
India 21, Pakistan 15, Sudan 7, Nepal 5, UAE 4 and Egypt 3; the other 18 come from 15 countries with one or two each.
The Caribbean accounts for 3 and the US for 2 of 78 (2.6%) [CALCULATION: `roster.py` → `derived/roster_counts.txt`;
one row per resident in `derived/roster_by_school_country.csv`]. The 2 Weill Cornell Medicine-Qatar graduates count
as IMGs: WCM-Q says its graduates enter the Match "as International Medical Graduates" [SOURCE: WCM-Q admissions FAQ,
reads/q1]. What is not:
"82", "80 on H-1B or J-1" and "2 Americans" as a citizenship count. The program says it sponsors both J-1 and H-1B and
prefers H-1B when obtainable [SOURCE: program page]; AMA FREIDA lists J-1 yes, H-1B no [SOURCE: FREIDA 1403531314].
DOL disclosure aggregators show RGH filing dozens of "Medical Resident Physician" H-1B LCAs a year (77 certified
FY2020–26, median $65,693) [SECONDARY]. So some residents are on H-1B, some on J-1, and some need no visa; the split
is not public.

### Q2. Pay and Medicare GME (quotes in `reads/q2_q3_pay_gme_tax.md`)

- **Pay is one scale.** RGH IM posts $73,000 / $76,000 / $80,000 for PGY-1/2/3 in 2025-26, "granted to all residents"
  [SOURCE]. For H-1B residents parity is a legal floor: the LCA wage must be "the greater of the actual wage rate" paid
  "to all other individuals with similar experience and qualifications" and the prevailing wage, including benefits
  [SOURCE: 20 CFR 655.731(a)]. No wage-parity rule exists for J-1 physicians in 22 CFR 62.27, but no evidence was found
  of J-1 residents paid below the program scale [GAP: no national pay-by-visa data].
- **Medicare pays per resident regardless of citizenship.** A "foreign medical graduate" is defined by the school's
  accreditation, not citizenship; an ECFMG-certified FMG counts like any resident, with weighting factor 1.0 during the
  initial residency period [SOURCE: 42 CFR 413.75(b), 413.79(b); 42 U.S.C. 1395ww(h)(4)(D)]. The count that Medicare
  funds is capped at each hospital's 1996 level [SOURCE: 1395ww(h)(4)(F)(i)]. No provision in the statute or the
  regulations conditions payment on visa status. **No GME money is gained by hiring a visa holder instead of a
  citizen.**

### Q3. FICA exemptions and the per-resident saving (quotes in `reads/q2_q3_pay_gme_tax.md`; `fica_calc.py`)

| Status | FICA while a resident | Legal basis | How long |
|---|---|---|---|
| J-1 physician (ECFMG) | Exempt, employer and employee, while a nonresident alien | 26 U.S.C. 3121(b)(19); FUTA 3306(c)(19) | J-1 physicians are "teachers or trainees" (IRS J-1 page): exempt individual for **2 calendar years** (2-of-6 rule, 7701(b)(5)(E)(i)); resident alien and taxed from year 3 |
| F-1 on OPT | Exempt while a nonresident alien; OPT is "practical training" | 3121(b)(19); Pub. 519 | F-1 students are exempt individuals for **5 calendar years** (7701(b)(5)(E)(ii)); rare for residents, as OPT is time-limited and FREIDA lists it separately |
| H-1B | **Not exempt**; taxed "from the very first day of U.S. employment" | H is not in 3121(b)(19); IRS alien-liability page | Whole residency (totalization certificates aside) |
| US citizen / green card | Taxed | Residents are not "students" under 3121(b)(10) since 2005 regs (Mayo, 2011) | Whole residency |

Per J-1 resident at RGH pay, starting in July with no prior exempt years: the exemption covers July of year 1 to
December of year 2, **$111,000 of wages, 48% of residency pay**. Each side saves 7.65%: **$8,492 employer and $8,492
employee over the residency, $16,983 combined**. That is $5,585 for the employer in the fully exempt PGY-1 year and
**$2,831 a year averaged over three years**, plus at most $42 a year of FUTA [CALCULATION: `fica_calc.py`,
`derived/fica_calc.txt`]. Prior US time on F or J shortens this.

H-1B costs the employer more than a citizen, not less: full FICA, plus petition fees [TRAINING-DATA, GAP: the 2024
fee rule was not re-fetched]. The Sept 2025 proclamation also added a $100,000 payment for beneficiaries abroad. It was
extended on 2026-09-18 to Sept 21, 2027, but guidance implementing it was vacated on 2026-06-08, with a stay denied on
2026-07-24 [SOURCE: USCIS H-1B page; FR 2026-19554]. A $103,265 fee on cap-subject petitions is proposed [SOURCE: FR
2026-17324]. RGH states that it prefers H-1B when it can get one [SOURCE]. That is the costlier route, so its stated
preference runs against a cost-minimizing motive [INFERENCE].

### Q4. Who is displaced (quotes in `reads/q4_nrmp_crowdout.md`; `nrmp_opt_calc.py`)

**Match rates, PGY-1** [SOURCE: NRMP Results and Data 2025, Table 4A]:

| Applicant type | 2025 match | 2025 placed after SOAP (active) | 2024 match | 2024 placed |
|---|---|---|---|---|
| US MD seniors | 93.5% | 97.8% | 93.5% | 97.9% |
| US DO seniors | 92.6% | 98.4% | 92.3% | 98.5% |
| US MD prior graduates | 45.9% | 53.3% | 45.7% | 54.1% |
| US DO prior graduates | 43.8% | 54.4% | 47.6% | 59.3% |
| US-citizen IMGs | 67.8% | 73.5% | 67.0% | 73.4% |
| Non-US-citizen IMGs | 58.0% | 60.3% | 58.5% | 61.5% |

- **Internal medicine (categorical), 2025:** 10,941 positions and 10,584 filled. US MD seniors filled 3,782, DO
  seniors 1,882, US IMGs 1,145 and non-US IMGs 3,573. IMGs hold **44.6% of filled seats** (non-citizens 33.8%, US
  citizens 10.8%). In 2024 the IMG share was 43.0% (non-citizens 31.8%) [CALCULATION: `nrmp_opt_calc.py` →
  `derived/nrmp_opt_calc.txt`, from NRMP Table 2/7].
- **Community programs:** program-director surveys, 2007–2019, found that IMGs filled **55–70% of community programs'
  IM intern seats versus 22–30% at university programs**. In 2017 community programs gave 46% of rank-list places to
  IMGs, against 16% at university programs [SOURCE: JGIM, PMC7878164]. In FREIDA 2017–18, **42% of IM programs were
  "IMG-dominated"** (US-citizen and non-citizen IMGs pooled) [SOURCE: JGIM 2020, PMC7210370]. No NRMP table splits
  community from university programs [GAP for 2024–25].
- **The displacement margin is not US MD seniors.** Of seniors who ranked only IM, 1.8% of MDs (67 of 3,772) and 2.5%
  of DOs (41 of 1,649) went unmatched. The seniors who do go unmatched are concentrated in competitive fields. Among
  those who ranked only orthopaedics, 26.4% of MD seniors went unmatched; neurosurgery 27.1%, dermatology 22.7%, plastic
  surgery 22.8% [SOURCE: Table 12A]. Those are fields IMGs barely enter.
- **The margin is prior US graduates and US-citizen IMGs.** After SOAP in 2025 the unplaced active applicants were: 446
  US MD seniors, 133 DO seniors, 817 prior US MD graduates, 287 prior DO graduates and 1,217 US-citizen IMGs, a total
  of **2,900**. Another 4,550 non-citizen IMGs were unplaced [CALCULATION: `derived/nrmp_opt_calc.txt`, from Table 4A/4B]. Prior US graduates who
  ranked only IM went unmatched at 31.7% (MD) and 35.1% (DO) [SOURCE: Table 12B]. Those applicants compete for the same
  IMG-heavy community seats. US-citizen IMGs match at a higher rate than non-citizen IMGs (67.8% vs 58.0%), so the
  national data show no blanket preference for non-citizens. That comparison does not control for exam scores [GAP].
- **The binding constraint is positions.** There are 40,041 PGY-1 positions against 20,368 active US MD seniors (1.97
  per senior) and 8,392 DO seniors. **11,281 first-year seats (28.2%) exceed the entire US MD and DO senior class**
  [SOURCE: Table 5; CALCULATION: `derived/nrmp_opt_calc.txt`]. Medicare funds residents only up to each hospital's 1996 count [SOURCE: 42 U.S.C.
  1395ww(h)(4)(F)]. Hospitals can add positions above the cap at their own cost, and the Match grew from 27,825 PGY-1
  positions in 2016 to 40,041 in 2025. So the cap limits Medicare's funding, not the count of positions itself. Because
  positions exceed US seniors, program preference can reorder only the roughly 2,900 unplaced Americans against the
  non-citizens now placed. If every unplaced American replaced a placed non-citizen IMG, 4,015 of the 6,915
  non-citizen PGY-1 placements would still be needed [INFERENCE; CALCULATION: `derived/nrmp_opt_calc.txt`].

### Q5. "Countries with documented USMLE cheating" (quotes in `reads/q5_usmle.md`)

- **Documented: Nepal, 2024.** On 2024-01-31 USMLE invalidated passing results for **832 examinees "associated with
  Nepal"**: 618 had one Step flagged, 202 two and 12 all three. The flags rested on answer-agreement odds of "1 in
  100 million" [SOURCE: NBME declaration, D.D.C. 1:24-cv-00410, Doc. 15-2 ¶19]. ECFMG told the 832 to destroy their
  certificates [SOURCE: plaintiffs' filing, Doc. 21 ¶46].
- **Flagged, not acted on publicly: Jordan, Pakistan, India.** NBME's own declaration says tips led it to analyse
  centers in Jordan, Nepal and Pakistan, and later two centers in India. For 2022 Step 1 and 2021–22 Step 2 CK, that
  group showed "a substantially higher percentage of examinees with a statistically significant level of agreement
  matches ... compared to the baseline group". The declaration also says "the vast majority" of flagged examinees
  tested in Nepal [SOURCE: Doc. 15-2 ¶6, ¶9]. The plaintiffs allege that NBME "has since taken no public action against
  test-takers from India, Jordan, Pakistan" [SOURCE: Doc. 21; advocate's claim].
- **Not documented:** any invalidation of a country cohort other than Nepal, any count for Pakistan, India, Sudan or
  Egypt, and any link between a Rochester resident and the Nepal invalidations. ECFMG's annual counts of individual
  irregular-behavior findings were not retrieved [GAP]. The RGH roster includes 5 Nepal-trained residents, PGY-1
  to chief [CALCULATION: `roster.py` → `derived/roster_counts.txt`]. Whether any of them was affected is unknown; invalidated examinees had to retest to keep
  their certification [UNVERIFIED].

### Q6. OPT beyond residency (quotes in `reads/q6_opt.md`; `nrmp_opt_calc.py`)

- **Participants, 2024** [SOURCE: SEVIS by the Numbers 2024]: 194,554 new OPT authorizations, 95,384 new STEM OPT
  authorizations and 381,140 unique records with any practical training (CPT included). The stock of records
  authorized at some point in 2024 was OPT 340,066 and STEM OPT 165,524.
- **Revenue forgone, rough.** Person-years were taken as 0.4–0.6 of the OPT stock plus 0.7–0.9 of the STEM stock. The
  other inputs are an 80–90% exempt share (IFP measured 85%) and a mean wage of $60,000–$90,000. SEVIS publishes no
  wages, so the wage is an assumption. The result is **$1.9–4.4bn a year, central $3.0bn**, split evenly: **employer
  about $1.5bn, employee about $1.5bn** [CALCULATION: `nrmp_opt_calc.py` → `derived/nrmp_opt_calc.txt`; assumption-heavy]. Outside checks agree: IFP's central
  $32bn over ten years (about $3.2bn a year) and CIS's $4.1bn for 2023. The CIS figure is an upper-end count because
  it includes CPT and assumes every participant is exempt all year.
- **Employer preference on cost grounds: incentive documented, behaviour not measured.** DHS's 2016 rule states the
  7.65% employer saving. IFP and Tax Notes argue it creates a hiring incentive. No empirical study of hiring responses
  was found [GAP]. For residents OPT hardly applies: it needs a US degree, and FREIDA lists it separately (RGH IM:
  "F-1 visa (OPT 1st year) No").

### Q7. Verdict by claim and mechanism

| Claim or mechanism | Verdict | Numbers |
|---|---|---|
| "hired 82 resident doctors" | **False as stated** | The roster lists 78 across three classes plus 5 chiefs; 24 intern seats a year |
| "80 are foreign workers on H-1B or J-1" | **Unverified; overstated as framed** | 73–76 of 78 trained abroad; visa status is not public; some are citizens or green-card holders by NRMP's definitions |
| "Only 2 are Americans" | **Unverified; likely a school count** | 2 US-school (LECOM DO) graduates; 3 Caribbean graduates of unknown citizenship |
| "mostly from countries with documented USMLE cheating" | **True only under a loose reading** | Nepal alone has a documented mass invalidation (832); 5 of 78 RGH residents trained there (6%). Counting every country in NBME's flagged analysis group (Nepal, Pakistan, India, Jordan; no public action outside Nepal) gives 42 of 78 (54%), by school country, not citizenship |
| Salary savings | **False** | One pay scale ($73k/$76k/$80k); the H-1B LCA forbids paying below the actual wage |
| Medicare GME favours visa holders | **False** | Payment per FTE is identical; FMG status depends on the school, not citizenship |
| J-1 FICA exemption | **True, small** | $8,492 employer and $8,492 resident per J-1 residency; $2,831 a year for the employer averaged over three years, 3.9% of PGY-1 pay (7.65% in a fully exempt year) |
| F-1 OPT FICA exemption (residency) | **True in law, negligible in practice** | OPT residents are rare; RGH does not take OPT |
| H-1B saves money | **False** | H-1B pays full FICA plus petition fees; $100k payment for hires abroad (extended to Sept 2027, now blocked by court) |
| Crowd-out of US MD seniors | **False at the national level** | 97.8% placed; 1.8% of IM-only MD seniors unmatched |
| Crowd-out of US-citizen IMGs and prior US graduates | **Plausible at the margin, unmeasured** | 2,900 unplaced a year; IMG-heavy community IM programs are where they compete; no score-controlled study |
| OPT FICA exemption economy-wide | **True** | Roughly $2–4bn a year forgone, half employer and half employee |

Table sources: roster counts (rows 1–4) from `roster.py` → `derived/roster_counts.txt`; J-1 figures from
`derived/fica_calc.txt`; NRMP and OPT figures from `derived/nrmp_opt_calc.txt` [CALCULATION].

Framing note [FRAMING-SENSITIVE]: calling a program "98% visa workers" treats training abroad as foreign status.
The documented facts are about training location and a J-1 payroll-tax break. Visa counts are not public, and
program-level evidence of cost-driven selection was not found.

## Gaps and next queries
- [GAP] The RGH visa split: ask the program or check ECFMG J-1 sponsorship counts by institution. DOL LCA files by
  FEIN 16-0743134 would give H-1B resident counts (primary DOL disclosure xlsx, not the aggregators).
- [GAP] ECFMG/Intealth annual irregular-behavior counts; USMLE annual performance data by country of school.
- [GAP] Community vs university IMG share for 2024–25 (ACGME Data Resource Book, or FREIDA scrape).
- [GAP] Score-controlled comparison of US-citizen versus non-citizen IMG match odds (NRMP Charting Outcomes for IMGs).
- [GAP] The 2024 USCIS fee schedule (I-129, ACWIA, asylum-program and fraud fees) was not re-fetched; values are
  TRAINING-DATA.
- The X image itself was not examined (x.com barred); the post's source may be another page or year.
- [GAP] NRMP 2026 Match data exist. A secondary source quotes PGY-1 match rates of 70% for US-citizen IMGs and 56.4%
  for non-citizen IMGs [SECONDARY: 1pmdaily.com, 2026-03-21]. This lane used 2024–2025 as briefed and did not pull
  the 2026 tables.
