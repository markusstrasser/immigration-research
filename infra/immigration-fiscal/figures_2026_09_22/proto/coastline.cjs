/* Prototype data: coastline, the assumption plane drawn as a map.
 *
 * x: how much of the usual per-pupil cost school budgets add for the group's children (the main case:
 * 0.63 or 0.66). y: how much every other service grows for them, together: colleges, police, courts and
 * prisons, public health, welfare administration, housing and community. General administration sits
 * at the main-case band unless the page's control sets it to 0 or 1; roads, transport and parks stay
 * fixed unless the page lets them grow; the gain from the group's work is counted; adopted model.
 * Height is the cost to everyone else, $bn a year.
 *
 * For a fixed spec the engine is affine in every response dial, so each main-case spec is one plane:
 *   cost = k + a·x + b·y + g·(general administration) + r·(roads).
 * build() measures k, a, b, g, r from the engine's corners, then gates that the planes predict direct
 * engine evaluations at other points (1e-9), that they reproduce the published anchors, and that the
 * analytic shore lines (each spec's zero-cost line, and the lowest and highest of them) match a
 * brute-force sign scan of the engine on a grid. The page draws every line from these planes with the
 * same envelope rule as envelope() below, and checks itself against the tide lines written here.
 */
"use strict";

// The page's controls: general administration (not growing, the main-case band, growing fully),
// with or without roads, transport and parks growing too.
const GGS = ["zero", "band", "full"];
const CONFIGS = GGS.flatMap((gg) => [false, true].map((roads) => ({ id: gg + (roads ? "_roads" : ""), gg, roads })));
// Contour levels, $bn a year: the land every 50, the sea every 10 (it is shallow).
const LAND = [50, 100, 150, 200, 250, 300, 350];
const SEA = [-10, -20, -30, -40, -50, -60, -70];

/* The upper (max) or lower (min) envelope of lines y = p + q·x on [0, 1], exactly: every vertex sits
 * at a crossing of two lines, and between crossings one line is extreme. Collinear vertices dropped. */
function envelope(lines, upper) {
  const xs = [0, 1];
  for (let i = 0; i < lines.length; i++) {
    for (let j = i + 1; j < lines.length; j++) {
      const dq = lines[i].q - lines[j].q;
      if (Math.abs(dq) < 1e-15) continue;
      const x = (lines[j].p - lines[i].p) / dq;
      if (x > 0 && x < 1) xs.push(x);
    }
  }
  xs.sort((u, v) => u - v);
  const pick = upper ? Math.max : Math.min;
  const pts = xs.map((x) => [x, pick(...lines.map((l) => l.p + l.q * x))]);
  const out = [pts[0]];
  for (let i = 1; i < pts.length - 1; i++) {
    const [x0, y0] = out[out.length - 1];
    const [x1, y1] = pts[i];
    const [x2, y2] = pts[i + 1];
    if (x1 - x0 < 1e-12) continue;
    const s1 = (y1 - y0) / (x1 - x0);
    const s2 = (y2 - y1) / (x2 - x1);
    if (Math.abs(s2 - s1) > 1e-9) out.push(pts[i]);
  }
  out.push(pts[pts.length - 1]);
  return out;
}

// y on a polyline at x (linear between vertices).
function at(poly, x) {
  for (let i = 1; i < poly.length; i++) {
    if (x <= poly[i][0] + 1e-15) {
      const [x0, y0] = poly[i - 1];
      const [x1, y1] = poly[i];
      return x1 === x0 ? y1 : y0 + ((y1 - y0) * (x - x0)) / (x1 - x0);
    }
  }
  return poly[poly.length - 1][1];
}

/* No area of the map is computed or written. Each axis spans its assumption's full range, so the share
 * of the map a region covers is not a likelihood; the page describes the sea by its boundary instead. */

