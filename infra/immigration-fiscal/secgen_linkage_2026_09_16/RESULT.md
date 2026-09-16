claude-opus-5[1m]

**Verdict:** COMPUTABLE-BUT-UNRUN, and the repo memo's premise survives with one correction. No published or
downloadable estimate exists of incarceration, arrest or conviction for US second-generation adults by parents'
country of birth against third-plus-generation whites, from any linked administrative source. The Opportunity
Insights restricted file does contain both ingredients for the 1978-83 birth cohorts — parents' country of origin
(from the 2000 Census long form / 2005-2015 ACS) and the child's 2010 institutionalization record — and the public
release of the country-of-origin cut carries **income rank only**. Correction to memo §9: Abramitzky, Boustan,
Jácome & Pérez did not themselves hold that microdata. They used aggregated statistics Opportunity Insights had
cleared out of Census (CBDRB-FY18-195), so "re-run it with incarceration" is a new Census-side tabulation or FSRDC
project, not a rerun of their replication package.

# Second-generation incarceration by parental country of birth — source audit

Lane: `/Users/alien/Projects/immigration-research/infra/immigration-fiscal/secgen_linkage_2026_09_16/`
Date: 2026-09-16. Question from team-lead: does any published/downloadable estimate of incarceration (or
arrest/conviction) exist for US second-generation adults BY PARENTS' COUNTRY OF BIRTH (esp. Mexico) vs
third-plus-generation whites, ideally at equal parental income, from linked administrative data?

## 1. Candidate source table

| Source | Links child outcome to parents' birthplace? | Carries incarceration? | Both at once? | Public? |
|---|---|---|---|---|
| OI "Race and Economic Opportunity" Online Tables 6a/6b | YES (51 countries + USA, 1978-83 cohorts) | NO (income rank only) | NO | YES, CSV/DTA |
| OI incarceration tables (same project) | NO (race x gender x geography x parent income) | YES | NO | YES |
| Chetty, Hendren, Jones & Porter 2020 paper/appendix | NO nativity split published | YES | NO | paper + Dataverse |
| Abramitzky, Boustan, Jácome & Pérez 2021 AER (openICPSR 120490) | YES, but its modern cohort IS the OI table above | NO | NO | gated (Cloudflare) |
| Abramitzky, Boustan, Jácome, Pérez & Torres, AERI 2024 (Law-Abiding Immigrants) | NO — first-generation vs US-born only | YES, 1870-2020 | NO | YES |
| CJARS / Justice Outcomes Explorer (JOE) 2022 vintage | NO — demographics are age, sex, race_ethnicity | YES | NO | YES |
| Finlay, Mueller-Smith & Street, QJE 2023 | survey-to-CJARS child-parent links exist, direction reversed | YES | unverified [GAP] | paper |
| Rumbaut et al. 2006 (CILS + 2000 Census) | ethnicity/ancestry proxy, not parental birthplace | YES (institutionalization) | proxy only | YES |
| Bersani 2013/2014, Bersani & Wy 2025, Inkpen 2024, Piquero et al. 2014 | YES (survey-reported parental nativity) | self-report only, single cohort | survey, not admin | YES |
| Add Health Wave V public use | probably [TRAINING-DATA], unverified | self-report | not admin | ICPSR 21600 |

## 2. Opportunity Insights country-of-origin tables — the exact variable list

