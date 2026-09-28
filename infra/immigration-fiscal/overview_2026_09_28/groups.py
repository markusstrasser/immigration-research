"""Conceptual groups for the confidence ladder, in order of how much each moves the answer.

Each group holds curated findings: one short sentence that may merge several ladder entries.
Every ladder entry must appear exactly once: in a finding's `refs`, in a group's `minor` list
(kept, not summarised), or in RETIRED (superseded or withdrawn, with its successor).
`build.py` refuses to write the page otherwise, so a new ladder entry must be placed here.
Prose follows ASD-STE100 habits: short sentences, active voice, one idea per sentence.
Numbers are copied from the cited ladder entries.
"""

# Old layer (research/immigration-confidence-ladder.md, "# Immigration confidence ladder", April-June)
# is keyed "o<N>"; the current layer by its number.
OLD_LAYER = [f"o{i}" for i in range(1, 52)]

RETIRED = {
    **{k: "April–June layer; re-rated in the September layers" for k in OLD_LAYER},
    52: "old SIPP outputs; replaced by the CPS ledgers (123, 161)",
    62: "early 2024 account; replaced by 123 and the complete account",
    76: "partial-ledger additions; replaced by the complete ledger (123, 172)",
    78: "crime cost per adult; replaced by the victim cost (189)",
    93: "superseded by 98", 94: "superseded by 99", 95: "superseded by 100",
    96: "superseded by 101", 97: "superseded by 102",
    121: "pre-repair aggregate; replaced by 123 and 172",
    122: "qualifies 121; replaced by 123 and 172",
    130: "pre-repair balance; replaced by 161 and 172",
    137: "compounds a superseded balance; replaced by 207",
    138: "withdrawn in the September 19 repair; replaced by 194",
    155: "exact-reproduction rating withdrawn",
    164: "superseded by 198",
    231: "subsumed by 238–239",
}

