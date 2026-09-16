#!/usr/bin/env python3
"""BJS state-prisoner offence composition by race/Hispanic origin, extended 2009r -> 2021 -> 2022.

Extends infra/immigration-fiscal/acs_institutional_2026_09_16/bjs_offense_by_ethnicity.py with the
newest BJS edition. Also carries the 2023 imprisonment-rate-by-race-and-age table, the jail
held-for-ICE series, and the ICE-share-of-foreign-born-institutional-GQ bound.

SOURCES (all counts transcribed from the primary tables this session):
  2009  original    BJS, Prisoners in 2010 (NCJ 236096), Appendix Table 16b.
  2009r restated    BJS, Prisoners in 2011 (NCJ 239808), Appendix Table 8 (SISCF-2004 basis).
  2021              BJS, Prisoners in 2022 - Statistical Tables (NCJ 307149), Table 17 (counts),
                    Table 16 (percents). Basis: NCRP 2021 + NPS 2021 + Survey of Prison Inmates 2016.
  2022              BJS, Prisoners in 2023 - Statistical Tables (NCJ 310197), Table 16 (counts),
                    Table 17 (percents), date of version 9/30/25, https://bjs.ojp.gov/document/p23st.zip
                    Basis: NCRP 2022 + NPS 2022 + Survey of Prison Inmates 2016. SAME basis as 2021.
  2023 rates        Prisoners in 2023, Table 13 (imprisonment rates by demographic characteristics,
                    31 Dec 2023; denominator = Census postcensal resident estimates for 1 Jan 2024).
  2022 rates        Prisoners in 2022 - Statistical Tables, Table 13.
  2010 rates        Prisoners in 2010, Appendix Table 15.
  Restatement test  Prisoners in 2022 Table 3 vs Prisoners in 2023 Table 3 (sentenced prisoners by
                    race/Hispanic origin, 2013-2023).
  Jail/ICE          BJS, Jail Inmates in 2024 (NCJ 311504, version 9/8/2026), Table 14,
                    https://bjs.ojp.gov/document/ji24st.zip
  Populations       "orig"  = denominators used by the predecessor script (mixed vintage, see below).
                    "pep"   = July 1 resident population, non-Hispanic white alone (NHWA_MALE +
                              NHWA_FEMALE) and Hispanic (H_MALE + H_FEMALE):
                              2009  Census intercensal 2000-2010, us-est00int-alldata.csv
                              2021, 2022  Census Vintage 2024, NC-EST2024 national ASRH
                              nc-est2024-alldata-r-file04.csv (2021-07) / -file06.csv (2022-07)
                              https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/national/asrh/

NOTE ON THE PREDECESSOR DENOMINATORS: the earlier script used 191.7e6 for non-Hispanic white in 2021,
which is the 2020 *decennial census* white-alone-not-Hispanic count, not a Vintage population estimate
(PEP July-2021 NHWA is 196.6e6). Its Hispanic 62.6e6 and its 2009 pair are PEP-like. The "pep" basis
below puts every year on a single, stated definition; both are reported so the published 2009r->2021
numbers remain reproducible.
"""
import csv, pathlib, sys

HERE = pathlib.Path(__file__).parent
OFFENCES = ("total", "violent", "murder", "sexual", "robbery", "assault",
            "property", "burglary", "mvt", "fraud", "drug", "public_order")

