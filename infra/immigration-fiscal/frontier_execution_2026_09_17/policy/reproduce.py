"""Recompute published H2B table arithmetic; does NOT re-estimate microdata regressions.

Run: uv run python3 reproduce.py
The parent directory may be relocated without changing this script.
"""
import csv
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW = ROOT / "raw"
OUT = ROOT / "derived"
OUT.mkdir(exist_ok=True)

article = (RAW / "article-piie-july2026.txt").read_text()
appendix = (RAW / "appendix.txt").read_text()
assert "Table 2: Effect of H-2B workers on primary outcomes" in article
assert "Appendix Table A4: First stage regressions, pooled 2021 and 2022" in appendix
for number in ["0.618", "0.112", "2.233", "0.374"]:
    assert number in appendix[appendix.index("Appendix Table A4: First stage"):][:1800]
table2 = article[article.index("Table 2: Effect of H-2B workers on primary outcomes"):][:3800]
for number in ["0.135", "0.051", "0.443", "0.154", "0.218", "0.080", "0.198", "0.069", "0.116", "0.095", "0.188", "0.149", "0.136", "0.285", "0.061", "0.125"]:
    assert number in table2, f"Published-table transcription mismatch: {number}"

# Values transcribed from primary Table 2 and Appendix Table A4, not synthetic records.
specs = [
    ("first_stage_win", "IHS H2B hires", "A4", 472, .618, .112),
    ("first_stage_share", "IHS H2B hires", "A4", 472, 2.233, .374),
    ("revenue_reduced_form_win", "log revenue", "2 col 2", 472, .135, .051),
    ("revenue_reduced_form_share", "log revenue", "2 col 4", 472, .443, .154),
    ("revenue_iv_win", "log revenue / IHS H2B", "2 col 3", 472, .218, .080),
    ("revenue_iv_share", "log revenue / IHS H2B", "2 col 5", 472, .198, .069),
    ("us_hires_reduced_form_win", "IHS US temporary hires", "2 col 7", 472, .116, .095),
    ("us_hires_reduced_form_share", "IHS US temporary hires", "2 col 9", 472, .136, .285),
    ("us_hires_iv_win", "IHS US temporary / IHS H2B", "2 col 8", 472, .188, .149),
    ("us_hires_iv_share", "IHS US temporary / IHS H2B", "2 col 10", 472, .061, .125),
    ("investment_iv_win", "IHS investment / IHS H2B", "3 col 3", 456, 2.072, .721),
    ("investment_iv_share", "IHS investment / IHS H2B", "3 col 5", 456, 1.466, .610),
]
rows = [dict(spec=s, units=u, table=t, n=n, estimate=b, se=se,
             normal95_low=b-1.96*se, normal95_high=b+1.96*se)
        for s,u,t,n,b,se in specs]
with (OUT / "published_table_arithmetic.csv").open("w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys()); w.writeheader(); w.writerows(rows)

ratios = [
    dict(endpoint="revenue_win", reduced=.135, first_stage=.618, published_iv=.218),
    dict(endpoint="revenue_share", reduced=.443, first_stage=2.233, published_iv=.198),
    dict(endpoint="us_hires_win", reduced=.116, first_stage=.618, published_iv=.188),
    dict(endpoint="us_hires_share", reduced=.136, first_stage=2.233, published_iv=.061),
]
for row in ratios:
    row["recomputed_ratio"] = row["reduced"] / row["first_stage"]
    row["difference_from_rounded_iv"] = row["recomputed_ratio"] - row["published_iv"]
    assert abs(row["difference_from_rounded_iv"]) < .001
result = {
    "status": "PARTIAL: published-table arithmetic only; raw data unavailable in this epoch",
    "ratio_checks": ratios,
    "revenue_win_conditional_geometric_ratio": math.exp(.135),
    "revenue_win_normal95_ratio_interval": [math.exp(.135-1.96*.051), math.exp(.135+1.96*.051)],
    "first_stage_loss_approx_log_percent": 100*(1-math.exp(-.618)),
    "first_stage_t_squared_rounded": (.618/.112)**2,
    "raw_form_to_core_fraction_2021": 251/371,
    "raw_form_to_core_fraction_2022": 221/297,
    "scope_warning": "IHS coefficients are not exact constant elasticities, especially at zero; normal intervals use rounded published SEs, not Anderson-Rubin or randomization intervals; response-form fractions are not response rates among all invited firms.",
}
(OUT / "checks.json").write_text(json.dumps(result, indent=2)+"\n")
urls = {
    "aea.html": "https://www.aeaweb.org/articles?id=10.1257/app.20250049",
    "article-piie-july2026.pdf": "https://www.piie.com/sites/default/files/2026-07/wp26-11.pdf",
    "appendix.pdf": "https://www.aeaweb.org/articles/materials/25505",
}
manifest = {"retrieved": "2026-09-17", "article_doi": "10.1257/app.20250049", "replication_doi": "10.3886/E234802V1", "files": []}
for path in sorted(RAW.iterdir()):
    if path.is_file():
        manifest["files"].append(dict(path=str(path.relative_to(ROOT)), bytes=path.stat().st_size,
                                     sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                                     source_url=urls.get(path.name),
                                     derivative=path.suffix == ".txt"))
manifest["failed_routes"] = [
    {"route": "sandbox curl", "result": "DNS unavailable; authorized public-download escalation succeeded for other URLs"},
    {"route": "AEA main PDF /articles/pdf/doi/10.1257/app.20250049", "result": "HTTP403; author institution published reprint obtained instead"},
    {"route": "https://www.openicpsr.org/openicpsr/project/234802/version/V1/view", "result": "curl HTTP403; web unsafe-redirect error; isolated headless browser displayed Cloudflare security verification"},
    {"route": "title+replication+github and package234802 web searches", "result": "No usable alternate package identified; not proof no alternate public copy exists"},
]
(ROOT / "manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
print(json.dumps(result, indent=2))
