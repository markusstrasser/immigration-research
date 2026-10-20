"""Pin all final oct16 inputs explicitly; missing evidence stops without repinning."""
from __future__ import annotations

import argparse
import json
import sys

import tables_oct16 as tables

sys.path.insert(0, str(tables.F / 'scripts'))
from adoption_gate import require_adopted


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--scope', choices=('tables', 'engine'), default='tables')
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    adoption = require_adopted('oct16')
    payload = json.loads((tables.CASE / 'corrections.json').read_text())
    tables.require_adopted_payload(payload)
    if args.scope == 'engine':
        tables.INPUTS = [*tables.INPUTS[:14], *[tables.F / 'generation_account_2026_09_24/derived' / name
                        for name in ('generation_corrections_oct16.json', 'generation_corrections_oct16_cash.json',
                                     'generation_results_oct16.csv', 'generation_results_oct16_cash.csv')],
                        # The engine's service break-even imports the case's sign-reversal rule and checks its file.
                        tables.CASE.parent / 'sign_reversal.cjs', tables.CASE / 'sign_reversal.csv',
                        tables.HERE / 'engine_breaks_sept29.cjs', tables.HERE / 'first_year_v9.cjs',
                         tables.HERE / 'generation_preflight.cjs',
                         tables.HERE / 'reproduce_generation_source.cjs',
                         tables.D / 'generation_source_contract_oct16.json', tables.F / 'live_case.json']
        tables.PINS = tables.HERE / 'engine_oct16_pins.json'
    snapshot = tables.snapshot()
    record = {'case': 'oct16', 'scope': args.scope, 'adoption': adoption, 'inputs': snapshot}
    if args.check:
        if not tables.PINS.exists() or json.loads(tables.PINS.read_text()) != record:
            tables.blocked(f'{args.scope} final evidence pins absent or stale')
        print(f'[PASS] {len(snapshot)} final oct16 {args.scope} evidence pins unchanged')
    else:
        # One line per pinned input: indent=2 put every cell on its own lines (40.7 MB for tables on oct16).
        head = json.dumps({k: v for k, v in record.items() if k != 'inputs'}, indent=2)[:-2]
        body = ',\n'.join(f'    {json.dumps(name)}: {json.dumps(pin, separators=(",", ":"))}' for name, pin in snapshot.items())
        text = f'{head},\n  "inputs": {{\n{body}\n  }}\n}}\n'
        if json.loads(text) != record:
            tables.blocked('pin serialization does not round-trip')
        tables.PINS.write_text(text)
        print(f'[PASS] rederived {len(snapshot)} final oct16 {args.scope} evidence pins')


if __name__ == '__main__':
    main()
