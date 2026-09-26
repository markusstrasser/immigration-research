<script>
  import { bands, mexican, white, categories } from '../data.js'

  let w = $state(0)

  // Magnitudes; the words around them carry the direction.
  const usd = (n) => '$' + Math.abs(Math.round(n)).toLocaleString('en-US')
  const bn = (n, digits) => '$' + Math.abs(n).toFixed(digits) + 'bn'

  const sum = (xs) => xs.reduce((s, x) => s + x, 0)
  const share = (pop) => {
    const n = sum(pop)
    return pop.map((p) => p / n)
  }
  const shM = share(mexican.pop)
  const shW = share(white.pop)
  const pop = sum(mexican.pop)
  const old = (sh) => sh[6] + sh[7]
  const pct = (x) => Math.round(100 * x) + '%'

  let blend = $derived(shM.map((m, i) => (1 - w) * m + w * shW[i]))
  let balance = $derived(sum(mexican.rate.map((r, i) => r * blend[i])))
  let whiteHere = $derived(sum(white.rate.map((r, i) => r * blend[i])))
  let total = $derived((balance * pop) / 1e9)
  let gap = $derived(balance - whiteHere)

  const movers = categories
    .map((c) => ({ ...c, move: c.white - c.own }))
    .sort((a, b) => Math.abs(b.move) - Math.abs(a.move))
  const maxMove = Math.max(...movers.map((c) => Math.abs(c.move)))

  // Left panel: weights. Right panel: net dollars per person at today's rates, drawn so that
  // receiving more than one pays in runs to the right (worse off for everyone else).
  const y0 = 46
  const dy = 29
  const barX = 58
  const barW = 190
  const maxShare = 0.3
  const rateX = 330
  const rateW = 400
  const rateLo = -36000
  const rateHi = 14000
  const rx = (v) => rateX + ((rateHi - v) / (rateHi - rateLo)) * rateW
  const k = (v) => (v === 0 ? '0' : Math.abs(v / 1000) + 'k')
  const tick = (sh) => barX + (sh / maxShare) * barW
</script>

