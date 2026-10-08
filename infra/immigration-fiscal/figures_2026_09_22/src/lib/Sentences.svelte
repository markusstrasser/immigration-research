<script>
  import fig from '../generated/figures.json'

  const { backcast, backcastWindows: w, schooling, fiscalWindows, incomeRatios, kitagawa, hulls, programmes, programmeYears } =
    fig.sentences

  const tn = (r) => `$${r[0].toFixed(1)}–${r[1].toFixed(1)}tn`
  const dollars = (r) => `$${r.map((v) => Math.round(v).toLocaleString('en-US')).join('–')}`

  // Back-cast band, 2005–2023 modelled, 2024 measured.
  const bx = (year) => 3 + ((year - 2005) / 19) * 94
  const by = (v) => 23 - (v / 500) * 20
  const model = backcast.filter((d) => d.year < 2024)
  const band = [...model.map((d) => `${bx(d.year)},${by(d.hi)}`), ...model.map((d) => `${bx(d.year)},${by(d.lo)}`).reverse()].join(' ')
  const last = backcast.at(-1)
  const credits = programmes.find((p) => p.name === 'Credits')
  const creditsPeak = credits.v[programmeYears.indexOf(2021)]

  // Schooling of recent arrivals.
  const sx = (year) => 3 + ((year - 1980) / 43) * 94
  const lthsLo = Math.min(...schooling.map((p) => p.lths))
  const lthsHi = Math.max(...schooling.map((p) => p.lths))
  const sy = (pct) => 22 - ((pct - lthsLo) / (lthsHi - lthsLo)) * 18
  const lths = schooling.map((p, i) => `${i ? 'L' : 'M'} ${sx(p.year).toFixed(1)} ${sy(p.lths).toFixed(1)}`).join(' ')

  // Income ratios; the lines break where a year is missing.
  const pcLo = Math.min(...incomeRatios.perCapita)
  const pcHi = Math.max(...incomeRatios.perCapita)
  const ix = (year) => 3 + ((year - 2008) / 16) * 94
  const iy = (v) => 22 - ((v - pcLo) / (pcHi - pcLo)) * 18
  function segments(values) {
    const out = []
    let cur = []
    incomeRatios.years.forEach((year, i) => {
      if (cur.length && year - incomeRatios.years[i - 1] > 1) {
        out.push(cur)
        cur = []
      }
      cur.push([year, values[i]])
    })
    out.push(cur)
    return out.map((seg) =>
      seg.map(([year, v], i) => `${i ? 'L' : 'M'} ${ix(year).toFixed(1)} ${iy(v).toFixed(1)}`).join(' '),
    )
  }
  const ratio = (xs) => [xs[0], xs.at(-1)].map((v) => v.toFixed(2))
  const perCap = ratio(incomeRatios.perCapita)
  const household = ratio(incomeRatios.household)

  const india = kitagawa.india
  // Magnitudes; the sentence carries the direction. The hulls are the group's balance, negative
  // (everyone else worse off); the arrival windows are gaps below whites.
  const bn = (v) => '$' + Math.abs(Math.round(v)) + 'bn'
  const usd = (v) => '$' + Math.abs(Math.round(v)).toLocaleString('en-US')
</script>

<section class="fig" id="sentences">
  <div class="body sentences">
    <p class="kicker">Retired figures</p>
    <h2>Where a sentence does the work</h2>

    <p>
      Carried back on national spending per resident, the 2024 account implies that everyone else was
      <svg class="spark" viewBox="0 0 100 26" aria-label="Back-cast band, 2005 to 2023, and the measured 2024, everyone else worse off in every year">
        <polygon points={band} fill="#f2cabc" stroke="#ca7a5e" stroke-width="0.8" />
        <circle cx={bx(2024)} cy={by((last.lo + last.hi) / 2)} r="2.2" fill="#ca7a5e" />
      </svg>
      {tn(w.ten)} worse off over ten years, {tn(w.fifteen)} over fifteen and {tn(w.twenty)} over twenty, in
      2024 dollars and before interest. A year per member of the lineage, the cost runs from
      {dollars(backcast[0].perMember)} in {backcast[0].year} to {dollars(fig.account.perMember)} in 2024. Only 2024 is
      measured. The pandemic years are probably over-attributed: refundable credits ran {creditsPeak.toFixed(1)}
      times their 2024 level in 2021.
    </p>

    <p>
      Adults arriving without a high-school diploma fell from {schooling[0].lths.toFixed(1)}% to
      {schooling.at(-1).lths.toFixed(1)}% of recent arrivals
      <svg class="spark" viewBox="0 0 100 26" aria-label="Share without a diploma, 1975–80 to 2018–23">
        <path d={lths} fill="none" stroke="#111" stroke-width="1.4" />
        <circle cx={sx(schooling[0].year)} cy={sy(schooling[0].lths)} r="2.2" fill="#111" />
        <circle cx={sx(schooling.at(-1).year)} cy={sy(schooling.at(-1).lths)} r="2.2" fill="#111" />
      </svg>
      between {schooling[0].window} and {schooling.at(-1).window}. On the partial account, with the income tax
      the survey misses, the newest arrivals, 2016–2025, still run {usd(fiscalWindows.recent)} a person below
      whites, next to
      {usd(fiscalWindows.older[1])} to {usd(fiscalWindows.older[0])} below for older windows.
    </p>

    <p>
      Income per person rose from {perCap[0]} to {perCap[1]} of the national figure between 2008 and 2024
      <svg class="spark" viewBox="0 0 100 26" aria-label="Per-capita income as a share of the national figure">
        {#each segments(incomeRatios.perCapita) as d}
          <path {d} fill="none" stroke="#111" stroke-width="1.4" />
        {/each}
        <circle cx={ix(incomeRatios.years[0])} cy={iy(incomeRatios.perCapita[0])} r="2.2" fill="#111" />
        <circle cx={ix(incomeRatios.years.at(-1))} cy={iy(incomeRatios.perCapita.at(-1))} r="2.2" fill="#111" />
      </svg>
      and household income from {household[0]} to {household[1]}; part of the per-person gain is a falling
      share of children.
    </p>

    <p>
      India-born workers earn {usd(india.gap)} a year more than US-born non-Hispanic white workers:
      {usd(india.mix)} from the occupations they hold and {usd(india.within)} from higher pay inside
      them. For recent noncitizens the occupations explain more than the whole gap.
    </p>

    <p>
      On the per-person generation ledger, with the income tax the survey misses, a budget modeller’s
      settings leave everyone else {bn(hulls.practitioner[1])} to {bn(hulls.practitioner[0])} a year worse off,
      and every switch the design allows spans {bn(hulls.design[1])} to {bn(hulls.design[0])} worse off. That is
      a range of conventions, not a confidence interval, and a different object from the complete account.
    </p>
  </div>

  <aside class="side">
    <p>
      These were figures on the earlier version of this page. Each fits in one sentence; the small
      graphics keep their shape.
    </p>
    <p>
      historical_backcast_2026_09_20 (derived/oct07 backcast_annual.csv and backcast_windows.csv, main case
      v6; national_programme_index.csv; the ACS income input); arrival_cohorts_2026_09_18
      entry_quality_fixed_duration_ipums.csv; arrival_window_fiscal_2026_09_18 window_estimates.csv;
      indian_generation_2026_09_21 occ_kitagawa.csv; ledger_recut_2026_09_22 hulls.csv.
    </p>
  </aside>
</section>
