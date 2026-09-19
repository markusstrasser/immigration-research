# Reproducible audit probes

These read existing local inputs and print the independent arithmetic behind the
[September 19 index](../../research/immigration-five-day-cross-check-2026-09-19.md).
Run from the repository environment:

```sh
UV_CACHE_DIR=/private/tmp/uv-immigration-audit OPENBLAS_NUM_THREADS=1 uv run --no-project python3 -B notes/audit-2026-09-19/fiscal_probe.py
UV_CACHE_DIR=/private/tmp/uv-immigration-audit uv run --no-project python3 -B notes/audit-2026-09-19/iv_scale_probe.py
```

The fiscal probe temporarily substitutes the existing person-source matrix in
memory; it does not call the principal generator's write path. Its JSON goes to
`/private/tmp/fiscal_audit_probe_20260919.json`. The IV probe independently fits
the stored metro panel with NumPy/pandas and varies only instrument scale.
Neither script writes principal analysis outputs. The numerical results are
recorded in the linked audit evidence notes; no derived data are committed here.
