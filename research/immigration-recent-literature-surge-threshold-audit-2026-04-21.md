# Immigration economics since 2023: surge and threshold audit

**Question:** What has recent economics research on immigration changed relative to the older literature, and does the newer work actually model surge/threshold effects?  
**Tier:** Deep | **Date:** 2026-04-21  
**Ground truth:** The repo already concluded that pre-2020 labor-market results are bounded to marginal-policy variation and do not cleanly answer the 2021-2024 surge. This memo checks whether the last three years of economist papers and official analyses materially change that picture. [DATA]

## Bottom line

1. **Yes, the literature has shifted.** The center of gravity is no longer just Card/Borjas-style wage regressions on local labor supply. Newer work pays much more attention to:
   - macro/population-growth effects
   - inflation and housing
   - local public finance and shelter systems
   - intergenerational outcomes
   - recent unauthorized/asylum surge composition

2. **No, the threshold problem is still mostly under-modeled.** I did not find strong recent economist papers that estimate clean breakpoints like `2% -> 6%` or `6% -> 10%` immigrant-share transitions with explicit nonlinear welfare/capacity thresholds.

3. The closest recent work to the user's concern is:
   - **CBO 2025** on state/local surge costs
   - **Meyer, Wyse, Williams 2025** on asylum seekers and sheltered homelessness
   - **Barrett and Tan 2025** on local inflation with housing/utility pressure
   - **new housing papers** that allow heterogeneity by permits/supply conditions

4. The newer literature is therefore **strictly better than the old literature for surge-era realism**, but it still does not fully solve the user's concern about **convex capacity costs** and **political threshold effects**.

## Claims table

| # | Claim | Evidence | Confidence | Source | Status |
|---|---|---|---|---|---|
| 1 | Since 2023, immigration economics has shifted toward macro, prices, fiscal incidence, and recent-surge composition | Multiple 2023-2026 papers/reports | HIGH | IMF 2023, CBO 2024/2025, IMF 2025, Dallas Fed 2024, FRBSF 2024/2026, NBER 2025 | VERIFIED |
| 2 | Newer work is better at modeling the recent surge than pre-2020 local-labor papers | Administrative-data surge work and official budget reports | HIGH | CBO 2024/2025, Dallas Fed 2024, FRBSF 2026, NBER 2025 | VERIFIED |
| 3 | Newer work has solved threshold/nonlinearity modeling | I found heterogeneity and episode studies, not clean threshold estimation | HIGH | targeted literature sample | REJECTED |
| 4 | The best recent evidence on local capacity stress points to housing/shelter/public finance rather than large average wage losses | Official budgets + housing/shelter papers | HIGH | CBO 2025, NBER w33655, IMF 2025, housing paper 2025 | VERIFIED |

## What changed relative to the older literature

### Before roughly 2023

The dominant questions were:

1. Do immigrants lower native wages?
2. Are immigrants substitutes or complements?
3. Are there long-run aggregate productivity gains?

The standard empirical designs were:

1. local labor market comparisons
2. shift-share instruments
3. famous shocks like Mariel
4. long-run cross-country or city-level productivity arguments

This older literature was strong on:

1. average labor-market impacts
2. task specialization/complementarity
3. long-run productivity and place-premium arguments

It was weaker on:

1. local public finance
2. housing/shelter capacity
3. recent asylum/unauthorized surge composition
4. nonlinear local system stress

### Since 2023

The newer literature has broadened the outcome set materially.

It now asks:

1. What do large immigration waves do to output, productivity, inflation, and labor-market tightness at the macro level?
2. What do immigrant inflows do to local public goods and budgets?
3. What do recent asylum/unauthorized inflows do to shelter systems and homelessness?
4. How do housing supply conditions change incidence?
5. What are the intergenerational effects on natives in receiving places?

That is a real shift, not just a new coat of paint.

## Recent papers and what they add

### 1) IMF 2023 — large immigration waves, macro focus

