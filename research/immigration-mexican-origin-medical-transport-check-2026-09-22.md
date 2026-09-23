# Mexican-origin public medical spending on the transport's own donor file: MEPS 2024

Date: 2026-09-22. [DATA / CALCULATION; FRAMING-SENSITIVE in the ledger translation]
Calculation record; narrative authorship remains operator-owned.

**Verdict:** In MEPS HC-256, the file the ledger transports medical costs from, people of
Mexican origin draw **less** public medical money per person than the average of the very
donor cell the transport assigns them, not more: **0.89 at 65+ (SE 0.15, 95% CI 0.61–1.18)**,
**0.69 at 18–64 (SE 0.10, interval excludes 1)** [2026-09-23: an age-domain figure; on the transport's cells the pooled 2016–2024 ratio is 0.92, ladder 206], 0.76 across all ages (SE 0.21). Medicaid
alone runs the other way, 3.3× the white dollars at 65+ with coverage of 26% against 7% for
whites and 12% for all donors; Medicare at 0.85×, out-of-pocket at 0.40× and private
insurance at 0.38× keep the public total below one. Holding the Medicaid mix at the
all-donor mix lowers the ratios further, to 0.80 at 65+ and 0.55 at 18–64. Across the ten
transport cells two exclude one, in opposite directions, so no flat ethnicity multiplier is
supported. Translated onto the union's ledger cells, 65+ implies **$2.7bn less cost (SE
6.7)**; the all-ages figure is unusable because one child record carries 68% of the
Mexican-origin 0–17 mean. Set against the MCBS finding of 1.27 for all Hispanic Medicare
beneficiaries, the sign of the ethnicity dimension at 65+ is **open, about −40% to +56%**;
what both files agree on is the mechanism.
[CALCULATION: [`meps_mexican_origin_medical_2026_09_22`](../infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22/RESULT.md)]

## 1. Object

The ledger's public medical charge is a donor transport: each CPS record receives the
weighted mean public-payer spending of MEPS 2024 donors in its age band × US-birth cell
(`donor_model(medical, d, False)` in `absolute_ledger.py`; the insurance key exists in the
module and is switched off in the pinned build). Public payers are Medicare, Medicaid, VA,
TRICARE, other federal and state/local. MEPS carries `HISPNCAT`, whose Mexican category
holds 2,679 people (42.4M weighted), and `BORNUSA`, so the Mexican-origin mean can be set
against the all-donor mean inside the transport's own cells. Standard errors are Taylor
linearizations on `VARSTR`/`VARPSU`, validated against a Rao-Wu PSU bootstrap within 2%. All
eight `HISPNCAT` codebook cells and both of the transport's nativity anchors reproduce
exactly before any ratio is computed. [DATA: `h256cb.pdf`; `derived/audit.json`]

## 2. Payments per person, 2024 dollars

| Domain | Group | n | Public | Medicare | Medicaid | Out of pocket | Private | All sources | Ever Medicaid |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 65+ | Mexican-origin | 280 | 9,794 | 8,386 | 974 | 921 | 1,112 | 11,939 | 0.258 |
| 65+ | NH white | 3,502 | 11,057 | 9,927 | 293 | 2,300 | 2,967 | 16,473 | 0.071 |
| 65+ | All donors | 4,839 | 10,963 | 9,594 | 531 | 1,963 | 2,696 | 15,757 | 0.124 |
| 18–64 | Mexican-origin | 1,567 | 1,314 | 199 | 883 | 621 | 1,908 | 3,931 | 0.258 |
| 18–64 | All donors | 10,092 | 1,911 | 619 | 1,066 | 1,084 | 4,635 | 7,739 | 0.189 |
| 0–17 | Mexican-origin | 729 | 3,620 | 0 | 3,462 | 247 | 777 | 4,662 | 0.619 |
| 0–17 | All donors | 3,545 | 1,489 | 4 | 1,408 | 494 | 1,510 | 3,522 | 0.436 |

[DATA: `derived/cells.csv`]

## 3. The transport's own cells

Mexican-origin / all-donor public spending per person [DATA: `derived/ratios.csv`, `scheme=transport`]:

| Band | US-born | Foreign-born |
|---|---|---|
| 0–17 | 2.44 (CI 0.58–4.29, n 691) | 1.36 (0.41–2.32, n 38) |
| 18–34 | 0.90 (0.48–1.31, n 507) | **2.00 (1.18–2.81, n 134)** |
| 35–49 | **0.62 (0.25–0.98, n 209)** | 1.18 (0.51–1.84, n 294) |
| 50–64 | 0.97 (0.51–1.42, n 154) | 0.58 (0.04–1.12, n 269) |
| 65+ | 0.97 (0.54–1.40, n 125) | 0.84 (0.52–1.16, n 155) |

Holding the Medicaid-coverage mix at the all-donor mix: 0.80 (SE 0.14) at 65+ and 0.55 (SE
0.07) at 18–64 against all donors. In every domain the pooled ratio sits above both
within-coverage ratios, so the Mexican-origin population's higher Medicaid coverage is what
holds the pooled figure up. [DATA: `derived/ratios.csv`, standardized rows]

