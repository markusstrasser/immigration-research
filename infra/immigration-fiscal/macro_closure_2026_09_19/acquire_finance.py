"""Acquire public Census fiscal aggregates without recording authentication."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import urllib.parse
import urllib.request

BASE = "https://api.census.gov/data/timeseries/govslocalfin"
HERE = Path(__file__).resolve().parent


def fetch(url, name):
    try:
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 research-data-client"})
        with urllib.request.urlopen(request, timeout=45) as response:
            return response.read()
    except Exception as error:
        # Exception strings can contain the authenticated URL. Never emit them.
        raise RuntimeError(f"Census fetch failed for {name}: {type(error).__name__}") from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=HERE / "_cache")
    args = parser.parse_args()
    key = os.environ.get("CENSUS_API_KEY")
    if not key:
        raise ValueError("Set CENSUS_API_KEY from the repository acquisition configuration; Data.gov keys are not Census keys")
    args.out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for year in [2022, 2024]:
        for geography in ["us:*", "state:*"]:
            query = dict(get="AGG_DESC,AGG_DESC_LABEL,GOVTYPE,GOVTYPE_LABEL,NAME,YEAR,AMOUNT,AMOUNT_F,AMOUNT_CV,AMOUNT_CV_F",
                         time=str(year), GOVTYPE="001", **{"for": geography})
            public_url = BASE + "?" + urllib.parse.urlencode(query)
            name = f"finance_{year}_{geography.split(':')[0]}_combined.json"
            path = args.out / name
            data = path.read_bytes() if path.exists() else fetch(public_url + "&key=" + urllib.parse.quote(key), name)
            try:
                rows = json.loads(data)
                if not isinstance(rows, list) or len(rows) < 2 or "AMOUNT" not in rows[0]:
                    raise ValueError
            except (ValueError, TypeError):
                text = data.decode(errors="replace").lower()
                reason = "invalid API key" if "invalid key" in text or "invalid api key" in text else "unexpected response format"
                raise ValueError(f"Invalid Census aggregate response for {name}: {reason}; nothing written") from None
            if not path.exists():
                path.write_bytes(data)
            manifest.append(dict(file=name, source_url=public_url, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data), rows=len(rows) - 1))
            print(name, "rows", len(rows) - 1, "bytes", len(data), flush=True)
    for name, url in [("variables.json", BASE + "/variables.json"),
                      ("methodology.pdf", "https://www2.census.gov/programs-surveys/gov-finances/technical-documentation/methodology/2024/2024_methodology.pdf")]:
        path = args.out / name
        data = path.read_bytes() if path.exists() else fetch(url, name)
        if name.endswith(".pdf") and not data.startswith(b"%PDF"):
            raise ValueError("Methodology response is not PDF")
        if not path.exists():
            path.write_bytes(data)
        manifest.append(dict(file=name, source_url=url, sha256=hashlib.sha256(data).hexdigest(), bytes=len(data)))
    (args.out / "manifest.json").write_text(json.dumps(dict(acquired="2026-09-19", files=manifest), indent=2) + "\n")


if __name__ == "__main__":
    main()
