"""Outcome construction. Every outcome is oriented so the sign is stated in LABEL."""
import numpy as np, pandas as pd
from norms_lib import CON, TOL_SPK, TOL_COL, TOL_LIB

# tolerant-response codes: spk* 1=allowed, col* 4=allowed to teach, lib* 2=not remove
TOL_CODE = {**{v: 1 for v in TOL_SPK}, **{v: 4 for v in TOL_COL}, **{v: 2 for v in TOL_LIB}}
TOL_VALID = {**{v: [1, 2] for v in TOL_SPK}, **{v: [4, 5] for v in TOL_COL},
             **{v: [1, 2] for v in TOL_LIB}}
TARGETS = ["ath", "rac", "com", "mil", "homo", "mslm"]
CLASSIC = ["ath", "rac", "com", "mil", "homo"]          # 15-item Stouffer scale
CORE = ["ath", "rac", "com"]                             # 9 items, fielded through 2024

IMPORT4 = ["amcit", "amancstr", "amchrstn", "amenglsh", "amfeel", "amgovt",
           "ambornin", "amlived"]                        # 1 very important .. 4 not at all
AGREE5 = ["amcitizn", "amshamed", "amcult", "amownway", "ethnofit", "ethadapt",
          "immlimit"]                                    # 1 strongly agree .. 5 strongly disagree
POLICE = ["polabuse", "polmurdr", "polescap", "polattak"]


def build(d):
    """Returns (DataFrame of outcomes, dict item -> human label with sign)."""
    o, L = {}, {}
    num = lambda c: pd.to_numeric(d[c], errors="coerce")

    # ---- 1. institutional confidence -------------------------------------
    for c in CON:
        v = num(c).where(num(c).isin([1, 2, 3]))
        o[f"{c}_great"] = v.eq(1).where(v.notna()).astype(float)
        o[f"{c}_mean"] = (4 - v)
        L[f"{c}_great"] = f"{c}: share 'a great deal' of confidence"
        L[f"{c}_mean"] = f"{c}: 3-point confidence mean (3=a great deal, 1=hardly any)"
    conf_mean = pd.concat([(4 - num(c).where(num(c).isin([1, 2, 3]))) for c in CON], axis=1)
    o["con_index_all13"] = conf_mean.mean(axis=1).where(conf_mean.notna().all(axis=1))
    L["con_index_all13"] = "mean of all 13 confidence items (higher = more confidence)"
    o["con_within_sd"] = conf_mean.std(axis=1, ddof=0).where(conf_mean.notna().all(axis=1))
    L["con_within_sd"] = ("INSTRUMENT CHECK: within-respondent SD across the 13 confidence "
                          "items; low = straightlining the battery")
    gov3 = pd.concat([(4 - num(c).where(num(c).isin([1, 2, 3]))) for c in
                      ["confed", "conlegis", "conjudge"]], axis=1)
    o["con_index_gov3"] = gov3.mean(axis=1).where(gov3.notna().all(axis=1))
    L["con_index_gov3"] = "mean of confidence in the executive, Congress and the Supreme Court"

    # ---- 2. Stouffer civil-liberties tolerance ---------------------------
    tol = {}
    for v, code in TOL_CODE.items():
        x = num(v).where(num(v).isin(TOL_VALID[v]))
        tol[v] = x.eq(code).where(x.notna()).astype(float)
        o[f"tol_{v}"] = tol[v]
        L[f"tol_{v}"] = f"{v}: share giving the tolerant answer"
    for name, tg in [("classic15", CLASSIC), ("core9", CORE), ("mslm3", ["mslm"])]:
        cols = [p + t for t in tg for p in ("spk", "col", "lib")]
        m = pd.concat([tol[c] for c in cols], axis=1)
        o[f"tolscale_{name}"] = m.sum(axis=1).where(m.notna().all(axis=1))
        L[f"tolscale_{name}"] = (f"summed tolerance scale, {len(cols)} items "
                                 f"({', '.join(tg)}); higher = more tolerant")

    # ---- 3. rule of law, policing, civic values --------------------------
    ob = num("obey").where(num("obey").between(1, 5))
    o["obey_top2"] = ob.isin([1, 2]).where(ob.notna()).astype(float)
    o["obey_rank"] = (6 - ob)
    L["obey_top2"] = "obedience ranked 1st or 2nd most important child quality"
    L["obey_rank"] = "obedience rank reversed (5 = most important child quality)"
    ct = num("courts").where(num("courts").isin([1, 2, 3]))
    o["courts_too_harsh"] = ct.eq(1).where(ct.notna()).astype(float)
    o["courts_not_harsh_enough"] = ct.eq(2).where(ct.notna()).astype(float)
    L["courts_too_harsh"] = "courts deal with criminals 'too harshly'"
    L["courts_not_harsh_enough"] = "courts 'not harshly enough'"
    for v, lab in [("cappun", "favours the death penalty for murder"),
                   ("gunlaw", "favours police permits to buy a gun"),
                   ("grass", "marijuana should be legal")]:
        x = num(v).where(num(v).isin([1, 2]))
        o[f"{v}_favor"] = x.eq(1).where(x.notna()).astype(float)
        L[f"{v}_favor"] = lab
    ph = num("polhitok").where(num("polhitok").isin([1, 2]))
    o["polhitok_yes"] = ph.eq(1).where(ph.notna()).astype(float)
    L["polhitok_yes"] = "ever approves of a policeman striking an adult male citizen"
    for v in POLICE:
        x = num(v).where(num(v).isin([1, 2]))
        o[f"{v}_yes"] = x.eq(1).where(x.notna()).astype(float)
        L[f"{v}_yes"] = f"{v}: approves police force in this scenario"
    pm = pd.concat([o[f"{v}_yes"] for v in POLICE], axis=1)
    o["police_force_index"] = pm.mean(axis=1).where(pm.notna().all(axis=1))
    L["police_force_index"] = "share of the 4 police-force scenarios approved"
    # INSTRUMENT CHECK, not an attitude: how far apart a respondent places the
    # weakest justification (vulgar language) and the strongest (attacking the officer).
    both = o["polattak_yes"].notna() & o["polabuse_yes"].notna()
    o["police_spread"] = (o["polattak_yes"] - o["polabuse_yes"]).where(both)
    L["police_spread"] = ("INSTRUMENT CHECK: approves force against an attacker minus "
                          "approves force after vulgar language; low = undifferentiated answers")

    # ---- 4. economic role of government (continuity with ladder 87) ------
    o["redist"] = (8 - num("eqwlth").where(num("eqwlth").between(1, 7)))
    L["redist"] = "government should reduce income differences (1-7, higher = more)"
    o["helppoor_r"] = (6 - num("helppoor").where(num("helppoor").between(1, 5)))
    L["helppoor_r"] = "government should improve living standards (1-5, higher = more)"
    o["helpnot_r"] = (6 - num("helpnot").where(num("helpnot").between(1, 5)))
    L["helpnot_r"] = "government should do more (1-5, higher = more)"
    nf = num("natfare").where(num("natfare").isin([1, 2, 3]))
    o["welfare_toolittle"] = nf.eq(1).where(nf.notna()).astype(float)
    L["welfare_toolittle"] = "spending on welfare is 'too little'"

    # ---- 5. national identity and pluralism (ISSP modules) ---------------
    for v in IMPORT4:
        x = num(v).where(num(v).between(1, 4))
        o[f"{v}_imp"] = (5 - x)
        o[f"{v}_very"] = x.eq(1).where(x.notna()).astype(float)
        L[f"{v}_imp"] = f"{v}: importance for being truly American (1-4, higher = more important)"
        L[f"{v}_very"] = f"{v}: share saying 'very important'"
    for v in AGREE5:
        x = num(v).where(num(v).between(1, 5))
        o[f"{v}_agree"] = (6 - x)
        L[f"{v}_agree"] = f"{v}: agreement (1-5, higher = more agreement with the item as worded)"
    ia = num("immassim").where(num("immassim").isin([1, 2, 3]))
    o["immassim_giveup"] = ia.eq(3).where(ia.notna()).astype(float)
    o["immassim_retain_only"] = ia.eq(1).where(ia.notna()).astype(float)
    L["immassim_giveup"] = "immigrants should give up their culture of origin and adopt American culture"
    L["immassim_retain_only"] = "immigrants should retain their culture of origin and not adopt American culture"
    ic = num("immcult").where(num("immcult").between(1, 4))
    o["immcult_agree"] = (5 - ic)
    L["immcult_agree"] = "immigrants undermine American culture (1-4, higher = more agreement)"
    return pd.DataFrame(o, index=d.index), L


