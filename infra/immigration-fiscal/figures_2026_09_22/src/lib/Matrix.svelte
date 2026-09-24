<script>
  import fig from '../generated/figures.json'

  const m = fig.matrix
  const mid = (r) => (r[0] + r[1]) / 2
  // Rows sorted by cost at the adopted low end of general administration.
  const rows = m.rows.slice().sort((a, b) => mid(a.cells[1].inner) - mid(b.cells[1].inner))
  const isMain = (r) => r.schools === 'cbo' && r.colleges === 1 && r.delayed === 0 && !r.frozen
  const columns = m.columns

  const costs = m.rows.filter((r) => !r.frozen).flatMap((r) => r.cells.flatMap((c) => c.outer))
  const frozen = m.rows.find((r) => r.frozen).cells.flatMap((c) => c.outer)
  const costSpan = [Math.min(...costs), Math.max(...costs)].map(Math.round)
  const gainSpan = [-Math.max(...frozen), -Math.min(...frozen)].map(Math.round)
  const cellCount = m.rows.filter((r) => !r.frozen).length * columns.length

  // Pastel heat: paper to terracotta for cost, paper to blue for gain.
  const mix = (a, b, t) => a.map((v, i) => Math.round(v + (b[i] - v) * t))
  const hex = (c) => '#' + c.map((v) => v.toString(16).padStart(2, '0')).join('')
  const COST = [[252, 238, 231], [242, 202, 188], [229, 160, 134]]
  const GAIN = [[232, 240, 249], [187, 212, 238]]
  function heat(v) {
    if (v < 0) return hex(mix(GAIN[0], GAIN[1], Math.min(1, -v / 100)))
    const t = Math.min(1, v / 360)
    return t < 0.5 ? hex(mix(COST[0], COST[1], t / 0.5)) : hex(mix(COST[1], COST[2], (t - 0.5) / 0.5))
  }
  const fmt = (r) => {
    const [a, b] = r.map(Math.round)
    const f = (n) => (n < 0 ? '−' + Math.abs(n) : String(n))
    return a < 0 || b < 0 ? `${f(a)} to ${f(b)}` : `${a}–${b}`
  }
  const level = (v) => (v === 'cbo' ? '63–66%' : v === 1 ? 'full' : 'fixed')
  const colLabel = (g) => (g === 0 ? '0' : g === 1 ? '1' : g.toFixed(2))
</script>

<section class="fig" id="matrix">
  <div class="body">
    <p class="kicker">Complete account · every combination</p>
    <h2>Every combination that charges for services is a cost</h2>
    <p class="lede">
      Four budget choices on the left, general administration across the top. All
      <span class="num">{cellCount}</span> combinations cost other residents
      <span class="num">${costSpan[0]}–{costSpan[1]}bn</span> a year, whatever the tax-incidence rule, the
      justice and hospital-care keys or the production model. Only freezing every service budget turns the result into a
      gain, of <span class="num">${gainSpan[0]}–{gainSpan[1]}bn</span>.
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
              <td class="ind" class:off={r.schools === 0}>{level(r.schools)}</td>
              <td class="ind" class:off={r.colleges === 0}>{level(r.colleges)}</td>
              <td class="ind" class:off={r.frozen}>{r.frozen ? 'fixed' : 'full'}</td>
              <td class="ind" class:off={r.delayed === 0}>{level(r.delayed)}</td>
              {#each r.cells as c, j}
                <td class="cell" class:adopted={isMain(r) && (j === 1 || j === 2)} style="background:{heat(mid(c.inner))}">
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
      $bn a year, positive a cost to other US residents. Large figure: the account’s own open choices.
      Small figure: every executed alternative as well. Outlined: the main case,
      <span class="num">${Math.round(fig.account.main[0])}–{Math.round(fig.account.main[1])}bn</span>.
    </p>
  </div>

  <aside class="side">
    <p>
      “Full” means the budget grows one for one with the population; “fixed” means not at all; schools
      at 63–66% follow CBO’s enrollment coefficients. Police, courts and prisons are charged by use in
      every row, and uninsured hospital care by uninsured use.
    </p>
    <p>
      The small figure adds all {m.receipts.length} executed tax-incidence rules, the
      {m.justiceKeys.length} justice keys, the {m.ucKeys.length} hospital-care keys and the production
      grid with private capital adjusted: a gain of ${m.productionSpan[0].toFixed(0)}–{m.productionSpan[1].toFixed(0)}bn
      across 432 scenarios. The data corrections are measured on CBO’s incidence rules; each other
      rule takes the same proportional change to the group’s share of each tax.
    </p>
    <p>
      Not in the grid: letting natives and immigrants be imperfect substitutes would lower every cell by
      about $4–8bn at the elasticity the job data support (FAQ 14). With private capital also held
      fixed, the frozen row runs from a gain to a cost (FAQ 2).
    </p>
    <p>build_data.cjs; three rows reproduce main_case_bands.csv exactly.</p>
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
