"""Oct16 household allocation on fixed rosters and calibrated survey weights.

Native-First: replay the pinned original piece constructor through its existing
AST boundary. Keep the original source and all historical outputs read-only.
"""
from __future__ import annotations

import argparse
import ast
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import sys
import tempfile
import time

sys.dont_write_bytecode = True
import numpy as np
import pandas as pd
import pyarrow as pa

from oct16_statistics import summarize, require

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
sys.path.insert(0, str(FISCAL/'scripts'))
from adoption_gate import require_adopted
GENS = ('G1', 'G2', 'G3plus')
ENDS = ('low', 'high')
NEW_ITEMS = ('veterans_compensation', 'income_security_administration', 'public_college_response',
             'native_minor_calibration', 'coverage_tenure', 'consumption_tax_bases', 'one_rate',
             'health_residual_key', 'coverage_repricing')


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def read(path):
    return json.loads(path.read_text())


def json_write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, allow_nan=False)+'\n')


def csv_write(path, rows):
    pd.DataFrame(rows).to_csv(path, index=False, lineterminator='\n', float_format='%.12g')


def construct(lines, allocation, basis, accrual='flat', payroll='all', placement='band'):
    """Return the unchanged v8 constructor's locals before allocation or writes."""
    source = HERE/'households.py'
    pins = read(FISCAL/'generation_account_2026_09_24/inputs/pins.json')
    require(digest(source) == pins['within_group_distribution_2026_09_29/households.py'], 'original household source pin')
    spec = importlib.util.spec_from_file_location('oct16_original_households', source)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    tree = ast.parse(source.read_text(), filename=str(source))
    functions = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'main']
    require(len(functions) == 1, 'unique household constructor')
    fn = functions[0]
    expected = {'prod_parts','vec','rk','sk','medical','edu','v'}
    boundaries = [i for i,n in enumerate(fn.body) if isinstance(n,ast.Delete)
                  and {x.id for x in n.targets if isinstance(x,ast.Name)} == expected]
    require(len(boundaries) == 1, 'unique original piece construction boundary')
    fields = ['pieces','residual','d','W','rows_u','coverage_identified_weights','coverage_added_weights',
              'nonreporter','rounding_people','lab','lines']
    result = ast.Dict(keys=[ast.Constant(k) for k in fields],values=[ast.Name(k,ast.Load()) for k in fields])
    fn.body = fn.body[:boundaries[0]] + [ast.Return(result)]
    adapted = ast.fix_missing_locations(ast.Module(body=[fn],type_ignores=[]))
    exec(compile(adapted,str(source),'exec'),module.__dict__)
    # Only the checked in-memory scaffold is given its declared original identity.
    # The principal oct16 line export is neither changed nor misidentified.
    scaffold = {**lines, 'meta':{**lines['meta'], 'case':lines['meta']['v9']['scaffold_case']}}
    directory = HERE/'_cache/oct16'/('shared_allocation' if allocation == 'shared' else '')
    directory.mkdir(parents=True,exist_ok=True)
    with tempfile.NamedTemporaryFile(mode='w',dir=directory,suffix='.json',delete=False) as stream:
        json.dump(scaffold,stream)
        temporary = Path(stream.name)
    try:
        module.FAILS.clear()
        got = module.main('row4',case='oct15',allocation=allocation,basis=basis,lines_path=temporary,
                          accrual=accrual,payroll_base=payroll,placement=placement)
    finally:
        temporary.unlink(missing_ok=True)
    require(not module.FAILS,'original constructor gates: '+repr(module.FAILS))
    return module,got


