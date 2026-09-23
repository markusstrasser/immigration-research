"""Print the RESULT.md tables from `derived/` so every quoted number comes from the CSVs.

Usage: `summarize.py` prints every part; `summarize.py --part headline cps` prints the named parts;
`summarize.py --fill RESULT.md` rewrites each `<!-- part: NAME -->` ... `<!-- /part -->` block in place."""
import re
import sys
from pathlib import Path

import pandas as pd

DERIVED = Path(__file__).resolve().parent / "derived"
LABELS = {
    "usb_mexican_hisp": "US-born, Mexican Hispanic origin",
    "usb_mexican_ancestry": "US-born, Mexican ancestry",
    "mexico_born": "Mexico-born, all",
    "mexico_born_naturalized": "Mexico-born, naturalized",
    "mexico_born_arrived_under_18": "Mexico-born, arrived before 18",
    "usb_asian_indian_ancestry": "US-born, Asian Indian ancestry",
    "usb_asian_indian_race": "US-born, Asian Indian race",
    "india_born": "India-born, all",
    "india_born_naturalized": "India-born, naturalized",
    "india_born_arrived_under_18": "India-born, arrived before 18",
    "usb_nh_white": "US-born non-Hispanic white",
    "usb_all": "All US-born",
}
SPECS = [("raw", "raw"), ("age_indirect", "same ages"), ("a_education_indirect", "(a) educ"),
         ("a_age_education_indirect", "(a) age × educ"), ("b_indirect_geo", "(b) geo, indirect"),
         ("b_indirect_full", "(b) full, indirect"), ("b_raked_geo", "(b) geo, raked"), ("b_raked_full", "(b) full, raked"),
         ("c_neighborhood_per_teen_15_17", "(c) tract income"), ("c_age_neighborhood_per_teen_15_17", "(c) + same ages")]
VARIANTS = [("age_direct", "age, direct"), ("age_indirect", "age, indirect"), ("a_education_direct", "educ, direct"),
            ("a_education_indirect", "educ, indirect"), ("a_age_education_direct", "age × educ, direct"),
            ("a_age_education_indirect", "age × educ, indirect"),
            ("c_neighborhood_per_youth_18_24", "(c) per 18–24"), ("c_neighborhood_per_household", "(c) per household"),
            ("c_age_neighborhood_per_youth_18_24", "(c) + ages, per 18–24"),
            ("c_age_neighborhood_per_household", "(c) + ages, per household")]


def pct(x, digits=2):
    return f"{100 * x:.{digits}f}"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" if i == 0 else "---:" for i in range(len(header))) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def military(sex, band, outcome="ever_active_duty"):
    rates = pd.read_csv(DERIVED / "military_rates.csv")
    adjusted = pd.read_csv(DERIVED / "military_adjusted.csv")
    rows = []
    for group, label in LABELS.items():
        r = rates[(rates.group == group) & (rates.sex == sex) & (rates.age_band == band) & (rates.universe == "all")
                  & (rates.outcome == outcome)].iloc[0]
        cells = [label, f"{r.n_records:,}", f"{pct(r.rate)} ({pct(r.se)})"]
        for spec, _ in SPECS:
            a = adjusted[(adjusted.group == group) & (adjusted.sex == sex) & (adjusted.age_band == band)
                         & (adjusted.outcome == outcome) & (adjusted.spec == spec)]
            cells.append("" if a.empty or pd.isna(a.ratio.iloc[0]) else f"{a.ratio.iloc[0]:.2f} ({a.ratio_se.iloc[0]:.2f})")
        rows.append(cells)
    header = ["Group", "records", "rate % (SE)"] + [name for _, name in SPECS]
    return f"**{outcome}, {sex}, ages {band}** — ratio to US-born non-Hispanic whites (SE)\n\n" + table(header, rows)


