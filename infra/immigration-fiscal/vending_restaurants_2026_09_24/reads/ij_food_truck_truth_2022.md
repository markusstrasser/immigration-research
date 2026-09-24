**Verdict:** A national county-panel test (CBP 2005–2016) of whether more food-truck establishments are followed by fewer restaurant establishments; it finds no significant lagged effect and a positive same-year association, but the design is weak (establishment counts only, employer trucks only, about one truck per county, an instrument with no credible exclusion restriction). Grade: C- (panel correlation with a lag; not causal; counts, not sales).

Source: Dick M. Carpenter II and Kyle Sweetland, *Food Truck Truth: Why Restaurants—and Cities—Have Nothing to Fear from Mobile Food Businesses*, Institute for Justice, January 2022 (file dated Dec 2021), 40 pp. A peer-reviewed version by Carpenter appears as "Does the growth of food trucks threaten the sustainability of restaurants? Evidence from a nationwide analysis of U.S. businesses", *Journal of Foodservice Business Research*, doi:10.1080/15378020.2023.2275514 (abstract seen via search; journal text not read).
[SOURCE: https://ij.org/wp-content/uploads/2021/12/Food-Truck-Truth-WEB-dec-2021.pdf, pp. 2–3, 15–16, 24–25]
Local copy: `_cache/reads/ij_food_truck_truth_2021.pdf`, parsed `.txt` beside it.

## Population, period, unit

All US counties (n = 3,133) and non-rural counties (n = 1,165), 2005–2016; County Business Patterns establishments: NAICS 722330 (mobile food services) against full-service, limited-service and cafeteria restaurants.

## Design

Arellano-Bond dynamic panel (one-step), restaurants on lagged restaurants, food trucks (same year and one-year lag), population, unemployment, year effects; ethnic diversity (HHI of racial shares) used as an instrument for food trucks. Robustness: OLS fixed effects, two-step, Blundell-Bond ("substantively similar").

## Numbers

| quantity | value | SE or CI if causal | page/table | verbatim quote (<=40 words) |
|---|---|---|---|---|
| Mean restaurants vs food trucks per county | 145 vs 1 | n/a | Table 1, p. 16 | "the average number of restaurants per county, 145, swamped the number of food trucks, just one per county." |
| Lagged food trucks → restaurants, all counties | +1.837 restaurants per truck | se 1.277, p = 0.150 [95% CI ≈ −0.67 to +4.34, CALCULATION: ±1.96 se] | Table A1, p. 25 | "Food trucks (lagged)                1.837          1.277         0.150" |
| Lagged food trucks → restaurants, non-rural | +2.120 | se 1.332, p = 0.112 [95% CI ≈ −0.49 to +4.73] | Table A1, p. 25 | "Food trucks (lagged)                1.837          1.277         0.150            2.120            1.332           0.112" |
| Same-year association, all counties | +3.450 | se 1.297, p = 0.008 (not causal, per authors) | Table A1, p. 25 | "Food trucks                        3.450           1.297        0.008" |
| Second lag | not robust | n/a | p. 25 | "The results were not robust across all models. Specifically, inconsis- tencies appeared in statistical significance, signs on coefficients and magnitudes of coefficients." |

## What it says about restaurants or formal businesses

"the number of food trucks in one year has no effect on the number of restaurants in the next year" (p. 2). Steel-man of the restaurant side, as the report quotes it: "[W]hen there's a whole bunch (of trucks), we see a significant drop in sales" (p. 24). [INFERENCE] The test cannot see that complaint: it counts establishments, not sales or margins, at county level, where one employer food truck per county is a tiny exposure; a null on closures within a year says little about lost revenue at restaurants next to vending. It also excludes unlicensed vendors and nonemployer trucks entirely (CBP covers employer establishments). The authors' own caveat: "our analysis is not a true experiment" (p. 15), and the same-year coefficient "is not causal" (p. 16).

## Stated limitations

"Note, however, that our analysis is not a true experiment in which the number of food trucks can be identified as the single cause of changes in" restaurants (p. 15). Census counts of 722330 are "a floor to the industry's size" (endnote 8).

## Advocacy note (applied symmetrically)

The Institute for Justice litigates against food-truck restrictions; per rule 3 this carries no grade weight, the same as vendor-advocacy and restaurant-association material. The grade rests on the design flaws listed above.
