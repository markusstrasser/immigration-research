<script>
  import d from '../generated/proto_flip.json'

  const W = 760
  const labelW = 262
  const t0 = 272
  const t1 = 548
  const rowH = 38
  const headH = 30

  // Bare numbers; the unit is written once per range: "$201–246bn", "4.8–16%", "1.51–1.66×".
  const pctN = (x) => {
    const v = 100 * x
    return String(Math.abs(v) < 10 && Math.abs(v - Math.round(v)) > 1e-9 ? v.toFixed(1) : Math.round(v))
  }
  const timesN = (x) => String(Number(x.toFixed(2)))
  const bnN = (x) => String(Math.round(x))
  const UNITS = {
    pct: [pctN, '', '%'],
    times: [timesN, '', '×'],
    bn: [bnN, '$', 'bn'],
  }
  const one = (unit, x) => UNITS[unit][1] + UNITS[unit][0](x) + UNITS[unit][2]
  const range = (r, unit) => {
    const [f, pre, post] = UNITS[unit]
    return f(r[0]) === f(r[1]) ? one(unit, r[0]) : pre + f(r[0]) + '–' + f(r[1]) + post
  }
  const fmt = (row, x) => one(row.unit, x)

  // Groups of rows, each drawn on its own track scale.
  const groups = [
    { title: 'One public service at a time', rows: d.services },
    { title: 'All together', rows: [d.together] },
    { title: 'What records show, and the gain from their work', rows: d.measured },
  ]
  let y = 8
  const layout = groups.map((g) => {
    const head = y
    y += headH
    const rows = g.rows.map((row) => {
      const at = y
      y += rowH
      return { row, y: at }
    })
    y += 10
    return { ...g, head, rows }
  })
  const H = y + 4

  const tx = (row, x) => t0 + ((x - row.axis[0]) / (row.axis[1] - row.axis[0])) * (t1 - t0)

  function verdict(row) {
    if (row.id === 'production') return `turns at ${range(row.roots, 'bn')}`
    if (!row.flipsInRange) {
      if (row.id === 'roads') return `at 100%: ${range(row.atEnd, 'bn')} worse off`
      return `at ${fmt(row, row.axis[0])}: still ${range(row.atStart, 'bn')} worse off`
    }
    return (row.direction > 0 ? 'turns below ' : 'turns above ') + range(row.roots, row.unit)
  }

  const allRow = d.together
  const [ben, tax, gain] = d.measured
  const schools = d.services.find((r) => r.id === 'schools')
  const times10 = Math.floor(gain.roots[0] / gain.executed[1])
</script>

