<script>
  import Staircase from '../lib/Staircase.svelte'
  import FlipDistance from './FlipDistance.svelte'
  import NumberLine from './NumberLine.svelte'
  import Coastline from './Coastline.svelte'
  import DotHeaps from './DotHeaps.svelte'
  import Nomogram from './Nomogram.svelte'
</script>

<main>
  <p class="kicker">Prototypes · not linked from the figures page</p>
  <h1>Is it costly under every sane assumption?</h1>
  <p class="subtitle">Five ways of showing it, with the staircase from the figures page first for comparison.</p>
  <nav>
    <a href="#staircase">Staircase</a>
    <a href="#flip">Distance to flip</a>
    <a href="#conventions">Number line</a>
    <a href="#coastline">Coastline</a>
    <a href="#dots">Heaps of dots</a>
    <a href="#nomogram">Nomogram</a>
  </nav>

  <Staircase />
  <FlipDistance />
  <NumberLine />
  <Coastline />
  <DotHeaps />
  <Nomogram />
</main>
