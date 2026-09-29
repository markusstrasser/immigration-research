# Sources read for the key's bias: quoted text and table cells

Read 2026-09-30. Neither file is kept in the lane; the hashes identify the copies read.

## SSA, "Spotlight on SSI benefits for noncitizens"

`https://www.ssa.gov/ssi/spotlights/spot-non-citizens.htm`, read through the Wayback Machine copy
`https://web.archive.org/web/2025id_/https://www.ssa.gov/ssi/spotlights/spot-non-citizens.htm` because ssa.gov refuses
scripted requests (sha256 of the HTML: `4c32f124e91f8c0fd8ae646bf01079d7eb881c269c401749751cffd7487249df`).

> In general, beginning August 22, 1996, most noncitizens must meet two requirements to be potentially eligible for
> SSI: be in a qualified alien category; and meet a condition that allows qualified aliens to get SSI.

> If you are in one of the 7 "qualified alien" categories listed above, you may be eligible for SSI if you also meet
> one of the following conditions: You were receiving SSI and lawfully residing in the U.S. on August 22, 1996. You
> are LAPR with 40 qualifying quarters of work. Work done by your spouse or parent may also count toward the 40
> quarters of work, but only for getting SSI. [...] IMPORTANT: If you entered the United States on or after August 22,
> 1996, then you may not be eligible for SSI for the first five years as a LAPR even if you have 40 qualifying
> quarters of coverage. You are currently on active duty in the U.S. Armed Forces or you are an honorably discharged
> veteran [...]. You were lawfully residing in the U.S. on August 22, 1996 and you are blind or have a qualifying
> disability. You may receive SSI for a maximum of 7 years from the date DHS granted you immigration status in one of
> the following categories [...]: Refugee [...]; Asylee [...]

The seven qualified-alien categories are LAPR, conditional entrants before 1980, parolees for at least a year,
refugees, asylees, persons whose deportation or removal is withheld, and Cuban or Haitian entrants. A person in none
of them, including an unauthorized immigrant, is not a qualified alien.

## Bee and Mitchell (2017), "Do Older Americans Have More Income Than We Think?"

Census Bureau SEHSD Working Paper 2017-39, `https://www.census.gov/content/dam/Census/library/working-papers/2017/demo/SEHSD-WP2017-39.pdf`
(sha256 `515cec1f10c91b1cbdba00a034f80f4bfed3a43aa50f673c9105baa1e7c796eb`). CPS ASEC 2013 (income 2012) linked to SSA
and IRS records.

Text, p. 39 of the PDF text layer:

> CPS reporting of SSI benefits is more complex. Persons aged 18 to 64 appear to overreport SSI, while those aged 65
> and over only report 73 percent of the target amount.

Table 1, "Aggregate income estimates by age group: 2012" (billions): Supplemental Security Income, CPS PIK sample 37
(18–64) and 7 (65+), linked administrative 30 and 10, CPS as % of admin **123.2%** and **72.7%**.

Table 6, Panel A, "Social Security recipiency by data source: 2012", people aged 65 and over. Columns: true
negative, false positive, false negative, true positive, total CPS receipt, total linked receipt, false-negative rate.

| Row | TN | FP | FN | TP | CPS receipt | Linked receipt | FN rate |
|---|---|---|---|---|---|---|---|
| White, not Hispanic | 0.068 | 0.051 | 0.056 | 0.825 | 0.876 | 0.881 | 0.064 |
| Hispanic (any race) | 0.128 | 0.084 | 0.112 | 0.675 | 0.760 | 0.788 | 0.143 |
| Foreign born | 0.191 | 0.104 | 0.115 | 0.590 | 0.694 | 0.705 | 0.163 |
| Not a citizen | 0.318 | 0.126 | 0.115 | 0.440 | 0.566 | 0.555 | 0.207 |

Panel B of Table 6 is retirement income. The paper has no SSI receipt table by race, Hispanic origin or nativity.

## What a bounded search found

A researcher sub-agent (40 turns, stopped at its limit) found no linked survey-administrative study that splits SSI
misreporting by Hispanic origin, Mexican origin, nativity, citizenship or interview language. It covered Gathright and
Crabb (2014, SIPP), Bee and Mitchell (2017, CPS), Bee, Dushi, Mitchell and Trenkamp (2024, HRS), Nicholas and Wiseman
(2009, CPS), Scherer and Giefer (2024, SIPP) and Giefer et al. (2015, SIPP). Only the Bee and Mitchell cells above were
re-read here from the primary PDF. Not checked: Huynh, Rupp and Sears (2002), Meyer, Mok and Sullivan, and Celhay,
Meyer and Mittag.
