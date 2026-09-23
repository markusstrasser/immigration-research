# Does local spending shift from education toward law and order where the immigrant share rises? Not in the Census of Governments

## Audit correction — September 19, 2026

**Keep the associations; the causal sign is unresolved.** Invalidating an opposite-signed IV does not establish zero. The repo's Hispanic/foreign-born stock-share treatment also differs from the cited paper's unauthorized-arrival treatment, so confidence intervals cannot be compared as a matched replication without reconciling those quantities. The cited paper's own budget-share table is a separate source-reading question. [SOURCE: design and caveats below; mechanisms audit]

This supersedes conflicting interpretations below; calculations are retained as evidence. [Audit index](immigration-five-day-cross-check-2026-09-19.md).


**Verdict:** Not reproduced. On 3,126 counties across the 2007, 2012, 2017 and 2022 Censuses of Governments, aggregating every local unit inside a county, no arm shows local budgets shifting from education toward police, corrections and courts as the Hispanic or foreign-born share rises, and none shows total local spending per resident falling. The log of law-and-order over education spending moves by −0.154 (se 0.063) per 10 points of Hispanic share over 2007–2022 and −0.227 (0.113) over 2012–2022, that is toward education; the police share, the endorsed paper's strongest share result, is −0.463 (0.264) weighted and −0.435 (0.162) unweighted, and the 95% interval at this sample's own mean dose excludes the paper's +0.23 points. The opposite-signed shift is not itself identified: over 2007–2022 the pre-period placebo (−0.151) equals the estimate, and over 2012–2022 the estimate halves and loses significance when California alone is dropped, which its 2013 Local Control Funding Formula explains. The defensible statement is the null. Separately, the sentence Tabarrok quoted rests on the paper's log-level columns; in its own share specification the education share coefficient is +0.23 (se 0.61), and the 2025 revision drops the share columns while keeping the sentence in the abstract. [SOURCE: `infra/immigration-fiscal/local_spending_composition_2026_09_18/derived/estimates_composition.csv`; Tiburcio and Camarena 2023 Table 4, 2025 Table 3]

Date: 2026-09-18. Lane: `infra/immigration-fiscal/local_spending_composition_2026_09_18/` (four local scripts plus two Modal fetch scripts, seven derived files, reproduced byte-identically by the parent). Extends ladder 141 (school flight: local school revenue falls, state aid offsets) from revenue to the composition of total local spending. Descriptive, within state, no instrument (ladder 136).

## 1. The paper and the endorsement

