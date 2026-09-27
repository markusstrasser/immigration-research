claude-opus-5-5

**Verdict:** Mexico sends about a quarter of all parents of US citizens admitted as LPRs (IR-5):
36,652 a year over FY2015–2024 and 63,050 in FY2024, three times India (18,910) or China (16,760)
and eight times the Philippines (7,990); the flow doubled after 2019. Mexican parents are
admitted younger than other parents: at most 48% of the FY2024 Mexican IR-5 cohort was 55+
(about 38% on the NIS-2003 ratio), against 83% of all parents in NIS-2003. In the ACS, 13.6% of
Mexico-born people 65+ arrived at 50+; against Mexican seniors who arrived younger they report
more Medicaid (40% vs 32%) and SSI (10.2% vs 8.7%), much less Social Security (47% vs 73%), 70%
are non-citizens, and 48% live as the householder's parent. Valued with the ledger's
Mexico-born profile rescaled by those receipt and earnings patterns and the five-year statutory
bar, a Mexican parent admitted at 55 / 60 / 65 is a remaining-lifetime net cost of $525k / $478k
/ $437k undiscounted and $270k / $275k / $286k at 3% (case range at 3%: $254–339k), close to
Australia's official A$335–410k per parent visa. Against a same-age white resident's remaining
lifetime the parent is $114–128k more costly at 55 but $136–161k less costly at 65, because
white retirees draw larger Social Security and Medicare they paid for. One year's Mexican IR-5
admissions carry about $16bn at 3% ($33bn undiscounted) over their remaining lives for FY2024,
$9bn ($19bn) for the decade's mean year — a flow valuation, not an annual-account line. The
childcare offset is real in sign and small: +6 to +7 pp participation for an immigrant mother
of a preschooler (correlational), worth $120–380 a year in taxes per co-resident parent during
preschool years only.

# Late-arrival tail — Mexico-born who arrive at 50+ (sponsored parents)

Lane started 2026-09-27. Sections are appended as each task completes.

## 1. Flow: parents of US citizens (IR-5) admitted, FY2005–FY2024

Script `flow.py` → `derived/ir5_flow.csv`, `derived/ir5_age_nis2003.csv`,
`derived/lpr_age_table9_fy2024.csv`, `derived/mexico_ir_new_vs_adjust.csv`,
`derived/flow_gates.csv` (128/128 pass), `derived/flow_sources.json` (sha256 of every input).

The IR-5 class by country is not a numbered Yearbook table. It comes from OHSS's companion
workbook "Persons Obtaining LPR Status by Region and Country of Birth", sheet "Immediate
Relatives – Parents" (FY2005–2022 unrounded edition, FY2005–2024 edition rounded to 10)
[SOURCE: ohss.dhs.gov/topics/immigration/lawful-permanent-residents/lprs-country-birth-and-major-classes-admission].
Gates: the sheet's all-country Total equals the Yearbook Table 6 "Parents" row in every year
(FY2013 Yearbook Table 6 for 2005–2013, FY2023 and FY2024 Table 6 for 2014–2024); the unrounded
country rows sum to the Total up to the withheld "D" cells; the rounded edition is within 5 of
the unrounded one for 2005–2022 [DATA: derived/flow_gates.csv].

| FY | All countries | Mexico | India | China | Philippines | Mexico share of all IR-5 | IR-5 share of Mexico's LPRs |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2005 | 82,113 | 15,289 | 8,618 | 6,853 | 6,421 | 18.6% | 9.5% |
| 2010 | 116,208 | 22,336 | 10,689 | 8,353 | 9,387 | 19.2% | 16.1% |
| 2015 | 132,961 | 29,035 | 10,618 | 11,863 | 8,833 | 21.8% | 18.3% |
| 2019 | 140,128 | 34,186 | 10,411 | 10,001 | 5,853 | 24.4% | 21.9% |
| 2021 | 80,515 | 25,798 | 3,843 | 4,638 | 1,231 | 32.0% | 24.1% |
| 2022 | 132,505 | 31,691 | 10,155 | 7,696 | 3,771 | 23.9% | 22.8% |
| 2023 | 208,350 | 52,380 | 19,210 | 11,170 | 5,770 | 25.1% | 29.0% |
| 2024 | 252,570 | 63,050 | 18,910 | 16,760 | 7,990 | 25.0% | 31.1% |
| Sum 2005–2024 | 2,653,573 | 612,797 | 209,851 | 198,598 | 147,107 | 23.1% | — |
| Mean 2015–2024 | 150,156 | 36,652 | 11,379 | 10,398 | 5,872 | 24.4% | — |

