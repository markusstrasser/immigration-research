claude-opus-5-5

**Verdict:** Read the rate together with item 6. Pricing the displaced private return above the Baa yield also
credits the group with corporate tax on that same return, which item 6 counts only at TP-5's normal share (0.37). On
one parameter, θ (the share of the measured return above the safe rate that scales with capital), the paired v9 band
is **$370.9–439.8bn at θ = 0, $375.0–430.9bn at the anchor θ = 0.49, and $379.2–421.7bn at θ = 1** (set, central
displacement; cash $287.3–356.1 / $291.3–347.3 / $295.5–338.1bn). At θ = 0, r_i is the Baa yield (3.49% real), not
the rate itself: the rate is r_c + d·(r_i − r_c) = 2.22% state/local and 2.55% federal. The scale runs to the GRR
measured return (7.52%) at θ = 1. The anchor is Farhi & Gourio (2018, BPEA, Table 12):
in 2001–16, risk premia plus unmeasured capital are 5.32 of the 10.87-point wedge between the return on capital and the
safe rate, net of depreciation; markups are 5.55. Its variants give 0.35–0.70, and that whole range keeps the band
within $373.8–433.4bn to $376.7–427.1bn. **I recommend θ = 0.49 paired: $375.0–430.9bn**, rate 2.42% state/local and
3.20% federal, item 6's high-end corporate response 0.678. It is the one measured split of the wedge into risk and
rent that asset prices discipline. At the high end the two legs nearly cancel, and the item 6 leg is larger:
−$13.3bn against +$7.7bn. So a higher private return narrows the band; it does not raise the headline. The unpaired
central (θ = 0, 2.22% / 2.55%, +$2.9 / +$3.2bn) remains the floor of the pairing. The unpaired high scenario (GRR at
high displacement, +$27.0bn at the high end) counts the return without its corporate tax. Paired at θ = 1, its high
end is $436.3bn, −$0.2bn from today. OMB's 7% on the whole stock (`capital_7pct`, +$96.15 / +$105.47bn) remains an
inconsistent beside arm: it needs full displacement, a risk-bearing return beside risk-free valuations elsewhere,
and item 6 left at 0.37 (§3, §6, §7).
[CALCULATION: `theta_item6.cjs` → `derived/theta_item6.json`; `rate_model.py` → `derived/rate_model.json`,
`derived/theta_pairing.csv`, `derived/line_deltas.csv`; SOURCE: `reads/farhi_gourio_2018.md`]

# Opportunity cost of public capital: rate model and repricing of v9 item 20

## 1. Frameworks and the steel-men

- **Shadow price of capital (Bradford 1975; Lind 1982/1990; Moore et al. 2004; NPP 2023).** Value displaced private
  investment in consumption units (×SPC) and discount everything at the consumption rate. SPC > 1 only because taxes
  drive a wedge between the pre-tax return and savers' return. NPP's central SPC is 1.1: r_c 2%, risk-adjusted pre-tax
  r_i 3.1%, τ 35% (NPP pp. 11–13, `reads/npp_2023_spc.md`).
- **Harberger weighted rate / SOC (Harberger 1969/72; Burgess & Zerbe 2011).** The rate is
  Σ shares × the cost of each source: displaced investment at the pre-tax return, induced saving at savers' return,
  foreign funds at their marginal cost. Moore et al. call it "generally invalid" for flows (p. 7), but for this case's
  object, the annual user cost of a stock held in steady state, the two coincide. When a stock is permanently
  displaced, the lost private stock is replaced each year too, so the annual loss is d·K·r_i. The steady-state SPC is
  then r_i/r_c (Moore eq. 1 with no depreciation or reinvestment term). Formula used:

  **r = r_c + d·(r_i − r_c)**, where d is the share of the stock's financing that displaced domestic private
  investment. The consumption-financed and foreign-financed shares cost r_c.

  So the SPC applies **only to the displaced share d**, never to the whole stock's return. Charging 7% on the whole
  stock is the special case d = 1 with an unadjusted r_i.
