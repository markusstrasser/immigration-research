<script>
  import data from '../generated/proto_nomogram.json'

  const { k, main, spec, high, order, geometry, spread, dials } = data
  const { W, H, top, x, mod, ticks } = geometry

  // Every scale reads 0 on the top line and grows downward; a depth is dollars times the scale's
  // modulus. So the cost scale runs from better off at the top to worse off at the bottom.
  const yS = (v) => top + mod.S * k.a * v
  const yO = (v) => top + mod.O * k.b * v
  const yG = (v) => top + mod.G * k.g * v
  const yT = (v) => top + mod.T * v
  const yC = (c) => top + mod.C * (c - k.c0)

  // The construction, as proto/nomogram.cjs gates it: the straightedge from schools to the other
  // services crosses the turning line; the one from there through general administration reads the
  // cost scale.
  const at = (p, q, xx) => p[1] + ((q[1] - p[1]) * (xx - p[0])) / (q[0] - p[0])
  function construct(s, o, g) {
    const S = [x.S, yS(s)]
    const O = [x.O, yO(o)]
    const G = [x.G, yG(g)]
    const T = [x.T, at(S, O, x.T)]
    const C = [x.C, at(T, G, x.C)]
    return { S, O, T, G, C, cost: k.c0 + (C[1] - top) / mod.C }
  }

  let s = $state(main.s)
  let o = $state(main.o)
  let g = $state(main.g)
  const live = $derived(construct(s, o, g))
  const home = construct(main.s, main.o, main.g)
  const atHome = $derived(s === main.s && o === main.o && g === main.g)
  // The band: the lowest and highest of the 16 combinations of the other open choices at the
  // current dials (each a plane in the dials, gated in the generator).
  const range = $derived.by(() => {
    const v = spread.map((q) => q.c0 + q.a * s + q.b * o + q.g * g)
    return [Math.min(...v), Math.max(...v)]
  })
  function reset() {
    s = main.s
    o = main.o
    g = main.g
  }

  // Graduations. Share scales: [minor, middle, major, labelled] steps on 0..1.
  const share = (v) => (v === 0 ? '0' : v === 1 ? '1' : v.toFixed(1))
  function shareTicks([minor, mid, major, lab]) {
    const n = Math.round(1 / minor)
    const every = (step) => Math.round(step / minor)
    return Array.from({ length: n + 1 }, (_, i) => ({
      v: i / n,
      size: i % every(major) === 0 ? 2 : i % every(mid) === 0 ? 1 : 0,
      label: i % every(lab) === 0 ? share(i / n) : null,
    }))
  }
  // The cost scale's numbers carry no sign: the words at its ends say which side is which.
  function costTicks([minor, mid, major, lab]) {
    const out = []
    for (let j = Math.ceil(k.c0 / minor); j * minor <= data.ceiling; j++) {
      const v = j * minor
      out.push({ v, size: v % major === 0 ? 2 : v % mid === 0 ? 1 : 0, label: v % lab === 0 ? String(Math.abs(v)) : null })
    }
    return out
  }
  const TICK = [3.4, 6, 9.5]
  const TICK_W = [0.45, 0.6, 0.9]
  const tickS = shareTicks(ticks.S)
  const tickO = shareTicks(ticks.O)
  const tickG = shareTicks(ticks.G)
  const tickC = costTicks(ticks.C)

  // The sign's colours (README, "Visual grammar").
  const WORSE = ['#f2cabc', '#ca7a5e']
  const BETTER = ['#bbd4ee', '#5c97d2']
  const BETTER_TEXT = '#2f5f8f'
  const EVEN = ['#ecdcae', '#b8913a']
  const REF = ['#e4e1d6', '#57544c']
  // The band's colour is its sign; ochre when the combinations disagree.
  const tone = $derived(range[0] > 0 ? WORSE : range[1] < 0 ? BETTER : EVEN)

  // Words and numbers for the text, all from the generator.
  const one = (v) => Math.abs(v).toFixed(1)
  // Word joiners keep a range on one line.
  function inWords([lo, hi]) {
    if (lo >= 0) return `$${one(lo)}⁠–⁠${one(hi)}bn worse off`
    if (hi <= 0) return `$${one(hi)}⁠–⁠${one(lo)}bn better off`
    return `from $${one(lo)}bn better off to $${one(hi)}bn worse off`
  }
  const pct = (v) => Math.round(100 * v) + '%'
  const perHead = (c) => '$' + Math.round(Math.abs((c * 1e9) / data.residents)).toLocaleString('en-US')
  const millions = Math.round(data.residents / 1e6)
  const terms = [
    { v: k.a, name: 'schools' },
    { v: k.b, name: 'every other service' },
    { v: k.g, name: 'general administration' },
  ]

  // The construction draws itself once when the plate scrolls into view: the first straightedge,
  // the turning point, the second straightedge, the reading. Reduced motion skips it.
  let p = $state(1)
  let plate = $state()
  let raf = 0
  $effect(() => {
    if (!plate || typeof IntersectionObserver === 'undefined') return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return
    p = 0
    let start = 0
    const io = new IntersectionObserver(
      (entries) => {
        if (!entries.some((e) => e.isIntersecting)) return
        io.disconnect()
        const step = (t) => {
          start ||= t
          p = Math.min(1, (t - start) / 1700)
          if (p < 1) raf = requestAnimationFrame(step)
        }
        raf = requestAnimationFrame(step)
      },
      { threshold: 0.3 },
    )
    io.observe(plate)
    return () => {
      io.disconnect()
      cancelAnimationFrame(raf)
    }
  })
  function finish() {
    cancelAnimationFrame(raf)
    p = 1
  }
  const clamp = (v) => Math.max(0, Math.min(1, v))
  const toward = (P, Q, f) => [P[0] + f * (Q[0] - P[0]), P[1] + f * (Q[1] - P[1])]
  const first = $derived(clamp(p / 0.4))
  const second = $derived(clamp((p - 0.5) / 0.38))
  const shown = $derived(p >= 0.92)

  // The reading's label sits on the side of the second straightedge away from the line, and below
  // it near the top line, where the titles are.
  const below = $derived(live.G[1] < live.T[1] || live.C[1] - top < 24)
  const better = $derived(live.cost < 0)
  // For the current general administration, a first straightedge that crosses the turning line
  // above v0 leaves everyone else better off (the generator gates this break-even).
  const v0 = $derived(-k.c0 - k.g * g)
