#!/usr/bin/env python3
"""Independent full-weight arithmetic and earnings-tail diagnostic from raw CSVs."""
import json
import zipfile
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
audit = json.loads((ROOT / "derived/audit.json").read_text())
parts = []
columns = ["A_AGE", "A_SEX", "PRPERTYP", "PRCITSHP", "PENATVTY", "PEFNTVTY",
           "PEMNTVTY", "PEHSPNON", "PRDTRACE", "MARSUPWT", "A_HGA", "A_LFSR",
           "POV_UNIV", "PERLIS", "PEARNVAL"]
for source in audit["sources"]:
    year = source["year"]
    with zipfile.ZipFile(source["path"]) as archive:
        frame = pd.read_csv(archive.open(f"pppub{year % 100}.csv"), usecols=columns)
    frame = frame.loc[frame.A_AGE.between(25, 54) & frame.PRPERTYP.eq(2)].copy()
    frame["year"] = year
    frame["weight"] = frame.MARSUPWT / 100
    frame["earnings"] = frame.PEARNVAL * audit["cpi"]["2025"] / audit["cpi"][str(year - 1)]
    frame["band"] = list(zip((frame.A_AGE - 25) // 10, frame.A_SEX))
    parts.append(frame)
data = pd.concat(parts, ignore_index=True)
reference = data.PENATVTY.eq(57) & data.PEFNTVTY.eq(57) & data.PEMNTVTY.eq(57) & data.PEHSPNON.eq(2) & data.PRDTRACE.eq(1)
target = data.loc[reference & data.year.eq(2025)].groupby("band").weight.sum()
target /= target.sum()
target_lookup = target.to_dict()
published = pd.read_csv(ROOT / "derived/levels.csv")
published = published.loc[(published.scope == "age25_54") & (published.standard == "age_sex_standardized")]
records, tails, skipped = [], [], []
groups = {"white_us_parents": reference}
for code, country in audit["countries"].items():
    groups[f"g2_{country}"] = data.PENATVTY.eq(57) & (data.PEFNTVTY.eq(int(code)) | data.PEMNTVTY.eq(int(code)))
for name, mask in groups.items():
    group = data.loc[mask].copy()
    if group.empty or set(group.band) != set(target.index):
        skipped.append(dict(group=name, reason="No records or an empty full-weight age/sex stratum"))
        continue
    for metric, value, valid in [
        ("ba", group.A_HGA.ge(43), np.ones(len(group), dtype=bool)),
        ("employment", group.A_LFSR.isin([1, 2]), np.ones(len(group), dtype=bool)),
        ("poverty", group.PERLIS.eq(1), group.POV_UNIV.eq(1)),
        ("earnings_2025usd", group.earnings, np.ones(len(group), dtype=bool)),
    ]:
        group["value"] = value
        cells = group.loc[valid].groupby("band").apply(lambda cell: np.average(cell.value, weights=cell.weight))
        estimate = float((cells * target).sum())
        match = published.loc[(published.group == name) & (published.metric == metric)]
        if match.empty:
            skipped.append(dict(group=name, metric=metric, reason="Published estimator suppressed a required replicate denominator"))
            continue
        assert len(match) == 1, (name, metric, "Duplicate published key")
        error = estimate - match.iloc[0].estimate
        # Public main weights are rounded to cents; replicate-zero has finer precision.
        tolerance = .1 if metric == "earnings_2025usd" else 1e-5
        assert abs(error) < tolerance, (name, metric, estimate, error)
        records.append(dict(group=name, metric=metric, independent_estimate=estimate, difference=error))
    cell_weights = group.groupby("band").weight.sum().to_dict()
    group["standard_weight"] = [weight * target_lookup[band] / cell_weights[band]
                                 for weight, band in zip(group.weight, group.band)]
    ordered = group.sort_values("earnings")
    median = float(ordered.loc[ordered.standard_weight.cumsum().ge(.5), "earnings"].iloc[0])
    mean = float((group.earnings * group.standard_weight).sum())
    max_share = float((group.earnings * group.standard_weight).max() / mean) if mean > 0 else None
    cap = float(ordered.loc[ordered.standard_weight.cumsum().ge(.99), "earnings"].iloc[0])
    capped = float((group.earnings.clip(upper=cap) * group.standard_weight).sum())
    tails.append(dict(group=name, median_earnings=median, mean_earnings=mean,
                      highest_record_share_of_total_earnings=max_share,
                      p99_cap=cap, mean_capped_at_group_p99=capped))
expected_rows = published.loc[published.group.isin(groups) & published.metric.isin(["ba", "employment", "poverty", "earnings_2025usd"])]
expected = set(zip(expected_rows.group, expected_rows.metric))
checked = {(row["group"], row["metric"]) for row in records}
assert {("white_us_parents", metric) for metric in ["ba", "employment", "poverty", "earnings_2025usd"]} <= checked
assert expected == checked, ("Incomplete independent verification", expected - checked, checked - expected)
(ROOT / "derived/independent_raw_coverage.json").write_text(json.dumps(dict(expected=len(expected), checked=len(checked), skipped=skipped), indent=2) + "\n")
pd.DataFrame(records).to_csv(ROOT / "derived/independent_raw_checks.csv", index=False)
pd.DataFrame(tails).to_csv(ROOT / "derived/earnings_tail_diagnostics.csv", index=False)
print(f"PASS: {len(records)} independent raw estimates, {len(tails)} tail diagnostics")
