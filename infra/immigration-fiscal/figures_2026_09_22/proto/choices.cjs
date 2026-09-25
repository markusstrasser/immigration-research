/* Prototype data: every combination of the account's choices, and which choice sets the sign.
 *
 * The combinations are the matrix's: 9 settings of which public services grow with the group
 * (build_data.cjs ROWS) × 4 settings of general administration × the 1,280 executed tax-incidence,
 * key and household choices (A.outerSpecs) × the 432 models of the gain from their work
 * (A.saneProduction). The gain from their work adds to the rest (build_data.cjs, matrix), so each
 * combination's cost is direct − gain, counted exactly into $5bn bins with 0 as a bin edge; a bin is
 * wholly on one side of zero. Every combination counts once.
 */
"use strict";

const BIN = 5, LO = -100, HI = 360;

function build(A) {
  const { cost, MODELS, gate, near, round, outerSpecs, GG, saneProduction } = A;
  const M = MODELS.adopted;
  const P = saneProduction;

  const GG_COLS = [0, GG[0], GG[1], 1];
  const ROWS = [{ id: "frozen", schools: 0, colleges: 0, delayed: 0, frozen: true }];
  for (const schools of ["cbo", 1]) for (const colleges of [0, 1]) for (const delayed of [0, 1]) {
    ROWS.push({ id: `s${schools}_c${colleges}_d${delayed}`, schools, colleges, delayed });
  }

  // Plain names (the explorer's, ui.js OPTION and KEY).
  const pct = (x) => Math.round(100 * x) + "%";
  const sortedP = [...P].sort((a, b) => a - b);
  const third = [sortedP[Math.floor(P.length / 3)], sortedP[Math.floor((2 * P.length) / 3)]];
  const prodLevel = (p) => (p < third[0] ? "low" : p < third[1] ? "mid" : "high");
  const pr = (lo, hi) => `$${Math.round(lo)}–${Math.round(hi)}bn a year`;
  const inLevel = (id) => sortedP.filter((p) => prodLevel(p) === id);
  const FAMILIES = [
    { id: "services", label: "whether public services grow with the group", of: (c) => (c.row.frozen ? "no" : "yes"),
      levels: [["no", "no: only administration may grow"], ["yes", "yes: schools, police, health, welfare"]] },
    { id: "schools", label: "school budgets for their children", among: "growing", of: (c) => (c.row.frozen ? "none" : String(c.row.schools)),
      levels: [["none", "nothing grows"], ["cbo", "63–66% of the usual cost"], ["1", "the full usual cost"]] },
    { id: "gg", label: "general administration", of: (c) => String(c.gg),
      levels: GG_COLS.map((g) => [String(g), g === 0 ? "held fixed" : g === 1 ? "grows fully" : `grows ${pct(g)}`]) },
    { id: "roads", label: "roads, transport, parks, culture", among: "growing", of: (c) => (c.row.frozen ? "none" : String(c.row.delayed)),
      levels: [["none", "nothing grows"], ["0", "held fixed"], ["1", "grow with the group"]] },
    { id: "colleges", label: "colleges and other education", among: "growing", of: (c) => (c.row.frozen ? "none" : String(c.row.colleges)),
      levels: [["none", "nothing grows"], ["0", "held fixed"], ["1", "grow with the group"]] },
    { id: "production", label: "the gain from their work", production: true,
      levels: ["low", "mid", "high"].map((id) => [id, (id === "low" ? "lowest third: " : id === "mid" ? "middle third: " : "highest third: ")
        + pr(Math.min(...inLevel(id)), Math.max(...inLevel(id)))]) },
    { id: "justice", label: "how police, courts and prisons are charged", of: (c) => c.spec.justice,
      levels: [["population", "per head"], ["adults", "per adult"], ["use", "by use"], ["use_raw_coding", "by use, codes as recorded"]] },
    { id: "allocation", label: "household money", of: (c) => c.spec.allocation,
      levels: [["personal", "each person’s own"], ["shared", "pooled in the household"]] },
    { id: "share", label: "schools’ share of education spending", of: (c) => String(c.spec.share),
      levels: A.SHARES.map((s) => [String(s), pct(s)]) },
    { id: "receipts", label: "who bears each tax", of: (c) => c.spec.receipts,
      levels: [["cbo_collective", "CBO rules"], ["treasury_815", "Treasury: 81.5% on capital"], ["nas_80", "National Academies: 80% on capital"],
        ["corporate_all_capital", "all corporate tax on capital"], ["federal_gap_high_agi", "tax gap on incomes over $500k"],
        ["property_residual_consumption", "business property tax on consumers"], ["public_assets_tax_base", "public asset income like taxes"],
        ["medicare_income_weighted", "Medicare premiums by income"]] },
    { id: "uc", label: "how unpaid hospital care is charged", of: (c) => c.spec.uc,
      levels: [["medicaid", "like Medicaid"], ["uninsured_use_low", "by uninsured use, low end"], ["uninsured_use_high", "by uninsured use, high end"],
        ["uninsured_use_07_low", "at 0.7× uninsured use, low end"], ["uninsured_use_07_high", "at 0.7× uninsured use, high end"]] },
  ];
  for (const f of FAMILIES) if (!f.production) {
    const ids = f.levels.map((l) => l[0]);
    f.index = new Map(ids.map((id, i) => [id, i]));
  }
  const prodFam = FAMILIES.find((f) => f.production);
  prodFam.index = new Map(prodFam.levels.map((l, i) => [l[0], i]));

  // The fiscal combinations, production off.
  const combos = [];
  for (const row of ROWS) {
    const base = row.frozen ? { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0 }
      : { schools: row.schools, colleges: row.colleges, police: 1, health: 1, other: 1, delayed: row.delayed };
    for (const gg of GG_COLS) for (const spec of outerSpecs) {
      combos.push({ row, gg, spec, direct: cost(spec, { ...base, gg, production: false }, M) });
    }
  }
  gate("the combinations are 9 × 4 × 1,280", combos.length === 9 * 4 * 1280, `${combos.length}`);
  for (const f of FAMILIES) if (!f.production) {
    const bad = combos.find((c) => !f.index.has(f.of(c)));
    gate(`${f.id}: every combination has a named level`, !bad, bad ? f.of(bad) : "");
  }

  // Exact counts: every fiscal combination with every production model.
  const NB = (HI - LO) / BIN;
  const fams = FAMILIES.map((f) => ({ f, hist: f.levels.map(() => new Float64Array(NB)), sum: f.levels.map(() => 0),
    min: f.levels.map(() => Infinity), max: f.levels.map(() => -Infinity), n: f.levels.map(() => 0) }));
  const all = new Float64Array(NB);
  const prodIdx = P.map((p) => prodFam.index.get(prodLevel(p)));
  let total = 0, lo = Infinity, hi = -Infinity, frozenNearest = -Infinity, growingNearest = Infinity;
  for (const c of combos) {
    const lv = fams.map((F) => (F.f.production ? -1 : F.f.index.get(F.f.of(c))));
    for (let j = 0; j < P.length; j++) {
      const x = c.direct - P[j];
      const b = Math.floor((x - LO) / BIN);
      if (b < 0 || b >= NB) throw new Error(`combination outside the axis: ${x}`);
      all[b] += 1; total += 1;
      if (x < lo) lo = x;
      if (x > hi) hi = x;
      if (c.row.frozen) { if (x > frozenNearest) frozenNearest = x; } else if (x < growingNearest) growingNearest = x;
      for (let k = 0; k < fams.length; k++) {
        const F = fams[k], i = lv[k] < 0 ? prodIdx[j] : lv[k];
        F.hist[i][b] += 1; F.sum[i] += x; F.n[i] += 1;
        if (x < F.min[i]) F.min[i] = x;
        if (x > F.max[i]) F.max[i] = x;
      }
    }
  }
  gate("every combination counted", total === combos.length * P.length, `${total}`);

  // Gates against the matrix the figures page publishes (figures.json, from build_data.cjs).
  const figures = JSON.parse(A.fs.readFileSync(A.path.join(A.HERE, "src", "generated", "figures.json"), "utf8"));
  const outer = figures.matrix.rows.map((r) => ({ frozen: !!r.frozen, lo: Math.min(...r.cells.map((c) => c.outer[0])), hi: Math.max(...r.cells.map((c) => c.outer[1])) }));
  const fz = outer.find((r) => r.frozen), gr = outer.filter((r) => !r.frozen);
  const frozenLo = fams[0].min[0], grHi = fams[0].max[1];
  gate("services held: the matrix's frozen row reproduces", near(round(frozenLo), fz.lo, 1e-4) && near(round(frozenNearest), fz.hi, 1e-4),
    `${frozenLo.toFixed(1)} to ${frozenNearest.toFixed(1)}`);
  gate("services grow: the matrix's other rows reproduce", near(round(growingNearest), Math.min(...gr.map((r) => r.lo)), 1e-4)
    && near(round(grHi), Math.max(...gr.map((r) => r.hi)), 1e-4), `${growingNearest.toFixed(1)} to ${grHi.toFixed(1)}`);
  gate("no combination lands between the two", frozenNearest < 0 && growingNearest > 0);
  gate("the adopted main case lies inside the growing combinations", A.MAIN[0] >= growingNearest && A.MAIN[1] <= grHi);

  /* The same combinations as a sum. Start from the least costly combination in which services grow,
   * then switch one choice at a time to its most costly option, in order of how far it moves the
   * average; every step is an engine difference, so the steps add to the end exactly. */
  const evalState = (st) => {
    const r = st.frozen ? { schools: 0, colleges: 0, police: 0, health: 0, other: 0, delayed: 0 }
      : { schools: st.schools, colleges: st.colleges, police: 1, health: 1, other: 1, delayed: st.delayed };
    const spec = { allocation: st.allocation, share: st.share, school: st.school, uc: st.uc, justice: st.justice, receipts: st.receipts };
    return cost(spec, { ...r, gg: st.gg, production: false }, M) - st.P;
  };
  const growing = combos.filter((c) => !c.row.frozen);
  const cheapest = growing.reduce((a, c) => (c.direct < a.direct ? c : a));
  const dearest = growing.reduce((a, c) => (c.direct > a.direct ? c : a));
  const pMin = Math.min(...P), pMax = Math.max(...P);
  const s0 = { frozen: false, schools: cheapest.row.schools, colleges: cheapest.row.colleges, delayed: cheapest.row.delayed, gg: cheapest.gg,
    ...cheapest.spec, P: pMax };
  let st = { ...s0 };
  const start = evalState(st);
  gate("the sum starts at the least costly combination where services grow", near(start, growingNearest, 1e-9), start.toFixed(2));
  const labelOf = (fid, id) => FAMILIES.find((f) => f.id === fid).levels.find((l) => l[0] === id)[1];
  const SCHOOL_OPTS = [...A.CBO_SCHOOLS.map((s) => ({ set: { schools: "cbo", school: s }, label: `${pct(s)} of the usual cost` })),
    { set: { schools: 1 }, label: "the full usual cost" }];
  const CHOICES = {
    schools: SCHOOL_OPTS,
    gg: GG_COLS.map((g) => ({ set: { gg: g }, label: labelOf("gg", String(g)) })),
    roads: [0, 1].map((v) => ({ set: { delayed: v }, label: labelOf("roads", String(v)) })),
    colleges: [0, 1].map((v) => ({ set: { colleges: v }, label: labelOf("colleges", String(v)) })),
    production: [pMax, pMin].map((p) => ({ set: { P: p }, label: `$${Math.round(p)}bn a year` })),
    justice: FAMILIES.find((f) => f.id === "justice").levels.map(([id, label]) => ({ set: { justice: id }, label })),
    allocation: FAMILIES.find((f) => f.id === "allocation").levels.map(([id, label]) => ({ set: { allocation: id }, label })),
    share: FAMILIES.find((f) => f.id === "share").levels.map(([id, label]) => ({ set: { share: Number(id) }, label })),
    receipts: FAMILIES.find((f) => f.id === "receipts").levels.map(([id, label]) => ({ set: { receipts: id }, label })),
    uc: FAMILIES.find((f) => f.id === "uc").levels.map(([id, label]) => ({ set: { uc: id }, label })),
  };
  const matches = (o) => Object.entries(o.set).every(([k, v]) => (k === "school" && st.schools !== "cbo") || st[k] === v);
  const order = fams.map((F) => F.f.id).filter((id) => CHOICES[id])
    .sort((a, b) => effectOf(b) - effectOf(a));
  function effectOf(id) {
    const F = fams.find((G) => G.f.id === id), means = F.sum.map((s, i) => s / F.n[i]);
    const ms = F.f.levels.map((l, i) => i).filter((i) => !(F.f.among === "growing" && F.f.levels[i][0] === "none")).map((i) => means[i]);
    return Math.max(...ms) - Math.min(...ms);
  }
  const steps = [];
  let now = start;
  for (const id of order) {
    const from = CHOICES[id].find(matches);
    if (!from) throw new Error(`no option of ${id} matches the current combination`);
    let best = null;
    for (const o of CHOICES[id]) {
      const v = evalState({ ...st, ...o.set });
      if (!best || v > best.v) best = { o, v };
    }
    steps.push({ id, label: fams.find((F) => F.f.id === id).f.label, from: from.label, to: best.o.label, add: round(best.v - now, 2),
      at: [round(now, 2), round(best.v, 2)] });
    st = { ...st, ...best.o.set };
    now = best.v;
  }
  gate("switching every choice to its most costly option reaches the most costly combination", near(now, dearest.direct - pMin, 1e-6),
    `${now.toFixed(2)} vs ${(dearest.direct - pMin).toFixed(2)}`);
  gate("every step adds cost", steps.every((s) => s.add >= 0));
  const freeze = evalState({ ...s0, frozen: true });
  gate("stopping services from growing at the least costly combination crosses zero", freeze < 0, freeze.toFixed(2));
  gate("and lands inside the frozen combinations", freeze >= frozenLo - 1e-9 && freeze <= frozenNearest + 1e-9);
  const waterfall = { start: round(start, 2), end: round(now, 2), steps, freeze: round(freeze, 2) };

  const r4 = (x) => round(x, 6);
  const families = fams.map((F) => {
    const means = F.sum.map((s, i) => s / F.n[i]);
    const counted = F.f.levels.map((l, i) => i).filter((i) => !(F.f.among === "growing" && F.f.levels[i][0] === "none"));
    const ms = counted.map((i) => means[i]);
    const levels = F.f.levels.map(([id, label], i) => ({ id, label, share: r4(F.n[i] / total), mean: round(means[i], 1),
      range: [round(F.min[i], 1), round(F.max[i], 1)], hist: Array.from(F.hist[i], (v) => r4(v / total)) }));
    gate(`${F.f.id}: the levels partition the combinations`, near(levels.reduce((a, l) => a + l.share, 0), 1, 1e-5));
    return { id: F.f.id, label: F.f.label, among: F.f.among || null, effect: round(Math.max(...ms) - Math.min(...ms), 1), levels };
  }).sort((a, b) => b.effect - a.effect);

  return {
    axis: { lo: LO, hi: HI, bin: BIN },
    counts: { total, services: ROWS.length, administration: GG_COLS.length, choices: outerSpecs.length, production: P.length },
    all: { hist: Array.from(all, (v) => r4(v / total)), range: [round(lo, 1), round(hi, 1)] },
    gap: [round(frozenNearest, 1), round(growingNearest, 1)],
    main: A.MAIN.map((x) => round(x, 1)),
    waterfall,
    families,
  };
}

module.exports = { build };
