# Validation audit: GSS baseline and SNAP state prediction

**Verdict:** The existing auxiliary education transition model predicts later
parent-link-weighted schooling distributions better than a frozen training
distribution in eight of nine overlapping frame/group comparisons. It loses for
second-generation respondents in the pre2021 English frame. No supported
Mexican-specific comparison exists. A new pooled SNAP reporting correction
worsens dollar-weighted state prediction despite reducing aggregate bias.
Neither diagnostic validates fiscal projections or changes the account.

The [audit memo](../../../research/immigration-validation-and-backtesting-2026-09-28.md)
places this diagnostic beside existing external and held-out checks.

`gss_baseline.py` reads the prior lane's `gss_transition_cells.csv` and
`gss_temporal_prediction.csv`; raw microdata and the upstream engine are unchanged.
It reconstructs both the reported predictions and observations from the cells
before scoring. It fails on unsupported/partial categories, invalid probabilities
or a mismatch to the upstream prediction. Previously unsupported Mexican-origin
rows remain explicit skips, rather than fabricated zero-error rows.

The naive prediction weights training transition cells by training parent-link
weights. The model instead uses held-out parent-link weights; later parental
composition is therefore known, not forecast. Error is total variation between
the observed and predicted three-category schooling distributions, multiplied by
100 to give percentage points. Both predictions use the same evaluation sample.

All three upstream frames are reported: English-only, English-only through2018
(named `english_only_pre2021` upstream), and all available interview languages.
This baseline was selected after the original results were known. It is a
retrospective diagnostic without design-based uncertainty or a prospective claim.
Input and generator SHA256s are saved with the ignored derived JSON.

```sh
UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/validation_audit_2026_09_28/gss_baseline.py
```

The primary English-only errors are model/naive 4.59/5.67pp (G2), 2.80/5.16pp
(G3), and 3.39/9.24pp (G4+). The contrary pre2021 G2 result is 3.29/2.72pp.
The script's cell reconstruction passed on September28; no other legacy analysis
builder was rerun for this audit.

## SNAP common-correction transport

`snap_loso.py` reuses the administrative-benefit lane's CPS state arrays, QC
benefit-dollar shares and prior validity screen. For each held-out state, it fits
on the 25 other valid state/DC jurisdictions. If A is the QC dollar weight, h the raw CPS share and
a the imputed QC share, the training correction is
`rho = odds(sum(A*h)/sum(A)) / odds(sum(A*a)/sum(A))`. The held-state prediction is
`h / (rho*(1-h)+h)`. The held-state administrative ethnicity share is excluded
from fitting rho; its pre-existing validity-screen classification remains used.

All 26 valid jurisdictions (including DC) are scored, with every residual retained. Point shares are
reconstructed from the CPS arrays and checked against their exported table.
Support, finite-value, positive-dollar and share-domain guards fail loudly.
The 17-state subset with at least 30 raw Hispanic records is an additional
descriptive score of the same predictions, not a separately refitted model.

```sh
OPENBLAS_NUM_THREADS=1 UV_CACHE_DIR=/private/tmp/immigration-audit-uv-cache uv run --no-project python3 infra/immigration-fiscal/validation_audit_2026_09_28/snap_loso.py
```

| Benefit-dollar-weighted error, percentage points | Raw CPS | Pooled correction |
|---|---:|---:|
| Mean absolute error | 5.1626 | 5.6882 |
| Root mean square error | 8.1301 | 8.7879 |
| Mean signed error | +1.0281 | −0.1882 |

Twenty jurisdictions improve and six worsen. Florida's error moves from −14.00 to −17.47pp;
California from +0.089 to −1.753pp. The higher-support subset's MAE also worsens,
5.4184→6.1073pp. No significance or interval-coverage claim is made; neither
survey-design uncertainty nor unknown-ethnicity uncertainty is propagated here.

This tests a new common-rho rule, **not the adopted BV direct-administrative key**.
The data, estimand and outcome-informed validity screen were previously inspected;
this is not a pristine prospective holdout. QC shares distribute dollars over
benefit participants; CPS shares use SPM-unit members. Scoring weights are QC's
reported FYWGT×FSBEN dollar sums, not asserted annual budget amounts. Hispanic
ethnicity is broader than the account's Mexican-origin union.

The ignored outputs are `derived/snap_loso.csv` (every state and denominator),
`.json` (summary), and `.method.json` (equation, scope and hashes).
