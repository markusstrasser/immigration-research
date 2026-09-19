"""Uncalibrated CPS2024 earnings/payroll diagnostics against pinned primary anchors."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import sys
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
TARGET = 'mexican_observed_total'
PARAMETERS = json.loads((HERE/'sources.json').read_text())['payroll_parameters']


def sha(path):
    with Path(path).open('rb') as handle:
        return hashlib.file_digest(handle, 'sha256').hexdigest()


def payroll_proxy(wages, business_profit, farm_profit, cap=None):
    """Statutory all-covered proxy, not an observed payment or CPS FICA replacement."""
    cap = PARAMETERS['oasdi_cap'] if cap is None else cap
    oasdi, hi = PARAMETERS['oasdi_one_side_rate'], PARAMETERS['hi_one_side_rate']
    wage = np.maximum(np.asarray(wages, float), 0)
    se = PARAMETERS['se_net_factor'] * np.maximum(np.asarray(business_profit, float)+np.asarray(farm_profit, float), 0)
    se = np.where(se >= PARAMETERS['se_threshold'], se, 0)
    wbase = np.minimum(wage, cap)
    sebase = np.minimum(se, np.maximum(cap-wbase, 0))
    return dict(gross_wages=wage, wage_earners=(wage > 0).astype(float),
                wage_oasdi_base_proxy=wbase, self_employment_net_proxy=se,
                self_employment_oasdi_base_proxy=sebase,
                oasdi_base_proxy=wbase+sebase,
                employer_oasdi_proxy=oasdi*wbase, employer_hi_proxy=hi*wage,
                employee_and_self_payroll_proxy=oasdi*wbase+hi*wage+2*oasdi*sebase+2*hi*se,
                both_sides_payroll_proxy=2*oasdi*(wbase+sebase)+2*hi*(wage+se))


def estimate(vector, weights):
    values = np.asarray(vector) @ weights
    return float(values[0]), float(np.sqrt(4/160*np.square(values[1:]-values[0]).sum()))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--source-root', type=Path, required=True)
    ap.add_argument('--out', type=Path, default=HERE/'derived')
    args = ap.parse_args()
    root, out = args.source_root.resolve(), args.out.resolve()
    fiscal = root/'infra/immigration-fiscal'
    helper = fiscal/'education_origin_fiscal_2026_09_19/builder.py'
    spec = importlib.util.spec_from_file_location('admin_tax_evidence', helper)
    evidence = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(evidence)
    A, AL, arrival = evidence.configure(root)
    for field in ['SEMP_VAL','FRSE_VAL','WECLW']:
        if field not in A.ext.base.PERSON:
            A.ext.base.PERSON.append(field)
    cps = fiscal/'gen_ledger_extension_2026_09_16/_cache/asecpub25csv.zip'
    if sha(cps) != A.ext.CPS_SHA:
        raise ValueError('Unreviewed CPS source change')
    state = A.ext.build(argparse.Namespace(cps_zip=cps))
    d, w = state['d'], state['person_weights']
    civilian = (d.PRPERTYP.eq(2)|d.A_AGE.lt(15)).to_numpy()
    target = np.logical_or.reduce([state['group'][g] for g in AL.TARGETS]) & civilian
    groups = {TARGET:target,'other_residents':civilian & ~target,'national_civilian':civilian}
    shared, personal, _ = A.matrices(state)
    values = payroll_proxy(d.WSAL_VAL,d.SEMP_VAL,d.FRSE_VAL)
    values.update(population=np.ones(len(d)),
                  business_profit=d.SEMP_VAL.to_numpy(), farm_profit=d.FRSE_VAL.to_numpy(),
                  fica_cps=d.FICA.to_numpy(), federal_before_refundable=d.FEDTAX_BC.to_numpy(),
                  federal_after_refundable=d.FEDTAX_AC.to_numpy(),
                  eitc=d.EIT_CRED.to_numpy(), actc=d.ACTC_CRD.to_numpy(),
                  state_after_credits=d.STATETAX_A.to_numpy(),
                  government_longest_job_wages=np.where(d.WECLW.eq(6),values['gross_wages'],0),
                  government_longest_job_oasdi_base=np.where(d.WECLW.eq(6),values['wage_oasdi_base_proxy'],0))
    values['cps_plus_employer_payroll'] = d.FICA.to_numpy()+personal[:,3]
    values['modeled_employer_payroll'] = personal[:,3]
    # Native scalar oracle, independent of vectorized cap/self-employment formula.
    for i in np.linspace(0,len(d)-1,250,dtype=int):
        wage=max(float(d.WSAL_VAL.iloc[i]),0)
        net=.9235*max(float(d.SEMP_VAL.iloc[i]+d.FRSE_VAL.iloc[i]),0)
        net=net if net>=400 else 0
        base=min(wage,168600)+min(net,max(168600-min(wage,168600),0))
        if abs(base-values['oasdi_base_proxy'][i])>1e-8:
            raise ValueError('Independent scalar payroll oracle failed')
    np.testing.assert_allclose(values['modeled_employer_payroll'],values['employer_oasdi_proxy']+values['employer_hi_proxy'],atol=1e-8)
    np.testing.assert_allclose(values['federal_after_refundable'],values['federal_before_refundable']-values['eitc']-values['actc'])
    rows=[]
    for allocation in ['personal','shared']:
        for name, vector in values.items():
            if allocation=='shared':
                unit=np.bincount(state['index'],weights=vector,minlength=state['n_units'])
                vector=A.ext.allocate(unit,state['index'],np.ones(len(d),bool),state['n_units'])
            for group,mask in groups.items():
                value,se=estimate(vector[mask],w[mask])
                rows.append(dict(allocation=allocation,group=group,metric=name,value=value,se_sampling=se,unit='persons' if name in ['population','wage_earners'] else 'dollars'))
    totals=pd.DataFrame(rows)
    p=totals.pivot(index=['allocation','metric'],columns='group',values='value')
    np.testing.assert_allclose(p.national_civilian,p[TARGET]+p.other_residents,atol=.01)
    anchors=pd.read_csv(fiscal/'macro_closure_2026_09_19/derived/account_components.csv')
    for allocation in ['shared','personal']:
        for group in groups:
            v=totals.query('allocation==@allocation and group==@group').set_index('metric').value
            old=anchors.query('allocation==@allocation and group==@group').set_index('component')
            np.testing.assert_allclose(v.federal_after_refundable+v.fica_cps+v.state_after_credits,old.loc['tax','receipts_bn']*1e9,atol=.1)
            np.testing.assert_allclose(v.modeled_employer_payroll,old.loc['employer','receipts_bn']*1e9,atol=.1)
            np.testing.assert_allclose(v.population,old.population.iloc[0],atol=.01)
    sources=json.loads((HERE/'sources.json').read_text())
    baseline=totals.query('allocation=="personal" and group=="national_civilian"').set_index('metric')
    # Different aggregation route from NumPy dot: independently check weighted wage sums.
    oracle=pd.DataFrame({'target':target,'civilian':civilian,'weighted_wage':d.WSAL_VAL*w[:,0]}).query('civilian').groupby('target').weighted_wage.sum()
    for group,flag in [(TARGET,True),('other_residents',False)]:
        observed=totals.query('allocation=="personal" and group==@group and metric=="gross_wages"').value.iloc[0]
        np.testing.assert_allclose(observed,oracle.loc[flag],rtol=1e-13,atol=.01)
    comparisons=[]
    for record in sources['benchmarks']:
        row=baseline.loc[record['metric']]
        comparisons.append(dict(**record,model_value=row.value,model_sampling_se=row.se_sampling,
                                raw_difference=row.value-record['amount'],raw_pct_difference=100*(row.value/record['amount']-1),
                                interpretation='Unadjusted diagnostic; coverage/year differences prevent an equality test'))
    implications=[]
    for allocation in ['personal','shared']:
        part=totals.query('allocation==@allocation').pivot(index='metric',columns='group',values='value')
        for metric in part.index:
            a,b,n=part.loc[metric,[TARGET,'other_residents','national_civilian']]
            if n!=0:
                implications.append(dict(allocation=allocation,metric=metric,target_share=a/n,
                                         target_per_resident=a/part.loc['population',TARGET],
                                         other_per_resident=b/part.loc['population','other_residents']))
    refs={r['id']:r['amount'] for r in sources['benchmarks']}
    govt=baseline.loc['government_longest_job_oasdi_base','value']
    wage_gap=baseline.loc['wage_oasdi_base_proxy','value']-refs['ssa_wage_oasdi_base_2024_preliminary']
    diagnostic=dict(cps_mean_per_wage_earner=baseline.loc['gross_wages','value']/baseline.loc['wage_earners','value'],
                    ssa_awi_mean_from_rounded_totals=refs['ssa_awi_wages_2024']/refs['ssa_awi_workers_2024'],
                    cps_employee_self_payroll_minus_statutory_proxy=baseline.loc['fica_cps','value']-baseline.loc['employee_and_self_payroll_proxy','value'],
                    government_job_wage_oasdi_base=govt,
                    wage_base_gap_fraction_of_government_job_base=wage_gap/govt,
                    interpretation='Last ratio is a dimensional coverage requirement if the whole wage-base residual came from government-job earnings; not an estimated exemption share, not applied to taxes.')
    for group in groups:
        v=totals.query('allocation=="personal" and group==@group').set_index('metric').value
        diagnostic[group]=dict(wages_per_wage_earner=v.gross_wages/v.wage_earners,
                               federal_after_refundable_per_resident=v.federal_after_refundable/v.population,
                               cps_plus_employer_payroll_per_resident=v.cps_plus_employer_payroll/v.population,
                               source_tax_sum=v.federal_after_refundable+v.fica_cps+v.state_after_credits)
    paths=[Path(__file__),HERE/'sources.json',HERE/'test_builder.py',helper,cps,
           fiscal/'macro_closure_2026_09_19/builder.py',fiscal/'macro_closure_2026_09_19/derived/account_components.csv',
           fiscal/'gen_ledger_extension_2026_09_16/state_parameters.csv',
           root/'sources/immigration-fiscal/data/external/cps_asec_doc/asec2025_ddl_pub_full.pdf']
    for module in [A,AL,arrival,A.ext,A.ext.base]:
        paths.append(Path(module.__file__))
    out.mkdir(parents=True,exist_ok=True)
    exports={'group_components':totals,'benchmark_comparisons':pd.DataFrame(comparisons),'target_implications':pd.DataFrame(implications)}
    for name,frame in exports.items():
        frame.to_csv(out/f'{name}.csv',index=False)
    (out/'coverage_diagnostics.json').write_text(json.dumps(diagnostic,indent=2,allow_nan=False)+'\n')
    audit=dict(calibration_applied=False,price_year=2024,source_hashes={str(p):sha(p) for p in paths},
               outputs={**{k:sha(out/f'{k}.csv') for k in exports},'coverage_diagnostics':sha(out/'coverage_diagnostics.json')},
               checks=['canonical populations/tax/employer anchors','disjoint group conservation','refundable credit identity','250 scalar payroll oracles','independent pandas group wage sums','employer formula equality'],
               limitations=sources['limitations']+['All-covered payroll proxy excludes additional Medicare tax and cannot resolve government/exempt jobs, multiple-employer overpayments or noncovered earnings','CPS civilian household universe excludes institutions/territories and differs from annual tax/W2 universe','Shared earnings/earner counts are attributed resource-unit amounts, not counts of ethnic earners; use personal counts for labor-market interpretation'])
    (out/'audit.json').write_text(json.dumps(audit,indent=2,allow_nan=False)+'\n')
    print(pd.DataFrame(comparisons)[['id','model_value','amount','raw_pct_difference']].to_string(index=False))
    print(totals.query('allocation=="personal" and group==@TARGET')[['metric','value']].to_string(index=False))


if __name__=='__main__':
    main()
