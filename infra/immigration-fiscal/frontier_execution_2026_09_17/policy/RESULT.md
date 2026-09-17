**Verdict:** A real row-level Bracero reconstruction now reproduces all four wage coefficients and sample sizes in the author working paper, with independent numerical checks. Its CSV is a public third-party mirror, so this is **[DEGRADED provenance], not a certified official-package reproduction**. H-2B remains a published-table reproduction, conditional on responding surviving firms. Published Danzer count results establish neither cumulative patent catch-up nor a precisely estimated cumulative stock loss.

## What ran, source versions and coverage

`replicate_bracero_danzer.py` independently reconstructs 1955 Mexican seasonal-worker exposure, post-1965 interactions, CPI-deflated wages, and state and quarter/year effects. It uses 15,831 raw CSV rows and a separately downloaded CPI table. Every coefficient was checked by an independent alternating-projection/FWL solver. Coefficients are not copied from the third-party Julia output; Julia source was inspected to recover variable definitions. `summarize_epoch2.py` verifies the four wage coefficient/sample-size anchors and every mirrored file against GitHub's git-blob hashes. Sources and SHA256 values are in `epoch2-sources.json`; complete input hashes and library versions are in `epoch2-manifest.json`.

The original [AEA article](https://www.aeaweb.org/articles?id=10.1257/aer.20170765) identifies the 2018 paper and [official replication archive](https://doi.org/10.3886/E113187V1). The public archive directory can be inspected, but download required login; legacy AEA data route returned404. No account, CAPTCHA bypass, contact, or purchase was attempted. A [public Julia replication repository](https://github.com/glpousse/bracero_pkg.jl) supplied the raw CSV. All files match its archived tree268ba5b189a348712859d94f468ef3bbb955bb52, but this does **not** verify identity with original Stata files. The primary table anchor is the [authors' NBER working paper](https://www.nber.org/system/files/working_papers/w23125/w23125.pdf), revised July2017, Tables1–2, PDF pp.43/45; the journal main PDF returns403. The official published appendix was downloaded. Thus published-final-table identity remains a separate [GAP].

## Results and discriminating checks

| Specification | N | Estimate | Cluster SE, all dummy parameters | SE, nested-state correction | Printed point estimate matches? |
|---|---:|---:|---:|---:|---|
| hourly_all | 4324 | -0.035644 | 0.042824 | 0.042596 | True |
| daily_all | 5813 | -0.384538 | 0.497400 | 0.495426 | True |
| hourly_1960_1970 | 2024 | -0.040054 | 0.031852 | 0.031488 | True |
| daily_1960_1970 | 1901 | -0.024672 | 0.313036 | 0.309218 | True |
| log_hourly_all | 4324 | -0.083084 | 0.065783 | 0.065432 | No printed anchor set |
| domestic_all | 8970 | -19229.596649 | 18809.152098 | 18760.856002 | False |
| domestic_1960_1970 | 5198 | -7105.300812 | 12130.406187 | 12076.601941 | False |

The hourly all-years estimate is −$0.035644/hour (1965 dollars) for exposure changing from0 to1; it is not a per-migrant effect. A10percentage-point exposure contrast scales it to −$0.003564/hour. The log-hourly estimate is−.083084 per full exposure unit. NBER Table1 reports−.0831(.0654), and rejects its model's +.1 semielasticity benchmark at p=.0075. This result supports a narrow conclusion: terminating this agricultural guest-worker program did not produce the predicted material wage gains in more exposed states. It does not establish an exact zero, effects for every worker, or gains from every admission policy. [SOURCE: Table1 and §4.1]

The two SE columns expose a software-convention difference: ordinary full-dummy clustered covariance counts absorbed state parameters; the second excludes45 redundant nested-state degrees of freedom. Point estimates match independently. Published table SEs round to .0426/.495/.0315/.309; any small residual differences from an exact package run remain visible. Intervals in CSV use the more conservative full-dummy SE and t45. We did not silently force published SEs. A covariance warning concerned nuisance fixed-effect variances; treatment variances are finite/positive and the FWL coefficient check passed.

**Missingness sensitivity matters.** An initial incorrect diagnostic converted every wholly unreported month into observed zero employment and did not match Table2. The corrected code permits zero for a missing state count only in months with some observed Local_final report, matching the paper's stated convention more closely. Current employment coefficients and N are shown above; if the anchor-match column is false they are a failed reproduction, not substitute evidence. There is no randomized assignment/attrition in this historical panel: identification rests on exposure-specific parallel trends and the absence of other simultaneous exposure-correlated shocks. National treatment and inter-state spillovers limit interpretation. [SOURCE: NBER §4.2 and Table2 notes; INFERENCE: identification limits]

The script also emits an exploratory Mexican-worker post1965 interaction. It is **not** a published first stage, not a randomized instrument, and not counted as reproduced causal evidence. H-2B supplies the credible randomized first stage in the earlier memo; no attempt is made to combine its first stage with Bracero outcomes.

Review correction: the employment diagnostic now completes the 46-state grid within months having any observed Local_final report. This adds 113 absent state-month rows in February, March and December 1954, in addition to filling missing cells. The completed all-years diagnostic has 8,970 rows; its source-table mismatch remains. The report calendar is inferred from observed Local_final values, not verified against the official package. Wage samples are unchanged. See `derived/domestic_panel_completion.json`.

## Automation and cumulative invention

Exact exposure definition: cumulative centrally allocated ethnic Germans divided by the pre-allocation average stock of unskilled manual workers plus unemployed people. This is an allocation-to-baseline ratio, not an observed increase in employed migrants or a population share. Allocation starts in 1996, 1997 or 2002 across the included regions. Event coefficients are relative to the year before allocation, use 1991 population weights and region-clustered SEs. [SOURCE: main paper §§3–4 and supplement B-6 notes.]

The [published Danzer et al.2024 main paper](https://edoc.ku.de/id/eprint/33404/1/1-s2.0-S0047272724000720-main.pdf), §5.2, and [published supplement](https://ars.els-cdn.com/content/image/1-s2.0-S0047272724000720-mmc1.pdf), TableB-6, provide annual **patent-count** PPML coefficients, so the effect is not solely a change in automation's share of patents. For a10percentage-point cumulative low-skilled inflow exposure change, the year4 coefficient−3.647(1.415) implies an estimated conditional automation-count ratio exp(−.3647)=0.694; its approximate normal95% ratio interval is[0.526,0.916]. Year10's−.194(.789) is imprecise and near zero. All11 post coefficients are negative point estimates; annual effects approaching zero do not replenish a missing knowledge stock. [SOURCE: B-6; calculation in derived/danzer_annual_count_ratios.csv]

However, actual cumulative patents require each untreated predicted count and aggregation weights, and valid joint uncertainty requires coefficient covariance. Neither printed table nor supplement supplies these. The main data statement says data available on request; no contact was made. As a substantive partial calculation, the equal-event-year average log-count effect has exp(.1×meanβ)=0.811690. The covariance-free upper bound SD(meanβ)≤mean(SE) gives a conservative asymptotic normal95% ratio interval[0.629073,1.047320]. It includes1. This is a geometric mean of conditional annual ratios, **not a cumulative patent-count estimate or stock confidence interval**. The bound does not assume independent event coefficients. [INFERENCE/calculation: Cauchy–Schwarz covariance bound; script and JSON]

Cross-institution disconfirmation is substantive: the H-2B lottery's positive short-run occasional equipment/real-estate spending concerns firm scale; Bracero exclusion allows agricultural technology/crop adjustment; Danzer studies local automation invention after ethnic-German labor allocation. These outcomes can coexist. Bracero is a different policy institution but shares two authors with H-2B; Danzer is independently authored. No one design identifies the combined social welfare effect or the consequences of broad present-day removals. [SOURCE: papers' outcomes/designs; INFERENCE: transport]

## Remaining gaps and next narrow check

- [GAP] Official Bracero package access/hash and final published table identity; a user-supplied official zip would resolve provenance immediately. No more general web search is warranted.
- [GAP] Any nonmatching domestic-employment table needs the original Stata report-month/sample code before it is called reproduced. Wage results already match the working-paper source.
- [GAP] H-2B raw assignment, response/survival selection and reported SEs remain unreplicated; retain published Table2/AppendixA4 arithmetic and conditional-survivor wording.
- [GAP] Danzer cumulative count loss and recovery need untreated fitted counts plus coefficient covariance/raw estimation rows. More annual significance tests cannot resolve stock catch-up.
- Coverage: public original landing pages, H-2B final main/appendix, Bracero raw mirror/CPI/primary working-paper Tables1–2 and official appendix, Danzer published count table and data-access statement. Skipped: package contact/login, new broad survey, allcrop machinery regressions, patents downloads, welfare dollars; these exceed either access or this discriminating check.

The scripts and results are integrated in the frontier execution directory. Raw inputs and derived tables remain local and ignored. The epoch-1 H-2B report is retained below as a historical checkpoint; its uncompleted Bracero/Danzer work is superseded by the results above. Its surviving/responding sample limitation still governs every use of the revenue result.

---

## Selected comparison and versions

Clemens–Lewis, *The Effect of Low-Skill Immigration Restrictions on US Firms and Workers: Evidence from a Randomized Lottery*, AEJ Applied 18(3), July 2026, pp.43–82, [DOI10.1257/app.20250049](https://www.aeaweb.org/articles?id=10.1257/app.20250049). The journal main PDF returned403, so the downloaded main text is the [author institution's July2026 reprint](https://www.piie.com/sites/default/files/2026-07/wp26-11.pdf), whose cover explicitly identifies the AEA publication and permission. The [downloaded journal appendix](https://www.aeaweb.org/articles/materials/25505) is dated June2026. The public replication DOI is [10.3886/E234802V1](https://doi.org/10.3886/E234802V1). These supersede relying only on the held May2024 working paper for this exercise.

The 2021/2022 lottery randomizes priority letters at the petition level. The binary firm instrument is a share exceeding50% of requested workers on A-priority petitions; some firms submit multiple petitions. The alternative instrument is requested-worker shares by lottery letter multiplied by corresponding approval rates. Hiring is therefore endogenous even though petition priority is randomized. Reduced-form assignment effects and the IV effect among firms whose hiring responds are different estimands. Main §§4.2–5, Tables2–3; appendixA4.

## Arithmetic actually completed

`reproduce.py` verifies the transcribed coefficients occur in the proper primary-table text, emits `derived/published_table_arithmetic.csv`, recomputes the four just-identified ratios, and hashes archived sources into `manifest.json`. `verify.py` independently checks intervals with Decimal and ratios with Fraction. **These are computational checks of published tables, not independent replication of the data, sampling, treatment assignment or standard errors.**

| Quantity | Published estimate (robust SE) | What the check establishes |
|---|---:|---|
| First stage: binary win → IHS H-2B hires, n472 | .618 (.112) | Approximate normal95% interval [.3985,.8375]; a material first stage. The paper's46% loss approximation is1−exp(−.618), not a direct raw head-count estimate. |
| First stage: expected share → IHS H-2B hires, n472 | 2.233 (.374) | Approximate interval[1.5000,2.9660]. |
| Primary reduced form: win → log revenue | .135 (.051) | Approximate interval[.0350,.2350]; conditional geometric ratio exp(.135)≈1.145. It is revenue, not separately observed physical output/productivity. |
| Revenue IV, win / expected share | .218 (.080) / .198 (.069) | .135/.618=.21845 and .443/2.233=.19839 reproduce within published rounding. |
| U.S.-temporary-hiring IV, win / expected share | .188 (.149) / .061 (.125) | .116/.618=.18770 and .136/2.233=.06090 reproduce. Approximate intervals[−.104,.480] and[−.184,.306] do not establish nonnegative effects. |
| Secondary investment IV, n456 | 2.072 (.721) /1.466 (.610) | Published coefficients and their rounded-SE intervals preserved; no first-stage ratio claim made because this outcome uses a different sample. |

Normal intervals here are not the paper's Anderson–Rubin or randomization intervals. IHS coefficients are not exact constant elasticities, especially near zero. The log-revenue retransformation is not an arithmetic-mean revenue effect. Table2's Anderson–Rubin p-values are .008/.004 for revenue and .219/.630 for U.S. temporary hiring; those published values were inspected, not re-estimated.

## Assignment, missingness, and causal limits

- **U.S. workers are citizens plus lawful permanent residents**, not native-born only (main footnote1; appendixA3). The 472 pooled firm observations concern seasonal H-2B applicants/respondents, not all firms or all residents.
- The 2021 survey received371 forms:54 too incomplete,15 zero-petition,13 duplicate responses were removed, leaving289;251 provided the full baseline needed for core analysis. In2022,297 forms minus10 duplicates and **two firms with near-zero revenue/apparent closure** left285;221 supplied core baseline data. Form-to-core fractions are67.7% and74.4%, **not population response rates**. AppendixA3.
- The paper explicitly says it surveys surviving firms, observes outcomes3–9months after the lottery and cannot estimate survival/long-run effects (main§4.1). Excluding closed firms and outcome nonrespondents matters if the lottery affects survival or reporting. Balance among respondents does not rule out selection involving unobserved outcomes. Its sample/universe lottery distributions and baseline balance are useful checks, not a proof that this channel vanishes. MainTable1; appendixA6.
- Both instrument specifications, reduced forms and IV estimates should be retained. The win threshold and multiple petitions make firm-level treatment less simple than one randomized Bernoulli draw per firm. Raw assignment, number-of-petitions adjustment, cross-year firm overlap and attrition-by-assignment cannot be independently audited without the package. [GAP]
- IV interpretation also needs the relevant exclusion and response assumptions: lottery priority may affect timing/uncertainty as well as worker counts. The policy bundle is still meaningful, but translating the hiring coefficient into the effect of an unrelated admission/removal policy is an extra assumption. [INFERENCE]
- The authors acknowledge possible business stealing from losing firms (main§9). Hence within-firm expansion under a fixed quota does not equal the effect of raising the aggregate quota. General-equilibrium wages/prices, incumbent individual transitions and migrant household effects are outside this table.

## Investment, automation and disconfirmation

Investment is a survey amount for occasional equipment or real-estate purchases; it does not classify automation, capital intensity or research. No prior-year investment was collected. Firm expansion can raise total investment while labor abundance lowers automation per worker or invention incentives. Therefore this positive investment result cannot refute an automation externality. Main§5.2, footnote26.

Within this source family, the2020 partial replication changes the labor-market regime and gives similar-signed but imprecise results. It lacks the corresponding baseline revenue and investment information; it uses requested workers as a size proxy. This is useful adverse-condition evidence but does not establish equivalence across regimes. AppendixA17. The overall U.S.-employment intervals and survivor selection are material disconfirming limits to an unrestricted positive conclusion. An independently assessed alternative institution/design has **not** been completed in this epoch. [GAP]

## Access, validation, next epoch

Public routes attempted: publisher page and linked DOI; direct openICPSR; indexed exact-title/package/GitHub searches; author-institution disclosure and reprint; one isolated browser session. openICPSR returned curl403, the web reader rejected its redirect, and the isolated browser displayed a Cloudflare security-verification widget. No account, payment or external contact was attempted. This is an access failure in this environment, **not evidence the package is private or nonexistent**. Browser challenge handling is not claimed complete; no challenge was bypassed.

Run from this directory: `UV_CACHE_DIR=$PWD/.uv-cache uv run --no-project python3 reproduce.py`, then the analogous command for `verify.py`. Initial sandbox execution failed because uv's default cache was outside the writable root; the task-local cache resolves that environment issue. Browser lifecycle commands require the same authorized execution context used to open it. The manifest preserves successful source hashes and failed routes. Source PDF extraction uses installed `pdftotext -layout`.

**[GAP / checkpoint]** For the next epoch, first try a legitimate readable download interface for replication234802; inspect README, raw survey/assignment files and author Stata code before translating the consequential Table2/A4 specifications. Do not substitute old NBER tables for this published version. If public retrieval remains unavailable, choose a genuinely public already-grounded policy package (e.g. the bracero exclusion) and reproduce its direct employment/wage endpoint, retaining H-2B as the source-table result above. Then inspect Danzer's published cumulative patent-count response/covariance; no such analysis is claimed here. No more broad paper-summary search is needed.

Coverage: main§§4–5/9, Tables1–3; appendixA3/A4/A6/A14/A17 design passages; exact publication/version and public-access checks; arithmetic scripts. Skipped: raw re-estimation and assignment/attrition reanalysis (package not obtained), external institution replication, and Danzer cumulative innovation (epoch boundary after the primary-source core). No repository edits or commits; all output lives in this owned temporary directory.
