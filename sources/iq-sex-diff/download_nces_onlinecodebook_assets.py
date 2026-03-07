#!/usr/bin/env python3
"""Fetch NCES Online Codebook file manifests and optionally download assets."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


SURVEYS = {
    "hsls": {
        "survey_id": 37,
        "survey_year": 2017,
        "version": "1.0",
        "target_dir": "hsls",
        "label": "HSLS: 2009-16, including PETS/SR",
    },
    "els": {
        "survey_id": 11,
        "survey_year": 2012,
        "version": "1.0",
        "target_dir": "els",
        "label": "ELS:2002-12, including PETS",
    },
    "nels": {
        "survey_id": 20,
        "survey_year": 2000,
        "version": "1.0",
        "target_dir": "nels",
        "label": "NELS:1988-00",
    },
    "hsb": {
        "survey_id": 25,
        "survey_year": 1980,
        "version": "1.0",
        "target_dir": "hsb",
        "label": "HS&B 1980",
    },
}


def fetch_json(url: str) -> dict:
    with urllib.request.urlopen(url) as response:
        return json.load(response)


def stream_download(url: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(url) as response, destination.open("wb") as fh:
        while True:
            chunk = response.read(1024 * 1024)
            if not chunk:
                break
            fh.write(chunk)


def resolve_manifest(key: str) -> tuple[str, dict]:
    spec = SURVEYS[key]
    guid_url = (
        "https://nces.ed.gov/datalab/api/v1/onlinecodebook/session/guid"
        f"?surveyId={spec['survey_id']}"
        f"&surveyYear={spec['survey_year']}"
        f"&versionNumber={spec['version']}"
    )
    guid_response = fetch_json(guid_url)
    guid = guid_response["result"]
    manifest_url = (
        "https://nces.ed.gov/datalab/api/v1/onlinecodebook/session/"
        f"{guid}/file/data/1"
    )
    manifest = fetch_json(manifest_url)
    return guid, manifest


def write_manifest(target_dir: Path, key: str, guid: str, manifest: dict) -> Path:
    output = {
        "survey_key": key,
        "survey": SURVEYS[key],
        "session_guid": guid,
        "manifest": manifest,
    }
    path = target_dir / f"{key}_onlinecodebook_manifest.json"
    path.write_text(json.dumps(output, indent=2) + "\n")
    return path


def run() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--survey",
        nargs="+",
        choices=sorted(SURVEYS),
        required=True,
        help="NCES Online Codebook survey keys to fetch.",
    )
    parser.add_argument(
        "--data-root",
        default="data",
        help="Root data directory containing survey subdirectories.",
    )
    parser.add_argument(
        "--download",
        action="store_true",
        help="Download all files listed in the manifest.",
    )
    args = parser.parse_args()

    data_root = Path(args.data_root).resolve()
    failures = []

    for key in args.survey:
        spec = SURVEYS[key]
        target_dir = data_root / spec["target_dir"]
        target_dir.mkdir(parents=True, exist_ok=True)
        print(f"[{key}] resolving manifest for {spec['label']}", flush=True)

        try:
            guid, manifest = resolve_manifest(key)
        except urllib.error.HTTPError as exc:
            failures.append((key, f"HTTP {exc.code}"))
            print(f"[{key}] manifest fetch failed: HTTP {exc.code}", file=sys.stderr)
            continue
        except Exception as exc:  # pragma: no cover - defensive
            failures.append((key, str(exc)))
            print(f"[{key}] manifest fetch failed: {exc}", file=sys.stderr)
            continue

        manifest_path = write_manifest(target_dir, key, guid, manifest)
        print(f"[{key}] manifest -> {manifest_path}", flush=True)

        if not args.download:
            continue

        for item in manifest.get("result", []):
            url = item["location"]
            filename = Path(urllib.parse.urlparse(url).path).name
            destination = target_dir / filename
            if destination.exists():
                print(f"[{key}] skip existing {filename}", flush=True)
                continue
            print(f"[{key}] downloading {filename}", flush=True)
            try:
                stream_download(url, destination)
            except Exception as exc:  # pragma: no cover - defensive
                failures.append((key, f"{filename}: {exc}"))
                print(
                    f"[{key}] download failed for {filename}: {exc}",
                    file=sys.stderr,
                )

    if failures:
        print("\nFailures:", file=sys.stderr)
        for key, message in failures:
            print(f"- {key}: {message}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
