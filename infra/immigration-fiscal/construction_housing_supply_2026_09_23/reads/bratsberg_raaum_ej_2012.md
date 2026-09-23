<!-- reader extraction, researcher agent (claude-opus-5-5[1m]), 2026-09-23; every quoted string below was re-found in the pdftotext -layout output (whitespace-normalised substring check + rg -F), see "Quote check" at the bottom -->
[UNVERIFIED]

# Bratsberg and Raaum (2012), "Immigration and Wages: Evidence from Construction"

## Citation and version read

- **Version of record:** Bernt Bratsberg and Oddbjørn Raaum, "Immigration and Wages: Evidence from Construction", *The Economic Journal* 122(565): 1177–1205, published 2012-09-03. DOI [10.1111/j.1468-0297.2012.02540.x](https://doi.org/10.1111/j.1468-0297.2012.02540.x). Metadata confirmed on Crossref 2026-09-23.
- **Text actually read (in full):** CReAM Discussion Paper No 06/10, UCL, dated April 2010, same title and authors, 42 pages. File `_cache/papers/bratsberg_cdp0610.pdf` (from `cream-migration.org/publ_uploads/CDP_06_10.pdf`), text `_cache/papers/bratsberg_cdp0610.txt`.
- **Version caveat:** the published EJ text was not read. Every number below is from the April 2010 discussion paper; the version of record may carry revised estimates. [GAP]

## Population, geography, period

- **Workers:** full-time employees aged 18–60 of Norwegian mainland construction firms (NACE two-digit 45), from administrative payroll records linked to the population register. "In the gross sample, there are between 174,000 and 181,000 observations of native-born construction workers each year." Main wage sample: 918,082 observations of 217,151 native workers (Table 1).
- **Immigrants:** foreign-born workers in the payroll register; about half hold a "D-number" (no Norwegian residence). Main sources Sweden, then Poland and the Baltic states after the 2004 EU enlargement. Immigrant construction employment ran from "15,000 (eight percent) in 1999 and 22,000 (11 percent of construction-sector workers) in 2005."
- **Units:** 16 construction activities defined by the employer's five-digit NACE code (industry, not occupation).
- **Period:** 1998–2005, annual.
- **Prices:** Statistics Norway building-cost price indices matched to 8 of the 16 activities (electrical, plumbing, road, site preparation, general/frame, concrete/other, painting, carpentry), 63 activity-year observations.
- **Wage measure:** daily wage = total pay / contract days (hours only in three brackets), full-time only.

## Design and identification

- Wage equation: log daily wage on f(P) = ln(1+M/N) (M, N = immigrant, native employment in the activity), activity fixed effects, year fixed effects, individual fixed effects, cubic in age, schooling, gender. Standard errors clustered by activity-year.
- Identifying variation: certification and licensing rules (electricians need a directorate certificate; heavy-machinery licences in road work and rentals) kept immigrant shares flat in electrical installation, plumbing, road, bridge and tunnel work, while carpentry and painting absorbed immigrants. "our estimate of the impact of immigration on wages will rely heavily on the wage growth of carpenters and painters relative to electricians, plumbers, and road construction workers."
- Checks: controls for overtime, skill share, union density (Table 2 col 1); dropping road/bridge/tunnel (col 2); a placebo on same-diploma workers outside construction (col 4); a triple difference pooling construction and non-construction workers with trade-specific year effects (col 5).
- Price equation (6): log price index of activity j in year t on ln(1+M/N), activity and year fixed effects.
- All effects are **relative** effects across trades within construction: year fixed effects absorb anything common to the sector.

## Estimates

Coefficients on ln(1+M/N) unless stated. The authors convert them: elasticity with respect to the immigrant stock = coefficient × P; derivative with respect to the share P = coefficient / (1 − P).

| Outcome | Estimate | SE or CI | Table / page (DP) | Verbatim quote (≤40 words) |
|---|---|---|---|---|
| Native log daily wage, no individual FE | −0.103 | (0.162) | Table 1 col 1, p.16 | "Ignoring individual fixed effects (ui), the estimate of θ is statistically insignificant and close to zero" |
| **Native log daily wage, individual FE (preferred)** | **−0.724** | (0.202) | Table 1 col 2, p.16 | "ln(1+M/N) -.103 -.724 -.554 -.570 -.032 -.569" |
| Same, SE row | — | (.162) (.202) (.175) (.183) (.175) (.180) | Table 1, p.16 | "(.162) (.202) (.175) (.183) (.175) (.180)" |
| Same, stated in text | −0.72, significant | — | §5.1, p.15 | "the estimate of θ is now negative, -0.72, and statistically significant." |
| **Native wage elasticity w.r.t. immigrant stock** | **−0.06** at mean share 0.085 | from (0.202) | §5.1, p.15 | "If immigrant employment increases by ten percent, wages of natives are predicted to fall by 0.6 percent." |
| Derivative w.r.t. immigrant share P; w.r.t. M/N | −0.791; −0.662 | — | §5.1, p.16 | "is -0.724/(1-0.085) = -0.791, while" |
| Same w.r.t. M/N if true immigrant count is 50% higher than payroll count | −0.44 | — | §5.1, p.16 | "our parameter estimate implies an elasticity with respect to relative immigrant employment of -0.44" |
| Balanced panel, no FE / with FE | −0.554 / −0.570 | (0.175) / (0.183) | Table 1 cols 3–4, p.16 | "Unlike in the full sample, introducing individual fixed effects has no impact whatsoever on the coefficient estimate" |
| Drop entrants / drop leavers | −0.032 / −0.569 | (0.175) / (0.180) | Table 1 cols 5–6, p.16 | "yields a coefficient estimate of -0.57 (0.18) which is remarkably close to the balanced-panel result" |
| With overtime, skill-share, union controls | −0.652 | (0.231) | Table 2 col 1, p.20 | "ln(1+M/N) -.652 -.760 -.719 -.018 -.637" |
| Drop road, bridge, tunnel firms | −0.760 | (0.177) | Table 2 col 2, p.20 | "(.231) (.177) (.199) (.127) (.279)" |
| Carpenters, electricians, painters, plumbers in own activity | −0.719 | (0.199) | Table 2 col 3, p.20 | "The reduced-sample estimate of θ, -.719, is practically identical to our preferred estimate" |
| Placebo: same diplomas, employed outside construction | −0.018 | (0.127) | Table 2 col 4, p.20 | "Column (4) shows that it is not; the estimate is basically zero and statistically insignificant." |
| Triple difference, pooled with trade-specific year effects | −0.637 | (0.279) | Table 2 col 5, p.20 | "the estimate remains negative and significantly different from zero" |
| Exit to welfare by 2005 per unit immigrant share (marginal effect) | +0.197 | (0.077) | Table 3 col 1, p.24 | "a one percentage point increase in the immigrant share is associated with a 0.20 percentage point boost in the transition rate to welfare" |
| Exit to new job outside construction / to the residual 'other' state | −0.121 / +0.146 | (0.148) / (0.021) | Table 3 cols 2–3, p.24 | "Immigrant share .197 -.121 .146" |
| Natives, all (pooled with immigrants) | −0.704 | (0.204) | Table 4, p.30 | "Natives/All -.704" |
| Immigrants, all | −0.885 | (0.206) | Table 4, p.30 | "Immigrants/All -.885" |
| Natives, low education, cols 1–4 | −1.053 / −0.813 / −0.512 / −0.520 | (0.170) (0.120) (0.200) (0.145) | Table 4, p.30 | "Natives/Low educ 30.9 -1.053 -.813 -.512 -.520" |
| Natives, high education, cols 1–4 | −0.310 / −0.073 / −0.095 / +0.127 | (0.201) (0.160) (0.235) (0.177) | Table 4, p.30 | "Natives/High educ 20.3 -.310 -.073 -.095 .127" |
| Implied elasticity of substitution across activities σJ | 1.4 (range 1.1–2.0 for low/medium skill) | — | §6.3, p.29–31 | "implies an elasticity of substitution between workers in different activities (σJ) of 1.4 (=1/0.704; see equation 4)." |
| Relative price growth, no-immigration trades vs immigrant-intensive trades | 50–100% faster | descriptive, Figure 4 | §7, p.33 | "the prices of services with no increases in immigrant labor have risen at a rate 50 to 100 percent above that observed for services that intensified their use of immigrant labor." |
| **Log price of construction service, full sample (δ)** | **−1.155** | (0.214) | Table 5 col 1, p.34 | "Coefficient of ln(1+M/N) (δ) -1.155 -1.028 -.763 -.387" |
| Price, SE row and N | — | (.214) (.231) (.163) (.088); N = 63 / 55 / 55 / 47 | Table 5, p.34 | "(.214) (.231) (.163) (.088)" |
| **Price elasticity w.r.t. immigrant employment** | **−0.11** at mean share 0.095 | from (0.214) | §7, p.33 | "a ten percent increase in immigrant construction labor is predicted to reduce prices of construction services by 1.1 percent." |
| Price, drop plumbing | −1.028 | (0.231) | Table 5 col 2, p.34 | "Observations 63 55 55 47" |
| Price, drop electrical | −0.763 | (0.163) | Table 5 col 3, p.34 | (same table rows as above) |
| Price, drop plumbing and electrical | −0.387 | (0.088) | Table 5 col 4, p.34 | "Figure 4 clearly suggests that the price changes of electrical installation and plumbing services are crucial to the estimate." |
| Authors' reading of price vs wage effect | price effect larger than wage effect | — | §1, p.3 | "the direct cost reductions associated with use of immigrant labor and the indirect reductions through their impact on native wages combine to produce relative price effects that are even larger in size than the relative wage adjustments" |

Not estimated: construction employment totals, housing starts or completions, house prices, rents. Figure 1 plots housing starts only as cycle context.

## Authors' stated limits

- **Undercount of immigrants** (off-the-books work, posted workers paid abroad, temp-agency workers): "Because posted workers typically are paid in the home country of the contractor, they will not be included in the Norwegian payroll data." With a 50% undercount, "the true parameter θ will be 70 percent of that based on observed counts." The stock elasticity (−0.06) is invariant to a proportional undercount.
- **Price indices are cost-based, not transaction prices** (fn 22): "the price indices used for this analysis are largely cost-based." They are "constructed by means of fixed weights from price indices for materials and labor".
- **The price result leans on electrical and plumbing** (the licensed trades whose prices rose fastest): dropping both cuts δ from −1.155 to −0.387.
- **One observation per activity-year**, so activity-by-year effects cannot be included; the triple difference is the substitute.
- **Exit is correlation, not a causal estimate:** "Although we are unable to conclude that there is a causal link between immigration and exit of construction workers with low wage potential".
- **One sector only:** "By focusing on one sector of the economy, we may overlook other important impacts of immigration."

## What the estimate implies per unit of immigrant labour

[CALCULATION from the paper's own coefficients and conversion formulas; the parent should re-derive before use.] The unit is a within-construction trade (activity) in Norway, 1998–2005, and the shock is registered immigrant employment in that trade, mostly Swedish, Polish and Baltic workers, many non-resident. **Prices:** a 10% rise in the number of immigrant workers in a trade lowers that trade's building-cost price index by 1.1% relative to other trades (δ × P̄ = −1.155 × 0.095 = −0.110; 95% CI on δ of −1.57 to −0.74 gives −0.15 to −0.07). Stated per percentage point of immigrant share, the relative price falls by δ/(1 − P̄) = 1.155/0.905 ≈ **1.28% per 1 pp** (CI about 0.81–1.74%). Excluding the two licensed trades that drive the fit, δ = −0.387 (0.088) gives an elasticity of about −0.037 and about **0.43% per 1 pp**. **Wages:** +1 pp of immigrant share lowers native daily wages in the trade by 0.79% (−0.724/0.915), a stock elasticity of −0.06, concentrated in low- and medium-education natives; high-education natives show no effect. These are relative effects, with year fixed effects absorbing any sector-wide price or wage change, and they are measured on cost-based indices built from input-price weights, so they are closer to a unit-labour-cost pass-through than to a measured change in the price of new housing. The paper has no housing-quantity outcome.

## Quote check

Method: each quoted string was checked as a substring of the whitespace-normalised `bratsberg_cdp0610.txt` (pdftotext -layout), result recorded by `scratchpad/verify_quotes.py`; single-line strings also with `rg -F`.

Result (2026-09-23): 36 quotes checked, 0 missing.
