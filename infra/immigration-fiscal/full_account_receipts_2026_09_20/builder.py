"""Exhaustive conditional BEA2024 receipt attribution, with an unallocated diagnostic."""
from __future__ import annotations

import sys as _path_sys
from pathlib import Path as _Path
_path_sys.path.insert(0, str(_Path(__file__).resolve().parents[1] / "build"))
import paths as _data_paths

import argparse
import importlib.util
import json
from pathlib import Path
import numpy as np
import openpyxl
import pandas as pd

HERE = Path(__file__).resolve().parent
TARGET = 'mexican_observed_total'
GROUPS = [TARGET, 'other_residents', 'national_civilian']
SCENARIOS = ['cbo_collective','federal_gap_high_agi','treasury_815','nas_80',
             'corporate_all_capital','property_residual_consumption','public_assets_tax_base',
             'capital_external_50','capital_external_100','medicare_income_weighted']


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def partition(amount, share, external_fraction=0):
    if not np.isfinite([amount,share,external_fraction]).all() or not 0 <= share <= 1 or not 0 <= external_fraction <= 1:
        raise ValueError('Invalid receipt allocation or incidence fraction')
    domestic = amount*(1-external_fraction)
    return domestic*share, domestic*(1-share), amount*external_fraction


def residual_property(total, modeled_owner):
    if modeled_owner < 0 or modeled_owner > total:
        raise ValueError('Modeled owner property exceeds national property pool')
    return total-modeled_owner


def required_share(keys, key, external=0, target_override=None):
    if external == 1 or target_override is not None:
        return 0.0  # These explicit paths do not use a domestic proxy.
    if key not in keys:
        raise ValueError(f'Missing required incidence key: {key}')
    return keys[key]


def ratio_replicates(target, national):
    if np.any(national <= 0) or not np.isfinite([target,national]).all():
        raise ValueError('Nonpositive or nonfinite proxy denominator')
    result = target/national
    if np.any(result < 0) or np.any(result > 1):
        raise ValueError('Proxy share outside disjoint population')
    return result


def share_summary(values):
    return float(values[0]),float(np.sqrt(4/160*np.square(values[1:]-values[0]).sum()))


