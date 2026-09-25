/* Prototype data: the cube of assumptions.
 *
 * Any three of the account's dials make a cube; every other dial stays at the main case. The account
 * is linear in each dial and has no interaction between dials, so for each of the main case's 64
 * specifications the cost to other US residents is
 *     cost(x) = main + sum_i slope_i * (x_i - mainAt_i)
 * and the break-even is a flat sheet through the cube. This file writes main, slope_i and mainAt_i per
 * specification and gates that formula against the engine at random points with every dial moved at
 * once. The page derives "every public service" (one common share for the six service families, general
 * administration apart) from the six slopes; a gate checks that derivation against the engine too.
 */
"use strict";

const MAIN_R = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };

// label: axis title; what: the unit in words. Ranges match the distance-to-flip rows.
const DIALS = [
  { id: "taxes", label: "Taxes they pay", what: "× what records show", unit: "times", range: [0, 2], mainAt: () => 1 },
  { id: "benefits", label: "Benefits they draw", what: "× what records show", unit: "times", range: [0, 2], mainAt: () => 1 },
  { id: "schools", label: "Schools", what: "share of per-pupil cost", unit: "pct", range: [0, 1], mainAt: (s) => s.school },
  { id: "colleges", label: "Colleges and other education", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: () => 1 },
  { id: "police", label: "Police, courts and prisons", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: () => 1 },
  { id: "health", label: "Public health services", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: () => 1 },
  { id: "other", label: "Welfare offices, housing, community", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: () => 1 },
  { id: "gg", label: "General administration", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: (s) => s.gg },
  { id: "roads", label: "Roads, transport, parks, culture", what: "share of average cost", unit: "pct", range: [0, 1], mainAt: () => 0 },
];
const SIX = ["schools", "colleges", "police", "health", "other", "roads"];
// Dials the page derives from several: one common share for their members. "others" with schools and
// general administration splits every public service budget into three parts, each counted once.
const COMPOSITES = [
  { id: "services", label: "Every public service", what: "one share of average cost", unit: "pct", range: [0, 1], members: SIX },
  { id: "others", label: "Every other public service", what: "one share of average cost", unit: "pct", range: [0, 1],
    members: SIX.filter((k) => k !== "schools") },
];

// The engine's inputs for a full dial vector x (every dial set).
function inputs(x) {
  return [
    { ...MAIN_R, schools: x.schools, colleges: x.colleges, police: x.police, health: x.health, other: x.other,
      gg: x.gg, delayed: x.roads },
    { direct_receipt_response: x.taxes, transfer_response: x.benefits },
  ];
}

// A small deterministic generator, so the gate draws the same points on every run.
function rng(seed) {
  let s = seed >>> 0;
  return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) / 2 ** 32);
}

