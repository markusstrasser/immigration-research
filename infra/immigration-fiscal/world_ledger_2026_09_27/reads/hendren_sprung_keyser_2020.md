**Verdict:** All five category ranges in the brief are confirmed verbatim in the NBER December 2019 revision (0.40–1.63 adult health insurance; 0.65–1.04 in-kind; negative to 1.20 cash welfare and tax credits; 1.16 to infinity top tax rates). One correction: 0.62 for food stamps is not an MVPF. It is the parents' willingness to pay per $1 the government spends on food stamps. The MVPF of the Food Stamp introduction is 1.04 (95% CI [-0.97, ∞]), or 0.39 under the conservative WTP. Table II gives WTP and cost per $1 of programmatic spending for every program. For cash transfers and tax credits WTP is set at $1.00 per $1 of mechanical transfer, and the behavioural response is booked in cost. The QJE 2020 version was not reached.

Source: Nathaniel Hendren and Ben Sprung-Keyser, "A Unified Welfare Analysis of Government Policies", NBER Working Paper 26144, August 2019, revised December 2019. URL: https://www.nber.org/system/files/working_papers/w26144/w26144.pdf. Local PDF: `_cache/reads/hsk_nber_w26144.pdf`, sha256 `e0197418a99913b1e2b20afc9184db60dbd7391d7d109b0e49498364011d59ee` (88 pages). This is **not** the QJE 135(3) 2020 version: `fetch_paper` for doi 10.1093/qje/qjaa006 failed. Published numbers may differ.

Text-extraction caveat: `pdftotext -layout` returns garbage for the body of this PDF, because it uses Type 3 fonts with no Unicode map. All quotes below therefore come from a tesseract OCR of the page images: 200 dpi for the body (`_cache/reads/hsk_ocr.txt`, with page tags in `hsk_ocr_paged.txt`) and 450 dpi for Table II (`_cache/reads/ocr_hsk_hi/t-76.txt`, `t-77.txt`). The quotes reproduce the OCR text, with only line breaks and hyphenation joined. OCR glyph errors are left in place and flagged in brackets. In particular, "oo", "©", "~" or "20" in an interval stand for ∞, and a stray "°", "!" or superscript digit is a footnote marker. Page numbers are given as the PDF page, followed by the printed page number from the page foot.

## 1a. Definition of the MVPF, and how WTP is set for cash transfers and tax credits

1. PDF p. 11 (printed p. 10), Section II, eq. (2): "The Marginal Value of Public Funds (MVPF) of policy 7 is given by the aggregate willingness to pay, WTP? = >> 5 WTP} , for the policy divided by the net cost to the government, Gj:" [OCR garbles the math. The legible part of eq. (2) reads "MV PF; = ... = WTP / Net Cost. (2)", that is, MVPF_j = WTP^j / G^j.]

2. PDF p. 10–11 (printed pp. 9–10): "let G; = ge denote the net impact of the policy on the government budget. This net cost is inclusive both of the initial cost of the program and all other impacts of behavioral responses on the government budget. For example, if spending $1 on preschool increases wages in the future, G; should incorporate the impact of those increases in future tax receipts." [OCR: "G;" = G_j]

3. PDF p. 11 (printed p. 10): "The MVPF is previously defined in Mayshar (1990) where it is referred to as the marginal excess burden (MEB), in Slemrod and Yitzhaki (1996) where it is referred to as both the marginal cost of ..." [the sentence continues past the OCR window and was not read]

4. PDF p. 4 (printed p. 3), benchmark of one: "For point of reference, a simple non-distortionary transfer from the government to an individual would have an MVPF of one. The cost to the government would be exactly equal to the individual beneficiary's willingness to pay. The MVPF can differ from this benchmark value of one if individuals value an expenditure at more or less than its resource cost. For instance, if the government provides insurance, willingness to pay may be greater than the resource costs of provision individuals if the insurance provides consumption smoothing benefits. By contrast, willingness to pay may fall below resource costs if individuals distort their behavior in order to receive higher transfers." It continues: "The MVPF may also deviate from the benchmark value of one if the policy induces fiscal externalities. For example, if spending a dollar on a government policy caused individuals to work less, government tax revenue might fall slightly and then the net cost of the policy would rise above $1. By contrast, if spending that dollar caused them to get more schooling and consequently increased their income, government revenue would rise and the net cost of the policy would fall below $1."

