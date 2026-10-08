<script>
  import fig from '../generated/figures.json'

  const generations = fig.generations
  let alloc = $state('shared')
  let g = $derived(generations[alloc])
  const thousands = (v) => '$' + Math.round(Math.abs(v) / 1000) + 'k'
  const [life2, life3, lifeWhite] = generations.lifetime.map(thousands)
  // The case's own split, $bn at the band's low and high ends, one decimal so the parts add to the case.
  const tenth = (v) => '$' + v.toFixed(1) + 'bn'
  const split = (conv) => generations.caseSplit[conv].map((g) => g.map(tenth).join(' / '))
  const [a1, a2, a3] = split('a')
  const [b1, b2, b3] = split('b')
  const ends = fig.account.main.map(tenth).join(' and ')

  const names = ['First generation', 'Second', 'Third-plus']
  const lo = -14000
  const hi = 6000
  const top = 40
  const bottom = 262
  const xs = [165, 375, 585]
  const y = (v) => top + ((hi - v) / (hi - lo)) * (bottom - top)
  // A gap against whites as a magnitude and a word; zero is "same as whites".
  const usd = (v) => '$' + Math.abs(Math.round(v)).toLocaleString('en-US')
  const side = (v) => (v < 0 ? 'below' : v > 0 ? 'above' : 'level')

  // Series, not signs: the net is the ink line, its two parts grey, told apart by label and dash.
  const series = $derived([
    { name: 'Taxes paid', stroke: '#8d897e', fill: '#fffff8', values: g.receipts },
    { name: 'Lower benefit use', stroke: '#8d897e', fill: '#fffff8', dash: '4 3', values: g.spending },
    { name: 'Net', stroke: '#111', fill: '#111', values: g.net, wide: true },
  ])

  function place(list, idx) {
    const items = list
      .map((s) => ({ ...s, v: s.values[idx], y: y(s.values[idx]) }))
      .sort((a, b) => a.y - b.y)
    for (let i = 1; i < items.length; i++) {
      if (items[i].y < items[i - 1].y + 15) items[i].y = items[i - 1].y + 15
    }
    return items
  }
  let left = $derived(place(series, 0))
  let right = $derived(place(series, 2))
  // Middle column: each label sits off the lines that pass through its dot. The benefit gap
  // (always the top line) above and right, the net above and left, taxes below and right.
  const midSpot = { 'Lower benefit use': [10, -7, 'start'], Net: [-10, -9, 'end'], 'Taxes paid': [10, 16, 'start'] }
  let middle = $derived(
    series.map((s) => {
      const [dx, dy, anchor] = midSpot[s.name]
      return { v: s.values[1], x: xs[1] + dx, y: y(s.values[1]) + dy, anchor }
    }),
  )
</script>

<section class="fig" id="generations">
  <div class="body">
    <p class="kicker">Generation ledger · white ages · 2024</p>
    <h2>Taxes converge; the net does not</h2>
    <p class="lede">
      The gap against third-plus whites at the same ages, for three generations alive in 2024. The second
      generation pays far more tax than the first, but the first generation’s lower use of benefits is gone
      by the second, so the net gap narrows only from <span class="num">{usd(g.net[0])}</span> to
      <span class="num">{usd(g.net[2])}</span> a person.
    </p>
    <div class="controls" role="radiogroup" aria-label="Allocation">
      <label><input type="radio" bind:group={alloc} value="shared" /> Household costs shared</label>
      <label><input type="radio" bind:group={alloc} value="personal" /> Each person’s own items</label>
    </div>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 290" role="img" aria-label="Slopegraph of taxes, benefit use and net gap by generation">
      <line x1="120" x2="680" y1={y(0)} y2={y(0)} stroke="#111" stroke-width="0.8" />
      <text class="faint" x="112" y={y(0) + 4} text-anchor="end" font-size="11">same as whites</text>
      {#each names as name, i}
        <text x={xs[i]} y="20" text-anchor="middle" font-size="13" font-style="italic">{name}</text>
        <line x1={xs[i]} x2={xs[i]} y1="30" y2="270" stroke="#efece2" />
      {/each}
      {#each series as s}
        <path
          d={s.values.map((v, i) => `${i ? 'L' : 'M'} ${xs[i]} ${y(v)}`).join(' ')}
          fill="none"
          stroke={s.stroke}
          stroke-width={s.wide ? 2.4 : 1.3}
          stroke-dasharray={s.dash}
        />
        {#each s.values as v, i}
          <circle cx={xs[i]} cy={y(v)} r={s.wide ? 5 : 4} fill={s.fill} stroke={s.stroke} stroke-width={s.wide ? 1 : 1.2} />
        {/each}
      {/each}
      {#each middle as lab}
        <text class="halo" x={lab.x} y={lab.y} text-anchor={lab.anchor} font-size="11.5"><tspan class="num">{usd(lab.v)}</tspan>&nbsp;{side(lab.v)}</text>
      {/each}
      {#each left as lab}
        <text x={xs[0] - 12} y={lab.y + 4} text-anchor="end" font-size="12"><tspan class="num">{usd(lab.v)}</tspan>&nbsp;{side(lab.v)}</text>
      {/each}
      {#each right as lab}
        <text x={xs[2] + 12} y={lab.y + 4} font-size="12"><tspan class="muted" font-style="italic">{lab.name.toLowerCase()}</tspan>&nbsp; <tspan class="num">{usd(lab.v)}</tspan>&nbsp;{side(lab.v)}</text>
      {/each}
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Dollars per person a year against third-plus non-Hispanic whites at white ages. Lower benefit use
      counts in the group’s favour, so it sits above zero. Taxes include the income tax the survey misses,
      keyed as the main case keys it (item T).
    </p>
    <p>
      These are generations alive in 2024, not one family line followed forward, and not a split of the
      national total. On the shared allocation the first and second generations are
      {usd(generations.shared.net[1] - generations.shared.net[0])} apart.
    </p>
    <p>
      Lifetime values at 3%, from birth: over a life the second generation receives {life2} more than it
      pays in, third-plus {life3} and whites {lifeWhite} (FAQ 5).
    </p>
    <p>
      The complete account splits its own total, {ends} at its two ends, without a reference group.
      Counted in their own generation, the Mexico-born cost everyone else {a1}, the second generation
      {a2} and the third-plus {a3}. Counted with their parents, as the National Academies count
      children: {b1}, {b2} and {b3}. A different object from the gaps above; neither is a rescaling of the
      other.
    </p>
    <p>
      ledger_absolute_2026_09_17 age_normalizations.csv, structure white_ages_today; lifetime/period_profiles.csv;
      generation_account_2026_09_24 generation_results_oct07.csv.
    </p>
  </aside>
</section>
