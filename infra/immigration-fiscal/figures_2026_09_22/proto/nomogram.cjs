/* Prototype data: nomogram. An exact alignment chart (d'Ocagne) of the complete account.
 *
 * For one executed specification the account is a straight sum of the three service dials:
 *   cost = c0 + a·schools + b·other + g·admin      ($bn a year, positive = cost to everyone else)
 * with roads, transport and parks held at 0 and the gain from the group's work counted, as in the
 * main case. The chart is drawn for the main case's low end (the specification most favourable to
 * the group). The coefficients come from the engine at the eight corners of the dial cube; the
 * gates check that the corners predict interior points, that the drawn construction reads the
 * main case and the frozen setting exactly, and that it reproduces the engine at 20 random
 * settings. The main case's other open choices (16 combinations, each also a plane in the dials)
 * give the band the page tints on the result scale. The page (src/proto/Nomogram.svelte) repeats
 * the construction from the geometry here.
 */
"use strict";

// Dials: schools, every other service together, general administration (0 = does not grow for
// them, 1 = grows one for one with the population). Roads stay fixed; production is counted.
const dial = (s, o, g) => ({ schools: s, colleges: o, police: o, health: o, other: o, delayed: 0, gg: g, production: true });
const MAIN_R = { schools: "cbo", colleges: 1, police: 1, health: 1, other: 1, delayed: 0, gg: "band", production: true };
const FROZEN_R = dial(0, 0, 0);

// Plain words for the account's open choices (explorer ui.js help texts).
const WORDS = {
  allocation: {
    shared: "taxes and benefits pooled within each household",
    personal: "each person’s own taxes and benefits",
  },
  normalization: {
    gdp: "the gain from their work scaled to national GDP",
    cash: "the gain from their work scaled to the earnings people report",
  },
  uc: {
    uninsured_use_low: "unpaid hospital care keyed to the lower estimate of uninsured use",
    uninsured_use_high: "unpaid hospital care keyed to the higher estimate of uninsured use",
  },
};

/* Seeded generator for the random settings, so every run checks the same points. */
function lcg(seed) {
  let x = seed >>> 0;
  return () => {
    x = (Math.imul(x, 1664525) + 1013904223) >>> 0;
    return x / 2 ** 32;
  };
}

/* The straightedge: the height of the line through p and q where it crosses the vertical at x. */
const at = (p, q, x) => p[1] + ((q[1] - p[1]) * (x - p[0])) / (q[0] - p[0]);

