# Intrinsic Organization of Contrast Sensitivity in Human Vision

## Empirical CSF and PSF data and analysis

Alexander Minns, Sergei Gepshtein, Natalia Janson, and Sergey Savel'ev.

This repository contains the paper's empirical contrast sensitivity functions (CSFs), preferred spatial frequencies (PSFs, `f_pref`), deidentified trial records, staircase calculations, saved resampling results, and the code needed to inspect and reproduce the archived empirical summaries. Spatial frequencies are expressed in cycles per degree (cpd).

**Archived release:** [v1.0.0, published 7 September 2026](https://github.com/aminns123/PNAS_Psychopysics_data/releases/tag/v1.0.0), [DOI: 10.5281/zenodo.22644071](https://doi.org/10.5281/zenodo.22644071). This maintenance branch contains later documentation and packaging changes. The version DOI identifies the original archive, not every subsequent GitHub edit. See [RELEASE_NOTES.md](RELEASE_NOTES.md).

## Start here

| What you need | File or folder |
|---|---|
| Measured CSFs and thresholds: 255 observations | [csf_thresholds.csv](data/processed/csf_thresholds.csv) |
| PSF means and percentile intervals: 31 conditions | [preferred_frequency.csv](data/processed/preferred_frequency.csv) |
| All 310,000 saved PSF fits, including excluded rows | [bootstrap_fpref.csv.gz](data/processed/bootstrap_fpref.csv.gz) |
| All saved CSF resampling inputs | [bootstrap_csf](data/processed/bootstrap_csf/) |
| Raw trials, reversals, staircases and stimulus settings | [data/raw](data/raw/) |
| Empirical Figure 2/3 source tables | [figure_source_data](data/processed/figure_source_data/) |
| Six verification figures | [validation/figures](validation/figures/) |
| Column meanings and file integrity | [data_dictionary.csv](data_dictionary.csv), [manifest.csv](manifest.csv) |
| Methods and supporting document evidence | [EMPIRICAL_METHODS.md](EMPIRICAL_METHODS.md) |
| Reproduction results and limits | [VALIDATION_REPORT.md](VALIDATION_REPORT.md) |

## Subjects, measurements and summaries

`P01`-`P04` correspond to manuscript Subjects 1-4. The 31 participant-luminance conditions comprise 12, 6, 7 and 6 conditions respectively. The deposit preserves 41,606 trials, 804 recorded staircases and 8,185 detected reversals. Two flagged staircases are excluded from the primary CSFs but remain in the raw tables. Private source locations and participant linkage are kept outside this repository.

For each included staircase, the primary threshold is the median of its final eight detected reversal values. Thresholds are averaged across staircases at the same spatial frequency, then sensitivity is the reciprocal of that mean. This reproduces all 255 archived primary CSF sensitivities exactly in the recorded environment.

The PSF summary retains saved fits with `0 <= NRMSE <= 0.3` and `f_pref > 1.05` cpd. It reports the arithmetic mean and the 2.5th/97.5th percentiles of retained values. All original saved rows remain available; 287,067 are retained. All 31 retention counts agree with thesis Table 4.5, as recorded in [thesis_retention_checks.json](validation/thesis_retention_checks.json).

**Reproduction scope:** the raw-to-CSF calculation and saved-distribution summaries are verified. The exact historical resampling sequence and the pairing between saved CSF inputs and saved PSF fit rows are not established. Read the [validation report](VALIDATION_REPORT.md) before interpreting row numbers as iteration links. Empirical curves labelled `_recomputed` were evaluated with the supplied current helper and are distinguished from original saved fit results.

## File conventions

CSV files use UTF-8, headers, comma separators, decimal points and `True`/`False` flags. Empty fields mean unknown/not recorded or not applicable, never zero. `.csv.gz` is compressed CSV. Headerless numeric `.tsv.gz` files under `data/raw/source_trials/` and `data/source/` preserve original bytes; their column order is in the dictionary. Source acquisition dates and private linkage fields are excluded from the public metadata.

`source_row` and `saved_fit_row` start at 1. `source_input_index` and `source_point_index` start at 0. Saved input 0 is the deterministic primary CSF; 1-9999 are the additional available inputs. Original saved fit tables already had four decimal places; this repository does not invent missing precision or historical fit-success flags.

## Reproduce the empirical results

Use a fresh copy, Python 3.12, and the pinned dependencies in [requirements.txt](requirements.txt):

```text
python -m pip install -r requirements.txt
python code/run_all.py
```

The driver verifies the archive, reproduces the primary CSFs and PSF summaries, plots empirical results and staircases, and audits a fixed sample of saved input/fit pairs. Outputs go under `validation/`. Verify the manifest before regenerating outputs, since new timings and plots can change their hashes. See [run_all.md](run_all.md) for individual commands, optional resampling and maintenance instructions. Historical software versions and random seeds remain unknown; the observed validation environment is recorded separately.

## Citation and reuse

[CITATION.cff](CITATION.cff) provides the citation for the archived v1.0.0 data release, and [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) supplies accurate scope-specific wording. Record the version or Git commit actually used.

The registered Zenodo metadata lists CC BY 4.0. The earlier repository contained placeholder license files, so the intended data/code coverage still needs author clarification. [LICENSE_DATA.txt](LICENSE_DATA.txt) and [LICENSE_CODE.txt](LICENSE_CODE.txt) record this status without introducing new terms. See [JOURNAL_DATA_CHECKLIST.md](JOURNAL_DATA_CHECKLIST.md) for the remaining release items.
