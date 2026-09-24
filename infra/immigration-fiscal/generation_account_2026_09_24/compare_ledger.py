"""Step 6: the September 19 ledger's generation figures beside this lane's, side by side, not scaled.

The ledger (`ledger_absolute_2026_09_17`) is read only through its own loader, lifetime.load_age_profiles,
which verifies the export's stored hashes and every input fingerprint before returning the age
profiles; complete_gaps.csv is then read as that lane's age_normalizations.py reads it. The ledger's
groups (mexico_born, mexican_second_gen, mexican_third_plus_selfid) keep children in their own
generation, so they meet this lane's convention (a); their populations must equal this lane's (gate).
One row per generation and allocation (shared = the adopted low end, personal = the high end), expanded
account, every figure a net balance in $ a year per person (negative = the group costs others), each
object in its own terms:
  ledger    published_gap         common-age gap to third-plus non-Hispanic whites, finer cells at the
                                  whites' ages (complete_gaps.csv; shared allocation only)
            gap_white_ages        the same gap from the export's eight age bands (must sit within 2% of
                                  the published one, the ledger's own verify() rule)
            gap_own_ages          the group's balance less the whites' at the group's own ages
            white_at_own_ages     the whites' age-specific balances weighted by the group's age bands
            own                   the group's own balance, no reference group
  account   proportional          direct fiscal lines, schools, other education and delayed services at
                                  average cost (the package's proportional reference), no production
                                  term, before corrections
            adopted_responses     the same lines at the adopted responses
            sept23                plus the production term (the September 23 case at the same spec)
            adopted               plus this generation's share of the 270 correction edits
The account columns come from run_generations.cjs (summary.ledger_bridge_a); nothing is converted from
one object to the other.
Output: derived/ledger_comparison.csv. Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/generation_account_2026_09_24/compare_ledger.py
"""
from __future__ import annotations

import sys

sys.dont_write_bytecode = True  # read-only imports from other lanes: write nothing beside them

import json  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import frame as F  # noqa: E402

LEDGER = F.FISCAL / "ledger_absolute_2026_09_17"
sys.path.insert(0, str(LEDGER))
from lifetime import load_age_profiles  # noqa: E402

GROUPS = {"G1": "mexico_born", "G2": "mexican_second_gen", "G3plus": "mexican_third_plus_selfid"}
WHITE = "third_plus_nh_white"
ACCOUNT = ["proportional", "adopted_responses", "sept23", "adopted"]


def main():
    profiles, fingerprints = load_age_profiles(F.ROOT)
    gaps = pd.read_csv(LEDGER / "derived/complete_gaps.csv").query("reference == @WHITE").set_index("group")
    summary = json.loads((F.OUT / "generation_summary.json").read_text())
    ours, bridge = summary["conventions"]["a"], summary["ledger_bridge_a"]
    ex = profiles[profiles.account == "expanded"]
    rows, fails = [], []
    for g, group in GROUPS.items():
        for allocation, end in [("shared", "low"), ("personal", "high")]:
            block = ex[(ex.allocation == allocation) & (ex.group == group)].set_index("band").sort_index()
            white = ex[(ex.allocation == allocation) & (ex.group == WHITE)].set_index("band").sort_index()
            pop = block.population.sum()
            if abs(pop / ours[g]["population"] - 1) > 1e-9:
                fails.append(f"{g} {allocation}: ledger population {pop:.1f} vs lane {ours[g]['population']:.1f}")
            gap_by_band = block.net_per_person - white.net_per_person
            b = bridge[g][end]
            parts = dict(proportional=b["proportional_fiscal_bn"], adopted_responses=b["adopted_responses_fiscal_bn"],
                         sept23=b["sept23_bn"], adopted=b["adopted_bn"])
            row = dict(generation=g, ledger_group=group, allocation=allocation, band_end=end, population=pop,
                       ledger_published_gap=float(gaps.loc[group, "complete_common_age_gap_per_person"])
                       if allocation == "shared" else np.nan,
                       ledger_gap_white_ages=(white.population * gap_by_band).sum() / white.population.sum(),
                       ledger_gap_own_ages=(block.population * gap_by_band).sum() / pop,
                       ledger_white_at_own_ages=(block.population * white.net_per_person).sum() / pop,
                       ledger_own=block.net_total.sum() / pop)
            row.update({f"account_{k}": -v * 1e9 / pop for k, v in parts.items()})
            row.update(ledger_own_bn=block.net_total.sum() / 1e9, **{f"account_{k}_bn": -v for k, v in parts.items()})
            rows.append(row)
    out = pd.DataFrame(rows)
    shared = out[out.allocation == "shared"]
    ratio = shared.ledger_gap_white_ages / shared.ledger_published_gap
    if not ratio.between(0.98, 1.02).all():
        fails.append(f"eight-band white-age gaps leave the published gaps: {ratio.round(4).tolist()}")
    if fails:
        sys.exit("✗ " + "; ".join(fails))
    out.to_csv(F.OUT / "ledger_comparison.csv", index=False, lineterminator="\n", float_format="%.6f")
    show = out.set_index(["generation", "allocation"])[
        ["ledger_published_gap", "ledger_gap_white_ages", "ledger_gap_own_ages", "ledger_white_at_own_ages",
         "ledger_own"] + [f"account_{k}" for k in ACCOUNT]].T.round(0)
    print(show.to_string())
    print(f"  ✓ ledger read through lifetime.load_age_profiles ({len(fingerprints)} fingerprinted files)")
    print("  ✓ ledger group populations equal this lane's convention (a) populations (1e-9)")
    print(f"  ✓ eight-band white-age gaps within 2% of the published gaps (ratios {ratio.round(4).tolist()})")


if __name__ == "__main__":
    main()
