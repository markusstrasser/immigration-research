<script>
  import fig from '../generated/figures.json'

  const m = fig.matrix
  const acc = fig.account
  const mid = (r) => (r[0] + r[1]) / 2
  // Rows sorted by cost at the case's low end of general administration.
  const rows = m.rows.slice().sort((a, b) => mid(a.cells[1].inner) - mid(b.cells[1].inner))
  const isMain = (r) => !r.frozen && r.schools === 1 && r.colleges === 1 && r.roads === 'long_run'
  const columns = m.columns

  const services = m.rows.filter((r) => !r.frozen)
  const costs = services.flatMap((r) => r.cells.flatMap((c) => c.outer))
  const costSpan = [Math.min(...costs), Math.max(...costs)].map(Math.round)
  // The frozen row (build_data.cjs checks the signs these sentences state): worse off at the case's general
  // administration, better off only with administration fixed too.
  const frozen = m.rows.find((r) => r.frozen).cells
  const frozenCase = [frozen[1].inner[0], frozen[2].inner[1]].map(Math.round)
  const frozenFixed = frozen[0].inner.map((v) => Math.round(-v)).sort((a, b) => a - b)
  const cellCount = services.length * columns.length
  // FAQ 2's frozen services: the enterprises frozen with them and private capital fixed (welfare: negative = cost).
  const faq2 = acc.breakEven.frozenCapitalFixed
  const roads = acc.longRun.roads.map((v) => v.toFixed(2))
  const parks = acc.longRun.parks.map((v) => (v === 1 ? '1' : v.toFixed(2)))
  const rates = acc.rates.map((r) => Math.round(100 * r))

  // Pastel heat, hue for the sign: paper to terracotta where everyone else is worse off, paper to
  // blue where better off, ochre where a cell's own range crosses zero.
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t))
  const hex = (c) => '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('')
  const COST = [[252, 238, 231], [242, 202, 188], [229, 160, 134]]
  const GAIN = [[232, 240, 249], [187, 212, 238]]
  function heat(r) {
    if (r[0] < 0 && r[1] > 0) return '#ecdcae'
    const v = mid(r)
    if (v < 0) return hex(mix(GAIN[0], GAIN[1], Math.min(1, -v / 100)))
    const t = Math.min(1, v / 480)
    return t < 0.5 ? hex(mix(COST[0], COST[1], t / 0.5)) : hex(mix(COST[1], COST[2], (t - 0.5) / 0.5))
  }
  // Magnitudes only, smaller first: the cell's colour and the legend carry the direction.
  const fmt = (r) => {
    const [a, b] = r.map(Math.round)
    if (a < 0 && b > 0) return `${-a} better to ${b} worse`
    const [p, q] = [Math.abs(a), Math.abs(b)].sort((m, n) => m - n)
    return p === q ? String(p) : `${p}–${q}`
  }
  const level = (v) => (v === 'cbo' ? '63–66%' : v === 1 || v === 'full' ? 'full' : v === 'long_run' ? 'long run' : 'fixed')
  const off = (v) => v === 0 || v === 'fixed'
  const colLabel = (g) => (g === 0 ? '0' : g === 1 ? '1' : g.toFixed(2))
</script>

