# Failure catalog

## 2026-10-20: same-named transport module shadows the social lane

The profiled live command stopped with `ImportError: cannot import name 'build_roads'`
after another consumer's `v9_transport.py` occupied the import path/module cache.
The social route temporarily imports source helpers from sibling lane directories;
an unqualified import therefore did not identify the authoritative formula.

`v9_totals.load_transport()` now loads the exact sibling file and fails if its
resolved path or required entry point differs. The regression installs a hostile
same-named module and prepends the foreign directory, then verifies the local
formula is selected. Protected source lanes are unchanged. The failed profile is
retained in the handoff scratch; successful production and replay receipts belong
in RESULT.md.

## 2026-10-20: shared weight adapter now validates its input declaration

The sibling `population_basis.reweight()` gained a strict guard matching display
weights to their declared production weights times the calibration factor before
restoring the production frame. This caller's earlier manual reset changed only
one side and correctly failed `source_rank_calibration_declared` on the next run.
The social and post-law callers now pass the declared loader frame intact. The
source adapter restores production weights, and the consumer still applies its
own member calibration once after row4. The live-frame regression gates both the
located and complete counts to `meta.population_v9`. No shared-source guard was
weakened, and the peer's source file is unchanged by this worker.

## 2026-10-20: duplicate native congestion setup dominates the pairing run

The full profile took 167.055s; road transport plus the average comparator spent
80.955s and 62.303s in their source routes. They independently reconstructed the
same congestion inputs; native `match_umr` alone took 56.242s in the second setup.
The live driver now shares one bounded in-process source setup. The average arm
still copies exposures before changing its random-group keys; all source formulas
and source-file pins remain. No protected producer is edited. Full-output byte
comparison against the uncached construction and the official replay verify that
sharing changes no numerical or provenance output. Further optimization of the
native matching loop is outside these owned lanes.

## 2026-10-20: inherited v8 metadata mislabeled as the live v9 case

Spreading the entire oct15 band contract retained its package, capital rates,
item registry and population. The oct16 exporter now builds those declarations
from the native v9 payload and gates the single rate across specifications.
Historical congestion/social/alternative blocks in the totals are explicitly
under `inherited_oct15`; live CSV notes name v9. A regression checks the source
rate, registry, package, count and absence of historical blocks at the live level.
Native/flow band comparisons are independent gates; the resource split is a
definition, and no longer advertised as an independent empirical check.
