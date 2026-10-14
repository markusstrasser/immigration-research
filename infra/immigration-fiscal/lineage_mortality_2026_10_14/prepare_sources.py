"""Parse the primary PDF with Poppler; pin sources once, verify thereafter.

Run: uv run --no-project python3 {lane}/prepare_sources.py [--pin]
The PDF is the published article hosted by Cleveland's health department, not
an LLM extraction. All Mexican rows are parsed, including adjusted models/CIs.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / "scripts"))
from memory_budget import require_within_budget
WHITE = HERE.parent / "white_replacement_2026_09_28"
PDF_URL = "https://www.clevelandhealth.org/assets/documents/health/minority_health/Analysis_in_Mortality_Experience_of_Hispanic_Subgroups.pdf"


def sha(path):
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def require(ok, label):
    if not ok:
        raise SystemExit(f"[BLOCKED] {label}")


def parse_pdf():
    target = HERE / "inputs/fenelon2017.txt"
    subprocess.run(["pdftotext", "-layout", str(HERE / "inputs/fenelon2017.pdf"), str(target)], check=True)
    text = target.read_text()
    require("10.1016/j.ssmph.2017.01.011" in text and "Chinn" in text, "PDF identity")
    rows = []
    for table, sex, page in ((3, "male", 6), (4, "female", 7)):
        body = text.split(f"Table {table}\n", 1)[1].split("Sociodemographic Covariates", 1)[0]
        require("Model 1" in body and "Model 4" in body and "Ages 65+" in body, "table headers")
        mex = [line.strip() for line in body.splitlines() if line.strip().startswith("Mexican ")]
        require(len(mex) == 2, f"Table {table} exactly two Mexican rows")
        for nativity, line in zip(("us_born", "foreign_born"), mex):
            cells = re.findall(r"([0-9]+\.[0-9]+) \(([0-9]+\.[0-9]+)[–-]([0-9]+\.[0-9]+)\)(\**)", line)
            require(len(cells) == 4, f"Table {table} {nativity} four HR/CI cells")
            for model, (hr, low, high, sig) in enumerate(cells, 1):
                rows.append(dict(table=table, pdf_page=page, sex=sex, nativity=nativity,
                                 age_band="25-64" if model <= 2 else "65+", model=model,
                                 adjustment="age_year_only" if model in (1, 3) else "socioeconomic",
                                 hr=float(hr), ci_low=float(low), ci_high=float(high),
                                 quoted_cell=f"{hr} ({low}–{high}){sig}", source_line=line))
    with (HERE / "derived/hazard_ratios.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    return rows


def parse_turra():
    target = HERE / "inputs/salmon_turra_elo_2008.txt"
    subprocess.run(["pdftotext", "-layout", str(HERE / "inputs/salmon_turra_elo_2008.pdf"), str(target)], check=True)
    text = target.read_text()
    require("Turra and Elo" in text and "10.1007/s11113-008-9087-4" in text, "Turra PDF identity")
    table = text.split("Table 4", 1)[1]
    require("1996-2000" in table and "Primary Social Security Beneficiaries" in table, "Turra Table 4 identity/window")
    rows, sex = [], None
    for line in table.splitlines():
        if line.strip() in ("Men", "Women"):
            sex = "male" if line.strip() == "Men" else "female"
        match = re.match(r"\s*(65-69|70-74|75-79|80-84|85-89|90\+)\s+(.*)", line)
        if not match:
            continue
        vals = re.findall(r"[0-9]+\.[0-9]+", match[2])
        require(sex is not None and len(vals) == 10, "Turra primary rate/CI row structure")
        low = int(match[1][:2])
        for population, index in (("all_hispanic", 0), ("all_nh_white", 1)):
            rows.append(dict(sex=sex, age_low=low, age_high=low + 4 if low < 90 else 120,
                             population=population, us_rate=vals[index], combined_rate=vals[index + 5],
                             source_table="Turra_Elo_2008_Table4"))
    require(len(rows) == 24, "Turra 24 sex/age/population rate rows")
    with (HERE / "inputs/salmon_turra_rates.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pin", action="store_true", help="one-time source inventory after inspection")
    ap.add_argument("--pin-salmon", action="store_true", help="append inspected supplementary sources once")
    ap.add_argument("--freeze-route", action="store_true", help="archive exact originally pinned v7 route after concurrent migration")
    args = ap.parse_args()
    pins_path = HERE / "inputs/pins.json"
    existing = json.loads(pins_path.read_text()) if pins_path.exists() else {}
    if args.freeze_route:
        require("route_archives" not in existing, "route archive already declared")
        paths_to_freeze = {
            str((WHITE / "inputs/pins.json").relative_to(ROOT)): "white_pins.json",
            str((WHITE / "tr2026_path.py").relative_to(ROOT)): "tr2026_path.py.txt",
            str((WHITE / "accrual_white.py").relative_to(ROOT)): "accrual_white.py.txt",
            str((WHITE / "mortality_comparators.py").relative_to(ROOT)): "mortality_comparators.py.txt",
            str((HERE.parent / "black_comparator_rough_2026_09_28/accrual_black.py").relative_to(ROOT)): "accrual_black.py.txt"}
        archives = {}
        for original, filename in paths_to_freeze.items():
            archive = HERE / "inputs/route_archive" / filename
            require(sha(archive) == existing["local_sources"][original], f"archive exactly original pinned bytes {original}")
            archives[original] = dict(file=str(archive.relative_to(ROOT)), sha256=sha(archive))
            existing["local_sources"][str(archive.relative_to(ROOT))] = sha(archive)
        existing["route_archives"] = archives
        existing["route_mode"] = "explicit frozen oct14/v7 route; concurrent oct15 entrypoint migration excluded"
        pins_path.write_text(json.dumps(existing, indent=2, sort_keys=True) + "\n")
    archive_map = existing.get("route_archives", {})
    upstream_file = archive_map.get(str((WHITE / "inputs/pins.json").relative_to(ROOT)), {}).get("file")
    upstream = json.loads((ROOT / upstream_file if upstream_file else WHITE / "inputs/pins.json").read_text())
    if args.pin:
        require(not pins_path.exists(), "refuse silent repinning")
        for name in upstream["mortality_sources"]:
            shutil.copyfile(WHITE / "inputs" / name, HERE / "inputs" / name)
    rows = parse_pdf()
    if (HERE / "inputs/salmon_turra_elo_2008.pdf").exists():
        parse_turra()
    paths = [HERE / "inputs/fenelon2017.pdf", HERE / "inputs/fenelon2017.txt"]
    paths += [WHITE / "inputs/pins.json"]
    for lane in (WHITE, HERE.parent / "black_comparator_rough_2026_09_28"):
        paths += [lane / "derived" / n for n in ("accrual_ratios_oct14.csv", "accrual_ratios_mortality_oct14.csv")]
    paths += [WHITE / "derived" / n for n in (
        "symmetric_hispanic_arm_oct14.csv", "symmetric_results_oct14.csv", "symmetric_comparisons_oct14.csv",
        "engine_lines_oct14_union.json", "engine_lines_oct14_union_cash.json",
        "engine_lines_oct14.json", "engine_lines_oct14_cash.json")]
    paths += [HERE.parent / "main_case_2026_10_14/derived" / n for n in (
        "corrections.json", "corrections_cash.json", "summary.json", "main_case_bands.csv")]
    paths += [HERE.parent / "main_case_candidate_2026_09_28/derived/production_row4.json"]
    paths += [WHITE / n for n in ("mortality_comparators.py", "accrual_white.py", "tr2026_path.py")]
    paths += [HERE.parent / "black_comparator_rough_2026_09_28/accrual_black.py"]
    for folder in ("pension_accrual_2026_09_28", "pension_tr2026_2026_10_06"):
        paths += sorted((HERE.parent / folder).glob("*.py"))
        paths += sorted((HERE.parent / folder / "reads").glob("*"))
    # The primary input frame is read through the admitted pension helper.
    paths += [HERE.parent / "gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip",
              HERE.parent / "lifetime_longevity_sstiming_2026_09_18/derived/cps_ss_stage.parquet",
              HERE.parent / "onbooks_share_2026_09_23/derived/onbooks_split.csv"]
    meta = json.loads((HERE.parent / "main_case_2026_10_14/derived/corrections.json").read_text())["meta"]
    paths += [HERE.parent / meta["lineage"]["age_mix"]["source"]["files"]["age_mix"]["file"]]
    salmon_names = ("salmon_turra_elo_2008.pdf", "salmon_turra_elo_2008.txt", "salmon_turra_rates.csv", "salmon_vanhook_zhang_2011.html")
    paths += [HERE / "inputs" / n for n in salmon_names if (HERE / "inputs" / n).exists()]
    paths += [ROOT / rec["file"] for rec in archive_map.values()]
    sources = {str(p.relative_to(ROOT)): sha(ROOT / archive_map[str(p.relative_to(ROOT))]["file"])
               if str(p.relative_to(ROOT)) in archive_map else sha(p) for p in paths if p.is_file()}
    if args.pin:
        pins = dict(mortality_sources=upstream["mortality_sources"], local_sources=sources,
                    fenelon=dict(url=PDF_URL, publisher_url="https://doi.org/10.1016/j.ssmph.2017.01.011",
                                 primary_copy="Published article PDF; not a secondary table",
                                 sha256=sha(HERE / "inputs/fenelon2017.pdf")))
        pins_path.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    pins = json.loads(pins_path.read_text())
    if args.pin_salmon:
        require("salmon_sources" not in pins, "refuse supplementary repinning")
        old = {k: v for k, v in sources.items() if Path(k).name not in salmon_names}
        require(pins["local_sources"] == old, "original source drift before supplementary append")
        require(sha(HERE / "inputs/salmon_turra_elo_2008.pdf") == "a70d7b848353f3bd1098d7099eadd9c6f3fd0b6c0b76462d7b9797731ac42d2d", "inspected Turra bytes")
        require(sha(HERE / "inputs/salmon_vanhook_zhang_2011.html") == "7f6ecc3564199587c35e80b274a4d8f5075e621e96aba6d178b62d662ad61742", "inspected Van Hook bytes")
        pins["local_sources"] = sources
        pins["salmon_sources"] = {
            "salmon_turra_elo_2008.pdf": dict(url="https://artefacts-discovery.researcher.life/full_text/DA-2/e2/e285c4d9b9f835799eded1acd9e1f52d/full_text/ac6ec3fbd082a0eb9d3165d716ddf65f.pdf",
                                             publisher_url="https://doi.org/10.1007/s11113-008-9087-4", sha256=sha(HERE / "inputs/salmon_turra_elo_2008.pdf")),
            "salmon_vanhook_zhang_2011.html": dict(url="https://pmc.ncbi.nlm.nih.gov/articles/PMC3367327/", sha256=sha(HERE / "inputs/salmon_vanhook_zhang_2011.html"))}
        pins_path.write_text(json.dumps(pins, indent=2, sort_keys=True) + "\n")
    require(pins["local_sources"] == sources, "source bytes changed; inspect rather than repin")
    for name, pin in pins["mortality_sources"].items():
        require(sha(HERE / "inputs" / name) == pin["sha256"], f"NVSS {name} hash")
    require(len(rows) == 16, "all Mexican sex/nativity/model HR cells extracted")
    require_within_budget("mortality source preparation")
    print("[gate] source pins verified; 16 exact primary HR/CI cells parsed")


if __name__ == "__main__":
    main()