## 4. Translation onto the union's ledger cells

Each band's `medical` and `M` charge for the union multiplied by that band's MEPS ratio, the
two nativity cells combined with the union's own foreign-born share per band. Positive means
a smaller cost. [DATA: `derived/ledger_translation.csv`]

| Bands | Ledger charge $bn | Δ $bn | SE | Δ without the one record |
|---|---:|---:|---:|---:|
| 65+ (65–74, 75+) | −43.6 | **+2.7** | 6.7 | +7.0 |
| All eight bands | −128.0 | −26.6 | 29.7 | +20.2 |

The all-bands figure is not usable. One 4-year-old with $1,242,405 of Medicaid payments and
a weight of 25,339 supplies 68% of the Mexican-origin 0–17 mean; with that record the 0–17
ratio is 2.43, without it 1.09, and six of the eight bands imply a smaller cost. The record
is a retained catastrophic case at the top of the codebook's range, not an error, and the
transport itself carries it inside its 0–17 donor means. Pooling 2023 with 2024 at 65+
(558 Mexican-origin records, 2023 dollars inflated by the CPI-U ratio 1.0295 from the local
FRED file) gives 0.81 (SE 0.09) against all donors; 2024 stays primary as the transport's
year. [DATA: `derived/audit.json`, `leave_one_out`, `pooled_2023_2024_65plus`]

## 5. Against the MCBS 65+ result

The [MCBS check](immigration-elderly-medical-by-ethnicity-2026-09-22.md) found Hispanic /
non-Hispanic white public payments at 65+ of 1.27 (CI 0.97–1.56); this file gives
Mexican-origin / non-Hispanic white of 0.89 (CI 0.59–1.18). The intervals overlap only on
0.97–1.18. Four differences separate the objects rather than falsifying either: MCBS covers
Medicare beneficiaries living in the community all year, MEPS every non-institutional 65+
resident including those without Medicare; MCBS pools every Hispanic origin, this lane
isolates Mexican origin; MCBS is 2023 with administrative Medicare claims behind its
fee-for-service amounts, MEPS 2024 with household-reported payments (which the ledger's item
M scales to national totals, uniformly across groups); MCBS counts Medicare Advantage plan
payments for services. What both agree on: far higher Medicaid coverage and dollars, far
lower out-of-pocket and private payment, equal or lower total spending, and a pooled public
ratio held up by coverage composition. For the ledger's 65+ cell the honest statement is
that the transport's zero ethnicity adjustment lies inside both files' intervals; the range
across them is about −40% to +56%. Under 65 only MEPS speaks, and it says the transport
assigns the union's members more public medical cost than Mexican-origin donors of the same
age and nativity actually draw, which is the lenient direction. [INFERENCE]

## 6. Limits

- MEPS is the civilian non-institutional population; institutional Medicaid is absent and
  item N is not bounded here.
- `HISPNCAT == 1` is self-reported Mexican origin, not birthplace or generation; people
  reporting multiple Hispanic origins fall outside it. The union is defined on CPS ancestry
  and nativity, so the translation assumes the two populations resemble each other cell by
  cell.
- 280 Mexican-origin records at 65+, 108 in the 75+ ledger band; every 65+ interval admits
  both a 40% shortfall and parity.
- No income dimension is used, although MEPS carries income; MCBS showed income reversing
  the 65+ sign, and coverage standardization is only a partial substitute because coverage
  is downstream of income.
- Item M's two NHEA coefficients are applied at band level here and record by record in the
  ledger.
- Retained catastrophic cases make untrimmed cell means fragile in small cells; a trimmed
  estimator would be more stable and a different estimand from the transport's.

## 7. Sources

[DATA: MEPS HC-256 (2024) `h256dat.zip`, `h256su.txt`, `h256cb.pdf` and HC-251 (2023), pinned
under `sources/immigration-fiscal/data/external/stage3/ahrq/`; the transport module
`infra/immigration-fiscal/build/meps_health_transport_2024.py`; ledger cells
`ledger_absolute_2026_09_17/derived/age_profile_components.csv`, `age_profiles.csv`]
[CALCULATION: `infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22/meps_mexican.py`,
gates in `derived/audit.json`, `test_meps_mexican.py` (20 tests)]

## Revisions

- 2026-09-23: Pooled MEPS 2016–2024 ([lane](../infra/immigration-fiscal/medical_ethnicity_pooled_2026_09_23/RESULT.md), ladder 206). Claim change: the 18–64 figure of 0.69 compares whole age domains; on the transport's cells the union-weighted ratio is 0.92 (0.96 winsorized). The 65+ range narrows to 0.88 (CI 0.74–1.02) against MCBS's 1.265, still open. The all-ages ledger correction, unusable on 2024 alone, is +$0.15bn (SE 10.4).
- 2026-09-22: created. Ladder 175; qualifies ladder 173 and the MCBS memo's "no reduction"
  clause, which is withdrawn there. No ledger value changes.
