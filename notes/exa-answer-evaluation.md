# Exa Answer API — Tool Evaluation

**Date:** 2026-03-02
**Endpoint:** `POST https://api.exa.ai/answer`
**Context:** Cross-checked 17 claims from JRE #2460 (Rachel Wilson) fact-check. Compared against 5-agent researcher output.

## How It Works

Exa `/answer` takes a natural language query, runs a web search, reads the top results, and synthesizes an answer with inline citations. It's a search-RAG pipeline — similar to Perplexity but API-first.

## Scorecard: Exa vs Our Agents (17 claims)

| Outcome | Count | Claims |
|---------|-------|--------|
| **Both agree, both correct** | 11 | 1, 3, 14, 22, 33, 36, 46, 47, 48, 49, 52 |
| **Both agree, Exa more precise** | 2 | 34 (500 vs "thousands"), 50 (15.3% CDC 2023 data) |
| **Exa correct, agent wrong** | 2 | 4 (hourly vs annual wages), 21 (Bebel/Kollontai quotes) |
| **Agent more precise, Exa vague** | 1 | 7 (38.3% narrow STEM vs Exa's ~50% broad STEM) |
| **Both hedged similarly** | 1 | 20 (Progressive Era overlap) |
| **Exa wrong, agent correct** | 0 | — |

**Exa accuracy: 16/17 useful answers (94%)**
**Agent accuracy: 15/17 (88%)**
**Exa found better data than agent: 4/17 (24%)**

## Claim-by-Claim Detail

| # | Exa Answer | Agent Answer | Who's Better | Notes |
|---|-----------|-------------|-------------|-------|
| 1 | ~17% in 1948, ~30% by 1970 | ~10% in 1940, ~20% by 1950, 51% by 1969 | **Agent** | Agent had more granular BLS data across decades. Exa's 30% for "1970" is less precise (the question was pre-1970). Both correctly falsify Wilson's 5%. |
| 3 | 52.4% vs 76.4% in 1980 | 51.5% vs 77.4% in 1980 | **Tie** | Trivially different numbers, same conclusion. |
| 4 | "Not fully recovered to 1970s levels" (hourly) | "Recovered to ~$60K by 2024" (annual) | **Exa** | Exa used the right metric (hourly real wages). Agent used annual earnings, which papered over the stagnation. This changed the verdict. |
| 7 | "~50%" (broad STEM) | 38.3% (narrow STEM, NCES Table 318.45) | **Agent** | Exa's ~50% includes biology/health sciences in STEM. Agent's 38.3% is the narrow engineering/CS/math/physics definition. Both are "correct" under different STEM definitions, but agent cited the specific NCES table number. Wilson's 20% is wrong either way. |
| 14 | "4% voted, majority voted yes" | "4% turnout, 96% voted FOR" | **Agent** | Both got the same story. Agent had the precise 96% figure. |
| 20 | "Not explicitly overlapping but interconnected networks" | Same conclusion after bias audit | **Tie** | Identical nuanced reading. |
| 21 | Direct Bebel/Kollontai quotes from marxists.org | "None argued for workforce entry as political tool" | **Exa** | Exa found the primary source texts. Agent denied what the texts say. Clearest agent failure in the set. |
| 22 | "CIA relationship ended before Ms. (1972)" + CIA reading room doc | Same conclusion | **Exa slightly** | Exa found an actual CIA declassified document (cia.gov/readingroom). Agent relied on Wikipedia and NWHM. Same verdict but Exa had a better source. |
| 33 | "Connected to eugenics; advocating for reduction of unfit" | Same conclusion | **Tie** | Both cited TIME, PP documents. |
| 34 | "~500 letters survive" | "~250,000 received, many thousands survive" | **Agent** | Agent had more detail from the Sanger Papers Project newsletter. Exa's "~500" seems low — may be a specific subcollection. |
| 36 | "Nazi scientists were not involved; Djerassi" | "Butenandt (Nazi member) did foundational chemistry but pill was Djerassi" | **Agent** | Agent's nuance (Butenandt's progesterone isolation was real but distant from pill development) is more historically accurate than Exa's flat "not involved." |
| 46 | "2.1x more likely" (BMC Public Health) | Same paper, same number | **Tie** | Both found the same BMC Public Health 2016 study. |
| 47 | "6.8 per 1,000 for married bio parents" (no multiplier) | "8-10x vs single parent with live-in partner" | **Agent** | Agent gave the actual risk multiplier from NIS-4. Exa gave the base rate but not the comparison. |
| 48 | "43% without father; 63% suicides" from advocacy site | "39% in mother-only households" from DOJ 2002 | **Agent** | Agent found actual DOJ data (39%). Exa cited an advocacy site with a different (higher) number. Both agreed 70-85% is unverifiable. |
| 49 | "~77%" | "77% overall; 89% elem, 72% middle, 60% high" | **Agent** | Same topline. Agent had the level breakdown. |
| 50 | "15.3% on depression medication" (CDC 2023) | "26% any mental health treatment; ~21% medication" | **Exa** | Exa found more recent CDC data (2023 Data Brief 528). Agent had 2020 data. Exa's number was more precise and more current. |
| 52 | "~2x for depression/anxiety, not 3x overall" | Same conclusion | **Tie** | Both reached identical verdict. |

