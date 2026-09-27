**Verdict:** Both values are anchored in primary text. λ = 1.16 is the MVPF of the 2013 top-rate change in Hendren & Sprung-Keyser (NBER w26144): WTP of 1.00 per $1 of mechanical cost against a net cost of 0.86. λ = 1.5 appears in Heckman & Smith (1998, NBER w6542), who apply a "welfare cost of taxation" of $0.50 per dollar of revenue. They call it "in the range suggested by Browning (1987)" and give a "consensus value" of $0.30–0.50. HSK also say φ "is taken to be 0.3 or 0.5 (Heckman et al., 2010)". OMB Circular A-94 (1992) sets a default excess burden of 25%, a factor of 1.25. I did not reach Browning (1987), Heckman–LaLonde–Smith (1999) or Ballard–Shoven–Whalley (1985).

## Sources reached

A. Hendren & Sprung-Keyser, "A Unified Welfare Analysis of Government Policies", NBER WP 26144, revised December 2019. Local file `_cache/reads/hsk_nber_w26144.pdf`, sha256 `e0197418a99913b1e2b20afc9184db60dbd7391d7d109b0e49498364011d59ee`. The text is OCR, as described in `hendren_sprung_keyser_2020.md`.

B. James J. Heckman and Jeffrey A. Smith, "Evaluating the Welfare State", NBER Working Paper 6542. URL: https://www.nber.org/system/files/working_papers/w6542/w6542.pdf. Local file `_cache/reads/heckman_smith_nber_w6542.pdf`, sha256 `6b640e215bb1899a5f0d9f117c5b42f925a49d26057cadbfdb48588aaf82140c` (98 pages). The PDF is a scan with no text layer, so the text is a tesseract OCR at 200 dpi (`_cache/reads/hs98_ocr.txt`, with page tags in `hs98_paged.txt`). The issue date was not read from the scan; NBER numbering puts it in 1998. Page numbers are PDF pages.

C. OMB Circular No. A-94 (Transmittal Memo No. 64), "Guidelines and Discount Rates for Benefit-Cost Analysis of Federal Programs". This is the 1992 version, hosted as a legacy file at https://www.whitehouse.gov/wp-content/uploads/legacy_drupal_files/omb/circulars/A94/a094.pdf. Local file `_cache/reads/omb_a94_1992.pdf`, sha256 `82c5f7377dd0198168420094e80fb732bbcfd05f1a013664133ec7f2156ed297` (22 pages), extracted with `pdftotext -layout`, which gives a clean text layer. I did not check whether the 2023 revision of A-94 keeps the 25% default.

## Quotes

### λ = 1.16 (source A)

1. HSK, PDF p. 31 (printed p. 30), footnote 65: "It is also worth noting that more recent reforms have substantially lower MVPFs. The MVPF of the 2013 top tax rate changes is 1.16."

2. HSK, PDF p. 77, Table II, row "Top Tax 2013": MVPF 1.16 [0.87, 1.92]; WTP 1.00; cost 0.86 [0.54, 1.16] per $1 of programmatic spending. The other top-tax rows are 1993: 1.85; 2001: 1.37; 1986: 44.27; 1981: ∞. The category average is 3.03 (450 dpi OCR).

3. HSK, PDF p. 25 (printed p. 24): "The cost of a tax cut that provides $1 of benefits in the absence of a behavioral response is given by 1+ FE, where FE is the impact of the behavioral response to the tax cut on government revenue. [...] The MVPF for each tax reform is the ratio of WTP to cost, 1/(1+ FE):"

4. HSK, PDF p. 11 (printed p. 10): "The MVPF is previously defined in Mayshar (1990) where it is referred to as the marginal excess burden (MEB), in Slemrod and Yitzhaki (1996) where it is referred to as both the marginal cost of ..." [the rest of the sentence was not captured]

### λ = 1.5 (sources A and B)

5. HSK, PDF p. 13 (printed p. 12): "The initial program outlays in the denominator are often multiplied by 1+ ¢, where ¢ is the marginal deadweight loss of raising government revenue. This is thought to translate the upfront costs into social costs by accounting for the welfare impact of an implicit tax policy that raises the needed funds. Often, ¢ is taken to be 0.3 or 0.5 (Heckman et al., 2010)." [OCR: "¢" = φ. Heckman et al. (2010) is cited, not reached.]

