"""Pull GDELT Television Explorer airtime shares for 2024 (CNN, Fox News, MSNBC).

Each value is the percent of a station's monitored news airtime, in 15-second clips, whose
captions match the query on that day (GDELT TV API v2, mode=timelinevol, datanorm=perc).
A single matching word marks the whole clip, so the share is a mention share, not a topic
share. Saved raw to inputs/ so attention_cost.py reads pinned files.

Run: uv run --no-project python3 infra/immigration-fiscal/attention_cost_2026_10_21/fetch_gdelt_tv.py
"""
import pathlib
import time
import urllib.parse
import urllib.request

HERE = pathlib.Path(__file__).resolve().parent
OUT = HERE / "inputs"
STATIONS = "(station:CNN OR station:FOXNEWS OR station:MSNBC)"
QUERIES = {
    "immigration_narrow": "(immigration OR immigrant OR immigrants OR migrant OR migrants OR deportation)",
    "immigration_border": "(immigration OR immigrant OR immigrants OR migrant OR migrants OR deportation OR border)",
    "mexico": "(mexico OR mexican OR mexicans)",
    "inflation_prices": "(inflation OR prices)",
    "abortion": "abortion",
    "ukraine": "ukraine",
}
YEARS = [2022, 2023, 2024]


def fetch(query: str, year: int) -> bytes:
    params = {
        "query": f"{query} {STATIONS}",
        "mode": "timelinevol",
        "format": "csv",
        "startdatetime": f"{year}0101000000",
        "enddatetime": f"{year}1231235959",
        "datanorm": "perc",
    }
    url = "https://api.gdeltproject.org/api/v2/tv/tv?" + urllib.parse.urlencode(params)
    with urllib.request.urlopen(url, timeout=120) as r:
        return r.read()


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for name, q in QUERIES.items():
        for y in YEARS:
            path = OUT / f"gdelt_tv_{name}_{y}.csv"
            if path.exists():
                continue
            body = fetch(q, y)
            if b"Series" not in body[:200]:
                raise SystemExit(f"[BLOCKED] unexpected GDELT body for {name} {y}: {body[:200]!r}")
            path.write_bytes(body)
            time.sleep(6)


if __name__ == "__main__":
    main()
