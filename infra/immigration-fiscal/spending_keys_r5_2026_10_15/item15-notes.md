**Verdict:** The conditional public-college net-consumption response is **0.885774850**, with the same split imposed on college capital. The measured finance functions do not identify a unique NIPA bridge or a causal enrollment elasticity. This response assigns the measured public-service residual response 0 under the parent's rule; it does not subtract all research expenses from a consumption total that has already excluded R&D production. [CALCULATION: `college.py`, `derived/item15.json`; FRAMING-SENSITIVE]

## Measured inputs and scope

The dataset register's IPEDS entry routes to the adopted fee lane. Its pinned FY2022–23 GASB finance archive, joined to public institutions in HD2023 in the 50 states/DC, yields **1,888 finance units**. This includes system offices without students; the bridge concerns the government-wide functional budget, whereas the existing use key was estimated from instruction-related costs at units with enrolled students. Missing amounts become zero only when their primary imputation flag is **A, not applicable**; other missing flags stop. Source hashes and zero counts travel in the item. [DATA: staged `F2223_F1A.zip`, `HD2023.csv`; primary finance dictionary]

| FY2022–23 public GASB function or revenue | $bn |
|---|---:|
| Instruction | 122.507638 |
| Academic support | 36.980972 |
| Student services | 25.579797 |
| Institutional support | 42.201003 |
| Instruction and support total | 227.269410 |
| Separately budgeted research | 48.477133 |
| Public service | 20.128745 |
| Auxiliary expenses / sales | 37.386138 / 30.431445 |
| Hospital expenses / sales | 72.302772 / 76.509152 |
| Other expenses and deductions | 36.389489 |
| Scholarships / independent operations | 19.631929 / 2.249081 |
| Net tuition / Pell / tuition discounts | 81.036563 / 18.010168 / 34.636820 |
| Sales incidental to educational activities | 15.475699 |
| Federal / state / local-private operating grants | 40.994680 / 11.771512 / 17.207050 |
| Total expenses | 463.834697 |

