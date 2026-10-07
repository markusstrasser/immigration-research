claude-opus-5-5

**Verdict:** The account does not charge pension legacy at the service lines' responses. It prices those lines from BEA consumption by function, and BEA books employer defined-benefit pensions there at the accrual normal cost. It moves the cash paid above that cost, which is amortization of the unfunded liability, out of compensation: $41.6bn of $214.3bn for state and local plans in 2024, $144.3bn of $250.5bn federal. Census's excess cash contributions also come out of state-local spending (NIPA T3.19 line 29). The legacy's interest sits in `domestic_interest`, which the case holds at response 0. [DATA: BEA T7.24 lines 5–6, T7.23 lines 5 and 8, T3.19 line 29; `derived/pension_trace.csv`]

**The gap is retiree health, which the pensions treatment does not cover.** Three corrections follow, each moving retiree health onto the treatment pensions already get:
- **State-local.** Retiree premiums paid as you go stay inside the service lines. The correction replaces them with the GASB 75 normal cost.
- **Federal civilian.** BEA counts annuitants' health premiums as compensation. The correction replaces them with OPM's normal cost.
- **Military.** Care bought for military retirees sits in `other_federal_benefits` at response 1. It is pay-go for past service, so the correction sets it to zero.

**Main case v5 moves +$0.56 / +$0.74bn, to $390.86–461.98bn.** The cash set moves by the same amount, to $307.94–384.15bn. That is $9,142–10,806 per member of the 42.75M lineage. [CALCULATION: `case_opeb.cjs` → `derived/case_oct05.csv`, arm `central`, ends 48 / 11]

**The arms span −$0.80 to +$2.93bn.** The sign rests on one measured ratio: the states' GASB 75 normal cost over their employer contributions, 1.20 in FY2019. At a ratio of 1 the correction is −$0.80 / −$0.69bn.

**Recommendation:** adopt it in the next main case as one package, "retiree health on accrual, legacy at response 0". It applies the account's pension rule to retiree health, and it moves the case by less than 0.2%. It does not need a case of its own.

**Strongest counter-argument.** The state-local amount is scaled up from FY2019 state plans:
- the all-government factor μ is 1.33–2.30;
- 2024 is reached by growth in group-health contributions;
- GASB 75 discounts unfunded plans at low municipal-bond rates, which inflates normal cost.

On a plan-rate basis the ratio could fall to 1 or below, and the sign flips. The brief's literal reading removes pay-go and adds no normal cost, which gives −$8.65 / −$9.05bn. I do not recommend it: it also drops the accrual of today's service, which BEA keeps on the line for pensions.

Lane `infra/immigration-fiscal/public_pension_legacy_2026_10_07/`, 2026-10-07, 10:42–11:00 JST (times from `date`). It adopts nothing.

## 1. Where the account's retirement costs sit

**The service lines.** These are NIPA T3.17 consumption expenditures by function (federal plus state and local): general public services, public order, economic affairs, housing, health, recreation, education and income security. Each is one cell of the partition. [SOURCE: `full_account_spending_2026_09_20/builder.py`, `partition()`] Schools are this education line, keyed by pupils priced at their states' per-pupil spending; the decision of 2026-09-26 sets their response to 1. General government responds at 0.60–0.85.

**Pensions are on accrual and their legacy is off the lines.**

| 2024, $bn | Cash employer contributions | In compensation (accrual) | Cash above the accrual |
|---|---:|---:|---:|
| State and local DB (T7.24 lines 5, 5+6) | 214.289 | 172.711 (incl. service charges) | 41.578 (19.4% of cash) |
| Federal DB (T7.23 lines 5, 5+8) | 250.510 | 106.162 | 144.348 (57.6%) |

[DATA: BEA Section 7 workbook, SHA256 `ce107c8c…b9ef`; `derived/pension_trace.csv`]

