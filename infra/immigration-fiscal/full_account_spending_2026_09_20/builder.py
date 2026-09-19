"""Exhaustive CY2024 current-spending allocation and declared proxy sensitivity.

Native-First: BEA workbook cells and existing survey parsers/operating-school
outputs; no residual inferred from the desired sign and no core ledger edits.
"""
from pathlib import Path
import argparse
import hashlib
import json
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
BEA_SHA = '69b5c7aefb38675324887ce31d6feb4fcde7c903ab952db7328da0813096615e'
CPS_SHA = '318845a2b5e0034eb2973898de1738f4df0025727de38499e7669cb9c0deef0b'
BEA_URL = 'https://apps.bea.gov/national/Release/XLS/Survey/Section3All_xls.xlsx'
TARGET = 'mexican_observed_total'
TOTAL_BN = 10061.458
AMOUNTS = ['target_bn','other_household_bn','outside_household_bn','external_bn','unallocated_bn']


def sha(path):
    with Path(path).open('rb') as f:
        return hashlib.file_digest(f, 'sha256').hexdigest()


def verify_primary_pins(paths,pins):
    actual={Path(p).name:Path(p) for p in paths}
    for item in pins['sources']:
        path=actual.get(item['name'])
        if path is None or sha(path)!=item['sha256']:
            raise ValueError(f'Pinned primary source absent or changed: {item["name"]}')


def verified_school_dependencies(school):
    manifest_path=school.parent/'manifest.json'
    manifest=json.loads(manifest_path.read_text())
    if not manifest.get('inputs'):
        raise ValueError('School manifest has no upstream inputs')
    paths=[manifest_path]
    for item in manifest['inputs']:
        path=Path(item['path'])
        if sha(path)!=item['sha256']:
            raise ValueError(f'Stale school upstream input: {path}')
        paths.append(path)
    return paths


def read_bea(path):
    if sha(path) != BEA_SHA:
        raise ValueError('Unreviewed BEA vintage')
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    tables, metadata = {}, {}
    for sheet in ['T30100-A','T31200-A','T31300-A','T31700-A']:
        rows = list(book[sheet].values)
        headers = [r for r in rows if r[0] == 'Line']
        if len(headers) != 1 or rows[1][0] != '[Millions of dollars]':
            raise ValueError('BEA units or header changed')
        indexes = [i for i, x in enumerate(headers[0]) if str(x) == '2024']
        if len(indexes) != 1:
            raise ValueError('Ambiguous or absent year')
        j = indexes[0]
        tables[sheet] = {int(r[0]):dict(label=r[1].strip(), series=r[2], million=r[j])
                         for r in rows if str(r[0]).isdigit()}
        metadata[sheet] = [str(r[0]) for r in rows if r[0] and not str(r[0]).isdigit() and r[0] != 'Line']
    book.close()
    if tables['T30100-A'][20]['million'] != 10061458:
        raise ValueError('Current expenditure anchor changed')
    return tables, metadata


