#!/usr/bin/env python3
"""Build frozen NLSY79 sibling pairs for Stage 0A and Experiment 2."""

from __future__ import annotations

import argparse
import csv
import zipfile
from collections import defaultdict
from pathlib import Path

from stage0_config import NLSY79


MISSING_CODES = {"", ".", "-1", "-2", "-3", "-4", "-5"}


def to_int(value: str) -> int | None:
    if value in MISSING_CODES:
        return None
    try:
        return int(value)
    except ValueError:
        return None


def nonmissing(values: dict[str, str], fields: list[str]) -> int:
    return sum(values.get(field, "") not in MISSING_CODES for field in fields)


def select_columns(header: list[str], wanted: list[str]) -> dict[str, int]:
    return {column: header.index(column) for column in wanted}


def load_rows() -> dict[int, dict[str, str]]:
    zipped = Path(NLSY79["path"])
    member = NLSY79["zip_member"]
    wanted = [
        NLSY79["id"]["code"],
        NLSY79["household_id"]["code"],
        NLSY79["sex"]["code"],
        NLSY79["race"]["code"],
        NLSY79["age"]["baseline"]["code"],
        NLSY79["age"]["asvab_proxy"]["code"],
        NLSY79["birth_order_proxy"]["code"],
        NLSY79["weights"]["cross_section_1979"]["code"],
        NLSY79["weights"]["asvab_1981"]["code"],
        "R0614900",
        "R0006500",
        "R0007900",
        "R0001800",
    ]
    wanted.extend(slot["id"] for slot in NLSY79["pair_link_slots"])
    wanted.extend(slot["relation"] for slot in NLSY79["pair_link_slots"])
    wanted.extend(slot["sibling_marker"] for slot in NLSY79["pair_link_slots"])
    wanted.extend(
        subtest["code"] for subtest in NLSY79["primary_subtests"].values()
    )

    rows: dict[int, dict[str, str]] = {}
    with zipfile.ZipFile(zipped) as archive:
        with archive.open(member) as raw:
            reader = csv.reader((line.decode("latin-1") for line in raw))
            header = next(reader)
            index = select_columns(header, wanted)
            for row in reader:
                caseid = to_int(row[index[NLSY79["id"]["code"]]])
                if caseid is None:
                    continue
                rows[caseid] = {column: row[position] for column, position in index.items()}
    return rows


def candidate_edges(rows: dict[int, dict[str, str]]) -> dict[frozenset[int], list[dict[str, int | None]]]:
    relation_codes = set(NLSY79["pair_rule"]["accept_relation_codes"])
    edges: dict[frozenset[int], list[dict[str, int | None]]] = defaultdict(list)
    id_code = NLSY79["id"]["code"]
    for caseid, values in rows.items():
        hhid = to_int(values[NLSY79["household_id"]["code"]])
        if hhid is None:
            continue
        for slot_no, slot in enumerate(NLSY79["pair_link_slots"], start=1):
            other_id = to_int(values[slot["id"]])
            relation = to_int(values[slot["relation"]])
            sibling_marker = to_int(values[slot["sibling_marker"]])
            if other_id is None or other_id == caseid or other_id not in rows:
                continue
            relation_is_sibling = relation in relation_codes
            marker_supports_sibling = sibling_marker is not None and sibling_marker > 0
            if not (relation_is_sibling or marker_supports_sibling):
                continue
            edges[frozenset({caseid, other_id})].append(
                {
                    "caseid": caseid,
                    "other_id": other_id,
                    "hhid": hhid,
                    "slot_no": slot_no,
                    "relation": relation,
                    "sibling_marker": sibling_marker,
                    "nonmissing_primary_subtests": nonmissing(
                        values,
                        [
                            subtest["code"]
                            for subtest in NLSY79["primary_subtests"].values()
                        ],
                    ),
                }
            )
    return edges


def age_gap_years(left: dict[str, str], right: dict[str, str]) -> int | None:
    primary = NLSY79["age"]["asvab_proxy"]["code"]
    fallback = NLSY79["age"]["baseline"]["code"]
    left_age = to_int(left[primary]) or to_int(left[fallback])
    right_age = to_int(right[primary]) or to_int(right[fallback])
    if left_age is None or right_age is None:
        return None
    return abs(left_age - right_age)