def headline():
    rates = pd.read_csv(DERIVED / "military_rates.csv")
    rows = []
    for group, label in LABELS.items():
        cells = [label]
        for sex, band, outcome in (("men", "18_49", "ever_active_duty"), ("women", "18_49", "ever_active_duty"),
                                   ("men", "25_34", "ever_active_duty"), ("men", "18_plus_born_1956_on", "ever_active_duty"),
                                   ("men", "18_24", "now_active_duty"), ("women", "18_24", "now_active_duty"),
                                   ("men", "18_49", "reserve_guard_only")):
            x = rates[(rates.group == group) & (rates.sex == sex) & (rates.age_band == band)
                      & (rates.outcome == outcome) & (rates.universe == "all")].iloc[0]
            cells.append(f"{pct(x.rate)} ({pct(x.se)}) · {x.ratio_to_nh_white:.2f}")
        rows.append(cells)
    header = ["Group", "ever, men 18–49", "ever, women 18–49", "ever, men 25–34", "ever, men 18+ born 1956+",
              "now, men 18–24", "now, women 18–24", "reserve/Guard only, men 18–49"]
    return ("**Per capita: % of each group (SE) · ratio to US-born non-Hispanic whites.** \"ever\" = ever on active "
            "duty (`MIL` 1–2); \"now\" = on active duty now (`MIL` 1)\n\n" + table(header, rows))


ADJUSTED_GROUPS = ["usb_mexican_hisp", "usb_mexican_ancestry", "mexico_born", "mexico_born_naturalized",
                   "usb_asian_indian_ancestry", "usb_asian_indian_race", "india_born", "india_born_naturalized"]


def adjustments(sex, band):
    adjusted = pd.read_csv(DERIVED / "military_adjusted.csv")
    birth = pd.read_csv(DERIVED / "military_birthstate.csv")
    columns = [(adjusted, "raw"), (adjusted, "age_indirect"), (adjusted, "a_age_education_indirect"),
               (adjusted, "a_age_education_direct"), (birth, "b_birthstate_indirect_full"),
               (birth, "b_birthstate_raked_full"), (adjusted, "b_indirect_full"), (adjusted, "b_raked_full"),
               (adjusted, "c_neighborhood_per_teen_15_17"), (adjusted, "c_age_neighborhood_per_teen_15_17")]
    rows = []
    for group in ADJUSTED_GROUPS:
        cells = [LABELS[group]]
        for frame, spec in columns:
            x = frame[(frame.group == group) & (frame.sex == sex) & (frame.age_band == band)
                      & (frame.outcome == "ever_active_duty") & (frame.spec == spec)]
            cells.append("—" if x.empty else f"{x.ratio.iloc[0]:.2f} ({x.ratio_se.iloc[0]:.2f})")
        rows.append(cells)
    header = ["Group", "raw", "same ages", "(a) age × educ, own mix", "(a) age × educ, white mix",
              "(b) birth state, own mix", "(b) birth state, raked", "(b) residence, own mix", "(b) residence, raked",
              "(c) tract income", "(c) + same ages"]
    return (f"**Ever on active duty, {sex} {band.replace('_', '–')}: ratio to US-born non-Hispanic whites (SE) under "
            "each adjustment.** \"own mix\" = indirect standardisation (white rates in the group's own cells); "
            "\"white mix\" and \"raked\" = the group reweighted to the white distribution. (b) uses age × "
            "education × state (and metro size at residence)\n\n" + table(header, rows))


def variants(sex, band, outcome="ever_active_duty"):
    adjusted = pd.read_csv(DERIVED / "military_adjusted.csv")
    rows = []
    for group, label in LABELS.items():
        if group == "usb_nh_white":
            continue
        cells = [label]
        for spec, _ in VARIANTS:
            a = adjusted[(adjusted.group == group) & (adjusted.sex == sex) & (adjusted.age_band == band)
                         & (adjusted.outcome == outcome) & (adjusted.spec == spec)]
            cells.append("" if a.empty or pd.isna(a.ratio.iloc[0]) else f"{a.ratio.iloc[0]:.2f} ({a.ratio_se.iloc[0]:.2f})")
        rows.append(cells)
    return (f"**Direct and indirect versions and other (c) bases, {outcome}, {sex}, ages {band}** — ratio to US-born "
            "NH whites (SE)\n\n" + table(["Group"] + [name for _, name in VARIANTS], rows))


