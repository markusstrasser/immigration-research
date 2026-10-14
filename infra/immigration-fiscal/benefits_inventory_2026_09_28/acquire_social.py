"""Acquire official CPS microdata and codebooks; pins fail closed on later runs."""
import concurrent.futures
import hashlib
import json
import pathlib
import shutil
import time
import urllib.request

LANE = pathlib.Path(__file__).resolve().parent
CACHE = LANE / "_cache"
INPUTS = LANE / "inputs"


def acquire(name, url, local=None):
    target = CACHE / name
    if not target.exists():
        if local and local.exists():
            shutil.copyfile(local, target)
        else:
            with urllib.request.urlopen(url, timeout=180) as response, target.open("wb") as out:
                shutil.copyfileobj(response, out)
    return {"file": f"_cache/{name}", "url": url,
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size}


def main():
    CACHE.mkdir(exist_ok=True)
    INPUTS.mkdir(exist_ok=True)
    jobs = []
    for year in (2023, 2024):
        for name in (f"dec{year % 100}pub.csv", f"dec{year % 100}hhrep.csv"):
            jobs.append((name, f"https://www2.census.gov/programs-surveys/cps/datasets/{year}/supp/{name}", None))
        name = f"cpsdec{year % 100}.pdf"
        jobs.append((name, f"https://www2.census.gov/programs-surveys/cps/techdocs/{name}", None))
    shared = LANE.parent / "service_by_ses_2026_09_23/_cache/cps"
    for name in ("sep23pub.csv", "sep23nrrep.csv"):
        jobs.append((name, f"https://www2.census.gov/programs-surveys/cps/datasets/2023/supp/{name}", shared / name))
    jobs.append(("cpssep23.pdf", "https://www2.census.gov/programs-surveys/cps/techdocs/cpssep23.pdf", shared / "cpssep23.pdf"))
    jobs.append(("cpssept15.pdf", "https://www2.census.gov/programs-surveys/cps/techdocs/cpssept15.pdf", None))
    jobs.append(("sep15pub.dat.gz", "https://www2.census.gov/programs-surveys/cps/datasets/2015/supp/sep15pub.dat.gz", None))
    start = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        pins = list(pool.map(lambda args: acquire(*args), jobs))
    path = INPUTS / "pins.json"
    if path.exists():
        old = json.loads(path.read_text())
        current = {p["file"]: p for p in pins}
        assert all(current[p["file"]] == p for p in old), "[BLOCKED] source pins changed"
        path.write_text(json.dumps(pins, indent=2) + "\n")
    else:
        path.write_text(json.dumps(pins, indent=2) + "\n")
    print(f"Pinned {len(pins)} sources in {time.perf_counter() - start:.2f}s")


if __name__ == "__main__":
    main()
