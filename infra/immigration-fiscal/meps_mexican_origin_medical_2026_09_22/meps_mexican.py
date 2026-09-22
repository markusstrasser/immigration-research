"""Mexican-origin vs all-donor public medical payments in the MEPS file the ledger transports.

The fiscal ledger's health transport (`../build/meps_health_transport_2024.py`,
`donor_model`) assigns every CPS record the mean public-payer spending of MEPS
donors matched on age band x US birth (x insurance status under 65). It carries
no ethnicity, income or Medicaid dimension. This lane measures, inside the very
same file, the same-cell ratio of Mexican-origin public payments to all-donor
public payments. A ratio different from 1 is the direct size of what that
transport misses for the Mexican-origin population.

Fixed-width parsing and the with-replacement stratified-PSU Taylor estimator
follow `../build/public_mvp_io.py::parse_meps_sas_fields` and
`../build/meps_health_transport_2024.py::donor_model`; the logic is copied here
with attribution rather than imported, so that neither module is touched.

Run from the repository root:
  OPENBLAS_NUM_THREADS=1 uv run --no-project python3 \
      infra/immigration-fiscal/meps_mexican_origin_medical_2026_09_22/meps_mexican.py
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

LANE = Path(__file__).resolve().parent
DERIVED = LANE / "derived"
REPO = LANE.parent.parent.parent
DATA = Path("/Users/alien/research-data/immigration-fiscal/data")

MEPS_2024_ZIP = DATA / "external/stage3/ahrq/meps_2024/h256dat.zip"
MEPS_2024_SAS = DATA / "external/stage3/ahrq/meps_2024/h256su.txt"
MEPS_2024_CB = DATA / "external/stage3/ahrq/meps_2024/h256cb.pdf"
MEPS_2023_ZIP = DATA / "external/stage3/ahrq/meps/h251dat.zip"
MEPS_2023_SAS = DATA / "external/stage3/ahrq/meps/h251su.txt"
CPI_CSV = DATA / "external/fred/cpi_all_urban.csv"

LEDGER = REPO / "infra/immigration-fiscal/ledger_absolute_2026_09_17"
COMPONENTS = LEDGER / "derived/age_profile_components.csv"
PROFILES = LEDGER / "derived/age_profiles.csv"
LEDGER_PARAMS = LEDGER / "params/params.json"
TRANSPORT = REPO / "infra/immigration-fiscal/build/meps_health_transport_2024.py"

# `read_meps` in the transport module, verbatim.
PUBLIC_PAYERS = ["TOTMCR", "TOTMCD", "TOTVA", "TOTTRI", "TOTOFD", "TOTSTL"]
MEASURES = {
    "public": None,          # sum of PUBLIC_PAYERS, built below
    "medicare": "TOTMCR",
    "medicaid": "TOTMCD",
    "out_of_pocket": "TOTSLF",
    "private": "TOTPRV",
    "total_all_sources": "TOTEXP",
}
BASE_FIELDS = ["AGE{y}X", "BORNUSA", "YRSINUS", "HISPANX", "HISPNCAT", "RACEV1X", "RACETHX",
               "PERWT{y}F", "VARSTR", "VARPSU", "INSURC{y}", "MCDEV{y}", "MCREV{y}",
               "TOTEXP{y}", "TOTSLF{y}", "TOTPRV{y}"] + [p + "{y}" for p in PUBLIC_PAYERS]

# Codebook anchors, MEPS HC-256 Codebook pp.108-109, 122, 469 (pdftotext -layout).
HISPNCAT_CODEBOOK = {
    1: ("MEXICAN/MEX AMER/CHICANO - NO OTHER HISP RPTD", 2679, 42446768),
    2: ("PUERTO RICAN - NO OTHER HISPANIC RPTD", 282, 5310040),
    3: ("CUBAN/CUBAN AMERICAN - NO OTHER HISPANIC RPTD", 144, 2030498),
    4: ("DOMINICAN - NO OTHER HISPANIC RPTD", 131, 2829667),
    5: ("CENTRAL OR SOUTH AMERICAN - NO OTHER HISPANIC RPTD", 588, 10298522),
    6: ("OTH LAT AM/HISP/LATINO/SPNSH ORGN-NO OTH", 216, 4168032),
    8: ("MULTIPLE HISPANIC GROUPS REPORTED", 76, 1522056),
    9: ("NON-HISPANIC", 15024, 271192047),
}
CODEBOOK_QUOTES = {
    "HISPNCAT": 'Name: HISPNCAT / Description: HISPANIC ETHNICITY (EDITED/IMPUTED) / Start: 211 / '
                '"1 MEXICAN/MEX AMER/CHICANO - NO OTHER HISP RPTD 2,679 42,446,768" ... '
                '"9 NON-HISPANIC 15,024 271,192,047" [h256cb.pdf p.109]',
    "HISPANX": 'Name: HISPANX / "1 HISPANIC 4,116 68,605,583" / "2 NOT HISPANIC 15,024 271,192,047" '
               '[h256cb.pdf p.108]',
    "RACEV1X": 'Name: RACEV1X / Description: RACE (EDITED/IMPUTED) / Start: 203 / '
               '"1 WHITE - NO OTHER RACE REPORTED 14,459 252,364,775" [h256cb.pdf p.107]',
    "RACETHX": 'Name: RACETHX / Description: RACE/ETHNICITY (EDITED/IMPUTED) / '
               '"2 NON-HISPANIC WHITE ONLY 10,766 191,692,001" [h256cb.pdf p.107]',
    "BORNUSA": 'Name: BORNUSA / Description: PERSON BORN IN THE US / Start: 278 / '
               '"1 YES 16,002 285,498,519" / "2 NO 3,050 52,835,316" [h256cb.pdf p.121]',
    "YRSINUS": 'Name: YRSINUS / Description: YEARS PERSON LIVED IN THE US / Start: 280 / '
               '"-1 INAPPLICABLE 16,090 286,962,313" ... "5 15 YEARS OR MORE 2,001 33,246,175" '
               '[h256cb.pdf p.121]',
    "AGE24X": 'Name: AGE24X / Description: AGE AS OF 12/31/24 (EDITED/IMPUTED) / Start: 192 / '
              '"-1 INAPPLICABLE 161 2,998,984" [h256cb.pdf p.99]',
    "MCDEV24": 'Name: MCDEV24 / Description: EVER HAVE MCAID/SCHIP DURING 2024 (ED) / Start: 2799 / '
               '"1 YES 4,941 78,147,553" / "2 NO 14,199 261,650,077" [h256cb.pdf p.469]',
    "MCREV24": 'Name: MCREV24 / Description: EVER HAVE MEDICARE DURING 2024 (ED) / Start: 2798 / '
               '"1 YES 5,469 70,105,211" / "2 NO 13,671 269,692,419" [h256cb.pdf p.469]',
    "INSURC24": 'Name: INSURC24 / Description: FULL YEAR INSURANCE COVERAGE STATUS 2024 / Start: 2806 / '
                '"1 <65 ANY PRIVATE" "2 <65 PUBLIC ONLY" "3 <65 UNINSURED" "4 65+ EDITED MEDICARE ONLY" '
                '[h256cb.pdf p.471]',
    "PERWT24F": 'Name: PERWT24F / Description: FINAL PERSON WEIGHT, 2024 / Start: 4599 / '
                '"0.000000 457" / "776.278855 - 91256.761356 18,683" [h256cb.pdf p.529]',
    "VARSTR": 'Name: VARSTR / Description: VARIANCE ESTIMATION STRATUM, 2024 / Start: 4635 / '
              '"2001 - 2117 19,140" [h256cb.pdf p.531]',
    "VARPSU": 'Name: VARPSU / Description: VARIANCE ESTIMATION PSU, 2024 / Start: 4639 / '
              '"1-7 19,140" [h256cb.pdf p.531]',
    "TOTMCR24": 'Name: TOTMCR24 / Description: TOTAL AMT PAID BY MEDICARE 24 / Start: 3208 [h256cb.pdf p.554]',
    "TOTMCD24": 'Name: TOTMCD24 / Description: TOTAL AMT PAID BY MEDICAID 24 / Start: 3214 [h256cb.pdf p.554]',
    "TOTVA24": 'Name: TOTVA24 / Description: TOTAL AMT PAID BY VA/CHAMPVA 24 / Start: 3227 [h256cb.pdf p.555]',
    "TOTTRI24": 'Name: TOTTRI24 / Description: TOTAL AMT PAID BY TRICARE 24 / Start: 3233 [h256cb.pdf p.555]',
    "TOTOFD24": 'Name: TOTOFD24 / Description: TOTAL AMT PAID BY OTHER FEDERAL 24 / Start: 3239 [h256cb.pdf p.555]',
    "TOTSTL24": 'Name: TOTSTL24 / Description: TOTAL AMT PAID BY OTH ST/LOCAL 24 / Start: 3244 [h256cb.pdf p.556]',
    "TOTSLF24": 'Name: TOTSLF24 / Description: TOTAL AMT PAID BY SELF/FAMILY 24 / Start: 3202 [h256cb.pdf p.553]',
    "TOTPRV24": 'Name: TOTPRV24 / Description: TOTAL AMT PAID BY PRIVATE INS 24 / Start: 3221 [h256cb.pdf p.554]',
    "TOTEXP24": 'Name: TOTEXP24 / Description: TOTAL HEALTH CARE EXP 24 / Start: 3195 [h256cb.pdf p.553]',
}

LEDGER_BAND_LABELS = ["0-17", "18-24", "25-34", "35-44", "45-54", "55-64", "65-74", "75+"]
TRANSPORT_BAND_LABELS = ["0-17", "18-34", "35-49", "50-64", "65+"]
Z95 = 1.959963984540054  # standard normal 0.975 quantile [CALCULATION: constant, no external source]


def _ok(msg):
    print(f"  ✓ {msg}")


def _header(s):
    print(f"\n[{s}]")


def fail(msg):
    print(f"  ✗ [BLOCKED] {msg}", file=sys.stderr)
    raise SystemExit(2)


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_sas_fields(su_path: Path) -> dict[str, tuple[int, int]]:
    """Copied from ../build/public_mvp_io.py::parse_meps_sas_fields."""
    fields: dict[str, tuple[int, int]] = {}
    for line in su_path.read_text(encoding="latin-1", errors="replace").splitlines():
        m = re.match(r"\s*@(\d+)\s+(\w+)\s+([\d.]+)", line)
        if not m:
            continue
        fields[m.group(2)] = (int(m.group(1)) - 1, int(float(m.group(3))))
    return fields


def age_band_transport(age):
    """Verbatim from ../build/meps_health_transport_2024.py::age_band."""
    return np.digitize(age, [18, 35, 50, 65])


def age_band_ledger(age):
    """Verbatim from ../ledger_absolute_2026_09_17/profile_export.py line 80."""
    return np.digitize(age, [18, 25, 35, 45, 55, 65, 75])


def read_meps(raw_zip: Path, sas: Path, yy: str) -> pd.DataFrame:
    """Fixed-width read following the transport module's `read_meps`."""
    layout = parse_sas_fields(sas)
    fields = [f.format(y=yy) for f in BASE_FIELDS]
    absent = [f for f in fields if f not in layout]
    if absent:
        fail(f"MEPS 20{yy} fields absent from {sas.name}: {absent}")
    with zipfile.ZipFile(raw_zip) as z:
        names = [n for n in z.namelist() if n.lower().endswith(".dat")]
        if len(names) != 1:
            fail(f"Expected exactly one MEPS ASCII member in {raw_zip.name}, got {names}")
        rows = []
        for line in z.open(names[0]):
            text = line.decode("ascii")
            rows.append({k: float(text[layout[k][0]:sum(layout[k])]) for k in fields})
    # Explicit rename map: strip the year suffix so 2023 and 2024 share column names.
    ren = {}
    for f in fields:
        base = f
        if f == f"AGE{yy}X":
            base = "AGE"
        elif f == f"PERWT{yy}F":
            base = "PERWT"
        elif f.endswith(yy):
            base = f[: -len(yy)]
        ren[f] = base
    d = pd.DataFrame(rows).rename(columns=ren)
    d["public"] = d[PUBLIC_PAYERS].sum(axis=1)
    d["year"] = int("20" + yy)
    return d


