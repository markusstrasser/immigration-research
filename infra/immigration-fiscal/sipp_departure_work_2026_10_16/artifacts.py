"""Aggregate influence diagnostics and a standalone trajectory figure."""
import json

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from extract import CACHE, DERIVED
from measure import cluster_interval


def main():
    p=pd.read_parquet(CACHE/'event_panel.parquet')
    diagnostics={};plotrows=[]
    for route,g in p.groupby('route'):
        z=g.pivot(index=['SSUID','PNUM'],columns='relative_month',values='earnings').dropna()
        diff=z[[0,1,2]].mean(axis=1)-z[[-3,-2,-1]].mean(axis=1)
        bycluster=diff.groupby(level='SSUID').agg(['sum','count'])
        leave=(diff.sum()-bycluster['sum'])/(len(diff)-bycluster['count'])
        largest=diff.loc[diff.abs().sort_values(ascending=False).index]
        diagnostics[route]={'adults':len(diff),'mean_change':diff.mean(),'median_change':diff.median(),
            'largest_absolute_changes_contribution_to_mean':{str(k):largest.iloc[:k].sum()/len(diff) for k in [1,3,5]},
            'leave_one_sample_unit_out_mean_min':leave.min(),'leave_one_sample_unit_out_mean_max':leave.max(),
            'note':'Influence diagnostics after seeing the earnings instability; full-sample estimate retained. No preferred trimmed estimate.'}
        for outcome in ['employment','hours','earnings']:
            z=g.pivot(index=['SSUID','PNUM'],columns='relative_month',values=outcome).dropna()
            baseline=z[[-3,-2,-1]].mean(axis=1)
            for month in range(-3,3):
                delta=z[month]-baseline
                lo,hi=cluster_interval(delta.to_numpy(),z.index.get_level_values('SSUID'))
                plotrows.append({'route':route,'outcome':outcome,'relative_month':month,'adults':len(z),
                                 'change_from_pre_mean':delta.mean(),'ci_low':lo,'ci_high':hi})
    (DERIVED/'influence.json').write_text(json.dumps(diagnostics,indent=2)+'\n')
    data=pd.DataFrame(plotrows)
    data.to_csv(DERIVED/'trajectory_changes.csv',index=False,lineterminator='\n',float_format='%.10g')
    fig,axes=plt.subplots(1,3,figsize=(12,4.4))
    colors={'tracked':'#245780','type2':'#ac5a35'}
    labels={'tracked':'Both adults tracked','type2':'Proxy roster departure'}
    for ax,outcome,title,unit in zip(axes,['employment','hours','earnings'],
            ['Employment','Weekly job hours','Monthly earnings'],
            ['Percentage points','Hours per week','2024 dollars; equal-length months']):
        ax.axhline(0,color='#888888',linewidth=.8)
        ax.axvline(-.5,color='#aaaaaa',linestyle=':',linewidth=1)
        for route in ['tracked','type2']:
            a=data[(data.route==route)&(data.outcome==outcome)]
            scale=100 if outcome=='employment' else 1
            ax.plot(a.relative_month,a.change_from_pre_mean*scale,marker='o',markersize=4,
                    color=colors[route],label=labels[route])
            ax.fill_between(a.relative_month,a.ci_low*scale,a.ci_high*scale,color=colors[route],alpha=.12)
        ax.set_title(title,loc='left',fontsize=12);ax.set_ylabel(unit,fontsize=9)
        ax.set_xticks(range(-3,3));ax.set_xlabel('Month relative to departure',fontsize=9)
        ax.spines[['top','right']].set_visible(False)
    axes[0].legend(frameon=False,fontsize=9,loc='lower left')
    fig.suptitle('Small estimated work changes; earnings vary more',x=.06,ha='left',fontsize=15)
    fig.text(.06,.045,'SIPP reference year 2024. Same-person changes from the three-month pre-departure mean.\n'
             'Tracked: 147 adults (146 for hours); proxy roster: 277. Shading: pointwise 95% cluster bootstrap intervals. Descriptive, not causal.',fontsize=9)
    fig.tight_layout(rect=(.025,.15,1,.90))
    fig.savefig(DERIVED/'trajectories.png',dpi=170)
    fig.savefig(DERIVED/'trajectories.pdf',metadata={'CreationDate':None,'ModDate':None})
    plt.close(fig)
    print(json.dumps(diagnostics,indent=2))


if __name__=='__main__':
    main()
