# Low-skill immigration by origin: first-pass incidence split memo

Date: 2026-04-10

## Scope

This memo answers two narrower questions than the general political debate:

1. Which origin groups account for the largest recent low-skill immigrant adult populations in the 2023 ACS-based warehouse?
2. Which origin groups are most likely to generate a `federal better / state-local worse` incidence split?

`Federal better / state-local worse` is not observed directly in the warehouse. The warehouse does **not** contain a full tax-and-transfer ledger by origin. This memo therefore uses a proxy design and should be read as an exposure ranking, not a causal estimate or a full net-present-value fiscal account.

## Data used

1. `acs_origin_national_2023` in [immigration_context.duckdb](/Users/alien/Projects/research/sources/immigration-fiscal/data/derived/immigration_context.duckdb)
2. `origin_destination_context_2023` in the same warehouse
3. ACS PUMS 2023 local extract from [csv_pus.csv](/Volumes/SSK1TB/corpus/census_acs/csv_pus.csv)
4. ACS state median gross rent series already joined into the warehouse
5. Census school finance current spending per pupil already joined into the warehouse
6. FHFA state house-price index context already joined into the warehouse
7. World Bank country ontology joined into `country_origin_dim`

## Measurement frame

The object here is not `all low-skill immigrants`. The relevant cell is:

`origin x education x recency x household structure x destination-cost regime`

The warehouse currently approximates this with:

1. `recent low-skill adult population`: adults 25-64 from a given birthplace with low education and recent arrival status
2. `federal-positive proxies`: higher observed income, lower Medicaid share, lower public-assistance share
3. `state-local-negative proxies`: higher child intensity, higher share of households with children, destination-weighted school spending, destination-weighted rent

This is a useful filter, but it is not a substitute for the National Academies-style full lifetime fiscal model.

## Top recent low-skill origin populations in the current warehouse

For foreign-country origins with at least 50,000 foreign-born adults and at least 10,000 recent low-skill adults, the largest recent low-skill groups are:

1. Mexico: `225,180`
2. Guatemala: `82,230`
3. Honduras: `48,968`
4. El Salvador: `47,738`
5. Cuba: `39,518`
6. Haiti: `28,117`
7. Viet Nam: `27,306`
8. China: `21,799`
9. Colombia: `20,638`
10. Brazil: `19,021`
11. Nicaragua: `18,273`
12. Venezuela: `15,684`
13. India: `15,630`
14. Afghanistan: `15,281`
15. Dominican Republic: `12,914`
16. Myanmar: `11,874`

## Heuristic buckets

### Bucket A: strongest candidates for `federal better / state-local worse`

These groups combine moderate-to-higher observed income for their low-skill recent-arrival cell with notable child intensity and concentration in high-cost states.

1. Brazil
   - Mean income about `32.1k`
   - Medicaid share about `38.5%`
   - Destination-weighted school spending about `18.5k` per pupil
   - Destination-weighted rent about `1672`
   - Mean household children about `1.20`
   - Interpretation: better tax capacity than most low-skill groups, but high destination cost and meaningful family load. This is a plausible split case.

2. Dominican Republic
   - Mean income about `29.3k`
   - Medicaid share about `35.5%`
   - Public assistance about `3.1%`
   - Destination-weighted school spending about `17.6k`
   - Destination-weighted rent about `1617`
   - Mean household children about `1.14`
   - Interpretation: not a clean federal win, but one of the clearer split candidates because the local-cost exposure is high while income is not at the bottom.

3. Cuba
   - Mean income about `25.7k`
   - Medicaid share about `29.2%`
   - Public assistance about `6.3%`
   - Destination-weighted school spending about `19.7k`
   - Destination-weighted rent about `1645`
   - Mean household children about `0.73`
   - Interpretation: lower child burden than most Latin American groups, but extremely high destination-cost exposure. If any low-skill cell can look decent federally while still straining local budgets, this is one of the better candidates.

4. China and Viet Nam low-skill recent-arrival cells
   - China mean income about `26.4k`; Viet Nam about `28.1k`
   - Both heavily concentrated in high-rent, high-spend states
   - Child intensity is moderate rather than extreme
   - Interpretation: these are smaller low-skill cells, but they fit the split logic better than the Central American cases because the local cost side is high without equally low income.

5. India low-skill recent-arrival cell
   - Mean income about `28.4k`
   - Medicaid share about `25.0%`
   - Destination-weighted school spending about `15.2k`
   - Destination-weighted rent about `1679`
   - Mean household children about `0.96`
   - Interpretation: this is a small low-skill slice of a generally high-skill migration stream. The cell is real in the warehouse, but it should not be overgeneralized. Still, it is one of the clearest proxy cases for `federal better / state-local worse`.

