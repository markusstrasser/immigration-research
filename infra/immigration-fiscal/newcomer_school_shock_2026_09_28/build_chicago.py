#!/usr/bin/env python3
"""Chicago (CPS; ISBE district RCDTS 15-016-2990-25) school x year panel, spring 2017-2025.

Run from the repository root. python-calamine reads the .xlsx files and the legacy .xls CPS files:

    OPENBLAS_NUM_THREADS=1 uv run --no-project --with python-calamine==0.8.2 \
        python3 infra/immigration-fiscal/newcomer_school_shock_2026_09_28/build_chicago.py

The script reads only files under `_cache/chicago/` and checks each one against the sha256 in
INPUTS before parsing anything. A missing file or a hash mismatch stops the build. Outputs are
written deterministically: sorted rows, Decimal formatting and LF line endings.

    derived/chicago_schools.csv    ISBE school x spring year 2017-2025, plus CPS-only rows
    derived/chicago_scores.csv     grade 3-8 ELA/math results in long format
    derived/chicago_crosswalk.csv  CPS School ID -> ISBE RCDTS by year, with match status
    derived/chicago_staff_quarterly.csv  CPS position rosters summed by school x quarterly snapshot
    derived/chicago_audit.json     input hashes, row counts, suppression counts, checks

Definitions, verbatim source quotes and caveats are in `reads/chicago_sources.md`. Nothing is
imputed. A blank cell was not published, or was suppressed: `suppressed_fields` in the schools
file and `suppressed` in the scores file record suppression. Two quantities are computed rather
than copied:
  - the non-EL group in 2018, 2019 and 2021-2023: ISBE all-student counts minus ISBE EL counts,
    with `group = non_el_derived`; each row names its method;
  - the staffing sums: CPS roster rows (one per position line) summed by school department and
    snapshot date, then attached to CPS School IDs through the school-profile Finance_ID.
"""
from __future__ import annotations

import csv
import hashlib
import importlib.metadata
import io
import json
import re
import sys
import zipfile
from collections import Counter, defaultdict
from decimal import ROUND_HALF_EVEN, Decimal, InvalidOperation, getcontext
from pathlib import Path

import python_calamine

getcontext().prec = 34

LANE = Path(__file__).resolve().parent
CACHE = LANE / "_cache" / "chicago"
OUT = LANE / "derived"
CITY = "Chicago"
CPS_PREFIX = "15016299025"  # ISBE region-county-district-type for City of Chicago SD 299
YEARS = list(range(2017, 2026))  # spring year: 2017 = SY2016-17
RCDTS_RE = re.compile(r"^\d{11}[0-9A-Z]{4}$")

INPUTS = {
    "cps/IARProficiency_SY2025_Present.xlsx": "08c07253f49ef766f3c2a72f9eb6f7294d54a1cd2bd26f47a119d0fed51ceca1",
    "cps/demographics_20thday_2017.xls": "50181007abfaff44e01ae62bf428b224ebbd868f631481ce195a5be470a17f61",
    "cps/demographics_20thday_2018.xls": "16dca1ee8e02f7deacb41626824de9e8771deee73da4d74048171ca22578115a",
    "cps/demographics_20thday_2019.xls": "97d3f8e82b129d6a3b9efbf50b2a990caed4488ce518b67517398f478d36cbe7",
    "cps/demographics_20thday_2020.xls": "819d936700e8a715ecf657d679fd1454e609e294fdc3fd39acdca7340fe95a0d",
    "cps/demographics_20thday_2021_v10072020.xls": "dffbf2f119ca6a0e994d214e385c592c19e1f6d086ee9298e69107dc35c251b4",
    "cps/demographics_20thday_2022_v10272021.xls": "b8fb0656fce2f77dafb3c1d62a8885d640bf75d547ba548120c7901165b309f3",
    "cps/demographics_20thday_2023.xlsx": "3b947ec63ef7eda2db8210f77cbf88b7670f5d28be46f39063efd6068dce7f5f",
    "cps/demographics_20thday_sy2024_finalv2.xlsx": "5bdbc38edaf2e6c1570fa8dea072336accb4447adde09c00f7382fe0692ff487",
    "cps/demographics_20thday_sy2025_final.xlsx": "32da3946bc2d850f4b53dd1fbcb0fab10c19dc5c44de2d82f5a69c729905ee44",
    "cps/demographics_lepiepfrm_20thday_sy2024_finalv2.xlsx": "ac07bdae4c533fe2da65b4ba23a5f2ec389d152bfe40e921b5e156ce05009b97",
    "cps/demographics_lepiepfrm_20thday_sy2025_final.xlsx": "8bd115ea4926d8c1e54d5954e945ba9fd533ab9d359740d1279b6975f9a98fb8",
    "cps/demographics_lepsped_2017_10202020.xls": "71633a0c83a8b19439149fb525035de4b32932146b959c9c7675d38cd2e9b731",
    "cps/demographics_lepsped_2018_10202020.xls": "57ff89643e5ec0c449f65993073e484882965e61b0a18d47394838c9029bf69d",
    "cps/demographics_lepsped_2019_10202020.xls": "aba97d30f7bf98de15763eb1ffe836e657f6a6a59ed7f09c1bac303998628804",
    "cps/demographics_lepsped_2020_10202020.xls": "a2b021b670b633c783046b54b2696e7d764067f519cc66a63a7b76c1e337c7bd",
    "cps/demographics_lepsped_2021_v10072020.xls": "1203bc30449ef6e5cc0ca400a22af0f8de2edcc368c47a21569d2de57161c9bd",
    "cps/demographics_lepsped_2022_v10272021.xls": "1fed1b93e0dd3ff52c9625a4dbb1da1c0dcd7d5c246ad2cfa8cb47f9fa818072",
    "cps/demographics_lepsped_20thday_2023.xlsx": "5c868580ff1de19da1e31337dd8f2353f4c1bf81c2fbd8f87dda50f997ff2200",
    "cps/iar-parcc_2015to2024_schoollevel.xlsx": "e4de9581e60a77f2e90395854e3cea309c9cc047554a3fac165b04d27609522d",
    "cps_budget/fy2025_budgetoverview_district_management-schools.xlsx": "699763c4390b82263f2636cd462d6dfbd895c24b30d665daf4845fb892f5448d",
    "isbe/2018-PARCC-SAT-Proficient.xlsx": "2f2801889cbabb6c2e5c2c255d927bceaa480b43f3a82703985d5465577b615e",
    "isbe/2019-Report-Card-Public-Data-Set.xlsx": "071913dbc531560f24abadc80670d0a4728a33a225f9f959c9515b11429ae436",
    "isbe/2020-Report-Card-Public-Data-Set.xlsx": "14a38185fa41565acd2a52662cbd87d485cbb7396d37f7f8e16bd79b8d79a99b",
    "isbe/2021-RC-Pub-Data-Set.xlsx": "b0a1a4fcfa51514e7f5e15562d395367b1c36d27dd4abe2ae9b16119e4fd8864",
    "isbe/2022-Report-Card-Public-Data-Set.xlsx": "6575e1b5bfbb8a133c763d4b93273cc75749b9bfc8289420b2ef226318e08a1d",
    "isbe/2025-Report-Card-Public-Data-Set.xlsx": "459ac146b52bafe7ce79fd76a95a65daa68d0472cce5205fa777cde19fb58cdf",
    "isbe/23-RC-Pub-Data-Set.xlsx": "951536d6f81cdfdebb75e41775d0d80cde37bdd81fe256a6f31e2e571b7088ba",
    "isbe/24-RC-Pub-Data-Set.xlsx": "bab4981cd42a5355cfa8a62515b8364b981ff5e2397f4521deb0061034befa29",
    "isbe/RC17_layout.xlsx": "1f13f3a0940aedb2121fc539ca82cb9648eb01323c34d279d3401a72b9e82a02",
    "isbe/Report-Card-Public-Data-Set.xlsx": "35b96aa88033591d01eb220f363ebfec4582401abb6a6684d385a2528e2243ac",
    "isbe/rc17.zip": "637d707b53d4d2a57bd6a2af15d0da1259417c70fc3dad7739c4ea9cf6186d8e",
    "isbe/rc17_assessment.zip": "37f495b3a89721af9ee851f2bc87b3a13b0ad676f6a7595d6a5f7596827082bf",
    "portal/progress_SY1617_cp7s-7gxg.csv": "fa1ec56389d837fafc558f843c64d75f7ec5f7d3bfa8e71408cd9bdbbdf25edc",
    "portal/progress_SY1718_wkiz-8iya.csv": "d1cee91c0362ccb9aace131f51b862e938baee8d4a823e67545759fb5eb81425",
    "portal/progress_SY1819_dw27-rash.csv": "6100523805793470029036097a1ec9d0ffac263925b04deff62f323b7fb7435b",
    "portal/progress_SY2122_ngix-dc87.csv": "00f1247ba5c43b558e25baba304062b4d24d832001fdeae9196ae8c4a6700068",
    "portal/progress_SY2223_d7as-muwj.csv": "7bf4e7086269f9d74e36bb1ae360ee1298549a5853ea155c68cd5632d91cd4e2",
    "portal/progress_SY2324_2dn2-x66j.csv": "c511d8d4a896c76654684fb6ad4f51550c56ef22e708906d94b6933b796e2276",
    "portal/progress_SY2425_twrw-chuq.csv": "ce4079c2dbbb60d0aa0e269f59c03cd0e4b8ecfe021762c7b9f4e01d9bcae270",
    "portal/profile_SY1617_8i6r-et8s.csv": "e7f935ae3a0f8b98524344eb94ec1bf52a6273188d13152bb2249c9f29cb1e61",
    "portal/profile_SY1718_w4qj-h7bg.csv": "a35acde10ffe4aff2b8690d03c1f69d7718fd6270d99a0fc36548199cb6209c2",
    "portal/profile_SY1819_kh4r-387c.csv": "ad49e9675308bb80228504e2f8ca8737824db9f33f7e5eefa16fe54a238e8e6d",
    "portal/profile_SY2021_83yd-jxxw.csv": "2d839dc07c7cb0907a8f976a7909407be21ff8f25ef9e46c9b82e6f84265554c",
    "portal/profile_SY2122_2dem-8rq7.csv": "4eba01b3dcab2bbddf0bf5142bb8081af89417d47471ea4f6ae2d9a3396f6faf",
    "portal/profile_SY2223_9a5f-2r4p.csv": "02b46c306328150eed0c7c1210ab1198aec67e0adb4d0174ce94def9d0968b44",
    "portal/profile_SY2324_cu4u-b4d9.csv": "3e4bb31144d359fe32a4342e28a1c65ef50f55e586e8bf1da054668ae2697c1c",
    "portal/profile_SY2425_3dhs-m3w4.csv": "632e742e2ea8b21f6fe3cdd0a8f4a3b28b8488b688078ca015f9154acf9d7f91",
    "cps_positions/employeepositionroster_09302016.xls": "f202cd333bf5c9b8aafc56919060f7ad63634c9a1c4489268e65ed4225707b77",
    "cps_positions/employeepositionroster_12312016.xls": "a61d70e16e2679f0a6eb38a7f20751cdbb21bcd2e14e1811c0553204f0734545",
    "cps_positions/employeepositionroster_03312017.xls": "f5b65be97369149c0bb8a95669b1aab2423a3030d0d05992cdf2f6005a384101",
    "cps_positions/employeepositionroster_06302017.xls": "ad0a6487b32a9b907db29b454a613a40a411b5e2775675e96f7bc727789d06f3",
    "cps_positions/employeepositionroster_09302017.xls": "7e71d3fa54e7611e52a89d37d1fa82075d4d8bb0ea8318658be30005c391ba96",
    "cps_positions/employeepositionroster_12312017.xls": "da3f9a661fb4041fc68b6cb2bf1a454497af126b720c3541d1c2bda254ee7a7e",
    "cps_positions/employeepositionroster_03312018.xls": "991b5875e244d476a3cdc9b96c54612952ba389d77820b8ff0f5292598333521",
    "cps_positions/employeepositionroster_06302018.xls": "fd9424e6eea67a684114dce8637aba5a13f043b81c869fca6d18b075f46f52f7",
    "cps_positions/employeepositionroster_09302018.xls": "8addc9f9172fb51706fca04c89124df145e661fe48ba1f331c8ea0a59cdc7225",
    "cps_positions/employeepositionroster_12312018.xls": "d3ac7858c0d0026d92c39cb7002688663a390f8d9d726a80e9c37c7b82ddf804",
    "cps_positions/employeepositionroster_03312019.xls": "9475c517e98913408b020717d1729a5ce9c2fa816fe6797caf94c60424bc1a10",
    "cps_positions/employeepositionroster_06302019.xls": "db146f785e43294ce41469a60390c903e85a3d8282d09e837aa249caed2f10f5",
    "cps_positions/employeepositionroster_09302019.xls": "941eab19b079122171d0a696ed053278fbd564da24f3d753e18ac45f7e74a834",
    "cps_positions/employeepositionroster_12312019.xls": "b00cc154999ef750bb79e40800db30e9b209e90fe4f12851539c4de415e3b9c4",
    "cps_positions/employeepositionroster_03312020.xls": "58c2555c82ccb5f82518f6234ac67004a3fbebbe9f4c0ef9649f5599438fafcd",
    "cps_positions/employeepositionroster_06302020.xls": "947e0514057aa28efe05d68c3c4f1e49eac626bcbb00276d6a9eb59279a99913",
    "cps_positions/employeepositionroster_09302020.xls": "bba6f9454c8b24d41b417e2f18bcc82a1a37bd16f9a12eebae496f5d9ee0c2ec",
    "cps_positions/employeepositionroster_12312020.xls": "e9447c5caeb1ee81245226ae21295c7b4ccc7267098ddf721a54777f693d6fc8",
    "cps_positions/employeepositionroster_03312021.xls": "082fe38b2602caeaccdc57652835427608dd59960b7ca3e8b1f14ea84cbe79af",
    "cps_positions/employeepositionroster-06302021.xls": "b8a44f77161aa92c71bd3db8ca94fbd32e4dade80903057be42e1a084d3c3cbc",
    "cps_positions/employeepositionroster-09302021.xls": "baea346eb0a7ab6d9869e056ba511ed854f92de5f3a8b9c208b116aa6dcb69da",
    "cps_positions/employeepositionroster-12312021.xls": "cbc41a3406050449f1a9ec01b5fb5d2cafdb05d7361d97ce77ec496506d2df20",
    "cps_positions/employeepositionroster-03312022.xls": "31877b2ab5066098450d5eda134a09973f07ab0d9f83b723c07d90b0db36baba",
    "cps_positions/employeepositionroster-06302022.xls": "3998411d01ee4b6479dd88521bb57f773f3cd9d1e7da05b60a107addd69798a3",
    "cps_positions/employeepositionroster_09302022.xls": "0e97afa65ad6f00550e0597366b3818d31ffb947a9c7c861a2e56a1c4c80df4d",
    "cps_positions/employeepositionroster-12312022.xls": "8da4fa4757ad6305a5d6f7d20e9bbc91761ecaf8e2571dada23e3464cb5dc6b9",
    "cps_positions/employeepositionroster_03312023.xls": "5fe536390c4682bd5895a785dcfdda94a93cb8335b14bf4063a7d7c7e47b6c59",
    "cps_positions/employeepositionroster_06302023.xls": "6bb3cf77d4a6a897c59b4f3a4fed780875152f6d52b2a968201c97491a5ec6a7",
    "cps_positions/employeepositionroster-09302023.xls": "cefaf7861936ac50421b7d28c8d180a00a5846b6c769d1a832ad6679aafa8504",
    "cps_positions/employeepositionroster_12312023-3.xls": "9a37b55c76dceebe7e095f2877364c96382327b59193476fd9fea1554aed8c6f",
    "cps_positions/employeepositionroster_03312024.xls": "ebb5f7af990c07eb93e6254720d5d6d4704a850f1504a3c06842346ec2d3af47",
    "cps_positions/employeepositionroster_06302024.xls": "ac3ffa67fadbe708c6187635649a59b927f12c74ed243f3c989ee24d1bdf696a",
    "cps_positions/employeepositionroster_09302024.xls": "36c4515c418e533323d5239fb14e5012ba16c88619077aea4ec0a7b38ac53aca",
    "cps_positions/employeepositionroster_12312024.xls": "40b1d4bef5ff07b7e51c3f6f8d81cb34156aae09bbb35583670d3d6c2c94a0c3",
    "cps_positions/employeepositionroster_03312025.xls": "cec6874c03d6d5a1c4eba82eeed901cb94f9a7359af3db37d00c2ce580d8292c",
    "cps_positions/employeepositionroster_06302025.xls": "35b20ca983aed3784df7d7b9c5313748795ed1a8247e09d59912a939e90e4aaf",
}

