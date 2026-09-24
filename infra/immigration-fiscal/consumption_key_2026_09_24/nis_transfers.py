"""NIS-2003 Round 1 adults: money given to relatives/friends in the last 12 months (Section I).

Mexico-born = CISCOBINSMO 135 (DS0002 P.I. codebook; same code as parent_status_2026_09_23).
Weight NISWGTSAMP1 (DS0002). Amounts: DS0016 '<item>A[_k]PPP' ("AMOUNT … in US current prices,
PPP adj"), annualized with the DS0015 periodicity item '<item>D[_k]' (1 per week x52, 2 every two
weeks x26, 3 per month x12, 4 per year x1, 5 one time only x1; 97 other and missing -> x1, counted).
Two definitions:
  any_give     gave to a non-coresident spouse, child, parent, parent-in-law, sibling,
               sibling-in-law, other relative or friend (I2, I6, I8, I13, I17, I21, I27, I31/I31A);
               location of recipients is not asked for the named-kin items -> upper bound on remittances
  abroad_expl  gave to other relatives (I31C) or friends (I39M) "when they were living outside the
               United States"; amounts I32 + I41 -> lower bound (excludes kin abroad)
Transfers are asked of "you or your spouse" (text fill when married), so the income base is own
wage and salary G7APPP (DS0012) plus, where present, the spouse wage item G16PPP in DS0012.
"""
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
ZIP = HERE.parents[2] / "sources/immigration-fiscal/data/external/icpsr_nis_2003/ICPSR_38031-V3.zip"
MEXICO = 135
N_ADULT = 8573
HANDOUT_MEXICO_WEIGHTED = 0.175  # NIS adult handout Table 3 (used as gate in parent_status_2026_09_23)
PERIOD = {1: 52, 2: 26, 3: 12, 4: 1, 5: 1}
GIVE_ITEMS = ["I3", "I7", "I10", "I14", "I18", "I22", "I28", "I32", "I34", "I41", "I43"]


def tsv(ds: str, want) -> pd.DataFrame:
    name = f"ICPSR_38031/DS{ds}/38031-{ds}-Data.tsv"
    with zipfile.ZipFile(ZIP) as z, z.open(name) as fh:
        header = fh.readline().decode("latin-1").rstrip("\n").split("\t")
    cols = [c for c in header if c == "PU_ID" or (want(c) if callable(want) else c in want)]
    with zipfile.ZipFile(ZIP) as z, z.open(name) as fh:
        df = pd.read_csv(fh, sep="\t", usecols=cols, dtype=str, encoding="latin-1")
    for c in cols:
        if c != "PU_ID":
            df[c] = pd.to_numeric(df[c].str.strip(), errors="coerce")
    return df


d2 = tsv("0002", ["CISCOBINSMO", "NISWGTSAMP1", "CISADJUST"])
flag_items = ["I1", "I2", "I6", "I8", "I13", "I17", "I21", "I27", "I31", "I31A", "I31C", "I39M"]
per_re = re.compile(r"^(%s)D(_\d+)?$" % "|".join(GIVE_ITEMS))
d15 = tsv("0015", lambda c: c in flag_items or bool(per_re.match(c)))
amt_re = re.compile(r"^(%s)A(_\d+)?PPP$" % "|".join(GIVE_ITEMS))
d16 = tsv("0016", lambda c: bool(amt_re.match(c)))
d12 = tsv("0012", ["G7APPP", "G16PPP"])
d = d2.merge(d15, on="PU_ID", how="left").merge(d16, on="PU_ID", how="left").merge(d12, on="PU_ID", how="left")
if len(d) != N_ADULT:
    sys.exit(f"[BLOCKED] adult n {len(d)} != {N_ADULT}")
mx = d["CISCOBINSMO"] == MEXICO
w = d["NISWGTSAMP1"].astype(float)
mx_share = float(w[mx].sum() / w.sum())
print(f"gate: adults {len(d)}; Mexico-born n {int(mx.sum())}; weighted share {mx_share:.4f} (handout {HANDOUT_MEXICO_WEIGHTED})")
if abs(mx_share - HANDOUT_MEXICO_WEIGHTED) > 0.005:
    sys.exit("[BLOCKED] Mexico weighted share does not match the handout")

fams = sorted({amt_re.match(c).group(1) for c in d16.columns if amt_re.match(c)})
print("amount families found:", fams, "| G16PPP in DS0012:", "G16PPP" in d.columns)