- **OMB.** The A-4 of 2023 (2.0% plus an SPC of 1.0–1.2 on the capital-incidence share, pp. 76–79) was **revoked on
  12 Feb 2025** (M-25-15), and A-4 (2003) is back: report 3% and 7%. A-94 (1992), listed as current, sets 7% for
  "proposed investments" and names "a Federally funded highway" as a 7% case (§8.b–c). It also calls the SPC
  "analytically preferred". The guidance now in force is the 7% steel-man; the 2023 economics is the SPC one.
  [SOURCE: `reads/omb_a4_a94.md`]
- **Steel-man for 2.08%.** It is a resource cost in consumption units, and the case discounts the pensions on the
  same Trustees path. State and local capital is mostly tax-financed under balanced-budget rules, and taxes come
  "almost entirely at the expense of private consumption" (Moore et al. 2004 p. 6). A-4 (2023) put the open-economy SPC
  at 1.0. Item 6 already takes Treasury's normal return to be the risk-free rate.
- **Steel-man for 7%.** It is the in-force OMB rule, and the measured pre-tax return on all US capital was 7.52% in
  2024 (GRR). Burgess & Zerbe's argument is the strongest: the capital market is the marginal source of every dollar,
  because any tax could instead pay down debt. The operator's full-cost telos favours charging what society gives up.
- **Central model chosen:** the steady-state Harberger/SPC formula with **measured d** and a **risk-consistent
  marginal r_i**. The rest of the case prices time at a risk-free rate: the Trustees path, and item 6's normal return.
  A risk-inclusive 7% paired with 2.08% implies a 71% capital-tax wedge, against τ_k = 0.25 in 2024
  (NPP p. 11; GRR). The marginal displaced project earns the marginal return; inframarginal rents are not displaced
  (Moore et al. p. 17).

## 2. Measured inputs (primary sources; `reads/`)

| Input | Low | Central | High | Source |
|---|---:|---:|---:|---|
| Investment displaced per $ of borrowing, d_bond | 0.15 | 0.33 | 0.50 | Huntley 2014 pp. 1, 7–8; CBO LTBO May 2025 still 33¢ |
| MPS out of disposable income | 0.024 | 0.067 | 0.11 | Dynan et al. via Moore 2004 n. 7 |
| Share of a saving drop that hits domestic investment | 0.39 | 0.57 | 0.71 | Huntley 2014 (1 − foreign offset) |
| d_tax | 0.009 | 0.038 | 0.15 [INFERENCE: widened for business-paid taxes] | product of the two rows above |
| Debt share of state/local capital | | 0.21 | | school lane §7 |
| **d, state/local** | 0.039 | **0.099** | 0.223 | 0.79·d_tax + 0.21·d_bond |
| d, federal lines | 0.009 | 0.33 | 0.50 | tax-financed to CBO deficit-financed |
| Marginal pre-tax r_i | | **3.49%** Baa real 2024 (Aaa 2.78%; CE r_c/(1−τ_k) 2.77%) | 7.52% GRR all-capital 2024 | FRED, Cleveland Fed; GRR usdata.csv |
| Consumption rate r_c | | 2.081% (case) vs A-4 2023 2.0% | | consistent within 0.08 pt |

Muni-specific evidence is thin. No US estimate of municipal bonds crowding out private investment was found. The
nearest is French local-government *bank* debt: €0.5 less corporate lending per €1 at the lending bank, with an
aggregate output loss of €0.2 (Pinardon-Touati 2026). That supports d_bond ≤ 0.5. The evidence supports this
summary: taxes displace little investment (MPS times the domestic share, about 4¢); bonds displace about a third;
the blended d is about 0.1. [SOURCE: `reads/cbo_crowding_out.md`, `reads/muni_local_debt.md`,
`reads/moore_2004_and_mbv_2013.md`]

## 3. The rate

