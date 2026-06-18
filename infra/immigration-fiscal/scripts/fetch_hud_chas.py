#!/usr/bin/env python3
"""Download HUD CHAS files (WAF blocks bare curl)."""
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: fetch_hud_chas.py <url> <dest>", file=sys.stderr)
        return 1
    url, dest = sys.argv[1], Path(sys.argv[2])
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("playwright not installed — run: uv run --with playwright python -m playwright install chromium", file=sys.stderr)
        return 1

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            ),
            accept_downloads=True,
        )
        page = context.new_page()
        page.goto(
            "https://www.huduser.gov/portal/datasets/chas.html",
            wait_until="networkidle",
            timeout=120_000,
        )
        resp = context.request.get(url, timeout=180_000)
        if not resp.ok:
            print(f"HTTP {resp.status} for {url}", file=sys.stderr)
            browser.close()
            return 1
        body = resp.body()
        if len(body) < 10_240:
            print(f"download too small ({len(body)} bytes): {url}", file=sys.stderr)
            browser.close()
            return 1
        dest.write_bytes(body)
        browser.close()

    print(f"saved {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