ISBE_FILES = {
    2018: "isbe/Report-Card-Public-Data-Set.xlsx",
    2019: "isbe/2019-Report-Card-Public-Data-Set.xlsx",
    2020: "isbe/2020-Report-Card-Public-Data-Set.xlsx",
    2021: "isbe/2021-RC-Pub-Data-Set.xlsx",
    2022: "isbe/2022-Report-Card-Public-Data-Set.xlsx",
    2023: "isbe/23-RC-Pub-Data-Set.xlsx",
    2024: "isbe/24-RC-Pub-Data-Set.xlsx",
    2025: "isbe/2025-Report-Card-Public-Data-Set.xlsx",
}
CPS_LEP = {
    2017: "cps/demographics_lepsped_2017_10202020.xls",
    2018: "cps/demographics_lepsped_2018_10202020.xls",
    2019: "cps/demographics_lepsped_2019_10202020.xls",
    2020: "cps/demographics_lepsped_2020_10202020.xls",
    2021: "cps/demographics_lepsped_2021_v10072020.xls",
    2022: "cps/demographics_lepsped_2022_v10272021.xls",
    2023: "cps/demographics_lepsped_20thday_2023.xlsx",
    2024: "cps/demographics_lepiepfrm_20thday_sy2024_finalv2.xlsx",
    2025: "cps/demographics_lepiepfrm_20thday_sy2025_final.xlsx",
}
CPS_MEMBERSHIP = {
    2017: "cps/demographics_20thday_2017.xls",
    2018: "cps/demographics_20thday_2018.xls",
    2019: "cps/demographics_20thday_2019.xls",
    2020: "cps/demographics_20thday_2020.xls",
    2021: "cps/demographics_20thday_2021_v10072020.xls",
    2022: "cps/demographics_20thday_2022_v10272021.xls",
    2023: "cps/demographics_20thday_2023.xlsx",
    2024: "cps/demographics_20thday_sy2024_finalv2.xlsx",
    2025: "cps/demographics_20thday_sy2025_final.xlsx",
}
PROGRESS = {  # spring year of the school year each Chicago Data Portal progress-report file covers
    2017: "portal/progress_SY1617_cp7s-7gxg.csv",
    2018: "portal/progress_SY1718_wkiz-8iya.csv",
    2019: "portal/progress_SY1819_dw27-rash.csv",
    2022: "portal/progress_SY2122_ngix-dc87.csv",
    2023: "portal/progress_SY2223_d7as-muwj.csv",
    2024: "portal/progress_SY2324_2dn2-x66j.csv",
    2025: "portal/progress_SY2425_twrw-chuq.csv",
}
PROFILES = {  # Chicago Data Portal school-profile files: School_ID -> Finance_ID (roster Dept ID)
    2017: "portal/profile_SY1617_8i6r-et8s.csv",
    2018: "portal/profile_SY1718_w4qj-h7bg.csv",
    2019: "portal/profile_SY1819_kh4r-387c.csv",
    2021: "portal/profile_SY2021_83yd-jxxw.csv",
    2022: "portal/profile_SY2122_2dem-8rq7.csv",
    2023: "portal/profile_SY2223_9a5f-2r4p.csv",
    2024: "portal/profile_SY2324_cu4u-b4d9.csv",
    2025: "portal/profile_SY2425_3dhs-m3w4.csv",
}
BUDGET_FY2025 = "cps_budget/fy2025_budgetoverview_district_management-schools.xlsx"
CPS_IAR_1524 = "cps/iar-parcc_2015to2024_schoollevel.xlsx"
CPS_IAR_25 = "cps/IARProficiency_SY2025_Present.xlsx"

SCHOOL_COLS = [
    "city", "school_id", "cps_school_id", "school_name", "year", "row_source",
    "school_type", "grades_served",
    "enroll_total", "el_n", "el_pct", "former_el_n", "never_el_n", "newcomer_n", "stls_n",
    "homeless_pct", "low_income_pct",
    "ppe_total", "ppe_federal", "ppe_state_local",
    "ppe_site_total", "ppe_site_federal", "ppe_site_state_local", "ppe_central_total", "ppe_enroll",
    "teacher_fte", "teacher_headcount", "pupil_teacher_ratio", "pupil_teacher_ratio_hs",
    "class_size_avg", "class_size_g3", "class_size_g4", "class_size_g5", "class_size_g6",
    "class_size_g7", "class_size_g8",
    "cps20_enroll_total", "cps20_el_n", "cps20_el_label", "cps_network", "cps_governance",
    "cps_budget_enroll_20th", "cps_budget_noncluster_enroll", "cps_budget_newcomer_adj",
    "cps_budget_teacher_enroll_input", "cps_budget_core_teacher_ratio",
    "cps_budget_core_classroom_teachers", "cps_budget_bilingual_coordinators",
    "cps_budget_stls_advocates",
    "cps_teacher_fte_sep30", "cps_teacher_fte_mar31", "cps_teacher_fte_filled_sep30",
    "cps_teacher_fte_filled_mar31", "cps_all_fte_sep30", "cps_all_fte_mar31",
    "xwalk_status", "xwalk_source", "xwalk_shared", "suppressed_fields",
]
STAFF_COLS = [
    "city", "school_id", "cps_school_id", "dept_id", "department", "snapshot_date", "school_year",
    "n_rows", "n_rows_vacant", "n_rows_shared_pos", "fte_all", "fte_filled", "fte_teacher", "fte_teacher_filled",
    "fte_regular_teacher", "fte_bilingual_teacher", "fte_sped_teacher", "fte_salary_filled", "benefit_cost_filled",
    "dept_map_source",
]
SCORE_COLS = [
    "city", "school_id", "cps_school_id", "year", "subject", "group", "group_label", "grade",
    "source", "test_scope", "test_name", "n_tested", "n_denominator", "n_proficient",
    "pct_proficient", "pct_proficient_method", "pct_proficient_min", "pct_proficient_max",
    "mean_scale_score", "pct_level1", "pct_level2", "pct_level3", "pct_level4", "pct_level5",
    "n_levels", "participation_rate", "suppressed",
]
XWALK_COLS = ["year", "cps_school_id", "cps_name", "school_id", "status", "progress_year_used", "n_cps_ids_for_rcdts"]


# ----------------------------------------------------------------------------- basics

def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_inputs() -> None:
    problems = []
    for rel, want in sorted(INPUTS.items()):
        p = CACHE / rel
        if not p.is_file():
            problems.append(f"missing: {rel}")
            continue
        got = sha256(p)
        if got != want:
            problems.append(f"sha256 mismatch: {rel} expected {want} got {got}")
    if problems:
        raise SystemExit("[BLOCKED] input verification failed:\n  " + "\n  ".join(problems))


NUM_RE = re.compile(r"^[+-]?(?:\d{1,3}(?:,\d{3})+|\d+)?(?:\.\d+)?$")


def parse(v):
    """Classify a published cell as ('num', Decimal) | ('blank', None) | ('sup', None); raise otherwise."""
    if v is None:
        return "blank", None
    if isinstance(v, bool):
        raise TypeError(f"unexpected boolean cell {v!r}")
    if isinstance(v, int):
        return "num", Decimal(v)
    if isinstance(v, float):
        if v != v or v in (float("inf"), float("-inf")):
            raise ValueError(f"non-finite cell {v!r}")
        return "num", Decimal(repr(v))
    if isinstance(v, str):
        s = v.strip()
        if s == "":
            return "blank", None
        if s == "*":
            return "sup", None
        if NUM_RE.match(s) and any(ch.isdigit() for ch in s):
            return "num", Decimal(s.replace(",", ""))
        raise ValueError(f"unexpected cell token {v!r}")
    raise TypeError(f"unexpected cell type {type(v).__name__}: {v!r}")