| Scenario | State/local | Federal | Δ headline, low / high end ($bn) | Headline ($bn) |
|---|---:|---:|---:|---:|
| Low: open economy, SPC = 1 (Lind 1990; A-4 2023 lower value) | 2.081% | 2.081% | 0 / 0 | 368.0–436.6 |
| **Central: d central, r_i Baa real** | **2.222%** | **2.547%** | **+2.89 / +3.22** | **370.9–439.8** |
| High: d high, r_i GRR measured 7.52% (unpaired; §7) | 3.297% | 4.801% | +24.43 / +27.02 | 392.5–463.6 |
| Beside: d central, r_i GRR measured (unpaired; §7) | 2.622% | 3.876% | +11.13 / +12.39 | 379.2–449.0 |
| Beside: Burgess–Zerbe margin, CBO 33/43/24 weights, risk-consistent | 2.547% | 2.547% | +9.11 / +9.99 | 377.1–446.6 |
| Beside: Burgess–Zerbe SOC, CBO weights, measured returns (7.52/5.40/5.40) | 6.10% | 6.10% | +78.55 / +86.17 | 446.6–522.7 |
| Beside: full displacement at 7% (A-94 1992; case arm `capital_7pct`) | 7.00% | 7.00% | +96.15 / +105.47 | 464.2–542.0 |

The cash set moves by the same dollars; the capital return is not a pension leg (checked in the script: the set and
cash 7% deltas match to 1e-6). Since the θ follow-up, the two federal enterprise lines (`ent_other_fed`,
`ent_power_fed`, $0.22bn of return) carry the federal margin; the first pass had labelled them state/local. That
adds $0.03bn central and $0.16bn high.

## 4. Dollars by line

The capital return at 2.081% is **$40.68bn (low end) / $44.62bn (high end)**, derived from the v9 `capital_7pct` arm
(`main_case_2026_10_16/derived/rate_check.json`): Δ/(0.07/r_c − 1). The line split comes from `summary.json`
`v9.one_rate` B-minus-v8 parts (v8: 2% low end, 3% high end), scaled to the v9 total. The scale factor is within 1% of
1, and both methods agree within 0.2%.

| Line group | Return at 2.081% (low / high) | Δ central | Δ high |
|---|---:|---:|---:|
| Enterprises (state/local and federal housing, transit, utilities…) | 12.65 / 12.64 | +0.89 / +0.89 | +7.55 / +7.55 |
| Schools (K-12) | 10.61 / 10.60 | +0.72 / +0.72 | +6.20 / +6.19 |
| Roads | 6.98 / 9.54 | +0.47 / +0.66 | +4.08 / +5.66 |
| Colleges | 3.35 / 3.35 | +0.23 / +0.23 | +1.96 / +1.95 |
| General government | 2.28 / 3.23 | +0.19 / +0.27 | +1.51 / +2.14 |
| Union-completion and coverage capital | 1.96 / 2.18 | +0.13 / +0.15 | +1.14 / +1.27 |
| Police/safety | 1.19 / 1.19 | +0.13 / +0.13 | +0.93 / +0.93 |
| Parks | 1.06 / 1.23 | +0.07 / +0.10 | +0.62 / +0.80 |
| Health | 0.60 / 0.60 | +0.06 / +0.06 | +0.45 / +0.45 |
| Transport (air, federal) | 0.00 / 0.07 | 0 / +0.01 | 0 / +0.08 |
| **Total** | **40.68 / 44.62** | **+2.89 / +3.22** | **+24.43 / +27.02** |

Per line: `derived/line_deltas.csv` (420 rows).

## 5. Symmetry: what a consistent adoption would also move (not priced unless stated)

- **Social Security and Part A promises (the Trustees path).** Under the SPC model these are consumption transfers, so
  they stay at r_c and **nothing moves**: the SPC adjusts only flows that displace capital. Under a single SOC rate
  (Burgess–Zerbe, or 7% everywhere), the present value of accruing promises falls, so the headline **falls**. The
  case's 3%-on-both-legs arm shows the sign: $349.4bn at the low end against $368.0bn (`rate_check.json`
  `both_highrate`). At 6–7% the offset would be far larger; not priced.
