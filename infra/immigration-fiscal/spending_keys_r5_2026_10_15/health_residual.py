"""Item21: a source-owned restricted-payer donor key, never a producer edit.

Ethnic translation changes only the target numerator; the national raw-key
denominator stays fixed, as in translate.py and the adopted package.
"""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True
import csv
import gc
import hashlib
import importlib.util
import json
from pathlib import Path
import resource
import time

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
FISCAL = HERE.parent
ROOT = FISCAL.parents[1]
OUT = HERE / 'derived'
sys.path.insert(0, str(FISCAL / 'build'))
import meps_health_transport_2024 as M
from health_ratios import build_ratios

GENS = ('G1', 'G2', 'G3plus')
BANDS = ('0-17', '18-34', '35-49', '50-64', '65+')
NAT = {1: 'us_born', 2: 'foreign_born'}
ARMS = ('central', 'population', 'no_ethnicity', 'plain_pooled', 'old_key')


def require(ok, message):
    if not ok:
        raise ValueError('[BLOCKED] item21: ' + message)


def read(path):
    return json.loads(path.read_text())


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, allow_nan=False) + '\n')


def write_csv(path, rows):
    require(bool(rows), 'empty CSV')
    fields=list(dict.fromkeys(k for row in rows for k in row))
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fields, lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def inputs():
    fields = ['PH_SEQ', 'PPPOS', 'A_AGE', 'PENATVTY', 'PRPERTYP', 'PRCITSHP',
              'PEFNTVTY', 'PEMNTVTY', 'PRDTHSP', 'PUB', 'PRIV', 'pwwgt0',
              'A_LINENO', 'PEPAR1', 'PEPAR2', 'PF_SEQ', 'GESTFIPS']
    frame = FISCAL / 'generation_account_2026_09_24/_cache/asec25_generation.parquet'
    d = pd.read_parquet(frame, columns=fields)
    civ = (d.PRPERTYP.eq(2) | d.A_AGE.lt(15)).to_numpy()
    native = d.PRCITSHP.isin([1, 2, 3]).to_numpy()
    us = [57, 60, 66, 69, 73, 78]
    masks = [d.PRCITSHP.isin([4, 5]).to_numpy() & d.PENATVTY.eq(303).to_numpy(),
             native & (d.PEFNTVTY.eq(303) | d.PEMNTVTY.eq(303)).to_numpy(),
             native & d.PEFNTVTY.isin(us).to_numpy() & d.PEMNTVTY.isin(us).to_numpy() & d.PRDTHSP.eq(1).to_numpy()]
    masks = np.asarray(masks) & civ
    union = masks.any(axis=0)
    w = d.pwwgt0.to_numpy(float)
    exposure = ~(d.PUB.eq(0) & d.PRIV.eq(0)).to_numpy()
    require(not np.any((~exposure) & (d.A_AGE.to_numpy() > 0)), 'noninfant exposure exclusion')
    md, anchors = M.read_meps(ROOT / 'sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip',
                              ROOT / 'sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt')
    keys, cells, covs = {}, [], {}
    valid = md.PERWT24F.gt(0) & md.AGE24X.ge(0) & md.BORNUSA.isin([1, 2])
    for key, cols in [('old', ['TOTVA24', 'TOTTRI24', 'TOTOFD24', 'TOTSTL24']), ('new', ['TOTOFD24', 'TOTSTL24'])]:
        donor = md.copy()
        donor['public_paid'] = donor[cols].sum(axis=1)
        tab, codes, covariance = M.donor_model(donor, d, False)
        keys[key] = tab.mean_public_paid.to_numpy()[codes] * exposure
        covs[key] = covariance.tolist()
        for row in tab.itertuples():
            sel = valid & md.age_band.eq(row.age_band) & md.born.eq(row.born)
            cells.append(dict(key=key, band=BANDS[int(row.age_band)], nativity=NAT[int(row.born)], n=int(row.n),
                              n_positive=int((donor.loc[sel, 'public_paid'] > 0).sum()),
                              population=float(row.population), mean=float(row.mean_public_paid), se=float(row.se_sampling)))
    totals = {k: float(v[civ] @ w[civ]) for k, v in keys.items()}
    incidence = pd.read_csv(FISCAL / 'full_account_spending_2026_09_20/derived/incidence_keys.csv')
    old = incidence.query("allocation == 'personal' and key == 'health_other'").iloc[0]
    require(abs(totals['old']/old.national_key_total-1) < 1e-12, 'old national donor key')
    require(abs(float(keys['old'][union] @ w[union])/old.target_key_total-1) < 1e-12, 'old union donor key')
    for k in keys:
        require(abs(float((keys[k][civ]/totals[k]) @ w[civ])-1) < 1e-12, k+' national normalized key closes')
    ratios = build_ratios()
    published = pd.read_csv(FISCAL / 'medical_ethnicity_pooled_2026_09_23/derived/ratios.csv')
    chosen = published.query("sample == 'pooled_2016_2024' and spec == 'winsor_p995' and scheme == 'transport' and comparison == 'mexican_origin/all_donors' and measure == 'other_public' and nativity in ['us_born','foreign_born']")
    ratios += chosen.to_dict('records')
    cell = list(zip(np.digitize(d.A_AGE, [18, 35, 50, 65]), np.where(d.PENATVTY.eq(57), 1, 2)))
    r = {}
    for spec, measure, name in [('winsor_p995', 'other_public', 'old'), ('winsor_p995', 'ofd_stl', 'central'), ('plain', 'ofd_stl', 'plain_pooled')]:
        lookup = {(BANDS.index(q['band']), 1 if q['nativity']=='us_born' else 2): q['ratio'] for q in ratios if q['spec']==spec and q['measure']==measure}
        require(len(lookup)==10, name+' ethnic cells missing')
        r[name] = np.array([lookup[c] for c in cell])
    donor_mass = {p: float((md.loc[valid, p]*md.loc[valid, 'PERWT24F']).sum()/1e9)
                  for p in ['TOTVA24','TOTTRI24','TOTOFD24','TOTSTL24']}
    return d, civ, union, masks, w, keys, totals, r, cells, ratios, donor_mass, covs


