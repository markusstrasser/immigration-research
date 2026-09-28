# CDC WONDER, Natality 2016–2024 expanded, year 2024: quoted definitions, queries and totals

Files (hashes in `derived/sources.json`):

- `_cache/wonder_natality_expanded_help.html`, from `https://wonder.cdc.gov/wonder/help/natality-expanded.html`,
  fetched in phase 1 for definitions; `_cache/wonder_natality_expanded_help.txt` is its text, and the line numbers
  below refer to it;
- five exports of dataset D149, made 2026-09-28 JST through the WONDER web form (the WONDER API refuses
  sub-national location), each ending with the query block quoted below.

## Definitions (help page)

> All statistics representing one to nine (1-9) births are suppressed.

(line 42)

> Location is based on mother's legal residence recorded on the birth certificate.

(line 1206)

> Mother's Birth Country — This field reports the place of mother's birth. The list includes 294 options, from
> Afghanistan to Zimbabwe; Unknown or Not Stated.

(lines 1854–1856)

> Expanded Hispanic origin categories - Mexican; Puerto Rican; Cuban; Dominican; Central or South American; Other
> and Unknown Hispanic;

(line 111, under "Maternal Hispanic Origin")

> Source of Payment for Delivery — This field reports the source of payment for delivery, in two fields (code values
> shown inside parenthesis after each category label): Source of Payment for Delivery - 5 categories: Medicaid (1);
> Private Insurance (2); Self Pay (3); Other (4); Unknown or Not Stated (9).

(lines 3390–3399)

> The term "Suppressed" replaces vital statistics, when the figure represents fewer than ten (1-9) births or deaths.
> Totals and sub-totals are suppressed when the value falls within scope of the suppression criteria, or when the
> summary value includes a single suppressed figure, in order to prevent the inadvertent disclosure of suppressed
> values.

(lines 4315–4321, under "Assurance of Confidentiality Constraints", line 4310)

## Query blocks (quoted from each export's footer)

Every export carries:

> Dataset: Natality, 2016-2024 expanded
>
> Show Zero Values: True
>
> Show Suppressed: True
>
> Caveats: 1. Each birth record represents one liveborn infant.

| File | Query parameters | Group by | Show totals | Query date (WONDER's clock) |
|---|---|---|---|---|
| `wonder_2024_state_x_origin.tsv` | Year: 2024 | State of Residence; Mother's Expanded Hispanic Origin | Disabled | Sep 27, 2026 11:59:49 PM |
| `wonder_2024_state_x_mexico_born.tsv` | Mother's Birth Country: MEXICO (MX); Year: 2024 | State of Residence | True | Sep 28, 2026 12:00:09 AM |
| `wonder_2024_payer_x_origin.tsv` | Year: 2024 | Source of Payment for Delivery; Mother's Expanded Hispanic Origin | True | Sep 28, 2026 12:00:41 AM |
| `wonder_2024_payer_mexico_born.tsv` | Mother's Birth Country: MEXICO (MX); Year: 2024 | Source of Payment for Delivery | True | Sep 28, 2026 12:00:43 AM |
| `wonder_2024_state_all.tsv` | Year: 2024 | State of Residence | True | Sep 28, 2026 12:01:15 AM |

The state × origin export states why its totals are off:

> Messages: 1. Totals are not available for these results due to suppression constraints.

No state's Mexican-origin cell is suppressed [DATA: derived/target_national.csv,
wonder_births_mex_origin_suppressed_states = 0], so its 51 state cells sum to the national count.

## Totals quoted from the exports

From `wonder_2024_payer_x_origin.tsv`:

> "Total" "Medicaid" "1" 1445210
>
> "Medicaid" "1" "Mexican" "2148-5" 295689
>
> "Private Insurance" "2" "Mexican" "2148-5" 169849
>
> "Self Pay" "3" "Mexican" "2148-5" 35366
>
> "Other" "4" "Mexican" "2148-5" 15939
>
> "Unknown or Not Stated" "9" "Mexican" "2148-5" 4306
>
> "Total" "Unknown or Not Stated" "9" 29992
>
> "Total" 3628934

From `wonder_2024_payer_mexico_born.tsv`: Medicaid 110823, Private Insurance 40489; the file's total is 185599
[DATA: derived/target_national.csv].

The five Mexican-origin payer cells sum to 521,149, the state export's national count
[CALCULATION: 295,689 + 169,849 + 35,366 + 15,939 + 4,306], so the two exports agree.
