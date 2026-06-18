#!/usr/bin/env python3
"""Download HUD CHAS files (WAF blocks bare curl; warm session on cp.html)."""
from __future__ import annotations

import sys
from pathlib import Path

CP_PAGE = "https://www.huduser.gov/portal/datasets/cp.html"
UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)


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
    dest_s.parent.mkdir(parents=True, exist_ok=True)
    min_bytes = 10_240 if dest_s.suffix.lower() == ".zip" else 5_000
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print(
            "playwright not installed — run: uv run --with playwright python -m playwright install chromium",
            file=sys.stderr,
        )
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(user_agent=UA, accept_downloads=True)
        page = context.new_page()
        page.goto(CP_PAGE, wait_until="networkidle", timeout=120_000)
        resp = context.request.get(
            url,
            headers={"Referer": CP_PAGE},
            timeout=300_000,
        )
        if not resp.ok:
            print(f"HTTP {resp.status} for {url}", file=sys.stderr)
            browser.close()
            return 1
        body = resp.body()
        browser.close()

    if len(body) < min_bytes:
        print(f"download too small ({len(body)} bytes): {url}", file=sys.stderr)
        return 1
    dest_s.write_bytes(body)
    print(f"saved {dest_s} ({dest_s.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
