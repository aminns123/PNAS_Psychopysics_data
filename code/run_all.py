"""Run the documented package checks and psychophysical reproduction sequence."""
from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
for script in ['code/tests/verify_package.py','code/analysis/reproduce.py','code/make_figures/plot_data.py','code/make_figures/plot_staircases.py','code/bootstrap/audit_saved_fits.py','code/model/replay_supplied_models.py']:
    print('\nRunning '+script,flush=True)
    subprocess.run([sys.executable,str(ROOT/script)],cwd=ROOT,check=True)
print('Completed. Review VALIDATION_REPORT.md: execution does not certify historical bootstrap or model agreement.')
