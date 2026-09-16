"""Year-by-year sentenced state prisoners by race/Hispanic origin and violent-offence count,
transcribed from BJS 'Prisoners in YYYY' PDFs (pdftotext -layout, this session; PDFs in ./pdf, text in ./txt).
Each row records the REPORT the number came from, because BJS restated the same reference years
on different race/Hispanic-origin estimation bases."""
import csv, pathlib
HERE = pathlib.Path(__file__).parent

# (ref_year, report, basis, page, white_total, black_total, hisp_total, all_total, white_viol, black_viol, hisp_viol)
ROWS = [
 (2008, "p10 App.T16a", "NIS 2008-09 / pre-2010 basis", 27, 532000, 584800, 209000, 1365400, 264200, 315500, 113400),
 (2009, "p10 App.T16b", "NIS 2008-09 / pre-2010 basis", 28, 532000, 582100, 212100, 1365800, 265600, 319700, 117800),
 (2008, "p11 App.T15",  "SISCF 2004 ratio (restated)",  28, 469076, 528008, 280716, 1365409, 232700, 280200, 152700),
 (2009, "p11 App.T16",  "SISCF 2004 ratio (restated)",  29, 467290, 525677, 287568, 1365688, 231500, 284600, 159800),
 (2010, "p11 T9",       "SISCF 2004 ratio",              9, 468528, 518763, 289429, 1362028, 231800, 286400, 164200),
 (2012, "p13 T14",      "SISCF 2004 ratio",             15, 462600, 498100, 271700, 1314900, 228100, 290300, 162900),
 (2013, "p14 App.T4",   "SISCF 2004 ratio",             29, 468600, 497000, 274200, 1325305, 223900, 282100, 162300),
 (2014, "p15 App.T5",   "SISCF 2004 ratio",             30, 451100, 456600, 261000, 1316409, 210400, 263800, 152900),
 (2015, "p16 T13",      "SISCF 2004 ratio",             18, 403600, 429000, 278600, 1298159, 190100, 252300, 167700),
 (2016, "p17 T13",      "SPI 2016 ratio",               21, 401100, 419700, 278400, 1288466, 190900, 252400, 168100),
 (2017, "p18 T14",      "SPI 2016 ratio",               21, 394800, 409600, 274300, 1273674, 188700, 250100, 166800),
 (2018, "p19 T14",      "SPI 2016 ratio",               22, 394800, 409600, 274300, 1249700, 190800, 253600, 168900),
 (2019, "p20st T17",    "SPI 2016 ratio",               29, 386700, 399000, 266500, 1221288, 192600, 255000, 176000),
 (2020, "p21st T17",    "SPI 2016 ratio",               31, 327300, 345500, 226800, 1043705, 178600, 234500, 179500),
 (2021, "p22st T17",    "SPI 2016 ratio",               29, 321700, 332000, 224300, 1021288, 176400, 227000, 160100),
]
# Census resident population, July 1 (Vintage): NH white alone, Hispanic (any race), millions
POP = {2008:(200.0,47.0),2009:(199.9,48.4),2010:(196.8,50.5),2012:(197.2,52.9),2013:(197.2,53.7),
       2014:(197.2,54.5),2015:(197.5,55.3),2016:(197.4,56.5),2017:(197.3,57.4),2018:(197.0,58.5),
       2019:(196.8,59.4),2020:(191.7,61.8),2021:(191.7,62.6)}
out=[]
for ry,rep,basis,pg,wt,bt,ht,at,wv,bv,hv in ROWS:
    w_pop,h_pop = POP[ry]
    out.append(dict(ref_year=ry, report=rep, basis=basis, page=pg,
        white_total=wt, hisp_total=ht, all_total=at, white_violent=wv, hisp_violent=hv,
        hisp_share_pct=round(100*ht/at,1),
        white_viol_per100k=round(1e5*wv/(w_pop*1e6),1), hisp_viol_per100k=round(1e5*hv/(h_pop*1e6),1),
        hisp_viol_share_of_hisp_pct=round(100*hv/ht,1)))
with open(HERE/"national_series.csv","w",newline="") as f:
    w=csv.DictWriter(f,fieldnames=list(out[0])); w.writeheader(); w.writerows(out)
hdr=f"{'yr':>5} {'report':<13} {'basis':<28} {'W tot':>8} {'H tot':>8} {'W viol':>8} {'H viol':>8} {'W/100k':>7} {'H/100k':>7} {'H viol%':>7}"
print(hdr); print("-"*len(hdr))
for r in out:
    print(f"{r['ref_year']:>5} {r['report']:<13} {r['basis']:<28} {r['white_total']:>8,} {r['hisp_total']:>8,} "
          f"{r['white_violent']:>8,} {r['hisp_violent']:>8,} {r['white_viol_per100k']:>7.1f} {r['hisp_viol_per100k']:>7.1f} {r['hisp_viol_share_of_hisp_pct']:>7.1f}")

def cmp(a_yr,a_rep,b_yr,b_rep,label):
    A=[r for r in out if r['ref_year']==a_yr and r['report'].startswith(a_rep)][0]
    B=[r for r in out if r['ref_year']==b_yr and r['report'].startswith(b_rep)][0]
    print(f"\n{label}")
    for k,lab in (("hisp_violent","Hispanic violent count"),("white_violent","White violent count"),
                  ("hisp_viol_per100k","Hispanic violent per 100k"),("white_viol_per100k","White violent per 100k")):
        print(f"  {lab:<28} {A[k]:>10,} -> {B[k]:>10,}   {100*(B[k]/A[k]-1):+6.1f}%")
cmp(2009,"p10",2021,"p22st","A. MEMO COMPARISON (2009 old basis -> 2021 SPI basis)")
cmp(2009,"p11",2021,"p22st","B. CONSISTENT-BASIS COMPARISON (2009 restated -> 2021)")
cmp(2009,"p10",2009,"p11","C. PURE METHOD EFFECT (same reference date 31 Dec 2009, two BJS estimates)")