def partition(tables):
    """Each category owns disjoint economic-account cells; rounding is explicit."""
    rows = []
    def add(category, refs, family, key, alternatives, coverage=False, fixed=False, external=False):
        cells = [tables[s][n] for s,n in refs]
        if not all(isinstance(c['million'], (int,float)) for c in cells):
            raise ValueError(f'Unusable BEA cell: {category}')
        rows.append(dict(category=category, family=family, official_bn=sum(c['million'] for c in cells)/1000,
                         source_cells=';'.join(f'{s}:{n}' for s,n in refs), source_labels=';'.join(c['label'] for c in cells),
                         preferred_key=key, alternatives=';'.join(dict.fromkeys([key,*alternatives])),
                         represented_dollar_cap=coverage, fixed_eligible=fixed, external=external))
    c='T31700-A'; b='T31200-A'; a='T30100-A'; s='T31300-A'
    for name,line,key,alts,fixed in [
        ('general_public_services',2,'population',['wages'],True),
        ('defense',3,'population',[],True),
        ('public_order_safety',4,'population',['adults'],False),
        ('economic_affairs_services',5,'resources',['wages','population'],False),
        ('housing_community_services',6,'population',['resources'],False),
        ('health_services',7,'health_other',['population','veterans'],False),
        ('recreation_culture',8,'population',['resources'],False),
        ('education_services',9,'education_mix',['school_operating','age5_24'],False),
        ('income_security_services',10,'cash_assistance',['population','all_cash'],False)]:
        add(name,[(c,line)],'consumption',key,alts,fixed=fixed)
    for benefits in [
        ('social_security',[5],'social_security',['age65plus'],True),
        ('medicare',[6],'medicare',['age65plus'],True),
        ('unemployment',[7],'unemployment',['working_age'],True),
        ('railroad_retirement',[12],'social_security',['age65plus'],False),
        ('pension_guaranty',[13],'age65plus',['social_security'],False),
        ('veterans_life_insurance',[14],'veterans',['adults'],False),
        ('workers_compensation',[15,30],'workers_comp',['working_age','wages'],False),
        ('military_medical',[16],'tricare',['veterans','population'],False),
        ('veterans_pension_disability',[18],'veterans',['adults'],True),
        ('veterans_readjustment',[19],'veterans',['age18_24'],False),
        ('veterans_other',[20],'va_medical',['veterans'],False),
        ('snap',[21],'snap',['cash_assistance'],True),
        ('black_lung',[22],'workers_comp',['age65plus'],False),
        ('ssi',[23,36],'ssi',['all_cash','population'],True),
        ('refundable_tax_credits',[25],'refundable_credits',['working_age'],True),
        ('other_federal_benefits',[26],'all_cash',['health_other','population'],False),
        ('temporary_disability',[29],'workers_comp',['working_age'],False),
        ('medicaid_and_chip_other_medical',[33,34],'medicaid',['medicaid_covered'],True),
        ('family_and_general_assistance',[35,37],'cash_assistance',['all_cash'],True),
        ('energy_assistance',[38],'energy',['cash_assistance'],True),
        ('other_state_welfare',[39],'wic',['cash_assistance'],False),
        ('education_benefits',[40],'postsecondary',['age18_24'],False),
        ('employment_training',[41],'working_age',['unemployment'],False),
        ('other_state_benefits',[42],'population',['veterans'],False)]:
        name, lines, key, alts, coverage = benefits
        add(name,[(b,n) for n in lines],'social_benefits',key,alts,coverage)
    add('foreign_territory_social_benefits',[(b,43)],'foreign','external',[],external=True)
    add('other_foreign_current_transfers',[(a,26)],'foreign','external',[],external=True)
    add('domestic_interest',[(a,28)],'interest','population',[],fixed=True)
    add('foreign_interest',[(a,29)],'interest','external',[],external=True)
    for name,lines,key,alts in [('agricultural_subsidies',[3],'wages',['resources']),
        ('housing_subsidies',[4],'housing_support',['resources','wages']),
        ('transport_subsidies',[5,6],'resources',['wages','population']),
        ('other_subsidies',[7,8],'resources',['wages','population'])]:
        add(name,[(s,n) for n in lines],'subsidies',key,alts)
    owned = [ref for r in rows for ref in r['source_cells'].split(';')]
    if len(set(owned)) != len(owned):
        raise ValueError('A BEA leaf is owned twice')
    for family, expected in [('consumption',tables[c][1]['million']/1000),
        ('social_benefits',tables[b][2]['million']/1000),('subsidies',tables[s][1]['million']/1000)]:
        subtotal=sum(r['official_bn'] for r in rows if r['family']==family)
        if abs(subtotal-expected)>.003: raise ValueError(f'BEA family not exhausted: {family}')
    residual = TOTAL_BN-sum(r['official_bn'] for r in rows)
    if abs(residual) > .01:
        raise ValueError(f'Nonrounding partition residual: {residual}')
    rows.append(dict(category='source_rounding',family='rounding',official_bn=residual,
        source_cells='T30100-A:20 minus disjoint leaves',source_labels='Published million-dollar cell rounding',
        preferred_key='external',alternatives='external',represented_dollar_cap=False,fixed_eligible=False,external=True))
    return pd.DataFrame(rows)