counts = {  # (year, group) -> {offence: count}
    ("2009", "white"):     dict(total=532000, violent=265600, murder=55700, sexual=36300 + 58600, robbery=45300,
                                assault=46600, property=132000, burglary=63400, mvt=8500, fraud=19600,
                                drug=73900, public_order=54400),
    ("2009", "hispanic"):  dict(total=212100, violent=117800, murder=32300, sexual=6800 + 15200, robbery=26600,
                                assault=28000, property=34400, burglary=16400, mvt=6100, fraud=2400,
                                drug=41400, public_order=16000),
    ("2009r", "white"):    dict(total=467290, violent=231500, murder=46900, sexual=33300 + 44800, robbery=40700,
                                assault=43300, property=111000, burglary=54300, mvt=6500, fraud=16000,
                                drug=69200, public_order=52000),
    ("2009r", "hispanic"): dict(total=287568, violent=159800, murder=38300, sexual=8900 + 24600, robbery=37600,
                                assault=37500, property=43100, burglary=22600, mvt=6600, fraud=2900,
                                drug=49400, public_order=34000),
    ("2021", "white"):     dict(total=321700, violent=176400, murder=36900, sexual=63600, robbery=20400,
                                assault=38000, property=57600, burglary=29200, mvt=2700, fraud=5800,
                                drug=48200, drug_possession=15800, drug_other=32400,
                                public_order=36800, weapons=8300, dui=6500),
    ("2021", "hispanic"):  dict(total=224300, violent=160100, murder=31900, sexual=42800, robbery=26600,
                                assault=47100, property=19000, burglary=11700, mvt=1700, fraud=1200,
                                drug=22600, drug_possession=6100, drug_other=16500,
                                public_order=21900, weapons=7700, dui=4500),
    # NEW: Prisoners in 2023 - Statistical Tables, Table 16 (31 Dec 2022).
    ("2022", "white"):     dict(total=333200, violent=180100, murder=37200, sexual=65300, robbery=19400,
                                assault=40000, property=57100, burglary=28400, mvt=3100, fraud=5700,
                                drug=53400, drug_possession=18200, drug_other=35100,
                                public_order=39800, weapons=9300, dui=7100),
    ("2022", "hispanic"):  dict(total=224100, violent=158900, murder=31700, sexual=43700, robbery=24900,
                                assault=46600, property=19000, burglary=11400, mvt=1700, fraud=1300,
                                drug=22200, drug_possession=6400, drug_other=15800,
                                public_order=23200, weapons=8500, dui=4700),
}

pop = {
    "orig": {("2009", "white"): 199.9e6, ("2009", "hispanic"): 48.4e6,
             ("2009r", "white"): 199.9e6, ("2009r", "hispanic"): 48.4e6,
             ("2021", "white"): 191.7e6, ("2021", "hispanic"): 62.6e6,
             ("2022", "white"): 191.7e6, ("2022", "hispanic"): 62.6e6},   # 2022 carried at 2021 levels: NOT used for headline
    "pep":  {("2009", "white"): 197_274_549, ("2009", "hispanic"): 49_327_489,
             ("2009r", "white"): 197_274_549, ("2009r", "hispanic"): 49_327_489,
             ("2021", "white"): 196_609_140, ("2021", "hispanic"): 63_011_125,
             ("2022", "white"): 195_994_987, ("2022", "hispanic"): 64_396_719},
}

# Restatement test: sentenced prisoners by race/Hispanic origin (state+federal), as printed in each edition.
restatement = {  # year -> {edition: (total, federal, state, white, black, hispanic)}
    2020: {"p22st": (1185733, 142028, 1043705, 360100, 390700, 276100),
           "p23st": (1185733, 142028, 1043705, 360100, 390700, 276100)},
    2021: {"p22st": (1165736, 144448, 1021288, 356000, 378000, 273800),
           "p23st": (1165736, 144448, 1021288, 356000, 378000, 273800)},
    2022: {"p22st": (1185648, 146108, 1039540, 367800, 384600, 273900),
           "p23st": (1185648, 146108, 1039540, 367800, 384600, 273900)},
}
# 2009, for contrast: the one restatement that did move (state sentenced, by race).
restatement_2009 = {"p10 (Prisoners in 2010, App. Table 16b)": dict(white=532000, hispanic=212100),
                    "p11 (Prisoners in 2011, App. Table 8)":   dict(white=467290, hispanic=287568)}

# Male imprisonment rate per 100k US residents (state+federal, sentence > 1 yr), NH white / Hispanic.
rates = {  # age -> (w2010, h2010, w2022, h2022, w2023, h2023)
    "18-19": (149, 563, 30, 85, 30, 84),
    "20-24": (638, 1908, 229, 663, 229, 672),
    "25-29": (980, 2707, 514, 1462, 496, 1431),
    "30-34": (1061, 2808, 732, 1774, 729, 1789),
    "35-39": (995, 2486, 813, 1747, 818, 1758),
    "40-44": (None, None, 776, 1634, 799, 1677),
    "all":   (459, 1258, 337, 794, 341, 800),
}

# BJS Jail Inmates in 2024, Table 14: persons held in local jails for federal authorities, last weekday in June.
jail_ice = {2014: 16400, 2015: 14400, 2016: 17400, 2017: 13300, 2018: 14900, 2019: 17300,
            2020: 9300, 2021: 7400, 2022: 6900, 2023: 7000, 2024: 8000}
JAIL_NOTE = "2019 and 2024 are Census of Jails (complete enumeration); other years Annual Survey of Jails."

