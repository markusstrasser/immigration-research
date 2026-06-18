#!/usr/bin/env python3
"""Download HUD CHAS files (WAF blocks bare curl; warm session on cp.html)."""
from __future__ import annotations

import sys
from pathlib import Path

# Allow import when run as script from infra/immigration-fiscal/scripts/
sys.path.insert(0, str(Path(__file__).resolve().parent))
from fetch_browser import fetch  # noqa: E402

CP_PAGE = "https://www.huduser.gov/portal/datasets/cp.html"


def _normalize_url(url: str) -> str:
    """Map legacy chas/files paths to current cp/ layout (Dec 2025 release)."""
    url = url.replace("/portal/datasets/chas/files/", "/portal/datasets/cp/")
    url = url.replace(
        "/portal/datasets/chas/files/CHAS-data-dictionary-18-22.xlsx",
        "/portal/datasets/cp/CHAS-data-dictionary-18-22.xlsx",
    )
    return url


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: fetch_hud_chas.py <url> <dest>", file=sys.stderr)
        return 1
    url, dest_s = _normalize_url(sys.argv[1]), Path(sys.argv[2])
    min_bytes = 10_240 if dest_s.suffix.lower() == ".zip" else 5_000
    try:
        fetch(url, dest_s, referer=CP_PAGE, min_bytes=min_bytes)
    except SystemExit as exc:
        print(exc, file=sys.stderr)
        return 1
    print(f"saved {dest_s} ({dest_s.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