### Bucket B: likely negative on both federal and state-local margins

These groups have low observed income and/or high Medicaid/public-assistance shares plus high child intensity or school-cost exposure.

1. Afghanistan
   - Mean income about `13.6k`
   - Medicaid share about `81.0%`
   - Public assistance about `20.4%`
   - Mean household children about `3.62`
   - Share with children about `93.5%`
   - Interpretation: this is the clearest `negative on both sides` case in the current warehouse.

2. Haiti
   - Mean income about `19.0k`
   - Medicaid share about `35.3%`
   - Public assistance about `6.9%`
   - Destination-weighted school spending about `19.0k`
   - Mean household children about `1.59`
   - Interpretation: high local-cost exposure with weak federal-side proxies.

3. Honduras
   - Mean income about `22.2k`
   - Medicaid share about `15.1%`
   - Mean household children about `1.65`
   - Share with children about `78.1%`
   - Interpretation: less transfer-heavy than Afghanistan or Haiti, but very high child intensity and weak income still point negative overall.

4. Guatemala
   - Mean income about `25.6k`
   - Medicaid share about `19.5%`
   - Mean household children about `1.38`
   - Share with children about `65.9%`
   - Interpretation: very large population and high local family load. Not necessarily the worst federally, but local burdens are clearly salient.

5. El Salvador and Nicaragua
   - Mid-to-lower income low-skill cells
   - Elevated child intensity
   - Concentration in relatively expensive states
   - Interpretation: these look more like broad negative or at best weakly mixed cases than split-positive cases.

### Bucket C: mixed / ambiguous

1. Mexico
   - This is the dominant case by scale, so it drives any aggregate statement.
   - Mean income about `24.8k`
   - Medicaid share about `21.5%`
   - Mean household children about `1.23`
   - Destination-weighted school spending about `15.2k`
   - Destination-weighted rent about `1716`
   - Interpretation: not obviously a federal positive case, not obviously a catastrophe case. It is large, middling on income, family-heavy, and heavily exposed to local housing and school costs. Aggregate national rhetoric about low-skill immigration often really means Mexico plus northern Central America.

2. Venezuela
   - Mean income about `32.3k`
   - Medicaid share about `9.8%`
   - Public assistance near zero
   - Mean household children about `0.83`
   - Destination-cost exposure is high
   - Interpretation: on the proxies, this is one of the strongest split candidates. But the World Bank metadata marks this origin as `Not classified`, and the sample is much smaller than Mexico or Guatemala. Use carefully.

3. Myanmar
   - Mean income about `28.8k`
   - Medicaid share about `61.2%`
   - Mean household children about `1.81`
   - Interpretation: conflicting signals. The income number is not weak, but transfer use and family intensity are high. This looks mixed rather than clearly split-positive.

## What the warehouse supports saying now

1. The largest recent low-skill origin groups in the 2023 ACS-based warehouse are overwhelmingly from Latin America and the Caribbean, especially Mexico and northern Central America.
2. The origin groups most exposed to `state-local` burdens are those with high child intensity and concentration in high school-spending, high-rent states. Afghanistan, Haiti, Honduras, Guatemala, and El Salvador are strong examples.
3. The best current candidates for `federal better / state-local worse` are not the largest groups. They are smaller low-skill cells with somewhat better income and weaker transfer-use proxies but still substantial exposure to costly destinations: Cuba, Brazil, Dominican Republic, Venezuela, and some East/South Asian low-skill cells.
4. Mexico is the central aggregate case and is best described as mixed. It is too large to ignore and too moderate on these proxies to fit a clean slogan.

## What this does not justify saying

1. It does not justify a claim that any named origin group is `fiscally positive overall`.
2. It does not justify a causal claim that origin alone determines fiscal impact.
3. It does not justify ad hoc ethnic or civilizational bins like `not Japan, not EU`.
4. It does not justify ignoring descendants. Child intensity is part of the local ledger, not noise.

## Next analytical upgrade

If we want a real incidence estimate rather than a proxy ranking, the next build should add:

1. federal tax/transfer microsimulation inputs by household, not just observed income and selected benefit proxies
2. household-level child counts and ages tied more directly to school-age exposure
3. a better renter-incidence model than state median gross rent alone
4. legal-status or admission-channel conditioning from OHSS where linkable
5. metro-level rather than state-level destination costs

## Bottom line

The clean statement is:

Low-skill immigration is not one object. In the current warehouse, the strongest candidates for a `federal better / state-local worse` split are smaller low-skill cells from origins like Cuba, Brazil, Dominican Republic, Venezuela, and some East/South Asian streams, while the largest low-skill streams from Mexico and northern Central America look more mixed or outright locally negative because child intensity and destination-cost exposure are materially higher.
