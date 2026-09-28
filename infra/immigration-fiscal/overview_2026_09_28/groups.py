"""Conceptual groups for the confidence ladder, in order of how much each moves the answer.

Every ladder entry (1-51 in the April-June layer, 52-261 in the current layer) belongs to
exactly one group. `build.py` refuses to write the page if an entry is missing or listed twice.
Prose follows ASD-STE100 habits: short sentences, active voice, one idea per sentence.
Numbers in `points` are copied from the cited ladder entries; `build.py` gates the ones that
also live in a derived file.
"""

# Old layer (research/immigration-confidence-ladder.md, "# Immigration confidence ladder",
# dated 2026-04-10 to 2026-06-25) is keyed "o<N>"; the current layer is keyed by its number.

GROUPS = [
    dict(
        id="account",
        title="The annual account",
        size="The headline: $322–387bn a year",
        why=(
            "This group defines the main number. It asks one question. In 2024, how much better off "
            "would all other US residents be if the Mexican-origin population (40.9M people, three "
            "generations) were not here, and public services were scaled to the smaller population? "
            "The answer is $322–387bn a year, about $7.9–9.5k per member."
        ),
        terms=[
            ("counterfactual", "the world we compare with; here, the same US without the group"),
            ("net fiscal impact", "taxes the group pays minus what governments spend on it"),
            ("specification", "one full set of choices; the range runs over 64 of them (ends 48 and 11)"),
            ("standard error", "sampling noise; about $10.6bn here, so a 95% interval of about ±$21bn"),
        ],
        points=[
            ("239", "The adopted main case (September 27) is $321.8–387.4bn a year. Each step from "
                    "earlier cases adds exactly; the chart below shows every step."),
            ("193, 219, 229, 230", "The number grew because we priced things that earlier cases held at "
                    "zero: $165–197bn (Sept 20), $203–250bn (Sept 23), $201–246bn (Sept 24), "
                    "$258–292bn (Sept 26), $322–387bn (Sept 27)."),
            ("121–130, 161", "The older ledger (September 17–19) compares the group with a white reference "
                    "group. That is a different object: a gap, not a cost of removal."),
            ("161, 169", "Age structure hides the cost here. At a common age mix the per-person gap is "
                    "larger ($7,049) than the raw gap ($4,093)."),
            ("184", "Sampling noise is about ±$21bn (95%). It is small next to the choices below."),
            ("55", "CBO's much-quoted $897bn smaller federal deficit over 2024–2034 is a different object: "
                   "federal only, new arrivals of all origins, a projection with macro effects."),
        ],
        members=["o15", "o16", "o41", "o45", "o46", "o47",
                 54, 55, 62, 76, 119, 121, 122, 123, 125, 126, 128, 130, 161, 169, 172, 184,
                 193, 204, 219, 229, 239],
    ),
    dict(
        id="services",
        title="How public services grow with people",
        size="Sets the sign; swings of $25–60bn per line",
        why=(
            "This is the biggest assumption in the account. Taxes paid minus benefits received favour "
            "other residents by about $60–70bn. Public services turn the sign. The question is how much "
            "a school, police or road budget grows when the population grows. If less than 3–14% of "
            "service costs grow with people, the sign flips."
        ),
        terms=[
            ("response (elasticity)", "the % rise in a budget for each 1% rise in users"),
            ("average vs marginal cost", "cost per user now vs the cost of one more user"),
            ("congestible public good", "a service that gets worse or costs more when more people use it"),
            ("pure public good", "a service that costs the same with more people (defense, by assumption)"),
            ("sign break-even", "the response at which the account turns from cost to gain: 2.8–13.6%"),
        ],
        points=[
            ("230", "Schools are charged at full average cost per pupil. Across districts and states, "
                    "spending rises about 1% per 1% more pupils. This added $46–58bn over CBO's "
                    "year-one 0.63–0.66."),
            ("237", "Roads and parks respond in the long run: highways 0.73% and parks 0.95% per 1% more "
                    "residents. This added $19–30bn."),
            ("193, 211", "General government responds at 0.60–0.85 (was 0). A county test cannot tell "
                    "this from 0 or 1."),
            ("252", "In the 2022–24 newcomer surge in NYC, Chicago and Denver, staff and money followed "
                    "new pupils only about half, and late. That is the short run."),
            ("141, 149", "Natives did not flee public schools, and local budgets did not shift from "
                    "schools to police as the Hispanic share rose."),
            ("215", "The school line is slightly too low: the group's pupils sit in districts that "
                    "spend 3.4% more than their state average (+$3bn, proposed)."),
        ],
        members=["o7", "o13", 80, 141, 149, 165, 211, 215, 227, 230, 237, 252],
    ),
    dict(
        id="conventions",
        title="Costs held at zero by convention",
        size="$34–56bn adopted; +$74–77bn and −$27bn waiting",
        why=(
            "Budget and national-accounts rules set some costs to zero. They do not measure them as "
            "zero. We price each one and show a band. Two are adopted. Two wait for your decision."
        ),
        terms=[
            ("opportunity cost of capital", "what public buildings and roads could earn if used elsewhere"),
            ("cash vs accrual accounting", "count money when paid, or count the promise when earned"),
            ("present value (NPV)", "future money converted to today's dollars at a discount rate"),
            ("tax incidence", "who finally bears a tax, whatever its legal payer"),
        ],
        points=[
            ("238, 239", "ADOPTED. A 2–3% real return on public capital adds $34–56bn. BEA's lines carry "
                    "only depreciation. This cost is imputed. It is never cash and never enters debt."),
            ("239", "ADOPTED. Every government enterprise responds. Their operating loss adds $5.6bn; "
                    "the return on their capital is inside the $34–56bn."),
            ("257", "WAITING. Social Security and Medicare Part A on accrual add $77.3 / $73.6bn under "
                    "current law (payable benefits). Scheduled benefits are an arm: +$106–112bn."),
            ("253", "CANDIDATE. Property taxes respond in the long run, like the capital they pay for. "
                    "This lowers the case by $27.2bn."),
            ("239, 253", "STILL ZERO. Defense, old interest and business subsidies. A GDP-share bound "
                    "on defense would add $47.5–72.0bn; it stays beside."),
        ],
        members=[146, 231, 238, 253, 257],
    ),
    dict(
        id="data",
        title="Measured inputs: taxes, benefits, counts",
        size="Gross ±$50bn each side; net about $11bn",
        why=(
            "Survey data carry known errors. We test each tax and benefit key against records the "
            "account did not use. The tax side was too high by about $49–50bn. The spending side was "
            "too high by about $51–54bn. They nearly cancel."
        ),
        terms=[
            ("allocation key", "the share of a national total charged to the group"),
            ("imputation (hot-deck)", "Census fills in missing answers with a similar person's answers"),
            ("held-out test", "check a model against data it never saw"),
            ("measurement error", "a gap between the survey answer and the true value"),
        ],
        points=[
            ("208", "Census fill-ins give the group too much income. The account understated its cost "
                    "by $9–15bn."),
            ("209", "The CPS counts the Mexico-born 9–13% above the ACS. About 11.1M is the right level."),
            ("210", "Medicaid long-term care was over-charged by $11.1bn: the group draws 7.4% of it, "
                    "not 12.25%."),
            ("206", "Nine pooled MEPS years: ethnicity adds no public medical cost in total."),
            ("217", "No sign of fear-driven under-reporting of benefits; re-keying adds $2.2bn."),
            ("85", "Legal status is not what drives the gap. Imputed unauthorized and legal Mexico-born "
                   "adults have similar gaps."),
            ("249, 251, 254", "Candidates for the next case: IRS tax key −$3.2bn; workers' comp "
                    "−$1.5–2.0bn; payroll compliance about −$0.2–0.4bn."),
            ("255, 256", "Two tests set before looking: the frame predicts births and hospital "
                    "charity care where they land."),
        ],
        members=["o1", "o3", "o12", 52, 77, 85, 90, 127, 129, 173, 175, 188, 192, 206, 208, 209,
                 210, 216, 217, 220, 225, 249, 251, 254, 255, 256],
    ),
    dict(
        id="time",
        title="Time: past years, debt, interest, lifetimes",
        size="$2.8–3.7tn over ten years; $31–42bn interest beside",
        why=(
            "Only 2024 is measured. Earlier years are a model carried back on national series. "
            "Future years belong to lifetime and lineage models, which use a reference group. "
            "Each is a separate object. Do not add them to the annual number."
        ),
        terms=[
            ("back-cast", "a model of past years built from today's position and past national data"),
            ("stock vs flow", "debt is a stock (an amount); a yearly gap is a flow (an amount per year)"),
            ("discount rate", "the rate that converts future dollars to today; 3% here"),
            ("generational accounting", "follow a person and descendants over their whole lives"),
        ],
        points=[
            ("162, 251", "Carried back, the cost is $2.8–3.7tn over 2015–2024 and $4.8–6.8tn over "
                    "2005–2024, in 2024 dollars, without interest."),
            ("207", "If the federal part of 2005–2023 was borrowed, it left $0.96–1.29tn of debt. In "
                    "2024 its interest is $30.9–41.6bn, about $756–1,018 per member. It stays beside."),
            ("131", "One more child on the white age profile is worth $160–240k (at 3%) more to the "
                    "treasury than one more Mexican-origin resident."),
            ("158, 159", "Per founder, the Mexican lineage runs $1.29M behind the white lineage "
                    "undiscounted ($513k at 3%). Descendants carry 57% of it."),
            ("240", "Mexico-born who arrived at 50 or older cost others $5.7–5.8bn a year."),
            ("247, 235", "A Mexican IR-5 parent who adjusts inside the US costs about $237k at 3%, "
                    "against $274k for a new arrival."),
        ],
        members=[131, 137, 143, 158, 159, 162, 207, 235, 240, 241, 247],
    ),
    dict(
        id="social",
        title="Costs outside the budgets",
        size="+$49–59bn beside the account",
        why=(
            "Some costs never pass through a government budget. Crime victims, traffic, housing, "
            "fear and school quality are examples. We price them beside the fiscal account. With "
            "them, the total is $371–446bn a year."
        ),
        terms=[
            ("externality", "a cost or gain that falls on people outside the transaction"),
            ("value of a statistical life", "the price used for a death in cost-benefit analysis"),
            ("capitalisation", "a cost or gain that shows up in house prices"),
            ("identification", "a design that separates cause from correlation"),
        ],
        points=[
            ("189, 202", "Violent crime by group members costs victims about $29bn a year in full cost, "
                    "$4.5bn in tangible losses."),
            ("195", "Traffic costs other commuters $12–14bn a year now that roads grow ($19.2bn at "
                    "fixed roads)."),
            ("190", "Other renters pay about $34bn more rent. Landlords who are also residents get 96.5% "
                    "of it. The net for others is a small gain of $0.7–3.5bn."),
            ("258", "ADOPTED into the social rows: fear, private security and school discipline add "
                    "$7.9bn (Black comparator: $51.0bn)."),
            ("260", "Beside, not added: PM2.5 from the group's consumption costs others $70bn a year "
                    "($31–122bn). As many average residents would cost them $47bn more."),
            ("261", "Beside, not added: infectious disease and food safety cost others $0.3bn a year. "
                    "Tuberculosis is $0.05bn."),
            ("248, 243, 246", "School quality: state NAEP shows no white loss with the Hispanic share. "
                    "In Germany, immigration explains about 7–14% of the PISA fall."),
            ("97, 102, 96, 101, 93, 98", "Unpriced and not bounded: political effects, city "
                    "productivity losses, native fertility."),
        ],
        members=["o2", "o6", "o8", "o18", "o20", "o38", "o50",
                 57, 78, 79, 81, 89, 91, 93, 96, 97, 98, 101, 102, 142, 155, 180, 183, 189, 190,
                 195, 222, 243, 246, 248, 258, 260, 261, 262],
    ),
    dict(
        id="whopays",
        title="Who pays and who gains",
        size="Moves who loses, not the total",
        why=(
            "The cost does not fall evenly. State and local budgets carry about 85% of it. The costs "
            "outside budgets fall on renters and less-educated workers. Landlords and the top income "
            "tenth gain most often. About one other resident in six comes out ahead."
        ),
        terms=[
            ("distributional incidence", "which households bear a cost, by income or place"),
            ("welfare weights", "how much a dollar counts for rich vs poor; Hendren's revealed weights"),
            ("marginal cost of public funds (λ)", "the full cost of raising $1 of tax: 1.16–1.5"),
        ],
        points=[
            ("226", "17–18% of other residents come out ahead. On the September 24 case, 95–98% in "
                    "California and Texas and 97–98% of US-born adults with high school or less came out behind."),
            ("194", "Financed by tax shares, the top fifth pays 62%. Financed by equal cuts, the "
                    "bottom fifth loses 12.4% of its resources."),
            ("250", "World view: the group gains much by living here. At equal weights the world total "
                    "is positive (central +$364bn). The US plus the group comes out behind only if the "
                    "group's dollar counts less than 0.61 of a payer's."),
            ("139", "Native out-migration from California is real but small: about $2.1bn of state-local "
                    "revenue."),
            ("213", "Race-based preferences cost white natives about $4.0bn a year; $0.6bn goes to "
                    "Mexican-origin beneficiaries."),
        ],
        members=["o5", "o11", "o23", "o39", 138, 139, 194, 213, 226, 250],
    ),
    dict(
        id="work",
        title="Work, wages and production",
        size="+$9–13bn net gain; $66–166bn moved between workers",
        why=(
            "The group's work makes the economy bigger. Almost all of that gain goes to the group as "
            "wages. Other residents get a small net gain, mostly through taxes. Inside that small net, "
            "large sums move between other residents."
        ),
        terms=[
            ("immigration surplus", "the extra income natives get because immigrants work here"),
            ("elasticity of substitution (ε)", "how easily one kind of worker replaces another"),
            ("general equilibrium", "a model where prices, wages and capital all adjust together"),
            ("shift-share instrument", "a design using old settlement patterns to predict new inflows"),
        ],
        points=[
            ("166, 176", "The production term is $8.8–13.3bn. With imperfect substitution (ε = 3) it "
                    "about doubles. The sign never changes."),
            ("181", "Studies that estimate ε for low-skill workers directly give 8.7 and 17.9. That "
                    "points to perfect substitution, the account's default."),
            ("191", "Less-educated natives earn 2.2–7.0% less ($66–166bn a year). More-educated natives "
                    "earn 1–3% more ($71–163bn)."),
            ("132, 198", "Cheaper services and more work by native women: about $22bn to consumers, "
                    "$8.7bn fiscal. Care channels add $4.1bn, already inside."),
            ("201", "City size and schooling mix would add +$13.9bn (proposed, not adopted)."),
        ],
        members=["o17", "o19", "o21", "o29", "o40", "o44",
                 53, 59, 94, 99, 120, 132, 136, 140, 156, 164, 166, 176, 181, 182, 191, 198, 199,
                 200, 201, 203],
    ),
    dict(
        id="generations",
        title="Generations and assimilation",
        size="Decides the future flow",
        why=(
            "The long-run cost depends on the children and grandchildren. The second generation "
            "closes most of the school-completion gap but less of the college gap. Progress stalls "
            "after the second generation. All three generations are net costs today."
        ),
        terms=[
            ("intergenerational transmission", "how much of the parents' gap reaches the children"),
            ("ethnic attrition", "descendants who stop reporting Mexican origin"),
            ("selection", "migrants differ from people who stay home, on schooling and more"),
            ("regression to the mean", "children move toward an average; which average matters"),
        ],
        points=[
            ("224", "On the September 27 case, counted in their own generation: Mexico-born $78–94bn, "
                    "second generation $128–153bn, third-plus $100–156bn a year."),
            ("178", "The second generation closes 76% of the no-high-school gap, 31% of the college gap, "
                    "59% of the employment gap and 66% of the income gap."),
            ("232", "From the second to the third-plus generation about 0.84 of the college gap stays. "
                    "Identity loss explains only about a tenth."),
            ("236", "About half of a first generation's distance from the white mean reaches its "
                    "children, across 78 origins."),
            ("163", "The group's relative income was flat 2008–2016 and has risen since (per-capita "
                    "0.52 → 0.61 of the national figure)."),
            ("88", "US-born Mexican-origin fertility is at or below the white level."),
        ],
        members=["o9", 67, 74, 75, 83, 86, 88, 92, 95, 100, 103, 107, 109, 111, 112, 113, 115, 116,
                 124, 133, 134, 154, 163, 174, 178, 197, 224, 228, 232, 236],
    ),
    dict(
        id="crime",
        title="Crime and custody rates",
        size="Feeds the $29bn victim cost and custody lines",
        why=(
            "Immigrants themselves offend less than natives. The advantage belongs to the first "
            "generation. US-born Mexican-origin men are held in custody at about twice the white "
            "rate. Most of the gap follows parental income."
        ),
        terms=[
            ("rate ratio", "one group's rate divided by another's"),
            ("mixture identity", "an average rate is a weighted mix of its parts' rates"),
            ("clearance rate", "the share of crimes that end in an arrest"),
        ],
        points=[
            ("42, 48, 144", "First generation: lower. In Texas, undocumented felony charges weighted by "
                    "cost are 0.40–0.43 of the US-born rate."),
            ("65", "US-born Mexican-origin men: 1.7–1.9× the white custody rate raw (2023–24), "
                    "2.1–2.3× after fixing prison coding. The 3.5× figure is from 2000."),
            ("82", "About 73% of the Hispanic–white male custody gap is parental income. At equal "
                    "income the ratio is 1.22×."),
            ("202, 218", "Police records (NIBRS, TX and AZ): Hispanic offenders at 2.30× the white "
                    "murder rate. Against all residents the ratios are 0.92–1.18."),
            ("214", "Noncitizen fraud runs at 1.8–2.0× citizens, the same ratio as for all federal "
                    "crime."),
        ],
        members=["o42", "o43", "o48", "o49", "o51",
                 56, 61, 63, 64, 65, 66, 68, 69, 70, 82, 105, 106, 108, 144, 148, 196, 202, 214, 218],
    ),
    dict(
        id="comparators",
        title="Other groups as benchmarks",
        size="Scale checks, not part of the total",
        why=(
            "The same account run on other groups shows whether the result is special to this group. "
            "Indian-origin residents are the most positive group measured. A rough re-key to "
            "non-Hispanic Black residents gives a larger cost per member."
        ),
        terms=[
            ("re-key", "run the same account with another group's shares"),
            ("composition effect", "a gap explained by age, schooling or place mix"),
        ],
        points=[
            ("150", "India-born adults: +$24,163 per adult-year, against +$13,431 for the white "
                    "reference."),
            ("259", "Non-Hispanic Black residents (rough): $549–595bn a year, $13.1–14.2k per member, "
                    "1.5–1.7× the Mexican-origin figure per member."),
            ("168, 171", "Degrees convert unequally by origin. Admission route predicts it; a "
                    "Muslim-majority origin does not."),
            ("72, 73", "In Europe the immigrant crime gap is mostly composition; the descendant gap is not."),
        ],
        members=[71, 72, 73, 150, 151, 152, 153, 167, 168, 171, 177, 179, 259],
    ),
    dict(
        id="status",
        title="Legal status, flows and enforcement",
        size="Counts and routes, small dollar effect",
        why=(
            "These entries count the unauthorized, trace legal routes and test surge-era claims. "
            "Status matters less for the fiscal gap than schooling does."
        ),
        terms=[
            ("residual method", "unauthorized = foreign-born minus legal records"),
            ("adjustment of status", "getting a green card from inside the US"),
        ],
        points=[
            ("157", "Unauthorized stock: 14.6–15.8M for mid-2024 on the usual definition; 8–9.5M on the "
                    "narrow one."),
            ("185, 186", "About half of low-education Mexico-born parents are imputed unauthorized. Their "
                    "US-born children do worse while parents lack status, and the same once they have it."),
            ("187", "Most who legalized after entry without papers used 245(i), a door that closed in 2001."),
            ("242", "The FY2019–24 doubling of Mexican IR-5 parents is processing, not a Mexico surge."),
        ],
        members=["o22", "o24", "o25", "o26", "o27", "o30", "o32", "o33", "o34", "o35",
                 118, 157, 185, 186, 187, 242],
    ),
    dict(
        id="civic",
        title="Civic life and politics",
        size="Unpriced",
        why=(
            "Attitudes on immigration converge to whites by the third generation. Views on "
            "redistribution and in-group warmth do not. We found no way to price the political "
            "effects."
        ),
        terms=[
            ("adjusted gap", "a difference after holding age, schooling and year constant"),
            ("apportionment", "how House seats follow population counts"),
        ],
        points=[
            ("87, 104, 135", "Immigration views converge. Redistribution and Democratic lean do not."),
            ("147", "Counting the group moves 24 of 435 House seats (2020); no presidential outcome flips."),
            ("160", "A county's Mexican-origin share does not move its presidential vote."),
            ("205", "US-born Mexican-origin men served in the military at 0.79 of the white rate "
                    "(0.88 at the same ages)."),
        ],
        members=["o28", "o31", "o36", 87, 104, 110, 114, 117, 135, 147, 160, 170, 205, 233, 234],
    ),
    dict(
        id="claims",
        title="Public claims checked",
        size="Specific posts and papers",
        why="Each entry tests one public claim against primary data.",
        terms=[],
        points=[
            ("212", "\"Legalized fraud\" in California: payments by status are mostly lawful and already "
                    "inside the account; no status fraud found."),
            ("244", "Rochester \"80 of 82 residents on visas\": the roster counts medical schools, not visas."),
            ("245", "DHS credit to interior enforcement: the gradient was as steep before the surge."),
            ("145", "Marginal Revolution 2003–2026: 13 agree, 9 coordinate, 1 hard conflict."),
            ("84", "No \"frivolous spending\" at equal income; the gap is wealth."),
        ],
        members=["o4", 84, 145, 212, 221, 223, 244, 245],
    ),
    dict(
        id="method",
        title="Method rules and withdrawals",
        size="How to read everything above",
        why=(
            "These entries set rules. A clean regression is not a causal result. A runnable "
            "calculation is not a theory test. Many early entries were withdrawn; the page marks them."
        ),
        terms=[
            ("non-significance ≠ zero", "a wide interval does not show no effect"),
            ("equivalence test", "a test that can show an effect is small"),
        ],
        points=[
            ("58, 60", "Controls and passed placebos do not by themselves identify causes. The old "
                       "verified/falsified tally is withdrawn."),
            ("o1–o51", "The April–June layer is mostly superseded. Read an old entry only with its "
                       "successor."),
        ],
        members=["o10", "o14", "o37", 58, 60],
    ),
]
