"""Restate H1--H10 from the household consumer's own oct16 point outputs.

Native-First: join the consumer's CSVs; do not transport old numerical claims.
"""
import json
from pathlib import Path

import pandas as pd

HERE=Path(__file__).resolve().parent
OUT=HERE/'derived/oct16'


def table(name,allocation='personal',basis='set',suffix=''):
    directory=OUT/('shared_allocation' if allocation=='shared' else '')/('cash' if basis=='cash' else '')
    return pd.read_csv(directory/(name+suffix+'.csv'))


def all_shares(allocation,basis,suffix=''):
    return table('net_positive_shares',allocation,basis,suffix).query("breakdown=='all' and cell=='all'").set_index(['convention','end'])


def main():
    rows=[]
    for suffix,arm in (('','flat'),('_person_accrual','person'),('_person_onbooks','person_onbooks')):
        for allocation in ('personal','shared'):
            set_rows=all_shares(allocation,'set',suffix)
            cash_rows=all_shares(allocation,'cash',suffix)
            for convention in ('A','B'):
                for end in ('low','high'):
                    a,b=set_rows.loc[(convention,end)],cash_rows.loc[(convention,end)]
                    rows.append(dict(id='H3',arm=arm,allocation=allocation,convention=convention,end=end,
                        quantity='cash_minus_set_contributor_pp',value=100*(b.share_members_net_positive-a.share_members_net_positive),
                        source='net_positive_shares'+suffix+'.csv: share_members_net_positive; each basis own located count and prices'))
                    for basis,r in (('set',a),('cash',b)):
                        rows.append(dict(id='H4',arm=arm,allocation=allocation,basis=basis,convention=convention,end=end,
                            quantity='household_minus_member_contributor_pp',value=100*(r.share_households_net_positive-r.share_members_net_positive),
                            source='net_positive_shares'+suffix+'.csv: separate household and member weighting; member-only balances'))
            for basis in ('set','cash'):
                bounds=table('lineage_share_bounds',allocation,basis,suffix)
                for r in bounds.query("convention in ['A','B']").to_dict('records'):
                    rows.append(dict(id='H2',arm=arm,allocation=allocation,basis=basis,**r,
                        source='lineage_share_bounds'+suffix+'.csv: unlocated coverage has no contributor classification'))
                f=all_shares(allocation,basis,suffix)
                for end in ('low','high'):
                    rows.append(dict(id='H9',arm=arm,allocation=allocation,basis=basis,end=end,
                        quantity='school_per_head_minus_pupil_key_contributor_pp',
                        value=100*(f.loc[('A_schools_per_head',end),'share_members_net_positive']-f.loc[('A',end),'share_members_net_positive']),
                        source='net_positive_shares'+suffix+'.csv: A_schools_per_head minus A; dollars conserved'))
        for basis in ('set','cash'):
            personal,shared=all_shares('personal',basis,suffix),all_shares('shared',basis,suffix)
            for end in ('low','high'):
                rows.append(dict(id='H5',arm=arm,basis=basis,end=end,quantity='shared_minus_personal_contributor_pp',
                    value=100*(shared.loc[('A',end),'share_members_net_positive']-personal.loc[('A',end),'share_members_net_positive']),
                    source='personal/shared net_positive_shares'+suffix+'.csv; shared also excludes item11'))
    for allocation in ('personal','shared'):
        for basis in ('set','cash'):
            flat,central=all_shares(allocation,basis),all_shares(allocation,basis,'_person_onbooks')
            for end in ('low','high'):
                rows.append(dict(id='H8',allocation=allocation,basis=basis,end=end,quantity='person_onbooks_minus_flat_contributor_pp',
                    value=100*(central.loc[('A',end),'share_members_net_positive']-flat.loc[('A',end),'share_members_net_positive']),
                    source='net_positive_shares_person_onbooks.csv minus net_positive_shares.csv; named allocation arms'))
    unresolved=[dict(id='H1',status='unmeasured observed mixed-survivor unit attribution',
        scope='item11 remains its declared generation amount distributed per member; changing its household placement may change crossings; removal or redistribution is not bounded by exclusion'),
        dict(id='H6',status='unidentified selected nonreporter household placement',
        scope='original latent descendants use age-band donor placement; uniform placement is a conditional sensitivity, neither identifies 2024 selection'),
        dict(id='H7',status='retained explicit P7 deferral',scope='six original sampled minors whose linked-parent classification changes retain frozen P7 source treatment; oct16 does not reopen that source decision'),
        dict(id='H10',status='first-order credit and service ownership remains unmeasured',
        scope='conserved source-key allocation does not establish actual dependent-owner credit incidence or the full fiscal balance of mixed families')]
    result=dict(case='oct16',quantities=rows,unresolved=unresolved,
        interpretation='Modeled member-only fiscal allocations. Net contributors are allocated net payers, not persons financially better off. Every numerical claim names basis, allocation, weighting and located/unlocated population.',
        source_rule='Each quantity is recomputed from this lane own oct16 CSV; no v8 numerical claim transported.')
    (OUT/'companion_claims.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    pd.DataFrame(rows).to_csv(OUT/'companion_claims.csv',index=False,lineterminator='\n',float_format='%.12g')
    print(f'oct16 H1--H10: {len(rows)} numeric restatements; 4 explicit unresolved/source records')


if __name__=='__main__':
    main()