def canonical_target(d):
    civilian = d.PRPERTYP.eq(2) | d.A_AGE.lt(15)
    native = d.PRCITSHP.isin([1,2,3])
    us = [57,60,66,69,73,78]
    target = ((d.PRCITSHP.isin([4,5]) & d.PENATVTY.eq(303)) |
        (native & (d.PEFNTVTY.eq(303)|d.PEMNTVTY.eq(303))) |
        (native & d.PEFNTVTY.isin(us) & d.PEMNTVTY.isin(us) & d.PRDTHSP.eq(1)))
    return civilian.to_numpy(), (target & civilian).to_numpy()


def equal_unit_share(values, ids):
    f=pd.DataFrame({'unit':ids,'v':np.asarray(values,float)})
    return (f.groupby('unit').v.transform('sum')/f.groupby('unit').v.transform('size')).to_numpy()


def build_keys(root):
    fiscal=root/'infra/immigration-fiscal'
    archive=fiscal/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    if sha(archive)!=CPS_SHA: raise ValueError('CPS source changed')
    fields=['PH_SEQ','PPPOS','A_AGE','PRPERTYP','PRCITSHP','PENATVTY','PEFNTVTY','PEMNTVTY','PRDTHSP',
        'SPM_ID','SPM_HEAD','SS_VAL','SSI_VAL','PAW_VAL','UC_VAL','VET_VAL','WC_VAL','WSAL_VAL',
        'EIT_CRED','ACTC_CRD','SPM_SNAPSUB','SPM_ENGVAL','SPM_WICVAL','SPM_CAPHOUSESUB','SPM_RESOURCES',
        'PUB','PRIV','MIL','CHAMPVA','MCAID']
    with zipfile.ZipFile(archive) as z:
        d=pd.read_csv(z.open('pppub25.csv'),usecols=fields)
        w=pd.read_csv(z.open('asec_csv_repwgt_2025.csv'),usecols=['h_seq','PPPOS','pwwgt0']).rename(columns={'h_seq':'PH_SEQ'})
    d=d.merge(w,on=['PH_SEQ','PPPOS'],validate='one_to_one',how='left')
    if d.isna().any().any(): raise ValueError('Missing CPS keys')
    civ,target=canonical_target(d); weight=d.pwwgt0.to_numpy(float)
    total=float(weight[civ].sum()); nt=float(weight[target].sum())
    if abs(nt-40896574.15235156)>.01: raise ValueError('Canonical target population drift')
    params=fiscal/'ledger_absolute_2026_09_17/params/params.json'
    parameters=json.loads(params.read_text())
    resident=parameters['population']['us_resident_population_2024_07_01']['value']
    pop_pin=next(p for p in parameters['staged_files'] if Path(p['path']).name=='NST-EST2024-ALLDATA.csv')
    pop_source=Path(pop_pin['path'])
    if sha(pop_source)!=pop_pin['sha256']: raise ValueError('Population source changed')
    raw_pop=pd.read_csv(pop_source)
    if raw_pop.loc[raw_pop.SUMLEV.eq(10),'POPESTIMATE2024'].tolist()!=[resident]:
        raise ValueError('Parameter disagrees with primary resident population cell')
    if not 0<nt<total<resident: raise ValueError('Invalid population bridge')
    counts=d.groupby('SPM_ID').SPM_ID.transform('size')
    def unit_field(field):
        if not d.groupby('SPM_ID')[field].nunique().eq(1).all(): raise ValueError(f'Nonconstant unit field {field}')
        return d[field].to_numpy(float)/counts.to_numpy()
    dollars={k:d[v].to_numpy(float) for k,v in [('social_security','SS_VAL'),('ssi','SSI_VAL'),
        ('cash_assistance','PAW_VAL'),('unemployment','UC_VAL'),('veterans','VET_VAL'),('workers_comp','WC_VAL'),('wages','WSAL_VAL')]}
    dollars['refundable_credits']=(d.EIT_CRED+d.ACTC_CRD).to_numpy(float)
    dollars['all_cash']=sum(dollars[k] for k in ['social_security','ssi','cash_assistance','unemployment','veterans'])
    units={k:unit_field(v) for k,v in [('snap','SPM_SNAPSUB'),('energy','SPM_ENGVAL'),('wic','SPM_WICVAL'),('housing_support','SPM_CAPHOUSESUB')]}
    units['resources']=np.maximum(unit_field('SPM_RESOURCES'),0)
    ages={'population':np.ones(len(d)), 'age65plus':d.A_AGE.ge(65).to_numpy(float),
        'working_age':d.A_AGE.between(18,64).to_numpy(float),'adults':d.A_AGE.ge(18).to_numpy(float),
        'age5_24':d.A_AGE.between(5,24).to_numpy(float),'age18_24':d.A_AGE.between(18,24).to_numpy(float),
        'medicaid_covered':d.MCAID.eq(1).to_numpy(float)}
    sys.path.insert(0,str(fiscal/'build'))
    from meps_health_transport_2024 import read_meps, donor_model
    meps=fiscal.parents[1]/'sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip'
    md,_=read_meps(meps,meps.with_name('h256su.txt')); cells,codes,_=donor_model(md,d,False)
    valid=md.PERWT24F.gt(0)&md.AGE24X.ge(0)&md.BORNUSA.isin([1,2])
    sample=md.loc[valid]; index=pd.MultiIndex.from_frame(cells[['age_band','born']])
    exposure=~(d.PUB.eq(0)&d.PRIV.eq(0)).to_numpy()
    if d.loc[~exposure,'A_AGE'].gt(0).any(): raise ValueError('Reference exclusion includes noninfant')
    medical={}
    for name,cols in [('medicare',['TOTMCR24']),('medicaid',['TOTMCD24']),('va_medical',['TOTVA24']),
        ('tricare',['TOTTRI24']),('health_other',['TOTVA24','TOTTRI24','TOTOFD24','TOTSTL24'])]:
        sums=sample.assign(wx=sample[cols].sum(axis=1)*sample.PERWT24F).groupby(['age_band','born']).wx.sum()
        pop=sample.groupby(['age_band','born']).PERWT24F.sum()
        mean=(sums/pop).reindex(index)
        if mean.isna().any(): raise ValueError('Unmatched payer cell')
        medical[name]=mean.to_numpy()[codes]*exposure
    rows=[]
    def export(allocation,name,vector,unit,scope,coverage=False):
        v=np.asarray(vector,float)
        if not np.isfinite(v).all() or np.any(v<0): raise ValueError(f'Invalid proxy {name}')
        national=float(v[civ]@weight[civ]); targeted=float(v[target]@weight[target])
        if national<=0: raise ValueError(f'Empty proxy {name}')
        rows.append(dict(allocation=allocation,key=name,national_key_total=national,target_key_total=targeted,
            other_key_total=national-targeted,target_share=targeted/national,unit=unit,scope=scope,
            national_positive_key_persons=float(weight[civ&(v>0)].sum()),target_positive_key_persons=float(weight[target&(v>0)].sum()),
            exposure_interpretation='People assigned a positive key, not necessarily direct recipients; donor means apply to whole matching cells',
            represented_dollars=national if coverage else np.nan))
    for allocation in ['personal','shared']:
        for name,v in dollars.items():
            export(allocation,name,v if allocation=='personal' else equal_unit_share(v,d.SPM_ID),'dollars','CPS2025 income2024; canonical civilian',True)
        for name,v in units.items(): export(allocation,name,v,'dollars','CPS SPM benefit/resources allocated equally to unit members',name!='resources')
        for name,v in ages.items(): export(allocation,name,v,'persons','CPS current-age or annual-coverage proxy')
        for name,v in medical.items(): export(allocation,name,v,'expected_dollars','Raw MEPS2024 payer mean, age/birth transport, reference exposure',True)
    school=fiscal/'school_enrollment_2026_09_20/derived/updated_account_components.csv'
    school_inputs=verified_school_dependencies(school)
    sc=pd.read_csv(school)
    for allocation in ['personal','shared']:
        part=sc.query('allocation==@allocation').pivot(index='component',columns='group',values='spending_bn')
        for name,components in [('school_operating',['school']),('postsecondary',['P']),('education_mix',['school','P'])]:
            n=float(part.loc[components,'national_civilian'].sum())*1e9; t=float(part.loc[components,TARGET].sum())*1e9
            rows.append(dict(allocation=allocation,key=name,national_key_total=n,target_key_total=t,
                other_key_total=n-t,target_share=t/n,unit='proxy_dollars',scope='Existing operating-school/postsecondary incidence; no K or D capital/interest',
                national_positive_key_persons=np.nan,target_positive_key_persons=np.nan,
                exposure_interpretation='Aggregate cost-weighted incidence key; recipient count not recovered from this export',represented_dollars=np.nan))
    metadata=dict(target_population=nt,cps_civilian_population=total,resident_population=resident,
        outside_cps_population=resident-total,household_pool_fraction=total/resident,
        denominator_warning='2024 July resident control versus March2025 CPS civilians; modeled bridge, not observed institutional spending',
        meps_excluded_donors=int((~valid&md.PERWT24F.gt(0)).sum()),meps_age_rule='AGE24X>=0, known US/not-US birth, positive weight')
    paths=[archive,params,pop_source,school,*school_inputs,meps,meps.with_name('h256su.txt'),fiscal/'build/meps_health_transport_2024.py',fiscal/'build/public_mvp_io.py']
    return pd.DataFrame(rows),metadata,paths


