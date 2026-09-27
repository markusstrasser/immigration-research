claude-opus-5-5

**Verdict:** [2026-09-28: the lineage lane now requires a living parent for each birth (conceptual audit 2026-09-27 §E). Every arm's gap moves by +$8,988 at 0% and +$1,237 at 3%; the parents' channels are unchanged in dollars, and channel shares move by at most 0.2 points. The lineage central is −$1,288,162 / −$513,398. The calibrated arm is −$1,279,450 / −$505,511 against −$1,254,932 / −$493,373 without parents, a channel of 1.9% / 2.4%. At p = 1 the arm is −$1.72M / −$723k, 27.0% / 31.7% of the gap (37.4% / 42.9% if naturalisation is certain). Arm 1 is −$1,276,267 / −$508,723 (adjust in place) or −$1,277,978 / −$509,887 (abroad under the bar). The statutory never-legalised founder with 2026 care is −$890,463 / −$424,717; the child's petition still adds −$386k / −$84k, now 30.2% / 16.5% of the gap. `arms.py` reads the lineage central from the lane's stored rows instead of the constant −1,297,150 / −514,635. Two reruns; the second is byte-identical, and all 125 gates pass.] [2026-09-27, late: the conceptual audit's second pass (§D, ffcce20), verified by the parent
session with `conceptual_audit_2026_09_27/probe_sponsorship.py`, narrows this verdict. "The rate Mexican
citizens actually petition" is a calibrated scenario, not an observed lifetime rate. The 0.619 is today's
naturalized share of the eligible stock, and the two calibration estimators share their admissions numerator
(ratio 1.089). At fixed probabilities, admitting parents in founder-year 10 or 16 lowers the channel from
$24,518 to $21,955 or $15,664 undiscounted.] The sponsored-parent channel is small at the rate Mexican citizens actually petition
and large only if every naturalised founder brings their parents. Calibrated on the IR-5 flow
(p = 0.053, i.e. 0.059 parents admitted per founder who becomes an LPR), a founder who is an LPR
on arrival and sponsors parents aged 60 moves the lineage gap from −$1,263,920 to **−$1,288,438**
undiscounted and from −$494,610 to **−$506,748** at 3%: the channel is **1.9% of the gap (2.4% at
3%)**, range 1.4–5.4% (1.8–6.7%) from the low calibration to the age-bound ceiling. At p = 1 the
gap is **−$1.73M / −$724k**, and the channel is 27% / 32% of it (37% / 43% if naturalisation is also
certain). Legalising the unauthorized founder through their US-born child at 21 (arm 1) lands at
**−$1,285,255 / −$509,960** (adjust in place) or **−$1,286,967 / −$511,124** (ten years abroad
under the bar), within 1% of the lineage lane's central −$1,297,150 / −$514,635, because that
central already gives the never-legalised founder the pooled profile from 65. Against the
statutory never-legalised founder with 2026 care (−$899,451 / −$425,954) the child's petition adds
**−$386k (30% of the gap) / −$84k (16%)**, and −$137k to −$413k across the twelve priced senior
regimes. The ten-year bar barely matters because the founder's balance at 50–59 is near zero.
Attribution [FRAMING-SENSITIVE]: the gap with parents charged to the petitioning lineage is the
figure above; without them it is the p = 0 row. [CALCULATION: `arms.py` → `derived/arms.csv`]

# Sponsored parents in the century lineage (2026-09-27)

Lane: `infra/immigration-fiscal/lineage_sponsored_parents_2026_09_27/`. Brief: `BRIEF.md`. Adds the
family-admission (IR-5) channel to `lineage_cost_2026_09_19` as arms, importing that lane's
machinery read-only. Sections are appended as each step completes.

Provenance tags: [SOURCE] primary or upstream-lane data · [DATA] local file · [CALCULATION]
arithmetic in this lane · [INFERENCE] my reading · [ASSUMPTION] a stated parameter choice ·
[TRAINING-DATA] not re-read here.

## Preregistered arms (written before any arm was run)

