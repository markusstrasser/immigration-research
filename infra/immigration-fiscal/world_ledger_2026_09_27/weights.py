"""Brief parts C and D, case-independent: Hendren's inverse-optimum weights g(y) digitized from his Figure 6,
the marginal costs of public funds, and the income positions of the group and of Mexico's residents that the
Hendren and log-income columns need.

g(y): Hendren (NBER w20351, April 2020) publishes the schedule only as Figure 6, a line over ordinary-income
quantiles. This script renders PDF page 21 at 200 dpi and reads the curve's pixel centre in every column,
calibrated on the figure's own tick marks (g = .6, .8, 1, 1.2; quantiles 0 to 100). Accuracy is about +-0.005 in g
at 200 dpi; the text's anchors (1.15 at the bottom, 0.65 at the top, crossing 1 near the 60th quantile) are gates.

Income positions (CPS ASEC 2025 through the distribution lane's loader): each person's SPM resources over the
SPM equivalence scale, ranked on other residents' distribution, the scale of that lane's channel_by_percentile.
Log-income weights are y_ref / max(y, floor) with y_ref the other residents' mean and floor their 5th
percentile, the distribution lane's normalization. Mexico (ENIGH 2024): household current income over the square
root of household size, in PPP dollars. Log weights use income per head on both sides (see income_positions).
Outputs (derived/): hendren_g.csv, income_positions.csv, log_weights_by_percentile.csv, weights_meta.json.
--basis row4 counts the group on the account's row-4 persons (population_basis.py) and writes only
income_positions_row4.csv: row 4 moves no other resident, so the other files do not depend on the basis. --basis
lineage (main case v5's 42.75M: row 4, with the G3+ records carrying the added people) writes only
income_positions_lineage.csv, for the same reason.
"""
import argparse
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd
from PIL import Image

from population_basis import BASES, lineage, reweight, suffixed

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
DERIVED = HERE / "derived"
PDF = HERE / "_cache/reads/hendren_nber_w20351.pdf"
PDF_SHA = "b62487ff6341673c9257eb13b92698b94e19e7ec6898c87c95d707181403e8d0"
# Marginal cost of public funds. 1.16: Hendren & Sprung-Keyser's Top Tax 2013 row (WTP 1.00, cost 0.86, MVPF
# 1.16; reads/hendren_sprung_keyser_2020.md). 1.25: OMB Circular A-94 (1992) excess burden of 25 cents per
# dollar (reads/mcpf_sources.md). 1.5: Heckman & Smith (1998), 50 cents per dollar (reads/mcpf_sources.md).
LAMBDA = {"1.0": 1.0, "1.16": 1.16, "1.25": 1.25, "1.5": 1.5}
# Mexico's residents: Hendren's weights are for the 2012 US tax schedule and "there is also no reason to expect
# weights identified in one setting or country to readily translate to another" (his section 8.4). Assumed: the
# bottom of the US schedule, since every Mexican household in PPP dollars sits there.
G_MEXICO_ASSUMED = 1.15


def gate(name, ok, **detail):
    if not ok:
        raise SystemExit(f"[BLOCKED] gate {name} failed: {detail}")


def sha256(path):
    import hashlib
    h = hashlib.sha256()
    h.update(Path(path).read_bytes())
    return h.hexdigest()


def digitize_g():
    gate("hendren_pdf_hash", sha256(PDF) == PDF_SHA)
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.run(["pdftoppm", "-f", "21", "-l", "21", "-r", "200", "-png", str(PDF), f"{tmp}/p"], check=True)
        png = next(Path(tmp).glob("p*.png"))
        im = np.asarray(Image.open(png).convert("RGB")).astype(int)
    r, g, b = im[..., 0], im[..., 1], im[..., 2]
    dark = (r < 120) & (g < 120) & (b < 120)
    # Tick marks: y ticks left of the vertical axis, x ticks below the horizontal axis.
    axis_x = int(np.argmax(dark.sum(axis=0)))
    axis_y = int(np.argmax(dark.sum(axis=1)))
    left = dark[:, axis_x - 10:axis_x - 1].sum(axis=1)
    yt = [y for y in range(axis_y - 650, axis_y) if left[y] >= 6]
    below = dark[axis_y + 1:axis_y + 13, :].sum(axis=0)
    xt = [x for x in range(axis_x, im.shape[1]) if below[x] >= 6]

    def centres(pos):
        groups, cur = [], [pos[0]]
        for p in pos[1:]:
            if p - cur[-1] <= 2:
                cur.append(p)
            else:
                groups.append(np.mean(cur))
                cur = [p]
        groups.append(np.mean(cur))
        return groups

    yt, xt = centres(yt), centres(xt)
    gate("fig6_ticks", len(yt) == 4 and len(xt) == 6, y=yt, x=xt)
    gy = np.polyfit(yt, [1.2, 1.0, 0.8, 0.6], 1)      # pixel row -> g
    qx = np.polyfit(xt, [0, 20, 40, 60, 80, 100], 1)  # pixel column -> quantile
    blue = (b > 90) & (r < 80) & (g < 110) & (b - r > 40)
    cols = np.nonzero(blue.any(axis=0))[0]
    q = np.polyval(qx, cols)
    val = np.array([np.polyval(gy, np.nonzero(blue[:, c])[0].mean()) for c in cols])
    grid = np.arange(1, 101)
    gq = np.interp(grid, q, val)
    out = pd.DataFrame({"quantile": grid, "g": np.round(gq, 4)})
    gate("fig6_bottom_near_1_15", 1.10 <= out.g[out["quantile"] <= 10].max() <= 1.16, top=out.g[:10].max())
    cross = out["quantile"][out.g < 1.0].min()
    gate("fig6_crosses_1_near_q60", 50 <= cross <= 62, cross=cross)
    gate("fig6_top_min_near_0_6", 0.54 <= out.g.min() <= 0.62, low=out.g.min())
    return out, dict(y_ticks_px=yt, x_ticks_px=xt, crosses_one_at_quantile=int(cross), g_min=float(out.g.min()),
                     g_q1=float(out.g.iloc[0]), g_q100=float(out.g.iloc[-1]))