def calibrated_factors(d, declaration):
    for value in (declaration,declaration['replicates'],declaration['cells'],declaration['builder']):
        require(digest(FISCAL/value['file']) == value['sha256'],'calibration source changed '+value['file'])
    factors = pd.read_parquet(FISCAL/declaration['file'],columns=['PH_SEQ','PPPOS','PRDTHSP','cell','central_member_factor']).set_index(['PH_SEQ','PPPOS'])
    identities = pd.MultiIndex.from_frame(d[['PH_SEQ','PPPOS']])
    joined = factors.reindex(identities)
    require(not joined.central_member_factor.isna().any(),'calibration identity join incomplete')
    replicas = read(FISCAL/declaration['replicates']['file'])['cells']
    out = np.ones((len(d),161))
    for cell, values in replicas.items():
        selected = joined.cell.eq(cell).to_numpy()
        for mexican,key in ((True,'mexican_rake_factor'),(False,'hispanic_reassignment_factor')):
            mask = selected & (joined.PRDTHSP.eq(1).to_numpy() if mexican else joined.PRDTHSP.gt(1).to_numpy())
            out[mask] = np.asarray(values[key])
    require(np.max(np.abs(out[:,0]-joined.central_member_factor.to_numpy())) < 1e-12,'central/replicate record factor agreement')
    require(np.isfinite(out).all() and (out>0).all(),'invalid calibrated factors')
    return out


def source_details(snapshot,piece,end):
    sys.path.insert(0,str(FISCAL/'coverage_bound_2026_10_14'))
    from export_pricing import component_metadata
    detail = component_metadata(snapshot,piece,end)
    if piece.get('completion_source'):
        population = 'completion'
    elif piece.get('native_child_source'):
        population = 'native'
    elif piece.get('state_price_source'):
        population={'identified':'original_union','latent':'added_lineage','native':'native'}[piece['state_price_source']['population']]
    else:
        population = 'engine'
    return {**detail,'population':population,'id':piece['id'],'cat':piece['cat'],'g':piece['g']}


def source_candidates(atom, originals):
    """Declared source coordinates locate the existing household driver."""
    side = atom['source_side']
    source = atom.get('capital_source_line') if atom.get('kind') == 'college_operating' else atom['source_line']
    side = 'capital' if atom.get('kind') == 'college_operating' else side
    college_proxy = atom['line'].startswith('oct16_college_operating:')
    if college_proxy:
        source,side=atom['line'].split(':',1)[1],'capital'
    scoped = [p for p in originals if p['g'] == atom['generation'] and p.get('source_side') == side]
    exact = [p for p in scoped if p['id'] == (source if college_proxy or atom.get('kind')=='college_operating' else atom['line'])]
    found = exact if exact else [p for p in scoped if p['source_line'] == source]
    population = atom['population']
    require(population in ('engine','completion','native','original_union','added_lineage','observed','coverage'),
            'unknown household source population '+population)
    if population == 'engine':
        found = [p for p in scoped if p['source_line'] == source and p['population'] in ('engine','original_union','added_lineage','native')]
    elif population == 'original_union':
        found = [p for p in found if p['population'] in ('engine','original_union')]
    elif population == 'added_lineage':
        found = [p for p in found if p['population'] in ('engine','added_lineage')]
    elif population in ('completion','native'):
        expected = 'native' if atom.get('profile')=='native_nonreporters' else population
        found = [p for p in found if p['population'] == expected]
    if atom.get('category') and population == 'observed' and not college_proxy:
        found = [p for p in found if p['cat'] == atom['category']]
    return found


def driver_parts(atom, originals, old_weight, factor):
    candidates = source_candidates(atom, originals)
    if not candidates:
        require(atom['source_side'] == 'post_engine', 'no declared household source driver '+json.dumps(atom))
        return []
    by_category = {}
    for p in candidates:
        cat = 'education_other' if atom.get('kind') == 'college_operating' or atom['line'].startswith('oct16_college_operating:') else p['cat']
        # Each original subpiece's own dollars determine its share. This retains
        # signed capital offsets and the source's school/college split.
        price = p['price']
        if atom['population']=='original_union' and p['population']=='engine':
            price=price*p['original_fraction']
        elif atom['population']=='added_lineage' and p['population']=='engine':
            price=price*p['latent_fraction']
        if atom['population']=='added_lineage' and atom.get('profile'):
            profiles=p['latent_profile_fractions']
            require(atom['profile'] in profiles,'unknown declared latent profile '+atom['profile'])
            price=price*profiles[atom['profile']]
        by_category.setdefault(cat,np.zeros_like(price))
        by_category[cat] += price
    if atom['population'] == 'observed':
        # Count changes affect existing records; no biological roster is changed.
        by_category = {cat:price*(factor-1)/factor for cat,price in by_category.items()}
    values = {cat:float(x @ (old_weight*factor)) for cat,x in by_category.items()}
    total = sum(values.values())
    if abs(total)<=1e-12 and atom['source_side']=='post_engine' and atom.get('economic_class') in ('unclassified_post_engine','unclassified_residual'):
        # Shared allocation has no item11 household price, while the declared
        # count-price kernel can carry its personal correction. No household
        # owner is identified for that explicitly unclassified post amount.
        require(not any(np.any(x) for x in by_category.values()),'nonzero unclassified post driver cancels; explicit allocation required')
        return []
    require(abs(total)>1e-12 or abs(atom['cost_bn'])<1e-12, 'zero signed source driver '+atom['source_piece'])
    return [(cat,values[cat]/total,x) for cat,x in by_category.items() if abs(values[cat])>1e-12]


