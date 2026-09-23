**Verdict:** Housing moves money mainly between other residents, from renters to owners. The net
gain to other residents is small. In the **long-run arm**, which matches the complete account's
primary case (structures are rebuilt and only land is scarce), the group's presence has other
residents' renter households paying **about $34bn a year more in contract rent**. The range is
$22–58bn, or about $860 per renter household ($830 where the householder was born in the US).
About 96.5% of that goes to landlords who are themselves other residents, so it is a transfer
inside the beneficiary set. Other owner-occupiers hold about **$1.9tn more home value**, a stock
with range $1.2–3.3tn. The group's own renters pay $4–11bn more. Of that, $4–10bn reaches
landlords who are other residents. About 3.5% of other renters' extra rent flows the other way,
to landlords who belong to the group or are abroad. Counting the group's extra rent in full, as
the brief's frame does, the **net for other residents is +$2.6bn to +$8.8bn a year** (range
+$1.0bn to +$17.6bn). That count gives the group's whole extra rent as a gain. In fact, the
housing the group occupies has to come out of other residents' consumption (short run), or the
landowners' gain builds up over the rent path (long run). The welfare-consistent net is
therefore about half as large: **+$0.7bn to +$3.5bn** (range −$0.4bn to +$9.4bn). It turns
negative if more than about 6% (uniform geography) to 13% (metro geography) of rental housing is
owned outside the beneficiary set. The **short-run arm** (fixed housing stock, rent elasticity
1.0–2.0) raises the renters' loss about 3.5-fold, to **$110–120bn a year** ($2,800–3,100 per
household). In that arm owners' stock gain is $6.3–6.8tn and the net is $9–25bn (frame) or
$2–10bn (welfare). **Overlap ruling:** the account's production term is a one-good CES model.
It has reproducible capital, no land and no housing sector. In its primary long-run case the
rental rate of capital is fixed, so land-rent transfers are inside neither P nor F. The
long-run welfare net can therefore be added as a disclosed Z item. It amounts to 0.4–2% of the
$165–197bn main-case net cost. The gross renter-to-owner transfer cancels at fiscal weight 1
and is purely distributional. The short-run arm must not be added to the account's
fixed-capital case, whose GDP-scaled capital gain already includes the return on residential
capital. 2026-09-23.

Model self-report: `claude-opus-5-5[1m]`. Lane brief: [`BRIEF.md`](BRIEF.md). Nothing was
committed and nothing outside this directory was edited.

## 1. Frame, population and money

The frame is the brief's and is not changed. It is the complete annual account's stationary
2024 comparison of the economy with and without the 40.896574m CPS Mexican-origin residents,
with effects measured on all other US residents
[SOURCE: [complete account](../../../research/immigration-complete-annual-account-2026-09-20.md)].
Money is 2024 dollars per year. Annual rent is the ACS monthly amount × 12. Owner-occupied home
value is a stock.

- **Group person (ACS):** Hispanic origin Mexican (`HISP=02`) or born in Mexico (`POBP=303`).
  ACS records no parental birthplace, so this is the closest available match to the CPS union.
  It counts 39.43m persons (SE 0.08m). `HISP=02` alone counts 38.93m, against a published
  B03001 figure of 38.99m. The CPS union is 3.7% larger. Local group shares are scaled up by
  1.0372 so that the national dose is the account's
  40.896574 / 340.110988 = **12.02%**. The rent and value aggregates below are not scaled; the
  1.47m people missing from the ACS count most likely live in households classified as other.
  [DATA: `derived/pums_persons.csv`]
- **Household rules:** the primary rule assigns a household to the group when its householder is
  a group person. The alternatives are any member being a group person, apportionment by the
  share of group members, and `HHLDRHISP=02` only. The household file's householder recode
  matches the person file in all 1,348,408 occupied records. [DATA: `derived/pums_checks.json`]
