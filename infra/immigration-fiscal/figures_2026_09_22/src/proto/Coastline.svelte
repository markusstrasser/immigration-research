<script>
  import data from '../generated/proto_coastline.json'
  import { Tween, prefersReducedMotion } from 'svelte/motion'
  import { cubicInOut } from 'svelte/easing'

  // Each version of the account is a plane over the map (proto/coastline.cjs measures and gates them):
  // how much worse off everyone else is = k + a·x + b·y + g·(general administration) + r·(roads), $bn a year.
  const planes = data.planes
  const LAND = data.levels.land
  const SEA = data.levels.sea
  const byId = Object.fromEntries(data.configs.map((c) => [c.id, c]))
  const anchors = data.anchors
  const WEIGHTS = { zero: [1, 0, 0], band: [0, 1, 0], full: [0, 0, 1] }

  const constants = (w, d) => planes.map((p) => p.k + p.g * (w[1] * p.gg + w[2]) + p.r * d)
  // Where each version's height is v, as a line y = p + q·x.
  const levelLines = (c, v) => planes.map((p, s) => ({ p: (v - c[s]) / p.b, q: -p.a / p.b }))
  // Upper envelope: the version that finds everyone else best off reaches v there (every version is at
  // least v above it). Lower envelope: the one that finds them worst off. Same rule as the generator's.
  function envelope(lines, upper) {
    const xs = [0, 1]
    for (let i = 0; i < lines.length; i++) {
      for (let j = i + 1; j < lines.length; j++) {
        const dq = lines[i].q - lines[j].q
        if (Math.abs(dq) < 1e-15) continue
        const x = (lines[j].p - lines[i].p) / dq
        if (x > 0 && x < 1) xs.push(x)
      }
    }
    xs.sort((u, v) => u - v)
    const pick = upper ? Math.max : Math.min
    return xs.map((x) => [x, pick(...lines.map((l) => l.p + l.q * x))])
  }
  function at(poly, x) {
    for (let i = 1; i < poly.length; i++) {
      if (x <= poly[i][0] + 1e-15) {
        const [x0, y0] = poly[i - 1]
        const [x1, y1] = poly[i]
        return x1 === x0 ? y1 : y0 + ((y1 - y0) * (x - x0)) / (x1 - x0)
      }
    }
    return poly[poly.length - 1][1]
  }
  // Landmark heights from the planes: the best and worst version at a point. The main case spans
  // schools 63% (its best version) to 66% (its worst); cost rises with x.
  const spanAt = (c, x, y) => {
    const v = planes.map((p, s) => c[s] + p.a * x + p.b * y)
    return [Math.min(...v), Math.max(...v)]
  }
  const landmarks = (c) => ({
    '00': spanAt(c, 0, 0), '10': spanAt(c, 1, 0), '01': spanAt(c, 0, 1), '11': spanAt(c, 1, 1),
    main: [spanAt(c, anchors.schools[0], 1)[0], spanAt(c, anchors.schools[1], 1)[1]],
  })
  // Fail loud if the drawing rule ever drifts from the generator's gated tide lines and landmarks.
  for (const cfg of data.configs) {
    const c = constants(WEIGHTS[cfg.gg], cfg.roads ? 1 : 0)
    const mine = { high: envelope(levelLines(c, 0), true), low: envelope(levelLines(c, 0), false) }
    for (const side of ['high', 'low']) {
      for (const [x, y] of cfg[side].poly) {
        if (!(Math.abs(at(mine[side], x) - y) < 1e-6)) {
          throw new Error(`coastline: drawn ${side} tide differs from proto/coastline.cjs (${cfg.id}, x = ${x})`)
        }
      }
    }
    const lm = landmarks(c)
    for (const [k, want] of [...Object.entries(cfg.corners), ['main', cfg.main]]) {
      if (!(Math.abs(lm[k][0] - want[0]) < 1e-3 && Math.abs(lm[k][1] - want[1]) < 1e-3)) {
        throw new Error(`coastline: landmark ${k} differs from proto/coastline.cjs (${cfg.id})`)
      }
    }
  }

  // Controls, and dials that glide between them: every frame of the glide is itself a setting of the
  // account (general administration and roads are linear dials).
  let gg = $state('band')
  let roads = $state(false)
  const cfg = $derived(byId[gg + (roads ? '_roads' : '')])
  const motion = { duration: () => (prefersReducedMotion.current ? 0 : 1100), easing: cubicInOut }
  const ggW = Tween.of(() => WEIGHTS[gg], motion)
  const roadsW = Tween.of(() => (roads ? 1 : 0), motion)

  // Map geometry, viewBox units.
  const W = 760
  const L = 72
  const T = 78
  const S = 462
  const H = T + S + 96
  const X = (x) => L + x * S
  const Y = (y) => T + (1 - y) * S
  const pt = ([x, y]) => `${X(x).toFixed(1)},${Y(y).toFixed(1)}`
  const path = (poly) => 'M' + poly.map(pt).join('L')
  const above = (poly) => `${path(poly)}L${X(1)},${Y(9)}L${X(0)},${Y(9)}Z`
  const below = (poly) => `${path(poly)}L${X(1)},${Y(-9)}L${X(0)},${Y(-9)}Z`

  const geo = $derived.by(() => {
    const c = constants(ggW.current, roadsW.current)
    const up = (v) => envelope(levelLines(c, v), true)
    const down = (v) => envelope(levelLines(c, v), false)
    return { c, land: LAND.map((v) => ({ v, poly: up(v) })), sea: SEA.map((v) => ({ v, poly: down(v) })), high: up(0), low: down(0), name: up(125) }
  })
  // Landmark numbers follow the glide; at rest they equal the generator's (checked above).
  const lm = $derived(landmarks(geo.c))

  // The part of a falling line inside the square, with its end points on the frame.
  function inside(poly) {
    const out = []
    for (let i = 0; i < poly.length; i++) {
      const [x, y] = poly[i]
      if (i) {
        const [x0, y0] = poly[i - 1]
        for (const edge of [1, 0]) {
          if ((y0 - edge) * (y - edge) < 0) out.push([x0 + ((x - x0) * (y0 - edge)) / (y0 - y), edge])
        }
      }
      if (y >= 0 && y <= 1) out.push([x, y])
    }
    return out
  }
  const lengthPx = (poly) => poly.slice(1).reduce((s, q, i) => s + Math.hypot((q[0] - poly[i][0]) * S, (q[1] - poly[i][1]) * S), 0)
  const angleOf = (x0, y0, x1, y1) => (Math.atan2(-(y1 - y0) * S, (x1 - x0) * S) * 180) / Math.PI
  // A point along a polyline at fraction f of its length, with the local angle (degrees, screen).
  function along(poly, f) {
    let goal = f * lengthPx(poly)
    for (let i = 1; i < poly.length; i++) {
      const [x0, y0] = poly[i - 1]
      const [x1, y1] = poly[i]
      const seg = Math.hypot((x1 - x0) * S, (y1 - y0) * S)
      if (goal <= seg || i === poly.length - 1) {
        const t = seg ? Math.min(1, goal / seg) : 0
        return { x: x0 + t * (x1 - x0), y: y0 + t * (y1 - y0), angle: angleOf(x0, y0, x1, y1) }
      }
      goal -= seg
    }
  }
  // Screen angle of the straight line from a polyline's first point to its last.
  const chord = (poly) => angleOf(...poly[0], ...poly[poly.length - 1])
  // Contour labels climb the diagonal x = y, a ladder read from the sea to the top corner; a contour
  // that misses the diagonal is labelled at the middle of its visible part.
  function ladder(poly) {
    for (let i = 1; i < poly.length; i++) {
      const [x0, y0] = poly[i - 1]
      const [x1, y1] = poly[i]
      const f0 = y0 - x0
      const f1 = y1 - x1
      if (f0 >= 0 && f1 < 0) {
        const t = f0 / (f0 - f1)
        const x = x0 + t * (x1 - x0)
        if (x > 0.05 && x < 0.95) return { x, y: y0 + t * (y1 - y0), angle: angleOf(x0, y0, x1, y1) }
      }
    }
    const vis = inside(poly)
    return vis.length > 1 && lengthPx(vis) > 70 ? along(vis, 0.5) : null
  }
  const labels = $derived(geo.land.map(({ v, poly }) => ({ v, at: ladder(poly) })).filter((l) => l.at))
  const highVis = $derived(inside(geo.high))
  const lowVis = $derived(inside(geo.low))
  const nameVis = $derived(inside(geo.name))

  // Colour is the sign only (README, "Visual grammar"): orange worse off, lighter to deeper with
  // height; blue better off; ochre break-even and the shore whose sign depends on the version; ink
  // for the main case.
  const TINTS = ['#fbe8dc', '#f9e0d3', '#f6d7c9', '#f4d0c2', '#f2cabc', '#eebca9', '#e9ad97', '#e4a089']
  const INDEX = (v) => v % 100 === 0
  const OCHRE = '#b8913a'
  // The shore is one flat tint between its two edge lines: it marks where the versions disagree on the
  // sign, and never how many of them do.
  const SAND = '#ecdcae'
  // Land bands present on this map: up to the best version's height at the top corner.
  const bands = $derived(Math.min(LAND.length, Math.floor(lm['11'][0] / 50) + 1))

  // Words and numbers: every amount carries its direction in words, from everyone else's side.
  const r0 = (v) => Math.round(v)
  const pct = (v) => Math.round(100 * v) + '%'
  const pcts = ([a, b]) => `${Math.round(100 * a)}–${Math.round(100 * b)}%`
  function money([lo, hi], unit = 'bn') {
    if (hi < 0) return `$${r0(-hi)}–${r0(-lo)}${unit} better off`
    if (lo > 0) return `$${r0(lo)}–${r0(hi)}${unit} worse off`
    return `from $${r0(-lo)}${unit} better off to $${r0(hi)}${unit} worse off`
  }
  const YR = 'bn a year'
  const better = (span) => span[1] < 0
  const ggWords = $derived(gg === 'zero' ? 'general administration does not grow' : gg === 'band'
    ? `general administration grows ${pcts(anchors.gg)}` : 'general administration grows fully')
  const band = byId.band

  // A spot height under the pointer: the best and the worst version at that point.
  let probe = $state(null)
  function locate(e) {
    const svg = e.currentTarget.ownerSVGElement
    const m = svg.getScreenCTM()
    if (!m) return
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m.inverse())
    const x = (p.x - L) / S
    const y = 1 - (p.y - T) / S
    probe = x >= 0 && x <= 1 && y >= 0 && y <= 1 ? { x, y } : null
  }
  function key(e) {
    const step = { ArrowRight: [0.05, 0], ArrowLeft: [-0.05, 0], ArrowUp: [0, 0.05], ArrowDown: [0, -0.05] }[e.key]
    if (!step) return
    e.preventDefault()
    const from = probe || { x: anchors.schools[0], y: 1 }
    probe = { x: Math.min(1, Math.max(0, from.x + step[0])), y: Math.min(1, Math.max(0, from.y + step[1])) }
  }
  const probeSpan = $derived(probe ? spanAt(geo.c, probe.x, probe.y) : null)

  // Legend column, right of the map.
  const lx = X(1) + 16
  const ly = T + 112
  const sw = 24
