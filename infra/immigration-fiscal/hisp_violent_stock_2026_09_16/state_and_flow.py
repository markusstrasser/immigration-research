"""(1) Texas coding-stability check: TDCJ on-hand population by race/ethnicity per 100k of state
population, FY2009 vs FY2021. TDCJ has coded Hispanic ethnicity separately for decades and does NOT
apply any survey adjustment, so its ethnic shares are a control for the BJS adjustment.
Source: TDCJ Statistical Report FY2009 p.6 and FY2021 p.6 ('TDCJ On Hand Demographic Highlights',
prison + state jail + SAFP). Population: ACS 1-year B03002 (total, NH white alone, Hispanic), state 48.
(2) Stock-flow model for the Hispanic violent stock."""
TDCJ = {  # year: (total, black, white, hispanic, other, violent_total)
 2009: (155076, 57127, 47971, 49197, 781, 78783),
 2021: (117876, 38547, 39735, 38914, 680, 73956)}
POP48 = {2009: (11546095, 9149688), 2021: (11627221, 11857387)}  # (NH white, Hispanic)

print("TEXAS (TDCJ on-hand, all offences; TDCJ publishes no race x offence cross-tab)")
print(f"{'':10} {'total':>9} {'white':>9} {'hisp':>9} {'hisp%':>7} {'W/100k':>8} {'H/100k':>8} {'H/W':>6} {'viol%':>7}")
for y in (2009, 2021):
    t, b, w, h, o, v = TDCJ[y]; wp, hp = POP48[y]
    print(f"FY{y:<8} {t:>9,} {w:>9,} {h:>9,} {100*h/t:>6.1f}% {1e5*w/wp:>8.1f} {1e5*h/hp:>8.1f} {(h/hp)/(w/wp):>6.2f} {100*v/t:>6.1f}%")
w0,h0 = 1e5*TDCJ[2009][2]/POP48[2009][0], 1e5*TDCJ[2009][3]/POP48[2009][1]
w1,h1 = 1e5*TDCJ[2021][2]/POP48[2021][0], 1e5*TDCJ[2021][3]/POP48[2021][1]
print(f"  change 2009->2021: NH white {100*(w1/w0-1):+.1f}%   Hispanic {100*(h1/h0-1):+.1f}%")
print(f"  Texas Hispanic SHARE of prisoners 2009->2021: {100*TDCJ[2009][3]/TDCJ[2009][0]:.1f}% -> {100*TDCJ[2021][3]/TDCJ[2021][0]:.1f}%  ({100*((TDCJ[2021][3]/TDCJ[2021][0])/(TDCJ[2009][3]/TDCJ[2009][0])-1):+.1f}% relative)")
print(f"  BJS national Hispanic share, memo basis 2009 (p10) -> 2021: 15.5% -> 22.0%  (+41.5% relative)")
print(f"  BJS national Hispanic share, consistent basis 2009 (p11) -> 2021: 21.1% -> 22.0%  (+4.4% relative)")

print("\nSTOCK-FLOW")
# BJS Prisoners in 2012 (p12tar9112) app. tables: new court commitments to state prison by race and offence
NCC = {2001: (63992, .341), 2006: (77274, .322), 2011: (69728, .357)}   # Hispanic: (admissions, violent share)
NCCW = {2001: (133442, .277), 2006: (162084, .239), 2011: (146054, .253)}  # NH white
for y in (2001, 2006, 2011):
    a, s = NCC[y]; aw, sw = NCCW[y]
    print(f"  {y}: Hispanic violent new court commitments {a*s:>8,.0f}   NH white {aw*sw:>8,.0f}   ratio {a*s/(aw*sw):.2f}")
# BJS Time Served in State Prison, 2016 (tssp16, table 1): mean time served, initial release
T = {"violent":4.7,"murder":15.0,"rape/sexual assault":6.2,"robbery":4.7,"assault":2.5,
     "property":21/12,"drug":22/12,"public order":20/12}
print(f"  mean time served, 2016 initial releases (yrs): " + ", ".join(f"{k} {v:.1f}" for k,v in T.items()))
# Hispanic state stock by offence, consistent SISCF-2004 basis 2009 (p11 app.T16) vs SPI basis 2021 (p22st T17)
S09 = dict(violent=159800, property=43100, drug=49400, public_order=34000)
S21 = dict(violent=160100, property=19000, drug=22600, public_order=21900)
print("\n  Hispanic state-prison stock by offence, consistent basis")
for k in S09:
    print(f"    {k:<13} {S09[k]:>8,} -> {S21[k]:>8,}  {100*(S21[k]/S09[k]-1):+6.1f}%")
nv09 = sum(v for k,v in S09.items() if k!="violent"); nv21 = sum(v for k,v in S21.items() if k!="violent")
print(f"    non-violent   {nv09:>8,} -> {nv21:>8,}  {100*(nv21/nv09-1):+6.1f}%")
print(f"    violent share {100*S09['violent']/(S09['violent']+nv09):>7.1f}% -> {100*S21['violent']/(S21['violent']+nv21):>6.1f}%")
# Counterfactual: if violent stock had fallen at the same rate as the non-violent stock
cf = S09["violent"] * (nv21/nv09)
print(f"\n  If the Hispanic violent stock had drained like the non-violent stock: {cf:,.0f} (actual {S21['violent']:,})")
print(f"  Excess attributable to long violent sentences / slow stock turnover: {S21['violent']-cf:+,.0f}")