def derive_keys(root, coverage, hashes):
    fiscal = root/'infra/immigration-fiscal'
    helper = fiscal/'education_origin_fiscal_2026_09_19/builder.py'
    annual,absolute,arrival = load(helper,'receipt_evidence').configure(root)
    for field in ['AGI','SEMP_VAL','FRSE_VAL']:
        if field not in annual.ext.base.PERSON:
            annual.ext.base.PERSON.append(field)
    cps = fiscal/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    if coverage.sha(cps) != annual.ext.CPS_SHA:
        raise ValueError('Unreviewed CPS source')
    state = annual.ext.build(argparse.Namespace(cps_zip=cps))
    d,w = state['d'],state['person_weights']
    civilian = (d.PRPERTYP.eq(2)|d.A_AGE.lt(15)).to_numpy()
    target = np.logical_or.reduce([state['group'][g] for g in absolute.TARGETS]) & civilian
    wage = d.WSAL_VAL.clip(lower=0).to_numpy(float)
    se = .9235*np.maximum(d.SEMP_VAL.to_numpy(float)+d.FRSE_VAL.to_numpy(float),0)
    se = np.where(se>=400,se,0)
    se_capped = np.minimum(se,np.maximum(168600-np.minimum(wage,168600),0))
    size = d.groupby('SPM_ID').SPM_ID.transform('size').to_numpy(float)
    consumption = d.SPM_RESOURCES.clip(lower=0).to_numpy(float)/size
    medicare = d.MCARE.eq(1).to_numpy(float)
    if not d.MCARE.isin([0,1,2]).all():
        raise ValueError('MCARE codebook drift')
    vectors = dict(population=np.ones(len(d)),adults=d.A_AGE.ge(18).to_numpy(float),
                   wage=wage,wage_oasdi=np.minimum(wage,168600),
                   self_payroll=.124*se_capped+.029*se,
                   positive_fica_worker=d.FICA.gt(0).to_numpy(float),
                   capital=(d.INT_VAL+d.DIV_VAL+d.RNT_VAL).clip(lower=0).to_numpy(float),
                   interest_dividend=(d.INT_VAL+d.DIV_VAL).clip(lower=0).to_numpy(float),
                   federal_liability=d.FEDTAX_BC.to_numpy(float),
                   federal_high_agi=(d.FEDTAX_BC*d.AGI.ge(500000)).to_numpy(float),
                   state_liability=d.STATETAX_A.clip(lower=0).to_numpy(float),
                   consumption=consumption,medicare=medicare,
                   medicare_income=medicare*(d.AGI.clip(lower=0).to_numpy(float)+1))
    params_path=fiscal/'ledger_absolute_2026_09_17/params/params.json'
    params=json.loads(params_path.read_text())
    population_path=_data_paths.data_root(require_exists=False) / 'external/census_popest_2024/NST-EST2024-ALLDATA.csv'
    expected='b8b50bd345d8a5f33d5c8a28c95aeaa0a50971356f000d9b48276a65fd9022a7'
    if coverage.sha(population_path)!=expected:
        raise ValueError('Unreviewed resident-population vintage')
    population_data=pd.read_csv(population_path)
    national_row=population_data.query('SUMLEV==10 and NAME=="United States"')
    if len(national_row)!=1:
        raise ValueError('Ambiguous resident population')
    resident=float(national_row.POPESTIMATE2024.iloc[0])
    coverage.same(resident,params['population']['us_resident_population_2024_07_01']['value'],'Resident-population primary source',0)
    records=[]
    keys={}
    for allocation in ['shared','personal']:
        keys[allocation]={}
        for name,original in vectors.items():
            vector=original
            if np.any(vector<0):
                raise ValueError(f'Negative allocation proxy:{name}')
            if allocation=='shared':
                unit=np.bincount(state['index'],weights=vector,minlength=state['n_units'])
                vector=annual.ext.allocate(unit,state['index'],np.ones(len(d),bool),state['n_units'])
            national=vector[civilian]@w[civilian]
            group=vector[target]@w[target]
            other=vector[civilian&~target]@w[civilian&~target]
            np.testing.assert_allclose(national,group+other,rtol=1e-12,atol=.05)
            shares=ratio_replicates(group,national)
            share,se_share=share_summary(shares)
            keys[allocation][name]=share
            records.append(dict(allocation=allocation,allocation_key=name,target_key_share=share,
                                target_share_sampling_se=se_share,target_key_total=group[0],
                                other_key_total=other[0],national_key_total=national[0],
                                denominator_scope='CPS2025 civilian household persons, income2024',
                                missing_components='adjusted/unrealized capital gains and institutional/territorial units absent' if name in ['capital','interest_dividend'] else 'coverage/concept error not included in sampling SE'))
            if name=='population':
                resident_shares=ratio_replicates(group,np.full_like(group,resident))
                resident_share,resident_se=share_summary(resident_shares)
                keys[allocation]['resident_population']=resident_share
                records.append(dict(allocation=allocation,allocation_key='resident_population',target_key_share=resident_share,
                                    target_share_sampling_se=resident_se,target_key_total=group[0],other_key_total=resident-group[0],
                                    national_key_total=resident,denominator_scope='Census July2024 US resident population; target observed March2025 CPS stock',
                                    missing_components='Target held observed; all resident coverage/time residual assigned other, not measured target institutional ancestry'))
    # Separate aggregation route checks the consequential wage key.
    oracle=pd.DataFrame(dict(target=target,civilian=civilian,value=w[:,0]*wage)).query('civilian').groupby('target').value.sum()
    coverage.same(keys['personal']['wage'],oracle[True]/oracle.sum(),'Independent pandas wage share',1e-12)
    paths=[helper,cps,params_path,population_path,Path(annual.__file__),Path(absolute.__file__),Path(arrival.__file__),
           Path(annual.ext.__file__),Path(annual.ext.base.__file__),
           fiscal/'gen_ledger_extension_2026_09_16/state_parameters.csv',
           root/'sources/immigration-fiscal/data/external/cps_asec_doc/ddl25.txt']
    for path in paths:
        hashes[str(path)]=coverage.sha(path)
    return keys,pd.DataFrame(records)