def gates_2024(d: pd.DataFrame) -> dict:
    """Fail loud on every published anchor the lane depends on."""
    g = {}
    _header("gates")
    if len(d) != 19140:
        fail(f"MEPS 2024 record count {len(d)} != 19,140")
    g["n_records"] = int(len(d))
    pos = int(d.PERWT.gt(0).sum())
    if pos != 18683:
        fail(f"positive-weight records {pos} != 18,683 [h256cb.pdf PERWT24F]")
    g["n_positive_weight"] = pos
    _ok(f"record counts: 19,140 rows, {pos:,} with PERWT24F > 0")

    hc = d.groupby("HISPNCAT").agg(n=("PERWT", "size"), w=("PERWT", "sum"))
    reproduced = {}
    for code, (label, n_exp, w_exp) in HISPNCAT_CODEBOOK.items():
        if code not in hc.index:
            fail(f"HISPNCAT code {code} absent from the data")
        n_got, w_got = int(hc.loc[code, "n"]), float(hc.loc[code, "w"])
        if n_got != n_exp or abs(w_got - w_exp) > 1:
            fail(f"HISPNCAT {code} ({label}): got {n_got}/{w_got:,.0f}, "
                 f"codebook {n_exp}/{w_exp:,.0f}")
        reproduced[str(code)] = {"label": label, "unweighted": n_got, "weighted": round(w_got, 2)}
    g["hispncat_codebook"] = reproduced
    _ok("HISPNCAT: all 8 codebook categories reproduce exactly (unweighted and weighted)")

    anchors = {"all": (np.ones(len(d), bool), 339797630),
               "born_us": (d.BORNUSA.eq(1).to_numpy(), 285498519),
               "born_elsewhere": (d.BORNUSA.eq(2).to_numpy(), 52835316)}
    got = {}
    for label, (mask, expected) in anchors.items():
        value = float(d.loc[mask, "PERWT"].sum())
        if abs(value - expected) > 1:
            fail(f"nativity anchor {label}: {value:,.0f} vs transport's {expected:,}")
        got[label] = round(value, 2)
    g["nativity_anchors"] = got
    _ok("nativity anchors match the transport: born_us 285,498,519 / born_elsewhere 52,835,316")

    nhw = d.HISPANX.eq(2) & d.RACEV1X.eq(1)
    if int(nhw.sum()) != int(d.RACETHX.eq(2).sum()) or int(nhw.sum()) != 10766:
        fail(f"nh_white definition {int(nhw.sum())} != RACETHX==2 {int(d.RACETHX.eq(2).sum())} / 10,766")
    if abs(float(d.loc[nhw, "PERWT"].sum()) - 191692001) > 1:
        fail("nh_white weighted total != 191,692,001 [h256cb.pdf RACETHX]")
    g["nh_white_equals_racethx2"] = {"unweighted": 10766, "weighted": 191692001.0}
    _ok("nh_white = HISPANX 2 & RACEV1X 1 reproduces RACETHX 2 exactly (10,766 / 191,692,001)")

    if d.VARSTR.isna().any() or d.VARPSU.isna().any():
        fail("VARSTR/VARPSU missing on some records")
    if not (d.VARSTR.between(2001, 2117).all() and d.VARPSU.between(1, 7).all()):
        fail("VARSTR/VARPSU outside the codebook ranges 2001-2117 / 1-7")
    design = d.loc[d.PERWT.gt(0), ["VARSTR", "VARPSU"]].drop_duplicates()
    per_stratum = design.groupby("VARSTR").size()
    if (per_stratum < 2).any():
        fail(f"lonely PSU strata: {per_stratum[per_stratum < 2].index.tolist()}")
    g["design"] = {"n_strata": int(len(per_stratum)), "n_psu": int(len(design)),
                   "min_psu_per_stratum": int(per_stratum.min()),
                   "max_psu_per_stratum": int(per_stratum.max())}
    _ok(f"design: {len(per_stratum)} strata, {len(design)} PSUs, min {per_stratum.min()} PSU/stratum")

    if (d[PUBLIC_PAYERS] < 0).any().any():
        fail("negative/reserved public-payer value present; no silent zero substitution")
    _ok("no negative or reserved public-payer values")

    if not set(d.MCDEV.unique()).issubset({1.0, 2.0}):
        fail(f"MCDEV24 carries codes outside 1/2: {sorted(d.MCDEV.unique())}")
    mcd_yes = int(d.MCDEV.eq(1).sum())
    if mcd_yes != 4941 or abs(float(d.loc[d.MCDEV.eq(1), "PERWT"].sum()) - 78147553) > 1:
        fail(f"MCDEV24==1 {mcd_yes}/{d.loc[d.MCDEV.eq(1),'PERWT'].sum():,.0f} != 4,941/78,147,553")
    g["mcdev_codebook"] = {"unweighted": 4941, "weighted": 78147553.0}
    _ok("MCDEV24 reproduces the codebook (4,941 / 78,147,553 ever covered)")
    return g


