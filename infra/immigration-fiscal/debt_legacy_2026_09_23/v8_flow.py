"""Source-classified v8 current flows; never invent financing for unlocated parts.

The historical debt stock is not identified by an annual resource total. The
explicit --current-flow-only reading keeps unidentified payer/timing components
beside cash, capital and displaced beneficiaries. A full stock run fails loudly
until the producer or operator supplies those financing rules.

Native-First: reuses debt_legacy's engine/federal payer ports, the case's native
API and the coverage producer's typed source decomposition; no new estimator.
"""
from __future__ import annotations

import hashlib
import copy
import json
import subprocess
import time
from pathlib import Path

import numpy as np
import pandas as pd

ADOPTION_COMMIT = "b35ac8fb533b26c797abd2e03f3610b79bbadd73"


def require_adopted(fiscal):
    live = json.loads((fiscal / 'live_case.json').read_text())
    summary = json.loads((fiscal / 'main_case_2026_10_15/derived/summary.json').read_text())
    require(live.get('key') == 'oct15' and live.get('adopted') == '2026-10-15'
            and summary.get('v8', {}).get('status') == 'adopted', 'authoritative case is not adopted')


def require(ok, message):
    if not ok:
        raise ValueError("[BLOCKED] v8 debt current-flow contract: " + message)


def coverage_source(d, payload, basis):
    meta = payload["meta"]["coverage"]
    require(not meta.get("stub"), "coverage is STUB")
    path = d.FISCAL / meta["file"]
    data = path.read_bytes()
    require(hashlib.sha256(data).hexdigest() == meta["sha256"], "coverage source bytes changed")
    source = json.loads(data)
    require(source["key"] == "oct15", "coverage source has wrong case")
    require(basis in source["sets"], "coverage needs separately priced set and cash sources")
    for end in ("low", "high"):
        z = source["sets"][basis]["ends"][end]
        require(abs(z["coverage_bn"] - meta["by_end"][end]["total_bn"]) < 1e-9,
                f"coverage {basis}/{end} source/payload total")
        require("decomposition" in z, f"coverage {basis}/{end} typed decomposition absent")
    return source["sets"][basis]


def repaired_corner(d, corner, payload):
    """Copy native parent responses into reporter carriers, on the selected key."""
    c = dict(corner, line_responses=dict(corner.get("line_responses", {})))
    rows = d.lines_at(c).set_index(["side", "id"])
    model = c["model"]
    for cid, source in payload["meta"]["union_completion"]["carriers"].items():
        if source["kind"] != "line":
            continue
        side, parent = source["side"], source["parent_line"]
        require((side, parent) in rows.index, f"reporter carrier {cid} has absent parent {side}/{parent}")
        if side == "receipt":
            selected = model["receipts"]["reference"]
        else:
            line = next(l for l in model["spending"]["lines"] if l["id"] == parent)
            selected = c.get("keys", {}).get(parent, line["preferred_key"])
        c["line_responses"][cid] = float(rows.loc[(side, parent), "response"]) if selected == source["parent_key"] else 0.0
    return c


def native_oracle(d, payloads):
    """Native API is the cross-check, never the Python port's source of totals."""
    js = r'''
const P=require(process.argv[1]), input=JSON.parse(require('fs').readFileSync(0,'utf8'));
const out={};
for(const [basis,pl] of Object.entries(input)) {
 const X=basis==='cash'?P.CASH:P;
 if(JSON.stringify(pl)!==JSON.stringify(X.correctionsPayload()))throw Error('[BLOCKED] package/saved payload differ');
 const m=P.Engine.applyCorrections(P.MODEL,pl);
 out[basis]=X.MAIN_SPECS.map(s=>{const r=X.evaluateFull(m,s);return {cost_bn:r.cost_bn,
 engine_cost_bn:-r.evaluation.welfare_bn,capital_bn:r.capital.total_bn,reading:s.reading,
 lines:Object.fromEntries(r.evaluation.spending.map(l=>['spending:'+l.id,[l.amount_bn,l.response]])
 .concat(r.evaluation.receipts.map(l=>['receipt:'+l.id,[l.amount_bn,l.response]])))};});
}
process.stdout.write(JSON.stringify(out));
'''
    run = subprocess.run(["node", "-e", js, str(d.FISCAL / "main_case_2026_10_15/package.cjs")],
                         input=json.dumps(payloads), capture_output=True, text=True)
    require(run.returncode == 0, "native payload oracle failed: " + run.stderr[-1000:])
    return json.loads(run.stdout)