def g_at(quantile, gtab):
    return np.interp(np.clip(quantile, 1, 100), gtab["quantile"], gtab["g"])


def income_positions(gtab, basis="cps"):
    """Each party's position on two US scales: 'money' (household money income over the square root of household
    size, the scale Mexico's incomes can be put on) and 'spm' (SPM resources over the SPM equivalence scale). Both
    rank persons on other residents' distribution, as the distribution lane's channel_by_percentile does."""
    spec = importlib.util.spec_from_file_location("dist_base", FISCAL / "distribution_weights_2026_09_23/distribute.py")
    B = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(B)
    d = B.load_cps()
    if basis != "cps":
        d = reweight(d, B.PATHS["cps"], gate, basis)
    other, tgt = d.other.to_numpy(), d.target.to_numpy()
    w = d.pw.to_numpy(float)
    usb = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    mexpar = d.PEFNTVTY.eq(303).to_numpy() | d.PEMNTVTY.eq(303).to_numpy()
    gen = np.select([tgt & ~usb & d.PENATVTY.eq(303).to_numpy(), tgt & usb & mexpar, tgt & usb & ~mexpar,
                     tgt, other], ["G1", "G2", "G3+", "group_other_foreign_born", "other_residents"], "")
    if basis == "lineage":
        # The lineage factor scales exactly this script's G3+ records and moves no other resident, so the scale the
        # parties are ranked on is row 4's.
        g3 = gen == "G3+"
        r4 = d.pw_row4.to_numpy(float)
        f = 1.0 + lineage()["added"] / r4[g3].sum()
        gate("lineage_scales_exactly_g3plus", np.array_equal(w[g3], r4[g3] * f) and np.array_equal(w[~g3], r4[~g3]),
             factor=f)
    rows, ref = [], {}
    # Log-income weights must use the income each person's consumption comes from: household money income per
    # head (money_pc). A household's relative change is its loss over its income, i.e. a per-person loss over
    # income per head; dividing a per-person loss by income per square-root adult would understate it by the
    # square root of household size. Bins are the distribution lane's own (position_rank on y_money among other
    # residents, 100 bins), so they align with its channel_by_percentile rows.
    ypc = np.maximum(d.money_pc.to_numpy(float), 0.0)
    ref_pc = float(np.average(ypc[other], weights=w[other]))
    floor_pc = wquant(ypc[other], w[other], 0.05)
    p_other = B.position_rank(d.y_money.to_numpy(float)[other], w[other])
    pbin = B.bins(p_other, 100) + 1
    inv = 1.0 / np.maximum(ypc[other], floor_pc)
    lw = pd.DataFrame({"percentile": pbin, "w": w[other], "wi": w[other] * inv,
                       "wy": w[other] * d.y_money.to_numpy(float)[other]}).groupby("percentile").sum()
    lw = pd.DataFrame({"percentile": lw.index, "persons_m": lw.w / 1e6, "ybar_money": lw.wy / lw.w,
                       "log_weight_pc": ref_pc * lw.wi / lw.w})
    ref["per_capita"] = dict(y_ref_other_mean=ref_pc, floor_other_p5=floor_pc)
    for measure in ("money", "spm"):
        y = d[f"y_{measure}"].to_numpy(float)
        o = np.argsort(y[other], kind="mergesort")
        ys, cw = y[other][o], np.cumsum(w[other][o]) / w[other].sum()
        pct = np.clip(np.ceil(np.interp(y, ys, cw) * 100), 1, 100)   # percentile on other residents' scale
        y_ref = float(np.average(y[other], weights=w[other]))
        floor = float(ys[np.searchsorted(cw, 0.05)])
        logw = y_ref / np.maximum(y, floor)
        gp = g_at(pct, gtab)
        ref[measure] = dict(y_ref_other_mean=y_ref, floor_other_p5=floor,
                            y_ref_other_median=wquant(y[other], w[other], 0.5))
        for k in ["G1", "G2", "G3+", "group_other_foreign_born", "other_residents"]:
            m = gen == k
            if not m.any():
                continue
            rows.append(dict(measure=measure, party=k, persons_m=w[m].sum() / 1e6,
                             mean_y=np.average(y[m], weights=w[m]), median_y=wquant(y[m], w[m], 0.5),
                             mean_percentile=np.average(pct[m], weights=w[m]), mean_g=np.average(gp[m], weights=w[m]),
                             mean_log_weight=np.average(logw[m], weights=w[m]),
                             mean_log_weight_pc=np.average(ref_pc / np.maximum(ypc[m], floor_pc), weights=w[m]),
                             mean_y_pc=np.average(ypc[m], weights=w[m]),
                             share_below_floor=w[m & (y < floor)].sum() / w[m].sum()))
    return pd.DataFrame(rows), ref, lw


