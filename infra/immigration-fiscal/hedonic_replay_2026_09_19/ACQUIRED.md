# Original Saiz–Wachter replication package

**Acquired:** 2026-09-19, via the operator's signed-in Chrome session after authorization to accept archive download terms. The completed ZIP passed CRC and SHA-256 checks before extraction. Raw files remain unchanged in ignored `_cache/original/`.

**Source:** Saiz, Albert, and Susan Wachter. *Replication data for: Immigration and the Neighborhood*. [openICPSR project114757,V1](https://www.openicpsr.org/openicpsr/project/114757/version/V1/view), [DOI10.3886/E114757V1](https://doi.org/10.3886/E114757V1). Article: [AEJ: Economic Policy3(2),169–188](https://www.aeaweb.org/articles?id=10.1257/pol.3.2.169).

| Object | Bytes | SHA-256 |
|---|---:|---|
| Downloaded `114757-V1.zip`, preserved as `_cache/original.zip` |41,152,145|`5315ad6e4118accafc94a0aad8fb923441c86ed6b21d5f8da75d44ee66e42a41`|
| `DATAAEJPOL2009-0191/DATAAEJPOLICY_MS_2009_191.dta` |105,273,639|`56ed0dcb0472cdeb75dd88a3938fbd32d831463bd696afda1cc6a765ffe5d833`|
| `DATAAEJPOL2009-0191/AEJPOLICY-MS2009-0191.do` |13,181|`07b6ce4cdb42b9ea3d4860b6561b871f818ea382400aebc15009899086a3a756`|
| `DATAAEJPOL2009-0191/AEJPOLICY-MS2009-0191-SUPPLEMENTAL-RESULTS.do` |9,156|`5b3d9a3da0b186ae5d77953314b4505936a41c5cf9901cf4bb212954a37cd237`|
| `DATAAEJPOL2009-0191/README_AEJpolicyMS2009-191.txt` |270|`3beeb48a281f3d6d0a78797e1ec4e6c1eb8d30a1c04ef84b918c5500a1ef4a81`|
| `LICENSE.txt` |14,974|`ee6cb3a4e20d54cbb5ce1ed04744c84ccf2342525367e5aec2ecb2f824eed6f0`|

The archive license assigns BSD-3-Clause to software and CC-BY4.0 to other objects, copyright2011 American Economic Association. Preserve the supplied license with the raw files. Authentication/download terms are distinct from those artifact licenses.

Dataset:102,766 rows×248 variables in Stata9 format;51,300 observations in1990 and51,466 in2000. `(tract,year)` is unique. The archive supplies a prepared analysis file, including `pull`, `pulli` and `pullmsa`; it does **not** supply the upstream Geolytics harmonization or gravity-construction code. The variable labels and both `.do` files are the local codebook.

Key fields: `dloval` log average-value change; `dlomval` log median-value change; `dforeigncap` foreign-born share change; `l1own` initial owner units; `msayear` MSA-period fixed-effect key; `tract` cluster key; `immicapmsa` metro inflow divided by initial population; `cha*` and `Ql1*` housing controls; initial socioeconomic controls and precomputed gravity instruments. Historical tract/MSA keys must not be joined directly to current ACS geographies without a validated crosswalk.

The actual baseline command expands to43 controls, while the paper describes44; the omitted field is `l1sharedrop`. Column3 also includes two land-use variables. Column1's archived command has34,835 observations; the published table says34,833. Appendix first stages use35,120 because their commands do not require a nonmissing house-value outcome. These differences are recorded in the [evidence note](../../../research/immigration-hedonic-replay-2026-09-19.md).
