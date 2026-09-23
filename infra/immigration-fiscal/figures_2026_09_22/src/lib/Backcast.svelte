<script>
  import { backcast } from '../data.js'

  const left = 44
  const right = 830
  const top = 24
  const bot = 250
  const yLo = 0
  const yHi = 400
  const x = (year) => left + ((year - 2005) / (2024 - 2005)) * (right - left)
  const y = (v) => top + ((yHi - v) / (yHi - yLo)) * (bot - top)

  const model = backcast.filter((d) => d.year < 2024)
  const band = [
    ...model.map((d) => `${x(d.year)},${y(d.hi)}`),
    ...model.map((d) => `${x(d.year)},${y(d.lo)}`).reverse(),
  ].join(' ')
  const flat = model
    .map((d, i) => `${i ? 'L' : 'M'} ${x(d.year)} ${y((d.flatLo + d.flatHi) / 2)}`)
    .join(' ')
  const last = backcast.at(-1)
</script>

<section class="fig" id="backcast">
  <p class="kicker">Fig. 6 · Back-cast of the complete account</p>
  <h2>Only 2024 is measured</h2>
  <p class="object">
    The band is the envelope of carrying the adopted 2024 position back on flat, ratio and
    income rules, low and high. The line is the flat carry. 2020 and 2021 open up
    because the ratio and income rules follow the benefit spike.
  </p>

  <svg viewBox="0 0 860 300" role="img" aria-label="Back-cast annual cost, model years hatched, 2024 measured">
    <defs>
      <pattern id="hatch" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
        <line x1="0" y1="0" x2="0" y2="5" stroke="#7c6232" stroke-width="1" />
      </pattern>
    </defs>
    {#each [0, 100, 200, 300, 400] as tick}
      <line x1={left} x2={right} y1={y(tick)} y2={y(tick)} stroke="#d4cdb8" />
      <text class="faint" x={left - 6} y={y(tick) + 4} text-anchor="end" font-size="11">{tick}</text>
    {/each}
    <rect x={x(2019.5)} y={top} width={x(2021.5) - x(2019.5)} height={bot - top} fill="#e7dcc4" />
    <polygon points={band} fill="url(#hatch)" opacity="0.85" />
    <path d={flat} fill="none" stroke="#24384a" stroke-width="1.5" />
    <line x1={x(2024)} x2={x(2024)} y1={y(last.lo)} y2={y(last.hi)} stroke="#8c2f16" stroke-width="4" />
    <text x={x(2020.5)} y="18" text-anchor="middle" font-size="11" fill="#7c6232">2020–21</text>
    <text x={x(2024)} y={y(last.hi) - 8} text-anchor="end" font-size="12" fill="#8c2f16">2024 measured</text>
    <text class="faint" x={left} y="286" font-size="11">$bn cost to other residents</text>
    <text class="faint" x={right} y="286" text-anchor="end" font-size="11">hatched = model</text>
  </svg>

  <div class="live">
    <div>
      <span class="n">$1.7–2.5tn</span>
      <span class="l">Ten years, 2024 dollars</span>
    </div>
    <div>
      <span class="n">$2.5–3.7tn</span>
      <span class="l">Fifteen years</span>
    </div>
    <div>
      <span class="n">$3.0–4.6tn</span>
      <span class="l">Twenty years, no interest</span>
    </div>
  </div>

  <p class="src">
    historical_backcast_2026_09_20/derived/backcast_annual.csv, the six adopted CBO-informed
    columns; the totals are backcast_windows.csv for the same concepts. 2020–2021 are probably
    over-attributed: pandemic business support is in national spending but was not paid in
    proportion to population.
    The band is a model range. It is not the generation ledger.
  </p>
</section>
