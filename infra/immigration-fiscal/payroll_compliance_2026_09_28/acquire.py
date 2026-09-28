"""Fetch the primary sources this lane quotes or calculates from, into _cache/sources/, with a manifest.

Each file is downloaded once with a generic user agent, checked against its pinned sha256 and converted to text
for quoting: PDFs with pdftotext -layout, the PMC article page by stripping its markup (table cells become
" | "), the Europe PMC record by its title, authors, citation and abstract fields. A cached file with the pinned
digest is not fetched again, so a rerun is offline. compliance.py reads only the cached texts.

Two routes differ from the publisher's https address, both recorded in the manifest:
- repec.tulane.edu served an expired TLS certificate on 2026-09-28, so the working paper comes over http and is
  held to its pinned digest instead;
- ssa.gov and oig.ssa.gov refuse a script's user agent (403 and 404), so Actuarial Note 151 and the OIG edit-routine
  audit come from the Internet Archive's unmodified capture (`id_`).

    OPENBLAS_NUM_THREADS=1 uv run --no-project python3 infra/immigration-fiscal/payroll_compliance_2026_09_28/acquire.py
"""
from __future__ import annotations

import datetime as dt
import hashlib
import html
import json
import re
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "_cache" / "sources"
UA = {"User-Agent": "research-script/1.0"}
WAYBACK = "https://web.archive.org/web/2024id_/"
# name: (url, publisher's address when the url is a mirror, pinned sha256)
SOURCES = {
    # IRS Publication 1415 (Rev. 10-2022), Federal Tax Compliance Research: Tax Gap Estimates for Tax Years 2014-2016.
    "irs_p1415.pdf": ("https://www.irs.gov/pub/irs-pdf/p1415.pdf", None,
                      "85409a6e4056f925578cc7adf14a391998d52c20c3779399d8785ef1ef807d0c"),
    # Alm and Erard, Using Public Information to Estimate Self-Employment Earnings of Informal Suppliers, Tulane
    # Economics Working Paper 1517 (2015).
    "tul1517.pdf": ("http://repec.tulane.edu/RePEc/pdf/tul1517.pdf", "https://repec.tulane.edu/RePEc/pdf/tul1517.pdf",
                    "f0cb0e55b176a2fa45b258f6fd62500c7a964c82dba8c31dbc3604501d37d583"),
    # SSA Office of the Chief Actuary, Actuarial Note 151 (Goss, Wade, Skirvin and Duggan, April 2013).
    "ssa_note151.pdf": (WAYBACK + "https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf",
                        "https://www.ssa.gov/oact/NOTES/pdf_notes/note151.pdf",
                        "e303a40dc437b52e91c63bce484971c73e1e0b08d83ea900cf1e028c6a6f8458"),
    # SSA OIG, Status of the Social Security Administration's Earnings Suspense File (A-03-15-50058, 2015).
    "ssa_oig_a0315500058.pdf": ("https://oig-files.ssa.gov/audits/full/A-03-15-50058.pdf", None,
                                "200ce7e79e337b3ef614b407621d9661be9ce18ad34c6ebb8c87344b916bc45b"),
    # SSA OIG, Edit Routines Used to Reinstate Wage Items from the Earnings Suspense File (A-03-21-51013, 2023).
    "ssa_oig_a0321510130.pdf": (WAYBACK + "https://oig.ssa.gov/assets/uploads/a-03-21-51013.pdf",
                                "https://oig.ssa.gov/assets/uploads/a-03-21-51013.pdf",
                                "a8cfe8c7a83ee0aeff6ebfda9b285a5437f5de7b694da94107b236d23b19db01"),
    # SSA OIG, The Social Security Administration's Major Management and Performance Challenges, FY 2024 (022401).
    "ssa_oig_022401.pdf": ("https://www.oversight.gov/sites/default/files/documents/reports/2024-11/022401.pdf",
                           None, "56fe6b0b29cfb530ac4fc1fa374aa8a23876be1ff0d51118d17515ac3c86790d"),
    # Census Bureau, CPS ASEC 2025 technical documentation (industry codes, Appendix A) and public-use data dictionary.
    "cpsmar25.pdf": ("https://www2.census.gov/programs-surveys/cps/techdocs/cpsmar25.pdf", None,
                     "7f0cb9f791f2737ad12fd552b8cb201f4d1de266eac160322597344e73499fb4"),
    "asec2025_ddl_pub_full.pdf": ("https://www2.census.gov/programs-surveys/cps/datasets/2025/march/asec2025_ddl_pub_full.pdf",
                                  None, "5cb80973326ef8b625fbaae70d80b0c641ce5d2b3911abd2fb4427abd5908a6f"),
    # Tamborini and Villarreal, Research Note: New Estimates of Immigrants' Self-employment From Linked Tax Records,
    # Demography 62(1):17 (2025), doi 10.1215/00703370-11773170; NIH author manuscript PMC11969445 (the publisher's
    # page and PDF return 403 to scripts; PMC's PDF link returns a challenge page, its article page the full text).
    "tv2025_pmc.html": ("https://pmc.ncbi.nlm.nih.gov/articles/PMC11969445/",
                        "https://doi.org/10.1215/00703370-11773170",
                        "cce4f551a47eec3acef909e91619673339684c45e5dbc7752c6431bef4d8ce6f"),
    # Imboden, Voorheis and Weber, Self-Employment Income Reporting on Surveys (May 2022 draft, Census Bureau DRB
    # release CBDRB-FY2022-CES010-015/016): CPS ASEC 2001-2016 linked to IRS and SSA earnings records. The copy is
    # the one the authors circulated for the 2022 UTAXI conference.
    "imboden_voorheis_weber_2022.pdf": ("https://nathanseegert.com/utaxi2022material/Weber.pdf", None,
                                        "72087288ef6cdec24f1d9d1e58b3f4fe0849cd5cc027cf800eb5fa3f89edef28"),
    # Villarreal and Tamborini, The Earnings Assimilation of Unauthorized Immigrants, Demography 63(1):137 (2026),
    # doi 10.1215/00703370-12470095: the Europe PMC record (abstract only; no full text is open).
    "vt2026_epmc.json": ("https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI%3A10.1215%2F00703370-12470095"
                         "&resultType=core&format=json", "https://doi.org/10.1215/00703370-12470095",
                         "f13608d21a3653c6cfb1ea05fcd1f354ab56e52b0b95b562e51c66f2b5a48735"),
}


