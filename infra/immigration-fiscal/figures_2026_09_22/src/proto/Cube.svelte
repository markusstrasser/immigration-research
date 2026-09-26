<script>
  import d from '../generated/proto_cube.json'

  /* ------------------------------------------------------------ the account, per specification ---- */
  // cost(x) = main + sum_i slope_i (x_i - mainAt_i), gated against the engine in proto/cube.cjs.
  // A derived dial sets its members to one share: slopes summed, the main case at their slope-weighted mean.
  const COMP = Object.fromEntries(d.composites.map((c) => [c.id, c]))
  const DIAL = Object.fromEntries([...d.dials, ...d.composites].map((x) => [x.id, x]))
  const members = (id) => (COMP[id] ? COMP[id].members : [id])
  const slope = (s, id) => members(id).reduce((t, k) => t + s.slope[k], 0)
  const mainAt = (s, id) => members(id).reduce((t, k) => t + s.slope[k] * s.mainAt[k], 0) / slope(s, id)

  // In cube coordinates u in [0, 1]^3 the cost is k0 + k . u.
  function linear(s, axes) {
    let k0 = s.main
    const k = axes.map((id) => {
      const [lo, hi] = DIAL[id].range
      k0 += slope(s, id) * (lo - mainAt(s, id))
      return slope(s, id) * (hi - lo)
    })
    return { k0, k }
  }
  const toU = (id, x) => (x - DIAL[id].range[0]) / (DIAL[id].range[1] - DIAL[id].range[0])
  const fromU = (id, u) => DIAL[id].range[0] + u * (DIAL[id].range[1] - DIAL[id].range[0])

  /* ------------------------------------------------------------ geometry ---------------------------- */
  const sub = (a, b) => [a[0] - b[0], a[1] - b[1], a[2] - b[2]]
  const addv = (a, b) => [a[0] + b[0], a[1] + b[1], a[2] + b[2]]
  const mul = (a, c) => [a[0] * c, a[1] * c, a[2] * c]
  const dot = (a, b) => a[0] * b[0] + a[1] * b[1] + a[2] * b[2]
  const cross = (a, b) => [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]]
  const lerp = (a, b, t) => addv(a, mul(sub(b, a), t))
  const mean = (ps) => mul(ps.reduce(addv, [0, 0, 0]), 1 / ps.length)
  const spanOf = (xs) => [Math.min(...xs), Math.max(...xs)]

  const V = [[0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]]
  const FACES = [[0, 3, 2, 1], [4, 5, 6, 7], [0, 1, 5, 4], [2, 3, 7, 6], [0, 4, 7, 3], [1, 2, 6, 5]]
  const NORMALS = [[0, 0, -1], [0, 0, 1], [0, -1, 0], [0, 1, 0], [-1, 0, 0], [1, 0, 0]]
  const EDGES = [[0, 1], [1, 2], [2, 3], [3, 0], [4, 5], [5, 6], [6, 7], [7, 4], [0, 4], [1, 5], [2, 6], [3, 7]]
  const EDGE_FACES = EDGES.map(([a, b]) => FACES.map((f, i) => [f, i]).filter(([f]) => f.includes(a) && f.includes(b)).map(([, i]) => i))

  function dedupe(ps) {
    const out = []
    for (const p of ps) if (!out.some((q) => Math.abs(q[0] - p[0]) + Math.abs(q[1] - p[1]) + Math.abs(q[2] - p[2]) < 1e-9)) out.push(p)
    return out
  }
  // Points on one plane with normal n, in order around their centre.
  function around(ps, n) {
    const c = mean(ps)
    const e1 = sub(ps[0], c)
    const e2 = cross(n, e1)
    return ps.map((p) => [p, Math.atan2(dot(sub(p, c), e2), dot(sub(p, c), e1))]).sort((a, b) => a[1] - b[1]).map((x) => x[0])
  }
  // The sheet where the cost is zero, cut to the cube.
  function sheet({ k0, k }) {
    const f = (u) => k0 + dot(k, u)
    const ps = []
    for (const [a, b] of EDGES) {
      const fa = f(V[a]), fb = f(V[b])
      if ((fa < 0) !== (fb < 0)) ps.push(lerp(V[a], V[b], fa / (fa - fb)))
    }
    const q = dedupe(ps)
    return q.length >= 3 ? around(q, k) : []
  }
  // Keep the part of a convex solid (a list of faces) where the cost is at most zero.
  function keepGain(faces, { k0, k }) {
    const g = (u) => k0 + dot(k, u)
    const out = [], cap = []
    for (const face of faces) {
      const kept = []
      for (let i = 0; i < face.length; i++) {
        const p = face[i], q = face[(i + 1) % face.length]
        const gp = g(p), gq = g(q)
        if (gp <= 0) kept.push(p)
        if ((gp <= 0) !== (gq <= 0)) {
          const x = lerp(p, q, gp / (gp - gq))
          kept.push(x)
          cap.push(x)
        }
      }
      if (kept.length >= 3) out.push(kept)
    }
    const c = dedupe(cap)
    if (c.length >= 3) out.push(around(c, k))
    return out
  }

  /* ------------------------------------------------------------ words for numbers ------------------- */
  const pctOne = (x) => { const v = 100 * x; return Math.abs(v) < 10 && Math.abs(v - Math.round(v)) > 0.05 ? v.toFixed(1) : String(Math.round(v)) }
  const pct = (r) => (pctOne(r[0]) === pctOne(r[1]) ? pctOne(r[0]) : pctOne(r[0]) + '–' + pctOne(r[1])) + '%'
  const times = (x) => Number(x.toFixed(2)) + '×'
  const fmt = (id, x) => (DIAL[id].unit === 'times' ? times(x) : pctOne(x) + '%')
  const bn = (r) => {
    const a = Math.round(Math.min(Math.abs(r[0]), Math.abs(r[1]))), b = Math.round(Math.max(Math.abs(r[0]), Math.abs(r[1])))
    return '$' + a + (a === b ? '' : '–' + b) + 'bn'
  }
  const mainRange = (id) => spanOf(d.specs.map((s) => mainAt(s, id)))

  /* ------------------------------------------------------------ two fixed views --------------------- */
  // The account is a straight-line sum of its assumptions, so the break-even is flat and one well-chosen
  // view shows all of it; turning the cube would add motion, not information.
  const low = d.specs[d.lowEnd]
  const VIEWS = [
    { id: 'split', axes: ['schools', 'others', 'gg'], yaw: -51, pitch: 24 },
    { id: 'measured', axes: ['benefits', 'services', 'taxes'], yaw: -42, pitch: 22, moves: true, labelAt: [0.08, 0.55, 0.97] },
  ]

  let cw = $state(640)
  const W = $derived(Math.max(400, Math.min(640, cw || 640)))
  const views = $derived(VIEWS.map((v) => draw(v, W)))

  function draw(v, W) {
    const S = 0.306 * W, CX = W / 2, CY = 0.37 * W - 10, H = 0.7 * W + (W < 560 ? 40 : 0)
    const rad = (x) => (x * Math.PI) / 180
    const cy = Math.cos(rad(v.yaw)), sy = Math.sin(rad(v.yaw)), cp = Math.cos(rad(v.pitch)), sp = Math.sin(rad(v.pitch))
    const P = (u) => {
      const x = u[0] - 0.5, y = u[1] - 0.5, z = u[2] - 0.5
      const x1 = x * cy - y * sy, y1 = x * sy + y * cy
      return [CX + S * x1, CY - S * (y1 * sp + z * cp), y1 * cp - z * sp]
    }
    const facing = (n) => (n[0] * sy + n[1] * cy) * cp - n[2] * sp < 0
    const pts = (poly) => poly.map((u) => P(u).slice(0, 2).map((q) => q.toFixed(1)).join(',')).join(' ')

    const lin = d.specs.map((s) => linear(s, v.axes))
    const sheets = lin.map(sheet)
    let faces = FACES.map((f) => f.map((i) => V[i]))
    for (const l of lin) {
      faces = keepGain(faces, l)
      if (!faces.length) break
    }
    const centre = faces.length ? mean(faces.flat()) : null
    const solid = faces
      .map((face) => {
        let n = [0, 0, 0]
        for (let i = 0; i < face.length; i++) {
          const p = face[i], q = face[(i + 1) % face.length]
          n = addv(n, [(p[1] - q[1]) * (p[2] + q[2]), (p[2] - q[2]) * (p[0] + q[0]), (p[0] - q[0]) * (p[1] + q[1])])
        }
        if (dot(n, sub(mean(face), centre)) < 0) n = mul(n, -1)
        return { points: pts(face), front: facing(n) }
      })
      .sort((a, b) => a.front - b.front)
    const frontFace = NORMALS.map(facing)
    const edges = EDGES.map(([a, b], i) => ({ a: P(V[a]), b: P(V[b]), front: EDGE_FACES[i].some((f) => frontFace[f]) }))

    // The main case: one dot per specification, one drop line to the floor.
    const mains = d.specs.map((s) => v.axes.map((id) => toU(id, mainAt(s, id))))
    const lowMain = v.axes.map((id) => toU(id, mainAt(low, id)))
    const m = P(lowMain)
    const mid = mean(mains)
    const top = Math.max(...mains.map((u) => u[2]))
    const drop = [P([mid[0], mid[1], top]), P([mid[0], mid[1], 0])]

    // Moves from the main case to the sheet, for the specification most favourable to the group. Each label
    // sits just past its end, along its own direction, so labels of moves that end close together fan out.
    const beyond = (from, to) => {
      const dx = to[0] - from[0], dy = to[1] - from[1], n = Math.hypot(dx, dy) || 1
      const ux = dx / n, uy = dy / n
      return { lx: to[0] + 9 * ux, ly: to[1] + 9 * uy + (uy > 0.3 ? 9 : uy < -0.3 ? -2 : 4),
        anchor: ux < -0.3 ? 'end' : ux > 0.3 ? 'start' : 'middle' }
    }
    const moves = []
    let diagonal = null
    if (v.moves) {
      const { k0, k } = linear(low, v.axes)
      for (const j of [0, 1, 2]) {
        const rest = k0 + [0, 1, 2].reduce((t, i) => (i === j ? t : t + k[i] * lowMain[i]), 0)
        const u = -rest / k[j]
        if (!(u >= 0 && u <= 1)) continue
        const to = [...lowMain]
        to[j] = u
        moves.push({ to: P(to), label: fmt(v.axes[j], fromU(v.axes[j], u)), ...beyond(m, P(to)) })
      }
      // Taxes up and benefits down by the same share, at once.
      const t = v.axes.indexOf('taxes'), b = v.axes.indexOf('benefits')
      if (t >= 0 && b >= 0) {
        const share = low.main / (slope(low, 'benefits') - slope(low, 'taxes'))
        const to = [...lowMain]
        to[t] = toU('taxes', 1 + share)
        to[b] = toU('benefits', 1 - share)
        diagonal = { to: P(to), label: `both ${Math.round(100 * share)}% off`, ...beyond(m, P(to)) }
      }
    }

    // Tick labels on the two floor edges nearest the reader and the leftmost upright edge.
    const center = P([0.5, 0.5, 0.5])
    const picks = []
    for (const j of [0, 1]) {
      let best = null
      for (const o of [0, 1]) {
        const a = [0, 0, 0], b = [0, 0, 0]
        a[1 - j] = b[1 - j] = o
        b[j] = 1
        const depth = P(lerp(a, b, 0.5))[2]
        if (!best || depth < best.depth) best = { j, a, b, depth }
      }
      picks.push(best)
    }
    let upright = null
    for (const [x, y] of [[0, 0], [1, 0], [0, 1], [1, 1]]) {
      const a = [x, y, 0], b = [x, y, 1]
      const sx = P(lerp(a, b, 0.5))[0]
      if (!upright || sx < upright.sx) upright = { j: 2, a, b, sx }
    }
    picks.push(upright)
    const fit = (t) => {
      const w = 6.3 * Math.max(t.label.length, 0.88 * t.what.length)
      const left = t.anchor === 'start' ? t.x : t.anchor === 'end' ? t.x - w : t.x - w / 2
      const shift = left < 4 ? 4 - left : left + w > W - 4 ? W - 4 - (left + w) : 0
      return { ...t, x: t.x + shift }
    }
    const placed = [], ticks = [], titles = []
    for (const { j, a, b } of picks) {
      const e = P(lerp(a, b, 0.5))
      let dx = j === 2 ? -1 : e[0] - center[0], dy = j === 2 ? 0 : e[1] - center[1]
      const len = Math.hypot(dx, dy) || 1
      dx /= len
      dy /= len
      const anchor = dx < -0.35 ? 'end' : dx > 0.35 ? 'start' : 'middle'
      for (const t of [0, 0.5, 1]) {
        const p = P(lerp(a, b, t))
        const x = p[0] + 11 * dx, y = p[1] + 11 * dy + (dy > 0.35 ? 8 : 4)
        if (placed.some((q) => Math.hypot(q[0] - x, q[1] - y) < 26)) continue
        placed.push([x, y])
        ticks.push({ x, y, anchor, text: fmt(v.axes[j], fromU(v.axes[j], t)) })
      }
      const D = DIAL[v.axes[j]]
      if (j === 2) {
        const tp = P(b)
        titles.push(fit({ x: tp[0], y: tp[1] - 30, anchor: 'middle', label: D.label, what: D.what }))
      } else {
        titles.push(fit({ x: e[0] + 40 * dx, y: e[1] + 40 * dy + (dy > 0.35 ? 10 : 0), anchor, label: D.label, what: D.what }))
      }
    }

    return {
      id: v.id, W, H, edges, solid, ticks, titles, m, drop, moves, diagonal,
      sheets: sheets.filter((s) => s.length).map(pts),
      lowSheet: sheets[d.lowEnd].length ? pts(sheets[d.lowEnd]) : null,
      highSheet: sheets[d.highEnd].length ? pts(sheets[d.highEnd]) : null,
      label: v.labelAt ? P(v.labelAt) : centre ? P(centre) : null,
      dots: mains.map(P),
    }
  }

  const w = d.wedge
  const ms = d.measured