[DATA: derived/ir5_flow.csv; FY2023–2024 from the rounded edition]

Mexico sends about a quarter of all IR-5 parents, three times India or China per year, and the
flow has doubled since 2019 (34k → 63k). In FY2024 IR-5 parents were 31% of all Mexican-born new
LPRs. Of Mexico's 149k immediate relatives in FY2024, 107k adjusted status inside the US and 42k
arrived from abroad (expanded Table 10; spouses, children and parents combined; the IR-5 split of
new vs adjusted is not published by country) [DATA: derived/mexico_ir_new_vs_adjust.csv].

### Age at admission

No published table crosses IR-5 with age by country. Three pieces bound it:

1. **Profiles on LPRs, Mexico** (OHSS, one workbook per year): Mexican-born new LPRs of all
   classes aged 55+ were 30,160 in FY2024 (21,490 aged 55–64, 8,670 aged 65+), against 63,050
   IR-5 parents. So at most 48% of Mexican IR-5 parents admitted in FY2024 were 55 or older. The
   same bound was 96% in FY2005 and has fallen steadily (80% 2010, 54% 2015, 45% 2019, 48% 2024):
   Mexican parents are now admitted younger, most at 45–54 (50,610 Mexican LPRs aged 45–54 in
   FY2024) [DATA: ir5_flow.csv `ir5_55plus_upper_bound_share`]. For India, China and the
   Philippines the bound is 1.0 and uninformative.
2. **New Immigrant Survey 2003** (a probability sample of LPRs admitted May–Nov 2003; visa
   category "Parent of U.S. Citizen", n = 982 with birth year): weighted mean age at admission
   62.0 for Mexico (n = 268) against 65.6 India, 65.7 China, 63.9 Philippines, 63.4 all. Share
   aged 55+: Mexico 75%, India 91%, China 95%, Philippines 87%, all 83%; 65+: Mexico 43%, all 46%
   [DATA: derived/ir5_age_nis2003.csv; age = admission year − A7 birth year, ±1 year].
3. **Yearbook FY2024 Table 9**, all countries: immediate relatives aged 55–59 50,460, 60–64
   47,150, 65–74 65,470, 75+ 25,640 (188,720 aged 55+) against 252,570 parents; so at least 64k
   parents nationally were under 55 [DATA: derived/lpr_age_table9_fy2024.csv].

Applying NIS-2003's Mexico ratio (75% of IR-5 aged 55+ when the profile bound was ~96%) to the
FY2024 bound puts about 38% (≈24k) of Mexico's FY2024 IR-5 parents at 55+, with 48% (30k) the
ceiling [INFERENCE: assumes the non-parent share of Mexican LPRs aged 55+ is stable]. Over
FY2015–2024 that is about 14–18k Mexican IR-5 parents a year admitted at 55+. The ACS proxy for
Mexico-born entries at 50+ by any route is 15–20k a year (section 2), consistent in size.

## 2. Stock and receipt: ACS 2019, 2021–2023, persons 65+

Scripts `acs_census.py`, `acs_late_arrival.py` (Census API 1-year PUMS, state-partitioned,
cached) → `derived/late_arrival_65plus.csv`, `derived/acs_arrivals.csv`, `derived/acs_gate.csv`.
The 2020 1-year PUMS is not on the API (HTTP 404). Gate: weighted foreign-born Mexico totals are
within −0.59% to +0.14% of published B05006 in all four years (India −0.32% to +0.40%)
[DATA: derived/acs_gate.csv]. Pooled estimates use PWGTP/4; SEs from the 80 successive-difference
replicates pooled the same way. Age at arrival = AGEP − (survey year − YOEP). YOEP is the most
recent arrival, so a circular migrant who last returned after 50 counts as a late arrival.

