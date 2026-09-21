# Muslim-majority origins in the US: fiscal position, attitudes, extremism counts, mosque funding

Model self-report: claude-fable-5-1 (parent synthesis); two reader lanes ran on claude-opus-5.
2026-09-21. Operator question: what about Islamists and Muslim high-skill immigrants, and who
funds their mosques?

**Verdict:** On the measures this repo can make, the high-education Muslim-majority birthplaces
are fiscally positive and their degree holders earn like other degree holders admitted the same
way; the weak groups are the refugee-route origins, which are not high-skill, and
Bangladesh-born residents, who combine 50% degree holding with 40% Medicaid enrolment. The one
difference that does not go with admission route is women's employment, 13–17 points lower for
Muslim-majority origins [exploratory]. Where religion itself is observed (Pew 2017), US Muslims
match the public on degrees and on incomes above $100,000, are over-represented under $30,000,
and reject violence against civilians at the public's rate (84% against 83%). Foreign-born
terrorism on US soil is 3,046 murders in 50 years, 97.8% of them on one day, by visitors on
tourist and student visas. The European evidence is much worse (44% consistently
fundamentalist; Denmark's MENAPT group negative in both generations), and its own author says
it does not transfer to the US, because US Muslims were selected differently. Mosque funding has
no ledger: houses of worship are exempt from the IRS return by statute, the only systematic
survey has no foreign-money item, and what it does measure is small and local (median budget
$80,000). Foreign-state money is documented case by case, at uneven evidentiary grades.
[INFERENCE from the sections below; 15 of 15 decisive quotes re-checked by the parent against
the cached primary texts]

Sources: [mosque funding notes](../infra/immigration-fiscal/muslim_origins_2026_09_21/notes/mosque_funding.md) (ids A-),
[outcomes, attitudes, extremism notes](../infra/immigration-fiscal/muslim_origins_2026_09_21/notes/outcomes_attitudes_extremism.md) (ids B-),
collected under [`BRIEF.md`](../infra/immigration-fiscal/muslim_origins_2026_09_21/BRIEF.md), both directions required.

## 1. What our own data show (birthplace, not religion)

Census surveys do not ask religion, so every row here is a birthplace. Emigrants are not a
religious cross-section: Iran-, Egypt-, Lebanon- and Nigeria-born US residents include large
non-Muslim shares [TRAINING-DATA].

| Born in | Degree, 25–64 | Balance per adult-year | At native ages | Medicaid, all ages | Degree holders ≥ $100k | Women employed |
|---|---:|---:|---:|---:|---:|---:|
| Iran | 67% | +$21,228 | +$22,292 | 19% | 40% | 70% |
| Egypt | 69% | +$17,488 | +$14,881 | 29% | 28% | 63% |
| Turkey | 70% | n/a | n/a | 12% | 36% | 59% |
| Pakistan | 62% | +$5,331ᵃ | +$2,329ᵃ | 25% | 28% | 54% |
| Bangladesh | 50% | +$5,331ᵃ | +$2,329ᵃ | 40% | 20% | 52% |
| Iraq | 33% | n/a | n/a | 44% | 26% | 50% |
| Afghanistan | 30% | n/a | n/a | 62% | 17% | 37% |
| India (reference) | 86% | +$29,174 | +$21,832 | 7% | 53% | 69% |
| All natives | | +$2,785 | +$2,785 | | | |

ᵃ Pakistan and Bangladesh are one pooled group in the CPS account (interval −$1,109 to +$11,772
at own ages). Balances: ladder 168–169 (CPS ASEC 2025, personal allocation; Iran and Egypt rest
on thin samples). Medicaid and degree shares: ACS 2024, all arrival years. Last two columns: ACS 2024,
entered 2000 or later (ladder 171). Degree holders born in Pakistan or Bangladesh pay $12,947 a
year less than native degree holders (−$21,152 to −$4,742).

The pre-specified cross-birthplace test (ladder 171) returned "not settled" by its rule, with
clear parts: the employment-route share predicts degree conversion strongly; the origin's Muslim
share carries no earnings penalty among degree holders (−1.8 raw, +2.7 at equal route mix, both
intervals spanning zero); women's employment is 13–17 points lower whatever the route, and men's
is not. Pakistan (18% employment route, 76% family) and Bangladesh (8%, 82%) were admitted
mostly through family; Iraq and Afghanistan through refugee and special-immigrant routes.

## 2. Where religion is observed

| Measure, Pew 2017 (n = 1,001 Muslim adults) | US Muslims | US public | id |
|---|---:|---:|---|
| Foreign-born | 58% | | B1 |
| College graduates | 31% | 31% | B3 |
| Household income ≥ $100,000 | 24% | 23% | B5 |
| Household income < $30,000 | 40% | 32% | B5 |
| Own their home | 37% | 57% | B6 |
| Killing civilians often or sometimes justified | 12% | 14% | B8 |
| … rarely or never justified | 84% | 83% | B9 |
| Homosexuality should be accepted by society | 52% (27% in 2007) | 63% | B11 |

The often-quoted "76% against 59% say never" is a split inside "rarely or never" (the public
says "rarely" three times as often), not a difference in rejection (B9). Foreign-born Muslims
hold degrees more often than US-born Muslims, 38% against 21% (B4). Microdata are downloadable
with a free Pew account (B30). Not reached: New Immigrant Survey 2003 (religion, earnings and,
in the restricted tier, visa class), the Cooperative Election Study religion item, ISPU's poll.

## 3. Extremism counts

Cato Policy Analysis 991, 1975–2024: 237 foreign-born terrorists, 3,046 murders, 0.30% of US
murders in the period, an annual risk of 1 in 4.56 million; 97.8% of the deaths were on
11 September 2001 (B12, B13, B17). By route: 81 lawful permanent residents, 44 tourists (who
account for 2,829 of the deaths), 29 refugees, 25 students, 13 asylum seekers, 9 illegal entrants
with no murders in 50 years (B14–B16). Foreign-born Islamists account for 99.4% of the murders in
the paper's scope; its sentence says "all people killed in a terrorist attack on US soil", but
the paper counts no native-born terrorists (B17, B19). That exclusion is the gap for this repo:
nothing here measures the US-born second generation. New America's and GWU's offender databases
carry nativity and were not reached.

## 4. The European contrast

Koopmans 2015 (Turkish- and Moroccan-origin Muslims in six countries, 2008): 44% agree with all
three fundamentalism items, 65% put religious rules above national law, 57% reject homosexual
friends, 45% do not trust Jews, 54% see the West as out to destroy Islam, 26% are hostile to all
three out-groups against 1.6% of native Christians (B21, B22). The same paper says the result does not carry to the US, whose Muslim
population is "predominantly middle class and highly educated" (B23). Denmark's Finance Ministry,
2019: MENAPT immigrants −74,000 kr per person (−13bn kr), MENAPT descendants −109,000 kr
(−11bn kr), while all immigrants together are +3bn kr; the ministry attributes the immigrant gap
to employment rates (B24–B26). MENAPT is a birthplace grouping, as ours is (B28). Income-year
2019 (revised September 2023) is the latest edition the reader found; a later one was not ruled
out. The
descendants' figure being worse than the immigrants' is the European datum most relevant to the
operator's regression-to-the-mean question, and it is confounded by age: descendants are young.
[INFERENCE for the last clause]

## 5. Who funds US mosques

- **No ledger exists, by law.** 26 U.S.C. § 6033(a)(3)(A)(i) exempts churches from the annual
  return, and the IRS applies that to houses of worship generally (A1, A2).
- **The one systematic survey cannot see foreign money.** Bagby's US Mosque Survey 2020 (470
  interviews from a census of 2,769 mosques) has six income categories, none foreign (A7). What
  it measures is small and congregational: median budget $80,000, mean $276,500; 52% of income
  from Friday collections and pledges; $674 per participant a year against $1,732 for churches
  (A5, A8, A10). That is evidence against a large hidden subsidy, not a measurement of its absence.
