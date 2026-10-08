/* Prototype data: dots. Two heaps of dots, one dot = $1bn a year. The left heap is what the
 * Mexican-origin population brings in for everyone else (the taxes the account counts and the gain
 * from its work); the right heap is what it draws (benefits, then each public service as the account
 * counts it). A pool holds what the account assigns to the group but does not count. The steps are
 * the staircase's; the spec is one executed spec, the main case's low end (the one most favourable to
 * the group).
 *
 * cost() in account_sept24.cjs returns only the total. build() rebuilds cost()'s engine state for each
 * step (the construction is copied below), reads Engine.evaluate()'s receipts, spending, P and F, and
 * sorts every line into a family. Gates: the main case reproduces A.MAIN; the copied steps match
 * build_data.cjs; the band at every step matches figures.json's staircase; the rebuilt total equals
 * A.cost() at every step; the families add up to it; each family's counted and full amounts equal
 * the change in A.cost() when only its own dial moves; the lines outside the families count nothing.
 */
"use strict";
const vm = require("vm");

// The staircase's steps, copied from build_data.cjs (requiring that file writes the figures page's
// data). The first gate compares these copies with the literals in build_data.cjs as it stood on the
// September 24 case (account_sept24.cjs PINS.page).
const TALLY = { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0, gg: 0, production: false, uc: false };
const STEPS = [
  { id: "tally", label: "Taxes paid minus benefits received", note: "no services, no gain from their work", r: {} },
  { id: "production", label: "Gain from their work", note: "wages, profits and the taxes on them", r: { production: true } },
  { id: "uc", label: "Unpaid hospital care", note: "keyed to uninsured use", r: { uc: true } },
  { id: "schools", label: "Schools, 63–66% of per-pupil cost", note: "from CBO’s coefficients", r: { schools: "cbo" } },
  { id: "colleges", label: "Colleges and other education", r: { colleges: 1 } },
  { id: "police", label: "Police, courts and prisons", note: "charged by use", r: { police: 1 } },
  { id: "health", label: "Public health services", r: { health: 1 } },
  { id: "other", label: "Welfare administration, housing, community", r: { other: 1 } },
  { id: "gg", label: "General administration, 0.59–0.84", note: "cross-state scale of administration", r: { gg: "band" } },
  { id: "taxes", label: "Data corrections: taxes", note: "legal status, survey fill-ins, CBO’s income shares", model: "taxes" },
  { id: "benefits", label: "Data corrections: benefits, services", note: "credits, medical care, schools, care work",
    model: "adopted", main: true },
  { id: "delayed", label: "Roads, transport, parks and culture", note: "held fixed in the main case", r: { delayed: 1 }, beyond: true },
  { id: "schools_full", label: "Schools at the full per-pupil cost", r: { schools: 1 }, beyond: true },
];
const MAIN_R = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };

// Parts: the engine's lines sorted by the dial that moves them between "not counted" and counted
// (null: counted in full at every step).
const PARTS = [
  { id: "taxes", label: "taxes they pay", dial: null },
  { id: "gain", label: "gain from their work", dial: "production" },
  { id: "benefits", label: "benefit programmes", dial: null },
  { id: "hospital", label: "unpaid hospital care", dial: "uc" },
  { id: "schools", label: "schools", dial: "schools" },
  { id: "colleges", label: "colleges and other education", dial: "colleges" },
  { id: "police", label: "police, courts, prisons", dial: "police" },
  { id: "health", label: "public health", dial: "health" },
  { id: "welfare", label: "welfare offices, housing, community", dial: "other" },
  { id: "admin", label: "general administration", dial: "gg" },
  { id: "roads", label: "roads, transport, parks, culture", dial: "delayed" },
];
// Families: the colours of the figure, bottom of each heap first. Eight, so each keeps its own hue;
// a family's parts are named in its label.
const FAMILIES = [
  { id: "taxes", side: "in", label: "Taxes they pay", parts: ["taxes"] },
  { id: "gain", side: "in", label: "Gain from their work", parts: ["gain"] },
  { id: "benefits", side: "out", label: "Benefits", parts: ["benefits", "hospital"] },
  { id: "education", side: "out", label: "Schools and colleges", parts: ["schools", "colleges"] },
  { id: "police", side: "out", label: "Police, courts, prisons", parts: ["police"] },
  { id: "services", side: "out", label: "Health, welfare offices, housing", parts: ["health", "welfare"] },
  { id: "admin", side: "out", label: "General administration", parts: ["admin"] },
  { id: "roads", side: "out", label: "Roads, transport, parks", parts: ["roads"] },
];
// Spending lines of the service families (education and the transfer lines are split below).
const SERVICE_LINES = {
  police: ["public_order_safety"], health: ["health_services"],
  welfare: ["income_security_services", "housing_community_services"], admin: ["general_public_services"],
  roads: ["economic_affairs_services", "recreation_culture"],
};
const MEDICAID = "medicaid_and_chip_other_medical";
// Lines the account never counts in these steps: defense, interest on existing debt, subsidies,
// foreign flows, rounding. Gated to count nothing at every step.
const NEVER = new Set(["public_goods", "interest", "subsidy", "foreign", "rounding"]);

