# Intrinsic Organization of Contrast Sensitivity in Human Vision

**Local preparation package, version 0.1.0-preparation, 6 September 2026.**

Alexander Minns, Sergei Gepshtein, Natalia Janson, and Sergey Savel'ev.

This package preserves the CSF (contrast sensitivity function) and PSF (preferred spatial frequency, written `f_pref`) data selected by the supplied plotting code for four manuscript subjects. It contains deidentified raw trials, reversal calculations, original saved CSFs, all saved preferred-frequency fits, resampling inputs, source-data tables, executable analysis, and verification plots.

**The archived data and summaries are verified. Full historical bootstrap and whole-paper model reproducibility are not established.** Read [VALIDATION_REPORT.md](VALIDATION_REPORT.md).

## Start here

| Item | Location |
|---|---|
| Main CSF observations, thresholds and fit flags | [csf_thresholds.csv](data/processed/csf_thresholds.csv) |
| Preferred-frequency means and percentile intervals | [preferred_frequency.csv](data/processed/preferred_frequency.csv) |
| All 310,000 saved PSF fits, including excluded values | [bootstrap_fpref.csv.gz](data/processed/bootstrap_fpref.csv.gz) |
| All 310,000 saved CSF input files, consolidated without loss of numeric precision | [bootstrap_csf](data/processed/bootstrap_csf/) |
| All 41,606 raw trial records | [trials.csv.gz](data/raw/trials.csv.gz) |
| 8,185 detected reversals and 804 staircase summaries | [data/raw](data/raw/) |
| Figure 2 and Figure 3 data selected by the supplied plotting code | [figure_source_data](data/processed/figure_source_data/) |
| Six verification figures | [validation/figures](validation/figures/) |
| Commands and execution limits | [run_all.md](run_all.md) |
| Column definitions | [data_dictionary.csv](data_dictionary.csv) |
| Source-to-output map and source checksums | [source_to_output_mapping.csv](source_to_output_mapping.csv), [source_manifest.csv](source_manifest.csv) |

## Subjects and coverage

`P01`, `P02`, `P03`, and `P04` denote manuscript Subjects 1, 2, 3, and 4 respectively. Original repository participant codes and acquisition dates are retained only in the separate private provenance record. No participant name files or unrelated participant folders were copied into this package.

There are 31 participant-luminance conditions (12, 6, 7, and 6 by subject), 255 primary CSF observations, 804 recorded staircases, and 802 staircases included in the primary CSFs. The two excluded staircases remain in the raw tables. See [participants.csv](data/processed/participants.csv), [conditions.json](config/conditions.json), and [exclusions_log.csv](data/exclusions/exclusions_log.csv).

The experimental data scope is CSF/PSF. It does not include the separate displacement-based ISF data, unrelated experiments, or excluded participants. Model calculations from the supplied Figure 2/3 functions are preserved and replayed for diagnosis under `validation/model_replay/`; they are not certified final model data. Figure 1, physiological Figure 4, and a complete SI reproduction remain outside the completed data scope. [figure_coverage.csv](figure_coverage.csv) records this explicitly.

## File conventions

- Ordinary tables are UTF-8 CSV with a header, comma delimiter, decimal point, and `True`/`False` booleans. `.csv.gz` is ordinary CSV compressed with gzip. Empty fields mean unknown or not recorded, never zero.
- Files under `data/raw/source_trials/`, `data/source/csf_baseline/`, and `data/source/fitted_psf/` preserve the original bytes inside gzip, with pseudonymous filenames. They are headerless tab-separated numeric text; source line endings and source precision remain intact. Column order is in the data dictionary.
- Sanitized key/value metadata in `data/raw/source_metadata/` is headerless UTF-8 tab-separated text. Exact date/linkage keys were removed. All retained values are unchanged strings.
- No values were rounded for this export. The original saved PSF and fit-quality files already contain four decimal places; lost pre-save precision cannot be recovered. Original spatial-frequency conversion rounds to three decimals; that existing convention is retained.
- All psychophysical `f` values are ordinary spatial frequencies in cycles per degree (cpd). Model `k` denotes spatial wavenumber, with `k = 2*pi*f`. Model-reference spatial coefficient conversions are preserved and discussed in [MODEL_NOTES.md](MODEL_NOTES.md).
- `source_row` and `saved_fit_row` start at 1. `source_input_index`, `source_point_index`, and `curve_index` start at 0. Saved input index 0 is the deterministic primary CSF; indices 1-9999 are the available resampled inputs. Saved PSF row numbers are not asserted to be verified input-iteration identifiers.
- `Pxx_Lxxx` identifies participant and luminance, not acquisition order. `S01` is a pseudonymous session label for the selected source folder. `Txxx` identifies a source trial file in stable filename order, not session chronology. `Axx` is the within-file staircase code.

