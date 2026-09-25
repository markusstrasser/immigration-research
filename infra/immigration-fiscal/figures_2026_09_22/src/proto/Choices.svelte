<script>
  import d from '../generated/proto_choices.json'

  const { lo: LO, hi: HI, bin: BIN } = d.axis
  const NB = (HI - LO) / BIN

  const W = 760
  const X0 = 222
  const X1 = 742
  const R = 2.35
  const STEP = 5.3
  const sx = (x) => X0 + ((x - LO) / (HI - LO)) * (X1 - X0)
  const binX = (j) => sx(LO + (j + 0.5) * BIN)
  const worse = (j) => LO + j * BIN >= 0

  // Numbers in words: no signs.
  const bn = (x) => '$' + Math.round(Math.abs(x)) + 'bn'
  function span(r) {
    const [a, b] = r
    if (a >= 0) return `$${Math.round(a)}–${Math.round(b)}bn worse off`
    if (b <= 0) return `$${Math.round(-b)}–${Math.round(-a)}bn better off`
    return `${bn(a)} better off to ${bn(b)} worse off`
  }
  const avg = (x) => (x >= 0 ? `${bn(x)} worse off` : `${bn(x)} better off`)
  const millions = (n) => (n / 1e6).toFixed(1) + ' million'

  // Largest-remainder rounding: integer counts that sum to n.
  function apportion(weights, n) {
    const tot = weights.reduce((a, b) => a + b, 0)
    if (tot <= 0) return weights.map(() => 0)
    const raw = weights.map((w) => (w / tot) * n)
    const out = raw.map(Math.floor)
    let left = n - out.reduce((a, b) => a + b, 0)
    raw.map((r, i) => [r - Math.floor(r), i]).sort((a, b) => b[0] - a[0]).slice(0, left).forEach(([, i]) => (out[i] += 1))
    return out
  }

  // A heap: per bin, a column of dots; each dot knows its level (for the top heap) and its side.
  function heap(counts, levelOf = () => -1) {
    const dots = []
    let tallest = 0
    counts.forEach((n, j) => {
      for (let k = 0; k < n; k++) dots.push({ j, k, level: levelOf(j, k), worse: worse(j) })
      tallest = Math.max(tallest, n)
    })
    return { dots, tallest }
  }

  const TOP_N = 200
  const ROW_N = 100

  let pick = $state('services')
  let focus = $state(null)
  const fam = $derived(d.families.find((f) => f.id === pick) || null)

  // The top heap, every combination; with a split chosen, each column's dots are shared out among the levels.
  const top = $derived.by(() => {
    const counts = apportion(d.all.hist, TOP_N)
    if (!fam) return heap(counts)
    const byBin = counts.map((n, j) => {
      const per = apportion(fam.levels.map((l) => l.hist[j]), n)
      const seq = []
      per.forEach((m, i) => { for (let k = 0; k < m; k++) seq.push(i) })
      return seq
    })
    return heap(counts, (j, k) => byBin[j][k])
  })

  // One heap per level, each 100 dots of that level's own combinations.
  const rows = $derived(fam ? fam.levels.map((l, i) => ({ ...l, i, ...heap(apportion(l.hist, ROW_N)) })) : [])

  // Vertical layout.
  const TOP_Y0 = 30
  const layout = $derived.by(() => {
    const topBase = TOP_Y0 + Math.max(8, top.tallest) * STEP + 6
    let y = topBase + 46
    const placed = rows.map((r) => {
      const h = Math.max(r.tallest * STEP + 8, 38)
      const base = y + h
      y = base + 16
      return { ...r, base, h }
    })
    return { topBase, placed, bottom: y + 6 }
  })

  const effectMax = Math.max(...d.families.map((f) => f.effect))
  const means = $derived(fam ? fam.levels.filter((l) => !(fam.among && l.id === 'none')).map((l) => l.mean) : [])

  function fillOf(dot, faded) {
    if (faded) return 'none'
    return dot.worse ? '#f2cabc' : '#bbd4ee'
  }
  function strokeOf(dot, faded) {
    if (faded) return '#d6d2c4'
    return dot.worse ? '#ca7a5e' : '#5c97d2'
  }

  /* The static sum: start at the least costly combination where services grow, add each choice. */
  const wf = d.waterfall
  const WX0 = 268
  const WX1 = 652
  const wx = (x) => WX0 + ((x - LO) / (HI - LO)) * (WX1 - WX0)
  const WROW = 31
  const WTOP = 34
  const wRows = [
    { kind: 'dot', label: 'Least costly option on every choice', sub: 'while public services grow', at: wf.start },
    ...wf.steps.map((st) => ({ kind: 'step', label: st.label, sub: `${st.from} → ${st.to}`, from: st.at[0], to: st.at[1], add: st.add })),
    { kind: 'dot', label: 'Most costly option on every choice', sub: 'the end of the sum', at: wf.end },
  ].map((r, i) => ({ ...r, y: WTOP + i * WROW }))
  const freezeY = WTOP + wRows.length * WROW + 20
  const wBottom = freezeY + 24
  const more = (x) => (x < 0.5 ? 'under $1bn' : '$' + Math.round(x) + 'bn')
