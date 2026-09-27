**Verdict:** Confirmed in the July 25, 2025 revision. Saving rates rise steeply with wealth: the top 1% save "well
over 40%" of disposable income (54% over 1983–2019), the next 9% 20%, the 51st–90th percentiles 12% and the bottom
50% "effectively zero". The authors find that the post-1982 rise in the top 1%'s saving "does not boost investment
or capital formation but instead funds dissaving elsewhere, primarily among middle-class households". The rates are
by wealth percentile, not income, and they are averages, not responses to a tax change.

Source: Atif Mian, Ludwig Straub and Amir Sufi, "The Saving Glut of the Rich", revision of July 25, 2025 (earlier
NBER Working Paper 26941, April 2020). URL:
https://atif.scholar.princeton.edu/sites/g/files/toruqf3691/files/documents/MSS_SGR_July242025.pdf. Local PDF:
`_cache/reads/mss_saving_glut_2025.pdf`, sha256 `e054238c7269d7c5e509f8c5ea4ab9aa5b23943561158c9958bc833eccdf91e2`
(66 pages), text by `pdftotext -layout`. Page numbers are PDF pages; the printed page is one lower.

Used for: the payers' saving rate in claim 2's productive-use reading (`world_ledger.py` `MSS_SAVING`,
`saving_leak`).

## Quotes

1. PDF p. 3, introduction: "Our distributional analysis shows that the top 1% save at an exceptionally high rate,
   averaging well over 40% of their disposable income. The saving rate drops to 20% for the next 9%, falls to 12%
   for households in the 51st to 90th percentile, and is effectively zero for the bottom 50%, who live
   hand-to-mouth. While these estimates are derived from repeated cross-sectional tax records, they are similar when
   using a Survey of Consumer Finances (SCF) panel that is nationally representative and follows the same households
   from 1983 to 1989. In fact, the saving rate estimate for the top 1% from tax data is conservative relative to the
   top 1% saving rate estimate in the SCF."

2. PDF p. 3, introduction: "Saving rates at the top have become increasingly skewed, reflecting strong
   non-homothetic preferences. Between 1963-1982 and 1983-2019, the top 1%'s saving rate rose from 43% to 54%, while
   the rest saw theirs fall from 14% to 7%. It is this divergence, combined with the rising income share of the
   wealthy that drives the saving glut of the rich. After 1982, the annual flow of saving from the top 1% increases
   by 2.9pp of national income—over 680 billion in 2024 dollars per year. Crucially, this surge does not boost
   investment or capital formation but instead funds dissaving elsewhere, primarily among middle-class households."

3. PDF p. 24, Figure 6 discussion: "the top 1%'s saving rate rose from 42.9% during 1963-1982 to 53.6% afterwards,
   while average saving rate for the rest of the population declined from 13.8% during 1963-1982 to 7.1%
   afterwards."

4. PDF p. 20, the grouping and the SCF check: "We sort households into percentiles based on their average wealth
   between 1983-1989, and divide them into four groups- top 1%, next 9%, next 40%, and bottom 50%. ... In both data
   sets, the top 1% save at a much higher rate (40% to 50% out of disposable income) than the rest, and the saving
   rate declines across the distribution with the bottom 50% of the population having zero saving rates in both
   data sets." Footnote 16: "The saving rates from the SCF Survey, measured relative to pre-tax income, are
   32.3 %, 26.9 %, 8.5 %, and 0 % for the top 1 %, next 9 %, next 40 %, and bottom 50 %, respectively."

5. PDF p. 1, abstract: "Unveiling the financial sector reveals that this glut financed much of the rise in
   middle-class borrowing before 2008 and the expansion of federal debt thereafter."

## Use and limits

- The lane applies 54% (top 1%, 1983–2019), 20% (next 9%), 12% (51st–90th) and 0 (bottom 50%) to the payers'
  percentiles in the distribution lane, which rank persons by income, not wealth. [INFERENCE: wealth rank stands in
  for income rank] Taking the post-1982 top rate is the choice most favourable to the productive-use reading.
- Average saving rates stand in for the marginal saving out of a permanent tax. With non-homothetic preferences
  (quote 2), the marginal rate at the top may exceed the average.
- Quote 2's finding is an equilibrium association over 1983–2019, not an estimate of how a tax-financed transfer
  changes investment. It bears on the share θ of forgone saving that would have become domestic capital, and it
  points below 1; it does not measure θ.