def latent_profiles(age,lineage):
    counts,mixes=lineage['counts'],lineage['age_mix']['mixes']
    later=np.asarray(mixes['later'])*counts['later_losses']
    at_g3=np.asarray(mixes['g3_rate'])*counts['at_g3_rate']
    total=later+at_g3
    require((total>0).all(),'empty declared latent age band')
    bands=np.minimum(np.asarray(age)//5,len(total)-1)
    c3=lineage['c3']
    profiles={'lineage_later_g3':(later/total)[bands],
        'lineage_g3_rate_g3':((1-c3)*at_g3/total)[bands],
        'lineage_g3_rate_white':(c3*at_g3/total)[bands]}
    require(np.max(np.abs(sum(profiles.values())-1))<1e-12,'latent profile age weights do not close')
    return profiles


def reconcile_native(price, old_weight, new_weight, selected, declared_bn):
    """Only actual source repricing can alter a reweighted person's unit price."""
    natural=float(price[selected] @ (new_weight[selected]-old_weight[selected])/1e9)
    remainder=declared_bn-natural
    correction=np.zeros_like(price)
    if abs(remainder)>1e-12:
        factor=new_weight/old_weight
        driver=np.where(selected,price*(factor-1)/factor,0.)
        denominator=float(driver @ new_weight)
        require(abs(denominator)>1e-12,'native price reconciliation lacks a signed changed-record driver')
        correction=driver*(remainder*1e9/denominator)
        require(np.all(correction[factor==1]==0),'native reconciliation changes unaffected records')
        require(abs(correction @ new_weight/1e9-remainder)<1e-9,'native reconciliation weighted closure')
    return correction,natural,remainder


def labels_for(snapshot, rows):
    d = snapshot['d']
    household = d.PH_SEQ.to_numpy()[rows]
    source = pd.read_parquet(HERE/'_cache/oct15/households.parquet')
    table = source.set_index('PH_SEQ')
    require(set(household) <= set(table.index),'fixed household roster changed')
    labels = {'all':np.full(len(rows),'all'), 'own_generation':np.asarray(GENS)[snapshot['lab'][rows]]}
    for key in ('head_education','head_generation','head_age','state_group','children_in_household'):
        labels[key] = table[key].reindex(household).to_numpy()
    return household,labels


def calculate(lines, basis='set', allocation='personal', accrual='flat', payroll='all', unlocated_residual='retain', placement='band',control_item=None,adoption=None):
    """Calculate allocations without publishing; candidate probes remain unadmitted."""
    require(lines['meta']['case']=='main_case_2026_10_16','oct16 export identity')
    require(control_item is not None or 'health_residual_key' in lines['meta']['v9']['selected_items'],'final item21 missing')
    require(lines['meta']['v9'].get('control_item')==control_item,'full-source control selection mismatch')
    for name in ('source_payload','source_generation'):
        source = lines['meta']['v9'][name]
        require(digest(FISCAL/source['file'])==source['sha256'],'stale oct16 source export '+source['file'])
    require(payroll=='all' or accrual=='person','onbooks allocation requires person pension allocation')
    module,s = construct(lines,allocation,basis,accrual,payroll,placement)
    rows = s['rows_u']
    weights = s['W'][rows].copy()
    # Discard the original constructor's full-frame temporaries at exactly its
    # normal release boundary before allocating any calibration matrix.
    for key in ('prod_parts','vec','rk','sk','medical','edu','v','models','shares','use_parts','routes','carriers',
                'W_pub','w_labor','completion_jobs','completion_pension','alt','onbooks_key','onbooks'):
        s.pop(key,None)
    s['W'] = weights
    gc.collect()
    pa.default_memory_pool().release_unused()
    factors = calibrated_factors(s['d'].iloc[rows],lines['meta']['v9']['record_factors'])
    if 'native_minor_calibration' not in lines['meta']['v9']['selected_items']:
        factors.fill(1.)
    # Original latent descendants are constructed. Calibrate observed reporters
    # and observed nonreporting children, not the placed original latent stock.
    identified = s['coverage_identified_weights']
    added = s['coverage_added_weights']
    nonreporter = s['nonreporter'][rows]
    calibrated = identified*factors + added
    calibrated[nonreporter] = weights[nonreporter]*factors[nonreporter]
    effective_factor = calibrated[:,0]/weights[:,0]
    population = lines['meta']['population_v9']
    require(abs(calibrated[:,0].sum()+s['rounding_people']-population['without_coverage'])<1e-6,'calibrated located population')
    household,labels = labels_for(s,rows)
    original = {}
    original_fraction=identified[:,0]/weights[:,0]
    latent_fraction=added[:,0]/weights[:,0]
    latent_fraction[nonreporter]=0.
    profile_fractions=latent_profiles(s['d'].A_AGE.to_numpy()[rows],lines['meta']['lineage'])
    for end in ENDS:
        original[end] = []
        for p in s['pieces'][end]:
            driver = p['alt']['person'] if accrual=='person' and 'alt' in p else p['x']
            if payroll=='onbooks' and 'alt_tax' in p:
                driver = p['alt_tax']
            denominator = driver @ weights[:,0]
            require(denominator != 0 or p['bn'] == 0,'unassignable original driver '+p['id'])
            detail = source_details(s,p,end)
            original[end].append({**detail,'price':driver*(p['bn']*1e9/denominator) if denominator else np.zeros(len(rows)),
                                  'bn':p['bn'],'original_fraction':original_fraction,'latent_fraction':latent_fraction,
                                  'latent_profile_fractions':profile_fractions})
    # Keep only small, union-row vectors before statistics. Original constructor
    # has no writes; every retained source pin is still checked above.
    original_residual = s['residual']
    rounding = s['rounding_people']
    del s, identified, added, factors
    gc.collect()
    pa.default_memory_pool().release_unused()
    tables = {key:[] for key in ('net_positive_shares','concentration','household_balance_quantiles','control','category_means','item_controls','crossings','people_survey_misses','allocation_atoms','lineage_share_bounds','calibration_reconciliation')}
    controls = {'case':'oct16','basis':basis,'allocation':allocation,'control_item':control_item,'accrual_allocation':accrual,'payroll_allocation':payroll,'latent_placement':placement,'adoption':adoption,'admission':'final' if adoption is not None else 'candidate preparation only',
        'population':population,'ranking_weight':'mean calibrated member weight per fixed observed household; quantile members use their own calibrated person weights',
        'balance_rule':'unweighted sum of per-person dollar balances; conservation uses sum of person-weighted dollars, never mean household weight times household dollars',
        'allocation_rule':'original per-person prices preserved; direct source deltas priced on original source weights; intrinsic record-weight change counted once. Only the difference from declared native source parts is allocated on changed records; roster is fixed.',
        'uncertainty':'Point allocations only. No new conditional survey SE or total model SE computed by this adapter; earlier case SEs remain historical.',
        'unlocated_residual_policy':unlocated_residual,
        'item_controls':lines['meta']['v9']['controls_rule'],'tolerance_bn':1e-9,'gates':[]}
    hh_table = None
    for end in ENDS:
        base = {}
        base_original = {}
        for p in original[end]:
            base.setdefault(p['cat'],np.zeros(len(rows)))
            base_original.setdefault(p['cat'],np.zeros(len(rows)))
            base_original[p['cat']] += p['price']
            base[p['cat']] += p['price']
        increments = {item:{} for item in NEW_ITEMS}
        native_targets = {}
        residual = dict(original_residual[end])
        unlocated = {g:lines['generations'][g][end]['post_engine'].get('coverage',0.) for g in GENS}
        for atom in lines['union'][end]['v9_parts']:
            require(atom['item'] in increments,'unknown selected item '+atom['item'])
            value = atom['cost_bn']
            if atom['population']=='coverage':
                unlocated[atom['generation']] += value
                residual[atom['generation']] = residual.get(atom['generation'],0.)+value
                continue
            parts = driver_parts(atom,original[end],weights[:,0],effective_factor)
            if not parts:
                require(unlocated_residual=='retain','selected source residual lacks an observed household key: '+atom['source_piece'])
                residual[atom['generation']] = residual.get(atom['generation'],0.)+value
                tables['allocation_atoms'].append({**atom,'end':end,'located':False,'allocation':'unlocated source residual'})
                continue
            for category,share,driver in parts:
                if atom['item']=='native_minor_calibration' and atom['population']=='observed':
                    coordinate=(atom['generation'],category)
                    native_targets[coordinate]=native_targets.get(coordinate,0.)+value*share
                    tables['allocation_atoms'].append({**atom,'end':end,'category':category,'located':True,
                        'allocated_cost_bn':value*share,'allocation':'declared calibrated target: intrinsic reweighting plus source reconciliation, see calibration_reconciliation.csv'})
                    continue
                denominator = float(driver @ weights[:,0])
                require(abs(denominator)>1e-12,'zero selected signed household denominator')
                contribution = driver*(value*share*1e9/denominator)
                target = increments[atom['item']].setdefault(category,np.zeros(len(rows)))
                target += contribution
                require(abs(contribution @ weights[:,0]/1e9-value*share)<1e-9,'source atom original-weight price closure')
                tables['allocation_atoms'].append({**atom,'end':end,'category':category,'located':True,'allocated_cost_bn':value*share,
                    'allocation':'selected original source price proportions; observed count atoms use signed record-factor change'})
        # Preserve person prices under statistical reweighting. The native item
        # already prices that weight change; adding it again would count twice.
        # Direct item prices also reweight naturally, so use the complete selected
        # pre-native profile when reconciling to the source's observed native parts.
        pre_native = {cat:array.copy() for cat,array in base.items()}
        for item,change in increments.items():
            if item=='native_minor_calibration':
                continue
            for cat,array in change.items():
                pre_native.setdefault(cat,np.zeros(len(rows)))
                pre_native[cat] += array
        for category,price in pre_native.items():
            for g in GENS:
                selected=labels['own_generation']==g
                declared=native_targets.get((g,category),0.)
                correction,natural,remainder=reconcile_native(price,weights[:,0],calibrated[:,0],selected,declared)
                if np.any(correction):
                    target=increments['native_minor_calibration'].setdefault(category,np.zeros(len(rows)))
                    target+=correction
                tables['calibration_reconciliation'].append(dict(end=end,generation=g,category=category,
                    source_declared_observed_change_bn=declared,intrinsic_weight_change_bn=natural,
                    changed_record_price_reconciliation_bn=remainder,scope='original source prices unchanged when intrinsic reweighting equals declared target'))
        final = {cat:array.copy() for cat,array in base.items()}
        for change in increments.values():
            for cat,array in change.items():
                final.setdefault(cat,np.zeros(len(rows)))
                final[cat] += array
        full = sum(final.values())
        target = lines['union'][end]['v9_target_cost_bn']
        actual = float(full @ calibrated[:,0]/1e9)+sum(residual.values())
        require(abs(actual-target)<1e-9,'full household plus unlocated case closure')
        controls['gates'].append(dict(end=end,actual_bn=actual,target_bn=target,gap_bn=actual-target))
        for g in GENS:
            selected = labels['own_generation'] == g
            amount = float(full[selected] @ calibrated[selected,0]/1e9)+residual.get(g,0.)
            expected = lines['generations'][g][end]['v9_target_cost_bn']
            require(abs(amount-expected)<1e-9,'generation household plus unlocated closure '+g)
            controls['gates'].append(dict(end=end,generation=g,actual_bn=amount,target_bn=expected,gap_bn=amount-expected))
        for g in GENS:
            tables['people_survey_misses'].append(dict(end=end,generation=g,block='people the survey misses',
                net_missing_people=lines['meta']['final_coverage']['counts_by_generation_final'][g],cost_bn=unlocated[g],
                observed_household=False,age_band='unlocated; no final joint age allocation supplied'))
        for cat,array in final.items():
            tables['control'].append(dict(end=end,item=cat,bn=float(array @ calibrated[:,0]/1e9),assigned=True))
        for g,value in residual.items():
            tables['control'].append(dict(end=end,item='unlocated_'+g,bn=value,assigned=False))
        tables['control'] += [dict(end=end,item='households_sum',bn=float(full @ calibrated[:,0]/1e9),assigned=True),
            dict(end=end,item='case',bn=target,assigned=None),dict(end=end,item='households_sum_plus_residual_minus_case',bn=actual-target,assigned=None)]
        for convention in ('A','B','A_schools_per_head'):
            allowed = set(final) if convention!='B' else set(module.B_CATS+[module.PENSION])
            person = sum(array for cat,array in final.items() if cat in allowed)
            baseline = sum(array for cat,array in base.items() if cat in allowed)
            if convention=='A_schools_per_head':
                school = final.get('schools',np.zeros(len(rows)))
                person = person-school+(school @ calibrated[:,0])/calibrated[:,0].sum()
            result = summarize(person,calibrated[:,0],household,labels)
            all_share = next(row for row in result['shares'] if row['breakdown']=='all' and row['cell']=='all')
            located_people = float(calibrated[:,0].sum())+rounding
            missing_people = population['with_coverage']-population['without_coverage']
            contributor_people = all_share['share_members_net_positive']*float(calibrated[:,0].sum())
            tables['lineage_share_bounds'].append(dict(convention=convention,end=end,
                located_people=located_people,unlocated_coverage_people=missing_people,
                denominator_people=population['with_coverage'],located_share=all_share['share_members_net_positive'],
                whole_lineage_share_lower=contributor_people/population['with_coverage'],
                whole_lineage_share_upper=(contributor_people+missing_people)/population['with_coverage'],
                interpretation='identification bounds: no contributor classification for constructed coverage people'))
            for key,field in (('net_positive_shares','shares'),('concentration','concentration'),('household_balance_quantiles','quantiles')):
                tables[key] += [dict(convention=convention,end=end,**r) for r in result[field]]
            for category,array in final.items():
                tables['category_means'].append(dict(convention=convention,end=end,category=category,in_B=category in module.B_CATS+[module.PENSION],
                    net_cost_per_member_usd=float(array @ calibrated[:,0]/calibrated[:,0].sum())))
            if hh_table is None:
                hh_table = pd.DataFrame(dict(PH_SEQ=result['household_ids'],union_members=result['members'],weight=result['weight'],
                    calibrated_members=result['member_weight']))
            hh_table[f'{convention}_{end}_household_cost_usd'] = result['balance']
            hh_table[f'{convention}_{end}_weighted_cost_usd'] = result['weighted_dollars']
            if convention=='A_schools_per_head':
                continue
            prior = summarize(baseline,calibrated[:,0],household,{'all':labels['all']})
            before = summarize(sum(array for cat,array in base_original.items() if cat in allowed),
                               weights[:,0],household,{'all':labels['all']})
            tables['item_controls'].append(dict(convention=convention,end=end,item='record_weight_calibration_only',
                scope='fixed source totals; original vs calibrated normalization and ranking weights',
                located_delta_bn=float(baseline @ calibrated[:,0]/1e9)-sum(float(array @ weights[:,0]/1e9) for cat,array in base_original.items() if cat in allowed),
                baseline_share=before['shares'][0]['share_members_net_positive'],
                single_item_share=prior['shares'][0]['share_members_net_positive']))
            for item,change in increments.items():
                delta = sum((array for cat,array in change.items() if cat in allowed),np.zeros(len(rows)))
                single = summarize(baseline+delta,calibrated[:,0],household,{'all':labels['all']})
                entered = (~prior['net_positive']) & single['net_positive']
                left = prior['net_positive'] & (~single['net_positive'])
                tables['item_controls'].append(dict(convention=convention,end=end,item=item,scope='conditional joint-price typed toggle',
                    located_delta_bn=float(delta @ calibrated[:,0]/1e9),baseline_share=prior['shares'][0]['share_members_net_positive'],
                    single_item_share=single['shares'][0]['share_members_net_positive']))
                tables['crossings'].append(dict(convention=convention,end=end,item=item,
                    members_into_contributor=float(calibrated[entered,0].sum()),members_out_of_contributor=float(calibrated[left,0].sum())))
            entered=(~before['net_positive']) & result['net_positive']
            left=before['net_positive'] & (~result['net_positive'])
            tables['crossings'].append(dict(convention=convention,end=end,item='joint',
                members_into_contributor=float(calibrated[entered,0].sum()),members_out_of_contributor=float(calibrated[left,0].sum())))
    require(abs(sum(lines['meta']['final_coverage']['counts_by_generation_final'].values())-(population['with_coverage']-population['without_coverage']))<1e-6,'coverage count closure')
    controls['source_sha256'] = {'within_group_distribution_2026_09_29/households.py':digest(HERE/'households.py'),
        'within_group_distribution_2026_09_29/oct16_households.py':digest(Path(__file__))}
    footprint = module.require_within_budget('oct16 household source allocation and statistics')
    return tables, hh_table, controls, footprint


def main(basis='set', allocation='personal', accrual='flat', payroll='all', unlocated_residual='retain', placement='band',control_item=None):
    started = time.perf_counter()
    adoption = require_adopted('oct16')
    sub = Path('oct16')/('shared_allocation' if allocation == 'shared' else '')
    if control_item is not None:
        sub=sub/'controls'/control_item
    lines_path = HERE/'_cache'/sub/('lines_cash.json' if basis == 'cash' else 'lines.json')
    tables, hh_table, controls, footprint = calculate(read(lines_path),basis,allocation,accrual,payroll,unlocated_residual,placement,control_item,adoption)
    controls['source_sha256'][str(lines_path.relative_to(FISCAL))] = digest(lines_path)
    out = HERE/'derived'/sub/('cash' if basis=='cash' else '')
    cache = HERE/'_cache'/sub/('cash' if basis=='cash' else '')
    if placement=='uniform':
        out,cache=out/'uniform_placement',cache/'uniform_placement'
    out.mkdir(parents=True,exist_ok=True)
    cache.mkdir(parents=True,exist_ok=True)
    # Publish only after all source, count and conservation gates pass.
    suffix = '' if accrual=='flat' else ('_person_onbooks' if payroll=='onbooks' else '_person_accrual')
    for key,rows_out in tables.items():
        csv_write(out/(key+suffix+'.csv'),rows_out)
    hh_table.to_parquet(cache/('households'+suffix+'.parquet'),index=False)
    json_write(out/('controls'+suffix+'.json'),controls)
    print(json.dumps(dict(case='oct16',basis=basis,allocation=allocation,elapsed_seconds=time.perf_counter()-started,
        physical_footprint_bytes=footprint,diagnostic_maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,
        gates=controls['gates'])))


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=['oct16'],default='oct16')
    parser.add_argument('--basis',choices=['set','cash'],default='set')
    parser.add_argument('--allocation',choices=['personal','shared'],default='personal')
    parser.add_argument('--accrual',choices=['flat','person'],default='flat')
    parser.add_argument('--payroll',choices=['all','onbooks'],default='all')
    parser.add_argument('--unlocated-residual',choices=['retain','stop'],default='retain')
    parser.add_argument('--placement',choices=['band','uniform'],default='band')
    parser.add_argument('--control-item',choices=['none']+list(NEW_ITEMS[:-1]))
    args=parser.parse_args()
    main(args.basis,args.allocation,args.accrual,args.payroll,args.unlocated_residual,args.placement,args.control_item)
