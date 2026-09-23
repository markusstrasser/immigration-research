<script>
  import { education, kitagawa, custody } from '../data.js'
  import { dollars } from '../format.js'

  const eduLo = -16000
  const eduHi = 8000
  const xp = (v) => ((v - eduLo) / (eduHi - eduLo)) * 100

  const kLo = -12000
  const kHi = 70000
  const kx = (v) => ((v - kLo) / (kHi - kLo)) * 100

  const spark = custody.ratio
    .map((v, i) => {
      const x = (i / (custody.ratio.length - 1)) * 92 + 4
      const y = 22 - ((v - 1.5) / (2.8 - 1.5)) * 16
      return `${i ? 'L' : 'M'} ${x.toFixed(1)} ${y.toFixed(1)}`
    })
    .join(' ')
</script>

<section class="fig" id="education">
  <p class="kicker">Fig. 8 · Education-specific account</p>
  <h2>The sign flips inside the schooling comparison</h2>
  <p class="object">
    Mexico-born adults, ages 25–64, common ages, household costs shared.
    Below high school beats natives with the same schooling. High-school-only does not.
    The third dot, against natives of every schooling level, is that composition.
  </p>

  {#each education as row}
    <div class="edu-row">
      <span>{row.label}</span>
      <div class="edu-plot">
        <i class="zero" style="left:{xp(0)}%"></i>
        {#if row.lo != null}
          <i class="whisk" style="left:{xp(row.lo)}%; width:{xp(row.hi) - xp(row.lo)}%"></i>
        {/if}
        <i class="dot" style="left:{xp(row.v)}%"></i>
      </div>
      <span class="num">{dollars(row.v)}</span>
    </div>
  {/each}

  <p class="src">
    education_origin_fiscal comparisons, account expanded_excluding_N, entry stock.
    Whiskers are the published intervals. The cell’s own level for below high school is
    −$5,558 on this allocation; that is a level, and it is not a dot here.
  </p>
</section>

<section class="fig" id="kitagawa">
  <p class="kicker">Fig. 9 · ACS 2023 earnings, ages 25–64</p>
  <h2>India: mix, then a within-occupation remainder</h2>
  <p class="object">
    Gap versus US-born non-Hispanic whites. Mix is the occupation weights. Within is the
    pay difference inside occupations. For recent noncitizens the mix is larger than the gap
    and the within term is negative.
  </p>

  {#each kitagawa as group}
    <h3>{group.label}</h3>
    <p class="object">{group.detail}. Gap {dollars(group.gap)}.</p>
    {#each [['Mix', group.mix], ['Within occupation', group.within], ['Interaction', group.inter]] as [name, v]}
      <div class="cat">
        <span>{name}</span>
        <div class="track">
          <i class="zero-k" style="left:{kx(0)}%"></i>
          {#if v >= 0}
            <i class="bar cost" style="left:{kx(0)}%; width:{kx(v) - kx(0)}%"></i>
          {:else}
            <i class="bar save" style="left:{kx(v)}%; width:{kx(0) - kx(v)}%"></i>
          {/if}
        </div>
        <span class="num">{dollars(v)}</span>
      </div>
    {/each}
  {/each}

  <p class="src">
    indian_generation_2026_09_21/derived/occ_kitagawa.csv. Employed persons. The ancestry
    row uses a broad IT split; the India-born rows use the detailed occupation bins.
    Green is a negative term. These dollars are earnings, not a fiscal balance.
  </p>
</section>

<section class="fig" id="custody">
  <p class="kicker">Not a fiscal series</p>
  <h2>Institutions, off the ledger</h2>
  <p class="sentence">
    US-born Mexican-origin men aged 18–39 in institutions, divided by native non-Hispanic
    white men:
    <svg viewBox="0 0 100 26" aria-label="2.56, 1.91, 1.72, 1.94">
      <path d={spark} fill="none" stroke="#8c2f16" stroke-width="1.6" />
      {#each custody.ratio as v, i}
        <circle
          cx={(i / (custody.ratio.length - 1)) * 92 + 4}
          cy={22 - ((v - 1.5) / 1.3) * 16}
          r="2"
          fill="#8c2f16"
        />
      {/each}
    </svg>
    2.56× in 2010, 1.91× in 2019, 1.72× in 2023, 1.94× in 2024.
    Reallocating prisons coded only as Hispanic lifts the later years to about 2.1–2.3×.
    The line starts in 2010 because 2000 counted correctional institutions only.
  </p>
  <p class="src">
    acs_institutional_rates.csv. Since September 23 the complete account’s headline charges
    prisons by the group’s share of people in custody, and police and courts partly by arrests.
    This ratio, US-born men 18–39, is not that key.
  </p>
</section>

<style>
  h3 { font-size: 1.05rem; margin: 1.1rem 0 0; }
  .zero-k {
    position: absolute;
    top: -2px;
    width: 1px;
    height: 12px;
    background: var(--ink);
  }
  .num { font-variant-numeric: tabular-nums; }
</style>
