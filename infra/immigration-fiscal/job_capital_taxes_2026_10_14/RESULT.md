claude-opus-5-5

**Verdict:** Taxes on the business capital that serves the group's jobs come to **$66.5bn a year at the band's low end
and $40.3bn at its high end**, both at the personal allocation, which v7 uses at both ends (SE $2.0bn / $1.1bn). That
much leaves with the union of 39.71M people under the case's full-adjustment premise, and main case v6 counts it at
zero. [CALCULATION: `job_capital.py` → `derived/item.json` central_bn, `derived/summary.json` central] The two ends
differ only in corporate tax:
- at the low end it leaves whole ($41.6bn);
- at the high end only its normal-return share leaves: 0.37, from Treasury OTA Technical Paper 5, p. 7 ($15.4bn).

Business property tax ($17.7bn at response 0.8806) and other production taxes ($7.2bn at 1) are the same at both ends.
[CALCULATION: same, by line] The shared allocation, a companion reading only, gives $72.6bn / $43.7bn.
[CALCULATION: same]

Mining responds at 0 on all three lines at both ends. It is a fixed, world-priced resource that is still extracted
without the group. Counted like other industries, mining would add $7.4bn low / $6.4bn high (arm
`mining_as_other_industries`). [CALCULATION: `summary.json` mining]

Across the arms, each one change from the central:
- the low end runs from **$63.1bn** (federal tax on foreign-source income removed) to **$75.9bn** (the plain wage share
  in place of the industry key). The exception is arm `normal_return_share`, which puts corporate tax at 0.37 at both
  ends and so gives $40.3bn at the low end too;
- the high end runs from **$35.3bn** (corporate at Power and Frerick's 2003–2013 normal-return share, 0.25) to
  **$46.7bn** (mining as other industries).

[CALCULATION: `item.json` arms] One finding for the high end goes beyond the brief. The group's corporate tax sits in
industries with a higher normal-return share than the nation's: 0.293 against 0.250 on Power and Frerick's Table 1,
by industry. At TP-5's level that pattern gives 0.433 for this group, and the high end becomes $42.9bn (beside row).
[CALCULATION: `summary.json` normal_return, beside_normal_return_share_by_industry_tp5] The receipt lane's ceiling
reproduces exactly: −$80.976701bn / −$86.848983bn, every line lost in full at the September 27 employer_hi key.
[DATA: `receipt_side_long_run_2026_09_28/derived/probe.json` item4; gate]

## What this lane measures

The 2026-10-14 assumption review (`research/immigration-v6-assumption-review-2026-10-14.md`, "For the operator" item 2)
found the zero. The case prices corporate tax (`corporate_capital`, `corporate_labor`), business property tax
(`remaining_production_property`) and other taxes on production (`other_production_taxes`) at response 0, and its
production module's capital-tax term is 0 at retention 1. Under full adjustment, the capital that works with the
group is not in the US without it. The taxes collected where that capital sits are lost on removal, and the owners
keep the same after-tax return, so the production terms P and F do not move and nothing offsets the loss. [SOURCE:
the review memo; the team lead's brief] The item is Σ over industry cells of (the group's share of the cell's wage
bill) × (the line's national amount in the cell) × (the line's response at the reading). [INFERENCE: the brief's
formula]

## Results

### The central, by line ($bn; negative = the group's net cost falls)

| line | national | base the key spreads | response, low / high | key share of the national, personal / shared | low, personal | low, shared | high, personal | high, shared |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| corporate tax | 663.685 | 651.508 | 1 / 0.37 | 0.06270 / 0.06921 | −41.61 (SE 1.53) | −45.94 (SE 1.69) | −15.40 (SE 0.57) | −17.00 (SE 0.63) |
| business property tax | 273.445 | 252.374 | 0.8806 / 0.8806 | 0.07347 / 0.07876 | −17.69 (SE 0.48) | −18.97 (SE 0.47) | −17.69 | −18.97 |
| other taxes on production | 145.258 | 90.165 | 1 / 1 | 0.04941 / 0.05297 | −7.18 (SE 0.19) | −7.69 (SE 0.19) | −7.18 | −7.69 |
| **all three** | 1,082.388 | 994.047 | | | **−66.48 (SE 2.01)** | **−72.60 (SE 2.17)** | **−40.27 (SE 1.11)** | **−43.66 (SE 1.16)** |

[CALCULATION: `derived/item.json` lines, se_bn; `derived/items.csv` central]

The SEs come from the 160 CPS replicate weights. The fill-in correction's own uncertainty adds $0.49bn at the low end
and $0.30bn at the high end (personal). [CALCULATION: `item.json` se_bn.fill_in]

The base is the national line less what the key gives no share:
- mining's cells: corporate 12.177, business property 21.072 and other production 28.463 ($bn);
- for other production taxes, also the residential parts of documentary taxes and special assessments (26.629).

[CALCULATION: `item.json` mining.by_line, other_production_line] On its base each line's key is 0.0796 / 0.0853 for
business property and other production, which share one pattern once severance is out, and 0.0639 / 0.0705 for
corporate tax. Against these, the group's plain share of all CPS wages is 0.0788 / 0.0843. [CALCULATION: `summary.json`
keys] So outside mining the group pays about its wage share of property and production taxes. It pays a smaller share
of corporate tax, because it is under-represented in finance, information, chemicals and computers. [CALCULATION:
`wages_by_industry.csv`]

### The three questions on the central (the team lead, 2026-10-14)

**1. Mining at response 0, and whether a reproducible part can be priced.** The union's mining amounts before the
response, personal, are $7.67bn:

| tax component | $bn |
|---|---:|
| corporate | 1.52 |
| business property | 2.63 |
| severance | 2.59 |
| licenses and other | 0.84 |
| documentary taxes | 0.06 |
| special assessments | 0.04 |

At the line responses this would be $7.36bn low / $6.40bn high. [CALCULATION: `summary.json`
mining.union_target_bn, added_by_the_arm_bn] The national amounts by cell ($bn) are below. [DATA: `summary.json`
mining.national_bn]

