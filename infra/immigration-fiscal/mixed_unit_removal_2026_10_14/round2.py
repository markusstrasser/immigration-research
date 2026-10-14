#!/usr/bin/env python3
"""Round-2 integration: replace item5b and D once; retain every round-1 control.

Native-First: consumes canonical survivor kernels and the frozen case evaluator.
This module is called by removal.py, not a second competing account engine.
"""
from pathlib import Path
import json
import subprocess
import numpy as np
import pandas as pd

LANE=Path(__file__).resolve().parent
OUT=LANE/'derived'
CACHE=LANE/'_cache'
GENS=('G1','G2','G3+')
SNAP_FULL_ARMS=tuple(f'SNAP_{shelter}_observed_{takeup}_takeup' for shelter in ('zero','cap') for takeup in ('low','high'))


def load_terms(command,path):
    completed=subprocess.run(command,check=True,capture_output=True,text=True)
    (CACHE/(Path(command[4]).stem+'_round2.log')).write_text(completed.stdout)
    with np.load(path,allow_pickle=False) as archive:
        return {key:archive[key].copy() for key in archive.files}


def snapshots(c,values):
    return {'bn':float(values[:,0].sum()),'se_bn':c.sdr(values.sum(axis=0)),
            'by_generation_bn':values[:,0].tolist(),
            'by_generation_se_bn':[c.sdr(v) for v in values]}


def full_snap_arms(terms):
    missing=set(SNAP_FULL_ARMS)-set(terms)
    if missing:
        raise ValueError('[BLOCKED] complete SNAP arms missing: '+str(sorted(missing)))
    return {key:terms[key] for key in SNAP_FULL_ARMS}


