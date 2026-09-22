<script>
  import { generations } from '../data.js'
  import { dollars } from '../format.js'

  let alloc = $state('shared')
  let g = $derived(generations[alloc])

  const names = ['First', 'Second', 'Third-plus']
  const lo = -15000
  const hi = 7000
  const top = 36
  const bottom = 250
  const xs = [150, 360, 570]
  const y = (v) => top + ((hi - v) / (hi - lo)) * (bottom - top)

  const series = $derived([
    { name: 'Receipts', color: '#24384a', values: g.receipts },
    { name: 'Spending', color: '#7c6232', values: g.spending },
    { name: 'Net', color: '#8c2f16', values: g.net, wide: true },
  ])

  function nudge(list, idx) {
    const items = list
      .map((s) => ({ color: s.color, name: s.name, v: s.values[idx], y: y(s.values[idx]) }))
      .sort((a, b) => a.y - b.y)
    for (let i = 1; i < items.length; i++) {
      if (items[i].y < items[i - 1].y + 14) items[i].y = items[i - 1].y + 14
    }
    return items
  }

  let leftLabels = $derived(nudge(series, 0))
  let rightLabels = $derived(nudge(series, 2))
</script>

<section class="fig" id="generations">
  <p class="kicker">Fig. 4 · Generation ledger, white ages</p>
  <h2>Taxes converge. The net does not.</h2>
  <p class="object">
    Same ages, three generations alive in 2024. Receipts climb toward the white level.
    The first generation’s lower spending is gone by the second. The net stays put.
    These people are not one lineage followed forward, and they are not a split of the national total.
  </p>

  <div class="picks">
    <button class:on={alloc === 'shared'} onclick={() => (alloc = 'shared')}>Household costs shared</button>
    <button class:on={alloc === 'personal'} onclick={() => (alloc = 'personal')}>Personal allocation</button>
  </div>

  <svg viewBox="0 0 860 290" role="img" aria-label="Generation slopegraph of receipts, spending and net gaps">
    <line x1="70" x2="780" y1={y(0)} y2={y(0)} stroke="#d4cdb8" />
    <text class="faint" x="64" y={y(0) + 4} text-anchor="end" font-size="11">0</text>
    {#each names as name, i}
      <text x={xs[i]} y="22" text-anchor="middle" font-size="13">{name}</text>
      <line x1={xs[i]} x2={xs[i]} y1="32" y2="258" stroke="#d4cdb8" stroke-width="1" />
    {/each}
    {#each series as s}
      <path
        d={s.values.map((v, i) => `${i ? 'L' : 'M'} ${xs[i]} ${y(v)}`).join(' ')}
        fill="none"
        stroke={s.color}
        stroke-width={s.wide ? 2.25 : 1.25}
      />
      {#each s.values as v, i}
        <circle cx={xs[i]} cy={y(v)} r="3.5" fill={s.color} />
      {/each}
    {/each}
    {#each leftLabels as lab}
      <text x={xs[0] - 12} y={lab.y + 4} text-anchor="end" font-size="12" fill={lab.color}>{dollars(lab.v)}</text>
    {/each}
    {#each rightLabels as lab}
      <text x={xs[2] + 14} y={lab.y + 4} font-size="12" fill={lab.color}>{dollars(lab.v)} {lab.name}</text>
    {/each}
  </svg>

  <p class="src">
    age_normalizations.csv, structure white_ages_today. On the shared allocation the first and
    second generations are $82 apart. Spending above zero means less spending than whites.
    Lifetime values at 3% (second −$280k, third-plus −$225k, white −$96k) are a different object
    and are not on this scale.
  </p>
</section>
