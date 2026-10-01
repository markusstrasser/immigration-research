# School demand associated with unauthorized immigration, 1975–2025

**Scope:** a first approximation of public-school demand during 1975–2025,
including births in the United States and subsequent maternal descendants.
The user clarified that “low skill” meant **unauthorized**, all origins.
No education or ethnicity filter is used. This is a **partial reconstruction**,
not all descendants, not a count of all people caused by post-1975 arrivals,
and not a net fiscal balance. [FRAMING-SENSITIVE]

## Reproduce

```sh
uv run --no-project --with matplotlib python3 infra/immigration-fiscal/school_growth_1975_2025_2026_10_02/build.py
```

Outputs: `derived/school_burden.png`, `.svg`, `annual_scenarios.csv`, `audit.json`.
The build verifies age windows, cohort conservation, totals, source anchors,
finite values, ordered scenarios and source hashes. Derived files are ignored.

## Sources and measured inputs

- [Pew March 2026 birth table](https://www.pewresearch.org/chart/sr_26-04-31_birthrightscotus/):
  `inputs/pew_births.csv`, 34 annual rows, 1990–2023, source units **thousands**.
  Exact published table, first numeric column: births to unauthorized mothers.
  Examples: 120,000 in 1990; 380,000 in 2006; 300,000 in 2023. Pew estimates
  immigration status using augmented surveys; these are not individually
  observed legal-status birth records. Counts are rounded to 5,000. [SOURCE]
- [Pew August 2025 report, printed p14](https://www.pewresearch.org/wp-content/uploads/sites/20/2025/08/RE_2025.08.21_Unauthorized-Immigrants_REPORT.pdf):
  unauthorized foreign-born under-18 stock: 1.1m in 1995, 1.4m in 2000,
  1.5m in 2007, 0.7m in 2015, 0.8m in 2021, 1.5m in 2023. These are
  children, not enrolled pupils. Pew's broad definition includes some people
  with temporary protection, asylum claims and parole. [SOURCE]
- [Census FY2024 school finance release](https://www.census.gov/newsroom/press-releases/2026/school-system-finances.html):
  national current spending $17,619 per pupil. Build reads the precise
  $17,619.389 from the existing `gen_ledger_extension_2026_09_16/`
  `census_assf_fy2024_summary_tables.xlsx`, sheet8, United States row. [DATA]
- [Census historical migration methods](https://www.census.gov/library/working-papers/1992/demo/POP-twps0001.html):
  approximately 1m net unauthorized arrivals enumerated from 1975–1980,
  or 200,000/year. Extending this rate and a constant birth ratio is our
  assumption, not a Census birth series. [SOURCE]

## Model

The central calculation ages every birth cohort into ages5–17, assumes90%
public-school participation, and annual survival/residence retention of99.5%.
Pre1990 births equal `(year−1975) × 200,000 × (120,000 / 3,500,000)`.
The denominator is Pew's1990 unauthorized-population estimate. This early
back-cast is illustrative and starts at zero by construction. It omits the
pre-existing population and descendants of pre1975 births. [CALCULATION]

Each subsequent maternal generation has a50% female share,2.0 lifetime births
per woman and a discretized Gaussian maternal-age profile18–40, centered29,
standard deviation4, normalized to sum1. Parent survival/residence retention
applies before giving birth, then each new child has its own retention schedule.
Repeat for every generation that can reach school age by2025. Only the maternal
line is followed: a child's mother uniquely assigns its generation, so the
birth categories cannot double-count the same child. [ASSUMPTION]

Foreign-born child counts interpolate between the listed stocks; the pre1995
line starts at zero in1975. A13/18 school-age share and90% public participation
convert under18 stocks into modeled pupils. The2023 stock is held constant
through2025 in the central case. This is a scenario, not a2025 observation.
No recent annual births beyond2020 affect school demand by2025. [ASSUMPTION]

Low/high scenarios jointly vary public participation85–95%, annual retention
98.8–99.8%, later-generation fertility1.6–2.4, maternal-age center32–26,
pre1990 births0.5–1.5 times central, school-age share of foreign minors65–85%,
and foreign-born under18 stock in2025 from1.2m to1.8m. Early foreign-child
uncertainty tapers to the1995 anchor. These are **chosen sensitivity scenarios**,
not confidence bounds or an empirical bound on total attribution. [ASSUMPTION]

Spending equals pupils times the same FY2024 price in every year. This isolates
school places at one unit price; it is **not actual historical spending** or a
historical cost series adjusted for inflation. It excludes capital construction,
debt service, cost differences between districts and any extra language-service
cost. It does not subtract taxes paid by these families. [CALCULATION]

## Limits and disconfirmation

The [Pew article](https://www.pewresearch.org/short-reads/2026/03/31/about-9-of-us-births-in-2023-were-to-unauthorized-or-temporary-legal-immigrant-mothers/)
explicitly warns that accumulated births are not resident stock: children leave
or die and parental status changes. Retention is consequently modeled here.
Current-parent-status counts cannot validate all children born under a past
status. Births to legal mothers with unauthorized fathers, births after a mother
legalizes, formerly unauthorized foreign-born pupils and descendant branches
through US-born fathers are excluded. These omissions mean incomplete coverage;
they do **not** make every modeled number a proven lower bound. [INFERENCE]

The arrival dates of birth-cohort parents are not identified, so some1990+
births may have pre1975-arrival parents. No counterfactual native fertility,
replacement legal migration or endogenous school policy is estimated. The
graph cannot establish how much national enrollment would actually fall under
a no-unauthorized-immigration policy. Citizenship/intermarriage do not mechanically
determine future fiscal outcomes. [INFERENCE]

This is an LLM-assisted analysis of a politically contentious question. The
auditable source table, explicit choices and separate gross-cost definition
are intended to expose framing and modeling choices rather than hide them.

## Scope-change receipt

`acquire.py` and `request.json` preserve IPUMS extract18, submitted before the
user clarified the scope. It requested parent links and schooling for an
education-based analysis. It is **unused** here; Census microdata do not directly
identify unauthorized status. No raw microdata download is needed for this graph.