def extend(m,c,x,d,case,federal,state,benefit,consumption):
    resource=m.load_module(LANE/'resource_keys.py','round2_resource')
    own_income,*_=m.disposable_income(d,x['R'],x['P'])
    resources=resource.compute(d,x,case,own_income)
    members=m.load_module(LANE/'membership.py','round2_membership')
    membership=members.compute(c,x,d,case)
    membership_details=members.write(c,membership)
    y,masks=members.expanded_context(c,x,d,case,latent_only=True)
    expanded=m.federal_removal(c,y,y['d'])
    state_kernel=m.load_module(LANE/'state_tax.py','round2_expanded_state')
    expanded_state=state_kernel.compute(y['d'],y['R'],y['P'],y['base'],y['W'],y['union'],y['gen'],y['flag'],y['onbooks'],y['model'],
                         civ=y['civ'],refiling={'own':expanded['own'],'dep_counts':expanded['counts'],
                                               'R':expanded['afterR'],'owner':expanded['owner'],
                                               'before_input':expanded['before_input'],'after_input':expanded['after_input']})
    latent_tax=(expanded['M1']+expanded['M3']+expanded_state['M2'])-(federal['M1']+federal['M3']+state['M2'])
    # Child-credit transport on observed latent children is replaced by their
    # nonlinear linked-return computation, rather than counted on both routes.
    projection=membership['terms']['M6_remove_roster_lineage_credit_projection']
    M6=latent_tax+projection
    # Keep the literal all-biological-child rule beside the fixed-lineage arm:
    # some observed children fall outside the frozen addition's source universe.
    # Their own costs are not silently inserted into the fixed 42.75M account.
    full_context=membership['context']
    full_federal=m.federal_removal(c,full_context,full_context['d'])
    full_M6_tax=(full_federal['M1']+full_federal['M3'])-(federal['M1']+federal['M3'])+projection
    tax=m.load_module(LANE/'tax_corrections.py','round2_tax_corrections')
    tax.verify_sources()
    kernel=m.load_module(LANE/'state_tax.py','round2_tax_kernel')
    eitc=tax.assert_eitc_used(kernel)
    high=tax.federal_high_agi(c,x,d,federal,removal_module=m)
    tax.write_results(c,federal,high,eitc)
    # Corrected D already sits inside M1+M3 on the observed union. Extend only
    # the unlocated remainder of the added G3-priced universe.
    Dadded=members.transport_added(case,federal['D_corrected'],membership['remaining_added_g3'])
    pension=m.load_module(LANE/'pensions.py','round2_pensions')
    pensions=pension.compute(c,x,d,case)
    pension_details=pension.write(c,pensions)
    healthpath=CACHE/'health_arrays.npz'
    health=load_terms(['uv','run','--no-project','python3',str(LANE/'health.py'),
                      '--arrays-out',str(healthpath)],healthpath)
    healthmeta=json.loads((OUT/'health_results.json').read_text())
    latentpath=CACHE/'health_latent_arrays.npz'
    health_latent=load_terms(['uv','run','--no-project','python3',str(LANE/'health.py'),
                             '--membership','latent','--arrays-out',str(latentpath),
                             '--out',str(OUT/'health_latent_results.json')],latentpath)
    snappath=CACHE/'snap_arm_arrays.npz'
    snap=load_terms(['uv','run','--no-project','python3',str(LANE/'snap_arm.py'),
                    '--arrays-out',str(snappath)],snappath)
    snapmeta=json.loads((OUT/'snap_arm_results.json').read_text())
    snaplatentpath=CACHE/'snap_arm_latent_arrays.npz'
    snap_latent=load_terms(['uv','run','--no-project','python3',str(LANE/'snap_arm.py'),
                    '--membership','latent','--arrays-out',str(snaplatentpath),
                    '--out',str(OUT/'snap_arm_latent_results.json')],snaplatentpath)
    fixed={'M1_federal':federal['M1'],'M2_state':state['M2'],'M3_refunds':federal['M3'],
           'M5_consumption':consumption['M5'],'M5_owner_property':resources['terms']['modeled_owner_property'],
           'M5_SNAP_key':resources['terms']['snap'],'M5_housing_key':resources['terms']['housing_subsidies'],
           'M6_biological_children':M6,'D_added_residual':Dadded}
    diagnostic={'D_corrected_union':federal['D_corrected'],'M1_high_AGI':high['M1_high_agi'],
                'M6_latent_nonlinear_tax':latent_tax,'M6_remove_old_projection':projection,
                'M6_all_biological_federal_tax_arm':full_M6_tax,
                **{'membership_'+k:v for k,v in membership['terms'].items()},
                **pensions['terms'],**{'health_'+k:v for k,v in health.items()},
                **{'health_latent_'+k:v for k,v in health_latent.items()},
                **{'SNAP_'+k:v for k,v in snap.items()},
                **{'SNAP_latent_'+k:v for k,v in snap_latent.items()}}
    benefit_interactions={**{'M6_benefit_'+k:health_latent[k]-health[k] for k in ('Medicaid_low','Medicaid_high','ACA_low','ACA_high')},
                          **{'M6_benefit_'+k:snap_latent[k]-snap[k] for k in SNAP_FULL_ARMS}}
    diagnostic.update(benefit_interactions)
    recommendation={
        'M1_federal':'arm: own-survivor flags/cell and filing status are measurement corrections; unobserved deductions remain conditional',
        'M2_state':'arm: state-calibrated own-return recomputation; income/deduction transport conditional',
        'M3_refunds':'arm: solved with M1; EITC operator repair is a measurement correction',
        'M5_consumption':'arm: own disposable resources are an explicit allocation rule',
        'M5_owner_property':'arm: applies same resource rule to owner unit',
        'M5_SNAP_key':'arm separately; exact baseline interaction removes it from solved SNAP removal',
        'M5_housing_key':'arm: reported housing pool reallocated, rent and eligibility responses held',
        'M6_biological_children':'arm: biological link correction adopted in arm; priced universe stays fixed and roster projection removed once',
        'D_added_residual':'arm: G3 transport on unlocated added people; white amount held at zero',
        'Medicaid_CHIP':'arm: statutory household/eligibility plus empirical takeup and primary-source cost bridge',
        'ACA':'arm: enhanced schedule, enrollment and premium proxy; rule-based bounded estimate',
        'pension':'arm only; one-earner upper model, no measured cash increment',
        'weight_artifact':'reject +1.44bn headline edit; personal allocation already excludes artifact; enforce conservation',
        'duplicate_child_1_033':'reject blanket subtraction; claimant carrier and added-child own cost do not establish that duplication'}
    entries=[]
    vectors={}
    old_parts=m.original_item_parts(x)
    old_item=old_parts['receipts']+old_parts['spending']
    full_old_item=old_item+members.transport_added(case,old_item)
    for method in ('set','cash'):
        for end in (0,1):
            evalcase=case['evaluated'][method][end]
            owner_response=next(v['response'] for v in evalcase['receipts'] if v['id']=='modeled_owner_property')
            for key,value in fixed.items():
                vector=value*(owner_response if key=='M5_owner_property' else 1.)
                vectors[(method,end,key)]=vector
                entries.append({'method':method,'end':('low','high')[end],'component':key,
                                'recommendation':recommendation[key],**snapshots(c,vector)})
            # Take-up variants are alternatives. Min/max define a model envelope,
            # not a confidence interval; sampling SE retains their covariance.
            candidates={}
            for hname in ('Medicaid_low','Medicaid_high'):
                for aname in ('ACA_low','ACA_high'):
                    for sname,sv in full_snap_arms(snap_latent).items():
                        hvec=health_latent[hname]+health_latent[aname]
                        # The M5 SNAP key is an attribution of pre-removal dollars;
                        # the solved survivor benefit uses its matching nonmember
                        # baseline, so this adjustment cancels that one key.
                        interaction=-fixed['M5_SNAP_key']
                        base=sum(vectors[(method,end,k)] for k in fixed)
                        candidates[hname+'|'+aname+'|'+sname]=base+sv+hvec+interaction
                        independent=sum(vectors[(method,end,k)] for k in fixed if k!='M5_SNAP_key')+sv+hvec
                        m.gate('round2_solved_SNAP_allocation_cancels_'+method+str(end)+hname+aname+sname,
                               np.max(abs(candidates[hname+'|'+aname+'|'+sname]-independent))<1e-9)
            m.gate('round2_bounded_stack_has_observed_takeup_arms',bool(candidates))
            lowname=min(candidates,key=lambda n:float(candidates[n][:,0].sum()))
            highname=max(candidates,key=lambda n:float(candidates[n][:,0].sum()))
            for label,name in [('bounded_low',lowname),('bounded_high',highname)]:
                v=candidates[name]
                vectors[(method,end,label)]=v
                entries.append({'method':method,'end':('low','high')[end],'component':label,
                                'arm':name,'recommendation':'unified conditional removal arm; frozen v7 plus this delta',
                                'case_total_bn':case['bands'][method][end]+float(v[:,0].sum()),**snapshots(c,v)})
                hname,aname,sname=name.split('|')
                cross=benefit_interactions['M6_benefit_'+hname]+benefit_interactions['M6_benefit_'+aname]+benefit_interactions['M6_benefit_'+sname]
                vectors[(method,end,label+'_membership_benefit_interaction')]=cross
                entries.append({'method':method,'end':('low','high')[end],'component':label+'_membership_benefit_interaction',
                                'arm':name,'recommendation':'adopt interaction accounting inside chosen arm; latent-child departures change survivors benefits',**snapshots(c,cross)})
            if method=='set':
                v=candidates[highname]+pensions['terms']['pension_reverse_max_model']
                vectors[(method,end,'bounded_high_plus_pension_model')]=v
                entries.append({'method':method,'end':('low','high')[end],'component':'bounded_high_plus_pension_model',
                                'arm':highname,'recommendation':'beside: historical pension-model upper family arm',
                                'case_total_bn':case['bands'][method][end]+float(v[:,0].sum()),**snapshots(c,v)})
            for key in ('Medicaid_low','Medicaid_high','ACA_low','ACA_high'):
                value=health[key]
                vectors[(method,end,key)]=value
                entries.append({'method':method,'end':('low','high')[end],'component':key,
                                'recommendation':recommendation['ACA' if key.startswith('ACA') else 'Medicaid_CHIP'],**snapshots(c,value)})
            for key,value in snap.items():
                vectors[(method,end,key)]=value
                entries.append({'method':method,'end':('low','high')[end],'component':key,
                                'recommendation':('arm: statutory SNAP with observed-cell takeup and shelter band' if key in SNAP_FULL_ARMS
                                                  else 'diagnostic component only; newly eligible/ineligible separately, never a complete SNAP arm'),**snapshots(c,value)})
            replacement=full_old_item+sum(fixed[k] for k in ('M1_federal','M2_state','M3_refunds','M6_biological_children','D_added_residual'))
            vectors[(method,end,'tax_replacement_item5b_and_D')]=replacement
            entries.append({'method':method,'end':('low','high')[end],'component':'tax_replacement_item5b_and_D',
                            'recommendation':'replacement item, not an additional change from v7; subtract old item5b first',**snapshots(c,replacement)})
            interaction=-fixed['M5_SNAP_key']
            vectors[(method,end,'M4_SNAP_baseline_interaction')]=interaction
            entries.append({'method':method,'end':('low','high')[end],'component':'M4_SNAP_baseline_interaction',
                            'recommendation':'adopt accounting identity in solved removal; cancels M5 SNAP key arm',**snapshots(c,interaction)})
            vectors[(method,end,'M6_all_biological_federal_tax_arm')]=full_M6_tax
            entries.append({'method':method,'end':('low','high')[end],'component':'M6_all_biological_federal_tax_arm',
                            'recommendation':'arm beside fixed lineage: all biological departures, including source-definition conflicts; own costs of outside-definition children held, not newly booked',**snapshots(c,full_M6_tax)})
    for key,value in diagnostic.items():
        vectors[('diagnostic',0,key)]=value
    repl=[]
    for (method,end,name),value in vectors.items():
        m.gate('round2_finite_'+name,bool(np.isfinite(value).all()))
        for g,label in enumerate(GENS):
            repl.append({'method':method,'end':('low','high')[end],'component':name,'generation':label,
                         **{f'r{r}':value[g,r] for r in range(161)}})
    pd.DataFrame(repl).to_csv(OUT/'round2_replicates.csv',index=False,lineterminator='\n',float_format='%.15g')
    frame=pd.DataFrame(entries)
    frame.to_csv(OUT/'round2_results.csv',index=False,lineterminator='\n',float_format='%.12f')
    details={'frame':'identified union and fixed 42.75M priced lineage; located latent children replace unlocated projection, not added own costs',
             'replacement_rule':'M1/M3 subtract union item5b once; retain existing unlocated crossing-credit projection; add corrected D only on residual unlocated G3 people; do not add old D',
             'recommendations':recommendation,'membership':membership_details,'resource_keys':resources['details'],
             'tax_high_AGI':high['details'],'EITC_actual_kernel':eitc,'pensions':pension_details,
             'health':healthmeta,'SNAP':snapmeta,'results':entries,
             'interaction_rule':'M1/M2/M3 solve one after-return; latent membership solved jointly in federal returns; health uses latent departure mask; M5 SNAP reallocation cancels its changed M4 baseline. No after-tax consumption behavioral response assumed.',
             'health_cost_vintage':'explicit primary-cost bridge; do not label older group costs observed CMS2024 group costs',
             'headline_adoption':'recommend the concrete corrections; publish full modeled arm rather than adopt it as measured outcome'}
    (OUT/'round2_summary.json').write_text(json.dumps(details,indent=2,allow_nan=False)+'\n')
    return details