def conditional_rows(scenario,allocation,tables,keys,raw,tax,coverage):
    """One disjoint receipt partition; ownership assumptions do not imply causal response."""
    v=lambda sheet,line:coverage.value(tables,sheet,line)
    a=lambda line:v('T30100-A',line)
    p=lambda line:v('T30400-A',line)
    s=lambda line:v('T30500-A',line)
    c=lambda line:v('T30600-A',line)
    k=keys[allocation]
    ext={'capital_external_50':.5,'capital_external_100':1}.get(scenario,0)
    rows=[]
    def add(category,amount,key,response,source,external=0,note='',target_override=None):
        share=required_share(k,key,external,target_override)
        target,other,foreign=partition(amount,share,external)
        if target_override is not None:
            if external or amount<=0 or not 0<=target_override<=amount:
                raise ValueError('Invalid explicit group amount')
            target,other=target_override,amount-target_override
            share=target/amount
        rows.append(dict(scenario_id=scenario,allocation=allocation,category=category,national_bn=amount,
                         target_bn=target,other_bn=other,external_bn=foreign,unallocated_bn=0.,
                         allocation_key=key,target_key_share=share,response_class=response,
                         source_locator=source,denominator_scope=('Census340110988 resident population; other includes outside-CPS residents' if key=='resident_population' else 'Domestic total transported to CPS civilian household proxy; outside-CPS other implicitly assigned0, not known0'),
                         incidence_status='conditional accounting allocation',
                         external_status='BEA identified RoW' if response=='foreign' else ('assumed foreign/nonresident capital incidence' if external else 'none assumed'),
                         causal_response_fixed=0. if response in ['public_asset','foreign','rounding'] else np.nan,
                         capital_fraction=1. if response in ['corporate_capital','business_property','other_business'] else 0.,
                         uncertainty=note or 'Proxy transport and universe closure; not measured ethnic incidence'))
    fedkey='federal_liability'
    override=None
    if scenario=='federal_gap_high_agi':
        national=tax.loc[('national_civilian','federal_before_refundable')]/1e9
        target=tax.loc[(TARGET,'federal_before_refundable')]/1e9
        if p(3)<national:
            raise ValueError('Federal high-AGI residual arm requires a positive national gap')
        override=target+(p(3)-national)*k['federal_high_agi']
        fedkey='observed_liability_plus_positive_gap_high_agi'
    add('federal_income_tax',p(3),fedkey,'personal_income','3.4/3',target_override=override,
        note='Tax-liability source labor versus capital unknown; liability/receipt timing and high-tail transport remain uncertain')
    add('state_local_income_tax',p(9),'state_liability','personal_income','3.4/9',note='Positive after-credit CPS liability proxy; negative after-credit observations retained in evidence arm; refundable state credits not separately identified')
    add('personal_motor_vehicle',p(10),'adults','household_direct','3.4/10')
    add('personal_property_tax',p(11),'capital','household_direct','3.4/11')
    add('other_personal_tax',p(12),'state_liability','household_direct','3.4/12')
    for name,line,key in [('employee_oasdi',24,'wage_oasdi'),('employee_hi',25,'wage'),
                           ('self_employment_oasdi_hi',26,'self_payroll'),('employer_oasdi',5,'wage_oasdi'),
                           ('employer_hi',6,'wage')]:
        add(name,c(line),key,'household_direct',f'3.6/{line}',note='All-covered earnings allocation proxy; actual exemptions/eligibility unresolved; employer incidence on labor')
    add('medicare_supplementary_premiums',c(27),'medicare_income' if scenario=='medicare_income_weighted' else 'medicare','household_direct','3.6/27')
    add('other_domestic_social_contributions',a(8)-c(22)-c(4)-c(27),'positive_fica_worker','household_direct','3.1/8 minus3.6/22,4,27',note='Positive-FICA worker proxy transports NAS UI convention to a heterogeneous other-fund residual')
    fraction={'treasury_815':.815,'nas_80':.8,'corporate_all_capital':1}.get(scenario,.75)
    capkey='interest_dividend' if scenario=='nas_80' else 'capital'
    add('corporate_capital',a(5)*fraction,capkey,'corporate_capital','3.1/5, conditional fraction',external=ext,
        note='CPS interest/dividend/rent proxy lacks adjusted capital gains; fractions are conventions/sensitivities')
    add('corporate_labor',a(5)*(1-fraction),'wage','household_direct','3.1/5, complementary fraction')
    add('general_sales_tax',s(20),'consumption','household_direct','3.5/20')
    owner=raw.loc[('national_civilian','owner_property'),'receipts_bn']
    owner_target=raw.loc[(TARGET,'owner_property'),'receipts_bn']
    add('modeled_owner_property',owner,'modeled_owner_property','household_direct','existing owner-housing model; part of3.5/38',target_override=owner_target)
    property_key='consumption' if scenario=='property_residual_consumption' else 'capital'
    add('remaining_production_property',residual_property(s(38),owner),property_key,'business_property','3.5/38 minus modeled_owner_property',external=ext,
        note='Residual includes rental/business property; consumer versus capital incidence unresolved')
    if property_key=='consumption':rows[-1]['capital_fraction']=0.
    add('excise_selective_sales',s(4)+s(23),'consumption','household_direct','3.5/4+23')
    add('customs_duties',s(15),'consumption','household_direct','3.5/15',note='Domestic consumer-incidence convention; foreign-supplier pass-through not estimated')
    add('other_production_taxes',s(1)-s(20)-s(38)-s(4)-s(23)-s(15),'capital','other_business','3.5 production remainder',external=ext)
    add('rest_world_tax_contributions',a(6)+a(9),'none','foreign','3.1/6+9',external=1)
    assetkey='federal_liability' if scenario=='public_assets_tax_base' else 'resident_population'
    add('government_asset_income',a(10),assetkey,'public_asset','3.1/10',note='Collective ownership convention; government asset cash flow fixed under population-response branch')
    add('business_current_transfers',a(16),'capital','other_business','3.1/16',external=ext,note='Net business transfers/fines/settlements allocated to capital by assumption')
    add('personal_current_transfers',a(17),'consumption','household_direct','3.1/17')
    add('rest_world_current_transfers',a(18),'none','foreign','3.1/18',external=1)
    add('enterprise_surplus',a(19),assetkey,'public_asset','3.1/19',note='Signed negative enterprise surplus retained; collective ownership allocation with response0')
    rounding=a(1)-sum(row['national_bn'] for row in rows)
    if abs(rounding)>.01:
        raise ValueError(f'Nonexhaustive BEA partition:{rounding}')
    add('source_rounding',rounding,'population','rounding','published component rounding')
    return rows


