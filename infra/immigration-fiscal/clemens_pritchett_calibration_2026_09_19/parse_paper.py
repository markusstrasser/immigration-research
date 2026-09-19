"""Parse Clemens-Pritchett Table 1 and the stated constants from the paper's own text.

Input : _cache/dp9730.txt  (pdftotext -layout of the pinned IZA DP 9730 PDF)
Output: derived/paper_table1.csv, derived/paper_constants.json

Nothing is typed in from memory: every number below is located by its row label
in the extracted text and parsed from that line.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TXT = os.path.join(HERE, "_cache", "dp9730.txt")
OUT = os.path.join(HERE, "derived")
os.makedirs(OUT, exist_ok=True)

NUM = re.compile(r"[−-]?\d+\.?\d*")


def nums(line):
    """All numbers on a line, with the PDF's U+2212 minus normalised."""
    return [float(t.replace("−", "-")) for t in NUM.findall(line)]


def row(lines, label, want, drop_leading=0):
    """Find the line starting (after indent) with `label` and carrying exactly
    `want` numbers. Figure panels reuse some labels, so the arity disambiguates;
    two different matches of the right arity is an error, not a silent pick."""
    hits = []
    for ln in lines:
        s = ln.strip()
        if drop_leading:
            parts = s.split(None, drop_leading)
            if len(parts) > drop_leading:
                s = parts[-1]
        if s.startswith(label):
            v = nums(s[len(label):])
            if len(v) == want:
                hits.append(v)
    uniq = {tuple(v) for v in hits}
    if len(uniq) == 1:
        return hits[0]
    raise SystemExit(f"row {label!r}: {len(uniq)} distinct matches with {want} numbers")


def main():
    lines = open(TXT, encoding="utf-8").read().splitlines()

    # --- country header of Table 1 -------------------------------------
    hdr = next(ln for ln in lines if "Bangladesh" in ln and "Somalia" in ln)
    countries = hdr.split()
    if len(countries) != 9:
        raise SystemExit(f"country header parsed to {countries}")

    # --- regression coefficients and the paper's own derived rows ------
    zeta = row(lines, "Foreign-born", 9)
    lam = row(lines, "Years in U.S.", 9)
    # this line carries a stray page number "35" from the PDF layout
    mu = row(lines, "(Years in U.S.)2", 9, drop_leading=1)
    delta = row(lines, "Initial earning diff. (δ)", 9)
    a = row(lines, "Indiv. assimilation (a)", 9)
    gamma_c = row(lines, "γ", 9)
    tau = row(lines, "Implied τ", 9)

    rows = []
    for i, c in enumerate(countries):
        rows.append({
            "country": c, "zeta": zeta[i], "lambda": lam[i], "mu": mu[i],
            "delta_paper": delta[i], "a_paper": a[i],
            "gamma_country": gamma_c[i], "tau_paper": tau[i],
        })
    rows.sort(key=lambda r: r["country"])

    cols = ["country", "zeta", "lambda", "mu", "delta_paper", "a_paper",
            "gamma_country", "tau_paper"]
    with open(os.path.join(OUT, "paper_table1.csv"), "w", encoding="utf-8") as fh:
        fh.write(",".join(cols) + "\n")
        for r in rows:
            fh.write(",".join(str(r[c]) for c in cols) + "\n")

    # --- stated constants, each located by its sentence ----------------
    text = " ".join(lines)
    text = re.sub(r"\s+", " ", text)

    def grab(pattern, name):
        m = re.search(pattern, text)
        if not m:
            raise SystemExit(f"constant {name} not found")
        return float(m.group(1).replace("−", "-"))

    const = {
        "gamma": grab(r"roughly γ = (0\.\d+)", "gamma"),
        "beta": grab(r"about β = (\d+) times larger", "beta"),
        "alpha": grab(r"close to α = (0\.\d+)", "alpha"),
        "rho": grab(r"discount rate ρ plausibly at (0\.\d+)", "rho"),
        "m0_observed": grab(r"roughly m0 = (0\.\d+)% of the destination", "m0") / 100.0,
        # text claim reproduced by the gate:
        "claim_c": grab(r"congestion rate c = (0\.\d+), if the transmission rate", "claim_c"),
        "claim_tau": grab(r"if the transmission rate τ < (0\.\d+)", "claim_tau"),
        "claim_a": grab(r"assimilation rate a > (0\.\d+)", "claim_a"),
        "claim_mstar": grab(r"then the optimal migration rate m∗ > (0\.\d+)", "claim_m"),
        "range_a_lo": grab(r"assimilation a lies in the range (0\.\d+) and", "a_lo"),
        "range_a_hi": grab(r"assimilation a lies in the range 0\.\d+ and (0\.\d+)", "a_hi"),
        "range_tau_lo": grab(r"transmission τ in the range (0\.\d+) to", "tau_lo"),
        "range_tau_hi": grab(r"transmission τ in the range 0\.\d+ to (0\.\d+)", "tau_hi"),
        "congestion_upper": grab(r"Figure 8 suggests that congestion c < (0\.\d+)", "c_up"),
        "delta_years_since_arrival": 5.0,  # "We measure productivity with earnings five years after arrival"
    }
    with open(os.path.join(OUT, "paper_constants.json"), "w", encoding="utf-8") as fh:
        json.dump(const, fh, indent=2, sort_keys=True)
        fh.write("\n")

    print(f"parsed {len(rows)} countries; constants: {sorted(const)}", file=sys.stderr)


if __name__ == "__main__":
    main()
