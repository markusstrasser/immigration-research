"""Same-income-year CPS2024 / IRS2023 / SSA2023 uncalibrated diagnostics."""
from pathlib import Path
import argparse, json
import numpy as np
import pandas as pd
from common import CW,PAYLOAD,check_sources,cps,payroll,returns,sha,summary

HERE=Path(__file__).resolve().parent
EDGES=np.array([5000,10000,15000,20000,25000,30000,40000,50000,75000,100000,200000,500000,1000000,1500000,2000000,5000000,10000000],float)

def band(agi):
    a=np.asarray(agi); return np.where(a<=0,0,np.searchsorted(EDGES,a,side='right')+1)

def source_tables(raw):
    a=pd.read_excel(raw/'23in12ms.xls',header=None)
    b=pd.read_excel(raw/'23in14ar.xls',header=None)
    assert 'Tax Year 2023' in a.iloc[0,0] and 'thousands of dollars' in a.iloc[1,0]
    assert 'Income tax after credits' in a.iloc[3,9]
    assert 'Total wages' in b.iloc[2,5]
    assert a.iloc[8,1]==b.iloc[8,1]==160602107
    assert a.iloc[9,0].strip()=='No adjusted gross income (includes deficits)'
    assert b.iloc[9,0].strip()=='No adjusted gross income'
    assert a.iloc[10:28,0].str.strip().tolist()==b.iloc[10:28,0].str.strip().tolist()
    metrics={'returns':(a,1,1),'agi':(a,2,1000),'taxable_income':(a,8,1000),
             'income_tax_after_nonrefundable':(a,10,1000),'total_wages':(b,6,1000),'w2_wages':(b,8,1000)}
    rows=[]
    for k,(frame,col,mult) in metrics.items():
        for i in range(19):
            rows.append({'band':i,'label':str(a.iloc[i+9,0]),'metric':k,'irs_value':float(frame.iloc[i+9,col])*mult})
        assert abs(frame.iloc[9:28,col].astype(float).sum()-float(frame.iloc[8,col]))<50
    return pd.DataFrame(rows),{k:float(f.iloc[8,c])*m for k,(f,c,m) in metrics.items()}

