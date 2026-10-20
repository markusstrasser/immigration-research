<script>
  import fig from '../generated/figures.json'

  const steps = fig.staircase
  const acc = fig.account
  const pct = (v) => (100 * v).toFixed(1)
  // Both ends of the break-even share, the case's personal allocation (enterprises with services), most adverse first.
  const breakEven = acc.breakEven.personal.map(pct)
  const cashTally = acc.tally.cash.map((v) => Math.round(-v)).sort((a, b) => a - b)
  const cash = acc.cash.map(Math.round)
  const gg = acc.gg.map((g) => g.toFixed(2))
  const shares = acc.shares.map((s) => Math.round(100 * s))
  const rate = (100 * acc.rate).toFixed(2)

  // Columns: label | step size | plot | running total. Worse off for everyone else runs right.
  // Wider than the plot needs: a range that crosses zero spells out both directions in the total column.
  const W = 860
  const stepX = 370
  const x0 = 384
  const x1 = 684
  const totalX = 696
  // Wide enough on the left for the job-capital step, the furthest the running total gets toward better off.
  const lo = -130
  const hi = 500
  const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0)

  const top = 52
  const rowH = 36
  const gap = 46
  const mainIndex = steps.findIndex((s) => s.main)
  const y = (k) => top + k * rowH + (k > mainIndex ? gap : 0)
  const height = y(steps.length - 1) + 44
  // The total the main case ends on, read from the chart's own row (a positive total: worse off).
  const main = steps[mainIndex].total.map(Math.round)
  const tally = steps[0].total

  // A range as magnitudes, smaller first, with its direction in words: a positive total or step
  // leaves everyone else worse off, a negative one better off.
  const r0 = (v) => Math.round(v)
  function said(a, b) {
    const [p, q] = [r0(a), r0(b)].sort((m, n) => m - n)
    if (p < 0 && q > 0) return { n: `${-p} better off to ${q}`, w: 'worse off' }
    const [m, n] = [Math.abs(p), Math.abs(q)].sort((u, v) => u - v)
    return { n: m === n ? String(m) : `${m}–${n}`, w: q > 0 ? 'worse off' : p < 0 ? 'better off' : '' }
  }
  // The tally leaves everyone else better off at every choice (build_data.cjs checks it): magnitudes, smaller first.
  const tallyEnds = tally.map((v) => Math.round(-v)).sort((a, b) => a - b)
  // Bar colour is the sign of the running total; ochre where the open choices decide it.
  function tone(t) {
    if (t[1] <= 0) return ['#bbd4ee', '#5c97d2']
    if (t[0] >= 0) return ['#f2cabc', '#ca7a5e']
    return ['#ecdcae', '#b8913a']
  }

  // The ribbon joins each running total to the next.
  function ribbon(k) {
    const a = steps[k - 1].total
    const b = steps[k].total
    return [
      [x(a[0]), y(k - 1) + 5],
      [x(a[1]), y(k - 1) + 5],
      [x(b[1]), y(k) - 5],
      [x(b[0]), y(k) - 5],
    ]
      .map((p) => p.join(','))
      .join(' ')
  }
  // The first row from which every total is worse off (build_data.cjs checks that every later row is).
  const crossing = steps.findIndex((s) => s.total[0] > 0)
</script>