def allocate(amount,share,household_fraction,external=False,fixed=False,represented_cap=None):
    if not 0<=share<=1 or not 0<household_fraction<=1: raise ValueError('Invalid incidence fraction')
    if external: return dict(target_bn=0.,other_household_bn=0.,outside_household_bn=0.,external_bn=amount,unallocated_bn=0.)
    household=amount*household_fraction
    outside=amount-household
    if represented_cap is not None:
        household=min(household,max(0.,represented_cap)); outside=0.
    target=0. if fixed else household*share
    return dict(target_bn=target,other_household_bn=household-target,outside_household_bn=outside,
        external_bn=0.,unallocated_bn=amount-household-outside)


def scenarios(categories,keys,population):
    rows=[]; table=keys.set_index(['allocation','key']); hf=population['household_pool_fraction']
    names=['complete_preferred_F_per_capita','complete_preferred_F_fixed','complete_alternative_keys_F_per_capita',
        'complete_alternative_keys_F_fixed','represented_only_F_per_capita']
    for attribution in ['personal','shared']:
        for scenario in names:
            for r in categories.to_dict('records'):
                choices=r['alternatives'].split(';')
                key=choices[1] if 'alternative' in scenario and len(choices)>1 else choices[0]
                if r['fixed_eligible']: key='population'
                external=bool(r['external']); fixed=bool(r['fixed_eligible']) and '_F_fixed' in scenario
                if external: share=0.; cap=None
                else:
                    proxy=table.loc[(attribution,key)]; share=float(proxy.target_share); cap=None
                    if scenario.startswith('represented'):
                        cap=(float(proxy.represented_dollars)/1e9 if r['represented_dollar_cap'] and pd.notna(proxy.represented_dollars) else 0.)
                allocated=allocate(r['official_bn'],share,hf,external,fixed,cap)
                row=dict(scenario=scenario,attribution=attribution,category=r['category'],family=r['family'],
                    official_bn=r['official_bn'],key=key,key_target_share=share,household_pool_fraction=hf,
                    proxy_scope='BEA explicit foreign' if external else table.loc[(attribution,key),'scope'],
                    F_convention='fixed_target_zero_redistribute_to_other' if fixed else 'average_cost_incidence',
                    **allocated)
                row['other_bn']=row['other_household_bn']+row['outside_household_bn']
                row['target_share_national']=row['target_bn']/r['official_bn'] if r['official_bn'] else 0.
                rows.append(row)
    frame=pd.DataFrame(rows)
    np.testing.assert_allclose(frame[AMOUNTS].sum(axis=1),frame.official_bn,atol=1e-9,rtol=0)
    return frame