annual = pd.DataFrame(index=d.index)
other_period = 0
for c in d16.columns:
    m = amt_re.match(c)
    if not m:
        continue
    item, k = m.group(1), m.group(2) or ""
    pcol = f"{item}D{k}"
    a = d[c].where(d[c] >= 0)
    if pcol in d:
        f = d[pcol].map(PERIOD)
        other_period += int((a.notna() & f.isna()).sum())
        f = f.fillna(1)
    else:
        f = pd.Series(1.0, index=d.index)
    annual[c] = a * f
abroad_cols = [c for c in annual if amt_re.match(c).group(1) in ("I32", "I41")]
amt_all = annual.sum(axis=1, min_count=1).fillna(0)
amt_abroad = annual[abroad_cols].sum(axis=1, min_count=1).fillna(0)
print(f"amounts with 'other'/missing periodicity treated as annual: {other_period}")

give = ((d["I2"] == 1) | (d["I6"] == 1) | (d["I8"] == 1) | d["I13"].isin([1, 3]) | d["I17"].isin([1, 3])
        | d["I21"].isin([1, 3]) | d["I27"].isin([1, 3]) | (d["I31"].isin([1, 3]) & d["I31A"].isin([1, 2, 3])))
abroad = d["I31C"].isin([1, 3]) | d["I39M"].isin([1, 3])
parents = d["I13"].isin([1, 3])
# I1 is asked only on the married path (1,385 valid); the parent item I13 (GIVE/RECEIVE/BOTH/NEITHER)
# is the first item asked of everyone who reached Section I (5,558 valid, 3,015 blank), so it
# defines the answering universe; blanks are treated as missing at random within group [INFERENCE].
answered = d["I13"].isin([1, 2, 3, 4])
amt_parents = annual[[c for c in annual if amt_re.match(c).group(1) == "I14"]].sum(axis=1, min_count=1).fillna(0)
print("I13 valid by group: Mexico-born", int((answered & mx).sum()), "of", int(mx.sum()),
      "| others", int((answered & ~mx).sum()), "of", int((~mx).sum()))
inc = d["G7APPP"].where(d["G7APPP"] >= 0).fillna(0)
if "G16PPP" in d:
    inc = inc + d["G16PPP"].where(d["G16PPP"] >= 0).fillna(0)


def wmed(x, wt):
    o = np.argsort(x)
    x, wt = np.asarray(x)[o], np.asarray(wt)[o]
    c = np.cumsum(wt)
    return float(x[np.searchsorted(c, c[-1] / 2)])


def summarize(mask, label):
    s = mask & answered
    ww = w[s]
    out = {"group": label, "n_answered": int(s.sum())}
    neff = ww.sum() ** 2 / (ww ** 2).sum()
    for nm, flag, amt in (("any_give", give, amt_all), ("abroad_explicit", abroad, amt_abroad),
                          ("parents_any_location", parents, amt_parents)):
        p = float((ww * flag[s]).sum() / ww.sum())
        out[f"{nm}_rate"] = round(100 * p, 2)
        out[f"{nm}_se_kish"] = round(100 * np.sqrt(p * (1 - p) / neff), 2)
        if amt is not None:
            snd = s & flag & (amt > 0)
            out[f"{nm}_n_pos_amount"] = int(snd.sum())
            out[f"{nm}_mean_usd"] = round(float(np.average(amt[snd], weights=w[snd])), 0) if snd.any() else None
            out[f"{nm}_median_usd"] = round(wmed(amt[snd], w[snd]), 0) if snd.any() else None
            pos = snd & (inc > 0)
            out[f"{nm}_share_of_couple_wages_ratio_of_means"] = (
                round(100 * float((w[pos] * amt[pos]).sum() / (w[pos] * inc[pos]).sum()), 1) if pos.any() else None)
            out[f"{nm}_share_median"] = round(100 * wmed((amt[pos] / inc[pos]).to_numpy(), w[pos]), 1) if pos.any() else None
            allpos = s & (inc > 0)
            out[f"{nm}_all_adults_amount_over_wages"] = round(
                100 * float((w[allpos] * amt[allpos]).sum() / (w[allpos] * inc[allpos]).sum()), 2)
    return out


rows = [summarize(mx, "Mexico-born"), summarize(~mx, "all other NIS adults"),
        summarize(mx & (d["CISADJUST"] == 1), "Mexico-born, adjustees"),
        summarize(mx & (d["CISADJUST"] == 0), "Mexico-born, new arrivals")]
res = pd.DataFrame(rows)
res.to_csv(HERE / "derived" / "nis_transfers.csv", index=False, lineterminator="\n")
pd.set_option("display.width", 250)
print(res.T.to_string())
