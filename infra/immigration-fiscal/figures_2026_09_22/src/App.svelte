<script>
  import ResponseLine from './lib/ResponseLine.svelte'
  import AgeWeights from './lib/AgeWeights.svelte'
  import Ranges from './lib/Ranges.svelte'
  import Slope from './lib/Slope.svelte'
  import Schooling from './lib/Schooling.svelte'
  import Backcast from './lib/Backcast.svelte'
  import Paths from './lib/Paths.svelte'
  import Places from './lib/Places.svelte'
  import Rest from './lib/Rest.svelte'
</script>

<main>
  <p class="kicker">Income year 2024 · executed tables</p>
  <h1>Assumptions, drawn</h1>
  <p class="lead">
    Each figure stays inside a single account. The interesting motion is an
    assumption being turned, with the measured part left in ink and the modelled part hatched.
  </p>
  <p class="epigraph">
    The generation ledger, the −$217bn union balance, and the $165–197bn complete account
    agree in direction. One is not a decomposition of the others. Nothing here puts them
    on the same axis.
  </p>
  <nav>
    <a href="#response">1 Response</a>
    <a href="#age">2 Age weights</a>
    <a href="#ranges">3 Conventions</a>
    <a href="#generations">4 Generations</a>
    <a href="#schooling">5 Schooling</a>
    <a href="#backcast">6 Back-cast</a>
    <a href="#programmes">Budgets</a>
    <a href="#rule">The path</a>
    <a href="#places">7 Places</a>
    <a href="#education">8 Schooling sign</a>
    <a href="#kitagawa">9 India, occupations</a>
    <a href="#custody">Custody</a>
  </nav>

  <ResponseLine />
  <AgeWeights />
  <Ranges />
  <Slope />
  <Schooling />
  <Backcast />
  <Paths />
  <Places />
  <Rest />
</main>