def main(args):
    out=args.out; out.mkdir(parents=True,exist_ok=True); (out/'audit.json').unlink(missing_ok=True)
    tables,meta=read_bea(args.bea); categories=partition(tables)
    keys,pop,inputs=build_keys(args.source_root)
    source_pins=HERE/'SOURCE_PINS.json'
    verify_primary_pins([args.bea,*inputs],json.loads(source_pins.read_text()))
    allocations=scenarios(categories,keys,pop)
    totals=allocations.groupby(['scenario','attribution'],sort=False)[['official_bn',*AMOUNTS,'other_bn']].sum().reset_index()
    np.testing.assert_allclose(totals.official_bn,TOTAL_BN,rtol=0,atol=1e-9)
    if not np.allclose(totals.loc[totals.scenario.str.startswith('complete'),'unallocated_bn'],0,atol=1e-9):
        raise ValueError('Complete arm leaves unexplained unallocated amount')
    alternatives=[]
    for attribution in ['personal','shared']:
        kt=keys.query('allocation==@attribution').set_index('key')
        for row in categories.to_dict('records'):
            for key in row['alternatives'].split(';'):
                external=bool(row['external']); share=0 if external else float(kt.loc[key,'target_share'])
                a=allocate(row['official_bn'],share,pop['household_pool_fraction'],external)
                alternatives.append(dict(attribution=attribution,category=row['category'],key=key,
                    official_bn=row['official_bn'],key_target_share=share,**a))
    rename={'scenario':'scenario_id','attribution':'allocation','official_bn':'national_bn',
            'key':'allocation_key','key_target_share':'target_key_share'}
    allocations['response_class']=allocations.family.map({'consumption':'service',
        'social_benefits':'household_transfer','interest':'interest','foreign':'foreign',
        'subsidies':'subsidy','rounding':'rounding'})
    public=allocations.category.isin(['defense','general_public_services'])
    allocations.loc[public,'response_class']='public_goods'
    frames={'categories':categories.rename(columns={'official_bn':'national_bn'}),
        'incidence_keys':keys,'allocations':allocations.rename(columns=rename),
        'scenario_totals':totals.rename(columns=rename),
        'category_proxy_alternatives':pd.DataFrame(alternatives).rename(columns=rename),
        'official_cells':pd.DataFrame([dict(sheet=s,line=n,**cell) for s,items in tables.items() for n,cell in items.items()])}
    for name,frame in frames.items(): frame.to_csv(out/f'{name}.csv',index=False)
    receipt=dict(year=2024,total_current_spending_bn=TOTAL_BN,bea_url=BEA_URL,table_metadata=meta,
        population=pop,contract_sha256=sha(HERE/'CONTRACT.md'),
        source_hashes={str(p):sha(p) for p in [args.bea,*inputs,HERE/'builder.py',source_pins]},
        outputs={name:sha(out/f'{name}.csv') for name in frames},
        boundary='Consolidated government current expenditure; no gross grants/capital add-on',
        incidence_status='CONDITIONAL_MODEL_NOT_IDENTIFIED_ETHNIC_ADMINISTRATIVE_COST',
        response_coefficients_applied=False,unallocated_is_not_institutional=True)
    (out/'audit.json').write_text(json.dumps(receipt,indent=2,allow_nan=False)+'\n')
    print(totals.to_string(index=False))


if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--source-root',type=Path,required=True)
    p.add_argument('--bea',type=Path,default=Path('/Users/alien/research-data/immigration-fiscal/data/external/bea_nipa/Section3All_xls.xlsx'))
    p.add_argument('--out',type=Path,default=HERE/'derived'); main(p.parse_args())
