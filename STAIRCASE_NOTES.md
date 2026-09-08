# Staircase plotting evidence


Its active analysis sets `nRetreat = 8` (source line 299), invokes the same contrast-normalization and reversal-detector helpers (449-450), takes the final eight detected reversals (461-462), and computes both their median and arithmetic mean (464-465). The staircase plots show the median threshold line, and the CSF plotting section compares alternative aggregation choices (901-924). The median-per-staircase and mean-across-staircases combination is independently verified here by exact recovery of all 255 primary CSF values.

The driver also contains legacy generic experiment defaults, including a different active staircase-directory rule. These defaults were not substituted for the explicit four-down/one-up CSF source selection. The file does not settle the discrepancy between the detector's 10/11/12 reversals and the manuscript's stopping description, nor does it establish the historical bootstrap generator.

`python code/make_figures/plot_staircases.py` creates illustrative diagnostics from the deposited data. Its example selection is deterministic (the first included staircase at 10 cd/m2 for each public participant); it is not an asserted original manuscript selection. Each plot shows all trials, all detected reversals, the final eight, and their median.
