# Scott Sumner immigration claims audit — 2026-09-22

**Verdict:** The pasted critique is mostly right about what Sumner's evidence can and cannot
reach, and wrong in three places about what he wrote. Every CBO and Caiumi–Peri number it
quotes is on the page, verbatim. Its Social Security sentence does not exist: Sumner wrote
"Immigration helps our economy, especially programs such as Social Security" in a 2018 comment,
and when he names a best fix for Social Security it is spending cuts and a carbon tax. Its
"$1.5 trillion" Trustees figure is not in the report, which gives 0.38% of taxable payroll,
about $2.6 trillion of a $22.6 trillion 75-year shortfall on the report's own anchors. Its
Phillips-curve paragraph attributes a supply-shock and nominal-GDP-targeting frame that the
post does not contain. The rest is cosigned with scope corrections: the surge score is a
federal ten-year flow of all origins (FAQ 16), the wage result is a level that cannot close an
annual account, the "undeniable" second-generation claim is a commenter's and the ledger and
the new second-generation lane both say the second generation does not flip, and the 110
million counterfactual is a levels story that does not identify the fiscal derivative.

September 22, 2026. Frame: a claim audit against Sumner's own pages, not an evaluation of
Sumner. Method: nine claims from the pasted text were sent to a verification agent with the
rule that every quote must come from a fetched page body (live or the Wayback raw body); the
notes are in `notes/sumner-claims-verification-2026-09-22.md`. This memo re-fetched three of
the pages (the February 2024 post with its comments, the May 2024 Phillips-curve post, the 2018
Econlib post with its comments) and found every quoted sentence where the notes said it was;
the Trustees table values are the agent's transcription of the 2024 report PDF and the dollar
conversion is a calculation on two published anchors. The pasted critique is graded in the
operator's terms: cosign, throw out, or complement.

## Primary texts