def regions(group, sex, band, by):
    frame = pd.read_csv(DERIVED / "military_by_region.csv")
    x = frame[(frame.group == group) & (frame.sex == sex) & (frame.age_band == band) & (frame.by == by)]
    x = pd.concat([x[x.region == "all"], x[x.region != "all"].sort_values("share_of_group", ascending=False)])
    rows = [[r.region.replace("_", " "), f"{r.n_records:,}", f"{100 * r.share_of_group:.1f}", f"{pct(r.rate)} ({pct(r.se)})",
             f"{pct(r.white_rate)} ({pct(r.white_se)})", f"{r.ratio:.2f} ({r.ratio_se:.2f})",
             f"{r.ratio_age_standardised:.2f} ({r.ratio_age_standardised_se:.2f})"] for r in x.itertuples()]
    header = [by.replace("_", " "), "records", "% of group", "rate % (SE)", "white rate % (SE)", "ratio (SE)",
              "at same ages (SE)"]
    return (f"**{LABELS[group]}, ever on active duty, {sex}, ages {band}, by {by.replace('_', ' ')}** — against "
            f"US-born NH whites of the same {by.split('_')[0]} region\n\n" + table(header, rows))


def raking_diagnostics(sex, band):
    adjusted = pd.read_csv(DERIVED / "military_adjusted.csv")
    rows = []
    for group, label in LABELS.items():
        a = adjusted[(adjusted.group == group) & (adjusted.sex == sex) & (adjusted.age_band == band)
                     & (adjusted.outcome == "ever_active_duty") & adjusted.spec.isin(["b_raked_geo", "b_raked_full"])]
        for _, x in a.iterrows():
            rows.append([label, x.spec, f"{x.n_records:,}", f"{x.n_eff:,.0f}", f"{x.top10_cell_share:.0%}",
                         f"{x.max_factor:,.0f}", f"{x.ref_share_off_support:.1%}", x.margins, int(x.replicate_fallbacks)])
    header = ["Group", "spec", "records", "Kish n_eff", "top-10 cells' share of numerator", "max/median factor",
              "white weight off support", "margins", "replicate fallbacks"]
    return f"**Raking diagnostics, {sex}, ages {band}**\n\n" + table(header, rows)


def education(sex, band):
    by_educ = pd.read_csv(DERIVED / "military_by_education.csv")
    rows = []
    for group, label in LABELS.items():
        cells = [label]
        for educ in ("less_than_hs", "hs_diploma", "some_college", "ba_plus"):
            x = by_educ[(by_educ.group == group) & (by_educ.sex == sex) & (by_educ.age_band == band)
                        & (by_educ.outcome == "ever_active_duty") & (by_educ.education == educ)]
            cells.append("" if x.empty else f"{pct(x.rate.iloc[0], 1)} ({pct(x.se.iloc[0], 1)}) n={x.n_records.iloc[0]:,}")
        rows.append(cells)
    return (f"**Ever on active duty by own education, {sex}, ages {band}** — rate % (SE), records\n\n"
            + table(["Group", "less than HS", "HS diploma", "some college", "BA+"], rows))


def other_outcomes():
    rates = pd.read_csv(DERIVED / "military_rates.csv")
    rows = []
    for group, label in LABELS.items():
        cells = [label]
        for sex, band, outcome, universe in (("men", "18_24", "now_active_duty", "all"),
                                             ("women", "18_24", "now_active_duty", "all"),
                                             ("men", "18_49", "reserve_guard_only", "all"),
                                             ("men", "18_49", "ever_active_duty", "household"),
                                             ("men", "18_plus_born_1956_on", "ever_active_duty", "all")):
            x = rates[(rates.group == group) & (rates.sex == sex) & (rates.age_band == band)
                      & (rates.outcome == outcome) & (rates.universe == universe)].iloc[0]
            cells.append(f"{pct(x.rate)} ({pct(x.se)}); {x.ratio_to_nh_white:.2f}")
        now = rates[(rates.group == group) & (rates.sex == "men") & (rates.age_band == "18_24")
                    & (rates.outcome == "now_active_duty") & (rates.universe == "all")].iloc[0]
        cells.append(f"{now.share_in_group_quarters:.0%}")
        rows.append(cells)
    header = ["Group", "now active duty, men 18–24", "now active duty, women 18–24", "reserve/Guard only, men 18–49",
              "ever active, men 18–49, households only", "ever active, men 18+ born 1956+",
              "share of men 18–24 on active duty living in group quarters"]
    return "**Other outcomes** — rate % (SE); ratio to US-born NH whites\n\n" + table(header, rows)


