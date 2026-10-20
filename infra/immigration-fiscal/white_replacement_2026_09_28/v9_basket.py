"""Prepare source item18's food/SNAP vectors, without rebuilding its source lane."""
from pathlib import Path
import hashlib
import importlib.util
import json
import sys
import numpy as np
import pandas as pd

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'consumption_tax_bases_r5_2026_10_15'


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def main():
    spec = importlib.util.spec_from_file_location('comparator_basket_source', SOURCE / 'household.py')
    h = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(h)
    a = h.load_frame()
    c, _ = h.original_consumption(a)
    fshare, _, _, _ = h.ce_food()
    bins = h.saving.rank_bins(h.saving.cps_units(a)['rank'], 50)[a['unit']]
    food = c * fshare[bins]
    snap = np.minimum(np.maximum(a['snap'], 0) / a['size'], food)
    rules = pd.read_csv(SOURCE / 'inputs/grocery_state_2024.csv').set_index('state_fips')
    exemption = rules.exempt_fraction.reindex(a['state_fips']).to_numpy()
    taxable = h.taxable_basket(c, food, snap, exemption, 'joint')
    spec = importlib.util.spec_from_file_location('comparator_state_source', SOURCE / 'assemble.py')
    assemble = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(SOURCE))
    spec.loader.exec_module(assemble)
    state = assemble.load(HERE.parent / 'state_priced_services_2026_09_29/state_price.py', 'basket_state_key')
    taxes = state.read_finance(2024).reindex(sorted(state.STATES)).T09.astype(float)
    taxes /= taxes.sum()
    out = HERE / '_cache/v9_basket.npz'
    out.parent.mkdir(exist_ok=True)
    np.savez(out, consumption=c, taxable=taxable, state=a['state_fips'], ph_seq=a['ph_seq'], pppos=a['pppos'], age=a['age'],
             tax_states=taxes.index.to_numpy(int), tax_shares=taxes.to_numpy())
    paths = [Path(__file__), SOURCE / 'household.py', SOURCE / 'derived/item.json',
             SOURCE / 'inputs/grocery_state_2024.csv', h.CONSUMPTION / '_cache/cps_arrays.npz']
    receipt = {'case': 'oct16', 'rule': 'source household_joint; own scenario weights; fixed state T09 pools',
               'sha256': {str(p.relative_to(HERE.parent)): digest(p) for p in paths},
               'array_sha256': digest(out), 'records': len(c)}
    (HERE / 'derived/v9_basket_inputs.json').write_text(json.dumps(receipt, indent=2) + '\n')
    sys.path.insert(0, str(HERE.parent / 'scripts'))
    from memory_budget import require_within_budget
    require_within_budget('comparator own food/SNAP basket')


if __name__ == '__main__':
    main()