def source_weights(d, civ, union, masks, w):
    sp = importlib.util.spec_from_file_location('item21_frame', FISCAL/'generation_account_2026_09_24/frame.py')
    frame = importlib.util.module_from_spec(sp); sp.loader.exec_module(frame)
    omega, _, _ = frame.assignments(d,civ,union,dict(zip(GENS,masks)))
    import combine_onbooks_lane as L
    acs=L.acs_cells()
    exact=np.column_stack([w,w])
    for name,cit in [('natz',4),('noncit',5)]:
        m=d.PENATVTY.eq(303).to_numpy() & ~d.GESTFIPS.isin(L.CA_TX).to_numpy() & d.PRCITSHP.eq(cit).to_numpy()
        exact,_=L.scale_cell(exact,m,acs[name])
    return omega,exact[:,0]


def target(key, ratio, om, w, w4, civ, national, hf):
    """The adopted medicalShifts + generation scaledSplit construction."""
    t0=national*hf*((key*w)@om)/(key[civ]@w[civ])
    t1=national*hf*((key*w4)@om)/(key[civ]@w4[civ])
    du=national*hf*((key*w*(ratio-1))@om)/(key[civ]@w[civ])
    unionchange=du.sum()*t1.sum()/t0.sum()
    own=du*t1/t0
    return t1+own+(unionchange-own.sum())*t1/t1.sum()


def amount(lines, name, key=None):
    line=next(q for q in lines if q['id']==name)
    return line['keys'][key or line['preferred_key']]['personal']['target_bn']


