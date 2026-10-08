<script>
  import data from '../generated/proto_dots.json'

  const steps = data.steps
  const N = steps.length
  const fams = data.families
  const mainK = steps.findIndex((s) => s.main)
  const main = steps[mainK]
  const SIDES = ['in', 'out']

  // Colour is the sign and only the sign (README, "Visual grammar"): a dot in the left heap leaves
  // everyone else better off (blue), one in the right heap worse off (orange); a dot below the line is
  // not counted (grey). Families are told apart by the seams between them and their labels.
  const SIGN = {
    in: { fill: '#bbd4ee', line: '#5c97d2' },
    out: { fill: '#f2cabc', line: '#ca7a5e' },
    pool: { fill: '#e4e1d6', line: '#57544c' },
  }
  // Labels for the narrow layout, where the label columns are short.
  const SHORT = {
    taxes: 'Taxes', gain: 'Their work', benefits: 'Benefits', education: 'Education',
    police: 'Police, courts', services: 'Health, welfare', admin: 'Administration', roads: 'Roads, parks',
  }
  const SHORT_PART = { hospital: 'Hospital care', schools: 'Schools', colleges: 'Colleges', health: 'Public health', welfare: 'Welfare offices' }
  const cap = (t) => t.charAt(0).toUpperCase() + t.slice(1)

  const onSide = { in: fams.filter((f) => f.side === 'in'), out: fams.filter((f) => f.side === 'out') }
  const heapN = (k, s) => onSide[s].reduce((t, f) => t + steps[k].fam[f.id].heap, 0)
  const poolN = (k, s) => onSide[s].reduce((t, f) => t + steps[k].fam[f.id].pool, 0)

  // Dots lifted off a heap at step k (in the heap at k - 1, gone at k), by side.
  const removed = steps.map((s, k) => {
    const out = { in: 0, out: 0 }
    if (k) for (const f of fams) {
      const was = steps[k - 1].fam[f.id], now = s.fam[f.id]
      out[f.side] += Math.max(0, was.heap - (now.heap + now.pool))
    }
    return out
  })

  // Every dot and its state at every step: in the heap, in the pool, lifted off by a correction at
  // this step (ghost), or gone. A family's dots are numbered; the lowest numbers sit in the heap.
  const maxT = Object.fromEntries(fams.map((f) => [f.id, Math.max(...steps.map((s) => s.fam[f.id].heap + s.fam[f.id].pool))]))
  const DOTS = []
  for (const f of fams) for (let i = 0; i < maxT[f.id]; i++) DOTS.push({ key: `${f.id}:${i}`, f: f.id, s: f.side, i, st: [] })
  for (let k = 0; k < N; k++) {
    const offH = { in: 0, out: 0 }, offP = { in: 0, out: 0 }, ghost = { in: 0, out: 0 }, start = {}
    for (const f of fams) {
      start[f.id] = { h: offH[f.side], p: offP[f.side] }
      offH[f.side] += steps[k].fam[f.id].heap
      offP[f.side] += steps[k].fam[f.id].pool
    }
    for (const d of DOTS) {
      const c = steps[k].fam[d.f]
      const prev = k ? d.st[k - 1] : null
      let st
      if (d.i < c.heap) st = { st: 'heap', i: start[d.f].h + d.i, n: heapN(k, d.s) }
      else if (d.i < c.heap + c.pool) st = { st: 'pool', j: start[d.f].p + d.i - c.heap }
      else if (prev && prev.st === 'heap') st = { st: 'ghost', g: ghost[d.s]++, n: heapN(k, d.s), m: removed[k][d.s] }
      else st = { st: 'gone' }
      st.fresh = st.st === 'heap' && !!prev && prev.st !== 'heap'
      d.st.push(st)
    }
  }

  // Each family's dots, as indices into DOTS.
  const BY_FAM = Object.fromEntries(fams.map((f) => [f.id, DOTS.map((d, n) => (d.f === f.id ? n : -1)).filter((n) => n >= 0)]))

  // Geometry. Heaps: rows packed like sand, filled from the outer edge, a seam every few dots and a
  // wider one under every hundred. The pool below the line is spread flat and wider, since nothing
  // is compared by its height. Wide: rows of 20, five rows to a hundred. Narrow: rows of 10.
  const GHOST = 4  // lifted-off dots float this many rows above their heap, clear of its total
  function layout(narrow) {
    const VW = narrow ? 380 : 760
    const W = narrow ? 10 : 20
    // Pool rows per side: the right pool spreads toward the middle, the left one (at most the gain
    // from their work) stays narrow enough that the two never meet.
    const PW = narrow ? { in: 8, out: 12 } : { in: W, out: 30 }
    const SEAM = narrow ? 5 : 10
    const BAND = 100 / W
    const P = 7.5, RH = (P * Math.sqrt(3)) / 2, R = 2.95, MG = 2.5, FG = 3.5
    const HW = W * P + (W / SEAM - 1) * MG + P / 2
    const LW = narrow ? { in: 84, out: 110 } : { in: 140, out: 200 }
    const X0 = { in: LW.in, out: VW - LW.out - HW }
    const outer = { in: X0.in, out: X0.out + HW }
    const bandPx = (rows) => rows * RH + Math.floor(rows / BAND) * FG
    const ghostRows = (k, s) => (removed[k][s] ? Math.ceil(removed[k][s] / W) + GHOST : 0)
    const maxRows = Math.max(...steps.flatMap((_, k) => SIDES.map((s) => Math.ceil(heapN(k, s) / W) + ghostRows(k, s))))
    const maxPoolRows = Math.max(...steps.flatMap((_, k) => SIDES.map((s) => Math.ceil(poolN(k, s) / PW[s]))))
    const top = narrow ? 58 : 48
    const ground = top + bandPx(maxRows) + 8
    const poolTop = ground + 9
    const height = poolTop + maxPoolRows * RH + 26

    const colX = (s, c, row) => {
      const d = P / 2 + c * P + Math.floor(c / SEAM) * MG + (row % 2 ? P / 2 : 0)
      return s === 'in' ? outer.in + d : outer.out - d
    }
    const rowY = (row) => ground - 4.5 - row * RH - Math.floor(row / BAND) * FG
    // n: slots in use; a partial top row is centred, so each heap ends in a small crest.
    function heapXY(s, i, n) {
      const row = Math.floor(i / W)
      const partial = n !== undefined && row === Math.floor((n - 1) / W) && n % W
      return [colX(s, (i % W) + (partial ? Math.floor((W - (n % W)) / 2) : 0), row), rowY(row)]
    }
    function poolXY(s, j) {
      const row = Math.floor(j / PW[s])
      return [colX(s, j % PW[s], row), poolTop + row * RH]
    }
    // The level of a heap holding n dots: the top edge of its dots, a partial row pro rata.
    const level = (n) => ground - 4.5 + RH / 2 - (n / W) * RH - Math.floor(n / (BAND * W)) * FG
    function heapTop(k, s) {
      const rows = Math.ceil(heapN(k, s) / W)
      return { rows, ghost: removed[k][s] ? { first: rows + GHOST, rows: Math.ceil(removed[k][s] / W) } : null }
    }
    // Every dot's place at every step; a gone dot stays where it last stood, and a dot that first
    // appears later waits, unseen, where it will first stand.
    const pos = DOTS.map((d) => {
      const at = []
      d.st.forEach((st, k) => {
        if (st.st === 'heap') at.push(heapXY(d.s, st.i, st.n))
        else if (st.st === 'pool') at.push(poolXY(d.s, st.j))
        else if (st.st === 'ghost') {
          const g0 = (Math.ceil(st.n / W) + GHOST) * W
          at.push(heapXY(d.s, g0 + st.g, g0 + st.m))
        } else at.push(k ? at[k - 1] : null)
      })
      const first = at.find(Boolean)
      return at.map((a) => a || first)
    })
    // Seams: the boundary between two families, as a path through the gaps between dots. A heap
    // family above slot b holds the rest of row b / W and every row above; a pool cluster from slot
    // j holds the rest of its row and every row below.
    function heapSeam(s, b, n) {
      const r = Math.floor(b / W), c = b % W, dir = s === 'in' ? 1 : -1
      const eOut = outer[s] - dir * 2, eIn = outer[s] + dir * (HW + 2)
      const below = (rowY(r - 1) + rowY(r)) / 2, above = (rowY(r) + rowY(r + 1)) / 2
      if (!c) return `M${eOut},${below} H${eIn}`
      const xc = (heapXY(s, b - 1, n)[0] + heapXY(s, b, n)[0]) / 2
      return `M${eIn},${below} H${xc} V${above} H${eOut}`
    }
    function poolSeam(s, j) {
      const r = Math.floor(j / PW[s]), c = j % PW[s], dir = s === 'in' ? 1 : -1
      const width = PW[s] * P + Math.floor((PW[s] - 1) / SEAM) * MG + P / 2
      const eOut = outer[s] - dir * 2, eIn = outer[s] + dir * (width + 2)
      const above = poolTop + (r - 0.5) * RH, below = poolTop + (r + 0.5) * RH
      if (!c) return `M${eOut},${above} H${eIn}`
      const xc = (poolXY(s, j - 1)[0] + poolXY(s, j)[0]) / 2
      return `M${eOut},${below} H${xc} V${above} H${eIn}`
    }
    return {
      narrow, VW, W, R, RH, HW, X0, outer, top, ground, poolTop, height, rowY, heapXY, poolXY, level, heapTop, pos,
      heapSeam, poolSeam,
      labelX: { in: X0.in - 10, out: X0.out + HW + 10 }, edgeX: { in: X0.in - 2, out: X0.out + HW + 2 },
      font: narrow ? 10.5 : 11.5, small: narrow ? 10 : 10.5,
      // How far the gap's words keep above the lower heap's level: in the narrow layout they reach over
      // that heap and must clear its total.
      clear: narrow ? 22 : 6,
    }
  }
  const WIDE = layout(false)
  const NARROW = layout(true)
  let cw = $state(0)
  const L = $derived(cw > 0 && cw < 600 ? NARROW : WIDE)

  let shown = $state(mainK)
  let from = $state(mainK)
  let playing = $state(false)
  let timer = null
  function go(k) {
    from = shown
    shown = Math.max(0, Math.min(N - 1, k))
  }
  function stop() {
    playing = false
    clearInterval(timer)
  }
  function play() {
    if (playing) return stop()
    playing = true
    go(0)
    timer = setInterval(() => (shown >= N - 1 ? stop() : go(shown + 1)), 1700)
  }

  // Dots that rise from the pool (or sink back) pour in order over 0.6 s; the rest move together.
  const delay = $derived.by(() => {
    const pos = L.pos
    const moving = DOTS.map((d, n) => ({ d, n })).filter(({ d }) => d.st[from].st !== d.st[shown].st &&
      (d.st[from].st === 'pool' || d.st[shown].st === 'pool'))
    const up = shown > from
    moving.sort((a, b) => (up ? pos[b.n][shown][1] - pos[a.n][shown][1] : pos[a.n][from][1] - pos[b.n][from][1]))
    const m = new Map(moving.map(({ d }, n) => [d.key, Math.round((n / Math.max(1, moving.length)) * 600)]))
    return (d) => m.get(d.key) || 0
  })

  const S = $derived(steps[shown])
  const prev = $derived(shown ? steps[shown - 1] : null)
  const name = (fid) => (L.narrow ? SHORT[fid] : fams.find((f) => f.id === fid).label)
  const partName = (pid) => (L.narrow ? SHORT_PART[pid] : cap(data.parts[pid].label))

  // Direct labels beside each layer, pushed apart where layers are thin.
  function spread(items, gap, lo, hi) {
    items.sort((a, b) => a.want - b.want)
    items.forEach((it, n) => (it.y = Math.max(it.want, n ? items[n - 1].y + gap : lo)))
    for (let n = items.length - 1; n >= 0; n--) items[n].y = Math.min(items[n].y, n < items.length - 1 ? items[n + 1].y - gap : hi)
    items.forEach((it, n) => (it.y = Math.max(it.y, n ? items[n - 1].y + gap : lo)))
    return items
  }
  const labels = $derived.by(() => {
    const out = []
    for (const s of SIDES) {
      let h = 0, p = 0
      const heap = [], pool = []
      for (const f of onSide[s]) {
        const c = S.fam[f.id]
        if (c.heap) {
          const a = L.heapXY(s, h)[1], b = L.heapXY(s, h + c.heap - 1)[1]
          heap.push({ key: f.id, s, n: c.heap, want: (a + b) / 2 + 4, mid: (a + b) / 2, name: name(f.id) })
        }
        if (c.pool) {
          const a = L.poolXY(s, p)[1], b = L.poolXY(s, p + c.pool - 1)[1]
          // Name the part when only one part of the family waits below the line.
          const waiting = Object.entries(c.parts).filter(([, v]) => v.pool > 0).map(([id]) => id)
          const nm = waiting.length === 1 && f.parts.length > 1 ? partName(waiting[0]) : name(f.id)
          pool.push({ key: f.id + ':pool', s, n: c.pool, want: (a + b) / 2 + 4, mid: (a + b) / 2, pool: true, name: nm })
        }
        h += c.heap
        p += c.pool
      }
      const t = L.heapTop(shown, s)
      if (t.ghost) {
        const mid = L.rowY(t.ghost.first + (t.ghost.rows - 1) / 2)
        heap.push({ key: s + ':ghost', s, n: removed[shown][s], want: mid + 4, mid, name: 'Lifted off', ghost: true })
      }
      out.push(...spread(heap, 13, L.top, L.ground - 10), ...spread(pool, 12.5, s === 'in' ? L.ground + 30 : L.poolTop + 4, L.height - 4))
    }
    return out
  })

  // Seams between neighbouring families in each heap and in the pool, at the shown step.
  const seams = $derived.by(() => {
    const out = []
    for (const s of SIDES) {
      const n = heapN(shown, s)
      let h = 0, p = 0, lastH = null, lastP = null
      for (const f of onSide[s]) {
        const c = S.fam[f.id]
        if (c.heap) {
          if (lastH) out.push({ key: `${s}:h:${f.id}`, d: L.heapSeam(s, h, n) })
          lastH = f.id
        }
        if (c.pool) {
          if (lastP) out.push({ key: `${s}:p:${f.id}`, d: L.poolSeam(s, p), pool: true })
          lastP = f.id
        }
        h += c.heap
        p += c.pool
      }
    }
    return out
  })

  // The gap between the heaps: a bracket from the lower heap's level to the higher one's.
  const gap = $derived.by(() => {
    const lo = S.dots.left, hi = S.dots.right
    const hiSide = hi >= lo ? 'out' : 'in'
    const yLo = L.level(Math.min(lo, hi)), yHi = L.level(Math.max(lo, hi))
    const x = hiSide === 'out' ? L.X0.out - 7 : L.X0.in + L.HW + 7
    return { hiSide, yLo, yHi, x, n: Math.abs(S.dots.gap) }
  })

  // Words. Every number is read from the JSON.
  const bn = (v) => '$' + Math.abs(v).toFixed(1) + 'bn'
  const pct = (v) => Math.round(v * 100) + '%'
  // What step k does to the dots: rise from the pool (a dial moved), or lifted off and added (a
  // correction changed the amounts). `stay`: parts whose dial moved but whose remainder stays below.
  function moved(k) {
    const s = steps[k], p = steps[k - 1]
    const rise = { in: 0, out: 0 }, lifted = { in: 0, out: 0 }, added = { in: 0, out: 0 }
    const stay = []
    for (const f of fams) {
      const a = p.fam[f.id], b = s.fam[f.id]
      if (b.heap + b.pool === a.heap + a.pool) {
        rise[f.side] += b.heap - a.heap
        for (const [id, v] of Object.entries(b.parts)) {
          const w = a.parts[id]
          if (v.heap + v.pool === w.heap + w.pool && v.heap > w.heap && v.pool > 0) stay.push({ part: id, n: v.pool })
        }
      } else {
        lifted[f.side] += Math.max(0, a.heap - (b.heap + b.pool))
        added[f.side] += Math.max(0, b.heap - a.heap)
      }
    }
    return { rise, lifted, added, stay }
  }
  const words = $derived.by(() => {
    const k = shown, s = S
    const out = []
    if (k === 0) {
      out.push(`Taxes they pay: ${s.fam.taxes.heap} dots. Benefits they receive: ${s.fam.benefits.heap} dots. Nothing else is counted yet.`)
    } else {
      const m = moved(k)
      if (m.rise.in) out.push(`${m.rise.in} dots rise from below the line into what they bring in.`)
      if (m.rise.out) out.push(`${m.rise.out} dots rise from below the line into what they draw.`)
      for (const st of m.stay) out.push(`The other ${st.n} dots of ${data.parts[st.part].label} stay below: that part of the budget does not grow for them.`)
      if (m.lifted.in) out.push(`Tax records lift ${m.lifted.in} dots off what they bring in: the group pays ${bn(prev.left - s.left)} less than the survey showed.`)
      if (m.lifted.out) out.push(`Records of benefits, tax credits and medical care lift ${m.lifted.out} dots off what they draw${m.added.out ? ` and add ${m.added.out}` : ''}: ${bn(prev.right - s.right)} less in all.`)
    }
    if (k && Math.sign(prev.cost) !== Math.sign(s.cost)) out.push('The balance tips at this step.')
    if (s.cost > 0) out.push(`What they draw exceeds what they bring in by ${s.dots.gap} dots: everyone else is ${bn(s.cost)} a year worse off.`)
    else out.push(`What they bring in exceeds what they draw by ${-s.dots.gap} dots: everyone else is ${bn(s.cost)} a year better off.`)
    return out.join(' ')
  })
  // The staircase's range at this step over the main case's 64 settings (positive = cost).
  function bandText(b) {
    const [lo, hi] = b.map(Math.round)
    const over = 'Over the account’s other open choices,'
    if (hi < 0) return `${over} everyone else is $${-hi}bn to $${-lo}bn a year better off at this step.`
    if (lo > 0) return `${over} everyone else is $${lo}bn to $${hi}bn a year worse off at this step.`
    return `${over} everyone else ends up anywhere from $${-lo}bn a year better off to $${hi}bn worse off at this step.`
  }
  const bandWords = $derived(bandText(S.band))

  // The notes.
  const sp = data.spec, other = data.otherEnd
  const schoolsMain = main.fam.education.parts.schools
  const adminMain = main.fam.admin.parts.admin
  const mismatch = steps.filter((s) => !s.dots.roundedMatch)
  const famLabel = Object.fromEntries(fams.map((f) => [f.id, f.label]))
  const ucK = steps.findIndex((s) => s.id === 'uc')
  const constantsWhat = data.constantsLabel.replace(/\s*\(.*\)$/, '').replace(/^./, (c) => c.toLowerCase())
  function title(fid) {
    const c = S.fam[fid]
    const parts = Object.entries(c.parts)
      .filter(([, v]) => v.full)
      .map(([id, v]) => `${data.parts[id].label} ${bn(v.counted)}${Math.abs(v.full - v.counted) > 0.05 ? ` of ${bn(v.full)}` : ''}`)
    return `${famLabel[fid]}: ${c.heap} dots counted, ${c.pool} not counted. ${parts.join('; ')}.`
  }
