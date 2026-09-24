"""Arm 4, task 6: what a corrected BJS jail Hispanic share does to the justice lane's BJS-check prisons key.

The cj lane (`cj_use_allocation_2026_09_23/allocate.py`, `bjs_custody()` and `shares["custody_bjs_adj"]`) keys
prisons spending by

    key = s x m_adj x tau,   s = (H_prison + H_jail) / (N_prison + N_jail)

with H_prison/N_prison = 282,700 / 1,210,308 (BJS sentenced prisoners, yearend 2023, SPI-adjusted),
H_jail/N_jail = 95,700 / 664,200 (BJS Jail Inmates in 2023 Table 5), m_adj = Mexican share of Hispanic
institutional residents 18-64 with the generic-Hispanic excess reallocated (ACS 2024), and tau = CPS target
18-64 over ACS Mexican household residents 18-64. The adopted central prisons key is the ACS custody share
(custody_acs_adj = 0.1419) on BEA prisons spending ($121.32bn); the BJS key is a corroborating arm only.

Positive control first: rebuild 0.1428 from the constants and the audit's +$2.45bn (jail share at the
FBI 2024 adult arrest share, 22.1%) against the adopted central. Then, for every corrected jail share in
derived/jail_share_estimates.csv, write derived/jail_bjs_arm.csv. Last, scale the adopted ACS custody key by
1/f for each recorded/self-identified ratio in derived/jail_acs_record_ratio.csv and write
derived/jail_acs_key_sensitivity.csv (a sensitivity, not a correction: it assumes proportional under-recording).

Run from the repository root:
    OPENBLAS_NUM_THREADS=1 uv run --no-project --with pandas python3 \
        infra/immigration-fiscal/crime_ratio_direction_2026_09_24/jail_bjs_arm.py
"""
import json, pathlib, sys

import pandas as pd

HERE = pathlib.Path(__file__).resolve().parent
FISCAL = HERE.parent
CJ = FISCAL / "cj_use_allocation_2026_09_23/derived/summary.json"
ARRESTS = FISCAL / "nibrs_arrests_2026_09_16/arrests_by_ethnicity_2023.csv"
EST = HERE / "derived/jail_share_estimates.csv"
OUT = HERE / "derived/jail_bjs_arm.csv"
RR = HERE / "derived/jail_acs_record_ratio.csv"        # from jail_share.py
SENS = HERE / "derived/jail_acs_key_sensitivity.csv"

H_PRISON, N_PRISON = 282_700, 1_210_308      # Prisoners in 2023 Table 3, sentenced, yearend 2023 (adjusted)
H_JAIL, N_JAIL = 95_700, 664_200             # Jail Inmates in 2023 Table 5, midyear 2023
HELD_IN_JAILS = 65_552                       # Prisoners in 2023 Table 14, state+federal prisoners held in local jails


def gate(name: str, ok: bool, detail: str) -> None:
    print(f"  {'✓' if ok else '✗'} {name}: {detail}")
    if not ok:
        sys.exit(f"[BLOCKED] gate failed: {name}")


def key_for(jail_share: float, m_adj: float, tau: float, overlap: str = "none") -> tuple:
    """Combined Hispanic share and BJS key for a jail Hispanic share.

    overlap='none' keeps the cj lane's sum (the 65,552 prisoners held in jails sit in both counts);
    'prison_share' / 'jail_share' remove them at the prison or the jail Hispanic share."""
    h_jail = jail_share * N_JAIL
    num, den = H_PRISON + h_jail, N_PRISON + N_JAIL
    if overlap == "prison_share":
        num, den = num - HELD_IN_JAILS * H_PRISON / N_PRISON, den - HELD_IN_JAILS
    elif overlap == "jail_share":
        num, den = num - HELD_IN_JAILS * jail_share, den - HELD_IN_JAILS
    s = num / den
    return s, s * m_adj * tau


