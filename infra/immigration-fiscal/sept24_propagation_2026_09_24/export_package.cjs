/* The adopted September 24 package, correction by correction, as engine cell edits.
 *
 * package.cjs builds the central case as one list of shifts and main_case.cjs nets them per cell into
 * derived/corrections.json. The debt legacy needs each correction's federal and state-local parts, so
 * this script keeps the component of every shift. It composes the components exactly as
 * packageShifts() does for CENTRAL (gate: the concatenation equals packageShifts() element for
 * element), averages the two fill-in methods, expands each component to the engine's cells, and gates
 * that the components sum to corrections.json cell for cell. Reads only; writes this lane's derived/.
 *
 * Run from anywhere: node export_package.cjs  ->  derived/package_components.json
 */
"use strict";
const fs = require("fs");
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_24", "package.cjs"));
const { METHODS, STACKS, CENTRAL, CONSTANTS, SYN, both, scale, plus, expand, packageShifts, correctionsPayload,
  stackShifts, cboShifts, row3Shifts, otaShifts, row1Shifts, medicalShifts, educationShifts, benefitShifts,
  justiceShifts, constantShifts } = P;

let failures = 0;
function gate(label, ok, detail) {
  console.log(`  ${ok ? "PASS" : "FAIL"} ${label}${detail ? " — " + detail : ""}`);
  if (!ok) failures += 1;
}

// packageShifts(), with each part labelled.
function components(p, caseName, method, o) {
  const edu = o.w === "avg"
    ? ["0.77", "0.82"].flatMap((w) => educationShifts(p, w, o.k).map((s) => ({ ...s, by: scale(s.by, both(0.5)) })))
    : educationShifts(p, o.w, o.k);
  const tax = o.incomeTax === "cbo" ? cboShifts(o.year, p, { scaled: o.scaled })
    : cboShifts(o.year, p, { scaled: o.scaled, incomeTax: false }).concat(row3Shifts(caseName, method));
  const extra = o.benefitsDev ? [{ side: "spending", line: SYN.constants, key: "k", by: o.benefitsDev }] : [];
  return [
    ["tax_stack", stackShifts(p)],
    ["cbo_income_gradients", tax],
    ["treasury_eitc_shares", otaShifts("vs_audit_package_ssn_rule")],
    ["audit_row1_premium_credits", row1Shifts()],
    ["medical_ethnicity_and_ltss", medicalShifts(p, o.medSpec, { mcbs: o.mcbs, ltss: o.ltss })],
    ["education_row6_and_school_price", edu],
    ["benefit_keys", benefitShifts(p, o.benefits)],
    ["justice_row7_and_booking", justiceShifts(o.row7, o.booking)],
    ["lane_constants", constantShifts(o.constants)],
    ["benefit_key_deviation", extra],
  ];
}

const cellId = (e) => [e.side, e.line, e.side === "receipt" ? e.scenario : e.key].join("|");
const cells = new Map();          // component|cell -> edit
for (const meth of METHODS) {
  const p = STACKS[`row4+status_state_aware|central|${meth}`];
  const parts = components(p, "central", meth, CENTRAL);
  const flat = parts.flatMap(([, s]) => s);
  gate(`labelled components equal packageShifts() (${meth})`,
    JSON.stringify(flat) === JSON.stringify(packageShifts(p, "central", meth, CENTRAL)), `${flat.length} shifts`);
  for (const [name, shifts] of parts) {
    for (const e of expand(shifts.map((x) => ({ ...x, by: scale(x.by, both(0.5)) })))) {
      const id = name + "|" + cellId(e);
      if (cells.has(id)) cells.get(id).by = plus(cells.get(id).by, e.by);
      else cells.set(id, { component: name, ...e, by: { ...e.by } });
    }
  }
}
const edits = [...cells.values()];

// Components sum to the payload, cell for cell, and to the file main_case.cjs wrote.
function netOf(list) {
  const net = new Map();
  for (const e of list) {
    const id = cellId(e);
    const cur = net.get(id) || { personal: 0, shared: 0 };
    net.set(id, { personal: cur.personal + e.by.personal, shared: cur.shared + e.by.shared });
  }
  return net;
}
function worstGap(a, b) {
  let worst = 0;
  for (const id of new Set([...a.keys(), ...b.keys()])) {
    const x = a.get(id) || { personal: 0, shared: 0 }, y = b.get(id) || { personal: 0, shared: 0 };
    worst = Math.max(worst, Math.abs(x.personal - y.personal), Math.abs(x.shared - y.shared));
  }
  return worst;
}
const mine = netOf(edits);
const payload = correctionsPayload();
const onDisk = JSON.parse(fs.readFileSync(path.join(__dirname, "..", "main_case_2026_09_24", "derived", "corrections.json"), "utf8"));
const gapPayload = worstGap(mine, netOf(payload.edits)), gapDisk = worstGap(mine, netOf(onDisk.edits));
gate("components sum to correctionsPayload() in every cell", gapPayload < 1e-12, `max |diff| ${gapPayload.toExponential(2)}`);
gate("components sum to derived/corrections.json in every cell", gapDisk < 1e-9, `max |diff| ${gapDisk.toExponential(2)}`);

// The constant line's parts (package.cjs CONSTANTS; shelter is the remainder of constantShifts()).
const total = constantShifts(null)[0].by;
const parts = {};
for (const [id, c] of Object.entries(CONSTANTS)) if (id !== "shelter") parts[id] = both(c.c);
const others = Object.values(parts).reduce(plus, both(0));
parts.shelter = { personal: total.personal - others.personal, shared: total.shared - others.shared };
gate("constant parts: shelter is -0.508 shared (gg 0.59) and -0.550 personal (gg 0.84)",
  Math.abs(parts.shelter.shared + 0.508) < 1e-9 && Math.abs(parts.shelter.personal + 0.5498) < 1e-9,
  `${parts.shelter.shared} / ${parts.shelter.personal}`);

if (failures) { console.error(`${failures} gate(s) failed; nothing written`); process.exit(1); }
const out = path.join(__dirname, "derived", "package_components.json");
fs.mkdirSync(path.dirname(out), { recursive: true });
fs.writeFileSync(out, JSON.stringify({
  meta: { source: "main_case_2026_09_24/package.cjs (CENTRAL, fill-in methods averaged)", methods: METHODS,
    corrections_json_max_abs_diff: gapDisk },
  constants: Object.fromEntries(Object.entries(parts).map(([k, v]) => [k, { label: CONSTANTS[k].label, by: v }])),
  edits,
}, null, 1) + "\n");
console.log(`all gates passed; ${edits.length} component cells -> ${path.relative(process.cwd(), out)}`);
