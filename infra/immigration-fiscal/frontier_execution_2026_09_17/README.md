# Frontier execution — 2026-09-17

**Verdict:** The six proposed workstreams were pursued. New survey estimates and an official variance benchmark pass independent checks; policy replication and local incidence remain partial at explicitly recorded access/identification limits. Read the [integrated findings](../../../research/immigration-frontier-execution-2026-09-17.md) first.

## Coverage and results

| Workstream | Executed | Remaining limit |
|---|---|---|
| Score units and selection | [NLS](nlsy/RESULT.md): primary Table 8 units; official AFQT mean/SE; family classification and retention sensitivities | Public self-ID and generic birthplace cannot reproduce restricted Mexico-specific ancestry. |
| Descendant outcomes | NLS adult education/wages and common-age arrest/incarceration; [social](social/RESULT.md) three-year CPS disability and corrected GSS trust | Crime cells remain small; cross-sectional generations are not a family trajectory. |
| Policy comparison | [Policy](policy/RESULT.md): H-2B final tables; raw Bracero wage reconstruction, independent solver and mirror hashes | H-2B raw access; Bracero official identity and failed employment sample matching. |
| Local incidence | [NYC](local/RESULT.md): fiscal-year expenditure/census exposure, alternative series, published homelessness arithmetic | Monthly census-days approximate actual exposure. Outcomes of incumbents and shelter leavers remain unmeasured. |
| Cumulative mechanism | Danzer count coefficients, scaling, covariance-conservative geometric-ratio calculation | No cumulative patent-count/stock estimate without fitted counterfactuals and joint covariance. |
| Transfer and rival explanations | CPS sex/cohort checks; [institutions/contact/environment](social/institutions-environment.md); [Swiss access attempt](social/swiss/RESULT.md); [fiscal reconciliation](fiscal/RESULT.md) | No single overall welfare score, immutable group mechanism, or new all-domain causal estimate. |

Previous supplied archives are accounted for in the [named library](../new_datasets_2026_09_17/library/README.md). ICPSR documentation-only downloads remain documentation; additional copies do not create respondents. Pew/LNS, fertility and agglomeration retain their earlier audited status. This lane makes no new estimates from those sources.

## Inputs, storage and joins

- Raw inputs are read-only. New public NYC inputs are in ignored `raw/local/`; Swiss source snapshots in `raw/swiss/`; policy snapshots in `policy/raw/`. Participant-level derived tables are ignored under `derived/` or `policy/derived/`.
- NLS extraction streams the held full 1997–2023 archive in the sibling IQ project. Archive SHA256: `8c513e4804e5b07fce0e6b913258747dcf8707c73bb9ae54cce88dbff6d23c28`. The 806-field, 8,984-row CSV hashes to `422b0964b568c60a5a9da6139ee6dc31ffc14a5a02dcae3e059f8809495bac3b`. Exact respondent IDs join earlier family/base rows and the adult profile cache; four overlapping adult variables must agree.
- CPS ASEC 2024, 2025 and 2026 use their own 161 weight columns and validated one-to-one person/replicate joins. Person IDs remain 22-character strings. Cross-year overlap is diagnosed, not treated as independent replication or a validated longitudinal panel.
- GSS uses its held source cache with original design fields and preferred nonresponse weights where available. Provenance hashes are emitted alongside results.
- NYC source URLs, retrieval dates, byte counts and hashes are in [source_manifest.json](local/source_manifest.json). Two official census charts disagree beyond rounding; both are preserved. School tabs end earlier and are not sufficient for an exposure/outcome analysis.
- Policy sources and hashes are in [manifest.json](policy/manifest.json), [epoch2-sources.json](policy/epoch2-sources.json) and [epoch2-manifest.json](policy/epoch2-manifest.json). Bracero is explicitly a verified third-party mirror, not a verified official-data copy.
- These surveys cannot be joined person-to-person across studies. Cross-study comparison requires harmonized definitions and independent evidence claims; only within-study IDs support respondent linkage.

## Reproduction

Run from the repository root. The repository environment has pandas, NumPy, pyarrow, requests and BeautifulSoup, but does not currently contain scipy/statsmodels. Standard reproducible environments can be requested with `uv run --no-project --with pandas --with numpy --with pyarrow --with scipy --with statsmodels --with requests --with beautifulsoup4 python3 SCRIPT`. Do not silently replace missing dependencies or change raw sources.

```sh
export UV_CACHE_DIR=/private/tmp/immigration-uv-cache
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/local/stage.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/local/analyze.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/fiscal/reconcile.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/social/probe.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/social/analyze_social.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/social/validate.py
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/nlsy/extract.py
```

The successful offline NLS execution reused an already installed scipy without modifying the repository environment:

```sh
uv run python3 -c 'import sys,runpy; sys.path.append("/Users/alien/.cache/uv/archive-v0/AUlzts5NxEUozS_J/lib/python3.13/site-packages"); runpy.run_path("infra/immigration-fiscal/frontier_execution_2026_09_17/nlsy/analyze.py",run_name="__main__")'
uv run python3 infra/immigration-fiscal/frontier_execution_2026_09_17/nlsy/verify.py
```

That machine-specific cache path is an execution record, not a permanent dependency location. On another machine use the explicit environment above. Policy execution, from the `policy/` directory:

```sh
UV_CACHE_DIR=/private/tmp/immigration-frontier-execution/policy/.uv-cache uv run --no-project --offline --with pandas --with numpy --with statsmodels python3 replicate_bracero_danzer.py
uv run --no-project python3 reproduce.py
uv run --no-project python3 verify.py
uv run --no-project python3 summarize_epoch2.py
```

Policy versions actually used: Python 3.13.6, NumPy 2.5.3, pandas 3.0.5, scipy 1.18.1, statsmodels 0.15.0. The offline command assumes the retained cache. Public PDF text extraction requires `pdftotext`. Swiss acquisition requires a new empty `--output-dir`; its failed retrievals remain failed and no Swiss regression is claimed.

## Validation actually completed

- NLS principal benchmark: official AFQT mean 50.410 and SE 0.638 reproduced; all 8,984 IDs and four adult source fields agree; 632 independent scalar checks pass.
- CPS: 468 annual cells, 390 contrasts and 286 equal-year pooled comparisons independently checked, with SDR replicate variance and no independence assumption across overlapping annual samples. GSS: 40 coefficient/SE and 24 proportion/SE checks pass.
- NYC: 13 source hashes and budget table anchors checked; symmetric spending/exposure decomposition reconciles exactly. The source-chart discrepancy remains explicit, not converted to a PASS claim.
- Fiscal: all 12 held group/allocation accounts reconcile to their seven components; no new fiscal causal estimate or SE is claimed.
- Policy: H-2B table arithmetic independently checked; four Bracero wage coefficients/sample sizes match primary working-paper anchors, and FWL independently matches the fitted coefficients. Domestic employment does not match. All 11 Danzer annual coefficient/SE pairs match the primary supplement.
- Acquisition regression: a valid binary PDF succeeds exactly once; HTML masquerading as PDF fails loudly, tested offline against the actual script. The historical Swiss access failure remains unchanged.

Source PDFs and codebooks, rather than model agreement, govern interpretation. See [review record](REVIEW.md) for the bounded code check and retained limitations.
