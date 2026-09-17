"""Point-estimate scenario envelope; deliberately not an uncertainty bound."""
from pathlib import Path
import hashlib
import json
import pandas as pd

HERE = Path(__file__).resolve().parent
source = HERE / 'derived/estimates.csv'
d = pd.read_csv(source)
q = d.loc[(d.metric == 'standardized_gap_per_person') &
          (d.reference == 'third_plus_nh_white')].pivot(
              index='scenario', columns='target', values='estimate')
if len(q) != 13 or q.isna().any().any():
    raise ValueError('Expected complete 13-scenario grid')
q['g2_minus_g1'] = q.mexican_second_gen - q.mexico_born
q['g3_minus_g2'] = q.mexican_third_plus_selfid - q.mexican_second_gen
q['g3_minus_g1'] = q.mexican_third_plus_selfid - q.mexico_born
q['in_expanded_envelope'] = ~q.index.isin(['baseline', 'no_health'])
out = HERE / 'derived/generation_envelope'
out.mkdir(parents=True, exist_ok=True)
q.to_csv(out / 'scenarios.csv')
envelope = q.loc[q.in_expanded_envelope, ['g2_minus_g1', 'g3_minus_g2', 'g3_minus_g1']].agg(['min', 'max'])
envelope.to_csv(out / 'envelope.csv')
(out / 'audit.json').write_text(json.dumps(dict(
    input_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
    script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    scope='11 named expanded-account point estimates; not a confidence or identification bound'), indent=2)+'\n')
print(envelope.to_string())