def build_pairs(rows: dict[int, dict[str, str]], max_age_gap: int, opposite_sex_only: bool) -> list[dict[str, str | int]]:
    pairs: list[dict[str, str | int]] = []
    sex_code = NLSY79["sex"]["code"]
    id_code = NLSY79["id"]["code"]
    hhid_code = NLSY79["household_id"]["code"]
    birth_order_code = NLSY79["birth_order_proxy"]["code"]
    edges = candidate_edges(rows)

    for pair_ids, evidence in edges.items():
        if len(evidence) < 2:
            continue
        left_id, right_id = sorted(pair_ids)
        left = rows[left_id]
        right = rows[right_id]
        left_hhid = to_int(left[hhid_code])
        right_hhid = to_int(right[hhid_code])
        if left_hhid is None or left_hhid != right_hhid:
            continue

        left_sex = to_int(left[sex_code])
        right_sex = to_int(right[sex_code])
        if left_sex is None or right_sex is None:
            continue
        if opposite_sex_only and left_sex == right_sex:
            continue

        gap = age_gap_years(left, right)
        if gap is not None and gap > max_age_gap:
            continue

        evidence = sorted(evidence, key=lambda item: item["slot_no"] or 99)
        female_caseid = left_id if left_sex == NLSY79["sex"]["female"] else right_id
        male_caseid = left_id if left_sex == NLSY79["sex"]["male"] else right_id

        pairs.append(
            {
                "pair_id": f"{left_id}-{right_id}",
                "hhid_1979": left_hhid,
                "caseid_low": left_id,
                "caseid_high": right_id,
                "female_caseid": female_caseid,
                "male_caseid": male_caseid,
                "sex_low": left_sex,
                "sex_high": right_sex,
                "age_gap_years": "" if gap is None else gap,
                "older_sibs_low": left[birth_order_code],
                "older_sibs_high": right[birth_order_code],
                "slot_low": evidence[0]["slot_no"],
                "slot_high": evidence[1]["slot_no"],
                "relation_low": "" if evidence[0]["relation"] is None else evidence[0]["relation"],
                "relation_high": "" if evidence[1]["relation"] is None else evidence[1]["relation"],
                "sibling_marker_low": ""
                if evidence[0]["sibling_marker"] is None
                else evidence[0]["sibling_marker"],
                "sibling_marker_high": ""
                if evidence[1]["sibling_marker"] is None
                else evidence[1]["sibling_marker"],
                "nonmissing_subtests_low": evidence[0]["nonmissing_primary_subtests"],
                "nonmissing_subtests_high": evidence[1]["nonmissing_primary_subtests"],
            }
        )

    return pairs


def reduce_one_pair_per_household(pairs: list[dict[str, str | int]]) -> list[dict[str, str | int]]:
    grouped: dict[int, list[dict[str, str | int]]] = defaultdict(list)
    for pair in pairs:
        grouped[int(pair["hhid_1979"])].append(pair)

    selected: list[dict[str, str | int]] = []
    for household_pairs in grouped.values():
        household_pairs.sort(
            key=lambda pair: (
                pair["age_gap_years"] == "",
                int(pair["age_gap_years"]) if pair["age_gap_years"] != "" else 999,
                -(
                    int(pair["nonmissing_subtests_low"])
                    + int(pair["nonmissing_subtests_high"])
                ),
                int(pair["caseid_low"]),
                int(pair["caseid_high"]),
            )
        )
        selected.append(household_pairs[0])
    return selected


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "-o",
        "--output",
        default=str(
            Path("sources/iq-sex-diff/data/nlsy/nlsy79_opposite_sex_sibling_pairs.tsv")
        ),
        help="Output TSV path",
    )
    parser.add_argument(
        "--max-age-gap",
        type=int,
        default=NLSY79["pair_rule"]["primary_max_age_gap_years"],
        help="Maximum allowed sibling age gap in years",
    )
    parser.add_argument(
        "--include-same-sex",
        action="store_true",
        help="Keep same-sex sibling pairs as well",
    )
    parser.add_argument(
        "--keep-all-pairs",
        action="store_true",
        help="Do not collapse to one pair per household",
    )
    args = parser.parse_args()

    rows = load_rows()
    pairs = build_pairs(
        rows,
        max_age_gap=args.max_age_gap,
        opposite_sex_only=not args.include_same_sex,
    )
    if not args.keep_all_pairs and NLSY79["pair_rule"]["primary_one_pair_per_household"]:
        pairs = reduce_one_pair_per_household(pairs)

    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "pair_id",
                "hhid_1979",
                "caseid_low",
                "caseid_high",
                "female_caseid",
                "male_caseid",
                "sex_low",
                "sex_high",
                "age_gap_years",
                "older_sibs_low",
                "older_sibs_high",
                "slot_low",
                "slot_high",
                "relation_low",
                "relation_high",
                "sibling_marker_low",
                "sibling_marker_high",
                "nonmissing_subtests_low",
                "nonmissing_subtests_high",
            ],
            delimiter="\t",
        )
        writer.writeheader()
        writer.writerows(pairs)

    print(f"Wrote {len(pairs)} pairs to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
