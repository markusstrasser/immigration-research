#!/usr/bin/env python3
"""Arm E: the Latin share of US recorded-music revenue, from the RIAA's own
year-end reports (primary PDFs, parsed here - no figure is taken from a search
snippet or from model memory).

Downloads the RIAA year-end Latin revenue reports and the all-genre year-end
revenue report, extracts their text, and pulls out every line that carries a
Latin share or revenue figure so the memo can quote the document itself.

Output: _cache/riaa/*.pdf, derived/arm_e_music_shares.csv,
        derived/arm_e_riaa_quotes.txt
"""
import re
import sys
from pathlib import Path

import pandas as pd
import requests
from pypdf import PdfReader

LANE = Path(__file__).resolve().parent.parent
CACHE = LANE / "_cache" / "riaa"
DER = LANE / "derived"
CACHE.mkdir(parents=True, exist_ok=True)

UA = {"User-Agent": "immigration-research-lane/1.0 (cultural-output arm E)"}
PDFS = {
    "riaa_latin_2025_year_end":
        "https://www.riaa.com/wp-content/uploads/2026/04/"
        "RIAA-US-Latin-Year-End-Revenue-2025.pdf",
    "riaa_latin_2024_year_end":
        "https://www.riaa.com/wp-content/uploads/2025/03/"
        "RIAA-2024-Year-End-US-Market-Latin-Music-Revenue-Report.pdf",
    "riaa_all_2024_year_end":
        "https://www.riaa.com/wp-content/uploads/2025/03/"
        "RIAA-2024Year-End-Revenue-Report.pdf",
}
PAT = re.compile(r"latin", re.I)
NUMPAT = re.compile(r"\d")


def get(name: str, url: str) -> Path:
    p = CACHE / f"{name}.pdf"
    if p.exists() and p.stat().st_size > 20000:
        return p
    r = requests.get(url, headers=UA, timeout=600)
    r.raise_for_status()
    if r.content[:4] != b"%PDF":
        print(f"  {name}: body is not a PDF ({r.content[:40]!r})", flush=True)
        return None
    p.write_bytes(r.content)
    print(f"  {name}: {len(r.content):,} bytes", flush=True)
    return p


def main() -> None:
    quotes = []
    rows = []
    for name, url in PDFS.items():
        p = get(name, url)
        if p is None:
            rows.append({"report": name, "status": "unavailable", "url": url})
            continue
        try:
            reader = PdfReader(str(p))
            text = "\n".join((pg.extract_text() or "") for pg in reader.pages)
        except Exception as exc:  # noqa: BLE001
            print(f"  {name}: parse failed {exc!r}", flush=True)
            rows.append({"report": name, "status": "parse_failed", "url": url})
            continue
        if len(text) < 200:
            rows.append({"report": name, "status": "no_text_layer",
                         "url": url})
            print(f"  {name}: no text layer ({len(text)} chars)", flush=True)
            continue
        # the share sentence is broken across lines in the RIAA layout, so
        # search a whitespace-normalised copy as well as the raw lines
        flat = re.sub(r"\s+", " ", text)
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        hits = [ln for ln in lines if PAT.search(ln) and NUMPAT.search(ln)]
        share_sentences = re.findall(
            r"[^.]*?Latin[^.]{0,200}?\d{1,2}(?:\.\d)?%[^.]{0,120}\.?", flat)
        share_sentences += re.findall(
            r"Latin music made up \d{1,2}(?:\.\d)?% of total US revenue", flat)
        (DER / f"arm_e_text_{name}.txt").write_text(flat + "\n")
        quotes.append(f"=== {name} ===\n{url}\nSHARE SENTENCES:\n"
                      + "\n".join(f"  \"{q.strip()}\"" for q in
                                  dict.fromkeys(share_sentences))
                      + "\nLATIN LINES:\n" + "\n".join(hits[:60]))
        # the headline share itself, pulled from the document text; if no
        # pattern matches, the field stays empty rather than being guessed
        share, share_src = "", ""
        for pat in (r"Latin music made up (\d{1,2}(?:\.\d)?)% of total US revenue",
                    r"growing to (\d{1,2}(?:\.\d)?)% of total recorded music "
                    r"revenue in the US"):
            m = re.search(pat, flat)
            if m:
                share = m.group(1)
                share_src = m.group(0)
                break
        total = ""
        m = re.search(r"Total Revenue \$([\d,]+(?:\.\d)?) \$([\d,]+(?:\.\d)?)",
                      flat)
        if m:
            total = m.group(2)
        basis = ("wholesale" if "WHOLESALE DATA" in flat.upper()
                 else "retail value" if share else "")
        pct = re.findall(r"(\d{1,2}\.\d)%", text)
        rows.append({"report": name, "status": "parsed", "url": url,
                     "latin_share_of_us_revenue_pct": share,
                     "reporting_basis": basis,
                     "latin_total_revenue_musd_latest_year": total,
                     "source_sentence": share_src,
                     "pages": len(reader.pages), "latin_lines": len(hits),
                     "share_sentences": len(set(share_sentences)),
                     "percentages_found": "|".join(sorted(set(pct))[:20])})
        print(f"  {name}: {len(reader.pages)} pages, {len(hits)} Latin lines",
              flush=True)
    if not rows:
        sys.exit("FAIL no RIAA reports processed")
    (DER / "arm_e_riaa_quotes.txt").write_text("\n\n".join(quotes) + "\n")
    out = pd.DataFrame(rows)
    out.to_csv(DER / "arm_e_music_shares.csv", index=False)
    got = out.get("latin_share_of_us_revenue_pct", pd.Series(dtype=str))
    if not (got.astype(str).str.len() > 0).any():
        sys.exit("FAIL no Latin revenue share extracted from any report")
    print(out[["report", "latin_share_of_us_revenue_pct", "reporting_basis",
               "latin_total_revenue_musd_latest_year"]].to_string(index=False),
          flush=True)
    print("\n".join(quotes)[:4000], flush=True)


if __name__ == "__main__":
    main()