def protective(occupation, per):
    frame = pd.read_csv(DERIVED / "protective_service.csv")
    rows = []
    for group, label in LABELS.items():
        cells = [label]
        for sex in ("men", "women"):
            x = frame[(frame.group == group) & (frame.sex == sex) & (frame.outcome == occupation)
                      & (frame.per_1000 == per)]
            raw = x[x.spec == "raw"].iloc[0]
            cells.append(f"{1000 * raw.group_rate:.1f} ({1000 * raw.group_rate_se:.1f})")
            for spec in ("raw", "age_indirect", "a_age_education_indirect", "b_indirect_full", "b_raked_full"):
                y = x[x.spec == spec]
                cells.append("" if y.empty else f"{y.ratio.iloc[0]:.2f} ({y.ratio_se.iloc[0]:.2f})")
        rows.append(cells)
    header = ["Group"] + [f"{s}: {h}" for s in ("men", "women") for h in
                          ("per 1,000 (SE)", "ratio raw", "same ages", "(a) age × educ", "(b) full indirect",
                           "(b) full raked")]
    return f"**{occupation}, per 1,000 {per} aged 18–64** — ratio to US-born NH whites (SE)\n\n" + table(header, rows)


def cps():
    rates = pd.read_csv(DERIVED / "cps_civic_rates.csv")
    gaps = pd.read_csv(DERIVED / "cps_civic_gaps.csv")
    labels = {"mexico_born": "Mexico-born", "mexico_born_citizen": "Mexico-born citizens",
              "mexican_2nd_gen": "Mexican second generation", "mexican_3rd_plus": "Mexican third-plus",
              "india_born": "India-born", "india_born_citizen": "India-born citizens",
              "indian_2nd_gen": "Indian second generation", "usb_asian_indian_selfid": "US-born Asian Indian (self-ID)",
              "usb_nh_white": "US-born NH white", "usb_all": "All US-born"}
    rows = []
    for group, label in labels.items():
        cells = [label]
        for arm, measure in (("adults_18_plus", "volunteered"), ("adults_18_plus", "gave_over_25"),
                             ("ba_plus", "volunteered"), ("ba_plus", "gave_over_25"),
                             ("men_18_plus_born_1956_on", "veteran")):
            x = rates[(rates.arm == arm) & (rates.group == group) & (rates.measure == measure)].iloc[0]
            cells.append(f"{pct(x.rate, 1)} ({pct(x.se, 1)}) n={x.n:,}")
        rows.append(cells)
    out = [("**CPS September 2021+2023, rates % (SE)**\n\n"
            + table(["Group", "volunteered, 18+", "gave >$25, 18+", "volunteered, BA+", "gave >$25, BA+",
                     "veteran, men born 1956+"], rows))]
    rows = []
    for measure in ("volunteered", "gave_over_25", "veteran", "volunteered_pes16"):
        for group in ("mexico_born", "mexican_2nd_gen", "mexican_3rd_plus", "india_born", "indian_2nd_gen"):
            cells = [measure, labels[group]]
            for spec in ("raw", "ses", "ses_geo"):
                x = gaps[(gaps.measure == measure) & (gaps.group == group) & (gaps.spec == spec)].iloc[0]
                cells.append(f"{x.gap_points:+.1f} ({x.se_points:.1f})")
            rows.append(cells)
    out.append("**Gap to US-born NH whites, percentage points (SE)**\n\n"
               + table(["measure", "group", "raw", "SES-adjusted", "SES + state + metro"], rows))
    return "\n\n".join(out)


