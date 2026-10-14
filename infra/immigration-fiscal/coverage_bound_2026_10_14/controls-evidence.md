**Verdict:** Both the original 2025 CPS ASEC and 2024 ACS 1-year weights use Vintage 2024 population estimates. The US base retained Census Hispanic resident totals and had no methodological base change from Vintage 2023. However, DA blending already increased Hispanic young-child cells: the published Vintage 2024 April 2020 base has 408,997 more Hispanic children ages 0–4 than the Census DHC (+8.823%). Applying a complete Census child undercount to those cells would count the existing adjustment again. Against the original DA Table 1C middle series, the remaining under-5 difference is +0.541%, with a wide low/high series range. [SOURCE: sources below] [CALCULATION: `inputs/controls/compare_base.py` → `inputs/controls/base_adjustments.csv`]

This is a controls-and-baseline finding, not a fiscal central estimate. Fiscal pricing and PES/DA acquisition outside `inputs/controls/` belong to the parent.

## 1. Exact survey controls

**2025 CPS ASEC.** Census Working Paper SEHSD-WP2025-13, September 9, 2025, PDF pp.1–2, says the 2025 ASEC uses independent national March 2025 population estimates by age, sex, race and Hispanic origin. The exact description on p.2 is: “weighted to the March 2025 value from the Vintage 2024 population estimates.” This establishes the vintage for ASEC directly; the BLS notice concerns the basic CPS and is corroboration, not a replacement for ASEC documentation. [SOURCE: https://www2.census.gov/library/working-papers/2025/demo/sehsd-wp2025-13.pdf; pinned `inputs/controls/sehsd-wp2025-13.pdf`]

**BLS corroboration.** The January 10, 2025 notice identifies the Census update as Vintage 2024 and says the January 2025 CPS release introduces these controls. It attributes recent updates in particular to new net international migration estimates, not PES adjustment. Its universe for labor-force estimates is the civilian noninstitutionalized population age 16+. [SOURCE: https://www.bls.gov/cps/notices/2025/population-controls.htm; pinned `inputs/controls/bls-controls-2025.web-extract.txt`, explicitly a web-tool text extraction because original HTML/PDF downloads returned HTTP 403]

**2024 ACS 1-year.** Census's September 11, 2025 research note, PDF p.1, states: “The 2024 1-year ACS was controlled to the Vintage 2024 housing and population estimates.” It identifies age, sex, race and Hispanic origin as population controls. The accompanying user note explains that weighting accounts for ACS sample coverage/nonresponse and that the 2024 control change concerns net international migration. [SOURCE: https://www.census.gov/content/dam/Census/programs-surveys/acs/tech-doc/user-notes/2024-acs-1-year-research-note.pdf; pinned `inputs/controls/acs-2024-research-note.pdf`; https://www.census.gov/programs-surveys/acs/technical-documentation/user-notes/2025-03.html; pinned `inputs/controls/acs-controls-2024.html`]

The original 2025 ASEC vintage must be distinguished from newer 2026 releases of alternative 2025 weights: this check establishes the original Vintage 2024 controls, not every later reweighted file. [INFERENCE from the dated documents]

## 2. What the Vintage 2024 US base actually does

The principal source is the December 2024 **Vintage 2024 Methodology Statement**, PDF pp.3–4. Its inputs are protected Census total resident/household/GQ counts; national DA age-sex estimates; and Vintage 2020 age-sex-race detail (plus Hispanic distributions for household/GQ). The Census PL94-171 file supplies Hispanic resident totals. V2020 full characteristics are initially attached to protected Census geographic totals; DA is controlled to Census national totals, then that V2020 detail is raked to DA national age-sex detail. Starting in V2023, Census Hispanic resident distributions were added. State and county raking retains protected Census Hispanic resident margins. Thus DA Hispanic-specific series are not direct origin controls, although DA age-sex constraints can change Hispanic age cells. [SOURCE: https://www2.census.gov/programs-surveys/popest/technical-documentation/methodology/2020-2024/methods-statement-v2024.pdf; pinned `inputs/controls/methods-statement-v2024.pdf`, pp.3–4]

Two short exact anchors on p.4: “age and sex detail is drawn from 2020 DA” and “Hispanic origin detail comes from the 2020 Census.” [SOURCE: same method statement p.4]

The **Vintage 2024 Release Notes**, PDF p.1, explicitly state: “The Vintage 2024 blended base for the United States did not feature changes relative to Vintage 2023.” Puerto Rico's GQ composition did change; that is separate from the US base. V2024 changes documented on pp.1–2 concern vital statistics and humanitarian-migrant inputs to international migration. This does not mean every geographic base count is numerically identical across vintages: boundaries, Count Question Resolution and post-census GQ corrections can alter counts. [SOURCE: https://www2.census.gov/programs-surveys/popest/technical-documentation/methodology/2020-2024/2024-est-relnotes.pdf; pinned `inputs/controls/2024-est-relnotes.pdf`]

The method statement p.5 also benchmarks births' race/Hispanic distribution to the blended-base under-age-1 distribution. Post-2020 births therefore do not inherit a Census **enumeration** omission, but vital-record origin classification is not an independently perfect measurement of Hispanic identification. A zero Census-2020 omission correction for later births remains distinct from claiming their survey controls have no other errors. [SOURCE: method statement p.5] [INFERENCE]

## 3. PAA paper and the disconfirmation

The mandatory Census **PAA 2024 paper**, PDF p.13, identifies the V2023 update: “Hispanic or Latino resident population totals from the 2020 Census.” On p.8 it says the PES design was “deemed inconducive to valid, reliable adjustments to the estimates base”. That decision concerned synthetic bias and the transfer of PES uncertainty into small-area estimates; it does not make PES error estimates uninformative. [SOURCE: https://www.census.gov/content/dam/Census/newsroom/press-kits/2024/paa/paa2024-paper-modernizing-popestimates-base.pdf; pinned `inputs/controls/paa2024-modernizing-base.pdf`]

But the same paper's pp.4 and 9–10 documents more children ages 0–4 and 10–14 because of DA age-sex blending. This is not evidence that all Hispanic age-specific omissions remain intact. [SOURCE: same PAA paper]

The Census June 22, 2023 article directly states that using DA age detail “increased the Hispanic population 17 years and under” compared with either Census-only or V2020-only bases. This is direct origin-specific disconfirmation, not an inference from total children alone. It describes V2022, before Census Hispanic resident margins were adopted for V2023. [SOURCE: https://www.census.gov/library/stories/2023/06/blended-base-methodology.html; pinned `inputs/controls/blended-base-2023.html`, section “Challenges Spur Innovations”]

The December 18, 2023 official PES/base recommendation article says DA blending “also indirectly mitigates the undercounts for these populations”, referring to Black and Hispanic young children, while stating that PES was not directly used for base adjustments. The V2024 numeric comparison below tests the later base directly instead of assuming the older V2022 pattern transferred unchanged. [SOURCE: https://www.census.gov/newsroom/blogs/random-samplings/2023/12/recommendations-2020-pes-coverage-results-in-vintage-2023-pop-estimates.html; pinned `inputs/controls/pes-base-recommendation-2023.html`, “Looking Ahead”]

## 4. Numeric April 2020 base versus Census and original DA

These are national **resident Hispanic** populations on April 1, 2020. Census counts come from the API's 2020 DHC P12H national table, with the machine-readable labels pinned separately. V2024 values come from `nc-est2024-alldata-r-file01.csv`, `UNIVERSE=R`, `YEAR=2020`, `MONTH=4.2`, summing `H_MALE+H_FEMALE` across ages. The official NC layout PDF p.3 explicitly defines MONTH 4.2 as the April 1, 2020 estimates base; ordinary MONTH=4 is not that base. [DATA: `inputs/controls/dhc-p12h-us.json`, `dhc-p12h-variables.json`, `nc-est2024-alldata-r-file01.csv`] [SOURCE: https://www2.census.gov/programs-surveys/popest/technical-documentation/file-layouts/2020-2024/NC-EST2024-ALLDATA.pdf; pinned `inputs/controls/nc-est2024-alldata-layout.pdf`]

DA counts are summed from the both-sex single-age rows of the parent's pinned `inputs/da_hispanic.xlsx`, Table 1C. The sheet explicitly uses thousands; low/middle/high are methodological series, not confidence limits. Individual rounded-age sums need not match rounded published totals. [DATA: `inputs/da_hispanic.xlsx`, rows 5–34; source URL in parent's `inputs/pins.json`] [CALCULATION: `inputs/controls/compare_base.py`]

| Age on April 1, 2020 | Census DHC | V2024 base | Base change vs Census | DA middle residual vs base | DA low / high residual vs base |
|---|---:|---:|---:|---:|---:|
| 0–4 | 4,635,698 | 5,044,695 | +8.823% | +0.541% | −8.201% / +7.162% |
| 5–9 | 5,135,533 | 5,236,266 | +1.961% | +1.866% | −6.861% / +7.749% |
| 10–14 | 5,675,286 | 5,651,037 | −0.427% | +4.264% | −3.504% / +10.245% |
| 15–17 | 3,310,735 | 3,190,211 | −3.640% | +3.159% | −3.329% / +9.303% |
| 18–29 | 12,324,769 | 11,850,626 | −3.847% | +0.003% | −5.313% / +6.146% |
| 0–29 | 31,082,021 | 30,972,835 | −0.351% | +1.508% | −5.511% / +7.656% |
| All ages | 62,080,044 | 62,075,161 | −0.00787% | unavailable | unavailable |

[CALCULATION: `inputs/controls/compare_base.py` → `inputs/controls/base_adjustments.csv` and `.json`; includes further aggregations 0–9, 10–17, 30–49, 50+, 0–17]

The all-age Hispanic base margin is essentially the Census count, while young-child counts change substantially. These are compatible statements: controlling both origin totals and total age cells redistributes origin counts over age. The full 0–4 DA middle-versus-Census count deficit is largely absent from the blended base already. Age corrections require the remaining gap relative to the base, rather than the original Census gap. The +408,997 is the combined blended-base difference, not a clean estimate of DA's isolated contribution. [INFERENCE]

## 5. Use in the pricing lane and remaining limits

- If `q = blended_base / census`, and PES net coverage error is signed as `nce = (census−PES_target)/PES_target`, the adjusted target/base factor is `1 / ((1+nce)*q) − 1`. The DA factor is directly `DA_target / blended_base − 1`. Do not add a DA residual to a PES all-age adjustment on the same people without a stated conserving allocation. [CALCULATION]
- [GAP] PES targets household population; DHC and the R-file comparison here target residents including GQ. Transferring PES rates to resident base age cells is an assumption, particularly for adult ages with substantial GQ populations. DA and the R-file comparison share the resident universe.
- [GAP] National Hispanic rates do not identify Mexican-origin, generation-specific, or state-specific omissions. Applying them to the priced group remains a transfer assumption even after correcting the base.
- [GAP] The reviewer's cited 7.34% Hispanic under-5 DA figure has not been traced by this subtask. It is not the same calculation as the original Table 1C middle count versus current DHC P12H; identify its DA release/series/count before substitution.
- [GAP] This check does not separately decompose Census origin classification differences from true enumeration omission, nor estimate survival/emigration of missed April 2020 members through March 2025.
- [GAP] No fiscal effect is calculated here. This evidence does not establish whether a particular fiscal correction clears $5bn.

## 6. Checks, reproducibility, files and acquisition log

Run `OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/coverage_bound_2026_10_14/inputs/controls/compare_base.py`.
It validates all controls source byte sizes/hashes, PDF signatures and JSON parses; unique base ages; resident universe and April-base date; complete age support; exact national Hispanic Census/base closure; DHC age labels and unsplit bands; DA units/series; positive denominators and finite outputs. Initial run: PASS, 0.024 seconds, 52,690,944 bytes maximum RSS (Python `time.perf_counter`, `resource.getrusage`).

Acquisition failures corrected: default urllib Census request returned 403; curl with explicit user agent retrieved and validated PDFs. BLS original requests returned 403, so only its primary web-tool extraction is pinned and marked as such. Census unkeyed API returned HTTP 200 with a “Missing Key” HTML page; the data request was repeated with the unprinted local key, parsed as JSON, and the erroneous snapshot/pin replaced. Source validity is now checked independently of HTTP success. The numeric input URLs omit the API key.

Files covered: CPS/ASEC and ACS control docs; V2024 methods/release notes; mandatory PAA paper; young-child disconfirmation docs; NC R-file/layout and Census P12H counts/labels; original DA Table 1C read from the parent's file. Skipped: fiscal code/consumer migration, PES/DA acquisition and pricing outputs, all owned by the parent. `inputs/controls/pins.json` inventories official source snapshots. The supplemental methodology webinar PDF is pinned as corroboration; principal conclusions use the method statement and release notes.

Final verification (2026-10-14T20:49:43+0900, from `date`): exact quoted phrases found on the stated pages of six pinned PDFs with local `pdftotext`; Python source compile PASS; two generated numeric files reproduced `IDENTICAL: 2/2`, subprocess exit 0. The parent should include the `compare_base.py` command in its lane-wide rerun invocation, since this worker did not rerun concurrently edited fiscal files.

Every changed path, relative to `infra/immigration-fiscal/coverage_bound_2026_10_14/`:

- `controls-evidence.md`
- `inputs/controls/2024-est-relnotes.pdf`
- `inputs/controls/acs-2024-research-note.pdf`
- `inputs/controls/acs-controls-2024.html`
- `inputs/controls/base_adjustments.csv`
- `inputs/controls/base_adjustments.json`
- `inputs/controls/blended-base-2023.html`
- `inputs/controls/bls-controls-2025.web-extract.txt`
- `inputs/controls/compare_base.py`
- `inputs/controls/dhc-p12h-us.json`
- `inputs/controls/dhc-p12h-variables.json`
- `inputs/controls/methods-statement-v2024.pdf`
- `inputs/controls/nc-est2024-alldata-layout.pdf`
- `inputs/controls/nc-est2024-alldata-r-file01.csv`
- `inputs/controls/paa2024-modernizing-base.pdf`
- `inputs/controls/pes-base-recommendation-2023.html`
- `inputs/controls/pins.json`
- `inputs/controls/sehsd-wp2025-13.pdf`
- `inputs/controls/v2024-methodology-updates.pdf`

## Adjacent sex-specific controls extension

At the parent's request, `compare_base.py` also writes `inputs/controls/base_adjustments_sex.csv`: six April-2020 age bands (0–4, 5–9, 10–17, 18–29, 30–49, 50–100), separately for sex 1=male and 2=female. Counts are parsed from the same pinned NC R-file (`H_MALE`, `H_FEMALE`) and DHC P12H labels; DA series come from Table 1C's explicitly labelled Male and Female sections. Each row includes `base_over_census` and low/middle/high `da_residual_factor_*` to avoid applying a both-sex base ratio to a sex-specific PES rate. The existing both-sex output calculations and schemas remain unchanged. [CALCULATION: `inputs/controls/compare_base.py` → `inputs/controls/base_adjustments_sex.csv`]

Under age 5, male/female base increases versus Census are +9.046% / +8.592%; corresponding original DA middle residuals versus base are +0.760% / +0.395%. At ages 30–49, male/female base changes are +6.002% / −2.246%, illustrating why sex-specific controls matter. These ratios describe the published base's age-sex composition; they do not identify isolated DA causal contributions. [CALCULATION: sex-specific CSV] [INFERENCE]

Checks: male and female single-age NC counts each close **exactly** to their declared all-age sex total; DHC single-age-category counts each close exactly to the corresponding sex total; each age band's male+female Census/base count closes exactly to the original both-sex output. DA cells were independently rounded to thousands, so male+female need not equal the rounded both-sex cell exactly; every age/series is checked against the maximal one-thousand difference implied by those rounded integer cells. This preserves the source's rounding, rather than inventing exact counts. All ratios must be finite and denominators positive.

Verification at 2026-10-14T21:04:57+0900 (`date`): input/pin/closure gates PASS; all three generated numeric files reproduced **IDENTICAL: 3/3**, subprocess exit 0; Python compile PASS; elapsed 0.023 seconds, maximum RSS 52,330,496 bytes. No new primary inputs or pins were needed. Changed paths in this extension only: `inputs/controls/compare_base.py`, `inputs/controls/base_adjustments_sex.csv`, `controls-evidence.md`.
