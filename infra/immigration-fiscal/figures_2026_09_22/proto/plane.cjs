/* Prototype data: the break-even plane (after Goh's "Why Momentum Really Works", Distill 2017).
 *
 * The account is exactly additive in four quantities: how much of the main case's service growth is
 * charged (k: 0 = public services do not grow with the group, 1 = the main case), taxes and benefits
 * as multiples of what records show (t, b), and the gain from their work (P, $bn). So for each of the
 * main case's 64 specifications the cost to other US residents is
 *
 *   cost = d0 + (d1 - d0) k + tax (t - 1) + ben (b - 1) - P
 *
 * and every zero line on any plane of two of them is straight. The page draws from these five numbers
 * per specification. The gates check the formula against the engine at off-axis points, the absence of
 * interactions, and the main case.
 */
"use strict";

function build(A) {
  const { cost, mainSpecs, MODELS, gate, near, span, round } = A;
  const M = MODELS.adopted;
  // The main case's service choices, scaled by k. Roads, transport and culture stay at zero, as in the main case.
  const R = (spec, k, production) => ({ schools: k * spec.school, colleges: k, police: k, health: k, other: k,
    delayed: 0, gg: k * spec.gg, production });
  const c = (spec, k, extra = {}, production = true) => cost(spec, R(spec, k, production), M, extra);
  const T = (x) => ({ direct_receipt_response: x });
  const B = (x) => ({ transfer_response: x });

  const specs = [];
  let worst = 0;
  for (const spec of mainSpecs) {
    const d0 = c(spec, 0, {}, false), d1 = c(spec, 1, {}, false);
    const pf = d1 - c(spec, 1);
    const tax = c(spec, 1, T(2)) - c(spec, 1);
    const ben = c(spec, 1, B(2)) - c(spec, 1);
    const f = (k, t, b, P) => d0 + (d1 - d0) * k + tax * (t - 1) + ben * (b - 1) - P;
    // Off-axis points, each moving several quantities at once; the engine must agree with the formula.
    const probes = [[0, 0, 0], [0.37, 1.8, 0.2], [0.8, 0.4, 1.6], [0, 2, 2], [1, 0, 2]];
    for (const [k, t, b] of probes) {
      worst = Math.max(worst, Math.abs(c(spec, k, { ...T(t), ...B(b) }) - f(k, t, b, pf)));
    }
    // Production is a constant: the direct cost minus the full cost is the same at k = 0 and k = 1.
    worst = Math.max(worst, Math.abs((d0 - c(spec, 0)) - pf));
    specs.push({ allocation: spec.allocation, normalization: spec.normalization, share: spec.share, school: spec.school,
      gg: spec.gg, uc: spec.uc, d0, d1, pf, tax, ben, main: f(1, 1, 1, pf) });
  }
  gate("the formula reproduces the engine at off-axis points (no interactions)", worst < 1e-8, `largest gap ${worst.toExponential(1)}`);
  const main = span(specs.map((s) => s.main));
  gate("the formula reproduces the main case", near(main[0], A.MAIN[0], 1e-4) && near(main[1], A.MAIN[1], 1e-4),
    main.map((x) => x.toFixed(4)).join(" to "));
  gate("taxes lower the cost and benefits raise it, in every specification",
    specs.every((s) => s.tax < 0 && s.ben > 0 && s.d1 > s.d0));
  const pfs = span(specs.map((s) => s.pf));
  gate("the main case's gain from their work lies inside the production grid", pfs[0] >= A.PROD_SPAN[0] - 1e-9 && pfs[1] <= A.PROD_SPAN[1] + 1e-9,
    `${pfs.map((x) => x.toFixed(2)).join("–")} in ${A.PROD_SPAN.map((x) => x.toFixed(2)).join("–")}`);

  const r = (x) => round(x, 4);
  return {
    main: main.map((x) => round(x, 2)),
    productionModels: A.PROD_SPAN.map((x) => round(x, 2)),
    specs: specs.map((s) => ({ ...s, d0: r(s.d0), d1: r(s.d1), pf: r(s.pf), tax: r(s.tax), ben: r(s.ben), main: r(s.main),
      share: r(s.share) })),
  };
}

module.exports = { build };
