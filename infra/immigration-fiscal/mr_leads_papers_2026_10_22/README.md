**Verdict:** two NBER papers Marginal Revolution posted on 2026-10-20 and 2026-10-21, read in full; neither
moves the main case. Memo: [research/immigration-marginal-revolution-leads-2026-10-22.md](../../../research/immigration-marginal-revolution-leads-2026-10-22.md).

# Marginal Revolution leads, 2026-10-22

No scripts. The PDFs were downloaded from NBER and converted with `pdftotext -layout`; both sit in the
ignored `_cache/`. Page numbers below are PDF pages of those files. Every number used in the memo is
quoted here from the text.

| File | Source | sha256 |
|---|---|---|
| `_cache/w35901.pdf` | Battisti, Peri & Romano, "Modeling and Evaluating the Labor Market and Fiscal Effects of Immigration", NBER w35901 (October 2026), https://www.nber.org/papers/w35901 | `84b0379a48f883c785f60251289cef2c40cbc525da66670ae22c01eee0e75ed5` |
| `_cache/w35900.pdf` | Hassan, Kalyani & Lopez Del Valle, "Foreign Giants' Broad Shoulders: The Causal Effect of Foreign Ideas on U.S. Innovation", NBER w35900 (October 2026), https://www.nber.org/papers/w35900 | `e6306a07c38d96606774ecc6724263e901c7dbb94f40753c3053b52b8a9c22da` |

Re-fetch: `curl -sL -o _cache/w3590N.pdf https://www.nber.org/system/files/working_papers/w3590N/w3590N.pdf`.

## Battisti, Peri & Romano (w35901)

- p. 4, mechanism: "as immigrants are hired at lower wages in most countries, because they bargain from a weaker
  outside option, and especially where unemployment rate is high, ﬁrms post more vacancies as a consequence of
  larger immigrant inﬂows."
- p. 4, US: "The United States lies at the other extreme: narrow wage gaps and low unemployment mute the labor
  market channel, while low tax progressivity and a small public sector mute the ﬁscal channel, so both are weak
  and the overall welfare eﬀect is small."
- p. 5: "The United States shows a modest +0.07 percent."
- p. 18, scenarios: each adds one percentage point to the labor force; Scenario 3 is "an inﬂow that is twice as
  intensive in low- and medium-skilled workers relative to the stock of natives".
- p. 21, Table 6, United States (WN / WLN / WHN): Scenario 1 0.00% / 0.02% / −0.02%; Scenario 2 0.13% / 0.32% /
  −0.06%; Scenario 3 −0.10% / −0.20% / 0.00%. Welfare is "percentage variations in steady-state consumption
  equivalents" (p. 18).
- p. 21: "the response operates almost entirely through the labor market rather than through the ﬁscal channel,
  which is limited by the small size of government and the low progressivity of the tax system."
- p. 6, Table 1 line [9]: pure public good share of government spending, maximum 20.7% (US).
- p. 27: "because the pure public good ḡ is ﬁxed in aggregate and provided by the government, immigration
  broadens the tax base that ﬁnances it."
- p. 30, Table 7, United States: residents 0.694 low-skilled / 0.306 high-skilled; 2019–2024 arrivals 0.614 /
  0.386. High-skilled means a tertiary degree.
- p. 32, Table 8, United States, 2019–2024 flow mix (WN / WLN / WHN): 0.07% / 0.18% / −0.04%.

## Hassan, Kalyani & Lopez Del Valle (w35900)

- p. 2: "54% of U.S. technologies build on at least one foreign input" (the CEPR DP22034 version says 56%).
- p. 11: "Overall, 20,786 technologies reach this threshold, with birth years between 1887 and 2024; of these,
  1,448 (7.0%) were born abroad. Japan (40%), Germany (25%), and the United Kingdom (11%) account for the
  majority". Origin is "the first country whose inventors file 10 patents mentioning it".
- p. 58, Table A.2: Japan 582, Germany 356, United Kingdom 162, France 59, Canada 49, … India 8, Spain 3, "Others
  (≤ 2 each)" 8; total 1,448. Mexico is not listed, so it has at most two.
- p. 7: "allowing recent immigration from the origin country, or ancestry itself, to affect invention directly
  barely changes the effect of having the specific inputs at hand—and ancestry itself has no effect once those
  inputs are there."

## Comparison inputs

- NAS (2017), *The Economic and Fiscal Consequences of Immigration*, p. 171: immigrants' 16.5% of hours "generated
  an immigration surplus of $54.2 billion, representing a 0.31 percent overall increase in income that accrues to
  the native population", estimates that "can at best be described as upper limits".
  https://nap.nationalacademies.org/read/23550/chapter/8
- 2024 GDP $29,300bn: `closed_budget_2026_10_06/closed_budget.py` `GDP_2024_BN` (BEA NIPA T1.1.5, 26 August 2026
  vintage).
- The union's BA share among positive earners, 0.190 against 0.433 for everyone else:
  `matched_benefits_2026_09_19/derived/skill_composition.csv`, proxy PEARNVAL, split `below_ba`, skill 1
  `positive_earners` over the group's total.
- Scenario 3 at the paper's own US resident mix: half of 0.306/0.694 is 0.2205, so 18.1% with a degree. The union's
  19.0% sits at it; only against the survey's 43.3% is it clearly below. The two baselines differ in sample
  (residents against positive earners) and definition (tertiary against BA).
