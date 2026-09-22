"""Pew 2017 Survey of U.S. Muslims: report reproduction plus cuts by nativity and origin.

Raw inputs stay read-only. Every code used is resolved from its codebook value label at
run time (`code()`), never written as a bare number, so a relabelled release fails loud
instead of silently recoding. Standard errors use the 100 jackknife replicate weights
Pew ships (JRR, Appendix B), not a simple-random-sample approximation.
"""
from pathlib import Path
import hashlib
import json

import numpy as np
import pandas as pd
import pyreadstat

LANE = Path(__file__).resolve().parent
REPO = LANE.parent.parent.parent
ZIP = REPO / 'sources/immigration-fiscal/data/external/pew/Pew-2017-US-Muslims.zip'
SAV = LANE / '_cache/2017USMuslimPublicData - checked.sav'
OUT = LANE / 'derived'
ZIP_SHA256 = '1117f84325f3450e12fce58c637e864684b190e33f98e22ad517527aaa5926af'
ZIP_BYTES = 6121578
N_ROWS = 1001
N_REPLICATES = 100
SMALL_CELL = 50

# Pew, "U.S. Muslims Concerned About Their Place in Society", Appendix B: the replicate
# weights are a delete-a-group jackknife with the deleted units' mates doubled (weight
# ratios are exactly {0, 1, 2}). The matching variance estimator sums squared replicate
# deviations with multiplier 1 -- Stata's default for jkrweight() with no multiplier().
JRR_MULTIPLIER = 1.0


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()


def load():
    """Gate G1 (source bytes) and G2 (shape, weights), then return frame + metadata."""
    assert ZIP.stat().st_size == ZIP_BYTES, f'G1 size: {ZIP.stat().st_size}'
    actual = sha256(ZIP)
    assert actual == ZIP_SHA256, f'G1 sha256: {actual}'
    d, meta = pyreadstat.read_sav(SAV, user_missing=True)
    assert len(d) == N_ROWS, f'G2 rows: {len(d)}'
    w = d['weight'].to_numpy(dtype=float)
    assert np.isfinite(w).all() and (w > 0).all(), 'G2 weight not positive and finite'
    reps = [c for c in d.columns if c.startswith('rpl')]
    assert len(reps) == N_REPLICATES, f'replicates: {len(reps)}'
    R = d[reps].div(d['weight'], axis=0).round(6).to_numpy()
    assert set(np.unique(R)) == {0.0, 1.0, 2.0}, f'replicate ratios: {set(np.unique(R))}'
    return d, meta, reps


class Book:
    """Codebook accessor: resolves codes from label text and records what was used."""

    def __init__(self, meta):
        self.meta = meta
        self.used = {}

    def label(self, var):
        return self.meta.column_names_to_labels.get(var, '')

    def values(self, var):
        return {float(k): v for k, v in self.meta.variable_value_labels.get(var, {}).items()}

    def note(self, var):
        if var not in self.used:
            self.used[var] = {'variable': var, 'variable_label': self.label(var),
                              'value_labels': {str(k): v for k, v in sorted(self.values(var).items())}}

    def code(self, var, text):
        """The single code whose value label is exactly `text`. Fails loud otherwise."""
        self.note(var)
        hits = [k for k, v in self.values(var).items() if v == text]
        assert len(hits) == 1, f'{var}: {len(hits)} codes labelled {text!r}'
        return hits[0]

    def codes(self, var, texts):
        return [self.code(var, t) for t in texts]


