<script>
  import d from '../generated/proto_plane.json'

  const S = d.specs

  // The four quantities the account is additive in. Everything not on a plane's axes stays at the main case.
  const Q = {
    k: { name: 'Services charged', unit: 'share of the main case', axis: [0, 1], ticks: [0, 0.25, 0.5, 0.75, 1], f: (x) => Math.round(100 * x) + '%' },
    t: { name: 'Taxes they pay', unit: '× what records show', axis: [0, 2], ticks: [0, 0.5, 1, 1.5, 2], f: (x) => Number(x.toFixed(2)) + '×' },
    b: { name: 'Benefits they draw', unit: '× what records show', axis: [0, 2], ticks: [0, 0.5, 1, 1.5, 2], f: (x) => Number(x.toFixed(2)) + '×' },
    P: { name: 'Gain from their work', unit: '$bn a year', axis: [0, 300], ticks: [0, 100, 200, 300], f: (x) => '$' + Math.round(x) + 'bn' },
  }
  const MAIN = { k: 1, t: 1, b: 1 }

  // Cost to everyone else ($bn a year, positive = worse off) for one specification.
  const costAt = (s, v) => s.d0 + (s.d1 - s.d0) * v.k + s.tax * (v.t - 1) + s.ben * (v.b - 1) - (v.P ?? s.pf)
  const span = (xs) => [Math.min(...xs), Math.max(...xs)]
  const bn = (x) => '$' + Math.round(Math.abs(x)) + 'bn'
  const rangeBn = (r) => (Math.round(r[0]) === Math.round(r[1]) ? bn(r[0]) : '$' + Math.round(r[0]) + '–' + Math.round(r[1]) + 'bn')
  const pct = (r) => Math.round(100 * r[0]) + '–' + Math.round(100 * r[1]) + '%'

  // Keep the side of a straight line g(x, y) = 0 where g has the sign `side` (Sutherland–Hodgman, one edge).
  function clip(poly, g, side) {
    const out = []
    for (let i = 0; i < poly.length; i++) {
      const p = poly[i], q = poly[(i + 1) % poly.length]
      const gp = side * g(p[0], p[1]), gq = side * g(q[0], q[1])
      if (gp >= 0) out.push(p)
      if ((gp >= 0) !== (gq >= 0)) {
        const a = gp / (gp - gq)
        out.push([p[0] + a * (q[0] - p[0]), p[1] + a * (q[1] - p[1])])
      }
    }
    return out
  }
  const rectOf = (u, v) => [[Q[u].axis[0], Q[v].axis[0]], [Q[u].axis[1], Q[v].axis[0]], [Q[u].axis[1], Q[v].axis[1]], [Q[u].axis[0], Q[v].axis[1]]]
  // g for specification s on the plane (u, v), the rest fixed.
  const gOf = (s, u, v, fixed) => (x, y) => costAt(s, { ...fixed, [u]: x, [v]: y })
  // Where every specification is a cost (side +1) or every one a gain (side -1).
  function region(u, v, fixed, side, specs = S) {
    let poly = rectOf(u, v)
    for (const s of specs) poly = clip(poly, gOf(s, u, v, fixed), side)
    return poly
  }
  // The zero line of one specification, cut to the plane.
  function zeroSegment(g, rect) {
    const pts = []
    for (let i = 0; i < 4; i++) {
      const p = rect[i], q = rect[(i + 1) % 4]
      const gp = g(p[0], p[1]), gq = g(q[0], q[1])
      if ((gp > 0) !== (gq > 0)) {
        const a = gp / (gp - gq)
        pts.push([p[0] + a * (q[0] - p[0]), p[1] + a * (q[1] - p[1])])
      }
    }
    return pts.length >= 2 ? pts.slice(0, 2) : null
  }
  // Screen scales for a plot box [x0, x1] × [y0 (top), y1 (bottom)].
  function scales(u, v, box) {
    const [x0, x1, y0, y1] = box
    const sx = (x) => x0 + ((x - Q[u].axis[0]) / (Q[u].axis[1] - Q[u].axis[0])) * (x1 - x0)
    const sy = (y) => y1 - ((y - Q[v].axis[0]) / (Q[v].axis[1] - Q[v].axis[0])) * (y1 - y0)
    const path = (poly) => (poly.length ? 'M' + poly.map((p) => sx(p[0]).toFixed(1) + ',' + sy(p[1]).toFixed(1)).join('L') + 'Z' : '')
    return { sx, sy, path }
  }

  // Facts every take quotes.
  const mainPf = span(S.map((s) => s.pf))
  const kStar = span(S.map((s) => (s.pf - s.d0) / (s.d1 - s.d0)))   // services charged at which the cost reaches zero
  const needP = span(S.map((s) => s.d1))                             // gain from their work that zeroes the main case

  /* ---------- Take 1: one hairline per specification, coloured by a choice ---------- */
  const FAMILIES = {
    none: { label: 'nothing', levels: null },
    allocation: { label: 'how taxes are split', levels: [['personal', 'by who pays them'], ['shared', 'shared across residents']] },
    share: { label: 'schools’ share of education', levels: null },
    school: { label: 'how far school budgets grow', levels: null },
    gg: { label: 'how far administration grows', levels: null },
    uc: { label: 'unpaid hospital care', levels: [['uninsured_use_low', 'low use key'], ['uninsured_use_high', 'high use key']] },
  }
  const numLevels = (key, f) => [...new Set(S.map((s) => s[key]))].sort((a, b) => a - b).map((x) => [x, f(x)])
  FAMILIES.share.levels = numLevels('share', (x) => Math.round(100 * x) + '% schools')
  FAMILIES.school.levels = numLevels('school', (x) => Math.round(100 * x) + '% of average cost')
  FAMILIES.gg.levels = numLevels('gg', (x) => Math.round(100 * x) + '% of average cost')
  const LEVEL_INK = ['#b8913a', '#4f6d8a']

  let family = $state('allocation')
  let focus = $state(null)
  const ink = (s) => {
    const f = FAMILIES[family]
    if (!f.levels) return '#8d897e'
    return LEVEL_INK[f.levels.findIndex((l) => l[0] === s[family])]
  }
  const opacity = (s) => (focus === null ? 0.75 : s[family] === focus ? 1 : 0.1)

  const W = 760
  const box1 = [58, 520, 18, 372]
  const A1 = scales('k', 'P', box1)
  const rect1 = rectOf('k', 'P')
  const lines1 = S.map((s) => ({ s, seg: zeroSegment(gOf(s, 'k', 'P', MAIN), rect1) }))
  const cost1 = region('k', 'P', MAIN, 1)
  const gain1 = region('k', 'P', MAIN, -1)

  /* ---------- Take 2: the landscape, with the taxes and benefits dials and a point to drag ---------- */
  let taxes = $state(1)
  let benefits = $state(1)
  let pt = $state({ k: 1, P: (mainPf[0] + mainPf[1]) / 2 })
  const mid = {
    d0: S.reduce((a, s) => a + s.d0, 0) / S.length, d1: S.reduce((a, s) => a + s.d1, 0) / S.length,
    tax: S.reduce((a, s) => a + s.tax, 0) / S.length, ben: S.reduce((a, s) => a + s.ben, 0) / S.length,
    pf: S.reduce((a, s) => a + s.pf, 0) / S.length,
  }
  const STEP = 50
  const LEVELS = Array.from({ length: 21 }, (_, i) => -500 + STEP * i) // −500 … +500
  const bandFill = (lo) => {
    const cost = ['#fbf0ea', '#f7e2d8', '#f2d3c5', '#edc3b1', '#e7b29d', '#e0a189', '#d99075', '#d17f62', '#c96e50', '#c05e40']
    const gain = ['#edf3fa', '#dfeaf6', '#d0e0f2', '#c1d6ed', '#b2cce8', '#a3c2e3', '#94b8de', '#85aed9', '#76a4d4', '#679acf']
    return lo >= 0 ? cost[Math.min(cost.length - 1, lo / STEP)] : gain[Math.min(gain.length - 1, -lo / STEP - 1)]
  }
  const box2 = [58, 520, 18, 372]
  const A2 = scales('k', 'P', box2)
  let fixed2 = $derived({ k: 1, t: taxes, b: benefits })
  let bands2 = $derived(LEVELS.slice(0, -1).map((lo) => {
    const g = gOf(mid, 'k', 'P', fixed2)
    const poly = clip(clip(rectOf('k', 'P'), (x, y) => g(x, y) - lo, 1), (x, y) => g(x, y) - lo - STEP, -1)
    return { lo, poly }
  }).filter((b) => b.poly.length))
  let contours2 = $derived(LEVELS.map((lv) => ({ lv, seg: zeroSegment((x, y) => gOf(mid, 'k', 'P', fixed2)(x, y) - lv, rectOf('k', 'P')) })).filter((c) => c.seg))
  let mixedCost2 = $derived(region('k', 'P', fixed2, 1))
  let mixedGain2 = $derived(region('k', 'P', fixed2, -1))
  let readout = $derived(span(S.map((s) => costAt(s, { k: pt.k, t: taxes, b: benefits, P: pt.P }))))
  let svg2 = $state(null)
  let dragging = $state(false)
  function move(e) {
    if (!dragging || !svg2) return
    const m = svg2.getScreenCTM().inverse()
    const p = new DOMPoint(e.clientX, e.clientY).matrixTransform(m)
    const k = Math.min(1, Math.max(0, (p.x - box2[0]) / (box2[1] - box2[0])))
    const P = Math.min(300, Math.max(0, ((box2[3] - p.y) / (box2[3] - box2[2])) * 300))
    pt = { k, P }
  }
  function reset() { taxes = 1; benefits = 1; pt = { k: 1, P: (mainPf[0] + mainPf[1]) / 2 } }
  function say(r) {
    if (r[0] > 0) return `everyone else is ${rangeBn(r)} a year worse off`
    if (r[1] < 0) return `everyone else is ${rangeBn([-r[1], -r[0]])} a year better off`
    return `the sign depends on the main case’s open choices: from ${bn(r[0])} better off to ${bn(r[1])} worse off`
  }

  /* ---------- Take 3: the same coast from every side ---------- */
  const PAIRS = [['k', 'P'], ['k', 't'], ['k', 'b'], ['t', 'b'], ['t', 'P'], ['b', 'P']]
  const box3 = [34, 214, 10, 150]
  const small = PAIRS.map(([u, v]) => {
    const sc = scales(u, v, box3)
    const cost = region(u, v, MAIN, 1)
    const gain = region(u, v, MAIN, -1)
    const mx = sc.sx(MAIN[u] ?? 0)
    const my = v === 'P' ? [sc.sy(mainPf[0]), sc.sy(mainPf[1])] : [sc.sy(MAIN[v]), sc.sy(MAIN[v])]
    const mxs = u === 'P' ? [sc.sx(mainPf[0]), sc.sx(mainPf[1])] : [mx, mx]
    return { u, v, sc, cost, gain, mxs, my }
  })
