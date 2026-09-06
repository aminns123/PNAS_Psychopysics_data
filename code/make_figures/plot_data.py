"""Plot deposited psychophysical observations and recomputed CSF interpolants.
No unresolved recurrent-model curves are added to these verification figures.
"""
from pathlib import Path
import csv,json,sys,os,tempfile
import numpy as np
_cache=tempfile.TemporaryDirectory(prefix='csf_matplotlib_')
os.environ['MPLCONFIGDIR']=_cache.name
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from matplotlib.ticker import ScalarFormatter
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/analysis'))
from reproduce import read_csv

def main():
    dest=ROOT/'validation/figures';dest.mkdir(parents=True,exist_ok=True)
    conditions=json.loads((ROOT/'config/conditions.json').read_text())
    summary=read_csv(ROOT/'data/processed/preferred_frequency.csv')
    curves=read_csv(ROOT/'validation/recomputed/csf_curves.csv')
    plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'savefig.facecolor':'white'})
    colors=['#183e5a','#286354','#654170','#9a5227']
    fig,axes=plt.subplots(2,2,figsize=(10,7.2),layout='constrained')
    for i,ax in enumerate(axes.flat):
        pid=f'P{i+1:02d}'; rows=[r for r in summary if r['participant_id']==pid]
        x=np.array([float(r['luminance_cd_m2']) for r in rows]); y=np.array([float(r['f_pref_mean_cpd']) for r in rows]); lo=np.array([float(r['percentile_2_5_cpd']) for r in rows]); hi=np.array([float(r['percentile_97_5_cpd']) for r in rows])
        ax.vlines(x,lo,hi,color=colors[i],linewidth=1.4);ax.scatter(x,lo,color=colors[i],marker='_');ax.scatter(x,hi,color=colors[i],marker='_');ax.scatter(x,y,color=colors[i],s=32,zorder=3)
        ax.set(xscale='log',xlim=(7,520),ylim=(0,14),xlabel='Mean luminance (cd/m²)',ylabel='Preferred spatial frequency (cycles/degree)')
        ax.set_title(f'Subject {i+1}  ·  {pid}',loc='left',fontweight='bold');ax.set_xticks([10,50,100,200,400]);ax.xaxis.set_major_formatter(ScalarFormatter());ax.grid(axis='y',color='#e5e8ec',lw=.6)
    fig.suptitle('Preferred spatial frequency across luminance',fontsize=17,fontweight='bold')
    fig.supxlabel('Points: retained distribution mean. Bars: 2.5th–97.5th percentiles. Saved data; 10,000 fits per condition.',fontsize=9)
    fig.savefig(dest/'preferred_frequency_all_subjects.png',dpi=180);fig.savefig(dest/'preferred_frequency_all_subjects.svg');plt.close(fig)
    for i in range(4):
        pid=f'P{i+1:02d}'; cc=[c for c in conditions if c['participant_id']==pid]; nr=(len(cc)+3)//4
        fig,axes=plt.subplots(nr,4,figsize=(12,2.75*nr),layout='constrained',squeeze=False)
        for ax,c in zip(axes.flat,cc):
            cid=c['condition_id'];a=np.loadtxt(ROOT/f'data/source/csf_baseline/{cid.lower()}.tsv.gz');cv=[r for r in curves if r['condition_id']==cid]
            ax.plot([float(r['spatial_frequency_cpd']) for r in cv],[float(r['contrast_sensitivity']) for r in cv],color=colors[i],lw=1)
            ax.scatter(a[:,0],a[:,1],c='black',marker='s',s=18,zorder=3)
            ax.set(xscale='log',yscale='log',xlim=(.35,55),ylim=(3,2000),xlabel='Spatial frequency (cycles/degree)',ylabel='Contrast sensitivity')
            ax.set_title(f'{c["luminance_cd_m2"]} cd/m²',loc='left',fontweight='bold');ax.set_xticks([1,10,50]);ax.xaxis.set_major_formatter(ScalarFormatter());ax.grid(color='#e8ebee',lw=.5)
        for ax in list(axes.flat)[len(cc):]: ax.set_visible(False)
        fig.suptitle(f'Subject {i+1} ({pid}): contrast sensitivity functions',fontsize=16,fontweight='bold')
        fig.supxlabel('Points: exact archived CSFs. Lines: interpolation recomputed with the supplied plotting helper.',fontsize=9)
        fig.savefig(dest/f'csf_{pid.lower()}.png',dpi=160);fig.savefig(dest/f'csf_{pid.lower()}.svg');plt.close(fig)
    print('Saved five data-verification figures in validation/figures.')
if __name__=='__main__': main()
