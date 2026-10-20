# Failure catalog

## 2026-10-20: total back-cast files precede the component-history export

The military-history consumer was launched when `backcast_annual.csv` appeared,
before its required `case_parts_annual.csv` was exported. The first command exited
1 and published no history. Total-account files do not establish completion of
the typed source history. The consumer now explicitly requires both the component
metadata and annual component export, with a `[BLOCKED]` prerequisite message.
The regression supplies metadata without the annual file and verifies that the
consumer stops before parsing or publishing. The final command waits for the
upstream completed file and gates the source-line selection at 2024.

The first completed-source invocation then exposed a separate schema mismatch:
annual concepts are explicitly named `net_cost_cbo_informed_oct16_low/high`, while
the draft consumer matched the unsuffixed metadata concept. The selector now
requires both exact case-end names, unique part/rule principal rows, and2024
values within the source CSV's six-decimal precision of metadata anchors. Its
regression rejects a missing endpoint part and a changed principal value.

## 2026-10-20: rebuildable native export unnecessarily carried in derived

The 34.6 MB native frame is an intermediate read by social pairing, not an
independent source. It now rebuilds in `_cache/oct16/native_frame.json`; the
tracked `derived/oct16/native_frame_manifest.json` pins its bytes, size and live
source hashes. Python and JavaScript consumers reject a missing or changed
cache, and stale live sources. A regression checks same-size content corruption
as well as absent cache/manifest. Rebuild debt before social pairing in a clone.
