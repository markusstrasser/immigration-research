"""Render every computed specification in derived/ into RESULT.md's appendix, between the markers.

The brief's gate: every computed specification appears in RESULT.md, null ones included. Each table
below is generated from one derived CSV; nothing is typed by hand. Cells are "estimate (SE)" unless the
header says otherwise. Run after price.py:

    uv run --no-project --with pandas python3 infra/immigration-fiscal/school_dilution_2026_09_24/tables.py
"""
import json
import math
import sys
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "derived"
RESULT = HERE / "RESULT.md"
START, END = "<!-- tables:start -->", "<!-- tables:end -->"
FUNCS_A = ["current", "instruction", "instr_support", "pupil_support", "instr_staff", "administration", "gen_admin",
           "school_admin", "business"]
FUNCS_B = ["om", "transport", "other_elsec", "support_other", "support_total", "capital_outlay", "interest",
           "net_federal"]
REV = ["rev_total", "rev_state", "rev_local", "rev_federal", "title1", "fed_bilingual", "state_comp",
       "state_bilingual", "state_formula", "idea"]
SPEND = ["current", "instruction", "instr_support", "administration"]


def num(x, nd=3):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return ""
    if isinstance(x, (int,)) or (isinstance(x, float) and nd == 0):
        return f"{x:,.0f}"
    return f"{x:,.{nd}f}"


def cell(b, se, nd=3):
    return "" if b is None or (isinstance(b, float) and math.isnan(b)) else f"{num(b, nd)} ({num(se, nd)})"


def table(header, rows):
    out = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def frame(df, cols, nd=None):
    """Rows as records, so integer columns (years, counts) keep their type; floats get nd decimals."""
    nd = nd or {}
    return table(cols, [[num(r[c], nd.get(c, 3)) if isinstance(r[c], float) else r[c] for c in cols]
                        for r in df.to_dict("records")])


def functions():
    e = pd.read_csv(OUT / "function_elasticities.csv")
    lvl = e.spec.str.startswith("fe_level")
    e["resp"] = e.implied_total_response.where(e.implied_total_response.notna(), e.beta)
    e.loc[lvl, "resp"] = e.loc[lvl, "response_ratio"]
    e["resp_se"] = e.se
    e.loc[lvl, "resp_se"] = e.loc[lvl, "se"] / e.loc[lvl, "avg_cost_per_pupil"]
    keys = e[["spec", "weight", "term"]].drop_duplicates()
    parts = []
    for funcs, label in [(FUNCS_A, "A3a"), (FUNCS_B, "A3b")]:
        rows = []
        for _, k in keys.iterrows():
            s = e[e.spec.eq(k.spec) & e.weight.eq(k.weight) & e.term.eq(k.term)].set_index("function")
            n = int(s.n_obs.max())
            rows.append([k.spec, k.weight, k.term, f"{n:,}"] +
                        [cell(s.resp.get(f), s.resp_se.get(f)) if f in s.index else "" for f in funcs])
        parts.append(f"**Table {label}.** Response of spending to pupils by function: elasticity for log and "
                     "difference designs, marginal over average cost for `fe_level`, 1 + coefficient for the "
                     "CBO-style per-pupil designs (`x`, `up`, `down` at state level); SE in parentheses.\n\n" +
                     table(["spec", "weight", "term", "obs"] + funcs, rows))
    return "\n\n".join(parts)


