"""Refit archived CSF inputs and compare with saved PSF/fit-quality rows.

Default: five fixed input indices per condition. --all evaluates all 310,000
stored inputs and may take many hours. This does not regenerate random draws.
The historical-grid candidate uses min(retained measured frequencies), unlike
the current source helper's 0.1 lower bound. Both are tested explicitly.
"""
from pathlib import Path
import sys, argparse, csv, gzip, json, time, warnings
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'analysis'))
from source_helpers import AoE,fit_to_CSF,goodnessFit_nrmse
from reproduce import write_csv
ROOT=Path(__file__).resolve().parents[2]

def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--all',action='store_true'); args=parser.parse_args()
    indices=set(range(10000)) if args.all else {0,1,1234,5000,9999}
    conditions=json.loads((ROOT/'config/conditions.json').read_text()); result=[]; start=time.perf_counter()
    for c in conditions:
        cid=c['condition_id']; sets={i:[] for i in indices}
        with gzip.open(ROOT/f'data/processed/bootstrap_csf/{cid.lower()}.csv.gz','rt',newline='') as f:
            for r in csv.DictReader(f):
                i=int(r['source_input_index'])
                if i in indices: sets[i].append(r)
        saved=np.loadtxt(ROOT/f'data/source/fitted_psf/{cid.lower()}.tsv.gz')
        for i,rows in sorted(sets.items()):
            kept=[r for r in rows if int(r['source_point_index']) not in c['csf_fit_excluded_source_point_indices']]
            x=[float(r['spatial_frequency_cpd']) for r in kept]; y=[float(r['contrast_sensitivity']) for r in kept]
            rec={'condition_id':cid,'source_input_index':i,'saved_fit_row_compared':i+1,'saved_f_pref_cpd':float(saved[i,0]),'status':'success','error':''}
            try:
                with warnings.catch_warnings():
                    warnings.simplefilter('ignore')
                    xf,yf,pars,peak=fit_to_CSF(x,y,AoE,[],[],[],5000000,'trf')
                rec['current_grid_f_pref_cpd']=float(peak)
                oldx=np.arange(min(x),max(x)+10,(max(x)+10-min(x))/1000)
                oldy=AoE(oldx,*pars.values()); oldpeak=float(oldx[np.argmax(oldy)])
                oldm=goodnessFit_nrmse(np.array(x),np.array(y),oldx,oldy,'mean')
                values=np.array([oldpeak,*oldm])
                delta=np.abs(values-saved[i])
                rec.update({'historical_grid_candidate_f_pref_cpd':oldpeak,'f_pref_absolute_difference_cpd':float(delta[0]),'all_5_metrics_match_after_4dp_rounding':bool(np.array_equal(np.round(values,4),saved[i])),'all_5_metrics_within_0_0001':bool(np.all(delta<=.0001)),'max_metric_absolute_difference':float(delta.max())})
                nearest=np.max(np.abs(saved-values),axis=1); nearest_i=int(np.argmin(nearest))
                rec.update({'nearest_saved_fit_row':nearest_i+1,'nearest_row_max_metric_absolute_difference':float(nearest[nearest_i]),'any_saved_row_matches_all_5_metrics_4dp':bool(np.any(np.all(np.round(values,4)==saved,axis=1)))})
            except Exception as e:
                rec.update({'status':'failure','error':type(e).__name__+': '+str(e)})
            result.append(rec)
        print('Audited',cid,flush=True)
    fields=['condition_id','source_input_index','saved_fit_row_compared','saved_f_pref_cpd','current_grid_f_pref_cpd','historical_grid_candidate_f_pref_cpd','f_pref_absolute_difference_cpd','all_5_metrics_match_after_4dp_rounding','all_5_metrics_within_0_0001','max_metric_absolute_difference','nearest_saved_fit_row','nearest_row_max_metric_absolute_difference','any_saved_row_matches_all_5_metrics_4dp','status','error']
    filename='all_saved_fit_checks.csv' if args.all else 'sample_saved_fit_checks.csv'
    write_csv(ROOT/'validation'/filename,result,fields)
    summary={'fits_checked':len(result),'failures':sum(r['status']=='failure' for r in result),'all_5_metrics_match_4dp':sum(r.get('all_5_metrics_match_after_4dp_rounding',False) for r in result),'all_5_metrics_within_0_0001':sum(r.get('all_5_metrics_within_0_0001',False) for r in result),'max_f_pref_absolute_difference_cpd':max((r.get('f_pref_absolute_difference_cpd',0) for r in result)),'sample_indices':sorted(indices) if not args.all else 'all','runtime_seconds':time.perf_counter()-start,'historical_grid_candidate':'min(x) to max(x)+10, 1000-step arange; inferred from saved metrics; current supplied helper uses 0.1'}
    summary['samples_matching_any_saved_row_at_4dp']=sum(r.get('any_saved_row_matches_all_5_metrics_4dp',False) for r in result)
    (ROOT/'validation'/('all_fit_summary.json' if args.all else 'sample_fit_summary.json')).write_text(json.dumps(summary,indent=2)+'\n',encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