## Verified analysis

The supplied analysis defines normalized source contrast as `(source_col_06 - background_intensity_source) / (1 - background_intensity_source)`. This is the operational quantity used by the source function named `weberContrast`; its physical calibration should not be inferred from the function name alone.

For each included staircase, the original `count_reversals_HighLow` function detects turning points. The primary threshold is the median of its final eight detected reversal values. Thresholds are then averaged across included staircases at the same spatial frequency, and sensitivity is the reciprocal of that mean. This reproduces **all 255 saved CSF sensitivities exactly** in the validation environment. The supplied staircase plotting file independently confirms the median/final-eight calculation.

For the reported PSF summary, all 10,000 saved fit rows per condition are preserved. Retain `0 <= NRMSE <= 0.3` and `f_pref > 1.05` cpd. Report the retained arithmetic mean and the 2.5th/97.5th percentiles (NumPy's linear method). This reproduces the selected saved-distribution summaries; 287,067 of 310,000 estimates are retained. These intervals describe reversal-resampling stability, as stated in the SI, and are not labelled classical population-bootstrap confidence intervals.

The empirical CSF is `b*exp(-(f-f0)) + a*exp(-((f-f0)/f1)**2)` with fixed `f2 = 1` cpd. Current-helper interpolations and fitted coefficients are deposited with `_recomputed` names. They are newly evaluated outputs, separate from the original saved PSF results. Unconstrained parameters have no assigned physiological interpretation.

## Reproduction and environment

Use Python 3.12 and install [requirements.txt](requirements.txt). Validation used Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1, and Matplotlib 3.11.1. These are observed validation versions, not claimed historical versions. [environment_provenance.json](environment_provenance.json) records the distinction and the supplied scripts' broader imports.

From the package root:

```text
python -m pip install -r requirements.txt
python code/run_all.py
```

The driver checks the package, reproduces the raw-to-CSF calculations and saved PSF summaries, plots data and staircase diagnostics, audits a fixed sample of historical fit/input pairs, and replays the supplied model functions. Typical validation steps take seconds to tens of seconds on the preparation machine. The optional full 310,000-fit audit may take many hours. See [run_all.md](run_all.md).

Original random seeds, generator states, and historical package versions were not recovered. The current bootstrap source has different settings, and the available CSF inputs do not have a verified row-for-row connection to the saved fit distributions. The exact distributions remain the authoritative archived results. New resampling code requires an explicit seed and scheme and saves only separately labelled sensitivity analyses.

## Calibration, privacy and provenance

[display_calibration.csv](data/raw/display_calibration.csv) records the selected condition luminances and source display settings; it is not a complete calibration curve. [stimulus_metadata.csv](data/raw/stimulus_metadata.csv) retains recorded settings. Four candidate calibration datasets were found and copied into `data/calibration_reference/`; their association with these sessions and definitive column meanings require author confirmation. See [CALIBRATION_NOTES.md](CALIBRATION_NOTES.md).

The trial matrices are numeric and were checked against the standardized export. Exact acquisition dates, machine-specific paths, personal participant labels, and name files are excluded from the public candidate. Private source locations and linkage are stored separately, outside this directory. This preparation does not assert that consent for public sharing has been confirmed.

[manifest.csv](manifest.csv) records package-file sizes and SHA-256 hashes, excluding itself and runtime caches. [source_manifest.csv](source_manifest.csv) records original source hashes without private paths. The 310,000 bootstrap source hashes are split into 31 compressed manifests in `validation/bootstrap_source_manifest/`. The checker reconstructs their original numeric text and verifies every original checksum.

## Citation and release

[CITATION.cff](CITATION.cff) identifies the paper and authors. A final repository URL, DOI and release date have not been invented. Author contact details are pending. [LICENSE_DATA.txt](LICENSE_DATA.txt) and [LICENSE_CODE.txt](LICENSE_CODE.txt) explicitly mark license selection as pending. Use [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) for proposed manuscript wording after its stated conditions are satisfied.
