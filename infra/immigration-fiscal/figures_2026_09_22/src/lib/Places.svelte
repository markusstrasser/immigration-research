<script>
  import { places } from '../data.js'
  import { dollars } from '../format.js'

  const ranked = places.filter((p) => !p.national).slice().sort((a, b) => a.v - b.v)
  const national = places.find((p) => p.national)
  const rows = [...ranked, national]

  const x0 = 250
  const x1 = 640
  const lo = -22000
  const hi = 0
  const x = (v) => x0 + ((v - lo) / (hi - lo)) * (x1 - x0)
  const top = 36
  const rowH = 27
  const y = (i) => top + i * rowH + (rows[i].national ? 12 : 0)
  const height = y(rows.length - 1) + 40
  const k = (v) => (v === 0 ? '0' : '−' + Math.abs(v / 1000) + 'k')
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
      <text class="faint it" x={x1 + 12} y="16" font-size="11.5">people</text>

      {#each rows as p, i}
        {@const yy = y(i)}
        {#if p.national}
          <line x1="0" x2="760" y1={yy - 18} y2={yy - 18} stroke="#dcd8c8" stroke-dasharray="2 3" />
        {/if}
        <text x="0" y={yy + 4} font-size="13" font-weight={isState(p) ? 700 : 400} class={p.national ? 'muted' : undefined}>{p.name}</text>
        <line x1={x0} x2={x(p.v)} y1={yy} y2={yy} stroke="#efece2" stroke-width="1" />
        {#if p.lo != null}
          <line x1={x(p.lo)} x2={x(p.hi)} y1={yy} y2={yy} stroke="#ca7a5e" stroke-width="1.2" />
        {/if}
        <circle cx={x(p.v)} cy={yy} r={isState(p) ? 5.5 : 4.2} fill={p.national ? '#e4e1d6' : '#f2cabc'} stroke={p.national ? '#8d897e' : '#ca7a5e'} />
        <text class="num" x={x(p.lo ?? p.v) - 9} y={yy + 4} text-anchor="end" font-size="12">{dollars(p.v)}</text>
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
      Against all local natives Los Angeles is −$8,028, close to Chicago’s −$8,344: part of the jump
      against whites is a richer white comparison. National, age only, is the last row and not a place.
    </p>
    <p>
      Not a slice of the $203–250bn complete account. ledger_stress_2026_09_17 and
      metro_match_2026_09_17.
    </p>
  </aside>
</section>