<section class="fig" id="matrix">
  <div class="body">
    <p class="kicker">Complete account · every combination</p>
    <h2>Every combination that charges for services leaves everyone else worse off</h2>
    <p class="lede">
      Four budget choices on the left, general administration across the top. All
      <span class="num">{cellCount}</span> combinations that charge for services leave everyone else
      <span class="num">${costSpan[0]}–{costSpan[1]}bn</span> a year worse off, whatever the tax-incidence rule,
      the justice and hospital-care keys or the production model. With every service budget frozen, everyone
      else is still <span class="num">${frozenCase[0]}–{frozenCase[1]}bn</span> worse off at the case’s general
      administration; only with administration fixed as well do they come out ahead, by
      <span class="num">${frozenFixed[0]}–{frozenFixed[1]}bn</span>.
    </p>

    <div class="scroll">
      <table class="book matrix">
        <thead>
          <tr>
            <th colspan="4" class="grp">Grows with the population</th>
            <th colspan="4" class="grp right">General administration responds at</th>
          </tr>
          <tr>
            <th>Schools</th>
            <th>Colleges</th>
            <th>Police, health, welfare</th>
            <th>Roads, parks</th>
            {#each columns as g}
              <th class="c">{colLabel(g)}</th>
            {/each}
          </tr>
        </thead>
        <tbody>
          {#each rows as r}
            <tr class:main={isMain(r)} class:frozen={r.frozen}>
              <td class="ind" class:off={off(r.schools)}>{level(r.schools)}</td>
              <td class="ind" class:off={off(r.colleges)}>{level(r.colleges)}</td>
              <td class="ind" class:off={r.frozen}>{r.frozen ? 'fixed' : 'full'}</td>
              <td class="ind" class:off={off(r.roads)}>{level(r.roads)}</td>
              {#each r.cells as c, j}
                <td class="cell" class:adopted={isMain(r) && (j === 1 || j === 2)} style="background:{heat(c.inner)}">
                  <span class="v num">{fmt(c.inner)}</span>
                  <span class="o num">{fmt(c.outer)}</span>
                </td>
              {/each}
            </tr>
          {/each}
        </tbody>
      </table>
    </div>
    <p class="note">
      $bn a year for everyone else: orange cells worse off by that much, blue better off, ochre where a
      range runs from one to the other. Large figure: the case’s own open choices. Small figure: every
      executed alternative as well. Outlined: the main case,
      <span class="num">${Math.round(acc.main[0])}–{Math.round(acc.main[1])}bn</span> worse off.
    </p>
  </div>

  <aside class="side">
    <p>
      “Full” means the budget grows one for one with the population; “fixed” means not at all. Schools at
      63–66% follow CBO’s enrollment coefficients; the main case charges them in full. “Long run” is the
      case’s response as budgets adjust over decades: {roads[0]}–{roads[1]} for roads and transport,
      {parks[0]}–{parks[1]} for parks. Police, courts and prisons are charged by use in every row, and unpaid
      hospital care by uninsured use.
    </p>
    <p>
      In every cell, rental assistance grows with the population; care work, shelter and the audit
      corrections count in full; property taxes take their long-run response; public enterprises’ losses
      count; and public capital earns {rates[0]}–{rates[1]}%. The frozen row freezes the service budgets alone.
    </p>
    <p>
      The small figure adds all {m.receipts.length} executed tax-incidence rules, the
      {m.justiceKeys.length} justice keys, the {m.ucKeys.length} hospital-care keys and the production
      grid with private capital adjusted: a gain of ${m.productionSpan[0].toFixed(0)}–{m.productionSpan[1].toFixed(0)}bn
      across 432 scenarios.
    </p>
    <p>
      Not in the grid: letting natives and immigrants be imperfect substitutes raises the gain from their
      work, mostly through a transfer from other foreign-born residents to natives, and it has not been run
      on the main case (FAQ 14). With every service budget frozen, the enterprises frozen with them and private capital not
      adjusting, everyone else ends between ${Math.round(-faq2[0])}bn worse off and ${Math.round(faq2[1])}bn better
      off (FAQ 2).
    </p>
    <p>build_data.cjs; five cells reproduce main_case_bands.csv and summary.json exactly.</p>
  </aside>
</section>

<style>
  .matrix { width: 100%; min-width: 40rem; font-size: 0.86rem; }
  .matrix th { color: var(--muted); font-size: 0.8rem; vertical-align: bottom; }
  .matrix th.grp { font-style: italic; font-size: 0.82rem; padding-bottom: 0; }
  .matrix th.grp.right { text-align: center; }
  .matrix th.c { text-align: center; }
  .matrix td.ind { color: var(--ink); white-space: nowrap; font-size: 0.82rem; }
  .matrix td.ind.off { color: var(--faint); font-style: italic; }
  .matrix td.cell {
    text-align: center;
    padding: 0.28rem 0.4rem;
    border-left: 2px solid var(--paper);
    border-bottom: 2px solid var(--paper);
    line-height: 1.15;
  }
  .matrix td.cell .v { display: block; font-size: 0.95rem; }
  .matrix td.cell .o { display: block; font-size: 0.7rem; color: var(--muted); }
  .matrix td.adopted { box-shadow: inset 0 0 0 1.5px var(--ink); }
  .matrix tr.main td.ind { font-weight: 700; }
  .matrix tr.frozen td { border-bottom: 1px solid var(--hair); }
</style>
