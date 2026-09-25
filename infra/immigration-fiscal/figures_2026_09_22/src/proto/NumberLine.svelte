<script>
  import d from '../generated/proto_conventions.json'

  const W = 760
  const labelW = 214
  const x0 = labelW + 16
  const x1 = W - 12
  const lo = -100
  const hi = 600
  const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0)
  const top = 40
  const rowH = 48
  const H = top + d.rows.length * rowH + 44
  const ticks = [-100, 0, 100, 200, 300, 400, 500, 600]
  // Magnitudes only; the ends of the axis say which way is worse off.
  const tick = (v) => (v === 0 ? '0' : '$' + Math.abs(v))

  // "$201–246bn worse off", "$56–67bn better off", "about $0": the direction in words, never a sign.
  const n = (v) => Math.round(Math.abs(v))
  function value(c) {
    if (c[0] > 0 && c[1] < 1) return 'about $0'
    if (c[1] < 0) return `$${n(c[1])}–${n(c[0])}bn better off`
    return `$${n(c[0])}–${n(c[1])}bn worse off`
  }
  const main = d.rows.find((r) => r.central)
  const gains = d.rows.filter((r) => r.cost[1] < 0)
  const WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven']
</script>

<section class="fig" id="conventions">
  <div class="body">
    <p class="kicker">Complete account · every convention in the explorer</p>
    <h2>Only the ways of counting that leave out public services come out as a gain</h2>
    <p class="lede">
      Each bar is one way of keeping the accounts, with the range its open choices allow. The {WORDS[gains.length]}
      that come out as a gain for everyone else charge no public service at all. Every mix that lets any public budget
      grow for the added people lands well to the right of zero: the {d.matrix.combinations} such mixes in the
      “Every combination” figure run from <span class="num">${n(d.matrix.growing[0])}bn</span> to
      <span class="num">${n(d.matrix.growing[1])}bn</span> a year.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 {W} {H}" role="img" aria-label="The cost to everyone else under each accounting convention, on one line">
      <!-- Axis and gridlines. -->
      {#each ticks as t}
        <line x1={x(t)} x2={x(t)} y1={top - 22} y2={H - 38} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.9 : 1} />
        <text class="faint num" x={x(t)} y={H - 24} text-anchor="middle" font-size="11">{tick(t)}</text>
      {/each}
      <text class="faint it" x={x(0) + 5} y={H - 6} font-size="11">everyone else worse off, $bn a year →</text>
      <text class="faint it" x={x(0) - 5} y={H - 6} text-anchor="end" font-size="11">← better off</text>

      <!-- Context: the matrix's two families. -->
      <rect x={x(d.matrix.frozen[0])} y={top - 14} width={x(d.matrix.frozen[1]) - x(d.matrix.frozen[0])} height="5" fill="#bbd4ee" />
      <rect x={x(d.matrix.growing[0])} y={top - 14} width={x(d.matrix.growing[1]) - x(d.matrix.growing[0])} height="5" fill="#f2cabc" />
      <text class="faint it" x={x(d.matrix.growing[0])} y={top - 20} font-size="10.5">every mix in which some budget grows</text>
      <text class="faint it" x={x(d.matrix.frozen[1])} y={top - 20} text-anchor="end" font-size="10.5">every budget frozen</text>
      <text class="it" x="0" y={top - 9} font-size="11">For comparison</text>

      {#each d.rows as r, i}
        {@const y = top + i * rowH + 18}
        {@const gain = r.cost[1] < 0}
        {@const zero = r.cost[0] > 0 && r.cost[1] < 1}
        <text x="0" y={y - 2} font-size="12.5" font-weight={r.central ? 600 : 400}>{r.label}</text>
        <foreignObject x="0" y={y + 2} width={labelW} height="30">
          <div class="what">{r.what}</div>
        </foreignObject>
        {#if r.outer}
          <line x1={x(r.outer[0])} x2={x(r.outer[1])} y1={y - 6} y2={y - 6} stroke="#ca7a5e" stroke-width="1" />
          <line x1={x(r.outer[0])} x2={x(r.outer[0])} y1={y - 10} y2={y - 2} stroke="#ca7a5e" stroke-width="1" />
          <line x1={x(r.outer[1])} x2={x(r.outer[1])} y1={y - 10} y2={y - 2} stroke="#ca7a5e" stroke-width="1" />
        {/if}
        <rect x={x(r.cost[0])} y={y - 11} width={Math.max(3, x(r.cost[1]) - x(r.cost[0]))} height="10"
          fill={zero ? '#e4e1d6' : gain ? '#bbd4ee' : '#f2cabc'} stroke={zero ? '#57544c' : gain ? '#5c97d2' : '#ca7a5e'} stroke-width="0.8" />
        {@const cx = (x(r.cost[0]) + x(r.cost[1])) / 2}
        <text class="num halo" x={cx > x1 - 60 ? x(r.cost[1]) : cx < x0 + 60 ? x(r.cost[0]) : cx} y={y + 12}
          text-anchor={cx > x1 - 60 ? 'end' : cx < x0 + 60 ? 'start' : 'middle'} font-size="11.5">{value(r.cost)}</text>
      {/each}
    </svg>
    </div>
    <p class="note">
      Thick bars: the range the convention’s own open choices allow. The thin line on the main case adds every other choice
      the account has run (<span class="num">${n(main.outer[0])}–{n(main.outer[1])}bn</span>).
    </p>
  </div>

  <aside class="side">
    <p>
      These are accounting conventions, not people: no commentator has produced a number for this population. The
      explorer’s author notes say which convention comes closest to a commentator’s framing, and why it is not the same
      thing.
    </p>
    <p>
      The private gain from their work is about zero: once investment catches up, the added output mostly pays the
      workers who produce it. What reaches everyone else comes as taxes on that output, which this view leaves out. The
      staircase counts wages, profits and those taxes together as one small step, “Gain from their work”.
    </p>
    <p>
      Every bar uses the corrected data. The staircase starts from the uncorrected tally, a gain of
      <span class="num">${n(d.staircase.tally[1])}–{n(d.staircase.tally[0])}bn</span>, and adds the corrections as its
      last steps.
    </p>
    <p>proto/conventions.cjs; each bar is an explorer preset through the engine. Gates reproduce the main case, the
      September 20 band and the proportional case.</p>
  </aside>
</section>

<style>
  .what { font-size: 10.5px; line-height: 1.25; color: var(--faint); font-style: italic; }
  .lede .num, .note .num { white-space: nowrap; }
</style>