Every arm is reported at 0% and 3% real discount, as the lineage gap (Mexican lineage minus the
unchanged white reference lineage) against the lineage lane's central −$1,297,150 (0%) and
−$514,635 (3%), with the channel's share of the arm's gap. All arms use the lineage lane's central
settings (complete account, `personal` allocation, per-capita attribution, low fertility,
generation 29, common US-total life table, no growth, 100 years) unless the arm names a change.
Crime lines are not touched.

**Gate first.** `verify.py` reproduces the lineage lane's central row and its three comparison
rows (senior_full central, statutory bars plus priced care under 2026 rules for a new enrollee,
legalised at year 10) from its own `derived/sensitivities.csv` to 1e-6 dollars, and the
late-arrival lane's `per_admission.csv` statutory/common-total rows from its `late_profile`, before
any arm runs. Any failure stops the lane.

**Arm 1 — the founder legalised through a US-born child at 21.** The first US-born child (G2) is
born in calendar year 4 (founder 29) and turns 21 in year 25, when the founder is 50. Petition to
admission lag 0 (the brief's "at the child's 21st birthday"); a 2-year lag is a sensitivity.
- **1a adjust in place** (founder had a lawful entry, INA 245(a)): LPR at 50. Unauthorized profile
  (with the −$870 working-age penalty) until 50, the pooled Mexico-born profile from 50 — the
  lineage lane's convention for a legalised founder. Variant **1a-bar**: the five-year bar on
  federal means-tested programs at 50–54 (public medical `medical`, `M`, `N` and `noncash`
  replaced by the lineage lane's priced floor scaled to pre-65 ages).
- **1b consular processing and the ten-year bar** (entered without inspection, INA
  212(a)(9)(B)(i)(II); a US-citizen child is not a qualifying relative for the waiver): the
  founder leaves at 50, has a zero US balance at 50–59, and is admitted at 60; pooled profile from
  60, variant **1b-bar** with the five-year bar at 60–64.
- Comparators: never legalised under the statutory bars plus priced care (all four regimes ×
  three cases; central = 2026 rules for a new enrollee, central) and under `senior_full`; and the
  lineage lane's legalised-at-year-10 arm.
- No blend of 1a and 1b unless a sourced share of the Mexican unauthorized stock with a lawful
  entry is found locally.

**Arm 2 — the founder sponsors their own parents.** Parents can be petitioned only once the
founder is a citizen, so the arm runs on founder tracks that pass through naturalisation:
- **L25** founder an LPR on arrival (founder at the Mexico-born average, the lineage lane's
  `mexico_born_average` status), naturalises at 30 (year 5);
- **L10** founder legalised at year 10 (the lineage lane's arm 2b), naturalises at 40 (year 15);
- **L50** founder legalised at 50 through arm 1a, naturalises at 55 (year 30).
Naturalisation probability 0.619 [SOURCE: `origin_attachment_mexico_2026_09_27`, ACS 2024 /
OHSS]. Parents are admitted one year after naturalisation. Parent age at admission = founder age
at admission + a parent–child age gap of 29 (lineage `GEN_LEN`); the grid 55/60/65 is run on L25
(gap 24/29/34). Expected living parents per petition m = 2·l(a0)/l(29) on the common total table.
Expected parents admitted per founder = 0.619 × p × m, with **p = 0, calibrated, 1**.
- **Pricing (i) new arrival:** the late-arrival lane's `statutory` central profile
  (`per_admission.late_profile`, five-year bar, observed late-arrival receipt by tenure), placed on
  the lineage calendar at the admission year, common total survival from a0, cut at year 100.
- **Pricing (ii) eligibility change only** (parent already resident without status): the LPR
  profile minus the same person's profile as an unauthorized resident — no Social Security or SSI
  (42 U.S.C. 402(y), 8 U.S.C. 1611), no federal medical or noncash programs at any age, public care
  at the lineage lane's priced 2026 new-enrollee rules (central) from 65 and its pre-65 scaling
  before 65; taxes and services unchanged.
- **Mixed** (calibrated arm only): already-resident share 0.33 (NIS 2003 Mexican IR-5 who
  adjusted) to 0.72 (FY2024 Mexican immediate relatives who adjusted).
- **Calibration of p.** Two estimators, both reported: (A) stock hazard — Mexican IR-5 admissions a
  year ÷ (naturalised Mexico-born adults + US-born adult children of Mexico-born parents) × mean
  years a petitioner stays in the stock; (B) flow ratio — IR-5 admissions a year ÷ (Mexican
  naturalisations a year + US-born children of Mexico-born parents turning 21 a year). Both give
  parents admitted per eligible citizen, E; p = E / m. Flow numerators: FY2015–2024 mean 36,652
  and FY2024 63,050. Denominators treat naturalised and US-born petitioners as equally likely to
  petition, which is untested.

**Arm 3 — attribution** [FRAMING-SENSITIVE]. (3a) the petitioning lineage owns the sponsored
parents' whole remaining-life cost; (3b) the lineage is descendants only and the parents are
excluded (the lineage lane's definition). Gap reported with and without. Under the calibrated p
the per-citizen E already divides parents among siblings who could petition; under p = 1 the
founder's lineage owns both parents whole.

Outputs: `derived/arms.csv` (one row per arm × discount), `derived/calibration.csv`,
`derived/audit.json`.

---

## Gates (run before every arm; `verify.py`, also inside `arms.py`)

All 125 checks pass [DATA: `derived/gates.csv`]:

| Gate | Checks | Max abs. difference |
|---|---:|---:|
| Lineage lane's stored rows (central 0% and 3%, Mexico-born-average founder, legalised at year 10, statutory bars, all 12 priced-care rows; Mexican lineage, white lineage, gap, founder) | 68 | 2.3e-10 $ |
| Founder stream rebuilt from `founder_profile` equals the lane's own (3 settings) | 3 | 0 |
| `common.late_components` sums to `per_admission.late_profile` (ages 50–84, two arms, three cases) | 36 | 0 |
| Parent stream on the lineage calendar reproduces `per_admission.csv` common-total NPVs (stored to $0.1) | 18 | $0.046 |

The lineage lane's central case reproduces as −$1,297,150.36 (0%) and −$514,635.25 (3%) [2026-09-28: after
audit §E, −$1,288,162.18 and −$513,398.38]. Reruns of
`verify.py`, `calibration.py` and `arms.py` leave `derived/` byte-identical (`diff -rq` empty, all
rc 0). No file outside this directory was written; the imports run with bytecode caching off.

## Arm 1 — the founder legalised by a US-born child at 21

G2 is born in year 4 and turns 21 in year 25; the founder is then 50. A parent of a citizen aged
21+ is an immediate relative [SOURCE: 8 U.S.C. 1151(b)(2)(A)(i), "in the case of parents, such
citizens shall be at least 21 years of age", `ir5_fraud_and_cohorts_2026_09_27/sources/law_8usc1151_ina201_cornell.txt`].
Adjustment inside the US needs an alien "who was inspected and admitted or paroled" [SOURCE: 8
U.S.C. 1255(a), same folder]. An entrant without inspection must interview abroad, and leaving
after a year or more of unlawful presence bars return for ten years [SOURCE: 8 U.S.C.
1182(a)(9)(B)(i)(II)]; the waiver counts hardship only to a "citizen or lawfully resident spouse
or parent" [SOURCE: 1182(a)(9)(B)(v)], so a citizen child does not open it (ladder 187).

Lineage gap, $ (negative = Mexican lineage more costly than the white reference):

| Arm | 0% | 3% | Channel vs never legalised, 2026 rules, central (0% / 3%) | Share of the arm's gap |
|---|---:|---:|---:|---:|
| Lineage lane central (never legalised, pooled profile from 65) | −1,297,150 | −514,635 | — | — |
| Never legalised, statutory bars + 2026 new-enrollee care, central | −899,451 | −425,954 | — | — |
| Never legalised, 12 priced regimes (range) | −872,558 to −1,147,983 | −419,897 to −481,929 | — | — |
| Lineage lane arm 2b, legalised at 35 | −1,272,572 | −502,214 | — | — |
| **1a** adjusts to LPR at 50, pooled profile after | **−1,285,255** | **−509,960** | −385,804 / −84,006 | 30.0% / 16.5% |
| 1a with the five-year bar at 50–54 | −1,281,018 | −508,050 | −381,566 / −82,096 | 29.8% / 16.2% |
| **1b** leaves at 50, ten-year bar, admitted at 60 | **−1,286,967** | **−511,124** | −387,515 / −85,170 | 30.1% / 16.7% |
| 1b with the five-year bar at 60–64 | −1,276,647 | −507,662 | −377,196 / −81,708 | 29.6% / 16.1% |
| 1a, two-year processing lag (LPR at 52) | −1,286,904 | −510,736 | −387,453 / −84,782 | 30.1% / 16.6% |
| 1b, two-year lag (abroad 52–61) | −1,282,906 | −509,510 | −383,454 / −83,556 | 29.9% / 16.4% |

Against the twelve priced never-legalised regimes the 1a channel runs −$137,272 to −$412,697 at 0%
(10.7–32.1% of the gap) and −$28,031 to −$90,063 at 3% (5.5–17.7%). Against the lineage lane's
central it is +$11,895 / +$4,675 (the gap 0.9% smaller), because that central charges the
never-legalised founder the pooled Mexico-born profile from 65 anyway. [CALCULATION]

Reading. Arm 1 is the lineage lane's 2026-09-26 finding — legalising widens the lineage gap by
$355–390k under 2026 rules — reached through the route a US-born child actually opens, fifteen
years later. The later date moves the result by $13k (the −$870 working-age penalty runs 15 more
years). The ten years abroad move it by $2k: the pooled Mexico-born balance is +$1,710 a year at
50–54 and −$1,385 at 55–64, so removing those years removes almost nothing. The arm is
conditional; how many unauthorized Mexican parents take the IR-5 route is outside it (the
calibrated flow in arm 2 counts them among US-born petitioners). No blend of 1a and 1b is given:
no local source measures the share of the Mexican unauthorized stock with a lawful entry, and
ladder 187's 55–61% entered-without-papers share is among 2003 green-card recipients, not the
stock. [INFERENCE]

## Calibration of p

`calibration.py` → `derived/calibration.csv`, `derived/calibration.json`. E = Mexican IR-5 parents
admitted per newly eligible citizen; p = E / m(60), where m(60) = 2·l(60)/l(29) = 1.805 living
parents on the common total table.

| Input | Value | Source |
|---|---:|---|
| Mexican IR-5 parents a year | 36,652 (FY2015–24 mean); 49,040 (FY2022–24); 63,050 (FY2024) | [DATA: `late_arrival_tail_2026_09_27/derived/ir5_flow.csv`, OHSS] |
| Mexico-born persons naturalised a year | 128,880 / 111,460 / 107,670 (FY2022/23/24) | [SOURCE: OHSS FY2024 Naturalizations Annual Flow Report, Table 2, ohss.dhs.gov/topics/immigration/naturalizations/annual-flow-report/fy-24-naturalizations-flow-report; cached `_cache/nat_fy24.html`, sha256 in `calibration.json`] |
| US-born children of Mexico-born parents turning 21 a year | 397,436 (2,782,050 aged 18–24 ÷ 7) | [DATA: ledger_absolute `age_profile_components.csv` population, `mexican_second_gen` = native with a Mexico-born parent, CPS ASEC 2025] |
| Naturalised Mexico-born adults; US-born adults 21+ with a Mexico-born parent | 3,765,836; 7,722,576 | [DATA: `origin_attachment_mexico_2026_09_27` ACS 2024; ledger population] |
| Share of Mexican IR-5 parents aged 55+ | 0.39–0.49 (FY2015–24), 0.38–0.48 (FY2024) | [DATA: ir5_flow.csv bound; NIS-2003 ratio, as the late-arrival lane] |

| Estimator | Low (FY2015–24 flow) | Central (FY2022–24) | High (FY2024) |
|---|---:|---:|---:|
| Equal hazard: IR-5 ÷ (naturalisations + turning 21) | 0.071 | **0.096** | 0.125 |
| Stock hazard × remaining life of a parent aged 59 (24.4 years) | 0.078 | 0.104 | 0.134 |
| Age bound, NIS ratio: IR-5 aged 55+ ÷ naturalisations | 0.122 | 0.167 | 0.221 |
| Age-bound ceiling | 0.155 | 0.211 | **0.280** |

The flow and stock estimators agree within 10%. The arms use equal hazard low / central (E 0.071 /
0.096, p 0.040 / 0.053) and the FY2024 age-bound ceiling as high (E 0.280, p 0.155), which gives
every parent admitted at 55+ to a naturalised petitioner. Expected parents per founder who becomes
an LPR = 0.619 × p × m(a0): 0.044 / 0.059 / 0.173 at a0 = 60. [CALCULATION]

Two cautions. Equal hazard between naturalised and US-born petitioners is untested; the age bound
is the only evidence on the split, and it caps the naturalised share rather than measuring it.
And m(60) overstates the living parents of an average new citizen (a Mexican naturalising in their
forties has parents near 70), so p is somewhat understated while E, which carries the result, is
not. [INFERENCE]

## Arm 2 — the founder sponsors their own parents

The founder must be a citizen to petition, so the arm runs on three tracks: **L25** an LPR on
arrival (the lineage lane's Mexico-born-average founder), naturalising at 30; **L10** legalised
at 35 (the lane's arm 2b), naturalising at 40; **L50** legalised at 50 by the child (arm 1a),
naturalising at 55. Naturalisation probability 0.619 [SOURCE: `origin_attachment_mexico_2026_09_27`
RESULT.md, 61.9% of the eligible Mexican pool, ACS 2024 / OHSS]. Parents are admitted a year after
naturalisation at the founder's age + 29 (L25 at 55/60/65 with gaps 24/29/34; L10 at 70; L50 at
85). The central case of the unauthorized founder, who never legalises, has no channel.

One parent's remaining-life value (common total survival; year 0 = founder's arrival):

| Parent admitted | New arrival, at admission, 0% | New arrival, to year 0, 3% | Eligibility change only, 0% / 3% |
|---|---:|---:|---:|
| 55 (L25, year 6) | −456,588 | −201,756 | −385,734 / −169,394 |
| 60 (L25, year 6) | −414,688 | −205,301 | −353,514 / −176,505 |
| 65 (L25, year 6) | −380,602 | −215,022 | −312,720 / −176,694 |
| 70 (L10, year 16) | −300,615 | −135,230 | −239,091 / −107,531 |
| 85 (L50, year 31) | −109,029 | −37,848 | −75,656 / −26,037 |

New arrival = `per_admission.late_profile` statutory arm, central case (five-year bar, observed
late-arrival receipt by tenure; low/high cases in `arms.csv`). Eligibility change only = that
profile minus the same parent as an unauthorized resident (from 65, no Social Security, SSI,
federal medical, institutional or noncash programs, and public care at the lineage lane's 2026
new-enrollee central, $2,667 a year). Variants in `arms.csv`: bars at every age (−$364,772 at 60);
counterfactual care at peak state coverage (−$270,150). The eligibility change is 85% of the
new-arrival value because an unauthorized senior under the bars is close to fiscally neutral;
the programs that legal status opens carry the cost. [CALCULATION]

Lineage gap, L25, parents admitted at 60 (the brief's central age):

| p | Parents per founder | 0% | 3% | Channel share of gap, 0% / 3% |
|---|---:|---:|---:|---:|
| 0 | 0 | −1,263,920 | −494,610 | — |
| Calibrated low, new arrival | 0.044 | −1,282,244 | −503,682 | 1.4% / 1.8% |
| **Calibrated central, new arrival** | **0.059** | **−1,288,438** | **−506,748** | **1.9% / 2.4%** |
| Calibrated central, eligibility change only | 0.059 | −1,284,821 | −505,045 | 1.6% / 2.1% |
| Calibrated central, 33% / 72% already resident | 0.059 | −1,287,235 / −1,285,837 | −506,182 / −505,524 | 1.8% / 2.3%; 1.7% / 2.2% |
| Calibrated high (age-bound ceiling), new arrival | 0.173 | −1,335,831 | −530,211 | 5.4% / 6.7% |
| **1, new arrival** | 1.118 | **−1,727,357** | **−724,045** | **26.8% / 31.7%** |
| 1, eligibility change only | 1.118 | −1,658,993 | −691,864 | 23.8% / 28.5% |
| 1, all pricings (range) | 1.118 | −1,565,828 to −1,754,108 | −642,417 to −741,877 | 19–28% / 23–33% |
| 1 and naturalisation certain | 1.805 | −2,012,607 | −865,264 | 37.2% / 42.8% |

Resident shares: 0.33 = NIS-2003 Mexican IR-5 parents who adjusted inside the US; 0.72 = FY2024
Mexican immediate relatives (all classes) who adjusted [DATA: `ir5_age_nis2003.csv`,
`mexico_ir_new_vs_adjust.csv`].

Other tracks and ages (new arrival, 0% / 3%):

| Track, parent age | p = 0 | Calibrated central | Channel share | p = 1 | Channel share |
|---|---:|---:|---:|---:|---:|
| L25, 55 | −1,263,920 / −494,610 | −1,291,707 / −506,888 | 2.2% / 2.4% | −1,789,155 / −726,699 | 29.4% / 31.9% |
| L25, 65 | −1,263,920 / −494,610 | −1,285,434 / −506,764 | 1.7% / 2.4% | −1,670,578 / −724,352 | 24.3% / 31.7% |
| L10, 70 | −1,272,572 / −502,214 | −1,288,236 / −509,260 | 1.2% / 1.4% | −1,568,661 / −635,408 | 18.9% / 21.0% |
| L50, 85 | −1,285,255 / −509,960 | −1,288,440 / −511,066 | 0.2% / 0.2% | −1,345,462 / −530,860 | 4.5% / 3.9% |

The later the founder naturalises, the older and fewer the parents and the smaller the channel.
The route the central unauthorized founder can actually take (legalised at 50, naturalised at 55,
parents about 85) adds 0.2% at the calibrated rate and 4.5% even at p = 1. [CALCULATION]

## Arm 3 — attribution [FRAMING-SENSITIVE]

The lineage lane defines a lineage as the founder and descendants; the sponsored parents are
ancestors, so on that definition they are excluded and the gap is the p = 0 row of each track.
Charging them to the lineage that petitioned is the other defensible reading: without the
founder's naturalisation and petition the parents would not be in the US (new arrivals) or would
stay outside the programs that legal status opens (already resident). The two readings differ by
the channel column: at the calibrated rate by $18–28k undiscounted on L25 (1.4–2.2% of the gap),
at p = 1 by $407–525k (24–29%).

Under the calibrated E the charge is already shared among siblings: E counts parents per
citizen, so two naturalised children of the same parents each carry half. At p = 1 the founder's
lineage owns both parents whole, which is the maternal-full analogue the lineage lane's
per-capita rule avoids for children, and so an upper bound on ownership. The white reference
carries no counterpart: a third-plus white founder's parents are already US residents. [INFERENCE]

## What is not in it

- **Chain beyond the founder.** G2 and later are US-born, so their only petitionable parents are
  the founder (arm 1) and the other parent, who belongs to another lineage under per-capita
  attribution. Siblings of the founder (IR-5 parents' other children, F4 visas) are not modelled.
- **SSI in the five-year bar** is inside `cash` and not separable at component level; the 1a/1b
  bar variants remove only medical, institutional and noncash programs and therefore understate
  the bar slightly (the bar variants move the gap by $4–10k).
- **Quarters of coverage** earned unauthorized and later credited after legalisation are not
  modelled; the legalised founder takes the pooled Mexico-born profile, as in the lineage lane.
- **Crime lines** are untouched and not reported for these arms.
- **Return migration of the parents** is zero, as in the per-admission lane.
- The calibrated p is a 2022–2024 rate; the Mexican IR-5 flow doubled after 2019 and the arm puts
  the admission in year 6 of a century.

## Disconfirmation

- The channel could be larger than the calibrated 2% if naturalised Mexicans petition far more
  than US-born children. The age-bound ceiling, which assigns every parent aged 55+ to a
  naturalised petitioner, raises it only to 5–7%. Reaching the p = 1 figure (27–32%) would need
  every naturalised founder to bring surviving parents: 19 times the calibrated central p (0.053)
  and 6.5 times the ceiling's (0.155).
- Arm 1 could have shrunk the gap if the ten years abroad removed costly years; they remove
  almost nothing because the founder's balance at 50–59 is near zero.
- Against the lineage lane's central (pooled from 65) the child's petition slightly reduces the
  gap. The sign of arm 1 therefore depends on the senior rule for the never-legalised founder,
  which the lineage lane's 2026-09-26 revision already settled in favour of the statutory rule.