# ---------------------------------------------------------------------------
# Design-based estimation: with-replacement stratified-PSU Taylor linearization,
# the same estimator `donor_model` uses in the transport module.
# ---------------------------------------------------------------------------
class Design:
    def __init__(self, d: pd.DataFrame):
        self.n = len(d)
        self.w = d.PERWT.to_numpy(dtype=float)
        frame = d.loc[d.PERWT.gt(0), ["VARSTR", "VARPSU"]].drop_duplicates().sort_values(
            ["VARSTR", "VARPSU"]).reset_index(drop=True)
        self.frame = frame
        key = {(int(s), int(p)): j for j, (s, p) in enumerate(zip(frame.VARSTR, frame.VARPSU))}
        self.psu_index = np.array([key.get((int(s), int(p)), -1)
                                   for s, p in zip(d.VARSTR, d.VARPSU)])
        self.n_psu = len(frame)
        self.stratum_of_psu = frame.VARSTR.to_numpy()
        self.strata = np.unique(self.stratum_of_psu)
        self._groups = [np.where(self.stratum_of_psu == h)[0] for h in self.strata]

    def psu_totals(self, z: np.ndarray) -> np.ndarray:
        """Sum record-level influence values to PSU totals (records with zero
        weight carry zero influence, so an unmapped PSU contributes nothing)."""
        z = np.atleast_2d(z.T).T if z.ndim == 1 else z
        out = np.zeros((self.n_psu, z.shape[1]))
        keep = self.psu_index >= 0
        np.add.at(out, self.psu_index[keep], z[keep])
        return out

    def variance(self, z: np.ndarray) -> np.ndarray:
        """V = sum_h n_h/(n_h-1) sum_a (z_ha - zbar_h)^2, per column."""
        single = z.ndim == 1
        Z = z[:, None] if single else z
        tot = self.psu_totals(Z)
        var = np.zeros(Z.shape[1])
        for idx in self._groups:
            nh = len(idx)
            block = tot[idx]
            centered = block - block.mean(axis=0)
            var += nh / (nh - 1) * (centered ** 2).sum(axis=0)
        return var[0] if single else var