</script>

<section class="fig" id="choices-sum">
  <div class="body">
    <p class="kicker">Complete account · every combination of its choices · read as a sum</p>
    <h2>Every choice at its least costly still leaves everyone else {bn(wf.start)} a year worse off</h2>
    <p class="lede">
      The account adds up, so its choices can be read as a sum. Take the least costly option on every choice while
      public services grow with the group: everyone else is <span class="num">{bn(wf.start)}</span> a year worse off.
      Switching each choice to its most costly option adds the amounts below, up to <span class="num">{bn(wf.end)}</span>.
      The one move that crosses zero is stopping public services from growing at all.
    </p>
    <div class="scroll">
      <svg class="wide" viewBox="0 0 {W} {wBottom + 40}" role="img" aria-label="The account's choices as a sum, from the least costly to the most costly combination">
        <line x1={wx(0)} x2={wx(0)} y1={WTOP - 22} y2={wBottom} stroke="#111" stroke-width="1" />
        <!-- the adopted main case -->
        <line x1={wx(d.main[0])} x2={wx(d.main[1])} y1={WTOP - 16} y2={WTOP - 16} stroke="#111" stroke-width="2" />
        <text class="num" x={wx(d.main[0]) - 6} y={WTOP - 12} text-anchor="end" font-size="11">main case, {span(d.main)}</text>

        {#each wRows as r, i}
          <text x="0" y={r.y + 4} font-size="12.5">{r.label}</text>
          <text class="faint it" x="0" y={r.y + 17} font-size="10.5">{r.sub}</text>
          {#if r.kind === 'dot'}
            <circle cx={wx(r.at)} cy={r.y + 6} r="4" fill="#111" />
            <text class="num" x={wx(r.at) + 9} y={r.y + 10} font-size="11.5">{bn(r.at)} worse off</text>
          {:else}
            <!-- the connector from the previous row's end -->
            <line x1={wx(r.from)} x2={wx(r.from)} y1={r.y - WROW + 12} y2={r.y} stroke="#8d897e" stroke-width="0.7" stroke-dasharray="2 2" />
            <rect x={wx(r.from)} y={r.y} width={Math.max(1.5, wx(r.to) - wx(r.from))} height="12" fill="#f2cabc" stroke="#ca7a5e" stroke-width="0.8" />
            <text class="num" x={wx(r.to) + 6} y={r.y + 10} font-size="11.5">{more(r.add)} more</text>
          {/if}
        {/each}
        <line x1={wx(wf.end)} x2={wx(wf.end)} y1={wRows.at(-2).y + 12} y2={wRows.at(-1).y + 2} stroke="#8d897e" stroke-width="0.7" stroke-dasharray="2 2" />

        <!-- the one move that crosses zero -->
        <line x1="0" x2={W} y1={freezeY - 12} y2={freezeY - 12} stroke="#dcd8c8" stroke-width="0.8" />
        <text x="0" y={freezeY + 4} font-size="12.5">Instead, stop public services growing</text>
        <text class="faint it" x="0" y={freezeY + 17} font-size="10.5">from the least costly option on every choice</text>
        <rect x={wx(wf.freeze)} y={freezeY} width={wx(wf.start) - wx(wf.freeze)} height="12" fill="#bbd4ee" stroke="#5c97d2" stroke-width="0.8" />
        <line x1={wx(wf.start)} x2={wx(wf.start)} y1={WTOP + 10} y2={freezeY} stroke="#8d897e" stroke-width="0.7" stroke-dasharray="2 2" />
        <text class="num" x={wx(wf.start) + 6} y={freezeY + 10} font-size="11.5" fill="#2f5f8f">{bn(wf.start - wf.freeze)} less: {bn(wf.freeze)} better off</text>

        {#each [-100, 0, 100, 200, 300] as t}
          <line x1={wx(t)} x2={wx(t)} y1={wBottom} y2={wBottom + 4} stroke="#8d897e" stroke-width="0.8" />
          <text class="faint num" x={wx(t)} y={wBottom + 16} text-anchor="middle" font-size="11">{t === 0 ? '0' : bn(t)}</text>
        {/each}
        <text class="muted it" x={wx(-100)} y={wBottom + 32} font-size="11.5">← everyone else better off</text>
        <text class="muted it" x={WX1} y={wBottom + 32} text-anchor="end" font-size="11.5">everyone else worse off →</text>
      </svg>
    </div>
    <p class="note">
      Nothing here is picked by hand: the start is the least costly of the combinations in which services grow, the end the
      most costly, and each bar is the engine’s difference between one combination and the next.
    </p>
  </div>

  <aside class="side">
    <p>
      The rows run in order of how far each choice moves the average across all combinations. A step can depend on the
      ones before it: the schools’ share of education adds under $1bn here because schools and colleges already grow fully.
    </p>
    <p>
      Stopping services from growing means schools, police, courts, health, welfare, colleges and roads all held still.
    </p>
    <p>proto/choices.cjs; gates check that the steps start and end at the least and most costly combinations.</p>
  </aside>
</section>

<section class="fig" id="choices">
  <div class="body">
    <p class="kicker">Complete account · every combination of its choices · after Distill’s explorable figures</p>
    <h2>One choice sets the sign: whether public services grow with the group</h2>
    <p class="lede">
      The account has run <span class="num">{millions(d.counts.total)}</span> combinations of its choices:
      {d.counts.services} settings of which public services grow with the group, {d.counts.administration} of general
      administration, {d.counts.choices.toLocaleString('en-US')} of how taxes, police, courts and unpaid hospital care are
      charged and how household money is counted, and {d.counts.production} models of the gain from their work.
      Every combination in which public services grow leaves everyone else
      <span class="num">{span([d.gap[1], d.all.range[1]])}</span> a year. Every one in which they do not leaves them
      <span class="num">{span([d.all.range[0], d.gap[0]])}</span>. None lands in between.
    </p>

    <div class="pick" role="radiogroup" aria-label="Split every combination by">
      <p class="pick-head">Split every combination by <span class="faint-text">(the bar shows how far each choice moves the average)</span></p>
      <label><input type="radio" name="choices-split" value="" bind:group={pick} onchange={() => (focus = null)} /> nothing</label>
      {#each d.families as f}
        <label>
          <input type="radio" name="choices-split" value={f.id} bind:group={pick} onchange={() => (focus = null)} />
          <span class="pick-label">{f.label}</span>
          <svg class="pick-bar" viewBox="0 0 130 10" aria-hidden="true"><rect x="0" y="2" width={Math.max(1, (130 * f.effect) / effectMax)} height="6" fill="#57544c" /></svg>
          <span class="num pick-num">{bn(f.effect)}</span>
        </label>
      {/each}
    </div>

    <div class="scroll">
      <svg class="wide" viewBox="0 0 {W} {layout.bottom + 40}" role="img" aria-label="Heaps of combinations along the cost to everyone else, split by one choice">
        <!-- the zero line, through every heap -->
        <line x1={sx(0)} x2={sx(0)} y1={TOP_Y0 - 14} y2={layout.bottom} stroke="#111" stroke-width="1" />

        <!-- every combination -->
        <text x="0" y={layout.topBase - 22} font-size="12.5">Every combination</text>
        <text class="faint it" x="0" y={layout.topBase - 8} font-size="10.5">each dot 0.5% of them</text>
        {#each top.dots as dot}
          {@const faded = focus !== null && dot.level !== focus}
          <circle cx={binX(dot.j)} cy={layout.topBase - (dot.k + 0.5) * STEP} r={R} fill={fillOf(dot, faded)} stroke={strokeOf(dot, faded)} stroke-width="0.6" />
        {/each}
        <!-- the empty stretch between the two halves -->
        <line x1={sx(d.gap[0])} x2={sx(d.gap[1])} y1={layout.topBase + 7} y2={layout.topBase + 7} stroke="#8d897e" stroke-width="0.8" />
        <line x1={sx(d.gap[0])} x2={sx(d.gap[0])} y1={layout.topBase + 4} y2={layout.topBase + 10} stroke="#8d897e" stroke-width="0.8" />
        <line x1={sx(d.gap[1])} x2={sx(d.gap[1])} y1={layout.topBase + 4} y2={layout.topBase + 10} stroke="#8d897e" stroke-width="0.8" />
        <text class="muted it" x={(sx(d.gap[0]) + sx(d.gap[1])) / 2 + 4} y={layout.topBase + 22} text-anchor="middle" font-size="10.5">none lands here</text>
        <!-- the adopted main case -->
        <line x1={sx(d.main[0])} x2={sx(d.main[1])} y1={TOP_Y0 - 10} y2={TOP_Y0 - 10} stroke="#111" stroke-width="2" />
        <text class="num" x={sx(d.main[0]) - 6} y={TOP_Y0 - 6} text-anchor="end" font-size="11">main case, {span(d.main)}</text>

        <!-- one heap per level of the chosen choice -->
        {#if fam}
          <text class="it" x="0" y={layout.topBase + 40} font-size="12.5">Split by {fam.label}</text>
          {#each layout.placed as row}
            <g role="presentation" onmouseenter={() => (focus = row.i)} onmouseleave={() => (focus = null)}>
              <rect x="0" y={row.base - row.h} width={W} height={row.h + 12} fill={focus === row.i ? '#f4f1e6' : 'transparent'} />
              <text x="0" y={row.base - row.h / 2 + 1} font-size="12.5">{row.label}</text>
              <text class="faint num" x="0" y={row.base - row.h / 2 + 15} font-size="10.5">{span(row.range)}</text>
              <line x1={X0} x2={X1} y1={row.base + 0.5} y2={row.base + 0.5} stroke="#dcd8c8" stroke-width="0.8" />
              {#each row.dots as dot}
                <circle cx={binX(dot.j)} cy={row.base - (dot.k + 0.5) * STEP} r={R} fill={fillOf(dot, false)} stroke={strokeOf(dot, false)} stroke-width="0.6" />
              {/each}
              <!-- the row's average -->
              <line x1={sx(row.mean)} x2={sx(row.mean)} y1={row.base + 1} y2={row.base + 7} stroke="#111" stroke-width="1.6" />
            </g>
          {/each}
        {/if}

        <!-- axis, in words -->
        {#each [-100, 0, 100, 200, 300] as t}
          <line x1={sx(t)} x2={sx(t)} y1={layout.bottom} y2={layout.bottom + 4} stroke="#8d897e" stroke-width="0.8" />
          <text class="faint num" x={sx(t)} y={layout.bottom + 16} text-anchor="middle" font-size="11">{t === 0 ? '0' : bn(t)}</text>
        {/each}
        <text class="muted it" x={sx(-100)} y={layout.bottom + 32} font-size="11.5">← everyone else better off</text>
        <text class="muted it" x={X1} y={layout.bottom + 32} text-anchor="end" font-size="11.5">everyone else worse off →</text>
      </svg>
    </div>

    <p class="note">
      {#if !fam}
        Pick a choice to split the heap by it. A choice that matters pulls the rows apart; one that does not leaves near copies.
      {:else if fam.id === 'services'}
        The two rows sit on opposite sides of zero with nothing between them. Hover a row to find its dots in the top heap.
      {:else}
        Averages (the ink ticks) run from <span class="num">{avg(Math.min(...means))}</span> to
        <span class="num">{avg(Math.max(...means))}</span>{fam.among ? ' among the combinations where services grow' : ''}.
        {#if fam.effect < 20}
          The rows are near copies of each other: this choice moves the answer less than any choice about services.
        {:else}
          The rows shift, but only the combinations where nothing grows cross zero.
        {/if}
        Hover a row to find its dots in the top heap.
      {/if}
    </p>
  </div>

  <aside class="side">
    <p>
      Every combination counts once, so the heaps count combinations. Their sizes do not say how likely a choice is:
      one of the nine service settings holds everything still, so about a ninth of the dots sit left of zero.
    </p>
    <p>
      Nothing is sampled. The gain from their work adds to the rest of the account, so each of its models pairs with
      every other choice, and each combination is counted into a $5bn bin whose edge is zero.
    </p>
    <p>“Where services grow” means schools, police, courts, health and welfare grow with the group; colleges and roads may or may not.</p>
    <p>proto/choices.cjs; gates reproduce the matrix’s ranges for both halves and check that every choice’s rows partition the combinations.</p>
  </aside>
</section>

<style>
  .pick { display: grid; grid-template-columns: 1fr; gap: 0.1rem; font-size: 0.92rem; color: var(--muted); margin: 0.2rem 0 0.9rem; max-width: 40rem; }
  .pick-head { margin: 0 0 0.2rem; color: var(--ink); }
  .pick label { display: grid; grid-template-columns: auto 1fr 130px 3.4rem; align-items: center; gap: 0.5rem; cursor: pointer; }
  .pick label:first-of-type { grid-template-columns: auto 1fr; }
  .pick input { margin: 0; }
  .pick-bar { width: 130px; height: 10px; display: block; }
  .pick-num { text-align: right; color: var(--ink); }
  .faint-text { color: var(--faint); font-style: italic; }
</style>