Tiburcio and Camarena, "The Local Reaction to Unauthorized Mexican Migration to the US" (Tufts job-market paper, November 2023; revised May 2025), measure newcomers from 14 million Mexican consular ID records, instrument with two shift-share designs on 2002–06 municipality-to-county shares, and take fiscal outcomes from the 2012 and 2017 local-finance censuses. At the mean four-year inflow (0.55% of county population) they report local direct spending −2%, education per child −3%, the police share +0.23 points and the judicial share +0.15 points. Alex Tabarrok endorsed it on 2023-12-02: unauthorized inflows "reduce local public spending, and shift it away from education towards law-and-order." [SOURCE: archived post in `mr_archive_2026_09_18/derived/mr_posts.jsonl`; 2023 PDF via Wayback, 2025 PDF from the author's site, both cached]

Two facts the quoted sentence does not carry. In the share specification the education coefficient is +0.23 (se 0.61), so education's share of the budget does not fall even in the paper; the rise is in the police and judicial shares, offset across the other categories. The May 2025 revision drops the share columns from the table and keeps the sentence in the abstract. [SOURCE: 2023 Table 4 p. 25; 2025 Table 3 p. 22]

## 2. Data

Census individual-unit local-finance files for 2012, 2017 and 2018–2023, parsed with the two fixed-width layouts from the shipped documentation; direct general expenditure built from item-code prefixes E, F, G, J and I89 excluding utilities and intergovernmental flows. County sums reproduce the Census's own national local-government aggregate exactly, function by function (total $1,422.9bn, education $597.3bn, police $84.0bn, corrections $26.7bn, judicial $21.6bn in 2012). There is no 2007 individual-unit file on census.gov; 2007 comes from the Willamette Government Finance Database (341 MB, pulled in a Modal container), validated county by county against the Census build on the three overlapping waves to within 0.25%. Shares from ACS 5-year (2009, 2012, 2017, 2022) and the 2000 Census for the placebo. Only census years enter the estimates because the annual survey enumerates a sample of units. Connecticut drops out after 2012 on its planning-region FIPS change. [SOURCE: `derived/county_finance.csv`, `county_shares.csv`; RESULT.md Phase 2]

## 3. Estimates

Within-state long differences, population-weighted and unweighted, clustered on state, per 10 points of share change; 206 estimates across 38 arms.

| Outcome | 2007–2022 weighted | 2007–2022 unweighted | 2012–2022 weighted |
|---|---|---|---|
| log(law and order / education) | −0.154 (0.063) | −0.087 (0.057) | −0.227 (0.113) |
| Education share, points | +4.16 (1.23) | +2.25 (0.58) | +6.71 (2.06) |
| Police share, points | −0.46 (0.26) | −0.44 (0.16) | −0.30 (0.32) |
| Law-and-order share, points | −0.56 (0.42) | +0.25 (0.47) | −0.58 (0.65) |
| log total direct expenditure per resident | −0.022 (0.018) | +0.013 (0.027) | −0.002 (0.023) |
| log education per resident | +0.065 (0.038) | +0.039 (0.017) | +0.155 (0.064) |

Foreign-born share gives −0.209 (0.082) and −0.189 (0.065) on the ratio; the Mexico-born share (2012–2022 only) gives education +7.34 (2.13) and law and order +0.69 (1.82). Total spending per resident is flat in three arms and up in the fourth (+0.139, se 0.052, unweighted 2012–2022). [CALCULATION: `derived/estimates_composition.csv`]

## 4. Why the opposite sign is a null, not a reversal

- Pre-period placebo: the 2000–2009 Hispanic-share change predicts the 2007–2022 ratio change at −0.151 (0.059), equal to the contemporaneous −0.154, and predicts the police share at −1.09 (0.27) against −0.46. Counties on a long Hispanic-growth trajectory were already tilting toward education. On 2012–2022 the ratio placebo is clean (−0.119, se 0.115) but the police-share placebo is not (−0.78, se 0.32).
- Leave one state out: on 2012–2022 the ratio runs from −0.279 (dropping Texas) to −0.093 (dropping California, se 0.072); California is the only state whose removal changes the verdict, and its Local Control Funding Formula (2013–14 onward) routes state money to districts by English-learner and low-income counts. No single county drives the education share (Los Angeles removed: +6.71 to +6.05).
- Dropping the 25 largest counties, trimming under-10,000 counties and 1% tails: 2012–2022 unchanged; law and order goes from −0.58 to +0.24 (0.59), still zero.

At this sample's mean Hispanic-share change (3.23 points over 2007–2022, 2.08 over 2012–2022) the implied police-share move is −0.150 points [−0.317, +0.018] and −0.061 [−0.191, +0.069]; both exclude the paper's +0.23 at its own mean dose. [CALCULATION: `derived/loo_state_logratio*.csv`, `influence_education_share.csv`]

## 5. What this does not say

The consular-ID treatment is confidential and cannot be rebuilt, and this lane has no instrument. A resident share is a stock that nets out-migration, naturalisation and internal moves; the paper's newcomer count is a gross flow of recent unauthorized arrivals. Both can hold if the fiscal response is specific to that flow and offset in the stock. This is a failure to find the pattern in the observable correlate over a longer window, not a refutation of their causal estimate. For the scorecard it changes Tabarrok's row T4 from AGREE to AGREE on the backlash half and COORDINATE on the composition half. [INFERENCE]

## Sources

Tiburcio E, Camarena KR, The Local Reaction to Unauthorized Mexican Migration to the US, 2023 and 2025 versions (cached). Census Bureau Annual Survey of State and Local Government Finances individual-unit files 2012, 2017–2023 and technical documentation; Willamette Government Finance Database (2007); ACS 5-year via api.census.gov; 2000 Census SF1/SF3. Instrument note: LLM-assisted; every number reproduced by the lane scripts.


## Revisions — September 19, 2026

Corrected the interpretation for the reasons above; see the [decision](../decisions/2026-09-19-bind-report-claims-to-matched-estimands.md).

## Revisions — September 23, 2026

**The 2022 wave carries a financial-administration break; the weighted verdict survives it.** The
July 2026 re-release of the 2022 unit file raises administration's share of direct spending
between 2017 and 2022 as follows:

| County | 2017 | 2022 |
|---|---|---|
| New York County (NYC) | 1.6% | 8.9% |
| Philadelphia | 3.8% | 11.6% |
| Cook | 4.2% | 7.6% |
| Miami-Dade | 3.2% | 6.1% |

Those gains lower every other share in those counties. The estimator was rerun on shares that
leave administration out of the denominator in every year. Per 10 points of Hispanic share:

| Arm | Outcome | Published | Administration left out |
|---|---|---|---|
| Weighted | police | −0.30 | −0.36 |
| Weighted | law and order | −0.58 | −0.67 |
| Weighted | education | +6.71 | +6.68 |
| Weighted, 2017–2022 | law and order | −1.15 | −1.32 |
| Weighted, 2012–2017 (before the break) | law and order | +0.05 | +0.03 |

The unweighted arm does move: law and order goes from +0.49 (SE 0.28) to +1.11 (SE 0.40). The
break does not cause that move:
- the same gap appears in 2012–2017, before the break (+0.57 → +1.30);
- it is absent in 2017–2022;
- it survives dropping Florida, New York, Illinois and Pennsylvania;
- it disappears under the lane's own trim (−0.75 → −0.83).

The cause is a denominator effect in tiny counties. In Loving County, Texas, for example, the 2012
law-and-order share goes from 21.9% to 41.0% once administration leaves the denominator.

The verdict stands: no weighted arm shows a shift toward law and order. [CALCULATION:
`../infra/immigration-fiscal/gg_response_county_iv_2026_09_23/e23_other_lanes.py` →
`derived/e23_other_lanes.csv`, using this lane's own `estimate_composition.py` read-only; its
derived files are byte-identical before and after.] The same break shows up in the Census state
series for 2023, so any window ending in 2022 or later needs this check.
