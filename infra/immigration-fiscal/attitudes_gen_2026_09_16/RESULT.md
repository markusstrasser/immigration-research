**September 17 correction:** GSS `PARBORN=3/5/7` remains unknown, and neither GSS nor ANES now assigns unknown-generation whites to its auxiliary G1–2 cell. All four generated tables were rerun; headline measured patterns survive. The [new-data audit](../../../research/immigration-new-datasets-and-conclusions-2026-09-17.md) gives corrected coefficients and Pew ancestry-selection results. Historical text below is retained; a single “collectivism” trait is not established by these different outcomes. ANES results appear in the later addendum.

**Verdict:** The X claim is PARTIALLY FALSIFIED as stated and UNTESTED on its own instrument. On the items I could measure (GSS 2000-2024, by generation), Hispanic attitudes converge toward the non-Hispanic white baseline on *immigration-specific* items (near-fully on "immigrants increase crime", ~65% of the raw gap on "reduce immigration") but show essentially **no convergence** on redistribution, welfare spending, Democratic party ID, or generalized trust — the trust gap is flat at about −11 points across all three generations once age, education and year are controlled. So "they stay collectivist" is wrong for group-targeted immigration attitudes and roughly right for redistribution and trust. The thermometer in-group test (item 1) could NOT be run: ANES is behind Cloudflare bot management plus a login, and Cremieux's own article does not do a generation split.

Model self-report: Claude Opus 5 (1M context), `claude-opus-5[1m]`, running as the `attitudes_gen_2026_09_16` lane.

## Data and access