def fmt(d, places: int = 6) -> str:
    if d is None:
        return ""
    if not isinstance(d, Decimal):
        d = Decimal(d)
    q = d.quantize(Decimal(1).scaleb(-places), rounding=ROUND_HALF_EVEN)
    s = format(q, "f")
    if "." in s:
        s = s.rstrip("0").rstrip(".")
    if s in ("-0", ""):
        s = "0"
    return s


def norm(h) -> str:
    s = str(h).replace("–", "-").replace("—", "-").replace("\xa0", " ").replace("​", "")
    s = re.sub(r"\s+", " ", s.replace("\n", " ")).strip().lower()
    return s


def cps_id(v) -> str:
    kind, d = parse(v)
    if kind != "num" or d != d.to_integral_value() or d <= 0:
        raise ValueError(f"bad CPS school id {v!r}")
    return str(int(d))


def is_note_row(r, id_i) -> bool:
    """A free-text note in the ID column with every other cell empty (e.g. 'NOTE: There were 449 ...')."""
    first = str(r[id_i]).strip()
    if not first:
        return False
    try:
        kind, _ = parse(r[id_i])
    except ValueError:
        kind = "text"
    if kind == "num":
        return False
    return all(not str(v).strip() for i, v in enumerate(r) if i != id_i)


class Tally:
    """Counts parsed cells by (source, year) and kind; the audit reports these."""

    def __init__(self):
        self.c = Counter()

    def get(self, v, key: str):
        kind, val = parse(v)
        self.c[(key, kind)] += 1
        return kind, val

    def report(self):
        out = defaultdict(dict)
        for (key, kind), n in sorted(self.c.items()):
            out[key][kind] = n
        return dict(out)


TALLY = Tally()
NOTES = []  # free-text note rows met in CPS sheets, reported verbatim in the audit


class Book:
    def __init__(self, rel: str):
        self.rel = rel
        self.wb = python_calamine.CalamineWorkbook.from_path(str(CACHE / rel))
        self.names = list(self.wb.sheet_names)
        self._cache = {}

    def rows(self, sheet: str):
        if sheet not in self.names:
            raise KeyError(f"{self.rel}: no sheet {sheet!r}; sheets are {self.names}")
        if sheet not in self._cache:
            self._cache[sheet] = self.wb.get_sheet_by_name(sheet).to_python()
        return self._cache[sheet]


def find_cols(header, name: str, label: str):
    n = norm(name)
    return [i for i, h in enumerate(header) if norm(h) == n]


def one_col(header, name: str, label: str, nth=None) -> int:
    idx = find_cols(header, name, label)
    if not idx:
        raise KeyError(f"{label}: header {name!r} not found")
    if nth is None:
        if len(idx) > 1:
            raise ValueError(f"{label}: header {name!r} is ambiguous at columns {idx}")
        return idx[0]
    if len(idx) <= nth:
        raise KeyError(f"{label}: header {name!r} has no occurrence #{nth}")
    return idx[nth]


class IsbeSheet:
    """One ISBE public-data-set sheet restricted to CPS school rows, keyed by 15-character RCDTS."""

    def __init__(self, book: Book, sheet: str):
        rows = book.rows(sheet)
        self.label = f"{book.rel}!{sheet}"
        self.header = [str(x) for x in rows[0]]
        id_i = one_col(self.header, "RCDTS", self.label)
        norm_h = [norm(h) for h in self.header]
        type_i = one_col(self.header, "Level", self.label) if "level" in norm_h else one_col(self.header, "Type", self.label)
        self.rows = {}
        for r in rows[1:]:
            rid = str(r[id_i]).replace("-", "").strip().upper()
            if not rid.startswith(CPS_PREFIX):
                continue
            t = str(r[type_i]).strip()
            if t == "District":
                continue
            if t != "School":
                raise ValueError(f"{self.label}: unexpected row type {t!r} for {rid}")
            if not RCDTS_RE.match(rid):
                raise ValueError(f"{self.label}: malformed RCDTS {rid!r}")
            if rid in self.rows:
                raise ValueError(f"{self.label}: duplicate RCDTS {rid}")
            self.rows[rid] = r

    def col(self, name: str, nth=None) -> int:
        return one_col(self.header, name, self.label, nth)

    def has(self, name: str) -> bool:
        return bool(find_cols(self.header, name, self.label))


def locate(sheets, name: str):
    """Find a header in exactly one of several sheets; return (sheet, column)."""
    hits = [(s, i) for s in sheets for i in find_cols(s.header, name, s.label)]
    if not hits:
        raise KeyError(f"header {name!r} not found in {[s.label for s in sheets]}")
    if len(hits) > 1:
        raise ValueError(f"header {name!r} ambiguous: {[(s.label, i) for s, i in hits]}")
    return hits[0]


# ----------------------------------------------------------------------------- ISBE 2017 (text)

def parse_layout(book: Book, sheet: str):
    fields, section = [], ""
    for r in book.rows(sheet):
        c0 = r[0]
        if isinstance(c0, float):
            if c0 != int(c0):
                raise ValueError(f"{sheet}: non-integer field number {c0}")
            fields.append({"num": int(c0), "test": str(r[1]).strip(), "group": str(r[2]).strip(),
                           "desc": norm(r[5]), "section": section})
        elif str(c0).strip():
            section = str(c0).strip()
    nums = [f["num"] for f in fields]
    if nums != list(range(1, len(nums) + 1)):
        raise ValueError(f"RC17 layout {sheet}: field numbers are not 1..n")
    return fields


def layout_find(fields, desc: str, *, group=None, test=None, section=None) -> int:
    d = norm(desc)
    hits = [f for f in fields if f["desc"] == d and (group is None or f["group"] == group)
            and (test is None or f["test"] == test) and (section is None or f["section"] == section)]
    if len(hits) != 1:
        raise ValueError(f"RC17 layout: {desc!r} group={group} test={test} section={section} -> {len(hits)} hits")
    return hits[0]["num"]


def read_rc17_lines(zip_rel: str, member: str, n_fields: int):
    """Yield CPS school rows (list of fields) from an rc17 semicolon file inside its zip."""
    out = {}
    with zipfile.ZipFile(CACHE / zip_rel) as z:
        with z.open(member) as f:
            for raw in f:
                if not raw.startswith(CPS_PREFIX.encode()):
                    continue
                line = raw.decode("utf-8").rstrip("\r\n")
                parts = line.split(";")
                if len(parts) == n_fields + 1 and parts[-1] == "":
                    parts = parts[:-1]
                if len(parts) != n_fields:
                    raise ValueError(f"{zip_rel}: {len(parts)} fields, layout has {n_fields}")
                rid = parts[0].strip().upper()
                if rid.endswith("0000"):
                    continue  # district row
                if not RCDTS_RE.match(rid):
                    raise ValueError(f"{zip_rel}: malformed RCDTS {rid!r}")
                if rid in out:
                    raise ValueError(f"{zip_rel}: duplicate {rid}")
                out[rid] = parts
    return out


# ----------------------------------------------------------------------------- ISBE schools fields

GENERAL_SPEC = {
    2018: dict(enroll="Student Enrollment - Total", el_pct="Student Enrollment - EL %",
               low="Student Enrollment - Low Income %", hl_pct="Student Enrollment - Homeless %",
               fte="Total Teacher FTE", head=None, cs_all="Avg Class Size - All Grades", cs="Avg Class Size - {g}"),
    2019: dict(enroll="# Student Enrollment", el_pct="% Student Enrollment - EL",
               low="% Student Enrollment - Low Income", hl_pct="% Student Enrollment - Homeless",
               fte="Total Teacher FTE", head=None, cs_all="Avg Class Size - All Grades", cs="Avg Class Size - {g}"),
}
for _y in (2020, 2021, 2022, 2023):
    GENERAL_SPEC[_y] = dict(GENERAL_SPEC[2019], head="Total Teacher Headcount")
for _y in (2024, 2025):
    GENERAL_SPEC[_y] = dict(GENERAL_SPEC[2019], head="Total Teacher Headcount", cs="Avg Class Size - Grade {g}",
                            el_n="# Student Enrollment - EL", hl_n="# Student Enrollment - Homeless")
GENERAL_SPEC[2025].update(former_n="# Student Enrollment - Former EL", never_n="# Student Enrollment - Never EL")

FINANCE_SHEET = {2019: "Financial", 2020: "Finance", 2021: "Finance", 2022: "Finance", 2023: "Finance",
                 2024: "Finance", 2025: "Finance"}
FINANCE_COLS = {
    "ppe_site_federal": "$ Site-Level Per-Pupil Expenditures - Federal",
    "ppe_site_state_local": "$ Site-level Per-Pupil Expenditures - State/Local",
    "ppe_site_total": "$ Site-level Per-Pupil Expenditures - Subtotal",
    "ppe_central_total": "$ District Centralized Per-Pupil Expenditure - Subtotal",
    "ppe_federal": "$ Total Per-Pupil Expenditures - Federal",
    "ppe_state_local": "$ Total Per-Pupil Expenditures - State/Local",
    "ppe_total": "$ Total Per-Pupil Expenditures - Subtotal",
    "ppe_enroll": "# School Enrollment",
}


def isbe_general_2017(layout):
    f = {
        "school_name": layout_find(layout, "SCHOOL NAME"),
        "school_type": layout_find(layout, "SCHOOL TYPE NAME"),
        "grades_served": layout_find(layout, "GRADES IN SCHOOL"),
        "enroll_total": layout_find(layout, "SCHOOL TOTAL ENROLLMENT"),
        "el_pct": layout_find(layout, "L.E.P. SCHOOL %"),
        "low_income_pct": layout_find(layout, "LOW-INCOME SCHOOL %"),
        "homeless_pct": layout_find(layout, "HOMELESS SCHOOL %"),
        "class_size_avg": layout_find(layout, "OVERALL AVERAGE CLASS SIZE - SCHOOL"),
    }
    for g in range(3, 9):
        f[f"class_size_g{g}"] = layout_find(layout, f"AVG CLASS SIZE - SCHOOL (GR{g})")
    rows = read_rc17_lines("isbe/rc17.zip", "rc17.txt", len(layout))
    out = {}
    for rid, parts in rows.items():
        rec, sup = {}, []
        for k, num in f.items():
            v = parts[num - 1]
            if k in ("school_name", "school_type", "grades_served"):
                rec[k] = re.sub(r"\s+", " ", v).strip()
                continue
            kind, val = TALLY.get(v, "isbe_general:2017")
            rec[k] = val
            if kind == "sup":
                sup.append(k)
        rec["_sup"] = sup
        out[rid] = rec
    return out


def isbe_general(year: int, book: Book):
    spec = GENERAL_SPEC[year]
    g = IsbeSheet(book, "General")
    cols = {
        "enroll_total": spec["enroll"], "el_pct": spec["el_pct"], "low_income_pct": spec["low"],
        "homeless_pct": spec["hl_pct"], "teacher_fte": spec["fte"],
        "pupil_teacher_ratio": "Pupil Teacher Ratio - Elementary",
        "pupil_teacher_ratio_hs": "Pupil Teacher Ratio - High School",
        "class_size_avg": spec["cs_all"],
    }
    if spec.get("head"):
        cols["teacher_headcount"] = spec["head"]
    if spec.get("el_n"):
        cols["el_n"] = spec["el_n"]
        cols["stls_n"] = spec["hl_n"]
    if spec.get("former_n"):
        cols["former_el_n"] = spec["former_n"]
        cols["never_el_n"] = spec["never_n"]
    for gr in range(3, 9):
        cols[f"class_size_g{gr}"] = spec["cs"].format(g=gr)
    idx = {k: g.col(v) for k, v in cols.items()}
    name_i, type_i, gs_i = g.col("School Name"), g.col("School Type"), g.col("Grades Served")
    out = {}
    for rid, r in g.rows.items():
        rec, sup = {"school_name": str(r[name_i]).strip(), "school_type": str(r[type_i]).strip(),
                    "grades_served": re.sub(r"\s+", " ", str(r[gs_i])).strip()}, []
        for k, i in idx.items():
            kind, val = TALLY.get(r[i], f"isbe_general:{year}")
            rec[k] = val
            if kind == "sup":
                sup.append(k)
        rec["_sup"] = sup
        out[rid] = rec
    if year in FINANCE_SHEET:
        fs = IsbeSheet(book, FINANCE_SHEET[year])
        fidx = {k: fs.col(v) for k, v in FINANCE_COLS.items()}
        for rid, r in fs.rows.items():
            if rid not in out:
                raise ValueError(f"{fs.label}: {rid} not in General")
            for k, i in fidx.items():
                kind, val = TALLY.get(r[i], f"isbe_finance:{year}")
                out[rid][k] = val
                if kind == "sup":
                    out[rid]["_sup"].append(k)
    return out