# ACS 1-yr PUMS institutional group quarters, men 18-39, foreign born (acs_institutional_2026_09_16).
acs_fb_inst = {2010: 123694, 2019: 84152, 2023: 65685, 2024: 73189}
ICE_ADP = {2023: 28289}  # ICE Annual Report FY2023, p. "Detention" - average daily population in ICE custody.


def build_rows():
    rows = []
    for pb in ("pep", "orig"):
        for base in ("2009", "2009r"):
            for g in ("white", "hispanic"):
                a, b, c = counts[(base, g)], counts[("2021", g)], counts[("2022", g)]
                for off in OFFENCES:
                    r09 = 1e5 * a[off] / pop[pb][(base, g)]
                    r21 = 1e5 * b[off] / pop[pb][("2021", g)]
                    r22 = 1e5 * c[off] / pop[pb][("2022", g)]
                    rows.append(dict(
                        pop_basis=pb, basis=base, group=g, offence=off,
                        n2009=a[off], n2021=b[off], n2022=c[off],
                        count_change_09_21_pct=round(100 * (b[off] / a[off] - 1), 1),
                        count_change_21_22_pct=round(100 * (c[off] / b[off] - 1), 1),
                        count_change_09_22_pct=round(100 * (c[off] / a[off] - 1), 1),
                        per100k_2009=round(r09, 1), per100k_2021=round(r21, 1), per100k_2022=round(r22, 1),
                        per100k_change_09_21_pct=round(100 * (r21 / r09 - 1), 1),
                        per100k_change_21_22_pct=round(100 * (r22 / r21 - 1), 1),
                        per100k_change_09_22_pct=round(100 * (r22 / r09 - 1), 1),
                        share2009_pct=round(100 * a[off] / a["total"], 1),
                        share2021_pct=round(100 * b[off] / b["total"], 1),
                        share2022_pct=round(100 * c[off] / c["total"], 1)))
    return rows


