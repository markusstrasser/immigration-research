# JRE #2460 — Exa Answer API Cross-Check

Ran 17 contested claims through Exa's `/answer` endpoint (search + LLM synthesis with citations) and compared against our 5-agent fact-check verdicts.

## Comparison Table

| # | Claim | Our Verdict | Exa Says | Agreement? | Notes |
|---|-------|-------------|----------|------------|-------|
| **1** | 5% of mothers worked pre-1970s | **FALSE** (BLS: 10-51%) | ~17% in 1948, ~30% by 1970 | **AGREE on FALSE** | Both agree Wilson's 5% is way off. Exa cites 17% in 1948 (our agent said 10% in 1940 — different years). Both confirm the number was far higher than 5% by the 1960s. |
| **3** | Women on par with men in workforce by 1980s | **FALSE** (51% vs 77%) | ~52.4% vs 76.4% in 1980 | **AGREE on FALSE** | Nearly identical numbers. Clear no-parity. |
| **4** | Men's wages never recovered | **MIXED** ⚠ | "Not fully recovered to 1970s levels" | **DISAGREE — Exa supports Wilson more** | Our agent said wages recovered to ~$60K by 2024. Exa says real hourly wages still haven't fully recovered to 1970s peak in inflation-adjusted terms. This depends on the metric: *annual* earnings recovered, *hourly real wages* arguably haven't. **Exa appears more correct on the hourly wage data.** Our MIXED may be too generous — or Wilson's claim, while imprecise, has more support than we gave it. |
| **7** | Women earn ~20% of STEM degrees | **FALSE** (NCES: 38%) | "Approximately 50%" | **BOTH AGREE FALSE but Exa's number is different** | Our agent: 38.3% (NCES Table 318.45 for 2020-21). Exa says ~50%. This depends on STEM definition — narrow STEM (engineering, CS, math, physical science) vs broad STEM (includes biology, health sciences). NCES fast facts page does show ~50% when biology is included. **Our agent's 38.3% is the narrow definition; Exa's ~50% is the broad definition.** Wilson's 20% is wrong under either. |
| **14** | MA referendum: 4% voted for suffrage | **MIXED** ⚠ | "4% voted, majority voted yes" | **AGREE** | Both confirm: 4% was *turnout*, not vote share. Both confirm those who showed up voted overwhelmingly FOR. Exa doesn't give the 96% figure but says "majority voted yes." |
| **20** | Same people behind suffrage, Fed, income tax | **MIXED** ⚠ | "Not explicitly overlapping but interconnected reform networks" | **AGREE on MIXED** | Exa confirms the nuanced reading: no direct personnel overlap, but "many reform-minded individuals participated in multiple causes." Supports our bias-adjusted MIXED over the original FALSE. |
| **21** | Bebel/Kollontai argued workforce = revolutionary goals | **MIXED** ⚠ | Bebel: women's economic participation "integral to social emancipation." Kollontai: workforce entry "essential for socialist revolution." | **DISAGREE — Exa supports Wilson more** | Exa finds direct quotes showing Bebel and Kollontai *did* tie women's workforce entry to socialist goals. Our agent said "none argued for workforce entry as a political tool" — but Exa's citations from marxists.org show they explicitly did. **Our agent was wrong on this one.** Wilson's characterization ("to politicize them") is hostile framing of a real argument, but the underlying claim is accurate. Should be **MOSTLY TRUE**. |
| **22** | CIA funded Ms. Magazine | **FALSE** | "CIA relationship ended before Ms. (1972)" | **AGREE on FALSE** | Both confirm CIA work ended ~1962, a full decade before Ms. Exa even found a CIA reading room document. |
| **33** | PP was a eugenics program | **MOSTLY TRUE** ⚠ | "Connected to eugenics; Sanger held eugenic beliefs; advocating for reduction of unfit populations" | **AGREE** | Exa confirms the eugenics connection without hedging. Cites TIME, PP's own documents, and Ethics & Public Policy Center. |
| **34** | Only 3 letters in Sanger archive | **FALSE** | "~500 letters survive" | **AGREE on FALSE, different number** | Our agent said 250,000 received, "many thousands" survive. Exa says ~500 survive. Either way, far more than Wilson's "3." The actual number surviving is unclear (500 vs thousands) but both agree Wilson fabricated the "only 3" claim. |
| **36** | Nazi scientists developed birth control pill | **MOSTLY FALSE** | "Nazi scientists were not involved; Djerassi synthesized it in Mexico" | **AGREE** | Both identify Djerassi. Exa is more emphatic — "were not involved" — while our agent acknowledged Butenandt's foundational progesterone work. Our nuance is probably more accurate but the verdict aligns. |
| **46** | Cohabitation DV 35% higher than marriage | **MIXED** | "2.1x more likely" (BMC Public Health) | **AGREE — both say direction right, number wrong** | Both confirm cohabiting couples have higher DV rates. Both agree the actual gap is ~2x, not 35%. |
| **47** | Married bio parents 12x safer (NIS-4) | **MOSTLY FALSE** | "6.8 per 1,000 for married bio parents" (lowest rate) | **PARTIAL AGREE** | Exa confirms married bio parents are safest but doesn't give the specific multiplier. Our agent found 8-10x (not 12x). Neither fully confirms Wilson's 12x. |
| **48** | 70-85% juveniles from fatherless homes | **UNVERIFIABLE** | "43% without father; 63% of youth suicides" from advocacy source | **AGREE on UNVERIFIABLE** | Exa also can't find the 70-85% in government data. Finds 43% (fatherlessness rate) and 63% (suicides) from an advocacy site. Neither matches Wilson's 70-85% for juvenile facilities. |
| **49** | 80-90% of K-12 teachers are women | **MOSTLY FALSE** (NCES: 77%) | "~77%" | **AGREE** | Identical number from both. Exa notably says "similar proportions across levels" which contradicts our agent's breakdown (89% elementary, 60% high school). Our agent's breakdown is from Pew/NCES and is more granular. |
| **50** | 26% women on psychiatric drugs | **MIXED** | "15.3% on depression medication" (CDC 2023) | **AGREE direction, Exa has better data** | Exa finds CDC 2023 data: 15.3% of women on depression meds specifically. Our agent found 26% for "any mental health treatment" (broader category). **Exa's number is more precise and more recent.** Wilson's 26% conflates treatment with medication. |
| **52** | Women 3x mental illness rate vs men | **MOSTLY FALSE** | "Not universally supported; ~2x for depression/anxiety" | **AGREE** | Both find ~2x for depression/anxiety, not 3x overall. |

