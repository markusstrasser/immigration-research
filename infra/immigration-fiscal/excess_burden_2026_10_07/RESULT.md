claude-opus-5-5
Stopped by the lead 2026-10-07: covered by ladder 250 / world_ledger_2026_09_27.

**Verdict:** The best-supported marginal excess burden (MEB) for the US tax mix is **0.25 per dollar (MCPF 1.25), range 0.10–0.50**. For broad federal income-tax rises it is 0.20, from Saez–Slemrod–Giertz 2012 (p. 42, ETI 0.25; 0.09–0.35 across ETI 0.12–0.40). Top-rate rises run 0.16–0.85 (Hendren & Sprung-Keyser 2020, Table II: 2013 1.16, 1993 1.85). The state-local sales and property mix is ≈0.13–0.19 before labor-supply effects (Muthitacharoen & Zodrow 2008). OMB A-94 uses 0.25 in both 1992 and 2023.

Applied correctly, the MEB goes only on what other residents finance through distortionary taxes. That is everything except the $82.9 / 77.8bn pension-accrual increment, which current law pays by cutting others' benefits pro rata, so its MEB ≈ 0. The beside reading is **0.25 × $307.4–383.4bn = $76.8–95.9bn a year (range $30.7–191.7bn)**, or $97.6–115.3bn if the accrual is included. Most public-finance economists would accept this as a sensitivity (it is OMB's supplementary analysis). None would headline it: the account's estimand is budgetary, and HSK argue against assuming a financing margin. [FRAMING-SENSITIVE: Jacobs 2018 shows MCF = 1 at an optimal schedule once distributional gains count]

Scope: best-supported MCPF / marginal excess burden for US federal income+payroll and state-local taxes; correct application to the main-case account; beside reading (MCPF−1) × $390.3–461.2bn; objections. Bounded ≤25 searches. Analysis only; no commits.

## Findings

### F0. Already in the repo (reused, not re-fetched)
`infra/immigration-fiscal/world_ledger_2026_09_27/reads/mcpf_sources.md` and `reads/hendren_2020_inverse_optimum.md` hold verbatim primary quotes:
- HSK (NBER w26144, Dec 2019) Table II: MVPF of the 2013 top-rate rise 1.16 [0.87, 1.92]; 1993 1.85; 2001 1.37; 1986 44.27; 1981 ∞ (PDF p. 77). For a tax change MVPF = 1/(1+FE), so it reads as the cost to payers per $1 of net revenue.
- Hendren, "Measuring Economic Efficiency Using Inverse-Optimum Weights" (NBER w20351, Apr 2020, p. 6, p. 21): cost to the government of a $1 tax cut is ~$1.15 at the bottom (EITC) and ~$0.65 at the top. The world-ledger lane already turned that schedule into λ_h = 1.286 by weighting 1/g(y) with payers' tax shares (`world_ledger_2026_09_27/RESULT.md:295`).
- Heckman & Smith 1998 (NBER w6542, p. 46): "consensus value ... typically in the range of $0.30-0.50"; they use $0.50.
- OMB A-94 (1992) §11: "a reasonable estimate is 25 cents per dollar of revenue", applied only as a supplementary analysis.

### F1. Saez, Slemrod & Giertz (2012), "The Elasticity of Taxable Income with Respect to Marginal Tax Rates", JEL 50(1): 3–50 [SOURCE: https://eml.berkeley.edu/~saez/saez-slemrod-giertzJEL12.pdf, read in full text]
- p. 8, eq. (6): marginal excess burden per $ of extra revenue = e·a·τ / (1 − τ − e·a·τ).
- p. 9: top bracket, e = 0.25, a = 1.5, τ = 0.425 (federal 35% + state 5.9% + Medicare 2.9% + sales 2.3%): revenue lost to behaviour 27.7%; "a utility loss (equal to the MECF) of 1/(1 − 0.277) = $1.38 ... a marginal excess burden of −dB/dR = $0.38".
- p. 10: if half the vanished income turns up in another base taxed at 0.3, the MEB "decreases from 38 percent to 22 percent".
- p. 42 (conclusion): "the best available estimates range from 0.12 to 0.40 ... at the approximate midpoint of this rate—an ETI of 0.25—the marginal excess burden per dollar of federal income tax revenue raised is $0.195 for an across-the-board proportional tax increase, and $0.339 for a tax increase focused on the top 1 percent"; fn 72: at e = 0.5 for the top 1%, $0.678.
- **This is the best single anchor for a broad federal income-tax increase: MEB ≈ 0.20 (MCPF ≈ 1.20) at ETI 0.25.** It counts no payroll-tax or state fiscal externality beyond what the formula carries; it is for 2005 returns.

