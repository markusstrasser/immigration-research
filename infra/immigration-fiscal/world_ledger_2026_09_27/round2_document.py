"""Generate every round-2 materiality verdict from executed delta CSV rows.

Native-First: render the lane's existing CSV outputs; no independent narrative
number registry or hard-coded materiality judgment.
"""
import argparse
from pathlib import Path
import pandas as pd

IDS = {
    "ownership": "R2D01,03,08,11,12,18,19,22–24,26,33,35,37,41",
    "prices": "R2D05,10,16,20,39",
    "g3_bounds": "R2D13,15,25,27,34,37,40",
    "capital_source": "R2D06,21,28–30,44,46,48",
    "remove_6b": "R2D02,04,07,09,14,17,31,32,36",
    "isn": "R2D47",
    "joint": "R2D38,43",
}
PARTS = ("world_total_bn", "mexico_residents_bn", "group_total_bn", "other_us_residents_bn")


def materiality_table(deltas):
    required = {"fix", "account_end", "g3_bound", "weighting", *(f"delta_{p}" for p in PARTS)}
    missing = required - set(deltas.columns)
    if missing:
        raise SystemExit(f"[BLOCKED] materiality input missing {sorted(missing)}")
    output = ["| fix | finding IDs | end | G3+ bound | weights | party | change, bn | $5bn bar |",
              "|---|---|---|---|---|---|---:|---|"]
    for row in deltas.itertuples():
        for part in PARTS:
            number = float(getattr(row, f"delta_{part}"))
            verdict = "over" if abs(number) >= 5 else "under"
            output.append(f"| {row.fix} | {IDS.get(row.fix, 'declared companion')} | {row.account_end} | "
                          f"{row.g3_bound} | {row.weighting} | {part} | {number:+.9f} | {verdict} |")
    return "\n".join(output)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    table = pd.read_csv(args.csv)
    for fix, subset in table.groupby("fix"):
        if set(subset.g3_bound) != {"zero", "upper"} or set(subset.account_end) != {"low", "high"}:
            raise SystemExit(f"[BLOCKED] incomplete endpoint/bound coverage for {fix}")
    text = "### Executed isolated and joint changes on v7 inputs\n\n"
    text += "Every bar verdict below is generated from the signed CSV value, using abs(change) >= 5. "
    text += "Each endpoint, G3+ bound, weighting and party is evaluated separately. "
    text += f"[CALCULATION: {args.csv}]\n\n"
    Path(args.out).write_text(text + materiality_table(table) + "\n")


if __name__ == "__main__":
    main()