# ----------------------------------------------------------------------------- scores helpers

SUBJ_LABEL = {"ela": "ELA", "math": "Mathematics"}


def score_row(**kw):
    row = {c: "" for c in SCORE_COLS}
    row["city"] = CITY
    for k, v in kw.items():
        if k not in row:
            raise KeyError(f"unknown score column {k}")
        row[k] = v
    return row


def cells(values, key):
    """Parse a dict name->raw cell; return (dict name->Decimal|None, any_suppressed, any_value)."""
    out, sup, anyv = {}, False, False
    for k, v in values.items():
        kind, val = TALLY.get(v, key)
        out[k] = val
        sup = sup or kind == "sup"
        anyv = anyv or kind != "blank"
    return out, sup, anyv


def levels_sum45(vals):
    if vals.get("pct_level4") is None or vals.get("pct_level5") is None:
        return None
    return vals["pct_level4"] + vals["pct_level5"]


# ----------------------------------------------------------------------------- ISBE scores

LEVEL_SPEC = {
    2018: (["PARCC"], "{grp} students PARCC {subj} Level {L} - Grade {G}", "parcc"),
    2019: (["IAR"], "{grp} students IAR {subj} Level {L} - Grade {G}", "iar"),
    2021: (["IAR"], "% {grp} students IAR {subj} Level {L} - Grade {G}", "iar"),
    2022: (["IAR", "IAR (2)"], "% {grp} students IAR {subj} Level {L} - Grade {G}", "iar"),
    2023: (["IAR", "IAR (2)"], "% {grp} students IAR {subj} Level {L} - Grade {G}", "iar"),
    2024: (["IAR", "IAR (2)"], "% {grp} students IAR {subj} Level {L} - Grade {G}", "iar"),
}
LEVEL_GROUP = {"all": "All", "el": "EL"}

# School-level all-tests counts/rates: (subject, group) -> column names.
ALLTESTS_2018 = {
    ("ela", "all"): dict(n_proficient="ELA Proficiency Total Count", pct="ELA Proficiency Total %",
                         n_tested="ELA Participation Total Student Count", part="ELA Participation Total Student %"),
    ("ela", "el"): dict(n_proficient="ELA Proficiency EL Count", pct="ELA Proficiency EL %",
                        n_tested="ELA Participation Total EL Count", part="ELA Participation Total EL %"),
    ("math", "all"): dict(n_proficient="Math Proficiency Total Count", pct="Math Proficiency Total %",
                          n_tested="Math Participation Total Student Count", part="Math Participation Total Student %"),
    # The EL math participation columns are mislabeled "IEP" (second of two identical headers);
    # verified arithmetically in check_2018_math_el() before use.
    ("math", "el"): dict(n_proficient="Math Proficiency EL Count", pct="Math Proficiency EL %",
                         n_tested=("Math Participation Total IEP Count", 1), part=("Math Participation IEP %", 1)),
}
ALLTESTS_1923 = {
    ("ela", "all"): dict(n_proficient="# ELA Proficiency", pct="% ELA Proficiency",
                         n_tested="# ELA Student Participation", part="% ELA Student Participation"),
    ("ela", "el"): dict(n_proficient="# ELA Proficiency - EL", pct="% ELA Proficiency - EL",
                        n_tested="# ELA Participation - EL", part="% ELA Participation - EL"),
    ("math", "all"): dict(n_proficient="# Math Proficiency", pct="% Math Proficiency",
                          n_tested="# Math Participation Total Student", part="% Math Student Participation"),
    ("math", "el"): dict(n_proficient="# Math Proficiency - EL", pct="% Math Proficiency - EL",
                         n_tested="# Math Participation - EL", part="% Math Participation - EL"),
}
ALLTESTS_2024 = {
    ("ela", "all"): dict(pct="% ELA Proficiency", part="% ELA Student Participation"),
    ("ela", "el"): dict(pct="% ELA Proficiency - EL", part="% ELA Participation - EL"),
    ("math", "all"): dict(pct="% Math Proficiency", part="% Math Student Participation"),
    ("math", "el"): dict(pct="% Math Proficiency - EL", part="% Math Participation - EL"),
}
ALLTESTS_2025 = {
    ("ela", "all"): dict(pct="% ELA Proficiency", part="% ELA Participation"),
    ("ela", "el"): dict(pct="% ELA Proficiency - EL", part="% ELA Participation - EL"),
    ("math", "all"): dict(pct="% Math Proficiency", part="% Math Participation"),
    ("math", "el"): dict(pct="% Math Proficiency - EL", part="% Math Participation - EL"),
}
ALLTESTS_2025_38 = {
    ("ela", "all"): dict(pct="% ELA Proficiency Grade 3 to 8"),
    ("ela", "el"): dict(pct="% ELA Proficiency Grade 3 to 8 - EL"),
    ("math", "all"): dict(pct="% Math Proficiency Grade 3 to 8"),
    ("math", "el"): dict(pct="% Math Proficiency Grade 3 to 8 - EL"),
}
# IAR/PARCC-only school-level grade 3-8 measures.
IAR38 = {
    2018: {("ela", "all"): dict(n_tested="Total Students PARCC ELA Participation", part="Total Students PARCC ELA Participation %"),
           ("ela", "el"): dict(n_tested="EL Students PARCC ELA Participation", part="EL Students PARCC ELA Participation %"),
           ("math", "all"): dict(n_tested="Total Students PARCC Math Participation", part="Total Students PARCC Math Participation %"),
           ("math", "el"): dict(n_tested="EL Students PARCC Math Participation", part="EL Students PARCC Math Participation %")},
}
for _y in (2019, 2021, 2022, 2023):
    IAR38[_y] = {("ela", "all"): dict(n_tested="# Students IAR ELA Participation", part="% Students IAR ELA Participation"),
                 ("ela", "el"): dict(n_tested="# EL Students IAR ELA Participation", part="% EL Students IAR ELA Participation"),
                 ("math", "all"): dict(n_tested="# Students IAR Math Participation", part="% Students IAR Math Participation"),
                 ("math", "el"): dict(n_tested="# EL Students IAR Math Participation", part="% EL Students IAR Math Participation")}
IAR38[2024] = {("ela", "all"): dict(pct="IAR ELA Proficiency Rate - Total", part="% Students IAR ELA Participation"),
               ("ela", "el"): dict(pct="IAR ELA Proficiency Rate - EL", part="% EL Students IAR ELA Participation"),
               ("math", "all"): dict(pct="IAR Math Proficiency Rate - Total", part="% Students IAR Math Participation"),
               ("math", "el"): dict(pct="IAR Math Proficiency Rate - EL", part="% EL Students IAR Math Participation")}
IAR38[2025] = {("ela", "all"): dict(pct="IAR ELA Proficiency Rate - Total", part="IAR ELA Participation Rate - Total"),
               ("ela", "el"): dict(pct="IAR ELA Proficiency Rate - EL", part="IAR ELA Participation Rate - EL"),
               ("math", "all"): dict(pct="IAR Math Proficiency Rate - Total", part="IAR Math Participation Rate - Total"),
               ("math", "el"): dict(pct="IAR Math Proficiency Rate - EL", part="IAR Math Participation Rate - EL")}
IAR38_SHEETS = {2018: ["PARCC"], 2019: ["IAR"], 2021: ["IAR"], 2022: ["IAR", "IAR (2)"], 2023: ["IAR", "IAR (2)"],
                2024: ["IAR", "IAR (2)"], 2025: ["IAR"]}
GROUP_LABEL = {"all": "All", "el": "EL"}


def colref(sheets, spec):
    """spec is a header string or (header, nth) for a deliberately positional duplicate."""
    if isinstance(spec, tuple):
        name, nth = spec
        if len(sheets) != 1:
            raise ValueError("positional duplicate lookups need exactly one sheet")
        return sheets[0], sheets[0].col(name, nth)
    return locate(sheets, spec)


def emit_school_measures(year, sheets, spec_by_key, *, source, test_scope, grade, scores, raw_store=None):
    refs = {key: {fld: colref(sheets, name) for fld, name in fields.items()} for key, fields in spec_by_key.items()}
    rids = sorted(set().union(*[s.rows.keys() for s in sheets]))
    for rid in rids:
        for (subj, grp), fr in refs.items():
            raw = {}
            for fld, (sh, ci) in fr.items():
                r = sh.rows.get(rid)
                raw[fld] = r[ci] if r is not None else ""
            vals, sup, anyv = cells(raw, f"{source}:{year}")
            if raw_store is not None:
                raw_store[(rid, subj, grp)] = {fld: parse(v) for fld, v in raw.items()}
            if not anyv:
                continue
            method = "published" if vals.get("pct") is not None else ""
            scores.append(score_row(
                school_id=rid, year=str(year), subject=subj, group=grp, group_label=GROUP_LABEL[grp], grade=grade,
                source=source, test_scope=test_scope, n_tested=fmt(vals.get("n_tested")),
                n_proficient=fmt(vals.get("n_proficient")), pct_proficient=fmt(vals.get("pct")),
                pct_proficient_method=method, participation_rate=fmt(vals.get("part")), suppressed="1" if sup else "0"))


def derive_non_el(year, raw_store, scores, checks):
    """ISBE all-student minus EL counts (school level, all tests). Exact when EL counts are published;
    bounds when ISBE leaves the EL cells blank (EL tested 0-9, verified below)."""
    n_exact = n_bounds = n_skip = 0
    for (rid, subj, grp), a in sorted(raw_store.items()):
        if grp != "all":
            continue
        e = raw_store.get((rid, subj, "el"))
        ka, A = a["n_tested"]
        kp, P = a["n_proficient"]
        if ka != "num" or kp != "num" or A <= 0:
            continue
        for x in (A, P):
            if x != x.to_integral_value():
                raise ValueError(f"non-integer count {x} {rid} {year}")
        ke, E = e["n_tested"] if e else ("blank", None)
        kq, Q = e["n_proficient"] if e else ("blank", None)
        if ke == "num" and kq == "num":
            nA, nP = A - E, P - Q
            if nA <= 0 or nP < 0 or nP > nA:
                n_skip += 1
                continue
            scores.append(score_row(
                school_id=rid, year=str(year), subject=subj, group="non_el_derived",
                group_label="All minus EL (derived from ISBE counts)", grade="school",
                source="derived_all_minus_el", test_scope="all_tests", n_tested=fmt(nA), n_proficient=fmt(nP),
                pct_proficient=fmt(nP * 100 / nA, 4), pct_proficient_method="all_minus_el",
                suppressed="0"))
            n_exact += 1
        elif ke == "blank" and kq == "blank":
            lo = hi = None
            for ee in range(0, 10):
                if A - ee <= 0:
                    break
                for qq in range(0, ee + 1):
                    np_, na_ = P - qq, A - ee
                    if np_ < 0 or np_ > na_:
                        continue
                    v = np_ * 100 / na_
                    lo = v if lo is None or v < lo else lo
                    hi = v if hi is None or v > hi else hi
            if lo is None:
                n_skip += 1
                continue
            scores.append(score_row(
                school_id=rid, year=str(year), subject=subj, group="non_el_derived",
                group_label="All minus EL (derived; EL tested 0-9, not published)", grade="school",
                source="derived_all_minus_el", test_scope="all_tests",
                pct_proficient_method="bounds_el_0_9", pct_proficient_min=fmt(lo, 4),
                pct_proficient_max=fmt(hi, 4), suppressed="1"))
            n_bounds += 1
        else:
            n_skip += 1
    checks[f"non_el_derived_{year}"] = {"exact_rows": n_exact, "bounds_rows": n_bounds, "skipped": n_skip}


def check_min_el_participation(year, raw_store, checks):
    vals = sorted(v[1] for (rid, s, g), d in raw_store.items() if g == "el" for k, v in [("n", d["n_tested"])] if v[0] == "num")
    if vals and vals[0] < 10:
        raise ValueError(f"{year}: EL participation count {vals[0]} < 10 is published; blank-means-0..9 bound invalid")
    checks[f"min_published_el_participation_{year}"] = fmt(vals[0]) if vals else ""