### F2. Feldstein (1995/1999), "Tax Avoidance and the Deadweight Loss of the Income Tax", NBER w5055 (Mar 1995; REStat 81(4), 1999) [SOURCE: https://www.nber.org/system/files/working_papers/w5055/w5055.pdf; scan, tesseract OCR at 200 dpi]
- Uses compensated ETI ε = 1.04, "the lowest of the elasticity" estimates from his 1986-reform study (OCR p. 15, line "I use ε = 1.04").
- Aggregate calculation: "a tax inefficiency ratio of 72 percent, i.e., there is 72 cents of incremental deadweight loss for every incremental dollar of revenue" (PDF p. 26).
- TAXSIM: "the incremental deadweight loss per dollar of additional revenue is $2.06" (≈PDF p. 30); abstract: "nearly two dollars per incremental dollar of revenue".
- Critics: the ETI literature after 1986 found much lower elasticities (SSG p. 42: "Subsequent research generated considerably lower estimates, in part because of better data and improved methodology"); Feldstein's ε ≈ 1 sits far above SSG's 0.12–0.40 band. Treat MCPF ≈ 3 as an outlier upper bound, not a range end.

[GAP] Still to reach: HSK QJE 2020 / Policy Impacts tax MVPFs; Kleven & Kreiner 2006; Ballard–Shoven–Whalley 1985; Dahlby 2008; state-local (sales, property) MCPF; payroll tax; OMB A-94 2023 revision; CBO.

### F3. Kleven & Kreiner (2006), "The Marginal Cost of Public Funds: Hours of Work Versus Labor Force Participation", JPubE 90(10–11): 1955–1973 [SOURCE: author copy https://web.econ.ku.dk/ctk/Papers/MCF-RRR5.pdf, text layer]
- Covers Denmark, France, Germany, Italy, UK only — **no US estimate**. The UK, with low participation tax rates at the bottom, is the closest US analogue.
- Table III (proportional tax changes): UK S1–S9 = 1.00, 0.93, 1.10, 1.02, 1.13, **1.26**, 1.18, 1.14, 1.36; Denmark 1.00–3.51.
- Text: S6 (intensive 0.1, extensive 0.2 declining) "perhaps a natural baseline scenario — the size of MCF varies from 1.26 for the UK to 2.20 for Denmark". Pure intensive-margin models "generate quite low costs", 1.10 (UK) – 1.29 (Denmark).
- Lesson for the US: counting participation responses adds ~0.1–0.15 to a UK-type MCPF. The ETI route (SSG) captures participation only in part, because ETI samples are mostly filers who already work.

