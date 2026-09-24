<script>
  import fig from '../generated/figures.json'
  import { education } from '../data.js'
  import { dollars } from '../format.js'

  let alloc = $state('personal')

  const left = 70
  const right = 700
  const top = 20
  const bottom = 380
  const yLo = -12000
  const yHi = 34000
  const x = (share) => left + share * (right - left)
  const y = (v) => top + ((yHi - v) / (yHi - yLo)) * (bottom - top)
  const clamp = (v) => Math.max(yLo, Math.min(yHi, v))

  const groups = fig.origins.filter((o) => !o.reference)
  const refs = fig.origins.filter((o) => o.reference)

  // Label placement: try spots around each dot, keep the first that clears every dot and every
  // label already placed. Mexico and India go first so they keep the plain right-hand spot.
  let labels = $derived.by(() => {
    const pts = groups.map((o) => ({ id: o.id, name: o.name, cx: x(o.ba), cy: y(o[alloc].v) }))
    const dots = pts.map((p) => ({ x0: p.cx - 5, x1: p.cx + 5, y0: p.cy - 5, y1: p.cy + 5 }))
    const first = ['mexico_born', 'india']
    const order = pts.slice().sort((a, b) => (first.includes(b.id) ? 1 : 0) - (first.includes(a.id) ? 1 : 0) || a.cx - b.cx)
    const placed = []
    const clear = (b) => ![...dots, ...placed.map((l) => l.box)].some((o) => b.x0 < o.x1 && b.x1 > o.x0 && b.y0 < o.y1 && b.y1 > o.y0)
    for (const p of order) {
      const w = p.name.length * 6.1 + 2
      const spots = [
        [p.cx + 8, p.cy + 4, 'start'], [p.cx - 8, p.cy + 4, 'end'],
        [p.cx + 6, p.cy - 8, 'start'], [p.cx + 6, p.cy + 16, 'start'],
        [p.cx - 6, p.cy - 8, 'end'], [p.cx - 6, p.cy + 16, 'end'],
        [p.cx + 8, p.cy - 19, 'start'], [p.cx + 8, p.cy + 27, 'start'],
      ]
      const boxOf = ([tx, ty, anchor]) => {
        const x0 = anchor === 'start' ? tx : tx - w
        return { x0, x1: x0 + w, y0: ty - 9, y1: ty + 2 }
      }
      const spot = spots.find((c) => clear(boxOf(c))) || spots[0]
      placed.push({ id: p.id, x: spot[0], y: spot[1], anchor: spot[2], box: boxOf(spot) })
    }
    return placed
  })
  const labelOf = (id) => labels.find((l) => l.id === id)

  const eduLabels = ['No diploma, vs natives with none', 'Diploma only, vs natives the same', 'No diploma, vs all natives']
  const eduLo = -16000
  const eduHi = 6000
  const ex = (v) => 250 + ((v - eduLo) / (eduHi - eduLo)) * 400
  const k = (v) => (v === 0 ? '0' : (v < 0 ? '−' : '+') + Math.abs(v / 1000) + 'k')
</script>

