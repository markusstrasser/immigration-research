"""Own-key item and gap changes at v9 counts; Mexican16/17 stay origin-specific."""
from pathlib import Path
import csv
import json
import rekey_sept29 as W


def main():
    W.use_case('oct16')
    W.setup()
    scenarios=W.scenarios()
    summary=json.loads((W.CASE_LANE/'derived/summary.json').read_text())['v9']
    old=json.loads((W.FISCAL/'main_case_2026_10_15/derived/summary.json').read_text())['v8']
    ids={13:'veterans_compensation',14:'income_security_administration',15:'public_college_response',
         16:'native_minor_calibration',17:'coverage_tenure',18:'consumption_tax_bases',20:'one_rate'}
    extra=[k for k in summary['change_by_item'] if k not in ids.values()]
    if len(extra)>1:
        raise SystemExit('[BLOCKED] item change export has unclassified new registry entries')
    if extra:
        ids[21]=extra[0]
    rows=[]
    for name in ('A1_third_plus_nh_white','nh_black_rough'):
        for basis,key in (('accrual','set'),('cash','cash')):
            for index,end in enumerate(W.ENDS):
                result=W.run29(scenarios[name],end,basis)[0]
                own=result['v9_items']
                typed=result['v9_service_parts']
                if any(abs(sum(p['delta_bn'] for p in typed if p['item']==i)-v)>1e-9 for i,v in own.items()):
                    raise SystemExit('[BLOCKED] own item and typed-part changes do not close')
                if abs(result['cost']-result['v9_before_cost_bn']-sum(own.values()))>1e-9:
                    raise SystemExit('[BLOCKED] own before/after item closure')
                current=summary['band_bn' if key=='set' else 'cash_set_bn'][index]
                prior=old['band_bn' if key=='set' else 'cash_set_bn'][index]
                changes={str(n):summary['change_by_item'][id][key][index] for n,id in ids.items()}
                changes.setdefault('21',0.)
                changes['interactions']=current-prior-sum(changes.values())
                for item,mexican in changes.items():
                    group_change=own.get(item,0.)
                    rows.append(dict(case='oct16',group=name,basis=basis,end=end,item=item,
                        mexican_change_bn=mexican,own_change_bn=group_change,gap_change_bn=mexican-group_change,
                        own_before_bn=result['v9_before_cost_bn'],own_after_bn=result['cost'],
                        comparator_population=result['population'],lineage_population=W.META['population_v9']['with_coverage'],
                        scope='fixed current comparator counts/keys; Mexican source-alone items plus exact remaining joint interaction; own20 includes15x20; excludes item11/mortality/count-standardization changes'))
    fields=list(rows[0])
    for lane,selected in ((W.LANE,rows),(W.BLACK_LANE,[r for r in rows if r['group']=='nh_black_rough'])):
        with (lane/'derived/v9_item_changes_oct16.csv').open('w',newline='') as stream:
            writer=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n')
            writer.writeheader();writer.writerows(selected)
    W.stop_if_failed()


if __name__=='__main__':
    main()