def birthstate(sex, band):
    adjusted = pd.read_csv(DERIVED / "military_adjusted.csv")
    birth = pd.read_csv(DERIVED / "military_birthstate.csv")
    movers = pd.read_csv(DERIVED / "military_movers.csv")
    rows = []
    for group in ("usb_mexican_hisp", "usb_mexican_ancestry", "usb_asian_indian_ancestry", "usb_asian_indian_race",
                  "usb_all"):
        def cell(frame, spec):
            x = frame[(frame.group == group) & (frame.sex == sex) & (frame.age_band == band)
                      & (frame.outcome == "ever_active_duty") & (frame.spec == spec)].iloc[0]
            return f"{x.ratio:.2f} ({x.ratio_se:.2f})"
        m = movers[(movers.group == group) & (movers.sex == sex) & (movers.age_band == band)].iloc[0]
        rows.append([LABELS[group], cell(adjusted, "raw"), cell(adjusted, "age_indirect"), cell(adjusted, "b_indirect_full"),
                     cell(birth, "b_birthstate_indirect_full"), cell(adjusted, "b_raked_full"),
                     cell(birth, "b_birthstate_raked_full"), cell(birth, "b_birthstate_raked_geo"),
                     f"{m.share_outside_birth_state:.0%}",
                     f"{pct(m.ever_rate_stayers, 1)} / {pct(m.ever_rate_movers, 1)}",
                     f"{m.ratio_stayers:.2f} ({m.ratio_se_stayers:.2f}) / {m.ratio_movers:.2f} ({m.ratio_se_movers:.2f})"])
    white = movers[(movers.group == "usb_nh_white") & (movers.sex == sex) & (movers.age_band == band)].iloc[0]
    rows.append([LABELS["usb_nh_white"], "1.00", "", "", "", "", "", "", f"{white.share_outside_birth_state:.0%}",
                 f"{pct(white.ever_rate_stayers, 1)} / {pct(white.ever_rate_movers, 1)}", "1.00 / 1.00"])
    header = ["Group", "raw", "same ages", "(b) full indirect, residence", "(b) full indirect, birth state",
              "(b) full raked, residence", "(b) full raked, birth state", "(b) geo raked, birth state",
              "living outside birth state", "ever-served % stayers / movers", "ratio stayers / movers"]
    return (f"**Residence versus birth state, ever on active duty, {sex}, ages {band}** — ratio to US-born NH "
            "whites (SE)\n\n" + table(header, rows))


def neighborhood():
    frame = pd.read_csv(DERIVED / "neighborhood_expected.csv")
    rows = []
    for group in ("us_born_nh_white", "us_born_all", "us_born_mexican_origin", "mexico_born", "us_born_asian_indian",
                  "india_born", "teen_15_17_nh_white", "teen_15_17_hispanic", "teen_15_17_asian"):
        cells = [group]
        for fy in ("FY23", "FY22"):
            for basis in ("per_teen_15_17", "per_youth_18_24", "per_household"):
                x = frame[(frame.fiscal_year == fy) & (frame.group == group) & (frame.propensity_basis == basis)]
                cells.append(f"{x.expected_ratio_to_nh_white.iloc[0]:.3f}")
        rows.append(cells)
    header = ["Group (tract counts)"] + [f"{fy} {b}" for fy in ("FY23", "FY22")
                                         for b in ("per 15–17", "per 18–24", "per household")]
    props = frame[(frame.group == "us_born_nh_white")].drop_duplicates(["fiscal_year", "propensity_basis"])
    prop_rows = [[f"{x.fiscal_year} {x.propensity_basis}"] + [f"{x[f'propensity_q{q}']:.2f}" for q in range(1, 6)]
                 for _, x in props.iterrows()]
    quint = pd.read_csv(DERIVED / "neighborhood_quintiles.csv")
    quint_rows = [[x.group] + [f"{100 * x[f'q{q}_share']:.1f}" for q in range(1, 6)]
                  for _, x in quint[quint.fiscal_year == "FY23"].iterrows()]
    return ("**(c) Expected ratio to US-born NH whites if only home-tract income mattered**\n\n" + table(header, rows)
            + "\n\n**Relative accession propensity by tract-income quintile (1 = poorest)**\n\n"
            + table(["basis", "Q1", "Q2", "Q3", "Q4", "Q5"], prop_rows)
            + "\n\n**Population shares by FY23 tract-income quintile, %**\n\n"
            + table(["group", "Q1", "Q2", "Q3", "Q4", "Q5"], quint_rows))


