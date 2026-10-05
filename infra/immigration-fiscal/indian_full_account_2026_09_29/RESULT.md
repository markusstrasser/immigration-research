claude-opus-5-5

**Verdict:** [2026-10-05: on main case v5 (`oct05`), Indian-origin residents benefit others by $9,325–10,782 per
member, the Mexican-origin union (the 42.75M lineage) costs others $11,581–13,349 per member with its social rows, and
the gap between the two is $22,400–22,700. See "v5 case (oct05)" below.] On the adopted v4 account plus the social rows the Mexican-origin union carries, Indian-origin residents (the India-born and the US-born children of an India-born parent, 6.08M in CPS ASEC 2025) benefit other residents by about **$9,300–10,800 per member a year, $57–65bn in all**. The fiscal part is a benefit of $10,600–12,000 (SE about $1,150), and the social rows are a cost of $1,250–1,350. At the age structure of third-plus non-Hispanic whites, the aged group still benefits others by **$7,100–8,400 per member**: a fiscal benefit of $8,600–9,900 against social rows of $1,450–1,510 (corrected 2026-10-06 from the first run's
$1,470–1,530; see the correction at the end of the v5 section). On the same footing, the Mexican-origin union costs others **$11,800–13,500 per member** ($12,200–13,900 at white ages), and third-plus whites cost **$2,900–4,200**. Per member, the Indian-origin group is therefore about **$13,500 better than whites** and **$22,500–22,800 better than the union**. Ageing to white ages removes about a sixth of its lead over whites. This is a rough re-key through the key library the Black and white comparators use, not an engine run. Its offending, long-term-care and driving inputs are proxies [DEGRADED]. On the union, the rough method comes out 2.4% below the engine at the high end and 1.1% above it at the low end. Two robustness checks leave the result standing. Pooling the thin second-generation cell over five ASEC files (941 adults instead of 209) moves the total by only $136 per member. Self-employed and wage-earning India-born adults both benefit others by about $17,000–20,000 per person, and the two are not distinguishable at n = 68. [CALCULATION: `rekey_indian.py`, `social_rows.py` → `derived/combined.csv`]

Lane `infra/immigration-fiscal/indian_full_account_2026_09_29/`, written 2026-09-29 by a teammate for the team lead. Nothing here is committed or adopted. Figures are 2024 dollars a year. A positive figure means the group's presence costs other residents; a negative figure means it benefits them. Each pair is the case's low / high end (specs 48 / 11).

## Main table (the case: accrual basis)

| Group | Persons | Fiscal, per member | Social rows, per member | **Total, per member** | Total, $bn |
|---|---:|---:|---:|---:|---:|
| Indian-origin, actual ages | 6.08M | −12,006 / −10,635 (SE 1,158 / 1,147) | +1,243 / +1,330 | **−10,763 / −9,305** | −65.4 / −56.6 |
| Indian-origin, third-plus white ages | 6.08M | −9,886 / −8,594 (SE 1,055 / 1,042) | +1,453 / +1,510 | **−8,433 / −7,084** | −51.3 / −43.1 |
| India-born only, actual ages | 4.28M | −12,179 / −10,751 (SE 1,099 / 1,085) | +887 / +990 | **−11,292 / −9,761** | −48.3 / −41.8 |
| India-born only, white ages | 4.28M | −7,492 / −6,212 (SE 979 / 967) | +1,256 / +1,328 | **−6,236 / −4,884** | −26.7 / −20.9 |
| Mexican-origin union, actual ages (engine) | 39.71M | +9,353 / +10,950 | +2,424 / +2,535 | **+11,777 / +13,485** | +467.7 / +535.5 |
| Mexican-origin union, white ages | 39.71M | +9,748 / +11,313 | +2,440 / +2,538 | **+12,188 / +13,851** | +484.0 / +550.0 |
| Third-plus NH whites (a 39.71M slice, own ages) | 39.71M | +610 / +1,865 | +2,254 / +2,294 | **+2,864 / +4,159** | +113.8 / +165.2 |

[DATA: `derived/combined.csv`, `derived/rekey_summary.csv`, `derived/social_rows.csv`]

