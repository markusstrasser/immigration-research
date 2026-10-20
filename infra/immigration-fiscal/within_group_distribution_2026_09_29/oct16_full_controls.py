"""Compare independently evaluated source-item controls at final fixed ends.

Native-First: existing household CSV/Parquet reductions, no fiscal re-evaluation.
"""
import json
from pathlib import Path

import pandas as pd

HERE=Path(__file__).resolve().parent
ITEMS=('none','veterans_compensation','income_security_administration','public_college_response',
       'native_minor_calibration','coverage_tenure','consumption_tax_bases','one_rate','health_residual_key')


def directory(allocation,basis,item=None,cache=False):
    root=HERE/('_cache' if cache else 'derived')/'oct16'/('shared_allocation' if allocation=='shared' else '')
    if item is not None:
        root=root/'controls'/item
    return root/('cash' if basis=='cash' else '')


def main():
    rows=[]
    for allocation in ('personal','shared'):
        for basis in ('set','cash'):
            none=directory(allocation,basis,'none')
            baseline=pd.read_csv(none/'net_positive_shares.csv').query("breakdown=='all' and cell=='all'").set_index(['convention','end'])
            bq=pd.read_csv(none/'household_balance_quantiles.csv').set_index(['convention','end','unit','quantile'])
            bc=pd.read_csv(none/'concentration.csv').set_index(['convention','end','statistic'])
            bh=pd.read_parquet(directory(allocation,basis,'none',True)/'households.parquet').set_index('PH_SEQ')
            for item in ITEMS+('joint',):
                which=None if item=='joint' else item
                source=directory(allocation,basis,which)
                shares=pd.read_csv(source/'net_positive_shares.csv').query("breakdown=='all' and cell=='all'").set_index(['convention','end'])
                quantiles=pd.read_csv(source/'household_balance_quantiles.csv').set_index(['convention','end','unit','quantile'])
                concentration=pd.read_csv(source/'concentration.csv').set_index(['convention','end','statistic'])
                households=pd.read_parquet(directory(allocation,basis,which,True)/'households.parquet').set_index('PH_SEQ').reindex(bh.index)
                if households.calibrated_members.isna().any():
                    raise ValueError('[BLOCKED] full source control changed observed household identities')
                for convention in ('A','B'):
                    for end in ('low','high'):
                        old_positive=bh[f'{convention}_{end}_household_cost_usd']<0
                        new_positive=households[f'{convention}_{end}_household_cost_usd']<0
                        entered=(~old_positive)&new_positive
                        left=old_positive&(~new_positive)
                        current=shares.loc[(convention,end)]
                        previous=baseline.loc[(convention,end)]
                        cq=quantiles.loc[(convention,end,'per_member',.5),'net_cost_usd']
                        pq=bq.loc[(convention,end,'per_member',.5),'net_cost_usd']
                        rows.append(dict(allocation=allocation,basis=basis,item=item,convention=convention,end=end,
                            population_m=current.members_m,share_members_net_positive=current.share_members_net_positive,
                            change_vs_none_pp=100*(current.share_members_net_positive-previous.share_members_net_positive),
                            members_into_contributor=households.loc[entered,'calibrated_members'].sum(),
                            members_out_of_contributor=households.loc[left,'calibrated_members'].sum(),
                            median_per_member_usd=cq,median_change_usd=cq-pq,
                            top10_net_share=concentration.loc[(convention,end,'top10_share_of_total'),'value'],
                            top10_change_pp=100*(concentration.loc[(convention,end,'top10_share_of_total'),'value']-bc.loc[(convention,end,'top10_share_of_total'),'value']),
                            top20_net_share=concentration.loc[(convention,end,'top20_share_of_total'),'value'],
                            top20_change_pp=100*(concentration.loc[(convention,end,'top20_share_of_total'),'value']-bc.loc[(convention,end,'top20_share_of_total'),'value']),
                            source_scope='full source registry: inherited items plus one new item, or all selected jointly; final case fixed specifications; flat pension allocation; each run own selected count/kernel rules'))
    out=HERE/'derived/oct16'
    pd.DataFrame(rows).to_csv(out/'full_source_item_controls.csv',index=False,lineterminator='\n',float_format='%.12g')
    (out/'full_source_item_controls.json').write_text(json.dumps(dict(case='oct16',rows=rows,
        interpretation='Standalone source runs and the final joint run, not additive causal effects. Partial selections follow their declared source price kernels; joint 16/17 is not stacked. Fixed ends are the final case ends, not each standalone run extrema.'),indent=2,allow_nan=False)+'\n')
    print(f'oct16 full-source item controls: {len(rows)} A/B/end/set/allocation rows')


if __name__=='__main__':
    main()
