<script>
  import { onMount } from 'svelte'
  import d from '../generated/proto_cube.json'

  /* ------------------------------------------------------------ the account, per specification ---- */
  // cost(x) = main + sum_i slope_i (x_i - mainAt_i), gated against the engine in proto/cube.cjs.
  // A derived dial sets its members to one share: slopes summed, the main case at their slope-weighted mean.
  const COMP = Object.fromEntries(d.composites.map((c) => [c.id, c]))
  const DIAL = Object.fromEntries([...d.dials, ...d.composites].map((x) => [x.id, x]))
  const OPTIONS = [...d.composites, ...d.dials]
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

  /* ------------------------------------------------------------ state ------------------------------- */
  // Default: every public service budget in three parts, each counted once; taxes and benefits at records.
  let axes = $state(['schools', 'others', 'gg']) // floor, floor, up
  let yaw = $state(-51)
  let pitch = $state(24)

  // An assumption can sit on one axis only, and a derived dial cannot share the cube with its parts.
  const taken = (id, j) => axes.some((a, i) => i !== j && members(a).some((k) => members(id).includes(k)))

  const low = d.specs[d.lowEnd]
  const lin = $derived(d.specs.map((s) => linear(s, axes)))
  const sheets = $derived(lin.map(sheet))
  const gainAll = $derived.by(() => {
    let faces = FACES.map((f) => f.map((i) => V[i]))
    for (const l of lin) {
      faces = keepGain(faces, l)
      if (!faces.length) break
    }
    return faces
  })
  const anyGain = $derived(lin.some(({ k0, k }) => V.some((u) => k0 + dot(k, u) < 0)))
  const mains = $derived(d.specs.map((s) => axes.map((id) => toU(id, mainAt(s, id)))))
  const lowMain = $derived(axes.map((id) => toU(id, mainAt(low, id))))

  // From the main case, one axis at a time, where the sheet is crossed (for every specification).
  const alone = $derived(
    axes.map((id, j) => {
      const D = DIAL[id]
      const ends = d.specs.map((s) => {
        const a = slope(s, id), m = mainAt(s, id)
        const end = a > 0 ? D.range[0] : D.range[1]
        return { root: m - s.main / a, atEnd: s.main + a * (end - m), end }
      })
      const all = ends.every((e) => e.atEnd < 0), none = ends.every((e) => e.atEnd >= 0)
      const roots = ends.map((e) => e.root)
      return { id, D, all, none, roots: [Math.min(...roots), Math.max(...roots)], atEnd: [Math.min(...ends.map((e) => e.atEnd)), Math.max(...ends.map((e) => e.atEnd))], end: ends[0].end, j }
    }),
  )
  // The low-end specification's moves, drawn as rays from its main point.
  const rays = $derived.by(() => {
    const { k0, k } = linear(low, axes)
    return [0, 1, 2].map((j) => {
      const rest = k0 + [0, 1, 2].reduce((t, i) => (i === j ? t : t + k[i] * lowMain[i]), 0)
      const u = -rest / k[j]
      if (!(u >= 0 && u <= 1)) return null
      const to = [...lowMain]
      to[j] = u
      return { j, to, value: fromU(axes[j], u) }
    }).filter(Boolean)
  })

  /* ------------------------------------------------------------ projection -------------------------- */
  // The drawing takes the container's width (400–640 units), so labels keep their size on a phone.
  let cw = $state(640)
  const W = $derived(Math.max(400, Math.min(640, cw || 640)))
  const S = $derived(0.306 * W)
  const CX = $derived(W / 2)
  const CY = $derived(0.37 * W + 26)
  const H = $derived(0.75 * W + (W < 560 ? 40 : 0))
  const rad = (x) => (x * Math.PI) / 180
  const cam = $derived({ cy: Math.cos(rad(yaw)), sy: Math.sin(rad(yaw)), cp: Math.cos(rad(pitch)), sp: Math.sin(rad(pitch)) })
  function P(u) {
    const x = u[0] - 0.5, y = u[1] - 0.5, z = u[2] - 0.5
    const x1 = x * cam.cy - y * cam.sy, y1 = x * cam.sy + y * cam.cy
    return [CX + S * x1, CY - S * (y1 * cam.sp + z * cam.cp), y1 * cam.cp - z * cam.sp]
  }
  const facing = (n) => (n[0] * cam.sy + n[1] * cam.cy) * cam.cp - n[2] * cam.sp < 0
  const pts = (poly) => poly.map((u) => P(u).slice(0, 2).map((v) => v.toFixed(1)).join(',')).join(' ')

  const frontFace = $derived(NORMALS.map(facing))
  const edges = $derived(EDGES.map(([a, b], i) => ({ a: P(V[a]), b: P(V[b]), front: EDGE_FACES[i].some((f) => frontFace[f]) })))

  // Faces of the solid where everyone else is better off under every specification: back ones first.
  const solid = $derived.by(() => {
    if (!gainAll.length) return []
    const c = mean(gainAll.flat())
    return gainAll
      .map((face) => {
        let n = [0, 0, 0]
        for (let i = 0; i < face.length; i++) {
          const p = face[i], q = face[(i + 1) % face.length]
          n = addv(n, [(p[1] - q[1]) * (p[2] + q[2]), (p[2] - q[2]) * (p[0] + q[0]), (p[0] - q[0]) * (p[1] + q[1])])
        }
        if (dot(n, sub(mean(face), c)) < 0) n = mul(n, -1)
        return { face, front: facing(n) }
      })
      .sort((a, b) => a.front - b.front)
  })
  const solidLabel = $derived(gainAll.length ? P(mean(gainAll.flat())) : null)
  const m = $derived(P(lowMain))
  // One drop line from the highest main point to the floor, at the specifications' mean floor position.
  const tops = $derived.by(() => {
    const x = mean(mains)
    const top = Math.max(...mains.map((u) => u[2]))
    return [[P([x[0], x[1], top]), P([x[0], x[1], 0])]]
  })

  /* Tick labels on the front edges: two floor edges nearest the reader, the leftmost upright edge. */
  const fmt = (id, x) => {
    const D = DIAL[id]
    return D.unit === 'times' ? Number(x.toFixed(2)) + '×' : Math.round(100 * x) + '%'
  }
  const center = $derived(P([0.5, 0.5, 0.5]))
  // Keep a two-line title inside the frame (about 6.3 units a character at 12.5).
  function fit(t) {
    const w = 6.3 * Math.max(t.label.length, 0.88 * t.what.length)
    const left = t.anchor === 'start' ? t.x : t.anchor === 'end' ? t.x - w : t.x - w / 2
    const shift = left < 4 ? 4 - left : left + w > W - 4 ? W - 4 - (left + w) : 0
    return { ...t, x: t.x + shift }
  }
  const axisEdges = $derived.by(() => {
    const out = []
    for (const j of [0, 1]) {
      const o = 1 - j
      let best = null
      for (const v of [0, 1]) {
        const a = [0, 0, 0], b = [0, 0, 0]
        a[o] = b[o] = v
        b[j] = 1
        const depth = P(lerp(a, b, 0.5))[2]
        if (!best || depth < best.depth) best = { a, b, depth }
      }
      out.push({ j, ...best })
    }
    let best = null
    for (const [x, y] of [[0, 0], [1, 0], [0, 1], [1, 1]]) {
      const a = [x, y, 0], b = [x, y, 1]
      const sx = P(lerp(a, b, 0.5))[0]
      if (!best || sx < best.sx) best = { a, b, sx }
    }
    out.push({ j: 2, ...best })
    return out
  })
  const labels = $derived.by(() => {
    const placed = []
    const out = { ticks: [], titles: [] }
    for (const { j, a, b } of axisEdges) {
      const mid = P(lerp(a, b, 0.5))
      let dx = mid[0] - center[0], dy = mid[1] - center[1]
      if (j === 2) { dx = -1; dy = 0 }
      const len = Math.hypot(dx, dy) || 1
      dx /= len; dy /= len
      const anchor = dx < -0.35 ? 'end' : dx > 0.35 ? 'start' : 'middle'
      for (const t of [0, 0.5, 1]) {
        const p = P(lerp(a, b, t))
        const x = p[0] + 11 * dx, y = p[1] + 11 * dy + (dy > 0.35 ? 8 : 4)
        if (placed.some((q) => Math.hypot(q[0] - x, q[1] - y) < 26)) continue
        placed.push([x, y])
        out.ticks.push({ x, y, anchor, text: fmt(axes[j], fromU(axes[j], t)) })
      }
      const D = DIAL[axes[j]]
      // The upright axis is titled above its top end; the floor axes beside their edges, kept inside the frame.
      if (j === 2) {
        const top = P(b)
        out.titles.push(fit({ x: top[0], y: top[1] - 30, anchor: 'middle', label: D.label, what: D.what }))
      } else {
        out.titles.push(fit({ x: mid[0] + 40 * dx, y: mid[1] + 40 * dy + (dy > 0.35 ? 10 : 0), anchor, label: D.label, what: D.what }))
      }
    }
    return out
  })

  /* ------------------------------------------------------------ interaction ------------------------- */
  let drag = null
  function down(e) {
    drag = { x: e.clientX, y: e.clientY, yaw, pitch }
    e.currentTarget.setPointerCapture(e.pointerId)
  }
  function move(e) {
    if (!drag) return
    yaw = ((drag.yaw - (e.clientX - drag.x) * 0.45 + 540) % 360) - 180
    pitch = Math.max(4, Math.min(70, drag.pitch + (e.clientY - drag.y) * 0.3))
  }
  const up = () => (drag = null)

  // One slow swing when the figure first comes into view, so the eye reads depth; none with reduced motion.
  let figure
  onMount(() => {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return
    let raf
    const io = new IntersectionObserver(([entry]) => {
      if (!entry.isIntersecting) return
      io.disconnect()
      const from = yaw - 38, to = yaw, t0 = performance.now()
      const step = (t) => {
        if (drag) return
        const k = Math.min(1, (t - t0) / 2600)
        yaw = from + (to - from) * (1 - Math.pow(1 - k, 3))
        if (k < 1) raf = requestAnimationFrame(step)
      }
      raf = requestAnimationFrame(step)
    }, { threshold: 0.5 })
    io.observe(figure)
    return () => { io.disconnect(); cancelAnimationFrame(raf) }
  })

  /* ------------------------------------------------------------ words ------------------------------- */
  const n0 = (x) => String(Math.round(x))
  const rangeOf = (id, r) => {
    const D = DIAL[id]
    if (D.unit === 'times') {
      const a = Number(r[0].toFixed(2)), b = Number(r[1].toFixed(2))
      return a === b ? a + '×' : a + '–' + b + '×'
    }
    const f = (x) => { const v = 100 * x; return Math.abs(v) < 10 ? v.toFixed(1) : String(Math.round(v)) }
    return f(r[0]) === f(r[1]) ? f(r[0]) + '%' : f(r[0]) + '–' + f(r[1]) + '%'
  }
  const bn = (r) => '$' + n0(r[0]) + '–' + n0(r[1]) + 'bn'
  const pct = (r) => Math.round(100 * r[0]) + '–' + Math.round(100 * r[1]) + '%'
  const tb = d.dials.find((x) => x.id === 'taxes'), bb = d.dials.find((x) => x.id === 'benefits')
  const lede = {
    taxes: d.specs.map((s) => mainAt(s, 'taxes') - s.main / slope(s, 'taxes')),
    benefits: d.specs.map((s) => 1 - (mainAt(s, 'benefits') - s.main / slope(s, 'benefits'))),
  }
  const span = (xs) => [Math.min(...xs), Math.max(...xs)]