def main() -> None:
    cj = json.loads(CJ.read_text())
    sh, bjs = cj["shares"], cj["bjs"]
    prisons_bn = cj["sublines_bn"]["prisons"]
    central = sh["custody_acs_adj"]
    m_adj = cj["acs_m"]["m_adj"]
    print("[positive control]")
    gate("cj lane BJS inputs", (bjs["prison_hisp"], bjs["prison_total"], bjs["jail_hisp"], bjs["jail_total"],
                                bjs["held_in_local_jails_2023"]) == (H_PRISON, N_PRISON, H_JAIL, N_JAIL, HELD_IN_JAILS),
         "282,700/1,210,308 prisons; 95,700/664,200 jails; 65,552 held in jails")
    s0 = (H_PRISON + H_JAIL) / (N_PRISON + N_JAIL)
    gate("combined share 20.19%", abs(s0 - bjs["hisp_share"]) < 1e-15, f"{s0:.6f}")
    tau = sh["custody_bjs_adj"] / (s0 * m_adj)
    gate("tau = CPS target 18-64 / ACS Mexican household 18-64 = 1.0824", round(tau, 4) == 1.0824, f"{tau:.6f}")
    s_chk, k0 = key_for(H_JAIL / N_JAIL, m_adj, tau)
    gate("BJS check key reproduces 0.1428", abs(k0 - sh["custody_bjs_adj"]) < 1e-12 and round(k0, 4) == 0.1428,
         f"{k0:.6f} = {s_chk:.4f} x {m_adj:.4f} x {tau:.4f}")
    gate("adopted central prisons key 0.1419 on $121.32bn", round(central, 4) == 0.1419 and round(prisons_bn, 2) == 121.32,
         f"{central:.6f}, ${prisons_bn:.3f}bn")
    gate("BJS check arm vs central reproduces the lane's +$0.11bn (6.05 - 5.94)",
         abs((k0 - central) * prisons_bn - (cj["one_at_a_time_change_bn"]["prisons_custody_bjs_adj"]
                                          - cj["one_at_a_time_change_bn"]["central"])) < 1e-9,
         f"{(k0 - central) * prisons_bn:+.4f}bn")
    arr = pd.read_csv(ARRESTS)
    a24 = arr[(arr.year.astype(str) == "2024") & (arr.offence == "ALL_OFFENCES")].iloc[0]
    arrest24 = float(a24.eth_panel_hispanic) / float(a24.eth_panel_total)
    gate("FBI 2024 Table 43C adult Hispanic arrest share 22.1%", round(arrest24, 3) == 0.221, f"{arrest24:.5f}")
    s_a, k_a = key_for(arrest24, m_adj, tau)
    d_a = (k_a - central) * prisons_bn
    gate("audit arm: jail at the arrest share gives 0.162 and +$2.45bn vs central", round(k_a, 3) == 0.162
         and round(d_a, 2) == 2.45, f"key {k_a:.5f}, {d_a:+.3f}bn vs 0.1419 ({(k_a - k0) * prisons_bn:+.3f}bn vs 0.1428)")
    if not EST.exists():
        print(f"[stop] {EST.name} not built yet; positive control only")
        return
    est = pd.read_csv(EST)
    rows = []
    for r in est.itertuples():
        for ov in ("none", "prison_share", "jail_share"):
            s, k = key_for(r.jail_H_share, m_adj, tau, ov)
            rows.append({"method": r.method, "kind": r.kind, "overlap_rule": ov, "jail_H_share": r.jail_H_share,
                         "combined_prison_jail_H_share": s, "bjs_check_key": k,
                         "delta_key_vs_central": k - central,
                         "delta_bn_vs_central_prisons": (k - central) * prisons_bn,
                         "delta_bn_vs_bjs_check_0_1428": (k - k0) * prisons_bn})
    out = pd.DataFrame(rows)
    OUT.parent.mkdir(exist_ok=True)
    out.to_csv(OUT, index=False, lineterminator="\n", float_format="%.6f")
    print(out[out.overlap_rule == "none"][["method", "kind", "jail_H_share", "combined_prison_jail_H_share", "bjs_check_key",
                                           "delta_bn_vs_central_prisons", "delta_bn_vs_bjs_check_0_1428"]].to_string(index=False))
    print(f"\nwrote {OUT.relative_to(HERE)} ({len(out)} rows)")
    # [INFERENCE] if ACS institutional records under-record Hispanic (hence Mexican) origin by f, proportionally
    # across origins, the adopted ACS custody key scales by 1/f (numerator I_mex; I_all and HH_mex are unaffected).
    if RR.exists():
        rr = pd.read_csv(RR)
        rr["acs_key_corrected"] = central / rr.record_ratio_f
        rr["delta_bn_vs_central_prisons"] = (rr.acs_key_corrected - central) * prisons_bn
        rr.to_csv(SENS, index=False, lineterminator="\n", float_format="%.6f")
        print("\n[adopted ACS custody key / f]")
        print(rr[["instrument", "jail_method", "universe", "record_ratio_f", "acs_key_corrected",
                  "delta_bn_vs_central_prisons"]].to_string(index=False))
        print(f"wrote {SENS.relative_to(HERE)} ({len(rr)} rows)")


if __name__ == "__main__":
    main()
