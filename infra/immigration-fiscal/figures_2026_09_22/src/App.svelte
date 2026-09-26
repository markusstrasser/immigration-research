<script>
  import Staircase from './lib/Staircase.svelte'
  import Matrix from './lib/Matrix.svelte'
  import AgeWeights from './lib/AgeWeights.svelte'
  import Slope from './lib/Slope.svelte'
  import Skills from './lib/Skills.svelte'
  import Places from './lib/Places.svelte'
  import WhoPays from './lib/WhoPays.svelte'
  import Percentiles from './lib/Percentiles.svelte'
  import Crime from './lib/Crime.svelte'
  import Sentences from './lib/Sentences.svelte'
  import fig from './generated/figures.json'

  const main = fig.account.main.map(Math.round)
</script>

<main>
  <p class="kicker">Income year 2024 · executed tables</p>
  <h1>Assumptions, drawn</h1>
  <p class="subtitle">
    What the Mexican-origin population costs other US residents, and which assumptions decide it.
  </p>
  <p class="lead">
    Each figure stays inside one account and names it above its title. The first two show every budget
    assumption at once; the rest show the people behind the totals.
  </p>
  <p class="rule-note">
    The generation ledger, the union balance and the complete account agree in direction: every generation
    sits below whites, and everyone else is $217bn a year worse off on the union balance and
    ${main[0]}–{main[1]}bn a year worse off on the complete account. None is a slice of another, and no figure
    puts two of them on one axis.
  </p>
  <nav>
    <a href="#staircase">The tally and the bill</a>
    <a href="#matrix">Every combination</a>
    <a href="#age">Ages</a>
    <a href="#generations">Generations</a>
    <a href="#skills">Schooling</a>
    <a href="#places">Places</a>
    <a href="#whopays">Who pays</a>
    <a href="#percentiles">By percentile</a>
    <a href="#crime">Crime</a>
    <a href="#sentences">In a sentence</a>
  </nav>

  <Staircase />
  <Matrix />
  <AgeWeights />
  <Slope />
  <Skills />
  <Places />
  <WhoPays />
  <Percentiles />
  <Crime />
  <Sentences />
</main>
