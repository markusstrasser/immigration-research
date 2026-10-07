"""Evidence map content: parts, sections with claim headings, findings.

For a reader who wants concepts and evidence, not the history of the analysis. The page leads with what the
evidence says and why (the answer, its cause, generations, who pays), and leaves the accounting machinery
(how the number is built, its checks and conventions) for later parts.
- `claim`: the section heading, stated as a claim.
- Finding `text`: one or two sentences. Numbers as a rounded value with the range in brackets.
- How a finding's number was obtained (input, step, known bias) lives in `evidence_class.py`,
  keyed by the finding's first ladder ref.
- `why`: what the finding rests on and what would change it.
Every ladder entry must appear exactly once: in a finding's `refs`, a section's `minor` list,
RETIRED or INTERNAL_ENTRIES. `build.py` refuses to write the page otherwise.
Style: ASD-STE100 structural rules (short sentences, active voice, no semicolons).
Numbers that depend on the main estimate are registry placeholders, `{{q:<id>|<view>}}`; the others are
copied from the cited ladder entries.
"""

OLD_LAYER = [f"o{i}" for i in range(1, 52)]

RETIRED = {
    **{k: "April–June layer" for k in OLD_LAYER},
    52: "replaced by 123, 161", 62: "replaced by 123", 76: "replaced by 123, 172", 78: "replaced by 189",
    93: "replaced by 98", 94: "replaced by 99", 95: "replaced by 100", 96: "replaced by 101", 97: "replaced by 102",
    121: "replaced by 123, 172", 122: "replaced by 123, 172", 130: "replaced by 161, 172", 137: "replaced by 207",
    138: "replaced by 194", 155: "rating withdrawn", 164: "replaced by 198", 231: "replaced by 238",
    193: "earlier version", 219: "earlier version", 229: "earlier version", 204: "earlier version",
    239: "earlier main estimate, replaced by 275 and 281", 275: "earlier main estimate, replaced by 281",
    281: "earlier main estimate, replaced by 295",
}

# How the work was done, not what it found: never shown to readers (operator 2026-09-29: the reader
# should not know about AI reviewers). Not counted as superseded either.
INTERNAL_ENTRIES = {
    271: "reviewer calibration",
}

# Most insightful first (operator 2026-10-06): the answer and its cause, then generations, who pays and the
# costs outside the budget. How the number is built comes after them; build.py puts the ledger, the
# alternatives and the assumption table at the start of the "build" part.
PARTS = [
    ("answer", "The answer and what drives it"),
    ("generations", "Across generations"),
    ("whopays", "Who pays and who gains"),
    ("beyond", "Beyond the public budget"),
    ("build", "How the number is built"),
    ("other", "Other evidence"),
]