| cell | corporate | property | severance | licenses and other | documentary | special assessments |
|---|---:|---:|---:|---:|---:|---:|
| 211 oil and gas | 9.12 | 17.47 | 16.58 | 5.58 | 0.39 | 0.28 |
| 212 other mining | 2.19 | 2.12 | 4.02 | 0.68 | 0.05 | 0.03 |
| 213 support | 0.86 | 1.48 | 0.34 | 0.47 | 0.03 | 0.02 |

The union's share is pooled at 0.1236 in 211 and 212 and is its own 0.1379 in 213 (personal). [DATA:
`summary.json` mining.union_share]

The data can split mining's corporate base. Power and Frerick's Table 1 puts mining's normal-return share at 0.44 and
petroleum and coal products' ("Fossil Fuel") at 0.06. [SOURCE: Treasury OTA Working Paper 111, Table 1, p. 16] The
business property key is the T00OTOP tax-payment pattern (`national.py:651`), which includes mineral-property taxes, so
it is not reproducible capital by construction (corrected 2026-10-14 after the parent's review; the Fixed Assets
stocks are separate beside rows). No table splits the property tax between mineral reserves and reproducible capital.
[DATA: `national.py` pattern; INFERENCE] A reading that lets mining's corporate base respond at its normal share and
its property tax respond like other industries' is $3.92bn (beside, personal); its property part, about $2.31bn, is
not identified as reproducible-property tax. In it:
- corporate responds at 0.44;
- business property responds at 0.8806;
- severance responds at 0;
- the other components respond at 1.

[CALCULATION: `summary.json` mining.reproducible_only_bn]

I do not recommend that reading. With world prices fixed and capital mobile at the world return, the mobile-capital
sectors pin the wage. A sector whose fixed factor is a resource then keeps its own employment, capital and output when
the labour endowment falls, and the group's mining jobs are refilled. [INFERENCE: the specific-factors logic of the
case's own premise] By that argument the wells stay with the reserve. Mining at 0 on every line is the reading the
data support. The same argument covers agriculture: its land is fixed and its crops are world-priced. Agriculture at
0 too gives $63.97bn / $38.01bn, a change of $2.51bn / $2.25bn (beside row; not adopted, your call). [CALCULATION:
`items.csv` beside_agriculture_0]

**2. Corporate tax by reading.** The response is {low: 1, high: 0.37}, item totals as in the verdict.
[CALCULATION: `item.json` lines.corporate.response, central_bn]
- **0.37:** TP-5, p. 7: "we find that 63 percent of current corporate taxable income is due to supernormal returns",
  and "the remaining 37 percent of the corporate tax on the taxable income attributable to normal returns". [SOURCE:
  Cronin, Lin, Power and Cooper, OTA Technical Paper 5, May 2012, p. 7] OTA's July 2021 methodology still splits the
  tax "between capital income (81.5 percent) and labor income (18.5 percent)", which is half of 37 (gate). [SOURCE:
  Treasury OTA, "Treasury's Distribution Methodology and Results", p. 3 note 4] Arm `normal_return_share` puts
  corporate tax at 0.37 at both ends: −$40.27bn / −$43.66bn at each. [CALCULATION: `item.json`
  arms.normal_return_share]
- **The 0.25 arm (`normal_return_share_0_25`), primary:** Power and Frerick apply TP-5's method to SOI's C-corporation
  files for 1992–2013. Their abstract finds the risk-free share "averaging 40 percent from 1992–2002 and 25 percent from
  2003–2013". The high end is then $35.27bn / $38.14bn. [SOURCE: Power and Frerick, "Have Excess Returns To
  Corporations Been Increasing Over Time?", Treasury OTA Working Paper 111, November 2016, p. 2 (the working paper of
  National Tax Journal 69(4), 2016), pinned; CALCULATION: `item.json` arms.normal_return_share_0_25] The 0.25 is the
  2003–2013 average, not one year's figure.
  The paper prints years only in a chart. The same paper notes that falling interest rates explain about half of the
  decline in its present-value estimate. [SOURCE: same, p. 11] 2024's rates are higher than 2013's. [INFERENCE]
- **By industry (new):** Table 1 (2011–2013) gives mining 0.44, utilities 0.85, construction 0.71, metal and machinery
  0.45, trade 0.40, transportation 0.25, technology 0.16, service 0.16, nondurables 0.15, chemicals 0.10, information
  0.08, fossil fuel 0.06. [SOURCE: same, Table 1, p. 16] On the cells' corporate tax:
  - the nation's weighted share is 0.250 (the gate checks it against the 2003–2013 average);
  - the union's is 0.293 (G1 0.311, G2 0.292, G3+ 0.276; third-plus whites 0.258).

  [CALCULATION: `summary.json` normal_return] The arm at Table 1's levels (`normal_return_share_by_industry`) gives
  $37.04bn at the high end. Scaled to TP-5's level (the union at 0.433) it gives $42.90bn / $46.38bn (beside).
  [CALCULATION: `item.json` arms.normal_return_share_by_industry; `items.csv`
  beside_normal_return_share_by_industry_tp5] The cell-to-industry map is mine. Agriculture, finance and real estate
  take the 0.25 average. [INFERENCE: `national.py` PF_INDUSTRY]
- **What "supernormal" includes.** TP-5's measured supernormal share is the whole base above the risk-free return:
  the part an expensing tax would still collect. For incidence it then "assume[s] the source of the supernormal return
  is pure rent, not risk". [SOURCE: TP-5 p. 7] Power and Frerick, using the same method, count as excess "returns to
  risk, entrepreneurial labor, decreasing returns to scale, market power, luck, etc.". Most self-created intangibles
  are already expensed, so their returns sit in the excess part. [SOURCE: Power and Frerick pp. 4 and 21] Returns to
  risk and to expensed intangibles scale with the capital under full adjustment, so the 0.37 reading is a floor for the
  corporate part, not a central. [INFERENCE]
