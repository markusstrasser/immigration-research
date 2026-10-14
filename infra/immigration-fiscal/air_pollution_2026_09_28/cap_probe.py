"""Retrieve official CAMPD allowance data; API key stays in process and is never logged."""
from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
import urllib.error
import urllib.request

HERE = Path(__file__).resolve().parent


def main():
    status = HERE / "_cache/cap_probe_status.json"
    if status.exists():
        # Preserve the dated acquisition receipt; an explicit new probe can
        # use a new filename. A rerun must not repeatedly hit a blocked API.
        records = json.loads(status.read_text())
        if {r["name"] for r in records} != {"account_swagger", "arp_compliance_2024"}:
            raise ValueError("[BLOCKED] incomplete CAMPD probe receipt")
        print(json.dumps(records))
        return
    envpath = HERE / "_cache/campd_env.js"
    if not envpath.exists():
        subprocess.run(["curl", "-fLsS", "--max-time", "30", "https://campd.epa.gov/env-config.js", "-o", str(envpath)], check=True)
    env = envpath.read_text()
    match = re.search(r"VITE_EASEY_CAMPD_UI_API_KEY['\"]?\s*:\s*(['\"])(.*?)\1", env)
    if match is None:
        raise ValueError("[BLOCKED] public CAMPD configuration lacks key declaration")
    records = []
    routes = {
        "account_swagger": "https://api.epa.gov/easey/account-mgmt/swagger-json",
        "arp_compliance_2024": "https://api.epa.gov/easey/account-mgmt/allowance-compliance?year=2024&programCode=ARP",
    }
    for name, url in routes.items():
        path = HERE / f"_cache/{name}.json"
        if path.exists():
            records.append(dict(name=name, url=url, status="preserved"))
            continue
        req = urllib.request.Request(url, headers={"x-api-key": match[2], "x-app-identifier": "CAMPD", "User-Agent": "Mozilla/5.0"})
        try:
            with urllib.request.urlopen(req, timeout=30) as response:
                data = response.read()
            parsed = json.loads(data)
            path.write_text(json.dumps(parsed, indent=2) + "\n")
            records.append(dict(name=name, url=url, status="acquired", bytes=len(data)))
        except urllib.error.HTTPError as exc:
            records.append(dict(name=name, url=url, status="HTTP_ERROR", code=exc.code))
    # Endpoint status only: never exception repr/header/key-bearing config.
    status.write_text(json.dumps(records, indent=2) + "\n")
    print(json.dumps(records))


if __name__ == "__main__":
    main()