def mean_influence(y: np.ndarray, w: np.ndarray, mask: np.ndarray):
    """Weighted mean over a domain, and its linearized influence values."""
    wm = w * mask
    W = wm.sum()
    if W <= 0:
        return np.nan, np.zeros(len(w)), 0.0, 0
    theta = float((wm * y).sum() / W)
    z = wm * (y - theta) / W
    return theta, z, float(W), int(mask.sum())


def combo_influence(parts):
    """Linear combination sum_j a_j * theta_j with composed influence values."""
    value = 0.0
    z = None
    for a, (theta, zj) in parts:
        value += a * theta
        z = a * zj if z is None else z + a * zj
    return value, z


def ratio_influence(num, den):
    """Ratio of two (possibly composite) estimates; delta method on influences."""
    (tn, zn), (td, zd) = num, den
    if not np.isfinite(tn) or not np.isfinite(td) or td == 0:
        return np.nan, np.zeros(len(zn))
    r = tn / td
    return r, (zn - r * zd) / td


def rao_wu_bootstrap(design: Design, y: np.ndarray, w: np.ndarray,
                     mask_num: np.ndarray, mask_den: np.ndarray, reps: int, seed: int) -> float:
    """Rao-Wu(n_h - 1) rescaling bootstrap over PSUs within strata.

    Drawing m_h = n_h - 1 PSUs with replacement and rescaling by n_h/(n_h - 1)
    reproduces the with-replacement linearization variance in expectation, so
    agreement between the two is a real check on the linearization code.
    """
    rng = np.random.default_rng(seed)
    groups = design._groups
    out = np.empty(reps)
    for b in range(reps):
        lam = np.zeros(design.n_psu)
        for idx in groups:
            nh = len(idx)
            draws = rng.integers(0, nh, size=nh - 1)
            counts = np.bincount(draws, minlength=nh)
            lam[idx] = counts * nh / (nh - 1)
        rec = np.where(design.psu_index >= 0, lam[design.psu_index], 0.0)
        wb = w * rec
        wn, wd = wb * mask_num, wb * mask_den
        out[b] = ((wn * y).sum() / wn.sum()) / ((wd * y).sum() / wd.sum())
    return float(out.std(ddof=1))


# ---------------------------------------------------------------------------
def build_domains(d: pd.DataFrame) -> list[dict]:
    """The transport's own cells, the ledger's bands, and the pooled domains."""
    tb = age_band_transport(d.AGE.to_numpy())
    lb = age_band_ledger(d.AGE.to_numpy())
    born = d.BORNUSA.to_numpy()
    age = d.AGE.to_numpy()
    mcd = d.MCDEV.to_numpy()
    valid = (d.PERWT.to_numpy() > 0) & (age >= 0) & np.isin(born, [1, 2])  # transport's valid set

    doms = []
    for b in range(5):
        for nat, natlab in [(1, "us_born"), (2, "foreign_born"), (0, "both")]:
            m = valid & (tb == b) & (born == nat if nat else True)
            doms.append(dict(scheme="transport", band=b, band_label=TRANSPORT_BAND_LABELS[b],
                             nativity=natlab, subgroup="all", mask=m))
    for b in range(8):
        for nat, natlab in [(1, "us_born"), (2, "foreign_born"), (0, "both")]:
            m = valid & (lb == b) & (born == nat if nat else True)
            doms.append(dict(scheme="ledger", band=b, band_label=LEDGER_BAND_LABELS[b],
                             nativity=natlab, subgroup="all", mask=m))
    for label, agemask in [("all_ages", valid), ("65plus", valid & (age >= 65)),
                           ("18_64", valid & (age >= 18) & (age < 65)),
                           ("under18", valid & (age < 18))]:
        for nat, natlab in [(1, "us_born"), (2, "foreign_born"), (0, "both")]:
            doms.append(dict(scheme="pooled", band=label, band_label=label, nativity=natlab,
                             subgroup="all", mask=agemask & (born == nat if nat else True)))
    for label, agemask in [("65plus", valid & (age >= 65)),
                           ("18_64", valid & (age >= 18) & (age < 65)),
                           ("all_ages", valid)]:
        for sub, submask in [("medicaid_ever", mcd == 1), ("no_medicaid", mcd == 2)]:
            doms.append(dict(scheme="pooled", band=label, band_label=label, nativity="both",
                             subgroup=sub, mask=agemask & submask))
    return doms


def group_masks(d: pd.DataFrame) -> dict[str, np.ndarray]:
    return {
        "mexican_origin": d.HISPNCAT.eq(1).to_numpy(),
        "nh_white": (d.HISPANX.eq(2) & d.RACEV1X.eq(1)).to_numpy(),
        "all_donors": np.ones(len(d), bool),
    }


def estimate(d: pd.DataFrame, design: Design):
    """Every domain x group x measure mean, with its influence column."""
    w = d.PERWT.to_numpy(dtype=float)
    ys = {"public": d.public.to_numpy(dtype=float)}
    for name, col in MEASURES.items():
        if col:
            ys[name] = d[col].to_numpy(dtype=float)
    ys["share_medicaid_ever"] = d.MCDEV.eq(1).to_numpy(dtype=float)

    groups = group_masks(d)
    store, rows = {}, []
    for dom in build_domains(d):
        for gname, gmask in groups.items():
            mask = dom["mask"] & gmask
            rec = dict(scheme=dom["scheme"], band=dom["band"], band_label=dom["band_label"],
                       nativity=dom["nativity"], subgroup=dom["subgroup"], group=gname)
            n = int(mask.sum())
            pop = float(w[mask].sum())
            rec["n"], rec["population"] = n, pop
            for mname, y in ys.items():
                theta, z, W, _ = mean_influence(y, w, mask)
                store[(dom["scheme"], dom["band"], dom["nativity"], dom["subgroup"], gname, mname)] = (theta, z)
                rec[f"mean_{mname}"] = theta
                rec[f"se_{mname}"] = float(np.sqrt(design.variance(z))) if n else np.nan
            rows.append(rec)
    return pd.DataFrame(rows), store