def estimator(d, reps):
    """Return est(values, base, weight_column) helpers bound to this frame."""
    w = d['weight'].to_numpy(dtype=float)
    W = d[reps].to_numpy(dtype=float)

    def point(y, weights):
        ok = np.isfinite(y)
        tot = weights[ok].sum()
        if not ok.any() or tot <= 0:
            return np.nan
        return float(np.dot(y[ok], weights[ok]) / tot)

    def measure(y):
        """Point estimate, JRR standard error, replicate vector, unweighted base n."""
        theta = point(y, w)
        rep = np.array([point(y, W[:, j]) for j in range(W.shape[1])])
        good = np.isfinite(rep)
        se = float(np.sqrt(JRR_MULTIPLIER * ((rep[good] - theta) ** 2).sum())) if np.isfinite(theta) else np.nan
        return theta, se, rep, int(np.isfinite(y).sum()), int(good.sum())

    def diff_se(rep_a, rep_b, theta_a, theta_b):
        good = np.isfinite(rep_a) & np.isfinite(rep_b)
        dev = (rep_a[good] - rep_b[good]) - (theta_a - theta_b)
        return float(np.sqrt(JRR_MULTIPLIER * (dev ** 2).sum()))

    return measure, diff_se


def indicator(d, book, var, include, base=None):
    """1/0 indicator for `include` labels over the `base` labels; outside base -> NaN."""
    col = d[var].to_numpy(dtype=float)
    inc = np.isin(col, book.codes(var, include))
    base_codes = sorted(book.values(var)) if base is None else book.codes(var, base)
    in_base = np.isin(col, base_codes)
    return np.where(in_base, inc.astype(float), np.nan)


# ---------------------------------------------------------------- variable vocabulary
INCOME_LOW = ['Less than $10,000', '10 to under $20,000', '20 to under $30,000']
INCOME_MID = ['30 to under $40,000', '40 to under $50,000', '50 to under $75,000']
INCOME_UPPER_MID = ['75 to under $100,000']
INCOME_HIGH = ['100 to under $150,000 [OR]', '$150,000 or more']
INCOME_VALID = INCOME_LOW + INCOME_MID + INCOME_UPPER_MID + INCOME_HIGH
EDU_ALL = ['Did not finish high school', 'High school graduate', 'Some college, no degree',
           'Two year associate degree', 'Four year college or university degree',
           'Postgraduate or professional schooling after college']
EDU_BA = ['Four year college or university degree',
          'Postgraduate or professional schooling after college']
CIV_YES = ['Can often be justified', 'Can sometimes be justified']
CIV_NO = ['Can rarely be justified', 'Can never be justified']
AGREE = ['Completely agree', 'Mostly agree']
AGE_18_29 = ['18-19', '20-24', '25-29']
AGE_30_49 = ['30-34', '35-39', '40-44', '45-49']
AGE_50_PLUS = ['50-54', '55-59', '60-64', '65-69', '70 or older']
AGE_ALL = AGE_18_29 + AGE_30_49 + AGE_50_PLUS
REGIONS = ['Americas (excluding U.S.)', 'South Asia', 'Other Asia/Pacific (excluding S. Asia)',
           'Europe', 'MENA (Middle East/North Africa)', 'Sub-Saharan Africa', 'Other/Undetermined']