<section class="fig" id="flip">
  <div class="body">
    <p class="kicker">Complete account · main case · one assumption at a time</p>
    <h2>Move any one assumption as far as it goes, and the cost stays</h2>
    <p class="lede">
      Each row takes one assumption of the main case, which puts the cost to everyone else at
      <span class="num">{range(d.main, 'bn')}</span> a year, and slides it alone across its whole range. The bar is
      orange where everyone else comes out worse off and blue where they come out better off. No single
      public service gets there: even if school budgets added nothing at all for the group’s children,
      everyone else would still be <span class="num">{range(schools.atStart, 'bn')}</span> a year worse off.
    </p>
    <p class="lede">
      Turning the bar blue takes one of four large moves: every public service at once growing by less than
      <span class="num">{range(allRow.roots, 'pct')}</span> of its average cost; benefits
      <span class="num">{range([1 - ben.roots[1], 1 - ben.roots[0]], 'pct')}</span> below what records show; taxes
      <span class="num">{range([tax.roots[0] - 1, tax.roots[1] - 1], 'pct')}</span> above what records show; or a gain from their work of
      <span class="num">{range(gain.roots, 'bn')}</span>, more than {times10} times the largest estimate the account has run.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 {W} {H}" role="img" aria-label="For each assumption, where along its range the cost to everyone else turns into a gain">

      {#each layout as g}
        <text class="it" x="0" y={g.head + 18} font-size="13">{g.title}</text>
        {#each g.rows as { row, y }}
          {@const mid = y + 17}
          <text x="0" y={mid - 2} font-size="12.5">{row.label}</text>
          <text class="faint it" x="0" y={mid + 12} font-size="11">{row.what}</text>

          <!-- The track: where everyone else is worse off, where better off, where it depends. -->
          {#each ['cost', 'mixed', 'gain'] as k}
            {@const seg = row.strip[k]}
            {#if seg && seg[1] > seg[0]}
              <rect x={tx(row, seg[0])} y={mid - 6} width={tx(row, seg[1]) - tx(row, seg[0])} height="11"
                fill={k === 'cost' ? '#f2cabc' : k === 'gain' ? '#bbd4ee' : '#ecdcae'} />
            {/if}
          {/each}
          <rect x={t0} y={mid - 6} width={t1 - t0} height="11" fill="none" stroke="#dcd8c8" stroke-width="0.8" />
          {#if (g.title !== groups[0].title || row === g.rows.at(-1).row) && !row.executed}
            <text class="faint num" x={t0} y={mid + 18} text-anchor="start" font-size="10">{fmt(row, row.axis[0])}</text>
            <text class="faint num" x={t1} y={mid + 18} text-anchor="end" font-size="10">{fmt(row, row.axis[1])}</text>
          {/if}

          <!-- The main case, and for the gain from their work the models the account ran. -->
          {#if row.executed}
            <!-- Below the track: the range of every production model the account has run. -->
            <line x1={tx(row, row.executed[0])} x2={tx(row, row.executed[1])} y1={mid + 9} y2={mid + 9} stroke="#57544c" stroke-width="0.9" />
            <line x1={tx(row, row.executed[0])} x2={tx(row, row.executed[0])} y1={mid + 6} y2={mid + 9} stroke="#57544c" stroke-width="0.9" />
            <line x1={tx(row, row.executed[1])} x2={tx(row, row.executed[1])} y1={mid + 6} y2={mid + 9} stroke="#57544c" stroke-width="0.9" />
            <text class="faint it" x={tx(row, row.executed[1]) + 5} y={mid + 13} font-size="10">models the account ran: {range(row.executed, 'bn')}</text>
          {/if}
          {#if row.main}
            {@const a = tx(row, row.main[0])}
            {@const b = tx(row, row.main[1])}
            {#if b - a < 3}
              <line x1={(a + b) / 2} x2={(a + b) / 2} y1={mid - 10} y2={mid + 9} stroke="#111" stroke-width="2" />
            {:else}
              <line x1={a} x2={b} y1={mid - 10} y2={mid - 10} stroke="#111" stroke-width="2" />
              <line x1={a} x2={a} y1={mid - 10} y2={mid + 9} stroke="#111" stroke-width="1.4" />
              <line x1={b} x2={b} y1={mid - 10} y2={mid + 9} stroke="#111" stroke-width="1.4" />
            {/if}
          {/if}

          <text class="num" x={t1 + 14} y={mid + 4} font-size="12" fill={row.flipsInRange ? '#2f5f8f' : '#111'}>{verdict(row)}</text>
        {/each}
      {/each}
      <text class="faint it" x={tx(d.services[0], d.services[0].main[1]) + 6} y={layout[0].rows[0].y + 5} font-size="10.5">main case</text>
    </svg>
    </div>
    <p class="note">
      Every other choice the account has run, on the main case’s services ({d.others.taxRules} rules for who bears each
      tax, {d.others.justiceKeys} ways to charge police and courts, {d.others.careKeys} for unpaid hospital care, {d.others.productionModels}
      models of the gain from their work), puts the cost at <span class="num">{range(d.others.range, 'bn')}</span>. None turns it into a
      gain.
    </p>
  </div>

  <aside class="side">
    <p>
      The black mark is the main case. Ochre means the answer depends on the main case’s open choices,
      such as how taxes are split and which share of education spending is schools.
    </p>
    <p>
      “Every public service” sets schools, colleges, police, health, welfare, housing and roads to one common
      share of their average cost, with general administration as in the main case. It is the break-even the
      staircase quotes.
    </p>
    <p>
      Taxes and benefits are measured from surveys and records, so their rows show how large a measurement error
      would have to be. The service rows are the account’s own assumptions.
    </p>
    <p>proto/flip.cjs; gates reproduce the main case, the published break-even and the matrix’s outer range.</p>
  </aside>
</section>

<style>
  .lede .num, .note .num { white-space: nowrap; }
</style>