- **Enterprise capital.** It is already in every arm above ($12.65bn at 2.081%, the largest group), because the 7%
  arm and the case's rate apply to enterprises. [GAP] Enterprises are probably more bond-financed than 21%, so their d
  is understated. At d_bond = 0.33 alone, their central rate would be 2.55%, about +$0.85bn more.
- **Item 6, taxes on the job-serving business capital.** The high end counts the corporate tax at Treasury's
  normal-return share, 0.37. That share treats the normal return as risk-free, the same premise as this lane's central
  r_i. Now priced on v9 in §7: at a share of 1 the high end falls by $27.25bn (engine −26.23, own coverage −1.17,
  count items +0.15), set and cash alike.
- **Booked public-employee pension and retiree-health normal costs.** These keep BEA's valuations; no change under SPC.
- **Capital return at the job-serving private capital.** The case charges none (item 6 counts only the taxes), so
  nothing to move.

## 6. Disconfirmation: the strongest case against a higher rate, tested

1. **Open economy (Lind 1990; A-4 2023 SPC = 1).** If foreign funds are perfectly elastic, d = 0 and 2.081% is
   exact. *Test:* CBO's measured foreign offset is 0.24 of a deficit dollar (0.43 of the national-saving decline), not
   1.0 (Huntley 2014). **Partly holds:** it sets the low end and cuts the bond-financed displacement by roughly
   two-fifths, but it does not zero it.
2. **Tax financing displaces consumption (Moore et al. 2004 p. 6).** This **holds** for 79% of state/local capital,
   which is why the central d is 0.10. Its counter is Burgess–Zerbe's claim that debt paydown is always the
   alternative use. *Test:* state and local capital budgets are bond-financed project by project, and balanced-budget
   rules bind the rest. Moore et al. say to assume tax financing "unless a specific state or municipal bond issue
   finances" the project. Even granting Burgess–Zerbe in full, d = 0.33 gives only 2.55% with risk-consistent
   returns (+$9.1 / +$10.0bn). The Burgess–Zerbe premise alone does not produce 7%.
3. **Risk (NPP 2023).** The 7.5% return includes an equity premium of about 4 points (Damodaran 4.2%, NPP n. 11).
   With r_c at 2.08%, the implied tax wedge is 71%, against a measured 25%. *Test:* the 2024 real Aaa yield (2.78%)
   and the certainty-equivalent r_c/(1−τ_k) (2.77%) agree to 0.01 pt, and Baa is 3.49%. **Holds**, and it is
   decisive. Burgess–Zerbe concede that the risk-free SOC is "somewhat lower". Their reply, that the project must be
   no less risky than the displaced investment, applies to schools and roads only if their social returns covary
   with the market as equity does. Nothing in the account measures that, so it stays [FRAMING-SENSITIVE].
4. **Removal does not hand capital back; existing buildings are sunk.** In year one, schools stand empty and the
   opportunity cost is the buildings' alternative-use value, near zero for special-purpose structures. *Test:* the
   case's capital return is charged at the long-run response, the stock the US would not have to replace as it
   depreciates (school lane §3–5), so the argument applies to the first-year reading, which already has its own
   response coefficients. It bears on the response, not on the rate. **Does not hold against the rate**, but any
   higher rate belongs only with the long-run response.
5. **Ricardian equivalence.** If tax and debt are equivalent, the financing shares do not matter and d is the
   economy-wide crowd-out of 0.33. That is the Burgess–Zerbe-margin row (2.55%), inside the range. It **does not**
   reach 7%.
6. **Municipal borrowing costs.** Tax-exempt muni yields sit below Treasury yields [INFERENCE; school lane §3], so
   state and local governments' own borrowing rate is *below* 2.08%. This pushes slightly the other way and is
   unpriced.