def main():
    blocks = []
    g = pd.read_csv(OUT / "gate_national_pp.csv")
    blocks.append("**Table A1.** Gate: national current spending per pupil, systems with pupils (Census Table 8 "
                  "convention), dollars.\n\n" + frame(g, list(g.columns), {"computed_pp": 2, "published_pp": 2,
                                                                               "rel_diff": 5}))
    p = pd.read_csv(OUT / "panel_coverage.csv")
    blocks.append("**Table A2.** F-33 panel by fiscal year: rows, districts and pupils (pupils in millions after "
                  "division; spending in $bn nominal).\n\n" +
                  table(list(p.columns), [[int(r.fiscal_year), f"{int(r.rows):,}", f"{int(r.rows_with_ncesid):,}",
                                           f"{int(r.regular_districts_with_pupils_and_spending):,}",
                                           num(r.pupils_all_units / 1e6, 3), num(r.pupils_regular / 1e6, 3),
                                           num(r.current_spending_all_units_bn, 2), num(r.current_pp_all_units, 0),
                                           num(r.cpi_fy, 3)] for _, r in p.iterrows()]))
    for y in ("2019", "2024"):
        c = pd.read_csv(OUT / f"sample_coverage_fy2000_{y}.csv")
        blocks.append(f"**Table A2{'b' if y == '2019' else 'c'}.** Estimation sample FY2000-{y} by year (districts "
                      "passing the spending band, size and spell rules; pupils in millions).\n\n" +
                      table(["year", "districts", "pupils_m"], [[int(r.year), f"{int(r.districts):,}",
                                                                 num(r.pupils / 1e6, 3)] for _, r in c.iterrows()]))
    blocks.append(functions())
    s = pd.read_csv(OUT / "nonresponse_summary.csv")
    blocks.append("**Table A4a.** Split of the non-response of current spending, pupil-weighted district designs "
                  "FY2000-2019 (shares of the sum of parts).\n\n" +
                  frame(s, ["spec", "horizon", "current_response", "nonresponse_total", "nonresponse_sum_of_parts",
                            "additivity_gap", "instruction_response", "dilution_share_of_parts",
                            "dilution_broad_share_of_parts", "scale_share_of_parts"]))
    dcp = pd.read_csv(OUT / "nonresponse_decomposition.csv")
    fns = list(dict.fromkeys(dcp.function))
    rows = []
    for spec, grp in dcp.groupby("spec", sort=False):
        gi = grp.set_index("function")
        rows.append([spec] + [num(gi.loc[f, "share_of_nonresponse"]) if gi.loc[f, "class"] != "beside_current"
                              else "resp " + num(gi.loc[f, "response"]) for f in fns])
    blocks.append("**Table A4b.** Each function's share of the non-response (capital outlay and interest: their "
                  "own response, outside current spending).\n\n" + table(["spec"] + fns, rows))
    fs = pd.read_csv(OUT / "iv_first_stage.csv")
    blocks.append("**Table A5a.** Shift-share first stage (fall-2000 Hispanic share x national group growth); "
                  "F is the clustered Wald F. Weak in every specification; not used.\n\n" +
                  frame(fs, list(fs.columns), {"n_obs": 0, "districts": 0}))
    iv = pd.read_csv(OUT / "iv_elasticities.csv")
    rows = []
    for (spec, w), grp in iv.groupby(["spec", "weight"], sort=False):
        gi = grp.set_index("function")
        rows.append([spec, w] + [cell(gi.beta_iv.get(f), gi.se_iv.get(f)) if f in gi.index else ""
                                 for f in FUNCS_A[:6] + ["om", "capital_outlay"]])
    blocks.append("**Table A5b.** 2SLS elasticities on the weak instrument, shown because computed; not used.\n\n" +
                  table(["spec", "weight"] + FUNCS_A[:6] + ["om", "capital_outlay"], rows))
    cc = pd.read_csv(OUT / "compensatory_coverage.csv")
    blocks.append("**Table A6a.** Compensatory-funding waves: districts, pupils (m), pupil-weighted Hispanic share "
                  "and covariate coverage.\n\n" + frame(cc, list(cc.columns)))
    ce = pd.read_csv(OUT / "compensatory_estimates.csv")
    for outs, label, what in [(REV, "A6b", "revenue"), (SPEND, "A6c", "spending")]:
        rows = []
        for (design, fy, spec, term), grp in ce.groupby(["design", "fy", "spec", "term"], sort=False):
            gi = grp.set_index("outcome")
            if not any(o in gi.index for o in outs):
                continue
            nd = 3 if spec.startswith("log_total") else 0
            rows.append([design, "" if fy < 0 else int(fy), spec, term, f"{int(grp.n_districts.max()):,}"] +
                        [cell(gi.coef_usd_per_pupil_per_unit_share.get(o), gi.se.get(o), nd) if o in gi.index else ""
                         for o in outs])
        blocks.append(f"**Table {label}.** Compensatory funding, {what} outcomes: dollars per pupil (2024) per unit "
                      "share (log-total specs: elasticities); state fixed effects in cross-sections, district and "
                      "state-year effects in panels; SE clustered by state.\n\n" +
                      table(["design", "fy", "spec", "term", "districts"] + outs, rows))
    cs = pd.read_csv(OUT / "class_size_elasticities.csv")
    blocks.append("**Table A7.** Teachers on pupils, long differences within state.\n\n" +
                  frame(cs, list(cs.columns), {"n_districts": 0}))
    ph = pd.read_csv(OUT / "pricing_by_horizon.csv")
    blocks.append("**Table A8.** Instruction dilution by response basis: instruction dollars a year ($bn, 2024) and "
                  "present value of other pupils' lifetime earnings ($bn a year).\n\n" +
                  frame(ph, ["horizon", "price_year", "b_instruction", "response_current", "instruction_dilution_bn",
                             "instruction_dilution_power_law_bn", "instruction_dilution_full_funding_others_bn",
                             "instr_support_dilution_bn", "per_other_pupil_in_group_districts_usd",
                             "pv_earnings_bn_jm_low", "pv_earnings_bn_jm_central", "pv_earnings_bn_jm_high",
                             "pv_earnings_bn_jm_central_cfr_va", "pv_earnings_bn_jm_central_power_law",
                             "pv_earnings_bn_jm_central_full_funding_others"],
                        {"per_other_pupil_in_group_districts_usd": 0}))
    geo = pd.read_csv(OUT / "pricing_by_region_income.csv")
    blocks.append("**Table A9.** By region and district child-poverty quintile (pupil-weighted, SAIPE 2023; Q1 least "
                  "poor): pupils (m), dilution ($bn), per other pupil ($).\n\n" +
                  frame(geo, list(geo.columns), {"per_other_pupil_usd": 0, "pv_per_other_pupil_usd_jm_central": 0,
                                                 "pv_per_other_pupil_usd_full_funding": 0}))
    pc = pd.read_csv(OUT / "pricing_composition.csv")
    blocks.append("**Table A10.** Composition channel: others' instruction change and its present value ($bn a year; "
                  "negative is a loss).\n\n" + frame(pc, list(pc.columns), {"gamma_usd_per_unit_share": 0}))
    pcs = pd.read_csv(OUT / "pricing_class_size.csv")
    blocks.append("**Table A11.** Class size as the same resource loss (never added).\n\n" +
                  frame(pcs, list(pcs.columns)))
    wl = pd.read_csv(OUT / "winners_losers_rows.csv")
    blocks.append("**Table A12.** `derived/winners_losers_rows.csv` ($bn a year; per person in dollars; the "
                  "counterfactual and source columns are in the file).\n\n" +
                  frame(wl, ["group", "channel", "direction", "bn_low", "bn_central", "bn_high", "population_m",
                             "per_person_usd", "basis", "relation_to_account"], {"per_person_usd": 0}))
    k = json.loads((OUT / "pricing_constants.json").read_text())
    blocks.append("**Table A13.** Pricing constants (`derived/pricing_constants.json`).\n\n" +
                  table(["constant", "value"], [[key, json.dumps(val) if isinstance(val, dict) else num(val, 4)]
                                                for key, val in k.items()]))
    text = RESULT.read_text()
    if START not in text or END not in text:
        raise SystemExit(f"[BLOCKED] RESULT.md lacks the {START} / {END} markers")
    head, rest = text.split(START, 1)
    _, tail = rest.split(END, 1)
    RESULT.write_text(head + START + "\n\n" + "\n\n".join(blocks) + "\n\n" + END + tail)
    print(f"rendered {len(blocks)} tables into {RESULT.name}")


if __name__ == "__main__":
    sys.exit(main())