The IMF paper *The Macroeconomic Effects of Large Immigration Waves* is a clear move away from tiny marginal local shocks. It studies **large immigration episodes** and uses IV plus local projections. The paper finds that in advanced countries, large immigration shocks raise output and productivity in the short and medium term; specifically, a **1 percentage point immigrant-flow / employment shock raises output by almost 1 percent by year five**. [SOURCE: https://www.imf.org/-/media/files/publications/wp/2023/english/wpiea2023259-print-pdf.pdf]

What changed:

1. The unit is now a **large wave**, not just a local-city cross-section.
2. The outcome is macro output/productivity, not only native wages.

What it still misses:

1. it is still an **average dynamic response**, not a threshold model
2. it does not solve local shelter/housing/budget overload

### 2) Mayda, Senses, Steingress 2023 — local public goods

This paper is one of the strongest recent departures from the old labor-only frame. It studies **county-level public goods provision**. It finds that low-skilled and high-skilled immigration have opposite fiscal/public-goods effects, and that the average national effect can mask very large local heterogeneity. The authors report that the average net effect is only about **0.3 percent per year**, but also give examples where estimated inflows imply a **15 percent reduction** in per-capita public goods in one county and a **14 percent increase** in another. They also find **no significant impact on education spending per capita or per pupil**, implying reallocation within budgets rather than a simple collapse story. [SOURCE: https://www.bankofcanada.ca/wp-content/uploads/2023/11/swp2023-57.pdf]

What changed:

1. The literature is now directly pricing **local public goods**, not just wages.
2. Heterogeneity by **skill composition** matters centrally.

What it still misses:

1. sample period is **1990-2010**, not the post-2021 surge
2. still not a discrete threshold model

### 3) CBO 2024 — federal budget and macro effects of the recent surge

This is not a journal paper, but it is economist-produced and more relevant to the current U.S. episode than most classic papers. CBO estimates the recent surge expands the labor force and economy, while also saying the surge slows wage growth for workers with **12 or fewer years of education** through 2026. [SOURCE: https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf]

What changed:

1. It models the **actual recent surge**, not a stylized historical average.
2. It puts macro gains and low-skill-worker pressure in the same framework.

What it still misses:

1. state/local costs were initially outside scope
2. no explicit threshold estimation

### 4) FRBSF 2024 — labor-market tightness in the recent spike

The San Francisco Fed letter directly analyzes the recent spike and estimates that about **one-fifth of the easing in labor-market tightness in 2023** can be attributed to the spike in immigration. [SOURCE: https://www.frbsf.org/research-and-insights/publications/economic-letter/2024/07/recent-spike-in-immigration-and-easing-labor-markets/]

What changed:

1. Focus shifts from wages to **vacancies/unemployment/tightness**.
2. It is explicitly about the **postpandemic surge**.

What it still misses:

1. not a welfare or local-capacity model
2. no threshold structure

### 5) Dallas Fed 2024 — surge composition and inflation

This paper is one of the best examples of the new literature. It is explicitly about the **postpandemic unauthorized immigration surge**, uses administrative and court data, and builds a model around two empirical facts: the new immigrants are **low-skilled** and **hand-to-mouth**. It concludes that the surge had **little effect on inflation**, because extra supply was largely offset by extra demand. [SOURCE: https://www.dallasfed.org/~/media/documents/research/papers/2024/wp2407.pdf]

What changed:

1. The paper is built around the **current surge composition**, not generic immigrants.
2. It treats immigration as both a **supply and demand shock**.

What it still misses:

1. the model shock is calibrated to a surge in population growth, but not to **local capacity breakpoints**
2. the outcome is inflation, not local welfare/crowding

### 6) CBO 2025 — state and local budgets

This is the cleanest official answer to the user's threshold concern so far. CBO estimates that the surge added **4.4 million** people to the U.S. resident population in 2023 and imposed a **$9.2 billion direct net cost** on state and local governments, with the main spending categories being **education, shelter and related services, and border security**. [SOURCE: https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf]

What changed:

1. The literature finally measures **local surge-era budget strain** in an official framework.
2. The burdens are not just “cash welfare”; they are concentrated in **education, shelter, and border-response systems**.

What it still misses:

1. one-year snapshot
2. still not a formal nonlinear threshold estimator

### 7) St.Clair 2024 — Mariel and local government finances

This paper revisits Mariel, but with a new outcome: **local government budgets**. It finds increased **per-pupil education costs** financed by higher state transfers, with effects persisting for at least ten years. [SOURCE: https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift_6.pdf]

What changed:

1. Even the old canonical shock is now being re-studied through **fiscal** rather than purely wage effects.
2. This is strong evidence that earlier labor-market nulls did not settle the local-incidence question.

What it still misses:

1. still one historical case
2. not a threshold model

### 8) Meyer, Wyse, Williams 2025 — asylum seekers and homelessness

This is one of the closest papers to the user’s actual concern. It finds that asylum seekers accounted for about **60 percent of the two-year rise in sheltered homelessness** between 2022 and 2024, with the rise heavily concentrated in **New York City, Chicago, Massachusetts, and Denver**. [SOURCE: https://www.nber.org/papers/w33655]

What changed:

1. The literature now studies **specific local systems** that can saturate.
2. This is much closer to a **capacity / convex-cost** story than the classic wage papers.

What it still misses:

1. it is not a general threshold estimator with identified breakpoints
2. it focuses on shelter/homelessness, not the full destination welfare ledger

### 9) 2025 shelter-price paper — heterogeneity by permits and immigrant education

The 2025 shelter-price paper is another major update relative to Saiz-style old results. It finds that a **1 percent immigrant inflow relative to county population** is associated with **3.5 percent higher median house prices and 2.0 percent higher rents** on average, and that in counties with **the most restrictive permitting and the highest-education immigrants**, the price effect can be **6 to 8 percent**. [SOURCE: https://www.sciencedirect.com/science/article/abs/pii/S0014292125002648]

What changed:

1. housing incidence is modeled with much richer heterogeneity
2. supply conditions now matter explicitly

What it still misses:

1. still interaction heterogeneity, not discrete thresholds
2. not directly a shelter-capacity or school-capacity model

### 10) Borgschulte, Cho, Lubotsky, Rothbaum 2025 — next generation

This NBER paper studies children of U.S.-born parents in immigrant-receiving cities and finds that immigration raises outcomes for those from poorer households and lowers them for those from more affluent households, increasing **intergenerational mobility** overall. [SOURCE: https://www.nber.org/papers/w33961]

What changed:

1. The literature is now tracking **distributional and intergenerational** effects inside the receiving population.
2. This is far beyond the old “average wage” frame.

What it still misses:

1. it is not about the 2021-2024 surge specifically
2. still no explicit threshold model

### 11) FRBSF 2026 — unauthorized worker flows and local employment

This letter uses newly constructed unauthorized immigrant worker flows and finds a roughly **one-for-one** effect on local employment growth during both the rise and slowdown periods, with strong effects in **construction and manufacturing**. [SOURCE: https://www.frbsf.org/research-and-insights/publications/economic-letter/2026/02/unauthorized-immigration-effects-on-local-labor-markets/]

What changed:

1. It directly studies the **rise and slowdown** of recent unauthorized flows.
2. The local labor market outcome is employment, not only wages.

What it still misses:

1. still no local-capacity threshold estimation
2. not a full welfare ledger

## So did the literature change?

Yes, in three clear ways.

### 1) The outcome space widened

Old:

1. wages
2. unemployment
3. productivity

New:

1. labor-market tightness
2. inflation
3. housing/shelter prices
4. local public goods
5. local budgets
6. homelessness/shelter systems
7. intergenerational mobility

### 2) The composition question got sharper

Newer work is much more willing to distinguish:

1. authorized vs unauthorized
2. asylum seekers vs economic migrants
3. low-skilled vs high-skilled
4. hand-to-mouth vs wealthier consumers
5. counties with elastic vs inelastic housing supply

That is a real advance over the older “immigration” blob.

### 3) The literature got more realistic about local incidence

The strongest recent shift is not that economists suddenly became anti-immigration. It is that they increasingly admit the relevant question is not just:

`Does GDP go up?`

It is also:

`Who pays, where, and through which local systems?`

## Did the literature solve surge and threshold effects?

### Surge effects

Partly yes.

The recent literature now has genuine surge-specific work:

1. CBO 2024 federal/macroeconomy
2. CBO 2025 state/local budgets
3. Dallas Fed 2024 inflation implications of the surge
4. FRBSF 2024 and 2026 on labor-market tightness and local employment
5. NBER 2025 on asylum seekers and homelessness

So the answer on **surge effects** is: **much better modeled than before**.

### Threshold effects

Mostly no.

I did **not** find strong recent economist papers that estimate:

1. a sharp immigrant-share breakpoint where effects flip
2. convex local costs after occupancy/shelter/school utilization passes a threshold
3. political backlash thresholds of the form “below X no effect, above Y large effect”
4. a unified structural model of housing + public finance + politics + labor absorption with explicit nonlinear breakpoints

What I found instead:

1. **episode studies** of large waves
2. **linear or semi-linear IV regressions**
3. **interactions** with housing supply, skill mix, or migrant type
4. **concentrated-case studies** like asylum shelters

That is better than the old literature, but it is not the same as estimating threshold functions.

## Best current answer to the user's intuition

The user's intuition is basically right.

The recent literature now captures:

1. that the **recent surge is different**
2. that **local systems** matter
3. that **housing and shelter** can bind
4. that **skill mix and legal category** matter

But it still mostly does **not** capture the full nonlinear story:

1. once a city goes from mild inflow to emergency shelter overflow
2. once school systems hit seat and staffing constraints
3. once shelter law or right-to-shelter rules create high marginal public cost
4. once public opinion flips after visible service overload

Those are closer to **capacity models** and **political threshold models** than to standard immigration regressions.

## Verdict

If the question is:

`Did economists in the last three years update relative to the old literature?`

The answer is **yes**.

If the question is:

`Did they fully solve surge immigration and threshold effects?`

The answer is **no**.

The literature is now:

1. better on **recent surge composition**
2. better on **local budgets and housing**
3. better on **heterogeneity**
4. still weak on **explicit nonlinear thresholds**

## Highest-value next question

The next useful research step is not another generic “does immigration lower wages?” paper.

It is:

`Under what local housing, shelter-law, school-capacity, and migrant-composition conditions do inflows produce convex public costs rather than smoothly absorbed adjustment?`

That is where the current literature is still thin.

## Sources used

1. IMF 2023, *The Macroeconomic Effects of Large Immigration Waves*  
   https://www.imf.org/-/media/files/publications/wp/2023/english/wpiea2023259-print-pdf.pdf
2. Mayda, Senses, Steingress 2023, *Immigration and Provision of Public Goods: Evidence at the Local Level in the U.S.*  
   https://www.bankofcanada.ca/wp-content/uploads/2023/11/swp2023-57.pdf
3. CBO 2024, *Effects of the Immigration Surge on the Federal Budget and the Economy*  
   https://www.cbo.gov/system/files/2024-07/60165-Immigration.pdf
4. FRBSF 2024, *Recent Spike in Immigration and Easing Labor Markets*  
   https://www.frbsf.org/research-and-insights/publications/economic-letter/2024/07/recent-spike-in-immigration-and-easing-labor-markets/
5. Dallas Fed 2024, *The Postpandemic U.S. Immigration Surge: New Facts and Inflationary Implications*  
   https://www.dallasfed.org/~/media/documents/research/papers/2024/wp2407.pdf
6. CBO 2025, *Effects of the Surge in Immigration on State and Local Budgets in 2023*  
   https://www.cbo.gov/system/files/2025-06/61256-immigration-state-local.pdf
7. St.Clair 2024, *The Fiscal Effects of Immigration on Local Governments: Revisiting the Mariel Boatlift*  
   https://wagner.nyu.edu/files/faculty/publications/Mariel%20Boatlift_6.pdf
8. Meyer, Wyse, Williams 2025, *Asylum Seekers and the Rise in Homelessness*  
   https://www.nber.org/papers/w33655
9. 2025, *Immigration and U.S. shelter prices: The role of geographical and immigrant heterogeneity*  
   https://www.sciencedirect.com/science/article/abs/pii/S0014292125002648
10. Borgschulte, Cho, Lubotsky, Rothbaum 2025, *Immigration and Inequality in the Next Generation*  
    https://www.nber.org/papers/w33961
11. FRBSF 2026, *Unauthorized Immigration Effects on Local Labor Markets*  
    https://www.frbsf.org/research-and-insights/publications/economic-letter/2026/02/unauthorized-immigration-effects-on-local-labor-markets/