def build_ratios(store, design: Design, cells: pd.DataFrame) -> pd.DataFrame:
    keys = cells[["scheme", "band", "nativity", "subgroup"]].drop_duplicates()
    measures = ["public", "medicare", "medicaid", "out_of_pocket", "private",
                "total_all_sources", "share_medicaid_ever"]
    rows = []
    counts = cells.set_index(["scheme", "band", "nativity", "subgroup", "group"]).n
    for _, k in keys.iterrows():
        sc, bd, nat, sub = k.scheme, k.band, k.nativity, k.subgroup
        for den in ("nh_white", "all_donors"):
            for m in measures:
                num = store[(sc, bd, nat, sub, "mexican_origin", m)]
                dn = store[(sc, bd, nat, sub, den, m)]
                r, z = ratio_influence(num, dn)
                se = float(np.sqrt(design.variance(z))) if np.isfinite(r) else np.nan
                diff, zd = combo_influence([(1.0, num), (-1.0, dn)])
                se_diff = float(np.sqrt(design.variance(zd))) if np.isfinite(diff) else np.nan
                rows.append(dict(
                    scheme=sc, band=bd, band_label=cells.loc[
                        (cells.scheme == sc) & (cells.band == bd), "band_label"].iloc[0],
                    nativity=nat, subgroup=sub, denominator=den, measure=m,
                    ratio=r, se=se, ci_lo=r - Z95 * se if np.isfinite(r) else np.nan,
                    ci_hi=r + Z95 * se if np.isfinite(r) else np.nan,
                    excludes_one=bool(np.isfinite(r) and (r - Z95 * se > 1 or r + Z95 * se < 1)),
                    difference=diff, se_difference=se_diff,
                    n_mexican=int(counts.get((sc, bd, nat, sub, "mexican_origin"), 0)),
                    n_denominator=int(counts.get((sc, bd, nat, sub, den), 0))))
    return pd.DataFrame(rows)


def coverage_standardized(d: pd.DataFrame, design: Design, store) -> pd.DataFrame:
    """How much of the gap is Medicaid-coverage composition rather than spending?

    Direct standardization: hold the Medicaid-coverage mix at the all-donor mix
    and recompute the ratio. The difference from the pooled ratio is the part of
    the gap that comes from Mexican-origin people being likelier to be covered,
    not from spending more inside either coverage stratum. The standard weights
    are the all-donor coverage shares, treated as fixed.
    """
    w = d.PERWT.to_numpy(dtype=float)
    age, born, mcd = d.AGE.to_numpy(), d.BORNUSA.to_numpy(), d.MCDEV.to_numpy()
    valid = (w > 0) & (age >= 0) & np.isin(born, [1, 2])
    rows = []
    for label, agemask in [("65plus", valid & (age >= 65)),
                           ("18_64", valid & (age >= 18) & (age < 65)),
                           ("all_ages", valid)]:
        shares = {}
        for sub, sm in [("medicaid_ever", mcd == 1), ("no_medicaid", mcd == 2)]:
            shares[sub] = float(w[agemask & sm].sum()) / float(w[agemask].sum())
        for den in ("nh_white", "all_donors"):
            for m in ("public", "total_all_sources"):
                num = combo_influence([(shares[s], store[("pooled", label, "both", s, "mexican_origin", m)])
                                       for s in shares])
                dn = combo_influence([(shares[s], store[("pooled", label, "both", s, den, m)])
                                      for s in shares])
                r, z = ratio_influence(num, dn)
                se = float(np.sqrt(design.variance(z)))
                pooled = store[("pooled", label, "both", "all", "mexican_origin", m)][0] / \
                    store[("pooled", label, "both", "all", den, m)][0]
                rows.append(dict(scheme="pooled", band=label, band_label=label, nativity="both",
                                 subgroup="coverage_standardized", denominator=den, measure=m,
                                 ratio=r, se=se, ci_lo=r - Z95 * se, ci_hi=r + Z95 * se,
                                 excludes_one=bool(r - Z95 * se > 1 or r + Z95 * se < 1),
                                 difference=np.nan, se_difference=np.nan,
                                 pooled_ratio=pooled, coverage_composition_part=pooled - r,
                                 standard_share_medicaid_ever=shares["medicaid_ever"],
                                 n_mexican=int((agemask & d.HISPNCAT.eq(1).to_numpy()).sum()),
                                 n_denominator=int((agemask & (np.ones(len(d), bool) if den == "all_donors"
                                                    else (d.HISPANX.eq(2) & d.RACEV1X.eq(1)).to_numpy())).sum())))
    return pd.DataFrame(rows)


def drop_top1_ratios(d: pd.DataFrame) -> dict[int, float]:
    """Each ledger band's public ratio with its single largest Mexican-origin
    weighted contributor removed. MEPS top-codes costs, so one retained record
    can carry a cell; this is a leave-one-out, not an outlier rule."""
    w = d.PERWT.to_numpy(dtype=float)
    age, born = d.AGE.to_numpy(), d.BORNUSA.to_numpy()
    lb = age_band_ledger(age)
    valid = (w > 0) & (age >= 0) & np.isin(born, [1, 2])
    mex = d.HISPNCAT.eq(1).to_numpy()
    y = d.public.to_numpy(dtype=float)
    out = {}
    for b in range(8):
        bm = valid & (lb == b)
        cand = np.where(bm & mex)[0]
        drop = cand[np.argmax((w * y)[cand])]
        keep = np.ones(len(d), bool)
        keep[drop] = False
        num = (w * y)[bm & mex & keep].sum() / w[bm & mex & keep].sum()
        den = (w * y)[bm & keep].sum() / w[bm & keep].sum()
        # the same concentration statistic for the whole band, as a yardstick
        allc = np.where(bm)[0]
        adrop = allc[np.argmax((w * y)[allc])]
        out[b] = dict(ratio=float(num / den), dropped_public=float(y[drop]),
                      dropped_weight=float(w[drop]), dropped_age=float(age[drop]),
                      n_mexican=int((bm & mex).sum()), n_all_donors=int(bm.sum()),
                      dropped_share_of_mexican_band_mean=float(
                          (w[drop] * y[drop]) / w[bm & mex].sum() /
                          ((w * y)[bm & mex].sum() / w[bm & mex].sum())),
                      all_donor_top1_share_of_band_mean=float(
                          (w[adrop] * y[adrop]) / w[bm].sum() /
                          ((w * y)[bm].sum() / w[bm].sum())))
    return out


