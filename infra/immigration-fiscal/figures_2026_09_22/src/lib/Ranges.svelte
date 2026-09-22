<script>
  import { hulls } from '../data.js'
  import { billions } from '../format.js'

  const lo = -540
  const hi = 80
  const left = 196
  const right = 820
  const x = (v) => left + ((v - lo) / (hi - lo)) * (right - left)
</script>

<section class="fig" id="ranges">
  <p class="kicker">Fig. 3 · September 19 ledger</p>
  <h2>A convention is not an interval</h2>
  <p class="object">
    Negative is a shortfall of the union’s expanded balance. The thick bar is what a
    budget modeler would run. The hairline is every switch the design can reach.
    The lower bar answers a different question.
  </p>

  <svg viewBox="0 0 860 250" role="img" aria-label="Practitioner hull, design span, and public-goods object">
    <line x1={x(0)} y1="16" x2={x(0)} y2="210" stroke="#1c1917" stroke-width="1" />
    <text class="faint" x={x(0) + 6} y="28" font-size="11">0</text>

    <text x="0" y="62" font-size="13">Practitioner</text>
    <rect x={x(hulls.practitioner.lo)} y="50" width={x(hulls.practitioner.hi) - x(hulls.practitioner.lo)} height="10" fill="#8c2f16" />
    <line x1={x(hulls.practitioner.mark)} x2={x(hulls.practitioner.mark)} y1="46" y2="64" stroke="#f3efe6" stroke-width="2" />
    <text class="muted" x={x(hulls.practitioner.hi) + 8} y="60" font-size="12">
      {billions(hulls.practitioner.lo, 0)} to {billions(hulls.practitioner.hi, 0)}
    </text>
    <text class="faint" x={x(hulls.practitioner.mark)} y="78" text-anchor="middle" font-size="11">
      {billions(hulls.practitioner.mark, 0)}
    </text>

    <text x="0" y="118" font-size="13">Design grid</text>
    <line x1={x(hulls.design.lo)} x2={x(hulls.design.hi)} y1="112" y2="112" stroke="#1c1917" stroke-width="1" />
    <line x1={x(hulls.design.hi)} x2={x(hulls.dial)} y1="112" y2="112" stroke="#1c1917" stroke-width="1" stroke-dasharray="3 3" />
    <text class="muted" x={x(hulls.dial) + 8} y="116" font-size="12">{billions(hulls.dial, 0)}</text>
    <text class="faint" x={x(hulls.design.lo)} y="132" font-size="11">63 cells</text>
    <text class="faint" x={x((hulls.design.hi + hulls.dial) / 2)} y="132" text-anchor="middle" font-size="11">taxes and transfers only</text>

    <text x="0" y="186" font-size="13">Public goods</text>
    <text class="faint" x="0" y="202" font-size="11">per person</text>
    <rect x={x(hulls.publicGoods.lo)} y="176" width={x(hulls.publicGoods.hi) - x(hulls.publicGoods.lo)} height="6" fill="#24384a" />
    <text class="muted" x={x(hulls.publicGoods.hi) + 8} y="184" font-size="12">
      {billions(hulls.publicGoods.lo, 0)} to {billions(hulls.publicGoods.hi, 0)}
    </text>
    <text class="faint" x="0" y="236" font-size="12">A different object. Defense, interest and general government assigned per capita.</text>
  </svg>

  <p class="src">
    ledger_recut_2026_09_22/derived/hulls.csv. The hairline grows whenever an arm is added.
    The dashed stub is the marginality dial at its end. None of these is a confidence interval,
    and none of them is the $165–197bn complete account.
  </p>
</section>
