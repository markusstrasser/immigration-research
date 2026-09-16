#!/usr/bin/env python3
"""CPS 3-digit birth-country code -> ISO3, plus origin-country tertiary-completion
(25+) from World Bank SE.TER.CUAT.BA.ZS and Barro-Lee 2013 v2.2 MF 25+ (lhc)."""
import json, os, csv
HERE = os.path.dirname(os.path.abspath(__file__))

X = {
"057":"USA","060":"ASM","066":"GUM","069":"MNP","073":"PRI","078":"VIR",
"100":"ALB","102":"AUT","103":"BEL","104":"BGR","105":"CZE","106":"DNK","108":"FIN",
"109":"FRA","110":"DEU","116":"GRC","117":"HUN","118":"ISL","119":"IRL","120":"ITA",
"126":"NLD","127":"NOR","128":"POL","129":"PRT","130":"PRT","132":"ROU","134":"ESP",
"136":"SWE","137":"CHE","138":"GBR","139":"GBR","140":"GBR","142":"GBR",
"147":"SRB","148":"CZE","149":"SVK","150":"BIH","151":"HRV","152":"MKD","154":"SRB",
"155":"EST","156":"LVA","157":"LTU","158":"ARM","159":"AZE","160":"BLR","161":"GEO",
"162":"MDA","163":"RUS","164":"UKR","165":"RUS","166":None,"168":"MNE",
"200":"AFG","202":"BGD","203":"BTN","205":"MMR","206":"KHM","207":"CHN","209":"HKG",
"210":"IND","211":"IDN","212":"IRN","213":"IRQ","214":"ISR","215":"JPN","216":"JOR",
"217":"KOR","218":"KAZ","220":"KOR","222":"KWT","223":"LAO","224":"LBN","226":"MYS",
"228":"MNG","229":"NPL","231":"PAK","233":"PHL","235":"SAU","236":"SGP","238":"LKA",
"239":"SYR","240":"TWN","242":"THA","243":"TUR","245":"ARE","246":"UZB","247":"VNM",
"248":"YEM","249":None,
"300":"BMU","301":"CAN","303":"MEX","310":"BLZ","311":"CRI","312":"SLV","313":"GTM",
"314":"HND","315":"NIC","316":"PAN","321":"ATG","323":"BHS","324":"BRB","327":"CUB",
"328":"DMA","329":"DOM","330":"GRD","332":"HTI","333":"JAM","338":"KNA","339":"LCA",
"340":"VCT","341":"TTO","343":None,
"360":"ARG","361":"BOL","362":"BRA","363":"CHL","364":"COL","365":"ECU","368":"GUY",
"369":"PRY","370":"PER","372":"URY","373":"VEN","374":None,"399":None,
"400":"DZA","407":"CMR","408":"CPV","412":"COG","414":"EGY","416":"ETH","417":"ERI",
"421":"GHA","423":"GIN","425":"CIV","427":"KEN","429":"LBR","430":"LBY","436":"MAR",
"440":"NGA","444":"SEN","447":"SLE","448":"SOM","449":"ZAF","451":"SDN","453":"TZA",
"454":"TGO","457":"UGA","459":"COD","460":"ZMB","461":"ZWE","462":None,
"501":"AUS","508":"FJI","511":"MHL","512":"FSM","515":"NZL","523":"TON","527":"WSM",
"555":None,
}
# Preferred display name per ISO3 when several CPS codes collapse
PREF = {"GBR":"138","KOR":"217","PRT":"129","RUS":"163","CZE":"148","SRB":"154"}

REFUGEE = {"VNM","LAO","KHM","CUB","SOM","ETH","ERI","IRN","IRQ","AFG","BIH","RUS",
           "UKR","BLR","MDA","ARM","AZE","GEO","KAZ","UZB","MMR","SDN","SRB","HRV","MKD","MNE"}
MEXCAM = {"MEX","GTM","SLV","HND","NIC","CRI","PAN","BLZ"}


def main():
    names = json.load(open(os.path.join(HERE, "cps_country_codes.json")))
    wb = json.load(open(os.path.join(HERE, "wb_ter_ba.json")))[1]
    best = {}
    for r in wb:
        iso, yr, v = r.get("countryiso3code"), int(r["date"]), r["value"]
        if not iso or v is None or not (2000 <= yr <= 2022):
            continue
        if iso not in best or yr > best[iso][0]:
            best[iso] = (yr, float(v))
    bl = {}
    with open(os.path.join(HERE, "barrolee_MF2599.csv")) as f:
        for r in csv.DictReader(f):
            try:
                bl[(r["WBcode"], int(r["year"]))] = float(r["lhc"])
            except (ValueError, KeyError):
                pass

    out = os.path.join(HERE, "country_crosswalk.csv")
    with open(out, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["cps_code","cps_name","iso3","display_name","wb_ba_pct","wb_year",
                    "bl_ter_2010","bl_ter_1990","bl_ter_1980","origin_ba_pref",
                    "origin_ba_source","refugee_origin","mex_centam"])
        for code in sorted(names, key=lambda x: int(x)):
            iso = X.get(code)
            yr, v = best.get(iso, (None, None))
            b10, b90, b80 = (bl.get((iso, y)) for y in (2010, 1990, 1980))
            if v is not None:
                pref, src = v, f"WB {yr}"
            elif b10 is not None:
                pref, src = b10, "Barro-Lee 2010"
            else:
                pref, src = None, ""
            disp = names[PREF[iso]] if iso in PREF else names[code]
            w.writerow([code, names[code], iso or "", disp if iso else names[code],
                        "" if v is None else round(v, 2), yr or "",
                        "" if b10 is None else round(b10, 2),
                        "" if b90 is None else round(b90, 2),
                        "" if b80 is None else round(b80, 2),
                        "" if pref is None else round(pref, 2), src,
                        int(iso in REFUGEE) if iso else 0,
                        int(iso in MEXCAM) if iso else 0])
    print(f"WROTE {out}")


if __name__ == "__main__":
    main()
