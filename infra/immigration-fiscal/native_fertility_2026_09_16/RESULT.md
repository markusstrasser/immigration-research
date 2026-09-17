# Native Fertility Crowd-Out — Does Immigration Suppress Native Births?

**Superseded interpretation, 2026-09-17:** the [adversarial audit](../../../research/immigration-new-conclusions-audit-2026-09-17.md) §2 reproduces the stored coefficient but withdraws causal/no-crowd-out and housing-channel-refutation claims. It finds age-control and IV construction defects, a false 2021-availability statement, and unresolved geographic comparability. Original text/output below is retained as the pre-audit record; it is not a current causal estimate.

**Corrected source-cache rerun:** age-bin repair changes the weighted top-50 cross-section from −0.270 to −0.1683 (SE 0.0950), so the claimed exact numerical replication does not survive. Corrected FE is −0.0930 (SE 0.2578), interval [−0.598, +0.412]. Origin code/denominator/missingness repairs leave 26 complete exposures, F≈2; causal 2SLS is disabled. Geography and 2021 inclusion remain open. Tracked CSV/text outputs are historical snapshots; current scripts reconstruct inputs from the cached source data.

**Verdict:** The CIS cross-sectional coefficient **reproduces almost exactly** (pop-weighted
−0.270 vs their −0.269), but it **does not survive within-metro identification**. A 432-metro,
12-year fixed-effects panel (5,108 metro-year observations) gives **−0.043, SE 0.26** — six times
smaller than the cross-section and indistinguishable from zero; weighting by native women flips
the sign to **+0.18**. The rent channel's *first* link holds (immigration raises rents within a
metro, +0.63% per point, p<0.0001) but its *second* link does not (those rent increases do not
lower native fertility). The "immigrants offset aging, but self-cancellingly" argument is
**NOT SUPPORTED** at the metro level on ACS data.

**Honest limit:** the fixed-effects confidence interval is [−0.55, +0.47]. It **contains** the CIS
value of −0.27, so this does not statistically *reject* their estimate. It shows the estimate is
not identified by their design and is not recovered by a better one.

Model self-report: environment block names **Opus 5 (1M context)**, model ID `claude-opus-5[1m]`.

[UNVERIFIED] — own computation from Census API, not yet externally replicated.
Source data: ACS 1-year and 5-year summary tables, Census API, cached in `_cache/`.

---

## Validation gates (both PASS)

**(a) National native birth rate from metro aggregation vs published national B13008**

| Vintage | Metro-aggregated | National B13008 | Error |
|---|---|---|---|
| ACS 2023 1-yr | 48.40 | 49.49 | −2.19% |
| ACS 2010 1-yr | 50.90 | 51.52 | −1.19% |
| ACS 2015–19 5-yr | 49.62 | 50.34 | −1.42% |

All within the 3% gate. The residual gap is real and expected: published CBSAs exclude rural
and small-metro women, whose native birth rate is slightly higher.

**(b) Foreign-born share for Los Angeles and Houston, B05012 vs B05002**

| Metro | B05012 | B05002 | Diff |
|---|---|---|---|
| Los Angeles (31080), 2023 | 32.87% | 32.87% | +0.000 pts |
| Houston (26420), 2023 | 24.80% | 24.80% | +0.000 pts |
| Los Angeles, 2015–19 | 33.09% | 33.09% | +0.000 pts |
| Houston, 2015–19 | 23.44% | 23.44% | +0.000 pts |

PASS, but honestly: this gate is **weak**. B05012 and B05002 are two tabulations of the same
universe from the same microdata, so exact agreement is near-automatic. It confirms I read the
right variables, not that the estimate is right.

**Geography note.** The PUMS `tabulate` endpoint rejects CBSA outright
(`unknown/unsupported geography hierarchy`); it accepts only state and PUMA. B13008 (women
15–50 with/without a birth in the past 12 months, by marital status **and nativity**) carries
the full native numerator and denominator at CBSA level, so the summary-table route replaces
PUMS entirely here. B13002 is marital-status-only and does not split by nativity.

---

## 1. CIS reproduction — it replicates

Camarota & Zeigler (CIS, Feb 2021) report **−0.269** native births per 1,000 native women 15–50
per 1-point immigrant share, 50 largest metros, ACS 2015–19 5-year, with controls.

