"""Typed crime mortality replacements on the frozen P7 social boundary."""
import csv
import hashlib
import io
import json
import os
from pathlib import Path
import sys
import tempfile

HERE=Path(__file__).resolve().parent
FISCAL=HERE.parent
ROOT=FISCAL.parent.parent
OUT=HERE/'derived/oct15'
VICTIM=FISCAL/'crime_victim_cost_2026_09_23'
sys.dont_write_bytecode=True
sys.path.insert(0,str(HERE))
import p7_crime as p7


def require(ok,message):
    if not ok:
        raise ValueError('[BLOCKED] crime mortality pairing: '+message)


def digest(path):
    with path.open('rb') as stream:
        return hashlib.file_digest(stream,'sha256').hexdigest()


def validated_inputs():
    p7_path=HERE/'derived/p7_payload.json'
    old=json.loads(p7_path.read_text())
    require(old['case']=='oct14' and old['vsl_standard']=='dot_uniform','wrong frozen P7 case/basis')
    for name,expected in old['sources_sha256'].items():
        require((ROOT/name).is_file() and digest(ROOT/name)==expected,'stale frozen P7 source: '+name)
    receipt_path=VICTIM/'derived/oct15/mortality_receipt.json'
    receipt=json.loads(receipt_path.read_text())
    require(receipt['case']=='oct15' and all(receipt['gates'].values()),'failed live mortality producer gates')
    for name,expected in receipt['inputs_sha256'].items():
        require((ROOT/name).is_file() and digest(ROOT/name)==expected,'stale live mortality input: '+name)
    for name,expected in receipt['outputs_sha256'].items():
        require(digest(VICTIM/'derived/oct15'/name)==expected,'partial/stale live mortality publication: '+name)
    arms=p7.rows(VICTIM/'derived/oct15/mortality_arms.csv')
    keys=[(r['footing'],r['valuation'],float(r['real_discount_rate'])) for r in arms]
    require(len(keys)==len(set(keys)),'duplicate mortality registry cells')
    return old,receipt,dict(zip(keys,arms)),p7_path,receipt_path