def report(details,case):
    items=details['results']
    def rows(method,end,component):
        return next(v for v in items if v['method']==method and v['end']==end and v['component']==component)
    bands={method:{arm:[rows(method,end,arm) for end in ('low','high')]
                   for arm in ('bounded_low','bounded_high')} for method in ('set','cash')}
    lines=['**Verdict:** Round 2 supplies a bounded unified removal arm, replacing item 5b and D once. Adopt the weight, survivor-record and EITC corrections; retain the tax-input, own-resource, health-takeup, added-person and pension assumptions as arms. [CALCULATION: `round2.py` → `derived/round2_summary.json`]',
           '', '| Unified removal, $bn | Low v7 end | High v7 end |', '|---|---:|---:|']
    for method in ('set','cash'):
        for arm in ('bounded_low','bounded_high'):
            a,b=bands[method][arm]
            lines.append(f"| {method}, {arm} | {a['case_total_bn']:.3f} (Δ{a['bn']:+.3f}, SE {a['se_bn']:.3f}) | {b['case_total_bn']:.3f} (Δ{b['bn']:+.3f}, SE {b['se_bn']:.3f}) |")
    lines+=['','The low/high model rows vary takeup and shelter within each fixed v7 end specification 16 / 11. They are conditional model envelopes, not sampling confidence intervals. Set and cash have the same current tax/transfer/key adjustments; the pension model upper arm is beside the set only. [ASSUMPTION] [FRAMING-SENSITIVE]','',
            '| One change from v7, $bn | Set low / high | Cash low / high | SE low / high | Recommendation |',
            '|---|---:|---:|---:|---|']
    keys=['M1_federal','M2_state','M3_refunds','M6_biological_children','D_added_residual','M5_consumption','M5_owner_property','M5_SNAP_key','M4_SNAP_baseline_interaction','M5_housing_key','Medicaid_low','Medicaid_high','ACA_low','ACA_high','tax_replacement_item5b_and_D']
    keys+=sorted({v['component'] for v in items if 'observed' in v['component']})
    keys+=['bounded_low_membership_benefit_interaction','bounded_high_membership_benefit_interaction','M6_all_biological_federal_tax_arm']
    for key in keys:
        a,b=rows('set','low',key),rows('set','high',key)
        ca,cb=rows('cash','low',key),rows('cash','high',key)
        lines.append(f"| {key} | {a['bn']:+.6f} / {b['bn']:+.6f} | {ca['bn']:+.6f} / {cb['bn']:+.6f} | {a['se_bn']:.6f} / {b['se_bn']:.6f} | {a['recommendation']} |")
    lines+=['','The tax replacement row is the new item amount, not an additional v7 delta. All other standalone rows are one change from v7. Health and SNAP standalone rows use the identified-union departures; the unified rows additionally include their explicit membership-benefit interaction. SEs sample all 160 signed CPS SDR replicates, conditional on policy/cost/calibration assumptions, not an uncertainty estimate for those assumptions. [CALCULATION / ASSUMPTION]','',
            'SNAP key allocation is shown as a one-change arm. Its negative baseline interaction is included in every unified row; adding it without that interaction would double count attribution. `round2_replicates.csv` stores generation vectors and the exact covariance-preserving stack. [CALCULATION]','',
            'The original item-5b and D controls remain byte-identical under `derived/positive_control/`; old D is a control and is not added to any unified row. The original conditional first-pass result is preserved in [round1-result.md](round1-result.md). All original diagnostic arms remain in `derived/results.csv` and `derived/replicates.csv`. [DATA]','',
            '## Membership and credit carriers','',
            f"The own-parent biological rule identifies {details['membership']['extra_children']/1e6:.6f}M children outside the union; {details['membership']['step_only_children_stay']/1e6:.6f}M step-only children stay. {details['membership']['latent_children_with_two_US_parents']/1e6:.6f}M fit the frozen latent universe. They replace its modeled crossing-credit projection once (not their own costs). The remaining outside-definition children are priced as an all-biological federal-tax arm beside the fixed-lineage result; inserting their own costs into the 42.75M headline would silently change its population. [CALCULATION / ASSUMPTION]",
            '', 'Every counted child is assigned to exactly one partition: identified union, located latent subset, or unlocated residual of the fixed addition. This is an explicit reconciliation rule, not an individual crosswalk observed in the aggregate loss estimate. `derived/membership.json` includes count closure, raw parent-field conflicts, generation/class assignment and nonmember claimants. The literal all-biological rule stays visible beside it. [DATA / ASSUMPTION]','',
            'The blanket −$1.033bn subtraction is rejected: a claimant credit for a child is not that child’s own refundable-credit record. The located latent children have no own-record CTC/ACTC/EITC; the nonzero crossing-credit projection that is replaced is explicitly traced by receipt/spending side. The reverse-credit diagnostic is not added a second time to the jointly solved returns. [CALCULATION: `membership.py`; `derived/membership.json`]','',
            '## Primary-source health arm and costs','',
            'See [health-result.md](health-result.md), `inputs/health*`, and `derived/health_results.json`. Health is priced as an arm; the primary expenditure/enrollment bridge and its vintage are explicit. Each state/category transition and newly eligible/ineligible count is in that output. [SOURCE / CALCULATION]','',
            '## Keys and weight conservation','',
            f"Own-resource splitting is an arm; all-zero own resources retain equal shares. The original civilian weighted key total stays fixed in every unit and all 161 columns. The worst closure discrepancy is {details['resource_keys']['unit_closure_max_bn']:.3g}bn. The old within-member unweighted sharing artifact is +{details['resource_keys']['four_person_line_artifact_bn']:.6f}bn; v7's personal allocation excludes it, so no extra +$1.44bn is booked. The four affected person-key metrics each pass the within-member identity in all 161 columns. [CALCULATION: `resource_keys.py`; `derived/round2_summary.json` `resource_keys`]",'',
            '## Pension and federal-tax alternatives','',
            'See [pensions-result.md](pensions-result.md) and [tax-corrections-result.md](tax-corrections-result.md). The high-AGI federal scenario is recomputed directly, not the former scalar; both headline ends use the ordinary key. The pension inputs support a conditional one-earner family-model envelope, not a measured lifetime-spouse entitlement correction or new cash payment. [CALCULATION / ASSUMPTION]','',
            f"The pension zero-current-earnings proxy is +{details['pensions']['terms']['pension_reverse_zero_current_earnings_proxy']['bn']:.6f}bn at both set ends (SE {details['pensions']['terms']['pension_reverse_zero_current_earnings_proxy']['se_bn']:.6f}); the historical-model upper is +{details['pensions']['terms']['pension_reverse_max_model']['bn']:.6f}bn (SE {details['pensions']['terms']['pension_reverse_max_model']['se_bn']:.6f}). Both are arms, with primary pension costs held in set/cash. Their hypothetical benefit timing cannot be inserted as this year's cash. [CALCULATION / ASSUMPTION]",'',
            'The remaining white-priced added people take zero crossing credits and D under the existing case rule, explicitly an assumption. Located biological children receive their observed linked-return treatment regardless of their aggregate G3/white price blend. The reviewer’s ≤$0.25bn white-credit amount is a sensitivity claim, not a verified hard bound on D; adding $0.25bn beside the reported arm moves each endpoint by that amount. [ASSUMPTION / INFERENCE]','',
            '## Reproduction and scope','',
            'Run `removal.py` then the full lane pytest command with `-p no:cacheprovider`; `RUN_LOG.md` records actual return codes and `rerun_lane.py` IDENTICAL receipts. Every computation is deterministic, retains 160 signed SDR replicates, and fails on source, weight or closure drift. No frozen-case or other-lane source is edited. No Git metadata is written. [CALCULATION]','',
            'This LLM-based political research can inherit framing bias; recommendations above separate numerical corrections from counterfactual assumptions. [INFERENCE]','']
    (LANE/'RESULT.md').write_text('\n'.join(lines))
    return bands
