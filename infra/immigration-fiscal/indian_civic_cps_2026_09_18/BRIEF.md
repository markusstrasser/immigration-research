# Lane: turnout, volunteering and charitable giving by birthplace from CPS supplements (2026-09-18)

## Goal
Microdata answer to "do they take part and give": India-born and second-generation Indian-origin adults against other foreign-born groups and US-born non-Hispanic whites, from CPS supplements that carry birthplace (PENATVTY, India=210; verify in each year's data dictionary) and parents' birthplace (PEFNTVTY/PEMNTVTY).

## Data
1. **CPS Voting and Registration Supplement**, November 2016, 2018, 2020, 2022, 2024: citizenship, registration, turnout (PES1/PES2 and the Census convention that non-response counts as not voting; report both conventions).
2. **CPS Volunteering and Civic Life Supplement**, September 2017, 2019, 2021, 2023: volunteered, hours, donated $25+ to charity, amount bracket if present, neighbour help, contacted official, group membership.
Routes: Census API microdata endpoints (`https://api.census.gov/data/<year>/cps/voting/nov`, `.../cps/volunteer/sep` or `civic`; check `variables.json`), else the public-use files at www2.census.gov/programs-surveys/cps/datasets/, else IPUMS CPS only if an extract already exists locally (do not create accounts). Census API key per the shared rules.

## Outputs
Weighted rates with SEs (supplement weight; successive-difference replicate weights if shipped, else a design-effect approximation, stated) for: India-born, China-born, Mexico-born, all other foreign-born, second-generation Indian-origin, US-born non-Hispanic white, all US-born. Turnout among citizens 18+; naturalization share among foreign-born by years since entry; volunteering and giving rates. Then a logit/LPM adjusting for age, sex, education, family income bracket, metro status and years in US, reporting the India-born coefficient raw and adjusted. Cell Ns beside every rate; suppress cells under 50 unweighted.

## Arms that could reverse the headline
Citizens only vs all adults; education-matched (BA+ only); recent arrivals (<10 years) excluded; proxy responses excluded (the volunteer supplement is proxy-sensitive).

## Rules
Identical to `../ncvs_victim_offender_2026_09_18/BRIEF.md` §Rules (all lanes); read it and follow it. Own only this directory. Do not commit. Verification: second run reproduces `derived/` byte-identically (`cmp`); a gate asserts your all-population 2020 citizen turnout matches the Census published figure (fetch Table 1 of the P20 release and cache it) within 0.5 points.
