# Author notes: fix_fft_empty_axes_typeerror

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/288
- commit: 57c67a5df354ea302e85cc2c6d80637755ce7b99
- base: 1c0abc54562e394cedfa2868ec30b73771bc334b (the fix's parent)
- subject: Fix TypeError with empty axes in FFT functions

## Files changed by the fix

- `CHANGELOG.md` (M)
- `mkl_fft/_fft_utils.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_repoevals_fix_fft_empty_axes_typeerror_fftnd.py`: test_empty_axes, test_empty_axes_with_out