def html_text(body: bytes) -> str:
    """The page's text: scripts and styles dropped, block ends as newlines, table cells closed by " | "."""
    s = body.decode("utf-8")
    s = re.sub(r"(?s)<script.*?</script>|<style.*?</style>", " ", s)
    s = re.sub(r"<(br|/p|/h[1-6]|/tr|/li|/caption|/title)[^>]*>", "\n", s)
    s = re.sub(r"</t[dh]>", " | ", s)
    s = html.unescape(re.sub(r"<[^>]+>", " ", s))
    s = re.sub(r"[ \t]+", " ", s)
    return re.sub(r"\n\s*\n+", "\n", s)


def epmc_text(body: bytes) -> str:
    rec = json.loads(body)["resultList"]["result"][0]
    j = rec.get("journalInfo", {})
    return "\n".join([rec["title"], rec["authorString"], f"{j.get('journal', {}).get('title')} {j.get('volume')}"
                      f"({j.get('issue')}):{rec.get('pageInfo')} ({rec.get('pubYear')}), doi {rec.get('doi')}, "
                      f"PMID {rec.get('pmid')}", "", rec["abstractText"], ""])


def looks_right(name: str, body: bytes) -> bool:
    if name.endswith(".pdf"):
        return body.startswith(b"%PDF")
    if name.endswith(".html"):
        return b"<html" in body[:2000].lower() and len(body) > 50_000
    return body.lstrip().startswith(b"{") and b'"abstractText"' in body


def get(url: str) -> tuple[int, bytes, dict, str]:
    req = urllib.request.Request(url, headers=UA)
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.status, r.read(), dict(r.headers), r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, b"", dict(e.headers or {}), url


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    mpath = OUT / "manifest.json"
    manifest = json.loads(mpath.read_text()) if mpath.exists() else {"user_agent": UA["User-Agent"], "files": {}}
    changed = False
    for name, (url, publisher, pin) in SOURCES.items():
        path = OUT / name
        if not path.exists():
            status, body, head, final = get(url)
            if status != 200 or not looks_right(name, body):
                raise SystemExit(f"[BLOCKED] {url} returned {status} ({len(body)} bytes, not the expected document)")
            path.write_bytes(body)
            manifest["files"][name] = {"url": url, "final_url": final, "publisher_url": publisher or url,
                                       "status": status, "bytes": len(body),
                                       "last_modified": head.get("Last-Modified"),
                                       "fetched_utc": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
            changed = True
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if manifest["files"].get(name, {}).get("sha256") not in (None, digest):
            raise SystemExit(f"[BLOCKED] {name} changed since the manifest recorded it")
        entry = manifest["files"].setdefault(name, {"url": url, "publisher_url": publisher or url})
        entry["sha256"] = digest
        txt = OUT / (path.stem + ".txt")
        if not txt.exists():
            if name.endswith(".pdf"):
                subprocess.run(["pdftotext", "-layout", str(path), str(txt)], check=True)
            else:
                txt.write_text((html_text if name.endswith(".html") else epmc_text)(path.read_bytes()))
            changed = True
        entry["text"] = txt.name
        # A PDF is pinned by its bytes. The two web records are pinned by their text: PMC's page carries a
        # per-request hit id in a meta tag, so its bytes differ between fetches while the article does not.
        pinned = digest if name.endswith(".pdf") else hashlib.sha256(txt.read_bytes()).hexdigest()
        entry["pinned_sha256_of"] = "file" if name.endswith(".pdf") else "text"
        if changed:
            mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")
        if pin is None:
            raise SystemExit(f"[BLOCKED] {name} has no pinned sha256; fetched {pinned}, pin it after reading the file")
        if pinned != pin:
            raise SystemExit(f"[BLOCKED] {name} sha256 {pinned[:12]} is not the pinned {pin[:12]}")
        print(f"  ✓ {name}: {path.stat().st_size:,} bytes, sha256 {pinned[:12]} ({entry['pinned_sha256_of']})")
    if changed:
        mpath.write_text(json.dumps(manifest, indent=1, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
