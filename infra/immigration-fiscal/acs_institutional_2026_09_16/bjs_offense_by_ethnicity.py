"""BJS state-prisoner offence composition, non-Hispanic white vs Hispanic, 2009 (Prisoners in 2010, App. Table 16b)
and 2021 (Prisoners in 2022 Statistical Tables, Table 17); plus male imprisonment rates by age (App. Table 15, 2010; Table 13, 2022).
Counts transcribed from the BJS PDFs (pdftotext this session). Resident populations: Census Vintage estimates, July 1 (rounded)."""
import csv, pathlib
HERE = pathlib.Path(__file__).parent
counts = {  # (year, group): {offence: count}
    # 2009 rows below are the ORIGINAL Prisoners in 2010 basis (NIS 2008-09). NOT comparable with 2021; see 2009r rows (Prisoners in 2011 App. Table 8 restatement, SISCF-2004 basis) which are.
    ("2009r", "white"):   dict(total=467290, violent=231500, murder=46900, sexual=33300+44800, robbery=40700, assault=43300, property=111000, burglary=54300, mvt=6500, fraud=16000, drug=69200, public_order=52000),
    ("2009r", "hispanic"): dict(total=287568, violent=159800, murder=38300, sexual=8900+24600, robbery=37600, assault=37500, property=43100, burglary=22600, mvt=6600, fraud=2900, drug=49400, public_order=34000),
    ("2009", "white"):    dict(total=532000, violent=265600, murder=55700, sexual=36300+58600, robbery=45300, assault=46600, property=132000, burglary=63400, mvt=8500, fraud=19600, drug=73900, public_order=54400),
    ("2009", "hispanic"): dict(total=212100, violent=117800, murder=32300, sexual=6800+15200, robbery=26600, assault=28000, property=34400, burglary=16400, mvt=6100, fraud=2400, drug=41400, public_order=16000),
    ("2021", "white"):    dict(total=321700, violent=176400, murder=36900, sexual=63600, robbery=20400, assault=38000, property=57600, burglary=29200, mvt=2700, fraud=5800, drug=48200, drug_possession=15800, drug_other=32400, public_order=36800, weapons=8300, dui=6500),
    ("2021", "hispanic"): dict(total=224300, violent=160100, murder=31900, sexual=42800, robbery=26600, assault=47100, property=19000, burglary=11700, mvt=1700, fraud=1200, drug=22600, drug_possession=6100, drug_other=16500, public_order=21900, weapons=7700, dui=4500),
}
pop = {("2009", "white"): 199.9e6, ("2009", "hispanic"): 48.4e6, ("2009r", "white"): 199.9e6, ("2009r", "hispanic"): 48.4e6, ("2021", "white"): 191.7e6, ("2021", "hispanic"): 62.6e6}
rows = []
for base in ("2009", "2009r"):
  for g in ("white", "hispanic"):
      a, b = counts[(base, g)], counts[("2021", g)]
      for off in ("total", "violent", "murder", "sexual", "robbery", "assault", "property", "burglary", "mvt", "fraud", "drug", "public_order"):
          r09, r21 = 1e5 * a[off] / pop[(base, g)], 1e5 * b[off] / pop[("2021", g)]
          rows.append(dict(basis=base, group=g, offence=off, n2009=a[off], n2021=b[off], count_change_pct=round(100 * (b[off] / a[off] - 1), 1),
                           per100k_2009=round(r09, 1), per100k_2021=round(r21, 1), per100k_change_pct=round(100 * (r21 / r09 - 1), 1),
                           share2009_pct=round(100 * a[off] / a["total"], 1), share2021_pct=round(100 * b[off] / b["total"], 1)))
with open(HERE / "bjs_offense_by_ethnicity.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
for r in rows:
    print(f"{r['group']:8s} {r['offence']:13s} n {r['n2009']:>7,} -> {r['n2021']:>7,} ({r['count_change_pct']:+6.1f}%)  per100k {r['per100k_2009']:6.1f} -> {r['per100k_2021']:6.1f} ({r['per100k_change_pct']:+6.1f}%)  share {r['share2009_pct']:5.1f} -> {r['share2021_pct']:5.1f}")
print("\nMale imprisonment rate per 100k (state+federal), 2010 -> 2022, white / Hispanic / ratio")
ages = {"18-19": (149, 30, 563, 85), "20-24": (638, 229, 1908, 663), "25-29": (980, 514, 2707, 1462), "30-34": (1061, 732, 2808, 1774), "35-39": (995, 813, 2486, 1747), "all": (459, 337, 1258, 794)}
for a, (w10, w22, h10, h22) in ages.items():
    print(f"{a:6s} white {w10:5d}->{w22:4d} ({100*(w22/w10-1):+5.0f}%)  Hispanic {h10:5d}->{h22:5d} ({100*(h22/h10-1):+5.0f}%)  ratio {h10/w10:4.2f}x -> {h22/w22:4.2f}x")
