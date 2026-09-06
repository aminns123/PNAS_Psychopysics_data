"""Replay the CURRENT supplied figure-code model calculations for diagnosis.

Outputs go to validation/model_replay. They are not certified manuscript model
data: the resonance luminance mapping and the fit targets require clarification.
"""
from pathlib import Path
import csv,json,sys,time,warnings
import numpy as np
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'code/analysis'))
from source_helpers import fitFunctionLimit
from reproduce import read_csv,write_csv
from supplied_model_functions import model_EI_fn,model_psf_function

def main():
    start=time.perf_counter(); dest=ROOT/'validation/model_replay';dest.mkdir(parents=True,exist_ok=True)
    cfg=json.loads((ROOT/'config/model_replay_config.json').read_text())
    conds=json.loads((ROOT/'config/conditions.json').read_text())
    peaks={r['condition_id']:float(r['baseline_fit_peak_cpd']) for r in read_csv(ROOT/'validation/recomputed/csf_fit_metrics.csv')}
    params=[];curves=[];targets=[];diagnostics=[]
    for c in cfg['participants']:
        pid=c['participant_id']; cc=[k for k in conds if k['participant_id']==pid]
        x=[k['luminance_cd_m2'] for k in cc];y=[peaks[k['condition_id']] for k in cc]
        xf=[v for i,v in enumerate(x) if i not in c['excluded_luminance_indices']];yf=[v for i,v in enumerate(y) if i not in c['excluded_luminance_indices']]
        for xx,yy in zip(xf,yf):targets.append({'participant_id':pid,'fit_target':'f_n','luminance_axis_value':xx,'frequency_cpd':yy,'target_type':'peak_of_primary_csf_fit_not_bootstrap_mean'})
        for xx in c['added_luminance_constraints']:
            xf.append(xx);yf.append(y[-1]);targets.append({'participant_id':pid,'fit_target':'f_n','luminance_axis_value':xx,'frequency_cpd':y[-1],'target_type':'auxiliary_constraint_added_in_source_not_an_observation'})
        try:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                xx,yy,pp,_=fitFunctionLimit([1,1000],xf,yf,model_EI_fn,c['initial_fn'],cfg['fn_lower_bounds'],cfg['fn_upper_bounds'],'trf',c['fn_maxfev'])
            for n,v in zip(cfg['fn_parameter_order'],pp.values()):params.append({'participant_id':pid,'fit_target':'f_n','parameter':n,'value':float(v),'status':'new_replay_of_current_source_not_historical_final_fit'})
            for i,(a,b) in enumerate(zip(xx,yy)):curves.append({'participant_id':pid,'fit_target':'f_n','curve_index':i,'luminance_axis_value':float(np.asarray(a).item()),'frequency_cpd':float(np.asarray(b).item()),'branch':'minus','status':'current_source_replay'})
            diagnostics.append({'participant_id':pid,'fit_target':'f_n','status':'executed','warnings':'; '.join(sorted(set(str(w.message) for w in warns)))})
        except Exception as e: diagnostics.append({'participant_id':pid,'fit_target':'f_n','status':'failed','warnings':type(e).__name__+': '+str(e)})
        for n,v in zip(cfg['fr_parameter_order'],c['literal_fr_parameters']):params.append({'participant_id':pid,'fit_target':'f_r','parameter':n,'value':v,'status':'literal_parameter_from_current_supplied_plotting_function'})
        try:
            with warnings.catch_warnings(record=True) as warns:
                warnings.simplefilter('always')
                xx,yy=model_psf_function(c['literal_fr_parameters'],np.linspace(0,40,1000))
            for i,(a,b) in enumerate(zip(xx,yy)):curves.append({'participant_id':pid,'fit_target':'f_r','curve_index':i,'luminance_axis_value':float(a),'frequency_cpd':float(b),'branch':'not_applicable','status':'current_source_replay_unresolved_luminance_mapping'})
            diagnostics.append({'participant_id':pid,'fit_target':'f_r','status':'executed','warnings':'; '.join(sorted(set(str(w.message) for w in warns)))})
        except Exception as e: diagnostics.append({'participant_id':pid,'fit_target':'f_r','status':'failed','warnings':type(e).__name__+': '+str(e)})
        print('Model replay',pid,flush=True)
    for name,rows in [('model_parameters.csv',params),('model_curves.csv',curves),('model_fit_targets.csv',targets),('diagnostics.csv',diagnostics)]:
        if rows: write_csv(dest/name,rows)
    (dest/'run_result.json').write_text(json.dumps({'status':'diagnostic_replay_only','elapsed_seconds':time.perf_counter()-start,'calculations_executed':sum(r['status']=='executed' for r in diagnostics),'calculations_failed':sum(r['status']=='failed' for r in diagnostics),'manuscript_agreement':'unresolved; see MODEL_NOTES.md'},indent=2)+'\n',encoding='utf-8')
if __name__=='__main__':main()
