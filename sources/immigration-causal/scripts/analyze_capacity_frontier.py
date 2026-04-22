"""Compare stock, flow, and load-capacity formulations on county outcomes."""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf

DATA = Path(__file__).parent.parent / "data"
COUNTY_PANEL = DATA / "outcomes" / "county_outcome_panel.parquet"
RECEIVER_PANEL = DATA / "threshold" / "analysis" / "receiver_threshold_panel.parquet"
OUT_DIR = DATA / "outcomes" / "analysis"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OUT_SUMMARY = OUT_DIR / "county_capacity_frontier_summary.json"
OUT_MODELS = OUT_DIR / "county_capacity_model_comparison.csv"
OUT_THRESH = OUT_DIR / "county_capacity_threshold_grid.csv"
OUT_DECILES = OUT_DIR / "county_load_capacity_deciles.csv"
OUT_RECEIVER = OUT_DIR / "receiver_capacity_descriptives_2024.csv"

OCCUPANTS_PER_UNIT = 2.5


def prepare_county() -> pd.DataFrame:
    df = pd.read_parquet(COUNTY_PANEL).copy()
    df = df.dropna(
        subset=[
            "margin_shift",
            "fb_share",
            "recent_fb_annual_share",
            "permit_units_2021_2024",
            "permit_rate_per_1k",
            "qcew_employment_log_change_2021_2024",
            "qcew_wkly_wage_log_change_2021_2024",
            "net_us_migration_share_2022_23",
            "log_pop",
            "state_name",
        ]
    )
    df = df[df["totpop"] >= 10000].copy()
    df["annual_recent_fb_persons"] = df["recent_fb_annual_share"] * df["totpop"]
    df["annual_permit_units"] = df["permit_units_2021_2024"] / 4.0
    df["annual_housing_capacity_persons"] = df["annual_permit_units"] * OCCUPANTS_PER_UNIT
    df["recent_fb_per_permit_unit"] = df["annual_recent_fb_persons"] / df["annual_permit_units"].replace(0, np.nan)
    df["recent_fb_to_capacity_ratio"] = df["annual_recent_fb_persons"] / df["annual_housing_capacity_persons"].replace(0, np.nan)

    finite = df["recent_fb_per_permit_unit"].replace([np.inf, -np.inf], np.nan).dropna()
    p95 = float(finite.quantile(0.95))
    p99 = float(finite.quantile(0.99))
    df["recent_fb_per_permit_unit_w95"] = df["recent_fb_per_permit_unit"].clip(upper=p95)
    df["recent_fb_per_permit_unit_w99"] = df["recent_fb_per_permit_unit"].clip(upper=p99)
    df["log_recent_fb_per_permit_unit_w95"] = np.log1p(df["recent_fb_per_permit_unit_w95"])
    df["log_recent_fb_per_permit_unit_w99"] = np.log1p(df["recent_fb_per_permit_unit_w99"])

    for col in ("fb_share", "recent_fb_annual_share", "log_recent_fb_per_permit_unit_w95", "log_recent_fb_per_permit_unit_w99"):
        std = df[col].std(ddof=0)
        df[f"z_{col}"] = (df[col] - df[col].mean()) / std

    for q in (0.7, 0.8, 0.9):
        df[f"high_recent_q{int(q * 100)}"] = (df["recent_fb_annual_share"] >= df["recent_fb_annual_share"].quantile(q)).astype(int)
        df[f"high_load_q{int(q * 100)}"] = (df["recent_fb_per_permit_unit_w99"] >= df["recent_fb_per_permit_unit_w99"].quantile(q)).astype(int)
    for q in (0.25, 0.5):
        df[f"low_permit_q{int(q * 100)}"] = (df["permit_rate_per_1k"] <= df["permit_rate_per_1k"].quantile(q)).astype(int)

    return df


