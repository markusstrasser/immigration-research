#!/usr/bin/env python3
"""Render RESULT.md from scripts/RESULT_template.md, substituting every arm D
number straight out of derived/ so that no figure in the memo is hand-copied.

Run last. Idempotent: the template is the source, RESULT.md is the product.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent.parent
DER = LANE / "derived"
TPL = LANE / "scripts" / "RESULT_template.md"
OUT = LANE / "RESULT.md"


def main() -> None:
    el = pd.read_csv(DER / "arm_d_elasticity.csv")
    summ = json.loads((DER / "arm_d_summary.json").read_text())
    spec = summ["primary_spec"]
    dec = pd.read_csv(DER / "arm_d_share_deciles.csv")
    pred = pd.read_csv(DER / "arm_d_predicted_density.csv")
    cov = json.loads((DER / "arm_d_coverage_fit.json").read_text())
    osm = json.loads((DER / "osm_cuisine_coverage.json").read_text())
    aw = pd.read_csv(DER / "awards_shares.csv")
    cls = pd.read_csv(DER / "awards_classified.csv")

    def row(sp, dep, quad=False):
        m = el[(el.spec == sp) & (el.dep == dep) & (el.quadratic == quad)]
        if m.empty:
            raise SystemExit(f"missing spec {sp}/{dep}/quad={quad}")
        return m.iloc[0]

    prim = row(spec, "mexican")
    name = row(f"{spec}_name_classifier", "mexican_by_name")
    tagged = row(f"{spec}_tagged_offset", "mexican")
    quad = row(spec, "mexican", True)

    d0, d9 = dec.iloc[0], dec.iloc[-1]
    ratio = d9.mex_per_100k_pooled / d0.mex_per_100k_pooled

    dens = ["| Mexican-origin share | predicted Mexican restaurants per 100,000 "
            "| share of the maximum |", "|---|---|---|"]
    mx = pred.pred_mex_per_100k.max()
    for _, r in pred.iterrows():
        dens.append(f"| {r.mexican_share:.1%} | {r.pred_mex_per_100k:.1f} "
                    f"| {r.pred_mex_per_100k / mx:.0%} |")

    ALL_STATES = set("AL AK AZ AR CA CO CT DE DC FL GA HI ID IL IN IA KS KY LA "
                     "ME MD MA MI MN MS MO MT NE NV NH NJ NM NY NC ND OH OK OR "
                     "PA RI SC SD TN TX UT VT VA WA WV WI WY".split())
    fetched = set(osm["cuisine_tagged_share_by_state"])
    missing = sorted(ALL_STATES - fetched)
    n_states = len(fetched)
    cov_line = (
        f"Coverage of this run: {n_states} states fetched, "
        f"{osm['osm_points']:,} restaurant and fast-food features, "
        f"{osm['points_inside_cbsa']:,} of them inside a CBSA, "
        f"{osm['national_tagged_share']:.0%} carrying a cuisine tag. "
        f"The estimates below use the {summ['cbsas_fully_covered']} CBSAs of "
        f"{summ['cbsas_total']} whose every state was fetched"
        + ("; a metro whose state was only partly fetched would show a "
           "spuriously low restaurant count, and since the fetched states "
           "skew towards high Mexican-origin shares that contaminates the "
           "all-CBSA fit upward, to "
           f"{summ['all_cbsas_elasticity']:.3f} (SE "
           f"{summ['all_cbsas_se']:.3f}); it is reported in the table file "
           "but is not the estimate to read."
           if spec != "all_cbsas" else "."))

    # the share at which the fitted curve first reaches 75% and 90% of its
    # own maximum: read off the grid rather than asserted in prose
    def share_at(frac: float):
        hit = pred[pred.pred_mex_per_100k >= frac * mx]
        return hit.mexican_share.iloc[0] if not hit.empty else None

    s75, s90 = share_at(0.75), share_at(0.90)
    have_any = dec.iloc[0].cbsas_with_any_mexican
    verdict = (
        f"Mexican-cuisine variety per head is nearly flat in a metro's "
        f"Mexican-origin share (elasticity {prim.elasticity_log_share:.2f}, SE "
        f"{prim.se:.2f}, {abs(prim.z_vs_one):.0f} SE below one), with three "
        f"quarters of the fitted maximum density reached by a {s75:.0%} local "
        f"share and {have_any:.0%} of the lowest-decile metros (mean "
        f"{dec.iloc[0].mexican_share_mean:.1%} Mexican-origin) already carrying "
        f"at least one Mexican restaurant. The saturation hypothesis is "
        f"SUPPORTED at the local margin and NOT IDENTIFIED for the national "
        f"counterfactual the operator posed")
    flat_line = (
        f"Three quarters of the fitted maximum density is reached by a {s75:.0%} "
        f"local share and 90% by {s90:.0%}, and the curve is flat above that.")

    # ---- arm B ----
    def awrow(scope, group):
        m = aw[(aw.scope == scope) & (aw.group == group)]
        if m.empty:
            raise SystemExit(f"missing awards row {scope}/{group}")
        return m.iloc[0]

    b_rows, b_repl = [], {}
    for scope, lab in (("all_winners", "all winners"),
                       ("us_citizens_only", "US citizens only")):
        for per in ("period 1990-2014", "period 2015-2025"):
            r = awrow(scope, per)
            b_rows.append(
                f"| {lab} | {per.split()[1]} | {int(r.winner_years):,} "
                f"| {r.hispanic_share:.2%} | {r.hispanic_share_upper_bound:.2%} "
                f"| {r.hispanic_documented_share:.2%} "
                f"| {r.hispanic_share_thr50:.2%} / {r.hispanic_share_thr90:.2%} "
                f"| {r.surname_unmatched_share:.1%} |")
            tag = ("ALL" if scope == "all_winners" else "CIT") + (
                "EARLY" if "1990" in per else "LATE")
            b_repl[f"AWSHARE_{tag}"] = f"{r.hispanic_share:.2%}"
            b_repl[f"AWUPPER_{tag}"] = f"{r.hispanic_share_upper_bound:.2%}"

    cls["period"] = np.where(cls["year_n"] < 2015, "early", "late")
    noncit = cls[~cls["us_citizen"].astype(bool)]
    nc = noncit.groupby("period")["hispanic_any"].agg(["size", "sum", "mean"])
    all_unmatched = awrow("all_winners", "ALL").surname_unmatched_share
    all_doc = awrow("all_winners", "ALL").hispanic_documented_share
    bm = pd.read_csv(DER / "education_benchmarks.csv")
    ba_late = bm[bm.year == 2023]["hispanic_share_ba_plus"].iloc[0]
    ba_early = bm[bm.year == 2010]["hispanic_share_ba_plus"].iloc[0]
    ad_late = bm[bm.year == 2024]["hispanic_share_25plus"].iloc[0]
    ad_early = bm[bm.year == 2010]["hispanic_share_25plus"].iloc[0]
    cit_e = awrow("us_citizens_only", "period 1990-2014").hispanic_share
    cit_l = awrow("us_citizens_only", "period 2015-2025").hispanic_share
    mex_late = awrow("us_citizens_only",
                     "period 2015-2025").mexican_documented_share

    # how much of the CBSA Mexican-origin population the fetched states cover,
    # and how the covered and uncovered metros compare on group share
    panel_cov = pd.read_csv(DER / "cbsa_restaurant_panel.csv")
    panel_cov = panel_cov[panel_cov.pop_b03001 > 0]
    inc = panel_cov[panel_cov.all_states_fetched == True]      # noqa: E712
    exc = panel_cov[panel_cov.all_states_fetched != True]      # noqa: E712
    mex_cov = inc.mexican_origin.sum() / panel_cov.mexican_origin.sum()
    sh_in = inc.mexican_origin.sum() / inc.pop_b03001.sum()
    sh_out = (exc.mexican_origin.sum() / exc.pop_b03001.sum()
              if len(exc) else float("nan"))
    coverage_caveat = (
        "Coverage is complete: every state was fetched."
        if not missing else
        f"{len(missing)} states were not fetched in this run "
        f"({', '.join(missing)}), so their metros are excluded from the primary "
        f"estimate rather than entered with partial counts. The covered metros "
        f"hold {mex_cov:.0%} of the Mexican-origin population living in CBSAs, "
        f"and are {sh_in:.1%} Mexican-origin against {sh_out:.1%} in the "
        f"excluded metros [CALCULATION]: the excluded set is the lower-share "
        f"half, so including it would add low-share metros that already carry "
        f"Mexican restaurants and would if anything flatten the curve further.")

    b = prim.elasticity_log_share
    big = None
    for cand in ("pop_250k_plus",):
        m = el[(el.spec == cand) & (el.dep == "mexican") & (~el.quadratic)]
        if not m.empty:
            big = m.iloc[0]
            bign = el[(el.spec == f"{cand}_name_classifier")
                      & (~el.quadratic)].iloc[0]
    if big is not None:
        big_sentence = (
            f"Restricting to the {int(big.n)} fully-covered CBSAs above 250,000 "
            f"residents, where every metro carries a double-digit tagged-restaurant "
            f"count and {'none' if big.dep_zero_cbsas == 0 else str(int(big.dep_zero_cbsas))} "
            f"{'has' if big.dep_zero_cbsas == 0 else 'have'} zero Mexican restaurants, "
            f"the elasticity is {big.elasticity_log_share:.3f} (SE {big.se:.3f}), "
            f"still {abs(big.z_vs_one):.1f} SE below one, with the name classifier at "
            f"{bign.elasticity_log_share:.3f} [CALCULATION]. The flatness is not a "
            f"small-count artefact of micropolitan areas.")
    else:
        big_sentence = ("The large-metro restriction is not reported: too few "
                        "fully-covered CBSAs above 250,000 residents.")

    repl = {
        "ELAST_Z_ABS": f"{abs(prim.z_vs_one):.0f}",
        "ELAST_Z0_ABS": f"{abs(prim.z_vs_zero):.0f}",
        "DOUBLING_PCT": f"{(2 ** b - 1) * 100:.0f}%",
        "TENFOLD_PCT": f"{(10 ** b - 1) * 100:.0f}%",
        "BIGMETRO_SENTENCE": big_sentence,
        "COVERAGE_CAVEAT": coverage_caveat,
        "FLATTEN_SENTENCE": flat_line,
        "AWARDS_TABLE_ROWS": "\n".join(b_rows),
        "AW_UNMATCHED_ALL": f"{all_unmatched:.0%}",
        "AW_DOCUMENTED_ALL": f"{all_doc:.1%}",
        "AW_NONCIT_EARLY": f"{nc.loc['early', 'mean']:.2%}",
        "AW_NONCIT_LATE": f"{nc.loc['late', 'mean']:.2%}",
        "AW_NONCIT_NE": f"{int(nc.loc['early', 'sum'])}/{int(nc.loc['early', 'size'])}",
        "AW_NONCIT_NL": f"{int(nc.loc['late', 'sum'])}/{int(nc.loc['late', 'size'])}",
        "AW_RATIO_BA_EARLY": f"{cit_e / ba_early:.2f}",
        "AW_RATIO_BA_LATE": f"{cit_l / ba_late:.2f}",
        "AW_RATIO_AD_EARLY": f"{cit_e / ad_early:.2f}",
        "AW_RATIO_AD_LATE": f"{cit_l / ad_late:.2f}",
        "AW_BA_EARLY": f"{ba_early:.1%}",
        "AW_BA_LATE": f"{ba_late:.1%}",
        "AW_AD_EARLY": f"{ad_early:.1%}",
        "AW_AD_LATE": f"{ad_late:.1%}",
        "AW_MEXDOC_LATE": f"{mex_late:.2%}",
        **b_repl,
        "ARM_D_VERDICT_PLACEHOLDER": verdict,
        "OSM_COVERAGE_LINE": cov_line,
        "ELAST_PRIMARY": f"{prim.elasticity_log_share:.3f}",
        "ELAST_PRIMARY_SE": f"{prim.se:.3f}",
        "ELAST_PRIMARY_Z": f"{prim.z_vs_one:.1f}",
        "ELAST_NAME": f"{name.elasticity_log_share:.3f}",
        "ELAST_NAME_SE": f"{name.se:.3f}",
        "ELAST_NAME_Z": f"{name.z_vs_one:.1f}",
        "ELAST_TAGGED": f"{tagged.elasticity_log_share:.3f}",
        "ELAST_TAGGED_SE": f"{tagged.se:.3f}",
        "ELAST_TAGGED_Z": f"{tagged.z_vs_one:.1f}",
        "PLACEBO_ALL": f"{row(f'{spec}_placebo', 'all').elasticity_log_share:+.3f}",
        "PLACEBO_CHINESE": f"{row(f'{spec}_placebo', 'chinese').elasticity_log_share:+.3f}",
        "PLACEBO_ITALIAN": f"{row(f'{spec}_placebo', 'italian').elasticity_log_share:+.3f}",
        "PLACEBO_AMERICAN": f"{row(f'{spec}_placebo', 'american').elasticity_log_share:+.3f}",
        "DENSITY_TABLE": "\n".join(dens),
        "DECILE0_SHARE": f"{d0.mexican_share_mean:.1%}",
        "DECILE9_SHARE": f"{d9.mexican_share_mean:.0%}",
        "DECILE0_ANY": f"{d0.cbsas_with_any_mexican:.0%}",
        "SHARE_RATIO": f"{d9.mexican_share_mean / d0.mexican_share_mean:.0f}",
        "DECILE0_DENSITY": f"{d0.mex_per_100k_pooled:.1f}",
        "DECILE9_DENSITY": f"{d9.mex_per_100k_pooled:.1f}",
        "DECILE_RATIO": f"{ratio:.1f}",
        "QUAD_COEF": f"{quad.quad_coef:+.3f}",
        "QUAD_SE": f"{quad.quad_se:.3f}",
        "COVERAGE_COEF": f"{cov['osm_coverage']['coef_log_share']:+.3f}",
        "COVERAGE_T": f"{cov['osm_coverage']['t']:.2f}",
        "COVERAGE_MEDIAN": f"{cov['osm_coverage']['median_coverage']:.2f}",
        "TAGCOV_COEF": f"{cov['tagged_coverage']['coef_log_share']:+.3f}",
        "TAGCOV_T": f"{cov['tagged_coverage']['t']:.2f}",
    }
    pan = pd.read_csv(DER / "cbsa_restaurant_panel.csv")
    pan = pan[(pan.get("all_states_fetched", True) == True)  # noqa: E712
              & (pan.pop_b03001 > 0)].copy()
    pan["share"] = pan.mexican_origin / pan.pop_b03001
    pan["per100k"] = pan.mexican / pan.pop_b03001 * 1e5
    # the two extremes are tiny metros with single-digit restaurant counts, so
    # the illustration uses the LARGEST metro in the bottom and top decile of
    # Mexican-origin share instead, where the counts can carry a comparison
    q10, q90 = pan.share.quantile(0.1), pan.share.quantile(0.9)
    lo = pan[pan.share <= q10].nlargest(1, "pop_b03001").iloc[0]
    hi = pan[pan.share >= q90].nlargest(1, "pop_b03001").iloc[0]

    def short(n):
        return str(n).replace(" Metro Area", "").replace(" Micro Area", "")

    repl["CONCRETE_SENTENCE"] = (
        f"Concretely, comparing the largest metro in the bottom decile of "
        f"Mexican-origin share with the largest in the top decile: {short(lo.NAME)} "
        f"is {lo.share:.1%} Mexican-origin and carries {lo.per100k:.1f} Mexican "
        f"restaurants per 100,000 residents on {int(lo.mexican)} tagged "
        f"restaurants; {short(hi.NAME)} is {hi.share:.0%} Mexican-origin and "
        f"carries {hi.per100k:.1f} on {int(hi.mexican)} [CALCULATION]. A "
        f"{hi.share / lo.share:.0f}-fold difference in group share, and "
        f"{hi.per100k / lo.per100k:.1f} times the density.")

    text = TPL.read_text()
    # longest key first: ELAST_PRIMARY is a prefix of ELAST_PRIMARY_SE, and
    # substituting the short one first would leave "0.109_SE" in the table
    for k in sorted(repl, key=len, reverse=True):
        text = text.replace(k, repl[k])
    left = [k for k in repl if k in text]
    # catch template tokens that were never registered in `repl` as well
    import re as _re
    stray = sorted(set(_re.findall(r"\b[A-Z][A-Z0-9_]{6,}\b", text))
                   - {"SOURCE", "CALCULATION", "INFERENCE", "UNVERIFIED",
                      "TRAINING", "SUPPORTED", "IDENTIFIED", "NAICS",
                      "MEXBORN", "USMEX", "USWHITE", "FBOTHER", "ADJINC",
                      "NATIVITY", "HISP", "POBP", "OCCP", "TIGER", "RESULT",
                      "README", "C15002I"})   # Census table name, not a token
    if left or stray:
        raise SystemExit(f"placeholders survived: {left + stray}")
    OUT.write_text(text)
    print(f"wrote {OUT} ({len(text):,} chars); primary spec {spec}, "
          f"elasticity {prim.elasticity_log_share:.3f}", flush=True)


if __name__ == "__main__":
    main()
