/** Executed numbers only. Each export names the account it belongs to. */

export const bands = ['0–17', '18–24', '25–34', '35–44', '45–54', '55–64', '65–74', '75+']

// Shared expanded ledger, income year 2024. Population and net $/person by age band.
// ledger_absolute_2026_09_17/derived/age_profiles.csv
export const mexican = {
  pop: [12123523.5152, 5023250.5947, 6301180.7419, 5693504.7306, 4921286.6263, 3671409.3847, 2050156.3178, 1112262.2413],
  rate: [-8597.9142, -2408.6524, 1224.3692, -2225.6609, -1602.0183, -2615.9796, -23333.7324, -27598.8521],
}
export const white = {
  pop: [31162353.9281, 13832325.9694, 21209374.6172, 22045949.116, 20431740.3528, 23960789.2598, 23016940.0355, 17394420.1185],
  rate: [72.8145, 6262.91, 10760.9272, 6626.3419, 9230.1219, 11278.2896, -22619.3664, -35225.4053],
}

// Category totals, $bn, same ledger, mexican observed total, shared allocation.
// age_normalizations_by_category.csv — own ages and white ages.
export const categories = [
  { label: 'Public medical', own: -128.03, white: -208.23 },
  { label: 'Social Security and other cash', own: -91.76, white: -161.97 },
  { label: 'Schools', own: -136.15, white: -105.22 },
  { label: 'Institutions', own: -19.07, white: -26.94 },
  { label: 'Rest of federal budget', own: -92.15, white: -99.61 },
  { label: 'Sales, excise, property tax', own: 88.46, white: 95.03 },
  { label: 'Corporate tax', own: 34.55, white: 39.25 },
  { label: 'State and local services', own: -148.96, white: -149.47 },
  { label: 'Income and payroll tax', own: 288.88, white: 289.23 },
  { label: 'Noncash aid', own: -13.08, white: -11.64 },
]

// September 19 ledger recut. Negative = shortfall of the union balance.
export const hulls = {
  practitioner: { lo: -290.5, hi: -190.1, mark: -217.3 },
  design: { lo: -496.2, hi: -76.1 },
  dial: 40.9,
  publicGoods: { lo: -502.1, hi: -401.8, mark: -429.0 },
}

// White-age gaps, $ per person. age_normalizations.csv
export const generations = {
  shared: {
    receipts: [-12149, -8395, -6984],
    spending: [4625, 953, 868],
    net: [-7525, -7443, -6116],
  },
  personal: {
    receipts: [-12239, -7257, -7104],
    spending: [4409, 459, 1086],
    net: [-7830, -6799, -6018],
  },
}

// Recent arrivals, ages 25–54, within five years. Less-than-high-school share.
export const schooling = [
  { year: 1980, window: '1975–80', lths: 82.5 },
  { year: 1990, window: '1985–90', lths: 66.4 },
  { year: 2000, window: '1995–2000', lths: 61.5 },
  { year: 2010, window: '2005–10', lths: 51.7 },
  { year: 2023, window: '2018–23', lths: 33.3 },
]

// Partial-account arrival windows, standardized person vs whites. Not the series above.
export const fiscalWindows = { older: [-5300, -4800], recent: -3978 }

export const incomeRatios = {
  years: [2008, 2009, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2021, 2022, 2023, 2024],
  breaks: [2010, 2020],
  perCapita: [0.5194, 0.5088, 0.5062, 0.5102, 0.5088, 0.5184, 0.5248, 0.5354, 0.5472, 0.5531, 0.5625, 0.5847, 0.5912, 0.5994, 0.6113],
  household: [0.7812, 0.7789, 0.7699, 0.7779, 0.7818, 0.7867, 0.7966, 0.8094, 0.8194, 0.8267, 0.8513, 0.8735, 0.8893, 0.9047, 0.9069],
  men: [0.6413, 0.6291, 0.6358, 0.6411, 0.6397, 0.6446, 0.6346, 0.6413, 0.6971, 0.7092, 0.7352, 0.7033, 0.7341, 0.7557, 0.7541],
}

// Shared all-age ledger vs local third-plus NH whites. Not the complete account.
export const places = [
  { name: 'Los Angeles', v: -17196, lo: -21144, hi: -13249, people: '4.50m' },
  { name: 'California', v: -12133, lo: -14068, hi: -10198, share: '32%' },
  { name: 'Chicago', v: -11838, people: '1.74m' },
  { name: 'Dallas–Fort Worth', v: -9823, people: '1.88m' },
  { name: 'Riverside–San Bernardino', v: -8621, people: '2.41m' },
  { name: 'Texas', v: -7479, lo: -9253, hi: -5705, share: '32%' },
  { name: 'Houston', v: -7493, people: '2.05m' },
  { name: 'Phoenix', v: -6721, people: '1.41m' },
  { name: 'National, age only', v: -5734, people: '40.9m', national: true },
]

// Mexico-born, ages 25–64, common ages, shared allocation, $ per person.
export const education = [
  { label: 'Below high school, vs natives below high school', v: 2263, lo: 751, hi: 3774 },
  { label: 'High school only, vs natives with high school only', v: -2286, lo: -3645, hi: -926 },
  { label: 'Below high school, vs natives of all schooling', v: -13502 },
]

// Earnings gap vs US-born non-Hispanic whites, employed ages 25–64. ACS 2023.
export const kitagawa = [
  { label: 'India-born', detail: 'Detailed occupations', mix: 24785, within: 22825, inter: 447, gap: 48056 },
  { label: 'US-born, Asian Indian ancestry', detail: 'IT vs not IT', mix: 2714, within: 63476, inter: -2167, gap: 64022 },
  { label: 'India-born, recent noncitizens', detail: 'Detailed occupations', mix: 26698, within: -3626, inter: -6925, gap: 16147 },
]

// Real national spending per resident, 2024 = 1. national_programme_index.csv
export const programmeYears = [2005, 2010, 2015, 2019, 2020, 2021, 2024]
export const programmes = [
  { name: 'Credits', color: '#8c2f16', v: [0.417, 0.969, 0.749, 0.855, 2.296, 4.359, 1] },
  { name: 'Medicaid', color: '#24384a', v: [0.584, 0.662, 0.781, 0.815, 0.858, 0.915, 1] },
  { name: 'Medicare', color: '#5e584e', v: [0.532, 0.715, 0.784, 0.89, 0.916, 0.936, 1] },
  { name: 'Schools', color: '#7c6232', v: [0.847, 0.911, 0.901, 0.93, 0.951, 0.976, 1] },
  { name: 'Police, courts', color: '#1d5a42', v: [0.9, 0.983, 0.949, 1.008, 1, 0.994, 1] },
]

// US-born Mexican-origin men 18–39 in institutions ÷ native NH white men.
export const custody = {
  years: [2010, 2019, 2023, 2024],
  ratio: [2.56, 1.91, 1.72, 1.94],
  reallocated: [2.6, 2.1, 2.11, 2.23],
}
