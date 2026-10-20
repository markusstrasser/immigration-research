"""Source-line-only military history beside the blocked complete debt stock.

Native-First: filter the executed programme back-cast's typed source histories;
do not invent a VA direct-consumption series or compound an aggregate delta.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import pandas as pd

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent
sys.path.insert(0,str(FISCAL/'scripts'))
from memory_budget import require_within_budget
BENEFITS={'veterans_pension_disability','veterans_life_insurance','military_medical',
          'veterans_readjustment','veterans_other'}


def select_history(meta, annual, located):
    concepts={f'net_cost_cbo_informed_oct16_{end}':end for end in ('low','high')}
    annual=annual[annual.concept.isin(concepts) & annual.part.isin(located)].copy()
    annual['end']=annual.concept.map(concepts)
    principal=annual[annual.year.eq(2024)]
    expected={(end,rule,part) for end in ('low','high')
              for rule in ('flat','ratio','income') for part in located}
    actual=set(zip(principal.end,principal.rule,principal.part))
    if actual!=expected or principal.duplicated(['end','rule','part']).any():
        raise ValueError('[BLOCKED] military history lacks unique2024 source parts at both named case ends')
    ends=meta['concepts']['net_cost_cbo_informed']['ends']
    for row in principal.itertuples():
        # The upstream annual export is deliberately rounded to six decimals.
        if abs(row.value_bn-ends[row.end]['additions_bn'][row.part])>1e-6:
            raise ValueError('[BLOCKED] military history2024 source-part anchor changed')
    annual['source_line']=annual.part.map(lambda k:located[k].get('source_line',located[k].get('line')))
    annual['federal_share']=1.
    annual['scope']='conditional source-line programme transport; not observed Treasury borrowing'
    return annual


def main():
    back=FISCAL/'historical_backcast_2026_09_20/derived'
    for required in (back/'case_components_oct16.json',back/'oct16/case_parts_annual_manifest.json'):
        if not required.is_file():
            raise ValueError('[BLOCKED] military source history prerequisite missing: '+str(required)+
                             '; finish the oct16 historical back-cast before this export')
    meta=json.loads((back/'case_components_oct16.json').read_text())
    parts=meta['concepts']['net_cost_cbo_informed']['v6_parts']
    located={k:v for k,v in parts.items() if 'veterans_compensation' in k
             and v.get('source_line',v.get('line')) in BENEFITS}
    if not located:
        raise ValueError('[BLOCKED] executed military benefit source histories not located')
    contract_path=back.parent/'cache_contract.py'
    spec=importlib.util.spec_from_file_location('oct16_backcast_cache_contract',contract_path)
    contract=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(contract)
    annual_path=contract.verify_cached_annual(back.parent)
    annual=pd.read_csv(annual_path)
    annual=select_history(meta,annual,located)
    pins={str(p.relative_to(FISCAL)):hashlib.sha256(p.read_bytes()).hexdigest()
          for p in (back/'case_components_oct16.json',back/'oct16/case_parts_annual_manifest.json',annual_path)}
    out=HERE/'derived/oct16'
    require_within_budget('oct16 military source history')
    annual.to_csv(out/'military_source_history.csv',index=False,lineterminator='\n')
    (out/'military_history_contract.json').write_text(json.dumps(dict(case='oct16',
      status='partial military source-line history; full historical financing blocked',
      included_source_lines=sorted(BENEFITS),rows=len(annual),
      national_histories='BEA3.12 source benefit lines; backcast own population and income rules retained',
      conditional_fraction='current compensation share carried on combined pension/disability series; not measured historical compensation composition',
      principal_source_tolerance_bn=1e-6,accounting_set='set; source13 military benefit response changes are current federal flows',
      omitted={'health_services':'no staged military-only VA direct-consumption history; broad federal health series is not a substitute'},
      complete_debt_stock=None,complete_debt_interest=None,
      source_parts=located,source_sha256=pins),indent=2)+'\n')
    print('PASS source-line military historical rows',len(annual),'full VA/direct-consumption and complete debt stock withheld')


if __name__=='__main__':
    main()