function build(A) {
  const { gate, near, cost, span, MODELS, mainSpecs, MAIN, SHARES } = A;
  const M = MODELS.adopted;

  /* ------------------------------------------------------------ the main case and its ends --- */
  const mainRuns = mainSpecs.map((spec) => ({ spec, cost: cost(spec, MAIN_R, M) }));
  const got = span(mainRuns.map((x) => x.cost));
  gate("main case reproduces A.MAIN", near(got[0], MAIN[0], 1e-4) && near(got[1], MAIN[1], 1e-4),
    `${got[0].toFixed(4)} to ${got[1].toFixed(4)}`);
  const sorted = mainRuns.slice().sort((p, q) => p.cost - q.cost);
  const low = sorted[0];
  const high = sorted.at(-1);
  gate("the main case's low end is one specification", sorted[1].cost - low.cost > 1e-6,
    `next lowest ${sorted[1].cost.toFixed(4)}`);
  const spec = low.spec;
  for (const k of ["allocation", "normalization", "uc"]) {
    if (!WORDS[k][spec[k]] || !WORDS[k][high.spec[k]]) throw new Error(`no words for ${k} = ${spec[k]} / ${high.spec[k]}`);
  }

  /* ------------------------------------------------------------ linearity ------------------- */
  const f = (s, o, g) => cost(spec, dial(s, o, g), M);
  const c0 = f(0, 0, 0);
  const k = { c0, a: f(1, 0, 0) - c0, b: f(0, 1, 0) - c0, g: f(0, 0, 1) - c0 };
  const lin = (s, o, g) => k.c0 + k.a * s + k.b * o + k.g * g;
  let cornerErr = 0;
  for (const s of [0, 1]) for (const o of [0, 1]) for (const g of [0, 1]) cornerErr = Math.max(cornerErr, Math.abs(f(s, o, g) - lin(s, o, g)));
  gate("eight corners fit one plane (no interaction between dials)", cornerErr < 1e-9, `max error ${cornerErr.toExponential(1)}`);
  const rnd = lcg(20260925);
  const interior = Array.from({ length: 20 }, () => [rnd(), rnd(), rnd()]);
  interior.push([spec.school, 1, spec.gg]);
  const linErr = Math.max(...interior.map(([s, o, g]) => Math.abs(f(s, o, g) - lin(s, o, g))));
  gate("corners predict 21 interior points to 1e-9", linErr < 1e-9, `max error ${linErr.toExponential(1)}`);

  /* ------------------------------------------------------------ geometry -------------------- */
  // Every input scale gets the same length per dollar (modulus m), so a scale's length is the most
  // its dial can add to the bill. For a straightedge between two parallel scales of moduli m1, m2,
  // the sum's scale sits at m1/(m1+m2) of the way from the first and has modulus m1·m2/(m1+m2).
  const W = 760;
  const TALLEST = 500; // px, the longest input scale
  const m = TALLEST / Math.max(k.a, k.b, k.g);
  const mod = { S: m, O: m, G: m };
  const tT = mod.S / (mod.S + mod.O);
  mod.T = (mod.S * mod.O) / (mod.S + mod.O);
  const tC = mod.T / (mod.T + mod.G);
  mod.C = (mod.T * mod.G) / (mod.T + mod.G);
  // Outer scales at fixed margins; the other-services scale is placed so that the cost scale sits
  // GAP to its right: x_C - x_O = GAP, with x_T = x_S + tT(x_O - x_S), x_C = x_T + tC(x_G - x_T).
  // xG leaves the cost scale near 334, so its title fits the first screen of a phone.
  const xS = 104;
  const xG = 660;
  const GAP = 96;
  const xO = ((1 - tC) * (1 - tT) * xS + tC * xG - GAP) / (1 - (1 - tC) * tT);
  const xT = xS + tT * (xO - xS);
  const xC = xT + tC * (xG - xT);
  // The page's side note says "halfway" and "a third"; equal moduli make both true.
  gate("turning line halfway, cost scale a third of the way at a third of the modulus",
    near(tT, 1 / 2, 1e-12) && near(tC, 1 / 3, 1e-12) && near(mod.C / m, 1 / 3, 1e-12) &&
    near((xT - xS) / (xO - xS), 1 / 2, 1e-12) && near((xC - xT) / (xG - xT), 1 / 3, 1e-12));
  // Every scale reads 0 on one top line and grows downward, so the frozen setting is the flat top
  // line and the cost scale runs from better off at the top to worse off at the bottom (the page's
  // visual grammar: a vertical axis runs better off up). Titles sit above the top line, where no
  // straightedge goes.
  const top = 100;
  const H = top + TALLEST + 52;
  const x = { S: xS, T: xT, O: xO, C: xC, G: xG };
  const yS = (s) => top + mod.S * k.a * s;
  const yO = (o) => top + mod.O * k.b * o;
  const yG = (g) => top + mod.G * k.g * g;
  const yC = (c) => top + mod.C * (c - k.c0);

  /* The construction, as the page draws it: schools to other services, read the turning line;
   * turning point to general administration, read the cost scale. */
  function construct(s, o, g) {
    const S = [x.S, yS(s)], O = [x.O, yO(o)], G = [x.G, yG(g)];
    const T = [x.T, at(S, O, x.T)];
    const C = [x.C, at(T, G, x.C)];
    return { S, O, T, G, C, cost: k.c0 + (C[1] - top) / mod.C };
  }
  gate("better off is up: the result scale's better-off end sits above its worse-off end", yC(k.c0) < yC(0) && yC(0) < yC(lin(1, 1, 1)));

  /* ------------------------------------------------------------ readings -------------------- */
  const mainCost = cost(spec, MAIN_R, M);
  const mainRead = construct(spec.school, 1, spec.gg).cost;
  gate("reading at the main case = A.cost() for the spec", near(mainRead, mainCost, 1e-9) && near(mainCost, MAIN[0], 1e-4),
    `${mainRead.toFixed(6)} vs ${mainCost.toFixed(6)}`);
  const frozenCost = cost(spec, FROZEN_R, M);
  const frozenRead = construct(0, 0, 0).cost;
  gate("reading at (0,0,0) = frozen cost for the spec", near(frozenRead, frozenCost, 1e-9), `${frozenRead.toFixed(6)} vs ${frozenCost.toFixed(6)}`);
  // The same frozen setting in the figures page's matrix (every service fixed, admin 0): the spec is
  // its most favourable end.
  const frozenRow = span(mainSpecs.map((sp) => cost(sp, FROZEN_R, M)));
  gate("frozen reading = matrix frozen row (admin 0), most favourable end", near(frozenRead, frozenRow[0], 1e-9),
    `${frozenRow[0].toFixed(4)} to ${frozenRow[1].toFixed(4)}`);
  const rnd2 = lcg(424242);
  let geoErr = 0;
  for (let i = 0; i < 20; i++) {
    const [s, o, g] = [rnd2(), rnd2(), rnd2()];
    geoErr = Math.max(geoErr, Math.abs(construct(s, o, g).cost - f(s, o, g)));
  }
  gate("construction reproduces the engine at 20 random settings to 0.01bn", geoErr < 0.01, `max error ${geoErr.toExponential(1)}bn`);
  // The page tints the foot of the turning line blue up to v0 = -c0 - g·admin: a first straightedge
  // crossing there reads zero, below it a gain. Check the boundary through the drawn construction.
  let zoneErr = 0;
  for (const g of [0, spec.gg, 1]) {
    const v0 = -k.c0 - k.g * g;
    for (const [s, o] of [[v0 / k.a, 0], [0, v0 / k.b], [v0 / (2 * k.a), v0 / (2 * k.b)]]) {
      zoneErr = Math.max(zoneErr, Math.abs(construct(s, o, g).cost), Math.abs(f(s, o, g)));
    }
  }
  gate("turning-line gain boundary reads zero (construction and engine)", zoneErr < 1e-9, `max ${zoneErr.toExponential(1)}bn`);
  // The drawn points stay on their scales.
  const hi = construct(1, 1, 1);
  gate("construction at (1,1,1) tops the cost scale", near(hi.cost, lin(1, 1, 1), 1e-9) && near(hi.C[1], yC(lin(1, 1, 1)), 1e-9),
    `${hi.cost.toFixed(2)}bn`);

  /* ------------------------------------------------------------ facts for the text ---------- */
  // The page's words assume these signs and sizes: every dial adds cost (scales growing down from
  // the top line, "+" in the formula), the frozen setting leaves everyone else better off, and equal
  // dials break even near 0.2.
  gate("every dial adds cost", k.a > 0 && k.b > 0 && k.g > 0);
  gate("frozen setting is a gain to everyone else", frozenCost < 0, `${frozenCost.toFixed(2)}bn`);
  const zero = -k.c0 / (k.a + k.b + k.g); // equal dials: the sign turns here; also zero's height on the scale
  gate("with equal dials everyone else breaks even near 0.2", zero > 0.17 && zero < 0.23, zero.toFixed(4));
  const schoolsAlone = lin(spec.school, 0, 0);
  gate("schools at the spec's value alone read a cost", schoolsAlone > 0, `${schoolsAlone.toFixed(2)}bn`);
  /* ------------------------------------------------------------ the other open choices ------- */
  // With the dials set by hand, the main case's remaining open choices are allocation,
  // normalization, the school share of education spending and the unpaid-care key: 16
  // combinations. Each is one plane in the dials too; the page tints the result scale between the
  // lowest and highest of the 16 readings at the dials' current settings.
  const others = A.product({ allocation: ["personal", "shared"], normalization: ["cash", "gdp"], share: SHARES,
    uc: ["uninsured_use_low", "uninsured_use_high"], justice: ["use"] });
  let spreadErr = 0;
  const spread = others.map((sp) => {
    const h = (s, o, g) => cost({ ...sp, school: spec.school, gg: spec.gg }, dial(s, o, g), M);
    const q0 = h(0, 0, 0);
    const q = { c0: q0, a: h(1, 0, 0) - q0, b: h(0, 1, 0) - q0, g: h(0, 0, 1) - q0 };
    const pts = [[1, 1, 0], [1, 0, 1], [0, 1, 1], [1, 1, 1], ...interior.slice(0, 5)];
    for (const [s, o, g] of pts) spreadErr = Math.max(spreadErr, Math.abs(h(s, o, g) - (q.c0 + q.a * s + q.b * o + q.g * g)));
    return q;
  });
  gate("each of the 16 other combinations is one plane in the dials", spreadErr < 1e-9, `max error ${spreadErr.toExponential(1)}`);
  gate("the drawn combination is one of the 16", spread.some((q) => ["c0", "a", "b", "g"].every((n) => near(q[n], k[n], 1e-12))));
  const range = (s, o, g) => span(spread.map((q) => q.c0 + q.a * s + q.b * o + q.g * g));
  const atMain = range(spec.school, 1, spec.gg);
  gate("at the main case's dials the band starts at the drawn reading", near(atMain[0], mainCost, 1e-9),
    `${atMain[0].toFixed(4)} to ${atMain[1].toFixed(4)}`);
  const atHigh = range(high.spec.school, 1, high.spec.gg);
  gate("at the other end's dials the band reaches A.MAIN's other end", near(atHigh[1], MAIN[1], 1e-4),
    `${atHigh[0].toFixed(4)} to ${atHigh[1].toFixed(4)}`);
  const envelope = span(A.CBO_SCHOOLS.flatMap((s) => A.GG.flatMap((g) => range(s, 1, g))));
  gate("over the main case's dial choices the band spans A.MAIN", near(envelope[0], MAIN[0], 1e-4) && near(envelope[1], MAIN[1], 1e-4),
    `${envelope[0].toFixed(4)} to ${envelope[1].toFixed(4)}`);
  const atFrozen = range(0, 0, 0);
  gate("at (0,0,0) the band is the matrix frozen row", near(atFrozen[0], frozenRow[0], 1e-9) && near(atFrozen[1], frozenRow[1], 1e-9),
    `${atFrozen[0].toFixed(4)} to ${atFrozen[1].toFixed(4)}`);
  // Every dial adds cost in every combination, so over the dial cube the band's extremes sit at
  // (0,0,0) and (1,1,1): the result scale runs from the drawn frozen reading to the highest
  // combination at (1,1,1), a little past the drawn combination's own end.
  gate("every dial adds cost in all 16 combinations", spread.every((q) => q.a > 0 && q.b > 0 && q.g > 0));
  const ceiling = range(1, 1, 1)[1];
  gate("the result scale covers every reading", near(atFrozen[0], k.c0, 1e-9) && ceiling >= lin(1, 1, 1),
    `${k.c0.toFixed(2)} to ${ceiling.toFixed(2)}bn`);

  // The drawn spec is the low end at the main case. Elsewhere another combination of the account's
  // other open choices can sit lower; the largest such gap sits at a corner (a maximum of planes).
  // Ties (general administration weighs the same in every combination) keep the first corner.
  let order = { gap: 0 };
  for (const s of [0, 1]) for (const o of [0, 1]) for (const g of [0, 1]) {
    for (const sp of others) {
      const d = lin(s, o, g) - cost({ ...sp, school: spec.school, gg: spec.gg }, dial(s, o, g), M);
      if (d > order.gap + 1e-9) order = { gap: d, s, o, g, share: sp.share };
    }
  }
  gate("ordering gap found at a corner", order.gap > 0 && order.gap < 100, `${order.gap.toFixed(2)}bn at (${order.s}, ${order.o}, ${order.g})`);

  // Dollars per other resident for the page's readout: the engine's own divisor
  // (evaluate().per_other_resident).
  const meta = M.meta;
  const residents = meta.resident_population - meta.target_population;
  const probe = A.Engine.evaluate(M, A.Engine.defaultState(M));
  gate("per-resident readout uses the engine's divisor", near(probe.per_other_resident * residents / 1e9, probe.welfare_bn, 1e-9),
    `${(residents / 1e6).toFixed(1)} million other residents`);

  console.log(`    spec: ${spec.allocation}, ${spec.normalization}, school share ${spec.share.toFixed(3)}, ${spec.uc}`);
  console.log(`    cost = ${k.c0.toFixed(3)} + ${k.a.toFixed(3)}·s + ${k.b.toFixed(3)}·o + ${k.g.toFixed(3)}·g`);
  console.log(`    x: S ${xS} T ${xT.toFixed(1)} O ${xO.toFixed(1)} C ${xC.toFixed(1)} G ${xG}; m ${m.toFixed(4)} px/$bn`);
  console.log(`    band of the 16 other combinations: main dials ${atMain.map((v) => v.toFixed(2)).join(" to ")}, ` +
    `frozen ${atFrozen.map((v) => v.toFixed(2)).join(" to ")}, (1,1,1) ${range(1, 1, 1).map((v) => v.toFixed(2)).join(" to ")}`);

  const describe = (sp) => ({
    allocation: sp.allocation, normalization: sp.normalization, share: sp.share, school: sp.school, gg: sp.gg, uc: sp.uc,
    words: [WORDS.allocation[sp.allocation], WORDS.normalization[sp.normalization], WORDS.uc[sp.uc]],
  });

  return {
    k,
    spec: describe(spec),
    high: { ...describe(high.spec), cost: high.cost },
    band: MAIN,
    main: { s: spec.school, o: 1, g: spec.gg, cost: mainCost },
    // The main case's own choices for the schools and general-administration dials.
    dials: { school: A.CBO_SCHOOLS, gg: A.GG },
    // The 16 combinations of the other open choices, each as a plane in the dials.
    spread,
    ceiling,
    frozen: frozenCost,
    full: lin(1, 1, 1),
    zero,
    schoolsAlone,
    order,
    residents,
    geometry: {
      W, H, top, x, mod,
      // Graduations: [minor, middle, major, labelled] steps, in dial units or $bn.
      ticks: {
        S: [0.01, 0.05, 0.1, 0.1],
        O: [0.01, 0.05, 0.1, 0.1],
        G: [0.02, 0.1, 0.1, 0.2],
        C: [5, 10, 50, 50],
      },
    },
  };
}

module.exports = { build };
