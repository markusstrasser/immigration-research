<script>
  import fig from '../generated/figures.json'

  const P = fig.byPercentile
  const a = P.series.a
  const b = P.series.b
  const s = P.stats

  // A word joiner keeps the sign on the same line as the amount.
  const usd = (v) => (v < 0 ? '−' : '+') + '\u2060$' + Math.abs(v).toLocaleString('en-US')
  const tens = (v) => '$' + (Math.round(Math.abs(v) / 10) * 10).toLocaleString('en-US')
  const fifty = (v) => '$' + (Math.round(Math.abs(v) / 50) * 50).toLocaleString('en-US')

  // One scale for both curves. Only the top 1% under tax shares falls below it; it is drawn to the
  // edge and labelled with its value.
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
  const k = (v) => (v === 0 ? '0' : (v < 0 ? '−' : '+') + Math.abs(v / 1000) + 'k')

  const line = (vals, n) => vals.slice(0, n).map((v, i) => `${x(i + 1).toFixed(1)},${y(v).toFixed(1)}`).join(' ')
  const aOff = a[99] < lo
</script>

<section class="fig" id="percentiles">
  <div class="body">
    <p class="kicker">Complete account and the costs beside it · by income percentile</p>
    <h2>The top 1% pays most under one rule and gains most under the other</h2>
    <p class="lede">
      Each point is one percentile of other US residents, poorest on the left. Its height is how much
      better off (above zero) or worse off (below zero) the average person in it is, in dollars a year.
      If taxes pay the bill, in proportion to what each person pays, every percentile is worse off: by
      <span class="num">{tens(s.aBelowTop[0])}</span> to <span class="num">{tens(s.aBelowTop[1])}</span> a person up to the
      99th, and by <span class="num">{usd(s.aTop).slice(2)}</span> in the top 1%. If equal cuts to public services pay
      it, <span class="num">{usd(P.top1.b.fiscal).slice(2)}</span> for every person, the bottom three fifths are worse off by
      about <span class="num">{fifty(s.bBottom60)}</span> each, and from the {s.bAheadFrom}th percentile up the
      average person is better off, by <span class="num">{usd(s.bTop).slice(2)}</span> in the top 1%.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 {W} {H}" role="img" aria-label="Net dollars per person a year by income percentile, under two ways of paying the fiscal cost">
      <text class="faint it" x={x0} y="10" font-size="11.5">better (+) or worse (−) off, $ per person a year</text>
      <text class="faint it" x={x(64)} y={y(0) - 7} font-size="11">better off ↑</text>
      <text class="faint it" x={x(64)} y={y(0) + 15} font-size="11">worse off ↓</text>
      {#each [-2000, -1000, 0, 1000, 2000, 3000] as t}
        <line x1={x0 - 6} x2={x1} y1={y(t)} y2={y(t)} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.8 : 1} />
        <text class="faint num" x={x0 - 10} y={y(t) + 4} text-anchor="end" font-size="11">{k(t)}</text>
      {/each}
      {#each [20, 40, 60, 80] as q}
        <line x1={x(q + 0.5)} x2={x(q + 0.5)} y1={top} y2={bottom} stroke="#efece2" stroke-dasharray="2 3" />
      {/each}
      {#each [1, 20, 40, 60, 80, 100] as p}
        <text class="faint num" x={x(p)} y={bottom + 16} text-anchor="middle" font-size="11">{p}</text>
      {/each}
      <text class="faint it" x={x(50.5)} y={bottom + 34} text-anchor="middle" font-size="11.5">percentile of other residents, by resources per equivalent adult</text>

      <!-- Equal cuts per person. -->
      <polyline points={line(b, 100)} fill="none" stroke="#b8913a" stroke-width="1.4" />
      {#each b as v, i}
        <circle cx={x(i + 1)} cy={y(v)} r="1.9" fill="#ecdcae" stroke="#b8913a" stroke-width="0.7" />
      {/each}

      <!-- In proportion to taxes; the top 1% runs off the bottom of the scale. -->
      <polyline points={line(a, aOff ? 99 : 100)} fill="none" stroke="#57544c" stroke-width="1.4" />
      {#each a.slice(0, aOff ? 99 : 100) as v, i}
        <circle cx={x(i + 1)} cy={y(v)} r="1.9" fill="#e4e1d6" stroke="#57544c" stroke-width="0.7" />
      {/each}
      {#if aOff}
        <line x1={x(99)} y1={y(a[98])} x2={x(100)} y2={bottom} stroke="#57544c" stroke-width="1.4" stroke-dasharray="3 2" />
        <path d="M {x(100) - 4} {bottom - 7} L {x(100)} {bottom} L {x(100) + 4} {bottom - 7}" fill="none" stroke="#57544c" stroke-width="1.2" />
        <text class="muted num halo" x={x(100) - 8} y={bottom - 10} text-anchor="end" font-size="11.5">top 1%: {usd(a[99])} (off the scale)</text>
      {/if}
      <text class="muted num halo" x={x(100) - 8} y={y(b[99]) + 4} text-anchor="end" font-size="11.5">top 1%: {usd(b[99])}</text>

      <text class="muted it halo" x={x(24)} y={y(a[23]) - 12} font-size="11.5">if taxes pay the bill</text>
      <text class="muted it halo" x={x(24)} y={y(b[23]) + 20} font-size="11.5">if equal service cuts pay the bill</text>
    </svg>
    </div>
    <p class="note">
      Averages within each percentile, over the fiscal cost and the priced costs beside the account
      <span class="num" style="white-space: nowrap">({P.totalBn < 0 ? '−' : ''}${Math.abs(P.totalBn).toFixed(1)}bn</span> in all, as in the fifths above). The
      dashed rules mark the fifths.
    </p>
  </div>

  <aside class="side">
    <p>
      An average hides the spread inside a percentile. Counted person by person, about one other resident
      in four or five comes out ahead (ladder 226).
    </p>
    <p>
      The top 1%, per person a year. If taxes pay: the bill {usd(P.top1.a.fiscal)}, housing {usd(P.top1.a.housing_net)}
      (landlords’ extra rent receipts less rent paid), wages {usd(P.top1.a.wages)}, crime {usd(P.top1.a.crime)},
      hospital care {usd(P.top1.a.unreimbursed_care)}. If service cuts pay: the same except the bill,
      {usd(P.top1.b.fiscal)}. Its tax share follows CBO’s published federal share for the top 1%: 27% of federal
      taxes on 18% of income.
    </p>
    <p>
      Inputs published in bins (CBO and ITEP tax groups, NCVS income brackets) are spread inside each bin
      by the survey’s own distribution of the key, so there the curve adds shape, not measurement. Percent
      of resources is not drawn: at the 1st and 2nd percentiles resources are near zero or negative.
    </p>
    <p>distribution_weights_2026_09_23/derived/channel_by_percentile.csv, measure spm, TOTAL_a and TOTAL_b.</p>
  </aside>
</section>