- **Fox (2020), beside, no arm:** "the actual tax raised only slightly more than the hypothetical cash flow tax over
  the most recent period from 1995–2013. The difference was about 4 percent on average"; more conservative
  assumptions "yield 21 percent". Under Treasury's rule that is labour 2–10%, a normal share of 0.04–0.21. [SOURCE:
  Fox, Journal of Empirical Legal Studies 17(1), 2020, p. 72 and note 5, doi 10.1111/jels.12243; INFERENCE: 0.5 × 4–21%]
- **Rents tied to domestic sales: [NOT FOUND].** No economic split of US corporate rents into domestic-sales and other
  rents turned up. The search covered the destination-based cash-flow tax papers (Auerbach, Devereux, Keen and Vella
  2017; Auerbach and Devereux), Clausing, the Tax Policy Center, the Tax Foundation and CRS R44823; JCT and CBO were not
  reached. [SOURCE: scratch research note] The nearest administrative proxy is IRS Form 8993. Foreign-derived
  intangible income is 19.7% of deemed intangible income in 2018 (143.3 of 725.9 $bn) and 18.0% in 2021 (301.3 of
  1,672.7). So about 80% of that statutory excess return, for filers only, is earned on sales for US use. [SOURCE: IRS
  SOI 18it01fdii.xlsx and 21it01sec250.xlsx, Table 1; CALCULATION] Rents earned from US customers shrink with the US
  market, which the group's removal shrinks too. That is another reason the high end is a floor. [INFERENCE]

**3. The other-production base and the whole line's key.** The case's line is 145.258 ($bn): federal other 1.580,
severance 20.935, documentary and stamp 21.468, special assessments 15.556, motor vehicle licenses 15.010, other
licenses 57.527, state and local other 13.182. [SOURCE: BEA NIPA 3.5 via `national.json`
other_production_components_bn] The old 118.629 base left out 26.629: the residential 71.92% (Z.1 market value) of
documentary taxes (15.441) and of special assessments (11.189). Mining now leaves out 28.463 more, so the base is
90.165. [CALCULATION: `national.json` residential_split; `item.json` other_production_line]

The whole-line key is the union's tax on that base over the whole line: 0.04941 personal. The residential parts and
mining's cells get no group share, which leaves them at zero, as v6 does. [CALCULATION: `item.json`
lines.other_production_taxes]

The 0.0912 was business property's key share in my first build (0.091258 on 273.445), never other production's. In
the 15:50 build other production's key was 0.0737 of the whole line. It falls to 0.0494 now because mining's 28.463
leaves. [DATA: the 14:10 build's items.csv in this session's record; `item.json`]

The residential parts go to the follow-up critique, not v7 (the team lead, 2026-10-14); see open problems.

### Arms (each one change from the central; personal / shared, $bn)

