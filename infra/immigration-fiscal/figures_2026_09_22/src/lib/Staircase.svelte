<script>
  import fig from '../generated/figures.json'

  const steps = fig.staircase
  const breakEven = fig.account.breakEven.map((v) => (100 * v).toFixed(1))

  // Columns: label | step size | plot | running total.
  const stepX = 336
  const x0 = 352
  const x1 = 676
  const totalX = 688
  const lo = -100
  const hi = 350
  const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0)

  const top = 52
  const rowH = 36
  const gap = 46
  const mainIndex = steps.findIndex((s) => s.main)
  const y = (k) => top + k * rowH + (k > mainIndex ? gap : 0)
  const height = y(steps.length - 1) + 44

  const r0 = (v) => Math.round(v)
  function range(a, b) {
    const [p, q] = [r0(a), r0(b)]
    const f = (n) => (n < 0 ? '−' + Math.abs(n) : String(n))
    if (p === q) return f(p)
    if (p < 0 || q < 0) return `${f(p)} to ${f(q)}`
    return `${p}–${q}`
  }
  function stepText(s) {
    if (!s) return ''
    const [p, q] = [r0(s[0]), r0(s[1])]
    const f = (n) => (n < 0 ? '−' + Math.abs(n) : '+' + n)
    return p === q ? f(p) : `${f(p)} to ${f(q)}`
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
      Count only taxes paid and benefits received and the Mexican-origin population leaves other
      residents better off. Each row then charges one more public service, at the share of its cost
      that grows with the population. Schools alone are enough to turn the sign.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 {height}" role="img" aria-label="Running total from taxes minus benefits to the main case, one service at a time">
      {#each [100, 200, 300] as t}
        <line x1={x(t)} x2={x(t)} y1="30" y2={height - 26} stroke="#efece2" />
      {/each}
      <line x1={x(0)} x2={x(0)} y1="30" y2={height - 26} stroke="#111" stroke-width="1" />
      <text class="faint it" x={x(0) - 6} y="24" text-anchor="end" font-size="11.5">gain</text>
      <text class="faint it" x={x(0) + 6} y="24" font-size="11.5">cost to other US residents</text>
      <text class="faint" x={stepX} y="24" text-anchor="end" font-size="11.5">adds</text>
      <text class="faint" x={totalX} y="24" font-size="11.5">running total</text>

      {#each steps as s, k}
        {#if k}
          <polygon points={ribbon(k)} fill="#eeebdf" opacity={s.beyond ? 0.55 : 1} />
        {/if}
      {/each}

      <line x1="0" x2="760" y1={y(mainIndex) + 30} y2={y(mainIndex) + 30} stroke="#dcd8c8" stroke-dasharray="2 3" />
      <text class="faint it" x="0" y={y(mainIndex) + 45} font-size="11.5">Beyond the main case: budgets it holds fixed</text>

      {#each steps as s, k}
        {@const yy = y(k)}
        {@const neg = s.total[1] <= 0}
        <text x="0" y={yy + 4} font-size="13.5" font-weight={s.main ? 700 : 400} class={s.beyond ? 'muted' : undefined}>{s.label}</text>
        {#if s.note}
          <text class="faint it" x="0" y={yy + 18} font-size="11">{s.note}</text>
        {/if}
        <text class="muted num" x={stepX} y={yy + 4} text-anchor="end" font-size="12.5">{stepText(s.step)}</text>
        <rect
          x={x(s.total[0])}
          y={yy - 5}
          width={Math.max(1.5, x(s.total[1]) - x(s.total[0]))}
          height="10"
          fill={neg ? '#bbd4ee' : '#f2cabc'}
          stroke={neg ? '#5c97d2' : '#ca7a5e'}
          stroke-width="0.8"
        />
        <text x={totalX} y={yy + 4} font-size="13" font-weight={s.main ? 700 : 400} class="num">{range(s.total[0], s.total[1])}</text>
        {#if s.main}
          <text class="faint it" x={totalX} y={yy + 18} font-size="11">the main case</text>
        {/if}
      {/each}

      {#if crossing > 0}
        <text class="muted it" x={x(0) + 7} y={(y(crossing - 1) + y(crossing)) / 2 + 4} font-size="11.5">the sign turns here</text>
      {/if}

      {#each [-100, 0, 100, 200, 300] as t}
        <text class="faint num" x={x(t)} y={height - 10} text-anchor="middle" font-size="11">{t < 0 ? '−' + Math.abs(t) : t}</text>
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
      With every other service budget fixed, the sign turns once {breakEven[0]}–{breakEven[1]}% of
      the service costs charged to the group grow with the population.
    </p>
    <p>
      Defense, interest on existing debt and business subsidies stay at zero throughout. Charging them
      per head is an average-cost convention, not a marginal cost.
    </p>
    <p>
      build_data.cjs runs the explorer’s engine on its executed model; the main-case row reproduces
      main_case_bands.csv and the last row the proportional benchmark. Break-even:
      sign_reversal.csv.
    </p>
  </aside>
</section>