- **Census reconciliation.** BEA builds state-local spending from Census totals. NIPA T3.19 line 29 removes $33.586bn of employer contributions to own DB plans (FY2023) from Census expenditure, and line 32 handles the imputed interest. [SOURCE: BEA Section 3 workbook, SHA256 `69b5c7ae…615e`]
- **BEA's method.** "Estimates of employers' normal costs are based on the service costs and employee contribution data reported in state and local government financial reports; BEA adjusts the estimates to reflect the same discount rate that is used for measures of privately sponsored defined benefit plans." [SOURCE: NIPA Handbook ch. 10, apps.bea.gov/national/pdf/chapter10.pdf]
- **The interest.** The legacy's interest is in `domestic_interest` at response 0: $162.963bn state-local imputed, plus $151.077bn federal. The pension legacy lane has measured it and keeps it beside the account. [DATA: `pension_legacy_2026_09_30/RESULT.md`]
- **Federal amortization.** The Treasury's payments for unfunded liabilities are excluded from NIPA expenditure, or treated as capital transfers. [SOURCE: BEA FAQ 553; SCB May 2023 federal budget article, note 4]

**State-local retiree health is on the lines on a pay-go basis.**
- **Census.** Census classifies "'Pay-as-you-go' plans or 'gratuities' to former employees" and "Group insurance premiums covering the government's own employees" as current operation expenditure. [SOURCE: Census Government Finance and Employment Classification Manual 2006, ch. 5, §5.3.4]
- **BEA.** BEA's state-local spending starts from Census total expenditure. T3.19 has no line for retiree health, and no state-local social benefit line in T3.12 (lines 27–42) is large enough to hold it. So it sits in consumption by function. [INFERENCE: table structure; T3.12 checked in this lane]

**Federal civilian retiree health is in compensation.** "The contributions for employee health insurance consist of the federal share of premium payments to private health insurance plans for current employees and retirees." [SOURCE: BEA FAQ 553, bea.gov/help/faq/553] Where BEA places them by function is not documented. They are spread here by the pension lane's federal civilian mix, a third of it to defense. [ASSUMPTION]

**Military retiree health has two parts.**
- **Defense.** Its accrual (the MERHCF normal cost, T7.8 line 16, $11.054bn) and the care in military treatment facilities sit in defense, at response 0.
- **Civilian providers.** "Payments for medical services for retired military personnel and their dependents at nonmilitary facilities" are in T3.12 line 26, footnote 7. That is the account's `other_federal_benefits`, $86.425bn, keyed `all_cash` at response 1. [SOURCE: T3.12 footnote 7; DATA: engine evaluation] The case therefore charges the group 4.6–5.0% of this pay-go for past service.

## 2. Measurement

