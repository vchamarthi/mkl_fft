# Author notes: fix_nd_empty_axes

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/288
- commit: 57c67a5df354ea302e85cc2c6d80637755ce7b99
- base: 1c0abc54562e394cedfa2868ec30b73771bc334b (the fix's parent)
- subject: Fix TypeError with empty axes in FFT functions

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_fft_utils.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_fftnd.py`

## Authoring decision

The oracle and hidden tests combine #288 (fix the TypeError) and #293 (return the input itself and ignore `out`,
as numpy does). #288 alone wrote into `out`, which numpy 2.x does not do; #293 corrected that three days later.
Targets: test_empty_axes, test_empty_axes_with_out, test_empty_axes_returns_same_object (test_fftnd.py as of #293).
