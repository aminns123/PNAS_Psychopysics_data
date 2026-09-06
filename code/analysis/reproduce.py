"""Reproduce the archived psychophysical summaries and audit the raw thresholds.

Run from the repository root: python code/analysis/reproduce.py
Archived observations are read-only. Recomputed output goes to validation/recomputed.
"""
from pathlib import Path
import argparse, collections, csv, gzip, json, platform, sys, time, warnings
import numpy as np
import scipy
from source_helpers import AoE, count_reversals_HighLow, fit_to_CSF, goodnessFit_nrmse

ROOT=Path(__file__).resolve().parents[2]
def read_csv(path):
    opener=gzip.open if str(path).endswith('.gz') else open
    with opener(path,'rt',encoding='utf-8',newline='') as f: return list(csv.DictReader(f))
def write_csv(path,rows,fields=None):
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fields or list(rows[0]),lineterminator='\n'); w.writeheader(); w.writerows(rows)

def summarize(conditions):
    result=[]
    for c in conditions:
        a=np.loadtxt(ROOT/f'data/source/fitted_psf/{c["condition_id"].lower()}.tsv.gz')
        psf,nrmse=a[:,0],a[:,1]
        quality=(nrmse>=0)&(nrmse<=.3); keep=quality&(psf>1.05)
        values=psf[keep]
        result.append({'condition_id':c['condition_id'],'participant_id':c['participant_id'],'luminance_cd_m2':c['luminance_cd_m2'],'f_pref_mean_cpd':float(np.mean(values)),'percentile_2_5_cpd':float(np.percentile(values,2.5,method='linear')),'percentile_97_5_cpd':float(np.percentile(values,97.5,method='linear')),'n_saved_fits':len(a),'n_pass_nrmse':int(quality.sum()),'n_retained':int(keep.sum()),'n_excluded':int((~keep).sum()),'source_id':c['condition_id']+'_FIT'})
    return result

def audit_raw(conditions):
    trials=read_csv(ROOT/'data/raw/trials.csv.gz')
    bycondition={c['condition_id']:c for c in conditions}
    bystair=collections.defaultdict(list)
    for r in trials:
        c=bycondition[r['condition_id']]; bg=c['background_intensity_source']
        assert float(r['contrast_normalized_source'])==(float(r['source_col_06'])-bg)/(1-bg)
        assert float(r['spatial_frequency_cpd'])==round(float(r['source_col_15'])/c['raw_frequency_divisor'],3)
        assert (r['correct']=='True')==(float(r['source_col_01'])==float(r['source_col_02']))
        bystair[r['staircase_id']].append(r)
    deposited={r['staircase_id']:r for r in read_csv(ROOT/'data/raw/staircase_summary.csv')}
    expected_rev=collections.defaultdict(list)
    for r in read_csv(ROOT/'data/raw/staircase_reversals.csv'): expected_rev[r['staircase_id']].append(r)
    computed=collections.defaultdict(list); stair_results=[]
    raw_source_matches=0
    for c in conditions:
      for path in sorted((ROOT/'data/raw/source_trials').glob(c['condition_id'].lower()+'_*.tsv.gz')):
        sid=path.name.split('.')[0].upper(); a=np.loadtxt(path)
        rows=sorted([r for r in trials if r['source_id']==sid],key=lambda r:int(r['source_row']))
        exported=np.asarray([[float(r[f'source_col_{i:02d}']) for i in range(16)] for r in rows])
        assert np.array_equal(a,exported),sid
        raw_source_matches+=len(rows)
    for key,rows in bystair.items():
        rows.sort(key=lambda r:int(r['trial_within_staircase']))
        v=[float(r['contrast_normalized_source']) for r in rows[:200]]
        n,indices,rev=count_reversals_HighLow(v)
        expected=expected_rev[key]
        assert n==len(expected) and np.array_equal(rev,[float(r['contrast_normalized_source']) for r in expected]),key
        assert [i+1 for i in indices]==[int(r['trial_within_staircase']) for r in expected],key
        median=float(np.median(rev[-8:]))
        assert median==float(deposited[key]['threshold_last8_median']),key
        included=deposited[key]['included_in_primary_csf']=='True'
        r=rows[0]
        if included: computed[(r['condition_id'],float(r['spatial_frequency_cpd']))].append(median)
        stair_results.append({'staircase_id':key,'n_reversals':n,'threshold_last8_median':median,'included':included})
    checks=[]
    for r in read_csv(ROOT/'data/processed/csf_thresholds.csv'):
        vals=computed[(r['condition_id'],float(r['spatial_frequency_cpd']))]
        s=float(1/np.mean(vals)); target=float(r['contrast_sensitivity'])
        checks.append({'condition_id':r['condition_id'],'spatial_frequency_cpd':r['spatial_frequency_cpd'],'n_staircases':len(vals),'recomputed_sensitivity':s,'saved_sensitivity':target,'absolute_difference':abs(s-target),'matches_tolerance_1e_12':bool(np.isclose(s,target,rtol=1e-12,atol=1e-12))})
    assert all(r['matches_tolerance_1e_12'] for r in checks)
    return checks,stair_results,raw_source_matches