| arm | low end | high end | what changes |
|---|---:|---:|---|
| central | −66.48 / −72.60 | −40.27 / −43.66 | |
| mining as other industries | −73.84 / −80.32 | −46.67 / −50.37 | mining's cells at the line responses (the 15:50 build) |
| `normal_return_share`: corporate at 0.37 at both ends | −40.27 / −43.66 | −40.27 / −43.66 | low end too |
| `normal_return_share_0_25`: high at 0.25 (Power and Frerick 2003–2013) | −66.48 / −72.60 | −35.27 / −38.14 | high end only |
| `normal_return_share_by_industry`: high by industry (Table 1 levels) | −66.48 / −72.60 | −37.04 / −40.10 | union's effective share 0.2926, one response |
| plain wage share in place of the industry key | −75.95 / −81.29 | −43.61 / −46.68 | each group's share of all CPS wages over the base |
| federal tax on foreign-source income removed | −63.05 / −68.70 | −39.00 / −42.21 | corporate base less $78.48bn (mining's part out) |
| business land at response 0 | −64.98 / −70.99 | −38.76 / −42.05 | property response 0.8059 |
| business land at response 1 | −68.88 / −75.17 | −42.66 / −46.23 | property response 1 |
| the case's wage key (status rules on) | −63.17 / −69.23 | −38.21 / −41.59 | each generation's targets × its case share over its lane share |
| floor: CBO's labour share of corporate tax only | −12.47 / −13.37 | −12.47 / −13.37 | corporate_labor at the case's wage key; the other lines at 0 |
| ceiling, receipt lane (Sept 27 employer_hi, all at 1) | −80.98 / −86.85 | | the gate |
| ceiling on the case's September 29 frame | −81.32 / −87.22 | | −plain_wage_share × 1,082.388 |

[CALCULATION: `derived/item.json` arms (net_cost_change_bn); `items.csv` arm_* and item_arm_* rows; the last row is
−0.075134336 × 1,082.388297 and −0.080580472 × 1,082.388297 from `case_keys.json` case_wage_key] The shared value of
the by-industry arm in `item.json` (−40.10) uses the union's personal effective share. The exact shared value is
−39.98 (items.csv; gated within $0.25bn). [CALCULATION]

### The wage concepts

| key | personal | shared | over the case's wage key |
|---|---:|---:|---:|
| this lane's plain share: CPS WSAL_VAL, all wages, row 4 and the fill-in | 0.078791 | 0.084335 | 1.04867 / 1.04659 |
| the case's wage key (corporate_labor at cbo_collective, September 29 payload): `plain_wage_share` in item.json | 0.075134 | 0.080580 | 1 |
| the September 28 union key you quoted | 0.075063 | 0.080511 | (this lane's over it: 1.04968 / 1.04750) |
| the probe's employer_hi share (September 27) | 0.074813 | 0.080238 | |

[DATA: `summary.json` keys; `case_keys.json` case_wage_key; the team lead's message, 2026-10-14; CALCULATION] Both
this lane's share and the case's key use wage and salary income (WSAL_VAL, the employer_hi key's concept). The case's
key also applies the status rules, which keep 0.526 of the imputed unauthorized's wages at the on-books lane's
shares. Most of the 4.9% gap is those rules. [SOURCE: `cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`;
INFERENCE] `per_wage_dollar` is per dollar of this lane's concept. The case's lineage pricing should use the factors,
which are ratios within one concept.

### Generations, whites and Blacks (personal)

| group | wages, $bn | item, low / high, $bn | tax per wage dollar, low / high | per person, low / high, $ |
|---|---:|---:|---:|---:|
| union | 942.6 | −66.48 / −40.27 | 0.0705 / 0.0427 | 1,674 / 1,014 |
| G1 (Mexico-born) | 291.5 | −21.81 / −13.49 | 0.0748 / 0.0463 | 1,976 / 1,222 |
| G2 | 330.9 | −22.48 / −13.47 | 0.0679 / 0.0407 | 1,569 / 940 |
| G3+ | 320.2 | −22.19 / −13.31 | 0.0693 / 0.0416 | 1,547 / 928 |
| third-plus non-Hispanic whites | 6,704.1 | −559.2 / −320.6 | 0.0834 / 0.0478 | 3,231 / 1,853 |
| third-plus non-Hispanic Blacks | 845.3 | −56.14 / −33.31 | 0.0664 / 0.0394 | 1,721 / 1,021 |
| nation (civilian) | 11,962.9 | | 0.0806 / 0.0463 | |

[CALCULATION: `summary.json` generations; `item.json` per_wage_dollar] Shared: G1 −$18.12bn / −$11.18bn, G2 −$24.68bn /
−$14.78bn, G3+ −$29.79bn / −$17.70bn. [CALCULATION: same]

The targets before the response, by line and generation, are in `item.json` by_generation. Each factor is a group's
key share over its share of the case's wage key (union, generations) or over its plain share (whites, Blacks). By line
(corporate / other production / property, personal):

| group | corporate | other production | property |
|---|---:|---:|---:|
| union | 0.8345 | 0.6576 | 0.9778 |
| G3+ | 0.7819 | 0.5919 | 0.8801 |
| third-plus whites | 1.0181 | 0.6399 | 0.9515 |

[CALCULATION: `item.json` factor] The other-production factors carry the base's 0.6207 of the line (90.165 / 145.258),
because the key spreads only the base. For the lineage this is the right object: the added people get no share of
mining or the residential parts either. [CALCULATION; INFERENCE]

**The lineage's 3.04M added people** [INFERENCE]: priced as identified G3+ members and as third-plus whites at the
G3+'s ages, they add −$5.63bn / −$3.31bn personal (low / high). Union plus lineage is then −$72.11bn / −$43.58bn
(shared −$80.17bn / −$48.09bn). [CALCULATION: `summary.json` lineage_inference] This is a check, not the v7 figure;
the v7 lane prices them from the case's own lineage cells times the G3plus and white_nh factors.

### Where the item comes from (personal, $bn)

| sector | low end | high end |
|---|---:|---:|
| durable manufacturing | −9.69 | −4.77 |
| nondurable manufacturing | −8.67 | −4.37 |
| retail | −7.47 | −4.30 |
| wholesale | −6.65 | −3.21 |
| finance | −5.18 | −2.62 |
| information | −3.99 | −1.83 |
| construction | −3.80 | −2.32 |
| utilities | −2.95 | −2.73 |
| accommodation and food | −2.89 | −2.07 |
| transportation | −2.54 | −1.86 |
| agriculture | −2.51 | −2.25 |
| health | −2.37 | −1.90 |
| professional | −2.01 | −1.28 |
| administrative | −1.92 | −1.28 |
| the rest | −3.83 | −3.47 |
| mining | 0 | 0 |

[CALCULATION: `summary.json` central_by_sector_bn]

### Beside rows (low / high end; personal, then shared; $bn)

| row | personal | shared |
|---|---:|---:|
| corporate high by industry at TP-5's level (0.433 for the union) | −66.48 / −42.90 | −72.60 / −46.38 |
| agriculture also at 0 | −63.97 / −38.01 | −69.98 / −41.31 |
| mining as other industries, its cells at the plain wage share | −71.15 / −44.33 | −77.59 / −48.00 |
| mining as other industries but severance at 0 (the reserve stays) | −71.25 / −44.08 | −77.60 / −47.66 |
| wages at $1M or more in their own records' industries | −65.65 / −39.81 | −71.73 / −43.19 |
| wage records at $1M or more out of both sides | −67.54 / −41.01 | −73.89 / −44.54 |
| no thin-cell pooling | −66.42 / −39.86 | −72.49 / −43.18 |
| thin cells pooled below 300 earners | −67.60 / −40.70 | −73.83 / −44.18 |
| earnings (wages plus self-employment and farm income) | −65.79 / −39.70 | −71.85 / −43.07 |
| business property by private nonresidential structures | −66.55 / −40.33 | −72.50 / −43.56 |
| structures, and equipment at τ | −66.77 / −40.56 | −72.76 / −43.82 |
| business property at BEA's housing split ($396.137bn) | −74.42 / −48.20 | −81.11 / −52.17 |
| r_b on the whole property line (no TPP split) | −66.13 / −39.92 | −72.23 / −43.28 |
| δ_L by the group's owner tax | −66.51 / −40.29 | −72.63 / −43.69 |
| δ_L by the national-share fall | −65.58 / −39.36 | −71.63 / −42.69 |
| management of companies kept at NAICS 55 | −67.06 / −40.48 | −73.14 / −43.86 |
| lessors' taxes kept with the lessors | −66.63 / −40.39 | −72.64 / −43.69 |
| the for-profit key (nonprofit jobs out) | −67.24 / −40.91 | −73.40 / −44.36 |
| published CPS weights (40.90M) | −68.67 / −41.62 | −74.30 / −44.71 |
| no fill-in correction | −68.01 / −41.21 | −73.82 / −44.41 |
| fill-in at one rate for every generation | −66.59 / −40.35 | −72.67 / −43.72 |

[CALCULATION: `derived/items.csv` beside_* rows; `summary.json` beside_bn] Mining's own reproducible-only reading,
−$3.92bn on top of the central at both ends, is under question 1.

## Method

### National tax by line and industry

The lines are the case's 2024 lines (`assumption_explorer_2026_09_21/derived/model.json`): business property
273.445297bn (remaining_production_property less the BEA tenant split, as the receipt lane takes it), other
production taxes 145.258bn, corporate 663.685bn (corporate_capital + corporate_labor). Every line's cells add to the
model's line (gate, 1e-6). [DATA: `case_keys.json` national_bn; `national.json`] Cells are the 2024 supply-use
summary industries. Housing (HS) is out, 525 is merged into 523, and there are federal and state-local government
cells, a household cell (zero) and a RESIDENTIAL cell outside the item. [DATA: `derived/national_by_industry.csv`]

- **Corporate:** BEA NIPA Table 6.18D, Section 6 workbook, published 2026-09-30. The 2024 sectors are spread by
  their 2023 detail, because 2024 has no detail. Retail and hospitals/nursing are split by 2024 SUT gross operating
  surplus. 6.18D's 2024 total of $660.908bn sets the pattern; the model's $663.685bn sets the level (factor
  1.0042). Management of companies (6.18D: "bank and other holding companies") goes pro rata to the other private
  cells. Lessors' taxes (real estate ORE, rental and leasing 532RL) go to the industries using their capital, in
  proportion to intermediate purchases. Self-use is netted and the two lessors' cross purchases are solved; the
  final-demand part stays (ORE keeps 12.2%, 532RL 34.8%). [SOURCE: BEA NIPA 6.18D; BEA 2024 summary use table;
  CALCULATION: `national.py`]
- **Business property:** the 2024 summary use table's other taxes on production (T00OTOP) by industry, housing
  out, is the central pattern. It is BEA's own estimate of what each industry pays, so it carries exemptions,
  tangible personal property and mineral property. The OTOP-to-structures ratio varies widely across industries.
  Beside rows use Fixed Assets Table 3.1S private nonresidential structures (2024, current cost; nonprofit
  structures of $2.98tn removed by the CPS nonprofit wage share). A variant adds equipment at τ.
  **Equipment rule:** equipment enters only through tangible personal property, the τ share of the line (below).
  [SOURCE: BEA SUT 2024; BEA Fixed Assets 3.1S; CALCULATION: `national.py`]
- **Other taxes on production:** NIPA Table 3.5 components sum to the line (question 3). Licenses and the rest follow
  the T00OTOP pattern. Severance follows the mining industries' taxes on products (oil and gas 16.58, other mining
  4.02, support 0.34). Documentary taxes and special assessments split by Z.1 market value: residential 71.9%
  (owner-occupied plus noncorporate residential real estate) against nonfinancial corporate and noncorporate
  nonresidential real estate. The residential $26.63bn goes outside the item. [SOURCE: BEA NIPA 3.5; Federal Reserve
  Z.1, 2026-09-11 release; CALCULATION: `national.py`]
- **No housing in the lines:** the case's owner line ($394.862bn) and tenant split ($83.840bn) already exceed BEA's
  housing property taxes ($356.011bn), so no business cell holds housing tax. On BEA's housing split, business
  property would be $396.137bn (beside row). [DATA: model.json; receipt lane housing.json; CALCULATION:
  `national.json`]
- **Mining:** its three cells stay in the national tables and leave the item's vectors (`responds` 0 in
  `wages_by_industry.csv`).

**Year mismatches.** 6.18D detail is 2023 inside 2024 sectors. SOI's foreign-source tax and the Tax Foundation's
personal-property share are tax year 2021. Power and Frerick's industry shares are 2011–2013. Z.1 and Fixed Assets are
2024 year-end; CPS income is 2024. [DATA: `inputs/pins.json`]

### The group's share of each industry's wages

CPS ASEC 2025 person file, income year 2024, on the receipts builder's frame: civilian household persons; the union
of the Mexico-born, the second generation and self-identified Mexican-origin third-plus; WSAL_VAL clipped at 0; the
longest job's industry (`inputs/census_industry_crosswalk.csv`, 305 codes, with each code's CPS earners and wages in
`derived/industry_crosswalk.csv`); government workers by class of worker. [DATA: `full_account_receipts_2026_09_20/
builder.py`; CALCULATION: `job_capital.py`] On published weights the frame reproduces the builder's wage key to 1e-9:
personal 0.083234408 (SE 0.001400974), shared 0.087823776. [DATA: `allocation_keys.csv`; gate] Row 4 rakes the
Mexico-born outside California and Texas to ACS 2024 by citizenship in all 161 weight columns. Its factors and
replicate ranges match `production_row4.json` to 1e-12, the union is 39,712,493 and G3+ is the case's identified
14,342,575. [DATA: `production_row4.json`; v6 corrections.json; gates] The case's fill-in correction (two methods'
mean wage rel_change, −2.084% personal, −1.562% shared) moves the union's wages, split across generations as the case
splits the same methods' change on the wage key (`generation_account_2026_09_24/derived/stack_by_generation.json`,
components D, convention a). G1 takes 116% of the personal change and G2 −31%, so the factors are G1 0.9262, G2
1.0190, G3+ 0.9907. [CALCULATION: `summary.json` meta.fill_in] Whites and Blacks are uncorrected.

