#!/usr/bin/env python3
"""Catalog staged public archive contents for quick dataset intake."""

from __future__ import annotations

import argparse
import csv
import zipfile
from pathlib import Path


TARGET_DIRS = [
    "nlscya",
    "ecls_k",
    "ecls_k2011",
    "hsls",
    "els",
    "nels",
]


def iter_archives(data_root: Path):
    for dirname in TARGET_DIRS:
        base = data_root / dirname
        if not base.exists():
            continue
        for path in sorted(base.glob("*.zip")):
            yield dirname, path


def build_catalog(data_root: Path) -> tuple[list[dict[str, object]], list[dict[str, object]]]:
    detail_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for dirname, archive_path in iter_archives(data_root):
        with zipfile.ZipFile(archive_path) as zf:
            infos = zf.infolist()
            summary_rows.append(
                {
                    "dataset_dir": dirname,
                    "archive": archive_path.name,
                    "member_count": len(infos),
                    "archive_bytes": archive_path.stat().st_size,
                }
            )
            for info in infos:
                detail_rows.append(
                    {
                        "dataset_dir": dirname,
                        "archive": archive_path.name,
                        "member": info.filename,
                        "member_bytes": info.file_size,
                        "compressed_bytes": info.compress_size,
                    }
                )
    return summary_rows, detail_rows


def write_tsv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()), delimiter="\t")
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", default="data")
    parser.add_argument(
        "--summary-out",
        default="data/public_archive_summary.tsv",
    )
    parser.add_argument(
        "--detail-out",
        default="data/public_archive_catalog.tsv",
    )
    args = parser.parse_args()

    data_root = Path(args.data_root).resolve()
    summary_rows, detail_rows = build_catalog(data_root)
    write_tsv(Path(args.summary_out).resolve(), summary_rows)
    write_tsv(Path(args.detail_out).resolve(), detail_rows)
    print(f"summary_rows={len(summary_rows)} detail_rows={len(detail_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