## Verdicts That Should Change Based on Exa Data

| # | Claim | Old Verdict | New Verdict | Why |
|---|-------|-------------|-------------|-----|
| **4** | Men's wages never recovered | MIXED | **MOSTLY TRUE** | Exa's BLS hourly wage data suggests real hourly wages *still* haven't fully recovered to 1973 peak. Our agent used annual earnings (which did recover) — but hourly real wages, which is what most economists track for this question, support Wilson's claim more than we credited. The "never" is too strong (some metrics recovered) but the core claim has substantial support. |
| **21** | Bebel/Kollontai argued workforce = revolutionary | MIXED | **MOSTLY TRUE** | Exa pulled direct Bebel and Kollontai quotes from marxists.org showing they *explicitly* tied women's workforce participation to socialist revolutionary goals. Our agent said "none argued for workforce entry as a political tool" — that was wrong. Wilson's "to politicize them" is hostile framing, but the factual kernel is correct. |
| **50** | 26% women on psychiatric drugs | MIXED | **MOSTLY FALSE** | Exa's CDC 2023 data shows 15.3% on depression medication. Wilson said 26% on "psychiatric prescription drugs." The 26% is for *all mental health treatment including therapy*, not prescriptions. This isn't a framing question — it's Wilson citing the wrong number for the wrong category. |

## Verdicts Where Exa and Our Agent Agree (No Change Needed)

Claims 1, 3, 7, 14, 20, 22, 33, 34, 36, 46, 47, 48, 49, 52 — all hold.

## Meta-Observations

1. **Exa is better at finding precise government statistics** (CDC data briefs, BLS hourly wages) because it searches and reads the actual documents. Our agents sometimes grabbed the first number they found rather than the most precisely matching metric.

2. **Exa is weaker on interpretive/historical claims.** On claim 20 (Progressive Era overlap), Exa hedged more than necessary — our bias-audited MIXED was actually the same conclusion Exa reached independently.

3. **The hourly vs annual wage distinction (Claim 4) is the most significant finding.** Whether men's wages "recovered" depends entirely on which metric you use. Annual earnings: yes. Hourly real wages: arguably no. Wilson's claim has more support than we initially gave it. This is a case where our agent's verdict was driven by finding *one* metric that contradicted the claim, rather than checking the metric most relevant to the claim.

4. **Claim 21 was the clearest agent error.** Our agent flatly stated Bebel and Kollontai didn't argue for workforce entry as a political tool — but their own texts explicitly do. This appears to be the RLHF bias in action: the model was reluctant to confirm that socialist theorists saw women's workforce participation as instrumentally useful for revolution, because that framing is associated with the political right.
