**Verdict:** No source-classification failure may silently become a zero purchaser response.

2026-10-15: The first integration failed on BEA purchaser `HS` (housing). Its
positive customs allocation has no item-6 wage support. It is now explicitly
`unkeyed_intermediate`; bounds/carry arms name its missing response. `assemble.py`
rejects any other unclassified purchaser key before arithmetic. Regression:
`test_item.py::test_unmapped_housing_cannot_enter_industry_key_as_zero` and
`test_business_bases.py` source mapping/missing-response checks. [CALCULATION]

2026-10-15: The first complete byte rerun compared 39/39 identical files but
exited3: its static script-coverage gate does not infer test filenames from a
pytest directory argument. Reproduction now names all four test files explicitly;
no `--allow-unrun` exemption is used. The required regression is the complete
rerun exiting0, including its script-coverage check. [CALCULATION]

2026-10-15, round6 WA06: the sales crosscheck divided item6's business-only
OTP target by the whole OTP line. It now loads item6's declared business base,
checks the residential/mining/base partition against the case national line,
and retains the old ratio as `whole_line_share_superseded`. Mining purchase
fractions remain labelled assumptions with zero mining response. Regression:
`test_item.py::test_sales_proxy_uses_item6_business_base_and_preserves_old_diagnostic`,
`test_mining_assumptions_keep_customs_fixed_and_response_zero` and
`test_round6_unchanged_household_customs_and_superseded_diagnostic`.
`evaluate.cjs` also blocks a method-averaged household-joint endpoint change
beyond1e-9bn in either set, or any arm moving endpoints from16/11.
[CODE / CALCULATION]

2026-10-15, round6 gate correction: the first new guard incorrectly applied
the published method-averaged household delta to each method separately.
The two method deltas are0.263801411 and0.262828365bn; their average is
0.263314888bn. The guard now compares the method-averaged endpoint in both
sets. All32 specifications per method remain evaluated. Regression:
`test_round6_unchanged_household_customs_and_superseded_diagnostic`.
[CODE / CALCULATION]
