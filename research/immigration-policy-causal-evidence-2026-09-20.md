# Policy effects, crime valuation and additional outcome data

**Date:** September 20, 2026. Evidence index and calculation record; narrative writing remains operator-owned.

**Later execution update:** The [raw-data causal checks](immigration-causal-execution-2026-09-20.md)
now supersede the pending Chalfin status below: the existing local archive was found,
validated and executed. Supplied crime outcomes are log-count changes despite
rate-suggesting names. The Mariel total-spending p=.045 below is **one-sided**;
TableA3 operating spending is+.20 log with one-sided p=.09. Independent public-data
reconstruction estimates operating log gaps.161–.194 with weaker two-sided placebo
evidence. These are specification estimates, not a national confidence interval.

**Finding:** Specific policy effects are more defensible than a causal dollar
total for an ethnic-origin population. New primary evidence supports additional
school costs after one immigration shock and increased Hispanic victimization
after one enforcement policy. Existing randomized evidence supports revenue gains
for employers obtaining temporary workers. These effects answer different questions;
they do not cancel or sum into a national number. [INFERENCE from sources below]

The [complete annual account](immigration-complete-annual-account-2026-09-20.md)
remains **$270–289bn/year net cost to other US residents under its source-centered
long-run assumptions**, with the broader $262–357bn sensitivity grid. Neither range
is newly identified by these studies. Different service-response and capital
assumptions can reverse the sign. It covers all ages and education levels among
40.897m current Mexican-origin residents, not just low-skill arrivals. Immigration,
descendant population, enforcement and legal access are different treatments.
[SOURCE: linked account; FRAMING-SENSITIVE]

## Primary findings and transfer limits

### Enforcement: reporting and victimization move differently