| Spec (2015–19 5-yr) | Coefficient | SE | p | n | R² |
|---|---|---|---|---|---|
| Top 50, bivariate | −0.303 | 0.046 | <0.001 | 50 | 0.30 |
| Top 50, full controls | −0.333 | 0.092 | 0.0003 | 50 | 0.73 |
| **Top 50, controls, pop-weighted** | **−0.270** | 0.091 | 0.003 | 50 | 0.78 |
| All CBSAs, bivariate | −0.020 | 0.087 | 0.82 | 926 | 0.00 |
| All CBSAs, full controls | −0.294 | 0.150 | 0.049 | 926 | 0.23 |
| Top 100, controls | −0.419 | 0.096 | <0.001 | 100 | 0.62 |
| Top 250, controls | −0.496 | 0.154 | 0.001 | 250 | 0.46 |
| **Rank 51+ only, controls** | **−0.215** | 0.177 | **0.22** | 876 | 0.22 |

Controls: log median gross rent, log median household income, BA+ share, Black share, Hispanic
share, homeownership rate, median age of native women, share of women 15–50 aged 20–34.

The pop-weighted top-50 estimate lands on CIS's number to three decimals. Their claim that the
effect is weaker in smaller metros also holds — rank 51+ is insignificant. So the CIS finding is
**arithmetically correct as stated**. The question is what it identifies.

## 2. Own cross-section, ACS 2023 1-year

| Spec | Coefficient | SE | p | n |
|---|---|---|---|---|
| Top 50, bivariate | −0.283 | 0.066 | <0.001 | 50 |
| Top 50, full controls | −0.186 | 0.105 | 0.076 | 50 |
| All CBSAs, bivariate | −0.125 | 0.098 | 0.20 | 438 |
| All CBSAs, full controls | −0.290 | 0.183 | 0.11 | 438 |
| All CBSAs, controls, pop-weighted | −0.256 | 0.107 | 0.017 | 438 |

Same sign, similar magnitude, but weaker significance in a single year than in the pooled
5-year file. The cross-sectional pattern is stable across vintages.

**Two results that damage the housing-cost mechanism:**

- **Foreign-born women's own birth rate rises with immigrant share** (+1.296, p=0.051). If
  expensive housing in high-immigrant metros suppressed fertility, it should suppress it hardest
  for immigrants, who rent at far higher rates. It does the opposite. This is a placebo failure
  for the stated channel.
- **Dropping rent from the controls barely moves the coefficient** (−0.290 → −0.229). Rent is
  a *mediator* of the claimed story, not a confounder, so conditioning on it should *shrink* the
  estimate toward zero if housing is the channel. It shrinks only slightly, meaning nearly all
  of the cross-sectional association runs through something other than rent.

The rent first stage itself is real but small: a 1-point higher immigrant share predicts 0.66%
higher median gross rent (p=0.0009), conditional on income and composition.

## 3. Long difference 2010 → 2023 — the effect disappears

CBSA codes harmonized across the 2009 and 2023 delineation vintages (31100→31080 for Los
Angeles, 42060→42200 for Santa Barbara); 232 metros match on both ends.

Sample attrition is a data limitation, not a filter I chose: the 2010 ACS 1-year file suppresses
B03002 race detail for micropolitan areas (277 of 525 rows return null), so the long difference
runs on **metropolitan areas only**. That is the right sample for this question anyway, and it
includes every metro CIS used.

| Spec | Coefficient | SE | p | n |
|---|---|---|---|---|
| Bivariate | −0.361 | 0.698 | 0.61 | 232 |
| Full delta controls | −0.278 | 0.774 | 0.72 | 232 |
| Controls, pop-weighted | −0.308 | 0.424 | 0.47 | 232 |
| Top 50 only | −0.304 | 0.851 | 0.72 | 50 |

The point estimates sit right on top of the cross-sectional ones — around −0.3 every time — but
the standard errors are **8 to 17 times larger**. Nothing is distinguishable from zero. Over this
period the mean metro lost 3.09 native births per 1,000 women while gaining 1.02 points of
immigrant share; the national fertility collapse swamps any metro-level immigration signal.

Five sizable 2010 metros drop out on delineation changes or non-publication: Cleveland (2.08M),
Honolulu (956k), Dayton (841k), Poughkeepsie (671k), Holland-Grand Haven (264k).

## 4. Shift-share instrument — WEAK, do not interpret

2010 origin-country settlement shares (B05006, 136 leaf countries) × the 2010→2023 national
change in each origin's stock, scaled by 2010 metro population.