def outcome_specs(d, book):
    """(id, description, variable, values) for every cut outcome."""
    ind = lambda v, inc, base=None: indicator(d, book, v, inc, base)
    fert_codes = book.codes('fertREC', ['None', 'One', 'Two', 'Three', 'Four or more'])
    fert = d['fertREC'].to_numpy(dtype=float)
    fert_mean = np.where(np.isin(fert, fert_codes), fert, np.nan)  # 'Four or more' counts as 4: a floor
    party = d['party'].to_numpy(dtype=float)
    lean = d['partyln'].to_numpy(dtype=float)
    party_base = np.isin(party, book.codes('party', ['Republican', 'Democrat', 'Independent',
                                                     '(VOL) No preference', '(VOL) Other party']))
    rep_lean = np.isin(party, [book.code('party', 'Republican')]) | np.isin(lean, [book.code('partyln', 'Republican')])
    dem_lean = np.isin(party, [book.code('party', 'Democrat')]) | np.isin(lean, [book.code('partyln', 'Democrat')])
    not_employed = d['employ'].to_numpy(dtype=float) == book.code('employ', 'Not employed')
    looking = np.isin(d['employ1'].to_numpy(dtype=float), [book.code('employ1', 'Yes, looking for work')])
    # CITIZEN is asked of the foreign born only; the U.S. born are citizens by birth and are
    # never asked, so an "all adults" citizenship rate needs them folded in explicitly.
    us_born = d['respondent_birthregion2'].to_numpy(dtype=float) == book.code('respondent_birthregion2', 'U.S. (native born)')
    citizen_all = np.where(us_born, 1.0, indicator(d, book, 'citizen', ['Yes'], ['Yes', 'No']))
    return [
        ('age_18_29', 'Aged 18-29', 'agerec', ind('agerec', AGE_18_29, AGE_ALL)),
        ('age_30_49', 'Aged 30-49', 'agerec', ind('agerec', AGE_30_49, AGE_ALL)),
        ('age_50_plus', 'Aged 50 or older', 'agerec', ind('agerec', AGE_50_PLUS, AGE_ALL)),
        ('female', 'Female', 'sex', ind('sex', ['Female'], ['Male', 'Female'])),
        ('race_black', 'Black, non-Hispanic', 'racethn',
         ind('racethn', ['Black non-Hispanic'], ['White non-Hispanic', 'Black non-Hispanic',
                                                 'Asian non-Hispanic', 'Hispanic', 'Other'])),
        ('income_lt_30k', 'Family income under $30,000', 'income', ind('income', INCOME_LOW, INCOME_VALID)),
        ('income_30_75k', 'Family income $30,000-$75,000', 'income', ind('income', INCOME_MID, INCOME_VALID)),
        ('income_75_100k', 'Family income $75,000-$100,000', 'income', ind('income', INCOME_UPPER_MID, INCOME_VALID)),
        ('income_ge_100k', 'Family income $100,000 or more', 'income', ind('income', INCOME_HIGH, INCOME_VALID)),
        ('income_refused', 'Income not reported (of all respondents)', 'income',
         ind('income', ['(VOL) Don’t know/Refused'] if '(VOL) Don’t know/Refused' in book.values('income').values() else ['(VOL) Don\'t know/Refused'])),
        ('edu_lt_hs', 'Did not finish high school', 'educrec', ind('educrec', ['Did not finish high school'], EDU_ALL)),
        ('edu_hs', 'High school graduate', 'educrec', ind('educrec', ['High school graduate'], EDU_ALL)),
        ('edu_some_college', 'Some college or associate degree', 'educrec',
         ind('educrec', ['Some college, no degree', 'Two year associate degree'], EDU_ALL)),
        ('edu_ba_plus', 'Four-year college degree or more', 'educrec', ind('educrec', EDU_BA, EDU_ALL)),
        ('edu_postgrad', 'Postgraduate or professional schooling', 'educrec',
         ind('educrec', ['Postgraduate or professional schooling after college'], EDU_ALL)),
        ('citizen_yes_of_foreign_born', 'U.S. citizen (item asked of the foreign born only)', 'citizen',
         ind('citizen', ['Yes'], ['Yes', 'No'])),
        ('citizen_or_us_born', 'U.S. citizen, counting the U.S. born as citizens', 'citizen+respondent_birthregion2',
         citizen_all),
        ('party_republican', 'Identifies as Republican', 'party', np.where(party_base, np.isin(party, [book.code('party', 'Republican')]), np.nan)),
        ('party_democrat', 'Identifies as Democrat', 'party', np.where(party_base, np.isin(party, [book.code('party', 'Democrat')]), np.nan)),
        ('party_independent', 'Identifies as independent', 'party', np.where(party_base, np.isin(party, [book.code('party', 'Independent')]), np.nan)),
        ('party_rep_or_lean', 'Republican or leans Republican', 'party+partyln', np.where(party_base, rep_lean, np.nan)),
        ('party_dem_or_lean', 'Democrat or leans Democratic', 'party+partyln', np.where(party_base, dem_lean, np.nan)),
        ('fert_none', 'No children ever born', 'fertREC', ind('fertREC', ['None'], ['None', 'One', 'Two', 'Three', 'Four or more'])),
        ('fert_3plus', 'Three or more children ever born', 'fertREC',
         ind('fertREC', ['Three', 'Four or more'], ['None', 'One', 'Two', 'Three', 'Four or more'])),
        ('fert_mean_floor', 'Mean children ever born (top code 4+ counted as 4: a floor)', 'fertREC', fert_mean),
        ('satisfied_country', 'Satisfied with the way things are going in the country', 'qa2', ind('qa2', ['Satisfied'], ['Satisfied', 'Dissatisfied'])),
        ('homeowner', 'Owns their home', 'qa6', ind('qa6', ['Yes'], ['Yes', 'No'])),
        ('civilians_often_sometimes', 'Killing civilians often or sometimes justified', 'qf3', ind('qf3', CIV_YES)),
        ('civilians_rarely_never', 'Killing civilians rarely or never justified', 'qf3', ind('qf3', CIV_NO)),
        ('civilians_no_answer', 'Killing civilians: no answer given (volunteered DK/refused)', 'qf3',
         ind('qf3', ['(VOL) Don\'t know/refused'])),
        ('homosexuality_accepted', 'Homosexuality should be accepted by society', 'qb2c', ind('qb2c', ['Statement #1'])),
        ('discrim_a_lot', 'A lot of discrimination against Muslims in the U.S.', 'qb7a',
         ind('qb7a', ['Yes, there is a lot of discrimination'], ['Yes, there is a lot of discrimination', 'No, not a lot of discrimination'])),
        ('harder_to_be_muslim', 'Has become more difficult to be a Muslim in the U.S.', 'qc3',
         ind('qc3', ['Has become more difficult to be a Muslim in the U.S.'],
             ['Has become more difficult to be a Muslim in the U.S.', "Hasn't changed very much",
              '(VOL) Has become easier to be a Muslim in the U.S.'])),
        ('exp_suspicion', 'Past year: people acted suspicious of them', 'qd1a',
         ind('qd1a', ['Yes, has happened'], ['Yes, has happened', 'No, has not happened'])),
        ('exp_offensive_names', 'Past year: called offensive names', 'qd1c',
         ind('qd1c', ['Yes, has happened'], ['Yes, has happened', 'No, has not happened'])),
        ('exp_threatened', 'Past year: physically threatened or attacked', 'qd1f',
         ind('qd1f', ['Yes, has happened'], ['Yes, has happened', 'No, has not happened'])),
        ('proud_american', 'Completely or mostly agree: proud to be an American', 'qc17b',
         ind('qc17b', AGREE, AGREE + ['Mostly disagree', 'Completely disagree'])),
        ('belong_muslim_community', 'Completely or mostly agree: strong belonging to U.S. Muslim community', 'qc17d',
         ind('qc17d', AGREE, AGREE + ['Mostly disagree', 'Completely disagree'])),
        ('lot_in_common', 'A lot in common with most Americans', 'qc13',
         ind('qc13', ['A lot in common'], ['A lot in common', 'Some in common', 'Not much in common', 'Nothing at all in common'])),
        ('employed_full_time', 'Employed full time', 'employ', ind('employ', ['Full-time'], ['Full-time', 'Part-time', 'Not employed'])),
        ('employed_part_time', 'Employed part time', 'employ', ind('employ', ['Part-time'], ['Full-time', 'Part-time', 'Not employed'])),
        ('not_employed', 'Not employed', 'employ', ind('employ', ['Not employed'], ['Full-time', 'Part-time', 'Not employed'])),
        ('looking_for_work_of_not_employed', 'Looking for work (base: not employed)', 'employ1',
         np.where(not_employed & np.isin(d['employ1'].to_numpy(dtype=float),
                                         book.codes('employ1', ['Yes, looking for work', 'No, not looking'])), looking, np.nan)),
    ]