FAMILY = {}
for c in CON:
    FAMILY[f"{c}_great"] = FAMILY[f"{c}_mean"] = "A1 institutional confidence"
FAMILY["con_index_all13"] = FAMILY["con_index_gov3"] = "A1 institutional confidence"
FAMILY["con_within_sd"] = FAMILY["police_spread"] = "A6 instrument checks"
for v in TOL_CODE:
    FAMILY[f"tol_{v}"] = "A2 civil liberties"
for n in ["classic15", "core9", "mslm3"]:
    FAMILY[f"tolscale_{n}"] = "A2 civil liberties"
for k in ["obey_top2", "obey_rank", "courts_too_harsh", "courts_not_harsh_enough",
          "cappun_favor", "gunlaw_favor", "grass_favor", "polhitok_yes",
          "police_force_index"] + [f"{v}_yes" for v in POLICE]:
    FAMILY[k] = "A3 rule of law and policing"
for k in ["redist", "helppoor_r", "helpnot_r", "welfare_toolittle"]:
    FAMILY[k] = "A4 role of government"
for v in IMPORT4:
    FAMILY[f"{v}_imp"] = FAMILY[f"{v}_very"] = "A5 national identity"
for v in AGREE5:
    FAMILY[f"{v}_agree"] = "A5 national identity"
for k in ["immassim_giveup", "immassim_retain_only", "immcult_agree"]:
    FAMILY[k] = "A5 national identity"
