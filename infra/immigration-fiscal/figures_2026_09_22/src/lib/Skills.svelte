<script>
  import fig from '../generated/figures.json'

  const education = fig.education

  const usd = (v) => '$' + Math.abs(Math.round(v)).toLocaleString('en-US')

  let alloc = $state('personal')

  const left = 70
  const right = 700
  const top = 20
  const bottom = 380
  const yLo = -12000
  const yHi = 50000
  const x = (share) => left + share * (right - left)
  const y = (v) => top + ((yHi - v) / (yHi - yLo)) * (bottom - top)
  const clamp = (v) => Math.max(yLo, Math.min(yHi, v))

  const groups = fig.origins.filter((o) => !o.reference)
  const refs = fig.origins.filter((o) => o.reference)

  // Label placement: try spots around each dot, keep the first that clears every dot and every
  // label already placed. When none does, take the spot, out to two lines away, that overlaps them
  // least; a spot away from the dot counts as a small overlap of its own and gets a leader. Mexico and
  // India go first so they keep the plain right-hand spot.
  let labels = $derived.by(() => {
    const pts = groups.map((o) => ({ id: o.id, name: o.name, cx: x(o.ba), cy: y(o[alloc].v) }))
    const dots = pts.map((p) => ({ x0: p.cx - 5, x1: p.cx + 5, y0: p.cy - 5, y1: p.cy + 5 }))
    const first = ['mexico_born', 'india']
    const order = pts.slice().sort((a, b) => (first.includes(b.id) ? 1 : 0) - (first.includes(a.id) ? 1 : 0) || a.cx - b.cx)
    const placed = []
    const overlap = (b, o) => Math.max(0, Math.min(b.x1, o.x1) - Math.max(b.x0, o.x0)) * Math.max(0, Math.min(b.y1, o.y1) - Math.max(b.y0, o.y0))
    for (const p of order) {
      const w = p.name.length * 6.1 + 2
      const spots = [
        [8, 4, 'start'], [-8, 4, 'end'], [6, -8, 'start'], [6, 16, 'start'], [-6, -8, 'end'], [-6, 16, 'end'],
        [8, -19, 'start'], [8, 27, 'start'], [-8, -19, 'end'], [-8, 27, 'end'],
        [8, -30, 'start'], [8, 38, 'start'], [-8, -30, 'end'], [-8, 38, 'end'],
      ].map(([dx, dy, anchor]) => ({ x: p.cx + dx, y: p.cy + dy, anchor, far: Math.abs(dy) > 16 }))
      const boxOf = (s) => {
        const x0 = s.anchor === 'start' ? s.x : s.x - w
        return { x0, x1: x0 + w, y0: s.y - 9, y1: s.y + 2 }
      }
      const covered = (b) => [...dots, ...placed.map((l) => l.box)].reduce((t, o) => t + overlap(b, o), 0)
      const outside = (b) => b.x0 < left || b.x1 > 760 || b.y0 < top || b.y1 > bottom
      const score = (s) => covered(boxOf(s)) + (s.far ? 20 : 0) + (outside(boxOf(s)) ? 1e6 : 0)
      const spot = spots.slice(0, 8).find((s) => covered(boxOf(s)) === 0) || spots.reduce((a, s) => (score(s) < score(a) ? s : a))
      placed.push({ id: p.id, ...spot, cx: p.cx, cy: p.cy, box: boxOf(spot) })
    }
    return placed
  })
  const labelOf = (id) => labels.find((l) => l.id === id)

  const eduLabels = ['No diploma, vs natives with none', 'Diploma only, vs natives the same', 'No diploma, vs all natives']
  const eduLo = -18000
  const eduHi = 6000
  // Gap against natives, drawn so that falling below them runs to the right.
  const ex = (v) => 250 + ((eduHi - v) / (eduHi - eduLo)) * 400
  const k = (v) => (v === 0 ? '0' : Math.abs(v / 1000) + 'k')
  const eduTop = 18
  const ey = (i) => eduTop + 16 + i * 30
  // A row's label sits beyond the far end of its interval, away from the zero line.
  function eduLabel(row) {
    const ends = [row.v, row.lo, row.hi].filter((v) => v != null).map(ex)
    return row.v < 0
      ? { x: Math.max(...ends) + 9, anchor: 'start', text: 'below' }
      : { x: Math.min(...ends) - 9, anchor: 'end', text: 'above' }
  }
</script>

