# Reproduction sequence

Run these commands from the root of a fresh copy. The code locates package inputs relative to its own location and never reads from the original workstation folders.

1. Create an environment: `python -m venv .venv`. Activate it (`.venv\Scripts\activate` on Windows or `source .venv/bin/activate` on macOS/Linux), then run `python -m pip install -r requirements.txt`.
2. Verify the unmodified package: `python code/tests/verify_package.py`. It checks all manifest hashes, all 310,000 original bootstrap-file checksums reconstructed from the consolidated tables, raw/source-file hashes, PSF row tokens and flags, and dictionary coverage. About 6 seconds before file-manifest verification on the preparation machine.
3. Reproduce primary thresholds, CSF sensitivities and saved PSF summaries: `python code/analysis/reproduce.py`. It also refits all 31 primary CSFs with the current supplied helper. Outputs: `validation/recomputed/`. About 7 seconds. Add `--skip-fits` to audit only raw thresholds and archived summaries.
4. Plot CSFs and PSF distributions: `python code/make_figures/plot_data.py`. Outputs: four CSF panels and one all-subject PSF figure as PNG/SVG in `validation/figures/`. About 8 seconds.
5. Plot staircase diagnostics: `python code/make_figures/plot_staircases.py`. Outputs: one four-example PNG/SVG. Add `--condition P01_L010` to plot every staircase in that condition. About 2 seconds for the examples.
6. Audit historical saved fits against available inputs: `python code/bootstrap/audit_saved_fits.py`. Five fixed indices per condition (155 fits); about 22 seconds. Outputs: `validation/sample_saved_fit_checks.csv` and `sample_fit_summary.json`. This is a diagnostic comparison, not a claim of historical equivalence; read the report. `--all` refits all 310,000 stored inputs and writes separate all-fit files; estimated many hours, not executed during preparation.
7. Replay the current supplied model functions: `python code/model/replay_supplied_models.py`. Outputs: separate `f_n` and `f_r` parameters, curves, actual fitting targets and diagnostics in `validation/model_replay/`. About 5 seconds. This preserves the source workflow for review, including its unresolved manuscript discrepancies. It does not refit the resonance parameters: it evaluates the literal parameter sets found in the plotting functions.

`python code/run_all.py` runs steps 2-7 in sequence. A successful execution means these declared computations ran; it does not establish that the disputed historical inputs or model descriptions are correct.

Regenerated files under `validation/` can change with package versions and include new timing records. Verify the manifest on a fresh copy before regeneration. The deposited files under `data/source/` and `data/processed/bootstrap_csf/` are never overwritten by these commands.

## New resampling, only for a separately labelled sensitivity analysis

`python code/bootstrap/resample_from_reversals.py --help` describes two explicit schemes: the manuscript's first-ten/independent-staircase scheme and the nine-reversal/shared-subset scheme consistent with the archived CSF values. A caller must supply the condition, scheme and their own integer seed. The default number of newly generated iterations is 10,000. Every iteration receives a success/failure record; none is silently dropped. Output goes to a new folder under `validation/new_resampling/`, which is excluded from version control by default.

This new code uses the original operational contrast, per-staircase median and across-staircase mean, but it is not presented as the unidentified historical generator. It does not enforce unique joint subset vectors, unlike the supplied generator helper, and uses the current 0.1-cpd fit grid lower bound. It does not replace either archived dataset.

## Importing data

CSV files can be read by standard statistical software. Python's `csv` and `gzip` modules suffice for plain tables. For example, `gzip.open('data/processed/bootstrap_fpref.csv.gz', 'rt')` yields the CSV text. Use `numpy.loadtxt` for the headerless numeric source `.tsv.gz` files. Do not use an arbitrary row number as a verified link between a saved CSF input and a saved fit; the sample audit demonstrates mismatches.