def ledger_translation(store, design: Design, cells: pd.DataFrame, audit: dict,
                       drop1: dict) -> pd.DataFrame:
    """Rescale the union's medical and M cells by the same-band MEPS ratio."""
    comp = pd.read_csv(COMPONENTS)
    prof = pd.read_csv(PROFILES)
    sel = (comp.allocation == "shared") & (comp.account == "expanded")
    union = comp[sel & (comp.group == "mexican_observed_total")]
    med = union[union.component == "medical"].set_index("band").signed_total
    mitem = union[union.component == "M"].set_index("band").signed_total

    psel = (prof.allocation == "personal") & (prof.account == "expanded")
    pop = {g: prof[psel & (prof.group == g)].set_index("band").population
           for g in ("mexican_observed_total", "mexico_born", "mexican_second_gen",
                     "mexican_third_plus_selfid")}
    parts = pop["mexico_born"] + pop["mexican_second_gen"] + pop["mexican_third_plus_selfid"]
    if (abs(parts - pop["mexican_observed_total"]) > 1).any():
        fail("union population != mexico_born + second_gen + third_plus_selfid by band")
    audit["nativity_mix_source"] = (
        "age_profile_components.csv carries no nativity split for mexican_observed_total, so the "
        "union's own per-band foreign-born share is taken from age_profiles.csv as "
        "population(mexico_born) / population(mexican_observed_total); the three sub-group "
        "populations sum to the union's exactly in every band (checked).")

    r_mcd = json.loads(LEDGER_PARAMS.read_text())["meps_coverage"]["nhea_to_meps_ratio_medicaid"]["value"]
    r_mcr = json.loads(LEDGER_PARAMS.read_text())["meps_coverage"]["nhea_to_meps_ratio_medicare"]["value"]
    audit["nhea_ratios"] = {"medicaid": r_mcd, "medicare": r_mcr,
                            "source": "ledger_absolute_2026_09_17/params/params.json meps_coverage"}

    rows, z_med_total, z_m_total = [], None, None
    for b in range(8):
        s = float(pop["mexico_born"].loc[b] / pop["mexican_observed_total"].loc[b])
        wts = [(s, "foreign_born"), (1 - s, "us_born")]
        # public: ratio of nativity-mixed Mexican-origin mean to nativity-mixed all-donor mean
        num = combo_influence([(a, store[("ledger", b, nat, "all", "mexican_origin", "public")])
                               for a, nat in wts])
        den = combo_influence([(a, store[("ledger", b, nat, "all", "all_donors", "public")])
                               for a, nat in wts])
        r_pub, z_pub = ratio_influence(num, den)
        se_pub = float(np.sqrt(design.variance(z_pub)))

        # item M is a fixed linear form in the Medicaid and Medicare donor means:
        #   M  ~  mcd*(r_mcd-1) + mcr*(r_mcr-1)
        mnum = combo_influence(
            [(a * (r_mcd - 1), store[("ledger", b, nat, "all", "mexican_origin", "medicaid")]) for a, nat in wts]
            + [(a * (r_mcr - 1), store[("ledger", b, nat, "all", "mexican_origin", "medicare")]) for a, nat in wts])
        mden = combo_influence(
            [(a * (r_mcd - 1), store[("ledger", b, nat, "all", "all_donors", "medicaid")]) for a, nat in wts]
            + [(a * (r_mcr - 1), store[("ledger", b, nat, "all", "all_donors", "medicare")]) for a, nat in wts])
        r_m, z_m = ratio_influence(mnum, mden)
        se_m = float(np.sqrt(design.variance(z_m)))

        c_med, c_m = float(med.loc[b]), float(mitem.loc[b])
        d_med, d_m = c_med * (r_pub - 1), c_m * (r_m - 1)
        zm_med, zm_m = c_med * z_pub, c_m * z_m
        z_med_total = zm_med if z_med_total is None else z_med_total + zm_med
        z_m_total = zm_m if z_m_total is None else z_m_total + zm_m
        nmex = int(cells[(cells.scheme == "ledger") & (cells.band == b) &
                         (cells.nativity == "both") & (cells.group == "mexican_origin")].n.iloc[0])
        rows.append(dict(
            band=b, band_label=LEDGER_BAND_LABELS[b],
            union_population=float(pop["mexican_observed_total"].loc[b]),
            foreign_born_share=s, n_mexican_donors=nmex,
            ledger_medical_bn=c_med / 1e9, ledger_M_bn=c_m / 1e9,
            ratio_public=r_pub, se_ratio_public=se_pub,
            ratio_M=r_m, se_ratio_M=se_m,
            delta_medical_bn=d_med / 1e9,
            se_delta_medical_bn=float(np.sqrt(design.variance(zm_med))) / 1e9,
            delta_M_bn=d_m / 1e9,
            se_delta_M_bn=float(np.sqrt(design.variance(zm_m))) / 1e9,
            delta_total_bn=(d_med + d_m) / 1e9,
            se_delta_total_bn=float(np.sqrt(design.variance(zm_med + zm_m))) / 1e9,
            ratio_public_drop_top1=drop1[b]["ratio"],
            delta_medical_bn_drop_top1=c_med * (drop1[b]["ratio"] - 1) / 1e9))

    df = pd.DataFrame(rows)
    for label, sel_bands in [("65plus", [6, 7]), ("all_bands", list(range(8)))]:
        zsel_med = zsel_m = None
        for b in sel_bands:
            c_med, c_m = float(med.loc[b]), float(mitem.loc[b])
            s = float(pop["mexico_born"].loc[b] / pop["mexican_observed_total"].loc[b])
            wts = [(s, "foreign_born"), (1 - s, "us_born")]
            num = combo_influence([(a, store[("ledger", b, nat, "all", "mexican_origin", "public")]) for a, nat in wts])
            den = combo_influence([(a, store[("ledger", b, nat, "all", "all_donors", "public")]) for a, nat in wts])
            _, zp = ratio_influence(num, den)
            mnum = combo_influence(
                [(a * (r_mcd - 1), store[("ledger", b, nat, "all", "mexican_origin", "medicaid")]) for a, nat in wts]
                + [(a * (r_mcr - 1), store[("ledger", b, nat, "all", "mexican_origin", "medicare")]) for a, nat in wts])
            mden = combo_influence(
                [(a * (r_mcd - 1), store[("ledger", b, nat, "all", "all_donors", "medicaid")]) for a, nat in wts]
                + [(a * (r_mcr - 1), store[("ledger", b, nat, "all", "all_donors", "medicare")]) for a, nat in wts])
            _, zmm = ratio_influence(mnum, mden)
            zsel_med = c_med * zp if zsel_med is None else zsel_med + c_med * zp
            zsel_m = c_m * zmm if zsel_m is None else zsel_m + c_m * zmm
        sub = df[df.band.isin(sel_bands)]
        df = pd.concat([df, pd.DataFrame([dict(
            band=-1 if label == "all_bands" else -2, band_label=label,
            union_population=sub.union_population.sum(),
            foreign_born_share=np.nan, n_mexican_donors=int(sub.n_mexican_donors.sum()),
            ledger_medical_bn=sub.ledger_medical_bn.sum(), ledger_M_bn=sub.ledger_M_bn.sum(),
            ratio_public=np.nan, se_ratio_public=np.nan, ratio_M=np.nan, se_ratio_M=np.nan,
            delta_medical_bn=sub.delta_medical_bn.sum(),
            se_delta_medical_bn=float(np.sqrt(design.variance(zsel_med))) / 1e9,
            delta_M_bn=sub.delta_M_bn.sum(),
            se_delta_M_bn=float(np.sqrt(design.variance(zsel_m))) / 1e9,
            delta_total_bn=sub.delta_total_bn.sum(),
            se_delta_total_bn=float(np.sqrt(design.variance(zsel_med + zsel_m))) / 1e9,
            ratio_public_drop_top1=np.nan,
            delta_medical_bn_drop_top1=sub.delta_medical_bn_drop_top1.sum())])],
            ignore_index=True)
    return df


