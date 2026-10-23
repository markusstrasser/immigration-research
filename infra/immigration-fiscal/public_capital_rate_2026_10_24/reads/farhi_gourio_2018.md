# Farhi & Gourio (2018): the share of the return wedge that is risk, rent or unmeasured capital

Farhi, E. and Gourio, F., "Accounting for Macro-Finance Trends: Market Power, Intangibles, and Risk Premia",
Brookings Papers on Economic Activity, Fall 2018, pp. 147–250. Final draft PDF
`https://www.brookings.edu/wp-content/uploads/2018/09/Farhi-Gourio_final-draft.pdf` (cached in
`_cache/farhi_gourio_2018_bpea.pdf`, md5 8b3e9117cc3b69e2bf202aae2454a1b8; journal page = PDF page + 146). Numbers
below were read from the `pdftotext -layout` text of that PDF, not from a search snippet.

**Why this paper anchors θ.** It is the one estimate found that splits the wedge between the measured return on
private capital and the safe rate into rents (markups), risk premia and unmeasured capital. It disciplines the risk
part with asset prices (equity returns, price-dividend ratios) and the rent part with the labour and profit shares.
Equation 27 (p. 169): "MPK − rf = d + gQ + (µ−1)/α (r* + d + gQ) + r* − rf", the three parts being "depreciation
(d + gQ), rents, and risk (r* – rf)" (p. 180). Eq. 29 (p. 202) adds a mismeasurement term, (1−λ)/λ · d/k, for
unmeasured intangible investment.

**2001–16 column, percentage points** (Table 12, pp. 206–207; Table 10, pp. 198–199):

| Version | Rents (market power) | Risk premium | Mismeasurement | θ = (risk + mism.) / (rents + risk + mism.) |
|---|---|---|---|---|
| Baseline (Table 12) | 5.55 | 5.23 | 0.09 | **0.489** |
| AA corporate rate as risk-free (Table 10) | 5.55 | 3.79 | — | 0.406 |
| 10-year Treasury net of term premium (Table 10) | 5.55 | 4.97 | — | 0.472 |
| Leverage (Table 10) | 6.99 | 3.81 | — | 0.353 |
| Constant 10% capital mismeasurement (Table 12) | 4.79 | 5.23 | 0.85 | 0.559 |
| Rising mismeasurement 10–30% (Table 12) | 3.27 | 5.23 | 2.37 | 0.699 |

Depreciation (4.37) is excluded: GRR's return is net of depreciation. Total spread 15.24 in every version.
[SOURCE: Tables 10 and 12; CALCULATION: `theta_item6.cjs` FG block]

**Quotes that bear on the reading.**
- "we show how previous researchers, who have used models without risk, have attributed too big a role to rising
  market power" (p. 149). Footnote 16 (p. 176): Barkai (2016) "simply uses a Treasury rate or corporate bond yield to
  construct the user cost". A bond-rate user cost assigns the whole risk premium to profit, i.e. θ ≈ 0 by
  construction.
- Leverage version: "These results are conservative, because we have assumed that corporate debt pays the same
  return as the risk-free asset" (p. 198). So 0.353 is a lower bound within the paper.
- Mismeasurement scenarios are "largely illustrative"; measured intellectual property is "about 6 percent" of
  capital (p. 203). So 0.56–0.70 are assumption-driven upper readings.
- Baseline equity premium "nearly 5 percent a year in the recent sample" (p. 180); risk-free rate −0.35%
  (Table 4, p. 181).

**Fit to the case.**
- TP-5's 63% supernormal share is measured above a risk-free return (item 6 RESULT §2). The baseline θ, defined on
  the spread above a Treasury rate, is the matching object for the item 6 leg.
- The rate leg starts from the Baa yield, which is a corporate rate. The AA-rate version (0.406) is the closer
  match there. The two differ by 0.08, about $1.5bn on the paired band.
- [GAP] The decomposition is for 2001–16 at a −0.35% safe rate. 2024's safe rate is higher, which shrinks the
  wedge, but the paper gives no shares for a different safe rate.
- [GAP] It covers the whole private economy (NIPA), not C corporations. Power–Frerick Table 1 shows wide industry
  variation in the normal share (item 6 RESULT §2). The group's job-capital industry mix is not mapped to FG's
  aggregate.
- [INFERENCE] "Rents do not scale" holds for the market-power markup on given demand. A removal also shrinks the
  market. If incumbents' rents scale with market size, some of the 5.55 scales too and θ is higher. This is
  unmeasured here.
