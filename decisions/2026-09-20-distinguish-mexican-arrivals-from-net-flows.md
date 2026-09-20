# 2026-09-20: Distinguish continuing Mexican arrivals from net migration

## Context and decision

The user challenged the claim that Mexican low-skill immigration is mostly a
historical question. The frontier memo's September 19 entry described a population
whose inflow ended. Withdraw that statement: the held data directly measure
continuing recent-arrival resident cohorts. [MEASUREMENT / INFERENCE]

## Evidence and alternatives

The [existing ACS output](../infra/immigration-fiscal/arrival_cohorts_2026_09_18/derived/acs_recent_arrival_origin_mix.csv),
row `survey_year=2024, arrival_window=2021-24`, estimates about 555,000 foreign-born
Mexico-born residents aged 25–54 reporting entry during that window. The
[producer](../infra/immigration-fiscal/arrival_cohorts_2026_09_18/acs_cohorts.py)
uses `NATIVITY=2`, `POBP=303`, entry year and person weights. This is a survey
estimate of residents observed in 2024, not gross arrivals or net migration;
deaths, subsequent departures, coverage error and return-entry reporting matter.
No sampling interval is supplied by this short descriptive check. [SOURCE]

A declining origin share or roughly flat stock can coexist with arrivals and
departures. Neither licenses the alternative interpretation that arrivals ended.
No verified continuous annual post-2010 bilateral net series was located in the
inspected arrival-cohort and population lanes. Net-flow claims require compatible
inbound/outbound populations and periods, or an explicit stock/mortality model.
The ACS snapshot alone cannot supply that missing quantity. [INFERENCE / GAP]

## Revisit if

Aligned US and Mexico-side flow data support a dated net-migration estimate.
Such an estimate would refine net flows without erasing observed resident cohorts.
No fiscal balance or causal immigration-effect estimate changes here.

## Supersedes

Item 3's ended-inflow statement in the September 19 addition to the
[research frontier](../research/immigration-research-question-frontier-2026-09-17.md).
The historical wording is retained under its dated correction.