def source_row(d, corner, source, amount, shares, conv, parent_rows=None):
    """Classify fiscal source lines by the existing government's payer rules."""
    side, parent = source["side"], source["parent_line"]
    phi = shares[conv].loc[d.LAST]
    if parent_rows is not None:
        row = parent_rows.get((side,parent))
        if row is not None and abs(row['responsive_bn'])>1e-12:
            fraction=row['federal_bn']/row['responsive_bn']
            federal=amount*fraction
            return dict(federal_bn=federal,state_local_bn=amount-federal,
                        financing=row['financing'],
                        assumption='source-line current payer ratio transported under the existing convention')
    if parent not in phi.index:
        return None  # composite constants retain an explicit unlocated payer
    if side == "spending" and parent == "general_public_services":
        return None  # finite-removal component mix needs its own traced payer
    if side == "spending" and parent in d.LONG_RUN_LINES:
        return None  # subfunction grants are not the parent average
    financing = "displaced_beneficiaries" if parent in corner["capped"] else "cash"
    fraction = float(phi[parent])
    if parent == d.ENTERPRISE_RECEIPT:
        national = next(l["national_bn"] for l in corner["model"]["receipts"]["lines"] if l["id"] == parent)
        fraction = float(phi["_enterprise_federal_bn"])/national
    if side == "spending" and parent == "school_reprice" and conv == "high":
        fraction = float(phi["_school_high"])
    fed = amount * fraction
    return dict(federal_bn=fed, state_local_bn=amount-fed, financing=financing)


def mixed_source(d,payload,basis):
    """Use explicit federal/state/program declarations; leave composites open."""
    meta=payload['meta']['mixed_unit_removal']
    entry=meta['source']['files']['replicates']
    path=d.ROOT/entry['path']
    with path.open('rb') as stream:
        require(hashlib.file_digest(stream,'sha256').hexdigest()==entry['sha256'],
                'mixed-unit component source hash changed')
    data=pd.read_csv(path)
    known={'M1_federal':('cash',1.0),'M2_state':('cash',0.0),
           'M3_refunds':('cash',1.0),'D_added_residual':('cash',1.0),
           'M5_owner_property':('cash',0.0),'M5_housing_key':('displaced_beneficiaries',1.0)}
    result={}
    for end in ('low','high'):
        rows=[]
        for component,(financing,fedshare) in known.items():
            selected=data[(data.method==basis)&(data.end==end)&(data.component==component)]
            require(len(selected)==3 and set(selected.generation)=={'G1','G2','G3+'},
                    f'mixed {basis}/{end}/{component} generation source incomplete')
            value=float(selected.r0.sum())
            if component=='D_added_residual':
                value*=meta['D_scaling']['scale']
                require(abs(value-meta['by_end'][end]['D_added_residual_bn'])<1e-9,
                        'mixed residual-D source and payload disagree')
            rows.append(dict(component=component,responsive_bn=value,financing=financing,
                             federal_bn=value*fedshare,state_local_bn=value*(1-fedshare)))
        residual=meta['by_end'][end]['total_bn']-sum(r['responsive_bn'] for r in rows)
        rows.append(dict(component='bounded_composites_unlocated',responsive_bn=residual,
                         financing='unlocated',federal_bn=None,state_local_bn=None,
                         reason='M5 consumption, latent mixed-state M6, bounded health/SNAP and their interactions lack a complete exported payer/timing decomposition'))
        require(abs(sum(r['responsive_bn'] for r in rows)-meta['by_end'][end]['total_bn'])<1e-9,
                f'mixed {basis}/{end} source-component closure')
        result[end]=rows
    return result