Two small-sample rules:

- **Wages at or above $1M are spread as the nation's are.** The public file caps each earnings source at
  $1,099,999: 175 civilian records sit at the cap and 233 are at or above $1M, 5.2% of the wage bill. The union
  holds 15 of them and 4.6% of their wages. [CALCULATION: scratch tabulation of pppub25.csv; `summary.json`
  pooling.top_wages] Each group's such wages are spread over the cells as the nation's are, so group totals are
  unchanged (gate, 1e-12). The reason was mining. Its 359 CPS earners include three at the cap, all union members
  (US-born, ages 35–48), carrying 9.7% of the sector's wages. With them the union holds 21.8% of mining wages
  against 15.0% of mining earners; without them it holds 13.4%. [CALCULATION: `summary.json` top_wages_by_sector]
  In every other sector that carries these taxes, the union's wage share is below its earner share. Private
  households are the one other exception, and they carry none of these taxes. [CALCULATION: same] BLS's 2024 annual
  average puts Hispanic workers at 22.7% of mining employment, and the ASEC gives 23.5%. [SOURCE: BLS CPS Table 18,
  2024 annual averages, https://www.bls.gov/cps/cpsaat18.htm, read from the Wayback capture of 2025-12-31;
  CALCULATION: scratch tabulation on published weights] That check confirms the sample's headcount, not the three
  records' wages; the spreading is a small-cell rule, not a validated correction (parent's review, 2026-10-14). With
  mining at 0 the rule matters less. Taking the top wages
  in their own industries now gives −$65.65bn at the low end against −$66.48bn. [CALCULATION: items.csv]
