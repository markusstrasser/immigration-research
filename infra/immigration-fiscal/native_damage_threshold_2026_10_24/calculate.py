#!/usr/bin/env python3
"""Source-extract the normalization and calculate explicitly conditional transports.

Run: OPENBLAS_NUM_THREADS=1 uv run --no-project python3 {lane}/calculate.py
No upstream lane is rebuilt. Raw CPS data and the adopted case are read-only.
BEA has no GDP-by-nativity table: the native-output allocation below is a proxy.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import resource
import sys
import time
import zipfile
from html.parser import HTMLParser
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
FISCAL = HERE.parent
CPS = FISCAL / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip"
CPS_SHA = "318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b"
BEA = HERE / "_cache/basis_bea_annual_2026.html"


def require(ok, message):
    if not ok:
        raise SystemExit(f"[BLOCKED] {message}")


def sha(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


class Tables(HTMLParser):
    """Extract a declared BEA table, retaining literal header and row cells."""
    def __init__(self, table_id):
        super().__init__(convert_charrefs=True)
        self.table_id, self.active = table_id, False
        self.rows, self.row, self.cell = [], None, None

    def handle_starttag(self, tag, attrs):
        if tag == "table" and dict(attrs).get("id") == self.table_id:
            self.active = True
        if self.active and tag == "tr":
            self.row = []
        if self.active and tag in ("th", "td"):
            self.cell = []

    def handle_data(self, data):
        if self.active and self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if self.active and tag in ("th", "td") and self.cell is not None:
            self.row.append(" ".join("".join(self.cell).split()))
            self.cell = None
        if self.active and tag == "tr" and self.row:
            self.rows.append(self.row)
            self.row = None
        if self.active and tag == "table":
            self.active = False


def bea_rows():
    html = BEA.read_text()
    extracted = {}
    for label, table_id in (("income", "CPSTable41941"), ("product", "CPSTable41942")):
        parser = Tables(table_id)
        parser.feed(html)
        require(len(parser.rows) > 5, f"BEA table {table_id} not extracted")
        require(parser.rows[1][:5] == ["2021", "2022", "2023", "2024", "2025"],
                f"BEA table {table_id} year-column layout changed")
        extracted[label] = parser.rows

    def value(table, label):
        matches = [row for row in extracted[table] if len(row) >= 7 and row[1] == label]
        require(len(matches) == 1, f"BEA row not unique: {label}")
        return float(matches[0][5].replace(",", "").replace("−", "-"))

    return extracted, {
        "gdp_2024_bn": value("product", "GDP"),
        "gdi_2024_bn": value("product", "Equals: GDI"),
        "compensation_2024_bn": value("income", "Compensation of employees"),
        "proprietors_2024_bn": value("income", "Proprietors’ income with IVA and CCAdj"),
        "source": "BEA September 2026 Annual Update, Tables 5 and 6, 2024 levels",
    }


def cps_basis(meta):
    require(CPS.exists(), f"missing pinned source {CPS}")
    require(sha(CPS) == CPS_SHA, "CPS source SHA256 differs")
    fields = ["PH_SEQ", "PPPOS", "A_AGE", "PRPERTYP", "PRCITSHP", "PENATVTY",
              "PEFNTVTY", "PEMNTVTY", "PRDTHSP", "PEARNVAL", "WSAL_VAL", "A_HGA",
              "INT_VAL", "DIV_VAL", "RNT_VAL", "WORKYN", "A_CIVLF"]
    with zipfile.ZipFile(CPS) as archive:
        d = pd.read_csv(archive.open("pppub25.csv"), usecols=fields)
        weights = pd.read_csv(archive.open("asec_csv_repwgt_2025.csv"),
                              usecols=["h_seq", "PPPOS", "pwwgt0"]).rename(columns={"h_seq": "PH_SEQ"})
        states = pd.read_csv(archive.open("hhpub25.csv"), usecols=["H_SEQ", "GESTFIPS"])
    d = d.merge(weights, on=["PH_SEQ", "PPPOS"], validate="one_to_one")
    d = d.merge(states, left_on="PH_SEQ", right_on="H_SEQ", validate="many_to_one")
    require(d.pwwgt0.notna().all(), "missing CPS person weight")
    civ = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
    native = d.PRCITSHP.isin([1, 2, 3])
    mexborn = d.PRCITSHP.isin([4, 5]) & d.PENATVTY.eq(303)
    mexparent = d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)
    us_codes = [57, 60, 66, 69, 73, 78]
    union = civ & (mexborn | (native & mexparent) |
                   (native & d.PEFNTVTY.isin(us_codes) & d.PEMNTVTY.isin(us_codes) & d.PRDTHSP.eq(1)))
    w = d.pwwgt0
    require(abs(w[civ].sum() - 336_727_803) < 1, "published civilian population gate")
    require(abs(w[union].sum() - 40_896_574.15235156) < 0.01, "published observable union gate")
    earnings = d.PEARNVAL.clip(lower=0)
    property_income = (d.INT_VAL + d.DIV_VAL + d.RNT_VAL).clip(lower=0)
    native_labor_share = float((w * earnings)[civ & native].sum() / (w * earnings)[civ].sum())
    native_capital_share = float((w * property_income)[civ & native].sum() / (w * property_income)[civ].sum())
    wage_native_share = float((w * d.WSAL_VAL.clip(lower=0))[civ & native].sum() /
                             (w * d.WSAL_VAL.clip(lower=0))[civ].sum())

    # Current authoritative row4 payload pins this exact adjustment. Native shares
    # above use the published national frame; group doses below use the case frame.
    row4_path = FISCAL / meta["production"]["file"]
    require(sha(row4_path) == meta["production"]["sha256"], "row4 production source changed")
    row4 = json.loads(row4_path.read_text())
    w4 = w.copy()
    for status, code in (("naturalized", 4), ("noncitizen", 5)):
        mask = mexborn & d.PRCITSHP.eq(code) & ~d.GESTFIPS.isin([6, 48])
        ref = row4["row4_factors"][status]
        require(int(mask.sum()) == ref["records"], f"row4 {status} records differ")
        w4.loc[mask] *= ref["factor"]
    require(abs(w4[union].sum() - row4["populations"]["row4"]) < 0.01, "row4 total gate")

    def total(mask, weight=w4):
        return float(weight[mask].sum())

    adults = civ & d.A_AGE.ge(25)
    adults18 = civ & d.A_AGE.ge(18)
    earners = civ & d.PEARNVAL.gt(0)
    not_ba = d.A_HGA.between(31, 42)
    hs_less = d.A_HGA.between(31, 39)
    drops = d.A_HGA.between(31, 38)
    hs_equiv = d.A_HGA.eq(39).astype(float) + 0.5 * d.A_HGA.between(40, 42).astype(float)
    years_education = d.A_HGA.map({31: 0, 32: 2.5, 33: 5.5, 34: 7.5, 35: 9, 36: 10,
                                  37: 11, 38: 12, 39: 12, 40: 13, 41: 14, 42: 14,
                                  43: 16, 44: 18, 45: 19, 46: 20})
    worker = civ & d.A_AGE.between(16, 65) & d.A_CIVLF.eq(1) & (d.A_AGE - years_education - 6).ge(1)
    # Lewis's regressor counts heads in the labor force. Potential experience is
    # approximated from CPS schooling categories; it is not a manufacturing dose.
    wl = w4.where(worker, 0)
    dh = float(wl[drops].sum() / (wl * hs_equiv).sum())
    dh_without_g1 = float(wl[drops & ~mexborn].sum() / (wl * hs_equiv)[~mexborn].sum())
    return {
        "national_frame": "published CPS ASEC 2025 civilian weights; income year 2024",
        "case_dose_frame": "CPS with adopted row4 Mexico-born reweight; missed people not imputed",
        "native_definition": "PRCITSHP in 1,2,3 (CPS native; includes born abroad to US parents)",
        "native_labor_income_share": native_labor_share,
        "native_wages_share": wage_native_share,
        "native_property_income_share": native_capital_share,
        "population_civilian_published": total(civ, w),
        "population_native_published": total(civ & native, w),
        "population_civilian_row4": total(civ),
        "observable_union_row4": total(union),
        "mexborn_row4": total(civ & mexborn),
        "mexborn_case_with_coverage": total(civ & mexborn) + meta["coverage"]["counts_by_generation_folded"]["G1"],
        "mexborn_adult25plus_noba_share_adults_pp": 100 * total(adults & mexborn & not_ba) / total(adults),
        "mexborn_adult25plus_hsless_share_adults_pp": 100 * total(adults & mexborn & hs_less) / total(adults),
        "mexborn_adult18plus_noba_share_adults_pp": 100 * total(civ & d.A_AGE.ge(18) & mexborn & not_ba) /
                                                   total(civ & d.A_AGE.ge(18)),
        "mexborn_adult18plus_belowhs_share_adults_pp": 100 * total(adults18 & mexborn & drops) / total(adults18),
        "mexborn_adult18plus_hsplus_share_adults_pp": 100 * total(adults18 & mexborn & d.A_HGA.between(39, 46)) /
                                                     total(adults18),
        "mexborn_earners_share_earners_pp": 100 * total(earners & mexborn) / total(earners),
        "mexborn_earners_noba_share_earners_pp": 100 * total(earners & mexborn & not_ba) / total(earners),
        "mexborn_earners_hsless_share_earners_pp": 100 * total(earners & mexborn & hs_less) / total(earners),
        "lewis_all_industry_labor_force_drop_hsequiv": dh,
        "lewis_all_industry_labor_force_drop_hsequiv_without_mexborn": dh_without_g1,
        "lewis_delta_drop_hsequiv": dh - dh_without_g1,
        "mexborn_nocoverage_warning": "case Census-coverage additions not individually observed; this is counted G1 dose",
    }


def conditional_scenarios(basis):
    """These outputs cannot be summed: none is an admissible new causal term."""
    inputs = json.loads((HERE / "source_inputs.json").read_text())
    roots = json.loads((HERE / "derived/roots_inputs.json").read_text())
    for name, source in roots["sources"].items():
        require(sha(HERE / "_cache" / name) == source["sha256"], f"deep-roots source changed: {name}")
    native = basis["native_output_proxy"]["central_two_thirds_proprietors"]["native_output_proxy_bn"]
    dose = basis["cps"]["lewis_delta_drop_hsequiv"]

    def harm(beta, treatment):
        # Outcome equation is log(Y_with/Y_without)=beta*treatment.
        # Every cost here divides by observed Y_with, like the threshold.
        return 100 * math.expm1(-beta * treatment)

    lewis = inputs["lewis"]
    lewis_range = sorted(harm(lewis["output_log_coefficient"] + j * 1.96 * lewis["se"], dose)
                         for j in (-1, 1))
    peri = inputs["peri"]
    current_share = basis["cps"]["mexborn_earners_share_earners_pp"] / 100
    inflow_over_initial = current_share / (1 - current_share)
    peri_range = sorted(harm(peri["output_log_coefficient"] + j * 1.96 * peri["se"], inflow_over_initial)
                        for j in (-1, 1))
    s = basis["lineage_share_published_civilian_pp"] / 100
    mx, us = roots["countries"]["mex"], roots["countries"]["usa"]
    gap_bounds = [us["normalized_lower"] - mx["normalized_upper"],
                  us["normalized_upper"] - mx["normalized_lower"]]
    gap_mid = sum(gap_bounds) / 2
    roots_readings = {}
    for name in ("putterman_weil", "briggeman"):
        row = inputs[name]
        beta, se = row["log_gdp_coefficient"], row["se"]
        scale = s / (1 - s)
        calc = lambda b, g: 100 * math.expm1(b * scale * g)
        coverage = sorted(calc(beta, g) for g in gap_bounds)
        coef_and_coverage = [calc(b, g) for b in (beta - 1.96 * se, beta + 1.96 * se) for g in gap_bounds]
        roots_readings[name] = {
            "central_midpoint_of_missing_input_bounds_pct": calc(beta, gap_mid),
            "source_input_coverage_only_range_pct": coverage,
            "coefficient_95_normal_and_source_coverage_envelope_pct": [min(coef_and_coverage), max(coef_and_coverage)],
            "envelope_is": "not an uncertainty interval for native output; excludes causal, lineage-ancestry, incidence, and date transport uncertainty",
            "beta_needed_for_1pct_at_gap_midpoint": math.log1p(0.01) / (scale * gap_mid),
        }
    cp = inputs["clemens_pritchett"]
    delta, c = cp["mexico_initial_gap"], cp["conservative_c_scenario"]
    # Eq3's h is measured against no-contamination output. Convert a current-
    # output threshold t into h=t/(1+t) before solving h=delta*phi/(1-c*phi).
    no_migration_loss = 0.01 / 1.01
    phi_at_1pct = no_migration_loss / (delta + c * no_migration_loss)
    politics = inputs["politics"]
    pdose = basis["cps"]["mexborn_adult18plus_belowhs_share_adults_pp"]
    hdose = basis["cps"]["mexborn_adult18plus_hsplus_share_adults_pp"]
    vote = politics["mayda_low_skill_vote_pp_per_share_pp"]
    vse = politics["mayda_low_skill_se"]
    attention = inputs["attention"]
    return {
        "sign": "positive = harm from migration, negative = benefit; percentages divide by current native-output proxy",
        "eligible_additional_causal_native_output_terms": [],
        "empty_set_accounting_subtotal_pct": 0,
        "total_omitted_damage_pct": None,
        "total_omitted_damage_status": "not identified; the empty subtotal is not an estimate or bound on omitted effects",
        "full_range_including_weaker_evidence_pct": None,
        "full_range_status": "not identified; incomparable treatments, missing transfer functions, overlap, and no joint distribution",
        "lewis_counted_g1_dose": {
            "delta_ratio": dose,
            "conditional_pct_times_native_exposed_sector_share": harm(lewis["output_log_coefficient"], dose),
            "coefficient_95_normal_range_times_sector_share": lewis_range,
            "sector_share_and_transport": "unmeasured; whole-economy application means setting sector share to one as an illustration",
        },
        "peri_counted_g1_stock_as_inflow": {
            "inflow_over_initial_workers_proxy": inflow_over_initial,
            "conditional_harm_pct": harm(peri["output_log_coefficient"], inflow_over_initial),
            "coefficient_95_normal_range_pct": peri_range,
            "transport_status": "not an identified lineage or low-skill native effect",
        },
        "deep_roots_gap_bounds": gap_bounds,
        "deep_roots_ecological_readings": roots_readings,
        "clemens_pritchett_model_only": {
            "phi_needed_for_1pct_current_output_loss": phi_at_1pct,
            "loss_per_pp_phi_near_zero_pct": delta,
            "measured_phi_range": None,
            "actual_lineage_native_output_effect_pct": None,
        },
        "politics": {
            "counted_g1_belowhs_adults_pp": pdose,
            "counted_g1_hsplus_adults_pp": hdose,
            "conditional_low_skill_only_vote_change_pp": vote * pdose,
            "coefficient_95_normal_low_skill_only_vote_change_pp": [(vote - 1.96 * vse) * pdose, (vote + 1.96 * vse) * pdose],
            "conditional_both_skill_arms_vote_change_pp": vote * pdose + politics["mayda_high_skill_vote_pp_per_share_pp"] * hdose,
            "both_arms_interval": None,
            "vote_warning": "fixed-denominator counted-G1 composition illustration, not finite national removal or national election prediction; covariance absent for two-arm interval",
            "extra_year15_episode_probability_for_1pct_loss": no_migration_loss /
                politics["funke_year15_gdp_loss_fraction_scenario"],
            "probability_threshold_assumption": "Zero episode probability absent the group's contribution; fixed homogeneous 10-percent year15 output loss. A nonzero baseline changes this diagnostic.",
            "measured_extra_episode_probability": None,
        },
        "attention_gross_allocation_only": {
            key: {"bn": attention["all_origin_gross_bn"] * a,
                  "pct_native_output": 100 * attention["all_origin_gross_bn"] * a / native}
            for key, a in attention["attribution"].items()
        },
        "historical_scale_design_costs_only": {
            "old_union_population": 40_896_574.15235156,
            "harm_bn": [109, 677],
            "normalization_pct": [100 * x / native for x in (109, 677)],
            "scope": "40.90M old-source calibration, not a repricing of the 44.90M lineage or native-only incidence; alternatives to existing scale row",
        },
    }


def main():
    start = time.perf_counter()
    parser = argparse.ArgumentParser()
    parser.add_argument("--out-dir", type=Path, default=HERE / "derived")
    args = parser.parse_args()
    args.out_dir.mkdir(parents=True, exist_ok=True)
    live_path = FISCAL / "live_case.json"
    live = json.loads(live_path.read_text())
    require(live["key"] == "oct16", "live case changed; review transport and baseline")
    case_path = FISCAL / live["lane"] / "derived/corrections.json"
    summary_path = FISCAL / live["lane"] / "derived/summary.json"
    meta = json.loads(case_path.read_text())["meta"]
    tables, bea = bea_rows()
    cps = cps_basis(meta)
    gdp, gdi = bea["gdp_2024_bn"], bea["gdi_2024_bn"]
    comp, prop = bea["compensation_2024_bn"], bea["proprietors_2024_bn"]
    native_outputs = {}
    for name, labor in (("comp_only", comp / gdi), ("central_two_thirds_proprietors", (comp + 2 * prop / 3) / gdi),
                        ("all_proprietors", (comp + prop) / gdi), ("production_alpha_065", 0.65)):
        share = labor * cps["native_labor_income_share"] + (1 - labor) * cps["native_property_income_share"]
        native_outputs[name] = {"labor_weight": labor, "native_factor_share": share,
                                "native_output_proxy_bn": gdp * share}
    readings_path = FISCAL / "world_ledger_2026_09_27/derived/readings_cash_oct16.csv"
    readings = pd.read_csv(readings_path)
    selected = readings[(readings.scope == "A_completed") & readings.reading.eq("R1") &
                        readings.public_pension_share.eq(1) & readings.g3_bound.eq("zero") &
                        readings.weighting.isin(["equal_lambda_1.16", "hendren_a"])]
    require(len(selected) == 4, "R1 selection must contain two ends and two welfare conventions")
    world_column = "world_total_bn"
    require(world_column in selected, "world ledger schema changed")
    baseline = {"bea": bea, "cps": cps, "native_output_proxy": native_outputs,
                "lineage_people": meta["population_v9"]["with_coverage"],
                "lineage_share_published_civilian_pp": 100 * meta["population_v9"]["with_coverage"] /
                                                      cps["population_civilian_published"],
                "r1_world_gain_bn": [float(selected[world_column].min()), float(selected[world_column].max())],
                "r1_break_even_native_output_pct": {
                    name: [100 * float(selected[world_column].min()) / v["native_output_proxy_bn"],
                           100 * float(selected[world_column].max()) / v["native_output_proxy_bn"]]
                    for name, v in native_outputs.items()},
                "r1_break_even_total_gdp_pct": [100 * float(selected[world_column].min()) / gdp,
                                                 100 * float(selected[world_column].max()) / gdp],
                "native_output_is": "allocation proxy, not BEA measurement or native welfare",
                "bea_vintage": "September 2026; preserves world ledger numerator rather than rebuilding it"}
    (args.out_dir / "basis.json").write_text(json.dumps(baseline, indent=2) + "\n")
    scenarios = conditional_scenarios(baseline)
    (args.out_dir / "conditional_scenarios.json").write_text(json.dumps(scenarios, indent=2) + "\n")
    (args.out_dir / "bea_extracted_rows.json").write_text(json.dumps(tables, indent=2) + "\n")
    selected.to_csv(args.out_dir / "r1_selected.csv", index=False, lineterminator="\n")
    paths = [live_path, case_path, summary_path, CPS, BEA, readings_path, HERE / "source_inputs.json",
             HERE / "derived/roots_inputs.json", FISCAL / meta["production"]["file"]]
    manifest = [{"path": str(p.relative_to(REPO)), "sha256": sha(p)} for p in paths]
    (args.out_dir / "source_hashes.json").write_text(json.dumps(manifest, indent=2) + "\n")
    with (args.out_dir / "source_cache_hashes.csv").open("w", newline="") as f:
        writer = csv.writer(f, lineterminator="\n")
        writer.writerow(["cache_file", "bytes", "sha256"])
        for path in sorted((HERE / "_cache").iterdir()):
            if path.suffix.lower() in (".pdf", ".xls", ".html", ".jpg", ".docx"):
                writer.writerow([path.name, path.stat().st_size, sha(path)])
    print(json.dumps(baseline, indent=2))
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * (1 if sys.platform == "darwin" else 1024)
    print(f"PASS; elapsed_s={time.perf_counter() - start:.3f}; maxrss_bytes={rss}")


if __name__ == "__main__":
    main()