<section class="fig" id="age">
  <div class="body">
    <p class="kicker">Generation ledger · shared allocation · 2024</p>
    <h2>Youth hides the gap</h2>
    <p class="lede">
      At every working age the group’s net balance falls short of the white one. The raw gap looks
      smaller because few of the group are old: {pct(old(shM))} are 65 or older, against {pct(old(shW))} of
      whites, and old age is where both cost the most. Slide the population to the white age structure,
      rates held at today’s values.
    </p>

    <div class="slider">
      <span>Their ages</span>
      <input type="range" min="0" max="1" step="0.01" bind:value={w} aria-label="Age weights, from the group's own to the white structure" />
      <span>White ages</span>
    </div>
    <p class="note">
      On these weights the group
      {#if balance < 0}receives <b class="num">{usd(balance)}</b> per person more than it pays in{:else}pays in <b class="num">{usd(balance)}</b> per person more than it receives{/if},
      or <span class="num">{bn(total, 0)}</span> a year for all {(pop / 1e6).toFixed(1)} million: everyone else is that
      much {total < 0 ? 'worse' : 'better'} off. Whites on the same weights
      {#if whiteHere < 0}receive <span class="num">{usd(whiteHere)}</span> more than they pay in{:else}pay in <span class="num">{usd(whiteHere)}</span> more than they receive{/if};
      the group sits <b class="num">{usd(gap)}</b> per person {gap < 0 ? 'below' : 'above'} them.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 304" role="img" aria-label="Age weights, and net dollars per person by age for each group">
      <text class="faint it" x={barX} y="12" font-size="11.5">share of the population</text>
      <text class="faint it" x={rateX} y="12" font-size="11.5">net $ per person a year, today’s rates</text>
      {#each [-30000, -20000, -10000, 0, 10000] as t}
        <line x1={rx(t)} x2={rx(t)} y1="20" y2="262" stroke={t === 0 ? '#111' : '#efece2'} />
        <text class="faint num" x={rx(t)} y="278" text-anchor="middle" font-size="11">{k(t)}</text>
      {/each}
      <text class="faint it" x={rateX} y="296" font-size="11">← pays in more than it receives</text>
      <text class="faint it" x={rateX + rateW} y="296" text-anchor="end" font-size="11">receives more than it pays in →</text>
      <text class="faint it" x={tick(shM[0])} y="31" text-anchor="middle" font-size="10.5">their ages</text>
      <text class="faint it" x={tick(shW[0])} y="31" text-anchor="middle" font-size="10.5">white ages</text>

      {#each bands as band, i}
        {@const y = y0 + i * dy}
        <text class="muted num" x="0" y={y + 4} font-size="12">{band}</text>
        <rect x={barX} y={y - 6} width={(blend[i] / maxShare) * barW} height="12" fill="#e4e1d6" />
        <line x1={tick(shM[i])} x2={tick(shM[i])} y1={y - 9} y2={y + 9} stroke="#111" stroke-width="2" />
        <line x1={tick(shW[i])} x2={tick(shW[i])} y1={y - 9} y2={y + 9} stroke="#8d897e" stroke-width="2" />

        <line x1={rx(mexican.rate[i])} x2={rx(white.rate[i])} y1={y} y2={y} stroke="#b9b5a8" />
        <circle cx={rx(white.rate[i])} cy={y} r="4.2" fill="#fffff8" stroke="#8d897e" stroke-width="1.2" />
        <circle cx={rx(mexican.rate[i])} cy={y} r="4.2" fill="#111" />
      {/each}
      <text class="it halo" x={rx(mexican.rate[0]) + 9} y={y0 + 4} font-size="11.5">Mexican-origin</text>
      <text class="muted it halo" x={rx(white.rate[0]) - 9} y={y0 + 4} text-anchor="end" font-size="11.5">third-plus white</text>
    </svg>
    </div>

    <h3>What moves when the ages move</h3>
    <p class="note">
      Each category’s change between their ages and white ages; the fill follows the slider. Right of
      the line, everyone else worse off; left, better off.
    </p>
    <div class="movers">
      {#each movers as c}
        {@const full = c.move}
        {@const shown = w * full}
        {@const px = (v) => (Math.abs(v) / maxMove) * 50}
        <span class="lab">{c.label}</span>
        <span class="track">
          <i class="mid"></i>
          {#if full < 0}
            <i class="ghost" style="left:50%; width:{px(full)}%"></i>
            <i class="bar cost" style="left:50%; width:{px(shown)}%"></i>
          {:else}
            <i class="ghost" style="right:50%; width:{px(full)}%"></i>
            <i class="bar gain" style="right:50%; width:{px(shown)}%"></i>
          {/if}
        </span>
        <span class="val"><span class="num">{bn(full, 1)}</span> {full < 0 ? 'worse off' : 'better off'}</span>
      {/each}
    </div>
  </div>

  <aside class="side">
    <p>
      With each group at its own ages, the group sits $4,093 per person below whites. On any common age
      structure it sits $7,049 to $8,716 below: the young structure is worth about $4,600 a year per
      person.
    </p>
    <p>
      The bars under the chart are each category’s change as the weights move; at the white end they
      sum to the move from everyone else $217bn a year worse off to $340bn worse off. Schools fall;
      pensions and medical care rise. A composition exercise at today’s rates, not a forecast.
    </p>
    <p>
      Dots: filled, Mexican-origin; open, third-plus whites. Ticks: black, the group’s own shares;
      grey, the white shares; pale bar, the weights in use. Sources: ledger_absolute_2026_09_17
      age_profiles.csv and age_normalizations_by_category.csv.
    </p>
  </aside>
</section>

<style>
  .movers {
    margin-top: 0.6rem;
    display: grid;
    grid-template-columns: 15rem 1fr 8.5rem;
    gap: 0.22rem 0.8rem;
    align-items: center;
    font-size: 0.86rem;
  }
  .movers .track { position: relative; height: 9px; }
  .movers .mid { position: absolute; left: 50%; top: -3px; bottom: -3px; width: 1px; background: var(--ink); }
  .movers .ghost { position: absolute; top: 3px; height: 3px; background: var(--hair); }
  .movers .bar { position: absolute; top: 0; height: 9px; }
  .movers .bar.cost { background: var(--cost-fill); box-shadow: inset 0 0 0 0.8px var(--cost); }
  .movers .bar.gain { background: var(--gain-fill); box-shadow: inset 0 0 0 0.8px var(--gain); }
  .movers .val { text-align: right; white-space: nowrap; }
  @media (max-width: 720px) {
    /* Label and value share a row, the track runs under them; dense packing puts the value back
       beside its label after the full-width track. */
    .movers { grid-template-columns: 1fr auto; grid-auto-flow: row dense; }
    .movers .track { grid-column: 1 / -1; }
  }
</style>
