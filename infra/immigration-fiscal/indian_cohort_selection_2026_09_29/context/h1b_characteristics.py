"""USCIS 'Characteristics of H-1B Specialty Occupation Workers' (annual reports to Congress), FY2003-FY2025.

Values hand-transcribed from pdftotext -layout (text-layer PDFs) or tesseract OCR (FY2006-FY2009 and
FY2015-FY2016 reports are image-only); each row carries the report file and the quoted source line.
Education = % of approved petitions with education known (FY2022-FY2024 carry large 'unknown' shares:
shares among known are computed from the Table 6 counts; see notes).
"""
import csv, pathlib
LANE = pathlib.Path(__file__).resolve().parents[1]
# fy, india_all_n, india_all_pct, india_initial_n, india_initial_pct, report, evidence
INDIA = [
 (2003, 79166, 36.5, 29269, 27.8, "fy04", "India 79,166 123,567 29,269 60,062 ... / India 36.5 43.0 27.8 46.0 ..."),
 (2004, 123567, 43.0, 60062, 46.0, "fy04", "India 79,166 123,567 29,269 60,062 49,897 63,505 / India 36.5 43.0 27.8 46.0 44.6 40.5"),
 (2005, 118520, 44.4, 57349, 49.0, "fy05", "India 123,567 118,520 60,062 57,349 63,505 61,171 / India 43.0 44.4 46.0 49.0 40.5 40.7"),
 (2006, 135329, 49.9, 59612, 54.4, "fy07(OCR)", "India 135,329 147,559 59,612 66,504 75,717 81,055 / India 49.9 52.4 54.4 55.4 46.9 50.2"),
 (2007, 147559, 52.4, 66504, 55.4, "fy07(OCR)", "same lines as FY2006 (FY2006, FY2007 columns)"),
 (2008, 149629, 54.2, 61739, 56.5, "fy09(OCR)", "India 149,629 103,059 61,739 33,961 87,890 69,098 / India 54.2 48.1 56.5 39.4 52.7 54.0"),
 (2009, 103059, 48.1, 33961, 39.4, "fy09(OCR)", "same lines as FY2008"),
 (2010, 102911, 53.3, 34617, 45.2, "fy11", "India 102,911 156,317 34,617 55,972 68,294 100,345 / India 53.3 58.0 45.2 52.6 58.7 61.5"),
 (2011, 156317, 58.0, 55972, 52.6, "fy12", "India 156,317 168,367 55,972 86,477 100,345 81,890 / India 58.0 64.1 52.6 63.2 61.5 65.2"),
 (2012, 168367, 64.1, 86477, 63.2, "fy13", "India 168,367 187,270 86,477 81,992 81,890 105,278 / India 64.1 65.3 63.2 63.9 65.2 66.4"),
 (2013, 187270, 65.3, 81992, 63.9, "fy14", "India 187,270 220,286 81,992 82,263 105,278 138,023 / India 65.3 69.7 63.9 66.2 66.4 72.1"),
 (2014, 220286, 69.7, 82263, 66.2, "fy14", "same lines as FY2013"),
 (2015, 195247, 70.9, 71263, 62.7, "fy15(OCR)", "India 220,286 195,247 82,263 71,263 138,023 123,984 / India 69.7 70.9 66.2 62.7 72.1 76.7"),
 (2016, 256226, 74.2, 70737, 61.8, "fy17", "India 256,226 276,423 70,737 67,815 185,489 208,608 / India 74.2 75.6 61.8 62.7 80.4 81.0"),
 (2017, 276423, 75.6, 67815, 62.7, "fy18", "India 243,994 276,423 51,353 67,815 192,641 208,608 (FY2018, FY2017 cols) / India 73.4 75.6 54.9 62.7 80.7 81.0"),
 (2018, 243994, 73.4, 51353, 54.9, "fy19", "India 278,491 243,994 79,423 51,353 199,068 192,641 (FY2019, FY2018) / India 71.7 73.4 57.2 54.9 79.8 80.7"),
 (2019, 278491, 71.7, 79423, 57.2, "fy19", "same lines as FY2018"),
 (2020, 319494, 74.9, 73717, 60.0, "fy20", "Table 4a India ... 319,494 74.9 / Table 4b India ... 73,717 60.0"),
 (2021, 301616, 74.1, 75858, 61.5, "fy21", "Table 4a India ... 301,616 74.1 / Table 4b India ... 75,858 61.5"),
 (2022, 320791, 72.6, 77673, 58.7, "fy22", "Table 4a India ... 320,791 72.6 / Table 4b India ... 77,673 58.7"),
 (2023, 279386, 72.3, 68825, 57.9, "fy23", "Table 4a India ... 279,386 72.3 / Table 4b India ... 68,825 57.9"),
 (2024, 283755, 71.0, 80449, 57.0, "fy24", "Table 4a India ... 283,755 71 / Table 4b India ... 80,449 57 (Figure: 283,397 71.0)"),
 (2025, 284106, 69.9, 57747, 50.3, "fy25", "INDIA 284,106 69.9 / INDIA 57,747 50.3"),
]
# fy, bachelor%, master%, doctorate%, professional%, basis, report, evidence  (all approved petitions)
EDU = [  # from multi-year 'Percent of H-1B Petitions Approved by Level of Education' tables unless noted
 (2002, 50, 30, 12, 5, "fy05 Table 6 FY2002-2005", "Bachelor's 50 50 49 45 | Master's 30 31 34 37 | Doctorate 12 12 11 5 | Professional 5 6 5 12"),
 (2003, 50, 31, 12, 6, "fy05 Table 6", "same"),
 (2004, 49, 34, 11, 5, "fy05 Table 6", "same"),
 (2005, 45, 37, 5, 12, "fy05 Table 6", "same (doctorate/professional as printed; fy05 bullet and fy06 text differ -> possible swap)"),
 (2006, 45, 39, 11, 5, "fy06(OCR) highlights", "Forty-five percent ... bachelor's degree. Thirty-nine percent ... master's degree, eleven percent had a doctorate, and five percent had a professional degree."),
 (2007, 44, 40, 10, 5, "fy07(OCR) highlights", "Forty-four percent ... bachelor's degree, 40 percent had a master's degree, 10 percent had a doctorate, and 5"),
 (2008, 43, 41, 11, 5, "fy08(OCR) highlights", "Forty-three percent ... bachelor's degree, 41 percent had a master's degree, 11 percent had a doctorate, and 5 percent"),
 (2009, 41, 40, 13, 6, "fy12 Table 6 FY2009-2012", "Bachelor's 41 42 41 46 | Master's 40 39 42 41 | Doctorate 13 12 11 8 | Professional 6 6 5 4"),
 (2010, 42, 39, 12, 6, "fy12 Table 6", "same"),
 (2011, 41, 42, 11, 5, "fy12 Table 6", "same"),
 (2012, 46, 41, 8, 4, "fy12 Table 6", "same"),
 (2013, 45, 41, 9, 5, "fy14 Table 6 FY2011-2014", "Bachelor's 41 46 45 45 | Master's 42 41 41 43 | Doctorate 11 8 9 8 | Professional 5 4 3 4"),
 (2014, 45, 43, 8, 4, "fy17 Table 6 FY2014-2017", "Bachelor's 45 45 44 45 | Master's 43 44 45 44 | Doctorate 8 7 7 7 | Professional 4 3 3 3"),
 (2015, 45, 44, 7, 3, "fy17 Table 6", "same"),
 (2016, 44, 45, 7, 3, "fy19 Table 6 FY2016-2019", "Bachelor's 44 45 37 36 | Master's 45 44 52 54 | Doctorate 7 7 7 8 | Professional 3 3 3 3"),
 (2017, 45, 44, 7, 3, "fy19 Table 6", "same"),
 (2018, 37, 52, 7, 3, "fy19 Table 6", "same"),
 (2019, 36, 54, 8, 3, "fy19 Table 6", "same"),
 (2020, 35.7, 54.2, 7.0, 3.0, "fy20 text", "54.2 percent ... master's degree, 35.7 percent a bachelor's degree, 7 percent a doctorate, and 3 percent a professional degree"),
 (2021, 33.7, 56.6, 6.8, 2.9, "fy21 text", "56.6 percent ... master's degree, 33.7 percent had a bachelor's degree, 6.8 percent had a doctorate, and 2.9 percent"),
 (2022, 43.1, 42.3, 10.3, 4.2, "fy22 Table 6 counts, among known", "Bachelor's 140,213 | Master's 137,614 | Doctorate 33,568 | Professional 13,582 | Unknown 116,751 of 442,043 (26%)"),
 (2023, 50.1, 32.8, 11.8, 5.2, "fy23 Table 6 counts, among known", "Bachelor's 131,022 | Master's 85,900 | Doctorate 30,759 | Professional 13,608 | Unknown 124,736 of 386,318 (32%)"),
 (2024, 36.5, 50.8, 8.9, 3.8, "fy24 Table 6 counts, among known", "Bachelor's 130,995 | Master's 182,227 | Doctorate 31,879 | Professional 13,561 | Unknown 40,349 (10.1%)"),
 (2025, 30.5, 57.5, 8.1, 3.7, "fy25 Appendix Table 2 (unknown <1%)", "Bachelor's 123,824 30.5 | Master's 233,779 57.5 | Doctorate 33,090 8.1 | Professional 14,934 3.7"),
]
MED = [  # median annual compensation, all approved beneficiaries, nominal USD
 (2004, 53000, "fy04 Table 10", "Total 282,404 42,000 53,000 72,000"),
 (2005, 55000, "fy05 highlights", "The median salary rose slightly from $53,000 in fiscal year 2004 to $55,000 in fiscal year 2005."),
 (2006, 60000, "fy06(OCR)", "The median salary increased from $55,000 in Fiscal Year 2005 to $60,000 in Fiscal Year 2006,"),
 (2007, 60000, "fy07(OCR)", "The median salary remained at $60,000 in Fiscal Year 2007"),
 (2008, 60000, "fy08(OCR)", "The median salary remained at $60,000 in Fiscal Year 2008"),
 (2009, 64000, "fy09(OCR)", "increased to $64,000 in Fiscal Year 2009, $4,000 more than in Fiscal Year 2008."),
 (2010, 68000, "fy11 highlights (derived)", "increased to $70,000 in FY 2011, $2,000 more than in FY 2010."),
 (2011, 70000, "fy11 Table", "Total 267,487 57,000 70,000 78,000 90,000"),
 (2012, 70000, "fy12", "median annual compensation ... during FY 2012 was $70,000."),
 (2013, 72000, "fy13 Table", "Total 284,884 60,000 72,000 82,000 95,000"),
 (2014, 75000, "fy14 Table", "Total 314,078 62,000 75,000 84,000 98,000"),
 (2015, 79000, "fy15(OCR)", "median annual compensation ... during FY 2015 was $79,000. The median annual compensation was $75,000 in FY 2014."),
 (2016, 82000, "fy17", "The median annual compensation was $82,000 in FY 2016."),
 (2017, 85000, "fy17 Table", "Total 365,672 69,000 85,000 94,000 110,000"),
 (2018, 95000, "fy19", "The median annual compensation was $95,000 in FY 2018."),
 (2019, 98000, "fy19", "median annual compensation ... during FY 2019 was $98,000."),
 (2020, 101000, "fy20", "Median annual compensation for all approved H-1B beneficiaries in FY 2020 was $101,000."),
 (2021, 108000, "fy21", "... in FY 2021 was $108,000."),
 (2022, 118000, "fy22", "... in FY 2022 was $118,000."),
 (2023, 118000, "fy23", "... in FY 2023 was $118,000."),
 (2024, 120000, "fy24", "... in FY 2024 was $120,000."),
 (2025, 133000, "fy25", "... in FY 2025 was $133,000."),
]
out = LANE / "context/h1b_characteristics_fy2003_2025.csv"
ed = {r[0]: r for r in EDU}; md = {r[0]: r for r in MED}; ind = {r[0]: r for r in INDIA}
with open(out, "w", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["fiscal_year", "india_approved_n", "india_approved_pct", "india_initial_n", "india_initial_pct",
                "edu_bachelor_pct", "edu_master_pct", "edu_doctorate_pct", "edu_professional_pct", "edu_source",
                "median_comp_usd_nominal", "median_source", "india_source", "india_evidence", "edu_evidence", "median_evidence"])
    for fy in sorted(set(ed) | set(md) | set(ind)):
        i = ind.get(fy, (fy, "", "", "", "", "", "")); e = ed.get(fy, (fy, "", "", "", "", "", "")); m = md.get(fy, (fy, "", "", ""))
        w.writerow([fy, i[1], i[2], i[3], i[4], e[1], e[2], e[3], e[4], e[5], m[1], m[2], i[5], i[6], e[6], m[3]])
print("wrote", out)