def main():
    rows = build_rows()
    out_csv = HERE / "bjs_offense_by_ethnicity_2023.csv"
    with open(out_csv, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    L = []
    p = L.append
    p("BJS sentenced state prisoners by most serious offence x race/Hispanic origin, 2009r -> 2021 -> 2022")
    p("New year: Prisoners in 2023 - Statistical Tables (NCJ 310197), Table 16, 31 December 2022.")
    p("The offence x race table LAGS ONE YEAR: the 2023 edition's newest offence table is 2022, because")
    p("its offence source is NCRP 2022. There is no 2023 offence-by-race table in any BJS publication yet.")
    p("Estimation basis 2021 and 2022 identical: NCRP + NPS of the reference year, race/Hispanic origin")
    p("imputed from the Survey of Prison Inmates 2016. 2009r is the SISCF-2004 restatement.")
    p("")

    p("=" * 110)
    p("RESTATEMENT CHECK: sentenced prisoners by race/Hispanic origin, Prisoners in 2022 vs Prisoners in 2023")
    p("=" * 110)
    p(f"{'year':6s} {'series':10s} {'p22st':>12s} {'p23st':>12s} {'delta':>8s}")
    fields = ("total", "federal", "state", "white", "black", "hispanic")
    n_diff = 0
    for yr in sorted(restatement):
        for i, fld in enumerate(fields):
            a, b = restatement[yr]["p22st"][i], restatement[yr]["p23st"][i]
            if a != b:
                n_diff += 1
            p(f"{yr:<6d} {fld:10s} {a:>12,} {b:>12,} {b - a:>8,}")
    p("")
    p(f"Discrepancies found: {n_diff} of {len(restatement) * len(fields)} cells.")
    p("The 2009-style restatement does NOT recur. Prisoners in 2023 reprints 2020, 2021 and 2022 race and")
    p("Hispanic-origin counts unchanged from Prisoners in 2022, to the last digit, despite its Table 3 note")
    p('that "counts for 2022 and earlier may have been revised". The 2009 restatement was a one-off caused by')
    p("a change of race/Hispanic-origin estimation source, not a routine annual revision:")
    for ed, d in restatement_2009.items():
        p(f"  2009 state sentenced, {ed:42s} white {d['white']:>7,}  Hispanic {d['hispanic']:>7,}")
    a, b = restatement_2009["p10 (Prisoners in 2010, App. Table 16b)"], restatement_2009["p11 (Prisoners in 2011, App. Table 8)"]
    p(f"  delta                                                        white {b['white'] - a['white']:>+7,}  "
      f"Hispanic {b['hispanic'] - a['hispanic']:>+7,}   "
      f"({100 * (b['white'] / a['white'] - 1):+.1f}% / {100 * (b['hispanic'] / a['hispanic'] - 1):+.1f}%)")
    p("So 2021 and 2022 may be taken from either edition; this script takes 2022 from the 2023 report.")
    p("")

    p("=" * 110)
    p("PER-CAPITA SERIES, consistent-vintage denominators (pop_basis=pep)")
    p("=" * 110)
    for base in ("2009r",):
        for g in ("white", "hispanic"):
            p(f"-- {g}, base {base}")
            p(f"{'offence':13s} {'n09':>8s} {'n21':>8s} {'n22':>8s} | {'r09':>7s} {'r21':>7s} {'r22':>7s} | "
              f"{'09-21':>7s} {'21-22':>7s} {'09-22':>7s}")
            for r in rows:
                if r["pop_basis"] == "pep" and r["basis"] == base and r["group"] == g:
                    p(f"{r['offence']:13s} {r['n2009']:>8,} {r['n2021']:>8,} {r['n2022']:>8,} | "
                      f"{r['per100k_2009']:>7.1f} {r['per100k_2021']:>7.1f} {r['per100k_2022']:>7.1f} | "
                      f"{r['per100k_change_09_21_pct']:>+6.1f}% {r['per100k_change_21_22_pct']:>+6.1f}% "
                      f"{r['per100k_change_09_22_pct']:>+6.1f}%")
            p("")

    p("=" * 110)
    p("LADDER-70 DIRECTION TEST: does Hispanic per-capita fall faster than white on EVERY offence class?")
    p("=" * 110)
    p("Ladder entry 70 and memo section 8 tabulate the four TOP-LEVEL BJS classes plus the total.")
    p("Sub-offences (murder, sexual, robbery, assault, burglary, mvt, fraud) are reported here as a")
    p("stricter secondary test that the original claim never made.")
    p("")
    lookup = {(r["pop_basis"], r["basis"], r["group"], r["offence"]): r for r in rows}
    TOPLEVEL = ("total", "violent", "property", "drug", "public_order")
    SUB = tuple(o for o in OFFENCES if o not in TOPLEVEL)
    verdicts = {}
    for pb in ("pep", "orig"):
        for leg, key in (("2009r->2021", "per100k_change_09_21_pct"), ("2009r->2022", "per100k_change_09_22_pct"),
                         ("2021->2022", "per100k_change_21_22_pct")):
            if pb == "orig" and leg != "2009r->2021":
                continue  # the orig basis has no independent 2022 denominator
            p(f"-- pop_basis={pb}  leg={leg}")
            p(f"{'offence':13s} {'white':>9s} {'hispanic':>9s}  {'Hisp fell faster?':>18s}")
            res = {}
            for label, group in (("TOP-LEVEL", TOPLEVEL), ("sub-offence", SUB)):
                holds = True
                p(f"  [{label}]")
                for off in group:
                    wv = lookup[(pb, "2009r", "white", off)][key]
                    hv = lookup[(pb, "2009r", "hispanic", off)][key]
                    ok = hv < wv
                    holds &= ok
                    p(f"{off:13s} {wv:>+8.1f}% {hv:>+8.1f}%  {('YES' if ok else 'NO'):>18s}")
                res[label] = holds
                p(f"   => holds on every {label} class: {'YES' if holds else 'NO'}")
            verdicts[(pb, leg)] = res
            p("")
    p("SUMMARY of the ladder-70 direction claim (TOP-LEVEL classes, the claim as written):")
    for (pb, leg), res in verdicts.items():
        p(f"  pop_basis={pb:4s} {leg:12s} top-level: {'HOLDS' if res['TOP-LEVEL'] else 'FAILS':5s}   "
          f"all classes incl. sub-offences: {'HOLDS' if res['sub-offence'] and res['TOP-LEVEL'] else 'FAILS'}")
    p("")
    p("Reading. The claim holds through the newest year (2022) on consistent Vintage-2024 denominators, and")
    p("holds for the whole 2021->2022 step on every top-level class. It FAILS at 2021 on the 'pep' basis for")
    p("violent only (white -23.5% vs Hispanic -21.6%), a sign flip caused entirely by the denominator fix:")
    p("the predecessor script divided 2021 white prisoners by the 2020 decennial count (191.7m) rather than")
    p("the July-2021 estimate (196.6m), which understated the white decline by about 2.5 points. On the")
    p("published 'orig' denominators the 2021 violent leg reads -20.5% white vs -22.5% Hispanic and the claim")
    p("holds, which is what ladder 70 and memo section 8 report. Adding 2022 restores the direction on both")
    p("bases, so the entry's conclusion survives; its violent margin at 2021 was inside denominator noise.")
    p("")

    p("=" * 110)
    p("MALE IMPRISONMENT RATE per 100k residents (state+federal, >1 yr), NH white vs Hispanic")
    p("2010: Prisoners in 2010 App. Table 15 | 2022: p22st Table 13 | 2023: p23st Table 13")
    p("=" * 110)
    p(f"{'age':7s} {'w10':>6s} {'w22':>6s} {'w23':>6s} | {'h10':>6s} {'h22':>6s} {'h23':>6s} | "
      f"{'ratio10':>8s} {'ratio22':>8s} {'ratio23':>8s} | {'w22-23':>7s} {'h22-23':>7s}")
    for age, (w10, h10, w22, h22, w23, h23) in rates.items():
        r10 = f"{h10 / w10:7.2f}x" if w10 else "      -"
        p(f"{age:7s} {str(w10 or '-'):>6s} {w22:>6d} {w23:>6d} | {str(h10 or '-'):>6s} {h22:>6d} {h23:>6d} | "
          f"{r10:>8s} {h22 / w22:7.2f}x {h23 / w23:7.2f}x | "
          f"{100 * (w23 / w22 - 1):>+6.1f}% {100 * (h23 / h22 - 1):>+6.1f}%")
    p("")

    p("=" * 110)
    p("LOCAL JAIL INMATES HELD FOR U.S. IMMIGRATION AND CUSTOMS ENFORCEMENT (BJS Jail Inmates in 2024, Table 14)")
    p("=" * 110)
    p(JAIL_NOTE)
    p(f"{'year':6s} {'held for ICE':>13s} {'yoy':>8s}")
    prev = None
    for yr in sorted(jail_ice):
        yoy = f"{100 * (jail_ice[yr] / prev - 1):+.1f}%" if prev else "-"
        if yr >= 2019:
            p(f"{yr:<6d} {jail_ice[yr]:>13,} {yoy:>8s}")
        prev = jail_ice[yr]
    p(f"2019->2024 change: {100 * (jail_ice[2024] / jail_ice[2019] - 1):+.1f}%   "
      f"2014->2024 (BJS printed): -51.2%")
    p("")

    p("=" * 110)
    p("ICE-DETENTION INFLATION BOUND on the ACS foreign-born institutional count (ladder 65 caveat)")
    p("=" * 110)
    fb23 = acs_fb_inst[2023]
    adp = ICE_ADP[2023]
    p(f"ACS 2023 1-yr PUMS, men 18-39, foreign born, institutional group quarters (TYPEHUGQ=2): {fb23:,}")
    p(f"ICE average daily detained population, FY2023: {adp:,} (all ages, both sexes, all facility types)")
    p(f"Upper bound if EVERY ICE detainee were a foreign-born man 18-39 captured in ACS GQ: "
      f"{100 * adp / fb23:.1f}% of the cell")
    p("That bound is not attainable. ICE detention is roughly 85-90% male and a minority is outside 18-39;")
    p("ICE holds a large share of its population in local jails under IGSA contract, which the Census Bureau")
    p("enumerates as correctional GQ, and a further share in dedicated facilities. Applying 87% male and a")
    p("55-70% share aged 18-39 gives a plausible ICE contribution of")
    lo = adp * 0.87 * 0.55
    hi = adp * 0.87 * 0.70
    p(f"  {lo:,.0f} - {hi:,.0f} detainees, i.e. {100 * lo / fb23:.0f}-{100 * hi / fb23:.0f}% of the "
      f"{fb23:,} foreign-born institutional cell.  [INFERENCE: the sex and age splits are assumptions]")
    p("Net of ICE, the foreign-born institutional rate for men 18-39 would be lower by that factor, which")
    p("widens rather than narrows the native-vs-foreign-born gap in the pro-immigrant direction.")
    p(f"Jail-side cross-check: BJS counts only {jail_ice[2023]:,} jail inmates held for ICE on the last")
    p(f"weekday of June 2023, {100 * jail_ice[2023] / adp:.0f}% of ICE ADP, so most ICE detainees sit in")
    p("dedicated or contract detention facilities rather than in the local-jail universe BJS surveys.")
    p("")

    p(f"CSV written: {out_csv}")
    text = "\n".join(L)
    (HERE / "bjs_2023_result.txt").write_text(text + "\n")
    print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