def classified_rows(d, corner, payload, cov, basis, end, conv, shares, extras, jf, ucf):
    """Every source gets a class or an explicit unidentified bucket."""
    table = d.lines_at(corner)
    carriers = payload["meta"]["union_completion"]["carriers"]
    item=next(it for it in payload['meta']['items'] if it['id']=='union_completion')
    first,count=item['edits']['first'],item['edits']['count']
    native_constant=0.0
    for tag,part in item['parts'].items():
        edit=payload['edits'][first+part['edit']]
        if edit.get('line')=='lane_constants':
            require(edit['side']=='spending' and edit['key']=='k', 'unexpected native constant source')
            if tag.startswith('union_') or 'constants' in corner.get('lineage_constants',()):
                native_constant+=part['by'][corner['allocation']]
    plain = dict(corner, model=dict(corner["model"], spending=dict(corner["model"]["spending"],
                 lines=[copy.deepcopy(l) for l in corner["model"]["spending"]["lines"] if l["id"] not in carriers])))
    constant_line=next(l for l in plain['model']['spending']['lines'] if l['id']=='lane_constants')
    constant_line['keys']['k'][corner['allocation']]['target_bn']-=native_constant
    # The engine cell port splits ordinary lines under its established payer
    # conventions; reporter carriers receive their economic source-side rules.
    before = d.cash_part(d.split_corner(dict(plain, model=d.MODEL), shares[conv], extras,
                     conv, d.LAST, jf, ucf, end))
    constant = d.constant_parts(plain, conv, shares, extras,
                              before.federal_bn.sum()/before.responsive_bn.sum())
    rows = d.split_corner(plain, shares[conv], extras, conv, d.LAST, jf, ucf, end, constant).to_dict("records")
    rows.append(dict(side='native_child_constant',id='union_completion:lane_constants',
                     responsive_bn=native_constant,financing='unlocated',federal_bn=None,state_local_bn=None,
                     reason='native child constant cell has no producer channel/payer decomposition'))
    parent_rows={(r['side'],r['id']):r for r in rows}
    rows += d.capital_split(plain).to_dict("records")
    capmeta = {x["id"]:x for x in payload["meta"]["capital_return"]["components"]}
    for row in table.itertuples():
        if row.id not in carriers or not row.responsive_bn:
            continue
        source = carriers[row.id]
        out = dict(side="reporter_carrier", id=row.id, source_side=source.get("side"),
                   source_line=source["parent_line"], responsive_bn=float(row.responsive_bn))
        if source["kind"] == "capital":
            parent = capmeta[source["parent_line"]]
            fed = out["responsive_bn"] if parent["level"] == "federal" else 0.0
            out.update(financing="resource_cost", federal_bn=fed, state_local_bn=out["responsive_bn"]-fed)
        elif source["kind"] == "line":
            typed = source_row(d, corner, source, out["responsive_bn"], shares, conv,parent_rows)
            if typed:
                out.update(typed)
            else:
                out.update(financing="unlocated", federal_bn=None, state_local_bn=None)
        else:
            require(source["kind"] == "production", "unknown reporter endpoint carrier class")
            out.update(financing="unlocated", federal_bn=None, state_local_bn=None,
                       reason="reporter endpoint total does not separately declare private P and induced F")
        rows.append(out)
    for piece_index,piece in enumerate(cov["ends"][end]["decomposition"]["line_parts"]):
        value = float(piece["coverage_bn"])
        out = dict(side="coverage", id=piece["line"], piece=piece_index, source_line=piece.get("source_line"),
                   source_side=piece.get("source_side"), generation=piece.get("generation"), responsive_bn=value)
        kind = piece["economic_class"]
        if kind == "capital_return":
            fed = value if piece["level"] == "federal" else 0.0
            out.update(financing="resource_cost", federal_bn=fed, state_local_bn=value-fed)
        elif kind == "production":
            rows.append(dict(out, id=piece["line"]+":private_P", responsive_bn=-piece["P_bn"],
                             financing="private_production", federal_bn=0.0, state_local_bn=0.0,
                             assumption="source-generation P/F ratio transport"))
            phi = float(shares[conv].loc[d.LAST, "_induced_receipts"])
            value = -float(piece["F_bn"])
            out.update(responsive_bn=value, financing="cash", federal_bn=value*phi,state_local_bn=value*(1-phi),
                       assumption="source-generation P/F ratio transport; existing induced-receipt government split")
        elif kind == "fiscal_line":
            source = dict(side=piece["source_side"],parent_line=piece["source_line"])
            typed = source_row(d, corner, source, value, shares, conv,parent_rows)
            out.update(typed or dict(financing="unlocated", federal_bn=None, state_local_bn=None))
        else:
            require(kind in ("unclassified_post_engine","unclassified_residual"), "unknown coverage economic class")
            out.update(financing="unlocated", federal_bn=None, state_local_bn=None,
                       reason="coverage source class/payer unresolved")
        rows.append(out)
    for part in payload['_mixed_source'][end]:
        rows.append(dict(part,side='post_engine',id='mixed_unit_removal:'+part['component']))
    p,_ = d.production(corner["normalization"],corner["model"])
    rows.append(dict(side="production", id="private_P", responsive_bn=-p,
                     financing="private_production", federal_bn=0.0, state_local_bn=0.0))
    return [dict(r,basis=basis,end=end,convention=conv) for r in rows]


