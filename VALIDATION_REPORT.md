# Empirical CSF/PSF validation report

Updated for the empirical-only repository review on 8 September 2026. The numerical CSF/PSF observations and original saved distributions are preserved. The public v1.0.0 archive was released on 7 September; later maintenance changes are distinguished in [RELEASE_NOTES.md](RELEASE_NOTES.md).

## Verified empirical results

| Check | Evidence |
|---|---|
| Subject selection | Manuscript P01-P04; 12/6/7/6 luminance conditions |
| Raw observations | 41,606 rows; all 16 source numeric columns preserved |
| Staircases and reversals | 804 recorded staircases; 802 included; 8,185 detected reversals |
| Primary CSFs | All 255 saved sensitivities recovered exactly by the final-eight median / across-staircase mean calculation |
| Saved PSF results | All 310,000 rows and all five original numeric fields preserved |
| PSF summary selection | 287,067 retained; 22,933 excluded; all 31 means and percentile intervals reproduced |
| Thesis cross-check | All 31 NRMSE-retained and final-retained counts agree with Table 4.5 |
| Saved CSF inputs | 310,000 source files consolidated into 2,550,000 rows; original bytes reconstructible and checksum-checked |
| Baseline interpolation | 31 fits evaluated with the supplied current helper; separately labelled recomputed curves/parameters |
| Empirical plots | Four CSF figures, one PSF figure and one staircase figure |

The empirical verification programs write their numerical evidence to `validation/recomputed/`. Thesis comparisons are in [thesis_retention_checks.json](validation/thesis_retention_checks.json). [source_manifest.csv](source_manifest.csv) preserves original hashes, and the 31 compressed manifests under `validation/bootstrap_source_manifest/` identify the saved CSF inputs without private locations.

## Historical resampling provenance remains unresolved

The paper and thesis describe eight-of-ten reversal selection without replacement and 10,000 resampling iterations per condition. The available input archive contains index 0, which is identical to the deterministic primary CSF, plus 9,999 additional inputs. No original random seed or generator state was recovered.

All 2,549,745 nonbaseline input point values are compatible with a common eight-element subset of detected indices 1-9 (reversals 2-10), using a median within each staircase and a mean across staircases at a frequency. The first-ten pool contains this pool and can also generate those values. This supports a candidate explanation of the archived values; it does not prove the exact algorithm, independence of choices, or historical random sequence. The supplied generator/fitter settings at preparation time do not uniquely establish the settings that created this eight-reversal archive.

A fixed sample of five input indices per condition (155 total) was refitted. The current helper uses a 0.1-cpd grid lower bound. A separately labelled historical-grid candidate starts at the lowest retained measured frequency. Only 18/155 same-position pairs match all five saved metrics after four-decimal rounding; 21/155 agree within 0.0001. The largest same-position preferred-frequency difference is 5.814 cpd. Searching every saved row finds a matching five-metric row for 37/155 sample inputs. This does not establish a complete input-to-fit mapping.

The audit does not determine whether regeneration, ordering, fit settings or historical software differences caused the mismatch. Saved PSF row numbers therefore remain source row numbers, not verified input-iteration labels. The distributions used for the archived summaries are preserved independently. Historical success flags remain blank where no success log was supplied. See [sample_fit_summary.json](validation/sample_fit_summary.json) and [resampling_pool_audit.json](validation/resampling_pool_audit.json).

## Reversals, exclusions and acquisition evidence

The supplied detector returns 657 staircases with 10 reversals, 143 with 11, two with 12, and two with 9. The two nine-reversal records are the excluded P02/10-cd/m2 staircases. Their exclusion reproduces the primary CSF, but its scientific reason was not recorded. For the 145 included staircases with more than ten detected reversals, the verified calculation uses the final eight detected values. The acquisition stopping counter has not been identified with the detector count by assumption.

Eight existing frequency points are excluded from baseline CSF fitting while remaining in the deposited observations. Two additional out-of-range exclusion indices have no effect. [exclusions_log.csv](data/exclusions/exclusions_log.csv) records both active and inactive exclusions, without inventing rationales.

The thesis supports the primary threshold estimator and supplies more detailed display and calibration descriptions. It does not resolve session-to-calibration linkage, all unused source-column meanings, or the difference between some stored timing values and the reported CSF duration. [EMPIRICAL_METHODS.md](EMPIRICAL_METHODS.md) distinguishes reported methods from verified execution.

## Figures, environment and archive maintenance

Figure 2/3 empirical source tables follow the supplied plotting selection. Exact numerical identity with every point or interpolated curve embedded in a submitted PDF has not been certified. The scope is the empirical CSF and PSF results shown in [figure_coverage.csv](figure_coverage.csv).

The observed validation environment is Python 3.12.14, NumPy 2.5.3, SciPy 1.18.1 and Matplotlib 3.11.1; these are not asserted historical versions. The programs use package-relative inputs. Original top-level scripts that can write into acquisition folders are not executed by the package driver.

The pre-maintenance manifest referred to two deleted documents and did not cover subsequently added files. Git's automatic Windows line endings also changed text bytes. The affected numerical tables were unchanged after line-ending normalization. This review specifies LF checkouts and regenerates the manifest over the revised file set; original compressed source files remain untouched. Verify a fresh copy before running computations that regenerate validation outputs.

The complete five-stage workflow passed on 8 September 2026 from a fresh Git-index checkout made with `core.autocrlf=true`. The initial manifest verification passed in that checkout. All 512 data files are unchanged relative to the pre-maintenance repository apart from text line endings; compressed sources are byte-identical. The citation file passes the official CFF 1.2.0 schema, and the documentation link and package-scope scans pass. See [empirical_repository_checks.json](validation/empirical_repository_checks.json) for the recorded results. Workflow success does not remove the historical resampling limitations described above.

## Remaining empirical and release decisions

Recover the exact historical CSF resampling/fitting source and input pairing if available; clarify the staircase and frequency exclusions, acquisition timing and calibration linkage; confirm the exact submitted manuscript files; and clarify reuse terms. The existing DOI and GitHub release are real, while licensing scope and a bioRxiv preprint identifier are not inferred. [DATA_AVAILABILITY.md](DATA_AVAILABILITY.md) identifies the archive accurately.