def row_amount(run, name, side='spending'):
    return next(q['amount_bn'] if side=='spending' else q['return_bn'] for q in run[side] if q['id']==name)


def main():
    start=time.perf_counter()
    d,civ,union,masks,w,keys,totals,ratios,cells,ratio_rows,donor_mass,covs=inputs()
    snap=read(OUT/'item21_snapshot.json'); source=snap['source']
    base=snap['sets']['set']['ends']['low'][0]
    national=next(q['national_bn'] for q in base['spending'] if q['id']=='health_services')
    va=89.742; residual=national-va; fraction=residual/national
    require(abs(residual+va-national)<1e-9,'residual plus VA national mass')
    n0=source['models']['a']['G1'][0]['national_bn']
    scale=national/n0; hf=float(w[civ].sum())/340110988.
    omega,w4=source_weights(d,civ,union,masks,w)
    raw_old={c:target(keys['old'],ratios['old'],om,w,w4,civ,n0,hf) for c,om in omega.items()}
    old_refs={c:np.array([amount(source['references']['set'][c][g],'health_services','health_other') for g in GENS]) for c in omega}
    oracle=max(float(np.max(np.abs(raw_old[c]-old_refs[c]))) for c in omega)
    require(oracle<1e-9,'old source medical translation reconstruction: '+str(oracle))
    age=np.minimum(d.A_AGE.to_numpy()//5,16)
    ak=read(FISCAL/'added_age_mix_2026_10_07/derived/g3_age_keys.json')
    old_profile=np.array(ak['keys']['spending']['personal']['health_other'])
    require(np.max(np.abs(np.bincount(age[masks[2]],weights=(keys['old']*w)[masks[2]],minlength=17)-old_profile))<1e-4,'G3 source raw age profile')
    people=read(FISCAL/'main_case_2026_10_15/derived/union_people.json')['records']
    idindex=pd.MultiIndex.from_frame(d[['PH_SEQ','PPPOS']])
    reporters=np.zeros(len(d),bool)
    for q in people:
        if q['central_reporter']: reporters[idindex.get_loc((q['PH_SEQ'],q['PPPOS']))]=True
    require(abs(w4[union].sum()-39712493.33120155)<1,'row4 account population')
    lineage=source['age_detail']['counts']; c3=lineage['c3']
    mix=read(FISCAL/'added_age_mix_2026_10_07/derived/age_mix.json')
    mixes=mix['readings']['cross_section_2007_2026']
    pi=np.array(mix['meta']['identified'])
    counts={'lineage_later_g3':lineage['later'],'lineage_g3_rate_g3':(1-c3)*lineage['g3_rate'],'lineage_g3_rate_white':c3*lineage['g3_rate']}
    countmix={'lineage_later_g3':np.array(mixes['later']),'lineage_g3_rate_g3':np.array(mixes['g3_rate']),'lineage_g3_rate_white':np.array(mixes['g3_rate'])}
    units={kind:{line:np.array([amount(q[kind]['set'],line,'health_other' if line=='health_services' else 'k') for q in source['unit_models']]) for line in ['health_services','state_price_health_services']} for kind in ['g3','white']}
    stock=next(q['stock_charged_bn'] for q in base['capital'] if q['id']=='health_sl')
    require(stock>0,'SL health stock')
    national_weights={k:{'published':float(v[civ]@w[civ]),'row4':float(v[civ]@w4[civ])} for k,v in keys.items()}
    normalized_gap=max(abs(float((v[civ]/national_weights[k]['row4'])@w4[civ])-1) for k,v in keys.items())
    require(normalized_gap<1e-12,'row4 national key normalization')
    gates={'national_raw_key_normalization':True,'national_row4_max_normalization_gap':normalized_gap,'national_residual_plus_va_gap_bn':residual+va-national,'old_translation_max_gap_bn':oracle}
    measurement={'number':21,'id':'health_residual_key','status':'measured donor-key counterfactual; parent adoption only','rates':{'low':.02,'high':.03},'national_bn':{'health_services':national,'va_held':va,'residual':residual},'donor_mass_bn':donor_mass,'donor_totals':totals,'arms':{},'gates':gates,'transport':'Source medicalShifts/scaledSplit; raw within-generation donor profiles; added G3/white unit-band repricing; fixed fee dollars held. Federal health stock and fee offsets held.'}
    measurement['national_donor_mass']=national_weights
    principal=read(HERE/'inputs/item21_v9_base.json')
    common_rate=principal['one_rate']['flat_real_equivalent']
    require(principal['one_rate']['arm']=='B' and common_rate>=0,'frozen v9 common capital rate')
    measurement['v9_capital_rate']=common_rate
    exposures={'federal_health_structures_national_bn':next(q['stock_charged_bn'] for q in base['capital'] if q['id']=='health_fed'),
               'federal_rule':'Held on old key: source FAAt701 line43 does not split VA from other federal health structures.',
               'equipment_rule':'eq_health_sl follows the key only in the equipment sensitivity; no absent reporter or coverage equipment carrier is invented.',
               'by_end':{}}
    for end,rate in [('low',.02),('high',.03)]:
        run=snap['sets']['set']['ends'][end][0]
        cap=next(q for q in run['capital'] if q['id']=='health_fed')
        carrier=sum(q['amount_bn']*q['response'] for q in run['spending'] if q['id'].startswith('union_completion_health_fed_') and 'user_fees' not in q['id'])
        covered=sum(q['coverage_bn'] for q in snap['sets']['set']['payload']['meta']['coverage']['by_end'][end]['decomposition']['line_parts'] if q.get('source_line')=='health_fed')
        exposures['by_end'][end]={'source_rate':rate,'engine_bn':cap['return_bn'],'completion_bn':carrier,'coverage_bn':covered,
                                 'gross_held_return_bn':cap['return_bn']+carrier+covered,
                                 'gross_held_group_stock_bn':(cap['return_bn']+carrier+covered)/rate}
    input_paths=[ROOT/'sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256dat.zip',ROOT/'sources/immigration-fiscal/data/external/stage3/ahrq/meps_2024/h256su.txt',FISCAL/'build/meps_health_transport_2024.py',FISCAL/'medical_ethnicity_pooled_2026_09_23/_cache/pooled.parquet',FISCAL/'medical_ethnicity_pooled_2026_09_23/derived/ratios.csv',FISCAL/'medical_ethnicity_pooled_2026_09_23/pooled_ratios.py',FISCAL/'generation_account_2026_09_24/_cache/asec25_generation.parquet',FISCAL/'generation_account_2026_09_24/run_generations.cjs',FISCAL/'main_case_2026_09_24/package.cjs',FISCAL/'added_age_mix_2026_10_07/derived/g3_age_keys.json',FISCAL/'capital_return_services_2026_09_27/derived/engine_components.json']
    measurement['source_hashes']={str(p.relative_to(ROOT)):hashlib.file_digest(p.open('rb'),'sha256').hexdigest() for p in input_paths}
    shares=[]; all_count=[]; coverage_out={'item':'health_residual_key','arms':{}}
    v9_count=[]; v9_coverage={'item':'health_residual_key','capital_rate':common_rate,'arms':{}}
    for arm in ARMS:
        key=keys['old'] if arm=='old_key' else np.ones(len(d)) if arm=='population' else keys['new']
        ratio=ratios['old'] if arm=='old_key' else ratios['central'] if arm=='central' else ratios['plain_pooled'] if arm=='plain_pooled' else np.ones(len(d))
        new_refs={c:old_refs[c]+target(key,ratio,om,w,w4,civ,n0,hf)-raw_old[c] for c,om in omega.items()}
        if arm=='old_key': new_refs={c:old_refs[c].copy() for c in omega}
        profile=old_profile.copy() if arm=='old_key' else np.bincount(age[masks[2]],weights=(key*w)[masks[2]],minlength=17)
        shape=(profile/profile.sum())/(old_profile/old_profile.sum())
        factor=new_refs['a'][2]/old_refs['a'][2]*shape
        newunits={kind:{line:a.copy() for line,a in rows.items()} for kind,rows in units.items()}
        for line in newunits['g3']:newunits['g3'][line]*=factor
        if arm=='population':
            for j,q in enumerate(source['unit_models']):
                newunits['white']['health_services'][j]=amount(q['white']['set'],'health_services','population')
                healthratio=newunits['white']['health_services'][j]/units['white']['health_services'][j]
                newunits['white']['state_price_health_services'][j]*=healthratio
        oldlin={line:{part:counts[part]*float(countmix[part]@units['white' if part.endswith('white') else 'g3'][line]) for part in counts} for line in units['g3']}
        newlin={line:{part:counts[part]*float(countmix[part]@newunits['white' if part.endswith('white') else 'g3'][line]) for part in counts} for line in units['g3']}
        native_old={line:0. for line in units['g3']}; native_new=native_old.copy()
        native_price={line:{} for line in native_old}
        for q in people:
            if not q['observed_nonreporter']:continue
            b=q['age_band']; blend=q['economic_class']!='later'
            for line in native_old:
                old=units['g3'][line][b] if not blend else (1-c3)*units['g3'][line][b]+c3*units['white'][line][b]
                new=newunits['g3'][line][b] if not blend else (1-c3)*newunits['g3'][line][b]+c3*newunits['white'][line][b]
                native_old[line]+=q['people']*old; native_new[line]+=q['people']*new
                native_price[line][(q['PH_SEQ'],q['PPPOS'])]=(old,new)
        require(abs(native_old['health_services']-.013459770480335528)<1e-9,'native-child source health reconstruction')
        old_ratio=float((keys['old']*w4)[reporters].sum()/(keys['old']*w4)[masks[2]].sum())
        new_ratio=float((key*w4)[reporters].sum()/(key*w4)[masks[2]].sum())
        reporter_ratio_factor=new_ratio/old_ratio
        blocks={}; amount_maps={}
        for conv in ['a','b']:
            rows=[]; old_donor=old_refs[conv]*scale; new_donor=new_refs[conv]*scale
            # Same-generation reference rates for the added people; conventions only route identified minors.
            for j,g in enumerate(GENS):
                rows.append(dict(line='health_services',source_line='health_services',side='spending',population='original_union',generation=g,part='residual_consumption',before_bn=old_donor[j]*fraction,after_bn=new_donor[j]*fraction,delta_bn=(new_donor[j]-old_donor[j])*fraction,donor_before_bn=old_donor[j],donor_after_bn=new_donor[j]))
            for line in units['g3']:
                for part in counts:
                    before=oldlin[line][part]; after=newlin[line][part]
                    mul=fraction if line=='health_services' else 1.
                    rows.append(dict(line=line,source_line=line,side='spending',population='added_lineage',generation='G3plus',profile=part,part='residual_consumption' if line=='health_services' else 'state_price',before_bn=before*mul,after_bn=after*mul,delta_bn=(after-before)*mul,donor_before_bn=before,donor_after_bn=after))
                before=native_old[line]; after=native_new[line]; mul=fraction if line=='health_services' else 1.
                rows.append(dict(line='native_child_spending_'+line,source_line=line,side='spending',population='completion',generation='G3plus',profile='native_nonreporters',part='residual_consumption' if line=='health_services' else 'state_price',before_bn=before*mul,after_bn=after*mul,delta_bn=(after-before)*mul,donor_before_bn=before,donor_after_bn=after))
            run=snap['sets']['set']['generations'][conv]['low']
            original_sp=[]
            for j,g in enumerate(GENS):
                actual=row_amount(run[j],'state_price_health_services')
                latent=sum(oldlin['state_price_health_services'].values())+native_old['state_price_health_services'] if j==2 else 0
                before=actual-latent; after=before*new_refs[conv][j]/old_refs[conv][j]
                original_sp.append((before,after))
                rows.append(dict(line='state_price_health_services',source_line='state_price_health_services',side='spending',population='original_union',generation=g,part='state_price',before_bn=before,after_bn=after,delta_bn=after-before))
            for line in units['g3']:
                before_carrier=row_amount(base,'union_completion_'+line+('_health_other' if line=='health_services' else '_k'))
                # Existing source anchors (which may include a fixed fee component) remain visible.
                old_total=(old_donor[2] if line=='health_services' else original_sp[2][0])+sum(oldlin[line].values())
                new_total=(new_donor[2] if line=='health_services' else original_sp[2][1])+sum(newlin[line].values())
                full_before=row_amount(run[2],line)-native_old[line]
                anchor=before_carrier/full_before
                donor_before=old_total*anchor; donor_after=new_total*anchor*reporter_ratio_factor
                mul=fraction if line=='health_services' else 1.
                rows.append(dict(line='union_completion_'+line+('_health_other' if line=='health_services' else '_k'),source_line=line,side='spending',population='completion',generation='G3plus',profile='reporters',part='residual_consumption' if line=='health_services' else 'state_price',before_bn=donor_before*mul,after_bn=donor_after*mul,delta_bn=(donor_after-donor_before)*mul,donor_before_bn=donor_before,donor_after_bn=donor_after))
            if conv=='b':
                # Completion uses the source's own G3+ account, never the minor-routing convention.
                rows=[json.loads(json.dumps(next(a for a in blocks['a'] if a['population']=='completion' and a['line']==q['line'] and a.get('profile')==q.get('profile')))) if q['population']=='completion' else q for q in rows]
                own=[q for q in rows if q['source_line']=='state_price_health_services' and q['population']=='original_union']
                target_delta=sum(q['delta_bn'] for q in blocks['a'] if q['source_line']=='state_price_health_services' and q['population']=='original_union')
                remainder=target_delta-sum(q['delta_bn'] for q in own)
                den=sum(q['before_bn'] for q in own)
                for q in own:
                    q['delta_bn']+=remainder*q['before_bn']/den;q['after_bn']=q['before_bn']+q['delta_bn']
            # Capital follows the complete health-use key, with no VA consumption fraction.
            for q in list(rows):
                if q['source_line']!='health_services':continue
                before=q['donor_before_bn']/national*stock; after=q['donor_after_bn']/national*stock
                rows.append(dict(line=q['line'].replace('health_services','health_sl'),source_line='health_sl',side='capital',population=q['population'],generation=q['generation'],profile=q.get('profile','identified'),part='sl_health_capital',capital_stock_before_bn=before,capital_stock_delta_bn=after-before,donor_before_bn=before,donor_after_bn=after))
            blocks[conv]=rows
        # New and old raw keys are transported through the source's actual row-level kernels.
        idkey=pd.Series(key,index=idindex)
        oldkey=pd.Series(keys['old'],index=idindex)
        def prices(data,audit,basis,vintage):
            from health_coverage import require as check
            ids=pd.MultiIndex.from_arrays([data['person_ph_seq'],data['person_pppos']])
            newdriver=idkey.reindex(ids).to_numpy(); olddriver=oldkey.reindex(ids).to_numpy()
            check(np.isfinite(newdriver).all() and np.isfinite(olddriver).all(),'complete driver/person join')
            obs=data['weights'][:,0]; added=data['added_weights'][:,0]; mass=obs+added
            original=pd.Series(union,index=idindex).reindex(ids).to_numpy(bool)
            report=pd.Series(reporters,index=idindex).reindex(ids).to_numpy(bool)
            band=np.minimum(data['age']//5,16)
            out=[]
            for end,rate in [('low',.02),('high',.03)]:
                for i,q in enumerate(blocks['a']):
                    line=q['source_line'];g=q['generation'];gi=GENS.index(g)
                    cap=q['side']=='capital';source_line='health_services' if cap else line
                    mul=rate if cap else 1.
                    before=q['donor_before_bn'] if cap else q['before_bn'];after=q['donor_after_bn'] if cap else q['after_bn']
                    delta=np.zeros(len(ids)); scope='identified'
                    if q['population']=='added_lineage':
                        scope='added';part=q['profile'];kind='white' if part.endswith('white') else 'g3'
                        per_band=counts[part]*countmix[part]*(newunits[kind][source_line]-units[kind][source_line])
                        if cap:per_band*=stock/national
                        elif line=='health_services':per_band*=fraction
                        for b,v in enumerate(per_band):
                            selected=original & (data['generation']==2) & (band==b)
                            den=float(added[selected].sum())
                            check(den>0 or abs(v)<1e-12,'added age-band mass')
                            if den:delta[selected]=v/den
                    elif q.get('profile')=='native_nonreporters':
                        scope='added'
                        for j,ident in enumerate(ids):
                            if ident in native_price[source_line]:
                                a,b=native_price[source_line][ident];delta[j]=b-a
                        if cap:delta*=stock/national
                        elif line=='health_services':delta*=fraction
                    else:
                        selected=(report if q.get('profile')=='reporters' else original) & (data['generation']==gi)
                        ov=np.where(selected,olddriver,0);nv=np.where(selected,newdriver,0)
                        od=float(ov@obs);nd=float(nv@obs)
                        check(od>0 and nd>0,'own-record donor mass')
                        delta=nv*(after/nd)-ov*(before/od)
                    delta*=mul
                    if arm=='old_key':delta[:]=0
                    weights=added if scope=='added' else obs
                    expected=(after-before)*mul
                    check(abs(float(delta@weights)-expected)<1e-9,'own-price population closure '+q['line']+':'+q.get('profile','identified'))
                    out.append({'end':end,'generation':g,'line':'item21:'+q['line']+':'+str(i),'source_line':line,'source_side':'capital' if cap else 'spending','category':'capital' if cap else 'health','level':'state_local' if cap else 'unclassified','economic_class':'capital_return' if cap else 'fiscal_line','source_response':1,'source_key':'ofd_stl','base_price':delta,'constructed_price':delta.copy(),'population':scope,'pricing':'separate source own-record and G3/white own-age donor deltas; no change to held fee or white payer amounts'})
            return out
        from health_coverage import build as coverage_build
        cov=coverage_build(prices,bases=('set',))
        cov['sets']['cash']=json.loads(json.dumps(cov['sets']['set']))
        coverage_out['arms'][arm]=cov
        cov_v9=coverage_build(prices,bases=('set',),capital_rate=common_rate)
        cov_v9['sets']['cash']=json.loads(json.dumps(cov_v9['sets']['set']))
        v9_coverage['arms'][arm]=cov_v9
        for which in ['set','cash']:
            for q in cov_v9['sets'][which]['count_parts']:v9_count.append({'arm':arm,'basis':which,**q})
        for end in ['low','high']:
            expected=sum(q['coverage_bn']*(common_rate/(.02 if end=='low' else .03) if q['economic_class']=='capital_return' else 1.) for q in cov['sets']['set']['ends'][end]['decomposition']['line_parts'])
            require(abs(expected-cov_v9['sets']['set']['ends'][end]['total_bn'])<1e-9,'common-rate coverage replay')
        armsets={}
        for which in ['set','cash']:
            byconv={c:{} for c in blocks}
            for end,rate in [('low',.02),('high',.03)]:
                covrows=cov['sets'][which]['ends'][end]['decomposition']['line_parts']
                for conv in blocks:
                    parts=json.loads(json.dumps(blocks[conv]))
                    for q in parts:
                        if q.get('side')=='capital':q.update(before_bn=q['capital_stock_before_bn']*rate,after_bn=(q['capital_stock_before_bn']+q['capital_stock_delta_bn'])*rate,delta_bn=q['capital_stock_delta_bn']*rate,source_rate=rate)
                    for q in covrows:
                        v=q['coverage_bn']; row={**q,'population':'coverage','part':'coverage','before_bn':0.,'after_bn':v,'delta_bn':v}
                        if q['source_side']=='capital':row.update(capital_stock_before_bn=0.,capital_stock_delta_bn=v/rate,source_rate=rate)
                        parts.append(row)
                    if arm=='old_key':require(max(abs(q['delta_bn']) for q in parts)<1e-9,'old-key zero changes')
                    byconv[conv][end]={'parts':parts,'source_rate':rate,'total_bn':sum(q['delta_bn'] for q in parts)}
                require(abs(byconv['a'][end]['total_bn']-byconv['b'][end]['total_bn'])<1e-9,'generation conventions total')
            armsets[which]={'by_end':byconv['a'],'by_generation':byconv,'count_interactions':cov['sets'][which]['item_overrides']}
            for q in cov['sets'][which]['count_parts']:all_count.append({'arm':arm,'basis':which,**q})
        measurement['arms'][arm]={'sets':armsets}
        for q in blocks['a']:
            if q['source_line']!='health_services':continue
            held=0.
            if q['population']=='original_union':
                j=GENS.index(q['generation']);actual=row_amount(snap['sets']['set']['generations']['a']['low'][j],'health_services')
                latent=sum(oldlin['health_services'].values())+native_old['health_services'] if j==2 else 0.
                held=actual-latent-q['donor_before_bn']
            elif q.get('profile')=='reporters':held=row_amount(base,q['line'])-q['donor_before_bn']
            shares.append({'arm':arm,'population':q['population'],'generation':q['generation'],'profile':q.get('profile','identified'),'old_share':(q['donor_before_bn']+held)/national,'new_share':(q['donor_after_bn']+held)/national,'held_share':held/national})
        for g in GENS:
            old=sum(q['coverage_bn'] for q in snap['sets']['set']['payload']['meta']['coverage']['by_end']['low']['decomposition']['line_parts'] if q.get('source_side')=='spending' and q.get('source_line')=='health_services' and q['generation']==g)
            change=sum(q['coverage_bn'] for q in cov['sets']['set']['ends']['low']['decomposition']['line_parts'] if q['source_side']=='spending' and q['source_line']=='health_services' and q['generation']==g)/fraction
            shares.append({'arm':arm,'population':'coverage','generation':g,'profile':'source_missing_people','old_share':old/national,'new_share':(old+change)/national,'held_share':0.})
        print(arm,[(e,armsets['set']['by_end'][e]['total_bn']) for e in ['low','high']],flush=True)
        gc.collect()
    gates['old_key_max_change_bn']=max(abs(q['delta_bn']) for e in measurement['arms']['old_key']['sets']['set']['by_end'].values() for q in e['parts'])
    write_json(OUT/'item21.json',measurement)
    write_json(OUT/'item21_coverage.json',coverage_out)
    write_json(OUT/'item21_v9_coverage.json',v9_coverage)
    write_json(OUT/'item21_exposures.json',exposures)
    write_csv(OUT/'item21_key_cells.csv',cells)
    # Keep only one schema in each uncertainty table.
    write_csv(OUT/'item21_ratios.csv',[q for q in ratio_rows if q['measure']=='ofd_stl'])
    write_csv(OUT/'item21_shares.csv',shares)
    write_csv(OUT/'item21_count_parts.csv',all_count)
    write_csv(OUT/'item21_v9_count_parts.csv',v9_count)
    write_json(OUT/'item21_gates.json',gates)
    print('item21 complete; elapsed',time.perf_counter()-start,'maxrss',resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,flush=True)


if __name__ == '__main__':
    main()
