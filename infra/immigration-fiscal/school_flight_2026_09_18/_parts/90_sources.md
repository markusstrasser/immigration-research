---

## 7. Sources

**Papers.** Full quotes, page numbers and confidence tags are in
`infra/immigration-fiscal/school_flight_2026_09_18/LIT.md`.

- Betts, J. & Fairlie, R. (2003). "Does immigration induce native flight from public
  schools into private schools?" *Journal of Public Economics* 87(5-6), 987–1012.
  [SOURCE: http://people.ucsc.edu/~rfairlie/papers/published/jpube%202003%20-%20native%20flight.pdf]
- Poterba, J. (1997). "Demographic structure and the political economy of public
  education." *Journal of Policy Analysis and Management* 16(1), 48–66; working paper
  NBER WP 5677. [SOURCE: https://www.nber.org/system/files/working_papers/w5677/w5677.pdf]
- Alesina, A., Baqir, R. & Easterly, W. (1999). "Public goods and ethnic divisions."
  *Quarterly Journal of Economics* 114(4), 1243–1284.
- Hopkins, D. (2009). "The diversity discount: when increasing ethnic and racial diversity
  prevents tax increases." *Journal of Politics* 71(1), 160–177.

**Data.**

- ACS 1-year PUMS, 2005–2023, via the Census API `acs/acs1/pums` (children 5–17).
  [SOURCE: https://api.census.gov/data/{year}/acs/acs1/pums]
- Census 2000 SF1 and ACS 5-year county tables for the elderly-share control.
  [SOURCE: https://api.census.gov/data/2000/dec/sf1, .../acs/acs5]
- MCDC Geocorr PUMA→county allocation factors (puma2k, puma12, puma22) and the OMB
  February-2013 metropolitan delineation, both reused from
  `employment_entry_2026_09_18/_cache/`. [SOURCE: https://mcdc.missouri.edu/]
- NCES Common Core of Data and Census F-33 district finance, 2000–2020, via the Urban
  Institute Education Data Portal.
  [SOURCE: https://educationdata.urban.org/api/v1/school-districts/ccd/]
- NCES Digest of Education Statistics 2023, tables 203.50 (public enrolment by race),
  205.10 (private share) and 205.50 (private enrolment and average tuition).
  [SOURCE: https://nces.ed.gov/programs/digest/d23/tables/dt23_203.50.asp and siblings]
- California Elections Data Archive, yearly workbooks, via the `justindbk/ceda` mirror of
  the CSU Sacramento portal. [SOURCE: https://github.com/justindbk/ceda]
- FRED CPI-U annual average (CPIAUCSL) for deflation.
  [SOURCE: https://fred.stlouisfed.org/series/CPIAUCSL]
- BEA, *NIPA Handbook*, Chapter 9, "Government Consumption Expenditures and Gross
  Investment," for the treatment of government output.
  [SOURCE: https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf]

**Repo lanes reused.** `school_angle_2026_09_16` (incumbent-student effects),
`ledger_absolute_2026_09_17` (F-33 and CCD loaders, district cost-to-serve differential),
`employment_entry_2026_09_18` (metro geography, 2000-base shift-share instrument).

**Instrument bias.** This analysis was produced by a language model on a politically
charged topic; see `notes/llm-bias-caveat.md`. The specific risk here is asymmetric
scepticism — applying harder disconfirmation to results that cut one way than the other.
The mitigations used were to preregister the disconfirmation checks in the brief before
looking at any estimate, to report every specification run rather than a selection, and to
write out the aggregate national series in §5.1 that cuts against the hypothesis before
estimating anything.