def wquant(x, w, q):
    o = np.argsort(x, kind="mergesort")
    cw = np.cumsum(w[o]) / w.sum()
    return float(x[o][np.searchsorted(cw, q)])


def mexico_incomes():
    """Mexico's residents on the US 'money' scale: household current income less imputed rent, over the square root
    of household size, PPP dollars; all residents and remittance-receiving households (ENIGH 2024)."""
    c = pd.read_csv(HERE / "_cache/mexico/enigh/concentradohogar.csv",
                    usecols=["ing_cor", "estim_alqu", "remesas", "tot_integ", "factor"])
    rates = json.load(open(HERE / "_cache/mexico/wdi_PA.NUS.PPP.json"))[1]
    ppp = [r["value"] for r in rates if r["country"]["id"] == "MX" and r["date"] == "2024"][0]
    # Current income less imputed rent (the US money-income scale has none), annual, per head (the log weights'
    # unit) and per square-root adult (reported for comparison with the US money scale).
    y = (c.ing_cor - c.estim_alqu) * 4 / c.tot_integ / ppp
    y_sqrt = (c.ing_cor - c.estim_alqu) * 4 / np.sqrt(c.tot_integ) / ppp
    wp = c.factor * c.tot_integ                   # persons
    rec = c.remesas > 0
    out = dict(ppp=ppp, persons_m=float(wp.sum() / 1e6), unit="per head",
               median_y_sqrt=wquant(y_sqrt.to_numpy(), wp.to_numpy(), 0.5),
               mean_y=float(np.average(y, weights=wp)), median_y=wquant(y.to_numpy(), wp.to_numpy(), 0.5),
               p90_y=wquant(y.to_numpy(), wp.to_numpy(), 0.9),
               remittance_households_persons_m=float(wp[rec].sum() / 1e6),
               remittance_households_mean_y=float(np.average(y[rec], weights=wp[rec])),
               remittance_households_median_y=wquant(y[rec].to_numpy(), wp[rec].to_numpy(), 0.5),
               top_decile_mean_y=float(np.average(y[y >= wquant(y.to_numpy(), wp.to_numpy(), 0.9)],
                                                  weights=wp[y >= wquant(y.to_numpy(), wp.to_numpy(), 0.9)])))
    return out


def main(basis="cps"):
    DERIVED.mkdir(exist_ok=True)
    gtab, gmeta = digitize_g()
    if basis != "cps":
        pos, _, _ = income_positions(gtab, basis)
        pos.to_csv(suffixed(DERIVED / "income_positions.csv", basis), index=False, lineterminator="\n",
                   float_format="%.6g")
        print(pos.round(3).to_string(), file=sys.stderr)
        return
    gtab.to_csv(DERIVED / "hendren_g.csv", index=False, lineterminator="\n")
    pos, ref, lw = income_positions(gtab)
    pos.to_csv(DERIVED / "income_positions.csv", index=False, lineterminator="\n", float_format="%.6g")
    lw.to_csv(DERIVED / "log_weights_by_percentile.csv", index=False, lineterminator="\n", float_format="%.6g")
    mx = mexico_incomes()
    meta = dict(hendren_fig6=gmeta, lambda_values=LAMBDA, g_mexico_assumed=G_MEXICO_ASSUMED, us_reference=ref,
                mexico=mx)
    json.dump(meta, open(DERIVED / "weights_meta.json", "w"), indent=1, sort_keys=True)
    print(json.dumps(meta, indent=1), file=sys.stderr)
    print(pos.round(3).to_string(), file=sys.stderr)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--basis", default="cps", choices=BASES)
    main(ap.parse_args().basis)
