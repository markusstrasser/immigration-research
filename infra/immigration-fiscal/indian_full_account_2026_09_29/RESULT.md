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

[2026-10-07: `derived/oct05/` is rebuilt on the IPEDS keys for Pell and public higher education, a defect fix decided in
the v6 propagation (section "v6 case (oct07)"). On them the Indian-origin group benefits others by **$9,392–10,843 per
member** (the figures below, on the rough keys of September 27: $9,325–10,782), third-plus whites on 42.75M cost
$2,717–4,008, and the union is unchanged at $11,581–13,349; the Indian-origin group is $13,400–13,600 better than
whites and $22,400–22,700 better than the union. The social rows do not move. [CALCULATION: `derived/oct05/combined.csv`,
`ipeds_terms.csv`]]

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

## v6 case (oct07), 2026-10-07

[Round 2, later on 2026-10-07: every group's income taxes moved to the case's own keys. The figures in this section
use the CPS-dollar rule, now the `cost_cps` arm; the current figures are in "v6 round 2" below.]

[2026-10-07: on main case v6 (`oct07`, `../main_case_2026_10_07/`), with every group on the IPEDS keys for Pell and
public higher education, Indian-origin residents benefit other residents by **$9,447–10,901 per member a year** on the
accrual basis, $57.4–66.3bn in all (v5 on the same keys $9,392–10,843); the Mexican-origin union costs others
**$11,550–13,349 per member** with its social rows (v5 $11,581–13,349) and third-plus whites on 42.75M **$2,591–3,884**
(v5 on the same keys $2,717–4,008). The Indian-origin group is $13,330–13,490 per member better than whites and
**$22,450–22,800 better than the union**. Item 4's hospital term stays beside the central, at the team lead's decision;
with it the Indian-origin group would benefit others by $81 per member more. [CALCULATION: `rekey_indian.py --case
oct07`, `social_rows.py --case oct07` → `derived/oct07/combined.csv`, `ipeds_terms.csv`]]

claude-opus-5-5 (prop-d)

**Rules.** The oct05 rules carry over, and v6's four items reach the groups as in the white lane's section "v6 case
(oct07)": the union's side carries the items' union parts and its added people their measured ages and the items'
lineage parts; retiree health reaches every group through the national totals.
- [ASSUMPTION] **The 2026 Trustees' separate-funds path** prices the Indian-origin groups as the union and the white
  slice: `accrual_indian.py --case oct07` rebuilds their payable accrual ratios through the pension lane's code (the
  white lane's `tr2026_path.py`). Net OASDI accrual per tax dollar, 2025 reports → 2026 path, immigrants from arrival:
  Indian-origin 0.836168 → 0.819495, India-born 0.862083 → 0.845797; Part A per HI tax dollar 0.653816 → 0.652027 and
  0.689810 → 0.689074. [DATA: `derived/oct07/accrual_ratios.csv`, `derived/accrual_ratios.csv`]