[SOURCE: https://opportunityinsights.org/data/ , section "Race and Economic Opportunity in the United States:
An Intergenerational Perspective"]

- Online Table 6a (parametric): https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6a_parametric.csv
  (also `.dta`); codebook https://opportunityinsights.org/wp-content/uploads/2019/08/Table6a.pdf . 51 rows, one per country, plus USA.
- Online Table 6b (non-parametric, by parent income ventile): https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6b_nonpar.csv
  (also `.dta`); codebook https://opportunityinsights.org/wp-content/uploads/2019/08/Table6b.pdf . 444 country x ventile rows.

Table 6a header, verbatim and complete:
```
country,n_kfr_P,kfr_P_p25,kfr_P_p25_se,kfr_P_p75,kfr_P_p75_se,n_kir_F,kir_F_p25,kir_F_p25_se,
kir_F_p75,kir_F_p75_se,n_kir_M,kir_M_p25,kir_M_p25_se,kir_M_p75,kir_M_p75_se,
age_in2015_mom_P,age_in2015_dad_P,age_in2015_mom_F,age_in2015_dad_F,age_in2015_mom_M,age_in2015_dad_M,
us_yrs_before_mom_P,us_yrs_before_dad_P,us_yrs_before_mom_F,us_yrs_before_dad_F,us_yrs_before_mom_M,us_yrs_before_dad_M
```
Table 6b header: `par_ventile,country,n_kfr_P,kfr_P,n_kir_F,kir_F,n_kir_M,kir_M`

Outcomes are child family income rank (`kfr`) and child individual income rank (`kir`), at parent percentile 25
and 75, by gender. Nothing else. No incarceration, no employment, no education, no marriage, no teen birth.
Covariates published alongside are parental age in 2015 and years in the US before the child's birth.

Country list (52 rows): ARGENTINA, AUSTRIA, BRAZIL, CAMBODIA, CANADA, CHILE, CHINA, COLOMBIA, CUBA, DOMINICAN
REPUBLIC, ECUADOR, EGYPT, EL SALVADOR, FRANCE, GERMANY, GREECE, GUATEMALA, GUYANA, HAITI, HONDURAS, HONG KONG,
HUNGARY, INDIA, IRAN, IRAQ, IRELAND, ISRAEL, ITALY, JAMAICA, JAPAN, LAOS, LEBANON, MEXICO, NETHERLANDS,
NICARAGUA, NIGERIA, PAKISTAN, PANAMA, PERU, PHILIPPINES, POLAND, PORTUGAL, SOUTH KOREA, SPAIN, TAIWAN, THAILAND,
TRINIDAD & TOBAGO, UNITED KINGDOM, USA, VIETNAM, YUGOSLAVIA.

Mexico and the USA benchmark row, 6a: MEXICO n_kfr_P=122,000, kfr_P_p25=0.4320, kfr_P_p75=0.5540;
USA n_kfr_P=5,615,000, kfr_P_p25=0.4118, kfr_P_p75=0.5967. [SOURCE: race_table6a_parametric.csv, read this session]

Codebook text establishing the linkage, verbatim (Table6a.pdf): "The underlying sample used to construct these
statistics consists of children born between 1978-1983. We obtain country of origin for the parents using the
2000 Census Long Form or the 2005-2015 ACS, prioritizing the country of origin of the father." Cleared
CBDRB-FY18-195; countries with fewer than 500 children suppressed.

Two limits on the "USA" row: it pools all US-born parents, so it is neither white-only nor third-plus-generation.
The published contrast the repo wants (Mexican second generation vs third-plus non-Hispanic white, at equal
parental income) does not exist even for **income**, let alone incarceration.

## 3. What the Opportunity Insights infrastructure holds but has not released

OI's incarceration products are all race x gender x geography x parent income:
"Household Income and Incarceration for Children from Low-Income Households by Census Tract / County /
Commuting Zone, Race, and Gender", and "All Outcomes by Census Tract, Race, Gender and Parental Income
Percentile" [SOURCE: https://opportunityinsights.org/data/ , same section]. No nativity dimension anywhere in
the data library; the only nativity-adjacent product is Online Data Table 3, "National Child and Parent Income
Transition Matrices by Race and Gender for Children with Mothers Born in the U.S." — a restriction, not a
breakout, and it is an income table.

The incarceration variable in that project is measured from the 2010 decennial institutionalization record for
the same 1978-83 cohorts (ages 27-32 on Census Day) [TRAINING-DATA — the definition is not re-verified from the
CHJP 2020 text this session; the existence of the incarceration tables is [SOURCE: data library page]].
Since parents' country of origin is already attached to these cohorts inside Census for Table 6a, a
country-of-origin x parental-income-percentile incarceration tabulation is a disclosure request against a file
that already exists. Nobody has published it.

## 4. Abramitzky, Boustan, Jácome & Pérez — what the replication package can and cannot contain

[SOURCE: NBER WP 26408 PDF, read this session; published as AER 111(2):580-608, 2021]

The paper's own data section, verbatim: "The third cohort includes first-generation immigrants observed around
1980 and their children who are participating in the contemporary labor market... For this cohort, we use two
sources of data. First, we use publicly available administrative data linking parents and their 2.7 million sons
using federal income tax returns from the Opportunity Insights project (Chetty et al. 2018a, 2018b)." And later:
"the Opportunity Insights data are available only in aggregate form."

So the modern-cohort input to that AER paper IS the public Table 6a/6b above. Its replication package
(openICPSR project 120490, https://www.openicpsr.org/openicpsr/project/120490/view ) can therefore only contain
income-rank country aggregates for the modern cohort plus linked historical census extracts for 1880/1910/1940,
where the outcome is an occupation-based income score, not incarceration.
[GAP] The openICPSR file listing itself is unverified: the site sits behind Cloudflare bot management and
returned HTTP 403 to both WebFetch and a browser-UA curl. Per repo memory this wall is not beatable with
agent-browser. Verification would need an operator-side login. The inference above rests on the paper's own
text, which is strong but is not the file manifest.

Their sequel, "Law-Abiding Immigrants: The Incarceration Gap between Immigrants and the US-Born, 1870-2020"
(Abramitzky, Boustan, Jácome, Pérez & Torres, AER: Insights 6(4), Dec 2024; NBER WP 31440;
https://www.aeaweb.org/articles?id=10.1257/aeri.20230459 , PDF at
https://ranabr.people.stanford.edu/sites/g/files/sbiybj26066/files/media/file/immigration_incarceration_jan2024.pdf )
does have incarceration and does span 1870-2020, but it is **first-generation immigrants vs the US-born**
throughout. Grep of the full text finds no second-generation incarceration series and no by-parental-origin cut.
Parental country of birth appears once, in the notes to Appendix Figure A11, only to explain that IPUMS's pre-1980
`Hispan` variable is built from "country of birth, parental country of birth, Spanish surname, or relationship to
someone identified as Hispanic" — used to construct a non-Hispanic-white US-born comparison group, not a
second-generation group. Their comparison rows are: all US-born, white US-born, non-Hispanic white US-born,
non-Black US-born. [SOURCE: PDF read this session, Figure A11 notes and Figure 1]

That is a notable miss, because the 1880-1940 full-count censuses they already use **do** record both parents'
birthplaces, so a second-generation-by-parental-origin incarceration series for 1880-1970 is computable from
public IPUMS data with no restricted access at all. It is simply not in the paper.

## 5. CJARS and the Justice Outcomes Explorer — no nativity

[SOURCE: https://www.census.gov/programs-surveys/cjars.html ; JOE at https://joe.cjars.org/ ]

The JOE 2022 public state-level files expose exactly these variables
[SOURCE: https://www2.census.gov/programs-surveys/cjars/technical-documentation/file-layouts/2022/cjars_joe_2022_st_variable_metadata.json , read this session]:
```
geoid, geo_name, state_fips, estimation_type, estimation_type_label, cj_event_type, cj_event_type_label,
cj_event_year, cj_event_window_length, outcome_type, outcome_type_label, outcome_year, outcome_period,
offense_type, offense_type_label, repeat_contact, repeat_contact_label, age_group, age_group_label,
sex, sex_label, race_ethnicity, race_ethnicity_label, statistic
```
Outcome codes present: `any_w2`, `w2_wages`, `above_poverty`, `medicaid`, `medicare`, `ssi`, `hud`, `mortality`,
`inc_exit`, `par_bgn`, `pro_bgn`, `adj_fe_chrg`, `adj_mi_chrg`. Demographics are age group, sex and
race/ethnicity only. **No nativity, no place of birth, no parental variables.** JOE is also the wrong direction
of causality for this question: it conditions on justice contact and reports later economic outcomes.

The design-relevant CJARS paper is Finlay, Mueller-Smith & Street, "Children's Indirect Exposure to the U.S.
Justice System: Evidence From Longitudinal Links between Survey and Administrative Data", QJE 138(4), 2023,
https://doi.org/10.1093/qje/qjad021 . It builds exactly the linkage a second-generation study needs — survey
household rosters (which carry each parent's place of birth) joined by protected identifier to CJARS criminal
histories — but it runs the link the other way, from parents' justice involvement to children's exposure.
[GAP] Not verified this session whether it reports any nativity split; the NBER number I tried (w30181) is a
different paper. Next query: "Finlay Mueller-Smith Street children indirect exposure CES working paper" and the
Census CES working paper index for 2022-2026 with terms "CJARS nativity", "CJARS immigrant".

No Census CES working paper linking CJARS to parental birthplace surfaced in this session's searches. Recording
that as a provisional VERIFIED NEGATIVE with the caveat that the CES working-paper index was not enumerated
directly. [GAP]

## 6. What is actually published on second-generation crime by origin

Everything published is survey self-report on a single cohort, or ethnicity-proxy rather than parentage:

- Rumbaut, Gonzales, Komaie, Morgan & Tafoya-Estrada 2006, "Immigration and Incarceration: Patterns and
  Predictors of Imprisonment Among First- and Second-Generation Young Adults",
  https://escholarship.org/uc/item/8798n03x — closest published thing. National-level incarceration of young men
  18-39 by nativity and national origin from the 2000 Census institutional GQ record, plus CILS San Diego panel.
  The 2000 Census has no parental birthplace, so its "second generation" national-origin cut is built from
  ethnicity/ancestry, not parentage, and CILS has no third-plus-generation white comparator.
- Bersani 2014 (first- and second-generation offending, NLSY97); Bersani & Wy 2025, "Assimilating into Crime?
  Explaining the Generational Disparity in Immigrant Offending", https://doi.org/10.1080/07418825.2025.2534405 ;
  the within-family design, https://doi.org/10.1177/0022427819850600 ; Inkpen 2024, "Differences in Time to
  Reported First Arrest by Race, National Origin, and Immigrant Generation", https://doi.org/10.1177/00111287231225125
  (already in the repo memo §6); Piquero, Bersani, Loughran & Fagan 2014, https://doi.org/10.1177/0011128714545830 .
  All self-report, one cohort, a few hundred Mexican second-generation men, no administrative outcome.

## 7. Add Health Wave V — unverified

[GAP] Not verified this session. The public-use series is ICPSR 21600 (https://www.icpsr.umich.edu/web/DSDR/studies/21600/variables),
and the Add Health Codebook Explorer at https://addhealth.cpc.unc.edu/documentation/ searches Wave I-V in-home
questions by variable name. That parental nativity is on the Wave I parent/in-home instrument and that
arrest/incarceration self-reports are on the Wave IV and V instruments is [TRAINING-DATA] and must be confirmed
against the codebook before any citation. Note ICPSR also sits behind the bot wall, so the ACE explorer or a
downloaded codebook PDF is the route. Even if confirmed, this is survey self-report on the 1976-82 cohort, not
linked administrative data, and the public-use subsample is small for a Mexican-parentage x male cell.

## 8. What an FSRDC proposal would need

The cheapest credible path is not a new linkage but a disclosure request against a file that already exists.
Opportunity Insights' cleared extract for the 1978-83 birth cohorts already carries, per person, the tax-record
parent-child link, parent household income averaged 1994-2000 and ranked within cohort, each parent's country of
birth from the 2000 Census long form or 2005-2015 ACS, the child's race and Hispanic origin from the census
short form, and the child's 2010 institutionalization status. A proposal would ask for one new table: mean
incarceration rate by parents' country of origin x parent income ventile x child gender, with a third-plus
non-Hispanic white comparison cell built from children whose parents are US-born, non-Hispanic white, and
themselves have US-born parents where observable. That last condition is the binding constraint: **third-plus
generation is not directly observable** in 2000-2015 census instruments, since parental birthplace was last
asked in 1970, so "third-plus white" has to be approximated as "US-born non-Hispanic white parents", which
contaminates the comparison with the white second generation (small) and loses the Mexican-American third-plus
group to ethnic attrition in the Hispanic-origin item. A project would need: an FSRDC proposal with a Census
Bureau sponsor and predominant-purpose justification, Special Sworn Status for all analysts, access to the
IRS-sourced files, which requires IRS approval on top of Census approval and is the usual point of failure for
outside teams, and a Disclosure Review Board release plan with cell-size suppression at 500 children per
statistic, matching the CBDRB-FY18-195 precedent. Realistic timeline is 12-24 months from proposal to cleared
output. The much cheaper fallback, which needs no restricted access at all, is to compute the
second-generation-by-parental-origin incarceration series from the 1880-1970 full-count IPUMS censuses, where
both parents' birthplaces and institutional group-quarters status are on the same public record; that answers
the historical version of the question conclusively and would be a week's work.

## 9. Corrections to repo memo §9

`research/immigration-mexican-origin-by-generation-2026-09-16.md` §9 says: "the Opportunity Insights linkage
that produced the Mexican second-generation earnings result already observes incarceration on 2010 Census Day
for children linked to parents' birthplace and income, so incarceration by parental origin at equal parental
income is computable in that infrastructure today". Substantively confirmed. Two refinements:
1. The Mexican second-generation earnings result reached Abramitzky et al. as a pre-cleared public aggregate,
   not as microdata they could re-cut. The re-cut is a Census/IRS-side request, not a rerun.
2. The comparison group in the public table is "USA", all US-born parents. Third-plus-generation white is not
   observable in the underlying instruments and would have to be approximated.

## 10. Remaining gaps, in priority order

- [GAP] openICPSR 120490 file manifest, blocked by Cloudflare. Needs operator login or an ICPSR-side contact.
- [GAP] Finlay, Mueller-Smith & Street QJE 2023 — does it report any nativity split, and does its survey-to-CJARS
  crosswalk retain parental birthplace? This is the single highest-value follow-up; it is the closest existing
  build of the needed infrastructure.
- [GAP] Census CES working-paper index 2022-2026 not enumerated directly; "CJARS nativity" negative is provisional.
- [GAP] Add Health Wave V public-use variable names unverified.
- [GAP] CHJP 2020 incarceration definition (2010 Census Day institutionalization, ages 27-32) taken from
  training memory, not re-read from the paper.
