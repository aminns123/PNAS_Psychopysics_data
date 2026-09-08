# Reproduce the empirical CSF/PSF results

Start from a fresh copy. All inputs are located relative to the package, without reading the original acquisition folders.

1. Create and activate a Python 3.12 environment. Install `python -m pip install -r requirements.txt`.
2. Run `python code/tests/verify_package.py` to check every manifest file, reconstruct and verify all 310,000 saved CSF source files, compare saved PSF row tokens and flags, and check dictionary coverage.
3. Run `python code/analysis/reproduce.py` to reproduce primary thresholds, all 255 CSF observations and all 31 PSF summaries, and refit the 31 baseline CSFs using the supplied current helper. Results go to `validation/recomputed/`. `--skip-fits` audits only the observations and saved-distribution summaries.
4. Run `python code/make_figures/plot_data.py` for four CSF figures and one PSF figure, and `python code/make_figures/plot_staircases.py` for staircase examples. PNG and SVG outputs go to `validation/figures/`. The staircase script accepts `--condition P01_L010` to show all staircases from one condition.
5. Run `python code/bootstrap/audit_saved_fits.py` to compare five fixed input indices per condition with saved fit results. The 155 comparisons diagnose historical correspondence; successful execution does not imply agreement. `--all` refits all 310,000 stored inputs and writes separate outputs; it may take many hours and was not part of the original preparation.

`python code/run_all.py` runs steps 2-5 in sequence. Runtime is usually around a minute in the observed preparation environment. Numerical results and timings are recorded by the scripts, not assumed from execution alone.

## Verify before regeneration

The manifest records the delivered file bytes. New timings, figures or validation outputs can legitimately change their hashes. Keep an unchanged copy and verify it before regeneration. Scripts do not overwrite the archived source observations or the preserved saved fit distributions.

The repository specifies LF endings for text and preserves binary/compressed files. After an intentional maintenance change, review the changes, run `python code/tools/build_manifest.py`, then verify a fresh Git checkout. Updating the manifest is a maintenance action, not evidence that the scientific analysis has been validated. New table columns also need dictionary entries.

## Optional new resampling

`python code/bootstrap/resample_from_reversals.py --help` describes the separately labelled sensitivity-analysis options. The user must explicitly select a condition, scheme and integer seed. The default is 10,000 new iterations. Each iteration has a success/failure record; output goes to a new `validation/new_resampling/` folder, excluded from version control by default.

This optional program is not the unidentified historical generator and does not replace the saved distributions. It uses the per-staircase median and across-staircase mean, current 0.1-cpd fit grid, and no uniqueness constraint on joint subset vectors. No historical seed is invented.

## Reading the tables

Use ordinary CSV-reading software for headered tables. A `.csv.gz` file is gzip-compressed CSV; Python's `gzip.open(path, 'rt')` reads it without manual extraction. Use `numpy.loadtxt` for the headerless numeric `.tsv.gz` source files. Missing fields, units and original column order are documented in `data_dictionary.csv`.
