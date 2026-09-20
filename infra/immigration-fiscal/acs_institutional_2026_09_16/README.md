# ACS institutional residence by origin and nativity

`pull_and_compute.py` and the adjacent producers measure institutional group-quarters
residence (`TYPE`/`TYPEHUGQ=2`). Public ACS cannot separate criminal custody,
immigration detention, nursing facilities or other institutional types. Do not label
the CSV values crime rates or detention-adjusted incarceration rates.

The Hispanic-origin codes are self-identification, not birthplace. Native-born
categories pool second and later generations. An age range is not exact age
standardization. Reallocating generic Hispanic codes is a sensitivity assumption,
not an observed individual correction. Comparisons with a historical correctional-only
measure have different outcome coverage.

[Current reporting and cost rule](../../../research/immigration-detention-crime-and-fiscal-scope-2026-09-20.md)
governs downstream cost, institutional-bound and lineage scenarios. Counts remain
reproducible; this correction changes their interpretation, not their values.

[Source: ACS 2024 dictionary](https://www2.census.gov/programs-surveys/acs/tech_docs/pums/data_dict/PUMS_Data_Dictionary_2024.pdf),
`TYPEHUGQ`, and the variable filters in the producers.
