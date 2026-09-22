# Project-local data and storage cleanup — September 20, 2026

The dataset tree now lives physically in this checkout's ignored `sources/`
directory. `~/research-data` is an inward-pointing alias for existing saved
commands. The original files retained their device/inode identities during the
move. Fourteen specifically used survey and supporting files were brought from
the sibling IQ project into `sources/reused-surveys/` as verified APFS clones.
The sibling originals remain available to that project.

The cleanup removed 8.765 GB of redundant extractions and failed downloads:
eight ACS extraction caches (8.159 GB), each matched by size and SHA-256 to a
member of a retained local source ZIP; one 123 MB truncated ACS2019 download;
and 15 failed acquisitions totaling 483 MB. Two of those 15 paths were replaced
by verified complete source clones (AHS and GFD); the other 13 were removed.
Sixty exact duplicate files (0.861 GB) now share APFS storage. All existing paths
and bytes were preserved; copy-on-write keeps subsequent writes independent.
Snapshots, raw originals, research outputs and cited validation evidence remain.

Four files totaling 0.822 GB were copied from the USB: ACS2019 person microdata,
BEA SAINC35, ACS2024 household microdata and the ACS2024 PDF dictionary. The first
two match historical pinned hashes; all four destination hashes match their USB
sources and both ZIPs passed full member CRC checks. The checked inputs no longer
require the USB. This is not a claim that the entire optional corpus was copied.

Full AHS2023 v1.0 and v1.1 archives were recovered from Census (283,574,972 bytes
combined); the full Government Finance Database archive was recovered from the
existing owned Modal volume (340,921,174 bytes). All member CRCs pass. GFD uses a
compression method unsupported by Python's standard ZIP reader, so `unzip -tqq`
performs its full check. Its documentation and classification manual are inside
the archive. AHS documentation remains in the enclave-quality lane's `_cache/`.

The stronger verifier exposed four previously misclassified optional acquisitions:
one BEA HTML response saved as ZIP, two NRC/NAP HTML responses saved as PDFs, and
an unrelated ZIP saved as the Lee–Miller PDF. They are now explicitly `blocked`
in the manifest. The three misleading paper responses are retained as evidence;
the unconsumed BEA error response was removed after recording its hash. The
older size-only pass of 148 files did not establish format validity.

Validation: the core required-plus-optional tier passes 144 available source
entries. ZIP verification checks central directories; acquisition checks all
member CRCs. PDFs receive a signature check and JSON files are parsed. These
checks do not establish source identity. Recovered/reused sources have separate
exact-content receipts. The unified warehouse remains readable with 121 catalog
objects and 366,808 catalogued rows. The path and acquisition regressions pass
23 tests, including relocation, explicit overrides, staged HTML rejection and
conditional error propagation. Native review found two path-override issues,
both fixed and tested; the separate archive-validator review found no regressions.

One incomplete ACS2013 archive remains for possible salvage: its first national
person member fails, while its second member and README pass full CRC. It must
not be treated as a complete national sample. Neither it nor the removed
2005/2010 fragments is used by the delivered estimates. The unfinished older-year
extension remains unfinished. The original gzip-wrapped surnames ZIP is also
preserved as source evidence alongside its validated unwrapped equivalent.

The final measured working footprint is **25.563 GB of logical file bytes**:
15.102 GB in `sources/`, 9.583 GB in analysis lanes, 0.625 GB in scratch/validation
evidence, 0.049 GB in warehouses and 0.204 GB in release packages. This includes
raw inputs, generated outputs, documentation and snapshots, counted once per
inode; APFS clones share underlying blocks, so it is not unique physical usage.
The roughly 70 source-family estimate and 270 static join/merge sites are separate
inventory measures, not file counts or runtime join counts.

Cleanup receipts, exact allowlists and file hashes are in the ignored
[`artifacts/storage-cleanup-2026-09-20/`](../artifacts/storage-cleanup-2026-09-20/).
Its `result.json` records an immediate free-space increase of 8.791 GB during the
first cleanup pass; later duplicate consolidation, truncated-file removal and
USB imports change the net footprint. APFS shared-block usage is not measured by
summing file sizes.

The initial clone attempt stopped before any replacement because macOS assigned
the clone a different group and protected per-inode provenance attribute. The
maintenance script was corrected to preserve owner/group, permissions, flags,
modification time and user xattrs while accepting the OS's new provenance marker.
A native clone probe verified metadata preservation and independent writes.

## 2026-09-21 follow-up

True extra copies removed (logical `du`, unique sources kept): GFD and AHS
v1.0 lane-cache clones (same SHA-256 as `sources/`), unzipped ACS 2024 CSVs
under `cultural_output/_cache/pums`, the QCEW 2,159-CSV extract, and the CCD
`.sas7bdat`. `ahs_analysis.py` now reads
`sources/.../ahs2023_flat_v1_0.zip`. `setup.sh` no longer unpacks QCEW.

The ACS 2013 `.part` was the official 616,326,250-byte zip plus a 90,112-byte
prefix; stripping the prefix left a same-size file whose first member still
failed CRC. A fresh `--http1.1` download passed `unzip -tqq`:
`csv_pus_2013.zip`, SHA-256
`414dad47774ae751209391cd83e4c88706488ca8a7dd4ac1c2faa4bf2d7cf2a1`.
3,132,795 person rows, weighted population 316,128,839, Mexico-born weighted
11,812,890.

ECLS-K:2011 is no longer idle: birthplace and teacher IDs are suppressed in
the microdata; an English-home NH-white kindergarten school-FE ELL association
is in `school_peer_checks_2026_09_20/derived/ecls_k2011_summary.json`.

Checkout `du` after this pass: **20 GB** (sources 12 GB, analysis lanes 6.4 GB).