PARTS = {
    "headline": headline,
    "adjust_men_18_49": lambda: adjustments("men", "18_49"),
    "adjust_men_25_49": lambda: adjustments("men", "25_49"),
    "adjust_women_18_49": lambda: adjustments("women", "18_49"),
    "neighborhood": neighborhood,
    "birthstate_men_18_49": lambda: birthstate("men", "18_49"),
    "birthstate_men_25_49": lambda: birthstate("men", "25_49"),
    "birthstate_women_18_49": lambda: birthstate("women", "18_49"),
    "regions_mex_men_birth": lambda: regions("usb_mexican_hisp", "men", "18_49", "birth_region"),
    "regions_mex_men_residence": lambda: regions("usb_mexican_hisp", "men", "18_49", "residence_region"),
    "regions_mex_women_birth": lambda: regions("usb_mexican_hisp", "women", "18_49", "birth_region"),
    "regions_indian_men_birth": lambda: regions("usb_asian_indian_ancestry", "men", "18_49", "birth_region"),
    "military_men_18_49": lambda: military("men", "18_49"),
    "variants_men_18_49": lambda: variants("men", "18_49"),
    "variants_women_18_49": lambda: variants("women", "18_49"),
    "military_men_25_49": lambda: military("men", "25_49"),
    "military_men_25_34": lambda: military("men", "25_34"),
    "military_men_born_1956_on": lambda: military("men", "18_plus_born_1956_on"),
    "military_women_18_49": lambda: military("women", "18_49"),
    "military_women_25_49": lambda: military("women", "25_49"),
    "military_now_men_18_24": lambda: military("men", "18_24", "now_active_duty"),
    "education_men_25_49": lambda: education("men", "25_49"),
    "education_women_25_49": lambda: education("women", "25_49"),
    "other_outcomes": other_outcomes,
    "raking_men_25_49": lambda: raking_diagnostics("men", "25_49"),
    "raking_women_25_49": lambda: raking_diagnostics("women", "25_49"),
    "protective_public_safety_workers": lambda: protective("public_safety_total", "employed"),
    "protective_police_workers": lambda: protective("police_sheriff_detective", "employed"),
    "protective_public_safety_adults": lambda: protective("public_safety_total", "adults"),
    "protective_soc33_workers": lambda: protective("all_protective_service_soc33", "employed"),
    "protective_security_guards": lambda: protective("security_guard", "employed"),
    "cps": cps,
}


def fill(path):
    """Rewrite every `<!-- part: NAME -->` ... `<!-- /part -->` block of a Markdown file from the CSVs."""
    text = Path(path).read_text()
    pattern = re.compile(r"<!-- part: (\S+) -->\n.*?<!-- /part -->", re.S)
    names = pattern.findall(text)
    unknown = [n for n in names if n not in PARTS]
    assert not unknown, f"unknown parts: {unknown}"
    Path(path).write_text(pattern.sub(lambda m: f"<!-- part: {m.group(1)} -->\n{PARTS[m.group(1)]()}\n<!-- /part -->", text))
    print(f"  ✓ {path}: {len(names)} tables refreshed")


def main():
    """Print every table with its part marker; `--part NAME ...` prints named parts; `--fill FILE` refreshes FILE."""
    if "--fill" in sys.argv:
        return fill(sys.argv[sys.argv.index("--fill") + 1])
    names = sys.argv[sys.argv.index("--part") + 1:] if "--part" in sys.argv else list(PARTS)
    print("\n\n".join(f"<!-- part: {name} -->\n{PARTS[name]()}\n<!-- /part -->" for name in names))


if __name__ == "__main__":
    sys.exit(main())