def check_2018_math_el(sheet: IsbeSheet, checks):
    """Confirm the second 'Math Participation Total IEP Count' column is EL math participation:
    Math EL % should equal EL proficient / that column (or be lower, under ISBE's 95% rule)."""
    c_prof, c_pct = sheet.col("Math Proficiency EL Count"), sheet.col("Math Proficiency EL %")
    c_first, c_second = sheet.col("Math Participation Total IEP Count", 0), sheet.col("Math Participation Total IEP Count", 1)
    ela_el, ela_iep = sheet.col("ELA Participation Total EL Count"), sheet.col("ELA Participation Total IEP Count")
    if not (c_second == c_first + 1 and ela_el == ela_iep + 1):
        raise ValueError("2018 ELA and Math: participation column order changed")
    exact = total = 0
    for r in sheet.rows.values():
        kq, q = parse(r[c_prof])
        kp, p = parse(r[c_pct])
        kn, n = parse(r[c_second])
        if kq == kp == kn == "num" and n > 0:
            total += 1
            if abs(q * 100 / n - p) <= Decimal("0.051"):
                exact += 1
    share = Decimal(exact) / Decimal(total) if total else Decimal(0)
    checks["isbe2018_math_el_participation_column"] = {
        "header": "Math Participation Total IEP Count (2nd occurrence)", "schools_checked": total,
        "share_pct_equals_count_over_column": fmt(share, 4)}
    if share < Decimal("0.8"):
        raise ValueError(f"2018 math EL participation column check failed: share {share}")


def isbe_scores_2017(layout, scores, checks):
    fields = {}
    names = {1: "DID NOT YET MEET", 2: "PARTIALLY MET", 3: "APPROACHED", 4: "MET", 5: "EXCEEDED"}
    for subj, s in (("ela", "ELA"), ("math", "MATH")):
        for grp, g in (("all", "ALL"), ("el", "LEP")):
            for gr in range(3, 9):
                fields[("lv", subj, grp, str(gr))] = [
                    layout_find(layout, f"GR{gr} {s} SCHOOL - STUDENTS {names[L]} EXPECTATIONS", group=g, test="PARCC")
                    for L in range(1, 6)]
            fields[("acct", subj, grp)] = layout_find(
                layout, f"PERCENTAGE OF PROFICIENCY IN {s} (ALL STUDENTS)", group=g, section="SCHOOL")
            fields[("taking", subj, grp)] = layout_find(
                layout, f"% OF STUDENTS TAKING {s} TESTS (SCHOOL)", group=g, section="SCHOOL")
        fields[("alltests", subj)] = layout_find(layout, f"2017 SCHOOL PERCENT OF PROFICIENCY IN {s}", test="ALL TESTS")
    rows = read_rc17_lines("isbe/rc17_assessment.zip", "rc17_assessment.txt", len(layout))
    for rid, parts in sorted(rows.items()):
        for key, spec in fields.items():
            if key[0] == "lv":
                _, subj, grp, gr = key
                raw = {f"pct_level{L}": parts[spec[L - 1] - 1] for L in range(1, 6)}
                vals, sup, anyv = cells(raw, "isbe_levels:2017")
                if not anyv:
                    continue
                s45 = levels_sum45(vals)
                scores.append(score_row(
                    school_id=rid, year="2017", subject=subj, group=grp, group_label="ALL" if grp == "all" else "LEP",
                    grade=gr, source="isbe_levels", test_scope="parcc",
                    pct_proficient=fmt(s45), pct_proficient_method="L4+L5" if s45 is not None else "",
                    n_levels="5", suppressed="1" if sup else "0",
                    **{k: fmt(v) for k, v in vals.items()}))
            elif key[0] == "acct":
                _, subj, grp = key
                raw = {"pct": parts[spec - 1], "part": parts[fields[("taking", subj, grp)] - 1]}
                vals, sup, anyv = cells(raw, "isbe_rc17_acct:2017")
                if not anyv:
                    continue
                scores.append(score_row(
                    school_id=rid, year="2017", subject=subj, group=grp, group_label="ALL" if grp == "all" else "LEP",
                    grade="school", source="isbe_rc17_acct", test_scope="all_tests_accountability",
                    pct_proficient=fmt(vals["pct"]),
                    pct_proficient_method="published" if vals["pct"] is not None else "",
                    participation_rate=fmt(vals["part"]), suppressed="1" if sup else "0"))
            elif key[0] == "alltests":
                _, subj = key
                vals, sup, anyv = cells({"pct": parts[spec - 1]}, "isbe_rc17_all_tests:2017")
                if not anyv:
                    continue
                scores.append(score_row(  # layout field has no student-group label (its "group" is "2017-ELA")
                    school_id=rid, year="2017", subject=subj, group="all", group_label="",
                    grade="school", source="isbe_rc17_all_tests", test_scope="all_tests",
                    pct_proficient=fmt(vals["pct"]),
                    pct_proficient_method="published" if vals["pct"] is not None else "",
                    suppressed="1" if sup else "0"))
    checks["isbe2017_assessment_school_rows"] = len(rows)


def isbe_levels(year, book, scores):
    sheet_names, tmpl, scope = LEVEL_SPEC[year]
    sheets = [IsbeSheet(book, s) for s in sheet_names]
    for subj in ("ela", "math"):
        for grp in ("all", "el"):
            for gr in range(3, 9):
                refs = [locate(sheets, tmpl.format(grp=LEVEL_GROUP[grp], subj=SUBJ_LABEL[subj], L=L, G=gr))
                        for L in range(1, 6)]
                rids = sorted(set().union(*[s.rows.keys() for s in sheets]))
                for rid in rids:
                    raw = {}
                    for L, (sh, ci) in enumerate(refs, start=1):
                        r = sh.rows.get(rid)
                        raw[f"pct_level{L}"] = r[ci] if r is not None else ""
                    vals, sup, anyv = cells(raw, f"isbe_levels:{year}")
                    if not anyv:
                        continue
                    s45 = levels_sum45(vals)
                    scores.append(score_row(
                        school_id=rid, year=str(year), subject=subj, group=grp,
                        group_label=f"{LEVEL_GROUP[grp]} students", grade=str(gr), source="isbe_levels",
                        test_scope=scope, pct_proficient=fmt(s45),
                        pct_proficient_method="L4+L5" if s45 is not None else "",
                        n_levels="5", suppressed="1" if sup else "0",
                        **{k: fmt(v) for k, v in vals.items()}))


def isbe_iar_grade_2025(book, scores):
    sh = IsbeSheet(book, "IAR")
    for subj, s in (("ela", "ELA"), ("math", "Math")):
        for grp, g in (("all", "Total"), ("el", "EL")):
            for gr in range(3, 9):
                ci_p = sh.col(f"IAR {s} Proficiency Rate Grade {gr} - {g}")
                ci_r = sh.col(f"IAR {s} Participation Rate Grade {gr} - {g}")
                for rid, r in sorted(sh.rows.items()):
                    vals, sup, anyv = cells({"pct": r[ci_p], "part": r[ci_r]}, "isbe_iar_grade:2025")
                    if not anyv:
                        continue
                    scores.append(score_row(
                        school_id=rid, year="2025", subject=subj, group=grp, group_label=g, grade=str(gr),
                        source="isbe_iar_grade", test_scope="iar", pct_proficient=fmt(vals["pct"]),
                        pct_proficient_method="published" if vals["pct"] is not None else "",
                        participation_rate=fmt(vals["part"]), n_levels="4",
                        suppressed="1" if sup else "0"))


def isbe_parcc_sat_2018(scores, checks):
    book = Book("isbe/2018-PARCC-SAT-Proficient.xlsx")
    rows = book.rows("2018 PARCC_SAT_enrollment")
    hdr_i = next(i for i, r in enumerate(rows[:12]) if str(r[0]).strip() == "RCDTS")
    grade_row, subj_row, hdr = rows[hdr_i - 2], rows[hdr_i - 1], rows[hdr_i]
    blocks = {}
    cur_grade = cur_subj = None
    for i, h in enumerate(hdr):
        if str(grade_row[i]).strip():
            cur_grade = str(grade_row[i]).strip()
        if str(subj_row[i]).strip():
            cur_subj = str(subj_row[i]).strip()
        if norm(h) == "% meets":
            if norm(hdr[i + 1]) != "# tested" or norm(hdr[i + 2]) != "# proficient":
                raise ValueError(f"2018 PARCC/SAT: unexpected block layout at column {i}")
            blocks[(cur_grade, cur_subj)] = i
    wanted = {}
    for gr in range(3, 9):
        for subj, s in (("ela", "ELA"), ("math", "Math")):
            wanted[(str(gr), subj)] = blocks[(f"Grade {gr}", s)]
    for subj, s in (("ela", "ELA"), ("math", "Math")):
        wanted[("3-8", subj)] = blocks[("Grade 3-8", s)]
    n = 0
    for r in rows[hdr_i + 1:]:
        rid = str(r[0]).strip().upper()
        if not rid.startswith(CPS_PREFIX) or rid.endswith("0000"):
            continue
        if not RCDTS_RE.match(rid):
            raise ValueError(f"2018 PARCC/SAT: malformed RCDTS {rid!r}")
        n += 1
        for (gr, subj), i in sorted(wanted.items()):
            vals, sup, anyv = cells({"pct": r[i], "den": r[i + 1], "prof": r[i + 2]}, "isbe_parcc_sat_2018:2018")
            if not anyv:
                continue
            scores.append(score_row(
                school_id=rid, year="2018", subject=subj, group="all", group_label="All students", grade=gr,
                source="isbe_parcc_sat_2018", test_scope="parcc", n_denominator=fmt(vals["den"]),
                n_proficient=fmt(vals["prof"]), pct_proficient=fmt(vals["pct"]),
                pct_proficient_method="published" if vals["pct"] is not None else "",
                suppressed="1" if sup else "0"))
    checks["isbe2018_parcc_sat_school_rows"] = n


def isbe_scores(year, book, scores, checks):
    if year in LEVEL_SPEC:
        isbe_levels(year, book, scores)
    raw_store = {}
    if year == 2018:
        sh = IsbeSheet(book, "ELA and Math")
        check_2018_math_el(sh, checks)
        emit_school_measures(year, [sh], ALLTESTS_2018, source="isbe_all_tests", test_scope="all_tests",
                             grade="school", scores=scores, raw_store=raw_store)
    elif year in (2019, 2021, 2022, 2023):
        sh = IsbeSheet(book, "ELA Math Science")
        spec = dict(ALLTESTS_1923)
        if year == 2019:  # the 2019 EL math participation-rate header is a duplicate "IEP" label; not used
            spec[("math", "el")] = {k: v for k, v in spec[("math", "el")].items() if k != "part"}
        emit_school_measures(year, [sh], spec, source="isbe_all_tests", test_scope="all_tests",
                             grade="school", scores=scores, raw_store=raw_store)
    elif year == 2024:
        emit_school_measures(year, [IsbeSheet(book, "ELAMathScience")], ALLTESTS_2024, source="isbe_all_tests",
                             test_scope="all_tests", grade="school", scores=scores)
    elif year == 2025:
        ems = IsbeSheet(book, "ELAMathScience")
        emit_school_measures(year, [ems], ALLTESTS_2025, source="isbe_all_tests", test_scope="all_tests",
                             grade="school", scores=scores)
        emit_school_measures(year, [ems], ALLTESTS_2025_38, source="isbe_all_tests", test_scope="all_tests",
                             grade="3-8", scores=scores)
        isbe_iar_grade_2025(book, scores)
    if year in IAR38:
        sheets = [IsbeSheet(book, s) for s in IAR38_SHEETS[year]]
        emit_school_measures(year, sheets, IAR38[year], source="isbe_iar_3_8",
                             test_scope="parcc" if year == 2018 else "iar", grade="3-8", scores=scores)
    if raw_store:
        check_min_el_participation(year, raw_store, checks)
        derive_non_el(year, raw_store, scores, checks)


# ----------------------------------------------------------------------------- CPS sources

def cps_school_year_label(book: Book) -> int:
    for sn in book.names:
        for r in book.rows(sn)[:4]:
            for v in r:
                m = re.search(r"20th Day (\d{4})-(\d{4})", str(v))
                if m:
                    return int(m.group(2))
    raise ValueError(f"{book.rel}: no '20th Day YYYY-YYYY' label")


def header_row(rows, must: str, limit: int = 8) -> int:
    for i, r in enumerate(rows[:limit]):
        if any(norm(v) == norm(must) for v in r):
            return i
    raise ValueError(f"no header row containing {must!r}")