- **Whites at white ages.** Whites' own ages are the white ages, so their row serves both columns. The slice is the white lane's A1, scaled to the union's count; per-member figures are the comparable ones.
- **The union at white ages.** This row is the engine's figure plus the rough method's age effect (rough at white ages less rough at own ages): +$395 / +$363 per member. The rough figure alone is +$9,850 / +$11,054.
- **The union's social rows.** These are the pairing's rows on the 39.71M the account prices, with the NHTS 5+ basis: $96.3 / 100.7bn. Added to the v4 fiscal account they give $467.7–535.5bn. The pairing printed in the index, $413.7–488.0bn, still carries the September 27 fiscal row ($317.5 / 387.4bn). This lane's gate rebuilds that sum exactly.
- **Standard errors.** They come from 160 CPS ASEC replicate weights and cover only the Indian groups' CPS sampling. MEPS (317 sampled Asian Indians), the ACS proxy and the social drivers are held fixed. The CPS sample is 2,311 Indian-origin persons: 1,607 India-born and 704 second generation. Among adults 25–64 it is 1,232 India-born and 209 second generation, the counts in ladder 150.

### Cash basis and the top tail, beside

| Per member | Indian-origin, actual | Indian-origin, white ages | India-born | Union (engine) | Union, white ages | Whites |
|---|---:|---:|---:|---:|---:|---:|
| Fiscal, cash set (pensions paid, not accrued) | −16,994 / −15,623 | −11,479 / −10,187 | −18,190 / −16,762 | +7,421 / +9,111 | +10,956 / +12,614 | +2,462 / +3,716 |
| Total, cash set | −15,751 / −14,293 | −10,012 / −8,663 | −17,302 / −15,772 | +9,845 / +11,646 | +13,396 / +15,152 | +4,716 / +6,010 |
| Fiscal, accrual, top tail spread by CPS income tax | −14,625 / −13,255 | −12,395 / −11,103 | −14,652 / −13,224 | rough +8,848 / +10,085 | rough +9,218 / +10,422 | −914 / +341 |

- **Cash against accrual.** On the cash set the young Indian group looks about $5,000 better than on accrual, because accrual books the pension promises its payroll taxes buy. At white ages the two bases differ by about $1,600.
- **The top tail.** The central charges each group only the income tax the CPS records. The CPS misses the top tail, and this group's income is concentrated there. Spreading the missing tail in proportion to CPS income-tax dollars improves the Indian figures by about $2,600 per member, so the central is conservative for this group. [DATA: `derived/rekey_summary.csv`, columns `cost_top_tail_proportional_*`]

## Robustness: the second generation pooled over five ASEC files

The 2025 file has only 209 second-generation adults aged 25–64. `pooled_asec.py` stacks ASEC 2022–2026 (income years 2021–2025, n = 941, CPI-U to 2024 dollars) on the re-key's own tax and earnings keys. [CALCULATION: `derived/g2_pooled.csv`]

| G2 adults 25–64, per person, 2024 $ | ASEC 2025 (SE, 160 replicates) | Pooled 2022–26 (SE across years) | Pooled / 2025 |
|---|---:|---:|---:|
| Federal income tax (tax-unit share) | 18,296 (2,601) | 16,887 (785) | 0.923 |
| State income tax | 5,069 (651) | 4,759 (242) | 0.939 |
| Earnings | 115,293 (12,321) | 117,604 (2,979) | 1.020 |
| OASDI earnings | 85,193 (4,143) | 86,612 (2,688) | 1.017 |

Scaling the 2025 G2 adults' keys to the pooled means (`indian_origin_g2_pooled`) moves the full account by only $136 per member. The whole Indian-origin group comes to −$11,870 / −10,498 fiscal and −$10,627 / −9,169 in total, against −$10,763 / −9,305 centrally. At white ages the total is −$8,326 / −6,976. The CPS replicate SE is $1,148 / 1,137, and the pooled means' own SE adds ±$90 per member. The 2025 G2 cell pays slightly more income tax than the five-year pool and earns about the same, so the thin cell does not drive the result. [CALCULATION: `derived/rekey_summary.csv`, `cost_per_member_se_pooled_mean`; `derived/combined.csv`]

## The India-born by class of worker

