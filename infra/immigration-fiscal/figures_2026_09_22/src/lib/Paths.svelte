<script>
  import { ruleYears, rulePaths, programmeYears, programmes } from '../data.js'

  const mid = (lo, hi) => lo.map((v, i) => (v + hi[i]) / 2)
  const programme = mid(rulePaths.programme.lo, rulePaths.programme.hi)
  const income = mid(rulePaths.income.lo, rulePaths.income.hi)
  const preferred = income.slice()
  const i19 = ruleYears.indexOf(2019)
  const i22 = ruleYears.indexOf(2022)
  const repaired = (income[i19] + income[i22]) / 2
  preferred[ruleYears.indexOf(2020)] = repaired
  preferred[ruleYears.indexOf(2021)] = repaired

  const left = 44
  const right = 760
  const top = 16
  const bot = 230
  const x = (year) => left + ((year - 2005) / 19) * (right - left)
  const y = (v) => top + ((420 - v) / 420) * (bot - top)
  const line = (values) => values.map((v, i) => `${i ? 'L' : 'M'} ${x(ruleYears[i])} ${y(v)}`).join(' ')

  const pLeft = 168
  const pRight = 800
  const pTop = 28
  const pBot = 200
  const py = (v) => pTop + ((1.15 - Math.min(v, 1.15)) / (1.15 - 0.35)) * (pBot - pTop)
  const px = (year) => pLeft + ((year - 2005) / 19) * (pRight - pLeft)
  const tags = programmes
    .map((s) => ({ ...s, y: py(s.v[0]) }))
    .sort((a, b) => a.y - b.y)
  for (let i = 1; i < tags.length; i++) {
    if (tags[i].y < tags[i - 1].y + 13) tags[i].y = tags[i - 1].y + 13
  }
</script>

<section class="fig" id="programmes">
  <p class="kicker">With fig. 6</p>
  <h2>The budgets do not move together</h2>
  <p class="object">
    Real national spending per resident. Every line is 1 in 2024.
  </p>
  <svg viewBox="0 0 860 240" role="img" aria-label="Program spending indexes, 2024 equals 1, credits marked above the frame">
    <line x1={pLeft} x2={pRight} y1={py(1)} y2={py(1)} stroke="#1c1917" stroke-width="1" />
    <text class="faint" x={pRight + 6} y={py(1) + 4} font-size="11">1</text>
    {#each programmes as series}
      {@const d = series.v.map((v, i) => `${i ? 'L' : 'M'} ${px(programmeYears[i])} ${py(v)}`).join(' ')}
      <path {d} fill="none" stroke={series.color} stroke-width={series.name === 'Credits' ? 2 : 1.3} />
    {/each}
    {#each tags as tag}
      <text x={pLeft - 8} y={tag.y + 4} text-anchor="end" font-size="11" fill={tag.color}>{tag.name}</text>
    {/each}
    <text fill="#8c2f16" x={px(2020) - 14} y="16" text-anchor="end" font-size="12">2.3×</text>
    <text fill="#8c2f16" x={px(2021) + 14} y="16" text-anchor="start" font-size="12">4.4×</text>
    {#each [2005, 2010, 2015, 2024] as year}
      <text class="faint" x={px(year)} y="228" text-anchor="middle" font-size="11">{year}</text>
    {/each}
  </svg>
  <p class="src">
    national_programme_index.csv. Benchmark years only. Credits are the group’s 2024 EITC and
    child-credit pattern; the 2021 point is why that pattern cannot be carried into the pandemic.
  </p>
</section>

<section class="fig" id="rule">
  <p class="kicker">With fig. 6 · September 20 anchor</p>
  <h2>The path that drops the spike</h2>
  <p class="object">
    Midpoint of the September 20 anchors, $165bn and $197bn in 2024; this programme-by-programme
    version has not been re-run on the adopted headline. Grey freezes 2024 program shares.
    Brass also scales receipts by relative income. Rust does that, then sets 2020 and 2021
    to the average of 2019 and 2022.
  </p>
  <svg viewBox="0 0 860 270" role="img" aria-label="Three back-cast rules, pandemic years replaced on the rust line">
    {#each [0, 100, 200, 300, 400] as tick}
      <line x1={left} x2={right} y1={y(tick)} y2={y(tick)} stroke="#d4cdb8" />
      <text class="faint" x={left - 6} y={y(tick) + 3} text-anchor="end" font-size="11">{tick}</text>
    {/each}
    <rect x={x(2019.5)} y={top} width={x(2021.5) - x(2019.5)} height={bot - top} fill="#e7dcc4" />
    <path d={line(programme)} fill="none" stroke="#8a8376" stroke-width="1.3" />
    <path d={line(income)} fill="none" stroke="#7c6232" stroke-width="1.3" />
    <path d={line(preferred)} fill="none" stroke="#8c2f16" stroke-width="2.2" />
    <text fill="#8a8376" x={x(2012)} y={y(programme[7]) - 8} font-size="12">frozen shares</text>
    <text fill="#7c6232" x={x(2008)} y={y(income[3]) - 8} font-size="12">income-adjusted</text>
    <text fill="#8c2f16" x={x(2022)} y={y(repaired) + 22} font-size="12">pandemic replaced</text>
    {#each [2005, 2010, 2015, 2020, 2024] as year}
      <text class="faint" x={x(year)} y="252" text-anchor="middle" font-size="11">{year}</text>
    {/each}
  </svg>
  <p class="src">
    backcast_categories_annual.csv, CBO-informed case, September 20 anchor. Replacing 2020–2021
    is the same step as income_ex_pandemic in backcast_categories_windows.csv: $1.6–1.9tn,
    $2.5–2.9tn and $3.1–3.6tn on that anchor.
  </p>
</section>
