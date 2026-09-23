"""Arithmetic behind RESULT.md (ITIN credits and state aid to undocumented students).

Every input is copied from a cached primary document; the source is named beside it.
Run: uv run --no-project python3 infra/immigration-fiscal/itin_credits_student_aid_2026_09_23/calc.py
"""

# NTA 2024 ARC, research report 3, Fig. 5.3.3 (IRS CDW IRTF + IRMF): returns with >=1 ITIN
nta = {  # tax year: (income tax before credits, after credits, credits, total tax paid, net refund)
    2017: (15_883_626_037, 13_397_477_360, 2_486_148_677, 15_283_349_533, -6_197_598_770),
    2018: (16_341_035_385, 12_384_659_498, 3_956_375_887, 14_432_852_937, -4_801_898_654),
    2019: (15_969_896_165, 12_138_382_932, 3_831_513_233, 14_136_907_317, -4_590_293_213),
    2020: (15_889_175_404, 12_533_665_484, 3_355_509_920, 14_832_013_938, -5_024_559_700),
    2021: (19_019_736_300, 17_313_039_371, 1_706_696_929, 20_154_593_652, -5_535_947_851),
    2022: (18_205_798_218, 14_511_054_710, 3_694_743_508, 17_308_825_668, -3_313_974_360),
    2023: (16_470_905_155, 13_162_654_179, 3_308_250_976, 15_695_272_870, -3_027_032_853),
}
print("NTA Fig. 5.3.3 identity check (before - after == credits); other taxes = total tax paid - after")
for ty, (b, a, c, paid, net) in nta.items():
    print(f"  TY{ty}: before-after={b - a:>14,} credits={c:>14,} match={b - a == c}  "
          f"other taxes={paid - a:>14,}  credits/before={c / b:.3f}")

returns_2022 = 3_791_421  # NTA Fig. 5.3.2
states = {"CA": 866_378, "TX": 446_522, "NY": 254_779, "FL": 185_119, "NJ": 172_349,
          "IL": 170_218, "GA": 142_125, "MD": 131_511, "NC": 111_982, "VA": 109_434,
          "WA": 88_816, "CO": 72_928, "MA": 65_244, "AZ": 54_824, "NV": 50_185}  # Fig. 5.3.6
abroad = [56_700, 19_239, 15_085, 12_687, 5_840, 5_149, 3_288, 3_090, 2_512, 2_284,
          2_250, 2_134, 1_996, 1_833, 1_618]  # Fig. 5.3.8, top 15 foreign countries
top15 = sum(states.values())
print(f"\nTop-15 states: {top15:,} = {top15 / returns_2022:.1%} of {returns_2022:,} ITIN returns")
for s in ("CA", "TX", "IL", "CO", "MD", "WA"):
    print(f"  {s}: {states[s] / returns_2022:.1%}")
print(f"Top-15 foreign countries: {sum(abroad):,} = {sum(abroad) / returns_2022:.1%}")

# ACTC order of magnitude [INFERENCE]: ~2M SSN children on returns without a taxpayer SSN
# (JCT via Tax Policy Center, House OBBBA text); TY2022 refundable cap $1,500 per child.
kids = 2_000_000
for per_child in (1_000, 1_250, 1_500):
    print(f"ACTC if {per_child:,}/child: ${kids * per_child / 1e9:.1f}bn")
# Refundable share for a median ITIN family (AGI $31,033, 2 SSN children, TY2022 law)
for label, std_ded in (("MFJ", 25_900), ("HOH", 19_400)):
    taxable = 31_033 - std_ded
    tax = 0.10 * min(taxable, 20_550 if label == "MFJ" else 14_650) + 0.12 * max(
        0, taxable - (20_550 if label == "MFJ" else 14_650))
    nonref = min(tax, 4_000)
    actc = min(3_000, 0.15 * (31_033 - 2_500), 4_000 - nonref)
    print(f"  median {label}: tax {tax:,.0f}, nonrefundable CTC {nonref:,.0f}, ACTC {actc:,.0f}, "
          f"refundable share {actc / (actc + nonref):.0%}")

# Washington WFTC (DOR 2025 report Tables 2 and 4; ITIN share of applications from DOR pages)
wftc = {2022: 133_426_107, 2023: 142_776_394, 2024: 205_589_501}
print("\nWFTC ITIN dollars if dollar share = application share [INFERENCE]")
for ty, share in ((2022, 0.10), (2022, 0.09), (2024, 0.06), (2024, 0.044)):
    print(f"  TY{ty} x {share:.1%}: ${wftc[ty] * share / 1e6:.1f}m")

# Maryland EITC, ITIN tax units (Urban Institute 2025, Table 5, Comptroller data)
md = {2021: (94_601, 45_851), 2022: (93_236, 41_794), 2023: (77_616, 30_556)}
print("\nMaryland ITIN EITC claimants = eligible - non-claimers")
for ty, (elig, miss) in md.items():
    print(f"  TY{ty}: {elig - miss:,} claimed; x $1,100 avg = ${(elig - miss) * 1_100 / 1e6:.0f}m")

# California Cal Grant: 2024-25 all filers (CSAC district report) and CADAA offers (CSAC SB1644)
offered, paid, dollars = 696_333, 453_482, 2_495_572_964
per_paid = dollars / paid
print(f"\nCal Grant 2024-25: paid/offered {paid / offered:.3f}; ${per_paid:,.0f} per paid recipient")
for yr, cadaa in (("2024-25", 15_606), ("2025-26", 16_844)):
    est_paid = cadaa * paid / offered
    print(f"  CADAA {yr}: {cadaa:,} offered -> ~{est_paid:,.0f} paid -> ~${est_paid * per_paid / 1e6:.0f}m")

# Washington College Grant 2023-24 (WSAC by-institution report p.2); WASFA recipients (news)
wcg_dollars, wcg_n, wasfa_recip = 468_247_896, 97_269, 3_067
print(f"\nWA Grant avg ${wcg_dollars / wcg_n:,.0f}; WASFA recipients x avg = "
      f"${wasfa_recip * wcg_dollars / wcg_n / 1e6:.1f}m ({wasfa_recip / wcg_n:.1%} of recipients)")

# Texas affidavit students FY2017 (THECB overview pp.3-5)
print(f"\nTexas FY2017: GR state grants per award ${12.32e6 / 11_285:,.0f}; "
      f"tuition+fees paid per affidavit student ${72.8e6 / 25_930:,.0f}")

# Minnesota Dream Act State Grants (OHE FY2025 Table 5; FY2024 Table 6; 2022-23 summary)
print(f"MN 2022-23 dollars ~ 411 x $6,715 = ${411 * 6_715 / 1e6:.2f}m")

# Student-aid total where a number exists, latest year [INFERENCE for CA and WA]
parts = {"CA Cal Grant (est.)": 56e6, "CA Dream Act Service Incentive Grant": 7.5e6,
         "WA WA Grant via WASFA (est.)": 14.8e6, "MN State Grant": 4.93e6}
print(f"Recurring student grants with a figure, excluding TX (ended 2025), NJ (2018-19), IL, NY: "
      f"${sum(parts.values()) / 1e6:.0f}m")