<section class="fig" id="skills">
  <div class="body">
    <p class="kicker">Adult ledger · CPS ASEC 2025 · native age mix</p>
    <h2>Schooling sets the sign</h2>
    <p class="lede">
      The {groups.length} birthplace groups in the screen, placed by the share of their working-age
      adults with a degree. The balance rises with schooling: Mexico sits at the bottom left, India at
      the top right. Groups that sit low for their schooling, such as Venezuela, pay less tax per degree.
    </p>
    <div class="controls" role="radiogroup" aria-label="Allocation">
      <label><input type="radio" bind:group={alloc} value="personal" /> Each adult’s own items</label>
      <label><input type="radio" bind:group={alloc} value="shared" /> Household costs shared</label>
    </div>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 420" role="img" aria-label="Net fiscal balance per adult against degree share, by birthplace">
      {#each [-10000, 0, 10000, 20000, 30000] as t}
        <line x1={left} x2={right} y1={y(t)} y2={y(t)} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.8 : 1} />
        <text class="faint num" x={left - 8} y={y(t) + 4} text-anchor="end" font-size="11">{k(t)}</text>
      {/each}
      {#each [0, 0.25, 0.5, 0.75, 1] as t}
        <text class="faint num" x={x(t)} y={bottom + 18} text-anchor="middle" font-size="11">{Math.round(t * 100)}%</text>
      {/each}
      <text class="faint it" x={right} y={bottom + 34} text-anchor="end" font-size="11.5">share of adults 25–64 with a bachelor’s degree or more</text>
      <text class="faint it" x={left} y={top - 6} font-size="11.5">net $ per adult a year, at the native age mix</text>

      {#each refs as r}
        <line x1={left} x2={right} y1={y(r[alloc].v)} y2={y(r[alloc].v)} stroke="#b9b5a8" stroke-dasharray="3 3" />
        <text class="muted it" x={left + 6} y={y(r[alloc].v) + (r.id === 'all_native' ? 13 : -5)} font-size="11">{r.name}</text>
      {/each}

      {#each groups as o}
        {@const v = o[alloc].v}
        {@const se = o[alloc].se}
        {@const mx = o.id === 'mexico_born'}
        <line x1={x(o.ba)} x2={x(o.ba)} y1={y(clamp(v - 1.96 * se))} y2={y(clamp(v + 1.96 * se))} stroke={mx ? '#ca7a5e' : '#d3cfc2'} />
        <circle cx={x(o.ba)} cy={y(v)} r={mx ? 5.5 : 4} fill={mx ? '#f2cabc' : '#bbd4ee'} stroke={mx ? '#ca7a5e' : '#5c97d2'} />
      {/each}
      {#each groups as o}
        {@const lab = labelOf(o.id)}
        {#if lab}
          <text class="halo" x={lab.x} y={lab.y} text-anchor={lab.anchor} font-size="11.5" font-weight={o.id === 'mexico_born' || o.id === 'india' ? 700 : 400}>{o.name}</text>
        {/if}
      {/each}
    </svg>
    </div>

    <h3>Inside one schooling level the sign can flip</h3>
    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 118" role="img" aria-label="Mexico-born against natives at the same schooling">
      <line x1={ex(0)} x2={ex(0)} y1="6" y2="96" stroke="#111" stroke-width="0.8" />
      {#each [-15000, -10000, -5000, 5000] as t}
        <text class="faint num" x={ex(t)} y="112" text-anchor="middle" font-size="11">{k(t)}</text>
      {/each}
      {#each education as row, i}
        {@const yy = 22 + i * 30}
        <text x="0" y={yy + 4} font-size="12.5">{eduLabels[i]}</text>
        {#if row.lo != null}
          <line x1={ex(row.lo)} x2={ex(row.hi)} y1={yy} y2={yy} stroke="#b9b5a8" stroke-width="1.2" />
        {/if}
        <circle cx={ex(row.v)} cy={yy} r="5" fill={row.v < 0 ? '#f2cabc' : '#bbd4ee'} stroke={row.v < 0 ? '#ca7a5e' : '#5c97d2'} />
        <text class="num" x={ex(row.v) + (row.v < -10000 ? -10 : 10)} y={yy + 4} text-anchor={row.v < -10000 ? 'end' : 'start'} font-size="11.5">{dollars(row.v)}</text>
      {/each}
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Balances are re-weighted to the native age mix, so an older group (the Philippines) is not
      penalised for its retirees. Whiskers are approximate 95% intervals; groups with few records carry
      long ones.
    </p>
    <p>
      Below the scatter: Mexico-born adults 25–64 against natives with the same schooling, household
      costs shared. Without a diploma they come out ahead; with a diploma only, behind. Against natives of
      every schooling level the gap is the whole composition.
    </p>
    <p>
      high_skill_origin_screen_2026_09_21: origin_screen_native_ages.csv and origin_screen.csv;
      education_origin_fiscal comparisons.csv. A different object from the complete account.
    </p>
  </aside>
</section>
