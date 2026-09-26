<script>
  import fig from '../generated/figures.json'

  const byId = Object.fromEntries(fig.whoPays.map((c) => [c.id, c]))
  const fiscal = ['fiscal_a', 'fiscal_b'].map((id) => byId[id])
  const outside = ['wages', 'housing_net', 'crime', 'unreimbursed_care'].map((id) => byId[id])

  // Bottom four fifths and top fifth, outside the budget (ladder 194).
  const sumQ = (ks) => outside.reduce((s, c) => s + ks.reduce((t, k) => t + c.quintiles[k - 1].bn, 0), 0)
  const bottom = sumQ([1, 2, 3, 4])
  const topFifth = sumQ([5])
  // Magnitudes; the words around them carry the direction (negative: everyone else worse off).
  const bn = (v) => '$' + Math.abs(v).toFixed(1) + 'bn'
  const side = (v) => (v < 0 ? 'worse off' : 'better off')

  // One scale per group, shared by its panels: small multiples compare only on a common scale.
  const H = 150
  const pad = { top: 16, bottom: 22 }
  function scale(lo, hi) {
    return (v) => pad.top + ((hi - v) / (hi - lo)) * (H - pad.top - pad.bottom)
  }
  const fiscalY = scale(-8.9, 1.2)
  const outsideY = scale(-2.1, 0.9)
  // Five bars spread across the panel's width.
  const bx = (k, W) => 24 + k * ((W - 40) / 4)
  // Bar labels are magnitudes: below the line (orange) that fifth is worse off, above (blue)
  // better off, as the note under the panels says. Under 0.05% prints as 0 and is drawn grey.
  const small = (v) => Math.abs(v) < 0.05
  const pct = (v) => (small(v) ? '0' : Math.abs(v).toFixed(Math.abs(v) < 1 ? 2 : 1))
  const tone = (v) => (small(v) ? ['#e4e1d6', '#57544c'] : v < 0 ? ['#f2cabc', '#ca7a5e'] : ['#bbd4ee', '#5c97d2'])
</script>

{#snippet panel(c, y, W)}
  <figure class="mini">
    <figcaption>{c.label}<br /><span class="num">{bn(c.totalBn)}</span> a year {side(c.totalBn)}</figcaption>
    <svg viewBox="0 0 {W} {H}" role="img" aria-label="{c.label}, share of resources by income fifth">
      <line x1="14" x2={W - 10} y1={y(0)} y2={y(0)} stroke="#111" stroke-width="0.8" />
      {#each c.quintiles as q, k}
        {@const v = q.pct}
        {@const [fill, stroke] = tone(v)}
        <rect
          x={bx(k, W) - 11}
          y={Math.min(y(0), y(v))}
          width="22"
          height={Math.max(0.8, Math.abs(y(v) - y(0)))}
          {fill}
          {stroke}
          stroke-width="0.7"
        />
        <text class="num" x={bx(k, W)} y={v < 0 ? y(v) + 12 : y(v) - 4} text-anchor="middle" font-size="11">{pct(v)}</text>
        <text class="faint num" x={bx(k, W)} y={H - 3} text-anchor="middle" font-size="10.5">{k + 1}</text>
      {/each}
    </svg>
  </figure>
{/snippet}

<section class="fig" id="whopays">
  <div class="body">
    <p class="kicker">Complete account and the costs beside it · by income fifth</p>
    <h2>Who pays depends on how the bill is paid</h2>
    <p class="lede">
      Each bar is one fifth of everyone else by income, poorest on the left, and its height the
      channel’s share of that fifth’s resources. The fiscal cost is progressive if it is paid in
      proportion to taxes and regressive if it comes out as equal service cuts per person. Outside the
      budget, the bottom four fifths lose <span class="num">{bn(bottom)}</span> a year and the top fifth gains
      <span class="num">{bn(topFifth)}</span>.
    </p>

    <h3>The fiscal cost, two ways of paying it</h3>
    <div class="grid two">
      {#each fiscal as c}{@render panel(c, fiscalY, 240)}{/each}
    </div>
    <h3>Outside the budget</h3>
    <div class="grid four">
      {#each outside as c}{@render panel(c, outsideY, 190)}{/each}
    </div>
    <p class="note">
      Percent of each fifth’s resources (SPM). Below the line, orange: that fifth is worse off by that
      share; above, blue: better off; grey, about zero. The two groups of panels use different scales;
      the panels within a group share one.
    </p>
  </div>

  <aside class="side">
    <p>
      Money moves up the income scale outside the budget: landlords’ extra receipts go 77% to the top
      fifth, and more-educated workers gain from the wage split, while renters, less-educated workers and
      crime victims sit lower down.
    </p>
    <p>
      The fiscal cost here is the lane’s central ${Math.abs(byId.fiscal_a.totalBn).toFixed(1)}bn, inside the main case. Which financing rule
      applies is a value choice; both are shown (ladder 194).
    </p>
    <p>distribution_weights_2026_09_23/derived/channel_by_quintile.csv, measure spm.</p>
  </aside>
</section>

<style>
  .grid { display: grid; gap: 0.4rem 1.4rem; }
  .grid.two { grid-template-columns: repeat(2, minmax(0, 15rem)); }
  .grid.four { grid-template-columns: repeat(4, minmax(0, 1fr)); }
  .mini { margin: 0; }
  .mini figcaption { font-size: 0.8rem; line-height: 1.25; color: var(--ink); min-height: 2.6em; }
  .mini figcaption .num { color: var(--muted); }
  @media (max-width: 720px) {
    .grid.four { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  }
</style>
