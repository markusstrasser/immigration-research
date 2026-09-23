"""Stage ACS 2022-2024 one-year person PUMS (adults 17+) as Parquet for the service lane.

Reads the three national person ZIPs already on disk (read-only), keeps the fields the lane
uses plus the 80 person replicate weights, and writes `_cache/acs{year}_persons.parquet`.
`MIL` is asked of persons 17 and over, so younger records are dropped. Group-quarters persons
(barracks, dormitories, prisons) are kept; `RELSHIPP` 37/38 marks them. The ZIP hashes and
row counts go to `derived/acs_inputs.json` so a rebuild can be checked against this one.
"""
import hashlib
import json
import sys
import zipfile
from pathlib import Path

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pv
import pyarrow.parquet as pq

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
CACHE, DERIVED = HERE / "_cache", HERE / "derived"
DATA = ROOT / "sources/immigration-fiscal/data"
ZIPS = {
    2022: DATA / "external/acs_pums_years/csv_pus_2022.zip",
    2023: DATA / "census/acs_pums_2023_person.zip",
    2024: DATA / "external/acs_pums_2024_1yr/csv_pus.zip",
}
REPLICATES = [f"PWGTP{i}" for i in range(1, 81)]
TYPES = {
    "SERIALNO": pa.string(), "SPORDER": pa.int16(), "PUMA": pa.int32(), "DIVISION": pa.int8(),
    "PWGTP": pa.int32(), "AGEP": pa.int16(), "SEX": pa.int8(), "CIT": pa.int8(),
    "NATIVITY": pa.int8(), "POBP": pa.int16(), "HISP": pa.int8(), "ANC1P": pa.int16(),
    "ANC2P": pa.int16(), "RAC1P": pa.int8(), "RAC2P": pa.int16(), "RACASN": pa.int8(),
    "SCHL": pa.int8(), "MIL": pa.int8(), "MLPA": pa.int8(), "OCCP": pa.int16(), "ESR": pa.int8(),
    "RELSHIPP": pa.int8(), "PINCP": pa.int64(), "ADJINC": pa.int64(), "POVPIP": pa.int16(),
    "YOEP": pa.int16(), "WAOB": pa.int8(),
    **{name: pa.int32() for name in REPLICATES},
}


def sha256(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1 << 22), b""):
            digest.update(block)
    return digest.hexdigest()


def read_member(archive, member, state_field):
    types = dict(TYPES, **{state_field: pa.int8()})
    options = pv.ConvertOptions(column_types=types, include_columns=list(types), strings_can_be_null=True)
    with archive.open(member) as handle:
        reader = pv.open_csv(handle, read_options=pv.ReadOptions(block_size=1 << 26), convert_options=options)
        batches, rows = [], 0
        for batch in reader:
            rows += batch.num_rows
            keep = pc.greater_equal(batch.column("AGEP"), 17)
            batches.append(batch.filter(keep))
    table = pa.Table.from_batches(batches)
    if state_field != "ST":
        table = table.rename_columns(["ST" if name == state_field else name for name in table.column_names])
    return table, rows


def main():
    CACHE.mkdir(exist_ok=True)
    DERIVED.mkdir(exist_ok=True)
    manifest_path = DERIVED / "acs_inputs.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for year, path in ZIPS.items():
        target = CACHE / f"acs{year}_persons.parquet"
        entry = manifest.get(str(year), {})
        if target.exists() and entry.get("parquet_rows"):
            print(f"  = {year}: cached ({entry['parquet_rows']:,} rows)")
            continue
        with zipfile.ZipFile(path) as archive:
            header = archive.open("psam_pusa.csv").readline().decode().strip().split(",")
            state_field = "ST" if "ST" in header else "STATE"
            parts, total = [], 0
            for member in ("psam_pusa.csv", "psam_pusb.csv"):
                table, rows = read_member(archive, member, state_field)
                parts.append(table)
                total += rows
                print(f"  . {year} {member}: {rows:,} records, {table.num_rows:,} aged 17+", flush=True)
        table = pa.concat_tables(parts).combine_chunks()
        pq.write_table(table, target, compression="zstd")
        manifest[str(year)] = {
            "zip": str(path.relative_to(ROOT)), "zip_bytes": path.stat().st_size, "zip_sha256": sha256(path),
            "person_records": total, "parquet_rows": table.num_rows,
            "weighted_17plus": int(pc.sum(table.column("PWGTP")).as_py()),
        }
        manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
        print(f"  ✓ {year}: {table.num_rows:,} rows -> {target.name}", flush=True)


if __name__ == "__main__":
    sys.exit(main())