These are institutional expenses, not interchangeable with NIPA consumption. Academic support serves instruction, research and public service; the parent's rule nevertheless assigns its whole block response 1. Operations/maintenance are already allocated to the functional expenses; the separately reported natural expense total must not be added a second time. Pell in the revenue bridge follows the adopted fee lane's net-tuition-plus-Pell convention. Pell transfers keep their own beneficiary response. [SOURCE: [NCES finance file](https://nces.ed.gov/ipeds/datacenter/data/F2223_F1A.zip), [finance dictionary](https://nces.ed.gov/ipeds/datacenter/data/F2223_F1A_Dict.zip); DATA: `measured_totals_bn`]

The NIPA principal-source check independently rereads the pinned BEA workbook: S&L higher-education consumption **$229.963bn**; all-education tuition/related charges **$103.911bn**; the adopted fee lane's allocation of federal education produces a consolidated higher-education exposure **$234.029706938bn**. These must reproduce the fee payload to 1e-9bn. [DATA: BEA `Section3All_xls.xlsx`, T3.16 line 108, T3.10.5 line 58; `read_primary_nipa()`]

## Gross cost, sales and net consumption

BEA removes own-account investment and sales from government gross output. Government-funded R&D is investment; federal purchases of S&L R&D also sit in S&L sales. Thus a separately reported research expense is not, by itself, an invariant component still inside higher-education consumption. The central bridge leaves research production outside consumption. The broad operating-grant fields include non-research programs, so the calculation does not subtract every grant from the remaining public-service budget. [SOURCE: [BEA NIPA Handbook chapter 9](https://www.bea.gov/resources/methodologies/nipa-handbook/pdf/chapter-09.pdf), pp. 9-5–9-6 and 9-21–9-22]

The Census source classification routes university hospitals to hospitals, agricultural experiment/extension activities to natural resources, and auxiliaries separately from the core college function. Public service contains extension as well as broadcasting, advisory and other services. The available public-service aggregate does not separate their NIPA destinations. Hospitals' **−$4.206380bn** net is shown beside; it is not allowed to reduce the education denominator or appear again on health. Auxiliaries enter centrally only at their **$6.954692bn** net. [SOURCE: [Census Government Finance Classification Manual](https://www2.census.gov/govs/pubs/classification/2006_classification_manual.pdf), pp. 5-22–5-23; DATA: primary finance totals]

The explicit central conditional bridge, in $bn, is:

```
gross in scope = 227.269410205 instruction/support
              + 20.128745339 public service
              + 37.386137581 auxiliary expense
              + 36.389489254 unclassified other
              = 321.173782379
sales         = 99.046731354 net tuition + Pell
              + 30.431445385 auxiliary sales
              + 15.475698800 educational-activity sales
net           = 176.219906840
invariant     = 20.128745339 public service
responsive    = 156.091161501
r_N           = responsive / net = 0.8857748497320679
```

The exact numerical gross and auxiliary fields are in `derived/item15.json`; printed fragments are rounded. The measured IPEDS net **does not equal** the NIPA control. The central transports its functional net shares proportionally to NIPA, scale **1.304977424** on the S&L control. This scale is an explicit bridge assumption, not observed 2023→2024 growth. It bundles fiscal/calendar timing, GASB/FASB coverage, sales scope, accounting adjustments, interest exclusion, and other unresolved differences. Unclassified other is responsive centrally, with a fixed arm; no claim is made that its $36.39bn is all instruction. Functional interest is unavailable; a separate arm removes all $8.626211bn institutional interest from other before rebridging. [CALCULATION; ASSUMPTION]

## Apply the item without changing fees

Let `U` be the existing college gross-use key, `N` the account's college net exposure, and `T` tuition. Before this item, the group's burden is `U*N + (U−s_R)*T`; afterward it is `r_N*U*N + (U−s_R)*T`. The item therefore changes operating cost by `(r_N−1)*U*N`, while keeping tuition loss and the adopted fee correction at response 1. Applying `r_N` to the whole prior burden would incorrectly reduce lost tuition. [DERIVATION; test `test_central_net_bridge_closes_and_preserves_tuition`]

At the adopted union key **U=0.11589579410930383**, the operating change is **−$3.098135459bn** in both sets at both ends, before additional descendants, completion, coverage and capital. The national use-cost change is **−$26.732078442bn**. The existing union tuition correction **+$1.844604621bn** is held fixed. These are not the whole-v8 item totals; the parent's evaluator adds those typed pieces. [CALCULATION: `build_item()`]

College capital follows the same response centrally by parent instruction. Its expense-mix arm instead includes research and public-service facilities at response 0, yielding **0.814403602**. No function-specific asset-stock measurement supports either proxy. The existing capital key includes some library/other stock: `U_capital=0.11681188165681472` differs from operating `U`. Added descendants must retain their own use pricing. The parent may recover added-use amounts from typed college capital keys, but that remains a stated transport assumption; applying the union's U uniformly to all added people is not a measured key. [DATA: adopted fee payload; ASSUMPTION]

## Bridge arms

| Assumption varied from conditional central | r_N |
|---|---:|
| Central | 0.885775 |
| Unclassified other fixed | 0.679274 |
| All educational-activity sales assigned to public service | 0.973595 |
| All public service outside education | 1.000000 |
| Auxiliaries outside education | 0.881082 |
| All institutional interest removed from other | 0.879896 |
| Tuition net without Pell | 0.896366 |
| Tuition with all discounts added back | 0.873875 |
| Diagnostic: all reported research still in consumption | 0.694674 |

The public-service-outside arm is a scope extreme, not evidence that all public service is agricultural extension. The research diagnostic illustrates the prohibited untraced subtraction and is not recommended for central adoption. No state formula tying separately budgeted research or public service to enrollment was verified; their response remains 0 under the parent rule. Arms are accounting/transport assumptions, not confidence intervals or measured removal responses. [CALCULATION; ASSUMPTION]

## Interactions, validation and coverage

Items 13 and 14 have no direct overlap. Item 9's corporate sourcing and item 10's union completion do not alter the function ratio; completion's college use still changes its exposure. The adopted item 11 source stack recomputes taxes, credits, selected benefits and resource keys; it has no college operating or capital component (`mixed_unit_removal_2026_10_14/round2.py:93–149`). Its amount stays fixed here. Item 12 prices missed people: the adapter applies the function response to their typed college capital/use parts while holding tuition and Pell fixed. Recomputing full education as college would also change school/library costs and is invalid. [CODE; CALCULATION]

`college.py` and `test_college.py` cover this bridge, raw-input pins, principal BEA exposure checks, structural-not-applicable flags, fee-loss preservation, research/hospital scope and named arms. They skip whole-case application and items 13/14, which are owned by the parent and peers. No external acquisition, raw-data edit, Git mutation, or case adoption occurred. Six tests pass; final timed build took **0.778 seconds**, peak RSS **154,075,136 bytes**, measured with Python. Validation timestamp is recorded in `item15-evidence.md`. The full lane's rerun is the parent's responsibility while peer scripts are still being written. [CHECK]