- First stage: **b = −0.0036, robust F = 7.3** — below the conventional threshold of 10, and
  **wrong-signed**: predicted inflow correlates −0.234 with actual change in immigrant share.
- 2SLS: +1.15 (SE 3.45). Uninterpretable.

The wrong sign has a real cause. The Mexican-born stock *fell* between 2010 and 2023, so metros
with the heaviest 2010 Mexican settlement get a large negative predicted shift, while their
actual immigrant share was buoyed by other origins. The canonical fix is a 1990 or 2000 base
year, which is not reachable at 2023-vintage CBSA geography from the ACS API. **This IV does not
identify anything and no conclusion rests on it.** [CAVEAT]

## 5. Zillow ZORI as an alternative rent measure

Matched 183 of 232 long-difference metros by principal city and state.

- corr(ZORI growth 2015→2023, ACS Δlog rent) = 0.335 — the two rent measures agree only
  moderately, which is itself a caution about the ACS rent control.
- corr(ZORI growth, Δ immigrant share) = **−0.076**. Metros that gained immigrants did **not**
  see faster market rent growth.
- Swapping ZORI for ACS rent in the long difference: **−0.282** (SE 0.656, p=0.67). Unchanged
  and still insignificant.
- ZORI growth regressed on Δ immigrant share: −0.005 (p=0.24). No rent channel in the
  time-series dimension at all.

## 6. Arithmetic at the estimated coefficients [INFERENCE]

National base, ACS 2023: 65,192,113 native women 15–50; 3,226,208 births to native women in the
past 12 months; 792,725 births to foreign-born women; national foreign-born share 15.6%.

Taking each coefficient at face value and applying it to the full national immigrant share — a
deliberately generous extrapolation, since no metro has a zero immigrant share:

| Coefficient source | b | Implied native births forgone/yr | As % of native births | As % of foreign-born births |
|---|---|---|---|---|
| CIS spec, top 50 | −0.333 | 338,000 | 10.5% | 42.7% |
| Own 2023 cross-section | −0.290 | 295,000 | 9.2% | 37.3% |
| Long difference 2010–23 | −0.278 | 283,000 | 8.8% | 35.7% |

So **if the cross-sectional coefficient were causal**, the crowd-out would cancel roughly
35–43% of the immigrant birth contribution. That is the strongest possible form of the
"self-cancelling" claim, and it is worth stating plainly because it is not trivial — it would
meaningfully reduce, though not eliminate, the demographic offset.

But the long-difference confidence interval spans −1.79 to +1.24, which at the same arithmetic
runs from "immigration cancels more than twice the immigrant birth contribution" to
"immigration *raises* native births by 1.6× the immigrant contribution." The data do not pin
this down.

---

## Cross-sectional caveats, stated plainly

1. **Sorting, not causation.** High-immigrant metros are large, coastal, expensive, highly
   educated, and late-marrying. Every one of those independently depresses native fertility.
   Controls for rent, income, education and age structure are crude proxies for a deep
   compositional difference.
2. **Selective native out-migration.** Natives who most want children may leave high-immigrant
   metros *because* they want children (space, schools, cost). Then the same total native births
   occur, relocated. The metro cross-section counts that as suppression; nationally it is zero.
   The long difference partially handles this and finds nothing.
3. **Reverse causation.** Immigrants go where labor demand is, and labor demand is concentrated
   where young natives are working and postponing children.
4. **"Native" includes second-generation.** B13008 nativity is birthplace, so US-born daughters
   of immigrants are native. High-immigrant metros therefore have a native denominator with
   higher-than-average underlying fertility, biasing the coefficient *toward zero*, not away.
5. **The literature is genuinely split.** Seah 2018 (Mariel) finds a short-run negative effect
   concentrated among renters that *recovers later* — a timing shift, not a level loss. Furtado
   & Hock 2010 and Furtado 2016 find low-skill immigration *raises* high-skill native fertility
   via cheaper childcare. Adserà & Ferrer find no UK effect. "Happily Ever After" (JEH 2025)
   finds 1910–30 immigration *raised* native marriage and fertility. Two of these four point the
   opposite direction from CIS.
6. **Instrument bias.** Per `notes/llm-bias-caveat.md`, this is a politically charged topic
   analyzed through an LLM. The finding here happens to cut against the restrictionist claim;
   that is not a reason to trust it more or less, and the code and cached API responses are in
   this directory for independent checking.

## 7. Within-metro fixed effects — the decisive test