def pooled_2023_check(audit: dict) -> dict:
    """65+ only: pool HC-251 with HC-256 at half weight, CPI-U deflated."""
    d23 = read_meps(MEPS_2023_ZIP, MEPS_2023_SAS, "23")
    cpi = pd.read_csv(CPI_CSV)
    cpi["yr"] = cpi.observation_date.str.slice(0, 4).astype(int)
    a23 = float(cpi[cpi.yr == 2023].CPIAUCSL.mean())
    a24 = float(cpi[cpi.yr == 2024].CPIAUCSL.mean())
    if not (cpi.yr == 2023).sum() == 12 or not (cpi.yr == 2024).sum() == 12:
        fail("CPI-U file does not carry 12 monthly observations for 2023 and 2024")
    factor = a24 / a23
    d24 = read_meps(MEPS_2024_ZIP, MEPS_2024_SAS, "24")
    for col in ["public", "TOTMCD", "TOTMCR"]:
        d23[col] = d23[col] * factor
    d23["VARSTR"] = d23.VARSTR + 10000  # 2023 and 2024 strata are separate samples
    pool = pd.concat([d23.assign(PERWT=d23.PERWT * 0.5),
                      d24.assign(PERWT=d24.PERWT * 0.5)], ignore_index=True)
    des = Design(pool)
    w = pool.PERWT.to_numpy(dtype=float)
    age = pool.AGE.to_numpy()
    valid = (w > 0) & (age >= 65) & np.isin(pool.BORNUSA.to_numpy(), [1, 2])
    y = pool.public.to_numpy(dtype=float)
    out = {"cpi_2023_annual_avg": a23, "cpi_2024_annual_avg": a24, "deflator_2023_to_2024": factor,
           "cpi_source": "external/fred/cpi_all_urban.csv (CPIAUCSL monthly, annual mean)"}
    gm = pool.HISPNCAT.eq(1).to_numpy()
    for den, dmask in [("nh_white", (pool.HISPANX.eq(2) & pool.RACEV1X.eq(1)).to_numpy()),
                       ("all_donors", np.ones(len(pool), bool))]:
        num = mean_influence(y, w, valid & gm)[:2]
        dd = mean_influence(y, w, valid & dmask)[:2]
        r, z = ratio_influence(num, dd)
        out[f"pooled_65plus_public_ratio_vs_{den}"] = {
            "ratio": r, "se": float(np.sqrt(des.variance(z))),
            "n_mexican": int((valid & gm).sum()), "n_denominator": int((valid & dmask).sum())}
    return out


