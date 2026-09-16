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