ACS 1-year, 2010–2023 (2020 and 2021 ACS 1-year were not published). 432 metros observed in at
least 10 of the 12 available years, 5,108 metro-year observations. Metro fixed effects absorb
every time-invariant reason a metro has low native fertility; year fixed effects absorb the
national fertility decline. Standard errors clustered by metro.

| Spec | Coefficient | SE | p |
|---|---|---|---|
| Metro FE + year FE, no time-varying controls | −0.103 | 0.253 | 0.68 |
| + age structure | −0.104 | 0.253 | 0.68 |
| **+ rent, income, age structure** | **−0.043** | **0.260** | **0.87** |
| + controls, weighted by native women | **+0.182** | 0.201 | 0.37 |
| 50 largest metros only | +0.023 | 0.429 | 0.96 |
| *Same data, pooled with year FE only (no metro FE)* | *+0.127* | *0.088* | *0.15* |

Three things to read off this table.

**The effect vanishes when metro identity is held fixed.** The point estimate falls from −0.27 to
−0.043, and the standard error (0.26) is three times tighter than the long difference (0.77), so
this is a genuinely more powerful test, not just a noisier one. The population-weighted version —
the specification that matches how CIS weights — is *positive*.

**The rent channel's first link is real.** Within a metro, a 1-point rise in immigrant share
predicts **+0.63% median gross rent** (SE 0.0014, p<0.0001), controlling for income and metro and
year effects. This is a clean, well-identified housing-cost effect and it is consistent with
Seah 2018 and with this repo's own rent work. Immigration does make housing more expensive.

**The second link is missing.** That same variation does not move native fertility. The chain
"immigration → higher rents → fewer native births" breaks at the second arrow, in the same data
where the first arrow is strongly identified. Combined with the cross-sectional placebo failure
in §2 (foreign-born women's own birth rates *rise* with immigrant share), the housing-cost
mechanism specifically is not supported.

**A fragility worth flagging.** Pooled with year effects only, the coefficient is *positive*
(+0.127). The negative cross-sectional coefficient appears only when the full demographic control
set is applied to large metros. It is not a robust feature of the raw data; it is produced by a
particular conditioning choice.

### Arithmetic at the fixed-effects coefficient [INFERENCE]

| | Native births forgone/yr | As % of the 792,725 births to foreign-born women |
|---|---|---|
| FE point estimate (−0.043) | 43,000 | 5.5% |
| FE CI lower bound (−0.552) | 561,000 | 70.8% |
| FE CI upper bound (+0.467) | −475,000 (i.e. a *gain*) | — |

The best-identified estimate says the crowd-out cancels about **5% of the immigrant birth
contribution**, against the 35–43% implied by the cross-section. The interval remains wide enough
that a large effect cannot be excluded, but nothing in the within-metro data points to one.

---

## Reconciliation with the cited literature

The result is more consistent with the literature than the CIS cross-section is. Seah 2018 finds a
*short-run* renter-concentrated dip that **recovers** — a timing shift, which a 12-year panel with
year effects would correctly show as near-zero in levels. Furtado & Hock 2010 and Furtado 2016
find low-skill immigration *raises* high-skill native fertility through cheaper childcare, an
offsetting positive channel. Adserà & Ferrer find no UK effect. "Happily Ever After" (JEH 2025)
finds 1910–30 immigration raised native marriage and fertility. Four of the five cited sources
point to zero, to recovery, or to a positive effect; CIS is the outlier, and it is the one design
here that cannot separate immigrant location from immigrant impact.

## What would change this conclusion

- Individual-level PUMS with metro identifiers and a tenure split, testing whether *renter* native
  women specifically reduce births — Seah's actual mechanism, which metro aggregates cannot see.
- A valid shift-share instrument with a 1990 or 2000 base year at consistent geography.
- Birth-order decomposition: a timing effect (delayed first births, recovered later) would show up
  in parity-specific rates while leaving completed fertility alone. Nothing here tests completed
  fertility.

## Files

- `fetch_acs.py` — Census API fetcher, all responses cached in `_cache/`
- `build_panel.py` — CBSA panel construction + validation gates
- `analyze.py` — sections 1–6; output in `analysis_output.txt`
- `panel_fe.py` — section 7 fixed-effects panel; output in `fe_output.txt`
- `panel_acs1_2023.csv`, `panel_acs1_2010.csv`, `panel_acs5_2019.csv`, `long_difference.csv`