/* cost()'s engine state (account_sept24.cjs), copied so the lines can be read; a gate checks the total. */
function buildState(A, spec, r, m) {
  const { Engine, model, CORR } = A;
  const s = Engine.defaultState(m);
  s.allocation = spec.allocation;
  s.receipt_scenario = spec.receipts || model.receipts.reference;
  if (spec.production) Object.assign(s.production, spec.production);
  if (spec.normalization) s.production.normalization = spec.normalization;
  s.count_production = r.production;
  s.general_government_response = r.gg === "band" ? spec.gg : r.gg;
  s.key_override = {};
  if (spec.justice) s.key_override.public_order_safety = spec.justice;
  if (r.uc !== false && spec.uc) s.key_override.medicaid_and_chip_other_medical = spec.uc;
  const schools = r.schools === "cbo" ? spec.school : r.schools;
  s.response_override = {
    education_services: spec.share * schools + (1 - spec.share) * r.colleges,
    public_order_safety: r.police,
    health_services: r.health,
    income_security_services: r.other,
    housing_community_services: r.other,
    economic_affairs_services: r.delayed,
    recreation_culture: r.delayed,
    [CORR.education_school_part]: spec.share * schools,
    [CORR.education_other_part]: (1 - spec.share) * r.colleges,
    [CORR.correction_constant]: 1,
  };
  return s;
}

/* One step split into families: counted (what the step counts) and full (what the account assigns
 * to the group before any share is held fixed). Amounts in $bn a year, positive. */
function decompose(A, spec, r, m) {
  const { Engine, CORR } = A;
  const s = buildState(A, spec, r, m);
  const out = Engine.evaluate(m, s);
  const lines = new Map(out.spending.map((l) => [l.id, l]));
  const amount = (id) => (lines.has(id) ? lines.get(id).amount_bn : 0);  // correction lines: adopted model only
  const draw = (id) => (lines.has(id) ? -lines.get(id).effect_bn : 0);
  const counted = {}, full = {}, used = new Set();

  // Left: the taxes the account counts, and the gain from their work (P + F at fiscal weight 1).
  if (s.fiscal_weight !== 1) throw new Error("the heaps assume a fiscal weight of 1");
  counted.taxes = out.receipts.filter((x) => x.group === "direct_receipts").reduce((t, x) => t + x.effect_bn, 0);
  full.taxes = out.receipts.filter((x) => x.group === "direct_receipts").reduce((t, x) => t + x.amount_bn, 0);
  const incidence = out.receipts.filter((x) => x.group !== "direct_receipts").reduce((t, x) => t + Math.abs(x.effect_bn), 0);
  counted.gain = out.private_wtp_bn + out.induced_receipts_bn;
  const on = Engine.evaluate(m, buildState(A, spec, { ...r, production: true }, m));
  full.gain = on.private_wtp_bn + on.induced_receipts_bn;

  // Right: benefits, with the unpaid-hospital-care re-key of the Medicaid line split out.
  const medBy = (uc) => Engine.evaluate(m, buildState(A, spec, { ...r, uc }, m)).spending.find((l) => l.id === MEDICAID).amount_bn;
  full.hospital = medBy(true) - medBy(false);
  counted.hospital = r.uc !== false ? full.hospital : 0;
  const transfers = out.spending.filter((l) => l.response_class === "household_transfer");
  transfers.forEach((l) => used.add(l.id));
  // The corrections' net care, shelter and audit items (a single constant line) sit with benefits.
  used.add(CORR.correction_constant);
  const constants = draw(CORR.correction_constant);
  counted.benefits = transfers.reduce((t, l) => t - l.effect_bn, 0) - counted.hospital + constants;
  full.benefits = counted.benefits;

  // Education: the line and its two correction lines, split into schools and colleges.
  const schoolsR = r.schools === "cbo" ? spec.school : r.schools;
  const edu = amount("education_services"), sr = amount(CORR.education_school_part), cr = amount(CORR.education_other_part);
  ["education_services", CORR.education_school_part, CORR.education_other_part].forEach((id) => used.add(id));
  full.schools = spec.share * (edu + sr);
  full.colleges = (1 - spec.share) * (edu + cr);
  counted.schools = schoolsR * full.schools;
  counted.colleges = r.colleges * full.colleges;
  const eduDraw = draw("education_services") + draw(CORR.education_school_part) + draw(CORR.education_other_part);

  for (const [fam, ids] of Object.entries(SERVICE_LINES)) {
    ids.forEach((id) => used.add(id));
    counted[fam] = ids.reduce((t, id) => t + draw(id), 0);
    full[fam] = ids.reduce((t, id) => t + amount(id), 0);
  }
  // Every other line must count nothing; every counted line must sit in a family.
  const stray = out.spending.filter((l) => !used.has(l.id));
  const strayEffect = stray.reduce((t, l) => t + Math.abs(l.effect_bn), 0);
  const strayClasses = [...new Set(stray.map((l) => l.response_class))].filter((c) => !NEVER.has(c));
  return { out, counted, full, incidence, eduDraw, strayEffect, strayClasses, cost: -out.welfare_bn,
    classes: out.classes, constants };
}

