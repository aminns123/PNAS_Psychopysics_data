"""Rebuild the file inventory after reviewed maintenance changes.

This records current bytes; it does not validate scientific correctness.
Run code/tests/verify_package.py afterwards, before regenerating outputs.
"""
from pathlib import Path
import csv
import hashlib
import os

ROOT = Path(__file__).resolve().parents[2]


def main():
    manifest = ROOT / 'manifest.csv'
    previous = {}
    if manifest.exists():
        with manifest.open(encoding='utf-8', newline='') as handle:
            previous = {r['file_name']: r for r in csv.DictReader(handle)}
    records = []
    for directory, subdirs, files in os.walk(ROOT):
        subdirs[:] = sorted(d for d in subdirs if d not in {'.git', '.venv', '__pycache__'})
        relative = Path(directory).relative_to(ROOT).as_posix()
        if relative == 'validation':
            subdirs[:] = [d for d in subdirs if d != 'new_resampling']
        for name in sorted(files):
            path = Path(directory) / name
            rel = path.relative_to(ROOT).as_posix()
            if rel == 'manifest.csv' or path.suffix in {'.pyc', '.pyo'}:
                continue
            old = previous.get(rel, {})
            if rel.startswith('code/'):
                description, role = 'Empirical analysis, plotting, resampling or package verification code', 'analysis_code'
            elif rel.startswith('validation/'):
                description, role = 'Recorded empirical verification evidence or generated output', 'validation'
            else:
                description, role = 'Package documentation, configuration, provenance or citation information', 'documentation'
            h = hashlib.sha256()
            with path.open('rb') as handle:
                for block in iter(lambda: handle.read(1024 * 1024), b''):
                    h.update(block)
            records.append(dict(file_name=rel, description=old.get('description', description),
                                role=old.get('role', role), size_bytes=path.stat().st_size,
                                sha256=h.hexdigest()))
    with manifest.open('w', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=['file_name', 'description', 'role', 'size_bytes', 'sha256'], lineterminator='\n')
        writer.writeheader()
        writer.writerows(sorted(records, key=lambda r: r['file_name']))
    print(f'Recorded {len(records)} files. The manifest excludes itself and local generated environments/runs.')


if __name__ == '__main__':
    main()