| Persons 65+, pooled | Mexico arr. <50 | Mexico arr. 50+ | India arr. <50 | India arr. 50+ | US-born NH white |
|---|---|---|---|---|---|
| Persons (annual avg) | 1,140,275 | 179,740 | 250,163 | 108,887 | 40,098,098 |
| Share of the origin's 65+ | 86.4% | 13.6 ±0.2% | 69.7% | 30.3 ±0.5% | — |
| Medicaid (HINS4) | 32.0 ±0.3% | 40.1 ±0.8% | 13.0 ±0.4% | 38.7 ±1.0% | 10.8% |
| Medicare (HINS3) | 89.7 ±0.2% | 74.9 ±0.7% | 91.4 ±0.4% | 73.9 ±1.1% | 96.6% |
| SSI receipt | 8.7 ±0.2% | 10.2 ±0.4% | 5.0 ±0.3% | 14.3 ±0.7% | 3.1% |
| Social Security receipt | 72.5 ±0.3% | 47.3 ±0.8% | 74.9 ±0.6% | 34.1 ±0.9% | 85.2% |
| Mean SS $ (2023, zeros incl.) | 9,675 | 5,270 ±117 | 14,562 | 4,148 | 16,285 |
| Mean SSI $ (2023) | 676 | 743 ±34 | 439 | 1,056 | 358 |
| Not a citizen | 34.8% | 69.5 ±0.8% | 6.9% | 51.0% | — |
| In poverty | 18.2% | 22.4 ±0.6% | 5.6% | 7.9% | 8.1% |
| Parent or parent-in-law of householder | 18.6% | 48.3 ±0.8% | 20.6% | 70.8% | 3.1% |
| Mean years since arrival | 46.5 | 16.5 | 41.7 | 12.7 | — |
| Less than high school | 68.4% | 75.0% | 12.2% | 31.5% | 7.2% |
| n | 44,443 | 6,512 | 10,899 | 4,277 | 2,195,047 |

[DATA: derived/late_arrival_65plus.csv; worker notes in ignored `_cache/acs_agent_result.md`]

By arrival band (Mexico 65+): Medicaid is flat at 38–41% across arrival at 50–54, 55–59, 60–64
and 65+; SSI falls from 12.5% (arrived 50–54) to 7.2% (arrived 65+); Social Security falls from
56.8% to 34.2%; non-citizens rise from 61% to 80%; living as the householder's parent rises from
36% to 63%. The Medicaid gap over earlier Mexican arrivals (+6 to +11 pp) and the Social
Security gap (about −25 pp) hold in each single year; the SSI gap is +1 to +3 pp except 2021
(none). HINS4 includes state-funded plans (e.g. Medi-Cal for undocumented seniors), and survey
reports under-count SSI and Medicaid, so the gaps are more reliable than the levels [INFERENCE].
An arrival at 50+ is not an IR-5 parent: the ACS group also holds spouses, other family classes,
refugees and people without status.

Stock: Mexico-born who arrived at 50+ are 2.4% of the 10.8M Mexico-born (259k across all current
ages); India 5.4%. Recent arrivals at 50+ (survey year − YOEP ≤ 1): Mexico ≈30k per survey year
(9.8% of recent Mexican arrivals), roughly 15–20k entries a year once the 1.5–2-year window is
allowed for; it excludes parents who adjusted inside the US [DATA: derived/acs_arrivals.csv].

## 3. Per-admission value: a Mexican parent admitted as an LPR at 55, 60 or 65

Script `per_admission.py` → `derived/per_admission.csv` (400 rows: arrival ages 45, 50, 55, 60,
65 × four arms × three cases × two survival arms × real rates 0/2/3/5%),
`derived/per_admission_provenance.json`. Added as arms in this lane; the lineage lane is not
edited.

