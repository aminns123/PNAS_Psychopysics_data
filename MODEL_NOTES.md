# Supplied model code and diagnostic replay

The runnable code in `code/model/` extracts the exact required numerical functions from source `LIB001`. Source names/line ranges are in `config/function_provenance.json`. The selected plotting-function settings are preserved in `config/model_replay_config.json`; their source is `SUP05`.

`validation/model_replay/model_parameters.csv` separates `fit_target = f_n` from `fit_target = f_r`. Intrinsic values are newly optimized in this validation environment with the current plotting workflow. Resonance values are the literal parameter sets present in the supplied plotting functions. Neither status implies verified final manuscript parameters. Parameter units are those of the supplied model parameterization; no physiological units are assigned.

The intrinsic parameter order is `wEE, wEI, wIE, wII, wEe, wEi, wIe, wIi, alpha, rI0, rE0`; the resonance order is `wEE, wEe, wEI, wEi, wIE, wIe, wII, wIi, alpha`. The source wrappers rescale lateral coefficients by `(2*pi)**2` while compensating local coefficients to preserve total couplings, then convert model wavenumbers to ordinary frequencies. This convention must accompany the numbers when comparing parameter sets with manuscript notation.

The minus algebraic branch is used for the intrinsic psychophysical fit. The resonance continuation is seeded from the other intrinsic branch, then selects the signed maximum of the excitatory response. Trial ordinary frequencies are converted to `k=2*pi*f`. The continuation searches a local grid around the previous result; this is not asserted to be a global maximum search over all frequencies.

The current equilibrium solver first attempts a root from the preceding state, uses a fallback grid if needed, and may return the previous state if roots fail. It prefers stable roots when available, otherwise the closest root. These source behaviors are retained, not silently improved. All four intrinsic replays report an unestimated covariance matrix.

The actual intrinsic target rows, including P03 auxiliary constraints, are in `validation/model_replay/model_fit_targets.csv`. The code fits primary-CSF peaks, whereas plotted PSF points are bootstrap-distribution means. It uses specified bounds and initial guesses from the plotting functions. Resonance optimization is not replayed because only final literal parameter values, not a definitive optimization workflow, were identified in those functions.

The manuscript's luminance mapping matches the intrinsic function but differs from the current resonance axis/drive mapping. Consequently, `model_curves.csv` deliberately names its horizontal coordinate `luminance_axis_value`, and its `status` column identifies the unresolved resonance mapping. Do not substitute these diagnostic curves for final paper curves without reconciling the code and manuscript.