</script>

<section class="fig" id="plane">
  <div class="body">
    <p class="kicker">Complete account · main case · two assumptions at a time · after Goh, Distill 2017</p>
    <h2>The break-even line is straight, and the main case sits far from it</h2>
    <p class="lede">
      The account adds up in four quantities: how much public services grow with the group, the taxes they pay, the
      benefits they draw and the gain from their work. Nothing multiplies anything else, so on any plane of two of them
      each of the main case’s {S.length} specifications has a straight break-even line. Three takes on one plane, then
      the same line seen from every side.
    </p>

    <!-- Take 1 -->
    <h3>1 · One hairline per specification</h3>
    <p class="lede">
      Across: how much of the main case’s service growth is charged, from none to all of it. Up: the gain from their
      work. Below the lines everyone else is worse off, above them better off. The main case’s own gain from their
      work, <span class="num">{rangeBn(mainPf)}</span>, is the black mark at the bottom right; the lines cross that height
      when services are charged at <span class="num">{pct(kStar)}</span> of the main case, and reach it at the main case
      only with a gain of <span class="num">{rangeBn(needP)}</span>.
    </p>
    <div class="controls" role="radiogroup" aria-label="Colour the lines by">
      <span>Colour the lines by</span>
      {#each Object.entries(FAMILIES) as [key, f]}
        <label><input type="radio" name="plane-family" value={key} bind:group={family} onchange={() => (focus = null)} /> {f.label}</label>
      {/each}
    </div>
    {#if FAMILIES[family].levels}
      <p class="controls legend">
        {#each FAMILIES[family].levels as [lv, text], i}
          <span role="button" tabindex="0" onmouseenter={() => (focus = lv)} onmouseleave={() => (focus = null)}
            onfocus={() => (focus = lv)} onblur={() => (focus = null)}>
            <svg width="22" height="10" style="display:inline-block;width:22px"><line x1="0" x2="22" y1="5" y2="5" stroke={LEVEL_INK[i]} stroke-width="2" /></svg>
            {text}
          </span>
        {/each}
        <span class="faint-text">hover to fade the others</span>
      </p>
    {/if}
    <div class="scroll">
      <svg class="wide" viewBox="0 0 {W} 410" role="img" aria-label="Break-even lines of every specification on the plane of services charged against the gain from their work">
        <path d={A1.path(cost1)} fill="var(--cost-fill)" opacity="0.55" />
        <path d={A1.path(gain1)} fill="var(--gain-fill)" opacity="0.7" />
        {#each lines1 as { s, seg }}
          {#if seg}
            <line x1={A1.sx(seg[0][0])} y1={A1.sy(seg[0][1])} x2={A1.sx(seg[1][0])} y2={A1.sy(seg[1][1])}
              stroke={ink(s)} stroke-width={focus !== null && s[family] === focus ? 1.3 : 0.8} opacity={opacity(s)} />
          {/if}
        {/each}
        <rect x={box1[0]} y={box1[2]} width={box1[1] - box1[0]} height={box1[3] - box1[2]} fill="none" stroke="var(--hair)" />
        {#each Q.k.ticks as x}
          <text class="faint num" x={A1.sx(x)} y={box1[3] + 16} text-anchor="middle" font-size="11">{Q.k.f(x)}</text>
        {/each}
        {#each Q.P.ticks as y}
          <text class="faint num" x={box1[0] - 6} y={A1.sy(y) + 4} text-anchor="end" font-size="11">{Q.P.f(y)}</text>
        {/each}
        <text class="muted it" x={(box1[0] + box1[1]) / 2} y={box1[3] + 34} text-anchor="middle" font-size="12">services charged, as a share of the main case’s service growth</text>

        <!-- Break-even at the main case's gain from their work -->
        <line x1={A1.sx(kStar[0])} x2={A1.sx(kStar[1])} y1={box1[3] + 3} y2={box1[3] + 3} stroke="var(--ink)" stroke-width="1.5" />
        <!-- The main case -->
        <line x1={A1.sx(1)} x2={A1.sx(1)} y1={A1.sy(mainPf[1]) - 3} y2={A1.sy(mainPf[0]) + 1} stroke="#111" stroke-width="4" />
        <text class="halo num" x={A1.sx(1) - 8} y={A1.sy(mainPf[1]) - 8} text-anchor="end" font-size="12">main case: {rangeBn(d.main)} a year worse off</text>
        <!-- What the gain from their work would have to be -->
        <line x1={A1.sx(1) + 6} x2={A1.sx(1) + 6} y1={A1.sy(needP[1])} y2={A1.sy(needP[0])} stroke="#111" stroke-width="1.2" />
        <text class="num" x={A1.sx(1) + 12} y={A1.sy((needP[0] + needP[1]) / 2) - 4} font-size="11.5">gain it would take</text>
        <text class="num" x={A1.sx(1) + 12} y={A1.sy((needP[0] + needP[1]) / 2) + 10} font-size="11.5">at the main case: {rangeBn(needP)}</text>
        <line x1={A1.sx(1) + 6} x2={A1.sx(1) + 6} y1={A1.sy(d.productionModels[1])} y2={A1.sy(d.productionModels[0])} stroke="#57544c" stroke-width="1.2" />
        <text class="muted num" x={A1.sx(1) + 12} y={A1.sy(d.productionModels[1]) + 2} font-size="11">every model the account ran: {rangeBn(d.productionModels)}</text>

        <text class="it" x={A1.sx(0.1)} y={A1.sy(270)} font-size="13" fill="#2f5f8f">everyone else better off</text>
        <text class="it" x={A1.sx(0.72)} y={A1.sy(95)} font-size="13" fill="#9a4f35">everyone else worse off</text>
        <text class="faint it num" x={A1.sx(kStar[1]) + 6} y={box1[3] - 5} font-size="10.5">break-even at the main case’s gain: {pct(kStar)}</text>
      </svg>
    </div>

    <!-- Take 2 -->
    <h3>2 · The landscape, with dials and a point to drag</h3>
    <p class="lede">
      The same plane as a contour map, one band per $50bn, drawn for the middle of the specifications; the hatched strip is
      where the specifications disagree about the sign. The two dials move what the plane holds fixed. Drag the dot.
    </p>
    <label class="slider"><span>Taxes they pay</span>
      <input type="range" min="0.5" max="2" step="0.01" bind:value={taxes} aria-label="Taxes they pay, as a multiple of what records show" />
      <span class="num">{Math.round(100 * taxes)}% of records</span></label>
    <label class="slider"><span>Benefits they draw</span>
      <input type="range" min="0" max="1.5" step="0.01" bind:value={benefits} aria-label="Benefits they draw, as a multiple of what records show" />
      <span class="num">{Math.round(100 * benefits)}% of records</span></label>
    <p class="lede readout">
      At <span class="num">{Math.round(100 * pt.k)}%</span> of the main case’s services and a gain from their work of
      <span class="num">{bn(pt.P)}</span>, {say(readout)}. <button class="textlink" onclick={reset}>Back to the main case</button>
    </p>
    <div class="scroll">
      <svg class="wide drag" viewBox="0 0 {W} 410" bind:this={svg2} role="img"
        aria-label="Contour map of the cost to everyone else over services charged and the gain from their work"
        onpointermove={move} onpointerup={() => (dragging = false)} onpointerleave={() => (dragging = false)}>
        <defs>
          <pattern id="plane-mixed" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
            <rect width="5" height="5" fill="#bbd4ee" />
            <rect width="2.5" height="5" fill="#f2cabc" />
          </pattern>
          <clipPath id="plane-box2"><rect x={box2[0]} y={box2[2]} width={box2[1] - box2[0]} height={box2[3] - box2[2]} /></clipPath>
        </defs>
        <g clip-path="url(#plane-box2)">
          {#each bands2 as b}
            <path d={A2.path(b.poly)} fill={bandFill(b.lo)} />
          {/each}
          {#each contours2 as c}
            <line x1={A2.sx(c.seg[0][0])} y1={A2.sy(c.seg[0][1])} x2={A2.sx(c.seg[1][0])} y2={A2.sy(c.seg[1][1])}
              stroke={c.lv === 0 ? '#111' : '#fffff8'} stroke-width={c.lv === 0 ? 1.4 : 0.8} opacity={c.lv === 0 ? 0.9 : 0.9} />
          {/each}
          <!-- where the specifications disagree: neither all-cost nor all-gain -->
          <path d={'M' + [box2[0], box2[2]].join(',') + 'H' + box2[1] + 'V' + box2[3] + 'H' + box2[0] + 'Z ' + A2.path(mixedCost2) + ' ' + A2.path(mixedGain2)}
            fill="url(#plane-mixed)" fill-rule="evenodd" opacity="0.9" />
        </g>
        {#each contours2 as c}
          {#if c.lv !== 0 && c.lv % 100 === 0}
            {@const e = c.seg[0][0] > c.seg[1][0] ? c.seg[0] : c.seg[1]}
            {@const top = c.seg[0][1] > c.seg[1][1] ? c.seg[0] : c.seg[1]}
            {#if e[0] > 0.98}
              <text class="faint num" x={box2[1] + 5} y={A2.sy(e[1]) + 4} font-size="10">{c.lv > 0 ? bn(c.lv) + ' worse' : bn(c.lv) + ' better'}</text>
            {:else if top[1] > 299}
              <text class="faint num" x={A2.sx(top[0])} y={box2[2] - 4} text-anchor="middle" font-size="10">{bn(c.lv) + ' better'}</text>
            {/if}
          {/if}
        {/each}
        <rect x={box2[0]} y={box2[2]} width={box2[1] - box2[0]} height={box2[3] - box2[2]} fill="none" stroke="var(--hair)" />
        {#each Q.k.ticks as x}
          <text class="faint num" x={A2.sx(x)} y={box2[3] + 16} text-anchor="middle" font-size="11">{Q.k.f(x)}</text>
        {/each}
        {#each Q.P.ticks as y}
          <text class="faint num" x={box2[0] - 6} y={A2.sy(y) + 4} text-anchor="end" font-size="11">{Q.P.f(y)}</text>
        {/each}
        <text class="muted it" x={(box2[0] + box2[1]) / 2} y={box2[3] + 34} text-anchor="middle" font-size="12">services charged, as a share of the main case’s service growth</text>
        <text class="muted it" x={box2[1] + 5} y={box2[2] + 8} font-size="11">up: gain from their work</text>

        <!-- the main case, and the draggable point -->
        <circle cx={A2.sx(1)} cy={A2.sy((mainPf[0] + mainPf[1]) / 2)} r="3" fill="#111" />
        <circle cx={A2.sx(pt.k)} cy={A2.sy(pt.P)} r="15" fill="transparent" style="cursor: grab"
          onpointerdown={(e) => { dragging = true; e.currentTarget.setPointerCapture?.(e.pointerId) }} />
        <circle cx={A2.sx(pt.k)} cy={A2.sy(pt.P)} r="7" fill="#fffff8" stroke="#111" stroke-width="1.6" pointer-events="none" />
        <circle cx={A2.sx(pt.k)} cy={A2.sy(pt.P)} r="2.5" fill="#111" pointer-events="none" />
      </svg>
    </div>

    <!-- Take 3 -->
    <h3>3 · The same line from every side</h3>
    <p class="lede">
      Six planes, one for each pair of the four quantities, everything else at the main case (the black mark). Blue where
      every specification leaves everyone else better off, orange where every one leaves them worse off, hatched where the
      open choices decide.
    </p>
    <div class="grid3">
      {#each small as p}
        <svg viewBox="0 0 230 196" role="img" aria-label="{Q[p.u].name} against {Q[p.v].name}">
          <defs>
            <pattern id="plane-mixed-{p.u}{p.v}" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">
              <rect width="4" height="4" fill="#bbd4ee" />
              <rect width="2" height="4" fill="#f2cabc" />
            </pattern>
          </defs>
          <rect x={box3[0]} y={box3[2]} width={box3[1] - box3[0]} height={box3[3] - box3[2]} fill="url(#plane-mixed-{p.u}{p.v})" />
          <path d={p.sc.path(p.cost)} fill="var(--cost-fill)" />
          <path d={p.sc.path(p.gain)} fill="var(--gain-fill)" />
          <rect x={box3[0]} y={box3[2]} width={box3[1] - box3[0]} height={box3[3] - box3[2]} fill="none" stroke="var(--hair)" />
          <line x1={p.mxs[0]} x2={p.mxs[1] + 0.01} y1={p.my[1]} y2={p.my[0] + 0.01} stroke="#111" stroke-width="5" stroke-linecap="round" />
          <text class="faint num" x={box3[0]} y={box3[3] + 13} font-size="10">{Q[p.u].f(Q[p.u].axis[0])}</text>
          <text class="faint num" x={box3[1]} y={box3[3] + 13} text-anchor="end" font-size="10">{Q[p.u].f(Q[p.u].axis[1])}</text>
          <text class="faint num" x={box3[0] - 4} y={box3[3]} text-anchor="end" font-size="10">{Q[p.v].f(Q[p.v].axis[0])}</text>
          <text class="faint num" x={box3[0] - 4} y={box3[2] + 8} text-anchor="end" font-size="10">{Q[p.v].f(Q[p.v].axis[1])}</text>
          <text class="it" x={(box3[0] + box3[1]) / 2} y={box3[3] + 28} text-anchor="middle" font-size="11">across: {Q[p.u].name.toLowerCase()}</text>
          <text class="it" x={(box3[0] + box3[1]) / 2} y={box3[3] + 42} text-anchor="middle" font-size="11">up: {Q[p.v].name.toLowerCase()}</text>
        </svg>
      {/each}
    </div>
  </div>

  <aside class="side">
    <p>
      “Services charged” scales every service the main case charges (schools, colleges, police and courts, health,
      welfare offices, housing, general administration) by one factor; roads and culture stay at zero, as in the main case.
      It is a different axis from the staircase’s break-even, which sets every service to one share of its average cost,
      so the two break-even shares differ.
    </p>
    <p>
      Taxes and benefits are multiples of what surveys and records show; the gain from their work is wages, profits and
      the taxes on them.
    </p>
    <p>
      The contour map uses the average of the {S.length} specifications’ coefficients; the hairlines and the hatching use
      every one.
    </p>
    <p>proto/plane.cjs; gates check the formula against the engine at off-axis points and reproduce the main case.</p>
  </aside>
</section>

<style>
  .grid3 { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.6rem 1rem; margin: 0.4rem 0 0.6rem; }
  @media (max-width: 720px) { .grid3 { grid-template-columns: repeat(2, minmax(0, 1fr)); } }
  .legend span[role='button'] { display: inline-flex; align-items: center; gap: 0.35rem; cursor: default; }
  .faint-text { color: var(--faint); font-style: italic; }
  .readout { min-height: 3.2em; }
  .textlink { font: inherit; color: inherit; background: none; border: 0; padding: 0; text-decoration: underline;
    text-decoration-color: var(--faint); text-underline-offset: 0.18em; cursor: pointer; }
  svg.drag { touch-action: none; }
</style>
