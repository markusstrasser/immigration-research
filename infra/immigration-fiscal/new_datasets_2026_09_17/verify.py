"""Source-integrity, published-benchmark, and non-linkage checks for this intake."""
import hashlib
import json
from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parent
manifest = json.loads((ROOT / 'manifest.json').read_text())['files']
assert len(manifest) == 13
assert len({r['sha256'] for r in manifest}) == 12
assert sum(r['exact_duplicate_of'] is not None for r in manifest) == 1
for item in manifest:
    staged = ROOT / item['staged']
    assert staged.stat().st_size == item['bytes']
    assert hashlib.sha256(staged.read_bytes()).hexdigest() == item['sha256']
    assert hashlib.sha256(Path(item['input']).read_bytes()).hexdigest() == item['sha256']
    if Path(item['input']).name.startswith('ICPSR_'):
        assert not any('-Data.' in m['name'] for m in item['members'])
pew = ROOT / 'derived/pew'
dictionary = json.loads((pew / 'survey_dictionary.json').read_text())
assert len(dictionary) == 8 and sum(x['n'] for x in dictionary.values()) == 14517
results = pd.read_csv(pew / 'results.csv')
assert not results.duplicated(['source', 'group', 'outcome']).any()
assert results.weighted_pct.between(0, 100).all()
assert (results.n_valid + results.n_missing == results.n_total).all()
dist = pd.read_csv(pew / 'distributions.csv')
never = dist.loc[(dist.variable == 'q22') & dist.value.eq(2), 'weighted_pct_all'].item()
assert round(never) == 81, 'Pew published never-identified benchmark failed'
counts = results.query("source == 'pooled_counts' and outcome == 'identified'").set_index('group')
assert counts.loc[['gen1', 'gen2', 'gen3', 'gen4'], 'weighted_pct'].round().tolist() == [97, 92, 77, 50]
freq = pd.read_csv(ROOT / 'derived/icpsr/codebook_frequency_checks.csv')
totals = freq.groupby(['study', 'variable']).n_unweighted.sum()
assert totals.loc[30302].eq(3415).all() and totals.loc[20862].eq(8634).all()
b = pd.read_csv(ROOT / 'derived/other_audit/cils_missing_record_bounds.csv')
assert (b.completion_lower_pct <= b.observed_pct).all()
assert (b.observed_pct <= b.completion_upper_pct).all()
print('PASS: 13 originals/copies, duplicate classification, docs-only ICPSR, eight Pew schemas, published 81 and 97/92/77/50 benchmarks, denominators and missing-record bounds')
