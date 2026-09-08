# Empirical methods and document evidence

This document describes the CSF and PSF measurements and distinguishes reported experimental methods from computations verified using the deposited files. It does not alter any recorded observation.

## Source documents

The comparison used the author-supplied main paper and supplement labelled 7 September 2026, and the supplied corrected thesis. File hashes and relevant page locations are recorded in [document_provenance.json](config/document_provenance.json). These filenames alone are not evidence of which PDF was uploaded to a submission portal. PDF page numbers below count from the first page, including thesis front matter.

## Experiment as described by the paper and thesis

The main paper, pp. 16-18, and thesis Chapter 4, PDF pp. 159-170 (printed pp. 121-132), describe four observers, binocular viewing at 100 cm with head stabilization, a dark room below 0.5 cd/m2, and a 27-inch 3840 x 2160 display operated at 60 Hz with a central 2560 x 1440 stimulus region. The thesis identifies the monitor as an EIZO ColorEdge CG2700X and the luminance meter as a Konica Minolta LS-150.

The CSF stimulus was a Gaussian-windowed sinusoidal grating with Gaussian standard deviation 1 degree, centred 0.5 degrees to either side of fixation. The reported sequence was 500-ms fixation, followed by a 300-ms grating and a self-paced left/right response. A four-down/one-up staircase used upward and downward steps of 0.36 and 0.30294 log units. The reported termination rule was ten reversals, typically with two to four independent CSF staircases at each spatial frequency. The paper and thesis report ethics approval from the Loughborough University Ethics Review Sub-Committee, Project ID 17492, and written informed consent. That statement alone does not specify the scope of permission for public data reuse.

## Operational contrast and primary CSF calculation

The source analysis uses `(I - I_background) / (1 - I_background)`, where `I` is the recorded source intensity. The thesis, PDF pp. 160-162, distinguishes normalized digital drive from physical luminance and explicitly describes this modified normalization. It also reports that the intensity-to-luminance mapping differed between calibration periods. Thus the source-normalized contrast values must not be relabelled as a separately verified physical luminance-contrast measure.

Source frequency is divided by 31.5 and rounded to three decimal places, following the supplied loader. The included staircases use the original `count_reversals_HighLow` function, the median of the final eight detected values per staircase, the arithmetic mean of thresholds across staircases, and its reciprocal for sensitivity. Thesis Eq. (4.4)-(4.6), PDF p. 168, supports the median/mean/reciprocal sequence. All 255 archived primary CSF observations reproduce exactly.

## Empirical fitting and PSF summaries

The CSF interpolant is `b*exp(-(f-f0)) + a*exp(-((f-f0)/f1)**2)`, with the first exponential scale fixed to 1 cpd. The first exponential is neither squared nor absolute-valued. The free parameters are empirical interpolation coefficients, without a physiological interpretation. The recorded helper uses SciPy's trust-region reflective least-squares fitting. Source-selected frequency exclusions are in [exclusions_log.csv](data/exclusions/exclusions_log.csv).

For each condition, the original saved fit table contains 10,000 candidate peak frequencies and four fit-quality metrics. The retained distribution satisfies inclusive NRMSE bounds 0-0.3 and a strict peak-frequency lower bound of 1.05 cpd. The mean and linear-method 2.5th/97.5th percentiles reproduce the saved-distribution summaries. The interval describes stability under reversal resampling, rather than a population confidence interval. See main-paper p. 18, supplement S5.3 (pp. 10-11), and thesis PDF pp. 169-173.

The 31 condition-level quality-filter and final retention counts in thesis Table 4.5, PDF pp. 171-173 (printed pp. 133-135), match the deposited counts exactly. [thesis_retention_checks.json](validation/thesis_retention_checks.json) preserves the comparison.

## Calibration evidence and remaining acquisition checks

Thesis Appendix A, PDF pp. 242-245 (printed pp. 204-207), describes inverse luminance calibration and two repeated photometric acquisitions near a nominal 10-bit command step. It distinguishes measurable command increments from certification of the complete display pipeline's physical bit depth. Four candidate calibration files are preserved under `data/calibration_reference/` with generic column labels. The thesis description does not by itself identify their definitive column meanings or link each acquisition to each participant session.

Some saved stimulus metadata contain `time_Stimulus = 250`, whereas the reported CSF procedure uses 300 ms. The actual acquisition code and session linkage are needed to resolve whether those values were defaults or executed timings. The deposited metadata are not overwritten by the prose description. Similarly, some staircases have more than ten detected turning points; the detector's relationship to the acquisition stopping counter remains to be established.

The selected saved CSFs contain 7-13 frequency points per condition. Three conditions contain seven points (P01_L200, P01_L300, P02_L026), whereas the thesis describes at least eight. This records the selected archive coverage; it does not assume that unarchived acquisition conditions were never measured.

See [VALIDATION_REPORT.md](VALIDATION_REPORT.md) for the unresolved historical resampling provenance and sampled input-to-fit differences.
