# Education-bucket stock cut and lifetime-status note

Date: 2026-04-11

## Question

What can the repo now say about the size and state distribution of low-skill immigrant stocks by education bucket, and what does it **not** yet support on bucket-specific lifetime fiscal cost?

## Bottom line

The repo now has a clean weighted `ACS` stock cut for foreign-born adults ages `25-64` in three education buckets:

1. `<HS`
2. `HS / GED`
3. `some college / associate`

It does **not** yet have a defensible bucket-specific `lifetime NPV` for those three groups from the current public stack.

That is the correct state of the project. Anything more precise right now would be fake precision. [SOURCE: research/immigration-lifetime-fiscal-data-stack-2026-04-10.md] [SOURCE: research/immigration-public-mvp-readiness-2026-04-11.md] [SOURCE: research/immigration-next-agent-handoff-2026-04-11.md]

## What this cut is

The stock cut uses the local `ACS 2023 PUMS` mirror and weighted person records with:

1. `NATIVITY = 2`
2. `AGEP between 25 and 64`
3. `PWGTP` as the person weight
4. `SCHL < 16` for `<HS`
5. `SCHL IN (16,17)` for `HS / GED`
6. `SCHL IN (18,19,20)` for `some college / associate`

This is a **foreign-born stock** cut, not an undocumented-only estimate, not a recent-surge-only estimate, and not a lifetime fiscal model. [SOURCE: /Volumes/SSK1TB/corpus/census_acs/csv_pus.csv] [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv] [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv]

## National totals

Weighted totals for foreign-born adults ages `25-64` in the three-bucket frame:

| Bucket | Weighted stock | Share of three-bucket total |
|---|---:|---:|
| `<HS` | `4,303,453` | `36.14%` |
| `HS / GED` | `4,115,963` | `34.56%` |
| `some college / associate` | `3,489,226` | `29.30%` |

Total across the three buckets: `11,908,642`. [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv]

## State concentration

Top states as a share of the full three-bucket stock:

1. `CA` `4,915,063` `41.27%`
2. `FL` `2,132,532` `17.91%`
3. `IL` `821,241` `6.90%`
4. `GA` `577,078` `4.85%`
5. `AZ` `482,467` `4.05%`
6. `MA` `482,214` `4.05%`
7. `MD` `416,203` `3.49%`

These seven states alone hold about `82.5%` of the three-bucket stock. [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv] [INFERENCE]

### `<HS`

Top state shares within the `<HS` bucket:

1. `CA` `2,103,057` `48.87%`
2. `FL` `496,003` `11.53%`
3. `IL` `281,762` `6.55%`
4. `GA` `216,120` `5.02%`
5. `AZ` `185,639` `4.31%`
6. `MD` `146,166` `3.40%`
7. `MA` `137,686` `3.20%`

### `HS / GED`

Top state shares within the `HS / GED` bucket:

1. `CA` `1,480,480` `35.97%`
2. `FL` `876,913` `21.31%`
3. `IL` `309,312` `7.51%`
4. `MA` `205,671` `5.00%`
5. `GA` `197,780` `4.81%`
6. `AZ` `168,329` `4.09%`
7. `MD` `140,793` `3.42%`

### `some college / associate`

Top state shares within the `some college / associate` bucket:

1. `CA` `1,331,526` `38.16%`
2. `FL` `759,616` `21.77%`
3. `IL` `230,167` `6.60%`
4. `GA` `163,178` `4.68%`
5. `MA` `138,857` `3.98%`
6. `MD` `129,244` `3.70%`
7. `AZ` `128,499` `3.68%`

[SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv]

## What this does and does not imply

### What survives

1. The project can now answer basic composition questions by education bucket and destination cleanly.
2. The three-bucket stock is not dominated only by `<HS`; `HS / GED` and `some college / associate` are both large.
3. `CA` and `FL` dominate all three buckets, but the `<HS` bucket is much more concentrated in `CA` than the other two.

### What does not survive

1. There is still **no repo-grade lifetime fiscal estimate** for these three buckets.
2. The existing broad scenario estimate around `+$29k` central `NPV` is for a different object: one unauthorized Mexican immigrant under a bounded assumption stack, not these three stock buckets. [SOURCE: sources/immigration-fiscal/fiscal_impact_synthesis_gpt54.md]
3. The repo's strongest operational low-skill findings still apply most cleanly to the narrower `SCHL < 16` group, not to the broader public shorthand for all non-college immigrants. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md]

## Best current first-principles ranking

The best current directional ranking is:

1. `<HS` is the most likely to remain net negative on direct fiscal accounting
2. `HS / GED` is more ambiguous
3. `some college / associate` is the least negative and may cross toward positive under some accounting choices

That is still an inference from the broader benchmark literature and the repo's current structure. It is **not** a finished repo estimate. [SOURCE: research/immigration-nas-scope-and-bias-update-2026-04-10.md] [SOURCE: research/immigration-economist-effects-matrix.md] [SOURCE: sources/immigration-fiscal/fiscal_impact_synthesis_gpt54.md] [INFERENCE]

## Practical use

Use this memo when the question is:

1. `How big is each education bucket?`
2. `Which states hold most of each bucket?`
3. `Do we already have a bucket-specific lifetime number?`

Do **not** use this memo to claim:

1. undocumented-only counts by education bucket
2. recent-surge-only counts by education bucket
3. bucket-specific lifetime taxpayer value
4. a settled all-ledgers welfare sign for each bucket

## Artifacts

1. [acs_foreign_born_education_bucket_totals_2023.csv](sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv)
2. [acs_foreign_born_education_state_shares_2023.csv](sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv)
