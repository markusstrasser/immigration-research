"""Build C_acquisitions/acquisitions.csv and prices.csv from curated rows.

Deflation: CPI-U (FRED CPIAUCSL, monthly, seasonally adjusted) annual averages.
Base year 2024.
"""
import csv, os, statistics

HERE = os.path.dirname(os.path.abspath(__file__))
CACHE = os.path.join(HERE, "_cache")

# ---- CPI-U annual averages ------------------------------------------------
from collections import defaultdict
cpi = defaultdict(list)
with open(os.path.join(CACHE, "cpi.csv")) as fh:
    for r in csv.DictReader(fh):
        v = r["CPIAUCSL"].strip()
        if v and v != ".":
            cpi[r["observation_date"][:4]].append(float(v))
CPI = {y: statistics.mean(v) for y, v in cpi.items()}
BASE = CPI["2024"]

def d2024(price, year):
    return price * BASE / CPI[str(year)]

# ---- curated acquisitions -------------------------------------------------
# fields: county_fips, county, agency, date, location, acres, price, land_only,
#         urban, price_basis, source, locator, quote
SBAPI = "https://webapi.legistar.com/v1/sanbernardino/matters?$filter=substringof('{}',MatterTitle)"

R = [
 # ---------------- Los Angeles ----------------
 dict(fips="06037", county="Los Angeles", agency="City of Los Angeles (GSD / Rec. & Parks)",
      date="2017-03-01", loc="Taylor Yard G2 parcel, Cypress Park / Elysian Valley, Los Angeles",
      acres=42.0, price=60_000_000, land_only="yes", urban="yes",
      basis="purchase price",
      source="https://tayloryardriverprojects.lacity.gov/about-taylor-yard-g2-projects",
      locator="'About Taylor Yard G2 Projects'; acreage from https://engineering.lacity.gov/about/divisions/projects-taylor-yard-100-acre-partnership",
      quote="\"The G2 Parcel was purchased by the City of Los Angeles in March 2017 for $60 million.\" / \"G2 is a Los Angeles River-adjacent, approximately 42-acre property\"",
      kind="urban"),
 dict(fips="06037", county="Los Angeles", agency="City of Long Beach",
      date="2019-06-11", loc="1400 W Wardlow Rd (Tanaka Park), Long Beach",
      acres=61926/43560, price=1_105_000, land_only="yes", urban="yes",
      basis="purchase price (not-to-exceed)",
      source="https://longbeach.legistar1.com/longbeach/attachments/d0ecf7a0-c7a2-40f4-b894-3a670fa4668a.pdf",
      locator="Long Beach City Council item 19-0555, staff report R-39, p.1-2",
      quote="\"for the purchase of certain real property at 1400 West Wardlow Road ... in an amount not to exceed $1,105,000\"; \"The Subject Property measures approximately 61,926 square feet\"; \"1.4 acres of land\"",
      kind="urban"),
 # ---------------- San Diego (City open data) ----------------
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2015-09-01", loc="San Ysidro Library site, San Diego", acres=1.55, price=830_000,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code Z733LB, year_acquired 2015, columns land_cost / file_acres / building_cost",
      quote="site_name=SAN YSIDRO LIBRARY; land_cost=830000.0; building_cost=0.0; file_acres=1.55", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2015-03-01", loc="Fairbrook Neighborhood Park, San Diego", acres=3.4, price=344_000,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code J633RS, year_acquired 2015",
      quote="site_name=Fairbrook Neighborhood Park; land_cost=344000.0; building_cost=0.0; file_acres=3.4; grantor=Ryland Homes of California", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2016-10-01", loc="Pacific Highlands Ranch Community Park, San Diego", acres=13.6, price=6_595_974,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code G314RS, year_acquired 2016",
      quote="site_name=Pacific Highlands Ranch Community Park; land_cost=6595974.0; building_cost=0.0; file_acres=13.6", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2017-03-01", loc="Fairmount Fire Station (future), San Diego", acres=1.28, price=325_000,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code R644FS, year_acquired 2017",
      quote="site_name=Fairmount Fire Station - Future; land_cost=325000.0; building_cost=0.0; file_acres=1.28", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2018-09-01", loc="Del Sur Neighborhood Park, San Diego", acres=5.04, price=196_400,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code E502RS, year_acquired 2018",
      quote="site_name=Del Sur Neighborhood Park; land_cost=196400.0; building_cost=0.0; file_acres=5.04; grantor=Black Mountain Ranch, LLC", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2021-12-01", loc="Dennery Ranch Neighborhood Park, San Diego", acres=9.21, price=7_732_183,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code Y720RS, year_acquired 2021",
      quote="site_name=DENNERY RANCH NEIGHBORHOOD PARK; land_cost=7732183.0; building_cost=0.0; file_acres=9.21", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2022-06-01", loc="Fire Station #49 (future), San Diego", acres=2.11, price=2_944_000,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code Y814FS, year_acquired 2022",
      quote="site_name=FIRE STATION #49 (FUTURE); land_cost=2944000.0; building_cost=0.0; file_acres=2.11", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2023-03-01", loc="McGonigle Canyon Neighborhood Park, San Diego", acres=6.15, price=3_289_411,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code G412RS, year_acquired 2023",
      quote="site_name=MCGONIGLE CANYON NEIGHBORHOOD PARK; land_cost=3289411.0; building_cost=0.0; file_acres=6.15", kind="urban"),
 dict(fips="06073", county="San Diego", agency="City of San Diego",
      date="2023-06-01", loc="San Carlos Branch Library site, San Diego", acres=0.52, price=150_000,
      land_only="yes", urban="yes", basis="land_cost",
      source="https://seshat.datasd.org/city_owned_properties/city_property_details_datasd.csv",
      locator="row site_code O701LB, year_acquired 2023",
      quote="site_name=SAN CARLOS BRANCH LIBRARY; land_cost=150000.0; building_cost=0.0; file_acres=0.52", kind="urban"),
 # ---------------- Santa Clara ----------------
 dict(fips="06085", county="Santa Clara", agency="City of San Jose",
      date="2020-02-25", loc="SW corner E Alma Ave & Senter Rd, San Jose", acres=4.95, price=8_500_000,
      land_only="yes", urban="yes", basis="purchase price",
      source="https://sanjose.legistar1.com/sanjose/attachments/edbf5624-8db4-49a5-a94c-93f226c8fe44.pdf",
      locator="San Jose City Council item 20-182, memorandum p.1",
      quote="\"for the purchase by the City of 4.95 acres located at the southwest corner of East Alma Avenue and Senter Road ... for a price of $8,500,000\"", kind="urban"),
 dict(fips="06085", county="Santa Clara", agency="City of San Jose",
      date="2021-05-24", loc="1138 Olinder Ct (NE corner Olinder Ct & Felipe Ave), San Jose", acres=1.1, price=3_135_300,
      land_only="yes", urban="yes", basis="purchase price",
      source="https://sanjose.legistar1.com/sanjose/attachments/04b228ac-4bd5-43d2-8fea-c2fc99bf3865.pdf",
      locator="San Jose City Council item 21-1329, memorandum",
      quote="\"purchase by the City of approximately 1.1 acres (47,916 square feet) of land located at the northeast corner of Olinder Court and Felipe Avenue ... for a price of $3,135,300\"", kind="urban"),
 # ---------------- San Bernardino: urban ----------------
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2015-10-06", loc="Sunhill Dr, Victorville", acres=2.49, price=115_000, land_only="yes", urban="yes",
      basis="purchase price", source=SBAPI.format("Sunhill"), locator="Board of Supervisors item HIST-243498 (2015-10-06)",
      quote="\"approximately 2.49 acres of vacant land ... for a purchase price of $115,000\"", kind="urban"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2016-05-24", loc="SE corner San Bernardino Ave & Carob Ave, unincorporated Fontana", acres=0.94,
      price=100_000, land_only="yes", urban="yes", basis="purchase price", source=SBAPI.format("Carob"),
      locator="Board of Supervisors item HIST-253847 (2016-05-24)",
      quote="\"approximately 0.94 acres of vacant land ... for a purchase price of $100,000\"", kind="urban"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2016-08-23", loc="Tokay St terminus, Victorville", acres=5.0, price=495_000, land_only="yes",
      urban="yes", basis="purchase price", source=SBAPI.format("Tokay"),
      locator="Board of Supervisors item HIST-255940 (2016-08-23)",
      quote="\"approximately five acres of vacant land at the terminus of Tokay Street in the City of Victorville ... for a purchase price of $495,000\"", kind="urban"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2016-08-23", loc="14677 Merrill Ave, unincorporated Fontana", acres=2.54, price=933_000,
      land_only="yes", urban="yes", basis="purchase price", source=SBAPI.format("Merrill"),
      locator="Board of Supervisors item HIST-255884 (2016-08-23)",
      quote="\"approximately 2.54 acres of vacant land, for a purchase price of $933,000\"", kind="urban"),
 # ---------------- San Bernardino: rural / open space ----------------
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2016-01-12", loc="Mojave Desert, adjacent National Trails Hwy", acres=80.0, price=40_000,
      land_only="yes", urban="no", basis="purchase price", source=SBAPI.format("quarry"),
      locator="Board of Supervisors item HIST-249293 (2016-01-12)",
      quote="\"an existing quarry of approximately 80 acres, for a purchase price of $40,000\"", kind="rural"),
 dict(fips="06071", county="San Bernardino", agency="County Service Area 70-CG",
      date="2016-04-19", loc="near Alder Rd, Cedar Glen (San Bernardino Mtns)", acres=1.05, price=35_000,
      land_only="yes", urban="no", basis="purchase price", source=SBAPI.format("Cedar Glen"),
      locator="Board of Supervisors item HIST-252961 (2016-04-19)",
      quote="\"approximately 1.05 acres cumulatively ... for the estimated total cost of $35,000\"", kind="rural"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County (Real Estate Services Dept.)",
      date="2016-12-20", loc="Twentynine Palms Hwy, Joshua Tree", acres=2.75, price=55_000, land_only="yes",
      urban="no", basis="purchase price", source=SBAPI.format("Joshua Tree"),
      locator="Board of Supervisors item HIST-258661 (2016-12-20)",
      quote="\"approximately 2.75 acres of vacant land cumulatively, for a combined purchase price of $55,000\"", kind="rural"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County Flood Control District",
      date="2015-12-01", loc="N side San Timoteo Creek, Redlands area", acres=11.49, price=300_000,
      land_only="yes", urban="no", basis="purchase price", source=SBAPI.format("San Timoteo"),
      locator="Board of Supervisors item HIST-246878 (2015-12-01)",
      quote="\"containing 11.49 acres of vacant land for the purchase price of $300,000\"", kind="rural"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County Flood Control District",
      date="2018-08-21", loc="E of Harvard Rd, N of Mojave Trail, Newberry Springs", acres=21.75, price=16_315,
      land_only="yes", urban="no", basis="purchase price", source=SBAPI.format("Newberry"),
      locator="Board of Supervisors item HIST-273526 (2018-08-21)",
      quote="\"approximately 21.75 acres of unimproved land ... for a purchase price of $16,315\"", kind="rural"),
 dict(fips="06071", county="San Bernardino", agency="San Bernardino County Flood Control District",
      date="2018-08-07", loc="Apple Valley (0.81 ac) + Oro Grande (90.95 ac)", acres=91.76, price=116_600,
      land_only="yes", urban="no", basis="purchase price", source=SBAPI.format("Apple Valley"),
      locator="Board of Supervisors item HIST-273212 (2018-08-07)",
      quote="\"approximately 0.81 acres ... in the Town of Apple Valley, and approximately 90.95 acres ... in the unincorporated area of Oro Grande, for the purchase price of $116,600\"", kind="rural"),
]

