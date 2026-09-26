<script>
  import fig from '../generated/figures.json'

  const steps = fig.staircase
  const breakEven = fig.account.breakEven.map((v) => (100 * v).toFixed(1))
  const taxes = fig.account.bySide.receipts.map(Math.round)
  const benefits = fig.account.bySide.spending.map((v) => Math.round(-v))

  // Columns: label | step size | plot | running total. Worse off for everyone else runs right.
  const W = 800
  const stepX = 370
  const x0 = 384
  const x1 = 684
  const totalX = 696
  const lo = -100
  const hi = 350
  const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0)

  const top = 52
  const rowH = 36
  const gap = 46
  const mainIndex = steps.findIndex((s) => s.main)
  const y = (k) => top + k * rowH + (k > mainIndex ? gap : 0)
  const height = y(steps.length - 1) + 44
  // The total the main case ends on, read from the chart's own row (a positive total: worse off).
  const main = steps[mainIndex].total.map(Math.round)

  // A range as magnitudes, smaller first, with its direction in words: a positive total or step
  // leaves everyone else worse off, a negative one better off.
  const r0 = (v) => Math.round(v)
  function said(a, b) {
    const [p, q] = [r0(a), r0(b)].sort((m, n) => m - n)
    if (p < 0 && q > 0) return { n: `${-p} better off to ${q}`, w: 'worse off' }
    const [m, n] = [Math.abs(p), Math.abs(q)].sort((u, v) => u - v)
    return { n: m === n ? String(m) : `${m}–${n}`, w: q > 0 ? 'worse off' : p < 0 ? 'better off' : '' }
  }
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
  const crossing = steps.findIndex((s) => s.total[0] > 0)
</script>

<section class="fig" id="staircase">
  <div class="body">
    <p class="kicker">Complete account · adopted main case</p>
    <h2>From the tally to the bill</h2>
    <p class="lede">
      Count only taxes paid and benefits received and the Mexican-origin population leaves everyone
      else better off. Each row then charges one more public service, at the share of its cost that
      grows with the population. Schools alone are enough to leave everyone else worse off. The last
      two rows replace the survey-based shares of taxes and benefits with outside records; the two
      corrections nearly cancel. After them, the main case leaves everyone else
      <span class="num">${main[0]}–{main[1]}bn</span> a year worse off.
    </p>

    <div class="scroll">
    <svg class="wide stair" viewBox="0 0 {W} {height + 14}" role="img" aria-label="Running total for everyone else, from taxes minus benefits to the main case, one service at a time">
      {#each [100, 200, 300] as t}
        <line x1={x(t)} x2={x(t)} y1="30" y2={height - 26} stroke="#efece2" />
      {/each}
      <line x1={x(0)} x2={x(0)} y1="30" y2={height - 26} stroke="#111" stroke-width="1" />
      <text class="muted it" x="0" y="9" font-size="12">The Mexican-origin population, income year 2024</text>
      <text class="faint it" x={x(0)} y="9" text-anchor="middle" font-size="11.5">everyone else</text>
      <text class="faint it" x={x(0) - 6} y="24" text-anchor="end" font-size="11.5">← better off</text>
      <text class="faint it" x={x(0) + 6} y="24" font-size="11.5">worse off →</text>
      <text class="faint" x={stepX} y="24" text-anchor="end" font-size="11.5">each row</text>
      <text class="faint" x={totalX} y="24" font-size="11.5">running total</text>

      {#each steps as s, k}
        {#if k}
          <polygon points={ribbon(k)} fill="#eeebdf" opacity={s.beyond ? 0.55 : 1} />
        {/if}
      {/each}

      <line x1="0" x2={W} y1={y(mainIndex) + 30} y2={y(mainIndex) + 30} stroke="#dcd8c8" stroke-dasharray="2 3" />
      <text class="faint it" x="0" y={y(mainIndex) + 45} font-size="11.5">Beyond the main case: budgets it holds fixed</text>

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

      {#each [-100, 0, 100, 200, 300] as t}
        <text class="faint num" x={x(t)} y={height - 10} text-anchor="middle" font-size="11">{Math.abs(t)}</text>
      {/each}
      <text class="faint" x={x1} y={height + 6} text-anchor="end" font-size="11">$bn a year</text>
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Each bar is the range over the account’s own open choices: household costs charged to each
      person or shared, the production gain scaled by cash or GDP, the school share of education,
      63% or 66%, and general administration at 0.59 or 0.84.
    </p>
    <p>
      The corrections come from a dataset audit and four outside checks, run together through the
      engine. The tax row adds ${taxes[0]}–{taxes[1]}bn: legal status, fill-ins for survey
      nonrespondents and CBO’s income shares lower what the group pays. The benefit row takes off
      ${benefits[0]}–{benefits[1]}bn, mostly because the same status and income corrections lower the
      benefits keyed to the group, medical care is charged by use, and premium tax credits had been
      keyed as the EITC.
    </p>
    <p>
      With every other service budget fixed, everyone else comes out worse off once
      {breakEven[0]}–{breakEven[1]}% of the service costs charged to the group grow with the population.
    </p>
    <p>
      Defense, interest on existing debt and business subsidies stay at zero throughout. Charging them
      per head is an average-cost convention, not a marginal cost.
    </p>
    <p>
      build_data.cjs runs the explorer’s engine on its executed model, then with the corrections of
      main_case_2026_09_24/package.cjs; the main-case row reproduces main_case_bands.csv and the last
      row the proportional benchmark. Break-even: sign_reversal.csv.
    </p>
  </aside>
</section>

<style>
  /* The step and total columns carry words, so the chart is wider than 760; keep its text at the
     old size on phones by scrolling a little further instead of shrinking. */
  @media (max-width: 720px) { svg.stair { min-width: 680px; } }
</style>