### F4. Muthitacharoen (CBO) & Zodrow (Rice), "Efficiency and State and Local Taxation", NTA Proceedings 2008 [SOURCE: https://ntanet.org/wp-content/uploads/proceedings/2008/006-muthitacharoen-efficiency-state-local-2008-nta-proceedings.pdf, full text via Exa]
- Small-open-economy CGE for a jurisdiction that raises 1% more revenue. Table 1: efficiency cost **14.40%** of the added revenue for the property tax and **12.93%** for the sales tax. Table 2 sensitivity: property 12.15–19.07%, sales 12.69–15.07%.
- The authors call these understated: the model "ignores labor supply and saving effects". Two things pull the other way. They ignore deductibility, which "would temper efficiency costs". And the property-tax cost here is mostly capital driven out of the jurisdiction (ΔK −0.173%). Seen from the nation, part of that is a move between jurisdictions, not a loss.
- They assume the capital-tax view; under the benefit view (Fischel) the property tax is a near-user charge with ~0 excess burden.
- Hawkins (2002, NTJ 55), as cited there: sales-tax excess burden from base narrowness alone is 17.9–26.7% of revenue with pyramiding, "closer to average" than marginal costs.
- Reading: the excess burden of the state-local *mix* from its own distortions alone is ≈ 0.13–0.15. Add the labor wedge, which a sales tax shares with income taxes, and a state-local MEB ≈ 0.2–0.3 is plausible. [INFERENCE]

### F5. What finances the $390.3–461.2bn [DATA: `infra/immigration-fiscal/debt_legacy_2026_09_23/derived/oct05/federal_split_2024.csv`, rows long_run_non_school_full / central]
| part | low end $bn | high end $bn | who finances it, and when |
|---|---|---|---|
| state-local cash gap | 228.3 | 251.1 | other residents' state-local taxes **now** (balanced budgets), or service cuts |
| federal cash gap | 32.4 | 61.2 | borrowing now; future federal taxes (or cuts) |
| pension accrual increment (SS + Part A promises at payable benefits, over current cash flows) | 82.9 | 77.8 | future benefits within payable levels: under current law others' benefits are cut pro rata, so the cost is not paid by a tax rise |
| capital return (imputed resource cost) | 37.1 | 61.9 | public capital is bought with taxes or debt; imputed, never a cash flow |
| displaced | 8.8 | 8.8 | tax-financed transfers |
| production term and rounding | 0.7 | 0.5 | — |
| **total** | **390.3** | **461.2** | |
Check: 228.3+32.4+82.9+37.1+8.8+0.7 = 390.2 (390.29 unrounded); 251.1+61.2+77.8+61.9+8.8+0.5 = 461.3 (461.24 unrounded).
- Federal share of the cash gap 12.4% (low) / 19.6% (high), with convention bounds 1.2–27.7%. About 2/3 of the total is a state-local cash flow paid by other residents now. [CALCULATION: 228.3/390.3 = 58.5%; 251.1/461.2 = 54.4% state-local cash; plus displaced]

### F6. Hendren & Sprung-Keyser (2020), QJE 135(3): 1209–1318, published version [SOURCE: https://bsprungkeyser.com/assets/MVPF_Mar_2020_QJE.pdf, text layer]
- Table II (QJE p. ~1236–1240): Top tax 2013 **1.16** [0.87, 1.92], cost 0.86; Top tax 1993 **1.85** [1.19, 4.07]; 2001 **1.37** [0.92, 2.86]; 1986 44.27; 1981 ∞; category mean 3.03 [1.35, ∞]. EITC 1986 1.20, EITC 1993 1.12 (cost 0.84–0.89: those expansions partly pay for themselves). These are identical to the NBER Dec 2019 numbers in F0, so the published version is confirmed.
- p. 1256: "estimates of the impacts of recent reforms have produced substantially smaller MVPFs (e.g., 1.16 for the 2013 top tax rate increase)".
- p. 1222–1224, the methodological objection to a single MCPF: "the MVPF approach does not require the government to close the budget constraint through an increase in taxation. Therefore, one does not adjust for the 'deadweight cost of taxation' based on this particular assumed method of government finance ... a policy that provides benefits to the poor cannot be readily compared to the raising of revenue on the rich without thinking about Okun's bucket and the social welfare weights". They also note φ "is taken to be 0.3 or 0.5 (Heckman et al. 2010)" in the BCR literature.
- What HSK give for *top* rates is 1.16–1.85. No HSK row prices a broad middle-class rate rise. Hendren (2020, F0) supplies that through g(y): a cut costs ≈1.0 near the 60th percentile, so the MCPF there is ≈1.0–1.1, while the top costs 1/0.65 ≈ 1.54.

