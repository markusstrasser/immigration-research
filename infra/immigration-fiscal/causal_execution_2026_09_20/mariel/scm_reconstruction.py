"""Independent ordinary SCM, not St Clair allsynth bias-corrected replication.

Input is a reviewed school panel with explicit fiscal_year and donor eligibility.
No automatic fiscal-year conversion or ethnicity/per-person extrapolation.
"""
import argparse,json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.optimize import minimize

def fit(y,x):
    # Scaling changes no minimizer; analytic Jacobian keeps the probe inspectable.
    center=y.mean(); yy=y-center; xx=x-center
    scale=max(float(np.linalg.norm(xx,ord=2)),float(np.linalg.norm(yy)),1.0)
    xx=xx/scale; yy=yy/scale
    def objective(w):
        residual=xx@w-yy
        return float(residual@residual)
    def jac(w): return 2*xx.T@(xx@w-yy)
    fit=minimize(objective,np.full(x.shape[1],1/x.shape[1]),jac=jac,
                 method='SLSQP',bounds=[(0,1)]*x.shape[1],
                 constraints={'type':'eq','fun':lambda w:w.sum()-1,
                              'jac':lambda w:np.ones_like(w)},
                 options={'ftol':1e-15,'maxiter':5000})
    if not fit.success: raise RuntimeError(fit.message)
    if not (np.isfinite(fit.x).all() and abs(fit.x.sum()-1)<1e-7 and fit.x.min()>-1e-7):
        raise ValueError('Optimizer violates simplex')
    return fit.x

def estimate(matrix,target,donors,train,post):
    w=fit(matrix.loc[train,target].to_numpy(),matrix.loc[train,donors].to_numpy())
    gap=matrix[target]-matrix[donors].to_numpy()@w
    rmspe=float(np.sqrt(np.mean(gap.loc[train]**2)))
    if not np.isfinite(rmspe) or rmspe <= 1e-10:
        raise ValueError('Undefined or numerically unstable preperiod standardization')
    return {'mean_log_gap':float(gap.loc[post].mean()),'pre_rmspe':rmspe,
            'post_pre_rmspe_ratio':float(np.sqrt(np.mean(gap.loc[post]**2))/rmspe),
            'standardized_mean_gap':float(gap.loc[post].mean()/rmspe),
            'weights':{str(k):float(v) for k,v in zip(donors,w) if v>1e-7},
            'gaps_by_year':{str(k):float(v) for k,v in gap.items()}}

def main():
    p=argparse.ArgumentParser();p.add_argument('--panel',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--timing-review',type=Path,required=True)
    a=p.parse_args(); review=json.loads(a.timing_review.read_text())
    if not (review.get('fiscal_year_mapping_verified') is True or review.get('explicit_survey_year_diagnostic') is True):
        raise ValueError('Missing fiscal-calendar review or explicit diagnostic status')
    df=pd.read_csv(a.panel,dtype={'ID':str})
    if df.duplicated(['ID','fiscal_year']).any():
        raise ValueError('Duplicate district-years')
    treated='105013001'; pre=list(range(1970,1980)); post=list(range(1981,1991)); years=pre+[1980]+post
    eligible=df[df.donor_eligible.eq(1)].ID.unique().tolist()
    if treated in eligible or len(eligible)<20:
        raise ValueError('Invalid donor pool')
    a.out.mkdir(parents=True,exist_ok=True)
    allresults={}
    outcomes=['Total_Expenditure','Total_Current_Oper','Total_Revenue','Total_Rev_Own_Sources',
              'Total_Taxes','Total_Fed_IG_Revenue','Total_State_IG_Revenue']
    for outcome in outcomes:
        raw=df.pivot(index='fiscal_year',columns='ID',values=outcome).reindex(years)
        usable=[u for u in [treated]+eligible if u in raw and np.isfinite(raw[u]).all() and (raw[u]>0).all()]
        if treated not in usable or len(usable)<20:
            raise ValueError(f'Insufficient complete positive outcomes: {outcome}, {len(usable)}')
        mat=np.log(raw[usable]);donors=[u for u in usable if u!=treated]
        actual=estimate(mat,treated,donors,pre,post)
        actual['ratio_geometric_means_minus_one']=float(np.expm1(actual['mean_log_gap']))
        largest=max(actual['weights'],key=actual['weights'].get)
        leaveout=estimate(mat,treated,[u for u in donors if u!=largest],pre,post)
        holdout=estimate(mat,treated,donors,list(range(1970,1977)),list(range(1977,1980)))
        # The actual treated district cannot supply post-treatment controls.
        placebos={u:estimate(mat,u,[j for j in donors if j!=u],pre,post) for u in donors}
        z=actual['standardized_mean_gap'];r=actual['post_pre_rmspe_ratio']
        one=(1+sum(v['standardized_mean_gap']>=z for v in placebos.values()))/len(usable)
        two=(1+sum(abs(v['standardized_mean_gap'])>=abs(z) for v in placebos.values()))/len(usable)
        rms=(1+sum(v['post_pre_rmspe_ratio']>=r for v in placebos.values()))/len(usable)
        result={'method':'ordinary nonnegative simplex SCM; no allsynth bias correction',
                'timing_review':review,
                'pre_years':pre,'post_years':post,'n_donors':len(donors),
                'dropped_donors_missing_or_nonpositive':sorted(set(eligible)-set(donors)),
                'actual':actual,'p_one_sided_standardized_mean':one,
                'p_two_sided_standardized_mean':two,'p_post_pre_rmspe_ratio':rms,
                'leave_largest_out_id':largest,'leave_largest_out':leaveout,
                'pre_holdout_1977_79':holdout,'placebos':placebos}
        (a.out/f'{outcome}.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
        allresults[outcome]={k:v for k,v in result.items() if k!='placebos'}
        print(outcome,actual['mean_log_gap'],one,two,leaveout['mean_log_gap'],flush=True)
    (a.out/'summary.json').write_text(json.dumps(allresults,indent=2,allow_nan=False)+'\n')

if __name__=='__main__': main()