function build(A) {
  const m = A.MODELS.adopted;
  const round = (v, d = 4) => A.round(v, d);
  const span4 = (xs) => A.span(xs).map((v) => round(v));
  const ggDial = (cfg) => (cfg.gg === "band" ? "band" : cfg.gg === "zero" ? 0 : 1);
  const resp = (x, y, cfg) => ({
    schools: x, colleges: y, police: y, health: y, other: y,
    delayed: cfg.roads ? 1 : 0, gg: ggDial(cfg), production: true,
  });
  const direct = (spec, x, y, cfg) => A.cost(spec, resp(x, y, cfg), m);

  /* ------------------------------------------------------------ planes, one per spec ------------ */
  const Z = { gg: "zero", roads: false };
  const planes = A.mainSpecs.map((spec) => {
    const k = direct(spec, 0, 0, Z);
    return {
      spec, k,
      a: direct(spec, 1, 0, Z) - k,
      b: direct(spec, 0, 1, Z) - k,
      g: direct(spec, 0, 0, { gg: "full", roads: false }) - k,
      r: direct(spec, 0, 0, { gg: "zero", roads: true }) - k,
    };
  });
  const ggOf = (pl, cfg) => (cfg.gg === "band" ? pl.spec.gg : cfg.gg === "zero" ? 0 : 1);
  const constant = (pl, cfg) => pl.k + pl.g * ggOf(pl, cfg) + pl.r * (cfg.roads ? 1 : 0);
  const predict = (pl, x, y, cfg) => constant(pl, cfg) + pl.a * x + pl.b * y;

  console.log("  planes");
  A.gate("64 main-case specs", planes.length === 64, `${planes.length}`);
  A.gate("every plane rises with both dials (a, b > 0), so each contour is one line across x",
    planes.every((pl) => pl.a > 0 && pl.b > 0),
    `a ${A.span(planes.map((p) => p.a)).map((v) => v.toFixed(1)).join("–")}, b ${A.span(planes.map((p) => p.b)).map((v) => v.toFixed(1)).join("–")}`);
  {
    // Linearity: the plane through three corners predicts the fourth corner and interior points,
    // for every spec and every setting of the page's controls.
    const pts = [[1, 1], [0.5, 0.5], [0.3, 0.7], [0.9, 0.1], [0.123, 0.456], [0.77, 0.21], [0.05, 0.95]];
    let worst = 0;
    for (const cfg of CONFIGS) {
      for (const pl of planes) {
        for (const [x, y] of [...pts, [pl.spec.school, 1], [pl.spec.school, 0]]) {
          worst = Math.max(worst, Math.abs(predict(pl, x, y, cfg) - direct(pl.spec, x, y, cfg)));
        }
      }
    }
    A.gate("linearity: planes predict the engine at 9 points × 64 specs × 6 control settings (1e-9)", worst < 1e-9,
      `worst ${worst.toExponential(2)}`);
    // On this map the x axis sets the school figure, so specs that differ only in it coincide.
    const key = (s) => JSON.stringify({ ...s, school: null });
    const groups = new Map();
    for (const pl of planes) groups.set(key(pl.spec), [...(groups.get(key(pl.spec)) || []), pl]);
    const dev = Math.max(...[...groups.values()].map((g) => Math.max(...["k", "a", "b", "g", "r"]
      .map((f) => Math.abs(g[0][f] - g[g.length - 1][f])))));
    A.gate("the school setting (63% or 66%) drops out once x sets schools: 32 distinct planes",
      groups.size === 32 && dev < 1e-9, `${groups.size} groups, max difference ${dev.toExponential(1)}`);
  }

  /* ------------------------------------------------------------ anchors --------------------------- */
  console.log("  anchors");
  const BAND = CONFIGS.find((c) => c.id === "band");
  {
    const got = A.span(A.mainSpecs.map((spec) => direct(spec, spec.school, 1, BAND)));
    A.gate("main-case point (x = 0.63 or 0.66, y = 1) = A.MAIN, engine", A.near(got[0], A.MAIN[0], 1e-4) && A.near(got[1], A.MAIN[1], 1e-4),
      `${got[0].toFixed(4)} to ${got[1].toFixed(4)}`);
    const pl = A.span(planes.map((p) => predict(p, p.spec.school, 1, BAND)));
    A.gate("main-case point = A.MAIN, planes", A.near(pl[0], A.MAIN[0], 1e-4) && A.near(pl[1], A.MAIN[1], 1e-4),
      `${pl[0].toFixed(4)} to ${pl[1].toFixed(4)}`);
    const lo = Math.min(...planes.map((p) => predict(p, A.CBO_SCHOOLS[0], 1, BAND)));
    const hi = Math.max(...planes.map((p) => predict(p, A.CBO_SCHOOLS[1], 1, BAND)));
    A.gate("lowest version at (0.63, 1) and highest at (0.66, 1) = A.MAIN ends", A.near(lo, A.MAIN[0], 1e-4) && A.near(hi, A.MAIN[1], 1e-4),
      `${lo.toFixed(4)} / ${hi.toFixed(4)}`);
    const prop = A.span(A.mainSpecs.map((spec) => direct(spec, 1, 1, { gg: "band", roads: true })));
    A.gate("corner (1, 1) with roads growing = A.PROPORTIONAL", A.near(prop[0], A.PROPORTIONAL[0], 1e-4) && A.near(prop[1], A.PROPORTIONAL[1], 1e-4),
      `${prop[0].toFixed(4)} to ${prop[1].toFixed(4)}`);
    // The frozen corner (nothing grows, general administration 0) with unpaid hospital care on the
    // published key is the explorer's "No public services charged" card.
    const frozen = A.span(A.mainSpecs.map((spec) => A.cost(spec, {
      schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0, gg: 0, production: true, uc: false,
    }, m)));
    const card = A.presetCost("no_services");
    A.gate("frozen corner, published hospital-care key = explorer card no_services", A.near(frozen[0], card[0], 1e-6) && A.near(frozen[1], card[1], 1e-6),
      `${frozen[0].toFixed(4)} to ${frozen[1].toFixed(4)}`);
  }

  /* ------------------------------------------------------------ shores ---------------------------- */
  // The level-L line of every spec as y = p + q·x. The lowest version's surface reaches L on the upper
  // envelope of these lines (every version is at least L above it); the highest version's on the
  // lower envelope. At L = 0: high tide (the shore of the most favourable version) and low tide.
  const levelLines = (cfg, L) => planes.map((pl) => ({ p: (L - constant(pl, cfg)) / pl.b, q: -pl.a / pl.b }));
  const highTide = (cfg) => envelope(levelLines(cfg, 0), true);
  const lowTide = (cfg) => envelope(levelLines(cfg, 0), false);

  console.log("  brute-force shore scan (engine at every grid point, every spec)");
  function scan(cfg, nx, ny) {
    const high = highTide(cfg);
    const low = lowTide(cfg);
    const Y = Array.from({ length: ny + 1 }, (_, k) => k / ny);
    let misses = 0, crossings = 0, checked = 0;
    // First grid row at or above zero; null if none. Also fails if the sign changes more than once.
    const firstLand = (vals) => {
      const k = vals.findIndex((v) => v >= 0);
      if (k >= 0 && vals.slice(k).some((v) => v < 0)) misses += 1;
      return k < 0 ? null : k;
    };
    const bracket = (k, yExact) => {
      checked += 1;
      if (k === null) return yExact > 1;
      if (k === 0) return yExact <= 1e-12;
      crossings += 1;
      return yExact > Y[k - 1] - 1e-12 && yExact <= Y[k] + 1e-12;
    };
    for (let j = 0; j <= nx; j++) {
      const x = j / nx;
      const vals = planes.map((pl) => Y.map((y) => direct(pl.spec, x, y, cfg)));
      planes.forEach((pl, s) => {
        const yExact = -(constant(pl, cfg) + pl.a * x) / pl.b;
        if (!bracket(firstLand(vals[s]), yExact)) misses += 1;
      });
      const lowest = Y.map((_, k) => Math.min(...vals.map((v) => v[k])));
      const highest = Y.map((_, k) => Math.max(...vals.map((v) => v[k])));
      if (!bracket(firstLand(lowest), at(high, x))) misses += 1;
      if (!bracket(firstLand(highest), at(low, x))) misses += 1;
    }
    return { misses, crossings, checked, evaluations: (nx + 1) * (ny + 1) * planes.length };
  }
  for (const cfg of CONFIGS) {
    const fine = cfg.id === "band";
    const r = fine ? scan(cfg, 20, 400) : scan(cfg, 10, 200);
    // A scan with no crossing is only a pass where the analytic shore lies off the map entirely.
    const offMap = highTide(cfg).every(([, y]) => y < 0);
    A.gate(`analytic zero lines = engine sign change, ${cfg.id} (${fine ? "21 × 401" : "11 × 201"} grid)`,
      r.misses === 0 && (r.crossings > 0 || offMap),
      `${r.checked} columns checked, ${r.crossings} crossings bracketed, ${r.misses} misses, ${r.evaluations} engine runs` +
      (offMap ? "; no sea on this map, every grid point a cost" : ""));
  }

  /* ------------------------------------------------------------ what the page states -------------- */
  const spanAt = (x, y, cfg) => span4(planes.map((pl) => predict(pl, x, y, cfg)));
  const configs = CONFIGS.map((cfg) => {
    const c = planes.map((pl) => constant(pl, cfg));
    const yAxis = planes.map((pl, s) => -c[s] / pl.b); // shore at x = 0
    const xAxis = planes.map((pl, s) => -c[s] / pl.a); // shore at y = 0
    const diag = planes.map((pl, s) => -c[s] / (pl.a + pl.b)); // shore on x = y
    const high = highTide(cfg);
    const low = lowTide(cfg);
    // The largest x + y on the shore inside the square: every point below the shore has the two shares
    // adding up to less than this. A linear function peaks on a polyline at a vertex or where the line
    // leaves the square (y = 0 or y = 1), so those points are enough.
    const sumMax = (poly) => {
      const inside = poly.filter(([, y]) => y >= 0 && y <= 1);
      const cross = [];
      for (let i = 1; i < poly.length; i++) {
        const [x0, y0] = poly[i - 1];
        const [x1, y1] = poly[i];
        for (const edge of [0, 1]) {
          if ((y0 - edge) * (y1 - edge) < 0) cross.push([x0 + ((x1 - x0) * (y0 - edge)) / (y0 - y1), edge]);
        }
      }
      const pts = [...inside, ...cross];
      return pts.length ? Math.max(...pts.map(([x, y]) => x + y)) : null;
    };
    const tide = (pick, poly) => ({
      y0: round(pick(...yAxis)), x0: round(pick(...xAxis)), diag: round(pick(...diag)),
      sum: sumMax(poly) === null ? null : round(sumMax(poly)),
      poly: poly.map(([x, y]) => [A.round(x, 9), A.round(y, 9)]),
    });
    return {
      id: cfg.id, gg: cfg.gg, roads: cfg.roads,
      corners: { "00": spanAt(0, 0, cfg), "10": spanAt(1, 0, cfg), "01": spanAt(0, 1, cfg), "11": spanAt(1, 1, cfg) },
      main: span4(planes.map((pl) => predict(pl, pl.spec.school, 1, cfg))),
      schoolsOnly: span4(planes.map((pl) => predict(pl, pl.spec.school, 0, cfg))),
      high: tide(Math.max, high),
      low: tide(Math.min, low),
    };
  });
  console.log("  shores");
  for (const c of configs) {
    const sum = (t) => (t.sum === null ? "off map" : t.sum.toFixed(3));
    console.log(`    ${c.id.padEnd(11)} high tide: x ${c.high.x0.toFixed(3)} y ${c.high.y0.toFixed(3)} diag ${c.high.diag.toFixed(3)} ` +
      `x+y < ${sum(c.high)}   low tide: x ${c.low.x0.toFixed(3)} y ${c.low.y0.toFixed(3)} x+y < ${sum(c.low)}   ` +
      `main ${c.main.map((v) => v.toFixed(1)).join("–")}   (0,0) ${c.corners["00"].map((v) => v.toFixed(1)).join(" to ")}`);
  }
  {
    const b = configs.find((c) => c.id === "band");
    A.gate("default map: (0, 0) is a gain in every version, the main case a cost in every version",
      b.corners["00"][1] < 0 && b.main[0] > 0, `(0,0) ${b.corners["00"].join(" to ")}, main ${b.main.join("–")}`);
    A.gate("default map: the shore never reaches the main-case row (y = 1) inside the square",
      b.high.poly.every(([, y]) => y < 1), `high tide at x = 0: y ${b.high.y0}`);
    // Low tide never rises above high tide: checked at every vertex of either line, which is enough for
    // two polylines.
    const worst = Math.max(...configs.map((c) => Math.max(...[...c.high.poly, ...c.low.poly]
      .map(([x]) => at(c.low.poly, x) - at(c.high.poly, x)))));
    A.gate("low tide at or below high tide everywhere, every setting", worst <= 1e-8, `largest low − high ${worst.toExponential(2)}`);
  }

  // The version most favourable to the group at the main case, and whether it is lowest everywhere:
  // a plane below every other at the four corners is below it on the whole square.
  const lowest = planes.reduce((best, pl) => (predict(pl, pl.spec.school, 1, BAND) < predict(best, best.spec.school, 1, BAND) ? pl : best));
  const lowestEverywhere = [[0, 0], [1, 0], [0, 1], [1, 1]].every(([x, y]) =>
    planes.every((pl) => predict(lowest, x, y, BAND) <= predict(pl, x, y, BAND) + 1e-9));
  console.log(`  lowest version at the main case: ${JSON.stringify(lowest.spec)}; lowest on the whole map: ${lowestEverywhere}`);

  // The page draws from the 32 distinct planes (the school setting drops out on this map, gated above).
  const distinct = planes.filter((pl) => pl.spec.school === A.CBO_SCHOOLS[0]);
  A.gate("distinct planes written: 32, one per non-school spec", distinct.length === 32, `${distinct.length}`);
  return {
    levels: { land: LAND, sea: SEA },
    planes: distinct.map((pl) => ({
      k: A.round(pl.k, 9), a: A.round(pl.a, 9), b: A.round(pl.b, 9), g: A.round(pl.g, 9), r: A.round(pl.r, 9),
      gg: pl.spec.gg,
    })),
    configs,
    lowest: {
      spec: { ...lowest.spec, share: round(lowest.spec.share) },
      everywhere: lowestEverywhere,
    },
    anchors: {
      main: A.MAIN.map((v) => round(v)),
      proportional: A.PROPORTIONAL.map((v) => round(v)),
      gg: A.GG.map((v) => round(v, 2)),
      schools: A.CBO_SCHOOLS,
      noServices: A.presetCost("no_services").map((v) => round(v)),
      // Who the group is, as the model defines it.
      group: { target: A.model.meta.target, millions: round(A.model.meta.target_population / 1e6, 1) },
    },
  };
}

module.exports = { build, envelope };
