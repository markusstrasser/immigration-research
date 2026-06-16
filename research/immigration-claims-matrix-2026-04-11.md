# Immigration claims matrix (comparative + quantitative, 2026-04-11)

## Scope

This is the current **defensible claim set** after the Smith/Decker/Friedman audit and the public-MVP data builds (`MEPS`, `SIPP`, and `SIPP→MEPS` bridge). The matrix is not a political conclusion; it is a claim ledger.

**Legend**

- `VERIFIED`: directly supported by primary source, official statistics, or direct warehouse query output.
- `MODERATE`: supported by multiple good sources but model-dependent or incomplete.
- `INFERRED`: logical or algebraic transform of verified numbers.
- `UNRESOLVED`: unsupported for a final scalar judgment.

## Quantitative matrix (common objective evidence)

| Claim | Evidence / frame | Status | Confidence | What we can claim now |
|---|---|---|---|---|
| 1. Immigration surge (2021–26) changed aggregate macro/fiscal terms in CBO’s official simulation | 8.7M above prior-trend migrants (2021–26), federal deficits down about $897B over 2024–2034, federal revenue gain about $1.175T, outlays +$278B, nominal GDP +$8.9T over 2024–2034 | VERIFIED | HIGH | Net national/macro accounting channel is favorable in that scenario. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf] |
| 2. Same surge made state/local 2023 totals less favorable | 4.4M added residents in 2023; direct net state/local about -$9.2B and potential net about -$9.8B | VERIFIED | HIGH | State/local channels are materially negative in this surge snapshot. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf] |
| 3. Per-added-resident local arithmetic (direct from CBO 2025) | 2023 direct taxes ~ $2.30k, direct spending ~$4.39k, direct net ~ -$2.09k; potential net ~ -$2.23k | DATA (derived from verified aggregates) | MODERATE | Useful scale check, but only for one year and one scenario; not a lifetime result. |
| 4. Higher immigration does not produce a uniform inflation story | IMF 2025: local inflation may fall 0.1–0.2pp, but housing and utilities inflation rises; effects stronger for working-age low-education immigrants | VERIFIED | HIGH | Housing incidence is a real local counterweight even when goods inflation softens. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2025/english/wpiea2025005-print-pdf.pdf] |
| 5. Local composition is heterogeneous by origin and destination | School burden: e.g., Afghanistan 2.6291 school-age children per household, Honduras 1.2855, Myanmar 1.2650, El Salvador 1.0600, Mexico 1.0114, Guatemala 0.9960; rent exposure high for China, Colombia, Brazil, Venezuela | VERIFIED | HIGH | “One average local burden” is falsified by warehouse joins. |
| 6. MEPS-to-SIPP bridge integrity for the public MVP | `sipp_public_mvp_cells_2024.csv` has 98 rows; bridge has 294 rows; 98 expected-health rows; exact match rate 98/98, no fallback, no unmatched | VERIFIED | HIGH | The low-skill transition-health path is now integrated enough to be a scenario input, but not itself final fiscal truth. [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/sipp_meps_bridge_cells_2024.meta.json] |
| 7. Foreign-born education stock (ACS 2023 cut) | `<HS`: 4,303,453; `HS/GED`: 4,115,963; `some college/assoc`: 3,489,226 | VERIFIED | HIGH | We can state stock and composition, not finalized bucket-level lifetime NPV yet. [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_bucket_totals_2023.csv] |
| 8. State concentration of stock by bucket | CA 4,915,063 (41.27%), FL 2,132,532 (17.91%), IL 821,241 (6.90%), GA 577,078 (4.85%), AZ 482,467 (4.05%) | VERIFIED | HIGH | Destination sorting is concentrated; local effects are not homogeneous. [SOURCE: sources/immigration-fiscal/data/derived/stage3_proto/acs_foreign_born_education_state_shares_2023.csv] |
| 9. MEPS working-age payer-cost pattern | In observed annual spending (`ages 25–64`), foreign-born with any private ~`$5,522` vs US-born `$8,084`; public-only foreign-born `$5,185` vs US-born `$10,200`; uninsured foreign-born `$782` vs US-born `$1,451` | VERIFIED (from module outputs) | MODERATE | crude foreign-born cost disadvantage claim is weakened, but this is one ledger and not the whole welfare score. |

## Economist-specific matrix (claim-by-claim)

| Claim / person | What the claim says | Status with current stack | Best surviving interpretation |
|---|---|---|---|
| Noah Smith | Immigration supports aggregate growth and weakly moves wages on net | MODERATE-VERIFIED | Survives on national macro lens (demographic + aggregate channels), fails as universal citizen-welfare claim because local/shelter-schooling channels are unpriced by the same statement. |
| Noah Smith | Inflation blamed mostly on other things | MODERATE | Survives in broad brush, but fails where housing utilities incidence is the channel. |
| Nicholas Decker | Immigrants must make us richer | MODERATE-FALSE (as universal statement) | Survives as “certain channels are real” (scale/specialization), not as a must-theorem for all policy frames. |
| Nicholas Decker | Main anti-immigration objections are purely political/institutional | VERIFIED false | Repo’s warehouse shows economic local-capacity channels (school/housing) are materially real. |
| David D. Friedman | Open migration should be judged mainly by global/liberty welfare | VERIFIED mostly | Survives on that frame and with transfer/rights exclusion as an instrument; does not settle native-local welfare. |
| David D. Friedman | Limiting transfers/voting eliminates the economic case for restriction | MODERATE-FALSE (as complete fix) | Partly survives institutionally, fails because non-welfare public-capacity channels remain. |

## Current verdict envelope

1. No scalar sign can be defended from current artifacts alone.
2. The strongest defensible statement is an **incidence split**:
   - some national/federal channels are positive,
   - some local channels are negative,
   - and welfare sign depends on scale, destination mix, and institutional design.
3. The dataset state now supports:
   - definitive stock/composition statements,
   - verified local burden heterogeneity,
   - and a complete `SIPP→MEPS` transition-to-health bridge for scenario scoring.
   It does **not** yet support final bucket-specific lifetime NPVs. [SOURCE: research/immigration-verified-findings-report-2026-04-10.md][SOURCE: research/immigration-education-bucket-stock-and-lifetime-status-2026-04-11.md]

## Open uncertainties

1. The repo still lacks a finalized federal + local lifetime micro-sim for each education bucket.
2. The MEPS bridge is a health-cost channel, not a complete fiscal or welfare model.
3. Political legitimacy/backlash costs remain in the model as first-order terms and can dominate near-term outcomes.