### F7. OMB Circular A-94, revised November 2023 [SOURCE: https://www.whitehouse.gov/wp-content/uploads/2023/11/CircularA-94.pdf, §11, p. 17, via Exa highlight]
- "Studies of the U.S. tax system suggest a range of values for the marginal cost of public funds, of which a reasonable estimate is 25 cents per dollar of revenue. Such studies typically reflect assumptions that may not apply in many cases". The analysis "**may** include a supplementary analysis with a 25 percent marginal cost of public funds" (1992: "should"). It cites HSK 2020, and it sets an MCPF of zero for "an investment funded by user charges that function like market prices".
- So the official US default is unchanged at 1.25 from 1992 to 2023, and it is used **only as a supplementary analysis, never in the main BCA**. [UNVERIFIED: whether the 2025 administration rescinded the 2023 A-94 along with the 2023 A-4; either version gives 25%.]

### F8. Ballard, Shoven & Whalley: the CGE canon [SOURCE: NBER w1043 (1982), https://www.nber.org/system/files/working_papers/w1043/w1043.pdf, text layer; Fullerton & Henderson, NBER w2353 (1987), p. 2 review, https://www.nber.org/system/files/working_papers/w2353/w2353.pdf]
- w1043 abstract and Table 4: "The marginal welfare loss to consumers from raising an additional dollar of revenue is in the range of 34 cents to 48 cents". Table 5, at saving elasticity 0.4 and labor 0.15: capital taxes 0.49, labor taxes 0.19, income taxes 0.55, consumer sales on goods other than alcohol, tobacco and gasoline 0.35 (1973 data; the sales-total cell OCRs as "63").
- Fullerton–Henderson (1987), on the published AER 1985 version: "Overall marginal excess burden centers around 33 cents per dollar of revenue but varies between 17 and 56 cents"; Browning (1976) 9–16¢ on labor; Stuart (1984) ~21¢ (range 7–99¢).
- These pre-1986 numbers rest on a higher-rate tax system with large intersectoral capital wedges, so read them as an upper-middle anchor for today.

### F9. Jacobs (2018), "The marginal cost of public funds is one at the optimal tax system", ITAX 25(4): 883–912 [SOURCE: abstract, https://link.springer.com/article/10.1007/s10797-017-9481-0; full text not read]
- "the MCF equals one at the optimal tax system, for both lump-sum and distortionary taxes ... the marginal excess burden of distortionary taxes is shown to be equal to the marginal distributional gain at the optimal tax system. Consequently, the modified Samuelson rule should not be corrected for the marginal cost of public funds." This is the strongest theoretical objection: the MEB is a real efficiency cost, but under welfare weights that rationalise the current schedule it is offset by distributional gains. Hendren's inverse-optimum weights (F0) give the efficiency (Kaldor–Hicks) version, which keeps an MCPF above 1 for payers who stand where taxes come from.

## Synthesis: best-supported MCPF

| tax | central MEB | range | load-bearing source |
|---|---|---|---|
| federal individual income tax, broad proportional rise | 0.20 | 0.09–0.35 | SSG 2012 p. 42 (0.195 at ETI 0.25); range from SSG's ETI band 0.12–0.40 [CALCULATION: invert 0.195 = x/(1−x) at e = 0.25 for the rate factor k = 0.653, then x = e·k: e = 0.12 → 0.085, e = 0.40 → 0.353] |
| federal, top-focused rise | 0.35 | 0.16–0.85 | SSG 0.339; HSK 2013 1.16, 1993 1.85; Hendren g(top) 0.65 → 0.54 |
| payroll tax (labor wedge, weak benefit link) | 0.20 | 0.10–0.30 | no direct modern US estimate found [GAP]; BSW labor taxes 0.19–0.23; KK UK 0.10–0.26; benefit linkage lowers it |
| state-local sales + property mix | 0.20 | 0.13–0.35 | M&Z 2008 0.13–0.19 without labor supply or saving; add the shared labor wedge [INFERENCE]; benefit-view property tax → ~0 (weak here, see O2) |
| **US tax mix, financing-weighted** | **0.25** | **0.10–0.50** | OMB A-94 1992 and 2023 (0.25); Hendren-weighted λ_h 1.286 (0.29, repo); SSG broad 0.20; Heckman–Smith "consensus" 0.30–0.50; BSW 0.17–0.56 |