</script>

<section class="fig" id="cube">
  <div class="body">
    <p class="kicker">Complete account · main case · three assumptions at once</p>
    <h2>Everyone else comes out ahead only where schools and the other services barely grow for them</h2>
    <p class="lede">
      Each axis is one assumption, from its lowest setting to its highest; every assumption not on an axis stays
      at the main case. The cost to everyone else is a straight-line sum of the assumptions, so the settings where it
      is exactly zero form a flat sheet (ochre). The sheet has some thickness because the main case leaves a few
      choices open, such as how taxes are split. Beyond it, in the blue corner, everyone else comes out ahead.
    </p>
    <p class="lede">
      The axes start by splitting every public service budget into three parts, each counted once: schools, every
      other public service, and general administration. Taxes and benefits stay at what records show. The blue corner
      is where schools and the other services both barely grow for the added people; the main case sits far from it.
    </p>
    <p class="lede">
      Put taxes or benefits on an axis and the blue corner grows, because each is larger than the whole cost. Taxes
      <span class="num">{pct(span(lede.taxes).map((x) => x - 1))}</span> above what records show reach the sheet on
      their own, as do benefits <span class="num">{pct(span(lede.benefits))}</span> below, or both
      <span class="num">{pct(d.together)}</span> off at once. Both are measured, not assumed; the cube runs them from
      zero to twice the records.
    </p>

    <div class="controls picks">
      {#each ['Up', 'Floor', 'Floor'] as name, j}
        {@const slot = [2, 0, 1][j]}
        <label>
          {name}
          <select bind:value={axes[slot]}>
            {#each OPTIONS as D}
              <option value={D.id} disabled={taken(D.id, slot)}>{D.label}</option>
            {/each}
          </select>
        </label>
      {/each}
    </div>

    <div bind:clientWidth={cw}>
    <svg bind:this={figure} class="cube" viewBox="0 0 {W} {H}" role="img"
      aria-label="A cube of three assumptions, cut by the flat sheet where the cost to everyone else is zero"
      onpointerdown={down} onpointermove={move} onpointerup={up} onpointercancel={up}>
      <!-- Hidden edges first, faint. -->
      {#each edges.filter((e) => !e.front) as e}
        <line x1={e.a[0]} y1={e.a[1]} x2={e.b[0]} y2={e.b[1]} stroke="#dcd8c8" stroke-width="0.8" stroke-dasharray="3 3" />
      {/each}

      <!-- The break-even sheet for each of the 64 specifications, drawn as one shape. -->
      <g opacity="0.55">
        {#each sheets as poly}
          {#if poly.length}<polygon points={pts(poly)} fill="#ecdcae" />{/if}
        {/each}
      </g>
      <!-- The two ends of the band: the specification most favourable to the group solid, the least dotted. -->
      {#if sheets[d.lowEnd].length}
        <polygon points={pts(sheets[d.lowEnd])} fill="none" stroke="#b8913a" stroke-width="0.8" />
      {/if}
      {#if sheets[d.highEnd].length}
        <polygon points={pts(sheets[d.highEnd])} fill="none" stroke="#b8913a" stroke-width="0.8" stroke-dasharray="1.5 2.5" />
      {/if}

      <!-- Where everyone else is better off under every specification. -->
      {#each solid as f}
        <polygon points={pts(f.face)} fill="#bbd4ee" fill-opacity={f.front ? 0.42 : 0.22} stroke="#5c97d2" stroke-width="0.7" stroke-linejoin="round" />
      {/each}
      {#if solidLabel}
        <text class="it halo" x={solidLabel[0]} y={solidLabel[1] + 4} text-anchor="middle" font-size="12.5" fill="#2f5f8f">better off</text>
      {/if}

      <!-- The main case: one point per specification, a drop line to the floor, and the moves to the sheet. -->
      {#each rays as r}
        {@const b = P(r.to)}
        <line x1={m[0]} y1={m[1]} x2={b[0]} y2={b[1]} stroke="#57544c" stroke-width="1" stroke-dasharray="1.5 3" />
        <circle cx={b[0]} cy={b[1]} r="2.6" fill="#fffff8" stroke="#57544c" stroke-width="1" />
        <text class="num halo muted" x={b[0] + 6} y={b[1] - 5} font-size="11">{fmt(axes[r.j], r.value)}</text>
      {/each}
      {#each tops as t}
        <line x1={t[0][0]} y1={t[0][1]} x2={t[1][0]} y2={t[1][1]} stroke="#8d897e" stroke-width="0.8" stroke-dasharray="2 2.5" />
      {/each}
      <path d="M{tops[0][1][0] - 3},{tops[0][1][1]} h6 M{tops[0][1][0]},{tops[0][1][1] - 2} v4" stroke="#8d897e" stroke-width="0.8" />
      {#each mains as u}
        {@const p = P(u)}
        <circle cx={p[0]} cy={p[1]} r="1.9" fill="#111" />
      {/each}
      <text class="halo" x={m[0] + 9} y={m[1] + 16} font-size="12.5">main case</text>
      <text class="halo muted num" x={m[0] + 9} y={m[1] + 30} font-size="11">{bn(d.main)} worse off</text>

      <!-- Front edges and axis labels. -->
      {#each edges.filter((e) => e.front) as e}
        <line x1={e.a[0]} y1={e.a[1]} x2={e.b[0]} y2={e.b[1]} stroke="#b9b5a8" stroke-width="0.9" />
      {/each}
      {#each labels.ticks as t}
        <text class="faint num halo" x={t.x} y={t.y} text-anchor={t.anchor} font-size="11">{t.text}</text>
      {/each}
      {#each labels.titles as t}
        <text class="halo" x={t.x} y={t.y} text-anchor={t.anchor} font-size="12.5">{t.label}</text>
        <text class="faint it halo" x={t.x} y={t.y + 14} text-anchor={t.anchor} font-size="11">{t.what}</text>
      {/each}
    </svg>
    </div>

    <div class="slider">
      <span>Turn</span>
      <input type="range" min="-180" max="180" step="1" bind:value={yaw} aria-label="Turn the cube" />
      <span class="num">{Math.round(yaw)}°</span>
    </div>
    <div class="slider">
      <span>Tilt</span>
      <input type="range" min="4" max="70" step="1" bind:value={pitch} aria-label="Tilt the cube" />
      <span class="num">{Math.round(pitch)}°</span>
    </div>

    <p class="note">
      {#if !anyGain}
        Nowhere in this cube is everyone else better off: even with all three at their most favourable settings, and
        every other assumption at the main case, the sheet lies outside it.
      {:else if !gainAll.length}
        Only some of the main case’s specifications have a corner of this cube where everyone else is better off.
      {/if}
      From the main case, one at a time:
      {#each alone as a, i}
        {a.D.label.toLowerCase()}
        {#if a.all}reaches the sheet at <span class="num">{rangeOf(a.id, a.roots)}</span>{:else if a.none}never
          reaches it (at <span class="num">{fmt(a.id, a.end)}</span> everyone else is still
          <span class="num">{bn(a.atEnd)}</span> worse off){:else}reaches it for some specifications only{/if}{i < 2 ? '; ' : '.'}
      {/each}
    </p>
  </div>

  <aside class="side">
    <p>
      Drag the cube or use the sliders to turn it. Choose any three assumptions for the axes; an assumption can
      appear once, and “every public service” cannot share the cube with one of its parts.
    </p>
    <p>
      The cube spans each assumption’s whole range, not its likely range, so the size of the blue corner is not a
      probability.
    </p>
    <p>
      On a derived axis the main case sits at the one share that costs the same as its own mix. It charges colleges,
      police, health and welfare in full and roads not at all, which on “every other public service” comes to
      <span class="num">{rangeOf('others', span(d.specs.map((s) => mainAt(s, 'others'))))}</span>.
    </p>
    <p>
      The ochre band holds the break-even sheet of every specification, drawn as one even tint: solid edge for the
      specification most favourable to the group, dotted for the least.
    </p>
    <p>
      Black dots: the main case under each of its {d.specs.length} specifications. The dotted moves and the drop line
      belong to the one most favourable to the group (<span class="num">${n0(d.main[0])}bn</span>).
    </p>
    <p>
      “Every public service” sets schools, colleges, police, health, welfare, housing and roads to one share of their
      average cost, with general administration as in the main case. Here it turns at
      <span class="num">{rangeOf('services', d.servicesRoot)}</span>; the staircase’s
      <span class="num">{rangeOf('services', d.publishedBreakEven)}</span> also varies the model of the gain from
      their work.
    </p>
    <p>proto/cube.cjs; the page’s straight-line formula is gated against the engine at {d.gatePoints.toLocaleString('en-US')} random points.</p>
  </aside>
</section>

<style>
  .cube { width: 100%; height: auto; display: block; touch-action: pan-y; cursor: grab; user-select: none; }
  .cube:active { cursor: grabbing; }
  .picks select { font: inherit; font-size: 0.88rem; max-width: 15rem; }
  .lede .num, .note .num, .side .num { white-space: nowrap; }
</style>