</script>

<section class="fig" id="cube">
  <div class="body">
    <p class="kicker">Complete account · main case · three assumptions at once</p>
    <h2>Everyone else comes out ahead only where schools and the other services barely grow for them</h2>
    <p class="lede">
      Each drawing is a cube of three of the account’s assumptions, each running from its lowest setting to its
      highest; every other assumption stays at the main case. The cost to everyone else is a straight-line sum of the
      assumptions, so the settings where it is exactly zero form a flat sheet (ochre). On one side everyone else is
      worse off; on the other, shaded blue, they come out ahead. Because the sheet is flat, a fixed view shows all of
      it.
    </p>

    <div bind:clientWidth={cw}>
      {#each views as g}
        <p class="view">
          {#if g.id === 'split'}
            <b>Every public service budget, in three parts.</b> Schools, every other public service and general
            administration, each counted once. Taxes and benefits stay at what records show.
          {:else}
            <b>Taxes, benefits and every public service.</b> Taxes and benefits as multiples of what records show;
            general administration as in the main case.
          {/if}
        </p>
        <svg class="cube" viewBox="0 0 {g.W} {g.H}" role="img"
          aria-label={g.id === 'split'
            ? 'A cube of schools, every other public service and general administration, cut near one edge by the flat sheet where the cost to everyone else is zero'
            : 'A cube of taxes, benefits and every public service, cut diagonally by the flat sheet where the cost to everyone else is zero'}>
          <!-- Hidden edges first, faint. -->
          {#each g.edges.filter((e) => !e.front) as e}
            <line x1={e.a[0]} y1={e.a[1]} x2={e.b[0]} y2={e.b[1]} stroke="#dcd8c8" stroke-width="0.8" stroke-dasharray="3 3" />
          {/each}

          <!-- The break-even sheet of every specification, one even tint; the two ends outlined. -->
          <g opacity="0.55">
            {#each g.sheets as points}<polygon {points} fill="#ecdcae" />{/each}
          </g>
          {#if g.lowSheet}<polygon points={g.lowSheet} fill="none" stroke="#b8913a" stroke-width="0.8" />{/if}
          {#if g.highSheet}<polygon points={g.highSheet} fill="none" stroke="#b8913a" stroke-width="0.8" stroke-dasharray="1.5 2.5" />{/if}

          <!-- Where everyone else is better off under every specification. -->
          {#each g.solid as f}
            <polygon points={f.points} fill="#bbd4ee" fill-opacity={f.front ? 0.42 : 0.22} stroke="#5c97d2" stroke-width="0.7" stroke-linejoin="round" />
          {/each}
          {#if g.label}
            <text class="it halo" x={g.label[0]} y={g.label[1] + 4} text-anchor="middle" font-size="12.5" style="fill: #2f5f8f">better off</text>
          {/if}

          <!-- Moves from the main case to the sheet. -->
          {#each g.moves as r}
            <line x1={g.m[0]} y1={g.m[1]} x2={r.to[0]} y2={r.to[1]} stroke="#57544c" stroke-width="1" stroke-dasharray="1.5 3" />
            <circle cx={r.to[0]} cy={r.to[1]} r="2.6" fill="#fffff8" stroke="#57544c" stroke-width="1" />
            <text class="num halo muted" x={r.lx} y={r.ly} text-anchor={r.anchor} font-size="11">{r.label}</text>
          {/each}
          {#if g.diagonal}
            <line x1={g.m[0]} y1={g.m[1]} x2={g.diagonal.to[0]} y2={g.diagonal.to[1]} stroke="#111" stroke-width="1.1" stroke-dasharray="4 2.5" />
            <circle cx={g.diagonal.to[0]} cy={g.diagonal.to[1]} r="2.8" fill="#111" />
            <text class="num halo" x={g.diagonal.lx} y={g.diagonal.ly} text-anchor={g.diagonal.anchor} font-size="11">{g.diagonal.label}</text>
          {/if}

          <!-- The main case: a dot per specification and a drop line to the floor. -->
          <line x1={g.drop[0][0]} y1={g.drop[0][1]} x2={g.drop[1][0]} y2={g.drop[1][1]} stroke="#8d897e" stroke-width="0.8" stroke-dasharray="2 2.5" />
          <path d="M{g.drop[1][0] - 3},{g.drop[1][1]} h6 M{g.drop[1][0]},{g.drop[1][1] - 2} v4" stroke="#8d897e" stroke-width="0.8" />
          {#each g.dots as p}<circle cx={p[0]} cy={p[1]} r="1.9" fill="#111" />{/each}
          <text class="halo" x={g.m[0] + 9} y={g.m[1] + 16} font-size="12.5">main case</text>
          <text class="halo muted num" x={g.m[0] + 9} y={g.m[1] + 30} font-size="11">{bn(d.main)} worse off</text>

          <!-- Front edges and axis labels. -->
          {#each g.edges.filter((e) => e.front) as e}
            <line x1={e.a[0]} y1={e.a[1]} x2={e.b[0]} y2={e.b[1]} stroke="#b9b5a8" stroke-width="0.9" />
          {/each}
          {#each g.ticks as t}
            <text class="faint num halo" x={t.x} y={t.y} text-anchor={t.anchor} font-size="11">{t.text}</text>
          {/each}
          {#each g.titles as t}
            <text class="halo" x={t.x} y={t.y} text-anchor={t.anchor} font-size="12.5">{t.label}</text>
            <text class="faint it halo" x={t.x} y={t.y + 14} text-anchor={t.anchor} font-size="11">{t.what}</text>
          {/each}
        </svg>

        {#if g.id === 'split'}
          <p class="note">
            With every service budget frozen, everyone else is <span class="num">{bn(w.frozen)}</span> better off, and
            general administration alone never undoes that: charged in full it still leaves them
            <span class="num">{bn(w.adminFull)}</span> better off. The blue wedge ends where:
          </p>
          <table class="book wedge">
            <thead>
              <tr><th>General administration</th><th>Schools, other services frozen</th><th>Other services, schools frozen</th></tr>
            </thead>
            <tbody>
              <tr><td>frozen</td><td class="num">below {pct(w.floor.schools)}</td><td class="num">below {pct(w.floor.others)}</td></tr>
              <tr><td>charged in full</td><td class="num">below {pct(w.top.schools)}</td><td class="num">below {pct(w.top.others)}</td></tr>
            </tbody>
          </table>
          <p class="note">
            The main case charges schools <span class="num">{pct(mainRange('schools'))}</span> of per-pupil cost, every
            other public service <span class="num">{pct(mainRange('others'))}</span> on this axis and general
            administration <span class="num">{pct(mainRange('gg'))}</span>: <span class="num">{bn(d.main)}</span> a year
            worse off. With every budget growing in full it would be <span class="num">{bn(w.full)}</span>.
          </p>
        {:else}
          <p class="note">
            Taxes and benefits are each larger than the whole cost, so the blue side is large here; the question is how
            far the records would have to be off. From the main case, taxes alone would have to be
            <span class="num">{pct([ms.taxes[0] - 1, ms.taxes[1] - 1])}</span> above what records show, benefits alone
            <span class="num">{pct([1 - ms.benefits[1], 1 - ms.benefits[0]])}</span> below, or every public service would
            have to grow by less than <span class="num">{pct(d.servicesRoot)}</span> of its average cost. Moved together
            (the black dashes), taxes and benefits would each have to be <span class="num">{pct(d.together)}</span> off in
            the group’s favour.
          </p>
        {/if}
      {/each}
    </div>
  </div>

  <aside class="side">
    <p>
      Each cube spans every assumption’s whole range, not its likely range, so the size of the blue region is not a
      probability.
    </p>
    <p>
      The ochre band holds the break-even sheet of each of the main case’s {d.specs.length} specifications, drawn as one
      even tint: solid edge for the specification most favourable to the group, dotted for the least. Black dots: the
      main case under each specification. The moves are drawn for the one most favourable to the group
      (<span class="num">{bn([d.main[0], d.main[0]])}</span>).
    </p>
    <p>
      On a derived axis the main case sits at the one share that costs the same as its own mix: it charges colleges,
      police, health and welfare in full and roads not at all, which comes to
      <span class="num">{pct(mainRange('others'))}</span> of “every other public service”.
    </p>
    <p>
      “Every public service” sets schools, colleges, police, health, welfare, housing and roads to one share of their
      average cost, with general administration as in the main case. Here it turns at
      <span class="num">{pct(d.servicesRoot)}</span>; the staircase’s <span class="num">{pct(d.publishedBreakEven)}</span>
      also varies the model of the gain from their work.
    </p>
    <p>
      proto/cube.cjs; the drawing’s straight-line formula is gated against the engine at
      {d.gatePoints.toLocaleString('en-US')} random points, and the table’s thresholds are gated to fall inside the cube
      for every specification.
    </p>
  </aside>
</section>

<style>
  .cube { width: 100%; height: auto; display: block; }
  .view { max-width: 40rem; margin: 1.6rem 0 0; font-size: 0.95rem; color: var(--muted); }
  .view b { color: var(--ink); font-weight: 600; }
  .wedge { font-size: 0.88rem; margin: 0.4rem 0 0.2rem; }
  .note .num, .side .num, .wedge .num { white-space: nowrap; }
</style>
