"""Own observed road-capacity calibration on the preserved source geography.

Native-First: congestion's executed arm and crash's declared affine density
formula; neither producer nor historical source outputs are modified.
"""
import csv
import importlib.util
from functools import lru_cache
import json
from pathlib import Path
import pandas as pd

FISCAL=Path(__file__).resolve().parent.parent


def require(ok,message):
    if not ok:
        raise ValueError('[BLOCKED] oct16 transport: '+message)


@lru_cache(maxsize=1)
def congestion_setup():
    """One read-only native source construction shared by the two comparators."""
    path=FISCAL/'service_response_long_run_2026_09_27/congestion.py'
    spec=importlib.util.spec_from_file_location('oct16_native_congestion',path)
    C=importlib.util.module_from_spec(spec);spec.loader.exec_module(C)
    return C,C.setup()


def build_roads(frame):
    C,(control,nhts,tau,vots,exposures,_)=congestion_setup()
    path=FISCAL/'service_response_long_run_2026_09_27/congestion.py'
    require(control['passed'],'native congestion positive control')
    ex=exposures['2017 southwest'];scope=ex.in_scope.to_numpy()
    before=json.loads((path.parent/'derived/net_change_oct15.json').read_text())
    count=pd.read_csv(FISCAL/'coverage_bound_2026_10_14/derived/line_parts_oct16_cash.csv')
    results={}
    for end in ('low','high'):
        state=frame['sets']['cash']['endpoints'][end]['r']
        cap=next(c for c in state['capital']['components'] if c['id']=='hwy_sl')
        selected=count[(count.scenario=='item16')&(count.end==end)&(count.line=='hwy_sl')]
        delta=float(selected.observed_change_bn.sum())
        rate=frame['sets']['cash']['payload']['meta']['one_rate']['flat_real_equivalent']
        key=cap['key']+delta/(cap['stock_charged_bn']*rate*cap['response'])
        response=before['by_band_end'][end]['highway_response']
        cut=key*response
        require(0<=cut<1,'calibrated capacity cut')
        value=C.arm(ex,scope,ex.s,C.A.POP_FIXED_LANES['central'],C.A.LANES_COEF_T10,
                    cut,tau['central'],vots['central'],2022,nhts['2017 southwest']['r_hours'])
        old=before['pairing_by_end'][end]
        factor=old['replacement_lineage_congestion_bn']/before['by_band_end'][end]['congestion_bn']
        results[end]=dict(old,replacement_lineage_congestion_bn=value*factor,
            lineage_congestion_delta_bn=value*factor-old['baseline_lineage_congestion_bn'],
            lane_cut=cut,before_lane_cut=before['by_band_end'][end]['lane_cut'],
            key_share=key,observed_capital_key_change=delta,
            source_published_after_bn=value,
            rule='Own observed calibration moves the native road key; post-engine missing/completion capacity remains unmeasured as in the source. Original urban traffic geography held; sender/receiver count transport separate.')
    return dict(case='oct16',pairing_by_end=results)


def crash_at_new_capacity(source,roads):
    """Exact affine derivative of the source density-capacity formula, by valuation."""
    valuation='dot_uniform' if source['mortality_valuation']=='uniform' else 'dot_life_years'
    end=source['end'];arm=source['crash_arm']
    path=FISCAL/'road_crash_externality_2026_09_28/derived/capacity_items_oct15.csv'
    rows=[r for r in csv.DictReader(path.open()) if r['end']==end and r['arm']==arm
          and r['valuation']==valuation and float(r['real_discount_rate'])==float(source['real_discount_rate'])
          and r['population']=='lineage']
    require(len(rows)==1,'native crash density row')
    row=rows[0]
    components=[r for r in csv.DictReader((path.parent/'capacity_components_oct15.csv').open())
                if r['end']==end and r['arm']==arm and r['valuation']==valuation
                and float(r['real_discount_rate'])==float(source['real_discount_rate'])]
    require(len(components)==1,'native crash density component')
    component=components[0]
    # This is the executed traffic share, including the VMT/person ratio;
    # a headcount share cannot substitute for it.
    s=float(component['residual_density_share'])/float(component['multiplier'])
    road=roads['pairing_by_end'][end]
    residual=lambda cut:1-(1-s)/(1-cut)
    require(0<s<1 and abs(float(row['central_bn']))>1e-12,'crash derivative support')
    density=float(component['density_fixed_bn'])*float(row['scale_from_union'])
    boundary=float(source['crash_replacement_bn'])/float(row['central_bn'])
    return float(source['crash_replacement_bn'])+density*(residual(road['lane_cut'])-residual(road['before_lane_cut']))/s*boundary
