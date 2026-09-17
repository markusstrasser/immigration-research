# Source access status — September 17, 2026

## NLSY97: requested export acquired and verified

The operator's browser report identifies the export session as NLSY97 1997–2023, rounds 1–21. Filesystem inspection confirms `/Users/alien/Downloads/nlsy97_gen_crime.zip` exists (1,209,610 bytes; SHA-256 `d9e0d085042cb6034c16c2c3b6501a913b245fd78e1f10e21c441f74f975320d`). Its CSV, codebook and tagset are byte-identical to the corresponding members of `default.zip`; the archive CRC passes. Its 99 columns contain all 98 requested references. Generated control filenames account for some wrapper differences; this is an equivalent export, not another cohort. [SOURCE: local archives, `organize.py`, `completion_check.json`; session/vintage corroborated by operator-provided browser report.]

The browser reportedly logged HTTP503, but the actual downloaded file passes content and integrity checks. The transport status is not evidence of missing data. No additional NLS download is needed for the completed request. Publicly available additional roster variables may be extracted locally from the already-held full archive if a new derivation requires them. [SOURCE: verified local file; browser status is operator-reported.]

## ICPSR20862: respondent data gated by account membership

The operator supplied this exact browser delivery message:

> These data are supported by members of the ICPSR. You are attempting to download data from a non-member MyData account. You will find that all documentation files will be delivered to your device with the exception of the data files; these data files are free to individuals at ICPSR member institutions; non-members may purchase these data. If you believe that you are affiliated with a member institution, please verify using the list of ICPSR member institutions; after verification, please contact ICPSR user support.

This supplies the access explanation that was absent from the downloaded documentation. It is a source-grounded operator report of the live account response, not an independently repeated login check. Do not infer that a public-use disclosure category guarantees free access to every account. The browser report observes the gate on Dataset3; it predicts the same account-wide restriction for Dataset1 but does not establish a separate completed Dataset1 attempt. [SOURCE: operator-provided browser report, September17.]

Local ZIPs `(2)` and `(3)` contain the same ten member names and byte-identical documentation as the original ZIP; their ZIP hashes differ. The extracted `ICPSR_20862/` folder is likewise an exact copy of those ten files. No respondent file is present. The library retains one named full documentation copy and labels the seven-file Dataset3 subset separately. Originals remain untouched. [SOURCE: `organize.py`, generated library catalog.]

**Action:** stop unchanged-account download retries. Acquisition would require legitimate member-account access, separately authorized purchase, or a verified openly authorized copy from the investigators/institution. No purchase, account modification, external contact or restricted-data application is authorized or performed by this analysis. Alternative public-source checks, if any, are recorded in the analysis memo.

## ICPSR30302: documentation only

The already-held New York second-generation study remains documentation only; its catalog specifies a restricted-data agreement. No application or additional acquisition is undertaken. [SOURCE: packaged study catalog; existing dataset register.]