GROUPS = [
    dict(
        id="account", part="answer",
        claim="Other US residents pay about {{q:case.main|mid}} a year for the group's presence",
        range="{{q:case.main|mid_range}}",
        why=("The account asks one question. In 2024, how much better off would all other US residents be "
             "without the Mexican-origin population? It adds each member's own taxes and benefits, corrected "
             "with records. It then charges a share of every public service that grows with the population."),
        terms=[("counterfactual", "the world we compare with. Here it is the same US without the group."),
               ("specification", "one full set of choices. The range covers 64 of them."),
               ("standard error", "sampling noise. It is about {{q:noise.se|range_unit}} here."),
               ("lineage", "the immigrants, their children and later descendants, whether or not they still "
                           "report Mexican origin")],
        findings=[
            dict(refs=[295],
                 text="Other residents would be about {{q:case.main|mid}} a year better off "
                      "({{q:case.main|range}}). That is about {{q:case.per_member|mid_range}} per member.",
                 why="The count is {{q:headcount.lineage|value}} people. Of them, "
                     "{{q:headcount.identified|value}} report Mexican birth, a Mexico-born parent or Mexican "
                     "origin. The other {{q:headcount.added|value}} are later descendants who no longer report "
                     "Mexican origin. Each person counts whole. Counted by share of Mexican-immigrant ancestry, "
                     "the total would be about {{q:case.ancestry_share|mid_range}}."),
            dict(refs=[184],
                 text="Sampling noise is about ±{{q:noise.sampling_95|value}} (95%).",
                 why="The assumptions move the number more than the data noise does. The assumption table, in "
                     "the part on how the number is built, ranks them."),
            dict(refs=[54, 55],
                 text="CBO's $897bn lower federal deficit over 2024–2034 answers a different question.",
                 why="CBO counts the federal budget only, new arrivals of all origins, and projected growth "
                     "effects. Two results can conflict only when population, period and outcome match."),
        ],
        minor=[],
    ),
    dict(
        id="why", part="answer",
        claim="The cost comes from lower taxes, not from heavier use of services",
        range="lower taxes make {{q:decomp.taxes_share|range_unit}} of the excess over average residents",
        why=("Compare the group with as many average residents under the same rules. Almost all of the "
             "group's extra cost comes from lower taxes at the same ages. At given ages it uses public services "
             "about as much as other residents do."),
        terms=[("average resident", "national taxes and spending divided by the whole population"),
               ("household transfers", "cash, food, housing and medical benefits paid to households"),
               ("cash vs accrual", "count a pension when it is paid, or count the promise when it is earned")],
        findings=[
            dict(refs=[269],
                 text="Any {{q:headcount.lineage|value}} average residents would cost others about "
                      "{{q:decomp.average_residents|mid_range}} under the same rules. The group's excess over "
                      "them is about {{q:decomp.excess|mid_range}}. Lower taxes at the same ages make up "
                      "{{q:decomp.taxes_share|range_unit}} of it.",
                 why="Governments spend more than they tax, so in this account any residents cost others "
                     "something. The group's age mix adds {{q:decomp.age_mix|range_unit}}. Its use of services "
                     "at given ages adds {{q:decomp.use|pair}} at the low and high ends."),
            dict(refs=[257, 286, 146],
                 text="With pensions counted when earned, the group's direct taxes about equal the benefits "
                      "it draws: {{q:tally.accrual|pair}} at the low and high ends. Schools and other public "
                      "services make the cost.",
                 why="On cash, the members who report Mexican origin pay about $65bn more payroll tax than they "
                     "draw (63–68), because they are young. Under current law and the Trustees' 2026 projections, "
                     "that tax buys future benefits worth about {{q:pension.accrual_ratio|value}} per tax dollar. "
                     "Current law keeps the retirement and disability funds apart, and each fund pays only what it "
                     "holds. Counting the promise when earned, as the main estimate does, adds about "
                     "{{q:pension.accrual|mid_range}} to the total."),
            dict(refs=[268],
                 text="About {{q:household.net_contributor_share|mid}} of members "
                      "({{q:household.net_contributor_share|range}}) live in households that pay more than they "
                      "cost. The costliest tenth of households carries {{q:household.top10_cost_share|range_unit}} "
                      "of the net cost.",
                 why="The share rises from about {{q:household.share_head_below_hs|mid}} when the head did not "
                     "finish high school to about {{q:household.share_head_ba_plus|mid}} with a degree. Households "
                     "with three or more children almost never pay their way, because a one-year account charges "
                     "each household for its children's schools. Counting only the services that a household uses "
                     "itself, the share is about {{q:household.share_convention_b|mid}}."),
        ],
        minor=[282],
    ),
    dict(
        id="selection", part="answer",
        claim="Who migrates matters most: under the same rules, Indian-origin residents benefit others",
        range="{{q:indian.gap_to_union|range_unit}} per member between the two groups",
        why=("The same account, applied to other groups, shows what is special to this one. Schooling at "
             "arrival sets most of the result, and the children carry it on."),
        terms=[("selection", "how migrants differ from the people who stay home"),
               ("re-key", "the same account with another group's shares"),
               ("replacement", "the group against an equal number of people from another group")],
        findings=[
            dict(refs=[276, 277],
                 text="Indian-origin residents benefit others by about {{q:indian.per_member|mid_range}} per "
                      "member a year, social costs included. The Mexican-origin group costs others about "
                      "{{q:union.per_member_social|mid_range}} per member on the same terms.",
                 why="At the ages of third-generation whites the Indian-origin benefit is still about "
                     "{{q:indian.white_ages|mid_range}}. Each arrival cohort since 1995 sits at the 75th–78th "
                     "percentile of US white schooling, above the cohorts of 1975–94. Telugu, Tamil, Marathi, "
                     "Kannada and Bengali speakers sit near the 80th percentile, Punjabi speakers at the 47th."),
            dict(refs=[74, 75, 86, 92, 133, 174, 197, 228],
                 text="Mexican migrants come from the middle of Mexico's schooling range. Their children move "
                      "toward the average of their origin group, not toward the national average.",
                 why="Across 29 origins, parents' schooling relative to their home country predicts their "
                     "children's degrees (R² 0.91)."),
            dict(refs=[150, 168, 171],
                 text="India-born adults have a balance of about +$24k a year each. For whites it is +$13k.",
                 why="How well degrees pay depends on the admission route more than on the origin country."),
            dict(refs=[263],
                 text="Against as many third-generation whites, the group costs others about "
                      "{{q:whites.gap_a1|mid_range}} a year more. Against local whites, state by state, the gap "
                      "is about {{q:whites.gap_local|mid_range}}.",
                 why="On raw cash the gap is only {{q:whites.gap_cash|mid_range}}, because whites are older and "
                     "draw pensions now. Counting pensions when earned removes that effect. Both sides have the "
                     "same number of people. As many third-generation whites cost others "
                     "{{q:whites.own_per_member|range_unit}} each, about break even, so the gap is close to the "
                     "group's whole cost. The gap comes from taxes and schools."),
            dict(refs=[259],
                 text="Under the same rules, non-Hispanic Black residents cost others about "
                      "{{q:black.per_member|mid_range}} per member. That is {{q:black.ratio_engine|range}} times the "
                      "main estimate per lineage member, {{q:case.per_member|mid}}.",
                 why="A rough calculation with group shares, not a full model run. Neither figure counts the "
                     "costs outside public budgets that the Indian comparison adds."),
        ],
        minor=[151, 152, 153, 167, 177, 179],
    ),
    dict(
        id="status", part="answer",
        claim="Legal status explains little of the cost",
        range="about 15M unauthorized",
        why="Schooling matters more for the fiscal gap than legal status does.",
        terms=[("residual method", "unauthorized = foreign-born minus people in legal records")],
        findings=[
            dict(refs=[85],
                 text="Imputed unauthorized and legal Mexico-born adults have similar fiscal gaps, about $7,800 "
                      "and $8,200 a year per adult against later-generation whites.",
                 why="Status is imputed, not observed. With benefits that status rules out set to zero and taxes "
                     "cut to the on-books share, the gaps are $9,720 and $8,234."),
            dict(refs=[157],
                 text="About 15.2M people were unauthorized in mid-2024 (14.6–15.8).",
                 why="This uses the definition that every publisher uses. The narrow definition gives 8–9.5M."),
            dict(refs=[185, 186, 187],
                 text="About half of Mexico-born parents with little schooling are unauthorized, and few can "
                      "get legal status.",
                 why="Their US-born children do worse while the parents lack status, and the same after they "
                     "get it."),
            dict(refs=[242],
                 text="The recent doubling of sponsored Mexican parents comes from processing, not from a surge.",
                 why="Other countries rose by the same proportion."),
        ],
        minor=[118, 283, 291],
    ),
    dict(
        id="generations", part="generations",
        claim="Each generation costs others, and the college gap stops closing after the second",
        range="three generations, each a net cost",
        why=("All three generations cost others today. The second generation closes most of the gap in "
             "finishing school but little of the college gap. The third generation keeps most of what is left."),
        terms=[("transmission", "how much of the parents' gap reaches the children"),
               ("ethnic attrition", "descendants who stop reporting Mexican origin")],
        findings=[
            dict(refs=[224],
                 text="In their own generation, the Mexico-born cost others about "
                      "{{q:generation.g1_own|mid_range}} a year, the second generation "
                      "{{q:generation.g2_own|mid_range}} and the third-plus {{q:generation.g3_own|mid_range}}.",
                 why="Counted with their parents, the Mexico-born carry the most, about "
                     "{{q:generation.g1_parents|mid_range}}. The third-plus includes the descendants who no "
                     "longer report Mexican origin."),
            dict(refs=[178, 232, 236, 293],
                 text="The second generation closes 76% of the gap in finishing school but 31% of the college "
                      "gap. The third generation keeps about 86% of the college gap that is left.",
                 why="CPS 1994–2026 at equal age, with the descendants who stop reporting Mexican origin put "
                     "back."),
            dict(refs=[280, 158, 292],
                 text="About {{q:identity.loss_g3|value}} of third-generation descendants do not report Mexican "
                      "origin. They close about {{q:identity.c3|value}} of the college gap to whites. They are too "
                      "few to explain the stall: counting them lowers the share of the gap that stays by about "
                      "{{q:identity.stall_share|value}}.",
                 why="Parents and children linked in the CPS, 1994–2026. The main estimate counts these "
                     "descendants, {{q:headcount.added|value}} people, at their measured ages. Those lost a generation "
                     "later are younger than identified third-generation members, and children cost more."),
            dict(refs=[272],
                 text="Second-generation Hispanic sons earn 14% less than white men at 25–27 and 24% less by "
                      "35–40. Daughters' gap, 13% and 18%, does not widen measurably.",
                 why="Most of the sons' widening is pay, and it follows schooling. At equal schooling the "
                     "daughters' gap is about zero."),
            dict(refs=[163, 134],
                 text="The group's income relative to the nation was flat from 2008 to 2016 and rose after.",
                 why="Income per person went from 0.52 to 0.61 of the national figure. Recent arrivals have the "
                     "smallest gap."),
            dict(refs=[83, 115, 105, 106, 108, 113, 124],
                 text="Test-score and custody gaps narrow to the third generation. After that the samples are "
                      "too small.",
                 why="NLSY97 and two local panels."),
            dict(refs=[67, 88, 100, 116],
                 text="US-born fertility is at or below the white level. The health advantage of immigrants "
                      "fades after the first generation.",
                 why="Disability rises from the first to the second generation."),
            dict(refs=[154],
                 text="With measured assimilation rates, a leading pro-migration model loses its Mexico result.",
                 why="Clemens and Pritchett assume faster convergence than the data show."),
        ],
        minor=[103, 107, 109, 111, 112, 287],
    ),
    dict(
        id="whopays", part="whopays",
        claim="State and local taxpayers pay most of the cost, and about one other resident in six gains",
        range="{{q:incidence.state_local_share|range_unit}} state and local",
        why=("State and local budgets carry most of the cost, through schools, police and local services. "
             "Renters and workers with less schooling lose most."),
        terms=[("incidence", "which households finally bear a cost"),
               ("welfare weights", "how much a dollar counts for a rich person vs a poor person")],
        findings=[
            dict(refs=[226],
                 text="About one other resident in six comes out ahead: {{q:winners.share_ahead_a|value}} when "
                      "taxes close the gap and {{q:winners.share_ahead_b|value}} under equal cuts. Most of them "
                      "are landlords or in the top tenth of income.",
                 why="The analysis follows each person through taxes, wages, rents and crime. Nearly everyone in "
                     "California and Texas comes out behind, and so do renters and US-born adults with high "
                     "school or less."),
            dict(refs=[194],
                 text="If taxes close the gap, the top fifth pays {{q:quintile.top_fifth_tax_share|value}}. If "
                      "equal cuts close it, the bottom fifth loses {{q:quintile.bottom_fifth_cuts|value}} of its "
                      "resources.",
                 why="Who pays depends on how budgets close the gap."),
            dict(refs=[250],
                 text="Counting the group's own gain, the world gains about {{q:world.total_equal|value}} in the "
                      "year measured, with every person weighted equally.",
                 why="The group earns far more here than it would in Mexico. Other US residents lose at any "
                     "weight. Counting the group as US residents, the US comes out behind when the group's welfare "
                     "counts for less than {{q:world.breakeven_us|value}} of other residents'. Over "
                     "generations the sign turns on how fast descendants catch up. At the measured pace, Clemens "
                     "and Pritchett's long-run model favours less migration in 14 of its 21 versions."),
            dict(refs=[139, 213],
                 text="Natives who leave California take about $2.1bn of revenue. Race preferences cost white "
                      "natives about $4bn.",
                 why="High earners leave with the top tax rate, not with the Hispanic share."),
        ],
        minor=[],
    ),
    dict(
        id="work", part="whopays",
        claim="The group's work adds about {{q:production.gain|mid}} a year for others and moves about $116bn "
              "between workers",
        range="{{q:production.gain|mid_range}}",
        why="The group's work makes the economy larger. Most of that gain is its own wages.",
        terms=[("immigration surplus", "the extra income that natives get because immigrants work here"),
               ("ε (substitution)", "how easily one kind of worker replaces another")],
        findings=[
            dict(refs=[166, 176, 181],
                 text="Other residents gain about {{q:production.gain|mid_range}} a year from the group's work, "
                      "through profits and taxes.",
                 why="If natives and immigrants were poor substitutes (ε = 3), the gain would double. Direct "
                     "estimates of ε (8.7–17.9) say they are close substitutes."),
            dict(refs=[191, 199],
                 text="Natives with less schooling earn 2.2–7.0% less, about $116bn (66–166). Natives with more "
                      "schooling earn more.",
                 why="A model with two skill groups. The two transfers nearly cancel."),
            dict(refs=[132, 198, 200, 203],
                 text="Cheaper services, more work by native women and home care add about $4bn a year.",
                 why="Price effects from published studies, at face value."),
            dict(refs=[201, 156],
                 text="Larger cities raise earnings and lower schooling lowers them. The two nearly cancel "
                      "(about +$14bn).",
                 why="One regression across commuting zones. Older studies of the college share would make it a "
                     "large cost. Studies of average schooling find nothing."),
            dict(refs=[53, 59, 99, 120, 136, 140, 182],
                 text="The wage and automation designs tested here cannot find a native wage effect.",
                 why="The usual instruments lose their power after {{q:instrument.power_lost_year|value}}."),
        ],
        minor=[],
    ),
    dict(
        id="social", part="beyond",
        claim="Costs outside the public budget add about {{q:social.items|mid}} a year",
        range="about {{q:social.items|mid_range}}",
        why=("Some costs never pass through a budget: crime victims, pollution, crashes, traffic and fear. "
             "The account prices them beside its total, net of gains from a larger economy. With them the total is "
             "about {{q:pairing.total|mid_range}}. Its low end also prices offending at the Hispanic average, "
             "{{q:pairing.footing_reduction|at_low_end}} less."),
        terms=[("externality", "a cost that falls on people outside the transaction"),
               ("value of a statistical life", "the price that cost-benefit analysis uses for a death"),
               ("normalized", "the same item for as many average residents, taken away")],
        findings=[
            dict(refs=[260],
                 text="Fine-particle pollution from the group's consumption causes about "
                      "{{q:pm25.deaths_priced|value}} deaths among others a year. The cost is about "
                      "{{q:pm25.cost|mid}} ({{q:pm25.span_priced|range}}).",
                 why="Per person the group causes 0.65 of an average resident's pollution because it consumes "
                     "less. Against as many average residents, the group is about "
                     "{{q:pm25.normalized_priced|value}} better."),
            dict(refs=[264, 266],
                 text="The group's traffic costs other residents about {{q:crash.cost|mid}} a year in road crashes "
                      "({{q:crash.span_priced|range}}).",
                 why="One more car barely changes other drivers' crash risk per mile. So most crashes that others "
                     "have with group drivers would happen anyway, among the remaining drivers. Counting every "
                     "crash that group drivers cause gives about {{q:crash.fault_based_priced|mid_range}}. "
                     "California records show Hispanic drivers are not at fault more often in injury crashes "
                     "(odds 0.98)."),
            dict(refs=[189],
                 text="Violent crime by group members costs victims outside the group about "
                      "{{q:victims.harm|mid_range}} a year.",
                 why="The full cost counts a death at a statistical value, plus pain. Tangible losses alone are "
                     "$4.5bn. Police records confirm the offender shares."),
            dict(refs=[195],
                 text="Traffic costs other commuters about $13bn a year (12–14).",
                 why="Speed falls 0.12% per 1% more people when road space stays fixed. Roads that grow with "
                     "population take up part of it."),
            dict(refs=[258],
                 text="Fear, private security and school discipline cost about $8bn a year.",
                 why="The same method gives $51bn for non-Hispanic Black residents."),
            dict(refs=[190, 79, 180, 183, 57],
                 text="In the long run rents rise {{q:housing.rent_elasticity_long_run|range}}% per 1% more people. "
                      "Other renters pay about $34bn more, and landlords receive it.",
                 why="Most landlords are other residents, so the net for others is a small gain of about $2bn "
                     "(0.7–3.5). The loss falls on renters."),
            dict(refs=[265],
                 text="Three benefits to others count against these costs: volunteering about $6bn, consumer "
                      "scale about $2bn and trade ties with Mexico about $7bn.",
                 why="The account already carries the large benefits: taxes, production, care and housing. "
                     "Defense and old interest are never charged to the group. That is an implicit credit of "
                     "about $271bn a year."),
            dict(refs=[261],
                 text="Infectious disease and food safety cost others about $0.3bn a year.",
                 why="Most TB among the foreign-born comes from old infection abroad. About 56 cases a year "
                     "among others trace to the group."),
            dict(refs=[248, 81, 91, 243, 246, 222],
                 text="White pupils did not lose ground in states where the Hispanic share rose.",
                 why="State NAEP scores, 2003–2019. The share of English learners gives a small negative that "
                     "fades. In Germany, immigration explains a small part of the fall in scores."),
            dict(refs=[262, 89, 142],
                 text="Friendships across income are fewer where the Hispanic share is higher. The main cause is "
                      "that people live apart.",
                 why="Facebook friendship data by county and ZIP code, one point in time. The payoff to such "
                     "friendships does not grow with county size."),
            dict(refs=[98, 101, 102],
                 text="Three effects have no price and no bound: native births, city productivity and politics.",
                 why="The designs tried here cannot separate these effects from their causes."),
        ],
        minor=[274],
    ),
    dict(
        id="crime", part="beyond",
        claim="Immigrants offend less, and their US-born sons are held at about twice the white rate",
        range="feeds the {{q:victims.harm|mid}} victim cost",
        why="The immigrant advantage belongs to the first generation. Parental income explains most of the later gap.",
        terms=[("rate ratio", "one group's rate divided by another group's rate"),
               ("clearance rate", "the share of crimes that end in an arrest")],
        findings=[
            dict(refs=[144, 61],
                 text="Undocumented Texans are charged with felonies, weighted by cost, at 0.40–0.43 of the "
                      "US-born rate.",
                 why="Texas fingerprint records give legal status. The comparison group is all US-born Texans."),
            dict(refs=[65, 66, 68, 70, 196],
                 text="US-born Mexican-origin men are held at 1.7–1.9 times the white rate, or 2.1–2.3 times "
                      "after a fix for prison coding. The often-quoted 3.5 times is from 2000.",
                 why="Census counts of people in institutions, 2010–2024. The ratio fell as both rates fell."),
            dict(refs=[82],
                 text="Parental income explains about 73% of the Hispanic–white gap in male custody.",
                 why="At equal parental income the ratio is 1.22."),
            dict(refs=[202, 218, 148],
                 text="In police records, Hispanic offenders commit murder at 2.30 times the white rate and "
                      "0.92–1.18 times the rate of all residents.",
                 why="Texas and Arizona incident records. Known recording errors do not change the ratios."),
            dict(refs=[71, 72, 73],
                 text="In Europe, composition explains most of the immigrant crime gap but not the gap of "
                      "their children.",
                 why="Population registers link parents and children. The US has no register."),
            dict(refs=[143],
                 text="One cleared homicide costs the treasury $1.5–1.8M, mostly for prison. Its social cost is "
                      "$13.1M.",
                 why="Homicide records 2019–2023 with the ethnicity of both sides known."),
            dict(refs=[214],
                 text="Noncitizens commit fraud at the same ratio as other federal crime, 1.8–2.0 times citizens.",
                 why="Federal sentencing records per adult."),
            dict(refs=[56, 63, 64, 69],
                 text="Nativity, race and generation are separate measures. Recording failures need bands.",
                 why="A comparison with whites only changes the question. It does not correct a bias."),
        ],
        minor=[],
    ),
    dict(
        id="services", part="build",
        claim="Schools are the largest cost, and most public spending grows with the population",
        range="schools at full cost per pupil",
        why=("The account charges each public service by how its budget grows with the number of residents. With every "
             "service held fixed, the group's taxes and benefits alone come close to balance. So the service "
             "responses decide most of the size."),
        terms=[("response (elasticity)", "the % rise in a budget for each 1% rise in users"),
               ("average vs marginal cost", "cost per user now vs the cost of one more user")],
        findings=[
            dict(refs=[230, 215, 252],
                 text="School spending rises about 1% per 1% more pupils. So each pupil costs the full average. "
                      "Schools are the largest line.",
                 why="Across districts and states the slope is 0.97–1.00. Inside one district over a few years "
                     "it is 0.84. In the 2022–24 surge, money followed new pupils about half, and late. Without the "
                     "return on school capital, the short-run response would lower the total by about "
                     "{{q:schools.first_year_effect|mid_range}}."),
            dict(refs=[237],
                 text="Road spending rises 0.73% and park spending 0.95% per 1% more residents.",
                 why="Slopes across states. Budget scoring sets them to zero for the first year. Over a long "
                     "stay the long-run slope applies."),
            dict(refs=[211, 165, 227],
                 text="General administration grows about {{q:gg.growth_elasticity|mid}}% per 1% more residents "
                      "({{q:gg.growth_elasticity|range}}).",
                 why="From the size of administration spending across states. Designs inside states are too "
                     "noisy to tell it from 0 or 1."),
            dict(refs=[141, 149],
                 text="Natives did not leave public schools as the Hispanic share rose. Local budgets did not "
                      "shift from schools to police.",
                 why="District and county panels, 2007–2023."),
            dict(refs=[80],
                 text="Fiscal studies charge shared services at average cost. Where prisons are full, building "
                      "costs add 18–27% to a prisoner-year.",
                 why="Prisons are full in 8 states and not in 22."),
        ],
        minor=[],
    ),
    dict(
        id="conventions", part="build",
        claim="Accounting rules set some real costs to zero, and the main estimate prices them",
        range="return on public capital, enterprises included: {{q:capital_return.total|mid_range}}",
        why="Budget and national-accounts rules set some costs to zero without measuring them. The account "
            "prices each one with a band.",
        terms=[("opportunity cost of capital", "what public capital could earn in another use")],
        findings=[
            dict(refs=[238],
                 text="Public capital (schools, roads, buildings) could earn 2–3% a year in another use. With "
                      "government enterprises' capital, this adds about {{q:capital_return.total|mid_range}}.",
                 why="National accounts charge only wear. The return is a resource cost, not a payment. It never "
                     "enters debt or the deficit. The assumption table shows the total at a private 7% return."),
            dict(refs=[253],
                 text="Property taxes follow people, like the capital they pay for. Taxes on owned and rented "
                      "homes respond at about 0.72–0.77.",
                 why="The house leaves with the household and land prices fall. Defense stays at zero. A bound "
                     "on defense by share of GDP would add about {{q:defense.bound|mid_range}}."),
            dict(refs=[161, 169],
                 text="On cash accounts a young age mix hides cost. Against third-generation whites, the gap per "
                      "person is {{q:gap_vs_white.per_person_common_age|value}} at a common age mix and "
                      "{{q:gap_vs_white.per_person_own_ages|value}} at the group's own ages.",
                 why="Children cost now and pay later. Old people draw pensions. Counting pensions when earned, "
                     "as the main estimate does, removes most of this effect."),
            dict(refs=[288],
                 text="Public pensions already count when earned. The main estimate counts public workers' retiree "
                      "health the same way, which adds about {{q:retiree_health.change|range_unit}}.",
                 why="National accounts book public pensions at the cost of the promises earned each year, but "
                     "retiree health as paid. Care bought for military retirees pays for past service, so it does "
                     "not grow with the group. The sign rests on one ratio: state plans' cost of promises earned in "
                     "a year is {{q:retiree_health.cost_ratio|value}} times what they pay."),
        ],
        minor=[],
    ),
    dict(
        id="data", part="build",
        claim="Checks against records move taxes and spending by about $50bn each (44–57), and the two almost cancel",
        range="net about $11bn",
        why=("Survey answers carry known errors. The analysis checks each tax and benefit share against "
             "records that the account did not use."),
        terms=[("allocation key", "the share of a national total charged to the group"),
               ("imputation", "Census fills a missing answer with a similar person's answer"),
               ("held-out test", "a check against data that the model never saw")],
        findings=[
            dict(refs=[208],
                 text="Census fill-ins for missing income give the group too much income. The correction raises "
                      "the cost by about {{q:fill_in.effect|mid_range}}.",
                 why="At equal age, sex and schooling, filled-in wages keep only 9% of the group's wage gap. "
                     "Eight versions of the correction all point the same way."),
            dict(refs=[209],
                 text="The CPS counts the Mexico-born 9–13% above the ACS. About 11.1M is the right level.",
                 why="The excess appears in every monthly file since 2024."),
            dict(refs=[206, 173, 175, 210],
                 text="Ethnicity adds no public medical cost in total. Medicaid long-term care was over-charged "
                      "by $11.1bn.",
                 why="Nine pooled MEPS years move cost from adults to children, not the total. CMS records put "
                     "the group at 7.4% of long-term-care dollars, not 12.25%."),
            dict(refs=[217, 216, 249, 289],
                 text="Fear does not cause people to hide benefits. The income-tax share is slightly too flat at "
                      "the top, so the main estimate uses IRS shares.",
                 why="Administrative totals match the survey where the group lives. IRS data for a year that "
                     "the account never used confirm the direction."),
            dict(refs=[254, 77, 220],
                 text="The account takes off-books pay out of taxes: about $65bn of the imputed unauthorized's "
                      "$137bn in survey wages.",
                 why="Survey wages include work paid off the books. The account scales payroll and income tax for the "
                     "imputed unauthorized to an on-books share, 0.53 for the Mexico-born."),
            dict(refs=[255, 256, 188, 192],
                 text="Two tests fixed before looking pass. The frame predicts where the group's births and "
                      "hospital charity care fall.",
                 why="Birth records put 14.36% of US births with Mexican-origin mothers. The frame says 14.43%. "
                     "Courts, police and prisons charged by use add $5.9bn."),
            dict(refs=[225, 90],
                 text="The account charges consumption taxes on what households spend, not on their income.",
                 why="Saving and money sent home lower spending. Money sent home lowers sales tax by about "
                     "{{q:remittance.sales_tax_effect|mid}}, or {{q:remittance.sales_tax_effect|min}} at surveyed "
                     "amounts."),
            dict(refs=[267],
                 text="Prices where the group lives raise its service costs by about $8.6bn and its sales and "
                      "vehicle taxes by about $6.4bn. The main estimate charges the net, about $2.2bn.",
                 why="The group lives where services cost more (California) and where sales taxes are high "
                     "(Texas and Arizona)."),
            dict(refs=[273],
                 text="The main estimate charges road costs by miles driven, net of the fuel taxes that move with "
                      "it. That adds about $2–4bn.",
                 why="The group has 8% of household income but drives 10% of the miles. Freight costs "
                     "follow what people buy."),
            dict(refs=[294],
                 text="The main estimate charges public colleges and Pell grants by the group's measured use, and "
                      "counts fees for the people who pay them. With two smaller keys, the college, Pell and fee "
                      "changes lower the total by {{q:fees.change|range_unit}}.",
                 why="IPEDS records give the group {{q:fees.use_share|value}} of public colleges' cost, against "
                     "{{q:fees.item_p_share|value}} on a key of state capital spending per head. At the measured "
                     "share, colleges cost {{q:fees.college_key|mid}} less. The group receives "
                     "{{q:fees.pell_share|value}} of Pell grants, which adds {{q:fees.pell|range_unit}}. Tuition "
                     "and hospital charges add {{q:fees.charges|mid}}. BEA's school share of education spending and "
                     "the capital keys make up the rest."),
            dict(refs=[127, 129],
                 text="A second survey gives the same earnings and income-tax gaps within 4%.",
                 why="ACS against CPS, with one tax calculator on both."),
        ],
        minor=[284, 285],
    ),
    dict(
        id="time", part="build",
        claim="Only 2024 is measured, and past years and old debt are separate numbers",
        range="about {{q:backcast.10y|mid}} over ten years, {{q:debt.interest|mid}} interest",
        why=("Earlier years come from a model. Lifetimes use a separate ledger with a reference group. None "
             "of them adds to the annual number."),
        terms=[("back-cast", "a model of past years from today's position and past national data"),
               ("stock vs flow", "debt is an amount. A yearly gap is an amount per year."),
               ("discount rate", "the rate that converts future dollars to today. It is 3% here.")],
        findings=[
            dict(refs=[162, 251],
                 text="Carried back on each year's national data, the cost is about {{q:backcast.10y|mid}} over "
                      "2015–2024 ({{q:backcast.10y|range}}), without interest.",
                 why="Receipts, programmes, prices, population and the group's income change each year. "
                     "Pandemic payments reached the group at about the same rate per person as others."),
            dict(refs=[207],
                 text="If the federal part was borrowed, it left about {{q:debt.stock|mid_range}} of debt. The "
                      "interest on it in 2024 is about {{q:debt.interest|mid_range}}.",
                 why="This is a legacy cost. Removing the group today does not remove old debt, so the number "
                     "stays beside the annual total. State and local budgets must balance and do not borrow "
                     "for it."),
            dict(refs=[123, 125, 126, 128, 172, 119],
                 text="Against third-generation whites of the same ages, the gap is about "
                      "{{q:gap_vs_white.age_matched_partial|value}} a year, and "
                      "{{q:gap_vs_white.age_matched_complete|value}} with every item of the ledger priced. Matching "
                      "by state or metro makes it larger.",
                 why="A gap against a reference group is a different measure from the cost of removal. On "
                     "taxes and benefits alone the group pays more than it gets. The gap is still negative."),
            dict(refs=[131, 159, 241],
                 text="Over all descendants, a Mexican founder's family line runs $1.29M behind a white family "
                      "line ($513k at 3%).",
                 why="Descendants carry 57% of it. This is a gap against whites from a separate ledger. Do not "
                     "scale it onto the annual number."),
            dict(refs=[240, 247, 235],
                 text="Arrivals at 50 or older cost others about {{q:late_arrivals.cost|mid_range}} a year. A "
                      "parent sponsored by a US citizen and entering at 55–65 costs "
                      "{{q:ir5.lifetime_cost_55_65|range_unit}} over the rest of life, at 3%.",
                 why="Per person, late arrivals cost less than seniors who arrived young. Their lower Social "
                     "Security outweighs their lower taxes."),
        ],
        minor=[278, 279, 290],
    ),
    dict(
        id="method", part="build",
        claim="Of the budget assumptions, only the horizon moves the size by more than a quarter",
        range="first-year budget responses: {{q:case.first_year|range_unit}}",
        why=("The analysis swapped each premise for its best-supported alternative, one at a time. The total stays a "
             "cost under every swap. A calculation that runs is not a test of a theory. Controls and "
             "stress tests each catch some errors and miss others."),
        terms=[("non-significance ≠ zero", "a wide interval does not show that there is no effect")],
        findings=[
            dict(refs=[270],
                 text="With first-year budget responses the total falls by about "
                      "{{q:breaks.first_year_pct|value}}. Counting descendants by share of ancestry, at the lowest "
                      "share, lowers it by about {{q:breaks.ancestry_low_pct|value}}. No other single swap moves "
                      "the total by a quarter.",
                 why="The group's taxes cover its benefits at the low end of the range, but not at the high "
                     "end. The observations most worth making next are how "
                     "budgets respond when people leave, and how much of the Mexico-born's pay is on the books."),
            dict(refs=[58, 60], text="Controls and placebo tests that pass do not by themselves show a cause.", why=""),
        ],
        minor=[],
    ),
    dict(
        id="civic", part="other",
        claim="Views on immigration converge by the third generation, and views on redistribution do not",
        range="not priced",
        why="These gaps have no dollar value in the account.",
        terms=[("adjusted gap", "a difference at equal age, schooling and year")],
        findings=[
            dict(refs=[87, 104, 110, 117, 135],
                 text="Trust stays 10–12 points lower. Views on redistribution and party do not converge.",
                 why="GSS and ANES by generation, at equal age and schooling."),
            dict(refs=[147, 160],
                 text="Counting the group moves 24 of 435 House seats. A county's share does not change its vote.",
                 why="Concentration moves seats, not size."),
            dict(refs=[233, 205, 170, 234],
                 text="Turnout is 9–13 points lower at equal status. Military service is 0.79 of the white rate.",
                 why="Ties to Mexico fade by the third generation."),
        ],
        minor=[114],
    ),
    dict(
        id="claims", part="other",
        claim="Five public claims checked against the records",
        range="posts and papers",
        why="Each item tests one public claim against primary data.",
        terms=[],
        findings=[
            dict(refs=[212], text="\"Legalized fraud\" in California: payments based on status are lawful and already in the account.", why=""),
            dict(refs=[244], text="Rochester \"80 of 82 residents on visas\": the list counts medical schools, not visas.", why=""),
            dict(refs=[245], text="A DHS post that credits enforcement: the pattern was as steep before the enforcement.", why=""),
            dict(refs=[145], text="Marginal Revolution 2003–2026: mostly agrees with these facts.", why=""),
            dict(refs=[84, 221, 223],
                 text="At equal income the group spends no more. Few Californians leave because of crime. Legal "
                      "street vending did not hurt restaurants.", why=""),
        ],
        minor=[],
    ),
]
