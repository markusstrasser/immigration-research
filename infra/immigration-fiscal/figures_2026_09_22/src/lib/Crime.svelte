<script>
  import fig from '../generated/figures.json'

  const rows = fig.crime
  const custody = fig.custody
  const victims = fig.victims.map((v) => v.toFixed(1))
  const x0 = 200
  const x1 = 560
  const lx = (v) => x0 + (Math.log10(v) / Math.log10(2000)) * (x1 - x0)
  const top = 44
  const rowH = 40
  const y = (i) => top + i * rowH
  const height = y(rows.length - 1) + 44
  const ticks = [1, 10, 100, 1000]
  const times = (v) => v.toFixed(1) + '×'
  const spanOf = (xs) => `${Math.min(...xs).toFixed(1)} to ${Math.max(...xs).toFixed(1)}`
  const vsWhite = spanOf(rows.map((r) => r.vsWhite[1]))
  const vsAll = spanOf(rows.map((r) => r.vsAll[1]))

  // Custody ratio, spaced by year.
  const sx = (year) => 4 + ((year - 2010) / 14) * 92
  const sy = (v) => 22 - ((v - 1.5) / 1.3) * 16
  const said = custody.years.map((yr, i) => `${custody.ratio[i].toFixed(2)} in ${yr}`)
  const first = `${custody.ratio[0].toFixed(2)} times the rate of native non-Hispanic white men in ${custody.years[0]}`
  const later = custody.reallocated.filter((_, i) => custody.years[i] >= 2019)
  const realloc = `${Math.min(...later).toFixed(2)}–${Math.max(...later).toFixed(2)}`
  const spark = custody.ratio.map((v, i) => `${i ? 'L' : 'M'} ${sx(custody.years[i]).toFixed(1)} ${sy(v).toFixed(1)}`).join(' ')
</script>

<section class="fig" id="crime">
  <div class="body">
    <p class="kicker">Police records · Texas and Arizona NIBRS · 2022–2023</p>
    <h2>Which comparison group</h2>
    <p class="lede">
      Offenders per 100,000 residents aged 12 and over, by the offender’s recorded ethnicity. Hispanic
      residents offend at {vsWhite} times the non-Hispanic white rate and {vsAll} times the rate of all
      residents. Both are true; which one a writer quotes is a choice of reference group.
    </p>

    <div class="scroll">
    <svg class="wide" viewBox="0 0 760 {height}" role="img" aria-label="Offending rates on a log scale: Hispanic, non-Hispanic white and all residents">
      {#each ticks as t}
        <line x1={lx(t)} x2={lx(t)} y1="26" y2={height - 22} stroke="#efece2" />
        <text class="faint num" x={lx(t)} y={height - 6} text-anchor="middle" font-size="11">{t.toLocaleString('en-US')}</text>
      {/each}
      <text class="faint it" x={x1} y={height + 10} text-anchor="end" font-size="11">per 100,000 a year, log scale</text>
      <text class="faint it" x="584" y="20" font-size="11">Hispanic rate as a multiple of</text>
      <text class="faint" x="584" y="34" font-size="11">whites · all residents</text>

      <!-- People are not coloured: Hispanic is the filled ink mark, the two comparisons grey. -->
      {#each rows as r, i}
        {@const yy = y(i)}
        <text x="0" y={yy + 4} font-size="13">{r.offence}</text>
        <line x1={lx(r.hispanicBounds[0])} x2={lx(r.hispanicBounds[1])} y1={yy} y2={yy} stroke="#111" stroke-width="1" />
        <circle cx={lx(r.per100k.white)} cy={yy} r="4.8" fill="#fffff8" stroke="#8d897e" stroke-width="1.2" />
        <line x1={lx(r.per100k.all)} x2={lx(r.per100k.all)} y1={yy - 8} y2={yy + 8} stroke="#8d897e" stroke-width="1.6" />
        <circle cx={lx(r.per100k.hispanic)} cy={yy} r="4.2" fill="#111" />
        <text class="num" x="584" y={yy + 4} font-size="12.5">{times(r.vsWhite[1])} · {times(r.vsAll[1])}</text>
        {#if i === 0}
          <text class="muted it" x={lx(r.per100k.white)} y={yy - 11} text-anchor="middle" font-size="11">white</text>
          <text class="muted it" x={lx(r.per100k.hispanic) + 26} y={yy - 11} text-anchor="middle" font-size="11">Hispanic, all</text>
        {/if}
      {/each}
    </svg>
    </div>

    <p class="note">
      Open grey circle: non-Hispanic white. Black dot: Hispanic, with a line from “every unknown
      offender non-Hispanic” to “every unknown offender Hispanic”. Grey tick: all residents.
    </p>

    <p class="sentence">
      Custody gives a similar ratio. US-born Mexican-origin men aged 18–39 are in institutions at
      <svg class="spark" viewBox="0 0 100 26" aria-label={said.join(", ")}>
        <path d={spark} fill="none" stroke="#111" stroke-width="1.4" />
        {#each custody.ratio as v, i}
          <circle cx={sx(custody.years[i])} cy={sy(v)} r="2" fill="#111" />
        {/each}
      </svg>
      {first}, then {said.slice(1, -1).join(', ')} and {said.at(-1)}; {realloc} since 2019 once prison records
      coded only “Hispanic” are reallocated.
    </p>
  </div>

  <aside class="side">
    <p>
      Crude rates for Hispanics of any origin in the agencies that record offender ethnicity for at least
      half of known offenders. 70–81% of Hispanic offenders’ victims are Hispanic.
    </p>
    <p>
      The custody series starts in 2010. The 2000 census filled in a US birthplace for most
      Mexican-origin inmates, so its 3.45 is not like for like; spreading those birthplaces gives about
      2.7–3.0.
    </p>
    <p>
      Victims’ harm from the group’s offending against other residents, ${victims[0]}–{victims[1]}bn a year,
      sits beside the fiscal account (FAQ 12).
    </p>
    <p>
      offender_ethnicity_nibrs_2026_09_23 rates_by_spec.csv (central, alloc=b, alloc=c);
      acs_institutional_2026_09_16 acs_institutional_rates.csv; population_basis_2026_09_29
      restated_pairing.csv.
    </p>
  </aside>
</section>

<style>
  .sentence { max-width: 40rem; margin: 1.4rem 0 0; }
</style>
