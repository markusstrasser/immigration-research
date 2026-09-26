/* The main case adopted on 2026-09-26, second decision that day: the September 26 case
 * (../main_case_2026_09_26/package.cjs, imported unchanged) with schools charged at their full average
 * cost per pupil, a school response of 1 (decisions/2026-09-26-main-case-schools-full-cost.md).
 *
 * The account is one year of a population present for decades, so the question is what a school
 * system sized for its pupils costs, not how next year's budget moves. Across 2019 districts spending
 * is proportional to pupils (elasticity 1.004 pupil-weighted) and across states nearly so (0.973);
 * within the same districts over 2000-2019 it rose 0.836% per 1% of pupils, pupil-weighted
 * (research/immigration-service-scaling-test-2026-09-20.md). CBO's 0.63/0.66 are year-to-year
 * growth coefficients; the September 26 case, which reads them over a removal (0.6522/0.6813), stays
 * as the one-year budget scenario.
 *
 * The low side reads the within-district elasticity 0.836 over a removal of the group's pupil share
 * (r = [1 - (1 - s)^b] / s = 0.8489), as the September 26 case reads every other elasticity; the same
 * elasticity taken as the response (r = b) is the other end of that component.
 *
 * The school response enters only through the specifications' school field. The payload's edits (the
 * September 24 corrections, row 8's finite factor, the consumption key) do not depend on it, so
 * corrections.json carries the September 26 edits and a new meta.responses.school.
 */
"use strict";
const path = require("path");
const P = require(path.join(__dirname, "..", "main_case_2026_09_26", "package.cjs"));
const { METHODS, mean2 } = P;

const HERE = __dirname;
const S_PUPIL = P.R.s_pupil;
const finiteR = (b) => (1 - Math.pow(1 - S_PUPIL, b)) / S_PUPIL;
const WITHIN_DISTRICT_B = 0.836; // scaling_test_2026_09_20, within districts 2000/2010/2019, pupil-weighted
const SCHOOL = {
  average: [1, 1],
  within_district: [finiteR(WITHIN_DISTRICT_B), finiteR(WITHIN_DISTRICT_B)],
  within_district_as_response: [WITHIN_DISTRICT_B, WITHIN_DISTRICT_B],
};
const RULES = {
  average: "full average cost per pupil (response 1): a school system sized for the group's pupils",
  within_district: `within-district elasticity ${WITHIN_DISTRICT_B} read over a removal of the pupil share, r = [1 - (1 - s)^b] / s`,
  within_district_as_response: `within-district elasticity ${WITHIN_DISTRICT_B} taken as the response (r = b)`,
};

// o.school_rule: "average" (adopted), "within_district", "within_district_as_response", or "one_year" (the
// September 26 responses, CBO's coefficients read over the removal). Every other option is the
// September 26 package's.
const CENTRAL = Object.assign({}, P.CENTRAL, { school_rule: "average" });
function withSchool(o) {
  const oo = Object.assign({}, CENTRAL, o);
  if (oo.school_rule === "one_year") { const x = Object.assign({}, oo); delete x.school_response; return x; }
  if (!SCHOOL[oo.school_rule]) throw new Error("unknown school rule " + oo.school_rule);
  return Object.assign(oo, { school_response: SCHOOL[oo.school_rule] });
}
function responsesFor(o) {
  const oo = withSchool(o);
  const r = P.responsesFor(oo);
  if (oo.school_rule !== "one_year") r.school = Object.assign({}, r.school, { rule: RULES[oo.school_rule] });
  return r;
}
const specsFor = (o) => P.specsFor(withSchool(o));
const evalPackage = (caseName, method, o) => P.evalPackage(caseName, method, withSchool(o));
const central = (o) => mean2(...METHODS.map((m) => evalPackage("central", m, o)));
const MAIN_SPECS = specsFor({});
const band = (m, profile) => P.bandFor(m, profile, MAIN_SPECS);
const RESPONSES = responsesFor({});

function correctionsPayload(o) {
  const oo = withSchool(o);
  const p = P.correctionsPayload(oo);
  return {
    meta: Object.assign({}, p.meta, {
      source: "main_case_schools_full_2026_09_26/package.cjs", adopted: "2026-09-26",
      decision: "decisions/2026-09-26-main-case-schools-full-cost.md",
      case: `${p.meta.case}; schools at ${oo.school_rule === "average" ? "full average cost" : oo.school_rule}`,
      previous: "main_case_2026_09_26/derived/corrections.json (same edits; schools at 0.6522/0.6813)",
      responses: responsesFor(oo),
    }),
    lines: p.lines, edits: p.edits,
  };
}

module.exports = Object.assign({}, P, {
  HERE, P26: P, S_PUPIL, WITHIN_DISTRICT_B, SCHOOL, RULES, CENTRAL, withSchool, responsesFor, specsFor, evalPackage,
  central, MAIN_SPECS, band, RESPONSES, correctionsPayload,
});