This split uses the class of each person's longest job last year (LJCW): self-employed (incorporated or not), wage and salary, and everyone else (children and adults who did not work). The three person-level parts add to the India-born total to within $0.01bn; the small gap comes from the state-price rule. The household rows put each Indian-origin person, children included, in the class of their household's highest-earning India-born worker. They are the fairer comparison, because a worker's children otherwise land in "other". Per member, accrual basis, low / high. [CALCULATION: `derived/combined.csv`, `derived/rekey_summary.csv`]

| India-born, 2025 | Sampled | Persons | Earnings per adult worker | of which self-employment income | Fiscal (SE) | Social | **Total** |
|---|---:|---:|---:|---:|---:|---:|---:|
| Self-employed adults | 68 | 0.17M | $150,840 | $37,284 | −19,044 / −17,373 (4,918) | +654 / +702 | **−18,390 / −16,672** |
| Wage and salary adults | 1,028 | 2.68M | $127,039 | $232 | −20,078 / −18,447 (1,213) | +278 / +394 | **−19,800 / −18,052** |
| Everyone else (children, non-workers) | 511 | 1.44M | | | +3,352 / +4,372 (1,400) | +2,090 / +2,173 | **+5,442 / +6,545** |
| Households led by a self-employed India-born worker | 136 | 0.36M | $125,341 | $26,851 | −18,817 / −17,453 (11,866) | +1,411 / +1,446 | **−17,405 / −16,008** |
| Households led by a wage-earning India-born worker | 1,810 | 4.72M | $124,325 | $344 | −12,582 / −11,198 (1,025) | +1,159 / +1,246 | **−11,423 / −9,952** |

- **Self-employed and wage workers are the same within sampling error.** Person by person the two are about $1,000 apart, with an SE of $4,900 on 68 self-employed persons. By household, the self-employed look $6,000 better, but that SE is $11,900: one or two very high-income households in 136 sampled persons drive it.
- **Motels and convenience stores are rare in the CPS.** Pooled over 2022–2026, only 27 of 350 sampled self-employed India-born adults work in traveler accommodation, grocery or convenience stores, or gasoline stations; 2025 has two. More India-born adults in those industries are wage workers (108 pooled). A full-account row for motel and convenience-store owners cannot be estimated from these files. [DATA: `derived/g1_class_pooled.csv`; the industry codes are Census 2017 codes, INFERENCE]
- **Self-employment income is under-reported, and this bias is not measured here.** Survey respondents and tax filers both understate self-employment income; income without third-party reporting has the largest misreporting rates in the IRS tax-gap studies [TRAINING-DATA]. Two things follow:
  - The CPS keys use reported income and the CPS tax model's tax on it, so the self-employed rows could be wrong in either direction. True income is higher than reported, while taxes actually paid may be lower than the model's.
  - Incorporated owners (LJCW 5) pay themselves partly in wages, so self-employment income ($37,284 of $150,840) is a lower bound on business income.
- **Proxies shared with the whole group.** MEPS cannot split by class of worker, so all India-born subgroups share the India-born medical shares. They also share the institutionalization proxy [DEGRADED].

## Where the fiscal gap comes from (accrual, low end, per member)

| Program group | Union (engine) | Indian-origin | Indian-origin, white ages | Whites |
|---|---:|---:|---:|---:|
| Income taxes lost | −3,489 | −14,917 | −14,038 | −8,327 |
| Payroll taxes and Medicare premiums lost | −4,065 | −9,324 | −8,678 | −6,276 |
| Sales, excise, fees lost | −2,731 | −4,615 | −4,538 | −4,054 |
| Capital, property, production taxes lost | −577 | −1,494 | −1,599 | −1,166 |
| Social Security (accrued) | +2,770 | +5,601 | +5,052 | +3,966 |
| Medicare | +1,861 | +2,862 | +3,960 | +3,934 |
| Medicaid | +2,965 | +1,000 | +1,737 | +2,334 |
| Schools and colleges | +5,071 | +4,801 | +4,005 | +3,193 |
| SNAP, SSI, housing, cash aid, credits | +2,932 | +768 | +784 | +1,667 |
| Police, courts, prisons | +1,915 | +836 | +829 | +1,263 |
| Per-head lines, veterans, capital return, production term | +2,700 | +2,476 | +2,602 | +4,080 |
| **Total** | **+9,353** | **−12,006** | **−9,886** | **+610** |

[DATA: `derived/rekey_buckets.csv`. Negative rows are taxes the group pays that other residents would lose.]