- **A cell with fewer than 100 CPS wage earners takes its sector's pooled share** (a one-cell sector takes every
  private cell's). The pooled cells are 113FF, 211 (38 earners), 212, 313TT, 315AL, 324, 483, 486 and 55. Without
  pooling the low end is −$66.42bn. [CALCULATION: `summary.json` pooling; items.csv]

The status rules of the case's wage key are not applied: the team lead kept all CPS wages central (2026-10-14), with
`case_wage_key` an arm. Those rules keep only the on-books lane's share of the imputed unauthorized's wages: 0.526
central for the Mexico-born. [SOURCE: `cps_imputation_keys_2026_09_23/combine_onbooks_lane.py`] The case uses them
because payroll taxes, and CBO's distribution of the labour share of corporate tax, follow reported wages. Capital
taxes are different. The structures, licences and profits behind an off-books job are taxed where they sit whether
or not the wage is reported. The case's production term also counts all CPS earnings
(`main_case_candidate_2026_09_28/production_row4.py` uses PEARNVAL). [INFERENCE; DATA: production_row4.py]

Within-industry informality is not measured. Off-books jobs sit in smaller, less capital-intensive and less
compliant firms than their industry's average. The industry key gives them the average firm's capital, which pushes
the true item toward the `case_wage_key` arm. [INFERENCE]

### Responses

- **Corporate:** 1 at the low end and 0.37 at the high end (question 2). [SOURCE: TP-5 p. 7; gate on OTA 2021]
- **Other production taxes:** 1 at both ends (the brief). Mining, at 0, is set inside the key.
- **Business property:** responds at **r = τ + (1 − τ) r_b = 0.8806** at both ends, with r_b = 1 − λ_b(1 − δ_L) =
  0.8634 on the real property. [CALCULATION: `summary.json` parameters]
  - **τ = 0.1265** is the tangible personal property share of the line, and it leaves whole (equipment has no land).
    It is the Tax Foundation's national estimate, "about 4.6 percent" of property taxes once car taxes are
    excluded, times $752.148bn of property taxes over the $273.445bn line. [SOURCE: Tax Foundation, Hulehan,
    "Personal Property Tax Exemptions for Small Businesses", 2023-12-07, tax year 2021; CALCULATION: `national.json`
    tpp] With the brief's r_b on the whole line, the low end is −$66.13bn (beside row).
  - **λ_b = 0.2222** is the land share of business real estate, 2024 year-end: 1 − (FA 4.1 line 39 nonfinancial
    corporate structures 13,818,860 + FA 5.1 line 3 corporate residential 369,614 + Z.1 FL115013665 noncorporate
    nonresidential structures 3,187,906) / (Z.1 LM105035005 nonfinancial corporate real estate 15,644,373 +
    LM115035035 noncorporate nonresidential real estate 6,696,508), $mn. Corporate alone is 0.093 and noncorporate
    0.524. [SOURCE: Federal Reserve Z.1; BEA Fixed Assets; CALCULATION: `national.json` land]
  - **δ_L = 0.3851** is the long-run land-price fall where the group lives: the receipt lane's county
    `fall_lr_metro / land_share`, weighted by the group's population as the place of its jobs. Weighting by the
    group's owner tax gives 0.3923; the national-share fall gives 0.1529. [DATA:
    `receipt_side_long_run_2026_09_28/derived/counties.csv`; CALCULATION: `summary.json`]

### Arms' sources

- **Foreign-source income:** IRS SOI Corporate Foreign Tax Credit, tax year 2021, Table 1 column 19, all
  industries $59.28bn. This is the file's footnote-2 measure of US tax on foreign-source income, and it equals
  column 18 less column 2 within 0.01%. Over Publication 5655's $371.4bn total income tax after credits it is
  0.1596. Applied to the federal $491.66bn by SOI industry rows, it removes $78.48bn. [SOURCE: IRS SOI;
  CALCULATION: `national.json` foreign]
- **Normal return:** TP-5, OTA 2021 and Power and Frerick as under question 2; all three are pinned and parsed, never
  typed. [DATA: `inputs/pins.json`; `national.json` normal_return]

## Gates (all passed)

- `case_keys.cjs` passes 16 gates:
  - the ceiling −86.848983 / −80.976702 and its employer_hi shares round to probe.json's;
  - the floor is trace.csv's;
  - the v6 nationals match and the three lines respond 0 at 48, 11 and 16;
  - the case's wage key and its owner and tenant property keys are keyed as named, their generations add up (1e-12),
    and set and cash agree;
  - v6 sets a response for the owner and tenant lines.
- `national.py` passes 76 gates: pins, labels, NIPA components, 6.18D sums, the SUT, SOI columns, the TP-5, OTA 2021
  and Power and Frerick statements and Table 1 (its income shares add to 1.01 and their weighted risk-free share is
  0.2463 against the 2003–2013 average of 0.25), cells adding to lines, no housing in the cells, no negative cell.
