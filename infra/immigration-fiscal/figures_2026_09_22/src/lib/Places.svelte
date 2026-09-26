<script>
  import fig from '../generated/figures.json'
  import { places } from '../data.js'

  const account = fig.account.main.map(Math.round)

  const ranked = places.filter((p) => !p.national).slice().sort((a, b) => a.v - b.v)
  const national = places.find((p) => p.national)
  const rows = [...ranked, national]

  // A gap against local whites, not a cost to everyone else: the places are ink marks. The gap
  // grows to the right, zero at the left edge.
  const x0 = 250
  const x1 = 640
  const lo = -22000
  const hi = 0
  const x = (v) => x0 + ((hi - v) / (hi - lo)) * (x1 - x0)
  const top = 36
  const rowH = 27
  const y = (i) => top + i * rowH + (rows[i].national ? 12 : 0)
  const height = y(rows.length - 1) + 40
  const k = (v) => (v === 0 ? '0' : Math.abs(v / 1000) + 'k')
  const usd = (v) => '$' + Math.abs(Math.round(v)).toLocaleString('en-US')
  // The value sits past the far end of the interval unless that would run into the people column.
  function valueAt(p) {
    const ends = [p.v, p.lo, p.hi].filter((v) => v != null).map(x)
    const text = `${usd(p.v)} ${p.v < 0 ? 'below' : 'above'} whites`
    const far = Math.max(...ends) + 9
    return far + text.length * 6.2 < x1 + 6
      ? { x: far, anchor: 'start', text }
      : { x: Math.min(...ends) - 9, anchor: 'end', text }
  }
  const isState = (p) => p.share != null
  const at = (name) => places.find((p) => p.name === name).v
  const larger = Math.round((at('California') / at('Texas') - 1) * 100)
  const times = (at('Los Angeles') / at('Houston')).toFixed(1)
</script>

<section class="fig" id="places">
  <div class="body">
    <p class="kicker">Shared all-age ledger · against local whites</p>
    <h2>Same share, not the same gap</h2>
    <p class="lede">
      California and Texas are both about 32% Mexican-origin. Against the third-plus non-Hispanic
      whites of the same state or metro, at common ages, California’s gap per person is {larger}%
      larger than Texas’s, and Los Angeles’s is {times} times Houston’s.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 {height}" role="img" aria-label="Gap per person against local whites, by state and metro">
      {#each [-20000, -15000, -10000, -5000, 0] as t}
        <line x1={x(t)} x2={x(t)} y1="22" y2={height - 24} stroke={t === 0 ? '#111' : '#efece2'} stroke-width={t === 0 ? 0.8 : 1} />
        <text class="faint num" x={x(t)} y={height - 8} text-anchor="middle" font-size="11">{k(t)}</text>
      {/each}
      <text class="faint it" x={x0 + 6} y="16" font-size="11.5">$ per person below local third-plus whites →</text>
      <text class="faint it" x={x1 + 12} y="16" font-size="11.5">people</text>

      {#each rows as p, i}
        {@const yy = y(i)}
        {@const val = valueAt(p)}
        {#if p.national}
          <line x1="0" x2="760" y1={yy - 18} y2={yy - 18} stroke="#dcd8c8" stroke-dasharray="2 3" />
        {/if}
        <text x="0" y={yy + 4} font-size="13" font-weight={isState(p) ? 700 : 400} class={p.national ? 'muted' : undefined}>{p.name}</text>
        <line x1={x0} x2={x(p.v)} y1={yy} y2={yy} stroke="#efece2" stroke-width="1" />
        {#if p.lo != null}
          <line x1={x(p.lo)} x2={x(p.hi)} y1={yy} y2={yy} stroke="#111" stroke-width="1" />
        {/if}
        <circle cx={x(p.v)} cy={yy} r={isState(p) ? 5.5 : 4.2} fill={p.national ? '#fffff8' : '#111'} stroke={p.national ? '#8d897e' : '#111'} stroke-width={p.national ? 1.2 : 1} />
        <text class="halo" x={val.x} y={yy + 4} text-anchor={val.anchor} font-size="12">{val.text}</text>
        <text class="muted num" x={x1 + 12} y={yy + 4} font-size="12">{p.people ?? p.share + ' of residents'}</text>
      {/each}
    </svg>
    </div>
  </div>

  <aside class="side">
    <p>
      Dollars per standardized person a year, CPS ASEC 2025, nominal: no regional price parity. Lines
      through the states and Los Angeles are the published intervals.
    </p>
    <p>
      Against all local natives Los Angeles sits $8,028 per person below, close to Chicago’s $8,344:
      part of the jump against whites is a richer white comparison. National, age only, is the last
      row, an open mark, and not a place.
    </p>
    <p>
      Not a slice of the ${account[0]}–{account[1]}bn complete account. ledger_stress_2026_09_17 and
      metro_match_2026_09_17.
    </p>
  </aside>
</section>
