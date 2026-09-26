/* Prototype data: the number line of accounting conventions.
 *
 * Every preset of the assumption explorer (assumption_explorer_2026_09_21/presets.json, pinned at
 * d710a74 by account.cjs), evaluated as the explorer and test_engine.js loaded it: the cost to other
 * US residents over the preset's unresolved dimensions. The presets are conventions, never people;
 * commentators appear only as the explorer's text (presets.json "authors"), which says which
 * convention comes closest to a framing and why it is not the same thing. Beside them, from the figures page's matrix: the span of every
 * combination that lets some service budget grow, and of the frozen row.
 */
"use strict";

// Plain-language description of each preset. A preset missing here stops the build.
const WHAT = {
  repo_central_gg: "Schools add 63–66% of per-pupil cost, other services grow fully, administration 59–84%.",
  repo_central: "As published September 20: general administration not charged, data not yet corrected.",
  proportional: "Every public service grows one for one with the population.",
  taxes_minus_benefits: "Taxes paid against benefits received. No public services, no gain from their work.",
  no_services: "Taxes, benefits and the gain from their work. No public service is charged.",
  average_cost_everything: "A per-head share of everything, including defense and interest on debt already issued.",
  production_only: "Others' gain in wages and profits. Every budget line is left out, even taxes on it.",
};
const SHORT = {
  repo_central_gg: "Main case", repo_central: "Main case as published September 20", proportional: "All services at average cost",
  taxes_minus_benefits: "Taxes minus benefits", no_services: "No public services charged",
  average_cost_everything: "Everything at average cost", production_only: "Private gain from their work only",
};

function build(A) {
  const { gate, near, round, presets, presetCost } = A;
  const missing = presets.filter((p) => !WHAT[p.id]).map((p) => p.id);
  gate("every explorer preset has a description", missing.length === 0, missing.join(", ") || `${presets.length} presets`);

  const rows = presets.map((p) => {
    const c = presetCost(p.id);
    return { id: p.id, label: SHORT[p.id], what: WHAT[p.id], central: !!p.central, cost: c.map((x) => round(x, 2)) };
  });
  const by = Object.fromEntries(rows.map((r) => [r.id, r]));

  const main = presetCost("repo_central_gg"), prop = presetCost("proportional");
  gate("the central preset reproduces the main case", near(main[0], A.MAIN[0], 1e-4) && near(main[1], A.MAIN[1], 1e-4),
    main.map((x) => x.toFixed(4)).join(" to "));
  gate("the proportional preset reproduces main_case_bands.csv", near(prop[0], A.PROPORTIONAL[0], 1e-4) && near(prop[1], A.PROPORTIONAL[1], 1e-4));
  const head = A.model.meta.headline.category_service_response_sensitivity.cbo_category_lag_non_school_full;
  const sept20 = presetCost("repo_central");
  gate("the September 20 preset reproduces the published band", near(sept20[0], -head.max_welfare_bn, 1e-6) && near(sept20[1], -head.min_welfare_bn, 1e-6),
    sept20.map((x) => x.toFixed(2)).join(" to "));
  const tally = presetCost("taxes_minus_benefits");
  gate("the tally is a gain", tally[1] < 0, tally.map((x) => x.toFixed(2)).join(" to "));

  // The main case with every data correction at its extreme in the same direction (main_case_bands.csv range
  // columns); the alternative rules are the matrix's outer envelope, $174–257bn, quoted by the flip figure.
  const bands = A.readCsv(A.path.join(A.MAIN_CASE, "derived", "main_case_bands.csv"));
  const adopted = bands.find((b) => b.profile === "cbo_category_lag_non_school_full" && b.variant === "adopted");
  by.repo_central_gg.outer = [round(Number(adopted.range_low_bn), 2), round(Number(adopted.range_high_bn), 2)];

  // The figures page's matrix: every combination that lets a service budget grow, and the frozen row.
  const figures = JSON.parse(A.fs.readFileSync(A.path.join(A.HERE, "src", "generated", "figures.json"), "utf8"));
  const cells = (pred) => figures.matrix.rows.filter(pred).flatMap((r) => r.cells.map((c) => c.outer));
  const growing = cells((r) => !r.frozen), frozen = cells((r) => r.frozen);
  const env = (xs) => [round(Math.min(...xs.map((c) => c[0])), 1), round(Math.max(...xs.map((c) => c[1])), 1)];
  const matrix = { growing: env(growing), frozen: env(frozen), combinations: growing.length };
  gate("every combination that lets a service grow is a cost", matrix.growing[0] > 0, matrix.growing.join(" to "));

  // The staircase starts from the uncorrected tally and adds the data corrections as its last steps; the presets
  // run on corrected data. The page states both so the two first rows can be read together.
  const stairTally = figures.staircase.find((r) => r.id === "tally").total;
  gate("the staircase's tally is the uncorrected one", !near(stairTally[0], tally[0], 1e-6), stairTally.map((x) => x.toFixed(2)).join(" to "));
  const staircase = { tally: stairTally.map((x) => round(x, 2)) };

  const authors = A.presetsFile.authors.map((a) => ({ name: a.name, closest: a.closest && a.closest.preset ? SHORT[a.closest.preset] : null }));

  rows.sort((a, b) => a.cost[0] - b.cost[0]);
  return { rows, matrix, staircase, authors };
}

module.exports = { build };