Feldstein's 0.72–2.06 rests on ETI 1.04, which the later ETI literature rejects (SSG 0.12–0.40). It sits outside the range as an outlier, not an end point.

## (1) How to apply it to this account

- **Group's own taxes:** the excess burden of the group's own taxes falls on the group. It is not a cost to others and is not added. The account already nets the group's taxes in dollars.
- **Removal saves others taxes:** removing the group lets other residents' taxes (or service cuts) fall by the net transfer. If the margin is distortionary taxes, they also save MEB × that amount. The saved distortion under a balanced-budget reading is (MCPF − 1) × net transfer, applied only to the tax-financed part.
- **By component (F5):**
  - *State-local cash gap and displaced* (60.8% low / 56.4% high of the total): financed by other residents' taxes now. Apply the MEB in full, scaled by the share of the margin that is taxes rather than cuts to others' services. A cut to services carries no excess burden; its cost is already in the dollar account.
  - *Federal cash gap* ($32.4 / 61.2bn): borrowed now. Under tax smoothing, the later taxes that service the debt carry the same MEB in present value, so it applies. If r < g lets the debt roll over, the factor is weaker.
  - *Pension accrual* ($82.9 / 77.8bn): the account values it at the benefits **current law can pay**. Under current law, a larger claimant pool after trust-fund depletion is paid for by **smaller benefits for others**, not higher payroll taxes. A pro-rata benefit cut is close to lump-sum, so **MEB ≈ 0 on the current-law reading**; it is an arm only if Congress closes the gap with taxes. [INFERENCE; current-law-first]
  - *Capital return* ($37.1 / 61.9bn): public capital is bought with taxes or debt, so the MEB applies when capital is added. It is an imputed resource cost, so this is the weakest of the applied parts.
- **Non-fiscal and real-resource items** carry no multiplier. The production term (−$0.7bn) and any scale benefit that enters as a dollar budget saving are already inside the net fiscal flow. Multiplying the *net* treats the group's tax dollars and benefit dollars symmetrically: each tax dollar the group pays spares others 1 + MEB as well.
- **Size of the change:** the transfer is ≈5–6% of all US government receipts, so it is not marginal. MEB rises with the rate; for a cut of that size the average saved MEB is ≈2–3% below the marginal. That is negligible against the parameter range. [INFERENCE: DWL ∝ τ², Δτ/τ ≈ 0.05]

## (2) Beside reading (arithmetic) [CALCULATION: python3 one-liner in this session]

Base A, the whole net transfer ($390.29–461.24bn), × MEB:
- 0.10 → $39.0–46.1bn; 0.20 → $78.1–92.2bn; **0.25 → $97.6–115.3bn**; 0.29 (λ_h) → $113.2–133.8bn; 0.50 → $195.1–230.6bn.