GROUPS = [
    dict(
        id="account", title="The annual account",
        size="The headline: $322–387bn a year",
        why=("The account asks one question. In 2024, how much better off would all other US residents be "
             "if the Mexican-origin population (40.9M people, three generations) were not here, with public "
             "services scaled to the smaller population?"),
        terms=[("counterfactual", "the world we compare with; here, the same US without the group"),
               ("specification", "one full set of choices; the range runs over 64 of them (ends 48 and 11)"),
               ("standard error", "sampling noise; about $10.6bn here")],
        findings=[
            dict(refs=[239, 193, 219, 229],
                 text="The adopted case is $322–387bn a year, $7.9–9.5k per member. It grew as costs held at zero "
                      "were priced: $165–197bn (Sept 20), $203–250bn (Sept 23), $201–246bn (Sept 24), $258–292bn "
                      "(Sept 26, schools at full cost), $322–387bn (Sept 27)."),
            dict(refs=[184], text="Sampling noise is about ±$21bn (95%). The choices below move the number more."),
            dict(refs=[161, 169],
                 text="The group's young age mix hides cost. At a common age mix the per-person gap is $7,049, "
                      "against $4,093 raw. A snapshot flatters young groups in general."),
            dict(refs=[123, 125, 126, 128, 172, 119],
                 text="The older ledger (Sept 17–19) is a different object: a gap against third-plus whites, about "
                      "$190–290bn a year around $217bn. Matching by state or metro does not shrink it. A negative "
                      "gap is not a negative balance: the partial balance was positive."),
            dict(refs=[54, 55],
                 text="CBO's $897bn lower federal deficit (2024–2034) and Colas–Sachs's positive channel are "
                      "different objects: federal only, all origins, projections with growth effects."),
        ],
        minor=[],
    ),
    dict(
        id="services", title="How public services grow with people",
        size="Sets the sign; $20–60bn per line",
        why=("Taxes paid minus benefits received favour other residents by about $60–70bn. Public services "
             "reverse the sign. If less than 3–14% of service costs grow with population, the sign flips."),
        terms=[("response (elasticity)", "the % rise in a budget for each 1% rise in users"),
               ("average vs marginal cost", "cost per user now vs the cost of one more user"),
               ("sign break-even", "the response at which the account turns from cost to gain")],
        findings=[
            dict(refs=[230, 215, 252],
                 text="Schools cost their full average per pupil: spending rises about 1% per 1% more pupils "
                      "(+$46–58bn over CBO's year-one 0.63–0.66). In the 2022–24 newcomer surge, money followed "
                      "pupils only about half, and late: that is the short run."),
            dict(refs=[237], text="Roads and parks grow 0.73% and 0.95% per 1% more residents: +$19–30bn."),
            dict(refs=[211, 165, 227],
                 text="General government responds at 0.60–0.85, from the cross-state scale of administration. "
                      "No county or bond-market design can tell it from 0 or 1."),
            dict(refs=[141, 149],
                 text="Natives did not flee public schools, and local budgets did not tilt from schools to police "
                      "as the Hispanic share rose."),
            dict(refs=[80],
                 text="Every fiscal study prices congestible services at average cost. Prison capacity binds in "
                      "8 states, where capital adds 18–27% to a prisoner-year."),
        ],
        minor=[],
    ),
    dict(
        id="conventions", title="Costs held at zero by convention",
        size="$34–56bn adopted; +$74–77bn and −$27bn waiting",
        why=("Budget and national-accounts rules set some costs to zero without measuring them. "
             "We price each one and show a band."),
        terms=[("opportunity cost of capital", "what public capital could earn if used elsewhere"),
               ("cash vs accrual", "count money when paid, or the promise when earned")],
        findings=[
            dict(refs=[238],
                 text="Adopted: a 2–3% real return on public capital, $34–56bn, and every government enterprise "
                      "responding. The return is imputed; it never enters debt. At 7% the case is $406–462bn."),
            dict(refs=[257, 146],
                 text="Waiting: Social Security and Part A on accrual add $77.3 / $73.6bn under current law "
                      "(payable benefits); scheduled benefits add $106–112bn."),
            dict(refs=[253],
                 text="Candidate: property taxes respond in the long run, −$27.2bn. Defense stays at zero; a "
                      "GDP-share bound would add $47.5–72.0bn."),
        ],
        minor=[],
    ),
    dict(
        id="data", title="Measured inputs: taxes, benefits, counts",
        size="Gross ±$50bn each side; net about $11bn",
        why=("Survey data carry known errors. Each tax and benefit key is tested against records the account "
             "did not use. Taxes were overstated by about $49–50bn and spending by $51–54bn."),
        terms=[("allocation key", "the share of a national total charged to the group"),
               ("imputation", "Census fills missing answers with a similar person's answers"),
               ("held-out test", "a check against data the model never saw")],
        findings=[
            dict(refs=[204, 208],
                 text="Census fill-ins give the group too much income; the account understated its cost by "
                      "$9–15bn. With every correction together the net move is about $11bn."),
            dict(refs=[209], text="The CPS counts the Mexico-born 9–13% above the ACS; about 11.1M is right."),
            dict(refs=[206, 173, 175, 210],
                 text="Medical: pooled over nine MEPS years, ethnicity adds no public medical cost in total. "
                      "Medicaid long-term care was over-charged by $11.1bn (7.4% of dollars, not 12.25%)."),
            dict(refs=[217, 216, 249],
                 text="No fear-driven under-reporting of benefits (+$2.2bn). IRS data show the income-tax key is "
                      "too flat at the top; an IRS-matched key lowers the case by $3.2bn (candidate)."),
            dict(refs=[85, 77, 254, 220],
                 text="Legal status does not drive the gap. Off-books work is already taken out; the survey keys "
                      "add about $0.2–0.4bn more."),
            dict(refs=[255, 256, 188, 192],
                 text="Tests set before looking: the frame predicts births and hospital charity care where they "
                      "land. Courts, police and prisons by use add $5.9bn."),
            dict(refs=[225, 90],
                 text="Consumption taxes are keyed on spending, net of saving and remittances (−$4.1bn). "
                      "Remittances cut sales tax by only $1.3–2.3bn nationally."),
            dict(refs=[127, 129],
                 text="The earnings gaps replicate on the ACS, and one tax calculator gives the same income-tax "
                      "gaps on CPS and ACS within 4%."),
        ],
        minor=[],
    ),
    dict(
        id="time", title="Time: past years, debt, interest, lifetimes",
        size="$2.8–3.7tn over ten years; $31–42bn interest beside",
        why=("Only 2024 is measured. Earlier years are a model. Lifetimes use a separate ledger with a "
             "reference group. Do not add them to the annual number."),
        terms=[("back-cast", "a model of past years from today's position and past national data"),
               ("stock vs flow", "debt is an amount; a yearly gap is an amount per year"),
               ("discount rate", "converts future dollars to today; 3% here")],
        findings=[
            dict(refs=[162, 251],
                 text="Carried back, the cost is $2.8–3.7tn over 2015–2024, without interest. The group got "
                      "pandemic payments at 0.87–1.03 of others per person, not 2.34."),
            dict(refs=[207],
                 text="If the federal part was borrowed, it left $0.96–1.29tn of debt; 2024 interest on it is "
                      "$31–42bn. It stays beside: removing the group does not remove old debt."),
            dict(refs=[131, 158, 159, 241],
                 text="Per founder, the Mexican lineage runs $1.29M behind the white lineage undiscounted "
                      "($513k at 3%); descendants carry 57%. One more white-profile child is worth $160–240k "
                      "more to the treasury."),
            dict(refs=[240, 247, 235],
                 text="Mexico-born who arrived at 50+ cost others $5.7–5.8bn a year. An IR-5 parent who adjusts "
                      "inside the US costs about $237k at 3%, against $274k for a new arrival."),
        ],
        minor=[],
    ),
    dict(
        id="social", title="Costs outside the budgets",
        size="+$49–59bn beside the account, more waiting",
        why=("Some costs never pass through a budget: crime victims, traffic, housing, fear, pollution. "
             "They are priced beside the account. With them the total is $371–446bn."),
        terms=[("externality", "a cost that falls on people outside the transaction"),
               ("value of a statistical life", "the price used for a death in cost-benefit analysis"),
               ("normalized", "the same item for as many average residents, subtracted")],
        findings=[
            dict(refs=[189], text="Violent crime by group members costs victims about $29bn a year in full cost."),
            dict(refs=[195], text="Traffic costs other commuters $12–14bn a year now that roads grow."),
            dict(refs=[190, 79, 180, 183, 57],
                 text="Rents rise about 1% per 1% more people. Other renters pay about $34bn more; landlords, "
                      "mostly other residents, get it. Net for others: a small gain of $0.7–3.5bn."),
            dict(refs=[258], text="Fear, private security and school discipline add $7.9bn (adopted into the rows)."),
            dict(refs=[260],
                 text="Fine-particle pollution from the group's consumption: about 4,900 deaths among others, "
                      "$69.7bn. The group pollutes 0.65× an average resident per head, so the normalized "
                      "figure favours it by $46.5bn."),
            dict(refs=[261], text="Infectious disease and food safety: about $0.3bn a year."),
            dict(refs=[248, 81, 91, 243, 246, 222],
                 text="School quality: state NAEP shows no white loss with the Hispanic share. Across countries "
                      "and in Germany, immigration explains a small part of falling scores."),
            dict(refs=[262, 89, 142],
                 text="Connectedness is lower where the Hispanic share is higher, mostly through segregation, and "
                      "it pays off no more in big counties. Neighbourhoods are not worse kept at equal income."),
            dict(refs=[98, 101, 102],
                 text="Unpriced and not bounded: native fertility, city productivity, political effects."),
        ],
        minor=[],
    ),
    dict(
        id="whopays", title="Who pays and who gains",
        size="Moves who loses, not the total",
        why="State and local budgets carry about 85%. Renters and less-educated workers lose most.",
        terms=[("incidence", "which households finally bear a cost"),
               ("welfare weights", "how much a dollar counts for rich vs poor"),
               ("λ (cost of public funds)", "the full cost of raising $1 of tax: 1.16–1.5")],
        findings=[
            dict(refs=[226], text="17–18% of other residents come out ahead, mostly landlords and the top tenth."),
            dict(refs=[194],
                 text="Financed by tax shares, the top fifth pays 62%. Financed by equal cuts, the bottom fifth "
                      "loses 12.4% of its resources."),
            dict(refs=[250],
                 text="World view: the group gains much by living here; at equal weights the world total is "
                      "positive (central +$364bn). The US side is behind if the group's dollar counts below 0.61."),
            dict(refs=[139, 213],
                 text="Native flight from California costs about $2.1bn of revenue. Race preferences cost white "
                      "natives about $4.0bn."),
        ],
        minor=[],
    ),
    dict(
        id="work", title="Work, wages and production",
        size="+$9–13bn net; $66–166bn moved between workers",
        why="The group's work makes the economy bigger. Most of that gain is its own wages.",
        terms=[("immigration surplus", "extra income natives get because immigrants work here"),
               ("ε (substitution)", "how easily one kind of worker replaces another")],
        findings=[
            dict(refs=[166, 176, 181],
                 text="The production gain to others is $8.8–13.3bn. Imperfect substitution (ε = 3) doubles it, "
                      "but direct estimates of ε are 8.7–17.9, near the account's default."),
            dict(refs=[191, 199],
                 text="Less-educated natives earn 2.2–7.0% less ($66–166bn); more-educated natives earn more."),
            dict(refs=[132, 198, 200, 203],
                 text="Cheaper services, more work by native women and care add about $4.1bn inside the account; "
                      "cheaper construction is already in the production term."),
            dict(refs=[201, 156],
                 text="City size and schooling mix nearly cancel (+$13.9bn, proposed). Creative work per head is "
                      "about three quarters of whites' at equal schooling."),
            dict(refs=[53, 59, 99, 120, 136, 140, 182],
                 text="The wage and automation designs tested here do not identify native wage effects; the "
                      "instruments lose power after 2000."),
        ],
        minor=[],
    ),
    dict(
        id="generations", title="Generations and assimilation",
        size="Decides the future flow",
        why="All three generations are net costs today. Progress stalls after the second.",
        terms=[("transmission", "how much of the parents' gap reaches the children"),
               ("ethnic attrition", "descendants who stop reporting Mexican origin"),
               ("selection", "migrants differ from those who stay home")],
        findings=[
            dict(refs=[224],
                 text="On the adopted case, in their own generation: Mexico-born $78–94bn, second generation "
                      "$128–153bn, third-plus $100–156bn a year."),
            dict(refs=[178, 232, 236],
                 text="The second generation closes 76% of the no-diploma gap but 31% of the college gap. About "
                      "0.84 of the college gap stays into the third-plus generation."),
            dict(refs=[74, 75, 86, 92, 133, 174, 197, 228],
                 text="Mexican migrants come from the middle of Mexico's schooling, the least selected large "
                      "stream. Children regress to an origin-specific mean."),
            dict(refs=[163, 134],
                 text="Relative income was flat 2008–2016 and has risen since. Recent arrivals carry the "
                      "smallest gap."),
            dict(refs=[83, 115, 105, 106, 108, 113, 124],
                 text="Test and custody gaps narrow to the third generation and are unclear after; small samples."),
            dict(refs=[67, 88, 100, 116],
                 text="39M people by generation; US-born fertility at or below white; the health advantage "
                      "fades after the first generation."),
            dict(refs=[154],
                 text="Fed measured assimilation rates, Clemens–Pritchett's model loses its Mexico conclusion."),
        ],
        minor=[103, 107, 109, 111, 112],
    ),
    dict(
        id="crime", title="Crime and custody rates",
        size="Feeds the $29bn victim cost",
        why="Immigrants offend less. US-born Mexican-origin men are held at about twice the white rate.",
        terms=[("rate ratio", "one group's rate over another's"),
               ("clearance rate", "the share of crimes that end in an arrest")],
        findings=[
            dict(refs=[144, 61],
                 text="First generation: lower. Undocumented Texans' cost-weighted felony charges are 0.40–0.43 "
                      "of the US-born rate."),
            dict(refs=[65, 66, 68, 70, 196],
                 text="US-born Mexican-origin men: 1.7–1.9× the white custody rate raw, 2.1–2.3× corrected. The "
                      "3.5× figure is from 2000."),
            dict(refs=[82], text="About 73% of the Hispanic–white male custody gap is parental income."),
            dict(refs=[202, 218, 148],
                 text="Police records: Hispanic offenders at 2.30× the white murder rate, 0.92–1.18× all residents."),
            dict(refs=[143], text="One cleared homicide costs the treasury $1.5–1.8M against $13.1M social cost."),
            dict(refs=[214], text="Noncitizen fraud runs at the same ratio as all federal crime, 1.8–2.0×."),
            dict(refs=[56, 63, 64, 69],
                 text="Nativity, race and generation are separate measures; recording failures need bands."),
        ],
        minor=[],
    ),
    dict(
        id="comparators", title="Other groups as benchmarks",
        size="Scale checks beside the total",
        why="The same rules run on other groups show whether the result is special.",
        terms=[("re-key", "the same account with another group's shares"),
               ("replacement", "the group against an equal number of another group")],
        findings=[
            dict(refs=[263],
                 text="Against 40.9M whites the group costs $315–330bn a year more (accrual, or white rates at "
                      "the group's ages); $406–412bn with local whites by state; $155–157bn on raw cash, "
                      "because whites are old."),
            dict(refs=[259],
                 text="Non-Hispanic Black residents (rough): $549–595bn, 1.5–1.7× per member."),
            dict(refs=[150, 168, 171],
                 text="India-born adults: +$24k per adult-year. Degrees convert by admission route."),
            dict(refs=[71, 72, 73],
                 text="Europe: registers explain its data; the immigrant gap is mostly composition."),
        ],
        minor=[151, 152, 153, 167, 177, 179],
    ),
    dict(
        id="status", title="Legal status, flows and enforcement",
        size="Counts and routes",
        why="Status matters less for the fiscal gap than schooling does.",
        terms=[("residual method", "unauthorized = foreign-born minus legal records")],
        findings=[
            dict(refs=[157], text="Unauthorized stock: 14.6–15.8M for mid-2024 on the usual definition."),
            dict(refs=[185, 186, 187],
                 text="About half of low-education Mexico-born parents are unauthorized. Few legalize: most who "
                      "did used 245(i), closed in 2001."),
            dict(refs=[242], text="The IR-5 parent doubling is processing, not a Mexico surge."),
        ],
        minor=[118],
    ),
    dict(
        id="civic", title="Civic life and politics",
        size="Unpriced",
        why="Immigration views converge by the third generation; redistribution views do not.",
        terms=[("adjusted gap", "a difference at equal age, schooling and year")],
        findings=[
            dict(refs=[87, 104, 110, 117, 135],
                 text="Trust stays 10–12 points lower; redistribution and Democratic lean do not converge."),
            dict(refs=[147, 160],
                 text="The group moves 24 of 435 House seats; county share does not move presidential votes."),
            dict(refs=[233, 205, 170, 234],
                 text="Turnout gaps of 9–13 points at equal status; military service 0.79 of white; ties to "
                      "Mexico fade by G3."),
        ],
        minor=[114],
    ),
    dict(
        id="claims", title="Public claims checked",
        size="Specific posts and papers",
        why="Each entry tests one public claim against primary data.",
        terms=[],
        findings=[
            dict(refs=[212], text="\"Legalized fraud\" in California: payments are lawful and inside the account."),
            dict(refs=[244], text="Rochester \"80 of 82 on visas\": the roster counts medical schools."),
            dict(refs=[245], text="DHS credit to enforcement: the gradient was as steep before the surge."),
            dict(refs=[145], text="Marginal Revolution 2003–2026: 13 agree, 9 coordinate, 1 hard conflict."),
            dict(refs=[84, 221, 223],
                 text="No frivolous spending at equal income; Californians rarely leave over crime; street "
                      "vending did not hurt restaurants."),
        ],
        minor=[],
    ),
    dict(
        id="method", title="Method rules",
        size="How to read everything above",
        why="A clean regression is not a cause. A runnable calculation is not a theory test.",
        terms=[("non-significance ≠ zero", "a wide interval does not show no effect")],
        findings=[
            dict(refs=[58, 60], text="Controls and passed placebos do not identify causes; the old tally is withdrawn."),
        ],
        minor=[],
    ),
]