def baseline_fits(conditions):
    curves=[]; params=[]; metrics=[]
    for c in conditions:
        a=np.loadtxt(ROOT/f'data/source/csf_baseline/{c["condition_id"].lower()}.tsv.gz')
        keep=np.array([i not in c['csf_fit_excluded_source_point_indices'] for i in range(len(a))])
        x,y=a[keep,0].tolist(),a[keep,1].tolist()
        with warnings.catch_warnings(record=True) as warns:
            warnings.simplefilter('always')
            xf,yf,pars,peak=fit_to_CSF(x,y,AoE,[],[],[],5000000,'trf')
        assert np.all(np.isfinite(yf)),c['condition_id']
        m=goodnessFit_nrmse(np.asarray(x),np.asarray(y),xf,yf,'mean')
        metrics.append({'condition_id':c['condition_id'],'baseline_fit_peak_cpd':float(peak),'nrmse':float(m[0]),'n_fit_points':len(x),'grid_min_cpd':.1,'grid_max_exclusive_cpd':max(x)+10,'warning_count':len(warns),'warnings':'; '.join(sorted(set(str(w.message) for w in warns))),'status':'recomputed_with_current_supplied_plotting_helpers'})
        for i,(xx,yy) in enumerate(zip(xf,yf)):
            curves.append({'condition_id':c['condition_id'],'curve_index':i,'spatial_frequency_cpd':float(xx),'contrast_sensitivity':float(yy)})
        for k,name,units in [('x0','b','dimensionless'),('x1','a','dimensionless'),('x2','f1','cycles/degree'),('x3','f0','cycles/degree')]:
            params.append({'condition_id':c['condition_id'],'parameter':name,'value':float(pars[k]),'units':units,'status':'recomputed_current_helpers_not_historical_saved_parameters'})
        print('Fitted',c['condition_id'],flush=True)
    return curves,params,metrics

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--skip-fits',action='store_true',help='Recompute raw thresholds and saved PSF summaries only.')
    args=parser.parse_args(); start=time.perf_counter()
    conditions=json.loads((ROOT/'config/conditions.json').read_text())
    dest=ROOT/'validation/recomputed'; dest.mkdir(exist_ok=True,parents=True)
    summary=summarize(conditions); write_csv(dest/'preferred_frequency.csv',summary)
    reference=ROOT/'data/processed/preferred_frequency.csv'
    if reference.exists():
        ref=read_csv(reference)
        assert len(ref)==len(summary)
        for a,b in zip(ref,summary):
            for k in ['f_pref_mean_cpd','percentile_2_5_cpd','percentile_97_5_cpd']:
                assert float(a[k])==b[k],(a['condition_id'],k)
    raw,stairs,nraw=audit_raw(conditions)
    write_csv(dest/'raw_to_csf_checks.csv',raw); write_csv(dest/'staircase_checks.csv',stairs)
    if not args.skip_fits:
        curves,params,metrics=baseline_fits(conditions)
        write_csv(dest/'csf_curves.csv',curves); write_csv(dest/'csf_fit_parameters.csv',params); write_csv(dest/'csf_fit_metrics.csv',metrics)
    result={'status':'PASS','scope':'raw trials to archived CSF points; saved PSF distributions to preferred-frequency summaries; current-helper baseline fits unless skipped','python':platform.python_version(),'numpy':np.__version__,'scipy':scipy.__version__,'conditions':len(conditions),'trials_numeric_roundtrip_checked':nraw,'staircases_checked':len(stairs),'csf_points_checked':len(raw),'all_csf_points_exactly_equal':all(r['absolute_difference']==0 for r in raw),'saved_psf_rows':sum(r['n_saved_fits'] for r in summary),'retained_psf_rows':sum(r['n_retained'] for r in summary),'runtime_seconds':time.perf_counter()-start,'historical_random_draw_regeneration':'not_claimed','whole_paper_model_reproduction':'not_claimed'}
    (dest/'run_result.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8'); print(json.dumps(result,indent=2))
if __name__=='__main__': main()
