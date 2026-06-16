# Research provenance tags

Canonical tag vocabulary for new research outputs in this repo:

| Tag | Use |
|-----|-----|
| `[SOURCE: path-or-url]` | Retrieved document, memo, paper, official table, or cited page. |
| `[DATA]` | Local computed result, database query, script output, or table row; name the table, view, or command nearby. |
| `[INFERENCE]` | Logical synthesis from sourced/data premises; state the bridge if non-obvious. |
| `[FRAMING-SENSITIVE]` | Verdict depends on welfare function, perspective, or normative frame. |
| `[LIMIT]` | Scoped claim, boundary condition, or unresolved measurement/design limit. |
| `[TRAINING-DATA]` | Model recall not checked against a retrieved source. Avoid for load-bearing claims. |
| `[UNVERIFIED]` | Plausible but not checked; do not use as support for conclusions. |

For new work, prefer `[DATA]` over a separate `[DATABASE:]` tag and name the database/view in prose.