Net: no tested argument supports 7% on the whole stock alongside the case's other risk-free valuations. The measured
inputs put the defensible range at 2.08–3.30%.

## 7. Paired reading: the rate and item 6 on one parameter

**θ** is the share of the measured private return above the safe rate that scales with capital: risk premia and
returns to unmeasured or expensed intangibles. Rents and market power do not scale. The rate leg uses
r_i(θ) = Baa real 3.49% + θ·(GRR 7.52% − 3.49%) in r = r_c + d·(r_i − r_c) on every capital line, with d as in §3.
Item 6's high-end corporate response is 0.37 + θ·0.63, the TP-5 normal share plus the scaling part of its 63%
supernormal share. The low end already has item 6 at 1, so only its rate moves.

**Pricing.** `theta_item6.cjs` resets `receipt:corporate_capital` and `receipt:corporate_labor` on the high-end
specification (MAIN_SPECS[11]) and runs `evaluateFull` with every v9 post-engine term, averaged over the two methods.
The engine moves the union-completion corporate carriers with the override. Three post-engine pieces price corporate
receipts at the source response: the case's own coverage line parts and the typed parts of items 16 and 16+17. They
are transported by the response ratio. Its 111 checks:
- the unmodified runs reproduce arm B (set and cash);
- θ = 0 is the identity, and the leg is linear in the response;
- every corporate coverage and count part sits at the source response;
- item 19's pass-through is absent;
- the corporate leg at the `capital_7pct` arm equals the leg at the default rate, so the legs add.

| θ | Source | r_i | Rate, state/local / federal | Rate leg, low / high ($bn) | Item 6 response (high) | Item 6 leg (high, $bn) | Set ($bn) | Cash ($bn) |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 0 | today's central | 3.49% | 2.222% / 2.547% | +2.89 / +3.22 | 0.370 | 0 | 370.9–439.8 | 287.3–356.1 |
| 0.353 | FG leverage | 4.91% | 2.363% / 3.016% | +5.80 / +6.46 | 0.592 | −9.61 | 373.8–433.4 | 290.2–349.8 |
| 0.406 | FG, AA rate as risk-free | 5.13% | 2.384% / 3.086% | +6.23 / +6.94 | 0.626 | −11.06 | 374.3–432.4 | 290.6–348.8 |
| 0.472 | FG, Treasury net of term premium | 5.40% | 2.411% / 3.175% | +6.78 / +7.55 | 0.668 | −12.87 | 374.8–431.2 | 291.2–347.6 |
| **0.489** | **FG baseline (anchor)** | **5.46%** | **2.418% / 3.197%** | **+6.92 / +7.71** | **0.678** | **−13.33** | **375.0–430.9** | **291.3–347.3** |
| 0.559 | FG, 10% unmeasured capital | 5.75% | 2.446% / 3.290% | +7.50 / +8.35 | 0.722 | −15.24 | 375.5–429.7 | 291.9–346.0 |
| 0.699 | FG, 10–30% unmeasured capital | 6.31% | 2.502% / 3.476% | +8.65 / +9.63 | 0.810 | −19.05 | 376.7–427.1 | 293.1–343.5 |
| 1 | all excess scales | 7.52% | 2.622% / 3.876% | +11.13 / +12.39 | 1 | −27.25 | 379.2–421.7 | 295.5–338.1 |

At high displacement (d high), the same θ gives $374.4–443.6bn (θ 0), $383.2–440.0bn (0.49) and $392.5–436.3bn (1).
[CALCULATION: `derived/theta_pairing.csv`, `rate_model.json` theta_pairing]