def cps_lep(year: int, checks):
    book = Book(CPS_LEP[year])
    label_year = cps_school_year_label(book)
    if label_year != year:
        raise ValueError(f"{book.rel}: file says spring {label_year}, expected {year}")
    rows = book.rows("Schools")
    h = header_row(rows, "School ID")
    hdr, grp = rows[h], rows[h - 1]
    id_i, name_i, tot_i = one_col(hdr, "School ID", book.rel), one_col(hdr, "School Name", book.rel), one_col(hdr, "Total", book.rel)
    net_i = one_col(hdr, "Network", book.rel)
    gov_i = one_col(hdr, "Governance", book.rel) if find_cols(hdr, "Governance", book.rel) else None
    el_label = None
    for i, v in enumerate(grp):
        if norm(v) in ("bilingual", "state english learners"):
            if el_label is not None:
                raise ValueError(f"{book.rel}: two EL group labels")
            el_label, el_i = str(v).strip(), i
    if el_label is None or norm(hdr[el_i]) != "n":
        raise ValueError(f"{book.rel}: EL count column not found under its group label")
    out, dist_total = {}, None
    for r in rows[h + 1:]:
        name = str(r[name_i]).strip()
        rid_raw = str(r[id_i]).strip()
        if not rid_raw:
            if "district total" in norm(name):
                dist_total = (parse(r[tot_i])[1], parse(r[el_i])[1])
            elif any(str(v).strip() for v in r):
                NOTES.append(f"{book.rel}: {' | '.join(str(v).strip() for v in r if str(v).strip())}")
            continue
        if is_note_row(r, id_i):
            NOTES.append(f"{book.rel}: {rid_raw}")
            continue
        cid = cps_id(r[id_i])
        kt, tot = TALLY.get(r[tot_i], f"cps20_lep:{year}")
        ke, el = TALLY.get(r[el_i], f"cps20_lep:{year}")
        if cid in out:
            raise ValueError(f"{book.rel}: duplicate School ID {cid}")
        out[cid] = {"name": name, "total": tot, "el": el, "label": el_label,
                    "network": re.sub(r"\s+", " ", str(r[net_i])).strip(),
                    "governance": re.sub(r"\s+", " ", str(r[gov_i])).strip() if gov_i is not None else ""}
    if dist_total is None:  # 2024-25 files carry the district total on the District sheet only
        drows = book.rows("District")
        for r in drows:
            if norm(r[0]) == "district total":
                dist_total = (parse(r[1])[1], parse(r[2])[1])
                break
    s_tot = sum((v["total"] or 0) for v in out.values())
    s_el = sum((v["el"] or 0) for v in out.values())
    checks[f"cps20_lep_{year}"] = {"schools": len(out), "sum_school_total": fmt(s_tot), "sum_school_el": fmt(s_el),
                                   "district_total": fmt(dist_total[0]) if dist_total else "",
                                   "district_el": fmt(dist_total[1]) if dist_total else "", "el_label": el_label}
    return out


def cps_membership(year: int):
    book = Book(CPS_MEMBERSHIP[year])
    sheet = book.names[0]
    if len(book.names) != 1:
        raise ValueError(f"{book.rel}: expected one sheet, got {book.names}")
    rows = book.rows(sheet)
    h = header_row(rows, "School ID")
    hdr = rows[h]
    id_i, name_i = one_col(hdr, "School ID", book.rel), one_col(hdr, "School Name", book.rel)
    tot_i, pe_i, pk_i = one_col(hdr, "Total", book.rel), one_col(hdr, "PE", book.rel), one_col(hdr, "PK", book.rel)
    out = {}
    for r in rows[h + 1:]:
        if not str(r[id_i]).strip():
            continue
        if is_note_row(r, id_i):
            NOTES.append(f"{book.rel}: {str(r[id_i]).strip()}")
            continue
        cid = cps_id(r[id_i])
        if cid in out:
            raise ValueError(f"{book.rel}: duplicate School ID {cid}")
        out[cid] = {"name": str(r[name_i]).strip(), "total": parse(r[tot_i])[1],
                    "pe": parse(r[pe_i])[1] or Decimal(0), "pk": parse(r[pk_i])[1] or Decimal(0)}
    return out


BUDGET_COLS = {
    "cps_budget_enroll_20th": "Fall 2023 20th Day Enrollment",
    "cps_budget_noncluster_enroll": "Fall 2023 20th Day Non-Cluster Enrollment",
    "cps_budget_newcomer_adj": "Adjustment for Schools With Increased Enrollment Due to Newcomer Students",
    "cps_budget_teacher_enroll_input": "Enrollment Input for Teacher Allocations (Non-Cluster + Newcomer Adjustment)",
    "cps_budget_core_teacher_ratio": "Student : Teacher Ratio for Core Classroom Teachers (Unadjusted for Floor)",
    "cps_budget_core_classroom_teachers": "Core Classroom",
    "cps_budget_bilingual_coordinators": "Bilingual Coordinators",
    "cps_budget_stls_advocates": "STLS Advocates",
}


def cps_budget_fy2025(memb2024, checks):
    book = Book(BUDGET_FY2025)
    rows = book.rows("Traditional")
    h = header_row(rows, "School Name")
    hdr = rows[h]
    name_i = one_col(hdr, "School Name", book.rel)
    idx = {k: one_col(hdr, v, book.rel) for k, v in BUDGET_COLS.items()}
    by_name = defaultdict(list)
    for cid, m in memb2024.items():
        by_name[m["name"]].append(cid)
    out, unmatched, enroll_mismatch = {}, [], []
    n_rows = n_pos = 0
    tot_adj = Decimal(0)
    for r in rows[h + 1:]:
        name = str(r[name_i]).strip()
        if not name:
            continue
        n_rows += 1
        vals = {}
        for k, i in idx.items():
            cell = r[i]
            if k == "cps_budget_core_teacher_ratio":  # published as text, e.g. '22:1'
                m = re.match(r"^\s*(\d+(?:\.\d+)?)\s*:\s*1\s*$", str(cell))
                if not m:
                    raise ValueError(f"budget: unexpected ratio {cell!r} for {name}")
                cell = m.group(1)
            kind, v = TALLY.get(cell, "cps_budget_fy2025:2025")
            if kind == "sup":
                raise ValueError("unexpected suppression marker in budget file")
            vals[k] = v
        adj = vals["cps_budget_newcomer_adj"]
        if adj is None:
            raise ValueError(f"budget: blank newcomer adjustment for {name}")
        if adj < 0:
            raise ValueError(f"budget: negative newcomer adjustment for {name}")
        tot_adj += adj
        n_pos += adj > 0
        ids = by_name.get(name, [])
        if len(ids) != 1:
            unmatched.append({"name": name, "newcomer_adj": fmt(adj), "candidates": len(ids)})
            continue
        m = memb2024[ids[0]]
        if vals["cps_budget_enroll_20th"] != m["total"] - m["pe"] - m["pk"]:
            enroll_mismatch.append({"name": name, "cps_school_id": ids[0]})
            continue
        if ids[0] in out:
            raise ValueError(f"budget: two budget rows match {ids[0]}")
        out[ids[0]] = vals
    checks["cps_budget_fy2025"] = {
        "traditional_rows": n_rows, "schools_with_positive_newcomer_adj": n_pos, "sum_newcomer_adj": fmt(tot_adj),
        "matched_by_exact_name_and_k12_enrollment": len(out), "unmatched_by_name": unmatched,
        "enrollment_check_failed": enroll_mismatch,
        "match_rule": "budget School Name == SY2023-24 20th-day School Name, and budget 'Fall 2023 20th Day "
                      "Enrollment' == 20th-day Total - PE - PK"}
    return out


CPS_TEST_RE = [
    (re.compile(r"^ELA/Literacy Grade ([3-8])$"), "ela", None),
    (re.compile(r"^Combined ELA Grades 3-8$"), "ela", "3-8"),
    (re.compile(r"^Mathematics Grade ([3-8])$"), "math", None),
    (re.compile(r"^Combined Math Grades 3-8$"), "math", "3-8"),
    (re.compile(r"^Algebra I Grade ([78])$"), "math", None),
]


def cps_iar_1524(scores, checks):
    book = Book(CPS_IAR_1524)
    skipped = Counter()
    seen = set()
    for subj, sheet, mean_name in (("ela", "IAR-PARCC ELA Results", "Overall ELA Mean Scale Score"),
                                   ("math", "IAR-PARCC Math Results", "Overall Math Mean Scale Score")):
        rows = book.rows(sheet)
        h = header_row(rows, "School ID")
        hdr = rows[h]
        lab = f"{book.rel}!{sheet}"
        c = {"id": one_col(hdr, "School ID", lab), "year": one_col(hdr, "Year", lab), "test": one_col(hdr, "Test Name", lab),
             "n": one_col(hdr, "# Students Tested", lab), "mean": one_col(hdr, mean_name, lab),
             "l1": one_col(hdr, "% Did Not Meet", lab), "l2": one_col(hdr, "% Partially Met", lab),
             "l3": one_col(hdr, "% Approached", lab, nth=0), "l4": one_col(hdr, "% Met", lab),
             "l5": one_col(hdr, "% Exceeded", lab), "me": one_col(hdr, "% Met or Exceeded", lab, nth=0)}
        order = [c["mean"], c["l1"], c["l2"], c["l3"], c["l4"], c["l5"], c["me"]]
        if order != list(range(c["mean"], c["mean"] + 7)):
            raise ValueError(f"{lab}: overall performance-level block not contiguous after the mean")
        for r in rows[h + 1:]:
            if not str(r[c["id"]]).strip():
                continue
            yr = int(parse(r[c["year"]])[1])
            test = str(r[c["test"]]).strip()
            if yr < 2017:
                continue
            grade = None
            for rx, s, fixed in CPS_TEST_RE:
                m = rx.match(test)
                if m and s == subj:
                    grade = fixed or m.group(1)
                    break
            if grade is None:
                skipped[test] += 1
                continue
            cid = cps_id(r[c["id"]])
            key = (cid, yr, subj, test)
            if key in seen:
                raise ValueError(f"{lab}: duplicate {key}")
            seen.add(key)
            raw = {"n": r[c["n"]], "mean": r[c["mean"]], "pct_level1": r[c["l1"]], "pct_level2": r[c["l2"]],
                   "pct_level3": r[c["l3"]], "pct_level4": r[c["l4"]], "pct_level5": r[c["l5"]], "pct": r[c["me"]]}
            vals, sup, anyv = cells(raw, f"cps_iar_1524:{yr}")
            if not anyv:
                continue
            scores.append(score_row(  # the CPS file has no student-group dimension, so no group label
                cps_school_id=cid, year=str(yr), subject=subj, group="all", group_label="",
                grade=grade, source="cps_iar_1524", test_scope="iar" if yr >= 2019 else "parcc",
                test_name=test, n_tested=fmt(vals["n"]), pct_proficient=fmt(vals["pct"]),
                pct_proficient_method="published" if vals["pct"] is not None else "",
                mean_scale_score=fmt(vals["mean"]), n_levels="5", suppressed="1" if sup else "0",
                **{f"pct_level{L}": fmt(vals[f"pct_level{L}"]) for L in range(1, 6)}))
    checks["cps_iar_1524_skipped_tests"] = dict(sorted(skipped.items()))


CPS25_GROUPS = {
    ("ALL", "All Students"): ("all", "3-8"),
    ("English Learner Status", "EL Students"): ("el", "3-8"),
    ("English Learner Status", "Non-EL Students"): ("non_el", "3-8"),
    ("Temporary Living Situation Status", "STLS Students"): ("stls", "3-8"),
    ("Temporary Living Situation Status", "Non-STLS Students"): ("non_stls", "3-8"),
}
CPS25_NOTE = "Data not reported because there are fewer than 10 students in this group."


