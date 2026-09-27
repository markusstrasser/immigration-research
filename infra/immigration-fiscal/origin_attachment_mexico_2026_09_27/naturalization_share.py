"""Share of naturalization-eligible adults who have naturalized, by country of birth.

naturalized adults (ACS 2024 1-year PUMS, CIT=4, AGEP>=18, weight PWGTP; sources/census_pums2024_cit_adults_*.json)
divided by naturalized + OHSS LPRs eligible to naturalize (revised Jan 2024, Table 2b,
https://ohss.dhs.gov/topics/immigration/lawful-permanent-residents/population-estimates/fy-25-lpr-pop-estimates).
Pew's convention (naturalized / (naturalized + eligible LPRs)). Unauthorized residents are outside both terms.
"""
import csv, json, os
H = os.path.dirname(os.path.abspath(__file__))
OHSS_ELIG_2024 = {"303": ("Mexico", 2_320_000), "207": ("China", 540_000), "329": ("Dominican Republic", 390_000),
                  "327": ("Cuba", 370_000), "233": ("Philippines", 330_000), "210": ("India", 270_000),
                  "312": ("El Salvador", 220_000), "247": ("Vietnam", 210_000), "217": ("Korea, South", 200_000),
                  "allforeignborn": ("All countries", 8_600_000)}
rows = []
for code, (name, elig) in OHSS_ELIG_2024.items():
    hdr, vals = json.load(open(f"{H}/sources/census_pums2024_cit_adults_{'pobp'+code if code.isdigit() else code}.json"))
    d = {list(h.values())[0]: v for h, v in zip(hdr, vals)}
    nat, non, abroad_us = d["4"], d["5"], d["3"]
    rows.append([name, code, nat, non, elig, round(nat / (nat + elig), 3), round(elig / non, 3)])
rows.sort(key=lambda r: r[5])
with open(f"{H}/derived/naturalization_share_2024.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["country", "pobp", "acs2024_naturalized_adults", "acs2024_noncitizen_adults", "ohss_eligible_lpr_jan2024",
                "naturalized_share_of_eligible", "eligible_lpr_share_of_acs_noncitizens"])
    w.writerows(rows)
for r in rows: print(r)
# Mexico by year of entry (adults): citizenship shares
out = []
for rng in ["2015_2024", "2005_2014", "1995_2004", "1900_1994"]:
    hdr, vals = json.load(open(f"{H}/sources/census_pums2024_cit_mex_adults_yoep{rng}.json"))
    d = {list(h.values())[0]: v for h, v in zip(hdr, vals)}
    tot = d["4"] + d["5"] + d["3"]
    out.append([rng.replace("_", "-"), d["4"], d["5"], d["3"], round(d["4"] / tot, 3)])
with open(f"{H}/derived/mexico_citizenship_by_entry_2024.csv", "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["year_of_entry", "naturalized", "noncitizen", "born_abroad_us_parents", "naturalized_share_of_all"])
    w.writerows(out)
for r in out: print(r)
