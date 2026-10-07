**Verdict:** Yes, 2024 flatters the group. Taking the group's own cyclical employment shortfall, a cycle-average year costs others about **$17–27bn more** than 2024 (averaged over 2005–2024) and **$23–35bn more** (2007–2019). The part above the nation's own cycle swing (the group's excess cyclicality) is **$4–7bn** and **$6–9bn**. Both clear the $3bn bar. These figures sit beside the account and do not change the headline: they are a first-order model with assumed fiscal sensitivities. [CALCULATION: `cycle.py` → `derived/result.json`] [INFERENCE]

model: claude-opus-5-5

## Is the cycle already in the back-cast?

No. The back-cast holds the group's **2024 relative position** and applies it to measured national budgets and the measured population for each year. Its `income` rule scales by relative per-capita income: 0.519 in 2008, 0.509 in 2013, 0.563 in 2019 and 0.611 in 2024. That series is dominated by trend, it does not model employment, earnings or take-up year by year, and its 2010 and 2020 values are missing. Its year-to-year changes therefore cannot isolate the cycle, so this lane uses the first-order route. [SOURCE: `infra/immigration-fiscal/historical_backcast_2026_09_20/README.md` lines 3–6; `research/immigration-historical-backcast-2026-09-20.md`] [INFERENCE]

## Where 2024 sits in the cycle

- Output gap (BEA GDPC1 against CBO GDPPOT, current FRED vintage, annual mean of quarters): **+1.49% in 2024**, against a mean of −0.78% over 2005–2024 and −1.45% over 2007–2019. [DATA: `derived/annual.csv`] [SOURCE: https://fred.stlouisfed.org/series/GDPPOT, https://fred.stlouisfed.org/series/GDPC1]
- Unemployment in 2024: Hispanic 5.07%, total 4.02%, a gap of 1.05pp. The gap averaged 1.44pp over 2005–2024 and 1.60pp over 2007–2019. [DATA: BLS CPS LNU04000009, LNU04000000 (FRED UNRATENSA), monthly NSA averaged per year]
- Fitting the employment-population ratio on a constant, a linear trend and the output gap (2005–2024, n=20) gives a slope of **1.07pp per output-gap point for Hispanics** and 0.76 for the total. [CALCULATION: `fits_const_trend_gap`; LNU02300009, LNU02300000]

## From employment to dollars

Average-year minus 2024 output gap × slope gives the Hispanic EPOP shortfall: −2.43pp (2005–2024) and −3.15pp (2007–2019). Relative to 2024's EPOP of 63.8%, that is −3.8% and −4.9% of jobs. The excess shortfall subtracts the national shortfall, scaled to the Hispanic EPOP level: −0.60pp and −0.78pp, or −0.9% and −1.2% of jobs.

The cost combines lost receipts and added transfers:
- lost receipts = job fraction × $488.5bn of group receipts × an employment-linked share of 0.75–0.90 [DATA: group receipts after the data corrections, back-cast memo table note] [ASSUMPTION: share];
- added transfers = job fraction × 18.0M employed members × $5k–15k per lost job (UI, SNAP, Medicaid) [ASSUMPTION: both inputs; 18.0M ≈ 39.7M × 0.70 adults × 0.65 EPOP].

| Window | Measure | ΔEPOP, pp | Cost vs 2024, $bn |
|---|---|---:|---:|
| 2005–2024 | own (absolute) | −2.43 | 17.4–27.0 |
| 2005–2024 | excess over the nation | −0.60 | 4.3–6.7 |
| 2007–2019 | own (absolute) | −3.15 | 22.5–35.0 |
| 2007–2019 | excess over the nation | −0.78 | 5.5–8.6 |

The comparison depends on framing. The account's net cost to others is the group's own net position, so the absolute row is the first-order answer for "what would a normal year cost." The excess row is the part peculiar to this group, because every group's net worsens in a weak year. [FRAMING-SENSITIVE]

## Limits

- The series cover all Hispanics, not people of Mexican origin (about 60% of Hispanics) or the 42.75M lineage. [INFERENCE]
- The fiscal sensitivities are assumed, not measured: the receipts share, transfers per job and employed count. Earnings per worker and hours also fall in slack years, so the receipts loss is probably understated. [INFERENCE]
- The fit includes 2020 and uses the current CBO potential vintage. A different vintage moves 2024's gap, and with it every row roughly in proportion. [INFERENCE]
- National spending per capita also moves with the cycle. The account keys services to national budgets, but this lane does not reprice them. [INFERENCE]
- None of this enters the main case. It belongs beside the $390–461bn account as a cycle-position caveat.

## Reproduce

```sh
L=infra/immigration-fiscal/cycle_average_2026_10_07
for s in LNU04000009 UNRATENSA LNU02300009 LNU02300000 GDPPOT GDPC1; do
  curl -sf --retry 3 -o $L/inputs/$s.csv "https://fred.stlouisfed.org/graph/fredgraph.csv?id=$s"; done
OPENBLAS_NUM_THREADS=1 uv run --no-project python3 $L/cycle.py
uv run --no-project python3 scripts/rerun_lane.py $L "uv run --no-project python3 {lane}/cycle.py"
```

The rerun gave `IDENTICAL: 9/9`, inner rc=0. A direct fetch of LNU04000000 failed twice with curl 56, so the lane uses FRED's UNRATENSA, which is the same BLS series.

## Log

- 10:43:26 JST start; read the back-cast memo and README.
- 10:43:57 fetched FRED series (LNU04000000 failed, curl 56; switched to UNRATENSA).
- 10:44:33 rerun IDENTICAL 9/9.