<section class="fig" id="staircase">
  <div class="body">
    <p class="kicker">Complete account · main case v9 (adopted October 20, 2026)</p>
    <h2>From the tally to the bill</h2>
    <p class="lede">
      Count only taxes paid and benefits received, with pension promises counted as they are earned, and
      the Mexican-origin population leaves everyone else slightly better off:
      <span class="num">${tallyEnds[0]}–{tallyEnds[1]}bn</span> a year.
      Each row then adds one line of the main case.
      Property taxes, the gain from their work and the taxes on the business capital their jobs use tilt
      the balance further toward everyone else; schools at their full cost are enough to leave everyone
      else worse off at every choice. With the return on public capital, the main case leaves everyone
      else <span class="num">${main[0]}–{main[1]}bn</span> a year worse off.
    </p>

    <div class="scroll">
    <svg class="wide stair" viewBox="0 0 {W} {height + 14}" role="img" aria-label="Running total for everyone else, from taxes minus benefits to the main case, one line at a time">
      {#each [-100, 100, 200, 300, 400] as t}
        <line x1={x(t)} x2={x(t)} y1="30" y2={height - 26} stroke="#efece2" />
      {/each}
      <line x1={x(0)} x2={x(0)} y1="30" y2={height - 26} stroke="#111" stroke-width="1" />
      <text class="muted it" x="0" y="9" font-size="12">The Mexican-origin population, income year 2024</text>
      <text class="faint it" x={x(0)} y="9" text-anchor="middle" font-size="11.5">everyone else</text>
      <text class="faint it" x={x(0) - 6} y="24" text-anchor="end" font-size="11.5">← better off</text>
      <text class="faint it" x={x(0) + 6} y="24" font-size="11.5">worse off →</text>
      <text class="faint" x={stepX} y="9" text-anchor="end" font-size="11.5">each row</text>
      <text class="faint" x={totalX} y="9" font-size="11.5">running total</text>

      {#each steps as s, k}
        {#if k}
          <polygon points={ribbon(k)} fill="#eeebdf" opacity={s.beyond ? 0.55 : 1} />
        {/if}
      {/each}

      <line x1="0" x2={W} y1={y(mainIndex) + 30} y2={y(mainIndex) + 30} stroke="#dcd8c8" stroke-dasharray="2 3" />
      <text class="faint it" x="0" y={y(mainIndex) + 45} font-size="11.5">Beyond the main case: what it holds back</text>

      {#each steps as s, k}
        {@const yy = y(k)}
        {@const [fill, stroke] = tone(s.total)}
        {@const step = s.step ? said(s.step[0], s.step[1]) : null}
        {@const total = said(s.total[0], s.total[1])}
        <text x="0" y={yy + 4} font-size="13.5" font-weight={s.main ? 700 : 400} class={s.beyond ? 'muted' : undefined}>{s.label}</text>
        {#if s.note}
          <text class="faint it" x="0" y={yy + 18} font-size="11">{s.note}</text>
        {/if}
        {#if step}
          <text class="muted" x={stepX} y={yy + 4} text-anchor="end" font-size="12.5"><tspan class="num">{step.n}</tspan><tspan class="it" font-size="11">&nbsp;{step.w}</tspan></text>
        {/if}
        <rect
          x={x(s.total[0])}
          y={yy - 5}
          width={Math.max(1.5, x(s.total[1]) - x(s.total[0]))}
          height="10"
          {fill}
          {stroke}
          stroke-width="0.8"
        />
        <text x={totalX} y={yy + 4} font-size="13" font-weight={s.main ? 700 : 400}><tspan class="num">{total.n}</tspan><tspan class="muted it" font-size="11" font-weight="400">&nbsp;{total.w}</tspan></text>
        {#if s.main}
          <text class="faint it" x={totalX} y={yy + 18} font-size="11">the main case</text>
        {/if}
      {/each}

      {#if crossing > 0}
        <text class="muted it" x={x(0) + 7} y={(y(crossing - 1) + y(crossing)) / 2 + 4} font-size="11.5">worse off from here on</text>
      {/if}

      {#each [-100, 0, 100, 200, 300, 400, 500] as t}
        <text class="faint num" x={x(t)} y={height - 10} text-anchor="middle" font-size="11">{Math.abs(t)}</text>
      {/each}
      <text class="faint" x={x1} y={height + 6} text-anchor="end" font-size="11">$bn a year</text>
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Each bar is the range over the case’s own open choices: the gain from their work scaled by cash or
      GDP; schools at {shares[0]}% or {shares[1]}% of the education budget; a low or a high reading, which sets
      general administration at {gg[0]} or {gg[1]} and roads and parks at their long-run responses; and unpaid
      hospital care keyed to uninsured use, low or high. Household costs are charged to each person, and
      public capital earns one rate at both ends, {rate}% real, the flat equivalent of the Social Security
      Trustees’ path that also prices the pension promises.
    </p>
    <p>
      The row for mixed households and the people the Census misses holds the taxes, credits, benefits and
      spending of the non-members who stay in mixed households, the {acc.coverageM.toFixed(2)} million members the
      Census misses, and the recounts of native Mexican-origin children and of whether the missed people own
      or rent. The case prices
      them at its own responses and gives them no split by line, so they do not move with the rows above.
    </p>
    <p>
      Pension promises count as members earn them, at the benefits current law can pay. Counted when the
      benefits are paid instead, the tally leaves everyone else ${cashTally[0]}–{cashTally[1]}bn better off and
      the main case ${cash[0]}–{cash[1]}bn worse off.
    </p>
    <p>
      With private capital adjusting and every service budget frozen, the public enterprises included,
      everyone else comes out ahead. That lasts only while few of the service costs charged to the group grow
      with the population: fewer than
      {breakEven[0]}% at the most adverse choices, {breakEven[1]}% at the least adverse.
    </p>
    <p>
      Defense, interest on existing debt and business subsidies stay at zero throughout. Charging them
      per head is an average-cost convention, not a marginal cost.
    </p>
    <p>
      build_data.cjs runs main case v9 through its package (main_case_2026_10_16/package.cjs) on the case’s
      payload, one evaluation per row and specification. The tally is c2_tally_oct16.csv’s, with the military
      item’s parts on the completed reporters’ veterans’ benefits; the main-case row reproduces summary.json
      and the last row the package’s proportional reference. Break-even: sign_reversal.csv, oct16.
    </p>
  </aside>
</section>

<style>
  /* The step and total columns carry words, so the chart is wider than 760; keep its text at the
     old size on phones by scrolling a little further instead of shrinking (680px at the old 800). */
  @media (max-width: 720px) { svg.stair { min-width: 730px; } }
</style>
