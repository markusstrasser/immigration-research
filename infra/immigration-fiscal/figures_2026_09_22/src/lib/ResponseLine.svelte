<script>
  import { responseRows, production } from '../data.js'
  import { billions } from '../format.js'

  let which = $state('jobs')
  let gain = $derived(production.find((p) => p.id === which))

  const lo = -150
  const hi = 360
  const left = 250
  const right = 800
  const x = (v) => left + ((v - lo) / (hi - lo)) * (right - left)

  function money(n) {
    const v = Math.abs(n).toFixed(0)
    return (n < 0 ? '−$' : '$') + v + 'bn'
  }

  const prodY = 52 + responseRows.length * 46
</script>

<section class="fig" id="response">
  <p class="kicker">Fig. 1 · Complete account</p>
  <h2>The service response is the result</h2>
  <p class="object">
    Positive is a cost to other US residents. The headline holds defense, interest,
    general government and subsidies at zero response. That zero is an assumption.
    What comes from CBO is the tax-incidence rule and a 63–66% school response.
  </p>

  <svg viewBox="0 0 860 370" role="img" aria-label="Service-response ranges on one dollar scale">
    <line x1={x(0)} y1="8" x2={x(0)} y2="300" stroke="#1c1917" stroke-width="1" />
    <text class="faint" x={x(0) - 6} y="20" text-anchor="end" font-size="11">gain</text>
    <text class="faint" x={x(0) + 6} y="20" font-size="11">cost</text>

    {#each responseRows as row, i}
      {@const y = 52 + i * 46}
      <text x="0" y={y - 2} font-size="13">{row.label}</text>
      <text class="faint" x="0" y={y + 12} font-size="10">{money(row.lo)} to {money(row.hi)}</text>
      {#if row.lo < 0}
        <rect x={x(row.lo)} y={y - 6} width={x(0) - x(row.lo)} height="8" fill="#1d5a42" />
        <rect x={x(0)} y={y - 6} width={x(row.hi) - x(0)} height="8" fill="#8c2f16" />
      {:else}
        <rect x={x(row.lo)} y={y - 6} width={x(row.hi) - x(row.lo)} height="8" fill="#8c2f16" />
      {/if}
    {/each}

    <text x="0" y={prodY + 4} font-size="13">Production gain</text>
    <rect x={x(-gain.hi)} y={prodY - 5} width={x(-gain.lo) - x(-gain.hi)} height="8" fill="#1d5a42" />
    <text class="muted" x={x(-gain.lo) + 8} y={prodY + 4} font-size="12">
      {billions(gain.lo, 1)} to {billions(gain.hi, 1)}
    </text>
    <text class="faint" x={x(-gain.hi)} y={prodY + 22} font-size="11">already inside the headline</text>

    <text class="faint" x={x(0)} y="348" text-anchor="middle" font-size="11">0 · break-even if 18.5–25.8% of service costs are incremental</text>
    <text class="faint" x={right} y="348" text-anchor="end" font-size="11">$bn / year</text>
  </svg>

  <div class="picks">
    {#each production as p}
      <button class:on={which === p.id} onclick={() => (which = p.id)}>{p.label}</button>
    {/each}
  </div>

  <p class="src">
    Complete account and FAQ entries 2 and 4. The fixed-services row is the paired path
    in “what can reverse the sign,” capital included. Production: cash scaling at the low
    end, GDP scaling at the high end. ε = 5 and ε = 7 on the account’s own nest, option A; 8.7 and 17.9 are the direct low-skill
    estimates (ladder 181).
    The removal model’s $27–80bn is a different population and is not drawn.
  </p>
</section>