1. "Yes, it was immigration", TheMoneyIllusion, 10 Feb 2024, with comments of 15 Feb 2024.
   [SOURCE: https://www.themoneyillusion.com/yes-it-was-immigration/]
2. "America, but with fewer immigrants", Econlib, 30 Apr 2024.
   [SOURCE: https://www.econlib.org/america-but-with-fewer-immigrants/]
3. "More immigration please (making America great again)", TheMoneyIllusion, 23 May 2016.
   [SOURCE: https://www.themoneyillusion.com/more-immigration-please-making-american-great-again/]
4. "Immigration, wages, and the Phillips Curve", TheMoneyIllusion, 3 May 2024, with comments.
   [SOURCE: https://www.themoneyillusion.com/immigration-wages-and-the-phillips-curve/]
5. "Us and them", Econlib, 27 Jun 2018, with Sumner's comment of 29 Jun 2018; "Higher Taxes or
   Lower Benefits?", Econlib, 27 Mar 2024, with his comment of the same day.
   [SOURCE: https://www.econlib.org/us-and-them/]
6. "Immigration and housing prices", TheMoneyIllusion, 4 Sep 2010.
   [SOURCE: https://www.themoneyillusion.com/immigration-and-housing-prices/]
7. Caiumi and Peri, NBER w32389 (2024), abstract. [SOURCE: https://www.nber.org/papers/w32389]
8. 2024 OASDI Trustees Report, overview and Table VI.D3 (p. 190).
   [SOURCE: https://www.ssa.gov/OACT/TR/2024/tr2024.pdf, fetched through the Wayback raw body]

## Claim by claim

| # | The pasted claim | What the page says | Grade |
|---|---|---|---|
| 1 | Feb 2024: Sumner quoted CBO (labor force +5.2M by 2033, GDP +$7tn, revenue +$1tn over 2024–34) and wrote "Our budget deficit was reduced by the recent wave of immigration." | All three CBO numbers are verbatim, for **2023 to 2034**; the post is one line plus the CBO block quote, whose last sentence is CBO's "We are continuing to assess the implications of immigration for revenues and spending." The deficit sentence is Sumner's **comment** of 15 Feb 2024, not post text. | **Cosign**, with the period and placement corrected. Routed to FAQ 16. |
| 2 | Apr 2024: he cited Caiumi–Peri, +1.7–2.6% on less-educated natives' wages 2000–2019 "thanks to native-immigrant complementarity and college skill content of immigrants", no crowding out. | Verbatim, and the abstract at NBER is word for word the text he block-quotes; his own contribution is "[Emphasis added]" on the complementarity clause. "No significant crowding out effects on employment" belongs to the 2019–2022 simulation, not the headline estimate. College-educated natives: "no significant wage effect", a null. | **Cosign** the reading that it is a wage level, not a fiscal flow. **Complement**: the complementarity half of the mechanism is now executed on the account's own data (ladder 176), so "wrong population" applies to the college-content half only. |
| 3 | 2016: he wants about 3 million immigrants a year and "a better balance of skilled and unskilled, so that the people at the bottom in America are not bearing the brunt of the competition for jobs." | Verbatim, 23 May 2016. "3 million a year is a good start" is a floor, and the post's PPS proposes 1% of population a year. Same post: the low-skill wage argument "may have a bit of merit, which is why we might want to consider adjusting the mix". | **Cosign.** |
| 4 | A commenter he was answering said the first generation is "nuanced" and for later generations "the net benefit seems undeniable"; Sumner replied without correcting it. | The commenter is Michael Sandifer (15 Feb 2024), replying to Lizard Man's fiscal objection. Sumner's only line in that exchange, 51 minutes later, is addressed to Lizard Man. He did not correct Sandifer, in the weak sense that he posted in the thread and let it stand. | **Throw out** as a claim about Sumner. **Keep** the substance: FAQ 5's same-age gaps (−$7,584, −$7,521, −$6,195) and ladder 178's closing ratios (76% of the no-high-school gap, 31% of the college gap) both say the second generation does not flip. |
| 5 | Housing: his "classroom case" is Hispanic immigration plus tight zoning raising prices in California, Nevada, Arizona and Florida but not Texas. | The 2010 post argues from the other direction: a slowdown "concentrated in illegal immigrant-rich areas with fast population growth (California's Inland Empire, Arizona, Nevada, etc) … could have had a significant effect on local markets". The elastic-Texas sentence on that page ("only true if supply is constrained … Texas has high population growth and no significant bubble") is a **commenter's**. The four-state-versus-Texas formulation was not found in his text. | **Partial.** The direction is his; the tidy formulation is the critique's. The repo agrees housing is unpriced on both sides (FAQ 4) and is measuring the metro incidence now (`housing_supply_ca_tx_2026_09_22`). |
| 6 | Under nominal-GDP targeting immigration is a supply shock; hourly wages lag nominal GDP while real output rises, so disinflation without a recession. | The post has "wages are about 8% above pre-Covid trend and NGDP is about 10% above trend", "the first recession-free disinflation" hedged twice with "might", and in comments "it depressed wages relative to NGDP". It has no "supply shock", no NGDP-targeting frame (the phrase appears only in a commenter's question, which Sumner declines), no real-output claim, and it closes with "Fed policy has been roughly 8% to 10% too expansionary over the past 5 years." | **Throw out** the attribution; the paragraph merges this post with a July 2024 Econlib post and adds a frame. The inference the critique draws, that a macro stabilisation point does not enlarge the production term, is the critique's own and is fine as such. |
| 7 | "Immigration is the best solution to financing Social Security and Medicare." | **Not found.** His sentence, in a 29 Jun 2018 comment: "Immigration helps our economy, especially programs such as Social Security." No Medicare, no "best". On 27 Mar 2024, asked about Social Security, he wrote that "the best approach is to do things that would make sense even if we did not have a Social Security crisis, such as cutting wasteful spending throughout the federal budget and implementing a carbon tax." | **Throw out** the quote. A commenter on the 2018 thread rebuts the line with "it is likely false that immigration helps Social Security"; that is not Sumner's either. |
| 8 | The Trustees' sensitivity: a larger immigration path moves the 75-year shortfall by about $1.5 trillion on a gap of about $23 trillion. | Table VI.D3: 75-year actuarial balance −3.90 / −3.50 / −3.12% of taxable payroll at 829k / 1,244k / 1,683k average annual net immigration; +100k a year improves the balance by about 0.09% of payroll. The report gives no dollar figure for the sensitivity. The open-group unfunded obligation is 3.32% of payroll and $22.6 trillion. | **Correct the number.** High minus intermediate is 0.38% of payroll; on the report's two anchors that is about **$2.6 trillion**, 10.9% of the 3.50% deficit `[CALCULATION: 0.38 × 22.6 / 3.32; assumes the balance and the obligation share the payroll base, which they do by construction]`. "$1.5 trillion" understates it by about 40%; the qualitative point survives. The age point (FAQ 1: the young structure is worth about $4,600 a year and the gap grows at common ages) stands. |
| 9 | The 110-million counterfactual: America is as rich as it is because it is large. | Verbatim in the Econlib post of 30 Apr 2024, not TheMoneyIllusion, and framed as a question to immigration opponents after the outlier fact (US GDP per capita $85,373 against Taiwan's $77,858 next). "Because it is large" is the implied direction, not a sentence. | **Cosign** the reading that a two-century levels story does not identify a fiscal derivative, and that it counts the immigrants' own gains. The scale channel is unpriced here in both directions (ladder 101: agglomeration cost unestimated). |

## What the critique adds, and what it does not

The useful part is the accounting discipline, and it is right: the surge score, the wage level
and the levels counterfactual are three different objects, none of them the annual position of
a resident population with state and local services included, and none can be netted against
$165–197bn (see "Before combining numbers" in the [FAQ](immigration-objections-faq-2026-09-21.md)).
That point is now an FAQ entry (16) because a reader raises it first.

The weak part is attribution. Three of its Sumner sentences are paraphrases dressed as quotes,
one of them (Social Security) contradicted by what he actually recommends. A commenter's
"undeniable" is not evidence about Sumner. The Phillips-curve paragraph is a composite. The
critique's own inferences, that a macro point does not enlarge the production term and that
housing will price as a metro incidence, are reasonable and should be stated as the critique's,
not his.

One thing the critique misses: Sumner's 2016 post concedes the low-skill wage argument "may
have a bit of merit" and proposes adjusting the skill mix, which is the same distinction the
account draws between the education-specific results (FAQ 7) and the aggregate.

## Disconfirmation

- The strongest reading for the critique on claim 7: Sumner's 2018 line does credit
  immigration with helping Social Security, and the Trustees' sign agrees. What fails is
  "best solution" and "Medicare", not the direction.
- The strongest reading against this memo's claim-6 verdict: Sumner's monetary framework is
  nominal-GDP targeting, so a reader can supply the frame he leaves implicit. The audit rule
  here is what the page says, and the page declines the frame when a commenter offers it.
- The Trustees conversion assumes the actuarial balance and the unfunded obligation are on
  the same present-value payroll base. They are, by the report's definitions, but the report
  itself publishes no dollar sensitivity, so $2.6 trillion is a derived figure, not a quote.
- The 2025 Trustees Report was not re-verified; the PDF arrived truncated through the archive.
  [GAP]

**Instrument.** LLM-conducted on a charged topic; the verification agent was required to
quote only from fetched bodies, the parent re-fetched three pages, and the pasted critique's
direction was graded in both directions (its correct scope points and its wrong attributions).
See `notes/llm-bias-caveat.md`.

## Sources

- Verification notes with every quote, URL, fetch route and date:
  `notes/sumner-claims-verification-2026-09-22.md`.
- CBO 60165 (July 2024) and the $897bn covered-federal figure:
  [disconfirmers memo](immigration-economics-disconfirmers-2026-06-25.md),
  [Caplan audit](immigration-bryan-caplan-claims-audit-2026-04-21.md).
- Repo results cited: [FAQ](immigration-objections-faq-2026-09-21.md) entries 1, 4, 5, 7, 16;
  [confidence ladder](immigration-confidence-ladder.md) 101, 176, 178;
  [second generation by origin](immigration-second-generation-by-origin-2026-09-22.md).

## Revisions

- **2026-09-22 (initial).** Written from the verification notes and three parent re-fetches.
