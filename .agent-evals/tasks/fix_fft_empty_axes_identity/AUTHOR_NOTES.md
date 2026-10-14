# Author notes: fix_fft_empty_axes_identity

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/293
- commit: 7b36ab36fe1647c895447ae40092599a73f73f0b
- base: 5a5f1c25e45dc5ee64dfb69707d9637ae507314e (the fix's parent)
- subject: Return input array unchanged when axes=() (ignore out parameter)

## Files changed by the fix

- `mkl_fft/_fft_utils.py` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_repoevals_fix_fft_empty_axes_identity_fftnd.py`: test_empty_axes_with_out, test_empty_axes_returns_same_object
