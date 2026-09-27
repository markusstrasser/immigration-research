# Part-3 inputs, verbatim

## Eurostat (retrieved 2026-09-28 via the dissemination API; JSON-stat in `_cache/`)

- First-time asylum applicants: `migr_asyappctza?format=JSON&lang=EN&citizen=TOTAL&sex=T&applicant=FRST&age=TOTAL&age=Y_LT18&age=Y14-17&time=2015&time=2016&time=2017&unit=PER` -> `_cache/eurostat_asy_first_2015_2016.json`.
- Positive first-instance decisions: `migr_asydcfsta?format=JSON&lang=EN&citizen=TOTAL&sex=T&decision=POS&age=TOTAL&age=Y_LT18&time=2015&time=2016&time=2017&time=2018&unit=PER` -> `_cache/eurostat_asy_decisions_pos_2015_2018.json` (label: "First instance decisions on applications by type of decision, citizenship, age and sex - annual aggregated data"; POS = "Positive decision").
- Population on 1 January: `demo_pjan` (sex=T, age=TOTAL, time=2015) -> `_cache/eurostat_pop_2015.json`.

- Austria (AT): population 1 Jan 2015 = 8584926; first-time applicants, all ages 2015 = 85520, 2016 = 39905; under 18: 2015 = 31655, 2016 = 17370; positive first-instance decisions, all ages 2015/16/17 = 15045/30370/25205; under 18 = 5900/13250/13120
- Belgium (BE): population 1 Jan 2015 = 11237274; first-time applicants, all ages 2015 = 39065, 2016 = 14290; under 18: 2015 = 12120, 2016 = 4970; positive first-instance decisions, all ages 2015/16/17 = 10475/15050/12585; under 18 = 3095/3890/4235
- Czech Republic (CZ): population 1 Jan 2015 = 10538275; first-time applicants, all ages 2015 = 1240, 2016 = 1205; under 18: 2015 = 250, 2016 = 240; positive first-instance decisions, all ages 2015/16/17 = 460/435/145; under 18 = 155/150/60
- Denmark (DK): population 1 Jan 2015 = 5659715; first-time applicants, all ages 2015 = 20855, 2016 = 6070; under 18: 2015 = 6300, 2016 = 2395; positive first-instance decisions, all ages 2015/16/17 = 9995/7125/2365; under 18 = 1960/2470/905
- Estonia (EE): population 1 Jan 2015 = 1313271; first-time applicants, all ages 2015 = 225, 2016 = 150; under 18: 2015 = 70, 2016 = 60; positive first-instance decisions, all ages 2015/16/17 = 80/130/95; under 18 = 20/45/50
- Finland (FI): population 1 Jan 2015 = 5471753; first-time applicants, all ages 2015 = 32150, 2016 = 5295; under 18: 2015 = 7590, 2016 = 1710; positive first-instance decisions, all ages 2015/16/17 = 1680/7070/3430; under 18 = 330/2665/1150
- France (FR): population 1 Jan 2015 = 66458153; first-time applicants, all ages 2015 = 70570, 2016 = 76790; under 18: 2015 = 13590, 2016 = 15240; positive first-instance decisions, all ages 2015/16/17 = 20630/28755/32565; under 18 = 7840/10385/11210
- Germany (DE): population 1 Jan 2015 = 81197537; first-time applicants, all ages 2015 = 441900, 2016 = 722365; under 18: 2015 = 137480, 2016 = 261375; positive first-instance decisions, all ages 2015/16/17 = 140915/433910/261630; under 18 = 34400/155750/114360
- Greece (EL): population 1 Jan 2015 = 10818041; first-time applicants, all ages 2015 = 11370, 2016 = 49875; under 18: 2015 = 2420, 2016 = 19635; positive first-instance decisions, all ages 2015/16/17 = 4030/2715/10455; under 18 = 965/890/4290
- Hungary (HU): population 1 Jan 2015 = 9815858; first-time applicants, all ages 2015 = 174435, 2016 = 28215; under 18: 2015 = 45315, 2016 = 8455; positive first-instance decisions, all ages 2015/16/17 = 425/430/1290; under 18 = 65/105/645
- Iceland (IS): population 1 Jan 2015 = 329100; first-time applicants, all ages 2015 = 360, 2016 = 1100; under 18: 2015 = 85, 2016 = 270; positive first-instance decisions, all ages 2015/16/17 = 50/95/70; under 18 = 10/25/20
- Ireland (IE): population 1 Jan 2015 = 4677627; first-time applicants, all ages 2015 = 3270, 2016 = 2235; under 18: 2015 = 385, 2016 = 580; positive first-instance decisions, all ages 2015/16/17 = 330/485/760; under 18 = 50/135/280
- Italy (IT): population 1 Jan 2015 = 60295497; first-time applicants, all ages 2015 = 82790, 2016 = 121185; under 18: 2015 = 7175, 2016 = 11080; positive first-instance decisions, all ages 2015/16/17 = 29615/35405/31795; under 18 = 5265/6310/7455
- Latvia (LV): population 1 Jan 2015 = 1986096; first-time applicants, all ages 2015 = 330, 2016 = 345; under 18: 2015 = 85, 2016 = 120; positive first-instance decisions, all ages 2015/16/17 = 20/135/265; under 18 = 5/55/135
- Lithuania (LT): population 1 Jan 2015 = 2926644; first-time applicants, all ages 2015 = 275, 2016 = 415; under 18: 2015 = 60, 2016 = 160; positive first-instance decisions, all ages 2015/16/17 = 85/195/285; under 18 = 20/90/125
- Netherlands (NL): population 1 Jan 2015 = 16900726; first-time applicants, all ages 2015 = 43035, 2016 = 19285; under 18: 2015 = 10205, 2016 = 5875; positive first-instance decisions, all ages 2015/16/17 = 16450/20810/7810; under 18 = 3605/5310/2510
- Norway (NO): population 1 Jan 2015 = 5165802; first-time applicants, all ages 2015 = 30505, 2016 = 3275; under 18: 2015 = 10300, 2016 = 1230; positive first-instance decisions, all ages 2015/16/17 = 6250/12780/4770; under 18 = 1610/4165/1760
- Poland (PL): population 1 Jan 2015 = 38005614; first-time applicants, all ages 2015 = 10255, 2016 = 9785; under 18: 2015 = 4780, 2016 = 4810; positive first-instance decisions, all ages 2015/16/17 = 640/295/510; under 18 = 245/130/250
- Portugal (PT): population 1 Jan 2015 = 10395121; first-time applicants, all ages 2015 = 870, 2016 = 710; under 18: 2015 = 145, 2016 = 140; positive first-instance decisions, all ages 2015/16/17 = 195/320/500; under 18 = 35/65/150
- Slovak Republic (SK): population 1 Jan 2015 = 5421349; first-time applicants, all ages 2015 = 270, 2016 = 100; under 18: 2015 = 90, 2016 = 30; positive first-instance decisions, all ages 2015/16/17 = 80/210/60; under 18 = 10/80/25
- Slovenia (SI): population 1 Jan 2015 = 2062874; first-time applicants, all ages 2015 = 260, 2016 = 1265; under 18: 2015 = 80, 2016 = 420; positive first-instance decisions, all ages 2015/16/17 = 45/170/150; under 18 = 15/70/55
- Spain (ES): population 1 Jan 2015 = 46425722; first-time applicants, all ages 2015 = 14610, 2016 = 15570; under 18: 2015 = 3720, 2016 = 3710; positive first-instance decisions, all ages 2015/16/17 = 1020/6855/4090; under 18 = 400/2510/1785
- Sweden math: exclusion 5.706 % (2015), 11.086 % (2018); SD 90.07 (2015), 90.69 (2018) [Table I.B1.5.10]; bound -6.30 points
- Sweden reading: exclusion 5.706 % (2015), 11.086 % (2018); SD 101.78 (2015), 107.53 (2018) [Table I.B1.5.11]; bound -7.84 points
- Sweden science: exclusion 5.706 % (2015), 11.086 % (2018); SD 102.48 (2015), 97.97 (2018) [Table I.B1.5.12]; bound -6.43 points
- Sweden (SE): population 1 Jan 2015 = 9747355; first-time applicants, all ages 2015 = 156195, 2016 = 22385; under 18: 2015 = 69155, 2016 = 9400; positive first-instance decisions, all ages 2015/16/17 = 32360/66590/26510; under 18 = 9275/23630/12525
- Switzerland (CH): population 1 Jan 2015 = 8237666; first-time applicants, all ages 2015 = 38120, 2016 = 25875; under 18: 2015 = 11155, 2016 = 8940; positive first-instance decisions, all ages 2015/16/17 = 13295/12660/14005; under 18 = 5295/6085/6465
- United Kingdom (UK): population 1 Jan 2015 = 64853393; first-time applicants, all ages 2015 = 39970, 2016 = 39355; under 18: 2015 = 8125, 2016 = 9330; positive first-instance decisions, all ages 2015/16/17 = 13955/9935/8570; under 18 = 3170/2630/2785
- Bulgaria (BG): population 1 Jan 2015 = 7029690; first-time applicants, all ages 2015 = 20160, 2016 = 18990; under 18: 2015 = 5470, 2016 = 6530; positive first-instance decisions, all ages 2015/16/17 = 5595/1350/1695; under 18 = 2095/530/730
- Croatia (HR): population 1 Jan 2015 = 4180915; first-time applicants, all ages 2015 = 145, 2016 = 2150; under 18: 2015 = 20, 2016 = 460; positive first-instance decisions, all ages 2015/16/17 = 40/100/150; under 18 = 5/35/40
- Cyprus (CY): population 1 Jan 2015 = 860846; first-time applicants, all ages 2015 = 2105, 2016 = 2840; under 18: 2015 = 510, 2016 = 675; positive first-instance decisions, all ages 2015/16/17 = 1585/1300/1245; under 18 = 410/440/375
- Malta (MT): population 1 Jan 2015 = 438805; first-time applicants, all ages 2015 = 1695, 2016 = 1735; under 18: 2015 = 375, 2016 = 420; positive first-instance decisions, all ages 2015/16/17 = 1250/1190/760; under 18 = 285/380/295
- Montenegro (ME): population 1 Jan 2015 = 622099; first-time applicants, all ages 2015 = None, 2016 = None; under 18: 2015 = None, 2016 = None; positive first-instance decisions, all ages 2015/16/17 = None/None/None; under 18 = None/None/None
- Romania (RO): population 1 Jan 2015 = 19870647; first-time applicants, all ages 2015 = 1225, 2016 = 1855; under 18: 2015 = 295, 2016 = 525; positive first-instance decisions, all ages 2015/16/17 = 480/805/1245; under 18 = 155/255/435

