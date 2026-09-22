<script>
  import { bands, mexican, white, categories } from '../data.js'
  import { dollars, billions } from '../format.js'

  let t = $state(0)
  let w = $derived(Number(t))

  const sum = (xs) => xs.reduce((s, x) => s + x, 0)
  const share = (pop) => {
    const n = sum(pop)
    return pop.map((p) => p / n)
  }
  const shM = share(mexican.pop)
  const shW = share(white.pop)
  const pop = sum(mexican.pop)

  let blend = $derived(shM.map((m, i) => (1 - w) * m + w * shW[i]))
  let balance = $derived(sum(mexican.rate.map((r, i) => r * blend[i])))
  let whiteHere = $derived(sum(white.rate.map((r, i) => r * blend[i])))
  let total = $derived((balance * pop) / 1e9)
  let gap = $derived(balance - whiteHere)

  const movers = categories
    .map((c) => ({ ...c, move: c.white - c.own }))
    .sort((a, b) => Math.abs(b.move) - Math.abs(a.move))
  const maxMove = Math.max(...movers.map((c) => Math.abs(c.move)))

  const maxShare = 0.32
  const y0 = 28
  const dy = 28
  const barX = 52
  const barW = 210
  const rateX = 390
  const rateW = 430
  const rateLo = -36000
  const rateHi = 14000
  const rx = (v) => rateX + ((v - rateLo) / (rateHi - rateLo)) * rateW

  function path(rates) {
    return rates
      .map((r, i) => `${i ? 'L' : 'M'} ${rx(r).toFixed(1)} ${y0 + i * dy}`)
      .join(' ')
  }
</script>

<section class="fig" id="age">
  <p class="kicker">Fig. 2 · Generation ledger, shared</p>
  <h2>Age is a weight, and it is working in their favor</h2>
  <p class="object">
    Drag the weights from the Mexican-origin age structure to the white one.
    Rates stay at today’s values. Each group at its own ages, the gap is −$4,093.
    On a common structure it is wider.
  </p>

  <div class="slider">
    <button class:on={w < 0.05} onclick={() => (t = 0)}>Their ages</button>
    <input type="range" min="0" max="1" step="0.005" value={w} oninput={(e) => (t = +e.currentTarget.value)} aria-label="Age weights" />
    <button class:on={w > 0.95} onclick={() => (t = 1)}>White ages</button>
  </div>

  <div class="live">
    <div>
      <span class="n">{dollars(balance)}</span>
      <span class="l">Mexican-origin, per person, these weights</span>
    </div>
    <div>
      <span class="n">{billions(total, 0)}</span>
      <span class="l">Same rates, all { (pop / 1e6).toFixed(1) } million</span>
    </div>
    <div>
      <span class="n">{dollars(gap)}</span>
      <span class="l">Gap vs whites on these same weights</span>
    </div>
  </div>
  <p class="object">Whites on these weights: {dollars(whiteHere)} per person.</p>

  <svg viewBox="0 0 860 270" role="img" aria-label="Age weights and net fiscal rate by age">
    <text class="faint" x={barX} y="14" font-size="11">share of the group</text>
    <text class="faint" x={rateX} y="14" font-size="11">net $ per person, today’s rates</text>
    <line x1={rx(0)} y1="20" x2={rx(0)} y2="250" stroke="#1c1917" stroke-width="1" />

    {#each bands as band, i}
      {@const y = y0 + i * dy}
      <text class="muted" x="0" y={y + 3} font-size="11">{band}</text>
      <rect x={barX} y={y - 7} width={(blend[i] / maxShare) * barW} height="10" fill="#8c2f16" />
      <line
        x1={barX + (shM[i] / maxShare) * barW}
        x2={barX + (shM[i] / maxShare) * barW}
        y1={y - 9}
        y2={y + 5}
        stroke="#8c2f16"
        stroke-width="1"
        stroke-dasharray="1 2"
      />
      <line
        x1={barX + (shW[i] / maxShare) * barW}
        x2={barX + (shW[i] / maxShare) * barW}
        y1={y - 9}
        y2={y + 5}
        stroke="#24384a"
        stroke-width="1.4"
      />
      <circle cx={rx(mexican.rate[i])} cy={y} r="3.2" fill="#8c2f16" />
      <circle cx={rx(white.rate[i])} cy={y} r="3.2" fill="#24384a" />
    {/each}
    <path d={path(mexican.rate)} fill="none" stroke="#8c2f16" stroke-width="1.25" />
    <path d={path(white.rate)} fill="none" stroke="#24384a" stroke-width="1.25" />
    <text class="muted" x={rx(-28000)} y="262" font-size="11">rust, Mexican-origin rates</text>
    <text class="muted" x={rx(2000)} y="262" font-size="11">slate, white rates</text>
  </svg>

  <div class="cats">
    {#each movers as c}
      {@const full = c.move}
      {@const shown = w * full}
      {@const px = (v) => (Math.abs(v) / maxMove) * 50}
      <div class="cat">
        <span>{c.label}</span>
        <div class="track">
          {#if full < 0}
            <i class="ghost" style="right:50%; width:{px(full)}%"></i>
            <i class="bar cost" style="right:50%; width:{px(shown)}%"></i>
          {:else}
            <i class="ghost" style="left:50%; width:{px(full)}%"></i>
            <i class="bar save" style="left:50%; width:{px(shown)}%"></i>
          {/if}
        </div>
        <span class="num">{billions(shown, 1)}</span>
      </div>
    {/each}
  </div>

  <p class="src">
    Age profiles and category totals, shared expanded ledger. The bars under the chart are the
    change in each category as the weights move; at the right-hand end they sum to the
    −$217bn → −$340bn composition. Schools fall. Cash and medical rise. This is not a forecast.
    Dashed ticks are Mexican-origin shares; solid ticks are white shares.
  </p>
</section>