- **Income tax carries the result.** The Indian-origin group's income tax per member is 4.3 times the union's and 1.8 times whites'.
- **Ageing the whole group.** White ages add about $1,100 of Medicare and $700 of Medicaid per member and remove about $800 of school cost. Taxes fall by only about $1,500.
- **Ageing the India-born.** The first generation alone ages harder: −12,179 → −7,492. It is concentrated at working ages, so white ages cut its payroll tax by $2,800 and its income tax by $1,700. They also add $1,100 of school cost, because the India-born have almost no children.
- **Accrual per tax dollar.** It is lower for this group than for the union: OASDI 0.944 against 1.018, and Part A 0.654 against 1.461. The likely reasons are that careers start at arrival and that high earnings fall on the flat part of the benefit formula [INFERENCE]. [DATA: `derived/accrual_ratios.csv`]

## Social rows (per member, low end)

| Row | Union | Indian-origin | Indian-origin, white ages | Whites | Rule for the Indian row |
|---|---:|---:|---:|---:|---|
| PM2.5 from consumption | +1,715 | +3,888 | +3,864 | +3,015 | air lane's grid; consumption per member 1.93× the union's; own-group share ι 0.10 assumed |
| Congestion | +343 | +343 | +343 | +343 | per member as the union [DEGRADED] |
| Road crashes (with against without) | +266 | +233 | +211 | +339 | driver-miles share, NHTS Asian rates [DEGRADED] |
| Violent-crime victims | +768 | +57 | +50 | +376 | ACS institutionalization 0.075× the union's [DEGRADED]; whites: the white lane's NCVS ratio 0.49 |
| Fear and avoidance | +260 | +20 | +17 | +128 | as victims |
| Property crime | +32 | +2 | +2 | +15 | as victims |
| Unreimbursed care | +78 | +33 | +30 | +24 | uninsured person-years per member (the lane's driver) |
| Private security | −12 | −206 | −208 | −103 | lane formula: $74.4bn × population share × (relative offending − 1) |
| School disruption | −49 | −129 | −107 | −65 | lane formula; CRDC Asian pupils: 6% of enrollment, about 1% of suspensions [DEGRADED] |
| Housing net | −86 | −139 | −106 | −68 | renters' consumption [DEGRADED] |
| Scale net (agglomeration + schooling) | −344 | −1,895 | −1,652 | −1,095 | scale lane's joint formula on the CPS, carried to its CZ level |
| Restaurant market size | −171 | −329 | −328 | −279 | consumption per member |
| Volunteering | −151 | −276 | −289 | −289 | 16+ count × the all-resident rate of 28.3% [UNVERIFIED: no Asian rate found] |
| Consumer-side scale | −54 | −103 | −103 | −87 | consumption per member |
| Trade, visits, FDI with the origin country | −171 | −256 | −271 | 0 | union's central × US–India / US–Mexico non-travel trade (0.22) |
| **Sum** | **+2,424** | **+1,243** | **+1,453** | **+2,254** | |

[DATA: `derived/social_rows.csv`, with each row's rule and its high end]

- **PM2.5 dominates the Indian social rows.** The row prices the group's share of consumption-driven pollution, so a high-spending group carries more of it. The air lane notes that this absolute row is mostly a matter of scale. Without it, the Indian social rows are a benefit of $2,645 per member.
- **The scale net becomes a large benefit.** For the union it is small. The schooling term flips sign: without the Indian-origin group, the share of workers with some college would fall 0.55 points, whereas removing the union raises it 2.9. At the CZ level, scale is worth $6.6bn and schooling $4.9bn. The lane's caveat applies with more force here: its 1970–2000 college-share estimates would make this benefit several times larger.
- **Innovation is not priced.** It is omitted for the union and the whites too (white lane, section C), because the repo has no primary source for a dollar value per inventor. For this group it is the likeliest large omission, and it would add to the benefit.

## Inputs: measured vs assumed

- **Measured, survey-based** [DATA]:
  - CPS ASEC 2025 keys: income and payroll tax, earnings, consumption, capital income, property, program dollars, pupils, uninsured person-years and state of residence;
  - MEPS 2024 medical shares for non-Hispanic Asian Indian alone (317 sampled);
  - ACS 2023 institutionalization (80 replicates);
  - NHTS 2017 driving by age for NH Asians;
  - Census c5330 goods trade with India, 2024;
  - the BEA USDIA position in India, 2024.
- **Proxies** [DEGRADED]:
  - Offending: the repo has no Indian offending data. ACS institutionalization at ages 18–64 stands in; it includes long-term care, so it is an upper bound on custody. On the NH Black group the proxy gives 34.5% of institutionalized adults, against SPI's 33.1% of prisoners. The India-born rate is 0.075% of adults (SE 0.012%), against 0.99% for the union proxy.
  - Asian or API data for Indians: T-MSIS Asian/Pacific Islander long-term-care spending per API resident 65+, NHTS NH Asian driving, and CRDC Asian suspensions.
  - The scale lane's formula, run nationally.
  - Housing and congestion, scaled rather than re-run.
- **Assumed** [ASSUMPTION / UNVERIFIED]:
  - ι, the share of the group's own pollution its members breathe: Indian 0.15 / 0.10 / 0.05, a white slice 0.15 / 0.12 / 0.10;
  - the volunteering rate, taken as the all-resident 28.3%;
  - the non-travel share of US–India services, 75% (range 50–100%);
  - FDI through India holding companies, not netted.
- **Structural** (as in the Black and white comparators):
  - no production (complementarity) term for the Indian group, while the union gets the engine's;
  - the rough CPS keys, not the engine's hot-deck administrative keys;
  - every Indian-origin member counted on the books, since the pension lane models unauthorized status for the Mexico-born only.
- **White ages mean today's per-age rates** [INFERENCE]. "In 40 years" is modelled as today's per-age rates at the white age structure. Today's older Indian-origin residents are mostly parents who arrived late on family visas and had short US careers. The future old will be today's high earners, with full careers. The white-age row therefore probably understates the aged group's taxes and overstates its Medicaid and SSI. The accrual basis already books the pension side of this on today's earnings.

## Checks against the adopted numbers

- **The engine's union reproduces the case.** Through W.setup()'s gates it gives the adopted $371.4146 / 434.8410bn (accrual) and $294.7011 / 361.8175bn (cash). The dumps match `main_case_bands.csv`, and the lane's cost formula on the engine's amounts reproduces them to 1e-9.
- **The rough method on the union** gives $375.5 / 424.6bn, which is 1.1% above and 2.4% below the engine, and $294.9 / 344.0bn on cash.
- **The other comparators reproduce.** The white A1, NH Black, rough-union and engine-union rows each match their lane's `rekey_summary_sept29.csv` to 5e-5.
- **The social rows reproduce the pairing.** The union's rows plus the September 27 fiscal row give $413.744835 / 488.047064bn to 1e-6. The air lane's grid reproduces the priced 68.092104. The security, school and scale formulas rebuild the union's rows to 1e-3.
- **The counts differ.** CPS ASEC 2025 counts 4.28M India-born; ACS 2023 counts 2.94M. The lane uses the CPS frame and does not reconcile the two. Per-member figures are insensitive to the count; totals in $bn scale with it.

## Files

- `acs_custody.py` → `derived/acs_institutional.csv`, `acs_institutional_cells.csv`
- `accrual_indian.py` → `derived/accrual_ratios.csv`, `benefit_tax_proxy.csv`. It imports the Black lane's `accrual_black.py` read-only.
- `nhts_asian.py` → `derived/nhts_vmt_asian.csv`
- `pooled_asec.py` → `derived/g2_pooled.csv`, `g1_class_pooled.csv`. It reads the ASEC 2022–2024 and 2026 zips from other lanes' caches.
- `rekey_indian.py` → `derived/rekey_summary.csv`, `rekey_buckets.csv`, `rekey_replicates.csv`, `keys.csv`, `age_structures.csv`, `drivers.csv`. It imports the white lane's `rekey_sept29.py` read-only; that file is uncommitted peer work in this checkout, so it must be committed before this lane is.
- `social_rows.py` → `derived/social_rows.csv`, `combined.csv`. It imports `air_pollution_2026_09_28/air_items.py` read-only.

Reproduce from the repository root, in order (4–20 minutes, depending on machine load):

```sh
L=infra/immigration-fiscal/indian_full_account_2026_09_29
for s in acs_custody accrual_indian nhts_asian pooled_asec rekey_indian social_rows; do
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/$s.py; done
```

## Log

Times come from `date`.
- 2026-09-29 21:52 JST: read the Black and white re-key lanes, the sept29 library and the social-row lanes.
- 2026-09-29 22:07 JST: inputs confirmed: the ACS proxy, the accrual ratios (the union gate passes) and NHTS Asian driving (the NH white gate passes).
- 2026-09-29 22:25 JST: `rekey_indian.py` exits 0 with all gates passing; `social_rows.py` exits 0 with all 23 gates passing.
- 2026-09-29 22:33 JST: began a from-scratch rerun of all five scripts to byte-compare `derived/`.
- 2026-09-29 22:36 JST: the rerun ended. All five scripts exit 0, and all 13 files in `derived/` are byte-identical to the first run (`cmp`).
- 2026-09-29 22:50 JST: the operator's two additions were run: the G2 cell pooled over ASEC 2022–2026 (`pooled_asec.py`) and the India-born split by class of worker; all gates pass.
- 2026-09-29 23:18 JST: a second from-scratch rerun of all six scripts ended (started 22:58). All exit 0, and all 15 files in `derived/` are byte-identical (`cmp`).

## v5 case (oct05), 2026-10-05

[2026-10-05: on main case v5 (`oct05`, `../main_case_2026_10_05/`), Indian-origin residents benefit other residents by
**$9,325–10,782 per member a year** on the accrual basis (sept29 $9,305–10,763), $56.7–65.6bn in all; the Mexican-origin
union, now the lineage's 42,752,213, costs others **$11,581–13,349 per member** with its social rows (sept29
$11,777–13,485 on 39,712,493) and third-plus whites on 42.75M **$2,834–4,128** (sept29 $2,864–4,159). The Indian-origin
group is about $13,500 per member better than whites, as before, and **$22,400–22,700 better than the union** (sept29
$22,500–22,800). [CALCULATION: `rekey_indian.py --case oct05`, `social_rows.py --case oct05` → `derived/oct05/combined.csv`]]

claude-opus-5-5 (v5consC)

**Rules (the case lane's Consumers row: both sides on 42.75M).**
- The union's fiscal rows (engine and rough) carry the 3,039,720 added people at the case lane's amounts, through the
  white lane's library (its section "v5 case (oct05)"). A1 is on 42,752,213, as in the white lane's oct05 run.
- The union's social rows add the added people's rows from the v5 pairing (`sept24_propagation_2026_09_24/derived/oct05/real_costs_totals.json`,
  `lineage_social_rows`: $8.56 / 8.76bn, each restated row times their share of its engine key, an [ASSUMPTION] of
  that lane), so the union's social rows are $104.8 / 109.4bn on 42.75M (sept29 $96.3 / 100.7bn).
- [ASSUMPTION] The Indian-origin groups keep their own CPS counts; only v5's responses move their fiscal rows ($18–19
  per member better), and their social rows do not move.
- [ASSUMPTION] **The union at white ages stays on the identified 39,712,493** at v5's responses. Its fiscal row is the
  identified engine union plus the rough method's age effect, as before; the case lane does not output the added
  people's amounts by age, so the age effect cannot be taken on them. Its per-member figure is the comparable one.
- Every other group's social rows keep this lane's rules against the identified union's per-member rows and drivers.
  A1's move from 39.71M to 42.75M changes two non-linear rows per member: PM2.5 −$22, scale +$6.
- The same comparison on the identified 39.71M at v5's responses is written beside, as `mexican_origin_engine_identified`
  ($371.12 / 434.53bn, $9,345 / 10,942 per member) and `mexican_origin_rough_identified` ($375.16 / 424.25bn).

**Main table on oct05** (accrual, per member, spec 48 / 11; parts add to totals with controlled rounding):

| Group | Persons | Fiscal | Social rows | **Total** | Total, $bn | sept29 total |
|---|---:|---:|---:|---:|---:|---:|
| Indian-origin, actual ages | 6.08M | −12,024 / −10,654 (SE 1,159 / 1,147) | +1,242 / +1,329 | **−10,782 / −9,325** | −65.6 / −56.7 | −10,763 / −9,305 |
| Indian-origin, third-plus white ages | 6.08M | −9,906 / −8,615 (SE 1,056 / 1,043) | +1,453 / +1,511 | **−8,453 / −7,104** | −51.4 / −43.2 | −8,433 / −7,084 |
| India-born only, actual ages | 4.28M | −12,197 / −10,770 (SE 1,100 / 1,085) | +887 / +990 | **−11,310 / −9,780** | −48.4 / −41.9 | −11,292 / −9,761 |
| India-born only, white ages | 4.28M | −7,510 / −6,230 (SE 979 / 968) | +1,255 / +1,328 | **−6,255 / −4,902** | −26.8 / −21.0 | −6,236 / −4,884 |
| Mexican-origin union (engine), 42.75M | 42.75M | +9,129 / +10,789 | +2,452 / +2,560 | **+11,581 / +13,349** | +495.1 / +570.7 | +11,777 / +13,485 |
| Mexican-origin union, white ages (identified) | 39.71M | +9,739 / +11,303 | +2,440 / +2,538 | **+12,179 / +13,841** | +483.7 / +549.7 | +12,188 / +13,851 |
| Third-plus NH whites (a 42.75M slice) | 42.75M | +596 / +1,850 | +2,238 / +2,278 | **+2,834 / +4,128** | +121.2 / +176.5 | +2,864 / +4,159 |

[DATA: `derived/oct05/combined.csv`, `derived/oct05/rekey_summary.csv`, `derived/oct05/social_rows.csv`]

- The union's per-member total falls by $196 / 136 because the added people cost $6,309 / 8,790 each on the fiscal
  side against the identified union's $9,345 / 10,942; their social rows add $28 / 25 per member.
- On the cash set the union is +$9,642 / +11,528 per member (sept29 +$9,845 / +11,646) and the Indian-origin group
  −$15,770 / −14,313 (sept29 −$15,751 / −14,293). [DATA: `derived/oct05/combined.csv`]
- The rough method on the union, both sides with the added people, is 1.0% above the engine at the low end ($394.3bn
  against $390.3bn) and 2.2% below it at the high end ($451.0bn against $461.2bn); on the identified 39.71M it is 1.1%
  above and 2.4% below, as on sept29.
- The pooled second generation moves the total by $136 / 137 per member, as before (−10,646 / −9,188).

**Gates.** `rekey_indian.py --case oct05`: 101 gates, exit 0. Beside the sept29 gates: the union, A1 and NH Black rows
reproduce the white and Black lanes' `rekey_summary_oct05.csv` (5e-5), and the identified engine union is the union
dump (1e-9). `social_rows.py --case oct05`: 25 gates, exit 0. Beside the sept29 gates: the v5 pairing prices the added
people on exactly this lane's items, and its union rows are this lane's restated rows (1e-6). The sept29 runs rewrite
`derived/` byte for byte (83 and 23 gates). `rerun_lane.py` with all eight commands (the six of the default list
and the two oct05 ones): **IDENTICAL 30/30, exit 0** (2026-10-06 00:40:08–00:42:42 JST).

**Reproduce (oct05)**, after the default list and the white and Black lanes' oct05 runs:

```sh
L=infra/immigration-fiscal/indian_full_account_2026_09_29
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_indian.py --case oct05
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/social_rows.py --case oct05
```

New: `derived/oct05/` with `rekey_summary.csv`, `rekey_buckets.csv`, `rekey_replicates.csv`, `keys.csv`,
`age_structures.csv` (with a `lineage` column), `drivers.csv`, `social_rows.csv` and `combined.csv`.
`rekey_indian.py` and `social_rows.py` gained `--case`; their default output is unchanged.

**Correction to the sept29 sections (2026-10-06).** The verdict, the main table's white-ages row and the social-rows
table carried the first run's values for the Indian-origin group at white ages. Commit f14d3d76 changed the trade row
for subgroups (−$257 to −$271 per member at white ages), and `derived/combined.csv` has carried the new values since.
The text now matches it: social rows $1,453 / 1,510, total −$8,433 / −7,084 per member (the verdict's "$1,470–1,530"
becomes "$1,450–1,510"). The two tables also now use controlled rounding, so printed parts add to printed totals; eight
cells moved by $1. [DATA: `derived/combined.csv`, `derived/social_rows.csv`]
