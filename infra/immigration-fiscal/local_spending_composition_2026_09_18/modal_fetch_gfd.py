"""Fetch the 341 MB Government Finance Database from Google Drive via Modal.

Google Drive throttles the laptop to ~35 kB/s (3+ hours to completion); a
container usually gets full speed. Run:  modal run modal_fetch_gfd.py
The file lands in the `gfd` volume. Canonical local copy:
`sources/immigration-fiscal/data/external/government_finance_database/gfd_entire.zip`.
Do not clone it into this lane's `_cache/`.
"""
import modal

app = modal.App("gfd-fetch")
image = modal.Image.debian_slim().pip_install("gdown")
vol = modal.Volume.from_name("gfd", create_if_missing=True)

FILE_ID = "1FtZQR34S69D2DnOeM_agRTeIVwojbaAK"


@app.function(image=image, volumes={"/data": vol}, timeout=1800)
def fetch():
    import os

    import gdown

    out = "/data/gfd_entire.zip"
    if os.path.exists(out) and os.path.getsize(out) > 300_000_000:
        print(f"already have {os.path.getsize(out):,}")
        return os.path.getsize(out)
    gdown.download(id=FILE_ID, output=out, quiet=False)
    vol.commit()
    size = os.path.getsize(out)
    print(f"downloaded {size:,} bytes")
    return size


@app.local_entrypoint()
def main():
    print("size:", fetch.remote())
