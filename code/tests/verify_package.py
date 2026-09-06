"""Verify archived file integrity, all saved bootstrap input bytes, and schemas.

Run this before regenerating outputs, which legitimately changes files in
validation/. This checker does not modify any package data.
"""
from pathlib import Path
import argparse,ast,csv,gzip,hashlib,json,re,sys,collections
ROOT=Path(__file__).resolve().parents[2]
def rows(path):
    op=gzip.open if str(path).endswith('.gz') else open
    with op(path,'rt',encoding='utf-8',newline='') as f:yield from csv.DictReader(f)
def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
    return h.hexdigest()

def package_files():
    """Ignore local environments, version-control files and optional new runs."""
    for p in ROOT.rglob('*'):
        rel=p.relative_to(ROOT)
        if any(part in {'.venv','.git','__pycache__'} for part in rel.parts):continue
        if rel.as_posix().startswith('validation/new_resampling/'):continue
        if p.is_file() and p.suffix not in {'.pyc','.pyo'}:yield p
def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--skip-manifest',action='store_true');args=parser.parse_args()
    counts=collections.Counter()
    if not args.skip_manifest:
        listed=set()
        for r in rows(ROOT/'manifest.csv'):
            assert r['file_name'] not in listed,('duplicate manifest entry',r['file_name'])
            listed.add(r['file_name'])
            p=ROOT/r['file_name'];assert p.is_file(),r['file_name'];assert p.stat().st_size==int(r['size_bytes']),r['file_name'];assert digest(p)==r['sha256'],r['file_name'];counts['manifest_files']+=1
        actual={p.relative_to(ROOT).as_posix() for p in package_files() if p.name!='manifest.csv'}
        assert actual==listed,('manifest coverage',sorted(actual-listed),sorted(listed-actual))
    # Exact source-byte reconstruction, including original numeric strings and row order.
    for c in json.loads((ROOT/'config/conditions.json').read_text()):
        cid=c['condition_id']; expected={int(r['source_input_index']):r for r in rows(ROOT/f'validation/bootstrap_source_manifest/{cid.lower()}.csv.gz')}
        path=ROOT/f'data/processed/bootstrap_csf/{cid.lower()}.csv.gz';current=None;buffer=[]
        def check(index,lines):
            e=expected[index]
            candidates=[(newline.join(lines)+tail).encode('utf-8') for newline in ['\r\n','\n'] for tail in ['',newline]]
            assert any(len(b)==int(e['source_bytes']) and hashlib.sha256(b).hexdigest()==e['source_sha256'] for b in candidates),(cid,index)
            counts['bootstrap_source_files_exact_bytes']+=1
        for r in rows(path):
            i=int(r['source_input_index'])
            if current is not None and i!=current:check(current,buffer);buffer=[]
            current=i;assert int(r['source_point_index'])==len(buffer),(cid,i)
            buffer.append(r['spatial_frequency_cpd']+'\t'+r['contrast_sensitivity']);counts['bootstrap_csf_points']+=1
        if current is not None:check(current,buffer)
        assert len(expected)==10000
    # Decompressed raw matrices and saved primary/PSF files match original bytes.
    for r in rows(ROOT/'source_manifest.csv'):
        if r['role'] in ['raw_trial_matrix','primary_csf_source','saved_psf_distribution']:
            b=gzip.decompress((ROOT/r['output_file']).read_bytes());assert hashlib.sha256(b).hexdigest()==r['source_sha256'],r['source_id'];counts['raw_or_saved_source_files_exact_bytes']+=1
    # Every archived PSF row, its quality flags, and its source row number.
    bycondition=collections.defaultdict(list)
    for r in rows(ROOT/'data/processed/bootstrap_fpref.csv.gz'):bycondition[r['condition_id']].append(r)
    for cid,rr in bycondition.items():
        text=gzip.decompress((ROOT/f'data/source/fitted_psf/{cid.lower()}.tsv.gz').read_bytes()).decode()
        source=[line.split() for line in text.splitlines() if line.strip()]
        assert len(source)==len(rr)==10000
        for i,(s,r) in enumerate(zip(source,rr)):
            assert [r[k] for k in ['f_pref_cpd','nrmse','mape_percent','rmse','mae']]==s
            assert int(r['saved_fit_row'])==i+1 and r['fit_success_recorded']==''
            assert (r['retained_for_summary']=='True')==(0<=float(s[1])<=.3 and float(s[0])>1.05)
            counts['psf_rows_exact_tokens']+=1
    assert set(r['participant_id'] for r in rows(ROOT/'data/processed/participants.csv'))=={'P01','P02','P03','P04'}
    for p in (ROOT/'code').rglob('*.py'):ast.parse(p.read_text(encoding='utf-8-sig'));counts['python_files_syntax_checked']+=1
    dictionary={(r['file_name'],r['column_name']) for r in rows(ROOT/'data_dictionary.csv')}
    for p in package_files():
        if p.is_file() and (p.name.endswith('.csv') or p.name.endswith('.csv.gz')) and p.name!='data_dictionary.csv':
            rel=p.relative_to(ROOT).as_posix();op=gzip.open if p.suffix=='.gz' else open
            with op(p,'rt',encoding='utf-8',newline='') as f:fields=next(csv.reader(f))
            assert all((rel,field) in dictionary for field in fields),('dictionary coverage',rel)
            counts['csv_schemas_documented']+=1
    print(json.dumps({'status':'PASS',**dict(counts)},indent=2))
if __name__=='__main__':main()