def cps_iar_2025(scores, checks):
    book = Book(CPS_IAR_25)
    rows = book.rows("Data")
    h = header_row(rows, "School Code")
    hdr = rows[h]
    lab = f"{book.rel}!Data"
    c = {k: one_col(hdr, v, lab) for k, v in {
        "id": "School Code", "sy": "School Year", "test": "Test Name", "cat": "Category", "grp": "Student Group",
        "pct": "%At or Above Proficient", "l4": "%Above Proficient", "l3": "%Proficient", "l2": "%Approaching Proficient",
        "l1": "%Below Proficient", "n": "#Tested", "np": "#At or Above Proficient", "note": "Notes"}.items()}
    tested = {}
    seen = set()
    for r in rows[h + 1:]:
        code = str(r[c["id"]]).strip()
        if code in ("", "--"):
            continue
        if str(r[c["sy"]]).strip() != "2024-2025":
            raise ValueError(f"{lab}: unexpected school year {r[c['sy']]!r}")
        subj = {"IAR ELA": "ela", "IAR MATH": "math"}[str(r[c["test"]]).strip()]
        cat, grp_label = str(r[c["cat"]]).strip(), str(r[c["grp"]]).strip()
        m = re.match(r"^Grade ([3-8]) Students$", grp_label)
        if cat == "Grade Level" and m:
            grp, grade = "all", m.group(1)
        elif (cat, grp_label) in CPS25_GROUPS:
            grp, grade = CPS25_GROUPS[(cat, grp_label)]
        else:
            continue
        cid = cps_id(r[c["id"]])
        key = (cid, subj, grp, grade)
        if key in seen:
            raise ValueError(f"{lab}: duplicate {key}")
        seen.add(key)
        note = str(r[c["note"]]).strip()
        if note not in ("", CPS25_NOTE):
            raise ValueError(f"{lab}: unexpected note {note!r}")
        raw = {k: r[c[k]] for k in ("pct", "l1", "l2", "l3", "l4", "n", "np")}
        vals, sup, anyv = cells(raw, "cps_iar_2025:2025")
        sup = sup or note == CPS25_NOTE
        if not anyv and not sup:
            continue
        if grade == "3-8":
            tested[(cid, subj, grp)] = vals["n"]
        scores.append(score_row(
            cps_school_id=cid, year="2025", subject=subj, group=grp, group_label=grp_label, grade=grade,
            source="cps_iar_2025", test_scope="iar", test_name=str(r[c["test"]]).strip(), n_tested=fmt(vals["n"]),
            n_proficient=fmt(vals["np"]), pct_proficient=fmt(vals["pct"]),
            pct_proficient_method="published" if vals["pct"] is not None else "",
            pct_level1=fmt(vals["l1"]), pct_level2=fmt(vals["l2"]), pct_level3=fmt(vals["l3"]),
            pct_level4=fmt(vals["l4"]), n_levels="4", suppressed="1" if sup else "0"))
    agree = disagree = 0
    for (cid, subj, grp), n in tested.items():
        if grp != "all" or n is None:
            continue
        e, ne = tested.get((cid, subj, "el")), tested.get((cid, subj, "non_el"))
        if e is not None and ne is not None:
            if e + ne == n:
                agree += 1
            else:
                disagree += 1
    checks["cps2025_el_plus_non_el_equals_all_tested"] = {"agree": agree, "disagree": disagree}


# ----------------------------------------------------------------------------- CPS staffing rosters

TEACHER_EXCLUDE = ("assist", "asst", "aide", "dir,", "director", "chief", "coord", "manager", "mgr", "pathway",
                   "recruit", "eval", "leadership", "teaching", "residency", "speech", "retired", "analyst")


def is_teacher(title: str) -> bool:
    t = title.lower()
    return "teacher" in t and not any(x in t for x in TEACHER_EXCLUDE)


def dept_key(v) -> str:
    s = str(v).strip()
    try:
        kind, d = parse(v)
    except ValueError:
        return s
    if kind == "num" and d == d.to_integral_value():
        return str(int(d))
    return s


