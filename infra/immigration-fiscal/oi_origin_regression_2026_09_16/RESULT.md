# Regression toward which mean? Second-generation income rank by parent income and country of origin

**Verdict:** The claim reproduces in the public Opportunity Insights country-of-origin tables, with a
sign that depends on origin. Every immigrant-origin group has a flatter child-rank-on-parent-rank
slope than children of US-born parents (0.69–1.38 percentile points per parent ventile against 1.65
for the USA), so second-generation outcomes regress toward a group-specific mean rather than the
national one. At the top of the parent distribution (ventiles 17–20) sons of Indian and Chinese parents
still rank 8.1 and 7.1 points above sons of equally rich US-born parents, while sons of Mexican,
Guatemalan, Jamaican and Haitian parents rank 4.2, 4.9, 6.6 and 8.3 points below. At the bottom
(ventiles 1–4) every origin outranks US-born-parent children, Mexico by +5.6, but that bottom premium
is partly the US-born comparison pooling Black natives, who dominate the bottom ventiles. [INFERENCE]

Model self-report: parent session, claude-fable-5-1.

Data [SOURCE: https://opportunityinsights.org/wp-content/uploads/2019/08/race_table6b_nonpar.csv and
race_table6a_parametric.csv; Chetty, Hendren, Jones & Porter 2020 online tables; children born
1978–83, parents' country of origin from the father's 2000 long-form / ACS record; income ranks
2014–15]. Script `origin_regression.py`; outputs `origin_regression_by_ventile.csv`, `origin_p25_p75.csv`.

Sons' rank minus US-born-parent sons' rank at the same parent ventile, percentile points (n = sons):

| origin | n | bottom v1–4 | mid v9–12 | top v17–20 | slope/ventile |
|---|---|---|---|---|---|
| India | 6,120 | +18.7 | +15.4 | +8.1 | 0.98 |
| China | 4,190 | +18.6 | +14.0 | +7.1 | 0.82 |
| Italy | 7,320 | +11.7 | +7.8 | +4.6 | 1.09 |
| Cuba | 5,050 | +6.3 | +1.4 | +2.3 | 1.36 |
| Vietnam | 4,250 | +15.7 | +8.2 | +1.6 | 0.69 |
| Germany | 14,700 | +5.0 | +0.6 | −0.5 | 1.24 |
| Philippines | 10,700 | +9.2 | +2.4 | −0.7 | 1.00 |
| El Salvador | 2,620 | +8.2 | +0.5 | −3.5 | 0.92 |
| **Mexico** | **63,000** | **+5.6** | **+1.3** | **−4.2** | **1.04** |
| Guatemala | 1,460 | +8.2 | +3.3 | −4.9 | 0.79 |
| Jamaica | 1,930 | +0.9 | −7.0 | −6.6 | 1.27 |
| Haiti | 1,750 | +4.7 | −4.7 | −8.3 | 0.86 |
| USA | 2,861,500 | 0 | 0 | 0 | 1.65 |

Table 6a parametric, predicted son rank at parent p75: India 73.0, China 71.7, Italy 68.0, USA 62.2,
Mexico 60.4, Guatemala 60.2, Dominican Republic 59.1, Jamaica 55.2, Haiti 53.9. At parent p25 every
origin with n ≥ 1,000 except Trinidad, Jamaica and Haiti is above the USA's 45.8 (Mexico 49.8).

Reading. This is Borjas's 1992 "ethnic capital" pattern measured on 2.9 million linked tax records:
conditional on parent income, the second generation converges toward its origin group's mean, and the
groups differ in where that mean sits. It is consistent with the account's regression-to-the-mean
framing but does not identify the mechanism: selection on unobservables (a high-rank Mexican parent
is less positively selected on the traits that transmit than a high-rank Indian parent, whose
immigration was skill-screened), ethnic-enclave labour-market effects, family size, and the composition
of the US-born comparison group all produce the same table. The USA row pools all races; against
white-only US-born parents the bottom-ventile immigrant premiums would shrink and the top-ventile
Mexican deficit would likely widen (Chetty et al. show white sons outrank the pooled mean at every
percentile). [INFERENCE] Not testable here: third generation (the table is second generation only),
outcomes other than income rank, and the white-only comparison (not published by country of origin).