- `job_capital.py` passes 70 gates:
  - the builder key reproduces (1e-9), row 4 holds (1e-12, 39,712,493) and every wage-bearing code maps;
  - spreading the top keeps totals, and the generations add up;
  - the fill-in splits to 1e-9 and the corrected generations add to rc to 1e-12;
  - the high end's 0.37 is twice OTA's 18.5;
  - mining's cells carry no tax in the item, and its components add to what the arm adds (1e-9);
  - the plain-wage-share ceiling reproduces −86.848983 / −80.976701 to 1e-6;
  - sectors add to the central and per-person items add to the union, at both readings;
  - for every item-file block, group_bn = key_share × national, generations add, factor.union =
    key_share / plain_wage_share (1e-9), plain_wage_share is the case's, and the central and six arms are
    items.csv's at both readings (1e-9).
- `test_gates.py` passes 15 tests.

[DATA: each `derived/*.json` gates list]

## For the v7 lane (main_case_2026_10_14)

- **`derived/item.json` follows the contract** in `item_job_capital.cjs`, as it read on 2026-10-14. [DATA: that file]
  - Every line's `response` is {low, high}: corporate {1, 0.37}, business property {0.8806, 0.8806}, other
    production {1, 1}.
  - `group_bn` = key_share × national_bn, before the response, which is the reader's gate. `item_bn`
    {low, high} × {personal, shared} is after it.
  - `central_bn` and `net_cost_change_bn` are {low, high} × {personal, shared}, in the central and in every arm. The
    reader already reads them by reading (`pairByReading`) and gates them against Σ response × group_bn.
  - Every arm writes each line's response at both readings; nothing is inherited from the central.
  - `per_wage_dollar` is {low, high} → group → line → allocation, plus `all`.
  - `gates` are {name, passed, value}.
- **Mining is inside the key.** Its cells have no tax, so key_share, by_generation and factor exclude it. The lineage
  route (wage share × factor × national) excludes it for the added people too. [CALCULATION; INFERENCE]
- **Arms (ten):** mining_as_other_industries, normal_return_share (0.37 at both ends), normal_return_share_0_25,
  normal_return_share_by_industry, plain_wage_share, foreign_source_removed, business_land_at_0, business_land_at_1,
  floor, case_wage_key.
- **Recommended for the team lead's decision:**
  - the high end at the group's industry mix (0.433, −$42.90bn) in place of the national 0.37 (−$40.27bn);
  - agriculture at 0 like mining (+$2.5bn).
- **The production capital-tax term must stay 0** (retention 1), so nothing counts twice: P and F do not move.
- **Out of scope:** business current transfers ($139.976bn) keep the case's treatment. [DATA: model.json]

## Caveats and open problems

- **Small cells.** Mining no longer drives the central. Its pooled share (0.124, SE 0.034) matters only for the arm.
  [CALCULATION: wages_by_industry.csv] A pooled multi-year ASEC or the ACS would firm up the thin cells. The local ACS
  extract lacks industry, so this lane did not use it. [DATA: register]
- **The corporate part is likely overstated at the low end.** Within industries the union works more in small firms:
  36.8% of its wages are at employers under 100 against 30.2% nationally, and 43.5% against 51.3% at employers of
  1,000 or more. Small firms are less often C corporations. [CALCULATION: `summary.json` firm_size_wage_shares;
  INFERENCE] Within-industry informality points the same way (above).
  [2026-10-14 correction, v7 assumption review round 1 (finding A19): these shares pool industries
  (`job_capital.py` 663–669), so "within industries" overstated them. On private BEA cells, the union's
  under-100 share is 41.5% against 34.0% nationally; of that 7.5-point gap, 2.6 points are within cells and
  4.9 come from the industry mix. At 1,000 or more the gap is −8.7 points, −3.8 within cells. The sign
  holds; the within-industry part is about a third. CALCULATION: `job_capital_key_refine_2026_10_14/derived/within_firm.json`]
- **The corporate part is likely understated at the high end.** "Supernormal" includes returns to risk and to
  expensed intangibles, and rents from US customers, all of which scale with the group's capital or market. The
  group's industry mix also has a higher normal share (question 2). [INFERENCE]
- **Residential documentary taxes and special assessments ($26.63bn)** sit in other_production_taxes at zero group
  share, as in v6. They go to the follow-up critique, not v7 (the team lead, 2026-10-14). A first pricing already
  falls out of the run: $1.46bn at the case's owner and tenant property keys and responses
  (`summary.json` residential_parts). The open check is whether the model's owner line, $122.7bn above BEA's housing
  property taxes, already holds special assessments. [CALCULATION; INFERENCE]
- **Classification.** 6.18D classifies companies and the CPS classifies establishments. Temp-agency workers (561)
  use their clients' capital but sit in 561, which understates the item. Farmland's land share is above λ_b, so
  agriculture's property response is overstated, by about $0.5bn. [INFERENCE]
- **Self-employment.** The key uses wages; adding self-employment and farm income gives −$65.79bn at the low end.
  [CALCULATION]
- **A measurement conflict for the case.** The model's owner line plus the tenant split exceed BEA's housing
  property taxes by $122.7bn. If BEA is right, business property is $396bn and the low end −$74.42bn. [CALCULATION]
- **The instrument.** This research runs through an LLM with known dispositions on immigration
  (`notes/llm-bias-caveat.md`). The two choices that lowered the central most came from the team lead's review: mining
  at 0 and the high end's 0.37. The lane priced both and kept the alternatives as arms. The one evidence-led change
  beyond the brief raises the high end (the industry mix). [INFERENCE]

## Files

- `acquire.py`, `inputs/pins.json`: 12 pinned sources in `_cache/` (ignored), Treasury OTA Working Paper 111 added
  on 2026-10-14.
