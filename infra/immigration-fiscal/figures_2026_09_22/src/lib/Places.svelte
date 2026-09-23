<script>
  import { places } from '../data.js'
  import { dollars } from '../format.js'

  const ranked = places.filter((p) => !p.national).slice().sort((a, b) => a.v - b.v)
  const national = places.find((p) => p.national)
  const scale = 22000

  const width = (v) => `${(Math.abs(v) / scale) * 100}%`
</script>

<section class="fig" id="places">
  <p class="kicker">Fig. 7 · Shared all-age ledger</p>
  <h2>Same share. Not the same gap.</h2>
  <p class="object">
    California and Texas are both about 32% Mexican-origin. The bars are the gap against
    local third-plus non-Hispanic whites, per standardized person. This is not a slice of
    the $203–250bn account.
  </p>

  <table class="places">
    <thead>
      <tr>
        <th>Place</th>
        <th>Gap vs local whites</th>
        <th class="num">$ / person</th>
        <th>Share or people</th>
      </tr>
    </thead>
    <tbody>
      {#each [...ranked, national] as p}
        <tr class:national={p.national}>
          <th>{p.name}</th>
          <td>
            <div class="meter">
              <i class="fill" style="width:{width(p.v)}"></i>
              {#if p.lo != null}
                <i class="whisk" style="left:{width(p.hi)}; width:{width(p.lo - p.hi)}"></i>
              {/if}
            </div>
          </td>
          <td class="num">{dollars(p.v)}</td>
          <td>{p.share ?? p.people}</td>
        </tr>
      {/each}
    </tbody>
  </table>

  <p class="src">
    ledger_stress and metro_match, CPS ASEC 2025. Whiskers are the published intervals where
    the table has them. Nominal dollars, no regional price parity. Los Angeles versus all
    local natives is −$8,028, close to Chicago’s −$8,344; the vs-white jump is partly a richer
    white comparison. National, age only, is the bottom row and is not a place.
  </p>
</section>