def evidence_rows(allocation,tables,raw,tax,coverage):
    national=raw.xs('national_civilian')
    t=tax.xs('national_civilian')/1e9
    source=coverage.receipt_rows(tables,national,t)
    tg=tax.xs(TARGET)/1e9
    targets=dict(federal_income_tax=tg.federal_before_refundable,state_local_income_tax=tg.state_after_credits,
                 employee_self_oasdi_hi=tg.fica_cps,employer_oasdi_hi=raw.loc[(TARGET,'employer'),'receipts_bn'])
    for category,component in [('corporate_income_tax','C'),('general_sales_tax','sales'),('production_property_tax','owner_property'),('excise_selective_sales','X')]:
        targets[category]=raw.loc[(TARGET,component),'receipts_bn']
    rows=[]
    for row in source:
        category=row['category']
        target=targets.get(category,0.)
        foreign=row['official_bn'] if category=='rest_world_tax_contributions' else 0.
        # The original coarse transfer row mixes source sectors; split observed RoW out.
        if category=='current_transfer_receipts':
            foreign=coverage.value(tables,'T30100-A',18)
        rows.append(dict(scenario_id='evidence_only',allocation=allocation,category=category,
                         national_bn=row['official_bn'],target_bn=target,other_bn=row['modeled_bn']-target,
                         external_bn=foreign,unallocated_bn=row['official_bn']-row['modeled_bn']-foreign,
                         allocation_key='existing_model_no_residual_allocation',target_key_share=target/row['modeled_bn'] if row['modeled_bn'] else 0,
                         response_class='diagnostic_only',source_locator='national_coverage receipt crosswalk',
                         denominator_scope='Existing CPS civilian household attribution; residual signed',
                         incidence_status='existing model plus unallocated residual',external_status='BEA identified RoW only',
                         causal_response_fixed=np.nan,capital_fraction=np.nan,uncertainty=row['interpretation']))
    return rows


