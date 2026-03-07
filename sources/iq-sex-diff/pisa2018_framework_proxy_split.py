from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path("/Users/alien/Projects/research/sources/iq-sex-diff")
DATA_DIR = ROOT / "data" / "pisa"

ITEM_PATH = DATA_DIR / "pisa2018_item_level_gaps.tsv"
MAP_PATH = DATA_DIR / "pisa2018_unit_framework_proxy.tsv"

UNIT_OUT = DATA_DIR / "pisa2018_framework_proxy_unit_summary.tsv"
CONTENT_OUT = DATA_DIR / "pisa2018_framework_proxy_content_summary.tsv"
CONTEXT_OUT = DATA_DIR / "pisa2018_framework_proxy_context_summary.tsv"
CONTENT_CONTEXT_OUT = DATA_DIR / "pisa2018_framework_proxy_content_context_summary.tsv"


def summarize(df: pd.DataFrame, group_cols: list[str]) -> pd.DataFrame:
    rows: list[dict[str, object]] = []
    for keys, sub in df.groupby(group_cols, observed=True):
        if not isinstance(keys, tuple):
            keys = (keys,)

        weights = sub["n_nonmissing"].astype(float).to_numpy()
        d = sub["country_weighted_mean_d"].astype(float).to_numpy()
        item_count = int(len(sub))
        unit_count = int(sub["unit_id"].nunique())
        male_items = int((d < 0).sum())
        female_items = int((d > 0).sum())

        row = {
            col: key for col, key in zip(group_cols, keys, strict=True)
        }
        row.update(
            {
                "items": item_count,
                "units": unit_count,
                "male_leaning_items": male_items,
                "female_leaning_items": female_items,
                "mean_item_d": float(np.nanmean(d)),
                "median_item_d": float(np.nanmedian(d)),
                "weighted_mean_item_d": float(np.average(d, weights=weights)) if weights.sum() > 0 else math.nan,
                "mean_abs_item_d": float(np.nanmean(np.abs(d))),
                "mean_low_conf_share": float((sub["confidence"] == "low").mean()),
            }
        )
        rows.append(row)

    return pd.DataFrame(rows).sort_values(group_cols).reset_index(drop=True)


def main() -> None:
    items = pd.read_csv(ITEM_PATH, sep="\t")
    proxy = pd.read_csv(MAP_PATH, sep="\t")

    merged = items.merge(proxy, on=["unit_id", "unit_label"], how="left", validate="many_to_one")
    merged["high_conf_proxy"] = merged["confidence"].isin(["medium", "high"])
    merged = merged.sort_values(["country_weighted_mean_d", "unit_id", "question_id"]).reset_index(drop=True)
    merged.to_csv(UNIT_OUT, sep="\t", index=False)

    content = summarize(merged, ["content_category"])
    context = summarize(merged, ["context_category"])
    content_context = summarize(merged, ["content_category", "context_category"])

    high_conf = merged[merged["high_conf_proxy"]].copy()
    content_high = summarize(high_conf, ["content_category"]).add_prefix("high_conf_")
    context_high = summarize(high_conf, ["context_category"]).add_prefix("high_conf_")
    content_context_high = summarize(high_conf, ["content_category", "context_category"]).add_prefix("high_conf_")

    content = content.merge(content_high, left_on="content_category", right_on="high_conf_content_category", how="left").drop(
        columns=["high_conf_content_category"]
    )
    context = context.merge(context_high, left_on="context_category", right_on="high_conf_context_category", how="left").drop(
        columns=["high_conf_context_category"]
    )
    content_context = content_context.merge(
        content_context_high,
        left_on=["content_category", "context_category"],
        right_on=["high_conf_content_category", "high_conf_context_category"],
        how="left",
    ).drop(columns=["high_conf_content_category", "high_conf_context_category"])

    content.to_csv(CONTENT_OUT, sep="\t", index=False)
    context.to_csv(CONTEXT_OUT, sep="\t", index=False)
    content_context.to_csv(CONTENT_CONTEXT_OUT, sep="\t", index=False)

    print(f"wrote {UNIT_OUT}")
    print(f"wrote {CONTENT_OUT}")
    print(f"wrote {CONTEXT_OUT}")
    print(f"wrote {CONTENT_CONTEXT_OUT}")


if __name__ == "__main__":
    main()