function build(A) {
  const { cost, mainSpecs, gate, near, span, round } = A;
  const M = A.MODELS.adopted;
  const evalAt = (spec, x) => {
    const [r, extra] = inputs(x);
    return cost(spec, r, M, extra);
  };

  const specs = mainSpecs.map((spec) => {
    const at = Object.fromEntries(DIALS.map((d) => [d.id, d.mainAt(spec)]));
    const main = evalAt(spec, at);
    const slope = {};
    for (const d of DIALS) slope[d.id] = evalAt(spec, { ...at, [d.id]: 1 }) - evalAt(spec, { ...at, [d.id]: 0 });
    return { spec, main, slope, mainAt: at };
  });
  const main = span(specs.map((s) => s.main));
  gate("main case reproduces A.MAIN", near(main[0], A.MAIN[0], 1e-4) && near(main[1], A.MAIN[1], 1e-4),
    main.map((x) => x.toFixed(4)).join(" to "));

  // The page's formula against the engine, every dial moved at once, 40 random points per specification.
  const formula = (s, x) => s.main + DIALS.reduce((t, d) => t + s.slope[d.id] * (x[d.id] - s.mainAt[d.id]), 0);
  const draw = rng(20260925);
  let worst = 0;
  for (const s of specs) {
    for (let i = 0; i < 40; i++) {
      const x = Object.fromEntries(DIALS.map((d) => [d.id, d.range[0] + draw() * (d.range[1] - d.range[0])]));
      worst = Math.max(worst, Math.abs(formula(s, x) - evalAt(s.spec, x)));
    }
  }
  gate("the linear formula reproduces the engine at 2,560 random points", worst < 1e-8, `worst gap ${worst.toExponential(2)} $bn`);

  // A derived dial: its members' slopes summed, the main case at their slope-weighted mean.
  const cSlope = (s, members) => members.reduce((t, k) => t + s.slope[k], 0);
  const cAt = (s, members) => members.reduce((t, k) => t + s.slope[k] * s.mainAt[k], 0) / cSlope(s, members);
  for (const c of COMPOSITES) {
    let worstComp = 0;
    for (const s of specs) {
      for (const share of [0, 0.37, 1]) {
        const x = { ...s.mainAt, ...Object.fromEntries(c.members.map((k) => [k, share])) };
        const page = s.main + cSlope(s, c.members) * (share - cAt(s, c.members));
        worstComp = Math.max(worstComp, Math.abs(page - evalAt(s.spec, x)));
      }
    }
    gate(`${c.label.toLowerCase()} at one share: derived dial = engine`, worstComp < 1e-8, `worst gap ${worstComp.toExponential(2)}`);
  }
  const compSlope = (s) => cSlope(s, SIX), compAt = (s) => cAt(s, SIX);
  const prop = span(specs.map((s) => s.main + compSlope(s) * (1 - compAt(s))));
  gate("every public service at 100% reproduces the proportional case", near(prop[0], A.PROPORTIONAL[0], 1e-4) &&
    near(prop[1], A.PROPORTIONAL[1], 1e-4), prop.map((x) => x.toFixed(2)).join(" to "));

  // The one-at-a-time roots agree with the distance-to-flip rows (same dials, same ranges).
  const flip = JSON.parse(A.fs.readFileSync(A.path.join(A.HERE, "src", "generated", "proto_flip.json"), "utf8"));
  const rootOf = (s, id) => s.mainAt[id] - s.main / s.slope[id];
  for (const id of ["taxes", "benefits"]) {
    const r = span(specs.map((s) => rootOf(s, id))).map((x) => round(x));
    const want = flip.measured.find((m) => m.id === id).roots;
    gate(`${id} alone turns where the flip figure says`, near(r[0], want[0], 1e-4) && near(r[1], want[1], 1e-4), r.join(" to "));
  }

  // Taxes above records and benefits below by the same share, at once: the share that reaches the sheet.
  const together = span(specs.map((s) => s.main / (s.slope.benefits - s.slope.taxes)));
  gate("taxes up and benefits down together reach the sheet sooner than either alone",
    together[1] < Math.min(...specs.map((s) => 1 - rootOf(s, "benefits"))) &&
    together[1] < Math.min(...specs.map((s) => rootOf(s, "taxes") - 1)), together.map((x) => (100 * x).toFixed(1) + "%").join(" to "));
  const servicesRoot = span(specs.map((s) => compAt(s) - s.main / compSlope(s)));

  // The published break-even (sign_reversal.csv) also varies the production model; the page says so.
  const published = A.readCsv(A.path.join(A.MAIN_CASE, "derived", "sign_reversal.csv"))
    .filter((p) => p.measure.startsWith("service_break_even"));
  const breakEven = [Math.min(...published.map((p) => Number(p.sept24_low))), Math.max(...published.map((p) => Number(p.sept24_high)))];
  gate("every public service alone turns inside the published break-even", servicesRoot[0] >= breakEven[0] - 1e-9 &&
    servicesRoot[1] <= breakEven[1] + 1e-9, `${servicesRoot.map((x) => (100 * x).toFixed(2)).join("–")}% inside ` +
    `${breakEven.map((x) => (100 * x).toFixed(2)).join("–")}%`);

  const order = specs.map((s, i) => [s.main, i]).sort((a, b) => a[0] - b[0]);
  const describe = (spec) => ({ allocation: spec.allocation, normalization: spec.normalization, schoolShare: round(spec.share, 4),
    schools: spec.school, gg: round(spec.gg, 4), uninsured: spec.uc });
  return {
    main: main.map((x) => round(x, 2)),
    dials: DIALS.map(({ mainAt, ...d }) => d),
    composites: COMPOSITES,
    specs: specs.map((s) => ({
      main: round(s.main, 6),
      slope: Object.fromEntries(Object.entries(s.slope).map(([k, v]) => [k, round(v, 6)])),
      mainAt: Object.fromEntries(Object.entries(s.mainAt).map(([k, v]) => [k, round(v, 6)])),
    })),
    lowEnd: order[0][1], highEnd: order.at(-1)[1], gatePoints: specs.length * 40,
    lowEndSpec: describe(specs[order[0][1]].spec),
    together: together.map((x) => round(x)),
    servicesRoot: servicesRoot.map((x) => round(x)),
    publishedBreakEven: breakEven.map((x) => round(x)),
  };
}

module.exports = { build };