def reproduction_specs(d, book):
    """(id, measure, variable, base description, values, published percent)."""
    born = d['respondent_birthregion2'].to_numpy(dtype=float)
    us = book.code('respondent_birthregion2', 'U.S. (native born)')
    dk = book.code('respondent_birthregion2', "Don't know/Refused")
    fb = np.where(np.isin(born, [dk]), np.nan, (born != us).astype(float))
    ba = indicator(d, book, 'educrec', EDU_BA, EDU_ALL)
    return [
        ('B1', 'Foreign born', 'respondent_birthregion2', 'excludes birthplace DK/Refused', fb, 58.0),
        ('B3', 'College graduates', 'educrec', 'excludes education DK/Refused', ba, 31.0),
        ('B4a', 'College graduates, foreign born', 'educrec', 'foreign born; excludes education DK/Refused',
         np.where(fb == 1.0, ba, np.nan), 38.0),
        ('B4b', 'College graduates, U.S. born', 'educrec', 'U.S. born; excludes education DK/Refused',
         np.where(born == us, ba, np.nan), 21.0),
        ('B5a', 'Household income $100,000 or more', 'income', 'excludes income DK/Refused',
         indicator(d, book, 'income', INCOME_HIGH, INCOME_VALID), 24.0),
        ('B5b', 'Household income under $30,000', 'income', 'excludes income DK/Refused',
         indicator(d, book, 'income', INCOME_LOW, INCOME_VALID), 40.0),
        ('B6', 'Own their home', 'qa6', 'excludes DK/Refused', indicator(d, book, 'qa6', ['Yes'], ['Yes', 'No']), 37.0),
        ('B8', 'Killing civilians often or sometimes justified', 'qf3', 'all respondents (DK in denominator)',
         indicator(d, book, 'qf3', CIV_YES), 12.0),
        ('B9', 'Killing civilians rarely or never justified', 'qf3', 'all respondents (DK in denominator)',
         indicator(d, book, 'qf3', CIV_NO), 84.0),
        ('B11', 'Homosexuality should be accepted by society', 'qb2c', 'all respondents (DK in denominator)',
         indicator(d, book, 'qb2c', ['Statement #1']), 52.0),
        ('B8-alt', 'Killing civilians often or sometimes justified', 'qf3', 'sensitivity: DK excluded from denominator',
         indicator(d, book, 'qf3', CIV_YES, CIV_YES + CIV_NO), 12.0),
        ('B9-alt', 'Killing civilians rarely or never justified', 'qf3', 'sensitivity: DK excluded from denominator',
         indicator(d, book, 'qf3', CIV_NO, CIV_YES + CIV_NO), 84.0),
        ('B11-alt', 'Homosexuality should be accepted by society', 'qb2c', 'sensitivity: DK and (VOL) Neither excluded',
         indicator(d, book, 'qb2c', ['Statement #1'], ['Statement #1', 'Statement #2']), 52.0),
    ]


