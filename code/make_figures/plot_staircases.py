"""Plot staircase diagnostics from deposited trials and detected reversals.

Default: four illustrative included staircases, one per participant at 10 cd/m2.
Use --condition P01_L010 to plot every staircase in one condition.
Illustrations are generated diagnostics, not identified manuscript figure panels.
"""
from pathlib import Path
import sys,os,tempfile,argparse,collections
import numpy as np
cache=tempfile.TemporaryDirectory(prefix='staircase_matplotlib_');os.environ['MPLCONFIGDIR']=cache.name
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'code/analysis'))
from reproduce import read_csv

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--condition');args=p.parse_args()
    ss=read_csv(ROOT/'data/raw/staircase_summary.csv');tr=read_csv(ROOT/'data/raw/trials.csv.gz');rv=read_csv(ROOT/'data/raw/staircase_reversals.csv')
    if args.condition:selected=[s for s in ss if s['condition_id']==args.condition]
    else:selected=[next(s for s in ss if s['condition_id']==f'P{i:02d}_L010' and s['included_in_primary_csf']=='True') for i in range(1,5)]
    if not selected:raise ValueError('No matching condition')
    dest=ROOT/'validation/figures';dest.mkdir(exist_ok=True,parents=True)
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False})
    for page,start in enumerate(range(0,len(selected),8),1):
        subset=selected[start:start+8];nr=(len(subset)+1)//2
        fig,axs=plt.subplots(nr,2,figsize=(12,3.1*nr),layout='constrained',squeeze=False)
        for ax,s in zip(axs.flat,subset):
            key=s['staircase_id'];ts=sorted([r for r in tr if r['staircase_id']==key],key=lambda r:int(r['trial_within_staircase']));rs=[r for r in rv if r['staircase_id']==key]
            x=[int(r['trial_within_staircase']) for r in ts];y=[float(r['contrast_normalized_source']) for r in ts]
            ax.plot(x,y,c='#234b64',lw=.9,marker='.',ms=3)
            ax.scatter([int(r['trial_within_staircase']) for r in rs],[float(r['contrast_normalized_source']) for r in rs],facecolors='none',edgecolors='#999999',s=45,zorder=3)
            last=[r for r in rs if r['in_last8_point_estimate']=='True']
            ax.scatter([int(r['trial_within_staircase']) for r in last],[float(r['contrast_normalized_source']) for r in last],c='#cb7825',s=24,zorder=4)
            ax.axhline(float(s['threshold_last8_median']),c='#267556',ls='--',lw=1)
            ax.set(yscale='log',xlabel='Trial within staircase (1-based)',ylabel='Normalized source contrast')
            ax.set_title(f'{key} | {s["spatial_frequency_cpd"]} cycles/degree\n{s["n_detected_reversals"]} detected reversals; included: {s["included_in_primary_csf"]}',loc='left',fontsize=10)
            ax.grid(axis='y',color='#e5e8ec',lw=.6)
        for ax in list(axs.flat)[len(subset):]:ax.set_visible(False)
        fig.suptitle('Staircase diagnostics',fontsize=17,fontweight='bold')
        fig.supxlabel('Grey rings: detected reversals. Orange: final eight. Green line: their median.',fontsize=10)
        name='staircase_examples' if not args.condition else f'staircases_{args.condition.lower()}_{page:02d}'
        fig.savefig(dest/(name+'.png'),dpi=160);fig.savefig(dest/(name+'.svg'));plt.close(fig)
    print('Saved staircase diagnostics.')
if __name__=='__main__':main()
