**Verdict:** Newell, Pizer and Prest propose a central shadow price of capital of 1.1, with a reasonable range of 1.1
to 1.2, for each dollar of displaced capital, in place of discounting at an investment rate of return. A 7% investment
return over a 2% or 3% consumption rate implies a 71% or 57% tax on capital, which they reject as implausible.

Used for:
- the upper m in claim 2's productive-use reading (`world_ledger.py` `RETURN_OVER_DISCOUNT`, quote 3): 1/(1 − τ)
  since 2026-10-07, replacing 7% over 2%;
- the crowd-in on the borrowed federal share in arm 4 of `beside_extra.py`: d (SPC − 1) with SPC 1.1.

## Source

Richard G. Newell, William A. Pizer and Brian C. Prest, "The Shadow Price of Capital: Accounting for Capital
Displacement in Cost Benefit Analysis", NBER Working Paper 31526, 2023. URL: https://www.nber.org/papers/w31526.
Local PDF: `_cache/reads/newell_pizer_prest_w31526.pdf`, sha256
`e054f630618ff1e0bb4fa001ea32e2930216640b94efd7cd49edc5ccda7a6dad` (24 pages), text by `pdftotext -layout` beside it.
Fetched by the lead's researcher on 2026-10-07; the quotes were checked against that text on the same day.

## Quotes

1. Abstract: "We derive a formula for the SPC as a function of four key parameters and propose a central SPC value of
   1.1, with a reasonable range of 1.1 to 1.2."
2. Abstract: "Government analysts have long used discount rates based on investment rates of return to approximate the
   effect of capital displacement. However, we show how this approach is not well grounded in economic theory and
   produces highly biased results".
3. Printed p. 11 (PDF p. 14): "However, the implied tax wedges that would rationalize a 7 percent investment rate with
   a 2 percent or 3 percent consumption rate are 71 percent and 57 percent respectively, which is implausibly high
   compared to the average historical capital tax rates of around 35 percent in the Gomme data (i.e., [7 percent – 2
   percent]/7 percent=71 percent and [7 percent – 3 percent]/7 percent=57 percent). ... This suggests an
   inconsistency in the triplet values of r_c = 2 percemt, r_i = 7 percent, and τ ≈ 35 percent." (sic: "percemt")
4. Eq. (4), printed p. 10 (PDF p. 13): SPC = (1 − s)(r_i + μ) / (r_c + μ − s(r_i + μ)), with μ the depreciation
   rate (10%), s the gross saving rate (22%), r_i the investment return net of depreciation and r_c the consumption
   discount rate.