for r in R:
    r["year"] = int(r["date"][:4])
    r["ppa"] = r["price"] / r["acres"]
    r["ppa24"] = d2024(r["ppa"], r["year"])

# ---- acquisitions.csv -----------------------------------------------------
cols = ["county_fips","county","agency","date","location","acres","price","price_basis",
        "land_only","urban","price_per_acre_nominal","price_per_acre_2024","source","source_locator","quote"]
with open(os.path.join(HERE, "acquisitions.csv"), "w", newline="\n") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(cols)
    for r in sorted(R, key=lambda x: (x["fips"], x["date"])):
        w.writerow([r["fips"], r["county"], r["agency"], r["date"], r["loc"],
                    f"{r['acres']:.4f}", r["price"], r["basis"], r["land_only"], r["urban"],
                    f"{r['ppa']:.0f}", f"{r['ppa24']:.0f}", r["source"], r["locator"], r["quote"]])

# ---- prices.csv -----------------------------------------------------------
def q(vals, p):
    v = sorted(vals)
    if len(v) < 4:
        return v[0] if p < 0.5 else v[-1]
    qs = statistics.quantiles(v, n=4, method="inclusive")
    return qs[0] if p < 0.5 else qs[2]

counties = {"06037":"Los Angeles","06059":"Orange","06073":"San Diego",
            "06085":"Santa Clara","06071":"San Bernardino"}