Base B, the current-law application, excluding the pension accrual paid by benefit cuts: $390.29 − 82.92 = **$307.38bn**; $461.24 − 77.83 = **$383.41bn**. (These equal the cash-set band in `main_case_2026_10_05/derived/summary.json` to the cent: `federal_split_2024.csv` gives `cash_set_net_cost_bn` = net cost − `accrual_bn`, and summary.json gives the cash set's change from the main case as −82.9 / −77.8. So the accrual column is the *increment* of accrued promises over the group's current Social Security and Part A cash flows, and those current flows already sit in the federal cash gap, where today's payroll taxes finance them and the MEB applies. Base B is therefore the cash set, and only the increment is excluded. [DATA: both files])
- 0.10 → $30.7–38.3bn; 0.20 → $61.5–76.7bn; **0.25 → $76.8–95.9bn**; 0.29 → $89.1–111.2bn; 0.50 → $153.7–191.7bn.

**Recommended beside line:** "Raising the transfer through distortionary taxes costs other residents a further **≈$77–96bn** a year (MEB 0.25 on the $307–383bn they finance through taxes; range $31–192bn at MEB 0.10–0.50). With the pension accrual included, it is $98–115bn." Never added to the headline.

## (3) Strongest objections

- **O1. The estimand is budgetary.** The account prices dollars moved between budgets, and the MEB is a welfare cost. Adding the two mixes units. CBO, JCT, the NAS (2017) fiscal chapters and the Heritage and Cato accounts do not apply an MCPF to fiscal-impact totals. [UNVERIFIED for NAS 2017; not read in this scan] This is decisive against a headline and irrelevant to a beside reading.
- **O2. Lump-sum-ish finance.**
  - Part of the state-local margin is cuts to others' services, which carry MEB 0 and a dollar loss already counted.
  - Land-value property tax is close to non-distortionary.
  - Fees "that function like market prices" carry MCPF 0 (OMB 2023 §11.b).
  - The pension accrual is paid by benefit cuts (above).
  - Against that, the benefit view of the property tax is *weak here*. The extra levy buys services for other households, so to the payer it is a pure tax.
- **O3. Borrowing.** The federal part is debt-financed. Tax smoothing gives the same MEB in present value; r < g (Blanchard 2019) lowers it. The federal cash gap is only 12–20% of the total, so this moves the reading by ≤$15bn.
- **O4. Distributional offset** (Jacobs 2018; Kaplow; HSK's Okun's-bucket point). At an optimal schedule the MEB equals the distributional gain, so the social MCF is 1. That holds only under the welfare weights that rationalise current taxes. The cost-to-others-in-dollars estimand is an efficiency frame, so the MEB applies there; under a social-welfare frame it can vanish. [FRAMING-SENSITIVE]
- **O5. Symmetry.** Each benefit to others that the account counts as a fiscal dollar (group taxes, scale savings in general government) also spares others MEB, and multiplying the net captures that. The reading becomes asymmetric only if non-fiscal gains to natives, such as labor-market surplus or lower prices, are left unmultiplied *and* they would have lowered taxes. They do not pass through budgets, so leaving them unmultiplied is correct, not asymmetric.
  - The asymmetry that does exist runs the other way. The group's induced behavior shrinks others' bases, for example native labor displaced into transfers; it is in the account only as the $8.8bn displaced line.
- **O6. Double counting.** The account has no dynamic tax-rate response, so the MEB is not already inside it. If a future version scores the rate changes needed to close budgets dynamically, the beside line must go.

## Would economists accept it?

As a **sensitivity, yes**. It is the textbook "1 + λ" adjustment: OMB A-94 has asked for it as a supplementary analysis since 1992 (25%); Heckman et al. use φ = 0.3–0.5 in benefit-cost ratios; HSK 2020 report the tax MVPFs that let one choose the financing margin. Most would argue over the parameter (0.1 vs 0.5) and the tax-financed share, not over whether it belongs beside the account.

As a **headline, no**. HSK argue explicitly against assuming a financing margin, and OMB keeps it supplementary even for federal investments. A fiscal-impact account is a budgetary estimand. No mainstream immigration fiscal study found in this scan multiplies its total by an MCPF. [GAP: not exhaustively checked]

## Gaps and next queries
- [GAP] Dahlby (2008, MIT Press) US tables and Jorgenson–Yun MEB 0.38 not read in primary text. Next: an archive.org or Google Books preview of Dahlby ch. 5; Jorgenson & Yun, *Lifting the Burden* (2001).
- [GAP] No modern US payroll-tax-specific MEB found. Next: "marginal excess burden payroll tax benefit linkage" (Liebman; Feldstein–Samwick).
- [GAP] Whether NAS 2017 or CBO immigration estimates mention the MCPF. Next: `rg` the NAS PDF if it is in `sources/`.
- [GAP] Whether the 2025 OMB withdrew the 2023 A-94 (A-4 2023 was rescinded); the 25% value is the same in both.
- [GAP] Accrual MEB ≈ 0 holds after trust-fund depletion (~2033–34, Trustees). Before then the group's claims draw down trust-fund bonds that general revenue redeems, so a small share of the increment is tax-financed. Not quantified; ≤ 0.25 × $82.9bn = $20.7bn is the ceiling.
- Tools: Firecrawl returned 402 (credits exhausted) on the first search; all web discovery went through Exa. Searches used: 8 of 25.

## Sources this lane found that ladder 250 / world_ledger_2026_09_27 lacks
Ladder 250 rests on HSK NBER w26144 (1.16), Heckman–Smith 1998 (1.5), OMB A-94 1992 (1.25) and Hendren w20351 (λ_h 1.286). New here:
1. Saez, Slemrod & Giertz (2012), JEL 50(1). p. 42: MEB $0.195 per $ for a broad proportional federal income-tax rise and $0.339 for the top 1%, at ETI 0.25 (band 0.12–0.40); fn 72: $0.678 at e = 0.5. pp. 8–9, eq. (6): top-bracket MECF $1.38. p. 10: 22% when shifted income stays taxed. **This is the modern broad-based anchor ladder 250 lacks; it sits between 1.16 and 1.29.**
2. HSK, published QJE 135(3) 2020, Table II: the same values as the NBER version (top tax 2013 1.16 [0.87, 1.92], 1993 1.85, 2001 1.37). pp. 1222–24 argue against assuming a 1+φ financing margin. Ladder 250's read had "QJE not reached"; it is now confirmed.
3. OMB A-94, revised Nov 2023, §11, p. 17: still "25 cents per dollar of revenue", now "may" include and supplementary only; MCPF 0 for user charges; cites HSK. The repo read had only the 1992 text.
4. Feldstein, NBER w5055 (1995; REStat 1999), OCR: ε = 1.04 gives a 72¢ aggregate tax inefficiency ratio and $2.06 per $ in TAXSIM. An outlier upper bound.
5. Kleven & Kreiner (2006), JPubE 90, Table III: no US; UK 1.00–1.36 (S6 baseline 1.26), Denmark to 3.51. Participation responses add ≈0.1–0.15.
6. Ballard, Shoven & Whalley, NBER w1043 (1982): 34–48¢ for the whole system. Table 5: labor 19¢, income taxes 55¢, sales on non-excise goods 35¢. The AER 1985 range, via Fullerton & Henderson w2353 p. 2: 17–56¢, centre 33¢.
7. Muthitacharoen & Zodrow (2008), NTA Proceedings, Tables 1–2: state-local property tax 14.4% (12.2–19.1%), sales tax 12.9% (12.7–15.1%), without labor supply or saving. **The only state-local estimate; ladder 250 has none.**
8. Jacobs (2018), ITAX 25(4), abstract: MCF = 1 at the optimal tax system. The distributional-offset objection.

## One divergence worth the lead's check
World ledger row 294 multiplies others' **whole** fiscal cost by λ. The $82.9 / 77.8bn pension-accrual increment, at payable benefits, is paid under current law by pro-rata cuts to others' benefits, not by distortionary taxes, so its λ − 1 ≈ 0 (section (1) above). On v5 that trims the multiplier base from $390.3–461.2bn to $307.4–383.4bn (the cash set): at λ 1.25 it is −$20.7 / −19.5bn. Also, 1.5 is Heckman–Smith's convention ("in the range suggested by Browning 1987"), not an estimate. Modern estimates (SSG 0.195; Hendren-weighted 0.29; Kleven–Kreiner UK 0.26) cluster at 1.2–1.3.
