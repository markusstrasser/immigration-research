"""How each finding's number was obtained, on two separate axes, plus any known systematic bias.

Input (where the numbers come from):
    count    administrative records, registers or full counts (tax, benefit, police, birth, school
             finance records; the decennial census head count)
    sample   a sample survey (ACS, CPS, MEPS, NCVS, NAEP): sampling error plus answers people give
    study    an estimate taken from another study or population
    platform data collected by a private platform (Facebook friendships)
Step (what the analysis does with them):
    tabulated     read directly from the data
    arithmetic    accounting on measured parts
    fitted        a slope or relation estimated in the same data
    extrapolated  carried beyond the data: other years, other places, other populations
    model         a structural model with assumed parameters
    rule          an accounting convention, shown with a band
Bias: only a known systematic bias, with its direction. Random error in the outcome shrinks at
these sample sizes. Random error in a group label does not vanish: it pulls group gaps toward zero.

Keyed by each finding's first ladder entry. `evidence.py` refuses a finding without an entry here.
"""

CLASS = {
    # the annual account
    239: ("sample", "arithmetic", "Survey income for the group was too high. The account corrects it with records."),
    184: ("sample", "tabulated", None),
    269: ("sample", "arithmetic", None),
    161: ("sample", "arithmetic", None),
    268: ("sample", "arithmetic", None),
    123: ("sample", "arithmetic", "Successful descendants stop reporting Mexican origin more often. That makes later "
                                  "generations look slightly worse, by about a tenth of the gap."),
    54: ("study", "extrapolated", None),
    # services
    230: ("count", "fitted", None),
    237: ("count", "fitted", None),
    211: ("count", "fitted", None),
    141: ("count", "fitted", None),
    80: ("count", "tabulated", None),
    # conventions
    238: ("count", "rule", None),
    257: ("count", "rule", None),
    253: ("count", "rule", None),
    # measured inputs
    208: ("sample", "fitted", "Census fills missing income with answers from similar people. For this group the "
                              "fill-ins run too high."),
    209: ("sample", "tabulated", "The CPS counts the Mexico-born 9–13% above the ACS."),
    206: ("count", "tabulated", None),
    217: ("count", "tabulated", None),
    254: ("sample", "arithmetic", None),  # on-books share from SSA applied to survey wages
    85: ("sample", "fitted", "Legal status is not asked. Rules impute it from other answers."),  # now in "status"
    255: ("count", "tabulated", None),
    225: ("sample", "arithmetic", None),
    267: ("count", "arithmetic", "Priced at state averages. The group's districts spend more than their state "
                                "averages, so the service side is likely too low."),
    127: ("sample", "tabulated", None),
    # outside the budget
    260: ("study", "extrapolated", None),
    264: ("study", "extrapolated", None),  # traffic elasticity from London, Manhattan, German strikes, 2020
    189: ("count", "arithmetic", "Jails record Hispanic ethnicity less often than people report it. Victims report "
                                 "the offender's ethnicity."),
    195: ("study", "extrapolated", None),
    258: ("study", "extrapolated", None),
    190: ("study", "fitted", None),
    265: ("study", "extrapolated", None),
    261: ("count", "arithmetic", None),
    248: ("sample", "fitted", None),
    262: ("platform", "fitted", "Only Facebook users aged 25–44 with 100+ US friends. Recent immigrants are "
                                "under-covered."),
    98: ("study", "model", None),
    # who pays
    226: ("sample", "arithmetic", None),
    194: ("sample", "arithmetic", None),
    250: ("study", "rule", None),
    139: ("count", "tabulated", None),
    # work
    166: ("study", "model", None),
    191: ("study", "model", None),
    132: ("study", "extrapolated", None),
    201: ("count", "fitted", None),
    53: ("sample", "fitted", None),
    # time
    162: ("count", "extrapolated", None),
    207: ("count", "extrapolated", None),
    131: ("sample", "model", "Successful descendants stop reporting Mexican origin more often, so later "
                             "generations look slightly worse."),
    240: ("sample", "arithmetic", None),
    # generations
    224: ("sample", "arithmetic", "The CPS puts 28% of the group's births with Mexico-born mothers. Birth records "
                                  "say 36%. So some children count in the wrong generation."),
    178: ("sample", "tabulated", "Successful descendants stop reporting Mexican origin more often. This explains "
                                 "about a tenth of the stall."),
    272: ("sample", "tabulated", "All Hispanics, not only Mexican-origin. In the CPS, Mexican-origin sons trail white "
                                 "men by more than Hispanic sons overall."),
    74: ("sample", "fitted", None),
    163: ("sample", "tabulated", None),
    83: ("sample", "tabulated", None),
    67: ("sample", "tabulated", None),
    154: ("study", "model", None),
    # crime
    144: ("count", "tabulated", None),
    65: ("sample", "tabulated", "Prison records code many Hispanics as generic \"other Hispanic\". The corrected "
                                "ratio is higher."),
    82: ("count", "fitted", None),
    202: ("count", "tabulated", "Some offenders have no recorded ethnicity. The ratios hold under every allocation "
                                "tried."),
    143: ("count", "arithmetic", None),
    214: ("count", "tabulated", None),
    56: ("count", "tabulated", None),
    # comparisons
    263: ("sample", "arithmetic", None),
    259: ("sample", "arithmetic", None),
    150: ("sample", "arithmetic", None),
    71: ("count", "tabulated", None),
    # status
    157: ("sample", "fitted", "Status is imputed. Assumptions about how many new arrivals the survey misses move "
                              "the newest cohort by up to 62%."),
    185: ("sample", "fitted", "Legal status is imputed by rules, not observed."),
    242: ("count", "tabulated", None),
    # civic
    87: ("sample", "fitted", None),
    147: ("count", "arithmetic", None),
    233: ("sample", "fitted", None),
    # claims
    212: ("count", "tabulated", None),
    244: ("count", "tabulated", None),
    245: ("count", "fitted", None),
    145: ("study", "tabulated", None),
    84: ("sample", "tabulated", None),
    # reading
    58: ("count", "rule", None),
    270: ("sample", "model", None),
}

INPUTS = {
    "count": ("records", "administrative records, registers or full counts"),
    "sample": ("sample survey", "a survey of a sample of people, with sampling error and self-reported answers"),
    "study": ("other study", "an estimate taken from another study or another population"),
    "platform": ("platform data", "data collected by a private platform"),
}
STEPS = {
    "tabulated": ("read off", "read directly from the data"),
    "arithmetic": ("accounting", "arithmetic on measured parts"),
    "fitted": ("fitted slope", "a relation estimated in the same data"),
    "extrapolated": ("extrapolated", "carried to other years, places or populations"),
    "model": ("model", "a model with assumed parameters"),
    "rule": ("rule", "an accounting convention, shown with a band"),
}