</script>

<section class="fig" id="dots">
  <div class="body">
    <p class="kicker">Prototype · heaps of dots · one setting of the main case</p>
    <h2>What they draw outweighs what they bring in by {main.dots.gap} dots of $1bn</h2>
    <p class="lede">
      Each dot is ${data.unitBn}bn a year. The left heap is what the Mexican-origin population brings in for
      everyone else: the taxes it pays that the account counts, and the gain from its work. The right
      heap is what it draws: its benefits, then, one at a time, the public services it uses, at the
      share of their cost that grows with the population. Below the line lie the dots the account
      assigns to the group but does not count. The difference between the heaps is what everyone else
      gains or loses.
    </p>

    <div class="slider">
      <span>Tally</span>
      <input type="range" min="0" max={N - 1} step="1" value={shown} list="dots-ticks"
        aria-label="Step through the account"
        oninput={(e) => { stop(); go(+e.currentTarget.value) }} />
      <span>Every service</span>
    </div>
    <datalist id="dots-ticks">
      {#each steps as _, k}<option value={k}></option>{/each}
    </datalist>
    <div class="steprow">
      <button class="link" onclick={() => { stop(); go(shown - 1) }} disabled={shown === 0}>← back</button>
      <button class="link" onclick={() => { stop(); go(shown + 1) }} disabled={shown === N - 1}>next →</button>
      <button class="link" onclick={play}>{playing ? 'stop' : 'pour from the tally'}</button>
      <button class="link" onclick={() => { stop(); go(mainK) }} disabled={shown === mainK}>main case</button>
    </div>
    <p class="caption" aria-live="polite">
      <span class="stepno num">Step {shown + 1} of {N}</span>
      <strong>{S.label}</strong>{#if S.note}{' · '}<span class="it">{S.note}</span>{/if}{#if S.main}{' · '}<span class="tag">the main case</span>{/if}{#if S.beyond}{' · '}<span class="tag">beyond the main case</span>{/if}<br />
      {words} <span class="muted">{bandWords}</span>
    </p>

    <div class="scroll" bind:clientWidth={cw}>
    <svg class={L.narrow ? '' : 'wide'} viewBox="0 0 {L.VW} {L.height}" role="img" aria-label="{S.label}. {words}">
      <!-- Headings over the heaps. -->
      <text x={L.X0.in + L.HW / 2} y="14" text-anchor="middle" font-size={L.narrow ? 12 : 13}>What they bring in</text>
      <text x={L.X0.out + L.HW / 2} y="14" text-anchor="middle" font-size={L.narrow ? 12 : 13}>What they draw</text>
      {#each SIDES as s}
        {@const way = s === 'in' ? 'better off' : 'worse off'}
        {#if L.narrow}
          <text class="muted it" x={L.X0[s] + L.HW / 2} y="29" text-anchor="middle" font-size={L.small}>each dot ${data.unitBn}bn</text>
          <text class="muted it" x={L.X0[s] + L.HW / 2} y="41" text-anchor="middle" font-size={L.small}>{way}</text>
        {:else}
          <text class="muted it" x={L.X0[s] + L.HW / 2} y="30" text-anchor="middle" font-size={L.small}>each dot: everyone else ${data.unitBn}bn {way}</text>
        {/if}
      {/each}

      <!-- The line: counted above, not counted below. -->
      <line x1="0" x2={L.VW} y1={L.ground} y2={L.ground} stroke="#111" stroke-width="0.8" />
      <text class="faint it" x="0" y={L.ground - 6} font-size={L.small}>counted ↑</text>
      <text class="faint it" x="0" y={L.ground + 15} font-size={L.small}>not counted ↓</text>

      <!-- The dots. -->
      {#each fams as f (f.id)}
        <g>
          <title>{title(f.id)}</title>
          {#each BY_FAM[f.id] as n (DOTS[n].key)}
            {@const d = DOTS[n]}
            {@const a = d.st[shown]}
            {@const xy = L.pos[n][shown]}
            {@const c = a.st === 'pool' ? SIGN.pool : SIGN[d.s]}
            <circle
              class="dot {a.st}"
              class:fresh={a.fresh}
              r={L.R}
              fill={a.fresh ? c.line : c.fill}
              stroke={c.line}
              style:transform="translate({xy[0]}px, {xy[1]}px)"
              style:transition-delay="{delay(d)}ms"
            />
          {/each}
        </g>
      {/each}

      <!-- Seams between families. -->
      {#key shown}
        <g class="seams">
          {#each seams as sm (sm.key)}
            <path d={sm.d} fill="none" stroke="#fffff8" stroke-width="3" stroke-linejoin="miter" />
          {/each}
        </g>
      {/key}

      <!-- The gap. -->
      {#if gap.n}
        {@const g = gap}
        {@const tx = g.hiSide === 'out' ? g.x - 7 : g.x + 7}
        {@const anchor = g.hiSide === 'out' ? 'end' : 'start'}
        <!-- The number and its two words sit beside the bracket, or above it when the gap is short. -->
        {@const base = g.yLo - L.clear - g.yHi >= 38 ? Math.min((g.yLo + g.yHi) / 2 + 16, g.yLo - L.clear) : g.yHi - 5}
        <line x1={g.hiSide === 'out' ? L.X0.in + L.HW : L.X0.out} x2={g.x} y1={g.yLo} y2={g.yLo} stroke="#57544c" stroke-width="0.8" stroke-dasharray="2 2" />
        <line x1={g.x} x2={g.x} y1={g.yLo} y2={g.yHi} stroke="#111" stroke-width="1" />
        <line x1={g.x - 3} x2={g.x + 3} y1={g.yHi} y2={g.yHi} stroke="#111" stroke-width="1" />
        <line x1={g.x - 3} x2={g.x + 3} y1={g.yLo} y2={g.yLo} stroke="#111" stroke-width="1" />
        <text class="num halo" x={tx} y={base - 25} text-anchor={anchor} font-size="15" font-weight="700">{g.n}</text>
        <text class="muted it halo" x={tx} y={base - 12} text-anchor={anchor} font-size={L.small}>everyone else</text>
        <text class="muted it halo" x={tx} y={base} text-anchor={anchor} font-size={L.small}>{S.cost > 0 ? 'worse off' : 'better off'}</text>
      {/if}

      <!-- Totals on top of each heap. -->
      {#each SIDES as s}
        {@const n = s === 'in' ? S.dots.left : S.dots.right}
        {@const t = L.heapTop(shown, s)}
        <text class="num" x={L.X0[s] + L.HW / 2} y={L.rowY(t.rows - 1) - L.RH / 2 - 7} text-anchor="middle" font-size="12.5" font-weight="700">{n}</text>
      {/each}

      <!-- Direct labels. -->
      {#each labels as l (l.key)}
        {@const ex = L.edgeX[l.s]}
        {@const lx = L.labelX[l.s]}
        {@const dir = l.s === 'in' ? -1 : 1}
        <polyline points="{ex},{l.mid} {ex + dir * 3},{l.mid} {lx - dir * 3},{l.y - 4}" fill="none" stroke="#dcd8c8" stroke-width="0.8" />
        <text x={lx} y={l.y} text-anchor={l.s === 'in' ? 'end' : 'start'} font-size={l.pool || l.ghost ? L.small : L.font}
          class={l.pool ? 'faint it' : l.ghost ? 'muted it' : ''}>
          {l.name}<tspan class={l.pool ? 'faint num' : 'muted num'} dx="4">{l.n}</tspan>
        </text>
      {/each}
    </svg>
    </div>

    <p class="note">
      Blue dots leave everyone else better off, orange dots worse off; grey dots below the line are
      not counted, and dark dots are the ones this step adds. The heaps use one setting of the account’s open choices,
      the one most favourable to the group: taxes and benefits pooled within each household, the gain from
      their work scaled to national output, schools {pct(sp.share)} of education spending with
      {pct(sp.school)} of the cost per pupil growing with enrollment, {pct(sp.gg)} of general
      administration growing with the population, and the lower of two estimates of unpaid hospital
      care. At the other end of the main case everyone else is {bn(other.mainCost)} worse off. Each part is rounded to
      whole dots; the gap in dots is within {data.maxDotError.toFixed(2)} of the exact figure{#if mismatch.length}, and
      matches it to the nearest billion at every step but {mismatch.map((s) => s.label.toLowerCase()).join(', ')}{/if}.
    </p>
  </div>

  <aside class="side">
    <p>
      Below the line sit the costs the account assigns to the group at the average cost per person but
      does not count, because that part of the budget does not grow for them. In the main case these are
      {pct(1 - sp.school)} of school costs ({bn(schoolsMain.full - schoolsMain.counted)}), roads, transport
      and parks ({bn(main.fam.roads.full)}) and {pct(1 - sp.gg)} of general administration
      ({bn(adminMain.full - adminMain.counted)}).
    </p>
    <p>
      Not drawn, because no step counts them: defense ({bn(data.never.defense)} at a per-head share),
      interest on existing debt ({bn(data.never.interest)}) and business subsidies
      ({bn(data.never.subsidies)}). Charging them per head would assume they grow with the population;
      the account holds that they do not. Corporate, property and asset taxes assigned to the group
      ({bn(data.never.corporateProperty)}) are not counted as revenue, because the gain from their work
      already counts that income.
    </p>
    <p>
      Benefits include unpaid hospital care from step {ucK + 1}. From the corrections on they are also
      {bn(main.constants)} {main.constants < 0 ? 'lower' : 'higher'}: the net of the corrections for
      {constantsWhat}.
    </p>
    <p>
      proto/dots.cjs rebuilds the engine state of account_sept24.cjs for every step at spec {sp.index} of {data.specCount}
      and reads every line; its gates check each step against cost(), each layer against cost() with
      only its own dial moved, and the main-case step against the band’s low end,
      {bn(sp.mainCost)} worse off.
    </p>
  </aside>
</section>

<style>
  .dot {
    stroke-width: 0.7;
    transition:
      transform 0.9s cubic-bezier(0.4, 0, 0.2, 1),
      opacity 0.5s,
      fill-opacity 0.5s,
      stroke-opacity 0.5s,
      fill 0.5s;
  }
  .dot.pool { fill-opacity: 0.8; stroke-opacity: 0.4; }
  .seams { animation: seam-in 0.4s 0.8s both; }
  @keyframes seam-in { from { opacity: 0; } to { opacity: 1; } }
  .dot.ghost { fill-opacity: 0; stroke-opacity: 0.9; }
  .dot.gone { opacity: 0; }
  .dot.fresh { fill-opacity: 0.9; }
  @media (prefers-reduced-motion: reduce) {
    .dot { transition: none; }
    .seams { animation: none; }
  }
  .steprow {
    display: flex;
    flex-wrap: wrap;
    gap: 0.2rem 1.2rem;
    font-size: 0.92rem;
    margin: -0.2rem 0 0.4rem;
  }
  button.link {
    font: inherit;
    color: var(--muted);
    background: none;
    border: 0;
    padding: 0;
    cursor: pointer;
    text-decoration: underline;
    text-decoration-color: var(--faint);
    text-underline-offset: 0.18em;
  }
  button.link:disabled { color: var(--faint); text-decoration: none; cursor: default; }
  .caption {
    font-size: 0.95rem;
    max-width: 40rem;
    min-height: 4.6em;
    margin: 0 0 0.6rem;
  }
  .caption .stepno { color: var(--faint); margin-right: 0.6rem; font-size: 0.85rem; }
  .caption strong { font-weight: 700; }
  .caption .it, .caption .tag { font-style: italic; color: var(--muted); }
  .caption .muted { color: var(--muted); }
</style>