**Method.** Remaining-lifetime NPV from the age of admission to 100, survival-weighted with the
NVSS 2024 tables and summed over the ledger's single-age balances, through the ledger lane's own
verified loaders (`lifetime.load_age_profiles`, `read_life_table`, `survival_npv`; no
`[BLOCKED]`; the pooled arm reproduces the ledger's survival NPVs to $0.05). Balances are the
`ledger_absolute_2026_09_17` Mexico-born component profile (personal allocation, expanded
account, 2024 prices, no real growth), rescaled for a late arrival as follows:

| Item | Rule | Status |
|---|---|---|
| Income, payroll and corporate taxes (`tax`, `employer`, `C`) | × ACS earnings ratio, arrived 50+ / arrived <50, by age band: 0.76 (50–54), 0.70 (55–59), 0.85 (60–64), 0.73 (65–69), 0.92 (70–74), 0.85 (75+) | measured, ACS [DATA: late_arrival_tenure.csv] |
| Social Security + SSI cash and under-reporting (`cash`, `U`) | × late-arrival mean SS+SSI at that age group and years since arrival / mean for all Mexico-born of the age group | measured, ACS |
| Medicare/Medicaid-linked (`medical`, `M`, `N`) | 65+: × 0.65·(Medicare rate ratio) + 0.35·(Medicaid rate ratio), by years since arrival; 55–64: × Medicaid rate ratio | rates measured; the 0.65 Medicare weight assumed (0.75/0.55 in low/high) |
| Unauthorized-only items (`S` state coverage, `E` enforcement) | zero for an LPR | rule |
| Years 0–4 after admission (statutory arm) | no SSI (8 U.S.C. 1612(a)(2) 40-quarter rule, 1613 five-year bar, I-864 deeming); no SNAP; no Medicare (Part A/B buy-in requires five years' continuous LPR residence without 40 quarters) and no federal Medicaid (1613); public care at the lineage lane's priced floor ($1,065 low federal floor / $7,132 central peak state coverage / $17,472 high full coverage, per year from 65; scaled by the Mexico-born 55–64/65+ medical ratio before 65) | statutes [TRAINING-DATA: citations not re-read here]; prices [DATA: lineage_cost_2026_09_19/derived/audit.json senior_pricing] |
| Year 5 on | observed ACS receipt by years since arrival, which embeds naturalisation (8% at 0–4 years, 22% at 5–9, 43% at 20+) and deeming as practised (GAO-09-375: rarely applied) | measured |
| Per-capita shared items (`G`, `P`, `R`, `X`, `I`) | kept at the Mexico-born values; the `statutory_direct` arm drops G, P, R for parent and white alike | ledger convention |

Receipt by years since arrival, Mexico-born 65+ who arrived at 50+ [DATA: late_arrival_tenure.csv]:

| Years since arrival | 0–4 | 5–9 | 10–14 | 15–19 | 20+ |
|---|---|---|---|---|---|
| Medicaid | 28% | 27% | 36% | 38% | 51% |
| Medicare | 54% | 61% | 72% | 75% | 87% |
| SSI | 4.3% | 3.7% | 5.9% | 9.6% | 16.5% |
| Social Security | 30% | 31% | 42% | 48% | 60% |
| Naturalized | 8% | 22% | 25% | 30% | 43% |
| n | 819 | 728 | 1,205 | 1,164 | 2,596 |

(All Mexico-born 65+: Medicaid 33%, Medicare 88%, SSI 8.9%, SS 69%.) Receipt inside the first
five years is not zero in the survey: some late arrivals are refugees, returning earlier migrants
or other classes, and state-funded plans count as HINS4.

**Result, statutory arm, central case, Hispanic survival for the parent and NH-white for the
white resident** (thousands of 2024 dollars; negative = net cost to all governments):

| Admitted at | NPV of the parent, 0% | at 3% | Same-age white resident's remaining lifetime, 0% | at 3% | Parent minus white, 0% | at 3% |
|---|---:|---:|---:|---:|---:|---:|
| 55 | −525 | −270 | −397 | −155 | −128 | −114 |
| 60 | −478 | −275 | −491 | −274 | +13 | −1 |
| 65 | −437 | −286 | −598 | −422 | +161 | +136 |
| (45) | −569 | −224 | −183 | +64 | −385 | −287 |
| (50) | −552 | −249 | −288 | −36 | −264 | −213 |

Ranges across cases (low–high bar price and Medicare weight), statutory arm: at 55 −$503k to
−$553k (0%), −$255k to −$290k (3%); at 60 −$459k to −$504k, −$261k to −$295k; at 65 −$400k to
−$496k, −$254k to −$339k. The observed arm (no statutory overrides) lands within $2k of the
statutory central value at 55 and 60 and $16k more costly at 65 (−$453k, 0%). With common US-total
survival for both, the 0% values are −$457k (55), −$415k (60), −$381k (65). Taxes and programs
only (`statutory_direct`, dropping the per-capita general-government items G, P, R for both):
−$343k (55), −$323k (60), −$308k (65) at 0%; −$152k, −$169k, −$194k at 3%
[DATA: derived/per_admission.csv].

**How to read it.** The admission's own fiscal value is the parent's NPV: without the admission
there is no one, so a Mexican parent admitted at 55–65 is a remaining-lifetime net cost of
about $440–530k undiscounted and $270–290k at 3%. A parent admitted at 55 works (employment 60%
at 55–59, earnings 70% of earlier Mexican arrivals of the same age) and roughly breaks even
until 65 (−$0.7k to −$1.1k a year), then costs $18k a year at 65–74, rising to $30k a year at
80+ (a parent admitted at 65 costs $11k a year during the five-year bar) as Medicaid, SSI and Medicare receipt climb with tenure and naturalisation.
The white comparison asked for in the brief cuts the other way at 60–65: a white 65-year-old
draws more Social Security and Medicare than the parent (white 65–74 net −$23.5k a year), so the
parent's remaining lifetime is less costly than the white retiree's by $136–161k. That
comparison does not describe the admission: the white retiree's deficit is the tail of a
working life that paid in, while the parent's working life was spent in Mexico. Against the
parent's own admission, the right benchmark is zero; against a same-age white resident, the
parent costs more at 55 and less at 65.

The number matches the only official costing found for a comparable visa: Australia's
Government Actuary put the lifetime net fiscal cost of a parent-visa holder at A$335–410k
present value in 2015 (≈ US$250–310k at about 0.75 US$/A$ [TRAINING-DATA]) [SOURCE: Productivity Commission 2016, p. 478, via
reads/offset_reads.md §6], against $254–339k at 3% here for admission at 65.

What is not in it: the sponsor household's own taxes and benefits (a co-resident parent can
raise household size for SNAP and Medicaid eligibility of the family, or free the daughter to
work, section 5); return migration (none assumed;
the NIS and ACS both show many parents living with their children, 48% as the householder's
parent); and real growth in health costs (none, per the ledger convention). The earnings ratio
for the 45 and 50 arms borrows the arrived-50+ ratio.

## 4. Scale: a year of Mexican IR-5 admissions, valued over their remaining lives

Script `scale.py` → `derived/flow_valuation.csv`. This is a flow valuation: the NPV of one
fiscal year's admissions over the rest of their lives. It is **not** an annual-account line; the
complete annual account already contains every Mexico-born resident at every age, these parents
included, and adding it to the annual total would double count.

Age mix at admission (IR-5 age by country is unpublished): `fy2024_central` puts 38% at 55+
(section 1), with NIS-2003 Mexican proportions inside the <55 and 55+ groups; `fy2024_upper`
48%; `nis2003` the 2003 Mexican mix (75% at 55+). Arrivals under 50 are valued at 45 and those
at 65+ at 65.

| Statutory arm, Hispanic survival | FY2024 flow (63,050) | FY2015–2024 mean flow (36,652) | Mean per parent |
|---|---:|---:|---:|
| Central, 0% | −$33.1bn | −$19.2bn | −$525k |
| Central, 3% | −$15.9bn | −$9.2bn | −$252k |
| Low–high, 0% | −$31.4 to −$35.4bn | −$18.3 to −$20.6bn | |
| Low–high, 3% | −$14.7 to −$17.6bn | −$8.5 to −$10.2bn | |
| Taxes and programs only (central), 0% / 3% | −$20.9bn / −$8.3bn | −$12.2bn / −$4.8bn | −$332k / −$132k |

The age mix barely matters (FY2024 flow at 3%: −$15.9bn central mix, −$16.2bn upper, −$17.0bn
NIS mix): Mexican parents admitted younger work longer before 65 but live longer after it, and
at 0% the younger mix is slightly more costly. The FY2024 cohort of Mexican parents carries a
remaining-lifetime net cost of about $16bn at 3% ($33bn undiscounted); a typical year of the last
decade, $9bn ($19bn) [DATA: derived/flow_valuation.csv].

## 5. Disconfirmation: do sponsored parents pay their way through childcare?

Full notes with verbatim quotes and page citations: `reads/offset_reads.md` (researcher lane;
Hu 2018 Table 3 re-checked against the primary PDF here: "Parent present in the same household
… 0.074*** (0.004)" for foreign-born mothers, −0.042 for natives, 0.062 for the ≤HS group, p. 105–106).

| Study | Sample | Design | Effect on the adult daughter's work |
|---|---|---|---|
| Hu 2018, RSF 4(1) | US foreign-born mothers of a child <6, CPS 2006–14 | correlational (120 group dummies; the IV is weak, coefficient 4.7) | co-resident parent +7.4 pp participation (≤HS mothers +6.2 pp); natives −4.2 pp; no hours estimate (Table 3, pp. 105–106) |
| Posadas & Vidal-Fernández 2013, IZA JLP | US mothers of a child 0–3, NLSY79 | women's fixed effects; IV imprecise | +9 pp when a grandparent actually provides care (OLS +16) (§5, Table 3) |
| Compton & Pollak 2014, JUE | US married women, NSFH; excludes grandmothers abroad | reduced form + IV | +4 to +10 pp for living near mother/mother-in-law; own mother only n.s.; co-resident single mothers −7.3 pp, −4.1 h/week (p. 1, Table 4 p. 34) |
| Frimpong & Compton 2023 (thesis ch. 1) | Canadian immigrant mothers, LAD 1983–2005 | triple difference on the 1995 shift away from family class; no first stage | −2.4 pp (family class) to −14 pp (refugees) employment when fewer parents were admitted (Table 1.3, p. 20) |
| IRCC 2024 evaluation | Canadian PGP sponsors, arrivals 2014–19 | self-report, 17.8% response | 10% "able to return to work", 20% "work more hours" (p. 29) |
| Productivity Commission 2016 | Australian parent-visa holders, 2011 census link | measured prevalence | only 18.7% (non-contributory) / 26.1% (contributory) provide any unpaid care for others' children (Table 13.4, p. 473) |

The offset is real in sign and small in size. The best immigrant-specific US figure is a +6 to
+7 pp participation association for a mother with a preschooler, with no hours estimate and
endogenous co-residence (the authors of the newest US study, Bansak–Dziadula–Zavodny 2026, read
it partly as parents being brought over because care is needed). It applies only in the years a
grandchild is under about 6, and only a fifth to a quarter of parent-visa holders provide care
at all (Australia). At $20–25k a year for a low-skill mother who works [ASSUMPTION], +6–7 pp is
$1,200–1,900 of gross earnings a year per co-resident parent in preschool years; the public
account gains only the tax on that, roughly $120–380 a year, or less inside the EITC phase-in
[CALCULATION/INFERENCE in reads §9]. Against the per-parent net costs in section 3 this is one to
two orders of magnitude smaller. Australia's Productivity Commission reached the same judgement
on its own parent visas, costing a parent-visa holder at A$335–410k present value (best ≈ A$370k,
p. 478) and calling the childcare saving "a small fraction" of the A$13.8k/yr KPMG figure it
rejected (pp. 472–473).

The cost side has independent support: GAO-09-375 found sponsor deeming "seldom or never"
applied in 69% of states and SSA never pursuing sponsor repayment of SSI (pp. 11, 24), and
Canada's PGP evaluation found social assistance "spiking following the termination of the
undertaking" (IRCC 2014 executive summary).

Not found: any Mexico- or Hispanic-specific estimate; any causal per-parent estimate for
immigrants in the US; SSA/CRS tables of SSI take-up by naturalised former IR-5 parents.

## Run, gates and files

```sh
# from the repository root
uv run --no-project --with xlrd --with openpyxl --with pandas python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/flow.py
uv run --no-project python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/acs_late_arrival.py   # offline from _cache/acs
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/per_admission.py
uv run --no-project python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/scale.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/late_arrival_tail_2026_09_27/verify.py
```

`verify.py`: 7/7 gates pass — ACS vs B05006 within 1% (max 0.59%); IR-5 flow gates 128/128;
IR-5 all-country Total equals Yearbook Table 6 Parents FY2005–2024; ledger loaders run without
`[BLOCKED]`; the pooled arm reproduces the ledger's survival NPVs (max $0.05); per_admission.csv
complete (400 rows); flow valuation present. A rerun of flow.py, per_admission.py and scale.py
reproduced every derived CSV/JSON byte-identically (all rc=0); the ACS script was rerun
byte-identically by its worker.

Specifications computed and reported: arrival ages 45, 50, 55, 60, 65; arms pooled_profile,
observed_late, statutory, statutory_direct; cases low/central/high; survival group-specific and
common-total; real rates 0, 2, 3, 5% (all in per_admission.csv; the tables above show 0% and 3%);
flow mixes nis2003, fy2024_central, fy2024_upper × flows FY2024 and FY2015–2024 mean
(flow_valuation.csv).

Files covered: every file in this directory. Inputs read, not edited: the OHSS major-class
workbooks (FY2005–2022 in `sources/`, FY2005–2024 cached here), Yearbook LPR workbooks FY2023
and FY2024 (read from `indian_ledger_2026_09_18/_cache/`) and FY2013 Table 6 (cached here), the
expanded Tables 8–11 FY2023–2024, 80 OHSS country profiles (Mexico, India, China, Philippines,
FY2005–2024), NIS-2003 DS0002/DS0003 from the ICPSR zip, `ledger_absolute_2026_09_17` (through
its loaders), `lineage_cost_2026_09_19/derived/audit.json`. Skipped: IR-5 new-arrival vs
adjustment split by country (not published); the 2020 ACS 1-year PUMS (not on the API); a
Mexico-specific childcare labor-supply estimate (none found); SSA tables of SSI by naturalised
former IR-5 parents (not found). `reads/offset_reads.md` is the researcher's source record;
`_cache/` (ignored) holds raw pulls and `acs_agent_result.md`.

## Revision 2026-09-27 (evening): the Medicare residence clock for adjusters

A conceptual audit (3db388d, relayed by the 1c session) flagged `per_admission.py`'s docstring,
"five years' continuous LPR residence" to buy into Medicare without 40 quarters. SSA POMS
GN 00303.800 A.4 reads: "the alien must have continuously resided in the U.S. for the 5-year period
immediately preceding the month of effective enrollment … The alien need not have had LAPR status
during this 5-year period" [SOURCE: https://secure.ssa.gov/poms.nsf/lnx/0200303800, fetched
2026-09-27]. For a new arrival, which is what `per_admission.csv` values, residence and LPR status
start together, so no number here changes. For a parent adjusting inside the US after 5+ years of
residence, the Medicare buy-in is available from the month of adjustment. The five-year bars on SSI
and federal Medicaid (8 U.S.C. 1613) run from the date the person gained qualified status
[TRAINING-DATA; not re-read]. This belongs to the adjuster (eligibility-change) variant, which is not
computed. Ladder 235 already reads the per-admission values as upper bounds for adjusters.
