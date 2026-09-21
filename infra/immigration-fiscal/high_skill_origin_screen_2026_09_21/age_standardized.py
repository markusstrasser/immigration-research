"""Re-weight each birthplace's adult balance to the native age mix (two bands: 25-64, 65+).

The screen's headline is a snapshot at each group's own ages, which flatters young groups. This
reads `derived/origin_screen.csv` and writes `derived/origin_screen_native_ages.csv` with three
figures per origin and allocation, dollars per adult-year:
  own_ages          the screen's 25+ estimate
  native_age_mix    the group's own 25-64 and 65+ balances at the native 65+ share
  native_old_age    as above, but the group's 65+ balance replaced by the native 65+ balance
                    (a bound for cohorts who will hold full entitlements when old, unlike
                    today's immigrant elderly, many of whom arrived late in life)
Standard errors combine the two band errors as if independent: an approximation, because the
bands share the medical-spending covariance.
"""
import csv
import math
import sys
from pathlib import Path

DERIVED = Path(__file__).resolve().parent / "derived"
SHARE = "share_65_plus_of_adults"


def value(row, scope, kind="estimate"):
    text = row[f"net_per_person_{scope}_{kind}"]
    return float(text) if text not in {"", "nan"} else float("nan")


def main():
    rows = [r for r in csv.DictReader(open(DERIVED / "origin_screen.csv")) if r["education"] == "all"]
    out = []
    for allocation in sorted({r["allocation"] for r in rows}):
        group = {r["origin"]: r for r in rows if r["allocation"] == allocation}
        native = group["all_native"]
        old_share = float(native[SHARE])
        native_old = value(native, "65_plus")
        for origin, row in group.items():
            young, old = value(row, "25_64"), value(row, "65_plus")
            se_young, se_old = value(row, "25_64", "se_joint"), value(row, "65_plus", "se_joint")
            out.append({
                "origin": origin, "allocation": allocation,
                "share_65_plus_of_adults": float(row[SHARE]),
                "net_25_64": young, "net_65_plus": old,
                "own_ages": value(row, "25_plus"),
                "native_age_mix": (1 - old_share) * young + old_share * old,
                "native_age_mix_se_approx": math.hypot((1 - old_share) * se_young, old_share * se_old),
                "native_old_age": (1 - old_share) * young + old_share * native_old,
                "native_share_65_plus_used": old_share,
            })
    out.sort(key=lambda r: (r["allocation"], -r["native_age_mix"]))
    with open(DERIVED / "origin_screen_native_ages.csv", "w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        for row in out:
            writer.writerow({k: (f"{v:.4f}" if isinstance(v, float) else v) for k, v in row.items()})
    for allocation in ("personal", "shared"):
        print(f"\n  [{allocation}] dollars per adult-year")
        print(f"  {'origin':22} {'65+':>6} {'own ages':>9} {'native mix':>10} {'±se':>7} {'native old age':>14}")
        for r in out:
            if r["allocation"] == allocation:
                print(f"  {r['origin'][:22]:22} {r['share_65_plus_of_adults']:6.1%} {r['own_ages']:9,.0f} "
                      f"{r['native_age_mix']:10,.0f} {r['native_age_mix_se_approx']:7,.0f} {r['native_old_age']:14,.0f}")


if __name__ == "__main__":
    sys.exit(main())