- **Rent base:** transfers use **contract rent** (`RNTP`), which is what landlords receive.
  Gross rent adds utilities that tenants pay to utility companies, and utilities do not respond
  to land scarcity. Applying the same percentages to gross rent would raise every flow by
  13–16%. Some short-run anchors are estimated on gross rents; this is disclosed, not corrected.

## 2. Tabulation and gate

ACS 2024 one-year PUMS, household weights `WGTP`, 80 replicate weights (SE in parentheses).
Annual $bn; value $tn; households and persons in millions (persons are all members of the
rule's households). [DATA: `derived/pums_tabulation.csv`]

| Rule | Households of | Owners | Renters | No cash rent | Persons | Gross rent | Contract rent | Owner-occupied value | Renter share |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| householder | group | 6.07 | 4.85 | 0.20 | 35.6 | 96.7 (0.6) | 83.4 (0.6) | 2.51 (0.019) | 43.6% |
| householder | other | 80.64 | 38.99 | 1.99 | 290.4 | 777.1 (2.4) | 685.0 (2.1) | 39.10 (0.101) | 32.1% |
| any member | group | 7.98 | 6.01 | 0.23 | 46.4 | 124.1 (0.7) | 107.3 (0.6) | 3.54 (0.024) | 42.2% |
| any member | other | 78.73 | 37.83 | 1.95 | 279.5 | 749.7 (2.3) | 661.2 (2.0) | 38.06 (0.098) | 31.9% |
| person share | group | 6.47 | 5.04 | 0.20 | 37.7 | 101.3 (0.6) | 87.4 (0.5) | 2.74 (0.018) | 43.0% |
| person share | other | 80.24 | 38.80 | 1.98 | 288.2 | 772.5 (2.3) | 681.0 (2.1) | 38.87 (0.101) | 32.1% |
| householder `HISP=02` | group | 5.99 | 4.78 | 0.19 | 35.0 | 95.3 (0.6) | 82.2 (0.6) | 2.47 (0.019) | 43.6% |

Other renter households with a US-born householder number 31.86m and pay $538.3bn of contract
rent. Under the householder rule, the group is 12.0% of residents but 11.1% of renter
households, 11.1% of gross rent, 7.0% of owner households and 6.0% of owner-occupied value.

**Gate: passed.** The PUMS totals match the published ACS 2024 one-year national tables
[DATA: `_cache/acs2024_us_totals.json`, api.census.gov with labels]:

| Item | PUMS | Published | Difference |
|---|---:|---:|---:|
| Aggregate gross rent, monthly (B25065) | $72.817bn | $72.562bn (MOE 0.28) | +0.35% |
| Aggregate contract rent, monthly (B25060) | $64.035bn | $63.744bn (MOE 0.25) | +0.46% |
| Aggregate owner-occupied value (B25079) | $41.602tn | $41.654tn (MOE 0.14) | −0.12% |
| Owner / renter-occupied units (B25003) | 86.711m / 46.025m | 86.636m / 46.102m | +0.09% / −0.17% |
| Total population (B01003) | 340,110,990 | 340,110,990 | 0 |

The complete account's 340.110988m denominator equals this ACS total to within two persons.

## 3. The rent effect of the group's presence

The per-point input is the **rent elasticity with respect to population** `e`, meaning the
percentage change in rent per 1% of population. Per point of the group's population share it
is `e / (1 − s)`, about 1.14e at the national share. The group's share of today's rent is
`f = 1 − (1 − s)^e`. That formula applies the same elasticity to the whole population
difference `N_with / N_without = 1 / (1 − s)`.

| Anchor | As published | Per 1% of population | Horizon | Use |
|---|---|---:|---|---|
| Ladder 183 (repo, ancestry IV, 334 metros) | +1.4% per point of foreign-born share, SE 1.4, 95% CI −1.5 to +4.2 | 1.24 (SE 1.24) | 2000–2010 decade | sensitivity row. The CI covers both arms, so it cannot separate them |
| Wilson & Zhou 2026, Table 6b | +1.438% (SE 0.344) per unauthorized **worker** flow of 1% of initial employment; permits null | **1.79–1.90** (total covered employment), 2.1–2.2 (private) | 2021–2024 | short-run high end (2.0) |
| Saiz 2007, as reported by Wilson & Zhou p.44 and the September 16 housing lane | about 1 per inflow of 1% of population (OLS and IV) | 1.0 | annual | short-run low end |
| Fixed-stock theory, 1/eD | eD 0.5–1.0 (the demand elasticity assumed in ladder 180) | 1.0–2.0 | no supply response | short-run central 1.5 |
| Land scarcity, a/(1 − a(1 − eD)) | a = land share of housing cost 0.25/0.35/0.46; eD 1.0/0.7/0.5 | **0.25 / 0.39 / 0.60** | long run, structures rebuilt | long-run arm |
| Saiz 2010 local, 1/(eS + 0.7) | 225 metros with an elasticity (84% of other renters' rent) | rent-weighted 0.52 | long run | long-run sensitivity |
| Piyapromdee 2020 (structural spatial model, ladder 181 reads) | 0.89 / 0.84 rent per 1% more immigrants, stock counterfactual | 0.84–0.89 | long run with wage and location effects | above the land range |
| Monras 2020 (ladder 181 reads) | log rent on the 1990–2000 relative inflow of low-skilled Mexicans: −0.55 (state IV, SE 0.37), −1.17 (metro IV, SE 0.52); author: "an elasticity of around −1" | negative (the regressor is a labour-force share, not converted) | long run, construction-cost channel | disconfirmation, not an arm |

- **Wilson–Zhou conversion** [CALCULATION: `derived/inputs_wz.csv`]. Their regressor counts
  workers. By their own text, "around 56% of all unauthorized immigrants … are workers" (p.25),
  and their employment IV on all flows against worker flows implies 0.53. March 2021 QCEW total
  covered employment was 140,589,959 [DATA: BLS QCEW 2021Q1 US000] against 331,893,745 residents
  (ACS 2021). A worker flow of 1% of employment is therefore persons equal to 0.757% of
  population, and 1.438 / 0.757 = 1.90. The parsed paper, not the repo summary, was read for
  the definitions [SOURCE: corpus `doi_10_24149_wp2607`, p.20 equation (1), p.25, p.43–44].
- **Land share** [DATA: `derived/inputs_land_foreign.csv`, Federal Reserve Z.1, current
  release]. Owner-occupied real estate at market value was $46.89tn in 2024Q4 (S.1M.b line 4)
  and households' residential structures at current cost $27.91tn (line 48). Land is therefore
  **40.5% of value**, against 34.8% in 2019Q4 and 40.4% in 2026Q2. For noncorporate residential
  real estate, which is mostly rental, land is 46.1%. Structures depreciate, so land's share
  of the annual rent is lower: about 0.33–0.34 at a 5% return and 1.5–2% depreciation. The arm
  uses 0.25/0.35/0.46. [CALCULATION/ASSUMPTION]
- **Geography.** The group is heavily concentrated. Across 377 metros (February 2013 CBSAs)
  and 47 non-metro state remainders, its share averages 27.9% weighted by the group's own rent,
  but 11.5% weighted by other renters' rent. Other renters therefore face slightly less than
  the 12.0% national dose. The two geographies bracket native re-sorting in the counterfactual.
  "Metro-local" applies each metro's own share, so nobody moves in to replace the group.
  "National-uniform" applies 12.02% everywhere, which amounts to full re-sorting.
  PUMA→county uses Geocorr 2022 population factors; county→CBSA uses the 2013 OMB
  delineation, the geography behind the ladder 183 estimates. The allocation preserves every
  national total. [CALCULATION: `derived/cbsa_exposure.csv`, `derived/checks.json`]
- **Extrapolation.** The per-point estimates come from inflows of about 1–5% of population.
  The national stock is 12 points, and local shares reach 35% (Los Angeles), 49% (Riverside)
  and 80–92% at the border. Four functional forms are reported: A, constant elasticity
  (central); B, linear per point of inflow; C, semi-log; D, the short-run elasticity on the
  first 3 points and the land elasticity beyond them. Nationally A–C differ by at most 1.5
  points of rent. The big sensitivity is D, which halves the short run (§4). The linear per-point
  extrapolation is row B.

## 4. Results per arm

Householder rule, form A, central ownership. Values are $bn a year except where marked.
"Landlords from others" is other renters' extra rent that reaches other-resident landlords.
"Landlords from group" is the group's extra rent that reaches them.
[CALCULATION: `derived/arms_headline.csv`]

| Arm | e | Geography | Other renters' extra rent | $ per other renter household | Group renters' extra rent | Landlords from others | Landlords from group | Net, frame | Net, welfare | Other owners' value gain, $tn stock |
|---|---:|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Long run low | 0.25 | uniform | 21.6 | 554 | 2.6 | 20.8 | 2.5 | 1.7 | 0.5 | 1.23 |
| | | metro | 22.1 | 568 | 7.2 | 21.4 | 6.7 | 5.9 | 2.3 | 1.26 |
| **Long run central** | **0.39** | uniform | **33.5** | **859** | 4.1 | 32.3 | 3.8 | **2.6** | **0.7** | **1.91** |
| | | metro | **33.9** | **868** | 10.7 | 32.7 | 10.0 | **8.8** | **3.5** | **1.93** |
| Long run high | 0.60 | uniform | 50.5 | 1,294 | 6.1 | 48.7 | 5.7 | 4.0 | 1.1 | 2.88 |
| | | metro | 50.1 | 1,284 | 15.4 | 48.3 | 14.4 | 12.7 | 5.2 | 2.86 |
| Short run low | 1.0 | uniform | 82.4 | 2,113 | 10.0 | 79.5 | 9.4 | 6.5 | 1.5 | 4.70 |
| | | metro | 78.9 | 2,024 | 23.2 | 76.2 | 21.7 | 19.0 | 7.3 | 4.50 |
| **Short run central** | **1.5** | uniform | **119.8** | **3,072** | 14.6 | 115.6 | 13.6 | **9.4** | **2.2** | **6.84** |
| | | metro | **110.4** | **2,832** | 31.0 | 106.5 | 29.0 | **25.2** | **10.3** | **6.29** |
| Short run high | 2.0 | uniform | 154.8 | 3,971 | 18.8 | 149.4 | 17.6 | 12.2 | 3.0 | 8.84 |
| | | metro | 138.0 | 3,539 | 37.3 | 133.1 | 34.9 | 30.1 | 12.9 | 7.85 |

- **Per US-born-headed renter household** (31.86m households, assumed to face the average local
  effect for other renters): long run $533 / $826 / $1,245 (uniform) and $546 / $835 / $1,235
  (metro); short run $2,031 / $2,954 / $3,818 (uniform) and $1,946 / $2,723 / $3,403 (metro).
  At the central elasticity that is 4.9% of their rent in the long run and 16–17.5% in the short
  run. [CALCULATION: `derived/checks.json`]
- **Ranges** across elasticity levels, forms A–C, the three ownership cases and both
  geographies [`derived/arms_summary.csv`]. Long run: other renters $21.6–57.8bn, net frame
  $1.0–17.6bn, net welfare −$0.4bn to +$9.4bn, owners' stock $1.23–3.30tn. Short run: other
  renters $78.9–163.9bn, net frame $3.8–38.1bn, net welfare −$2.2bn to +$21.8bn, owners' stock
  $4.50–9.35tn.
- **Owners' value gain is a stock and is never added to the flow.** It assumes a constant
  price-to-rent ratio. Scaling it by Wilson–Zhou's price-to-rent response ratio of 1.52 would
  raise it to $2.9tn (long run) or $9.6–10.4tn (short run). Ladder 183's value coefficient,
  +11.6% per point, carries the 2000s boom and bust and is not used. For group owner-occupiers
  the same premium is $0.12–0.37tn (long run), their own asset.

**Sensitivities, central elasticity** [`derived/arms_grid.csv`]:

| Variant | Geography | Other renters | Group renters | Net, frame | Net, welfare |
|---|---|---:|---:|---:|---:|
| Long run, form B (linear) / C (semi-log) | uniform | 34.8 / 35.7 | 4.2 / 4.3 | 2.7 / 2.8 | 0.8 / 0.8 |
| | metro | 36.9 / 39.6 | 12.3 / 13.8 | 10.2 / 11.5 | 4.5 / 5.7 |
| Long run, each metro at its Saiz (2010) elasticity (mean 0.52) | uniform / metro | 44.1 / 45.3 | 5.6 / 13.9 | 3.7 / 11.5 | 1.0 / 4.6 |
| Short run, form B / C | uniform | 116.6 / 127.0 | 14.2 / 15.5 | 9.2 / 10.0 | 2.1 / 2.5 |
| | metro | 105.6 / 122.7 | 29.3 / 35.6 | 23.7 / 28.9 | 9.0 / 14.5 |
| Short run, form D (1.5 on the first 3 points, 0.39 beyond) | uniform / metro | 55.1 / 53.3 | 6.7 / 13.1 | 4.3 / 10.4 | −0.1 / 2.6 |
| Ladder 183 decade estimate, e = 1.24 | uniform / metro | 101.0 / 94.9 | 12.3 / 27.3 | 8.0 / 22.2 | 1.8 / 8.8 |
| Long run, any-member / person-share / `HISP=02` rule | uniform | 32.3 / 33.3 / 33.5 | 5.2 / 4.3 / 4.0 | 3.8 / 2.8 / 2.6 | 1.3 / 0.8 / 0.7 |
| Short run, the same three rules | uniform | 115.6 / 119.1 / 120.0 | 18.8 / 15.3 / 14.4 | 13.5 / 10.1 / 9.2 | 4.2 / 2.6 / 2.1 |

Other renters' loss depends mainly on the elasticity. Geography, functional forms A–C and the
household rule move it by under 20%. Metro-level Saiz elasticities raise the long run by about a
third, and form D halves the short run. The net depends on the
group's own extra rent, which doubles or halves with geography, and on who owns the rentals (§5).

## 5. Who receives the rent: ownership ranges

| Evidence | Value | Source |
|---|---|---|
| Rental units by owner entity, RHFS 2024 (share of reported units) | individual investors 35.4%, trustee 4.2%, partnership / tenants in common 1.7%, **LLP, LP or LLC 48.3%**, REIT 1.5%, real estate corporation 3.4%, nonprofit / cooperative / other institution 5.5%; 10.8% not reported | [DATA: `derived/inputs_rhfs.csv`, Census RHFS 2024 PUF, 4,425 properties, `WEIGHT × NUMUNITS_R`] |
| Hispanic share of other residential real estate (1–4 family non-home property, second homes) | 2.86% (implicates 2.78–3.09%); nonresidential real-estate equity 3.08%; families 11.09% | [DATA: `derived/inputs_scf.csv`, SCF 2022 summary extract; definitions from the Fed's `bulletin.macro.txt`] |
| Group share of Hispanic householders | 55.0% (11.12m of 20.22m) | [DATA: `derived/pums_ownership_proxies.csv`] |
| Group share of interest, dividend and net rental income (ACS `INTP`) | 2.17% ($17.3bn of $796.0bn); 3.0% of persons with positive `INTP` | [DATA] |
| Group share of owner-occupants of 2–4 unit buildings (on-site landlords) | 5.98% (0.105m of 1.748m) | [DATA] |
| Foreign direct investment in noncorporate real estate (equity plus debt) / its market value | 0.71% (2024Q4) | [DATA: Z.1 S.11.2.b lines 3, 37, 40] |

Institutions are counted through their beneficial owners. REIT and corporate shareholders,
and LLC and LP partners, are US residents apart from a foreign share that is not measured here.
The leak shares in the model are:

- **Group-owned share of other residents' rentals: 1% / 2% / 3%.** The SCF share times the
  group share of Hispanics gives 1.6%, the ACS capital-income share is 2.2%, and on-site small
  landlords are 6%. [CALCULATION]
- **Group-owned share of the group's own rentals: 2% / 5% / 10%.** Co-ethnic landlords are not
  measured. [ASSUMPTION]
- **Foreign share: 0.7% / 1.5% / 3%.** Z.1 FDI gives 0.7%; foreign holdings of REIT and
  corporate landlords and small foreign LP stakes are not measured. [DATA/ASSUMPTION]

The net for other residents falls to zero at a common leak share of 10.8% (frame) or 5.7%
(welfare) under the uniform geography, and 24.1% or 12.9% under the metro geography (long run;
the short run is almost the same). The central leak on other renters' rent is 3.5%. The
evidence puts group plus foreign ownership at about 2–6%, so the sign of the net is probably
positive, but the net sits within a factor of two of break-even under the uniform geography.

## 6. Why the welfare net is about half of the frame's net

The brief's frame values the group's contribution at the rectangle: the rent increase times the
units the group occupies. That overstates what other residents gain. [CALCULATION, derivation
in `arms.py` and checked numerically in `test_arms.py`]

- **Short run, fixed stock `S`.** Landlords gain `S·ΔP`. Other renters pay more on the units
  they keep, and they also give up the `H_g` units the group moves into. They valued those
  units at between the old and the new rent. Their loss is `∫H_o dP = S·ΔP − H_g∫λ dP`, so the
  net for other residents is `κ·H_g·ΔP − leakage`, where `κ = [P(1) − mean P] / [P(1) − P(0)]`.
- **Long run, fixed land, structures at cost.** Shephard's lemma gives `L·dr = H·dP`.
  Landowners' gain is `∫H dP`, which is smaller than `H_with·ΔP` because housing expands along
  the path. The net is again `κ·H_g·ΔP` less leakage.

κ is 0.46–0.54 across arms, which is the standard immigration-surplus triangle. The
**welfare** column is the one to add to the account's W as a Z item. The frame column is the
money flow the brief asked for.

## 7. Overlap with the complete account

The production term cannot contain the land-rent transfer. It is a normalized one-good CES of
two skill groups and one reproducible capital stock
[SOURCE: `../matched_benefits_2026_09_19/model.py`]. That lane's README says "The income model
omits housing". The benefits README says "our GDP-normalized CES has no separate housing sector,
so no exact property-overlap claim is made"
[SOURCE: `../full_account_benefits_2026_09_20/README.md`, "Fiscal interface" section]. In the
account's primary long-run case capital fully adjusts, the rental rate is unchanged and "net
capital-income gain is zero", so P + F (+$8.8bn cash / +$13.3bn GDP scaling) carries no return
to a scarce factor. The ruling follows:

1. **Can be added:** the **long-run welfare net, +$0.7bn to +$3.5bn** (range −$0.4bn to
   +$9.4bn), as a signed Z item under the account's residual contract, which covers
   nonoverlapping benefits to included residents under the same counterfactual
   [SOURCE: `../full_account_benefits_2026_09_20/mechanism_contracts.json`]. It would lower the
   $165–197bn main-case net cost by 0.4–2%. The frame figure of $2.6–8.8bn overstates the
   welfare gain by about two-fold (§6).
2. **Cannot be added:** the gross flow from other renters to other landlords ($32bn long run)
   and owners' $1.9tn stock gain. At fiscal-dollar weight 1 these cancel inside the
   beneficiary set; they answer the distributional question, not the net one.
3. **Do not pair the short-run arm with the primary case.** Its natural pair is the account's
   fixed-capital sensitivity. There the GDP-scaled CES pays a higher return on all fixed
   capital, and because GDP includes housing services, that capital includes residential
   capital. The short-run housing arm and that production case overlap in the residential share
   of capital income. [INFERENCE; that GDP includes housing services is TRAINING-DATA]
4. **Taxes on the transfer** (property tax on higher values, income tax on rental income) only
   split the landlords' gain between owners and governments. At weight 1 they do not change the
   net; do not add them as F. Higher voucher payments when market rents rise are likewise
   taxpayer-to-landlord flows inside the set.
5. **The construction-cost channel** (Monras: immigrant construction labor lowers housing costs)
   is a relative-price form of the production gain. The consumer-price lane excluded
   construction [SOURCE: `../../../research/immigration-consumer-price-and-native-hours-2026-09-18.md`],
   and the account does not add consumer-price savings on top of factor income. The same rule
   applies here: not priced and not added.

This updates FAQ 4's "housing unpriced in both directions" for this beneficiary set. The price
channel is now priced as a transfer; amenity capitalization stays unpriced (ladder 155).

## 8. Distribution, the social-cost question

Within other residents, the loss falls on **38.99m renter households** (31.86m with a US-born
householder): $34bn a year in the long run and $110–120bn in the short run. The gain goes to
**landlords** as a flow and to **80.64m owner-occupier households** as a stock, $1.9tn in the
long run. For an owner who keeps living in the house, that stock is matched by a higher implicit
rent. It becomes real on sale to a buyer, which moves it from younger future buyers to current
owners inside the set; that transfer is not modeled here. The group's own renters pay
$4–11bn (long run) and are outside the beneficiary set. Renters' and owners' incomes and ages
were not tabulated in this lane, so their relative positions are not claimed.

## 9. Disconfirmation

- **Monras 2020** is the only long-run estimate specific to Mexican inflows, and it finds rents
  **fall** (−0.55 state, −1.17 metro, per unit of the 1990–2000 low-skilled Mexican inflow
  share; the author calls it an elasticity of about −1) because cheaper construction labor
  outweighs demand. If that is right, the long-run sign reverses and other
  renters gain. The repo's decade estimate (ladder 183, +1.4 per point, CI −1.5 to +4.2) does
  not reject it at the 5% level. [SOURCE: ladder 181 reads, Table 10]
- **Wilson–Zhou's own ACS arm**, which measures self-reported rents (the stock the ACS
  measures), gives +0.734 (SE 1.567), not significant, against 1.438 on Zillow's market rents
  [SOURCE: W&Z Table B5 via the reads file]. The short-run magnitude on sitting tenants' rents
  may be overstated.
- **Timing:** Harvard JCHS and the Yale Budget Lab note that rents surged in 2021 while inflows
  were modest, and Cabral–Steingress attribute about 1.3% of a 17% rise to immigration
  (ladder 50 caveats).
- **Supply:** ladder 183 finds no extra rent effect in supply-inelastic metros
  (−2.3% ± 3.9). This is why the Saiz-local long-run variant stays a sensitivity.

## 10. Limits

1. No elasticity is specific to Mexican origin, and none is a stock (level) elasticity. The
   anchors are flows of all-origin or unauthorized arrivals. Mexican-born is not estimable at
   the 2000 metro endpoint (n = 25, ladder 183).
2. Local shares far beyond the estimates' support drive the metro-geography short run. Areas
   where the group is above 50% hold 8% of the group's rent and 0.8% of other renters' rent.
3. Ownership of the group's own rentals by co-ethnic landlords, and foreign beneficial ownership
   of LLC, REIT and corporate landlords, are assumptions.
4. Rents in public and project-based subsidized housing do not track market rents; those
   properties are part of the 5.5% nonprofit and institutional units. Both renters' loss and
   landlords' gain are overstated by up to that share; the sign of the net does not change.
5. Incidence within renters is not modeled. Saiz (2003) finds the effect concentrated in
   low-quality units, and ladder 79 says the same.
6. Dynamics are outside the frame: durable housing, and removal differing from arrival with the
   sign reversed (Howard, Wang & Zhang 2025).
7. The 1.47m people in the CPS union who are not in the ACS group are left in "other"
   households, understating the group's rent by up to about 4%.

## Covered / skipped

Covered:
- ACS 2024 PUMS household and person files, all four household rules, national and PUMA
  cells, the gate against five published tables, and replicate-weight SEs on the tabulation.
- Wilson–Zhou parsed text: regressor and denominator definitions, and the worker share.
- Z.1 land shares and FDI; SCF 2022 Hispanic ownership shares; RHFS 2024 ownership entities;
  ACS ownership proxies.
- Both arms at three elasticity levels × four functional forms × two geographies × three
  ownership cases; Saiz-local and ladder 183 rows; the welfare correction with tests; and the
  overlap reading of the CES model and the benefits contracts.

Skipped:
- **Replicate SEs on the arms.** Input sampling error is under 1% (§2); the elasticity range
  dominates.
- **Gross-rent base.** Contract rent is what landlords receive; gross rent would add 13–16%.
- **Re-reading Saiz 2007 and Cabral–Steingress in full text.** They enter only as the low and
  high anchors that Wilson–Zhou's parsed text and the September 16 lane already report; neither
  sets a central value.
- **Owner ethnicity from the RHFS.** The public file has no owner race or ethnicity item.
- **Renter and owner income and age profiles.** Not needed for the transfer totals; the next
  step if the distribution is written up.
- **Construction-cost pricing and removal dynamics.** They belong to other overlap classes or
  other frames (§7, §10).
- **Any edit to memos, the ladder or the index.** Outside the lane by instruction.

## Reproduce

Run from the repository root. PUMS ZIPs and the Geocorr cache
(`employment_entry_2026_09_18/_cache/xwalk_puma22.csv`, from that lane's
`fetch_crosswalks.py`) must be present.

```sh
set -a; . infra/immigration-fiscal/acquire/config.local.env; set +a
uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/fetch.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/tabulate.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/inputs.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/housing_transfer_2026_09_23/arms.py
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -m pytest infra/immigration-fiscal/housing_transfer_2026_09_23/ -q
```

The tabulation takes about two minutes and the rest seconds. Five tests pass.

## Files

| File | What |
|---|---|
| `fetch.py` | published ACS totals with labels, ACS 2021 population, QCEW, SCF 2022, Z.1, RHFS 2024 into `_cache/` (ignored); key redacted |
| `tabulate.py` | PUMS chunked reads: `pums_tabulation.csv`, `pums_persons.csv`, `pums_puma_cells.csv`, `pums_ownership_proxies.csv`, `pums_checks.json` |
| `inputs.py` | `inputs_land_foreign.csv` (Z.1), `inputs_scf.csv`, `inputs_wz.csv`, `inputs_rhfs.csv` |
| `arms.py` | `cbsa_exposure.csv`, `arms_grid.csv` (every case), `arms_headline.csv`, `arms_summary.csv`, `parameters.csv` (each input with its source tag), `checks.json` |
| `test_arms.py` | rent-path arithmetic, the fixed-stock welfare integral, support-limited form, land elasticity |

## Revisions

2026-09-23: Connecticut planning regions (09110–09190) now map to 2013 CBSAs in the shared crosswalk; `nonmetro_09` shrinks from 3.68m to 0.11m persons and metros go 377 → 381 (Hartford, New Haven, Bridgeport–Stamford, Norwich–New London; Worcester gains northeastern Connecticut). Saiz-matched metros go 225 → 227 (Hartford 1.50, New Haven 0.98; Bridgeport–Stamford, Norwich–New London and Worcester have no Saiz match), 84.4% → 85.1% of other renters' rent. Metro-local flows move by at most $0.01bn: long-run central other renters' extra rent $33.86bn → $33.86bn (+$0.002bn), short-run central $110.41bn → $110.42bn, Saiz-local $45.30bn → $45.31bn; frame and welfare nets move by under $0.001bn and national-uniform rows are unchanged; owners' stock (long-run central) $1,931.57bn → $1,931.64bn. In the arms table, two printed metro cells change in their last digit: landlords' gain from other renters goes from 106.5 to 106.6 (short run, central) and from 133.1 to 133.2 (short run, high). Detail: [`CT_PLANNING_REGIONS.md`](../hedonic_composition_2026_09_19/CT_PLANNING_REGIONS.md).