def model_comparison(df: pd.DataFrame) -> pd.DataFrame:
    outcomes = {
        "margin_shift": "margin_shift",
        "wkly_wage_log_change": "qcew_wkly_wage_log_change_2021_2024",
        "employment_log_change": "qcew_employment_log_change_2021_2024",
        "net_us_migration_share": "net_us_migration_share_2022_23",
    }
    formulas = {
        "stock_only": ("z_fb_share", "{outcome} ~ z_fb_share + receiver_city + border_state + log_pop + C(state_name)"),
        "flow_only": ("z_recent_fb_annual_share", "{outcome} ~ z_recent_fb_annual_share + receiver_city + border_state + log_pop + C(state_name)"),
        "load_only": (
            "z_log_recent_fb_per_permit_unit_w99",
            "{outcome} ~ z_log_recent_fb_per_permit_unit_w99 + receiver_city + border_state + log_pop + C(state_name)",
        ),
        "combined": (
            "z_log_recent_fb_per_permit_unit_w99",
            "{outcome} ~ z_fb_share + z_recent_fb_annual_share + z_log_recent_fb_per_permit_unit_w99 + receiver_city + border_state + log_pop + C(state_name)",
        ),
        "high_load90": ("high_load_q90", "{outcome} ~ high_load_q90 + receiver_city + border_state + log_pop + C(state_name)"),
    }

    rows: list[dict[str, object]] = []
    for outcome_name, outcome_var in outcomes.items():
        for model_name, (term, formula_tpl) in formulas.items():
            model = smf.ols(formula_tpl.format(outcome=outcome_var), data=df).fit(cov_type="HC3")
            rows.append(
                {
                    "outcome": outcome_name,
                    "model": model_name,
                    "term": term,
                    "beta": float(model.params.get(term, np.nan)),
                    "t_stat": float(model.tvalues.get(term, np.nan)),
                    "p_value": float(model.pvalues.get(term, np.nan)),
                    "adj_r2": float(model.rsquared_adj),
                    "n": int(model.nobs),
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(OUT_MODELS, index=False)
    return out


def threshold_grid(df: pd.DataFrame) -> pd.DataFrame:
    outcomes = {
        "margin_shift": "margin_shift",
        "wkly_wage_log_change": "qcew_wkly_wage_log_change_2021_2024",
        "employment_log_change": "qcew_employment_log_change_2021_2024",
        "net_us_migration_share": "net_us_migration_share_2022_23",
    }
    rows: list[dict[str, object]] = []
    for rq in (70, 80, 90):
        for pq in (25, 50):
            high_recent = f"high_recent_q{rq}"
            low_permit = f"low_permit_q{pq}"
            for outcome_name, outcome_var in outcomes.items():
                model = smf.ols(
                    f"{outcome_var} ~ {high_recent}*{low_permit} + receiver_city + border_state + us_inflow_share + log_pop + C(state_name)",
                    data=df,
                ).fit(cov_type="HC3")
                term = f"{high_recent}:{low_permit}"
                rows.append(
                    {
                        "family": "flow_x_permit",
                        "recent_quantile": rq,
                        "capacity_quantile": pq,
                        "outcome": outcome_name,
                        "term": term,
                        "beta": float(model.params.get(term, np.nan)),
                        "t_stat": float(model.tvalues.get(term, np.nan)),
                        "p_value": float(model.pvalues.get(term, np.nan)),
                        "adj_r2": float(model.rsquared_adj),
                        "n": int(model.nobs),
                    }
                )
    for lq in (80, 90):
        high_load = f"high_load_q{lq}"
        for outcome_name, outcome_var in outcomes.items():
            model = smf.ols(
                f"{outcome_var} ~ {high_load} + receiver_city + border_state + fb_share + log_pop + C(state_name)",
                data=df,
            ).fit(cov_type="HC3")
            rows.append(
                {
                    "family": "load_threshold",
                    "recent_quantile": lq,
                    "capacity_quantile": np.nan,
                    "outcome": outcome_name,
                    "term": high_load,
                    "beta": float(model.params.get(high_load, np.nan)),
                    "t_stat": float(model.tvalues.get(high_load, np.nan)),
                    "p_value": float(model.pvalues.get(high_load, np.nan)),
                    "adj_r2": float(model.rsquared_adj),
                    "n": int(model.nobs),
                }
            )
    out = pd.DataFrame(rows)
    out.to_csv(OUT_THRESH, index=False)
    return out


def load_deciles(df: pd.DataFrame) -> pd.DataFrame:
    base = df[df["recent_fb_per_permit_unit_w99"].notna()].copy()
    base["load_decile"] = pd.qcut(base["recent_fb_per_permit_unit_w99"], 10, labels=[f"D{i}" for i in range(1, 11)], duplicates="drop")
    out = (
        base.groupby("load_decile", observed=True)
        .agg(
            n=("fips5", "count"),
            median_fb_per_permit_unit=("recent_fb_per_permit_unit_w99", "median"),
            median_recent_fb_share=("recent_fb_annual_share", "median"),
            median_fb_share=("fb_share", "median"),
            median_margin_shift_pp=("margin_shift", lambda x: x.median() * 100),
            median_wkly_wage_change_pp=("qcew_wkly_wage_log_change_2021_2024", lambda x: x.median() * 100),
            median_employment_change_pp=("qcew_employment_log_change_2021_2024", lambda x: x.median() * 100),
            median_net_us_migration_share_pp=("net_us_migration_share_2022_23", lambda x: x.median() * 100),
        )
        .reset_index()
    )
    out.to_csv(OUT_DECILES, index=False)
    return out


def receiver_descriptives() -> tuple[pd.DataFrame, dict[str, object]]:
    df = pd.read_parquet(RECEIVER_PANEL)
    sub = df[df["year"] == 2024].copy()
    sub["permit_to_hic"] = sub["county_total_units"] / sub["hic_total_beds"].replace(0, np.nan)
    sub["permit_to_pit"] = sub["county_total_units"] / sub["pit_overall_homeless"].replace(0, np.nan)
    sub["shelter_gap_vs_hic"] = sub["pit_sheltered_total"] - sub["hic_total_beds"]
    out = sub[
        [
            "node_label",
            "sheltered_to_hic_ratio",
            "overall_to_hic_ratio",
            "shelter_gap_vs_hic",
            "county_total_units",
            "permit_to_hic",
            "permit_to_pit",
            "total_spending_usd_M",
            "peak_shelter_census",
            "peak_minus_baseline_shelter",
        ]
    ].sort_values("sheltered_to_hic_ratio", ascending=False)
    out.to_csv(OUT_RECEIVER, index=False)
    summary = {
        "n_2024_nodes": int(len(out)),
        "saturated_nodes_2024": out[out["sheltered_to_hic_ratio"] > 1]["node_label"].tolist(),
        "corr_sheltered_ratio_vs_spending": float(out["sheltered_to_hic_ratio"].corr(out["total_spending_usd_M"])),
        "corr_shelter_gap_vs_spending": float(out["shelter_gap_vs_hic"].corr(out["total_spending_usd_M"])),
        "corr_permit_to_hic_vs_sheltered_ratio": float(out["permit_to_hic"].corr(out["sheltered_to_hic_ratio"])),
    }
    return out, summary


def load_robustness(df: pd.DataFrame) -> dict[str, object]:
    specs = {
        "all_w99": ("z_log_recent_fb_per_permit_unit_w99", df),
        "all_w95": ("z_log_recent_fb_per_permit_unit_w95", df),
        "non_receiver_non_border_w99": (
            "z_log_recent_fb_per_permit_unit_w99",
            df[(df["receiver_city"] == 0) & (df["border_state"] == 0)].copy(),
        ),
    }
    outcomes = {
        "wkly_wage_log_change": "qcew_wkly_wage_log_change_2021_2024",
        "employment_log_change": "qcew_employment_log_change_2021_2024",
    }
    out: dict[str, object] = {}
    for spec_name, (term, sub) in specs.items():
        out[spec_name] = {}
        for outcome_name, outcome_var in outcomes.items():
            model = smf.ols(
                f"{outcome_var} ~ {term} + receiver_city + border_state + log_pop + C(state_name)",
                data=sub,
            ).fit(cov_type="HC3")
            out[spec_name][outcome_name] = {
                "beta": float(model.params.get(term, np.nan)),
                "t_stat": float(model.tvalues.get(term, np.nan)),
                "p_value": float(model.pvalues.get(term, np.nan)),
                "adj_r2": float(model.rsquared_adj),
                "n": int(model.nobs),
            }
    return out


def build_summary(models: pd.DataFrame, thresholds: pd.DataFrame, deciles: pd.DataFrame, receiver: dict[str, object], df: pd.DataFrame) -> dict[str, object]:
    def pick(outcome: str, model: str) -> dict[str, float]:
        row = models[(models["outcome"] == outcome) & (models["model"] == model)].iloc[0]
        return {
            "beta": float(row["beta"]),
            "t_stat": float(row["t_stat"]),
            "p_value": float(row["p_value"]),
            "adj_r2": float(row["adj_r2"]),
        }

    def pick_thresh(outcome: str, family: str, recent_q: int, capacity_q: float | None = None) -> dict[str, float]:
        mask = (
            (thresholds["outcome"] == outcome)
            & (thresholds["family"] == family)
            & (thresholds["recent_quantile"] == recent_q)
        )
        if capacity_q is None:
            mask &= thresholds["capacity_quantile"].isna()
        else:
            mask &= thresholds["capacity_quantile"] == capacity_q
        row = thresholds[mask].iloc[0]
        return {
            "beta": float(row["beta"]),
            "t_stat": float(row["t_stat"]),
            "p_value": float(row["p_value"]),
            "adj_r2": float(row["adj_r2"]),
        }

    d1 = deciles.iloc[0].to_dict()
    d10 = deciles.iloc[-1].to_dict()

    return {
        "sample_n": int(len(df)),
        "occupants_per_unit_assumption": OCCUPANTS_PER_UNIT,
        "recent_fb_per_permit_unit_median": float(df["recent_fb_per_permit_unit_w99"].median()),
        "recent_fb_per_permit_unit_q80": float(df["recent_fb_per_permit_unit_w99"].quantile(0.8)),
        "recent_fb_per_permit_unit_q90": float(df["recent_fb_per_permit_unit_w99"].quantile(0.9)),
        "margin_shift_models": {
            "stock_only": pick("margin_shift", "stock_only"),
            "flow_only": pick("margin_shift", "flow_only"),
            "load_only": pick("margin_shift", "load_only"),
            "combined": pick("margin_shift", "combined"),
            "high_load90": pick("margin_shift", "high_load90"),
        },
        "wkly_wage_models": {
            "stock_only": pick("wkly_wage_log_change", "stock_only"),
            "flow_only": pick("wkly_wage_log_change", "flow_only"),
            "load_only": pick("wkly_wage_log_change", "load_only"),
            "combined": pick("wkly_wage_log_change", "combined"),
            "high_load90": pick("wkly_wage_log_change", "high_load90"),
        },
        "net_migration_models": {
            "stock_only": pick("net_us_migration_share", "stock_only"),
            "flow_only": pick("net_us_migration_share", "flow_only"),
            "load_only": pick("net_us_migration_share", "load_only"),
            "combined": pick("net_us_migration_share", "combined"),
            "high_load90": pick("net_us_migration_share", "high_load90"),
        },
        "employment_models": {
            "stock_only": pick("employment_log_change", "stock_only"),
            "flow_only": pick("employment_log_change", "flow_only"),
            "load_only": pick("employment_log_change", "load_only"),
            "combined": pick("employment_log_change", "combined"),
            "high_load90": pick("employment_log_change", "high_load90"),
        },
        "threshold_grid_key_rows": {
            "margin_flow80_permit50": pick_thresh("margin_shift", "flow_x_permit", 80, 50),
            "wage_flow80_permit50": pick_thresh("wkly_wage_log_change", "flow_x_permit", 80, 50),
            "margin_flow90_permit25": pick_thresh("margin_shift", "flow_x_permit", 90, 25),
            "wage_flow90_permit25": pick_thresh("wkly_wage_log_change", "flow_x_permit", 90, 25),
            "margin_high_load90": pick_thresh("margin_shift", "load_threshold", 90, None),
            "wage_high_load90": pick_thresh("wkly_wage_log_change", "load_threshold", 90, None),
        },
        "load_decile_gap": {
            "D1": d1,
            "D10": d10,
            "margin_shift_gap_pp": float(d10["median_margin_shift_pp"] - d1["median_margin_shift_pp"]),
            "wkly_wage_gap_pp": float(d10["median_wkly_wage_change_pp"] - d1["median_wkly_wage_change_pp"]),
            "net_migration_gap_pp": float(d10["median_net_us_migration_share_pp"] - d1["median_net_us_migration_share_pp"]),
        },
        "receiver_2024": receiver,
        "load_robustness": load_robustness(df),
    }


def main() -> int:
    county = prepare_county()
    models = model_comparison(county)
    thresholds = threshold_grid(county)
    deciles = load_deciles(county)
    _, receiver_summary = receiver_descriptives()
    summary = build_summary(models, thresholds, deciles, receiver_summary, county)
    OUT_SUMMARY.write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))
    print(
        f"Wrote {OUT_SUMMARY}, {OUT_MODELS}, {OUT_THRESH}, {OUT_DECILES}, and {OUT_RECEIVER}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