def nativity_groups(d, book):
    born = d['respondent_birthregion2'].to_numpy(dtype=float)
    us = book.code('respondent_birthregion2', 'U.S. (native born)')
    dk = book.code('respondent_birthregion2', "Don't know/Refused")
    return [('All Muslim adults', np.ones(len(d), dtype=bool)),
            ('U.S. born', born == us),
            ('Foreign born', ~np.isin(born, [us, dk]))]


def origin_groups(d, book):
    """Foreign born by own birth region; U.S. born by parents' birth region."""
    born = d['respondent_birthregion2'].to_numpy(dtype=float)
    us = book.code('respondent_birthregion2', 'U.S. (native born)')
    dk = book.code('respondent_birthregion2', "Don't know/Refused")
    groups = [('Foreign born: ' + r, born == book.code('respondent_birthregion2', r)) for r in REGIONS]
    father = d['father_birthregion2'].to_numpy(dtype=float)
    mother = d['mother_birthregion2'].to_numpy(dtype=float)
    f_us = book.code('father_birthregion2', 'U.S. (native born)')
    m_us = book.code('mother_birthregion2', 'U.S. (native born)')
    f_unknown = book.codes('father_birthregion2', ['Undesignated', "Don't know/Refused"])
    m_unknown = book.codes('mother_birthregion2', ['Undesignated', "Don't know/Refused"])
    usb = born == us
    f_foreign = usb & ~np.isin(father, [f_us] + f_unknown)
    m_foreign = usb & ~np.isin(mother, [m_us] + m_unknown)
    any_foreign = f_foreign | m_foreign
    groups.append(('U.S. born: both parents U.S. born', usb & (father == f_us) & (mother == m_us)))
    groups.append(('U.S. born: at least one foreign-born parent', any_foreign))
    for r in REGIONS:
        fc = book.code('father_birthregion2', r)
        mc = book.code('mother_birthregion2', r)
        # Father's region identifies the group; mother's is used when the father is U.S. born
        # or unknown, so each U.S.-born respondent lands in exactly one region.
        primary = (f_foreign & (father == fc)) | (~f_foreign & m_foreign & (mother == mc))
        groups.append(('U.S. born, parent from: ' + r, primary))
    groups.append(('Birthplace not reported', np.isin(born, [dk])))
    return groups


