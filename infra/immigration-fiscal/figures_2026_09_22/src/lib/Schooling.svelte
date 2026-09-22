<script>
  import { schooling, fiscalWindows, incomeRatios, cohortMatrix } from '../data.js'
  import { dollars } from '../format.js'

  const y0 = 1980
  const y1 = 2023
  const left = 48
  const right = 520
  const top = 16
  const bot = 150
  const x = (year) => left + ((year - y0) / (y1 - y0)) * (right - left)
  const y = (pct) => top + ((90 - pct) / 90) * (bot - top)

  function segments(years, values) {
    const out = []
    let cur = []
    years.forEach((year, i) => {
      if (cur.length && year - years[i - 1] > 1) {
        out.push(cur)
        cur = []
      }
      cur.push([year, values[i]])
    })
    out.push(cur)
    return out
  }

  const ratioLines = [
    { label: 'Per-capita income', values: incomeRatios.perCapita, a: 0.519, b: 0.611 },
    { label: 'Median household income', values: incomeRatios.household, a: 0.781, b: 0.907 },
    { label: 'Full-time men’s earnings', values: incomeRatios.men, a: 0.641, b: 0.754 },
  ]

  function spark(values) {
    const years = incomeRatios.years
    const min = 0.48
    const max = 0.94
    return segments(years, values).map((seg) =>
      seg
        .map(([year, v], i) => {
          const px = ((year - 2008) / (2024 - 2008)) * 160
          const py = 28 - ((v - min) / (max - min)) * 26
          return `${i ? 'L' : 'M'} ${px.toFixed(1)} ${py.toFixed(1)}`
        })
        .join(' '),
    )
  }
</script>

<section class="fig" id="schooling">
  <p class="kicker">Fig. 5 · Arrival cohorts, and a partial account</p>
  <h2>Schooling fell by half. The fiscal gap moved a little.</h2>
  <p class="object">
    Less-than-high-school share of Mexican arrivals aged 25–54, observed within five years
    of arrival. The fiscal marks are a different table: arrival windows on the partial account,
    per standardized person against whites.
  </p>

  <svg viewBox="0 0 860 200" role="img" aria-label="Less-than-high-school share of recent arrivals, 1980 to 2023">
    <line x1={left} x2={right} y1={y(0)} y2={y(0)} stroke="#d4cdb8" />
    {#each schooling as p, i}
      {#if i}
        <line
          x1={x(schooling[i - 1].year)}
          y1={y(schooling[i - 1].lths)}
          x2={x(p.year)}
          y2={y(p.lths)}
          stroke="#8c2f16"
          stroke-width="1.4"
        />
      {/if}
      <circle cx={x(p.year)} cy={y(p.lths)} r="3.5" fill="#8c2f16" />
      <text x={x(p.year)} y={y(p.lths) - 10} text-anchor="middle" font-size="12">{p.lths}%</text>
      <text class="faint" x={x(p.year)} y="176" text-anchor="middle" font-size="11">{p.window}</text>
    {/each}

    <text x="560" y="28" font-size="13">Older arrival windows</text>
    <text class="muted" x="560" y="48" font-size="13">{dollars(fiscalWindows.older[1])} to {dollars(fiscalWindows.older[0])}</text>
    <text x="560" y="84" font-size="13">Arrived 2016–2025</text>
    <text class="muted" x="560" y="104" font-size="13">{dollars(fiscalWindows.recent)}</text>
    <text class="faint" x="560" y="128" font-size="11">partial account, vs whites</text>
  </svg>

  <div class="sparks">
    {#each ratioLines as line}
      <div>
        <svg viewBox="0 0 160 36" aria-hidden="true">
          {#each spark(line.values) as d}
            <path {d} fill="none" stroke="#24384a" stroke-width="1.4" />
          {/each}
        </svg>
        <p>{line.label}<br />{line.a.toFixed(2)} → {line.b.toFixed(2)} of the national figure, 2008–2024</p>
      </div>
    {/each}
  </div>

  <table class="matrix">
    <thead>
      <tr>
        <th>Cohort</th>
        {#each cohortMatrix.cols as col}<th>{col} years here</th>{/each}
      </tr>
    </thead>
    <tbody>
      {#each cohortMatrix.rows as row}
        <tr>
          <th>{row.cohort}</th>
          {#each row.cells as cell}
            <td>
              {#if cell == null}
                <span class="cell"><em>—</em></span>
              {:else}
                <span class="cell">
                  <i style="width: {(cell * 4.2).toFixed(2)}rem"></i>
                  {(cell * 100).toFixed(0)}%
                </span>
              {/if}
            </td>
          {/each}
        </tr>
      {/each}
    </tbody>
  </table>

  <p class="src">
    Arrival-cohort memo, census and ACS, ages 25–54 within five years. Income ratios from the
    back-cast ACS input; 2010 and 2020 are missing and the lines break there. The matrix is
    edu_lths_cohort_x_duration_matrix.csv. An empty cell has not been observed. Men’s earnings
    rose in 2016–2019 and 2021–2023 and were flat in 2024.
  </p>
</section>