<section class="fig" id="skills">
  <div class="body">
    <p class="kicker">Adult ledger · CPS ASEC 2025 · native age mix</p>
    <h2>Schooling decides which groups pay in more than they receive</h2>
    <p class="lede">
      The {groups.length} birthplace groups in the screen, placed by the share of their working-age
      adults with a degree. The balance rises with schooling: Mexico sits at the bottom left, India at
      the far right. Groups that sit low for their schooling, such as Venezuela, pay less tax per degree.
    </p>
    <div class="controls" role="radiogroup" aria-label="Allocation">
      <label><input type="radio" bind:group={alloc} value="personal" /> Each adult’s own items</label>
      <label><input type="radio" bind:group={alloc} value="shared" /> Household costs shared</label>
    </div>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 420" role="img" aria-label="Net fiscal balance per adult against degree share, by birthplace">
      {#each [-10000, 0, 10000, 20000, 30000, 40000, 50000] as t}
        <line x1={left} x2={right} y1={y(t)} y2={y(t)} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.8 : 1} />
        <text class="faint num" x={left - 8} y={y(t) + 4} text-anchor="end" font-size="11">{k(t)}</text>
      {/each}
      <text class="faint it" x={left + 6} y={y(50000) + 14} font-size="11">↑ pays in more than it receives</text>
      <text class="faint it" x={right} y={y(-10000) + 14} text-anchor="end" font-size="11">↓ receives more than it pays in</text>
      {#each [0, 0.25, 0.5, 0.75, 1] as t}
        <text class="faint num" x={x(t)} y={bottom + 18} text-anchor="middle" font-size="11">{Math.round(t * 100)}%</text>
      {/each}
      <text class="faint it" x={right} y={bottom + 34} text-anchor="end" font-size="11.5">share of adults 25–64 with a bachelor’s degree or more</text>
      <text class="faint it" x={left} y={top - 6} font-size="11.5">net $ per adult a year, at the native age mix</text>

      {#each refs as r}
        <line x1={left} x2={right} y1={y(r[alloc].v)} y2={y(r[alloc].v)} stroke="#b9b5a8" stroke-dasharray="3 3" />
        <text class="muted it" x={left + 6} y={y(r[alloc].v) + (r.id === 'all_native' ? 13 : -5)} font-size="11">{r.name}</text>
      {/each}

      <!-- People are not coloured: Mexico is the filled ink mark, the other birthplaces grey open marks. -->
      {#each groups as o}
        {@const v = o[alloc].v}
        {@const se = o[alloc].se}
        {@const mx = o.id === 'mexico_born'}
        {@const ends = [v - 1.96 * se, v + 1.96 * se]}
        <line x1={x(o.ba)} x2={x(o.ba)} y1={y(clamp(ends[0]))} y2={y(clamp(ends[1]))} stroke={mx ? '#111' : '#d3cfc2'} />
        <!-- A whisker cut at the axis ends in an arrowhead: its interval runs on past the scale. -->
        {#each [[ends[1] > yHi, yHi, 1], [ends[0] < yLo, yLo, -1]] as [cut, at, dir]}
          {#if cut}
            <path d="M {x(o.ba) - 3.5} {y(at) + 5 * dir} L {x(o.ba)} {y(at)} L {x(o.ba) + 3.5} {y(at) + 5 * dir}" fill="none" stroke={mx ? '#111' : '#8d897e'} stroke-width="1" />
          {/if}
        {/each}
        <circle cx={x(o.ba)} cy={y(v)} r={mx ? 5.5 : 4} fill={mx ? '#111' : '#fffff8'} stroke={mx ? '#111' : '#8d897e'} stroke-width={mx ? 1 : 1.2} />
      {/each}
      {#each groups as o}
        {@const lab = labelOf(o.id)}
        {#if lab}
          {#if lab.far}
            <line x1={lab.cx} y1={lab.cy + (lab.y < lab.cy ? -5 : 5)} x2={lab.x} y2={lab.y < lab.cy ? lab.y + 3 : lab.y - 10} stroke="#b9b5a8" stroke-width="0.7" />
          {/if}
          <text class="halo" x={lab.x} y={lab.y} text-anchor={lab.anchor} font-size="11.5" font-weight={o.id === 'mexico_born' || o.id === 'india' ? 700 : 400}>{o.name}</text>
        {/if}
      {/each}
    </svg>
    </div>

    <h3>Inside one schooling level the gap can reverse</h3>
    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 {ey(education.length - 1) + 36}" role="img" aria-label="Mexico-born against natives at the same schooling">
      <text class="faint it" x={ex(0)} y={eduTop - 6} text-anchor="middle" font-size="11">same as natives</text>
      <line x1={ex(0)} x2={ex(0)} y1={eduTop} y2={ey(education.length - 1) + 14} stroke="#111" stroke-width="0.8" />
      {#each [5000, 0, -5000, -10000, -15000] as t}
        <text class="faint num" x={ex(t)} y={ey(education.length - 1) + 30} text-anchor="middle" font-size="11">{k(t)}</text>
      {/each}
      <text class="faint it" x={ex(eduHi) - 10} y={ey(education.length - 1) + 30} text-anchor="end" font-size="11">← above natives</text>
      <text class="faint it" x={ex(eduLo) + 10} y={ey(education.length - 1) + 30} font-size="11">below natives →</text>
      {#each education as row, i}
        {@const yy = ey(i)}
        {@const lab = eduLabel(row)}
        <text x="0" y={yy + 4} font-size="12.5">{eduLabels[i]}</text>
        {#if row.lo != null}
          <line x1={ex(row.lo)} x2={ex(row.hi)} y1={yy} y2={yy} stroke="#b9b5a8" stroke-width="1.2" />
        {/if}
        <circle cx={ex(row.v)} cy={yy} r="5" fill="#111" />
        <text x={lab.x} y={yy + 4} text-anchor={lab.anchor} font-size="11.5"><tspan class="num">{usd(row.v)}</tspan>&nbsp;{lab.text}</text>
      {/each}
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Balances are re-weighted to the native age mix, so an older group (the Philippines) is not
      penalised for its retirees. Whiskers are approximate 95% intervals; groups with few records carry
      long ones. An arrowhead marks a whisker that runs past the scale.
    </p>
    <p>
      Below the scatter: Mexico-born adults 25–64 against natives with the same schooling, household
      costs shared. Without a diploma they come out ahead; with a diploma only, behind. Against natives of
      every schooling level the gap is the whole composition.
    </p>
    <p>
      Taxes include the income tax the survey misses, keyed as the main case keys it (item T).
    </p>
    <p>
      high_skill_origin_screen_2026_09_21: origin_screen_native_ages.csv and origin_screen.csv;
      education_origin_fiscal_2026_09_19 comparisons.csv. A different object from the complete account.
    </p>
  </aside>
</section>
