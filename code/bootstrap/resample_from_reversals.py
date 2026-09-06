"""Generate a NEW, explicitly seeded sensitivity analysis, not historical draws.

--scheme paper_first10_independent: 8 of detected reversals 1-10, independently
per staircase. --scheme inferred_indices1to9_shared: 8 of detected reversals
2-10, sharing a subset across staircases at one frequency. The latter reproduces
the possible sensitivity values seen in the archived inputs, but the historical
random sequence and exact sampling provenance were not recovered.
"""
from pathlib import Path
import argparse,collections,csv,gzip,json,sys
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/analysis'))
from reproduce import read_csv
from source_helpers import AoE,fit_to_CSF,goodnessFit_nrmse

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--condition',required=True,help='For example P01_L010.')
    p.add_argument('--seed',required=True,type=int)
    p.add_argument('--scheme',required=True,choices=['paper_first10_independent','inferred_indices1to9_shared'])
    p.add_argument('--iterations',type=int,default=10000)
    a=p.parse_args(); assert a.iterations>0
    conditions=json.loads((ROOT/'config/conditions.json').read_text()); c=next(c for c in conditions if c['condition_id']==a.condition)
    included={r['staircase_id']:float(r['spatial_frequency_cpd']) for r in read_csv(ROOT/'data/raw/staircase_summary.csv') if r['condition_id']==a.condition and r['included_in_primary_csf']=='True'}
    stairs=collections.defaultdict(list)
    for r in read_csv(ROOT/'data/raw/staircase_reversals.csv'):
        if r['staircase_id'] in included:stairs[r['staircase_id']].append(float(r['contrast_normalized_source']))
    bysf=collections.defaultdict(list)
    for k,rev in stairs.items():
        if len(rev)<10:raise ValueError('Included staircase has fewer than ten detected reversals: '+k)
        bysf[included[k]].append(np.asarray(rev))
    rng=np.random.default_rng(a.seed);pool=np.arange(10) if a.scheme=='paper_first10_independent' else np.arange(1,10)
    dest=ROOT/'validation/new_resampling'/f'{a.condition.lower()}_{a.scheme}_seed{a.seed}'
    dest.mkdir(parents=True,exist_ok=False)
    with gzip.open(dest/'new_psf_fits.csv.gz','wt',encoding='utf-8',newline='') as f:
        fields=['iteration','f_pref_cpd','nrmse','fit_success','error'];w=csv.DictWriter(f,fields,lineterminator='\n');w.writeheader()
        for i in range(a.iterations):
            x=[];y=[]
            for j,(sf,revs) in enumerate(sorted(bysf.items())):
                subset=rng.choice(pool,8,replace=False)
                th=[float(np.median(r[rng.choice(pool,8,replace=False) if a.scheme=='paper_first10_independent' else subset])) for r in revs]
                if j not in c['csf_fit_excluded_source_point_indices']:x.append(sf);y.append(1/np.mean(th))
            try:
                xf,yf,params,peak=fit_to_CSF(x,y,AoE,[],[],[],5000000,'trf')
                metric=goodnessFit_nrmse(np.array(x),np.array(y),xf,yf,'mean')[0]
                if not np.isfinite(peak) or not np.isfinite(metric):raise ValueError('nonfinite fit output')
                w.writerow({'iteration':i+1,'f_pref_cpd':peak,'nrmse':metric,'fit_success':True,'error':''})
            except Exception as e:w.writerow({'iteration':i+1,'f_pref_cpd':'','nrmse':'','fit_success':False,'error':type(e).__name__+': '+str(e)})
    metadata=vars(a)|{'rng':'numpy.random.default_rng / PCG64','numpy':np.__version__,'status':'new_sensitivity_analysis_not_historical_distribution','threshold_rule':'median per staircase; mean across staircases','grid_lower_bound':.1,'joint_unique_vectors_enforced':False}
    (dest/'run_metadata.json').write_text(json.dumps(metadata,indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