**The anchor.** Farhi & Gourio decompose the wedge MPK − rf into depreciation, rents ((µ−1)/α times the user cost),
risk (r* − rf) and, in an extension, unmeasured capital. Their estimates match six macro and finance ratios at once,
asset prices among them. For 2001–16 the baseline gives rents 5.55, risk 5.23 and unmeasured capital 0.09, so θ =
0.489. They warn that models without risk "have attributed too big a role to rising market power" (p. 149). Their
footnote 16 puts Barkai's bond-rate user cost in that class. [SOURCE: `reads/farhi_gourio_2018.md`, Tables 10 and 12]

**Why 0.49 and not an end.**
- θ = 0 treats the whole equity premium as rent. That is Barkai's construction, which FG reject for ignoring risk.
- θ = 1 treats markups as zero. Their own estimate is 3.3–7.0 points, and Power–Frerick list market power among the
  excess returns.
- The paper's intangible versions (0.56–0.70) rest on "largely illustrative" mismeasurement. Its leverage version
  (0.35) is "conservative" by the authors' account. The baseline sits between and needs neither assumption.
- The choice moves little: across 0.35–0.70 the band stays within $373.8–433.4bn and $376.7–427.1bn.

**Limits.**
- [GAP] FG's split is for the whole private economy over 2001–16, at a −0.35% safe rate. Item 6's base is C-corporation
  taxable income in the group's industries.
- [GAP] The rate leg's θ = 0 starts at Baa, a corporate yield, while TP-5's 0.37 is above a risk-free rate. FG's
  AA-rate version (0.406) is the closer match for the rate leg. The difference is about $1.5bn.
- [INFERENCE] If incumbents' rents scale with market size under a removal, θ is higher. This is unmeasured.

- [GAP] US municipal-bond → private-investment displacement is unmeasured; d_bond borrows CBO's federal figure.
- [GAP] d_tax high (0.15) is an inference for business-paid taxes; the measured MPS product tops out at 0.078.
- [GAP] Enterprise debt share is unmeasured (21% applied to them).
- [GAP] The CBO PDFs were read via Exa's verbatim extraction; curl returned an HTML stub. Lind 1990 is abstract-only.
  M-25-23 (A-94 rescission) is cited from a tracker, not read. The A-4 2023 preamble was not read.
- [GAP] The 2024 10-yr TIPS mean computed here from FRED DFII10 is 1.86%; the v9 decision quotes 1.94%. A series
  choice to check; not load-bearing here.
- [DONE 2026-10-24] The item 6 symmetry is now priced on v9 (§7); the v7-scale inference (−$28bn) is superseded by
  −$27.25bn.
- [GAP] θ's anchor is one paper. Karabarbounis–Neiman (2019, factorless income) and De Loecker–Eeckhout–Unger (2020)
  were not read. Crouzet–Eberly (rents vs intangibles in Q) was not read either. Barkai is characterized through FG's
  footnote, not read.

## Reproduce
```sh
node infra/immigration-fiscal/public_capital_rate_2026_10_24/theta_item6.cjs        # ~15 s; writes derived/theta_item6.json
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/public_capital_rate_2026_10_24/rate_model.py
```
Order matters: `rate_model.py` reads `theta_item6.json`. Inputs: `main_case_2026_10_16/` package and
`derived/{rate_check,summary}.json`, and `job_capital_taxes_2026_10_14/derived/item.json`. Raw downloads are in
`_cache/` (ignored). Byte-identity checksums are in the findings log.

## Files covered and skipped
Read: OMB A-4 2003/2023, A-94 1992/2023, M-25-15, NPP w31526, Moore et al. 2004 (SFU copy), MBV 2013, Burgess–Zerbe
2011, the GRR usdata.csv, FRED AAA/BAA/DFII10/EXPINF10YR, Pinardon-Touati 2026, CBO (Exa), and the school lane §3, §5,
§7. For the θ follow-up: Farhi & Gourio 2018 (PDF, Tables 2, 4, 10–12), item 6 RESULT §2 and `item.json`, and the v9
package's `companions.cjs`, `item_rate.cjs` and `rate_check.cjs`. Skipped: Bradford 1975 and Harberger 1969/72 (cited through Moore and Burgess–Zerbe, not read), Szekeres 2011
comment, MBV 2013 SOC weights detail (not needed for the arithmetic).