def separate_timing(rows):
    """Set fiscal dollars are cash plus their actual set-minus-cash difference.

    Do not put earned promises into the cash column. Source keys identify the
    paired rows; a missing cash source keeps the set dollars unlocated.
    """
    def key(r):
        return (r['end'],r['convention'],r['side'],r['id'],r.get('generation'),r.get('piece'),
                r.get('source_line'),r.get('source_side'),r['financing'])
    cash={key(r):r for r in rows if r['basis']=='cash'}
    require(len(cash)==sum(r['basis']=='cash' for r in rows),'cash timing source keys duplicated')
    out=[]
    for source in rows:
        row=dict(source)
        if row['basis']!='set' or row['financing'] not in ('cash','unlocated'):
            out.append(row)
            continue
        mate=cash.get(key(row))
        if mate is None or mate['financing']!=row['financing']:
            row.update(financing='unlocated',federal_bn=None,state_local_bn=None,
                       reason='set fiscal source has no uniquely classified cash counterpart')
            out.append(row)
            continue
        difference=row['responsive_bn']-mate['responsive_bn']
        if abs(difference)<=1e-12:
            out.append(row)
            continue
        accrual=dict(row,id=row['id']+':set_minus_cash',responsive_bn=difference,
                     financing='pension_accrual' if row['financing']=='cash' else 'unlocated',
                     timing_rule='source-set less its separately priced source-cash counterpart; never borrowing')
        for field in ('federal_bn','state_local_bn','union_bn','lineage_bn'):
            accrual[field]=(row[field]-mate[field] if row.get(field) is not None and mate.get(field) is not None else None)
            row[field]=mate.get(field)
        row['responsive_bn']=mate['responsive_bn']
        out.extend((row,accrual))
    for basis in ('set','cash'):
        for end in ('low','high'):
            for conv in {r['convention'] for r in rows}:
                old=sum(r['responsive_bn'] for r in rows if (r['basis'],r['end'],r['convention'])==(basis,end,conv))
                new=sum(r['responsive_bn'] for r in out if (r['basis'],r['end'],r['convention'])==(basis,end,conv))
                require(abs(old-new)<1e-9,f'{basis}/{end}/{conv} set-cash timing closure')
    return out


def coalesce_coverage(rows):
    """Match set/cash by economic source, not their different piece positions.

    The set contains additional tax-on-accrual price pieces absent from cash.
    Their insertion shifts every later numeric piece index. Aggregate pieces
    on the same generation/source/class before taking the timing difference.
    """
    out=[]
    grouped={}
    for source in rows:
        if source['side']!='coverage':
            out.append(source)
            continue
        key=tuple(source.get(k) for k in ('basis','end','convention','id','generation',
                    'source_line','source_side','financing'))
        if key not in grouped:
            grouped[key]=dict(source,source_piece_count=1)
            grouped[key].pop('piece',None)
        else:
            target=grouped[key]
            target['source_piece_count']+=1
            for field in ('responsive_bn','federal_bn','state_local_bn','union_bn','lineage_bn'):
                target[field]=(target[field]+source[field]
                               if target.get(field) is not None and source.get(field) is not None else None)
    out.extend(grouped.values())
    require(abs(sum(r['responsive_bn'] for r in rows)-sum(r['responsive_bn'] for r in out))<1e-9,
            'coverage economic-source coalescence closure')
    return out


