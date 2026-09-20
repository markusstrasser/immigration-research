# MASP acquisition, 2026-09-20

Author's [project page](https://www.edwardtelles.com/masp) labels the download **2019 version**. Actual Stata file parses as **1,850 rows × 2,560 columns**. Rows are not a count of independent adult-child interviews; original, follow-up and child records/fields require reconstruction.

| File | Source URL | Bytes | SHA256 |
|---|---|---:|---|
| `raw/masp_combined.dta` | https://www.edwardtelles.com/s/masp_combined-3.dta | 16365775 | `3aeb2699940a41cfebf14e7f46ab3c76218f5f85ede68b9b8a1615c69e9b4aae` |
| `raw/codebook.zip` | https://www.edwardtelles.com/s/28481-0001-Codebookpdf-1.zip | 8186816 | `6d69fe9085b4959f9d612cd5e6d6dd7dab933205d27551b400046c33fe4e2f5a` |

ZIP CRC check passes; contains `ICPSR_28481/DS0001/28481-0001-Codebook.pdf`. This older ICPSR codebook is **not proof of equivalence** to the author-distributed 2019 file. ICPSR's confidentiality blanking and missing-code conventions must not be assumed identical. No respondent-level output or raw data committed; no redistribution license established. Public author download supports local research acquisition, not unrestricted republication.

Verified labels include `v75` own birth country; `c28/c29` nonrespondent parent's parents' birthplaces; `v25`, `v26...` and `v51` identity items; `v348` family income; `v338` SSI; schooling history `c80/c94/c95...`. The single-response `v25` is mostly missing and cannot alone classify identity; multiple-response items and skip rules need reconstruction. Immigration generation is not supplied as a verified ready-made field in this probe.

Source design: Mexican-American adults in Los Angeles/San Antonio, 1965–66, followed with surviving eligible original respondents and selected adult children in 1998–2002. Historical/local, selected survival and follow-up, no contemporary national representativeness. The [author's preliminary paper](https://paa2005.populationassociation.org/papers/51444) documents family-history generation classification and non-Mexican identity labels; its analytic sample is not identical to this raw row count.

Reproduce inventory: `UV_CACHE_DIR=/private/tmp/codex-uv-cache uv run --no-project --with pyreadstat python3 infra/immigration-fiscal/masp_2026_09_20/probe.py`. Raw/derived files ignored. Probe asserts observed data size, parses the Stata file, validates ZIP CRCs and exports field metadata; **no outcome analysis yet**.