## Findings log (append-only)
- [DONE 2026-10-24] stub placeholder; model, inputs, arithmetic, symmetry (§5) and disconfirmation (§6) are complete above.

### 2026-10-24 entry 1 — case amounts and the rate guidance now in force
- Case: v9 `rate_check.json` arm `capital_7pct` (capital only, pensions stay on the Trustees path; `item_rate.cjs:10`)
  = $464.18–542.04bn set vs B $368.03–436.56bn ⇒ +$96.15 / +$105.47bn. Linear ⇒ capital return at 2.08107%
  = $40.68bn low / $44.62bn high. [DATA: main_case_2026_10_16/derived/rate_check.json]
- OMB A-4 (2023) was revoked 2025-02-12 (M-25-15) and A-4 (2003) reinstated; whitehouse.gov circulars page lists
  A-94 of 1992 as current. A-94 (1992) §8.b(1): 7% base case "for proposed investments"; §8.b(3) SPC preferred;
  §8.c(3): Treasury rate only for "internal" federal cost savings, 7% for external social benefits (highway example).
  [SOURCE: reads/omb_a4_a94.md]
- NPP (w31526) pp. 10–13: central SPC 1.1 (r_c 2%, r_i 3.1% risk-adjusted pre-tax, τ 35%, s 22%, μ 10%); GRR pre-tax
  return 7.4% (1947–2021), 6.7% (1992–2021); 7% with 2% implies 71% tax wedge (inconsistent).
- [GAP] GRR current series (paulgomme.github.io) 2024 value; state/local displacement evidence; Huntley PDF (curl got HTML).

### 2026-10-24 entry 2 — inputs measured and first pricing (`rate_model.py` → `derived/rate_model.json`, `line_deltas.csv`)
- Displacement: Huntley (CBO WP 2014-02) 33¢ (15–50¢) of private investment per $1 of federal deficit; private saving
  +43¢, foreign +24¢; CBO's May 2025 LTBO still uses 33¢ (66¢ and 0¢ as alternatives). Moore et al. 2004 pp. 6–7:
  state/local balanced-budget rules ⇒ assume tax financing unless a specific bond issue; MPS out of disposable income
  2.4–11% (Dynan et al., their n. 7). Muni-specific: Pinardon-Touati (Apr 2026, France, local-government BANK debt)
  €1 of debt demand cuts that bank's corporate lending €0.5; aggregate output −€0.2. No US muni → private-investment
  estimate found. d(state/local) = 0.79·d_tax + 0.21·d_bond = 0.039 / 0.099 / 0.223.
- Private return: GRR series (paulgomme.github.io usdata.csv, live; 2024 rows present): all-capital pre-tax 7.52% (2024),
  7.41% (1947–2024); business pre-tax 9.78% (2024); all-capital after-tax 5.40% (2024); τ_k 0.25 (2024). Marginal
  return proxies (Moore 2004 method, bond yields): Aaa 2.78%, Baa 3.49% real in 2024 (FRED AAA/BAA minus Cleveland Fed
  10-yr expected inflation 2.26%). CE pre-tax r_c/(1−τ_k) = 2.77% — matches Aaa.