5. PDF p. 4 (printed p. 3), footnote on the envelope theorem: "The intuition here comes from the envelope theorem. Willingness to pay for a government transfer is determined by the "mechanical cost" of that transfer. Additional costs due to behavioral responses are not valued dollar for" [the OCR loses the rest of this footnote line]

6. PDF p. 13 (printed p. 12), decomposition used in the comparison with a benefit-cost ratio: "Let C; denote the initial program outlays of the policy (absent the impact of any behavioral responses on net costs), and let FE; = Gj — Cj denote the impact of the behavioral responses to the policy on the government budget." [So the net cost is G = C + FE, and Table II's "cost per dollar of programmatic spending" is G/C = 1 + FE/C.]

7. PDF p. 25 (printed p. 24), tax cuts: "This literature notes that a tax cut providing $1 in additional after-tax income is valued at $1 by mechanical beneficiaries . In other words, the tax cut is valued at cost by those would receive it in the absence of any behavioral response to the change in the tax code. As a result, measuring WTP is straightforward. The cost to the government of the tax policy is more difficult. The cost of a tax cut that provides $1 of benefits in the absence of a behavioral response is given by 1+ FE, where FE is the impact of the behavioral response to the tax cut on government revenue." And: "The MVPF for each tax reform is the ratio of WTP to cost, 1/(1+ FE):"

8. PDF p. 23 (printed p. 22), EITC-type transfer (Paycheck Plus): "The envelope theorem suggests participants do not value the full $1,399 subsidy dollar for dollar. This is because part of this cost reflects the impact of behavioral responses. To first order, those who entered the labor force in order to obtain the transfer are indifferent between working and not working. [...] Consequently, 98% of the transfer (45/45.9) is valued by the beneficiaries, which implies a WTP of $630 for the transfers in 2014." And: "The estimated WTP of $1,070 combined with the net cost of $1,074 implies an MVPF of 0.996 (which rounds to 1 in Table 2)." And: "Every $1 the government spends in transfers leads to a benefit of roughly $1.48" [OCR: "48" is footnote marker 48; the text reads "roughly $1."]

Answer to 1a: yes. WTP is $1 per $1 of *mechanical* transfer, meaning the transfer that would be paid absent behavioural response. It is not $1 per $1 of total spending. Behavioural costs go into the net cost, which is why Table II shows WTP = 1.00 and cost ≠ 1 for the EITC, AFDC term limits, the Alaska UBI and the top-tax rows (see 1c).

## 1b. Category ranges (brief's figures checked)

9. PDF p. 6 (printed p. 5), introduction: "Our results show lower MVPFs for policies targeted to adults. Most of these MVPFs lie between 0.5 and 2. For example, we find MVPFs ranging from 0.40-1.63 for health insurance expansions to adults, 0.65-1.04 for in-kind transfers such as housing vouchers and food stamps, and from negative values to 1.20 for tax credits and cash welfare programs to low-income households. These lower MVPFs reflect the fact that spending on many of these policies reduced labor earnings."

10. PDF p. 6 (printed p. 5): "Amongst expenditures on adults, we find relatively large MVPFs for reductions in top marginal tax rates, with estimates from 1.16 to infinity. There is, however, substantial sampling uncertainty in these estimates." Footnote: "For example, we estimate an infinite MVPF for the 1981 reduction in the top marginal income tax rate from 70% to 50%. Our confidence interval, however, includes both 1 and infinity."

11. PDF p. 30 (printed p. 29), Section IV.B Adults: "we find MVPFs ranging from 0.40 to 1.63 for the six health insurance policies in our baseline sample targeted to adults. Along the same lines, we find MVPFs ranging from 0.43 to 1.03 for unemployment insurance policies, 0.74-0.96 for disability insurance expansions, and 1.12-1.20 for earned income tax credits. We find MVPFs of housing vouchers ranging from 0.65 using assignment of vouchers in Chicago via lottery (Jacob and Ludwig, 2012) to 0.91 using an RCT of the provision of housing vouchers to families on cash welfare (Mills et al., 2006)." It continues: "As depicted in Figure V, the average cost per $1 of government spending on these adult policies is generally slightly above $1."

12. PDF p. 31 (printed p. 30), footnote 65: "It is also worth noting that more recent reforms have substantially lower MVPFs. The MVPF of the 2013 top tax rate changes is 1.16." [This is the lowest top-rate MVPF, and it is the source of lambda = 1.16.]

13. PDF p. 31 (printed p. 30): "In the case of the 1981 reform, the tax bill reduced the top federal marginal tax rate on income from 70% to 50%. Using estimates of the elasticity of taxable income from Saez 2003, we calculate that the MVPF is co (95% CI of [0.94, 00])." And: "we analyzed the 1986 reform and found an MVPF of 44.27, with a confidence interval ranging from 2.37 to oo." [OCR: co, 00, oo = ∞]

14. PDF p. 2, abstract: "We find smaller MVPFs for policies targeting adults, generally between 0.5 and 2. Expenditures on adults have exceeded this MVPF range in particular if they induced large spillovers on children."

## 1c. WTP per $1 and net cost per $1 of programmatic spending (Table II)

15. PDF p. 77, Table II notes: "This table presents our baseline estimates for each program in our extended sample, along the category averages reported in the bold header rows in each category. We exclude the welfare to work policies discussed in Section VI.C. For each policy, we report its MVPF, cost per dollar of programmatic spending, and willingness to pay per dollar of programmatic spending. We also report bootstrapped 95% confidence with adjustments discussed in Appendix H. The final column indicates whether the program is included in the baseline estimates (and thus included in the category averages)."

16. PDF pp. 76–77, "Table II: MVPF, WTP and Cost Estimates with Confidence Intervals, All Programs". Column order as OCR'd: Program | MVPF | MVPF CI | WTP | WTP CI | Cost | Cost CI | Baseline. Rows are from the 450 dpi OCR; a trailing "x" marks inclusion in the baseline.

| Row (verbatim label) | MVPF [CI] | WTP per $1 [CI] | Cost per $1 [CI] |
|---|---|---|---|
| Health Adult (category) | 0.89 [0.56, 1.57] | 1.49 [1.00, 1.99] | 1.67 [1.01, 2.39] |
| Mass HI (150%FPL) | 0.80 | 1.00 | 1.25 |
| Mass HI (200%FPL) | 0.85 | 1.00 | 1.18 |
| Mass HI (250%FPL) | 1.09 | 1.00 | 0.92 |
| Medicare Intro | 1.63 [0.52, 3.83] | 2.00 [0.58, 3.44] | 1.23 [0.48, 1.78] |
| Oregon Health | 1.16 [1.08, 1.25] | 1.46 [1.19, 1.83] | 1.26 [1.04, 1.57] |
| Medigap Tax | 0.40 [0.22, 1.54] | 1.00 | 2.53 [0.64, 4.44] |
| Housing Vouchers (category) | 0.77 [0.74, 0.81] | 0.91 [0.91, 0.91] | 1.19 [1.13, 1.24] |
| HCV RCT to Welfare | 0.91 [0.86, 0.96] | 1.00 | 1.10 [1.04, 1.17] |
| HCV Chicago Lottery | 0.65 [0.61, 0.70] | 0.83 | 1.27 [1.18, 1.37] |
| WIC (no baseline mark) | 1.38 [1.10, 1.66] | 1.28 [1.08, 1.47] | 0.93 [0.88, 0.98] |
| SNAP Assist | 0.92 [0.91, 0.96]* | 0.92 [0.91, 0.96]* | 1.00 |
| SNAP Info | 0.89 [0.89, 0.89]* | 0.89 [0.89, 0.89]* | 1.00 |
| SNAP Intro | 1.04 [-0.97, ∞] | 1.09 [-2.45, 4.55] | 1.05 [-0.38, 2.51] |
| Cash Transfers (category) | 0.74 [0.36, 1.47] | 0.86 [0.50, 1.37] | 1.16 [0.89, 1.34] |
| EITC 1986 | 1.20 [1.05, 1.38] | 1.00 | 0.84 [0.73, 0.95] |
| EITC 1993 | 1.12 [0.82, 1.21] | 1.00 | 0.89 [0.67, 1.06] |
| AFDC Generosity | 0.91 [0.83, 1.00] | 1.04 [0.96, 1.11] | 1.14 [1.10, 1.18] |
| AFDC Term Limits | 0.81 [0.73, 0.90] | 1.00 | 1.23 [1.11, 1.38] |
| Alaska UBI | 0.92 [0.89, 0.96] | 1.00 | 1.09 [1.05, 1.12] |
| Paycheck+ | 1.00 [0.87, 1.19] | 1.00 | 1.00 [0.85, 1.15] |
| Neg Inc Tax | -0.01 [-0.82, 9.83] | -0.02 [-2.50, 3.53] | 1.96 [0.18, 3.20] |
| Top Taxes (category) | 3.03 [1.35, ∞] | 1.00 [1.00, 1.00] | 0.33 [-0.09, 0.74] |
| Top Tax 2013 | 1.16 [0.87, 1.92] | 1.00 | 0.86 [0.54, 1.16] |
| Top Tax 1993 | 1.85 [1.19, 4.07] | 1.00 | 0.54 [0.25, 0.84] |
| Top Tax 1986 | 44.27 [2.37, ∞] | 1.00 | 0.02 [-0.37, 0.42] |
| Top Tax 2001 | 1.37 [0.92, 2.86] | 1.00 | 0.73 [0.36, 1.09] |
| Top Tax 1981 | ∞ [0.94, ∞] | 1.00 | -0.51 [-2.13, 1.06] |
| K12 Spend (Jackson et al.) | ∞ | 8.78 [4.58, 13.03] | -1.03 [-2.02, -0.06] |
| K12 Spend Mich. | 0.65 [0.05, 2.19] | 0.62 [-0.01, 1.58] | 0.95 [0.79, 1.08] |

OCR check: every row satisfies MVPF ≈ WTP/Cost; for example, EITC 1986 gives 1.00/0.84 = 1.19, Oregon 1.46/1.26 = 1.16 and HCV Chicago 0.83/1.27 = 0.65. The 200 dpi pass misread "1.16" as "4.46" and "1.12" as "1.42", and dropped the minus signs on Neg Inc Tax and Top Tax 1981. The 450 dpi pass above fixes those errors. A "*" means the CI was inferred from reported p-values (per the notes).

17. Food stamps, PDF p. 20 (printed p. 19), costs: "Costs The first component of our total costs is the average yearly benefit from food stamp enrollment, equal to $2,904. To this, we add the fiscal externality resulting from the impacts on both adults and children. For adults, Hoynes and Schanzenbach (2012) document large yet imprecise reductions in earnings of $3650 that imply a fiscal externality of $471 from reductions in tax revenue — roughly $0.16 per $1 of food stamps provided." The passage continues onto PDF p. 21 (printed p. 20): "This suggests that for each $1 in food stamp spending the resulting impacts on children increase government revenue by $0.11. Taken together these estimates imply that every $1 of spending on food stamps costs $1.05."

18. Food stamps WTP, PDF p. 21 (printed p. 20): "WTP We provide a willingness to pay from three components. First, the envelope theorem suggests that individuals are willing to pay for the mechanical cost of SNAP benefits, which we estimate to be $1,809. We arrive at this number by taking the $3,650 increase in earnings and noting that SNAP benefits decline with earnings at a 30% phase out rate. This means that $1,095 of the food stamp cost is the result of a cost increase from behavioral responses. Consequently, our point estimate suggests individuals value $0.62 for each $1 spent by the government on food stamps." It continues: "Second, we incorporate the WTP for reductions in infant mortality and increases in longevity amongst their children. [...] This leads to an additional WTP of $0.02. Lastly, we incorporate an additional willingness to pay due to increases in after tax income amongst those who received food stamps as children. [...] Combining costs with willingness to pay creates an MVPF of 1.04 (95% CI of |-0.97, oo])." [The OCR reads "$3,650 increase in earnings" here, but quote 17 calls the same $3,650 a reduction in earnings. I did not check the page image, so it is unclear whether the PDF itself says "increase".]

19. Food stamps, footnote 38, PDF p. 21 (printed p. 20): "It is also worth noting that this willingness to pay is nearly identical to the value we would receive if we did not apply the envelope theorem in this context, but rather used estimates from Whitmore (2002) suggesting food stamps have a trade value of at least 65%. For our "conservative" willingness to pay specification, we make both the envelope theorem and trade value modifications and find that the MVPF falls to 0.39."

20. Medicaid for adults: the NBER main text reports only the Table II row "Oregon Health": WTP 1.46 and cost 1.26 per $1 of programmatic spending, and MVPF 1.16. **[NOT FOUND in NBER w26144 main text]** is the explanation of how this WTP is built: whether it counts the transfer to uncompensated-care providers, and what "programmatic spending" means for Medicaid. That explanation sits in the online appendix, which I did not reach. This WTP of 1.46 per $1 cannot be read as recipients' valuation: FHL (2019) put recipients' WTP at $0.2–0.4 per $1 of government spending, plus about $0.6 transferred to external parties (see `finkelstein_hendren_luttmer_2019.md`). Footnote 61 on PDF p. 30 (printed p. 29) covers the Massachusetts subsidies only: "Translating these estimates into an MVPF suggests values ranging from 0.800 to 1.09 for different subsidy eligibility levels."

## 1d. K–12 schooling and child spending

21. PDF p. 17 (printed p. 16), the general rule (FIU example): "Throughout, our approaches to estimating WTP rely heavily on the logic of the envelope theorem and revealed preference. For the baseline estimate, we assume that increases in income amongst the college educated stem from returns to human capital, not from higher levels of effort. In this case, the envelope theorem implies that we can form an estimate of WTP using the policy's impact on net income after taxes and other expenses." [Earnings gains therefore enter WTP net of tax. The tax on those gains enters the net cost, as fiscal externality (quote 2: "G; should incorporate the impact of those increases in future tax receipts").]

22. PDF p. 10 (printed p. 9), footnote 16: "For the purposes of our analysis, we assume that changes in individual willingness to pay do not incorporate altruism. For example, we assume that parents do not place independent value on changes in willingness to pay amongst their children. Similarly, we do not incorporate individual willingness to pay for redistribution to others."

23. PDF p. 27 (printed p. 26): "We find an infinite MVPF for increased K-12 spending due to school finance equalization as studied in Jackson et al. (2016)." Footnote 50: "In cases where both parents and children are beneficiaries of the policy, we assign the age of the "economic" beneficiary based on who has the highest WTP."

24. PDF p. 6 (printed p. 5): "we find large MVPFs for policies targeting older children, such as historical equalizations in K-12 school financing (studied in Jackson et al. (2016)) and policies increasing college attainment." The Table II rows are in quote 16: K12 Spend, with WTP 8.78 and cost -1.03 per $1; and K12 Spend Mich., with MVPF 0.65, WTP 0.62 and cost 0.95.

## Relevant to `mcpf_sources.md`

25. PDF p. 13 (printed p. 12): "The initial program outlays in the denominator are often multiplied by 1+ ¢, where ¢ is the marginal deadweight loss of raising government revenue. This is thought to translate the upfront costs into social costs by accounting for the welfare impact of an implicit tax policy that raises the needed funds. Often, ¢ is taken to be 0.3 or 0.5 (Heckman et al., 2010)." [OCR: "¢" = φ]

## Corrections to the brief's figures

- In-kind transfers to adults, 0.65–1.04: **confirmed** (quote 9). The ends are HCV Chicago Lottery (0.65) and SNAP Intro (1.04).
- Food stamps / SNAP "0.62": **corrected**. 0.62 is the parents' WTP per $1 of government food-stamp spending (quote 18). The MVPF is 1.04 (95% CI [-0.97, ∞]), with a net cost of $1.05 per $1. The conservative-WTP MVPF is 0.39 (quote 19). In Table II, WTP for SNAP Intro is 1.09 per $1 of programmatic spending, because it includes children's after-tax earnings gains.
- Cash welfare and tax credits, below zero to 1.20: **confirmed** (quote 9). The low end is the Negative Income Tax (-0.01); the high end is EITC 1986 (1.20). The EITC range alone is 1.12–1.20 (quote 11).
- Adult health insurance, 0.40–1.63: **confirmed** (quotes 9 and 11). The ends are the Medigap Tax (0.40) and the Medicare introduction (1.63). Oregon Medicaid is 1.16.
- Top tax rates, 1.16 to ∞: **confirmed** (quotes 10 and 12). 1.16 is the 2013 top-rate change.
- WTP per $1 of mechanical transfer is 1.00 for the EITC, AFDC term limits, the Alaska UBI, Paycheck+ and all top-tax rows. The behavioural response shows up in cost per $1: 0.84–0.89 for the EITC and 1.09–1.23 for cash welfare and the UBI. None of this is verified against the QJE 2020 version.