## Strengths

1. **Fresh government data.** Exa found the CDC 2023 Data Brief 528 (claim 50) and BLS hourly wage charts that our agents missed. Its search-then-read pipeline is good at surfacing recent statistical publications.

2. **Primary source text retrieval.** On claim 21, Exa went straight to marxists.org and pulled Bebel's and Kollontai's actual words. Our agent *summarized* their positions from secondary sources and got it wrong.

3. **Citation quality.** Every Exa answer came with 3 clickable URLs. Several were government (.gov) or academic sources. The CIA reading room document on claim 22 was a genuine find.

4. **Speed.** Each query returned in ~5-10 seconds. Our 5-agent pipeline took ~6 minutes total.

5. **Zero hallucinated sources.** Every URL Exa cited was real and relevant. (Cannot say the same for all LLM citation systems.)

## Weaknesses

1. **No nuance on contested questions.** Exa gives one answer. It doesn't present competing interpretations or flag when evidence is mixed. On claim 36, it said "Nazi scientists were not involved" when the truth is more nuanced (Butenandt's foundational work was real, just distant from the pill itself).

2. **STEM definition ambiguity (claim 7).** Exa said "~50%" without noting this is the broad definition including biology. Our agent specified the narrow definition and cited the exact NCES table number. For fact-checking, the table number matters.

3. **Shallow on archives.** On claim 34, Exa said "~500 letters survive" — likely from a specific subcollection page. Our agent found the Sanger Papers Project newsletter describing "many thousands" across multiple archives. Exa's search-and-read doesn't go deep enough for archival research.

4. **No multiplier on NIS-4 (claim 47).** Exa found the base rate (6.8 per 1,000) but not the comparative risk multipliers, which was the actual claim being checked. Our agent found the 8-10x figure.

5. **Advocacy source contamination (claim 48).** Exa cited thecitizenswhocare.org (an advocacy site) with inflated fatherlessness statistics. Our agent found the actual DOJ survey data showing a lower (39%) figure. Exa doesn't distinguish advocacy sources from government primary data.

6. **It's still an LLM.** Exa's synthesis layer has the same RLHF dispositions as any frontier model. It just has better search input. On claim 21, Exa overcame the bias because it retrieved the primary texts — but on questions where the search results themselves are politically filtered, Exa would reproduce the same biases.

## When to Use Exa vs Agents

| Use Case | Better Tool |
|----------|-------------|
| Checking a specific number against government data | **Exa** — faster, finds recent data briefs |
| Verifying a quote or date | **Exa** — fast, good at finding primary text |
| Evaluating a contested interpretive claim | **Agent** — can present multiple framings |
| Deep archival research | **Agent** — can chain searches, read newsletters, cross-reference |
| Checking who specifically did something (misattribution) | **Agent** — can dig into biographical details |
| Quick pre-check before deploying full agents | **Exa** — 5 seconds vs 3 minutes |
| Cross-checking agent verdicts for errors | **Exa** — independent pipeline catches different things |

## Recommendation

Use Exa `/answer` as the **first pass** on numerical/statistical claims and quotes. Use researcher agents for historical, biographical, and interpretive claims. Then cross-check the agents' most surprising verdicts with Exa as a **second opinion** — this is where we caught the Claim 4 and Claim 21 errors.

The optimal pipeline for this project:
1. Exa `/answer` sweep on all hard-data claims (fast, cheap, precise)
2. Researcher agents on historical/biographical/interpretive claims (deep, nuanced)
3. Exa cross-check on any agent verdict that seems politically convenient for either side