- GSS 1972-2024 cumulative, Stata release R3a, downloaded without login [SOURCE: https://gss.norc.org/content/dam/gss/get-the-data/documents/stata/GSS_stata.zip, 45 MB, last-modified 2026-07-14; local `raw/GSS_stata/gss7224_r3a.dta`]. `pyreadstat` needs `encoding="latin1"`; UTF-8 fails on the value labels.
- **ANES BLOCKED** [SOURCE: verified 2026-09-16]. Every `electionstudies.org` URL returns HTTP 403 to curl (with and without a browser user-agent), and `agent-browser` lands on a Cloudflare "Performing security verification" interstitial (Ray ID a3c2cea49bfe83f0). ANES also requires a free account for the data files, so this is not a UA problem. The Cumulative Data File is behind the same wall. Item 1 is therefore **not delivered**.
- Cremieux's article is "What's Up With Self-Hating White Liberals?", 2026-09-12 [SOURCE: https://www.cremieux.xyz/p/whats-up-with-self-hating-white-liberals]. I read the indexed summary, not the full post (Substack paywall/JS). **His analysis splits by race and ideology, not by generation** — so he does not test the repo's question. Two of his own caveats matter: he notes the Hispanic and Asian thermometer results "are harder to interpret here because the questions are not the same until more recent waves", and that the GSS "supports the trend, but not the sign reversal" because it uses rated in-group closeness rather than a thermometer [SOURCE: same].

## Method

Generation coding, GSS variables printed from the codebook [SOURCE: `gss7224_r3a.dta` value labels, `gss_labels.py` output]:

| Variable | Label | Use |
|---|---|---|
| `born` | "Was R born in this country" (1 yes, 2 no) | G1 = `born==2` |
| `parborn` | "Were R's parents born in this country" (0 both US-born; 1-8 at least one foreign or DK) | G2 = US-born & `parborn` in 1-8; G3+ = US-born & `parborn==0` |
| `hispanic` | "R Hispanic Specific" (1 not Hispanic; 2 Mexican; 3 Puerto Rican; 4 Cuban; 5 other) | Hispanic = `hispanic>=2` |
| `race` | 1 white | NH white = `race==1 & hispanic==1` |

`hispanic` only exists from 2000, so the sample is GSS 2000-2024. Weight `wtssps` with `wtssall` fallback; coverage is 1.000. Standard errors are cluster-robust on (year, `vstrat`, `vpsu`). Adjusted models are weighted least squares with age, age-squared, education and year fixed effects, same clustering. Scripts: `gss_gen.py`, `gss_adj.py`; outputs `gss_gen_results.csv`, `gss_gen_adjusted.csv`.

**Validation.** Weighted generation shares among Hispanic GSS respondents, 2000-2024: G1 0.517, G2 0.244, G3+ 0.239 [SOURCE: `gss_gen.py` output]. That first-generation share is consistent with the foreign-born share of the adult Hispanic population over this period [INFERENCE]. The ANES white-white thermometer validation check was not possible, see access above. **No cell falls below n=60**; the smallest is n=116 (Hispanic G2 on the immigration-levels item, which was fielded only on some ballots).

## Item 1 — in-group net warmth: NOT DELIVERED

No ANES access, and no published source I found does the thermometer split by Hispanic generation. Nearest available substitute is Cremieux's race-by-ideology cut, which cannot answer the repo's question. [GAP] A re-dispatch with an ANES account, or the Berkeley SDA archive (which hosts ANES and GSS and appeared reachable at https://sda.berkeley.edu/), would close this.

## Item 2 — policy preferences by generation

Weighted means, unadjusted [SOURCE: `gss_gen_results.csv`]. Higher is more pro-redistribution / more restrictionist as labelled.

| Item | Hisp G1 | Hisp G2 | Hisp G3+ | NH white G3+ |
|---|---|---|---|---|
| Govt should reduce income differences (1-7) | 4.94 (.08) | 5.00 (.09) | 4.79 (.08) | 4.10 (.02) |
| Govt should help the poor (1-5) | 3.53 (.05) | 3.44 (.06) | 3.40 (.05) | 2.98 (.01) |
| Welfare spending "too little" | .251 (.018) | .310 (.025) | .294 (.024) | .199 (.005) |
| Immigration should be reduced | .313 (.041) | .340 (.057) | .451 (.048) | .560 (.016) |
| Immigrants increase crime (agree) | .178 (.022) | .190 (.032) | .265 (.037) | .285 (.012) |
| Democratic party ID | .440 (.015) | .511 (.020) | .469 (.019) | .361 (.005) |
| Strong partisan (strong D or strong R) | .161 (.011) | .166 (.014) | .195 (.014) | .288 (.004) |

Unweighted n runs from 116 to 20,990 per cell; the full table with n and cluster counts is in the CSV.

Adjusted gaps versus non-Hispanic white third-plus generation, same sign convention [SOURCE: `gss_gen_adjusted.csv`]:

| Item | G1 | G2 | G3+ |
|---|---|---|---|
| Reduce income differences | +0.63 (.08) | +0.62 (.09) | +0.50 (.08) |
| Govt help the poor | +0.45 (.05) | +0.30 (.06) | +0.31 (.05) |
| Welfare "too little" | +.050 (.020) | +.088 (.025) | +.072 (.024) |
| Immigration should be reduced | −.272 (.044) | −.177 (.062) | −.092 (.050) |
| Immigrants increase crime | −.140 (.026) | −.085 (.036) | −.021 (.038) |
| Democratic party ID | +.139 (.016) | +.182 (.020) | +.140 (.019) |
| Strong partisan | −.065 (.012) | −.063 (.015) | −.049 (.014) |

Reading: the two immigration items converge monotonically and the third generation is statistically indistinguishable from whites on "immigrants increase crime". Redistribution, welfare and party ID do not converge; the third-generation gap is as large as the first-generation gap within noise. This is the opposite of what a single "collectivism" factor predicts — if in-group preference drove redistribution support, the item that should persist is the redistribution one and the item that should fade is the one about one's own group's immigration, and the data run the other way. [INFERENCE]

On strength of partisanship, Hispanics of every generation are **less** strongly partisan than whites, by 5 to 6.5 points adjusted, rising slightly across generations. That is weak-to-moderate evidence against "importing intense political tribalism" on this measure [SOURCE: table above].

## Item 3 — generalized trust

| | Hisp G1 | Hisp G2 | Hisp G3+ | NH white G3+ |
|---|---|---|---|---|
| "Most people can be trusted" (unadjusted) | .130 (.013) | .173 (.019) | .218 (.021) | .400 (.007) |
| Adjusted gap vs NH white G3+ | −.111 (.017) | −.117 (.021) | −.105 (.020) | — |

n = 970 / 499 / 594 / 9,886. The raw series looks like convergence, closing roughly a third of the gap by the third generation. **The adjusted series shows none** — the gap is flat. Education and survey year account for the entire apparent convergence [SOURCE: `gss_gen_adjusted.csv`]. This is the single most load-bearing result in the memo, and it cuts against the assimilation story rather than for it.

## Caveats that limit the verdict

- **Cross-sectional generations are not lineages.** Third-generation Hispanics in a 2000-2024 sample are mostly descendants of earlier, often Southwest-origin migration, not of today's first generation. Ethnic attrition compounds this: the more assimilated descendants of Hispanic immigrants are the ones most likely to stop identifying as Hispanic, which biases the measured third generation toward *less* convergence than the true lineage shows. This biases my non-convergence findings in the direction I found, so the redistribution and trust results are an upper bound on persistence. [INFERENCE, standard in the Duncan-Trejo literature]
- **Education is a mediator, not just a confounder.** Controlling for it in the adjusted models absorbs part of genuine assimilation. Both versions are reported for that reason; the honest read is that the truth lies between the two columns. [INFERENCE]
- No period interaction is fitted, so the 2024 Hispanic vote swing is inside the year fixed effects rather than being tested. [GAP]
- `letin1` and `immcrime` are ISSP-module items fielded in a subset of years, which is why those n's are an order of magnitude smaller. [SOURCE: GSS codebook]

## Disconfirming and supporting literature

- **Citrin, Lerman, Murakami and Pearson (2007), "Testing Huntington: Is Hispanic Immigration a Threat to American Identity?", *Perspectives on Politics*** — finds Hispanics acquire English rapidly from the second generation, a clear majority reject a purely ethnic identification, and patriotism *grows* generation to generation; concludes traditional political assimilation prevails. Directly against the X claim. [SOURCE: https://www.cambridge.org/core/journals/perspectives-on-politics/article/abs/testing-huntington-is-hispanic-immigration-a-threat-to-american-identity/3FEF0D64DFC062082551717A1141F15E]
- **Abrajano and Singh / Abrajano (2010), "Divided Loyalties? Understanding Variation in Latino Attitudes Toward Immigration", *Social Science Quarterly*** — foreign-born Latinos hold much more positive immigration attitudes than the second and third generation; the driver is ethnic and linguistic identity plus attachment to American culture rather than self-interest. This is the same generational gradient I find on `letin1`, from independent data. [SOURCE: https://onlinelibrary.wiley.com/doi/10.1111/j.1540-6237.2010.00723.x]
- **Abrajano and Alvarez (2009), "Assessing the Causes and Effects of Political Trust Among U.S. Latinos"** — first-generation Latinos are *more* trusting of government than later generations, and the aggregate Latino-Anglo trust gap is driven by immigrant composition. Note the direction: on *political* trust the first generation is highest, whereas on GSS *generalized* trust the first generation is lowest. Different constructs, and worth not conflating. [SOURCE: https://doi.org/10.1177/1532673x08330273]
- **Pleites-Hernandez and Shrode (2024), *SSQ*** — attitudes converge toward Anglo preferences with acculturation, but respondents who report personal discrimination stay much further from the Anglo baseline, and on police reform show no convergence at all. This is a segmented-assimilation mechanism that could generate exactly my item-specific pattern. [SOURCE: https://doi.org/10.1111/ssqu.13435]
- **Setzler and McRee (2010), *Political Research Quarterly*** — Mexican American voting rises monotonically across four-plus generations while ethnic political activity declines after the second. Supports behavioral assimilation. [SOURCE: https://journals.sagepub.com/doi/10.1177/1065912909346738]
- **[GAP]** I found no paper that runs the ANES thermometer in-group premium by Hispanic generation. If none exists, that is a genuinely open cell and worth building once ANES access is obtained. [UNVERIFIED — absence of evidence from two search passes, not an exhaustive check]

## Suggested next queries if re-dispatched

1. Berkeley SDA (https://sda.berkeley.edu/) hosts ANES and GSS with a web tabulation backend; check whether the ANES 2020/2024 time series can be tabulated there without a login. That would deliver item 1.
2. ANES account registration is operator-gated. If the operator creates one, the 2020 variables to pull are the thermometers plus `V201549x` (Hispanic origin) and the birthplace/parental-nativity block near `V201553`-`V201555`, confirmed against the codebook before use.
3. Add a Mexican-origin-only cut (`hispanic==2`) to match the repo's central question, and a period interaction to test whether the generational gradient itself moved after 2016.

---

# ANES section (added 2026-09-17): item 1 delivered

**Verdict on item 1: the X claim SURVIVES on the thermometer measure.** The Hispanic in-group premium does not shrink across generations. Net warmth toward Hispanics minus whites is +11.7 in the first generation, +15.3 in the second and +12.3 in the third-plus, against −1.2 for non-Hispanic whites. No generational trend, and every Hispanic cell is more than ten points above the white baseline. Meanwhile the same respondents' *immigration policy* views converge toward the white baseline, exactly as in the GSS. Affect and policy move apart, which is the central finding of this lane.

## Variable names, read from the codebooks

Extracted with `pypdf` from the shipped user-guide codebooks (`cb_scan.py`, output in `cb_2020.txt` / `cb_2024.txt`). Not guessed.

| Concept | ANES 2020 | ANES 2024 |
|---|---|---|
| Hispanic origin summary | `V201558x` (1 Mexican, 2 Puerto Rican, 3 other Hispanic, 4 type undetermined, 7 not Hispanic) | `V241512x` |
| Race/ethnicity summary | `V201549x` (1 = white non-Hispanic) | `V241501x` |
| Respondent birthplace | `V201554` "RS: BORN US, PUERTO RICO, OR SOME OTHER COUNTRY" (1 US state/DC, 2 Puerto Rico, 3 other US territory, 4 another country) | `V241507` |
| Parents' nativity | `V201553` "NATIVE STATUS OF PARENTS" (1 both born in US, 2 one born in US, 3 both born in another country) | `V241506` |
| Thermometer: Hispanics | `V202479` | `V242515` |
| Thermometer: whites | `V202482` | `V242518` |
| Immigration levels | `V202232` (1 increased a lot to 5 decreased a lot) | `V242227` |
| Guaranteed jobs/income 7-point | `V201255` (1 govt should see to jobs, 7 each person on own) | `V241252` |
| Post-election full-sample weight | `V200010b` | `V240107b` |
| Variance unit / stratum | `V200010c` / `V200010d` | `V240107c` / `V240107d` |

[SOURCE: `raw/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_userguidecodebook_20220210.pdf` and the 2024 equivalent dated 2026-05-19]

Generation coding: G1 = born in another country (`born==4`); G2 = US-born or US territory with at least one foreign-born parent (`par` in {2,3}); G3+ = US-born with both parents US-born (`par==1`). Note that Puerto Rico-born respondents are US-born here, which is the correct citizenship treatment but means Puerto Rican migrants land in G1's conceptual slot only if their parents were also foreign-born. [INFERENCE] Thermometers kept only on 0-100; negative codes are refusals and missing-interview flags. Weighted means with cluster-robust SEs on stratum and variance unit. Script `anes_gen.py`, output `anes_gen_results.csv` (per-item, per-year and pooled).

## Gate: white-to-white thermometer

My computed weighted mean among non-Hispanic white respondents, ANES 2020, is **70.9** (SE 0.39, n = 5,152). The published replication figure is **71.03** (SE 0.40, n = 5,157 in the subpopulation) from Zigerell's ANES 2020 Stata run, which uses the identical variables and `svyset [pw=V200010b]` [SOURCE: https://www.ljzigerell.com/wp-content/uploads/2021/03/ANES-2020-TS-How-racial-groups-rate-each-other.pdf]. Difference 0.13 points. **Gate passes** (threshold 2 points). The same source gives Hispanic respondents rating whites at 65.17 and Hispanics at 80.55, both within a point of my pooled Hispanic cells, a second consistency check.

The ANES Guide's own published marginal page is still behind Cloudflare, so the benchmark here is an independent replication that uses the same weight and variables, not ANES's own table. [SOURCE: verified unreachable 2026-09-16]

## Results, pooled 2020 and 2024

Weighted, SEs in parentheses [SOURCE: `anes_gen_results.csv`].

| Item | Hisp G1 | Hisp G2 | Hisp G3+ | NH white G3+ |
|---|---|---|---|---|
| Thermometer toward Hispanics | 80.0 (1.7) | 78.3 (1.6) | 78.4 (1.5) | 69.4 (0.4) |
| Thermometer toward whites | 68.2 (1.9) | 63.2 (1.7) | 65.5 (1.4) | 70.6 (0.3) |
| **Net in-group warmth** | **+11.7 (2.2)** | **+15.3 (1.7)** | **+12.3 (1.5)** | **−1.2 (0.4)** |
| Immigration should be decreased | .219 (.030) | .224 (.027) | .350 (.033) | .380 (.009) |
| Govt should guarantee jobs/income (1-7) | 4.39 (.14) | 4.65 (.14) | 4.49 (.14) | 3.57 (.03) |

Unweighted n per cell, by year: 2020 gives 209 / 230 / 299 Hispanic G1 / G2 / G3+ and 5,391 white G3+; 2024 gives 147 / 195 / 212 and 3,428. Item-level n is somewhat lower because the thermometers are post-election. **The 2024 Hispanic G1 cell on some items falls near n=130**, so per-year Hispanic splits are thin; the pooled row is the one to read, and all pooled cells exceed n=250. Per-year results are in the CSV.

Weighted generation shares among Hispanic ANES respondents: 2020 gives G1 .276, G2 .334, G3+ .389; 2024 gives .282 / .399 / .319. These differ sharply from GSS 2000-2024 (G1 .517), because ANES weights to the citizen-eligible adult population and the GSS window spans a much higher-immigration period. [INFERENCE] This is a composition difference, not a contradiction, but it means the two surveys' G1 cells are not the same people.

## Cross-check against the GSS section above

| | GSS finding | ANES finding | Agree? |
|---|---|---|---|
| Immigration restriction rises across generations | G1 .31 to G3+ .45 | G1 .219 to G3+ .350 | Yes, same direction and similar magnitude |
| Redistribution support does not converge | third-gen gap as large as first-gen | G3+ 4.49 vs white 3.57, no generational trend | Yes |
| In-group affect | not measured in GSS | no convergence at all | ANES only |

The two independent surveys agree on both of the items they share. That is the strongest thing in this memo.

## What this does and does not settle

The claim "importing ethno-collectivist groups does not turn them into individualists" is **supported on group affect** and **refuted on immigration policy preference**. Those are usually assumed to move together, and here they do not: the third generation is nearly as restrictionist as whites while feeling just as warmly toward its own group. A single "collectivism" trait cannot produce that pattern. [INFERENCE]

Two limits stand. First, the thermometer gap is a *level* difference with no generational slope, but the whites' baseline is itself unusual: white non-Hispanic net in-group warmth of −1.2 is historically anomalous, having fallen from clearly positive values before the mid-1990s [SOURCE: https://emilkirkegaard.dk/en/2025/05/american-race-relations-1964-2024/, which computes the 1964-2024 ANES series and shows whites reaching zero in 2020]. So the gap can be described either as Hispanics staying ethnocentric or as whites having stopped, and the data alone do not adjudicate which side moved. That is the [FRAMING-SENSITIVE] fork in the whole question. Second, the ethnic-attrition caveat from the GSS section applies identically here and biases the third generation toward looking less converged than the true lineage. [INFERENCE]

[GAP] I did not fit the adjusted models (age, education, year) on ANES, so the thermometer result is unadjusted while the GSS trust result is adjusted. A re-dispatch should run the ANES net-warmth regression with the same covariates before the affect and trust findings are compared directly.

## Adjusted models (added 2026-09-17)

Closes the [GAP] left above, so the ANES affect result is now comparable to the adjusted GSS trust result. Weighted least squares of each outcome on group dummies (reference non-Hispanic white third-plus generation) plus age, age-squared, a harmonized five-band education variable and a 2024 dummy; cluster-robust SEs on year by stratum by variance unit. Script `anes_adj.py`, output `anes_gen_adjusted.csv`.

Education needed harmonizing because the two waves use different scales: 2020 `V201510` is an 8-level scale and 2024 `V241463` is a 16-level scale running from "less than 1st grade". Both are collapsed to less-than-high-school, high-school graduate, some college or associate, bachelor's, and graduate or professional. Age is `V201507x` in 2020 and `V241458x` in 2024, both top-coded at 80. [SOURCE: `cb_2020.txt`, `cb_2024.txt`, extracted from the shipped codebook PDFs]

**Gate passes.** Every unadjusted coefficient reproduces the corresponding difference of pooled means in `anes_gen_results.csv`; the largest deviation is 0.0007, against a 0.1 tolerance [SOURCE: `anes_adj.py` gate output].

Net in-group warmth, coefficients versus non-Hispanic white third-plus generation:

| Group | Unadjusted | Adjusted |
|---|---|---|
| Hispanic G1 | +12.88 (2.18) | +13.40 (2.24) |
| Hispanic G2 | +16.49 (1.78) | +14.09 (1.83) |
| Hispanic G3+ | +13.52 (1.53) | +12.39 (1.60) |
| NH white G1-2 | +0.44 (0.84) | +1.30 (0.91) |

n = 9,386 unadjusted and 8,836 adjusted.

**The generational pattern does not change.** Adjustment shaves the second-generation peak by about two points but leaves all three Hispanic generations between +12 and +14 with no downward slope, so the absence of convergence in group affect is not an artifact of age or education composition. The same holds for the two policy items in `anes_gen_adjusted.csv`: immigration restriction still converges monotonically (−.195, −.140, −.017) while support for guaranteed jobs becomes *flatter* under adjustment (+0.82, +0.84, +0.83), which strengthens rather than weakens the GSS redistribution finding.