6. Heckman & Smith (1998), PDF p. 46, on the JTPA cost-benefit table: "Each of the remaining rows of Table 6 presents estimates that net out the direct costs of training based on the assumptions stated in those rows about the duration of program benefits (30 months or 7 years), the interest rate used to discount the benefits (0.00 or 0.25 over six months), and the welfare cost of taxation ($0.0 or $0.50 per dollar of revenue)."

7. Heckman & Smith (1998), PDF p. 46: "Second, accounting for the welfare costs of taxation has a substantial effect on the cost-benefit calculation. For adult females with benefits assumed to last. 30 months, and assuming no discounting, netting out welfare costs of taxation equal to $0.50 per dollar changes the difference between costs and benefits from $532 to $-54, The estimates of the welfare cost of public funds presented in the literature vary over the range from $0.00 to $3.00 per dollar of taxes. See Browning (1987). However, the "consensus value" is less than $1.00 and typically in the range of $0.30-0.50." It continues: "In this paper we use the marginal cost of funds given the current scale of government, which is appropriate because the scale the JT'PA program is relatively" [the sentence runs on; OCR punctuation kept as read]

8. Heckman & Smith (1998), PDF p. 76, table note 2: "Welfare cost of taxes indicates the additional cost in terms of lost output due to each additional dollar of taxes raised. The value of 0.50 lies in the range suggested by Browning (1987)."

### λ = 1.25, official default (source C)

9. OMB A-94 (1992), PDF p. 13, §11: "Special Guidance for Public Investment. This guidance applies only to public investments with social benefits apart from decreased Federal costs. It is not required for cost-effectiveness or lease-purchase analyses. Because taxes generally distort relative prices, they impose a burden in excess of the revenues they raise. Recent studies of the U.S. tax system suggest a range of values for the marginal excess burden, of which a reasonable estimate is 25 cents per dollar of revenue."

10. OMB A-94 (1992), PDF p. 13, §11.a–b: "a. Analysis of Excess Burdens. The presentation of results for public investments that are not justified on cost-saving grounds should include a supplementary analysis with a 25 percent excess burden. Thus, in such analyses, costs in the form of public expenditures should be multiplied by a factor of 1.25 and net present value recomputed. b. Exceptions. Where specific information clearly suggests that the excess burden is lower (or higher) than 25 percent, analyses may use a different figure. When a different figure is used, an explanation should be provided for it."

11. OMB A-94 (1992), glossary: "Excess Burden -- Unless a tax is imposed in the form of a lump sum unrelated to economic activity, such as a head tax, it will affect economic decisions on the margin. Departures from economic efficiency resulting from the distorting effect of taxes are called excess burdens because they disadvantage society without adding to Treasury receipts. This concept is also sometimes referred to as deadweight loss."

## Not reached

- Browning (1987), AER 77(1), "On the Marginal Welfare Cost of Taxation": JSTOR only, not attempted. Its range is known here only through Heckman & Smith's citation ("$0.00 to $3.00").
- Heckman, LaLonde & Smith (1999), Handbook of Labor Economics 3A: `fetch_paper` for doi 10.1016/S1573-4463(99)03012-6 failed. The brief's claim that they "assume a 50% deadweight cost" is therefore **[NOT FOUND in primary text]**. The same authors' 1998 NBER paper does use $0.50 (quotes 6–8).
- Ballard, Shoven & Whalley (1985): NBER w1352, which I tried, is a different paper (Hendershott & Ling); I downloaded and deleted it. BSW was not reached.

## Corrections to the brief's figures

- λ = 1.16 is **confirmed** as the lowest top-rate MVPF (2013 reform). Note what it measures: WTP 1.00 over a net cost of 0.86 per $1 of mechanical tax cut, in the NBER December 2019 revision.
- λ = 1.5 is **confirmed as a convention**, not as an estimate. Heckman & Smith (1998) use $0.50 per dollar of revenue, "in the range suggested by Browning (1987)". They also call $0.30–0.50 the "consensus value". The claim that Heckman–LaLonde–Smith (1999) assume 50% was not checked in primary text.
- A third anchor the brief did not list is OMB A-94 (1992), with a default excess burden of 25% (factor 1.25) and a band that is "lower (or higher)" by exception.