## PISA natives' 2015 means: 2015 Vol I Tables I.7.15a/b/c vs the 2022 Vol I trend columns

- 172 country-subject pairs matched; max absolute difference 0.014 points (Romania, reading: 434.148 vs 434.134).
- Germany (2015 Vol I, `statlink_888933433226.xlsx`): "Mathematics performance in PISA 2015 / Non-immigrant students / Mean score" 519.434; reading 525.612; science 527.198.

## Test mode

- PISA 2015 Vol I, p. text line 1570 of `_cache/pisa2015_vol1.txt`: "The paper-based form was used in 15 countries/economies including Albania, Algeria, Argentina, Georgia, Indonesia, Jordan, Kazakhstan, Kosovo, Lebanon, the Former Yugoslav Republic of Macedonia, Malta, Moldova, Romania, Trinidad and Tobago, and Viet Nam, as well as in Puerto Rico".
- PISA 2022 Vol I (`_cache/pisa2022_vol1.txt` line 7971): "Argentina, Jordan, Moldova, North Macedonia, Romania, Saudi Arabia and Ukraine switched from paper to computer assessment in 2022."
- PISA 2015 Vol I (line 13714): "It was not possible to rule out small and moderate effects of the mode of delivery on the mean performance of countries/economies."
- [INFERENCE] Paper in 2015 and computer in 2018: Albania, Georgia, Indonesia, Kazakhstan, Kosovo, Malta. Most other countries switched from paper (2012) to computer (2015), so the switch sits in the 2012->2015 pre-trend and the 2015 level.

PISA natives' 2012/2018 means (2022 Vol I Tables I.B1.7.18/7.22/7.26), first-generation and immigrant shares (I.B1.7.2) and gaps are listed per country in `derived/national_channel_data.csv`.