def validate(frame,official):
    np.testing.assert_allclose(frame.national_bn,frame.target_bn+frame.other_bn+frame.external_bn+frame.unallocated_bn,rtol=0,atol=1e-9)
    if frame.duplicated(['scenario_id','allocation','category']).any():
        raise ValueError('Duplicate receipt category')
    np.testing.assert_allclose(frame.groupby(['scenario_id','allocation']).national_bn.sum(),official,atol=1e-9)
    conditional=frame.query('scenario_id != "evidence_only"')
    np.testing.assert_allclose(conditional.unallocated_bn,0,atol=0)
    if not conditional.query('response_class == "public_asset"').causal_response_fixed.eq(0).all():
        raise ValueError('Public asset response must stay zero')


def validate_bea_parents(frame,tables,coverage):
    """Independent parent-line reconciliation catches omissions across subcategories."""
    groups={
        ('T30400-A',1):['federal_income_tax','state_local_income_tax','personal_motor_vehicle','personal_property_tax','other_personal_tax'],
        ('T30100-A',8):['employee_oasdi','employee_hi','self_employment_oasdi_hi','employer_oasdi','employer_hi','medicare_supplementary_premiums','other_domestic_social_contributions'],
        ('T30500-A',1):['general_sales_tax','modeled_owner_property','remaining_production_property','excise_selective_sales','customs_duties','other_production_taxes'],
        ('T30100-A',5):['corporate_capital','corporate_labor'],
        ('T30100-A',15):['business_current_transfers','personal_current_transfers','rest_world_current_transfers']}
    for (scenario,allocation),part in frame.query('scenario_id != "evidence_only"').groupby(['scenario_id','allocation']):
        amounts=part.set_index('category').national_bn
        for (sheet,line),categories in groups.items():
            coverage.same(amounts.loc[categories].sum(),coverage.value(tables,sheet,line),f'{scenario}/{allocation}/{sheet}/{line}')


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root',type=Path,required=True)
    ap.add_argument('--bea',type=Path,default=_data_paths.data_root(require_exists=False) / 'external/bea_nipa/Section3All_xls.xlsx')
    ap.add_argument('--out',type=Path,default=HERE/'derived')
    args=ap.parse_args()
    root=args.source_root.resolve(); fiscal=root/'infra/immigration-fiscal'
    coverage_path=fiscal/'national_coverage_2026_09_20/builder.py'
    coverage=load(coverage_path,'receipt_coverage')
    hashes={str(coverage_path):coverage.sha(coverage_path)}
    if coverage.sha(args.bea)!=coverage.BEA_SHA:
        raise ValueError('Unreviewed BEA vintage')
    hashes[str(args.bea)]=coverage.BEA_SHA
    book=openpyxl.load_workbook(args.bea,read_only=True,data_only=True)
    tables={name:coverage.read_table(list(book[name].values)) for name in ['T30100-A','T30400-A','T30500-A','T30600-A']}
    book.close()
    official=coverage.value(tables,'T30100-A',1)
    coverage.same(official,8008.290,'Pinned BEA current receipts',1e-9)
    tax=coverage.verified_output(fiscal/'admin_tax_checks_2026_09_19/derived','group_components',hashes)
    # Upstream school manifest binds source bytes; receipts must also equal verified macro output.
    school=fiscal/'school_enrollment_2026_09_20/derived'
    manifest=json.loads((school/'manifest.json').read_text())
    for record in manifest['inputs']:
        if coverage.sha(record['path'])!=record['sha256']:
            raise ValueError(f'School upstream drift:{record["path"]}')
        hashes[record['path']]=record['sha256']
    accounts=pd.read_csv(school/'updated_account_components.csv')
    macro=coverage.verified_output(fiscal/'macro_closure_2026_09_19/derived','updated_account_components',hashes)
    index=['allocation','group','component']
    np.testing.assert_allclose(accounts.set_index(index).sort_index().receipts_bn,macro.set_index(index).sort_index().receipts_bn,atol=1e-10)
    for path in [school/'manifest.json',school/'updated_account_components.csv']:
        hashes[str(path)]=coverage.sha(path)
    keys,keyframe=derive_keys(root,coverage,hashes)
    np.testing.assert_allclose(keyframe.query('allocation_key=="population"').target_key_total,40896574.152351856,atol=.02)
    rows=[];credits=[];sources=[]
    for allocation in ['shared','personal']:
        r=accounts.query('allocation==@allocation').set_index(['group','component'])
        t=tax.query('allocation==@allocation').set_index(['group','metric']).value
        rows.extend(evidence_rows(allocation,tables,r,t,coverage))
        for scenario in SCENARIOS:
            rows.extend(conditional_rows(scenario,allocation,tables,keys,r,t,coverage))
        for group in GROUPS:
            credit=(t.loc[(group,'eitc')]+t.loc[(group,'actc')])/1e9
            before=t.loc[(group,'federal_before_refundable')]/1e9
            after=t.loc[(group,'federal_after_refundable')]/1e9
            coverage.same(before-after,credit,'Credit presentation identity',1e-7)
            old=r.xs(group)
            fees=old.loc['G_fee_grossup','receipts_bn']
            receipt=old.receipts_bn.sum()-fees
            spending=old.spending_bn.sum()-fees
            credits.append(dict(allocation=allocation,group=group,credits_moved_to_spending_bn=credit,
                                fees_removed_from_both_sides_bn=fees,old_receipts_excluding_fees_bn=receipt,
                                before_credit_receipts_excluding_fees_bn=receipt+credit,
                                old_spending_excluding_fees_bn=spending,credit_presented_spending_bn=spending+credit,
                                net_balance_bn=receipt-spending))
        for scenario in SCENARIOS:
            for name in ['federal_income_tax','state_local_income_tax']:
                row=next(x for x in reversed(rows) if x['scenario_id']==scenario and x['allocation']==allocation and x['category']==name)
                sources.append(dict(scenario_id=scenario,allocation=allocation,category=name,
                                    target_tax_bn=row['target_bn'],identified_capital_tax_bn=np.nan,
                                    tax_source_unknown_bn=row['target_bn'],capital_tax_identification='not identified; missing amount is not zero capital tax',
                                    observed_asset_income_target_share=keys[allocation]['capital']))
    frame=pd.DataFrame(rows)
    validate(frame,official)
    validate_bea_parents(frame,tables,coverage)
    totals=frame.groupby(['scenario_id','allocation'],as_index=False)[['national_bn','target_bn','other_bn','external_bn','unallocated_bn']].sum()
    for allocation in ['shared','personal']:
        target_base=next(x['before_credit_receipts_excluding_fees_bn'] for x in credits if x['allocation']==allocation and x['group']==TARGET)
        coverage.same(totals.query('scenario_id=="evidence_only" and allocation==@allocation').target_bn.iloc[0],target_base,'Existing target receipts reproduced',1e-7)
    for allocation in ['shared','personal']:
        baseline=totals.query('scenario_id=="evidence_only" and allocation==@allocation').target_bn.iloc[0]
        totals.loc[totals.allocation.eq(allocation),'target_change_from_presented_partial_bn']=totals.loc[totals.allocation.eq(allocation),'target_bn']-baseline
    args.out.mkdir(parents=True,exist_ok=True)
    frames=dict(category_allocations=frame,scenario_totals=totals,allocation_keys=keyframe,
                credit_presentation=pd.DataFrame(credits),income_tax_source=pd.DataFrame(sources))
    for name,data in frames.items():
        data.to_csv(args.out/f'{name}.csv',index=False)
    for path in HERE.glob('*'):
        if path.is_file():hashes[str(path)]=coverage.sha(path)
    audit=dict(source_hashes=hashes,outputs={name:coverage.sha(args.out/f'{name}.csv') for name in frames},
               scope='CPS2025 observed Mexican-origin union40.896574m; calendar2024 dollars/current receipts',
               national_current_receipts_bn=official,calibration='conditional incidence allocation only; core unchanged',
               checks=['all rows and scenario sums conserve signed BEA receipts','public assets fixed response0',
                       'CPS161 replicate target+other conservation','independent pandas wage-share oracle',
                       'canonical current receipt and refundable-credit identities','all upstream source hashes'],
               assumptions=json.loads((HERE/'sources.json').read_text()))
    (args.out/'audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
    print(totals.to_string(index=False))


if __name__=='__main__':
    main()
