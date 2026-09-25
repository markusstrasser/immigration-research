/* Prototype data: distance to flip.
 *
 * Each row moves one assumption of the main case alone across its whole range, the rest held at the
 * main case, and reports where the cost to other US residents turns into a gain, for every one of
 * the main case's 64 specifications. The account is linear in each dial, so the turning point is an
 * exact root: x* = x0 + (x1 - x0) * c(x0) / (c(x0) - c(x1)).
 *
 * The row "every service at once" is the published break-even (main_case_2026_09_24/sign_reversal.cjs):
 * every ordinary service budget at one common share s of average cost, general administration at its
 * adopted value paired with the uninsured-use key, the production grid with private capital adjusted.
 * It is recomputed here and gated against derived/sign_reversal.csv.
 */
"use strict";

const MAIN_R = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };

function build(A) {
  const { cost, mainSpecs, MODELS, gate, near, span, round } = A;
  const M = MODELS.adopted;
  const main = span(mainSpecs.map((spec) => cost(spec, MAIN_R, M)));
  gate("main case reproduces A.MAIN", near(main[0], A.MAIN[0], 1e-4) && near(main[1], A.MAIN[1], 1e-4),
    main.map((x) => x.toFixed(4)).join(" to "));

  // A dial: at(spec, x) -> [r, extra]; axis [x0, x1]; mainAt(spec) -> the main case's value, or null.
  const DIALS = [
    { id: "schools", label: "Schools", what: "share of the usual per-pupil cost added for their children",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, schools: x }], mainAt: (spec) => spec.school },
    { id: "colleges", label: "Colleges and other education", what: "how much the budget grows for them",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, colleges: x }], mainAt: () => 1 },
    { id: "police", label: "Police, courts and prisons", what: "charged by how much the group uses them",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, police: x }], mainAt: () => 1 },
    { id: "health", label: "Public health services", what: "how much the budget grows for them",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, health: x }], mainAt: () => 1 },
    { id: "other", label: "Welfare offices, housing, community", what: "how much the budget grows for them",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, other: x }], mainAt: () => 1 },
    { id: "gg", label: "General administration", what: "how much it grows with the population",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, gg: x }], mainAt: (spec) => spec.gg },
    { id: "roads", label: "Roads, transport, parks, culture", what: "held fixed in the main case",
      axis: [0, 1], unit: "pct", at: (spec, x) => [{ ...MAIN_R, delayed: x }], mainAt: () => 0 },
    { id: "benefits", label: "Benefits they draw", what: "as a multiple of what records show",
      axis: [0, 2], unit: "times", at: (spec, x) => [MAIN_R, { transfer_response: x }], mainAt: () => 1 },
    { id: "taxes", label: "Taxes they pay", what: "as a multiple of what records show",
      axis: [0, 2], unit: "times", at: (spec, x) => [MAIN_R, { direct_receipt_response: x }], mainAt: () => 1 },
  ];

  function row(d) {
    const c0 = [], c1 = [], roots = [], mains = [];
    for (const spec of mainSpecs) {
      const [x0, x1] = d.axis;
      const a = cost(spec, ...d.at(spec, x0).slice(0, 1), M, d.at(spec, x0)[1]);
      const b = cost(spec, ...d.at(spec, x1).slice(0, 1), M, d.at(spec, x1)[1]);
      // Linearity: the midpoint of the range is the mean of its ends.
      const xm = (x0 + x1) / 2, m = cost(spec, d.at(spec, xm)[0], M, d.at(spec, xm)[1]);
      if (Math.abs(m - (a + b) / 2) > 1e-9) throw new Error(`${d.id} is not linear at ${xm}`);
      c0.push(a); c1.push(b);
      roots.push(a === b ? null : x0 + (x1 - x0) * a / (a - b));
      const mv = d.mainAt(spec);
      mains.push(mv);
      // The main case sits on this row: at its own value the dial reproduces the main-case cost.
      const back = cost(spec, d.at(spec, mv)[0], M, d.at(spec, mv)[1]);
      if (Math.abs(back - cost(spec, MAIN_R, M)) > 1e-9) throw new Error(`${d.id}: main value off the row`);
    }
    const slopes = c0.map((a, i) => c1[i] - a);
    const dir = slopes.every((s) => s > 0) ? 1 : slopes.every((s) => s < 0) ? -1 : 0;
    gate(`${d.id}: one direction across the 64 specifications`, dir !== 0, dir > 0 ? "cost rises" : "cost falls");
    return summarize(d, c0, c1, roots, span(mains), dir);
  }

  function summarize(d, c0, c1, roots, mainRange, dir) {
    const r = span(roots);
    const [x0, x1] = d.axis;
    const clip = (v) => Math.min(x1, Math.max(x0, v));
    // Where every specification is a cost, where every one is a gain, where it depends.
    const strip = dir > 0
      ? { gain: [x0, clip(r[0])], mixed: [clip(r[0]), clip(r[1])], cost: [clip(r[1]), x1] }
      : { cost: [x0, clip(r[0])], mixed: [clip(r[0]), clip(r[1])], gain: [clip(r[1]), x1] };
    const inRange = r[1] >= x0 && r[0] <= x1;
    return {
      id: d.id, label: d.label, what: d.what, unit: d.unit, axis: d.axis, direction: dir,
      main: mainRange.map((x) => round(x)), atStart: span(c0).map((x) => round(x, 2)),
      atEnd: span(c1).map((x) => round(x, 2)), roots: r.map((x) => round(x)), flipsInRange: inRange,
      strip: Object.fromEntries(Object.entries(strip).map(([k, v]) => [k, v.map((x) => round(x))])),
    };
  }

  const rows = DIALS.map(row);
  const byId = Object.fromEntries(rows.map((r) => [r.id, r]));

  // Every service at once: the published break-even, recomputed on the corrected model.
  const pairs = [{ end: "least", g: A.GG[0], uc: "uninsured_use_low" }, { end: "most", g: A.GG[1], uc: "uninsured_use_high" }];
  function together(allocation, s, pair, production, share) {
    const st = A.Engine.defaultState(M);
    st.allocation = allocation;
    st.receipt_scenario = M.receipts.reference;
    st.production = { ...production };
    st.service_response = s;
    st.general_government_response = pair.g;
    st.school_share = share;
    st.key_override = { public_order_safety: "use", medicaid_and_chip_other_medical: pair.uc };
    st.response_override = { [A.CORR.education_school_part]: s * share, [A.CORR.education_other_part]: s * (1 - share),
      [A.CORR.correction_constant]: 1 };
    return -A.Engine.evaluate(M, st).welfare_bn;
  }
  const published = A.readCsv(A.path.join(A.MAIN_CASE, "derived", "sign_reversal.csv"));
  const tc0 = [], tc1 = [], troots = [];
  for (const allocation of ["personal", "shared"]) {
    const ends = { least: [], most: [] };
    for (const pair of pairs) for (const prod of A.saneProductionDims) for (const share of A.SHARES) {
      const a = together(allocation, 0, pair, prod, share), b = together(allocation, 1, pair, prod, share);
      tc0.push(a); tc1.push(b);
      const root = a / (a - b);
      troots.push(root);
      ends[pair.end].push(root);
    }
    const be = [Math.min(...ends.most), Math.max(...ends.least)];
    const want = published.find((p) => p.measure === `service_break_even_${allocation}`);
    gate(`every service at once, ${allocation}: sign_reversal.csv reproduces`,
      near(be[0], Number(want.sept24_low), 1e-4) && near(be[1], Number(want.sept24_high), 1e-4),
      be.map((x) => (100 * x).toFixed(2) + "%").join(" to "));
  }
  // The published break-even pairs the ends (least with least); report that pairing, as the page does.
  const publishedBe = [Math.min(...published.filter((p) => p.measure.startsWith("service_break_even")).map((p) => Number(p.sept24_low))),
    Math.max(...published.filter((p) => p.measure.startsWith("service_break_even")).map((p) => Number(p.sept24_high)))];
  const all = summarize({ id: "all", label: "Every public service", what: "at one common share of its average cost",
    axis: [0, 1], unit: "pct" }, tc0, tc1, troots, [NaN, NaN], 1);
  all.main = null;
  all.roots = publishedBe;
  all.strip = { gain: [0, round(publishedBe[0])], mixed: [round(publishedBe[0]), round(publishedBe[1])], cost: [round(publishedBe[1]), 1] };
  gate("every service at once: the root range lies inside the full sweep", troots.every((x) => x > 0) &&
    Math.min(...troots) <= publishedBe[0] + 1e-9 && Math.max(...troots) >= publishedBe[1] - 1e-9);

  // The gain from their work: what it would have to be for the cost to reach zero.
  const pf = mainSpecs.map((spec) => A.Engine.evaluate(M, A.stateFor(spec, MAIN_R, M)).production_gain_bn);
  const needed = mainSpecs.map((spec, i) => cost(spec, MAIN_R, M) + pf[i]);
  const gain = {
    id: "production", label: "Gain from their work", what: "wages, profits and the taxes on them, $bn a year",
    unit: "bn", axis: [0, 300], direction: -1, main: span(pf).map((x) => round(x, 2)),
    executed: A.PROD_SPAN.map((x) => round(x, 2)), roots: span(needed).map((x) => round(x, 1)), flipsInRange: true,
  };
  gain.strip = { cost: [0, gain.roots[0]], mixed: [gain.roots[0], gain.roots[1]], gain: [gain.roots[1], 300] };
  gate("gain from their work: the needed gain exceeds every executed model", gain.roots[0] > A.PROD_SPAN[1],
    `$${gain.roots[0]}–${gain.roots[1]}bn needed; models give $${gain.executed[0]}–${gain.executed[1]}bn`);

  // Every other executed choice, on the main case's service choices (the matrix's outer range).
  const outer = { lo: Infinity, hi: -Infinity };
  for (const g of A.GG) {
    const r = { ...MAIN_R, gg: g };
    const direct = span(A.outerSpecs.map((spec) => cost(spec, { ...r, production: false }, M)));
    outer.lo = Math.min(outer.lo, direct[0] - A.PROD_SPAN[1]);
    outer.hi = Math.max(outer.hi, direct[1] - A.PROD_SPAN[0]);
  }
  const figures = JSON.parse(A.fs.readFileSync(A.path.join(A.HERE, "src", "generated", "figures.json"), "utf8"));
  const mainRow = figures.matrix.rows.find((r) => r.schools === "cbo" && r.colleges === 1 && r.delayed === 0);
  const fromMatrix = mainRow.cells.filter((c) => A.GG.some((g) => near(c.gg, g, 1e-12)));
  gate("every other choice = the matrix's outer range on the main row", near(round(outer.lo), Math.min(...fromMatrix.map((c) => c.outer[0])), 1e-4)
    && near(round(outer.hi), Math.max(...fromMatrix.map((c) => c.outer[1])), 1e-4), `${outer.lo.toFixed(1)} to ${outer.hi.toFixed(1)}`);
  gate("no executed choice turns the sign", outer.lo > 0);

  const order = ["schools", "colleges", "police", "health", "other", "gg", "roads"];
  return {
    main: main.map((x) => round(x, 2)),
    services: order.map((id) => byId[id]),
    together: all,
    measured: [byId.benefits, byId.taxes, gain],
    others: { range: [round(outer.lo, 1), round(outer.hi, 1)], taxRules: A.RECEIPTS.length,
      justiceKeys: A.JUSTICE_KEYS.length, careKeys: A.UC_KEYS.length, productionModels: A.saneProduction.length },
  };
}

module.exports = { build };