- Rate: low 2.081% (Δ0) · central 2.22% SL / 2.55% fed (Δ +$2.9 / +$3.2bn) · high 3.30% SL / 4.80% fed
  (Δ +$24.3 / +$26.9bn) · beside: d central with unadjusted 7.5% (+$11.0 / +$12.3bn) · full displacement 7%
  (+$96.15 / +$105.47bn = the case's own `capital_7pct` arm, reproduced exactly).
- [GAP] FRED DFII10 2024 daily mean computed here = 1.86%, the v9 decision quotes 1.94% for the 2024 10-yr TIPS
  average; source series may differ (Treasury par real curve vs FRED constant-maturity). Not load-bearing here.

### 2026-10-24 entry 3 — final arms, symmetry, disconfirmation (post-crash resume)
- Burgess–Zerbe arms added to `rate_model.py`: CBO weights 33/43/24 for every line. With risk-consistent returns
  the rate is 2.547% (+$9.11 / +$9.99bn); with measured GRR returns (7.52/5.40/5.40%) it is 6.10% (+$78.55 / +$86.17bn).
- Symmetry (§5): under SPC nothing besides capital moves. A single SOC rate would lower the pension-promise value
  (sign shown by `both_highrate`: $349.4bn low end). A measured r_i would raise item 6's high-end corporate share from
  0.37 toward 1, about −$28bn [INFERENCE from v7 scale]. Enterprises are already in every arm.
- Disconfirmation (§6): six tests. Risk consistency is decisive against 7%: real Aaa 2.78% = CE 2.77%. Sunk
  buildings bear on the response, not the rate. Lind's open economy sets the low end. Ricardian equivalence and
  Burgess–Zerbe both land at 2.55%.
- Rerun after the crash: byte-identical outputs (rate_model.json 7e6e8cbf…, line_deltas.csv 4219417c…).
4. 2026-10-24 01:14 JST (from `date`): θ follow-up opened (paired rate × item 6 corporate response). [DONE 01:24] anchor,
   package pricing and the federal enterprise label fix are in §7, §3 and the Verdict.
5. 2026-10-24 01:24:45 JST (from `date`): ran `theta_item6.cjs` and `rate_model.py` twice in order, and the outputs are
   byte-identical. md5: line_deltas.csv f9e53243…, rate_model.json 2f83ec37…, theta_item6.json c1b1c9e6…,
   theta_pairing.csv a5e3f4d7…. The θ anchor is Farhi & Gourio 2018 Table 12 baseline 2001–16, θ = 0.489
   (`reads/farhi_gourio_2018.md`). The federal enterprise fix moves the unpaired central from +2.86/+3.18 to
   +2.89/+3.22.

## Revision, 2026-10-24 15:00 JST: the bound over θ, and highway grants

A blind review found that §7 pairs only the high end: the low end keeps item 6 at 1, which under §7's own formula is
θ = 1, while its rate leg used θ = 0.49. Farhi–Gourio measure the risk share of the wedge, not the share that scales
under a removal, so θ is not settled. The operator adopted the bound over θ: **the low end at θ = 1** (item 6 at 1, the
rate at r_i = GRR 7.52%) and **the high end at θ = 0** (item 6 at TP-5's 0.37, the rate at r_i = Baa 3.49%). Item 6 is
unchanged at both ends; only each end's rate moves.

The review also found that d_sl treated state and local highway capital as financed like K-12, ignoring federal-aid
grants. The federal government funded 42.5% of highway capital spending in 2014 (FHWA, 23rd *Conditions and
Performance Report*, Highlights). `hwy_sl` now takes d = 0.425·d_fed + 0.575·d_sl (0.197 central, against 0.099).

| Reading | Set, $bn | Cash, $bn |
|---|---|---|
| **Bound: θ = 1 low, θ = 0 high (adopted)** | **380.9–440.4** | **297.3–356.8** |
| θ = 0 at both ends | 371.4–440.4 | 287.8–356.8 |
| Anchor θ = 0.489 at both rates, item 6 paired at the high end only (superseded) | 376.1–432.4 | 292.4–348.8 |
| θ = 1 at both ends | 380.9–424.1 | 297.3–340.5 |

Rates at the bound: state and local 2.62% low / 2.22% high, state and local highways 3.15% / 2.36%, federal 3.88% /
2.55%. The highway change adds $1.8bn to the low end and $0.6bn to the high end. [CALCULATION: `derived/rate_model.json`
`theta_pairing.bound`] The table in §7 and the verdict above keep the first pass's numbers as recorded. Rerun with both
commands: IDENTICAL 16/16.