def load_finance_ids(checks):
    fin = {}
    for y, rel in sorted(PROFILES.items()):
        m = defaultdict(set)
        with open(CACHE / rel, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                fid = r["Finance_ID"].strip()
                if fid:
                    m[dept_key(fid)].add(cps_id(r["School_ID"]))
        fin[y] = dict(m)
        checks[f"profile_finance_ids_{y}"] = {
            "finance_ids": len(m), "shared_by_several_school_ids": sorted(k for k, v in m.items() if len(v) > 1)}
    across = defaultdict(set)
    for y, m in fin.items():
        for fid, ids in m.items():
            if len(ids) == 1:
                across[fid] |= ids
    checks["profile_finance_ids_mapping_to_different_school_ids_across_years"] = {
        k: sorted(v) for k, v in sorted(across.items()) if len(v) > 1}
    return fin


def roster_files():
    out = []
    for rel in INPUTS:
        if not rel.startswith("cps_positions/"):
            continue
        m = re.search(r"roster[_-](\d{2})(\d{2})(\d{4})(?:-\d+)?\.xls$", rel)
        if not m:
            raise ValueError(f"cannot date roster file {rel}")
        out.append((f"{m.group(3)}-{m.group(1)}-{m.group(2)}", rel))
    return sorted(out)


def spring_year(date_iso: str) -> int:
    y, mth = int(date_iso[:4]), int(date_iso[5:7])
    return y + 1 if mth >= 7 else y


STAFF_SUMS = ("fte_all", "fte_filled", "fte_teacher", "fte_teacher_filled", "fte_regular_teacher",
              "fte_bilingual_teacher", "fte_sped_teacher", "fte_salary_filled", "benefit_cost_filled")
STAFF_TITLES = {"Regular Teacher": "fte_regular_teacher", "Bilingual Teacher": "fte_bilingual_teacher",
                "Special Education Teacher": "fte_sped_teacher"}


def staff_quarterly(fin, checks):
    """Sum CPS quarterly employee position rosters by school department (Dept ID) and snapshot date.

    One roster row is one position line; a blank Name is a vacancy. FTE sums run over rows as published,
    so the ~1% of rows that share a Pos # with another named row (two incumbents, each FTE 1) count twice;
    n_rows_shared_pos reports them. Salary and benefit sums cover filled rows only, because CPS stopped
    listing compensation for vacant positions from the June 30, 2023 file. The roster lists CPS employees
    only: at charter and contract schools it holds the few CPS-employed positions carrying the school's
    department ID, not the school's staff (filter on cps_governance / cps_network)."""
    out, teacher_titles, per_file = [], Counter(), {}
    for date, rel in roster_files():
        with open(CACHE / rel, "rb") as f:  # content-sniffed: the 03/31/2017 file is xlsx despite its .xls name
            wb = python_calamine.CalamineWorkbook.from_filelike(io.BytesIO(f.read()))
        if len(wb.sheet_names) != 1:
            raise ValueError(f"{rel}: expected one sheet, got {wb.sheet_names}")
        rows = wb.get_sheet_by_name(wb.sheet_names[0]).to_python()
        hdr = rows[0]
        c = {k: one_col(hdr, v, rel) for k, v in {
            "pos": "Pos #", "dept": "Dept ID", "dname": "Department", "fte": "FTE", "sal": "FTE Annual Salary",
            "ben": "Annual Benefit Cost", "title": "Job Title", "name": "Name"}.items()}
        recs = []
        for r in rows[1:]:
            if all(not str(v).strip() for v in r):
                continue
            kf, fte = parse(r[c["fte"]])
            if kf != "num":
                raise ValueError(f"{rel}: position {r[c['pos']]!r} has no FTE")
            _, sal = parse(r[c["sal"]])
            _, ben = parse(r[c["ben"]])
            recs.append({"pos": dept_key(r[c["pos"]]), "dept": dept_key(r[c["dept"]]),
                         "dname": re.sub(r"\s+", " ", str(r[c["dname"]])).strip(), "fte": fte, "sal": sal,
                         "ben": ben, "title": re.sub(r"\s+", " ", str(r[c["title"]])).strip(),
                         "vacant": not str(r[c["name"]]).strip()})  # blank Name; a real employee is named "Vacanti"
        pos_n = Counter(x["pos"] for x in recs)
        sy = spring_year(date)
        agg = {}
        for x in recs:
            a = agg.get(x["dept"])
            if a is None:
                a = agg[x["dept"]] = {"department": x["dname"], "n_rows": 0, "n_rows_vacant": 0,
                                      "n_rows_shared_pos": 0, "titles": Counter(),
                                      **{k: Decimal(0) for k in STAFF_SUMS}}
            fte, filled, teacher = x["fte"], not x["vacant"], is_teacher(x["title"])
            a["n_rows"] += 1
            a["n_rows_vacant"] += x["vacant"]
            a["n_rows_shared_pos"] += pos_n[x["pos"]] > 1
            a["fte_all"] += fte
            if teacher:
                a["titles"][x["title"]] += 1
                a["fte_teacher"] += fte
            if x["title"] in STAFF_TITLES:
                a[STAFF_TITLES[x["title"]]] += fte
            if filled:
                a["fte_filled"] += fte
                a["fte_salary_filled"] += x["sal"] or 0
                a["benefit_cost_filled"] += x["ben"] or 0
                if teacher:
                    a["fte_teacher_filled"] += fte
        n_school = n_shared = n_other = 0
        for dept, a in sorted(agg.items()):
            hit = next(((y, fin[y][dept]) for _, y in sorted((abs(sy - y), y) for y in fin) if dept in fin[y]), None)
            if hit is None:
                n_other += a["n_rows"]
                continue
            y_used, ids = hit
            if len(ids) != 1:
                n_shared += a["n_rows"]
                continue
            n_school += a["n_rows"]
            teacher_titles.update(a["titles"])
            row = {"city": CITY, "school_id": "", "cps_school_id": next(iter(ids)), "dept_id": dept,
                   "department": a["department"], "snapshot_date": date, "school_year": str(sy),
                   "n_rows": str(a["n_rows"]), "n_rows_vacant": str(a["n_rows_vacant"]),
                   "n_rows_shared_pos": str(a["n_rows_shared_pos"]), "dept_map_source": f"profile_{y_used}"}
            row.update({k: fmt(a[k], 2) for k in STAFF_SUMS})
            out.append(row)
        per_file[date] = {
            "file": rel, "rows": len(recs), "rows_sharing_a_pos_number": sum(n for n in pos_n.values() if n > 1),
            "vacant_rows": sum(x["vacant"] for x in recs),
            "vacant_rows_with_salary": sum(1 for x in recs if x["vacant"] and x["sal"] is not None),
            "rows_at_mapped_schools": n_school, "rows_at_shared_finance_ids": n_shared,
            "rows_not_at_schools": n_other}
    checks["staff_rosters"] = per_file
    checks["staff_teacher_titles_counted"] = dict(sorted(teacher_titles.items()))
    return out


# ----------------------------------------------------------------------------- crosswalk

def load_progress(checks):
    maps = {}
    for py, rel in sorted(PROGRESS.items()):
        m, invalid, blank = {}, 0, 0
        with open(CACHE / rel, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f):
                cid = cps_id(r["School_ID"])
                url = r["State_School_Report_Card_URL"] or ""
                hit = re.search(r"schoolid=([0-9A-Za-z]+)", url)
                rc = hit.group(1).upper() if hit else None
                if rc is None:
                    blank += 1
                elif not RCDTS_RE.match(rc):
                    invalid += 1
                    rc = None
                if cid in m:
                    raise ValueError(f"{rel}: duplicate School_ID {cid}")
                m[cid] = rc
        maps[py] = m
        checks[f"progress_{py}"] = {"rows": len(m), "no_url": blank, "invalid_schoolid": invalid}
    return maps


def crosswalk_year(year, cids, isbe_ids, maps):
    """Map each CPS ID to an RCDTS present in that year's ISBE file, taking the progress-report year
    nearest to `year` (ties to the earlier). Pass 2: a CPS ID whose nearest RCDTS is shared with other
    CPS IDs moves to its next-nearest candidate if that RCDTS is in the ISBE file and unclaimed; this
    fixes SY2016-17 progress links that point charter campuses at a network-level RCDTS while the
    2017 ISBE file also reports the campus itself. Scores agreement in the audit tests the result."""
    cands = {}
    for cid in cids:
        c = sorted((abs(year - py), py, m[cid]) for py, m in maps.items()
                   if m.get(cid) is not None and m[cid] in isbe_ids)
        if c:
            cands[cid] = c
    chosen = {cid: (c[0][2], c[0][1]) for cid, c in cands.items()}
    by_rc = defaultdict(list)
    for cid, (rc, py) in chosen.items():
        by_rc[rc].append(cid)
    claimed = set(by_rc)
    for cid in sorted(chosen):
        rc, py = chosen[cid]
        if len(by_rc[rc]) < 2:
            continue
        for _, py2, rc2 in cands[cid][1:]:
            if rc2 != rc and rc2 not in claimed:
                chosen[cid] = (rc2, py2)
                claimed.add(rc2)
                break
    by_rc = defaultdict(list)
    for cid, (rc, py) in chosen.items():
        by_rc[rc].append(cid)
    status = {}
    for cid in cids:
        if cid not in chosen:
            status[cid] = ("unmapped", "", "", 0)
        else:
            rc, py = chosen[cid]
            n = len(by_rc[rc])
            status[cid] = ("attached" if n == 1 else "shared_rcdts", rc, py, n)
    return status, by_rc


# ----------------------------------------------------------------------------- main

def write_csv(path: Path, cols, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(cols)
        for r in rows:
            w.writerow([r[c] for c in cols])


GRADE_ORDER = {str(g): (0, g) for g in range(3, 9)}
GRADE_ORDER.update({"3-8": (1, 0), "school": (2, 0)})


def agreement_isbe_cps(scores):
    """Per-grade all-student level distributions published by both ISBE and CPS for the same school:
    count cells where all five level percentages agree exactly, within 1 point, or differ by more."""
    isbe, cps = {}, {}
    for r in scores:
        if r["group"] != "all" or len(r["grade"]) != 1 or not r["school_id"]:
            continue
        k = (r["year"], r["school_id"], r["subject"], r["grade"])
        if r["source"] == "isbe_levels":
            isbe[k] = r
        elif r["source"] == "cps_iar_1524" and not r["test_name"].startswith("Algebra"):
            cps[k] = r
    out = defaultdict(Counter)
    for k, a in sorted(isbe.items()):
        b = cps.get(k)
        lv = [f"pct_level{L}" for L in range(1, 6)]
        if b is None or any(a[x] == "" or b[x] == "" for x in lv):
            continue
        d = max(abs(Decimal(a[x]) - Decimal(b[x])) for x in lv)
        out[k[0]]["exact" if d == 0 else ("within_1pt" if d <= 1 else "over_1pt")] += 1
    return {y: dict(sorted(c.items())) for y, c in sorted(out.items())}


def main():
    verify_inputs()
    OUT.mkdir(exist_ok=True)
    checks = {}
    scores = []

    # ISBE
    layout_rc17 = parse_layout(Book("isbe/RC17_layout.xlsx"), "RC17")
    layout_asmt = parse_layout(Book("isbe/RC17_layout.xlsx"), "Assessment")
    general = {2017: isbe_general_2017(layout_rc17)}
    isbe_scores_2017(layout_asmt, scores, checks)
    isbe_parcc_sat_2018(scores, checks)
    for year, rel in sorted(ISBE_FILES.items()):
        book = Book(rel)
        general[year] = isbe_general(year, book)
        isbe_scores(year, book, scores, checks)
        del book

    # CPS
    lep = {y: cps_lep(y, checks) for y in YEARS}
    memb = {y: cps_membership(y) for y in YEARS}
    for y in YEARS:
        diff = sorted(cid for cid in lep[y] if cid in memb[y] and lep[y][cid]["total"] != memb[y][cid]["total"])
        only_lep = sorted(set(lep[y]) - set(memb[y]))
        only_memb = sorted(set(memb[y]) - set(lep[y]))
        checks[f"cps20_lep_vs_membership_{y}"] = {"total_differs": diff, "only_in_lep_file": only_lep,
                                                   "only_in_membership_file": only_memb}
    budget = cps_budget_fy2025(memb[2024], checks)
    cps_iar_1524(scores, checks)
    cps_iar_2025(scores, checks)

    # CPS IDs present in any CPS source, by year
    cps_ids = defaultdict(set)
    cps_names = defaultdict(dict)
    for y in YEARS:
        for cid, v in lep[y].items():
            cps_ids[y].add(cid)
            cps_names[y][cid] = v["name"]
    for cid in budget:
        cps_ids[2024].add(cid)
        cps_ids[2025].add(cid)
        cps_names[2024].setdefault(cid, memb[2024][cid]["name"])
    for r in scores:
        if r["cps_school_id"]:
            cps_ids[int(r["year"])].add(r["cps_school_id"])

    # CPS quarterly position rosters -> school (Dept ID) x snapshot
    fin = load_finance_ids(checks)
    staff = staff_quarterly(fin, checks)
    staff_by = {}
    for r in staff:
        k = (r["cps_school_id"], r["snapshot_date"])
        if k in staff_by:
            raise ValueError(f"two roster departments map to CPS school {k[0]} on {k[1]}: "
                             f"{staff_by[k]['dept_id']}, {r['dept_id']}")
        staff_by[k] = r

    maps = load_progress(checks)
    xw, xw_rows = {}, []
    for y in YEARS:
        status, by_rc = crosswalk_year(y, sorted(cps_ids[y]), set(general[y]), maps)
        xw[y] = (status, by_rc)
        cnt = Counter(s[0] for s in status.values())
        matched_rc = {s[1] for s in status.values() if s[0] != "unmapped"}
        checks[f"crosswalk_{y}"] = {"cps_ids": len(status), **dict(sorted(cnt.items())),
                                    "isbe_schools": len(general[y]),
                                    "isbe_schools_without_cps_id": len(set(general[y]) - matched_rc)}
        for cid, (st, rc, py, n) in status.items():
            xw_rows.append({"year": str(y), "cps_school_id": cid, "cps_name": cps_names[y].get(cid, ""),
                            "school_id": rc, "status": st, "progress_year_used": str(py) if py else "",
                            "n_cps_ids_for_rcdts": str(n) if n else ""})
        for rid in sorted(set(general[y]) - matched_rc):
            xw_rows.append({"year": str(y), "cps_school_id": "", "cps_name": "", "school_id": rid,
                            "status": "isbe_no_cps_match", "progress_year_used": "", "n_cps_ids_for_rcdts": ""})

    # schools
    def cps_fields(y, cid):
        d = {}
        v = lep[y].get(cid)
        if v:
            d.update(cps20_enroll_total=fmt(v["total"]), cps20_el_n=fmt(v["el"]), cps20_el_label=v["label"],
                     cps_network=v["network"], cps_governance=v["governance"])
        if y == 2024 and cid in budget:
            d["newcomer_n"] = fmt(budget[cid]["cps_budget_newcomer_adj"])
        if y == 2025 and cid in budget:
            d.update({k: fmt(val) for k, val in budget[cid].items()})
        for tag, date in (("sep30", f"{y - 1}-09-30"), ("mar31", f"{y}-03-31")):
            s = staff_by.get((cid, date))
            if s:
                d[f"cps_teacher_fte_{tag}"] = s["fte_teacher"]
                d[f"cps_teacher_fte_filled_{tag}"] = s["fte_teacher_filled"]
                d[f"cps_all_fte_{tag}"] = s["fte_all"]
        return d

    school_rows = []
    num_fields = [c for c in SCHOOL_COLS if c not in (
        "city", "school_id", "cps_school_id", "school_name", "year", "row_source", "school_type", "grades_served",
        "cps20_el_label", "cps_network", "cps_governance", "xwalk_status", "xwalk_source", "xwalk_shared",
        "suppressed_fields")]
    for y in YEARS:
        status, by_rc = xw[y]
        for rid, rec in sorted(general[y].items()):
            row = {c: "" for c in SCHOOL_COLS}
            row.update(city=CITY, school_id=rid, year=str(y), row_source="isbe", school_name=rec["school_name"],
                       school_type=rec["school_type"], grades_served=rec["grades_served"],
                       suppressed_fields=";".join(sorted(rec["_sup"])))
            for k in num_fields:
                if k in rec:
                    row[k] = fmt(rec[k])
            ids = by_rc.get(rid, [])
            if len(ids) == 1:
                cid = ids[0]
                _, _, py, _ = status[cid]
                row.update(cps_school_id=cid, xwalk_status="attached", xwalk_source=f"progress_{py}")
                row.update(cps_fields(y, cid))
            elif len(ids) > 1:
                row.update(xwalk_status="shared_rcdts", xwalk_shared=";".join(sorted(ids)))
            else:
                row.update(xwalk_status="no_cps_match")
            school_rows.append(row)
        for cid in sorted(cps_ids[y]):
            st, rc, py, n = status[cid]
            if st == "attached":
                continue
            row = {c: "" for c in SCHOOL_COLS}
            row.update(city=CITY, cps_school_id=cid, year=str(y), row_source="cps_only",
                       school_name=cps_names[y].get(cid, ""), xwalk_status=st,
                       xwalk_source=f"progress_{py}" if py else "", xwalk_shared=rc)
            row.update(cps_fields(y, cid))
            school_rows.append(row)
    school_rows.sort(key=lambda r: (int(r["year"]), r["school_id"] or "~", r["cps_school_id"]))

    # scores: fill the other identifier from the crosswalk
    for r in scores:
        y = int(r["year"])
        status, by_rc = xw[y]
        if r["school_id"] and not r["cps_school_id"]:
            ids = by_rc.get(r["school_id"], [])
            if len(ids) == 1:
                r["cps_school_id"] = ids[0]
        elif r["cps_school_id"] and not r["school_id"]:
            st, rc, py, n = status[r["cps_school_id"]]
            if st == "attached":
                r["school_id"] = rc
    scores.sort(key=lambda r: (int(r["year"]), r["school_id"] or "~", r["cps_school_id"], r["subject"], r["group"],
                               GRADE_ORDER[r["grade"]], r["source"], r["test_name"]))
    keys = Counter((r["year"], r["school_id"], r["cps_school_id"], r["subject"], r["group"], r["grade"], r["source"],
                    r["test_name"]) for r in scores)
    dups = [k for k, n in keys.items() if n > 1]
    if dups:
        raise ValueError(f"duplicate score keys, e.g. {dups[:3]}")
    xw_rows.sort(key=lambda r: (int(r["year"]), r["cps_school_id"] or "~", r["school_id"]))
    checks["isbe_vs_cps_grade_levels"] = agreement_isbe_cps(scores)

    # staff: attach the ISBE RCDTS where the school-year crosswalk attaches the CPS ID
    no_cps_row = Counter()
    for r in staff:
        y = int(r["school_year"])
        st = xw[y][0].get(r["cps_school_id"]) if y in xw else None
        if st is None:
            no_cps_row[r["school_year"]] += 1
        elif st[0] == "attached":
            r["school_id"] = st[1]
    checks["staff_rows_without_cps_school_in_year"] = dict(sorted(no_cps_row.items()))
    staff.sort(key=lambda r: (r["snapshot_date"], int(r["cps_school_id"]), r["dept_id"]))

    write_csv(OUT / "chicago_schools.csv", SCHOOL_COLS, school_rows)
    write_csv(OUT / "chicago_scores.csv", SCORE_COLS, scores)
    write_csv(OUT / "chicago_crosswalk.csv", XWALK_COLS, xw_rows)
    write_csv(OUT / "chicago_staff_quarterly.csv", STAFF_COLS, staff)

    by_year_src = defaultdict(Counter)
    sup_by = defaultdict(Counter)
    for r in scores:
        by_year_src[r["year"]][r["source"]] += 1
        if r["suppressed"] == "1":
            sup_by[r["year"]][r["source"]] += 1
    audit = {
        "inputs_sha256": dict(sorted(INPUTS.items())),
        "python_calamine": importlib.metadata.version("python-calamine"),
        "cps_note_rows": NOTES,
        "rows": {
            "chicago_schools.csv": {str(y): dict(sorted(Counter(r["row_source"] for r in school_rows
                                                                 if r["year"] == str(y)).items())) for y in YEARS},
            "chicago_scores.csv": {y: dict(sorted(c.items())) for y, c in sorted(by_year_src.items())},
            "chicago_crosswalk.csv": len(xw_rows),
            "chicago_staff_quarterly.csv": dict(sorted(Counter(r["snapshot_date"] for r in staff).items())),
        },
        "score_rows_flagged_suppressed": {y: dict(sorted(c.items())) for y, c in sorted(sup_by.items())},
        "parsed_cells_by_source_year": TALLY.report(),
        "checks": checks,
    }
    with open(OUT / "chicago_audit.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(audit, f, indent=1, sort_keys=True, ensure_ascii=False)
        f.write("\n")
    print(f"schools rows {len(school_rows)}, score rows {len(scores)}, crosswalk rows {len(xw_rows)}, "
          f"staff rows {len(staff)}")


if __name__ == "__main__":
    sys.exit(main())