- `inputs/census_industry_crosswalk.csv`: CPS industry codes mapped to BEA cells.
- `case_keys.cjs` → `derived/case_keys.json`.
- `national.py` → `derived/national_by_industry.csv` (with each cell's Power and Frerick industry and share),
  `derived/national.json`.
- `job_capital.py` → `derived/wages_by_industry.csv` (per cell: shares, national taxes, `responds`, the union's item
  at each end), `derived/industry_crosswalk.csv`, `derived/items.csv`, `derived/summary.json`, `derived/item.json`.
- `test_gates.py`.

## Reproduce

```sh
uv run --no-project python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/acquire.py --check
node infra/immigration-fiscal/job_capital_taxes_2026_10_14/case_keys.cjs
OPENBLAS_NUM_THREADS=1 uv run --no-project --with openpyxl python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/national.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/job_capital_taxes_2026_10_14/job_capital.py
uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/job_capital_taxes_2026_10_14/test_gates.py -q
```

## Log (append-only; times from `date`)

- 2026-10-14 14:10 JST: lane started from the team lead's brief (2026-10-14; review item 2 of
  `research/immigration-v6-assumption-review-2026-10-14.md`). Inputs fetched and pinned by `acquire.py`
  (`inputs/pins.json`, 10 files): BEA NIPA Section 6 (published 2026-09-30), BEA Fixed Assets Sections 3–5, BEA
  supply-use tables (2024 summary use table), Federal Reserve Z.1 of 2026-09-11, IRS SOI Corporate Foreign Tax
  Credit TY2021, IRS Publication 5655 (TY2021), the Census 2022 industry code list and Treasury OTA's 2021
  methodology summary. `inputs/census_industry_crosswalk.csv` maps every CPS ASEC 2025 industry code (2017 and
  2022 lists) to BEA's summary industries; the 34 codes the 2017 list lacks came from the Census 2022 list.
- 2026-10-14 15:02 JST (the transcript's recorded time of the tool result): first full build, the Tax Foundation
  page added as the 11th pin; rerun IDENTICAL 14/14. Central then −$78.35bn personal, with the fill-in at one rate
  and top wages in their own industries.
- 2026-10-14 15:33 JST: `derived/item.json` written to main_case_2026_10_14's contract, read from the v7 brief and
  stub; the contract had not arrived by message. Fill-in split by generation as the case splits it; black_nh and
  the every-nativity groups added; `case_keys.cjs` reads the case's wage key on the September 29 payload. The
  consumer's readers and plain-share gate pass on a scratch copy. Told the team lead about the status-rules choice.
- 2026-10-14 15:47 JST: mining's three capped union records found (BLS Table 18 confirms the sample's headcount);
  wages at or above $1M now spread as the nation's are. Central −$73.84bn / −$80.32bn; the old reading stays as a
  beside row. RESULT written.
- 2026-10-14 15:50 JST: `scripts/rerun_lane.py` with the five commands under Reproduce: IDENTICAL 15/15, exit 0.
  Four beside-row roundings and the sector remainder in this file were then corrected against the outputs (no
  output changed).
- 2026-10-14 15:55 JST: the team lead's six messages arrived together after the 15:50 report: the item contract,
  its addendum, three questions on the central, the normal-return arm and the wage-key decision (all CPS wages
  stay central, `case_wage_key` an arm). Verdict set to PROBE IN PROGRESS while the central is rebuilt. The
  superseded central was −$73.84bn personal / −$80.32bn shared: all three lines, corporate at 1, mining at the
  central responses.
- 2026-10-14 16:40 JST: rebuilt to those asks.
  - Changes: mining at 0 at both readings; corporate {low 1, high 0.37}; every line's response {low, high}; arms at
    0.25 and by industry.
  - New inputs: Treasury OTA Working Paper 111 pinned (the primary Power and Frerick; the TP-5 source page corrected
    to p. 7); the case's owner and tenant property keys added to `case_keys.cjs` for the residential parts.
  - New outputs: `derived/industry_crosswalk.csv` and per-cell items in `wages_by_industry.csv`.
  - Literature: a researcher subagent read Fox (2020) and searched the domestic-sales split. I checked its Fox quote
    (p. 72) and the IRS Form 8993 cells myself.
  - Central: −$66.48bn low / −$40.27bn high (personal), −$72.60bn / −$43.66bn shared. 76 + 16 + 69 gates and 15
    tests pass.
- 2026-10-14 16:46 JST: `scripts/rerun_lane.py` with the five commands under Reproduce: IDENTICAL 16/16, exit 0,
  run before this line was added. main_case_2026_10_14's `item_job_capital.cjs`, as it stands, reads the new
  item.json in a scratch copy with only its source pointer changed. The central and all nine arms pass readBlock,
  including central_bn by reading. The plain-share gate passes on set and cash, and the nationals match.
- 2026-10-14 16:50 JST: the team lead's "final v7 construction" message and v7case's format message arrived after the
  16:46 report; they confirm mining at 0 and corporate {1, 0.37}. To match their names:
  - arm `normal_return_share` restored (0.37 at both readings);
  - the 0.25 arm renamed `normal_return_share_0_25` and the by-industry arm `normal_return_share_by_industry`;
  - beside row `beside_mining_severance_0` restored (mining as other industries, severance at 0).

  TP-5's "pure rent, not risk" assumption is added to the construct note. The residential pricing moved to open
  problems (the team lead: follow-up critique, not v7). The central is unchanged. 76 + 16 + 70 gates and 15 tests pass.
- 2026-10-14 16:52 JST: `scripts/rerun_lane.py` with the five commands under Reproduce: IDENTICAL 16/16, exit 0, run
  before this line was added. `derived/item.json` sha256
  a9c747113ecfc9f23cdf525e232c52a0c9fb592af70201dadb9832c61fcbc283. The v7 reader, in a scratch copy, passes on the
  central and all ten arms, on set and cash. Final.
- 2026-10-14 16:59 JST: parent's read-only construct review (GPT-6.1 Sol): no central defect over $1bn. Two prose
  corrections: mining's property key is the T00OTOP tax pattern, not Fixed Assets; the BLS check validates the headcount,
  not the capped wages. No output changed.
