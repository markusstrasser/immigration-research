<script>
  import fig from '../generated/figures.json'

  const P = fig.byPercentile
  const a = P.series.a
  const b = P.series.b
  const s = P.stats

  // A word joiner keeps a sign on the same line as its amount.
  const usd = (v) => (v < 0 ? '−' : '+') + '⁠$' + Math.abs(v).toLocaleString('en-US')
  const abs = (v) => '$' + Math.abs(v).toLocaleString('en-US')
  const tens = (v) => '$' + (Math.round(Math.abs(v) / 10) * 10).toLocaleString('en-US')
  const fifty = (v) => '$' + (Math.round(Math.abs(v) / 50) * 50).toLocaleString('en-US')
  const aheadPct = 101 - s.bAheadFrom
  const cut = Math.abs(P.top1.b.fiscal)

  // One scale for both lines. Only the richest 1% under the tax line falls below it; that point is
  // drawn to the edge and labelled with its value.
  const W = 760
  const H = 330
  const x0 = 62
  const x1 = 690
  const top = 18
  const bottom = 280
  const lo = -2000
  const hi = 3500
  const x = (p) => x0 + ((p - 1) / 99) * (x1 - x0)
  const y = (v) => top + ((hi - v) / (hi - lo)) * (bottom - top)
  const k = (v) => (v === 0 ? '0' : (v < 0 ? '−' : '+') + '$' + Math.abs(v / 1000) + 'k')

  const line = (vals, n) => vals.slice(0, n).map((v, i) => `${x(i + 1).toFixed(1)},${y(v).toFixed(1)}`).join(' ')
  const aOff = a[99] < lo
</script>

<section class="fig" id="percentiles">
  <div class="body">
    <p class="kicker">Complete account and the costs beside it · by income percentile</p>
    <h2>Paid by taxes, everyone loses. Paid by service cuts, the richest {aheadPct}% gain.</h2>
    <p class="lede">
      Line up everyone else in the US, the 296 million people outside the Mexican-origin population,
      from poorest to richest, and split them into 100 equal groups. Each dot is one group: how many
      dollars a year its average member gains or loses, counting the cost to government and the costs we
      price outside it (wages, rents, crime, hospital care). The government cost has to be paid somehow,
      and the two lines are the two ways the account considers.
    </p>
    <p class="lede">
      Paid through taxes, richer people pay more, and every group loses:
      <span class="num">{tens(s.aBelowTop[0])}</span> to <span class="num">{tens(s.aBelowTop[1])}</span> a person up to the
      99th group, <span class="num">{abs(s.aTop)}</span> in the richest 1%. Paid through service cuts, everyone loses
      the same <span class="num">${cut}</span> of services. The poorest three fifths then lose about
      <span class="num">{fifty(s.bBottom60)}</span> each, and the richest {aheadPct}% come out ahead, because they collect
      more rent as landlords and earn higher wages.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 {W} {H}" role="img" aria-label="Dollars a year gained or lost per person, in 100 income groups from poorest to richest, for two ways of paying the government cost">
      <text class="faint it" x={x0} y="10" font-size="11.5">$ a year, average person in the group</text>
      {#each [-2000, -1000, 0, 1000, 2000, 3000] as t}
        <line x1={x0 - 6} x2={x1} y1={y(t)} y2={y(t)} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.8 : 1} />
        <text class="faint num" x={x0 - 10} y={y(t) + 4} text-anchor="end" font-size="11">{k(t)}</text>
      {/each}
      <text class="faint it" x={x(64)} y={y(0) - 7} font-size="11">better off ↑</text>
      <text class="faint it" x={x(64)} y={y(0) + 15} font-size="11">worse off ↓</text>
      {#each [20, 40, 60, 80] as q}
        <line x1={x(q + 0.5)} x2={x(q + 0.5)} y1={top} y2={bottom} stroke="#efece2" stroke-dasharray="2 3" />
      {/each}
      <text class="faint it" x={x(1)} y={bottom + 16} text-anchor="start" font-size="11">poorest</text>
      <text class="faint it" x={x(50.5)} y={bottom + 16} text-anchor="middle" font-size="11">middle</text>
      <text class="faint it" x={x(100)} y={bottom + 16} text-anchor="end" font-size="11">richest</text>
      <text class="faint it" x={x(50.5)} y={bottom + 34} text-anchor="middle" font-size="11.5">100 equal groups, by income after taxes and benefits, adjusted for household size</text>

      <!-- Paid through service cuts. -->
      <polyline points={line(b, 100)} fill="none" stroke="#b8913a" stroke-width="1.4" />
      {#each b as v, i}
        <circle cx={x(i + 1)} cy={y(v)} r="1.9" fill="#ecdcae" stroke="#b8913a" stroke-width="0.7" />
      {/each}

      <!-- Paid through taxes; the richest 1% runs off the bottom of the scale. -->
      <polyline points={line(a, aOff ? 99 : 100)} fill="none" stroke="#57544c" stroke-width="1.4" />
      {#each a.slice(0, aOff ? 99 : 100) as v, i}
        <circle cx={x(i + 1)} cy={y(v)} r="1.9" fill="#e4e1d6" stroke="#57544c" stroke-width="0.7" />
      {/each}
      {#if aOff}
        <line x1={x(99)} y1={y(a[98])} x2={x(100)} y2={bottom} stroke="#57544c" stroke-width="1.4" stroke-dasharray="3 2" />
        <path d="M {x(100) - 4} {bottom - 7} L {x(100)} {bottom} L {x(100) + 4} {bottom - 7}" fill="none" stroke="#57544c" stroke-width="1.2" />
        <text class="muted num halo" x={x(100) - 8} y={bottom - 10} text-anchor="end" font-size="11.5">richest 1%: {abs(a[99])} worse off, below the chart</text>
      {/if}
      <text class="muted num halo" x={x(100) - 8} y={y(b[99]) + 4} text-anchor="end" font-size="11.5">richest 1%: {abs(b[99])} better off</text>

      <text class="muted it halo" x={x(20)} y={y(a[19]) - 12} font-size="11.5">paid through taxes: richer people pay more</text>
      <text class="muted it halo" x={x(20)} y={y(b[19]) + 20} font-size="11.5">paid through service cuts: ${cut} less for everyone</text>
    </svg>
    </div>
    <p class="note">
      Each dot is an average, and people inside a group differ. The dashed lines mark the fifths used
      above. Under either line, everyone else together is
      <span class="num" style="white-space: nowrap">${Math.abs(P.totalBn).toFixed(1)}bn</span> a year worse off.
    </p>
  </div>

  <aside class="side">
    <p>
      Counted person by person instead of by group, about one person in four or five comes out ahead
      (ladder 226).
    </p>
    <p>
      The richest 1%, per person a year: their share of the government cost {usd(P.top1.a.fiscal)} through taxes or
      {usd(P.top1.b.fiscal)} through service cuts; rent collected as landlords less rent paid {usd(P.top1.a.housing_net)};
      wages {usd(P.top1.a.wages)}; crime {usd(P.top1.a.crime)}; hospital care {usd(P.top1.a.unreimbursed_care)}. They pay
      27% of federal taxes on 18% of income (CBO, 2022), which is why the tax line drops at the end.
    </p>
    <p>
      Some sources report only broad income bands (tax shares, crime surveys). Each band’s amount is spread
      over its members by income, so inside a band the curve is smoother than the evidence.
    </p>
    <p>distribution_weights_2026_09_23/derived/channel_by_percentile.csv, measure spm, TOTAL_a and TOTAL_b.</p>
  </aside>
</section>
