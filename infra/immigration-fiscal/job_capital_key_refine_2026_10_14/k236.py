#!/usr/bin/env python3
"""K2 foreign residence tax, K3 residential taxes, K6 mining size sensitivities.

Run only after core.py and housing_keys.cjs. Frozen national.py is imported
read-only and replayed into this lane's ignored cache, parsing its primary bytes.
"""
from __future__ import annotations
import contextlib
import importlib.util
import json
import resource
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
from core import CACHE, DERIVED, FISCAL, HERE, SOURCE, digest


def main():
    start = time.perf_counter()
    specs = {
        "k3_acs2023_subjects.pdf": "https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2023_ACSSubjectDefinitions.pdf",
        "k3_acs2024_subjects.pdf": "https://www2.census.gov/programs-surveys/acs/tech_docs/subject_definitions/2024_ACSSubjectDefinitions.pdf",
        "k3_bea_mp5.pdf": "https://www.bea.gov/sites/default/files/methodologies/mp5.pdf",
    }
    pin_path = HERE / "inputs/k236_pins.json"
    old = json.loads(pin_path.read_text()) if pin_path.exists() else None
    pins = {}
    for name, url in specs.items():
        p = CACHE / name
        if not p.exists():
            with urllib.request.urlopen(url, timeout=60) as r:
                p.write_bytes(r.read())
        h = digest(p)
        if old and old[name]["sha256"] != h:
            raise RuntimeError(f"[BLOCKED] changed primary source: {name}")
        pins[name] = {"url": url, "sha256": h}
    before_caches={str(p):digest(p) for p in (SOURCE/"__pycache__").glob("*") if p.is_file()}
    spec = importlib.util.spec_from_file_location("frozen_national", SOURCE / "national.py")
    national = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(national)
    previous_argv = sys.argv
    try:
        sys.argv = [str(SOURCE / "national.py"), "--out-dir", str(CACHE / "national_control")]
        with (CACHE / "national_control.log").open("w") as log, contextlib.redirect_stdout(log):
            rc = national.main()
    finally:
        sys.argv = previous_argv
    if rc != 0:
        raise RuntimeError("[BLOCKED] national primary-source replay failed")
    gates = []

    def gate(name, ok, detail=None):
        gates.append({"name": name, "passed": bool(ok), "detail": detail})
        if not ok:
            raise RuntimeError(f"[BLOCKED] {name}: {detail}")

    for p in (CACHE / "national_control").iterdir():
        gate(f"national primary parser positive control: {p.name}", digest(p) == digest(SOURCE / "derived" / p.name))
    gate("national parser import leaves frozen interpreter caches untouched", before_caches==
         {str(p):digest(p) for p in (SOURCE/"__pycache__").glob("*") if p.is_file()})
    text23 = national.pdf_text(CACHE / "k3_acs2023_subjects.pdf")
    text24 = national.pdf_text(CACHE / "k3_acs2024_subjects.pdf")
    for year, text in ((2023, text23), (2024, text24)):
        gate(f"ACS {year} real-estate tax includes special assessments", "including special assessments" in text)
    nat = json.loads((SOURCE / "derived/national.json").read_text())
    z = nat["land"]["z1_mn"]
    parts = nat["residential_split"]["residential_parts_bn"]
    f_owner = z["household_owner_real_estate"] / (z["household_owner_real_estate"] + z["noncorp_res_real_estate"])
    housing = json.loads((DERIVED / "housing_keys.json").read_text())
    arrays = np.load(CACHE / "core.npz")
    core = json.loads((DERIVED / "core.json").read_text())
    cells = list(arrays["cells"])
    outputs = {}
    details = {}
    for g in ("union", "G3plus", "white"):
        s = arrays[f"shares_{g}"]
        outputs[f"foreign_removed_{g}"] = s.T @ arrays["tax_corporate_ex_foreign"]
        # Support services have no owned reserve. Severance still stays zero.
        support = cells.index("213")
        for rd in ("low", "high"):
            r = core["responses"][rd]
            value = (s[support] * (arrays["full_corporate_bn"][support] * r["corporate"]
                     + arrays["full_c_and_i_property_bn"][support] * r["c_and_i_property"]
                     + arrays["full_otp_licenses_and_other_bn"][support]
                     + arrays["full_otp_documentary_bn"][support]
                     + arrays["full_otp_special_assessments_bn"][support]))
            outputs[f"support_{rd}_{g}"] = -value
            extract = np.array([cells.index("211"), cells.index("212")])
            # A sizing proxy, not a mineral/equipment tax measurement: apply the
            # source national tangible-personal-property fraction to extraction.
            equipment = s[extract].T @ arrays["full_c_and_i_property_bn"][extract] * nat["tpp"]["tau_of_business_line"]
            outputs[f"support_equipment_proxy_{rd}_{g}"] = -value-equipment
    for component, amount in parts.items():
        details[component] = {"national_bn": amount, "owner_bn": amount*f_owner, "tenant_bn": amount*(1-f_owner)}
        gate(f"K3 {component} owner+tenant national closure", abs(details[component]["owner_bn"]+details[component]["tenant_bn"]-amount)<1e-6)
        for population in ("union", "lineage"):
            key = f"{population}_share"
            receipt = amount * sum(frac * housing["lines"][line][key] * housing["lines"][line]["response"]["low"]
                                   for frac, line in ((f_owner,"modeled_owner_property"),(1-f_owner,"tenant_occupied_property")))
            details[component][f"{population}_delta_bn"] = -receipt
    gate("K2 federal foreign national amounts match parsed source", abs(float(arrays["full_corporate_bn"].sum()-arrays["full_corporate_ex_foreign_bn"].sum())-nat["foreign"]["removed_bn"])<1e-6)
    for primary, item in national.PINS.items():
        p = SOURCE / "_cache" / primary
        pins[f"source:{primary}"] = {"path": str(p), "sha256": digest(p), "url": item.get("url")}
    pins["source:bea_nipa3"] = {"path":str(national.NIPA3),"sha256":digest(national.NIPA3)}
    pin_path.write_text(json.dumps(pins, indent=2)+"\n")
    np.savez(CACHE / "k236_targets.npz", **outputs)
    result = {"K2":nat["foreign"],"K3": {"components":details,"owner_fraction":f_owner,"housing":housing,
              "recommendation":"Gross requested pricing is a sensitivity. Withhold special-assessment addition: ACS 2023 B25103 includes assessments, feeding the modeled-owner rate; rental base is BEA housing taxes on production. Documentary transfer-tax candidate is separate and still requires housing-tax reconciliation.",
              "overlap_chain":["gen_ledger_extension_2026_09_16/stage_inputs.py:34-39 ACS2023 B25103/B25077", "extend_ledger.py:173-178 state property rate", "generation_account_2026_09_24/keys.py:50-57 modeled owner amount", "full_account_receipts_2026_09_20/builder.py:209-214 owner amount subtracted from NIPA property pool"]},
              "K6":{"recommendation":"Size only. Support plus equipment is not proof of a net capital departure: mining jobs may refill at fixed output. Equipment tax share is a national proxy, not measured mining property composition.","equipment_proxy_tau":nat["tpp"]["tau_of_business_line"]}, "gates":gates}
    (DERIVED / "k236.json").write_text(json.dumps(result,indent=2)+"\n")
    runtime={"elapsed_s":time.perf_counter()-start,"peak_rss_bytes":resource.getrusage(resource.RUSAGE_SELF).ru_maxrss}
    (CACHE / "k236_runtime.json").write_text(json.dumps(runtime)+"\n")
    print(json.dumps({"gates":len(gates),"K3":details,"runtime":runtime},indent=2))


if __name__ == "__main__":
    main()
