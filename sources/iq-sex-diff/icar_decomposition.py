#!/usr/bin/env python3
"""First-pass ICAR domain decomposition under the frozen Stage -1 / 0A rules."""

from __future__ import annotations

import csv
import math
from pathlib import Path

from stage0_config import ICAR, ICAR_COMPOSITE_GRID


MISSING = {"", "NA"}


def mean(values: list[float]) -> float:
    return sum(values) / len(values)


def sample_variance(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mu = mean(values)
    return sum((value - mu) ** 2 for value in values) / (len(values) - 1)


def pooled_sd(female: list[float], male: list[float]) -> float | None:
    if len(female) < 2 or len(male) < 2:
        return None
    vf = sample_variance(female)
    vm = sample_variance(male)
    numerator = ((len(female) - 1) * vf) + ((len(male) - 1) * vm)
    denominator = len(female) + len(male) - 2
    if denominator <= 0 or numerator <= 0:
        return None
    return math.sqrt(numerator / denominator)


def cohens_d(female: list[float], male: list[float]) -> float | None:
    psd = pooled_sd(female, male)
    if psd in (None, 0):
        return None
    return (mean(female) - mean(male)) / psd


def min_items_required(items: list[str]) -> int:
    # The public SAPA release uses planned missingness; MR and R3D top out at
    # four administered items in this file, so a proportional threshold would
    # zero out the domains. Freeze the minimum at three scored items instead.
    return 3


def domain_score(row: dict[str, str], items: list[str]) -> float | None:
    values = [int(row[item]) for item in items if row[item] in {"0", "1"}]
    if len(values) < min_items_required(items):
        return None
    return sum(values) / len(values)


def load_records() -> list[dict[str, float | str]]:
    path = Path(ICAR["path"])
    records: list[dict[str, float | str]] = []
    with path.open("r", encoding="latin-1") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            sex = row[ICAR["sex"]["code"]].strip().lower()
            if sex not in {"male", "female"}:
                continue
            record: dict[str, float | str] = {"sex": sex}
            for domain, items in ICAR["domains"].items():
                record[domain] = domain_score(row, items)
            records.append(record)
    return records


def z_standardize(records: list[dict[str, float | str]], field: str) -> tuple[float, float]:
    values = [float(record[field]) for record in records if record[field] is not None]
    mu = mean(values)
    sd = math.sqrt(sample_variance(values))
    if sd == 0:
        sd = 1.0
    for record in records:
        if record[field] is None:
            continue
        record[f"{field}_z"] = (float(record[field]) - mu) / sd
    return mu, sd


def summarize_score(
    records: list[dict[str, float | str]], score_name: str, field: str
) -> dict[str, str | float | int]:
    female = [
        float(record[field])
        for record in records
        if record["sex"] == "female" and record.get(field) is not None
    ]
    male = [
        float(record[field])
        for record in records
        if record["sex"] == "male" and record.get(field) is not None
    ]
    d = cohens_d(female, male)
    return {
        "score_name": score_name,
        "n_female": len(female),
        "n_male": len(male),
        "female_mean": round(mean(female), 6),
        "male_mean": round(mean(male), 6),
        "d_female_minus_male": "" if d is None else round(d, 6),
    }


def build_composite_scores(records: list[dict[str, float | str]]) -> None:
    for domain in ICAR["domains"]:
        z_standardize(records, domain)

    for composite_name, weights in ICAR_COMPOSITE_GRID.items():
        for record in records:
            components = []
            for domain, weight in weights.items():
                value = record.get(f"{domain}_z")
                if value is None:
                    components = []
                    break
                components.append(weight * float(value))
            record[composite_name] = None if not components else sum(components)


def main() -> int:
    records = load_records()
    build_composite_scores(records)

    rows: list[dict[str, str | float | int]] = []
    for domain in ICAR["domains"]:
        rows.append(summarize_score(records, domain, domain))
    for composite_name in ICAR_COMPOSITE_GRID:
        rows.append(summarize_score(records, composite_name, composite_name))

    output_path = Path("sources/iq-sex-diff/data/icar_first_pass.tsv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "score_name",
                "n_female",
                "n_male",
                "female_mean",
                "male_mean",
                "d_female_minus_male",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(rows)

    print("ICAR first pass")
    print("Negative d = male advantage | Positive d = female advantage")
    for row in rows:
        print(
            f"{row['score_name']:<16} "
            f"n_f={row['n_female']:<6} "
            f"n_m={row['n_male']:<6} "
            f"d={row['d_female_minus_male']}"
        )
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