| Item | Value | Source |
|---|---:|---|
| States FY2019: GASB 75 normal cost (service cost) | $26.858bn | Pew 2023, Appendix B, 48 states (NE, SD n/a) [SOURCE, parsed from the PDF; the parse is gated on Pew's own $30bn net-amortization shortfall, which sums to $30.386bn] |
| States FY2019: employer contributions | $22.390bn | same |
| States FY2019: interest on net OPEB liability (legacy, not priced) | $28.247bn | same |
| Ratio ρ, normal cost over employer contributions | **1.1995** | [CALCULATION] |
| States, net OPEB gap 2019 / 2016 | $680.3bn / $650bn | Pew 2023 (national row; 2016 sentence) |
| All S&L net OPEB liability, FY2019 | $1,233.3bn | Reason Foundation 2021 survey, totals row |
| All S&L unfunded OPEB, CRR (FY2013–14 data) | $862bn | CRR SLP 48 (2016) |
| μ, all S&L over state plans | low 1.326 (CRR / Pew 2016), **central 1.813** (Reason / Pew 2019, same year, both net), high 2.300 | [CALCULATION; high is symmetric about the central, ASSUMPTION] |
| Growth 2019→2024, employer group-health contributions | 1.2509 ($801.7bn → $1,002.9bn) | BEA T7.8 line 17 |
| **S&L pay-go 2024** | $28.01bn states × 1.813 = **$50.78bn** ($48.82bn on the engine's lines, the rest enterprises) | [CALCULATION] |
| Federal civilian FY2024: normal cost / benefits paid | $20.4bn / $16.6bn (ρ 1.229) | FR FY2025 Note 13, FY2024 column |
| Military FY2024: normal cost / benefits paid | $37.5bn / $24.9bn (ρ 1.506; used as ρ's high arm) | same |
| MERHCF FY2024: purchased care / total care | $9.7bn / $12.2bn | DoD MERHCF Audited Financial Report FY2024 |
| Military retiree purchased care in line 26 | low 9.7 (MERHCF only), **central 19.80** (+ pre-65 $12.7bn × MERHCF's purchased share), high 22.4 (+ all pre-65) | [CALCULATION; central and high ASSUMPTION] |

- **Cross-check.** Lutz and Sheiner (2014) put total state-local retiree-health outlays near $31bn in 2011. Growing at about 3.4% a year to 2019, that reaches the $40.6bn implied here (22.39 × 1.813). [SOURCE: Exa highlight of Lutz–Sheiner; not re-read in full: UNVERIFIED as a calculation input, used only as a check]
- **Funding.** Per Pew, states' 2019 contributions collectively exceeded benefit payments by $1.2bn, so state employer contributions are close to pay-go. [SOURCE: Pew 2023]

**Allocation to lines.** Each total is spread by the pension legacy lane's 2024 payroll mix (`pension_legacy_2026_09_30/derived/oct05/function_mix.csv`). For state-local payroll that is education 51.2%, public order 16.8%, health 10.3% and administration 7.3% (ASPEP 2024). Highways fold into `economic_affairs_services`. Enterprises (3.9%: +$0.39bn national, about +$0.05bn for the group) are left off the engine. [ASSUMPTION: OPEB proportional to payroll by function]

## 3. Construction

**National change.** For each line and plan: normal cost less pay-go, national. Military gets −pay-go only, since its normal cost is defense's.

- **Engine edit.** The change enters the case's payload as a national-scale edit (engine.js `scaleLine`). The line's national total moves and every cell scales with it, so the group's share of the line holds. The swap changes what the line costs, not who uses it.
- **Group's move.** The group's amount, on the key the case evaluates (the lineage's added people included), moves by change × share. The engine applies each line's response at each of the 64 specifications.
- **What stays fixed.** The capital return and the state-price and school correction lines do not move. The one exception is $0.001bn, through the k12 component's `part_rekeyed` key. The cash set takes the same edits on its own model.

Per line, central arm, low end (spec 48, shared allocation) / high end (spec 11, personal allocation), $bn:

| Line | Group share | National change | Response | Change |
|---|---:|---:|---:|---:|
| education_services | 0.170 / 0.177 | +5.238 | 1 | +0.891 / +0.929 |
| public_order_safety (use key) | 0.143 | +2.050 | 1 | +0.294 / +0.294 |
| health_services | 0.061 | +1.820 | 1 | +0.112 / +0.112 |
| general_public_services | 0.126 | +1.163 | 0.601 / 0.851 | +0.088 / +0.125 |
| income_security_services | 0.189 / 0.178 | +0.447 | 1 | +0.085 / +0.079 |
| economic_affairs_services | 0.088 | +1.202 | 0.384 / 0.639 | +0.041 / +0.067 |
| housing_community_services | 0.126 | +0.211 | 1 | +0.027 / +0.027 |
| recreation_culture | 0.126 | +0.153 | 0.856 / 1 | +0.016 / +0.019 |
| defense | 0.126 | +1.259 | 0 | 0 |
| other_federal_benefits (military retiree care) | 0.050 / 0.046 | −19.798 | 1 | −0.989 / −0.915 |
| **Total** | | −6.257 | | **+0.565 / +0.737** |

[CALCULATION: `derived/by_line_oct05.csv`]

## 4. Arms ($bn, change at the case's ends 48 / 11; the cash set moves identically)

| Arm | National change | Case | Change |
|---|---:|---:|---:|
| **central** (μ 1.813, ρ 1.1995, federal in, military 19.8) | −6.26 | **390.86–461.98** | **+0.56 / +0.74** |
| μ low (1.326) | −8.87 | 390.49–461.60 | +0.20 / +0.35 |
| μ high (2.300) | −3.64 | 391.22–462.36 | +0.93 / +1.12 |
| ρ = 1 (accrual equals pay-go in state and local plans) | −16.00 | 389.50–460.55 | −0.80 / −0.69 |
| ρ high (1.506, the military ratio) | +8.71 | 392.95–464.17 | +2.65 / +2.93 |
| military low (MERHCF purchased care only, 9.7) | +3.84 | 391.36–462.45 | +1.07 / +1.20 |
| military high (22.4) | −8.86 | 390.73–461.86 | +0.43 / +0.62 |
| no federal (state and local only) | +9.74 | 391.65–462.67 | +1.36 / +1.43 |
| federal only (civilian swap + military) | −16.00 | 389.50–460.55 | −0.80 / −0.69 |
| beside: pay-go removed, no normal cost added | −85.22 | 381.65–452.19 | −8.65 / −9.05 |

Pensions only (the brief's "without retiree health" arm) is **0** by construction: no pension amortization is on a responding line. Band ends stay at specifications 48 / 11 in every arm. [CALCULATION: `derived/case_oct05.csv`, `derived/case_oct05.json`]

**Beside, not an edit: the school key's state prices.**
- **The mechanism.** The school key prices each pupil at the state's ASSF current spending per pupil, which includes cash benefits (amortization and OPEB pay-go). The group's states spend 22.1% of current spending on benefits, against 23.4% nationally. [DATA: ASSF FY2024 Table 6; `account_pupils_by_state.csv`]
- **The bound.** If legacy is 15–35% of benefits in every state [ASSUMPTION], stripping it raises the group's relative school price by 0.18–0.46%, which adds **+$0.27–0.66bn at the low end and +$0.36–0.87bn at the high end**. [CALCULATION: `derived/school_beside_oct05.csv`]
- **Status.** The legacy fraction of benefits by state is not measured, so this stays beside the account.

## 5. Gates (all pass)

- The consumer reproduces the case ($390.2940 / 461.2431bn) and the cash set ($307.3764 / 383.4093bn) from their payloads to 1e-9. Ends are 48 / 11.
- The per-member divisor is the payload's lineage population, 42.752M.
- A zero edit on every line reproduces both sets exactly at all 64 specifications: the positive control.
- Every arm's engine change, less its capital-return move, equals Σ change × share × the engine's own line response, to 2e-13bn at all 64 specifications of both sets.
- The capital-return move is at most $0.0012bn.
- `national.csv` adds to `inputs.json`.
- The Pew parse reproduces Pew's $30bn shortfall.
- The FR civilian FY2024 values are pinned (20.4 / 16.6), civilian + military = total for every FR row, and the BEA labels are checked.
- Every source file's SHA256 is pinned.

## 6. Limits

- **The state-local flows are not measured for 2024 or for local governments.** They are FY2019 state-plan flows scaled by liability ratios (μ) and by group-health growth. No national 2024 GASB 75 flow aggregate was found in a primary source. The μ sources differ in year and coverage: Reason misses local governments that do not follow GASB.
- **GASB 75 normal cost uses the municipal-bond rate for unfunded plans.** That is roughly BEA's kind of discount rate for pensions, so the accrual reading matches the pensions treatment. At plan rates of about 7% the normal cost would be lower, toward the ρ = 1 arm.
- **The function mix is payroll.** Retiree health is more generous for teachers and public safety than for general employees, which would tilt it toward education and public order. Both are lines at response 1 with group shares above average, so the payroll mix probably understates the swap. [INFERENCE]
- **BEA's placement by function of the federal annuitant premium is not documented.** If it all sits in federal health (share 0.061), the civilian part shrinks by about half.
- **Pensions on a lower discount rate (the symmetric case, not priced).** The FR's federal pension normal cost at Treasury rates is $142.2bn, against BEA's federal employer accrual of $106.2bn. The FR figure includes employee contributions, so it is not like for like. A Treasury-rate accrual for all public plans would raise the lines. That is a different convention question from legacy.
- **The group's own veterans' benefits are left as they are.** VA medical and veterans' pensions and disability stay keyed to the group's own veterans at response 1. They are benefits to members and stop on removal, so they are not legacy in the brief's sense.

## 7. Reproduce

```sh
# from the repository root
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/public_pension_legacy_2026_10_07/opeb_national.py
node infra/immigration-fiscal/public_pension_legacy_2026_10_07/case_opeb.cjs
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/public_pension_legacy_2026_10_07 \
  "uv run --no-project python3 {lane}/opeb_national.py" "node {lane}/case_opeb.cjs"
```

**Inputs.**
- **Downloaded here** (under `sources/immigration-fiscal/data/external/stage3/`, each with an `ACQUIRED.md` line): Pew 2023 (`pew/opeb_2023/`), CRR SLP 48 (`crr/slp48/`), the Reason survey (`reason/opeb_2021/`) and the DoD MERHCF AFR FY2024 (`dod/merhcf_afr_fy2024/`).
- **Reused, hash-checked:** the pension legacy lane's cached BEA Section 3 and 7 workbooks and FR Note 13, the school lane's ASSF FY2024 summary tables, and its `account_pupils_by_state.csv`.
- **Tooling:** `pdftotext` (poppler) is required. Peak memory is under 100 MB.

## Log (append-only)
- 2026-10-07 10:46 JST: traced the lines. The account's service lines are BEA T3.17 consumption by function (`full_account_spending_2026_09_20/builder.py` partition()). BEA records state-local and federal DB pension compensation at the accrual normal cost (T7.24 lines 5+6 = $172.711bn against $214.289bn cash; T7.23 federal $106.162bn against $250.510bn cash) and removes the cash excess as the negative imputed contribution; T3.19 line 29 removes Census's excess cash employer contributions ($33.586bn FY2023) from S&L expenditure. So pension amortization is not on any responding line [DATA: pension_legacy_2026_09_30 measured_2024.csv; SOURCE: BEA T3.19 FY2023]. Open: retiree health (OPEB). Census classifies pay-as-you-go payments to former employees and group premiums as current operations (Classification Manual 2006 ch. 5, §5.3.4) and T3.19 has no OPEB line; BEA FAQ 553 says federal health contributions cover "current employees and retirees" [SOURCE].
- 2026-10-07 10:48 JST: OPEB measured. Federal (FR FY2025 Note 13, FY2024 column): civilian normal cost $20.4bn against benefits paid $16.6bn; military $37.5bn against $24.9bn (military sits in defense, response 0). States (Pew 2023 Appendix B, FY2019, 48 states parsed, sum checks against Pew's $30bn shortfall: $30.39bn): GASB 75 normal cost $26.86bn, employer contributions $22.39bn, interest on net OPEB liability $28.25bn. Accrual exceeds pay-go in both: the symmetric case. [CALCULATION; SOURCE]
- 2026-10-07 10:54 JST: opeb_national.py runs (rc 0). National 2024, central: S&L pay-go $50.78bn (states $22.39bn FY2019 x growth 1.2509 x mu 1.813), of which $48.82bn on engine lines; normal cost at rho 1.1995; federal civilian pay-go $16.6bn, normal $20.4bn. Swap on the engine lines: +$13.54bn national (mu 1.326-2.300: +$10.9-16.2bn; rho 1: +$3.8bn; rho 1.506: +$28.5bn). Pay-go removed without the normal cost (the brief's literal reading): -$65.4bn national. Next: engine run.
- 2026-10-07 10:59 JST: first engine run used group-amount edits, which leaked into share-based items (implied responses up to 1.26). Switched to national-scale edits (shares hold); the gate now ties the engine change to Σ change × share × response (2e-13bn). Found military retiree purchased care in T3.12 line 26 (`other_federal_benefits`, all_cash key, response 1) and added it at response 0 (MERHCF AFR FY2024: $9.7bn purchased care). Central: +$0.56 / +$0.74bn on the case and the cash set.
- 2026-10-07 11:00 JST: RESULT written; rerun_lane run follows.
- 2026-10-07 11:00 JST: rerun_lane.py with both commands: IDENTICAL 11/11, exit 0. Not committed (analysis worker).
