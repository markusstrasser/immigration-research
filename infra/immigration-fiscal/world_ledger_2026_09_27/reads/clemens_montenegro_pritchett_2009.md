# Clemens, Montenegro and Pritchett, "The Place Premium" (working paper)

Used for: the first generation's selection (G1_SELECTION, G2_INHERITED in g2_premium.py) and the check of the
direct 2024 ratio.

Source read: Michael A. Clemens, Claudio E. Montenegro and Lant Pritchett, "The Place Premium: Wage Differences
for Identical Workers Across the US Border", Harvard Kennedy School Faculty Research Working Paper Series
(SSRN 1211427). Local copy: `~/Projects/corpus/doi_10_2139_ssrn_1211427/parsed.marker-modal@1.10.2+gemini-3-
flash-preview+cfg-806a7815/page.md`. The published version (Review of Economics and Statistics 101(2), 2019,
titled "The Place Premium: Bounding the Price Equivalent of Migration Barriers") was not read; the figures
below are the working paper's. [UNVERIFIED: that the published tables carry the same Mexico figures]

## Quotes

1. Definition of Ro (p. 12, line 193 of page.md): "Ratios in the remaining columns control for education, age,
   gender, and rural/urban residence. ... give predicted average wage for a 35 year-old urban male with 9 years
   of education. ... In column 6 the numerator represents workers born in each country of origin and (likely)
   educated there, having arrived at or after age 20. These ratios, in boldface, are the estimates of Ro—the
   ratio of predicted wages for observably identical workers across the US border."

2. Table 1, Mexico row (line 178): "Mexico | 3.82 | 2.72 | 2.68 | 3.83 | 2.78 | **2.53** | (2.42, 2.65) | 1.31"
   (columns 1-6, the 95% interval of column 6, column 8). Ro = 2.53.

3. Selection for Mexico (line 333): "These nationally-representative data reveal that the average emigrant
   comes from the 56th percentile of residual wages, suggesting that Ro/Re = 1.03 (with a 95% confidence
   interval of (0.96, 1.12)), so that Re ≈ 2.46. (The median emigrant comes from the 50th percentile of
   non-migrants.)" The data (line 331): "Mexico data from 2005 to 2008 thus contain wage information for
   274,955 workers, 569 of which are known to have left Mexico by 12 months later."

4. Table 8, "Implied Re under different assumptions about selection", Mexico row (line 583):
   "Mexico | 2.53 | 3.19 | 0.79 | 2.79 | 0.91 | 2.40 | 1.05 | 2.08 | 1.22 | 72.2" — Ro; Re and Ro/Re with the
   median migrant at the 40th, 50th, 60th and 70th percentiles; the origin percentile at which Re = 2.
   Used: Re 2.79 at the 50th percentile, 2.08 at the 70th.

5. Wages are PPP-adjusted, in 1999 dollars (line 81): "The US census data were collected for the year 1999
   while the surveys were in the 1990s and early 2000s ... We convert each wage estimate in current year local
   currency to current year US dollars at Purchasing Power Parity using factors from the World Bank (2007) and
   then deflate these dollar amounts to 1999 PPP US dollars".

6. Mexico's survey and its income question (appendix table, line 931): "Mexico | 2002 | 2002 | ... | Encuesta
   Nacional de Ingresos y Gastos de los Hogares | ... | Cuánto recibió el mes pasado por sueldos, salarios y
   jornales en el mes pasado? (declare su ingreso bruto)". CMP's Mexican wages are gross; ENIGH 2024 asks for
   the amount received (reads/enigh_2024_questionnaire.md), so this lane grosses it up before comparing.

7. The basis of the ratio (lines 247–249 and footnote 14): "Furthermore, wage data for the United States reflect
   gross earnings before taxes, and we expect that most people responding to a general question about their wages
   or earnings would have provided gross wages on most of the country surveys, but for a handful of countries it
   may be that the responses reflect after-tax wages. If respondents provided net-of-tax instead of gross wages this
   would result in some upward bias to our estimated Ro. This bias will be small, however, if it is present at all.
   Formal-sector income taxes are on the order of 5% in most developing countries (Easterly and Rebelo (1993))."
   With quote 6, CMP's Mexico ratio compares gross with gross. The selection factor Ro/Re is a ratio of two
   gross-basis ratios, so it applies unchanged to this lane's gross premium. For scale, this lane's 2024 gross-up
   of the G1 cells is 8.5% of take-home pay (7.9% withheld tax and contributions, 0.6% retirement deposit).
   [CALCULATION: derived/g2_premium.csv, G1 p56]

## Derived in the lane

- G1 selection δ = Ro/Re − 1: 2.53/2.46 − 1 = +0.028 (56th percentile, central); 2.53/2.79 − 1 = −0.093
  (50th); 2.53/2.08 − 1 = +0.216 (70th). [CALCULATION: g2_premium.py G1_SELECTION]
- The CMP-based G1 premium applies Re 2.46 to the 12.22m first generation; the lane's central G1 row uses the
  direct 2024 cell method instead, with CMP's selection.