</script>

<section class="fig" id="coastline">
  <div class="body">
    <p class="kicker">Prototype · coastline · adopted main case</p>
    <h2>Everyone else is better off only if schools and other services grow little for the Mexican-origin population</h2>
    <p class="lede">
      Read it as a map of assumptions about the Mexican-origin population, all generations, about
      <span class="num">{r0(anchors.group.millions)} million</span> people. Across: how much school budgets add for each of its
      pupils, as a share of the usual cost per pupil. Up: how much other services grow for them: colleges,
      police, courts and prisons, public health, welfare administration, housing and community. Height is
      how much worse off everyone else is, in $bn a year, counting the gain from the group’s work; below sea
      level everyone else is better off. General administration grows <span class="num">{pcts(anchors.gg)}</span> and roads,
      transport and parks do not grow, as in the main case.
    </p>
    <p class="lede">
      The main case sits on the top edge, at <span class="num">{pcts(anchors.schools)}</span> for schools and 100% for other
      services, where everyone else is <span class="num">{money(anchors.main, YR)}</span>. Some versions of the account find
      everyone else better off, but only in the bottom-left corner, below the solid high-tide line. That line meets the
      school axis at <span class="num">{pct(band.high.x0)}</span> and the service axis at <span class="num">{pct(band.high.y0)}</span>;
      everywhere below it the school share and the service share add up to less than <span class="num">{pct(band.high.sum)}</span>.
      Every version finds them better off only below the dotted low-tide line, where the two add up to less than
      <span class="num">{pct(band.low.sum)}</span>. With schools at <span class="num">{pcts(anchors.schools)}</span> and none of the
      other services growing, everyone else is still <span class="num">{money(band.schoolsOnly, YR)}</span>. Stop general
      administration growing too and the corner reaches only to shares adding up to <span class="num">{pct(byId.zero.high.sum)}</span>,
      while the main case’s schools and services still leave everyone else <span class="num">{money(byId.zero.main, YR)}</span>.
    </p>

    <div class="controls" role="radiogroup" aria-label="General administration">
      <span>General administration grows for them:</span>
      <label><input type="radio" name="coast-gg" value="zero" bind:group={gg} /> not at all</label>
      <label><input type="radio" name="coast-gg" value="band" bind:group={gg} /> as in the main case, {pcts(anchors.gg)}</label>
      <label><input type="radio" name="coast-gg" value="full" bind:group={gg} /> fully</label>
    </div>
    <div class="controls">
      <label><input type="checkbox" bind:checked={roads} /> roads, transport and parks grow too</label>
    </div>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 {W} {H}" role="img" aria-label={`Map of how much worse off everyone else is over the school and service assumptions. ${cfg.high.sum === null
      ? 'No version finds everyone else better off anywhere on this map.'
      : `Some versions find everyone else better off, only in the corner where the two shares add up to less than ${pct(cfg.high.sum)}.`} The main case’s schools and services leave everyone else ${money(cfg.main, YR)}.`}>
      <defs>
        <clipPath id="coast-clip"><rect x={L} y={T} width={S} height={S} /></clipPath>
        <mask id="coast-gaps" maskUnits="userSpaceOnUse" x="0" y="0" width={W} height={H}>
          <rect width={W} height={H} fill="white" />
          {#each labels as l}
            <rect x="-13" y="-6" width="26" height="12" fill="black" transform="translate({X(l.at.x)},{Y(l.at.y)}) rotate({l.at.angle})" />
          {/each}
        </mask>
      </defs>

      <!-- The land: orange, lighter to deeper every $50bn of the best version's height. -->
      <g clip-path="url(#coast-clip)">
        <rect x={L} y={T} width={S} height={S} fill={TINTS[0]} />
        {#each geo.land as lv, i}
          <path d={above(lv.poly)} fill={TINTS[i + 1]} />
        {/each}
        <!-- The shore: better off in some versions, worse off in others. The sea: better off in every one. -->
        <path d={below(geo.high)} fill={SAND} />
        <path d={below(geo.low)} fill="#bbd4ee" />
        {#each geo.sea as d}
          <path d={path(d.poly)} fill="none" stroke="#5c97d2" stroke-width="0.7" />
        {/each}
        <!-- Graticule every 25%, in paper, as on a chart. -->
        {#each [0.25, 0.5, 0.75] as t}
          <line x1={X(t)} x2={X(t)} y1={T} y2={T + S} stroke="#fffff8" stroke-width="0.9" opacity="0.9" />
          <line x1={L} x2={L + S} y1={Y(t)} y2={Y(t)} stroke="#fffff8" stroke-width="0.9" opacity="0.9" />
        {/each}
        <g mask="url(#coast-gaps)">
          {#each geo.land as lv}
            <path d={path(lv.poly)} fill="none" stroke="#ca7a5e" stroke-width={INDEX(lv.v) ? 1.15 : 0.6} />
          {/each}
        </g>
        <!-- Break-even lines, ochre: low tide dotted, high tide solid. -->
        <path d={path(geo.low)} fill="none" stroke={OCHRE} stroke-width="1.5" stroke-linecap="round" stroke-dasharray="0.1 3" />
        <path d={path(geo.high)} fill="none" stroke={OCHRE} stroke-width="1.5" />
      </g>

      <!-- Contour heights, reading uphill. -->
      {#each labels as l}
        <text class="muted num" font-size="10.5" text-anchor="middle" dy="0.35em" transform="translate({X(l.at.x)},{Y(l.at.y)}) rotate({l.at.angle})">{l.v}</text>
      {/each}

      <!-- Names on the map. -->
      {#if nameVis.length > 1 && lengthPx(nameVis) > 260}
        <!-- Set on the chord of the $125bn line, so a bend in that line never breaks the lettering. -->
        {@const p = along(nameVis, 0.34)}
        <text class="faint" font-size="11" letter-spacing="3.2" text-anchor="middle" dy="-4"
          transform="translate({X(p.x)},{Y(p.y)}) rotate({chord(nameVis)})">EVERYONE ELSE WORSE OFF</text>
      {/if}
      {#if highVis.length > 1 && lengthPx(highVis) > 90}
        {@const a = along(highVis, 0.62)}
        <text class="muted it halo" font-size="10.5" text-anchor="middle" transform="translate({X(a.x)},{Y(a.y)}) rotate({a.angle})" dy="-5">high tide</text>
      {/if}
      {#if lowVis.length > 1 && lengthPx(lowVis) > 70}
        {@const a = along(lowVis, 0.62)}
        <text class="muted it halo" font-size="10.5" text-anchor="middle" transform="translate({X(a.x)},{Y(a.y)}) rotate({a.angle})" dy="-5">low tide</text>
      {/if}
      {#if lowVis.length > 1 && lengthPx(lowVis) > 170}
        {@const s = along(lowVis, 0.4)}
        <text class="it better sea" font-size="11.5" text-anchor="middle" letter-spacing="1.5" transform="translate({X(s.x)},{Y(s.y)}) rotate({s.angle})" dy="30">sea: better off</text>
      {/if}

      <!-- The frame: a graduated border every 5%, as on a chart's neat line. -->
      {#each Array.from({ length: 20 }, (_, i) => i).filter((i) => i % 2 === 0) as i}
        <rect x={X(i / 20)} y={T - 4} width={S / 20} height="4" fill="#8d897e" />
        <rect x={X(i / 20)} y={T + S} width={S / 20} height="4" fill="#8d897e" />
        <rect x={L - 4} y={Y((i + 1) / 20)} width="4" height={S / 20} fill="#8d897e" />
        <rect x={L + S} y={Y((i + 1) / 20)} width="4" height={S / 20} fill="#8d897e" />
      {/each}
      <rect x={L} y={T} width={S} height={S} fill="none" stroke="#57544c" stroke-width="0.7" />
      <rect x={L - 4} y={T - 4} width={S + 8} height={S + 8} fill="none" stroke="#57544c" stroke-width="0.5" />

      {#each [0.25, 0.5, 0.75, 1] as t}
        <text class="faint num" x={X(t)} y={T + S + 22} text-anchor="middle" font-size="11">{pct(t)}</text>
      {/each}
      {#each [0, 0.25, 0.5, 0.75, 1] as t}
        <text class="faint num" x={L - 11} y={Y(t) + 4} text-anchor="end" font-size="11">{pct(t)}</text>
      {/each}
      <text class="muted it" x={X(1)} y={T + S + 42} text-anchor="end" font-size="12">School budgets add this share of the usual cost per pupil →</text>
      <text class="muted it" transform="translate(14,{Y(0)}) rotate(-90)" font-size="12">Other services grow by this share of their average cost →</text>
      <text class="faint it" transform="translate(28,{Y(0)}) rotate(-90)" font-size="10.5">colleges, police, courts and prisons, public health, welfare administration, housing</text>

      <!-- Landmarks: the main case in ink. -->
      <rect x={X(anchors.schools[0])} y={T - 4} width={X(anchors.schools[1]) - X(anchors.schools[0])} height="4" fill="#111" />
      <path d="M {X((anchors.schools[0] + anchors.schools[1]) / 2) - 4} {T - 14} l 8 0 l -4 7 z" fill="#111" />
      <text x={X((anchors.schools[0] + anchors.schools[1]) / 2)} y={T - 36} text-anchor="middle" font-size="13">{cfg.id === 'band' ? 'Main case' : 'Main case’s schools and services'}</text>
      <text class="num" x={X((anchors.schools[0] + anchors.schools[1]) / 2)} y={T - 20} text-anchor="middle" font-size="12.5">{money(lm.main, YR)}</text>

      <circle cx={X(1)} cy={Y(1)} r="2.2" fill="#111" />
      <text x={lx} y={T + 4} font-size="12.5">Schools and other services</text>
      <text x={lx} y={T + 19} font-size="12.5">{roads ? 'grow fully, roads too' : 'grow fully'}</text>
      <text class="num" x={lx} y={T + 35} font-size="12.5">{money(lm['11'])}</text>
      <text class="faint it" x={lx} y={T + 50} font-size="11">{ggWords}</text>
      <text class="faint it" x={lx} y={T + 63} font-size="11">{roads ? (gg === 'band' ? 'the proportional benchmark' : '') : 'roads, transport, parks do not grow'}</text>

      <text class="muted it halo" x={X(0) + 8} y={Y(1) + 17} font-size="11">services alone: <tspan class="num">{money(lm['01'])}</tspan></text>
      <text class="muted it halo" x={X(1) - 8} y={Y(0) - 9} text-anchor="end" font-size="11">schools alone: <tspan class="num">{money(lm['10'])}</tspan></text>

      <circle cx={X(0)} cy={Y(0)} r="2.2" fill="#111" />
      <line x1={X(0)} x2={X(0)} y1={Y(0) + 9} y2={Y(0) + 56} stroke="#8d897e" stroke-width="0.7" />
      <text x={X(0) + 6} y={Y(0) + 66} font-size="12">{gg === 'zero' && !roads ? 'Nothing grows for them' : 'Neither schools nor other services grow'}<tspan class="faint it" font-size="11">{gg === 'zero' && !roads ? '' : `; ${ggWords}${roads ? ', and roads, transport and parks do' : ''}`}</tspan></text>
      <text class="num" class:better={better(lm['00'])} x={X(0) + 6} y={Y(0) + 82} font-size="12">{money(lm['00'], YR)}</text>
      {#if highVis.length < 2}
        <text class="muted it halo" x={X(0) + 10} y={Y(0) - 12} font-size="11">no sea: everyone else is worse off everywhere on this map</text>
      {/if}

      <!-- Legend: a scale that runs worse off to the right, then the sea, the shore and the tides. -->
      <text class="it" x={lx} y={ly} font-size="12">How much worse off everyone</text>
      <text class="it" x={lx} y={ly + 15} font-size="12">else is, $bn a year</text>
      <text class="faint" x={lx} y={ly + 30} font-size="11">in the version that finds them</text>
      <text class="faint" x={lx} y={ly + 43} font-size="11">best off at each point</text>
      {#each TINTS.slice(0, bands) as fill, i}
        <rect x={lx + i * sw} y={ly + 54} width={sw} height="13" fill={fill} />
      {/each}
      <line x1={lx} x2={lx} y1={ly + 52} y2={ly + 71} stroke="#111" stroke-width="0.8" />
      {#each Array.from({ length: bands + 1 }, (_, i) => i) as i}
        <text class="faint num" x={lx + i * sw} y={ly + 82} text-anchor="middle" font-size="10">{i * 50}</text>
      {/each}
      <text class="faint it" x={lx + bands * sw} y={ly + 96} text-anchor="end" font-size="11">worse off →</text>

      <rect x={lx} y={ly + 110} width="16" height="16" fill="#bbd4ee" />
      <line x1={lx} x2={lx + 16} y1={ly + 118} y2={ly + 118} stroke="#5c97d2" stroke-width="0.7" />
      <text class="faint" x={lx + 24} y={ly + 118} font-size="11">sea: every version finds them</text>
      <text class="faint" x={lx + 24} y={ly + 131} font-size="11">better off; a line every $10bn</text>
      <rect x={lx} y={ly + 142} width="16" height="16" fill={SAND} />
      <text class="faint" x={lx + 24} y={ly + 150} font-size="11">shore: some versions find them</text>
      <text class="faint" x={lx + 24} y={ly + 163} font-size="11">better off, others worse off</text>
      <line x1={lx} x2={lx + 16} y1={ly + 182} y2={ly + 182} stroke={OCHRE} stroke-width="1.5" />
      <text class="faint" x={lx + 24} y={ly + 186} font-size="11">high tide: break-even in the</text>
      <text class="faint" x={lx + 24} y={ly + 199} font-size="11">version that finds them best off</text>
      <line x1={lx} x2={lx + 16} y1={ly + 216} y2={ly + 216} stroke={OCHRE} stroke-width="1.5" stroke-linecap="round" stroke-dasharray="0.1 3" />
      <text class="faint" x={lx + 24} y={ly + 220} font-size="11">low tide: break-even in the</text>
      <text class="faint" x={lx + 24} y={ly + 233} font-size="11">version that finds them worst off</text>

      <!-- Probe: pointer or arrow keys. -->
      {#if probe && probeSpan}
        {@const right = probe.x < 0.6}
        <g pointer-events="none">
          <line x1={X(probe.x)} x2={X(probe.x)} y1={T} y2={T + S} stroke="#57544c" stroke-width="0.5" opacity="0.6" />
          <line x1={L} x2={L + S} y1={Y(probe.y)} y2={Y(probe.y)} stroke="#57544c" stroke-width="0.5" opacity="0.6" />
          <circle cx={X(probe.x)} cy={Y(probe.y)} r="2.5" fill="#111" />
          <text class="halo num" x={X(probe.x) + (right ? 9 : -9)} y={Y(probe.y) - 22} text-anchor={right ? 'start' : 'end'} font-size="11.5">schools {pct(probe.x)}, other services {pct(probe.y)}</text>
          <text class="halo num" class:better={better(probeSpan)} x={X(probe.x) + (right ? 9 : -9)} y={Y(probe.y) - 8} text-anchor={right ? 'start' : 'end'} font-size="11.5">{money(probeSpan)}</text>
        </g>
      {/if}
      <!-- ARIA's role for a region that takes the arrow keys itself; Svelte's lint counts it as static. -->
      <!-- svelte-ignore a11y_no_noninteractive_tabindex, a11y_no_noninteractive_element_interactions -->
      <rect x={L} y={T} width={S} height={S} fill="transparent" tabindex="0" role="application" aria-label="Probe the map with the arrow keys"
        onpointermove={locate} onpointerdown={locate} onpointerleave={() => (probe = null)} onkeydown={key}
        onfocus={() => (probe = probe || { x: anchors.schools[0], y: 1 })} onblur={() => (probe = null)} style="outline: none" />
    </svg>
    </div>
    <p class="note">
      {#if cfg.high.sum === null}
        With these settings no version finds everyone else better off anywhere on the map.
      {:else}
        With these settings, some versions find everyone else better off only where the two shares add up to less than
        <span class="num">{pct(cfg.high.sum)}</span>{#if cfg.low.sum === null}, and at no point on the map do all of them find
        everyone else better off.{:else}, and all of them do only where the two add up to less than <span class="num">{pct(cfg.low.sum)}</span>.{/if}
      {/if}
      Heights and contours on land come from the version that finds everyone else best off at each point, so every version
      is at least that high{#if cfg.low.sum !== null}; the depth lines at sea come from the version that finds them worst
      off{/if}. Point at the map, or select it and use the arrow keys, to read the range across the versions at that spot.
    </p>
  </div>

  <aside class="side">
    <p>
      Each axis runs over its assumption’s whole range, 0 to 100%, so the size of a region on the map says nothing about
      how likely it is.
    </p>
    <p>
      The main case leaves six choices open, 64 versions in all: household costs charged to each person or shared, two
      measures of the gain from their work, the share of education spending that goes to schools, general
      administration at {pct(anchors.gg[0])} or {pct(anchors.gg[1])}, two estimates of unpaid hospital care, and schools at
      {pct(anchors.schools[0])} or {pct(anchors.schools[1])}. The last is this map’s x axis, so each point has
      <span class="num">{planes.length}</span> versions behind it. At the main case they leave everyone else between
      <span class="num">${r0(anchors.main[0])}bn</span> and <span class="num">${r0(anchors.main[1])}bn</span> a year worse off.
    </p>
    <p>
      At the main case, the version that finds everyone else best off {data.lowest.spec.allocation === 'shared' ? 'shares household costs' : 'charges household costs to each person'},
      takes the {data.lowest.spec.normalization === 'gdp' ? 'GDP-based' : 'cash-based'} measure of the gain from their work,
      counts {pct(data.lowest.spec.share)} of education spending as schools, grows general administration
      {pct(data.lowest.spec.gg)} and takes the {data.lowest.spec.uc === 'uninsured_use_low' ? 'lower' : 'higher'} estimate of
      unpaid hospital care.{data.lowest.everywhere ? ' It is the best version everywhere on the map.' : ' Elsewhere on the map another version can be the best.'}
    </p>
    <p>
      The engine adds costs line by line, so each version is a flat plane over this map: its contours are straight and
      parallel, and so is its break-even line. The contours and tide lines here bend because each follows, at every point,
      whichever version is best or worst there.
    </p>
    <p>
      If nothing grows at all and unpaid hospital care is charged by its published rule, everyone else is
      <span class="num">{money(anchors.noServices)}</span>: the explorer’s “No public services charged”.
    </p>
    <p>
      Source: proto/coastline.cjs. It measures each version from the account’s engine on the adopted model, checks the
      main case and the proportional benchmark against their published values, and checks every shore against the
      engine point by point.
    </p>
  </aside>
</section>

<style>
  /* Better-off text is blue (README, "Visual grammar"). */
  .better { fill: #2f5f8f; }
  /* The sea's name breaks the depth lines with a halo of sea, as the paper halo does on land. */
  .sea { paint-order: stroke; stroke: #bbd4ee; stroke-width: 3.5px; stroke-linejoin: round; }
  /* A range such as $173–207bn never breaks at its dash. */
  p .num { white-space: nowrap; }
</style>