def main():
    DERIVED.mkdir(parents=True, exist_ok=True)
    audit = {"lane": LANE.name, "generated_for_income_year": 2024,
             "inputs": {p.name: {"path": str(p), "sha256": sha256(p)} for p in
                        [MEPS_2024_ZIP, MEPS_2024_SAS, MEPS_2023_ZIP, MEPS_2023_SAS,
                         COMPONENTS, PROFILES, LEDGER_PARAMS, TRANSPORT, CPI_CSV]},
             "codebook_quotes": CODEBOOK_QUOTES,
             "band_definitions": {
                 "transport": "np.digitize(age, [18, 35, 50, 65]) -- verbatim from "
                              "build/meps_health_transport_2024.py::age_band",
                 "ledger": "np.digitize(age, [18, 25, 35, 45, 55, 65, 75]) -- verbatim from "
                           "ledger_absolute_2026_09_17/profile_export.py line 80"},
             "groups": {
                 "mexican_origin": "HISPNCAT == 1 (MEXICAN/MEX AMER/CHICANO - NO OTHER HISP RPTD)",
                 "nh_white": "HISPANX == 2 and RACEV1X == 1; identical to RACETHX == 2",
                 "all_donors": "the transport's valid set: PERWT24F > 0, AGE24X >= 0, BORNUSA in (1,2)"},
             "public_payer_definition": "TOTMCR24 + TOTMCD24 + TOTVA24 + TOTTRI24 + TOTOFD24 + TOTSTL24, "
                                        "the transport's PUBLIC_PAYERS list"}

    _header("read")
    d = read_meps(MEPS_2024_ZIP, MEPS_2024_SAS, "24")
    _ok(f"MEPS HC-256 parsed: {len(d):,} records, {len(d.columns)} fields")
    audit["gates"] = gates_2024(d)

    _header("estimate")
    design = Design(d)
    cells, store = estimate(d, design)
    cells.to_csv(DERIVED / "cells.csv", index=False)
    _ok(f"cells.csv: {len(cells):,} domain x group rows")

    ratios = build_ratios(store, design, cells)
    ratios = pd.concat([ratios, coverage_standardized(d, design, store)], ignore_index=True)
    ratios.to_csv(DERIVED / "ratios.csv", index=False)
    _ok(f"ratios.csv: {len(ratios):,} ratio rows")

    _header("se validation")
    w = d.PERWT.to_numpy(dtype=float)
    age, born = d.AGE.to_numpy(), d.BORNUSA.to_numpy()
    valid = (w > 0) & (age >= 0) & np.isin(born, [1, 2])
    mnum = valid & (age >= 65) & d.HISPNCAT.eq(1).to_numpy()
    mden = valid & (age >= 65)
    lin = ratios[(ratios.scheme == "pooled") & (ratios.band == "65plus") &
                 (ratios.nativity == "both") & (ratios.subgroup == "all") &
                 (ratios.denominator == "all_donors") & (ratios.measure == "public")]
    se_lin = float(lin.se.iloc[0])
    reps = 2000
    se_boot = rao_wu_bootstrap(design, d.public.to_numpy(dtype=float), w, mnum, mden, reps, seed=20260922)
    audit["se_validation"] = {
        "cell": "65+, both nativities, mexican_origin / all_donors, public payments",
        "linearized_se": se_lin, "bootstrap_se": se_boot, "bootstrap_replicates": reps,
        "bootstrap_method": "Rao-Wu(n_h - 1) rescaling bootstrap over PSUs within strata; "
                            "multiplier n_h/(n_h-1) times the multinomial count",
        "relative_difference": abs(se_boot - se_lin) / se_lin,
        "formula_status": "the with-replacement stratified-PSU linearization is the estimator "
                          "build/meps_health_transport_2024.py::donor_model already uses; the "
                          "bootstrap is an independent check of this implementation, not a "
                          "second published method"}
    _ok(f"65+ public ratio SE: linearized {se_lin:.4f}, Rao-Wu bootstrap {se_boot:.4f} "
        f"({abs(se_boot - se_lin) / se_lin:.1%} apart, {reps} replicates)")
    if abs(se_boot - se_lin) / se_lin > 0.20:
        fail(f"linearized and bootstrap SEs disagree by more than 20%: {se_lin} vs {se_boot}")

    _header("outlier sensitivity")
    drop1 = drop_top1_ratios(d)
    audit["leave_one_out"] = {
        "method": "each ledger band's mexican_origin / all_donors public ratio recomputed with "
                  "that band's single largest Mexican-origin weighted contributor removed",
        "note": "MEPS top-codes total expenditures; a single retained record can carry a small "
                "cell. Point values only: a leave-one-out has no design-based standard error.",
        "bands": {str(b): v for b, v in drop1.items()}}
    worst = max(drop1.items(), key=lambda kv: kv[1]["dropped_share_of_mexican_band_mean"])
    _ok(f"band {worst[0]} ({LEDGER_BAND_LABELS[worst[0]]}): one record supplies "
        f"{worst[1]['dropped_share_of_mexican_band_mean']:.1%} of the Mexican-origin mean; "
        f"ratio {drop1[worst[0]]['ratio']:.3f} without it")

    _header("ledger translation")
    trans = ledger_translation(store, design, cells, audit, drop1)
    trans.to_csv(DERIVED / "ledger_translation.csv", index=False)
    tot = trans[trans.band_label == "all_bands"].iloc[0]
    old = trans[trans.band_label == "65plus"].iloc[0]
    _ok(f"all bands: {tot.delta_total_bn:+.2f}bn (SE {tot.se_delta_total_bn:.2f}); "
        f"65+ bands: {old.delta_total_bn:+.2f}bn (SE {old.se_delta_total_bn:.2f})")
    _ok(f"all bands, leave-one-out medical only: {tot.delta_medical_bn_drop_top1:+.2f}bn "
        f"against {tot.delta_medical_bn:+.2f}bn as measured")
    audit["translation_assumption"] = (
        "Each ledger band's medical and M charge is multiplied by that band's MEPS "
        "mexican_origin / all_donors ratio, the nativity cells combined with the union's own "
        "per-band foreign-born share. This is a translation under the assumption that the "
        "union's members in a band resemble MEPS Mexican-origin donors in that band. It is not "
        "a re-estimate of the ledger.")

    _header("pooled 2023+2024 check")
    audit["pooled_2023_2024_65plus"] = pooled_2023_check(audit)
    p = audit["pooled_2023_2024_65plus"]["pooled_65plus_public_ratio_vs_all_donors"]
    _ok(f"pooled 65+ ratio vs all donors: {p['ratio']:.3f} (SE {p['se']:.3f}, "
        f"n_mexican {p['n_mexican']}); primary remains 2024, the transport's year")
    audit["pooled_note"] = ("Secondary. 2023 dollars deflated to 2024 by the CPI-U annual-average "
                            "ratio from the acquired FRED file; both years' weights halved; 2023 "
                            "strata offset by 10000 so the two samples never share a stratum.")

    (DERIVED / "audit.json").write_text(json.dumps(audit, indent=2, default=float) + "\n")
    _ok("audit.json written")
    print("\n[done]")


if __name__ == "__main__":
    main()