def tabulate(measure, groups, specs, label):
    rows = []
    for gname, mask in groups:
        n_group = int(mask.sum())
        for oid, desc, var, values in specs:
            y = np.where(mask, values, np.nan)
            theta, se, _, n_base, n_rep = measure(y)
            pct = 100 * theta if oid != 'fert_mean_floor' else theta
            sev = 100 * se if oid != 'fert_mean_floor' else se
            rows.append({'cut': label, 'group': gname, 'n_group': n_group, 'outcome_id': oid,
                         'outcome': desc, 'variable': var, 'estimate': round(pct, 2),
                         'jrr_se': round(sev, 2), 'n_base': n_base,
                         'small_cell_flag': 'n<50' if n_base < SMALL_CELL else '',
                         'replicates_used': n_rep})
    return rows


def main():
    OUT.mkdir(exist_ok=True)
    d, meta, reps = load()
    book = Book(meta)
    measure, diff_se = estimator(d, reps)

    # ---- Gate G3: reproduce the published rows.
    rep_rows, misses = [], []
    for rid, name, var, base, values, published in reproduction_specs(d, book):
        theta, se, _, n_base, _ = measure(values)
        srs = float(np.sqrt(theta * (1 - theta) / n_base)) if n_base else np.nan
        diff = 100 * theta - published
        rep_rows.append({'id': rid, 'measure': name, 'variable': var, 'variable_label': book.label(var),
                         'base': base, 'estimate_pct': round(100 * theta, 2), 'jrr_se_pp': round(100 * se, 2),
                         'srs_se_pp': round(100 * srs, 2), 'design_effect': round((se / srs) ** 2, 2),
                         'n_base': n_base, 'published_pct': published, 'diff_pp': round(diff, 2),
                         'within_1pt': abs(diff) <= 1.0})
        if abs(diff) > 1.0 and not rid.endswith('-alt'):
            misses.append((rid, name, base, round(100 * theta, 2), published, round(diff, 2)))
    rep_df = pd.DataFrame(rep_rows)
    rep_df.to_csv(OUT / 'report_reproduction.csv', index=False)

    # ---- Cuts.
    specs = outcome_specs(d, book)
    for var in ['respondent_birthregion2', 'father_birthregion2', 'mother_birthregion2', 'STRATUM']:
        book.note(var)
    nat = nativity_groups(d, book)
    nat_rows = tabulate(measure, nat, specs, 'nativity')
    usb_mask = dict(nat)['U.S. born']
    fb_mask = dict(nat)['Foreign born']
    for oid, desc, var, values in specs:
        ta, sa, ra, na, _ = measure(np.where(fb_mask, values, np.nan))
        tb, sb, rb, nb, _ = measure(np.where(usb_mask, values, np.nan))
        scale = 100 if oid != 'fert_mean_floor' else 1
        se = diff_se(ra, rb, ta, tb)
        nat_rows.append({'cut': 'nativity', 'group': 'Difference: foreign born minus U.S. born',
                         'n_group': int(fb_mask.sum() + usb_mask.sum()), 'outcome_id': oid, 'outcome': desc,
                         'variable': var, 'estimate': round(scale * (ta - tb), 2), 'jrr_se': round(scale * se, 2),
                         'n_base': na + nb, 'small_cell_flag': 'n<50' if min(na, nb) < SMALL_CELL else '',
                         'replicates_used': N_REPLICATES})
    nat_df = pd.DataFrame(nat_rows)
    nat_df.to_csv(OUT / 'cuts_by_nativity.csv', index=False)

    org_groups = origin_groups(d, book)
    org_rows = tabulate(measure, org_groups, specs, 'origin')
    gmap = dict(org_groups)
    # Pre-specified origin contrasts. The second is the generational one: U.S.-born children of
    # immigrants against U.S.-born Muslims whose parents were also born here (largely converts
    # and long-settled families). Both cells are U.S. born, so nativity is held fixed.
    contrasts = [('Foreign born: South Asia', 'Foreign born: MENA (Middle East/North Africa)'),
                 ('U.S. born: at least one foreign-born parent', 'U.S. born: both parents U.S. born'),
                 ('U.S. born, parent from: South Asia', 'Foreign born: South Asia'),
                 ('U.S. born, parent from: MENA (Middle East/North Africa)', 'Foreign born: MENA (Middle East/North Africa)')]
    for a, b in contrasts:
        for oid, desc, var, values in specs:
            ta, _, ra, na, _ = measure(np.where(gmap[a], values, np.nan))
            tb, _, rb, nb, _ = measure(np.where(gmap[b], values, np.nan))
            scale = 100 if oid != 'fert_mean_floor' else 1
            if not (np.isfinite(ta) and np.isfinite(tb)):
                continue
            org_rows.append({'cut': 'origin_contrast', 'group': f'Difference: {a} minus {b}',
                             'n_group': int(gmap[a].sum() + gmap[b].sum()), 'outcome_id': oid,
                             'outcome': desc, 'variable': var, 'estimate': round(scale * (ta - tb), 2),
                             'jrr_se': round(scale * diff_se(ra, rb, ta, tb), 2), 'n_base': na + nb,
                             'small_cell_flag': 'n<50' if min(na, nb) < SMALL_CELL else '',
                             'replicates_used': N_REPLICATES})
    org_df = pd.DataFrame(org_rows)
    org_df.to_csv(OUT / 'cuts_by_origin.csv', index=False)

    # ---- Audit.
    ratios = d[reps].div(d['weight'], axis=0).round(6)
    audit = {
        'lane': 'pew_muslims_2017_2026_09_22',
        'source_zip': str(ZIP.relative_to(REPO)), 'zip_sha256': ZIP_SHA256, 'zip_bytes': ZIP_BYTES,
        'sav_sha256': sha256(SAV), 'n_rows': int(len(d)), 'n_variables': int(len(d.columns)),
        'weight_variable': 'weight', 'weight_label': book.label('weight'),
        'weight_min': float(d.weight.min()), 'weight_max': float(d.weight.max()),
        'weight_sum': float(d.weight.sum()),
        'variance': {
            'method': 'jackknife repeated replication (JRR), 100 replicate weights rpl001-rpl100',
            'multiplier': JRR_MULTIPLIER,
            'source': 'Pew, U.S.-MUSLIMS-FULL-REPORT.pdf, Appendix B: "analyses in this report used a '
                      'repeated replication technique, specifically jackknife repeated replication (JRR), '
                      'to calculate the standard errors... A total of 100 replicates were created."',
            'replicate_weight_ratios': sorted(float(x) for x in np.unique(ratios.to_numpy())),
            'rows_zeroed_per_replicate_mean': float((ratios == 0).sum().mean()),
            'rows_doubled_per_replicate_mean': float((ratios == 2).sum().mean()),
            'rows_ever_zeroed': int((ratios == 0).any(axis=1).sum()),
            'published_average_design_effect': 3.51,
            'published_average_design_effect_source': 'back-solved from the published +/-5.8pp 95% margin '
                                                      'of error at p=0.5 on n=1,001 (Appendix B margins table)',
        },
        'variables_used': [book.used[k] for k in sorted(book.used)],
        'items_searched_and_absent': {
            'public_assistance_or_welfare_receipt': 'No item. Label search for assist/welfare/medicaid/'
                                                    'food stamp/SNAP/benefit/unemploy/insur over all 222 '
                                                    'variable labels returned zero hits.',
        },
        'reproduction_misses_over_1pt': misses,
    }
    (OUT / 'audit.json').write_text(json.dumps(audit, indent=2))

    # ---- Console report (line based).
    print('G1 zip sha256+size: PASS')
    print(f'G2 rows={len(d)} weight_min={d.weight.min():.2f} weight_max={d.weight.max():.2f} '
          f'finite_positive=True replicates={len(reps)}: PASS')
    print('')
    print('REPRODUCTION (published vs microdata, JRR standard errors)')
    for r in rep_rows:
        flag = 'HIT ' if r['within_1pt'] else 'MISS'
        print(f"  {flag} {r['id']:8s} {r['measure'][:46]:46s} est={r['estimate_pct']:6.2f} "
              f"se={r['jrr_se_pp']:5.2f} deff={r['design_effect']:5.2f} n={r['n_base']:4d} "
              f"published={r['published_pct']:5.1f} diff={r['diff_pp']:+5.2f}")
    print(f"G3 misses over 1 point among published rows: {len(misses)}")
    print(f"G4 variables printed with labels in audit.json: {len(book.used)}")
    print('')
    print('NATIVITY: foreign born minus U.S. born, largest gaps first')
    dd = nat_df[nat_df.group.eq('Difference: foreign born minus U.S. born')].copy()
    dd['abs'] = dd.estimate.abs()
    for _, r in dd.sort_values('abs', ascending=False).head(14).iterrows():
        z = r.estimate / r.jrr_se if r.jrr_se else np.nan
        print(f"  {r.outcome[:56]:56s} {r.estimate:+7.2f} +/- {r.jrr_se:5.2f}  z={z:+5.2f}")
    print('')
    print('ORIGIN GROUPS (unweighted n)')
    for g, n in org_df[org_df.cut.eq('origin')].groupby('group', sort=False).n_group.first().items():
        print(f"  {g:52s} n={int(n):4d}{'  [n<50]' if n < SMALL_CELL else ''}")
    print('')
    print('ORIGIN CONTRASTS, gaps over 10 points')
    cc = org_df[org_df.cut.eq('origin_contrast')].copy()
    cc['abs'] = cc.estimate.abs()
    for _, r in cc[cc['abs'] > 10].sort_values(['group', 'abs'], ascending=[True, False]).iterrows():
        z = r.estimate / r.jrr_se if r.jrr_se else np.nan
        print(f"  {r.group[:62]:62s} {r.outcome[:40]:40s} {r.estimate:+7.2f} +/- {r.jrr_se:5.2f} z={z:+5.2f}")
    print('')
    print(f"wrote {OUT/'report_reproduction.csv'}")
    print(f"wrote {OUT/'cuts_by_nativity.csv'}")
    print(f"wrote {OUT/'cuts_by_origin.csv'}")
    print(f"wrote {OUT/'audit.json'}")
    return rep_df, nat_df, org_df


if __name__ == '__main__':
    main()