def build():
    old,source,arms,p7_path,receipt_path=validated_inputs()
    factor=p7.population_factor()
    baseline=json.loads((HERE/'inputs/baseline_totals_oct14.json').read_text())
    original=next(r for r in baseline['lineage_social_rows']['rows'] if r['item']=='victims')
    pairing=[]
    envelope=[]
    standalone=[]
    choices=[(r['valuation'],float(r['real_discount_rate'])) for r in source['valuation_choices']]
    require(set(choices)=={('dot_uniform',0.0),('dot_life_years',0.0),('dot_life_years',.03)}
            and len(choices)==3,'wrong mortality basis/rate registry')
    for end,footing in (('low','mixed'),('high','custody')):
        parameters=old['response_parameters'][end]
        recipient=parameters['recipient_share']
        sender=parameters['added_offending_share']
        scaling=factor*(1+sender)*(1-recipient)
        expected=float(old['lineage_crime_rows'][end]['victims'])
        rebuilt=float(arms[(footing,'dot_uniform',0.0)]['victim_cost_bn'])*scaling
        require(abs(rebuilt-expected)<1e-9,'native uniform prices do not reproduce current P7 victim baseline: '+end)
        for valuation,rate in choices:
            replacement=float(arms[(footing,valuation,rate)]['victim_cost_bn'])*scaling
            union=float(arms[(footing,valuation,rate)]['victim_cost_bn'])*factor*(1-recipient)
            row=dict(end=end,valuation=valuation,real_discount_rate=rate,
                     lineage_victim_delta_bn=replacement-expected,
                     baseline_lineage_victim_bn=expected,replacement_lineage_victim_bn=replacement,
                     baseline_union_victim_bn=old['union_crime_rows_outside_lineage'][end]['victims'],
                     replacement_union_victim_bn=union,replacement_added_victim_bn=replacement-union,
                     published_pre_round1_union_victim_bn=original[f'union_{end}_bn'],
                     published_pre_round1_lineage_victim_bn=original[f'union_{end}_bn']+original[f'added_{end}_bn'],
                     held_lineage_fear_bn=old['lineage_crime_rows'][end]['fear_avoidance'],
                     held_lineage_security_bn=old['lineage_crime_rows'][end]['private_security'],
                     source_footing=footing,source_frame_factor=factor,recipient_share=recipient,
                     added_offending_share=sender,
                     scope='conditional fixed-v7 social sender/receiver keys on oct15 fiscal account; victim mortality replacement only; fear/security held')
            require(abs(row['replacement_union_victim_bn']+row['replacement_added_victim_bn']-replacement)<1e-9,
                    'union plus added victim closure')
            pairing.append(row)
            for category,chosen,target in (('envelope','envelope_'+end,envelope),
                                           ('standalone_unmixed','equal' if end=='low' else 'custody_unmixed',standalone)):
                active=arms[(chosen,valuation,rate)]
                legacy=float(active['legacy_victim_cost_bn'])*scaling
                value=float(active['victim_cost_bn'])*scaling
                target.append(dict(end=end,valuation=valuation,real_discount_rate=rate,source_footing=chosen,
                                   baseline_legacy_lineage_victim_bn=legacy,replacement_lineage_victim_bn=value,
                                   legacy_price_delta_bn=value-legacy,
                                   mortality_channel_bn=float(active['mortality_bn'])*scaling,
                                   scope=category+'; matching selected mortality basis/rate on every death; frozen v7 exposure'))
    require(len(pairing)==6 and len(envelope)==6 and len(standalone)==6,'incomplete low/high basis/rate coverage')
    for row in pairing:
        if row['valuation']=='dot_uniform':
            require(abs(row['lineage_victim_delta_bn'])<1e-9,'current P7 central is not uniformly priced')
    inputs={str(p7_path.relative_to(ROOT)):digest(p7_path),str(receipt_path.relative_to(ROOT)):digest(receipt_path)}
    for path in (HERE/'inputs/baseline_totals_oct14.json',Path(__file__),HERE/'p7_crime.py',
                 FISCAL/'population_basis_2026_09_29/derived/frame_counts.csv',
                 VICTIM/'derived/oct15/mortality_arms.csv'):
        inputs[str(path.relative_to(ROOT))]=digest(path)
    return {'mortality_pairing_rows.csv':pairing,'mortality_envelope_rows.csv':envelope,
            'mortality_standalone_rows.csv':standalone},dict(case='oct15',source_quantity_case='frozen v7 social frame',
            inputs_sha256=inputs,producer_receipt_sha256=digest(receipt_path),
            baseline_contract='exact p7_payload.lineage_crime_rows[end].victims; apply_p7_crime sets these boundary-adjusted rows directly',
            central_round2_victim_delta_bn={r['end']:r['lineage_victim_delta_bn'] for r in pairing if r['valuation']=='dot_uniform'},
            gates=dict(source_pins=True,current_P7_uniform_baseline_1e_9=True,union_added_closure_1e_9=True,
                       complete_basis_rate_coverage=True,fear_security_held=True),
            assumptions='C3 sender/offending keys and descendant recipient exposure remain at P7/v7; no v8 crime membership repricing. Life-year arms use primary SHR victim ages and NVSS common period mortality; matching environment/crash arms required in joint consumer.')


def main():
    tables,receipt=build()
    OUT.mkdir(parents=True,exist_ok=True)
    files={}
    for name,rows in tables.items():
        buffer=io.StringIO(newline='')
        writer=csv.DictWriter(buffer,fieldnames=list(rows[0]),lineterminator='\n')
        writer.writeheader()
        writer.writerows(rows)
        files[name]=buffer.getvalue().encode()
    receipt['outputs_sha256']={name:hashlib.sha256(value).hexdigest() for name,value in files.items()}
    with tempfile.TemporaryDirectory(prefix='.mortality-',dir=OUT) as stage:
        staging=Path(stage)
        for name,value in files.items():
            (staging/name).write_bytes(value)
        (staging/'mortality_pairing_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
        for name in files:
            os.replace(staging/name,OUT/name)
        os.replace(staging/'mortality_pairing_receipt.json',OUT/'mortality_pairing_receipt.json')
    print('PASS crime mortality replacement: current P7 uniform central delta0, both life-year rates and envelope/standalone basis registry')


if __name__=='__main__':
    main()
