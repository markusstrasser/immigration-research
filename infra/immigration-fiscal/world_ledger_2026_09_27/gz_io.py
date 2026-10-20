"""Deterministic gzip for the lane's large tracked artifacts.

GitHub rejects a file over 100 MiB and the repo has no LFS. On 2026-10-20 the v9 run wrote a 259.5 MB
`reading_cells_cash_oct16.csv` and a 57 MB source-cell artifact; both now ship as gzip, the way the winners
lane ships `p7_cuts.csv.gz`. The stream carries no clock and no file name, so a rerun reproduces the bytes.
A pinned artifact's sha256 is taken over its decompressed content, so compression never changes a pin.
"""
import gzip
import io
from pathlib import Path


def gzip_bytes(body: bytes) -> bytes:
    raw = io.BytesIO()
    with gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream:
        stream.write(body)
    return raw.getvalue()


def write_csv_gz(frame, path, **kwargs):
    """Stream a frame to <name>.csv.gz without holding the CSV text in memory."""
    path = Path(path)
    if not path.name.endswith(".csv.gz"):
        raise SystemExit(f"[BLOCKED] gzip CSV output must end .csv.gz: {path.name}")
    with open(path, "wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as stream, \
            io.TextIOWrapper(stream, encoding="utf-8", newline="") as text:
        frame.to_csv(text, index=False, lineterminator="\n", **kwargs)


def read_artifact(path) -> bytes:
    """Content bytes of a pinned artifact: a .gz file is decompressed, any other file is read as is."""
    path = Path(path)
    body = path.read_bytes()
    return gzip.decompress(body) if path.suffix == ".gz" else body