def main(d,args):
    require_adopted(d.FISCAL)
    start=time.perf_counter()
    pins=d.check_pins()
    payloads={b:d.case_payload("oct15",b) for b in ("set","cash")}
    coverage={b:coverage_source(d,p,b) for b,p in payloads.items()}
    native=native_oracle(d,payloads)
    for basis,payload in payloads.items():
        payload['_mixed_source']=mixed_source(d,payload,basis)
    wb=d.Workbook(d.BEA/"Section3All_xls.xlsx")
    old=d.later_state("oct14",wb)
    shares,extras=old["run_shares"],old["extras"]
    first=d.case_payload(next(iter(d.LATER_CASES)))
    d.COMPONENTS.clear()
    d.COMPONENTS.update(d.sept26_components(json.loads(d.CORRECTIONS_FILE.read_text()),first))
    d.COMPONENTS['lineage_by_case']={}
    for case in ('oct14','oct15'):
        parts=d.v5_parts(case,d.case_payload(case,'cash'),'cash')
        d.COMPONENTS['lineage_by_case'][case]=dict(row8=parts['row8'],constants=parts['constants'])
    d.COMPONENTS['lineage']=d.COMPONENTS['lineage_by_case']['oct15']
    jf=d.justice_federal(wb)
    ucf=d.uncompensated_federal(float(shares["central"].loc[d.LAST,d.MEDICAID]))
    allrows=[]
    checks=[]
    for basis,payload in payloads.items():
        model=d.apply_corrections(d.MODEL,payload)
        twin=d.union_model('oct15',basis)
        meta=payload["meta"]
        corners=d.frame_corners(d.main_profile("oct15"),model,meta["responses"],"oct15",meta)
        require(len(corners)==len(native[basis]),"specification count mismatch")
        costs=[]
        for i,c in enumerate(corners):
            c=repaired_corner(d,c,payload)
            end=c["reading"]
            post=meta["mixed_unit_removal"]["by_end"][end]["total_bn"]+meta["coverage"]["by_end"][end]["total_bn"]
            cost=d.cost(c)+post
            ref=native[basis][i]
            require(end==ref["reading"],"specification ordering differs")
            require(abs(cost-ref["cost_bn"])<1e-9,f"{basis}/{i} Python/native full-cost parity")
            require(abs(-d.welfare(c)-ref["engine_cost_bn"])<1e-9,f"{basis}/{i} Python/native engine parity")
            for r in d.lines_at(c).itertuples():
                target=ref["lines"][f"{r.side}:{r.id}"]
                require(abs(r.amount_bn-target[0])<1e-9 and abs(r.response-target[1])<1e-12,
                        f"{basis}/{i}/{r.id} source response/amount parity")
            costs.append(cost)
            if i in d.case_oracle("oct15")["ends"]:
                for conv in d.CONVENTIONS:
                    rows=classified_rows(d,c,payload,coverage[basis],basis,end,conv,shares,extras,jf,ucf)
                    require(abs(sum(r["responsive_bn"] for r in rows)-cost)<1e-9,
                            f"{basis}/{end}/{conv} full typed current-flow closure")
                    # R10 union_* versus lineage_* edits and R11 native children
                    # have already been separated by the strict union twin.
                    # Coverage's central added-descendant amount is zero. R12's
                    # only declared added-person term is the D residual.
                    union_payload=copy.deepcopy(payload)
                    mixed=union_payload['meta']['mixed_unit_removal']['by_end'][end]
                    mixed['total_bn']-=mixed['D_added_residual_bn']
                    dpart=next(r for r in union_payload['_mixed_source'][end] if r['component']=='D_added_residual')
                    for field in ('responsive_bn','federal_bn','state_local_bn'):
                        dpart[field]=0.0
                    require(coverage[basis]['parts'][end]['added']['coverage_bn']==0,
                            'central coverage has undeclared added-descendant dollars')
                    tc=repaired_corner(d,dict(c,model=twin,lineage_constants=('row8',)),payload)
                    union_rows=classified_rows(d,tc,union_payload,coverage[basis],basis,end,conv,shares,extras,jf,ucf)
                    row_key=lambda r:(r['side'],r['id'],r.get('piece'))
                    union_keys={row_key(r):r['responsive_bn'] for r in union_rows}
                    require(len(union_keys)==len(union_rows),'union row keys duplicated')
                    for r in rows:
                        key=row_key(r)
                        r['union_bn']=union_keys.pop(key,0.0)
                        r['lineage_bn']=r['responsive_bn']-r['union_bn']
                    require(not union_keys,'union twin contains rows absent from full case')
                    require(abs(sum(r['union_bn']+r['lineage_bn'] for r in rows)-cost)<1e-9,
                            f'{basis}/{end}/{conv} union plus lineage closure')
                    allrows+=rows
            checks.append(dict(basis=basis,spec=i,cost_bn=cost,passed=True))
        want=d.case_oracle("oct15")[basis]
        require(max(abs(a-b) for a,b in zip([min(costs),max(costs)],want))<1e-9,
                f"{basis} adopted band gate")
    timed_rows=separate_timing(coalesce_coverage(allrows))
    for r in timed_rows:
        if r['financing']=='unlocated':
            require(r.get('federal_bn') is None and r.get('state_local_bn') is None,
                    'unlocated financing was given a guessed government')
        else:
            require(np.isfinite(r['federal_bn']) and np.isfinite(r['state_local_bn']),
                    'nonfinite classified government price')
            if r['financing']!='private_production':
                require(abs(r['federal_bn']+r['state_local_bn']-r['responsive_bn'])<1e-9,
                        'classified federal plus state-local source closure')
    frame=pd.DataFrame(timed_rows)
    summary={"case":"oct15","status":"current flows only; historical stocks blocked by unlocated financing",
             "financing_complete":False,"historical_stock_identified":False,
             "case_commit":ADOPTION_COMMIT,"gates":checks,"closure_tolerance_bn":1e-9,
             "source_pins":pins,"bands_bn":{b:d.case_oracle('oct15')[b] for b in ('set','cash')},
             "unlocated_by_set_end_convention":frame[frame.financing=='unlocated'].groupby(
                 ['basis','end','convention']).responsive_bn.sum().to_dict(),
             "population":payloads['set']['meta']['population_v8'],
             "source_rule":"classified source pieces retain their government and timing; no aggregate federal/cash fallback",
             "coverage_production_rule":"producer generation_ratio P/F transport is conditional"}
    grouped=frame.groupby(['basis','end','convention','financing']).responsive_bn.sum()
    summary['financing_totals_bn']={'|'.join(k):float(v) for k,v in grouped.to_dict().items()}
    summary['mixed_population_rule']='Declared D_added_residual booked to added lineage; other surviving-unit components booked to the identified-union route [ASSUMPTION]. Generation totals alone do not identify a further union/lineage split.'
    count_m=d.member_count('oct15')
    summary['per_member_usd']={b:[v*1e3/count_m for v in summary['bands_bn'][b]] for b in ('set','cash')}
    summary['previous_case_bands_bn']={b:d.case_oracle('oct14')[b] for b in ('set','cash')}
    summary['change_from_oct14_bn']={b:[v-old for v,old in zip(summary['bands_bn'][b],
                                  summary['previous_case_bands_bn'][b])] for b in ('set','cash')}
    summary['unlocated_by_set_end_convention']={"|".join(k):v for k,v in summary['unlocated_by_set_end_convention'].items()}
    import sys
    sys.path.insert(0,str(d.FISCAL/'scripts'))
    from memory_budget import require_within_budget
    footprint=require_within_budget('v8 debt current flows')
    out=args.out_dir or d.HERE/'derived/oct15'
    out.mkdir(parents=True,exist_ok=True)
    frame.to_csv(out/'current_flow_source_parts_2024.csv',index=False,lineterminator='\n')
    (out/'current_flow_contract.json').write_text(json.dumps(summary,indent=2,allow_nan=False)+'\n')
    print(f"PASS v8 current-flow source closure {len(checks)} specs; elapsed {time.perf_counter()-start:.3f}s")
    print(f"Peak physical footprint {footprint/1e9:.3f} GB")
    if not args.current_flow_only:
        raise ValueError("[BLOCKED] v8 historical stocks need explicit payer/timing rules for current_flow_contract.json's "
                         "unlocated parts; source-classified current-flow audit saved. Use --current-flow-only for this "
                         "declared partial reading; it does not report a full legacy stock.")