def run(args):
    raw,out=args.raw,args.out; out.mkdir(parents=True,exist_ok=True)
    check_sources(raw,json.loads((HERE/'source_lock.json').read_text()))
    d=cps(raw/'asecpub24csv.zip',2024); w=d[CW].to_numpy(float)
    values=payroll(d,160200)
    values.update(population=np.ones(len(d)),gross_wages=d.WSAL_VAL.to_numpy(),fica_cps=d.FICA.to_numpy(),
                  federal_before_refundable=d.FEDTAX_BC.to_numpy(),federal_after_refundable=d.FEDTAX_AC.to_numpy(),
                  agi=d.AGI.to_numpy(),state_tax=d.STATETAX_A.to_numpy(),
                  government_wage_oasdi_base=np.where(d.WECLW.eq(6),values['oasdi_wage_base'],0))
    values['cps_fica_plus_employer']=values['fica_cps']+values['employer_payroll']
    groups={'all':np.ones(len(d),bool),'selfid_mexican':d.PRDTHSP.eq(1).to_numpy(),'mexico_born':d.PENATVTY.eq(303).to_numpy()}
    groups['other_selfid']=~groups['selfid_mexican']
    scopes={'all_survey_persons':np.ones(len(d),bool),'civilian':d.civilian.to_numpy(),'civilian_household':(d.civilian&d.household).to_numpy()}
    rows=[]
    for scope,eligible in scopes.items():
        for region,geo in [('US',np.ones(len(d),bool)),('CA',d.GESTFIPS.eq(6).to_numpy()),('TX',d.GESTFIPS.eq(48).to_numpy())]:
            for group,g in groups.items():
                keep=eligible&geo&g
                for name,v in values.items():
                    rows.append({'scope':scope,'region':region,'group':group,'metric':name,**summary(v[keep]@w[keep])})
    components=pd.DataFrame(rows)
    for scope in scopes:
        for region in ['US','CA','TX']:
            p=components.query('scope==@scope and region==@region').pivot(index='metric',columns='group',values='estimate')
            np.testing.assert_allclose(p['all'],p.selfid_mexican+p.other_selfid,rtol=1e-12,atol=.1)
    sources=json.loads((HERE/'ssa_sources.json').read_text())
    comparisons=[]
    for system in ['oasdi','hi']:
        rowsource=sources[system]
        for region in ['US','CA','TX']:
            ref=np.array(rowsource['all_areas' if region=='US' else region],float)
            if region=='US': ref=ref-np.array(rowsource['PR'])-np.array(rowsource['other_unknown'])
            for scope in scopes:
                modeled=components.query('scope==@scope and region==@region and group=="all"').set_index('metric')
                for name,j,mult in [('wage_workers',1,1000),('se_workers',2,1000),(system+'_total_base',3,1e6),(system+'_wage_base',4,1e6),(system+'_se_base',5,1e6)]:
                    value=modeled.loc[name]
                    comparisons.append({'scope':scope,'region':region,'source':system,'metric':name,'cps_value':value.estimate,'cps_se':value.se_sampling,'source_value':ref[j]*mult,'raw_pct_difference':100*(value.estimate/(ref[j]*mult)-1)})
    for metric,key,mult in [('gross_wages','wages_millions',1e6),('wage_workers','workers_thousands',1000)]:
        for scope in scopes:
            value=components.query('scope==@scope and region=="US" and group=="all" and metric==@metric').iloc[0]
            ref=sources['awi'][key]*mult
            comparisons.append({'scope':scope,'region':'US','source':'awi_all_areas','metric':metric,'cps_value':value.estimate,'cps_se':value.se_sampling,'source_value':ref,'raw_pct_difference':100*(value.estimate/ref-1)})
    r,return_audit=returns(d)
    refbands,reftotal=source_tables(raw)
    taxmap={'returns':np.ones(len(r)),'agi':r.AGI.to_numpy(),'taxable_income':r.TAX_INC.to_numpy(),
            'income_tax_after_nonrefundable':r.FEDTAX_BC.to_numpy(),'total_wages':r.return_wages.to_numpy(),
            'federal_after_refundable':r.FEDTAX_AC.to_numpy()}
    taxrows=[]; totals=[]; rw=r[CW].to_numpy(float); bands=band(r.AGI)
    # IRS includes noncivilian/outside-household filers; show unrestricted survey and account scopes.
    for scope in scopes:
        eligible=np.ones(len(r),bool) if scope=='all_survey_persons' else (r.civilian if scope=='civilian' else r.civilian&r.household).to_numpy()
        for name,v in taxmap.items():
            total=summary(v[eligible]@rw[eligible]); reference=reftotal.get(name)
            totals.append({'scope':scope,'metric':name,**total,'irs_value':reference,'raw_pct_difference':100*(total['estimate']/reference-1) if reference else None})
            for i in range(19):
                keep=eligible&(bands==i)
                taxrows.append({'scope':scope,'band':i,'metric':name,**summary(v[keep]@rw[keep])})
    taxbands=pd.DataFrame(taxrows).merge(refbands,on=['band','metric'],how='left',validate='many_to_one')
    taxbands['raw_pct_difference']=100*(taxbands.estimate/taxbands.irs_value-1)
    for scope in scopes:
        for metric in taxmap:
            found=taxbands.query('scope==@scope and metric==@metric').estimate.sum()
            expected=next(t['estimate'] for t in totals if t['scope']==scope and t['metric']==metric)
            np.testing.assert_allclose(found,expected,rtol=1e-12,atol=.01)
    # Statutory coverage sensitivity only: no estimated exemption probability or adjustment.
    # Existing 2024 ledger maximum exposure to removing OASDI from all government-longest-job wages.
    current=args.source_root/'infra/immigration-fiscal/admin_tax_checks_2026_09_19/derived/group_components.csv'
    old=pd.read_csv(current)
    exposure=old.query('metric=="government_longest_job_oasdi_base"').copy()
    exposure['one_side_oasdi_ceiling_dollars']=.062*exposure.value
    exposure['applied_correction']=0.0
    prior_tax=pd.read_excel(raw/'22in12ms.xls',header=None)
    prior_wage=pd.read_excel(raw/'22in14ar.xls',header=None)
    assert 'Tax Year 2022' in prior_tax.iloc[0,0] and 'Tax Year 2022' in prior_wage.iloc[0,0]
    assert prior_tax.iloc[8,10]==2098923017 and prior_wage.iloc[8,6]==9738950972
    refinement=pd.DataFrame([{'metric':'wages','pub4801_p9_mislabeled_2023':9738950972000,'verified_2022_table':prior_wage.iloc[8,6]*1000,'verified_2023_table':reftotal['total_wages']},
                            {'metric':'after_nonrefundable_tax','pub4801_p9_mislabeled_2023':2098923017000,'verified_2022_table':prior_tax.iloc[8,10]*1000,'verified_2023_table':reftotal['income_tax_after_nonrefundable']}])
    exports={'cps2023_components':components,'ssa_comparisons':pd.DataFrame(comparisons),'irs_bands':taxbands,'irs_national':pd.DataFrame(totals),'government_coverage_ceiling':exposure,'irs_source_refinement':refinement}
    for name,frame in exports.items(): frame.to_csv(out/f'{name}.csv',index=False)
    paths=[HERE/'builder.py',HERE/'common.py',HERE/'ssa_sources.json',HERE/'source_lock.json',*[raw/f for f in ['asecpub24csv.zip','asec2024_ddl_pub_full.pdf','2024_replicates.docx','23in12ms.xls','23in14ar.xls','22in12ms.xls','22in14ar.xls','p4801.pdf']],current]
    audit={'income_year':2023,'calibration_applied':False,'return_construction':return_audit,'source_hashes':{str(p):sha(p) for p in paths},
           'outputs':{name:sha(out/f'{name}.csv') for name in exports},
           'limits':['CPS modeled returns are not observed IRS filing; AGI and statutory coverage are modeled','IRS taxable wages differ from CPS gross wage; return-weighted wages differ from person-weighted totals','OASDI all-covered proxy, HI coverage and multiple-employer treatment remain unresolved','SSA public state numbers are rounded preliminary sample estimates; US subtractsPR and other/unknown, not institutions/ArmedForces','No target-specific administrative tax calibration identified; zero adjustment applied, not evidence true bias is zero']}
    (out/'audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print(pd.DataFrame(totals).query('scope=="civilian"')[['metric','estimate','irs_value','raw_pct_difference']].to_string(index=False),flush=True)
    print(pd.DataFrame(comparisons).query('scope=="civilian" and region=="US"')[['source','metric','raw_pct_difference']].to_string(index=False),flush=True)

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--source-root',type=Path,required=True); p.add_argument('--raw',type=Path,default=HERE/'_cache'); p.add_argument('--out',type=Path,default=HERE/'derived')
    run(p.parse_args())