Goncalves, Jacome and Weisburst use staggered Secure Communities activation and
confidential county-linked NCVS records, 2006–2015. In Table 2, Hispanic monthly
victimization rises **0.152 percentage points** (SE0.067); reporting among Hispanic
victimization incidents falls **9.446 points** (SE3.664). Approximate normal 95%
intervals are [0.021,0.283] and [−16.627,−2.265]. The non-Hispanic victimization
estimate is 0.003 (SE 0.035), compatible with increases or decreases.
[SOURCE: [Census CES26-23](https://www2.census.gov/library/working-papers/2026/adrm/ces/CES-WP-26-23.pdf), April 2026, Table 2 p.40]

Identification requires comparable untreated trends, no consequential spillovers
or anticipation, and stable measurement. The sample excludes southern-border
counties, three states and small counties. Some alternative estimates are less
precise. This is an enforcement effect on Hispanic residents aged 12+, including
citizens; it is not a Mexican-inflow or descendant-offending effect. NCVS excludes
homicide. The coefficients cannot be priced as additional incident counts, nor
assigned wholly to the fiscal account's other-resident beneficiaries. Public
replication code exists, but the geographic microdata are restricted.
[SOURCE: same paper, sample/design and robustness sections;
[replication record](https://doi.org/10.3886/E242546V1)]

**Consequence:** Police-recorded crime alone can misstate the victim-harm change.
A reduction in reports cannot automatically be treated as a reduction in crime.
[INFERENCE]

### Education: a historical arrival shock raised spending

St. Clair's synthetic-control analysis of the Mariel Boatlift estimates
Miami-Dade school spending **0.25 log points higher**, averaged over 1981–1990
(permutation p=.045). That is a 28.4% geometric difference; the manuscript uses
the 25% approximation. City +.05 (p=.38) and county −.08 (p=.65) estimates do not
establish broad spending increases; county pretreatment fit is weak. Alternative
school specifications give .21–.28, with covariate-adjusted p=.068.
[SOURCE: [August 9, 2024 author manuscript](https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift_5.pdf), Tables 2/4, printed pp.37/39]

This supports real incremental education costs, conditional on a valid synthetic
counterfactual. One Cuban-refugee shock does not identify today's Mexican-origin
population's service-cost response, or a universal variable-cost fraction. The
published article confirms the direction; exact final-table identity is unverified.
CBO's separate enrollment/spending calibration is observational and cannot close
that identification gap. [INFERENCE; SOURCE:
[published article record](https://doi.org/10.1016/j.regsciurbeco.2024.104053),
[CBO Appendix A](https://www.cbo.gov/publication/61464)]

### Production: randomized access helps participating employers

The already-held H-2B lottery paper estimates winning raises log firm revenue by
**.135** (SE .051), about 14.5% geometrically, among 472 responding surviving firm
observations. Revenue is neither profit nor national surplus. Fixed-quota
winner-versus-loser comparisons can include business redistribution; selection
and general-equilibrium effects constrain quota expansion claims. Its US-worker
definition includes permanent residents, not just native-born people. These are
substantive benefits to retain, but no fresh national dollar offset follows.
[SOURCE: Clemens–Lewis, July 2026,
[final institutional reprint](https://www.piie.com/sites/default/files/2026-07/wp26-11.pdf), Table 2,
[publication identifier](https://doi.org/10.1257/app.20250049);
[existing audit](../infra/immigration-fiscal/frontier_execution_2026_09_17/policy/RESULT.md)]

## Direct Mexican-inflow crime replication: earlier status, superseded above

Chalfin (2015) has a small [public replication package](https://doi.org/10.3886/E113382V1):
a 253.3 KB Stata file and 1.7 KB code file. The authenticated download is prepared;
acceptance of ICPSR's binding terms awaits the operator's answer. No inaccessible
file or abstract is described as a completed replication. Its primary abstract
reports lower property crime and higher aggravated assault using Mexican birth
cohorts and migration networks as an instrument. The full original paper and
coefficient tables were not acquired; these qualitative signs remain abstract-only
evidence. [SOURCE: [AEA article record](https://www.aeaweb.org/articles?id=10.1257/aer.p20151043)]

There is a concrete inference risk worth testing. Cullen–Steigerwald's June 2020
draft reports 92 nominal clusters but 11 effective clusters for a selected Chalfin
specification; dropping one cluster changes |t| 2.05→1.29. The inspected passage
does not name its outcome. This neither invalidates all results nor establishes
their robustness. Reproduce the supplied estimator first, then assess weak
instruments, influential clusters and offense-specific uncertainty. Log crime
changes require baseline incidents and compatible covariance before valuation.
[SOURCE: [author-linked draft](https://drive.google.com/file/d/1--EQ3f2bnmSkUyunNKyxKyg7o_xh9hVQ/view), §5.1 and Table 3]

**Contrary enforcement evidence:** Chalfin–Deza (2020) report property-crime
reductions following Arizona's employer-verification law. They attribute the
result to departures of young men, without claiming higher offending than
age/sex-comparable natives. The original abstract supports those statements;
we have not independently checked its tables or replication. This prevents a
blanket claim that all immigration enforcement increases crime.
[SOURCE, ABSTRACT ONLY: [publisher record](https://onlinelibrary.wiley.com/doi/10.1111/1745-9133.12498);
INFERENCE for the last sentence]

## Crime-harm rule

[Source-specific detention/crime scope](immigration-detention-crime-and-fiscal-scope-2026-09-20.md)
specifies which held data can separate civil custody and criminal offenses, and
how federal payments/local receipts are consolidated. ACS institutions cannot
supply a detention-adjusted crime rate.

**An immigration-only violation has no automatic victim-harm price.** A crossing
that uses no enforcement resources and causes no separate harm gets **$0 at that
event**. Real additional enforcement, courts or detention belong in government
costs once; status is not itself a priced injury. This implements the operator's
September 20 accounting instruction. [FRAMING-SENSITIVE]

For a specified intervention and beneficiary population:

```text
victim-harm change = sum(change in incidents by offense × victim-only unit cost)
```

Changes must be relative to a credible counterfactual and can be negative. Police
reports, arrests and victimized person-months are not interchangeable incident
counts. Exclude government-cost components already in the fiscal ledger and
overlapping mortality/earnings valuations. The earlier $13–19bn white-reference
crime scenario includes corrections and does not satisfy this causal population
match; it remains outside the current net account. [INFERENCE; SOURCE:
[aggregate audit](immigration-aggregate-and-generation-audit-2026-09-17.md),
[accounting contract](../infra/immigration-fiscal/causal_evidence_2026_09_20/README.md)]

## Data acquired and validation

Copied **72,120,892 bytes** from `/Volumes/2TBPNY/corpus/`: BEA CAINC4 and 11 IRS
county income CSVs; added 11 official IRS guides. Total staged output is about 80 MB,
well below the 10 GB limit. No originals were moved or deleted. The joined panel has
**34,733 county-year rows**, 2011 and 2013–2022; 2012 is missing. The independent
corrected verifier passed **583,225 source value/label/flag comparisons**, exact
source coverage and missingness checks, **23 input hashes** and six output hashes.
Ten deliberate corruption cases are rejected; this fixes gaps found in the
earlier checker rather than an observed error in the current data values.
[SOURCE: [recipe and checks](../infra/immigration-fiscal/causal_evidence_2026_09_20/CORPUS.md),
[source lock](../infra/immigration-fiscal/causal_evidence_2026_09_20/SOURCES.json)]

IRS amounts and BEA monetary fields are converted from thousands to nominal
dollars. A06500 is income tax liability, not net federal receipts. BEA transfers
include non-government transfers. County boundaries, unmatched geographies and
suppression remain explicit; no invented crosswalk or 2012 interpolation. These
outcomes support future verified policy designs and aggregate reconciliation;
they contain no ethnicity, nativity or treatment variable. Their availability
does not make a county correlation causal. [SOURCE: yearly codebooks and table
metadata, pinned above; INFERENCE]

All six cited DOI identifiers resolved in the mechanical citation check; actual
support and version limits were checked separately against the primary sources.
Arithmetic for ten published-table rows is reproducible with
`causal_evidence_2026_09_20/audit_estimates.py`. It is not microdata replication.
No national cost change is inferred from this round. LLM selection can bias which
papers look salient; adverse cost, favorable production and enforcement-harm
evidence are retained together. [INFERENCE; [instrument note](../notes/llm-bias-caveat.md)]

## Revisions

- Later2026-09-20: locate and execute the already-held Chalfin archive; withdraw
  the unresolved-download status as current. Clarify the Mariel one-sided tests
  and distinguish operating/total spending. Preserve earlier source notes above;
  [executed update](immigration-causal-execution-2026-09-20.md).