/* The literal `const NAME = …;` in build_data.cjs, evaluated without running the file. */
function literalIn(text, name, open, close) {
  const start = text.indexOf(`const ${name} = ${open}`);
  if (start < 0) throw new Error(`build_data.cjs has no ${name}`);
  const end = text.indexOf(`${close};`, start);
  return vm.runInNewContext("(" + text.slice(start + `const ${name} = `.length, end + 1) + ")");
}

function build(A) {
  const { gate, near, round, span, MODELS, MAIN, mainSpecs, cost, fs, path, HERE } = A;
  const R4 = (x) => round(x, 4);

  console.log("  (main case)");
  const mainCosts = mainSpecs.map((spec) => cost(spec, MAIN_R, MODELS.adopted));
  const got = span(mainCosts);
  gate("main case over the 64 specs = A.MAIN", near(got[0], MAIN[0], 1e-4) && near(got[1], MAIN[1], 1e-4),
    `${got[0].toFixed(4)} to ${got[1].toFixed(4)}`);
  const lowAt = mainCosts.indexOf(got[0]), highAt = mainCosts.indexOf(got[1]);
  const lowTies = mainCosts.filter((c) => Math.abs(c - got[0]) < 1e-9).length;
  gate("one spec sits at the band's low end", lowTies === 1, `spec ${lowAt} of ${mainSpecs.length}`);
  const spec = mainSpecs[lowAt];

  const listed = FAMILIES.flatMap((f) => f.parts);
  gate("every part sits in exactly one family", listed.length === PARTS.length &&
    PARTS.every((p) => listed.filter((x) => x === p.id).length === 1), `${PARTS.length} parts, ${FAMILIES.length} families`);

  console.log("  (steps copied from build_data.cjs)");
  const text = A.pinned("page", path.join(HERE, "build_data.cjs"));
  const theirs = { TALLY: literalIn(text, "TALLY", "{", "}"), STEPS: literalIn(text, "STEPS", "[", "]") };
  gate("TALLY and STEPS equal build_data.cjs's", JSON.stringify(theirs.TALLY) === JSON.stringify(TALLY) &&
    JSON.stringify(theirs.STEPS) === JSON.stringify(STEPS), `${STEPS.length} steps`);

  // The staircase's band at every step (build_data.cjs's trajectories), against figures.json.
  const figures = JSON.parse(A.pinned("page", path.join(HERE, "src", "generated", "figures.json")));
  const bands = [];
  {
    let r = { ...TALLY }, m = MODELS.base;
    for (const step of STEPS) {
      r = { ...r, ...(step.r || {}) };
      if (step.model) m = MODELS[step.model];
      bands.push(span(mainSpecs.map((sp) => cost(sp, r, m))));
    }
  }
  const drift = bands.map((b, k) => Math.max(Math.abs(R4(b[0]) - figures.staircase[k].total[0]), Math.abs(R4(b[1]) - figures.staircase[k].total[1])));
  gate("band at every step = figures.json staircase", figures.staircase.length === STEPS.length &&
    figures.staircase.every((s, k) => s.id === STEPS[k].id) && Math.max(...drift) < 1e-9, `max gap ${Math.max(...drift)}`);

  console.log("  (the spec's steps, family by family)");
  const steps = [];
  let r = { ...TALLY }, m = MODELS.base, modelId = "base";
  const worst = { total: 0, sum: 0, dial: 0, stray: 0, incidence: 0, classes: 0 };
  let strayClasses = [];
  STEPS.forEach((step, k) => {
    r = { ...r, ...(step.r || {}) };
    if (step.model) { m = MODELS[step.model]; modelId = step.model; }
    const d = decompose(A, spec, r, m);
    const total = cost(spec, r, m);
    worst.total = Math.max(worst.total, Math.abs(d.cost - total));
    const sum = (side, what) => FAMILIES.filter((f) => f.side === side).reduce((t, f) => t + f.parts.reduce((u, p) => u + what[p], 0), 0);
    const left = sum("in", d.counted);
    const right = sum("out", d.counted);
    worst.sum = Math.max(worst.sum, Math.abs(right - left - total));
    worst.stray = Math.max(worst.stray, d.strayEffect);
    worst.incidence = Math.max(worst.incidence, d.incidence);
    strayClasses = strayClasses.concat(d.strayClasses);
    // The engine's own class sums: a second path to the taxes and the transfer lines.
    const cls = (c) => (d.classes[c] ? d.classes[c].responsive_bn : 0);
    worst.classes = Math.max(worst.classes, Math.abs(cls("direct_receipts") - d.counted.taxes),
      Math.abs(cls("household_transfer") + cls("correction_constant") - d.counted.benefits - d.counted.hospital),
      Math.abs(cls("education_school_part") + cls("education_other_part") + d.out.spending.find((l) => l.id === "education_services").amount_bn *
        d.out.spending.find((l) => l.id === "education_services").response - d.counted.schools - d.counted.colleges));
    // Each dial alone, through cost(): its full amount (dial at 1 less dial at 0) and what the step counts.
    for (const p of PARTS.filter((x) => x.dial)) {
      let fullBy, countedBy;
      if (p.dial === "production") {
        fullBy = cost(spec, { ...r, production: false }, m) - cost(spec, { ...r, production: true }, m);
        countedBy = cost(spec, { ...r, production: false }, m) - total;
      } else if (p.dial === "uc") {
        fullBy = cost(spec, { ...r, uc: true }, m) - cost(spec, { ...r, uc: false }, m);
        countedBy = total - cost(spec, { ...r, uc: false }, m);
      } else {
        fullBy = cost(spec, { ...r, [p.dial]: 1 }, m) - cost(spec, { ...r, [p.dial]: 0 }, m);
        countedBy = total - cost(spec, { ...r, [p.dial]: 0 }, m);
      }
      worst.dial = Math.max(worst.dial, Math.abs(fullBy - d.full[p.id]), Math.abs(countedBy - d.counted[p.id]));
    }
    // Dots: each part rounds to whole dots, so a part's dots change only when its own amount does; the
    // heap holds the counted dots, the pool the rest.
    const fam = {};
    for (const f of FAMILIES) {
      const counted = f.parts.reduce((t, p) => t + d.counted[p], 0), full = f.parts.reduce((t, p) => t + d.full[p], 0);
      const heap = f.parts.reduce((t, p) => t + Math.round(d.counted[p]), 0);
      const all = f.parts.reduce((t, p) => t + Math.round(d.full[p]), 0);
      fam[f.id] = { counted: R4(counted), full: R4(full), heap, pool: all - heap,
        parts: Object.fromEntries(f.parts.map((p) => [p, { counted: R4(d.counted[p]), full: R4(d.full[p]),
          heap: Math.round(d.counted[p]), pool: Math.round(d.full[p]) - Math.round(d.counted[p]) }])) };
    }
    const dotsIn = FAMILIES.filter((f) => f.side === "in").reduce((t, f) => t + fam[f.id].heap, 0);
    const dotsOut = FAMILIES.filter((f) => f.side === "out").reduce((t, f) => t + fam[f.id].heap, 0);
    steps.push({
      id: step.id, label: step.label, note: step.note || null, main: !!step.main, beyond: !!step.beyond, model: modelId,
      constants: R4(d.constants),
      cost: R4(total), band: bands[k].map(R4), left: R4(left), right: R4(right),
      dots: { left: dotsIn, right: dotsOut, gap: dotsOut - dotsIn, error: R4(dotsOut - dotsIn - total),
        roundedMatch: dotsOut - dotsIn === Math.round(total) },
      fam,
    });
  });
  gate("rebuilt state = A.cost() at every step", worst.total < 1e-9, `max ${worst.total.toExponential(1)}`);
  gate("families add up to the cost at every step", worst.sum < 1e-9, `max ${worst.sum.toExponential(1)}`);
  gate("each family = A.cost() moving only its dial", worst.dial < 1e-9, `max ${worst.dial.toExponential(1)}`);
  gate("taxes, transfers, education = engine class sums", worst.classes < 1e-9, `max ${worst.classes.toExponential(1)}`);
  gate("lines outside the families count nothing", worst.stray === 0 && strayClasses.length === 0,
    `defense, interest, subsidies, foreign, rounding: ${worst.stray}`);
  gate("corporate, property and asset receipts count nothing", worst.incidence === 0, `${worst.incidence}`);
  const main = steps.find((s) => s.main);
  gate("main-case step = A.MAIN[0]", near(main.cost, MAIN[0], 1e-4), `${main.cost} vs ${MAIN[0]}`);
  const negative = steps.flatMap((s) => FAMILIES.filter((f) => s.fam[f.id].heap < 0 || s.fam[f.id].pool < 0).map((f) => `${s.id}/${f.id}`));
  gate("no family has negative dots", negative.length === 0, negative.join(" ") || `${steps.length} steps × ${FAMILIES.length} families`);
  const maxError = Math.max(...steps.map((s) => Math.abs(s.dots.error)));
  gate("dot gap within one dot of the exact cost at every step", maxError < 1, steps.map((s) => s.dots.error.toFixed(2)).join(" "));
  gate("main-case dot gap = the main case rounded", main.dots.roundedMatch, `${main.dots.gap} dots, $${main.cost}bn`);
  for (const s of steps) {
    console.log(`    ${s.label.padEnd(44)} cost ${s.cost.toFixed(2).padStart(8)}  dots ${String(s.dots.left).padStart(3)} | ` +
      `${String(s.dots.right).padStart(3)}  gap ${String(s.dots.gap).padStart(4)}  error ${s.dots.error.toFixed(2)}`);
  }

  // What the account never charges in these steps, at a per-head share, and the corporate, property
  // and asset receipts assigned to the group, which it does not count as revenue (the production gain
  // already counts that income). Read at the main-case step.
  const mainOut = Engine_evaluate(A, spec, MAIN_R, MODELS.adopted);
  const byClass = (c) => mainOut.spending.filter((l) => l.response_class === c).reduce((t, l) => t + l.amount_bn, 0);
  const never = {
    defense: R4(mainOut.spending.find((l) => l.id === "defense").amount_bn),
    generalAdminRest: R4(main.fam.admin.full - main.fam.admin.counted),
    interest: R4(byClass("interest")),
    subsidies: R4(byClass("subsidy")),
    corporateProperty: R4(mainOut.receipts.filter((x) => x.group !== "direct_receipts").reduce((t, x) => t + x.amount_bn, 0)),
  };
  const highSpec = mainSpecs[highAt];
  const plain = (sp) => ({
    allocation: sp.allocation, normalization: sp.normalization, share: R4(sp.share), school: sp.school, gg: R4(sp.gg), uc: sp.uc,
    justice: sp.justice,
  });
  // The corrections' constant line (care work, shelter, audit rows), which the benefits layer carries.
  const constantsLine = MODELS.adopted.spending.lines.find((l) => l.response_class === "correction_constant");
  return {
    unitBn: 1,  // one dot; every part rounds to whole units of it (Math.round above)
    specCount: mainSpecs.length,
    constantsLabel: constantsLine.label,
    spec: { index: lowAt, ...plain(spec), mainCost: R4(got[0]) },
    otherEnd: { index: highAt, ...plain(highSpec), mainCost: R4(got[1]) },
    band: { main: MAIN.map(R4), proportional: A.PROPORTIONAL.map(R4) },
    families: FAMILIES.map(({ id, side, label, parts }) => ({ id, side, label, parts })),
    parts: Object.fromEntries(PARTS.map(({ id, label, dial }) => [id, { label, dial }])),
    steps,
    maxDotError: R4(maxError),
    never,
  };
}

function Engine_evaluate(A, spec, r, m) {
  return A.Engine.evaluate(m, buildState(A, spec, r, m));
}

module.exports = { build };
