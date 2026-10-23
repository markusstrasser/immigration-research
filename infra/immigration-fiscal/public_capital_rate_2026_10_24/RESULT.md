claude-opus-5-5

**Verdict:** Keep the case's rate essentially where it is. The opportunity cost of the group's public capital is
**2.22% central** (state/local lines; 2.55% on the small federal lines), range **2.08–3.30%** (federal 2.08–4.80%).
That moves the $368.0–436.6bn headline by **+$2.9bn / +$3.2bn** at the central rate (to $370.9–439.7bn) and by
**+$0 to +$24.3bn / +$26.9bn** across the range (top: $392.3–463.4bn). Every capital line moves up in proportion:
schools, colleges, police, health, roads, transport, parks, general government, the enterprises and the
union-completion/coverage capital (table, §4). OMB's 7% on the whole stock, the case's own `capital_7pct` beside arm
(+$96.15 / +$105.47bn → $464.2–542.0bn, reproduced exactly here), applies only if every dollar of the capital displaced
private investment AND the displaced return is measured with its risk premium while the rest of the case discounts
at a risk-free 2.08%. Neither condition holds. That makes it an inconsistent beside arm, not an alternative central.
The one reading that comes near it, Burgess–Zerbe's SOC with measured returns throughout (6.10%,
+$78.6 / +$86.2bn), would also move the case's consumption rate and its pension leg; it is not a capital-only change.
[CALCULATION: `rate_model.py` → `derived/rate_model.json`, `derived/line_deltas.csv`]

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
| **Central: d central, r_i Baa real** | **2.222%** | **2.547%** | **+2.86 / +3.18** | **370.9–439.7** |
| High: d high, r_i GRR measured 7.52% | 3.297% | 4.801% | +24.27 / +26.86 | 392.3–463.4 |
| Beside: d central, r_i GRR measured | 2.622% | 3.876% | +11.00 / +12.26 | 379.0–448.8 |
| Beside: Burgess–Zerbe margin, CBO 33/43/24 weights, risk-consistent | 2.547% | 2.547% | +9.11 / +9.99 | 377.1–446.6 |
| Beside: Burgess–Zerbe SOC, CBO weights, measured returns (7.52/5.40/5.40) | 6.10% | 6.10% | +78.55 / +86.17 | 446.6–522.7 |
| Beside: full displacement at 7% (A-94 1992; case arm `capital_7pct`) | 7.00% | 7.00% | +96.15 / +105.47 | 464.2–542.0 |

The cash set moves by the same dollars; the capital return is not a pension leg (checked in the script: the set and
cash 7% deltas match to 1e-6).

## 4. Dollars by line

The capital return at 2.081% is **$40.68bn (low end) / $44.62bn (high end)**, derived from the v9 `capital_7pct` arm
(`main_case_2026_10_16/derived/rate_check.json`): Δ/(0.07/r_c − 1). The line split comes from `summary.json`
`v9.one_rate` B-minus-v8 parts (v8: 2% low end, 3% high end), scaled to the v9 total. The scale factor is within 1% of
1, and both methods agree within 0.2%.

| Line group | Return at 2.081% (low / high) | Δ central | Δ high |
|---|---:|---:|---:|
| Enterprises (state/local housing, transit, utilities…) | 12.65 / 12.64 | +0.85 / +0.85 | +7.39 / +7.39 |
| Schools (K-12) | 10.61 / 10.60 | +0.72 / +0.72 | +6.20 / +6.19 |
| Roads | 6.98 / 9.54 | +0.47 / +0.66 | +4.08 / +5.66 |
| Colleges | 3.35 / 3.35 | +0.23 / +0.23 | +1.96 / +1.95 |
| General government | 2.28 / 3.23 | +0.19 / +0.27 | +1.51 / +2.14 |
| Union-completion and coverage capital | 1.96 / 2.18 | +0.13 / +0.15 | +1.14 / +1.27 |
| Police/safety | 1.19 / 1.19 | +0.13 / +0.13 | +0.93 / +0.93 |
| Parks | 1.06 / 1.23 | +0.07 / +0.10 | +0.62 / +0.80 |
| Health | 0.60 / 0.60 | +0.06 / +0.06 | +0.45 / +0.45 |
| Transport (air, federal) | 0.00 / 0.07 | 0 / +0.01 | 0 / +0.08 |
| **Total** | **40.68 / 44.62** | **+2.86 / +3.18** | **+24.27 / +26.86** |

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
  r_i. Adopting a measured r_i of 7.5% consistently would push that share toward 1 and credit the group with more
  receipts, so the cost **falls**. Rough scale from v7's item-6 corporate line at the high end (−$16.68bn at 0.37):
  about −$28bn at a share of 1 [INFERENCE; not v9-priced]. That roughly cancels the high-end capital rise
  (+$26.9bn). A measured-return reading therefore leaves the high end near unchanged once applied symmetrically.
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

## Gaps
- [GAP] US municipal-bond → private-investment displacement is unmeasured; d_bond borrows CBO's federal figure.
- [GAP] d_tax high (0.15) is an inference for business-paid taxes; the measured MPS product tops out at 0.078.
- [GAP] Enterprise debt share is unmeasured (21% applied to them).
- [GAP] The CBO PDFs were read via Exa's verbatim extraction; curl returned an HTML stub. Lind 1990 is abstract-only.
  M-25-23 (A-94 rescission) is cited from a tracker, not read. The A-4 2023 preamble was not read.
- [GAP] The 2024 10-yr TIPS mean computed here from FRED DFII10 is 1.86%; the v9 decision quotes 1.94%. A series
  choice to check; not load-bearing here.
- [GAP] The item-6 symmetry figure is a v7-scale inference; pricing it needs the v9 package (`postFor`).

## Reproduce
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/public_capital_rate_2026_10_24/rate_model.py`
(deterministic: three runs, the last after the session crash, gave md5 7e6e8cbf… for `derived/rate_model.json` and 4219417c… for `derived/line_deltas.csv`).
Inputs: `main_case_2026_10_16/derived/{rate_check,summary}.json`. Raw downloads are in `_cache/` (ignored).

## Files covered and skipped
Read: OMB A-4 2003/2023, A-94 1992/2023, M-25-15, NPP w31526, Moore et al. 2004 (SFU copy), MBV 2013, Burgess–Zerbe
2011, the GRR usdata.csv, FRED AAA/BAA/DFII10/EXPINF10YR, Pinardon-Touati 2026, CBO (Exa), and the school lane §3, §5,
§7. Skipped: Bradford 1975 and Harberger 1969/72 (cited through Moore and Burgess–Zerbe, not read), Szekeres 2011
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
