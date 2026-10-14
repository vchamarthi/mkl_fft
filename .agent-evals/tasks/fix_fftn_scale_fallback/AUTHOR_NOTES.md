# Author notes: fix_fftn_scale_fallback

Not shown to the agent under evaluation.

- source: https://github.com/IntelPython/mkl_fft/pull/111
- commit: c13a9a251450ce33d6b6fe29aa5ba17483d7b07d
- base: 6335c5948a4a9a271e1897e14dfc1d8bf05d8efe (the fix's parent)
- subject: Fix gh-109

## Files changed by the fix

- `.github/workflows/conda-package.yml` (M)
- `mkl_fft/_pydfti.pyx` (M)

## Hidden tests (from the fix commit)

- `mkl_fft/tests/test_repoevals_fix_fftn_scale_fallback_fftnd.py`: test_gh109