METHOD = ("median of government land-acquisition prices per acre, land-only parcels, "
          "converted to 2024 dollars with CPI-U (FRED CPIAUCSL annual average); "
          "low/high = 25th/75th percentile (min/max when n<4)")

rows_out = []
for fips, cname in counties.items():
    sub = [r for r in R if r["fips"] == fips and r["kind"] == "urban"]
    if len(sub) < 2:
        continue
    vals = [r["ppa24"] for r in sub]
    yrs = sorted({r["year"] for r in sub})
    rows_out.append({
        "county_fips": fips, "county": cname,
        "price_per_acre_2024": f"{statistics.median(vals):.0f}",
        "low_per_acre_2024": f"{q(vals,0.25):.0f}",
        "high_per_acre_2024": f"{q(vals,0.75):.0f}",
        "n_obs": len(sub),
        "year_measured": f"{yrs[0]}-{yrs[-1]}" if len(yrs) > 1 else str(yrs[0]),
        "land_type": "urban vacant/land-only (park, civic, transit-site land)",
        "method": METHOD,
        "source": "see acquisitions.csv (government board records / open data)",
        "source_locator": "per-row in acquisitions.csv",
        "notes": "n is small; see RESULT.md limitations",
    })

pcols = ["county_fips","county","price_per_acre_2024","low_per_acre_2024","high_per_acre_2024",
         "n_obs","year_measured","land_type","method","source","source_locator","notes"]
with open(os.path.join(HERE, "prices.csv"), "w", newline="\n") as fh:
    w = csv.DictWriter(fh, fieldnames=pcols, lineterminator="\n")
    w.writeheader()
    for r in rows_out:
        w.writerow(r)

# ---- rural / open-space comparison ---------------------------------------
print("CPI 2024 =", round(BASE, 3))
for fips, cname in counties.items():
    sub = [r for r in R if r["fips"] == fips and r["kind"] == "rural"]
    if sub:
        v = [r["ppa24"] for r in sub]
        print(f"rural {cname}: n={len(v)} median=${statistics.median(v):,.0f}/ac "
              f"range ${min(v):,.0f}-${max(v):,.0f}")
for r in rows_out:
    print(r["county"], "n=", r["n_obs"], "median", r["price_per_acre_2024"],
          "IQR", r["low_per_acre_2024"], "-", r["high_per_acre_2024"])
