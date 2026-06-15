#!/usr/bin/env python3
"""Download HUD CHAS files through headless Chromium (WAF blocks curl)."""
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
        print("playwright not installed", file=sys.stderr)
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
            wait_until="domcontentloaded",
            timeout=120_000,
        )
        fname = Path(url).name
        with page.expect_download(timeout=180_000) as dl_info:
            page.locator(f'a[href*="{fname}"]').first.click()
        download = dl_info.value
        download.save_as(str(dest))
        browser.close()

    if not dest.exists() or dest.stat().st_size < 10_240:
        print(f"download too small: {dest}", file=sys.stderr)
        return 1
    print(f"saved {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