- **Foreign-state money is documented case by case.**
  - Iran: the Alavi Foundation, which supports Shia Islamic centers in several states, was the
    target of a federal forfeiture action from 2008. The amended complaint alleged transfers to
    Bank Melli, owned by the Iranian government (A12); prosecutors won summary judgment in 2013
    and announced a settlement on distributing the forfeited properties (New York, Maryland,
    Virginia, Texas, California) in 2014 (A11). A jury verdict for the government followed in
    2017 [pointer only: Bloomberg, 2017-06-29, via the Wikipedia article; not read]. The Second
    Circuit decided the case again on 2019-08-09 (934 F.3d 147, located through CourtListener,
    text not retrieved); as recalled, it vacated the verdict [TRAINING-DATA]. A 2026 SDNY release
    exists that the reader could not open. The final status must be read before this case is
    cited as adjudicated. [UNVERIFIED]
  - Saudi Arabia: two named mosques (King Fahd Mosque, Los Angeles; the Islamic Center of
    Washington) were acknowledged on the king's own website as receiving official support; the
    quantified Saudi figures are worldwide self-reports (A14, A15). The Freedom House 2005 study
    is a convenience collection of publications from "more than a dozen" mosques, gathered in
    2003–04, and says so (A13, A16).
  - Turkey (Diyanet Center of America), the North American Islamic Trust's property holdings,
    Qatar and Kuwait: not documented this epoch; sites failed or were not attempted.
- **The open route to a partial ledger:** Form 990s of the non-church Islamic nonprofits that do
  file (NAIT, Alavi, ISNA, ICNA), through ProPublica's Nonprofit Explorer.

## 6. What this does and does not support

[FRAMING-SENSITIVE] "Islamists" and "Muslim immigrants" are different populations; the evidence
above is about the second and says little about the first beyond offender counts. For the US the
better-measured evidence is reassuring on earnings, degrees and attitudes to violence, mixed on
social attitudes and poverty, and silent on the second generation and on foreign funding. The
European evidence is alarming and is about differently selected populations; the mechanism both
sides' data point to is selection at admission, which ladder 171 also finds for degree
conversion.

[DISCONFIRMATION] Strongest items against the reassuring reading: the statutory disclosure hole
means absence of funding evidence is guaranteed rather than measured (A1, A7); Denmark's
descendants are more negative than its immigrants (B24); women's employment is lower regardless
of route (ladder 171), which depresses household taxes for a generation; Cato omits the
native-born (B19); Pew's 2017 survey predates the 2021–24 inflow.

[INSTRUMENT] LLM-conducted on a charged topic, with a known disposition toward the reassuring
reading; the readers were required to record both directions with equal care, the route test was
specified before its data, and the parent re-checked 15 quotes. See `notes/llm-bias-caveat.md`.

## Next

1. Alavi: read 934 F.3d 147 and the 2026 SDNY release; settle what is adjudicated.
2. Form 990s for NAIT, Alavi, ISNA, ICNA: the partial ledger.
3. New America and GWU offender tables by nativity: the second-generation gap.
4. Pew 2017 microdata (free account, operator action): income and attitudes by nativity and origin.
5. New Immigrant Survey 2003 public-use files (ICPSR 38031, 38061; listed in the sociology
   frontier memo as pullable): religion with earnings for new green-card holders. Visa class sits
   in the restricted tier. The outcomes reader names it the highest-value source not reached.