- [ASSUMPTION] **The IPEDS keys** (the white lane's section "The IPEDS keys": a defect fix of the rough keys, every
  group on oct05 and oct07, sept29 kept). IPEDS reports Asian students, not Indian ones, so the Indian-origin groups take
  NH Asian students' shares by their CPS keys over NH Asians' (use 9.6%, tuition 8.7% at θ = 1, Pell 6.7% at
  intensity 0.980 for the race) [DEGRADED: Asian for Indian]. IPEDS counts students on visas apart ("U.S.
  nonresident"), while the CPS counts those living in households among Asians: their use then falls on the race's
  IPEDS share, which leaves them out, so the Indian-origin groups' use term is biased down and their Pell term up
  (visa students draw no Pell) [INFERENCE; not sized]. On oct07 the hospital term, priced beside the central (the white
  lane's hospital bullet), uses the groups' own MEPS records (Asian Indian; the India-born by birthplace).
- The added people's social rows are the v6 pairing's (`sept24_propagation_2026_09_24/derived/oct07/real_costs_totals.json`,
  `lineage_social_rows`; sha256 e84db10b…, committed by its lane at b0a2ccac): the union's
  social rows are $104.7 / 109.2bn on 42.75M (v5 $104.8 / 109.4bn). The Indian-origin groups' social rows do not move.

**Main table on oct07** (accrual, per member, spec 48 / 11; the social rows take any rounding difference so printed
parts add to printed totals):

| Group | Fiscal | Social rows | **Total** | Total, $bn | oct05 total (IPEDS keys) |
|---|---:|---:|---:|---:|---:|
| Indian-origin, actual ages (6.08M) | −12,144 / −10,777 (SE 1,163 / 1,152) | +1,243 / +1,330 | **−10,901 / −9,447** | −66.3 / −57.4 | −10,843 / −9,392 |
| Indian-origin, third-plus white ages | −10,095 / −8,806 (SE 1,060 / 1,047) | +1,453 / +1,510 | **−8,642 / −7,296** | −52.5 / −44.4 | −8,555 / −7,211 |
| India-born only, actual ages (4.28M) | −12,347 / −10,922 (SE 1,108 / 1,092) | +888 / +990 | **−11,459 / −9,932** | −49.1 / −42.5 | −11,362 / −9,838 |
| India-born only, white ages | −7,687 / −6,410 (SE 987 / 976) | +1,255 / +1,328 | **−6,432 / −5,082** | −27.5 / −21.8 | −6,350 / −5,003 |
| Mexican-origin union (engine), 42.75M | +9,101 / +10,794 | +2,449 / +2,555 | **+11,550 / +13,349** | +493.8 / +570.7 | +11,581 / +13,349 |
| Mexican-origin union, white ages (identified 39.71M) | +9,570 / +11,134 | +2,440 / +2,538 | **+12,010 / +13,672** | +476.9 / +542.9 | +12,116 / +13,780 |
| Third-plus NH whites (a 42.75M slice) | +353 / +1,607 | +2,238 / +2,277 | **+2,591 / +3,884** | +110.8 / +166.1 | +2,717 / +4,008 |

[DATA: `derived/oct07/combined.csv`, `derived/oct05/combined.csv`; the rounding in a scratch tabulation]

- **What the IPEDS keys do here** ($bn, oct07, low / high; `derived/oct07/ipeds_terms.csv`): Indian-origin Pell
  +0.45, use −0.75, the college stock −0.07 / −0.11, tuition +0.28, in all −0.09 / −0.13 (−$15 / −21 per member), and
  the hospital term beside −0.49 (−$81); India-born +0.27, −0.45, −0.04 / −0.07, +0.17, in all −0.05 / −0.08, the
  hospital term beside −0.05. On oct05, without the tuition term, −0.37 / −0.41 and −0.22 / −0.25. The white slice's
  cost falls by more per member ($110 / 112, mostly Pell), so the Indian-origin group's lead over whites narrows by $95 /
  91 per member. [CALCULATION: `ipeds_terms.csv` over the groups' counts; per-member figures by controlled rounding]
- From v5 to v6 on the same keys the Indian-origin fiscal row improves by $0.36 / 0.34bn: the 2026 path lowers its
  Social Security and Medicare accrual by $0.70bn, schools and colleges rise by $0.40bn (item 4's tuition term, +$0.28bn,
  and retiree health's accrual), and the other lines move −$0.06 / 0.04bn. [CALCULATION: `derived/oct07/rekey_buckets.csv`
  against `derived/oct05/rekey_buckets.csv`]
- On the cash set the union is +$9,639 / +11,568 per member (v5 +$9,642 / +11,528) and the Indian-origin group
  −$15,774 / −14,320 (v5 on the same keys −$15,831 / −14,379). [DATA: `derived/oct07/combined.csv`]
- The rough method on the union, both sides with the added people, is 1.6% above the engine at the low end ($395.4bn
  against $389.1bn) and 1.8% below it at the high end ($453.4bn against $461.5bn); on the identified 39.71M at v6's
  responses ($375.1 / 423.9bn against $368.7 / 432.0bn) 1.7% above and 1.9% below.
- The pooled second generation moves the total by $135 / 136 per member, as before (−10,766 / −9,311).

**Gates.** `rekey_indian.py --case oct07`: 186 gates, exit 0 (oct05 on the IPEDS keys: 155). Beside the oct05 gates:
the union, A1 and NH Black rows reproduce the white and Black lanes' `rekey_summary_oct07.csv` (5e-5); the IPEDS terms'
cost is the summary's for each group, basis and end (5e-5), and the library's parts add to each move (1e-9).
`social_rows.py --case oct07`: 25 gates, exit 0 (the v6 pairing prices the added people on exactly this lane's items,
and its union rows are this lane's restated rows, 1e-6). The rerun of `rekey_indian.py` that added `ipeds_terms.csv`
rewrote every other oct05 and oct07 file byte for byte.

**Reproduce (oct07)**, after the oct05 list (now after the white lane's `ipeds_keys.py`) and the white and Black
lanes' oct07 runs:

```sh
L=infra/immigration-fiscal/indian_full_account_2026_09_29
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/accrual_indian.py --case oct07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/rekey_indian.py --case oct07
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/social_rows.py --case oct07
```

New: `derived/oct07/` with `accrual_ratios.csv`, `rekey_summary.csv`, `rekey_buckets.csv`, `rekey_replicates.csv`,
`keys.csv`, `age_structures.csv`, `drivers.csv`, `ipeds_terms.csv`, `social_rows.csv` and `combined.csv`;
`derived/oct05/ipeds_terms.csv`, and `derived/oct05/`'s `rekey_summary.csv`, `rekey_buckets.csv`,
`rekey_replicates.csv` and `combined.csv` rebuilt on the IPEDS keys. `accrual_indian.py`, `rekey_indian.py` and
`social_rows.py` gained `--case oct07`; `rekey_indian.py` gained the IPEDS race map and the parts file.

### Log (times from `date`)

- 2026-10-07 13:10:37 (file time): `accrual_indian.py --case oct07`.
- 15:18:00–15:19:13 (file times): `rekey_indian.py --case oct05` and `--case oct07` on the IPEDS keys (gates pass).
- 15:32:59 (by `date`): rerun with `ipeds_terms.csv` added; every other output byte for byte the same.
- 15:41:17 (by `date`): `social_rows.py --case oct05` (`combined.csv` moves with the fiscal rows; `social_rows.csv`
  does not) and `--case oct07`.
- After 15:41 the team lead decided that item 4's hospital term comes out of every comparator's central on oct07 and
  stays beside (the white library's `HOSPITAL_ON = False`). v6 is final.
- 16:42:47–16:45:11 (by `date`): `rekey_indian.py` and `social_rows.py`, `--case oct05` and `--case oct07`, in place,
  exit 0 (155, 25, 186 and 25 gates). oct05: only `ipeds_terms.csv` changes (it gains the beside columns; its values
  do not move). oct07: `rekey_summary.csv`, `rekey_buckets.csv`, `rekey_replicates.csv`, `ipeds_terms.csv` and
  `combined.csv` change; `social_rows.csv` does not. The pairing's oct07 file is sha256 e84db10b…, as committed at
  b0a2ccac.
- 17:02:24–17:06:27 (by `date`): `rerun_lane.py` with all eleven commands (the six of the default list, the two oct05
  ones and the three oct07 ones), after the white and Black lanes' final reruns: **IDENTICAL 41/41, exit 0**; the
  pairing's file read e84db10b… at the start.

## v6 round 2: income taxes on the case's own keys (oct05, oct07), 2026-10-07

[2026-10-07, round 2: every group's income taxes now take the case's own keys (the white lane's section "v6 round
2"). Under them, Indian-origin residents benefit other residents by **$11,436–12,890 per member a year** on the
accrual basis, $69.5–78.4bn in all. On the CPS-dollar rule, which charged each group only the income tax it reports to
the CPS, the figures were $9,447–10,901 and $57.4–66.3bn. The group pays $12.09bn more income tax, $1,988 per member.
Third-plus whites on 42.75M now cost others **$1,038–2,332 per member** with their social rows (was $2,591–3,884), and
the engine's union $11,550–13,349, as before. The Indian-origin group is **$13,768–13,928 per member better than
whites** and **$24,440–24,785 better than the union**. The fiscal row's sampling error rises from $1,163 to $1,971.
[CALCULATION: `rekey_indian.py --case oct07`, `social_rows.py --case oct07` → `derived/oct07/combined.csv`,
`rekey_summary.csv`, `income_tax_keys.csv`]]

claude-opus-5-5 (prop-d)

**Rules.** The white lane's section "v6 round 2" applies:
- Federal income tax takes v4 item 3's IRS-raked key, and state and other personal taxes take the state-liability key.
- Both ends use the shared allocation, with the personal one beside.
- No group takes a union-only correction.

`evaluate()` now takes the library's central. The summary carries the CPS-dollar rule (`cost_cps_*`) beside the
proportional spread. [INFERENCE] The pooled second generation scales the case's keys by the rough keys' pooled ratios,
because `pooled_asec.py` measures the tax-unit split of FEDTAX_AC and STATETAX_A, not FEDTAX_BC. The Indian-origin
federal share goes from 0.0305 to **0.0350** (+14.7%) and its state share from 0.0333 to 0.0357. [DATA:
`derived/oct07/income_tax_keys.csv`]

**Main table on oct07** (accrual, per member, spec 48 / 11; the social rows take any rounding difference so printed
parts add to printed totals):

| Group | Fiscal | Social rows | **Total** | Total, $bn | CPS-dollar rule total | oct05 total |
|---|---:|---:|---:|---:|---:|---:|
| Indian-origin, actual ages (6.08M) | −14,132 / −12,765 (SE 1,971 / 1,960) | +1,242 / +1,329 | **−12,890 / −11,436** | −78.4 / −69.5 | −10,901 / −9,447 | −12,831 / −11,380 |
| Indian-origin, third-plus white ages | −12,028 / −10,739 (SE 1,654 / 1,642) | +1,453 / +1,510 | **−10,575 / −9,229** | −64.3 / −56.1 | −8,642 / −7,296 | −10,488 / −9,144 |
| India-born only, actual ages (4.28M) | −13,663 / −12,237 (SE 1,517 / 1,501) | +888 / +990 | **−12,775 / −11,247** | −54.7 / −48.2 | −11,459 / −9,932 | −12,677 / −11,153 |
| India-born only, white ages | −8,964 / −7,687 (SE 1,232 / 1,220) | +1,255 / +1,328 | **−7,709 / −6,359** | −33.0 / −27.2 | −6,432 / −5,082 | −7,627 / −6,280 |
| Mexican-origin union (engine), 42.75M | +9,101 / +10,794 | +2,449 / +2,555 | **+11,550 / +13,349** | +493.8 / +570.7 | +11,550 / +13,349 | +11,581 / +13,349 |
| Mexican-origin union, white ages (identified 39.71M) | +9,548 / +11,112 | +2,440 / +2,538 | **+11,988 / +13,650** | +476.1 / +542.1 | +12,010 / +13,672 | +12,095 / +13,758 |
| Third-plus NH whites (a 42.75M slice) | −1,200 / +54 | +2,238 / +2,278 | **+1,038 / +2,332** | +44.4 / +99.7 | +2,591 / +3,884 | +1,164 / +2,456 |

[DATA: `derived/oct07/combined.csv`, `derived/oct05/combined.csv`; the CPS-dollar column is the v6 section's table;
rounding by a scratch tabulation, which reproduces that table from the pre-round-2 files]

- **The key's move, per member** (`income_tax_keys.csv`, the case's key less the CPS-dollar rule):
  - Indian-origin pays +$1,988 more and India-born +$1,315.
  - The union pays +$381 more on its identified 39.71M and +$402 at white ages.
  - Third-plus whites pay +$1,553 more.
  - On the printed totals, the Indian-origin group's lead over whites widens by $436 / 437 per member, and its lead
    over the union by $1,989.
- **The proportional spread** (the 'prop' rule beside the central) gives the Indian-origin fiscal row −$14,763 / −13,397.
  The case's key falls between the CPS-dollar rule (−$12,144 / −10,777) and that spread.
- **The personal allocation** hardly moves the Indian-origin group (−$43 per member), but it moves the India-born rows a
  lot. Under it, India-born residents pay $5,421 more per member, and $1,978 more at white ages, because the shared
  allocation gives their US-born children part of their household's tax. The class-of-worker adult rows move more:
  wage and salary adults by $8,617 and the self-employed by $40,301. [CALCULATION: `income_tax_keys.csv`, personal less
  shared amounts; the sum is exact because each income-tax line's response is 1]
- **Sampling error.** The fiscal row's SE rises from $1,163 / 1,152 to $1,971 / 1,960, and the self-employed
  households' from $11,873 to $25,033. [INFERENCE] The raked key puts the top AGI cells' tax on few records, and the
  Indian-origin group holds many of them. The 160 replicates re-key the group's own weights on the fixed key vector
  (national totals held, as before).
- **The cash set.** The union is +$9,639 / +11,568 per member, unchanged, and the Indian-origin group −$17,762 / −16,308
  (was −$15,774 / −14,320).
- **The rough method on the union**, both sides with the added people, is 2.3% below the engine at the low end ($380.3bn
  against $389.1bn) and 5.0% below at the high end ($438.3bn against $461.5bn). On the identified 39.71M at v6's
  responses it is 2.4% and 5.4% below ($360.0 / 408.8bn against $368.7 / 432.0bn). The case scales the union's own
  income taxes by its tax-records stack, and at the high end gives each earner their own tax; the comparators take
  neither (the white lane's round-2 section).
- **Unchanged parts.**
  - The pooled second generation moves the total by $167 / 168 per member (−12,723 / −11,268); it was $135 / 136.
  - The IPEDS terms' parts do not move.
  - From v5 to v6 the Indian-origin fiscal row still improves by $0.36 / 0.34bn.
  - The social rows do not move.

**Gates.** `rekey_indian.py --case oct07` passes 193 gates and exits 0; `--case oct05` passes 162. The new gates are
the library's round-2 gates. The union, A1 and NH Black rows reproduce the white and Black lanes'
`rekey_summary_<case>.csv` (5e-5), and the IPEDS terms' cost is the summary's (5e-5). `social_rows.py` passes 25 gates
per case. The pairing's oct07 file is still sha256 e84db10b….

**Files.** New: `derived/oct05/income_tax_keys.csv` and `derived/oct07/income_tax_keys.csv`. Changed, for both cases:
`rekey_summary.csv` (it gains `cost_cps_bn` and `cost_cps_per_member`), `rekey_buckets.csv`, `rekey_replicates.csv`,
`ipeds_terms.csv` (levels only) and `combined.csv`. `social_rows.csv`, `keys.csv`, `age_structures.csv` and
`drivers.csv` do not move. The reproduce list is the v6 section's.

### Log (round 2; times from `date`)

- 2026-10-07 20:20:34–20:22:34 (by `date`): `rekey_indian.py` and `social_rows.py`, `--case oct05` and `--case oct07`,
  ran in place, exit 0 (162, 25, 193 and 25 gates; peak memory 2.36 GB).
- 21:10:21–21:14:47 (by `date`): `rerun_lane.py` with the v6 section's eleven commands, after the white and Black
  lanes' round-2 reruns: **IDENTICAL 43/43, exit 0**, the 41 v6 files and the two `income_tax_keys.csv`; the
  pairing's file read e84db10b… at the start.
- 21:51:23–21:57:07 (by `date`): the same rerun after the white library relabelled the columns of its CPS-totals file:
  **IDENTICAL 43/43, exit 0**; the pairing's file again read e84db10b….

## v7 propagation (oct14), 2026-10-14: Indian R7 policy required

The live default is oct14. The three routes now target v7 and preserve all oct07/oct05 outputs: accrual_indian.py uses the 2026 separate-funds path and this case published-weight pension metadata, writing derived/oct14/accrual_ratios.csv; rekey_indian.py uses the completed white/Black v7 library and personal ends; social_rows.py selects the committed oct14 pairing. All existing gates retain their tolerances.

The first oct14 re-key reached the inherited gates but stopped at the absent accrual-path map (KeyError oct14). That map is repaired. It now preflights every Indian scenario against the R7 policy before pricing or writing. The source item supplies no Indian factor, and the old shared helper would silently select white_nh. That fallback is removed, with 12 regression tests including all seven unsupported Indian aliases. Both re-key and social scripts exit 1 before writing. [CALCULATION: rekey_indian.py --case oct14; social_rows.py --case oct14; white test_job_policy_oct14.py]

**STOP / parent question:** what R7 rule applies to Indian-origin and India-born people, their worker/household subgroups and age/replicate variants? A measured Indian factor or an explicitly approved labelled proxy is needed for ind, ind1, ind1se, ind1wage, ind1oth, hhse and hhwage. The IPEDS Asian proxy does not supply a job-capital policy. No Indian oct14 fiscal, social or combined figure is claimed.

Live commands after the policy is resolved: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/accrual_indian.py --case oct14; then rekey_indian.py --case oct14; then social_rows.py --case oct14, followed by rerun_lane.py with all three. Historical reproduce blocks are prior receipts. The independent accrual leaf may be rerun with explicit allow-unrun for the two stopped consumers; that cannot imply full-lane completion.

- 2026-10-14 19:17 JST — the independent 2026 accrual leaf exits 0; union ratio/timing/Part A/HI-tax source gates pass. Initial run 27.13s, max RSS 539.9MiB; leaf-only rerun IDENTICAL 44/44, exit 0, 23.17s, max RSS 532.5MiB. The two stopped fiscal/social consumers are explicitly allow-unrun; this is not a full-lane pass. Their guarded runs both exit 1 before writes. All three modified Python sources compile. [CALCULATION: accrual_indian.py --case oct14; wave-2 leaf rerun and guarded-stop receipts]

## 2026-10-14 round 3: measured Indian job-capital factors

The parent authorized measurement on this lane's own persons, rather than a comparator proxy. The factor is
`sum(industry wage share * national industry tax) / line national / plain wage share` at the personal allocation.
`job_capital_factors.py` imports the source lane's industry mapper read-only and reads its national per-industry
vectors and crosswalk. This frame has the same CPS ASEC 2025 `INDUSTRY` codes; a gate checks its person columns
against the original raw rows before adding industry and class-of-worker data. `LJCW` government's overrides,
source thin-cell pooling, national spreading of wages >=$1M, mining at zero and residential exclusion all match
the source construction. Each Indian alias, worker/household group and age variant gets its own factor.
[CALCULATION: `rekey_indian.py --case oct14` → `derived/oct14/job_capital_factors.csv`]

The same function on the job-capital lane's frame reproduces its committed `white_nh` personal factors at
**1e-9** on every line; the maximum absolute error is **2.22e-16**. The national vectors also reproduce each
source item's `base_bn` at 1e-9. Own-age Indian-origin factors are corporate **1.2929556573920054**,
business property **0.8201939140519006**, and other production taxes **0.5516237966530695**.
All 160 own-group replicate weights are available: the factor is remeasured in each, with national weights
held fixed as this lane holds its other national keys fixed. The three factors travel in `rekey_replicates.csv`;
there is no unpropagated-factor approximation. Both readings retain the case's responses, corporate **1 / 0.37**.
[CALCULATION: `job_capital_factors.py`; `derived/oct14/job_capital_gates.json`, `job_capital_factors.csv`]

The scenario adapter is installed at the library's `run29` consumer, covering the fiscal, IPEDS and replicate
paths; it restores `job_factor` after each call even on failure. The white library and job-capital source lane
remain read-only. No mixed-credit counterpart is invented; previously documented external-key limitations remain.

Indian-origin own-age modeled costs, $bn, low / high (negative means a net benefit to other residents):

| Basis | Fiscal | Social | Combined |
|---|---:|---:|---:|
| Accrual | −126.2293 / −98.8827 | 7.5542 / 8.0828 | −118.6751 / −90.7999 |
| Cash | −155.7943 / −128.4476 | 7.5542 / 8.0828 | −148.2401 / −120.3648 |

[CALCULATION: `derived/oct14/combined.csv`, group `indian_origin`; model outputs, not measured removal effects]

Initial fiscal run: **218 PASS gates**, exit 0, 85.73s, peak RSS 1782.6MiB. Social run: **25 PASS gates**, exit 0,
0.50s, 103.7MiB. All inherited numerical gates remain, including exact engine/identified-union checks (1e-9),
white/Black parity (5e-5 for printed CSVs), white-age identity (1e-12), IPEDS decomposition (1e-9) and the existing
India-born partition tolerance (0.05bn, group state-price products). Independent scoped code review found no material
defect and reran the positive control successfully. Full reproducibility receipt follows after the final run.

Live reproduce commands (historical blocks above remain receipts):
```
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/job_capital_factors.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/accrual_indian.py --case oct14
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/rekey_indian.py --case oct14
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/social_rows.py --case oct14
```

- 2026-10-14 19:44 JST — full live reproducibility: all four commands above exit 0;
  **IDENTICAL 57/57, exit 0**, 89.79s, Python child peak RSS **2222.9MiB**. All archived outputs remain unchanged.

## Live v8 propagation (oct15)

The live accrual, fiscal and social commands now target oct15 and write `derived/oct15/`.
Indian job-capital factors remeasure the source's `foreign_source_removed` industry vector on
each group's own weights, including all 160 replicate weights. A separate white positive control
checks the K2 source factors at 1e-9. Items 10 and 11 apply to the measured Mexican lineage;
they have no invented Indian counterparts. Comparator coverage follows the shared comparator
library's declared policy. The social route requires the completed oct15 pairing explicitly.

```sh
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/job_capital_factors.py --foreign-source-removed
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/accrual_indian.py --case oct15
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/rekey_indian.py --case oct15
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/indian_full_account_2026_09_29/social_rows.py --case oct15
uv run --no-project python3 scripts/rerun_lane.py infra/immigration-fiscal/indian_full_account_2026_09_29 "uv run --no-project python3 {lane}/job_capital_factors.py --foreign-source-removed" "uv run --no-project python3 {lane}/accrual_indian.py --case oct15" "uv run --no-project python3 {lane}/rekey_indian.py --case oct15" "uv run --no-project python3 {lane}/social_rows.py --case oct15"
```

- 2026-10-14 23:50 JST — Initial accrual probe stopped on unsupported oct15. Added live
  mappings and K2 own-industry calculation. Candidate K2 positive control exits 0, maximum
  factor discrepancy 2.22e-16; final case runs wait for CASE_FINAL. [CALCULATION: indian-candidate.log; indian-k2-probe.log]
  The first successful harness (134.77s) peaked at 2579.7MiB; isolating the source's 161-weight-column
  positive-control frame in a subprocess reduced the final peak without changing any output. The subprocess
  fails loudly on a failed control and returns the same three numerical receipts. The final harness above
  covers this resource fix. Frozen-case, archived-output, factor/replicate coverage, combined-table closure,
  source syntax, CSV LF and scoped whitespace checks pass. No Git writes.

### 2026-10-15 Round-2 rules

The headline lineage stays on whole-population mortality. The Indian accrual route also uses
whole-population survival with its own careers and eligibility; no Indian-specific mortality
schedule is measured here. Comparative oct15 rows explicitly carry case/mortality labels and
state that Indian mortality remains whole-population. Fully own-mortality Indian comparisons
remain unmeasured. The white/Black symmetric lane owns the requested two-convention annual
contrasts; its scalar lineage mortality adjustment does not identify an Indian mortality
schedule or a historical borrowing path. [DATA: accrual_indian.py; SOURCE: parent round-2 rules]

Item 9 is additionally reported on the two evaluated corporate receipt lines in
`derived/oct15/item9_own_job_lines.csv`: each Indian scenario takes its own before/after
industry-weighted factors, with unchanged national totals and responses, and the line effects
must reproduce its total cost change at 1e-9bn. New unit probes: 6 pass; K2 source positive
control exits 0 in 5.970s. No final oct15 figure or reproduction is claimed before CASE_FINAL.
[CALCULATION: test_job_source_scope.py; indian-k2-resume.json]


### Round-2 comparator fixes: live source engine (2026-10-15)

Before, the union-at-white-ages combined row added the rough age difference to the case fiscal level. For oct15 it now retains its own rough fiscal level, with the case-versus-rough bridge quoted in a separate column. Live fiscal input/output rows carry their source engine tag; the social consumer rejects missing/wrong source tags, and the age contrast requires two rough-engine tags. Archived calibration/rows are preserved. These are absolute source rows, not a newly invented historical mortality or Black stock comparison. [SOURCE: parent one-engine follow-up; CALCULATION: rekey_indian.py, social_rows.py]

Absolute principal amounts are preserved. The live rough age-comparison row now quotes both the full-lineage and identified-union case/rough bridges and the removed level calibration separately. test_social_engine.py verifies principal preservation, live calibration removal and archived behavior without loading live data. The focused Indian check is: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest -p no:cacheprovider infra/immigration-fiscal/indian_full_account_2026_09_29/test_social_engine.py infra/immigration-fiscal/indian_full_account_2026_09_29/test_job_source_scope.py -q (7 passed). Add the same explicit test command to the live rerun after CASE_FINAL. [CALCULATION: changed caller and fixture tests]


### Correction: mortality labels on the base route (2026-10-15)

The earlier mixed-mortality label was wrong for this base route. Plain K.run29 consumes the base general-mortality ratios; white rekey_sept29.py write() labels these diagnostic rows whole-population mortality. group_lines.py now inherits that actual upstream label and rejects missing, own-group or mixed labels. Legacy financing rows inherit the gated group-line label; Indian base references must both have the same authoritative general label. Indian mortality is independently traced: accrual_indian uses A.G (the white producer's P.CENTRAL mortality=general), passes that grid/default Part-A mortality to A.oasdi_ratio/A.part_a, and now gates G[1]=general on the live route. Its CSV's explicit whole_population_tables label is checked before downstream rekeying. Indian combined rows inherit their gated fiscal input label; pure social terms have not_applicable_social_terms. Pension employee-service stock rows retain not_applicable_service_share.

Canonical display labels load mortality_conventions.py; no copied definition is introduced. The symmetric producer separately supplies its mixed/own-group convention comparisons; base diagnostic rows do not claim to be either of those. General-mortality inheritance and missing/wrong-label negative controls pass. Three legacy fixture probes and seven Indian source/level probes pass; changed callers compile. Historical rows and logs remain, with this dated correction superseding their misleading current-label statement. [DATA: white_replacement_2026_09_28/rekey_sept29.py write(), accrual_white.py G/part_a; pension_accrual_2026_09_28/pension_accrual.py CENTRAL; owned callers/tests]


### Adopted v8 independent fiscal receipt and social stop, 2026-10-15

CASE_FINAL b35ac8fb inspected. Independent job-factor/accrual/fiscal producers and7fixturetests reproduce IDENTICAL71/71,exit0,148.918s (Python perf_counter/resource; child RSS1,915,715,584bytes informational). social_rows.py is explicitly allow-unrun in this independent-only receipt; no full-lane PASS is claimed. Earlier direct fiscal rekey82.748s with2.278GB physical peak; accrual26.629s. Principal absolute case-lineage fiscal amounts remain368.9909 /459.2029bn (set),284.9516 /375.1635bn(cash). Indian-origin fiscal−120.3087 /−96.6921bn on set,−149.8736 /−126.2570bn on cash are model results under the declared general mortality and own-job source rules; inspect rekey_summary.csv for printed precision. [CALCULATION: derived/oct15/rekey_summary.csv,accrual_ratios.csv; scratch indian-leaf-repro.json]

Actual social consumer exits1 before writing social_rows.csv or combined.csv. The new pairing explicitly identifies lineage_social_rows as P7 sender/recipient-boundary rows before environment, and v8_social_environment.current_social_rows as current replacements on frozen v7 source keys, with completion/coverage social effects unpriced. These are different estimands from this lane's preserved restated pair_value baseline: victims high39.008480793656645 vs31.873558bn (+7.134922793656646); private security low+0.49405030321520194 vs−0.490639bn. Old equality gate1e-6 is retained; no measured Indian incidence is fabricated. Missing rule: each Indian-origin/India-born/subgroup/age scenario's sender/receiver boundary and environment replacement incidence, and explicit transport for new completion/coverage people. Affected output rows: every live social item/group and their combined fiscal+social totals, including lineage/white-age rows that share that baseline. Independent fiscal rows remain valid outputs; pure social/combined outputs are withheld. Parent confirms no declared transport within scope. [DATA: ../sept24_propagation_2026_09_24/derived/oct15/real_costs_totals.json; CALCULATION: scratch indian-social-final.log]

At the inspected pairing snapshot79329619e41cd39afa8c3882abe97250aae8661462d49cc196cd95574be62e22,30/31sources match; conditional_stacks.csv had changed from stored1bcdc243e6811d4b3b20bdec364c9f32e62922eb9e0af744013b7c01f620b781 to5c8d64eb428d7bc1543a5bd7e0e6b1fccc5018bfcda990460013ad97d45f99e3 during peer refresh. This additional source-order staleness is distinct from the independently demonstrated semantic stop and reported to the parent for regeneration. No stored hash edited.

## R2C40 final receipt — 2026-10-15T03:58:49+09:00

Own-mask comparator item11 is now measured and applied post-evaluator, with pinned paired gap SEs. [FRAMING-SENSITIVE] The labeled one-sided gap is preserved immediately below the measured row. Full White 210/210, full Black 96/96, C8 source-only 77/77, legacy annual-only 39/39, pension 43/43, Indian independent fiscal 71/71: all IDENTICAL, exit 0. Exact baselines unchanged; no feedback into M5; no annual charge to legacy stock. Break tables and Indian social/combined rows remain withheld. [CALCULATION: parent scratch c40-*-rerun.json/log; c40-validation.json; prop-d-result.md]

Log: 2026-10-15 06:19:49 JST (`date`, parent): rerun on corrected v8 (`d1a24d47`: the coverage term no longer charges the missed people's custody, arrests and ICE a second time, −$3.199004 / −$3.221092bn on the lineage), IDENTICAL 71/71, exit 0. The Mexican-origin reference rows fall by the correction (engine $368.9909 / 459.2029bn → $365.7919 / 455.9818bn; rough $345.2043 / 433.3482bn → $342.0053 / 430.1271bn); the Indian-origin rows are unchanged.

Log: 2026-10-15 08:40:26 JST (`date`, parent): rerun on round 3's comparator code (4548e70f), IDENTICAL 71/71, exit 0. The white library's school key now keys every record on its own cell's October public K-12 rate at state spending per pupil; the Indian-origin and India-born records take the cell for everyone outside the Mexican-origin, Black and white cells [ASSUMPTION: their enrollment equals that cell's at each age band]. Indian origin, accrual: −$120.3087 / −96.6921bn → **−$118.7802 / −95.1202bn**; India-born −$111.6166 / −92.0045bn → −$111.1243 / −91.4982bn; the rough Mexican-origin reference +$2.4185 / 2.4869bn; the engine reference is unchanged ($365.7919 / 455.9818bn). [DATA: derived/oct15/rekey_summary.csv]

### R4C4 downstream receipt — 2026-10-15 10:38:53 JST (`date`)

Independent job-factor/accrual/fiscal producer and seven source fixtures reproduce **IDENTICAL 71/71, exit 0**, 136.056s. `social_rows.py` is explicitly allow-unrun in that receipt; its direct probe still exits 1 on the existing v8 pairing/restated-social estimand mismatch (maximum about 7.1bn). No consumer code change or gate relaxation was needed. Indian-origin accrual remains −118.7802 / −95.1202bn, India-born −111.1243 / −91.4982bn under their declared general mortality; item11 on the Indian masks remains unmeasured. Independent fiscal PASS does not authorize social/combined publication. [CALCULATION: derived/oct15/rekey_summary.csv; scratch prop8/c4fix-indian-{social-probe,rerun}.log]