</script>

{#snippet scale(xx, y, list, side, from, to)}
  <line x1={xx} x2={xx} y1={y(from)} y2={y(to)} stroke="#111" stroke-width="0.9" />
  {#each list as t}
    <line x1={xx} x2={xx + side * TICK[t.size]} y1={y(t.v)} y2={y(t.v)} stroke="#111" stroke-width={TICK_W[t.size]} />
  {/each}
{/snippet}

<!-- Labels go on after the straightedges, with a paper halo, so a line passing a label never hides it. -->
{#snippet labels(xx, y, list, side)}
  {#each list.filter((t) => t.label) as t}
    <text class="num halo" x={xx + side * (TICK[2] + 3.5)} y={y(t.v) + 3.9} text-anchor={side < 0 ? 'end' : 'start'} font-size="11">{t.label}</text>
  {/each}
{/snippet}

<!-- A band along one side of a scale, from depth y1 to y2. -->
{#snippet strip(xx, side, y1, y2, [fill, stroke])}
  <rect x={side < 0 ? xx - 6 : xx} y={Math.min(y1, y2)} width="6" height={Math.abs(y2 - y1)} {fill} {stroke} stroke-width="0.7" />
{/snippet}

<section class="fig" id="nomogram">
  <div class="body">
    <p class="kicker">Prototype · nomogram · the main case’s low end</p>
    <h2>Only budgets that barely grow leave everyone else better off</h2>
    <p class="lede">
      Three dials set the bill: schools, every other public service, and general administration. Each
      runs from 0, the budget does not grow for the group, to 1, it grows one for one with the
      population; for schools, 1 is the usual cost per pupil. A straightedge from schools to the other
      services crosses the turning line. A second, from there through general administration, reads how
      much better or worse off everyone else is.
    </p>
    <p class="lede">
      Hold every budget fixed and both lines lie flat along the top: counting taxes, benefits and the gain
      from the group’s work, everyone else is <span class="num">${Math.round(-data.frozen)}bn</span> a year better off.
      The three dials together can add <span class="num">${Math.round(k.a + k.b + k.g)}bn</span>, so with all three
      at one value everyone else breaks even at <span class="num">{data.zero.toFixed(2)}</span>. Schools alone at
      CBO’s <span class="num">{main.s}</span> already leave everyone else <span class="num">${Math.round(data.schoolsAlone)}bn</span>
      worse off. At the main case’s settings the chart reads <span class="num">${one(main.cost)}bn</span> worse off,
      the low end of the main case’s <span class="num">${Math.round(data.band[0])}–{Math.round(data.band[1])}bn</span>.
    </p>

    <div class="dials">
      <label for="nomo-s">Schools</label>
      <input id="nomo-s" type="range" min="0" max="1" step="0.01" bind:value={s} oninput={finish} />
      <output class="num" for="nomo-s">{s.toFixed(2)}</output>
      <label for="nomo-o">Every other service</label>
      <input id="nomo-o" type="range" min="0" max="1" step="0.01" bind:value={o} oninput={finish} />
      <output class="num" for="nomo-o">{o.toFixed(2)}</output>
      <label for="nomo-g">General administration</label>
      <input id="nomo-g" type="range" min="0" max="1" step="0.01" bind:value={g} oninput={finish} />
      <output class="num" for="nomo-g">{g.toFixed(2)}</output>
    </div>
    <p class="readout" aria-live="polite">
      Everyone else <b style:color={better ? BETTER_TEXT : null}>${one(live.cost)}bn</b> a year
      {better ? 'better' : 'worse'} off: about {perHead(live.cost)} for each of the {millions} million other residents.
      <br />
      <span class="band">Across the other open choices (the band): {inWords(range)}.</span>
      {#if atHome}
        <span class="muted">Main-case settings.</span>
      {:else}
        <button type="button" onclick={reset}>Back to the main case</button>
      {/if}
    </p>

    <!-- Observed for the drawing: the scroll box, since it clips the plate's width on a phone. -->
    <div class="scroll" bind:this={plate}>
    <svg
      class="wide"
      viewBox="0 0 {W} {H}"
      role="img"
      aria-label="Alignment chart with scales for schools, every other service, general administration and the result for everyone else. The straightedges read ${one(live.cost)}bn a year {better ? 'better' : 'worse'} off; the band for the other open choices runs {inWords(range)}."
    >
      <!-- Every budget fixed: the top line, where every scale reads 0. -->
      <line x1={x.S} x2={x.G} y1={top} y2={top} stroke="#efece2" />

      <!-- The turning line has no graduation. For the drawn combination at the current general
           administration, a first straightedge crossing its blue top leaves everyone else better off;
           the ochre mark is break-even. -->
      <line x1={x.T} x2={x.T} y1={yT(0)} y2={yT(k.a + k.b)} stroke="#8d897e" stroke-width="0.7" />
      {#if v0 > 0}
        <rect x={x.T - 3} y={yT(0)} width="6" height={yT(v0) - yT(0)} fill={BETTER[0]} stroke={BETTER[1]} stroke-width="0.7" />
        <line x1={x.T - 7} x2={x.T + 7} y1={yT(v0)} y2={yT(v0)} stroke={EVEN[1]} stroke-width="2" />
      {/if}

      <!-- The result scale's sign: blue above break-even, orange below. -->
      {@render strip(x.C, -1, yC(k.c0), yC(0), BETTER)}
      {@render strip(x.C, -1, yC(0), yC(data.ceiling), WORSE)}
      <!-- The main case's own choices for two dials: a neutral reference. -->
      {@render strip(x.S, 1, yS(dials.school[0]), yS(dials.school[1]), REF)}
      {@render strip(x.G, -1, yG(dials.gg[0]), yG(dials.gg[1]), REF)}
      <!-- The band: every combination of the other open choices at the current dials, one even tint
           between its two ends, in the colour of its sign, twice the width of the sign strip it
           covers. -->
      <rect
        x={x.C - 12}
        y={yC(range[0])}
        width="12"
        height={Math.max(1.5, yC(range[1]) - yC(range[0]))}
        fill={tone[0]}
        stroke={tone[1]}
        stroke-width="0.9"
      />

      <!-- Scales. -->
      {@render scale(x.S, yS, tickS, -1, 0, 1)}
      {@render scale(x.O, yO, tickO, -1, 0, 1)}
      {@render scale(x.G, yG, tickG, 1, 0, 1)}
      {@render scale(x.C, yC, tickC, 1, k.c0, data.ceiling)}
      <line x1={x.C} x2={x.C} y1={yC(k.c0)} y2={yC(data.ceiling)} stroke="#111" stroke-width="1.5" />
      <line x1={x.C - 12} x2={x.C + 12} y1={yC(0)} y2={yC(0)} stroke="#111" stroke-width="1.3" />

      <!-- The main case, left as a faint trace once the dials move. -->
      {#if !atHome}
        <line x1={home.S[0]} y1={home.S[1]} x2={home.O[0]} y2={home.O[1]} stroke="#8d897e" stroke-width="0.7" opacity="0.7" />
        <line x1={home.T[0]} y1={home.T[1]} x2={home.G[0]} y2={home.G[1]} stroke="#8d897e" stroke-width="0.7" opacity="0.7" />
      {/if}

      <!-- The two straightedges. -->
      {#if first > 0}
        {@const e = toward(live.S, live.O, first)}
        <line x1={live.S[0]} y1={live.S[1]} x2={e[0]} y2={e[1]} stroke="#111" stroke-width="1.05" />
      {/if}
      {#if second > 0}
        {@const e = toward(live.T, live.G, second)}
        <line x1={live.T[0]} y1={live.T[1]} x2={e[0]} y2={e[1]} stroke="#111" stroke-width="1.05" />
      {/if}

      <!-- Words and numbers over the lines. -->
      {@render labels(x.S, yS, tickS, -1)}
      {@render labels(x.O, yO, tickO, -1)}
      {@render labels(x.G, yG, tickG, 1)}
      {@render labels(x.C, yC, tickC, 1)}
      <text class="faint it halo" x={x.C - 17} y={(yC(k.c0) + yC(0)) / 2 + 4} text-anchor="end" font-size="11">better off ↑</text>
      <text class="faint it halo" x={x.C - 17} y={yC(0) + 4} text-anchor="end" font-size="11">break-even</text>
      <!-- Below the scale's end no straightedge passes: from any reading the second line runs up and
           away from here on both sides. -->
      <text class="faint it halo" x={x.C} y={yC(data.ceiling) + 17} text-anchor="middle" font-size="11">worse off ↓</text>
      {#if v0 > 0}
        <text class="it halo" x={x.T - 7} y={(yT(0) + yT(v0)) / 2 + 4} text-anchor="end" font-size="11" style:fill={BETTER_TEXT}>better off</text>
      {/if}
      <text class="faint it halo" x={x.T} y={yT(k.a + k.b) + 16} text-anchor="middle" font-size="11">turning line</text>
      <text class="faint it" x={x.S - 40} y={yS(1) + 26} font-size="11">On each dial, 0: the budget does not grow for the group;</text>
      <text class="faint it" x={x.S - 40} y={yS(1) + 40} font-size="11">1: it grows one for one with the population.</text>

      <!-- Titles above the top line, where no straightedge goes; two tiers keep them apart. -->
      <text class="it" x={x.S} y={top - 42} text-anchor="middle" font-size="14">Schools</text>
      <text class="muted" x={x.S} y={top - 28} text-anchor="middle" font-size="11">share of the usual</text>
      <text class="muted" x={x.S} y={top - 14} text-anchor="middle" font-size="11">cost per pupil</text>
      <text class="it" x={x.O - 22} y={top - 42} font-size="14">Every other service</text>
      <text class="muted" x={x.O - 22} y={top - 28} font-size="11">colleges, police, courts, prisons,</text>
      <text class="muted" x={x.O - 22} y={top - 14} font-size="11">public health, welfare, housing</text>
      <text class="it" x={x.C} y={top - 76} text-anchor="middle" font-size="14">Everyone else</text>
      <text class="muted" x={x.C} y={top - 62} text-anchor="middle" font-size="11">$bn a year</text>
      <text class="it" x={x.G + 30} y={top - 42} text-anchor="end" font-size="14">General administration</text>
      <text class="muted" x={x.G + 30} y={top - 28} text-anchor="end" font-size="11">share of its usual cost</text>

      <!-- The key and what the chart solves, in words: the plate's open field, which no straightedge
           reaches. -->
      <rect x="470" y={top + 386} width="12" height="12" fill={tone[0]} stroke={tone[1]} stroke-width="0.9" />
      <text class="muted it" x="490" y={top + 396} font-size="12">the band: every combination of</text>
      <text class="muted it" x="490" y={top + 410} font-size="12">the other open choices, at these settings</text>
      <g class="formula">
        <text class="muted it" x="470" y={top + 440} font-size="12">The chart weighs, in $bn a year,</text>
        {#each terms as t, i}
          <text class="num" x="470" y={top + 460 + 18 * i} font-size="12.5">{i ? '+' : ''}</text>
          <text class="num" x="540" y={top + 460 + 18 * i} text-anchor="end" font-size="12.5">{one(t.v)}</text>
          <text x="548" y={top + 460 + 18 * i} font-size="12.5"><tspan class="muted">×</tspan> <tspan class="it">{t.name}</tspan></text>
        {/each}
        <text x="470" y={top + 518} font-size="12.5">against <tspan class="num">{one(k.c0)}</tspan>, everyone else’s gain</text>
        <text x="470" y={top + 534} font-size="12.5">with every budget fixed.</text>
      </g>

      <!-- Pins where the straightedges meet the scales. -->
      {#each [live.S, live.O, live.G] as q}
        <circle cx={q[0]} cy={q[1]} r="3.3" fill="#fffff8" stroke="#111" stroke-width="1" />
      {/each}
      {#if p >= 0.4}
        <circle cx={live.T[0]} cy={live.T[1]} r="2.4" fill="#111" />
      {/if}
      {#if shown}
        {@const c = better ? BETTER : WORSE}
        <circle cx={live.C[0]} cy={live.C[1]} r="4" fill={c[0]} stroke={c[1]} stroke-width="1.2" />
        <text class="num halo reading" x={x.C + 40} y={live.C[1] + (below ? 15 : -7)} font-size="13" font-weight="700" style:fill={better ? BETTER_TEXT : null}>
          ${one(live.cost)}bn {better ? 'better' : 'worse'} off
        </text>
      {/if}
    </svg>
    </div>

    <p class="note">
      Drawn for one combination of the account’s open choices, the one most favourable to the group at the
      main case: {spec.words[0]}, {spec.words[1]}, schools as {pct(spec.share)} of education spending, and
      {spec.words[2]}. The band beside the result scale spans all {spread.length} combinations of these four
      choices at the dials’ settings, as one even tint in the colour of its sign: orange when every
      combination leaves everyone else worse off, blue when every one leaves them better off, ochre when
      they disagree. The main case also leaves two dials open, marked grey: schools at
      {dials.school[0]}–{dials.school[1]} and general administration at {dials.gg[0]}–{dials.gg[1]}. Its other end,
      <span class="num">${one(high.cost)}bn</span> worse off, takes {high.words[0]}, {high.words[1]}, schools as
      {pct(high.share)} of education spending, the schools dial at {high.school}, general administration at
      {high.gg} and {high.words[2]}. Every other service sits at {main.o}. Roads, transport and parks stay fixed
      and the gain from the group’s work is counted, as in the main case.
    </p>
  </div>

  <aside class="side">
    <p>
      Each dial’s scale has the same length per dollar, so its length is the most that dial can add to the
      bill. The turning line sits halfway between schools and the other services. The scale for everyone
      else sits a third of the way from the turning line to general administration and has a third of the
      length per dollar. Every scale reads 0 on the top line.
    </p>
    <p>
      Colour is the sign: blue where everyone else is better off, orange where they are worse off, ochre at
      break-even or where the open choices disagree. The blue top of the turning line moves with general
      administration: for the drawn combination, a first straightedge that crosses it there leaves everyone
      else better off, and the ochre mark is break-even.
    </p>
    <p>
      Away from the main case the drawn combination is not always the lowest: with the schools dial at
      {order.s} and every other budget fixed, schools as {pct(order.share)} of education spending cost
      everyone else <span class="num">${Math.round(order.gap)}bn</span> less, and the band reaches that far above
      the reading.
    </p>
    <p>
      proto/nomogram.cjs runs the explorer’s engine (account.cjs) at the corners of the three dials for each
      of the {spread.length} combinations. Its gates: the corners predict other settings to 1e-9; the drawn
      construction reads the main case and the frozen setting exactly and matches the engine at 20 random
      settings; over the main case’s own dial choices the band spans its
      <span class="num">${Math.round(data.band[0])}–{Math.round(data.band[1])}bn</span>.
    </p>
  </aside>
</section>

<style>
  .dials {
    display: grid;
    grid-template-columns: auto minmax(5rem, 1fr) 2.4em;
    gap: 0.2rem 0.9rem;
    align-items: center;
    max-width: 36rem;
    margin: 0.6rem 0 0.4rem;
    font-size: 0.92rem;
    color: var(--muted);
  }
  .dials input { width: 100%; margin: 0; }
  .dials output { color: var(--ink); text-align: right; }
  .readout { max-width: 40rem; margin: 0.2rem 0 0.8rem; font-size: 0.95rem; }
  .readout b { font-weight: 700; }
  .readout .muted { color: var(--muted); font-style: italic; margin-left: 0.3rem; white-space: nowrap; }
  .readout .band { color: var(--muted); font-size: 0.9rem; }
  .readout button {
    font: inherit;
    font-size: 0.85rem;
    margin-left: 0.4rem;
    padding: 0.05rem 0.45rem;
    color: var(--muted);
    background: var(--paper);
    border: 1px solid var(--hair);
    border-radius: 3px;
    cursor: pointer;
    white-space: nowrap;
  }
  .readout button:hover { color: var(--ink); border-color: var(--faint); }
  /* On a phone the plate scrolls sideways and the reading label would sit at the cut edge; the
     readout above the plate carries the number. */
  @media (max-width: 720px) {
    .reading { display: none; }
  }
</style>
