# Brief: measure two modelled social channels with the repo's own instrument

Date: 2026-09-23. Operator: "how can we make better case for social costs? better estimates?
better grounding?" Two channels beside the fiscal account rest on borrowed or calibrated slopes:

1. **Congestion**, central $19.2bn ($8.0–35.3bn), uses a 2008 cross-section of 100 metros: speed
   falls 0.12% per 1% more population at fixed lanes (Couture–Duranton–Turner)
   [`congestion_2026_09_23/RESULT.md`].
2. **Wages**: the account's CES calibration moves $66–166bn a year from less-educated to
   more-educated natives (2.2–7.0% lower wages for the less educated, ε = ∞)
   [`wage_distribution_2026_09_23/RESULT.md`; ladder 191].

The repo holds a strong instrument for the 2000–2010 inflow: the Burchardi–Chaney–Hassan
ancestry prediction on 334 metros, first-stage F 63.9, passes the level-placebo the settlement
instrument fails [`ancestry_instrument_2026_09_22/RESULT.md`, `second_instrument.py`; ladder 182].
Use it to estimate both slopes on local data. The goal is a measured estimate, whichever way it
moves the channels.

## Estimate

On the same 2000–2010 metro panel (`displacement_transfers_2026_09_18/derived/metro_panel.csv`,
`pums_metro_panel.csv`; builders in that lane), long differences, population-weighted, HC1 SEs,
the instrument exactly as `second_instrument.py` builds it:

- **Commute time.** Change in mean one-way commute time (Census 2000 SF3 aggregate travel time /
  workers not at home; ACS 2008–2012 5-year B08013/B08012 or the 2010 1-year equivalent) on the
  change in the foreign-born share and, separately, on log population change instrumented by the
  predicted inflow. Convert to the speed–population elasticity the congestion lane uses and set it
  against −0.12 (SE 0.035). Control for, or report with and without, commute-mode shares; note
  that commute time conflates speed and distance.
- **Wages.** Change in log hourly or weekly wages of native workers without a BA (and with a BA),
  full-time full-year, composition-adjusted within cells of age × sex × education, on the change in
  the immigrant (and, if feasible, Mexico-born) share of employment. Set the implied percentage
  against the CES calibration's −2.2 to −7.0% for the less educated and +1.0 to +3.0% for the
  more educated, scaled to the group's actual 2024 presence.
- For both, report the first stage, reduced form, OLS, the level-placebo on 2000 outcomes, the
  Mexico-component-removed instrument, and every specification computed. A null with a wide
  interval is a result; say what it rules out.

## Data and conventions

Census key in `infra/immigration-fiscal/acquire/config.local.env` (source it; never print it; pipe
URL-bearing output through `sed -E 's/key=[A-Za-z0-9]+/key=<KEY>/g'`; the API truncates large
responses silently, so check row counts). IPUMS microdata only in `_cache/` (add a `.gitignore`
with `_cache/`); the held IPUMS panel has no metro identifier, so wages at metro level come from
the displacement lane's PUMS panel or a fresh ACS/2000-census PUMS pull at PUMA → CBSA.

## Output

`RESULT.md` opening with `**Verdict:**`, tables with SEs, what each estimate implies for the
congestion central and the wage transfer, limits. Scripts and `derived/*.csv` aggregates only.
Write only in this directory. Do not edit other lanes. Do not commit. Run with
`OPENBLAS_NUM_THREADS=1 uv run --no-project python3 <script>` from the repo root.
